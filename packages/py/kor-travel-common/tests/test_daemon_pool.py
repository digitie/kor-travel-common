# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"""가짜 DBAPI와 lazy engine으로 SDK/DB 연결 없이 수명·상한을 검증한다."""

import os
import sys
import types

import pytest
from sqlalchemy import create_engine, exc
from sqlalchemy.dialects import plugins
from sqlalchemy.engine import make_url
from sqlalchemy.pool import NullPool, QueuePool

from kortravelcommon import _daemon_pool_plugin as pool
from kortravelcommon import daemon_pool as cli

# 연결하지 않는 가짜 credential을 URL 구조 API로 넣어 원 옵션 보존만 검사한다.
URL = make_url(
    "postgresql+psycopg2://127.0.0.1:1/fixture?connect_timeout=3&options=-cstatement_timeout%3D5000%20-clock_timeout%3D1000"
).set(username="fixture", password="<fixture>").render_as_string(hide_password=False)


@pytest.fixture(autouse=True)
def clean_scope():
    assert pool._owner_pid is None and not pool._engines and pool._primary_slots == 0
    assert pool._settings is None
    yield
    assert pool._owner_pid is None and not pool._engines and pool._primary_slots == 0
    assert pool._settings is None


def engine():
    # 실제 연결을 시도하면 반드시 실패한다. create_engine 자체는 lazy다.
    def forbidden():
        raise AssertionError("실제 DB 연결 금지")

    return create_engine(
        cli._pooled_url(URL, URL), poolclass=NullPool,
        isolation_level="AUTOCOMMIT", creator=forbidden,
    )


@pytest.fixture
def registered():
    # 배포판 entry point와 동일한 SQLAlchemy 공식 등록 API만 사용한다.
    plugins.register(pool.PLUGIN_NAME, pool.__name__, "DaemonPoolPlugin")


def test_plugin_preserves_options_and_lazy_three_engine_lifecycle(registered):
    with pool.activation():
        engines = [engine() for _ in range(3)]
        for item in engines:
            assert isinstance(item.pool, QueuePool)
            assert item.pool._pre_ping is True
            assert item.pool.size() == 4 and item.pool._max_overflow == 4
            assert item.pool.timeout() == 10 and item.pool._recycle == 3600
            assert item.url == make_url(URL)
            assert item.get_execution_options() == {}
        first_pool = engines[0].pool
        engines[0].dispose()
        assert engines[0].pool is not first_pool
        temporary = engine()
        assert type(temporary.pool) is NullPool
        assert set(engines) == pool._engines
        assert pool._primary_slots == 3
        temporary.dispose()
    assert all(item.pool.checkedout() == 0 for item in engines)


@pytest.mark.parametrize("kwargs", [
    {}, {"poolclass": QueuePool}, {"poolclass": NullPool, "pool_timeout": 3},
])
def test_only_explicit_nullpool_and_no_existing_pool_options(kwargs):
    with pool.activation(), pytest.raises(pool.PoolScopeError):
        pool.DaemonPoolPlugin(make_url(URL), kwargs)


def test_plugin_inactive_wrong_driver_and_nested_scope():
    with pytest.raises(pool.PoolScopeError):
        pool.DaemonPoolPlugin(make_url(URL), {"poolclass": NullPool})
    with pool.activation():
        with pytest.raises(pool.PoolScopeError):
            pool.DaemonPoolPlugin(make_url("sqlite://"), {"poolclass": NullPool})
        with pytest.raises(pool.PoolScopeError):
            with pool.activation():
                pass


def test_fake_dbapi_reuse_cap_and_dispose():
    created = []
    class Connection:
        def __init__(self):
            self.closed = False
            created.append(self)
        def rollback(self):
            pass
        def close(self):
            self.closed = True

    null = NullPool(Connection)
    for _ in range(40):
        connection = null.connect()
        connection.close()
    assert len(created) == 40 and all(row.closed for row in created)
    created.clear()
    bounded = QueuePool(Connection, pool_size=2, max_overflow=2, timeout=1, recycle=3600)
    for _ in range(40):
        connection = bounded.connect()
        connection.close()
    assert len(created) == 1 and not created[0].closed
    held = [bounded.connect() for _ in range(4)]
    assert len(created) == 4
    with pytest.raises(exc.TimeoutError):
        bounded.connect()
    for connection in held:
        connection.close()
    bounded.dispose()
    assert all(row.closed for row in created)


def test_pid_scope_and_sqlalchemy_invalid_record_recipe(monkeypatch):
    record = types.SimpleNamespace(info={}, dbapi_connection=object())
    proxy = types.SimpleNamespace(dbapi_connection=object())
    with pool.activation():
        pool._on_connect(None, record)
        pool._on_checkout(None, record, proxy)
        record.info["kortravel_pid"] = -1
        with pytest.raises(exc.DisconnectionError):
            pool._on_checkout(None, record, proxy)
        assert record.dbapi_connection is None and proxy.dbapi_connection is None
        monkeypatch.setattr(pool, "os", types.SimpleNamespace(getpid=lambda: os.getpid() + 1))
        with pytest.raises(pool.PoolScopeError):
            pool._on_checkout(None, record, proxy)
        monkeypatch.undo()


