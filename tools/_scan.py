# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"""두 정보 유출 검사기가 공유하는 Git 범위 선택과 값 비공개 판정."""

from __future__ import annotations

import argparse
import json
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import tomllib


class ScanError(Exception):
    """원문이나 외부 명령 출력을 포함하지 않는 진단."""


def git(root: Path, *args: str) -> bytes:
    result = subprocess.run(["git", "-C", str(root), *args], capture_output=True)
    if result.returncode:
        raise ScanError("Git 입력을 읽지 못함")
    return result.stdout


def path_name(raw: bytes | str) -> str:
    try:
        name = raw.decode("utf-8") if isinstance(raw, bytes) else raw
    except UnicodeDecodeError:
        raise ScanError("UTF-8 파일명이 아님") from None
    if (not isinstance(name, str) or not name or "\\" in name or ":" in name
            or any(ord(char) < 32 or ord(char) == 127 for char in name)
            or name.startswith("/") or any(part in ("", ".", "..") for part in name.split("/"))):
        raise ScanError("안전한 저장소 상대 경로가 아님")
    return name


def commit(root: Path, ref: str) -> str:
    value = git(root, "rev-parse", "--verify", "--end-of-options", ref + "^{commit}").decode().strip()
    if not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", value):
        raise ScanError("commit 해석 실패")
    return value


class Snapshot:
    """작업 트리·index·commit 중 선택한 동일 스냅샷에서 정책과 파일을 읽는다."""

    def __init__(self, root: Path, staged: bool, base: str | None):
        try:
            actual = Path(git(root, "rev-parse", "--show-toplevel").decode("utf-8").strip()).resolve()
        except (UnicodeDecodeError, OSError):
            raise ScanError("저장소 루트 해석 실패") from None
        if root.resolve() != actual:
            raise ScanError("--root는 Git 저장소 루트여야 함")
        self.root = actual
        self.working = not staged and base is None
        self.entries: dict[str, tuple[str, str]] = {}
        self.selected: set[str] = set()
        if base is not None:
            head = commit(root, "HEAD")
            baseline = commit(root, base)
            records = git(root, "ls-tree", "-r", "-z", "--full-tree", head)
            changed = git(root, "diff", "--no-ext-diff", "--no-renames", "--name-only", "-z",
                          "--diff-filter=ACMT", baseline, head, "--")
        else:
            records = git(root, "ls-files", "--stage", "-z")
            changed = git(root, "diff", "--no-ext-diff", "--cached", "--no-renames", "--name-only",
                          "-z", "--diff-filter=ACMT", "--") if staged else b""
        for record in records.split(b"\0"):
            if not record:
                continue
            metadata, raw_name = record.split(b"\t", 1)
            fields = metadata.decode("ascii").split()
            mode, oid = (fields[0], fields[2]) if base is not None else (fields[0], fields[1])
            if base is None and fields[2] != "0":
                raise ScanError("충돌 중인 index는 검사할 수 없음")
            self.entries[path_name(raw_name)] = (mode, oid)
        if self.working:
            for raw_name in git(root, "ls-files", "--others", "--exclude-standard", "-z").split(b"\0"):
                if raw_name:
                    self.entries[path_name(raw_name)] = ("100644", "")
            self.selected = set(self.entries)
        else:
            self.selected = {path_name(name) for name in changed.split(b"\0") if name}
        if not self.selected:
            raise ScanError("검사 대상 파일 없음(NOT_RUN)")

    def read(self, name: str) -> bytes:
        name = path_name(name)
        if name not in self.entries:
            raise ScanError("스냅샷에 필수 입력 파일이 없음")
        mode, oid = self.entries[name]
        if mode not in ("100644", "100755"):
            raise ScanError("심볼릭 링크·submodule은 검사할 수 없음")
        if self.working:
            path = self.root
            for part in PurePosixPath(name).parts:
                path = path / part
                if path.is_symlink():
                    raise ScanError("심볼릭 링크는 검사할 수 없음")
            if path.resolve() != path.absolute():
                raise ScanError("경로 재지정·junction은 검사할 수 없음")
            if not stat.S_ISREG(path.stat().st_mode):
                raise ScanError("일반 파일이 아닌 입력")
            return path.read_bytes()
        if not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", oid):
            raise ScanError("blob 식별자 오류")
        return git(self.root, "cat-file", "blob", oid)


def decode(data: bytes) -> str:
    try:
        value = data.decode("utf-8-sig")
    except UnicodeDecodeError:
        raise ScanError("UTF-8로 검사할 수 없는 입력") from None
    if "\0" in value:
        raise ScanError("NUL이 있는 입력은 검사할 수 없음")
    return value


