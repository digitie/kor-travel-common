# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"""`--kt-*` 색 토큰의 WCAG 대비를 검사하는 표준 라이브러리 도구."""

from __future__ import annotations

import argparse
import datetime as _datetime
import json
import math
import os
from pathlib import Path
import re
import sys
from dataclasses import dataclass
from typing import Iterable, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TOKENS = ROOT / "packages" / "tokens" / "tokens.css"


class ContrastError(ValueError):
    """입력 CSS 또는 baseline이 계약을 위반했을 때 발생한다."""


@dataclass(frozen=True)
class Color:
    """선형 sRGB 색과 불투명도를 보관한다."""

    red: float
    green: float
    blue: float
    alpha: float = 1.0

    def luminance(self) -> float:
        """WCAG 상대 휘도를 계산한다."""

        red, green, blue = (max(0.0, min(1.0, value)) for value in (self.red, self.green, self.blue))
        return 0.2126 * red + 0.7152 * green + 0.0722 * blue


@dataclass(frozen=True)
class Pair:
    """검사할 전경·배경 의미 토큰 쌍."""

    name: str
    foreground: str
    background: str
    required: float


PAIRS: tuple[Pair, ...] = tuple(
    [
        Pair(f"text-{text}/surface-{surface}", f"text-{text}", f"surface-{surface}", 4.5)
        for text in ("primary", "secondary", "strong", "tertiary")
        for surface in ("page", "subtle", "card")
    ]
    + [
        Pair(f"icon/surface-{surface}", "icon", f"surface-{surface}", 3.0)
        for surface in ("page", "subtle", "muted", "card")
    ]
    + [
        Pair(f"control-line/surface-{surface}", "control-line", f"surface-{surface}", 3.0)
        for surface in ("page", "subtle", "muted", "card")
    ]
    + [Pair("focus/surface-page", "focus", "surface-page", 3.0)]
    + [Pair("brand-foreground/brand", "brand-foreground", "brand", 4.5)]
    + [Pair("brand/brand-tint", "brand", "brand-tint", 3.0)]
    + [
        Pair(f"{status}/{status}-tint", status, f"{status}-tint", 4.5)
        for status in ("success", "warning", "info", "destructive")
    ]
)


_DECLARATION = re.compile(r"(--kt-[\w-]+)\s*:\s*([^;{}]+)", re.ASCII)
_VAR = re.compile(r"^var\(\s*(--kt-[\w-]+)(?:\s*,\s*(.*))?\s*\)$", re.ASCII)
_OKLCH = re.compile(
    r"^oklch\(\s*([+-]?(?:\d+(?:\.\d*)?|\.\d+)%?)\s+"
    r"([+-]?(?:\d+(?:\.\d*)?|\.\d+)%?)\s+"
    r"([+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:deg|grad|rad|turn)?)"
    r"(?:\s*/\s*([+-]?(?:\d+(?:\.\d*)?|\.\d+)%?))?\s*\)$",
    re.IGNORECASE,
)
_HEX = re.compile(r"^#([0-9a-f]{3,4}|[0-9a-f]{6}|[0-9a-f]{8})$", re.IGNORECASE)


def _strip_css_comments(text: str) -> str:
    """CSS 주석을 공백으로 치환해 줄 위치와 블록을 보존한다."""

    return re.sub(r"/\*.*?\*/", lambda match: "".join("\n" if char == "\n" else " " for char in match.group()), text, flags=re.DOTALL)


def _selector_mode(selector: str, parent_dark: bool) -> str | None:
    normalized = re.sub(r"\s+", " ", selector.strip().lower())
    if not normalized:
        return "dark" if parent_dark else "light"
    if "prefers-color-scheme: dark" in normalized or ".dark" in normalized or "[data-theme=\"dark\"]" in normalized:
        return "dark"
    if ":root" in normalized or "[data-theme=\"light\"]" in normalized:
        return "dark" if parent_dark else "light"
    return "dark" if parent_dark else None


