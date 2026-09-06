# 횡단 비교 — Admin UI 컴포넌트 계약 심층 비교

작성일: 2026-09-06 · 조사 성격: 읽기 전용(대상 저장소 무수정) · 산출 위치: `docs/survey/cross/ui-components.md`

이 문서는 kor-travel 계열 admin 프런트엔드 7곳의 UI 컴포넌트를 **파일 단위**로 비교해, `kor-travel-common` UI 패키지의 1차/2차/보류 범위, 프리미티브 엔진, 배포(등록) 방식의 결정 근거를 모은다. 표기 규칙: **사실**(파일에서 직접 확인) / **후보**(설계 선택지) / **추정**(정황 근거, 직접 확인 안 함) / **미확인**(확인하지 못함).

---

## 0. 기준(조사 커밋)

| 저장소 | 로컬 경로 | 커밋 | 비고 |
|---|---|---|---|
| kor-travel-map (map) | `F:/dev/kor-travel-common-survey/ktm-main` | `c494e227` | `packages/kor-travel-map-admin/frontend` |
| pinvi | `F:/dev/kor-travel-common-survey/pinvi` | `9af25e5` (main) | `apps/web` (admin + 사용자 UI 공존) |
| kor-travel-geo (geo) | `F:/dev/kor-travel-geo-fixes` | `1d9d74d` (main) | `kor-travel-geo-ui` |
| kor-travel-concierge (concierge) | `F:/dev/kor-travel-concierge` | `7945305` (main) | `frontend` |
| kor-travel-airport main (airport) | `F:/dev/kor-travel-common-survey/kta-main` | `2bb1111` | `frontend` — Tailwind/shadcn 없음 |
| kor-travel-airport WIP | `F:/dev/kor-travel-airport` | `99b3f98` (`codex/shadcn-ui-foundation`) | 읽기 전용. main 대비 `frontend/src/components/ui/button.tsx` 등 8파일 추가/변경(`git diff --stat 2bb1111 99b3f98 -- frontend`) |
| kor-travel-docker-manager (ktdm) | `F:/dev/kor-travel-common-survey/ktdm-main` | `862562d` | `frontend` |
| kor-travel-weather (weather) | `F:/dev/kor-travel-weather` | `6003da9` (main) | `packages/kor-travel-weather-admin/frontend` |
| 선행 보고서 | `F:/dev/kor-travel-geo-fixes/docs/kor-travel-common-library-review.md` | 2026-09-05 | §3.1~3.4, §7.2~7.3를 재검증 대상으로 삼음 |

---

## 1. 방법

실행한 명령(모두 읽기 전용):

- 파일 목록·줄 수: `ls`, `find -maxdepth 2 -type f`, `wc -l` — 8개 `ui` 디렉터리와 8개 앱 레벨 `components` 디렉터리.
- 동일성: `diff -q` (바이트 동일 여부) → 27쌍 모두 상이. 이어서 **정규화 diff**(`sed`로 행끝 세미콜론 제거·따옴표 통일·앞뒤 공백/끝 콤마 제거 후 `diff`, 그리고 주석 행 제외 `diff -w`)로 포맷 차이를 걷어낸 **의미 차이 줄 수**를 셌다(아래 표의 "정규화 diff").
- 프리미티브 엔진: `rg -n "from ['\"]radix-ui"`, `rg -l '@base-ui'`, `rg -n "asChild"`, `rg -n '\brender=\{'`, `rg -n nativeButton`.
- 소비처 계수: `rg -l "components/ui/<name>['\"]"` (테스트 파일 제외) — 앱별 import 파일 수.
- 설치 버전: 각 `package-lock.json`에서 `"node_modules/<pkg>": {` 다음 `version`을 읽음(`grep -A3`). pinvi는 루트 lock에 tailwind 3.4.19(모바일 NativeWind용)와 `apps/web/node_modules/tailwindcss` 4.3.3이 공존함을 확인.
- 토큰 정의: 각 `globals.css`에서 `--spacing-control`, `--radius-control/panel`, `--text-2xs`, `--color-*` 이름을 `grep`.
- 테스트: `find -name '*.test.tsx'` + `rg -l "AdminTable|VirtualTable"` (테스트/e2e 파일).
- 읽은 파일(전문): map/pinvi/geo/concierge/airport-WIP `button.tsx`·`button-variants.ts`, pinvi `ui/Button.tsx`, map/pinvi/concierge `table.tsx`, geo `VirtualTable.tsx`, map `data-table.tsx`(전문) 및 map↔pinvi `data-table.tsx` 정규화 diff 전문, map/pinvi `status-badge*.ts(x)`, map/pinvi/geo `badge-variants.ts`, concierge `badge.tsx`, map `checkbox.tsx`, pinvi `AdminTable.tsx`(1–140행)·`DataTable.tsx`·`admin-shell-parts.tsx`·`AdminPage.tsx`, map `admin-shell.tsx`(1–140행 + 시그니처), 각 `components.json`, 각 `package.json`(의존 발췌), 선행 보고서 §3.1–3.4·§7.1–7.3·§12 인용 목록. 그 외 파일은 `grep`으로 import·export·props 시그니처만 추출했다(본문에 "시그니처만 확인"으로 표기).

---

## 2. §1 컴포넌트 × 앱 매트릭스

범례: **동일** = 바이트 동일, **유사** = 정규화 diff가 import 경로·색 토큰 치환·주석에 그침(계약 동일), **상이** = props/엔진/동작 계약이 다름, **없음** = 대응 파일 없음. 괄호는 줄 수. "정규화 diff"는 map↔pinvi admin 기준.

### 2.1 shadcn 계열 primitive (map↔pinvi 27쌍 전수 + geo·concierge·airport)

