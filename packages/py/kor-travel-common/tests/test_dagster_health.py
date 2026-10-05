# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"""실제 Dagster protobuf·loopback RPC로 빈/손상 reply의 정상 오인을 막는다."""

import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import grpc
import pytest
from dagster._grpc.__generated__ import dagster_api_pb2 as wire
from grpc_health.v1 import health, health_pb2, health_pb2_grpc

from kortravelcommon.dagster_health import code_server_is_healthy


def normal(symbols=None):
    return json.dumps(
        {
            "__class__": "ListRepositoriesResponse",
            "repository_symbols": [] if symbols is None else symbols,
            "repository_code_pointer_dict": {},
        }
    )


@pytest.mark.parametrize(
    "payload,expected",
    [
        (normal(), True),
        (
            normal(
                [
                    {
                        "__class__": "LoadableRepositorySymbol",
                        "repository_name": "repo",
                        "attribute": "defs",
                    }
                ]
            ),
            True,
        ),
        (
            normal(
                [
                    {
                        "__class__": "LoadableRepositorySymbol",
                        "repository_name": "SerializableErrorInfo",
                        "attribute": "defs",
                    }
                ]
            ),
            True,
        ),
        ("", False),
        ("{}", False),
        ("[]", False),
        ("null", False),
        ("{", False),
        (json.dumps({"__class__": "SerializableErrorInfo", "message": "load error"}), False),
        (json.dumps({"__class__": "ListRepositoriesResponse"}), False),
        (normal([None]), False),
        (normal([{"__class__": "LoadableRepositorySymbol"}]), False),
        ('{"__class__":"SerializableErrorInfo",' + normal()[1:], False),
    ],
)
def test_actual_wire_response_is_fail_closed(payload, expected):
    with ThreadPoolExecutor(max_workers=2) as executor:
        server = grpc.server(executor)
        readiness = health.HealthServicer()
        readiness.set("DagsterApi", health_pb2.HealthCheckResponse.SERVING)
        health_pb2_grpc.add_HealthServicer_to_server(readiness, server)
        reply = wire.ListRepositoriesReply(
            serialized_list_repositories_response_or_error=payload
        ).SerializeToString()
        handler = grpc.unary_unary_rpc_method_handler(lambda request, context: reply)
        server.add_generic_rpc_handlers(
            (grpc.method_handlers_generic_handler("api.DagsterApi", {"ListRepositories": handler}),)
        )
        port = server.add_insecure_port("127.0.0.1:0")
        server.start()
        try:
            assert code_server_is_healthy(port) is expected
        finally:
            server.stop(0).wait()


@pytest.mark.parametrize("port", [True, 0, -1, 65536, "1", None])
def test_invalid_port_does_not_connect(port):
    assert code_server_is_healthy(port) is False


def test_health_module_does_not_import_dagster():
    root = str(Path(__file__).resolve().parents[1] / "src")
    code = (
        "import sys; from kortravelcommon.dagster_health import _reply_class; "
        "_reply_class(); assert 'dagster' not in sys.modules"
    )
    subprocess.run(
        [sys.executable, "-c", code],
        env={**os.environ, "PYTHONPATH": root},
        check=True,
        capture_output=True,
        timeout=15,
    )


@pytest.mark.parametrize("raw", [b"", b"\x80", b"x" * (4 * 1024 * 1024 + 1)])
def test_corrupt_or_oversized_wire_is_not_healthy(raw):
    with ThreadPoolExecutor(max_workers=2) as executor:
        server = grpc.server(executor)
        readiness = health.HealthServicer()
        readiness.set("DagsterApi", health_pb2.HealthCheckResponse.SERVING)
        health_pb2_grpc.add_HealthServicer_to_server(readiness, server)
        handler = grpc.unary_unary_rpc_method_handler(lambda request, context: raw)
        server.add_generic_rpc_handlers(
            (grpc.method_handlers_generic_handler("api.DagsterApi", {"ListRepositories": handler}),)
        )
        port = server.add_insecure_port("127.0.0.1:0")
        server.start()
        try:
            assert code_server_is_healthy(port) is False
        finally:
            server.stop(0).wait()


@pytest.mark.parametrize("failure", ["not-serving", "rpc-error"])
def test_rpc_deadlines_receive_cap_and_channel_cleanup(monkeypatch, failure):
    calls = []

    class Channel:
        def __enter__(self):
            return self

        def __exit__(self, *exc):
            calls.append("closed")

        def unary_unary(self, path):
            assert path == "/api.DagsterApi/ListRepositories"

            def invoke(body, timeout):
                assert body == b"" and timeout == 4
                calls.append("list")
                raise grpc.RpcError("private upstream text")

            return invoke

    def channel(address, options):
        assert address == "127.0.0.1:12703"
        assert options == (("grpc.max_receive_message_length", 4 * 1024 * 1024),)
        return Channel()

    class Stub:
        def __init__(self, channel):
            pass

        def Check(self, request, timeout):
            assert request.service == "DagsterApi" and timeout == 4
            calls.append("health")
            status = (
                health_pb2.HealthCheckResponse.NOT_SERVING
                if failure == "not-serving"
                else health_pb2.HealthCheckResponse.SERVING
            )
            return health_pb2.HealthCheckResponse(status=status)

    monkeypatch.setattr(grpc, "insecure_channel", channel)
    monkeypatch.setattr(health_pb2_grpc, "HealthStub", Stub)
    assert code_server_is_healthy(12703) is False
    assert calls == (
        ["health", "closed"] if failure == "not-serving" else ["health", "list", "closed"]
    )