def _parse_blocks(text: str, parent_dark: bool = False) -> Iterable[tuple[str, str]]:
    """중첩된 at-rule을 포함해 선언 블록과 적용 모드를 반환한다."""

    index = 0
    length = len(text)
    while index < length:
        opening = text.find("{", index)
        if opening < 0:
            break
        selector = text[index:opening]
        depth = 1
        cursor = opening + 1
        quote: str | None = None
        while cursor < length and depth:
            char = text[cursor]
            if quote:
                if char == "\\":
                    cursor += 2
                    continue
                if char == quote:
                    quote = None
            elif char in "\"'":
                quote = char
            elif char == "{":
                depth += 1
            elif char == "}":
                depth -= 1
            cursor += 1
        if depth:
            raise ContrastError("CSS 블록이 닫히지 않았습니다")
        body = text[opening + 1 : cursor - 1]
        mode = _selector_mode(selector, parent_dark)
        if mode is not None:
            yield mode, body
        if "@" in selector.strip() or mode is None:
            yield from _parse_blocks(body, parent_dark=(mode == "dark" or parent_dark))
        index = cursor


def parse_css(paths: Sequence[Path], dark: bool) -> dict[str, str]:
    """CSS 파일을 순서대로 읽어 선택된 모드의 `--kt-*` 선언을 병합한다."""

    values: dict[str, str] = {}
    for path in paths:
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            raise ContrastError(f"CSS 입력을 읽을 수 없습니다: {path.name}") from error
        cleaned = _strip_css_comments(text)
        for mode, body in _parse_blocks(cleaned):
            if (mode == "dark") != dark:
                continue
            for name, value in _DECLARATION.findall(body):
                values[name] = value.strip()
    if not values:
        raise ContrastError("선택한 모드에서 --kt-* 선언을 찾지 못했습니다")
    return values


def _parse_number(value: str, percent_scale: float = 1.0) -> float:
    value = value.strip().lower()
    if value.endswith("%"):
        return float(value[:-1]) / 100.0 * percent_scale
    return float(value) * percent_scale


def _angle(value: str) -> float:
    value = value.strip().lower()
    if value.endswith("deg"):
        return float(value[:-3])
    if value.endswith("grad"):
        return float(value[:-4]) * 0.9
    if value.endswith("rad"):
        return math.degrees(float(value[:-3]))
    if value.endswith("turn"):
        return float(value[:-4]) * 360.0
    return float(value)


def _srgb_to_linear(value: float) -> float:
    return value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4


def _oklch(value: str) -> Color:
    match = _OKLCH.fullmatch(value)
    if not match:
        raise ContrastError(f"지원하지 않는 색 형식: {value[:40]}")
    lightness = _parse_number(match.group(1), 1.0 if not match.group(1).endswith("%") else 1.0)
    chroma = _parse_number(match.group(2), 0.01 if match.group(2).endswith("%") else 1.0)
    hue = math.radians(_angle(match.group(3)))
    alpha = _parse_number(match.group(4), 1.0) if match.group(4) else 1.0
    a = chroma * math.cos(hue)
    b = chroma * math.sin(hue)
    l_value = lightness + 0.3963377774 * a + 0.2158037573 * b
    m_value = lightness - 0.1055613458 * a - 0.0638541728 * b
    s_value = lightness - 0.0894841775 * a - 1.2914855480 * b
    l_value, m_value, s_value = l_value**3, m_value**3, s_value**3
    return Color(
        4.0767416621 * l_value - 3.3077115913 * m_value + 0.2309699292 * s_value,
        -1.2684380046 * l_value + 2.6097574011 * m_value - 0.3413193965 * s_value,
        -0.0041960863 * l_value - 0.7034186147 * m_value + 1.7076147010 * s_value,
        max(0.0, min(1.0, alpha)),
    )


def parse_color(value: str) -> Color:
    """OKLCH 또는 hex 색을 선형 sRGB로 변환한다."""

    normalized = value.strip().lower()
    hex_match = _HEX.fullmatch(normalized)
    if hex_match:
        digits = hex_match.group(1)
        if len(digits) in (3, 4):
            digits = "".join(char * 2 for char in digits)
        channels = [int(digits[index : index + 2], 16) / 255 for index in range(0, 6, 2)]
        alpha = int(digits[6:8], 16) / 255 if len(digits) == 8 else 1.0
        return Color(*(_srgb_to_linear(channel) for channel in channels), alpha)
    if normalized.startswith("oklch("):
        return _oklch(normalized)
    raise ContrastError(f"지원하지 않는 색 형식: {value[:40]}")


