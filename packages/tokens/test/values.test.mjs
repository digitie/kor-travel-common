// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
// Modified: 2026-09-07 — 정본·DTCG·실제 CSS 전달 계약 회귀 시험

import { execFileSync } from "node:child_process";
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import test from "node:test";
import assert from "node:assert/strict";

const packageRoot = join(dirname(fileURLToPath(import.meta.url)), "..");
const read = (name) => readFileSync(join(packageRoot, name), "utf8");
const block = (css, selector) => {
  const start = css.indexOf(`${selector} {`);
  assert.notEqual(start, -1, `${selector} 블록이 필요합니다`);
  const open = css.indexOf("{", start);
  let depth = 0;
  for (let index = open; index < css.length; index += 1) {
    if (css[index] === "{") depth += 1;
    if (css[index] === "}") {
      depth -= 1;
      if (depth === 0) return css.slice(open + 1, index);
    }
  }
  assert.fail(`${selector} 블록이 닫히지 않았습니다`);
};
const properties = (css, selector) => Object.fromEntries(
  [...block(css, selector).matchAll(/(--kt-[a-z0-9-]+)\s*:\s*([^;]+);/g)]
    .map((match) => [match[1], match[2].trim()]),
);

const lightExpected = {
  "--kt-surface-page": "oklch(97.8% 0.003 128)",
  "--kt-surface-subtle": "oklch(96.7% 0.006 138)",
  "--kt-surface-muted": "oklch(92.5% 0.01 141)",
  "--kt-surface-card": "oklch(99.2% 0.002 140)",
  "--kt-text-primary": "oklch(30% 0.006 157)",
  "--kt-text-secondary": "oklch(48% 0.012 159)",
  "--kt-text-tertiary": "oklch(54% 0.012 154)",
  "--kt-text-disabled": "oklch(79% 0.012 154)",
  "--kt-text-strong": "var(--kt-text-primary)",
  "--kt-icon": "var(--kt-text-tertiary)",
  "--kt-border": "var(--kt-surface-muted)",
  "--kt-control-line": "oklch(61% 0.012 145)",
  "--kt-brand": "oklch(51.4% 0.081 169)",
  "--kt-brand-hover": "oklch(46% 0.085 169)",
  "--kt-brand-tint": "oklch(95.2% 0.013 172)",
  "--kt-brand-foreground": "oklch(99% 0.002 140)",
  "--kt-focus": "oklch(45% 0.09 169)",
  "--kt-success": "oklch(46.9% 0.087 149)",
  "--kt-success-tint": "oklch(95% 0.03 150)",
  "--kt-warning": "oklch(50.9% 0.103 71)",
  "--kt-warning-tint": "oklch(96% 0.035 80)",
  "--kt-info": "oklch(50% 0.16 258)",
  "--kt-info-tint": "oklch(95.5% 0.025 255)",
  "--kt-destructive": "oklch(51.4% 0.167 27)",
  "--kt-destructive-tint": "oklch(96% 0.03 25)",
  "--kt-overlay": "oklch(30% 0.006 157 / 0.45)",
  "--kt-radius-control": "0.375rem",
  "--kt-radius-panel": "0.5rem",
  "--kt-control-h": "2.25rem",
  "--kt-control-h-sm": "1.875rem",
  "--kt-rail": "22rem",
  "--kt-duration-fast": "100ms",
  "--kt-duration-base": "150ms",
  "--kt-ease-out": "cubic-bezier(0.16, 1, 0.3, 1)",
  "--kt-ease-in": "cubic-bezier(0.7, 0, 0.84, 0)",
  "--kt-shadow-elevated": "0 4px 12px oklch(30% 0.006 157 / 0.1)",
  "--kt-shadow-modal": "0 8px 24px oklch(30% 0.006 157 / 0.14)",
  "--kt-z-nav": "30",
  "--kt-z-panel": "40",
  "--kt-z-overlay": "50",
  "--kt-z-modal": "60",
  "--kt-z-toast": "70",
  "--kt-font-sans": '"Pretendard Variable", Pretendard, "Noto Sans KR", "Apple SD Gothic Neo", system-ui, sans-serif',
  "--kt-font-mono": 'ui-monospace, "SF Mono", Menlo, Consolas, monospace',
};

