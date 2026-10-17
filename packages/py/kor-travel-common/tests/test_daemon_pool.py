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
    yield
    assert pool._owner_pid is None and not pool._engines and pool._primary_slots == 0


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
            assert item.pool.size() == 2 and item.pool._max_overflow == 2
            assert item.pool.timeout() == 1 and item.pool._recycle == 3600
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