| 파일 | map | pinvi admin | 정규화 diff | 판정(map↔pinvi) | geo | concierge | airport WIP |
|---|---|---|---|---|---|---|---|
| alert-dialog.tsx | 110 | 120 | 54 | 유사(+`data-pv-surface`, `items-start`, `bg-scrim/50`, `duration-normal`) | 160 (radix; `Portal/Overlay/Action/Cancel` export) — 상이 | 109 (base-ui) — 유사 | 없음 |
| alert.tsx | 116 | 123 | 41 | 유사 | 68 — 상이(`AlertActions` 없음) | 없음 | 없음 |
| badge-variants.ts | 44 | 60 | 52 | 유사(토큰 치환, `default`가 `bg-cta`) | 23 — **상이**(variant 축이 `tone`: neutral/brand/ok/warn/error/info) | badge.tsx 내 inline cva — 유사(10 variant 동일) | 없음 |
| badge.tsx | 39 | 42 | 53 | **상이**(base-ui `useRender`+`render` prop → 순수 `<span>`) | 21 (순수 span, `tone`) | 54 (`useRender`) | 없음 |
| breadcrumb.tsx | 98 | 110 | 72 | 유사(map은 `useRender`; pinvi는 `render` prop을 `BreadcrumbLink`에 자체 구현 — 미확인 세부) | 없음 | 없음 | 없음 |
| button-variants.ts | 86 | 110 | 66 | 유사(토큰 치환; `default`=`bg-cta`) | 41 — 유사(클래스 문자열 map과 동일 계열) | button.tsx 내 inline — 유사(`destructive`에 `aria-expanded:` 누락만 다름) | button.tsx 내 inline — **상이**(shadcn 기본 레시피) |
| button.tsx | 110 | 129 | 60 | **상이**(§3.1) | 33 — **상이** | 115 — 유사(map과 동일 구조) | 57 — **상이** |
| card.tsx | 134 | 130 | 58 | 유사 | 110 — 유사(동일 7개 서브컴포넌트) | 110 — 유사 | 없음 |
| checkbox.tsx | 51 | 94 | 102 | **상이**(base-ui Root/Indicator → native `<input type=checkbox>`+`forwardRef`, `onCheckedChange(boolean)`) | 36 (radix) | 31 (base-ui) | 없음 |
| data-table.tsx | 799 (+test 175) | 853 | 155 | **상이**(계약 확장, §3.3) | `VirtualTable.tsx` 409 — **상이** | 없음(도메인 `review/CandidateTable.tsx` 344) | 없음 |
| dialog.tsx | 135 | 192 | 106 | **상이**(+`hasUnsavedInput`, `viewportProps`, `data-pv-surface`) | 142 (radix; `Portal/Overlay` export) — 상이 | 116 (base-ui; Root/Trigger/Close 재수출) — 유사 | 없음 |
| field-variants.ts | 10 | 14 | 17 | 유사 | 없음 | 5 | 없음 |
| field.tsx | 265 | 272 | 75 | 유사(11개 서브컴포넌트 동일) | 224 — 유사(`FieldMessage` 없음) | 241 — 유사(`FieldMessage` 없음) | 없음 |
| form-field-input.tsx | 99 (+test 51) | 100 | 25 | 유사 | 없음 | 없음 | 없음 |
| form-field-shared.ts / form-field.ts | 59 / 6 | 64 / 12 | 15 / 18 | 유사 | 없음 | 없음 | 없음 |
| form-select.tsx / form-textarea.tsx | 94 / 93 | 94 / 93 | 22 / 24 | 유사 | 없음 | 없음 | 없음 |
| input.tsx | 38 | 53 | 32 | **상이**(base-ui `Input` → native `<input>`; 클래스 동일 계열) | 31 (native, `size` variant) | 32 (base-ui) | 없음 |
| native-select(-option).tsx | 56 / 20 | 66 / 26 | 36 / 22 | 유사 | 51 (`forwardRef`) — 유사 | `select.tsx` 331 안에 `NativeSelect` + base-ui `Select` — 상이 | 없음 |
| popover.tsx | 64 | 75 | 31 | 유사(+`data-pv-surface`) | 46 (radix) | 40 (base-ui) | 없음 |
| separator.tsx | 27 | 45 | 40 | **상이**(base-ui → `<div role=separator aria-orientation>`) | 28 (radix) | 25 (base-ui) | 없음 |
| skeleton.tsx | 27 | 41 | 17 | 유사 | 16 | 없음 | 없음 |
| sonner.tsx | 76 | 없음 (pinvi에 토스트 시스템 없음 — `copy-button.tsx` 6행 주석) | — | 없음 | `toaster.tsx` 62 (radix `Toast` + zustand `@/lib/toast`) | 없음 | 없음 |
| table.tsx | 137 | 184 | 96 | **상이**(+`containerStyle`, `containerTestId`, `TableHeader sticky`, `scope="col"` 기본, hover는 `data-clickable` 행에만, 선택 열 셀렉터 `[data-slot=checkbox]`) | 없음(`VirtualTable`이 `.table` CSS 직접 렌더) | 117 — 유사(카드 내 flush 규칙 없음, `ktc-scroll-cue`) | 없음 |
| tabs.tsx / tabs-variants.ts | 105 / 26 | 없음 | — | pinvi admin은 Tabs 미사용(0 파일) | 69 (radix `Content/Trigger`) — 상이 | 84 (base-ui `Tab/Panel`) — 유사 | 없음 |
| textarea.tsx | 26 | 39 | 24 | 유사 | 없음 | 22 | 없음 |
| tooltip.tsx | 63 | 74 | 45 | 유사(+`data-pv-surface`) | 55 (radix) | 없음 | 없음 |
| help-tip.tsx | `components/help-tip.tsx` 70 | `admin/ui/help-tip.tsx` 87 | 41 | 유사(pinvi는 ui/ 하위로 이동) | `admin/shared/HelpTip.tsx` 39 (radix Popover, `asChild`) | `HelpTip.tsx` 42 (base-ui Popover) | 없음 |
| geo 전용 ui | — | — | — | — | collapsible 28, label 24, progress 32, JsonBlock 56, PageHeader 59, Panel 49, StatusBadge 23 | — | — |
| concierge 전용 ui | — | — | — | — | — | select 331, switch 26, label 20 | — |

사실: map `ui` 디렉터리는 32파일(테스트 2 포함, 3,239줄), pinvi admin `ui`는 28파일(3,302줄), 같은 이름 27쌍, 바이트 동일 0 — 선행 보고서 §3.1의 수치(30/28/27/0)와 일치한다. 정규화 후에도 27쌍 모두 차이가 남으며, 그중 8쌍(badge, button, checkbox, data-table, dialog, input, separator, table)은 **계약 차이**이고 나머지는 import 경로·색 토큰·주석 차이다.

사실: pinvi admin `ui` 28파일 전부가 파일 상단에 "KTM …에서 이식(T-356)" 및 "원문에서 바꾼 부분" 주석을 갖는다(`rg -c "pinvi 추가|원문에서 바꾼|이식\(T-"`: 모든 파일 ≥1). 즉 pinvi admin UI는 map의 **소스 복사본**이며, 색 토큰 치환표와 엔진 축소(base-ui는 overlay에만)라는 두 규칙으로 갈라졌다.

### 2.2 앱 레벨 공유 컴포넌트

| 컴포넌트 | map | pinvi | 정규화 diff | geo | concierge | ktdm | weather |
|---|---|---|---|---|---|---|---|
| admin-shell | `admin-shell.tsx` 510 (`AdminShell` title/description/section/breadcrumbs/help/meta/actions + NAV_GROUPS 정본 + rail 접힘 + 로그아웃) | `admin-shell-parts.tsx` 224 (`AdminSkipLink`/`AdminPageHeader`/`AdminRailGrid`만 이식; nav는 `app/(admin)/admin/layout.tsx` 소유) + `AdminPage.tsx` 91 (`AdminPage`/`FilterBar`/`Section` 어댑터, 39 소비처) | 부분 이식 | `layout/AppShell.tsx` 347 (`{children}`만; nav는 `lib/admin-pages`) + `ui/PageHeader.tsx` 59 (title/description/actions/section/meta) | `AppShell.tsx` 360 (title/description/actions/children/contentClassName/viewportLocked) | `layout/AppShell.tsx` 259 (title/description/section/meta/actions + 콜백 7개: onLogout/onOpen* ) | `admin-shell.tsx` 152 (`AdminShell {children}` + `PageHeader` title/description/section/actions) |
| filter-bar | 67 (`FilterBar`/`FilterField`/`FilterActions`) | 77 | 26 (유사) | 없음 | 없음(미확인) | 없음 | 없음 |
| pagination-bar | 290 (`OffsetPager`/`CursorPager`) | 298 | 46 (유사) | 없음(1파일 언급) | 없음(도메인 내 3파일 언급) | 없음 | 없음 |
| status-badge(+variants) | 111 + 21 (`StatusBadge`/`LevelBadge`/`SeverityBadge`/`HttpStatusBadge`/`LiveBadge`; tone 5종 ← `lib/status-label`) | 114 + 33 | 48 + 20 (유사; 경로만) | `ui/StatusBadge.tsx` 23 (`value`, `tone: ok\|warn\|error` ← `lib/consistency.severityClass`) — 상이 | `review/CandidateTable.tsx` 내부(시그니처 미확인) | 없음 | 없음 |
| empty-state | 63 (icon/title/description/action/framed/size) | 72 | 21 (유사) | `admin/shared/EmptyState.tsx` 14 — 상이(축소) | 없음(문자열 참조 6파일; 컴포넌트 파일 없음) | 없음 | 없음 |
| section-card | 62 (title/description/actions/footer/size/headingLevel/className/contentClassName) | 69 | 18 (유사) | `ui/Panel.tsx` 49 (title:string/description/actions/className) — 유사 | `SectionCard.tsx` 44 — **props 동일** | 없음 | 없음 |
| stat-strip | 146 (items[label/value/unit/caption/tone(StatusTone)/href/loading/help/testId], isLoading/size/framed/ariaLabel) | 166 | 59 (유사; `TONE_DOT` 토큰) | 없음(`MetricTile` 25) | `StatStrip.tsx` 117 — 유사(loading/testId 없음, tone 로컬 타입) | `StatStrip.tsx` 95 — 상이(tone `ok\|warn\|danger\|info\|neutral`, `title`) | 없음 |
| copy-button | 87 (`value`/`label`; 복사 후 `sonner` toast) | 131 (sonner 제거 → inline 상태 copied/error/unsupported + `TriangleAlertIcon`) | 95 (**상이**: 피드백 채널) | clipboard 인라인 3파일 | `CopyButton.tsx` 54 (`text`/`label`/`copiedLabel`/`size`; `Button` 사용) — 상이 | `CopyableCommand.tsx` 56 — 상이 | 없음 |
| json-viewer | 73 (value/maxHeight/tone/copyable) | 93 | 35 (유사) | `JsonBlock.tsx` 56 (`{value}`) + `admin/shared/JsonDetails.tsx` 49 — 상이 | 없음(`<pre>` 6파일) | 없음 | 없음 |
| detail-list | 122 (items[label/value/mono/copyable/href/help/numeric], columns/layout) | 137 | 40 (유사) | `admin/shared/KeyValueGrid.tsx` 39 — 상이 | `detail.tsx` 32 (`DetailSection`/`DetailRow` label/value:string) — 상이 | 없음 | 없음 |
| help-tip | 70 | 87 | 41 (유사) | 39 | 42 | 없음 | 없음 |
| confirm-dialog | 180 (`ConfirmDialogProvider` + `useConfirm()` → `Promise<boolean>`; `confirmLabel`에 generic 라벨("확인" 등) 타입 차단) | `ui/ConfirmDialog.tsx` 137 (제어형 props open/onConfirm/onCancel/tone/busy/returnFocusRef; `createPortal`+`useModalDialog`) | 267 (**전면 상이**) | `admin/shared/ConfirmActionDialog.tsx` 84 (trigger `asChild` + `RoleRequirementNote`) | `ConfirmActionButton.tsx` 69 (trigger + AlertDialog, onConfirm) | 없음 | 없음 |
| login-form | 138 (`nextPath`; `fetch /api/auth/login`; Button/Input; `clearDomainIdempotencyKeys`) | 없음(admin 로그인 화면 미확인) | — | `auth/LoginForm.tsx` 96 (`nextPath`; 순수 CSS `.login-form`) | `LoginForm.tsx` 112 (props 없음; `useSearchParams`+`router.replace`; Button/Field/Input) | `LoginScreen.tsx` 93 (`onLogin` 콜백; `postJson`; `ops-*` CSS) | `auth/LoginForm.tsx` 103 (`nextPath`; `sanitizeLocalPath`; 순수 CSS) |
| app-error-panel | 110 (`error`/`reset?`/`standalone?`) | 없음(`feedback/RouteError.tsx` 76, 시그니처 미확인) | — | `layout/AppErrorPanel.tsx` 87 — **props 동일** | `layout/AppErrorPanel.tsx` 112 — 타입은 동일하나 함수 인자에서 `standalone` 미사용 | `layout/AppErrorPanel.tsx` 103 — props 동일 | 없음 |
| selectable-row | 246 (+test 81; `role=option` 그룹, 단일 tab stop) | 없음 | — | `role="option"` 1파일(동등성 미확인) | 없음 | 없음 | 없음 |
| entity-link | 74 (+test 85; `hrefFor(kind,id)` 도메인 라우팅) | 없음 | — | 없음 | 없음 | 없음 | 없음 |
| multi-filter-combobox | 268 | 없음 | — | listbox 1파일(미확인) | 없음 | 없음 | 없음 |
| vworld-map-view | 1858 (`VWorldMapView`/`VWorldMarker`/`VWorldServerClusters`/`VWorldFeatureClusters`; `maplibre-gl` 5.24 직접) | `map/vworldPrimitives.tsx` 97 (재수출) + `MapView` 173/`FeatureMapView` 913/`TripMapView` 589; `vworld-map-core`는 `file:../mobile/vendor/vworld-map-core-1.0.0.tgz` | — | `vworld/CoordinateMap.tsx` 421 (`maplibre-vworld-react` GitHub tarball — **유일한 소비자**) | `VWorldMap.tsx` 316 (`maplibre-gl` **6.0** 직접) | 없음 | `vworld-map-view.tsx` 636 (`useVWorldMap`/`VWorldMapView`/`VWorldMarker`/`VWorldWeatherMarker`/`VWorldWeatherClusters`) + `weather-map.tsx` 500 |

