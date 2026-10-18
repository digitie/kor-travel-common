# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"""같은 좌표의 주소 변경·달력 주기·중단 재개를 결과에 결박한다."""

from datetime import UTC, datetime, timedelta

import pytest
from sqlalchemy import MetaData, create_engine

from kortravelcommon.reverse_address import (
    AddressResolver,
    AddressTarget,
    OwnershipLost,
    ReverseAddressError,
    ReverseAddressStore,
    refresh_reverse_addresses,
    reverse_address_tables,
    six_months_after,
)

START = datetime(2026, 1, 31, 10, tzinfo=UTC)


class Resolver(AddressResolver):
    provider_id = "fixture"

    def __init__(self):
        self.calls = []
        self.address = "구주소"
        self.fail = False

    def reverse(self, target):
        self.calls.append(target.key)
        if self.fail:
            raise ReverseAddressError("fixture_failure")
        return {
            "provider": "fixture",
            "address": {"full": self.address},
            "region": {"legal_dong": self.address},
        }


@pytest.fixture
def setup_store(tmp_path):
    engine = create_engine("sqlite:///" + str(tmp_path / "addresses.db"))
    metadata = MetaData()
    reverse_address_tables(metadata)
    metadata.create_all(engine)
    store = ReverseAddressStore(engine, "fixture")
    yield store
    engine.dispose()


def run(store, resolver, targets, now=START, **kwargs):
    def page(cursor, limit):
        return [target for target in targets if target.key > cursor][:limit]

    def retries(at, limit):
        due = []
        for target in targets:
            row = store.row(target.key)
            if row is not None and row["status"] == "error" and (
                row["coordinate_key"] != target.coordinate_key
                or row["next_retry_at"].replace(tzinfo=UTC) <= at
            ):
                due.append((row["next_retry_at"], target.key, target))
        return [target for _, _, target in sorted(due)[:limit]]

    return refresh_reverse_addresses(
        store,
        resolver,
        page,
        retries,
        pending_failures=lambda: any(
            (row := store.row(target.key)) is not None and row["status"] == "error"
            for target in targets
        ),
        now=lambda: now,
        **kwargs,
    )


def test_same_coordinate_new_address_after_six_calendar_months(setup_store):
    target = AddressTarget("a", 127, 37)
    resolver = Resolver()
    first = run(setup_store, resolver, [target])
    assert first["requests"] == 1
    assert setup_store.row("a")["next_refresh_at"] == datetime(2026, 7, 31, 10)
    resolver.address = "신주소"
    early = run(setup_store, resolver, [target], now=datetime(2026, 7, 30, 10, tzinfo=UTC))
    assert early["requests"] == 0
    due = run(setup_store, resolver, [target], now=datetime(2026, 7, 31, 10, tzinfo=UTC))
    assert due["requests"] == due["changed"] == 1
    assert setup_store.row("a")["payload"]["address"]["full"] == "신주소"
    assert target.longitude == 127 and target.latitude == 37


@pytest.mark.parametrize(
    "start,expected",
    [
        (datetime(2025, 8, 31, tzinfo=UTC), datetime(2026, 2, 28, tzinfo=UTC)),
        (datetime(2023, 8, 31, tzinfo=UTC), datetime(2024, 2, 29, tzinfo=UTC)),
    ],
)
def test_calendar_month_end(start, expected):
    assert six_months_after(start) == expected


def test_manual_force_resumes_one_cycle_and_reuses_same_point(setup_store):
    targets = [
        AddressTarget("a", 127, 37),
        AddressTarget("b", 127, 37),
        AddressTarget("c", 128, 38),
    ]
    resolver = Resolver()
    assert run(setup_store, resolver, targets, force=True, batch_size=1)["remaining"] == 1
    cycle = setup_store.row("a")["refresh_id"]
    assert run(setup_store, resolver, targets, force=True, batch_size=1)["requests"] == 0
    assert setup_store.row("b")["refresh_id"] == cycle
    assert run(setup_store, resolver, targets, force=True, batch_size=1)["remaining"] == 0
    assert resolver.calls == ["a", "c"]
    # 완료 뒤의 새 수동 실행은 6개월 전이어도 새 조회를 한다.
    run(setup_store, resolver, targets, force=True)
    assert resolver.calls == ["a", "c", "a", "c"]


def test_failure_keeps_good_address_and_retries_after_backoff(setup_store):
    resolver = Resolver()
    targets = [AddressTarget("a", 127, 37)]
    run(setup_store, resolver, targets)
    resolver.fail = True
    failed = run(setup_store, resolver, targets, now=START + timedelta(days=200))
    assert failed["failed"] == 1
    row = setup_store.row("a")
    assert row["payload"]["address"]["full"] == "구주소"
    assert row["resolved_at"] == START.replace(tzinfo=None)
    assert run(setup_store, resolver, targets, now=START + timedelta(days=200))["requests"] == 0
    resolver.fail = False
    resolver.address = "신주소"
    run(setup_store, resolver, targets, now=START + timedelta(days=200, minutes=3))
    assert setup_store.row("a")["status"] == "ok"
    assert setup_store.row("a")["payload"]["address"]["full"] == "신주소"


