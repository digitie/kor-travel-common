# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"""누적 MDX 문맥 반례와 변형의 패턴·원본 좌표 불변식을 검증한다."""

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from tools import ux_lint


CORPUS = Path(__file__).parent / "fixtures" / "ux" / "mdx-contexts.json"


class MdxContextTests(unittest.TestCase):
    def test_context_corpus_through_cli_and_added_lines(self):
        cases = json.loads(CORPUS.read_text(encoding="utf-8"))["cases"]
        env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
        env.pop("GITHUB_STEP_SUMMARY", None)
        script = Path(ux_lint.__file__).resolve()
        with tempfile.TemporaryDirectory(prefix="kt-mdx-corpus-") as directory:
            root = Path(directory)

            def git(*args):
                return subprocess.check_output(["git", *args], cwd=root, env=env, text=True).strip()

            git("init", "-q")
            names = [f"case-{index:02}.mdx" for index in range(len(cases))]
            for name in names:
                (root / name).write_text('{window.confirm("기존")}\n\n', encoding="utf-8")
            git("add", "--", *names)
            git("-c", "user.name=회귀 시험", "-c", "user.email=test@example.invalid", "commit", "-qm", "시험 기준선")
            base = git("rev-parse", "HEAD")
            expected = {}
            for name, case in zip(names, cases):
                (root / name).write_text('{window.confirm("기존")}\n\n' + case["source"], encoding="utf-8")
                expected[name] = case["expected"]
            result = subprocess.run(
                [sys.executable, "-B", "-X", "utf8", str(script), "--root", str(root), "--base", base, "--fail-new", "--json"],
                cwd=root, env=env, capture_output=True, text=True, encoding="utf-8",
            )
            self.assertEqual(result.returncode, 1, result.stderr)
            payload = json.loads(result.stdout)
            actual = {name: [] for name in names}
            for finding in payload["findings"]:
                if finding["line"] == 1:
                    self.assertFalse(finding["added"])
                    self.assertFalse(finding["fail"])
                else:
                    self.assertTrue(finding["added"])
                    self.assertTrue(finding["fail"])
                    actual[finding["file"]].append(finding["pattern"])
            self.assertEqual(actual, expected)
            self.assertEqual(payload["fail_count"], sum(map(len, expected.values())))

    def test_context_corpus_and_coordinate_preservation(self):
        cases = json.loads(CORPUS.read_text(encoding="utf-8"))["cases"]
        variants = []
        for case in cases:
            for separator in ("\n", "\r\n", "\r"):
                for prefix in case.get("prefixes", ("", "> ", ">> ")):
                    source = separator.join(prefix + line for line in case["source"].split("\n"))
                    variants.append((case, separator, prefix, source))
        masks = ux_lint.mask_mdx_sources([source for _, _, _, source in variants])
        for (case, separator, prefix, source), masked in zip(variants, masks):
            with self.subTest(case=case["id"], separator=repr(separator), prefix=prefix):
                self.assertEqual(len(masked), len(source))
                for offset, char in enumerate(source):
                    if char in "\r\n\u2028\u2029":
                        self.assertEqual(masked[offset], char)
                findings = sorted(
                    (match.start(), name)
                    for name, _, pattern in ux_lint.COMPILED_PATTERNS
                    if name != "P4b"
                    for match in pattern.finditer(masked)
                )
                self.assertEqual([name for _, name in findings], case["expected"])

    def test_inline_delimiter_lengths_and_document_punctuation(self):
        sources = []
        for run in range(1, 5):
            for separator in ("\n", "\r\n", "\r"):
                for word in ("for example,", "don't", '"문장', "https://example.invalid", "src/*"):
                    for marker in ("~~~", "`" * (run + 3)):
                        delimiter = "`" * run
                        source = separator.join([
                            f"Example {delimiter}{word} {{window.confirm('실행')}}",
                            marker + "js",
                            "{window.confirm('문서')}",
                            "close " + delimiter,
                            marker,
                            "{ /* window.confirm('주석') */ }",
                        ])
                        sources.append(source)
        for source, masked in zip(sources, ux_lint.mask_mdx_sources(sources)):
            self.assertEqual(masked.count("window.confirm"), 1, source)

    def test_invalid_mdx_is_input_error_without_partial_success_or_source(self):
        with tempfile.TemporaryDirectory(prefix="kt-mdx-invalid-") as directory:
            root = Path(directory)
            (root / "valid.mdx").write_text('{window.confirm("실행")}\n', encoding="utf-8")
            (root / "invalid.mdx").write_text("export const PRIVATE_SOURCE_MARKER =", encoding="utf-8")
            result = subprocess.run(
                [sys.executable, "-B", "-X", "utf8", str(Path(ux_lint.__file__).resolve()), "--root", str(root), "--json"],
                capture_output=True, text=True, encoding="utf-8",
            )
            self.assertEqual(result.returncode, 2)
            self.assertEqual(result.stdout, "")
            self.assertNotIn("PRIVATE_SOURCE_MARKER", result.stderr)
            self.assertNotIn(directory, result.stderr)
            self.assertNotIn("Traceback", result.stderr)

    def test_node_is_only_required_when_mdx_is_present(self):
        with patch.object(ux_lint.shutil, "which", return_value=None):
            self.assertEqual(ux_lint.mask_mdx_sources([]), [])
            self.assertIn("outline-none", ux_lint._mask_comments_and_backticks('const value = "outline-none";', False))
            with self.assertRaisesRegex(ux_lint.UxLintError, "Node.js"):
                ux_lint.mask_mdx_sources(['{window.confirm("실행")}'])

    def test_parser_failure_and_coordinate_drift_cannot_report_success(self):
        source = "문서\n😀"
        for stdout, returncode in (
            ('[]', 0),
            ('[{"masked": "문서 😀"}]', 0),
            ('[{"masked": "문서\\n  "}]', 0),
            ('[{"error": "INVALID_MDX"}]', 0),
            ('원문이 섞인 잘못된 출력', 0),
            ('[]', 2),
        ):
            with self.subTest(stdout=stdout, returncode=returncode):
                result = subprocess.CompletedProcess([], returncode, stdout, "PRIVATE_SOURCE_MARKER")
                with patch.object(ux_lint.subprocess, "run", return_value=result):
                    with self.assertRaises(ux_lint.UxLintError) as error:
                        ux_lint.mask_mdx_sources([source])
                    self.assertNotIn("PRIVATE_SOURCE_MARKER", str(error.exception))
        with patch.object(ux_lint.subprocess, "run", side_effect=subprocess.TimeoutExpired("node", 30)):
            with self.assertRaises(ux_lint.UxLintError):
                ux_lint.mask_mdx_sources([source])


if __name__ == "__main__":
    unittest.main()
