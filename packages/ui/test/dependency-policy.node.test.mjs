// SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
// SPDX-License-Identifier: GPL-3.0-or-later
import { test } from "node:test";
import assert from "node:assert/strict";
import { mkdtempSync, mkdirSync, writeFileSync, rmSync, renameSync, symlinkSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, relative } from "node:path";
import { fileURLToPath } from "node:url";
import { createHash } from "node:crypto";
import { spawnSync } from "node:child_process";
import policy from "../dependency-policy.json" with { type: "json" };
function fixture(change, {profile="web",workspace="",canonical=false,policyOverride,requireCanonical=false,packageDirectory=""}={}) {
 const root=mkdtempSync(join(tmpdir(),"kt-policy-"));
 try {
  const dependencies={}, devDependencies={}, packages={}, artifacts={packages:{}};
  const manifest={dependencies,devDependencies};
  mkdirSync(join(root,"vendor"));
  mkdirSync(join(root,packageDirectory,"src"),{recursive:true});
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
  change?.({dependencies,devDependencies,packages,artifacts,root,manifest});
  writeFileSync(join(root,packageDirectory,"package.json"),JSON.stringify(manifest));
  writeFileSync(join(root,"package-lock.json"),JSON.stringify({lockfileVersion:3,packages}));
  writeFileSync(join(root,"common-artifacts.json"),JSON.stringify(artifacts));
  if(canonical) writeFileSync(join(root,"canonical.json"),JSON.stringify(canonicalArtifacts));
  if(policyOverride) { const externalPolicy=structuredClone(policy);policyOverride(externalPolicy);writeFileSync(join(root,"policy.json"),JSON.stringify(externalPolicy)); }
  return spawnSync(process.execPath,[fileURLToPath(new URL("../check-dependencies.mjs",import.meta.url)),"--package",join(packageDirectory,"package.json"),"--artifacts","common-artifacts.json","--profile",profile,"--workspace",workspace,...(canonical?["--canonical","canonical.json"]:[]),...(policyOverride?["--policy","policy.json"]:[])],{cwd:root,encoding:"utf8",env:{...process.env,...(requireCanonical?{KT_REQUIRE_CANONICAL:"1"}:{})}});
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

for (const profile of ["web", "mobile"]) {
 test(profile + "의 Lightning CSS는 개발 의존성으로 허용", () => {
  const result=fixture(({dependencies,devDependencies})=>{
   devDependencies.lightningcss=dependencies.lightningcss;
   delete dependencies.lightningcss;
  },{profile,canonical:true});
  assert.equal(result.status,0,result.stderr);
 });
}
test("Lightning CSS build metadata가 다른 lock 버전은 거부",()=>rejected(fixture(({packages})=>{
 packages["node_modules/lightningcss"].version="1.33.0+nativecss.fix.2";
}),"lock 설치 버전"));
test("Lightning CSS registry 선언으로 vendor를 우회하면 거부",()=>rejected(fixture(({dependencies})=>{
 dependencies.lightningcss=policy.versions.lightningcss;
}),"공통 vendor 산출물 참조 불일치"));
test("Lightning CSS의 파일·원장·lock을 함께 바꿔도 중앙 bytes가 다르면 거부",()=>rejected(fixture(({root,packages,artifacts})=>{
 const bytes=Buffer.from("변경된 CSS compiler"),integrity="sha512-"+createHash("sha512").update(bytes).digest("base64");
 writeFileSync(join(root,"vendor/lightningcss-"+policy.versions.lightningcss+".tgz"),bytes);
 packages["node_modules/lightningcss"].integrity=integrity;
 artifacts.packages.lightningcss.integrity=integrity;
},{canonical:true,profile:"mobile"}),"중앙 산출물 정본과 다름"));
for (const changed of ["version","integrity"]) {
 test("개발 도구 아래 Lightning CSS의 다른 "+changed+"는 거부",()=>rejected(fixture(({devDependencies,packages})=>{
  devDependencies.builder="1.0.0";
  packages["node_modules/builder"]={version:"1.0.0",dependencies:{lightningcss:policy.versions.lightningcss}};
  packages["node_modules/builder/node_modules/lightningcss"]={...packages["node_modules/lightningcss"],
   [changed]:changed==="version"?"1.33.0":"sha512-변경된bytes"};
 }),"빌드 전이 버전·bytes 불일치"));
}
test("연결되지 않은 다른 workspace의 CSS는 현재 앱의 판정 밖",()=>{
 const result=fixture(({packages})=>{
  packages["apps/other/node_modules/lightningcss"]={version:"1.30.1",integrity:"다른 앱"};
 });
 assert.equal(result.status,0,result.stderr);
});
function sharedVendor({dependencies,root},prefix) {
 mkdirSync(join(root,"apps/web"),{recursive:true});
 renameSync(join(root,"vendor"),join(root,"apps/web/vendor"));
 for(const name of Object.keys(dependencies)) if(policy.artifactPackages.includes(name)) {
  const filename=dependencies[name].slice("file:vendor/".length);
  dependencies[name]="file:"+prefix+filename;
 }
}
test("root가 workspace 안의 공통 vendor 파일을 직접 참조해도 허용",()=>{
 const result=fixture(data=>sharedVendor(data,"apps/web/vendor/"),{canonical:true});
 assert.equal(result.status,0,result.stderr);
});
test("모바일의 형제 workspace vendor 상대 경로를 허용",()=>{
 const result=fixture(data=>sharedVendor(data,"../web/vendor/"),{
  profile:"mobile",workspace:"apps/mobile",packageDirectory:"apps/mobile",canonical:true});
 assert.equal(result.status,0,result.stderr);
});
test("lock 루트 밖의 vendor 참조는 거부",()=>rejected(fixture(({dependencies})=>{
 dependencies.lightningcss="file:../외부/vendor/lightningcss-"+policy.versions.lightningcss+".tgz";
}),"공통 vendor 산출물 참조 불일치"));
test("절대 vendor 경로는 같은 파일이어도 거부",()=>rejected(fixture(({dependencies,root})=>{
 dependencies.lightningcss="file:"+join(root,"vendor/lightningcss-"+policy.versions.lightningcss+".tgz");
}),"공통 vendor 산출물 참조 불일치"));
test("vendor symlink가 lock 루트를 벗어나면 거부",()=>{
 const outside=mkdtempSync(join(tmpdir(),"kt-css-outside-"));
 try {
  const result=fixture(({root})=>{
   renameSync(join(root,"vendor"),join(root,"saved-vendor"));
   symlinkSync(outside,join(root,"vendor"),"junction");
   writeFileSync(join(outside,"lightningcss-"+policy.versions.lightningcss+".tgz"),Buffer.from("lightningcss"));
  });
  rejected(result,"공통 vendor 산출물 참조 불일치");
 } finally {rmSync(outside,{recursive:true,force:true});}
});

test("루트 밖 선언이 symlink로 안으로 돌아와도 비이식 경로이므로 거부",()=>{
 const outside=mkdtempSync(join(tmpdir(),"kt-css-return-"));
 try {
  const result=fixture(({dependencies,root})=>{
   symlinkSync(root,join(outside,"return"),"junction");
   dependencies.lightningcss="file:"+relative(root,join(outside,"return/vendor/lightningcss-"+policy.versions.lightningcss+".tgz"));
  });
  rejected(result,"공통 vendor 산출물 참조 불일치");
 } finally {rmSync(outside,{recursive:true,force:true});}
});

test("옛 private 지도 mono-root 직접 설치와 root/private source import를 거부",()=>{
 for (const profile of ["web", "mobile"])
  rejected(fixture(({dependencies})=>dependencies["maplibre-vworld-react"]="1.0.0",{profile}),"공개 core/web/RN 배포물로 이관 필요");
 for (const imported of ["maplibre-vworld-react", "maplibre-vworld-react/packages/web/src/index"])
  rejected(fixture(({root})=>writeFileSync(join(root,"src/map.tsx"),"import { Map } from '"+imported+"';")),"금지 패키지 import");
 const adjacent=fixture(({root})=>writeFileSync(join(root,"src/map.tsx"),"import { Map } from 'maplibre-vworld-react-extra';"));
 assert.equal(adjacent.status,0,adjacent.stderr);
});


// 원 리뷰어의 실제 우회 구문을 같은 CLI 입력에서 거부해야 한다.
const moduleForms = [
 ["재export", path => "export { Map } from " + JSON.stringify(path) + ";"],
 ["전체 재export", path => "export * from " + JSON.stringify(path) + ";"],
 ["지연 import", path => "export const load = () => import(" + JSON.stringify(path) + ");"],
 ["문자열 템플릿 import", path => "export const load = () => import(" + String.fromCharCode(96) + path + String.fromCharCode(96) + ");"],
 ["CommonJS require", path => "export const Map = require(" + JSON.stringify(path) + ");"],
 ["문자열 템플릿 require", path => "export const Map = require(" + String.fromCharCode(96) + path + String.fromCharCode(96) + ");"],
 ["TS 외부 import", path => "import Map = require(" + JSON.stringify(path) + ");"],
 ["타입 import", path => "export type Model = import(" + JSON.stringify(path) + ").Model;"],
];
for (const [label, code] of moduleForms) {
 test("금지 private 지도 경로의 " + label + "도 거부", () => rejected(fixture(({root}) => {
  writeFileSync(join(root,"src/legacy-map.ts"),code("maplibre-vworld-react/packages/web/src/index"));
 }),"금지 패키지 import"));
 test("인접한 다른 지도 패키지의 " + label + "는 허용", () => {
  const result=fixture(({root}) => writeFileSync(join(root,"src/map.ts"),code("maplibre-vworld-react-extra/packages/web/src/index")));
  assert.equal(result.status,0,result.stderr);
 });
}
test("개별 Radix의 CommonJS require도 거부",()=>rejected(fixture(({root})=>{
 writeFileSync(join(root,"src/overlay.ts"),'const Dialog = require("@radix-ui/react-dialog");');
}),"공통 Radix 외 overlay 구현"));
test("금지 모듈을 언급한 문자열·주석은 실제 import로 오인하지 않는다",()=>{
 const result=fixture(({root})=>writeFileSync(join(root,"src/note.ts"),'// import("maplibre-vworld-react")\nexport const note = "require(legacy)";'));
 assert.equal(result.status,0,result.stderr);
});

function linkedBuildTool({manifest,devDependencies,packages}, cssEntry) {
 manifest.private=true;manifest.workspaces=["tools/*"];
 devDependencies["build-helper"]="*";
 packages["node_modules/build-helper"]={resolved:"tools/build-helper",link:true};
 packages["tools/build-helper"]={name:"build-helper",version:"1.0.0",devDependencies:{lightningcss:cssEntry.version}};
 packages["tools/build-helper/node_modules/lightningcss"]=cssEntry;
}
test("도달한 linked workspace 빌드 helper의 개발 stock CSS를 거부",()=>rejected(fixture(context=>{
 linkedBuildTool(context,{version:"1.33.0",integrity:"stock-bytes"});
}),"빌드 전이 버전·bytes 불일치 tools/build-helper/node_modules/lightningcss"));
test("linked workspace에서 버전만 같고 bytes가 다른 CSS도 거부",()=>rejected(fixture(context=>{
 linkedBuildTool(context,{...context.packages["node_modules/lightningcss"],integrity:"다른-bytes"});
}),"빌드 전이 버전·bytes 불일치 tools/build-helper/node_modules/lightningcss"));
test("linked workspace의 동일 compiler bytes는 허용",()=>{
 const result=fixture(context=>linkedBuildTool(context,{...context.packages["node_modules/lightningcss"]}));
 assert.equal(result.status,0,result.stderr);
});
test("연결되지 않은 다른 workspace의 stock CSS는 현재 앱 빌드 그래프 밖",()=>{
 const result=fixture(({packages})=>{
  packages["tools/unused"]={name:"unused",version:"1.0.0",devDependencies:{lightningcss:"1.33.0"}};
  packages["tools/unused/node_modules/lightningcss"]={version:"1.33.0",integrity:"무관한-bytes"};
 });
 assert.equal(result.status,0,result.stderr);
});
test("공개 registry 도구의 미설치 개발 의존성은 앱의 설치 그래프가 아니다",()=>{
 const result=fixture(({devDependencies,packages})=>{
  devDependencies["registry-helper"]="1.0.0";
  packages["node_modules/registry-helper"]={version:"1.0.0",devDependencies:{lightningcss:"1.33.0"}};
  packages["node_modules/registry-helper/node_modules/lightningcss"]={version:"1.33.0",integrity:"미설치-개발-bytes"};
 });
 assert.equal(result.status,0,result.stderr);
});

for (const extension of ["mjs","cjs","mts","cts"]) {
 test(extension + " 소스의 금지 private 지도 경로도 검사",()=>rejected(fixture(({root})=>{
  writeFileSync(join(root,"src/legacy-map."+extension),'export * from "maplibre-vworld-react/packages/web/src/index";');
 }),"금지 패키지 import"));
}
