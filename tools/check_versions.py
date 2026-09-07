# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"""소비 저장소의 선언·설치 버전을 루트 `versions.json`과 대조해 판정한다(읽기 전용).

규칙 정본은 docs/standards/versions.md, 값 정본은 versions.json이다. 이 도구는
파일을 쓰지 않고(`--json`·`--markdown`으로 지정한 출력 파일 제외), 네트워크를 쓰지
않으며, 표준 라이브러리만 사용한다(`tomllib`은 Python 3.11+). Windows Python에서도
동작해야 한다.

읽는 파일: package.json / package-lock.json(lockfileVersion 3) / pyproject.toml /
uv.lock / requirements.txt. `poetry.lock` 파서는 T-005b.

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
import sys
import tomllib
from urllib.parse import unquote, urlsplit


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


def ref_is_pinned(text: str, *, kind: str = "npm") -> bool:
    """git/URL 참조가 불변 대상(SHA·버전 태그·릴리스 자산)으로 고정돼 있는지.

    고정으로 보는 것: 40자리 SHA, `/tarball|/archive|/commit/<7~40 hex>`, GitHub Release
    자산(`/releases/download/<tag>/…`, D-11), Python `@<태그>`·npm `#<태그>`의 버전형 태그(`v1.2.3`,
    `py-v0.1.0`). 브랜치 이름(`main`·`master`·`develop`)·참조 없음·`semver:` 범위는 floating.
    """
    def valid_ref(ref: str) -> bool:
        return bool(re.fullmatch(r"[0-9a-f]{40}", ref) or TAG_RE.fullmatch(ref))

    parsed = urlsplit(text.removeprefix("git+"))
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
        return "@" in path and valid_ref(path.rsplit("@", 1)[1])
    # npm git 선언의 revision은 fragment다. URL query나 Python식 @rev를 혼용하지 않는다.
    return bool(fragment and valid_ref(fragment))


