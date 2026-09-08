# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"""공통 UX 금지 패턴을 보고하고 신규 위반을 검사하는 표준 라이브러리 도구."""

from __future__ import annotations

import argparse
from collections import defaultdict
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from typing import Iterable, Mapping, Sequence


TARGET_EXTENSIONS = {".tsx", ".ts", ".css", ".mdx"}
SKIP_DIRECTORIES = {".git", "node_modules", ".next", "dist", "build", "coverage", "__pycache__", "e2e", "tests", "vendor"}
_MARKDOWN_LINE_BREAK_PATTERN = r"(?:\r\n|\n|\r(?!\n))"
_MDX_PARAGRAPH_BOUNDARY = re.compile(
    rf"{_MARKDOWN_LINE_BREAK_PATTERN}"
    rf"(?:[ \t]*{_MARKDOWN_LINE_BREAK_PATTERN}|[ \t]*>(?:[ \t]*>)*[ \t]*{_MARKDOWN_LINE_BREAK_PATTERN})"
)
_MDX_LINE_TERMINATORS = frozenset("\r\n\u2028\u2029")
_MARKDOWN_LINE_TERMINATORS = frozenset("\r\n")


class UxLintError(ValueError):
    """입력·git diff·baseline이 잘못된 경우의 오류."""


class _UxArgumentParser(argparse.ArgumentParser):
    """argparse가 입력 원문을 오류 채널에 되풀이하지 않게 한다."""

    def error(self, message: str) -> None:
        raise UxLintError("명령 인자가 잘못되었습니다")


PATTERNS: tuple[tuple[str, str, str], ...] = (
    (
        "P1",
        "transition-all/colors 또는 bare transition",
        r"(?<![\w-])transition(?:-all|-colors)?(?=$|[\s\"'`])",
    ),
    ("P2", "임의 px 텍스트 크기", r"\btext-\[[0-9]+(?:\.[0-9]+)?px\]"),
    ("P3", "큰 radius 또는 임의 radius", r"\brounded(?:-[a-z]{1,2})?-(?:2xl|3xl|4xl|\[)"),
    (
        "P4a",
        "유틸리티 안 raw 색상",
        r"\b(?:bg|text|border|outline|ring|fill|stroke|from|to|via)-\[(?:#|oklch\(|rgba?\(|hsla?\()",
    ),
    (
        "P4b",
        "토큰 파일 밖 raw 색상",
        r"(?<![\w-])#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{4}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})\b|\b(?:oklch|rgba?|hsla?)\s*\(",
    ),
    (
        "P5",
        "팔레트 alpha 유틸리티",
        r"\b(?:bg|text|border|ring|outline|fill|stroke|from|to|via|shadow)-[a-z][a-z0-9-]*/[0-9]{1,3}\b",
    ),
    ("P6", "outline-none", r"\boutline-none\b"),
    ("P7", "aria-disabled/busy opacity", r"\baria-(?:disabled|busy):opacity-"),
    ("P8", "window.confirm 또는 bare confirm", r"\bwindow\.confirm\b|(?<![.\w])confirm\("),
)
COMPILED_PATTERNS = tuple((name, description, re.compile(expression)) for name, description, expression in PATTERNS)
KNOWN_RULES = {name for name, _, _ in PATTERNS}
_SECRET_PATH_PART = re.compile(r"(?:gh[pousr]_[A-Za-z0-9_-]{16,}|github_pat_[A-Za-z0-9_\-]{16,}|sk-[A-Za-z0-9_-]{16,}|AKIA[0-9A-Z]{12,})")
_PRIVATE_ADDRESS_PART = re.compile(r"(?<![\w])(?:\d{1,3}\.){3}\d{1,3}(?![\w])")


def _public_path(value: str) -> str:
    """경로에 우연히 포함된 자격증명 형태를 출력에서 가린다."""

    redacted = _SECRET_PATH_PART.sub("<redacted>", value)
    return _PRIVATE_ADDRESS_PART.sub("<redacted>", redacted)


def _read_text_preserving_newlines(path: Path) -> str:
    """소스의 CR/LF/Unicode 줄 종결자를 변환하지 않고 읽는다."""

    with path.open("r", encoding="utf-8", newline="") as stream:
        return stream.read()


def _find_backtick_run_end(text: str, start: int, run_length: int) -> int:
    """같은 길이의 backtick delimiter 끝을 찾아 닫히지 않으면 끝을 반환한다."""

    delimiter = "`" * run_length
    index = start + run_length
    while index < len(text):
        if text[index] == "\\" and run_length == 1:
            index += 2
            continue
        if text.startswith(delimiter, index):
            run = 0
            while index + run < len(text) and text[index + run] == "`":
                run += 1
            if run == run_length:
                return index
            index += run
            continue
        index += 1
    return len(text)


def _paragraph_end(text: str, start: int) -> int:
    """현재 Markdown 문단의 끝 위치를 반환한다."""

    boundary = _MDX_PARAGRAPH_BOUNDARY.search(text, start)
    return boundary.start() if boundary else len(text)


def _is_mdx_whitespace(char: str) -> bool:
    """Python 버전과 무관하게 ECMAScript 공백 문자인지 확인한다."""

    return char.isspace() or char == "\ufeff"


