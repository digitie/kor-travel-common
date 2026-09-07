# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"""소비 저장소의 선언·설치 버전을 루트 `versions.json`과 대조해 판정한다(읽기 전용).

규칙 정본은 docs/standards/versions.md, 값 정본은 versions.json이다. 이 도구는
파일을 쓰지 않고(`--json`·`--markdown`으로 지정한 출력 파일 제외), 네트워크를 쓰지
않으며, 표준 라이브러리만 사용한다(`tomllib`은 Python 3.11+). Windows Python에서도
동작해야 한다.

읽는 파일: package.json / package-lock.json(lockfileVersion 3) / pyproject.toml /
uv.lock / poetry.lock / requirements*.txt / `.github/workflows/*.yml|*.yaml`. Poetry·requirements는
uv 전환 전까지의 과도기 입력이며, requirements 설치본은 정확 핀만 후보로 보고 항상
`NO_LOCK`을 남긴다. workflow는 제한된 정적 YAML만 읽고 원격 실행 버전은 추정하지 않는다.

판정 어휘(D-07): OK / BELOW_FLOOR / ABOVE_MAX / NOT_RECOMMENDED / NO_LOCK / NO_ENGINES /
FLOATING_REF / BLOCKED / EXEMPT / EXEMPT_EXPIRED.

모드(D-30): report(기본, exit 0; FLOATING_REF·BLOCKED·EXEMPT_EXPIRED는 `::error::`) →
warn(exit 0, `::warning::`) → fail(exit 1). 모드는 versions.json `consumers.<repo>.enforce`가
소유하며 `--mode`는 로컬 실행용 override다.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass, field
from datetime import date
import ipaddress
import json
import os
from pathlib import Path
import re
import shlex
import sys
import tomllib
from urllib.parse import unquote, urlsplit, urlunsplit

try:
    from manifest_schema import MANIFEST_SCHEMA, validate_manifest_file
except ImportError:  # repository-root imports in the unit tests
    from tools.manifest_schema import MANIFEST_SCHEMA, validate_manifest_file


REGISTRY_SCHEMA = "kor-travel-common.version-registry.v1"
REPORT_SCHEMA = "kor-travel-common.version-report.v1"

VERDICTS = ("OK", "BELOW_FLOOR", "ABOVE_MAX", "NOT_RECOMMENDED", "NO_LOCK", "NO_ENGINES",
            "FLOATING_REF", "BLOCKED", "EXEMPT", "EXEMPT_EXPIRED")
HARD = frozenset({"FLOATING_REF", "BLOCKED", "EXEMPT_EXPIRED"})
FAILING = HARD | frozenset({"BELOW_FLOOR", "ABOVE_MAX", "NO_LOCK", "NO_ENGINES"})
SOFT = frozenset({"NOT_RECOMMENDED"})
MODES = ("report", "warn", "fail")

SKIP_DIRS = frozenset({"node_modules", ".venv", "venv", ".git", ".next", "dist", "build", "out",
                       "coverage", ".tools", "vendor", "__pycache__", ".turbo", "target"})
MAX_DEPTH = 4
SHA_RE = re.compile(r"\b[0-9a-f]{40}\b")
TAG_RE = re.compile(r"^(?:[A-Za-z0-9._-]+-)?v?\d+(?:\.\d+){1,3}(?:[-+.][0-9A-Za-z.-]+)?$")
# GitHub Actions는 `@v4`처럼 major만 적는 태그도 사용하므로 일반 패키지
# 태그 정규식과 분리한다. 실제 action major를 원격에서 확인하지는 않는다.
WORKFLOW_TAG_RE = re.compile(r"^(?:[A-Za-z0-9._-]+-)?v?\d+(?:\.\d+){0,3}(?:[-+.][0-9A-Za-z.-]+)?$")
FLOATING_NAMES = frozenset({"main", "master", "develop", "dev", "head", "latest", "trunk"})
VERSION_RE = re.compile(r"v?(\d+)(?:\.(\d+))?(?:\.(\d+))?(?:\.(\d+))?(?:-slim|\+[0-9A-Za-z]+(?:[.-][0-9A-Za-z]+)*)?")
NPM_VERSION_RE = re.compile(r"(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?")
REQ_RE = re.compile(r"^\s*([A-Za-z0-9][A-Za-z0-9._-]*)\s*(\[[^\]]*\])?\s*(.*)$")
EXACT_REQUIREMENT_RE = re.compile(r"^==\s*(v?\d+(?:\.\d+){0,3})\s*$")


# --------------------------------------------------------------------------- 버전 비교

def parse_version(text: str | None) -> tuple[int, ...] | None:
    """지원 형식 전체를 확인하고 숫자 튜플을 돌려준다. `3.12-slim` → (3, 12)."""
    if not isinstance(text, str) or not text:
        return None
    match = VERSION_RE.fullmatch(text.strip())
    if match is None:
        return None
    return tuple(int(group) for group in match.groups() if group is not None)


def normalize_name(name: str) -> str:
    return re.sub(r"[-_.]+", "-", name.strip().lower())


def package_identity(ecosystem: str, name: str) -> str:
    """npm의 서로 다른 점·밑줄·하이픈 이름을 Python 정규화로 합치지 않는다."""
    return normalize_name(name) if ecosystem == "pypi" else name.strip()


def installed_version(ecosystem: str, text: str | None) -> tuple[int, ...] | None:
    """설치본의 지원 문법을 검사한 뒤 build metadata를 제외한 수치를 읽는다."""
    if not isinstance(text, str):
        return None
    if ecosystem == "npm":
        return parse_version(text.split("+", 1)[0]) if NPM_VERSION_RE.fullmatch(text) else None
    if "-slim" in text:
        return None
    return parse_version(text)


def npm_entry(packages: dict, directory: str, name: str) -> tuple[str, dict]:
    """lock 안에서 각 상위 node_modules를 찾으며 파일시스템 링크는 따라가지 않는다."""
    while True:
        if directory.rsplit("/", 1)[-1] == "node_modules":
            directory = directory.rsplit("/", 1)[0] if "/" in directory else ""
            continue
        path = f"{directory}/node_modules/{name}" if directory else f"node_modules/{name}"
        if path in packages:
            return path, packages[path]
        if not directory:
            return "", {}
        directory = directory.rsplit("/", 1)[0] if "/" in directory else ""


def below(installed: tuple[int, ...], floor: tuple[int, ...]) -> bool:
    width = max(len(installed), len(floor))
    return installed + (0,) * (width - len(installed)) < floor + (0,) * (width - len(floor))


def at_or_above(installed: tuple[int, ...], limit: tuple[int, ...]) -> bool:
    return not below(installed, limit)


def same_version(left: tuple[int, ...], right: tuple[int, ...]) -> bool:
    return not below(left, right) and not below(right, left)


def matches_prefix(installed: tuple[int, ...], prefix: tuple[int, ...]) -> bool:
    return installed[:len(prefix)] == prefix


@dataclass(frozen=True)
class Bound:
    lower: tuple[int, ...] | None
    exact: bool


def lower_bound(spec: str | None) -> Bound | None:
    """단일 숫자·접두 연산자 또는 >=/< 교집합의 하한. 미지원 문법은 미확인이다."""
    if spec is None:
        return None
    text = re.sub(r"(>=|<=|==|~=|!=|>|<|\^|~|=)\s+", r"\1", spec.strip())
    if not text or text in {"*", "latest", "x"}:
        return Bound(None, False)
    lows: list[tuple[int, ...]] = []
    exact = False
    for alternative in text.split("||"):
        parts = [part.strip() for part in re.split(r",|\s+", alternative) if part.strip()]
        alt_low: tuple[int, ...] | None = None
        alt_upper: tuple[int, ...] | None = None
        alt_exact = False
        for part in parts:
            operator = ""
            for candidate in (">=", "<=", "==", "~=", "!=", ">", "<", "^", "~", "="):
                if part.startswith(candidate):
                    operator = candidate
                    part = part[len(candidate):].strip()
                    break
            if operator in {">", "<=", "!="} or (len(parts) > 1 and operator not in {">=", "<"}):
                return Bound(None, False)
            if not re.fullmatch(r"v?\d+(?:\.\d+){0,3}(?:\.[xX*])?", part):
                return Bound(None, False)
            version = parse_version(re.sub(r"(?:\.[xX*])$", "", part))
            if version is None:
                return Bound(None, False)
            if operator == "<":
                if alt_upper is None or below(version, alt_upper):
                    alt_upper = version
                continue
            if operator in {"", "=", "=="}:
                alt_exact = "x" not in part and "*" not in part and len(version) >= 2
            if alt_low is None or below(alt_low, version):
                alt_low = version
        if alt_low is None:
            return Bound(None, False)
        if alt_upper is not None and at_or_above(alt_low, alt_upper):
            return Bound(None, False)
        lows.append(alt_low)
        exact = exact or (alt_exact and len(parts) == 1)
    if not lows:
        return Bound(None, False)
    lowest = lows[0]
    for candidate in lows[1:]:
        if below(candidate, lowest):
            lowest = candidate
    return Bound(lowest, exact and len(lows) == 1)


def range_contains(version: tuple[int, ...], spec: str) -> bool:
    """`>=2`, `>=2,<3`, `==2.1.1` 같은 차단 범위에 포함되는지."""
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        operator = ""
        for candidate in (">=", "<=", "==", "!=", ">", "<"):
            if part.startswith(candidate):
                operator, part = candidate, part[len(candidate):].strip()
                break
        bound = parse_version(part)
        if bound is None:
            return False
        if operator in {"", "=="} and not matches_prefix(version, bound):
            return False
        if operator == ">=" and below(version, bound):
            return False
        if operator == ">" and (below(version, bound) or matches_prefix(version, bound)):
            return False
        if operator == "<" and at_or_above(version, bound):
            return False
        if operator == "<=" and at_or_above(version, bound) and not matches_prefix(version, bound):
            return False
        if operator == "!=" and matches_prefix(version, bound):
            return False
    return True


# --------------------------------------------------------------------------- 자료 구조

@dataclass
class Finding:
    repo: str
    scope: str
    key: str
    ecosystem: str
    declared: str
    installed: str
    verdict: str
    detail: str = ""


@dataclass
class Scope:
    kind: str  # npm | python
    label: str
    manifest: Path | None
    lock: Path | None
    lock_kind: str = ""  # package-lock | uv | poetry | requirements | none
    workspace: str = ""  # lock 기준 상대 경로(워크스페이스 멤버일 때)
    note: str = ""
    root: Path | None = None  # strict 매니페스트의 소비자 저장소 루트


@dataclass
class Registry:
    data: dict
    path: Path
    axes: dict = field(default_factory=dict)
    by_package: dict = field(default_factory=dict)

    @classmethod
    def load(cls, path: Path) -> "Registry":
        data = json.loads(path.read_text(encoding="utf-8"))
        def fields(value, allowed, label, required=()):
            if not isinstance(value, dict):
                raise ValueError(f"{path}: {label}은 객체여야 함")
            unknown = set(value) - set(allowed)
            missing = set(required) - set(value)
            if unknown or missing:
                raise ValueError(f"{path}: {label} 미지 필드 {sorted(unknown)}, 누락 {sorted(missing)}")

        def strings(value, names, label):
            for name in names:
                if name in value and (not isinstance(value[name], str) or not value[name].strip()):
                    raise ValueError(f"{path}: {label}.{name}은 빈 문자열이 아니어야 함")

        def iso_date(value, label):
            if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
                raise ValueError(f"{path}: {label}은 YYYY-MM-DD 날짜여야 함")
            date.fromisoformat(value)

        fields(data, {"schema", "baseline", "updated", "next_review", "policy", "source",
                      "semantics", "axes", "actions", "exceptions", "blocked", "consumers", "providers"},
               "registry", {"schema", "axes"})
        if data.get("schema") != REGISTRY_SCHEMA:
            raise ValueError(f"{path}: schema가 {REGISTRY_SCHEMA}가 아님: {data.get('schema')!r}")
        strings(data, ("policy", "source"), "registry")
        for name in ("baseline", "next_review"):
            if name in data:
                value = data[name]
                if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}", value):
                    raise ValueError(f"{path}: {name}은 YYYY-MM이어야 함")
                iso_date(value + "-01", name)
        if "updated" in data:
            iso_date(data["updated"], "updated")
        semantics = data.get("semantics", {})
        fields(semantics, {"floor", "recommended", "max", "checked", "packages"}, "semantics")
        strings(semantics, semantics, "semantics")
        actions = data.get("actions", {})
        fields(actions, {"consumer_policy", "common", "checked", "source"}, "actions")
        strings(actions, ("consumer_policy", "source"), "actions")
        if "checked" in actions and actions["checked"] is not False:
            raise ValueError(f"{path}: actions는 아직 미검사이므로 checked: false만 허용")
        common_actions = actions.get("common", {})
        if not isinstance(common_actions, dict) or any(
                not re.fullmatch(r"[\w.-]+/[\w.-]+", name)
                or not isinstance(ref, str) or not re.fullmatch(r"v\d+", ref)
                for name, ref in common_actions.items()):
            raise ValueError(f"{path}: actions.common은 owner/action: vN 정책이어야 함")
        providers = data.get("providers", {})
        fields(providers, {"policy", "packages", "note", "source"}, "providers")
        strings(providers, ("note", "source"), "providers")
        if providers.get("policy", "report") != "report":
            raise ValueError(f"{path}: providers.policy는 report만 허용")
        provider_packages = providers.get("packages", {})
        if not isinstance(provider_packages, dict):
            raise ValueError(f"{path}: providers.packages는 객체여야 함")
        for name, provider in provider_packages.items():
            fields(provider, {"repo"}, f"providers.packages.{name}", {"repo"})
            strings(provider, ("repo",), f"providers.packages.{name}")
            if not name.strip() or not provider["repo"].startswith("https://"):
                raise ValueError(f"{path}: provider 이름 또는 저장소 URL 오류")
        axes = data.get("axes")
        if not isinstance(axes, dict) or not axes:
            raise ValueError(f"{path}: axes가 비어 있음")
        registry = cls(data, path, axes)
        for key, axis in axes.items():
            fields(axis, {"ecosystem", "packages", "floor", "recommended", "max", "image", "check",
                          "checked", "note", "source"}, f"axes.{key}", {"ecosystem"})
            if axis["ecosystem"] not in {"runtime", "npm", "pypi", "image", "tool", "db"}:
                raise ValueError(f"{path}: axes.{key}.ecosystem 오류")
            strings(axis, ("image", "check", "note", "source"), f"axes.{key}")
            for field_name in ("floor", "recommended", "max"):
                value = axis.get(field_name)
                if value is not None and (parse_version(value) is None
                        or ("-" in value and axis["ecosystem"] != "image")):
                    raise ValueError(f"{path}: axes.{key}.{field_name} 버전 오류")
            floor, recommended, maximum = (parse_version(axis.get(n)) for n in ("floor", "recommended", "max"))
            if ((floor is not None and recommended is not None and below(recommended, floor))
                    or (maximum is not None and any(v is not None and at_or_above(v, maximum)
                                                    for v in (floor, recommended)))):
                raise ValueError(f"{path}: axes.{key}은 floor <= recommended < max 순서여야 함")
            if "checked" in axis and not isinstance(axis["checked"], bool):
                raise ValueError(f"{path}: axes.{key}.checked는 bool이어야 함")
            names = axis.get("packages", [key])
            if not isinstance(names, list) or not names or any(not isinstance(n, str) or not n for n in names):
                raise ValueError(f"{path}: axes.{key}.packages 목록 오류")
            for name in axis.get("packages", [key]):
                identity = (axis["ecosystem"], package_identity(axis["ecosystem"], name))
                if identity in registry.by_package:
                    raise ValueError(f"{path}: 패키지 축 중복 {name}")
                registry.by_package[identity] = key
        consumers = data.get("consumers", {})
        if not isinstance(consumers, dict):
            raise ValueError(f"{path}: consumers는 객체여야 함")
        aliases = {name.lower() for name in consumers}
        for name, entry in consumers.items():
            fields(entry, {"enforce", "clean_runs", "aliases", "note"}, f"consumers.{name}", {"enforce"})
            strings(entry, ("note",), f"consumers.{name}")
            if entry["enforce"] not in MODES:
                raise ValueError(f"{path}: consumers.{name}.enforce 오류")
            if not isinstance(entry.get("aliases", []), list):
                raise ValueError(f"{path}: consumers.{name}.aliases 목록 오류")
            for alias in entry.get("aliases", []):
                if not isinstance(alias, str) or not alias or (alias.lower() in aliases and alias.lower() != name.lower()):
                    raise ValueError(f"{path}: 소비자 별칭 오류 또는 중복")
                aliases.add(alias.lower())
            runs = entry.get("clean_runs", 0)
            if type(runs) is not int or runs < 0:
                raise ValueError(f"{path}: consumers.{name}.clean_runs 오류")
        for name in ("exceptions", "blocked"):
            if not isinstance(data.get(name, []), list):
                raise ValueError(f"{path}: {name}는 목록이어야 함")
        exception_prefixes: dict[tuple[str, str], list[tuple[int, ...]]] = {}
        for entry in data.get("exceptions", []):
            names = {"repo", "key", "installed", "reason", "until", "review"}
            fields(entry, names, "exceptions 항목", names)
            if any(not isinstance(entry[n], str) or not entry[n].strip() for n in names):
                raise ValueError(f"{path}: exceptions 값은 빈 문자열이 아니어야 함")
            if entry["repo"] not in consumers or entry["key"] not in axes or parse_version(entry["installed"]) is None:
                raise ValueError(f"{path}: exceptions 참조 또는 버전 오류")
            iso_date(entry["until"], "exceptions.until")
            prefix = parse_version(entry["installed"])
            if not re.fullmatch(r"\d+(?:\.\d+){0,3}", entry["installed"]):
                raise ValueError(f"{path}: exceptions.installed는 숫자 접두여야 함")
            previous = exception_prefixes.setdefault((entry["repo"], entry["key"]), [])
            if any(matches_prefix(prefix, old) or matches_prefix(old, prefix) for old in previous):
                raise ValueError(f"{path}: 같은 저장소·축의 예외 접두가 겹침")
            previous.append(prefix)
        for entry in data.get("blocked", []):
            fields(entry, {"ecosystem", "name", "range", "reason", "since", "source"}, "blocked 항목",
                   {"ecosystem", "name", "range", "reason"})
            if entry["ecosystem"] not in {"npm", "pypi"}:
                raise ValueError(f"{path}: blocked ecosystem 오류")
            if any(not isinstance(entry[n], str) or not entry[n] for n in ("name", "range", "reason")):
                raise ValueError(f"{path}: blocked 문자열 오류")
            strings(entry, ("source",), "blocked")
            if "since" in entry:
                iso_date(entry["since"], "blocked.since")
            for clause in entry["range"].split(","):
                number = re.sub(r"^\s*(?:>=|<=|==|!=|>|<)?", "", clause).strip()
                if (not re.fullmatch(r"\s*(?:>=|<=|==|!=|>|<)?\d+(?:\.\d+)*\s*", clause)
                        or parse_version(number) is None):
                    raise ValueError(f"{path}: blocked 범위 오류")
        return registry

    def axis_for(self, ecosystem: str, name: str) -> str | None:
        return self.by_package.get((ecosystem, package_identity(ecosystem, name)))

    def consumer(self, repo: str) -> str | None:
        consumers = self.data.get("consumers", {})
        if repo in consumers:
            return repo
        lowered = repo.lower()
        for name, entry in consumers.items():
            aliases = {alias.lower() for alias in entry.get("aliases", [])}
            if lowered == name.lower() or lowered in aliases:
                return name
        return None

    def enforce(self, repo: str) -> str:
        name = self.consumer(repo)
        if name is None:
            return "report"
        mode = self.data["consumers"][name].get("enforce", "report")
        return mode

    def exception(self, repo: str, key: str, installed: tuple[int, ...] | None):
        if installed is None:
            return None
        name = self.consumer(repo) or repo
        for entry in self.data.get("exceptions", []):
            if entry["repo"] != name or entry["key"] != key:
                continue
            prefix = parse_version(entry["installed"])
            if prefix is not None and matches_prefix(installed, prefix):
                return entry
        return None

    def blocked(self, ecosystem: str, name: str, version: tuple[int, ...] | None):
        if version is None:
            return None
        for entry in self.data.get("blocked", []):
            if entry["ecosystem"] == ecosystem and package_identity(ecosystem, entry["name"]) == package_identity(ecosystem, name):
                if range_contains(version, entry["range"]):
                    return entry
        return None

    def blocked_name(self, ecosystem: str, name: str) -> bool:
        return any(entry["ecosystem"] == ecosystem
                   and package_identity(ecosystem, entry["name"]) == package_identity(ecosystem, name)
                   for entry in self.data.get("blocked", []))

    def provider_names(self) -> set[str]:
        packages = self.data.get("providers", {}).get("packages", {})
        return {normalize_name(name) for name in packages}


