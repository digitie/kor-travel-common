# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"""컨테이너 재시작으로 유실된 native 실행의 명시적 정산. health에서는 호출하지 않는다."""

import ctypes
import json
import math
import os
import stat
import sys
import time
import uuid
from dataclasses import dataclass
from pathlib import Path

_CLOCK_DRIFT_SECONDS = 1.0


@dataclass(frozen=True)
class ContainerIncarnation:
    """검증된 컨테이너 init과 동기화된 Linux clock의 관측값."""

    boot_id: str
    pid1_start_ticks: int
    ticks_per_second: int
    boot_epoch: float
    clock_error_seconds: float

    def __post_init__(self):
        if str(uuid.UUID(self.boot_id)) != self.boot_id:
            raise ValueError("boot ID가 유효하지 않습니다.")
        if any(
            type(v) is not int or v <= 0 for v in (self.pid1_start_ticks, self.ticks_per_second)
        ):
            raise ValueError("PID1 시작 tick이 유효하지 않습니다.")
        if any(
            type(v) not in (int, float) or not math.isfinite(v)
            for v in (self.boot_epoch, self.clock_error_seconds)
        ):
            raise ValueError("clock 관측이 유효하지 않습니다.")
        if self.boot_epoch <= 0 or not 0 <= self.clock_error_seconds <= 1:
            raise ValueError("clock 오차를 신뢰할 수 없습니다.")

    @property
    def identity(self):
        return self.boot_id, self.pid1_start_ticks, self.ticks_per_second

    @property
    def started_at_lower_bound(self):
        return (
            self.boot_epoch
            + self.pid1_start_ticks / self.ticks_per_second
            - self.clock_error_seconds
            - _CLOCK_DRIFT_SECONDS
        )


def _ntp_error_seconds():
    # Linux 64-bit timex ABI에서 modes=0은 조회만 한다. 다른 ABI는 추정하지 않는다.
    if sys.platform != "linux" or ctypes.sizeof(ctypes.c_long) != 8:
        raise OSError("지원되지 않는 clock ABI입니다.")

    class Timeval(ctypes.Structure):
        _fields_ = [("tv_sec", ctypes.c_long), ("tv_usec", ctypes.c_long)]

    class Timex(ctypes.Structure):
        _fields_ = [
            ("modes", ctypes.c_uint),
            ("offset", ctypes.c_long),
            ("freq", ctypes.c_long),
            ("maxerror", ctypes.c_long),
            ("esterror", ctypes.c_long),
            ("status", ctypes.c_int),
            ("constant", ctypes.c_long),
            ("precision", ctypes.c_long),
            ("tolerance", ctypes.c_long),
            ("time", Timeval),
            ("tick", ctypes.c_long),
            ("ppsfreq", ctypes.c_long),
            ("jitter", ctypes.c_long),
            ("shift", ctypes.c_int),
            ("stabil", ctypes.c_long),
            ("jitcnt", ctypes.c_long),
            ("calcnt", ctypes.c_long),
            ("errcnt", ctypes.c_long),
            ("stbcnt", ctypes.c_long),
            ("tai", ctypes.c_int),
            ("padding", ctypes.c_int * 11),
        ]

    if ctypes.sizeof(Timex) != 208:
        raise OSError("지원되지 않는 timex 크기입니다.")
    value = Timex()
    function = ctypes.CDLL(None, use_errno=True).adjtimex
    function.argtypes = [ctypes.POINTER(Timex)]
    function.restype = ctypes.c_int
    state = function(ctypes.byref(value))
    # leap 진행 중도 보류한다. STA_UNSYNC/STA_CLOCKERR·큰 오차는 정상으로 추정하지 않는다.
    if state != 0 or value.status & (0x40 | 0x1000) or not 0 <= value.maxerror <= 1_000_000:
        raise OSError("clock 동기화가 확인되지 않았습니다.")
    return value.maxerror / 1_000_000


def _clock_sample():
    before = time.clock_gettime(time.CLOCK_BOOTTIME)
    wall = time.time()
    after = time.clock_gettime(time.CLOCK_BOOTTIME)
    if after < before or after - before > 0.1:
        raise OSError("clock 표본의 불확실성이 큽니다.")
    return wall - (before + after) / 2, after


