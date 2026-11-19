# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"""직접 축만 맞춘 뒤 남은 실제 shared lock 차이·설치 교집합 회귀."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from test_check_versions import CV, SCRIPT, python_fixture, snapshot


CATALOG = SCRIPT.parents[1] / "versions.json"
EVIDENCE = json.loads((Path(__file__).parent / "fixtures/shared-python-20261120.json").read_text())


class SharedProfileTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.repo = self.root / "consumer"
        self.repo.mkdir()
        self.registry = CV.Registry.load(CATALOG)
        self.policy = CV.Checker(self.registry, "kor-travel-weather", None).application_policy()
        self.targets = {name: row["exact"] for name, row in self.policy.items()}

    def cli(self, *args, repo="kor-travel-weather"):
        return subprocess.run([sys.executable, str(SCRIPT), str(self.repo), "--repo", repo,
                               "--strict-python-application", "--no-step-summary", "--quiet",
                               *args], capture_output=True, text=True)

    def full_lock(self, changes=None, requires=">=3.12"):
        packages = {name: self.targets[name] for name in EVIDENCE["sharedNames"] if name in self.targets}
        packages.update(changes or {})
        python_fixture(self.repo, requires=requires, deps=["shared-anchor==1.0.0"],
                       locked={"shared-anchor": "1.0.0", **packages})

    def test_catalog_covers_all_105_original_shared_names(self):
        providers = self.registry.data["providers"]["packages"]
        self.assertEqual(set(EVIDENCE["sharedNames"]) - self.targets.keys(),
                         {"python-kasi-api", "python-krex-api", "python-vworld-api"})
        for name in set(EVIDENCE["sharedNames"]) - self.targets.keys():
            self.assertRegex(providers[name]["ref"], r"^[0-9a-f]{40}$")
        self.assertEqual(len(EVIDENCE["oldMismatchVersions"]), 38)

    def test_all_current_shared_lock_rows_pass_without_direct_dependency_promotion(self):
        self.full_lock()
        before = snapshot(self.repo)
        result = self.cli()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(snapshot(self.repo), before)
        self.assertNotIn("starlette", (self.repo / "pyproject.toml").read_text())
        self.assertIn("설치본 미검증; 실행동작/바이트 별도", result.stdout)
        self.assertNotIn("관측된 설치버전 대조", result.stdout)

    def test_all_38_original_transitive_and_dev_gaps_fail_closed(self):
        for name, old in EVIDENCE["oldMismatchVersions"].items():
            with self.subTest(package=name, old=old):
                self.full_lock({name: old})
                output = self.root / "report.json"
                result = self.cli("--json", str(output))
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                findings = json.loads(output.read_text())["findings"]
                self.assertTrue(any(row["key"] == name and row["verdict"] != "OK" for row in findings))

    def test_equal_but_outdated_packages_are_not_omitted(self):
        self.assertTrue(EVIDENCE["equalButOutdated"])
        for name, old in EVIDENCE["equalButOutdated"].items():
            with self.subTest(package=name):
                self.full_lock({name: old})
                self.assertEqual(self.cli().returncode, 1)

    def test_no_shared_catalog_row_can_escape_as_transitive_or_dev(self):
        for name in EVIDENCE["sharedNames"]:
            if name not in self.targets:
                continue
            with self.subTest(package=name):
                self.full_lock({name: "0.0.0"})
                self.assertEqual(self.cli().returncode, 1)

    def test_dropping_referenced_old_lock_row_does_not_hide_the_gap(self):
        python_fixture(self.repo, requires=">=3.12", deps=["shared-anchor==1.0.0"],
                       locked={"shared-anchor": "1.0.0"})
        path = self.repo / "uv.lock"
        path.write_text(path.read_text().replace('version = "1.0.0"',
                       'version = "1.0.0"\ndependencies = [{name="starlette"}]'))
        self.assertEqual(self.cli().returncode, 1)

    def test_root_python_minimum_must_admit_pyproj_38(self):
        self.full_lock(requires=">=3.11")
        self.assertEqual(self.cli("--python-version", "3.12").returncode, 1)
        self.full_lock(requires=">=3.12")
        self.assertEqual(self.cli("--python-version", "3.12").returncode, 0)

    def test_workspace_sdk_lower_minimum_is_not_rewritten_for_app_shared_lock(self):
        self.full_lock()
        sdk = self.repo / "packages/sdk"
        sdk.mkdir(parents=True)
        (sdk / "pyproject.toml").write_text('[project]\nname="sdk"\nrequires-python=">=3.10"\n'
                                         'dependencies=["pyproj>=3.6"]\n')
        before = snapshot(self.repo)
        result = self.cli()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(snapshot(self.repo), before)

    def test_constraints_and_actual_installed_intersection_do_not_force_unused_packages(self):
        (self.repo / "requirements.txt").write_text("httpx==0.28.1\n")
        (self.repo / "image.txt").write_text("starlette==1.10.0\nanyio==4.16.0\n")
        observed = self.root / "native.json"
        observed.write_text(json.dumps({"python": "3.12.7", "packages": {"httpx": "0.28.1"}}))
        output = self.root / "report.json"
        result = self.cli("--constraints", "image.txt", "--installed-versions", str(observed),
                          "--json", str(output))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        record = json.loads(output.read_text())["selectedPythonApplication"]
        self.assertEqual(record["installedVersionIntersection"]["count"], 1)
        self.assertEqual(record["runtimeImplementation"], "NOT_CHECKED")
        self.assertIn("관측된 설치버전 대조; 실행동작/바이트 별도", result.stdout)
        self.assertNotIn("설치본 미검증", result.stdout)
        observed.write_text(json.dumps({"python": "3.12.7", "packages": {"anyio": "4.14.2"}}))
        self.assertEqual(self.cli("--constraints", "image.txt", "--installed-versions", str(observed)).returncode, 1)

    def test_installed_metadata_errors_are_private_and_not_empty_success(self):
        (self.repo / "requirements.txt").write_text("httpx==0.28.1\n")
        path = self.root / "native.json"
        cases = [
            {"python": "3.12", "packages": {"HTTPX": "0.28.1", "httpx": "0.28.1"}},
            {"python": "3.12", "packages": {"httpx": "SECRET_SENTINEL"}},
            {"python": "SECRET_SENTINEL", "packages": {"httpx": "0.28.1"}},
            {"python": "3.12", "packages": {"unrelated": "1.0"}},
        ]
        for data in cases:
            with self.subTest(data=data):
                path.write_text(json.dumps(data))
                result = self.cli("--installed-versions", str(path))
                self.assertEqual(result.returncode, 2)
                self.assertNotIn("SECRET_SENTINEL", result.stdout + result.stderr)

    def test_role_python_cannot_disagree_with_actual_observation(self):
        (self.repo / "requirements.txt").write_text("httpx==0.28.1\n")
        path = self.root / "native.json"
        path.write_text(json.dumps({"python": "3.12.7", "packages": {"httpx": "0.28.1"}}))
        self.assertEqual(self.cli("--python-version", "3.11", "--installed-versions", str(path)).returncode, 2)

    def test_concierge_real_python311_compatibility_is_not_global_exception(self):
        (self.repo / "requirements.txt").write_text("pyproj>=3.6\nprotobuf>=4\n")
        (self.repo / "image.txt").write_text("pyproj==3.7.2\nprotobuf==5.29.6\n")
        result = self.cli("--python-version", "3.11", "--constraints", "image.txt", repo="kor-travel-concierge")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(self.cli("--python-version", "3.11", "--constraints", "image.txt").returncode, 1)
        self.assertEqual(self.cli("--python-version", "3.12", "--constraints", "image.txt", repo="kor-travel-concierge").returncode, 1)

    def test_compatible_postrelease_exact_and_ordering(self):
        python_fixture(self.repo, requires=">=3.12", deps=["python-dateutil>=2.8,<3"],
                       locked={"python-dateutil": "2.9.0.post0"})
        self.assertEqual(self.cli().returncode, 0)
        self.assertTrue(CV.below(CV.parse_version("2.9.0"), CV.parse_version("2.9.0.post0")))
        self.assertTrue(CV.below(CV.parse_version("2.9.0.post0"), CV.parse_version("2.9.0.post1")))
        self.assertTrue(CV.below(CV.parse_version("2.9.0.post1"), CV.parse_version("2.9.1")))
        self.assertFalse(CV.application_allows("==2.9.0", "2.9.0.post0"))

    def test_git_only_sdks_use_canonical_commit_and_matching_lock_not_pypi(self):
        for name in ("python-kasi-api", "python-krex-api", "python-vworld-api"):
            policy = self.registry.data["providers"]["packages"][name]
            for change in ("good", "old", "registry", "wrong_repo", "lock_old"):
                with self.subTest(name=name, change=change):
                    url = policy["repo"] + ".git"
                    ref = "a" * 40 if change == "old" else policy["ref"]
                    if change == "wrong_repo":
                        url += "-other"
                    deps = [f"{name}==0.1.0"] if change == "registry" else [f"{name} @ git+{url}@{ref}"]
                    python_fixture(self.repo, requires=">=3.12", deps=deps, locked={name: "0.1.0"})
                    lock = self.repo / "uv.lock"
                    text = lock.read_text()
                    if change != "registry":
                        actual = "b" * 40 if change == "lock_old" else ref
                        text = text.replace('source = { registry = "https://pypi.org/simple" }',
                                            f'source = {{ git = "{url}?rev={actual}#{actual}" }}')
                        lock.write_text(text)
                    result = self.cli()
                    self.assertEqual(result.returncode, 0 if change == "good" else 1,
                                     result.stdout + result.stderr)

    def test_git_archive_full_commit_is_valid_for_existing_requirements_path(self):
        policy = self.registry.data["providers"]["packages"]["python-vworld-api"]
        (self.repo / "requirements.txt").write_text(
            f"python-vworld-api @ {policy['repo']}/archive/{policy['ref']}.zip\n")
        self.assertEqual(self.cli().returncode, 0)


if __name__ == "__main__":
    unittest.main()