### 2.3 스택·버전 매트릭스(설치 버전은 lockfile 기준)

| 항목 | map | pinvi web | geo | concierge | airport WIP | airport main | ktdm | weather admin |
|---|---|---|---|---|---|---|---|---|
| react | 19.2.8 | 19.2.6 | **18.3.1** | 19.2.8 | 19.2.8 | ^19.2.8(선언) | **18.3.1** | 19.2.8 |
| next | 16.2.12 | 16.3.3 | 16.2.12 | 16.2.7 | 16.3.2 | ^16.3.2 | **14.2.35** | **15.5.24** |
| tailwindcss | 4.3.3 | 4.3.3 (`apps/web/node_modules`; 루트 3.4.19는 모바일) | 4.3.1 | 4.3.1 | 4.3.3 | 없음 | 4.3.1 | **없음**(순수 CSS 2,334줄) |
| primitive 엔진 | `@base-ui/react` 1.6.0 | `@base-ui/react` 1.8.0 (overlay만) | `radix-ui` 1.6.0 | `@base-ui/react` 1.5.0 | `@base-ui/react` 1.8.0 | 없음 | 없음 | 없음 |
| cva / cn | 0.7.1 / clsx+tailwind-merge (`@/lib/utils`) | 0.7.1 / `@/lib/admin/cn` | 0.7.1 / `@/lib/utils` | 0.7.1 / `@/lib/utils` | 0.7.1 / **npm `cn@0.2.5`** (clsx·tailwind-merge 미설치, `lib/utils.ts`가 재수출) | — | 없음 | 없음 |
| lucide-react | 1.27.0 | 0.460.0 | 0.468.0 | 1.17.0 | 1.41.0 | — | 0.363.0 | 0.468.0 |
| @tanstack/react-table / -virtual | 8.21.3 / 3.14.8 | 8.21.3 / 3.14.10 | 8.21.3 / 3.14.3 | 없음 | 없음 | 없음 | 없음 | 없음 |
| shadcn CLI(dep) | 없음 | 없음 | 없음 | 4.10.0 | 4.21.0 | — | — | — |
| components.json style | `base-nova` | **없음** | `radix-nova` | `base-nova` | `base-nova` | 없음 | 없음 | 없음 |
| typescript | 5.9.3 | 5.9.3 | 5.9.3 | 5.9.3 | **7.0.2** | ^7.0.2 | 5.9.3 | 5.9.3 |
| `noUncheckedIndexedAccess` | 없음 | **true**(`tsconfig.base.json`) | 없음 | 없음 | 없음 | — | — | — |
| 디자인 문서 | `frontend/design.md` 302줄 + `docs/architecture/admin-frontend-design-rules.md` | `DESIGN.md` 451줄 | (map 동기화 기록 `docs/resume.md`) | 없음 | 없음 | — | — | — |
| "Hallmark ·" 마커 파일 수 | 88 | 39 | 1 | 2 | 0 | — | — | — |

사실: React 18(geo, ktdm) 과 19(그 외)가 공존하고, Next는 14/15/16이 공존한다. `@base-ui/react` 1.6.0의 peerDependencies는 `react ^17 || ^18 || ^19`(map lock)이므로 geo가 React 18을 유지한 채 base-ui를 채택하는 것은 peer 관점에서 가능하다(사실). 단 `forwardRef` 없이 ref를 props로 받는 map식 컴포넌트 작성은 React 19 전제이므로 React 18 소비자는 `forwardRef` 래핑이 필요하다(추정 — geo `button.tsx` 7–8행 주석이 같은 이유로 `forwardRef`를 명시).

---

## 3. §2 컴포넌트별 계약 차이와 통합 시 회귀 위험

### 3.1 Button — 선행 §3.3 재검증·확장

| 구현 | 요소/엔진 | ref | `type` 기본 | `loading` 의미 | `disabled` 의미 | 합성(`asChild`/`render`) | variant 축 | size 축 | 근거 |
|---|---|---|---|---|---|---|---|---|---|
| geo `ui/button.tsx` | `radix-ui` `Slot.Root` 또는 `<button>` | `React.forwardRef`(React 18) | 없음 → 네이티브 **submit** | **없음** | 네이티브 `disabled`(레시피는 `disabled:`/`aria-disabled:` 두 벌 유지) | `asChild` | default/outline/secondary/ghost/destructive/destructive-solid/link | default/sm/xs/lg/icon/icon-sm/icon-xs/icon-lg | `components/ui/button.tsx` 9–31, `button-variants.ts` 3–39 |
| map `ui/button.tsx` | `@base-ui/react/button` `ButtonPrimitive` | 없음(React 19 ref prop, base-ui가 전달) | base-ui가 `type="button"` 부여(pinvi 주석 13–15행 근거; base-ui 소스 직접 미확인) | `aria-disabled`+`aria-busy`+spinner, **native disabled 안 걺**(포커스 유지), `onClick`을 `blockBusyActivation`으로 교체(`preventDefault`로 submit 차단) | `nativeDisabled = disabled && !loading`; `disabledReason` → `title` | base-ui `render` prop(호출부 3줄/2파일), `nativeButton` 2건 | 동일 7종 | 동일 8종(xs/lg/icon-xs/icon-lg는 `@deprecated` alias) | `button.tsx` 21–107, `button-variants.ts` 35–84 |
| pinvi admin `admin/ui/button.tsx` | native `<button>` | `React.forwardRef` | **`type='button'` 명시 기본** | map과 동일 | map과 동일 | **없음**(링크 버튼은 `<a className={buttonVariants()}>`) | 동일 7종(`default`=`bg-cta`) | 동일 8종 | `button.tsx` 3–19(변경 사유), 69–126 |
| pinvi 사용자 `ui/Button.tsx` | native `<button>` + `ButtonLink`(next/link) | `forwardRef` | `type='button'` | `disabled={disabled \|\| loading}` → **native disabled**(포커스 손실 허용), `aria-busy` | 위와 동일 | 없음(`ButtonLink` 별도) | primary/secondary/ghost/danger | md(44px)/sm/lg | `Button.tsx` 24–115 |
| concierge `ui/button.tsx` | `@base-ui/react/button` | 없음 | base-ui 기본 | map과 동일 | map과 동일 | base-ui `render`(호출부 9줄/7파일) | 동일 7종(`destructive`에 `aria-expanded:` 없음) | 동일 8종 | `button.tsx` 8–112 |
| airport WIP `ui/button.tsx` | `@base-ui/react/button` | 없음 | base-ui 기본 | **없음** | `disabled:pointer-events-none disabled:opacity-50`(title 도달 불가) | base-ui `render` | default/outline/secondary/ghost/destructive/link(**destructive-solid 없음**) | default(h-8)/xs/sm/lg/icon/icon-xs/icon-sm/icon-lg — 높이 4단계 | `button.tsx` 5–55 |

