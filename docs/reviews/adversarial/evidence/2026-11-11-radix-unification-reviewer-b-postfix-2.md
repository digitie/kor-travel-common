# 원 리뷰어 B(Epicurus) — immutable manifest 2 수정 후 독립 재검토

- 실행 ID: `Epicurus-B-postfix-2-20261111T140648Z`
- 시작 UTC: `2026-11-11T14:06:48Z`
- 종료 UTC: `2026-11-11T14:17:58+00:00`
- 역할: 최초 B와 동일한 packaging/dependency/CI/license 독립 리뷰어. 구현 참여 없음.
- 최종 verdict: **CONDITIONAL**
- 기존 finding closure: **11건 모두 FIXED** (P0 1 / P1 7 / P2 3)
- 신규 finding: **P3 1건 OPEN**. 신규 P0/P1/P2 발견 없음.
- 별도 미완료 gate: 이 보고서의 마지막 원격 조회에서 exact common head의 `packages` job이 `in_progress`였음. 실행 중을 PASS/FAIL로 집계하지 않는다.

`CONDITIONAL`의 조건은 신규 P3 고지 문구 정리 또는 규정에 맞는 명시적 DEFERRED, 그리고 정확한 common head의 남은 필수 packages CI 성공 확인이다. 이 판정은 본 common/VWorld 소스·산출물 범위에 한정하며 소비자 최종 채택·배포나 별도 NativeCSS fork 승인을 뜻하지 않는다.

## 불변 입력과 독립성

| 항목 | 실제 관찰값 |
|---|---|
| manifest | `/home/digitie/dev/common-unification-20261111/review-manifest-common-2.json` |
| manifest SHA256 | `a78334ceb396293ee377aa29403554fc158c2e256b1159b26607acad0bdfda90` — 요청과 일치 |
| common observed SHA | `8dad71a50f9f8f12f0e3ba1c913a93e404dabfed` |
| common 이전 리뷰 SHA | `789e6d2e179a055b3cd793fb886083543244089c` |
| upstream observed SHA | `9a7a348b02d61969b394c681b024d5851eef836b` |
| upstream 이전 리뷰 SHA | `7402214b9d4829f1f73f80ac29f68d22e2809254` |
| artifact 후보 | `artifacts/integration-7-review`, `CANDIDATE_NOT_RELEASED` |
| B 최초 report SHA256 | `520356751417c84ecb0f8d078891556e3533c2b93a9d09184b6260567867ce87` — 종료 시 재확인, 원본 무수정 |

격리는 `/tmp/review-b2-common-20261111-140648`, `/tmp/review-b2-map-20261111-140648`의 detached worktree로 수행했다. 시작·종료 HEAD가 위 SHA이고 `git status --porcelain=v1`이 모두 빈 문자열임을 확인했다. 모든 source 읽기는 불변 git 객체 또는 이 worktree에서 수행했다. parent의 작업 중 source·향후 정책 변경을 기준선에 섞지 않았다. source 파일은 편집하지 않았다.

원 리뷰어 A의 보고서·finding·통합 report는 열람하지 않았다. reviews 디렉터리는 파일명 변경 목록과 필수 README 색인의 기존 상태 행만 보였으며 상대 원문·상세 결과는 읽지 않았다. 최초 B의 11개 ID와 이 B의 재현·검증만 closure 판단에 사용했다.

새 npm 설치는 **0회**다. 빌드/시험 도구만 기존 common node_modules를 임시 symlink로 연결해 사용했으며 소스는 새 detached worktree의 파일이었다. TypeScript5.9.3, Vitest5.1.0, Tailwind4.3.5, React/DOM19.3.1, Testing Library16.3.3, tw-animate-css1.4.0, Playwright1.65.0을 확인했다. 종료 전에 symlink를 해제했고 외부 node_modules·캐시는 삭제하지 않았다. 검사 증거는 `review-B-common-postfix-2-evidence/`에 보존했다.

## 직접 실행한 명령과 결과

다음 명령은 reviewer 소유 detached worktree에서 실행했다. 전체 대규모 install·새 native/browser 번들 빌드는 실행하지 않았다.

