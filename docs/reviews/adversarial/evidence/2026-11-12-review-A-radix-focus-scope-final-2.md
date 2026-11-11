# 원 reviewer A — Radix FocusScope2 최종 독립 재검토

- runid: `Mill-A-Scope2-175`, 원 A(Mill), frontend/accessibility. 구현 비참여, 읽기 전용. 상대 raw/verdict를 열지 않았다.
- 시작 UTC: 2026-11-11T18:45:08.539418+00:00; 종료 관찰 UTC: 2026-11-11T18:59:17.241074+00:00.
- immutable input `review-manifest-radix-focus-scope-2.json`, 실제 SHA256 **d4df7d2898a8a36f70821314afb9fd254d03d94187269246f55894ecf475ca01** 일치.
- source **1752a539c8d5ae57961a0fa2702d2573d48fefe7**, 이전 formal706e27aaf87bda2df7bbb9da60cc01cebc9ff064. 자기 detached worktree `/tmp/review-A-scope-final2/source`, 시작/종료 exact175/clean. 실행용 자체 Vitest config는 evidence에 보존하고 source 밖으로 정리했다.
- 전달 supplement **01e8181f6fc73fac6aeb140cac96dcdb30f8aaa6**은 source175 판정과 분리하여 아래3파일만 비교했다. 공유 checkout은 처음부터01이므로 moving workingtree를175로 취급하지 않았다.
- actual packet **1.3.1+kortravel.fix.2**, **33511 bytes**, SHA256 **1ca04870692565c243130d99c3dba91f3ac853ab2ec9538fc7b658b17fb7b49a**.

**Verdict: PASS(이 원본 source·고정 pack·bounded delivery 범위). A-SCOPE-P2-01 FIXED. 신규 P0/P1/P2/P3=0.** 최종 Common C11 통합·각 소비자·배포는 별도다. 기존 Scope1 CONDITIONAL 원문·f97/fix1·C10을 수정하지 않았다.

## 1. 원 finding의 실제 수정

원 finding 위치는 `packages/react/focus-scope/src/focus-scope.tsx`의 tabbable candidate 판정이다. `.disabled` property는 disabled fieldset에서 상속된 disabled 상태를 보지 못했다. 마지막 candidate가 비활성 input으로 선택되어 focus()가 실패하고, 이미 preventDefault된 Shift+Tab의 포커스가 container/first에 남았다.

새 `:352` 부근 `isDisabledFormControl`은 native `element.matches(':disabled')`를 먼저 확인하고, HTML button/input/select/textarea에 대해서만 모든 disabled fieldset 조상을 추가 확인한다. 각 조상의 **첫 직접 legend** 안에 속한 control의 예외를 개별적으로 적용한다. 가장 가까운 fieldset만 처리하지 않으며, disabled를 상속하지 않는 링크는 배제하지 않는다. `getTabbableCandidates`의 `:385` 부근에서 이 함수를 사용한다. 캐시된 disabled 값이 아니라 현재 DOM을 조회하므로 enable/disable 및 legend 순서 변경에 대응한다.

기존 수정 경계는 구분한다. registry stock1.3.1에는 없던 IME guard는 upstream Git eb3에 이미 있었고, 로컬 source706의 초기 container reverse-entry 수정도 유지한다. 이번175의 추가 runtime 변경은 fieldset disabled semantics다. 이를 모두 이번에 새로 만든 수정으로 설명하지 않는다. API·types·공개 dependencies는 변하지 않았다.

## 2. 동일 source test red/green — 본인 직접 실행

source175의 test bytes SHA256 `84591bcb66e557479e52222db55c6560da7e326ea9fa13bd2b4cbf968f4763c0`를 사용했다. 이전 source706을 자기 red fixture에 복원하고 동일한 최종38 test bytes를 적용했다.

| 원 A 직접 실행 | 결과 |
|---|---|
| source706 + 최종 동일 test | **6 FAIL / 32 PASS / 38 실행**, exit1 |
| source175 + 동일 test | **38 PASS / 0 FAIL**, exit0 |

실패6건은 inherited disabled의 container/first 역방향2, 첫 legend 예외1, enable/disable 전환2, 중첩 outer-disabled/inner-legend1이다. missing import·0 test·환경 실패를 red로 사용하지 않았다. 로컬 기존 Vitest4.1.7/Node22.22.2와 source-specific modules를 읽기 참조했으며 retry0/maxWorkers1이다. `source-before-unit.log`, `source-after-unit.log`, 두 config를 보존했다.

## 3. 최종 실제 pack browser — 본인 직접 실행

고정 fix1의 실제 ESM dist와 최종33511-byte fix2의 실제 ESM dist를 동일 React19 최소 harness에 각각 bundle했다. commonRoot의 현재 Scope를 baseline으로 쓰지 않았다. Playwright는 기존 modules를 읽기 참조했고 실제 Chromium **158.0.8127.18**을 사용했다. loopback만 허용하며 자기 server/browser를 회수했다.

