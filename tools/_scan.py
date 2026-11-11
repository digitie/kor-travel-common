# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"""두 정보 유출 검사기가 공유하는 Git 범위 선택과 값 비공개 판정."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import gzip
import io
import json
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import tarfile
import zlib
import tomllib


MAX_INPUT_BYTES = 64 * 1024 * 1024
MAX_ARCHIVE_BYTES = 64 * 1024 * 1024
MAX_MEMBER_BYTES = 32 * 1024 * 1024
MAX_EXPANDED_BYTES = 256 * 1024 * 1024
MAX_ARCHIVE_MEMBERS = 4096
MAX_ARCHIVE_DEPTH = 4


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
    if isinstance(name, str):
        try:
            name.encode("utf-8")
        except UnicodeError:
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
                    # reusable workflow가 caller root 안에 common을 nested checkout할 수 있다.
                    # 그 checkout은 caller의 입력 파일이 아니므로 경로를 읽기 전에 제외한다.
                    name = path_name(raw_name.rstrip(b"/"))
                    current = self.root
                    nested = False
                    for part in PurePosixPath(name).parts:
                        current /= part
                        if current != self.root and (current / ".git").exists():
                            nested = True
                            break
                    if not nested:
                        self.entries[name] = ("100644", "")
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
            if path.stat().st_size > MAX_INPUT_BYTES:
                raise ScanError("입력 크기 제한 초과")
            with path.open("rb") as stream:
                data = stream.read(MAX_INPUT_BYTES + 1)
            if len(data) > MAX_INPUT_BYTES:
                raise ScanError("입력 크기 제한 초과")
            return data
        if not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", oid):
            raise ScanError("blob 식별자 오류")
        if int(git(self.root, "cat-file", "-s", oid)) > MAX_INPUT_BYTES:
            raise ScanError("입력 크기 제한 초과")
        return git(self.root, "cat-file", "blob", oid)


def decode(data: bytes) -> str:
    try:
        value = data.decode("utf-8-sig")
    except UnicodeDecodeError:
        raise ScanError("UTF-8로 검사할 수 없는 입력") from None
    if "\0" in value:
        raise ScanError("NUL이 있는 입력은 검사할 수 없음")
    return value



@dataclass
class ArchiveBudget:
    """선택 스냅샷 전체의 압축 해제량과 항목 수를 제한한다."""

    expanded: int = 0
    members: int = 0


@dataclass
class ScanPart:
    name: str
    value: str
    byte_offset: int | None = None


def ascii_parts(name: str, data: bytes):
    """모든 ASCII 문자열을 검사하며 바이너리 경계를 넘어 합치지 않는다."""
    for match in re.finditer(rb"[\x09\x0a\x0d\x20-\x7e]+", data):
        yield ScanPart(name, match.group().decode("ascii"), match.start())


def known_binary(name: str, data: bytes) -> bool:
    """확장자와 서명이 일치하는 native·이미지·V8 payload만 인식한다."""
    suffix = PurePosixPath(name).suffix.lower()
    if suffix == ".wasm":
        return data.startswith(b"\0asm\x01\0\0\0")
    if suffix == ".bin":
        return len(data) >= 3 and data.startswith(b"\xff\x0f")
    if suffix == ".node":
        elf = len(data) >= 16 and data[:4] == b"\x7fELF" and data[4] in (1, 2) and data[5] in (1, 2) and data[6] == 1
        macho = len(data) >= 28 and data[:4] in (
            b"\xfe\xed\xfa\xce", b"\xce\xfa\xed\xfe", b"\xfe\xed\xfa\xcf", b"\xcf\xfa\xed\xfe", b"\xca\xfe\xba\xbe",
        )
        pe = False
        if len(data) >= 64 and data[:2] == b"MZ":
            offset = int.from_bytes(data[60:64], "little")
            pe = offset >= 64 and data[offset:offset + 4] == b"PE\0\0"
        return elf or macho or pe
    return (
        suffix in (".jpg", ".jpeg") and data.startswith(b"\xff\xd8\xff")
        or suffix == ".png" and data.startswith(b"\x89PNG\r\n\x1a\n")
        or suffix == ".gif" and data.startswith((b"GIF87a", b"GIF89a"))
    )


def gzip_header_parts(name: str, data: bytes):
    """gzip의 선택 이름·주석·extra도 값 비공개 검사에 포함한다."""
    if len(data) < 10 or data[2] != 8 or data[3] & 0xe0:
        raise ScanError("gzip 헤더 형식 오류")
    flags, position = data[3], 10
    if flags & 4:
        if position + 2 > len(data):
            raise ScanError("gzip 헤더 형식 오류")
        size = int.from_bytes(data[position:position + 2], "little")
        position += 2
        if position + size > len(data):
            raise ScanError("gzip 헤더 형식 오류")
        yield from ascii_parts(name + "!/@gzip-extra", data[position:position + size])
        position += size
    for flag, label in ((8, "name"), (16, "comment")):
        if flags & flag:
            end = data.find(b"\0", position, min(len(data), position + 65536))
            if end < 0:
                raise ScanError("gzip 메타데이터 크기·형식 오류")
            yield ScanPart(name + "!/@gzip-" + label, decode(data[position:end]))
            position = end + 1


