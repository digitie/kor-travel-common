# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"""외부 작업 없이 실제 Dagster 자식 프로세스 종료만 재현한다."""

import os

from dagster import (
    DagsterInstance,
    build_sensor_context,
    execute_job,
    job,
    multiprocess_executor,
    op,
    reconstructable,
)

from kortravelcommon.dagster import RecoveryPolicy, infrastructure_retry_sensor


@op
def crash_worker():
    os._exit(42)


@job(
    executor_def=multiprocess_executor.configured({"max_concurrent": 1}),
    tags={
        **RecoveryPolicy(300, idempotent=True, infrastructure_retries=1).tags(
            project="test", job_name="crash_job"
        ),
        "dagster/code_location": "test",
    },
)
def crash_job():
    crash_worker()


if __name__ == "__main__":
    with DagsterInstance.local_temp(overrides={"run_retries": {"enabled": False}}) as instance:
        with execute_job(reconstructable(crash_job), instance=instance) as result:
            assert not result.success
            definition = infrastructure_retry_sensor(
                name="crash_retry",
                project="test",
                location_name="test",
                job=crash_job,
                policy=RecoveryPolicy(300, idempotent=True, infrastructure_retries=1),
            )
            tick = definition.evaluate_tick(build_sensor_context(instance=instance))
            assert len(tick.run_requests) == 1
            assert tick.run_requests[0].tags["dagster/max_retries"] == "0"
            print("actual-child-crash: one bounded fallback request")
