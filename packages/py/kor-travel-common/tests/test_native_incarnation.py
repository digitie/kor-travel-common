# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"""운영 접속 없이 init 정산의 귀속·보류·실제 native 이벤트를 검증한다."""

import json
import subprocess
import sys
from dataclasses import replace
from pathlib import Path
from types import SimpleNamespace as NS

import pytest
from dagster import (
    DagsterEvent,
    DagsterEventType,
    DagsterInstance,
    DagsterRunStatus,
    DefaultSensorStatus,
    build_sensor_context,
    job,
    op,
)
from dagster._core.remote_origin import (
    GrpcServerCodeLocationOrigin,
    RemoteJobOrigin,
    RemoteRepositoryOrigin,
)

from kortravelcommon import dagster_recovery as recovery

ORIGIN_ID = "a" * 40
BOOT = "00000000-0000-0000-0000-000000000001"
ANCHOR = recovery.ContainerIncarnation(BOOT, 10000, 100, 1000.0, 0.1)


@op
def leaf():
    pass


@job
def sample():
    leaf()


def definition(**kwargs):
    return recovery.native_incarnation_recovery_sensor(
        name="recover_test",
        project="test",
        location_name="test",
        **({"repository_origin_id": ORIGIN_ID} | kwargs),
    )


def record(
    *,
    status=DagsterRunStatus.STARTED,
    start=800.0,
    location="test",
    repository="__repository__",
    project="test",
    origin=True,
    **extra,
):
    run = NS(
        run_id="test-run",
        status=status,
        job_name="sample",
        tags={"kortravelcommon/project": project},
        remote_job_origin=NS(
            job_name="sample",
            repository_origin=NS(
                repository_name=repository,
                get_id=lambda: ORIGIN_ID,
                code_location_origin=NS(location_name=location),
            ),
        )
        if origin
        else None,
    )
    for key, value in extra.items():
        setattr(run, key, value)
    return NS(dagster_run=run, start_time=start)


def eligible(row, anchor=ANCHOR):
    return recovery._candidate(
        row,
        anchor,
        60,
        "test",
        "test",
        "__repository__",
        ORIGIN_ID,
        DagsterRunStatus.STARTED,
    )


@pytest.mark.parametrize(
    "kw",
    [{"status": s} for s in DagsterRunStatus if s != DagsterRunStatus.STARTED]
    + [
        {"start": None},
        {"start": float("nan")},
        {"start": float("inf")},
        {"start": -1},
        {"start": True},
        {"start": 1100},
        {"location": "foreign"},
        {"repository": "foreign"},
        {"project": "foreign"},
        {"origin": False},
        {"tags": {"dagster/code_location": "foreign"}},
        {"tags": {"kortravelcommon/job": "test/another"}},
    ],
)
def test_non_orphan_or_foreign_is_never_failed(kw):
    assert not eligible(record(**kw))


def test_legacy_exact_origin_and_boundary():
    assert eligible(record(tags={}))
    cutoff = ANCHOR.started_at_lower_bound - 60
    assert not eligible(record(start=cutoff))
    assert eligible(record(start=cutoff - 0.001))
    assert not eligible(record(start=ANCHOR.started_at_lower_bound + 1))


@pytest.mark.parametrize(
    "kw",
    [
        {"grace_seconds": 0},
        {"grace_seconds": 59},
        {"grace_seconds": True},
        {"page_size": 101},
        {"page_size": 0},
        {"max_pages_per_tick": 6},
        {"repository_name": ""},
        {"repository_name": " x "},
    ],
)
def test_factory_invalid_budget(kw):
    with pytest.raises(ValueError):
        definition(**kw)


def test_core_import_does_not_import_dagster():
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "import sys; import kortravelcommon.dagster_recovery; "
            "assert 'dagster' not in sys.modules",
        ],
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0


