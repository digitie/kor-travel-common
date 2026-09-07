# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"""consumer-manifest.v1 strict validator 회귀 시험."""

from __future__ import annotations

import json
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
        self.assertTrue(any("enforce" in error for error in errors))
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

    def test_lockfile_kind_and_path_are_strict(self):
        for kind, path in (("pipenv", "package-lock.json"), ("npm", "../package-lock.json"),
                           ("npm", "C:/package-lock.json")):
            data = valid_manifest()
            data["lockfiles"] = [{"kind": kind, "path": path, "scope": "root"}]
            errors = validate_manifest(data, {"kor-travel-map"})
            self.assertTrue(any("$.lockfiles[0]" in error for error in errors), (kind, path))

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


if __name__ == "__main__":
    unittest.main()
