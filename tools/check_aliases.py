# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"""tokens 별칭 CSS의 참조·네임스페이스·중복 선언을 읽기 전용으로 검사한다."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import os
from pathlib import Path
import re
import sys


CUSTOM_PROPERTY_NAME = re.compile(r"--[a-zA-Z0-9_-]+")
KT_REFERENCE = re.compile(r"(?i)\bvar\(\s*(--kt-[a-zA-Z0-9_-]+)")


class CSSInputError(ValueError):
    """CSS 입력을 안전하게 읽거나 해석할 수 없을 때 사용하는 내부 오류."""


@dataclass(frozen=True)
class Definition:
    name: str
    value: str
    path: Path
    line: int
    scope: str | None


@dataclass(frozen=True)
class ImportRule:
    target: str
    path: Path
    line: int


@dataclass(frozen=True)
class ParsedCSS:
    definitions: tuple[Definition, ...]
    imports: tuple[ImportRule, ...]


def _read_text(path: Path) -> str:
    """UTF-8 CSS를 읽고 오류 세부를 외부 출력으로 흘리지 않는다."""
    try:
        return path.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeError) as exc:
        raise CSSInputError("CSS 파일을 읽을 수 없음") from exc


def _mask_comments(text: str) -> str:
    """문자열 안의 주석 표기는 보존하고 CSS 주석만 공백으로 치환한다."""
    chars = list(text)
    result = list(text)
    quote: str | None = None
    escaped = False
    i = 0
    while i < len(text):
        char = text[i]
        if quote is not None:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                quote = None
            i += 1
            continue
        if char in "'\"":
            quote = char
            i += 1
            continue
        if text.startswith("/*", i):
            end = text.find("*/", i + 2)
            if end < 0:
                raise CSSInputError("닫히지 않은 CSS 주석")
            for position in range(i, end + 2):
                if chars[position] not in "\r\n":
                    result[position] = " "
            i = end + 2
            continue
        i += 1
    return "".join(result)


def _mask_strings(text: str) -> str:
    """CSS 값의 문자열 리터럴을 공백으로 바꿔 실제 var()만 찾는다."""
    result = list(text)
    quote: str | None = None
    escaped = False
    for index, char in enumerate(text):
        if quote is not None:
            if char not in "\r\n":
                result[index] = " "
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                quote = None
            continue
        if char in "'\"":
            quote = char
            result[index] = " "
    if quote is not None:
        raise CSSInputError("닫히지 않은 CSS 문자열")
    return "".join(result)


def _line_number(text: str, position: int) -> int:
    return text.count("\n", 0, position) + 1


def _scope(stack: list[str]) -> str | None:
    """직접 :root/.dark 선택자만 별칭 모드로 인정한다."""
    selector: str | None = None
    for candidate in reversed(stack):
        candidate = candidate.strip()
        if not candidate or candidate.startswith("@"):
            continue
        selector = candidate
        break
    if selector is None:
        return None
    parts = tuple(part.strip() for part in selector.split(","))
    if not parts or any(part not in (":root", ".dark") for part in parts):
        return None
    scopes = set(parts)
    if scopes == {":root", ".dark"}:
        return "both"
    if scopes == {":root"}:
        return "root"
    if scopes == {".dark"}:
        return "dark"
    return None


def _scan_value(text: str, start: int) -> tuple[str, int]:
    """선언 값의 끝과 값을 반환한다(괄호·문자열 안의 세미콜론은 무시)."""
    quote: str | None = None
    escaped = False
    parentheses = 0
    i = start
    while i < len(text):
        char = text[i]
        if quote is not None:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                quote = None
            i += 1
            continue
        if char in "'\"":
            quote = char
        elif char == "(":
            parentheses += 1
        elif char == ")":
            if parentheses == 0:
                raise CSSInputError("CSS 괄호가 올바르지 않음")
            parentheses -= 1
        elif parentheses == 0 and char in ";}":
            return text[start:i].strip(), i
        i += 1
    if quote is not None or parentheses:
        raise CSSInputError("CSS 선언 값이 닫히지 않음")
    raise CSSInputError("CSS 선언이 닫히지 않음")


def _quoted_target(text: str, start: int) -> tuple[str, int]:
    quote = text[start]
    escaped = False
    i = start + 1
    chars: list[str] = []
    while i < len(text):
        char = text[i]
        if escaped:
            chars.append(char)
            escaped = False
        elif char == "\\":
            escaped = True
        elif char == quote:
            return "".join(chars), i + 1
        else:
            chars.append(char)
        i += 1
    raise CSSInputError("CSS import 문자열이 닫히지 않음")


