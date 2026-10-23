# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"""기존 daemon CLI를 같은 프로세스에서 호출하는 명시적 연결 풀 진입점."""

from __future__ import annotations

import importlib.metadata
import os
import sys
from contextlib import contextmanager

SHARED_URL_ENV = "KOR_TRAVEL_DAGSTER_SHARED_PG_URL"
DAEMON_URL_ENV = "KOR_TRAVEL_DAGSTER_DAEMON_POSTGRES_URL"
WORKSPACE_RELOAD_ENV = "KOR_TRAVEL_DAGSTER_WORKSPACE_RELOAD_SECONDS"
EXPECTED_VERSIONS = {
    "dagster": "1.13.24",
    "dagster-postgres": "0.29.24",
    "SQLAlchemy": "2.0.54",
}


class DaemonPoolConfigurationError(RuntimeError):
    """값이나 URL을 포함하지 않는 설정 오류."""


def _original_cli():
    for name, expected in EXPECTED_VERSIONS.items():
        if importlib.metadata.version(name) != expected:
            raise DaemonPoolConfigurationError("지원하는 설치 버전이 아닙니다.")
    entries = [
        entry
        for entry in importlib.metadata.distribution("dagster").entry_points
        if entry.group == "console_scripts" and entry.name == "dagster-daemon"
    ]
    if len(entries) != 1 or entries[0].value != "dagster._daemon.cli:main":
        raise DaemonPoolConfigurationError("공식 daemon 진입점을 확인할 수 없습니다.")
    return entries[0].load()


def _pooled_url(shared: str | None, dedicated: str | None) -> str:
    from sqlalchemy.engine import make_url

    from kortravelcommon._daemon_pool_plugin import PLUGIN_NAME

    if not shared or dedicated != shared:
        raise DaemonPoolConfigurationError("전용 DSN과 원 shared DSN이 같아야 합니다.")
    try:
        url = make_url(dedicated)
    except Exception:
        raise DaemonPoolConfigurationError("DSN 형식이 잘못되었습니다.") from None
    if url.drivername != "postgresql+psycopg2" or "plugin" in url.query:
        raise DaemonPoolConfigurationError("지원하지 않는 DSN 또는 기존 plugin입니다.")
    return url.update_query_dict({"plugin": PLUGIN_NAME}).render_as_string(hide_password=False)


def _validate_storage_config() -> None:
    from pathlib import Path

    import yaml

    try:
        path = Path(os.environ["DAGSTER_HOME"]) / "dagster.yaml"
        with path.open("rb") as stream:
            raw = stream.read(1024 * 1024 + 1)
        if len(raw) > 1024 * 1024:
            raise ValueError
        data = yaml.safe_load(raw)
        if "instance_class" in data:
            raise ValueError
        storage = data["storage"]
        if set(storage) != {"postgres"}:
            raise ValueError
        config = storage["postgres"]
        if config.get("postgres_url") != {"env": SHARED_URL_ENV}:
            raise ValueError
        if config.get("should_autocreate_tables") is not False:
            raise ValueError
    except Exception:
        raise DaemonPoolConfigurationError("지원하는 shared storage 설정이 아닙니다.") from None


@contextmanager
def _workspace_refresh_profile():
    """검증한 SDK의 전체 metadata 갱신 주기만 명시적으로 늦춘다."""
    raw = os.environ.get(WORKSPACE_RELOAD_ENV)
    if raw is None:
        yield
        return
    # 긴 미확인 상태를 만들지 않도록 원 60초 또는 요청한 3배 주기만 지원한다.
    if raw not in {"60", "180"}:
        raise DaemonPoolConfigurationError("workspace 갱신 주기 설정을 확인할 수 없습니다.")

    from dagster._daemon import controller

    original_interval = controller.RELOAD_WORKSPACE_INTERVAL
    original_tolerance = controller.DEFAULT_WORKSPACE_FRESHNESS_TOLERANCE
    if type(original_interval) is not int or original_interval != 60:
        raise DaemonPoolConfigurationError("지원하는 workspace 갱신 계약이 아닙니다.")
    if type(original_tolerance) is not int or original_tolerance != 300:
        raise DaemonPoolConfigurationError("지원하는 workspace 장애 유예 계약이 아닙니다.")
    interval = int(raw)
    # 마지막 정상 갱신 뒤의 상한에는 원 240초 실패 유예를 그대로 더한다.
    # heartbeat/센서/실행 감시/SDK controller 함수는 변경하지 않는다.
    controller.RELOAD_WORKSPACE_INTERVAL = interval
    controller.DEFAULT_WORKSPACE_FRESHNESS_TOLERANCE = interval + (
        original_tolerance - original_interval
    )
    try:
        yield
    finally:
        controller.RELOAD_WORKSPACE_INTERVAL = original_interval
        controller.DEFAULT_WORKSPACE_FRESHNESS_TOLERANCE = original_tolerance


def run() -> None:
    """argv와 SDK 신호 처리는 원 CLI에 맡기고 run 명령만 pool을 활성화한다."""
    original = _original_cli()
    if sys.argv[1:2] != ["run"] or "--help" in sys.argv[2:]:
        original()
        return

    if any(arg == "--instance-ref" or arg.startswith("--instance-ref=") for arg in sys.argv[2:]):
        raise DaemonPoolConfigurationError("별도 instance ref는 지원하지 않습니다.")

    from kortravelcommon._daemon_pool_plugin import activation

    _validate_storage_config()
    shared = os.environ.get(SHARED_URL_ENV)
    pooled = _pooled_url(shared, os.environ.get(DAEMON_URL_ENV))
    try:
        with activation(), _workspace_refresh_profile():
            os.environ[SHARED_URL_ENV] = pooled
            original()
    finally:
        if shared is None:
            os.environ.pop(SHARED_URL_ENV, None)
        else:
            os.environ[SHARED_URL_ENV] = shared


def main() -> None:
    """새 설정 오류만 값 없는 메시지로 종료하고 기존 CLI 종료 코드는 유지한다."""
    try:
        run()
    except DaemonPoolConfigurationError:
        print("daemon 연결 풀 설정을 확인할 수 없습니다.", file=sys.stderr)
        raise SystemExit(2) from None


if __name__ == "__main__":
    main()
