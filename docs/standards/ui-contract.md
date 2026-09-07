# `@kor-travel/ui` 공개 계약 — data-slot·testid·heading·sr-only·prop 기본값·SemVer 0.x

- 정본 지위: 이 문서는 `@kor-travel/ui`의 **공개 계약**(export 이름·prop 기본값·마크업 훅·문구·버전 규칙)의 정본 **초안**이다. 이 문서에 없는 마크업은 계약이 아니며 자유롭게 바뀔 수 있다.
- 확정 task: **T-204** — 실물 패키지(T-201 골격·T-203 소형 13종·T-205~T-210)와 대조해 확정하는 task가 남아 있다. "후보"로 표기한 값은 실물에서 확정될 때까지 소비자 코드가 의존하지 않는다. 마지막 갱신: 2026-09-06.
- 근거 약칭: `ui` = [ui-components 조사](../survey/cross/ui-components.md), `ux` = [ux-patterns 조사](../survey/cross/ux-patterns.md), `dt` = [design-tokens 조사](../survey/cross/design-tokens.md), `inv/<app>` = [인벤토리](../survey/README.md) §3.1. 결정: [설계 브리프](../plan/design-brief.md) D-09·D-10·D-31.

## 1. 계약의 범위

**UC-1 (MUST)** 다음이 공개 계약이며 변경은 §9의 버전 규칙을 따른다.

| 항목 | 내용 |
|---|---|
| export | 패키지 subpath와 named export 이름·타입 |
| prop 기본값 | 표에 "기본" 열로 적은 값(예: Button `type="button"`, DataTable `manualSorting: true`) |
| 마크업 훅 | `data-slot` 이름, testid를 받는 prop 이름, ARIA role·상태 속성 |
| heading 구조 | 각 컴포넌트가 만드는 heading 레벨과 그 제어 prop |
| 문구 | sr-only·기본 라벨 한국어 문자열(§5) |
| CSS | `kt-` 유틸리티만 사용(소비자가 `@source`로 스캔), 배포 CSS 파일 경로 |
| peer | `react ^19.0.0`, `react-dom ^19.0.0`, `@kor-travel/tokens`(호환 minor 하나), `@base-ui/react ^1.6.0`(0.1 useRender부터 필수; 권장 값은 versions.json) |

계약이 아닌 것: 내부 클래스 문자열, DOM 깊이, 애니메이션 시간, 아이콘 모양. 소비자 e2e는 `data-slot`·testid prop·문구·role로만 요소를 잡는다.

## 2. 패키지 형태

**UC-2 (MUST)** D-10 결정의 요약이다(정본은 [style-delivery](../architecture/style-delivery.md)와 ADR-007, 색인 [ADR README](../adr/README.md)).

| 항목 | 규칙 |
|---|---|
| 형식 | ESM + `.d.ts`, `'use client'`·`'use no memo'` 지시문 보존, 컴파일된 JS + Tailwind 소스 클래스(`kt-`) |
| subpath | `@kor-travel/ui`(전체), `@kor-travel/ui/cn`, 컴포넌트별 subpath(`@kor-travel/ui/button` 등, 후보) |
| React | 19 전용. ref는 prop으로 받고 `forwardRef`를 쓰지 않는다. React 18 앱(geo·ktdm)은 tokens부터 채택 |
| 엔진 | overlay(Dialog·AlertDialog·Popover·Tooltip·Tabs·Breadcrumb·HelpTip)만 `@base-ui/react`. 비-overlay(Button·Checkbox·Input·Textarea·NativeSelect·Separator·Badge)는 native 요소 + `useRender`로 `render` 합성 선택 지원 |
| 아이콘 | 인라인 SVG. `lucide-react` peer 없음 |
| 타입 검사 | `noUncheckedIndexedAccess: true` |
| 소비자 필수 | `@import "@kor-travel/tokens/theme.css"` + `@source "../node_modules/@kor-travel/ui"`([frontend-stack](frontend-stack.md) §4) |
| 스모크 | webpack·Turbopack 양쪽 `next build`(consumer-smoke) |

## 3. 공통 마크업 규약

**UC-3 (MUST)**

