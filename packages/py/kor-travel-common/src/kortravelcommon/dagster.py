# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"""앱 도메인/DB를 소유하지 않는 Dagster 예약·장애 복구 계약.

`reconciliation_sensor`의 선택 기능(기존 호출은 그대로 동작한다):

- `budget_seconds`: 콜백을 `reconcile(context, remaining)`으로 호출한다. `remaining()`은
  tick 예산의 남은 초(0 이상)이며 콜백은 이를 보고 page 순회를 일찍 멈춘다. 대기는
  `call_with_deadline`으로 같은 예산에서 끊고 sensor 전용 1-slot을 쓴다. 끝나지 않은 이전
  콜백이 slot을 쥐고 있으면 다음 tick은 즉시 `DeadlineExceeded`로 실패한다(겹쳐 실행하지
  않는다). 끊긴 콜백 thread는 종료되지 않으므로 콜백은 자체 statement/lock timeout을 둔다.
  Dagster의 sensor 평가 상한(기본 60초)보다 작게 잡는다.
- `on_stall`: 켜면 콜백 예외로 tick을 실패시키지 않고 `context.log`에 남긴 뒤 정체 시계
  (`kortravelcommon.stall`)에 기록한다. 시계는 sensor cursor에 두며 모든 반환 경로에서
  cursor를 커밋한다. 실패 서명은 예외 형식 이름과 SQLSTATE뿐이다(원문 message 제외).
  첫 실패 뒤 `stall_after_seconds`가 지나면 `on_stall(context, clock)`을 부르고,
  이후 `realert_after_seconds`마다 다시 부른다. `on_stall`이 실패하면 경보하지 않은
  것으로 두어 다음 tick에 재시도한다. 콜백이 성공하면 시계를 지운다.
  cursor가 손상되면 경고 후 새 시계로 시작한다(경보가 한 주기 늦어질 수 있다).
  wall clock이 뒤로 가 cursor의 시각이 미래가 되면 시작 시각은 다시 잡고 경보 시각은 없는
  것으로 본다(`kortravelcommon.stall`).
  시계는 고정 4필드라 마지막 관측 시각이 없다. 실패 중에 sensor를 오래 멈췄다가 다시 켜면
  cursor의 옛 시작 시각 때문에 재기동 뒤 첫 실패(일시 오류여도)에 바로 경보한다. 성공 tick은
  시계를 지우므로 이후는 정상이다. 원치 않으면 재기동 전에 sensor cursor를 지운다.
  이 모드에서는 factory가 cursor를 소유하므로 콜백은 `context.update_cursor`를 쓰지 않는다.
  cursor·경보에는 원문이 없지만 `context.log`의 traceback에는 예외 message가 남는다
  (기존 tick 실패 기록과 같은 범위).
- 콜백이 멈추는 정체는 `budget_seconds`가 있어야 예외(`DeadlineExceeded`)로 기록된다. 예산이
  없으면 Dagster의 sensor 평가 timeout이 tick을 먼저 끊어 시계가 시작되지 않는다.
  `budget_seconds`와 `on_stall` 소요 시간의 합도 sensor 평가 상한 안에 두어야 한다. 넘으면
  경보는 나갔어도 `alerted_at`이 저장되지 않아 다음 tick에 다시 경보한다.
- 예산을 넘겨 끊긴 콜백 thread는 tick이 끝난 뒤에도 돌 수 있다. 그 thread에서
  `context.resources`·`context.log`를 `remaining()`이 0이 된 뒤에 쓰지 않는다.