선행 보고서와의 차이: (1) geo의 Slot은 `@radix-ui/react-slot`이 아니라 통합 패키지 `radix-ui`에서 온다(사실; `rg "@radix-ui/"`는 lockfile만 히트). (2) pinvi에는 Button 계약이 **두 벌**(admin 23 소비 파일, 사용자 UI 29 소비 파일)이며, `loading` 시 포커스 처리가 서로 반대다 — 선행 보고서는 admin 쪽만 다뤘다. (3) concierge는 map과 사실상 같은 계약이라 "map 계열"로 묶을 수 있고, airport WIP는 shadcn 기본 레시피라 세 번째 계열이다.

회귀 위험(통합 시):

| 위험 | 영향 앱 | 근거 |
|---|---|---|
| `type` 기본이 submit으로 돌아가면 폼 안 보조 버튼이 제출을 일으킴 | pinvi(두 Button 모두 `'button'` 명시), geo(현재 submit 기본에 의존하는 호출부 존재 가능 — 미확인) | pinvi `admin/ui/button.tsx` 13–15 |
| `loading` 중 native `disabled`를 걸면 포커스가 body로 이탈 → map/pinvi admin/concierge의 "방금 누른 위치 유지" 동작 상실 | map·pinvi admin·concierge | map `button.tsx` 35–41, 64–67 |
| `loading` 중 native `disabled`를 안 걸면 pinvi 사용자 UI가 기대하는 "클릭 완전 차단(disabled)" 셀렉터·테스트가 깨질 수 있음 | pinvi 사용자 UI | `ui/Button.tsx` 99–101 |
| `asChild` 제거 시 geo 호출부 12곳(`<Button asChild>`)이 `render`로 바뀌어야 함 | geo | §5 계수 |
| root `opacity`로 disabled를 흐리면 포커스 링 대비가 3:1 미만으로 떨어진다는 map 설계 제약과 airport WIP 레시피(`disabled:opacity-50`) 충돌 | airport | map `button-variants.ts` 15–20 vs airport `button.tsx` 6 |
| `destructive-solid`/`secondary` tint 경계(`border-brand`) 등 variant 의미가 airport에는 없음 | airport | airport `button.tsx` 9–19 |

### 3.2 Table primitive(`table.tsx`)

| 항목 | map | pinvi admin | concierge |
|---|---|---|---|
| 컨테이너 | `div[data-slot=table-container]` + `containerClassName` | + `containerStyle`, `containerTestId`(e2e가 실제 스크롤 요소를 잡음) | + `ktc-scroll-cue` 클래스 |
| Card 내부 flush | `group-data-[slot=card]/card:*` 로 테두리 제거 | 동일 | **없음** |
| 헤더 고정 | 가상화 경로에서만 sticky | `TableHeader sticky` prop(가상화와 독립) | 없음 |
| `th scope` | 미지정 | `scope="col"` 기본 | 미지정 |
| 행 hover | 모든 행 | `data-[clickable]` 행만 | 모든 행 |
| 선택 열 패딩 셀렉터 | `[&:has([role=checkbox])]:pr-0`(base-ui 버튼 체크박스 전제) | `[&:has([data-slot=checkbox])]:pr-0`(native input 전제) | 없음 |
| 근거 | `ui/table.tsx` 16–113 | `admin/ui/table.tsx` 32–172 | `ui/table.tsx` 7–83 |

위험: 선택 열 셀렉터가 체크박스 엔진에 종속된다 — 공통 Table은 `data-slot="checkbox"`처럼 엔진 무관 훅으로 통일해야 한다(후보).

### 3.3 DataTable — 선행 §3.4 재검증·절 단위 비교

대상: map `ui/data-table.tsx`(799), pinvi `admin/ui/data-table.tsx`(853) + `admin/AdminTable.tsx`(272, 어댑터) + `admin/DataTable.tsx`(8, shim), geo `ui/VirtualTable.tsx`(409).

| 절 | map DataTable | pinvi DataTable (이식본) | pinvi AdminTable (실소비 계약, 35 파일) | geo VirtualTable (13 import 파일, `as="table"` 26회) |
|---|---|---|---|---|
| 컬럼 정의 | TanStack `ColumnDef<TData, unknown>[]` + `meta: DataTableColumnMeta{align,wrap,className,headerClassName,cellClassName}` | + `meta.headerStyle`(런타임 폭은 inline style) | `AdminTableColumn{key,header,width,cell,sortable,sortValue,sortKey,align}` → 내부에서 `ColumnDef` 변환, `width`(px)→`size` | `VirtualColumn<T>{key,header,headerCell,cell,sortValue,align,cellClassName,rowHeader,width}` → 내부 `ColumnDef` |
| 정렬 | `manualSorting` **기본 true**(서버), `sorting`/`onSortingChange` 제어형 또는 내부 상태, `getSortedRowModel`은 `manualSorting=false`일 때만 | + `initialSorting`, `enableSortingRemoval`(3상태 해제 방지), `enableMultiSort:false` 명시 | **`manualSorting={false}` 고정**(클라이언트), `serverSort{key,order,onChange}` 있을 때만 서버 정렬; `initialSort` | 클라이언트 전용(`getSortedRowModel`), `sortDescFirst:false`, `sortUndefined:'last'`, `initialSortKey/Dir` |
| 선택 | `enableRowSelection: boolean \| (row)=>boolean`, `rowSelection`/`onRowSelectionChange`, `rowSelectionLabel`(접근성 이름), `renderBulkActions`(선택 시 상단 bulk bar `role=region`) | 동일 | **없음**(어댑터가 노출하지 않음) | 없음(`headerCell`/`cell`로 호출부가 직접 구성) |
| 가상화 | `virtualized`(opt-in) → `display:grid` + `role=table/rowgroup/row/columnheader/cell` 명시 + `aria-rowcount`; `estimateRowSize` 40, `overscan` 12; 고정 높이 필수 | + `rowTestId`를 가상 경로에도, `stickyHeader`, `containerStyle/TestId`, `noUncheckedIndexedAccess` 가드 | `virtualized` + `virtualizeThreshold`(기본 30행 미만이면 비가상), `maxHeight`(기본 `70dvh`), `mobileCard`(모바일 카드 목록, pinvi 고유) | **기본 `as="grid"` 가상화**(height 360, rowHeight 44, overscan 8, ARIA grid roles); `as="table"`은 시맨틱 `<table>` + `caption` + `th scope` |
| 빈/오류/로딩 | `isLoading` → skeleton 행(`aria-busy`, `skeletonRowCount` 6); `isError`/`error`/`errorTitle`/`errorState`/`onRetry`(Promise면 버튼 loading); `emptyMessage`/`emptyState{title,description,action,icon}` → `EmptyState` | 동일 | `loading` → skeleton + sr-only "불러오는 중…"(e2e 계약), `empty` 문자열(기본 "항목이 없습니다."), `isError/error/onRetry` | `emptyHint` 문자열만; 로딩/오류 표면 **없음** |
| 페이지네이션 | 내부 없음 — `pagination-bar.tsx`(`OffsetPager`/`CursorPager`) 별도 | 동일 | 없음 | 없음 |
| 행 상호작용 | `onRowClick`(Enter/Space, tabIndex), `isRowActive` → `data-state=selected`, `rowTestId`, `rowIdentity` | `aria-selected` 제거(role=table 행에 무효) → `data-clickable` | `onRowClick`, `rowTestId` | `onRowClick`(Enter/Space), `getRowClassName` |
| 접근성 | `ariaLabel`(caption), 정렬 헤더 버튼 + `aria-sort`, 글리프 `aria-hidden` | + 정렬 버튼 `data-testid=admin-table-sort-<id>` | `ariaLabel` | `caption`, `aria-sort`, 스크롤 영역 `role=group tabIndex=0` + 접근 가능한 이름 |
| 검색/툴바 | 없음(FilterBar 별도) | 없음 | 없음 | `getSearchText` 전역 필터 + `toolbarExtras` + "n / total" 카운트 |
| 스타일 | Tailwind 토큰 클래스 | pinvi 토큰 클래스 | — | 순수 CSS 클래스(`.vtable-*`, `.table.compact`; `globals.css` 3,750줄) |
| 테스트 | `data-table.test.tsx` 175줄(컬럼헤더/정렬 aria-sort/빈·오류/행 클릭 키보드/선택 가능 predicate) | 없음(직접) | `tests/AdminTable*.test.tsx` 3파일 418줄 + `AdminSectionContract.test.tsx` 99줄 + e2e 5파일(`admin-table-scroll`, `admin-table-sort-*`, `admin-mobile-cards` testid 계약) | `tests/unit/virtual-table*.test.tsx` 280줄(스크롤 영역 포커스/이름, 시맨틱 유지, 필터/정렬, grid ARIA) |

