// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
// Modified: 2026-09-07 — tokens.css를 유일한 정본으로 읽는 무의존 생성기 구현

import { readFile, writeFile, mkdir } from "node:fs/promises";
import { existsSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const packageRoot = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const sourcePath = join(packageRoot, "tokens.css");
const distPath = join(packageRoot, "dist");
const checkOnly = process.argv.includes("--check");

const requiredTokens = [
  "surface-page", "surface-subtle", "surface-muted", "surface-card",
  "text-primary", "text-secondary", "text-tertiary", "text-disabled", "text-strong",
  "icon", "border", "control-line", "brand", "brand-hover", "brand-tint",
  "brand-foreground", "focus", "success", "success-tint", "warning", "warning-tint",
  "info", "info-tint", "destructive", "destructive-tint", "overlay",
  "radius-control", "radius-panel", "control-h", "control-h-sm", "rail",
  "duration-fast", "duration-base", "ease-out", "ease-in", "shadow-elevated",
  "shadow-modal", "z-nav", "z-panel", "z-overlay", "z-modal", "z-toast",
  "font-sans", "font-mono",
];

const typeFor = (name) => {
  if (/^(surface|text|icon|border|control-line|brand|focus|success|warning|info|destructive|overlay)/.test(name)) {
    return "color";
  }
  if (/^radius|^control-h|^rail/.test(name)) return "dimension";
  if (/^duration/.test(name)) return "duration";
  if (/^ease/.test(name)) return "cubicBezier";
  if (/^shadow/.test(name)) return "shadow";
  if (/^z-/.test(name)) return "number";
  if (/^font/.test(name)) return "fontFamily";
  return "unknown";
};

function matchingBlock(css, selector) {
  const start = css.indexOf(`${selector} {`);
  if (start < 0) throw new Error(`tokens.css에 ${selector} 블록이 없습니다`);
  const open = css.indexOf("{", start);
  let depth = 0;
  for (let index = open; index < css.length; index += 1) {
    if (css[index] === "{") depth += 1;
    if (css[index] === "}") {
      depth -= 1;
      if (depth === 0) return css.slice(open + 1, index);
    }
  }
  throw new Error(`tokens.css의 ${selector} 블록이 닫히지 않았습니다`);
}

function properties(block) {
  const result = new Map();
  const pattern = /(--kt-[a-z0-9-]+)\s*:\s*([^;]+);/g;
  for (const match of block.matchAll(pattern)) result.set(match[1].slice(5), match[2].trim());
  return result;
}

function nestedTokenPath(name) {
  const dash = name.indexOf("-");
  return dash < 0 ? [name, "$root"] : [name.slice(0, dash), name.slice(dash + 1)];
}

function tokenReference(name) {
  return `{${nestedTokenPath(name).join(".")}}`;
}

function normaliseNumber(value) {
  return Number(Number(value).toFixed(6));
}

function dimensionValue(value) {
  const match = /^(?<number>[+-]?(?:\d+\.?\d*|\.\d+))(?<unit>px|rem)$/.exec(value);
  if (!match) {
    if (value === "0") return { value: 0, unit: "px" };
    throw new Error(`DTCG dimension으로 변환할 수 없는 값: ${value}`);
  }
  return { value: normaliseNumber(match.groups.number), unit: match.groups.unit };
}

function durationValue(value) {
  const match = /^(?<number>[+-]?(?:\d+\.?\d*|\.\d+))(?<unit>ms|s)$/.exec(value);
  if (!match) throw new Error(`DTCG duration으로 변환할 수 없는 값: ${value}`);
  return { value: normaliseNumber(match.groups.number), unit: match.groups.unit };
}

function cubicBezierValue(value) {
  const match = /^cubic-bezier\(\s*([^,]+),\s*([^,]+),\s*([^,]+),\s*([^\)]+)\s*\)$/.exec(value);
  if (!match) throw new Error(`DTCG cubicBezier로 변환할 수 없는 값: ${value}`);
  return match.slice(1).map(normaliseNumber);
}

function colorValue(value) {
  const alias = /^var\(--kt-([a-z0-9-]+)\)$/.exec(value);
  if (alias) return tokenReference(alias[1]);
  const match = /^oklch\(\s*([+-]?(?:\d+\.?\d*|\.\d+))%\s+([+-]?(?:\d+\.?\d*|\.\d+))\s+([+-]?(?:\d+\.?\d*|\.\d+))(?:\s*\/\s*([+-]?(?:\d+\.?\d*|\.\d+)))?\s*\)$/.exec(value);
  if (!match) throw new Error(`DTCG color로 변환할 수 없는 값: ${value}`);
  const result = {
    colorSpace: "oklch",
    components: [normaliseNumber(Number(match[1]) / 100), normaliseNumber(match[2]), normaliseNumber(match[3])],
  };
  if (match[4] !== undefined) result.alpha = normaliseNumber(match[4]);
  return result;
}