def test_busy_cleanup_preserves_original_failure_and_disposes_all(monkeypatch, capsys):
    calls = []
    class Fake:
        pool = types.SimpleNamespace(checkedout=lambda: 1)
        def dispose(self):
            calls.append("dispose")
    fake = Fake()
    with pytest.raises(SystemExit) as caught:
        with pool.activation():
            pool._engines.add(fake)
            raise SystemExit(7)
    assert caught.value.code == 7 and calls == ["dispose"]
    assert "정리가 완료되지" in capsys.readouterr().err
    with pytest.raises(pool.PoolScopeError):
        with pool.activation():
            pool._engines.add(fake)


@pytest.mark.parametrize("bad", [None, URL + "&plugin=other", URL.replace("psycopg2", "psycopg")])
def test_url_rejects_missing_existing_plugin_or_wrong_driver(bad):
    with pytest.raises(cli.DaemonPoolConfigurationError):
        cli._pooled_url(bad, bad)
    with pytest.raises(cli.DaemonPoolConfigurationError):
        cli._pooled_url(URL, URL + "&other=1")


def config(tmp_path, monkeypatch):
    monkeypatch.setenv("DAGSTER_HOME", str(tmp_path))
    path = tmp_path / "dagster.yaml"
    path.write_text(
        "storage:\n  postgres:\n    postgres_url:\n"
        "      env: KOR_TRAVEL_DAGSTER_SHARED_PG_URL\n    should_autocreate_tables: false\n"
    )
    return path


def test_wrapper_same_process_argv_environment_and_original_exception(tmp_path, monkeypatch):
    config(tmp_path, monkeypatch)
    monkeypatch.setenv(cli.SHARED_URL_ENV, URL)
    monkeypatch.setenv(cli.DAEMON_URL_ENV, URL)
    monkeypatch.setattr(sys, "argv", ["own-wrapper", "run", "-w", "same-workspace"])
    before = dict(os.environ)
    observed = []
    def original():
        observed.append((os.getpid(), list(sys.argv)))
        assert make_url(os.environ[cli.SHARED_URL_ENV]).query["plugin"] == pool.PLUGIN_NAME
        raise SystemExit(9)
    monkeypatch.setattr(cli, "_original_cli", lambda: original)
    with pytest.raises(SystemExit) as caught:
        cli.run()
    assert caught.value.code == 9
    assert observed == [(os.getpid(), ["own-wrapper", "run", "-w", "same-workspace"])]
    assert dict(os.environ) == before


def test_config_requires_unresolved_env_and_existing_migrated_schema(tmp_path, monkeypatch):
    path = config(tmp_path, monkeypatch)
    cli._validate_storage_config()
    original = path.read_text()
    for bad in [
        original.replace("env: KOR_TRAVEL_DAGSTER_SHARED_PG_URL", "env: OTHER"),
        original.replace("false", "true"),
        "storage:\n  postgres:\n    postgres_url: literal\n    should_autocreate_tables: false\n",
    ]:
        path.write_text(bad)
        with pytest.raises(cli.DaemonPoolConfigurationError):
            cli._validate_storage_config()


def test_official_loader_versions_and_entrypoint_are_pinned(monkeypatch):
    seen = []
    item = types.SimpleNamespace(
        group="console_scripts", name="dagster-daemon", value="dagster._daemon.cli:main",
        load=lambda: seen.append("loaded"),
    )
    monkeypatch.setattr(cli.importlib.metadata, "version", lambda name: cli.EXPECTED_VERSIONS[name])
    monkeypatch.setattr(cli.importlib.metadata, "distribution",
                        lambda name: types.SimpleNamespace(entry_points=[item]))
    cli._original_cli()
    assert seen == ["loaded"]
    monkeypatch.setattr(cli.importlib.metadata, "version", lambda name: "0")
    with pytest.raises(cli.DaemonPoolConfigurationError):
        cli._original_cli()


def test_help_delegation_does_not_require_dsn(monkeypatch):
    called = []
    monkeypatch.setattr(cli, "_original_cli", lambda: lambda: called.append("official"))
    monkeypatch.setattr(sys, "argv", ["own-wrapper", "run", "--help"])
    monkeypatch.setattr(cli, "_validate_storage_config", lambda: None)
    # 원 run --help도 run 활성화 경로이므로 실제 DSN 요구는 명시한다.
    monkeypatch.delenv(cli.SHARED_URL_ENV, raising=False)
    monkeypatch.delenv(cli.DAEMON_URL_ENV, raising=False)
    monkeypatch.setattr(sys, "argv", ["own-wrapper", "--help"])
    cli.run()
    assert called == ["official"]


@pytest.mark.parametrize("arguments", [
    ["run", "--instance-ref", "synthetic-no-secret"],
    ["run", "--instance-ref=synthetic-no-secret"],
])
def test_hidden_instance_ref_cannot_bypass_environment_contract(monkeypatch, arguments):
    monkeypatch.setattr(cli, "_original_cli", lambda: lambda: pytest.fail("위임하면 안 됨"))
    monkeypatch.setattr(sys, "argv", ["own-wrapper", *arguments])
    with pytest.raises(cli.DaemonPoolConfigurationError):
        cli.run()


