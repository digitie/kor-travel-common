# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"""같은 좌표의 주소 변경을 위한 공통 검증·영속 갱신 엔진."""

from __future__ import annotations

import hashlib
import json
import math
import time
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Any
from uuid import uuid4

from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    DateTime,
    Float,
    Integer,
    MetaData,
    String,
    Table,
    and_,
    func,
    insert,
    or_,
    select,
    update,
)
from sqlalchemy.engine import Connection, Engine, make_url


class ReverseAddressError(RuntimeError):
    """비밀·원문 응답을 싣지 않는 유한한 실패 코드."""


class OwnershipLost(ReverseAddressError):
    """만료·교체된 worker의 늦은 결과는 게시하지 않는다."""


@dataclass(frozen=True)
class AddressTarget:
    key: str
    longitude: float
    latitude: float

    def __post_init__(self) -> None:
        if not self.key or len(self.key) > 240:
            raise ValueError("위치 식별자가 유효하지 않습니다.")
        if not (math.isfinite(self.longitude) and math.isfinite(self.latitude)):
            raise ValueError("좌표는 유한해야 합니다.")
        if not (-180 <= self.longitude <= 180 and -90 <= self.latitude <= 90):
            raise ValueError("좌표 범위를 벗어났습니다.")

    @property
    def coordinate_key(self) -> str:
        return _digest([float(self.longitude) or 0.0, float(self.latitude) or 0.0])


def _digest(value: Any) -> str:
    encoded = json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(encoded.encode()).hexdigest()


def reverse_address_tables(metadata: MetaData) -> tuple[Table, Table]:
    """소비자 migration이 소유하는 두 공통 테이블의 SQLAlchemy 선언."""
    if "reverse_address_entries" in metadata.tables:
        return metadata.tables["reverse_address_entries"], metadata.tables[
            "reverse_address_control"
        ]
    entries = Table(
        "reverse_address_entries",
        metadata,
        Column("provider_id", String(64), primary_key=True),
        Column("target_key", String(240), primary_key=True),
        Column("coordinate_key", String(64), nullable=False, index=True),
        Column("longitude", Float, nullable=False),
        Column("latitude", Float, nullable=False),
        Column("refresh_id", String(64)),
        Column("payload", JSON),
        Column("result_hash", String(64)),
        Column("status", String(20), nullable=False),
        Column("checked_at", DateTime(timezone=True), nullable=False),
        Column("resolved_at", DateTime(timezone=True)),
        Column("next_retry_at", DateTime(timezone=True), index=True),
        Column("next_refresh_at", DateTime(timezone=True), index=True),
        Column("failures", Integer, nullable=False),
        Column("error_code", String(80)),
    )
    control = Table(
        "reverse_address_control",
        metadata,
        Column("provider_id", String(64), primary_key=True),
        Column("refresh_id", String(64)),
        Column("cursor", String(240), nullable=False),
        Column("force_refresh", Boolean, nullable=False, default=False),
        Column("owner", String(36)),
        Column("lease_until", DateTime(timezone=True)),
    )
    return entries, control


class AddressResolver:
    """외부 provider 구현을 소비하는 주입 경계."""

    provider_id: str

    def reverse(self, target: AddressTarget) -> dict[str, Any] | None:
        raise NotImplementedError


def six_months_after(value: datetime) -> datetime:
    """180일이 아닌 달력 6개월. 월말은 대상 월의 마지막 날로 맞춘다."""
    from calendar import monthrange
    from zoneinfo import ZoneInfo

    if value.tzinfo is None:
        raise ValueError("timezone-aware 시각이 필요합니다.")
    original_zone = value.tzinfo
    value = value.astimezone(ZoneInfo("Asia/Seoul"))
    month = value.month + 6
    year = value.year + (month - 1) // 12
    month = (month - 1) % 12 + 1
    return value.replace(
        year=year, month=month, day=min(value.day, monthrange(year, month)[1])
    ).astimezone(original_zone)


