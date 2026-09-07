# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"""소비자 매니페스트 v1의 공통 검증 규칙."""

from __future__ import annotations

from datetime import date
import json
from pathlib import Path
import re
from typing import Any


MANIFEST_SCHEMA = "kor-travel-common.consumer-manifest.v1"
LOCKFILE_KINDS = frozenset({"npm", "uv", "poetry", "requirements"})
TOP_LEVEL_FIELDS = frozenset({
    "schema", "repo", "app", "tokens", "ui", "python", "lockfiles",
    "contrast", "ux_gate", "openapi", "exceptions",
})
VERSION_FIELDS = frozenset({"version"})
TOKENS_FIELDS = frozenset({"version", "override"})
LOCKFILE_FIELDS = frozenset({"kind", "path", "scope"})
CONTRAST_FIELDS = frozenset({"baseline", "dark"})
UX_GATE_FIELDS = frozenset({"baseline"})
OPENAPI_FIELDS = frozenset({"exceptions"})
EXCEPTION_COMMON_FIELDS = frozenset({"reason", "until", "review"})
EXCEPTION_RULE_FIELDS = EXCEPTION_COMMON_FIELDS | {"rule", "surface"}
EXCEPTION_KEY_FIELDS = EXCEPTION_COMMON_FIELDS | {"key"}
DATE_RE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")


def _field_error(path: str, message: str) -> str:
    return f"{path}: {message}"


