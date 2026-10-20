# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"""PostgreSQL 오류의 분류 정보만 driver import 없이 꺼낸다.

예외 연쇄(`exc.orig` → `__cause__` → `__context__`)를 너비 우선으로 따라가며 asyncpg
(`sqlstate`·`constraint_name`·`message`), psycopg 3(`sqlstate`·`diag.constraint_name`·
`diag.message_primary`), psycopg2(`pgcode`·`diag.*`) 속성을 읽는다. SQLAlchemy가 감싼
예외와 asyncpg 어댑터의 번역 예외도 같은 연쇄로 다룬다.

반환값은 SQLSTATE(5자 형식만)·제약 이름·primary message 세 필드뿐이다. `DETAIL`·`HINT`·쿼리·
파라미터·`str(exc)`는 행 값이나 DSN을 담을 수 있으므로 읽지 않는다. primary message도
서버가 만든 문장이므로 로그·경보에 넣을지는 소비자가 정한다.
"""

import re
from collections import deque
from dataclasses import dataclass

_MAX_CHAIN = 32
_MAX_TEXT = 500
_SQLSTATE = re.compile(r"[0-9A-Z]{5}")


@dataclass(frozen=True)
class PgErrorInfo:
    sqlstate: str
    constraint: str | None = None
    message: str | None = None


def _text(value: object) -> str | None:
    if not isinstance(value, str) or not value:
        return None
    return value[:_MAX_TEXT]


def _attr(obj: object, name: str) -> object:
    try:
        return getattr(obj, name, None)
    except Exception:
        # driver 속성 접근이 실패해도 원래 예외 처리를 방해하지 않는다.
        return None


def _code(value: object) -> str | None:
    # SQLSTATE 형식(5자 대문자·숫자)만 받는다. 다른 라이브러리의 자유 문자열을 싣지 않는다.
    return value if isinstance(value, str) and _SQLSTATE.fullmatch(value) else None


def _sqlstate(exc: BaseException) -> str | None:
    return _code(_attr(exc, "sqlstate")) or _code(_attr(exc, "pgcode"))


def _constraint(exc: BaseException) -> str | None:
    return _text(_attr(exc, "constraint_name")) or _text(
        _attr(_attr(exc, "diag"), "constraint_name")
    )


def _message(exc: BaseException) -> str | None:
    # asyncpg 예외의 message는 primary message다. psycopg는 diag에 둔다.
    return _text(_attr(_attr(exc, "diag"), "message_primary")) or (
        _text(_attr(exc, "message")) if _code(_attr(exc, "sqlstate")) else None
    )


def _chain(exc: BaseException) -> list[BaseException]:
    seen: set[int] = set()
    ordered: list[BaseException] = []
    queue: deque[object] = deque([exc])
    while queue and len(ordered) < _MAX_CHAIN:
        current = queue.popleft()
        if not isinstance(current, BaseException) or id(current) in seen:
            continue
        seen.add(id(current))
        ordered.append(current)
        queue.extend((_attr(current, "orig"), current.__cause__, current.__context__))
    return ordered


def pg_error_info(exc: BaseException) -> PgErrorInfo | None:
    """연쇄에서 처음 발견한 SQLSTATE와, 같은 SQLSTATE를 가진 예외의 제약·message를 반환한다.

    SQLSTATE가 다른 예외(예: 오류 처리 중 새로 난 예외)의 필드는 섞지 않는다.
    PostgreSQL 오류가 없으면 None이다.
    """
    chain = _chain(exc)
    sqlstate = next((code for code in map(_sqlstate, chain) if code), None)
    if sqlstate is None:
        return None
    same = [item for item in chain if _sqlstate(item) == sqlstate]
    return PgErrorInfo(
        sqlstate=sqlstate,
        constraint=next((value for value in map(_constraint, same) if value), None),
        message=next((value for value in map(_message, same) if value), None),
    )
