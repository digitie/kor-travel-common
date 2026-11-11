// SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
// SPDX-License-Identifier: GPL-3.0-or-later
import { readFileSync, existsSync, readdirSync } from "node:fs";
import { resolve, dirname } from "node:path";
import { createHash } from "node:crypto";
import { parseArgs } from "node:util";
import { createRequire } from "node:module";
const { values } = parseArgs({ options: { profile: { type: "string", default: "web" }, package: { type: "string", default: "package.json" }, lock: { type: "string", default: "package-lock.json" }, workspace: { type: "string", default: "" }, artifacts: { type: "string" }, source: { type: "string", multiple: true, default: [] } } });
const read = p => JSON.parse(readFileSync(p, "utf8"));
const bundledPolicy = new URL("./dependency-policy.json", import.meta.url);
const policy = read(existsSync(bundledPolicy) ? bundledPolicy : new URL("../frontend-dependencies.json", import.meta.url));
const artifactNames = new Set(policy.artifactPackages);
const skippedDirectories = new Set(["node_modules", ".next", "test", "tests", "e2e", "dist", "build", ".expo"]);
const packagePath = resolve(values.package), lockPath = resolve(values.lock);
const manifest = read(packagePath), lock = read(lockPath), errors = [];
let ts;
try { ts = createRequire(packagePath)("typescript"); }
catch { ts = createRequire(import.meta.url)("typescript"); }
const deps = { ...manifest.dependencies, ...manifest.devDependencies };
if (!policy.profiles[values.profile]) throw new Error("알 수 없는 검사 프로필");
for (const name of policy.profiles[values.profile].required) if (!(name in deps)) errors.push(name + ": 필수 직접 의존성 없음");
for (const name of policy.forbidden) if (name in deps) errors.push(name + ": 공통 Radix 구현으로 이관 필요");
function installed(name) {
 const parts = values.workspace.split("/").filter(Boolean);
 for (let i=parts.length;i>=0;i--) {
  const key = [...parts.slice(0,i), "node_modules",name].join("/");
  if (lock.packages?.[key]) return lock.packages[key];
 }
 return undefined;
}
for (const [name, spec] of Object.entries(deps)) {
 const wanted = policy.versions[name];
 if (!wanted) continue;
 if (artifactNames.has(name)) {
  if (spec !== "file:vendor/" + (name.startsWith("@") ? name.slice(1).replace("/", "-") : name) + "-" + wanted + ".tgz") errors.push(name + ": 공통 vendor 산출물 참조 불일치");
 } else if (spec !== wanted) errors.push(name + ": 선언 " + spec + " != " + wanted);
 const got = installed(name);
 if (got?.version !== wanted) errors.push(name + ": lock 설치 버전 " + got?.version + " != " + wanted);
}
// 체크인한 산출물 원장은 실제 bytes와 lock integrity를 함께 검증한다.
if (!values.artifacts) errors.push("--artifacts 공통 산출물 원장이 필요함");
else {
 const artifacts = read(resolve(values.artifacts));
 for (const name of ["@kor-travel/ui","@kor-travel/tokens","vworld-map-web","vworld-map-core"]) {
  if (!(name in deps)) continue;
  const artifact = artifacts.packages?.[name], spec = deps[name];
  if (!artifact?.integrity || !spec.startsWith("file:")) { errors.push(name + ": 산출물 무결성 원장 누락"); continue; }
  const path = resolve(dirname(packagePath), spec.slice(5));
  if (!existsSync(path)) { errors.push(name + ": 산출물 파일 없음"); continue; }
  const actual = "sha512-" + createHash("sha512").update(readFileSync(path)).digest("base64");
  if (artifact.integrity !== actual || installed(name)?.integrity !== actual) errors.push(name + ": 파일·원장·lock 해시 불일치");
 }
}
function scan(path) {
 if (!existsSync(path)) { errors.push(path + ": 검사할 소스 경로 없음"); return; }
 for (const entry of readdirSync(path, { withFileTypes: true })) {
  if (skippedDirectories.has(entry.name)) continue;
  const file = resolve(path, entry.name);
  if (entry.isDirectory()) scan(file);
  else if (/\.[jt]sx?$/.test(entry.name) && !/\.(test|spec)\./.test(entry.name)) {
   const source = ts.createSourceFile(file, readFileSync(file, "utf8"), ts.ScriptTarget.Latest, true);
   function visit(node) {
    if (ts.isJsxOpeningElement(node) || ts.isJsxSelfClosingElement(node)) {
     const tag = node.tagName.getText(source);
     if (tag === "table" || tag === "Table") errors.push(file + ": 공통 VirtualTable 외 표 구현");
    }
    if (ts.isImportDeclaration(node) && ts.isStringLiteral(node.moduleSpecifier)
      && (node.moduleSpecifier.text.startsWith("@base-ui/react") || node.moduleSpecifier.text.startsWith("@floating-ui/"))) errors.push(file + ": 공통 Radix 외 overlay 구현");
    ts.forEachChild(node, visit);
   }
   visit(source);
  }
 }
}
// 옵션을 생략해도 실제 앱 소스를 자동 검사한다.
const sourcePaths = values.source.length ? values.source.map(path => resolve(path))
 : ["src", "app", "components", "lib"].map(path => resolve(dirname(packagePath), path)).filter(existsSync);
if (!sourcePaths.length) errors.push("검사할 앱 소스가 없음: --source 경로 지정 필요");
for (const path of sourcePaths) scan(path);
if (errors.length) { console.error(errors.join("\n")); process.exitCode = 1; }
else console.log("공통 의존성과 산출물 일치");