def test_anchor_linux_files_fail_closed(tmp_path, monkeypatch):
    # 합성 proc 자료만 사용한다. 실제 adjtimex나 운영 /proc를 읽지 않는다.
    for name in ["1", "self", "sys/kernel/random", "1/ns", "self/ns"]:
        (tmp_path / "proc" / name).mkdir(parents=True, exist_ok=True)
    (tmp_path / "dockerenv").write_bytes(b"")
    (tmp_path / "proc/1/ns/pid").symlink_to("pid:[1]")
    (tmp_path / "proc/self/ns/pid").symlink_to("pid:[1]")
    for name in ["1/cgroup", "self/cgroup"]:
        (tmp_path / "proc" / name).write_text("0::/owned\n")
    (tmp_path / "proc/sys/kernel/random/boot_id").write_text(BOOT)
    fields = ["S"] + ["0"] * 18 + ["1000"]
    (tmp_path / "proc/1/stat").write_text("1 (init name) " + " ".join(fields))
    (tmp_path / "proc/stat").write_text("btime 1000\n")
    monkeypatch.setattr(
        recovery,
        "Path",
        lambda name: tmp_path / "dockerenv" if name == "/.dockerenv" else tmp_path / "proc",
    )
    monkeypatch.setattr(recovery, "_ntp_error_seconds", lambda: 0.1)
    monkeypatch.setattr(recovery, "_clock_sample", lambda: (1000.1, 2000))
    monkeypatch.setattr(recovery.os, "sysconf", lambda _: 100)
    # lstat root owner는 host가 아닌 이 테스트 process UID와 별개로 합성한다.
    original = Path.lstat
    monkeypatch.setattr(
        Path,
        "lstat",
        lambda p: NS(st_mode=0o100600, st_uid=0) if p == tmp_path / "dockerenv" else original(p),
    )
    assert recovery.read_container_incarnation() is not None
    (tmp_path / "proc/self/cgroup").write_text("0::/foreign\n")
    assert recovery.read_container_incarnation() is None
    (tmp_path / "proc/self/cgroup").write_text("0::/owned\n")
    monkeypatch.setattr(
        recovery, "_ntp_error_seconds", lambda: (_ for _ in ()).throw(OSError("unsynchronized"))
    )
    assert recovery.read_container_incarnation() is None


def invoke(monkeypatch, rows, *, cursor=None, current=None, anchor=ANCHOR):
    calls = []
    fake = NS(
        get_run_records=lambda **kwargs: rows,
        get_run_record_by_id=lambda _: current or rows[0],
        report_run_failed=lambda *args: calls.append(args),
    )
    monkeypatch.setattr(recovery, "read_container_incarnation", lambda: anchor)
    with DagsterInstance.ephemeral() as instance:
        # 실제 sensor wrapper/context를 쓰되 DB·RPC 없는 대역으로 평가한다.
        context = build_sensor_context(instance=instance, cursor=cursor)
        monkeypatch.setattr(instance, "get_run_records", fake.get_run_records)
        monkeypatch.setattr(instance, "get_run_record_by_id", fake.get_run_record_by_id)
        monkeypatch.setattr(instance, "report_run_failed", fake.report_run_failed)
        result = definition().evaluate_tick(context)
    return result, calls


def test_first_tick_and_unknown_do_not_mutate(monkeypatch):
    result, calls = invoke(monkeypatch, [record()])
    assert not calls and result.cursor
    result, calls = invoke(monkeypatch, [record()], cursor=result.cursor, anchor=None)
    assert not calls and result.skip_message


def test_exact_restart_reason_and_no_run_request(monkeypatch):
    cursor = recovery._cursor(ANCHOR, None)
    result, calls = invoke(monkeypatch, [record()], cursor=cursor)
    assert len(calls) == 1
    assert calls[0][2].failure_reason.value == "RUN_WORKER_RESTART"
    assert not result.run_requests


