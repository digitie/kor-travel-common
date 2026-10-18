# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"""기존 SDK 호출·보조 API·좌표 순서·오류 비밀 비노출."""

import httpx
import pytest

from kortravelcommon.address_providers import VworldKakaoAddressResolver
from kortravelcommon.reverse_address import AddressTarget, ReverseAddressError


class Vworld:
    calls = []
    fail = False

    def __init__(self, **kwargs):
        assert kwargs["max_retries"] == 0

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        pass

    async def get_address(self, point, **kwargs):
        self.calls.append((point, kwargs))
        if self.fail:
            raise RuntimeError("SECRET-KEY https://provider.invalid/key")
        return {
            "response": {
                "status": "OK",
                "result": [
                    {
                        "type": "road",
                        "text": "신도로 1",
                        "zipcode": "12345",
                        "structure": {"level1": "서울", "level2": "새구", "level4L": "새동"},
                    },
                    {"type": "parcel", "text": "새동 1"},
                ],
            }
        }


def test_vworld_sdk_is_used_and_original_coordinate_order_is_preserved(monkeypatch):
    monkeypatch.setattr(Vworld, "fail", False)
    Vworld.calls = []
    client = VworldKakaoAddressResolver(vworld_key="SECRET", kakao_key=None, vworld_factory=Vworld)
    client._pace = lambda: None
    try:
        result = client.reverse(AddressTarget("a", 127, 37))
        assert Vworld.calls[0][0] == (127, 37)
        assert result["address"]["road_address"] == "신도로 1"
        assert result["address"]["parcel_address"] == "새동 1"
        assert result["region"]["legal_dong"] == "새동"
    finally:
        client.close()


def test_kakao_fallback_queries_address_and_both_region_types(monkeypatch):
    monkeypatch.setattr(Vworld, "fail", True)
    calls = []

    def handler(request):
        calls.append(request)
        assert request.headers["Authorization"] == "KakaoAK SECRET"
        assert request.url.params["x"] == "127"
        if request.url.path.endswith("coord2address.json"):
            return httpx.Response(
                200,
                json={
                    "documents": [
                        {
                            "address": {"address_name": "새동 2", "region_3depth_name": "새동"},
                            "road_address": {"address_name": "새길 2", "zone_no": "12345"},
                        }
                    ]
                },
            )
        return httpx.Response(
            200,
            json={
                "documents": [
                    {"region_type": "B", "code": "1111010100"},
                    {"region_type": "H", "code": "1111051000", "region_3depth_name": "새행정동"},
                ]
            },
        )

    client = VworldKakaoAddressResolver(
        vworld_key="BAD",
        kakao_key="SECRET",
        vworld_factory=Vworld,
        transport=httpx.MockTransport(handler),
    )
    client._pace = lambda: None
    try:
        result = client.reverse(AddressTarget("a", 127, 37))
        assert len(calls) == 2
        assert result["provider"] == "kakao"
        assert result["address"]["admin_dong_code"] == "1111051000"
        assert result["region"]["admin_dong"] == "새행정동"
    finally:
        client.close()


def test_provider_failure_never_leaks_key_or_url(monkeypatch):
    monkeypatch.setattr(Vworld, "fail", True)
    client = VworldKakaoAddressResolver(vworld_key="SECRET", kakao_key=None, vworld_factory=Vworld)
    client._pace = lambda: None
    try:
        with pytest.raises(ReverseAddressError, match="^vworld_failed$"):
            client.reverse(AddressTarget("a", 127, 37))
    finally:
        client.close()


def test_kakao_body_is_bounded_before_loading_json():
    transport = httpx.MockTransport(lambda request: httpx.Response(200, content=b"x" * 131073))
    client = VworldKakaoAddressResolver(vworld_key=None, kakao_key="fixture", transport=transport)
    try:
        with pytest.raises(ReverseAddressError, match="kakao_response_budget"):
            client._kakao_get("coord2address.json", AddressTarget("a", 127, 37))
    finally:
        client.close()


def test_slow_drip_response_has_total_body_deadline(monkeypatch):
    class Chunks(httpx.SyncByteStream):
        def __iter__(self):
            yield b'{"documents":'
            yield b"[]}"

    transport = httpx.MockTransport(lambda request: httpx.Response(200, stream=Chunks()))
    client = VworldKakaoAddressResolver(
        vworld_key=None, kakao_key="fixture", timeout=1, transport=transport
    )
    client._pace = lambda: None
    moments = iter([0.0, 0.1, 2.0])
    monkeypatch.setattr("kortravelcommon.address_providers.time.monotonic", lambda: next(moments))
    try:
        with pytest.raises(ReverseAddressError, match="kakao_deadline"):
            client._kakao_get("coord2address.json", AddressTarget("a", 127, 37))
    finally:
        client.close()


def test_successful_empty_fallback_overrides_primary_failure(monkeypatch):
    monkeypatch.setattr(Vworld, "fail", True)
    client = VworldKakaoAddressResolver(
        vworld_key="fixture",
        kakao_key="fixture",
        vworld_factory=Vworld,
        transport=httpx.MockTransport(lambda request: httpx.Response(200, json={"documents": []})),
    )
    client._pace = lambda: None
    try:
        assert client.reverse(AddressTarget("a", 127, 37)) is None
    finally:
        client.close()


@pytest.mark.parametrize("status_code", [200, 500])
def test_real_sdk_httpx_logs_never_include_provider_key_or_url(caplog, status_code):
    import logging
    from concurrent.futures import ThreadPoolExecutor

    from vworld import VworldClient

    canary = "fixture-canary-never-a-real-key"
    body = {"response": {"status": "OK", "result": [{"type": "road", "text": "fixture road"}]}}

    def handler(request):
        # 같은 프로세스의 다른 thread가 보내는 HTTPX 로그는 그대로 남아야 한다.
        with ThreadPoolExecutor(max_workers=1) as pool:
            pool.submit(logging.getLogger("httpx").info, "parallel-httpx-record").result()
        return httpx.Response(status_code, json=body)

    class Factory:
        def __init__(self, **kwargs):
            self.session = httpx.AsyncClient(
                transport=httpx.MockTransport(handler), trust_env=False
            )
            self.client = VworldClient(**kwargs, session=self.session)

        async def __aenter__(self):
            return self.client

        async def __aexit__(self, *args):
            await self.session.aclose()

    client = VworldKakaoAddressResolver(vworld_key=canary, kakao_key=None, vworld_factory=Factory)
    client._pace = lambda: None
    try:
        with caplog.at_level(logging.INFO, logger="httpx"):
            if status_code == 200:
                assert client.reverse(AddressTarget("a", 127, 37))["provider"] == "vworld"
            else:
                with pytest.raises(ReverseAddressError, match="vworld_failed"):
                    client.reverse(AddressTarget("a", 127, 37))
            logging.getLogger("httpx").info("outside-provider-record")
        assert canary not in caplog.text and "api.vworld.kr" not in caplog.text
        assert "parallel-httpx-record" in caplog.text
        assert "outside-provider-record" in caplog.text
    finally:
        client.close()
