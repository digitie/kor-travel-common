# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"""앱 도메인/DB를 소유하지 않는 Dagster 예약·장애 복구 계약."""

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from dagster import (
    DagsterRunStatus,
    DefaultSensorStatus,
    RunsFilter,
    ScheduleDefinition,
    SkipReason,
    sensor,
)

PROJECT_TAG = "kortravelcommon/project"
JOB_TAG = "kortravelcommon/job"
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
