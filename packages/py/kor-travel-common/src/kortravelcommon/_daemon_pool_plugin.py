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
_engines: set[Engine] = set()
_lock = threading.RLock()


class PoolScopeError(RuntimeError):
    """허용된 daemon 수명 밖의 pool 생성을 거절한다."""


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
    """SDK의 명시적 NullPool만 engine 생성 전에 유한 QueuePool로 전환한다."""

    def __init__(self, url, kwargs):
        with _lock:
            if _owner_pid != os.getpid():
                raise PoolScopeError("daemon wrapper에서만 사용할 수 있습니다.")
        if url.drivername != "postgresql+psycopg2" or kwargs.get("poolclass") is not NullPool:
            raise PoolScopeError("지원하는 PostgreSQL NullPool이 아닙니다.")
        if any(key.startswith("pool_") or key == "max_overflow" for key in kwargs):
            raise PoolScopeError("기존 pool 옵션을 덮어쓸 수 없습니다.")
        kwargs.update(
            poolclass=QueuePool,
            pool_size=POOL_SIZE,
            max_overflow=MAX_OVERFLOW,
            pool_timeout=POOL_TIMEOUT,
            pool_recycle=POOL_RECYCLE,
            pool_pre_ping=True,
        )

    def update_url(self, url):
        return url

    def engine_created(self, engine):
        with _lock:
            if _owner_pid != os.getpid() or len(_engines) >= 3:
                engine.dispose()
                raise PoolScopeError("한 daemon instance의 세 engine만 허용합니다.")
            _engines.add(engine)
        event.listen(engine, "connect", _on_connect)
        event.listen(engine, "checkout", _on_checkout)


@contextmanager
def activation() -> Iterator[None]:
    """동일 프로세스 CLI 호출을 감싸고 세 storage의 연결 풀을 정리한다."""
    global _owner_pid
    with _lock:
        if _owner_pid is not None or len(_engines):
            raise PoolScopeError("daemon pool 중첩 실행은 허용하지 않습니다.")
        _owner_pid = os.getpid()
    owner = os.getpid()
    try:
        yield
    finally:
        original_error = sys.exception()
        with _lock:
            _owner_pid = None
            engines = list(_engines)
            _engines.clear()
        problem = False
        if os.getpid() != owner:
            # fork된 자식에서 부모 연결의 close/rollback도 하지 않는다.
            problem = True
        else:
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
