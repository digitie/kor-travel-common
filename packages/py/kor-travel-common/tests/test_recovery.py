# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
import threading
from types import SimpleNamespace

import pytest
from dagster import DagsterInstance, DagsterRunStatus, build_schedule_context, job, op

from kortravelcommon.dagster import RecoveryPolicy, coalescing_schedule
from kortravelcommon.deadline import DeadlineExceeded, call_with_deadline


@op
def noop():
    pass


@job(
    tags=RecoveryPolicy(300, idempotent=True, infrastructure_retries=1).tags(
        project="test", job_name="sample"
    )
)
def sample():
    noop()


def test_deadline_returns_and_preserves_exception():
    release = threading.Event()
    try:
        with pytest.raises(DeadlineExceeded):
            call_with_deadline(lambda: release.wait(5), timeout_seconds=0.01)
    finally:
        release.set()
    error = ValueError("contract")

    def fail():
        raise error

    with pytest.raises(ValueError) as caught:
        call_with_deadline(fail, timeout_seconds=1)
    assert caught.value is error
    assert call_with_deadline(lambda: 42, timeout_seconds=1) == 42


@pytest.mark.parametrize("value", [0, -1, float("nan"), float("inf")])
def test_invalid_deadline(value):
    with pytest.raises(ValueError):
        call_with_deadline(lambda: None, timeout_seconds=value)


def test_non_idempotent_jobs_never_inherit_retries():
    assert RecoveryPolicy(300).tags(project="pinvi", job_name="email")["dagster/max_retries"] == "0"
    with pytest.raises(ValueError):
        RecoveryPolicy(300, infrastructure_retries=1)


@pytest.mark.parametrize(
    "status", [DagsterRunStatus.STARTING, DagsterRunStatus.STARTED, DagsterRunStatus.CANCELING]
)
def test_schedule_coalesces_and_recovers_after_terminal_status(status):
    schedule = coalescing_schedule(
        project="test", location_name="test", job=sample, cron_schedule="* * * * *"
    )
    with DagsterInstance.local_temp() as instance:
        run = instance.create_run_for_job(sample, status=status, tags=sample.tags)
        context = build_schedule_context(instance=instance)
        assert schedule.evaluate_tick(context).skip_message
        instance.report_run_failed(run)
        assert len(schedule.evaluate_tick(context).run_requests) == 1


def test_foreign_location_does_not_block_and_legacy_run_does():
    from kortravelcommon.dagster import has_active_run

    def run(location):
        return SimpleNamespace(
            tags={},
            remote_job_origin=SimpleNamespace(
                repository_origin=SimpleNamespace(
                    code_location_origin=SimpleNamespace(location_name=location)
                )
            ),
        )

    instance = SimpleNamespace(get_runs=lambda **kw: [run("other")])
    assert not has_active_run(instance, job_name="sample", project="test", location_name="test")
    instance.get_runs = lambda **kw: [run("test")]
    assert has_active_run(instance, job_name="sample", project="test", location_name="test")


def test_storage_failure_does_not_allow_a_duplicate():
    schedule = coalescing_schedule(
        project="test", location_name="test", job=sample, cron_schedule="* * * * *"
    )
    with DagsterInstance.local_temp() as instance:
        context = build_schedule_context(instance=instance)
        with pytest.MonkeyPatch.context() as patch:
            patch.setattr(
                context.instance,
                "get_runs",
                lambda **kw: (_ for _ in ()).throw(ConnectionError("storage unavailable")),
            )
            with pytest.raises(Exception) as caught:
                schedule.evaluate_tick(context)
            assert isinstance(caught.value.__cause__, ConnectionError)


def test_unsubmitted_run_does_not_permanently_stop_scheduling():
    schedule = coalescing_schedule(
        project="test", location_name="test", job=sample, cron_schedule="* * * * *"
    )
    with DagsterInstance.local_temp() as instance:
        instance.create_run_for_job(sample, status=DagsterRunStatus.NOT_STARTED, tags=sample.tags)
        assert schedule.evaluate_tick(build_schedule_context(instance=instance)).run_requests


def test_consumer_predicate_is_preserved():
    schedule = coalescing_schedule(
        project="test",
        location_name="test",
        job=sample,
        cron_schedule="* * * * *",
        should_execute=lambda context: False,
    )
    with DagsterInstance.local_temp() as instance:
        assert schedule.evaluate_tick(build_schedule_context(instance=instance)).skip_message
