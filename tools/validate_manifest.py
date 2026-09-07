# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"""kor-travel-common 소비자 매니페스트 v1 strict 검증기."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

try:
    from manifest_schema import MANIFEST_SCHEMA, validate_manifest_file
except ImportError:  # tests and imports from the repository root
    from tools.manifest_schema import MANIFEST_SCHEMA, validate_manifest_file


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path, help="검사할 kor-travel-common.lock.json")
    parser.add_argument(
        "--registry",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "versions.json",
        help="정식 repo key를 확인할 versions.json",
    )
    args = parser.parse_args(argv)
    errors = validate_manifest_file(args.manifest, args.registry.resolve())
    if errors:
        print(f"validate_manifest: {MANIFEST_SCHEMA} 오류 {len(errors)}건")
        for error in errors:
            print(f"ERROR {error}")
        return 1
    print(f"validate_manifest: {MANIFEST_SCHEMA} 통과")
    return 0


if __name__ == "__main__":
    sys.exit(main())
