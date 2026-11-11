# 독립 적대리뷰 A(Mill) — COMMON source3 / integration8

- Run ID: Mill-A-common-postfix-3-7e3f33e-integration8.
- 원 reviewer A, frontend/accessibility. 구현에 참여하지 않았으며 다른 reviewer의 보고서·결과를 열람하지 않았다.
- 시작 UTC: 2026-11-11T15:33:44Z. 시험 종료 관찰 UTC: 2026-11-11T15:43:48.388208+00:00.
- 원문 작성 UTC: 2026-11-11T15:48:56.904493+00:00.
- **전체 merge-gate verdict: BLOCK. exact7e CI는 FAIL이며 후속 수정은 이 manifest에 없다.**
- **담당 source review: CONDITIONAL. 신규 P0 0 / P1 0 / P2 1 / P3 0. A-P2-09 OPEN.**
- 원 source2 finding **A-P2-08 FIXED**를 원 reviewer 본인이 실제 c8 브라우저에서 확인했다.
- 기존 raw report와 evidence는 수정하지 않았다. 이 원문은 source3의 별도 기록이다.

## 1. 불변 입력·관찰 SHA·격리

manifest: root/review-manifest-common-3.json.
실측 SHA256: 047ae6686cf8a08515a1e20b97147c218d5278823e976a6022aad34097021cd6.

| 입력 | 검토 기준 |
|---|---|
| common base | c289b4624c8640eb918cc915803e72ae754e58fb |
| source2 → source3 | 8dad71a50f9f8f12f0e3ba1c913a93e404dabfed → 7e3f33e0391990b9312fee513de581e28035aa8b |
| VWorld base/head | 9c46c57181d433c91f7e8837c4e4396204e9b583 / 9a7a348b02d61969b394c681b024d5851eef836b |
| c8 pack source | 670a753bc17f956f71bdc28385d6241a6e4ee017 |
| artifacts | root/artifacts/integration-8-review |

여기서 root는 /home/digitie/dev/common-unification-20261111 이다.

common은 /tmp/review-A-common3/source의 detached immutable worktree로 검토했다. 시험 후 HEAD는7e3, porcelain은 비어 있다. 670a→7e3은 원장·docs·작업 기록 변경으로 pack runtime/CSS는 동일하다. source2→7e3 diff와 변경 주변 타입·시험·policy·workflow를 조사했다.

종료 시 공유 common checkout은 이미 00ddd65be56a1955a4cee1a458a8cc274946fbe1 / clean으로 진행돼 있었다. 이 새 commit은 검토 기준에 섞지 않았다. 공유 VWorld는9a7a348 / clean이었다. 실제 관찰값은 observations-end.json에 저장했다.

source2 원문의 실측 SHA256은 c74c05a4ae3b4752c38e5fa809e8fda432971fb13f424c7d6a526ad622411891 로 전후 일치한다. 최초 원문도 수정하지 않았다.

## 2. c8 bytes와 실제 consumer

6 tgz 모두 SHA512를 manifest와 대조하여 MATCH했다. artifact-check.json에 실제 SHA256/SHA512를 보존했다. 주요 SHA256:

- UI: 8e6a0adfb5ca3229e288a7e1c982ccf28f31ad88cd3086d642fdf8746f2f914a
- tokens: f0fd2d95a3dea718f6111ce98207d122f336134b6e3703c5986c284d25db0b1d
- lightningcss.fix.4: 12c8326428a56e38231f7b5b376df0c6882e3492da794f3499269628edcaccf0

UI94파일, tokens25파일의 비교 대상 source/build와 pack 내용은 차이0이다(source-pack-match.json). VWorld3 pack은 이전과 같은 bytes이다. 비교 대상 밖까지 source 일치를 주장하지 않는다.

UI/tokens/fix4를 private consumer에 실제 풀었다. 기존 모듈을 읽기 참조하고 Tailwind 및 node/postcss adapter만 작게 복사하여 private fix4를 일반 module resolution으로 사용했다. Tailwind의 실제 lightningcss 해석 경로는 /tmp/review-A-common3/pack/node_modules/lightningcss/node/index.js, version은1.33.0+nativecss.fix.4였다. Playwright1.65.0을 사용했다. consumer-module-resolution.log에 기록했으며 clean install 결과로 표현하지 않는다.

## 3. 직접 실행한 검증과 raw evidence

영구 evidence: root/review-A-common-evidence-postfix-3/.
commands.txt는 cwd를 적은 재실행 명령표다. config·공격 script·raw stdout도 같은 곳에 보존했다. Python discovery의 원 argv는 보존되지 않았으며 실행 결과는 raw log로 제시한다.

