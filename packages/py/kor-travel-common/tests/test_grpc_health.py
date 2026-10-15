# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"""실제 loopback RPC와 논리 clock으로 조회·예산·무부작용 경계를 검증한다."""

import contextlib
import json
import os
import socket
import socketserver
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from types import SimpleNamespace

import grpc
import pytest
from grpc_health.v1 import health, health_pb2, health_pb2_grpc

from kortravelcommon import grpc_health as probe
from kortravelcommon.dagster_health import _reply_class, code_server_is_healthy


def payload():
    return {
        "__class__": "ListRepositoriesResponse",
        "repository_symbols": [{
            "__class__": "LoadableRepositorySymbol",
            "repository_name": "repo",
            "attribute": "defs",
        }],
        "repository_code_pointer_dict": {
            "repo": {"__class__": "ModuleCodePointer", "module": "example", "fn_name": "defs"},
        },
    }


def wire(value):
    return _reply_class()(
        serialized_list_repositories_response_or_error=json.dumps(value)
    ).SerializeToString()


@contextlib.contextmanager
def server(raw=None, serving=True, health_delay=0, list_delay=0):
    with ThreadPoolExecutor(max_workers=2) as executor:
        instance = grpc.server(executor)
        calls = []

        class Status(health.HealthServicer):
            def Check(self, request, context):
                calls.append("Check")
                time.sleep(health_delay)
                return super().Check(request, context)

        service = Status()
        service.set("DagsterApi", health_pb2.HealthCheckResponse.SERVING if serving
                    else health_pb2.HealthCheckResponse.NOT_SERVING)
        health_pb2_grpc.add_HealthServicer_to_server(service, instance)

        def repositories(request, context):
            calls.append("ListRepositories")
            time.sleep(list_delay)
            return wire(payload()) if raw is None else raw

        instance.add_generic_rpc_handlers((grpc.method_handlers_generic_handler(
            "api.DagsterApi", {
                "ListRepositories": grpc.unary_unary_rpc_method_handler(repositories),
            },
        ),))
        port = instance.add_insecure_port("127.0.0.1:0")
        assert port
        instance.start()
        try:
            yield port, calls
        finally:
            instance.stop(0).wait()


def test_real_live_does_not_request_or_require_definitions():
    with server(raw=b"corrupt") as (port, calls):
        assert probe.grpc_code_server_is_live(port)
        assert calls == ["Check"]
        assert not probe.grpc_code_server_is_ready(port, repository_name="repo")
        assert calls == ["Check", "Check", "ListRepositories"]


def test_real_ready_and_quiet_cli():
    with server() as (port, _):
        assert probe.grpc_code_server_is_ready(port, repository_name="repo")
        result = subprocess.run(
            [sys.executable, "-m", "kortravelcommon.grpc_health", str(port),
             "--check", "ready", "--repository", "repo"],
            capture_output=True,
            env={**os.environ, "PYTHONPATH": str(Path(probe.__file__).parents[1])},
            timeout=10,
        )
        assert result.returncode == 0
        assert result.stdout == result.stderr == b""


@pytest.mark.parametrize("serving,health_delay,list_delay", [
    (False, 0, 0), (True, 0.15, 0), (True, 0, 0.15),
])
def test_real_failure_and_short_deadline(serving, health_delay, list_delay):
    with server(serving=serving, health_delay=health_delay, list_delay=list_delay) as (port, _):
        started = time.monotonic()
        assert not probe.grpc_code_server_is_ready(
            port, repository_name="repo", timeout_seconds=0.05
        )
        assert time.monotonic() - started < 1


@pytest.mark.parametrize("bad", [
    {}, {"__class__": "SerializableErrorInfo", "message": "private"},
    {**payload(), "repository_symbols": []},
    {**payload(), "repository_symbols": payload()["repository_symbols"] * 2},
    {**payload(), "repository_code_pointer_dict": {}},
    {**payload(), "repository_code_pointer_dict": {
        "repo": {"__class__": "ModuleCodePointer", "module": "example", "fn_name": "wrong"},
    }},
    {**payload(), "container_context": {"__class__": "unknown"}},
    {**payload(), "new_unreviewed_metadata": True},
])
def test_ready_rejects_error_unknown_or_wrong_repository(bad):
    with server(raw=wire(bad)) as (port, _):
        assert not probe.grpc_code_server_is_ready(port, repository_name="repo")


