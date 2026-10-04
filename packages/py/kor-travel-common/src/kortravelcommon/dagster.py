# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"""앱 도메인/DB를 소유하지 않는 Dagster 예약·장애 복구 계약."""

from collections.abc import Callable
from dataclasses import dataclass
from time import monotonic
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

PROJECT_TAG = "kortravelcommon/project"
JOB_TAG = "kortravelcommon/job"
INFRA_RETRY_ATTEMPT_TAG = "kortravelcommon/infra_retry_attempt"
INFRA_RETRY_PARENT_TAG = "kortravelcommon/infra_retry_parent"
INFRA_RETRY_PENDING_TAG = "kortravelcommon/infra_retry_pending"
_RETRY_SCAN_HEAD = "head"
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


def reconciliation_sensor(
    *, name: str, reconcile: Callable[[Any], int], required_resource_keys: set[str]
):
    """새 작업 예약과 독립적으로 앱이 소유한 stale lease 회수 콜백을 실행한다."""

    @sensor(
        name=name,
        minimum_interval_seconds=60,
        required_resource_keys=required_resource_keys,
        default_status=DefaultSensorStatus.RUNNING,
    )
    def reconcile_tick(context):
        recovered = reconcile(context)
        context.log.info("중단된 실행 기록 회수: %s", recovered)
        return SkipReason(f"중단된 실행 기록 {recovered}건 회수")

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
    """native retry가 꺼진 instance에서 멱등 job의 worker 장애만 제한적으로 재예약한다.

    실행 종료 이벤트의 명시적 인프라 사유만 허용한다. step/provider 실패, timeout에
    의한 취소, 원인 불명은 제외한다. native retry가 켜지면 미완료 인계만 마무리한다.
    run key는 이벤트 재평가를 중복 제거하며, 동시 수동 실행은 JOB_TAG queue limit과
    소비자 DB lease가 별도로 보호해야 한다. partition job은 이 factory의 대상이 아니다.
    """
    if not policy.idempotent or not policy.infrastructure_retries:
        raise ValueError("인프라 재시도 sensor는 재시도가 허용된 멱등 job에만 적용합니다.")
    if job.partitions_def is not None:
        raise ValueError("partition job은 전용 재시도 정책이 필요합니다.")

    def retry_failed_run(context):
        instance = context.instance
        run = context.dagster_run
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
        reason = getattr(context.failure_event.event_specific_data, "failure_reason", None)
        if getattr(reason, "value", None) not in {
            "UNEXPECTED_TERMINATION",
            "START_TIMEOUT",
            "RUN_WORKER_RESTART",
        }:
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
        if instance.get_records_for_run(
            run_id=run.run_id, of_type=DagsterEventType.STEP_FAILURE, limit=1
        ).records:
            return SkipReason("step 실패가 기록되어 자동 재시도하지 않습니다.")
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
        cursor = None if context.cursor == _RETRY_SCAN_HEAD else context.cursor or None
        if cursor is not None and instance.get_run_by_id(cursor) is None:
            cursor = None
        runs = instance.get_runs(
            filters=RunsFilter(
                job_name=job.name, statuses=[DagsterRunStatus.FAILURE], tags=filter_tags
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
            records = instance.get_records_for_run(
                run_id=run.run_id,
                of_type=DagsterEventType.RUN_FAILURE,
                limit=1,
                ascending=False,
            ).records
            if not records:
                continue
            event = records[0].event_log_entry.dagster_event
            result = retry_failed_run(
                SimpleNamespace(
                    instance=instance,
                    dagster_run=run,
                    failure_event=event,
                )
            )
            if isinstance(result, RunRequest):
                requests.append(result)
                # 같은 job은 한 tick에 하나만 발급한다. 다음 tick에 active 여부를 재확인한다.
                return SensorResult(run_requests=requests, cursor=run.run_id)
        # 유한한 batch를 모두 확인한 뒤에만 cursor를 전진한다. 끝에서는 새 실패부터 재확인한다.
        return SensorResult(cursor=runs[-1].run_id if len(runs) == 100 else _RETRY_SCAN_HEAD)

    @sensor(
        name=name,
        job=job,
        minimum_interval_seconds=60,
        default_status=DefaultSensorStatus.RUNNING,
    )
    def retry_tick(context):
        # run_failure_sensor는 callback 예외도 failure event cursor를 소비한다. 일반 sensor의
        # 결과 반환 경계를 사용하여 metadata 오류/timeout 시 동일 batch를 다시 확인한다.
        return call_with_deadline(lambda: evaluate_failures(context), timeout_seconds=10)

    return retry_tick
