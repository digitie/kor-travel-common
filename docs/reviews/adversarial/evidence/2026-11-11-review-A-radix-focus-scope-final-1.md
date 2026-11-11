# 원 reviewer A(Mill) — FocusScope source/실제 pack1 독립 감사

- Run ID: Mill-A-radix-focus-scope-final1.
- 시작 UTC: 2026-11-11T18:01:06.344699+00:00. 종료 UTC: 2026-11-11T18:10:18.644778+00:00.
- 같은 원 reviewer A, frontend/accessibility. 구현하지 않았고 peer raw/verdict를 읽지 않았다.
- **Verdict: CONDITIONAL.** 목표 plain-container 역진입 수정은 실제 packed9 동작에서 확인했다. 단, disabled fieldset의 기존 upstream 잔여 P2 한 건을 직접 재현하여 OPEN으로 기록한다.
- 신규 독립 발견: P0=0/P1=0/P2=1/P3=0. 이 P2는 stock에도 있는 문제이며 이번 조건 변경이 만든 회귀라고 하지 않는다.
- consumer1 원문과 Pinvi BLOCK을 수정하지 않았다. common6/C10 및 Pinvi 실제 채택은 별도 입력/gate다.

root=/home/digitie/dev/common-unification-20261111.
evidence=root/review-A-radix-focus-scope-final-1-evidence/.

## 1. Immutable source·실측 pack

manifest=root/review-manifest-radix-focus-scope-1.json.
SHA256=4a7457463f69ad3e68ea9bba804401c546375ce8f69b1b389fe04d9df97c37ce, 전달값과 일치.

- Git base eb3a2b7091293e27df8f9ba906632d8daa3d81a3.
- 검토 head706e27aaf87bda2df7bbb9da60cc01cebc9ff064.
- 실제 tar31214bytes, SHA256 f97c1dd4851fd1dc7b75bfbe9ce7e2d68bbd32e225b9ff52954c683fd4c7081d, manifest SHA512도 계산 일치.
- 이름 @radix-ui/react-focus-scope, full version1.3.1+kortravel.fix.1.
- 실제15파일을 개인 fixed 디렉터리에 풀어 검사했다. stock은 보존 registry1.3.1의 원9파일을 개인 stock으로 복사했다. receipt를 stock runtime 파일로 합산하지 않았다.
- 공유 repo는 이미 cc66292dd12f11bf083173f00d8dab9e9c4541df/clean이었다. 검토는 별도706 detached worktree에서 했고 종료에도 clean이다. 이후 CI/pack verifier/e2e metadata 변경은 별도 input2 대상이며 이번 source로 섞지 않았다.

동봉4 source/tsconfig SHA가 manifest와 같고706 Git blob과 byte 동일했다. LICENSE는 repo/stock MIT 전문과 동일, README 및 두 declaration도 stock과 byte 동일했다. package provenance가706을 가리키는 점도 확인했다. currentCC를 producer로 둔 임의 새 pack이라고 표현하지 않는다.

## 2. 조건 수정과 stock/Git 차이

수정은 기존 Shift+Tab edge 조건에 focusedElement===container를 추가한다. loop/trapped 모두 false면 기존 조기 return, paused scope return, empty container 처리 및 stack/복원·branch API는 그대로다. loop가 있으면 last로 이동하고 trapped-only면 기본 이동만 막아 container를 유지한다.

**registry1.3.1과 Git baseeb3의 source를 동일시하지 않았다.** 보존 stock source map와 Git base를 직접 비교하니 eb3에는 IME composition/keyCode229 조기 return이 추가돼 있다. 이 코드는 local706 patch 이전부터 Git base에 존재한다.

실제 compiled ESM/CJS를 stock과 diff한 결과는 source 경로 주석, 그 IME guard 및 이번 container edge 조건이다. fixed sourcemap의 sourcesContent는706 TSX와 정확히 같았다. stock sourcemap은 eb3와 byte 같지 않으며 위 IME 차이를 stock-registry-vs-Git-base.patch에 보존했다.

이 추가 IME 동작도 실제 packed probe에서 확인했다: 조합 중 Tab을 fixed는 취소하지 않고 first를 유지하며 stock은 last로 이동했다. 이를 local patch가 새로 만든 코드라고 하지 않는다.

## 3. 실제 API·license·package 경계

public deps3개의 이름/정확 버전, peer ranges/meta, exports object는 stock과 동일하다. workspace:*나 private @repo dependency가 배포 runtime에 남지 않았다. devDependencies/scripts/publishConfig는 소비 pack에서 제거됐으며 packageManager pnpm11.5.0은 재현 build 메타데이터다.

두 .d.ts/.d.mts는 stock과 byte 동일하다. private public-name resolution fixture에서 ESM/CJS를 실제 로드하여 다음5 runtime export가 동일함을 직접 확인했다:

~~~text
FocusScope
FocusScopeBranchProvider
Root
useFocusScopeBranch
useFocusScopeBranchRegistry
~~~

npm 새 install은 하지 않았고 이미 고정된 pack을 private fixture의 package 경로로 연결했다. 부모의 실제 npm install/lock/SRI 성공 인계와 이 직접 Node export resolution을 구분한다.

