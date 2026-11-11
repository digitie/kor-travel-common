# SCOPE2 — 原 reviewer B / Epicurus 独립 source·pack·producer 후속 원문

- Run ID `Epicurus-B-scope2-20261111T184622Z`. 시작 UTC `2026-11-11T18:46:22Z`, 종료 UTC `2026-11-11T18:52:48.874490+00:00`. Reviewer B, packaging/platform/security/license/release 전문, 구현 비참여.
- 불변 입력 `review-manifest-radix-focus-scope-2.json` SHA256 `d4df7d2898a8a36f70821314afb9fd254d03d94187269246f55894ecf475ca01`를 시작/종료 직접 확인했다.
- Preferred source **`1752a539c8d5ae57961a0fa2702d2573d48fefe7`**; upstream `eb3a2b7091293e27df8f9ba906632d8daa3d81a3`; 원 formal source `706e27aaf87bda2df7bbb9da60cc01cebc9ff064`. `706→175` 13개 파일의 전체 diff를 검토했다.
- 별도 bounded delivery **`01e8181f6fc73fac6aeb140cac96dcdb30f8aaa6`**는 사용자 지정 frozen delivery commit으로만 대조했다. preferred source를 moving HEAD로 대체하지 않았다.
- 본인 격리 fixture `/tmp/review-b-scope2-20261111T184622Z`와 immutable `git show`로 조립한 source snapshot을 사용했다. source hash inventory를 보존했다. 기존 modules는 dependency 읽기 참조만 했다. 기존 source/manifest/원문/pack 수정, install·재pack·타인 cache 정리 없음. peer raw·verdict 파일을 열지 않았다.

## Verdict

**PASS — preferred source175 + fix.2 pack + producer·검증/복사 연결의 독립 B 검토. 신규 P0/P1/P2/P3 finding 0건.** 원 Scope1의 미완료 regression CI 조건은 새 불변 입력에서 실제 성공으로 충족됐다. Scope1 원문 CONDITIONAL과 당시 취소/skip 기록은 그대로 보존한다.

범위는 이 라이브러리와 지정 frozen delivery delta다. delivery Chromatic은 최종 관찰 시 IN_PROGRESS이므로 모든 workflow가 끝났다고 주장하지 않는다. COMMON7/C11·Pinvi 등 최종 앱 채택/배포 승인은 별도다.

## 실제 artifact·API·license

- 고유 버전 `@radix-ui/react-focus-scope@1.3.1+kortravel.fix.2`, **33511 bytes**.
- SHA256 `1ca04870692565c243130d99c3dba91f3ac853ab2ec9538fc7b658b17fb7b49a`.
- SRI `sha512-v3XweXrUSZ/QfrMVvYmsAkVNDnvcN21QKbSrViXYf0OQf5Ue9xSgqQIukgGjsYMEBQ5qxQW8fnOC9t1Y0ENPXw==`.
- 실제 tar 15개 regular member를 검사했다. 중복명·절대경로·상위 경로·link·특수 member가 없고 source4/dist6 및 package/README/LICENSE/PROVENANCE/BUILDING이 존재한다. 모든 source/dist digest가 manifest·내부 provenance와 일치한다.
- source4 bytes가 Git175와 같고 workspace lock SHA256은 `30ae793af509fcf3bfb96172f9c47ccff45486b7fa9dfe399ebfd486d3fb9d64`로 Git175와 같다. sourcemap의 preferred source 내용도 동봉 src와 일치한다.
- 전체 MIT LICENSE는 원 upstream Git 및 preferred source LICENSE와 byte-identical이다. 권리자·허가문 삭제/확대 없음.
- public dependencies3, peers/optional type peers, exports, sideEffects, 두 선언 파일은 fix.1과 동일하다. published manifest에는 workspace source/main이나 devDependencies/scripts/publishConfig가 남지 않고 dist export target을 사용한다.
- 직접 Node **v22.22.2**에서 canonical package require/ESM import를 실행했다. 양쪽 모두 정확한 full version과 5개 export `FocusScope`, `FocusScopeBranchProvider`, `Root`, `useFocusScopeBranch`, `useFocusScopeBranchRegistry`를 확인했다. CJS는 실제 `dist/index.js`, ESM은 package import 조건의 `dist/index.mjs`를 소비한다. `exports-node22.json`.
- 부모의 actual npm install receipt는 별도 handed-off evidence로 full version/SRI/15files/5exports가 일치함을 읽었다. 본인 probe는 추출한 actual package exports의 동작 확인이며 본인 새 npm clean install이라고 표시하지 않는다.

