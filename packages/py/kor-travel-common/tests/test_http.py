# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"""압축 폭주·chunked 누적·trickle 응답과 오류 응답의 동일 상한을 검증한다."""

import asyncio

import httpx
import pytest

from kortravelcommon.http import BoundedResponseError, bounded_request


class Chunks(httpx.AsyncByteStream):
    def __init__(self, chunks, delay=0):
        self.chunks = chunks
        self.delay = delay
        self.reads = 0
        self.closed = False

    async def __aiter__(self):
        for chunk in self.chunks:
            self.reads += 1
            if self.delay:
                await asyncio.sleep(self.delay)
            yield chunk

    async def aclose(self):
        self.closed = True


def run(stream, *, headers=None, status=200, **options):
    async def request():
        def handler(req):
            assert req.headers["Accept-Encoding"] == "identity"
            return httpx.Response(status, stream=stream, headers=headers)

        async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
            return await bounded_request(client, "POST", "http://example.test/graphql", **options)

    return asyncio.run(request())


def test_chunked_limit_and_close():
    stream = Chunks([b"x" * 65536] * 100)
    with pytest.raises(BoundedResponseError, match="크기 상한"):
        run(stream, max_response_bytes=65536)
    assert stream.reads == 2 and stream.closed


@pytest.mark.parametrize("encoding", ["gzip", "br", "deflate", "gzip, identity"])
def test_compression_rejected_before_decode(encoding):
    stream = Chunks([b"invalid compressed payload"])
    with pytest.raises(BoundedResponseError, match="압축"):
        run(stream, headers={"Content-Encoding": encoding})
    assert stream.reads == 0 and stream.closed


@pytest.mark.parametrize("length", ["100000000", "-1", "bad"])
def test_declared_size_rejected_before_read(length):
    stream = Chunks([b"x"])
    with pytest.raises(BoundedResponseError):
        run(stream, headers={"Content-Length": length})
    assert stream.reads == 0 and stream.closed


def test_trickle_response_has_total_deadline():
    stream = Chunks([b"x"] * 100, delay=0.02)
    with pytest.raises(httpx.ReadTimeout, match="전체 대기"):
        run(stream, total_timeout_seconds=0.06)
    assert stream.reads < 100 and stream.closed


def test_error_status_is_returned_with_same_size_bound():
    response = run(Chunks([b'{"error":"unauthorized"}']), status=401)
    assert response.status_code == 401 and response.json()["error"] == "unauthorized"
    with pytest.raises(BoundedResponseError):
        run(Chunks([b"x" * 65536] * 2), status=500, max_response_bytes=65536)


def test_redirect_is_not_followed():
    response = run(Chunks([b""]), status=302, headers={"Location": "http://other.test"})
    assert response.status_code == 302


@pytest.mark.parametrize("value", [0, -1, True, 1.5])
def test_invalid_body_limit(value):
    with pytest.raises(ValueError):
        run(Chunks([]), max_response_bytes=value)


@pytest.mark.parametrize("value", [0, -1, True, float("nan"), float("inf")])
def test_invalid_total_deadline(value):
    with pytest.raises(ValueError):
        run(Chunks([]), total_timeout_seconds=value)


def test_digest_challenge_does_not_read_unbounded_intermediate_response():
    stream = Chunks([b"x" * 65536] * 100)
    calls = 0

    async def request():
        def handler(req):
            nonlocal calls
            calls += 1
            return httpx.Response(
                401,
                headers={
                    "WWW-Authenticate": (
                        'Digest realm="test", nonce="abc", qop="auth", algorithm=MD5'
                    )
                },
                stream=stream,
            )

        async with httpx.AsyncClient(
            transport=httpx.MockTransport(handler), auth=httpx.DigestAuth("admin", "test")
        ) as client:
            return await bounded_request(
                client, "GET", "http://example.test", max_response_bytes=1024
            )

    with pytest.raises(BoundedResponseError):
        asyncio.run(request())
    assert calls == 1 and stream.reads == 1 and stream.closed


def test_response_hook_cannot_read_body_before_cap():
    called = False

    async def hook(response):
        nonlocal called
        called = True
        await response.aread()

    async def request():
        async with httpx.AsyncClient(event_hooks={"response": [hook]}) as client:
            await bounded_request(client, "GET", "http://example.test")

    with pytest.raises(BoundedResponseError, match="hook"):
        asyncio.run(request())
    assert not called


def test_slow_cooperative_cleanup_has_separate_bounded_budget():
    import time

    class SlowClose(Chunks):
        async def aclose(self):
            await asyncio.sleep(1)
            self.closed = True

    stream = SlowClose([b"x"] * 100, delay=0.02)
    start = time.monotonic()
    with pytest.raises(httpx.ReadTimeout) as caught:
        run(stream, total_timeout_seconds=0.04)
    assert caught.value.request.url == "http://example.test/graphql"
    assert time.monotonic() - start < 0.25


def test_cleanup_failure_never_returns_healthy_response():
    class SlowClose(Chunks):
        async def aclose(self):
            await asyncio.sleep(1)
            self.closed = True

    stream = SlowClose([b"{}"])
    with pytest.raises(BoundedResponseError, match="정리"):
        run(stream)
    assert not stream.closed
