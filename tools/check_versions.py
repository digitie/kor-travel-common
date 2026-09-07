# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"""소비 저장소의 선언·설치 버전을 루트 `versions.json`과 대조해 판정한다(읽기 전용).

규칙 정본은 docs/standards/versions.md, 값 정본은 versions.json이다. 이 도구는
파일을 쓰지 않고(`--json`·`--markdown`으로 지정한 출력 파일 제외), 네트워크를 쓰지
않으며, 표준 라이브러리만 사용한다(`tomllib`은 Python 3.11+). Windows Python에서도
동작해야 한다.

읽는 파일: package.json / package-lock.json(lockfileVersion 3) / pyproject.toml /
uv.lock / poetry.lock / requirements.txt. Poetry·requirements는 uv 전환 전까지의
과도기 입력이며, requirements 설치본은 정확 핀만 후보로 보고 항상 `NO_LOCK`을 남긴다.

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
import json
import os
from pathlib import Path
import re
import shlex
import sys
import tomllib
from urllib.parse import unquote, urlsplit, urlunsplit


REGISTRY_SCHEMA = "kor-travel-common.version-registry.v1"
REPORT_SCHEMA = "kor-travel-common.version-report.v1"
MANIFEST_SCHEMA = "kor-travel-common.consumer-manifest.v1"

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


POETRY_TOP_FIELDS = frozenset({"package", "metadata"})
POETRY_PACKAGE_FIELDS = frozenset({
    "name", "version", "description", "category", "optional", "python-versions", "groups",
    "files", "dependencies", "extras", "source", "develop", "markers",
})
POETRY_SOURCE_FIELDS = frozenset({"type", "url", "reference", "resolved_reference"})
POETRY_SOURCE_TYPES = frozenset({"git", "url", "legacy", "file", "directory"})


def _poetry_error() -> ValueError:
    """Poetry 입력 원문을 출력하지 않는 일반 오류."""
    return ValueError("poetry.lock 지원 형식 오류")


def _validate_url(value: object, *, require_host: bool) -> str:
    if not isinstance(value, str) or not value.strip() or "\x00" in value:
        raise _poetry_error()
    text = value.strip()
    # Poetry는 git+ 접두를 기록하기도 하고, 일반 git URL을 기록하기도 한다.
    parsed_text = text.removeprefix("git+")
    try:
        parsed = urlsplit(parsed_text)
        hostname = parsed.hostname
        parsed.port
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
    if not isinstance(packages, list) or not isinstance(metadata, dict):
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
        if source_type != "git" and ("reference" in source or "resolved_reference" in source):
            raise _poetry_error()
        if source_type == "git" and "resolved_reference" in source:
            # SHA 이외의 값은 오류가 아니라 부동 참조로 보고한다.
            if not source["resolved_reference"].strip():
                raise _poetry_error()
    return data


def _strip_inline_comment(line: str) -> str:
    """공백 또는 탭 뒤의 주석만 제거한다(URL fragment의 `#`는 보존)."""
    return re.split(r"[ \t]+#", line, maxsplit=1)[0].rstrip()


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
        tokens = shlex.split(line, posix=True)
    except ValueError as exc:
        raise ValueError("requirements.txt 입력 구조 오류") from exc
    kept: list[str] = []
    index = 0
    while index < len(tokens):
        token = tokens[index]
        if token == "--hash":
            index += 1
            if index >= len(tokens) or not re.fullmatch(r"[A-Za-z0-9_-]+:[0-9A-Fa-f]+", tokens[index]):
                raise ValueError("requirements.txt 입력 구조 오류")
        elif token.startswith("--hash="):
            if not re.fullmatch(r"--hash=[A-Za-z0-9_-]+:[0-9A-Fa-f]+", token):
                raise ValueError("requirements.txt 입력 구조 오류")
        elif token.startswith("--"):
            kept.append(token)
        else:
            kept.append(token)
        index += 1
    return " ".join(kept)