def _is_mdx_line_terminator(char: str) -> bool:
    """ECMAScript line comment를 끝내는 네 가지 문자인지 확인한다."""

    return char in _MDX_LINE_TERMINATORS


def _find_mdx_line_terminator(text: str, start: int, boundary: int) -> int:
    """범위 안에서 가장 가까운 ECMAScript 줄 종결자 위치를 반환한다."""

    positions = [text.find(char, start, boundary) for char in _MDX_LINE_TERMINATORS]
    found = [position for position in positions if position >= 0]
    return min(found, default=boundary)


def _is_markdown_line_terminator(char: str) -> bool:
    """CommonMark 줄 종결자(LF·CR·CRLF)의 문자 부분인지 확인한다."""

    return char in _MARKDOWN_LINE_TERMINATORS


def _find_markdown_line_terminator(text: str, start: int, boundary: int) -> int:
    """Markdown 문법에서 줄을 끝내는 가장 가까운 위치를 반환한다."""

    positions = [text.find(char, start, boundary) for char in _MARKDOWN_LINE_TERMINATORS]
    found = [position for position in positions if position >= 0]
    return min(found, default=boundary)


def _markdown_line_terminator_end(text: str, start: int, boundary: int | None = None) -> int:
    """Markdown 줄 종결자의 다음 위치를 반환한다(CRLF는 한 줄로 소비한다)."""

    limit = len(text) if boundary is None else boundary
    if start >= limit:
        return start
    if text.startswith("\r\n", start) and start + 1 < limit:
        return start + 2
    return start + 1 if _is_markdown_line_terminator(text[start]) else start


def _markdown_line_start(text: str, index: int) -> int:
    """CommonMark 줄 종결자만 사용해 현재 줄의 시작 위치를 찾는다."""

    positions = [text.rfind(char, 0, index) for char in _MARKDOWN_LINE_TERMINATORS]
    latest = max(positions, default=-1)
    if latest < 0:
        return 0
    return _markdown_line_terminator_end(text, latest, index)