```bash
sha256sum review-manifest-common-2.json review-B-common.md
git rev-parse <manifest-head>^{commit}
git diff <previous-review-head> <manifest-head> -- <관련 경로>
git worktree add --detach /tmp/review-b2-common-20261111-140648 8dad71a50f9f8f12f0e3ba1c913a93e404dabfed
git worktree add --detach /tmp/review-b2-map-20261111-140648 9a7a348b02d61969b394c681b024d5851eef836b
node tools/sync_frontend_policy.mjs --check
node --test packages/ui/test/dependency-policy.node.test.mjs
node packages/tokens/scripts/build.mjs
node node_modules/typescript/bin/tsc -p packages/ui/tsconfig.json
node packages/ui/scripts/check-package.mjs
(cd packages/ui && node ../../node_modules/vitest/vitest.mjs run)
(cd packages/tokens && node --test test/*.test.mjs)
python3 -m unittest discover -s tests -p test_check_versions.py
python3 tools/check_versions.py --self-check
python3 tools/scan_secrets.py --all
python3 tools/check_spdx.py
git diff --check c289b462 8dad71a
git diff --check 7402214 9a7a348
```

| 검증 | 독립 실행 결과 | 증거 |
|---|---|---|
| 정책 회귀 | **21 PASS / 0 skip** | `policy21.log` |
| UI Vitest | **99 PASS / 8 suites / 0 skip** | `ui99-after-build.log` |
| tokens | **9 PASS / 0 skip** | `tokens.log` |
| 버전 도구 회귀 | **91 PASS** | `registry-tests.log` |
| 독립 추가 lock/React 공격 | **12개 모두 기대값** | `independent-policy-attacks.mjs`, `.log` |
| schema 연결 공격 | **4개 모두 거부** | `schema-attacks.json` |
| 토큰 생성·UI tsc·지시문 검사 | 성공, 지시문·고지 검사 성공 | `build.log` |
| 정책 생성물 check | 성공 | `policy-sync.log` |
| 비밀 스캐너 | **1302파일 / 0건 / 예외 0건**, exit 0 | `secrets.log` |
| SPDX | **196파일 / 오류 0** | `spdx.log` |
| 공통/upstream diff 공백 | 두 범위 모두 exit 0 | 불변 diff 직접 확인 |

manifest의 tokens7이라는 요약과 별개로, 고정 source에서 실제 실행된 tokens는 9개다. 제공된 `common-python-final.log`는 **Ran 341 / skipped=1**, 즉 실행 성공 340개이며 이 실행을 내가 다시 수행했다고 세지 않았다. Doctor0·전체 lint/examples는 제공된 실제 log와 exact-head 원격 frontend 성공을 근거로 구분했다.

첫 Vitest 실행은 일반 pretest에 해당하는 dist 준비를 생략해 preview suite가 self package import를 해석하지 못했다(나머지 97 PASS). 정해진 build 준비 후 재실행한 결과가 99 PASS다. 최초 로그 `ui99.log`도 보존했다. 임시 node_modules symlink를 연결한 상태에서 전체 트리 secret scanner가 symlink를 거부했으므로 연결을 해제한 뒤 다시 실행해 위 1302/0 결과를 확인했다. 두 준비 문제를 제품 회귀 또는 PASS로 숨겨 집계하지 않았다.

## 산출물·소스·c6 실측 증거의 독립 대조

다섯 tgz를 읽기 전용으로 열어 실제 SHA512를 manifest와 대조했으며 **전부 일치**했다. 파일 내용을 새 immutable worktree의 source/생성물과 비교한 결과, 비교 가능한 파일은 UI94 / tokens25 / core11 / web31 / RN14개이며 불일치가 없었다. UI/tokens dist는 이번 독립 build 결과를 대조했다. upstream dist는 이번에 새로 빌드하지 않았고, 동봉 source/metadata/config/license를 불변 source와 대조하고 정확 SHA의 원격 전체 gate를 별도로 확인했다.

| 패키지 | 버전 | 무결성·핵심 내용 |
|---|---|---|
| @kor-travel/ui | 0.2.0 | manifest SHA512 일치; runtime/CSS/dist/checker가 고정 source·build와 일치 |
| @kor-travel/tokens | 0.1.1 | manifest SHA512 일치; Radix 상태 CSS·tw-animate import·MIT 전문 포함 |
| vworld-map-core | 1.0.1 | manifest SHA512 일치; GPL-3.0-only, LICENSE/NOTICE/src/tsconfig 포함; source7파일 |
| vworld-map-web | 1.0.3 | manifest SHA512 일치; GPL-3.0-only, LICENSE/NOTICE/src/tsconfig 포함; source27파일; core 정확 1.0.1 |
| vworld-map-rn | 1.0.1 | manifest SHA512 일치; GPL-3.0-only, LICENSE/NOTICE/src/tsconfig 포함; source10파일 |

