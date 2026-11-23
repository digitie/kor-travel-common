# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"""재시도 간격 계산. Dagster·HTTP 의존성이 없는 순수 함수다.

- `backoff_seconds`: `base × 2^(attempt-1)`를 `cap`에서 자른 값에 jitter를 섞는다.
  `jitter`는 무작위로 흩뜨리는 비율이다. 0이면 고정 간격, 1이면 full jitter(0~간격),
  기본 0.5는 간격의 절반은 지키고 나머지 절반만 흩뜨린다(equal jitter). 같은 순간에 실패한
  여러 호출·행이 같은 시각에 다시 몰리지 않게 한다.
- `retry_after_seconds`: HTTP `Retry-After` 값(초 또는 HTTP-date)을 대기 초로 바꾼다.
  해석할 수 없으면 None이다. 상한은 호출자가 정한다(서버 값을 무한정 따르지 않는다).

재시도 여부·횟수·대상 오류의 분류는 호출자가 소유한다.
"""

import math
import random
from email.utils import parsedate_to_datetime
from time import time as wall_clock

__all__ = ["backoff_seconds", "retry_after_seconds"]

_EXPONENT_CAP = 62


def _positive(value: object, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name}는 유한한 양수여야 합니다.")
    if not math.isfinite(value) or value <= 0:
        raise ValueError(f"{name}는 유한한 양수여야 합니다.")
    return float(value)


def backoff_seconds(
    attempt: int,
    *,
    base_seconds: float,
    cap_seconds: float,
    jitter: float = 0.5,
    rng: random.Random | None = None,
) -> float:
    """attempt번째(1부터) 재시도 전 대기 초. 결과는 `[간격×(1-jitter), 간격]` 안이다."""
    if type(attempt) is not int or attempt < 1:
        raise ValueError("attempt는 1 이상의 정수여야 합니다.")
    base = _positive(base_seconds, "base_seconds")
    cap = _positive(cap_seconds, "cap_seconds")
    if base > cap:
        raise ValueError("base_seconds는 cap_seconds 이하여야 합니다.")
    if (
        isinstance(jitter, bool)
        or not isinstance(jitter, (int, float))
        or not 0 <= jitter <= 1
    ):
        raise ValueError("jitter는 0~1 사이 비율이어야 합니다.")
    # 큰 attempt에서도 float overflow 없이 cap으로 수렴한다.
    delay = min(cap, base * 2 ** min(attempt - 1, _EXPONENT_CAP))
    if not jitter:
        return delay
    spread = delay * jitter
    return delay - spread + (rng or random).uniform(0, spread)


def retry_after_seconds(value: str | None, *, now: float | None = None) -> float | None:
    """`Retry-After` 헤더 값을 0 이상의 대기 초로 바꾼다. 없거나 잘못되면 None."""
    if value is None:
        return None
    text = value.strip()
    if not text:
        return None
    if text.isascii() and text.isdecimal():
        # 지나치게 긴 숫자는 의미 있는 대기가 아니다(int 변환 비용도 막는다).
        return float(int(text)) if len(text) <= 9 else None
    try:
        moment = parsedate_to_datetime(text)
    except (TypeError, ValueError, IndexError, OverflowError):
        return None
    if moment is None or moment.tzinfo is None:
        # RFC 9110의 HTTP-date는 GMT다. 시간대 없는 값은 모호하므로 따르지 않는다.
        return None
    current = wall_clock() if now is None else now
    return max(0.0, moment.timestamp() - current)