def _start_ticks(raw):
    pid, _, tail = raw.rpartition(")")
    if not pid.startswith("1 ("):
        raise ValueError("PID1 자료가 아닙니다.")
    ticks = int(tail.split()[19])
    if ticks <= 0:
        raise ValueError("PID1 시작 tick이 없습니다.")
    return ticks


def read_container_incarnation():
    """Docker private PID namespace의 Linux init만 읽는다. 불확실하면 None이다.

    host PID namespace를 공유하지 않는 신뢰된 code-server 배포가 선행 조건이다.
    이 함수는 컨테이너 보안 인증이나 과거 NTP 변경 이력을 증명하지 않는다.
    """
    try:
        marker = Path("/.dockerenv").lstat()
        if not stat.S_ISREG(marker.st_mode) or marker.st_uid != 0:
            return None
        proc = Path("/proc")
        if (proc / "1/ns/pid").readlink() != (proc / "self/ns/pid").readlink():
            return None
        group = (proc / "1/cgroup").read_bytes()
        if group != (proc / "self/cgroup").read_bytes() or not group.strip():
            return None
        boot = (proc / "sys/kernel/random/boot_id").read_text().strip()
        ticks = _start_ticks((proc / "1/stat").read_text())
        error = _ntp_error_seconds()
        epoch, uptime = _clock_sample()
        hz = os.sysconf("SC_CLK_TCK")
        btime = [
            row.split()[1]
            for row in (proc / "stat").read_text().splitlines()
            if row.startswith("btime ")
        ]
        if len(btime) != 1 or abs(epoch - int(btime[0])) > 2:
            return None
        epoch_after, _ = _clock_sample()
        if abs(epoch_after - epoch) > 0.1 or ticks / hz > uptime:
            return None
        if boot != (proc / "sys/kernel/random/boot_id").read_text().strip():
            return None
        if ticks != _start_ticks((proc / "1/stat").read_text()):
            return None
        if group != (proc / "1/cgroup").read_bytes():
            return None
        return ContainerIncarnation(boot, ticks, hz, epoch, error)
    except (OSError, ValueError, AttributeError, ZeroDivisionError):
        return None


def _cursor(anchor, after):
    return json.dumps(
        {
            "v": 1,
            "boot": anchor.boot_id,
            "ticks": anchor.pid1_start_ticks,
            "hz": anchor.ticks_per_second,
            "epoch": anchor.boot_epoch,
            "after": after,
        },
        sort_keys=True,
        separators=(",", ":"),
    )


def _decode_cursor(raw):
    if raw is None:
        return None
    value = json.loads(raw)
    if not isinstance(value, dict) or set(value) != {"v", "boot", "ticks", "hz", "epoch", "after"}:
        raise ValueError("복구 cursor 형식이 유효하지 않습니다.")
    if type(value["v"]) is not int or value["v"] != 1:
        raise ValueError("지원하지 않는 복구 cursor입니다.")
    ContainerIncarnation(value["boot"], value["ticks"], value["hz"], value["epoch"], 0)
    if value["after"] is not None and (
        type(value["after"]) is not str or not value["after"] or len(value["after"]) > 128
    ):
        raise ValueError("복구 page cursor가 유효하지 않습니다.")
    return value


def _owned(run, project, location_name, repository_name, repository_origin_id):
    origin = run.remote_job_origin
    if origin is None:
        return False
    repository = origin.repository_origin
    if (
        repository.get_id() != repository_origin_id
        or repository.code_location_origin.location_name != location_name
        or repository.repository_name != repository_name
        or origin.job_name != run.job_name
    ):
        return False
    # 과거 무태그 run은 exact origin으로 귀속한다. 모순된 태그는 받아들이지 않는다.
    tags = run.tags
    return (
        tags.get("kortravelcommon/project", project) == project
        and tags.get("kortravelcommon/job", f"{project}/{run.job_name}")
        == f"{project}/{run.job_name}"
        and tags.get("dagster/code_location", location_name) == location_name
    )


def _candidate(
    record,
    anchor,
    grace,
    project,
    location,
    repository,
    repository_origin_id,
    started_status,
):
    return (
        record.dagster_run.status == started_status
        and type(record.start_time) in (int, float)
        and math.isfinite(record.start_time)
        and 0 < record.start_time < anchor.started_at_lower_bound - grace
        and _owned(record.dagster_run, project, location, repository, repository_origin_id)
    )