def is_vcs_spec(spec: str) -> bool:
    lowered = spec.lower()
    return (lowered.startswith(("git+", "git:", "github:", "gitlab:", "bitbucket:", "https://", "http://"))
            or "github.com/" in lowered or "gitlab.com/" in lowered
            or bool(re.match(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+(#.*)?$", spec)))


def parse_requirement(text: str) -> tuple[str, str, str] | None:
    """PEP 508 문자열 → (이름, 범위, URL). URL 의존성은 범위가 빈 문자열."""
    text = text.split(";")[0].strip()
    if not text or text.startswith(("-", "#")):
        return None
    match = REQ_RE.match(text)
    if match is None:
        return None
    name, _extras, rest = match.groups()
    rest = rest.strip()
    if rest.startswith("@"):
        return normalize_name(name), "", rest[1:].strip()
    return normalize_name(name), rest.strip("() "), ""


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
                scopes.append(Scope("python", rel, manifest, directory / "poetry.lock", "poetry",
                                    note="poetry.lock 파서 미지원(T-005b)"))
            else:
                scopes.append(Scope("python", rel, manifest, None, "none"))
        elif "requirements.txt" in files:
            scopes.append(Scope("python", rel, directory / "requirements.txt", None, "requirements",
                                note="requirements.txt는 선언만 읽는다(T-005b)"))
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
                                path if path.is_file() else None, kind,
                                note="poetry.lock 파서 미지원(T-005b)" if kind == "poetry" else ""))
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
        pinned = (ref_is_pinned(resolved, kind="uv" if ecosystem == "pypi" else "npm")
                  if spec == "(전이)" else ref_is_pinned(spec, kind=ecosystem))
        provider = (normalize_name(name) in self.registry.provider_names()
                    or re.fullmatch(r"python-[a-z0-9-]+-api", normalize_name(name)) is not None)
        sha = SHA_RE.search(resolved or spec)
        installed = sha.group(0)[:12] if sha else "-"
        if pinned:
            self.add(scope, name, "git", spec, installed, "OK",
                     "providers 보고만(O-16)" if provider else "git 참조 고정됨")
        else:
            self.add(scope, name, "git", spec, installed, "FLOATING_REF",
                     "브랜치·미고정 참조 금지(D-11): SHA 또는 버전 태그로 고정")

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

    # --- python
    def check_python(self, scope: Scope) -> None:
        label = scope.label
        declared: dict[str, str] = {}
        urls: dict[str, str] = {}
        requires_python: str | None = None
        manifest = scope.manifest
        if manifest is not None and manifest.name == "pyproject.toml":
            data = read_toml(manifest)
            project = data.get("project", {})
            requires_python = project.get("requires-python")
            specs = list(project.get("dependencies", []))
            for group in project.get("optional-dependencies", {}).values():
                specs.extend(group)
            for text in specs:
                parsed = parse_requirement(str(text))
                if parsed is None:
                    continue
                name, spec, url = parsed
                declared.setdefault(name, spec)
                if url:
                    urls[name] = url
            for name, source in data.get("tool", {}).get("uv", {}).get("sources", {}).items():
                if isinstance(source, dict) and "git" in source:
                    ref = source.get("rev") or source.get("tag") or source.get("branch") or ""
                    urls[normalize_name(name)] = f"{source['git']}@{ref}" if ref else source["git"]
            poetry = data.get("tool", {}).get("poetry", {})
            if poetry:
                requires_python = requires_python or poetry.get("dependencies", {}).get("python")
                groups = [poetry.get("dependencies", {})]
                groups.extend(g.get("dependencies", {}) for g in poetry.get("group", {}).values())
                for group in groups:
                    for name, value in group.items():
                        if normalize_name(name) == "python":
                            continue
                        spec = value.get("version", "") if isinstance(value, dict) else str(value)
                        declared.setdefault(normalize_name(name), spec)
                        if isinstance(value, dict) and value.get("git"):
                            ref = value.get("rev") or value.get("tag") or value.get("branch") or ""
                            urls[normalize_name(name)] = f"{value['git']}@{ref}" if ref else value["git"]
        elif manifest is not None and manifest.name == "requirements.txt":
            for line in manifest.read_text(encoding="utf-8-sig").splitlines():
                line = line.split(" #")[0].strip()
                parsed = parse_requirement(line)
                if parsed is None:
                    continue
                name, spec, url = parsed
                declared.setdefault(name, spec)
                if url:
                    urls[name] = url

        if requires_python is None:
            self.add(label, "python", "runtime", "", "", "NO_ENGINES",
                     "`requires-python` 미선언(D-06: floor 3.11)")
        else:
            self.record_range("python", label, "runtime", str(requires_python))

        lock_packages: dict[str, list[dict]] = {}
        if scope.lock is not None and scope.lock.is_file() and scope.lock_kind == "uv":
            data = read_toml(scope.lock)
            for entry in data.get("package", []):
                lock_packages.setdefault(normalize_name(entry.get("name", "")), []).append(entry)

        # git/URL 참조
        for name, url in urls.items():
            resolved = ""
            for entry in lock_packages.get(name, []):
                source = entry.get("source", {})
                if "git" in source:
                    resolved = source["git"]
            self.record_ref(label, "pypi", name, url, resolved)
        if scope.lock is not None and manifest is not None and scope.lock.parent == manifest.parent:
            for name, entries in lock_packages.items():
                if name in urls:
                    continue
                for entry in entries:
                    source = entry.get("source", {})
                    if "git" in source:
                        self.record_ref(label, "pypi", name, "(전이)", source["git"])

        if not lock_packages:
            added = 0
            for name, spec in declared.items():
                key = self.registry.axis_for("pypi", name)
                if key is not None:
                    self.add(label, key, "pypi", spec, "", "NO_LOCK",
                             scope.note or "uv.lock 없음 — 설치본 대조 불가(lockfile 의무 D-07)")
                    added += 1
            if not added:
                self.add(label, "lockfile", "pypi", "", "", "NO_LOCK", scope.note or "uv.lock 없음")
            return
        owns_lock = scope.lock is not None and manifest is not None and scope.lock.parent == manifest.parent

        for name, spec in declared.items():
            key = self.registry.axis_for("pypi", name)
            if key is None or not self.registry.axes[key].get("checked", True):
                continue
            entries = [e for e in lock_packages.get(name, []) if "registry" in e.get("source", {})]
            if not entries:
                self.add(label, key, "pypi", spec, "", "NO_LOCK",
                         f"uv.lock에 `{name}` registry 항목 없음")
                continue
            for entry in entries:
                self.record_axis(label, key, "pypi", spec, str(entry.get("version", "")))
        # 전이 의존성까지 포함한 축·차단 검사는 lock을 소유한 범위에서 1회만(선언에 없는 축은 전이로 표시)
        if not owns_lock:
            return
        for name, entries in lock_packages.items():
            for entry in entries:
                version = str(entry.get("version", ""))
                if "registry" not in entry.get("source", {}):
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
