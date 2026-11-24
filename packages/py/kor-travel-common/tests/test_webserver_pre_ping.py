# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"""webserver storage pre-ping plugin: 실제 dagster-postgres 재생성 경로와 opt-in 환경 복원.

DB에 연결하지 않는다. engine은 lazy이고 creator는 호출되면 실패한다.
"""

import os
import sys

import pytest
from sqlalchemy import create_engine
from sqlalchemy.dialects import plugins
from sqlalchemy.engine import make_url
from sqlalchemy.pool import NullPool, QueuePool

from kortravelcommon import _webserver_pool_plugin as webpool
from kortravelcommon import daemon_pool as cli

URL = make_url(
    "postgresql+psycopg2://127.0.0.1:1/fixture?connect_timeout=3"
).set(username="fixture", password="<fixture>").render_as_string(hide_password=False)


def _forbidden():
    raise AssertionError("실제 DB 연결 금지")


@pytest.fixture
def registered():
    plugins.register(webpool.PLUGIN_NAME, webpool.__name__, "WebserverPrePingPlugin")


def _plugged():
    return cli._with_plugin(URL, webpool.PLUGIN_NAME)


def test_plugin_turns_on_pre_ping_only_for_explicitly_sized_pools(registered):
    sized = create_engine(
        _plugged(), isolation_level="AUTOCOMMIT", pool_size=1, max_overflow=20,
        pool_recycle=3600, creator=_forbidden,
    )
    assert isinstance(sized.pool, QueuePool) and sized.pool._pre_ping is True
    assert sized.pool.size() == 1 and sized.pool._max_overflow == 20
    assert sized.pool._recycle == 3600
    assert "plugin" not in sized.url.query and sized.url == make_url(URL)

    null = create_engine(_plugged(), isolation_level="AUTOCOMMIT", poolclass=NullPool,
                         creator=_forbidden)
    assert type(null.pool) is NullPool and null.pool._pre_ping is False

    # 연결 확인용 일회 engine(크기 미지정)과 명시 pre-ping 값은 바꾸지 않는다.
    plain = create_engine(_plugged(), creator=_forbidden)
    assert plain.pool._pre_ping is False
    explicit = create_engine(_plugged(), pool_size=1, pool_pre_ping=False, creator=_forbidden)
    assert explicit.pool._pre_ping is False


@pytest.mark.parametrize("module, name", [
    ("dagster_postgres.run_storage.run_storage", "PostgresRunStorage"),
    ("dagster_postgres.event_log.event_log", "PostgresEventLogStorage"),
    ("dagster_postgres.schedule_storage.schedule_storage", "PostgresScheduleStorage"),
])
def test_real_optimize_for_webserver_engines_get_pre_ping(registered, module, name):
    """설치된 dagster-postgres의 webserver 재생성 호출 모양이 plugin 조건과 맞는지 본다."""
    storage_module = pytest.importorskip(module)
    storage_class = getattr(storage_module, name)
    storage = storage_class.__new__(storage_class)
    storage.postgres_url = _plugged()
    storage._token_provider = None
    storage._engine = create_engine(
        storage.postgres_url, isolation_level="AUTOCOMMIT", poolclass=NullPool,
        creator=_forbidden,
    )
    assert storage._engine.pool._pre_ping is False
    storage.optimize_for_webserver(15000, 3600, 20)
    assert isinstance(storage._engine.pool, QueuePool)
    assert storage._engine.pool._pre_ping is True
    assert storage._engine.pool.size() == 1 and storage._engine.pool._max_overflow == 20

    # plugin 없는 원 URL에서는 SDK 그대로 pre-ping이 없다(이 변경이 필요한 이유).
    storage.postgres_url = URL
    storage.optimize_for_webserver(15000, 3600, 20)
    assert storage._engine.pool._pre_ping is False


def _config(tmp_path, monkeypatch):
    monkeypatch.setenv("DAGSTER_HOME", str(tmp_path))
    (tmp_path / "dagster.yaml").write_text(
        "storage:\n  postgres:\n    postgres_url:\n"
        "      env: KOR_TRAVEL_DAGSTER_SHARED_PG_URL\n    should_autocreate_tables: false\n"
    )


def test_opt_in_patches_only_own_process_url_and_restores(tmp_path, monkeypatch):
    adapter = pytest.importorskip("kortravelcommon.dagster_webserver")
    _config(tmp_path, monkeypatch)
    monkeypatch.setenv(cli.SHARED_URL_ENV, URL)
    monkeypatch.setenv(adapter.PRE_PING_ENV, "1")
    seen = []
    with pytest.raises(RuntimeError):
        with adapter._storage_pre_ping():
            seen.append(make_url(os.environ[cli.SHARED_URL_ENV]).query.get("plugin"))
            raise RuntimeError("원 CLI 실패")
    assert seen == [webpool.PLUGIN_NAME]
    assert os.environ[cli.SHARED_URL_ENV] == URL


@pytest.mark.parametrize("value", [None, "0"])
def test_without_opt_in_url_is_untouched(tmp_path, monkeypatch, value):
    adapter = pytest.importorskip("kortravelcommon.dagster_webserver")
    monkeypatch.setenv(cli.SHARED_URL_ENV, URL)
    if value is None:
        monkeypatch.delenv(adapter.PRE_PING_ENV, raising=False)
    else:
        monkeypatch.setenv(adapter.PRE_PING_ENV, value)
    # opt-in이 아니면 storage YAML도 읽지 않는다.
    monkeypatch.setenv("DAGSTER_HOME", str(tmp_path / "missing"))
    with adapter._storage_pre_ping():
        assert os.environ[cli.SHARED_URL_ENV] == URL
    assert os.environ[cli.SHARED_URL_ENV] == URL


@pytest.mark.parametrize("case", ["bad-flag", "bad-yaml", "existing-plugin", "wrong-driver",
                                  "missing-url"])
def test_opt_in_rejects_unsupported_configuration_without_values(tmp_path, monkeypatch, case):
    adapter = pytest.importorskip("kortravelcommon.dagster_webserver")
    _config(tmp_path, monkeypatch)
    monkeypatch.setenv(adapter.PRE_PING_ENV, "1")
    monkeypatch.setenv(cli.SHARED_URL_ENV, URL)
    if case == "bad-flag":
        monkeypatch.setenv(adapter.PRE_PING_ENV, "yes")
    elif case == "bad-yaml":
        (tmp_path / "dagster.yaml").write_text("storage:\n  postgres:\n    postgres_url: x\n")
    elif case == "existing-plugin":
        monkeypatch.setenv(cli.SHARED_URL_ENV, URL + "&plugin=other")
    elif case == "wrong-driver":
        monkeypatch.setenv(cli.SHARED_URL_ENV, URL.replace("psycopg2", "psycopg"))
    else:
        monkeypatch.delenv(cli.SHARED_URL_ENV)
    before = os.environ.get(cli.SHARED_URL_ENV)
    with pytest.raises(cli.DaemonPoolConfigurationError) as caught:
        with adapter._storage_pre_ping():
            pytest.fail("거절해야 함")
    assert "fixture" not in str(caught.value)
    assert os.environ.get(cli.SHARED_URL_ENV) == before


def test_main_runs_native_cli_inside_opt_in_and_exits_2_on_bad_config(tmp_path, monkeypatch,
                                                                       capsys):
    adapter = pytest.importorskip("kortravelcommon.dagster_webserver")
    pytest.importorskip("dagster_webserver")
    from dagster_webserver import app
    from dagster_webserver import cli as native_cli

    original = app.DagsterWebserver
    _config(tmp_path, monkeypatch)
    monkeypatch.setenv(cli.SHARED_URL_ENV, URL)
    monkeypatch.setenv(adapter.PRE_PING_ENV, "1")
    monkeypatch.setattr(sys, "argv", ["owned", "-h", "127.0.0.1"])
    seen = []
    monkeypatch.setattr(
        native_cli, "main",
        lambda: seen.append(make_url(os.environ[cli.SHARED_URL_ENV]).query.get("plugin")),
    )
    try:
        adapter.main()
        assert seen == [webpool.PLUGIN_NAME] and os.environ[cli.SHARED_URL_ENV] == URL
        monkeypatch.setenv(adapter.PRE_PING_ENV, "true")
        with pytest.raises(SystemExit) as caught:
            adapter.main()
        assert caught.value.code == 2 and len(seen) == 1
        assert "fixture" not in capsys.readouterr().err
    finally:
        app.DagsterWebserver = original


def test_wheel_metadata_registers_both_plugins():
    import tomllib
    from pathlib import Path

    project = tomllib.loads(
        (Path(__file__).resolve().parents[1] / "pyproject.toml").read_text(encoding="utf-8")
    )
    entry = project["project"]["entry-points"]["sqlalchemy.plugins"]
    assert entry[webpool.PLUGIN_NAME] == (
        "kortravelcommon._webserver_pool_plugin:WebserverPrePingPlugin"
    )
    assert entry["kortravel_daemon_pool"] == (
        "kortravelcommon._daemon_pool_plugin:DaemonPoolPlugin"
    )
