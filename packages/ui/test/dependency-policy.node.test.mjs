// SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
// SPDX-License-Identifier: GPL-3.0-or-later
import { test } from "node:test";
import assert from "node:assert/strict";
import { mkdtempSync, mkdirSync, writeFileSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { createHash } from "node:crypto";
import { spawnSync } from "node:child_process";
import policy from "../dependency-policy.json" with { type: "json" };
function fixture(change, {profile="web",workspace=""}={}) {
 const root=mkdtempSync(join(tmpdir(),"kt-policy-"));
 try {
  const dependencies={}, packages={}, artifacts={packages:{}};
  mkdirSync(join(root,"vendor"));
  mkdirSync(join(root,"src"));
  for(const name of policy.profiles[profile].required) {
   const version=policy.versions[name] ?? "1.0.0";
   dependencies[name]=version; packages["node_modules/"+name]={version};
   if(name.startsWith("@kor-travel/")) {
    const filename=name.slice(1).replace("/","-")+"-"+version+".tgz";
    const bytes=Buffer.from(name), integrity="sha512-"+createHash("sha512").update(bytes).digest("base64");
    writeFileSync(join(root,"vendor",filename),bytes);
    dependencies[name]="file:vendor/"+filename;packages["node_modules/"+name].integrity=integrity;artifacts.packages[name]={version,integrity};
   }
  }
  change?.({dependencies,packages,artifacts,root});
  writeFileSync(join(root,"package.json"),JSON.stringify({dependencies}));
  writeFileSync(join(root,"package-lock.json"),JSON.stringify({lockfileVersion:3,packages}));
  writeFileSync(join(root,"common-artifacts.json"),JSON.stringify(artifacts));
  return spawnSync(process.execPath,[new URL("../check-dependencies.mjs",import.meta.url).pathname,"--artifacts","common-artifacts.json","--profile",profile,"--workspace",workspace],{cwd:root,encoding:"utf8"});
 } finally {rmSync(root,{recursive:true,force:true});}
}
test("동일 선언·lock·산출물은 통과",()=>{const result=fixture();assert.equal(result.status,0,result.stderr);});
function rejected(result, reason) {
 assert.equal(result.status,1,result.stderr);
 assert.ok(result.stderr.includes(reason), result.stderr);
}
test("lock 버전만 달라도 실패",()=>rejected(fixture(({packages})=>packages["node_modules/react"].version="0.0.0"),"lock 설치 버전"));
test("같은 버전의 다른 bytes를 거부",()=>rejected(fixture(({root})=>writeFileSync(join(root,"vendor/kor-travel-ui-0.2.0.tgz"),"다른 파일")),"파일·원장·lock 해시 불일치"));
test("Base UI 직접 의존을 거부",()=>rejected(fixture(({dependencies})=>dependencies["@base-ui/react"]="1.9.0"),"공통 Radix 구현으로 이관 필요"));
test("네이티브 표 재도입을 거부",()=>rejected(fixture(({root})=>writeFileSync(join(root,"src/table.tsx"),"export const T = () => <table><tbody /></table>")),"공통 VirtualTable 외 표 구현"));
test("개별 floating 구현을 거부",()=>rejected(fixture(({root})=>writeFileSync(join(root,"src/dialog.tsx"),"import { useFloating } from '@floating-ui/react';")),"공통 Radix 외 overlay 구현"));
test("설명 주석의 표 예시는 구현으로 오인하지 않는다",()=>{const result=fixture(({root})=>writeFileSync(join(root,"src/readme.tsx"),"// <table> 설명\nexport const n = 1;"));assert.equal(result.status,0,result.stderr);});
test("모바일 workspace의 Tailwind4가 root의 다른 버전보다 우선한다",()=>{
 const result=fixture(({packages})=>{
  packages["apps/mobile/node_modules/tailwindcss"]={version:policy.versions.tailwindcss};
  packages["node_modules/tailwindcss"]={version:"3.4.0"};
 },{profile:"mobile",workspace:"apps/mobile"});
 assert.equal(result.status,0,result.stderr);
});