function fontFamilyValue(value) {
  const result = [];
  const pattern = /"([^"]*)"|'([^']*)'|([^,]+)/g;
  for (const match of value.matchAll(pattern)) {
    const font = (match[1] ?? match[2] ?? match[3]).trim().replace(/^(['"])(.*)\1$/, "$2");
    if (font) result.push(font);
  }
  if (!result.length) throw new Error(`DTCG fontFamily로 변환할 수 없는 값: ${value}`);
  return result;
}

function shadowValue(value) {
  const match = /^(?<x>[+-]?(?:\d+\.?\d*|\.\d+)(?:px|rem)?)\s+(?<y>[+-]?(?:\d+\.?\d*|\.\d+)(?:px|rem)?)\s+(?<blur>[+-]?(?:\d+\.?\d*|\.\d+)(?:px|rem)?)\s+(?<color>oklch\([^)]*\))$/.exec(value);
  if (!match) throw new Error(`DTCG shadow로 변환할 수 없는 값: ${value}`);
  const length = (raw) => dimensionValue(raw === "0" ? "0" : raw);
  return {
    color: colorValue(match.groups.color),
    offsetX: length(match.groups.x),
    offsetY: length(match.groups.y),
    blur: length(match.groups.blur),
    spread: { value: 0, unit: "px" },
  };
}

function dtcgValue(name, value, aliasValues = null) {
  const alias = /^var\(--kt-([a-z0-9-]+)\)$/.exec(value);
  if (alias) {
    return aliasValues ? dtcgValue(alias[1], aliasValues.get(alias[1]), aliasValues) : tokenReference(alias[1]);
  }
  switch (typeFor(name)) {
    case "color": return colorValue(value);
    case "dimension": return dimensionValue(value);
    case "duration": return durationValue(value);
    case "cubicBezier": return cubicBezierValue(value);
    case "shadow": return shadowValue(value);
    case "number": return normaliseNumber(value);
    case "fontFamily": return fontFamilyValue(value);
    default: throw new Error(`지원하지 않는 DTCG 토큰 타입: ${name}`);
  }
}

function tokenDocument(light, dark) {
  const document = {
    $schema: "https://www.designtokens.org/schemas/2025.10/format.json",
    $description: "kor-travel-common의 --kt-* 디자인 토큰. 값의 정본은 tokens.css이다.",
    $extensions: {
      "kor-travel-common": {
        profiles: {
          admin: {
            description: "공용 admin 밀도 프로필",
            radius: { control: "{radius.control}", panel: "{radius.panel}" },
            controlHeight: { default: "{control.h}", small: "{control.h-sm}" },
            body: "sm",
            typeScale: ["2xs", "xs", "sm", "md", "lg", "xl", "2xl"],
          },
          consumer: {
            description: "의미 이름만 common이 제공하며 값과 밀도는 소비자가 소유한다.",
            ownedBy: "consumer",
            semanticGroups: ["surface", "text", "brand", "status", "font"],
          },
        },
      },
    },
  };
  for (const [name, value] of light) {
    const mode = { $type: typeFor(name), $value: dtcgValue(name, value) };
    const darkValue = dark.get(name);
    if (darkValue !== undefined) mode.$extensions = { "kor-travel-common": { dark: dtcgValue(name, darkValue, dark) } };
    const path = nestedTokenPath(name);
    if (path.length === 1) {
      document[path[0]] = mode;
    } else {
      const [category, key] = path;
      const bucket = document[category] ??= {};
      bucket[key] = mode;
    }
  }
  return document;
}

function flatValues(light) {
  return Object.fromEntries([...light].map(([name, value]) => [`--kt-${name}`, value]));
}

function jsModule(document, light) {
  return `// 이 파일은 tokens.css에서 생성된다. 직접 수정하지 않는다.\nexport const tokens = ${JSON.stringify(document, null, 2)};\nexport const tokenValues = ${JSON.stringify(flatValues(light), null, 2)};\n`;
}

function tsModule(document, light) {
  return `// 이 파일은 tokens.css에서 생성된다. 직접 수정하지 않는다.\nexport const tokens = ${JSON.stringify(document, null, 2)} as const;\nexport const tokenValues = ${JSON.stringify(flatValues(light), null, 2)} as const;\nexport type TokenName = keyof typeof tokenValues;\n`;
}

function tailwindPreset(light) {
  const values = Object.fromEntries([...light].map(([name]) => [name, `var(--kt-${name})`]));
  const fontSize = {};
  const lineHeights = { "2xs": "1.5", xs: "1.5", sm: "1.5", md: "1.4", lg: "1.3", xl: "1.25", "2xl": "1.2" };
  for (const [key, value] of Object.entries({
    "2xs": "0.75rem", xs: "0.84375rem", sm: "0.9375rem", md: "1.0625rem",
    lg: "1.25rem", xl: "1.5rem", "2xl": "1.875rem",
  })) fontSize[`kt-${key}`] = [value, { lineHeight: lineHeights[key] }];
  return {
    theme: {
      extend: {
        colors: Object.fromEntries(Object.keys(values).filter((key) => typeFor(key) === "color").map((key) => [`kt-${key}`, values[key]])),
        spacing: {
          "kt-control": "var(--kt-control-h)",
          "kt-control-sm": "var(--kt-control-h-sm)",
          "kt-rail": "var(--kt-rail)",
        },
        borderRadius: { "kt-control": "var(--kt-radius-control)", "kt-panel": "var(--kt-radius-panel)" },
        fontSize,
        fontFamily: { "kt-sans": "var(--kt-font-sans)", "kt-mono": "var(--kt-font-mono)" },
        boxShadow: { "kt-elevated": "var(--kt-shadow-elevated)", "kt-modal": "var(--kt-shadow-modal)" },
        zIndex: Object.fromEntries(["nav", "panel", "overlay", "modal", "toast"].map((key) => [`kt-${key}`, `var(--kt-z-${key})`])),
        transitionDuration: { "kt-fast": "var(--kt-duration-fast)", "kt-base": "var(--kt-duration-base)" },
        transitionTimingFunction: { "kt-out": "var(--kt-ease-out)", "kt-in": "var(--kt-ease-in)" },
      },
    },
  };
}

function generatedFiles(document, light) {
  const preset = `// 이 파일은 tokens.css에서 생성된다. 직접 수정하지 않는다.\nmodule.exports = ${JSON.stringify(tailwindPreset(light), null, 2)};\n`;
  return {
    "tokens.json": `${JSON.stringify(document, null, 2)}\n`,
    "tokens.js": jsModule(document, light),
    "tokens.ts": tsModule(document, light),
    "tailwind-preset.cjs": preset,
    "index.js": `// 이 파일은 tokens.css에서 생성된다. 직접 수정하지 않는다.\nexport { tokens, tokenValues } from "./tokens.js";\n`,
    "index.d.ts": `export declare const tokens: ${JSON.stringify(document, null, 2)};\nexport declare const tokenValues: Readonly<Record<string, string>>;\nexport type TokenName = keyof typeof tokenValues;\n`,
  };
}

function darkMediaCss(dark) {
  const declarations = [...dark].map(([name, value]) => `    --kt-${name}: ${value};`).join("\n");
  return `/* SPDX-License-Identifier: GPL-3.0-or-later
 * SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
 * Generated: scripts/build.mjs — tokens.css의 .dark 값을 OS media로 전달
 */

/* Tailwind v4의 기본 dark variant가 prefers-color-scheme을 사용하므로 class override를 선언하지 않는다. */
@media (prefers-color-scheme: dark) {
  :root {
    color-scheme: dark;
${declarations}
  }
}
`;
}

async function main() {
  const css = await readFile(sourcePath, "utf8");
  const light = properties(matchingBlock(css, ":root"));
  const dark = properties(matchingBlock(css, ".dark"));
  const darkRequired = requiredTokens.filter((name) => typeFor(name) === "color");
  const missing = requiredTokens.filter((name) => !light.has(name))
    .concat(darkRequired.filter((name) => !dark.has(name)));
  if (missing.length) throw new Error(`light/dark 토큰 누락: ${missing.join(", ")}`);
  const document = tokenDocument(light, dark);
  const files = generatedFiles(document, light);
  const outputs = [
    ...Object.entries(files).map(([name, content]) => ({ path: join(distPath, name), name, content })),
    { path: join(packageRoot, "dark-media.css"), name: "dark-media.css", content: darkMediaCss(dark) },
  ];
  if (!checkOnly) await mkdir(distPath, { recursive: true });
  const mismatches = [];
  for (const { path, name, content } of outputs) {
    if (checkOnly) {
      const actual = existsSync(path) ? await readFile(path, "utf8") : null;
      if (actual !== content) mismatches.push(name);
    } else {
      await writeFile(path, content, "utf8");
    }
  }
  if (mismatches.length) throw new Error(`생성물 drift: ${mismatches.join(", ")}. npm run build를 먼저 실행하십시오.`);
  if (checkOnly) console.log("tokens.css 생성물 검사: clean");
  else console.log(`tokens.css 생성 완료: ${outputs.length}개 파일`);
}

await main();
