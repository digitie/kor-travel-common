# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"""명시적으로 활성화한 daemon 프로세스의 PostgreSQL engine만 재사용한다."""

from __future__ import annotations

import os
import sys
import threading
from collections.abc import Iterator
from contextlib import contextmanager

from sqlalchemy import event, exc
from sqlalchemy.engine import CreateEnginePlugin, Engine
from sqlalchemy.pool import NullPool, QueuePool

PLUGIN_NAME = "kortravel_daemon_pool"
# daemon은 schedule·sensor worker(각 4)와 queue·monitoring·backfill thread가 세 storage를
# 함께 쓴다. 2+2에서는 기동 뒤 몇 시간 동안 pool 부족 경고와 tick 실패가 났다
# (2026-11-23 수집 실패 감사). 기본 primary 상한은 3×(4+4)=24 연결이다.
# 대기는 잠금 밖에서 하므로(DaemonQueuePool.connect) 동시 대기자가 서로 직렬화되지 않고
# 각자 timeout만큼만 기다린다. 소비자는 activation 인자(daemon wrapper는 env)로 바꾼다.
POOL_SIZE = 4
MAX_OVERFLOW = 4
POOL_TIMEOUT = 10
POOL_RECYCLE = 3600
# 설정 허용 범위(양 끝 포함). 상한은 공유 PG 접속 예산을 지키려는 것이다(최대 3×(16+16)=96).
POOL_SIZE_RANGE = (1, 16)
MAX_OVERFLOW_RANGE = (0, 16)
POOL_TIMEOUT_RANGE = (1, 60)

_owner_pid: int | None = None
_scope: object | None = None
_settings: tuple[int, int, int] | None = None
_engines: set[Engine] = set()
_primary_slots = 0
_lock = threading.RLock()
_lock_pid = os.getpid()


class PoolScopeError(RuntimeError):
    """허용된 daemon 수명 밖의 pool 생성을 거절한다."""


def validate_settings(
    pool_size: int = POOL_SIZE,
    max_overflow: int = MAX_OVERFLOW,
    pool_timeout: int = POOL_TIMEOUT,
) -> tuple[int, int, int]:
    """정수가 아니거나 허용 범위 밖인 값은 값을 싣지 않은 ValueError로 거절한다."""
    for value, (low, high) in (
        (pool_size, POOL_SIZE_RANGE),
        (max_overflow, MAX_OVERFLOW_RANGE),
        (pool_timeout, POOL_TIMEOUT_RANGE),
    ):
        if type(value) is not int or not low <= value <= high:
            raise ValueError("daemon pool 크기·대기 설정이 허용 범위 밖입니다.")
    return pool_size, max_overflow, pool_timeout


def _check_process():
    if os.getpid() != _lock_pid:
        raise PoolScopeError("fork로 상속한 daemon pool은 사용할 수 없습니다.")


class DaemonQueuePool(QueuePool):
    """세대 교체와 대여 시작을 직렬화하고 부모·퇴역 pool 접근을 거절한다.

    수명 잠금은 scope 검사와 진행 중 대여 수(``_inflight``) 증감만 감싼다. 실제 대기·연결
    생성·pre-ping은 잠금 밖의 원 QueuePool이 하므로 동시 대기자는 서로를 기다리지 않는다
    (이전에는 잠금 안에서 대기해 N번째 대기자가 N×timeout을 기다렸다). 연결 상한은 원
    QueuePool의 overflow 계수가 지킨다. dispose/recreate는 진행 중 대여도 대여 중으로 보고
    거절한다. 대여가 끝나 ``checkedout()``에 잡힌 뒤에야 ``_inflight``를 줄이므로 두 계수
    사이에 빈틈이 없다.
    """

    def __init__(self, *args, **kwargs):
        self._creator_pid = os.getpid()
        self._pool_scope = _scope
        self._lifecycle_lock = threading.RLock()
        self._retired = False
        self._inflight = 0
        super().__init__(*args, **kwargs)

    def _check_creator(self):
        if self._creator_pid != os.getpid():
            raise PoolScopeError("다른 프로세스의 daemon pool입니다.")

    def connect(self):
        self._check_creator()
        with self._lifecycle_lock:
            if (
                _owner_pid != os.getpid()
                or self._pool_scope is None
                or self._pool_scope is not _scope
                or self._retired
            ):
                raise PoolScopeError("다른 수명 또는 퇴역한 daemon pool입니다.")
            self._inflight += 1
        try:
            return super().connect()
        finally:
            with self._lifecycle_lock:
                self._inflight -= 1

    def _busy(self):
        return bool(self._inflight or self.checkedout())

    def dispose(self):
        self._check_creator()
        with self._lifecycle_lock:
            if self._busy():
                raise PoolScopeError("대여 중인 pool은 닫을 수 없습니다.")
            return super().dispose()

    def recreate(self):
        self._check_creator()
        with self._lifecycle_lock:
            if self._busy() or self.checkedin() or self._retired:
                raise PoolScopeError("비어 있지 않거나 퇴역한 pool은 재생성할 수 없습니다.")
            replacement = super().recreate()
            replacement._pool_scope = self._pool_scope
            self._retired = True
            return replacement


