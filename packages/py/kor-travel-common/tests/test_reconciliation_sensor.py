# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
import json
import threading

import pytest
from dagster import build_sensor_context

import kortravelcommon.dagster as dagster_module
from kortravelcommon.dagster import reconciliation_sensor
from kortravelcommon.stall import StallClock


class PgError(Exception):
    def __init__(self):
        super().__init__("raw message with secret value")
        self.sqlstate = "08006"


def _tick(sensor_def, cursor=None):
    return sensor_def.evaluate_tick(build_sensor_context(cursor=cursor))


def _clock(cursor):
    assert cursor.startswith("stall:")
    payload = json.loads(cursor[len("stall:") :])
    return None if payload is None else StallClock.from_dict(payload)


def test_legacy_signature_and_behavior_unchanged():
    calls = []

    def reconcile(context):
        calls.append(context)
        return 3

    sensor_def = reconciliation_sensor(
        name="legacy", reconcile=reconcile, required_resource_keys=set()
    )
    result = _tick(sensor_def)
    assert len(calls) == 1
    assert "3건" in result.skip_message
    assert result.cursor is None

    def broken(context):
        raise RuntimeError("boom")

    failing = reconciliation_sensor(name="legacy2", reconcile=broken, required_resource_keys=set())
    with pytest.raises(Exception, match="boom"):
        _tick(failing)


def test_budget_passes_remaining_and_bounds_wait():
    seen = []

    def reconcile(context, remaining):
        seen.append(remaining())
        return 1

    sensor_def = reconciliation_sensor(
        name="budget", reconcile=reconcile, required_resource_keys=set(), budget_seconds=5
    )
    _tick(sensor_def)
    assert 0 < seen[0] <= 5

    release = threading.Event()
    entered = threading.Event()

    def hang(context, remaining):
        entered.set()
        release.wait(5)
        return 0

    hanging = reconciliation_sensor(
        name="hang", reconcile=hang, required_resource_keys=set(), budget_seconds=0.05
    )
    try:
        with pytest.raises(Exception, match="대기 상한"):
            _tick(hanging)
        assert entered.wait(1)
        entered.clear()
        # 이전 콜백이 아직 전용 slot을 쥐고 있으므로 새 콜백은 시작조차 하지 않는다.
        with pytest.raises(Exception, match="slot"):
            _tick(hanging)
        assert not entered.is_set()
    finally:
        release.set()


@pytest.mark.parametrize("value", [0, -1, float("nan"), float("inf"), True, "5"])
def test_invalid_budget_rejected(value):
    with pytest.raises(ValueError):
        reconciliation_sensor(
            name="x", reconcile=lambda c, r: 0, required_resource_keys=set(), budget_seconds=value
        )


def test_invalid_stall_thresholds_rejected():
    with pytest.raises(ValueError):
        reconciliation_sensor(
            name="x", reconcile=lambda c: 0, required_resource_keys=set(), realert_after_seconds=0
        )


def test_stall_clock_lifecycle_in_cursor(monkeypatch, capfd):
    now = [1000.0]
    monkeypatch.setattr(dagster_module, "wall_clock", lambda: now[0])
    outcome = {"fail": PgError()}
    alerts = []

    def reconcile(context):
        if outcome["fail"] is not None:
            raise outcome["fail"]
        return 2

    sensor_def = reconciliation_sensor(
        name="weather_sync_recovery",
        reconcile=reconcile,
        required_resource_keys=set(),
        on_stall=lambda context, clock: alerts.append(clock),
        stall_after_seconds=900,
        realert_after_seconds=3600,
    )
    result = _tick(sensor_def)
    clock = _clock(result.cursor)
    assert clock == StallClock("weather_sync_recovery", 1000.0, "PgError:08006", None)
    assert "secret" not in result.cursor
    # 예외는 tick 실패 대신 context.log로 드러난다.
    assert "PgError:08006" in capfd.readouterr().err
    assert alerts == []

    # 실패 서명이 바뀌어도 정체 시작 시각은 유지된다.
    now[0] = 1899.0
    outcome["fail"] = TimeoutError()
    result = _tick(sensor_def, result.cursor)
    assert _clock(result.cursor).first_failed_at == 1000.0
    assert _clock(result.cursor).last_failure == "TimeoutError"
    assert alerts == []

    now[0] = 1900.0
    result = _tick(sensor_def, result.cursor)
    assert len(alerts) == 1 and alerts[0].first_failed_at == 1000.0
    assert _clock(result.cursor).alerted_at == 1900.0

    now[0] = 5499.0
    result = _tick(sensor_def, result.cursor)
    assert len(alerts) == 1
    now[0] = 5500.0
    result = _tick(sensor_def, result.cursor)
    assert len(alerts) == 2

    outcome["fail"] = None
    result = _tick(sensor_def, result.cursor)
    assert result.cursor == "stall:null"
    assert "2건" in result.skip_message

    # 성공 뒤 새 실패는 새 시계로 시작한다.
    now[0] = 9000.0
    outcome["fail"] = PgError()
    result = _tick(sensor_def, result.cursor)
    assert _clock(result.cursor).first_failed_at == 9000.0


