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


def _mask_comments_and_backticks(text: str) -> str:
    """주석·백틱 영역을 공백으로 가려 줄 번호와 열 번호를 유지한다."""

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
        if state == "backtick":
            if char == "\\":
                output[index] = " "
                if index + 1 < len(text):
                    output[index + 1] = "\n" if text[index + 1] == "\n" else " "
                index += 2
                continue
            if char == "`":
                output[index] = " "
                state = "code"
            elif char != "\n":
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
        if char == "`":
            output[index] = " "
            state = "backtick"
            index += 1
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
    except ValueError:
        return path.name


def collect_files(inputs: Sequence[Path], root: Path) -> list[tuple[Path, str]]:
    """입력 파일·디렉터리에서 검사 대상 확장자만 수집한다."""

    result: dict[str, Path] = {}
    for item in inputs:
        if not item.exists():
            raise UxLintError(f"대상을 찾을 수 없습니다: {item.name}")
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
        raise UxLintError(f"파일을 읽을 수 없습니다: {relative}") from error
    masked = _mask_comments_and_backticks(text)
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
        raise UxLintError("--base 커밋을 확인할 수 없습니다")
    return completed.stdout


def added_lines(root: Path, base: str, files: Sequence[str]) -> dict[str, set[int]]:
    """git diff -U0에서 추가된 파일·행을 추출한다."""

    if not files:
        raise UxLintError("--base에는 검사할 파일이 필요합니다")
    output = _git_output(root, ["-c", "core.quotePath=false", "diff", "--no-ext-diff", "--unified=0", base, "--", *files])
    result: dict[str, set[int]] = defaultdict(set)
    current: str | None = None
    current_line: int | None = None
    for raw_line in output.splitlines():
        if raw_line.startswith("+++ b/"):
            current = raw_line[6:]
            current_line = None
            continue
        if raw_line.startswith("@@"):
            match = re.search(r"\+(\d+)(?:,(\d+))?", raw_line)
            if match:
                current_line = int(match.group(1))
            continue
        if current is None or current_line is None:
            continue
        if raw_line.startswith("+"):
            if not raw_line.startswith("+++"):
                result[current].add(current_line)
            current_line += 1
        elif raw_line.startswith(" "):
            current_line += 1
    return result


def load_baseline(path: Path) -> list[dict[str, object]]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise UxLintError(f"baseline JSON을 읽을 수 없습니다: {path.name}") from error
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
        try:
            count = int(entry["count"])
            until = str(entry["until"])
            from datetime import date

            date.fromisoformat(until)
        except (TypeError, ValueError) as error:
            raise UxLintError("UX baseline count/until 형식이 잘못되었습니다") from error
        if count < 0:
            raise UxLintError("UX baseline count는 0 이상이어야 합니다")
        if not isinstance(entry["reason"], str) or not entry["reason"] or not isinstance(entry["task"], str) or not entry["task"]:
            raise UxLintError("UX baseline reason/task 형식이 잘못되었습니다")
        result.append({"rule": entry["rule"], "path": entry["path"].replace("\\", "/"), "count": count, "reason": entry["reason"], "until": until, "task": entry["task"]})
    return result


def apply_baseline(findings: Sequence[Mapping[str, object]], entries: Sequence[Mapping[str, object]], root_prefix: str = "") -> list[dict[str, object]]:
    from datetime import date

    today = date.today()
    limits = {
        (str(entry["path"]), str(entry["rule"])): int(entry["count"])
        for entry in entries
        if date.fromisoformat(str(entry["until"])) >= today
    }
    seen: defaultdict[tuple[str, str], int] = defaultdict(int)
    result: list[dict[str, object]] = []
    for finding in findings:
        finding_path = str(finding["file"])
        relative_to_root = finding_path
        if root_prefix and finding_path.startswith(root_prefix.rstrip("/") + "/"):
            relative_to_root = finding_path[len(root_prefix.rstrip("/")) + 1 :]
        candidates = [(finding_path, str(finding["pattern"])), (relative_to_root, str(finding["pattern"]))]
        key = next((candidate for candidate in candidates if candidate in limits), candidates[0])
        index = seen[key]
        seen[key] += 1
        item = dict(finding)
        item["baseline"] = limits.get(key, 0)
        item["exempt"] = index < limits.get(key, 0)
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
            lines.append(f"| `{finding['file']}` | {finding['line']} | `{finding['pattern']}` | {state} |")
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
    parser = argparse.ArgumentParser(description="공통 UX 금지 패턴을 검사합니다.")
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
    args = build_parser().parse_args(argv)
    root = Path.cwd().resolve()
    try:
        inputs = ([args.root] if args.root else []) + list(args.paths)
        if not inputs:
            raise UxLintError("검사할 파일 또는 --root가 필요합니다")
        files = collect_files(inputs, root)
        token_files = set()
        if args.token_files:
            for item in args.token_files.split(","):
                candidate = item.strip()
                if candidate:
                    candidate_path = Path(candidate)
                    if not candidate_path.is_absolute() and args.root and (args.root / candidate_path).is_file():
                        candidate_path = args.root / candidate_path
                    token_files.add(_relative(candidate_path, root))
        findings = [finding for path, relative in files for finding in scan_file(path, relative, token_files)]
        baseline = load_baseline(args.baseline) if args.baseline else []
        root_prefix = _relative(args.root, root) if args.root else ""
        if root_prefix == ".":
            root_prefix = ""
        findings = apply_baseline(findings, baseline, root_prefix)
        added = added_lines(root, args.base, [relative for _, relative in files]) if args.base else {}
        should_fail = bool(args.base or args.fail_new)
        for finding in findings:
            is_added = not args.base or int(finding["line"]) in added.get(str(finding["file"]), set())
            finding["added"] = is_added
            finding["fail"] = bool(should_fail and is_added and not finding.get("exempt", False))
        fail_count = sum(1 for finding in findings if finding.get("fail"))
        from datetime import date

        expired = [entry for entry in baseline if date.fromisoformat(str(entry["until"])) < date.today()]
        status = "EXEMPT_EXPIRED" if expired else ("PASS" if fail_count == 0 else "FAIL")
        payload = {"tool": "ux_lint", "status": status, "findings": findings, "fail_count": fail_count, "base": args.base, "expired": expired}
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
