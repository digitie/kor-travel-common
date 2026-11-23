# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
import pytest

import kortravelcommon.dagster as recovery


@pytest.fixture(autouse=True)
def immediate_failure_events(monkeypatch):
    """시험은 방금 만든 실패 event를 바로 판정한다. settle 대기는 전용 시험에서만 켠다."""
    monkeypatch.setattr(recovery, "FAILURE_SETTLE_SECONDS", 0)
