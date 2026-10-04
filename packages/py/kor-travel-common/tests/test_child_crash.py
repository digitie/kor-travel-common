# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
import os
import subprocess
import sys
import time
from pathlib import Path
from types import SimpleNamespace

import pytest
from dagster import (
    DagsterEvent,
    DagsterEventType,
    DagsterInstance,
    RunRequest,
    SkipReason,
    build_sensor_context,
)
from dagster._core.events import JobFailureData, RunFailureReason, StepFailureData
from dagster._core.execution.plan.objects import ErrorSource
from dagster._utils.error import SerializableErrorInfo
from test_recovery import evaluate_retry, failure_context, retry_definition, sample

import kortravelcommon.dagster as factory


def record(cls="ChildProcessCrashException", source="FRAMEWORK_ERROR", user=None):
    return SimpleNamespace(
        event_log_entry=SimpleNamespace(
            dagster_event=SimpleNamespace(
                event_specific_data=SimpleNamespace(
                    error=SimpleNamespace(cls_name=cls),
                    error_source=SimpleNamespace(value=source),
                    user_failure_data=user,
                )
            )
        )
    )


@pytest.mark.parametrize(
    "case", ["crash", "provider", "user", "mixed-page", "no-evidence", "unknown"]
)
def test_only_proven_child_crash_is_retried(monkeypatch, case):
    with DagsterInstance.local_temp() as instance:
        context = failure_context(instance, RunFailureReason.RUN_EXCEPTION)
        event = DagsterEvent(
            event_type_value=DagsterEventType.RUN_FAILURE.value,
            job_name=sample.name,
            event_specific_data=JobFailureData(
                SerializableErrorInfo("worker exited", [], "DagsterSubprocessError"),
                failure_reason=RunFailureReason.RUN_EXCEPTION,
            ),
        )
        instance.report_dagster_event(event, context.dagster_run.run_id)
        original = instance.get_records_for_run
        pages = []

        def events(**kw):
            if kw["of_type"] != DagsterEventType.STEP_FAILURE:
                return original(**kw)
            assert kw["limit"] == 100
            pages.append(kw.get("cursor"))
            records = [record()]
            if case == "provider":
                records = [record("ValueError", "USER_CODE_ERROR")]
            if case == "user":
                records = [record(user=object())]
            if case == "unknown":
                records = [object()]
            if case == "no-evidence":
                records = []
            more = case == "mixed-page" and kw.get("cursor") is None
            if more:
                records = [record() for _ in range(100)]
            if case == "mixed-page" and not more:
                records = [record("ValueError", "USER_CODE_ERROR")]
            return SimpleNamespace(records=records, has_more=more, cursor="next")

        monkeypatch.setattr(instance, "get_records_for_run", events)
        outcome = evaluate_retry(retry_definition(), context)
        assert isinstance(outcome, RunRequest if case == "crash" else SkipReason)
        if case == "mixed-page":
            assert pages == [None, "next"]