core/RN은 이전1.0.0에서1.0.1로 증가했다. 기존1.0.0 bytes를 같은 버전으로 재발행한 것으로 취급하지 않는다. web1.0.3은 manifest상 미출시 후보 상태를 유지한다. registry 공개·과거 release 기록 전체를 새로 조사한 것은 아니다. README의 이용범위를 확대하지 않고 package 자체를 GPL-3.0-only로 명시한 점을 확인했다.

common artifact의 source는 `5e064808fabd3a54968dd20910eaccd04eba9f38`이고 review head는8dad71a다. 두 SHA의 제품 delta는 **frontend-artifacts.json만**이며 코드·policy·runtime/CSS 변경은 없었다. 해당 JSON은 새 c7 원장 기록이다.

기존 실측 root `/tmp/kor-ui-final-l47so8dm`의 c6 tgz와 이번 c7 tgz를 **내가 직접 파일별 비교**했다. UI/tokens 모두 변경 파일은 정확히 `package/check-dependencies.mjs` 하나였다. `validation/common-c6-c7-runtime-equivalence.json`의 주장과 일치한다. c6 앱의 실제 node_modules 내용도 c6 tgz 전체 파일과 대조해 불일치 0을 확인했다. root node_modules가 없고 app별 node_modules를 사용한 격리 구조였다.

추가로 c6 앱의 server-variants/radix-contracts TSX, globals.css, postcss 설정, package.json이 고정 source와 동일함을 확인했다. 기존 `.next/server/app/server-variants.html`에 서버 링크·서버 배지·client 대조 버튼이 실제 생성돼 있다. 제공된 `common-isolated-final.log`에는 webpack 및 Turbopack의 `/server-variants` 포함 빌드 성공, 그 앱에서 수행한 Chromium의 방향·상태 CSS·키보드·포커스 시험1 PASS가 기록돼 있다. 이것을 **기존 실제 실행 증거 + 이번 독립 bytes/설치본 대조**로 사용했다. 내가 c7에서 브라우저를 새로 실행한 것으로 표시하지 않는다.

