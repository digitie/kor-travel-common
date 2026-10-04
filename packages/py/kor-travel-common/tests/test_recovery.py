# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
import threading
from types import SimpleNamespace

import pytest
from dagster import (
    DagsterEvent,
    DagsterEventType,
    DagsterInstance,
    DagsterRunStatus,
    RunRequest,
    SkipReason,
    build_run_status_sensor_context,
    build_schedule_context,
    job,
    op,
)
from dagster._core.events import JobFailureData, RunFailureReason

from kortravelcommon.dagster import (
    INFRA_RETRY_ATTEMPT_TAG,
    INFRA_RETRY_PARENT_TAG,
    RecoveryPolicy,
    coalescing_schedule,
    infrastructure_retry_sensor,
)
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
    "kwargs",
    [{"max_runtime_seconds": value} for value in (float("nan"), float("inf"), 1.5, "300", True)]
    + [
        {"max_runtime_seconds": 300, "idempotent": "false", "infrastructure_retries": 1},
        {"max_runtime_seconds": 300, "idempotent": True, "infrastructure_retries": 1.5},
        {"max_runtime_seconds": 300, "infrastructure_retries": True},
    ],
)
def test_dynamic_policy_values_cannot_disable_safety(kwargs):
    with pytest.raises(ValueError):
        RecoveryPolicy(**kwargs)


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


def retry_definition():
    return infrastructure_retry_sensor(
        name="test_infra_retry",
        project="test",
        location_name="test",
        job=sample,
        policy=RecoveryPolicy(300, idempotent=True, infrastructure_retries=1),
    )


def failure_context(instance, reason=RunFailureReason.UNEXPECTED_TERMINATION, **tags):
    run = instance.create_run_for_job(
        sample,
        status=DagsterRunStatus.FAILURE,
        run_config={"ops": {"noop": {}}},
        tags={**sample.tags, "dagster/code_location": "test", **tags},
    )
    event = DagsterEvent(
        event_type_value=DagsterEventType.RUN_FAILURE.value,
        job_name=sample.name,
        event_specific_data=JobFailureData(None, failure_reason=reason),
    )
    return build_run_status_sensor_context(
        sensor_name="test_infra_retry",
        dagster_event=event,
        dagster_instance=instance,
        dagster_run=run,
    )


@pytest.mark.parametrize(
    "reason",
    [
        RunFailureReason.UNEXPECTED_TERMINATION,
        RunFailureReason.START_TIMEOUT,
        RunFailureReason.RUN_WORKER_RESTART,
    ],
)
def test_infra_retry_preserves_config_and_deduplicates_event_with_one_attempt(reason):
    with DagsterInstance.local_temp() as instance:
        context = failure_context(instance, reason, **{"dagster/schedule_name": "old"})
        retry = retry_definition()
        request = retry(context)
        assert isinstance(request, RunRequest)
        assert request.run_config == context.dagster_run.run_config
        assert request.tags[INFRA_RETRY_ATTEMPT_TAG] == "1"
        assert request.tags[INFRA_RETRY_PARENT_TAG] == context.dagster_run.run_id
        assert "dagster/schedule_name" not in request.tags
        assert retry(context).run_key == request.run_key
        assert isinstance(retry(failure_context(instance, **request.tags)), SkipReason)


@pytest.mark.parametrize(
    "reason",
    [
        RunFailureReason.STEP_FAILURE,
        RunFailureReason.RUN_EXCEPTION,
        RunFailureReason.JOB_INITIALIZATION_FAILURE,
        RunFailureReason.UNKNOWN,
        None,
    ],
)
def test_provider_or_unknown_failure_is_not_retried(reason):
    with DagsterInstance.local_temp() as instance:
        assert isinstance(retry_definition()(failure_context(instance, reason)), SkipReason)


@pytest.mark.parametrize(
    "tags",
    [
        {"dagster/code_location": "foreign"},
        {"kortravelcommon/project": "foreign"},
        {INFRA_RETRY_ATTEMPT_TAG: "invalid"},
        {INFRA_RETRY_ATTEMPT_TAG: "-1"},
        {INFRA_RETRY_ATTEMPT_TAG: "99999999999999"},
        {INFRA_RETRY_ATTEMPT_TAG: "١"},
    ],
)
def test_retry_scope_and_malformed_budget_fail_closed(tags):
    with DagsterInstance.local_temp() as instance:
        assert isinstance(retry_definition()(failure_context(instance, **tags)), SkipReason)


def test_native_retry_and_active_job_prevent_fallback_retry(monkeypatch):
    with DagsterInstance.local_temp() as instance:
        context = failure_context(instance)
        monkeypatch.setattr(DagsterInstance, "run_retries_enabled", property(lambda self: True))
        assert isinstance(retry_definition()(context), SkipReason)
        monkeypatch.setattr(DagsterInstance, "run_retries_enabled", property(lambda self: False))
        instance.create_run_for_job(sample, status=DagsterRunStatus.STARTED, tags=sample.tags)
        assert isinstance(retry_definition()(context), SkipReason)


def test_infra_failure_after_step_failure_is_not_retried(monkeypatch):
    with DagsterInstance.local_temp() as instance:
        context = failure_context(instance)
        monkeypatch.setattr(
            instance, "get_records_for_run", lambda **kw: SimpleNamespace(records=[object()])
        )
        assert isinstance(retry_definition()(context), SkipReason)


def test_retry_requires_explicit_idempotent_policy():
    with pytest.raises(ValueError, match="멱등"):
        infrastructure_retry_sensor(
            name="unsafe",
            project="test",
            location_name="test",
            job=sample,
            policy=RecoveryPolicy(300),
        )


def test_timed_out_calls_keep_bounded_capacity_until_they_finish(monkeypatch):
    import kortravelcommon.deadline as deadline_module

    release = threading.Event()
    exited = threading.Event()
    monkeypatch.setattr(deadline_module, "_CALL_SLOTS", threading.BoundedSemaphore(1))

    def blocked():
        try:
            release.wait(5)
        finally:
            exited.set()

    try:
        with pytest.raises(DeadlineExceeded):
            call_with_deadline(blocked, timeout_seconds=0.01)
        with pytest.raises(DeadlineExceeded, match="상한"):
            call_with_deadline(
                lambda: pytest.fail("용량 부족이면 호출하지 않는다"), timeout_seconds=1
            )
    finally:
        release.set()
        assert exited.wait(1)


def test_retry_storage_failure_is_not_interpreted_as_an_empty_queue(monkeypatch):
    with DagsterInstance.local_temp() as instance:
        context = failure_context(instance)
        monkeypatch.setattr(
            instance, "get_runs", lambda **kw: (_ for _ in ()).throw(ConnectionError("offline"))
        )
        with pytest.raises(ConnectionError):
            retry_definition()(context)
