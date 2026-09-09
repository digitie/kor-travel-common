# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"""OpenAPI 예외 레지스트리 파서·생성물 drift 회귀 시험."""

from __future__ import annotations

from datetime import date
import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "openapi_exceptions.py"
SPEC = importlib.util.spec_from_file_location("kor_travel_common_openapi_exceptions", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
OE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = OE
SPEC.loader.exec_module(OE)


class OpenApiExceptionsTest(unittest.TestCase):
    def test_canonical_registry_has_exact_schema_and_rule_coverage(self) -> None:
        registry = OE.load_registry(as_of=date(2026, 9, 9))
        self.assertEqual(registry["schema"], "kor-travel-common.openapi-exceptions.v1")
        self.assertEqual(set(registry["apps"]), OE.ALLOWED_APPS)
        self.assertEqual(len(registry["exceptions"]), 46)
        self.assertTrue(all(set(entry) == OE.ENTRY_KEYS for entry in registry["exceptions"]))
        self.assertTrue(OE.CORE_RULE_IDS.issubset(OE._rule_ids()))

    def test_generated_markdown_is_current(self) -> None:
        passed, message = OE.check()
        self.assertTrue(passed, message)
        self.assertIn("46건", OE.render_markdown(OE.load_registry()))

    def test_drift_is_a_failure(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "openapi-exceptions.md"
            output.write_text("stale\n", encoding="utf-8")
            passed, message = OE.check(output_path=output)
        self.assertFalse(passed)
        self.assertIn("drift", message)

    def test_duplicate_key_is_rejected(self) -> None:
        text = OE.DEFAULT_INPUT.read_text(encoding="utf-8")
        text = text.replace("  - app: geo\n    rule: M3\n", "  - app: geo\n    rule: M3\n    rule: M3\n", 1)
        self._assert_invalid(text, "중복 YAML 키")

    def test_unknown_entry_key_is_rejected(self) -> None:
        text = OE.DEFAULT_INPUT.read_text(encoding="utf-8")
        text = text.replace("    owner: kor-travel-geo\n", "    owners: kor-travel-geo\n", 1)
        self._assert_invalid(text, "키는 정확히")

    def test_unknown_rule_is_rejected(self) -> None:
        text = OE.DEFAULT_INPUT.read_text(encoding="utf-8")
        text = text.replace("    rule: M3\n", "    rule: M99\n", 1)
        self._assert_invalid(text, "규칙 문서에 없음")

    def test_immediate_must_cannot_have_indefinite_sunset(self) -> None:
        text = OE.DEFAULT_INPUT.read_text(encoding="utf-8")
        text = text.replace(
            "  - app: airport\n    rule: M4\n    surface: \"*\"\n    reason: \"요청 ID 미구현(oa §2.5). 계층 1 규칙이므로 기한부. T-482에서 additive 추가.\"\n    sunset: \"2026-12-31\"",
            "  - app: airport\n    rule: M4\n    surface: \"*\"\n    reason: \"요청 ID 미구현(oa §2.5). 계층 1 규칙이므로 기한부. T-482에서 additive 추가.\"\n    sunset: null",
            1,
        )
        self._assert_invalid(text, "sunset을 null")

    def test_header_and_request_id_contract_is_documented(self) -> None:
        text = (ROOT / "docs" / "standards" / "openapi.md").read_text(encoding="utf-8")
        for required in ("UUID v4/v7", "ULID", "128자", "trust_incoming=False", "AppId"):
            self.assertIn(required, text)
        for suffix in ("Api-Key", "Service-Token", "Actor", "Admin-Proxy-Secret", "Ops-Token", "Ops-Scope"):
            self.assertIn(f"`{suffix}`", text)
        self.assertNotIn("`Roles`", text)
        self.assertIn("O-14", text)
        self.assertIn("OpenAPI 산출물↔Zod", text)

    def _assert_invalid(self, text: str, expected: str) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "registry.yaml"
            path.write_text(text, encoding="utf-8")
            with self.assertRaises(OE.RegistryError) as context:
                OE.load_registry(path, as_of=date(2026, 9, 9))
        self.assertIn(expected, str(context.exception))


if __name__ == "__main__":
    unittest.main()
