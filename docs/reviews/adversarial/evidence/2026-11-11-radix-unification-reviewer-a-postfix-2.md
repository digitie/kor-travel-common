# 독립 적대리뷰 A(Mill) — 수정 후 2차

- Execution ID: `Mill-A-postfix-2-8dad71a-9a7a348`(본 실행 식별자).
- 원 리뷰어: A(Mill), frontend/accessibility. 구현에는 참여하지 않았다.
- 시작 UTC: `2026-11-11T14:05:58Z`.
- 종료 UTC: `2026-11-11T14:19:42.790542+00:00`.
- 종류/상태: 같은 원 리뷰어의 post-fix 독립 재검토, `COMPLETE`.
- **전체 verdict: `CONDITIONAL`**.
- **최초 A finding 10건: 전부 `FIXED`**. 최초 P1 두 건을 원 reviewer A가 직접 재현 기준으로 닫았다.
- **신규 OPEN: P0 0 / P1 0 / P2 1 / P3 0**. 신규 `A-P2-08`의 수정 재확인 또는 owner·task·gate·기한을 갖춘 정식 연기 disposition이 조건이다. 이 보고서가 연기를 승인한 것은 아니다.
- 지도 원본의 이번 delta: 본 담당 범위에서 새 finding 없음.
- 다른 리뷰어의 원본 보고서/finding은 열람하지 않았다. 최초 보고서와 evidence는 변경하지 않았다.

## 1. 기준선·원본 보존·격리

manifest: `/home/digitie/dev/common-unification-20261111/review-manifest-common-2.json`.

실제 SHA256은 전달값 `a78334ceb396293ee377aa29403554fc158c2e256b1159b26607acad0bdfda90`과 일치한다.

| 저장소 | 원 기준 base | 이전 A review head | 이번 실제 관찰/검토 head |
|---|---|---|---|
| common | `c289b4624c8640eb918cc915803e72ae754e58fb` | `789e6d2e179a055b3cd793fb886083543244089c` | `8dad71a50f9f8f12f0e3ba1c913a93e404dabfed` |
| VWorld 원본 | `9c46c57181d433c91f7e8837c4e4396204e9b583` | `7402214b9d4829f1f73f80ac29f68d22e2809254` | `9a7a348b02d61969b394c681b024d5851eef836b` |

최초 `review-A-common.md`의 시작/종료 SHA256은 모두 `a295b96a40f70d2cf02eb73235cdd9a877b9a85d560adc985d02635944389832`이다. 원문을 수정하지 않았다.

common은 `/tmp/review-A-postfix2-common` detached worktree를 위 commit으로 만들었다. 초기 설정 과정의 node_modules 최상위 symlink 두 개는 directory 형태와 내부 symlink로 바꾸어 실제 검토/시험 시작 전 clean을 확인했다. 초기 preflight의 untracked 출력과 이후 clean 확인을 모두 evidence에 남겼다. 시험 뒤에도 HEAD는 동일하고 porcelain 출력은 비어 있다. tracked code·생성물 diff는 없다.

두 구현 checkout도 시작·종료 관찰에서 위 SHA/clean이었다. VWorld 소스는 immutable object로 읽고, 마지막 core/web `tsc --noEmit`만 동일 SHA/clean 원 checkout에서 실행했다. 코드·배포·운영 데이터는 수정하지 않았다.

대규모 설치는 하지 않았다. root 디스크 약1.9GB·tmp 약4.6GB의 시작 여유를 확인한 뒤, 일반 의존성은 기존 설치를 참조하고 Vite/Vitest/Next 출력과 private c7 package는 본 리뷰의 `/tmp/review-A-postfix2-*` 경로에 두었다. 다른 agent의 cache나 환경을 지우지 않았다.

## 2. integration-7-review 실제 pack 검증

사용한 디렉터리는 **`artifacts/integration-7-review`**이다. 루트의 c6 tgz를 c7로 오인하지 않았다.