def policy(snapshot: Snapshot, name: str):
    try:
        data = tomllib.loads(decode(snapshot.read(name)))
    except tomllib.TOMLDecodeError:
        raise ScanError("패턴 파일 TOML 형식 오류") from None
    if set(data) - {"version", "patterns", "allowlist"} or type(data.get("version")) is not int or data["version"] != 1:
        raise ScanError("패턴 파일 스키마 오류")
    definitions = data.get("patterns")
    if not isinstance(definitions, list) or not definitions:
        raise ScanError("비어 있는 패턴 목록")
    patterns = {}
    for entry in definitions:
        if not isinstance(entry, dict) or set(entry) != {"id", "regex"}:
            raise ScanError("패턴 항목 형식 오류")
        identifier, expression = entry["id"], entry["regex"]
        if not isinstance(identifier, str) or not re.fullmatch(r"[A-Z][A-Z0-9-]{1,63}", identifier) or identifier in patterns:
            raise ScanError("패턴 ID 오류·중복")
        if not isinstance(expression, str) or not expression:
            raise ScanError("정규식 누락")
        try:
            compiled = re.compile(expression)
        except (re.error, RecursionError):
            raise ScanError("정규식 컴파일 실패") from None
        if compiled.search(""):
            raise ScanError("빈 문자열에 일치하는 정규식")
        patterns[identifier] = compiled
    allowed = {}
    entries = data.get("allowlist", [])
    if not isinstance(entries, list):
        raise ScanError("allowlist 형식 오류")
    for entry in entries:
        if not isinstance(entry, dict) or set(entry) != {"path", "rules", "reason"}:
            raise ScanError("allowlist 항목 형식 오류")
        path = path_name(entry["path"])
        rules, reason = entry["rules"], entry["reason"]
        if (path not in snapshot.entries or path in allowed or any(c in path for c in "*?[]")
                or not isinstance(reason, str) or not reason.strip()
                or not isinstance(rules, list) or not rules
                or any(not isinstance(rule, str) or rule not in patterns for rule in rules)
                or len(set(rules)) != len(rules)):
            raise ScanError("allowlist 경로·규칙·사유 오류")
        allowed[path] = set(rules)
    return patterns, allowed


def main(default_patterns: str, argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="원문을 출력하지 않는 저장소 정보 유출 검사")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--patterns", default=default_patterns, help="같은 스냅샷의 패턴 파일 상대 경로")
    parser.add_argument("--scope", default=".", help="저장소 루트 기준 검사 범위(기본: 전체)")
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--all", action="store_true", help="추적 파일과 ignore되지 않은 새 파일의 현재 내용")
    modes.add_argument("--staged", action="store_true", help="staged 변경 파일의 index blob")
    modes.add_argument("--base", help="지정 commit과 HEAD 사이 변경 파일의 HEAD blob")
    args = parser.parse_args(argv)
    try:
        snapshot = Snapshot(args.root, args.staged, args.base)
        patterns, allowed = policy(snapshot, args.patterns)
        if args.scope == ".":
            scope_prefix = ""
        else:
            scope_value = args.scope.rstrip("/")
            scope_prefix = path_name(scope_value) + "/"
        selected = {
            name for name in snapshot.selected
            if not scope_prefix or name.startswith(scope_prefix)
        }
        if not selected:
            raise ScanError("검사 scope에 파일 없음(NOT_RUN)")
        findings, exceptions = [], 0
        for name in sorted(selected):
            if any(expression.search(name) for expression in patterns.values()):
                raise ScanError("탐지 패턴에 일치하는 경로명 — 원문 비공개")
            value = decode(snapshot.read(name))
            for identifier, expression in patterns.items():
                lines = {value.count("\n", 0, match.start()) + 1 for match in expression.finditer(value)}
                if identifier in allowed.get(name, set()):
                    exceptions += len(lines)
                else:
                    findings.extend((name, line, identifier) for line in sorted(lines))
        for name, line, identifier in sorted(findings):
            print(json.dumps({"path": name, "line": line, "rule": identifier}, ensure_ascii=False))
        print(f"검사 {len(selected)}개 파일, 발견 {len(findings)}건, 명시적 예외 {exceptions}건")
        return 1 if findings else 0
    except (ScanError, OSError, ValueError, TypeError, KeyError, IndexError, UnicodeError) as error:
        message = str(error) if isinstance(error, ScanError) else "입력 읽기·형식 오류"
        print("검사 오류: " + message)
        return 2
