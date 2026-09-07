# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"""토큰 별칭 검사기의 정상·고장 주입 경계를 검증한다."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "tools" / "check_aliases.py"
SPEC = importlib.util.spec_from_file_location("check_aliases", SCRIPT)
CHECK = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = CHECK
SPEC.loader.exec_module(CHECK)


class AliasCheckerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="kt-alias-")
        self.addCleanup(self.temp.cleanup)
        self.package = Path(self.temp.name) / "tokens"
        self.aliases = self.package / "aliases"
        self.aliases.mkdir(parents=True)
        self.write("tokens.css", ":root { --kt-brand: red; --kt-text-primary: black; }\n")
        self.write("theme.css", "@theme inline { --color-kt-brand: var(--kt-brand); }\n")
        self.write("shadcn.css", ":root { --border: var(--kt-brand); }\n")
        self.write("aliases/map.css", "@import \"../shadcn.css\";\n:root { --brand: var(--kt-brand); }\n.dark { --brand: var(--kt-brand); }\n")

    def write(self, name: str, text: str) -> Path:
        path = self.package / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8", newline="\n")
        return path

    def errors(self) -> list[str]:
        return CHECK.check_aliases(self.aliases)

    def test_repository_aliases_pass(self) -> None:
        result = subprocess.run(
            [sys.executable, "-B", "-X", "utf8", str(SCRIPT),
             str(Path(__file__).resolve().parents[1] / "packages" / "tokens" / "aliases")],
            text=True, encoding="utf-8", capture_output=True, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("오류 0개", result.stdout)

    def test_repository_exposes_shared_weather_vocabulary(self) -> None:
        root = Path(__file__).resolve().parents[1] / "packages" / "tokens"
        text = (root / "aliases" / "map-vocabulary.css").read_text(encoding="utf-8")
        text += (root / "shadcn.css").read_text(encoding="utf-8")
        names = {
            "surface-page", "surface-subtle", "surface-muted", "surface-card", "card",
            "text-primary", "text-secondary", "text-tertiary", "text-disabled", "text-strong",
            "icon-default", "border", "control-line", "brand", "brand-hover", "brand-tint",
            "brand-foreground", "focus", "success", "success-tint", "warning", "warning-tint",
            "info", "info-tint", "destructive", "destructive-tint", "radius-control",
            "radius-panel", "control-h", "control-h-sm", "rail", "duration-fast",
            "duration-base", "ease-out", "ease-in", "shadow-elevated", "shadow-modal",
            "font-sans", "font-mono",
        }
        for name in names:
            self.assertIn(f"--{name}:", text, name)

    def test_weather_spacing_stays_in_nonpackaged_example(self) -> None:
        root = Path(__file__).resolve().parents[1] / "packages" / "tokens"
        alias_text = (root / "aliases" / "map-vocabulary.css").read_text(encoding="utf-8")
        example_text = (root / "examples" / "weather-overrides.css").read_text(encoding="utf-8")
        for name in ("3xs", "2xs", "xs", "sm", "md", "lg", "xl", "2xl"):
            self.assertNotIn(f"--space-{name}:", alias_text)
            self.assertIn(f"--space-{name}:", example_text)

    def test_weather_override_keeps_navy_and_rail_contract(self) -> None:
        path = Path(__file__).resolve().parents[1] / "packages" / "tokens" / "examples" / "weather-overrides.css"
        text = path.read_text(encoding="utf-8")
        for value in (
            "--kt-brand: oklch(47% 0.14 255)",
            "--kt-brand-hover: oklch(41% 0.15 255)",
            "--kt-brand-tint: oklch(95% 0.025 250)",
            "--kt-brand-foreground: oklch(99% 0.002 250)",
            "--kt-rail: 17rem",
        ):
            self.assertIn(value, text)
        self.assertIn('--kt-font-mono: var(--font-geist-mono, "Geist Mono")', text)
        self.assertIn("--kt-ease-in: cubic-bezier(0.7, 0, 0.84, 1)", text)

    def test_alias_radius_md_uses_map_contract_and_weather_override(self) -> None:
        path = Path(__file__).resolve().parents[1] / "packages" / "tokens" / "aliases" / "map-vocabulary.css"
        text = path.read_text(encoding="utf-8")
        self.assertEqual(text.count("--radius-md: var(--kt-radius-control);"), 2)
        example = (path.parent.parent / "examples" / "weather-overrides.css").read_text(encoding="utf-8")
        self.assertEqual(example.count("--radius-md: var(--kt-radius-panel);"), 2)

    def test_imported_shadcn_names_are_not_duplicate_alias_definitions(self) -> None:
        self.assertEqual(self.errors(), [])

    def test_undefined_kt_reference_fails(self) -> None:
        self.write("aliases/map.css", ":root { --brand: var(--kt-missing); }\n")
        self.assertTrue(any("미정의" in error for error in self.errors()))

    def test_kt_definition_fails(self) -> None:
        self.write("aliases/map.css", ":root { --kt-brand: red; }\n")
        self.assertTrue(any("--kt-* 정의 금지" in error for error in self.errors()))

    def test_kt_definition_without_final_semicolon_fails(self) -> None:
        self.write("aliases/map.css", ":root { --kt-brand: red }\n.dark { --kt-brand: red }\n")
        self.assertTrue(any("--kt-* 정의 금지" in error for error in self.errors()))

    def test_uppercase_var_undefined_reference_fails(self) -> None:
        self.write(
            "aliases/map.css",
            ":root { --brand: VAR(--kt-missing); }\n.dark { --brand: VAR(--kt-missing); }\n",
        )
        self.assertTrue(any("미정의" in error for error in self.errors()))

    def test_escaped_custom_property_is_rejected(self) -> None:
        escaped = chr(92) + "6b"
        self.write(
            "aliases/map.css",
            f":root {{ --{escaped} t-brand: red; }}\n.dark {{ --{escaped} t-brand: red; }}\n",
        )
        self.assertTrue(any("지원하지 않는 CSS" in error for error in self.errors()))

    def test_escaped_var_reference_is_rejected(self) -> None:
        escaped = chr(92) + "6b"
        self.write(
            "aliases/map.css",
            f":root {{ --brand: var(--{escaped} t-missing); }}\n"
            f".dark {{ --brand: var(--{escaped} t-missing); }}\n",
        )
        self.assertTrue(any("지원하지 않는 CSS" in error for error in self.errors()))

    def test_escaped_var_function_name_is_rejected(self) -> None:
        escaped = chr(92) + "61r"
        self.write(
            "aliases/map.css",
            f":root {{ --brand: v{escaped}(--kt-missing); }}\n"
            f".dark {{ --brand: v{escaped}(--kt-missing); }}\n",
        )
        self.assertTrue(any("지원하지 않는 CSS" in error for error in self.errors()))

    def test_escaped_import_name_is_rejected(self) -> None:
        escaped = chr(92) + "69mport"
        self.write(
            "aliases/map.css",
            f"@{escaped} \"../shadcn.css\";\n"
            ":root { --brand: var(--kt-brand); }\n.dark { --brand: var(--kt-brand); }\n",
        )
        self.assertTrue(any("지원하지 않는 CSS" in error for error in self.errors()))

    def test_escaped_import_target_is_rejected(self) -> None:
        self.write(
            "aliases/map.css",
            '@import "../sha' + chr(92) + '64cn.css";\n'
            ":root { --brand: var(--kt-brand); }\n.dark { --brand: var(--kt-brand); }\n",
        )
        self.assertTrue(any("지원하지 않는 CSS" in error for error in self.errors()))

    def test_unicode_custom_property_definition_is_rejected(self) -> None:
        self.write(
            "aliases/map.css",
            ":root { --kt-한글: red; }\n.dark { --kt-한글: red; }\n",
        )
        self.assertTrue(any("--kt-* 정의 금지" in error for error in self.errors()))

    def test_unicode_kt_reference_is_checked(self) -> None:
        self.write(
            "aliases/map.css",
            ":root { --brand: var(--kt-없는); }\n.dark { --brand: var(--kt-없는); }\n",
        )
        self.assertTrue(any("미정의" in error for error in self.errors()))

    def test_var_text_in_string_is_not_a_reference(self) -> None:
        self.write(
            "aliases/map.css",
            ':root { --brand: "var(--kt-missing)"; }\n.dark { --brand: "var(--kt-missing)"; }\n',
        )
        self.assertFalse(any("미정의" in error for error in self.errors()))

    def test_dark_block_is_required(self) -> None:
        self.write("aliases/map.css", ":root { --brand: var(--kt-brand); }\n")
        self.assertTrue(any(".dark 블록" in error for error in self.errors()))

    def test_combined_root_dark_selector_counts_for_both_modes(self) -> None:
        self.write("aliases/map.css", ":root, .dark { --brand: var(--kt-brand); }\n")
        self.assertEqual(self.errors(), [])

    def test_descendant_dark_selector_does_not_count_as_dark_mode(self) -> None:
        self.write(
            "aliases/map.css",
            ":root { --brand: var(--kt-brand); }\n"
            ".dark .child { --brand: var(--kt-brand); }\n",
        )
        self.assertTrue(any(".dark 블록" in error for error in self.errors()))

    def test_nested_dark_selector_does_not_count_as_dark_mode(self) -> None:
        self.write(
            "aliases/map.css",
            "@media print { .dark { --brand: var(--kt-brand); } }\n"
            ":root { --brand: var(--kt-brand); }\n",
        )
        self.assertTrue(any(".dark 블록" in error for error in self.errors()))

    def test_combined_selector_duplicate_is_detected_per_mode(self) -> None:
        self.write(
            "aliases/map.css",
            ":root, .dark { --brand: var(--kt-brand); }\n"
            ":root { --brand: var(--kt-brand); }\n",
        )
        self.assertTrue(any("별칭 중복 선언" in error for error in self.errors()))

    def test_error_redacts_identifiers_and_relative_paths(self) -> None:
        marker = "ghp_" + "Q" * 36
        self.write("aliases/" + marker + ".css", f":root {{ --kt-{marker}: red; }}\n")
        self.write(
            "aliases/map.css",
            f'@import "./{marker}.css";\n'
            ":root { --brand: var(--kt-brand); }\n.dark { --brand: var(--kt-brand); }\n",
        )
        output = "\n".join(self.errors())
        self.assertNotIn(marker, output)

    @unittest.skipUnless(sys.platform == "win32", "Windows 8.3 경로 API가 필요함")
    def test_windows_short_path_is_accepted(self) -> None:
        import ctypes

        buffer = ctypes.create_unicode_buffer(32768)
        length = ctypes.windll.kernel32.GetShortPathNameW(
            str(self.aliases), buffer, len(buffer)
        )
        if not length:
            self.skipTest("Windows 8.3 경로를 사용할 수 없음")
        short_path = buffer.value
        result = subprocess.run(
            [sys.executable, "-B", "-X", "utf8", str(SCRIPT), short_path],
            text=True, encoding="utf-8", capture_output=True, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_theme_namespace_exact_collision_fails(self) -> None:
        self.write("theme.css", "@theme { --color-ink: red; }\n")
        self.write("aliases/map.css", ":root { --color-ink: var(--kt-brand); }\n")
        self.assertTrue(any("Tailwind @theme 이름 충돌" in error for error in self.errors()))

    def test_shadcn_duplicate_fails(self) -> None:
        self.write("aliases/map.css", ":root { --border: var(--kt-brand); }\n")
        self.assertTrue(any("shadcn.css 이름 중복" in error for error in self.errors()))

    def test_import_outside_package_fails(self) -> None:
        self.write("aliases/map.css", "@import \"../../outside.css\";\n")
        self.assertTrue(any("패키지 밖" in error for error in self.errors()))

    def test_same_line_url_and_media_import_outside_fails(self) -> None:
        self.write(
            "aliases/map.css",
            '@import "../shadcn.css"; @import url("../../outside.css") screen;\n'
            ':root { --brand: var(--kt-brand); }\n.dark { --brand: var(--kt-brand); }\n',
        )
        self.assertTrue(any("패키지 밖" in error for error in self.errors()))

    def test_url_import_inside_package_passes(self) -> None:
        self.write(
            "aliases/map.css",
            '@import url("../shadcn.css") screen;\n:root { --brand: var(--kt-brand); }\n'
            '.dark { --brand: var(--kt-brand); }\n',
        )
        self.assertEqual(self.errors(), [])

    def test_recursive_imported_kt_definition_fails(self) -> None:
        self.write("extra.css", ":root { --kt-brand: red; }\n")
        self.write(
            "aliases/map.css",
            '@import "../extra.css";\n:root { --brand: var(--kt-brand); }\n'
            '.dark { --brand: var(--kt-brand); }\n',
        )
        self.assertTrue(any("--kt-* 정의 금지" in error for error in self.errors()))

    def test_recursive_imported_shadcn_duplicate_fails(self) -> None:
        self.write("extra.css", ":root { --border: red; }\n")
        self.write(
            "aliases/map.css",
            '@import "../extra.css";\n:root { --brand: var(--kt-brand); }\n'
            '.dark { --brand: var(--kt-brand); }\n',
        )
        self.assertTrue(any("shadcn.css 이름 중복" in error for error in self.errors()))

    def test_import_cycle_returns_controlled_error(self) -> None:
        self.write("a.css", '@import "b.css";\n')
        self.write("b.css", '@import "a.css";\n')
        self.write(
            "aliases/map.css",
            '@import "../a.css";\n:root { --brand: var(--kt-brand); }\n'
            '.dark { --brand: var(--kt-brand); }\n',
        )
        self.assertTrue(any("순환" in error for error in self.errors()))

    def test_invalid_css_returns_controlled_error(self) -> None:
        path = self.package / "aliases" / "map.css"
        path.write_bytes(b":root { --brand: \xff; }\n")
        errors = self.errors()
        self.assertTrue(errors)
        self.assertFalse(any("Traceback" in error for error in errors))

    def test_error_does_not_echo_import_target(self) -> None:
        marker = "SECRET_MARKER_9f2d"
        self.write("aliases/map.css", f'@import url("../../{marker}.css");\n')
        result = subprocess.run(
            [sys.executable, "-B", "-X", "utf8", str(SCRIPT), str(self.aliases)],
            text=True, encoding="utf-8", capture_output=True, check=False,
        )
        self.assertNotIn(marker, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