def resolve_colors(values: Mapping[str, str], targets: Iterable[str] | None = None) -> dict[str, Color]:
    """var 참조를 해석한다. 순환 참조와 잘못된 fallback은 오류로 처리한다."""

    resolved: dict[str, Color] = {}
    visiting: set[str] = set()

    def resolve(name: str) -> Color:
        if name in resolved:
            return resolved[name]
        if name in visiting:
            raise ContrastError(f"색 변수 순환 참조: {name}")
        if name not in values:
            raise ContrastError(f"필수 색 변수가 없습니다: {name}")
        visiting.add(name)
        raw = values[name].strip()
        var_match = _VAR.fullmatch(raw)
        if var_match:
            reference = var_match.group(1)
            if reference in values:
                color = resolve(reference)
            elif var_match.group(2):
                color = parse_color(var_match.group(2).strip())
            else:
                raise ContrastError(f"색 변수 참조를 찾지 못했습니다: {reference}")
        else:
            color = parse_color(raw)
        visiting.remove(name)
        resolved[name] = color
        return color

    names = targets if targets is not None else values.keys()
    for name in names:
        resolve(name)
    return resolved


def contrast_ratio(foreground: Color, background: Color) -> float:
    """알파 색을 배경에 합성한 뒤 WCAG 대비를 반환한다."""

    white = Color(1.0, 1.0, 1.0)

    def composite(source: Color, under: Color) -> Color:
        alpha = max(0.0, min(1.0, source.alpha))
        return Color(
            source.red * alpha + under.red * (1.0 - alpha),
            source.green * alpha + under.green * (1.0 - alpha),
            source.blue * alpha + under.blue * (1.0 - alpha),
        )

    opaque_background = composite(background, white)
    opaque_foreground = composite(foreground, opaque_background)
    first, second = opaque_foreground.luminance(), opaque_background.luminance()
    lighter, darker = max(first, second), min(first, second)
    return (lighter + 0.05) / (darker + 0.05)


def inspect(values: Mapping[str, str]) -> list[dict[str, object]]:
    targets = {f"--kt-{name}" for pair in PAIRS for name in (pair.foreground, pair.background)}
    resolved = resolve_colors(values, targets)
    findings: list[dict[str, object]] = []
    for pair in PAIRS:
        foreground = resolved.get(f"--kt-{pair.foreground}")
        background = resolved.get(f"--kt-{pair.background}")
        if foreground is None or background is None:
            missing = pair.foreground if foreground is None else pair.background
            raise ContrastError(f"필수 색 변수가 없습니다: --kt-{missing}")
        measured = contrast_ratio(foreground, background)
        findings.append(
            {
                "pair": pair.name,
                "foreground": pair.foreground,
                "background": pair.background,
                "measured": measured,
                "required": pair.required,
                "pass": measured >= pair.required,
            }
        )
    return findings


def _load_json(path: Path) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ContrastError(f"JSON 입력을 읽을 수 없습니다: {path.name}") from error


def load_baseline(path: Path) -> list[dict[str, object]]:
    """baseline의 entries 목록을 검증해 반환한다."""

    data = _load_json(path)
    if isinstance(data, dict):
        entries = data.get("entries", data.get("baseline"))
    else:
        entries = data
    if not isinstance(entries, list):
        raise ContrastError("대비 baseline은 entries 배열이어야 합니다")
    result: list[dict[str, object]] = []
    for entry in entries:
        if not isinstance(entry, dict) or not all(key in entry for key in ("pair", "surface", "measured", "required", "until")):
            raise ContrastError("대비 baseline 항목 필드가 부족합니다")
        if not isinstance(entry["pair"], str) or not isinstance(entry["surface"], str):
            raise ContrastError("대비 baseline pair/surface 형식이 잘못되었습니다")
        try:
            measured = float(entry["measured"])
            required = float(entry["required"])
            _datetime.date.fromisoformat(str(entry["until"]))
        except (TypeError, ValueError) as error:
            raise ContrastError("대비 baseline 수치 또는 until 형식이 잘못되었습니다") from error
        result.append({"pair": entry["pair"], "surface": entry["surface"], "measured": measured, "required": required, "until": str(entry["until"])})
    return result


