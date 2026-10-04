# SPDX-License-Identifier: GPL-3.0-or-later
import os
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest
from dagster import DagsterEvent, DagsterEventType, DagsterInstance, RunRequest, SkipReason
from dagster._core.events import JobFailureData, RunFailureReason
from dagster._utils.error import SerializableErrorInfo
from test_recovery import evaluate_retry, failure_context, retry_definition, sample


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
