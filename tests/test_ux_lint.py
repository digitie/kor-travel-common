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
                "expression-comment.mdx": "Example ` unmatched {/* note */ window.confirm('x')}\n",
                "expression-combining.mdx": "Example ` unmatched {e\u0301 && window.confirm('x')}\n",
                "expression-decimal.mdx": "Example ` unmatched {.5 && window.confirm('x')}\n",
                "expression-division.mdx": "const n = 1;\nExample ` unmatched {n / window.confirm('x')}\n",
                "expression-escape.mdx": "Example ` unmatched {\\u006e && window.confirm('x')}\n",
                "expression-one.mdx": "Example ` unmatched {window.confirm('x')}\n",
                "expression-double.mdx": "Example `` unmatched {window.confirm('x')}\n",
                "expression-keyword.mdx": "Example ` unmatched {void window.confirm('x')}\n",
                "expression-logical.mdx": "Example ` unmatched {true && window.confirm('x')}\n",
                "expression-number.mdx": "Example ` unmatched {1 && window.confirm('x')}\n",
                "expression-regexp.mdx": "Example ` unmatched {/x/.test(window.confirm('x'))}\n",
                "expression-unicode.mdx": "Example ` unmatched {값 && window.confirm('x')}\n",
                "expression-unary.mdx": "Example ` unmatched {!window.confirm('x')}\n",
                "expression-xor.mdx": "const n = 1;\nExample ` unmatched {n ^ window.confirm('x')}\n",
                "expression-zwnj.mdx": "Example ` unmatched {a\u200c && window.confirm('x')}\n",
                "multiline-expression.mdx": (
                    "Example `` unmatched\n"
                    "<div className={\n"
                    " [`outline-none`].join(\" \")\n"
                    "}/>\n"
                ),
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
                    ("expression-combining.mdx", "P8"),
                    ("expression-comment.mdx", "P8"),
                    ("expression-decimal.mdx", "P8"),
                    ("expression-division.mdx", "P8"),
                    ("expression-double.mdx", "P8"),
                    ("expression-escape.mdx", "P8"),
                    ("expression-keyword.mdx", "P8"),
                    ("expression-logical.mdx", "P8"),
                    ("expression-number.mdx", "P8"),
                    ("expression-one.mdx", "P8"),
                    ("expression-regexp.mdx", "P8"),
                    ("expression-unary.mdx", "P8"),
                    ("expression-unicode.mdx", "P8"),
                    ("expression-xor.mdx", "P8"),
                    ("expression-zwnj.mdx", "P8"),
                    ("multiline-expression.mdx", "P6"),
                    ("paragraphs.mdx", "P6"),
                    ("same-paragraph-double.mdx", "P6"),
                    ("same-paragraph.mdx", "P6"),
                ],
            )

    def test_mdx_expression_resume_uses_ecmascript_identifier_boundaries(self):
        with tempfile.TemporaryDirectory(prefix="kt-ux-") as directory:
            root = Path(directory)
            expressions = {
                "unicode-iv.mdx": "\u2163 && window.confirm('x')",
                "unicode-script.mdx": "\u2118 && window.confirm('x')",
                "unicode-greek.mdx": "\u037a && window.confirm('x')",
                "unicode-middle-dot.mdx": "a\u00b7 && window.confirm('x')",
                "unicode-ano-teleia.mdx": "a\u0387 && window.confirm('x')",
                "unicode-new-script.mdx": "\U00011f02 && window.confirm('x')",
                "unicode-new-cjk.mdx": "\U0002ebf0 && window.confirm('x')",
                "unicode-feff-leading.mdx": "\ufeff\u2118 && window.confirm('x')",
                "unicode-feff-between.mdx": "\u2118\ufeff&& window.confirm('x')",
                "async-arrow.mdx": "async x => window.confirm('x')",
            }
            for name, expression in expressions.items():
                (root / name).write_text(
                    f"Example ` unmatched {{{expression}}}\n"
                    f"Example `` unmatched {{{expression}}}\n",
                    encoding="utf-8",
                )
            (root / "closed.mdx").write_text(
                "Example ` {\u2118 && window.confirm('x')} `\n",
                encoding="utf-8",
            )
            (root / "plain.mdx").write_text(
                "{\u2118 && window.confirm('x')}\n",
                encoding="utf-8",
            )

            result = self.run_tool(root, "--root", root, "--json")
            self.assertEqual(result.returncode, 0, result.stderr)
            findings = json.loads(result.stdout)["findings"]
            counts = {name: 0 for name in (*expressions, "closed.mdx", "plain.mdx")}
            for finding in findings:
                self.assertEqual(finding["pattern"], "P8")
                counts[finding["file"]] += 1
            self.assertEqual(counts["plain.mdx"], 1)
            self.assertEqual(counts["closed.mdx"], 0)
            for name in expressions:
                self.assertEqual(counts[name], 2)

    def test_ecmascript_line_terminators_end_line_comments(self):
        with tempfile.TemporaryDirectory(prefix="kt-ux-") as directory:
            root = Path(directory)
            for suffix, terminator in (("ls", "\u2028"), ("ps", "\u2029")):
                (root / f"line-comment-{suffix}.ts").write_text(
                    f"// 설명{terminator}window.confirm('x')\n",
                    encoding="utf-8",
                )
                (root / f"line-comment-{suffix}.mdx").write_text(
                    f"// 설명{terminator}window.confirm('x')\n"
                    "Example ` unmatched {window.confirm('x')}\n"
                    "Example `` unmatched {window.confirm('x')}\n",
                    encoding="utf-8",
                )

            result = self.run_tool(root, "--root", root, "--json")
            self.assertEqual(result.returncode, 0, result.stderr)
            findings = json.loads(result.stdout)["findings"]
            counts = {finding["file"]: 0 for finding in findings}
            for finding in findings:
                self.assertEqual(finding["pattern"], "P8")
                counts[finding["file"]] += 1
            self.assertEqual(counts, {
                "line-comment-ls.mdx": 3,
                "line-comment-ls.ts": 1,
                "line-comment-ps.mdx": 3,
                "line-comment-ps.ts": 1,
            })

    def test_mdx_all_line_terminators_preserve_paragraph_and_fence_boundaries(self):
        for separator in ("\r", "\n", "\r\n", "\u2028", "\u2029"):
            with tempfile.TemporaryDirectory(prefix="kt-ux-") as directory:
                root = Path(directory)
                if separator in ("\r", "\n", "\r\n"):
                    paragraph = root / "paragraph.mdx"
                    paragraph.write_bytes(
                        (
                            f"Example `` unmatched{separator}{separator}"
                            f"<div className=\"outline-none\"/>{separator}{separator}"
                            f"Later `` delimiter{separator}"
                        ).encode("utf-8")
                    )
                    fence = root / "fence.mdx"
                    fence.write_bytes(
                        (
                            f"~~~tsx{separator}<div className=\"outline-none\"/>{separator}"
                            f"~~~{separator}<div className=\"outline-none\"/>{separator}"
                        ).encode("utf-8")
                    )
                    quoted = root / "quoted.mdx"
                    quoted.write_bytes(
                        f"export const x = {{}}{separator}{separator}"
                        f"Example: `window.confirm(\"quoted\")`{separator}".encode("utf-8")
                    )
                    esm = root / "esm.mdx"
                    esm.write_bytes(
                        (
                            f"Example `` unmatched{separator}{separator}"
                            f"export const X = <div className=\"outline-none\" />{separator}"
                        ).encode("utf-8")
                    )
                    expected = [("esm.mdx", "P6"), ("fence.mdx", "P6"), ("paragraph.mdx", "P6")]
                else:
                    for run_length in (1, 2, 3):
                        delimiter = "`" * run_length
                        quoted = root / f"quoted-{run_length}.mdx"
                        quoted.write_bytes(
                            (
                                f"Example {delimiter} outline-none{separator}{separator}"
                                f"{{window.confirm(\"quoted\")}} {delimiter}{separator}"
                            ).encode("utf-8")
                        )
                    expected = []

                result = self.run_tool(root, "--root", root, "--json")
                self.assertEqual(result.returncode, 0, result.stderr)
                findings = json.loads(result.stdout)["findings"]
                self.assertEqual(
                    [(item["file"], item["pattern"]) for item in findings],
                    expected,
                )

    def test_mdx_fence_closing_line_rejects_unicode_nonspace_suffix(self):
        for suffix, expected in (("\u2028", []), ("\u2029", []), (" ", ["P6"]), ("\t", ["P6"])):
            with tempfile.TemporaryDirectory(prefix="kt-ux-") as directory:
                root = Path(directory)
                fixture = root / "fence.mdx"
                fixture.write_bytes(
                    (
                        "~~~tsx\nquoted\n"
                        f"~~~{suffix}\n"
                        "<div className=\"outline-none\"/>\n"
                        "~~~\n"
                    ).encode("utf-8")
                )
                result = self.run_tool(root, "--root", root, "--json")
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(
                    [item["pattern"] for item in json.loads(result.stdout)["findings"]],
                    expected,
                )

    def test_mdx_fence_closing_line_allows_at_most_three_indent_columns(self):
        for indent, expected in (("", ["P6"]), (" ", ["P6"]), ("   ", ["P6"]), ("    ", []), ("\t", []), (" \t", [])):
            with tempfile.TemporaryDirectory(prefix="kt-ux-") as directory:
                root = Path(directory)
                fixture = root / "fence.mdx"
                fixture.write_text(
                    (
                        "~~~tsx\nquoted\n"
                        f"{indent}~~~\n"
                        "<div className=\"outline-none\"/>\n"
                        "~~~\n"
                    ),
                    encoding="utf-8",
                )
                result = self.run_tool(root, "--root", root, "--json")
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(
                    [item["pattern"] for item in json.loads(result.stdout)["findings"]],
                    expected,
                )

    def test_mdx_backtick_info_string_rejects_backtick_fence_and_scans_next_paragraph(self):
        for separator in ("\n", "\r\n", "\r"):
            with tempfile.TemporaryDirectory(prefix="kt-ux-") as directory:
                root = Path(directory)
                fixture = root / "inline.mdx"
                fixture.write_bytes(
                    (
                        f"```a`b```{separator}{separator}"
                        f"{{window.confirm(\"x\")}}{separator}"
                    ).encode("utf-8")
                )
                result = self.run_tool(root, "--root", root, "--fail-new", "--json")
                self.assertEqual(result.returncode, 1, result.stderr)
                self.assertEqual(
                    [item["pattern"] for item in json.loads(result.stdout)["findings"]],
                    ["P8"],
                )

    def test_mdx_invalid_backtick_info_does_not_hide_next_fence_paragraph(self):
        for prefix in ("", "> ", ">> "):
            for separator in ("\n", "\r\n", "\r"):
                with tempfile.TemporaryDirectory(prefix="kt-ux-") as directory:
                    root = Path(directory)
                    fixture = root / "invalid-info.mdx"
                    fixture.write_bytes(
                        (
                            f"{prefix}```bad`info{separator}"
                            f"{prefix}{{window.confirm(\"x\")}}{separator}"
                            f"{prefix}```{separator}"
                        ).encode("utf-8")
                    )
                    result = self.run_tool(root, "--root", root, "--fail-new", "--json")
                    self.assertEqual(result.returncode, 1, result.stderr)
                    self.assertEqual(
                        [item["pattern"] for item in json.loads(result.stdout)["findings"]],
                        ["P8"],
                    )

    def test_mdx_tilde_info_string_allows_backtick(self):
        with tempfile.TemporaryDirectory(prefix="kt-ux-") as directory:
            root = Path(directory)
            fixture = root / "tilde.mdx"
            fixture.write_text(
                "~~~a`b\n<div className=\"outline-none\"/>\n~~~\n",
                encoding="utf-8",
            )
            result = self.run_tool(root, "--root", root, "--json")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)["findings"], [])

    def test_mdx_blockquote_fences_are_ignored_and_stop_at_container_boundary(self):
        for separator in ("\n", "\r\n", "\r"):
            with tempfile.TemporaryDirectory(prefix="kt-ux-") as directory:
                root = Path(directory)
                fixture = root / "blockquote.mdx"
                fixture.write_bytes(
                    (
                        f"> ~~~tsx{separator}"
                        f"> <div className=\"outline-none\"/>{separator}"
                        f"> {{window.confirm(\"quoted\")}}{separator}"
                        f"> ~~~{separator}{separator}"
                        f"{{window.confirm(\"outside\")}}{separator}"
                    ).encode("utf-8")
                )
                result = self.run_tool(root, "--root", root, "--fail-new", "--json")
                self.assertEqual(result.returncode, 1, result.stderr)
                findings = json.loads(result.stdout)["findings"]
                self.assertEqual([item["pattern"] for item in findings], ["P8"])

    def test_mdx_blockquote_backtick_fence_masks_blank_quoted_line(self):
        with tempfile.TemporaryDirectory(prefix="kt-ux-") as directory:
            root = Path(directory)
            fixture = root / "blockquote.mdx"
            fixture.write_text(
                "> ```tsx\n>\n> <div className=\"outline-none\"/>\n> ```\n",
                encoding="utf-8",
            )
            result = self.run_tool(root, "--root", root, "--fail-new", "--json")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)["findings"], [])

    def test_mdx_blockquote_fence_tracks_nested_depth_and_post_marker_indent(self):
        with tempfile.TemporaryDirectory(prefix="kt-ux-") as directory:
            root = Path(directory)
            nested = root / "nested.mdx"
            nested.write_text(
                ">> ~~~tsx\n>> <div className=\"outline-none\"/>\n>> ~~~\n"
                "> {window.confirm(\"outside\")}\n",
                encoding="utf-8",
            )
            result = self.run_tool(root, "--root", root, "--fail-new", "--json")
            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertEqual([item["pattern"] for item in json.loads(result.stdout)["findings"]], ["P8"])

            nested.unlink()
            for indent, expected in (
                ("", ["P6"]),
                (" ", ["P6"]),
                ("   ", ["P6"]),
                ("    ", ["P6"]),
                ("\t", ["P6"]),
                (" \t", ["P6"]),
                ("     ", []),
                ("\t\t", []),
                (" \t\t", []),
            ):
                fixture = root / "indent.mdx"
                fixture.write_bytes(
                    (
                        "> ~~~tsx\n"
                        f">{indent}~~~\n"
                        "> <div className=\"outline-none\"/>\n"
                        "> ~~~\n"
                    ).encode("utf-8")
                )
                result = self.run_tool(root, "--root", root, "--fail-new", "--json")
                findings = json.loads(result.stdout)["findings"]
                self.assertEqual(result.returncode, 1 if expected else 0, result.stderr)
                self.assertEqual([item["pattern"] for item in findings], expected)

            fixture.write_text(
                ">    ~~~tsx\n> <div className=\"outline-none\"/>\n> ~~~\n",
                encoding="utf-8",
            )
            result = self.run_tool(root, "--root", root, "--fail-new", "--json")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)["findings"], [])

            fixture.write_text(
                ">     ~~~tsx\n> <div className=\"outline-none\"/>\n> ~~~\n",
                encoding="utf-8",
            )
            result = self.run_tool(root, "--root", root, "--fail-new", "--json")
            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertEqual([item["pattern"] for item in json.loads(result.stdout)["findings"]], ["P6"])

    def test_mdx_blockquote_fence_padding_keeps_p8_after_valid_closing(self):
        valid_padding = ("", " ", "   ", "    ", "\t", " \t")
        invalid_padding = ("     ", "\t\t", " \t\t")
        for marker in ("~~~", "```"):
            for padding in valid_padding:
                with tempfile.TemporaryDirectory(prefix="kt-ux-") as directory:
                    root = Path(directory)
                    fixture = root / "padding.mdx"
                    fixture.write_bytes(
                        (
                            f"> {marker}tsx\n> quoted\n>{padding}{marker}\n"
                            "> {window.confirm(\"after\")}\n"
                        ).encode("utf-8")
                    )
                    result = self.run_tool(root, "--root", root, "--fail-new", "--json")
                    self.assertEqual(result.returncode, 1, result.stderr)
                    findings = json.loads(result.stdout)["findings"]
                    self.assertEqual([item["pattern"] for item in findings], ["P8"])
            for padding in invalid_padding:
                with tempfile.TemporaryDirectory(prefix="kt-ux-") as directory:
                    root = Path(directory)
                    fixture = root / "padding.mdx"
                    fixture.write_bytes(
                        (
                            f"> {marker}tsx\n> quoted\n>{padding}{marker}\n"
                            "> {window.confirm(\"inside\")}\n"
                        ).encode("utf-8")
                    )
                    result = self.run_tool(root, "--root", root, "--fail-new", "--json")
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertEqual(json.loads(result.stdout)["findings"], [])

    def test_mdx_blockquote_fence_rejects_overindented_nested_marker(self):
        with tempfile.TemporaryDirectory(prefix="kt-ux-") as directory:
            root = Path(directory)
            fixture = root / "nested.mdx"
            fixture.write_text(
                ">> ~~~\n>> quoted\n>     > literal\n>> {window.confirm(\"outside\")}\n",
                encoding="utf-8",
            )
            result = self.run_tool(root, "--root", root, "--fail-new", "--json")
            self.assertEqual(result.returncode, 1, result.stderr)
            findings = json.loads(result.stdout)["findings"]
            self.assertEqual([item["pattern"] for item in findings], ["P8"])

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

    def test_diff_added_lines_keep_unicode_line_separators_inside_source_rows(self):
        for separator in ("\r", "\u2028", "\u2029"):
            with tempfile.TemporaryDirectory(prefix="kt-ux-") as directory:
                root = Path(directory)
                self.git(root, "init", "-q")
                fixture = root / "fixture.ts"
                fixture.write_bytes("const text = 'base';\nconst safe = 1;\n".encode("utf-8"))
                self.git(root, "add", "fixture.ts")
                self.git(root, "-c", "user.name=테스트", "-c", "user.email=test@example.invalid", "commit", "-q", "-m", "base")
                fixture.write_bytes(f'const text = "a{separator}@@ -0,0 +99,1 @@";\nwindow.confirm("확인");\n'.encode("utf-8"))

                result = self.run_tool(root, "--root", root, "--base", "HEAD", "--fail-new", "--json")
                self.assertEqual(result.returncode, 1, result.stderr)
                payload = json.loads(result.stdout)
                self.assertEqual(payload["fail_count"], 1)
                self.assertEqual(payload["findings"][0]["line"], 2)
                self.assertTrue(payload["findings"][0]["added"])

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
