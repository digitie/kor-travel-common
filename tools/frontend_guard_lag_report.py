# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"""frontend guard 지연 보고(ADR-019 결정 3, T-024).

소비자 main의 workflow에서 frontend-consumer-guard 호출 SHA·common-ref와 벤더한
`common-artifacts.json` 버전을 읽어 common 정본(이 checkout)과의 차이를 표로 낸다.
차이는 실패가 아니라 보고다. 읽기 실패를 포함해 어떤 경우에도 exit 0이다.
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import posixpath
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

COMMON = "digitie/kor-travel-common"
CONSUMERS = (
    "digitie/pinvi",
    "digitie/kor-travel-map",
    "digitie/kor-travel-weather",
    "digitie/kor-travel-transport",
    "digitie/kor-travel-docker-manager",
    "digitie/kor-travel-geo",
    "digitie/kor-travel-concierge",
)
POLICY_FILES = ("versions.json", "frontend-dependencies.json", "frontend-artifacts.json")
GUARD = "frontend-consumer-guard.yml"
CALL = re.compile(r"^(?P<indent>[ \t]*)uses:\s*[\"']?digitie/kor-travel-common/\.github/workflows/"
                  + re.escape(GUARD) + r"@(?P<sha>[^\s#\"']+)", re.M)


def _indent(line: str) -> int:
    return len(line) - len(line.lstrip())


def parse_calls(text: str) -> list[dict]:
    """workflow 본문에서 guard 호출마다 줄 번호·호출 SHA·common-ref·root·frontends를 뽑는다."""
    calls = []
    lines = text.splitlines()
    for match in CALL.finditer(text):
        line = text.count("\n", 0, match.start()) + 1
        indent = len(match.group("indent"))
        block = []
        for raw in lines[line:]:
            stripped = raw.strip()
            if stripped and not stripped.startswith("#") and _indent(raw) < indent:
                break
            block.append(raw)
        body = "\n".join(block)
        ref = re.search(r"^\s*common-ref:\s*[\"']?([0-9A-Za-z._/-]+)", body, re.M)
        root = re.search(r"^\s*root:\s*[\"']?([^\"'\s#]+)", body, re.M)
        frontends: list = []
        found = re.search(r"frontends:[^\[]*(\[.*?\}\s*\])", body, re.S)
        if found:
            try:
                frontends = json.loads(found.group(1))
            except ValueError:
                frontends = []
        calls.append({"line": line, "sha": match.group("sha"),
                      "common_ref": ref.group(1) if ref else "",
                      "root": root.group(1) if root else ".", "frontends": frontends})
    return calls


def guard_model(guard_text: str | None) -> str:
    """그 ref의 guard가 정책을 main에서 읽는 옛 판인지 구분한다."""
    if guard_text is None:
        return "읽기 실패"
    if re.search(r"^\s*ref:\s*main\s*$", guard_text, re.M):
        return "옛 판(main 읽음)"
    return "ADR-019(ref 읽음)"


def version_diffs(vendored: dict, canonical: dict) -> list[str]:
    """벤더 원장과 정본 산출물의 버전 차이를 'name 벤더→정본'으로 낸다."""
    result = []
    packages = vendored.get("packages") if isinstance(vendored, dict) else None
    for name, entry in sorted((packages or {}).items()):
        want = (canonical.get("packages") or {}).get(name, {}).get("version")
        got = entry.get("version") if isinstance(entry, dict) else None
        if want and got != want:
            result.append(f"{name} {got}→{want}")
    return result