def _import_target(rule: str) -> str:
    """@import 뒤의 CSS 문자열 또는 url() 대상을 해석한다."""
    value = rule.strip()
    if not value:
        raise CSSInputError("CSS import 대상이 없음")
    if value[0] in "'\"":
        target, _ = _quoted_target(value, 0)
        return target
    match = re.match(r"(?i)url\s*\(", value)
    if match:
        start = match.end()
        quote: str | None = None
        escaped = False
        i = start
        while i < len(value):
            char = value[i]
            if quote is not None:
                if escaped:
                    escaped = False
                elif char == "\\":
                    escaped = True
                elif char == quote:
                    quote = None
                i += 1
                continue
            if char in "'\"":
                quote = char
            elif char == ")":
                target = value[start:i].strip()
                if target and target[0] in "'\"":
                    target, _ = _quoted_target(target, 0)
                return target.strip()
            i += 1
        raise CSSInputError("CSS import url()이 닫히지 않음")
    raise CSSInputError("지원하지 않는 CSS import 문법")


def _parse_imports(text: str, masked: str, path: Path) -> tuple[ImportRule, ...]:
    """한 줄·url·media 조건을 포함한 모든 @import 규칙을 찾는다."""
    imports: list[ImportRule] = []
    i = 0
    quote: str | None = None
    escaped = False
    while i < len(masked):
        char = masked[i]
        if quote is not None:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                quote = None
            i += 1
            continue
        if char in "'\"":
            quote = char
            i += 1
            continue
        if masked[i:i + 7].lower() == "@import" and (
            i == 0 or not (masked[i - 1].isalnum() or masked[i - 1] in "_-")
        ):
            end = i + 7
            nested_quote: str | None = None
            nested_escape = False
            parentheses = 0
            while end < len(masked):
                current = masked[end]
                if nested_quote is not None:
                    if nested_escape:
                        nested_escape = False
                    elif current == "\\":
                        nested_escape = True
                    elif current == nested_quote:
                        nested_quote = None
                elif current in "'\"":
                    nested_quote = current
                elif current == "(":
                    parentheses += 1
                elif current == ")" and parentheses:
                    parentheses -= 1
                elif current == ";" and parentheses == 0:
                    break
                elif current in "{}" and parentheses == 0:
                    raise CSSInputError("CSS import 규칙이 세미콜론으로 끝나지 않음")
                end += 1
            if end >= len(masked) or nested_quote is not None or parentheses:
                raise CSSInputError("CSS import 규칙이 닫히지 않음")
            target = _import_target(masked[i + 7:end])
            imports.append(ImportRule(target, path, _line_number(text, i)))
            i = end + 1
            continue
        i += 1
    return tuple(imports)


def _parse_css(path: Path) -> ParsedCSS:
    text = _read_text(path)
    masked = _mask_comments(text)
    # CSS escape를 해석하는 완전한 tokenizer가 아니므로, 문자열·식별자 안 escape를
    # 조용히 건너뛰지 않고 명시적으로 거부한다(@import·var 함수명 포함).
    if "\\" in masked:
        raise CSSInputError("지원하지 않는 CSS escape")
    imports = _parse_imports(text, masked, path)
    definitions: list[Definition] = []
    stack: list[str] = []
    header_start = 0
    can_start_declaration = True
    quote: str | None = None
    escaped = False
    i = 0
    while i < len(masked):
        char = masked[i]
        if quote is not None:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                quote = None
            i += 1
            continue
        if char in "'\"":
            quote = char
            can_start_declaration = False
            i += 1
            continue
        if char == "{":
            stack.append(masked[header_start:i].strip())
            header_start = i + 1
            can_start_declaration = True
            i += 1
            continue
        if char == "}":
            if not stack:
                raise CSSInputError("CSS 블록이 올바르지 않음")
            stack.pop()
            header_start = i + 1
            can_start_declaration = True
            i += 1
            continue
        if char == ";":
            can_start_declaration = True
            header_start = i + 1
            i += 1
            continue
        if can_start_declaration and masked.startswith("--", i):
            match = CUSTOM_PROPERTY_NAME.match(masked, i)
            if match is None and i + 2 < len(masked) and masked[i + 2] == "\\":
                raise CSSInputError("지원하지 않는 CSS custom property escape")
            if match is not None:
                name_end = match.end()
                colon = name_end
                while colon < len(masked) and masked[colon].isspace():
                    colon += 1
                if colon < len(masked) and masked[colon] == ":":
                    value, end = _scan_value(masked, colon + 1)
                    definitions.append(Definition(
                        match.group(0), value, path, _line_number(text, i), _scope(stack)
                    ))
                    can_start_declaration = False
                    i = end
                    continue
        if not char.isspace():
            can_start_declaration = False
        i += 1
    if quote is not None or stack:
        raise CSSInputError("CSS 블록 또는 문자열이 닫히지 않음")
    return ParsedCSS(tuple(definitions), imports)


