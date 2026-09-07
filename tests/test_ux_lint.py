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

    def test_all_patterns_report_and_comments_backticks_are_ignored(self):
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
            self.assertEqual(sum(item["pattern"] == "P8" for item in payload["findings"]), 1)

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

    @staticmethod
    def git(root: Path, *args: str) -> None:
        result = subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True)
        if result.returncode:
            raise AssertionError(result.stderr)


if __name__ == "__main__":
    unittest.main()