| 규칙 | 내용 | 근거 |
|---|---|---|
| UC-3.1 `data-slot` | 모든 컴포넌트 루트와 이름 있는 부분에 `data-slot="<component>[-<part>]"`(kebab-case)를 둔다. 예: `button`, `button-spinner`, `table-container`, `checkbox`, `dialog-popup`, `admin-shell-rail`. shadcn `base-nova` 생성물의 관행이며 map·ktdm 셸이 같은 이름을 이미 공유한다 | `inv/ktdm` §3(`admin-shell-rail/header/main` 동일), `ui` §3.2 |
| UC-3.2 testid | 패키지는 `data-testid`를 **하드코딩하지 않는다**. testid는 prop(`testId`, `rowTestId`, `containerTestId`, `sortTestIdPrefix`, `viewportProps`)으로만 부착된다. 소비자가 기존 e2e testid를 그대로 넘긴다 | pinvi e2e 잠금(`ui` §3.3) |
| UC-3.3 엔진 무관 셀렉터 | 내부 셀렉터는 `[data-slot=…]`만 쓴다(예: 선택 열 패딩 `[&:has([data-slot=checkbox])]:pr-0`). `[role=checkbox]` 같은 엔진 종속 셀렉터 금지 | `ui` §3.2 |
| UC-3.4 ARIA | `aria-busy`·`aria-disabled`·`aria-sort`·`aria-current`·`aria-live`는 표의 계약대로. `role="table"` 행에 `aria-selected`를 두지 않는다(무효 속성) | `ui` §3.3 |
| UC-3.5 문구 | 한국어 고정 문구는 §5 사전만. 문구 변경은 파괴 항목 | D-31 |
| UC-3.6 스코프 | `base.scoped.css` 사용 앱은 `[data-kt-surface]` 안에서만 base 규칙을 받는다. pinvi의 `data-pv-surface`는 앱 속성으로 병존 | [design-tokens](design-tokens.md) §7.1 |
| UC-3.7 알림 주입 | 토스트가 필요한 컴포넌트(CopyButton·DetailList)는 `onNotify?(message, tone)` prop으로 앱 엔진에 위임한다. 패키지는 토스트를 렌더하지 않는다 | D-09, `ux` C8 |

## 4. 컴포넌트별 계약

표기: "기본" = prop 기본값, "슬롯" = `data-slot` 이름, "heading" = 만들어지는 heading, "문구" = §5 사전 참조. 릴리스 묶음은 브리프 §6 T-2xx.

### 4.1 1차 소형(T-203, ui v0.1.0)

| 컴포넌트 | 루트·슬롯 | 주요 prop(기본) | heading·ARIA | 근거 |
|---|---|---|---|---|
| `Badge` | `<span data-slot="badge">` | `variant`(10종, map·pinvi·concierge 동일 집합 — 이름 목록은 T-203에서 실물 대조 기입), `render?`(링크 배지 합성) | 없음 | `ui` §2.1·§4.1 |
| `Skeleton` | `<div data-slot="skeleton" aria-hidden="true">` | — | 로딩 상태는 **감싸는 영역**이 `aria-busy` | `ux` G4.5 |
| `Separator` | `<div role="separator" aria-orientation data-slot="separator">` | `orientation`(`"horizontal"`), `decorative`(`true` → `role="none"`) | | `ui` §3.4 |
| `Card`, `CardHeader`, `CardTitle`, `CardDescription`, `CardAction`, `CardContent`, `CardFooter` | `data-slot="card"`, `card-header`… 7종 | `size`(`"default"`\|`"sm"`) | `CardTitle`은 `role="heading"` + `aria-level`(기본 2, `headingLevel`) — 후보 | `ui` §2.1, `inv/geo` §3 |
| `Alert`, `AlertTitle`, `AlertDescription`, `AlertActions` | `<div role="alert" data-slot="alert">` | `variant`(`"default"`\|`"destructive"`\|`"warning"`\|`"info"`; 성공 variant 없음) | what/why/what-to-do 3부 | `ux` G4.1·G4.2 |
| `Input`, `Textarea` | native `<input data-slot="input">` / `<textarea data-slot="textarea">` | `size`(`"default"` 36px\|`"sm"` 30px) | `aria-invalid` 스타일 | `ui` §4.1 |
| `NativeSelect`, `NativeSelectOption` | native `<select data-slot="native-select">` | `size` 동일 | `fireEvent.change` 구동 가능 | `inv/geo` §3 |
| `Field` 계열 11종 | `Field`, `FieldLabel`, `FieldDescription`, `FieldError`, `FieldMessage`, `FieldGroup`, `FieldSet`, `FieldLegend`, `FieldContent`, `FieldTitle`, `FieldSeparator` | `orientation` | `FieldError`는 `role="alert"`; `FieldSet`은 `<fieldset>` + `FieldLegend` | `ui` §2.1 |
| `EmptyState` | `<div data-slot="empty-state">` 좌정렬 | `title`, `description?`, `action?`, `icon?`, `framed`(`false`), `size`(`"default"`) | title은 `<p data-slot="empty-state-title">`(heading 아님, 후보) | `ux` G4.4 |
| `SectionCard` | `<section data-slot="section-card" aria-labelledby>` + `section-card-header` / `-body` / `-footer` | `title`, `description?`, `actions?`, `footer?`, `size`, `headingLevel`(`2`), `className`, `contentClassName` | `h{headingLevel}` in header. 카드 안 카드 금지 | `ux` G3.1, `ui` §4.1 |
| `FilterBar`, `FilterField`, `FilterActions` | `<div role="search" data-slot="filter-bar">`(후보) / `filter-field` / `filter-actions` | `FilterField`: `label`(가시), `hint?`, `htmlFor` | 가로 스크롤 없음(wrap) | `ux` G2.1 |
| `StatStrip` | `<dl data-slot="stat-strip" aria-label>` | `items[{label, value, unit?, caption?, tone?: StatusTone, href?, loading?, help?, testId?}]`, `isLoading`, `size`, `framed`(`false`), `ariaLabel` | `dt`/`dd`; 값 없음 `—`; 로딩 중 가짜 0 금지 | `ui` §2.2, `ux` G5.6 |