def test_pre_ping_replaces_dead_idle_fake_connection_before_return():
    from sqlalchemy.engine.default import DefaultDialect

    created = []
    pinged = []
    class Connection:
        alive = True
        def __init__(self):
            created.append(self)
        def rollback(self):
            pass
        def close(self):
            self.alive = False
    class Dialect(DefaultDialect):
        def do_ping(self, connection):
            pinged.append(connection)
            return connection.alive
    queue = QueuePool(Connection, pool_size=2, max_overflow=2, timeout=1,
                      recycle=3600, pre_ping=True, dialect=Dialect())
    first = queue.connect()
    first_record = first.dbapi_connection
    first.close()
    first_record.alive = False
    second = queue.connect()
    assert second.dbapi_connection is not first_record
    assert second.dbapi_connection.alive
    assert len(created) == 2 and pinged == [first_record]
    second.close()
    queue.dispose()


def test_fork_scope_rejected_before_ping_or_parent_connection_close(monkeypatch):
    from sqlalchemy import event
    from sqlalchemy.engine.default import DefaultDialect

    pid = [100]
    monkeypatch.setattr(pool, "_lock_pid", 100)
    events = []
    monkeypatch.setattr(pool, "os", types.SimpleNamespace(getpid=lambda: pid[0]))
    class Connection:
        def rollback(self):
            events.append(("rollback", pid[0]))
        def close(self):
            events.append(("close", pid[0]))
    class Dialect(DefaultDialect):
        def do_ping(self, connection):
            events.append(("ping", pid[0]))
            return True

    with pool.activation():
        # 원 후보에는 subclass가 없으므로 실제 QueuePool의 선행 ping 반례가 RED다.
        pool_class = getattr(pool, "DaemonQueuePool", QueuePool)
        queue = pool_class(Connection, pool_size=2, max_overflow=2, timeout=1,
                           pre_ping=True, dialect=Dialect())
        event.listen(queue, "connect", pool._on_connect)
        event.listen(queue, "checkout", pool._on_checkout)
        first = queue.connect()
        first.close()
        events.clear()
        pid[0] = 200
        try:
            with pytest.raises(pool.PoolScopeError):
                queue.connect()
            assert events == []
        finally:
            pid[0] = 100
            queue.dispose()


def test_recreated_pool_preserves_early_scope_guard(registered, monkeypatch):
    with pool.activation():
        item = engine()
        item.dispose()
        assert type(item.pool).__name__ == "DaemonQueuePool"
        monkeypatch.setattr(pool, "os", types.SimpleNamespace(getpid=lambda: os.getpid() + 1))
        try:
            with pytest.raises(pool.PoolScopeError):
                item.pool.connect()
        finally:
            monkeypatch.undo()


def test_busy_engine_dispose_cannot_retire_live_pool_generations(registered):
    from sqlalchemy.engine import Engine
    from sqlalchemy.engine.default import DefaultDialect

    opened = []
    class Connection:
        closed = False
        def __init__(self):
            opened.append(self)
        def rollback(self):
            pass
        def close(self):
            self.closed = True

    held = []
    with pool.activation():
        for _ in range(3):
            queue = pool.DaemonQueuePool(
                Connection, pool_size=2, max_overflow=2, timeout=1, dialect=DefaultDialect()
            )
            item = Engine(queue, DefaultDialect(), make_url(URL))
            plugin = pool.DaemonPoolPlugin(make_url(URL), {"poolclass": NullPool})
            plugin.engine_created(item)
            held.extend(item.raw_connection() for _ in range(4))
            with pytest.raises(pool.PoolScopeError):
                item.dispose()
            with pytest.raises(pool.PoolScopeError):
                item.dispose(close=False)
            assert item.pool is queue
        assert len(opened) == 12 and all(not row.closed for row in opened)
        for connection in held:
            connection.close()
    assert all(row.closed for row in opened)


def test_close_false_with_idle_pool_rejects_but_default_dispose_works(registered):
    from sqlalchemy.engine import Engine
    from sqlalchemy.engine.default import DefaultDialect

    class Connection:
        def rollback(self):
            pass
        def close(self):
            pass
    with pool.activation():
        queue = pool.DaemonQueuePool(Connection, pool_size=2, max_overflow=2)
        item = Engine(queue, DefaultDialect(), make_url(URL))
        plugin = pool.DaemonPoolPlugin(make_url(URL), {"poolclass": NullPool})
        plugin.engine_created(item)
        conn = item.raw_connection()
        conn.close()
        with pytest.raises(pool.PoolScopeError):
            item.dispose(close=False)
        assert item.pool is queue and queue.checkedin() == 1
        item.dispose()
        assert item.pool is not queue and item.pool.checkedin() == 0


def test_old_scope_cannot_reactivate_old_or_finally_recreated_pool(registered):
    with pool.activation():
        old = engine()
        first_pool = old.pool
    after_scope_pool = old.pool
    with pool.activation():
        old.dispose()
        for stale in (first_pool, after_scope_pool, old.pool):
            with pytest.raises(pool.PoolScopeError):
                stale.connect()


