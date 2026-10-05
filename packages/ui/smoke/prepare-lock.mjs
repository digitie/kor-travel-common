// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFileSync, writeFileSync } from "node:fs";

const fixture = new URL("./next-app/", import.meta.url);
const manifest = JSON.parse(readFileSync(new URL("package.json", fixture), "utf8"));
const lockPath = new URL("package-lock.json", fixture);
const lock = JSON.parse(readFileSync(lockPath, "utf8"));

// 매 실행에서 생성한 두 로컬 산출물만 갱신한다. registry 고정값은 유지한다.
for (const [name, filename] of [
  ["@kor-travel/tokens", "kor-travel-tokens-0.1.0.tgz"],
  ["@kor-travel/ui", "kor-travel-ui-0.1.0-dev.6.tgz"],
]) {
  const source = `file:../../../../test-results/ui-pack/${filename}`;
  const entry = lock.packages[`node_modules/${name}`];
  assert.equal(manifest.dependencies[name], source);
  assert.equal(lock.packages[""].dependencies[name], source);
  assert.equal(entry.resolved, source);
  const bytes = readFileSync(new URL(source.slice(5), fixture));
  entry.integrity = `sha512-${createHash("sha512").update(bytes).digest("base64")}`;
  console.log(`${name}: ${entry.integrity}`);
}
writeFileSync(lockPath, `${JSON.stringify(lock, null, 2)}\n`);
