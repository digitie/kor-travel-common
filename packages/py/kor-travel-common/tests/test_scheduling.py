# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"""실제 Dagster 달력과 예약 판정으로 고정 phase 계약을 확인한다."""

from collections import Counter
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import pytest
from dagster import DagsterInstance, DagsterRunStatus, build_schedule_context, job, op
from dagster._utils.schedules import schedule_execution_time_iterator

from kortravelcommon.dagster import RecoveryPolicy, coalescing_schedule
from kortravelcommon.scheduling import staggered_cron


def calendar(cron, start, end):
    result = []
    for tick in schedule_execution_time_iterator(start.timestamp(), cron, str(start.tzinfo)):
        if tick >= end:
            return result
        result.append(tick)
    raise AssertionError("유한 달력 경계에 도달하지 못함")


@pytest.mark.parametrize("interval", [1, 2, 3, 4, 5, 6, 10, 12, 15, 20, 30, 60,
                                     120, 180, 240, 360, 480, 720, 1440])
@pytest.mark.parametrize("last_phase", [False, True])
def test_supported_periods_have_exact_daily_count_phase_and_month_boundary(interval, last_phase):
    phase = interval - 1 if last_phase else 0
    start = datetime(2028, 2, 29, tzinfo=ZoneInfo("Asia/Seoul"))
    end = start + timedelta(days=2)
    ticks = calendar(staggered_cron(interval_minutes=interval, phase_minutes=phase), start, end)
    assert len(ticks) == 2 * 1440 // interval
    assert ticks[0] == start + timedelta(minutes=phase)
    assert all(b - a == timedelta(minutes=interval)
               for a, b in zip(ticks, ticks[1:], strict=False))
    assert set(Counter(tick.date() for tick in ticks).values()) == {1440 // interval}


@pytest.mark.parametrize("timezone", ["Asia/Seoul", "UTC"])
def test_weather_reserves_distinct_phases_without_changing_72_daily_ticks(timezone):
    start = datetime(2026, 12, 31, tzinfo=ZoneInfo(timezone))
    end = start + timedelta(days=2)
    baseline = calendar("15 */3 * * *", start, end)
    phases = [7, 27, 47, 67, 87, 107, 127, 147, 167]
    reservations = Counter()
    crons = {}
    for phase in phases:
        cron = staggered_cron(interval_minutes=180, phase_minutes=phase)
        crons[phase] = cron
        ticks = calendar(cron, start, end)
        assert len(ticks) == len(baseline) == 16
        reservations.update(ticks)
    assert len(reservations) == 144 and max(reservations.values()) == 1
    assert len(baseline) * 9 == sum(reservations.values())
    # 다른 예약을 추가해도 기존 phase의 cron은 변하지 않는다.
    staggered_cron(interval_minutes=180, phase_minutes=177)
    assert crons == {phase: staggered_cron(interval_minutes=180, phase_minutes=phase)
                     for phase in reversed(phases)}


def test_transport_keeps_five_minute_cadence_and_288_ticks_per_job():
    start = datetime(2026, 1, 31, tzinfo=ZoneInfo("Asia/Seoul"))
    end = start + timedelta(days=1)
    baseline = calendar("*/5 * * * *", start, end)
    shifted = [calendar(staggered_cron(interval_minutes=5, phase_minutes=phase), start, end)
               for phase in [1, 3]]
    assert len(baseline) == len(shifted[0]) == len(shifted[1]) == 288
    assert set(shifted[0]).isdisjoint(shifted[1])
    assert all(b - a == timedelta(minutes=5) for ticks in shifted
               for a, b in zip(ticks, ticks[1:], strict=False))


def test_dst_calendar_is_wall_clock_not_a_fixed_elapsed_time_guarantee():
    start = datetime(2026, 3, 7, tzinfo=ZoneInfo("America/New_York"))
    ticks = calendar(staggered_cron(interval_minutes=1440, phase_minutes=180),
                     start, start + timedelta(days=3))
    assert len(ticks) == 3 and all(tick.hour == 3 for tick in ticks)
    assert ticks[1].timestamp() - ticks[0].timestamp() == 23 * 3600


@pytest.mark.parametrize("value", [True, False, None, 5.0, "5", [], {}])
@pytest.mark.parametrize("field", ["interval_minutes", "phase_minutes"])
def test_non_integer_inputs_are_rejected(value, field):
    kwargs = {"interval_minutes": 5, "phase_minutes": 1, field: value}
    with pytest.raises(TypeError):
        staggered_cron(**kwargs)


@pytest.mark.parametrize("interval", [0, -1, 7, 45, 61, 90, 100, 150, 1000, 2880])
def test_periods_that_do_not_tile_the_clock_are_rejected(interval):
    with pytest.raises(ValueError):
        staggered_cron(interval_minutes=interval, phase_minutes=0)


@pytest.mark.parametrize("phase", [-1, 5, 6])
def test_phase_outside_period_is_rejected(phase):
    with pytest.raises(ValueError):
        staggered_cron(interval_minutes=5, phase_minutes=phase)


def test_existing_coalescing_and_recovery_contract_is_preserved():
    @op
    def noop():
        pass

    tags = RecoveryPolicy(300).tags(project="phase-test", job_name="collect")

    @job(tags=tags)
    def collect():
        noop()

    schedule = coalescing_schedule(
        project="phase-test", location_name="phase-test", job=collect,
        cron_schedule=staggered_cron(interval_minutes=5, phase_minutes=3),
        execution_timezone="Asia/Seoul",
    )
    with DagsterInstance.local_temp() as instance:
        run = instance.create_run_for_job(collect, status=DagsterRunStatus.STARTED, tags=tags)
        context = build_schedule_context(instance=instance)
        assert schedule.evaluate_tick(context).skip_message
        instance.report_run_failed(run)
        assert len(schedule.evaluate_tick(context).run_requests) == 1