**actual fix2 packed browser20/20 PASS**, pageerror0. 같은 harness의 fix1은11PASS/9FAIL로 관찰되었고, 특히 원 A의 container/first 두 실패가 각각 scope/first에 포커스를 남기는 것을 다시 재현했다. 기대한 red 두 건이 없어지면 runner 자체가 실패하도록 했다.

- 기존9: loop/trapped4조합, forward entry, disabled/hidden edges, empty 양방향, 명시 first의 loop, nested scope pause/restore 및 close 후 focus 복귀.
- 추가11: disabled fieldset container/first2, 첫 legend active·explicit disabled·두 번째 legend의 상속 disabled, enable/disable/re-enable2, outer disabled의 inner first legend 차단 및 outer enable 뒤 활성화, 링크 허용, IME container Tab 비취소 뒤 정상 역방향, 두 조상 모두의 첫 legend 예외, legend DOM 순서 변경 후 예외 재계산,229/alt/ctrl/meta guard.

disabled assertion은 **native `:disabled`와 실제 focus() 거부**로 확인했다. inherited input의 own.disabled=false도 확인하여 단순 explicit disabled 테스트로 대체하지 않았다. 중첩 legend에서 Playwright nearest-fieldset matcher의 잘못된 판정에 의존하지 않았다. first legend control은 native enabled 및 실제 focus 성공을 확인했다. 이는 source175가 강화한 native assertion과도 일치한다.

증거: `packed-browser-results.json`, `packed-browser.log`, `packed-browser-probe.cjs`, `entry.jsx`. 이것은 좁은 실제 pack/DOM/keyboard fixture다. 실제 Pinvi/common 전체 앱 browser나 n150 live 배포 검증은 아니다. source17 CI와 own packed20을 합산하여 하나의 suite로 표시하지 않는다.

## 4. packet·API·출처·라이선스

압축파일 SHA256/SHA512/크기,15 regular files, package identity를 직접 확인했다. 전체 SRI:

`sha512-v3XweXrUSZ/QfrMVvYmsAkVNDnvcN21QKbSrViXYf0OQf5Ue9xSgqQIukgGjsYMEBQ5qxQW8fnOC9t1Y0ENPXw==`

- PROVENANCE.sourceCommit=175, source4개 Git blob/hash와 모두 일치. index/source/test/tsconfig가 원장과 actual tar entry에서 같다.
- six dist SHA256 모두 manifest/provenance와 일치, ESM/CJS 두 source map의 source content는 actual175 TSX와 같다.
- pnpm-lock Git bytes SHA256 `30ae793af509fcf3bfb96172f9c47ccff45486b7fa9dfe399ebfd486d3fb9d64` 일치. Node24.22.2/pnpm11.5.0/esbuild0.25.12/tsup8.5.1/TypeScript5.9.3 producer metadata는 직접 CI 출력과도 같다.
- MIT LICENSE는 repo 원문 전체와 같다. `.d.ts/.d.mts`, public dependencies/peers/optional peer flags/exports/main/module/types는 stock 및 fix1과 동일하다. package에 workspace dependency·dev dependency·producer scripts를 소비자 실행 의존성으로 넣지 않았다.
- bare package ESM/CJS 해석을 **Node22.22.2와 실제 Node24.22.2 각각**에서 실행했다. 네 실행 모두 정확5 runtime exports: FocusScope, FocusScopeBranchProvider, Root, useFocusScopeBranch, useFocusScopeBranchRegistry. fresh npm install을 했다는 뜻은 아니다. own package link와 기존 dependency modules를 사용했다.
- old f97 fix1 SHA256과 원 Scope1 raw SHA256도 재확인했다. 각각 `f97c1dd4851fd1dc7b75bfbe9ce7e2d68bbd32e225b9ff52954c683fd4c7081d`, `82aba7ea2674023df0272d745160441dfeeefc430fda975652ae6cb09bc629b8` 그대로다.

`source-pack-audit.json`, `public-exports.json`에 실제 상세 hashes/API를 보존했다. 전체 native/npm dependency 설치를 새로 하지 않았다. browser behavior는 ESM 경로를 실행했으며 CJS는 공개 export load와 source map/compiled source를 확인했다. 전체 CJS browser20을 별도로 실행했다고 주장하지 않는다.

## 5. create/verify/pack recipe와 delivery01

source706/cc 이후의 source175 scripts 전체를 읽었다.

- create는 pinned Node24, clean tracked/untracked 입력, workspace builder, 원 package identity, 공개 dependency 버전 정규화, toolVersions, source/dist/lock hashes를 기록한다. frozen fix2 ledger가 있으면 생성 자체를 거부하고, 기존 output tarball도 덮어쓰지 않는다. 이 검토에서 후보를 다시 만들지 않았다.
- verify는 고정 SRI·크기·name/version·sourceCommit·LICENSE, archived source4와 지정 Git commit, rebuilt six dist와 provenance hashes를 확인한다. producer의 원 toolchain metadata와 현재 packet 연결은 이번 수동 Git/lock/API 비교 및 실제 CI와 함께 확인했다. standalone verifier가 모든 build environment를 새로 설치·검증하는 도구라고 과장하지 않는다.
- pack은 frozen fix2만 rebuild/verify 뒤 copy한다. 다른 bytes가 있는 동일 이름 destination을 거부한다. create/reissue와 frozen delivery를 분리한다.

