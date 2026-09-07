# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"""사설 주소·내부 호스트·운영 도메인을 전체 Git 작업 트리에서 검사한다."""

from _scan import main


if __name__ == "__main__":
    raise SystemExit(main(".prod-redaction-patterns"))