def test_child_dispose_and_recreate_cannot_close_parent_pool(monkeypatch):
    from sqlalchemy.engine.default import DefaultDialect

    pid = [100]
    monkeypatch.setattr(pool, "_lock_pid", 100)
    calls = []
    monkeypatch.setattr(pool, "os", types.SimpleNamespace(getpid=lambda: pid[0]))
    class Connection:
        def rollback(self):
            pass
        def close(self):
            calls.append("closed")
    with pool.activation():
        queue = pool.DaemonQueuePool(
            Connection, pool_size=2, max_overflow=2, dialect=DefaultDialect()
        )
        conn = queue.connect()
        conn.close()
        pid[0] = 200
        try:
            with pytest.raises(pool.PoolScopeError):
                queue.dispose()
            with pytest.raises(pool.PoolScopeError):
                queue.recreate()
            assert calls == []
        finally:
            pid[0] = 100
            queue.dispose()


def test_retired_pool_reference_cannot_connect_after_recreate(registered):
    with pool.activation():
        item = engine()
        retired = item.pool
        item.dispose()
        assert item.pool is not retired
        with pytest.raises(pool.PoolScopeError):
            retired.connect()


def test_dispose_check_and_close_serialize_with_checkout(monkeypatch):
    import threading

    from sqlalchemy.engine.default import DefaultDialect

    checked = threading.Event()
    release = threading.Event()
    attempted = threading.Event()
    created = threading.Event()
    errors = []
    connections = []
    class Connection:
        def __init__(self):
            created.set()
        def rollback(self):
            pass
        def close(self):
            pass
    with pool.activation():
        queue = pool.DaemonQueuePool(Connection, pool_size=2, max_overflow=2,
                                     dialect=DefaultDialect())
        original = queue.checkedout
        def gated_checkedout():
            result = original()
            checked.set()
            assert release.wait(2)
            return result
        monkeypatch.setattr(queue, "checkedout", gated_checkedout)
        def dispose():
            try:
                queue.dispose()
            except BaseException as error:
                errors.append(error)
        def borrow():
            attempted.set()
            try:
                connections.append(queue.connect())
            except BaseException as error:
                errors.append(error)
        first = threading.Thread(target=dispose)
        second = threading.Thread(target=borrow)
        first.start()
        try:
            assert checked.wait(2)
            second.start()
            assert attempted.wait(2)
            assert not created.wait(0.05)
        finally:
            release.set()
            first.join(2)
            if second.ident is not None:
                second.join(2)
            for connection in connections:
                connection.close()
            monkeypatch.setattr(queue, "checkedout", original)
            queue.dispose()
        assert not first.is_alive() and not second.is_alive() and errors == []


def test_waiting_checkout_can_be_unblocked_by_connection_return():
    import threading

    from sqlalchemy.engine.default import DefaultDialect

    class Connection:
        def rollback(self):
            pass
        def close(self):
            pass
    with pool.activation():
        queue = pool.DaemonQueuePool(Connection, pool_size=2, max_overflow=2,
                                     timeout=1, dialect=DefaultDialect())
        held = [queue.connect() for _ in range(4)]
        waiting = threading.Event()
        acquired = []
        errors = []
        def borrow():
            waiting.set()
            try:
                acquired.append(queue.connect())
            except BaseException as error:
                errors.append(error)
        thread = threading.Thread(target=borrow)
        thread.start()
        try:
            assert waiting.wait(2)
            held.pop().close()
            thread.join(2)
            assert not thread.is_alive() and errors == [] and len(acquired) == 1
        finally:
            for connection in held + acquired:
                connection.close()
            queue.dispose()


def test_fork_global_entrypoints_reject_before_inherited_lock(monkeypatch):
    class PoisonLock:
        def __enter__(self):
            raise AssertionError("inherited lock entered")
        def __exit__(self, *args):
            pass
    with pool.activation():
        plugin = pool.DaemonPoolPlugin(make_url(URL), {"poolclass": NullPool})
        with monkeypatch.context() as child:
            child.setattr(pool, "_lock", PoisonLock())
            child.setattr(pool, "os", types.SimpleNamespace(getpid=lambda: os.getpid() + 1))
            with pytest.raises(pool.PoolScopeError):
                pool.DaemonPoolPlugin(make_url(URL), {"poolclass": NullPool})
            with pytest.raises(pool.PoolScopeError):
                plugin.engine_created(types.SimpleNamespace(dispose=lambda: pytest.fail("I/O")))
            with pytest.raises(pool.PoolScopeError):
                with pool.activation():
                    pytest.fail("entered child scope")


def test_fork_activation_exit_rejects_before_inherited_lock(monkeypatch):
    class PoisonLock:
        def __enter__(self):
            raise AssertionError("inherited lock entered")
        def __exit__(self, *args):
            pass
    manager = pool.activation()
    manager.__enter__()
    try:
        with monkeypatch.context() as child:
            child.setattr(pool, "_lock", PoisonLock())
            child.setattr(pool, "os", types.SimpleNamespace(getpid=lambda: os.getpid() + 1))
            with pytest.raises(pool.PoolScopeError):
                manager.__exit__(None, None, None)
    finally:
        # 모형 자식은 별도 주소 공간이 아니므로 부모의 빈 활성 상태만 복원한다.
        pool._owner_pid = None
        pool._scope = None
        pool._settings = None
        pool._primary_slots = 0