def address_engine(database_url: str) -> Engine:
    """앱의 같은 DB에 연결하되 작업/조회가 끝나면 소비자가 dispose한다."""
    from sqlalchemy import create_engine

    url = make_url(database_url)
    if url.drivername in {"postgres", "postgresql", "postgresql+asyncpg"}:
        url = url.set(drivername="postgresql+psycopg2")
    elif url.drivername == "sqlite+aiosqlite":
        url = url.set(drivername="sqlite")
    options: dict[str, Any] = {"pool_pre_ping": True}
    if url.get_backend_name() == "postgresql":
        options.update(
            pool_size=1,
            max_overflow=0,
            connect_args={
                "connect_timeout": 5,
                "options": "-c statement_timeout=10000 -c lock_timeout=2000",
            },
        )
    return create_engine(url, **options)


class ReverseAddressStore:
    """소비자 DB의 파생 주소·커서. 원천 테이블은 읽거나 쓰지 않는다."""

    def __init__(self, engine: Engine, provider_id: str) -> None:
        self.engine = engine
        self.provider_id = provider_id
        self.entries, self.control = reverse_address_tables(MetaData())

    def _control_where(self) -> Any:
        return self.control.c.provider_id == self.provider_id

    def claim(self, owner: str, now: datetime) -> bool:
        from sqlalchemy.exc import IntegrityError

        with self.engine.begin() as conn:
            if conn.execute(select(self.control).where(self._control_where())).first() is None:
                try:
                    with conn.begin_nested():
                        conn.execute(
                            insert(self.control).values(
                                provider_id=self.provider_id,
                                cursor="",
                                refresh_id=None,
                                force_refresh=False,
                            )
                        )
                except IntegrityError:
                    pass
            count = conn.execute(
                update(self.control)
                .where(
                    self._control_where(),
                    or_(self.control.c.owner.is_(None), self.control.c.lease_until <= now),
                )
                .values(owner=owner, lease_until=now + timedelta(seconds=90))
            ).rowcount
        return count == 1

    def _fence(self, conn: Connection, owner: str, now: datetime) -> None:
        count = conn.execute(
            update(self.control)
            .where(
                self._control_where(),
                self.control.c.owner == owner,
                self.control.c.lease_until > now,
            )
            .values(lease_until=now + timedelta(seconds=90))
        ).rowcount
        if count != 1:
            raise OwnershipLost("lease_lost")

    def prepare(self, owner: str, force: bool, now: datetime) -> tuple[str, str, bool]:
        with self.engine.begin() as conn:
            self._fence(conn, owner, now)
            row = conn.execute(select(self.control).where(self._control_where())).mappings().one()
            if force and not row["force_refresh"]:
                cycle = str(uuid4())
                conn.execute(
                    update(self.control)
                    .where(self._control_where())
                    .values(refresh_id=cycle, cursor="", force_refresh=True)
                )
                return "", cycle, True
            return row["cursor"], row["refresh_id"] or "", bool(row["force_refresh"])

    def complete_cycle(self, owner: str, now: datetime) -> None:
        with self.engine.begin() as conn:
            self._fence(conn, owner, now)
            conn.execute(
                update(self.control)
                .where(self._control_where())
                .values(cursor="", force_refresh=False)
            )

    def advance(self, owner: str, cursor: str, now: datetime) -> None:
        with self.engine.begin() as conn:
            self._fence(conn, owner, now)
            conn.execute(update(self.control).where(self._control_where()).values(cursor=cursor))

    def release(self, owner: str) -> None:
        with self.engine.begin() as conn:
            conn.execute(
                update(self.control)
                .where(
                    self._control_where(),
                    self.control.c.owner == owner,
                )
                .values(owner=None, lease_until=None)
            )

    def row(self, key: str) -> Mapping[str, Any] | None:
        with self.engine.connect() as conn:
            return (
                conn.execute(
                    select(self.entries).where(
                        self.entries.c.provider_id == self.provider_id,
                        self.entries.c.target_key == key,
                    )
                )
                .mappings()
                .first()
            )

    def reuse(
        self, target: AddressTarget, cycle: str, force: bool, now: datetime
    ) -> Mapping[str, Any] | None:
        with self.engine.connect() as conn:
            eligible = (
                self.entries.c.refresh_id == cycle
                if force
                else (self.entries.c.next_refresh_at > now)
            )
            return (
                conn.execute(
                    select(self.entries)
                    .where(
                        self.entries.c.provider_id == self.provider_id,
                        self.entries.c.coordinate_key == target.coordinate_key,
                        self.entries.c.status == "ok",
                        eligible,
                    )
                    .order_by(self.entries.c.resolved_at.desc())
                    .limit(1)
                )
                .mappings()
                .first()
            )

    def retries(self, now: datetime, limit: int) -> list[str]:
        with self.engine.connect() as conn:
            return list(
                conn.execute(
                    select(self.entries.c.target_key)
                    .where(
                        self.entries.c.provider_id == self.provider_id,
                        self.entries.c.next_retry_at <= now,
                    )
                    .order_by(self.entries.c.next_retry_at, self.entries.c.target_key)
                    .limit(limit)
                ).scalars()
            )

    def save(
        self,
        owner: str,
        target: AddressTarget,
        cycle: str,
        now: datetime,
        payload: dict[str, Any] | None,
        error: str | None,
        reused_from: Mapping[str, Any] | None = None,
    ) -> bool:
        with self.engine.begin() as conn:
            self._fence(conn, owner, now)
            where = and_(
                self.entries.c.provider_id == self.provider_id,
                self.entries.c.target_key == target.key,
            )
            old = conn.execute(select(self.entries).where(where)).mappings().first()
            same = old is not None and old["coordinate_key"] == target.coordinate_key
            failures = ((old["failures"] if same else 0) + 1) if error else 0
            keep = same and (error is not None or payload is None)
            value = {
                "provider_id": self.provider_id,
                "target_key": target.key,
                "coordinate_key": target.coordinate_key,
                "longitude": target.longitude,
                "latitude": target.latitude,
                "refresh_id": (old["refresh_id"] if same else None) if error else cycle,
                "payload": old["payload"] if keep else payload,
                "result_hash": old["result_hash"]
                if keep
                else (
                    _digest({k: payload.get(k) for k in ("address", "region")})
                    if payload is not None
                    else None
                ),
                "status": "error" if error else "ok" if payload is not None else "not_found",
                "checked_at": now,
                "resolved_at": old["resolved_at"] if keep else now if payload else None,
                "failures": failures,
                "error_code": error,
                "next_refresh_at": (old["next_refresh_at"] if same else None)
                if error
                else six_months_after(now),
                "next_retry_at": now + timedelta(seconds=min(86400, 60 * 2 ** min(failures, 10)))
                if error
                else None,
            }
            if reused_from is not None:
                # 동일 좌표 재사용은 제공자 확인일을 연장하지 않는다.
                for name in ("checked_at", "resolved_at", "next_refresh_at"):
                    value[name] = reused_from[name]
            if old is None:
                conn.execute(insert(self.entries).values(**value))
            else:
                conn.execute(update(self.entries).where(where).values(**value))
            return bool(
                same
                and old["payload"] is not None
                and payload is not None
                and not error
                and old["result_hash"] != value["result_hash"]
            )

    def projections(self, targets: Sequence[AddressTarget]) -> dict[str, dict[str, Any]]:
        if not targets:
            return {}
        expected = {target.key: target.coordinate_key for target in targets}
        result = {}
        with self.engine.connect() as conn:
            for offset in range(0, len(targets), 200):
                keys = [target.key for target in targets[offset : offset + 200]]
                rows = conn.execute(
                    select(self.entries).where(
                        self.entries.c.provider_id == self.provider_id,
                        self.entries.c.target_key.in_(keys),
                    )
                ).mappings()
                for row in rows:
                    if expected.get(row["target_key"]) != row["coordinate_key"]:
                        continue
                    result[row["target_key"]] = {
                        "status": row["status"],
                        "refresh_id": row["refresh_id"],
                        "provider": (row["payload"] or {}).get("provider"),
                        "next_refresh_at": _iso(row["next_refresh_at"]),
                        "stale": row["status"] != "ok"
                        or row["next_refresh_at"] is None
                        or row["next_refresh_at"].replace(
                            tzinfo=row["next_refresh_at"].tzinfo or UTC
                        )
                        <= datetime.now(UTC),
                        "address": (row["payload"] or {}).get("address"),
                        "region": (row["payload"] or {}).get("region"),
                        "checked_at": _iso(row["checked_at"]),
                        "resolved_at": _iso(row["resolved_at"]),
                        "error_code": row["error_code"],
                    }
        return result


