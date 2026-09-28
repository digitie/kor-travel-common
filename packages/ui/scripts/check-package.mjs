// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
import { readFileSync, readdirSync } from "node:fs";
import assert from "node:assert/strict";
const root = new URL("../", import.meta.url);
for (const file of readdirSync(new URL("src/", root))) {
  if (!/\.tsx?$/.test(file)) continue;
  const source = readFileSync(new URL(`src/${file}`, root), "utf8");
  const emitted = readFileSync(new URL(`dist/${file.replace(/\.tsx?$/, ".js")}`, root), "utf8");
  const clean = (text) => text.replace(/^(?:\s|\/\/[^\n]*(?:\n|$)|\/\*[\s\S]*?\*\/)+/, "");
  for (const directive of ["use client", "use no memo"]) {
    if (clean(source).startsWith(`"${directive}"`)) assert.ok(clean(emitted).startsWith(`"${directive}"`), `${file}: 지시문 유실`);
  }
}
for (const file of ["LICENSE", "NOTICE", "THIRD_PARTY_NOTICES.md"]) {
  assert.ok(readFileSync(new URL(file, root), "utf8").length > 0, `${file}: 고지 누락`);
}
console.log("UI 지시문·고지 확인 통과");
