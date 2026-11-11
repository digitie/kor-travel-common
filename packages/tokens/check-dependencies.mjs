// SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
// SPDX-License-Identifier: GPL-3.0-or-later
import { readFileSync, existsSync, readdirSync, realpathSync } from "node:fs";
import { resolve, dirname, basename, relative, isAbsolute, sep } from "node:path";
import { createHash } from "node:crypto";
import { parseArgs } from "node:util";
import { createRequire } from "node:module";
const { values } = parseArgs({ options: { profile: { type: "string", default: "web" }, policy: { type: "string" }, package: { type: "string", default: "package.json" }, lock: { type: "string", default: "package-lock.json" }, workspace: { type: "string", default: "" }, artifacts: { type: "string" }, canonical: { type: "string" }, source: { type: "string", multiple: true, default: [] } } });
const read = p => JSON.parse(readFileSync(p, "utf8"));
const bundledPolicy = new URL("./dependency-policy.json", import.meta.url);
const policy = read(values.policy ? resolve(values.policy) : existsSync(bundledPolicy) ? bundledPolicy : new URL("../frontend-dependencies.json", import.meta.url));
const artifactNames = new Set(policy.artifactPackages);
const skippedDirectories = new Set(["node_modules", ".next", "test", "tests", "e2e", "dist", "build", ".expo"]);
const packagePath = resolve(values.package), lockPath = resolve(values.lock);
const manifest = read(packagePath), lock = read(lockPath), errors = [];
let ts;
try { ts = createRequire(packagePath)("typescript"); }
catch { ts = createRequire(import.meta.url)("typescript"); }
const sections = ["dependencies", "devDependencies", "optionalDependencies", "peerDependencies"];
const deps = {}, declaredBy = new Map();
for (const section of sections) {
 for (const [name, spec] of Object.entries(manifest[section] ?? {})) {
  if (declaredBy.has(name)) errors.push(name + ": " + declaredBy.get(name) + "/" + section + " 중복 선언");
  const wanted = policy.versions[name];
  if (wanted && !artifactNames.has(name) && spec !== wanted) errors.push(name + ": " + section + " 선언 " + spec + " != " + wanted);
  declaredBy.set(name, section); deps[name] = spec;
 }
}
for (const name of Object.keys(deps)) if (name.startsWith("@radix-ui/react-")) errors.push(name + ": 개별 Radix 대신 공통 UI 경로 사용");
if (!policy.profiles[values.profile]) throw new Error("알 수 없는 검사 프로필");
const profile = policy.profiles[values.profile];
for (const name of profile.required) {
 if (!(name in deps)) errors.push(name + ": 필수 직접 의존성 없음");
 if (!policy.versions[name]) errors.push(name + ": 필수 항목의 정확 버전 정본 없음");
}
for (const name of profile.runtimeRequired ?? []) if (!(name in (manifest.dependencies ?? {}))) errors.push(name + ": dependencies에 필수 런타임 선언 필요");
const forbidden = new Set([...policy.forbidden, ...(profile.forbidden ?? [])]);
for (const name of forbidden) if (name in deps) errors.push(name + ": " + (name === "maplibre-vworld-react" ? "공개 core/web/RN 배포물로 이관 필요" : "공통 Radix 구현으로 이관 필요"));
function resolveInstalled(name, directory = values.workspace) {
 const parts = directory.split("/").filter(Boolean);
 for (let i = parts.length; i >= 0; i--) {
  if (parts[i - 1] === "node_modules") continue;
  const key = [...parts.slice(0, i), "node_modules", name].join("/");
  const entry = lock.packages?.[key];
  if (!entry) continue;
  if (entry.link) {
   const location = entry.resolved?.replace(/^file:/, "");
   return location && lock.packages?.[location] ? { location, entry: lock.packages[location] } : undefined;
  }
  return { location: key, entry };
 }
 return undefined;
}
const installed = name => resolveInstalled(name)?.entry;
// 별도 도구·다른 workspace가 아닌, 이 앱의 런타임 의존 그래프만 검사한다.
const visited = new Set(), runtime = [{ location: values.workspace, entry: manifest }];
const reactLocations = new Map([["react", new Set()], ["react-dom", new Set()]]);
for (let index = 0; index < runtime.length; index++) {
 const { location, entry } = runtime[index];
 for (const name of Object.keys({ ...entry.dependencies, ...entry.optionalDependencies, ...entry.peerDependencies })) {
  const found = resolveInstalled(name, location);
  if (!found) continue;
  const identity = found.entry.name ?? name;
  if (reactLocations.has(identity)) {
   reactLocations.get(identity).add(found.location);
   if (found.entry.version !== policy.versions[identity]) errors.push(identity + ": 런타임 전이 버전 " + found.entry.version + " != " + policy.versions[identity]);
  }
  if (artifactNames.has(identity) && !(identity in deps)) errors.push(identity + ": 공통 vendor 직접 의존성으로 고정 필요");
  if (!visited.has(found.location)) {
   visited.add(found.location); runtime.push(found);
  }
 }
}
for (const [name, locations] of reactLocations) if (locations.size > 1) errors.push(name + ": 런타임 중복 인스턴스 " + [...locations].join(", "));
const artifactPaths = new Map();
const artifactRoot = realpathSync(dirname(lockPath));
for (const [name, spec] of Object.entries(deps)) {
 const wanted = policy.versions[name];
 if (!wanted) continue;
 if (artifactNames.has(name)) {
  const filename = (name.startsWith("@") ? name.slice(1).replace("/", "-") : name) + "-" + wanted + ".tgz";
  const path = spec.startsWith("file:") ? resolve(dirname(packagePath), spec.slice(5)) : null;
  const locations = path ? [relative(dirname(lockPath), path), relative(artifactRoot, existsSync(path) ? realpathSync(path) : path)] : [];
  if (!path || isAbsolute(spec.slice(5)) || basename(path) !== filename || basename(dirname(path)) !== "vendor"
    || locations.some(location => location === ".." || location.startsWith(".." + sep) || isAbsolute(location)))
    errors.push(name + ": 공통 vendor 산출물 참조 불일치");
  else artifactPaths.set(name, path);
 } else if (spec !== wanted) errors.push(name + ": 선언 " + spec + " != " + wanted);
 const got = installed(name);
 if (got?.version !== wanted) errors.push(name + ": lock 설치 버전 " + got?.version + " != " + wanted);
}
// CSS는 빌드/개발 의존성에서도 실행되므로 해당 앱의 개발 그래프까지 같은 bytes를 확인한다.
const cssCopies = new Map(), buildVisited = new Set();
const build = [{ location: values.workspace, entry: manifest }];
for (let index = 0; index < build.length; index++) {
 const { location, entry } = build[index];
 const dependencies = { ...entry.dependencies, ...entry.optionalDependencies, ...entry.peerDependencies,
  ...(index === 0 ? manifest.devDependencies : {}) };
 for (const name of Object.keys(dependencies)) {
  const found = resolveInstalled(name, location);
  if (!found) continue;
  if ((found.entry.name ?? name) === "lightningcss") cssCopies.set(found.location, found.entry);
  if (!buildVisited.has(found.location)) {
   buildVisited.add(found.location); build.push(found);
  }
 }
}
// 체크인한 산출물 원장은 실제 bytes와 lock integrity를 함께 검증한다.
if (!values.artifacts) errors.push("--artifacts 공통 산출물 원장이 필요함");
else {
 const artifacts = read(resolve(values.artifacts));
 const canonical = values.canonical ? read(resolve(values.canonical)) : null;
 if (process.env.KT_REQUIRE_CANONICAL === "1" && !values.policy) errors.push("중앙 CI는 --policy 최신 정본을 요구함");
 if (process.env.KT_REQUIRE_CANONICAL === "1" && !canonical) errors.push("중앙 CI는 --canonical 산출물 정본을 요구함");
 for (const name of artifactNames) {
  if (!(name in deps)) continue;
  const artifact = artifacts.packages?.[name], spec = deps[name];
  if (canonical && (canonical.packages?.[name]?.integrity !== artifact?.integrity
    || canonical.packages?.[name]?.version !== artifact?.version)) errors.push(name + ": 중앙 산출물 정본과 다름");
  if (!artifact?.integrity || !spec.startsWith("file:")) { errors.push(name + ": 산출물 무결성 원장 누락"); continue; }
  const path = artifactPaths.get(name);
  if (!path) continue;
  if (!existsSync(path)) { errors.push(name + ": 산출물 파일 없음"); continue; }
  const actual = "sha512-" + createHash("sha512").update(readFileSync(path)).digest("base64");
  if (artifact.integrity !== actual || installed(name)?.integrity !== actual) errors.push(name + ": 파일·원장·lock 해시 불일치");
  if (name === "lightningcss") for (const [location, entry] of cssCopies) {
   if (entry.version !== policy.versions[name] || entry.integrity !== actual)
    errors.push(name + ": 빌드 전이 버전·bytes 불일치 " + location);
  }
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
    if (ts.isImportDeclaration(node) && ts.isStringLiteral(node.moduleSpecifier)) {
     const imported = node.moduleSpecifier.text;
     if ([...forbidden].some(name => imported === name || imported.startsWith(name + "/")))
      errors.push(file + ": 공통 정책의 금지 패키지 import: " + imported);
    }
    if (ts.isImportDeclaration(node) && ts.isStringLiteral(node.moduleSpecifier)
      && (node.moduleSpecifier.text.startsWith("@base-ui/react") || node.moduleSpecifier.text.startsWith("@floating-ui/") || node.moduleSpecifier.text.startsWith("@radix-ui/react-"))) errors.push(file + ": 공통 Radix 외 overlay 구현");
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