def definitions(path: Path) -> list[Definition]:
    """한 CSS 파일의 custom property 선언을 읽는다."""
    return list(_parse_css(path).definitions)


def imports(path: Path) -> list[Path]:
    """한 CSS 파일의 상대 import 대상을 반환한다."""
    parsed = _parse_css(path)
    return [path.parent / item.target for item in parsed.imports]


def _absolute(path: Path) -> Path:
    """심볼릭 링크를 따라가지 않는 절대 lexical 경로를 만든다."""
    return Path(os.path.abspath(os.fspath(path)))


def _safe_real(
    path: Path,
    root: Path,
    *,
    directory: bool = False,
    lexical_root: Path | None = None,
) -> Path:
    """패키지 root 안의 실제 파일만 허용하고 링크 탈출을 차단한다."""
    lexical = _absolute(path)
    lexical_root = _absolute(root if lexical_root is None else lexical_root)
    try:
        lexical_inside = lexical.is_relative_to(lexical_root)
    except (OSError, ValueError):
        lexical_inside = False
    if not lexical_inside:
        raise CSSInputError("패키지 밖 파일 경로")
    try:
        boundary = _absolute(root).resolve(strict=True)
        real = lexical.resolve(strict=True)
    except (OSError, RuntimeError, ValueError) as exc:
        raise CSSInputError("파일 경로를 해석할 수 없음") from exc
    try:
        inside = real.is_relative_to(boundary)
    except (OSError, ValueError):
        inside = False
    if not inside:
        raise CSSInputError("패키지 밖 파일 경로")
    if directory:
        if not real.is_dir():
            raise CSSInputError("별칭 디렉터리가 아님")
    elif not real.is_file():
        raise CSSInputError("CSS 파일이 아님")
    return real


def _label(path: Path, root: Path) -> str:
    """진단 위치를 고정 문자열로 표시해 입력 경로를 로그에 남기지 않는다."""
    del path, root
    return "<package-css>"


def _load(
    path: Path,
    root: Path,
    cache: dict[Path, ParsedCSS],
    *,
    lexical_root: Path | None = None,
) -> ParsedCSS:
    real = _safe_real(path, root, lexical_root=lexical_root)
    if real not in cache:
        cache[real] = _parse_css(real)
    return cache[real]


def _collect(
    path: Path,
    root: Path,
    cache: dict[Path, ParsedCSS],
    collected: set[Path],
    active: tuple[Path, ...] = (),
    lexical_root: Path | None = None,
) -> tuple[list[Path], list[tuple[str, Path, int]]]:
    """CSS import closure를 수집하고 경계·순환 오류를 반환한다."""
    try:
        real = _safe_real(path, root, lexical_root=lexical_root)
        parsed = _load(real, root, cache, lexical_root=lexical_root)
    except CSSInputError as exc:
        return [], [(str(exc), path, 0)]
    if real in active:
        return [], [("CSS import 순환", real, 0)]
    if real in collected:
        return [], []
    collected.add(real)
    paths = [real]
    errors: list[tuple[str, Path, int]] = []
    for rule in parsed.imports:
        target = rule.target.strip()
        if not target or target.startswith(("/", "\\")) or re.match(r"(?i)^[a-z][a-z0-9+.-]*:", target):
            errors.append(("CSS import 패키지 경계 오류", real, rule.line))
            continue
        child = real.parent / target
        nested, nested_errors = _collect(
            child, root, cache, collected, (*active, real), lexical_root
        )
        paths.extend(nested)
        errors.extend(nested_errors)
    return paths, errors


def _refs(value: str) -> list[str]:
    masked = _mask_strings(value)
    if re.search(r"(?i)\bvar\(\s*--\\", masked):
        raise CSSInputError("지원하지 않는 CSS var custom property escape")
    return KT_REFERENCE.findall(masked)


def _append_safe_error(errors: list[str], reason: str, path: Path, root: Path, line: int = 0) -> None:
    location = _label(path, root)
    suffix = f" {location}:{line}" if line else f" {location}"
    errors.append(f"{reason}:{suffix}")