def test_real_multiprocess_crash_produces_one_fallback_request():
    result = subprocess.run(
        [sys.executable, str(Path(__file__).with_name("crash_fixture.py"))],
        env={**os.environ, "PYTHONPATH": str(Path(__file__).parents[1] / "src")},
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "actual-child-crash: one bounded fallback request" in result.stdout


@pytest.mark.parametrize("failure_delay, active_delay", [(0, 0), (3.1, 0), (3.1, 2.1)])
def test_slow_finite_step_pages_resume_without_late_metadata_write(
    monkeypatch, failure_delay, active_delay
):
    with DagsterInstance.local_temp() as instance:
        context = failure_context(instance, RunFailureReason.RUN_EXCEPTION)
        instance.report_dagster_event(
            DagsterEvent(
                event_type_value=DagsterEventType.RUN_FAILURE.value,
                job_name=sample.name,
                event_specific_data=JobFailureData(
                    SerializableErrorInfo("worker exited", [], "DagsterSubprocessError"),
                    failure_reason=RunFailureReason.RUN_EXCEPTION,
                ),
            ),
            context.dagster_run.run_id,
        )
        original = instance.get_records_for_run
        pages = []
        writes = []
        original_add = instance.add_run_tags

        def events(**kw):
            if kw["of_type"] != DagsterEventType.STEP_FAILURE:
                time.sleep(failure_delay)
                return original(**kw)
            pages.append(kw.get("cursor"))
            time.sleep(5.1)
            more = kw.get("cursor") is None
            return SimpleNamespace(
                records=[record() for _ in range(100 if more else 1)],
                has_more=more,
                cursor="second" if more else "end",
            )

        def add_tags(run_id, tags):
            writes.append(tags)
            return original_add(run_id, tags)

        monkeypatch.setattr(instance, "get_records_for_run", events)
        monkeypatch.setattr(instance, "add_run_tags", add_tags)
        original_active = factory.has_active_run

        def slow_active(*args, **kwargs):
            time.sleep(active_delay)
            return original_active(*args, **kwargs)

        monkeypatch.setattr(factory, "has_active_run", slow_active)
        definition = retry_definition()
        first = definition.evaluate_tick(context.sensor_context)
        assert first.run_requests == [] and first.cursor.startswith("steps:")
        assert writes == []
        second = definition.evaluate_tick(
            build_sensor_context(instance=instance, cursor=first.cursor)
        )
        if failure_delay:
            assert second.run_requests == []
            assert writes == []
            second = definition.evaluate_tick(
                build_sensor_context(instance=instance, cursor=second.cursor)
            )
        assert len(second.run_requests) == 1
        assert second.run_requests[0].tags["dagster/max_retries"] == "0"
        assert pages == [None, "second"]
        assert len(writes) == 1


def test_completed_checkpoint_rejects_late_provider_step_without_new_run_failure(monkeypatch):
    with DagsterInstance.local_temp() as instance:
        context = failure_context(instance, RunFailureReason.RUN_EXCEPTION)
        run_id = context.dagster_run.run_id

        def step(provider=False):
            instance.report_dagster_event(
                DagsterEvent(
                    event_type_value=DagsterEventType.STEP_FAILURE.value,
                    job_name=sample.name,
                    step_key="noop",
                    event_specific_data=StepFailureData(
                        SerializableErrorInfo(
                            "error", [], "ValueError" if provider else "ChildProcessCrashException"
                        ),
                        None,
                        ErrorSource.USER_CODE_ERROR if provider else ErrorSource.FRAMEWORK_ERROR,
                    ),
                ),
                run_id,
            )

        step()
        instance.report_dagster_event(
            DagsterEvent(
                event_type_value=DagsterEventType.RUN_FAILURE.value,
                job_name=sample.name,
                event_specific_data=JobFailureData(
                    SerializableErrorInfo("worker", [], "DagsterSubprocessError"),
                    failure_reason=RunFailureReason.RUN_EXCEPTION,
                ),
            ),
            run_id,
        )
        definition = retry_definition()
        with monkeypatch.context() as clock:
            clock.setattr(factory, "monotonic", iter([0, 9]).__next__)
            first = definition.evaluate_tick(context.sensor_context)
        assert first.run_requests == []
        assert "true" in first.cursor
        step(provider=True)
        resumed = definition.evaluate_tick(
            build_sensor_context(instance=instance, cursor=first.cursor)
        )
        cold = definition.evaluate_tick(build_sensor_context(instance=instance))
        denied = definition.evaluate_tick(
            build_sensor_context(instance=instance, cursor=resumed.cursor)
        )
        assert resumed.run_requests == denied.run_requests == cold.run_requests == []
        assert "kortravelcommon/infra_retry_pending" not in instance.get_run_by_id(run_id).tags


@pytest.mark.parametrize("after_checkpoint", [False, True])
def test_late_valid_child_step_resumes_with_finite_slow_metadata(monkeypatch, after_checkpoint):
    with DagsterInstance.local_temp() as instance:
        context = failure_context(instance, RunFailureReason.RUN_EXCEPTION)
        run_id = context.dagster_run.run_id

        def crash():
            instance.report_dagster_event(
                DagsterEvent(
                    event_type_value=DagsterEventType.STEP_FAILURE.value,
                    job_name=sample.name,
                    step_key="noop",
                    event_specific_data=StepFailureData(
                        SerializableErrorInfo("worker", [], "ChildProcessCrashException"),
                        None,
                        ErrorSource.FRAMEWORK_ERROR,
                    ),
                ),
                run_id,
            )

        crash()
        instance.report_dagster_event(
            DagsterEvent(
                event_type_value=DagsterEventType.RUN_FAILURE.value,
                job_name=sample.name,
                event_specific_data=JobFailureData(
                    SerializableErrorInfo("worker", [], "DagsterSubprocessError"),
                    failure_reason=RunFailureReason.RUN_EXCEPTION,
                ),
            ),
            run_id,
        )
        if not after_checkpoint:
            crash()
        original = instance.get_records_for_run
        step_queries = []
        writes = []
        original_add = instance.add_run_tags

        def events(**kw):
            is_step = kw["of_type"] == DagsterEventType.STEP_FAILURE
            time.sleep(5.1 if is_step else 3.1)
            if is_step:
                step_queries.append(kw.get("cursor"))
            return original(**kw)

        def add_tags(run_id, tags):
            writes.append(tags)
            return original_add(run_id, tags)

        monkeypatch.setattr(instance, "get_records_for_run", events)
        monkeypatch.setattr(instance, "add_run_tags", add_tags)
        definition = retry_definition()
        cursor = None
        requests = []
        for tick in range(5):
            outcome = definition.evaluate_tick(
                build_sensor_context(instance=instance, cursor=cursor)
            )
            cursor = outcome.cursor
            if tick == 0:
                assert not outcome.run_requests and not writes and "true" in cursor
                if after_checkpoint:
                    crash()
            requests.extend(outcome.run_requests)
            if requests:
                break
        assert len(requests) == len(writes) == 1
        assert len(step_queries) == (2 if after_checkpoint else 1)
        assert requests[0].tags["dagster/max_retries"] == "0"