def test_fork_pool_methods_reject_before_inherited_pool_lock(monkeypatch):
    class PoisonLock:
        def __enter__(self):
            raise AssertionError("inherited pool lock entered")
        def __exit__(self, *args):
            pass
    with pool.activation():
        queue = pool.DaemonQueuePool(lambda: pytest.fail("I/O"))
        with monkeypatch.context() as child:
            child.setattr(queue, "_lifecycle_lock", PoisonLock())
            child.setattr(pool, "os", types.SimpleNamespace(getpid=lambda: os.getpid() + 1))
            for operation in (queue.connect, queue.dispose, queue.recreate):
                with pytest.raises(pool.PoolScopeError):
                    operation()
        queue.dispose()


def test_temporary_sdk_instances_keep_nullpool_and_close_on_success_and_error(registered):
    from sqlalchemy.engine import Engine
    from sqlalchemy.engine.default import DefaultDialect

    opened = []
    class Connection:
        def __init__(self):
            self.closed = False
            opened.append(self)
        def rollback(self):
            pass
        def close(self):
            self.closed = True

    with pool.activation():
        primary = [engine() for _ in range(3)]
        for fail in (False, True, False):
            temporary = []
            try:
                for _ in range(3):
                    kwargs = {"poolclass": NullPool}
                    plugin = pool.DaemonPoolPlugin(make_url(URL), kwargs)
                    assert kwargs == {"poolclass": NullPool}
                    item = Engine(NullPool(Connection), DefaultDialect(), make_url(URL))
                    plugin.engine_created(item)
                    temporary.append(item)
                    with item.connect():
                        pass
                    assert opened[-1].closed
                if fail:
                    raise RuntimeError("가짜 RPC 실패")
            except RuntimeError:
                assert fail
            finally:
                for item in temporary:
                    item.dispose()
            assert pool._engines == set(primary) and pool._primary_slots == 3
        assert len(opened) == 9 and all(row.closed for row in opened)
    assert pool._primary_slots == 0


def test_parallel_engine_constructors_reserve_only_three_primary_slots():
    from concurrent.futures import ThreadPoolExecutor

    def construct(_):
        kwargs = {"poolclass": NullPool}
        plugin = pool.DaemonPoolPlugin(make_url(URL), kwargs)
        return plugin, kwargs
    with pool.activation():
        with ThreadPoolExecutor(max_workers=8) as executor:
            rows = list(executor.map(construct, range(12)))
        assert sum(kwargs["poolclass"] is pool.DaemonQueuePool for _, kwargs in rows) == 3
        assert sum(kwargs == {"poolclass": NullPool} for _, kwargs in rows) == 9
        assert pool._primary_slots == 3


def test_failed_primary_construction_does_not_allow_unbounded_pool_replacement():
    with pool.activation():
        for _ in range(3):
            pool.DaemonPoolPlugin(make_url(URL), {"poolclass": NullPool})
        kwargs = {"poolclass": NullPool}
        pool.DaemonPoolPlugin(make_url(URL), kwargs)
        assert kwargs == {"poolclass": NullPool}
    with pool.activation():
        kwargs = {"poolclass": NullPool}
        pool.DaemonPoolPlugin(make_url(URL), kwargs)
        assert kwargs["poolclass"] is pool.DaemonQueuePool


def test_delayed_temporary_engine_registration_rejects_changed_scope(registered):
    from sqlalchemy.engine import Engine
    from sqlalchemy.engine.default import DefaultDialect

    with pool.activation():
        for _ in range(3):
            engine()
        plugin = pool.DaemonPoolPlugin(make_url(URL), {"poolclass": NullPool})
    with pool.activation():
        item = Engine(NullPool(lambda: pytest.fail("I/O")), DefaultDialect(), make_url(URL))
        with pytest.raises(pool.PoolScopeError):
            plugin.engine_created(item)


# ── 잠금 밖 대기(2026-11-24) ────────────────────────────────────────────────
# 이전 DaemonQueuePool.connect는 수명 잠금을 쥔 채 원 QueuePool에서 대기해, 동시 대기자가
# 잠금 순서대로 한 명씩 timeout을 다 쓰고 나왔다(N번째는 N×timeout). 아래 시험은 그 직렬화와
# 그것을 없앤 뒤의 상한·반환·예외 누수를 가짜 DBAPI로 본다. 실제 DB 연결은 하지 않는다.


class _Counted:
    """생성·종료를 세는 가짜 DBAPI 연결."""

    def __init__(self, ledger):
        self.ledger = ledger
        self.closed = False
        with ledger["lock"]:
            ledger["created"] += 1
            ledger["live"] += 1
            ledger["peak_live"] = max(ledger["peak_live"], ledger["live"])

    def rollback(self):
        pass

    def close(self):
        if not self.closed:
            self.closed = True
            with self.ledger["lock"]:
                self.ledger["live"] -= 1


def _ledger():
    import threading

    return {"lock": threading.Lock(), "created": 0, "live": 0, "peak_live": 0}


def _queue(ledger, **kwargs):
    from sqlalchemy.engine.default import DefaultDialect

    return pool.DaemonQueuePool(lambda: _Counted(ledger), dialect=DefaultDialect(), **kwargs)


def _wait_until(predicate, seconds=5.0):
    import time

    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        if predicate():
            return True
        time.sleep(0.005)
    return predicate()


