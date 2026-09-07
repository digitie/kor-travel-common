# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"""tokens 별칭 CSS의 참조·네임스페이스·중복 선언을 읽기 전용으로 검사한다."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import re
import sys


CUSTOM_PROPERTY = re.compile(r"(?<![a-zA-Z0-9_-])(--[a-zA-Z0-9_-]+)\s*:\s*([^;{}]+);")
KT_REFERENCE = re.compile(r"var\(\s*(--kt-[a-zA-Z0-9_-]+)")
IMPORT = re.compile(r'(?m)^\s*@import\s+["\']([^"\']+)["\']\s*;')
THEME_NAMESPACES = ("--color-", "--spacing-", "--radius-", "--text-", "--font-")


@dataclass(frozen=True)
class Definition:
    name: str
    value: str
    path: Path
    line: int


def without_comments(text: str) -> str:
    """CSS 블록 주석을 제거해 주석 안의 가짜 선언을 검사하지 않는다."""
    return re.sub(r"/\*.*?\*/", "", text, flags=re.DOTALL)


def definitions(path: Path) -> list[Definition]:
    """한 CSS 파일의 custom property 선언과 행을 읽는다."""
    text = without_comments(path.read_text(encoding="utf-8-sig"))
    result = []
    for match in CUSTOM_PROPERTY.finditer(text):
        result.append(Definition(
            match.group(1), match.group(2).strip(), path,
            text.count("\n", 0, match.start()) + 1,
        ))
    return result


def imports(path: Path) -> list[Path]:
    """상대 CSS import를 읽고 패키지 밖 경로는 호출자에게 오류로 넘긴다."""
    text = without_comments(path.read_text(encoding="utf-8-sig"))
    return [path.parent / target for target in IMPORT.findall(text)]


def package_root(alias_dir: Path) -> Path:
    """aliases 디렉터리에서 tokens 패키지 루트를 계산한다."""
    return alias_dir.resolve().parent


def collect_imports(path: Path, root: Path, seen: set[Path] | None = None) -> tuple[list[Path], list[str]]:
    """별칭 CSS의 상대 import를 안전하게 따라가며 순환·누락을 보고한다."""
    seen = set() if seen is None else seen
    canonical = path.resolve()
    if canonical in seen:
        return [], [f"CSS import 순환: {path.relative_to(root).as_posix()}"]
    if not canonical.is_relative_to(root):
        return [], [f"패키지 밖 CSS import: {path}"]
    if not canonical.is_file():
        return [], [f"CSS import 파일 없음: {path.relative_to(root).as_posix()}"]
    seen.add(canonical)
    paths = [canonical]
    errors = []
    for child in imports(canonical):
        nested, nested_errors = collect_imports(child, root, seen.copy())
        paths.extend(nested)
        errors.extend(nested_errors)
    return paths, errors


def check_aliases(alias_dir: Path) -> list[str]:
    """별칭 디렉터리를 검사하고 사람이 읽을 수 있는 오류 목록을 반환한다."""
    errors: list[str] = []
    try:
        alias_dir = alias_dir.resolve()
    except OSError as exc:
        return [f"별칭 경로를 해석할 수 없음: {exc}"]
    if not alias_dir.is_dir():
        return [f"별칭 디렉터리 없음: {alias_dir}"]
    alias_paths = sorted(alias_dir.glob("*.css"))
    if not alias_paths:
        return [f"별칭 CSS가 없음: {alias_dir}"]

    root = package_root(alias_dir)
    tokens_path = root / "tokens.css"
    theme_path = root / "theme.css"
    shadcn_path = root / "shadcn.css"
    for required in (tokens_path, theme_path, shadcn_path):
        if not required.is_file():
            errors.append(f"필수 tokens 파일 없음: {required.relative_to(root).as_posix()}")
    if errors:
        return errors

    token_names = {item.name for item in definitions(tokens_path)}
    theme_defs = definitions(theme_path)
    theme_names = {item.name for item in theme_defs}
    shadcn_defs = definitions(shadcn_path)
    shadcn_names = {item.name for item in shadcn_defs}
    alias_defs: list[Definition] = []
    imported_defs: list[Definition] = []
    imported_paths: set[Path] = set()
    for alias_path in alias_paths:
        paths, import_errors = collect_imports(alias_path, root)
        errors.extend(import_errors)
        for path in paths:
            if path == alias_path.resolve():
                alias_defs.extend(definitions(path))
            elif path not in imported_paths:
                imported_paths.add(path)
                imported_defs.extend(definitions(path))

    alias_names = {item.name for item in alias_defs}
    imported_names = {item.name for item in imported_defs}
    all_defs = alias_defs + imported_defs
    all_refs = []
    for path in [*alias_paths, *sorted(imported_paths)]:
        text = without_comments(path.read_text(encoding="utf-8-sig"))
        all_refs.extend((path, ref) for ref in KT_REFERENCE.findall(text))

    for path, reference in all_refs:
        if reference not in token_names:
            errors.append(
                f"미정의 --kt-* 대상: {path.relative_to(root).as_posix()} -> {reference}"
            )

    for item in alias_defs:
        if item.name.startswith("--kt-"):
            errors.append(
                f"별칭 파일에서 --kt-* 정의 금지: {item.path.relative_to(root).as_posix()}:{item.line} {item.name}"
            )
        if item.name in theme_names:
            errors.append(
                f"Tailwind @theme 이름 충돌: {item.path.relative_to(root).as_posix()}:{item.line} {item.name}"
            )
        if item.name in shadcn_names:
            errors.append(
                f"shadcn.css 이름 중복 정의: {item.path.relative_to(root).as_posix()}:{item.line} {item.name}"
            )

    # 접두 네임스페이스는 exact 선언과 비교한다. --text-primary 같은 legacy
    # 이름은 --text-kt-*가 발행하는 Tailwind 이름과 충돌하지 않는다.
    for item in alias_defs:
        if any(item.name.startswith(namespace) for namespace in THEME_NAMESPACES):
            if item.name in theme_names:
                errors.append(
                    f"Tailwind 네임스페이스 exact 충돌: {item.path.relative_to(root).as_posix()}:{item.line} {item.name}"
                )

    # :root와 .dark에서 같은 legacy 이름을 쓰되 값이 갈라지면 profile 전달이
    # 깨진다. 같은 값의 반복은 의도적인 상속 경계로 허용한다.
    by_name: dict[str, set[str]] = {}
    for item in alias_defs:
        by_name.setdefault(item.name, set()).add(item.value)
    for name, values in sorted(by_name.items()):
        if len(values) > 1:
            errors.append(f"별칭 값 drift: {name} -> {', '.join(sorted(values))}")

    # import로 유효 이름을 제공하는 것은 허용하지만, alias가 같은 이름을
    # 직접 다시 선언하면 중복이므로 위 검사에서 반드시 잡힌다.
    _ = all_defs
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="tokens 별칭 CSS 계약 검사")
    default = Path(__file__).resolve().parents[1] / "packages" / "tokens" / "aliases"
    parser.add_argument("aliases", nargs="?", type=Path, default=default,
                        help="검사할 aliases 디렉터리")
    args = parser.parse_args(argv)
    errors = check_aliases(args.aliases)
    if errors:
        print(f"별칭 검사 실패: 오류 {len(errors)}개")
        for error in errors:
            print(f"- {error}")
        return 1
    files = len(sorted(args.aliases.resolve().glob("*.css")))
    print(f"별칭 검사 통과: CSS {files}개, 오류 0개")
    return 0


if __name__ == "__main__":
    sys.exit(main())
