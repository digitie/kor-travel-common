# 원 reviewer A — Geo43 / Concierge50 finding 수정 후 검토

- runid: `Mill-A-consumers-Geo43-Concierge50-postfix1`
- reviewer: 원 A(Mill), frontend/accessibility. 구현 비참여, read-only. 상대 raw/verdict는 열지 않았다.
- 시작 UTC `2026-11-11T18:28:33.460222+00:00`; 종료 source 관찰 `2026-11-11T18:33:27.631793+00:00`.
- 입력은 사용자 exact Git 지정과 원 finding이다. 새 7repo 전체 immutable manifest가 제공되었다고 주장하지 않는다.
- Geo before `a193fd1762ab7dd1058bf5b85ec2d7c96a1368d1` → after **`43c4a7f011427f362cf510a28a0fea564a087b7e`**.
- Concierge before `bcfc1b80b78a47319ddcf4918698f19331fb8206` → after **`50e707ba45fdf539dec0aacf13a81045de591fd4`**. 축약50e707b를 직접 Git lookup하여 full SHA를 확인했다.
- 자기 Git frontend snapshots: `/tmp/review-A-consumers-closure-geoconcierge-1/{geo-before,geo-after,concierge-before,concierge-after}`. 대형 install/repack/공유 소스 수정 없음.

**판정: 두 원 finding FIXED. Geo A-CONS-P2-03 source closure PASS / Concierge A-CONS-P2-01 focus closure PASS. 신규 P0/P1/P2/P3=0.** 최종 스타일·C11/Scope2·새 앱 통합 gate의 무조건 승인이 아니다. 기존 `review-A-consumers-final-1.md` BLOCK 원문은 보존했다.

## 1. 입력 고정 및 동작 근거 분리

Geo 공유 checkout은 시작·종료 HEAD43c4였지만 C10 도입 metadata/workflow/vendor와 문서가 dirty였다. 그 workingtree를 source 입력으로 사용하지 않았다. after43c4의 source 변경은 두 Button 모듈, 신규 public contract test와 journal/resume 총5파일이다. manifest/lock은 이 commit에서 C9 계약이다.

Concierge 공유 checkout은 관찰 시 HEAD50e707/clean. 이 단일 commit에는 CandidateTable 수정 외에 C10 Scope1 vendor/lock/metadata, 회귀 테스트의 user-event/jsdom 개발 의존성, workflow, 문서, e2e 변경이 함께 들어 있다. **이번 finding closure 범위는 실제 CandidateTable source와 그 keyboard regression에 한정한다.** 전체 C10 이관·새 e2e 수정·release 원장까지 승인한 것으로 확대하지 않는다. owner focus receipt도 `OWNER_FIXED_A_RECHECK_PENDING`이라고 구분되어 있었고, 그 상태를 아래 직접 실행으로 확인했다.

네 private snapshot의 기존 source files를 최종 Git과 다시 비교했다. Geo before289/after290, Concierge before175/after176 파일에서 차이0. before에는 after의 동일 test bytes만 추가했다. actual vendor 설치를 하지 않고 canonical C9 UI/tokens를 자기 module 폴더에 풀어 사용했다. 4개 copy 모두 package regular files UI94/tokens25 byte 일치.

- C9 UI archive SHA256 `8f63ca4f88da6e5d6637c0d98bcf7d86822376d592bf1a7ffe42f7df3451521d`.
- C9 tokens archive SHA256 `b16ca6c1843af26b255c3f5889d2e798600719e394112838dbbbb0b709406705`.
- 다른 기존 모듈은 읽기 참조했다. unit의 실제 Radix 경유 Scope는 **1.3.1+kortravel.fix.1**, stock으로 부르지 않는다. `module-provenance.json`에 실제 resolve 경로·React19.3.1/Vitest5.1.0/Node22.22.2를 남겼다.
- 별도 browser 원 공격은 **보존된 stock Scope1.3.1 dist/index.mjs를 esbuild alias로 명시**했다. 따라서 root의 이후 Scope 교체에 기대어 옛 baseline을 추정하지 않았다. source/function closure에 C9 공용 API가 충분한지를 직접 확인했다. 최종 C10/C11 설치 수용은 별도다.

## 2. Geo A-CONS-P2-03 — FIXED

원 finding은 Geo가 독자 Button/CVA 전체 구현을 유지하여 공통 Button을 실제 소비하지 않던 문제였다. 단순 package 의존성 추가만으로 닫지 않았다.

