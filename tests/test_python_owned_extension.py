# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"""실제 추가 49개 이름과 명시적 build 도구 범위의 유한한 회귀."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from test_check_versions import CV, SCRIPT, python_fixture

INPUTS = json.loads((Path(__file__).parent / "fixtures/owned-shared-python-20261120.json").read_text())


class OwnedExtensionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.repo = self.root / "consumer"
        self.repo.mkdir()
        self.registry = CV.Registry.load(SCRIPT.parents[1] / "versions.json")

    def cli(self, *args):
        return subprocess.run([sys.executable, "-B", str(SCRIPT), str(self.repo), "--repo",
                               "kor-travel-weather", "--strict-python-application", "--quiet",
                               "--no-step-summary", *args], text=True, capture_output=True)

    def lock(self, rows, requires=">=3.12"):
        python_fixture(self.repo, requires=requires, deps=["owned-anchor==1.0.0"],
                       locked={"owned-anchor": "1.0.0", **rows})

    def test_all_49_are_classified_and_old_values_cannot_hide_in_transitive_lock(self):
        self.assertEqual(len(INPUTS), 49)
        for name, row in INPUTS.items():
            with self.subTest(package=name):
                axis = self.registry.axes[name]
                self.assertEqual(axis["exact"], row["exact"])
                args = ("--python-build-tools",) if row["class"] == "build-tool" else ()
                rows = {name: row["exact"]}
                if name == "mcp":
                    rows["mcp-types"] = row["exact"]
                self.lock(rows)
                result = self.cli(*args)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.lock({**rows, name: "0.0.1"})
                self.assertEqual(self.cli(*args).returncode, 1)

    def test_build_tools_are_explicit_and_do_not_force_absent_setuptools_or_wheel(self):
        self.lock({"httpx": "0.28.1"})
        observed = self.root / "actual.json"
        observed.write_text(json.dumps({"python": "3.12.13", "packages": {"httpx": "0.28.1", "pip": "24.0"}}))
        self.assertEqual(self.cli("--installed-versions", str(observed)).returncode, 0)
        (self.repo / "build.txt").write_text("pip==26.3\n")
        self.assertEqual(self.cli("--python-build-tools", "--constraints", "build.txt",
                                  "--installed-versions", str(observed)).returncode, 1)
        observed.write_text(json.dumps({"python": "3.12.13", "packages": {"httpx": "0.28.1", "pip": "26.3"}}))
        self.lock({"httpx": "0.28.1", "pip": "26.3"})
        self.assertEqual(self.cli("--python-build-tools", "--constraints", "build.txt",
                                  "--installed-versions", str(observed)).returncode, 0)

    def test_dormant_mcp_constraint_does_not_force_mcp_companion_into_lock(self):
        self.lock({"httpx": "0.28.1"})
        (self.repo / "app.txt").write_text("mcp==2.3.0\nmcp-types==2.3.0\n")
        self.assertEqual(self.cli("--constraints", "app.txt").returncode, 0)

    def test_mcp2_requires_matching_actual_companion(self):
        for rows, expected in [({"mcp": "2.3.0"}, 1),
                               ({"mcp": "2.3.0", "mcp-types": "2.2.0"}, 1),
                               ({"mcp": "1.30.0", "mcp-types": "2.3.0"}, 1),
                               ({"mcp": "2.3.0", "mcp-types": "2.3.0"}, 0)]:
            self.lock(rows)
            self.assertEqual(self.cli().returncode, expected)

    def test_numpy_av_minimum_does_not_raise_common_sdk_or_accept_old_app_minimum(self):
        for name in ["numpy", "av"]:
            self.lock({name: INPUTS[name]["exact"]}, requires=">=3.11")
            self.assertEqual(self.cli("--python-version", "3.12.13").returncode, 1)
            self.lock({name: INPUTS[name]["exact"]}, requires=">=3.12")
            self.assertEqual(self.cli("--python-version", "3.12.13").returncode, 0)

    def test_httpx2_and_core2_old_equal_pins_are_both_rejected(self):
        for name in ["httpx2", "httpcore2"]:
            self.lock({"httpx2": "2.16.2", "httpcore2": "2.16.2", name: "2.16.0"})
            self.assertEqual(self.cli().returncode, 1)

    def test_build_profile_requires_application_mode_and_valid_class(self):
        result = subprocess.run([sys.executable, str(SCRIPT), str(self.repo), "--repo",
                                 "kor-travel-weather", "--python-build-tools"], capture_output=True)
        self.assertEqual(result.returncode, 2)
        for change in [{"buildTool": False}, {"application": True, "buildTool": True}]:
            data = json.loads((SCRIPT.parents[1] / "versions.json").read_text())
            data["axes"]["pip"].update(change)
            registry = self.root / "registry.json"
            registry.write_text(json.dumps(data))
            with self.assertRaises(ValueError):
                CV.Registry.load(registry)

    def test_new_python312_role_does_not_get_legacy_google_protobuf_pin(self):
        checker = CV.Checker(self.registry, "kor-travel-concierge", None)
        for python, protobuf, health in [("3.11.18", "5.29.6", "1.71.2"),
                                         ("3.12.13", "6.33.6", "1.81.2")]:
            checker.application_python = python
            self.assertEqual(checker.application_target(self.registry.axes["protobuf"])[0], protobuf)
            self.assertEqual(checker.application_target(self.registry.axes["grpcio-health-checking"])[0], health)

    def test_latest_aws_patch_pair_does_not_accept_previous_core(self):
        self.lock({"boto3": "1.44.7", "botocore": "1.44.6"})
        self.assertEqual(self.cli().returncode, 1)
        self.lock({"boto3": "1.44.7", "botocore": "1.44.7"})
        self.assertEqual(self.cli().returncode, 0)
