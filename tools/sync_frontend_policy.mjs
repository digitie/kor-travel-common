// SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
// SPDX-License-Identifier: GPL-3.0-or-later
import { readFileSync, writeFileSync } from "node:fs";
const registry = JSON.parse(readFileSync(new URL("../versions.json", import.meta.url), "utf8"));
const allowedPolicyFields = new Set(["schema", "forbidden", "exceptions", "artifactPackages", "profiles", "packages", "patchedRadixPackages"]);
if (!registry.frontendPolicy || typeof registry.frontendPolicy !== "object" || Array.isArray(registry.frontendPolicy)
 || Object.keys(registry.frontendPolicy).some(name => !allowedPolicyFields.has(name)))
 throw new Error("프런트 정책 객체·미지 필드 오류");
const { packages, ...metadata } = registry.frontendPolicy;
const versions = {};
for (const name of packages) {
  const axes = Object.entries(registry.axes).filter(([key, axis]) =>
    axis.ecosystem === "npm" && (axis.packages ?? [key]).includes(name));
  const values = new Set(axes.map(([, axis]) => (axis.exact ?? axis.recommended)));
  if (values.size !== 1 || ![...values][0]) throw new Error(name + ": 정확 버전 정본을 찾을 수 없음");
  versions[name] = [...values][0];
}
// 선택 목록이 없으면 기존 정책을 유지하고, 명시하면 독립 생성에서도 같은 좁은 계약을 적용한다.
const patched = Object.hasOwn(metadata, "patchedRadixPackages") ? metadata.patchedRadixPackages : [];
if (!Array.isArray(patched) || patched.some(name => typeof name !== "string"
 || !/^@radix-ui\/react-[a-z0-9]+(?:-[a-z0-9]+)*$/.test(name) || name.trim() !== name)
 || new Set(patched).size !== patched.length)
 throw new Error("patchedRadixPackages 목록 오류");
const exactSemVer = /^(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)(?:-(?:0|[1-9][0-9]*|[0-9]*[A-Za-z-][0-9A-Za-z-]*)(?:\.(?:0|[1-9][0-9]*|[0-9]*[A-Za-z-][0-9A-Za-z-]*))*)?(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$/;
for (const name of patched) {
 const axes = Object.entries(registry.axes).filter(([key, axis]) =>
  axis.ecosystem === "npm" && (axis.packages ?? [key]).includes(name));
 const axis = axes.length === 1 ? axes[0][1] : null;
 if (!packages.includes(name) || !metadata.artifactPackages.includes(name) || !axis
  || axis.checked !== false || axis.recommended != null || typeof axis.exact !== "string"
  || axis.exact.trim() !== axis.exact || !exactSemVer.test(axis.exact))
  throw new Error("patchedRadixPackages 정확 관리 축·산출물 연결 오류");
}
for (const [name, profile] of Object.entries(metadata.profiles)) {
  const required = new Set(profile.required);
  const forbidden = new Set([...metadata.forbidden, ...(profile.forbidden ?? [])]);
  for (const dependency of required)
    if (!versions[dependency] || forbidden.has(dependency)) throw new Error(name + ": 필수 의존성의 버전·금지 조건 충돌");
  for (const dependency of profile.runtimeRequired ?? [])
    if (!required.has(dependency)) throw new Error(name + ": 런타임 필수 항목의 선언 누락");
}
for (const dependency of metadata.artifactPackages)
  if (!versions[dependency]) throw new Error(dependency + ": 산출물 정확 버전 누락");
const generated = { generatedFrom: "versions.json", ...metadata, versions };
const target = new URL("../frontend-dependencies.json", import.meta.url);
const content = JSON.stringify(generated, null, 2) + "\n";
const documentTarget = new URL("../docs/standards/frontend-libraries.md", import.meta.url);
const document = readFileSync(documentTarget, "utf8");
const start = "<!-- frontend-library-versions:start -->", end = "<!-- frontend-library-versions:end -->";
const first = document.indexOf(start), last = document.indexOf(end);
if (first < 0 || last < first || first !== document.lastIndexOf(start) || last !== document.lastIndexOf(end))
  throw new Error("라이브러리 문서의 단일 생성 영역 표시가 필요함");
const table = ["| 라이브러리 | 정확 버전 |", "|---|---|",
  ...Object.keys(versions).sort().map(name => "| " + name + " | " + versions[name] + " |")].join("\n");
const generatedDocument = document.slice(0, first + start.length) + "\n\n" + table + "\n\n" + document.slice(last);
const outputs = [[target, content], [documentTarget, generatedDocument]];
for (const [path, expected] of outputs) {
  if (process.argv.includes("--check")) {
    if (readFileSync(path, "utf8") !== expected) throw new Error(path.pathname + ": 생성물이 versions.json 정본과 다름");
  } else writeFileSync(path, expected);
}