## 원본 버그와 실제 사용 회귀 — 본인 red/green

175의 source unit 38개에서 **FocusScope import와 test-utils import 경로만** 바꿔 실제 tgz exports를 소비하게 했다. assertion/시나리오/성공 조건은 유지하고 retry0로 실행했다.

| 실제 engine | CommonJS | ESM |
|---|---|---|
| 원본 frozen fix.1 f97 | **32 PASS / 6 FAIL** | **32 PASS / 6 FAIL** |
| 새 frozen fix.2 1ca048 | **38 PASS / 0 FAIL** | **38 PASS / 0 FAIL** |

실패 6건은 inherited disabled reverse entry(container/first), 첫 legend 예외, 동적 enabled 전환(container/first), outer disabled ancestor 아래 inner legend다. 따라서 stock에 상속된 fieldset 문제를 새 소스·compiled package가 실제로 고치는 것을 B도 직접 재현했다. 상대 report를 근거로 closure하지 않았다.

source의 새 `isDisabledFormControl`은 native `:disabled`를 우선 확인하고 HTML button/input/select/textarea에 한해 모든 disabled fieldset ancestor와 각 첫 legend 예외를 확인한다. disabled fieldset 안의 링크를 일괄 제외하지 않는다. 기존 initial container reverse 조건·IME/keyCode229·modified Tab·empty scope·중첩 pause/ref/focus restoration 검사는 그대로 통과한다.

기존 stock registry→upstream Git의 IME 변화, 원706의 initial container 변화, 이번 inherited fieldset 변화를 구분했다. fix.1→fix.2 compiled CJS/ESM diff는 source comment 경로 변경 외에는 helper 추가와 disabled 후보 판정 교체다. 추가 public export/의존성/선언 runtime 변화는 없었다. 실제 diff를 동봉했다.

## Producer·verification·고정 bytes 경계

706의 최초 packaging script 이후 create/verify/frozen-copy 역할 분리와 fail-closed 변경을 포함해 검토했다.

- creator는 Node24.22.2, pnpm11.5.0, 표준 workspace builder context와 esbuild0.25.12/tsup8.5.1/TypeScript5.9.3을 사용한다. clean committed source, 고유 fix.2 identity, source commit/hash, workspace lock hash, dist6 hash를 기록한다. pnpm manifest normalizer의 build metadata 제거를 피하면서 실제 publish manifest를 deterministic tar+gzip으로 보존한다.
- 동일 output tarball 덮어쓰기를 거부하고, frozen fix.2 ledger가 있는 delivery tree에서 creator를 다시 사용하지 못하게 한다. normal delivery는 기존 frozen packet을 복사한다. 과거 preferred producer commit에서의 재현과 현재 delivery에서의 frozen bytes 전달을 구분했다.
- verifier는 SRI·크기·package/provenance identity·전체 LICENSE·source Git bytes/hash·표준 builder dist6 bytes/hash를 검사한다. frozen copy는 missing ledger/tarball을 거부하고, 관련 tracked source의 dirty diff를 거부하며, 재빌드·verify 후 같은 bytes를 복사한다. 기존 destination이 다른 bytes면 덮어쓰지 않는다.
- 본인 verifier control: 알려진 reference dist 양성1 및 **거부 control6**(tgz 손상, current dist 변조, LICENSE 불일치, 잘못된 producer source receipt, missing frozen ledger, 잘못된 producer Node) 모두 기대 결과다. reference dist를 공급한 verifier control이며 본인 재빌드라는 뜻이 아니다. 실제 pinned 재빌드의 bytes 연결은 아래 exact CI 로그에서 확인했다. 본인은 재pack하지 않았다.
- 원 fix.1 SHA256 `f97c1dd4851fd1dc7b75bfbe9ce7e2d68bbd32e225b9ff52954c683fd4c7081d`가 원 artifacts와 Git175의 historical archive에서 모두 유지된다. fix.2로 덮어쓰지 않았다. Scope1 원문 SHA256 `f46ba7e6b5334694e73e2b98a4ed0a3e1d7736673e40cfb375130b48d3b80691`도 동일하다.

