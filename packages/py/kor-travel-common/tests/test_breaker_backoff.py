# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"""연속 실패 차단기, 오래된 QUEUED 합침 상한, jitter backoff."""

import random
from datetime import UTC, datetime, timedelta
from types import SimpleNamespace

import pytest
from dagster import (
    DagsterInstance,
    DagsterRunStatus,
    RetryPolicy,
    build_schedule_context,
    job,
    op,
)

import kortravelcommon.dagster as recovery
from kortravelcommon.backoff import backoff_seconds, retry_after_seconds
from kortravelcommon.dagster import (
    BREAKER_FINGERPRINT_TAG,
    BREAKER_STREAK_TAG,
    BREAKER_TAG,
    PROJECT_TAG,
    FailureStreak,
    RecoveryPolicy,
    breaker_retry_at,
    coalescing_schedule,
    failure_breaker,
    failure_fingerprint,
    failure_streak,
)


class AlertPageDuplicate(RuntimeError):
    pass


class AlertPageMetadata(RuntimeError):
    pass


@op(config_schema={"mode": str})
def collect(context):
    mode = context.op_config["mode"]
    if mode == "duplicate":
        raise AlertPageDuplicate("event 중복")
    if mode == "metadata":
        raise AlertPageMetadata("metadata 누락")


@job(tags=RecoveryPolicy(300).tags(project="test", job_name="alerts"))
def alerts():
    collect()


def execute(instance, mode):
    return alerts.execute_in_process(
        instance=instance,
        run_config={"ops": {"collect": {"config": {"mode": mode}}}},
        raise_on_error=False,
    ).run_id


def create(instance, status):
    return instance.create_run_for_job(
        alerts,
        status=status,
        tags=alerts.tags,
        run_config={"ops": {"collect": {"config": {"mode": "ok"}}}},
    )


def breaker(**kwargs):
    return failure_breaker(project="test", location_name="test", job=alerts, **kwargs)


def allowed(predicate, instance):
    return predicate(build_schedule_context(instance=instance))


def streak(instance):
    return failure_streak(instance, job_name="alerts", project="test", location_name="test")


def test_breaker_opens_after_threshold_same_failures_and_tags_the_last_run():
    calls = []
    predicate = breaker(on_open=lambda context, value: calls.append(value))
    with DagsterInstance.local_temp() as instance:
        execute(instance, "duplicate")
        execute(instance, "duplicate")
        assert allowed(predicate, instance)
        last = execute(instance, "duplicate")
        assert not allowed(predicate, instance)
        assert not allowed(predicate, instance)
        tags = instance.get_run_by_id(last).tags
        assert tags[BREAKER_TAG] == "open"
        assert tags[BREAKER_STREAK_TAG] == "3"
        assert tags[BREAKER_FINGERPRINT_TAG] == "STEP_FAILURE|collect|AlertPageDuplicate"
        # 경보 콜백은 새 실패마다 한 번만 부른다.
        assert [value.count for value in calls] == [3]


def test_breaker_half_opens_after_cooldown_and_waits_for_the_probe(monkeypatch):
    predicate = breaker(base_cooldown_seconds=60, max_cooldown_seconds=600)
    with DagsterInstance.local_temp() as instance:
        for _ in range(3):
            execute(instance, "duplicate")
        current = streak(instance)
        retry_at = breaker_retry_at(
            current, threshold=3, base_cooldown_seconds=60, max_cooldown_seconds=600
        )
        assert retry_at == pytest.approx(current.last_failed_at + 60)
        monkeypatch.setattr(recovery, "wall_clock", lambda: retry_at + 1)
        assert allowed(predicate, instance)
        probe = create(instance, DagsterRunStatus.STARTED)
        assert not allowed(predicate, instance)
        instance.report_run_failed(probe)
        # 시험 실행의 실패는 사유가 달라(지문 변경) 연속이 끊긴다.
        assert allowed(predicate, instance)


def test_failed_probe_doubles_the_cooldown_up_to_the_cap():
    def at(count):
        value = FailureStreak("x", count, "run", 1000.0)
        return breaker_retry_at(
            value, threshold=3, base_cooldown_seconds=60, max_cooldown_seconds=300
        )

    assert at(2) is None
    assert [at(count) - 1000.0 for count in (3, 4, 5, 6, 9)] == [60, 120, 240, 300, 300]


