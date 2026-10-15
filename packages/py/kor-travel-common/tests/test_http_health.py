# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"""실제 loopback 소켓으로 상태·헤더·전체 시간 제한을 검증한다."""

import contextlib
import socket
import subprocess
import sys
import threading
import time

import pytest

from kortravelcommon.http_health import check_http_health


@contextlib.contextmanager
def server(response: bytes, *, drip: bool = False, hold: bool = False):
    stop = threading.Event()
    requests = []
    errors = []
    with socket.socket() as listener:
        listener.bind(("127.0.0.1", 0))
        listener.listen(1)
        listener.settimeout(2)
        port = listener.getsockname()[1]

        def respond():
            try:
                with listener.accept()[0] as connection:
                    connection.settimeout(2)
                    requests.append(connection.recv(4096))
                    if drip:
                        for value in response:
                            if stop.wait(0.02):
                                break
                            connection.sendall(bytes([value]))
                    else:
                        connection.sendall(response)
                    if hold:
                        stop.wait(2)
            except (BrokenPipeError, ConnectionResetError):
                pass
            except BaseException as error:
                errors.append(error)

        worker = threading.Thread(target=respond, daemon=True)
        worker.start()
        try:
            yield port, requests
        finally:
            stop.set()
            worker.join(3)
            assert not worker.is_alive()
            assert not errors


@pytest.mark.parametrize("status", [200, 204, 206, 299, 100, 302, 304, 401, 404, 503])
def test_actual_status_and_one_request(status):
    # redirect용 Location은 의도적으로 없다. 302 자체가 성공할 수 없다.
    response = f"HTTP/1.1 {status} Test\r\nContent-Length: 0\r\n\r\n".encode()
    with server(response) as (port, requests):
        assert check_http_health(port=port) is (200 <= status < 300)
    assert len(requests) == 1
    assert requests[0].startswith(b"GET /health HTTP/1.0\r\n")


@pytest.mark.parametrize(
    "response",
    [
        b"",
        b"HTTP/1.1 200 OK\r\n",
        b"HTTP/1.1 200 OK\r\nBroken\r\n\r\n",
        b"HTTP/1.1 200 OK\r\nHeader : x\r\n\r\n",
        b"HTTP/1.1 200 OK\r\nHeader: \x00\r\n\r\n",
        b"HTTP/1.1 200 \x00\r\n\r\n",
        b"HTTP/1.1 200 OK\r\nContent-Length: bad\r\n\r\n",
        b"HTTP/1.1 200 OK\r\nContent-Length: 0\r\nContent-Length: 0\r\n\r\n",
        b"HTTP/1.1 200 OK\r\nContent-Length: 0\r\nTransfer-Encoding: chunked\r\n\r\n",
        b"HTTP/1.1 200 OK\r\nTransfer-Encoding: nope\r\n\r\n",
        b"HTTP/1.1 200\r\n\r\n",
        b"HTTP/1.0 204\r\n\r\n",
        b"HTTP/1.1 2000 OK\r\n\r\n",
        b"HTTP/2 200 OK\r\n\r\n",
        b"HTTP/1.1 200 OK\r\nLong:" + b"x" * 16384 + b"\r\n\r\n",
    ],
)
def test_malformed_eof_and_header_cap(response):
    with server(response) as (port, _):
        assert not check_http_health(port=port, timeout_seconds=0.5)


@pytest.mark.parametrize("protocol,status", [("HTTP/1.1", 200), ("HTTP/1.0", 204)])
def test_empty_reason_preserves_required_separator(protocol, status):
    response = f"{protocol} {status} \r\n\r\n".encode()
    with server(response) as (port, _):
        assert check_http_health(port=port)


def test_body_is_not_awaited():
    # 응답 헤더가 완전하면 미전송 본문을 기다리지 않는다.
    response = b"HTTP/1.0 200 OK\r\nContent-Length: 999999999\r\n\r\n"
    with server(response, hold=True) as (port, _):
        start = time.monotonic()
        assert check_http_health(port=port, path="/v1/healthz", timeout_seconds=0.2)
        assert time.monotonic() - start < 0.5


def test_drip_has_one_total_deadline():
    with server(b"HTTP/1.1 200 OK\r\n\r\n", drip=True) as (port, _):
        start = time.monotonic()
        assert not check_http_health(port=port, timeout_seconds=0.08)
        assert time.monotonic() - start < 0.5


def test_closed_port():
    with socket.socket() as listener:
        listener.bind(("127.0.0.1", 0))
        port = listener.getsockname()[1]
    assert not check_http_health(port=port, timeout_seconds=0.2)


@pytest.mark.parametrize(
    "kwargs",
    [
        {"port": True}, {"port": 0}, {"port": 65536}, {"port": 1.0},
        {"port": 1, "path": "health"}, {"port": 1, "path": "/a\r\nb"},
        {"port": 1, "path": "/" + "x" * 2048}, {"port": 1, "path": "/한글"},
        {"port": 1, "timeout_seconds": True}, {"port": 1, "timeout_seconds": 0},
        {"port": 1, "timeout_seconds": float("nan")},
        {"port": 1, "timeout_seconds": float("inf")},
        {"port": 1, "timeout_seconds": 10**1000},
    ],
)
def test_invalid_before_network(monkeypatch, kwargs):
    def forbidden(*args, **kw):
        raise AssertionError("인자 검증 전에 네트워크를 호출함")

    monkeypatch.setattr(socket, "socket", forbidden)
    with pytest.raises(ValueError):
        check_http_health(**kwargs)


@pytest.mark.parametrize("args", [[], ["--port", "bad"], ["--port", "0"], ["--unknown", "x"]])
def test_invalid_cli_is_quiet(args):
    result = subprocess.run(
        [sys.executable, "-m", "kortravelcommon.http_health", *args],
        capture_output=True, timeout=3, check=False,
    )
    assert result.returncode == 2
    assert result.stdout == result.stderr == b""


def test_cli_real_success_and_failure():
    for status in (200, 503):
        with server(f"HTTP/1.1 {status} Test\r\n\r\n".encode()) as (port, _):
            result = subprocess.run(
                [sys.executable, "-m", "kortravelcommon.http_health", "--port", str(port)],
                capture_output=True, timeout=3, check=False,
            )
        assert result.returncode == (0 if status == 200 else 1)
        assert result.stdout == result.stderr == b""