`StatusTone = "success" | "warning" | "destructive" | "info" | "neutral"`([ux-guide](ux-guide.md) UX-G5.1). ktdm `ok/warn/danger`는 소비자 alias.

### 4.2 Button·오류 패널(T-205)

**Button** — D-09 계약. 루트 native `<button data-slot="button">`, 스피너 `data-slot="button-spinner"`.

| prop | 기본 | 계약 |
|---|---|---|
| `type` | `"button"` | 엔진과 무관하게 **명시** 기본. 폼 제출은 `type="submit"` 명시 |
| `variant` | `"default"` | 7종: `default`·`outline`·`secondary`·`ghost`·`destructive`·`destructive-solid`·`link` |
| `size` | `"default"` | 8종: `default`(36px)·`sm`(30px)·`icon`·`icon-sm` + deprecated alias `xs`·`lg`·`icon-xs`·`icon-lg`(1 minor 후 제거 예고) |
| `loading` | `false` | `aria-disabled="true"` + `aria-busy="true"` + 스피너 + **포커스 유지**(native `disabled` 안 걺) + `onClick` 차단(`preventDefault`로 submit 차단). 라벨은 유지 |
| `disabled` | `false` | native `disabled`. `loading`과 동시면 `nativeDisabled = disabled && !loading` |
| `disabledReason` | — | 있으면 `title`로 노출. root `opacity` 흐림 금지(라벨 자식 래퍼 `opacity-55`) |
| `render` | — | `useRender` 합성(`render={<Link/>}`). `asChild`는 없다 |
| `nativeButton` | `true` | `render`로 비-button 요소를 줄 때 `false` |

회귀 위험(`ui` §3.1): pinvi 사용자 `Button`은 `loading`에 native disabled를 거는 반대 계약이므로 사용자 표면은 소비 대상이 아니다. base-ui `Button`의 `type` 기본 부여는 **미확인**이라 이 계약은 native 요소에서 명시로 보장한다(§10).

**AppErrorPanel** — `props {error, reset?, standalone?}`(map·geo·ktdm 동일 시그니처). `<div role="alert" data-slot="app-error-panel">`, `standalone`이면 `h1` 아니면 `h2`. 행동 `다시 시도`(reset) / `이전 화면`(history back). chunk/RSC/network 오류는 같은 pathname에서 1회 hard reload(`sessionStorage` 키 `reloadStorageKey`, 기본 `"kt-error-reload"`, 후보). mono 상세는 `<details>`.

### 4.3 overlay·Table·Checkbox(T-206)