- `kor-travel-geo-ui/components/ui/button.tsx:5`: client 경계에서 **`export { Button } from "@kor-travel/ui/button"`** 직접 위임. 지역 Slot/native button 렌더와 별도 runtime 로직 제거.
- `kor-travel-geo-ui/components/ui/button-variants.ts:3`: 순수 common subpath에서 import하고 같은 함수 re-export. 로컬 CVA 전체 제거. client Button 파일을 통해 서버 helper를 가져오지 않는다. `ButtonVariantProps`는 공통 함수에서 유도한다.
- Node에서 실제 순수 TS helper를 import하여 common C9 함수와 **sameFunction=true, sameOutput=true**를 확인했다. destructive-solid/icon-xs 조합도 같은 함수 출력이다. 이는 완전한 Next RSC production build 실행을 뜻하지 않는다.

부모가 추가한 5개 test의 SHA256은 `f8f7160637788edc8dc780b210df0cc4949bdba15799009c2c6279bdf5f33bee`. before/after에 같은 bytes를 사용해 원 reviewer가 직접 실행했다.

| 직접 실행 | before a193 | after43c4 |
|---|---|---|
| public contract5 | **3 FAIL / 2 PASS**, exit1 | **5 PASS**, exit0 |
| 전체 단위 | 이번 미반복 | **294 PASS / 53 files**, exit0 |
| tsc --noEmit --incremental false | 이번 미반복 | exit0 |

실제 실패3건은 loading의 aria/활성화 차단, disabledReason title, 기본 button의 불필요한 form submit이다. after는 loading 상태 focus 보존·click 차단, 명시적 submit만 제출, asChild link 의미/variant/size, React19 ref와 Dialog trigger/Escape/focus 복귀를 통과했다. user-event 모듈 부재로 0 test가 실행됐던 초기 owner driver 로그는 red 증거로 사용하지 않았다. fireEvent를 쓰는 수정된 동일 5개 test를 직접 판별했다.

default type이 native 암묵 submit에서 common의 button으로 바뀌므로 호출부를 별도 AST로 확인했다. 자기 probe는 **tests/vendor/node_modules를 제외한 production source 기준 Button 관련 import21, 명시적 submit Button6**을 찾았다. 실제 form 안 Button은 submit6 또는 명시적 type=button이며 암묵 submit Button은 없었다. owner의 전체23 imports/7 submit 집계와 스캔 범위가 다르다. `geo-callsites.json`에 파일·행·form별 목록을 남겼다. 새 source 전체 타입 검사와294 단위도 함께 통과했다. 이로써 단순 코드 중복 삭제뿐 아니라 공개 Button 동작 채택을 확인했다.

**A-CONS-P2-03: FIXED.** 단, 새 공통 Button 스타일의 실제 앱 browser 시각 검증과 final Scope2 설치/CI/배포는 이번 미실행이다. 부모의 lint/Doctor0/CodeGraph 로그는 참고 인계이며 본인이 CodeGraph를 새로 생성·sync하거나 앱 lint/Doctor를 재실행한 결과로 쓰지 않았다.

## 3. Concierge A-CONS-P2-01 — FIXED

원 finding은 매 render마다 만들어지는 column.header/cell 함수가 TanStack flexRender의 component type으로 해석되어, checkbox 선택 때 DOM을 remount하고 focus를 BODY로 잃는 문제였다.

- `frontend/src/components/review/CandidateTable.tsx:60`의 `CandidateSelectionHeader`는 module scope의 안정된 component identity다. 최신 checked/disabled/label/onToggle을 column meta에서 읽는다.
- body는 새 `columns.cell` component wrapper를 만들지 않고 `VirtualTable`의 **renderCell callback**으로 CandidateCell node를 반환한다. C9 common API에서 지원되는 직접 callback이다. 후보/출처/상태/액션 index 매핑은 기존5열 순서와 같다. fresh props/callback은 그대로 전달되어 stale selection closure로 고치지 않았다.
- 선택 제한, actionable/pending 판정, 후보 id identity, source 값, row/action handlers를 이번 수정을 이유로 바꾸지 않았다.

동일 test bytes SHA256 `b1a174c8cb94947c8514e5bc7ce7636eb7f62b4957a5a839d167e1ba0b3ab4ea`로 직접 실행: before **DOM identity2 FAIL**, after **2 PASS**. after 전체 **396 PASS / 30 files**, 실제 product tsc exit0.

