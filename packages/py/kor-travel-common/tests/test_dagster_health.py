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
from dagster._check import CheckError
from dagster._core.code_pointer import ModuleCodePointer
from dagster._grpc.__generated__ import dagster_api_pb2 as wire
from dagster._grpc.types import ListRepositoriesResponse, LoadableRepositorySymbol
from dagster._serdes import deserialize_value, serialize_value
from dagster_shared.serdes.errors import DeserializationError
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


@pytest.mark.parametrize(
    "field,value",
    [
        ("repository_code_pointer_dict", {"repo": None}),
        ("repository_code_pointer_dict", {"repo": {"__class__": "UnknownPointer"}}),
        (
            "repository_code_pointer_dict",
            {"repo": {"__class__": "ModuleCodePointer", "module": [], "fn_name": "defs"}},
        ),
        (
            "repository_code_pointer_dict",
            {
                "repo": {
                    "__class__": "ModuleCodePointer",
                    "module": "jobs",
                    "fn_name": "defs",
                    "working_directory": 1,
                }
            },
        ),
        ("executable_path", []),
        ("executable_path", {}),
        ("container_image", 123),
        ("entry_point", 123),
        ("entry_point", [False]),
        ("entry_point", [None]),
        ("container_context", []),
        ("container_context", {"nested": {"__class__": "UnknownContext"}}),
        ("dagster_library_versions", []),
        ("dagster_library_versions", {"dagster": 123}),
        ("dagster_library_versions", {"__class__": "UnknownLibraryMetadata", "dagster": "1.13.24"}),
        ("defs_state_info", {"__class__": "UnknownState"}),
    ],
)
def test_invalid_metadata_rejected_by_actual_dagster_and_health(field, value):
    payload = json.loads(normal())
    payload[field] = value
    text = json.dumps(payload)
    with pytest.raises((CheckError, DeserializationError)):
        deserialize_value(text, ListRepositoriesResponse)
    test_actual_wire_response_is_fail_closed(text, False)


@pytest.mark.parametrize(
    "kind,fields",
    [
        ("ModuleCodePointer", {"module": "jobs", "fn_name": "defs"}),
        ("FileCodePointer", {"python_file": "/work/jobs.py", "fn_name": "defs"}),
        ("PackageCodePointer", {"module": "jobs", "attribute": "defs"}),
    ],
)
def test_supported_pointer_and_optional_metadata_are_valid(kind, fields):
    payload = json.loads(
        normal(
            [
                {
                    "__class__": "LoadableRepositorySymbol",
                    "repository_name": "repo",
                    "attribute": "defs",
                }
            ]
        )
    )
    payload.update(
        {
            "repository_code_pointer_dict": {
                "repo": {"__class__": kind, **fields, "working_directory": None}
            },
            "executable_path": "/usr/local/bin/python",
            "entry_point": ["dagster"],
            "container_image": None,
            "container_context": {"nested": [1, "value", None]},
            "dagster_library_versions": {"dagster": "1.13.24"},
            "defs_state_info": None,
        }
    )
    text = json.dumps(payload)
    assert isinstance(deserialize_value(text, ListRepositoriesResponse), ListRepositoriesResponse)
    test_actual_wire_response_is_fail_closed(text, True)


def test_unknown_profile_is_rejected_without_reinterpreting_schema():
    payload = json.loads(normal())
    payload["future_metadata"] = "unknown"
    test_actual_wire_response_is_fail_closed(json.dumps(payload), False)


@pytest.mark.parametrize(
    "variant",
    [
        "normal",
        "empty-wire",
        "pointer-null",
        "pointer-unknown",
        "executable-list",
        "entry-number",
        "unsupported-state",
        "versions-marker",
        "pointers-marker",
        "default-repository",
    ],
)
def test_actual_isolated_module_cli_schema_boundary(variant):
    control = serialize_value(
        ListRepositoriesResponse(
            repository_symbols=[LoadableRepositorySymbol(repository_name="repo", attribute="defs")],
            repository_code_pointer_dict={"repo": ModuleCodePointer("jobs", "defs", None)},
            executable_path="/usr/local/bin/python",
            entry_point=["dagster"],
        )
    )
    payload = json.loads(control)
    if variant == "pointer-null":
        payload["repository_code_pointer_dict"] = {"repo": None}
    elif variant == "pointer-unknown":
        payload["repository_code_pointer_dict"] = {"repo": {"__class__": "UnknownPointer"}}
    elif variant == "executable-list":
        payload["executable_path"] = []
    elif variant == "entry-number":
        payload["entry_point"] = 123
    elif variant == "versions-marker":
        payload["dagster_library_versions"] = {
            "__class__": "UnknownLibraryMetadata",
            "dagster": "1.13.24",
        }
    elif variant == "pointers-marker":
        payload["repository_code_pointer_dict"] = {
            "__class__": payload["repository_code_pointer_dict"]["repo"]
        }
    elif variant == "default-repository":
        payload["repository_symbols"][0]["repository_name"] = "__repository__"
        payload["repository_code_pointer_dict"] = {
            "__repository__": payload["repository_code_pointer_dict"]["repo"]
        }
        assert isinstance(
            deserialize_value(json.dumps(payload), ListRepositoriesResponse),
            ListRepositoriesResponse,
        )
    elif variant == "unsupported-state":
        payload["defs_state_info"] = {"__class__": "DefsStateInfo", "info_mapping": {}}
        assert isinstance(
            deserialize_value(json.dumps(payload), ListRepositoriesResponse),
            ListRepositoriesResponse,
        )
    raw = (
        b""
        if variant == "empty-wire"
        else wire.ListRepositoriesReply(
            serialized_list_repositories_response_or_error=json.dumps(payload)
        ).SerializeToString()
    )
    with ThreadPoolExecutor(max_workers=2) as executor:
        server = grpc.server(executor)
        readiness = health.HealthServicer()
        readiness.set("DagsterApi", health_pb2.HealthCheckResponse.SERVING)
        health_pb2_grpc.add_HealthServicer_to_server(readiness, server)
        server.add_generic_rpc_handlers(
            (
                grpc.method_handlers_generic_handler(
                    "api.DagsterApi",
                    {
                        "ListRepositories": grpc.unary_unary_rpc_method_handler(
                            lambda request, context: raw
                        )
                    },
                ),
            )
        )
        port = server.add_insecure_port("127.0.0.1:0")
        server.start()
        try:
            result = subprocess.run(
                [sys.executable, "-I", "-m", "kortravelcommon.dagster_health", str(port)],
                capture_output=True,
                text=True,
                timeout=20,
            )
            assert result.returncode == (0 if variant in ("normal", "default-repository") else 1)
            assert result.stdout == result.stderr == ""
        finally:
            server.stop(0).wait()


@pytest.mark.parametrize("field", ["dagster_library_versions", "repository_code_pointer_dict"])
@pytest.mark.parametrize(
    "marker", ["__class__", "__enum__", "__set__", "__frozenset__", "__mapping_items__"]
)
def test_mapping_serdes_markers_are_rejected(field, marker):
    payload = json.loads(normal())
    value = (
        "1.13.24"
        if field == "dagster_library_versions"
        else {"__class__": "ModuleCodePointer", "module": "jobs", "fn_name": "defs"}
    )
    payload[field] = {marker: value}
    test_actual_wire_response_is_fail_closed(json.dumps(payload), False)
