# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"""기존 VWorld SDK 우선, Kakao Local 보조의 좌표→주소 소비 경계."""

from __future__ import annotations

import asyncio
import json
import logging
import time
from collections.abc import Callable, Mapping
from contextvars import ContextVar
from typing import Any

import httpx

from .reverse_address import AddressResolver, AddressTarget, ReverseAddressError

_PRIVATE_REQUEST = ContextVar("reverse_address_private_request", default=False)


class _RequestLogFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        # HTTPX는 정상 응답도 query key가 든 URL을 INFO로 기록한다.
        # 해당 요청의 context에서만 저수준 로그를 막고 다른 요청은 보존한다.
        return not _PRIVATE_REQUEST.get()


_REQUEST_LOG_FILTER = _RequestLogFilter()
for _logger_name in (
    "httpx",
    "httpcore.connection",
    "httpcore.http11",
    "httpcore.http2",
    "httpcore.proxy",
    "httpcore.socks",
):
    logging.getLogger(_logger_name).addFilter(_REQUEST_LOG_FILTER)


def _text(value: Any) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str) or len(value) > 1000:
        raise ReverseAddressError("invalid_response")
    return value.strip() or None


class VworldKakaoAddressResolver(AddressResolver):
    """제공자 키·원문 예외는 외부로 노출하지 않는다."""

    provider_id = "vworld-kakao-reverse-v1"

    def __init__(
        self,
        *,
        vworld_key: str | None,
        kakao_key: str | None,
        timeout: float = 5.0,
        vworld_factory: Callable[..., Any] | None = None,
        transport: httpx.BaseTransport | None = None,
    ) -> None:
        if not vworld_key and not kakao_key:
            raise ValueError("VWorld 또는 Kakao 키가 필요합니다.")
        if not 0 < timeout <= 10:
            raise ValueError("주소 조회 timeout은 0초 초과·10초 이하여야 합니다.")
        self.vworld_key, self.kakao_key = vworld_key, kakao_key
        self.timeout = timeout
        self.vworld_factory = vworld_factory
        self._last_request = 0.0
        self._http = httpx.Client(
            timeout=httpx.Timeout(timeout, connect=min(timeout, 2)),
            follow_redirects=False,
            trust_env=False,
            transport=transport,
        )

    def close(self) -> None:
        self._http.close()

    def _pace(self) -> None:
        # SDK/보조 제공자를 합쳐 한 worker가 초당 2회보다 자주 요청하지 않는다.
        time.sleep(max(0, 0.5 - (time.monotonic() - self._last_request)))
        self._last_request = time.monotonic()

    async def _vworld(self, target: AddressTarget) -> dict[str, Any] | None:
        from vworld import (
            VworldClient,
            VworldNoDataError,
            parse_reverse_geocode_response,
            process_reverse_geocode_response,
        )

        factory = self.vworld_factory or VworldClient
        key = self.vworld_key
        try:
            async with factory(
                api_key=key, timeout=self.timeout, max_retries=0, max_rps=2.0
            ) as client:
                raw = await client.get_address(
                    (target.longitude, target.latitude),
                    type="both",
                    zipcode=True,
                    simple=False,
                )
        except VworldNoDataError:
            return None
        processed = process_reverse_geocode_response(parse_reverse_geocode_response(raw))
        if processed.status == "NOT_FOUND":
            return None
        if processed.status != "OK" or not isinstance(processed.result, list):
            raise ReverseAddressError("vworld_invalid_response")
        address: dict[str, str] = {}
        region: dict[str, str] = {}
        for item in processed.result:
            if not isinstance(item, Mapping):
                raise ReverseAddressError("vworld_invalid_response")
            text = _text(item.get("text"))
            kind = str(item.get("type", "")).lower()
            if text and kind in {"road", "parcel"}:
                address[kind + "_address"] = text
            postcode = _text(item.get("zipcode"))
            if postcode:
                address["postal_code"] = postcode
            structure = item.get("structure")
            if isinstance(structure, Mapping):
                for source, name in (
                    ("level1", "sido"),
                    ("level2", "sigungu"),
                    ("level4L", "legal_dong"),
                    ("level4A", "admin_dong"),
                ):
                    value = _text(structure.get(source))
                    if value:
                        region[name] = value
                for source, name in (
                    ("level4LC", "legal_dong_code"),
                    ("level4AC", "admin_dong_code"),
                ):
                    value = _text(structure.get(source))
                    if value:
                        address[name] = value
        full = address.get("road_address") or address.get("parcel_address")
        if not full:
            raise ReverseAddressError("vworld_invalid_response")
        return {"provider": "vworld", "address": {**address, "full": full}, "region": region}

    def _kakao_get(self, path: str, target: AddressTarget) -> dict[str, Any]:
        self._pace()
        deadline = time.monotonic() + self.timeout
        with self._http.stream(
            "GET",
            "https://dapi.kakao.com/v2/local/geo/" + path,
            params={"x": target.longitude, "y": target.latitude, "input_coord": "WGS84"},
            headers={
                "Authorization": "KakaoAK " + str(self.kakao_key),
                "Accept-Encoding": "identity",
            },
        ) as response:
            if response.status_code != 200:
                raise ReverseAddressError(f"kakao_http_{response.status_code}")
            content = bytearray()
            for chunk in response.iter_bytes():
                if time.monotonic() >= deadline:
                    raise ReverseAddressError("kakao_deadline")
                if len(content) + len(chunk) > 131072:
                    raise ReverseAddressError("kakao_response_budget")
                content.extend(chunk)
        result = json.loads(content)
        if not isinstance(result, dict) or not isinstance(result.get("documents"), list):
            raise ReverseAddressError("kakao_invalid_response")
        return result

    def _kakao(self, target: AddressTarget) -> dict[str, Any] | None:
        docs = self._kakao_get("coord2address.json", target)["documents"]
        if not docs:
            return None
        item = docs[0]
        if not isinstance(item, dict):
            raise ReverseAddressError("kakao_invalid_response")
        parcel, road = item.get("address"), item.get("road_address")
        parcel = parcel if isinstance(parcel, dict) else {}
        road = road if isinstance(road, dict) else {}
        address = {
            "parcel_address": _text(parcel.get("address_name")),
            "road_address": _text(road.get("address_name")),
            "postal_code": _text(road.get("zone_no") or parcel.get("zip_code")),
        }
        full = address["road_address"] or address["parcel_address"]
        if not full:
            raise ReverseAddressError("kakao_invalid_response")
        regions = self._kakao_get("coord2regioncode.json", target)["documents"]
        names: dict[str, str | None] = {
            "sido": _text(parcel.get("region_1depth_name")),
            "sigungu": _text(parcel.get("region_2depth_name")),
            "legal_dong": _text(parcel.get("region_3depth_name")),
        }
        for region in regions:
            if not isinstance(region, dict):
                raise ReverseAddressError("kakao_invalid_response")
            code = _text(region.get("code"))
            if region.get("region_type") == "B":
                address["legal_dong_code"] = code
            elif region.get("region_type") == "H":
                address["admin_dong_code"] = code
                names["admin_dong"] = _text(region.get("region_3depth_name"))
        return {
            "provider": "kakao",
            "address": {key: value for key, value in {**address, "full": full}.items() if value},
            "region": {key: value for key, value in names.items() if value},
        }

    def reverse(self, target: AddressTarget) -> dict[str, Any] | None:
        mark = _PRIVATE_REQUEST.set(True)
        try:
            return self._reverse(target)
        finally:
            _PRIVATE_REQUEST.reset(mark)

    def _reverse(self, target: AddressTarget) -> dict[str, Any] | None:
        failure = None
        if self.vworld_key:
            self._pace()
            try:
                return_value = asyncio.run(
                    asyncio.wait_for(self._vworld(target), timeout=self.timeout + 1)
                )
                if return_value is not None:
                    return return_value
            except Exception:
                failure = "vworld_failed"
        if self.kakao_key:
            try:
                # 정상 무결과도 fallback 확인의 완료다. 앞선 VWorld 오류와 구별한다.
                return self._kakao(target)
            except Exception:
                failure = "kakao_failed"
        if failure:
            raise ReverseAddressError(failure) from None
        return None
