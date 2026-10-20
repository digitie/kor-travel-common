# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
import json
import threading
from types import SimpleNamespace

import pytest

from kortravelcommon.deadline import DeadlineExceeded, call_with_deadline
from kortravelcommon.pg_errors import PgErrorInfo, pg_error_info
from kortravelcommon.stall import (
    MAX_FAILURE_CHARS,
    StallClock,
    due_alert,
    mark_alerted,
    observe_failure,
)

# --- deadline slots ---------------------------------------------------------


def test_custom_slots_reject_immediately_and_stay_held_until_thread_ends():
    slots = threading.BoundedSemaphore(1)
    release = threading.Event()
    finished = threading.Event()

    def blocked():
        release.wait(5)
        finished.set()

    try:
        with pytest.raises(DeadlineExceeded):
            call_with_deadline(blocked, timeout_seconds=0.01, slots=slots)
        # 끝나지 않은 thread가 전용 slot을 쥐고 있으므로 즉시 거절된다.
        with pytest.raises(DeadlineExceeded, match="지정한 slot"):
            call_with_deadline(lambda: 1, timeout_seconds=1, slots=slots)
        # 공용 pool은 영향을 받지 않는다.
        assert call_with_deadline(lambda: 2, timeout_seconds=1) == 2
    finally:
        release.set()
    assert finished.wait(5)
    for _ in range(100):
        if slots.acquire(blocking=False):
            slots.release()
            break
        threading.Event().wait(0.01)
    assert call_with_deadline(lambda: 3, timeout_seconds=1, slots=slots) == 3


def test_custom_slots_released_after_success_and_error():
    slots = threading.BoundedSemaphore(1)
    assert call_with_deadline(lambda: 1, timeout_seconds=1, slots=slots) == 1

    def fail():
        raise KeyError("x")

    with pytest.raises(KeyError):
        call_with_deadline(fail, timeout_seconds=1, slots=slots)
    assert call_with_deadline(lambda: 4, timeout_seconds=1, slots=slots) == 4


# --- pg_errors --------------------------------------------------------------


class FakeAsyncpgError(Exception):
    def __init__(self):
        super().__init__("raw detail Key (id)=(secret) already exists")
        self.sqlstate = "23505"
        self.constraint_name = "uq_job"
        self.message = 'duplicate key value violates unique constraint "uq_job"'
        self.detail = "Key (id)=(secret) already exists"


class AdaptedError(Exception):
    """SQLAlchemy asyncpg 어댑터의 번역 예외처럼 sqlstate만 가진다."""

    def __init__(self, sqlstate):
        super().__init__("<class 'asyncpg...'>: secret")
        self.sqlstate = sqlstate
        self.pgcode = sqlstate


class FakeSqlAlchemyError(Exception):
    def __init__(self, orig):
        super().__init__("(sqlalchemy) statement with secret params")
        self.orig = orig


def _raise_from(outer, inner):
    try:
        raise outer from inner
    except BaseException as exc:
        return exc


def test_asyncpg_through_sqlalchemy_adapter_chain():
    driver = FakeAsyncpgError()
    adapted = _raise_from(AdaptedError("23505"), driver)
    wrapped = _raise_from(FakeSqlAlchemyError(adapted), adapted)
    info = pg_error_info(wrapped)
    assert info == PgErrorInfo(
        "23505", "uq_job", 'duplicate key value violates unique constraint "uq_job"'
    )
    assert "secret" not in repr(info)


def test_psycopg3_and_psycopg2_shapes():
    psycopg3 = Exception("raw")
    psycopg3.sqlstate = "40001"
    psycopg3.diag = SimpleNamespace(
        constraint_name=None, message_primary="could not serialize access", message_detail="x"
    )
    assert pg_error_info(FakeSqlAlchemyError(psycopg3)) == PgErrorInfo(
        "40001", None, "could not serialize access"
    )
    psycopg2 = Exception("raw")
    psycopg2.pgcode = "23503"
    psycopg2.diag = SimpleNamespace(constraint_name="fk_run", message_primary="fk violated")
    assert pg_error_info(psycopg2) == PgErrorInfo("23503", "fk_run", "fk violated")


