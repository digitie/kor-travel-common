// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
// Modified: 2026-09-07 — 정본 CSS·생성물·공개 subpath 회귀 시험 추가

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

test("tokens.css는 map c494e227의 고정 light 값을 유지한다", () => {
  const light = properties(read("tokens.css"), ":root");
  const expected = {
    "--kt-surface-page": "oklch(97.8% 0.003 128)",
    "--kt-surface-subtle": "oklch(96.7% 0.006 138)",
    "--kt-surface-muted": "oklch(92.5% 0.01 141)",
    "--kt-surface-card": "oklch(99.2% 0.002 140)",
    "--kt-text-primary": "oklch(30% 0.006 157)",
    "--kt-text-secondary": "oklch(48% 0.012 159)",
    "--kt-text-tertiary": "oklch(54% 0.012 154)",
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
  };
  for (const [name, value] of Object.entries(expected)) assert.equal(light[name], value, name);
  assert.equal(light["--kt-font-sans"], '"Pretendard Variable", Pretendard, "Noto Sans KR", "Apple SD Gothic Neo", system-ui, sans-serif');
  assert.equal(light["--kt-font-mono"], 'ui-monospace, "SF Mono", Menlo, Consolas, monospace');
});

test("tokens.css는 D-12 역할의 map dark 값을 모두 정의한다", () => {
  const dark = properties(read("tokens.css"), ".dark");
  const expected = {
    "--kt-surface-page": "oklch(19% 0.006 150)",
    "--kt-surface-card": "oklch(23% 0.007 145)",
    "--kt-text-primary": "oklch(93% 0.006 155)",
    "--kt-text-secondary": "oklch(78% 0.01 155)",
    "--kt-text-tertiary": "oklch(68% 0.012 155)",
    "--kt-control-line": "oklch(58% 0.012 145)",
    "--kt-brand": "oklch(76% 0.085 169)",
    "--kt-brand-hover": "oklch(81% 0.085 169)",
    "--kt-brand-tint": "oklch(31% 0.035 169)",
    "--kt-brand-foreground": "oklch(20% 0.02 165)",
    "--kt-overlay": "oklch(10% 0.006 157 / 0.6)",
    "--kt-shadow-elevated": "0 4px 12px oklch(10% 0.006 157 / 0.32)",
    "--kt-shadow-modal": "0 8px 24px oklch(10% 0.006 157 / 0.4)",
  };
  for (const [name, value] of Object.entries(expected)) assert.equal(dark[name], value, name);
  for (const name of Object.keys(properties(read("tokens.css"), ":root"))) {
    assert.ok(dark[name], `dark ${name}`);
  }
});

test("theme.css는 kt 네임스페이스와 비inline 타입 스케일을 분리한다", () => {
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
});

test("shadcn·base·dark 파일은 공개 계약을 유지한다", () => {
  const shadcn = read("shadcn.css");
  assert.match(shadcn, /--input:\s*var\(--kt-control-line\)/);
  assert.match(shadcn, /--accent:\s*var\(--kt-brand-tint\)/);
  assert.match(shadcn, /--border:\s*var\(--kt-border\)/);
  assert.match(shadcn, /--radius:\s*var\(--kt-radius-control\)/);
  assert.match(read("base.css"), /:focus-visible[\s\S]*outline: 2px solid var\(--kt-focus\)/);
  assert.match(read("base.css"), /button:not\(:disabled\)[\s\S]*cursor: pointer/);
  assert.match(read("base.scoped.css"), /data-kt-surface/);
  assert.match(read("dark-class.css"), /@custom-variant dark/);
  assert.match(read("dark-media.css"), /prefers-color-scheme: dark/);
});

test("생성기는 tokens.css에서 결정적으로 재생성된다", () => {
  execFileSync(process.execPath, [join(packageRoot, "scripts/build.mjs")], { stdio: "pipe" });
  execFileSync(process.execPath, [join(packageRoot, "scripts/build.mjs"), "--check"], { stdio: "pipe" });
  const document = JSON.parse(read("dist/tokens.json"));
  assert.equal(document.surface.page.$value, "oklch(97.8% 0.003 128)");
  assert.equal(document.surface.page.$extensions["kor-travel-common"].dark, "oklch(19% 0.006 150)");
  assert.equal(document.profiles.consumer.ownedBy, "consumer");
  assert.match(read("dist/tailwind-preset.cjs"), /kt-surface-page/);
  assert.match(read("dist/index.d.ts"), /export declare const tokens/);
});

test("패키지에는 금지된 앱 접두가 없다", () => {
  for (const name of ["tokens.css", "theme.css", "shadcn.css", "base.css", "base.scoped.css", "dark-class.css", "dark-media.css"]) {
    const css = read(name);
    assert.doesNotMatch(css, /--(?:ktc|ui|pv|color-admin)-/);
  }
});
