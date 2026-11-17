# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"""frontend guard 지연 보고의 파싱과 '항상 exit 0'을 네트워크 없이 확인한다."""
from __future__ import annotations

import io
import json
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import frontend_guard_lag_report as lag  # noqa: E402

OLD = "97f8ed98360518e7afc96e89a5b45a6a478ac955"
WORKFLOW = f"""name: ci
jobs:
  frontend-policy:
    uses: digitie/kor-travel-common/.github/workflows/frontend-consumer-guard.yml@{OLD}
    with:
      common-ref: {OLD}
      frontends: >-
        [{{"package":"frontend/package.json","lock":"frontend/package-lock.json","workspace":"","profile":"web"}}]
      node-dockerfiles: '["frontend/Dockerfile"]'
  other:
    runs-on: ubuntu-24.04
    steps:
      - run: echo common-ref: ffff
"""


class FakeGitHub:
    def __init__(self, files: dict[tuple[str, str, str], str], fail: bool = False):
        self.files, self.fail = files, fail

    def workflows(self, repo):
        if self.fail:
            raise RuntimeError("network")
        return sorted(path for (r, path, _ref) in self.files if r == repo and path.startswith(".github/"))

    def text(self, repo, path, ref):
        return self.files.get((repo, path, ref))

    def behind(self, ref, main):
        return "3"


class LagReportTest(unittest.TestCase):
    def test_parse_call_block(self):
        calls = lag.parse_calls(WORKFLOW)
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0]["line"], 4)
        self.assertEqual(calls[0]["sha"], OLD)
        self.assertEqual(calls[0]["common_ref"], OLD)
        self.assertEqual(calls[0]["root"], ".")
        self.assertEqual(calls[0]["frontends"][0]["package"], "frontend/package.json")

    def test_guard_model(self):
        self.assertEqual(lag.guard_model("        with:\n          ref: main\n"), "옛 판(main 읽음)")
        self.assertEqual(lag.guard_model("ref: ${{ inputs.common-ref }}\n"), "ADR-019(ref 읽음)")
        self.assertEqual(lag.guard_model(None), "읽기 실패")

    def test_report_marks_version_and_policy_drift(self):
        canonical = json.loads((ROOT / "frontend-artifacts.json").read_text(encoding="utf-8"))
        name = "@kor-travel/tokens"
        vendored = {"packages": {name: {"version": "0.0.1"}}}
        repo = "digitie/example"
        files = {
            (repo, ".github/workflows/ci.yml", "main"): WORKFLOW,
            (repo, "frontend/common-artifacts.json", "main"): json.dumps(vendored),
            (lag.COMMON, ".github/workflows/" + lag.GUARD, OLD): "ref: main\n",
        }
        rows = lag.report(FakeGitHub(files), ROOT, "main", (repo,))
        row = rows[-1]
        self.assertIn("`.github/workflows/ci.yml:4`", row)
        self.assertIn("옛 판(main 읽음)", row)
        self.assertIn("versions.json", row)  # ref의 정책 파일을 읽지 못하면 차이로 표시한다
        self.assertIn(f"{name} 0.0.1→{canonical['packages'][name]['version']}", row)

    def test_main_never_fails(self):
        original = lag.report
        lag.report = lambda *args: (_ for _ in ()).throw(RuntimeError("boom"))
        try:
            with redirect_stdout(io.StringIO()) as out:
                self.assertEqual(lag.main(["--main-sha", "main", "--repo", "digitie/x"]), 0)
            self.assertIn("보고를 만들지 못했습니다", out.getvalue())
        finally:
            lag.report = original


if __name__ == "__main__":
    unittest.main()
