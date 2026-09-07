# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"""kt_contrast의 변환·쌍 판정·baseline 만료를 검증한다."""

from __future__ import annotations

from datetime import date, timedelta
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from tools.kt_contrast import contrast_ratio, parse_color


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "kt_contrast.py"
TOKENS = ROOT / "packages" / "tokens" / "tokens.css"


class ContrastTests(unittest.TestCase):
    def run_tool(self, *args: str | Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, "-B", "-X", "utf8", str(SCRIPT), *(str(arg) for arg in args)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )

    def test_oklch_matches_map_measurement(self):
        page = parse_color("oklch(97.8% 0.003 128)")
        tertiary = parse_color("oklch(54% 0.012 154)")
        self.assertAlmostEqual(contrast_ratio(tertiary, page), 4.73, delta=0.05)

    def test_canonical_light_and_dark_pass(self):
        for mode in ((), ("--dark",)):
            with self.subTest(mode=mode):
                result = self.run_tool(TOKENS, *mode, "--json")
                self.assertEqual(result.returncode, 0, result.stderr)
                payload = json.loads(result.stdout)
                self.assertEqual(payload["status"], "PASS")
                self.assertTrue(all(item["pass"] for item in payload["findings"]))

    def test_override_fails_control_line_pair(self):
        with tempfile.TemporaryDirectory(prefix="kt-contrast-") as directory:
            override = Path(directory) / "override.css"
            override.write_text(
                ":root { --kt-control-line: #aab5ad; --kt-surface-card: #fcfcf9; }\n",
                encoding="utf-8",
            )
            result = self.run_tool(TOKENS, override, "--json")
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            finding = next(item for item in payload["findings"] if item["pair"] == "control-line/surface-card")
            self.assertFalse(finding["pass"])
            self.assertAlmostEqual(finding["measured"], 2.06, delta=0.05)

    def test_expired_baseline_fails_and_active_baseline_passes(self):
        with tempfile.TemporaryDirectory(prefix="kt-contrast-") as directory:
            directory_path = Path(directory)
            override = directory_path / "override.css"
            override.write_text(":root { --kt-brand: oklch(64.6% 0.222 41.1); --kt-brand-foreground: #fff; }\n", encoding="utf-8")
            entry = {"pair": "brand-foreground/brand", "surface": "brand", "measured": 3.59, "required": 4.5}
            active = directory_path / "active.json"
            active.write_text(json.dumps({"version": 1, "entries": [{**entry, "until": str(date.today() + timedelta(days=1))}]}), encoding="utf-8")
            expired = directory_path / "expired.json"
            expired.write_text(json.dumps({"version": 1, "entries": [{**entry, "until": "2000-01-01"}]}), encoding="utf-8")
            active_result = self.run_tool(TOKENS, override, "--baseline", active, "--fail-new", "--json")
            expired_result = self.run_tool(TOKENS, override, "--baseline", expired, "--fail-new", "--json")
            self.assertEqual(active_result.returncode, 0, active_result.stderr)
            self.assertEqual(expired_result.returncode, 1, expired_result.stderr)
            self.assertEqual(json.loads(expired_result.stdout)["expired"][0]["until"], "2000-01-01")

    def test_step_summary_is_markdown(self):
        with tempfile.TemporaryDirectory(prefix="kt-contrast-") as directory:
            summary = Path(directory) / "summary.md"
            result = self.run_tool(TOKENS, "--step-summary", summary)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("kt_contrast", summary.read_text(encoding="utf-8"))

    def test_malformed_css_and_cycle_are_input_errors(self):
        with tempfile.TemporaryDirectory(prefix="kt-contrast-") as directory:
            directory_path = Path(directory)
            malformed = directory_path / "malformed.css"
            malformed.write_text(":root { --kt-brand: #fff;\n", encoding="utf-8")
            cycle = directory_path / "cycle.css"
            cycle.write_text(":root { --kt-brand: var(--kt-brand-foreground); --kt-brand-foreground: var(--kt-brand); }\n", encoding="utf-8")
            for path in (malformed, cycle):
                with self.subTest(path=path.name):
                    result = self.run_tool(TOKENS, path)
                    self.assertEqual(result.returncode, 2)


if __name__ == "__main__":
    unittest.main()
