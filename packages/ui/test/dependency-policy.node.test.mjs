// SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
// SPDX-License-Identifier: GPL-3.0-or-later
import { test } from "node:test";
import assert from "node:assert/strict";
import { mkdtempSync, mkdirSync, writeFileSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { fileURLToPath } from "node:url";
import { createHash } from "node:crypto";
import { spawnSync } from "node:child_process";
import policy from "../dependency-policy.json" with { type: "json" };
function fixture(change, {profile="web",workspace="",canonical=false,policyOverride,requireCanonical=false}={}) {
 const root=mkdtempSync(join(tmpdir(),"kt-policy-"));
 try {
  const dependencies={}, devDependencies={}, packages={}, artifacts={packages:{}};
  mkdirSync(join(root,"vendor"));
  mkdirSync(join(root,"src"));
  for(const name of policy.profiles[profile].required) {
   const version=policy.versions[name] ?? "1.0.0";
   dependencies[name]=version; packages["node_modules/"+name]={version};
   if(policy.artifactPackages.includes(name)) {
    const prefix=name.startsWith("@")?name.slice(1).replace("/","-"):name;
    const filename=prefix+"-"+version+".tgz";
    const bytes=Buffer.from(name), integrity="sha512-"+createHash("sha512").update(bytes).digest("base64");
    writeFileSync(join(root,"vendor",filename),bytes);
    dependencies[name]="file:vendor/"+filename;packages["node_modules/"+name].integrity=integrity;artifacts.packages[name]={version,integrity};
   }
  }
  const canonicalArtifacts=structuredClone(artifacts);
  change?.({dependencies,devDependencies,packages,artifacts,root});
  writeFileSync(join(root,"package.json"),JSON.stringify({dependencies,devDependencies}));
  writeFileSync(join(root,"package-lock.json"),JSON.stringify({lockfileVersion:3,packages}));
  writeFileSync(join(root,"common-artifacts.json"),JSON.stringify(artifacts));
  if(canonical) writeFileSync(join(root,"canonical.json"),JSON.stringify(canonicalArtifacts));
  if(policyOverride) { const externalPolicy=structuredClone(policy);policyOverride(externalPolicy);writeFileSync(join(root,"policy.json"),JSON.stringify(externalPolicy)); }
  return spawnSync(process.execPath,[fileURLToPath(new URL("../check-dependencies.mjs",import.meta.url)),"--artifacts","common-artifacts.json","--profile",profile,"--workspace",workspace,...(canonical?["--canonical","canonical.json"]:[]),...(policyOverride?["--policy","policy.json"]:[])],{cwd:root,encoding:"utf8",env:{...process.env,...(requireCanonical?{KT_REQUIRE_CANONICAL:"1"}:{})}});
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
test("중앙 원장과 같은 bytes는 통과",()=>{const result=fixture(undefined,{canonical:true});assert.equal(result.status,0,result.stderr);});
test("앱 파일·원장·lock을 함께 바꿔도 중앙 정본 차이는 거부",()=>rejected(fixture(({root,packages,artifacts})=>{
 const bytes=Buffer.from("앱별 임의 재포장");
 const integrity="sha512-"+createHash("sha512").update(bytes).digest("base64");
 writeFileSync(join(root,"vendor/kor-travel-ui-0.2.0.tgz"),bytes);
 packages["node_modules/@kor-travel/ui"].integrity=integrity;
 artifacts.packages["@kor-travel/ui"].integrity=integrity;
},{canonical:true}),"중앙 산출물 정본과 다름"));
test("운영 선언을 개발 선언으로 덮어쓰는 중복은 거부",()=>rejected(fixture(({dependencies,devDependencies})=>{
 dependencies.react="18.3.1"; devDependencies.react=policy.versions.react;
}),"중복 선언"));
test("전이 의존성의 다른 React 설치는 거부",()=>rejected(fixture(({dependencies,packages})=>{
 dependencies.widget="1.0.0";
 packages["node_modules/widget"]={version:"1.0.0",dependencies:{react:"18.3.1"}};
 packages["node_modules/widget/node_modules/react"]={version:"18.3.1"};
}),"런타임 중복 인스턴스"));
test("동일 버전도 별도 물리 React 인스턴스면 거부",()=>rejected(fixture(({dependencies,packages})=>{
 dependencies.widget="1.0.0";
 packages["node_modules/widget"]={version:"1.0.0",dependencies:{react:policy.versions.react}};
 packages["node_modules/widget/node_modules/react"]={version:policy.versions.react};
}),"런타임 중복 인스턴스"));
test("별도 workspace와 독립 개발 도구의 React는 런타임 판정 밖",()=>{
 const result=fixture(({devDependencies,packages})=>{
  devDependencies.widget="1.0.0";
  packages["node_modules/widget"]={version:"1.0.0",dependencies:{react:"18.3.1"}};
  packages["node_modules/widget/node_modules/react"]={version:"18.3.1"};
  packages["apps/other/node_modules/react"]={version:"18.3.1"};
 });
 assert.equal(result.status,0,result.stderr);
});
test("모바일 React Native wildcard와 lock 누락은 거부",()=>rejected(fixture(({dependencies,packages})=>{
 dependencies["react-native"]="*";delete packages["node_modules/react-native"];
},{profile:"mobile"}),"lock 설치 버전"));
test("모바일에 DOM 공통 UI를 추가하면 거부",()=>rejected(fixture(({dependencies,packages,artifacts,root})=>{
 const bytes=Buffer.from("ui"),version=policy.versions["@kor-travel/ui"];
 const integrity="sha512-"+createHash("sha512").update(bytes).digest("base64");
 const filename="kor-travel-ui-"+version+".tgz";
 writeFileSync(join(root,"vendor",filename),bytes);
 dependencies["@kor-travel/ui"]="file:vendor/"+filename;
 packages["node_modules/@kor-travel/ui"]={version,integrity};
 artifacts.packages["@kor-travel/ui"]={version,integrity};
},{profile:"mobile"}),"공통 Radix 구현으로 이관 필요"));
test("개별 Radix 직접 선언은 공통 경로로 이관해야 한다",()=>rejected(fixture(({dependencies})=>dependencies["@radix-ui/react-dialog"]="1.0.0"),"개별 Radix"));
test("개별 Radix 전이 경로 직접 import도 거부",()=>rejected(fixture(({root})=>writeFileSync(join(root,"src/dialog.tsx"),"import { Root } from '@radix-ui/react-dialog';")),"공통 Radix 외 overlay 구현"));
test("내장 정책이 오래되어도 중앙 최신 정책을 대조한다",()=>rejected(fixture(undefined,{
 policyOverride:value=>value.versions.pretendard="9.0.0",
}),"!= 9.0.0"));
test("중앙 CI는 정책과 산출물의 외부 정본 입력을 요구",()=>rejected(fixture(undefined,{canonical:true,requireCanonical:true}),"--policy 최신 정본"));
test("중앙 CI의 동일 최신 정책·산출물은 통과",()=>{
 const result=fixture(undefined,{canonical:true,policyOverride:()=>{},requireCanonical:true});
 assert.equal(result.status,0,result.stderr);
});
