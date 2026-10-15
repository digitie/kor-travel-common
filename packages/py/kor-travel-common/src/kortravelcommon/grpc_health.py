# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"""조회 전용 gRPC 생존/정의 준비 점검. 복구·run 변경·프로세스 관리는 하지 않는다."""

import sys
import time

_MAX_REPLY_BYTES = 4 * 1024 * 1024
_READY_VERSIONS = frozenset({"1.13.24", "1.13.25"})


def _repository_loaded(raw: bytes, expected: str) -> bool:
    # 생존 점검에는 Dagster distribution이나 protobuf 파일이 필요하지 않다.
    import importlib.metadata

    from .dagster_health import _loaded_payload

    if importlib.metadata.version("dagster") not in _READY_VERSIONS:
        return False
    payload = _loaded_payload(raw)
    if payload is None:
        return False
    symbols = payload["repository_symbols"]
    names = [symbol["repository_name"] for symbol in symbols]
    pointers = payload["repository_code_pointer_dict"]
    if len(set(names)) != len(names) or set(names) != set(pointers) or expected not in names:
        return False
    symbol = next(symbol for symbol in symbols if symbol["repository_name"] == expected)
    pointer = pointers[expected]
    return symbol["attribute"] == pointer.get("fn_name", pointer.get("attribute"))


def _probe(port: int, budget: float, repository: str | None) -> bool:
    if (
        type(port) is not int or not 1 <= port <= 65535
        or type(budget) not in (int, float) or not 0 < budget <= 4
    ):
        return False
    deadline = time.monotonic() + budget

    def remaining() -> float:
        left = deadline - time.monotonic()
        if left <= 0:
            raise TimeoutError("공유 점검 예산 초과")
        return left

    try:
        import grpc
        from grpc_health.v1 import health_pb2, health_pb2_grpc

        remaining()
        with grpc.insecure_channel(
            f"127.0.0.1:{port}",
            options=(
                ("grpc.max_receive_message_length", _MAX_REPLY_BYTES),
                ("grpc.enable_retries", 0),
                ("grpc.enable_http_proxy", 0),
            ),
        ) as channel:
            response = health_pb2_grpc.HealthStub(channel).Check(
                health_pb2.HealthCheckRequest(service="DagsterApi"), timeout=remaining()
            )
            remaining()
            result = response.status == health_pb2.HealthCheckResponse.SERVING
            if result and repository is not None:
                raw = channel.unary_unary("/api.DagsterApi/ListRepositories")(
                    b"", timeout=remaining()
                )
                remaining()
                result = _repository_loaded(raw, repository)
                remaining()
        remaining()  # channel 정리 시간까지 초과한 결과는 성공으로 반환하지 않는다.
        return result
    except Exception:
        return False


def grpc_code_server_is_live(port: int, *, timeout_seconds: float = 4.0) -> bool:
    """표준 DagsterApi SERVING만 확인한다. 자식 정의/worker/DB 준비는 보장하지 않는다."""
    return _probe(port, timeout_seconds, None)


def grpc_code_server_is_ready(
    port: int, *, repository_name: str, timeout_seconds: float = 4.0
) -> bool:
    """생존과 기대 저장소의 지원된 정의 응답을 단일 논리 예산으로 확인한다."""
    if not isinstance(repository_name, str) or not repository_name or not repository_name.strip():
        return False
    return _probe(port, timeout_seconds, repository_name)


def main(argv: list[str] | None = None) -> int:
    """기존 CLI와 별개인 quiet CLI. 성공0/조회 실패1/인자 오류2."""
    args = sys.argv[1:] if argv is None else argv
    if (
        len(args) not in (3, 5) or not args[0].isascii() or not args[0].isdigit()
        or len(args[0]) > 5 or args[1] != "--check" or args[2] not in ("live", "ready")
    ):
        return 2
    port = int(args[0])
    if not 1 <= port <= 65535:
        return 2
    if args[2] == "live":
        return (0 if grpc_code_server_is_live(port) else 1) if len(args) == 3 else 2
    if len(args) != 5 or args[3] != "--repository" or not args[4].strip():
        return 2
    return 0 if grpc_code_server_is_ready(port, repository_name=args[4]) else 1


if __name__ == "__main__":
    raise SystemExit(main())
