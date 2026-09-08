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

    def test_oklch_chroma_percent_matches_numeric(self):
        self.assertAlmostEqual(
            contrast_ratio(parse_color("oklch(56% 25% 135)"), parse_color("#fff")),
            contrast_ratio(parse_color("oklch(56% 0.1 135)"), parse_color("#fff")),
            delta=1e-9,
        )

    def test_alpha_uses_srgb_source_over(self):
        self.assertAlmostEqual(contrast_ratio(parse_color("#ffffff33"), parse_color("#000")), 1.6621, delta=0.01)

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

    def test_light_selector_and_quoted_text_do_not_override_tokens(self):
        with tempfile.TemporaryDirectory(prefix="kt-contrast-") as directory:
            override = Path(directory) / "override.css"
            override.write_text(
                ':root:not(.dark) { --kt-brand: #fff; --kt-brand-foreground: #fff; content: "--kt-brand: #000;"; }\n',
                encoding="utf-8",
            )
            result = self.run_tool(TOKENS, override, "--fail-new", "--json")
            self.assertEqual(result.returncode, 1)
            payload = json.loads(result.stdout)
            finding = next(item for item in payload["findings"] if item["pair"] == "brand-foreground/brand")
            self.assertFalse(finding["pass"])

    def test_equivalent_root_selector_order_and_attribute_quotes_are_applied(self):
        cases = (
            (".dark:root { --kt-brand: #fff; --kt-brand-foreground: #fff; }\n", ("--dark",)),
            ("[data-theme='light'] { --kt-brand: #fff; --kt-brand-foreground: #fff; }\n", ()),
        )
        with tempfile.TemporaryDirectory(prefix="kt-contrast-") as directory:
            for index, (source, mode) in enumerate(cases):
                with self.subTest(index=index):
                    override = Path(directory) / f"equivalent-{index}.css"
                    override.write_text(source, encoding="utf-8")
                    result = self.run_tool(TOKENS, override, *mode, "--fail-new", "--json")
                    self.assertEqual(result.returncode, 1, result.stderr)
                    finding = next(
                        item for item in json.loads(result.stdout)["findings"] if item["pair"] == "brand-foreground/brand"
                    )
                    self.assertFalse(finding["pass"])

    def test_unsupported_token_selector_is_an_input_error(self):
        with tempfile.TemporaryDirectory(prefix="kt-contrast-") as directory:
            override = Path(directory) / "unsupported.css"
            override.write_text(".theme-root { --kt-brand: #fff; --kt-brand-foreground: #fff; }\n", encoding="utf-8")
            result = self.run_tool(TOKENS, override, "--json")
            self.assertEqual(result.returncode, 2)

    def test_selector_values_keep_case_and_quoted_spaces(self):
        with tempfile.TemporaryDirectory(prefix="kt-contrast-") as directory:
            for index, selector in enumerate((":root:where( .dark )", ".DARK", "[data-theme='d ark']")):
                with self.subTest(selector=selector):
                    override = Path(directory) / f"unsupported-{index}.css"
                    override.write_text(
                        f":root {{ --kt-brand: #fff; --kt-brand-foreground: #fff; }}\n{selector} {{ --kt-brand: #000; }}\n",
                        encoding="utf-8",
                    )
                    result = self.run_tool(TOKENS, override, "--dark", "--json")
                    self.assertEqual(result.returncode, 2)

    def test_css_scope_and_media_boundaries_are_explicit(self):
        with tempfile.TemporaryDirectory(prefix="kt-contrast-") as directory:
            override = Path(directory) / "override.css"
            override.write_text(
                ':root { --kt-brand: #fff; --kt-brand-foreground: #fff; content: "/* --kt-brand: #000; */"; }\n'
                '.dark .button { --kt-brand: #000; --kt-brand-foreground: #fff; }\n'
                '@media   ( prefers-color-scheme : dark ) { :root { --kt-brand: #000; --kt-brand-foreground: #fff; } }\n',
                encoding="utf-8",
            )
            light = self.run_tool(TOKENS, override, "--fail-new", "--json")
            dark = self.run_tool(TOKENS, override, "--dark", "--fail-new", "--json")
            self.assertEqual(light.returncode, 1)
            self.assertEqual(dark.returncode, 1, dark.stderr)
            light_payload = json.loads(light.stdout)
            dark_payload = json.loads(dark.stdout)
            light_brand = next(item for item in light_payload["findings"] if item["pair"] == "brand-foreground/brand")
            dark_brand = next(item for item in dark_payload["findings"] if item["pair"] == "brand-foreground/brand")
            self.assertFalse(light_brand["pass"])
            self.assertTrue(dark_brand["pass"])

    def test_unsupported_condition_is_input_error(self):
        with tempfile.TemporaryDirectory(prefix="kt-contrast-") as directory:
            override = Path(directory) / "override.css"
            override.write_text("@media (max-width: 1px) { :root { --kt-brand: #fff; } }\n", encoding="utf-8")
            result = self.run_tool(TOKENS, override)
            self.assertEqual(result.returncode, 2)

    def test_media_negation_and_nested_blocks_are_input_errors(self):
        with tempfile.TemporaryDirectory(prefix="kt-contrast-") as directory:
            directory_path = Path(directory)
            negated = directory_path / "negated.css"
            negated.write_text("@media not all and (prefers-color-scheme: dark) { :root { --kt-brand: #fff; } }\n", encoding="utf-8")
            compound = directory_path / "compound.css"
            compound.write_text("@media (prefers-color-scheme: dark) and (min-width: 1px) { :root { --kt-brand: #fff; } }\n", encoding="utf-8")
            nested = directory_path / "nested.css"
            nested.write_text(":root { .child { --kt-brand: #fff; } }\n", encoding="utf-8")
            for path in (negated, compound, nested):
                with self.subTest(path=path.name):
                    result = self.run_tool(TOKENS, path)
                    self.assertEqual(result.returncode, 2, result.stderr)

    def test_media_and_selector_modes_intersect(self):
        with tempfile.TemporaryDirectory(prefix="kt-contrast-") as directory:
            directory_path = Path(directory)
            contradictory = directory_path / "contradictory.css"
            contradictory.write_text(
                ":root { --kt-brand: #fff; --kt-brand-foreground: #fff; }\n"
                "@media (prefers-color-scheme: dark) { :root:not(.dark) { --kt-brand: #000; } }\n",
                encoding="utf-8",
            )
            nested = directory_path / "nested-media.css"
            nested.write_text(
                "@media (prefers-color-scheme: light) { @media (prefers-color-scheme: dark) { :root { --kt-brand: #fff; --kt-brand-foreground: #fff; } } }\n",
                encoding="utf-8",
            )
            for mode in ((), ("--dark",)):
                with self.subTest(mode=mode):
                    result = self.run_tool(TOKENS, contradictory, "--fail-new", "--json", *mode)
                    self.assertEqual(result.returncode, 1)
                    nested_result = self.run_tool(TOKENS, nested, "--fail-new", "--json", *mode)
                    self.assertEqual(nested_result.returncode, 0, nested_result.stderr)
            root_dark = directory_path / "root-dark.css"
            root_dark.write_text(":root.dark { --kt-brand: #fff; --kt-brand-foreground: #fff; }\n", encoding="utf-8")
            result = self.run_tool(TOKENS, root_dark, "--dark", "--fail-new", "--json")
            self.assertEqual(result.returncode, 1)
            finding = next(item for item in json.loads(result.stdout)["findings"] if item["pair"] == "brand-foreground/brand")
            self.assertFalse(finding["pass"])

    def test_muted_read_surface_is_explicit(self):
        with tempfile.TemporaryDirectory(prefix="kt-contrast-") as directory:
            override = Path(directory) / "override.css"
            override.write_text(
                ":root { --kt-surface-muted: #111; --kt-text-primary: #111; }\n",
                encoding="utf-8",
            )
            result = self.run_tool(TOKENS, override, "--read-surface", "muted", "--fail-new", "--json")
            self.assertEqual(result.returncode, 1)
            payload = json.loads(result.stdout)
            finding = next(item for item in payload["findings"] if item["pair"] == "text-primary/surface-muted")
            self.assertFalse(finding["pass"])

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
            extra_close = directory_path / "extra-close.css"
            extra_close.write_text(":root { --kt-brand: #fff; } }\n", encoding="utf-8")
            cycle = directory_path / "cycle.css"
            cycle.write_text(":root { --kt-brand: var(--kt-brand-foreground); --kt-brand-foreground: var(--kt-brand); }\n", encoding="utf-8")
            for path in (malformed, extra_close, cycle):
                with self.subTest(path=path.name):
                    result = self.run_tool(TOKENS, path)
                    self.assertEqual(result.returncode, 2)

    def test_invalid_baseline_is_input_error_without_traceback(self):
        with tempfile.TemporaryDirectory(prefix="kt-contrast-") as directory:
            baseline = Path(directory) / "invalid.json"
            baseline.write_text(
                json.dumps(
                    {
                        "version": 999,
                        "entries": [
                            {"pair": "brand-foreground", "surface": "brand", "measured": "NaN", "required": -9, "until": "2099-01-01"}
                        ],
                    }
                ),
                encoding="utf-8",
            )
            result = self.run_tool(TOKENS, "--baseline", baseline, "--json")
            self.assertEqual(result.returncode, 2)
            self.assertNotIn("Traceback", result.stderr)

    def test_huge_integer_baseline_is_input_error_without_traceback(self):
        with tempfile.TemporaryDirectory(prefix="kt-contrast-") as directory:
            baseline = Path(directory) / "invalid.json"
            baseline.write_text(
                '{"version":1,"entries":[{"pair":"brand-foreground/brand","surface":"brand","measured":'
                + "9" * 5000
                + ',"required":4.5,"until":"2099-01-01"}]}',
                encoding="utf-8",
            )
            result = self.run_tool(TOKENS, "--baseline", baseline, "--json")
            self.assertEqual(result.returncode, 2)
            self.assertNotIn("Traceback", result.stderr)

    def test_deep_json_baseline_is_input_error_without_traceback(self):
        with tempfile.TemporaryDirectory(prefix="kt-contrast-") as directory:
            baseline = Path(directory) / "deep.json"
            baseline.write_text("[" * 2000 + "0" + "]" * 2000, encoding="utf-8")
            result = self.run_tool(TOKENS, "--baseline", baseline, "--json")
            self.assertEqual(result.returncode, 2)
            self.assertNotIn("Traceback", result.stderr)

    def test_invalid_option_value_is_generic(self):
        result = self.run_tool(TOKENS, "--json=REVIEW_INPUT_MARKER")
        self.assertEqual(result.returncode, 2)
        self.assertNotIn("REVIEW_INPUT_MARKER", result.stderr)

    def test_invalid_surface_and_missing_input_are_generic_errors(self):
        invalid_surface = self.run_tool(TOKENS, "--read-surface", "REVIEW_INPUT_MARKER", "--json")
        self.assertEqual(invalid_surface.returncode, 2)
        self.assertNotIn("REVIEW_INPUT_MARKER", invalid_surface.stderr)
        missing = self.run_tool(Path("REVIEW_INPUT_MARKER.css"), "--json")
        self.assertEqual(missing.returncode, 2)
        self.assertNotIn("REVIEW_INPUT_MARKER", missing.stderr)


if __name__ == "__main__":
    unittest.main()