| 컴포넌트 | 부분(export) | 슬롯 | 계약 | 근거 |
|---|---|---|---|---|
| `Dialog` | `Dialog`, `DialogTrigger`, `DialogPortal`, `DialogBackdrop`, `DialogPopup`, `DialogViewport`, `DialogHeader`, `DialogTitle`, `DialogDescription`, `DialogFooter`, `DialogClose` | `dialog-backdrop`, `dialog-popup`, `dialog-viewport`, `dialog-title`… | base-ui. `hasUnsavedInput`(`false`; `true`면 Esc·바깥 클릭으로 닫히지 않음), `viewportProps`(pass-through, `data-testid` 포함). 애니메이션 상태는 `data-starting-style`/`data-ending-style`/`data-open`. `DialogTitle`은 `h2`. 포커스 계약은 [ux-guide](ux-guide.md) UX-G4.8 | `ui` §3.4, D-09 |
| `AlertDialog` | Dialog와 동형 + `AlertDialogClose` | `alert-dialog-*` | `Action/Cancel` 컴포넌트 없음 → `AlertDialogClose` + `Button` 조합. 취소 초기 포커스, 동사 라벨은 호출부 책임(UX-G4.6) | `ui` §3.4 |
| `Popover` | `Popover`, `PopoverTrigger`, `PopoverPositioner`, `PopoverPopup`, `PopoverClose` | `popover-popup` | base-ui | |
| `Tooltip` | `Tooltip`, `TooltipTrigger`, `TooltipPopup`, `TooltipProvider` | `tooltip-popup` | hover 800ms / focus 0ms 기본(`delay`) | `ux` G8.1 |
| `Tabs` | `Tabs`, `TabsList`, `Tab`, `TabsPanel` | `tabs-list`, `tabs-tab`, `tabs-panel` | base-ui 이름(`Tab`/`Panel`). radix `Trigger/Content` 이름 없음 | `ui` §5.2 |
| `Breadcrumb` | `Breadcrumb`(`<nav aria-label="breadcrumb">`), `BreadcrumbList`(`<ol>`), `BreadcrumbItem`, `BreadcrumbLink`(`render` 합성), `BreadcrumbPage`(`aria-current="page"`), `BreadcrumbSeparator`(`aria-hidden`) | `breadcrumb-*` | | `ux` G1.5 |
| `HelpTip` | `HelpTip` | `help-tip` | `label` 필수 → `aria-label="도움말: {label}"`, 24px 박스 + `before:-inset-2` 40px 히트, tooltip + click popover. `mode`(`"tooltip-popover"`\|`"popover"`, 후보) | `ux` G8.1·C17 |
| `Table` 계열 | `Table`, `TableHeader`, `TableBody`, `TableFooter`, `TableRow`, `TableHead`, `TableCell`, `TableCaption` | `table-container`(`<div>` 스크롤 컨테이너), `table`, `table-row`… | `containerClassName`, `containerStyle`, `containerTestId`; `TableHeader sticky`(`false`); `TableHead scope="col"` 기본; hover는 `data-clickable` 행만; 선택 열 `[&:has([data-slot=checkbox])]:pr-0`; Card 안에서는 테두리 flush | `ui` §3.2 |
| `Checkbox` | `Checkbox` | native `<input type="checkbox" data-slot="checkbox">` | `checked`, `defaultChecked`, `indeterminate`(`false` → DOM `indeterminate` + `data-indeterminate`), `onCheckedChange(checked: boolean)`; 폼 직렬화는 native가 보장 | `ui` §3.4, D-09 |

### 4.4 DataTable·Pager(T-208)

**DataTable** — TanStack v8 헤드리스 + 표면. 루트는 `Table` 계열을 쓰므로 슬롯은 `table-container`·`table` + `data-table` 상태 슬롯.

| 영역 | prop(기본) | 계약 |
|---|---|---|
| 컬럼 | `columns: ColumnDef<TData, unknown>[]` + `meta: {align, wrap, className, headerClassName, cellClassName, headerStyle}` | 우측 정렬은 `meta.align: "right"` + `tabular-nums` |
| 정렬 | `manualSorting`(**`true`**), `sorting`/`onSortingChange`(제어형) 또는 내부 상태, `initialSorting`, `enableSortingRemoval`(TanStack 기본값 유지; 서버 정렬 목록은 `false` 권장), `enableMultiSort`(`false`) | `manualSorting: false`일 때만 `getSortedRowModel`. 헤더 버튼 `aria-sort`, `h-7`(micro-control 예외), 글리프 `aria-hidden`, `sortTestIdPrefix`(있으면 `data-testid="{prefix}-sort-{column.id}"`) |
| 선택 | `enableRowSelection`(`false`; `boolean \| (row) => boolean`), `rowSelection`/`onRowSelectionChange`, `rowSelectionLabel(row)`, `renderBulkActions(selected)` | 체크박스 `aria-label="{rowSelectionLabel} 선택"`, bulk 바 `role="region" aria-label="선택 작업"` |
| 가상화 | `virtualized`(`false`), `estimateRowSize`(40), `overscan`(12), `stickyHeader`(`false`), `containerStyle`(고정 높이 필수) | 가상 경로는 `display: grid` + `role="table"/"rowgroup"/"row"/"columnheader"/"cell"` 명시 + `aria-rowcount`; `rowTestId`는 가상 경로에도 부착 |
| 4상태 | `isLoading`(`false`) → skeleton 행 × `skeletonRowCount`(6) + 컨테이너 `aria-busy="true"` + sr-only `불러오는 중…`; `isError`/`error`/`errorTitle`/`errorState`/`onRetry`(Promise면 버튼 `loading`) → `Alert variant="destructive"` + `다시 시도`; `emptyMessage`(`"항목이 없습니다."`)/`emptyState{title, description, action, icon}` → `EmptyState`; data | 순서: loading > error > empty > data |
| 행 | `onRowClick`(Enter/Space, `tabIndex=0`, `data-clickable`), `isRowActive(row)` → `data-state="selected"`, `rowTestId(row)`, `rowIdentity(row)` | `aria-selected` 없음 |
| 접근성 | `ariaLabel`(→ `<caption>` 또는 `aria-label`), `containerTestId` | 스크롤 컨테이너 `tabIndex=0` + 이름 |
| 미포함 | 검색 툴바·`getSearchText`·`rowHeader`(geo `VirtualTable` 잔류)·`mobileCard`(pinvi 어댑터 잔류)·페이지네이션(별도) | `ui` §3.3, D-09 |

