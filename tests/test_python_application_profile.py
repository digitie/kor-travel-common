# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"""선택 application profile의 실제 CLI·lock/constraints·미사용 경계 회귀."""

import json
from datetime import date
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from test_check_versions import CV, SCRIPT, python_fixture, snapshot


CATALOG = SCRIPT.parents[1] / "versions.json"


class ApplicationProfileTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.repo = self.root / "consumer"
        self.repo.mkdir()
        self.registry = self.root / "versions.json"
        self.data = json.loads(CATALOG.read_text(encoding="utf-8"))
        self.registry.write_text(json.dumps(self.data))

    def cli(self, *extra, registry=None):
        return subprocess.run([sys.executable, str(SCRIPT), str(self.repo),
                               "--repo", "transport", "--registry",
                               str(registry or self.registry), "--strict-python-application",
                               "--no-step-summary", *extra], capture_output=True, text=True)

    def test_actual_cli_accepts_current_lock_and_keeps_consumer_readonly(self):
        python_fixture(self.repo, requires=">=3.11", deps=["sqlalchemy>=2.0,<3"],
                       locked={"sqlalchemy": "2.1.9"})
        before = snapshot(self.repo)
        output = self.root / "report.json"
        result = self.cli("--json", str(output))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        report = json.loads(output.read_text(encoding="utf-8"))
        self.assertEqual(report["selectedPythonApplication"]["runtimeImplementation"], "NOT_CHECKED")
        self.assertTrue(all(not row["installed"] for row in report["findings"]))
        self.assertEqual(snapshot(self.repo), before)

    def test_old_lock_conflicting_range_and_direct_url_fail_closed(self):
        for spec, locked in [("sqlalchemy>=2.0,<3", "2.0.52"),
                             ("sqlalchemy>=2.0,<2.1", "2.1.9"),
                             ("sqlalchemy!=2.1.*", "2.1.9"),
                             ("sqlalchemy<=2.1", "2.1.9"),
                             ("sqlalchemy @ https://example.invalid/wheel.whl", "2.1.9")]:
            with self.subTest(spec=spec, locked=locked):
                python_fixture(self.repo, requires=">=3.11", deps=[spec],
                               locked={"sqlalchemy": locked})
                self.assertEqual(self.cli().returncode, 1)

    def test_pydantic_core_pair_is_selected_without_new_direct_core_dependency(self):
        python_fixture(self.repo, requires=">=3.11", deps=["fastapi>=0.115"],
                       locked={"fastapi": "0.165.0", "pydantic": "2.14.4",
                               "pydantic-core": "2.50.5"})
        self.assertEqual(self.cli().returncode, 0)
        for version in [None, "2.46.5"]:
            with self.subTest(core=version):
                packages = {"fastapi": "0.165.0", "pydantic": "2.14.4"}
                if version:
                    packages["pydantic-core"] = version
                python_fixture(self.repo, requires=">=3.11", deps=["fastapi>=0.115"], locked=packages)
                self.assertEqual(self.cli().returncode, 1)

    def test_old_transitive_gap_is_rejected_without_forcing_unused_driver(self):
        python_fixture(self.repo, requires=">=3.11", deps=["httpx>=0.27"],
                       locked={"httpx": "0.28.1", "sqlalchemy": "2.0.54",
                               "psycopg2-binary": "2.9.13", "asyncpg": "0.31.0"})
        result = self.cli()
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("NOT_USED", result.stdout)
        self.assertIn("asyncpg", result.stdout)

    def test_no_lock_requires_exact_declaration_or_consumed_constraints(self):
        (self.repo / "requirements.txt").write_text("sqlalchemy>=2.0,<3\n")
        self.assertEqual(self.cli().returncode, 1)
        constraints = self.repo / "image-constraints.txt"
        constraints.write_text("sqlalchemy==2.1.9\n")
        self.assertEqual(self.cli("--constraints", "image-constraints.txt").returncode, 0)
        constraints.write_text("sqlalchemy==2.0.54\n")
        self.assertEqual(self.cli("--constraints", "image-constraints.txt").returncode, 1)
        (self.repo / "requirements.txt").write_text("sqlalchemy==2.1.9\n")
        self.assertEqual(self.cli().returncode, 0)

    def test_constraints_do_not_bypass_a_conflicting_manifest_or_second_old_constraint(self):
        python_fixture(self.repo, requires=">=3.11", deps=["sqlalchemy<2.1"], locked=None)
        (self.repo / "api.txt").write_text("sqlalchemy==2.1.9\n")
        self.assertEqual(self.cli("--constraints", "api.txt").returncode, 1)
        python_fixture(self.repo, requires=">=3.11", deps=["sqlalchemy>=2.0"], locked=None)
        (self.repo / "cs.txt").write_text("sqlalchemy==2.0.54\n")
        self.assertEqual(self.cli("--constraints", "api.txt", "--constraints", "cs.txt").returncode, 1)

    def test_requirements_include_and_nested_constraint_are_reused(self):
        (self.repo / "requirements.txt").write_text("-r dependencies.txt\n-c image.txt\n")
        (self.repo / "dependencies.txt").write_text("sqlalchemy>=2.0\n")
        (self.repo / "image.txt").write_text("sqlalchemy==2.1.9\n")
        self.assertEqual(self.cli().returncode, 0)

    def test_profile_fails_when_used_catalog_exact_is_missing(self):
        self.data["axes"]["sqlalchemy"].pop("exact", None)
        self.registry.write_text(json.dumps(self.data))
        python_fixture(self.repo, requires=">=3.11", deps=["sqlalchemy==2.1.9"], locked=None)
        self.assertEqual(self.cli().returncode, 2)

    def test_failure_json_markdown_and_annotation_match_exit(self):
        python_fixture(self.repo, requires=">=3.11", deps=["asyncpg>=0.30"],
                       locked={"asyncpg": "0.31.0"})
        output, markdown = self.root / "report.json", self.root / "report.md"
        result = self.cli("--json", str(output), "--markdown", str(markdown))
        self.assertEqual(result.returncode, 1)
        self.assertEqual(json.loads(output.read_text(encoding="utf-8"))["exit_code"], 1)
        self.assertIn("· exit 1", markdown.read_text(encoding="utf-8"))
        self.assertIn("::error title=check_versions::NOT_RECOMMENDED", result.stdout)

    def test_external_daemon_pin_is_not_an_application_sqlalchemy_exemption(self):
        (self.repo / "requirements.txt").write_text("sqlalchemy==2.0.54\n")
        self.assertEqual(self.cli().returncode, 1)
        source = (SCRIPT.parents[1] / "packages/py/kor-travel-common/pyproject.toml").read_text(encoding="utf-8")
        self.assertIn('"SQLAlchemy==2.0.54"', source)

    def test_poetry_source_pin_without_lock_and_caret_conflict(self):
        manifest = self.repo / "pyproject.toml"
        manifest.write_text('[tool.poetry]\nname="test"\nversion="0.1.0"\n'
                            '[tool.poetry.dependencies]\npython="^3.11"\nsqlalchemy="2.1.9"\n')
        self.assertEqual(self.cli().returncode, 0)
        manifest.write_text(manifest.read_text(encoding="utf-8").replace('sqlalchemy="2.1.9"', 'sqlalchemy="^2.0"'))
        self.assertEqual(self.cli().returncode, 1)
        (self.repo / "image.txt").write_text("sqlalchemy==2.1.9\n")
        self.assertEqual(self.cli("--constraints", "image.txt").returncode, 0)

    def test_common_immutable_ref_and_lock_must_bind_current_package_tree(self):
        provider = self.data["providers"]["packages"]["kor-travel-common"]
        ref = provider["ref"]
        url = f"git+{provider['repo']}.git@{ref}#subdirectory=packages/py/kor-travel-common"
        resolved = f"{provider['repo']}.git?subdirectory=packages%2Fpy%2Fkor-travel-common&rev={ref}#{ref}"
        python_fixture(self.repo, requires=">=3.11", deps=[f"kor-travel-common[http] @ {url}"],
                       locked={}, git_locked={"kor-travel-common": ("0.1.0.dev0", resolved)})
        self.assertEqual(self.cli().returncode, 0)
        for bad in [url.removeprefix("git+"),
                    url.replace("#subdirectory=", "?subdirectory=packages/py/kor-travel-common#subdirectory=other/"),
                    url.replace(ref, "main"), url.replace("github.com", "example.invalid"),
                    url.replace(ref, "344d91c0eec4b605e007e61ce248693a729d692d")]:
            with self.subTest(url=bad):
                python_fixture(self.repo, requires=">=3.11", deps=[f"kor-travel-common @ {bad}"],
                               locked={}, git_locked={"kor-travel-common": ("0.1.0.dev0", resolved)})
                self.assertEqual(self.cli().returncode, 1)

    def test_common_byte_equal_other_ref_is_accepted_with_local_object_proof(self):
        # 얕은 CI checkout의 과거 object 유무와 무관한 실제 Git tree 증거를 만든다.
        authority = self.root / "authority"
        authority.mkdir()
        def git(*args):
            return subprocess.check_output([
                "git", "-c", "user.name=fixture", "-c", "user.email=fixture@example.invalid",
                "-c", "commit.gpgsign=false", "-c", "core.hooksPath=" + str(authority / "no-hooks"),
                "-C", str(authority), *args], text=True).strip()
        git("init", "-q")
        package = authority / "packages/py/kor-travel-common"
        package.mkdir(parents=True)
        (package / "marker").write_text("같은 package bytes", encoding="utf-8")
        git("add", "packages/py/kor-travel-common/marker")
        git("commit", "-qm", "fixture")
        canonical = git("rev-parse", "HEAD")
        tree = git("rev-parse", "HEAD:packages/py/kor-travel-common")
        (authority / "outside").write_text("package 밖의 변경", encoding="utf-8")
        git("add", "outside")
        git("commit", "-qm", "outside")
        ref = git("rev-parse", "HEAD")
        data = json.loads(CATALOG.read_text(encoding="utf-8"))
        data["providers"]["packages"]["kor-travel-common"].update(ref=canonical, packageTree=tree)
        registry = authority / "versions.json"
        registry.write_text(json.dumps(data))
        url = f"git+https://github.com/digitie/kor-travel-common.git@{ref}#subdirectory=packages/py/kor-travel-common"
        python_fixture(self.repo, requires=">=3.11", deps=[f"kor-travel-common @ {url}"], locked=None)
        before = snapshot(authority)
        result = self.cli(registry=registry)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(snapshot(authority), before)
        (package / "marker").write_text("다른 package bytes", encoding="utf-8")
        git("add", "packages/py/kor-travel-common/marker")
        git("commit", "-qm", "different")
        bad = git("rev-parse", "HEAD")
        python_fixture(self.repo, requires=">=3.11", deps=[f"kor-travel-common @ {url.replace(ref, bad)}"], locked=None)
        self.assertEqual(self.cli(registry=registry).returncode, 1)

    def test_missing_alternate_common_object_fails_closed(self):
        url = ("git+https://github.com/digitie/kor-travel-common.git@" + "b" * 40
               + "#subdirectory=packages/py/kor-travel-common")
        python_fixture(self.repo, requires=">=3.11", deps=[f"kor-travel-common @ {url}"], locked=None)
        self.assertEqual(self.cli().returncode, 1)

    def test_existing_floor_and_psycopg_only_modes_remain_independent(self):
        registry = CV.Registry.load(self.registry)
        checker = CV.Checker(registry, "kor-travel-transport", date(2026, 11, 20))
        self.assertEqual(checker.judge("sqlalchemy", (2, 0, 52))[0], "OK")
        self.assertEqual(checker.judge("asyncpg", (0, 31, 0))[0], "OK")
        python_fixture(self.repo, requires=">=3.11", deps=["asyncpg==0.31.0"],
                       locked={"asyncpg": "0.31.0"})
        result = subprocess.run([sys.executable, str(SCRIPT), str(self.repo), "--repo", "transport",
                                 "--registry", str(self.registry), "--strict-psycopg", "--no-step-summary"],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_all_selected_axes_exact_lock_and_poetry_locked_evidence(self):
        targets = {name: self.data["axes"][name]["exact"] for name in CV.APPLICATION_AXES}
        python_fixture(self.repo, requires=">=3.11", deps=[f"{name}=={version}" for name, version in targets.items()],
                       locked=targets)
        self.assertEqual(self.cli().returncode, 0)
        # 다른 범위의 실제 Poetry lock도 기존 strict parser로 검사한다.
        (self.repo / "uv.lock").unlink()
        (self.repo / "pyproject.toml").write_text('[tool.poetry]\nname="test"\nversion="0.1.0"\n'
            '[tool.poetry.dependencies]\npython="^3.11"\nsqlalchemy="^2.0"\n')
        (self.repo / "poetry.lock").write_text('[[package]]\nname="sqlalchemy"\nversion="2.1.9"\n'
            'description="fixture"\noptional=false\npython-versions=">=3.11"\nfiles=[]\n'
            '[metadata]\nlock-version="2.1"\npython-versions="^3.11"\ncontent-hash="fixture"\n')
        self.assertEqual(self.cli().returncode, 0)
        lock = self.repo / "poetry.lock"
        lock.write_text(lock.read_text(encoding="utf-8").replace('version="2.1.9"', 'version="2.0.54"'))
        self.assertEqual(self.cli().returncode, 1)

    def test_dormant_constraints_validate_pins_without_requiring_installs(self):
        (self.repo / "requirements.txt").write_text("httpx==0.28.1\n")
        (self.repo / "image.txt").write_text("sqlalchemy==2.0.54\nasyncpg==0.31.0\npsycopg==3.3.6\n")
        self.assertEqual(self.cli("--constraints", "image.txt").returncode, 1)
        (self.repo / "image.txt").write_text("sqlalchemy==2.1.9\nasyncpg==0.32.0\npsycopg==3.3.9\n")
        installed = self.root / "native.json"
        installed.write_text(json.dumps({"python": "3.12.1", "packages": {"httpx": "0.28.1"}}))
        self.assertEqual(self.cli("--constraints", "image.txt", "--installed-versions", str(installed)).returncode, 0)

    def test_application_does_not_silently_select_the_external_daemon_extra(self):
        provider = self.data["providers"]["packages"]["kor-travel-common"]
        url = (f"git+{provider['repo']}.git@{provider['ref']}"
               "#subdirectory=packages/py/kor-travel-common")
        python_fixture(self.repo, requires=">=3.11",
                       deps=[f"kor-travel-common[daemon-pool] @ {url}", "sqlalchemy==2.1.9"], locked=None)
        self.assertEqual(self.cli().returncode, 1)

    def test_constraint_escape_and_cycle_fail_closed(self):
        (self.repo / "requirements.txt").write_text("sqlalchemy>=2.0\n")
        (self.root / "outside.txt").write_text("sqlalchemy==2.1.9\n")
        self.assertEqual(self.cli("--constraints", "../outside.txt").returncode, 2)
        (self.repo / "a.txt").write_text("-c b.txt\n")
        (self.repo / "b.txt").write_text("-c a.txt\n")
        self.assertEqual(self.cli("--constraints", "a.txt").returncode, 2)

    def test_common_git_object_proof_disables_lazy_fetch_and_optional_writes(self):
        registry = CV.Registry.load(self.registry)
        checker = CV.Checker(registry, "kor-travel-transport", date(2026, 11, 20),
                             strict_python_application=True)
        policy = self.data["providers"]["packages"]["kor-travel-common"]
        url = ("git+" + policy["repo"] + ".git@" + "a" * 40
               + "#subdirectory=packages/py/kor-travel-common")
        scope = CV.Scope("python", ".", self.repo / "pyproject.toml", None)
        result = subprocess.CompletedProcess([], 0, stdout=policy["packageTree"] + "\n", stderr="")
        with patch.object(CV.subprocess, "run", return_value=result) as run:
            checker.check_application_common(scope, {"kor-travel-common": [""]},
                                               {"kor-travel-common": [url]}, {})
        self.assertEqual(run.call_args.kwargs.get("env", {}).get("GIT_NO_LAZY_FETCH"), "1")
        self.assertEqual(run.call_args.kwargs.get("env", {}).get("GIT_OPTIONAL_LOCKS"), "0")


if __name__ == "__main__":
    unittest.main()
