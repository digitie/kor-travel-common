# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"""연속 실패의 정체 시계. Dagster·DB 의존성이 없는 순수 값 객체다.

- `observe_failure`: 같은 key의 실패는 `first_failed_at`과 `alerted_at`을 유지하고 마지막
  실패 서명만 바꾼다. 실패 서명이 바뀌어도(예: timeout → 연결 거부) 정체는 이어진다.
  key가 다르거나 시계가 없으면 새 시계를 시작한다. 성공은 시계를 버리는 것(None)으로 표현한다.
  `first_failed_at`이 `now`보다 미래이면(wall clock이 뒤로 갔거나 저장값이 손상됨) 같은 key라도
  `now`에서 새 시계를 시작한다. 그대로 두면 되돌아간 폭만큼 경보가 억제된다.
- `due_alert`: 첫 실패 뒤 `stall_after`초가 지났고, 아직 경보하지 않았거나 마지막 경보 뒤
  `realert_after`초가 지났으면 True다. `first_failed_at`이 미래이면 경보하지 않는다(다음
  `observe_failure`가 시계를 다시 시작한다). `alerted_at`이 미래이면 경보하지 않은 것으로 본다
  (되돌아간 폭만큼 재경보가 억제되지 않게 한다).
- `to_dict`/`from_dict`: sensor cursor 등에 넣는 고정 4필드 JSON 형태다. key·실패 서명은
  길이 상한이 있으며 실패 서명은 잘라서 보관한다. 소비자는 예외 message 같은 원문 값을
  서명에 넣지 않는다(SQLSTATE·예외 형식 이름 정도로 제한한다).

시각은 epoch 초(float)다. 시계의 저장·경보 전송·소유는 소비자가 맡는다.
"""

import math
from dataclasses import dataclass, replace
from typing import Any

MAX_KEY_CHARS = 200
MAX_FAILURE_CHARS = 200
_FIELDS = ("key", "first_failed_at", "last_failure", "alerted_at")


def _instant(value: object, name: str) -> float:
    if not isinstance(value, bool) and isinstance(value, (int, float)):
        try:
            # float 범위를 넘는 정수는 OverflowError이므로 같은 형식 오류로 바꾼다.
            converted = float(value)
        except OverflowError:
            converted = math.inf
        if math.isfinite(converted):
            return converted
    raise ValueError(f"{name} 값은 유한한 초 단위 숫자여야 합니다.")


def _key(value: object) -> str:
    if not isinstance(value, str) or not value or len(value) > MAX_KEY_CHARS:
        raise ValueError(f"key는 1~{MAX_KEY_CHARS}자 문자열이어야 합니다.")
    return value


def _failure(value: object) -> str:
    if not isinstance(value, str):
        raise ValueError("failure는 문자열이어야 합니다.")
    return value[:MAX_FAILURE_CHARS]


@dataclass(frozen=True)
class StallClock:
    key: str
    first_failed_at: float
    last_failure: str
    alerted_at: float | None = None

    def __post_init__(self) -> None:
        _key(self.key)
        first = _instant(self.first_failed_at, "first_failed_at")
        object.__setattr__(self, "first_failed_at", first)
        object.__setattr__(self, "last_failure", _failure(self.last_failure))
        if self.alerted_at is not None:
            object.__setattr__(self, "alerted_at", _instant(self.alerted_at, "alerted_at"))

    def to_dict(self) -> dict[str, Any]:
        return {
            "key": self.key,
            "first_failed_at": self.first_failed_at,
            "last_failure": self.last_failure,
            "alerted_at": self.alerted_at,
        }

    @classmethod
    def from_dict(cls, value: object) -> "StallClock":
        """`to_dict` 형태만 받는다. 필드 누락·추가·형식 오류는 ValueError다."""
        if not isinstance(value, dict) or set(value) != set(_FIELDS):
            raise ValueError("정체 시계 형태가 유효하지 않습니다.")
        if not isinstance(value["last_failure"], str) or (
            len(value["last_failure"]) > MAX_FAILURE_CHARS
        ):
            raise ValueError("정체 시계의 실패 서명이 유효하지 않습니다.")
        return cls(
            key=value["key"],
            first_failed_at=value["first_failed_at"],
            last_failure=value["last_failure"],
            alerted_at=value["alerted_at"],
        )


def observe_failure(
    clock: StallClock | None, *, key: str, failure: str, now: float
) -> StallClock:
    if clock is None or clock.key != key:
        return StallClock(key=key, first_failed_at=now, last_failure=failure)
    if clock.first_failed_at > _instant(now, "now"):
        # 시계가 뒤로 갔거나 저장값이 손상됐다. 미래 시작 시각은 경보를 억제하므로 다시 시작한다.
        return StallClock(key=key, first_failed_at=now, last_failure=failure)
    return replace(clock, last_failure=failure)


def due_alert(
    clock: StallClock | None,
    *,
    now: float,
    stall_after: float = 900,
    realert_after: float = 3600,
) -> bool:
    now = _instant(now, "now")
    if _instant(stall_after, "stall_after") < 0 or _instant(realert_after, "realert_after") <= 0:
        raise ValueError("stall_after는 0 이상, realert_after는 양수여야 합니다.")
    if clock is None or now - clock.first_failed_at < stall_after:
        return False
    if clock.alerted_at is None or clock.alerted_at > now:
        # 미래 경보 시각(시계 역행·손상)은 경보하지 않은 것으로 본다.
        return True
    return now - clock.alerted_at >= realert_after


def mark_alerted(clock: StallClock, now: float) -> StallClock:
    return replace(clock, alerted_at=now)