**OffsetPager / CursorPager** — `<nav data-slot="pager" aria-label="{labelPrefix} 페이지 이동">`. 버튼 접근성 이름 `"{labelPrefix} 첫 페이지"`·`이전`·`다음`·`마지막 페이지`, 요약 `페이지 n / m · 총 N건`(Cursor는 `총` 생략 가능), 경계 native `disabled`, 전환 중 `Button loading`(포커스 유지), `framed`(`false`), page-size 선택은 pager 안(`pageSizeOptions`).

### 4.5 복사·JSON·상세·상태(T-209)

| 컴포넌트 | 루트·슬롯 | prop(기본) | 계약 |
|---|---|---|---|
| `CopyButton` | `<button data-slot="copy-button">` | `value`, `label`, `onNotify?` | `aria-label="{label} 복사"`; 성공 = 아이콘 스왑 1200ms + sr-only `aria-live="polite"` `복사됨`; 실패·비보안 컨텍스트 = 인라인 상태(`data-state="error"\|"unsupported"`) + `onNotify` 호출 |
| `JsonViewer` | `<pre data-slot="json-viewer">` | `value`, `maxHeight`(`"md"`; `sm`/`md`/`lg`), `tone?`(`"destructive"`), `copyable`(`false`) | mono 12px(`text-kt-2xs`), 빈 값 `—` |
| `DetailList` | `<dl data-slot="detail-list">` | `items[{label, value, mono?, copyable?, href?, help?, numeric?}]`, `layout`(`"stacked"`\|`"inline"`), `columns`(1) | 라벨 열 8rem, `—` null glyph, `numeric`은 우측 + `tabular-nums`, `help` → HelpTip, `copyable` → CopyButton(`onNotify` 전달) |
| `StatusBadge`, `LevelBadge`, `HttpStatusBadge`, `LiveBadge` | `<span data-slot="status-badge" data-tone>` | `tone: StatusTone`, `label`; 사전 주입형(`labels`/`tones` prop 또는 `StatusLabelProvider`) | dot(`aria-hidden`) + 텍스트; `LiveBadge`는 `role="status" aria-live="polite"`; `HttpStatusBadge` mono + 2xx neutral/3xx info/4xx warning/5xx destructive. `statusLabel()` 사전은 앱 소유 |

### 4.6 헤더·스킵 링크·폼(T-210)

| 컴포넌트 | 루트·슬롯 | prop(기본) | 계약 |
|---|---|---|---|
| `AdminPageHeader` | `<header data-slot="admin-shell-header">` | `title`, `description?`, `section?`, `breadcrumbs?[{label, href?}]`, `help?`, `meta?`, `actions?` | 순서 breadcrumb/section → `h1`(+HelpTip) + actions(primary ≤1, secondary ≤2) → meta → description, 아래 hairline(`border-b`). 페이지 `h1`은 여기서만 |
| `AdminSkipLink` | `<a data-slot="skip-link">` | `targetId`(`"main-content"`) | 문구 `본문으로 건너뛰기`. `<main id={targetId} tabIndex={-1}>`는 앱이 렌더 |
| `AdminRailGrid` | `<div data-slot="admin-rail-grid">` | `rail`(ReactNode) | `xl:grid-cols-[minmax(0,1fr)_var(--kt-rail)]`, 그 아래는 1열 |
| `FormFieldInput`, `FormSelect`, `FormTextArea` | `data-slot="form-field"` | `label`, `hint?`, `error?`, `required?`, `help?`, `reserveMessage`(`true`) | 라벨 위 · 컨트롤 · 메시지 슬롯 1개 예약(error가 hint 대체), `aria-describedby`는 표시 중 메시지만, required `*` `aria-hidden` + 접근성 이름 보정 |
| `validateForm` (`form-validation`) | 헤드리스 | `rules[]` | `{errors, firstErrorField}`; 규칙 순서 = 포커스 순서 |

