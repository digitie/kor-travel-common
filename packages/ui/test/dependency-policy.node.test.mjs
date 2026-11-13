// SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
// SPDX-License-Identifier: GPL-3.0-or-later
import { test } from "node:test";
import assert from "node:assert/strict";
import { mkdtempSync, mkdirSync, writeFileSync, readFileSync, rmSync, renameSync, symlinkSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, relative } from "node:path";
import { fileURLToPath } from "node:url";
import { createHash } from "node:crypto";
import { spawnSync } from "node:child_process";
import policy from "../dependency-policy.json" with { type: "json" };
function fixture(change, {profile="web",workspace="",canonical=false,policyOverride,requireCanonical=false,packageDirectory="",checker="../check-dependencies.mjs"}={}) {
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
  change?.({dependencies,devDependencies,packages,artifacts,canonicalArtifacts,root,manifest});
  writeFileSync(join(root,packageDirectory,"package.json"),JSON.stringify(manifest));
  writeFileSync(join(root,"package-lock.json"),JSON.stringify({lockfileVersion:3,packages}));
  writeFileSync(join(root,"common-artifacts.json"),JSON.stringify(artifacts));
  if(canonical) writeFileSync(join(root,"canonical.json"),JSON.stringify(canonicalArtifacts));
  if(policyOverride) { const externalPolicy=structuredClone(policy);policyOverride(externalPolicy);writeFileSync(join(root,"policy.json"),JSON.stringify(externalPolicy)); }
  return spawnSync(process.execPath,[fileURLToPath(new URL(checker,import.meta.url)),"--package",join(packageDirectory,"package.json"),"--artifacts","common-artifacts.json","--profile",profile,"--workspace",workspace,...(canonical?["--canonical","canonical.json"]:[]),...(policyOverride?["--policy","policy.json"]:[])],{cwd:root,encoding:"utf8",env:{...process.env,...(requireCanonical?{KT_REQUIRE_CANONICAL:"1"}:{})}});
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

// 미래 정책의 정확한 단일 엔진만 fixture에 주입한다. 실제 버전·원장은 변경하지 않는다.
const patchedEngine = "@radix-ui/react-focus-scope", patchedVersion = "1.1.0+focus.fixture";
function addArtifact(context, name, version=policy.versions[name]) {
 const {dependencies,packages,artifacts,canonicalArtifacts,root}=context;
 const prefix=name.startsWith("@")?name.slice(1).replace("/","-"):name;
 const filename=prefix+"-"+version+".tgz", bytes=Buffer.from("canonical fixture "+name);
 const integrity="sha512-"+createHash("sha512").update(bytes).digest("base64");
 writeFileSync(join(root,"vendor",filename),bytes);
 dependencies[name]="file:vendor/"+filename;
 packages["node_modules/"+name]={version,integrity};
 artifacts.packages[name]={version,integrity};
 canonicalArtifacts.packages[name]={version,integrity};
}
function patchedFixture(change, policyChange=()=>{}) {
 return fixture(context=>{
  addArtifact(context,patchedEngine,patchedVersion);
  context.packages["node_modules/@kor-travel/ui"].dependencies={[patchedEngine]:patchedVersion};
  change?.(context);
 },{canonical:true,policyOverride:value=>{
  value.patchedRadixPackages=[patchedEngine];
  value.artifactPackages.push(patchedEngine);
  value.versions[patchedEngine]=patchedVersion;
  policyChange(value);
 }});
}
test("패치 엔진의 정확한 직접 vendor·중앙 bytes는 허용",()=>{
 const result=patchedFixture();assert.equal(result.status,0,result.stderr);
});
for (const missing of ["list","artifact","version"]) {
 test("패치 엔진의 "+missing+" 정책 등록이 없으면 개별 Radix 선언을 거부",()=>{
  const result=patchedFixture(undefined,value=>{
   if(missing==="list")delete value.patchedRadixPackages;
   if(missing==="artifact")value.artifactPackages=value.artifactPackages.filter(name=>name!==patchedEngine);
   if(missing==="version")delete value.versions[patchedEngine];
  });
  rejected(result,"개별 Radix");
 });
}
test("패치 엔진 목록은 다른 개별 primitive 직접 선언을 허용하지 않는다",()=>{
 rejected(patchedFixture(({dependencies})=>dependencies["@radix-ui/react-dialog"]="1.0.0"),"개별 Radix");
});
for (const [label,code] of [["정적 import",path=>"import { Root } from "+JSON.stringify(path)+";"],...moduleForms]) {
 test("패치 엔진을 승인해도 앱 소스의 "+label+"는 계속 거부",()=>{
  rejected(patchedFixture(({root})=>writeFileSync(join(root,"src/engine.ts"),code(patchedEngine))),"공통 Radix 외 overlay 구현");
 });
}
for (const changed of ["metadata-version","metadata-missing","canonical-version","canonical-bytes","file-bytes","lock-version","lock-bytes"]) {
 test("패치 엔진의 "+changed+" 불일치는 거부",()=>{
  const result=patchedFixture(({root,packages,artifacts,canonicalArtifacts,dependencies})=>{
   if(changed==="metadata-version")artifacts.packages[patchedEngine].version="0.0.0";
   if(changed==="metadata-missing")delete artifacts.packages[patchedEngine];
   if(changed==="canonical-version")canonicalArtifacts.packages[patchedEngine].version="0.0.0";
   if(changed==="canonical-bytes")canonicalArtifacts.packages[patchedEngine].integrity="sha512-other";
   if(changed==="file-bytes")writeFileSync(join(root,dependencies[patchedEngine].slice(5)),"다른 bytes");
   if(changed==="lock-version")packages["node_modules/"+patchedEngine].version="1.1.0";
   if(changed==="lock-bytes")packages["node_modules/"+patchedEngine].integrity="sha512-stock";
  });
  assert.equal(result.status,1,result.stderr);
 });
}
test("패치 엔진은 원장과 중앙 version을 같이 바꿔도 정책 버전이 다르면 거부",()=>{
 rejected(patchedFixture(({artifacts,canonicalArtifacts})=>{
  artifacts.packages[patchedEngine].version="0.0.0";
  canonicalArtifacts.packages[patchedEngine].version="0.0.0";
 }),"원장 버전");
});
test("패치 엔진의 전이 설치가 있어도 직접 고정이 없으면 거부",()=>{
 rejected(patchedFixture(({dependencies})=>delete dependencies[patchedEngine]),"직접 의존성");
});

function reachedArtifact(context,name,edge="runtime") {
 const {dependencies,devDependencies,packages,manifest}=context;
 if(edge==="linked-dev") {
  manifest.private=true;manifest.workspaces=["tools/*"];
  devDependencies["artifact-helper"]="*";
  packages["node_modules/artifact-helper"]={resolved:"tools/artifact-helper",link:true};
  packages["tools/artifact-helper"]={name:"artifact-helper",version:"1.0.0",devDependencies:{[name]:"*"}};
  const key="tools/artifact-helper/node_modules/"+name;
  packages[key]={...packages["node_modules/"+name]};return key;
 }
 (edge==="runtime"?dependencies:devDependencies)["artifact-helper"]="1.0.0";
 packages["node_modules/artifact-helper"]={version:"1.0.0",dependencies:{"artifact-bridge":"1.0.0"}};
 packages["node_modules/artifact-helper/node_modules/artifact-bridge"]={version:"1.0.0",dependencies:{[name]:"*"}};
 const key="node_modules/artifact-helper/node_modules/artifact-bridge/node_modules/"+name;
 packages[key]={...packages["node_modules/"+name]};return key;
}
const managedNames=[patchedEngine,"vworld-map-web","@kor-travel/ui","@kor-travel/tokens"];
function managedFixture(name,change) {
 if(name===patchedEngine)return patchedFixture(change);
 return fixture(context=>{
  if(!context.dependencies[name])addArtifact(context,name);
  change(context);
 },{canonical:true});
}
for (const name of managedNames) {
 for(const edge of ["runtime","build","linked-dev"]) {
  test("관리 산출물 "+name+" "+edge+"의 동일 version·bytes는 허용",()=>{
   const result=managedFixture(name,context=>reachedArtifact(context,name,edge));
   assert.equal(result.status,0,result.stderr);
  });
  for(const changed of ["version","integrity"]) {
   test("관리 산출물 "+name+" "+edge+"의 전이 "+changed+" 불일치를 거부",()=>{
    const result=managedFixture(name,context=>{
     const key=reachedArtifact(context,name,edge);
     context.packages[key][changed]=changed==="version"?"0.0.0":"sha512-stock-bytes";
    });
    rejected(result,"빌드 전이 버전·bytes 불일치");
   });
  }
 }
}
for (const edge of ["runtime","build","linked-dev"]) {
 test("관리 산출물 "+edge+" 전이 설치의 직접 선언 누락을 거부",()=>{
  rejected(managedFixture("vworld-map-web",context=>{
   reachedArtifact(context,"vworld-map-web",edge);
   delete context.dependencies["vworld-map-web"];
  }),"직접 의존성");
 });
 test("관리 산출물 "+edge+"의 미해결 전이 항목도 직접 고정 누락을 거부",()=>{
  rejected(managedFixture("vworld-map-web",context=>{
   const key=reachedArtifact(context,"vworld-map-web",edge);
   delete context.dependencies["vworld-map-web"];
   delete context.packages[key];delete context.packages["node_modules/vworld-map-web"];
  }),"직접 의존성");
 });
}
for(const name of managedNames) {
 test("관리 산출물 "+name+"의 무관 workspace·registry 개발 전이는 제외",()=>{
  const result=managedFixture(name,({devDependencies,packages})=>{
   devDependencies["registry-artifact-helper"]="1.0.0";
   packages["node_modules/registry-artifact-helper"]={version:"1.0.0",devDependencies:{[name]:"*"}};
   packages["node_modules/registry-artifact-helper/node_modules/"+name]={version:"0.0.0",integrity:"무관"};
   packages["tools/unused"]={name:"unused",version:"1.0.0",devDependencies:{[name]:"*"}};
   packages["tools/unused/node_modules/"+name]={version:"0.0.0",integrity:"무관"};
  });
  assert.equal(result.status,0,result.stderr);
 });
}
test("관리 산출물 검사는 도달한 alias의 실제 package identity도 확인",()=>{
 rejected(managedFixture("vworld-map-web",({dependencies,packages})=>{
  dependencies.widget="1.0.0";
  packages["node_modules/widget"]={version:"1.0.0",dependencies:{"map-alias":"*"}};
  packages["node_modules/widget/node_modules/map-alias"]={name:"vworld-map-web",version:policy.versions["vworld-map-web"],integrity:"sha512-stock"};
 }),"빌드 전이 버전·bytes 불일치");
});
// 통합 진입점도 앱 자체 primitive 구현을 허용하는 우회 경로가 아니다.
for (const modulePath of ["radix-ui", "radix-ui/dialog"]) {
 for (const [label, code] of [["정적 import", path => "import { Dialog } from " + JSON.stringify(path) + "; export const Overlay = () => <Dialog.Root />;"], ...moduleForms]) {
  test("통합 Radix " + modulePath + "의 " + label + "도 공통 UI 경로를 요구", () => {
   rejected(fixture(({root, dependencies, packages}) => {
    dependencies["radix-ui"] = policy.versions["radix-ui"];
    packages["node_modules/radix-ui"] = {version: policy.versions["radix-ui"]};
    writeFileSync(join(root,"src/overlay.tsx"), code(modulePath));
   }), "공통 Radix 외 overlay 구현");
  });
 }
}
test("공통 wrapper와 내부 Radix 전이 구현은 유지", () => {
 const result = fixture(({root, packages}) => {
  packages["node_modules/@kor-travel/ui"].dependencies = {"radix-ui": policy.versions["radix-ui"]};
  packages["node_modules/radix-ui"] = {version: policy.versions["radix-ui"], dependencies: {"@radix-ui/react-dialog": "1.0.0"}};
  packages["node_modules/@radix-ui/react-dialog"] = {version: "1.0.0"};
  mkdirSync(join(root,"node_modules/@kor-travel/ui"), {recursive:true});
  writeFileSync(join(root,"node_modules/@kor-travel/ui/index.tsx"), 'import { Dialog } from "radix-ui"; import { Root } from "@radix-ui/react-dialog";');
  writeFileSync(join(root,"src/dialog.tsx"), 'import { Dialog, DialogContent } from "@kor-travel/ui"; export const Overlay = () => <Dialog><DialogContent /></Dialog>;');
 });
 assert.equal(result.status,0,result.stderr);
});
for (const modulePath of ["radix-ui-extra", "@example/radix-ui"]) {
 test("통합 Radix 인접 이름 " + modulePath + "는 실제 금지 경로로 오인하지 않는다", () => {
  const result = fixture(({root}) => writeFileSync(join(root,"src/adjacent.ts"), "export * from " + JSON.stringify(modulePath) + ";"));
  assert.equal(result.status,0,result.stderr);
 });
}
test("통합 Radix 이름을 설명한 주석과 문자열은 import가 아니다", () => {
 const result = fixture(({root}) => writeFileSync(join(root,"src/note.ts"), '// import { Dialog } from "radix-ui";\nexport const note = "radix-ui/dialog";'));
 assert.equal(result.status,0,result.stderr);
});
test("통합 Radix 버전 선언의 기존 web 계약은 변경하지 않는다", () => {
 const result = fixture(({dependencies,packages}) => {
  dependencies["radix-ui"] = policy.versions["radix-ui"];
  packages["node_modules/radix-ui"] = {version:policy.versions["radix-ui"]};
 });
 assert.equal(result.status,0,result.stderr);
});
test("통합 Radix를 사용하지 않는 native tokens 경로는 유지", () => {
 const result = fixture(({root}) => writeFileSync(join(root,"src/native.tsx"), 'import { View } from "react-native"; import { tokens } from "@kor-travel/tokens"; export const Screen = () => <View />;'), {profile:"mobile"});
 assert.equal(result.status,0,result.stderr);
});
test("통합 Radix의 기존 native 금지 선언은 유지", () => {
 rejected(fixture(({root,dependencies,packages}) => {
  dependencies["radix-ui"] = policy.versions["radix-ui"];
  packages["node_modules/radix-ui"] = {version:policy.versions["radix-ui"]};
  writeFileSync(join(root,"src/native.ts"), 'import { Dialog } from "radix-ui";');
 }, {profile:"mobile"}), "공통 정책의 금지 패키지 import: radix-ui");
});
// 실제 tools CLI에 기존 정책·canonical을 전달해 npm 요청 이름과 실제 identity를 함께 검사한다.
const centralAliasOptions = {checker:"../../../tools/check_frontend_dependencies.mjs", canonical:true, policyOverride:()=>{}, requireCanonical:true};
const aliasCases = [
 ["web root", "overlay-bridge", "radix-ui", "web", "", "normal"],
 ["web scoped", "@example/overlay-bridge", "radix-ui", "web", "", "normal"],
 ["web subpath", "overlay-bridge", "radix-ui", "web", "/dialog", "normal"],
 ["scoped subpath", "@example/overlay-bridge", "radix-ui", "web", "/dialog", "normal"],
 ["mobile root", "overlay-bridge", "radix-ui", "mobile", "", "normal"],
 ["mobile scoped subpath", "@example/overlay-bridge", "radix-ui", "mobile", "/dialog", "normal"],
 ["individual Radix", "overlay-bridge", "@radix-ui/react-dialog", "web", "", "normal"],
 ["individual scoped subpath", "@example/overlay-bridge", "@radix-ui/react-dialog", "web", "/subpath", "normal"],
 ["Base UI", "overlay-bridge", "@base-ui/react", "web", "", "normal"],
 ["Floating UI", "overlay-bridge", "@floating-ui/react", "web", "", "normal"],
 ["manifest identity", "overlay-bridge", "radix-ui", "web", "", "missing-name"],
 ["manifest/lock disagreement", "overlay-bridge", "radix-ui", "web", "", "different-name"],
 ["undeclared transitive identity", "overlay-bridge", "radix-ui", "web", "", "transitive"],
 ["mobile declaration only", "overlay-bridge", "radix-ui", "mobile", "", "no-import"],
 ["nearest workspace identity", "@example/overlay-bridge", "radix-ui", "mobile", "/dialog", "workspace"],
];
for (const [label, alias, target, profile, subpath, kind] of aliasCases) {
 test("패키지 alias의 " + label + " 우회도 실제 tools CLI에서 거부", () => {
  const version = policy.versions[target] ?? "1.0.0";
  const result = fixture(({root, dependencies, packages}) => {
   dependencies[alias] = "npm:" + target + "@" + version;
   packages["node_modules/" + alias] = {name:target, version};
   if (kind === "missing-name") delete packages["node_modules/" + alias].name;
   if (kind === "different-name") packages["node_modules/" + alias].name = "unrelated-engine";
   if (kind === "transitive") {
    delete dependencies[alias];
    dependencies["fixture-helper"] = "1.0.0";
    packages["node_modules/fixture-helper"] = {version:"1.0.0", dependencies:{[alias]:"npm:" + target + "@" + version}};
   }
   if (kind === "workspace") {
    dependencies[alias] = "npm:unrelated-engine@1.0.0";
    packages["node_modules/" + alias] = {name:"unrelated-engine", version:"1.0.0"};
    packages["apps/mobile/node_modules/" + alias] = {name:target, version};
   }
   if (kind !== "no-import") writeFileSync(join(root,"src/alias.tsx"), "import { Dialog } from " + JSON.stringify(alias + subpath) + "; export const Overlay = () => <Dialog.Root />;");
  }, {...centralAliasOptions, profile, ...(kind === "workspace" ? {workspace:"apps/mobile"} : {})});
  rejected(result, "Radix");
 });
}
for (const [label, target] of [["무관한 alias", "unrelated-engine"], ["인접한 이름", "radix-ui-extra"], ["다른 scope", "@example/radix-ui"]]) {
 test("패키지 alias의 " + label + " 정상 경로는 유지", () => {
  const result = fixture(({root, dependencies, packages}) => {
   dependencies["overlay-bridge"] = "npm:" + target + "@1.0.0";
   packages["node_modules/overlay-bridge"] = {name:target, version:"1.0.0"};
   writeFileSync(join(root,"src/alias.ts"), 'export * from "overlay-bridge/subpath";');
  }, centralAliasOptions);
  assert.equal(result.status,0,result.stderr);
 });
}
test("패키지 alias의 nearer workspace 정상 identity는 무관한 root 설치보다 우선", () => {
 const result = fixture(({root,dependencies,packages}) => {
  dependencies["overlay-bridge"] = "npm:unrelated-engine@1.0.0";
  packages["node_modules/overlay-bridge"] = {name:"radix-ui", version:policy.versions["radix-ui"]};
  packages["apps/mobile/node_modules/overlay-bridge"] = {name:"unrelated-engine", version:"1.0.0"};
  writeFileSync(join(root,"src/alias.ts"), 'export * from "overlay-bridge/subpath";');
 }, {...centralAliasOptions,profile:"mobile",workspace:"apps/mobile"});
 assert.equal(result.status,0,result.stderr);
});
for (const kind of ["wrong-both", "wrong-selector", "range-selector", "wrong-lock", "missing-identity"]) {
 test("패키지 alias의 버전 " + kind + "는 기존 exact 정책으로 거부", () => {
  const result = fixture(({dependencies,packages}) => {
   const wanted = policy.versions["radix-ui"];
   dependencies["overlay-bridge"] = "npm:radix-ui@" + (kind === "wrong-both" || kind === "wrong-selector" ? "1.8.0" : kind === "range-selector" ? "^" + wanted : wanted);
   packages["node_modules/overlay-bridge"] = {name:"radix-ui", version:kind === "wrong-both" || kind === "wrong-lock" ? "1.8.0" : wanted};
   if (kind === "missing-identity") delete packages["node_modules/overlay-bridge"].name;
  }, centralAliasOptions);
  rejected(result,"별칭");
 });
}
test("패키지 alias의 정확한 registry 선언만 있고 직접 구현은 없으면 허용", () => {
 const result = fixture(({dependencies,packages}) => {
  dependencies["overlay-bridge"] = "npm:radix-ui@" + policy.versions["radix-ui"];
  packages["node_modules/overlay-bridge"] = {name:"radix-ui", version:policy.versions["radix-ui"]};
 },centralAliasOptions);
 assert.equal(result.status,0,result.stderr);
});
test("패키지 alias의 common UI vendor·canonical bytes는 wrapper로 허용", () => {
 const result = fixture(({root,dependencies,packages}) => {
  dependencies["ui-bridge"] = dependencies["@kor-travel/ui"];
  packages["node_modules/ui-bridge"] = {...packages["node_modules/@kor-travel/ui"],name:"@kor-travel/ui"};
  writeFileSync(join(root,"src/wrapper.tsx"), 'import { Dialog } from "ui-bridge"; export const Overlay = () => <Dialog />;');
 },centralAliasOptions);
 assert.equal(result.status,0,result.stderr);
});
for (const [label,code] of moduleForms) {
 test("패키지 alias의 scoped subpath " + label + "도 실제 identity를 검사", () => {
  const result = fixture(({root,dependencies,packages}) => {
   dependencies["@example/overlay-bridge"] = "npm:radix-ui@" + policy.versions["radix-ui"];
   packages["node_modules/@example/overlay-bridge"] = {name:"radix-ui",version:policy.versions["radix-ui"]};
   writeFileSync(join(root,"src/alias.ts"), code("@example/overlay-bridge/dialog"));
  },centralAliasOptions);
  rejected(result,"공통 Radix 외 overlay 구현");
 });
}
test("관리 산출물 source·UI·tokens 배포 checker bytes는 동일",()=>{
 const source=readFileSync(new URL("../../../tools/check_frontend_dependencies.mjs",import.meta.url));
 assert.deepEqual(readFileSync(new URL("../check-dependencies.mjs",import.meta.url)),source);
 assert.deepEqual(readFileSync(new URL("../../tokens/check-dependencies.mjs",import.meta.url)),source);
});
