# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"""주소 갱신의 제한된 실행과 자동 재개를 소비자 Dagster에 연결한다."""

from collections.abc import Callable
from time import time

from dagster import (
    DagsterRunStatus,
    DefaultSensorStatus,
    Failure,
    Field,
    RunRequest,
    RunsFilter,
    SkipReason,
    job,
    op,
    sensor,
)

from .dagster import RecoveryPolicy


def address_refresh_definitions(
    *,
    project: str,
    location_name: str,
    run: Callable[[bool], dict],
    pending: Callable[[], bool],
):
    """같은 job만 예약한다. provider 호출·트랜잭션은 sensor에서 실행하지 않는다."""
    tags = {
        "dagster/code_location": location_name,
        **RecoveryPolicy(120, idempotent=True, infrastructure_retries=1).tags(
            project=project, job_name="address_refresh_job"
        ),
    }

    @op(name="refresh_addresses", config_schema={"force": Field(bool, default_value=False)})
    def refresh_addresses(context):
        result = run(context.op_config["force"])
        if context.op_config["force"] and result.get("status") == "busy":
            raise Failure("다른 주소 갱신 worker가 실행 중입니다. 완료 후 다시 실행하세요.")
        context.log.info("주소 갱신 결과: %s", result)
        return result

    @job(name="address_refresh_job", tags=tags)
    def address_refresh_job():
        refresh_addresses()

    @sensor(
        name=f"{project}_address_refresh",
        job=address_refresh_job,
        minimum_interval_seconds=600,
        default_status=DefaultSensorStatus.RUNNING,
    )
    def address_refresh_sensor(context):
        active = context.instance.get_runs(
            filters=RunsFilter(
                job_name=address_refresh_job.name,
                tags={"dagster/code_location": location_name},
                statuses=[
                    DagsterRunStatus.QUEUED,
                    DagsterRunStatus.NOT_STARTED,
                    DagsterRunStatus.STARTING,
                    DagsterRunStatus.STARTED,
                    DagsterRunStatus.CANCELING,
                ],
            ),
            limit=1,
        )
        if active:
            return SkipReason("주소 갱신이 이미 예약되었거나 실행 중입니다.")
        if not pending():
            return SkipReason("6개월 갱신·재시도·수동 재개 대상이 없습니다.")
        return RunRequest(
            run_key=f"address-refresh-{int(time() // 600)}",
            run_config={"ops": {"refresh_addresses": {"config": {"force": False}}}},
            tags=tags,
        )

    return address_refresh_job, address_refresh_sensor
