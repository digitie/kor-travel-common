# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"""consumer-manifest.v1 strict validator 회귀 시험."""

from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from tools.manifest_schema import validate_manifest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "validate_manifest.py"
REGISTRY = ROOT / "versions.json"


def valid_manifest() -> dict:
    return {
        "schema": "kor-travel-common.consumer-manifest.v1",
        "repo": "kor-travel-map",
        "app": "admin",
        "tokens": {"version": None, "override": None},
        "ui": {"version": None},
        "python": {"version": None},
        "lockfiles": [{"kind": "npm", "path": "package-lock.json", "scope": "root"}],
        "contrast": {"baseline": None, "dark": False},
        "ux_gate": {"baseline": None},
        "openapi": {"exceptions": ["docs/standards/openapi-exceptions.yaml#map"]},
        "exceptions": [],
    }


class ValidateManifestTests(unittest.TestCase):
    def run_cli(self, data: dict) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory(prefix="kor-travel-common-manifest-") as directory:
            path = Path(directory) / "kor-travel-common.lock.json"
            path.write_text(json.dumps(data), encoding="utf-8")
            return subprocess.run(
                [sys.executable, "-B", "-X", "utf8", str(SCRIPT), str(path), "--registry", str(REGISTRY)],
                capture_output=True,
                text=True,
                encoding="utf-8",
            )

    def test_all_initial_manifests_pass(self):
        manifests = sorted((ROOT / "templates" / "manifests").glob("*.lock.json"))
        self.assertEqual(len(manifests), 10)
        for path in manifests:
            with self.subTest(path=path.name):
                result = subprocess.run(
                    [sys.executable, "-B", "-X", "utf8", str(SCRIPT), str(path), "--registry", str(REGISTRY)],
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                )
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_valid_manifest_passes(self):
        self.assertEqual(validate_manifest(valid_manifest(), {"kor-travel-map"}), [])
        result = self.run_cli(valid_manifest())
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_unknown_field_and_enforce_are_rejected(self):
        data = valid_manifest()
        data["enforce"] = "report"
        data["tokens"]["future"] = True
        errors = validate_manifest(data, {"kor-travel-map"})
        self.assertTrue(any("$." in error and "미지 필드" in error for error in errors))
        self.assertTrue(any("$.tokens" in error for error in errors))
        self.assertEqual(self.run_cli(data).returncode, 1)

    def test_until_is_required_and_must_be_a_real_date(self):
        for until in (None, "2026/12/31", "2026-02-30"):
            data = valid_manifest()
            data["exceptions"] = [{
                "rule": "UX-G7.1",
                "surface": "login",
                "reason": "시험",
                "until": until,
                "review": "2026-09-30",
            }]
            errors = validate_manifest(data, {"kor-travel-map"})
            self.assertTrue(any("$.exceptions[0].until" in error for error in errors), until)

    def test_review_is_required_and_must_be_a_real_date(self):
        for review in (None, "tomorrow", "2026/09/30", "2026-02-30"):
            data = valid_manifest()
            data["exceptions"] = [{
                "key": "react",
                "reason": "시험",
                "until": "2026-12-31",
                "review": review,
            }]
            errors = validate_manifest(data, {"kor-travel-map"})
            self.assertTrue(any("$.exceptions[0].review" in error for error in errors), review)

    def test_lockfile_kind_and_path_are_strict(self):
        for kind, path in (("pipenv", "package-lock.json"), ("npm", "../package-lock.json"),
                           ("npm", "C:/package-lock.json")):
            data = valid_manifest()
            data["lockfiles"] = [{"kind": kind, "path": path, "scope": "root"}]
            errors = validate_manifest(data, {"kor-travel-map"})
            self.assertTrue(any("$.lockfiles[0]" in error for error in errors), (kind, path))

    def test_kind_non_string_values_return_errors_without_traceback(self):
        for kind in ([], {}, None, True, 7):
            data = valid_manifest()
            data["lockfiles"] = [{"kind": kind, "path": "package-lock.json", "scope": "root"}]
            with self.subTest(kind=kind):
                errors = validate_manifest(data, {"kor-travel-map"})
                self.assertTrue(any("$.lockfiles[0].kind" in error for error in errors))
                result = self.run_cli(data)
                self.assertEqual(result.returncode, 1)
                self.assertNotIn("Traceback", result.stderr)

    def test_unknown_field_does_not_echo_input(self):
        data = valid_manifest()
        marker = "opaque_input_" + "A" * 36
        data[marker] = True
        errors = validate_manifest(data, {"kor-travel-map"})
        self.assertTrue(errors)
        self.assertNotIn(marker, "\n".join(errors))
        result = self.run_cli(data)
        self.assertEqual(result.returncode, 1)
        self.assertNotIn(marker, result.stdout + result.stderr)

    def test_schema_path_edge_cases_are_rejected(self):
        for path in ("C:/package-lock.json", "apps//package-lock.json", "apps/",
                     " ", "apps/\x00/package-lock.json", "apps/\t/package-lock.json",
                     "apps/\n/package-lock.json", "apps/\x7f/package-lock.json",
                     "apps/package-lock.json\n"):
            data = valid_manifest()
            data["lockfiles"] = [{"kind": "npm", "path": path, "scope": "root"}]
            with self.subTest(path=path):
                self.assertTrue(validate_manifest(data, {"kor-travel-map"}))

    def test_json_schema_rejects_control_character_paths_like_stdlib(self):
        try:
            from jsonschema import Draft202012Validator
        except ImportError:
            self.skipTest("jsonschema 미설치")
        schema = json.loads((ROOT / "templates" / "kor-travel-common.lock.schema.json").read_text(encoding="utf-8"))
        validator = Draft202012Validator(schema)
        for path in ("apps/\t/package-lock.json", "apps/\n/package-lock.json",
                     "apps/\x1f/package-lock.json", "apps/\x7f/package-lock.json"):
            data = valid_manifest()
            data["lockfiles"] = [{"kind": "npm", "path": path, "scope": "root"}]
            with self.subTest(path=path):
                self.assertTrue(list(validator.iter_errors(data)))

    def test_repo_must_be_a_versions_consumer_key(self):
        data = valid_manifest()
        data["repo"] = "map"
        errors = validate_manifest(data, {"kor-travel-map"})
        self.assertTrue(any("$.repo" in error for error in errors))

    def test_missing_required_field_is_rejected(self):
        data = valid_manifest()
        del data["ux_gate"]
        errors = validate_manifest(data, {"kor-travel-map"})
        self.assertTrue(any("$.ux_gate" in error for error in errors))

    def test_key_exception_variant_is_supported(self):
        data = valid_manifest()
        data["exceptions"] = [{
            "key": "react",
            "reason": "React 18 유지",
            "until": "2026-12-31",
            "review": "2026-09-30",
        }]
        self.assertEqual(validate_manifest(data, {"kor-travel-map"}), [])

    def test_check_versions_uses_explicit_repository_root(self):
        with tempfile.TemporaryDirectory(prefix="kor-travel-common-root-") as directory:
            root = Path(directory)
            manifest = root / "templates" / "manifests" / "map.lock.json"
            manifest.parent.mkdir(parents=True)
            manifest.write_text(json.dumps(valid_manifest()), encoding="utf-8")
            (root / "package.json").write_text(json.dumps({
                "name": "fixture",
                "version": "0.0.0",
                "engines": {"node": ">=22.12"},
                "dependencies": {"react": "^19.0.0"},
            }), encoding="utf-8")
            (root / "package-lock.json").write_text(json.dumps({
                "name": "fixture",
                "lockfileVersion": 3,
                "packages": {
                    "": {"name": "fixture", "version": "0.0.0", "engines": {"node": ">=22.12"},
                         "dependencies": {"react": "^19.0.0"}},
                    "node_modules/react": {"version": "19.2.8"},
                },
            }), encoding="utf-8")
            result = subprocess.run([
                sys.executable, "-B", "-X", "utf8", str(ROOT / "tools" / "check_versions.py"),
                str(root), "--manifest", str(manifest), "--repo", "kor-travel-map",
                "--today", "2026-09-07", "--quiet", "--no-step-summary",
            ], capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertNotIn("검사 대상 scope가 없음", result.stdout)

    def test_check_versions_selects_workspace_manifest(self):
        with tempfile.TemporaryDirectory(prefix="kor-travel-common-workspace-") as directory:
            root = Path(directory)
            app = root / "apps" / "web"
            app.mkdir(parents=True)
            manifest = root / "apps" / "web" / "kor-travel-common.lock.json"
            data = valid_manifest()
            data["app"] = "apps/web"
            data["lockfiles"] = [{"kind": "npm", "path": "package-lock.json", "scope": "apps/web"}]
            manifest.write_text(json.dumps(data), encoding="utf-8")
            (root / "package.json").write_text(json.dumps({
                "name": "fixture-root",
                "version": "0.0.0",
                "workspaces": ["apps/*"],
                "engines": {"node": ">=22.12.0"},
                "dependencies": {"react": "^19.0.0"},
            }), encoding="utf-8")
            (app / "package.json").write_text(json.dumps({
                "name": "fixture-web",
                "version": "0.0.0",
                "engines": {"node": ">=18.0.0"},
                "dependencies": {"react": "^19.0.0"},
            }), encoding="utf-8")
            (root / "package-lock.json").write_text(json.dumps({
                "name": "fixture-root",
                "lockfileVersion": 3,
                "packages": {
                    "": {"name": "fixture-root", "version": "0.0.0",
                         "engines": {"node": ">=22.12.0"},
                         "workspaces": ["apps/*"], "dependencies": {"react": "^19.0.0"}},
                    "apps/web": {"name": "fixture-web", "version": "0.0.0",
                                  "engines": {"node": ">=18.0.0"},
                                  "dependencies": {"react": "^19.0.0"}},
                    "node_modules/react": {"version": "19.2.8"},
                },
            }), encoding="utf-8")
            result = subprocess.run([
                sys.executable, "-B", "-X", "utf8", str(ROOT / "tools" / "check_versions.py"),
                str(root), "--manifest", str(manifest), "--repo", "kor-travel-map",
                "--mode", "fail", "--today", "2026-09-07", "--no-step-summary",
            ], capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("apps/web", result.stdout)
            self.assertIn("BELOW_FLOOR", result.stdout)

    def test_sensitive_workspace_path_is_redacted_from_all_report_channels(self):
        with tempfile.TemporaryDirectory(prefix="kor-travel-common-workspace-redaction-") as directory:
            root = Path(directory)
            marker = "secret_workspace_value12345678"
            member = root / marker
            member.mkdir(parents=True)
            manifest = root / "manifest.json"
            data = valid_manifest()
            data["lockfiles"] = [{"kind": "npm", "path": "package-lock.json", "scope": marker}]
            manifest.write_text(json.dumps(data), encoding="utf-8")
            (member / "package.json").write_text(json.dumps({
                "name": "fixture-member", "version": "0.0.0",
                "engines": {"node": ">=22.12.0"}, "dependencies": {"react": "^19.0.0"},
            }), encoding="utf-8")
            (root / "package-lock.json").write_text(json.dumps({
                "name": "fixture-root", "lockfileVersion": 3,
                "packages": {
                    "": {"name": "fixture-root", "version": "0.0.0"},
                    marker: {"name": "fixture-member", "version": "0.0.0",
                             "engines": {"node": ">=22.12.0"},
                             "dependencies": {"react": "^19.0.0"}},
                    f"{marker}/node_modules/react": {"version": "19.2.8"},
                },
            }), encoding="utf-8")
            output = root / "report"
            json_path = output.with_suffix(".json")
            markdown_path = output.with_suffix(".md")
            summary_path = output.with_name("summary.md")
            env = dict(os.environ)
            env["GITHUB_STEP_SUMMARY"] = str(summary_path)
            result = subprocess.run([
                sys.executable, "-B", "-X", "utf8", str(ROOT / "tools" / "check_versions.py"),
                str(root), "--manifest", str(manifest), "--repo", "kor-travel-map",
                "--mode", "fail", "--json", str(json_path), "--markdown", str(markdown_path),
            ], capture_output=True, text=True, encoding="utf-8", env=env)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            for path in (json_path, markdown_path, summary_path):
                self.assertNotIn(marker, path.read_text(encoding="utf-8"))
            self.assertNotIn(marker, result.stdout + result.stderr)

    def test_check_versions_rejects_companion_manifest_symlink_escape(self):
        with tempfile.TemporaryDirectory(prefix="kor-travel-common-symlink-") as directory:
            root = Path(directory)
            outside = root.parent / f"{root.name}-outside-package.json"
            outside.write_text(json.dumps({
                "name": "outside", "version": "0.0.0", "engines": {"node": ">=22.12.0"},
            }), encoding="utf-8")
            try:
                (root / "package.json").symlink_to(outside)
            finally:
                outside.unlink(missing_ok=True)
            (root / "package-lock.json").write_text(json.dumps({
                "name": "fixture", "lockfileVersion": 3,
                "packages": {"": {"name": "fixture", "version": "0.0.0"}},
            }), encoding="utf-8")
            manifest = root / "manifest.json"
            manifest.write_text(json.dumps(valid_manifest()), encoding="utf-8")
            result = subprocess.run([
                sys.executable, "-B", "-X", "utf8", str(ROOT / "tools" / "check_versions.py"),
                str(root), "--manifest", str(manifest), "--repo", "kor-travel-map",
                "--mode", "fail", "--no-step-summary",
            ], capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
            self.assertNotIn(str(outside), result.stdout + result.stderr)

    def test_empty_lockfiles_report_declaration_only_app(self):
        with tempfile.TemporaryDirectory(prefix="kor-travel-common-etl-") as directory:
            root = Path(directory)
            app = root / "apps" / "etl"
            app.mkdir(parents=True)
            manifest = app / "kor-travel-common.lock.json"
            data = valid_manifest()
            data["repo"] = "pinvi"
            data["app"] = "apps/etl"
            data["lockfiles"] = []
            manifest.write_text(json.dumps(data), encoding="utf-8")
            (app / "pyproject.toml").write_text(
                "[project]\nname = 'fixture-etl'\nversion = '0.0.0'\ndependencies = []\n",
                encoding="utf-8",
            )
            result = subprocess.run([
                sys.executable, "-B", "-X", "utf8", str(ROOT / "tools" / "check_versions.py"),
                str(root), "--manifest", str(manifest), "--repo", "pinvi",
                "--mode", "fail", "--today", "2026-09-07", "--no-step-summary",
            ], capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("NO_LOCK", result.stdout)

    def test_requirements_include_cannot_escape_consumer_root(self):
        with tempfile.TemporaryDirectory(prefix="kor-travel-common-requirements-root-") as directory:
            root = Path(directory)
            app = root / "apps" / "etl"
            app.mkdir(parents=True)
            manifest = app / "kor-travel-common.lock.json"
            data = valid_manifest()
            data["repo"] = "pinvi"
            data["app"] = "apps/etl"
            data["lockfiles"] = []
            manifest.write_text(json.dumps(data), encoding="utf-8")
            (app / "requirements.txt").write_text(
                "-r ../../../outside-requirements.txt\n", encoding="utf-8")
            outside = root.parent / "outside-requirements.txt"
            outside.write_text("fastapi==0.1.0\n", encoding="utf-8")
            try:
                result = subprocess.run([
                    sys.executable, "-B", "-X", "utf8", str(ROOT / "tools" / "check_versions.py"),
                    str(root), "--manifest", str(manifest), "--repo", "pinvi",
                    "--mode", "fail", "--no-step-summary",
                ], capture_output=True, text=True, encoding="utf-8")
            finally:
                outside.unlink(missing_ok=True)
            self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
            self.assertNotIn("outside-requirements", result.stdout + result.stderr)
            self.assertNotIn("fastapi", result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
