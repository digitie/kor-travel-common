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
    ScheduleDefinition,
    SensorResult,
    SkipReason,
    sensor,
)

from kortravelcommon.deadline import call_with_deadline
from kortravelcommon.pg_errors import pg_error_info
from kortravelcommon.stall import StallClock, due_alert, mark_alerted, observe_failure

PROJECT_TAG = "kortravelcommon/project"
JOB_TAG = "kortravelcommon/job"
INFRA_RETRY_ATTEMPT_TAG = "kortravelcommon/infra_retry_attempt"
INFRA_RETRY_PARENT_TAG = "kortravelcommon/infra_retry_parent"
INFRA_RETRY_PENDING_TAG = "kortravelcommon/infra_retry_pending"
_RETRY_SCAN_HEAD = "head"
_STEP_CURSOR_PREFIX = "steps:"
_STALL_CURSOR_PREFIX = "stall:"


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
            origin = run.remote_job_origin
            if origin is not None:
                if origin.repository_origin.code_location_origin.location_name == location_name:
                    return True
            elif run.tags.get(PROJECT_TAG) == project:
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
    **kwargs: Any,
):
    """진행/대기 중인 동일 job이 있으면 새 tick을 합친다. 수동 실행은 별도다.

    경쟁하는 수동 실행은 instance의 JOB_TAG별 limit=1로 막아야 한다.
    DB 장애는 예외로 전달하여 tick을 실패시킨다. 확인 실패를 빈 큐로 간주하지 않는다.
    """

    def eligible(context):
        active = has_active_run(
            context.instance, job_name=job.name, project=project, location_name=location_name
        )
        if active:
            context.log.info("동일 job 실행이 남아 있어 이번 예약을 합칩니다: %s", job.name)
        return not active and (should_execute(context) if should_execute is not None else True)

    return ScheduleDefinition(job=job, should_execute=eligible, **kwargs)


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
        if (
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
        tags = {key: value for key, value in run.tags.items() if not key.startswith("dagster/")}
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

    def evaluate_failures(context):
        started = monotonic()
        instance = context.instance
        filter_tags = {PROJECT_TAG: project}
        if instance.run_retries_enabled:
            filter_tags[INFRA_RETRY_PENDING_TAG] = "true"
        checkpoint = _decode_step_checkpoint(context.cursor)
        cursor = None if context.cursor == _RETRY_SCAN_HEAD else context.cursor or None
        if checkpoint is not None:
            resumed = instance.get_run_by_id(checkpoint.run_id)
            runs = [resumed] if resumed is not None else []
        else:
            if cursor is not None and instance.get_run_by_id(cursor) is None:
                cursor = None
            runs = instance.get_runs(
                filters=RunsFilter(
                    job_name=next(iter(jobs)) if single_job else None,
                    statuses=[DagsterRunStatus.FAILURE],
                    tags=filter_tags,
                ),
                limit=100,
                cursor=cursor,
            )
        requests = []
        for index, run in enumerate(runs):
            # 느리지만 정상인 metadata에서도 완료한 행을 checkpoint한다. 전체 페이지가
            # 10초를 넘는다는 이유로 같은 100행을 영구 반복하지 않는다.
            if index and monotonic() - started >= 5:
                return SensorResult(cursor=runs[index - 1].run_id)
            if run.job_name not in jobs:
                continue
            records = instance.get_records_for_run(
                run_id=run.run_id,
                # 완료 checkpoint 뒤에 추가된 step 실패도 확인한다. terminal 이벤트 ID만
                # 같다고 step 이력이 불변이라고 가정하지 않는다.
                of_type=(
                    {DagsterEventType.RUN_FAILURE, DagsterEventType.STEP_FAILURE}
                    if checkpoint is not None and checkpoint.complete
                    else DagsterEventType.RUN_FAILURE
                ),
                limit=1,
                ascending=False,
            ).records
            if not records:
                continue
            if (
                checkpoint is not None
                and checkpoint.complete
                and records[0].storage_id
                != max(checkpoint.failure_storage_id, checkpoint.step_storage_id)
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
            event = records[0].event_log_entry.dagster_event
            result = retry_failed_run(
                SimpleNamespace(
                    instance=instance,
                    dagster_run=run,
                    failure_event=event,
                    started=started,
                    step_checkpoint=checkpoint,
                    failure_storage_id=(
                        checkpoint.failure_storage_id
                        if checkpoint is not None and checkpoint.complete
                        else records[0].storage_id
                    ),
                )
            )
            if isinstance(result, _StepCheckpoint):
                return SensorResult(cursor=result.encode())
            if isinstance(result, RunRequest):
                requests.append(result)
                # 같은 job은 한 tick에 하나만 발급한다. 다음 tick에 active 여부를 재확인한다.
                return SensorResult(run_requests=requests, cursor=run.run_id)
        # 유한한 batch를 모두 확인한 뒤에만 cursor를 전진한다. 끝에서는 새 실패부터 재확인한다.
        return SensorResult(
            cursor=runs[-1].run_id
            if runs and (checkpoint is not None or len(runs) == 100)
            else _RETRY_SCAN_HEAD
        )

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