source175는 pre-freeze producer 커밋이므로 fix2 frozen ledger가 그 Git tree에 없는 것은 예상된 경계다. 현재01은 **workflow, fix2 JSON, fix2 tgz 세 파일만** 추가/변경한다. workflow는 create 호출을 frozen pack/verify-copy로 전환한다. runtime/source/test/builder/scripts는175와 완전히 같고,01의 ledger는 immutable manifest artifact와 객체 전체 일치, tgz는 실제33511 bytes와 완전 일치한다. `delivery-01e-proof.json`.

자기 verification fixture에서 실제 frozen bytes와 Git175를 사용했다. positive1, six dist 각각 변조6, ledger integrity/identity2, LICENSE1, Node24 create-frozen 거부1의 **11 기대 결과 일치**. archive를 재포장하지 않았고 frozen bytes도 불변이다. 로컬 verifier positive의 dist 입력은 packet에서 복사한 것으로 **local fresh rebuild 증거가 아니다**. 원 reviewer local full producer rebuild는 기존 builder modules 부재/설치 제약으로 NOT_RUN이며, 아래 직접 관찰한 exact CI가 fresh build와 exact byte 정합 근거다. 초기 fixture의 root→tmp hardlink는 filesystem이 달라 EXDEV가 나서 자기 fixture copy로 바꿨다. source/product 실패가 아니다.

## 6. 원격 exact CI 직접 관찰

GitHub 도구로 commit runs/jobs/job logs를 본인이 읽었다. source175와 delivery01을 구분했다.

- [source175 run43078944952 / regression130726100529](https://github.com/digitie/radix-primitives/actions/runs/43078944952/job/130726100529): SUCCESS. exact175 checkout, frozen-lock install·build/lint/type/format, source38, **source Storybook browser17 PASS(24.5초)**, Node24 producer. 생성 output **33511 bytes/1ca048.../SRIv3X...**가 최종 input과 같다. 과거5806의33510-byte packet을 이 증거로 쓰지 않았다.
- source175 Build43078944892, SSR43078945016, Chromatic43078944986도 직접 run-list에서 SUCCESS.
- [delivery01 run43080256258 / regression130730641316](https://github.com/digitie/radix-primitives/actions/runs/43080256258/job/130730641316): SUCCESS. source38/browser17 PASS(21.9초), 실제 frozen verify는 `verified:true`, `normalization:none; six dist files exact`, copy는 `copiedFrozenArtifact:true`. sourceCommit175, 같은33511/SRI를 출력했다.
- delivery01 Build43080256232, SSR43080255852, Chromatic43080255899도 SUCCESS.

`scope175-ci.log`, `delivery01-ci.log`, `ci-observation.json`. source17은 실제 packed17로 바꾸어 부르지 않는다. 본인의 actual packed20이 별도로 있다. manifest 생성 당시 pending 기록은 역사 그대로 보존하고 최신 직접 관찰을 이 새 원문에 추가했다.

## 7. commands·disposition·limits

```text
git worktree add --detach /tmp/review-A-scope-final2/source 1752a539c8d5ae57961a0fa2702d2573d48fefe7
git diff 706e27aaf87bda2df7bbb9da60cc01cebc9ff064..1752a539 -- packages/react/focus-scope scripts .github/workflows/focus-scope-fix.yml
# same final38 test bytes against own706 red fixture and175 source, retry0
node node_modules/vitest/vitest.mjs run --config vitest.review.config.mts
node E/packed-browser-probe.cjs
node /tmp/review-A-scope-final2/npm-export-check/check.mjs
node /tmp/review-A-scope-final2/npm-export-check/check.cjs
# repeat exports with existing pinned Node24 binary; no install
node scripts/verify-focus-scope-fix.mjs
# own verifier fixture; GIT_DIR/GIT_WORK_TREE point to immutable175 for git-show source checks
# exact Git175→01 three-file diff + JSON/artifact byte comparison
# GitHub fetch_commit_workflow_runs / fetch_workflow_run_jobs / fetch_workflow_job_logs
```

E=`review-A-radix-focus-scope-final-2-evidence/`. source runtime/unit/delivery patch, 원 manifest, 시작/종료 관찰, source/packet/provenance, browser, verifier, CI raw를 별도 보존했다.

**A-SCOPE-P2-01 FIXED / Scope2 PASS.** 신규 finding 없음. Common7의 실제Scope2 lock·C11 packed65는 별도 원문이며, Pinvi 등 최종 앱 채택·export·deploy는 후속 immutable input의 별도 gate다. Scope1 원문을 PASS로 덮어쓰지 않는다.