독립 actual Chromium158.0.8127.18에서 **원 A browser 공격을 확장 재사용**했다. 같은 최소 production bundle 안에서 원 443 baseline, 문제 bcfc, 수정50e707의 실제 CandidateTable source를 각각 mount했다. 나머지 harness·C9 UI·명시 stock Scope는 같게 유지했다.

| actual browser | 동작 | DOM / focus |
|---|---|---|
| 원443 baseline | 헤더/행 Space 선택2 | 같은 node, 연결 유지, BUTTON focus 보존2 |
| 문제bcfc | 헤더/행 Space 선택2 | **node 교체, old disconnected, BODY focus2** |
| 수정50e707 | 헤더 선택→해제, 행 선택→해제4 | **같은 node, 연결 유지, BUTTON focus 보존4** |

checked 값은 각각 true/false로 실제 바뀌었다. pageerror0. 원결함을 동일 browser harness에서 다시 재현한 뒤 수정의4개 전환을 확인했으므로 owner의 Chromium 로그만으로 닫지 않았다. `concierge-browser-results.json/.log`, `concierge-browser-probe.cjs`에 소스 bundle/entry/common/stock 해시와 관찰을 남겼다. 이 fixture는 CSS 없는 좁은 실제 DOM/keyboard 검증이며 전체 Next 앱·테이블 layout·virtual scroll·n150 live E2E·새 Scope2의 검증은 아니다.

첫 type-check는 browser 대조용으로 자기 fixture src에 추가한 옛443 `.baseline.tsx`의 구형 indeterminate prop 때문에 실패했다. 그 파일은 대상50e707 source가 아니다. 자기 browser 입력을 source 밖 `/tmp/.../own-browser-inputs`로 이동한 후 **제품 source와 원 test 그대로** type-check하여 exit0을 확인했다. 최초 driver 진단은 `concierge-after-tsc.log`, 올바른 재실행은 `concierge-after-tsc-clean.log`에 모두 보존했다. source를 수정하거나 test assertion을 약화하지 않았다.

**A-CONS-P2-01: FIXED.** final C11/Scope2의 actual install·full Next build·최종 앱 browser와 정확 CI는 후속 immutable input에서 별도로 확인해야 한다.

## 4. Commands / raw evidence / limits

```text
# exact source blobs from git archive <SHA> <frontend-prefix>; vendor 제외, private source only
# before에 after의 동일 regression test blob 추가
node node_modules/vitest/vitest.mjs run tests/unit/ui-button-common.test.tsx --maxWorkers=2
node node_modules/vitest/vitest.mjs run src/components/review/CandidateTable.test.ts --maxWorkers=2
# 두 after 각 frontend root
node node_modules/vitest/vitest.mjs run --maxWorkers=2
node node_modules/typescript/bin/tsc --noEmit --incremental false
node review-A-consumers-geoconcierge-postfix-1-evidence/geo-callsite-probe.cjs
node review-A-consumers-geoconcierge-postfix-1-evidence/module-provenance.cjs
node review-A-consumers-geoconcierge-postfix-1-evidence/concierge-browser-probe.cjs
# browser 입력은 실행 뒤 own-browser-inputs에 옮겼으므로 재실행시 entry와 두 대조 source를 자기 fixture에 복원할 것
```

증거 디렉터리 `review-A-consumers-geoconcierge-postfix-1-evidence/`: observations-start/end.json, geo/concierge-diff.patch, 네 focused.log, 두 after-full.log, tsc logs, geo-pure-helper.log, geo-callsites.json, module-provenance.json, canonical-c9-module-bytes.json, concierge-browser-results.json, browser runner/log.

Owner 증거는 Geo validation/geo-button-common/* 및 proof.json, Concierge exact50의 docs/reports/candidate-table-focus-20261112.json와 그에 명시된 `.git/candidate-*` 로그를 읽었다. 이들은 구현자 인계이지 상대 reviewer 보고서가 아니다. 본인의 direct 결과와 분리했다. 기존 raw/manifests/tarballs는 수정하지 않았다.

원 consumer1 전체 BLOCK 기록은 유지한다. 이번으로 Geo03/Concierge01의 원 finding을 닫지만, Map02는 새 bounded input 검토 전이고 Pinvi04/최종Scope2/전체 consumer final acceptance도 이번 판정 밖이다. 앱 PR merge·이미지 export·배포 PASS로 확대하지 않는다.