# --------------------------------------------------------------------------- 파일 읽기

def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def read_toml(path: Path) -> dict:
    with path.open("rb") as handle:
        return tomllib.load(handle)


POETRY_TOP_FIELDS = frozenset({"package", "metadata", "extras"})
POETRY_PACKAGE_FIELDS = frozenset({
    "name", "version", "description", "category", "optional", "python-versions", "groups",
    "files", "dependencies", "extras", "source", "develop", "markers",
})
POETRY_SOURCE_FIELDS = frozenset({"type", "url", "reference", "resolved_reference", "subdirectory"})
POETRY_SOURCE_TYPES = frozenset({"git", "url", "legacy", "file", "directory"})


def _poetry_error() -> ValueError:
    """Poetry 입력 원문을 출력하지 않는 일반 오류."""
    return ValueError("poetry.lock 지원 형식 오류")


def _validate_bracketed_host(netloc: str) -> None:
    """URL authority의 대괄호 호스트가 실제 IPv6 주소인지 확인한다."""
    if "[" not in netloc and "]" not in netloc:
        return
    if "@" in netloc:
        userinfo = netloc.rsplit("@", 1)[0]
        if "[" in userinfo or "]" in userinfo:
            raise ValueError("URL 호스트 형식 오류")
    authority = netloc.rsplit("@", 1)[-1]
    if not authority.startswith("["):
        raise ValueError("URL 호스트 형식 오류")
    closing = authority.find("]")
    if closing <= 1:
        raise ValueError("URL 호스트 형식 오류")
    host = authority[1:closing]
    try:
        ipaddress.ip_address(host)
    except ValueError as exc:
        raise ValueError("URL 호스트 형식 오류") from exc
    suffix = authority[closing + 1:]
    if suffix and not re.fullmatch(r":\d+", suffix):
        raise ValueError("URL 호스트 형식 오류")


def _parse_url(value: str):
    """URL을 파싱하고 파서가 놓치는 잘못된 대괄호 호스트도 거부한다."""
    parsed_text = value.removeprefix("git+")
    try:
        parsed = urlsplit(parsed_text)
        # hostname/port 접근은 잘못된 bracket·port를 표준 라이브러리에서
        # ValueError로 닫게 한다. 원문은 예외 메시지에 재출력하지 않는다.
        hostname = parsed.hostname
        parsed.port
        _validate_bracketed_host(parsed.netloc)
    except ValueError as exc:
        raise ValueError("URL 형식 오류") from exc
    return parsed, hostname


def _validate_url(value: object, *, require_host: bool) -> str:
    if not isinstance(value, str) or not value.strip() or "\x00" in value:
        raise _poetry_error()
    text = value.strip()
    # Poetry는 git+ 접두를 기록하기도 하고, 일반 git URL을 기록하기도 한다.
    try:
        parsed, hostname = _parse_url(text)
    except ValueError as exc:
        raise _poetry_error() from exc
    if require_host and (not parsed.scheme or not hostname):
        raise _poetry_error()
    return text


def read_poetry_lock(path: Path) -> dict:
    """Poetry lock의 제한된 package/source 구조를 fail-close로 읽는다."""
    try:
        data = read_toml(path)
    except (tomllib.TOMLDecodeError, UnicodeError) as exc:
        raise _poetry_error() from exc
    if not isinstance(data, dict) or set(data) - POETRY_TOP_FIELDS:
        raise _poetry_error()
    packages = data.get("package")
    metadata = data.get("metadata")
    extras = data.get("extras", {})
    if (not isinstance(packages, list) or not isinstance(metadata, dict)
            or not isinstance(extras, (dict, list))):
        raise _poetry_error()
    python_versions = metadata.get("python-versions")
    if (not isinstance(python_versions, str) or not python_versions.strip()
            or _range_interval(python_versions) is None
            or not any(item[0] is not None or item[2] is not None for item in _range_interval(python_versions))):
        raise _poetry_error()
    for entry in packages:
        if not isinstance(entry, dict) or set(entry) - POETRY_PACKAGE_FIELDS:
            raise _poetry_error()
        name, version = entry.get("name"), entry.get("version")
        if (not isinstance(name, str) or not name.strip()
                or not isinstance(version, str) or not version.strip()):
            raise _poetry_error()
        source = entry.get("source")
        if source is None:
            continue
        if not isinstance(source, dict) or set(source) - POETRY_SOURCE_FIELDS:
            raise _poetry_error()
        source_type = source.get("type")
        if not isinstance(source_type, str) or source_type not in POETRY_SOURCE_TYPES:
            raise _poetry_error()
        for field_name in ("url", "reference", "resolved_reference"):
            if field_name in source and (
                    not isinstance(source[field_name], str) or not source[field_name].strip()):
                raise _poetry_error()
        if source_type in {"git", "url", "legacy"}:
            if "url" not in source:
                raise _poetry_error()
            _validate_url(source["url"], require_host=True)
        elif "url" in source:
            _validate_url(source["url"], require_host=False)
        else:
            raise _poetry_error()
        if "subdirectory" in source and (
                not isinstance(source["subdirectory"], str) or not source["subdirectory"].strip()):
            raise _poetry_error()
        if source_type == "git" and "resolved_reference" in source:
            # SHA 이외의 값은 오류가 아니라 부동 참조로 보고한다.
            if not source["resolved_reference"].strip():
                raise _poetry_error()
    return data


def _strip_inline_comment(line: str) -> str:
    """공백 또는 탭 뒤의 주석만 제거한다(URL fragment의 `#`는 보존)."""
    return re.split(r"[ \t]+#", line, maxsplit=1)[0].rstrip()


def _include_path(value: str) -> str:
    """requirements include 인자를 따옴표 하나의 경로로 정규화한다."""
    value = value.strip()
    if not value:
        raise ValueError("requirements.txt 입력 구조 오류")
    if value[0] in {"'", '"'}:
        quote = value[0]
        if len(value) < 2 or value[-1] != quote or quote in value[1:-1]:
            raise ValueError("requirements.txt 입력 구조 오류")
        return value[1:-1]
    if "'" in value or '"' in value:
        raise ValueError("requirements.txt 입력 구조 오류")
    return value


def _editable_requirement(line: str) -> str | None:
    """지원하는 editable git 행을 일반 PEP 508 URL 행으로 바꾼다."""
    match = re.match(r"^(?:-e|--editable)(?:=|[ \t]+)(.+)$", line)
    if match is None:
        return None
    value = match[1].strip()
    if not value:
        raise ValueError("requirements.txt 입력 구조 오류")
    try:
        parsed = urlsplit(value)
    except ValueError as exc:
        raise ValueError("requirements.txt 입력 구조 오류") from exc
    egg = next((item.split("=", 1)[1] for item in parsed.fragment.split("&")
                if item.startswith("egg=") and "=" in item), None)
    if not egg or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", egg):
        raise ValueError("requirements.txt 입력 구조 오류")
    if not value.lower().startswith(("git+", "git:", "github:", "gitlab:", "bitbucket:")):
        raise ValueError("requirements.txt 입력 구조 오류")
    without_egg = urlunsplit((parsed.scheme, parsed.netloc, parsed.path, parsed.query, ""))
    return f"{egg} @ {without_egg}"


def _strip_requirement_hashes(line: str) -> str:
    """선언 행의 per-requirement `--hash` 토큰을 제거하고 형식을 검증한다."""
    try:
        # posix=False로 marker의 문자열 인용부호를 보존한다. 인용부호를
        # 제거하면 `>=`가 `>`와 `=`로 다시 해석되는 등 잘못된 marker가
        # 정상 입력으로 통과할 수 있다.
        tokens = shlex.split(line, posix=False)
    except ValueError as exc:
        raise ValueError("requirements.txt 입력 구조 오류") from exc
    kept: list[str] = []
    index = 0
    while index < len(tokens):
        token = tokens[index]
        if token == "--hash":
            index += 1
            hash_value = tokens[index] if index < len(tokens) else ""
            if len(hash_value) >= 2 and hash_value[0] in {"'", '"'} and hash_value[-1] == hash_value[0]:
                hash_value = hash_value[1:-1]
            if not re.fullmatch(r"[A-Za-z0-9_-]+:[0-9A-Fa-f]+", hash_value):
                raise ValueError("requirements.txt 입력 구조 오류")
        elif token.startswith("--hash="):
            hash_value = token[len("--hash="):]
            if len(hash_value) >= 2 and hash_value[0] in {"'", '"'} and hash_value[-1] == hash_value[0]:
                hash_value = hash_value[1:-1]
            if not re.fullmatch(r"[A-Za-z0-9_-]+:[0-9A-Fa-f]+", hash_value):
                raise ValueError("requirements.txt 입력 구조 오류")
        elif token.startswith("--"):
            kept.append(token)
        else:
            kept.append(token)
        index += 1
    return " ".join(kept)


REQUIREMENTS_IGNORED_OPTIONS = frozenset({
    "--no-index", "--pre", "--require-hashes", "--use-pep517", "--no-use-pep517",
    "--prefer-binary", "--no-cache-dir",
})
REQUIREMENTS_VALUE_OPTIONS = frozenset({
    "--index-url", "--extra-index-url", "--trusted-host", "--find-links",
})
REQUIREMENTS_PARAMETER_OPTIONS = frozenset({"--only-binary", "--no-binary"})


def read_requirements(path: Path, *, _stack: tuple[Path, ...] = (), root: Path | None = None) -> list[str]:
    """`-r`/`--requirement`를 재귀 확장하고 유효한 선언 행만 돌려준다."""
    try:
        path = path.resolve()
        if root is not None:
            root = root.resolve()
    except (OSError, RuntimeError) as exc:
        raise ValueError("requirements.txt 입력 구조 오류") from exc
    if root is not None and not _path_within(path, root):
        raise ValueError("requirements.txt 입력 구조 오류")
    if path in _stack or not path.is_file():
        raise ValueError("requirements.txt 입력 구조 오류")
    try:
        raw_lines = path.read_text(encoding="utf-8-sig").splitlines()
    except (OSError, UnicodeError) as exc:
        raise ValueError("requirements.txt 입력 구조 오류") from exc
    lines: list[str] = []
    pending = ""
    for raw in raw_lines:
        current = raw.strip()
        pending = (pending + " " + current) if pending else current
        if pending.endswith("\\"):
            pending = pending[:-1].rstrip()
            continue
        if pending:
            lines.append(pending)
        pending = ""
    if pending:
        raise ValueError("requirements.txt 입력 구조 오류")

    result: list[str] = []
    stack = _stack + (path,)
    for original in lines:
        line = _strip_inline_comment(original).strip()
        if not line or line.startswith("#"):
            continue
        include: str | None = None
        if re.match(r"^-r(?:[ \t]+|$)", line) or (line.startswith("-r") and not line.startswith("--")):
            include = _include_path(line[2:])
        elif line == "--requirement" or line.startswith("--requirement=") or line.startswith("--requirement ") or line.startswith("--requirement\t"):
            value = line[len("--requirement"):]
            include = _include_path(value[1:] if value.startswith("=") else value)
        if include is not None:
            if not include:
                raise ValueError("requirements.txt 입력 구조 오류")
            result.extend(read_requirements(path.parent / include, _stack=stack, root=root))
            continue
        editable = _editable_requirement(line)
        if editable is not None:
            result.append(editable)
            continue
        if line.startswith(("-e", "--editable")):
            raise ValueError("requirements.txt 입력 구조 오류")
        normalized = _strip_requirement_hashes(line)
        if not normalized:
            raise ValueError("requirements.txt 입력 구조 오류")
        tokens = normalized.split()
        option = tokens[0]
        if option in REQUIREMENTS_IGNORED_OPTIONS:
            if len(tokens) != 1:
                raise ValueError("requirements.txt 입력 구조 오류")
            continue
        option_name, separator, option_value = option.partition("=")
        if option_name in REQUIREMENTS_VALUE_OPTIONS:
            if (separator and not option_value) or (not separator and len(tokens) != 2):
                raise ValueError("requirements.txt 입력 구조 오류")
            continue
        if option_name in REQUIREMENTS_PARAMETER_OPTIONS:
            if separator:
                if not option_value:
                    raise ValueError("requirements.txt 입력 구조 오류")
            elif len(tokens) != 2 or not tokens[1]:
                raise ValueError("requirements.txt 입력 구조 오류")
            continue
        if option.startswith("-"):
            raise ValueError("requirements.txt 입력 구조 오류")
        if parse_requirement(normalized, strict=True) is None:
            raise ValueError("requirements.txt 입력 구조 오류")
        result.append(normalized)
    return result