class GitHub:
    """공개 저장소 읽기 전용 접근. 실패는 None/빈 값으로 돌려 보고를 멈추지 않는다."""

    def __init__(self, token: str | None):
        self.token = token

    def _get(self, path: str) -> bytes:
        headers = {"Accept": "application/vnd.github+json",
                   "User-Agent": "kor-travel-common-lag-report"}
        if self.token:
            headers["Authorization"] = "Bearer " + self.token
        request = urllib.request.Request("https://api.github.com/" + path, headers=headers)
        with urllib.request.urlopen(request, timeout=15) as response:
            return response.read()

    def text(self, repo: str, path: str, ref: str) -> str | None:
        try:
            quoted, ref_q = urllib.parse.quote(path), urllib.parse.quote(ref, safe="")
            data = json.loads(self._get(f"repos/{repo}/contents/{quoted}?ref={ref_q}"))
            return base64.b64decode(data["content"]).decode("utf-8")
        except Exception:  # noqa: BLE001 — 보고는 실패하지 않는다
            return None

    def workflows(self, repo: str) -> list[str]:
        try:
            items = json.loads(self._get(f"repos/{repo}/contents/.github/workflows?ref=main"))
            return sorted(item["path"] for item in items if item.get("type") == "file"
                          and item["path"].endswith((".yml", ".yaml")))
        except Exception:  # noqa: BLE001
            return []

    def behind(self, ref: str, main: str) -> str:
        try:
            pair = urllib.parse.quote(ref, safe="") + "..." + urllib.parse.quote(main, safe="")
            return str(json.loads(self._get(f"repos/{COMMON}/compare/{pair}")).get("ahead_by", "?"))
        except Exception:  # noqa: BLE001
            return "?"


def report(gh: GitHub, common_root: Path, main_sha: str, consumers: tuple[str, ...]) -> list[str]:
    local = {name: (common_root / name).read_text(encoding="utf-8") for name in POLICY_FILES}
    canonical = json.loads(local["frontend-artifacts.json"])
    rows = ["| 저장소 | 호출 위치 | 호출 SHA | common-ref | guard 판 | main보다 뒤 커밋 "
            "| 정책 파일 차이 | 벤더 버전 차이(벤더→정본) |",
            "|---|---|---|---|---|---|---|---|"]
    cache: dict[str, tuple[str, str, str]] = {}
    for repo in consumers:
        calls = [(path, call) for path in gh.workflows(repo)
                 for call in parse_calls(gh.text(repo, path, "main") or "")]
        if not calls:
            rows.append(f"| {repo} | 호출 없음 또는 읽기 실패 | - | - | - | - | - | - |")
        for path, call in calls:
            ref = call["common_ref"] or call["sha"]
            if ref not in cache:
                guard = gh.text(COMMON, ".github/workflows/" + GUARD, ref)
                changed = [name for name in POLICY_FILES if gh.text(COMMON, name, ref) != local[name]]
                cache[ref] = (guard_model(guard), gh.behind(ref, main_sha), ", ".join(changed) or "없음")
            kind, behind, changed = cache[ref]
            diffs = []
            for frontend in call["frontends"]:
                package = frontend.get("package") if isinstance(frontend, dict) else None
                if not isinstance(package, str):
                    continue
                ledger = posixpath.normpath(posixpath.join(
                    call["root"], posixpath.dirname(package), "common-artifacts.json"))
                text = gh.text(repo, ledger, "main")
                if text is None:
                    diffs.append(f"{ledger}: 읽기 실패")
                    continue
                try:
                    found = version_diffs(json.loads(text), canonical)
                except ValueError:
                    found = ["원장 JSON 오류"]
                diffs.extend(f"{ledger}: {item}" for item in found)
            pair = "" if call["sha"] == call["common_ref"] else " (호출 SHA≠common-ref)"
            rows.append(f"| {repo} | `{path}:{call['line']}` | `{call['sha'][:12]}`{pair} "
                        f"| `{ref[:12]}` | {kind} | {behind} | {changed} | "
                        + ("<br>".join(diffs) or "없음") + " |")
    return rows


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="frontend guard 지연 보고(항상 exit 0)")
    parser.add_argument("--common-root", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--main-sha", default=os.environ.get("GITHUB_SHA", "main"))
    parser.add_argument("--repo", action="append", help="소비자(owner/name). 생략하면 일곱 소비자")
    args = parser.parse_args(argv)
    try:
        rows = report(GitHub(os.environ.get("GITHUB_TOKEN") or None), Path(args.common_root),
                      args.main_sha, tuple(args.repo or CONSUMERS))
        text = "\n".join([f"## frontend guard 지연 보고 (정본 common `{args.main_sha[:12]}`)",
                          "", *rows, ""])
    except Exception as error:  # noqa: BLE001 — 지연 보고는 어떤 경우에도 실패하지 않는다
        text = f"## frontend guard 지연 보고\n\n보고를 만들지 못했습니다: {type(error).__name__}\n"
    print(text)
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        try:
            with open(summary, "a", encoding="utf-8") as handle:
                handle.write(text)
        except OSError:
            pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
