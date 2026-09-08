# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"""소비자 smoke 입력(핀·자산·승인)을 네트워크 없이 검증한다.

실제 소비자 checkout과 Next 빌드는 GitHub Actions workflow가 담당한다.
이 도구는 workflow가 실행되기 전에 입력을 닫힌 형식으로 확인하고, 로컬
tarball의 digest와 npm package metadata를 대조한다.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sys
import tarfile
from urllib.parse import urlsplit


SCHEMA = "kor-travel-common.consumer-pins.v1"
TOP_LEVEL_FIELDS = {"schema", "updated", "sources"}
SOURCE_FIELDS = {"role", "url", "revision", "path", "package", "approval"}
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
DATE_RE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")
NPM_PACKAGE_RE = re.compile(r"^@[a-z0-9][a-z0-9._-]*/[a-z0-9][a-z0-9._-]*$")
ROLE_RE = re.compile(r"^[a-z][a-z0-9-]{1,63}$")
REPOSITORY_RE = re.compile(r"^https://github\.com/digitie/[A-Za-z0-9][A-Za-z0-9.-]*$")
ASSET_RE = re.compile(
    r"^https://github\.com/digitie/[A-Za-z0-9][A-Za-z0-9.-]*/releases/download/"
    r"[A-Za-z0-9._-]+/[A-Za-z0-9._-]+\.tgz$"
)


class SmokeInputError(ValueError):
    """workflow 입력이 계약을 만족하지 않을 때 사용하는 오류."""


