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


def _find_template_end(text: str, start: int) -> int:
    """단일 backtick template의 끝을 찾아 닫히지 않으면 끝을 반환한다."""

    return _find_backtick_run_end(text, start, 1)


def _has_open_jsx_expression(text: str, start: int) -> bool:
    """JSX 속성의 중첩 중괄호가 현재 위치까지 열려 있는지 확인한다."""

    before = text[:start]
    matches = list(re.finditer(r"[A-Za-z_$][\w$-]*\s*=\s*\{", before))
    for match in reversed(matches):
        scope_start = max(before.rfind(";", 0, match.start()), before.rfind("\n\n", 0, match.start())) + 1
        if not re.search(r"<[A-Za-z]", before[scope_start : match.start()]):
            continue
        balance = 0
        quote: str | None = None
        index = match.end() - 1
        while index < len(before):
            char = before[index]
            if quote:
                if char == "\\":
                    index += 2
                    continue
                if char == quote:
                    quote = None
            elif char in "\"'`":
                quote = char
            elif char == "{":
                balance += 1
            elif char == "}":
                balance -= 1
            index += 1
        if balance > 0:
            return True
    return False


def _is_executable_mdx_template(text: str, start: int, end: int) -> bool:
    """MDX의 Markdown code span과 JSX/JavaScript template을 구분한다."""

    line_start = text.rfind("\n", 0, start) + 1
    line_prefix = text[line_start:start]
    leading = line_prefix.lstrip()
    if leading.startswith(">"):
        leading = leading[1:].lstrip()
        if not re.search(r"(?:[A-Za-z_$][\w$-]*\s*=\s*\{|<[A-Za-z])", leading):
            return False
    prefix = leading.rstrip()

    # JSX 속성의 `{...}` 안에서는 tag 이름·배열·삼항식·computed tag를
    # 구분하지 않고 모두 JavaScript template으로 취급한다. Markdown 본문은
    # 해당 중괄호 문맥을 갖지 않으므로 inline code를 계속 제외한다.
    if re.search(r"[A-Za-z_$][\w$-]*\s*=\s*\{[^{}]*$", prefix):
        return True
    if re.search(r"<(?:[A-Za-z][\w.-]*|[A-Z][\w.-]*)[^>]*\{[^{}]*$", prefix):
        return True

    # JSX/ESM 식이 여러 줄로 끊겨도 파일 앞부분의 열린 expression과
    # 선언 문맥을 유지한다. 마지막 중괄호가 열린 속성보다 뒤에 있으면
    # Markdown 본문의 일반적인 `{...}` 인용은 실행 코드로 바꾸지 않는다.
    before = text[:start]
    if _has_open_jsx_expression(text, start):
        return True
    statement = before[max(before.rfind(";"), before.rfind("\n\n")) + 1 :]
    previous_line = text[:line_start].splitlines()[-1].rstrip() if line_start else ""
    declaration = bool(re.search(r"\b(?:export\s+)?(?:const|let|var)\b", statement)) and "=" in statement
    if declaration and (line_prefix != line_prefix.lstrip() or re.search(r"(?:=|=>|[([{,:])\s*$", previous_line)):
        return True

    # MDX ESM/JavaScript 선언의 값 template과 return/template tag도 실행
    # 문맥이다. 선언의 오른쪽에 이미 식이 시작됐는지 확인해 `Example: `...
    # `` 같은 문장형 Markdown을 실행 코드로 오인하지 않는다.
    if re.match(r"\s*(?:export\s+)?(?:const|let|var)\b", prefix) and "=" in prefix:
        return True
    if re.search(r"(?:\breturn|=>)\s+[^\n]*$", prefix):
        return True
    if prefix and prefix[-1] in "={([,?:":
        return bool(re.search(r"(?:className|style|\b(?:const|let|var|return|export)\b|=>|<[A-Za-z])", prefix))
    return False


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

    line_start = text.rfind("\n", 0, start) + 1
    if text[line_start:start].strip():
        return "", start
    opener_end = text.find("\n", start)
    if opener_end < 0:
        opener_end = len(text)
    opener_run = 0
    while start + opener_run < opener_end and text[start + opener_run] == marker:
        opener_run += 1
    if opener_run < 3:
        return "", start
    line_end = opener_end
    if line_end < 0:
        line_end = len(text)
    cursor = line_end + 1
    closing = len(text)
    while cursor < len(text):
        next_end = text.find("\n", cursor)
        if next_end < 0:
            next_end = len(text)
        candidate = text[cursor:next_end].lstrip()
        closing_run = 0
        while closing_run < len(candidate) and candidate[closing_run] == marker:
            closing_run += 1
        if closing_run >= opener_run and not candidate[closing_run:].strip():
            closing = next_end + (1 if next_end < len(text) else 0)
            break
        cursor = next_end + 1
    output = list(text[start:closing])
    for offset, char in enumerate(text[start:closing]):
        if char != "\n":
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
                while index < len(text) and text[index] != "\n":
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
                    output[index] = "\n" if text[index] == "\n" else " "
                    index += 1
                continue
            if char == "{":
                depth += 1
            elif char == "}":
                depth -= 1
            index += 1
    return "".join(output)


