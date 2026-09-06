# 횡단 비교 — UX 패턴·PC/Mobile 웹 규약

- 작성일: 2026-09-06
- 상태: **읽기 전용 조사 결과**. 조사 대상 저장소는 수정하지 않았고, 이 문서 외 산출물은 없다.
- 목적: `kor-travel-common`이 정의할 **공통 UX 가이드**와 **PC/Mobile Web 규약**의 근거를 각 앱의 현행 코드·설계 문서에서 모으고, 앱 간 충돌 규칙을 드러낸다.
- 표기: 각 주장에 `사실`(코드/문서에서 직접 확인) / `후보`(공통화 제안, 근거는 있으나 합의 필요) / `추정`(근거로부터의 추론) / `미확인`(이번 조사에서 확인하지 못함)을 붙인다.
- 약칭: kta = kor-travel-airport, ktc = kor-travel-concierge, ktdm = kor-travel-docker-manager, geo = kor-travel-geo(kor-travel-geo-ui), map = kor-travel-map(kor-travel-map-admin/frontend), weather = kor-travel-weather(kor-travel-weather-admin/frontend), pinvi-admin = pinvi apps/web `(admin)`, pinvi-user = pinvi apps/web 사용자 표면, pinvi-mobile = pinvi apps/mobile(Expo).

## 0. 기준

### 0.1 조사 커밋

| 저장소 | 로컬 정본 체크아웃 | 기준 커밋 | 조사한 프론트엔드 루트 |
|---|---|---|---|
| kor-travel-airport | `F:/dev/kor-travel-common-survey/kta-main` | `2bb1111` | `frontend/` |
| kor-travel-concierge | `F:/dev/kor-travel-concierge` | `7945305` | `frontend/` |
| kor-travel-docker-manager | `F:/dev/kor-travel-common-survey/ktdm-main` | `862562d` | `frontend/` |
| kor-travel-geo | `F:/dev/kor-travel-geo-fixes` | `1d9d74d` | `kor-travel-geo-ui/` |
| kor-travel-map | `F:/dev/kor-travel-common-survey/ktm-main` | `c494e227` | `packages/kor-travel-map-admin/frontend/` |
| kor-travel-weather | `F:/dev/kor-travel-weather` | `6003da9` | `packages/kor-travel-weather-admin/frontend/` |
| pinvi | `F:/dev/kor-travel-common-survey/pinvi` | `9af25e5` | `apps/web/`, `apps/mobile/`, `packages/design-tokens/` |
| canview(구조 참조) | `F:/dev/canview` | (커밋 미기록, 구조만 참조) | `AGENTS.md`, `docs/ui/design.md` |

선행 보고서 `F:/dev/kor-travel-geo-fixes/docs/kor-travel-common-library-review.md`(2026-09-05)는 §1.14에서 관련 사실을 재검증했다. 그 보고서의 map 기준 커밋(`c72456f`)은 이번 조사 커밋(`c494e227`)보다 이전이다.

### 0.2 방법

- 각 저장소에서 `git log -1`로 커밋을 확인하고 `find`로 프론트엔드 파일 목록을 만들었다(`node_modules`, `.next`, `vendor` 제외).
- 셸·헤더·목록·상세·피드백·상태·로그인·도움말·복사·JSON·지도 컴포넌트를 `sed`/`cat`으로 읽었다(큰 파일은 머리 부분과 필요한 절만). `design.md`/`DESIGN.md`/`DESIGN-RULES.md`/`tokens.css`/`globals.css`의 토큰·브레이크포인트·reduced-motion 절을 읽었다.
- 패턴 사용 파일 수는 `grep -rlE`로 집계했다(스크립트: 세션 scratchpad `count.sh`; 대상 확장자 `.ts/.tsx/.css`, `e2e`/`tests`/`vendor` 제외). 파일 수는 "그 문자열이 나오는 파일 수"이며 사용 빈도·정확성을 뜻하지 않는다(주석 언급 포함).
- 브라우저 실행·스크린샷·실제 뷰포트 검증은 하지 않았다. 반응형 서술은 전부 CSS/JS 소스와 설계 문서 기준이다.
- `F:/dev/maplibre-vworld-react`, `maplibre-vworld-js`는 파일을 열지 않았고, 각 앱의 `package.json`·컴포넌트 주석에서 참조 관계만 확인했다.

## 1. 앱별 비교표

### 1.1 Admin shell 레이아웃

| 항목 | map | ktc | geo | ktdm | weather | pinvi-admin | kta |
|---|---|---|---|---|---|---|---|
| 셸 파일 | `src/components/admin-shell.tsx` (510줄) | `src/components/AppShell.tsx` (360줄) | `components/layout/AppShell.tsx` (347줄) + `components/ui/PageHeader.tsx` | `src/components/layout/AppShell.tsx` (259줄) | `components/admin-shell.tsx` (152줄, `PageHeader` 동봉) | `app/(admin)/admin/layout.tsx` (325줄) + `components/admin/admin-shell-parts.tsx` | 없음 — 단일 대시보드 `dashboard-app.tsx`/`dashboard-screen.tsx` (사실) |
| 스타일 방식 | Tailwind v4 유틸 + `@theme inline` | Tailwind v4 유틸 + `tokens.css` | 클래스 CSS(`.app-shell .sidebar .content`) + Tailwind v4 토큰 | 클래스 CSS(`.app-shell .sidebar .page-head`) + Tailwind v4 `@theme` | 클래스 CSS(`.app-grid .rail .main`), Tailwind 미사용(사실, `package.json`) | Tailwind v4 유틸 + `@config` v3 preset | 클래스 CSS + `tokens.css`(OKLCH), Tailwind 미사용 |
| 데스크톱 rail 폭 / 접힘 | `lg:grid-cols-[16rem_…]` / `4rem` | 16rem / 4rem | CSS 클래스(수치 미확인) / 접힘 상태 `data-sidebar-collapsed` | 16rem / 4rem (DESIGN.md §반응형) | `--rail: 17rem`(tokens.css) / **접힘 없음**(코드에 collapsed 상태 없음, 사실) — design.md는 "16rem·4rem 접힘"이라 적어 **문서와 코드 불일치**(사실) | `lg:w-64`(16rem) / `lg:w-20`(**5rem**) | 해당 없음 |
| 접힘 상태 저장 | `localStorage kor-travel-map:sidebar-collapsed` | `kor-travel-concierge:sidebar-collapsed` | `kor-travel-geo:sidebar-collapsed` | `kor-travel-docker-manager:sidebar-collapsed` (try/catch) | 없음 | `pinvi.admin.sidebar.collapsed` | 해당 없음 |
| 셸 전환 breakpoint | `lg`(1024px) | `lg`(1024px) | `(max-width: 1023px)` | `(max-width: 63.999rem)`(=1024px) | `(max-width: 62rem)`(=992px) | `lg`(1024px) | JS `innerWidth < 860` + CSS `max-width: 860px` |
| 좁은 화면 셸 | 상단 가로 스크롤 nav strip(`overflow-x-auto`), 로그아웃은 상단 아이콘 | 동일(map 이식) | **off-canvas drawer** `min(280px,84vw)`, 상단 56px topbar, backdrop, 닫힘 시 `inert`, focus trap, body scroll lock | 상단 가로 nav strip(sticky) | 상단 가로 nav strip(`position: static`) | 상단 가로 strip, 항목은 **44px 아이콘 전용**(`h-11 w-11`, 라벨 sr-only) | 셸 없음(페이지 폭 `min(100% - 24px, 720px)`) |
| skip link / `<main tabIndex=-1>` | 있음 (`#main-content`) | 있음 | 있음(`.skip-link`) | 있음 | 있음(`.skip-link`) | 있음(`AdminSkipLink`, `#admin-main-content`) | 없음(미확인: grep에서 skip-link 없음) |
| 본문 패딩 | `px-6 py-6` | `px-4 py-5 lg:px-6 lg:py-6` | `.content` (모바일 `18px 16px 40px`) | `.content` | `.main` | `px-4 py-6 sm:px-6 lg:px-8 lg:py-8` | 페이지 셸 폭 제한 |
| 우측 inspector rail | `--rail: 22rem`, `xl:grid-cols-[minmax(0,1fr)_var(--rail)]` | 미확인(토큰 `--spacing-rail` 미발견) | 없음(패널 그리드 `.grid.two/.three`) | 없음(모달 중심) | design.md "right inspector"(weather 페이지), 폭 미확인 | `AdminRailGrid` (`--spacing-rail: 22rem`, xl 2열) | 없음 |
| 인증 게이트 위치 | 없음(ADR-005/035, intranet) — `layout.tsx` 주석 | 프록시/`proxy.ts`(미확인 세부) | `session-guard.ts`(미확인 세부), 로그인은 셸 밖 | `LoginScreen` 컴포넌트 분기(단일 라우트) | `middleware.ts`(미확인 세부), 로그인은 셸 밖 | 클라이언트 `AdminGuard`: `me()` 쿼리 + roles `admin/operator/cpo`, pending 시 "권한 확인 중…" 텍스트 | 없음(무인증, design.md "no-auth internal backup/restore tool") |

사실: map·ktc·ktdm·weather·pinvi-admin의 좁은 화면 셸은 모두 "상단 가로 strip"이고 geo만 drawer다. geo는 drawer의 `inert`/focus 순서 문제를 단위 테스트(`tests/unit/app-shell-drawer.test.tsx`)로 고정한다.

### 1.2 네비게이션·breadcrumb·헤더 밴드

| 항목 | map | ktc | geo | ktdm | weather | pinvi-admin | pinvi-user |
|---|---|---|---|---|---|---|---|
| nav 정본 | `NAV_GROUPS` 5그룹 19항목(셸 파일 내) | `navGroups` 4그룹 7항목 | `lib/admin-pages.ts` `ADMIN_PAGES`/`ADMIN_NAV_GROUPS` + debug 4링크(셸 내) | `navGroups` 4그룹(링크 + **모달 여는 버튼** 혼합, `⌘K` 힌트) | `NAV_ITEMS` 8항목 **평면**(그룹 없음) — design.md "same grouped rows"와 불일치(사실) | `NAV_GROUPS` 3그룹 31항목, `(Sprint N)`가 aria-label/title에 포함 | `NAV_ITEMS` 7 + 모바일 1순위 4 |
| 활성 판정 | longest-prefix(`isActive`) | `lib/nav.ts pickActiveNavHref`(단위 테스트) | `DocumentNavLink`(활성 표시 세부 미확인) | `window.location.hash` 기준 | longest-prefix | longest-prefix(`getActiveNavHref`) | 경로별 규칙(`/settings/*` 묶음) |
| 활성 표현 | `bg-brand-tint` + 좌측 2px brand mark + `aria-current="page"` | 흰 배경 + 2px brand mark(짙은 rail 위) | `aria-current`(CSS 미확인) | `aria-current` | `.active` + `aria-current` | **`bg-ink text-canvas` 채움**(2px mark 없음) | ink 2px 밑줄(데스크톱) / 하단 탭 6px×2px 바(모바일) |
| 링크 방식 | `next/link` | `next/link` | `DocumentNavLink`(문서 내비게이션, T-278) | `<a href="#…">` + onClick | `next/link` | `DocumentNavLink`(geo T-278 이식) | `next/link` |
| breadcrumb | `breadcrumbs?: {label, href?}[]` → `ui/breadcrumb.tsx`; 없으면 section 라벨 1줄 | 없음(section 라벨만) | 없음(section 라벨 자동 유도 `sectionForPath`) | 없음(`section` prop 기본 '개요') | 없음 — `page-path`에 **현재 pathname 문자열**을 표시(사실) | `AdminPageHeader`(map 이식)에 breadcrumbs 있음, `breadcrumbs=` 사용 페이지 0(집계) → 레거시 `AdminPage`(h1 `text-2xl`)와 **헤더 2종 공존**(사실) | 없음 |
| 헤더 밴드 구성 | breadcrumb/section → h1(+HelpTip) + actions(primary ≤1, secondary ≤2) → meta → description, `border-b` flush, `px-6 pt-5 pb-4` | section → h1 + actions → description | section → h1 + actions → meta → description(map 이식 명시) | section(eyebrow) → h1 + actions → meta → description | section + pathname → h1 + actions → description | 두 종류(위) | 헤더 = 워드마크 + 탭 |
| 로그아웃 위치 | rail footer(≥lg) / 상단 아이콘(<lg) | 동일 + `JobStatusLink` | rail footer | rail footer + 상단 아이콘, nav에도 항목 | rail footer + 실패 시 인라인 `role="alert"` | 없음(집계 범위에서 로그아웃 버튼 미확인) | 없음(프로필/설정 경로) |