def test_success_or_a_different_failure_closes_the_breaker():
    predicate = breaker()
    with DagsterInstance.local_temp() as instance:
        for _ in range(3):
            execute(instance, "duplicate")
        execute(instance, "metadata")
        assert streak(instance).count == 1
        assert allowed(predicate, instance)
        for _ in range(3):
            execute(instance, "metadata")
        assert not allowed(predicate, instance)
        execute(instance, "ok")
        assert streak(instance) is None
        assert allowed(predicate, instance)


def test_canceled_runs_neither_break_nor_extend_the_streak():
    with DagsterInstance.local_temp() as instance:
        execute(instance, "duplicate")
        create(instance, DagsterRunStatus.CANCELED)
        execute(instance, "duplicate")
        assert streak(instance).count == 2


def test_foreign_project_runs_are_ignored():
    with DagsterInstance.local_temp() as instance:
        for _ in range(3):
            alerts.execute_in_process(
                instance=instance,
                run_config={"ops": {"collect": {"config": {"mode": "duplicate"}}}},
                raise_on_error=False,
                tags={PROJECT_TAG: "foreign"},
            )
        assert streak(instance) is None


def test_custom_fingerprint_and_callback_failure_retries_the_alert():
    attempts = []

    def flaky(context, value):
        attempts.append(value.count)
        if len(attempts) == 1:
            raise ConnectionError("경보 채널 오류")

    predicate = breaker(threshold=2, fingerprint=lambda instance, run_id: "same", on_open=flaky)
    with DagsterInstance.local_temp() as instance:
        execute(instance, "duplicate")
        last = execute(instance, "metadata")
        assert not allowed(predicate, instance)
        assert BREAKER_TAG not in instance.get_run_by_id(last).tags
        assert not allowed(predicate, instance)
        assert instance.get_run_by_id(last).tags[BREAKER_FINGERPRINT_TAG] == "same"
        assert attempts == [2, 2]


@pytest.mark.parametrize(
    "kwargs",
    [
        {"threshold": 0},
        {"threshold": 51},
        {"threshold": True},
        {"base_cooldown_seconds": 0},
        {"max_cooldown_seconds": float("inf")},
        {"base_cooldown_seconds": 600, "max_cooldown_seconds": 60},
    ],
)
def test_breaker_rejects_invalid_settings(kwargs):
    with pytest.raises(ValueError):
        breaker(**kwargs)


def queued_record(run_id, age_seconds, status=DagsterRunStatus.QUEUED):
    return SimpleNamespace(
        dagster_run=SimpleNamespace(
            run_id=run_id, status=status, tags={PROJECT_TAG: "test"}, remote_job_origin=None
        ),
        create_timestamp=datetime.now(UTC) - timedelta(seconds=age_seconds),
    )


@pytest.mark.parametrize(
    "records, expected",
    [
        ([], True),
        ([queued_record("young", 10)], False),
        ([queued_record("stale", 7200)], True),
        ([queued_record("stale", 7200), queued_record("young", 10)], False),
        ([queued_record("stale", 7200), queued_record("older", 9000)], False),
        ([queued_record("started", 7200, DagsterRunStatus.STARTED)], False),
    ],
)
def test_stale_queued_run_allows_only_one_extra_tick(monkeypatch, records, expected):
    schedule = coalescing_schedule(
        project="test",
        location_name="test",
        job=alerts,
        cron_schedule="*/5 * * * *",
        queued_stale_after_seconds=3600,
    )
    with DagsterInstance.local_temp() as instance:
        context = build_schedule_context(instance=instance)
        monkeypatch.setattr(context.instance, "get_run_records", lambda **kwargs: records)
        result = schedule.evaluate_tick(context)
        assert bool(result.run_requests) is expected


def test_stale_queued_limit_is_validated():
    for invalid in (0, -1, float("nan"), True):
        with pytest.raises(ValueError):
            coalescing_schedule(
                project="test",
                location_name="test",
                job=alerts,
                cron_schedule="* * * * *",
                queued_stale_after_seconds=invalid,
            )