def test_concurrent_waiters_time_out_in_parallel_not_serially():
    import threading
    import time

    ledger = _ledger()
    waiters = 8
    with pool.activation():
        queue = _queue(ledger, pool_size=1, max_overflow=0, timeout=1)
        held = queue.connect()
        start = threading.Barrier(waiters + 1)
        elapsed = []
        errors = []

        def borrow():
            start.wait(5)
            began = time.monotonic()
            try:
                queue.connect().close()
                errors.append("acquired")
            except exc.TimeoutError:
                elapsed.append(time.monotonic() - began)
            except BaseException as error:
                errors.append(error)

        threads = [threading.Thread(target=borrow) for _ in range(waiters)]
        for thread in threads:
            thread.start()
        began = time.monotonic()
        start.wait(5)
        for thread in threads:
            thread.join(30)
        total = time.monotonic() - began
        try:
            assert errors == [] and len(elapsed) == waiters
            # 직렬화되면 마지막 대기자가 약 8초, 합계도 약 8초가 걸린다(부하 여유를 둔 상한).
            assert max(elapsed) < 4.5 and total < 5.0
            assert min(elapsed) >= 0.9
            assert queue._inflight == 0 and queue.checkedout() == 1
        finally:
            held.close()
        assert queue.checkedout() == 0
        queue.dispose()
    assert ledger["live"] == 0 and ledger["created"] == 1


def test_returned_connection_wakes_one_waiter_while_others_keep_waiting():
    import threading

    ledger = _ledger()
    with pool.activation():
        queue = _queue(ledger, pool_size=2, max_overflow=0, timeout=10)
        held = [queue.connect(), queue.connect()]
        acquired = []
        acquired_lock = threading.Lock()

        def borrow():
            connection = queue.connect()
            with acquired_lock:
                acquired.append(connection)

        threads = [threading.Thread(target=borrow) for _ in range(3)]
        for thread in threads:
            thread.start()
        try:
            # 세 대기자가 모두 잠금 밖 대기에 들어간 뒤 하나만 반환한다.
            assert _wait_until(lambda: queue._inflight == 3)
            held.pop().close()
            assert _wait_until(lambda: len(acquired) == 1)
            assert _wait_until(lambda: queue._inflight == 2)
            assert len(acquired) == 1 and queue.checkedout() == 2
            # 나머지 두 대기자도 반환되는 대로 각자 깨어난다.
            held.pop().close()
            with acquired_lock:
                acquired.pop().close()
            for thread in threads:
                thread.join(5)
            assert not any(thread.is_alive() for thread in threads)
        finally:
            for connection in held + acquired:
                connection.close()
        assert queue._inflight == 0 and queue.checkedout() == 0
        queue.dispose()
    assert ledger["live"] == 0 and ledger["peak_live"] == 2