### 1.3 목록 화면 패턴

| 항목 | map | pinvi-admin | geo | ktc | ktdm | weather | kta |
|---|---|---|---|---|---|---|---|
| 필터 바 | `filter-bar.tsx`: `FilterBar`(wrap, `items-end`) / `FilterField`(가시 라벨 위, hint 아래) / `FilterActions`; 가로 스크롤 금지, 정렬은 컬럼 헤더만, page-size는 pager 쪽 | `components/admin/filter-bar.tsx` 이식(색 토큰만 치환) + `AdminPage.FilterBar` 위임(23페이지 호환) | `Panel` 안 `NativeSelect`/`Checkbox`; `VirtualTable` 툴바 검색 | `review-list-state.ts`(URL 상태) + 검색 패널; 공용 FilterBar 파일 없음(사실) | 없음(단일 원장 + 그룹 필터 미확인) | 검색 input(`LocationAdmin`) | 공항/주차장 select(control band) |
| 표 컴포넌트 | `ui/data-table.tsx` (TanStack, 799줄): 기본 `manualSorting=true`, skeleton 행 + `aria-busy`, 빈 상태 `EmptyState`, 오류 Alert(what/why/what-to-do + `다시 시도`), 선택 opt-in(`rowSelectionLabel`, `renderBulkActions`), 가상화 시 명시 ARIA grid, `meta.align:right` | `AdminTable` 어댑터(36페이지) → DataTable: **`manualSorting=false`** 기본, `serverSort` opt-in(T-357), `mobileCard`(pinvi 고유), sr-only `불러오는 중…` 유지 | `ui/VirtualTable.tsx`: `VirtualColumn` 계약, 클라이언트 검색·정렬, `as="grid"`(가상화, 기본) / `as="table"`(시맨틱), `emptyHint` | shadcn `Table` + 체크박스 선택(`REVIEW_BULK_SELECTION_MAX`) | 서비스 원장 `<table>`; ≤48rem에서 보관 이력 표를 block 행으로 | 일반 `<table>`(sync-runs) / `article.panel.dataset-row` 카드 | 데스크톱 `<table>` / 모바일 `lot-card` 카드(사실) |
| 페이지네이션 | `pagination-bar.tsx` `OffsetPager`/`CursorPager`: 라벨 `첫 페이지/이전/다음/마지막 페이지`, 요약 `페이지 n / m · 총 N건`, 전환 중 `Button loading`(포커스 유지), 경계는 native disabled, `framed` 기본 off | 이식(동일 aria 규약) | 공용 pager 없음(파일 목록에 없음, 사실) | 미확인(공용 파일 없음) | 없음 | `offset`/`PAGE_SIZE=100` 상태(UI 미확인) | 없음 |
| 정렬 | 서버 정렬 기본, 컬럼 헤더 버튼 `h-7`(28px, 닫힌 예외 목록) | 클라이언트 정렬 기본(현재 페이지 안에서만 유효함을 주석으로 경고) | 클라이언트 `sortValue` | 미확인 | 미확인 | 없음 | 없음 |
| 선택/bulk | `enableRowSelection` 3파일, `renderBulkActions` 2파일 | 각 1파일 | `headerCell`로 select-all | `ReviewBulkPanel`: AlertDialog + 진행 요약(total/processed/succeeded/conflicts/failed), 모바일 sticky 하단 바 + `env(safe-area-inset-bottom)` | 그룹 재시작(확인 후) | 없음 | 없음 |
| 행 선택 idiom | `selectable-row.tsx`: `role="listbox"/"option"`, roving tabindex, ↑↓/Home/End, 선택 = brand-tint + 2px mark, `disabledReason` 흐리지 않음 | 미확인(이식 목록에 없음) | `onRowClick` + `getRowClassName` | `CandidateTable` 행 클릭 | 행 안 액션 버튼 | 지도 마커/목록 | 없음 |
| 빈 상태(표 안) | `emptyState` prop → `EmptyState` | `empty='항목이 없습니다.'` 계약 유지 | `emptyHint='결과가 없습니다.'` | 미확인 | `EmptyState` `<p>` 가운데 정렬(모달) | `.empty` div | `notice` |
| 키보드 단축키 | 없음(확인 범위) | `useReviewKeyboard`: J/K, 1–9, Enter, X, U, `/`, `?`; IME·modifier·편집 요소 가드 | 없음(확인 범위) | `⌘/Ctrl+K` 명령 팔레트, 모달 탭 ←→ 포커스 이동 | 없음 | 없음 | 없음 |

### 1.4 상세/편집 패턴