REQUIREMENTS_IGNORED_OPTIONS = frozenset({
    "--no-index", "--pre", "--require-hashes", "--use-pep517", "--no-use-pep517",
    "--prefer-binary", "--only-binary", "--no-binary", "--no-cache-dir",
})
REQUIREMENTS_VALUE_OPTIONS = frozenset({
    "--index-url", "--extra-index-url", "--trusted-host", "--find-links",
})


def read_requirements(path: Path, *, _stack: tuple[Path, ...] = ()) -> list[str]:
    """`-r`/`--requirement`를 재귀 확장하고 유효한 선언 행만 돌려준다."""
    path = path.resolve()
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
            include = line[2:].strip()
        elif line == "--requirement" or line.startswith("--requirement=") or line.startswith("--requirement ") or line.startswith("--requirement\t"):
            value = line[len("--requirement"):]
            include = value[1:].strip() if value.startswith("=") else value.strip()
        if include is not None:
            if not include:
                raise ValueError("requirements.txt 입력 구조 오류")
            result.extend(read_requirements(path.parent / include, _stack=stack))
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
            continue
        option_name, separator, option_value = option.partition("=")
        if option_name in REQUIREMENTS_VALUE_OPTIONS:
            if (separator and not option_value) or (not separator and len(tokens) != 2):
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
        exact_seen = False
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
                if exact_seen:
                    return None
                exact_seen = True
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
                if exact_seen and (lower is None or not same_version(lower, version)):
                    return None
                exact_seen = True
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
            parsed = urlsplit(source[kinds[0]])
            hostname = parsed.hostname
            parsed.port
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

    try:
        parsed = urlsplit(text.removeprefix("git+"))
        # hostname/port는 URL이 실제로 해석 가능한지 확인한다. 원문 예외는
        # 입력 값이 로그로 재출력될 수 있으므로 여기서 일반 판정으로 닫는다.
        parsed.hostname
        parsed.port
    except ValueError:
        return False
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


def parse_requirement(text: str, *, strict: bool = False) -> tuple[str, str, str] | None:
    """PEP 508 문자열 → (이름, 범위, URL). URL 의존성은 범위가 빈 문자열."""
    text, separator, marker = text.partition(";")
    if strict and separator and not marker.strip():
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
    spec = rest.strip("() ")
    if strict and spec and _range_interval(spec) is None:
        return None
    return normalize_name(name), spec, ""


# --------------------------------------------------------------------------- 탐색

def walk(root: Path):
    root = root.resolve()
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


def discover(root: Path) -> list[Scope]:
    root = root.resolve()
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
    return scopes


def scopes_from_manifest(manifest_path: Path) -> tuple[str | None, list[Scope]]:
    data = read_json(manifest_path)
    if data.get("schema") not in (None, MANIFEST_SCHEMA):
        raise ValueError(f"{manifest_path}: schema가 {MANIFEST_SCHEMA}가 아님")
    base = manifest_path.parent.resolve()
    scopes: list[Scope] = []
    for entry in data.get("lockfiles", []):
        kind = entry.get("kind", "")
        path = (base / entry.get("path", "")).resolve()
        label = entry.get("scope") or path.parent.relative_to(base).as_posix() or "."
        if kind == "npm":
            manifest = path.parent / "package.json"
            scopes.append(Scope("npm", label, manifest if manifest.is_file() else None,
                                path if path.is_file() else None, "package-lock"))
        elif kind in {"uv", "poetry"}:
            manifest = path.parent / "pyproject.toml"
            scopes.append(Scope("python", label, manifest if manifest.is_file() else None,
                                path if path.is_file() else None, kind))
        elif kind == "requirements":
            scopes.append(Scope("python", label, path if path.is_file() else None, None,
                                "requirements", note="requirements.txt는 선언만 읽는다(T-005b)"))
        else:
            scopes.append(Scope("python", label, None, None, "none",
                                note=f"알 수 없는 lockfile kind {kind!r}"))
    return data.get("repo"), scopes


