// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { copyFileSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";

const root = new URL("../../../", import.meta.url);
const fixture = new URL("./next-app/", import.meta.url);
const read = url => JSON.parse(readFileSync(url, "utf8"));
const registry = read(new URL("versions.json", root));
const artifacts = read(new URL("frontend-artifacts.json", root)).packages;
function fixedEngine(name, version) {
  const label = name === "lightningcss" ? "Lightning CSS" : name;
  assert.ok(typeof version === "string" && version.trim(), label + " 정확 버전 정본 누락");
  const prefix = name.startsWith("@") ? name.slice(1).replace("/", "-") : name;
  const filename = prefix + "-" + version + ".tgz";
  const source = new URL("vendor/" + filename, root);
  const artifact = artifacts[name];
  assert.ok(artifact, label + " 산출물 원장 누락");
  assert.equal(artifact.version, version, label + " 정확 버전 정본 불일치");
  assert.equal(artifact.filename, filename, label + " 파일명 정본 불일치");
  const integrity = "sha512-" + createHash("sha512").update(readFileSync(source)).digest("base64");
  assert.equal(artifact.integrity, integrity, label + " 원본 vendor bytes 불일치");
  return {name, label, version, filename, source, integrity};
}
const engines = [fixedEngine("lightningcss", registry.axes.lightningcss.exact)];
const patched = Object.hasOwn(registry.frontendPolicy ?? {}, "patchedRadixPackages")
  ? registry.frontendPolicy.patchedRadixPackages : [];
assert.ok(Array.isArray(patched) && patched.every(name => typeof name === "string"
  && /^@radix-ui\/react-[a-z0-9]+(?:-[a-z0-9]+)*$/.test(name) && name.trim() === name)
  && new Set(patched).size === patched.length, "패치 Radix 목록 오류");
for (const name of patched) {
  assert.ok(registry.frontendPolicy.artifactPackages?.includes(name)
    && registry.frontendPolicy.packages?.includes(name), "패치 Radix 정책 등록 불일치");
  const axes = Object.entries(registry.axes).filter(([key, axis]) =>
    axis.ecosystem === "npm" && (axis.packages ?? [key]).includes(name));
  assert.ok(axes.length === 1 && axes[0][1].checked === false
    && axes[0][1].recommended == null && typeof axes[0][1].exact === "string"
    && axes[0][1].exact.trim(), "패치 Radix 정확 관리 축·버전 불일치");
  engines.push(fixedEngine(name, axes[0][1].exact));
}

// 모든 원본·선언·lock을 먼저 검증한다. 실패하면 어떤 대상의 vendor나 pin도 변경하지 않는다.
const targets = [root, fixture, new URL("../examples/next-app/", import.meta.url)];
const sections = ["dependencies", "devDependencies", "optionalDependencies", "peerDependencies"];
for (const target of targets) {
  const manifest = read(new URL("package.json", target));
  const lock = read(new URL("package-lock.json", target));
  for (const {name, label, version, filename, integrity} of engines) {
    const section = name === "lightningcss" || target === root ? "devDependencies" : "dependencies";
    const kind = section === "devDependencies" ? "개발" : "런타임";
    const spec = "file:vendor/" + filename;
    assert.equal(manifest[section]?.[name], spec, label + " " + kind + " 의존성 경로 불일치");
    for (const other of sections.filter(value => value !== section)) {
      assert.ok(!(name in (manifest[other] ?? {})), label + " 의존성 중복·범위 불일치");
      assert.ok(!(name in (lock.packages[""][other] ?? {})), label + " lock 직접 선언 중복·범위 불일치");
    }
    assert.equal(manifest.overrides?.[name], "$" + name, label + " 전이 override 누락");
    assert.equal(lock.packages[""][section]?.[name], spec, label + " lock 직접 선언 불일치");
    let copies = 0;
    for (const [location, entry] of Object.entries(lock.packages)) {
      if (!location.endsWith("node_modules/" + name) && entry.name !== name) continue;
      copies++;
      assert.equal(entry.version, version, label + " lock 전이 버전 불일치");
      assert.equal(entry.integrity, integrity, label + " lock 전이 bytes 불일치");
      assert.equal(entry.resolved, spec, label + " lock vendor 참조 불일치");
    }
    assert.ok(copies > 0, label + " lock 설치본 누락");
    if (name !== "lightningcss")
      assert.ok(lock.packages["node_modules/" + name], label + " lock 직접 설치본 누락");
  }
}
// root의 검증된 단일 원본만 두 실제 Next 경로에 복사한다. 원장/lock 해시는 덮어쓰지 않는다.
for (const target of targets.filter(value => value !== root)) {
  mkdirSync(new URL("vendor/", target), {recursive: true});
  for (const {source, filename} of engines) copyFileSync(source, new URL("vendor/" + filename, target));
}

// --css-only는 호환 옵션명이며 이제 모든 고정 엔진을 준비한다.
if (!process.argv.includes("--css-only")) {
  const manifest = read(new URL("package.json", fixture));
  const lockPath = new URL("package-lock.json", fixture);
  const lock = read(lockPath);
  // 매 실행에서 생성한 두 로컬 common 산출물만 갱신한다. 고정 엔진 pin은 위에서 검증한다.
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
console.log("root·smoke·example의 " + engines.map(engine => engine.label).join(", ") + " 고정 bytes 확인");