def test_harmless_error_substring_is_not_a_structured_error():
    value = payload()
    value["container_image"] = "SerializableErrorInfo"
    with server(raw=wire(value)) as (port, _):
        assert probe.grpc_code_server_is_ready(port, repository_name="repo")
        assert not probe.grpc_code_server_is_ready(port, repository_name="missing")


def test_unknown_version_fails_closed(monkeypatch):
    import importlib.metadata
    monkeypatch.setattr(importlib.metadata, "version", lambda _: "future")
    with server() as (port, _):
        assert not probe.grpc_code_server_is_ready(port, repository_name="repo")


@pytest.mark.parametrize("port", [True, 0, -1, 65536, "1", None])
def test_invalid_ports_do_not_connect(port):
    assert not probe.grpc_code_server_is_live(port)


@pytest.mark.parametrize("budget", [True, 0, -1, float("inf"), float("nan"), 4.001, 10**1000, None])
def test_invalid_or_expanded_budgets_do_not_connect(budget):
    assert not probe.grpc_code_server_is_live(1, timeout_seconds=budget)


@pytest.mark.parametrize("name", [None, "", " ", 1, True])
def test_invalid_repository(name):
    assert not probe.grpc_code_server_is_ready(1, repository_name=name)


def fake_rpc(monkeypatch, *, first=3, second=2, decode=0, close=0, require_no_retry=True):
    clock = [0.0]
    timeouts = []
    monkeypatch.setattr(probe.time, "monotonic", lambda: clock[0])

    class Channel:
        def __enter__(self):
            return self

        def __exit__(self, *args):
            clock[0] += close

        def unary_unary(self, path):
            assert path == "/api.DagsterApi/ListRepositories"

            def call(raw, timeout):
                assert raw == b""
                timeouts.append(timeout)
                clock[0] += second
                return b"wire"
            return call

    def check(request, timeout):
        assert request.service == "DagsterApi"
        timeouts.append(timeout)
        clock[0] += first
        return SimpleNamespace(status=health_pb2.HealthCheckResponse.SERVING)

    def channel_factory(target, *, options):
        assert target == "127.0.0.1:1"
        if require_no_retry:
            assert ("grpc.enable_retries", 0) in options
            assert ("grpc.enable_http_proxy", 0) in options
        return Channel()

    monkeypatch.setattr(grpc, "insecure_channel", channel_factory)
    monkeypatch.setattr(health_pb2_grpc, "HealthStub", lambda _: SimpleNamespace(Check=check))

    def parsed(*args):
        clock[0] += decode
        return True

    monkeypatch.setattr(probe, "_repository_loaded", parsed)
    return timeouts


def test_old_each_rpc_budget_vs_new_shared_budget(monkeypatch):
    import kortravelcommon.dagster_health as legacy
    timeouts = fake_rpc(monkeypatch, require_no_retry=False)
    monkeypatch.setattr(legacy, "_is_loaded_reply", lambda _: True)
    assert code_server_is_healthy(1) is True  # 기존 함수의 각4초 호환 계약은 유지한다.
    assert timeouts == [4, 4]
    timeouts = fake_rpc(monkeypatch)
    assert probe.grpc_code_server_is_ready(1, repository_name="repo") is False
    assert timeouts == [4, 1]


@pytest.mark.parametrize("first,second,decode,close", [
    (4.1, 0, 0, 0), (1, 1, 2.1, 0), (1, 1, 0, 2.1),
])
def test_elapsed_work_never_returns_success(monkeypatch, first, second, decode, close):
    fake_rpc(monkeypatch, first=first, second=second, decode=decode, close=close)
    assert not probe.grpc_code_server_is_ready(1, repository_name="repo")


