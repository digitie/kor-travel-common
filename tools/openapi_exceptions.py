#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"""OpenAPI 예외 레지스트리를 검증하고 사람이 읽는 표를 생성한다.

레지스트리는 공통 저장소에서 재현 가능한 검증을 해야 하므로 PyYAML에
의존하지 않는다. 이 도구가 읽는 YAML은 문자열·null·단순 flow sequence와
block mapping/list만 허용하는 의도적으로 작은 부분집합이다. 지원하지 않는
YAML 문법은 조용히 문자열로 바꾸지 않고 입력 오류로 닫는다.
"""

from __future__ import annotations

import argparse
import calendar
import html
import json
import os
import re
import sys
import tempfile
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "docs" / "standards" / "openapi-exceptions.yaml"
DEFAULT_OUTPUT = ROOT / "docs" / "standards" / "openapi-exceptions.md"
OPENAPI_STANDARD = ROOT / "docs" / "standards" / "openapi.md"
BACKEND_STANDARD = ROOT / "docs" / "standards" / "backend-stack.md"

TOP_LEVEL_KEYS = frozenset({"schema", "updated", "apps", "exceptions"})
ENTRY_KEYS = frozenset({"app", "rule", "surface", "reason", "sunset", "review", "owner"})
ALLOWED_APPS = frozenset({"airport", "concierge", "ktdm", "geo", "map", "weather", "pinvi"})
IMMEDIATE_MUST = frozenset({"M2", "M4", "M9", "N6", "N7"})
CORE_RULE_IDS = frozenset(
    {*(f"M{i}" for i in range(1, 10)), *(f"S{i}" for i in range(1, 14)), *(f"N{i}" for i in range(1, 9))}
)
ISO_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
RULE_RE = re.compile(r"^[MSN]\d+(?:\.\d+)?$|^BE-\d+$")
TASK_REFERENCE_RE = re.compile(r"(?<![A-Za-z0-9])T-\d{3}[a-z]?(?![A-Za-z0-9])")
PLAIN_NONSTRING_RE = re.compile(
    r"^(?:[-+]?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][-+]?\d+)?|[-+]?\.inf|\.nan|"
    r"\d{4}-\d{2}-\d{2}|\d{2}:\d{2}:\d{2})$",
    re.IGNORECASE,
)


class RegistryError(ValueError):
    """레지스트리 문법·계약 오류."""


@dataclass(frozen=True)
class _YamlLine:
    indent: int
    content: str
    number: int


def _error(message: str, line: int | None = None) -> RegistryError:
    if line is None:
        return RegistryError(message)
    return RegistryError(f"{message} (line {line})")


def _validate_text(value: str, context: str) -> str:
    """출력·키·값을 오염시키는 제어 문자와 lone surrogate를 거부한다."""
    for character in value:
        codepoint = ord(character)
        if codepoint < 0x20 or codepoint == 0x7F:
            raise RegistryError(f"{context}에 제어 문자가 있음")
        if 0xD800 <= codepoint <= 0xDFFF:
            raise RegistryError(f"{context}에 유효하지 않은 surrogate가 있음")
    return value


def _strip_comment(raw: str, number: int) -> str:
    """인용 문자열 밖의 공백 뒤 `#`를 주석으로 제거한다."""
    quote = ""
    escaped = False
    index = 0
    while index < len(raw):
        char = raw[index]
        if quote:
            if quote == '"':
                if escaped:
                    escaped = False
                elif char == "\\":
                    escaped = True
                elif char == '"':
                    quote = ""
            elif char == "'":
                if index + 1 < len(raw) and raw[index + 1] == "'":
                    index += 1
                else:
                    quote = ""
            index += 1
            continue
        if char in {"'", '"'}:
            quote = char
        elif char == "#" and (index == 0 or raw[index - 1].isspace()):
            return raw[:index].rstrip()
        index += 1
    if quote:
        raise _error("인용 문자열이 닫히지 않음", number)
    return raw.rstrip()


class _FlatYamlParser:
    """레지스트리에 필요한 YAML 부분집합만 읽는 fail-closed 파서."""

    def __init__(self, text: str):
        self.lines: list[_YamlLine] = []
        for number, raw in enumerate(text.splitlines(), 1):
            if number == 1 and raw.startswith("\ufeff"):
                raw = raw[1:]
            if "\t" in raw or "\x00" in raw:
                raise _error("탭·NUL은 허용하지 않음", number)
            _validate_text(raw, f"line {number}")
            clean = _strip_comment(raw, number)
            if not clean.strip():
                continue
            indent = len(clean) - len(clean.lstrip(" "))
            content = clean[indent:]
            if content in {"---", "..."} or content.startswith("%"):
                raise _error("YAML document stream은 허용하지 않음", number)
            self.lines.append(_YamlLine(indent, content, number))

    @staticmethod
    def _split_pair(content: str, number: int) -> tuple[str, str] | None:
        quote = ""
        escaped = False
        index = 0
        while index < len(content):
            char = content[index]
            if quote:
                if quote == '"':
                    if escaped:
                        escaped = False
                    elif char == "\\":
                        escaped = True
                    elif char == '"':
                        quote = ""
                elif char == "'":
                    if index + 1 < len(content) and content[index + 1] == "'":
                        index += 1
                    else:
                        quote = ""
                index += 1
                continue
            if char in {"'", '"'}:
                quote = char
            elif char == ":" and (index + 1 == len(content) or content[index + 1].isspace()):
                key = content[:index].strip()
                if not key:
                    raise _error("빈 YAML 키", number)
                return key, content[index + 1 :].strip()
            index += 1
        if quote:
            raise _error("인용 문자열이 닫히지 않음", number)
        return None

    @staticmethod
    def _decode_single(value: str, number: int) -> str:
        if len(value) < 2 or not value.endswith("'"):
            raise _error("잘못 닫힌 single-quoted scalar", number)
        inner = value[1:-1]
        result: list[str] = []
        index = 0
        while index < len(inner):
            if inner[index] != "'":
                result.append(inner[index])
                index += 1
                continue
            if index + 1 >= len(inner) or inner[index + 1] != "'":
                raise _error("single quote escape 오류", number)
            result.append("'")
            index += 2
        return _validate_text("".join(result), f"line {number} scalar")

    @staticmethod
    def _decode_double(value: str, number: int) -> str:
        if len(value) < 2 or not value.endswith('"'):
            raise _error("잘못 닫힌 double-quoted scalar", number)
        try:
            decoded = json.loads(value)
        except json.JSONDecodeError as exc:
            raise _error("double quote escape 오류", number) from exc
        if not isinstance(decoded, str):
            raise _error("문자열이 아닌 scalar", number)
        return _validate_text(decoded, f"line {number} scalar")

    def _scalar(self, raw: str, number: int) -> object:
        value = raw.strip()
        if not value:
            raise _error("빈 scalar", number)
        if value.startswith("["):
            if not value.endswith("]"):
                raise _error("flow sequence이 닫히지 않음", number)
            inner = value[1:-1].strip()
            if not inner:
                return []
            parts: list[str] = []
            start = 0
            quote = ""
            escaped = False
            index = 0
            while index < len(inner):
                char = inner[index]
                if quote:
                    if quote == '"':
                        if escaped:
                            escaped = False
                        elif char == "\\":
                            escaped = True
                        elif char == '"':
                            quote = ""
                    elif char == "'":
                        if index + 1 < len(inner) and inner[index + 1] == "'":
                            index += 1
                        else:
                            quote = ""
                    index += 1
                    continue
                if char in {"'", '"'}:
                    quote = char
                elif char in "[]{}":
                    raise _error("중첩 flow 구조는 허용하지 않음", number)
                elif char == ",":
                    part = inner[start:index].strip()
                    if not part:
                        raise _error("flow sequence 항목이 비어 있음", number)
                    parts.append(part)
                    start = index + 1
                index += 1
            if quote:
                raise _error("flow sequence 인용 문자열이 닫히지 않음", number)
            part = inner[start:].strip()
            if not part:
                raise _error("flow sequence 끝 항목이 비어 있음", number)
            parts.append(part)
            return [self._scalar(part, number) for part in parts]
        if value.startswith(("{", "|", ">", "!", "&", "*", "%")):
            raise _error("지원하지 않는 YAML scalar 문법", number)
        if value.startswith("---") or value.startswith("..."):
            raise _error("YAML document marker는 허용하지 않음", number)
        if value.startswith("'"):
            return self._decode_single(value, number)
        if value.startswith('"'):
            return self._decode_double(value, number)
        if value.lower() in {"null", "~"}:
            return None
        if re.search(r":(?:\s|$)", value):
            raise _error("plain scalar 안의 mapping colon은 허용하지 않음", number)
        if value[:1] in {",", "]", "}"}:
            raise _error("잘못된 flow scalar", number)
        if value.lower() in {"true", "false", "yes", "no", "on", "off"} or PLAIN_NONSTRING_RE.fullmatch(value):
            raise _error("plain scalar는 문자열로 해석되는 값만 허용함", number)
        return _validate_text(value, f"line {number} scalar")

    def _key(self, raw: str, number: int) -> str:
        value = self._scalar(raw, number)
        if not isinstance(value, str) or not value:
            raise _error("YAML 키는 비어 있지 않은 문자열이어야 함", number)
        return value

    def _parse_value(self, raw: str, index: int, parent_indent: int, number: int) -> tuple[object, int]:
        if raw:
            return self._scalar(raw, number), index
        if index < len(self.lines) and self.lines[index].indent > parent_indent:
            if self.lines[index].indent != parent_indent + 2:
                raise _error("들여쓰기는 두 칸 단위여야 함", self.lines[index].number)
            return self._parse_block(self.lines[index].indent, index)
        return None, index

    def _parse_map(self, indent: int, index: int) -> tuple[dict[str, object], int]:
        values: dict[str, object] = {}
        while index < len(self.lines):
            current = self.lines[index]
            if current.indent < indent:
                break
            if current.indent > indent or current.content == "-" or current.content.startswith("- "):
                break
            pair = self._split_pair(current.content, current.number)
            if pair is None:
                raise _error("mapping 항목에 colon이 없음", current.number)
            raw_key, raw_value = pair
            key = self._key(raw_key, current.number)
            if key in values:
                raise _error(f"중복 YAML 키: {key}", current.number)
            values[key], index = self._parse_value(raw_value, index + 1, indent, current.number)
        if not values:
            raise _error("빈 mapping", self.lines[index].number if index < len(self.lines) else None)
        return values, index

    def _parse_list(self, indent: int, index: int) -> tuple[list[object], int]:
        values: list[object] = []
        while index < len(self.lines):
            current = self.lines[index]
            if current.indent < indent:
                break
            if current.indent > indent or not (current.content == "-" or current.content.startswith("- ")):
                break
            rest = current.content[1:].strip()
            index += 1
            if not rest:
                if index < len(self.lines) and self.lines[index].indent > indent:
                    if self.lines[index].indent != indent + 2:
                        raise _error("list mapping 들여쓰기 오류", self.lines[index].number)
                    item, index = self._parse_block(self.lines[index].indent, index)
                else:
                    item = None
                values.append(item)
                continue
            pair = self._split_pair(rest, current.number)
            if pair is None:
                item = self._scalar(rest, current.number)
                if index < len(self.lines) and self.lines[index].indent > indent:
                    raise _error("scalar list 항목에 자식이 있음", self.lines[index].number)
                values.append(item)
                continue
            raw_key, raw_value = pair
            key = self._key(raw_key, current.number)
            item, index = self._parse_value(raw_value, index, indent + 2, current.number)
            mapping: dict[str, object] = {key: item}
            if index < len(self.lines) and self.lines[index].indent > indent:
                if self.lines[index].indent != indent + 2:
                    raise _error("list mapping 들여쓰기 오류", self.lines[index].number)
                continuation, index = self._parse_map(indent + 2, index)
                for continuation_key, continuation_value in continuation.items():
                    if continuation_key in mapping:
                        raise _error(f"중복 YAML 키: {continuation_key}", self.lines[index - 1].number)
                    mapping[continuation_key] = continuation_value
            values.append(mapping)
        if not values:
            raise _error("빈 list", self.lines[index].number if index < len(self.lines) else None)
        return values, index

    def _parse_block(self, indent: int, index: int) -> tuple[object, int]:
        if index >= len(self.lines) or self.lines[index].indent != indent:
            raise _error("YAML block 들여쓰기 오류", self.lines[index].number if index < len(self.lines) else None)
        content = self.lines[index].content
        if content == "-" or content.startswith("- "):
            return self._parse_list(indent, index)
        if content.startswith("-"):
            raise _error("잘못된 list marker", self.lines[index].number)
        return self._parse_map(indent, index)

    def parse(self) -> object:
        if not self.lines or self.lines[0].indent != 0:
            raise _error("최상위 YAML mapping이 필요함")
        value, index = self._parse_block(0, 0)
        if index != len(self.lines):
            raise _error("YAML 뒤에 해석되지 않은 내용이 있음", self.lines[index].number)
        return value


def _parse_date(value: object, field: str) -> date:
    if not isinstance(value, str) or not ISO_DATE_RE.fullmatch(value):
        raise RegistryError(f"{field}는 YYYY-MM-DD 문자열이어야 함")
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise RegistryError(f"{field}가 유효한 날짜가 아님") from exc


def _add_months(value: date, months: int) -> date:
    month_index = value.month - 1 + months
    year, month = value.year + month_index // 12, month_index % 12 + 1
    return date(year, month, min(value.day, calendar.monthrange(year, month)[1]))


def _rule_ids() -> set[str]:
    ids: set[str] = set()
    for path in (OPENAPI_STANDARD, BACKEND_STANDARD):
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            raise RegistryError(f"규칙 문서를 읽을 수 없음: {path}") from exc
        ids.update(re.findall(r"^\|\s*((?:M|S|N)\d+(?:\.\d+)?|BE-\d+)\s*\|", text, re.MULTILINE))
    if not CORE_RULE_IDS.issubset(ids):
        missing = ", ".join(sorted(CORE_RULE_IDS - ids))
        raise RegistryError(f"규칙 문서에 core ID가 없음: {missing}")
    return ids


def _task_ids() -> set[str]:
    """common task 원장에서 실제로 정의된 task ID를 수집한다."""
    paths = [ROOT / "docs" / "tasks.md", *(ROOT / "docs" / "tasks").glob("T-*.md")]
    ids: set[str] = set()
    for path in paths:
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            raise RegistryError(f"task 원장을 읽을 수 없음: {path}") from exc
        ids.update(TASK_REFERENCE_RE.findall(text))
    return ids


def load_registry(path: Path = DEFAULT_INPUT, *, as_of: date | None = None) -> dict[str, Any]:
    """YAML을 읽고 레지스트리 계약을 검증한 뒤 plain dict로 반환한다."""
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise RegistryError(f"레지스트리를 읽을 수 없음: {path}") from exc
    try:
        root = _FlatYamlParser(text).parse()
    except RegistryError:
        raise
    except Exception as exc:  # pragma: no cover - fail closed safety net
        raise RegistryError("레지스트리 YAML 파싱 실패") from exc
    if not isinstance(root, dict) or set(root) != TOP_LEVEL_KEYS:
        raise RegistryError(f"최상위 키는 정확히 {sorted(TOP_LEVEL_KEYS)}여야 함")
    if root["schema"] != "kor-travel-common.openapi-exceptions.v1":
        raise RegistryError("지원하지 않는 registry schema")
    updated = _parse_date(root["updated"], "updated")
    apps = root["apps"]
    if not isinstance(apps, list) or any(not isinstance(app, str) for app in apps):
        raise RegistryError("apps는 문자열 list여야 함")
    if set(apps) != ALLOWED_APPS or len(apps) != len(ALLOWED_APPS):
        raise RegistryError("apps는 7개 공통 소비자 목록과 정확히 일치해야 함")
    entries = root["exceptions"]
    if not isinstance(entries, list) or not entries:
        raise RegistryError("exceptions는 비어 있지 않은 list여야 함")
    valid_rules = _rule_ids()
    valid_tasks = _task_ids()
    seen: set[tuple[str, str, str]] = set()
    today = as_of or date.today()
    if updated > today:
        raise RegistryError("updated가 검사 기준일보다 미래일 수 없음")
    for index, entry in enumerate(entries, 1):
        if not isinstance(entry, dict) or set(entry) != ENTRY_KEYS:
            raise RegistryError(f"exceptions[{index}] 키는 정확히 {sorted(ENTRY_KEYS)}여야 함")
        for key in ("app", "rule", "surface", "reason", "owner"):
            if not isinstance(entry[key], str) or not entry[key].strip():
                raise RegistryError(f"exceptions[{index}].{key}는 비어 있지 않은 문자열이어야 함")
        task_references = TASK_REFERENCE_RE.findall(entry["reason"])
        if not task_references:
            raise RegistryError(f"exceptions[{index}].reason에 정합 task ID가 없음")
        if any(task_id not in valid_tasks for task_id in task_references):
            raise RegistryError(f"exceptions[{index}].reason에 정의되지 않은 task ID가 있음")
        if entry["rule"].startswith("S"):
            if entry["surface"] == "*" or "외부 계약" not in entry["reason"]:
                raise RegistryError(
                    f"exceptions[{index}] SHOULD 예외는 구체적인 외부 계약 표면만 등록할 수 있음"
                )
            if "M10" not in entry["reason"] and "동반 PR" not in entry["reason"]:
                raise RegistryError(f"exceptions[{index}] SHOULD 외부 계약 예외는 동반 PR 근거가 필요함")
        if entry["app"] not in apps or entry["app"] not in ALLOWED_APPS:
            raise RegistryError(f"exceptions[{index}].app가 apps 목록에 없음")
        if not RULE_RE.fullmatch(entry["rule"]) or entry["rule"] not in valid_rules:
            raise RegistryError(f"exceptions[{index}].rule가 규칙 문서에 없음: {entry['rule']}")
        identity = (entry["app"], entry["rule"], entry["surface"])
        if identity in seen:
            raise RegistryError(f"중복 예외 항목: {identity}")
        seen.add(identity)
        sunset = entry["sunset"]
        if sunset is not None:
            sunset_date = _parse_date(sunset, f"exceptions[{index}].sunset")
            if sunset_date < updated:
                raise RegistryError(f"exceptions[{index}].sunset가 updated보다 빠름")
            if sunset_date < today:
                raise RegistryError(f"exceptions[{index}].sunset가 지남")
        elif entry["rule"] in IMMEDIATE_MUST:
            raise RegistryError(f"exceptions[{index}] 즉시 MUST는 sunset을 null로 둘 수 없음")
        review = _parse_date(entry["review"], f"exceptions[{index}].review")
        if review < updated or review > _add_months(updated, 6):
            raise RegistryError(f"exceptions[{index}].review는 updated부터 6개월 안이어야 함")
    return {"schema": root["schema"], "updated": updated, "apps": list(apps), "exceptions": entries}


def _markdown_cell(value: object) -> str:
    if value is None:
        return "null"
    text = html.escape(str(value).replace("\r", " ").replace("\n", " "), quote=False)
    for character, entity in {
        "\\": "&#92;",
        "|": "&#124;",
        "[": "&#91;",
        "]": "&#93;",
        "(": "&#40;",
        ")": "&#41;",
        "`": "&#96;",
        "*": "&#42;",
        "_": "&#95;",
        "~": "&#126;",
        "!": "&#33;",
    }.items():
        text = text.replace(character, entity)
    return text


def render_markdown(registry: dict[str, Any]) -> str:
    """검증된 레지스트리의 결정적 Markdown 표현을 만든다."""
    entries = registry["exceptions"]
    lines = [
        "<!-- SPDX-License-Identifier: GPL-3.0-or-later -->",
        "<!-- SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie) -->",
        "# OpenAPI·REST 예외 레지스트리",
        "",
        "> 이 문서는 [정본 YAML](openapi-exceptions.yaml)에서 생성한 읽기 전용 표다. 수기 편집하지 않는다.",
        "",
        f"- schema: `{registry['schema']}`",
        f"- updated: `{registry['updated'].isoformat()}`",
        f"- apps: {', '.join(f'`{app}`' for app in registry['apps'])}",
        f"- exceptions: **{len(entries)}건**",
        "",
        "| 앱 | 규칙 | 표면 | 사유 | sunset | review | owner |",
        "|---|---|---|---|---|---|---|",
    ]
    for entry in entries:
        lines.append(
            "| "
            + " | ".join(
                _markdown_cell(entry[key])
                for key in ("app", "rule", "surface", "reason", "sunset", "review", "owner")
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "검사: `python -B -X utf8 tools/openapi_exceptions.py --check`.",
            "",
        ]
    )
    return "\n".join(lines)


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def _ensure_distinct_paths(input_path: Path, output_path: Path) -> None:
    """input 정본과 생성물 alias를 차단한다."""
    try:
        if input_path.resolve(strict=False) == output_path.resolve(strict=False):
            raise RegistryError("input과 output은 같은 파일일 수 없음")
    except OSError as exc:
        raise RegistryError("input/output 경로를 확인할 수 없음") from exc
    if input_path.exists() and output_path.exists():
        try:
            if os.path.samefile(input_path, output_path):
                raise RegistryError("input과 output은 같은 파일일 수 없음")
        except OSError:
            # 서로 다른 파일이거나 아직 samefile을 지원하지 않는 파일 시스템이다.
            pass


def generate(input_path: Path = DEFAULT_INPUT, output_path: Path = DEFAULT_OUTPUT) -> tuple[int, int]:
    _ensure_distinct_paths(input_path, output_path)
    registry = load_registry(input_path)
    rendered = render_markdown(registry)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="\n",
            dir=output_path.parent,
            prefix=f".{output_path.name}.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            temporary_path = Path(handle.name)
            handle.write(rendered)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_path, output_path)
    except Exception:
        if temporary_path is not None:
            try:
                temporary_path.unlink(missing_ok=True)
            except OSError:
                pass
        raise
    return len(registry["exceptions"]), len(rendered.splitlines())


def check(input_path: Path = DEFAULT_INPUT, output_path: Path = DEFAULT_OUTPUT) -> tuple[bool, str]:
    _ensure_distinct_paths(input_path, output_path)
    registry = load_registry(input_path)
    expected = render_markdown(registry)
    try:
        actual = output_path.read_text(encoding="utf-8")
    except OSError:
        return False, f"생성물이 없음: {_display_path(output_path)}"
    if actual != expected:
        return False, f"생성물 drift: {_display_path(output_path)} (먼저 --write 실행)"
    return True, f"예외 {len(registry['exceptions'])}건·Markdown {len(expected.splitlines())}줄"


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT, help="예외 YAML 경로")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="생성 Markdown 경로")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="생성물 drift를 검사")
    mode.add_argument("--write", action="store_true", help="생성 Markdown을 기록")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    try:
        if args.check:
            passed, message = check(args.input, args.output)
            print(message)
            return 0 if passed else 1
        count, lines = generate(args.input, args.output)
        print(f"생성 완료: 예외 {count}건, Markdown {lines}줄")
        return 0
    except (OSError, RegistryError, ValueError) as exc:
        print(f"openapi 예외 레지스트리 오류: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