const darkExpected = {
  "--kt-surface-page": "oklch(19% 0.006 150)",
  "--kt-surface-subtle": "oklch(24% 0.008 145)",
  "--kt-surface-muted": "oklch(31% 0.012 145)",
  "--kt-surface-card": "oklch(23% 0.007 145)",
  "--kt-text-primary": "oklch(93% 0.006 155)",
  "--kt-text-secondary": "oklch(78% 0.01 155)",
  "--kt-text-tertiary": "oklch(68% 0.012 155)",
  "--kt-text-disabled": "oklch(52% 0.012 155)",
  "--kt-text-strong": "var(--kt-text-primary)",
  "--kt-icon": "oklch(70% 0.01 155)",
  "--kt-border": "var(--kt-surface-muted)",
  "--kt-control-line": "oklch(58% 0.012 145)",
  "--kt-brand": "oklch(76% 0.085 169)",
  "--kt-brand-hover": "oklch(81% 0.085 169)",
  "--kt-brand-tint": "oklch(31% 0.035 169)",
  "--kt-brand-foreground": "oklch(20% 0.02 165)",
  "--kt-focus": "oklch(80% 0.09 169)",
  "--kt-success": "oklch(75% 0.09 149)",
  "--kt-success-tint": "oklch(28% 0.04 150)",
  "--kt-warning": "oklch(77% 0.12 75)",
  "--kt-warning-tint": "oklch(30% 0.045 80)",
  "--kt-info": "oklch(75% 0.11 258)",
  "--kt-info-tint": "oklch(30% 0.05 258)",
  "--kt-destructive": "oklch(72% 0.14 27)",
  "--kt-destructive-tint": "oklch(30% 0.06 27)",
  "--kt-overlay": "oklch(10% 0.006 157 / 0.6)",
  "--kt-shadow-elevated": "0 4px 12px oklch(10% 0.006 157 / 0.32)",
  "--kt-shadow-modal": "0 8px 24px oklch(10% 0.006 157 / 0.4)",
  "--kt-radius-control": "0.375rem",
  "--kt-radius-panel": "0.5rem",
  "--kt-control-h": "2.25rem",
  "--kt-control-h-sm": "1.875rem",
  "--kt-rail": "22rem",
  "--kt-duration-fast": "100ms",
  "--kt-duration-base": "150ms",
  "--kt-ease-out": "cubic-bezier(0.16, 1, 0.3, 1)",
  "--kt-ease-in": "cubic-bezier(0.7, 0, 0.84, 0)",
  "--kt-z-nav": "30",
  "--kt-z-panel": "40",
  "--kt-z-overlay": "50",
  "--kt-z-modal": "60",
  "--kt-z-toast": "70",
  "--kt-font-sans": '"Pretendard Variable", Pretendard, "Noto Sans KR", "Apple SD Gothic Neo", system-ui, sans-serif',
  "--kt-font-mono": 'ui-monospace, "SF Mono", Menlo, Consolas, monospace',
};

test("tokens.css는 map c494e227의 고정 light 값을 유지한다", () => {
  assert.deepEqual(properties(read("tokens.css"), ":root"), lightExpected);
});

test("tokens.css는 map c494e227의 고정 dark 값을 모두 유지한다", () => {
  assert.deepEqual(properties(read("tokens.css"), ".dark"), darkExpected);
});