선행 보고서 §3.4 재검증 결과: "map과 Pinvi의 DataTable은 `manualSorting=true`를 기본으로 한다"는 두 `data-table.tsx` 파일에 대해서는 사실이지만, pinvi에서 실제로 35개 페이지가 소비하는 계약은 `AdminTable` 어댑터이고 이는 **`manualSorting={false}` 고정**이다(`AdminTable.tsx` 25–27행, 사실). 따라서 pinvi의 "화면이 거짓말을 하는 클라이언트 부분 정렬" 위험은 어댑터 주석(66–75행)이 이미 인지하고 `serverSort`로 opt-in 해결한 상태이며, 공통화 시 이 두 모드(클라이언트 전체 정렬 vs 서버 제어 정렬)를 하나의 prop 체계로 명시해야 한다는 선행 결론은 그대로 유효하다.

회귀 위험(DataTable 공통화):

| 위험 | 영향 | 근거 |
|---|---|---|
| pinvi e2e가 잠근 testid(`admin-table-scroll`, `admin-table-sort-<key>`, `admin-mobile-cards`)와 sr-only 로딩 문구 | pinvi e2e 5파일 | `AdminTable.tsx` 16–23 |
| geo `VirtualTable`의 기본 가상화(`as="grid"`)와 툴바 검색을 DataTable로 옮기면 검색·카운트 UI가 사라짐(DataTable에는 없음) | geo 13 소비 파일 | `VirtualTable.tsx` 168–191 |
| geo `rowHeader`(전치 key/value 표) 계약은 map DataTable에 없음 | geo | `VirtualTable.tsx` 32–37, 290–297 |
| `aria-selected` on `role=table` row — map은 부착, pinvi는 제거(무효 속성) | map | pinvi diff 554–557행 |
| `enableSortingRemoval` 미지원 시 서버 정렬 목록에서 헤더가 `desc`에 갇힘 | pinvi(T-357) | pinvi `data-table.tsx` 124–132 |
| `noUncheckedIndexedAccess` 하에서 map 원문이 타입 오류 | pinvi | pinvi `data-table.tsx` 598–600, 799–801 |

### 3.4 나머지 primitive 계약 차이

| 컴포넌트 | 차이 | 회귀 위험 |
|---|---|---|
| Checkbox | map/concierge: base-ui `Root/Indicator`(button 기반, `role=checkbox`, `indeterminate` prop, `onCheckedChange(checked, details)`); pinvi: native `<input>` + `forwardRef`, `onCheckedChange(checked: boolean)`, `data-indeterminate`; geo: radix `Root/Indicator` | 폼 직렬화(native input은 `FormData`에 포함, 버튼형은 미포함 — base-ui가 hidden input을 두는지 미확인), Table 선택 열 셀렉터, 콜백 시그니처 |
| Badge | map/concierge: `useRender` + `render` prop(링크 배지 `<a>` 합성); pinvi/geo: 순수 `<span>`; geo variant 축 이름이 `tone`이고 값이 `ok/warn/error/brand`(map `success/warning/destructive/secondary`) | geo `StatusBadge`·`severityClass` 매핑 재작성, `[a]:hover:` 셀렉터 유지 여부 |
| Dialog | map: base-ui `Root/Trigger/Close/Popup/Backdrop/Viewport`; pinvi: + `hasUnsavedInput`(Esc/바깥 클릭 차단), `viewportProps`(testid), `data-pv-surface="admin"`(토큰 스코프); geo: radix `Portal/Overlay/Content`; concierge: base-ui, Root/Trigger/Close 재수출; pinvi 사용자 `ui/Dialog.tsx`는 `createPortal` + 자체 `useModalDialog`(focus-trap/`inert`) | overlay 엔진 교체 시 포커스 복귀·`inert` 처리·애니메이션 data 속성(`data-[starting-style]` vs radix `data-[state]`) 전면 재검증 |
| AlertDialog | geo는 `Action/Cancel` 컴포넌트가 `buttonVariants`를 적용; map/pinvi/concierge는 `Close` + `Button` 조합 | geo 호출부 API 변경 |
| Tabs | map/concierge base-ui `Tab/Panel`, geo radix `Trigger/Content`; pinvi admin 미사용 | geo 1 파일 |
| Separator/Input | pinvi는 native 요소(`role=separator`, `<input>`)로 대체 — 시각·동작 동일 | 낮음(엔진 무관 구현 채택 가능) |
| Toast | map `sonner`(2.0.7), geo radix `Toast` + zustand 스토어, ktdm 자체 `ToastStack`, pinvi 없음(인라인 상태), concierge 없음 | `CopyButton`/`JsonViewer` 등 피드백 채널을 prop 주입으로 분리해야 함 |
| Field | map/pinvi에만 `FieldMessage`; geo/concierge에는 `label.tsx`(radix Label/네이티브) 별도 | 낮음 |
| HelpTip | 4앱 모두 Popover 트리거(hover 툴팁 아님) — 계약 일치. geo는 `PopoverTrigger asChild` | overlay 엔진에 종속 |
| ConfirmDialog | 4가지 API(Provider+Promise / 제어형 props / trigger 래퍼 2종) | 호출부 10(map)+5(pinvi)+geo/concierge 미계수 전부 재작성 |
| AppErrorPanel | map/geo/ktdm props 동일(`error`, `reset?`, `standalone?`); concierge는 타입만 동일 | 낮음 — 단 내부가 `Alert`/`Button`을 쓰므로 1차 primitive 이후 |
| LoginForm | 5개 구현이 모두 `username` 기본값 "admin", `fetch('/api/auth/login')`(ktdm은 `postJson`)를 쓰지만 리다이렉트(`nextPath` prop vs `useSearchParams` vs `onLogin` 콜백)·스타일(Tailwind vs 순수 CSS)이 다름 | 인증 경계 — 선행 §7.2대로 첫 범위 제외 |

---

## 4. §3 common UI 패키지 후보 분류

분류 기준: (a) 두 앱 이상에서 props 계약이 이미 일치하거나 색 토큰 치환만으로 갈라짐, (b) 프리미티브 엔진 비의존, (c) 도메인 import(`lib/status-label`, `lib/entity-href`, 인증, 지도) 없음. 소비처 수는 §1 방법의 `rg -l` 계수.

### 4.1 1차 후보(작고 계약 합의가 쉬움)