@pytest.mark.parametrize("status", [DagsterRunStatus.SUCCESS, DagsterRunStatus.CANCELED])
def test_terminal_on_final_read_is_preserved(monkeypatch, status):
    result, calls = invoke(
        monkeypatch,
        [record()],
        cursor=recovery._cursor(ANCHOR, None),
        current=record(status=status),
    )
    assert not calls and result.cursor


def test_reloaded_child_does_not_change_anchor_and_clock_jump_abstains(monkeypatch):
    cursor = recovery._cursor(ANCHOR, "last-run")
    result, calls = invoke(
        monkeypatch,
        [record()],
        cursor=cursor,
        anchor=replace(ANCHOR, boot_epoch=1002),
    )
    assert not calls and result.skip_message
    # 동일 init의 clock jump는 새 기준으로 cursor를 덮지 않아 다음 tick도 보류한다.
    result, calls = invoke(
        monkeypatch,
        [record()],
        cursor=cursor,
        anchor=replace(ANCHOR, boot_epoch=1002),
    )
    assert not calls and result.skip_message


def test_paging_bounded_and_failure_does_not_commit_cursor(monkeypatch):
    rows = [record(start=1200) for _ in range(3)]
    for index, row in enumerate(rows):
        row.dagster_run.run_id = str(index)
    after = []
    with DagsterInstance.ephemeral() as instance:
        monkeypatch.setattr(recovery, "read_container_incarnation", lambda: ANCHOR)

        def page(**kwargs):
            after.append(kwargs["cursor"])
            return [rows[len(after) - 1]]

        monkeypatch.setattr(instance, "get_run_records", page)
        sensor = definition(page_size=1, max_pages_per_tick=2)
        result = sensor.evaluate_tick(
            build_sensor_context(
                instance=instance,
                cursor=recovery._cursor(ANCHOR, None),
            )
        )
        assert after == [None, "0"]
        assert json.loads(result.cursor)["after"] == "1"
        monkeypatch.setattr(
            instance,
            "get_run_records",
            lambda **kw: (_ for _ in ()).throw(RuntimeError("metadata unavailable")),
        )
        with pytest.raises(Exception, match="metadata unavailable"):
            sensor.evaluate_tick(build_sensor_context(instance=instance, cursor=result.cursor))


def test_real_sdk_local_run_failure_event_and_replay(monkeypatch):
    origin = RemoteJobOrigin(
        RemoteRepositoryOrigin(
            GrpcServerCodeLocationOrigin(host="127.0.0.1", port=9000, location_name="test"),
            "__repository__",
        ),
        "sample",
    )
    monkeypatch.setattr(recovery, "read_container_incarnation", lambda: ANCHOR)
    with DagsterInstance.ephemeral() as instance:
        run = instance.create_run_for_job(sample, remote_job_origin=origin)
        instance.report_dagster_event(
            DagsterEvent(DagsterEventType.RUN_START.value, job_name="sample"),
            run.run_id,
            timestamp=800.0,
        )
        sensor = definition(repository_origin_id=origin.repository_origin.get_id())
        assert sensor.default_status == DefaultSensorStatus.STOPPED
        cursor = recovery._cursor(ANCHOR, None)
        first = sensor.evaluate_tick(build_sensor_context(instance=instance, cursor=cursor))
        assert instance.get_run_by_id(run.run_id).status == DagsterRunStatus.FAILURE
        events = instance.get_records_for_run(
            run.run_id,
            of_type=DagsterEventType.RUN_FAILURE,
        ).records
        assert len(events) == 1
        assert (
            events[0].event_log_entry.dagster_event.job_failure_data.failure_reason.value
            == "RUN_WORKER_RESTART"
        )
        second = sensor.evaluate_tick(build_sensor_context(instance=instance, cursor=first.cursor))
        assert not second.run_requests
        assert (
            len(
                instance.get_records_for_run(
                    run.run_id,
                    of_type=DagsterEventType.RUN_FAILURE,
                ).records
            )
            == 1
        )