def _iso(value: datetime | None) -> str | None:
    if value is None:
        return None
    return value.replace(tzinfo=value.tzinfo or UTC).astimezone(UTC).isoformat()


class DatabaseAddressSource:
    """소비자가 선언한 위치 SELECT를 keyset으로 읽는 공통 연결."""

    def __init__(self, store: ReverseAddressStore, selectable: Any) -> None:
        self.store = store
        self.source = selectable.subquery("address_targets")

    def _target(self, row: Mapping[str, Any]) -> AddressTarget:
        return AddressTarget(
            str(row["target_key"]), float(row["longitude"]), float(row["latitude"])
        )

    def page(self, cursor: str, limit: int) -> list[AddressTarget]:
        with self.store.engine.connect() as conn:
            rows = conn.execute(
                select(self.source)
                .where(
                    self.source.c.target_key > cursor,
                )
                .order_by(self.source.c.target_key)
                .limit(limit)
            ).mappings()
            return [self._target(row) for row in rows]

    def lookup(self, key: str) -> AddressTarget | None:
        with self.store.engine.connect() as conn:
            row = (
                conn.execute(select(self.source).where(self.source.c.target_key == key))
                .mappings()
                .first()
            )
            return self._target(row) if row is not None else None

    def _joined(self) -> Any:
        entries = self.store.entries
        return self.source.outerjoin(
            entries,
            and_(
                entries.c.provider_id == self.store.provider_id,
                entries.c.target_key == self.source.c.target_key,
            ),
        )

    def _due(self, now: datetime) -> Any:
        entries = self.store.entries
        return or_(
            entries.c.target_key.is_(None),
            entries.c.longitude != self.source.c.longitude,
            entries.c.latitude != self.source.c.latitude,
            and_(entries.c.status == "error", entries.c.next_retry_at <= now),
            and_(
                entries.c.status != "error",
                or_(
                    entries.c.next_refresh_at.is_(None),
                    entries.c.next_refresh_at <= now,
                ),
            ),
        )

    def has_work(self, now: datetime | None = None, *, automatic: bool = True) -> bool:
        now = now or datetime.now(UTC)
        with self.store.engine.connect() as conn:
            control = (
                conn.execute(select(self.store.control).where(self.store._control_where()))
                .mappings()
                .first()
            )
            if control is not None and (control["cursor"] or control["force_refresh"]):
                return True
            if not automatic:
                return False
            return (
                conn.execute(
                    select(self.source.c.target_key)
                    .select_from(self._joined())
                    .where(self._due(now))
                    .limit(1)
                ).first()
                is not None
            )

    def summary(self) -> dict[str, Any]:
        entries = self.store.entries
        with self.store.engine.connect() as conn:
            total = conn.execute(select(func.count()).select_from(self.source)).scalar_one()
            due = conn.execute(
                select(func.count()).select_from(self._joined()).where(self._due(datetime.now(UTC)))
            ).scalar_one()
            control = (
                conn.execute(select(self.store.control).where(self.store._control_where()))
                .mappings()
                .first()
            )
            failed = conn.execute(
                select(func.count()).select_from(self._joined()).where(entries.c.status == "error")
            ).scalar_one()
            last = conn.execute(
                select(func.max(entries.c.resolved_at)).where(
                    entries.c.provider_id == self.store.provider_id
                )
            ).scalar_one()
        return {
            "total": total,
            "due": due,
            "failed": failed,
            "last_resolved_at": _iso(last),
            "in_progress": bool(
                control and (control["owner"] or control["cursor"] or control["force_refresh"])
            ),
            "manual_cycle": bool(control and control["force_refresh"]),
            "refresh_months": 6,
            "items": self.sample(),
        }

    def sample(self, limit: int = 50) -> list[dict[str, Any]]:
        entries = self.store.entries
        with self.store.engine.connect() as conn:
            rows = (
                conn.execute(
                    select(self.source)
                    .select_from(self._joined())
                    .where(
                        entries.c.coordinate_key.is_not(None),
                        entries.c.longitude == self.source.c.longitude,
                        entries.c.latitude == self.source.c.latitude,
                    )
                    .order_by(entries.c.checked_at.desc(), self.source.c.target_key)
                    .limit(min(50, max(1, limit)))
                )
                .mappings()
                .all()
            )
        targets = [self._target(row) for row in rows]
        projections = self.store.projections(targets)
        return [
            {
                "target_key": row["target_key"],
                "name": row.get("display_name"),
                **projections[row["target_key"]],
            }
            for row in rows
            if row["target_key"] in projections
        ]