- UI0.2.0, tokens0.1.1, core1.0.1, web1.0.3, RN1.0.1 다섯 tgz를 실제 SHA512로 계산하여 manifest integrity와 모두 MATCH했다.
- c7 원장의 common source는 `5e064808fabd3a54968dd20910eaccd04eba9f38`이다. 이 commit에서 review HEAD `8dad71a`까지는 **frontend-artifacts.json만 변경**되어 source/검사기/runtime 차이는 없다.
- 제출된 `validation/common-c6-c7-runtime-equivalence.json`을 읽었으며, c6와 c7 archive의 **모든 일반 파일을 독립 비교**했다. UI와 tokens 각각 실제 차이는 `package/check-dependencies.mjs` 하나뿐이었다. runtime·CSS뿐 아니라 나머지 일반 파일도 동일했다.
- c7 UI/tokens를 별도 consumer의 private node_modules에 실제로 풀어 사용했다. webpack/Turbopack·브라우저 확인은 이 c7에 대해 직접 실행했다. 따라서 제출 c6 브라우저 성공만으로 closure를 추론하지 않았다.
- 별도 source build의 UI dist/CSS/checker/policy 88파일, tokens 19파일을 c7과 비교해 모두 동일했다. VWorld의 pack 내 source/manifest/tsconfig를 commit object와 비교한 결과 core9·web29·RN12파일 모두 동일했다. 비교 대상 외 파일까지 같다고 확장하지 않는다.

입력/결과: `artifact-check.json`, `source-pack-match.json`, `observations-start.json`, `observations-end.json`.

## 3. 직접 실행한 검증과 raw evidence

영구 evidence: `/home/digitie/dev/common-unification-20261111/review-A-common-evidence-postfix-2/`.

