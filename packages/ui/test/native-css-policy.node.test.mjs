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

const scopeName = "@radix-ui/react-focus-scope";
const scopeVersion = "1.3.1+kortravel.fix.1";
const scopeFilename = "radix-ui-react-focus-scope-" + scopeVersion + ".tgz";
const scopeBytes = Buffer.from("고정 FocusScope engine fixture bytes");
const scopeIntegrity = "sha512-" + createHash("sha512").update(scopeBytes).digest("base64");

function fixture(change, cssOnly = true, {scope = false} = {}) {
 const root = mkdtempSync(join(tmpdir(), "kt-css-prepare-"));
 const dirs = ["", "packages/ui/smoke/next-app", "packages/ui/examples/next-app"];
 const json = (path, data) => writeFileSync(path, JSON.stringify(data, null, 2) + "\n");
 const script = join(root, "packages/ui/smoke/prepare-lock.mjs");
 try {
  mkdirSync(join(root, "vendor"));
  writeFileSync(join(root, "vendor", filename), bytes);
  const registry = {axes: {lightningcss: {exact: version}}};
  const artifacts = {packages: {lightningcss: {version, filename, integrity}}};
  if (scope) {
   registry.axes["scope-engine-alias"] = {ecosystem:"npm",packages:[scopeName],exact:scopeVersion,checked:false,recommended:null};
   registry.frontendPolicy = {patchedRadixPackages:[scopeName],artifactPackages:["lightningcss",scopeName],packages:["lightningcss",scopeName]};
   artifacts.packages[scopeName] = {version:scopeVersion,filename:scopeFilename,integrity:scopeIntegrity};
   writeFileSync(join(root,"vendor",scopeFilename),scopeBytes);
  }
  json(join(root, "versions.json"), registry);
  json(join(root, "frontend-artifacts.json"), artifacts);
  for (const directory of dirs) {
   const target = join(root, directory);
   mkdirSync(target, {recursive: true});
   const manifest = {devDependencies: {lightningcss: "file:vendor/" + filename}, overrides: {lightningcss: "$lightningcss"}};
   const lock = {lockfileVersion: 3, packages: {"": {devDependencies: {...manifest.devDependencies}},
    "node_modules/lightningcss": {version, resolved: manifest.devDependencies.lightningcss, integrity}}};
   if (scope) {
    const section = directory === "" ? "devDependencies" : "dependencies";
    const spec = "file:vendor/" + scopeFilename;
    (manifest[section] ??= {})[scopeName] = spec;
    manifest.overrides[scopeName] = "$" + scopeName;
    (lock.packages[""][section] ??= {})[scopeName] = spec;
    // npm v3가 실제 사용하는 metadata를 고정 pin 외에는 보존해야 한다.
    lock.packages["node_modules/"+scopeName] = {
     version:scopeVersion,resolved:spec,integrity:scopeIntegrity,license:"MIT",
     dependencies:{"@radix-ui/react-compose-refs":"1.1.5","@radix-ui/react-primitive":"2.2.0","@radix-ui/react-use-callback-ref":"1.1.5"},
     peerDependencies:{"@types/react":"*","@types/react-dom":"*",react:"^16.8 || ^17.0 || ^18.0 || ^19.0 || ^19.0.0-rc","react-dom":"^16.8 || ^17.0 || ^18.0 || ^19.0 || ^19.0.0-rc"},
     peerDependenciesMeta:{"@types/react":{optional:true},"@types/react-dom":{optional:true}}
    };
   }
   if (directory.includes("/smoke/")) {
    manifest.dependencies ??= {};
    lock.packages[""].dependencies ??= {};
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
  const scopeCopied = dirs.slice(1).map(directory => {
   const path=join(root,directory,"vendor",scopeFilename);
   return existsSync(path)?readFileSync(path):undefined;
  });
  return {result,before,after,copied,scopeCopied};
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

function mutateJson(context, directory, file, change) {
 const path=join(context.root,directory,file), value=JSON.parse(readFileSync(path,"utf8"));
 change(value);context.json(path,value);
}
function scopeRejected(change,reason,cssOnly=true) {
 const outcome=fixture(change,cssOnly,{scope:true});
 assert.equal(outcome.result.status,1,outcome.result.stderr);
 if(reason)assert.match(outcome.result.stderr,reason);
 assert.deepEqual(outcome.after,outcome.before);
 assert.deepEqual(outcome.scopeCopied,[undefined,undefined]);
 assert.deepEqual(outcome.copied,[undefined,undefined]);
}
test("패치 엔진은 alias axis와 실제 npm metadata를 보존하며 두 Next vendor로 복사",()=>{
 const {result,before,after,copied,scopeCopied}=fixture(undefined,true,{scope:true});
 assert.equal(result.status,0,result.stderr);assert.deepEqual(after,before);
 for(const copy of copied)assert.deepEqual(copy,bytes);
 for(const copy of scopeCopied)assert.deepEqual(copy,scopeBytes);
});
test("패치 엔진을 포함한 기본 모드도 common 개발 pack 해시만 갱신",()=>{
 const {result,before,after,scopeCopied}=fixture(undefined,false,{scope:true});
 assert.equal(result.status,0,result.stderr);
 assert.equal(after[0],before[0]);assert.equal(after[2],before[2]);
 const old=JSON.parse(before[1]),fresh=JSON.parse(after[1]);
 assert.notEqual(fresh.packages["node_modules/@kor-travel/ui"].integrity,old.packages["node_modules/@kor-travel/ui"].integrity);
 for(const name of ["lightningcss",scopeName])assert.deepEqual(fresh.packages["node_modules/"+name],old.packages["node_modules/"+name]);
 for(const copy of scopeCopied)assert.deepEqual(copy,scopeBytes);
});
test("패치 엔진 root vendor 변조는 CSS 포함 복사·lock 수정 전에 거부",()=>{
 scopeRejected(({root})=>writeFileSync(join(root,"vendor",scopeFilename),"다른 Scope bytes"),/원본 vendor bytes 불일치/,false);
});
for(const field of ["version","filename","integrity"]) {
 test("패치 엔진 canonical "+field+" 불일치를 거부",()=>{
  scopeRejected(context=>mutateJson(context,"","frontend-artifacts.json",value=>{
   value.packages[scopeName][field]="다른 정본";
  }),/정본 불일치|원본 vendor bytes 불일치/);
 });
}
test("패치 엔진 canonical 원장 누락을 거부",()=>{
 scopeRejected(context=>mutateJson(context,"","frontend-artifacts.json",value=>delete value.packages[scopeName]));
});
for(const change of ["missing","duplicate","unmanaged"]) {
 test("패치 엔진 "+change+" axis를 거부",()=>{
  scopeRejected(context=>mutateJson(context,"","versions.json",value=>{
   if(change==="missing")delete value.axes["scope-engine-alias"];
   if(change==="duplicate")value.axes.other={...value.axes["scope-engine-alias"]};
   if(change==="unmanaged"){delete value.axes["scope-engine-alias"].exact;value.axes["scope-engine-alias"].recommended=scopeVersion;}
  }),/정확.*축|정확.*버전/);
 });
}
for(const directory of ["","packages/ui/smoke/next-app","packages/ui/examples/next-app"]) {
 const label=directory || "root";
 for(const change of ["registry-direct","wrong-section","override","lock-direct","missing-install"]) {
  test("패치 엔진 "+label+" "+change+" 불일치는 pin 재작성 없이 거부",()=>{
   scopeRejected(context=>{
    if(change==="registry-direct")mutateJson(context,directory,"package.json",value=>{
     value[directory===""?"devDependencies":"dependencies"][scopeName]=scopeVersion;
    });
    if(change==="wrong-section")mutateJson(context,directory,"package.json",value=>{
     const expected=directory===""?"devDependencies":"dependencies",opposite=expected==="dependencies"?"devDependencies":"dependencies";
     const spec=value[expected][scopeName];delete value[expected][scopeName];(value[opposite] ??= {})[scopeName]=spec;
    });
    if(change==="override")mutateJson(context,directory,"package.json",value=>delete value.overrides[scopeName]);
    if(change==="lock-direct")mutateJson(context,directory,"package-lock.json",value=>{
     value.packages[""][directory===""?"devDependencies":"dependencies"][scopeName]=scopeVersion;
    });
    if(change==="missing-install")mutateJson(context,directory,"package-lock.json",value=>delete value.packages["node_modules/"+scopeName]);
   },/의존성|override|직접 선언|설치본/);
  });
 }
 for(const change of ["version","integrity","resolved"]) {
  test("패치 엔진 "+label+" nested "+change+" 불일치는 전체 lock에서 거부",()=>{
   scopeRejected(context=>mutateJson(context,directory,"package-lock.json",value=>{
    const entry={...value.packages["node_modules/"+scopeName]};
    entry[change]=change==="version"?"1.3.1":change==="integrity"?"sha512-stock-bytes":"https://registry.example/stock.tgz";
    value.packages["node_modules/helper/node_modules/"+scopeName]=entry;
   }),/lock 전이 버전 불일치|lock 전이 bytes 불일치|lock vendor 참조 불일치/);
  });
 }
}
test("패치 엔진 alias 위치의 stock 설치도 거부",()=>{
 scopeRejected(context=>mutateJson(context,"packages/ui/examples/next-app","package-lock.json",value=>{
  value.packages["node_modules/scope-alias"]={...value.packages["node_modules/"+scopeName],name:scopeName,integrity:"sha512-stock"};
 }),/lock 전이 bytes 불일치/);
});
test("패치 엔진 실패 시 기존 Next vendor와 잠긴 값도 그대로 보존",()=>{
 const outcome=fixture(context=>{
  for(const directory of context.dirs.slice(1)){
   mkdirSync(join(context.root,directory,"vendor"),{recursive:true});
   writeFileSync(join(context.root,directory,"vendor",scopeFilename),"기존 Scope 파일");
  }
  mutateJson(context,"packages/ui/examples/next-app","package-lock.json",value=>{
   value.packages["node_modules/"+scopeName].integrity="sha512-invalid";
  });
 },false,{scope:true});
 assert.equal(outcome.result.status,1);
 assert.deepEqual(outcome.after,outcome.before);
 for(const copy of outcome.scopeCopied)assert.deepEqual(copy,Buffer.from("기존 Scope 파일"));
});