def refresh_reverse_addresses(
    store: ReverseAddressStore,
    client: AddressResolver,
    page: Callable[[str, int], Sequence[AddressTarget]],
    lookup: Callable[[str], AddressTarget | None],
    *,
    batch_size: int = 50,
    budget_seconds: float = 30.0,
    force: bool = False,
    now: Callable[[], datetime] = lambda: datetime.now(UTC),
    clock: Callable[[], float] = time.monotonic,
) -> dict[str, int | str]:
    """부분 완료를 영속화하고 다음 tick에서 남은 위치를 이어 처리한다."""
    if not 1 <= batch_size <= 500 or not 0 < budget_seconds <= 300:
        raise ValueError("배치/시간 예산이 허용 범위를 벗어났습니다.")
    owner = str(uuid4())
    stats: dict[str, int | str] = {
        "status": "success",
        "processed": 0,
        "requests": 0,
        "changed": 0,
        "failed": 0,
        "reused": 0,
        "skipped": 0,
    }
    if not store.claim(owner, now()):
        return {**stats, "status": "busy"}
    deadline = clock() + budget_seconds
    try:
        cursor, cycle, force = store.prepare(owner, force, now())
        retry_keys = store.retries(now(), min(10, batch_size))
        retry_targets = [target for key in retry_keys if (target := lookup(key)) is not None]
        targets = [(target, False) for target in retry_targets]
        targets.extend((target, True) for target in page(cursor, batch_size))
        seen = set()
        for target, advance in targets:
            if clock() >= deadline or int(stats["processed"]) >= batch_size:
                break
            if target.key in seen:
                continue
            seen.add(target.key)
            old = store.row(target.key)
            same = old is not None and old["coordinate_key"] == target.coordinate_key
            verified = (
                same
                and old["status"] in {"ok", "not_found"}
                and (
                    old["refresh_id"] == cycle
                    if force
                    else (
                        old["next_refresh_at"] is not None
                        and old["next_refresh_at"].replace(
                            tzinfo=old["next_refresh_at"].tzinfo or UTC
                        )
                        > now()
                    )
                )
            )
            waiting = (
                same
                and old["next_retry_at"] is not None
                and (
                    old["next_retry_at"].replace(tzinfo=old["next_retry_at"].tzinfo or UTC) > now()
                )
            )
            if verified or waiting:
                stats["skipped"] = int(stats["skipped"]) + 1
            else:
                # HTTP 직전에도 갱신하여 오래된 worker가 새 외부 호출을 시작하지 않게 한다.
                store.advance(owner, cursor, now())
                cached = store.reuse(target, cycle, force, now())
                error = None
                try:
                    if cached is not None:
                        payload = cached["payload"] if cached["status"] == "ok" else None
                        stats["reused"] = int(stats["reused"]) + 1
                    else:
                        stats["requests"] = int(stats["requests"]) + 1
                        payload = client.reverse(target)
                except ReverseAddressError as exc:
                    error, payload = str(exc), None
                    stats["failed"] = int(stats["failed"]) + 1
                changed = store.save(owner, target, cycle, now(), payload, error, cached)
                stats["changed"] = int(stats["changed"]) + int(changed)
            stats["processed"] = int(stats["processed"]) + 1
            if advance:
                cursor = target.key
                store.advance(owner, cursor, now())
        # 끝까지 읽었으면 다음 실행은 신규/실패 위치를 포함해 처음부터 확인한다.
        if not page(cursor, 1):
            store.complete_cycle(owner, now())
        stats["remaining"] = int(bool(page(cursor, 1)))
        if stats["failed"]:
            stats["status"] = "partial_failure"
        return stats
    finally:
        store.release(owner)
