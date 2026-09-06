# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"""SPDX 검사기의 헤더 위장·출처 누락·읽기 실패를 고장 주입으로 검증한다."""

import hashlib
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "tools/check_spdx.py"
SPEC = importlib.util.spec_from_file_location("check_spdx", SCRIPT)
CHECK = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECK)
BODY = "SPDX-License-Identifier: GPL-3.0-or-later\nSPDX-FileCopyrightText: 2026 작성자\n"
HEADER = "".join("# " + line + "\n" for line in BODY.splitlines())
SHA = "1234567890abcdef1234567890abcdef12345678"


class SpdxTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="kt-spdx-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.write("PROVENANCE.md", "# PROVENANCE\n")

    def write(self, name, text):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8", newline="\n")
        return path

    def run_cli(self):
        return subprocess.run([sys.executable, "-B", "-X", "utf8", str(SCRIPT),
                               "--root", str(self.root)], text=True, encoding="utf-8",
                              capture_output=True, check=False)

    def errors(self, text, name="tools/sample.py"):
        path = self.write(name, text)
        return CHECK.check_file(path, self.root, CHECK.provenance(self.root))

    def port(self, repo="canview", modified="변경 (2026-09-07)", license_text="GPL-3.0-or-later"):
        self.write("PROVENANCE.md", "# PROVENANCE\n\n"
                   f"| PV-001 | `tools/sample.py` | {repo} | `{SHA}` | `src/sample.py` | "
                   f"{license_text} | {modified} | 검증 |\n")
        return HEADER + f"# Origin: {repo}@{SHA} src/sample.py\n"

    def test_cli_pass_and_read_only(self):
        path = self.write("tools/sample.py", HEADER + "print(1)\n")
        before = hashlib.sha256(path.read_bytes()).digest()
        result = self.run_cli()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("1개 파일, 오류 0개", result.stdout)
        self.assertEqual(before, hashlib.sha256(path.read_bytes()).digest())

    def test_cli_missing_header_fails(self):
        self.write("packages/ui/src/sample.tsx", "export const x = 1\n")
        result = self.run_cli()
        self.assertEqual(result.returncode, 1)
        self.assertIn("SPDX-License-Identifier", result.stdout)

    def test_missing_or_empty_copyright(self):
        for text in (HEADER.splitlines()[0], HEADER.replace("2026 작성자", "")):
            with self.subTest(text=text):
                self.assertTrue(self.errors(text))

    def test_wrong_license_fails(self):
        self.assertTrue(self.errors(HEADER.replace("GPL-3.0-or-later", "MIT")))

    def test_code_strings_and_late_comments_do_not_count(self):
        for text in ('"""\n' + BODY + '"""\n', "print(1)\n" + HEADER,
                     "text = '''\n" + HEADER + "'''\n"):
            with self.subTest(text=text):
                self.assertTrue(self.errors(text))

    def test_comment_syntax_matches_file_type(self):
        self.assertTrue(self.errors(HEADER, "packages/ui/src/sample.ts"))
        self.assertTrue(self.errors("// " + BODY.replace("\n", "\n// "), "packages/tokens/a.css"))

    def test_typescript_and_css_headers(self):
        ts = "".join("// " + line + "\n" for line in BODY.splitlines())
        self.assertFalse(self.errors(ts + "'use client';\n", "packages/ui/a.tsx"))
        self.assertFalse(self.errors("/*\n" + BODY + "*/\n", "packages/tokens/a.css"))
        self.assertFalse(self.errors("/**\n * " + BODY.replace("\n", "\n * ") + "*/\n",
                                     "packages/tokens/a.css"))

    def test_unclosed_block_comment_fails(self):
        self.assertTrue(self.errors("/*\n" + BODY, "packages/tokens/a.css"))

    def test_shebang_and_bom(self):
        self.assertFalse(self.errors("\ufeff#!/usr/bin/env python3\n" + HEADER))

    def test_header_cannot_resume_after_blank_line(self):
        self.assertTrue(self.errors(HEADER.replace("\n# SPDX-File", "\n\n# SPDX-File")))

    def test_port_missing_origin_fails(self):
        self.port()
        self.assertIn("이식 소스의 Origin은 정확히 하나 필요", self.errors(HEADER))

    def test_modified_port_requires_notice(self):
        text = self.port()
        self.assertIn("수정 이식 소스의 Modified 누락", self.errors(text))
        self.assertFalse(self.errors(text + "# Modified: 2026-09-07 — 경로 변경\n"))

    def test_unmodified_port_does_not_require_notice(self):
        text = self.port(modified="없음(diff 0)")
        self.assertFalse(self.errors(text))

    def test_origin_must_match_index(self):
        text = self.port(modified="없음")
        for wrong in (text.replace("canview@", "other@"), text.replace(SHA, "abcdef0"),
                      text.replace("src/sample.py", "src/other.py")):
            with self.subTest(wrong=wrong):
                self.assertTrue(self.errors(wrong))

    def test_origin_short_sha_and_format(self):
        text = self.port(modified="없음")
        self.assertFalse(self.errors(text.replace(SHA, SHA[:7])))
        for wrong in (text.replace("@", " "), text.replace(SHA, "main"),
                      text.replace(SHA, "abc123"), text.replace("src/sample.py", "../sample.py")):
            with self.subTest(wrong=wrong):
                self.assertTrue(self.errors(wrong))

    def test_unregistered_origin_fails(self):
        self.assertTrue(self.errors(HEADER + f"# Origin: canview@{SHA} sample.py\n"))

    def test_geo_requires_only_license(self):
        text = self.port(repo="kor-travel-geo", modified="없음")
        self.assertTrue(self.errors(text))
        self.assertFalse(self.errors(text.replace("GPL-3.0-or-later", "GPL-3.0-only")))
        self.assertFalse(self.errors(text.replace("GPL-3.0-or-later",
                                                 "GPL-3.0-or-later AND GPL-3.0-only")))

    def test_derivative_requires_source_notice(self):
        text = self.port(modified="없음", license_text="GPL-3.0-or-later (shadcn/ui MIT 파생)")
        self.assertTrue(self.errors(text))
        self.assertFalse(self.errors(text + "# Derived-From: shadcn/ui (MIT)\n"))

    def test_modified_requires_real_date_and_summary(self):
        for value in ("2026-02-30 — 변경", "어제 변경", "2026-09-07", "2026-09-07 — "):
            with self.subTest(value=value):
                self.assertTrue(self.errors(HEADER + "# Modified: " + value + "\n"))

    def test_stamp_fails(self):
        self.assertIn("금지된 Hallmark 스탬프", self.errors(HEADER + "# Hallmark" + " · 복사\n"))

    def test_generated_exclusions_and_all_source_locations(self):
        for name in ("packages/tokens/dist/a.ts", "packages/tokens/a.gen.ts", "packages/ui/a.d.ts",
                     "node_modules/lib/a.js", "LICENSES/upstream/a.py", "templates/a.json"):
            self.write(name, "헤더 없음\n")
        for name in ("tools/a.py", "tests/a.py", "templates/a.sh", ".github/workflows/a.yml",
                     "packages/py/pkg/a.py", "docs/standards/a.yaml", ".editorconfig"):
            self.write(name, HEADER)
        result = self.run_cli()
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("7개 파일", result.stdout)

    def test_empty_scope_is_not_pass(self):
        result = self.run_cli()
        self.assertEqual(result.returncode, 1)
        self.assertIn("검사 대상 0개", result.stdout)

    def test_missing_index_is_not_pass(self):
        (self.root / "PROVENANCE.md").unlink()
        self.write("tools/a.py", HEADER)
        self.assertEqual(self.run_cli().returncode, 1)

    def test_bad_encoding_is_not_pass(self):
        path = self.write("tools/a.py", HEADER)
        path.write_bytes(b"\xff\xfe")
        result = self.run_cli()
        self.assertEqual(result.returncode, 1)
        self.assertNotIn("Traceback", result.stderr)

    def test_stale_index_is_not_pass(self):
        self.port()
        result = self.run_cli()
        self.assertEqual(result.returncode, 1)
        self.assertIn("소스 파일 없음", result.stdout)

    def test_malformed_index_is_not_pass(self):
        self.write("PROVENANCE.md", "| PV-001 | 누락 |\n")
        self.assertEqual(self.run_cli().returncode, 1)


if __name__ == "__main__":
    unittest.main()