앱별 셸 골격(nav·접힘·로그아웃·RBAC 구성)과 `ConfirmDialog` 엔진 선택은 앱 소유다. 공용 `LoginForm`·로그인 오류/상태 슬롯의 마크업 계약은 패키지에서 제공할 수 있으며, endpoint·IdP·redirect·세션 왕복은 앱이 주입한다([ADR-015](../adr/015-common-shared-systems-scope.md), T-210·T-312). 셸·기준선 템플릿 채널은 T-211에서 별도로 다룬다.

## 5. 문구 사전

**UC-4 (MUST)** 아래 문자열은 계약이며 변경은 파괴 항목이다. 소비자 e2e는 이 문구를 그대로 단언할 수 있다.

| 키 | 문구 | 사용처 |
|---|---|---|
| `loading` | `불러오는 중…` | DataTable sr-only(pinvi e2e 잠금) |
| `copied` | `복사됨` | CopyButton sr-only live |
| `copyLabel` | `{label} 복사` | CopyButton `aria-label` |
| `empty` | `항목이 없습니다.` | DataTable `emptyMessage` 기본 |
| `retry` | `다시 시도` | DataTable 오류, AppErrorPanel |
| `back` | `이전 화면` | AppErrorPanel |
| `pager.first/prev/next/last` | `첫 페이지` / `이전` / `다음` / `마지막 페이지` | Pager 접근성 이름(`labelPrefix` 앞에 붙음) |
| `pager.summary` | `페이지 {n} / {m} · 총 {N}건` | Pager 요약 |
| `pager.nav` | `{labelPrefix} 페이지 이동` | Pager `<nav aria-label>` |
| `help` | `도움말: {label}` | HelpTip `aria-label` |
| `select` | `{label} 선택` | DataTable 행 체크박스 |
| `bulk` | `선택 작업` | bulk 바 `aria-label` |
| `skip` | `본문으로 건너뛰기` | AdminSkipLink |
| `null` | `—` | 값 없음 glyph(DetailList·StatStrip·JsonViewer) |

문구는 한국어 고정이며 i18n 훅은 두지 않는다(D-32). geo `emptyHint` 기본 `결과가 없습니다.`는 소비자가 `emptyMessage`로 넘긴다.

## 6. heading 구조

**UC-5 (MUST)**

| 위치 | heading | 제어 |
|---|---|---|
| 페이지 제목 | `h1` — `AdminPageHeader`만 만든다 | — |
| 섹션 | `SectionCard` `h{headingLevel}`(기본 `2`) | `headingLevel` |
| 카드 | `CardTitle` `role="heading" aria-level`(기본 2) | `headingLevel`(후보) |
| 다이얼로그 | `DialogTitle`/`AlertDialogTitle` = `h2` | — |
| 빈 상태·오류 패널 | `EmptyState` title은 heading 아님; `AppErrorPanel`은 `standalone ? h1 : h2` | `standalone` |
| 상세 리스트·통계 | `dl`/`dt`(heading 아님) | — |

한 페이지에 `h1`은 하나, 레벨을 건너뛰지 않는다. 접근성 이름에 배지·운영 정보를 넣지 않는다([ux-guide](ux-guide.md) UX-G1.9).

## 7. geo·pinvi·map e2e 셀렉터 대응표

**UC-6 (SHOULD)** 소비자 e2e가 잠근 셀렉터와 공통 계약의 대응이다. 이관 PR은 이 표대로 셀렉터를 바꾸거나, 전환 기간에 기존 클래스(`className`)를 그대로 넘겨 두 셀렉터가 모두 잡히게 한다. 대응 없음은 앱 잔류다.