def _mask_comments_and_backticks(text: str, ignore_backticks: bool) -> str:
    """주석과 Markdown 인용만 공백으로 가리고 실행 template은 보존한다."""

    output = list(text)
    state = "code"
    quote: str | None = None
    index = 0
    while index < len(text):
        char = text[index]
        next_char = text[index + 1] if index + 1 < len(text) else ""
        if state == "line-comment":
            if char == "\n":
                state = "code"
            else:
                output[index] = " "
            index += 1
            continue
        if state == "block-comment":
            if char == "*" and next_char == "/":
                output[index] = output[index + 1] = " "
                index += 2
                state = "code"
                continue
            if char != "\n":
                output[index] = " "
            index += 1
            continue
        if quote:
            if char == "\\":
                index += 2
                continue
            if char == quote:
                quote = None
            index += 1
            continue
        if char in "\"'":
            quote = char
            index += 1
            continue
        if ignore_backticks and char == "~" and text.startswith("~~~", index):
            segment, stop = _mask_mdx_fence(text, index, "~")
            if stop != index:
                output[index:stop] = list(segment)
                index = stop
                continue
        if char == "`":
            run_length = 0
            while index + run_length < len(text) and text[index + run_length] == "`":
                run_length += 1
            if ignore_backticks and run_length >= 3:
                segment, stop = _mask_mdx_fence(text, index, "`")
                if stop != index:
                    output[index:stop] = list(segment)
                    index = stop
                    continue
            if ignore_backticks and run_length >= 2:
                end = _find_backtick_run_end(text, index, run_length)
                if end >= len(text):
                    for offset in range(index, min(index + run_length, len(text))):
                        output[offset] = " "
                    index += run_length
                    continue
                stop = min(end + run_length, len(text)) if end < len(text) else len(text)
                for offset in range(index, stop):
                    if text[offset] != "\n":
                        output[offset] = " "
                index = stop
                continue
            end = _find_template_end(text, index)
            executable = not ignore_backticks or _is_executable_mdx_template(text, index, end)
            stop = min(end + 1, len(text))
            if executable:
                segment = _mask_template_interpolation_comments(text[index:stop])
                output[index:stop] = list(segment)
            else:
                for offset in range(index, stop):
                    if text[offset] != "\n":
                        output[offset] = " "
            index = stop
            continue
        if char == "/" and next_char == "/":
            output[index] = output[index + 1] = " "
            state = "line-comment"
            index += 2
            continue
        if char == "/" and next_char == "*":
            output[index] = output[index + 1] = " "
            state = "block-comment"
            index += 2
            continue
        index += 1
    return "".join(output)


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
        text = path.read_text(encoding="utf-8")
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
        completed = subprocess.run(["git", "-C", str(root), *args], check=False, capture_output=True, text=True, encoding="utf-8")
    except (OSError, UnicodeError) as error:
        raise UxLintError("git diff를 실행할 수 없습니다") from error
    if completed.returncode != 0:
        raise UxLintError("Git 명령을 실행할 수 없습니다")
    return completed.stdout


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
            text=True,
            encoding="utf-8",
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
                line_count = len(path.read_text(encoding="utf-8").splitlines())
            except (OSError, UnicodeError) as error:
                raise UxLintError("검사 파일을 읽을 수 없습니다") from error
            result[relative].update(range(1, line_count + 1))
            continue
        output = _git_output(root, ["diff", "--no-ext-diff", "--unified=0", base, "--", relative])
        current_line: int | None = None
        for raw_line in output.splitlines():
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
        data = json.loads(path.read_text(encoding="utf-8"))
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
