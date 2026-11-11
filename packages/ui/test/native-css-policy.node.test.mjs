// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
import { test } from "node:test";
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { mkdtempSync, mkdirSync, writeFileSync, readFileSync, existsSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { spawnSync } from "node:child_process";
import policy from "../dependency-policy.json" with { type: "json" };

const prepare = new URL("../smoke/prepare-lock.mjs", import.meta.url);
const version = policy.versions.lightningcss;
const filename = "lightningcss-" + version + ".tgz";
const bytes = Buffer.from("고정 CSS compiler bytes");
const integrity = "sha512-" + createHash("sha512").update(bytes).digest("base64");

function fixture(change, cssOnly = true) {
 const root = mkdtempSync(join(tmpdir(), "kt-css-prepare-"));
 const dirs = ["", "packages/ui/smoke/next-app", "packages/ui/examples/next-app"];
 const json = (path, data) => writeFileSync(path, JSON.stringify(data, null, 2) + "\n");
 const script = join(root, "packages/ui/smoke/prepare-lock.mjs");
 try {
  mkdirSync(join(root, "vendor"));
  writeFileSync(join(root, "vendor", filename), bytes);
  json(join(root, "versions.json"), { axes: {lightningcss: {exact: version}} });
  json(join(root, "frontend-artifacts.json"), {packages: {lightningcss: {version, filename, integrity}}});
  for (const directory of dirs) {
   const target = join(root, directory);
   mkdirSync(target, {recursive: true});
   const manifest = {devDependencies: {lightningcss: "file:vendor/" + filename}, overrides: {lightningcss: "$lightningcss"}};
   const lock = {lockfileVersion: 3, packages: {"": {devDependencies: {...manifest.devDependencies}},
    "node_modules/lightningcss": {version, resolved: manifest.devDependencies.lightningcss, integrity}}};
   if (directory.includes("/smoke/")) {
    manifest.dependencies = {};
    lock.packages[""].dependencies = {};
    for (const [name, archive] of [["@kor-travel/ui","kor-travel-ui-0.2.0.tgz"], ["@kor-travel/tokens","kor-travel-tokens-0.1.1.tgz"]]) {
     const spec = "file:../../../../test-results/ui-pack/" + archive;
     manifest.dependencies[name] = spec;
     lock.packages[""].dependencies[name] = spec;
     lock.packages["node_modules/" + name] = {resolved: spec, integrity: "이전 개발 산출물"};
     mkdirSync(join(root,"test-results/ui-pack"),{recursive:true});
     writeFileSync(join(root,"test-results/ui-pack",archive),Buffer.from(name));
    }
   }
   json(join(target, "package.json"), manifest);
   json(join(target, "package-lock.json"), lock);
  }
  writeFileSync(script, readFileSync(prepare));
  change?.({root, dirs, json});
  const before = dirs.map(directory => readFileSync(join(root,directory,"package-lock.json"),"utf8"));
  const result = spawnSync(process.execPath,[script,...(cssOnly?["--css-only"]:[])],{cwd:root,encoding:"utf8"});
  const after = dirs.map(directory => readFileSync(join(root,directory,"package-lock.json"),"utf8"));
  const copied = dirs.slice(1).map(directory => {
   const path=join(root,directory,"vendor",filename);
   return existsSync(path)?readFileSync(path):undefined;
  });
  return {result,before,after,copied};
 } finally {rmSync(root,{recursive:true,force:true});}
}

test("CSS 준비는 두 Next 경로에 동일 bytes를 복사하고 고정 lock을 바꾸지 않는다",()=>{
 const {result,before,after,copied}=fixture();
 assert.equal(result.status,0,result.stderr);
 assert.deepEqual(after,before);
 for(const copy of copied) assert.deepEqual(copy,bytes);
});
test("기본 준비는 common 개발 pack 해시만 갱신하고 CSS 정본은 유지",()=>{
 const {result,before,after}=fixture(undefined,false);
 assert.equal(result.status,0,result.stderr);
 const old=JSON.parse(before[1]),fresh=JSON.parse(after[1]);
 assert.notEqual(fresh.packages["node_modules/@kor-travel/ui"].integrity,old.packages["node_modules/@kor-travel/ui"].integrity);
 assert.deepEqual(fresh.packages["node_modules/lightningcss"],old.packages["node_modules/lightningcss"]);
 assert.equal(after[0],before[0]); assert.equal(after[2],before[2]);
});
test("root CSS vendor 재포장은 복사 전에 거부",()=>{
 const {result,copied}=fixture(({root})=>writeFileSync(join(root,"vendor",filename),"임의 재포장"));
 assert.equal(result.status,1);
 assert.match(result.stderr,/원본 vendor bytes 불일치/);
 assert.deepEqual(copied,[undefined,undefined]);
});
test("별도 Next lock의 중첩 stock CSS는 거부",()=>{
 const {result}=fixture(({root,dirs,json})=>{
  const path=join(root,dirs[2],"package-lock.json"),lock=JSON.parse(readFileSync(path,"utf8"));
  lock.packages["node_modules/builder/node_modules/lightningcss"]={version:"1.33.0",resolved:"registry",integrity};
  json(path,lock);
 });
 assert.equal(result.status,1);
 assert.match(result.stderr,/lock 전이 버전 불일치/);
});
test("고정 CSS lock integrity를 원본 bytes로 조용히 갱신하지 않는다",()=>{
 const {result,before,after}=fixture(({root,dirs,json})=>{
  const path=join(root,dirs[1],"package-lock.json"),lock=JSON.parse(readFileSync(path,"utf8"));
  lock.packages["node_modules/lightningcss"].integrity="조작한 해시";
  json(path,lock);
 });
 assert.equal(result.status,1);
 assert.match(result.stderr,/lock 전이 bytes 불일치/);
 assert.deepEqual(after,before);
});
