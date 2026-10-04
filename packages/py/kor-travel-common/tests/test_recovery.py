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
    build_schedule_context,
    build_sensor_context,
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


def retry_definition(job_definition=sample):
    return infrastructure_retry_sensor(
        name="test_infra_retry",
        project="test",
        location_name="test",
        job=job_definition,
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
    instance.report_dagster_event(event, run.run_id)
    return SimpleNamespace(
        dagster_run=run,
        sensor_context=build_sensor_context(instance=instance),
    )


def evaluate_retry(definition, context):
    tick = definition.evaluate_tick(context.sensor_context)
    return tick.run_requests[0] if tick.run_requests else SkipReason(tick.skip_message or "생략")


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
        request = evaluate_retry(retry, context)
        assert isinstance(request, RunRequest)
        assert request.run_config == context.dagster_run.run_config
        assert request.tags[INFRA_RETRY_ATTEMPT_TAG] == "1"
        assert request.tags[INFRA_RETRY_PARENT_TAG] == context.dagster_run.run_id
        assert "dagster/schedule_name" not in request.tags
        assert request.tags["dagster/max_retries"] == "0"
        parent = instance.get_run_by_id(context.dagster_run.run_id)
        assert parent.tags["dagster/max_retries"] == "0"
        assert parent.tags["dagster/will_retry"] == "false"
        assert evaluate_retry(retry, context).run_key == request.run_key


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
        assert isinstance(
            evaluate_retry(retry_definition(), failure_context(instance, reason)), SkipReason
        )


@pytest.mark.parametrize(
    "tags",
    [
        {"dagster/code_location": "foreign"},
        {"kortravelcommon/project": "foreign"},
        {INFRA_RETRY_ATTEMPT_TAG: "invalid"},
        {INFRA_RETRY_ATTEMPT_TAG: "-1"},
        {INFRA_RETRY_ATTEMPT_TAG: "99999999999999"},
        {INFRA_RETRY_ATTEMPT_TAG: "١"},
        {INFRA_RETRY_ATTEMPT_TAG: "1"},
        {"dagster/retry_number": "1", "dagster/parent_run_id": "old", "dagster/root_run_id": "old"},
        {"dagster/retry_number": "invalid"},
    ],
)
def test_retry_scope_and_malformed_budget_fail_closed(tags):
    with DagsterInstance.local_temp() as instance:
        assert isinstance(
            evaluate_retry(retry_definition(), failure_context(instance, **tags)), SkipReason
        )


def test_native_retry_and_active_job_prevent_fallback_retry(monkeypatch):
    with DagsterInstance.local_temp() as instance:
        context = failure_context(instance)
        monkeypatch.setattr(DagsterInstance, "run_retries_enabled", property(lambda self: True))
        assert isinstance(evaluate_retry(retry_definition(), context), SkipReason)
        monkeypatch.setattr(DagsterInstance, "run_retries_enabled", property(lambda self: False))
        instance.create_run_for_job(sample, status=DagsterRunStatus.STARTED, tags=sample.tags)
        assert isinstance(evaluate_retry(retry_definition(), context), SkipReason)


def test_infra_failure_after_step_failure_is_not_retried(monkeypatch):
    with DagsterInstance.local_temp() as instance:
        context = failure_context(instance)
        original = instance.get_records_for_run
        monkeypatch.setattr(
            instance,
            "get_records_for_run",
            lambda **kw: (
                SimpleNamespace(records=[object()])
                if kw["of_type"] == DagsterEventType.STEP_FAILURE
                else original(**kw)
            ),
        )
        assert isinstance(evaluate_retry(retry_definition(), context), SkipReason)


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
        original = instance.get_runs
        monkeypatch.setattr(
            instance, "get_runs", lambda **kw: (_ for _ in ()).throw(ConnectionError("offline"))
        )
        with pytest.raises(Exception) as caught:
            retry_definition().evaluate_tick(context.sensor_context)
        assert isinstance(caught.value, ConnectionError)
        assert context.sensor_context.cursor is None
        monkeypatch.setattr(instance, "get_runs", original)
        assert isinstance(evaluate_retry(retry_definition(), context), RunRequest)


def test_retry_cursor_cycles_to_new_failures_after_the_last_page():
    with DagsterInstance.local_temp() as instance:
        retry = retry_definition()
        first = failure_context(instance)
        first_tick = retry.evaluate_tick(first.sensor_context)
        assert len(first_tick.run_requests) == 1
        end_tick = retry.evaluate_tick(
            build_sensor_context(instance=instance, cursor=first_tick.cursor)
        )
        assert end_tick.cursor == "head"
        second = failure_context(instance)
        new_tick = retry.evaluate_tick(
            build_sensor_context(instance=instance, cursor=end_tick.cursor)
        )
        assert new_tick.run_requests[0].tags[INFRA_RETRY_PARENT_TAG] == second.dagster_run.run_id


def test_partial_op_selection_is_not_expanded_to_the_entire_job():
    with DagsterInstance.local_temp() as instance:
        context = failure_context(instance)
        original_run = context.dagster_run
        selected = instance.create_run_for_job(
            sample,
            status=DagsterRunStatus.FAILURE,
            op_selection=["noop"],
            tags=original_run.tags,
        )
        records = instance.get_records_for_run(run_id=original_run.run_id).records
        instance.report_dagster_event(records[-1].event_log_entry.dagster_event, selected.run_id)
        # 첫 run은 삭제하여 부분 실행의 판정만 검증한다.
        instance.delete_run(original_run.run_id)
        assert isinstance(evaluate_retry(retry_definition(), context), SkipReason)


@pytest.mark.parametrize("foreign", ["repository", "job"])
def test_retry_origin_repository_and_job_are_both_scoped(monkeypatch, foreign):
    with DagsterInstance.local_temp() as instance:
        context = failure_context(instance)
        run = context.dagster_run
        origin = SimpleNamespace(
            job_name="other" if foreign == "job" else sample.name,
            repository_origin=SimpleNamespace(
                repository_name="other" if foreign == "repository" else "__repository__",
                code_location_origin=SimpleNamespace(location_name="test"),
            ),
        )
        scoped_run = SimpleNamespace(
            job_name=run.job_name,
            run_id=run.run_id,
            status=run.status,
            tags=run.tags,
            remote_job_origin=origin,
        )
        monkeypatch.setattr(instance, "get_runs", lambda **kw: [scoped_run])
        assert isinstance(evaluate_retry(retry_definition(), context), SkipReason)


def test_retry_metadata_deadline_does_not_consume_the_failure(monkeypatch):
    import kortravelcommon.dagster as dagster_module

    release = threading.Event()
    exited = threading.Event()
    bounded_call = dagster_module.call_with_deadline
    with DagsterInstance.local_temp() as instance:
        context = failure_context(instance)
        original = instance.get_runs

        def short_deadline(call, **kwargs):
            def invoke():
                try:
                    return call()
                finally:
                    exited.set()

            return bounded_call(invoke, timeout_seconds=0.01)

        monkeypatch.setattr(dagster_module, "call_with_deadline", short_deadline)
        monkeypatch.setattr(instance, "get_runs", lambda **kw: release.wait(5) and [])
        try:
            with pytest.raises(DeadlineExceeded):
                retry_definition().evaluate_tick(context.sensor_context)
            assert context.sensor_context.cursor is None
        finally:
            release.set()
            assert exited.wait(1)
        monkeypatch.setattr(instance, "get_runs", original)
        monkeypatch.setattr(dagster_module, "call_with_deadline", bounded_call)
        assert isinstance(evaluate_retry(retry_definition(), context), RunRequest)


def test_retry_does_not_copy_native_parent_bookkeeping_tags():
    previous_tags = {
        "dagster/auto_retry_run_id": "unrelated",
        "dagster/will_retry": "true",
        "dagster/is_resume_retry": "true",
        "dagster/is_asset_resume_retry": "true",
        "dagster/failure_reason": "UNEXPECTED_TERMINATION",
        "dagster/retry_strategy": "FROM_FAILURE",
    }
    with DagsterInstance.local_temp() as instance:
        context = failure_context(instance, **previous_tags, source="preserved")
        request = evaluate_retry(retry_definition(), context)
        assert isinstance(request, RunRequest)
        assert not (previous_tags.keys() & request.tags.keys())
        assert request.tags["source"] == "preserved"
        child = instance.create_run_for_job(sample, tags=request.tags)
        assert not child.is_resume_retry


@job
def two_steps():
    noop.alias("first")()
    noop.alias("second")()


@pytest.mark.parametrize(
    "selection",
    [
        {"resolved_op_selection": {"first"}},
        {"partial_plan": True},
    ],
)
def test_resolved_or_plan_subset_is_not_expanded(selection):
    from dagster._core.execution.api import create_execution_plan

    with DagsterInstance.local_temp() as instance:
        if selection.get("partial_plan"):
            selection = {
                "execution_plan": create_execution_plan(two_steps, step_keys_to_execute=["first"])
            }
        run = instance.create_run_for_job(
            two_steps,
            status=DagsterRunStatus.FAILURE,
            **selection,
            tags={
                **RecoveryPolicy(300, idempotent=True, infrastructure_retries=1).tags(
                    project="test", job_name=two_steps.name
                ),
                "dagster/code_location": "test",
            },
        )
        instance.report_dagster_event(
            DagsterEvent(
                event_type_value=DagsterEventType.RUN_FAILURE.value,
                job_name=two_steps.name,
                event_specific_data=JobFailureData(
                    None, failure_reason=RunFailureReason.UNEXPECTED_TERMINATION
                ),
            ),
            run.run_id,
        )
        assert (
            not retry_definition(two_steps)
            .evaluate_tick(build_sensor_context(instance=instance))
            .run_requests
        )


def test_slow_healthy_metadata_checkpoints_completed_rows_before_outer_deadline(monkeypatch):
    import kortravelcommon.dagster as dagster_module

    with DagsterInstance.local_temp() as instance:
        target = failure_context(instance)
        failure_context(instance, RunFailureReason.STEP_FAILURE)
        newest = failure_context(instance, RunFailureReason.STEP_FAILURE)
        clock = iter([0, 6])
        monkeypatch.setattr(dagster_module, "monotonic", lambda: next(clock))
        first = retry_definition().evaluate_tick(build_sensor_context(instance=instance))
        assert not first.run_requests
        assert first.cursor == newest.dagster_run.run_id
        monkeypatch.setattr(dagster_module, "monotonic", lambda: 0)
        resumed = retry_definition().evaluate_tick(
            build_sensor_context(instance=instance, cursor=first.cursor)
        )
        assert resumed.run_requests[0].tags[INFRA_RETRY_PARENT_TAG] == target.dagster_run.run_id


def test_completed_native_child_consumes_the_parent_retry_budget():
    with DagsterInstance.local_temp() as instance:
        context = failure_context(instance)
        parent = context.dagster_run
        child = instance.create_run_for_job(
            sample,
            status=DagsterRunStatus.SUCCESS,
            root_run_id=parent.run_id,
            parent_run_id=parent.run_id,
            tags={**parent.tags, "dagster/retry_number": "1"},
        )
        instance.add_run_tags(parent.run_id, {"dagster/auto_retry_run_id": child.run_id})
        assert isinstance(evaluate_retry(retry_definition(), context), SkipReason)


def test_completed_fallback_child_is_not_issued_again():
    with DagsterInstance.local_temp() as instance:
        context = failure_context(instance)
        request = evaluate_retry(retry_definition(), context)
        instance.create_run_for_job(sample, status=DagsterRunStatus.SUCCESS, tags=request.tags)
        assert isinstance(evaluate_retry(retry_definition(), context), SkipReason)