test("theme.css는 kt 네임스페이스와 Tailwind v4 유틸리티를 발행한다", () => {
  const theme = read("theme.css");
  assert.match(theme, /@theme inline\s*\{/);
  assert.match(theme, /@theme\s*\{/);
  assert.match(theme, /--color-kt-surface-page:\s*var\(--kt-surface-page\)/);
  assert.match(theme, /--spacing-kt-control:\s*var\(--kt-control-h\)/);
  assert.match(theme, /--radius-kt-control:\s*var\(--kt-radius-control\)/);
  assert.match(theme, /--font-kt-sans:\s*var\(--kt-font-sans\)/);
  assert.match(theme, /--text-kt-2xl:\s*1\.875rem/);
  assert.match(theme, /@utility duration-kt-fast/);
  assert.match(theme, /@utility duration-kt-base/);
  for (const name of ["nav", "panel", "overlay", "modal", "toast"]) {
    assert.match(theme, new RegExp(`@utility z-kt-${name}`));
  }
});

test("shadcn·base·dark 파일은 공개 계약을 유지한다", () => {
  const shadcn = read("shadcn.css");
  assert.match(shadcn, /--input:\s*var\(--kt-control-line\)/);
  assert.match(shadcn, /--accent:\s*var\(--kt-brand-tint\)/);
  assert.match(shadcn, /--border:\s*var\(--kt-border\)/);
  assert.match(shadcn, /--radius:\s*var\(--kt-radius-control\)/);
  assert.match(shadcn, /:where\(\[data-kt-surface\]\)/);
  assert.match(shadcn, /:where\(\[data-kt-surface\]\)[\s\S]*--radius:\s*var\(--kt-radius-control\)/);
  assert.match(read("base.css"), /:focus-visible[\s\S]*outline: 2px solid var\(--kt-focus\)/);
  assert.match(read("base.css"), /button:not\(:disabled\)[\s\S]*cursor: pointer/);
  assert.match(read("base.css"), /\.border-kt-hairline\s*\{/);
  assert.match(read("base.scoped.css"), /border-kt-hairline-scoped/);
  assert.doesNotMatch(read("base.scoped.css"), /color-scheme:\s*light/);
  assert.match(read("dark-class.css"), /@custom-variant dark/);
  assert.match(read("dark-media.css"), /prefers-color-scheme: dark/);
  assert.doesNotMatch(read("dark-media.css"), /@custom-variant dark/);
});

function assertDtcgToken(node, path = []) {
  if (node && typeof node === "object" && Object.prototype.hasOwnProperty.call(node, "$value")) {
    assert.ok(typeof node.$type === "string", `${path.join(".")} type`);
    const value = node.$value;
    if (typeof value === "string" && /^\{[^}]+\}$/.test(value)) return;
    switch (node.$type) {
      case "color":
        assert.equal(value.colorSpace, "oklch", `${path.join(".")} color space`);
        assert.equal(value.components.length, 3, `${path.join(".")} color components`);
        break;
      case "dimension":
      case "duration":
        assert.equal(typeof value.value, "number", `${path.join(".")} scalar`);
        assert.equal(typeof value.unit, "string", `${path.join(".")} unit`);
        break;
      case "cubicBezier":
        assert.equal(value.length, 4, `${path.join(".")} bezier`);
        assert.ok(value.every((item) => typeof item === "number"), `${path.join(".")} bezier numbers`);
        break;
      case "number":
        assert.equal(typeof value, "number", `${path.join(".")} number`);
        break;
      case "fontFamily":
        assert.ok(Array.isArray(value) && value.every((item) => typeof item === "string"), `${path.join(".")} fonts`);
        break;
      case "shadow":
        assert.ok(value.color && value.offsetX && value.offsetY && value.blur && value.spread, `${path.join(".")} shadow`);
        break;
      default:
        assert.fail(`${path.join(".")} unsupported DTCG type ${node.$type}`);
    }
    return;
  }
  if (!node || typeof node !== "object") return;
  for (const [name, child] of Object.entries(node)) {
    if (name.startsWith("$")) continue;
    assertDtcgToken(child, [...path, name]);
  }
}

test("생성 tokens.json은 DTCG 타입과 root token 계층을 지킨다", () => {
  execFileSync(process.execPath, [join(packageRoot, "scripts/build.mjs")], { stdio: "pipe" });
  execFileSync(process.execPath, [join(packageRoot, "scripts/build.mjs"), "--check"], { stdio: "pipe" });
  const document = JSON.parse(read("dist/tokens.json"));
  assert.equal(document.$schema, "https://www.designtokens.org/schemas/2025.10/format.json");
  assertDtcgToken(document);
  assert.deepEqual(document.surface.page.$value, { colorSpace: "oklch", components: [0.978, 0.003, 128] });
  assert.deepEqual(document.surface.page.$extensions["kor-travel-common"].dark, { colorSpace: "oklch", components: [0.19, 0.006, 150] });
  assert.equal(document.$extensions["kor-travel-common"].profiles.consumer.ownedBy, "consumer");
  assert.deepEqual(document.radius.control.$value, { value: 0.375, unit: "rem" });
  assert.deepEqual(document.duration.fast.$value, { value: 100, unit: "ms" });
  assert.deepEqual(document.ease.out.$value, [0.16, 1, 0.3, 1]);
  assert.equal(document.z.nav.$value, 30);
  assert.deepEqual(document.font.mono.$value, ["ui-monospace", "SF Mono", "Menlo", "Consolas", "monospace"]);
  assert.equal(document.text.strong.$value, "{text.primary}");
  assert.equal(document.brand.$root.$type, "color");
  assert.equal(document.brand.hover.$type, "color");
  assert.match(read("dist/tailwind-preset.cjs"), /kt-surface-page/);
  assert.match(read("dist/tailwind-preset.cjs"), /transitionTimingFunction/);
  assert.match(read("dist/index.d.ts"), /export declare const tokens/);
});

test("dark-media는 정본의 dark 값을 전수 전달한다", () => {
  const media = read("dark-media.css");
  for (const [name, value] of Object.entries(darkExpected)) {
    assert.ok(media.includes(`${name}: ${value};`), `${name} media 값`);
  }
});

test("패키지에는 금지된 앱 접두가 없다", () => {
  for (const name of ["tokens.css", "theme.css", "shadcn.css", "base.css", "base.scoped.css", "dark-class.css", "dark-media.css"]) {
    const css = read(name);
    assert.doesNotMatch(css, /--(?:ktc|ui|pv|color-admin)-/);
  }
});
