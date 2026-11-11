// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { copyFileSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";

const root = new URL("../../../", import.meta.url);
const fixture = new URL("./next-app/", import.meta.url);
const read = url => JSON.parse(readFileSync(url, "utf8"));
const registry = read(new URL("versions.json", root));
const css = read(new URL("frontend-artifacts.json", root)).packages.lightningcss;
const version = registry.axes.lightningcss.exact;
const filename = "lightningcss-" + version + ".tgz";
const source = new URL("vendor/" + filename, root);
const integrity = "sha512-" + createHash("sha512").update(readFileSync(source)).digest("base64");
assert.equal(css.version, version, "Lightning CSS 정확 버전 정본 불일치");
assert.equal(css.filename, filename, "Lightning CSS 파일명 정본 불일치");
assert.equal(css.integrity, integrity, "Lightning CSS 원본 vendor bytes 불일치");

// root의 단일 원본을 두 실제 Next 설치 경로에 복사한다. 원장/lock 해시는 덮어쓰지 않는다.
for (const target of [root, fixture, new URL("../examples/next-app/", import.meta.url)]) {
  const manifest = read(new URL("package.json", target));
  const lock = read(new URL("package-lock.json", target));
  const spec = "file:vendor/" + filename;
  assert.equal(manifest.devDependencies.lightningcss, spec, "Lightning CSS 개발 의존성 경로 불일치");
  assert.equal(manifest.overrides.lightningcss, "$lightningcss", "Lightning CSS 전이 override 누락");
  assert.equal(lock.packages[""].devDependencies.lightningcss, spec, "Lightning CSS lock 직접 선언 불일치");
  let copies = 0;
  for (const [location, entry] of Object.entries(lock.packages)) {
    if (!location.endsWith("node_modules/lightningcss")) continue;
    copies++;
    assert.equal(entry.version, version, "Lightning CSS lock 전이 버전 불일치");
    assert.equal(entry.integrity, integrity, "Lightning CSS lock 전이 bytes 불일치");
    assert.equal(entry.resolved, spec, "Lightning CSS lock vendor 참조 불일치");
  }
  assert.ok(copies > 0, "Lightning CSS lock 설치본 누락");
  if (target !== root) {
    mkdirSync(new URL("vendor/", target), { recursive: true });
    copyFileSync(source, new URL("vendor/" + filename, target));
  }
}

// 예시 단독 설치 전에는 CSS 복사만 실행한다.
if (!process.argv.includes("--css-only")) {
  const manifest = read(new URL("package.json", fixture));
  const lockPath = new URL("package-lock.json", fixture);
  const lock = read(lockPath);
  // 매 실행에서 생성한 두 로컬 common 산출물만 갱신한다. 고정 CSS 산출물은 위에서 검증한다.
  for (const name of ["@kor-travel/tokens", "@kor-travel/ui"]) {
    const source = manifest.dependencies[name];
    assert.ok(source.startsWith("file:../../../../test-results/ui-pack/"));
    const entry = lock.packages["node_modules/" + name];
    assert.equal(lock.packages[""].dependencies[name], source);
    assert.equal(entry.resolved, source);
    const bytes = readFileSync(new URL(source.slice(5), fixture));
    entry.integrity = "sha512-" + createHash("sha512").update(bytes).digest("base64");
    console.log(name + ": " + entry.integrity);
  }
  writeFileSync(lockPath, JSON.stringify(lock, null, 2) + "\n");
}
console.log("root·smoke·example의 Lightning CSS 고정 bytes 확인");
