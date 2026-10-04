# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"""앱 도메인/DB를 소유하지 않는 Dagster 예약·장애 복구 계약."""

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from dagster import (
    DagsterEventType,
    DagsterRunStatus,
    DefaultSensorStatus,
    RunRequest,
    RunsFilter,
    ScheduleDefinition,
    SkipReason,
    run_failure_sensor,
    sensor,
)

from kortravelcommon.deadline import call_with_deadline

PROJECT_TAG = "kortravelcommon/project"
JOB_TAG = "kortravelcommon/job"
INFRA_RETRY_ATTEMPT_TAG = "kortravelcommon/infra_retry_attempt"
INFRA_RETRY_PARENT_TAG = "kortravelcommon/infra_retry_parent"
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
    *, name: str, project: str, location_name: str, job: Any, policy: RecoveryPolicy
):
    """native retry가 꺼진 instance에서 멱등 job의 worker 장애만 제한적으로 재예약한다.

    실행 종료 이벤트의 명시적 인프라 사유만 허용한다. step/provider 실패, timeout에
    의한 취소, 원인 불명은 제외한다. native retry가 켜지면 이 sensor는 위임한다.
    run key는 이벤트 재평가를 중복 제거하며, 동시 수동 실행은 JOB_TAG queue limit과
    소비자 DB lease가 별도로 보호해야 한다. partition job은 이 factory의 대상이 아니다.
    """
    if not policy.idempotent or not policy.infrastructure_retries:
        raise ValueError("인프라 재시도 sensor는 재시도가 허용된 멱등 job에만 적용합니다.")
    if job.partitions_def is not None:
        raise ValueError("partition job은 전용 재시도 정책이 필요합니다.")

    def retry_failed_run(context):
        instance = context.instance
        if instance.run_retries_enabled:
            return SkipReason("native run retry에 위임합니다.")
        run = context.dagster_run
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
        reason = getattr(context.failure_event.event_specific_data, "failure_reason", None)
        if getattr(reason, "value", None) not in {
            "UNEXPECTED_TERMINATION",
            "START_TIMEOUT",
            "RUN_WORKER_RESTART",
        }:
            return SkipReason("명시적인 worker 인프라 장애만 재시도합니다.")
        # 인프라 종료 전에 provider/step 실패가 있었으면 같은 호출을 반복하지 않는다.
        if instance.get_records_for_run(
            run_id=run.run_id, of_type=DagsterEventType.STEP_FAILURE, limit=1
        ).records:
            return SkipReason("step 실패가 기록되어 자동 재시도하지 않습니다.")
        attempt = run.tags.get(INFRA_RETRY_ATTEMPT_TAG, "0")
        if not attempt.isascii() or not attempt.isdecimal() or len(attempt) > 6:
            return SkipReason("재시도 횟수가 유효하지 않습니다.")
        next_attempt = int(attempt) + 1
        if next_attempt > policy.infrastructure_retries:
            return SkipReason("인프라 재시도 상한에 도달했습니다.")
        if has_active_run(
            instance, job_name=job.name, project=project, location_name=location_name
        ):
            return SkipReason("같은 job의 실행이 남아 있어 재시도를 합칩니다.")
        # sensor/예약 identity를 새 sensor가 소유한다. 과거 native retry lineage도 섞지 않는다.
        tags = {
            key: value
            for key, value in run.tags.items()
            if key
            not in {
                "dagster/sensor_name",
                "dagster/schedule_name",
                "dagster/run_key",
                "dagster/root_run_id",
                "dagster/parent_run_id",
                "dagster/retry_number",
            }
        }
        tags.update(policy.tags(project=project, job_name=job.name))
        tags.update(
            {
                "dagster/code_location": location_name,
                INFRA_RETRY_ATTEMPT_TAG: str(next_attempt),
                INFRA_RETRY_PARENT_TAG: run.run_id,
            }
        )
        return RunRequest(
            run_key=f"{project}/infra/{run.run_id}/{next_attempt}",
            run_config=run.run_config,
            tags=tags,
        )

    @run_failure_sensor(
        name=name,
        monitored_jobs=[job],
        request_job=job,
        minimum_interval_seconds=60,
        default_status=DefaultSensorStatus.RUNNING,
    )
    def retry_tick(context):
        return call_with_deadline(lambda: retry_failed_run(context), timeout_seconds=10)

    return retry_tick
