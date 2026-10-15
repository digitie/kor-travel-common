# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"""프레임워크 없이 loopback HTTP 헤더만 확인하는 생존 점검."""

import math
import socket
import time

_HEADER_LIMIT = 16 * 1024
_TOKEN = frozenset(b"!#$%&'*+-.^_`|~0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")


def check_http_health(*, port: int, path: str = "/health", timeout_seconds: float = 4.0) -> bool:
    """GET 한 번의 완전한2xx 헤더를 유한 예산·메모리로 확인한다.

    IPv4 loopback 전용이며 redirect·재시도·본문 검증은 하지 않는다.
    인자가 잘못되면 ValueError, 연결·프로토콜·시간 제한 오류이면 False다.
    """
    if isinstance(port, bool) or not isinstance(port, int) or not 1 <= port <= 65535:
        raise ValueError("port는1~65535 정수여야 합니다.")
    if (
        not isinstance(path, str)
        or not path.startswith("/")
        or len(path) > 2048
        or any(not 33 <= ord(char) <= 126 for char in path)
    ):
        raise ValueError("path는 공백 없는 ASCII 절대 경로여야 합니다.")
    if (
        isinstance(timeout_seconds, bool)
        or not isinstance(timeout_seconds, (int, float))
        or not 0 < timeout_seconds <= 60
        or not math.isfinite(timeout_seconds)
    ):
        raise ValueError("timeout_seconds는0초 초과60초 이하의 유한한 수여야 합니다.")
    deadline = time.monotonic() + timeout_seconds

    def remaining() -> float:
        seconds = deadline - time.monotonic()
        if seconds <= 0:
            raise TimeoutError
        return seconds

    request = (
        f"GET {path} HTTP/1.0\r\nHost: 127.0.0.1:{port}\r\nConnection: close\r\n\r\n"
    ).encode("ascii")
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as connection:
            connection.settimeout(remaining())
            connection.connect(("127.0.0.1", port))
            connection.settimeout(remaining())
            connection.sendall(request)
            header = bytearray()
            while b"\r\n\r\n" not in header:
                if len(header) == _HEADER_LIMIT:
                    return False
                connection.settimeout(remaining())
                chunk = connection.recv(min(1024, _HEADER_LIMIT - len(header)))
                if not chunk:
                    return False
                header.extend(chunk)
            lines = bytes(header).split(b"\r\n\r\n", 1)[0].split(b"\r\n")
            status = lines[0].split(b" ", 2)
            if (
                len(status) != 3
                or status[0] not in (b"HTTP/1.0", b"HTTP/1.1")
                or len(status[1]) != 3
                or not status[1].isdigit()
                or not 200 <= int(status[1]) < 300
                or any(char < 32 and char != 9 or char == 127 for char in lines[0])
            ):
                return False
            framing: dict[bytes, bytes] = {}
            for line in lines[1:]:
                name, separator, value = line.partition(b":")
                if (
                    not separator
                    or not name
                    or any(char not in _TOKEN for char in name)
                    or any(char < 32 and char != 9 or char == 127 for char in value)
                ):
                    return False
                key = name.lower()
                if key in (b"content-length", b"transfer-encoding"):
                    if key in framing:
                        return False
                    framing[key] = value.strip()
            if b"content-length" in framing:
                if not framing[b"content-length"].isdigit() or b"transfer-encoding" in framing:
                    return False
            if (
                b"transfer-encoding" in framing
                and framing[b"transfer-encoding"].lower() != b"chunked"
            ):
                return False
            return time.monotonic() <= deadline
    except OSError:
        return False


def main() -> int:
    """CLI는 판정만 종료 코드로 전달하고 응답·오류 내용을 출력하지 않는다."""
    import argparse

    class QuietParser(argparse.ArgumentParser):
        def error(self, message: str) -> None:
            raise ValueError

    parser = QuietParser(description=__doc__)
    parser.add_argument("--port", type=int, required=True)
    parser.add_argument("--path", default="/health")
    parser.add_argument("--timeout-seconds", type=float, default=4.0)
    try:
        args = parser.parse_args()
        healthy = check_http_health(
            port=args.port, path=args.path, timeout_seconds=args.timeout_seconds
        )
    except ValueError:
        return 2
    return 0 if healthy else 1


if __name__ == "__main__":
    raise SystemExit(main())