| 앱 | 기존 셀렉터·계약(사실) | 공통 대응 | 비고 |
|---|---|---|---|
| geo | `section.panel .panel-header h2`, `[data-ui="panel"]` | `section[data-slot="section-card"] [data-slot="section-card-header"] h2` | `Panel` → `SectionCard`(`className="panel"` 유지 가능). e2e 40 스펙 회귀 주의(`inv/geo` §9) |
| geo | `pre.json-box` | `pre[data-slot="json-viewer"]` | `JsonBlock` → `JsonViewer`(`copyable`) |
| geo | `span.status` + `severityClass` `ok/warn/error` | `span[data-slot="status-badge"][data-tone]` | tone 매핑 `ok→success`, `warn→warning`, `error→destructive`; `CANCELLED` 보류 |
| geo | `.vtable-*`, `VirtualTable as="grid"` 검색 툴바·`rowHeader` | 대응 없음 | `VirtualTable` 잔류(D-09) |
| geo | `<Button asChild>` 12곳, `*Trigger asChild` 5곳 | `render={…}` | T-444 |
| geo | `AlertDialogAction/Cancel`, `TabsTrigger/Content`, `DialogPortal/Overlay/Content`, `data-[state=open]` | `AlertDialogClose + Button`, `Tab/TabsPanel`, `DialogBackdrop/Popup`, `data-open`·`data-starting-style` | `ui` §5.2 |
| geo | `.skip-link`, `data-sidebar-collapsed` | `[data-slot="skip-link"]`, 셸은 앱 잔류 | |
| pinvi | `data-testid="admin-table-scroll"` | `containerTestId="admin-table-scroll"` | `AdminTable` 어댑터가 전달 |
| pinvi | `data-testid="admin-table-sort-<key>"` | `sortTestIdPrefix="admin-table"` | 후보 |
| pinvi | `data-testid="admin-mobile-cards"` | 대응 없음 | `mobileCard`는 어댑터 잔류([responsive-web](responsive-web.md) §10) |
| pinvi | sr-only `불러오는 중…` | §5 `loading` 동일 문구 | |
| pinvi | `#admin-main-content` | `AdminSkipLink targetId="admin-main-content"` | |
| pinvi | `data-pv-surface="admin"`, `data-mobile-layout` | `data-kt-surface` 병존, 앱 속성 유지 | |
| pinvi | `Dialog hasUnsavedInput`, `viewportProps.data-testid` | 동일 이름으로 흡수 | §8 |
| map | `#main-content`, `data-slot="admin-shell-rail/header/main"`, `localStorage kor-travel-map:sidebar-collapsed` | 셸은 앱 잔류(템플릿 T-211), `AdminPageHeader`는 `admin-shell-header` 슬롯 유지 | |
| map | `[data-slot="button-spinner"]`, `[data-slot=table-container]`, `[role=checkbox]` 선택 열 | 동일 슬롯; 선택 열은 `[data-slot=checkbox]`로 교체(T-412, 호출부 3파일) | `ui` §3.2 |
| map | pager 접근성 이름 `"{prefix} 첫 페이지"`, `rowSelectionLabel` | 동일 | |
| ktdm | `data-slot="admin-shell-rail/header/main"`, `skip-link` | 동일 이름 | 셸은 앱 잔류 |

## 8. pinvi 확장의 흡수

**UC-7 (MUST)** pinvi가 이식하면서 추가한 확장 중 공통 계약으로 흡수하는 것과 앱 잔류로 두는 것(`ui` §3.3·§7-6).

| 확장 | 흡수 | 위치 |
|---|---|---|
| `Dialog.hasUnsavedInput`, `Dialog.viewportProps` | **흡수** | §4.3 |
| `Table.containerStyle`, `containerTestId`, `TableHeader.sticky`, `th scope="col"`, `data-clickable` hover | **흡수** | §4.3 |
| `DataTable.initialSorting`, `enableSortingRemoval`, `rowTestId`(가상 경로 포함), `stickyHeader`, `noUncheckedIndexedAccess` 가드, `meta.headerStyle` | **흡수** | §4.4 |
| sr-only `불러오는 중…` | **흡수** | §5 |
| `data-pv-surface` 토큰 스코프 | 병존(앱 속성), 공통은 `data-kt-surface` | §3 |
| `AdminTable`(`manualSorting=false`, `serverSort`, `virtualizeThreshold`, `maxHeight`, `mobileCard`), `AdminPage`/`Section`/`FilterBar` 어댑터, `DataTable.tsx` shim | 앱 잔류 | pinvi 소유 |
| Checkbox native + `forwardRef` | native는 흡수, `forwardRef`는 React 19 ref prop으로 대체 | §4.3 |
| 사용자 UI(`ui/Button`, `ui/Dialog`, `ui/ConfirmDialog`) | 소비 대상 아님 | D-29 |

## 9. SemVer 0.x 파괴 항목

**UC-8 (MUST)** D-31 결정의 적용이다. 릴리스 절차는 [release runbook](../runbooks/release.md), 버전 레지스트리는 [versions.md](versions.md).