| 검증 | 결과 | evidence |
|---|---|---|
| common type / build | PASS | type.log / build.log |
| UI Vitest | 101 PASS / 0 SKIP | ui-unit.log / vitest.config.mjs |
| tokens | 9 PASS / 0 SKIP | tokens.log |
| dependency/nativeCSS policy | 41 PASS / 0 SKIP | policy.log |
| lint / examples / policy 생성물 동기화 | PASS | lint.log / examples.log / policy-sync.log |
| Python unittest 전체 | 347실행 = 346 PASS + 1 SKIP, 실패0 | python-all.log |
| 실제 c8 Next production webpack / Turbopack | 모두 PASS | next-webpack.log / next-turbopack.log |
| c8 webpack packed Chromium | 65 PASS | packed-browser.log |
| c8 Turbopack selected Chromium | 10 PASS | packed-browser-turbopack.log |
| A-P2-08 원 공격 | PASS, outline-color 전환 없음 | focus-transition-regression.mjs / focus-transition.log |
| 새 policy 구문 공격 | 거부해야 할 3종을 수락, 아래 finding | policy-source-forms.mjs / policy-source-forms.log |
| strict UTF8 prod scan 전체 | FAIL exit2, 기존 CI 실패를 로컬 재현 | known-prod-scan-failure.log |
| source2→7e diff --check | PASS | delta-diff-check.log |

Dialog browser suite는 immutable source의 dialog-browser.spec.ts를 사용했다. 320x568/375x667/667x375/1280x720에서 긴 Dialog·AlertDialog의 내부 스크롤, 저장, 상단 닫기, Escape, 초점 복원, 중첩 portal, 입력 보존, unstyled sheet, overlay 취소와 busy 제어를 확인했다. 375/500/640/700/1280/1600폭에서 full/sm/md/lg/xl/2xl과 consumer override를 확인했다. webpack 전체는 Dialog64+Radix1, Turbopack 추가는 좁은 폭4+responsive override6이다. 실제 브라우저 실행 없이 제출 CI 증거만으로 PASS한 항목이 아니다.

## 4. 원 finding disposition

**A-P2-08: FIXED.** 위치 packages/ui/src/table.tsx:72.

TableRow의 transition-colors가 outline을 제외한 명시 transition 속성 목록으로 변경됐다. 실제 c8의 clickable VirtualTable 행을 키보드 focus하고 즉시/300ms 후를 독립 측정했다:

- focused=true, focusVisible=true.
- 즉시/안정 후 outlineColor 모두 oklch(0.45 0.09 169).
- transitionProperty = color, background-color, border-color, text-decoration-color, fill, stroke.
- outline-color가 없고 원 assertion은 exit0이다. 다른 속성의0.15s 전환이 남아도 focus outline에는 적용되지 않는다.

최초10건(A-P1-01/02, A-P2-01〜07, A-P3-01)의 source2 FIXED disposition은 원문대로 유지한다. 이번 delta·UI101·packed Radix/Dialog·두 production builder에서 다시 OPEN할 회귀를 찾지 못했다. 이전의 모든 공격과 지도 WebGL을 이번에 전부 다시 실행했다는 의미는 아니다.

Dialog/AlertDialog의 viewport 상한, 내부 overflow, size, unstyled, 단일 overlay에 대한 props/ref/events 전달을 source·타입·unit·packed browser로 확인했다. 이번 delta에서 새 UI finding은 없다.

## 5. 신규 A-P2-09 — 금지 root/deep path가 재export·literal import/require로 policy 통과

- **P2 / OPEN.** 수정 또는 정식 disposition 후 원 reviewer 재확인이 필요하다. 이 원문은 연기를 승인하지 않는다.
- 위치: tools/check_frontend_dependencies.mjs:145, 배포 복제 packages/ui/check-dependencies.mjs:145 및 packages/tokens/check-dependencies.mjs:145.
- 계약: docs/standards/frontend-libraries.md의 구 private maplibre-vworld-react root 및 하위 경로 source import 금지. 현재 AST 방문은 ImportDeclaration만 검사한다.
- 재현: 정상 required 의존성과 canonical artifact hashes를 갖는 기존 policy fixture를 사용한다. legacyAdapter의 transitive 구 root를 lock에 넣되 구 root 자체를 direct dependency로 선언하지 않는다. src/map.tsx의 한 줄만 다음 네 형태로 바꾸어 같은 checker를 실행한다.

~~~ts
import {Map} from 'maplibre-vworld-react/packages/web/src/index';
export {Map} from 'maplibre-vworld-react/packages/web/src/index';
export const load=()=>import('maplibre-vworld-react/packages/web/src/index');
export const Map=require('maplibre-vworld-react/packages/web/src/index');
~~~