정확한 실행 명령은 `commands.txt`에 보존했다. PowerShell tool workdir은 `C:\`, 실행은 `wsl.exe --exec` 기준이다.

| 실행 | 결과 | Raw evidence |
|---|---|---|
| `npm run check` | PASS(tokens 생성물·UI 타입) | `type.log` |
| `npm run build` | PASS(tokens·UI, 고지 검사 포함) | `build.log` |
| UI `vitest run`(격리 cache config) | **99 PASS / 0 SKIP** | `ui-unit.log`, `vitest.config.mjs` |
| dependency-policy `node --test` | **21 PASS / 0 SKIP** | `policy.log` |
| tokens workspace 시험 | **9 PASS / 0 SKIP** | `tokens.log` |
| A 최초 공격 시험을 이 source에 맞춰 재실행 | **8 PASS / 0 SKIP** | `adversarial.test.tsx`, `adversarial.log` |
| lint·examples·policy 생성물 검사 | PASS | `lint.log`, `examples.log`, `policy-sync.log` |
| Python 전체 unittest | **341 실행 = 340 PASS / 1 SKIP / 0 FAIL / 0 ERROR**, 75.974초 | `python-all.log` |
| c7 Next16.4.6 `next build --webpack` | PASS, server-variants 포함 | `next-webpack.log` |
| c7 Next16.4.6 `next build`(Turbopack) | PASS, server-variants 및 A 추가 재현 route 포함 | `next-turbopack.log` |
| c7 webpack Chromium | RSC HTTP200·세로 방향키·2px panel focus·Switch 상태색/thumb·Dialog 복원 PASS, pageerror0 | `browser-c7.mjs`, `browser-webpack-c7.log` |
| c7 Turbopack Chromium 확장 확인 | 위 검증과 forceMount 상태/DOM 보존·Progress60/200·predicate 변경/bulk 해제·bulk/header 토큰·행 focus 폭 PASS | `review-a-page.tsx`, `browser-c7-extended.mjs`, `browser-turbopack-c7.log` |
| 새 행 focus 전환 공격 | **FAIL(exit1): outline-color가 150ms 전환됨** | `focus-transition-regression.mjs`, `focus-transition-regression.log` |
| c7 VWorld packed ESM 실제 Chromium/WebGL | 키 없는 명시 style·maxZoom22·style 교체 시 instance 보존·기존 missing-key fallback PASS, 외부 HTTP요청0·pageerror0 | `map-fixture.tsx`, `packed-map-server.mjs`, `browser-map-c7.mjs`, `browser-map-c7.log` |
| VWorld core/web `tsc --noEmit` | 두 명령 모두 exit0 | 명령 `commands.txt`; console 출력 없음 |
| 두 저장소 원 base→이번 head `git diff --check` | 두 명령 모두 exit0 | `kor-travel-common-diff-check.log`, `maplibre-vworld-react-diff-check.log` |

manifest의 tokens7 표기와 별개로 본 reviewer가 실행한 현 tokens suite는 9개다. 전체 Python의 skip1은 pass로 합산하지 않았다.

초기 harness 실패도 숨기지 않았다. UI suite의 첫 실행은 cwd를 루트에 두어 상대 CSS 경로가 맞지 않았고, 실제 workspace cwd에서 재실행하여99 PASS를 확인했다. MapTabPanel의 구 repro는 click 이벤트만 쏘아 Radix의 mouseDown 선택을 발생시키지 않았으므로 userEvent 전체 클릭과 실제 selected 전환 assert로 보강했다. 브라우저의 첫 즉시 assert/마우스 모달리티 assert도 실제 비동기 전환·키보드 조건에 맞게 수정했다. 첫 Turbopack 실행의 제한 root는 기존 의존성 symlink를 경계 밖으로 판단해 실패했으며, module들이 실제 존재하는 `/tmp`를 root로 설정한 뒤 빌드가 통과했다. 각각의 `*-first-*.log`를 보존했고 이 환경/driver 문제를 제품 finding으로 세지 않았다.

## 4. 최초 finding의 원 reviewer disposition

원본의 severity·ID는 바꾸지 않는다. 아래 `FIXED`는 A가 이번 manifest의 source와 pack에서 직접 확인한 결과다.

| 최초 ID | 이번 disposition | 수정 위치/확인 근거 |
|---|---|---|
| A-P1-01 | **FIXED** | `packages/ui/src/button-variants.ts:8`, `badge-variants.ts:8`의 순수 CVA 소유 모듈. client module 재수출 제거. 두 Next production builder에서 RSC 함수 호출 성공, c7 `/server-variants` HTTP200/링크·배지 표시. |
| A-P1-02 | **FIXED** | `packages/ui/src/map-controls.tsx:169`의 context 선택값에 따른 hidden. userEvent/실제 Chromium에서 inactive panel role 제외, hidden=true, 재활성화 후 같은 input DOM과 서울역 값 보존. |
| A-P2-01 | **FIXED** | `packages/ui/src/progress.tsx:18`의 max/current 정규화와 Root value 전달.60/200 ARIA/30% transform, 기존 suite의0·완료·미확정 확인. |
| A-P2-02 | **FIXED** | `virtual-table.tsx:384`의 유효 page 상태, `:408` 전체 해제 reset, `:419` 선택 불가 행 표시, `:573` bulk getCanSelect 필터. 최초 a,b선택→a불가 후 bulk=b, 전체 해제 후 bulk없음. controlled raw selection 보존/외부 이용 제약도 API 주석에 명시됨. |
| A-P2-03 | **FIXED** | `virtual-table.tsx:1192`/`:1195`의 row/detail 태그 JSON key. `x`/`x:detail` 입력으로 duplicate-key 경고0. 추가된 unit의 가상 항목/상세행 검사도 통과. |
| A-P2-04 | **FIXED** | `virtual-table.tsx:315`, `:382`, `:582`, `:926` 등 kt 유틸리티 정렬. c7에서 bulk·sticky header 실제 배경이 해당 kt token과 일치, focus token 클래스/최종색도 적용됨. 아래 신규 finding은 **정적 이름 누락과 다른 전환 문제**다. |
| A-P2-05 | **FIXED** | `packages/ui/src/tabs.tsx:89` 대체 2px focus outline. 실제 Tab으로 panel 포커스 후 computed solid/2px 확인. |
| A-P2-06 | **FIXED** | `tabs.tsx:21`의 Root orientation 전달. vertical ARIA와 ArrowDown 실제 선택/focus 확인. |
| A-P2-07 | **FIXED** | `packages/tokens/radix.css:4` 이후 animation/CSS vendor import. vendored custom data-state/data-orientation 정의 확인, c7 Switch 실제 track 색과 thumb 위치 변경 확인. |
| A-P3-01 | **FIXED** | 최초 후보에서 이번 후보까지 포함한 common 전체 base→head diff-check exit0. |

이전 report는 그대로 두고 closure를 이 별도 원문에 기록한다. 최초 두 P1에 대해 다른 reviewer의 대리 승인을 사용하지 않았다.

## 5. 신규 finding

### A-P2-08 — TableRow의 transition-colors가 focus outline 색을 150ms 전환함

- 상태: **OPEN**.
- 위치: `packages/ui/src/table.tsx:72`, `packages/ui/src/virtual-table.tsx:377`, `packages/ui/src/virtual-table.tsx:382`.
- 기준: `docs/standards/ux-guide.md:126`의 focus 링 즉시 표시/transition 밖 계약. VirtualTable의377행 주석도 outline-color를 포함하는 transition-colors 대신 명시 속성 목록을 쓰라고 적고 있다.
- 실패 원인: TableRow 기본 클래스에는 `transition-colors`가 있고, CLICKABLE_ROW_CLASS에는 이를 배제하는 transition 속성 override가 없다. Tailwind4가 outline-color를 전환 목록에 포함시킨다.
- 재현: 실제 c7 UI/tokens로 production build한 `/review-a`에서 `onRowClick`이 있는 VirtualTable을 렌더한다. Chromium reducedMotion=no-preference 상태에서 Tab 입력 후 행으로 focus를 이동하고 즉시/300ms 후 computed style을 읽는다. `node focus-transition-regression.mjs`의 기대는 outline-color 비전환이다.
- 실제: activeElement가 해당 행이고 `:focus-visible`도 true지만 transition-property에 `outline-color`, duration에 `0.15s`가 들어간다. 즉시 색은 `oklab(0.0150301 -0.00295071 0.000573852)`였고, 안정화 후에만 최종 focus token인 `lab(37.3873 -31.4435 6.34352)`가 된다. 자동 assertion exit1로 재현했다.
- 영향: clickable table row의 focus token 색이 계약처럼 즉시 나타나지 않는다. outline 폭 자체가 완전히 사라진다는 주장이나 데이터/인증 결함 주장은 하지 않는다. 위 A-P2-04의 utility-name 문제는 고쳐졌고, 이 항목은 병합된 TableRow 스타일의 별도 focus 동작 문제다.
- 수정 권고: TableRow 또는 clickable-row override에서 `transition-[color,background-color,border-color]` 등 outline을 제외한 명시 목록을 사용한다. 실제 c7 소비자와 같은 조건에서 computed transition-property에 outline-color가 없는지, focus 색이 즉시 token인지 확인한다.
- 근거: `focus-transition-regression.mjs`, `focus-transition-regression.log`, 보조 `focus-debug.mjs`/`focus-debug.log`.
- 권고 disposition: 수정 후 원 reviewer 재확인. 연기하려면 owner·상세 task·gate·목표시점이 있는 P2 DEFERRED 절차를 따르며, 본 원문은 아직 OPEN으로 남긴다.

## 6. 전체 delta와 판정 경계

일반 frontend delta에서는 CVA 분리, SSR/hydration 준비 경계 유지, native 자동완성 값→RHF 동기화, empty/error/loading, table server/client sorting·controlled selection·가상화 identity·확장행, CSS vendor 연결, direct dependency/lock/중앙 canonical 대조의 새 경로를 확인했다. 기존 로그인 중복 제출/비밀번호 초기화와 Dialog trap/복원을 자체 공격 시험에 유지했다.

지도 delta에서는 명시 mapStyle의 키 우회 계약, 기존 missing-key fallback 보존, setStyle 기반 instance 유지, 명시 style의 maxZoom 경로를 소스와 실제 packed WebGL로 확인했다. src/manifest를 immutable source와 대조하고 ESM consumer에서 사용했다. 본 담당 범위에서 새 지도 finding은 없다.

제출된 Doctor0·원격 CI15·VWorld 전체 source19/packed19·RN21는 부모 validation 증거이며, 본 reviewer가 그 전체를 다시 실행했다고 주장하지 않는다. CI 최종 상태·모든 소비자·native CSS fork·운영 배포·외부 VWorld API/타일·스크린리더 실제 낭독·6폭/다크 전체 수용은 **NOT_RUN(별도 범위/후속 manifest)**이다. 지도 독립 브라우저의 HTTP 요청은 loopback만 사용했다.

두 P1과 기존 P2/P3의 closure는 확정하지만, 신규 P2 OPEN1 때문에 이 reviewer의 전체 verdict는 `CONDITIONAL`이다. 해당 수정 또는 정식 연기 disposition 없이는 이 원문을 무조건 PASS로 요약하지 않는다. 이후 다른 정책/native CSS가 추가되어도 이 manifest 판정에 섞지 않는다.

## 7. 결과 보존·종료 상태

- 새 원문: `/home/digitie/dev/common-unification-20261111/review-A-common-postfix-2.md`.
- evidence: `/home/digitie/dev/common-unification-20261111/review-A-common-evidence-postfix-2/`.
- 원본/manifest SHA256 보존 및 종료 HEAD/clean: `observations-end.json`.
- 시험용51876/51877 listener는 PID와 cwd가 본 리뷰 임시 경로인지 확인한 뒤 종료했다.
- common detached 기준선은 clean으로 보존한다. 원 checkout·다른 agent cache·소비 앱 소스·원 리뷰 원문은 변경하지 않았다.
