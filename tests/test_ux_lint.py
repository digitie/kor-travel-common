# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"""ux_lint의 금지 패턴·인용 제외·diff 판정을 검증한다."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "ux_lint.py"


class UxLintTests(unittest.TestCase):
    def run_tool(self, root: Path, *args: str | Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, "-B", "-X", "utf8", str(SCRIPT), *(str(arg) for arg in args)],
            cwd=root,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )

    def test_all_patterns_report_and_executable_templates_are_checked(self):
        with tempfile.TemporaryDirectory(prefix="kt-ux-") as directory:
            root = Path(directory)
            fixture = root / "fixture.tsx"
            fixture.write_text(
                """const positive = <div className=\"bg-[#fff] text-[13px] rounded-2xl bg-blue-500/50 outline-none transition transition-colors aria-disabled:opacity-50\" />;
// window.confirm rounded-2xl
const quoted = `window.confirm #fff text-[12px] rounded-2xl`;
window.confirm('확인');
""",
                encoding="utf-8",
            )
            (root / "fixture.css").write_text(".raw { color: #fff; background: oklch(50% 0.1 20); }\n", encoding="utf-8")
            result = self.run_tool(root, "--root", root, "--json")
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            patterns = {item["pattern"] for item in payload["findings"]}
            self.assertEqual(patterns, {"P1", "P2", "P3", "P4a", "P4b", "P5", "P6", "P7", "P8"})
            self.assertEqual(sum(item["pattern"] == "P8" for item in payload["findings"]), 2)

    def test_mdx_inline_code_is_ignored_but_executable_templates_are_checked(self):
        with tempfile.TemporaryDirectory(prefix="kt-ux-") as directory:
            root = Path(directory)
            fixture = root / "fixture.mdx"
            fixture.write_text(
                "`outline-none window.confirm()`\n"
                "`${window.confirm('문서 예시')}`\n"
                "const value = <div className={`outline-none ${window.confirm('확인')}`} />;\n"
                "const safe = `${/* window.confirm('주석') */ value}`;\n",
                encoding="utf-8",
            )
            result = self.run_tool(root, "--root", root, "--json")
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual({item["pattern"] for item in payload["findings"]}, {"P6", "P8"})
            self.assertEqual(sum(item["pattern"] == "P8" for item in payload["findings"]), 1)

    def test_mdx_tagged_templates_fences_and_colon_examples(self):
        with tempfile.TemporaryDirectory(prefix="kt-ux-") as directory:
            root = Path(directory)
            fixture = root / "fixture.mdx"
            fixture.write_text(
                "Example: `outline-none window.confirm()`\n"
                "```tsx\nconst ignored = `outline-none`; window.confirm('문서');\n```\n"
                "~~~tsx\nconst alsoIgnored = `outline-none`; window.confirm('문서');\n~~~\n"
                "export const X = () => <div className={String.raw`outline-none`} />;\n",
                encoding="utf-8",
            )
            result = self.run_tool(root, "--root", root, "--json")
            self.assertEqual(result.returncode, 0, result.stderr)
            findings = json.loads(result.stdout)["findings"]
            self.assertEqual({item["pattern"] for item in findings}, {"P6"})
            self.assertEqual(len(findings), 1)

    def test_mdx_js_templates_inside_array_ternary_and_arbitrary_tags_are_checked(self):
        with tempfile.TemporaryDirectory(prefix="kt-ux-") as directory:
            root = Path(directory)
            fixture = root / "fixture.mdx"
            fixture.write_text(
                "export const A = () => <div className={[\"kt\", `outline-none`].join(\" \" )} />;\n"
                "export const B = () => <div className={true ? `outline-none` : \"kt\"} />;\n"
                "export const C = () => <div className={classes`outline-none`} />;\n"
                "export const D = () => <div className={String['raw']`outline-none`} />;\n",
                encoding="utf-8",
            )
            result = self.run_tool(root, "--root", root, "--json")
            self.assertEqual(result.returncode, 0, result.stderr)
            findings = json.loads(result.stdout)["findings"]
            self.assertEqual(sum(item["pattern"] == "P6" for item in findings), 4)

    def test_mdx_fence_length_and_suffix_are_preserved_and_blockquote_code_is_ignored(self):
        with tempfile.TemporaryDirectory(prefix="kt-ux-") as directory:
            root = Path(directory)
            fixture = root / "fixture.mdx"
            fixture.write_text(
                "````tsx\n``\nwindow.confirm(\"문서 예시\");\n````\n"
                "```tsx\n```not-a-closing-fence\nwindow.confirm(\"문서 예시\");\n```\n"
                "> `outline-none window.confirm()`\n",
                encoding="utf-8",
            )
            result = self.run_tool(root, "--root", root, "--json")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)["findings"], [])

    def test_mdx_multiline_jsx_and_blockquote_jsx_templates_are_checked(self):
        with tempfile.TemporaryDirectory(prefix="kt-ux-") as directory:
            root = Path(directory)
            fixture = root / "fixture.mdx"
            fixture.write_text(
                "export const X = () => (\n"
                "  <div\n"
                "    className={\n"
                "      `outline-none`\n"
                "    }\n"
                "  />\n"
                ");\n"
                "> <div className={\n"
                "  classes`outline-none`\n"
                "} />\n",
                encoding="utf-8",
            )
            result = self.run_tool(root, "--root", root, "--json")
            self.assertEqual(result.returncode, 0, result.stderr)
            findings = json.loads(result.stdout)["findings"]
            self.assertEqual(sum(item["pattern"] == "P6" for item in findings), 2)

    def test_mdx_two_backtick_inline_code_span_is_ignored(self):
        with tempfile.TemporaryDirectory(prefix="kt-ux-") as directory:
            root = Path(directory)
            fixture = root / "fixture.mdx"
            fixture.write_text("Example: `` `outline-none window.confirm()` ``\n", encoding="utf-8")
            result = self.run_tool(root, "--root", root, "--json")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)["findings"], [])

    def test_mdx_nested_jsx_expression_and_unindented_esm_are_checked(self):
        with tempfile.TemporaryDirectory(prefix="kt-ux-") as directory:
            root = Path(directory)
            nested = root / "nested.mdx"
            nested.write_text(
                "export function classes(a,b){return b;}\n\n"
                "export function X() {\n"
                "  return <div className={classes(\n"
                "    {},\n"
                "    `outline-none`\n"
                "  )} />;\n"
                "}\n",
                encoding="utf-8",
            )
            esm = root / "esm.mdx"
            esm.write_text("export const classes =\n`outline-none`;\n", encoding="utf-8")
            result = self.run_tool(root, "--root", root, "--json")
            self.assertEqual(result.returncode, 0, result.stderr)
            findings = json.loads(result.stdout)["findings"]
            self.assertEqual(sum(item["pattern"] == "P6" for item in findings), 2)

    def test_mdx_unclosed_span_does_not_hide_later_jsx_and_docs_do_not_leak_context(self):
        with tempfile.TemporaryDirectory(prefix="kt-ux-") as directory:
            root = Path(directory)
            fixture = root / "fixture.mdx"
            fixture.write_text(
                "Example `` unmatched\n\n"
                "export const X = () => <div className=\"outline-none\" />;\n",
                encoding="utf-8",
            )
            docs = root / "docs.mdx"
            docs.write_text("문법 예시: `className={`\n\n다른 인용: `outline-none`\n", encoding="utf-8")
            result = self.run_tool(root, "--root", root, "--json")
            self.assertEqual(result.returncode, 0, result.stderr)
            findings = json.loads(result.stdout)["findings"]
            self.assertEqual(sum(item["pattern"] == "P6" for item in findings), 1)

    def test_mdx_comments_do_not_close_jsx_expression_and_code_examples_do_not_leak(self):
        with tempfile.TemporaryDirectory(prefix="kt-ux-") as directory:
            root = Path(directory)
            fixture = root / "fixture.mdx"
            fixture.write_text(
                "export function X() {\n"
                "  return <div className={\n"
                "    // }\n"
                "    `outline-none`\n"
                "  } />;\n"
                "}\n\n"
                "문법 예시: `<div className={`\n\n다른 인용: `outline-none`\n",
                encoding="utf-8",
            )
            result = self.run_tool(root, "--root", root, "--json")
            self.assertEqual(result.returncode, 0, result.stderr)
            findings = json.loads(result.stdout)["findings"]
            self.assertEqual(sum(item["pattern"] == "P6" for item in findings), 1)

    def test_mdx_inline_spans_stop_at_blank_lines_and_cover_file_start(self):
        with tempfile.TemporaryDirectory(prefix="kt-ux-") as directory:
            root = Path(directory)
            cases = {
                "paragraphs.mdx": (
                    "Example `` unmatched\n\n"
                    "export const X=()=> <div className=\"outline-none\"/>;\n\n"
                    "Later `` delimiter\n"
                ),
                "same-paragraph.mdx": "Example ` unmatched <span className=\"outline-none\" />\n",
                "same-paragraph-double.mdx": "Example `` unmatched <div className=\"outline-none\"/>\n",
                "blockquote.mdx": "> Example ` unmatched\n>\n> <div className=\"outline-none\" />\n",
                "backslash.mdx": "Example `path\\`<span className=\"outline-none\" />\n",
                "start.mdx": "`<div className={`\n\n다른 인용: `outline-none`\n",
                "triple.mdx": "문법 예시: ```<div className={```\n\n다른 인용: `outline-none`\n",
            }
            for name, source in cases.items():
                (root / name).write_text(source, encoding="utf-8")
            result = self.run_tool(root, "--root", root, "--json")
            self.assertEqual(result.returncode, 0, result.stderr)
            findings = json.loads(result.stdout)["findings"]
            self.assertEqual(
                [(item["file"], item["pattern"]) for item in findings],
                [
                    ("backslash.mdx", "P6"),
                    ("blockquote.mdx", "P6"),
                    ("paragraphs.mdx", "P6"),
                    ("same-paragraph-double.mdx", "P6"),
                    ("same-paragraph.mdx", "P6"),
                ],
            )

    def test_escaped_template_text_remains_scannable(self):
        with tempfile.TemporaryDirectory(prefix="kt-ux-") as directory:
            root = Path(directory)
            fixture = root / "fixture.tsx"
            fixture.write_text("const X = () => <div className={`\\${/* outline-none */}`} />;\n", encoding="utf-8")
            result = self.run_tool(root, "--root", root, "--json")
            self.assertEqual(result.returncode, 0, result.stderr)
            findings = json.loads(result.stdout)["findings"]
            self.assertEqual({item["pattern"] for item in findings}, {"P6"})

    def test_baseline_and_added_lines(self):
        with tempfile.TemporaryDirectory(prefix="kt-ux-") as directory:
            root = Path(directory)
            self.git(root, "init", "-q")
            fixture = root / "fixture.tsx"
            fixture.write_text("const old = 'outline-none';\n", encoding="utf-8")
            self.git(root, "add", "fixture.tsx")
            self.git(root, "-c", "user.name=테스트", "-c", "user.email=test@example.invalid", "commit", "-q", "-m", "base")
            fixture.write_text("const old = 'outline-none';\nconst added = 'outline-none';\n", encoding="utf-8")
            result = self.run_tool(root, "--root", root, "--base", "HEAD", "--json")
            self.assertEqual(result.returncode, 1)
            payload = json.loads(result.stdout)
            self.assertEqual([item["line"] for item in payload["findings"] if item["fail"]], [2])

    def test_front_insertion_cannot_consume_baseline_budget(self):
        with tempfile.TemporaryDirectory(prefix="kt-ux-") as directory:
            root = Path(directory)
            self.git(root, "init", "-q")
            fixture = root / "fixture.tsx"
            fixture.write_text("const old = 'outline-none';\n", encoding="utf-8")
            self.git(root, "add", "fixture.tsx")
            self.git(root, "-c", "user.name=테스트", "-c", "user.email=test@example.invalid", "commit", "-q", "-m", "base")
            fixture.write_text("const added = 'outline-none';\nconst old = 'outline-none';\n", encoding="utf-8")
            baseline = root / "baseline.json"
            baseline.write_text(
                json.dumps(
                    {
                        "schema": "kor-travel-common.ux-baseline.v1",
                        "entries": [{"rule": "P6", "path": "fixture.tsx", "count": 1, "reason": "이관 전", "until": "2099-12-31", "task": "T-103"}],
                    }
                ),
                encoding="utf-8",
            )
            result = self.run_tool(root, "--root", root, "--baseline", baseline, "--base", "HEAD", "--json")
            self.assertEqual(result.returncode, 1)
            payload = json.loads(result.stdout)
            self.assertEqual([item["line"] for item in payload["findings"] if item["fail"]], [1])

    def test_baseline_schema_exempts_count_and_expiry_fails(self):
        with tempfile.TemporaryDirectory(prefix="kt-ux-") as directory:
            root = Path(directory)
            fixture = root / "fixture.tsx"
            fixture.write_text("const value = 'outline-none';\n", encoding="utf-8")
            baseline = root / "baseline.json"
            baseline.write_text(
                json.dumps(
                    {
                        "schema": "kor-travel-common.ux-baseline.v1",
                        "entries": [
                            {"rule": "P6", "path": "fixture.tsx", "count": 1, "reason": "이관 전", "until": "2099-12-31", "task": "T-103"}
                        ],
                    }
                ),
                encoding="utf-8",
            )
            active = self.run_tool(root, "--root", root, "--baseline", baseline, "--fail-new", "--json")
            self.assertEqual(active.returncode, 0, active.stderr)
            baseline.write_text(baseline.read_text(encoding="utf-8").replace("2099-12-31", "2000-01-01"), encoding="utf-8")
            expired = self.run_tool(root, "--root", root, "--baseline", baseline, "--json")
            self.assertEqual(expired.returncode, 1)
            self.assertEqual(json.loads(expired.stdout)["status"], "EXEMPT_EXPIRED")

    def test_step_summary_is_markdown(self):
        with tempfile.TemporaryDirectory(prefix="kt-ux-") as directory:
            root = Path(directory)
            fixture = root / "fixture.tsx"
            fixture.write_text("const value = 'outline-none';\n", encoding="utf-8")
            summary = root / "summary.md"
            result = self.run_tool(root, "--root", root, "--step-summary", summary)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("ux_lint", summary.read_text(encoding="utf-8"))

    def test_excluded_paths_and_token_allowlist(self):
        with tempfile.TemporaryDirectory(prefix="kt-ux-") as directory:
            root = Path(directory)
            (root / "src").mkdir()
            (root / "tests").mkdir()
            (root / "src" / "keep.tsx").write_text("const value = 'outline-none';\n", encoding="utf-8")
            (root / "src" / "ignored.test.tsx").write_text("const value = 'outline-none';\n", encoding="utf-8")
            (root / "src" / "generated.gen.ts").write_text("const value = 'outline-none';\n", encoding="utf-8")
            (root / "tests" / "ignored.tsx").write_text("const value = 'outline-none';\n", encoding="utf-8")
            token = root / "src" / "tokens.css"
            token.write_text(":root { --color: #fff; }\n", encoding="utf-8")
            result = self.run_tool(root, "--root", root, "--token-files", "src/tokens.css", "--json")
            self.assertEqual(result.returncode, 0, result.stderr)
            files = {item["file"] for item in json.loads(result.stdout)["findings"]}
            self.assertEqual(files, {"src/keep.tsx"})

    def test_external_root_uses_its_own_git_repository(self):
        with tempfile.TemporaryDirectory(prefix="kt-ux-") as directory:
            root = Path(directory) / "frontend"
            root.mkdir()
            self.git(root, "init", "-q")
            fixture = root / "page.tsx"
            fixture.write_text("const value = 1;\n", encoding="utf-8")
            self.git(root, "add", "page.tsx")
            self.git(root, "-c", "user.name=테스트", "-c", "user.email=test@example.invalid", "commit", "-q", "-m", "base")
            fixture.write_text("const value = 'outline-none';\n", encoding="utf-8")
            result = self.run_tool(ROOT, "--root", root, "--base", "HEAD", "--json")
            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertEqual(json.loads(result.stdout)["fail_count"], 1)

    def test_invalid_baseline_numbers_are_input_errors(self):
        with tempfile.TemporaryDirectory(prefix="kt-ux-") as directory:
            root = Path(directory)
            fixture = root / "fixture.tsx"
            fixture.write_text("const value = 'outline-none';\n", encoding="utf-8")
            baseline = root / "baseline.json"
            baseline.write_text(
                json.dumps(
                    {
                        "schema": "kor-travel-common.ux-baseline.v1",
                        "entries": [{"rule": "P6", "path": "fixture.tsx", "count": 1e309, "reason": "이관 전", "until": "2099-12-31", "task": "T-103"}],
                    }
                ),
                encoding="utf-8",
            )
            result = self.run_tool(root, "--root", root, "--baseline", baseline, "--json")
            self.assertEqual(result.returncode, 2)
            self.assertNotIn("Traceback", result.stderr)

    def test_huge_integer_baseline_is_input_error_without_traceback(self):
        with tempfile.TemporaryDirectory(prefix="kt-ux-") as directory:
            root = Path(directory)
            fixture = root / "fixture.tsx"
            fixture.write_text("const value = 'outline-none';\n", encoding="utf-8")
            baseline = root / "baseline.json"
            baseline.write_text(
                '{"schema":"kor-travel-common.ux-baseline.v1","entries":[{"rule":"P6","path":"fixture.tsx","count":'
                + "9" * 5000
                + ',"reason":"이관 전","until":"2099-12-31","task":"T-103"}]}',
                encoding="utf-8",
            )
            result = self.run_tool(root, "--root", root, "--baseline", baseline, "--json")
            self.assertEqual(result.returncode, 2)
            self.assertNotIn("Traceback", result.stderr)

    def test_deep_json_baseline_is_input_error_without_traceback(self):
        with tempfile.TemporaryDirectory(prefix="kt-ux-") as directory:
            root = Path(directory)
            fixture = root / "fixture.tsx"
            fixture.write_text("const value = 1;\n", encoding="utf-8")
            baseline = root / "deep.json"
            baseline.write_text("[" * 2000 + "0" + "]" * 2000, encoding="utf-8")
            result = self.run_tool(root, "--root", root, "--baseline", baseline, "--json")
            self.assertEqual(result.returncode, 2)
            self.assertNotIn("Traceback", result.stderr)

    def test_invalid_option_value_is_generic(self):
        with tempfile.TemporaryDirectory(prefix="kt-ux-") as directory:
            root = Path(directory)
            fixture = root / "fixture.tsx"
            fixture.write_text("const value = 1;\n", encoding="utf-8")
            result = self.run_tool(root, "--root", root, "--json=REVIEW_INPUT_MARKER")
            self.assertEqual(result.returncode, 2)
            self.assertNotIn("REVIEW_INPUT_MARKER", result.stderr)

    def test_diff_added_line_starting_with_triple_plus_is_checked(self):
        with tempfile.TemporaryDirectory(prefix="kt-ux-") as directory:
            root = Path(directory)
            self.git(root, "init", "-q")
            fixture = root / "fixture.tsx"
            fixture.write_text("const value = 1;\n", encoding="utf-8")
            self.git(root, "add", "fixture.tsx")
            self.git(root, "-c", "user.name=테스트", "-c", "user.email=test@example.invalid", "commit", "-q", "-m", "base")
            fixture.write_text("const value = 1;\n+++counter; window.confirm('확인');\n", encoding="utf-8")
            result = self.run_tool(root, "--root", root, "--base", "HEAD", "--json")
            self.assertEqual(result.returncode, 1, result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["fail_count"], 1)
            self.assertEqual(payload["findings"][0]["line"], 2)

    def test_base_option_like_ref_is_rejected(self):
        with tempfile.TemporaryDirectory(prefix="kt-ux-") as directory:
            root = Path(directory)
            self.git(root, "init", "-q")
            fixture = root / "fixture.tsx"
            fixture.write_text("const value = 'outline-none';\n", encoding="utf-8")
            result = self.run_tool(root, "--root", root, "--base=--name-only", "--json")
            self.assertEqual(result.returncode, 2)
            self.assertNotIn("Traceback", result.stderr)

    def test_secret_like_path_is_redacted_in_outputs(self):
        with tempfile.TemporaryDirectory(prefix="kt-ux-") as directory:
            root = Path(directory)
            fixture = root / ("ghp_" + "Z" * 36 + ".tsx")
            fixture.write_text("const value = 'outline-none';\n", encoding="utf-8")
            summary = root / "summary.md"
            result = self.run_tool(root, "--root", root, "--fail-new", "--step-summary", summary, "--json")
            self.assertEqual(result.returncode, 1)
            raw = result.stdout + summary.read_text(encoding="utf-8")
            self.assertNotIn(fixture.name, raw)
            self.assertIn("<redacted>", raw)

    def test_private_address_like_path_is_redacted_in_outputs(self):
        with tempfile.TemporaryDirectory(prefix="kt-ux-") as directory:
            root = Path(directory)
            fixture = root / ("10" + ".23.45.67.tsx")
            fixture.write_text("const value = 'outline-none';\n", encoding="utf-8")
            summary = root / "summary.md"
            result = self.run_tool(root, "--root", root, "--fail-new", "--step-summary", summary, "--json")
            self.assertEqual(result.returncode, 1)
            raw = result.stdout + summary.read_text(encoding="utf-8")
            self.assertNotIn(fixture.name, raw)
            self.assertIn("<redacted>", raw)

    @staticmethod
    def git(root: Path, *args: str) -> None:
        result = subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True)
        if result.returncode:
            raise AssertionError(result.stderr)


if __name__ == "__main__":
    unittest.main()