def check_aliases(alias_dir: Path) -> list[str]:
    """별칭 디렉터리를 검사하고 사람이 읽을 수 있는 오류 목록을 반환한다."""
    errors: list[str] = []
    cache: dict[Path, ParsedCSS] = {}
    try:
        alias_lexical = _absolute(alias_dir)
        lexical_root = _absolute(alias_lexical.parent)
        root = _safe_real(lexical_root, lexical_root, directory=True, lexical_root=lexical_root)
        alias_real = _safe_real(alias_lexical, root, directory=True, lexical_root=lexical_root)
        alias_paths = sorted(
            (item for item in alias_real.iterdir() if item.name.endswith(".css")),
            key=lambda item: item.name,
        )
    except (OSError, CSSInputError):
        return ["별칭 경로를 읽을 수 없음"]
    if not alias_paths:
        return ["별칭 CSS가 없음"]

    # 짧은(8.3) 입력 경로를 허용하려면 lexical 경로와 canonical 경로를 섞지 않는다.
    required_paths = {name: lexical_root / name for name in ("tokens.css", "theme.css", "shadcn.css")}
    required: dict[str, Path] = {}
    for name, lexical in required_paths.items():
        try:
            required[name] = _safe_real(lexical, root, lexical_root=lexical_root)
            cache[required[name]] = _parse_css(required[name])
        except (OSError, CSSInputError):
            errors.append(f"필수 {name} 파일을 읽을 수 없음")
    if errors:
        return errors

    token_names = {item.name for item in cache[required["tokens.css"]].definitions}
    theme_defs = list(cache[required["theme.css"]].definitions)
    shadcn_defs = list(cache[required["shadcn.css"]].definitions)
    theme_names = {item.name for item in theme_defs}
    shadcn_names = {item.name for item in shadcn_defs}
    canonical_shadcn = required["shadcn.css"]

    alias_defs: list[Definition] = []
    imported_defs: list[Definition] = []
    imported_paths: set[Path] = set()
    for alias_path in alias_paths:
        try:
            alias_real = _safe_real(alias_path, root, lexical_root=root)
            parsed = _load(alias_real, root, cache, lexical_root=root)
        except CSSInputError as exc:
            _append_safe_error(errors, str(exc), alias_path, root)
            continue
        except OSError:
            _append_safe_error(errors, "별칭 CSS를 읽을 수 없음", alias_path, root)
            continue
        alias_defs.extend(parsed.definitions)
        paths, import_errors = _collect(
            alias_real, root, cache, imported_paths, lexical_root=root
        )
        for reason, error_path, line in import_errors:
            _append_safe_error(errors, reason, error_path, root, line)
        for path in paths:
            if path != alias_real and path != canonical_shadcn:
                imported_defs.extend(cache[path].definitions)

    noncanonical_defs = alias_defs + imported_defs
    all_defs = noncanonical_defs + shadcn_defs
    for item in all_defs:
        try:
            references = _refs(item.value)
        except CSSInputError:
            _append_safe_error(errors, "지원하지 않는 CSS var 문법", item.path, root, item.line)
            continue
        for reference in references:
            if reference not in token_names:
                _append_safe_error(
                    errors, "미정의 --kt-* 대상", item.path, root, item.line
                )

    for item in noncanonical_defs:
        if item.name.startswith("--kt-"):
            _append_safe_error(errors, "--kt-* 정의 금지", item.path, root, item.line)
        if item.name in theme_names:
            _append_safe_error(errors, "Tailwind @theme 이름 충돌", item.path, root, item.line)
        if item.name in shadcn_names:
            _append_safe_error(errors, "shadcn.css 이름 중복 정의", item.path, root, item.line)

    # 별칭 디렉터리의 모든 직접 선언은 :root와 .dark에 한 번씩 있어야 한다.
    root_names = {item.name for item in alias_defs if item.scope in ("root", "both")}
    dark_names = {item.name for item in alias_defs if item.scope in ("dark", "both")}
    unscoped = {item.name for item in alias_defs if item.scope is None}
    if unscoped:
        errors.append("별칭 모드 밖 선언")
    if not root_names:
        errors.append("별칭 :root 블록이 없음")
    if not dark_names:
        errors.append("별칭 .dark 블록이 없음")
    for name in sorted(root_names - dark_names):
        errors.append("별칭 .dark 선언 누락")
    for name in sorted(dark_names - root_names):
        errors.append("별칭 :root 선언 누락")

    # 같은 모드의 중복 정의와 root/dark 값 drift를 모두 검사한다.
    by_scope_name: dict[tuple[str | None, str], list[Definition]] = {}
    by_name: dict[str, set[str]] = {}
    for item in noncanonical_defs:
        by_scope_name.setdefault((item.scope, item.name), []).append(item)
        by_name.setdefault(item.name, set()).add(item.value)
    for (scope, name), items in sorted(by_scope_name.items(), key=lambda pair: str(pair[0])):
        if len(items) > 1:
            errors.append(f"별칭 중복 선언 ({scope or 'import'})")
    for name, values in sorted(by_name.items()):
        if len(values) > 1:
            errors.append("별칭 값 drift")

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
    try:
        files = len([path for path in _absolute(args.aliases).iterdir() if path.name.endswith(".css")])
    except OSError:
        files = 0
    print(f"별칭 검사 통과: CSS {files}개, 오류 0개")
    return 0


if __name__ == "__main__":
    sys.exit(main())