| 구분 | 항목 | 버전 |
|---|---|---|
| 파괴(minor, 0.x) | 토큰 이름·의미 변경, `data-slot` 이름 변경·삭제, testid prop 이름 변경, §5 문구 변경, prop 기본값 변경(예: `manualSorting`·`type`·`headingLevel`·`emptyMessage`), 정렬 모드 의미 변경, export 이름 변경·삭제, CSS 파일 경로 변경, peer 범위 축소, deprecated alias 제거, heading 레벨 변경 | `0.N+1.0` + `-rc.N` → 소비자 PR 검증 → 정식. CHANGELOG `### Breaking` + 이관 절 필수 |
| 비파괴(patch) | 선택 prop 추가, 새 컴포넌트·subpath 추가, 슬롯 **추가**, variant 추가, 내부 클래스·DOM 깊이 변경, 버그 수정(계약 유지) | `0.N.M+1`(additive) |
| 폐기 | 토큰 이름·prop 폐기는 1 minor 동안 alias·경고 유지 후 다음 minor에서 제거 | 예고 → 제거 |
| 독립 버전 | tokens·ui·py는 독립 버전. ui는 `@kor-travel/tokens`의 호환 minor 하나를 peer | 구체적 호환 조합은 [packages](../architecture/packages.md) UI 절·ADR-013 |
| 1.0 | GPL 소비자 3곳 채택 후 | — |

파괴 항목 여부가 애매하면 파괴로 본다. 소비자 e2e·계약 테스트가 먼저 깨지도록 계약 테스트(§11)를 유지한다.

## 10. base-ui 미확인 3건(릴리스 차단)

**UC-9 (MUST)** 아래 3건은 T-201에서 base-ui 소스로 확인하기 전 릴리스하지 않는다(D-09).

| # | 미확인 | 이 계약의 대응 |
|---|---|---|
| 1 | base-ui `Button`이 `type="button"`을 기본 부여하는지(pinvi 주석 근거만) | native `<button>`에 명시 기본이므로 엔진과 무관. 확인 결과는 evidence로 기록 |
| 2 | base-ui `Checkbox`가 폼 제출 시 hidden input을 두는지 | native `<input>` 채택으로 회피 |
| 3 | base-ui Toast API | 토스트는 앱 소유. `onNotify` 주입만 |

## 11. 검증

**UC-10 (MUST)**

| 검사 | 도구 | 내용 |
|---|---|---|
| 계약 단위 테스트 | Vitest + RTL + jsdom(`packages/ui`) | 컴포넌트마다 슬롯·기본값·문구·ARIA·heading을 단언. map `data-table.test.tsx`(175줄)·pinvi `AdminTable*.test.tsx`(418줄)를 이관 출발점으로 |
| 타입 | `tsc` `noUncheckedIndexedAccess` | |
| 스모크 | consumer-smoke(패키지별 승인 소비자 pinned SHA, webpack + Turbopack) | `kt-` 유틸리티 생성·지시문 보존 |
| 드리프트 | `tools/ui_drift.py`(T-211) | npm 소비자의 로컬 패치 사본 탐지. 우회 패치 ≥2 → 배포 방식 재검토(D-28) |
| 이관 evidence | 소비자 e2e(map 30·pinvi 56·geo 23) + §7 셀렉터 diff | 채택 PR 본문 |

## 12. 열린 결정

| # | 항목 | 기본값(이 문서) |
|---|---|---|
| O-1 | pinvi 라이선스(L6) | ui 1차 소비자 = map + pinvi admin; L6 미결이면 airport 소형 부품으로 대체(D-16) |
| O-3 | UI 배포 방식 | npm 1차 |
| O-22 | dirty 이탈 경고 | Dialog `hasUnsavedInput`만 흡수, `beforeunload` 규칙 없음 |
| — | 컴포넌트별 subpath, `sortTestIdPrefix`, `reloadStorageKey`, `HelpTip.mode`, `FilterBar role="search"`, `CardTitle headingLevel`, Badge variant 목록 | 후보. T-201·T-203·T-204 확정 |
| — | ConfirmDialog 공통 API(4종 공존) | 미포함, T-508 |

## 13. 근거

- 컴포넌트 매트릭스·계약 차이·회귀 위험·엔진·등록 방식: [ui-components 조사](../survey/cross/ui-components.md) §2~§7.
- 행동 규칙(셸·목록·피드백·상태·도움말): [ux-patterns 조사](../survey/cross/ux-patterns.md) §1·§2.
- geo e2e 셀렉터 계약: [geo 인벤토리](../survey/inventory/kor-travel-geo.md) §3·§9.
- pinvi testid·어댑터·`cn`·tsconfig: [pinvi 인벤토리](../survey/inventory/pinvi.md) §3·§8.
- map DataTable·ESLint·슬롯 이름: [map 인벤토리](../survey/inventory/kor-travel-map.md) §3·§8, [ktdm 인벤토리](../survey/inventory/kor-travel-docker-manager.md) §3.
- 결정: [설계 브리프](../plan/design-brief.md) D-01·D-09·D-10·D-16·D-29·D-31·D-32, O-1·O-3·O-22.