| 후보 | 근거(계약 일치) | 소비처(map/pinvi/geo/concierge) | 합의할 것 |
|---|---|---|---|
| `badge-variants` + `Badge` | map/pinvi/concierge 10 variant 동일; geo만 `tone` 축 | 8/2/12/17 | `render` prop 채택 여부(map·concierge 有, pinvi·geo 無); geo `tone`→`variant` 매핑 |
| `Skeleton`, `Separator`, `Card`, `Alert` | 클래스만 다름; Card 서브컴포넌트 7종 동일(map/geo/concierge) | skeleton 19/1/14/0, alert 29/1/15/0, card 7/1/1/1 | Separator는 native `div role=separator`(pinvi식)로 엔진 제거; Alert의 `AlertActions` 유무 |
| `Input`, `Textarea`, `NativeSelect(+Option)` | native 요소; base-ui `Input`은 얇은 래퍼 | input 16/16/12/8, native-select 16/22/8/0 | React 18 소비자용 `forwardRef`(geo `native-select.tsx`는 이미 forwardRef) |
| `Field`(+variants) | 11/10 서브컴포넌트 동일 | 4/3/15/5 | `FieldMessage` 포함 여부 |
| `EmptyState` | map/pinvi props 동일; geo 14줄판은 상위호환 가능 | 19/1/—/— | `framed`/`size` |
| `SectionCard` | map/pinvi/**concierge** props 완전 동일; geo `Panel`은 `title:string` 제한 | 17/1/—/— (concierge SectionCard 소비처 미계수) | `headingLevel` 기본 2 |
| `FilterBar/FilterField/FilterActions` | map/pinvi 동일 | 14/24(AdminPage 경유) | 없음 |
| `StatStrip` | map/pinvi 동일, concierge 유사(loading/testId 없음), ktdm tone 이름 상이 | 6/1/—/— | `tone` 값 집합 = `StatusTone`(success/warning/destructive/info/neutral)로 통일 — ktdm `ok/warn/danger` 매핑 |
| `HelpTip` | 4앱 모두 Popover 기반, `label`+`children` | 8/6/—/— | Popover 엔진(§5)에 종속 → 1차 후반 |
| `button-variants`(레시피만) | map/geo/concierge 클래스 문자열 동일 계열; pinvi는 토큰명만 다름 | — | 토큰 별칭 계층(§6.4) 선행 |
| `AppErrorPanel` | map/geo/ktdm props 동일 | — | Alert/Button 이후 |

추정: 위 항목은 pinvi T-356 이식 주석이 "색 토큰 치환표만 적용"이라고 명시한 파일들과 겹치며, 토큰 별칭만 해결되면 소스 동일화가 가능하다.

### 4.2 2차 후보(계약 합의·엔진 결정 필요)

| 후보 | 왜 2차인가 | 선행 조건 |
|---|---|---|
| `Button` | §3.1의 세 계열(map계열 / pinvi native·두 벌 / airport shadcn 기본) | `type='button'` 기본 확정, `loading`=aria-disabled 방식 확정, `render` 지원 여부, React 18용 ref |
| `Checkbox`, `Dialog`, `AlertDialog`, `Popover`, `Tooltip`, `Tabs`, `Breadcrumb` | 엔진 종속(base-ui vs radix), pinvi 확장(`hasUnsavedInput`, `data-pv-surface`) | §5 엔진 결정 |
| `Table` primitive | pinvi 확장 4종(§3.2) 흡수 필요 | 선택 열 셀렉터 엔진 무관화 |
| `DataTable` | §3.3 — 정렬 2모드, 선택, 가상화, testid 계약, geo 검색 툴바·`rowHeader` | `Table`·`Checkbox`·`Alert`·`EmptyState`·`Skeleton`·`Button` 확정 후; pinvi `AdminTable` 어댑터는 pinvi에 잔류 |
| `OffsetPager/CursorPager` | map/pinvi만 존재(유사); 타 앱 수요 미확인 | `Button` 확정 |
| `CopyButton`, `JsonViewer`, `DetailList` | 피드백 채널(sonner vs inline) 차이; DetailList는 CopyButton+HelpTip 의존 | 토스트 정책 |
| `StatusBadge` 계열 | `lib/status-label`의 tone 테이블·`statusLabel` 사전(도메인 문자열 → 한글)이 앱별 | tone 테이블을 prop/컨텍스트 주입으로 분리 |
| `AdminPageHeader`/`AdminSkipLink`/`AdminRailGrid` | pinvi가 이미 map `AdminShell`에서 이식 가능한 부분만 분리(224줄); geo `PageHeader`·weather `PageHeader`·ktdm `AppShell` props(title/description/section/actions/meta)와 동형 | Breadcrumb 엔진; nav 정본은 앱 |
| `FormFieldInput/FormSelect/FormTextArea` | map/pinvi만; HelpTip·Field 의존 | 1차 완료 후 |
| Toast 어댑터 | 3가지 구현 + 2앱 없음 | 정책 결정(전역 toast 채택 여부) |

### 4.3 보류(도메인·인증·지도 결합)

| 항목 | 이유 | 근거 |
|---|---|---|
| `AdminShell`의 nav/로그아웃/접힘/RBAC | 앱별 URL·권한·제품명; pinvi도 통째 이식을 거부하고 부분만 가져옴 | pinvi `admin-shell-parts.tsx` 1–13 |
| `LoginForm`/`LoginScreen` | 신뢰 경계(선행 §7.2 "첫 범위 제외"와 일치); 리다이렉트 계약 3종 | §3.4 |
| `ConfirmDialog` | API 4종 — 합의 전까지 각 앱 유지; 합의 시 2차 | §2.2 |
| `SelectableRow`, `EntityLink`, `MultiFilterCombobox`, `admin-region-autosearch`, `feature-*` 패널 | map 전용(소비처 2/13/2), `hrefFor` 도메인 라우팅 | map `entity-link.tsx` 5 |
| `vworld-map-view` 계열 | map 1,858줄 도메인 클러스터; 기존 라이브러리(`maplibre-vworld-react`)와 경계 중복 금지; 현재 그 라이브러리 소비자는 geo뿐이고 나머지는 `maplibre-gl` 직접(concierge는 6.0, 나머지 5.24) | §2.2 표 |
| pinvi 사용자 UI(`ui/Button.tsx`, `ui/Dialog.tsx`, `ui/ConfirmDialog.tsx`) | 제품 정체성(Airbnb 톤, 44px 컨트롤) — 선행 §3.5 | `ui/Button.tsx` 1–23 |
| pinvi `AdminTable` 어댑터·`DataTable` shim | pinvi 하위호환 계층 자체는 pinvi 소유 | `AdminTable.tsx` 8–14 |
| weather·airport main·ktdm의 순수 CSS 컴포넌트 | Tailwind v4 전환(설계 전제 1) 이후에야 클래스 기반 공통 UI 소비 가능; ktdm은 v4 설치는 있으나 `ops-*` 클래스 146줄과 유틸리티 179줄 혼용 | §2.3 |

---

## 5. §4 프리미티브 엔진 결정 근거

### 5.1 현황 계수(사실)

| 앱 | 엔진 | 엔진 import 파일 수 | 합성 방식 호출부 |
|---|---|---|---|
| map | `@base-ui/react` 1.6.0 (button, alert-dialog, checkbox, dialog, input, popover, separator, tabs, tooltip, merge-props/use-render) | 12 | `render=` 3줄/2파일, `nativeButton` 2 |
| pinvi admin | `@base-ui/react` 1.8.0 — **overlay 4종만**(alert-dialog, dialog, popover, tooltip; help-tip 경유) | 13(앱 파일 포함) | `render=` 2줄/2파일 |
| concierge | `@base-ui/react` 1.5.0 (button, alert-dialog, checkbox, dialog, input, popover, select, separator, switch, tabs, use-render) | 12 | `render=` 9줄/7파일 |
| airport WIP | `@base-ui/react` 1.8.0 (button) | 2 | 0 |
| geo | `radix-ui` 1.6.0 — 12 ui 파일: alert-dialog, button(Slot), checkbox, collapsible, dialog, label, popover, progress, separator, tabs, toaster(Toast), tooltip | 12 | `<Button asChild>` **12곳/7파일**(FilesPanel 5, LoadConsole 2, DagsterPanel 2, BackupsPanel 1, DagsterEmbed 1, ConsistencyPanel 1) + `*Trigger asChild` **5곳**(ConfirmActionDialog 1, HelpTip 1, ReconcileTab 2, 나머지 1은 `app/` 하위 — 파일 미특정) |
| ktdm / weather / airport main | 없음 | 0 | — |

shadcn `components.json` style: map·concierge·airport WIP = `base-nova`, geo = `radix-nova`, pinvi = 파일 없음(§6).

### 5.2 base-ui 채택 시 geo 이관 범위(사실 + 추정)

| 작업 | 규모 | 근거 |
|---|---|---|
| ui primitive 재작성 | 12파일(`components/ui/{alert-dialog,button,checkbox,collapsible,dialog,label,popover,progress,separator,tabs,toaster,tooltip}.tsx`, 합계 약 800줄) | `rg -n "from ['\"]radix-ui"` |
| 서브컴포넌트 이름 변경 | Dialog `Portal/Overlay/Content` → base-ui `Portal/Backdrop/Popup(+Viewport)`; AlertDialog `Action/Cancel` → `Close`+`Button`; Tabs `Trigger/Content` → `Tab/Panel`; 애니메이션 `data-[state=open]` → `data-[starting-style]/[ending-style]` | geo `dialog.tsx`/`alert-dialog.tsx`/`tabs.tsx` export 목록 vs map |
| 호출부 | `asChild` 17곳(위 계수) → `render={<Link/>}` 등; `Dialog*` 소비 6파일, `Checkbox` 6, `Tooltip` 3, `AlertDialog` 2, `Popover`/`Tabs`/`Separator`/`Label` 각 1, `Toaster` 1(`app/providers.tsx`) | `rg -l "components/ui/<name>"` |
| Toast | radix `Toast` + zustand 스토어(`lib/toast.ts`) → base-ui에는 Toast가 있으나(미확인 API) sonner 채택 시 스토어 API(`toast.success` 등, 소비처 0 — `@/lib/toast` import 0 파일이므로 `Toaster`만 마운트된 상태) 재검토 | `rg -l "@/lib/toast"` = 0 |
| React 18 유지 가능성 | base-ui peer `react ^17 \|\| ^18 \|\| ^19` — 가능. 단 map식 "ref를 props로" 작성은 React 19 전제라 공통 패키지가 React 18을 지원하려면 `forwardRef` 유지 필요 | map lock `@base-ui/react` peerDependencies |
| 테스트 | geo `tests/unit/*.test.tsx` 중 ui 참조 5파일(backups-panel, source-files-panel, virtual-table ×2, upload-tab-sse-cap) 재검증 | `rg -l "VirtualTable\|components/ui" tests` |

### 5.3 radix 채택 시(대안) 범위

map 12 + concierge 12 + pinvi admin 4(overlay) + airport 1 = 29 파일이 역방향으로 바뀌고, `render`/`useRender` 호출부(3+9+2줄)와 `nativeButton`이 `asChild`로 돌아간다. 또한 세 앱의 `components.json` style(`base-nova`)이 바뀐다. 사실 기준으로 base-ui 소비 파일 수(29)가 radix(12)보다 많다.

### 5.4 결정 근거 요약(후보)

- **base-ui를 공통 엔진으로 채택**하는 편이 변경 파일 수·shadcn style 정합(3:1)·최신 작업(airport WIP, pinvi T-356) 방향과 일치한다(사실 기반 후보).
- pinvi가 보여준 "overlay만 base-ui, 나머지는 native 요소" 절충은 Button/Checkbox/Input/Separator/Badge에서 엔진 의존을 없애므로, 공통 패키지의 **비-overlay primitive는 native 우선**으로 설계하면 geo(React 18)·pinvi(사용자 UI와 공존) 양쪽 부담이 줄어든다(후보). 대가: map·concierge의 `render` prop 합성(Badge 링크, Breadcrumb Link)을 어떻게 유지할지 결정해야 한다 — pinvi는 `<a className={badgeVariants()}>` 관용구로 대체했다(사실).
- overlay(Dialog/AlertDialog/Popover/Tooltip/Tabs)는 base-ui로 통일하되 pinvi 확장(`hasUnsavedInput`, `viewportProps.data-testid`, 표면 스코프 속성)을 공통 계약에 포함할지 결정해야 한다.
- 미확인: base-ui `Button`이 `type="button"`을 기본 부여하는지(pinvi 주석 근거만 있음), base-ui `Checkbox`의 폼 제출 시 hidden input 여부, base-ui Toast API.

---

## 6. §5 shadcn 등록 방식 후보와 `components.json` 정합

### 6.1 현재 `components.json`(사실)

| 앱 | 존재 | style | `tailwind.config` | `tailwind.css` | aliases.ui / utils | `registries` |
|---|---|---|---|---|---|---|
| map | 있음 | base-nova | `""` | `src/app/globals.css` | `@/components/ui` / `@/lib/utils` | `{}` |
| concierge | 있음 | base-nova | `tailwind.config.ts`(`@config`로 로드, 색·radius extend) | `src/app/globals.css` | 동일 | `{}` |
| airport WIP | 있음 | base-nova | `""` | `src/app/globals.css` | 동일 | `{}` |
| geo | 있음 | radix-nova | `tailwind.config.ts`(`--ui-*` 변수 매핑) | `app/globals.css` | 동일 | `{}` |
| pinvi web | **없음** | — | `tailwind.config.ts`(`@pinvi/design-tokens/tailwind-preset`, `@config`) | `app/globals.css` | 실제 경로 `@/components/admin/ui` / `@/lib/admin/cn` | — |
| ktdm / weather / airport main | 없음 | — | — | — | — | — |

사실: 어떤 저장소에도 `registry.json`·`registry/` 디렉터리가 없고, shadcn CLI는 concierge(4.10.0)·airport WIP(4.21.0)에만 dependency로 있으며 `scripts`에는 없다. 즉 현재는 **소스 복사(수동 이식)** 방식이 사실상의 등록 방식이다.

### 6.2 후보 비교

| 방식 | 동작 | 장점(근거) | 비용·위험(근거) | `components.json` 정합 |
|---|---|---|---|---|
| A. 자체 shadcn 레지스트리(`registry.json` 배포, `shadcn add @kor-travel/<item>`) | 소스를 앱에 복사하되 출처·버전을 레지스트리가 관리 | 3앱이 이미 `base-nova` components.json을 갖고 있어 CLI 흐름과 맞음; 앱별 미세 조정(pinvi `hasUnsavedInput`) 허용 | 복사 후 드리프트는 여전(현재 27/27 상이가 그 증거); 클래스 문자열의 토큰명이 앱마다 달라 그대로 복사하면 pinvi(`admin-*`), airport(shadcn 기본명)에서 스타일이 깨짐 → 토큰 별칭 선행(§6.4); geo는 style이 `radix-nova` | pinvi·ktdm·weather·airport main에 `components.json` 신설 필요(pinvi는 `aliases.ui=@/components/admin/ui`, `utils=@/lib/admin/cn`) |
| B. npm 패키지(`@digitie/kor-travel-common-ui`; 선행 §7.1 명명) | 컴파일된 ESM + d.ts + CSS(또는 Tailwind 소스 + `@source`) | 버전 갱신으로 전파(선행 §3.2의 geo 반복 동기화 T-302/T-303 비용 절감 근거); pinvi처럼 앱이 `transpilePackages`를 이미 쓰는 곳은 소스 배포도 가능 | Tailwind 클래스 탐지(`@source` 등록) 필요(선행 §7.3); React 18/19 peer 동시 지원 검증; 앱별 확장(pinvi testid/sticky)을 prop으로 흡수해야 함; base-ui peer | components.json과 무관(설치 경로 아님) — 대신 `@theme` 토큰 별칭과 `@source`가 정합 포인트 |
| C. 소스 복사 유지 + 정본 지정(현행) | map을 정본으로 두고 수동 이식 | 즉시 가능, pinvi가 이식 규칙(주석 헤더·치환표)을 이미 문서화 | 드리프트 상시(사실); 검증 자동화 없음 | 현행 |

후보: 1차(§4.1) 항목은 **A 또는 B 어느 쪽이든 토큰 별칭 계층이 선행**되어야 하며, 2차 DataTable처럼 앱별 확장이 많은 것은 B(prop으로 흡수) 쪽이 유리하다는 정황이 있다(추정). 결정 자체는 이 조사의 범위 밖이다.

### 6.3 토큰 이름 정합(모든 방식의 선행 조건)

| 토큰 | map | geo | concierge | pinvi admin | airport WIP |
|---|---|---|---|---|---|
| 컨트롤 높이/radius | `h-control`/`h-control-sm`, `rounded-control`, `rounded-panel`(`--spacing-control`, `--radius-control/panel` @theme) | 동일 이름 | `--control-height`, `--radius-control/panel`을 `tailwind.config.ts` extend로 노출(`--color-*` @theme 없음) | 동일 이름(`@theme`에 같은 값 등록 — pinvi 주석) | `--radius-control` 2회 언급 — `h-control` 없음(shadcn 기본 `h-8` 등) |
| 색 | `brand/brand-tint/brand-hover`, `surface-page/subtle/muted`, `text-primary/secondary/tertiary`, `input`, `focus`, `success/warning/info/destructive(+tint)` | 대부분 동일 + `ink/paper/rule` 계열 병존 | `brand/surface-*/text-primary` 등을 `tailwind.config.ts` colors → `--ktc-*`/`--brand` CSS 변수 | **`admin-*` 네임스페이스**(admin-line, admin-subtle, admin-muted, admin-danger…), `ink/body/canvas/cta/primary` | shadcn 기본(`primary/background/muted/ring…`) |
| 타이포/모션 | `text-2xs`, `duration-fast/base`, `outline-focus` | 동일 | `duration-fast` 있음 | `text-2xs`, `duration-fast/normal`(base→normal), `outline-focus` | 없음 |

사실: 같은 클래스 문자열이 map·geo·concierge에서는 그대로 동작하지만 pinvi admin과 airport에서는 동작하지 않는다. pinvi는 이 문제를 **치환표**로, concierge는 **config 매핑**으로 풀었다. 공통 패키지는 (i) 클래스에 공통 토큰명을 쓰고 앱이 `@theme`에서 별칭을 정의하거나(예: pinvi `--color-brand: var(--color-admin-brand-ink)`), (ii) 클래스 대신 CSS 변수 참조(`bg-[var(--kt-brand)]`)를 쓰는 두 길이 있다(후보). pinvi의 `[data-pv-surface='admin']` 스코프(globals.css 114행)는 사용자 UI와 admin 토큰을 한 앱에서 분리하는 선례다(사실).

---

## 7. 열린 질문

1. base-ui `Button`이 `type="button"`을 기본 부여한다는 pinvi 주석을 base-ui 소스로 확인할 것(미확인). 공통 Button은 엔진과 무관하게 `type='button'`을 명시 기본으로 둘지.
2. `loading` 의미: aria-disabled(포커스 유지, map 계열)로 통일할 경우 pinvi 사용자 UI(`disabled={disabled||loading}`)는 별도 유지인가, 아니면 admin/사용자 공통 계약으로 수렴하는가.
3. React 18(geo, ktdm) 지원 기간: 공통 패키지가 `forwardRef`를 유지할지, React 19 업그레이드를 선행 조건으로 둘지.
4. geo `VirtualTable`의 검색 툴바·`rowHeader`·기본 가상화 계약을 DataTable에 흡수할지, geo 전용으로 남길지(13 소비 파일, `as="table"` 26회).
5. 토스트 정책: sonner(map) / radix Toast+zustand(geo, 실제 호출 0) / 자체(ktdm) / 없음(pinvi, concierge). `CopyButton` 피드백을 inline 기본 + 선택적 toast 주입으로 갈지.
6. pinvi 확장(`hasUnsavedInput`, `stickyHeader`, `containerTestId`, `enableSortingRemoval`, `data-pv-surface`)을 공통 계약에 올릴지 — pinvi e2e가 잠근 testid 계약을 공통이 보장할 것인지.
7. airport WIP의 `cn@0.2.5` npm 패키지 채택은 다른 앱(clsx+tailwind-merge)과 다르다 — 공통 `cn`을 패키지에서 제공할지, 앱 alias(`@/lib/utils`)를 요구할지.
8. 레지스트리(A)와 npm(B) 병행 여부: primitive는 A, 합성 컴포넌트는 B 같은 이원화가 필요한지, 아니면 하나로 갈지.
9. 색 토큰 별칭 계층의 소유: 각 앱 `@theme`에서 별칭 정의(앱 소유) vs 공통 패키지가 앱별 preset 제공(pinvi `@pinvi/design-tokens` 모델).
10. weather admin(순수 CSS, Tailwind 없음)·airport main·ktdm 혼용 CSS의 Tailwind v4 전환 순서 — 전환 전에는 공통 UI를 소비할 수 없다.
11. `lucide-react` 메이저 불일치(0.363 ~ 1.41): 공통 UI가 아이콘을 직접 import하면 peer 범위를 어떻게 잡을지.
12. pinvi `AdminPage`·`Section`·`FilterBar` 어댑터(39/20/24 소비처)를 공통 `AdminPageHeader`/`SectionCard`/`FilterBar`로 대체할 때의 이름 충돌(`Section` vs `SectionCard`).

---

## 8. 근거 파일 목록(저장소 상대 경로)

kor-travel-map @ `c494e227` (`packages/kor-travel-map-admin/frontend/`):
1. `src/components/ui/button.tsx`
2. `src/components/ui/button-variants.ts`
3. `src/components/ui/badge.tsx`, `src/components/ui/badge-variants.ts`
4. `src/components/ui/checkbox.tsx`
5. `src/components/ui/table.tsx`
6. `src/components/ui/data-table.tsx`, `src/components/ui/data-table.test.tsx`
7. `src/components/ui/dialog.tsx`, `alert-dialog.tsx`, `popover.tsx`, `tooltip.tsx`, `tabs.tsx`, `separator.tsx`, `input.tsx`, `field.tsx`, `sonner.tsx`
8. `src/components/admin-shell.tsx`
9. `src/components/status-badge.tsx`, `src/components/status-badge-variants.ts`
10. `src/components/{filter-bar,pagination-bar,empty-state,section-card,stat-strip,copy-button,json-viewer,detail-list,help-tip,confirm-dialog,login-form,app-error-panel,selectable-row,entity-link,multi-filter-combobox,vworld-map-view}.tsx`
11. `components.json`, `package.json`, `next.config.ts`, `tsconfig.json`, `src/app/globals.css`, `design.md`
12. 루트 `package-lock.json`, `docs/architecture/admin-frontend-design-rules.md`

pinvi @ `9af25e5` (`apps/web/`):
13. `components/admin/ui/button.tsx`, `button-variants.ts`
14. `components/admin/ui/{badge,badge-variants,checkbox,input,separator,skeleton,dialog,alert-dialog,tooltip,popover,table,data-table,help-tip,field}.ts(x)`
15. `components/admin/AdminTable.tsx`, `components/admin/DataTable.tsx`
16. `components/admin/admin-shell-parts.tsx`, `components/admin/AdminPage.tsx`, `components/admin/Placeholder.tsx`
17. `components/admin/{status-badge,status-badge-variants,copy-button,json-viewer,detail-list,empty-state,section-card,stat-strip,filter-bar,pagination-bar}.ts(x)`
18. `components/ui/Button.tsx`, `components/ui/Dialog.tsx`, `components/ui/ConfirmDialog.tsx`, `lib/useModalDialog.ts`
19. `tests/AdminTable.test.tsx`, `tests/AdminTableServerSort.test.tsx`, `tests/AdminTableVirtualization.test.tsx`, `tests/AdminSectionContract.test.tsx`, `e2e/admin-table.e2e.ts`
20. `package.json`, `next.config.mjs`, `postcss.config.mjs`, `tailwind.config.ts`, `app/globals.css`; 루트 `tsconfig.base.json`, `package-lock.json`, `DESIGN.md`, `packages/design-tokens/package.json`

kor-travel-geo @ `1d9d74d` (`kor-travel-geo-ui/`):
21. `components/ui/button.tsx`, `components/ui/button-variants.ts`
22. `components/ui/VirtualTable.tsx`
23. `components/ui/{badge,badge-variants,StatusBadge,dialog,alert-dialog,checkbox,tabs,tooltip,popover,toaster,field,alert,native-select,JsonBlock,Panel,PageHeader,collapsible,label,progress,separator,skeleton,input,card}.ts(x)`
24. `components/admin/shared/{HelpTip,ConfirmActionDialog,EmptyState,MetricTile,RefreshButton,AdminTabs,KeyValueGrid,JsonDetails}.tsx`
25. `components/admin/{FilesPanel,LoadConsole,DagsterPanel,DagsterEmbed,BackupsPanel,ConsistencyPanel}.tsx`, `components/admin/source-files/ReconcileTab.tsx` (asChild 호출부)
26. `components/auth/LoginForm.tsx`, `components/layout/AppErrorPanel.tsx`, `components/layout/AppShell.tsx`, `components/vworld/CoordinateMap.tsx`, `app/providers.tsx`, `lib/toast.ts`
27. `components.json`, `package.json`, `package-lock.json`, `tailwind.config.ts`, `app/globals.css`, `tests/unit/virtual-table.test.tsx`, `tests/unit/virtual-table-scroll.test.tsx`; 루트 `docs/resume.md`(T-302/T-303), `docs/kor-travel-common-library-review.md`

kor-travel-concierge @ `7945305` (`frontend/`):
28. `src/components/ui/button.tsx`, `table.tsx`, `badge.tsx`, `dialog.tsx`, `alert-dialog.tsx`, `select.tsx`, `tabs.tsx`, `field.tsx`, `checkbox.tsx`, `input.tsx`, `popover.tsx`
29. `src/components/{SectionCard,StatStrip,HelpTip,CopyButton,ConfirmActionButton,LoginForm,AppShell,VWorldMap,panels,detail}.tsx`, `src/components/layout/AppErrorPanel.tsx`
30. `components.json`, `package.json`, `package-lock.json`, `tailwind.config.ts`, `tokens.css`, `src/app/globals.css`

kor-travel-airport:
31. WIP `99b3f98`: `frontend/src/components/ui/button.tsx`, `frontend/components.json`, `frontend/package.json`, `frontend/package-lock.json`, `frontend/src/lib/utils.ts`, `frontend/tsconfig.json`, `frontend/src/app/globals.css`
32. main `2bb1111`: `frontend/package.json`, `frontend/src/components/*.tsx`(6파일 목록)

kor-travel-docker-manager @ `862562d` (`frontend/`):
33. `src/components/{StatStrip,Toast,InlineError,CopyableCommand,LoginScreen}.tsx`, `src/components/layout/{AppShell,AppErrorPanel}.tsx`, `package.json`, `package-lock.json`, `src/app/globals.css`

kor-travel-weather @ `6003da9` (`packages/kor-travel-weather-admin/frontend/`):
34. `components/admin-shell.tsx`, `components/auth/LoginForm.tsx`, `components/vworld-map-view.tsx`, `components/weather-map.tsx`, `package.json`, `package-lock.json`, `app/globals.css`
