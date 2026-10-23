# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"""실제 SDK controller에서 갱신 비용과 장애 감지 계약을 검증한다."""

import os
import sys
from types import SimpleNamespace
from unittest.mock import Mock

import pytest
from dagster._daemon import controller

from kortravelcommon import daemon_pool as cli


def test_no_opt_in_preserves_original_controller(monkeypatch):
    monkeypatch.delenv(cli.WORKSPACE_RELOAD_ENV, raising=False)
    before = (controller.RELOAD_WORKSPACE_INTERVAL,
              controller.DEFAULT_WORKSPACE_FRESHNESS_TOLERANCE)
    with cli._workspace_refresh_profile():
        assert (controller.RELOAD_WORKSPACE_INTERVAL,
                controller.DEFAULT_WORKSPACE_FRESHNESS_TOLERANCE) == before
    assert (controller.RELOAD_WORKSPACE_INTERVAL,
            controller.DEFAULT_WORKSPACE_FRESHNESS_TOLERANCE) == before


@pytest.mark.parametrize("raw", ["", "0", "59", "181", "3600", "-1", "180.0", " 180", "secret"])
def test_invalid_interval_rejects_without_exposing_input(monkeypatch, raw):
    monkeypatch.setenv(cli.WORKSPACE_RELOAD_ENV, raw)
    with pytest.raises(cli.DaemonPoolConfigurationError, match="주기 설정") as error:
        with cli._workspace_refresh_profile():
            pytest.fail("위임하면 안 됨")
    assert raw != "secret" or raw not in str(error.value)
    assert controller.RELOAD_WORKSPACE_INTERVAL == 60
    assert controller.DEFAULT_WORKSPACE_FRESHNESS_TOLERANCE == 300


@pytest.mark.parametrize("interval,tolerance", [(61, 300), (60, 301), (True, 300)])
def test_unknown_controller_contract_rejects(monkeypatch, interval, tolerance):
    monkeypatch.setenv(cli.WORKSPACE_RELOAD_ENV, "180")
    monkeypatch.setattr(controller, "RELOAD_WORKSPACE_INTERVAL", interval)
    monkeypatch.setattr(controller, "DEFAULT_WORKSPACE_FRESHNESS_TOLERANCE", tolerance)
    with pytest.raises(cli.DaemonPoolConfigurationError):
        with cli._workspace_refresh_profile():
            pytest.fail("알 수 없는 SDK를 실행하면 안 됨")
    assert controller.RELOAD_WORKSPACE_INTERVAL == interval
    assert controller.DEFAULT_WORKSPACE_FRESHNESS_TOLERANCE == tolerance


def test_real_controller_skips_two_reloads_preserves_failure_grace_and_restores(monkeypatch):
    monkeypatch.setenv(cli.WORKSPACE_RELOAD_ENV, "180")
    now = [179.0]
    monkeypatch.setattr(controller, "get_current_timestamp", lambda: now[0])
    item = object.__new__(controller.DagsterDaemonController)
    refresh = Mock()
    item._workspace_process_context = SimpleNamespace(refresh_workspace=refresh)
    item._grpc_server_registry = SimpleNamespace(clear_all_grpc_endpoints=Mock())
    item._logger = Mock()
    method = controller.DagsterDaemonController.check_workspace_freshness
    with pytest.raises(SystemExit):
        with cli._workspace_refresh_profile():
            assert controller.THREAD_CHECK_INTERVAL == 5
            assert controller.DEFAULT_HEARTBEAT_INTERVAL_SECONDS == 30
            assert method(item, 0.0) == 0.0
            refresh.assert_not_called()
            now[0] = 181.0
            assert method(item, 0.0) == 181.0
            refresh.assert_called_once()
            refresh.side_effect = RuntimeError("의도한 metadata 장애")
            now[0] = 362.0
            assert method(item, 181.0) == 181.0
            now[0] = 602.0
            with pytest.raises(RuntimeError, match="metadata 장애"):
                method(item, 181.0)
            raise SystemExit(7)
    assert controller.RELOAD_WORKSPACE_INTERVAL == 60
    assert controller.DEFAULT_WORKSPACE_FRESHNESS_TOLERANCE == 300


def test_original_interval_is_supported_without_semantic_change(monkeypatch):
    monkeypatch.setenv(cli.WORKSPACE_RELOAD_ENV, "60")
    with cli._workspace_refresh_profile():
        assert controller.RELOAD_WORKSPACE_INTERVAL == 60
        assert controller.DEFAULT_WORKSPACE_FRESHNESS_TOLERANCE == 300


@pytest.mark.parametrize("arguments", [["run"], ["--help"], ["run", "--help"]])
def test_cli_profile_only_changes_run_and_restores_on_original_exit(monkeypatch, arguments):
    url = "postgresql+psycopg2://localhost/synthetic"
    monkeypatch.setenv(cli.WORKSPACE_RELOAD_ENV, "180")
    monkeypatch.setenv(cli.SHARED_URL_ENV, url)
    monkeypatch.setenv(cli.DAEMON_URL_ENV, url)
    monkeypatch.setattr(cli, "_validate_storage_config", lambda: None)
    monkeypatch.setattr(sys, "argv", ["profile-test", *arguments])
    before = dict(os.environ)
    expected = 180 if arguments == ["run"] else 60
    called = []

    def original():
        called.append(os.getpid())
        assert controller.RELOAD_WORKSPACE_INTERVAL == expected
        assert list(sys.argv) == ["profile-test", *arguments]
        raise SystemExit(9)

    monkeypatch.setattr(cli, "_original_cli", lambda: original)
    with pytest.raises(SystemExit) as error:
        cli.run()
    assert error.value.code == 9 and called == [os.getpid()]
    assert dict(os.environ) == before
    assert controller.RELOAD_WORKSPACE_INTERVAL == 60
    assert controller.DEFAULT_WORKSPACE_FRESHNESS_TOLERANCE == 300