## Exact CI·bounded delivery — API/로그 직접 관찰

[preferred175 regression run43078944952/job130726100529](https://github.com/digitie/radix-primitives/actions/runs/43078944952/job/130726100529)은 **SUCCESS**다. 정확한175 checkout, frozen install/build/lint/type/format, **unit38 PASS, source Storybook browser17 PASS(24.5s)**, creator 실행을 직접 관찰했다. creator 출력의 sourceCommit175·dist6·33511·전체 SRI/SHA가 이번 고정 artifact와 같다. 최종175의 Build43078944892/SSR43078945016/Chromatic43078944986도 SUCCESS다.

Storybook browser는 library source 경로를 검증한다. 이를 실제 npm tarball을 설치한 앱 browser17이라고 부르지 않는다. packed 동작은 위 본인 CJS/ESM38과 Node22 exports 검증으로 별도 연결했다. nested fieldset browser assertion은 기존 nearest-fieldset matcher를 native `matches(':disabled')`와 실제 거부된 focus 확인으로 강화했으며 테스트 skip/약화로 통과시킨 것이 아니다.

`175→01e8181` diff는 다음 **3파일만**이다: `.github/workflows/focus-scope-fix.yml`, frozen fix.2 ledger, frozen fix.2 tgz. ledger는 formal manifest artifact object와 같고 Git delivery tgz는 이번 실제 artifact와 byte-identical이다. source·builder·create/verify/pack scripts·lock은 모두 그대로다. CI의 producer 호출을 frozen verify/copy 호출로 바꾼 metadata/delivery 분류는 **타당하다**.

[delivery01e regression run43080256258/job130730641316](https://github.com/digitie/radix-primitives/actions/runs/43080256258/job/130730641316)도 **SUCCESS**를 직접 관찰했다. 정확한01e checkout, unit38/source browser17 PASS(21.9s), standard workspace 재빌드 후 `normalization:none; six dist files exact`, `verified:true`, `copiedFrozenArtifact:true`와 동일 SRI/SHA/source175가 로그에 있다. delivery Build43080256232/SSR43080255852 SUCCESS. **Chromatic43080255899는 최종 관찰 시 IN_PROGRESS**, PASS로 확대하지 않는다.

## Closure·한계·인계

B 원 Scope1의 source/pack 판단과 당시 CI conditional 원문은 불변 보존한다. **새 입력175에서 해당 regression/pack CI 미완료 조건은 CLOSED**이며 새로운 fieldset 동작 및 고유 fix.2 bytes도 B가 독립 확인했다. 이번 B 신규 finding 없음.

본인이 로컬 browser를 새로 실행하거나 새 producer install/rebuild/repack하지는 않았다. 실제 source browser·pinned creator·delivery 재빌드는 exact 원격 로그 직접 관찰이며, actual npm receipt는 handed-off 관찰, packed unit/exports·archive/provenance·negative controls는 본인 실행이다. 이 세 종류를 혼동하지 않는다.

C11/COMMON7은 다음 별도 불변 입력이며 이번 검토에서 common 정책·consumer lock 채택이나 앱 export/배포를 승인하지 않는다. B 소비자 Map/Pinvi finding은 후속 앱 delta의 본인 재검증까지 유지한다. 기존 COMMON6 BLOCK과 Doctor571 FIXED 원문도 그대로 보존한다.

증거 `review-B-radix-focus-scope-final-2-evidence/`: source snapshot/hash, source/delivery patch, audit 및 recipe probe script/results, 4개 packed unit log와 import 변경 test, Node exports, 원격 API/log 발췌, 명령/실행 metadata, 기존 본인 raw hash를 보존했다. `SHA256SUMS.json`은 증거별 digest다. 본인 임시 fixture만 정리하고 타인의 cache/checkout을 변경하지 않는다.