def exact_requirement_version(spec: str) -> str | None:
    match = EXACT_REQUIREMENT_RE.fullmatch(spec.strip())
    if match is None or parse_version(match[1]) is None:
        return None
    return match[1]


def _range_interval(spec: str):
    """PEP 440의 하한·상한을 닫힌/열린 구간으로 보수적으로 해석한다."""

    def next_release(version: tuple[int, ...], operator: str) -> tuple[int, ...]:
        values = list(version)
        if operator == "^":
            if values[0] > 0:
                return (values[0] + 1,)
            if len(values) > 1 and values[1] > 0:
                return (0, values[1] + 1)
            return (0, 0, (values[2] + 1) if len(values) > 2 else 1)
        if operator == "~=":
            if len(values) <= 2:
                return (values[0] + 1,)
            return tuple(values[:-2] + [values[-2] + 1])
        if operator == "~":
            if len(values) <= 1:
                return (values[0] + 1,)
            return tuple(values[:-1] + [values[-1] + 1])
        return tuple(values)

    def parse_version_token(token: str) -> tuple[tuple[int, ...], tuple[int, ...] | None] | None:
        if token in {"", "*", "x", "X"}:
            return None
        wildcard = re.fullmatch(r"(v?\d+(?:\.\d+)*)\.[xX*]", token)
        if wildcard:
            lower = parse_version(wildcard[1])
            if lower is None:
                return None
            values = list(lower)
            values[-1] += 1
            return lower, tuple(values)
        version = parse_version(token)
        if version is None or "*" in token.lower() or "x" in token.lower():
            return None
        return version, None

    def update_lower(old, old_inc, new, new_inc):
        if old is None or below(old, new):
            return new, new_inc
        if same_version(old, new):
            return old, old_inc and new_inc
        return old, old_inc

    def update_upper(old, old_inc, new, new_inc):
        if old is None or below(new, old):
            return new, new_inc
        if same_version(old, new):
            return old, old_inc and new_inc
        return old, old_inc

    intervals = []
    for alternative in spec.split("||"):
        normalized = re.sub(r"(===|==|!=|~=|>=|<=|>|<|\^|~|=)\s+", r"\1", alternative.strip())
        if not normalized:
            return None
        parts = [part for part in re.split(r"[,\s]+", normalized) if part]
        if not parts:
            return None
        lower = upper = None
        lower_inclusive = upper_inclusive = True
        exclusions: list[tuple[int, ...]] = []
        for part in parts:
            match = re.match(r"^(===|==|!=|~=|>=|<=|>|<|\^|~|=)?(.*)$", part)
            if match is None:
                return None
            operator = match[1] or ""
            token = match[2]
            if token in {"*", "x", "X"}:
                if operator == "":
                    continue
                return None
            parsed = parse_version_token(token)
            if parsed is None:
                return None
            version, wildcard_upper = parsed
            if operator in {"==", "="} and wildcard_upper is not None:
                lower, lower_inclusive = update_lower(lower, lower_inclusive, version, True)
                upper, upper_inclusive = update_upper(upper, upper_inclusive, wildcard_upper, False)
                continue
            if wildcard_upper is not None:
                if operator == "!=":
                    # 제외 wildcard는 구간으로 정확히 표현하지 못하므로 전체와 겹칠
                    # 가능성이 있는 것으로 남겨 둔다(보수적 BLOCKED).
                    continue
                return None
            if operator in {"", "===", "=="}:
                lower, lower_inclusive = update_lower(lower, lower_inclusive, version, True)
                upper, upper_inclusive = update_upper(upper, upper_inclusive, version, True)
            elif operator == "!=":
                exclusions.append(version)
            elif operator in {">=", ">"}:
                lower, lower_inclusive = update_lower(lower, lower_inclusive, version, operator == ">=")
            elif operator in {"<", "<="}:
                upper, upper_inclusive = update_upper(upper, upper_inclusive, version, operator == "<=")
            elif operator in {"^", "~", "~="}:
                lower, lower_inclusive = update_lower(lower, lower_inclusive, version, True)
                upper, upper_inclusive = update_upper(upper, upper_inclusive,
                                                      next_release(version, operator), False)
            else:
                return None
        if (lower is not None and upper is not None
                and (below(upper, lower)
                     or (same_version(lower, upper) and not (lower_inclusive and upper_inclusive)))):
            return None
        intervals.append((lower, lower_inclusive, upper, upper_inclusive, exclusions))
    return intervals or None


def ranges_overlap(left: str, right: str) -> bool:
    """두 선언 범위가 겹치는지 보수적으로 판단한다. 해석 불가면 겹침으로 닫는다."""
    left_intervals, right_intervals = _range_interval(left), _range_interval(right)
    if left_intervals is None or right_intervals is None:
        return True
    for a_lower, a_lower_inc, a_upper, a_upper_inc, a_exclusions in left_intervals:
        for b_lower, b_lower_inc, b_upper, b_upper_inc, b_exclusions in right_intervals:
            lower = a_lower
            lower_inc = a_lower_inc
            if lower is None or (b_lower is not None and below(lower, b_lower)):
                lower, lower_inc = b_lower, b_lower_inc
            elif b_lower is not None and same_version(lower, b_lower):
                lower_inc = lower_inc and b_lower_inc
            upper = a_upper
            upper_inc = a_upper_inc
            if upper is None or (b_upper is not None and below(b_upper, upper)):
                upper, upper_inc = b_upper, b_upper_inc
            elif b_upper is not None and same_version(upper, b_upper):
                upper_inc = upper_inc and b_upper_inc
            if lower is not None and upper is not None:
                if below(upper, lower) or (same_version(lower, upper) and not (lower_inc and upper_inc)):
                    continue
            if lower is not None and any(same_version(lower, excluded)
                                         for excluded in a_exclusions + b_exclusions):
                if upper is not None and same_version(lower, upper):
                    continue
            return True
    return False


UV_TOP_FIELDS = frozenset({
    "version", "revision", "requires-python", "resolution-markers", "supported-markers",
    "required-markers", "conflicts", "options", "manifest", "package", "distribution",
})
UV_PACKAGE_FIELDS = frozenset({
    "name", "version", "source", "dependencies", "optional-dependencies", "dependency-groups",
    "dev-dependencies", "resolution-markers", "metadata", "sdist", "wheels",
})
UV_SOURCE_FIELDS = frozenset({"registry", "git", "editable", "directory", "virtual"})
UV_SUPPORTED_REVISION = 4
DEPENDENCY_GROUP_NAME_RE = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9._-]*[A-Za-z0-9])?$")


def _uv_error(path: Path, detail: str) -> ValueError:
    return ValueError("uv.lock 지원 형식 오류")


def _manifest_input_error() -> ValueError:
    """입력의 이름·경로·값을 로그에 재출력하지 않는 manifest 오류."""
    return ValueError("Python manifest 지원 형식 오류")


def uv_source_kind(source: object, path: Path, package_name: str) -> str:
    """uv package source의 제한된 네 종류를 확인하고 종류를 돌려준다."""
    if not isinstance(source, dict):
        raise _uv_error(path, f"package {package_name!r}의 source는 객체여야 함")
    unknown = set(source) - UV_SOURCE_FIELDS
    if unknown:
        raise _uv_error(path, f"package {package_name!r} source 미지 필드 {sorted(unknown)}")
    kinds = [key for key in UV_SOURCE_FIELDS if key in source]
    if len(kinds) != 1 or not isinstance(source[kinds[0]], str) or not source[kinds[0]].strip():
        raise _uv_error(path, f"package {package_name!r} source 종류·값이 잘못됨")
    if kinds[0] in {"registry", "git"}:
        try:
            parsed, hostname = _parse_url(source[kinds[0]])
        except ValueError as exc:
            raise _uv_error(path, "source URL 형식 오류") from exc
        if not parsed.scheme or not hostname:
            raise _uv_error(path, "source URL 형식 오류")
    elif "\x00" in source[kinds[0]]:
        raise _uv_error(path, "source 경로 형식 오류")
    return kinds[0]


def read_uv_lock(path: Path) -> dict:
    """uv v1 revision 0~4의 검사 대상 필드만 허용하는 오프라인 파서."""
    try:
        data = read_toml(path)
    except (tomllib.TOMLDecodeError, UnicodeError) as exc:
        raise _uv_error(path, "TOML 형식 오류") from exc
    if not isinstance(data, dict):
        raise _uv_error(path, "최상위가 객체가 아님")
    unknown = set(data) - UV_TOP_FIELDS
    if unknown:
        raise _uv_error(path, f"최상위 미지 필드 {sorted(unknown)}")
    if type(data.get("version")) is not int or data["version"] != 1:
        raise _uv_error(path, "version은 지원하는 정수 1이어야 함")
    revision = data.get("revision", 0)
    if type(revision) is not int or not 0 <= revision <= UV_SUPPORTED_REVISION:
        raise _uv_error(path, f"revision은 0~{UV_SUPPORTED_REVISION} 정수만 지원")
    requires_python = data.get("requires-python")
    if not isinstance(requires_python, str) or not requires_python.strip():
        raise _uv_error(path, "requires-python이 비어 있거나 문자열이 아님")
    if lower_bound(requires_python) is None or lower_bound(requires_python).lower is None:
        raise _uv_error(path, "requires-python의 하한을 해석할 수 없음")
    for field_name in ("resolution-markers", "supported-markers", "required-markers"):
        if field_name in data and (not isinstance(data[field_name], list)
                                   or any(not isinstance(item, str) for item in data[field_name])):
            raise _uv_error(path, "marker 형식 오류")
    for field_name in ("conflicts", "options", "manifest"):
        if field_name in data and not isinstance(data[field_name], (dict, list)):
            raise _uv_error(path, "lock 메타데이터 형식 오류")
    packages = data.get("package", data.get("distribution", []))
    if "package" in data and "distribution" in data:
        raise _uv_error(path, "package와 distribution을 동시에 사용할 수 없음")
    if not isinstance(packages, list):
        raise _uv_error(path, "package는 배열이어야 함")
    for index, entry in enumerate(packages):
        if not isinstance(entry, dict):
            raise _uv_error(path, f"package[{index}]는 객체여야 함")
        unknown_package = set(entry) - UV_PACKAGE_FIELDS
        if unknown_package:
            raise _uv_error(path, f"package[{index}] 미지 필드 {sorted(unknown_package)}")
        name = entry.get("name")
        version = entry.get("version")
        if not isinstance(name, str) or not name.strip():
            raise _uv_error(path, f"package[{index}].name이 비어 있음")
        if not isinstance(version, str):
            raise _uv_error(path, f"package[{name!r}].version은 문자열이어야 함")
        uv_source_kind(entry.get("source"), path, name)
        if "dependencies" in entry and (
                not isinstance(entry["dependencies"], list)
                or any(not isinstance(item, dict)
                       or not isinstance(item.get("name"), str)
                       or not item["name"].strip() for item in entry["dependencies"])):
            raise _uv_error(path, "package dependencies 형식 오류")
        for field_name in ("optional-dependencies", "dependency-groups", "dev-dependencies"):
            if field_name not in entry:
                continue
            value = entry[field_name]
            if (not isinstance(value, dict)
                    or any(not isinstance(items, list)
                           or any(not isinstance(item, dict)
                                  or not isinstance(item.get("name"), str)
                                  or not item["name"].strip() for item in items)
                           for items in value.values())):
                raise _uv_error(path, "package group 형식 오류")
        for field_name in ("metadata", "sdist"):
            if field_name in entry and not isinstance(entry[field_name], dict):
                raise _uv_error(path, "package metadata 형식 오류")
        if "wheels" in entry and (not isinstance(entry["wheels"], list)
                                   or any(not isinstance(item, dict) for item in entry["wheels"])):
            raise _uv_error(path, "package wheel 형식 오류")
        if "resolution-markers" in entry and (
                not isinstance(entry["resolution-markers"], list)
                or any(not isinstance(item, str) for item in entry["resolution-markers"])):
            raise _uv_error(path, "package marker 형식 오류")
    return data


def ref_is_pinned(text: str, *, kind: str = "npm") -> bool:
    """git/URL 참조가 불변 대상(SHA·버전 태그·릴리스 자산)으로 고정돼 있는지.

    고정으로 보는 것: 40자리 SHA, `/tarball|/archive|/commit/<7~40 hex>`, GitHub Release
    자산(`/releases/download/<tag>/…`, D-11), Python `@<태그>`·npm `#<태그>`의 버전형 태그(`v1.2.3`,
    `py-v0.1.0`). 브랜치 이름(`main`·`master`·`develop`)·참조 없음·`semver:` 범위는 floating.
    """
    def valid_ref(ref: str) -> bool:
        return bool(re.fullmatch(r"[0-9a-f]{40}", ref) or TAG_RE.fullmatch(ref))

    if not isinstance(text, str) or not text.strip():
        raise ValueError("git 참조 형식 오류")
    try:
        parsed, hostname = _parse_url(text)
    except ValueError as exc:
        raise ValueError("git 참조 형식 오류") from exc
    if parsed.scheme.lower() in {"http", "https", "ssh", "git"} and not hostname:
        raise ValueError("git 참조 형식 오류")
    path = unquote(parsed.path)
    fragment = unquote(parsed.fragment)
    hosted = parsed.hostname in {"github.com", "gitlab.com"}
    if kind == "uv":
        # uv.lock의 git source fragment는 해석된 전체 commit SHA다.
        return bool(re.fullmatch(r"[0-9a-f]{40}", fragment))
    if hosted:
        release = re.fullmatch(r"/[^/]+/[^/]+/releases/download/([^/]+)/[^/]+", path)
        if release:
            return valid_ref(release[1])
        if re.fullmatch(r"/[^/]+/[^/]+/(?:tarball|archive|commit)/[0-9a-f]{7,40}(?:\.tar\.gz|\.zip)?", path):
            return True
    git_spec = (text.startswith(("git+", "git:", "github:", "gitlab:", "bitbucket:"))
                or (hosted and re.fullmatch(r"/[^/]+/[^/]+", path))
                or re.fullmatch(r"[^/:]+/[^/]+", path) and not parsed.scheme)
    if not git_spec:
        return False
    if kind == "pypi":
        # Python 선언에서 fragment는 subdirectory 등 메타데이터이며 revision이 아니다.
        # manifest에서 branch 종류를 보존하기 위해 넣은 내부 표식은 이름 모양과 무관하게 부동이다.
        if "@branch:" in path:
            return False
        # tag/rev/branch 이름에 `@`가 들어가면 마지막 조각만 버전 태그로 볼 수 없다.
        if path.count("@") != 1:
            return False
        return "@" in path and valid_ref(path.rsplit("@", 1)[1])
    # npm git 선언의 revision은 fragment다. URL query나 Python식 @rev를 혼용하지 않는다.
    return bool(fragment and valid_ref(fragment))


