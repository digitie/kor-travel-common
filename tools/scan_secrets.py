# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"""자격증명 값의 패턴을 검사하고 값 자체는 출력하지 않는다."""

from _scan import main


if __name__ == "__main__":
    raise SystemExit(main(".secret-scan-patterns"))
