# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"""tools/check_versions.py 회귀 시험: 판정 어휘·모드·예외 만료·lockfile 파서·읽기 전용 동작."""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "tools/check_versions.py"
SPEC = importlib.util.spec_from_file_location("kor_travel_common_check_versions", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
CV = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = CV
SPEC.loader.exec_module(CV)

REGISTRY = {
    "schema": CV.REGISTRY_SCHEMA,
    "baseline": "2026-09",
    "updated": "2026-09-06",
    "axes": {
        "node": {"ecosystem": "runtime", "floor": "22.12", "recommended": "22.23"},
        "npm": {"ecosystem": "runtime", "floor": "10.9", "recommended": "11.19"},
        "python": {"ecosystem": "runtime", "floor": "3.11", "recommended": None},
        "next": {"ecosystem": "npm", "floor": "16.2", "recommended": "16.3.4"},
        "react": {"ecosystem": "npm", "packages": ["react", "react-dom"], "floor": "19.0",
                  "recommended": "19.2.8"},
        "typescript": {"ecosystem": "npm", "floor": "5.9", "recommended": "5.9.3", "max": "6.1"},
        "fastapi": {"ecosystem": "pypi", "floor": "0.115", "recommended": "0.141"},
        "starlette": {"ecosystem": "pypi", "floor": None, "recommended": "1.6"},
        "postgresql": {"ecosystem": "db", "floor": None, "recommended": None, "checked": False},
    },
    "exceptions": [
        {"repo": "app-a", "key": "typescript", "installed": "7.0", "reason": "TS 7 실검증",
         "until": "2026-12-31", "review": "T-433"},
    ],
    "blocked": [
        {"ecosystem": "pypi", "name": "mcp", "range": ">=2", "reason": "FastMCP API 변경",
         "since": "2026-09-04"},
    ],
    "consumers": {
        "app-a": {"enforce": "report", "aliases": ["a"]},
        "app-fail": {"enforce": "fail"},
    },
    "providers": {"packages": {"python-kasi-api": {"repo": "https://github.com/digitie/python-kasi-api"}}},
}


def npm_fixture(root: Path, *, deps: dict, engines: dict | None, installed: dict | None,
                lock_version: int = 3, extra_packages: dict | None = None) -> None:
    manifest = {"name": "fixture", "version": "0.0.0", "dependencies": deps}
    if engines is not None:
        manifest["engines"] = engines
    (root / "package.json").write_text(json.dumps(manifest), encoding="utf-8")
    if installed is None:
        return
    packages = {"": {"name": "fixture", "version": "0.0.0", "dependencies": deps}}
    if engines is not None:
        packages[""]["engines"] = engines
    for name, version in installed.items():
        packages[f"node_modules/{name}"] = {"version": version,
                                            "resolved": f"https://registry.npmjs.org/{name}/-/{name}-{version}.tgz"}
    packages.update(extra_packages or {})
    (root / "package-lock.json").write_text(
        json.dumps({"name": "fixture", "lockfileVersion": lock_version, "packages": packages}),
        encoding="utf-8")


def python_fixture(root: Path, *, requires: str | None, deps: list[str], locked: dict | None,
                   git_locked: dict | None = None, lock_requires: str | None = None) -> None:
    lines = ["[project]", 'name = "fixture"', 'version = "0.0.0"']
    if requires is not None:
        lines.append(f'requires-python = "{requires}"')
    lines.append("dependencies = [")
    lines.extend(f'  "{dep}",' for dep in deps)
    lines.append("]")
    (root / "pyproject.toml").write_text("\n".join(lines) + "\n", encoding="utf-8")
    if locked is None:
        return
    blocks = ['version = 1', 'revision = 3']
    if lock_requires is None:
        lock_requires = requires
    if lock_requires is not None:
        blocks.append(f'requires-python = "{lock_requires}"')
    blocks.append('\n[[package]]\nname = "fixture"\nversion = "0.0.0"\nsource = { editable = "." }')
    for name, version in locked.items():
        blocks.append(f'\n[[package]]\nname = "{name}"\nversion = "{version}"\n'
                      'source = { registry = "https://pypi.org/simple" }')
    for name, (version, url) in (git_locked or {}).items():
        blocks.append(f'\n[[package]]\nname = "{name}"\nversion = "{version}"\nsource = {{ git = "{url}" }}')
    (root / "uv.lock").write_text("\n".join(blocks) + "\n", encoding="utf-8")


def snapshot(root: Path) -> dict[str, str]:
    return {path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in sorted(root.rglob("*")) if path.is_file()}


class CheckVersionsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="kor-travel-common-versions-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.registry_path = self.root / "versions.json"
        self.registry_path.write_text(json.dumps(REGISTRY, ensure_ascii=False), encoding="utf-8")
        self.repo = self.root / "app-a"
        self.repo.mkdir()

    def run_checker(self, repo: str = "app-a", root: Path | None = None, today: str = "2026-09-06",
                    manifest: Path | None = None) -> list:
        registry = CV.Registry.load(self.registry_path)
        scopes = []
        if manifest is not None:
            _, scopes = CV.scopes_from_manifest(manifest)
        else:
            scopes = CV.discover(root or self.repo)
        checker = CV.Checker(registry, repo, CV.date.fromisoformat(today))
        checker.run(scopes)
        return checker.findings

    def verdicts(self, findings, key: str) -> list[str]:
        return [f.verdict for f in findings if f.key == key]

    def cli(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run([sys.executable, "-B", "-X", "utf8", str(SCRIPT), "--registry",
                               str(self.registry_path), "--today", "2026-09-06", *args],
                              capture_output=True, text=True, encoding="utf-8")

    # --- 버전 파싱·범위 도우미
    def test_blocked_only_unknown_versions_fail_closed(self):
        data = json.loads(json.dumps(REGISTRY))
        data["blocked"].append({"ecosystem": "npm", "name": "mcp", "range": ">=2", "reason": "시험"})
        self.registry_path.write_text(json.dumps(data), encoding="utf-8")
        for ecosystem in ("npm", "pypi"):
            for version, expected in (("2.1.1", "BLOCKED"), ("1.9.0", None),
                                      ("2.1.1-rc.1", "NO_LOCK"), ("broken", "NO_LOCK"), ("", "NO_LOCK")):
                with self.subTest(ecosystem=ecosystem, version=version):
                    root = self.root / (ecosystem + version)
                    root.mkdir()
                    if ecosystem == "npm":
                        npm_fixture(root, deps={"mcp": ">=1"}, engines={"node": ">=22.12"}, installed={"mcp": version})
                    else:
                        python_fixture(root, requires=">=3.12", deps=["mcp>=1"], locked={"mcp": version})
                    findings = self.run_checker(root=root, repo="app-fail")
                    self.assertEqual(self.verdicts(findings, "mcp"), [expected] if expected else [])
                    self.assertEqual(self.cli(str(root), "--repo", "app-fail").returncode, int(expected is not None))

    def test_blocked_range_parser_matches_self_check(self):
        for value, code in ((">=2.1.1.0.0", 2), (">=2.1.1.0", 0)):
            data = json.loads(json.dumps(REGISTRY)); data["blocked"][0]["range"] = value
            self.registry_path.write_text(json.dumps(data), encoding="utf-8")
            self.assertEqual(self.cli("--self-check").returncode, code)
            if code == 0:
                registry = CV.Registry.load(self.registry_path)
                self.assertIsNotNone(registry.blocked("pypi", "mcp", (2, 1, 1)))

    def test_exception_requires_nonblank_evidence(self):
        for name in ("reason", "review"):
            data = json.loads(json.dumps(REGISTRY)); data["exceptions"][0][name] = " \t "
            self.registry_path.write_text(json.dumps(data), encoding="utf-8")
            self.assertEqual(self.cli("--self-check").returncode, 2)

    def test_npm_name_identity_is_not_pypi_identity(self):
        data = json.loads(json.dumps(REGISTRY))
        data["blocked"].append({"ecosystem": "npm", "name": "bad-name", "range": ">=1", "reason": "시험"})
        self.registry_path.write_text(json.dumps(data), encoding="utf-8")
        npm_fixture(self.repo, deps={}, engines={"node": ">=22.12"},
                    installed={"react.dom": "1.0.0", "react_dom": "1.0.0", "bad.name": "1.0.0"})
        findings = self.run_checker()
        self.assertEqual(self.verdicts(findings, "react"), [])
        self.assertEqual(self.verdicts(findings, "bad.name"), [])
        registry = CV.Registry.load(self.registry_path)
        self.assertEqual(registry.axis_for("pypi", "FastAPI"), "fastapi")

    def test_npm_transitive_links_in_manifest_are_unknown(self):
        data = json.loads(json.dumps(REGISTRY))
        data["blocked"].append({"ecosystem": "npm", "name": "bad", "range": ">=2", "reason": "시험"})
        self.registry_path.write_text(json.dumps(data), encoding="utf-8")
        npm_fixture(self.repo, deps={}, engines={"node": ">=22.12"}, installed={}, extra_packages={
            "node_modules/react": {"resolved": "packages/react", "link": True},
            "packages/react": {"name": "react", "version": "18.3.1"},
            "node_modules/bad": {"resolved": "packages/bad", "link": True},
        })
        manifest = self.repo / "kor-travel-common.lock.json"
        manifest.write_text(json.dumps({"schema": CV.MANIFEST_SCHEMA, "repo": "app-fail",
                                       "lockfiles": [{"kind": "npm", "path": "package-lock.json"}]}), encoding="utf-8")
        findings = self.run_checker(manifest=manifest)
        self.assertEqual(self.verdicts(findings, "react"), ["NO_LOCK"])
        self.assertEqual(self.verdicts(findings, "bad"), ["NO_LOCK"])
        self.assertEqual(self.cli("--manifest", str(manifest)).returncode, 1)

    def test_manifest_parent_alias_uses_resolved_scope(self):
        npm_fixture(self.repo, deps={"react": "19.0.0"}, engines={"node": ">=22.12"},
                    installed={"react": "19.0.0"})
        manifest = self.repo / "kor-travel-common.lock.json"
        manifest.write_text(json.dumps({"schema": CV.MANIFEST_SCHEMA, "repo": "app-a",
                                       "lockfiles": [{"kind": "npm", "path": "package-lock.json"}]}),
                            encoding="utf-8")
        alias = self.repo / ".." / self.repo.name / manifest.name
        self.assertEqual(CV.scopes_from_manifest(alias), CV.scopes_from_manifest(manifest.resolve()))

    def test_npm_transitive_declarations_and_urls(self):
        cases = [
            ("git+https://github.com/example/custom#main", "git+https://github.com/example/custom#" + "a" * 40, "FLOATING_REF"),
            ("https://github.com/example/custom/archive/refs/heads/main.tar.gz", "https://github.com/example/custom/archive/refs/heads/main.tar.gz", "FLOATING_REF"),
            ("1.0.0", "https://github.com/example/custom/archive/refs/heads/main.tar.gz", "FLOATING_REF"),
            ("1.0.0", "https://registry.npmjs.org/custom/-/custom-1.0.0.tgz", None),
            ("*", "https://registry.npmjs.org/custom/-/custom-1.0.0.tgz", None),
            ("git+https://github.com/example/custom#v1.0.0", "git+https://github.com/example/custom#" + "a" * 40, "OK"),
        ]
        for spec, resolved, expected in cases:
            with self.subTest(spec=spec, resolved=resolved):
                npm_fixture(self.repo, deps={}, engines={"node": ">=22.12"}, installed={}, extra_packages={
                    "node_modules/wrapper": {"version": "1.0.0", "dependencies": {"custom": spec}},
                    "node_modules/custom": {"version": "1.0.0", "resolved": resolved},
                })
                findings = self.run_checker()
                self.assertEqual(self.verdicts(findings, "custom"), [expected] if expected else [])

    def test_runtime_unsupported_and_empty_intersection(self):
        for spec in ("^22.12 <20", ">=22.12 <20", ">22.11", "22.11 >=22.12", ">=22.12-slim"):
            with self.subTest(spec=spec):
                npm_fixture(self.repo, deps={}, engines={"node": spec}, installed={})
                self.assertEqual(self.verdicts(self.run_checker(), "node"), ["NO_ENGINES"])
        npm_fixture(self.repo, deps={}, engines={"node": ">=22.12 <23"}, installed={})
        self.assertEqual(self.verdicts(self.run_checker(), "node"), ["OK"])

    def test_npm_build_metadata_keeps_stable_numeric_version(self):
        for version in ("19.2.8+build--", "19.2.8+001.build-x", "19.2.8+build.1"):
            npm_fixture(self.repo, deps={"react": version}, engines={"node": ">=22.12"}, installed={"react": version})
            self.assertEqual(self.verdicts(self.run_checker(), "react"), ["OK"])

    def test_registry_nested_fields_and_order_are_strict(self):
        mutations = [
            ("providers", {"polciy": "report"}),
            ("providers", {"policy": "fail"}),
            ("providers", {"packages": {"x": {"repo": "https://example.com/x", "pin": "main"}}}),
            ("actions", {"cheked": False}),
            ("actions", {"checked": True}),
            ("actions", {"common": {"actions/checkout": "main"}}),
            ("semantics", {"florr": "잘못된 필드"}),
            ("updated", "2026-02-30"),
            ("baseline", "2026-13"),
        ]
        for key, value in mutations:
            with self.subTest(key=key, value=value):
                data = json.loads(json.dumps(REGISTRY))
                data[key] = value
                self.registry_path.write_text(json.dumps(data), encoding="utf-8")
                self.assertEqual(self.cli("--self-check").returncode, 2)
        for values in ({"floor": "8", "max": "6.1"}, {"recommended": "6.1"},
                       {"recommended": "5.8"}, {"floor": "5.9-rc.1"}, {"check": False}):
            with self.subTest(values=values):
                data = json.loads(json.dumps(REGISTRY))
                data["axes"]["typescript"].update(values)
                self.registry_path.write_text(json.dumps(data), encoding="utf-8")
                self.assertEqual(self.cli("--self-check").returncode, 2)

    def test_overlapping_exception_prefixes_are_rejected(self):
        data = json.loads(json.dumps(REGISTRY))
        data["exceptions"].append({**data["exceptions"][0], "installed": "7", "until": "2027-01-31"})
        self.registry_path.write_text(json.dumps(data), encoding="utf-8")
        self.assertEqual(self.cli("--self-check").returncode, 2)

    def test_self_check_expiry_is_not_report_success(self):
        self.assertEqual(self.cli("--self-check", "--today", "2026-12-31").returncode, 0)
        result = self.cli("--self-check", "--today", "2027-01-01", "--mode", "report")
        self.assertEqual(result.returncode, 1)
        self.assertIn("EXEMPT_EXPIRED", result.stdout)

    def test_npm_prerelease_and_alias_are_not_stable(self):
        for version in ("19.2.8-rc.1", "19.2.8-slim", "19.2", "v19.2.8"):
            with self.subTest(version=version):
                npm_fixture(self.repo, deps={"react": "^19.2.8"}, engines={"node": ">=22.12"},
                            installed={"react": version})
                self.assertEqual(self.verdicts(self.run_checker(), "react"), ["NO_LOCK"])
        npm_fixture(self.repo, deps={"react": "npm:other@19.2.8"}, engines={"node": ">=22.12"},
                    installed={"react": "19.2.8"})
        self.assertEqual(self.verdicts(self.run_checker(), "react"), ["NO_LOCK"])
        npm_fixture(self.repo, deps={"react": "19.2.8+build.1"}, engines={"node": ">=22.12"},
                    installed={"react": "19.2.8+build.1"})
        self.assertEqual(self.verdicts(self.run_checker(), "react"), ["OK"])

    def test_npm_transitive_nested_versions_and_blocked(self):
        data = json.loads(json.dumps(REGISTRY))
        data["blocked"].append({"ecosystem": "npm", "name": "bad", "range": ">=2", "reason": "시험"})
        self.registry_path.write_text(json.dumps(data), encoding="utf-8")
        npm_fixture(self.repo, deps={"react": "19.2.8"}, engines={"node": ">=22.12"},
                    installed={"react": "19.2.8"}, extra_packages={
                        "node_modules/other/node_modules/react": {"version": "18.3.1"},
                        "apps/web/node_modules/bad": {"version": "2.0.0"},
                        "apps/web/node_modules/custom": {"version": "1.0.0", "resolved": "git+https://github.com/example/custom#main"},
                    })
        findings = self.run_checker()
        self.assertEqual(sorted(self.verdicts(findings, "react")), ["BELOW_FLOOR", "OK"])
        self.assertEqual(self.verdicts(findings, "bad"), ["BLOCKED"])
        self.assertEqual(self.verdicts(findings, "custom"), ["FLOATING_REF"])

    def test_npm_optional_and_workspace_ancestor_hoisting(self):
        npm_fixture(self.repo, deps={}, engines={"node": ">=22.12"}, installed={"react": "19.2.8"},
                    extra_packages={"apps/node_modules/react": {"version": "18.3.1"}})
        member = self.repo / "apps/web"
        member.mkdir(parents=True)
        (member / "package.json").write_text(json.dumps({"optionalDependencies": {"react": "18.3.1"}}), encoding="utf-8")
        findings = self.run_checker()
        member_rows = [f for f in findings if f.scope == "apps/web" and f.key == "react"]
        self.assertEqual([f.verdict for f in member_rows], ["BELOW_FLOOR"])
        self.assertEqual(len([f for f in findings if f.installed == "18.3.1"]), 1)

    def test_shrinkwrap_precedence_does_not_use_stale_package_lock(self):
        npm_fixture(self.repo, deps={"react": "19.2.8"}, engines={"node": ">=22.12"},
                    installed={"react": "19.2.8"})
        (self.repo / "npm-shrinkwrap.json").write_text("{}", encoding="utf-8")
        self.assertEqual(self.verdicts(self.run_checker(), "react"), ["NO_LOCK"])

    def test_invalid_installed_versions_are_not_success(self):
        for version in ("banana", "19.2.8garbage", ""):
            with self.subTest(version=version):
                npm_fixture(self.repo, deps={"react": "^19.2.8"}, engines={"node": ">=22.12"},
                            installed={"react": version})
                self.assertIn("NO_LOCK", self.verdicts(self.run_checker(), "react"))
                self.assertEqual(self.cli(str(self.repo), "--repo", "app-fail").returncode, 1)

    def test_empty_scope_is_an_input_error(self):
        self.assertEqual(self.cli(str(self.repo), "--repo", "app-fail").returncode, 2)
        manifest = self.root / "manifest.json"
        for fields in ({}, {"lockfiles": []}):
            manifest.write_text(json.dumps({"schema": CV.MANIFEST_SCHEMA, "repo": "app-fail", **fields}),
                                encoding="utf-8")
            self.assertEqual(self.cli("--manifest", str(manifest)).returncode, 2)

    def test_compound_runtime_bounds(self):
        for spec in ("<22 || >=22.12", ">=22.12 || *", ">=22.12 || invalid"):
            with self.subTest(spec=spec):
                npm_fixture(self.repo, deps={}, engines={"node": spec}, installed={})
                self.assertIn("NO_ENGINES", self.verdicts(self.run_checker(), "node"))
        self.assertEqual(CV.lower_bound(">=20,>=22.12").lower, (22, 12))
        self.assertEqual(CV.lower_bound(">= 22.12 < 24 || >=26").lower, (22, 12))

    def test_registry_rejects_policy_typos(self):
        for field, value in (("enforce", "FAIL"), ("floor", "banana"), ("florr", "22")):
            with self.subTest(field=field):
                data = json.loads(json.dumps(REGISTRY))
                if field == "enforce":
                    data["consumers"]["app-fail"][field] = value
                else:
                    data["axes"]["next"][field] = value
                self.registry_path.write_text(json.dumps(data), encoding="utf-8")
                self.assertEqual(self.cli("--self-check").returncode, 2)
        self.registry_path.write_text(json.dumps(REGISTRY), encoding="utf-8")
        self.assertEqual(self.cli("--self-check").returncode, 0)

    def test_floating_urls_cannot_bypass_ref_check(self):
        for url in ("https://github.com/example/pkg/releases/download/latest/pkg.tgz",
                    "git+https://github.com/example/pkg.git?cache=" + "0" * 40 + "#main",
                    "https://example.com/packages/latest.tgz",
                    "https://example.com/packages/latest.tgz#v1.2.3",
                    "https://github.com/example/pkg/archive/main.zip#" + "0" * 40):
            with self.subTest(url=url):
                npm_fixture(self.repo, deps={"custom-lib": url}, engines={"node": ">=22.12"},
                            installed={"custom-lib": "1.0.0"})
                self.assertIn("FLOATING_REF", self.verdicts(self.run_checker(), "custom-lib"))
                self.assertEqual(self.cli(str(self.repo), "--repo", "app-fail").returncode, 1)

    def test_python_declaration_fragment_is_not_a_revision(self):
        for url in ("git+https://github.com/example/pkg.git@main#v1.2.3",
                    "git+https://github.com/example/pkg.git#v1.2.3"):
            with self.subTest(url=url):
                python_fixture(self.repo, requires=">=3.12", deps=["custom-lib @ " + url], locked={})
                self.assertEqual(self.cli(str(self.repo), "--repo", "app-fail").returncode, 1)
                self.assertIn("FLOATING_REF", self.verdicts(self.run_checker(), "custom-lib"))

    def test_python_declaration_and_uv_resolved_ref_are_distinct(self):
        sha = "a" * 40
        for ref in (sha, "py-v0.1.0"):
            with self.subTest(ref=ref):
                url = "git+https://github.com/example/pkg.git@" + ref + "#subdirectory=src"
                python_fixture(self.repo, requires=">=3.12", deps=["custom-lib @ " + url], locked={})
                self.assertEqual(self.verdicts(self.run_checker(), "custom-lib"), ["OK"])
        for fragment, expected in ((sha, "OK"), ("v1.2.3", "FLOATING_REF")):
            with self.subTest(fragment=fragment):
                python_fixture(self.repo, requires=">=3.12", deps=[], locked={},
                               git_locked={"custom-lib": ("1.0.0", "https://github.com/example/pkg?rev=main#" + fragment)})
                self.assertEqual(self.verdicts(self.run_checker(), "custom-lib"), [expected])
        python_fixture(self.repo, requires=">=3.12",
                       deps=["custom-lib @ git+https://github.com/example/pkg.git@" + sha],
                       locked={}, git_locked={"custom-lib": ("1.0.0", "https://github.com/example/pkg?rev=main#main")})
        self.assertEqual(self.verdicts(self.run_checker(), "custom-lib"), ["FLOATING_REF"])
        lock_text = (self.repo / "uv.lock").read_text(encoding="utf-8")
        (self.repo / "uv.lock").write_text(
            lock_text + '\n[[package]]\nname = "custom-lib"\nversion = "1.1.0"\n'
            'source = { git = "https://github.com/example/pkg?rev=short#abc" }\n', encoding="utf-8")
        self.assertEqual(self.verdicts(self.run_checker(), "custom-lib"), ["FLOATING_REF"])
        branch_url = "git+https://github.com/example/pkg.git@branch:topic@v1.2.3"
        python_fixture(self.repo, requires=">=3.12", deps=["custom-lib @ " + branch_url], locked={},
                       git_locked={"custom-lib": ("1.0.0", "https://github.com/example/pkg?branch=topic%40v1.2.3#" + sha)})
        self.assertEqual(self.verdicts(self.run_checker(), "custom-lib"), ["FLOATING_REF"])
        for field in ("tag", "rev"):
            python_fixture(self.repo, requires=">=3.12", deps=["custom-lib"], locked={},
                           git_locked={"custom-lib": ("1.0.0", "https://github.com/example/pkg?rev=main#" + sha)})
            with (self.repo / "pyproject.toml").open("a", encoding="utf-8") as stream:
                stream.write(f'\n[tool.uv.sources]\ncustom-lib = {{ git = "https://github.com/example/pkg.git", {field} = "topic@v1.2.3" }}\n')
            self.assertEqual(self.verdicts(self.run_checker(), "custom-lib"), ["FLOATING_REF"])
        npm_fixture(self.repo, deps={"custom-lib": "git+https://github.com/example/pkg.git#v1.2.3"},
                    engines={"node": ">=22.12"}, installed={"custom-lib": "1.2.3"})
        npm_findings = CV.Checker(CV.Registry.load(self.registry_path), "app-a", CV.date(2026, 9, 6))
        npm_findings.check_npm(next(scope for scope in CV.discover(self.repo) if scope.kind == "npm"))
        self.assertEqual(self.verdicts(npm_findings.findings, "custom-lib"), ["OK"])

    def test_version_helpers(self):
        self.assertEqual(CV.parse_version("22.12"), (22, 12))
        self.assertEqual(CV.parse_version("3.12-slim"), (3, 12))
        self.assertEqual(CV.parse_version("v1.63.0"), (1, 63, 0))
        self.assertIsNone(CV.parse_version("latest"))
        self.assertEqual(CV.lower_bound("^22.22.2 || ^24.15.0 || >=26.0.0").lower, (22, 22, 2))
        self.assertEqual(CV.lower_bound(">=0.40,<1.0"), CV.Bound((0, 40), False))
        self.assertEqual(CV.lower_bound("12.0.1"), CV.Bound((12, 0, 1), True))
        self.assertEqual(CV.lower_bound("^3.11").lower, (3, 11))
        self.assertIsNone(CV.lower_bound("*").lower)
        self.assertTrue(CV.range_contains((2, 1, 1), ">=2"))
        self.assertFalse(CV.range_contains((1, 9, 0), ">=2"))
        self.assertFalse(CV.range_contains((3, 0, 0), ">=2,<3"))

    def test_ref_pinning_heuristics(self):
        pinned = [
            "git+https://github.com/digitie/python-kasi-api@51c39c1b0dd5b169b748552e81b9b9a55e86b9a1",
            "git+https://github.com/digitie/kor-travel-common.git@py-v0.1.0#subdirectory=packages/py/kor-travel-common",
            "https://github.com/digitie/kor-travel-common/releases/download/tokens-v0.1.0/kor-travel-tokens-0.1.0.tgz",
            "https://github.com/digitie/maplibre-vworld-react/tarball/95b49d3",
            "github:digitie/maplibre-vworld-react#v0.2.0",
            "https://github.com/digitie/python-vworld-api/archive/a1fea840531f0b4d8e1b6a0db85e15063532602d.zip",
        ]
        floating = [
            "git+https://github.com/digitie/python-kasi-api.git@main",
            "git+https://github.com/digitie/python-kasi-api.git",
            "github:digitie/maplibre-vworld-react",
            "git+ssh://git@github.com/o/r.git#semver:^1.0",
        ]
        for text in pinned:
            self.assertTrue(CV.ref_is_pinned(text, kind="pypi" if "@" in text else "npm"), text)
        for text in floating:
            self.assertFalse(CV.ref_is_pinned(text), text)

    # --- npm lock v3 판정
    def test_npm_lock_verdicts(self):
        npm_fixture(self.repo, deps={"next": "^16.2.7", "react": "^19.2.8", "react-dom": "^19.2.8",
                                     "typescript": "^5.4.5"},
                    engines={"node": ">=22.12", "npm": "11.19.1"},
                    installed={"next": "16.2.7", "react": "19.2.8", "react-dom": "19.2.8",
                               "typescript": "5.9.3"})
        findings = self.run_checker()
        self.assertEqual(self.verdicts(findings, "next"), ["NOT_RECOMMENDED"])
        self.assertEqual(self.verdicts(findings, "react"), ["OK"])  # react/react-dom 행 병합
        self.assertEqual(self.verdicts(findings, "typescript"), ["OK"])
        self.assertEqual(self.verdicts(findings, "node"), ["OK"])
        self.assertEqual(self.verdicts(findings, "npm"), ["OK"])
        react = next(f for f in findings if f.key == "react")
        self.assertEqual(react.declared, "^19.2.8")

    def test_below_floor_and_above_max_and_exception(self):
        npm_fixture(self.repo, deps={"next": "^15.2.0", "typescript": "^7.0.2"}, engines={"node": ">=22.12"},
                    installed={"next": "15.5.24", "typescript": "7.0.2"})
        findings = self.run_checker()
        self.assertEqual(self.verdicts(findings, "next"), ["BELOW_FLOOR"])
        self.assertEqual(self.verdicts(findings, "typescript"), ["EXEMPT"])
        ts = next(f for f in findings if f.key == "typescript")
        self.assertIn("원 판정 ABOVE_MAX", ts.detail)
        # 다른 저장소에는 예외가 적용되지 않는다.
        other = self.run_checker(repo="app-b")
        self.assertEqual(self.verdicts(other, "typescript"), ["ABOVE_MAX"])

    def test_exception_expires_by_today(self):
        npm_fixture(self.repo, deps={"typescript": "^7.0.2"}, engines={"node": ">=22.12"},
                    installed={"typescript": "7.0.2"})
        self.assertEqual(self.verdicts(self.run_checker(today="2026-12-31"), "typescript"), ["EXEMPT"])
        self.assertEqual(self.verdicts(self.run_checker(today="2027-01-01"), "typescript"), ["EXEMPT_EXPIRED"])

    def test_no_lock_and_no_engines(self):
        npm_fixture(self.repo, deps={"next": "^16.3.4"}, engines=None, installed=None)
        findings = self.run_checker()
        self.assertEqual(self.verdicts(findings, "node"), ["NO_ENGINES"])
        self.assertEqual(self.verdicts(findings, "next"), ["NO_LOCK"])

    def test_engines_range_lower_bound(self):
        npm_fixture(self.repo, deps={}, engines={"node": ">=20", "npm": ">=11"}, installed={})
        findings = self.run_checker()
        node = next(f for f in findings if f.key == "node")
        self.assertEqual(node.verdict, "BELOW_FLOOR")
        self.assertEqual(node.installed, "20")
        self.assertEqual(self.verdicts(findings, "npm"), ["OK"])  # 범위 하한에는 NOT_RECOMMENDED 미적용

    def test_npm_floating_ref_and_workspace_link(self):
        npm_fixture(self.repo, deps={"maplibre-vworld-react": "github:digitie/maplibre-vworld-react",
                                     "@fixture/internal": "*", "left-pad": "latest"},
                    engines={"node": ">=22.12"},
                    installed={"left-pad": "1.3.0"},
                    extra_packages={
                        "node_modules/maplibre-vworld-react": {
                            "version": "0.0.0",
                            "resolved": "git+ssh://git@github.com/digitie/maplibre-vworld-react.git#95b49d3aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"},
                        "node_modules/@fixture/internal": {"resolved": "packages/internal", "link": True},
                    })
        findings = self.run_checker()
        self.assertEqual(self.verdicts(findings, "maplibre-vworld-react"), ["FLOATING_REF"])
        self.assertEqual(self.verdicts(findings, "left-pad"), ["FLOATING_REF"])
        self.assertEqual(self.verdicts(findings, "@fixture/internal"), [])  # 워크스페이스 링크는 허용

    def test_lockfile_version_other_than_3_is_no_lock(self):
        npm_fixture(self.repo, deps={"next": "^16.3.4"}, engines={"node": ">=22.12"},
                    installed={"next": "16.3.4"}, lock_version=2)
        findings = self.run_checker()
        self.assertIn("NO_LOCK", self.verdicts(findings, "package-lock.json"))
        self.assertEqual(self.verdicts(findings, "next"), ["NO_LOCK"])

    # --- Python
    def test_uv_lock_blocked_and_transitive_and_provider(self):
        python_fixture(self.repo, requires=">=3.12",
                       deps=["fastapi>=0.115", "mcp>=1",
                             "python-kasi-api @ git+https://github.com/digitie/python-kasi-api@51c39c1b0dd5b169b748552e81b9b9a55e86b9a1"],
                       locked={"fastapi": "0.141.1", "starlette": "1.6.0", "mcp": "2.1.1"},
                       git_locked={"python-kasi-api": ("0.1.0", "https://github.com/digitie/python-kasi-api?rev=51c39c1b0dd5b169b748552e81b9b9a55e86b9a1#51c39c1b0dd5b169b748552e81b9b9a55e86b9a1")})
        findings = self.run_checker()
        self.assertEqual(self.verdicts(findings, "python"), ["OK"])
        self.assertEqual(self.verdicts(findings, "fastapi"), ["OK"])
        self.assertEqual(self.verdicts(findings, "mcp"), ["BLOCKED"])
        starlette = next(f for f in findings if f.key == "starlette")
        self.assertEqual((starlette.declared, starlette.verdict), ("(전이)", "OK"))
        provider = next(f for f in findings if f.key == "python-kasi-api")
        self.assertEqual((provider.ecosystem, provider.verdict, provider.installed), ("git", "OK", "51c39c1b0dd5"))

    def test_uv_lock_requires_python_is_checked_against_floor(self):
        python_fixture(self.repo, requires=">=3.12", lock_requires=">=3.10",
                       deps=["fastapi>=0.115"], locked={"fastapi": "0.141.1"})
        python_findings = self.run_checker()
        self.assertEqual(self.verdicts(python_findings, "python"), ["OK", "BELOW_FLOOR"])
        lock_python = next(f for f in python_findings
                           if f.key == "python" and "uv.lock" in f.scope)
        self.assertEqual(lock_python.installed, "3.10")
        self.assertIn("floor 3.11", lock_python.detail)

    def test_uv_lock_schema_and_source_fail_closed(self):
        python_fixture(self.repo, requires=">=3.12", deps=["fastapi>=0.115"],
                       locked={"fastapi": "0.141.1"})
        lock_path = self.repo / "uv.lock"
        original = lock_path.read_text(encoding="utf-8")
        for replacement in (
            ("version = 1", "version = 2"),
            ("revision = 3", "revision = 5"),
            ("revision = 3", "revision = 3\nresolution-markers = 42"),
            ('source = { registry = "https://pypi.org/simple" }',
             'source = { registry = "https://pypi.org/simple", git = "https://example.invalid/repo" }'),
            ('source = { registry = "https://pypi.org/simple" }',
             'source = { registry = "https://[" }'),
            ('source = { registry = "https://pypi.org/simple" }',
             'source = { registry = "https://pypi.org/simple" }\ndependencies = { broken = true }'),
            ('source = { registry = "https://pypi.org/simple" }',
             'source = { registry = "https://@" }'),
            ('source = { registry = "https://pypi.org/simple" }',
             'source = { registry = "https://example.invalid:bad/simple" }'),
            ('source = { registry = "https://pypi.org/simple" }',
             'source = { registry = "https://pypi.org/simple" }\noptional-dependencies = { test = [42] }'),
        ):
            with self.subTest(replacement=replacement):
                lock_path.write_text(original.replace(*replacement), encoding="utf-8")
                with self.assertRaises(ValueError):
                    self.run_checker()
        lock_path.write_text(original, encoding="utf-8")

    def test_uv_input_error_does_not_echo_input_names(self):
        python_fixture(self.repo, requires=">=3.12", deps=["fastapi>=0.115"],
                       locked={"fastapi": "0.141.1"})
        lock_path = self.repo / "uv.lock"
        lock_path.write_text(lock_path.read_text(encoding="utf-8")
                             .replace("version = 1", "version = 1\nSENTINEL_INPUT_FIELD = true"),
                             encoding="utf-8")
        result = self.cli(str(self.repo), "--repo", "app-fail", "--quiet")
        self.assertEqual(result.returncode, 2)
        self.assertNotIn("SENTINEL_INPUT_FIELD", result.stdout)
        self.assertNotIn(str(self.repo), result.stdout)

    def test_uv_shared_lock_checks_transitive_package_from_member_scope(self):
        workspace = self.root / "workspace"
        member = workspace / "packages" / "api"
        member.mkdir(parents=True)
        (member / "pyproject.toml").write_text(
            '[project]\nname = "member"\nversion = "0.0.0"\nrequires-python = ">=3.12"\n'
            'dependencies = ["fastapi>=0.115"]\n', encoding="utf-8")
        (workspace / "uv.lock").write_text(
            'version = 1\nrevision = 3\nrequires-python = ">=3.12"\n\n'
            '[[package]]\nname = "member"\nversion = "0.0.0"\nsource = { virtual = "." }\n\n'
            '[[package]]\nname = "fastapi"\nversion = "0.141.1"\n'
            'source = { registry = "https://pypi.org/simple" }\n\n'
            '[[package]]\nname = "mcp"\nversion = "2.1.1"\n'
            'source = { registry = "https://pypi.org/simple" }\n', encoding="utf-8")
        findings = self.run_checker(root=workspace)
        self.assertEqual(self.verdicts(findings, "fastapi"), ["OK"])
        self.assertEqual(self.verdicts(findings, "mcp"), ["BLOCKED"])

    def test_uv_dependency_group_and_list_source_are_inspected(self):
        (self.repo / "pyproject.toml").write_text(
            '[project]\nname = "fixture"\nversion = "0.0.0"\nrequires-python = ">=3.12"\n'
            'dependencies = []\n\n[dependency-groups]\nlint = ["fastapi>=0.115"]\ndev = [{ include-group = "lint" }]\n\n'
            '[tool.uv.sources]\ncustom-lib = [\n'
            '  { git = "https://github.com/example/custom-lib", branch = "v1.2.3" },\n'
            '  { git = "https://github.com/example/custom-lib", tag = "v1.2.3" },\n]\n',
            encoding="utf-8")
        findings = self.run_checker()
        self.assertEqual(self.verdicts(findings, "fastapi"), ["NO_LOCK"])
        self.assertEqual(self.verdicts(findings, "custom-lib"), ["FLOATING_REF", "OK"])

        malformed_group = (self.repo / "pyproject.toml").read_text(encoding="utf-8").replace(
            'lint = ["fastapi>=0.115"]', 'lint = "fastapi>=0.115"')
        (self.repo / "pyproject.toml").write_text(malformed_group, encoding="utf-8")
        self.assertEqual(self.cli(str(self.repo), "--repo", "app-fail", "--quiet").returncode, 2)
        malformed_source = malformed_group.replace('lint = "fastapi>=0.115"',
                                                     'lint = ["fastapi>=0.115"]')
        malformed_source = malformed_source.replace(
            'custom-lib = [\n  { git = "https://github.com/example/custom-lib", branch = "v1.2.3" },\n  { git = "https://github.com/example/custom-lib", tag = "v1.2.3" },\n]',
            'custom-lib = "invalid"')
        (self.repo / "pyproject.toml").write_text(malformed_source, encoding="utf-8")
        self.assertEqual(self.cli(str(self.repo), "--repo", "app-fail", "--quiet").returncode, 2)

        normalized_group = malformed_group.replace(
            '[dependency-groups]\nlint = "fastapi>=0.115"\ndev = [{ include-group = "lint" }]',
            '[dependency-groups]\nTest_Group = ["fastapi>=0.115"]\ndev = [{ include-group = "test-group" }]')
        (self.repo / "pyproject.toml").write_text(normalized_group, encoding="utf-8")
        self.assertNotEqual(self.cli(str(self.repo), "--repo", "app-fail", "--quiet").returncode, 2)

        cyclic_group = normalized_group.replace(
            'Test_Group = ["fastapi>=0.115"]', 'Test_Group = [{ include-group = "dev" }]')
        (self.repo / "pyproject.toml").write_text(cyclic_group, encoding="utf-8")
        self.assertEqual(self.cli(str(self.repo), "--repo", "app-fail", "--quiet").returncode, 2)

        extra_include_key = normalized_group.replace(
            '{ include-group = "test-group" }',
            '{ include-group = "test-group", unexpected = true }')
        (self.repo / "pyproject.toml").write_text(extra_include_key, encoding="utf-8")
        self.assertEqual(self.cli(str(self.repo), "--repo", "app-fail", "--quiet").returncode, 2)

        missing_group = malformed_group.replace('lint = "fastapi>=0.115"',
                                                  'lint = [{ include-group = "missing" }]')
        (self.repo / "pyproject.toml").write_text(missing_group, encoding="utf-8")
        self.assertEqual(self.cli(str(self.repo), "--repo", "app-fail", "--quiet").returncode, 2)

    def test_python_floating_ref_without_lock(self):
        python_fixture(self.repo, requires=None,
                       deps=["fastapi>=0.110", "python-kasi-api @ git+https://github.com/digitie/python-kasi-api.git@main"],
                       locked=None)
        findings = self.run_checker()
        self.assertEqual(self.verdicts(findings, "python"), ["NO_ENGINES"])
        self.assertEqual(self.verdicts(findings, "fastapi"), ["NO_LOCK"])
        self.assertEqual(self.verdicts(findings, "python-kasi-api"), ["FLOATING_REF"])

    def test_invalid_poetry_lock_is_input_error(self):
        (self.repo / "pyproject.toml").write_text(
            '[tool.poetry]\nname = "fixture"\nversion = "0.0.0"\n\n'
            '[tool.poetry.dependencies]\npython = "^3.11"\nfastapi = "^0.110.0"\n', encoding="utf-8")
        (self.repo / "poetry.lock").write_text("# placeholder\n", encoding="utf-8")
        result = self.cli(str(self.repo), "--repo", "app-fail", "--quiet")
        self.assertEqual(result.returncode, 2)
        self.assertNotIn(str(self.repo), result.stdout)

    def test_poetry_lock_packages_and_git_sources(self):
        (self.repo / "pyproject.toml").write_text(
            '[tool.poetry]\nname = "fixture"\nversion = "0.0.0"\n\n'
            '[tool.poetry.dependencies]\npython = "^3.11"\nfastapi = "^0.110.0"\n'
            'custom-lib = { git = "https://github.com/example/custom-lib.git", tag = "v1.2.3" }\n',
            encoding="utf-8")
        (self.repo / "poetry.lock").write_text(
            '[[package]]\nname = "fastapi"\nversion = "0.141.1"\n\n'
            '[[package]]\nname = "custom-lib"\nversion = "1.2.3"\n\n'
            '[package.source]\ntype = "git"\nurl = "https://github.com/example/custom-lib.git"\n'
            'reference = "v1.2.3"\nresolved_reference = "' + "a" * 40 + '"\n\n'
            '[metadata]\nlock-version = "2.1"\npython-versions = ">=3.11,<4.0"\n', encoding="utf-8")
        findings = self.run_checker()
        self.assertEqual(self.verdicts(findings, "python"), ["OK"])
        self.assertEqual(self.verdicts(findings, "fastapi"), ["OK"])
        self.assertEqual(self.verdicts(findings, "custom-lib"), ["OK"])

        lock = (self.repo / "poetry.lock").read_text(encoding="utf-8").replace(
            'reference = "v1.2.3"', 'reference = "main"')
        (self.repo / "poetry.lock").write_text(lock, encoding="utf-8")
        manifest = (self.repo / "pyproject.toml").read_text(encoding="utf-8").replace(
            'tag = "v1.2.3"', 'branch = "main"')
        (self.repo / "pyproject.toml").write_text(manifest, encoding="utf-8")
        self.assertEqual(self.verdicts(self.run_checker(), "custom-lib"), ["FLOATING_REF"])

    def test_requirements_recursive_exact_range_blocked_and_no_lock(self):
        nested = self.repo / "nested"
        nested.mkdir()
        (self.repo / "requirements.txt").write_text(
            "-r nested/base.txt\nmcp>=2\n", encoding="utf-8")
        (nested / "base.txt").write_text(
            "fastapi==0.141.1\ncustom-lib @ git+https://github.com/example/custom-lib.git@main\n",
            encoding="utf-8")
        findings = self.run_checker()
        self.assertEqual(self.verdicts(findings, "fastapi"), ["OK"])
        self.assertEqual(self.verdicts(findings, "mcp"), ["BLOCKED"])
        self.assertEqual(self.verdicts(findings, "custom-lib"), ["FLOATING_REF"])
        self.assertEqual(self.verdicts(findings, "lockfile"), ["NO_LOCK"])
        result = self.cli(str(self.repo), "--repo", "app-fail", "--quiet")
        self.assertEqual(result.returncode, 1)
        self.assertIn("::error title=check_versions::BLOCKED", result.stdout)

    def test_requirements_safe_blocked_range_is_not_blocked(self):
        (self.repo / "requirements.txt").write_text("mcp<2\n", encoding="utf-8")
        findings = self.run_checker()
        self.assertEqual(self.verdicts(findings, "mcp"), [])
        self.assertEqual(self.verdicts(findings, "lockfile"), ["NO_LOCK"])

    def test_requirements_duplicate_declarations_are_all_checked(self):
        (self.repo / "requirements.txt").write_text("mcp<2\nmcp>=2\n", encoding="utf-8")
        self.assertEqual(self.verdicts(self.run_checker(), "mcp"), ["BLOCKED"])

    def test_requirements_range_boundaries_use_normalized_versions(self):
        data = json.loads(json.dumps(REGISTRY))
        data["blocked"][0]["range"] = ">=2.0"
        self.registry_path.write_text(json.dumps(data), encoding="utf-8")
        (self.repo / "requirements.txt").write_text("mcp<2\n", encoding="utf-8")
        self.assertEqual(self.verdicts(self.run_checker(), "mcp"), [])

    def test_requirements_include_cycle_and_missing_file_are_input_errors(self):
        (self.repo / "requirements.txt").write_text("-r child.txt\n", encoding="utf-8")
        (self.repo / "child.txt").write_text("-r requirements.txt\n", encoding="utf-8")
        result = self.cli(str(self.repo), "--repo", "app-fail", "--quiet")
        self.assertEqual(result.returncode, 2)
        (self.repo / "child.txt").write_text("-r missing.txt\n", encoding="utf-8")
        result = self.cli(str(self.repo), "--repo", "app-fail", "--quiet")
        self.assertEqual(result.returncode, 2)

    def test_requirements_include_forms_and_per_requirement_hashes(self):
        nested = self.repo / "nested"
        nested.mkdir()
        (self.repo / "requirements.txt").write_text(
            "--requirement=nested/equals.txt\n--requirement nested/space.txt\n"
            "-r nested/compact.txt\n-rnested/compact.txt\n",
            encoding="utf-8")
        (nested / "equals.txt").write_text("fastapi==0.141.1 --hash=sha256:" + "a" * 64 + "\n",
                                           encoding="utf-8")
        (nested / "space.txt").write_text("fastapi==0.141.1\t# 탭 주석\n", encoding="utf-8")
        (nested / "compact.txt").write_text("fastapi==0.141.1 --hash sha256:" + "b" * 64 + "\n",
                                             encoding="utf-8")
        findings = self.run_checker()
        self.assertEqual(self.verdicts(findings, "fastapi"), ["OK"])
        self.assertEqual(len([f for f in findings if f.key == "fastapi"]), 1)

    def test_requirements_quoted_include_paths_are_expanded(self):
        (self.repo / "requirements.txt").write_text(
            '-r "child name.txt"\n--requirement="second child.txt"\n', encoding="utf-8")
        (self.repo / "child name.txt").write_text("mcp>=2\n", encoding="utf-8")
        (self.repo / "second child.txt").write_text("fastapi==0.141.1\n", encoding="utf-8")
        findings = self.run_checker()
        self.assertEqual(self.verdicts(findings, "mcp"), ["BLOCKED"])
        self.assertEqual(self.verdicts(findings, "fastapi"), ["OK"])

    def test_requirements_editable_git_and_invalid_options_fail_closed(self):
        (self.repo / "requirements.txt").write_text(
            "-e git+https://example.com/repo.git@main#egg=custom-lib\n", encoding="utf-8")
        findings = self.run_checker()
        floating = next(f for f in findings if f.key == "custom-lib")
        self.assertEqual(floating.verdict, "FLOATING_REF")
        self.assertIn("@main", floating.declared)
        for invalid in (
            "--unsupported-option\n",
            "--hash sha256:" + "a" * 64 + "\n",
            "-e git+https://example.com/repo.git@main\n",
            "fastapi==not-a-version\n",
            "fastapi>=2,<2\n",
        ):
            with self.subTest(invalid=invalid):
                (self.repo / "requirements.txt").write_text(invalid, encoding="utf-8")
                self.assertEqual(self.cli(str(self.repo), "--repo", "app-fail", "--quiet").returncode, 2)

    def test_requirements_range_overlap_uses_pep440_bounds(self):
        cases = (
            ("==2.*", ">=2", True),
            ("==1.*", ">=2", False),
            ("~=1.0", ">=2", False),
            ("~=1.0", ">=1.5", True),
            (">= 2", "<2", False),
            ("<=2", ">2", False),
            (">=2,<3", "==2.*", True),
            (">=2,<2", ">=2", True),  # 빈/잘못된 교집합은 안전하지 않은 입력으로 닫는다.
        )
        for left, right, expected in cases:
            with self.subTest(left=left, right=right):
                self.assertEqual(CV.ranges_overlap(left, right), expected)

    def test_requirements_range_equalities_intersect_idempotently(self):
        for spec in ("mcp==2.*,==2.1", "mcp==2.1,==2.*", "mcp==2.*,==2.*"):
            with self.subTest(spec=spec):
                (self.repo / "requirements.txt").write_text(spec + "\n", encoding="utf-8")
                self.assertEqual(self.cli(str(self.repo), "--repo", "app-a", "--quiet").returncode, 0)
        (self.repo / "requirements.txt").write_text("mcp==2.1,==2.2\n", encoding="utf-8")
        self.assertEqual(self.cli(str(self.repo), "--repo", "app-fail", "--quiet").returncode, 2)

    def test_poetry_source_and_metadata_validation_fail_closed(self):
        (self.repo / "pyproject.toml").write_text(
            '[tool.poetry]\nname = "fixture"\nversion = "0.0.0"\n\n'
            '[tool.poetry.dependencies]\npython = "^3.11"\nfastapi = "^0.110.0"\n',
            encoding="utf-8")
        valid = (
            '[[package]]\nname = "fastapi"\nversion = "0.141.1"\n\n'
            '[metadata]\nlock-version = "2.1"\npython-versions = ">=3.11,<4.0"\n')
        lock_path = self.repo / "poetry.lock"
        for suffix in (
            '[package.source]\ntype = "git"\nurl = "https://["\n',
            '[package.source]\ntype = "url"\nurl = "https://example.com:bad/pkg.whl"\n',
            '[package.source]\ntype = "file"\nurl = 42\n',
            '[metadata]\nlock-version = "2.1"\n',
        ):
            with self.subTest(suffix=suffix):
                lock_path.write_text(valid.replace('[metadata]', suffix + '\n[metadata]')
                                     if suffix.startswith('[package.source]') else suffix,
                                     encoding="utf-8")
                self.assertEqual(self.cli(str(self.repo), "--repo", "app-fail", "--quiet").returncode, 2)

    def test_poetry_input_error_does_not_echo_url_value(self):
        marker = "SENSITIVE" + "A" * 12
        (self.repo / "pyproject.toml").write_text(
            '[tool.poetry]\nname = "fixture"\nversion = "0.0.0"\n\n'
            '[tool.poetry.dependencies]\npython = "^3.11"\nfastapi = "^0.110.0"\n',
            encoding="utf-8")
        (self.repo / "poetry.lock").write_text(
            '[[package]]\nname = "fastapi"\nversion = "0.141.1"\n\n'
            '[[package]]\nname = "custom-lib"\nversion = "1.2.3"\n'
            '[package.source]\ntype = "git"\nurl = "https://[' + marker + ']"\n'
            'reference = "main"\nresolved_reference = "' + "a" * 40 + '"\n\n'
            '[metadata]\nlock-version = "2.1"\npython-versions = ">=3.11,<4.0"\n',
            encoding="utf-8")
        result = self.cli(str(self.repo), "--repo", "app-fail", "--quiet")
        self.assertEqual(result.returncode, 2)
        self.assertNotIn(marker, result.stdout)

    def test_manifest_git_input_error_does_not_create_output_rows(self):
        marker = "BADPORT" + "A" * 8
        (self.repo / "pyproject.toml").write_text(
            '[project]\nname = "fixture"\nversion = "0.0.0"\nrequires-python = ">=3.11"\n'
            'dependencies = ["custom-lib @ https://example.com:' + marker + '/repo.git@v1.2.3"]\n',
            encoding="utf-8")
        (self.repo / "uv.lock").write_text(
            'version = 1\nrevision = 3\nrequires-python = ">=3.11"\n\n'
            '[[package]]\nname = "custom-lib"\nversion = "1.2.3"\n'
            'source = { git = "https://example.com/repo.git#' + "a" * 40 + '" }\n',
            encoding="utf-8")
        report = self.root / "manifest-error.json"
        markdown = self.root / "manifest-error.md"
        summary = self.root / "manifest-summary.md"
        result = self.cli(str(self.repo), "--repo", "app-fail", "--quiet", "--json", str(report),
                          "--markdown", str(markdown), "--no-step-summary")
        self.assertEqual(result.returncode, 2)
        self.assertNotIn(marker, result.stdout)
        self.assertFalse(report.exists())
        self.assertFalse(markdown.exists())
        self.assertFalse(summary.exists())

    def test_requirements_malformed_marker_parentheses_and_option_value_fail_closed(self):
        for invalid in (
            'fastapi==0.141.1; this is invalid\n',
            'fastapi(((==0.141.1)))\n',
            '--only-binary\n',
        ):
            with self.subTest(invalid=invalid):
                (self.repo / "requirements.txt").write_text(invalid, encoding="utf-8")
                self.assertEqual(self.cli(str(self.repo), "--repo", "app-fail", "--quiet").returncode, 2)

    def test_poetry_upstream_optional_fields_are_accepted(self):
        (self.repo / "pyproject.toml").write_text(
            '[tool.poetry]\nname = "fixture"\nversion = "0.0.0"\n\n'
            '[tool.poetry.dependencies]\npython = "^3.11"\n'
            'fastapi = "^0.110.0"\ncustom-lib = { git = "https://example.com/repo.git", tag = "v1.2.3", subdirectory = "python" }\n',
            encoding="utf-8")
        (self.repo / "poetry.lock").write_text(
            '[[package]]\nname = "fastapi"\nversion = "0.141.1"\n'
            '[package.source]\ntype = "legacy"\nurl = "https://example.com/simple"\nreference = "mirror"\n\n'
            '[[package]]\nname = "custom-lib"\nversion = "1.2.3"\n'
            '[package.source]\ntype = "git"\nurl = "https://example.com/repo.git"\n'
            'reference = "v1.2.3"\nsubdirectory = "python"\nresolved_reference = "' + "a" * 40 + '"\n\n'
            '[extras]\nweb = ["fastapi"]\n\n'
            '[metadata]\nlock-version = "2.1"\npython-versions = ">=3.11,<4.0"\n',
            encoding="utf-8")
        findings = self.run_checker()
        self.assertEqual(self.verdicts(findings, "fastapi"), ["OK"])
        self.assertEqual(self.verdicts(findings, "custom-lib"), ["OK"])

    def test_poetry_dependency_list_preserves_branch_and_rejects_malformed_list(self):
        (self.repo / "pyproject.toml").write_text(
            '[tool.poetry]\nname = "fixture"\nversion = "0.0.0"\n\n'
            '[tool.poetry.dependencies]\npython = "^3.11"\n'
            'custom-lib = [\n'
            '  { git = "https://example.com/repo.git", branch = "main" },\n'
            '  { git = "https://example.com/repo.git", tag = "v1.2.3" },\n]\n',
            encoding="utf-8")
        (self.repo / "poetry.lock").write_text(
            '[[package]]\nname = "custom-lib"\nversion = "1.2.3"\n\n'
            '[package.source]\ntype = "git"\nurl = "https://example.com/repo.git"\n'
            'resolved_reference = "' + "a" * 40 + '"\n\n'
            '[metadata]\nlock-version = "2.1"\npython-versions = ">=3.11,<4.0"\n',
            encoding="utf-8")
        findings = self.run_checker()
        self.assertEqual(sorted(self.verdicts(findings, "custom-lib")), ["FLOATING_REF", "OK"])
        branch = next(f for f in findings if f.key == "custom-lib" and f.verdict == "FLOATING_REF")
        self.assertIn("branch:main", branch.declared)
        (self.repo / "pyproject.toml").write_text(
            (self.repo / "pyproject.toml").read_text(encoding="utf-8").replace(
                '{ git = "https://example.com/repo.git", branch = "main" }', "1"),
            encoding="utf-8")
        self.assertEqual(self.cli(str(self.repo), "--repo", "app-fail", "--quiet").returncode, 2)

    def test_requirements_glob_discovery_keeps_nested_base_out_of_scope(self):
        (self.repo / "requirements-dev.txt").write_text("fastapi==0.141.1\n", encoding="utf-8")
        nested = self.repo / "requirements"
        nested.mkdir()
        (nested / "base.txt").write_text("fastapi==0.141.1\n", encoding="utf-8")
        scopes = CV.discover(self.repo)
        self.assertEqual([scope.manifest.name for scope in scopes if scope.lock_kind == "requirements"],
                         ["requirements-dev.txt"])

    def test_no_lock_manifest_reports_no_lock_and_missing_path_is_input_error(self):
        fixture = SCRIPT.parents[1] / "tests" / "fixtures" / "versions" / "geo-no-lock"
        result = self.cli(str(fixture), "--repo", "geo", "--mode", "report")
        self.assertEqual(result.returncode, 0)
        self.assertIn("NO_LOCK", result.stdout)
        missing = self.cli(str(self.root / "does-not-exist"), "--repo", "geo", "--quiet")
        self.assertEqual(missing.returncode, 2)

    def test_t005b_repository_fixtures(self):
        fixtures = SCRIPT.parents[1] / "tests" / "fixtures" / "versions"
        poetry = self.cli(str(fixtures / "ktdm"), "--repo", "app-a", "--mode", "report")
        self.assertEqual(poetry.returncode, 0)
        self.assertIn("custom-lib", poetry.stdout)
        self.assertIn("OK", poetry.stdout)
        requirements = self.cli(str(fixtures / "ktc"), "--repo", "app-a", "--mode", "report")
        self.assertEqual(requirements.returncode, 0)
        self.assertIn("NO_LOCK", requirements.stdout)
        self.assertIn("FLOATING_REF", requirements.stdout)

    # --- 매니페스트·모드·CLI
    def test_manifest_lockfiles_and_registry_enforce(self):
        repo = self.root / "app-fail"
        (repo / "web").mkdir(parents=True)
        npm_fixture(repo / "web", deps={"next": "^15.2.0"}, engines={"node": ">=22.12"},
                    installed={"next": "15.5.24"})
        manifest = repo / "kor-travel-common.lock.json"
        manifest.write_text(json.dumps({
            "schema": CV.MANIFEST_SCHEMA, "repo": "app-fail",
            "lockfiles": [{"kind": "npm", "path": "web/package-lock.json", "scope": "web"},
                          {"kind": "uv", "path": "api/uv.lock", "scope": "api"}],
        }), encoding="utf-8")
        result = self.cli("--manifest", str(manifest), "--today", "2026-09-06", "--quiet")
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("mode=fail", result.stdout)
        self.assertIn("::error title=check_versions::BELOW_FLOOR: app-fail/web next", result.stdout)
        self.assertIn("NO_LOCK", result.stdout)  # api/uv.lock 없음

    def test_report_mode_exit_zero_with_error_annotation(self):
        python_fixture(self.repo, requires=">=3.12",
                       deps=["python-kasi-api @ git+https://github.com/digitie/python-kasi-api.git@main"],
                       locked={})
        before = snapshot(self.root)
        out_json = self.root / "out" / "report.json"
        result = self.cli(str(self.repo), "--repo", "a", "--today", "2026-09-06", "--json", str(out_json))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("::error title=check_versions::FLOATING_REF", result.stdout)
        self.assertIn("mode=report", result.stdout)
        self.assertEqual(snapshot(self.root), before | {"out/report.json": snapshot(self.root)["out/report.json"]})
        report = json.loads(out_json.read_text(encoding="utf-8"))
        self.assertEqual(report["schema"], CV.REPORT_SCHEMA)
        self.assertEqual(report["repo"], "app-a")
        self.assertEqual(report["summary"]["FLOATING_REF"], 1)

    def test_mode_override_and_warn_annotation(self):
        npm_fixture(self.repo, deps={"next": "^15.2.0"}, engines={"node": ">=22.12"},
                    installed={"next": "15.5.24"})
        warn = self.cli(str(self.repo), "--mode", "warn", "--quiet")
        self.assertEqual(warn.returncode, 0)
        self.assertIn("::warning title=check_versions::BELOW_FLOOR", warn.stdout)
        fail = self.cli(str(self.repo), "--mode", "fail", "--quiet")
        self.assertEqual(fail.returncode, 1)

    def test_registry_schema_error_exit_2(self):
        bad = self.root / "bad.json"
        bad.write_text(json.dumps({"schema": "other", "axes": {}}), encoding="utf-8")
        result = subprocess.run([sys.executable, "-B", "-X", "utf8", str(SCRIPT), "--registry", str(bad),
                                 str(self.repo)], capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(result.returncode, 2)
        self.assertIn("::error", result.stdout)

    def test_repo_registry_values_load(self):
        """저장소 루트 versions.json이 스키마·필수 필드를 만족하고 예외 until이 ISO 날짜다."""
        registry = CV.Registry.load(SCRIPT.parents[1] / "versions.json")
        self.assertEqual(registry.data["baseline"], "2026-09")
        self.assertIn("node", registry.axes)
        self.assertEqual(registry.enforce("kor-travel-map"), "report")
        self.assertEqual(registry.consumer("ktdm"), "kor-travel-docker-manager")
        for entry in registry.data["exceptions"]:
            self.assertIn(entry["repo"], registry.data["consumers"], entry)
            self.assertIn(entry["key"], registry.axes, entry)


if __name__ == "__main__":
    unittest.main()