def test_context_chain_and_unrelated_sqlstate_not_mixed():
    first = Exception("first")
    first.sqlstate = "57014"
    first.constraint_name = "stale"
    first.diag = SimpleNamespace(message_primary="canceling statement")
    second = Exception("second")
    second.sqlstate = "23505"
    try:
        try:
            raise first
        except Exception:
            raise second  # noqa: B904 - __context__ 연쇄를 일부러 만든다.
    except Exception as exc:
        outer = RuntimeError("outer")
        outer.__context__ = exc
    # 처음 만나는 SQLSTATE는 second(23505)이고 앞선 57014의 제약·message는 섞지 않는다.
    assert pg_error_info(outer) == PgErrorInfo("23505", None, None)
    assert pg_error_info(first) == PgErrorInfo("57014", "stale", "canceling statement")


def test_no_pg_error_and_cycle_and_bad_attrs():
    assert pg_error_info(ValueError("x")) is None
    a = Exception("a")
    b = Exception("b")
    a.__cause__ = b
    b.__cause__ = a
    assert pg_error_info(a) is None

    class Exploding(Exception):
        @property
        def sqlstate(self):
            raise RuntimeError("driver bug")

    assert pg_error_info(Exploding()) is None
    wrong = Exception()
    wrong.sqlstate = 23505
    assert pg_error_info(wrong) is None


# --- stall ------------------------------------------------------------------


def test_same_key_keeps_first_failure_when_signature_changes():
    clock = observe_failure(None, key="sync", failure="TimeoutError", now=100)
    clock = mark_alerted(clock, 1200)
    later = observe_failure(clock, key="sync", failure="OperationalError:08006", now=2000)
    assert later.first_failed_at == 100
    assert later.last_failure == "OperationalError:08006"
    assert later.alerted_at == 1200
    other = observe_failure(later, key="other", failure="TimeoutError", now=3000)
    assert other == StallClock("other", 3000, "TimeoutError", None)


def test_due_alert_thresholds():
    clock = observe_failure(None, key="k", failure="E", now=1000)
    assert not due_alert(clock, now=1899)
    assert due_alert(clock, now=1900)
    alerted = mark_alerted(clock, 1900)
    assert not due_alert(alerted, now=5499)
    assert due_alert(alerted, now=5500)
    assert not due_alert(None, now=10**9)
    # 시각이 뒤로 가도 경보하지 않는다.
    assert not due_alert(clock, now=0)
    assert due_alert(clock, now=1010, stall_after=10, realert_after=1)
    for kwargs in ({"stall_after": -1}, {"realert_after": 0}, {"stall_after": float("nan")}):
        with pytest.raises(ValueError):
            due_alert(clock, now=1, **kwargs)


def test_round_trip_is_json_safe_fixed_and_bounded():
    clock = mark_alerted(
        observe_failure(None, key="k", failure="x" * 1000, now=10), 20
    )
    assert len(clock.last_failure) == MAX_FAILURE_CHARS
    encoded = json.dumps(clock.to_dict())
    assert StallClock.from_dict(json.loads(encoded)) == clock
    assert set(clock.to_dict()) == {"key", "first_failed_at", "last_failure", "alerted_at"}


@pytest.mark.parametrize(
    "payload",
    [
        None,
        [],
        {"key": "k", "first_failed_at": 1, "last_failure": "e"},
        {"key": "k", "first_failed_at": 1, "last_failure": "e", "alerted_at": None, "x": 1},
        {"key": "", "first_failed_at": 1, "last_failure": "e", "alerted_at": None},
        {"key": "k" * 201, "first_failed_at": 1, "last_failure": "e", "alerted_at": None},
        {"key": "k", "first_failed_at": True, "last_failure": "e", "alerted_at": None},
        {"key": "k", "first_failed_at": "1", "last_failure": "e", "alerted_at": None},
        {"key": "k", "first_failed_at": float("inf"), "last_failure": "e", "alerted_at": None},
        {"key": "k", "first_failed_at": 1, "last_failure": 5, "alerted_at": None},
        {"key": "k", "first_failed_at": 1, "last_failure": "e" * 201, "alerted_at": None},
        {"key": "k", "first_failed_at": 1, "last_failure": "e", "alerted_at": "x"},
    ],
)
def test_from_dict_rejects_bad_shapes(payload):
    with pytest.raises(ValueError):
        StallClock.from_dict(payload)