def scan_parts(name: str, data: bytes, patterns, budget: ArchiveBudget, depth: int = 0):
    """디스크 추출 없이 tar 계열과 중첩 source archive를 제한적으로 순회한다."""
    if any(expression.search(name) for expression in patterns.values()):
        raise ScanError("탐지 패턴에 일치하는 경로명 — 원문 비공개")
    compressed = data.startswith(b"\x1f\x8b")
    archive_input = compressed or name.lower().endswith((".tgz", ".tar.gz", ".tar")) or data[257:262] == b"ustar"
    if not archive_input:
        if known_binary(name, data):
            yield from ascii_parts(name, data)
        else:
            yield ScanPart(name, decode(data))
        return
    if depth >= MAX_ARCHIVE_DEPTH or len(data) > MAX_INPUT_BYTES:
        raise ScanError("archive 깊이·입력 크기 제한 초과")
    try:
        if compressed:
            yield from gzip_header_parts(name, data)
            limit = min(MAX_ARCHIVE_BYTES, MAX_EXPANDED_BYTES - budget.expanded)
            with gzip.GzipFile(fileobj=io.BytesIO(data)) as stream:
                raw = stream.read(limit + 1)
        else:
            raw = data
        if len(raw) > MAX_ARCHIVE_BYTES or budget.expanded + len(raw) > MAX_EXPANDED_BYTES:
            raise ScanError("archive 압축 해제 크기 제한 초과")
        budget.expanded += len(raw)
        seen, end = set(), 0
        with tarfile.open(fileobj=io.BytesIO(raw), mode="r:") as archive:
            for member in archive:
                budget.members += 1
                if budget.members > MAX_ARCHIVE_MEMBERS:
                    raise ScanError("archive 항목 수 제한 초과")
                member_name = member.name.removesuffix("/") if member.isdir() else member.name
                member_name = path_name(member_name)
                label = name + "!/" + member_name
                if member_name in seen:
                    raise ScanError("archive 중복 경로")
                seen.add(member_name)
                if any(expression.search(label) for expression in patterns.values()):
                    raise ScanError("탐지 패턴에 일치하는 경로명 — 원문 비공개")
                if (not member.isfile() and not member.isdir()) or member.sparse is not None:
                    raise ScanError("archive 링크·특수·sparse 항목은 검사할 수 없음")
                if member.size < 0 or member.size > MAX_MEMBER_BYTES or member.isdir() and member.size:
                    raise ScanError("archive 항목 크기 제한 초과")
                if member.offset_data + member.size > len(raw):
                    raise ScanError("archive 항목이 잘림")
                yield from ascii_parts(label + "!/@tar-header", raw[member.offset:member.offset_data])
                for value in (member.uname, member.gname, *(key + "=" + value for key, value in member.pax_headers.items())):
                    yield ScanPart(label + "!/@metadata", decode(value.encode("utf-8")))
                end = max(end, member.offset_data + (member.size + 511) // 512 * 512)
                if member.isfile():
                    stream = archive.extractfile(member)
                    if stream is None:
                        raise ScanError("archive 항목 읽기 실패")
                    with stream:
                        content = stream.read(MAX_MEMBER_BYTES + 1)
                    if len(content) != member.size:
                        raise ScanError("archive 항목 길이 불일치")
                    yield from scan_parts(label, content, patterns, budget, depth + 1)
            for key, value in archive.pax_headers.items():
                yield ScanPart(name + "!/@metadata", decode((key + "=" + value).encode("utf-8")))
        if raw[end:].strip(b"\0"):
            raise ScanError("archive 종료 뒤 비어 있지 않은 입력")
    except (tarfile.TarError, gzip.BadGzipFile, EOFError, OverflowError, RecursionError, UnicodeError, zlib.error):
        raise ScanError("archive 읽기·형식 오류") from None


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
        findings, exceptions = set(), set()
        budget = ArchiveBudget()
        for name in sorted(selected):
            for part in scan_parts(name, snapshot.read(name), patterns, budget):
                for identifier, expression in patterns.items():
                    for match in expression.finditer(part.value):
                        line = part.value.count("\n", 0, match.start()) + 1
                        offset = None if part.byte_offset is None else part.byte_offset + match.start()
                        if part.name == name and part.byte_offset is None and identifier in allowed.get(name, set()):
                            exceptions.add((name, line, identifier))
                        else:
                            findings.add((part.name, line, identifier, offset))
        for name, line, identifier, offset in sorted(findings, key=lambda item: (item[:3], -1 if item[3] is None else item[3])):
            finding = {"path": name, "line": line, "rule": identifier}
            if offset is not None:
                finding["byte"] = offset
            print(json.dumps(finding, ensure_ascii=False))
        print(f"검사 {len(selected)}개 파일, 발견 {len(findings)}건, 명시적 예외 {len(exceptions)}건")
        return 1 if findings else 0
    except (ScanError, OSError, ValueError, TypeError, KeyError, IndexError, UnicodeError) as error:
        message = str(error) if isinstance(error, ScanError) else "입력 읽기·형식 오류"
        print("검사 오류: " + message)
        return 2
