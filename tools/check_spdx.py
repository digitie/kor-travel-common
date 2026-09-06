# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"""소스의 선두 주석 헤더와 PROVENANCE 색인을 읽기 전용으로 대조한다."""

from __future__ import annotations

import argparse
from datetime import date
import os
from pathlib import Path, PurePosixPath
import re


SUFFIXES = {".ts", ".tsx", ".js", ".mjs", ".cjs", ".css", ".py", ".toml",
            ".yml", ".yaml", ".sh"}
EXCLUDED_DIRS = {".git", ".venv", "venv", "node_modules", "__pycache__", "dist",
                 "build", ".next", ".turbo", "coverage", "LICENSES"}
LICENSES = {"GPL-3.0-or-later", "GPL-3.0-only",
            "GPL-3.0-or-later AND GPL-3.0-only"}
ORIGIN = re.compile(r"(?P<repo>[\w.-]+(?:/[\w.-]+)?)@(?P<sha>[0-9a-f]{7,40}) "
                    r"(?P<path>[^\s()]+)(?: \((?P<license>[^()]+)\))?")
FIELDS = re.compile(r"^(SPDX-License-Identifier|SPDX-FileCopyrightText|Origin|"
                    r"Derived-From|Modified):\s*(.*)$")


def is_source(path: Path) -> bool:
    """고정 제외 목록 밖의 소스·설정 파일을 선택한다."""
    return (not any(part in EXCLUDED_DIRS for part in path.parts)
            and ".gen." not in path.name and not path.name.endswith(".d.ts")
            and (path.suffix in SUFFIXES or path.name == ".editorconfig")
            and not path.name.endswith(".lock") and path.name != "pnpm-lock.yaml")


def source_files(root: Path) -> list[Path]:
    """심볼릭 링크는 따라가지 않으며 선택된 링크는 호출자가 오류로 판정한다."""
    found = []

    def fail(error: OSError) -> None:
        raise error

    for directory, dirs, files in os.walk(root, onerror=fail, followlinks=False):
        dirs[:] = sorted(name for name in dirs if name not in EXCLUDED_DIRS)
        for name in dirs:
            path = Path(directory) / name
            if path.is_symlink():
                raise ValueError(f"심볼릭 링크 디렉터리는 검사할 수 없음: {path.relative_to(root)}")
        for name in sorted(files):
            path = Path(directory) / name
            if is_source(path.relative_to(root)):
                found.append(path)
    return sorted(found)


def first_comment(text: str, suffix: str) -> list[str]:
    """문자열·docstring·뒤쪽 주석을 헤더로 오인하지 않는다."""
    lines = text.lstrip("\ufeff\r\n \t").splitlines()
    if lines and lines[0].startswith("#!") and suffix in {".py", ".sh", ".js", ".mjs", ".cjs"}:
        lines = lines[1:]
    result = []
    block = False
    slash = suffix in {".ts", ".tsx", ".js", ".mjs", ".cjs", ".css"}
    for line in lines:
        value = line.strip()
        if not block:
            if slash and value.startswith("/*"):
                block = True
                value = value[2:]
            elif slash and suffix != ".css" and value.startswith("//"):
                result.append(value[2:].strip())
                continue
            elif not slash and value.startswith("#"):
                result.append(value[1:].strip())
                continue
            else:
                break
        if "*/" in value:
            value, tail = value.split("*/", 1)
            result.append(value.strip().lstrip("*").strip())
            block = False
            if tail.strip():
                break
        else:
            result.append(value.strip().lstrip("*").strip())
    return [] if block else result


def provenance(root: Path) -> dict[str, tuple[str, str, str, bool, bool, bool]]:
    """색인의 명시적 소스 경로를 읽는다. 문서 파일군은 검사 범위 밖이다."""
    text = (root / "PROVENANCE.md").read_text(encoding="utf-8-sig")
    source_names = {path.relative_to(root).as_posix() for path in source_files(root)}
    entries = {}
    for line in text.splitlines():
        if not re.match(r"\s*\|\s*PV-", line):
            continue
        cells = [part.strip() for part in line.strip().strip("|").split("|")]
        if len(cells) != 8:
            raise ValueError("PROVENANCE: PV 행은 8열이어야 함")
        _, files, repo, sha, original, license_text, modified, _ = cells
        sha = sha.strip("`")
        if not re.fullmatch(r"[0-9a-f]{7,40}", sha):
            raise ValueError(f"PROVENANCE: 커밋 형식 오류: {cells[0]}")
        paths = re.findall(r"`([^`]+)`", files)
        if not paths:
            raise ValueError(f"PROVENANCE: 명시적 파일 경로 없음: {cells[0]}")
        for name in paths:
            path = PurePosixPath(name)
            if path.is_absolute() or ".." in path.parts or "\\" in name or ":" in name:
                raise ValueError(f"PROVENANCE: 저장소 상대 경로가 아님: {name}")
            if name != path.as_posix():
                raise ValueError(f"PROVENANCE: 정규 상대 경로가 아님: {name}")
            if not is_source(Path(name)):
                continue
            if name in entries:
                raise ValueError(f"PROVENANCE: 소스 경로 중복: {name}")
            if not (root / name).is_file():
                raise ValueError(f"PROVENANCE: 소스 파일 없음: {name}")
            if name not in source_names:
                raise ValueError(f"PROVENANCE: 실제 소스 경로의 대소문자와 불일치: {name}")
            origins = re.findall(r"`([^`]+)`", original)
            if len(origins) != 1:
                raise ValueError(f"PROVENANCE: 소스는 행마다 원천 경로 하나 필요: {name}")
            entries[name] = (repo.strip("`"), sha, origins[0],
                             not modified.startswith("없음"), "파생" in license_text,
                             "GPL-3.0-only" in license_text)
    return entries