def apply_baseline(findings: Sequence[Mapping[str, object]], entries: Sequence[Mapping[str, object]]) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    today = _datetime.date.today()
    misses = [finding for finding in findings if not bool(finding["pass"])]
    expired: list[dict[str, object]] = []
    for entry in entries:
        try:
            until = _datetime.date.fromisoformat(str(entry["until"]))
        except ValueError:
            continue
        if until < today:
            expired.append(dict(entry))
    for finding in misses:
        pair = str(finding["pair"])
        foreground = str(finding["foreground"])
        background = str(finding["background"])
        background_aliases = {background, background.removeprefix("surface-")}
        baseline = next(
            (
                entry
                for entry in entries
                if (str(entry["pair"]), str(entry["surface"])) in {
                    (candidate_pair, candidate_surface)
                    for candidate_pair in (pair, foreground)
                    for candidate_surface in background_aliases
                }
            ),
            None,
        )
        finding["baseline"] = bool(baseline)
        finding["exempt"] = bool(baseline and _datetime.date.fromisoformat(str(baseline["until"])) >= today)
    return [dict(finding) for finding in findings], expired


def _format_ratio(value: object) -> str:
    return f"{float(value):.2f}"


def render_markdown(mode: str, findings: Sequence[Mapping[str, object]], expired: Sequence[Mapping[str, object]], fail_new: bool) -> str:
    misses = [finding for finding in findings if not bool(finding["pass"])]
    new_misses = [finding for finding in misses if fail_new and not bool(finding.get("exempt", False))]
    status = "EXEMPT_EXPIRED" if expired else ("FAIL" if new_misses else "PASS")
    lines = [f"### kt_contrast ({mode})", "", f"- 상태: **{status}**", f"- 쌍: {len(findings)}개 · 미달: {len(misses)}개"]
    if fail_new:
        lines.append(f"- 신규 미달: {len(new_misses)}개 · 만료 baseline: {len(expired)}개")
    lines.extend(["", "| 쌍 | 측정 | 기준 | 판정 |", "|---|---:|---:|---|"])
    for finding in findings:
        state = "PASS" if finding["pass"] else ("EXEMPT" if finding.get("exempt") else "FAIL")
        lines.append(f"| `{finding['pair']}` | {_format_ratio(finding['measured'])} | {_format_ratio(finding['required'])} | {state} |")
    if expired:
        lines.extend(["", "#### 만료 baseline", ""])
        lines.extend(f"- `{entry['pair']}/{entry['surface']}` until `{entry['until']}`" for entry in expired)
    return "\n".join(lines) + "\n"


def write_step_summary(content: str, explicit: str | None) -> None:
    target = explicit or os.environ.get("GITHUB_STEP_SUMMARY")
    if not target:
        return
    try:
        with Path(target).open("a", encoding="utf-8", newline="\n") as handle:
            handle.write(content)
    except OSError as error:
        raise ContrastError("step summary를 쓸 수 없습니다") from error


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="--kt-* 토큰의 WCAG 대비를 검사합니다.")
    parser.add_argument("paths", nargs="*", type=Path, help="canonical tokens.css 뒤에 적용할 오버라이드 CSS")
    parser.add_argument("--dark", action="store_true", help="dark 모드 선언을 검사합니다")
    parser.add_argument("--baseline", type=Path, help="미달 예외 JSON")
    parser.add_argument("--fail-new", action="store_true", help="baseline에 없는 미달 또는 만료를 실패 처리합니다")
    parser.add_argument("--json", action="store_true", dest="as_json", help="JSON으로 출력합니다")
    parser.add_argument("--step-summary", type=str, help="GitHub step summary 파일 경로")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    paths = args.paths or [DEFAULT_TOKENS]
    try:
        values = parse_css(paths, args.dark)
        findings = inspect(values)
        baseline = load_baseline(args.baseline) if args.baseline else []
        findings, expired = apply_baseline(findings, baseline)
        misses = [finding for finding in findings if not bool(finding["pass"])]
        new_misses = [finding for finding in misses if not bool(finding.get("exempt", False))]
        status = "EXEMPT_EXPIRED" if expired else ("FAIL" if args.fail_new and new_misses else "PASS")
        payload = {"tool": "kt_contrast", "mode": "dark" if args.dark else "light", "status": status, "findings": findings, "expired": expired}
        markdown = render_markdown(payload["mode"], findings, expired, args.fail_new)
        write_step_summary(markdown, args.step_summary)
        if args.as_json:
            print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
        else:
            print(markdown, end="")
        return 1 if status in {"FAIL", "EXEMPT_EXPIRED"} else 0
    except ContrastError as error:
        print(f"kt_contrast 오류: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