def _on_connect(connection, record):
    record.info["kortravel_pid"] = os.getpid()


def _on_checkout(connection, record, proxy):
    if _owner_pid != os.getpid():
        raise PoolScopeError("daemon pool 활성 범위가 아닙니다.")
    if record.info.get("kortravel_pid") != os.getpid():
        # SQLAlchemy 공식 multiprocessing recipe: 부모의 socket을 재사용하지 않는다.
        record.dbapi_connection = proxy.dbapi_connection = None
        raise exc.DisconnectionError("다른 프로세스의 연결은 재사용할 수 없습니다.")


class DaemonPoolPlugin(CreateEnginePlugin):
    """최초 세 storage만 풀링하고 SDK의 임시 instance는 NullPool을 유지한다."""

    def __init__(self, url, kwargs):
        global _primary_slots
        _check_process()
        if url.drivername != "postgresql+psycopg2" or kwargs.get("poolclass") is not NullPool:
            raise PoolScopeError("지원하는 PostgreSQL NullPool이 아닙니다.")
        if any(key.startswith("pool_") or key == "max_overflow" for key in kwargs):
            raise PoolScopeError("기존 pool 옵션을 덮어쓸 수 없습니다.")
        with _lock:
            if _owner_pid != os.getpid():
                raise PoolScopeError("daemon wrapper에서만 사용할 수 있습니다.")
            self._activation_scope = _scope
            settings = _settings
            # engine_created보다 먼저 예약하여 동시 생성도 primary 세 개로 제한한다.
            # 생성 실패의 예약은 해당 activation 종료까지 유지한다.
            self._primary = _primary_slots < 3
            if self._primary:
                _primary_slots += 1
        if self._primary:
            pool_size, max_overflow, pool_timeout = settings
            kwargs.update(
                poolclass=DaemonQueuePool,
                pool_size=pool_size,
                max_overflow=max_overflow,
                pool_timeout=pool_timeout,
                pool_recycle=POOL_RECYCLE,
                pool_pre_ping=True,
            )

    def update_url(self, url):
        return url

    def engine_created(self, engine):
        _check_process()
        with _lock:
            if _owner_pid != os.getpid() or self._activation_scope is not _scope:
                engine.dispose()
                raise PoolScopeError("engine 생성 중 daemon 활성 수명이 변경되었습니다.")
            if not self._primary:
                return
            if len(_engines) >= 3:
                engine.dispose()
                raise PoolScopeError("primary pooled engine 상한을 초과했습니다.")
            _engines.add(engine)
        event.listen(engine, "connect", _on_connect)
        event.listen(engine, "checkout", _on_checkout)


@contextmanager
def activation(
    *,
    pool_size: int = POOL_SIZE,
    max_overflow: int = MAX_OVERFLOW,
    pool_timeout: int = POOL_TIMEOUT,
) -> Iterator[None]:
    """동일 프로세스 CLI 호출을 감싸고 세 storage의 연결 풀을 정리한다.

    크기·대기는 이 수명에서 새로 만드는 primary engine에만 적용된다. 범위 밖 값은
    수명을 열기 전에 ValueError로 거절한다.
    """
    global _owner_pid, _scope, _primary_slots, _settings
    _check_process()
    settings = validate_settings(pool_size, max_overflow, pool_timeout)
    with _lock:
        if _owner_pid is not None or len(_engines) or _primary_slots:
            raise PoolScopeError("daemon pool 중첩 실행은 허용하지 않습니다.")
        _owner_pid = os.getpid()
        _scope = object()
        _settings = settings
    owner = os.getpid()
    try:
        yield
    finally:
        original_error = sys.exception()
        problem = False
        if os.getpid() != owner:
            # 상속된 잠금과 부모 연결에 접근하기 전에 자식 종료를 거절한다.
            problem = True
        else:
            with _lock:
                _owner_pid = None
                _scope = None
                _settings = None
                _primary_slots = 0
                engines = list(_engines)
                _engines.clear()
            for engine in engines:
                try:
                    problem = bool(engine.pool.checkedout()) or problem
                    engine.dispose()
                except Exception:
                    problem = True
        if problem:
            if original_error is not None and not (
                isinstance(original_error, SystemExit) and original_error.code in (None, 0)
            ):
                print("daemon 연결 풀 정리가 완료되지 않았습니다.", file=sys.stderr)
            else:
                raise PoolScopeError("daemon 연결 풀 정리가 완료되지 않았습니다.")
