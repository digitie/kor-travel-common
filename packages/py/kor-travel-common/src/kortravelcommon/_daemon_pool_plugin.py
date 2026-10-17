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
POOL_SIZE = 2
MAX_OVERFLOW = 2
POOL_TIMEOUT = 1
POOL_RECYCLE = 3600

_owner_pid: int | None = None
_scope: object | None = None
_engines: set[Engine] = set()
_primary_slots = 0
_lock = threading.RLock()
_lock_pid = os.getpid()


class PoolScopeError(RuntimeError):
    """허용된 daemon 수명 밖의 pool 생성을 거절한다."""


def _check_process():
    if os.getpid() != _lock_pid:
        raise PoolScopeError("fork로 상속한 daemon pool은 사용할 수 없습니다.")


class DaemonQueuePool(QueuePool):
    """대여와 세대 교체를 직렬화하고 부모·퇴역 pool 접근을 거절한다."""

    def __init__(self, *args, **kwargs):
        self._creator_pid = os.getpid()
        self._pool_scope = _scope
        self._lifecycle_lock = threading.RLock()
        self._retired = False
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
            return super().connect()

    def dispose(self):
        self._check_creator()
        with self._lifecycle_lock:
            if self.checkedout():
                raise PoolScopeError("대여 중인 pool은 닫을 수 없습니다.")
            return super().dispose()

    def recreate(self):
        self._check_creator()
        with self._lifecycle_lock:
            if self.checkedout() or self.checkedin() or self._retired:
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
            # engine_created보다 먼저 예약하여 동시 생성도 primary 세 개로 제한한다.
            # 생성 실패의 예약은 해당 activation 종료까지 유지한다.
            self._primary = _primary_slots < 3
            if self._primary:
                _primary_slots += 1
        if self._primary:
            kwargs.update(
                poolclass=DaemonQueuePool,
                pool_size=POOL_SIZE,
                max_overflow=MAX_OVERFLOW,
                pool_timeout=POOL_TIMEOUT,
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
def activation() -> Iterator[None]:
    """동일 프로세스 CLI 호출을 감싸고 세 storage의 연결 풀을 정리한다."""
    global _owner_pid, _scope, _primary_slots
    _check_process()
    with _lock:
        if _owner_pid is not None or len(_engines) or _primary_slots:
            raise PoolScopeError("daemon pool 중첩 실행은 허용하지 않습니다.")
        _owner_pid = os.getpid()
        _scope = object()
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