def native_incarnation_recovery_sensor(
    *,
    name,
    project,
    location_name,
    repository_origin_id,
    repository_name="__repository__",
    grace_seconds=60,
    page_size=100,
    max_pages_per_tick=5,
):
    """native STARTED의 구 incarnation만 공식 실패 이벤트로 정산한다.

    기본 STOPPED이며 소비자 검증 후 활성화한다. RunRequest·kill·DB 직접 쓰기는 없다.
    최종 재조회와 공식 API 사이 외부 수동 terminal 쓰기는 원자 CAS로 막지 못한다.
    """
    from dagster import (
        DagsterRunStatus,
        DefaultSensorStatus,
        RunsFilter,
        SensorResult,
        SkipReason,
        sensor,
    )
    from dagster._core.events import JobFailureData, RunFailureReason

    for value in (name, project, location_name, repository_name, repository_origin_id):
        if type(value) is not str or not value or value.strip() != value:
            raise ValueError("복구 scope는 비어 있지 않은 문자열이어야 합니다.")
    for value, maximum in ((grace_seconds, 3600), (page_size, 100), (max_pages_per_tick, 5)):
        if type(value) is not int or not 1 <= value <= maximum:
            raise ValueError("복구 예산이 유효하지 않습니다.")
    if grace_seconds < 60:
        raise ValueError("복구 grace는 최소60초여야 합니다.")

    @sensor(name=name, minimum_interval_seconds=60, default_status=DefaultSensorStatus.STOPPED)
    def recover(context):
        anchor = read_container_incarnation()
        if anchor is None:
            return SkipReason("컨테이너 init/clock을 확인하지 못해 정산을 보류합니다.")
        saved = _decode_cursor(context.cursor)
        if saved is not None and saved["boot"] == anchor.boot_id:
            if abs(saved["epoch"] - anchor.boot_epoch) > _CLOCK_DRIFT_SECONDS:
                return SkipReason("clock 기준이 변하여 cursor를 보존하고 정산을 보류합니다.")
        identity = (saved["boot"], saved["ticks"], saved["hz"]) if saved else None
        if identity != anchor.identity:
            # 새 init은 첫 tick에 기록만 한다. 재로드된 user-code child는 이 값을 바꾸지 않는다.
            return SensorResult(cursor=_cursor(anchor, None))
        after = saved["after"]
        started = time.monotonic()
        recovered = 0
        for _ in range(max_pages_per_tick):
            if time.monotonic() - started >= 5:
                break
            records = context.instance.get_run_records(
                filters=RunsFilter(statuses=[DagsterRunStatus.STARTED]),
                limit=page_size,
                cursor=after,
            )
            for record in records:
                if time.monotonic() - started >= 5:
                    return SensorResult(cursor=_cursor(anchor, after))
                if _candidate(
                    record,
                    anchor,
                    grace_seconds,
                    project,
                    location_name,
                    repository_name,
                    repository_origin_id,
                    DagsterRunStatus.STARTED,
                ):
                    fresh_anchor = read_container_incarnation()
                    if (
                        fresh_anchor is None
                        or fresh_anchor.identity != anchor.identity
                        or abs(fresh_anchor.boot_epoch - anchor.boot_epoch) > _CLOCK_DRIFT_SECONDS
                    ):
                        raise RuntimeError("정산 직전 incarnation/clock이 변경됐습니다.")
                    current = context.instance.get_run_record_by_id(record.dagster_run.run_id)
                    if (
                        current is not None
                        and current.start_time == record.start_time
                        and _candidate(
                            current,
                            fresh_anchor,
                            grace_seconds,
                            project,
                            location_name,
                            repository_name,
                            repository_origin_id,
                            DagsterRunStatus.STARTED,
                        )
                    ):
                        context.instance.report_run_failed(
                            current.dagster_run,
                            "이전 컨테이너 init에 속한 run worker 유실을 확인했습니다.",
                            JobFailureData(
                                error=None,
                                failure_reason=RunFailureReason.RUN_WORKER_RESTART,
                            ),
                        )
                        recovered += 1
                after = record.dagster_run.run_id
            if len(records) < page_size:
                after = None
                break
        context.log.info("구 incarnation native 실행 정산: %s건", recovered)
        return SensorResult(cursor=_cursor(anchor, after))

    return recover
