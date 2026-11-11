// SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
// SPDX-License-Identifier: GPL-3.0-or-later
import { readFileSync, writeFileSync } from "node:fs";
const registry = JSON.parse(readFileSync(new URL("../versions.json", import.meta.url), "utf8"));
const { packages, ...metadata } = registry.frontendPolicy;
const versions = {};
for (const name of packages) {
  const axes = Object.entries(registry.axes).filter(([key, axis]) =>
    axis.ecosystem === "npm" && (axis.packages ?? [key]).includes(name));
  const values = new Set(axes.map(([, axis]) => (axis.exact ?? axis.recommended)));
  if (values.size !== 1 || ![...values][0]) throw new Error(name + ": 정확 버전 정본을 찾을 수 없음");
  versions[name] = [...values][0];
}
const generated = { generatedFrom: "versions.json", ...metadata, versions };
const target = new URL("../frontend-dependencies.json", import.meta.url);
const content = JSON.stringify(generated, null, 2) + "\n";
if (process.argv.includes("--check")) {
  if (readFileSync(target, "utf8") !== content) throw new Error("frontend-dependencies.json 생성물이 정본과 다름");
} else writeFileSync(target, content);
