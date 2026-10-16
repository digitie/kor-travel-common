# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"""운영 접속 없이 init 정산의 귀속·보류·실제 native 이벤트를 검증한다."""

import ctypes
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
    DefaultRunLauncher,
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
        tags={
            "kortravelcommon/project": project,
            ".dagster/grpc_info": json.dumps({"host": "127.0.0.1", "port": 9000}),
        },
        remote_job_origin=NS(
            job_name="sample",
            repository_origin=NS(
                repository_name=repository,
                get_id=lambda: ORIGIN_ID,
                code_location_origin=NS(
                    location_name=location,
                    host="127.0.0.1",
                    port=9000,
                    socket=None,
                    use_ssl=None,
                ),
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
    assert eligible(
        record(
            tags={
                ".dagster/grpc_info": json.dumps({"host": "127.0.0.1", "port": 9000}),
            }
        )
    )
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


@pytest.fixture
def anchor_proc(tmp_path, monkeypatch):
    # 합성 proc 자료만 사용한다. 실제 adjtimex나 운영 /proc를 읽지 않는다.
    for name in ["1/task/1", "self", "sys/kernel/random", "1/ns", "self/ns"]:
        (tmp_path / "proc" / name).mkdir(parents=True, exist_ok=True)
    (tmp_path / "dockerenv").write_bytes(b"")
    (tmp_path / "proc/1/ns/pid").symlink_to("pid:[1]")
    (tmp_path / "proc/self/ns/pid").symlink_to("pid:[1]")
    for name in ["1/cgroup", "self/cgroup"]:
        (tmp_path / "proc" / name).write_text("0::/owned\n")
    (tmp_path / "proc/sys/kernel/random/boot_id").write_text(BOOT)
    fields = ["S"] + ["0"] * 18 + ["1000"]
    for name in ["1/stat", "1/task/1/stat"]:
        (tmp_path / "proc" / name).write_text("1 (init name) " + " ".join(fields))
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
    return tmp_path / "proc"


def test_anchor_linux_files_fail_closed(anchor_proc, monkeypatch):
    tmp_path = anchor_proc.parent
    assert recovery.read_container_incarnation() is not None
    (tmp_path / "proc/self/cgroup").write_text("0::/foreign\n")
    assert recovery.read_container_incarnation() is None
    (tmp_path / "proc/self/cgroup").write_text("0::/owned\n")
    monkeypatch.setattr(
        recovery, "_ntp_error_seconds", lambda: (_ for _ in ()).throw(OSError("unsynchronized"))
    )
    assert recovery.read_container_incarnation() is None


def test_anchor_uses_pid1_leader_across_emulated_calling_threads(anchor_proc, monkeypatch):
    # QEMU의 일반 /proc/1/stat rewrite가 호출 스레드별로 달라도 leader는 동일하다.
    original = Path.read_text
    legacy_ticks = iter([1001, 1001, 2001, 2001])
    legacy_reads = []

    def read_text(path, *args, **kwargs):
        if path == anchor_proc / "1/stat":
            legacy_reads.append(path)
            return "1 (emulated thread) " + " ".join(
                ["S"] + ["0"] * 18 + [str(next(legacy_ticks))]
            )
        return original(path, *args, **kwargs)

    monkeypatch.setattr(Path, "read_text", read_text)
    first = recovery.read_container_incarnation()
    second = recovery.read_container_incarnation()
    assert first is not None and second is not None
    assert first.identity == second.identity
    assert first.pid1_start_ticks == 1000
    assert not legacy_reads


@pytest.mark.parametrize(
    "raw",
    [
        "2 (other task) " + " ".join(["S"] + ["0"] * 18 + ["1000"]),
        "1 (init) " + " ".join(["S"] + ["0"] * 18 + ["0"]),
        "1 (init) " + " ".join(["S"] + ["0"] * 18 + ["invalid"]),
        "1 (init) S",
    ],
)
def test_anchor_malformed_leader_does_not_fall_back(anchor_proc, raw):
    (anchor_proc / "1/task/1/stat").write_text(raw)
    assert recovery.read_container_incarnation() is None


def test_anchor_missing_leader_does_not_fall_back(anchor_proc):
    (anchor_proc / "1/task/1/stat").unlink()
    assert recovery.read_container_incarnation() is None


def test_anchor_unstable_leader_fails_closed(anchor_proc, monkeypatch):
    original = Path.read_text
    ticks = iter([1000, 1001])

    def read_text(path, *args, **kwargs):
        if path == anchor_proc / "1/task/1/stat":
            return "1 (init) " + " ".join(["S"] + ["0"] * 18 + [str(next(ticks))])
        return original(path, *args, **kwargs)

    monkeypatch.setattr(Path, "read_text", read_text)
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
        monkeypatch.setattr(instance, "_run_launcher", DefaultRunLauncher())
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
        monkeypatch.setattr(instance, "_run_launcher", DefaultRunLauncher())
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
        monkeypatch.setattr(instance, "_run_launcher", DefaultRunLauncher())
        run = instance.create_run_for_job(sample, remote_job_origin=origin)
        instance.add_run_tags(
            run.run_id,
            {".dagster/grpc_info": json.dumps({"host": "127.0.0.1", "port": 9000})},
        )
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


def test_same_location_foreign_repository_origin_is_not_owned():
    row = record(
        tags={
            ".dagster/grpc_info": json.dumps({"host": "127.0.0.1", "port": 9000}),
        }
    )
    row.dagster_run.remote_job_origin.repository_origin.get_id = lambda: "b" * 40
    assert not eligible(row)


@pytest.mark.parametrize(
    "raw",
    [
        "{}",
        "[]",
        "{",
        json.dumps({"v": 1, "extra": True}),
    ],
)
def test_bad_cursor_abstains_before_writes(monkeypatch, raw):
    with pytest.raises(ValueError):
        invoke(monkeypatch, [record()], cursor=raw)


@pytest.mark.parametrize(
    "state,status,error",
    [
        (-1, 0, 1),
        (1, 0, 1),
        (5, 0, 1),
        (0, 0x40, 1),
        (0, 0x1000, 1),
        (0, 0, -1),
        (0, 0, 1000001),
    ],
)
def test_ntp_unsynchronized_or_error_cannot_be_success(monkeypatch, state, status, error):
    def query(pointer):
        value = pointer._obj
        assert value.modes == 0
        value.status = status
        value.maxerror = error
        return state

    monkeypatch.setattr(recovery.ctypes, "CDLL", lambda *a, **kw: NS(adjtimex=query))
    with pytest.raises(OSError):
        recovery._ntp_error_seconds()


def test_ntp_query_only_valid_abi(monkeypatch):
    def query(pointer):
        assert pointer._obj.modes == 0
        assert ctypes.sizeof(pointer._obj) == 208
        pointer._obj.maxerror = 50000
        return 0

    monkeypatch.setattr(recovery.ctypes, "CDLL", lambda *a, **kw: NS(adjtimex=query))
    assert recovery._ntp_error_seconds() == 0.05


def test_gradual_clock_slew_cannot_move_original_baseline(monkeypatch):
    result, calls = invoke(
        monkeypatch,
        [],
        cursor=recovery._cursor(ANCHOR, None),
        anchor=replace(ANCHOR, boot_epoch=1000.8),
    )
    assert not calls and json.loads(result.cursor)["epoch"] == ANCHOR.boot_epoch
    later, calls = invoke(
        monkeypatch,
        [],
        cursor=result.cursor,
        anchor=replace(ANCHOR, boot_epoch=1001.5),
    )
    assert not calls and later.skip_message


def test_anchor_drift_on_final_read_preserves_native(monkeypatch):
    anchors = iter([ANCHOR, replace(ANCHOR, pid1_start_ticks=10001)])
    monkeypatch.setattr(recovery, "read_container_incarnation", lambda: next(anchors))
    with DagsterInstance.ephemeral() as instance:
        monkeypatch.setattr(instance, "_run_launcher", DefaultRunLauncher())
        monkeypatch.setattr(instance, "get_run_records", lambda **kw: [record()])
        monkeypatch.setattr(instance, "report_run_failed", lambda *a: pytest.fail("mutation"))
        with pytest.raises(Exception, match="incarnation/clock"):
            definition().evaluate_tick(
                build_sensor_context(
                    instance=instance,
                    cursor=recovery._cursor(ANCHOR, None),
                )
            )


def test_partial_failure_replay_rechecks_native_terminal(monkeypatch):
    with DagsterInstance.ephemeral() as instance:
        monkeypatch.setattr(instance, "_run_launcher", DefaultRunLauncher())
        first = record()
        first.dagster_run.run_id = "first"
        second = record()
        second.dagster_run.run_id = "second"
        current = {"first": first, "second": second}
        failures = []
        monkeypatch.setattr(recovery, "read_container_incarnation", lambda: ANCHOR)
        monkeypatch.setattr(instance, "get_run_records", lambda **kw: [first, second])
        monkeypatch.setattr(instance, "get_run_record_by_id", lambda rid: current[rid])

        def fail(run, *args):
            if run.run_id == "second" and not failures:
                raise RuntimeError("metadata failed")
            current[run.run_id] = record(status=DagsterRunStatus.FAILURE)
            failures.append(run.run_id)

        # 첫 실행의 partial 성공을 만든 뒤 둘째 쓰기에서 실패시킨다.
        state = {"second_failed": False}

        def partial(run, *args):
            if run.run_id == "second" and not state["second_failed"]:
                state["second_failed"] = True
                raise RuntimeError("metadata failed")
            fail(run, *args)

        monkeypatch.setattr(instance, "report_run_failed", partial)
        sensor = definition()
        cursor = recovery._cursor(ANCHOR, None)
        with pytest.raises(Exception, match="metadata failed"):
            sensor.evaluate_tick(build_sensor_context(instance=instance, cursor=cursor))
        sensor.evaluate_tick(build_sensor_context(instance=instance, cursor=cursor))
        assert failures == ["first", "second"]


@pytest.mark.parametrize(
    "change",
    [
        {"host": "localhost"},
        {"port": 9001},
        {"use_ssl": False},
    ],
)
def test_same_location_actual_sdk_different_origin_cannot_be_reaped(change):
    options = {"host": "127.0.0.1", "port": 9000, "location_name": "test"}
    original = RemoteRepositoryOrigin(
        GrpcServerCodeLocationOrigin(**options),
        "__repository__",
    )
    foreign = RemoteRepositoryOrigin(
        GrpcServerCodeLocationOrigin(**(options | change)),
        "__repository__",
    )
    assert original.get_id() != foreign.get_id()
    row = record(
        tags={
            ".dagster/grpc_info": json.dumps({"host": "127.0.0.1", "port": 9000}),
        }
    )
    row.dagster_run.remote_job_origin = RemoteJobOrigin(foreign, "sample")
    assert not recovery._candidate(
        row,
        ANCHOR,
        60,
        "test",
        "test",
        "__repository__",
        original.get_id(),
        DagsterRunStatus.STARTED,
    )


def test_recovery_failure_uses_existing_retry_and_preserves_existing_child(monkeypatch):
    from kortravelcommon.dagster import (
        INFRA_RETRY_PARENT_TAG,
        RecoveryPolicy,
        infrastructure_retry_sensor,
    )

    origin = RemoteJobOrigin(
        RemoteRepositoryOrigin(
            GrpcServerCodeLocationOrigin(host="127.0.0.1", port=9000, location_name="test"),
            "__repository__",
        ),
        "sample",
    )
    policy = RecoveryPolicy(300, idempotent=True, infrastructure_retries=1)
    monkeypatch.setattr(recovery, "read_container_incarnation", lambda: ANCHOR)
    with DagsterInstance.ephemeral() as instance:
        monkeypatch.setattr(instance, "_run_launcher", DefaultRunLauncher())
        run = instance.create_run_for_job(
            sample,
            remote_job_origin=origin,
            tags=policy.tags(project="test", job_name="sample"),
        )
        instance.add_run_tags(
            run.run_id,
            {".dagster/grpc_info": json.dumps({"host": "127.0.0.1", "port": 9000})},
        )
        instance.report_dagster_event(
            DagsterEvent(DagsterEventType.RUN_START.value, job_name="sample"),
            run.run_id,
            timestamp=800.0,
        )
        definition(repository_origin_id=origin.repository_origin.get_id()).evaluate_tick(
            build_sensor_context(instance=instance, cursor=recovery._cursor(ANCHOR, None)),
        )
        retry = infrastructure_retry_sensor(
            name="recovery_retry",
            project="test",
            location_name="test",
            job=sample,
            policy=policy,
        )
        first = retry.evaluate_tick(build_sensor_context(instance=instance))
        assert len(first.run_requests) == 1
        assert first.run_requests[0].tags[INFRA_RETRY_PARENT_TAG] == run.run_id
        instance.create_run_for_job(
            sample,
            remote_job_origin=origin,
            tags=first.run_requests[0].tags,
        )
        duplicate = retry.evaluate_tick(build_sensor_context(instance=instance))
        assert not duplicate.run_requests


@pytest.mark.parametrize("kind", ["external", "custom_subclass", "unknown"])
def test_external_custom_unknown_launcher_abstains_before_any_anchor_or_query(monkeypatch, kind):
    from dagster import DefaultRunLauncher

    class CustomLauncher(DefaultRunLauncher):
        pass

    with DagsterInstance.ephemeral() as instance:
        monkeypatch.setattr(instance, "_run_launcher", DefaultRunLauncher())
        original = instance._run_launcher
        launcher = {
            "external": NS(dispose=lambda: None),
            "custom_subclass": CustomLauncher(),
            "unknown": None,
        }[kind]
        monkeypatch.setattr(instance, "_run_launcher", launcher)
        monkeypatch.setattr(
            recovery,
            "read_container_incarnation",
            lambda: pytest.fail("anchor was accessed"),
        )
        monkeypatch.setattr(
            instance,
            "get_run_records",
            lambda **kw: pytest.fail("native metadata was accessed"),
        )
        try:
            result = definition().evaluate_tick(
                build_sensor_context(
                    instance=instance,
                    cursor=recovery._cursor(ANCHOR, None),
                )
            )
            assert result.skip_message and not result.run_requests
        finally:
            instance._run_launcher = original


@pytest.mark.parametrize(
    "raw",
    [
        None,
        "",
        "[]",
        "null",
        "{",
        "{}",
        '{"host":"127.0.0.1","port":"9000"}',
        '{"host":"127.0.0.1","port":true}',
        '{"host":"localhost","port":9000}',
        '{"host":"127.0.0.1","port":9001}',
        '{"host":"127.0.0.1","port":9000,"socket":"/tmp/example.sock"}',
        '{"host":"127.0.0.1","port":9000,"unknown":1}',
        '{"host":"127.0.0.1","port":9000,"use_ssl":false}',
        '{"host":"127.0.0.1","port":9000,"use_ssl":true}',
        '{"host":"foreign","host":"127.0.0.1","port":9000}',
        '{"host":"127.0.0.1","port":9001,"port":9000}',
    ],
)
def test_missing_corrupt_or_contradictory_launcher_history_is_not_reaped(raw):
    assert not eligible(record(tags={".dagster/grpc_info": raw}))


@pytest.mark.parametrize("ssl", [None, False, True])
@pytest.mark.parametrize("socket_mode", [False, True])
def test_actual_default_launcher_tagging_format_without_rpc(monkeypatch, ssl, socket_mode):
    from dagster._grpc.types import StartRunResult
    from dagster._serdes import serialize_value

    options = {
        "host": "127.0.0.1",
        "location_name": "test",
        "use_ssl": ssl,
        **({"socket": "/tmp/example.sock"} if socket_mode else {"port": 9000}),
    }
    location = GrpcServerCodeLocationOrigin(**options)
    origin = RemoteJobOrigin(RemoteRepositoryOrigin(location, "__repository__"), "sample")
    with DagsterInstance.local_temp() as instance:
        run = instance.create_run_for_job(sample, remote_job_origin=origin)
        rpc_calls = []

        def start_run(args):
            rpc_calls.append(args.run_id)
            return serialize_value(
                StartRunResult(success=True, message=None, serializable_error_info=None)
            )

        client = NS(
            host=location.host,
            port=location.port,
            socket=location.socket,
            use_ssl=bool(location.use_ssl),
            start_run=start_run,
        )
        DefaultRunLauncher.launch_run_from_grpc_client(instance, run, client)
        stored = instance.get_run_by_id(run.run_id)
        assert recovery._default_worker_origin(stored)
        expected = {
            "host": "127.0.0.1",
            **({"socket": "/tmp/example.sock"} if socket_mode else {"port": 9000}),
            **({"use_ssl": True} if ssl else {}),
        }
        assert json.loads(stored.tags[".dagster/grpc_info"]) == expected
        assert rpc_calls == [run.run_id]
        # fake RPC 하나로 실제 태그 생산만 검증하며 worker를 시작하지 않는다.
        assert stored.status == DagsterRunStatus.NOT_STARTED