def _string(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise SmokeInputError(f"{label}: 비어 있지 않은 문자열이어야 함")
    return value


def _relative_path(value: object, label: str) -> str:
    text = _string(value, label)
    path = PurePosixPath(text)
    if (
        "\\" in text
        or text.startswith("/")
        or ":" in text
        or any(part in {"", ".", ".."} for part in path.parts)
    ):
        raise SmokeInputError(f"{label}: 저장소 루트 기준 POSIX 상대 경로여야 함")
    return text


def _repository(value: object, label: str) -> str:
    text = _string(value, label).rstrip("/")
    if REPOSITORY_RE.fullmatch(text) is None:
        raise SmokeInputError(f"{label}: digitie 공개 GitHub 저장소 URL이어야 함")
    return text


def validate_pins(data: object) -> list[dict[str, object]]:
    """핀 레지스트리의 schema, 고정 revision, GPL 승인 필드를 검사한다."""
    if not isinstance(data, dict):
        raise SmokeInputError("pins: 최상위 객체가 아님")
    if set(data) != TOP_LEVEL_FIELDS:
        raise SmokeInputError("pins: schema, updated, sources 외 필드가 있음")
    if data.get("schema") != SCHEMA:
        raise SmokeInputError(f"pins.schema: {SCHEMA}이어야 함")
    if not isinstance(data.get("updated"), str) or DATE_RE.fullmatch(data["updated"]) is None:
        raise SmokeInputError("pins.updated: YYYY-MM-DD 날짜여야 함")
    sources = data.get("sources")
    if not isinstance(sources, list) or not sources:
        raise SmokeInputError("pins.sources: 비어 있지 않은 배열이어야 함")

    result: list[dict[str, object]] = []
    roles: set[str] = set()
    for index, entry in enumerate(sources):
        label = f"pins.sources[{index}]"
        if not isinstance(entry, dict) or set(entry) != SOURCE_FIELDS:
            raise SmokeInputError(f"{label}: role, url, revision, path, package, approval만 허용")
        role = _string(entry.get("role"), f"{label}.role")
        if ROLE_RE.fullmatch(role) is None or role in roles:
            raise SmokeInputError(f"{label}.role: 고유한 소문자 역할명이 아님")
        roles.add(role)
        url = _repository(entry.get("url"), f"{label}.url")
        revision = _string(entry.get("revision"), f"{label}.revision")
        if SHA_RE.fullmatch(revision) is None:
            raise SmokeInputError(f"{label}.revision: 40자 소문자 SHA가 아님")
        path = _relative_path(entry.get("path"), f"{label}.path")
        package = _string(entry.get("package"), f"{label}.package")
        if NPM_PACKAGE_RE.fullmatch(package) is None:
            raise SmokeInputError(f"{label}.package: npm scope package 이름이 아님")
        approval = entry.get("approval")
        if not isinstance(approval, dict) or set(approval) != {"status", "task", "license"}:
            raise SmokeInputError(f"{label}.approval: status, task, license 객체여야 함")
        if approval.get("status") != "approved":
            raise SmokeInputError(f"{label}.approval: approved 상태가 아님")
        _string(approval.get("task"), f"{label}.approval.task")
        if approval.get("license") != "GPL-3.0-or-later":
            raise SmokeInputError(f"{label}.approval.license: GPL-3.0-or-later이어야 함")
        result.append({"role": role, "url": url, "revision": revision, "path": path,
                       "package": package, "approval": approval})
    return result


def load_pins(path: Path) -> list[dict[str, object]]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise SmokeInputError("pins: JSON을 읽을 수 없음") from exc
    return validate_pins(data)


def select_pin(sources: list[dict[str, object]], role: str) -> dict[str, object]:
    """역할 하나를 선택하고 승인 상태를 다시 확인한다."""
    if ROLE_RE.fullmatch(role) is None:
        raise SmokeInputError("role: 유효한 역할명이 아님")
    matches = [entry for entry in sources if entry["role"] == role]
    if len(matches) != 1:
        raise SmokeInputError(f"role: 핀을 하나로 선택할 수 없음({role})")
    selected = matches[0]
    approval = selected["approval"]
    if not isinstance(approval, dict) or approval.get("status") != "approved":
        raise SmokeInputError(f"role: 승인되지 않은 핀({role})")
    return selected


def validate_asset_url(value: object) -> str:
    """자산 URL을 공개 GitHub Release 경로로 제한한다."""
    text = _string(value, "asset-url")
    if ASSET_RE.fullmatch(text) is None:
        raise SmokeInputError("asset-url: digitie GitHub Release의 고정 .tgz URL이어야 함")
    parsed = urlsplit(text)
    if parsed.query or parsed.fragment or parsed.username or parsed.password:
        raise SmokeInputError("asset-url: query·fragment·인증정보를 허용하지 않음")
    return text


def validate_asset(path: Path, expected_sha256: str, expected_package: str) -> str:
    """tarball 존재·SHA256·안전한 package/package.json 이름을 검사한다."""
    if not path.is_file():
        raise SmokeInputError("asset: 파일이 없음")
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if not re.fullmatch(r"[0-9a-f]{64}", expected_sha256):
        raise SmokeInputError("asset-sha256: 64자 소문자 SHA256이어야 함")
    if digest != expected_sha256:
        raise SmokeInputError("asset: SHA256 digest 불일치")
    try:
        with tarfile.open(path, "r:gz") as archive:
            members = archive.getmembers()
            names = {member.name for member in members}
            package_member = next((member for member in members if member.name in {
                "package/package.json", "package.json"
            }), None)
            if package_member is None or not package_member.isfile():
                raise SmokeInputError("asset: package/package.json이 없음")
            if any(
                name.startswith("/") or "\\" in name
                or any(part in {"", ".", ".."} for part in name.split("/"))
                for name in names
            ):
                raise SmokeInputError("asset: tar 경로 traversal이 있음")
            raw = archive.extractfile(package_member)
            if raw is None:
                raise SmokeInputError("asset: package metadata를 읽을 수 없음")
            metadata = json.loads(raw.read().decode("utf-8"))
    except (OSError, tarfile.TarError, UnicodeError, json.JSONDecodeError) as exc:
        raise SmokeInputError("asset: 유효한 gzip tarball이 아님") from exc
    if not isinstance(metadata, dict) or metadata.get("name") != expected_package:
        raise SmokeInputError("asset: package name이 핀과 일치하지 않음")
    return digest


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pins", type=Path, required=True)
    parser.add_argument("--role", required=True)
    parser.add_argument("--asset", type=Path, required=True)
    parser.add_argument("--asset-sha256", required=True)
    parser.add_argument("--asset-url")
    args = parser.parse_args(argv)
    try:
        sources = load_pins(args.pins)
        selected = select_pin(sources, args.role)
        if args.asset_url is not None:
            validate_asset_url(args.asset_url)
        digest = validate_asset(args.asset, args.asset_sha256, str(selected["package"]))
    except SmokeInputError as exc:
        print(f"consumer_smoke: 입력 오류: {exc}")
        return 2
    print(json.dumps({
        "schema": SCHEMA,
        "role": selected["role"],
        "url": selected["url"],
        "repository": urlsplit(str(selected["url"])).path.lstrip("/"),
        "revision": selected["revision"],
        "path": selected["path"],
        "package": selected["package"],
        "asset_sha256": digest,
        "approval": "approved",
    }, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