def test_many_threads_never_exceed_cap_and_leave_nothing_checked_out():
    import threading
    import time

    ledger = _ledger()
    size, overflow = 2, 2
    with pool.activation():
        queue = _queue(ledger, pool_size=size, max_overflow=overflow, timeout=5)
        counter = {"out": 0, "peak": 0, "timeouts": 0}
        counter_lock = threading.Lock()
        errors = []

        def work():
            for _ in range(40):
                try:
                    connection = queue.connect()
                except exc.TimeoutError:
                    with counter_lock:
                        counter["timeouts"] += 1
                    continue
                except BaseException as error:
                    errors.append(error)
                    return
                with counter_lock:
                    counter["out"] += 1
                    counter["peak"] = max(counter["peak"], counter["out"])
                time.sleep(0.001)
                with counter_lock:
                    counter["out"] -= 1
                connection.close()

        threads = [threading.Thread(target=work) for _ in range(16)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join(60)
        assert not any(thread.is_alive() for thread in threads) and errors == []
        assert counter["peak"] <= size + overflow
        assert ledger["peak_live"] <= size + overflow
        # timeout 자체는 무거운 러너에서 날 수 있으므로(Condition 깨어남 불공정) 세지 않는다.
        assert queue._inflight == 0 and queue.checkedout() == 0
        # overflow 연결은 반환 때 닫히고 상주분은 pool_size 이하만 남는다.
        assert queue.checkedin() <= size
        queue.dispose()
    assert ledger["live"] == 0


def test_failed_connection_creation_releases_inflight_and_overflow_slot():
    from sqlalchemy.engine.default import DefaultDialect

    ledger = _ledger()
    failures = [2]

    def creator():
        if failures[0]:
            failures[0] -= 1
            raise OSError("가짜 연결 실패")
        return _Counted(ledger)

    with pool.activation():
        queue = pool.DaemonQueuePool(
            creator, pool_size=1, max_overflow=0, timeout=1, dialect=DefaultDialect()
        )
        for _ in range(2):
            with pytest.raises(OSError):
                queue.connect()
            assert queue._inflight == 0 and queue.checkedout() == 0
        # 실패가 overflow 계수를 먹지 않았으므로 상한 1개를 그대로 쓴다.
        connection = queue.connect()
        assert queue.checkedout() == 1
        connection.close()
        queue.dispose()
    assert ledger["live"] == 0 and ledger["created"] == 1


def test_timeout_leaves_no_inflight_and_pool_is_reusable():
    ledger = _ledger()
    with pool.activation():
        queue = _queue(ledger, pool_size=1, max_overflow=0, timeout=1)
        held = queue.connect()
        with pytest.raises(exc.TimeoutError):
            queue.connect()
        assert queue._inflight == 0 and queue.checkedout() == 1
        held.close()
        again = queue.connect()
        again.close()
        queue.dispose()
    assert ledger["live"] == 0 and ledger["created"] == 1


def test_dispose_and_recreate_reject_while_checkout_is_in_flight(monkeypatch):
    import threading

    ledger = _ledger()
    with pool.activation():
        queue = _queue(ledger, pool_size=1, max_overflow=0, timeout=5)
        entered = threading.Event()
        release = threading.Event()
        original = queue._do_get

        def gated():
            entered.set()
            assert release.wait(5)
            return original()

        monkeypatch.setattr(queue, "_do_get", gated)
        acquired = []

        def borrow():
            acquired.append(queue.connect())

        borrower = threading.Thread(target=borrow)
        borrower.start()
        outcomes = []

        def lifecycle():
            for operation in (queue.dispose, queue.recreate):
                try:
                    operation()
                    outcomes.append("ok")
                except pool.PoolScopeError:
                    outcomes.append("rejected")

        try:
            assert entered.wait(5)
            # 대여가 원 QueuePool 안(잠금 밖)에 있는 동안 checkedout()은 아직 0이다.
            assert queue.checkedout() == 0 and queue._inflight == 1
            # 이전 구현은 여기서 수명 잠금을 기다리며 멈췄다.
            closer = threading.Thread(target=lifecycle)
            closer.start()
            closer.join(2)
            assert not closer.is_alive()
            assert outcomes == ["rejected", "rejected"] and not queue._retired
        finally:
            release.set()
            borrower.join(5)
            monkeypatch.setattr(queue, "_do_get", original)
        assert len(acquired) == 1 and queue._inflight == 0
        acquired[0].close()
        queue.dispose()
    assert ledger["live"] == 0


def test_retire_and_new_checkout_cannot_interleave():
    import threading

    ledger = _ledger()
    with pool.activation():
        for _ in range(50):
            queue = _queue(ledger, pool_size=1, max_overflow=0, timeout=1)
            start = threading.Barrier(2)
            results = {}

            def borrow(queue=queue, start=start, results=results):
                start.wait(5)
                try:
                    results["connection"] = queue.connect()
                except pool.PoolScopeError:
                    results["connection"] = None

            def retire(queue=queue, start=start, results=results):
                start.wait(5)
                try:
                    results["replacement"] = queue.recreate()
                except pool.PoolScopeError:
                    results["replacement"] = None

            threads = [threading.Thread(target=borrow), threading.Thread(target=retire)]
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join(5)
            connection, replacement = results["connection"], results["replacement"]
            # 둘 중 정확히 하나만 이긴다: 대여가 먼저면 재생성 거절, 퇴역이 먼저면 대여 거절.
            assert (connection is None) != (replacement is None)
            if connection is not None:
                connection.close()
                queue.dispose()
            else:
                assert queue._retired and queue.checkedout() == 0
    assert ledger["live"] == 0


# ── 크기·대기 설정 ──────────────────────────────────────────────────────────


def test_default_settings_and_custom_activation_apply_to_primary_engines(registered):
    assert (pool.POOL_SIZE, pool.MAX_OVERFLOW, pool.POOL_TIMEOUT) == (4, 4, 10)
    with pool.activation(pool_size=6, max_overflow=2, pool_timeout=30):
        engines = [engine() for _ in range(3)]
        for item in engines:
            assert item.pool.size() == 6 and item.pool._max_overflow == 2
            assert item.pool.timeout() == 30 and item.pool._pre_ping is True
        assert type(engine().pool) is NullPool
    with pool.activation():
        item = engine()
        assert (item.pool.size(), item.pool._max_overflow, item.pool.timeout()) == (4, 4, 10)


@pytest.mark.parametrize("kwargs", [
    {"pool_size": 0}, {"pool_size": 11}, {"max_overflow": -1}, {"max_overflow": 11},
    {"pool_size": 6, "max_overflow": 5}, {"pool_size": 10, "max_overflow": 1},
    {"pool_timeout": 0}, {"pool_timeout": 31}, {"pool_size": True}, {"pool_timeout": 1.5},
    {"pool_size": "4"},
])
def test_invalid_activation_settings_reject_before_opening_scope(kwargs):
    with pytest.raises(ValueError):
        with pool.activation(**kwargs):
            pytest.fail("범위 밖 설정으로 수명이 열리면 안 됨")


@pytest.mark.parametrize("env, expected", [
    ({}, {"pool_size": 4, "max_overflow": 4, "pool_timeout": 10}),
    ({"KOR_TRAVEL_DAGSTER_DAEMON_POOL_SIZE": "8",
      "KOR_TRAVEL_DAGSTER_DAEMON_POOL_MAX_OVERFLOW": "0",
      "KOR_TRAVEL_DAGSTER_DAEMON_POOL_TIMEOUT_SECONDS": "30"},
     {"pool_size": 8, "max_overflow": 0, "pool_timeout": 30}),
    ({"KOR_TRAVEL_DAGSTER_DAEMON_POOL_TIMEOUT_SECONDS": "30",
      "KOR_TRAVEL_DAGSTER_DAEMON_POOL_SIZE": "10",
      "KOR_TRAVEL_DAGSTER_DAEMON_POOL_MAX_OVERFLOW": "0"},
     {"pool_size": 10, "max_overflow": 0, "pool_timeout": 30}),
])
def test_pool_settings_from_environment(monkeypatch, env, expected):
    for name in (cli.POOL_SIZE_ENV, cli.POOL_MAX_OVERFLOW_ENV, cli.POOL_TIMEOUT_ENV):
        monkeypatch.delenv(name, raising=False)
    for name, value in env.items():
        monkeypatch.setenv(name, value)
    assert cli._pool_settings() == expected


@pytest.mark.parametrize("name, value", [
    ("KOR_TRAVEL_DAGSTER_DAEMON_POOL_SIZE", ""),
    ("KOR_TRAVEL_DAGSTER_DAEMON_POOL_SIZE", "0"),
    ("KOR_TRAVEL_DAGSTER_DAEMON_POOL_SIZE", " 4"),
    ("KOR_TRAVEL_DAGSTER_DAEMON_POOL_SIZE", "+4"),
    ("KOR_TRAVEL_DAGSTER_DAEMON_POOL_SIZE", "４"),
    ("KOR_TRAVEL_DAGSTER_DAEMON_POOL_SIZE", "11"),
    ("KOR_TRAVEL_DAGSTER_DAEMON_POOL_SIZE", "7"),
    ("KOR_TRAVEL_DAGSTER_DAEMON_POOL_MAX_OVERFLOW", "-1"),
    ("KOR_TRAVEL_DAGSTER_DAEMON_POOL_TIMEOUT_SECONDS", "10.0"),
    ("KOR_TRAVEL_DAGSTER_DAEMON_POOL_TIMEOUT_SECONDS", "31"),
    ("KOR_TRAVEL_DAGSTER_DAEMON_POOL_TIMEOUT_SECONDS", "1000"),
])
def test_invalid_pool_environment_is_a_value_free_configuration_error(monkeypatch, name, value):
    monkeypatch.setenv(name, value)
    with pytest.raises(cli.DaemonPoolConfigurationError) as caught:
        cli._pool_settings()
    assert value.strip() == "" or value not in str(caught.value)


def test_wrapper_passes_environment_settings_to_primary_engines(
    tmp_path, monkeypatch, registered, capsys
):
    config(tmp_path, monkeypatch)
    monkeypatch.setenv(cli.SHARED_URL_ENV, URL)
    monkeypatch.setenv(cli.DAEMON_URL_ENV, URL)
    monkeypatch.setenv(cli.POOL_SIZE_ENV, "5")
    monkeypatch.setenv(cli.POOL_MAX_OVERFLOW_ENV, "3")
    monkeypatch.setenv(cli.POOL_TIMEOUT_ENV, "20")
    monkeypatch.setattr(sys, "argv", ["own-wrapper", "run", "-w", "same-workspace"])
    observed = []

    def original():
        item = create_engine(
            os.environ[cli.SHARED_URL_ENV], poolclass=NullPool,
            isolation_level="AUTOCOMMIT", creator=lambda: pytest.fail("I/O"),
        )
        observed.append((item.pool.size(), item.pool._max_overflow, item.pool.timeout()))

    monkeypatch.setattr(cli, "_original_cli", lambda: original)
    cli.run()
    assert observed == [(5, 3, 20)]
    err = capsys.readouterr().err
    assert "pool_size=5 max_overflow=3 pool_timeout=20s" in err
    assert "<fixture>" not in err and "fixture@" not in err and "127.0.0.1" not in err


def test_wrapper_rejects_bad_pool_environment_before_delegating(tmp_path, monkeypatch):
    config(tmp_path, monkeypatch)
    monkeypatch.setenv(cli.SHARED_URL_ENV, URL)
    monkeypatch.setenv(cli.DAEMON_URL_ENV, URL)
    monkeypatch.setenv(cli.POOL_TIMEOUT_ENV, "0")
    monkeypatch.setattr(sys, "argv", ["own-wrapper", "run"])
    monkeypatch.setattr(cli, "_original_cli", lambda: lambda: pytest.fail("위임하면 안 됨"))
    with pytest.raises(SystemExit) as caught:
        cli.main()
    assert caught.value.code == 2


def test_waiter_from_ended_activation_cannot_borrow_in_next_activation():
    import threading

    from sqlalchemy import event

    ledger = _ledger()
    first = pool.activation()
    first.__enter__()
    queue = _queue(ledger, pool_size=1, max_overflow=0, timeout=10)
    event.listen(queue, "connect", pool._on_connect)
    event.listen(queue, "checkout", pool._on_checkout)
    held = queue.connect()
    outcome = []

    def borrow():
        try:
            outcome.append(queue.connect())
        except pool.PoolScopeError as error:
            outcome.append(error)

    waiter = threading.Thread(target=borrow)
    waiter.start()
    try:
        assert _wait_until(lambda: queue._inflight == 1)
        first.__exit__(None, None, None)
        with pool.activation():
            # 이전 수명 pool로 반환되면 대기자가 깨어나지만 checkout에서 거절된다.
            held.close()
            waiter.join(5)
            assert not waiter.is_alive()
            assert len(outcome) == 1 and isinstance(outcome[0], pool.PoolScopeError)
            assert queue._inflight == 0 and queue.checkedout() == 0
            queue.dispose()
    finally:
        if waiter.is_alive():
            held.close()
            waiter.join(5)
    assert ledger["live"] == 0