def check_file(path: Path, root: Path, entries: dict) -> list[str]:
    """파일 하나의 오류 메시지를 반환한다. 소스 내용을 출력하지 않는다."""
    if path.is_symlink():
        return ["심볼릭 링크 소스는 검사할 수 없음"]
    text = path.read_text(encoding="utf-8-sig")
    fields: dict[str, list[str]] = {}
    for line in first_comment(text, path.suffix):
        match = FIELDS.fullmatch(line)
        if match:
            fields.setdefault(match[1], []).append(match[2])
    errors = []
    for key in ("SPDX-License-Identifier", "SPDX-FileCopyrightText"):
        if not fields.get(key) or any(not value for value in fields[key]):
            errors.append(f"선두 주석의 {key} 누락 또는 빈 값")
    for value in fields.get("SPDX-License-Identifier", []):
        if value not in LICENSES:
            errors.append("허용되지 않은 SPDX 라이선스 식별자")
    if re.search(r"Hallmark\s*·", text):
        errors.append("금지된 Hallmark 스탬프")
    entry = entries.get(path.relative_to(root).as_posix())
    origins = fields.get("Origin", [])
    if entry and len(origins) != 1:
        errors.append("이식 소스의 Origin은 정확히 하나 필요")
    if origins and not entry:
        errors.append("Origin에 대응하는 PROVENANCE 소스 행 없음")
    for value in origins:
        match = ORIGIN.fullmatch(value)
        if not match or any(part in {"..", ""} for part in value.split(" ")[1].split("/")):
            errors.append("Origin 형식은 저장소@커밋 원천상대경로 (선택 라이선스)")
            continue
        source = PurePosixPath(match["path"])
        if source.is_absolute() or "\\" in match["path"] or ":" in match["path"]:
            errors.append("Origin 원천 경로는 저장소 상대 경로여야 함")
        if entry and (match["repo"] != entry[0] or match["path"] != entry[2]
                      or not (match["sha"].startswith(entry[1]) or entry[1].startswith(match["sha"]))):
            errors.append("Origin과 PROVENANCE의 저장소·커밋·경로 불일치")
        if (match["repo"].rsplit("/", 1)[-1].casefold() == "kor-travel-geo"
                or match["license"] == "GPL-3.0-only" or (entry and entry[5])):
            if not any("GPL-3.0-only" in item for item in fields.get("SPDX-License-Identifier", [])):
                errors.append("geo 또는 GPL-3.0-only 원천의 -only 식별자 누락")
    if entry and entry[3] and not fields.get("Modified"):
        errors.append("수정 이식 소스의 Modified 누락")
    if entry and entry[4] and not fields.get("Derived-From"):
        errors.append("서드파티 파생 소스의 Derived-From 누락")
    for value in fields.get("Derived-From", []):
        if not value:
            errors.append("Derived-From 빈 값")
    for value in fields.get("Modified", []):
        try:
            date.fromisoformat(value[:10])
            if not value[10:].strip(" —-"):
                raise ValueError
        except ValueError:
            errors.append("Modified는 ISO 날짜와 수정 요약 필요")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1],
                        help="PROVENANCE.md가 있는 검사 대상 저장소")
    root = parser.parse_args().root.resolve()
    try:
        entries = provenance(root)
        files = source_files(root)
        if not files:
            raise ValueError("검사 대상 0개: 통과로 판정할 수 없음")
        errors = []
        for path in files:
            for error in check_file(path, root, entries):
                errors.append(f"{path.relative_to(root).as_posix()}: {error}")
    except (OSError, UnicodeError, ValueError) as error:
        print(f"SPDX 검사 오류: {error}")
        return 1
    for error in errors:
        print(error)
    print(f"SPDX 검사: {len(files)}개 파일, 오류 {len(errors)}개")
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