MIT 전문·원 소스·PROVENANCE·BUILDING이 pack에 있다. BUILDING은 전체 fork checkout/Node24/pnpm11에서 재현하는 절차이며, 동봉 source 일부만으로 독립 monorepo build가 가능하다고 하지 않는다. source recipe는 dist 복사·publishConfig 반영·정확 public deps·source hash/provenance·정렬 tar를 만드는 것을 확인했다. 본인이 전체 build/pack을 재생성한 것은 아니다.

## 4. 직접 실행

| 직접 검증 | 결과 | raw |
|---|---|---|
| source706 FocusScope 단위 | 26 PASS / retry0 | source-unit.log |
| 실제 stock registry packed browser 기본9 | 5 PASS/4 FAIL | packed-browser-probe.log / packed-browser-results.json |
| 실제 f97 fixed packed browser 기본9 | **9 PASS/0 FAIL** | 동일 |
| packed IME 추가 공격 | fixed PASS/stock 기존 동작 확인 | 동일 extra |
| disabled fieldset 추가 공격2 | stock/fixed 각각2 FAIL, 아래 finding | 동일 extra |
| 실제 ESM/CJS public export | 양쪽5개 동일 | public-api-audit.json |
| source/hash/license/declarations/compiled diff | 위 결과 일치 | source-pack-audit.json, index.js/index.mjs-delta.patch |

브라우저는 Chromium158.0.8127.18, pageerror0이었다. loop/trapped4조합, forward entry, 직접 disabled/hidden edge, empty, explicit-first 정상 loop, nested pause·restore를 동일 fixture에서 확인했다. 기존 Source browser9를 packed browser9로 읽어 바꾼 것이 아니라 **직접 f97 dist로 별도 실행**했다.

로컬 Node v22.22.2/Vitest4.1.7을 사용했고 Root source의 기존 모듈만 읽기 참조했다. producer Node24 전체 build는 NOT_RUN이다. 추가18초 install이나 공유 RootScope를 stock으로 돌려 쓰지 않았다. stock/fixed entry는 private 두 파일 경로로 명시했다. 자기 browser/server는 종료했다.

source26의22PASS/4FAIL-before는 부모 인계이고 이 실행에서 before unit26을 다시 돌리지 않았다. 대신 실제 stock packed9의4실패를 직접 대조했다. 최종 Pinvi 앱 회귀·common packed65는 본9 fixture와 별도다.

## 5. A-SCOPE-P2-01 — disabled fieldset의 자식을 tabbable edge로 고름

**OPEN / P2 / 기존 upstream 잔여 문제, source706와 실제 f97에 존재.**

위치: packages/react/focus-scope/src/focus-scope.tsx:356〜370(getTabbableCandidates), :339〜343(getTabbableEdges), :236〜239(역진입 focus).

최소 HTML/React 구성:

~~~tsx
<FocusScope loop trapped>
  <button>First</button>
  <button>Last</button>
  <fieldset disabled>
    <input />
  </fieldset>
</FocusScope>
~~~

container를 초기 focus하고 Shift+Tab하면 마지막 실제 tabbable인 Last로 가야 한다. 실제 fixed는 container에 남는다. First에서 Shift+Tab으로 정상 edge-loop를 해도 First에 남는다. 같은 두 구성의 stock도 실패하므로 이번 조건 변경의 신규 회귀라고 주장하지 않는다.

원인: fieldset에 의해 비활성화된 input은 자신의 disabled property는 false지만 실제 browser에서는 disabled이므로 focus할 수 없다. 후보 수집이 node.disabled만 검사하여 이 input을 last로 고른다. focus()는 실패하고 이미 preventDefault된 Tab은 진행되지 않는다. direct button.disabled를 검사하는 기존9는 이 구성을 포함하지 않는다.

영향: fieldset disabled를 쓰는 폼에서 컨테이너 역진입 및 first→last 순환 계약이 충족되지 않는다. 실제 데이터 노출이나 background focus 누출을 입증한 것은 아니다. 필드셋이 없는 plain-container 원 요청은 fixed9에서 정상이다.

권고: 실제 disabled 상속을 반영하는 후보 판정(예: :disabled)을 적용하되 disabled fieldset의 first legend 예외도 보존한다. 같은 sibling 배치의 container/first 역진입·정상 legend/control·fieldset 활성화 전환을 browser와 단위로 검증한다. 새 변경은 새 immutable source/version/pack으로 기록하고 이 f97을 재발행하지 않는다.

증거는 packed-browser-probe.cjs의 extra fieldset2 및 결과JSON이다. 이 원문은 자동 연기를 승인하지 않으며 수정 재확인 또는 정식 owner/task/gate/기한 disposition이 필요하다.

## 6. CI·후속 경계·보존

exact706에 대한 GitHub workflow-runs를 직접 조회했을 때 Chromatic43070580263와 SSR43070580180은 SUCCESS, Build43070580508와 Patched FocusScope43070580672는 CANCELLED였다. 모든 source CI가 PASS했다고 하지 않는다. 이후CC의 검증/recipe/e2e metadata는 별도 input2에서 확인해야 한다.

common C10 generic policy/schema/helper/7pack, 실제 Pinvi/C10 adoption, whole-app nested overlay·모든 소비자 test 및 deploy는 이 source/pack 원문이 승인하지 않는다. consumer1 원본과 source4/Native/gzip 원문도 변경하지 않았다.

**목표 f97 basic packed9 PASS / public API·source 대응 확인 / 기존 disabled-fieldset P2 OPEN / 최종 CONDITIONAL.**