신규 shadcn-tailwind.css도 [공식 고정 source](https://github.com/shadcn-ui/ui/blob/dd41d19e2f80ff6891951f7ced74c2c9a650b065/packages/shadcn/src/tailwind.css)를 GitHub 도구로 직접 조회했다. 추가 출처 헤더를 제외하면 원문과 정확히 같으며 원문 SHA256은 `4c371f7a1ff5d219ae2f7ff28bd256b4346fd546fe46fbae22092e57db2f0fae`다. MIT 전문과 PV-047/048/049의 출처 행도 동봉/기록됐다.

상세 근거: `artifact-verification.json`, `existing-c6-smoke-verification.json`, `shadcn-upstream-reference.css`, 제공된 실제 로그 사본.

## 최초 B finding closure

원본 심각도와 ID를 변경하지 않는다. 아래 FIXED는 원 리뷰어 B가 manifest2에서 확인한 closure다.

| 최초 ID | 심각도 | 상태 | 수정 위치·재검증 근거 |
|---|---|---|---|
| B-P0-01 | P0 | **FIXED** | upstream 세 package의 files/license/NOTICE, `scripts/check-package-notices.mjs:6`. 실제 다섯 tgz 중 core/web/RN의 GPL-3.0-only 전문·NOTICE·원 source·tsconfig를 직접 확인했다. source가 이전1.0.0 bytes 재발행 없이 core/RN1.0.1, web의 core1.0.1로 연결됐다. 정확9a7 CI의 pack 고지 단계도 성공. |
| B-P1-01 | P1 | **FIXED** | common `tools/check_frontend_dependencies.mjs:38`, `:55`, `:73`. runtime부터 실제 lock 물리 경로를 해석하며 동일 버전의 별도 React도 거부한다. 기존21회귀와 독립 alias/link/hoist/순환 테스트에서 올바른 결과. 다른 workspace·독립 dev 도구의 React18은 통과. 두 배포 checker 사본이 고정 source와 같음. |
| B-P1-02 | P1 | **FIXED** | `tools/check_frontend_dependencies.mjs:19`, `:23`, `:36`. 4개 dependency section별 정확 버전·중복을 검사하고 runtimeRequired는 dependencies에 요구한다. 운영18/dev19 덮어쓰기와 runtime의 dev-only 이동을 모두 exit1로 재현했다. |
| B-P1-03 | P1 | **FIXED** | `versions.json` react-native0.88.1 축과 `tools/check_versions.py:369` 연결 검사, JS 필수 정본 존재 검사. 모바일 RN wildcard와 lock 누락 각각 거부. required 축 누락/required-forbidden 충돌/artifact 축 누락/runtimeRequired 연결 오류도 모두 schema에서 거부. |
| B-P1-04 | P1 | **FIXED** | `packages/ui/src/button-variants.ts:7`, badge-variants의 동일 분리. 순수 CVA 정의이고 client 모듈 재export가 제거됨. c6의 실제 webpack+Turbopack RSC route 성공·생성 HTML을 확인했고 c7의 모든 runtime 바이트가 같음을 증명했다. |
| B-P1-05 | P1 | **FIXED** | `packages/ui/smoke/prepare-lock.mjs:13`, smoke/example package·lock 핀 갱신. helper가 manifest의 실제 새 tgz 이름을 읽는다. 기존 c6 격리 앱의 새 버전 install·양 빌드·browser 성공과 c7 동일 runtime 확인. exact8dad packages CI의 최종 완료는 별도 남은 gate다. |
| B-P1-06 | P1 | **FIXED** | `packages/tokens/radix.css:4`, `:6`, `shadcn-tailwind.css`. 공식 custom variant·애니메이션 CSS 연결을 실제 동봉했다. 공식 원문 동일성, c6 실제 computed style 시험 성공, c7 동일 CSS를 대조했다. |
| B-P1-07 | P1 | **FIXED** | login-form 스키마/포커스 표현과 공백 정리. scanner1302/0, 공통·upstream diff check0을 직접 확인했고 exact common head의 docs·secret·tools 양 OS가 성공했다. 실제 secret 노출 finding으로 바꾸지 않았다. |
| B-P2-01 | P2 | **FIXED** | mobile profile의 `forbidden`에 ui/radix-ui를 추가하고 JS가 profile 금지를 적용한다. DOM ui 추가 회귀와 독립 mobile radix 입력이 거부된다. 별도 native CSS fork의 버전 승인을 포함하지 않는다. |
| B-P2-02 | P2 | **FIXED** | `packages/ui/src/tabs.tsx:21`에 orientation 전달. 직접 실행한 UI 회귀에서 vertical ARIA·ArrowDown 전환이 성공했다. 기존 실제 browser 시험도 동일 runtime에서 성공. |
| B-P2-03 | P2 | **FIXED** | `packages/ui/src/tabs.tsx:89`의 inactive hidden selector, map-controls의 현재 활성값·hidden 처리. forceMount 상태 보존/숨김 단위시험과 동일 runtime의 실제 browser panel 가시성 시험을 확인했다. |

추가 공격은 원래 시험을 재진술하는 데 그치지 않고, npm alias의 실제 name, workspace link의 resolved source, hoisted root와 앱별 같은 버전 React 인스턴스, runtime dependency cycle, dev 도구 분리를 포함했다. 12개 모두 기대값이었다. 새 거대 설치 없이 lock resolution 경계에 집중한 fixture이며 실제 소비자 전체 설치 재실행을 대신한다고 주장하지 않는다.

## 신규 finding

### B2-P3-01 — tokens 고지의 현재 상태 설명이 새 MIT CSS 동봉 사실과 모순된다

- 심각도: **P3**, 상태: **OPEN**
- 위치: **common `packages/tokens/THIRD_PARTY_NOTICES.md:23`** (`:27`의 새 고지와 충돌).
- 근거: 23~25행은 현재 패키지에 별도 서드파티 소스 사본이 없어 추가 MIT/ISC/OFL 고지 항목이 없다고 단정한다. 27행은 shadcn-tailwind.css를 MIT 원문에서 가져와 동봉한다고 설명한다. 실제 manifest2 tokens tgz에는 그 CSS와 SHADCN_LICENSE가 있다. 같은 파일의 과거 무사본 설명을 남겨 현재 설명을 둘로 만들었다.
- 재현: `git show 8dad71a:packages/tokens/THIRD_PARTY_NOTICES.md`의23~27행과 integration-7-review의 tokens tgz 내용을 함께 확인하면 된다.
- 영향: 수령자가 고지·출처 감사 때 현재 패키지의 서드파티 포함 여부를 모순되게 읽게 되는 작은 문서 결함이다. GPL/MIT 전문은 실제 동봉돼 있으며 P0 고지 누락으로 분류하지 않는다.
- 권고: 과거 무사본 문장을 현재 동봉 CSS/의존성 설명에 맞게 수정하거나 역사 설명으로 명확히 표시한다. 수정은 새 불변 delta에서 확인한다. 연기할 경우 owner·상세 task·gate·기한을 갖춘 정식 DEFERRED가 필요하며 이 보고서는 임의로 연기 승인하지 않는다.

## 원격 CI 관찰

review/comment API는 사용하지 않았다. 아래는 commit별 runs/jobs API로 직접 관찰한 결과이며 증거의 `remote-ci-jobs.json`에 UTC를 함께 보존했다.

- common8dad의 [frontend run43035225996](https://github.com/digitie/kor-travel-common/actions/runs/43035225996), [workflow selftest43035225988](https://github.com/digitie/kor-travel-common/actions/runs/43035225988), [python-package43035226277](https://github.com/digitie/kor-travel-common/actions/runs/43035226277): success.
- [docs run43035225968](https://github.com/digitie/kor-travel-common/actions/runs/43035225968): check-versions130572322649 / docs130572322735 / tools Windows130572322783 / secret130572322809 / tools Ubuntu130572322997은 success. **packages130572322451은 마지막 조회에서 in_progress**, Next 설치 산출물 검증 단계이며 후속 tarball 설치 smoke는 pending이었다. 이전 commit의15 PASS로 이 상태를 덮지 않았다.
- upstream9a7의 [Marker CI43028824563](https://github.com/digitie/maplibre-vworld-react/actions/runs/43028824563), job130550264740: success. 정확 SHA 확인·typecheck/build/lint·신규 pack 고지·RN21·source browser19·packed browser19 단계 모두 성공. 로컬에서 이 전체 pipeline을 다시 수행한 것으로 세지 않았다.

중앙 reusable guard의 실행 source40자리 pin, 현재 main의 정책 데이터 checkout과 실제 revision 기록, 외부 policy/canonical 요구를 확인했다. main은 문서화된 검사 정책 데이터이며 배포 코드 참조와 구분돼 있다. canonical 회귀는 앱이 vendor·원장·lock을 함께 바꿔도 중앙 차이를 거부한다. 아직 이 변경을 실제 소비자 main에 배포했다고 주장하지 않는다.

## 한계와 merge 조건

1. 기존 11개 finding은 본 manifest에서 FIXED다. 새로운 P0/P1/P2 회귀는 발견하지 않았다. 새 P3 고지 문구는 OPEN이다.
2. exact common packages CI 최종 상태는 이 보고서 완료 시점의 관찰 결과를 따른다. in_progress를 성공으로 집계하지 않으며 merge 담당은 완료 결과를 별도로 확인해야 한다.
3. 새로운 실제 브라우저 실행은 **NOT_RUN**이다. 임시 서버/브라우저 재실행 명령이 자동 승인 검토에서 `blocked by policy`로 거부됐으며 추가 이유는 제공되지 않았다. 제한을 우회하지 않고, 사용자 허용 범위의 기존 c6 실제 실행 증거·설치 내용·c7 바이트 동등성 독립 검증으로 확인했다.
4. 실제 소비자 최종 통합·이미지/운영 배포·모바일 native 실행·별도 NativeCSS fork/향후 정책 변경은 **범위 밖 / NOT_REVIEWED**다. 이번 manifest는 불변으로 유지하고 별도 후속 manifest에서 검토해야 한다.
5. 소스 수정·npm 재설치·다른 에이전트 캐시 삭제를 수행하지 않았다. 이전 B 원본 보고서는 동일 SHA256으로 보존했다.

**최종 verdict: CONDITIONAL — 기존 11건 FIXED, 신규 P3 1건 OPEN, exact common packages CI 완료 확인 필요.**

검증 종료 뒤 두 reviewer 소유 worktree와 임시 evidence 디렉터리를 정리했다. 별도 보존한 evidence와 기존 validation/캐시/산출물은 유지했다. 최종 원본 B·manifest SHA256도 위 값과 일치했다.
