# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"""가벼운 code-server 점검: proxy와 자식의 정상 저장소 응답을 함께 확인한다.

Dagster 전체 import는 하지 않는다. 설치된 Dagster의 생성 protobuf를 직접 읽어
wire schema를 재구현하지 않고, 빈/손상/오류 응답은 실패로 판정한다.
"""

import importlib.metadata
import importlib.util
import json
import sys
from typing import Any

_MAX_REPLY_BYTES = 4 * 1024 * 1024


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("중복된 저장소 응답 필드")
        result[key] = value
    return result


def _reply_class() -> Any:
    distribution = importlib.metadata.distribution("dagster")
    path = distribution.locate_file("dagster/_grpc/__generated__/dagster_api_pb2.py")
    spec = importlib.util.spec_from_file_location("_kt_code_server_wire", path)
    if spec is None or spec.loader is None:
        raise ValueError("설치된 Dagster protobuf를 읽을 수 없음")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.ListRepositoriesReply


def _is_loaded_reply(raw: bytes) -> bool:
    if not raw or len(raw) > _MAX_REPLY_BYTES:
        return False
    reply = _reply_class().FromString(raw)
    payload = json.loads(
        reply.serialized_list_repositories_response_or_error,
        object_pairs_hook=_unique_object,
    )
    if not isinstance(payload, dict) or payload.get("__class__") != "ListRepositoriesResponse":
        return False
    symbols = payload.get("repository_symbols")
    if not isinstance(symbols, list) or not isinstance(
        payload.get("repository_code_pointer_dict"), dict
    ):
        return False
    return all(
        isinstance(symbol, dict)
        and symbol.get("__class__") == "LoadableRepositorySymbol"
        and isinstance(symbol.get("repository_name"), str)
        and bool(symbol["repository_name"])
        and isinstance(symbol.get("attribute"), str)
        and bool(symbol["attribute"])
        for symbol in symbols
    )


def code_server_is_healthy(port: int) -> bool:
    """loopback code-server를 RPC 각 4초·수신 4MiB 한도로 점검한다.

    grpc/Dagster 의존성은 호출 때만 필요하다. 프로토콜 변경, 누락된 의존성,
    연결 실패·timeout·유효하지 않은 응답은 모두 False다. 서비스 재시작 정책은
    소비자가 소유하며 이 함수는 프로세스나 run을 변경하지 않는다.
    """
    if type(port) is not int or not 1 <= port <= 65535:
        return False
    try:
        import grpc
        from grpc_health.v1 import health_pb2, health_pb2_grpc

        with grpc.insecure_channel(
            f"127.0.0.1:{port}",
            options=(("grpc.max_receive_message_length", _MAX_REPLY_BYTES),),
        ) as channel:
            health = health_pb2_grpc.HealthStub(channel).Check(
                health_pb2.HealthCheckRequest(service="DagsterApi"), timeout=4
            )
            if health.status != health_pb2.HealthCheckResponse.SERVING:
                return False
            raw = channel.unary_unary("/api.DagsterApi/ListRepositories")(b"", timeout=4)
            return _is_loaded_reply(raw)
    except Exception:
        # health 출력에 자식 load error/연결 설정/비밀값 원문을 내보내지 않는다.
        return False


if __name__ == "__main__":
    valid = len(sys.argv) == 2 and sys.argv[1].isascii() and sys.argv[1].isdigit()
    raise SystemExit(0 if valid and code_server_is_healthy(int(sys.argv[1])) else 1)
