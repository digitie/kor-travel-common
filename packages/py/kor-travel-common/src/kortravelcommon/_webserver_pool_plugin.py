# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"""webserver가 오래 쥐는 storage pool에만 SQLAlchemy pool_pre_ping을 켠다.

dagster-postgres 0.29.24/0.29.25의 ``optimize_for_webserver``는 run·event·schedule storage
engine을 ``pool_size=1``·``max_overflow``·``pool_recycle``로 다시 만들지만 pre-ping 키를
받지 않는다. 그래서 PG 재시작·idle 절단 뒤 첫 요청이 끊긴 연결을 받아 실패한다.
이 plugin은 그 재생성 호출(명시 ``pool_size``가 있고 ``poolclass``가 없는 것)에만
``pool_pre_ping=True``를 더한다. 초기 NullPool engine, 연결 확인용 일회 engine, 이미
pre-ping 값을 준 호출은 그대로 둔다. 연결 수·크기·recycle·statement_timeout은 바꾸지 않는다.
"""

from __future__ import annotations

from sqlalchemy.engine import CreateEnginePlugin

PLUGIN_NAME = "kortravel_webserver_pre_ping"


class WebserverPrePingPlugin(CreateEnginePlugin):
    """webserver 최적화 engine에만 checkout 전 연결 검증을 켠다."""

    def __init__(self, url, kwargs):
        super().__init__(url, kwargs)
        self.applied = (
            "pool_size" in kwargs
            and "poolclass" not in kwargs
            and "pool_pre_ping" not in kwargs
        )
        if self.applied:
            kwargs["pool_pre_ping"] = True

    def update_url(self, url):
        return url