# --------------------------------------------------------------------------- 판정

class Checker:
    def __init__(self, registry: Registry, repo: str, today: date):
        self.registry = registry
        self.repo = repo
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
        entry = self.registry.exception(self.repo, key, installed)
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
                self.record_npm_declarations(f"{label} [lock:{path}]", declared, packages, path, lock_path,
                                             transitive=True)
            for path, entry in packages.items():
                if not re.search(r"(?:^|/)node_modules/", path):
                    continue
                name = entry.get("name") or path.rsplit("node_modules/", 1)[1]
                location = f"{label} [lock:{path}]"
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
            for line in read_requirements(manifest):
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
            else:
                if scope.manifest is None or not scope.manifest.is_file():
                    self.add(scope.label, "pyproject.toml", "pypi", "", "", "NO_LOCK",
                             scope.note or "pyproject.toml 없음(매니페스트 lockfiles 경로 확인)")
                    continue
                self.check_python(scope)
        self.check_npm_locks()
        order = {"runtime": 0, "npm": 1, "pypi": 2, "git": 3}
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
    lines = [
        f"## check_versions — {repo}",
        "",
        f"- 레지스트리: `{registry.path.name}` (baseline {registry.data.get('baseline')}, "
        f"updated {registry.data.get('updated')})",
        f"- 대상: {', '.join('`' + r + '`' for r in roots) or '-'}",
        f"- 모드: `{mode}` ({mode_source}) · 기준일 {today.isoformat()} · exit {exit_code(mode, findings)}",
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
        "registry": {"path": registry.path.as_posix(), "baseline": registry.data.get("baseline"),
                     "updated": registry.data.get("updated")},
        "repo": repo,
        "roots": roots,
        "mode": mode,
        "mode_source": mode_source,
        "today": today.isoformat(),
        "summary": summarize(findings),
        "exit_code": exit_code(mode, findings),
        "findings": [asdict(finding) for finding in findings],
    }


# --------------------------------------------------------------------------- CLI

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("paths", nargs="*", type=Path, help="소비 저장소 루트(또는 앱 디렉터리). 생략 시 --manifest 필요")
    parser.add_argument("--manifest", type=Path, help="kor-travel-common.lock.json(consumer-manifest.v1). lockfiles[]만 읽는다")
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
        registry = Registry.load(args.registry.resolve())
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
    if args.manifest is not None:
        try:
            manifest_repo, scopes = scopes_from_manifest(args.manifest.resolve())
        except (OSError, ValueError, TypeError, AttributeError, KeyError) as exc:
            print(f"::error title=check_versions::매니페스트 오류: {exc}")
            return 2
        roots.append(args.manifest.resolve().parent.as_posix())
    for path in args.paths:
        root = path.resolve()
        if not root.is_dir():
            print(f"::error title=check_versions::디렉터리 아님: {root}")
            return 2
        roots.append(root.as_posix())
        scopes.extend(discover(root))

    if not scopes:
        print("::error title=check_versions::검사 대상 scope가 없음(경로·lockfiles 확인 필요)")
        return 2

    repo = args.repo or manifest_repo or (args.paths[0].resolve().name if args.paths else args.manifest.resolve().parent.name)
    repo = registry.consumer(repo) or repo
    if args.mode:
        mode, mode_source = args.mode, "--mode 로컬 override"
    else:
        mode, mode_source = registry.enforce(repo), f"versions.json consumers.{repo}.enforce" if registry.consumer(repo) else "미등록 소비자 기본값"
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
    print(f"check_versions: {repo} mode={mode} findings={len(findings)} "
          f"failing={sum(counts[v] for v in FAILING)} exit={code} (읽기 전용 대조; 제품 gate 아님)")
    return code


if __name__ == "__main__":
    sys.exit(main())