def test_failing_on_stall_retries_next_tick_and_cursor_still_committed(monkeypatch):
    now = [0.0]
    monkeypatch.setattr(dagster_module, "wall_clock", lambda: now[0])
    attempts = []

    def on_stall(context, clock):
        attempts.append(clock)
        if len(attempts) == 1:
            raise RuntimeError("alert channel down")

    def reconcile(context):
        raise RuntimeError("db down")

    sensor_def = reconciliation_sensor(
        name="s",
        reconcile=reconcile,
        required_resource_keys=set(),
        on_stall=on_stall,
        stall_after_seconds=0,
    )
    result = _tick(sensor_def)
    assert len(attempts) == 1
    assert _clock(result.cursor).alerted_at is None
    now[0] = 60.0
    result = _tick(sensor_def, result.cursor)
    assert len(attempts) == 2
    assert _clock(result.cursor).alerted_at == 60.0


def test_budget_timeout_is_recorded_with_on_stall(monkeypatch):
    monkeypatch.setattr(dagster_module, "wall_clock", lambda: 100.0)
    release = threading.Event()

    def hang(context, remaining):
        release.wait(5)
        return 0

    sensor_def = reconciliation_sensor(
        name="t",
        reconcile=hang,
        required_resource_keys=set(),
        budget_seconds=0.05,
        on_stall=lambda context, clock: None,
    )
    try:
        result = _tick(sensor_def)
        assert _clock(result.cursor).last_failure == "DeadlineExceeded"
        result = _tick(sensor_def, result.cursor)
        assert _clock(result.cursor).last_failure == "DeadlineExceeded"
        assert _clock(result.cursor).first_failed_at == 100.0
    finally:
        release.set()


_HUGE = "1" + "0" * 400
_CORRUPT = [
    "stall:{bad",
    'stall:{"key":"x"}',
    "other",
    "stall:[]",
    # float 범위를 넘는 정수와 깊은 중첩도 sensor를 멈추지 않는다.
    'stall:{"key":"c","first_failed_at":' + _HUGE + ',"last_failure":"e","alerted_at":null}',
    "stall:" + "[" * 100000,
]


@pytest.mark.parametrize("cursor", _CORRUPT)
def test_corrupt_cursor_starts_new_clock(monkeypatch, cursor):
    monkeypatch.setattr(dagster_module, "wall_clock", lambda: 7.0)

    def reconcile(context):
        raise RuntimeError("down")

    sensor_def = reconciliation_sensor(
        name="c", reconcile=reconcile, required_resource_keys=set(), on_stall=lambda c, k: None
    )
    result = _tick(sensor_def, cursor)
    assert _clock(result.cursor) == StallClock("c", 7.0, "RuntimeError", None)


def test_overlong_name_rejected_at_definition_with_on_stall():
    with pytest.raises(ValueError):
        reconciliation_sensor(
            name="n" * 201,
            reconcile=lambda c: 0,
            required_resource_keys=set(),
            on_stall=lambda c, k: None,
        )