"""

import json
import math
import threading
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from datetime import UTC, datetime
from time import monotonic
from time import time as wall_clock
from types import SimpleNamespace
from typing import Any

from dagster import (
    DagsterEventType,
    DagsterRunStatus,
    DefaultSensorStatus,
    RunRequest,
    RunsFilter,
    RunStatusChangeRecordsFilter,
    ScheduleDefinition,
    SensorResult,
    SkipReason,
    sensor,
)

from kortravelcommon.backoff import backoff_seconds
from kortravelcommon.deadline import call_with_deadline
from kortravelcommon.pg_errors import pg_error_info
from kortravelcommon.stall import StallClock, due_alert, mark_alerted, observe_failure

PROJECT_TAG = "kortravelcommon/project"
JOB_TAG = "kortravelcommon/job"
INFRA_RETRY_ATTEMPT_TAG = "kortravelcommon/infra_retry_attempt"
INFRA_RETRY_PARENT_TAG = "kortravelcommon/infra_retry_parent"
INFRA_RETRY_PENDING_TAG = "kortravelcommon/infra_retry_pending"
# 사유(JobFailureData) 없이 밖에서 실패 처리된 run의 판별 결과. 재시도 sensor가 남긴다.
FAILURE_CLASS_TAG = "kortravelcommon/failure_class"
# 실행 시작(RUN_START) 전에 dequeue·launch가 실패했다. step이 돌지 않았으므로 재시도한다.
FAILURE_CLASS_LAUNCH = "launch_failure"
# 시작한 뒤 worker가 사라져 run monitoring 등이 실패 처리했다. 취소·step 실패 기록은 없다.
FAILURE_CLASS_WORKER_LOST = "worker_lost"
# 취소(최대 실행시간 초과 포함) 뒤 실패 처리됐다. 같은 상한에 다시 걸리므로 보고만 한다.
FAILURE_CLASS_CANCELED = "canceled"
# step 실패 기록이 있다. provider·도메인 오류일 수 있으므로 보고만 한다.
FAILURE_CLASS_STEP_FAILURE = "step_failure"
# worker가 살아 있을 수 있다: 실패 기록 뒤에도 실행 event가 이어지거나, RUN_START 뒤에
# launch 경로 오류(launch RPC timeout 등)로 실패 처리됐다. 재시도하면 중복 실행이므로 보고만 한다.
FAILURE_CLASS_WORKER_ALIVE = "worker_alive"
_RETRYABLE_FAILURE_CLASSES = frozenset({FAILURE_CLASS_LAUNCH, FAILURE_CLASS_WORKER_LOST})
# 차단기가 결정적 오류로 세지 않는 분류.
_NOT_DETERMINISTIC_CLASSES = _RETRYABLE_FAILURE_CLASSES | {FAILURE_CLASS_WORKER_ALIVE}
# 실행 중인 worker가 남기는 event. 실패 기록 뒤에 보이면 worker가 살아 있다.
_WORKER_ACTIVITY_EVENTS = frozenset(
    {
        DagsterEventType.RUN_START,
        DagsterEventType.STEP_WORKER_STARTED,
        DagsterEventType.STEP_START,
        DagsterEventType.STEP_OUTPUT,
        DagsterEventType.STEP_SUCCESS,
        DagsterEventType.ASSET_MATERIALIZATION,
        DagsterEventType.RUN_SUCCESS,
    }
)
# 재시도 sensor가 보는 실패 창. 이보다 오래된 실패는 다음 정기 실행이 맡는다.
FAILURE_LOOKBACK_SECONDS = 3600
# 이보다 젊은 실패 event는 다음 tick에 읽는다. event 저장 뒤 run 상태 갱신·storage id
# commit 순서 역전·launch timeout 뒤 늦게 시작한 worker의 event를 기다린다.
FAILURE_SETTLE_SECONDS = 120
_FAILURE_SCAN_LIMIT = 100
_FAILURE_CURSOR_PREFIX = "failures:"
_STEP_CURSOR_PREFIX = "steps:"
_STALL_CURSOR_PREFIX = "stall:"


def _encode_failure_cursor(storage_id: int) -> str:
    return f"{_FAILURE_CURSOR_PREFIX}{storage_id}"


def _decode_failure_cursor(cursor: str | None) -> int | None:
    """판정을 마친 마지막 RUN_FAILURE event ID. 옛 형식(run_id·head)·손상은 None이다."""
    if not cursor or not cursor.startswith(_FAILURE_CURSOR_PREFIX):
        return None
    raw = cursor[len(_FAILURE_CURSOR_PREFIX) :]
    if not (raw.isascii() and raw.isdecimal() and len(raw) <= 18):
        return None
    return int(raw)


def classify_unreported_failure(
    instance: Any, run_id: str, failure_storage_id: int | None = None
) -> str:
    """사유 없이 실패 처리된 run을 event 이력의 구조로 분류한다(원문 message는 보지 않는다).

    Dagster는 dequeue·launch 실패, run worker 소실, 최대 실행시간 초과 종료를 모두
    `report_run_failed(run)`(JobFailureData 없음)로 기록한다. 취소·step 실패 기록이 있으면
    보고 대상, 없으면 RUN_START 유무로 launch 실패와 worker 소실을 가른다. RUN_START가
    있어도 실패 event(`failure_storage_id`) 뒤에 실행 event가 있거나, launch 경로 오류
    (오류가 담긴 ENGINE_EVENT)가 남아 있으면 worker가 살아 있을 수 있어 보고만 한다.
    launch 단계의 결정적 오류(정의 load 실패 등)도 `launch_failure`이며 재시도 상한만큼
    반복될 수 있다.
    """
    blocking = instance.get_records_for_run(
        run_id=run_id,
        of_type={DagsterEventType.RUN_CANCELING, DagsterEventType.STEP_FAILURE},
        limit=1,
        ascending=False,
    ).records
    if blocking:
        event = blocking[0].event_log_entry.dagster_event
        if event is not None and event.event_type == DagsterEventType.STEP_FAILURE:
            return FAILURE_CLASS_STEP_FAILURE
        return FAILURE_CLASS_CANCELED
    started = instance.get_records_for_run(
        run_id=run_id, of_type=DagsterEventType.RUN_START, limit=1
    ).records
    if not started:
        return FAILURE_CLASS_LAUNCH
    if failure_storage_id is not None:
        latest_activity = instance.get_records_for_run(
            run_id=run_id, of_type=set(_WORKER_ACTIVITY_EVENTS), limit=1, ascending=False
        ).records
        if latest_activity and latest_activity[0].storage_id > failure_storage_id:
            return FAILURE_CLASS_WORKER_ALIVE
    engine_events = instance.get_records_for_run(
        run_id=run_id, of_type=DagsterEventType.ENGINE_EVENT, limit=20, ascending=False
    ).records
    for record in engine_events:
        if failure_storage_id is not None and record.storage_id > failure_storage_id:
            continue
        event = record.event_log_entry.dagster_event
        # launch_run/submit_run 실패 경로는 실패 기록 바로 앞에 step 없는 오류 engine event를
        # 남긴다(launch RPC timeout 등 — worker가 살아 있을 수 있다). 실패 기록 직전의
        # engine event 하나만 본다. step의 compute log 오류 같은 더 앞선 기록은 보지 않는다.
        data = getattr(event, "event_specific_data", None)
        if getattr(data, "error", None) is not None and not getattr(event, "step_key", None):
            return FAILURE_CLASS_WORKER_ALIVE
        break
    return FAILURE_CLASS_WORKER_LOST


@dataclass(frozen=True)
class _StepCheckpoint:
    run_id: str
    cursor: str
    crashed_steps: int
    complete: bool = False
    failure_storage_id: int = 0
    step_storage_id: int = 0

    def encode(self) -> str:
        return _STEP_CURSOR_PREFIX + json.dumps(
            [
                self.run_id,
                self.cursor,
                self.crashed_steps,
                self.complete,
                self.failure_storage_id,
                self.step_storage_id,
            ],
            separators=(",", ":"),
        )


def _decode_step_checkpoint(cursor: str | None) -> _StepCheckpoint | None:
    if not cursor or not cursor.startswith(_STEP_CURSOR_PREFIX):
        return None
    value = json.loads(cursor[len(_STEP_CURSOR_PREFIX) :])
    if not (
        isinstance(value, list)
        and len(value) in (3, 5, 6)
        and isinstance(value[0], str)
        and value[0]
        and isinstance(value[1], str)
        and value[1]
        and type(value[2]) is int
        and value[2] > 0
    ):
        raise ValueError("step 복구 checkpoint가 유효하지 않습니다.")
    if len(value) >= 5 and not (type(value[3]) is bool and type(value[4]) is int and value[4] > 0):
        raise ValueError("step 복구 완료 phase가 유효하지 않습니다.")
    if len(value) == 6 and not (type(value[5]) is int and value[5] >= 0):
        raise ValueError("step 복구 증거 ID가 유효하지 않습니다.")
    if len(value) < 6:
        # 이전 형식은 마지막 STEP 증거를 갖지 않는다. terminal ID부터 다시 검증한다.
        return _StepCheckpoint(*value[:3])
    return _StepCheckpoint(*value)


ACTIVE_STATUSES = [
    DagsterRunStatus.QUEUED,
    DagsterRunStatus.STARTING,
    DagsterRunStatus.STARTED,
    DagsterRunStatus.CANCELING,
]


@dataclass(frozen=True)
class RecoveryPolicy:
    """재시도는 멱등성이 확인된 소비자만 명시적으로 허용한다."""

    max_runtime_seconds: int
    idempotent: bool = False
    infrastructure_retries: int = 0

    def __post_init__(self) -> None:
        if (
            type(self.max_runtime_seconds) is not int
            or type(self.infrastructure_retries) is not int
            or type(self.idempotent) is not bool
        ):
            raise ValueError("실행/재시도 상한은 정수, 멱등 선언은 boolean이어야 합니다.")
        if self.max_runtime_seconds <= 0 or self.infrastructure_retries < 0:
            raise ValueError("실행 상한은 양수, 재시도 상한은 0 이상이어야 합니다.")
        if self.infrastructure_retries and not self.idempotent:
            raise ValueError("멱등 작업만 자동 재시도를 허용합니다.")

    def tags(self, *, project: str, job_name: str) -> dict[str, str]:
        return {
            PROJECT_TAG: project,
            JOB_TAG: f"{project}/{job_name}",
            "dagster/max_runtime": str(self.max_runtime_seconds),
            "dagster/max_retries": str(self.infrastructure_retries),
            # provider 재시도와 중첩하지 않는다. 프로세스/launcher 장애만 재시도한다.
            "dagster/retry_on_asset_or_op_failure": "false",
        }


def has_active_run(instance: Any, *, job_name: str, project: str, location_name: str) -> bool:
    """현재 location의 과거 무태그 run도 포함하고 다른 앱의 동명 job은 제외한다."""
    cursor = None
    filters = RunsFilter(job_name=job_name, statuses=ACTIVE_STATUSES)
    while True:
        batch = instance.get_runs(filters=filters, limit=100, cursor=cursor)
        for run in batch:
            if _owned(run, project=project, location_name=location_name):
                return True
        if len(batch) < 100:
            return False
        cursor = batch[-1].run_id


def coalescing_schedule(
    *,
    project: str,
    location_name: str,
    job: Any,
    should_execute: Callable[[Any], bool] | None = None,
    queued_stale_after_seconds: float | None = None,
    **kwargs: Any,
):
    """진행/대기 중인 동일 job이 있으면 새 tick을 합친다. 수동 실행은 별도다.

    경쟁하는 수동 실행은 instance의 JOB_TAG별 limit=1로 막아야 한다.
    DB 장애는 예외로 전달하여 tick을 실패시킨다. 확인 실패를 빈 큐로 간주하지 않는다.

    `queued_stale_after_seconds`를 주면 그보다 오래 QUEUED인 run마다 warning을 남긴다.
    남은 실행이 그 오래된 QUEUED run 하나뿐이면 이번 tick을 허용한다(막힌 대기 run 하나가
    예약을 영원히 막지 않게 한다). 생략하면 기존과 같다. STARTED run의 상한은 job의
    `dagster/max_runtime`이 맡으므로 주기에 비례하게 잡는다(5분 job에 몇 시간은 과하다).
    """

    if queued_stale_after_seconds is not None:
        _require_positive(queued_stale_after_seconds, "queued_stale_after_seconds")

    def blocked(context) -> bool:
        if queued_stale_after_seconds is None:
            return has_active_run(
                context.instance, job_name=job.name, project=project, location_name=location_name
            )
        active = _active_run_records(
            context.instance, job_name=job.name, project=project, location_name=location_name
        )
        now = wall_clock()
        if any(_epoch(record.create_timestamp) > now + 60 for record in active):
            # 저장소 시각이 UTC가 아니면(서버 TimeZone) 나이가 음수가 되어 상한이 꺼진다.
            context.log.warning("run 생성 시각이 현재보다 미래입니다. 저장소 시간대를 확인합니다.")
        stale = [
            record
            for record in active
            if record.dagster_run.status == DagsterRunStatus.QUEUED
            and now - _epoch(record.create_timestamp) >= queued_stale_after_seconds
        ]
        for record in stale:
            context.log.warning(
                "QUEUED run이 %d초째 dequeue되지 않았습니다: %s %s",
                now - _epoch(record.create_timestamp),
                job.name,
                record.dagster_run.run_id,
            )
        if len(active) == 1 and stale:
            # 막힌 대기 run 하나 뒤에 한 번만 더 넣는다. 새 run도 막히면 다음 tick은 그 새
            # run(아직 젊다)이나 대기 run 둘을 보고 다시 합치므로 대기열이 계속 불지 않는다.
            context.log.warning(
                "오래 대기한 QUEUED run만 남아 이번 예약을 허용합니다: %s", job.name
            )
            return False
        return bool(active)

    def eligible(context):
        if blocked(context):
            context.log.info("동일 job 실행이 남아 있어 이번 예약을 합칩니다: %s", job.name)
            return False
        return should_execute(context) if should_execute is not None else True

    return ScheduleDefinition(job=job, should_execute=eligible, **kwargs)


def _require_positive(value: object, name: str) -> float:
    if (
        isinstance(value, bool)
        or not isinstance(value, (int, float))
        or not math.isfinite(value)
        or value <= 0
    ):
        raise ValueError(f"{name}는 유한한 양수여야 합니다.")
    return float(value)


def _epoch(value: Any) -> float:
    """RunRecord 시각(datetime·epoch)을 epoch 초로. 시간대 없는 datetime은 UTC로 본다."""
    if isinstance(value, datetime):
        if value.tzinfo is None:
            value = value.replace(tzinfo=UTC)
        return value.timestamp()
    return float(value)


def _owned(run: Any, *, project: str, location_name: str) -> bool:
    origin = run.remote_job_origin
    if origin is not None:
        return origin.repository_origin.code_location_origin.location_name == location_name
    return run.tags.get(PROJECT_TAG) == project


def _active_run_records(instance: Any, *, job_name: str, project: str, location_name: str):
    cursor = None
    owned = []
    filters = RunsFilter(job_name=job_name, statuses=ACTIVE_STATUSES)
    while True:
        batch = instance.get_run_records(filters=filters, limit=100, cursor=cursor)
        owned.extend(
            record
            for record in batch
            if _owned(record.dagster_run, project=project, location_name=location_name)
        )
        if len(batch) < 100:
            return owned
        cursor = batch[-1].dagster_run.run_id


# 차단기가 연 실패 run에 남기는 경보용 tag. 운영 경보는 이 tag로 run을 찾는다.
BREAKER_TAG = "kortravelcommon/breaker"
BREAKER_FINGERPRINT_TAG = "kortravelcommon/breaker_fingerprint"
BREAKER_STREAK_TAG = "kortravelcommon/breaker_streak"
_FINGERPRINT_CHARS = 200
_PARENT_ONLY_TAGS = frozenset(
    {FAILURE_CLASS_TAG, BREAKER_TAG, BREAKER_FINGERPRINT_TAG, BREAKER_STREAK_TAG}
)


@dataclass(frozen=True)
class FailureStreak:
    """가장 최근에 끝난 run부터 같은 실패 지문이 연속한 구간."""

    fingerprint: str
    count: int
    last_run_id: str
    last_failed_at: float
    # 가장 최근 실패보다 새 run이 아직 끝나지 않았다(시험 실행이 진행 중).
    in_flight: bool = False


# 사용자 예외를 cause로 감싸는 Dagster 오류. 지문에는 감싼 원 예외 형식을 쓴다.
_WRAPPER_ERRORS = frozenset(
    {
        "DagsterExecutionStepExecutionError",
        "RetryRequestedFromPolicy",
        "RetryRequested",
        "DagsterMaxRetriesExceededError",
    }
)
# 재시도로 고칠 수 있는 worker·launch 장애. 차단기는 이 실패를 세지도 끊지도 않는다.
_TRANSIENT_RUN_REASONS = frozenset(
    {"START_TIMEOUT", "UNEXPECTED_TERMINATION", "RUN_WORKER_RESTART"}
)


def _error_name(error: Any) -> str:
    for _ in range(8):
        if error is None:
            return ""
        if error.cls_name in _WRAPPER_ERRORS and error.cause is not None:
            error = error.cause
            continue
        break
    return error.cls_name or ""


def failure_fingerprint(instance: Any, run_id: str) -> str | None:
    """실패 사유·첫 실패 step·예외 형식으로 만든 지문. 원문 message는 넣지 않는다.

    worker·launch 장애(`START_TIMEOUT` 등, 사유 없는 `launch_failure`·`worker_lost`·
    `worker_alive`)는 결정적 오류가 아니므로 None을 돌려준다. 최대 실행시간 초과로
    취소된 실패는 센다.
    """
    run_failure = instance.get_records_for_run(
        run_id=run_id, of_type=DagsterEventType.RUN_FAILURE, limit=1, ascending=False
    ).records
    run_data = (
        run_failure[0].event_log_entry.dagster_event.event_specific_data if run_failure else None
    )
    reason = getattr(getattr(run_data, "failure_reason", None), "value", None)
    if reason in _TRANSIENT_RUN_REASONS:
        return None
    if run_data is None:
        failure_class = classify_unreported_failure(
            instance, run_id, run_failure[0].storage_id if run_failure else None
        )
        if failure_class in _NOT_DETERMINISTIC_CLASSES:
            return None
        if failure_class == FAILURE_CLASS_CANCELED:
            return "CANCELED||"
    reason = reason or "NONE"
    step_failure = instance.get_records_for_run(
        run_id=run_id, of_type=DagsterEventType.STEP_FAILURE, limit=1, ascending=True
    ).records
    if step_failure:
        event = step_failure[0].event_log_entry.dagster_event
        step_key = event.step_key or ""
        error = getattr(event.event_specific_data, "error", None)
    else:
        step_key = ""
        error = getattr(run_data, "error", None)
    return f"{reason}|{step_key}|{_error_name(error)}"[:_FINGERPRINT_CHARS]


def failure_streak(
    instance: Any,
    *,
    job_name: str,
    project: str,
    location_name: str,
    limit: int = 32,
    fingerprint: Callable[[Any, str], str | None] = failure_fingerprint,
) -> FailureStreak | None:
    """최근 run을 생성 역순으로 읽어 같은 지문의 연속 실패를 센다. 성공을 만나면 멈춘다.

    취소된 run, backfill run, 다른 project/location run, 지문이 None인 실패(worker·launch
    장애)는 건너뛴다(연속을 끊지도 세지도 않는다). 수동·재시도 run도 같은 job이면 센다.
    `count`는 최대 `limit`까지만 센다. 세어 볼 실패가 없거나 가장 최근 판정 run이 성공이면
    None이다. 읽는 run은 page 5개(최대 500건), 지문 계산은 `2×limit`건까지다.
    """
    if type(limit) is not int or not 1 <= limit <= 100:
        raise ValueError("limit는 1~100 정수여야 합니다.")
    filters = RunsFilter(
        job_name=job_name,
        statuses=[
            DagsterRunStatus.SUCCESS,
            DagsterRunStatus.FAILURE,
            DagsterRunStatus.CANCELED,
            *ACTIVE_STATUSES,
        ],
    )
    in_flight = False
    first = None
    count = 0
    computed = 0
    cursor = None
    done = False
    for _ in range(5):
        records = instance.get_run_records(filters=filters, limit=100, cursor=cursor)
        for record in records:
            run = record.dagster_run
            if (
                not _owned(run, project=project, location_name=location_name)
                or "dagster/backfill" in run.tags
            ):
                continue
            if run.status in ACTIVE_STATUSES:
                in_flight = in_flight or first is None
                continue
            if run.status == DagsterRunStatus.CANCELED:
                continue
            if run.status != DagsterRunStatus.FAILURE:
                done = True
                break
            # 이미 판정된 tag로 worker·launch 장애를 event 조회 없이 건너뛴다.
            if (
                run.tags.get("dagster/failure_reason") in _TRANSIENT_RUN_REASONS
                or run.tags.get(FAILURE_CLASS_TAG) in _NOT_DETERMINISTIC_CLASSES
            ):
                continue
            computed += 1
            if computed > 2 * limit:
                # 세지 않는 실패가 길게 이어지면 지문 계산을 멈춘다(tick 비용 상한).
                done = True
                break
            current = fingerprint(instance, run.run_id)
            if current is None:
                continue
            if first is None:
                first = (current, record)
            elif current != first[0]:
                done = True
                break
            count += 1
            if count >= limit:
                done = True
                break
        if done or len(records) < 100:
            break
        cursor = records[-1].dagster_run.run_id
    if first is None:
        return None
    current, record = first
    return FailureStreak(
        fingerprint=current,
        count=count,
        last_run_id=record.dagster_run.run_id,
        last_failed_at=(
            record.end_time if record.end_time is not None else _epoch(record.update_timestamp)
        ),
        in_flight=in_flight,
    )


def breaker_retry_at(
    streak: FailureStreak,
    *,
    threshold: int,
    base_cooldown_seconds: float,
    max_cooldown_seconds: float,
) -> float | None:
    """차단기가 열렸으면 다음 시험 실행을 허용할 epoch 초, 닫혀 있으면 None.

    threshold번째 연속 실패에서 열리고 대기는 base에서 시작해 시험이 실패할 때마다 두 배
    (max에서 멈춤)다. 소비자가 자체 저장소로 차단기를 구현할 때도 이 계산을 쓸 수 있다.
    """
    if streak.count < threshold:
        return None
    cooldown = backoff_seconds(
        streak.count - threshold + 1,
        base_seconds=base_cooldown_seconds,
        cap_seconds=max_cooldown_seconds,
        jitter=0,
    )
    return streak.last_failed_at + cooldown


def failure_breaker(
    *,
    project: str,
    location_name: str,
    job: Any,
    threshold: int = 3,
    base_cooldown_seconds: float = 900,
    max_cooldown_seconds: float = 6 * 3600,
    fingerprint: Callable[[Any, str], str | None] = failure_fingerprint,
    on_open: Callable[[Any, FailureStreak], None] | None = None,
) -> Callable[[Any], bool]:
    """같은 지문으로 threshold회 연속 실패하면 schedule tick을 건너뛰는 `should_execute`.

    재시도로 고칠 수 없는 결정적 오류가 매 주기 run을 만드는 것을 막는다. 상태는 따로
    저장하지 않고 매 tick run 이력에서 다시 계산한다(재기동·배포에 안전하다).

    - 열림: 마지막 실패 뒤 대기(`breaker_retry_at`) 동안 tick을 건너뛴다. 대기가 지나면
      시험 실행 한 번을 허용하고(반개방), 그 run이 끝날 때까지 다음 tick은 건너뛴다.
      시험이 같은 지문으로 실패하면 대기가 두 배가 되고, 성공하거나 지문이 바뀌면 닫힌다.
    - 경보: 열림을 처음 본 실패 run에 `BREAKER_TAG=open`, 지문, 연속 횟수 tag를 남기고
      warning 로그를 쓴다. `on_open(context, streak)`는 그 tag를 새로 쓰기 직전에 한 번
      부른다. 콜백이 실패하면 tag를 쓰지 않아 다음 tick에 다시 부른다(최소 1회 전달이며
      tag 쓰기가 실패하면 중복될 수 있다). 콜백은 짧게 끝나야 한다(schedule 평가 시간 안).
      연속 횟수 tag는 대기 계산에 필요한 창(threshold+대기 두 배 횟수)까지만 센다.
    - 지문 기본값은 실패 사유|첫 실패 step|예외 형식(RetryPolicy·step 오류 래퍼는 원 예외로
      푼다)이다. worker·launch 장애(`failure_fingerprint`가 None)는 세지도 끊지도 않는다.
      오류 코드로 가르려면 오류마다 예외 형식을 나누거나 `fingerprint(instance, run_id)`를
      준다(원문 message는 넣지 않는다). backfill run은 보지 않는다.
    - 운영: 원인을 고쳐 배포해도 남은 대기 동안은 열려 있다. 수동 실행 한 번이 성공하면 닫힌다.

    `coalescing_schedule(should_execute=...)` 또는 `ScheduleDefinition(should_execute=...)`에
    넣는다. 이력 조회가 실패하면 예외로 tick을 실패시킨다(확인 실패를 정상으로 보지 않는다).
    """
    if type(threshold) is not int or not 1 <= threshold <= 50:
        raise ValueError("threshold는 1~50 정수여야 합니다.")
    base = _require_positive(base_cooldown_seconds, "base_cooldown_seconds")
    cap = _require_positive(max_cooldown_seconds, "max_cooldown_seconds")
    if base > cap:
        raise ValueError("base_cooldown_seconds는 max_cooldown_seconds 이하여야 합니다.")
    # 대기가 max에 닿는 데 필요한 만큼만 이력을 읽는다.
    scan_limit = min(100, threshold + math.ceil(math.log2(cap / base)) + 1)

    def should_execute(context) -> bool:
        streak = failure_streak(
            context.instance,
            job_name=job.name,
            project=project,
            location_name=location_name,
            limit=scan_limit,
            fingerprint=fingerprint,
        )
        if streak is None:
            return True
        retry_at = breaker_retry_at(
            streak,
            threshold=threshold,
            base_cooldown_seconds=base,
            max_cooldown_seconds=cap,
        )
        if retry_at is None:
            return True
        _record_open(context, streak, on_open)
        if streak.in_flight:
            context.log.info("차단기 시험 실행이 아직 끝나지 않았습니다: %s", job.name)
            return False
        now = wall_clock()
        if now >= retry_at:
            context.log.warning(
                "차단기 반개방: 같은 실패 %d회 뒤 시험 실행 1회를 허용합니다: %s %s",
                streak.count,
                job.name,
                streak.fingerprint,
            )
            return True
        context.log.warning(
            "차단기 열림: 같은 실패 %d회, %d초 뒤 시험 실행: %s %s",
            streak.count,
            retry_at - now,
            job.name,
            streak.fingerprint,
        )
        return False

    return should_execute


def _record_open(context: Any, streak: FailureStreak, on_open) -> None:
    tags = {
        BREAKER_TAG: "open",
        BREAKER_FINGERPRINT_TAG: streak.fingerprint,
        BREAKER_STREAK_TAG: str(streak.count),
    }
    run = context.instance.get_run_by_id(streak.last_run_id)
    if run is None or all(run.tags.get(key) == value for key, value in tags.items()):
        return
    if on_open is not None:
        try:
            on_open(context, streak)
        except Exception:
            context.log.exception("차단기 경보 콜백이 실패하여 다음 tick에 다시 부릅니다.")
            return
    context.instance.add_run_tags(streak.last_run_id, tags)


def _failure_signature(exc: BaseException) -> str:
    info = pg_error_info(exc)
    name = type(exc).__name__
    return f"{name}:{info.sqlstate}" if info is not None else name


def _encode_stall(clock: StallClock | None) -> str:
    payload = None if clock is None else clock.to_dict()
    return _STALL_CURSOR_PREFIX + json.dumps(payload, separators=(",", ":"))


def _decode_stall(context: Any) -> StallClock | None:
    cursor = context.cursor
    if not cursor:
        return None
    try:
        if not cursor.startswith(_STALL_CURSOR_PREFIX):
            raise ValueError("정체 시계 cursor 접두가 아닙니다.")
        payload = json.loads(cursor[len(_STALL_CURSOR_PREFIX) :])
        return None if payload is None else StallClock.from_dict(payload)
    except Exception:
        # 거대 정수(OverflowError)·깊은 중첩(RecursionError)도 sensor를 멈추지 않게 한다.
        context.log.warning("정체 시계 cursor가 유효하지 않아 새로 시작합니다.")
        return None


def reconciliation_sensor(
    *,
    name: str,
    reconcile: Callable[..., int],
    required_resource_keys: set[str],
    budget_seconds: float | None = None,
    on_stall: Callable[[Any, StallClock], None] | None = None,
    stall_after_seconds: float = 900,
    realert_after_seconds: float = 3600,
):
    """새 작업 예약과 독립적으로 앱이 소유한 stale lease 회수 콜백을 실행한다.

    budget_seconds·on_stall의 의미는 모듈 docstring을 따른다. 둘 다 생략하면 기존과 같다.
    """
    if budget_seconds is not None and (
        isinstance(budget_seconds, bool)
        or not isinstance(budget_seconds, (int, float))
        or not math.isfinite(budget_seconds)
        or budget_seconds <= 0
    ):
        raise ValueError("budget_seconds는 유한한 양수여야 합니다.")
    # 설정 오류를 정의 시점에 드러낸다. 시계 key는 sensor 이름이다.
    due_alert(None, now=0, stall_after=stall_after_seconds, realert_after=realert_after_seconds)
    if on_stall is not None:
        StallClock(key=name, first_failed_at=0, last_failure="")
    slots = threading.BoundedSemaphore(1) if budget_seconds is not None else None

    def run_reconcile(context) -> int:
        if budget_seconds is None:
            return reconcile(context)
        deadline = monotonic() + budget_seconds

        def remaining() -> float:
            return max(0.0, deadline - monotonic())

        return call_with_deadline(
            lambda: reconcile(context, remaining), timeout_seconds=budget_seconds, slots=slots
        )

    @sensor(
        name=name,
        minimum_interval_seconds=60,
        required_resource_keys=required_resource_keys,
        default_status=DefaultSensorStatus.RUNNING,
    )
    def reconcile_tick(context):
        if on_stall is None:
            recovered = run_reconcile(context)
            context.log.info("중단된 실행 기록 회수: %s", recovered)
            return SkipReason(f"중단된 실행 기록 {recovered}건 회수")
        clock = _decode_stall(context)
        try:
            recovered = run_reconcile(context)
        except Exception as exc:
            signature = _failure_signature(exc)
            context.log.exception("회수 콜백 실패를 정체 시계에 기록합니다: %s", signature)
            now = wall_clock()
            clock = observe_failure(clock, key=name, failure=signature, now=now)
            if due_alert(
                clock,
                now=now,
                stall_after=stall_after_seconds,
                realert_after=realert_after_seconds,
            ):
                try:
                    on_stall(context, clock)
                except Exception:
                    context.log.exception("정체 경보 콜백이 실패하여 다음 tick에 재시도합니다.")
                else:
                    clock = mark_alerted(clock, now)
            return SensorResult(
                skip_reason=f"회수 실패 기록: {signature}", cursor=_encode_stall(clock)
            )
        if clock is not None:
            context.log.info("회수 콜백 성공으로 정체 시계를 지웁니다: %s", clock.last_failure)
        context.log.info("중단된 실행 기록 회수: %s", recovered)
        return SensorResult(
            skip_reason=f"중단된 실행 기록 {recovered}건 회수", cursor=_encode_stall(None)
        )

    return reconcile_tick


def infrastructure_retry_sensor(
    *,
    name: str,
    project: str,
    location_name: str,
    job: Any,
    policy: RecoveryPolicy,
    repository_name: str = "__repository__",
):
    """기존 단일 job의 엄격한 인프라 재시도 API를 보존한다."""
    return _infrastructure_retry_sensor(
        name=name,
        project=project,
        location_name=location_name,
        jobs={job.name: (job, policy)},
        repository_name=repository_name,
        single_job=True,
    )


def infrastructure_retry_sensor_for_jobs(
    *,
    name: str,
    project: str,
    location_name: str,
    jobs: Mapping[str, tuple[Any, RecoveryPolicy]],
    repository_name: str = "__repository__",
):
    """명시한 여러 멱등 job이 하나의 실패 page·cursor·시간 예산을 공유한다.

    각 값은 (JobDefinition, RecoveryPolicy)이며 key는 job.name과 같아야 한다.
    기존 단일 factory와 같은 실패 분류·부분 선택 제외·pending 인계를 사용한다.
    native retry가 켜지면 미완료 인계만 마무리하고 한 tick에 요청은 최대 하나다.
    물리 worker 정산·소비자 DB lease·native 설정 변경은 이 factory가 소유하지 않는다.
    """
    return _infrastructure_retry_sensor(
        name=name,
        project=project,
        location_name=location_name,
        jobs=jobs,
        repository_name=repository_name,
        single_job=False,
    )


def _infrastructure_retry_sensor(
    *, name, project, location_name, jobs, repository_name, single_job
):
    # 외부 mapping의 후속 변경이 이미 등록된 allowlist를 바꾸지 않게 고정한다.
    jobs = {job_name: (job, policy) for job_name, (job, policy) in jobs.items()}
    if not jobs:
        raise ValueError("재시도 대상 job을 명시해야 합니다.")
    for job_name, (job, policy) in jobs.items():
        if job_name != job.name:
            raise ValueError("재시도 mapping key는 job.name과 같아야 합니다.")
        if not policy.idempotent or not policy.infrastructure_retries:
            raise ValueError("인프라 재시도 sensor는 재시도가 허용된 멱등 job에만 적용합니다.")
        if job.partitions_def is not None:
            raise ValueError("partition job은 전용 재시도 정책이 필요합니다.")

    def retry_failed_run(context):
        instance = context.instance
        run = context.dagster_run
        selected = jobs.get(run.job_name)
        if selected is None:
            return SkipReason("명시한 재시도 job이 아닙니다.")
        job, policy = selected
        pending = run.tags.get(INFRA_RETRY_PENDING_TAG) == "true"
        if instance.run_retries_enabled and not pending:
            return SkipReason("native run retry에 위임합니다.")
        if run.job_name != job.name or run.status != DagsterRunStatus.FAILURE:
            return SkipReason("대상 job의 실패 이벤트가 아닙니다.")
        origin = run.remote_job_origin
        location = (
            origin.repository_origin.code_location_origin.location_name
            if origin is not None
            else run.tags.get("dagster/code_location")
        )
        if location != location_name or run.tags.get(PROJECT_TAG) != project:
            return SkipReason("다른 project/location의 실행은 재시도하지 않습니다.")
        if origin is not None and (
            origin.repository_origin.repository_name != repository_name
            or origin.job_name != job.name
        ):
            return SkipReason("다른 repository/job origin은 재시도하지 않습니다.")
        if (
            run.op_selection is not None
            or run.asset_selection is not None
            or run.asset_check_selection is not None
            or (
                run.resolved_op_selection is not None
                and run.resolved_op_selection != set(job.graph.node_names())
            )
        ):
            return SkipReason("부분 선택 실행은 전체 job으로 확대하지 않습니다.")
        checkpoint = context.step_checkpoint
        failure_data = context.failure_event.event_specific_data
        completed_step = (
            checkpoint is not None
            and checkpoint.complete
            and context.failure_event.event_type_value == DagsterEventType.STEP_FAILURE.value
            and getattr(getattr(failure_data, "error_source", None), "value", None)
            == "FRAMEWORK_ERROR"
            and getattr(getattr(failure_data, "error", None), "cls_name", None)
            == "ChildProcessCrashException"
            and getattr(failure_data, "user_failure_data", None) is None
        )
        reason = getattr(failure_data, "failure_reason", None)
        subprocess_failure = completed_step or (
            getattr(reason, "value", None) == "RUN_EXCEPTION"
            and getattr(getattr(failure_data, "error", None), "cls_name", None)
            == "DagsterSubprocessError"
        )
        unreported = (
            checkpoint is None
            and failure_data is None
            and context.failure_event.event_type_value == DagsterEventType.RUN_FAILURE.value
        )
        if unreported:
            failure_class = classify_unreported_failure(
                instance, run.run_id, context.failure_storage_id
            )
            if run.tags.get(FAILURE_CLASS_TAG) != failure_class:
                # 분류 tag는 보고용이다. 예산이 부족하면 tick을 실패시키지 않고 생략한다.
                if monotonic() - context.started < 8:
                    instance.add_run_tags(run.run_id, {FAILURE_CLASS_TAG: failure_class})
            log = getattr(context, "log", None)
            if log is not None:
                log.warning(
                    "사유 없이 실패 처리된 run을 분류했습니다: %s %s", run.run_id, failure_class
                )
            if failure_class not in _RETRYABLE_FAILURE_CLASSES:
                return SkipReason(f"사유 없는 실패({failure_class})는 보고만 합니다.")
        elif (
            getattr(reason, "value", None)
            not in {
                "UNEXPECTED_TERMINATION",
                "START_TIMEOUT",
                "RUN_WORKER_RESTART",
            }
            and not subprocess_failure
        ):
            return SkipReason("명시적인 worker 인프라 장애만 재시도합니다.")
        if run.step_keys_to_execute is not None:
            plan = (
                instance.get_execution_plan_snapshot(run.execution_plan_snapshot_id)
                if run.execution_plan_snapshot_id is not None
                else None
            )
            if plan is None or set(run.step_keys_to_execute) != {step.key for step in plan.steps}:
                return SkipReason("부분 실행 계획은 전체 job으로 확대하지 않습니다.")
        # 인프라 종료 전에 provider/step 실패가 있었으면 같은 호출을 반복하지 않는다.
        if checkpoint is not None and checkpoint.failure_storage_id != context.failure_storage_id:
            checkpoint = None
        step_cursor = checkpoint.cursor if checkpoint is not None else None
        crashed_steps = checkpoint.crashed_steps if checkpoint is not None else 0
        step_storage_id = checkpoint.step_storage_id if checkpoint is not None else 0
        while not (checkpoint is not None and checkpoint.complete):
            failures = instance.get_records_for_run(
                run_id=run.run_id,
                of_type=DagsterEventType.STEP_FAILURE,
                limit=100,
                cursor=step_cursor,
            )
            for record in failures.records:
                event = getattr(getattr(record, "event_log_entry", None), "dagster_event", None)
                data = getattr(event, "event_specific_data", None)
                if not (
                    subprocess_failure
                    and getattr(getattr(data, "error_source", None), "value", None)
                    == "FRAMEWORK_ERROR"
                    and getattr(getattr(data, "error", None), "cls_name", None)
                    == "ChildProcessCrashException"
                    and getattr(data, "user_failure_data", None) is None
                ):
                    return SkipReason("step/provider 실패는 자동 재시도하지 않습니다.")
                crashed_steps += 1
                step_storage_id = max(step_storage_id, getattr(record, "storage_id", 0))
            if not getattr(failures, "has_more", False):
                step_cursor = getattr(failures, "cursor", None) or step_cursor
                break
            next_cursor = getattr(failures, "cursor", None)
            if not next_cursor or next_cursor == step_cursor:
                raise RuntimeError("step 실패 이력 cursor가 전진하지 않습니다.")
            step_cursor = next_cursor
            if monotonic() - context.started >= 5:
                return _StepCheckpoint(
                    run.run_id,
                    step_cursor,
                    crashed_steps,
                    False,
                    context.failure_storage_id,
                    step_storage_id,
                )
        if subprocess_failure and not crashed_steps:
            return SkipReason("명시적인 자식 프로세스 종료 기록이 없습니다.")
        # 느린 STEP 이력을 모두 검증한 즉시 저장한다. 추가 metadata 조회가
        # deadline을 소진해 완료 지점을 잃는 일을 막는다. 다음 tick은 scope와 중복을 재검증한다.
        if subprocess_failure and step_cursor and monotonic() - context.started >= 8:
            return _StepCheckpoint(
                run.run_id,
                step_cursor,
                crashed_steps,
                True,
                context.failure_storage_id,
                step_storage_id,
            )
        attempts = [
            run.tags.get(INFRA_RETRY_ATTEMPT_TAG, "0"),
            run.tags.get("dagster/retry_number", "0"),
        ]
        if any(
            not value.isascii() or not value.isdecimal() or len(value) > 6 for value in attempts
        ):
            return SkipReason("재시도 횟수가 유효하지 않습니다.")
        next_attempt = sum(int(value) for value in attempts) + 1
        if next_attempt > policy.infrastructure_retries:
            return SkipReason("인프라 재시도 상한에 도달했습니다.")
        native_child_id = run.tags.get("dagster/auto_retry_run_id")
        if native_child_id:
            native_child = instance.get_run_by_id(native_child_id)
            if native_child is not None and native_child.parent_run_id == run.run_id:
                if pending:
                    instance.add_run_tags(run.run_id, {INFRA_RETRY_PENDING_TAG: "false"})
                return SkipReason("native 재시도 실행이 이미 발급되었습니다.")
        if any(
            instance.get_runs(
                filters=RunsFilter(
                    job_name=job.name,
                    tags={parent_tag: run.run_id},
                ),
                limit=1,
            )
            for parent_tag in ("dagster/parent_run_id", INFRA_RETRY_PARENT_TAG)
        ):
            if pending:
                instance.add_run_tags(run.run_id, {INFRA_RETRY_PENDING_TAG: "false"})
            return SkipReason("이미 발급된 재시도 실행이 있습니다.")
        if has_active_run(
            instance, job_name=job.name, project=project, location_name=location_name
        ):
            return SkipReason("같은 job의 실행이 남아 있어 재시도를 합칩니다.")
        # 전체 deadline이 끝난 worker는 metadata를 뒤늦게 변경하지 않는다.
        # 검증 완료 위치를 저장하고 다음 tick에서 예산·scope를 다시 확인한다.
        if monotonic() - context.started >= 8:
            final_cursor = step_cursor
            if subprocess_failure and final_cursor:
                return _StepCheckpoint(
                    run.run_id,
                    final_cursor,
                    crashed_steps,
                    True,
                    context.failure_storage_id,
                    step_storage_id,
                )
            raise TimeoutError("재시도 인계에 필요한 시간 예산이 부족합니다.")
        # 이전 run의 native 상태 태그는 전달하지 않는다. job 정의의 실행 설정만 다시 적용한다.
        # parent의 실패 판정(분류·차단기 경보) tag도 child에 넘기지 않는다.
        tags = {
            key: value
            for key, value in run.tags.items()
            if not key.startswith("dagster/") and key not in _PARENT_ONLY_TAGS
        }
        tags.update(job.tags)
        tags.update(policy.tags(project=project, job_name=job.name))
        tags.pop(INFRA_RETRY_PENDING_TAG, None)
        tags["dagster/max_retries"] = str(policy.infrastructure_retries - next_attempt)
        tags.update(
            {
                "dagster/code_location": location_name,
                INFRA_RETRY_ATTEMPT_TAG: str(next_attempt),
                INFRA_RETRY_PARENT_TAG: run.run_id,
            }
        )
        # child의 잔여 예산만 줄이면 native OFF→ON에서 원 parent가 다시 재시도된다.
        # native 억제와 미완료 인계를 같은 metadata 쓰기에 남긴다. 저장 응답 유실 또는
        # 요청 제출 실패 뒤 native를 켜도 이 sensor가 동일 run key의 인계를 마무리한다.
        instance.add_run_tags(
            run.run_id,
            {
                "dagster/max_retries": "0",
                "dagster/will_retry": "false",
                INFRA_RETRY_PENDING_TAG: "true",
            },
        )
        return RunRequest(
            job_name=None if single_job else job.name,
            run_key=f"{project}/infra/{run.run_id}/{next_attempt}",
            run_config=run.run_config,
            tags=tags,
        )

    def runs_by_id(instance, run_ids):
        filter_tags = {PROJECT_TAG: project}
        if instance.run_retries_enabled:
            filter_tags[INFRA_RETRY_PENDING_TAG] = "true"
        unique = list(dict.fromkeys(run_ids))
        if not unique:
            return {}
        runs = instance.get_runs(
            filters=RunsFilter(
                run_ids=unique,
                job_name=next(iter(jobs)) if single_job else None,
                statuses=[DagsterRunStatus.FAILURE],
                tags=filter_tags,
            ),
            limit=len(unique),
        )
        return {run.run_id: run for run in runs}

    def evaluate_checkpoint(context, started, checkpoint):
        """한 run의 step 이력 검증을 이어 한다. 끝나면 그 실패 event 다음부터 훑는다."""
        instance = context.instance
        resumed = runs_by_id(instance, [checkpoint.run_id]).get(checkpoint.run_id)
        # 옛 3필드 checkpoint의 실패 event ID는 0이다. 0부터 읽어도 창(timestamp) 안만 본다.
        # None을 돌려주면 Dagster가 옛 cursor를 그대로 두어 sensor가 멈춘다.
        after = _encode_failure_cursor(checkpoint.failure_storage_id)
        if resumed is None or resumed.job_name not in jobs:
            return SensorResult(cursor=after)
        records = instance.get_records_for_run(
            run_id=resumed.run_id,
            # 완료 checkpoint 뒤에 추가된 step 실패도 확인한다. terminal 이벤트 ID만
            # 같다고 step 이력이 불변이라고 가정하지 않는다.
            of_type=(
                {DagsterEventType.RUN_FAILURE, DagsterEventType.STEP_FAILURE}
                if checkpoint.complete
                else DagsterEventType.RUN_FAILURE
            ),
            limit=1,
            ascending=False,
        ).records
        if not records:
            return SensorResult(cursor=after)
        if checkpoint.complete and records[0].storage_id != max(
            checkpoint.failure_storage_id, checkpoint.step_storage_id
        ):
            # 새 실패 기록은 완료 증거를 무효화한다. 다음 tick에서 RUN_FAILURE를
            # 확인하고 cursor 이후 이력을 읽어 provider 거부와 복구 진행을 함께 지킨다.
            return SensorResult(
                cursor=_StepCheckpoint(
                    checkpoint.run_id,
                    checkpoint.cursor,
                    checkpoint.crashed_steps,
                    False,
                    checkpoint.failure_storage_id,
                    checkpoint.step_storage_id,
                ).encode()
            )
        result = retry_failed_run(
            SimpleNamespace(
                instance=instance,
                dagster_run=resumed,
                failure_event=records[0].event_log_entry.dagster_event,
                started=started,
                step_checkpoint=checkpoint,
                failure_storage_id=(
                    checkpoint.failure_storage_id if checkpoint.complete else records[0].storage_id
                ),
                log=context.log,
            )
        )
        if isinstance(result, _StepCheckpoint):
            return SensorResult(cursor=result.encode())
        if isinstance(result, RunRequest):
            return SensorResult(run_requests=[result], cursor=after)
        return SensorResult(cursor=after)

    def evaluate_failures(context):
        started = monotonic()
        instance = context.instance
        checkpoint = _decode_step_checkpoint(context.cursor)
        if checkpoint is not None:
            return evaluate_checkpoint(context, started, checkpoint)
        # 이미 판정한 실패 event 다음부터 오래된 순서로 읽는다. 옛 run_id/head cursor나
        # cursor가 없으면 최근 창 안의 실패부터 시작한다(창 밖의 오래된 실패는 재시도하지 않는다).
        after = _decode_failure_cursor(context.cursor)
        now = wall_clock()
        # 창보다 오래 밀린 실패(예: sensor를 오래 멈춘 뒤)는 건너뛴다. 늦은 재실행은 다음
        # 정기 실행과 겹칠 뿐이다.
        settled_before = now - FAILURE_SETTLE_SECONDS
        window_start = now - FAILURE_LOOKBACK_SECONDS
        events = instance.fetch_run_status_changes(
            RunStatusChangeRecordsFilter(
                DagsterEventType.RUN_FAILURE,
                after_storage_id=after,
                after_timestamp=window_start,
            ),
            limit=_FAILURE_SCAN_LIMIT,
            ascending=True,
        ).records
        if not events:
            # 창 안에 실패가 없다. 창보다 오래된 최신 event까지 전진해 창 밖 행을 매 tick
            # 다시 훑지 않는다.
            latest = instance.fetch_run_status_changes(
                RunStatusChangeRecordsFilter(
                    DagsterEventType.RUN_FAILURE, before_timestamp=window_start
                ),
                limit=1,
                ascending=False,
            ).records
            after = max(after or 0, latest[0].storage_id if latest else 0)
            return SensorResult(cursor=_encode_failure_cursor(after))
        # 공용 plane의 실패 event는 모든 project의 것이다. project·job run만 한 번에 고른다.
        owned = runs_by_id(instance, [event.run_id for event in events])
        # 같은 run의 실패 event가 batch에 여럿이면 마지막 것만 판정한다.
        latest = {event.run_id: event.storage_id for event in events}
        handled = after
        evaluated = False
        for event in events:
            # id 순서로 읽다가 아직 자리 잡지 않은(젊은) event를 만나면 멈춘다. 그 앞까지만
            # 전진하므로 id와 생성 시각 순서가 어긋난 event도 다음 tick에 다시 읽는다.
            if event.timestamp >= settled_before:
                break
            run = owned.get(event.run_id)
            dagster_event = event.event_log_entry.dagster_event
            if (
                run is None
                or run.job_name not in jobs
                or dagster_event is None
                or latest[event.run_id] != event.storage_id
            ):
                handled = event.storage_id
                continue
            # 판정한 event까지만 전진한다. 다음 tick은 그 뒤부터 이어 읽고 같은 run을 다시
            # 훑지 않는다. 첫 판정은 예산과 무관하게 하여 매 tick 반드시 전진한다.
            if evaluated and monotonic() - started >= 5:
                break
            evaluated = True
            result = retry_failed_run(
                SimpleNamespace(
                    instance=instance,
                    dagster_run=run,
                    failure_event=dagster_event,
                    started=started,
                    step_checkpoint=None,
                    failure_storage_id=event.storage_id,
                    log=context.log,
                )
            )
            if isinstance(result, _StepCheckpoint):
                return SensorResult(cursor=result.encode())
            handled = event.storage_id
            if isinstance(result, RunRequest):
                # 같은 job은 한 tick에 하나만 발급한다. 다음 tick에 active 여부를 재확인한다.
                return SensorResult(run_requests=[result], cursor=_encode_failure_cursor(handled))
        return SensorResult(cursor=_encode_failure_cursor(handled or 0))

    @sensor(
        name=name,
        **({"job": next(iter(jobs.values()))[0]} if single_job else {
            "jobs": [entry[0] for entry in jobs.values()]
        }),
        minimum_interval_seconds=60,
        default_status=DefaultSensorStatus.RUNNING,
    )
    def retry_tick(context):
        # run_failure_sensor는 callback 예외도 failure event cursor를 소비한다. 일반 sensor의
        # 결과 반환 경계를 사용하여 metadata 오류/timeout 시 동일 batch를 다시 확인한다.
        return call_with_deadline(lambda: evaluate_failures(context), timeout_seconds=10)

    return retry_tick