| 항목 | map | pinvi-admin / pinvi-user | geo | ktc | ktdm | weather / kta |
|---|---|---|---|---|---|---|
| 섹션 컨테이너 | `SectionCard`(Card 헤더 `border-b` + flat body, `headingLevel`, containment 1층 — 카드 안 카드 금지) | admin: 이식 + `AdminPage.Section` 위임(20페이지); user: `SettingsSurface`(hairline rule 섹션, 표 대신 row divider 리스트) | `Panel`(`section.panel` + `.panel-header h2`, badges 슬롯, actions `min-w-0` wrap — #514) | `SectionCard`(map과 동일 구조·props, Hallmark 스탬프 없음) + `panels.tsx Section/Panel` | `ops-*` 클래스 패널, 모달(`ops-modal`) 중심 | weather `.panel`; kta `.metric-card`/`table-surface` |
| 상세 dl | `DetailList` `stacked`/`inline`(라벨 열 8rem 고정, `—` null glyph, `mono`, `copyable`, `href`, `help`, `numeric` 우측 정렬) | admin: 이식 | `KeyValueGrid`(`dl.criteria-grid`, `help`) | `DetailSection`/`DetailRow`(label/value 한 행, truncate) | `Row`(dt/dd 그리드, `—`) | weather `metric-rows`; kta `detail-ribbon` |
| 폼 필드 | `FormField`(라벨 위 · 컨트롤 · 메시지 슬롯 1개 **항상 예약**(`reserveMessage`), error가 hint 대체, `aria-describedby`는 표시 중 메시지만, required `*` aria-hidden + 명시 `aria-label` 보정, `help`→HelpTip) | admin: 이식; user: `forms/FormField`(`min-h-11`, `text-base` 16px, hint/error 같은 슬롯, `role=alert`) | shadcn `Field`/`FieldError` + react-hook-form/zod(deps) | shadcn `Field` + react-hook-form/zod(deps), `field-variants.ts` | `ops-field`/`ops-input`, 필드별 오류 `id=…-error` + `aria-live` | weather/kta: 기본 `<label><input>` |
| 검증 | `lib/form-validation.ts validateForm`(규칙 순서 = 포커스 이동 순서, `firstErrorField`) | `@pinvi/domain validateForm(zodSchema)` → `firstField` 포커스 | zod + rhf | zod + rhf | `configValidation.ts` | 없음(미확인) |
| 저장/취소·diff | 폼 knob "한 저장 행 끝에"(design.md) | admin category-mapping: `isDirty`로 저장 버튼 활성(사실, 1파일) | 위저드(RestoreWizard) | `RecurringEditDialog` 등 | 저장 전 **변경 전/후 diff 미리보기**(`configDiff.ts`, `- 포트`, `row.before`) | 없음 |
| dirty 이탈 경고 | `beforeunload` 0건(집계) | 0건 | 0건 | 0건 | 0건 | 0건 |

사실: 조사한 8개 표면 어디에도 `beforeunload` 기반 dirty 이탈 경고가 없다. 공통 규칙으로 정할지 여부는 열린 질문이다(§5).

### 1.5 피드백 — 토스트·인라인 오류·오류 패널·빈 상태·스켈레톤·확인·undo

| 항목 | map | pinvi-admin / pinvi-user | geo | ktc | ktdm | weather / kta |
|---|---|---|---|---|---|---|
| 토스트 엔진 | `sonner` (`ui/sonner.tsx`, top-right, `richColors` 없음, 아이콘 모양 + 상태 토큰 색) | **없음**(copy-button 이식 주석 "토스트 시스템 자체가 없다") — 인라인 `role=alert` 69파일 | 자체(`radix-ui Toast` + zustand `lib/toast.ts`): success/error/info, error 8000ms·기타 4000ms, 최대 5개, bottom-right | 없음(`SettingsPanel.tsx`에 문자열 1건, 미확인) — `ReviewUndoSnackbar` 사용 | 자체 `Toast.tsx`: success 6초 자동 닫힘, **error는 사람이 닫을 때까지 유지**, raw 원문 접기, error=`role=alert`/success=`role=status` | 없음(인라인 `.error[role=alert]`) / kta `.notice`, backup-panel에 `aria-live`·`role=alert` |
| 토스트 정책 | "silent success" — 자기 영역이 다시 그려지는 mutation은 토스트 없음, 교차 페이지 효과만(design.md §Microinteractions) | user DESIGN.md: 성공은 조용히(`role=status`), 축하 토스트 없음 | 미확인(정책 문서 없음) | — | 성공/실패 모두 토스트 | — |
| 인라인 오류(모달 내) | `Alert` what/why/what-to-do 3부(`AlertTitle/Description/Actions`), 성공 Alert 없음 | admin: `alert.tsx` 이식 | `Alert` | `role=alert` 16파일 | `InlineError`(제목·힌트·**요청 ID 상시 노출**·raw 접기) | — |
| 런타임 오류 패널 | `app-error-panel.tsx`: chunk/RSC/network 오류 같은 pathname 1회 hard reload(sessionStorage 플래그), 3부 구조, `다시 시도`/`이전 화면`, `role=alert`, mono 상세 접기 | `feedback/RouteError` + `FullPageMessage`(같은 `lib/error-recovery`, `claimErrorReloadAttempt`) | `layout/AppErrorPanel.tsx`(원천, PR #391/T-278) | `layout/AppErrorPanel.tsx`(동일 계보) | `layout/AppErrorPanel.tsx`(동일 계보) | weather·kta: `error.tsx` 없음(파일 목록, 사실) |
| 빈 상태 | `EmptyState`: 좌측 정렬, 제목 1문장 + 이유 1문장 + 행동 1개, `framed` 기본 off, dashed/가운데/아이콘 타일 금지 | admin: 이식; user: `FullPageMessage`(좌정렬, `border-t-2 border-ink` rule) | `EmptyState` = `<p class="py-2 text-sm">`(문구는 호출부 계약) | 미확인 | `EmptyState` `<p class="text-center">` | weather `.empty` div; kta `notice` |
| 스켈레톤 | `Skeleton`(`aria-hidden`, `motion-reduce:animate-none`; 로딩은 감싸는 영역 `aria-busy`) — 24파일 | admin 8파일(이식) / user `PageLoading` 스피너 카드 | `skeleton.tsx` 17파일 | 없음(스피너, reduced-motion에서도 회전 유지) | 없음 | weather `.skeleton` 2파일 / kta 없음 |
| 확인 다이얼로그 | `useConfirm`(AlertDialog Provider): **`확인/OK/Yes` 라벨을 타입+런타임에서 거부**, 취소 초기 포커스, destructive fill은 다이얼로그 안에서만 — 단 `curation-collections-client.tsx`에 `window.confirm` 2건 잔존(사실) | admin: 미확인(useConfirm 이식 없음); user: `ui/ConfirmDialog`(custom portal + `useModalDialog`, `tone='danger'`, **기본 라벨 `'확인'`**, busy 스피너, 취소 초기 포커스) | `ConfirmActionDialog`(radix AlertDialog, `RoleRequirementNote`, `TypedConfirmField` 게이트, 기본 라벨 `"실행"`) | `ConfirmActionButton`(base-ui AlertDialog, 기본 라벨 `"삭제"`) | `window.confirm` 3파일(영향 범위 카운트 + PostgreSQL 경고 문구 포함) | weather `window.confirm`(API 키 삭제) / kta `window.confirm`(복원) |
| undo | design.md: 멱등 쓰기는 optimistic + Undo(구현 미확인) | user DESIGN.md: 가역 = 즉시 실행 + Undo(구현 미확인) | 없음(확인 범위) | `ReviewUndoSnackbar`(`role=status aria-live=polite`, 마지막 1건만 되돌림, 오류 `role=alert`) + `lib/review-undo.ts` | 없음 | 없음 |
| 모달 엔진 | `@base-ui/react` Dialog/AlertDialog/Popover(패널 `focus-visible:outline-0` 닫힌 목록 4개) | admin: base-ui(`RestoreHotswapDialog` 주석: "두 모달 스택을 섞지 않는다"); user: `useModalDialog`(focus trap, Escape, scroll lock 참조 카운트, 포커스 복원) | `radix-ui` + `use-modal-a11y.ts`(T-227) | base-ui | 자체(`role=dialog aria-modal`, Escape, 초기 포커스, backdrop blur 금지) | weather/kta: 모달 미확인 |

### 1.6 상태 표현(status badge 의미·색)

| 앱 | 정본 | tone 집합 | 라벨 규칙 | 비고 |
|---|---|---|---|---|
| map | `lib/status-label.ts`(375줄) `STATUS_LABELS`/`STATUS_TONE`/`httpStatusTone` | `success/warning/destructive/info/neutral` | enum raw 렌더 금지, `statusLabel()` 단일 정본, **같은 한글 라벨은 같은 tone**(테스트로 잠금), 정상 취소 = neutral, HTTP 2xx neutral·3xx info·4xx warning·5xx destructive | `StatusBadge`(dot + 라벨), `LevelBadge`, `HttpStatusBadge`(mono), `LiveBadge`(`role=status aria-live=polite`) |
| pinvi-admin | `lib/admin/status-label.ts`(387줄, 값 무변경 이식, `tests/adminStatusLabel.test.ts`) | 동일 | 동일 | `status-badge.tsx` 이식 |
| geo | `lib/consistency.ts severityClass` | `ok/warn/error` 3종 | `ERROR/FAILED→error`, **`WARN/CANCELLED→warn`**, 그 외 ok; `StatusBadge`는 값 문자열을 그대로 표시 | map과 취소 의미 충돌(§4) |
| ktdm | `lib/containerPresentation.ts STATUS_LABELS`(running→실행 중 …, 미매핑은 원문) | `StatStrip` tone `ok/warn/danger/info/neutral` | 표시는 한국어, 원문은 `title` | 상태색은 dot·배지·수치 강조에만(DESIGN.md) |
| ktc | `lib/display-labels.ts`(`groundingStatusBadgeVariant`, `queueReasonBadgeVariant`) | Badge variant `success/warning/info/neutral/destructive`(map과 이름 동일) | 도메인별 매핑 함수 | 미확인: 라벨 유일성 테스트 |
| weather | 없음 — `lastRun.status` **raw 문자열** + `.status.on/.off`(사실, `app/page.tsx:100`) | on/off | 없음 | map 규칙("enum never raw") 위반 상태 |
| kta | `statusTone`/`statusLabel`(dashboard-screen.tsx) | `full/critical/warning/busy/stable` → `tone-*` | 만차/10대 미만/50대 미만/여유 적음/원활 | 도메인 임계값 기반 5단계, 공통 5-tone과 1:1 아님 |
| pinvi-mobile | 화면 로컬 `STATUS_LABELS`(trips) | `Badge` 중립 1종 | — | 색 의미 없음 |

### 1.7 위험 작업(백업/복원/컨테이너 제어) UX

| 앱 | 대상 작업 | 확인 방식 | 진행/결과 표현 | 권한·게이트 |
|---|---|---|---|---|
| geo | DB 백업·복원·Hot-swap | `RestoreWizard` 4단계(`1. 백업·모드 선택 → 2. manifest 미리보기 → 3. dry-run 검사 → 4. 확인·실행`, `WizardSteps aria-current="step"`) + `TypedConfirmField`(정확 문구 입력, 복사 버튼 의도적 부재, 일치 여부 `aria-live`) + `ConfirmActionDialog` | `JobProgress`, `use-job-events`(SSE, 미확인 세부), toast | `RoleRequirementNote`(백엔드 require_role 안내) |
| pinvi-admin | 백업 스냅샷 복원(hot-swap) | `RestoreHotswapDialog`(base-ui Dialog) | 5단계 phase 목록(`preparing/restoring/validating/draining/switching`) 아이콘 상태 | 기능 플래그 `NEXT_PUBLIC_PINVI_RESTORE_HOTSWAP_UI_ENABLED='1'` |
| ktdm | 컨테이너 start/stop/restart, 그룹 재시작, target 재생성(`compose up --build`), 설정 원복, 백업 복원 | `window.confirm` — 문구에 **영향 대상 수와 이름**(`대상 N개: …`), PostgreSQL 포함 시 스키마·권한 스크립트 경고, 백업은 `durationWarning(role)` | 인라인 `ensureState`/`InlineError`(요청 ID), 토스트 | target 재생성 버튼은 `NODE_ENV !== 'production'`에서만 노출(주석: "유일한 방어선", 서버 미차단 T-044) ; CLI 전용 작업은 `CopyableCommand`로 명령 원형 제시 |
| map | 백업 | `backups-client.tsx`에 `Alert variant="destructive"`(사실); 확인 메커니즘 미확인 | 미확인 | 없음(intranet) |
| kta | PostgreSQL dump 생성/다운로드/복원 | `window.confirm("현재 PostgreSQL 데이터를 덮어씁니다. 복원 전에 자동 백업을 만든 뒤 계속할까요?")`; `.dump`만 허용, 내부망 경고 문구(design.md) | `backup-panel-message`(`aria-live`), `role=alert` | **무인증** |
| weather | API 키 삭제 | `window.confirm` | 인라인 | 세션 로그인 |
| ktc | 검수 bulk ignore/delete/reopen | `ReviewBulkPanel` AlertDialog + 진행 요약 + undo | 스낵바 | 세션 로그인 |

### 1.8 로그인 화면

| 앱 | 구조 | 오류 표현 | 진행 상태 | 기타 |
|---|---|---|---|---|
| map | 단일 가운데 열, 타이포 워드마크, **카드 프레임·아이콘 타일 없음**, footer 위 hairline(design.md login knob) | CTA 위 **항상 렌더되는 live region 슬롯**(M13) | `Button loading`(aria-disabled, 포커스 유지) + `if (busy) return` | 로그인 시 `clearDomainIdempotencyKeys()` |
| ktc | 동일 형태(`Field`/`Input`), 워드마크 텍스트 | `ERROR_MESSAGES` 코드→문구 맵 | `pending` | `router.replace(next)` |
| geo | `login-shell/login-panel`, **`LockKeyhole` 아이콘 타일**(map 감사가 지적한 "icon-in-tinted-square" 형태) | HTTP 상태별 문구(503/429/403/기타) | `aria-busy` form, 입력 disabled | 셸 밖 렌더 |
| weather | geo와 거의 동일 마크업 | 상태별 + 서버 `detail` 우선 | 동일 | `sanitizeLocalPath`로 open-redirect 차단(로그인 커밋 `6003da9` "match kor-travel-geo session login boundary") |
| ktdm | `ops-auth-shell`(graphite 안내면 + 밝은 폼면, DESIGN.md) | 상태별 문구 | `aria-busy`, disabled | 단일 라우트 내 분기 |
| pinvi-admin | `/admin/login`, `FormField`(44px), zod `LoginRequestSchema` + `validateForm` → 첫 오류 필드 포커스 | `reason=forbidden` 쿼리 → "관리자 권한이 필요합니다." | `loading` | 관리자 role 아니면 로그아웃 처리 |
| pinvi-user | `(auth)/login` — 세부 미확인 | — | — | — |
| kta | 로그인 없음(사실) | — | — | — |

### 1.9 도움말(help-tip)·복사(copy-button)·JSON viewer

| 항목 | map | pinvi-admin | geo | ktc | ktdm |
|---|---|---|---|---|---|
| HelpTip | hover 800ms/focus 0ms **Tooltip** + click **Popover**, 24px 박스 + `before:-inset-2`로 40px 히트, `aria-label="도움말: {label}"` | 이식(base-ui; 이전 판은 `title`+`role=dialog` 대체였음) | Popover만, `size-5`(20px), 히트 확장 없음, `Info` 아이콘 | Popover만, `size-5` + `after:-inset-2`, `text-[12px]`(map 금지 패턴 2 해당) | 없음 |
| CopyButton | 24px 아이콘 + 40px 히트, 성공 = 아이콘 스왑 1200ms + sr-only `aria-live` "복사됨", 비보안 컨텍스트/실패는 toast | sonner 없음 → `idle/copied/error/unsupported` 인라인 상태 + `TriangleAlert` 아이콘 | `JsonBlock` 내 복사(1500ms), 실패 시 pre 내용 전체 선택 폴백 | outline `Button` + 텍스트 라벨(`복사/복사됨`), 실패 `role=alert` | `CopyableCommand`(2000ms, 실패 무시, CLI 명령 원형) |
| JSON viewer | `JsonViewer`(mono 12px, `—` 빈 값, `copyable`, `tone=destructive`, maxHeight sm/md/lg) | 이식(주석의 "Geist Mono"를 시스템 mono로 수정) | `JsonDetails`(Collapsible "원본 JSON") + `JsonBlock`(`pre.json-box` e2e 계약) | 미확인 | Toast/InlineError 안 raw `<pre>` |

### 1.10 지도 뷰(vworld-map-view) 사용 방식

| 앱 | 구현 | 마커/클러스터 | 비고 |
|---|---|---|---|
| map | `src/components/vworld-map-view.tsx`(1858줄) + `lib/vworld-style.ts`; 마커는 `@kor-travel-map/map-marker-react`(workspace 패키지) | 클러스터 소스 + 지오메트리 레이어(area/route), 가격 마커 라벨 | Hallmark "map" knob: full-bleed + flat legend strip |
| weather | `components/vworld-map-view.tsx` — 주석: "maplibre-vworld-react `vworld-map-web`를 본떠 로컬 유지(해당 모노레포가 npm을 발행하지 않음)" | `lib/weather-clusters.ts` | `lib/vworld-style.ts` 중복 존재(사실) |
| geo | `maplibre-vworld-react`를 GitHub tarball로 의존(`package.json`), `components/vworld/CoordinateMap.tsx`/`LazyCoordinateMap.tsx` | 좌표 표시 | 기존 공유 라이브러리 소비자 |
| ktc | `components/VWorldMap.tsx` raw `maplibre-gl` + 번호 마커(목록 행 번호 동기화), 한국 경계 고정 | 자체 | 라이브러리 미사용 |
| pinvi-web | `vworld-map-web`/`vworld-map-core` **로컬 tgz vendor**(`vendor/vworld-map-web-1.0.0.tgz`, `../mobile/vendor/vworld-map-core-1.0.0.tgz`), `components/map/vworldPrimitives.tsx`, `MapView`/`FeatureMapView` | 16색 마커 팔레트(`docs/design/marker-palette.md`) | 지도 관련 다이얼로그(`LocationConsentDialog`, `FeatureRequestDialog`) |
| pinvi-mobile | `vworld-map-rn` tgz + `@maplibre/maplibre-react-native` | — | — |
| ktdm / kta | 지도 없음 | — | — |

추정: `lib/vworld-style.ts`가 map과 weather에 각각 존재하고 pinvi는 tgz vendor, geo는 tarball 의존이라 "VWorld 스타일 빌더"의 배포 경로가 4가지다. 이는 common의 범위(지도 엔진 제외, 기존 라이브러리 유지)와 별개로, 배포 경로 통일이 필요한 항목이다.

### 1.11 PC/Mobile 대응

| 항목 | map | ktc | geo | ktdm | weather | pinvi-admin | pinvi-user | pinvi-mobile | kta |
|---|---|---|---|---|---|---|---|---|---|
| breakpoint 체계 | Tailwind 기본(sm 640/md 768/lg 1024/xl 1280) | 동일 + `useIsMobile` `(max-width: 767px)` | 1023 drawer, 768, 640–1023 태블릿 규칙, `hover:hover and pointer:fine` 3곳 | 64rem/48rem | 62rem(992)/42rem(672) | Tailwind 기본 | Tailwind 기본 + `useMobileWebLayout` `(max-width:1023px), (pointer:coarse) and (hover:none)` | 네이티브(해당 없음) | 860/980/560/380 |
| 설계 문서 검사 폭 | 미확인 | 320/375/414/768 | 미확인 | 320/375/414/768/1024 | 320/375/414/768 | — | DESIGN.md Airbnb 참조 744/1128/1440(참조값, 코드는 Tailwind 기본) | — | 320/375/414/768/1440 |
| 모바일 기본 자세 | PC 우선, <lg는 strip 셸 | PC 우선 + 상세는 모바일=페이지/PC=모달 분기 | PC 우선 + drawer | PC 우선 + 표 영역만 가로 스크롤 | PC 우선 | PC 우선 + `mobileCard` 표 대체(`data-testid="admin-mobile-cards"`) | **모바일 우선 셸**: 하단 탭바 4+더보기, `--app-tabbar-h: 56px`, 여행 상세는 모바일에서 chrome 제거 | 네이티브 Stack 헤더 | 모바일 카드·`<details>` 접기 |
| 터치 타깃 | 컨트롤 36/30px, micro-control ≥24px(닫힌 예외 4개), 체크박스 16+8×2=32px | 36/30px | 36/30px + `min-height: 44px` 규칙(`.field select/textarea`, `.checkbox-row`, `.filter-bar input/select`, `.vtable-search`) + `min-h-11` 2파일 | 미확인(DESIGN.md에 수치 없음) | `.nav-link min-height: var(--control-h)`=36px(design.md는 30px 행이라 적음 — 불일치, 사실) | 36/30px 명시(globals 주석: "44px 관행은 admin에 적용하지 않는다… WCAG 2.5.8(24px) 초과"), 예외 2페이지는 e2e가 44px 단언 | **44px**(`min-h-11`, `.touch-target`, `minHeight.touch`), `sm`은 coarse pointer에서 44px 승격 | 버튼·입력 `min-h-12`(48px), 체크박스·칩 `min-h-11` | `.heatmap-table th/td min-width: 44px`(1건) |
| 안전영역 | 없음 | `ReviewBulkPanel` sticky 바 `pb-[calc(0.5rem+env(safe-area-inset-bottom))]` | 없음 | 없음 | 없음 | 없음 | 탭바 `pb-[env(safe-area-inset-bottom)]`, `.app-shell-main` 하단 패딩 | `SafeAreaView edges top/bottom` | 없음 |
| 폰트 최소/본문 | 7단 스케일 12/13.5/15/17/20/24/30, 본문 15px, `text-[Npx]` 금지 | 15/13.5/12, 제목 24 | 동일 7단 + `body 15px` | 본문 14px(`0.875rem`), `text-[11px]` 존재(사실) | html 16px, body 15px, 13px(0.8125rem) 사용 | admin scope에서 7단 스케일로 변수 재정의(`[data-pv-surface='admin']`) | 본문 16px(입력 포함, iOS 확대 방지), 12px 이하 금지(배지 예외) | `text-base` 16 / `text-sm` 14 / `text-xs` 12 | `0.8rem`(12.8px)~, `font-size: 11px` 1건(사실) |
| 가로 스크롤 정책 | 표 컨테이너 안에서만(`overflow-x` 컨테이너) | `html { overflow-x: clip }` | `body { overflow-x: clip }` | 표 영역만(DESIGN.md) | nav strip만(design.md) | `html, body { overflow-x: clip }` | 동일 | — | `overflow-x: clip`(감사 후 hidden→clip) |
| 다크 모드 | `.dark` 토큰 블록 있음, 토글/ThemeProvider 없음(사실, sonner 주석) | `.dark` 정의 + "light 전용" 주석(토글 미확인) | 없음 | 없음 | `.dark` 1파일(미확인) | 없음 | 없음 | 없음 | `prefers-color-scheme: dark` 자동 |
| e2e 뷰포트 | Playwright `Desktop Chrome`만 | 미확인 | `Desktop Chrome`/`Desktop Firefox` | 미확인 | 미확인 | 기본 `Desktop Chrome`; `admin-feature-requests.e2e.ts`가 여러 폭에서 44px·overflow 검사 | `app-shell-mobile.e2e.ts`(T-314 회귀) | — | `Desktop Chrome`; design.md가 live 검사 폭 명시 |

### 1.12 접근성

파일 수 집계(§0.2 방법; 주석 포함):

| 패턴 | kta | ktc | ktdm | geo | map | weather | pinvi-web | pinvi-mobile |
|---|---|---|---|---|---|---|---|---|
| `focus-visible` | 1 | 20 | 8 | 18 | 38 | 1 | 21 | 0 |
| `prefers-reduced-motion` | 1 | 2 | 1 | 1 | 3 | 1 | 2 | 0 |
| `aria-live` | 1 | 6 | 4 | 3 | 12 | 3 | 12 | 0 |
| `role="alert"` | 1 | 16 | 7 | 19 | 3 | 10 | 69 | 0 |
| `aria-busy` | 0 | 3 | 2 | 8 | 27 | 7 | 19 | 0 |
| `inert` | 0 | 0 | 0 | 2 | 1 | 0 | 5 | 0 |
| `window.confirm` | 1 | 1(주석) | 3 | 0 | 2(+주석 1) | 1 | 0 | 0 |
| `Skeleton`/`skeleton` | 0 | 0 | 0 | 17 | 24 | 2 | 8 | 0 |

규칙 수준 비교:

| 항목 | map | pinvi | geo | ktc | ktdm | weather / kta |
|---|---|---|---|---|---|---|
| focus 레시피 | `@layer base :focus-visible { outline: 2px solid var(--focus); offset 2px }` **단일 발행**, `outline-none` 전면 금지(grep 게이트 6), 링 끄기는 `focus-visible:outline-0`만·닫힌 목록 4개, 링은 transition 밖(열거형 transition만), root `opacity` 흐림 금지(자식 래퍼에만) | `.focus-ring` 유틸(`outline-2 offset-2 outline-focus`), 즉시 표시 이유 주석; admin은 KTM 규율 이식 | 컴포넌트별 `focus-visible:outline-2 … outline-focus` | 동일 토큰(`outline-focus`, rail 위는 `outline-white`) | `focus-visible` 8파일, DESIGN.md "2px brand outline" | weather 1파일; kta `--shadow-focus` box-shadow 링 |
| reduced-motion | 전역 규칙 + **스피너는 1.6s로 유지**, Skeleton은 `motion-reduce:animate-none`(판단 기준 문서화) | 전역 ≤0.01ms; `PageLoading` 스피너 `motion-reduce:animate-none` | 전역 | 전역 + `.animate-spin` 1s 유지 | 전역(DESIGN.md) | 전역 |
| 키보드 | skip link, listbox roving tabindex, pager 포커스 유지(`aria-disabled`), `<main tabIndex=-1>` | skip link(admin), `useModalDialog` trap/복원, 더보기 시트 Escape/focusout | drawer trap/Escape/복원/`inert`, `use-modal-a11y` | 검수 단축키 + IME 가드 | ⌘K, Escape, 모달 탭 화살표 이동 | weather skip link; kta 미확인 |
| 이름 규약 | 아이콘 전용 버튼 `aria-label`+`title`, 행 체크박스 `${label} 선택`, pager `"{prefix} 첫 페이지"` 계약 | nav `aria-label="{label} (Sprint N)"`(운영 정보가 접근성 이름에 섞임, 사실) | Panel h2 접근명에 배지 제외 | — | — | — |
| 상태 알림 | `LiveBadge role=status`, Alert `role=alert` | `role=status`/`alert` 다수 | `aria-live` 3 | `role=status` 스낵바 | 오류 `role=alert`, 성공 `role=status` | `role=alert`/`status` |

### 1.13 Hallmark(design.md 장르·macrostructure) 적용

| 앱 | 설계 문서 | 장르 / macrostructure | 스탬프 파일 수(`Hallmark ·`) | 감사 산출물 | 비고 |
|---|---|---|---|---|---|
| map | `packages/kor-travel-map-admin/frontend/design.md`(302줄, 잠금 시스템) | editorial-utilitarian / Rail-Workbench, 변형 knob 6종(list·detail·map·form·dashboard·login) | 88 | `docs/reports/hallmark-audit-admin-frontend-2026-08-18.md` | 금지 패턴 7종 grep 게이트, 상태 tone 테이블, Focus/States 규율 — **가장 상세한 정본** |
| ktc | `design.md`(54줄) + `frontend/docs/DESIGN-RULES.md`(47줄) | editorial-utilitarian / Rail-Workbench(map 기준, 보라 팔레트 유지) | 2 | `.hallmark` 없음 | "색상은 유지, 구조는 map" 명시 |
| ktdm | `DESIGN.md`(139줄) | editorial-utilitarian / Rail-Workbench, 테마 Ember | 1(tokens.css) | `.hallmark/log.json`, 감사 2026-08-13 언급 | 반응형 표(320/375/414/768/1024), 상호작용 8상태 표, DTCG/shadcn 매핑 |
| geo | `design.md`(54줄) + `kor-travel-geo-ui/docs/DESIGN-RULES.md`(73줄, StyleSeed 해석) | editorial-utilitarian / Workbench(drawer) | 1 | `.hallmark/log.json`, `preflight.json` | 청색 팔레트 유지, `Panel/Card/PageHeader/DocumentNavLink`가 계약 중심 |
| weather | `frontend/design.md`(45줄, 영문) | map 셸·컴포넌트 계약 준수 선언 | 2 | 없음 | 문서와 코드 불일치 2건(§1.1, §1.11) |
| kta | `design.md`(38줄, 영문) | modern-minimal workbench(대시보드) | 0(스탬프 형식이 `Hallmark stamp: parking-radar / token layer`로 다름, 사실) | `.hallmark/log.json`, `preflight.json`, `docs/reports/hallmark-audit-2026-08-22.md` | 무인증 백업 도구, 320px 가독성 게이트 |
| pinvi | `DESIGN.md`(451줄, Airbnb 참조 + "Hallmark 잠금 시스템") + `docs/design/styleseed-rules.md` | modern-minimal / Narrative Workflow(`/`)·Workbench(app)·Long Document(법무·공유·오류) — **`(admin)`은 잠금에서 제외**(밀도 규칙이 다름) | 38 | `.hallmark/log.json`, `preflight.json` | admin은 KTM 구조 규약만 이식(T-356), 색은 pinvi 팔레트 |
| canview(참조) | `docs/ui/design.md`(LVGL, 320×480) | 임베디드 운전자 UI | — | — | 문서 라우팅 구조(AGENTS.md → docs/README → resume → tasks)만 참조 가치. UI 규약은 웹과 무관 |

사실: 7개 kor-travel 앱 모두 Hallmark 문맥의 설계 문서를 가지며, admin 6개 중 5개(map·ktc·ktdm·geo·weather)가 같은 장르(editorial-utilitarian)와 같은 macrostructure 계열(Rail-Workbench/Workbench)을 선언한다. pinvi-admin은 장르 선언 없이 map 구조 규약을 부분 이식했고, pinvi-user/kta는 modern-minimal이다.

### 1.14 선행 보고서(2026-09-05) 재검증

| 선행 보고서 주장 | 이번 조사 결과 | 판정 |
|---|---|---|
| §3.1 pinvi `data-table.tsx`는 map 이식본 | pinvi `components/admin/*` 12개 파일 머리 주석이 "kor-travel-map admin … 이식(T-356)"과 변경 사유를 명시. `AdminTable`은 그 위의 어댑터(36페이지) | 사실 확인, 범위는 더 넓음(table뿐 아니라 filter-bar·pagination-bar·status-label·empty-state·json-viewer·copy-button·section-card·detail-list·help-tip·breadcrumb·alert·stat-strip) |
| §3.3 버튼 계약 차이(geo Radix Slot / map base-ui / pinvi native) | pinvi-user `components/ui/Button.tsx`는 native `forwardRef`, 44px 기본. pinvi-admin `components/admin/ui/button.tsx`는 이번 조사에서 열지 않음 | 부분 확인(pinvi-admin 버튼 본문은 미확인) |
| §3.4 geo VirtualTable 클라이언트 정렬 vs map/pinvi 서버 정렬 | geo는 클라이언트 검색·정렬(사실). map DataTable `manualSorting=true` 기본(사실). **pinvi `AdminTable`은 `manualSorting=false` 기본**이고 `serverSort` opt-in(T-357) | 선행 보고서의 "pinvi DataTable manualSorting=true"는 원본 `data-table.tsx`에는 맞지만, 실제 36페이지가 쓰는 `AdminTable`에는 맞지 않음 — **결론 보정** |
| §7.2 AppShell은 "구조 일부만 후보" | pinvi는 실제로 skip link·헤더 밴드·rail 그리드만 뽑았고 nav·접힘·RBAC는 자체 유지(`admin-shell-parts.tsx` 주석) | 사실로 뒷받침 |
| §3.5 토큰 공유 시 제품 정체성 유지 | ktc·geo·ktdm·weather·pinvi-admin 모두 "구조는 map, 색은 자기 팔레트"를 문서로 선언 | 사실로 뒷받침 |
| §1 Pinvi 사용자 웹·모바일은 첫 이관 대상 제외 | 사용자 표면은 44/48px·16px·하단 탭바·centered EmptyState(mobile) 등 규칙이 admin과 다름. 다만 상태 UI 4종·reduced-motion·focus ring·확인 다이얼로그 원칙은 문서 수준에서 admin과 같다 | 코드 공유 제외에는 동의, **규칙 문서 공유는 가능**(후보) |
| kta·ktdm UX | 선행 보고서 범위 밖 | 이번 조사에서 추가: kta는 admin 셸·인증이 없고(사실), ktdm은 `window.confirm`·자체 모달·명령 팔레트가 있음 |

## 2. 공통 UX 가이드 초안 — 목차와 규칙별 근거

아래 목차는 `kor-travel-common/docs/ux-guide.md`(가칭)의 뼈대다. 각 규칙에 "출처 앱: 파일"을 적고, 채택 근거 수준을 표기한다. 원칙: **map admin `design.md`를 구조·상태·접근성 규칙의 1차 정본으로 채택하고**, pinvi DESIGN.md의 사용자 표면 규칙을 별도 장으로 두며, 색·브랜드 값은 앱 소유로 남긴다(선행 보고서 §3.5와 일치).

### G0. 범위와 소유

| 규칙 | 근거 | 수준 |
|---|---|---|
| G0.1 common은 구조·밀도·상태·접근성·문구 규칙을 소유하고, 브랜드 색·nav 항목·권한·라우트는 앱이 소유한다 | ktc `design.md` §색상("초록색 브랜드 팔레트로 교체하지 않는다"), geo `design.md` §색상, pinvi `apps/web/app/globals.css` admin 토큰 주석("색은 pinvi 팔레트… KTM oklch 이식 안 함"), weather `frontend/design.md`("only the content and primary accent hue") | 사실(5개 앱이 동일 원칙 선언) |
| G0.2 admin 표면과 사용자 표면은 밀도 규칙이 다르므로 장을 분리한다 | pinvi `DESIGN.md` "Hallmark 잠금 시스템"이 `(admin)` 제외, `globals.css` 주석 "밀도 규칙이 다르다" | 사실 |
| G0.3 규칙 문서는 grep 가능한 금지 패턴 목록을 포함한다 | map `design.md` §금지 패턴(7종, 백틱 인용 제외 규칙) | 후보 |

### G1. 셸(Rail-Workbench)

| 규칙 | 근거 | 수준 |
|---|---|---|
| G1.1 데스크톱(≥1024px): 좌측 rail 16rem, 접힘 4rem, 접힘 상태는 `localStorage "{app}:sidebar-collapsed"` | map `admin-shell.tsx`, ktc `AppShell.tsx`, ktdm `AppShell.tsx`+`DESIGN.md`, geo `AppShell.tsx`(키 규약), ktc `design.md` §방향 | 사실(4앱 일치; pinvi 5rem·weather 17rem·접힘 없음은 §4 충돌) |
| G1.2 <1024px: rail은 상단 가로 strip으로 전환하고 활성 항목을 `scrollIntoView`(reduced-motion 시 `auto`) | map·ktc 셸의 동일 effect; ktc `DESIGN-RULES.md` §반응형 | 사실(2앱 코드 동일, 3앱 CSS 동일 방향) — geo drawer는 대안(§4) |
| G1.3 skip link → `<main id tabIndex={-1} focus-visible:outline-0>` | map·pinvi-admin·geo·ktdm·weather 셸 전부 | 사실(5앱) |
| G1.4 활성 nav = `aria-current="page"` + 색 이외의 형태(2px 좌측 mark) | map, ktc `design.md` §상태와 접근성, geo `design.md` §장르와 구조, ktc `DESIGN-RULES.md` 9 | 사실(4앱 문서 일치; pinvi ink 채움은 §4) |
| G1.5 헤더 밴드 순서: breadcrumb/section → h1(+help) + actions(primary ≤1, secondary ≤2) → meta → description, 아래 hairline | map `admin-shell.tsx` props 주석, pinvi `admin-shell-parts.tsx`, geo `PageHeader.tsx` 주석("map header band를 geo 계약에"), ktdm `page-head` | 사실(4앱) |
| G1.6 로그아웃은 rail footer(데스크톱) / 상단 아이콘(모바일); 별도 사이트 footer 없음 | map, ktc, geo `design.md` §풋터, ktdm `DESIGN.md` §하단 | 사실 |
| G1.7 nav 정본은 셸 밖 모듈(`admin-pages.ts` 형태)로 두어 h1·nav 라벨·e2e가 같은 문자열을 소비 | geo `lib/admin-pages.ts` 주석, ktc `lib/nav.ts`(활성 판정 단위 테스트) | 후보 |
| G1.8 우측 inspector rail 22rem은 `xl` 이상에서만 2열 | map `--rail`, pinvi `AdminRailGrid` | 사실(2앱) |

### G2. 목록 화면

| 규칙 | 근거 | 수준 |
|---|---|---|
| G2.1 툴바는 `FilterBar/FilterField/FilterActions`: 가시 라벨 위, hint 아래, wrap, 가로 스크롤 금지, 정렬은 컬럼 헤더, page-size는 pager | map `filter-bar.tsx`, pinvi 이식 + `AdminPage.FilterBar` 위임 주석 | 사실(2앱) |
| G2.2 표는 4상태(loading skeleton + `aria-busy` / empty EmptyState / error Alert+`다시 시도` / data)를 내부에서 렌더 | map `data-table.tsx` 헤더 주석, pinvi `AdminTable`(`isError/onRetry`), pinvi `styleseed-rules.md` §5 | 사실 |
| G2.3 서버 페이징 목록은 서버 정렬(`manualSorting=true`); 클라이언트 정렬은 전체 데이터 보유 목록만 | map `data-table.tsx` 주석(#502), pinvi `AdminTable serverSort` 주석("화면이 거짓말을 한다") | 사실(원칙 일치, 기본값은 §4) |
| G2.4 pager 라벨·요약·aria 규약: `첫 페이지/이전/다음/마지막 페이지`, `페이지 n / m · 총 N건`, 경계 = native disabled, 전환 중 = `loading`(포커스 유지) | map `pagination-bar.tsx`(P1-5 주석), pinvi 이식 | 사실 |
| G2.5 행 선택 목록은 listbox + roving tabindex, 선택 = tint + 2px mark, disabled 사유는 흐리지 않음 | map `selectable-row.tsx` | 후보(1앱 구현, 2앱 문서) |
| G2.6 행 체크박스 접근성 이름 `"{row label} 선택"`, bulk 액션은 선택 시 표 위 바 | map `data-table.tsx` `rowSelectionLabel`; ktc `ReviewBulkPanel`(진행 요약) | 후보 |
| G2.7 모바일 표 대체(카드)는 표와 같은 데이터·testid 계약을 유지 | pinvi `AdminTable mobileCard`, kta `dashboard-screen.tsx`(`desktop-lot-table`/`mobile-lot-grid`) | 후보(2앱) |

### G3. 상세·편집

| 규칙 | 근거 | 수준 |
|---|---|---|
| G3.1 섹션 컨테이너는 1층(카드 안 카드 금지); `SectionCard`(헤더 hairline + flat body, `headingLevel`) | map `section-card.tsx`, ktc `SectionCard.tsx`(동일), pinvi 이식, geo `design.md` §간격, ktdm `DESIGN.md` §감사 기준, pinvi `styleseed-rules.md` §3 | 사실(6앱 문서/코드 일치) |
| G3.2 상세 dl은 `DetailList`(`—` null glyph, mono 식별자, tabular-nums, copyable, help) | map `detail-list.tsx`, pinvi 이식, geo `KeyValueGrid`(help 슬롯) | 사실(3앱) |
| G3.3 폼 필드 = 라벨 위 · 컨트롤 · 메시지 슬롯 1개 예약(error가 hint 대체), `aria-describedby`는 표시 중 메시지만, required 별표는 접근성 이름에서 제외 | map `form-field-input.tsx`/`form-field-shared.ts`, pinvi-user `forms/FormField.tsx`(같은 슬롯 규칙) | 사실(admin/user 모두) |
| G3.4 제출 실패 시 첫 오류 필드로 포커스 | map `lib/form-validation.ts firstErrorField`, pinvi `@pinvi/domain validateForm firstField`(admin login) | 사실(2앱) |
| G3.5 파괴적 설정 변경은 저장 전 diff 미리보기 | ktdm `DashboardClient.tsx`(포트/네트워크/env before-after) | 후보(1앱) |
| G3.6 dirty 이탈 경고 | 8표면 모두 없음 | 미확인(정책 결정 필요, §5) |

### G4. 피드백

| 규칙 | 근거 | 수준 |
|---|---|---|
| G4.1 성공은 조용히: 자기 영역이 다시 그려지면 토스트 없음, 교차 페이지 효과만 토스트; 성공 Alert 없음 | map `design.md` §Microinteractions, `ui/alert.tsx` 주석, pinvi `DESIGN.md` §Microinteractions stance, `copy-button.tsx`(아이콘 스왑 + sr-only live) | 사실(2앱 문서 일치) — ktdm은 성공 토스트 사용(§4) |
| G4.2 오류는 what/why/what-to-do 3부 + 회복 행동 1–2개; stack trace dead-end 금지 | map `app-error-panel.tsx`, `ui/alert.tsx`; pinvi `styleseed-rules.md` §5; ktdm `InlineError`(요청 ID 상시 노출) | 사실 |
| G4.3 런타임 오류는 chunk/RSC/network 계열에 한해 같은 pathname 1회 hard reload, 반복 시 패널 | geo `lib/error-recovery.ts`(원천), map·ktc·ktdm·pinvi 동일 계보 | 사실(5앱 동일 구현) |
| G4.4 빈 상태 = 좌측 정렬, 무엇이 비었나 1문장 + 다음 행동 1개; dashed·가운데·아이콘 타일 금지 | map `empty-state.tsx`, pinvi `FullPageMessage.tsx` 주석, map 감사 M17 | 사실(2앱) — ktdm/pinvi-mobile 가운데 정렬은 §4 |
| G4.5 로딩: 형태가 정해진 목록/카드는 Skeleton(`aria-hidden`, 감싸는 영역 `aria-busy`), 인라인 액션은 버튼 스피너(라벨 유지, `aria-busy`), 페이지 스피너는 목적지 불명확한 대기만 | map `skeleton.tsx`·`design.md` §States, pinvi `styleseed-rules.md` §5·`PageLoading` | 사실 |
| G4.6 파괴적·비가역 행동은 공용 확인 다이얼로그: 질문형 제목 + 결과 1줄, **동사 라벨(`확인`/`OK` 금지)**, 취소 초기 포커스, destructive fill은 다이얼로그 안에서만, `window.confirm` 금지 | map `confirm-dialog.tsx`(타입·런타임 거부), pinvi `DESIGN.md`("`window.confirm` 금지"), ktc `ConfirmActionButton`, geo `ConfirmActionDialog` | 후보(원칙 4앱, 라벨 규칙은 map만) |
| G4.7 가역 행동은 즉시 실행 + Undo 스낵바(`role=status`), 마지막 1건 | ktc `ReviewUndoSnackbar`, map·pinvi 문서 | 후보 |
| G4.8 모달 a11y: 열릴 때 포커스 이동, Tab trap, Escape 닫기, 닫힐 때 트리거로 복원(분리된 트리거면 생략), body scroll lock | geo `use-modal-a11y.ts`, pinvi `useModalDialog.ts`, ktdm `ContainerDetailModal`(Escape·초기 포커스) | 사실(엔진과 무관하게 3앱 동일 요구) |

### G5. 상태 표현

| 규칙 | 근거 | 수준 |
|---|---|---|
| G5.1 5-tone: success(활성/완료) · warning(사람 결정 대기/저하) · destructive(실제 잘못된 것만) · info(정보성 + 기계 진행 중) · neutral(보관/비활성/정상 취소) | map `lib/status-label.ts`, pinvi 동일 이식 + 잠금 테스트 | 사실(2앱) |
| G5.2 enum raw 렌더 금지, 라벨은 `statusLabel()` 단일 정본, 같은 라벨은 같은 tone(테스트 잠금) | map `design.md` §Status colour semantics, `status-label.test.ts` 언급 | 사실 |
| G5.3 배지는 dot + 텍스트(색 단독 금지) | map `status-badge.tsx`, geo `StatusBadge.tsx`·`DESIGN-RULES.md` 7, ktc `design.md`, pinvi `styleseed-rules.md` §6 | 사실(4앱) |
| G5.4 HTTP 코드 tone: 2xx neutral · 3xx info · 4xx warning · 5xx destructive | map `httpStatusTone` | 후보 |
| G5.5 상태색은 dot·배지·소수치에만, 큰 표면 채움 금지 | ktdm `DESIGN.md` §색상, geo `DESIGN-RULES.md` 1·7 | 사실(2앱 문서) |
| G5.6 값 없음은 `—`, 단위는 값이 있을 때만; 로딩 중 가짜 0 금지 | map `design.md` §Copy, `stat-strip.tsx`, canview `docs/ui/design.md`("숫자를 꾸며내지 않고 `—`") | 사실 |

### G6. 위험 작업

| 규칙 | 근거 | 수준 |
|---|---|---|
| G6.1 복원·교체류는 단계형(선택 → 미리보기 → dry-run → 확인·실행) + typed confirmation(정확 문구, 복사 금지, 일치 여부 live) | geo `RestoreWizard.tsx`, `TypedConfirmField.tsx`, `WizardSteps.tsx` | 후보(1앱 구현, 가장 정교) |
| G6.2 확인 문구에 영향 범위(대상 수·이름·DB 포함 경고)를 명시 | ktdm `ContainerDetailModal.tsx`·`DashboardClient.tsx` | 후보 |
| G6.3 장기 작업은 phase 목록 + 상태 아이콘으로 진행 표시 | pinvi `RestoreHotswapDialog.tsx`, geo `JobProgress` | 후보 |
| G6.4 필요 역할을 다이얼로그 안에 안내 | geo `RoleRequirementNote` | 후보 |
| G6.5 UI에서 막은 작업은 CLI 명령 원형을 제시 | ktdm `CopyableCommand.tsx` | 후보 |
| G6.6 개발 전용 위험 버튼의 클라이언트 게이트만으로는 부족(서버 차단 필요) | ktdm `ContainerDetailModal.tsx` IS_DEV 주석(T-044) | 사실(교훈) |

### G7. 로그인

| 규칙 | 근거 | 수준 |
|---|---|---|
| G7.1 단일 가운데 열, 타이포 워드마크, 카드·아이콘 타일 없음, 항상 렌더되는 오류 live region, 제출 중 CTA는 탭 순서 유지 | map `login-form.tsx`, ktc `LoginForm.tsx` | 후보(2앱; geo/weather 아이콘 타일은 §4) |
| G7.2 오류 문구는 상태 코드/오류 코드 → 한국어 맵(503 설정 누락 / 429 시도 제한 / 403 출처 / 기타 자격 증명) | map·geo·weather·ktdm 동일 4분기, ktc `ERROR_MESSAGES` | 사실(5앱) |
| G7.3 `next` 경로는 로컬 경로만 허용 | weather `lib/navigation.ts sanitizeLocalPath` | 후보(보안, 1앱) |

### G8. 도움말·복사·JSON·지도

| 규칙 | 근거 | 수준 |
|---|---|---|
| G8.1 HelpTip = hover 800ms/focus 0ms tooltip + click popover, 히트 ≥24px(40px 확장), 이름 `도움말: {label}` | map `help-tip.tsx`, pinvi 이식 | 사실(2앱) — geo/ktc popover-only는 허용 하위 집합(추정) |
| G8.2 CopyButton = 아이콘 스왑 + sr-only live "복사됨", 비보안 컨텍스트 폴백(선택 안내 또는 전체 선택) | map, pinvi, geo `JsonBlock` | 사실(3앱) |
| G8.3 JSON은 `JsonViewer`(mono 12px, `—`, copyable, destructive tone) 또는 접이식(`JsonDetails`) | map, pinvi, geo | 사실 |
| G8.4 지도 엔진·VWorld 스타일은 common 범위 밖(기존 `maplibre-vworld-react` 등 유지); 다만 배포 경로 4종은 별도 정리 | §1.10 | 사실 + 열린 질문 |

### G9. 접근성·모션·타이포(횡단)

| 규칙 | 근거 | 수준 |
|---|---|---|
| G9.1 focus 링 = `outline 2px` 불투명 토큰 + offset 2px, 즉시 표시(transition 밖), `outline-none` 금지, 끄는 자리는 프로그램 포커스 컨테이너뿐 | map `design.md` §Focus·§금지 패턴 6, pinvi `.focus-ring` 주석, ktc `design.md` | 사실(3앱 문서) |
| G9.2 `disabled`/`aria-disabled` 두 벌, 진행 중은 `aria-busy`+`aria-disabled`(포커스 유지), 흐림은 라벨 자식에만 | map `button-variants.ts`, `design.md` §States | 후보(map 구현, 접근성 근거 상세) |
| G9.3 reduced-motion 전역 규칙 + "사라지면 상태를 알 수 없는 애니메이션(스피너)은 유지, 자리표시(skeleton)는 끈다" | map `design.md` §Motion, ktc `globals.css`(`.animate-spin` 유지) | 사실(2앱) |
| G9.4 전환 유틸은 열거형만(`transition-all/colors/transition` 금지 — v4가 `outline-color`를 포함) | map `design.md` §Motion, ktdm `DESIGN.md`(`transition-all` 금지) | 사실(2앱) |
| G9.5 한글 라벨에 `uppercase`/tracking 금지 | map 셸 주석(m3), ktc `design.md` §타이포, ktdm `DESIGN.md` §타이포, pinvi `AdminPage.Section` 주석 | 사실(4앱) |
| G9.6 admin 타입 스케일 7단(12/13.5/15/17/20/24/30), 본문 15px, `text-[Npx]` 금지 | map `globals.css`, geo `globals.css` `@theme`, ktc `design.md`, pinvi `[data-pv-surface='admin']` | 사실(4앱) — ktdm 14px·kta/ktdm 11px은 §4 |
| G9.7 radius 2종(6px 컨트롤 / 8px 패널), 컨트롤 높이 2종(36/30px) | map, ktc `tokens.css`, weather `tokens.css`, ktdm `tokens.css`, pinvi admin `@theme`, geo `@theme` | 사실(6앱) |
| G9.8 hairline 2종: 장식 `border-border` vs 컨트롤 경계 `border-input`(3:1) | map `globals.css` 주석, pinvi admin `--color-admin-control-line` 주석(실측 대비) | 사실(2앱) |
| G9.9 `overflow-x: clip`(hidden 금지) | ktc·pinvi·geo `globals.css`, kta 감사 결정 | 사실(4앱) |

## 3. PC/Mobile Web 규약 초안

### 3.1 표면 분류와 기본 자세

| 표면 | 기본 자세 | 근거 | 수준 |
|---|---|---|---|
| Admin(map·ktc·geo·ktdm·weather·pinvi-admin) | **PC-first + 최소 모바일 보장**: 1024px 이상에서 rail-workbench, 그 아래에서는 셸을 strip(또는 drawer)으로 바꾸고 문서 전체 가로 스크롤을 만들지 않는다. 표·지도·작업면만 자체 overflow. | ktc `design.md` §상태와 접근성("320px부터 … 문서 전체 가로 스크롤 금지"), ktdm `DESIGN.md` §반응형·§감사 기준, weather `design.md` §Verification, geo `Panel.tsx` #514 주석, pinvi admin globals 주석 | 사실(5앱 문서 일치) |
| 사용자 웹(pinvi-user) | **mobile-first**: 하단 탭바 셸, 44px 타깃, 16px 입력, 안전영역 패딩, 데스크톱(lg)에서 상단 탭으로 전환. 판정은 뷰포트 + 포인터 능력(UA 스니핑 금지). | pinvi `AppShell.tsx`, `useMobileWebLayout.ts`, `globals.css` `.app-shell-main`, `DESIGN.md` Touch Targets·Motion | 사실 |
| 사용자 대시보드(kta) | 반응형 단일 페이지: 860px 이하 카드·`<details>` 접기, 320px 가독성 게이트 | kta `dashboard-app.tsx useViewportMode`, `dashboard-screen.tsx ResponsiveSection`, `design.md` §Layout contract | 사실 |
| 모바일 앱(pinvi-mobile) | 네이티브 Stack 헤더 + SafeArea, 48px 버튼/입력, NativeWind(Tailwind v3) + `@pinvi/design-tokens` preset | `apps/mobile/components/ui.tsx`, `tailwind.config.js`, `app/(app)/_layout.tsx` | 사실 |

### 3.2 breakpoint 규약(제안)

| 이름 | 값 | 용도 | 근거 |
|---|---|---|---|
| `sm` | 640px | 헤더 actions/summary 한 줄 배치(`sm:flex-row`), pinvi main 패딩 | map `pagination-bar.tsx`, pinvi admin main |
| `md` | 768px | 헤더 h1/actions 행 분리, 2열 dl, ktdm 표 block 전환, ktc 모바일 상세 분기(767) | map 셸 헤더 `md:flex-row`, `detail-list.tsx sm:grid-cols-2`, ktdm 48rem, ktc `use-is-mobile.ts` |
| `lg` | 1024px | **셸 전환(rail ↔ strip/drawer)**, 사용자 웹 탭바 ↔ 상단 탭 | map·ktc·geo·ktdm·pinvi 전부 |
| `xl` | 1280px | 우측 inspector rail 2열 | map `xl:grid-cols-[…_var(--rail)]`, pinvi `AdminRailGrid` |
| 검사 폭 | 320 / 375 / 414 / 768 / 1024 / 1440 | 설계 문서·감사 게이트 공통 집합 | ktc·ktdm·weather·kta 설계 문서 합집합 |

사실: weather의 62rem(992px)/42rem(672px)과 kta의 860/980/560/380은 위 표와 다르다(§4).

### 3.3 터치 타깃·타이포·안전영역(제안)

| 항목 | Admin | 사용자 웹 | 모바일 앱 | 근거 |
|---|---|---|---|---|
| 독립 컨트롤 높이 | 36px(`h-control`) / 30px(`h-control-sm`) | 44px(`min-h-11`); `sm`은 coarse pointer에서 44px 승격 | 48px(`min-h-12`) | map/ktc/geo/weather/ktdm/pinvi-admin 토큰; pinvi `Button.tsx`; mobile `ui.tsx` |
| 최소 히트 영역 | 24px(WCAG 2.5.8) — micro-control은 의사요소로 확장(HelpTip/Copy 40px, 체크박스 32px) | 44px | 44px(체크박스·칩) | map `design.md` §Spacing, pinvi admin globals 주석, mobile `ui.tsx` |
| 본문/최소 폰트 | 15px / 12px(`text-2xs`) | 16px(입력 포함) / 12px 배지 예외 | 16 / 12 | map·geo `@theme`, pinvi `DESIGN.md` Typography, mobile tokens |
| 안전영역 | 하단 고정 바가 있을 때만 `env(safe-area-inset-bottom)`(ktc bulk 바) | 탭바 + main 하단 패딩 | `SafeAreaView edges=['top','bottom']` | ktc `ReviewBulkPanel.tsx`, pinvi `AppShell.tsx`·`globals.css`, mobile `ui.tsx` |
| 가로 overflow | `html/body overflow-x: clip`, 표 컨테이너만 스크롤 | 동일 | — | §G9.9 |
| 다크 모드 | 기본 light 전용(토큰은 `.dark` 블록 준비 가능) | light 전용 | light 전용 | map/ktc 주석, pinvi 토큰; kta만 자동 dark(§4) |

### 3.4 모바일 셸 전략(제안, 근거 기반)

| 전략 | 채택 앱 | 장점 | 비용 | 제안 |
|---|---|---|---|---|
| 상단 가로 strip | map, ktc, ktdm, weather, pinvi-admin | 구현 단순, 전 항목 노출, 활성 자동 스크롤 | 31항목(pinvi)까지 가로 스크롤, 라벨 sr-only(pinvi) | admin 기본값(후보). 항목 ≤10이면 라벨 표시, 그 이상은 아이콘+라벨 유지 여부 결정 필요 |
| off-canvas drawer | geo | 항목 수 무관, 본문 공간 확보 | `inert`·focus trap·scroll lock·hydration 전 `visibility` 처리 필요(geo가 해결, 테스트 존재) | 항목 수가 많은 admin의 대안(후보). geo 구현을 common의 참조 구현으로 검토 |
| 하단 탭바 4+더보기 | pinvi-user | 사용자 웹 관용, 엄지 도달 | 앱 밖 목적지는 시트로 이동, 셸 밖 페이지 처리 | 사용자 웹 전용(사실) |

## 4. 충돌 규칙 목록과 해결 제안

| # | 충돌 | 관련 앱·근거 | 해결 제안 | 수준 |
|---|---|---|---|---|
| C1 | 접힌 rail 폭 4rem vs 5rem | map/ktc/ktdm 4rem; pinvi-admin `lg:w-20`(5rem, 44px 아이콘 버튼 + 패딩) | admin 규약은 4rem. pinvi는 접힘 행을 36px(`h-control`)로 낮추면 4rem 수용 가능(추정). 44px 유지가 필요하면 5rem을 "터치 admin 변형"으로 명시 | 후보 |
| C2 | rail 폭 16rem vs 17rem; 접힘 있음 vs 없음 | weather `--rail: 17rem`, 접힘 코드 없음(design.md는 16rem·접힘 서술) | weather 문서를 코드에 맞추거나 코드를 규약(16rem+접힘)에 맞춘다. common 도입 시 weather는 셸 자체를 교체하는 편이 싸다(추정) | 사실(불일치) |
| C3 | 셸 전환 breakpoint 1024 vs 992 vs 860 | weather 62rem, kta 860 | 1024(lg)로 통일. kta는 admin 셸이 없으므로 860은 콘텐츠 breakpoint로 남기되 규약 표(§3.2)의 768/1024로 재조정 검토 | 후보 |
| C4 | 좁은 화면 셸: strip vs drawer | geo drawer, 나머지 strip | 둘 다 허용하되 a11y 요구(G4.8 동일)를 규약으로 고정. common 셸은 strip 기본 + drawer 옵션(후보) | 후보 |
| C5 | 활성 nav 표현: brand tint + 2px mark vs ink 채움 vs 밑줄 | pinvi-admin `bg-ink text-canvas`; 사용자 웹 밑줄 | admin은 tint+mark(4앱 문서). pinvi-admin은 색 의미 규율(G5.3, 색 이외 형태)을 위해 mark 추가 권고. 사용자 웹은 별도 장 | 후보 |
| C6 | 컨트롤 높이 36/30 vs 44 vs 48 | admin 6앱 vs pinvi-user vs mobile; pinvi-admin 2페이지는 e2e가 44px 단언 | 표면별 분리(§3.3). pinvi-admin의 2페이지 예외는 "터치 검토 화면" 변형으로 문서화하거나 e2e를 36px로 재조정 | 사실(예외 존재) |
| C7 | 확인 다이얼로그: 동사 라벨 강제 vs 기본 `'확인'`/`"실행"`/`"삭제"` vs `window.confirm` | map 거부; pinvi-user `ConfirmDialog` 기본 `'확인'`; geo `"실행"`; ktc `"삭제"`; ktdm 3곳·kta·weather·map 2곳 `window.confirm` | 규약: 동사 라벨 필수, 기본값 없음, `window.confirm` 금지(grep 게이트). map 잔존 2건·ktdm·kta·weather는 이관 대상 목록화 | 후보 |
| C8 | 토스트: sonner vs radix+zustand vs 자체 vs 없음; 성공 토스트 정책 | map silent success; ktdm 성공 토스트 6초; geo/ktdm 자체 엔진; pinvi/ktc/weather 없음 | 정책(G4.1)은 통일, 엔진은 앱 선택. common은 "토스트가 필요한 경우"만 정의하고 구현은 강제하지 않음(선행 보고서 §7.2 overlay 후속과 정합) | 후보 |
| C9 | 상태 tone: 5-tone(취소=neutral) vs geo 3-tone(CANCELLED=warn) vs ktdm 이름(ok/warn/danger) vs kta 도메인 5단계 vs weather raw | §1.6 | 5-tone 이름과 의미를 규약으로 채택. geo `severityClass`는 CANCELLED→neutral로 매핑 변경 검토(도메인 의미 확인 필요, §5). ktdm은 이름만 alias(ok=success, warn=warning, danger=destructive). kta는 도메인 레벨 → tone 매핑 표 추가. weather는 `statusLabel` 도입 | 후보 |
| C10 | 정렬 기본값: DataTable `manualSorting=true` vs AdminTable `false` vs VirtualTable 클라이언트 | §1.3 | 규약은 "페이징 목록 = 서버 정렬"(G2.3). pinvi `AdminTable` 기본값은 36페이지 호환 때문이므로 common DataTable 채택 시 페이지별 `serverSort` 전환 목록 필요 | 사실 |
| C11 | 빈 상태 정렬: 좌측 vs 가운데 | ktdm 모달 `EmptyState` 가운데, pinvi-mobile 가운데 | admin/사용자 웹은 좌측(G4.4). 모바일 앱은 플랫폼 관용에 따라 가운데 허용(추정) | 후보 |
| C12 | 폰트 스택: Pretendard+Geist Mono / Noto 우선+IBM Plex Mono / Geist 우선 / Pretendard+시스템 mono / JetBrains Mono | map, ktdm(`Noto Sans KR` 1순위), weather(`Geist` 1순위), pinvi, kta | 규약: 한글 본문 1순위 Pretendard Variable(로드 보장), mono는 앱 선택. weather의 Geist 1순위는 map 감사 C-등급 지적("한글 전용 서체 없음")과 같은 위험(추정) | 후보 |
| C13 | 본문 14px/11px 존재 vs 12px 하한 | ktdm 14px 본문·`text-[11px]`, kta `11px` | admin 규약 15px/12px(G9.6). ktdm·kta는 이관 시 스케일 정렬 | 후보 |
| C14 | 다크 모드 자동 vs 준비만 vs 없음 | kta `prefers-color-scheme`, map/ktc `.dark` 클래스 | light 전용을 admin 기본으로 명시(4앱 사실). 토큰 계약에는 `.dark` 슬롯을 남겨 kta 같은 자동 dark를 허용 | 후보 |
| C15 | 로그인: 아이콘 타일 카드 vs 타이포 워드마크 vs graphite 분할 | geo/weather vs map/ktc vs ktdm | G7.1 채택(map 감사가 아이콘 타일을 템플릿 지문으로 지적). geo/weather는 후속 정렬 | 후보 |
| C16 | 헤더 2종 공존 / pathname 노출 | pinvi `AdminPage` vs `AdminPageHeader`; weather `page-path` | pinvi는 `AdminPage`를 `AdminPageHeader`로 수렴(이미 `FilterBar`/`Section`은 위임 완료). weather pathname 표시는 breadcrumb로 대체 | 후보 |
| C17 | HelpTip: tooltip+popover vs popover-only | map/pinvi vs geo/ktc | popover-only를 허용 하위 집합으로 두고 히트 영역(≥24px, 확장)만 필수 | 후보 |
| C18 | 모달 엔진: base-ui vs radix vs 자체 훅 | map/ktc/pinvi-admin vs geo vs pinvi-user/ktdm | 엔진은 앱 소유(선행 보고서 §3.3·§7.2). common은 G4.8의 행동 계약과 "한 화면에 두 모달 스택 금지"(pinvi 주석)만 규약화 | 후보 |
| C19 | 오류 페이지 부재 | weather·kta `error.tsx` 없음 | `AppErrorPanel` 계보(5앱 동일)를 common 후보로, weather·kta 도입 | 후보 |
| C20 | nav 접근성 이름에 운영 정보 포함 | pinvi `(Sprint N)` | 접근성 이름은 라벨만, 부가 정보는 `data-*` | 후보 |
| C21 | Hallmark 스탬프 형식 | `Hallmark · genre: …`(map/ktc/geo/weather/pinvi) vs `Hallmark stamp: …`(kta) vs 없음(ktdm 대부분) | common 규약이 스탬프 형식과 위치(파일 1행)를 정하고, 이식 파일은 출처 앱 스탬프를 유지할지 결정(pinvi는 제거+일부 잔존) | 후보 |
| C22 | 지도 스타일 빌더 배포 경로 4종 | §1.10 | common 범위 밖이나 `maplibre-vworld-react` 배포 정책과 함께 결정 | 열린 질문 |

## 5. 열린 질문

1. geo `severityClass`의 `CANCELLED → warn`은 정합성 리포트 도메인의 의미(취소된 검증은 재검토 필요)일 수 있다. map의 "정상 취소 = neutral"과 같은 축인지 도메인 확인이 필요하다(미확인).
2. dirty 이탈 경고(`beforeunload`)를 규약에 넣을지: 8표면 모두 없다. 넣는다면 어느 폼(설정·큐레이션 편집)이 대상인지 앱별 목록이 필요하다.
3. pinvi-admin의 44px 예외 2페이지(`feature-requests`, `feature-reference-reconciliations`)를 "터치 검토 화면" 변형으로 규약화할지, 36px로 되돌릴지.
4. weather 문서-코드 불일치(rail 17rem·접힘 없음·평면 nav·36px nav 행)를 문서 수정으로 닫을지, common 셸 이관으로 닫을지.
5. kta는 admin 셸·인증이 없다. 사용자 전제 (3) "kor-travel-airport Admin"이 가리키는 표면이 현재의 무인증 백업 패널(design.md "no-auth internal backup/restore tool")인지, 신설할 admin인지 확인이 필요하다.
6. 토스트 엔진을 common이 제공할지(sonner 채택 시 pinvi·ktc·weather는 신규 의존성), 정책만 제공할지.
7. `Hallmark ·` 스탬프를 common 배포 파일에 어떤 형식으로 남길지, 소비 앱이 이식 시 제거하는 관행(pinvi)을 유지할지.
8. pinvi `DESIGN.md`의 Airbnb 참조 breakpoint(744/1128/1440)는 코드에 반영되지 않았다(사실: Tailwind 기본 사용). 사용자 웹 규약을 Tailwind 기본으로 확정할지.
9. map 감사 보고서와 design.md의 M/C 번호(M11·M13·M17·M26·M33 등)가 컴포넌트 주석에 인용된다. common 문서가 이 번호 체계를 승계할지, 새 규칙 ID를 발급할지.
10. `lib/vworld-style.ts` 중복(map·weather)과 pinvi tgz vendor의 정본 위치.

## 6. 근거 파일 목록(저장소 상대 경로)

kor-travel-map @ `c494e227` (`packages/kor-travel-map-admin/frontend/` 기준)
1. `design.md`
2. `src/app/globals.css`
3. `src/app/layout.tsx`
4. `src/components/admin-shell.tsx`
5. `src/components/filter-bar.tsx`
6. `src/components/pagination-bar.tsx`
7. `src/components/selectable-row.tsx`
8. `src/components/ui/data-table.tsx`
9. `src/components/section-card.tsx`
10. `src/components/detail-list.tsx`
11. `src/components/empty-state.tsx`
12. `src/components/confirm-dialog.tsx`
13. `src/components/app-error-panel.tsx`
14. `src/lib/error-recovery.ts`
15. `src/components/status-badge.tsx`, `src/components/status-badge-variants.ts`
16. `src/lib/status-label.ts`
17. `src/components/help-tip.tsx`
18. `src/components/copy-button.tsx`
19. `src/components/json-viewer.tsx`
20. `src/components/ui/sonner.tsx`
21. `src/components/ui/skeleton.tsx`
22. `src/components/ui/alert.tsx`
23. `src/components/ui/dialog.tsx`
24. `src/components/ui/button-variants.ts`
25. `src/components/ui/form-field-input.tsx`, `src/components/ui/form-field-shared.ts`
26. `src/lib/form-validation.ts`
27. `src/components/stat-strip.tsx`
28. `src/components/login-form.tsx`
29. `src/components/vworld-map-view.tsx`
30. `src/app/admin/features/admin-features-client.tsx`
31. `src/app/admin/features/curated/curation-collections-client.tsx`(`window.confirm` 잔존)
32. `src/app/admin/backups/backups-client.tsx`
33. `playwright.config.ts`
34. `../../../docs/reports/hallmark-audit-admin-frontend-2026-08-18.md`

pinvi @ `9af25e5`
35. `DESIGN.md`
36. `docs/design/styleseed-rules.md`
37. `docs/architecture/frontend.md`(목차·§2.1·§3.5·§3.8만)
38. `packages/design-tokens/tailwind-preset.cjs`, `src/spacing.ts`, `src/typography.ts`, `src/motion.ts`
39. `apps/web/app/globals.css`
40. `apps/web/app/(admin)/layout.tsx`
41. `apps/web/app/(admin)/admin/layout.tsx`
42. `apps/web/app/(admin)/admin/login/page.tsx`
43. `apps/web/app/(admin)/admin/backup/page.tsx`
44. `apps/web/app/(admin)/admin/users/page.tsx`
45. `apps/web/app/(admin)/admin/category-mapping/page.tsx`(`isDirty`)
46. `apps/web/components/admin/admin-shell-parts.tsx`
47. `apps/web/components/admin/AdminPage.tsx`
48. `apps/web/components/admin/AdminTable.tsx`, `DataTable.tsx`
49. `apps/web/components/admin/filter-bar.tsx`, `pagination-bar.tsx`, `empty-state.tsx`, `status-badge.tsx`, `json-viewer.tsx`, `copy-button.tsx`, `section-card.tsx`, `detail-list.tsx`, `stat-strip.tsx`
50. `apps/web/components/admin/ui/help-tip.tsx`, `breadcrumb.tsx`, `alert.tsx`
51. `apps/web/components/admin/RestoreHotswapDialog.tsx`
52. `apps/web/lib/admin/status-label.ts`
53. `apps/web/components/app/AppShell.tsx`, `SettingsSurface.tsx`
54. `apps/web/lib/useMobileWebLayout.ts`, `lib/useModalDialog.ts`
55. `apps/web/components/ui/Button.tsx`, `ConfirmDialog.tsx`
56. `apps/web/components/forms/FormField.tsx`
57. `apps/web/components/feedback/RouteError.tsx`, `FullPageMessage.tsx`, `PageLoading.tsx`
58. `apps/web/e2e/app-shell-mobile.e2e.ts`, `e2e/admin-feature-requests.e2e.ts`, `e2e/admin-feature-reference-reconciliations.e2e.ts`
59. `apps/mobile/components/ui.tsx`, `lib/confirm.ts`, `global.css`, `tailwind.config.js`, `app/_layout.tsx`, `app/(app)/_layout.tsx`, `app/(app)/trips/index.tsx`, `package.json`

kor-travel-geo @ `1d9d74d` (`kor-travel-geo-ui/` 기준)
60. `../design.md`
61. `docs/DESIGN-RULES.md`
62. `app/globals.css`
63. `components/layout/AppShell.tsx`
64. `components/ui/PageHeader.tsx`, `Panel.tsx`, `StatusBadge.tsx`, `VirtualTable.tsx`, `JsonBlock.tsx`, `toaster.tsx`, `dialog.tsx`, `field.tsx`
65. `components/admin/shared/EmptyState.tsx`, `ConfirmActionDialog.tsx`, `TypedConfirmField.tsx`, `HelpTip.tsx`, `JsonDetails.tsx`, `KeyValueGrid.tsx`, `WizardSteps.tsx`
66. `components/admin/backups/RestoreWizard.tsx`
67. `components/admin/FilesPanel.tsx`
68. `components/auth/LoginForm.tsx`
69. `lib/admin-pages.ts`, `lib/toast.ts`, `lib/use-modal-a11y.ts`, `lib/consistency.ts`
70. `tests/unit/app-shell-drawer.test.tsx`(존재 확인만)
71. `package.json`, `playwright.config.ts`

kor-travel-concierge @ `7945305` (`frontend/` 기준)
72. `../design.md`
73. `docs/DESIGN-RULES.md`
74. `tokens.css`
75. `src/app/globals.css`, `src/app/error.tsx`
76. `src/components/AppShell.tsx`, `src/lib/nav.ts`, `src/lib/use-is-mobile.ts`
77. `src/components/SectionCard.tsx`, `detail.tsx`, `panels.tsx`, `HelpTip.tsx`, `CopyButton.tsx`, `ConfirmActionButton.tsx`, `ReviewUndoSnackbar.tsx`, `ReviewBulkPanel.tsx`, `LoginForm.tsx`, `VWorldMap.tsx`
78. `src/components/layout/AppErrorPanel.tsx`
79. `src/components/review/CandidateTable.tsx`, `useReviewKeyboard.ts`
80. `src/components/ui/badge.tsx`, `field.tsx`
81. `src/app/review/[id]/page.tsx`
82. `package.json`

kor-travel-docker-manager @ `862562d` (`frontend/` 기준)
83. `../DESIGN.md`
84. `tokens.css`
85. `src/app/globals.css`
86. `src/components/layout/AppShell.tsx`, `AppErrorPanel.tsx`
87. `src/components/Toast.tsx`, `InlineError.tsx`, `CopyableCommand.tsx`, `LoginScreen.tsx`, `ContainerDetailModal.tsx`, `DashboardClient.tsx`(grep 범위), `BackupHistoryPanel.tsx`(grep 범위), `StatStrip.tsx`
88. `src/lib/containerPresentation.ts`
89. `package.json`

kor-travel-weather @ `6003da9` (`packages/kor-travel-weather-admin/frontend/` 기준)
90. `design.md`
91. `app/tokens.css`, `app/globals.css`
92. `components/admin-shell.tsx`, `lib/navigation.ts`
93. `components/auth/LoginForm.tsx`, `components/location-admin.tsx`, `components/vworld-map-view.tsx`, `components/weather-map.tsx`(grep 범위)
94. `app/datasets/page.tsx`, `app/page.tsx`(grep 범위), `app/settings/providers/page.tsx`(grep 범위)
95. `package.json`

kor-travel-airport @ `2bb1111` (`frontend/` 기준)
96. `../design.md`
97. `../docs/reports/hallmark-audit-2026-08-22.md`
98. `src/app/tokens.css`, `src/app/globals.css`, `src/app/layout.tsx`
99. `src/components/dashboard-app.tsx`, `dashboard-screen.tsx`, `backup-panel.tsx`
100. `package.json`, `playwright.config.ts`

참조
101. `F:/dev/canview/AGENTS.md`, `docs/ui/design.md`(구조 참조)
102. `F:/dev/kor-travel-geo-fixes/docs/kor-travel-common-library-review.md`(선행 보고서)
