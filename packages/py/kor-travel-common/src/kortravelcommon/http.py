# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"""공용 Dagster 조회의 압축·응답 크기·전체 대기 예산을 제한한다.

인증, URL 허용목록, GraphQL 계약과 재시도 여부는 소비자가 소유한다.
"""

from __future__ import annotations

import asyncio
import math
from typing import Any

import httpx

DEFAULT_RESPONSE_LIMIT = 4 * 1024 * 1024
DEFAULT_TOTAL_TIMEOUT_SECONDS = 10.0


class BoundedResponseError(httpx.RequestError):
    """본문을 누적하기 전에 압축·크기 상한 위반을 알린다."""


async def bounded_request(
    client: httpx.AsyncClient,
    method: str,
    url: str,
    *,
    max_response_bytes: int = DEFAULT_RESPONSE_LIMIT,
    total_timeout_seconds: float = DEFAULT_TOTAL_TIMEOUT_SECONDS,
    **kwargs: Any,
) -> httpx.Response:
    """작은 plain HTTP 응답만 읽는다. redirect·자동 재시도는 허용하지 않는다.

    성공/오류 status 모두 같은 body cap을 갖는다. HTTP status와 JSON 의미 판정은
    호출자가 맡는다. 압축 헤더는 디코더가 body를 읽기 전에 거부한다. 소켓 timeout과
    별개인 전체 deadline으로 매번 조금씩 도착하는 응답도 무한 대기하지 않는다.
    정리에 최대 50ms를 추가로 허용한다. 표준 HTTPX 또는 취소에 협조하는 transport만
    지원하며 취소를 억제하는 임의 transport의 종료는 보장할 수 없다. HTTPX auth flow와
    response hook는 허용하지 않으며 인증 header·client 수명은 소비자가 관리한다.
    """
    if type(max_response_bytes) is not int or max_response_bytes <= 0:
        raise ValueError("응답 상한은 양의 정수여야 합니다.")
    if (
        isinstance(total_timeout_seconds, bool)
        or not isinstance(total_timeout_seconds, (int, float))
        or not math.isfinite(total_timeout_seconds)
        or total_timeout_seconds <= 0
    ):
        raise ValueError("전체 timeout은 유한한 양수여야 합니다.")
    if client.event_hooks.get("response"):
        # response hook는 send(stream=True)에서도 cap 검사보다 먼저 본문을 읽을 수 있다.
        raise BoundedResponseError("응답 hook가 있는 client는 허용하지 않습니다.")
    if kwargs.pop("auth", None) is not None:
        raise BoundedResponseError("인증은 요청 header로 주입해야 합니다.")
    headers = httpx.Headers(kwargs.pop("headers", None))
    headers["Accept-Encoding"] = "identity"
    kwargs.pop("follow_redirects", None)
    request = client.build_request(method, url, headers=headers, **kwargs)
    response: httpx.Response | None = None
    completed = False
    try:
        async with asyncio.timeout(total_timeout_seconds):
            # 기본 DigestAuth 등은 중간 401 body를 cap 이전에 materialize한다.
            response = await client.send(request, auth=None, follow_redirects=False, stream=True)
            encoding = response.headers.get("content-encoding", "identity")
            if encoding.strip().lower() not in {"", "identity"}:
                raise BoundedResponseError("압축 응답은 허용하지 않습니다.", request=request)
            length = response.headers.get("content-length")
            if length is not None:
                try:
                    declared = int(length)
                except ValueError as exc:
                    raise BoundedResponseError(
                        "응답 길이 헤더가 올바르지 않습니다.", request=request
                    ) from exc
                if declared < 0 or declared > max_response_bytes:
                    raise BoundedResponseError("응답이 크기 상한을 초과했습니다.", request=request)
            content = bytearray()
            # Response.aiter_bytes는 EOF에서 aclose를 내부 await하므로 raw stream을
            # 직접 소비하고 close는 별도의 작은 예산으로 실행한다(identity만 허용).
            stream = response.stream
            if not isinstance(stream, httpx.AsyncByteStream):
                raise BoundedResponseError("비동기 응답 stream이 아닙니다.", request=request)
            async for chunk in stream:
                if len(content) + len(chunk) > max_response_bytes:
                    raise BoundedResponseError("응답이 크기 상한을 초과했습니다.", request=request)
                content.extend(chunk)
            completed = True
            return httpx.Response(
                response.status_code,
                headers=response.headers,
                content=bytes(content),
                request=request,
            )
    except TimeoutError as exc:
        raise httpx.ReadTimeout("응답 전체 대기 상한을 초과했습니다.", request=request) from exc
    finally:
        if response is not None:
            # 읽기 예산과 별도로 정리에 최대 50ms를 허용한다. 소비자는 표준 HTTPX
            # transport 또는 취소에 협조하는 transport를 사용하고 client 수명을 관리한다.
            try:
                await asyncio.wait_for(response.aclose(), timeout=0.05)
            except Exception as exc:
                if completed:
                    raise BoundedResponseError(
                        "응답 정리를 완료하지 못했습니다.", request=request
                    ) from exc
                # 본문 실패/외부 취소는 원래 예외를 보존한다. 소비자는 RequestError 뒤
                # client를 폐기하므로 이 경로를 정상 응답·재사용 가능 상태로 해석하지 않는다.