def test_reusing_a_point_does_not_extend_its_provider_verification(setup_store):
    resolver = Resolver()
    targets = [AddressTarget("a", 127, 37)]
    run(setup_store, resolver, targets)
    targets.append(AddressTarget("b", 127, 37))
    result = run(setup_store, resolver, targets, now=datetime(2026, 6, 1, tzinfo=UTC))
    assert result["reused"] == 1
    assert setup_store.row("b")["next_refresh_at"] == datetime(2026, 7, 31, 10)
    assert resolver.calls == ["a"]


def test_expired_owner_cannot_write_or_unlock_new_owner(setup_store):
    assert setup_store.claim("old", START)
    assert not setup_store.claim("other", START)
    assert setup_store.claim("new", START + timedelta(seconds=91))
    with pytest.raises(OwnershipLost):
        setup_store.save(
            "old",
            AddressTarget("a", 127, 37),
            "",
            START + timedelta(seconds=92),
            {"address": {"full": "잘못된 늦은 값"}},
            None,
        )
    setup_store.release("old")
    assert not setup_store.claim("third", START + timedelta(seconds=92))
    assert setup_store.row("a") is None


def test_changed_coordinate_never_serves_previous_coordinate_address(setup_store):
    resolver = Resolver()
    run(setup_store, resolver, [AddressTarget("a", 127, 37)])
    moved = AddressTarget("a", 128, 38)
    assert setup_store.projections([moved]) == {}
    resolver.fail = True
    run(setup_store, resolver, [moved])
    assert setup_store.row("a")["payload"] is None


def test_same_result_is_not_reported_as_address_change(setup_store):
    resolver = Resolver()
    target = AddressTarget("a", 127, 37)
    run(setup_store, resolver, [target])
    assert run(setup_store, resolver, [target], force=True)["changed"] == 0


def test_poison_retry_does_not_starve_next_location_at_smallest_batch(setup_store):
    class SelectiveResolver(Resolver):
        def reverse(self, target):
            if target.key == "a":
                self.calls.append(target.key)
                raise ReverseAddressError("fixture_failure")
            return super().reverse(target)

    resolver = SelectiveResolver()
    targets = [AddressTarget("a", 127, 37), AddressTarget("b", 128, 38)]
    for tick in range(3):
        run(
            setup_store,
            resolver,
            targets,
            batch_size=1,
            now=START + timedelta(hours=tick),
        )
    assert resolver.calls == ["a", "b", "a"]
    assert setup_store.row("b")["status"] == "ok"


def test_kst_calendar_month_boundary():
    # 4월 30일 18 UTC == 5월 1일 03 KST -> 11월 1일 03 KST.
    assert six_months_after(datetime(2026, 4, 30, 18, tzinfo=UTC)) == datetime(
        2026, 10, 31, 18, tzinfo=UTC
    )


def test_database_source_due_manual_resume_and_changed_coordinate(setup_store):
    from sqlalchemy import Column, Float, String, Table, insert, select, update

    from kortravelcommon.reverse_address import DatabaseAddressSource

    metadata = MetaData()
    targets = Table(
        "targets",
        metadata,
        Column("target_key", String, primary_key=True),
        Column("longitude", Float),
        Column("latitude", Float),
        Column("display_name", String),
    )
    metadata.create_all(setup_store.engine)
    with setup_store.engine.begin() as conn:
        conn.execute(
            insert(targets),
            [
                {"target_key": "a", "longitude": 127, "latitude": 37, "display_name": "첫 위치"},
                {"target_key": "b", "longitude": 128, "latitude": 38, "display_name": "둘째"},
            ],
        )
    source = DatabaseAddressSource(setup_store, select(targets))
    assert source.has_work(START)
    assert not source.has_work(START, automatic=False)
    resolver = Resolver()
    result = refresh_reverse_addresses(
        setup_store,
        resolver,
        source.page,
        source.retries,
        pending_failures=source.pending_failures,
        force=True,
        batch_size=1,
        now=lambda: START,
    )
    assert result["remaining"] == 1
    assert source.has_work(START, automatic=False)
    refresh_reverse_addresses(
        setup_store, resolver, source.page, source.retries,
        pending_failures=source.pending_failures, now=lambda: START,
    )
    assert not source.has_work(START)
    assert source.summary()["total"] == 2
    assert len(source.sample()) == 2
    assert source.has_work(datetime(2026, 7, 31, 10, tzinfo=UTC))
    with setup_store.engine.begin() as conn:
        conn.execute(update(targets).where(targets.c.target_key == "a").values(longitude=129))
    assert source.has_work(START)
    assert [row["target_key"] for row in source.sample()] == ["b"]


def test_provider_switch_with_identical_address_is_not_change(setup_store):
    resolver = Resolver()
    target = AddressTarget("a", 127, 37)
    run(setup_store, resolver, [target])
    original = resolver.reverse
    resolver.reverse = lambda value: {**original(value), "provider": "fallback"}
    assert run(setup_store, resolver, [target], force=True)["changed"] == 0


