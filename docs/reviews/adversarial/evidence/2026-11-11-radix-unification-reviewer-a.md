# 독립 적대리뷰 A — 공통·지도 원본 1차

- 실행 식별자(본 리뷰에서 부여): `review-A-common-1-789e6d2-7402214`.
- 역할: 구현에 참여하지 않은 frontend/accessibility 전문 리뷰어 A.
- 범위: 공통 Radix 27 부품, VirtualTable/TanStack9, RHF·Zod·Zustand LoginForm, SSR/RSC, 접근성·focus·행 identity, 지도 ESM 빌드/소비 경로.
- 요청: 부모가 제공한 immutable manifest에 대한 독립 source inspect와 필요한 격리 실행. 앱 최종 수용·PR merge·이미지 배포는 이번 범위 밖이다.
- 검토 시작 기준 기록: 2026-11-11 21:40:00.426 KST(첫 detached worktree 생성 시각). manifest/object 검증은 이보다 먼저 시작했으나 그 단계의 초 단위 시각은 기록하지 않았다.
- 종료: 2026-11-11T21:52:58.261493+09:00.
- 상태: `COMPLETE`.
- **전체 verdict: `BLOCK`**. `P0=0 / P1=2 / P2=7 / P3=1`, 전부 이 기준선에서 `OPEN`.
- 독립 신규: P1 1건·P2 5건·P3 1건. 부모 사전 공개 항목: P1 1건·P2 2건. 부모가 전달한 내용과 자체 발견을 아래에서 구분했다.
- 다른 리뷰어의 원본 보고서·finding은 열람하지 않았다. 부모가 진행 중에 직접 공개한 Tabs orientation/MapTabPanel/custom variants 세 항목은 독립 신규 발견으로 세지 않았다.

## 1. Immutable 기준선과 원장 검증

manifest: `/home/digitie/dev/common-unification-20261111/review-manifest-common-1.json`.

SHA256: `84179b1add068f8cd1ec5344d134055aa73a4d283b7ab8dd3124daf83666a3b3`.

| 저장소 | base | 실제 검토 head | 격리 경로 |
|---|---|---|---|
| common | `c289b4624c8640eb918cc915803e72ae754e58fb` | `789e6d2e179a055b3cd793fb886083543244089c` | `/tmp/review-A-common-789e6d2` |
| 지도 원본 | `9c46c57181d433c91f7e8837c4e4396204e9b583` | `7402214b9d4829f1f73f80ac29f68d22e2809254` | `/tmp/review-A-vworld-7402214` |

두 구현 checkout은 최초 관찰 시 manifest HEAD와 같았고 clean이었다. 두 detached worktree에서 시작·종료 `git status --porcelain=v1`가 모두 빈 출력이었다. 설치·빌드·시험은 격리 환경에서 실행했다. 구현 checkout의 추적 파일은 수정하지 않았다.

종료 시 common 구현 checkout은 부모의 후속 수정으로 dirty였다. 이 상태의 파일 내용은 판정 근거로 읽지 않았으며, 모든 finding과 line 번호는 고정 detached 기준선에 속한다. 지도 구현 checkout은 종료 시에도 clean이었다. 정확한 관찰값은 `review-A-common-evidence-1/metadata.json`에 보존했다.

`artifacts/common-artifacts.json`의 candidate는 `integration-5-review`, status는 `CANDIDATE_NOT_RELEASED`이며 manifest의 source/원장과 일치했다. 네 tgz의 SHA512를 실제 bytes로 계산해 모두 manifest integrity와 대조했다.

| 패키지 | SHA512 대조 | 고정 소스로 별도 빌드한 dist와 일치한 파일 |
|---|---|---|
| `@kor-travel/ui@0.2.0` | MATCH | 84 |
| `@kor-travel/tokens@0.1.1` | MATCH | 6 |
| `vworld-map-core@1.0.0` | MATCH | 14 |
| `vworld-map-web@1.0.3` | MATCH | 54 |

위 dist 비교 대상에서 불일치는 0이었다. 비교하지 않은 고지 파일까지 byte 동일하다고 확장해 해석하지 않는다.

manifest validation 원문은 evidence의 `manifest.json`에 그대로 보존했다. 그중 schema 전체340 시험은 **부모 제출 시점에는 pending**으로 기재되어 있었다. 본 리뷰가 별도로 실행한 결과는 아래와 같다. 부모의 lint/type/build/Doctor·RN21·Chromium17·tarball17 등 제출 증거와 본 리뷰의 직접 실행은 구분한다.