def test_backoff_grows_caps_and_jitters_within_bounds():
    assert [
        backoff_seconds(n, base_seconds=60, cap_seconds=300, jitter=0) for n in (1, 2, 3, 4, 99)
    ] == [60, 120, 240, 300, 300]
    assert backoff_seconds(10**6, base_seconds=1, cap_seconds=5, jitter=0) == 5
    rng = random.Random(7)
    samples = [
        backoff_seconds(3, base_seconds=60, cap_seconds=3600, jitter=0.25, rng=rng)
        for _ in range(200)
    ]
    assert all(180 <= value <= 240 for value in samples)
    assert len(set(samples)) > 100
    full = [
        backoff_seconds(1, base_seconds=10, cap_seconds=10, jitter=1, rng=rng) for _ in range(50)
    ]
    assert all(0 <= value <= 10 for value in full)


@pytest.mark.parametrize(
    "kwargs",
    [
        {"attempt": 0},
        {"attempt": True},
        {"base_seconds": 0},
        {"cap_seconds": float("nan")},
        {"base_seconds": 10, "cap_seconds": 1},
        {"jitter": 1.5},
        {"jitter": -0.1},
    ],
)
def test_backoff_rejects_invalid_inputs(kwargs):
    values = {"attempt": 1, "base_seconds": 1, "cap_seconds": 10, **kwargs}
    attempt = values.pop("attempt")
    with pytest.raises(ValueError):
        backoff_seconds(attempt, **values)


def test_retry_after_accepts_seconds_and_http_dates():
    now = datetime(2026, 11, 24, 0, 0, tzinfo=UTC).timestamp()
    assert retry_after_seconds("120") == 120
    assert retry_after_seconds(" 0 ") == 0
    assert retry_after_seconds("Tue, 24 Nov 2026 00:01:30 GMT", now=now) == 90
    assert retry_after_seconds("Mon, 23 Nov 2026 23:00:00 GMT", now=now) == 0
    unknown_zone = "Tue, 24 Nov 2026 00:01:30 -0000"
    invalid_values = (None, "", "-5", "1.5", "soon", "9999999999", unknown_zone)
    for invalid in invalid_values:
        assert retry_after_seconds(invalid, now=now) is None


@op(config_schema={"mode": str}, retry_policy=RetryPolicy(max_retries=1))
def collect_with_retry(context):
    raise AlertPageDuplicate("event 중복")


@job(tags=RecoveryPolicy(300).tags(project="test", job_name="alerts_retry"))
def alerts_retry():
    collect_with_retry()


def test_retry_policy_wrapper_is_unwrapped_to_the_original_exception():
    with DagsterInstance.local_temp() as instance:
        run_id = alerts_retry.execute_in_process(
            instance=instance,
            run_config={"ops": {"collect_with_retry": {"config": {"mode": "x"}}}},
            raise_on_error=False,
        ).run_id
        assert failure_fingerprint(instance, run_id) == (
            "STEP_FAILURE|collect_with_retry|AlertPageDuplicate"
        )


def test_worker_and_launch_failures_neither_count_nor_break_the_streak():
    predicate = breaker()
    with DagsterInstance.local_temp() as instance:
        for _ in range(3):
            instance.report_run_failed(create(instance, DagsterRunStatus.STARTING))
        assert streak(instance) is None
        assert allowed(predicate, instance)
        execute(instance, "duplicate")
        execute(instance, "duplicate")
        instance.report_run_failed(create(instance, DagsterRunStatus.STARTING))
        execute(instance, "duplicate")
        assert streak(instance).count == 3
        assert not allowed(predicate, instance)


def test_backfill_runs_and_many_skipped_runs_do_not_hide_the_streak():
    with DagsterInstance.local_temp() as instance:
        for _ in range(3):
            execute(instance, "duplicate")
        for _ in range(12):
            create(instance, DagsterRunStatus.CANCELED)
        alerts.execute_in_process(
            instance=instance,
            run_config={"ops": {"collect": {"config": {"mode": "ok"}}}},
            tags={"dagster/backfill": "b1"},
        )
        assert streak(instance).count == 3
        assert not allowed(breaker(), instance)
