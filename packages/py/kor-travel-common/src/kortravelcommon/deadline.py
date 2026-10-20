# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
# Origin: kor-travel-weather@5da6e15 packages/kor-travel-weather-dagster/src/kortravelweather_dagster/external_weather.py
# 원천 경로를 정확히 보존하는 출처 주석은 한 줄 길이 예외다.
# ruff: noqa: E501
# Modified: 2026-10-04 — provider 의존성을 제거하고 유한한 대기 상한과 오류 계약으로 추출
# Modified: 2026-10-21 — 호출자 전용 slot semaphore 주입 추가
"""동기 호출의 대기 상한. 중단된 호출이 있는 객체는 재사용하지 않는다."""

import math
import threading
from collections.abc import Callable
from typing import TypeVar

T = TypeVar("T")
_CALL_SLOTS = threading.BoundedSemaphore(4)


class DeadlineExceeded(TimeoutError):
    """호출은 아직 살아 있을 수 있다. 소비자는 해당 실행을 즉시 끝내야 한다."""


def call_with_deadline(
    call: Callable[[], T],
    *,
    timeout_seconds: float,
    slots: threading.BoundedSemaphore | None = None,
) -> T:
    """daemon thread로 대기만 제한한다. thread 강제 종료를 보장하지 않는다.

    timeout 뒤 같은 client를 닫거나 다음 요청에 사용하면 경합이 생긴다.
    worker process 종료는 Dagster run monitoring/launcher가 소유한다.
    slots를 주면 프로세스 공용 4-slot 대신 그 semaphore를 같은 의미로 사용한다.
    가득 차 있으면 즉시 DeadlineExceeded이고, 끝나지 않은 thread는 종료까지 slot을 보유한다.
    """
    if not math.isfinite(timeout_seconds) or timeout_seconds <= 0:
        raise ValueError("timeout_seconds는 유한한 양수여야 합니다.")
    # timeout된 호출도 실제 종료 전까지 slot을 보유한다. 장수 sensor에서 thread가
    # 무한히 쌓이지 않으며, 용량 부족은 확인 실패로 전달하여 중복 예약을 막는다.
    call_slots = _CALL_SLOTS if slots is None else slots
    if not call_slots.acquire(blocking=False):
        if slots is None:
            raise DeadlineExceeded("아직 종료하지 않은 호출이 프로세스 상한(4개)에 도달했습니다.")
        raise DeadlineExceeded("아직 종료하지 않은 호출이 지정한 slot을 모두 점유하고 있습니다.")
    values: list[T] = []
    errors: list[BaseException] = []

    def invoke() -> None:
        try:
            values.append(call())
        except BaseException as exc:
            errors.append(exc)
        finally:
            call_slots.release()

    worker = threading.Thread(target=invoke, name="bounded-call", daemon=True)
    try:
        worker.start()
    except BaseException:
        call_slots.release()
        raise
    worker.join(timeout_seconds)
    if worker.is_alive():
        raise DeadlineExceeded("호출이 대기 상한을 초과했습니다.")
    if errors:
        raise errors[0]
    return values[0]