def test_normal_not_found_is_reused_without_inventing_resolution_time(setup_store):
    class NoAddress(Resolver):
        def reverse(self, target):
            self.calls.append(target.key)
            return None

    resolver = NoAddress()
    targets = [AddressTarget(str(index).zfill(3), 127, 37) for index in range(50)]
    result = run(setup_store, resolver, targets)
    assert result["requests"] == 1 and result["reused"] == 49
    assert setup_store.row("049")["status"] == "not_found"
    assert setup_store.row("049")["payload"] is None
    assert setup_store.row("049")["resolved_at"] is None
    assert setup_store.row("049")["checked_at"] == START.replace(tzinfo=None)


def test_expired_owner_after_completion_is_not_reported_in_progress(setup_store):
    from sqlalchemy import Column, Float, String, Table, select

    from kortravelcommon.reverse_address import DatabaseAddressSource

    metadata = MetaData()
    target = Table(
        "summary_targets",
        metadata,
        Column("target_key", String),
        Column("longitude", Float),
        Column("latitude", Float),
    )
    metadata.create_all(setup_store.engine)
    source = DatabaseAddressSource(setup_store, select(target))
    now = datetime.now(UTC)
    assert setup_store.claim("crashed", now - timedelta(minutes=3))
    assert not source.summary()["in_progress"]
    assert setup_store.claim("live", now)
    assert source.summary()["in_progress"]
    setup_store.release("live")
    assert not source.summary()["in_progress"]


def retry_source(store):
    from sqlalchemy import Column, Float, String, Table, insert, select

    from kortravelcommon.reverse_address import DatabaseAddressSource

    metadata = MetaData()
    targets = Table(
        "retry_targets", metadata,
        Column("target_key", String, primary_key=True),
        Column("longitude", Float), Column("latitude", Float),
    )
    metadata.create_all(store.engine)
    with store.engine.begin() as conn:
        conn.execute(insert(targets), {"target_key": "a", "longitude": 127, "latitude": 37})
    return DatabaseAddressSource(store, select(targets)), targets


def refresh_source(source, resolver, now=START, **kwargs):
    return refresh_reverse_addresses(
        source.store, resolver, source.page, source.retries,
        pending_failures=source.pending_failures, now=lambda: now, **kwargs,
    )


def test_manual_failure_resumes_after_backoff_even_when_automatic_disabled(setup_store):
    source, _ = retry_source(setup_store)
    resolver = Resolver()
    resolver.fail = True
    result = refresh_source(source, resolver, force=True)
    assert result["remaining"] == 1
    assert not source.has_work(START + timedelta(minutes=1), automatic=False)
    assert source.has_work(START + timedelta(minutes=3), automatic=False)
    resolver.fail = False
    result = refresh_source(source, resolver, now=START + timedelta(minutes=3))
    assert result["remaining"] == 0 and result["requests"] == 1
    assert setup_store.row("a")["status"] == "ok"
    assert not source.has_work(START + timedelta(days=200), automatic=False)


def test_manual_cycle_waits_for_an_existing_failure_without_resetting_backoff(setup_store):
    source, _ = retry_source(setup_store)
    resolver = Resolver()
    resolver.fail = True
    refresh_source(source, resolver)
    result = refresh_source(source, resolver, force=True, now=START + timedelta(seconds=30))
    assert result["requests"] == 0 and result["remaining"] == 1
    assert not source.has_work(START + timedelta(minutes=1), automatic=False)
    assert source.has_work(START + timedelta(minutes=3), automatic=False)


def test_removed_manual_failure_does_not_leave_a_permanent_pending_cycle(setup_store):
    from sqlalchemy import delete

    source, targets = retry_source(setup_store)
    resolver = Resolver()
    resolver.fail = True
    refresh_source(source, resolver, force=True)
    with setup_store.engine.begin() as conn:
        conn.execute(delete(targets))
    assert source.has_work(START, automatic=False)  # provider 없는 마지막 정리 tick
    refresh_source(source, resolver, now=START + timedelta(minutes=1))
    assert not source.has_work(START, automatic=False)


def test_inactive_failure_rows_do_not_starve_the_live_manual_retry(setup_store):
    source, _ = retry_source(setup_store)
    resolver = Resolver()
    resolver.fail = True
    refresh_source(source, resolver, force=True)
    old = START - timedelta(days=1)
    assert setup_store.claim("orphan-fixture", old)
    for index in range(11):
        setup_store.save(
            "orphan-fixture", AddressTarget(f"removed-{index}", 128, 38), "",
            old, None, "fixture_failure",
        )
    setup_store.release("orphan-fixture")
    resolver.fail = False
    assert source.has_work(START + timedelta(minutes=3), automatic=False)
    result = refresh_source(source, resolver, now=START + timedelta(minutes=3))
    assert result["requests"] == 1
    assert setup_store.row("a")["status"] == "ok"
    assert result["remaining"] == 0