실측 결과는 순서대로 exit1, exit0, exit0, exit0이다. 첫 구문만 금지 package import 오류이며 나머지 셋은 「공통 의존성과 산출물 일치」로 통과한다. policy-source-forms.mjs와 JSON-lines log에 전체 입력과 stdout/stderr를 보존했다.

영향: barrel의 정적 재export나 SSR 지연 로딩에서 구 private/deep 경로를 사용해도 source gate를 우회한다. direct dependency 거부와 artifact hash 검사 자체가 무력화됐다는 주장은 아니다. transitive package가 존재할 때도 source 금지 계약을 지켜야 하며, 정적 재export는 동적 이름 해석 문제도 아니다. 실제 소비 앱이 이미 이 구문을 사용한다고 주장하지 않는다.

수정 권고: module specifier 추출을 공통화하고 ExportDeclaration, literal import()/require(), 필요하면 외부 ImportEqualsDeclaration에 동일한 exact root 또는 root+"/" 판정을 적용한다. 이번 거부 회귀와 함께 maplibre-vworld-react-extra 같은 인접 이름을 허용하는 시험을 유지하고 배포 checker도 동기화한다. 비literal 동적 specifier 전체 해석은 본 finding의 요구가 아니다.

## 6. exact7e CI 실패와 판정 경계

부모의 실제 CI 관찰(다른 reviewer의 진단이 아님)을 parent-ci-status.json에 명시했다. exact7e는 FAIL이다:

1. 새 vendor binary tgz가 strict UTF8 scanner에서 입력 오류가 된다. 본인도7e immutable source에서 python3 -B -X utf8 tools/check_prod_redaction.py --all을 실행하여 exit2 / 「검사 오류: UTF-8로 검사할 수 없는 입력」을 재현했다. tools/_scan.py:123-127의 decode 제약 및 workflow 전체 scan 호출을 확인했다.
2. MCR packages job이 SHA assert 전에 Git dubious ownership으로 실패한다. 이 건은 부모의 실제 CI 관찰이며 본 reviewer가 MCR container에서 재현하지는 않았다.

부모가 수정 중인 bounded archive scan/security regression, exact workspace Git trust는 후속 delta이며 이7e에는 포함하지 않는다. 이 두 건을 자신의 독립 신규 finding으로 중복 채번하지 않았으나 **merge gate를 BLOCK하는 기존 실패**로 유지한다. 로컬 UI/browser 통과를 remote CI PASS로 바꾸어 쓰지 않는다.

MCR workflow는 digest 고정 Playwright1.65.0 noble, Node22.23.1, --init/--ipc=host, /ms-playwright의 version/path/executable/Chromium 기동 preflight를 source로 확인했다. MCR image pull/container 실행은 NOT_RUN이다. 로컬 Chromium 성공은 해당 remote 환경의 실증을 대신하지 않는다.

별도 NativeCSS748 run43047084671의 macOS job130613789629는 부모의 최신 관찰상 CANCELLED(실행 없음)이다. Linux/Windows/source-gate SUCCESS의 공유 상태와 구분하며 macOS PASS라고 쓰지 않는다(native-css-ci-parent-update.json). 이 별도 manifest 보충 정보가 common7e FAIL을 해소하지 않는다.

제출 Doctor0, links/plan, VWorld 전체 source19/packed19 및 NativeCSS Rust/native/WASM 전체는 이번 직접 재실행 성과에 합산하지 않는다. VWorld source/bytes는 이전과 불변이다. NativeCSS fork 원 finding 전체 closure, 소비 앱 전체, 앱 CSS fork, 실제 앱 export·배포, 실제 스크린리더 낭독은 별도 scope/NOT_RUN이다.

## 7. 보전·최종 판정

구현 source를 수정하지 않았다. 대규모 install이나 타 agent cache 삭제를 하지 않았다. 용량 확보를 위해 중지된 자신의 과거 NativeCSS Rust target 두 경로만 절대 경로 검증 후 삭제했고 own-cleanup.json에 기록했다. 이전 raw/evidence/source/pack은 유지했다. 생성 출력은 자신의 tmp에, 영구 evidence는 root의 자신의 별도 디렉터리에 두었다.51878의 자신의 server는 PID/cwd 확인 후 중지했다.

**A-P2-08 FIXED / 신규 A-P2-09 OPEN(P2) / 담당 source CONDITIONAL / exact7e merge gate BLOCK.**

P2 수정 재확인 또는 정식 disposition, 별도 delta의 기존 CI 실패 해소 및 exact 새 source CI acceptance 전에는 이 원문을 무조건 PASS로 요약하지 않는다.
