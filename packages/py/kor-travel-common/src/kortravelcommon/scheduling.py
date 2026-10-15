# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"""명시적인 고정 phase로 일주기를 나누는 순수 cron 생성 함수."""

__all__ = ["staggered_cron"]


def staggered_cron(*, interval_minutes: int, phase_minutes: int) -> str:
    """분/시간 주기의 일일 횟수를 보존한다. 시간대·실행 동시성은 호출자 소유다.

    60분의 약수 또는 60의 배수이면서 1440분의 약수인 주기만 지원한다.
    DST 없는 clock의 자정부터 phase분 뒤에 시작하며 재시작해도 값이 같다.
    """
    if type(interval_minutes) is not int or type(phase_minutes) is not int:
        raise TypeError("주기와 phase는 bool이 아닌 정수여야 한다")
    if interval_minutes <= 0 or not (
        (interval_minutes <= 60 and 60 % interval_minutes == 0)
        or (interval_minutes % 60 == 0 and 1440 % interval_minutes == 0)
    ):
        raise ValueError("주기는 60분의 약수 또는 24시간의 약수인 정시 주기여야 한다")
    if not 0 <= phase_minutes < interval_minutes:
        raise ValueError("phase는 0 이상 주기 미만이어야 한다")
    if interval_minutes < 60:
        return f"{phase_minutes}-59/{interval_minutes} * * * *"
    hour_phase, minute = divmod(phase_minutes, 60)
    hours = ",".join(str(hour) for hour in range(hour_phase, 24, interval_minutes // 60))
    return f"{minute} {hours} * * *"