@pytest.mark.parametrize("args", [
    [], ["1"], ["True", "--check", "live"], ["0", "--check", "live"],
    ["1", "--check", "wrong"], ["1", "--check", "ready"],
    ["1", "--check", "live", "--repository", "repo"],
    ["1", "--check", "ready", "--repository", ""],
])
def test_cli_invalid_is_quiet(args, capsys):
    assert probe.main(args) == 2
    assert capsys.readouterr() == ("", "")


def test_fresh_import_and_actual_live_do_not_load_app_or_dagster():
    root = str(Path(probe.__file__).parents[1])
    with server() as (port, _):
        code = (
            "import sys; from kortravelcommon.grpc_health import grpc_code_server_is_live; "
            f"assert grpc_code_server_is_live({port}); "
            "assert not any(m.split('.')[0] in {'dagster','sqlalchemy','kortravelweather'} "
            "for m in sys.modules)"
        )
        subprocess.run([sys.executable, "-c", code],
                       env={**os.environ, "PYTHONPATH": root}, check=True, timeout=10)


def test_source_has_no_recovery_side_effect_calls():
    import ast
    tree = ast.parse(Path(probe.__file__).read_text())
    forbidden = {"kill", "Popen", "report_run_failed", "DagsterInstance", "fork", "system"}
    assert not any(isinstance(node, ast.Attribute) and node.attr in forbidden
                   for node in ast.walk(tree))


@contextlib.contextmanager
def rejecting_proxy():
    attempts = []

    class Reject(socketserver.BaseRequestHandler):
        def handle(self):
            attempts.append(True)
            self.request.settimeout(1)
            self.request.recv(4096)
            self.request.sendall(
                b"HTTP/1.1 403 Forbidden\r\nContent-Length: 0\r\n\r\n"
            )

    with socketserver.ThreadingTCPServer(("127.0.0.1", 0), Reject) as instance:
        thread = threading.Thread(target=instance.serve_forever, kwargs={"poll_interval": 0.01})
        thread.start()
        try:
            yield instance.server_address[1], attempts
        finally:
            instance.shutdown()
            thread.join(timeout=2)
            assert not thread.is_alive()
            instance.socket.setblocking(False)
            while True:
                try:
                    queued, _ = instance.socket.accept()
                except BlockingIOError:
                    break
                attempts.append(True)
                queued.close()


def proxy_cli(port, variable, proxy_port, mode):
    root = str(Path(probe.__file__).parents[1])
    env = {key: value for key, value in os.environ.items()
           if key.lower() not in {"grpc_proxy", "http_proxy", "https_proxy",
                                  "no_proxy", "no_grpc_proxy"}}
    env.update(PYTHONPATH=root, **{variable: f"http://127.0.0.1:{proxy_port}"})
    args = [sys.executable, "-m", "kortravelcommon.grpc_health", str(port), "--check", mode]
    if mode == "ready":
        args += ["--repository", "repo"]
    return subprocess.run(args, env=env, capture_output=True, timeout=10)


@pytest.mark.parametrize("variable", ["grpc_proxy", "http_proxy", "https_proxy"])
@pytest.mark.parametrize("mode,raw,expected", [
    ("live", None, 0), ("ready", None, 0), ("ready", b"malformed", 1),
])
def test_actual_proxy_environment_cannot_redirect_or_emit_errors(variable, mode, raw, expected):
    with rejecting_proxy() as (proxy_port, attempts), server(raw=raw) as (port, _):
        result = proxy_cli(port, variable, proxy_port, mode)
        assert result.returncode == expected
        assert result.stdout == result.stderr == b""
    assert attempts == []


@pytest.mark.parametrize("variable", ["grpc_proxy", "http_proxy", "https_proxy"])
def test_closed_loopback_target_never_becomes_healthy_through_proxy(variable):
    with socket.socket() as unused:
        unused.bind(("127.0.0.1", 0))
        port = unused.getsockname()[1]
    with rejecting_proxy() as (proxy_port, attempts):
        result = proxy_cli(port, variable, proxy_port, "live")
        assert result.returncode == 1
        assert result.stdout == result.stderr == b""
    assert attempts == []
