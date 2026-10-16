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

URL = "postgresql+psycopg2://fixture:fixture@127.0.0.1:1/fixture?connect_timeout=3&options=-cstatement_timeout%3D5000%20-clock_timeout%3D1000"


@pytest.fixture(autouse=True)
def clean_scope():
    assert pool._owner_pid is None and not pool._engines
    yield
    assert pool._owner_pid is None and not pool._engines


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
            assert item.pool.size() == 2 and item.pool._max_overflow == 2
            assert item.pool.timeout() == 1 and item.pool._recycle == 3600
            assert item.url == make_url(URL)
            assert item.get_execution_options() == {}
        first_pool = engines[0].pool
        engines[0].dispose()
        assert engines[0].pool is not first_pool
        with pytest.raises(pool.PoolScopeError):
            engine()
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