def _is_string(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _check_object(value: object, path: str, fields: frozenset[str], errors: list[str]) -> bool:
    if not isinstance(value, dict):
        errors.append(_field_error(path, "객체여야 함"))
        return False
    unknown = sorted(set(value) - fields)
    if unknown:
        errors.append(_field_error(path, f"미지 필드 {len(unknown)}개"))
    return True


def _check_string(value: object, path: str, errors: list[str]) -> None:
    if not _is_string(value):
        errors.append(_field_error(path, "비어 있지 않은 문자열이어야 함"))


def _check_nullable_string(value: object, path: str, errors: list[str]) -> None:
    if value is not None:
        _check_string(value, path, errors)


def _check_relative_path(value: object, path: str, errors: list[str]) -> None:
    """저장소 루트에서 해석할 수 있는 POSIX 상대 경로만 허용한다."""
    if not _is_string(value):
        errors.append(_field_error(path, "비어 있지 않은 상대 경로여야 함"))
        return
    if any(ord(char) < 0x20 or ord(char) == 0x7F for char in value):
        errors.append(_field_error(path, "저장소 루트 기준 정규 POSIX 상대 경로여야 함"))
        return
    if value != value.strip():
        errors.append(_field_error(path, "저장소 루트 기준 정규 POSIX 상대 경로여야 함"))
        return
    text = value.strip()
    parts = text.split("/")
    if (
        "\\" in text
        or text.startswith("/")
        or ":" in text
        or any(part in {"", ".", ".."} for part in parts)
    ):
        errors.append(_field_error(path, "저장소 루트 기준 정규 POSIX 상대 경로여야 함"))


def _check_date(value: object, path: str, errors: list[str]) -> None:
    if not isinstance(value, str) or DATE_RE.fullmatch(value) is None:
        errors.append(_field_error(path, "YYYY-MM-DD 날짜여야 함"))
        return
    try:
        date.fromisoformat(value)
    except ValueError:
        errors.append(_field_error(path, "유효한 날짜여야 함"))


def _check_version_object(value: object, path: str, errors: list[str], *, tokens: bool = False) -> None:
    fields = TOKENS_FIELDS if tokens else VERSION_FIELDS
    if not _check_object(value, path, fields, errors):
        return
    if "version" not in value:
        errors.append(_field_error(f"{path}.version", "필수 필드"))
    else:
        _check_nullable_string(value["version"], f"{path}.version", errors)
    if tokens and "override" not in value:
        errors.append(_field_error(f"{path}.override", "필수 필드"))
    elif tokens and value.get("override") is not None:
        _check_relative_path(value["override"], f"{path}.override", errors)


def _check_exceptions(value: object, path: str, errors: list[str]) -> None:
    if not isinstance(value, list):
        errors.append(_field_error(path, "배열이어야 함"))
        return
    for index, entry in enumerate(value):
        entry_path = f"{path}[{index}]"
        if not isinstance(entry, dict):
            errors.append(_field_error(entry_path, "객체여야 함"))
            continue
        keys = set(entry)
        if "rule" in keys:
            expected = EXCEPTION_RULE_FIELDS
            required = ("rule", "surface")
        elif "key" in keys:
            expected = EXCEPTION_KEY_FIELDS
            required = ("key",)
        else:
            errors.append(_field_error(entry_path, "rule 또는 key 필드가 필요"))
            continue
        unknown = sorted(keys - expected)
        missing = sorted(expected - keys)
        if unknown:
            errors.append(_field_error(entry_path, f"미지 필드 {len(unknown)}개"))
        if missing:
            errors.append(_field_error(entry_path, f"누락 필드: {', '.join(missing)}"))
        for field in required:
            if field in entry:
                _check_string(entry[field], f"{entry_path}.{field}", errors)
        if "reason" in entry:
            _check_string(entry["reason"], f"{entry_path}.reason", errors)
        if "until" in entry:
            _check_date(entry["until"], f"{entry_path}.until", errors)
        if "review" in entry:
            _check_date(entry["review"], f"{entry_path}.review", errors)


def validate_manifest(data: object, consumer_repos: set[str] | None = None) -> list[str]:
    """매니페스트 객체를 검사하고 사람이 읽을 수 있는 오류 목록을 반환한다."""
    errors: list[str] = []
    if not isinstance(data, dict):
        return [_field_error("$", "최상위가 객체여야 함")]

    unknown = sorted(set(data) - TOP_LEVEL_FIELDS)
    missing = sorted(TOP_LEVEL_FIELDS - set(data))
    if unknown:
        errors.append(_field_error("$", f"미지 필드 {len(unknown)}개"))
    if missing:
        errors.append(_field_error("$", f"누락 필드: {', '.join(missing)}"))

    if data.get("schema") != MANIFEST_SCHEMA:
        errors.append(_field_error("$.schema", f"{MANIFEST_SCHEMA}이어야 함"))
    _check_string(data.get("repo"), "$.repo", errors)
    if consumer_repos is not None and isinstance(data.get("repo"), str):
        if data["repo"] not in consumer_repos:
            errors.append(_field_error("$.repo", "versions.json consumers의 정식 key가 아님"))
    _check_relative_path(data.get("app"), "$.app", errors)

    _check_version_object(data.get("tokens"), "$.tokens", errors, tokens=True)
    _check_version_object(data.get("ui"), "$.ui", errors)
    _check_version_object(data.get("python"), "$.python", errors)

    lockfiles = data.get("lockfiles")
    if not isinstance(lockfiles, list):
        errors.append(_field_error("$.lockfiles", "배열이어야 함"))
    else:
        for index, entry in enumerate(lockfiles):
            entry_path = f"$.lockfiles[{index}]"
            if not _check_object(entry, entry_path, LOCKFILE_FIELDS, errors):
                continue
            for field in LOCKFILE_FIELDS:
                if field not in entry:
                    errors.append(_field_error(f"{entry_path}.{field}", "필수 필드"))
            if "kind" in entry:
                if not isinstance(entry["kind"], str) or entry["kind"] not in LOCKFILE_KINDS:
                    errors.append(_field_error(f"{entry_path}.kind", "지원하지 않는 lockfile 종류"))
            if "path" in entry:
                _check_relative_path(entry["path"], f"{entry_path}.path", errors)
            if "scope" in entry:
                _check_relative_path(entry["scope"], f"{entry_path}.scope", errors)

    contrast = data.get("contrast")
    if _check_object(contrast, "$.contrast", CONTRAST_FIELDS, errors):
        for field in CONTRAST_FIELDS:
            if field not in contrast:
                errors.append(_field_error(f"$.contrast.{field}", "필수 필드"))
        if "baseline" in contrast:
            _check_nullable_string(contrast["baseline"], "$.contrast.baseline", errors)
            if contrast["baseline"] is not None:
                _check_relative_path(contrast["baseline"], "$.contrast.baseline", errors)
        if "dark" in contrast and type(contrast["dark"]) is not bool:
            errors.append(_field_error("$.contrast.dark", "boolean이어야 함"))

    ux_gate = data.get("ux_gate")
    if _check_object(ux_gate, "$.ux_gate", UX_GATE_FIELDS, errors):
        if "baseline" not in ux_gate:
            errors.append(_field_error("$.ux_gate.baseline", "필수 필드"))
        elif ux_gate["baseline"] is not None:
            _check_relative_path(ux_gate["baseline"], "$.ux_gate.baseline", errors)

    openapi = data.get("openapi")
    if _check_object(openapi, "$.openapi", OPENAPI_FIELDS, errors):
        if "exceptions" not in openapi:
            errors.append(_field_error("$.openapi.exceptions", "필수 필드"))
        elif not isinstance(openapi["exceptions"], list):
            errors.append(_field_error("$.openapi.exceptions", "배열이어야 함"))
        else:
            for index, reference in enumerate(openapi["exceptions"]):
                _check_string(reference, f"$.openapi.exceptions[{index}]", errors)

    _check_exceptions(data.get("exceptions"), "$.exceptions", errors)
    return errors


def _consumer_keys(registry_path: Path) -> tuple[set[str] | None, str | None]:
    try:
        registry = json.loads(registry_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return None, "versions.json을 읽을 수 없음"
    consumers = registry.get("consumers") if isinstance(registry, dict) else None
    if not isinstance(consumers, dict):
        return None, "versions.json consumers가 객체가 아님"
    return {key for key in consumers if isinstance(key, str)}, None


def validate_manifest_file(path: Path, registry_path: Path | None = None) -> list[str]:
    """JSON 파일과 versions.json의 소비자 key를 함께 검사한다."""
    try:
        data: Any = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return ["$: 매니페스트 JSON을 읽을 수 없음"]
    consumer_repos = None
    if registry_path is not None:
        consumer_repos, registry_error = _consumer_keys(registry_path)
        if registry_error:
            return [f"$: {registry_error}"]
    return validate_manifest(data, consumer_repos)