def _markdown_advance_column(column: int, char: str) -> int:
    """문자 하나를 소비한 뒤 Markdown의 실제 열 위치를 반환한다."""

    if char == " ":
        return column + 1
    if char == "\t":
        return ((column // 4) + 1) * 4
    return column


def _markdown_leading_indent(text: str, start: int = 0) -> tuple[int, int] | None:
    """공백/탭 선행부의 끝과 절대 열을 반환한다."""

    index = start
    column = 0
    while index < len(text) and text[index] in " \t":
        column = _markdown_advance_column(column, text[index])
        index += 1
    if column > 3:
        return None
    return index, column


def _markdown_consume_marker_padding(text: str, index: int, column: int) -> tuple[int, int, int]:
    """`>` 뒤 선택 공백 한 열과 콘텐츠 들여쓰기를 분리한다.

    CommonMark의 block quote marker는 `>`와 뒤따르는 공백 한 열을 함께
    소비한다. 탭은 문자 단위로 잘라낼 수 없으므로 실제 tab-stop을 전개한
    절대 열에서 delimiter 한 열을 제외하고 나머지를 콘텐츠로 계산한다.
    """

    content_start = column
    if index >= len(text) or text[index] not in " \t":
        return index, column, 0
    column = _markdown_advance_column(column, text[index])
    index += 1
    content_start += 1
    while index < len(text) and text[index] in " \t":
        column = _markdown_advance_column(column, text[index])
        index += 1
    return index, column, column - content_start


def _markdown_fence_container(prefix: str) -> tuple[str, int] | None:
    """fence 앞의 일반 들여쓰기 또는 blockquote 깊이를 반환한다."""

    leading = _markdown_leading_indent(prefix)
    if leading is None:
        return None
    index, column = leading
    if index == len(prefix):
        return ("plain", 0)
    depth = 0
    while index < len(prefix):
        if prefix[index] != ">":
            return None
        depth += 1
        column += 1
        index, column, content_indent = _markdown_consume_marker_padding(prefix, index + 1, column)
        if content_indent > 3:
            return None
        if index < len(prefix) and prefix[index] != ">":
            return None
    return ("blockquote", depth)


def _markdown_fence_candidate(raw_line: str, container: tuple[str, int]) -> tuple[str, int] | None:
    """컨테이너에 맞는 fence 후보와 marker 뒤 들여쓰기 열을 반환한다."""

    kind, expected_depth = container
    if kind == "plain":
        leading = _markdown_leading_indent(raw_line)
        if leading is None:
            return None
        indent_end, indent_columns = leading
        return raw_line[indent_end:], indent_columns

    leading = _markdown_leading_indent(raw_line)
    if leading is None:
        return None
    index, column = leading
    for depth in range(expected_depth):
        if index >= len(raw_line) or raw_line[index] != ">":
            return None
        column += 1
        index, column, content_indent = _markdown_consume_marker_padding(raw_line, index + 1, column)
        if depth + 1 < expected_depth:
            if content_indent > 3 or index >= len(raw_line) or raw_line[index] != ">":
                return None
    return raw_line[index:], content_indent


def _find_inline_span_end(text: str, start: int, run_length: int) -> int | None:
    """Markdown inline span의 닫힘을 같은 문단 안에서만 찾는다."""

    delimiter = "`" * run_length
    boundary = _paragraph_end(text, start)
    index = start + run_length
    while index < boundary:
        if text.startswith(delimiter, index):
            run = 0
            while index + run < boundary and text[index + run] == "`":
                run += 1
            if run == run_length:
                return index
            index += run
            continue
        index += 1
    return None


def _markdown_fence_start_at_line(text: str, line_start: int) -> tuple[int, str] | None:
    """줄 시작에서 유효한 fence delimiter의 위치와 marker를 반환한다."""

    line_end = _find_markdown_line_terminator(text, line_start, len(text))
    raw_line = text[line_start:line_end]
    containers = [("plain", 0)] + [
        ("blockquote", depth) for depth in range(1, raw_line.count(">") + 1)
    ]
    for candidate_container in containers:
        candidate_info = _markdown_fence_candidate(raw_line, candidate_container)
        if candidate_info is None:
            continue
        candidate, indent_columns = candidate_info
        if not candidate:
            continue
        candidate_start = line_start + len(raw_line) - len(candidate)
        # marker 뒤 콘텐츠가 4열 이상이면 같은 container의 fence가 아니라
        # inline code span의 내용이다. tab은 parser가 계산한 실제 열을 쓴다.
        if indent_columns > 3:
            continue
        marker = candidate[0]
        if marker not in "`~":
            continue
        run = 0
        while run < len(candidate) and candidate[run] == marker:
            run += 1
        if run < 3:
            continue
        # CommonMark는 backtick fence의 info string에 backtick을 허용하지 않는다.
        if marker == "`" and "`" in candidate[run:]:
            continue
        return candidate_start, marker
    return None


def _markdown_is_fence_start(text: str, index: int, marker: str) -> bool:
    """같은 위치가 어떤 Markdown container의 실제 block fence인지 확인한다."""

    line_start = _markdown_line_start(text, index)
    candidate = _markdown_fence_start_at_line(text, line_start)
    return candidate == (index, marker)


def _markdown_fence_before(text: str, start: int, boundary: int) -> int | None:
    """범위 안에서 inline 닫힘보다 먼저 시작한 block fence 위치를 찾는다."""

    line_start = _markdown_line_start(text, start)
    line_end = _find_markdown_line_terminator(text, line_start, len(text))
    cursor = _markdown_line_terminator_end(text, line_end)
    while cursor < boundary:
        candidate = _markdown_fence_start_at_line(text, cursor)
        if candidate is not None and candidate[0] < boundary:
            return candidate[0]
        next_end = _find_markdown_line_terminator(text, cursor, len(text))
        cursor = _markdown_line_terminator_end(text, next_end)
    return None


def _markdown_has_fence_before(text: str, start: int, boundary: int) -> bool:
    """범위 안에서 inline 닫힘보다 먼저 시작한 block fence를 찾는다."""

    return _markdown_fence_before(text, start, boundary) is not None


def _mask_inline_opener_delimiter(text: str, start: int, run_length: int) -> tuple[str, int]:
    """block fence 앞 inline span의 delimiter 뒤에서 즉시 lexer를 재개한다."""

    stop = min(start + run_length, len(text))
    return " " * (stop - start), stop


def _find_template_end(text: str, start: int) -> int:
    """단일 backtick template의 끝을 찾아 닫히지 않으면 끝을 반환한다."""

    return _find_backtick_run_end(text, start, 1)


def _is_escaped(text: str, index: int) -> bool:
    """문자 앞의 연속 역슬래시 개수가 홀수인지 확인한다."""

    backslashes = 0
    index -= 1
    while index >= 0 and text[index] == "\\":
        backslashes += 1
        index -= 1
    return bool(backslashes % 2)


def _mask_mdx_fence(text: str, start: int, marker: str) -> tuple[str, int]:
    """MDX의 줄 단위 backtick/tilde fence 전체를 공백으로 가린다."""

    line_start = _markdown_line_start(text, start)
    container = _markdown_fence_container(text[line_start:start])
    opener_end = _find_markdown_line_terminator(text, start, len(text))
    opener_run = 0
    while start + opener_run < opener_end and text[start + opener_run] == marker:
        opener_run += 1
    if opener_run < 3:
        return "", start
    if container is None and marker != "`":
        return "", start
    # CommonMark backtick fence의 info string에는 backtick을 넣을 수 없다.
    # 이 경계가 없으면 파일 첫 inline code span을 unclosed fence로 가린다.
    if marker == "`" and (
        container is None or "`" in text[start + opener_run : opener_end]
    ):
        # 무효한 fence는 같은 문단의 정상 inline span으로 되돌린다. 다만
        # 닫힘 delimiter가 줄 시작의 유효한 block fence라면 inline span의
        # 닫힘으로 취급하지 않고 현재 줄만 격리해 다음 실행식을 검사한다.
        closing = _find_inline_span_end(text, start, opener_run)
        if (
            closing is not None
            and not _markdown_has_fence_before(text, opener_end, closing)
            and not _markdown_is_fence_start(text, closing, marker)
        ):
            stop = min(closing + opener_run, len(text))
            segment = list(text[start:stop])
            for offset, char in enumerate(segment):
                if not _is_markdown_line_terminator(char):
                    segment[offset] = " "
            return "".join(segment), stop
        return _mask_inline_opener_delimiter(text, start, opener_run)
    cursor = _markdown_line_terminator_end(text, opener_end)
    closing = len(text)
    while cursor < len(text):
        next_end = _find_markdown_line_terminator(text, cursor, len(text))
        raw_line = text[cursor:next_end]
        candidate_info = _markdown_fence_candidate(raw_line, container)
        if candidate_info is None:
            if container[0] == "blockquote":
                closing = cursor
                break
            cursor = _markdown_line_terminator_end(text, next_end)
            continue
        candidate, indent_columns = candidate_info
        if indent_columns > 3:
            cursor = _markdown_line_terminator_end(text, next_end)
            continue
        closing_run = 0
        while closing_run < len(candidate) and candidate[closing_run] == marker:
            closing_run += 1
        if closing_run >= opener_run and not candidate[closing_run:].strip(" \t"):
            closing = _markdown_line_terminator_end(text, next_end)
            break
        cursor = _markdown_line_terminator_end(text, next_end)
    output = list(text[start:closing])
    for offset, char in enumerate(text[start:closing]):
        if not _is_markdown_line_terminator(char):
            output[offset] = " "
    return "".join(output), closing


def _mask_template_interpolation_comments(text: str) -> str:
    """template 보간식 안의 JavaScript 주석만 공백으로 치환한다."""

    output = list(text)
    index = 0
    while index + 1 < len(text):
        if text[index : index + 2] != "${" or _is_escaped(text, index):
            index += 1
            continue
        index += 2
        depth = 1
        quote: str | None = None
        while index < len(text) and depth:
            char = text[index]
            next_char = text[index + 1] if index + 1 < len(text) else ""
            if quote:
                if char == "\\":
                    index += 2
                    continue
                if char == quote:
                    quote = None
                index += 1
                continue
            if char in "\"'`":
                quote = char
                index += 1
                continue
            if char == "/" and next_char == "/":
                output[index] = output[index + 1] = " "
                index += 2
                while index < len(text) and not _is_mdx_line_terminator(text[index]):
                    output[index] = " "
                    index += 1
                continue
            if char == "/" and next_char == "*":
                output[index] = output[index + 1] = " "
                index += 2
                while index < len(text):
                    if text[index] == "*" and index + 1 < len(text) and text[index + 1] == "/":
                        output[index] = output[index + 1] = " "
                        index += 2
                        break
                    output[index] = text[index] if _is_mdx_line_terminator(text[index]) else " "
                    index += 1
                continue
            if char == "{":
                depth += 1
            elif char == "}":
                depth -= 1
            index += 1
    return "".join(output)


def _mask_script_comments(text: str) -> str:
    """TS·TSX·CSS의 기존 문자열 보존과 주석 제외 동작을 유지한다."""

    output = list(text)
    index = 0
    while index < len(text):
        char = text[index]
        if char in "\"'":
            quote = char
            index += 1
            while index < len(text):
                if text[index] == "\\":
                    index += 2
                elif text[index] == quote:
                    index += 1
                    break
                else:
                    index += 1
            continue
        if char == "`":
            stop = min(_find_template_end(text, index) + 1, len(text))
            output[index:stop] = _mask_template_interpolation_comments(text[index:stop])
            index = stop
            continue
        if text[index:index + 2] in {"//", "/*"}:
            if text[index:index + 2] == "//":
                stop = _find_mdx_line_terminator(text, index + 2, len(text))
            else:
                closing = text.find("*/", index + 2)
                stop = len(text) if closing < 0 else closing + 2
            for offset in range(index, stop):
                if not _is_mdx_line_terminator(text[offset]):
                    output[offset] = " "
            index = stop
            continue
        index += 1
    return "".join(output)


def _mask_mdx_source(text: str) -> str:
    """문서·태그·JS·template의 수명을 스택으로 추적해 인용과 주석을 가린다.

    문서에서 JS로 들어가는 입구는 중괄호, JSX 속성, 줄 시작 선언뿐이다.
    JS 안의 빈 줄은 문맥을 닫지 않는다. 닫힘 delimiter를 소비한 후에만
    이전 문맥으로 돌아가므로 본문 URL·문장부호가 JS 상태에 섞이지 않는다.
    """

    output = list(text)
    # (문맥, 닫힘 괄호 스택, 마지막 토큰): 재귀 호출 없이 중첩을 처리한다.
    frames: list[dict[str, object]] = [{"kind": "prose"}]
    index = 0

    def mask(start: int, stop: int) -> None:
        for offset in range(start, stop):
            if not _is_mdx_line_terminator(text[offset]):
                output[offset] = " "

    def code(kind: str, closes: list[str]) -> dict[str, object]:
        return {"kind": kind, "closes": closes, "last": "", "operand": True}

    while index < len(text):
        frame = frames[-1]
        kind = frame["kind"]
        char = text[index]
        following = text[index:index + 2]

        if kind == "template":
            if char == "\\":
                index += 2
            elif following == "${":
                frames.append(code("expression", ["}"]))
                index += 2
            elif char == "`":
                frames.pop()
                index += 1
            else:
                index += 1
            continue

        if kind in {"prose", "jsx-text"}:
            # 유효한 block fence가 inline delimiter보다 우선한다.
            if kind == "prose" and char in "`~" and text.startswith(char * 3, index):
                segment, stop = _mask_mdx_fence(text, index, char)
                if stop > index:
                    output[index:stop] = segment
                    index = stop
                    continue
            if kind == "prose" and char == "`" and not _is_escaped(text, index):
                run = 1
                while index + run < len(text) and text[index + run] == "`":
                    run += 1
                end = _find_inline_span_end(text, index, run)
                if end is not None and not _markdown_has_fence_before(text, index, end):
                    mask(index, end + run)
                    index = end + run
                else:
                    # 닫히지 않은 delimiter는 본문 문자다. 뒤의 표현식·태그를
                    # 찾기 위해 별도 lexer를 실행하거나 문단을 건너뛰지 않는다.
                    index += run
                continue
            if char == "{" and not _is_escaped(text, index):
                frames.append(code("expression", ["}"]))
                index += 1
                continue
            if char == "<" and not _is_escaped(text, index) and re.match(r"</?(?:[A-Za-z]|>)", text[index:]):
                frames.append({"kind": "tag", "script": kind == "jsx-text", "closing": following == "</"})
                index += 1
                continue
            if kind == "prose":
                prefix = text[_markdown_line_start(text, index):index]
                at_start = bool(re.fullmatch(r"[ \t]*(?:>[ \t]*)*", prefix))
                if at_start and ">" not in prefix and (
                    re.match(r"(?:import|export)(?=\s|\{)", text[index:])
                    # 기존 도구의 선언형 문서 예제 지원. 제어문 단어만으로는
                    # JS를 시작하지 않고 선언 식별자와 대입 구문을 요구한다.
                    or re.match(r"(?:const|let|var)\s+[\w$]+\s*=", text[index:])
                ):
                    frames.append(code("esm", []))
                    continue
                if at_start and following in {"//", "/*"}:
                    # 줄 전체 주석 예제에 대한 기존 검사 계약을 유지한다.
                    frames.append(code("esm", []))
                    continue
            index += 1
            continue

        if kind == "tag":
            if char in "\"'":
                quote = char
                index += 1
                while index < len(text) and text[index] != quote:
                    index += 1
                index += index < len(text)
            elif char == "{":
                frames.append(code("expression", ["}"]))
                index += 1
            elif char == ">":
                tag = frames.pop()
                if tag["script"]:
                    if tag["closing"]:
                        if frames[-1]["kind"] == "jsx-text":
                            frames.pop()
                    elif index == 0 or text[index - 1] != "/":
                        frames.append({"kind": "jsx-text"})
                index += 1
            else:
                index += 1
            continue

        # 이하에서는 JS 표현식 또는 ESM이 현재 문맥이다.
        closes = frame["closes"]
        if following in {"//", "/*"}:
            if following == "//":
                stop = _find_mdx_line_terminator(text, index + 2, len(text))
            else:
                end = text.find("*/", index + 2)
                stop = len(text) if end < 0 else end + 2
            mask(index, stop)
            index = stop
            continue
        if char in "\"'":
            quote = char
            index += 1
            while index < len(text):
                if text[index] == "\\":
                    index += 2
                elif text[index] == quote:
                    index += 1
                    break
                else:
                    index += 1
            frame["last"] = "value"
            frame["operand"] = False
            continue
        if char == "`":
            frame["last"] = "value"
            frame["operand"] = False
            frames.append({"kind": "template"})
            index += 1
            continue
        if char == "/" and frame["operand"]:
            # 정규식 내부의 slash·괄호는 JS 주석이나 표현식 닫힘이 아니다.
            cursor = index + 1
            in_class = False
            while cursor < len(text) and not _is_mdx_line_terminator(text[cursor]):
                if text[cursor] == "\\":
                    cursor += 2
                    continue
                if text[cursor] == "[":
                    in_class = True
                elif text[cursor] == "]":
                    in_class = False
                elif text[cursor] == "/" and not in_class:
                    index = cursor + 1
                    frame["last"] = "value"
                    frame["operand"] = False
                    break
                cursor += 1
            else:
                index += 1
            continue
        if char == "<" and re.match(r"<(?:[A-Za-z]|>)", text[index:]):
            frame["last"] = "value"
            frame["operand"] = False
            frames.append({"kind": "tag", "script": True, "closing": False})
            index += 1
            continue
        if char in "({[":
            closes.append({"(": ")", "{": "}", "[": "]"}[char])
            frame["last"] = char
            frame["operand"] = True
        elif char in ")}]":
            if closes and closes[-1] == char:
                closes.pop()
                if kind == "expression" and not closes:
                    frames.pop()
            frame["last"] = char
            frame["operand"] = False
        elif _is_mdx_line_terminator(char):
            if kind == "esm" and not closes and frame["last"] not in {
                "=", "=>", ",", ".", "+", "-", "*", "/", "?", ":", "&", "|",
                "import", "export", "default", "from", "const", "let", "var", "return",
            }:
                frames.pop()
        elif char.isalpha() or char in "_$" or char.isdigit():
            end = index + 1
            while end < len(text) and (text[end].isalnum() or text[end] in "_$"):
                end += 1
            word = text[index:end]
            frame["last"] = word
            frame["operand"] = word in {"return", "throw", "case", "typeof", "void", "delete", "new", "yield", "await"}
            index = end
            continue
        elif not _is_mdx_whitespace(char):
            frame["last"] = "=>" if following == "=>" else char
            frame["operand"] = char not in "."
            if following == "=>":
                index += 2
                continue
        index += 1
    return "".join(output)


def _mask_comments_and_backticks(text: str, ignore_backticks: bool) -> str:
    """확장자별 문법 처리기를 선택하며 결과의 원본 위치를 유지한다."""

    return _mask_mdx_source(text) if ignore_backticks else _mask_script_comments(text)


def _relative(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except (OSError, RuntimeError, ValueError):
        raise UxLintError("검사 경로가 작업 root 밖에 있습니다")


def collect_files(inputs: Sequence[Path], root: Path) -> list[tuple[Path, str]]:
    """입력 파일·디렉터리에서 검사 대상 확장자만 수집한다."""

    result: dict[str, Path] = {}
    for item in inputs:
        if not item.exists():
            raise UxLintError("검사 대상을 찾을 수 없습니다")
        base = item if item.is_dir() else None
        candidates = [item] if item.is_file() else [path for path in item.rglob("*") if path.is_file()]
        for path in candidates:
            if path.suffix.lower() not in TARGET_EXTENSIONS:
                continue
            relative_to_input = path.relative_to(base).parts if base else ()
            if (base and any(part in SKIP_DIRECTORIES for part in relative_to_input[:-1])) or ".test." in path.name or path.name.endswith(".gen.ts"):
                continue
            relative = _relative(path, root)
            result[relative] = path
    return sorted((path, relative) for relative, path in result.items())


def scan_file(path: Path, relative: str, token_files: set[str]) -> list[dict[str, object]]:
    try:
        text = _read_text_preserving_newlines(path)
    except (OSError, UnicodeError) as error:
        raise UxLintError("검사 파일을 읽을 수 없습니다") from error
    masked = _mask_comments_and_backticks(text, ignore_backticks=path.suffix.lower() == ".mdx")
    findings: list[dict[str, object]] = []
    for name, description, pattern in COMPILED_PATTERNS:
        if name == "P4b" and (path.suffix.lower() != ".css" or relative in token_files):
            continue
        for match in pattern.finditer(masked):
            line = masked.count("\n", 0, match.start()) + 1
            line_start = masked.rfind("\n", 0, match.start()) + 1
            column = match.start() - line_start + 1
            findings.append(
                {
                    "file": relative,
                    "line": line,
                    "column": column,
                    "pattern": name,
                    "description": description,
                }
            )
    return sorted(findings, key=lambda finding: (int(finding["line"]), int(finding["column"]), str(finding["pattern"])))


def _git_output(root: Path, args: Sequence[str]) -> str:
    try:
        completed = subprocess.run(["git", "-C", str(root), *args], check=False, capture_output=True)
    except (OSError, UnicodeError) as error:
        raise UxLintError("git diff를 실행할 수 없습니다") from error
    if completed.returncode != 0:
        raise UxLintError("Git 명령을 실행할 수 없습니다")
    try:
        return completed.stdout.decode("utf-8")
    except UnicodeError as error:
        raise UxLintError("Git 출력이 UTF-8이 아닙니다") from error


def git_root(path: Path) -> Path:
    """검사 대상이 속한 Git top-level을 반환한다."""

    probe = path if path.is_dir() else path.parent
    try:
        output = _git_output(probe, ["rev-parse", "--show-toplevel"]).strip()
    except UxLintError as error:
        raise UxLintError("검사 root의 Git 저장소를 찾을 수 없습니다") from error
    if not output:
        raise UxLintError("검사 root의 Git 저장소를 찾을 수 없습니다")
    return Path(output).resolve()


def resolve_base(root: Path, base: str) -> str:
    """옵션으로 해석되지 않도록 기준 ref를 commit SHA로 고정한다."""

    try:
        return _git_output(root, ["rev-parse", "--verify", "--end-of-options", f"{base}^{{commit}}"]).strip()
    except UxLintError as error:
        raise UxLintError("--base 커밋을 확인할 수 없습니다") from error


def _is_tracked(root: Path, relative: str) -> bool:
    try:
        completed = subprocess.run(
            ["git", "-C", str(root), "ls-files", "--error-unmatch", "--", relative],
            check=False,
            capture_output=True,
        )
    except (OSError, UnicodeError) as error:
        raise UxLintError("Git 파일 상태를 확인할 수 없습니다") from error
    return completed.returncode == 0 and bool(completed.stdout.strip())


def added_lines(root: Path, base: str, files: Mapping[str, Path]) -> dict[str, set[int]]:
    """파일별 git diff -U0에서 추가 행을 추출한다(인용 경로도 보존)."""

    if not files:
        raise UxLintError("--base에는 검사할 파일이 필요합니다")
    result: dict[str, set[int]] = defaultdict(set)
    for relative, path in files.items():
        if not _is_tracked(root, relative):
            try:
                source = _read_text_preserving_newlines(path)
                line_count = source.count("\n") + (1 if source and not source.endswith("\n") else 0)
            except (OSError, UnicodeError) as error:
                raise UxLintError("검사 파일을 읽을 수 없습니다") from error
            result[relative].update(range(1, line_count + 1))
            continue
        output = _git_output(root, ["diff", "--no-ext-diff", "--unified=0", base, "--", relative])
        current_line: int | None = None
        for raw_line in output.split("\n"):
            if raw_line.startswith("@@"):
                match = re.search(r"\+(\d+)(?:,(\d+))?", raw_line)
                current_line = int(match.group(1)) if match else None
                continue
            if current_line is None:
                continue
            if raw_line.startswith("+"):
                result[relative].add(current_line)
                current_line += 1
            elif raw_line.startswith(" "):
                current_line += 1
    return result


def load_baseline(path: Path) -> list[dict[str, object]]:
    try:
        data = json.loads(_read_text_preserving_newlines(path))
    except (OSError, UnicodeError, ValueError, RecursionError, json.JSONDecodeError) as error:
        raise UxLintError("baseline JSON을 읽을 수 없습니다") from error
    if not isinstance(data, dict) or data.get("schema") != "kor-travel-common.ux-baseline.v1":
        raise UxLintError("UX baseline schema가 kor-travel-common.ux-baseline.v1이 아닙니다")
    entries = data.get("entries")
    if not isinstance(entries, list):
        raise UxLintError("UX baseline은 entries 배열이어야 합니다")
    result: list[dict[str, object]] = []
    for entry in entries:
        required = ("rule", "path", "count", "reason", "until", "task")
        if not isinstance(entry, dict) or not all(key in entry for key in required):
            raise UxLintError("UX baseline 항목 필드가 부족합니다")
        if not isinstance(entry["rule"], str) or entry["rule"] not in KNOWN_RULES:
            raise UxLintError("UX baseline rule 형식이 잘못되었습니다")
        if not isinstance(entry["path"], str) or not entry["path"] or Path(entry["path"]).is_absolute() or "\\" in entry["path"]:
            raise UxLintError("UX baseline path 형식이 잘못되었습니다")
        if isinstance(entry["count"], bool) or not isinstance(entry["count"], int):
            raise UxLintError("UX baseline count 형식이 잘못되었습니다")
        if not isinstance(entry["until"], str):
            raise UxLintError("UX baseline until 형식이 잘못되었습니다")
        try:
            count = entry["count"]
            until = entry["until"]
            from datetime import date

            date.fromisoformat(until)
        except (TypeError, ValueError, OverflowError) as error:
            raise UxLintError("UX baseline count/until 형식이 잘못되었습니다") from error
        if count < 0:
            raise UxLintError("UX baseline count는 0 이상이어야 합니다")
        if not isinstance(entry["reason"], str) or not entry["reason"] or not isinstance(entry["task"], str) or not entry["task"]:
            raise UxLintError("UX baseline reason/task 형식이 잘못되었습니다")
        result.append({"rule": entry["rule"], "path": entry["path"].replace("\\", "/"), "count": count, "reason": entry["reason"], "until": until, "task": entry["task"]})
    return result


def apply_baseline(
    findings: Sequence[Mapping[str, object]],
    entries: Sequence[Mapping[str, object]],
    root_prefix: str = "",
    added: Mapping[str, set[int]] | None = None,
) -> list[dict[str, object]]:
    from datetime import date

    today = date.today()
    limits = {
        (str(entry["path"]), str(entry["rule"])): int(entry["count"])
        for entry in entries
        if date.fromisoformat(str(entry["until"])) >= today
    }
    grouped: defaultdict[tuple[str, str], list[int]] = defaultdict(list)
    for index, finding in enumerate(findings):
        finding_path = str(finding["file"])
        relative_to_root = finding_path
        if root_prefix and finding_path.startswith(root_prefix.rstrip("/") + "/"):
            relative_to_root = finding_path[len(root_prefix.rstrip("/")) + 1 :]
        candidates = [(finding_path, str(finding["pattern"])), (relative_to_root, str(finding["pattern"]))]
        key = next((candidate for candidate in candidates if candidate in limits), candidates[0])
        grouped[key].append(index)
    result: list[dict[str, object]] = []
    exemptions: dict[int, bool] = {}
    for key, indices in grouped.items():
        ordered = sorted(
            indices,
            key=lambda index: (
                1 if added is not None and int(findings[index]["line"]) in added.get(str(findings[index]["file"]), set()) else 0,
                int(findings[index]["line"]),
                int(findings[index]["column"]),
            ),
        )
        limit = limits.get(key, 0)
        for rank, index in enumerate(ordered):
            exemptions[index] = rank < limit
    for index, finding in enumerate(findings):
        item = dict(finding)
        finding_path = str(finding["file"])
        relative_to_root = finding_path
        if root_prefix and finding_path.startswith(root_prefix.rstrip("/") + "/"):
            relative_to_root = finding_path[len(root_prefix.rstrip("/")) + 1 :]
        candidates = [(finding_path, str(finding["pattern"])), (relative_to_root, str(finding["pattern"]))]
        key = next((candidate for candidate in candidates if candidate in limits), candidates[0])
        item["baseline"] = limits.get(key, 0)
        item["exempt"] = exemptions.get(index, False)
        result.append(item)
    return result


def render_markdown(findings: Sequence[Mapping[str, object]], fail_count: int, mode: str, expired: Sequence[Mapping[str, object]]) -> str:
    status = "EXEMPT_EXPIRED" if expired else ("PASS" if fail_count == 0 else "FAIL")
    lines = [f"### ux_lint ({mode})", "", f"- 상태: **{status}**", f"- 발견: {len(findings)}건 · 실패 대상: {fail_count}건"]
    counts: defaultdict[str, int] = defaultdict(int)
    for finding in findings:
        counts[str(finding["pattern"])] += 1
    if counts:
        lines.append("- 패턴별 건수: " + ", ".join(f"{name}={counts[name]}" for name, _, _ in PATTERNS))
    if expired:
        lines.append(f"- 만료 baseline: {len(expired)}건")
    if findings:
        lines.extend(["", "| 파일 | 행 | 패턴 | 판정 |", "|---|---:|---|---|"])
        for finding in findings:
            state = "EXEMPT" if finding.get("exempt") else ("FAIL" if finding.get("fail") else "REPORT")
            lines.append(f"| `{_public_path(str(finding['file']))}` | {finding['line']} | `{finding['pattern']}` | {state} |")
    return "\n".join(lines) + "\n"


def write_step_summary(content: str, explicit: str | None) -> None:
    target = explicit or os.environ.get("GITHUB_STEP_SUMMARY")
    if not target:
        return
    try:
        with Path(target).open("a", encoding="utf-8", newline="\n") as handle:
            handle.write(content)
    except OSError as error:
        raise UxLintError("step summary를 쓸 수 없습니다") from error


def build_parser() -> argparse.ArgumentParser:
    parser = _UxArgumentParser(description="공통 UX 금지 패턴을 검사합니다.")
    parser.add_argument("paths", nargs="*", type=Path, help="파일 또는 디렉터리")
    parser.add_argument("--root", type=Path, help="검사할 프런트엔드 루트")
    parser.add_argument("--token-files", help="P4b raw 색상을 허용할 토큰 파일 목록(쉼표 구분)")
    parser.add_argument("--base", help="git diff 기준 커밋; 추가 행만 실패 처리")
    parser.add_argument("--baseline", type=Path, help="기존 위반 건수 JSON")
    parser.add_argument("--fail-new", action="store_true", help="baseline을 초과한 위반을 실패 처리합니다")
    parser.add_argument("--json", action="store_true", dest="as_json", help="JSON으로 출력합니다")
    parser.add_argument("--step-summary", type=str, help="GitHub step summary 파일 경로")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    workspace = Path.cwd().resolve()
    try:
        args = parser.parse_args(argv)
        try:
            scan_root = (args.root or workspace).resolve()
        except (OSError, RuntimeError) as error:
            raise UxLintError("검사 root를 확인할 수 없습니다") from error
        if args.root and not scan_root.exists():
            raise UxLintError("검사 root를 찾을 수 없습니다")
        inputs = ([scan_root] if args.root else []) + list(args.paths)
        if not inputs:
            raise UxLintError("검사할 파일 또는 --root가 필요합니다")
        files = collect_files(inputs, scan_root)
        token_files = set()
        if args.token_files:
            for item in args.token_files.split(","):
                candidate = item.strip()
                if candidate:
                    candidate_path = Path(candidate)
                    if not candidate_path.is_absolute():
                        candidate_path = scan_root / candidate_path
                    token_files.add(_relative(candidate_path, scan_root))
        findings = [finding for path, relative in files for finding in scan_file(path, relative, token_files)]
        baseline = load_baseline(args.baseline) if args.baseline else []
        base_sha: str | None = None
        added: dict[str, set[int]] = {}
        if args.base:
            repository = git_root(scan_root)
            base_sha = resolve_base(repository, args.base)
            git_files: dict[str, Path] = {}
            scan_to_git: dict[str, str] = {}
            for path, relative in files:
                try:
                    git_relative = path.resolve().relative_to(repository).as_posix()
                except ValueError as error:
                    raise UxLintError("검사 파일이 Git 저장소 밖에 있습니다") from error
                git_files[git_relative] = path
                scan_to_git[relative] = git_relative
            raw_added = added_lines(repository, base_sha, git_files)
            added = {relative: raw_added.get(git_relative, set()) for relative, git_relative in scan_to_git.items()}
        findings = apply_baseline(findings, baseline, added=added if args.base else None)
        should_fail = bool(args.base or args.fail_new)
        for finding in findings:
            is_added = not args.base or int(finding["line"]) in added.get(str(finding["file"]), set())
            finding["added"] = is_added
            finding["fail"] = bool(should_fail and is_added and not finding.get("exempt", False))
        fail_count = sum(1 for finding in findings if finding.get("fail"))
        from datetime import date

        expired = [
            {"rule": entry["rule"], "path": _public_path(str(entry["path"])), "count": entry["count"], "until": entry["until"]}
            for entry in baseline
            if date.fromisoformat(str(entry["until"])) < date.today()
        ]
        status = "EXEMPT_EXPIRED" if expired else ("PASS" if fail_count == 0 else "FAIL")
        public_findings = []
        for finding in findings:
            public_finding = dict(finding)
            public_finding["file"] = _public_path(str(finding["file"]))
            public_findings.append(public_finding)
        payload = {"tool": "ux_lint", "status": status, "findings": public_findings, "fail_count": fail_count, "base": base_sha, "expired": expired}
        markdown = render_markdown(findings, fail_count, "diff" if args.base else "report", expired)
        write_step_summary(markdown, args.step_summary)
        if args.as_json:
            print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
        else:
            print(markdown, end="")
        return 1 if status in {"FAIL", "EXEMPT_EXPIRED"} else 0
    except UxLintError as error:
        print(f"ux_lint 오류: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