## 2. 직접 실행한 검증

환경: WSL Linux, Node `22.22.2`; PowerShell 도구의 workdir은 `C:\`이며 `wsl.exe --exec`로 실행했다.

| 명령·검증 | 직접 관찰한 결과 |
|---|---|
| 두 저장소 `git diff base head`, 관련 `git show head:path` | 고정 변경 범위 확인 |
| common `npm ci --no-audit --no-fund` | 성공; 고정 lock 사용 |
| common `npm run check` | tokens 생성물 검사·UI TypeScript 통과 |
| common `npm test` | tokens 8 PASS, UI 91 PASS, dependency-policy 8 PASS |
| common `npm run check:examples --workspace packages/ui` | PASS |
| common `npm run lint` | PASS |
| common `npm run check:policy` | PASS |
| common `python3 -B -X utf8 -m unittest discover -s tests -p 'test_*.py'` | 340 실행, **339 PASS / 1 SKIP / 0 FAIL / 0 ERROR**, 70.418초. skip을 pass로 합산하지 않음 |
| 지도 `npm ci --workspace vworld-map-core --workspace vworld-map-web --include-workspace-root --no-audit --no-fund` | 성공 |
| 지도 core build, web typecheck, web build | 전부 PASS |
| common `git diff --check base head` | **FAIL(exit 2)**: P3-01의 trailing whitespace |
| 지도 `git diff --check base head` | PASS(exit 0) |
| 추가 RTL/Vitest 공격 시험 8개 | 기대 동작 기준 **5 FAIL / 3 PASS**. 실패 5개는 Progress·predicate 변경·key 충돌·부모 공개 orientation·부모 공개 inactive panel 재현 |
| Tailwind4에 common theme/radix/tokens와 기본 theme/utilities를 입력해 실제 클래스 생성 | VirtualTable의 비-kt 클래스 7종 미생성; 대응 kt 클래스는 생성 |
| 실제 tgz 4종+정확 React/MapLibre 설치 후 Vite·Chromium 소비자 | 지도 ESM 주요 export import와 Zod schema 사용 성공, pageerror 0 |
| 동일 Chromium 소비자 | inactive map panel 노출, TabsContent의 focus 표시 부재, Switch 상태 스타일 불변 재현 |
| Next `16.4.6` webpack 개발 서버, 실제 UI tgz | `buttonVariants` 서버 호출 HTTP500, `badgeVariants` 서버 호출 HTTP500; `<Button>` 서버 렌더 대조군 HTTP200 |

공격 시험의 PASS 3개는 행 체크박스의 상태 갱신 시 focus 보존, Dialog 초기 focus/양방향 Tab trap/Escape 후 trigger 복원, 로그인 중복 제출 차단/username trim/password 초기화다. 기존 UI suite의 SSR/hydration 시험 3개도 PASS였다. LoginForm 저장소는 인스턴스별 생성이며 전역 Zustand 저장소에 비밀번호를 저장하지 않는 것을 소스로 확인했다.

첫 브라우저 harness는 workspace dist를 파일 경로로 직접 연결하여 CJS core가 Vite dependency 최적화 대상에서 빠졌고 named export 오류가 났다. 이 결과를 지도 제품 결함으로 판정하지 않았다. 정상 npm tarball 설치와 package import로 다시 구성한 소비자에서는 동일 export들이 오류 없이 로드되었다. 두 시도의 로그를 구분해 보존했다.

## 3. P1 finding

### A-P1-01 — variant 전용 공개 subpath가 client 파일을 재수출하여 RSC에서 HTTP500

- 출처: 독립 신규. 상태: `OPEN`.
- 위치: `packages/ui/src/button-variants.ts:3`, `packages/ui/src/badge-variants.ts:3`; client 경계는 `packages/ui/src/button.tsx:6`, `packages/ui/src/badge.tsx:6`.
- 근거: 별도 subpath가 CVA 정의를 소유하지 않고 `"use client"` 파일에서 함수를 재수출한다. 서버가 사용할 수 있는 순수 클래스 함수가 React client reference가 된다.
- 재현: 실제 manifest UI tgz를 설치한 Next 16.4.6의 server `app/page.js`에서 `import { buttonVariants } from '@kor-travel/ui/button-variants'` 후 `<a className={buttonVariants({variant:'outline'})}>…</a>`를 반환한다. `/badge`에서는 badgeVariants로 같은 동작을 한다.
- 실제: 두 route 모두 HTTP500. 오류는 `Attempted to call buttonVariants() from the server but buttonVariants is on the client` 및 badgeVariants 대응 오류. `<Button>…</Button>`를 server page에서 렌더한 `/control`은 HTTP200.
- 영향: Next 서버 페이지/서버 컴포넌트에서 링크·배지 클래스만 재사용하는 정상 소비 경로가 실패한다. 타입 검사는 이 client boundary 오류를 잡지 못한다.
- 권고: CVA 정의를 hook/`use client` 의존이 없는 실제 별도 모듈로 이동하고 Button/Badge가 그 모듈을 import하게 한다. 공개 variant subpath가 이 순수 정의를 직접 export하도록 한다. RSC에서 두 함수 호출과 component 렌더 대조군을 모두 시험한다.
- 근거 파일: evidence `next-button-page.js`, `next-badge-page.js`, `next-control-page.js`, `next-*-response.html`, `metadata.json`.

### A-P1-02 — forceMount된 비활성 지도 탭이 노출되고 작업 버튼도 접근 가능

- 출처: **부모 사전 공개 회귀**, A가 추가 재현. 상태: `OPEN`.
- 위치: `packages/ui/src/map-controls.tsx:160`, `packages/ui/map-controls.css:23`, `packages/ui/map-controls.css:48`.
- 근거: MapTabPanel이 Radix Content의 forceMount를 그대로 통과시키지만 CSS는 `[hidden]`만 숨긴다. forceMount Content는 inactive여도 hidden을 설정하지 않는다.
- 재현: 기본 `map`인 MapTabs에서 map panel에 forceMount와 작업 버튼을 넣고, list panel을 만든 뒤 `목록` 탭을 선택한다.
- 실제: map panel의 `data-state`는 inactive이나 hidden은 없고, 작업 버튼은 RTL role 조회에 남으며 Chromium `isVisible()`도 true다.
- 영향: 지도/목록 동시 노출·남은 높이 배분 오류·비활성 작업의 focus/접근성 트리 노출이 발생한다. 지도 인스턴스를 보존하려 forceMount를 쓰는 소비자의 탭 계약이 깨진다.
- 권고: mounted 상태와 표시 상태를 분리하고 inactive panel을 확실히 숨겨 tab 순서·접근성 트리에서 제외한다. 재활성화 때 지도 크기 갱신과 인스턴스 보존도 함께 확인한다.
- 근거: `adversarial.test.tsx`의 parent-disclosed map 시험, `probes-final.log`, `browser.log`, `browser.png`.

## 4. P2 finding

### A-P2-01 — Progress가 value를 Root에 전달하지 않고 max도 시각 계산에서 무시

- 출처: 독립 신규. 상태: `OPEN`.
- 위치: `packages/ui/src/progress.tsx:14`, `packages/ui/src/progress.tsx:18`, `packages/ui/src/progress.tsx:29`.
- 재현: `<Progress aria-label="진행" value={60} max={200}/>`.
- 실제: Root는 `data-state="indeterminate"`, `aria-valuemax="200"`이지만 `aria-valuenow`가 없다. Indicator transform은 `translateX(-40%)`로 60%를 그린다. 기대는 확정값 60/200, 즉 30%이다. max 기본값에서도 모든 유효 value가 접근성 값으로 전달되지 않는다.
- 영향: 보이는 진행량과 보조기술에 전달되는 진행 상태가 다르며, max가 100이 아니면 시각 진행률까지 틀린다.
- 권고: value를 Radix Root에 전달하고 유효한 max 기준으로 Indicator를 정규화한다. indeterminate와 0/완료/비100 max를 구분하는 계약 시험을 추가한다.

### A-P2-02 — 선택 불가로 바뀐 행이 bulk 작업 대상에 남고 UI에서 해제할 수 없음

- 출처: 독립 신규. 상태: `OPEN`.
- 위치: `packages/ui/src/virtual-table.tsx:540`, `packages/ui/src/virtual-table.tsx:564`, `packages/ui/src/virtual-table.tsx:582`.
- 재현: id a,b인 두 행을 전체 선택한다. 같은 id/data로 rerender하면서 enableRowSelection을 `row.original.id === 'b'`로 변경한다. renderBulkActions에서 전달된 row id를 표시한다.
- 실제: a 체크박스는 disabled가 되지만 bulk에는 a,b가 그대로 전달된다. 전체 선택 체크박스를 눌러 해제해도 b만 해제되고 a가 남는다(`PREDICATE_AFTER_CLEAR a`). a 체크박스 자체도 disabled이므로 화면에서 해제할 수 없다.
- 영향: 행 상태 갱신 후 사용자가 선택할 수 없는 항목이 작업 대상·선택 건수에 남는다. 서버 권한 우회를 입증한 것은 아니나, bulk 요청 대상이 화면의 선택 가능 정책과 달라진다.
- 권고: 선택 가능 predicate 변경 때 실제 유효 선택을 정리하거나, 최소한 bulk 전달 대상에서 getCanSelect가 false인 행을 제외하고 controlled selection 정리 규칙을 명시한다. 선택 불가 전환 후 전체 해제까지 시험한다.

### A-P2-03 — 본행과 상세행의 key namespace 충돌

- 출처: 독립 신규. 상태: `OPEN`.
- 위치: `packages/ui/src/virtual-table.tsx:1181`, `packages/ui/src/virtual-table.tsx:1184`; 실제 재사용 지점 `packages/ui/src/virtual-table.tsx:872`, `packages/ui/src/virtual-table.tsx:1214`.
- 재현: getRowId가 각각 `x`, `x:detail`인 서로 다른 행을 주고, 첫 행에서 상세를 반환한다.
- 실제: 본행 x의 상세 key와 두 번째 본행 key가 모두 `x:detail`이 되어 React duplicate-key 경고가 발생한다. virtualizer도 같은 키를 항목 식별/측정에 사용한다.
- 영향: 합법적인 불투명 id만으로 React 행 identity와 가상 항목의 높이 캐시가 충돌한다. 상세 열고 닫기/데이터 교체 때 잘못된 state 재사용·remount/행 누락 가능성이 생긴다. 실제 앱에서 데이터 손실이 발생했다고 주장하지 않는다.
- 권고: 본행과 상세행 모두 `JSON.stringify(['row', row.id])` / `JSON.stringify(['detail', row.id])` 같은 충돌 없는 태그 namespace를 사용한다. 접미사 문자열 단순 결합을 피한다.

### A-P2-04 — VirtualTable에 원 앱의 비-kt 토큰 클래스가 남아 공통 CSS로 생성되지 않음

- 출처: 독립 신규. 상태: `OPEN`.
- 위치: `packages/ui/src/virtual-table.tsx:311`, `packages/ui/src/virtual-table.tsx:378`, `packages/ui/src/virtual-table.tsx:574`, `packages/ui/src/virtual-table.tsx:917`; 제공되는 정본은 `packages/tokens/theme.css:8` 이후와 `packages/tokens/radix.css:7` 이후.
- 재현: 공통 tokens.css/theme.css/shadcn.css/radix.css와 Tailwind 기본 theme/utilities를 입력해 실제 클래스 생성을 요청한다. 앱 전용 alias는 추가하지 않는다.
- 실제: `bg-surface-subtle`, `hover:bg-surface-muted`, `text-text-secondary`, `focus-visible:outline-focus`, `bg-brand-tint`, `rounded-control`, `text-2xs`는 생성되지 않는다. 같은 입력에서 `bg-kt-surface-subtle`, `focus-visible:outline-kt-focus`는 생성된다.
- 영향: 문서대로 설치한 소비자에서 sticky header 배경·bulk 표시·정렬 버튼의 의미 색상/모서리/타입 스케일이 빠진다. focus outline 폭 자체는 남을 수 있으나 지정 focus 토큰 색은 적용되지 않는다. 원 앱에서 우연히 같은 alias를 선언한 경우에만 가려진다.
- 권고: VirtualTable을 `kt-` 공통 토큰 유틸리티로 정렬하거나 공통 bridge에서 해당 alias를 명시적으로 제공한다. 앱 전용 theme 없는 최소 소비자에서 생성 CSS와 sticky/focus 상태를 검증한다.
- 근거: `css.mjs`, `styles.css`. 이 문제는 아래 custom variants 누락과 별개의 **유틸리티 이름 불일치**다.

### A-P2-05 — 기본 TabsContent의 키보드 focus가 완전히 보이지 않음

- 출처: 독립 신규. 상태: `OPEN`.
- 위치: `packages/ui/src/tabs.tsx:88`; 관련 기준 `docs/standards/ux-guide.md:126`.
- 재현: 텍스트만 든 active TabsContent를 기본 스타일로 렌더하고 Tab 순서 또는 element.focus()로 panel에 포커스를 둔다.
- 실제: Radix는 panel에 tabindex=0을 주지만 wrapper는 outline-none을 지정하고 대체 focus 표시는 없다. 정상 tarball Chromium에서 activeElement가 panel인 상태의 computed outline은 none, boxShadow도 none이다.
- 영향: 탭 다음의 텍스트 panel로 이동한 키보드 사용자가 현재 focus 위치를 볼 수 없다. common의 불투명 2px focus 링 계약에도 맞지 않는다.
- 권고: focus-visible에 즉시 표시되는 공통 토큰 outline을 제공하거나, 동등한 focus 표면을 보장하도록 tabindex/focus 설계를 바꾼다. 텍스트 전용 panel을 실제 Tab으로 탐색하는 시험이 필요하다.

### A-P2-06 — Tabs orientation이 Radix Root에 전달되지 않음

- 출처: **부모 사전 공개 회귀**, A가 추가 재현. 상태: `OPEN`.
- 위치: `packages/ui/src/tabs.tsx:15`, `packages/ui/src/tabs.tsx:19`.
- 재현: `<Tabs orientation="vertical">`로 TabsList/Trigger 두 개를 렌더한다.
- 실제: tablist aria-orientation은 horizontal이다. wrapper는 orientation을 destructure하여 CSS용 data-orientation만 주고 Root의 실제 orientation prop은 누락한다.
- 영향: 세로 배치와 보조기술·방향키 탐색 축이 불일치한다.
- 권고: orientation을 Radix Root에 실제 전달하고 vertical에서 ArrowUp/ArrowDown, horizontal에서 ArrowLeft/ArrowRight 동작을 함께 시험한다.

### A-P2-07 — shadcn custom variants가 공통 CSS 계약에 포함되지 않음

- 출처: **부모 사전 공개 회귀**. 해당 속성/선택자 불일치는 부모 전달 전에도 소스에서 관찰했으나, 최종 원인인 shadcn custom variants 누락은 부모 공개 내용을 반영해 분류했다. 상태: `OPEN`.
- 위치: `packages/tokens/radix.css:4`, `packages/ui/src/switch.tsx:24`, `packages/ui/src/switch.tsx:31`, `packages/ui/src/tabs.tsx:72`, `packages/ui/src/separator.tsx:24`.
- 근거: Radix 런타임은 data-state/data-orientation 속성을 내보낸다. 부품은 data-checked/data-active/data-horizontal 등의 custom variant를 쓰지만, 현 bridge에는 이를 Radix 속성에 연결하는 정의/import가 없다.
- 재현: 문서의 common theme/radix import만 제공한 tarball 소비자에서 Switch를 on/off하고 Tabs를 전환한다.
- 실제: Switch의 aria-checked는 true/false로 바뀌어도 track 배경은 동일하고 thumb의 translate/transform은 전후 모두 none이다. Tabs active 선택자와 Separator 방향 크기 등도 같은 종류의 의존성이 있다.
- 영향: checked/active 상태의 시각 표시와 방향 레이아웃이 앱의 기존 shadcn import 유무에 따라 달라진다. 이 ARIA 값 자체가 틀렸다는 뜻은 아니다.
- 권고: 필요한 custom variant 정의를 정식 공통 CSS 산출물로 포함하고 출처를 보존하거나, 모든 부품을 Radix data-state/data-orientation에 직접 대응시킨다. 기존 앱의 우연한 import에 의존하지 않는 소비자 시험을 추가한다.

## 5. P3 finding

### A-P3-01 — 신규 벤더 부품의 공백 행에 trailing whitespace가 남음

- 출처: 독립 신규. 상태: `OPEN`.
- 위치 예: `packages/ui/src/accordion.tsx:62`, `packages/ui/src/checkbox.tsx:37`, `packages/ui/src/dialog.tsx:92`, `packages/ui/src/select.tsx:65`.
- 재현: `git diff --check c289b4624c8640eb918cc915803e72ae754e58fb 789e6d2e179a055b3cd793fb886083543244089c`.
- 실제: 다수 trailing whitespace 진단, exit 2.
- 영향: 비기능 품질 문제이나 저장소가 요구하는 diff-check 검증을 통과하지 않는다. 브라우저 기능 결함으로 과장하지 않는다.
- 권고: 이 변경에서 추가된 빈 아이콘 prop 행의 공백을 제거하고 diff-check를 다시 실행한다.
- 전체 위치: `kor-travel-common-diff-check.log`.

## 6. 남은 범위와 판정 경계

- **common merge: BLOCK.** P1 두 건은 post-fix immutable commit에서 원 reviewer 재확인이 필요하다. P2/P3를 연기하려면 저장소 규칙의 owner·task·gate·기한이 필요하며, 이 raw report 자체에서 연기 승인하지 않았다.
- **지도 원본 delta 자체: 검토 범위에서 새 finding 없음.** ES2022 target/정확 의존성 변경의 type/build와 정상 tarball ESM 소비는 확인했다. 이것이 전체 지도 동작 수용 판정은 아니다.
- 지도 RN21/마커 Chromium17/tarball17은 부모 manifest 제출 증거이며 본 리뷰가 17개 시나리오를 재실행하지는 않았다. 실제 WebGL 지도 생성·외부 타일·VWorld 네트워크·키·운영 배포는 `NOT_RUN(이번 공통 소스 리뷰 범위 밖)`이다.
- 모든 소비 앱의 6폭·다크·coarse pointer·스크린리더 실제 낭독·공개 로그인/API·최종 앱 tarball 채택 상태는 `NOT_RUN(후속 앱 manifest에서 별도 review)`이다.
- VirtualTable의 wheel scroll로 현재 focused 가상 행이 범위 밖으로 사라지면 focus가 body로 돌아가는 것도 Chromium에서 관찰했다. 가상화 focus 보존 정책/소비자 탐색 계약이 이번 문서에 명확하지 않아 별도 확정 finding으로 올리지 않았으나, 후속 virtualized 화면에서 검사할 항목으로 남긴다.
- Doctor, SPDX, 링크 검사와 원격 CI를 본 리뷰가 새로 실행했다고 주장하지 않는다. 해당 결과는 manifest의 부모 증거이고 위 직접 실행 표에 없는 gate는 독립 PASS로 세지 않았다.
- 부모가 준비 중인 수정은 이 report에서 FIXED로 처리하지 않았다. 새 delta manifest/commit으로 자신의 finding과 전체 delta 회귀를 다시 검토해야 한다.

## 7. 재현 evidence와 환경 정리

영구 evidence 디렉터리: `/home/digitie/dev/common-unification-20261111/review-A-common-evidence-1/`.

- `manifest.json`, `metadata.json`, `artifact-validation.json`: 입력 원문·종료 HEAD/clean·실제 hash와 dist 비교.
- `adversarial.test.tsx`, `vitest.config.mjs`, `probes-final.log`: 추가 8개 공격 시험 원문과 실패/성공 관찰.
- `css.mjs`, `styles.css`: 공통 토큰만의 실제 Tailwind 생성 입력/결과.
- `browser.tsx`, `browser-check.mjs`, `browser.log`, `browser.png`: 실제 pack 소비자와 Chromium 관찰.
- `source-path-harness-failure.log`: 첫 harness 경로 구성 실패 원문. 정상 설치 성공 로그와 구분한다.
- `consumer-package.json`, `consumer-package-lock.json`, `next-*-page.js`, `next-*-response.html`: Next 두 실패와 HTTP200 대조군 재현 입력/응답.
- `python-340.log`, `*-diff-check.log`: 전체340 실행 결과 및 diff-check 원문.

재현하려면 위 두 고정 commit에 detached worktree를 만들고 잠긴 의존성을 설치한다. 현 evidence의 vitest config는 `/tmp/review-A-common-789e6d2` 및 `/tmp/review-A-probes`를 사용하므로 다른 위치에서는 해당 절대 경로만 조정한다. 실행 예: `node /tmp/review-A-common-789e6d2/node_modules/vitest/vitest.mjs run --config /tmp/review-A-probes/vitest.config.mjs`.

독립 시험용 51873/51874/51875 서버는 PID의 cwd가 본 리뷰용 임시 디렉터리인지 대조한 뒤 종료했다. 구현 checkout·운영 서비스·실제 앱은 수정/배포하지 않았다. 두 detached 기준선은 clean 상태로 후속 재현을 위해 보존했다(아직 merge/abandon 단계 아님).
