# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"""OpenAPI 예외 레지스트리 파서·생성물 drift 회귀 시험."""

from __future__ import annotations

from datetime import date
import importlib.util
import os
from pathlib import Path
import re
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
        self.assertEqual(len(registry["exceptions"]), 39)
        self.assertTrue(all(set(entry) == OE.ENTRY_KEYS for entry in registry["exceptions"]))
        self.assertTrue(OE.CORE_RULE_IDS.issubset(OE._rule_ids()))

    def test_generated_markdown_is_current(self) -> None:
        passed, message = OE.check()
        self.assertTrue(passed, message)
        self.assertIn("39건", OE.render_markdown(OE.load_registry()))

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

    def test_future_updated_is_rejected(self) -> None:
        text = OE.DEFAULT_INPUT.read_text(encoding="utf-8").replace(
            'updated: "2026-09-06"', 'updated: "2099-01-01"', 1
        )
        self._assert_invalid(text, "미래일 수 없음")

    def test_reason_requires_reference_id(self) -> None:
        text = self._replace_first_line(OE.DEFAULT_INPUT.read_text(encoding="utf-8"), "reason:", '    reason: "근거만 있고 추적 ID 없음"')
        self._assert_invalid(text, "정합 task ID")

    def test_reason_rejects_undefined_task_id(self) -> None:
        text = self._replace_first_line(
            OE.DEFAULT_INPUT.read_text(encoding="utf-8"), "reason:", '    reason: "근거와 T-999 정합 task"'
        )
        self._assert_invalid(text, "정의되지 않은 task ID")

    def test_reason_requires_task_file_not_body_reference(self) -> None:
        text = self._replace_first_line(
            OE.DEFAULT_INPUT.read_text(encoding="utf-8"), "reason:", '    reason: "근거와 T-034 정합 task"'
        )
        self._assert_invalid(text, "정의되지 않은 task ID")

    def test_should_exception_requires_external_contract_surface(self) -> None:
        text = OE.DEFAULT_INPUT.read_text(encoding="utf-8").replace(
            '    surface: "/v2/*"\n    reason: "v2 성공 envelope',
            '    surface: "*"\n    reason: "v2 성공 envelope',
            1,
        )
        self._assert_invalid(text, "외부 계약")

    def test_should_exception_requires_canonical_surface_and_positive_contract_evidence(self) -> None:
        text = OE.DEFAULT_INPUT.read_text(encoding="utf-8").replace(
            '    surface: "/v2/*"\n    reason: "v2 성공 envelope',
            '    surface: "/v2/* "\n    reason: "v2 성공 envelope',
            1,
        )
        self._assert_invalid(text, "양끝 공백")
        text = OE.DEFAULT_INPUT.read_text(encoding="utf-8").replace(
            "Pinvi가 직접 소비하는 외부 계약", "외부 계약 동반 PR 근거 없음", 1
        )
        self._assert_invalid(text, "외부 계약")

    def test_plain_numeric_scalar_is_rejected(self) -> None:
        text = OE.DEFAULT_INPUT.read_text(encoding="utf-8").replace(
            "    owner: kor-travel-geo", "    owner: 123", 1
        )
        self._assert_invalid(text, "plain scalar")

    def test_all_yaml_numeric_and_timestamp_plain_scalars_are_rejected(self) -> None:
        for value in (
            "0x10",
            "0o10",
            "0b10",
            "0123",
            "1_000",
            ".5",
            "1.",
            "2026-09-06",
            "2026-09-06T00:00:00Z",
            "2026-09-06T00:00:00+09:00",
            "1:20:30.15",
        ):
            with self.subTest(value=value):
                text = OE.DEFAULT_INPUT.read_text(encoding="utf-8").replace(
                    "    owner: kor-travel-geo", f"    owner: {value}", 1
                )
                self._assert_invalid(text, "plain scalar")

    def test_control_and_surrogate_scalars_are_rejected(self) -> None:
        control = self._replace_first_line(
            OE.DEFAULT_INPUT.read_text(encoding="utf-8"), "reason:", '    reason: "bad\\u0000value"'
        )
        self._assert_invalid(control, "제어·format")
        surrogate = self._replace_first_line(
            OE.DEFAULT_INPUT.read_text(encoding="utf-8"), "reason:", '    reason: "bad\\ud800value"'
        )
        self._assert_invalid(surrogate, "surrogate")

    def test_unicode_control_format_and_line_separator_scalars_are_rejected(self) -> None:
        for escaped in (r"\u0080", r"\u2028", r"\u2029", r"\u202e", r"\u200b", r"\ufeff"):
            with self.subTest(escaped=escaped):
                text = self._replace_first_line(
                    OE.DEFAULT_INPUT.read_text(encoding="utf-8"),
                    "reason:",
                    f'    reason: "bad{escaped}value T-483"',
                )
                self._assert_invalid(text, "제어·format")

    def test_utf8_bom_is_allowed_only_at_document_start(self) -> None:
        text = "\ufeff" + OE.DEFAULT_INPUT.read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "registry.yaml"
            path.write_text(text, encoding="utf-8")
            self.assertEqual(OE.load_registry(path, as_of=date(2026, 9, 9))["schema"], "kor-travel-common.openapi-exceptions.v1")

    def test_single_quote_escape_is_supported(self) -> None:
        text = self._replace_first_line(
            OE.DEFAULT_INPUT.read_text(encoding="utf-8"), "reason:", "    reason: 'VWorld ''legacy'' 계약 T-483'"
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "registry.yaml"
            path.write_text(text, encoding="utf-8")
            registry = OE.load_registry(path, as_of=date(2026, 9, 9))
        self.assertIn("VWorld 'legacy' 계약", registry["exceptions"][0]["reason"])

    def test_markdown_cells_escape_markup(self) -> None:
        registry = OE.load_registry(as_of=date(2026, 9, 9))
        registry["exceptions"][0]["reason"] = "<img src=x onerror=x> [x](https://evil) `code` *em*"
        rendered = OE.render_markdown(registry)
        self.assertNotIn("<img", rendered)
        self.assertNotIn("[x](https://evil)", rendered)
        self.assertNotIn("`code`", rendered)
        self.assertIn("&lt;img", rendered)
        self.assertIn("&#91;x&#93;&#40;https://evil&#41;", rendered)

    def test_markdown_cells_reject_unicode_format_controls_after_load(self) -> None:
        registry = OE.load_registry(as_of=date(2026, 9, 9))
        registry["exceptions"][0]["reason"] = "bad\u202evalue T-483"
        with self.assertRaises(OE.RegistryError) as context:
            OE.render_markdown(registry)
        self.assertIn("제어·format", str(context.exception))

    def test_write_rejects_input_output_alias_and_preserves_input(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "same.yaml"
            original = OE.DEFAULT_INPUT.read_text(encoding="utf-8")
            path.write_text(original, encoding="utf-8")
            with self.assertRaises(OE.RegistryError):
                OE.generate(path, path)
            self.assertEqual(path.read_text(encoding="utf-8"), original)

    def test_write_rejects_hardlink_alias(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            input_path = Path(directory) / "input.yaml"
            alias_path = Path(directory) / "alias.yaml"
            input_path.write_text(OE.DEFAULT_INPUT.read_text(encoding="utf-8"), encoding="utf-8")
            try:
                os.link(input_path, alias_path)
            except OSError as exc:  # pragma: no cover - filesystem capability varies
                self.skipTest(f"hardlink을 만들 수 없음: {exc}")
            with self.assertRaises(OE.RegistryError):
                OE.generate(input_path, alias_path)

    def test_atomic_write_preserves_existing_output_on_invalid_scalar(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            input_path = Path(directory) / "registry.yaml"
            output_path = Path(directory) / "generated.md"
            text = self._replace_first_line(
                OE.DEFAULT_INPUT.read_text(encoding="utf-8"), "reason:", '    reason: "bad\\ud800value"'
            )
            input_path.write_text(text, encoding="utf-8")
            output_path.write_text("기존 생성물\n", encoding="utf-8")
            with self.assertRaises(OE.RegistryError):
                OE.generate(input_path, output_path)
            self.assertEqual(output_path.read_text(encoding="utf-8"), "기존 생성물\n")

    def test_openapi_rule_tables_keep_seven_columns_and_m10_tier(self) -> None:
        text = (ROOT / "docs" / "standards" / "openapi.md").read_text(encoding="utf-8")
        tables: list[list[list[str]]] = []
        lines = text.splitlines()
        for index, line in enumerate(lines):
            if not line.startswith("| ID | 계층 |") or "검사 수단" not in line:
                continue
            rows: list[list[str]] = []
            for candidate in lines[index + 2 :]:
                if not candidate.startswith("|"):
                    break
                cells = [cell.strip() for cell in re.split(r"(?<!\\)\|", candidate.strip("|"))]
                if all(set(cell) <= {"-"} for cell in cells):
                    continue
                rows.append(cells)
            tables.append(rows)
        self.assertEqual(len(tables), 3)
        for rows in tables:
            self.assertTrue(rows)
            self.assertTrue(all(len(row) == 7 for row in rows))
        rule_rows = [row for table in tables for row in table]
        rule_ids = {row[0] for row in rule_rows}
        self.assertTrue(OE.CORE_RULE_IDS.issubset(rule_ids))
        self.assertIn("M10", rule_ids)
        m10 = next(row for row in rule_rows if row[0] == "M10")
        self.assertEqual(m10[1], "교차 저장소 MUST")
        self.assertIn("pinvi", m10[2])
        immediate = next(line for line in lines if line.startswith("| 1. 즉시 MUST |"))
        self.assertIn("M2·M4·M9·N6·N7", immediate)
        self.assertNotIn("M10", immediate)

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

    @staticmethod
    def _replace_first_line(text: str, prefix: str, replacement: str) -> str:
        lines = text.splitlines()
        for index, line in enumerate(lines):
            if line.strip().startswith(prefix):
                lines[index] = replacement
                return "\n".join(lines) + "\n"
        raise AssertionError(f"line not found: {prefix}")


if __name__ == "__main__":
    unittest.main()
