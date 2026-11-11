# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"""프런트 버전 문서가 정본·생성 JSON과 따로 변하지 못하는 계약."""
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "tools/sync_frontend_policy.mjs"
START = "<!-- frontend-library-versions:start -->"
END = "<!-- frontend-library-versions:end -->"

@unittest.skipUnless(shutil.which("node"), "Node가 필요한 생성 계약")
class FrontendPolicyDocsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "tools").mkdir()
        shutil.copy2(SCRIPT, self.root / "tools/sync_frontend_policy.mjs")
        self.document = self.root / "docs/standards/frontend-libraries.md"
        self.document.parent.mkdir(parents=True)
        self.document.write_text("앞 설명\n" + START + "\n검토 중\n" + END + "\n뒤 설명\n", encoding="utf-8")
        self.registry = {
            "axes": {"react": {"ecosystem": "npm", "recommended": "19.3.1"}},
            "frontendPolicy": {"schema": 1, "packages": ["react"], "forbidden": [],
                "artifactPackages": [], "profiles": {"web": {"required": ["react"], "runtimeRequired": ["react"]}}}
        }
        self.save_registry()

    def save_registry(self):
        (self.root / "versions.json").write_text(json.dumps(self.registry), encoding="utf-8")

    def run_generator(self, check=False):
        return subprocess.run(["node", str(self.root / "tools/sync_frontend_policy.mjs"), *(["--check"] if check else [])],
                              cwd=self.root, text=True, capture_output=True)

    def patched_registry(self):
        self.registry["axes"]["fixture-engine"] = {"ecosystem": "npm",
            "packages": ["@radix-ui/react-focus-scope"], "exact": "1.1.0+focus.fixture",
            "recommended": None, "checked": False}
        policy = self.registry["frontendPolicy"]
        policy["packages"].append("@radix-ui/react-focus-scope")
        policy["artifactPackages"].append("@radix-ui/react-focus-scope")
        policy["patchedRadixPackages"] = ["@radix-ui/react-focus-scope"]
        return json.loads(json.dumps(self.registry))

    def test_patched_radix_generation_preserves_explicit_list_and_exact_axis(self):
        self.patched_registry(); self.save_registry()
        result = self.run_generator()
        self.assertEqual(result.returncode, 0, result.stderr)
        generated = json.loads((self.root / "frontend-dependencies.json").read_text())
        self.assertEqual(generated["patchedRadixPackages"], ["@radix-ui/react-focus-scope"])
        self.assertEqual(generated["versions"]["@radix-ui/react-focus-scope"], "1.1.0+focus.fixture")
        self.assertEqual(self.run_generator(check=True).returncode, 0)
        del generated["patchedRadixPackages"]
        (self.root / "frontend-dependencies.json").write_text(json.dumps(generated))
        self.assertNotEqual(self.run_generator(check=True).returncode, 0)

    def test_patched_radix_generation_absent_keeps_legacy_output(self):
        result = self.run_generator()
        self.assertEqual(result.returncode, 0, result.stderr)
        generated = json.loads((self.root / "frontend-dependencies.json").read_text())
        self.assertNotIn("patchedRadixPackages", generated)

    def test_patched_radix_invalid_registry_never_writes_generated_outputs(self):
        original = self.patched_registry()
        document = self.document.read_text()
        for change in ("null-list", "string-list", "duplicate", "object-entry", "adjacent", "subpath",
                       "wildcard", "newline", "empty-name", "artifact", "package", "axis",
                       "recommended", "checked", "empty-version", "range-version", "unknown-field"):
            with self.subTest(change=change):
                self.registry = json.loads(json.dumps(original))
                policy = self.registry["frontendPolicy"]; axis = self.registry["axes"]["fixture-engine"]
                engine = "@radix-ui/react-focus-scope"
                if change == "null-list": policy["patchedRadixPackages"] = None
                elif change == "string-list": policy["patchedRadixPackages"] = engine
                elif change == "duplicate": policy["patchedRadixPackages"].append(engine)
                elif change == "object-entry": policy["patchedRadixPackages"] = [{}]
                elif change == "artifact": policy["artifactPackages"] = []
                elif change == "package": policy["packages"].remove(engine)
                elif change == "axis": del self.registry["axes"]["fixture-engine"]
                elif change == "recommended": axis.pop("exact"); axis["recommended"] = "1.1.0"
                elif change == "checked": axis["checked"] = True
                elif change == "empty-version": axis["exact"] = ""
                elif change == "range-version": axis["exact"] = "^1.1.0"
                elif change == "unknown-field": policy["patchedRadixPackagesExtra"] = []
                else:
                    bad = {"adjacent":"@radix-uix/react-focus-scope", "subpath":engine+"/subpath",
                           "wildcard":"@radix-ui/react-*", "newline":engine+"\n", "empty-name":""}[change]
                    policy["patchedRadixPackages"] = [bad]
                    policy["artifactPackages"] = [bad]
                    policy["packages"] = ["react", bad]
                    axis["packages"] = [bad]
                self.save_registry()
                output = self.root / "frontend-dependencies.json"; output.unlink(missing_ok=True)
                self.document.write_text(document)
                result = self.run_generator()
                self.assertNotEqual(result.returncode, 0, result.stderr)
                self.assertFalse(output.exists())
                self.assertEqual(self.document.read_text(), document)

    def test_registry_change_requires_json_and_document_regeneration(self):
        first = self.run_generator()
        self.assertEqual(first.returncode, 0, first.stderr)
        self.registry["axes"]["react"]["recommended"] = "19.3.2"
        self.save_registry()
        self.assertNotEqual(self.run_generator(check=True).returncode, 0)
        regenerated = self.run_generator()
        self.assertEqual(regenerated.returncode, 0, regenerated.stderr)
        doc = self.document.read_text(encoding="utf-8")
        self.assertIn("| react | 19.3.2 |", doc)
        self.assertTrue(doc.startswith("앞 설명\n"))
        self.assertTrue(doc.endswith("\n뒤 설명\n"))
        self.assertEqual(json.loads((self.root / "frontend-dependencies.json").read_text())["versions"]["react"], "19.3.2")

    def test_document_only_drift_is_rejected(self):
        first = self.run_generator()
        self.assertEqual(first.returncode, 0, first.stderr)
        self.document.write_text("앞 설명\n" + START + "\n| react | 0.0.0 |\n" + END + "\n뒤 설명\n", encoding="utf-8")
        self.assertNotEqual(self.run_generator(check=True).returncode, 0)

    def test_missing_markers_never_overwrite_the_document(self):
        self.document.write_text("사람이 작성한 설명만 있음\n", encoding="utf-8")
        result = self.run_generator()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.document.read_text(encoding="utf-8"), "사람이 작성한 설명만 있음\n")

if __name__ == "__main__":
    unittest.main()