def is_vcs_spec(spec: str) -> bool:
    lowered = spec.lower()
    return (lowered.startswith(("git+", "git:", "github:", "gitlab:", "bitbucket:", "https://", "http://"))
            or "github.com/" in lowered or "gitlab.com/" in lowered
            or bool(re.match(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+(#.*)?$", spec)))


REQUIREMENT_MARKER_NAMES = frozenset({
    "python_version", "python_full_version", "os_name", "sys_platform", "platform_release",
    "platform_system", "platform_version", "platform_machine", "platform_python_implementation",
    "implementation_name", "implementation_version", "extra",
})


def _outer_pair_wraps(text: str) -> bool:
    if not text.startswith("(") or not text.endswith(")"):
        return False
    depth = 0
    quote = ""
    escaped = False
    for index, char in enumerate(text):
        if quote:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                quote = ""
            continue
        if char in {"'", '"'}:
            quote = char
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0 and index != len(text) - 1:
                return False
            if depth < 0:
                return False
    return depth == 0 and not quote


def _marker_boundary(char: str) -> bool:
    return not (char.isalnum() or char == "_")


def _split_marker_top(text: str, keyword: str) -> list[str] | None:
    """인용 문자열·괄호 안을 보존한 채 최상위 boolean 항을 나눈다."""
    parts: list[str] = []
    start = 0
    depth = 0
    quote = ""
    escaped = False
    index = 0
    while index < len(text):
        char = text[index]
        if quote:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                quote = ""
            index += 1
            continue
        if char in {"'", '"'}:
            quote = char
            index += 1
            continue
        if char == "(":
            depth += 1
            index += 1
            continue
        if char == ")":
            depth -= 1
            if depth < 0:
                return None
            index += 1
            continue
        if depth == 0 and text[index:index + len(keyword)] == keyword:
            before = text[index - 1] if index else " "
            after_index = index + len(keyword)
            after = text[after_index] if after_index < len(text) else " "
            if _marker_boundary(before) and _marker_boundary(after):
                parts.append(text[start:index].strip())
                start = after_index
                index = after_index
                continue
        index += 1
    if quote or depth != 0:
        return None
    parts.append(text[start:].strip())
    return parts


def _marker_string(text: str) -> bool:
    """PEP 508 marker 문자열 리터럴인지 확인한다."""
    if len(text) < 2 or text[0] not in {"'", '"'} or text[-1] != text[0]:
        return False
    quote = text[0]
    escaped = False
    for char in text[1:-1]:
        if escaped:
            escaped = False
        elif char == "\\":
            escaped = True
        elif char == quote or char in {"\r", "\n"}:
            return False
    return not escaped


def _marker_operand(text: str) -> tuple[str, str] | None:
    text = text.strip()
    if text in REQUIREMENT_MARKER_NAMES:
        return "name", text
    if _marker_string(text):
        return "value", text
    return None


def _marker_comparison(text: str) -> bool:
    """단일 marker 비교를 확인하며 피연산자 역순도 허용한다."""
    operators = ("not in", "===", "~=", "==", "!=", "<=", ">=", "<", ">", "in")
    depth = 0
    quote = ""
    escaped = False
    index = 0
    while index < len(text):
        char = text[index]
        if quote:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                quote = ""
            index += 1
            continue
        if char in {"'", '"'}:
            quote = char
            index += 1
            continue
        if char == "(":
            depth += 1
            index += 1
            continue
        if char == ")":
            depth -= 1
            if depth < 0:
                return False
            index += 1
            continue
        if depth == 0:
            for operator in operators:
                if text[index:index + len(operator)] != operator:
                    continue
                end = index + len(operator)
                if operator in {"in", "not in"}:
                    before = text[index - 1] if index else " "
                    after = text[end] if end < len(text) else " "
                    if not _marker_boundary(before) or not _marker_boundary(after):
                        continue
                left = _marker_operand(text[:index])
                right = _marker_operand(text[end:])
                if left is None or right is None:
                    return False
                return True
        index += 1
    return False


def _valid_marker_expression(expression: str) -> bool:
    expression = expression.strip()
    if not expression:
        return False
    while _outer_pair_wraps(expression):
        expression = expression[1:-1].strip()
    if not expression:
        return False
    for keyword in ("or", "and"):
        parts = _split_marker_top(expression, keyword)
        if parts is None:
            return False
        if len(parts) > 1:
            return all(_valid_marker_expression(part) for part in parts)
    return _marker_comparison(expression)


def _valid_requirement_marker(marker: str) -> bool:
    return _valid_marker_expression(marker)


def _normalize_requirement_spec(rest: str) -> str | None:
    spec = rest.strip()
    if not spec:
        return ""
    if spec.startswith("("):
        if not _outer_pair_wraps(spec):
            return None
        spec = spec[1:-1].strip()
    if any(char in spec for char in "()"):
        return None
    return spec


def parse_requirement(text: str, *, strict: bool = False) -> tuple[str, str, str] | None:
    """PEP 508 문자열 → (이름, 범위, URL). URL 의존성은 범위가 빈 문자열."""
    text, separator, marker = text.partition(";")
    if strict and separator and not _valid_requirement_marker(marker):
        return None
    text = text.strip()
    if not text or text.startswith(("-", "#")):
        return None
    match = REQ_RE.match(text)
    if match is None:
        return None
    name, extras, rest = match.groups()
    if strict and extras is not None:
        values = extras[1:-1].split(",")
        if any(not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", value.strip()) for value in values):
            return None
    rest = rest.strip()
    if rest.startswith("@"):
        url = rest[1:].strip()
        if strict and (not url or url.startswith("@")
                       or not url.lower().startswith(("git+", "git:", "github:", "gitlab:",
                                                       "bitbucket:", "https://", "http://", "file:"))):
            return None
        return normalize_name(name), "", url
    spec = _normalize_requirement_spec(rest) if strict else rest.strip("() ")
    if spec is None:
        return None
    if strict and spec and _range_interval(spec) is None:
        return None
    return normalize_name(name), spec, ""


# --------------------------------------------------------------------------- workflow YAML

@dataclass(frozen=True)
class _WorkflowNode:
    """제한된 YAML 값과 원본 행을 함께 보존한다."""

    value: object
    line: int


@dataclass(frozen=True)
class _WorkflowLine:
    indent: int
    content: str
    line: int


_WORKFLOW_SENSITIVE_VALUE_RE = re.compile(
    r"(?ix)(?:"
    r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b|"
    r"\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})\b|"
    r"(?<![\w])(?:[a-z0-9]+_)*(?:api[_-]?key|client[_-]?secret|secret|password|passwd|access[_-]?token|refresh[_-]?token|token)"
    r"\b['\"]?\s*[:=]\s*['\"]?(?!<|\$\{)[A-Za-z0-9+/_.=-]{8,}|"
    r"(?<![\w])(?:[a-z0-9]+_)*(?:api[_-]?key|client[_-]?secret|secret|password|passwd|access[_-]?token|refresh[_-]?token|token)"
    r"\b['\"]?\s*[:=]\s*['\"][^'\"\r\n<\${}]+['\"]|"
    r"(?:secret|password|passwd|token|api[_-]?key|access[_-]?token|refresh[_-]?token)"
    r"[-_A-Za-z0-9]{8,}\b|"
    r"\bpbkdf2_sha256\$[0-9]+\$[^\s$]+\$[A-Za-z0-9+/=]+|"
    r"\b[a-z][a-z0-9+.-]*://[^\s/:@<>]+:[^\s/@<>]+@|"
    r"(?<![\w.])(?:10\.(?:[0-9]{1,3}\.){2}[0-9]{1,3}|192\.168\.[0-9]{1,3}\.[0-9]{1,3}|172\.(?:1[6-9]|2[0-9]|3[01])\.(?:[0-9]{1,3}\.)[0-9]{1,3})(?!\w|\.[0-9])|"
    r"(?<![\w:])(?:f[cd][0-9a-f]{2}|fe[89ab][0-9a-f]):[0-9a-f:]+(?:%[a-z0-9_-]+)?(?![\w:])|"
    r"(?<![\w.-])(?:[a-z0-9][a-z0-9-]*\.)+(?:internal|local|lan|corp)(?![\w-]|\.[\w-])|"
    r"(?<![\w.-])(?:[a-z0-9][a-z0-9-]*\.)+(?:iptime\.org|duckdns\.org|ddns\.net|myddns\.me)(?![\w-]|\.[\w-])|"
    r"(?<![\w.-])(?:prod|production)[.-](?:[a-z0-9][a-z0-9-]*\.)+(?:com|net|org|kr|io|dev)(?![\w-]|\.[\w-])|"
    r"(?<![\w.-])(?:api|web|weather|airport|dagster)[a-z0-9-]*\.(?:[a-z0-9-]+\.){2,}(?:com|net|org|kr|io|dev)(?![\w-]|\.[\w-])|"
    r"-----BEGIN (?:[A-Z0-9]+ )?PRIVATE KEY-----|"
    r"\$\{\{\s*secrets(?:\.|\s|\[)"
    r")"
)


def _workflow_display_value(value: object, fallback: str = "(workflow 값 비공개)") -> str:
    """workflow 원문이 보고서·annotation·요약으로 재게시되지 않게 제한한다."""
    if not isinstance(value, str):
        return ""
    text = value.replace("\r", " ").replace("\n", " ")
    if (len(text) > 256 or any(ord(char) < 0x20 or ord(char) == 0x7F for char in text)
            or any(0xD800 <= ord(char) <= 0xDFFF for char in text)):
        return fallback
    if _WORKFLOW_SENSITIVE_VALUE_RE.search(text):
        return fallback
    return text


def _display_lock_location(label: object, path: object) -> str:
    """lock 내부 경로가 보고 채널에서 민감한 scope를 재조합하지 않게 한다."""
    display_label = _workflow_display_value(label, "(scope 경로 비공개)")
    display_path = _workflow_display_value(path, "(lock 경로 비공개)")
    return f"{display_label} [lock:{display_path}]"


def _path_within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True


def _resolve_input_path(path: Path, message: str) -> Path:
    """입력 경로의 symlink loop·I/O 오류를 원문 없는 입력 오류로 닫는다."""
    try:
        return path.resolve()
    except (OSError, RuntimeError) as exc:
        raise ValueError(message) from exc


def _path_contains_symlink(path: Path) -> bool:
    """경로 중간의 symlink loop도 Windows의 느슨한 resolve 결과와 함께 감지한다."""
    parts = path.parts
    current = Path(path.anchor) if path.anchor else Path()
    if path.anchor:
        parts = parts[1:]
    for part in parts:
        current /= part
        try:
            if current.is_symlink():
                return True
        except (OSError, RuntimeError):
            return True
    return False


def _workflow_input_error() -> ValueError:
    """workflow 파싱 실패를 입력값·경로를 노출하지 않는 일반 오류로 만든다."""
    return ValueError("workflow 입력 구조 오류")


def _yaml_quote_starts(text: str, index: int, *, flow: bool = False) -> bool:
    """plain scalar 내부의 apostrophe·quote를 인용 시작으로 오인하지 않는다."""
    if index == 0 or not text[:index].strip() or text[:index].strip() == "-":
        return True
    if flow:
        delimiter = text.rfind(",", 0, index)
        if delimiter < 0:
            delimiter = -1
        return not text[delimiter + 1:index].strip()
    mapping_colon = -1
    for match in re.finditer(r":(?=\s|$)", text):
        if match.start() >= index:
            break
        mapping_colon = match.start()
        break
    if mapping_colon < 0:
        return False
    value_start = mapping_colon + 1
    while value_start < index and text[value_start].isspace():
        value_start += 1
    if value_start < index and text[value_start] == "[":
        delimiter = text.rfind(",", value_start, index)
        if delimiter >= value_start:
            return not text[delimiter + 1:index].strip()
        return not text[value_start + 1:index].strip()
    return not text[mapping_colon + 1:index].strip()


def _strip_yaml_comment(line: str) -> str:
    """인용 문자열 밖의 공백 뒤 `#`만 주석으로 제거한다."""
    quote = ""
    escaped = False
    for index, char in enumerate(line):
        if quote:
            if escaped:
                escaped = False
            elif quote == '"' and char == "\\":
                escaped = True
            elif quote == "'" and char == "'" and index + 1 < len(line) and line[index + 1] == "'":
                escaped = True
            elif char == quote:
                quote = ""
            continue
        if char in {"'", '"'} and _yaml_quote_starts(line, index):
            quote = char
        elif char == "#" and (index == 0 or line[index - 1].isspace()):
            return line[:index].rstrip()
    if quote:
        raise _workflow_input_error()
    return line.rstrip()


class _WorkflowYamlParser:
    """GitHub workflow에서 필요한 block map/list만 읽는 YAML 부분 파서.

    flow mapping, anchor/alias, block scalar, 태그와 document stream은
    지원하지 않는다. 단순 flow sequence 외 지원하지 않는 문법을 문자열이나 빈 값으로 바꾸지 않고
    입력 오류로 닫아야 정적 보고가 정상 판정을 만들지 않는다.
    """

    def __init__(self, text: str):
        self.lines: list[_WorkflowLine] = []
        for number, raw in enumerate(text.splitlines(), 1):
            if number == 1 and raw.startswith("\ufeff"):
                raw = raw[1:]
            if "\t" in raw or "\x00" in raw:
                raise _workflow_input_error()
            clean = _strip_yaml_comment(raw)
            if not clean.strip():
                continue
            indent = len(clean) - len(clean.lstrip(" "))
            content = clean[indent:]
            if content in {"---", "..."} or content.startswith("%"):
                raise _workflow_input_error()
            self.lines.append(_WorkflowLine(indent, content, number))

    @staticmethod
    def _split_pair(content: str) -> tuple[str, str] | None:
        quote = ""
        escaped = False
        for index, char in enumerate(content):
            if quote:
                if escaped:
                    escaped = False
                elif quote == '"' and char == "\\":
                    escaped = True
                elif quote == "'" and char == "'" and index + 1 < len(content) and content[index + 1] == "'":
                    escaped = True
                elif char == quote:
                    quote = ""
                continue
            if char in {"'", '"'} and _yaml_quote_starts(content, index):
                quote = char
            elif char == ":" and (index + 1 == len(content) or content[index + 1].isspace()):
                key = content[:index].strip()
                if not key:
                    raise _workflow_input_error()
                return key, content[index + 1:].strip()
        if quote:
            raise _workflow_input_error()
        return None

    def _flow_sequence(self, value: str) -> list[object]:
        """단순 scalar만 담은 flow sequence를 읽는다. flow mapping은 거부한다."""
        if not value.endswith("]"):
            raise _workflow_input_error()
        inner = value[1:-1].strip()
        if not inner:
            return []
        parts: list[str] = []
        start = 0
        quote = ""
        escaped = False
        for index, char in enumerate(inner):
            if quote:
                if escaped:
                    escaped = False
                elif quote == '"' and char == "\\":
                    escaped = True
                elif quote == "'" and char == "'" and index + 1 < len(inner) and inner[index + 1] == "'":
                    escaped = True
                elif char == quote:
                    quote = ""
                continue
            if char in {"'", '"'} and _yaml_quote_starts(inner, index, flow=True):
                quote = char
            elif char in "[]{}":
                raise _workflow_input_error()
            elif char == ":" and index + 1 < len(inner) and inner[index + 1].isspace():
                raise _workflow_input_error()
            elif char == ",":
                part = inner[start:index].strip()
                if not part:
                    raise _workflow_input_error()
                parts.append(part)
                start = index + 1
        if quote:
            raise _workflow_input_error()
        part = inner[start:].strip()
        if not part:
            raise _workflow_input_error()
        parts.append(part)
        return [self._scalar(part) for part in parts]

    def _scalar(self, raw: str) -> object:
        value = raw.strip()
        if not value:
            raise _workflow_input_error()
        if value.startswith("["):
            return self._flow_sequence(value)
        if value.startswith(("{", "|", ">", "!")):
            raise _workflow_input_error()
        if value.startswith("${{") and value.endswith("}}"):
            return value
        if value.startswith("'"):
            if len(value) < 2 or not value.endswith("'"):
                raise _workflow_input_error()
            inner = value[1:-1]
            result: list[str] = []
            index = 0
            while index < len(inner):
                if inner[index] != "'":
                    result.append(inner[index])
                    index += 1
                    continue
                if index + 1 >= len(inner) or inner[index + 1] != "'":
                    raise _workflow_input_error()
                result.append("'")
                index += 2
            return "".join(result)
        if value.startswith('"'):
            if len(value) < 2 or not value.endswith('"'):
                raise _workflow_input_error()
            inner = value[1:-1]
            escapes = {
                "0": "\0", "a": "\a", "b": "\b", "t": "\t", "n": "\n",
                "v": "\v", "f": "\f", "r": "\r", "e": "\x1b", " ": " ",
                '"': '"', "/": "/", "\\": "\\", "N": "\u0085", "_": "\u00a0",
                "L": "\u2028", "P": "\u2029",
            }
            result: list[str] = []
            index = 0
            while index < len(inner):
                char = inner[index]
                if char != "\\":
                    if char == '"':
                        raise _workflow_input_error()
                    result.append(char)
                    index += 1
                    continue
                index += 1
                if index >= len(inner):
                    raise _workflow_input_error()
                escape = inner[index]
                if escape in escapes:
                    result.append(escapes[escape])
                    index += 1
                    continue
                width = {"x": 2, "u": 4, "U": 8}.get(escape)
                if width is None or index + width >= len(inner):
                    raise _workflow_input_error()
                digits = inner[index + 1:index + 1 + width]
                if not re.fullmatch(rf"[0-9A-Fa-f]{{{width}}}", digits):
                    raise _workflow_input_error()
                codepoint = int(digits, 16)
                if codepoint > 0x10FFFF or 0xD800 <= codepoint <= 0xDFFF:
                    raise _workflow_input_error()
                try:
                    result.append(chr(codepoint))
                except ValueError as exc:
                    raise _workflow_input_error() from exc
                index += width + 1
            return "".join(result)
        if value.startswith(("@", "`", "&", "*", "%", "#")):
            raise _workflow_input_error()
        if value[:1] in {",", "]", "}"}:
            raise _workflow_input_error()
        if value[:1] in {"?", ":"} and (len(value) == 1 or value[1].isspace()):
            raise _workflow_input_error()
        if re.search(r"(?:^|\s)[&*](?:[A-Za-z0-9_.-]+)?(?:\s|$)", value):
            raise _workflow_input_error()
        if re.search(r":(?:\s|$)", value):
            raise _workflow_input_error()
        lowered = value.lower()
        if lowered in {"null", "~"}:
            return None
        if lowered == "true":
            return True
        if lowered == "false":
            return False
        if re.fullmatch(r"[-+]?\d+", value):
            try:
                return int(value)
            except ValueError as exc:
                raise _workflow_input_error() from exc
        if re.fullmatch(r"[-+]?(?:\d+\.\d*|\.\d+)", value):
            try:
                return float(value)
            except ValueError as exc:
                raise _workflow_input_error() from exc
        return value

    def _key(self, raw: str) -> str:
        key = self._scalar(raw)
        if not isinstance(key, str) or not key:
            raise _workflow_input_error()
        return key

    def _parse_value(self, raw: str, line: _WorkflowLine, index: int,
                     parent_indent: int) -> tuple[_WorkflowNode, int]:
        if raw:
            return _WorkflowNode(self._scalar(raw), line.line), index
        if index < len(self.lines) and self.lines[index].indent > parent_indent:
            if self.lines[index].indent != parent_indent + 2:
                raise _workflow_input_error()
            child, index = self._parse_block(self.lines[index].indent, index)
            return _WorkflowNode(child.value, line.line), index
        return _WorkflowNode(None, line.line), index

    def _parse_map(self, indent: int, index: int) -> tuple[_WorkflowNode, int]:
        values: dict[str, _WorkflowNode] = {}
        first_line = self.lines[index].line
        while index < len(self.lines):
            current = self.lines[index]
            if current.indent < indent:
                break
            if current.indent > indent or current.content == "-" or current.content.startswith("- "):
                break
            pair = self._split_pair(current.content)
            if pair is None:
                raise _workflow_input_error()
            raw_key, raw_value = pair
            key = self._key(raw_key)
            if key in values:
                raise _workflow_input_error()
            node, index = self._parse_value(raw_value, current, index + 1, indent)
            values[key] = node
        if not values:
            raise _workflow_input_error()
        return _WorkflowNode(values, first_line), index

    def _parse_list(self, indent: int, index: int) -> tuple[_WorkflowNode, int]:
        values: list[_WorkflowNode] = []
        first_line = self.lines[index].line
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
                        raise _workflow_input_error()
                    item, index = self._parse_block(self.lines[index].indent, index)
                else:
                    item = _WorkflowNode(None, current.line)
                values.append(item)
                continue
            pair = self._split_pair(rest)
            if pair is None:
                item = _WorkflowNode(self._scalar(rest), current.line)
                if index < len(self.lines) and self.lines[index].indent > indent:
                    raise _workflow_input_error()
                values.append(item)
                continue
            raw_key, raw_value = pair
            key = self._key(raw_key)
            mapping: dict[str, _WorkflowNode] = {}
            # `- key:`의 논리 parent는 list marker보다 두 칸 안쪽이다.
            item, index = self._parse_value(raw_value, current, index, indent + 2)
            mapping[key] = item
            if index < len(self.lines) and self.lines[index].indent > indent:
                continuation_indent = self.lines[index].indent
                if continuation_indent != indent + 2:
                    raise _workflow_input_error()
                continuation, index = self._parse_map(continuation_indent, index)
                if not isinstance(continuation.value, dict):
                    raise _workflow_input_error()
                for continuation_key, continuation_value in continuation.value.items():
                    if continuation_key in mapping:
                        raise _workflow_input_error()
                    mapping[continuation_key] = continuation_value
            values.append(_WorkflowNode(mapping, current.line))
        if not values:
            raise _workflow_input_error()
        return _WorkflowNode(values, first_line), index

    def _parse_block(self, indent: int, index: int) -> tuple[_WorkflowNode, int]:
        if index >= len(self.lines) or self.lines[index].indent != indent:
            raise _workflow_input_error()
        current = self.lines[index]
        if current.content == "-" or current.content.startswith("- "):
            return self._parse_list(indent, index)
        if current.content.startswith("-"):
            raise _workflow_input_error()
        return self._parse_map(indent, index)

    def parse(self) -> _WorkflowNode:
        if not self.lines or self.lines[0].indent != 0:
            raise _workflow_input_error()
        node, index = self._parse_block(0, 0)
        if index != len(self.lines):
            raise _workflow_input_error()
        return node


# --------------------------------------------------------------------------- 탐색

def walk(root: Path):
    root = _resolve_input_path(root, "소비자 입력 오류")
    for current, dirs, files in os.walk(root):
        current_path = Path(current)
        depth = len(current_path.relative_to(root).parts)
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")
                         and depth < MAX_DEPTH)
        yield current_path, files


def nearest_lock(start: Path, root: Path, name: str) -> Path | None:
    current = start
    while True:
        candidate = current / name
        if candidate.is_file():
            return candidate
        if current == root or current.parent == current:
            return None
        current = current.parent


def discover_workflows(root: Path) -> list[Scope]:
    """저장소 루트의 `.github/workflows` 정적 입력만 발견한다."""
    root = _resolve_input_path(root, "workflow 입력 구조 오류")
    directory = root / ".github" / "workflows"
    if not directory.is_dir():
        return []
    try:
        resolved_directory = directory.resolve()
    except (OSError, RuntimeError) as exc:
        raise _workflow_input_error() from exc
    if not _path_within(resolved_directory, root):
        raise _workflow_input_error()
    scopes: list[Scope] = []
    for path in sorted(directory.iterdir(), key=lambda item: item.name):
        if not path.is_file() or path.suffix.lower() not in {".yml", ".yaml"}:
            continue
        label = path.relative_to(root).as_posix()
        scopes.append(Scope("workflow", label, None, path, "workflow"))
    return scopes


def discover(root: Path) -> list[Scope]:
    root = _resolve_input_path(root, "소비자 입력 오류")
    scopes: list[Scope] = []
    for directory, files in walk(root):
        rel = directory.relative_to(root).as_posix() or "."
        if "package.json" in files:
            manifest = directory / "package.json"
            lock = nearest_lock(directory, root, "package-lock.json")
            if lock is None:
                scopes.append(Scope("npm", rel, manifest, None, "none"))
            else:
                workspace = directory.relative_to(lock.parent).as_posix()
                scopes.append(Scope("npm", rel, manifest, lock, "package-lock",
                                    "" if workspace == "." else workspace))
        if "pyproject.toml" in files:
            manifest = directory / "pyproject.toml"
            lock = nearest_lock(directory, root, "uv.lock")
            if lock is not None:
                scopes.append(Scope("python", rel, manifest, lock, "uv"))
            elif (directory / "poetry.lock").is_file():
                scopes.append(Scope("python", rel, manifest, directory / "poetry.lock", "poetry"))
            else:
                scopes.append(Scope("python", rel, manifest, None, "none"))
        for requirement_name in sorted(name for name in files
                                       if re.fullmatch(r"requirements[^/]*\.txt", name)):
            scopes.append(Scope("python", rel, directory / requirement_name, None, "requirements",
                                note=f"{requirement_name}는 선언만 읽는다(T-005b)"))
    scopes.extend(discover_workflows(root))
    return scopes


def _safe_declared_file(candidate: Path, root: Path) -> Path | None:
    """동반 선언 파일의 최종 경로를 소비자 root 안으로 제한한다."""
    resolved = _resolve_input_path(candidate, "매니페스트 동반 선언 파일 입력 구조 오류")
    if not _path_within(resolved, root):
        raise ValueError("매니페스트 동반 선언 파일이 소비자 저장소 루트 밖에 있음")
    if _path_contains_symlink(candidate) and not resolved.is_file():
        raise ValueError("매니페스트 동반 선언 파일 입력 구조 오류")
    return resolved if candidate.is_file() else None


def _manifest_declaration_scopes(root: Path, app: object) -> list[Scope]:
    """빈 lockfiles 매니페스트의 앱 선언을 NO_LOCK scope로 보존한다."""
    if not isinstance(app, str) or not app:
        return []
    candidate = (root / app)
    if not candidate.exists() and not candidate.is_symlink():
        return []
    app_dir = _resolve_input_path(candidate, "매니페스트 app 입력 구조 오류")
    if not _path_within(app_dir, root):
        raise ValueError("매니페스트 app 경로가 소비자 저장소 루트 밖에 있음")
    if _path_contains_symlink(candidate) and not app_dir.is_dir():
        raise ValueError("매니페스트 app 입력 구조 오류")
    if not app_dir.is_dir():
        return []
    label = app_dir.relative_to(root).as_posix() or "."
    display_label = _workflow_display_value(label, "(scope 경로 비공개)")
    scopes: list[Scope] = []
    package_manifest = _safe_declared_file(app_dir / "package.json", root)
    if package_manifest is not None:
        scopes.append(Scope("npm", display_label, package_manifest, None, "none", root=root))
    python_manifest = _safe_declared_file(app_dir / "pyproject.toml", root)
    if python_manifest is not None:
        scopes.append(Scope("python", display_label, python_manifest, None, "none", root=root))
    for path in sorted(app_dir.glob("requirements*.txt"), key=lambda item: item.name):
        requirement = _safe_declared_file(path, root)
        if requirement is not None:
            scopes.append(Scope(
                "python", display_label, requirement, None, "requirements",
                note=f"{path.name}는 선언만 읽는다(T-005b)",
                root=root,
            ))
    return scopes


def scopes_from_manifest(
    manifest_path: Path,
    *,
    root: Path | None = None,
    strict: bool = False,
    registry_path: Path | None = None,
) -> tuple[str | None, list[Scope]]:
    """매니페스트의 lockfiles를 scope로 바꾼다.

    이전 최소 fixture는 `root` 없이 계속 읽을 수 있다. 실제 소비자 호출은
    저장소 루트와 매니페스트를 함께 주어 strict v1·루트 기준 경로를 사용한다.
    """
    declared_manifest_path = manifest_path
    manifest_path = _resolve_input_path(manifest_path, "매니페스트 입력 구조 오류")
    if _path_contains_symlink(declared_manifest_path) and not manifest_path.is_file():
        raise ValueError("매니페스트 입력 구조 오류")
    base = _resolve_input_path(root or manifest_path.parent, "매니페스트 입력 구조 오류")
    if not _path_within(manifest_path, base):
        raise ValueError("매니페스트가 소비자 저장소 루트 밖에 있음")
    if strict:
        errors = validate_manifest_file(manifest_path, registry_path)
        if errors:
            raise ValueError("매니페스트 strict 검증 실패: " + "; ".join(errors[:8]))
    data = read_json(manifest_path)
    if data.get("schema") not in (None, MANIFEST_SCHEMA):
        raise ValueError(f"매니페스트 schema가 {MANIFEST_SCHEMA}가 아님")
    scopes: list[Scope] = []
    for entry in data.get("lockfiles", []):
        kind = entry.get("kind", "")
        raw_path = entry.get("path", "")
        declared_path = base / raw_path
        path = _resolve_input_path(declared_path, "매니페스트 lock path 입력 구조 오류")
        if not _path_within(path, base):
            raise ValueError("매니페스트 lock path가 소비자 저장소 루트 밖에 있음")
        if _path_contains_symlink(declared_path) and not path.is_file():
            raise ValueError("매니페스트 lock path 입력 구조 오류")
        raw_label = entry.get("scope")
        if not isinstance(raw_label, str) or not raw_label:
            raw_label = path.parent.relative_to(base).as_posix() or "."
        workspace = "" if raw_label in {".", "root"} else raw_label
        label = _workflow_display_value(raw_label, "(scope 경로 비공개)")
        if kind == "npm":
            if root is None and not strict:
                # 기존 최소 fixture는 scope를 보고 label로만 사용하고 lock 옆 manifest를 읽는다.
                workspace_root = path.parent
            else:
                workspace_root = (_resolve_input_path(path.parent / workspace,
                                                      "매니페스트 npm workspace 입력 구조 오류")
                                  if workspace else path.parent)
            if not _path_within(workspace_root, base):
                raise ValueError("매니페스트 npm workspace가 소비자 저장소 루트 밖에 있음")
            manifest = _safe_declared_file(workspace_root / "package.json", base)
            scopes.append(Scope("npm", label, manifest,
                                path if path.is_file() else None, "package-lock", workspace=workspace,
                                root=base))
        elif isinstance(kind, str) and kind in {"uv", "poetry"}:
            manifest = _safe_declared_file(path.parent / "pyproject.toml", base)
            scopes.append(Scope("python", label, manifest,
                                path if path.is_file() else None, kind, root=base))
        elif kind == "requirements":
            scopes.append(Scope("python", label, path if path.is_file() else None, None,
                                "requirements", note="requirements.txt는 선언만 읽는다(T-005b)", root=base))
        else:
            scopes.append(Scope("python", label, None, None, "none",
                                note="알 수 없는 lockfile kind", root=base))
    if not data.get("lockfiles"):
        scopes.extend(_manifest_declaration_scopes(base, data.get("app")))
    # manifest가 lockfile 목록을 명시해도 저장소 루트 workflow는 같은 보고에 포함한다.
    scopes.extend(discover_workflows(base))
    return data.get("repo"), scopes


# --------------------------------------------------------------------------- 판정

class Checker:
    def __init__(self, registry: Registry, repo: str, today: date):
        self.registry = registry
        self.repo_id = repo
        self.repo = _workflow_display_value(repo, "(소비자 식별자 비공개)")
        self.today = today
        self.findings: list[Finding] = []
        self.npm_locks: dict[Path, tuple[str, dict]] = {}
        self.npm_direct: set[tuple[Path, str]] = set()
        self.npm_floating: set[tuple[Path, str]] = set()
        self.npm_manifests: set[tuple[Path, str]] = set()
        self.uv_locks_scanned: set[Path] = set()
        self.poetry_locks_scanned: set[Path] = set()

    # --- 공통
    def add(self, scope: str, key: str, ecosystem: str, declared: str, installed: str,
            verdict: str, detail: str = "") -> None:
        self.findings.append(Finding(self.repo, scope, key, ecosystem, declared, installed,
                                     verdict, detail))

    def judge(self, key: str, installed: tuple[int, ...] | None, exact: bool = True) -> tuple[str, str]:
        """축 값과 설치본(또는 선언 하한)을 대조한다. 예외·차단은 호출자가 먼저 처리한다."""
        axis = self.registry.axes[key]
        if installed is None:
            return "NO_LOCK", "설치 버전 파싱 실패 — 정상 설치본으로 판정할 수 없음"
        floor = parse_version(axis.get("floor"))
        maximum = parse_version(axis.get("max"))
        recommended = parse_version(axis.get("recommended"))
        if maximum is not None and at_or_above(installed, maximum):
            return "ABOVE_MAX", f"max {axis['max']}"
        if floor is not None and below(installed, floor):
            return "BELOW_FLOOR", f"floor {axis['floor']}"
        if exact and recommended is not None and not matches_prefix(installed, recommended):
            return "NOT_RECOMMENDED", f"recommended {axis['recommended']}"
        return "OK", ""

    def apply_exception(self, key: str, installed: tuple[int, ...] | None,
                        verdict: str, detail: str) -> tuple[str, str]:
        entry = self.registry.exception(self.repo_id, key, installed)
        if entry is None:
            return verdict, detail
        expired = self.today > date.fromisoformat(entry["until"])
        note = f"예외 until {entry['until']} · {entry['review']} · {entry['reason']}"
        if expired:
            return "EXEMPT_EXPIRED", f"만료(원 판정 {verdict}) · {note}"
        return "EXEMPT", f"원 판정 {verdict} · {note}"

    def record_axis(self, scope: str, key: str, ecosystem: str, declared: str,
                    installed_text: str, exact: bool = True) -> None:
        installed = installed_version(ecosystem, installed_text)
        verdict, detail = self.judge(key, installed, exact)
        verdict, detail = self.apply_exception(key, installed, verdict, detail)
        self.add(scope, key, ecosystem, declared, installed_text, verdict, detail)

    def record_blocked(self, scope: str, ecosystem: str, name: str, version_text: str) -> None:
        if not self.registry.blocked_name(ecosystem, name):
            return
        version = installed_version(ecosystem, version_text)
        if version is None:
            self.add(scope, name, ecosystem, "(차단 대상)", version_text, "NO_LOCK",
                     "차단 대상 설치 버전 미해석 — 범위 대조를 성공으로 표시할 수 없음")
            return
        entry = self.registry.blocked(ecosystem, name, version)
        if entry is not None:
            self.add(scope, name, ecosystem, entry["range"], version_text, "BLOCKED",
                     f"since {entry.get('since', '?')} · {entry['reason']}")

    def record_ref(self, scope: str, ecosystem: str, name: str, spec: str, resolved: str = "") -> None:
        # 선언이 브랜치를 가리키면 lock이 SHA를 기록해도 다음 설치에서 움직인다(D-11).
        declared_pinned = (ref_is_pinned(spec, kind=ecosystem) if spec != "(전이)" else True)
        if spec == "(전이)":
            resolved_pinned = bool(resolved) and ref_is_pinned(resolved, kind="uv")
        else:
            resolved_pinned = (ref_is_pinned(resolved, kind="uv")
                              if ecosystem == "pypi" and resolved else True)
        pinned = declared_pinned and resolved_pinned
        provider = (normalize_name(name) in self.registry.provider_names()
                    or re.fullmatch(r"python-[a-z0-9-]+-api", normalize_name(name)) is not None)
        sha = SHA_RE.search(resolved or spec)
        installed = sha.group(0)[:12] if sha else "-"
        if pinned:
            self.add(scope, name, "git", spec, installed, "OK",
                     "providers 보고만(O-16)" if provider else "git 참조 고정됨")
        else:
            if declared_pinned and not resolved_pinned:
                detail = "선언은 고정됐지만 uv.lock source.git이 전체 SHA로 고정되지 않음"
            else:
                detail = "브랜치·미고정 참조 금지(D-11): SHA 또는 버전 태그로 고정"
            self.add(scope, name, "git", spec, installed, "FLOATING_REF",
                     detail)

    # --- npm
    def record_npm_declarations(self, label: str, declared: dict, packages: dict,
                                directory: str, lock_path: Path | None, *, transitive: bool = False) -> None:
        for name, spec in declared.items():
            path, entry = npm_entry(packages, directory, name)
            if is_vcs_spec(str(spec)):
                self.record_ref(label, "npm", name, str(spec), entry.get("resolved", ""))
                if path and not ref_is_pinned(str(spec)):
                    self.npm_floating.add((lock_path, path))
            elif not transitive and str(spec).strip() in {"*", "latest", ""} and not entry.get("link"):
                self.add(label, name, "npm", str(spec), "", "FLOATING_REF",
                         "`*`/`latest` 선언 금지: 범위 또는 정확 버전으로 선언")

    def check_npm(self, scope: Scope) -> None:
        label = scope.label
        manifest = read_json(scope.manifest) if scope.manifest and scope.manifest.is_file() else {}
        declared = {**manifest.get("dependencies", {}), **manifest.get("devDependencies", {}),
                    **manifest.get("optionalDependencies", {})}
        engines = manifest.get("engines") or {}
        lock: dict = {}
        if scope.lock is not None and scope.lock.is_file():
            if (scope.lock.parent / "npm-shrinkwrap.json").is_file():
                self.add(label, "npm-shrinkwrap.json", "npm", "", "", "NO_LOCK",
                         "npm-shrinkwrap.json이 우선하지만 파서 미지원 — package-lock을 대신 신뢰하지 않음")
            else:
                lock = read_json(scope.lock)
            if lock and lock.get("lockfileVersion") != 3:
                self.add(label, "package-lock.json", "npm", "", str(lock.get("lockfileVersion")),
                         "NO_LOCK", "lockfileVersion 3만 지원")
                lock = {}
        packages = lock.get("packages", {}) if lock else {}
        if not isinstance(packages, dict) or any(not isinstance(entry, dict) for entry in packages.values()):
            raise ValueError("npm lock packages는 경로별 객체여야 함")
        if packages and scope.lock is not None:
            self.npm_locks.setdefault(scope.lock, (label, packages))
            self.npm_manifests.add((scope.lock, scope.workspace))

        root_entry = packages.get("", {})
        own_engines = bool(engines)
        if not engines and root_entry.get("engines"):
            engines = root_entry["engines"]

        # engines.node / engines.npm / packageManager — 워크스페이스 멤버는 자기 선언이 있을 때만
        if own_engines or not scope.workspace:
            node_spec = engines.get("node")
            if node_spec is None:
                self.add(label, "node", "runtime", "", "", "NO_ENGINES",
                         "`engines.node` 미선언(D-06: floor 22.12)")
            else:
                self.record_range("node", label, "runtime", node_spec)
            npm_spec = engines.get("npm")
            manager = manifest.get("packageManager", "")
            if npm_spec is None and manager.startswith("npm@"):
                npm_spec = manager.split("@", 1)[1]
            if npm_spec is not None:
                self.record_range("npm", label, "runtime", npm_spec)

        # 선언된 git/floating 참조(워크스페이스 링크 `*`는 제외)
        self.record_npm_declarations(label, declared, packages, scope.workspace, scope.lock)

        if not packages:
            added = 0
            for name, spec in declared.items():
                key = self.registry.axis_for("npm", name)
                if key is not None:
                    self.add(label, key, "npm", str(spec), "", "NO_LOCK",
                             "package-lock.json(v3) 없음 — 설치본 대조 불가")
                    added += 1
            if not added:
                self.add(label, "package-lock.json", "npm", "", "", "NO_LOCK",
                         "package-lock.json(v3) 없음")
            return

        # 직접 설치본을 먼저 기록하고 전이 설치본은 모든 멤버 처리 뒤 대조한다.
        for name, spec in declared.items():
            key = self.registry.axis_for("npm", name)
            if key is None or not self.registry.axes[key].get("checked", True):
                continue
            path, entry = npm_entry(packages, scope.workspace, name)
            if path:
                self.npm_direct.add((scope.lock, path))
            if str(spec).startswith("npm:") or entry.get("name", name) != name or entry.get("link"):
                self.add(label, key, "npm", str(spec), "", "NO_LOCK",
                         "별칭·로컬 링크는 원 패키지 설치 버전으로 대조하지 않음")
            elif not entry.get("version"):
                self.add(label, key, "npm", str(spec), "", "NO_LOCK",
                         f"lock에 `{name}` 항목 없음(`npm install`로 lock 갱신 필요)")
            else:
                self.record_axis(label, key, "npm", str(spec), entry["version"])

    def check_npm_locks(self) -> None:
        """직접·전이·워크스페이스 중첩 설치본을 lock별 1회 검사한다."""
        for lock_path, (label, packages) in self.npm_locks.items():
            # 전이 선언의 branch가 resolved SHA에 가려지지 않도록 선언을 먼저 본다.
            for path, entry in packages.items():
                if (lock_path, path) in self.npm_manifests:
                    continue
                declared = {**entry.get("dependencies", {}), **entry.get("devDependencies", {}),
                            **entry.get("optionalDependencies", {})}
                self.record_npm_declarations(_display_lock_location(label, path), declared, packages, path, lock_path,
                                             transitive=True)
            for path, entry in packages.items():
                if not re.search(r"(?:^|/)node_modules/", path):
                    continue
                name = entry.get("name") or path.rsplit("node_modules/", 1)[1]
                location = _display_lock_location(label, path)
                if entry.get("link"):
                    target = packages.get(entry.get("resolved", ""), {})
                    names = {name, target.get("name", name)}
                    for linked_name in sorted(names):
                        key = self.registry.axis_for("npm", linked_name)
                        if (lock_path, path) not in self.npm_direct and (key or self.registry.blocked_name("npm", linked_name)):
                            self.add(location, key or linked_name, "npm", "(로컬 링크)", "", "NO_LOCK",
                                     "로컬 링크 설치본 미지원 — 정책 축·차단 대상을 검사에서 제외하지 않음")
                    continue
                version = entry.get("version", "")
                self.record_blocked(location, "npm", name, version)
                resolved = entry.get("resolved", "")
                parsed = urlsplit(resolved)
                # 기본 npm registry의 버전 tarball과 외부 URL 참조를 구분한다.
                registry_tarball = (
                    parsed.scheme == "https" and parsed.hostname == "registry.npmjs.org" and "/-/" in parsed.path
                    and parsed.path.endswith(f"-{version}.tgz")
                )
                if (is_vcs_spec(resolved) and not registry_tarball and not ref_is_pinned(resolved)
                        and (lock_path, path) not in self.npm_floating):
                    self.add(location, name, "git", "(전이)", "", "FLOATING_REF",
                             f"lock resolved가 고정되지 않음: {resolved[:80]}")
                key = self.registry.axis_for("npm", name)
                if ((lock_path, path) not in self.npm_direct and key is not None
                        and self.registry.axes[key].get("checked", True)):
                    self.record_axis(location, key, "npm", "(전이)", version)

    # --- workflow 정적 보고
    @staticmethod
    def _workflow_scope(scope: Scope, line: int) -> str:
        label = _workflow_display_value(scope.label, "(workflow 경로 비공개)")
        return f"{label or 'workflow'}:{line}"

    @staticmethod
    def _workflow_map(node: _WorkflowNode | None) -> dict[str, _WorkflowNode] | None:
        if node is None or not isinstance(node.value, dict):
            return None
        return node.value

    @staticmethod
    def _workflow_list(node: _WorkflowNode | None) -> list[_WorkflowNode] | None:
        if node is None or not isinstance(node.value, list):
            return None
        return node.value

    @staticmethod
    def _workflow_repository_root(scope: Scope) -> Path:
        """workflow의 lexical root를 유지하고 symlink 탈출을 읽기 전에 차단한다."""
        if scope.lock is None:
            raise _workflow_input_error()
        try:
            repository_root = scope.lock.parent.parent.parent.resolve()
        except (OSError, RuntimeError) as exc:
            raise _workflow_input_error() from exc
        try:
            resolved_workflow = scope.lock.resolve()
        except (OSError, RuntimeError) as exc:
            raise _workflow_input_error() from exc
        if not scope.lock.is_file() or not _path_within(resolved_workflow, repository_root):
            raise _workflow_input_error()
        return repository_root

    def _workflow_uses(self, scope: Scope, node: _WorkflowNode) -> tuple[str, str, str, str]:
        """uses 문자열을 ecosystem·설치 표기·판정·설명으로 분류한다."""
        if not isinstance(node.value, str):
            raise _workflow_input_error()
        text = node.value.strip()
        if not text:
            return "github-action", "-", "FLOATING_REF", "참조가 비어 있음"
        repository_root = self._workflow_repository_root(scope)
        if text.startswith("./"):
            try:
                candidate = (repository_root / text).resolve()
            except (OSError, RuntimeError) as exc:
                raise _workflow_input_error() from exc
            try:
                candidate.relative_to(repository_root)
            except ValueError:
                raise _workflow_input_error()
            if candidate.exists():
                return "local", candidate.relative_to(repository_root).as_posix(), "OK", "local action 경로 존재"
            return "local", "-", "NO_LOCK", "local action 경로 없음"
        if text.startswith("docker://"):
            image = text[len("docker://"):]
            if not image or re.search(r"\s", image):
                return "docker", "-", "FLOATING_REF", "Docker image 참조 형식 미지원"
            if image.count("@") > 1:
                return "docker", "-", "FLOATING_REF", "Docker image 참조 형식 미지원"
            if "@" in image:
                name, digest = image.split("@", 1)
                if self._workflow_docker_name(name) and re.fullmatch(r"sha256:[0-9a-f]{64}", digest):
                    return "docker", digest, "OK", "Docker digest로 고정됨"
                return "docker", digest or "-", "FLOATING_REF", "Docker digest가 고정 형식이 아님"
            last = image.rsplit("/", 1)[-1]
            if ":" not in last:
                return "docker", "-", "FLOATING_REF", "Docker image tag가 없음"
            name, tag = image.rsplit(":", 1)
            if (not self._workflow_docker_name(name) or not tag or tag.lower() in FLOATING_NAMES
                    or not WORKFLOW_TAG_RE.fullmatch(tag)):
                return "docker", tag or "-", "FLOATING_REF", "Docker image tag가 버전형이 아님"
            return "docker", tag, "OK", "Docker image 버전형 tag"
        if text.count("@") != 1:
            return "github-action", "-", "FLOATING_REF", "owner/repo@ref 형식이 아니거나 ref가 없음"
        target, ref = text.rsplit("@", 1)
        target_parts = target.split("/")
        if (not re.fullmatch(r"[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)+", target)
                or any(part in {"", ".", ".."} for part in target_parts)
                or not ref.strip() or re.search(r"\s", text)):
            return "github-action", ref or "-", "FLOATING_REF", "action 참조 형식 미지원"
        if re.fullmatch(r"[0-9a-f]{40}", ref):
            return "github-action", ref[:12], "OK", "action commit SHA로 고정됨"
        if WORKFLOW_TAG_RE.fullmatch(ref):
            return "github-action", ref, "OK", "action 버전형 tag로 고정됨"
        return "github-action", ref, "FLOATING_REF", "branch·미고정 action ref 금지"

    @staticmethod
    def _workflow_docker_name(name: str) -> bool:
        """Docker image name의 빈 segment·이동 경로·빈 repository를 거부한다."""
        if not name or name.startswith("/") or name.endswith("/"):
            return False
        parts = name.split("/")
        if any(not part or part in {".", ".."} for part in parts):
            return False
        component = re.compile(r"[a-z0-9]+(?:(?:[._]|__|-+)[a-z0-9]+)*")
        host_label = re.compile(r"[a-z0-9](?:[a-z0-9-]*[a-z0-9])?")
        for index, part in enumerate(parts):
            if ":" in part:
                if index != 0:
                    return False
                host, port = part.rsplit(":", 1)
                if (not host or not port.isdigit()
                        or not all(host_label.fullmatch(label) for label in host.split("."))):
                    return False
            elif index == 0 and len(parts) > 1 and ("." in part or part == "localhost"):
                if not all(host_label.fullmatch(label) for label in part.split(".")):
                    return False
            elif not component.fullmatch(part):
                return False
        return True

    def _check_workflow_uses(self, scope: Scope, node: _WorkflowNode) -> None:
        ecosystem, installed, verdict, detail = self._workflow_uses(scope, node)
        self.add(self._workflow_scope(scope, node.line), "uses", ecosystem,
                 _workflow_display_value(node.value, "(workflow uses 값 비공개)"),
                 _workflow_display_value(installed, "(workflow ref 비공개)"), verdict,
                 _workflow_display_value(detail, "(workflow 진단 비공개)"))

    def _check_setup_node(self, scope: Scope, uses_node: _WorkflowNode,
                          step: dict[str, _WorkflowNode]) -> None:
        with_node = step.get("with")
        if with_node is None:
            self.add(self._workflow_scope(scope, uses_node.line), "node", "runtime", "", "",
                     "NO_ENGINES", "actions/setup-node의 정적 `with.node-version` 없음")
            return
        with_values = self._workflow_map(with_node)
        if with_values is None:
            raise _workflow_input_error()
        node_node = with_values.get("node-version")
        if node_node is None or not isinstance(node_node.value, str):
            line = node_node.line if node_node is not None else uses_node.line
            self.add(self._workflow_scope(scope, line), "node", "runtime", "", "", "NO_ENGINES",
                     "node-version이 정적 문자열이 아님")
            return
        value = node_node.value.strip()
        display_value = _workflow_display_value(value, "(workflow node 값 비공개)")
        if display_value != value:
            self.add(self._workflow_scope(scope, node_node.line), "node", "runtime", display_value, "",
                     "NO_ENGINES", "node-version 값은 안전한 정적 표시를 만들 수 없음")
            return
        if not value or "${{" in value or "}}" in value or "$" in value:
            self.add(self._workflow_scope(scope, node_node.line), "node", "runtime", value, "",
                     "NO_ENGINES", "node-version expression·동적 값은 해석하지 않음")
            return
        self.record_range("node", self._workflow_scope(scope, node_node.line), "runtime", value)

    def check_workflow(self, scope: Scope) -> None:
        """workflow의 uses와 setup-node 정적 선언만 검사한다."""
        self._workflow_repository_root(scope)
        if scope.lock is None:
            raise _workflow_input_error()
        try:
            text = scope.lock.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            raise _workflow_input_error() from exc
        root = _WorkflowYamlParser(text).parse()
        root_map = self._workflow_map(root)
        if root_map is None:
            raise _workflow_input_error()
        jobs_node = root_map.get("jobs")
        jobs = self._workflow_map(jobs_node)
        if jobs is None or not jobs:
            raise _workflow_input_error()
        checked_targets = 0
        for job_node in jobs.values():
            job = self._workflow_map(job_node)
            if job is None:
                raise _workflow_input_error()
            job_uses = job.get("uses")
            if job_uses is not None:
                if "steps" in job:
                    raise _workflow_input_error()
                if "with" in job and self._workflow_map(job.get("with")) is None:
                    raise _workflow_input_error()
                checked_targets += 1
                self._check_workflow_uses(scope, job_uses)
                continue
            steps_node = job.get("steps")
            if steps_node is None:
                raise _workflow_input_error()
            steps = self._workflow_list(steps_node)
            if steps is None or not steps:
                raise _workflow_input_error()
            for step_node in steps:
                step = self._workflow_map(step_node)
                if step is None:
                    raise _workflow_input_error()
                uses_node = step.get("uses")
                if "with" in step and self._workflow_map(step.get("with")) is None:
                    raise _workflow_input_error()
                if uses_node is None:
                    run_node = step.get("run")
                    if (run_node is None or not isinstance(run_node.value, str)
                            or not run_node.value.strip()):
                        raise _workflow_input_error()
                    continue
                if "run" in step:
                    raise _workflow_input_error()
                checked_targets += 1
                self._check_workflow_uses(scope, uses_node)
                if (isinstance(uses_node.value, str)
                        and uses_node.value.strip().split("@", 1)[0] == "actions/setup-node"):
                    self._check_setup_node(scope, uses_node, step)
        if checked_targets == 0:
            raise _workflow_input_error()

    def record_range(self, key: str, scope: str, ecosystem: str, spec: str) -> None:
        bound = lower_bound(spec)
        if bound is None or bound.lower is None:
            self.add(scope, key, ecosystem, spec, "", "NO_ENGINES", "하한 없는 범위(`*`·상한만)")
            return
        installed_text = ".".join(str(part) for part in bound.lower)
        verdict, detail = self.judge(key, bound.lower, exact=bound.exact)
        verdict, detail = self.apply_exception(key, bound.lower, verdict, detail)
        prefix = "exact" if bound.exact else "하한"
        self.add(scope, key, ecosystem, spec, installed_text, verdict,
                 f"{prefix} {installed_text} · {detail}".strip(" ·"))

    def record_requirement(self, scope: str, name: str, spec: str) -> None:
        """requirements 선언을 설치본 후보·범위·차단 정책으로 분리해 기록한다."""
        exact = exact_requirement_version(spec)
        blocked_entries = [entry for entry in self.registry.data.get("blocked", [])
                           if entry["ecosystem"] == "pypi"
                           and package_identity("pypi", entry["name"]) == package_identity("pypi", name)]
        if exact is None:
            for entry in blocked_entries:
                if ranges_overlap(spec, entry["range"]):
                    self.add(scope, name, "pypi", spec, "", "BLOCKED",
                             f"requirements 범위가 차단 범위와 겹침 · {entry['reason']}")
            key = self.registry.axis_for("pypi", name)
            if key is not None and self.registry.axes[key].get("checked", True):
                self.add(scope, key, "pypi", spec, "", "NO_LOCK",
                         "requirements.txt 범위 선언은 설치본 후보일 뿐이라 uv.lock 도입 전 대조 불가")
            return
        installed = installed_version("pypi", exact)
        for entry in blocked_entries:
            if installed is not None and range_contains(installed, entry["range"]):
                self.add(scope, name, "pypi", spec, exact, "BLOCKED",
                         f"since {entry.get('since', '?')} · {entry['reason']}")
        key = self.registry.axis_for("pypi", name)
        if key is not None and self.registry.axes[key].get("checked", True):
            self.record_axis(scope, key, "pypi", spec, exact)

    # --- python
    def check_python(self, scope: Scope) -> None:
        label = scope.label
        declared: dict[str, str] = {}
        urls: dict[str, list[str]] = {}
        requirement_specs: dict[str, list[str]] = {}
        requires_python: str | None = None
        requirements_mode = scope.lock_kind == "requirements"
        poetry_mode = scope.lock_kind == "poetry"
        manifest = scope.manifest
        if manifest is not None and manifest.name == "pyproject.toml":
            try:
                data = read_toml(manifest)
            except (tomllib.TOMLDecodeError, UnicodeError) as exc:
                raise _manifest_input_error() from exc
            project = data.get("project", {})
            requires_python = project.get("requires-python")
            specs = list(project.get("dependencies", []))
            for group in project.get("optional-dependencies", {}).values():
                specs.extend(group)
            dependency_groups = data.get("dependency-groups", {})
            if not isinstance(dependency_groups, dict):
                raise _manifest_input_error()
            normalized_groups: dict[str, list] = {}
            for original_name, group in dependency_groups.items():
                if (not isinstance(original_name, str)
                        or not DEPENDENCY_GROUP_NAME_RE.fullmatch(original_name)
                        or not isinstance(group, list)):
                    raise _manifest_input_error()
                normalized_name = normalize_name(original_name)
                if normalized_name in normalized_groups:
                    raise _manifest_input_error()
                normalized_groups[normalized_name] = group
            expanded_groups: set[str] = set()
            active_groups: set[str] = set()

            def append_group(group_name: str) -> None:
                if not isinstance(group_name, str) or not DEPENDENCY_GROUP_NAME_RE.fullmatch(group_name):
                    raise _manifest_input_error()
                normalized_name = normalize_name(group_name)
                if normalized_name in active_groups or normalized_name not in normalized_groups:
                    raise _manifest_input_error()
                if normalized_name in expanded_groups:
                    return
                active_groups.add(normalized_name)
                try:
                    for item in normalized_groups[normalized_name]:
                        if isinstance(item, str):
                            if parse_requirement(item) is None:
                                raise _manifest_input_error()
                            specs.append(item)
                        elif (isinstance(item, dict) and set(item) == {"include-group"}
                              and isinstance(item.get("include-group"), str)):
                            append_group(item["include-group"])
                        else:
                            raise _manifest_input_error()
                finally:
                    active_groups.remove(normalized_name)
                expanded_groups.add(normalized_name)

            for group_name in normalized_groups:
                append_group(group_name)
            for text in specs:
                parsed = parse_requirement(str(text))
                if parsed is None:
                    continue
                name, spec, url = parsed
                declared.setdefault(name, spec)
                if url:
                    urls.setdefault(name, []).append(url)
            uv_sources = data.get("tool", {}).get("uv", {}).get("sources", {})
            if not isinstance(uv_sources, dict):
                raise _manifest_input_error()
            for name, source_value in uv_sources.items():
                source_entries = source_value if isinstance(source_value, list) else [source_value]
                if not source_entries or any(not isinstance(source, dict) for source in source_entries):
                    raise _manifest_input_error()
                for source in source_entries:
                    if "git" not in source:
                        continue
                    git_url = source.get("git")
                    if not isinstance(git_url, str) or not git_url.strip():
                        raise _manifest_input_error()
                    refs = [field_name for field_name in ("rev", "tag", "branch")
                            if source.get(field_name) is not None]
                    if len(refs) > 1 or any(not isinstance(source[field_name], str)
                                            or not source[field_name].strip() for field_name in refs):
                        raise _manifest_input_error()
                    if not git_url.startswith("git+"):
                        git_url = "git+" + git_url
                    if source.get("branch") is not None and not source.get("rev") and not source.get("tag"):
                        ref = f"branch:{source['branch']}"
                    else:
                        ref = source.get("rev") or source.get("tag") or ""
                    urls.setdefault(normalize_name(name), []).append(
                        f"{git_url}@{ref}" if ref else git_url
                    )
            tool = data.get("tool", {})
            if not isinstance(tool, dict):
                raise _manifest_input_error()
            poetry = tool.get("poetry", {})
            if poetry:
                if not isinstance(poetry, dict):
                    raise _manifest_input_error()
                poetry_dependencies = poetry.get("dependencies", {})
                poetry_groups = poetry.get("group", {})
                if not isinstance(poetry_dependencies, dict) or not isinstance(poetry_groups, dict):
                    raise _manifest_input_error()
                groups = [poetry_dependencies]
                for group in poetry_groups.values():
                    if not isinstance(group, dict) or not isinstance(group.get("dependencies", {}), dict):
                        raise _manifest_input_error()
                    groups.append(group["dependencies"])

                def add_poetry_dependency(name: object, value: object) -> None:
                    if not isinstance(name, str) or not name.strip():
                        raise _manifest_input_error()
                    values = value if isinstance(value, list) else [value]
                    if not values or any(not isinstance(item, (str, dict)) for item in values):
                        raise _manifest_input_error()
                    normalized = normalize_name(name)
                    for item in values:
                        if isinstance(item, str):
                            config = {}
                            spec = item
                        else:
                            config = item
                            spec = config.get("version", "")
                            if not isinstance(spec, str):
                                raise _manifest_input_error()
                        if normalized == "python":
                            if not isinstance(spec, str) or not spec.strip():
                                raise _manifest_input_error()
                            nonlocal_requires[0] = nonlocal_requires[0] or spec
                            continue
                        declared.setdefault(normalized, spec)
                        git_url = config.get("git") if isinstance(config, dict) else None
                        if isinstance(config, dict) and any(field_name in config
                                                           for field_name in ("rev", "tag", "branch")) and git_url is None:
                            raise _manifest_input_error()
                        if git_url is None:
                            continue
                        if not isinstance(git_url, str) or not git_url.strip():
                            raise _manifest_input_error()
                        refs = [field_name for field_name in ("rev", "tag", "branch")
                                if field_name in config and config[field_name] is not None]
                        if len(refs) > 1 or any(not isinstance(config[field_name], str)
                                                or not config[field_name].strip() for field_name in refs):
                            raise _manifest_input_error()
                        normalized_url = git_url if git_url.startswith("git+") else "git+" + git_url
                        if config.get("branch") is not None:
                            ref = f"branch:{config['branch']}"
                        else:
                            ref = config.get("rev") or config.get("tag") or ""
                        urls.setdefault(normalized, []).append(
                            f"{normalized_url}@{ref}" if ref else normalized_url
                        )

                nonlocal_requires = [requires_python]
                for group in groups:
                    for name, value in group.items():
                        add_poetry_dependency(name, value)
                requires_python = nonlocal_requires[0]
        elif manifest is not None and requirements_mode:
            for line in read_requirements(manifest, root=scope.root):
                parsed = parse_requirement(line)
                if parsed is None:
                    raise ValueError("requirements.txt 입력 구조 오류")
                name, spec, url = parsed
                declared.setdefault(name, spec)
                requirement_specs.setdefault(name, []).append(spec)
                if url:
                    urls.setdefault(name, []).append(url)

        if requires_python is None:
            self.add(label, "python", "runtime", "", "", "NO_ENGINES",
                     "`requires-python` 미선언(D-06: floor 3.11)")
        else:
            self.record_range("python", label, "runtime", str(requires_python))

        lock_data: dict = {}
        lock_packages: dict[str, list[dict]] = {}
        if scope.lock is not None and scope.lock.is_file() and scope.lock_kind == "uv":
            lock_data = read_uv_lock(scope.lock)
            for entry in lock_data.get("package", lock_data.get("distribution", [])):
                lock_packages.setdefault(normalize_name(entry.get("name", "")), []).append(entry)

            lock_requires = str(lock_data["requires-python"])
            manifest_bound = lower_bound(str(requires_python)) if requires_python is not None else None
            lock_bound = lower_bound(lock_requires)
            if (requires_python is None
                    or manifest_bound is None or lock_bound is None
                    or manifest_bound.lower != lock_bound.lower
                    or manifest_bound.exact != lock_bound.exact):
                self.record_range("python", f"{label} [uv.lock]", "runtime", lock_requires)
        elif scope.lock is not None and scope.lock.is_file() and poetry_mode:
            lock_data = read_poetry_lock(scope.lock)
            for entry in lock_data["package"]:
                lock_packages.setdefault(normalize_name(entry["name"]), []).append(entry)
            lock_requires = lock_data.get("metadata", {}).get("python-versions")
            if isinstance(lock_requires, str) and lock_requires.strip():
                manifest_bound = lower_bound(str(requires_python)) if requires_python is not None else None
                lock_bound = lower_bound(lock_requires)
                if (requires_python is None or manifest_bound is None or lock_bound is None
                        or manifest_bound.lower != lock_bound.lower
                        or manifest_bound.exact != lock_bound.exact):
                    self.record_range("python", f"{label} [poetry.lock]", "runtime", lock_requires)

        # git/URL 참조
        def lock_git_reference(entry: dict) -> tuple[str, str] | None:
            source = entry.get("source", {})
            if scope.lock_kind == "uv" and isinstance(source, dict) and "git" in source:
                return source["git"], source["git"]
            if scope.lock_kind != "poetry" or not isinstance(source, dict) or source.get("type") != "git":
                return None
            url = source["url"]
            reference = source.get("reference", "")
            resolved = source.get("resolved_reference", "")
            normalized_url = url if url.startswith("git+") else "git+" + url
            declared_ref = reference or (resolved if re.fullmatch(r"[0-9a-f]{40}", resolved) else "")
            declared = f"{normalized_url}@{declared_ref}" if declared_ref else normalized_url
            # Poetry의 resolved_reference는 uv처럼 fragment에 두어 SHA 판정을 재사용한다.
            locked = f"{normalized_url}#{resolved}" if resolved else declared
            return declared, locked

        for name, url_specs in urls.items():
            resolved_refs = [lock_git_reference(entry)[1] for entry in lock_packages.get(name, [])
                             if lock_git_reference(entry) is not None]
            for url in url_specs:
                if resolved_refs:
                    for resolved in resolved_refs:
                        self.record_ref(label, "pypi", name, url, resolved)
                else:
                    self.record_ref(label, "pypi", name, url)
        first_python_lock_scan = False
        if scope.lock is not None and scope.lock_kind in {"uv", "poetry"} and lock_packages:
            # uv workspace는 멤버마다 같은 lock을 가리킬 수 있다. 첫 범위가 멤버여도
            # 공유 lock 전체의 전이 축·차단·git 참조를 한 번 검사한다.
            lock_path = scope.lock.resolve()
            scanned = self.uv_locks_scanned if scope.lock_kind == "uv" else self.poetry_locks_scanned
            first_python_lock_scan = lock_path not in scanned
            if first_python_lock_scan:
                scanned.add(lock_path)
            for name, entries in lock_packages.items():
                if not first_python_lock_scan or name in urls:
                    continue
                for entry in entries:
                    lock_ref = lock_git_reference(entry)
                    if lock_ref is not None:
                        if scope.lock_kind == "uv":
                            self.record_ref(label, "pypi", name, "(전이)", lock_ref[1])
                        else:
                            self.record_ref(label, "pypi", name, lock_ref[0], lock_ref[1])

        if requirements_mode:
            self.add(label, "lockfile", "pypi", "", "", "NO_LOCK",
                     "requirements.txt은 lockfile이 아님 — uv.lock 도입 task(T-005b) 필요")
            for name, specs in requirement_specs.items():
                for spec in specs:
                    self.record_requirement(label, name, spec)
            return
        if not lock_packages:
            missing_lock_note = scope.note or (
                f"{scope.lock_kind}.lock 없음 — uv.lock 도입 task(T-005b) 필요"
                if scope.lock_kind == "poetry" else
                "uv.lock 없음 — 설치본 대조 불가(lockfile 의무 D-07)"
            )
            added = 0
            for name, spec in declared.items():
                key = self.registry.axis_for("pypi", name)
                if key is not None:
                    self.add(label, key, "pypi", spec, "", "NO_LOCK",
                             missing_lock_note)
                    added += 1
            if not added:
                self.add(label, "lockfile", "pypi", "", "", "NO_LOCK", missing_lock_note)
            return
        for name, spec in declared.items():
            key = self.registry.axis_for("pypi", name)
            if key is None or not self.registry.axes[key].get("checked", True):
                continue
            if poetry_mode:
                entries = lock_packages.get(name, [])
            else:
                entries = [e for e in lock_packages.get(name, []) if "registry" in e.get("source", {})]
            if not entries:
                self.add(label, key, "pypi", spec, "", "NO_LOCK",
                         f"{scope.lock_kind}.lock에 `{name}` 항목 없음")
                continue
            for entry in entries:
                self.record_axis(label, key, "pypi", spec, str(entry.get("version", "")))
        # 전이 의존성까지 포함한 축·차단 검사는 공유 lock당 1회만 수행한다.
        if first_python_lock_scan:
            for name, entries in lock_packages.items():
                for entry in entries:
                    version = str(entry.get("version", ""))
                    if not poetry_mode and "registry" not in entry.get("source", {}):
                        continue
                    self.record_blocked(label, "pypi", name, version)
                    key = self.registry.axis_for("pypi", name)
                    if key is not None and name not in declared and self.registry.axes[key].get("checked", True):
                        self.record_axis(label, key, "pypi", "(전이)", version)

    def run(self, scopes: list[Scope]) -> None:
        for scope in scopes:
            if scope.kind == "npm":
                if scope.manifest is None or not scope.manifest.is_file():
                    self.add(scope.label, "package.json", "npm", "", "", "NO_LOCK",
                             "package.json 없음(매니페스트 lockfiles 경로 확인)")
                    continue
                self.check_npm(scope)
            elif scope.kind == "workflow":
                self.check_workflow(scope)
            else:
                if scope.manifest is None or not scope.manifest.is_file():
                    self.add(scope.label, "pyproject.toml", "pypi", "", "", "NO_LOCK",
                             scope.note or "pyproject.toml 없음(매니페스트 lockfiles 경로 확인)")
                    continue
                self.check_python(scope)
        self.check_npm_locks()
        order = {"runtime": 0, "npm": 1, "pypi": 2, "git": 3,
                 "github-action": 4, "local": 5, "docker": 6}
        self.findings.sort(key=lambda f: (f.repo, f.scope, order.get(f.ecosystem, 9), f.key, f.installed))
        # 한 축에 여러 패키지(react/react-dom 등)가 대응하면 같은 판정 행을 하나로 접는다.
        merged: dict[tuple[str, str, str, str, str], Finding] = {}
        for finding in self.findings:
            signature = (finding.scope, finding.key, finding.ecosystem, finding.installed, finding.verdict)
            existing = merged.get(signature)
            if existing is None:
                merged[signature] = finding
            elif finding.declared and finding.declared not in existing.declared.split(" / "):
                existing.declared = f"{existing.declared} / {finding.declared}"
        self.findings = list(merged.values())


# --------------------------------------------------------------------------- 출력

def summarize(findings: list[Finding]) -> dict[str, int]:
    counts = {verdict: 0 for verdict in VERDICTS}
    for finding in findings:
        counts[finding.verdict] = counts.get(finding.verdict, 0) + 1
    return counts


def exit_code(mode: str, findings: list[Finding]) -> int:
    if mode != "fail":
        return 0
    return int(any(finding.verdict in FAILING for finding in findings))


def escape_cell(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ")


def render_markdown(findings: list[Finding], registry: Registry, repo: str, mode: str,
                    mode_source: str, today: date, roots: list[str]) -> str:
    counts = summarize(findings)
    display_roots = [_workflow_display_value(root, "(입력 경로 비공개)") for root in roots]
    display_repo = _workflow_display_value(repo, "(소비자 식별자 비공개)")
    display_registry_name = _workflow_display_value(registry.path.name, "(레지스트리 이름 비공개)")
    display_mode_source = _workflow_display_value(mode_source, "(모드 출처 비공개)")
    lines = [
        f"## check_versions — {display_repo}",
        "",
        f"- 레지스트리: `{display_registry_name}` (baseline {registry.data.get('baseline')}, "
        f"updated {registry.data.get('updated')})",
        f"- 대상: {', '.join('`' + r + '`' for r in display_roots) or '-'}",
        f"- 모드: `{mode}` ({display_mode_source}) · 기준일 {today.isoformat()} · exit {exit_code(mode, findings)}",
        "- 판정 요약: " + " · ".join(f"{verdict} {count}" for verdict, count in counts.items() if count),
        "",
        "| 범위 | 축 | 생태계 | 선언 | 설치·하한 | 판정 | 비고 |",
        "|---|---|---|---|---|---|---|",
    ]
    for finding in findings:
        lines.append("| " + " | ".join(escape_cell(cell) for cell in (
            finding.scope, finding.key, finding.ecosystem, finding.declared or "-",
            finding.installed or "-", finding.verdict, finding.detail or "")) + " |")
    if not findings:
        lines.append("| - | - | - | - | - | - | 대조할 매니페스트를 찾지 못함 |")
    lines.append("")
    lines.append("판정 어휘·모드·승격 규칙은 `docs/standards/versions.md` §3. "
                 "NOT_RECOMMENDED는 어느 모드에서도 실패가 아니다.")
    return "\n".join(lines) + "\n"


def annotations(findings: list[Finding], mode: str) -> list[str]:
    lines: list[str] = []
    for finding in findings:
        where = f"{finding.repo}/{finding.scope} {finding.key}"
        message = f"{finding.verdict}: {where} 선언={finding.declared or '-'} 설치={finding.installed or '-'} {finding.detail}"
        if finding.verdict in HARD:
            lines.append(f"::error title=check_versions::{message}")
        elif finding.verdict in FAILING and mode in {"warn", "fail"}:
            lines.append(f"::{'error' if mode == 'fail' else 'warning'} title=check_versions::{message}")
        elif finding.verdict in SOFT and mode in {"warn", "fail"}:
            lines.append(f"::warning title=check_versions::{message}")
    return lines


def build_report(findings: list[Finding], registry: Registry, repo: str, mode: str,
                 mode_source: str, today: date, roots: list[str]) -> dict:
    return {
        "schema": REPORT_SCHEMA,
        "registry": {"path": _workflow_display_value(registry.path.as_posix(), "(레지스트리 경로 비공개)"),
                     "baseline": registry.data.get("baseline"),
                     "updated": registry.data.get("updated")},
        "repo": _workflow_display_value(repo, "(소비자 식별자 비공개)"),
        "roots": [_workflow_display_value(root, "(입력 경로 비공개)") for root in roots],
        "mode": mode,
        "mode_source": _workflow_display_value(mode_source, "(모드 출처 비공개)"),
        "today": today.isoformat(),
        "summary": summarize(findings),
        "exit_code": exit_code(mode, findings),
        "findings": [asdict(finding) for finding in findings],
    }


# --------------------------------------------------------------------------- CLI

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("paths", nargs="*", type=Path, help="소비 저장소 루트(또는 앱 디렉터리). 생략 시 --manifest 필요")
    parser.add_argument("--manifest", type=Path, help="kor-travel-common.lock.json(consumer-manifest.v1). 위치 인자 root와 함께 주면 strict v1·root workflow를 사용")
    parser.add_argument("--registry", type=Path, default=Path(__file__).resolve().parents[1] / "versions.json")
    parser.add_argument("--repo", help="consumers 키(별칭 허용). 기본: 매니페스트 repo → 디렉터리 이름")
    parser.add_argument("--mode", choices=MODES, help="로컬 override. 생략하면 versions.json consumers.<repo>.enforce")
    parser.add_argument("--today", type=date.fromisoformat, default=None, help="예외 만료 기준일(YYYY-MM-DD)")
    parser.add_argument("--json", type=Path, help="JSON 보고 출력 경로")
    parser.add_argument("--markdown", type=Path, help="Markdown 보고 출력 경로")
    parser.add_argument("--no-step-summary", action="store_true", help="$GITHUB_STEP_SUMMARY에 쓰지 않음")
    parser.add_argument("--quiet", action="store_true", help="표준 출력에 표를 쓰지 않음(annotation·요약만)")
    parser.add_argument("--self-check", action="store_true", help="레지스트리 형식·정책만 검사하고 종료")
    args = parser.parse_args(argv)

    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

    try:
        registry_path = _resolve_input_path(args.registry, "레지스트리 입력 구조 오류")
        registry = Registry.load(registry_path)
    except (OSError, ValueError, TypeError, AttributeError, KeyError) as exc:
        print(f"::error title=check_versions::레지스트리 오류: {exc}")
        return 2
    if args.self_check:
        today = args.today or date.today()
        expired = [entry for entry in registry.data.get("exceptions", [])
                   if today > date.fromisoformat(entry["until"])]
        for entry in expired:
            print(f"::error title=check_versions::EXEMPT_EXPIRED: {entry['repo']} {entry['key']} "
                  f"until {entry['until']} · {entry['review']}")
        if expired:
            return 1
        print("check_versions: 레지스트리 자체 검사 통과(소비자 버전 검사는 실행하지 않음)")
        return 0
    if not args.paths and args.manifest is None:
        parser.error("소비 저장소 경로 또는 --manifest가 필요")

    scopes: list[Scope] = []
    roots: list[str] = []
    manifest_repo: str | None = None
    manifest_path: Path | None = None
    if args.manifest is not None:
        try:
            manifest_path = _resolve_input_path(args.manifest, "매니페스트 입력 구조 오류")
            manifest_root = (_resolve_input_path(args.paths[0], "매니페스트 입력 구조 오류")
                             if args.paths else None)
            manifest_repo, scopes = scopes_from_manifest(
                manifest_path,
                root=manifest_root,
                strict=manifest_root is not None,
                registry_path=registry_path,
            )
        except (OSError, ValueError, TypeError, AttributeError, KeyError) as exc:
            print(f"::error title=check_versions::매니페스트 오류: {exc}")
            return 2
        roots.append((manifest_root or manifest_path.parent).as_posix())
    else:
        manifest_root = None
    first_root: Path | None = manifest_root
    for index, path in enumerate(args.paths):
        try:
            root = _resolve_input_path(path, "소비자 입력 오류")
        except ValueError as exc:
            print(f"::error title=check_versions::소비자 입력 오류: {exc}")
            return 2
        if not root.is_dir():
            print(f"::error title=check_versions::디렉터리 아님: "
                  f"{_workflow_display_value(root.as_posix(), '(입력 경로 비공개)')}")
            return 2
        if first_root is None:
            first_root = root
        if args.manifest is not None and index == 0:
            # 매니페스트 모드에서는 lockfiles[]와 저장소 루트 workflow만 읽는다.
            continue
        roots.append(root.as_posix())
        try:
            scopes.extend(discover(root))
        except (OSError, ValueError, TypeError, AttributeError, KeyError) as exc:
            print(f"::error title=check_versions::소비자 입력 오류: {exc}")
            return 2

    if not scopes:
        print("::error title=check_versions::검사 대상 scope가 없음(경로·lockfiles 확인 필요)")
        return 2

    repo = args.repo or manifest_repo or (
        first_root.name if first_root is not None
        else manifest_path.parent.name if manifest_path is not None
        else ""
    )
    repo = registry.consumer(repo) or repo
    if args.mode:
        mode, mode_source = args.mode, "--mode 로컬 override"
    else:
        mode, mode_source = (registry.enforce(repo),
                             f"versions.json consumers.{_workflow_display_value(repo, '(소비자 식별자 비공개)')}.enforce"
                             if registry.consumer(repo) else "미등록 소비자 기본값")
    today = args.today or date.today()

    checker = Checker(registry, repo, today)
    try:
        checker.run(scopes)
    except (OSError, ValueError, TypeError, AttributeError, KeyError) as exc:
        print(f"::error title=check_versions::소비자 입력 오류: {exc}")
        return 2
    findings = checker.findings
    markdown = render_markdown(findings, registry, repo, mode, mode_source, today, roots)
    report = build_report(findings, registry, repo, mode, mode_source, today, roots)

    if not args.quiet:
        print(markdown)
    for line in annotations(findings, mode):
        print(line)
    if args.json is not None:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if args.markdown is not None:
        args.markdown.parent.mkdir(parents=True, exist_ok=True)
        args.markdown.write_text(markdown, encoding="utf-8")
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_path and not args.no_step_summary:
        with open(summary_path, "a", encoding="utf-8") as handle:
            handle.write(markdown)
    code = exit_code(mode, findings)
    counts = summarize(findings)
    print(f"check_versions: {_workflow_display_value(repo, '(소비자 식별자 비공개)')} mode={mode} findings={len(findings)} "
          f"failing={sum(counts[v] for v in FAILING)} exit={code} (읽기 전용 대조; 제품 gate 아님)")
    return code


if __name__ == "__main__":
    sys.exit(main())
