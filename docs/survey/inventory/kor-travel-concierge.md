# kor-travel-concierge 인벤토리

- 기준 커밋: `7945305dd8bcb3eccae54e08b1205d565daa3661` (2026-09-04 22:37 +0900, "fix: mcp 패키지를 mcp<2로 직접 고정 (n150 crash-loop 긴급 수정) (#227)")
- 조사일: 2026-09-06
- 조사 경로: `F:/dev/kor-travel-concierge` (정본 체크아웃, `git status --porcelain` 빈 출력 = 작업 트리 깨끗함)
- 라이선스: **MIT** — `LICENSE` 첫 줄 `MIT License`, 둘째 줄 `Copyright (c) 2026 kor-travel-concierge contributors`. `README.md` 말미 "MIT License" 절과 일치. 선행 보고서(`kor-travel-common-library-review.md` §9)의 "concierge는 MIT" 서술을 재검증한 결과 사실.
- 커밋 이력: 307 커밋, 저자 `Youn-sok Choi` 219 / `OpenAI Codex` 67 / `digitie` 21 (`git shortlog -sn`). 최근 커밋 제목은 `feat|fix|docs|test|deps: … (#NNN)` 형태의 PR 스쿼시.
- 표기 규칙: 본문에서 **사실**은 근거 경로를 붙여 단정형으로, **후보/추정**은 명시 표기, 확인하지 못한 것은 **미확인**으로 적는다.

## 1. 저장소 개요와 역할

`README.md`와 `AGENTS.md` 근거로 정리한 정체성은 다음과 같다.

1. `kor-travel-concierge`는 사용자가 지정한 유튜버·재생목록·검색 키워드로 YouTube 여행 콘텐츠를 탐색하고, Gemini/DeepSeek LLM으로 영상 속 여행지(POI)를 추출·요약해 PostgreSQL + PostGIS에 적재하는 **운영 콘솔형 서비스**다 (`README.md` 상단, `AGENTS.md` "목표"). 브랜딩은 2026-09-01부터 `Travel Concierge Admin UI`로 통일됐다 (`CHANGELOG.md`, `frontend/src/app/layout.tsx` metadata).
2. 1~2인 개발·운영, 동시 사용자 10명 내외를 전제로 하며 분산 크롤러 대신 공식 YouTube Data API v3, 단일 실행자 APScheduler, 전면 비동기 처리를 택했다 (`README.md` "핵심 특징", `docs/decisions.md` ADR-11/ADR-13).
3. 시스템은 네 부분이다: Next.js App Router 프론트(관리 UI), FastAPI + SQLAlchemy 2.0 백엔드, MCP 서버(FastMCP 읽기/쓰기 도구), ETL/스케줄러 (`AGENTS.md` "역할", `docker-compose.yml` 서비스 4종 `api/mcp/scheduler/frontend`).
4. 사용자 표면은 **관리자 단일 계정 로그인 뒤의 운영 콘솔**뿐이며 최종 사용자용 공개 화면은 없다 (`frontend/src/proxy.ts`가 `/login`·`/api/auth/*`·정적 자산 외 모든 경로에 세션을 요구).
5. 외부 공급은 REST `/api/v1/features/snapshot|changes`(범용 feature), `/api/v1/themes*`(테마 중심 POI), `/api/v1/destinations*`(장소 목록/export)이며 DB 발급 `read` 키로만 접근한다 (`docs/feature-export-api.md`, `docs/themes-api.md`, `backend/ktc/core/security.py` `READ_SCOPE_EXACT_PATHS`).
6. 형제 프로젝트 연동: `kor-travel-map`이 features API를 Dagster provider `kor-travel-concierge-youtube`로 pull하고, PinVi는 map이 만든 `feature_id`/`feature_snapshot`을 자체 POI row로 저장한다(직접 연결 없음) (`docs/feature-export-api.md` "기본 원칙"). `kor-travel-geo` v2 API로 확정 장소의 행정코드를 보강한다 (`backend/ktc/etl/admin_region_service.py`). 포트 정책과 prod 배포 오케스트레이션은 `kor-travel-docker-manager`가 단일 출처다 (ADR-27/ADR-28).
7. 디자인 방향은 2026-08 리디자인 이후 "최신 `kor-travel-map` admin의 Rail-Workbench 구조를 가져오되 Concierge 고유의 보라 팔레트(`--brand #7c3aed`)는 유지"로 명문화됐다 (`design.md`, `frontend/docs/DESIGN-RULES.md`, 커밋 `e7ee99e`/`22ee95a`).
8. 실행·개발 환경은 Linux Docker/WSL2 전용이고 에이전트 명령(`git`, `gh`, codegraph 포함)도 Linux bash에서만 실행한다. Windows PowerShell은 n150 Playwright 불가 시 E2E fallback에만 허용한다 (`AGENTS.md` "개발 환경 정책", ADR-23/ADR-33).
9. 외부 provider 약관(YouTube/Google Places/Naver/Kakao/VWorld) 충돌을 `docs/provider-policy.md`에 매트릭스로 관리하며 일부 기능(T-169/T-173, 제한 provider 결과 영구 저장 확대)은 릴리스 게이트 뒤에 있다.

## 2. 저장소 구조

최상위 트리(추적 파일 446개, `git ls-files`):

```
kor-travel-concierge/
├── AGENTS.md CLAUDE.md SKILL.md README.md design.md CHANGELOG.md LICENSE
├── .env.example (308줄)  .gitignore .gitattributes .dockerignore
├── alembic.ini            # script_location = backend/alembic
├── docker-compose.yml     # api / mcp / scheduler / frontend (+ profile embedded-rustfs)
├── Dockerfile.python      # python:3.11-slim + ffmpeg, api/mcp/scheduler/etl 공용 이미지
├── ktcctl                 # bash → python -m ktc.cli
├── backend/               # 182 파일: ktc 패키지 + alembic + tests + requirements.txt + main.py + pytest.ini
├── frontend/              # 129 파일: Next.js 16 App Router (src/, tokens.css, docs/DESIGN-RULES.md, Dockerfile)
├── etl/ mcp/ scheduler/   # 얇은 실행 래퍼 + 각자 requirements.txt (-r ../backend/requirements.txt)
├── tests/                 # Playwright 하니스(별도 npm 패키지) + seed/start 스크립트
├── scripts/               # start-live.sh stop-fixed-ports.sh verify-docker-compose.sh verify_rustfs.py init_rustfs_buckets.py backfill-place-admin-codes.py ktcctl
├── deploy/Caddyfile       # prod 리버스 프록시(5개 도메인, env로 주입)
├── docs/                  # 18개 md (architecture, decisions, tasks, journal, dev-environment, API 계약 4종 등)
├── .claude/ .agents/ .opencode/ .codex/   # 에이전트 페르소나·스킬(postgres 계열) 4중 미러
└── claude.json codex.json opencode.json antigravity.json   # MCP 서버 설정(playwright, sequential-thinking, codegraph, filesystem)
```

주요 패키지/앱 디렉터리:

| 디렉터리 | 종류 | 추적 파일 수 | 비고 |
|---|---|---:|---|
| `frontend/` | Next.js 앱 (npm, `package-lock.json` v3) | 129 | 단일 앱, workspaces 없음 |
| `backend/ktc/` | Python 패키지 `ktc` (api 2, core 6, etl 32, mcp_server 3, models 26, services 12, `cli.py`, `telemetry.py`) | 85 | `pyproject.toml` 없음, `requirements.txt`만 |
| `backend/alembic/` | Alembic env + versions 29개 | 30 | `alembic.ini`는 루트 |
| `backend/tests/` | pytest 62개 `test_*.py` + `conftest.py` | 64 | 실제 PostGIS DSN 필요 |
| `etl/`, `mcp/`, `scheduler/` | 실행 래퍼(레거시 ETL 샘플 `etl/*.py`, `mcp/server.py`, `scheduler/worker.py` 1,735줄) | 6/2/3 | 각자 `requirements.txt` |
| `tests/` | Playwright 패키지(`@playwright/test`) | 8 | e2e 2 spec(45+5 test) |
| `docs/` | 문서 | 18 | 절 5 참고 |

모노레포/workspace 구성은 아니다(`frontend/package.json`, `tests/package.json` 두 개의 독립 npm 루트, Python은 requirements 파일 4개).

## 3. 프론트엔드

### 3.1 Travel Concierge Admin UI (`frontend/`)

- **프레임워크/런타임** (`frontend/package.json`, `frontend/package-lock.json`)
  - `next ^16.2.7` (설치 16.2.7), `react ^19.2.8` / `react-dom ^19.2.8` (19.2.8), `typescript ^5.4.5` (설치 **5.9.3**), `engines.node >=22`, `packageManager` 필드 **없음**, 패키지 매니저 npm(`package-lock.json` lockfileVersion 3), `overrides.postcss = $postcss`.
  - scripts: `dev`(next dev, 3000), `dev:live`(`--hostname 127.0.0.1 --port 12605`), `build`(`next build --webpack`), `start`, `lint`(`eslint .`), `type-check`(`next typegen && tsc --noEmit`), `test`(`vitest run`).
- **스타일**
  - `tailwindcss ^4.3.1` / `@tailwindcss/postcss ^4.3.1` (설치 4.3.1). `frontend/postcss.config.mjs`는 `@tailwindcss/postcss`만 등록(주석: autoprefixer 불필요). `autoprefixer ^10.4.19`, `postcss ^8.4.38`은 devDependencies에 남아 있으나 PostCSS 설정에서 쓰지 않는다(잔존).
  - `frontend/src/app/globals.css` 첫 5줄: `@import "tailwindcss"; @import "tw-animate-css"; @import "maplibre-gl/dist/maplibre-gl.css"; @import "../../tokens.css"; @config "../../tailwind.config.ts";` → **v4 CSS-first 엔진이지만 `@theme` 블록 없이 v3식 JS config를 `@config`로 유지하는 혼합형**. `frontend/tailwind.config.ts`(148줄)는 `content`, `theme.extend`(colors → `var(--…)` 매핑, borderRadius `control/panel`, spacing `control/control-sm`, fontFamily, fontSize 7단계, boxShadow, transition 토큰)를 정의한다. ADR-29(2026-06-20)에서 v3.4 → v4 전환.
  - custom variant: `@custom-variant dark (&:is(.dark *))`, `data-checked`, `data-active`, `data-interactive`, `data-horizontal`, `data-vertical` (`globals.css` 9~14줄).
  - **토큰 정본**: `frontend/tokens.css`(87줄, `--ktc-*` 접두). 내용: 폰트 스택 1, surface 5(`page/card/subtle/muted/row`), brand 5(`brand/ink/hover/foreground/tint`), shell-rail 4, text 5(`strong/primary/secondary/tertiary/disabled`), `icon-default`, `line`, `control-line`, `focus`, `overlay`, 상태색 4×(색+tint) (`info/warning/success/destructive`), radius 4(`radius 0.5rem`, `radius-control 0.375rem`, `radius-panel 0.5rem`, `radius-sm`), control-height 2(`2.25rem`/`1.875rem`), shadow 5(`card/card-hover/button/modal/elevated`), duration 2(`120ms/180ms`), ease 1. z-index 토큰은 **없음**. `.dark` 블록에 값이 정의돼 있으나 토글이 없어 실제로는 light 전용(주석 "현재 토글 없음 → 항상 light").
  - `globals.css`는 3단 매핑: `--ktc-*` → 의미 토큰(`--surface-*`, `--brand`, `--text-*`, `--warn/--danger/--ok` 별칭) → shadcn 토큰(`--background/--primary/--border/--ring/--sidebar-*`, `--chart-1..5`). 앞쪽 `@layer base :root` 블록은 구 geo 계열 fallback 값(예: `--surface-page #f7f8f6`)이고 뒤 블록이 `tokens.css` 값으로 덮어쓴다(주석에 명시). `--sidebar`는 `--shell-rail`(짙은 보라 `#2e1065`)로 매핑.
  - 라이트/다크: light 전용 운영 콘솔. `dark:` 유틸리티 사용 1건.
  - 폰트: `pretendard 1.3.9`(npm), `frontend/src/app/layout.tsx`에서 `pretendard/dist/web/variable/pretendardvariable-dynamic-subset.css` import; `--ktc-font-sans: "Pretendard Variable", Pretendard, "Noto Sans KR", …`. mono는 `"Geist Mono", ui-monospace, …` 폴백만(패키지 없음). body `letter-spacing: -0.012em`, `font-feature-settings "kern","tnum"`.
  - 아이콘 `lucide-react ^1.17.0`(1.17.0). 애니메이션 `tw-animate-css ^1.4.0`(1.4.0).
  - 전역 규칙: `:focus-visible { outline: 2px solid var(--focus); outline-offset: 2px }`, `::selection` brand tint, 커스텀 스크롤바 10px, `prefers-reduced-motion`에서 animation/transition 0.01ms로 축소하되 `.animate-spin`은 유지, `html { overflow-x: clip }`, `.ktc-viewport-locked`(≥1024px에서 100vh 잠금), `.ktc-workspace`(max-width 96rem), `.ktc-eyebrow`, `.ktc-scroll-cue`.
- **UI 프리미티브**
  - `@base-ui/react ^1.5.0`(설치 1.5.0). lockfile에 `@radix-ui/*` 패키지 **0개**. `shadcn ^4.10.0`(4.10.0)이 **dependencies**(devDependencies 아님)에 있다.
  - `frontend/components.json`: `style: "base-nova"`, `rsc: true`, `tsx: true`, `tailwind.config: tailwind.config.ts`, `tailwind.css: src/app/globals.css`, `baseColor: neutral`, `cssVariables: true`, `prefix: ""`, `iconLibrary: lucide`, `rtl: false`, aliases `components=@/components, utils=@/lib/utils, ui=@/components/ui, lib=@/lib, hooks=@/hooks`, `menuColor: default`, `menuAccent: subtle`, `registries: {}`.
- **컴포넌트 인벤토리**
  - `frontend/src/components/ui/` 18개: `alert-dialog.tsx`(Base UI AlertDialog), `badge.tsx`(Base UI `useRender`+`mergeProps`, cva), `button.tsx`(Base UI Button, cva 변형 7종 `default/outline/secondary/ghost/destructive/destructive-solid/link`, 크기 8종, `loading`·`disabledReason` prop, 진행 중 `aria-disabled`+`aria-busy`+spinner 겹침·`blockBusyActivation`), `card.tsx`(flat card, `data-interactive`), `checkbox.tsx`, `dialog.tsx`, `field-variants.ts`, `field.tsx`(241줄), `input.tsx`(Base UI Input, `size sm|default` → `h-control/h-control-sm`), `label.tsx`, `popover.tsx`, `select.tsx`(331줄), `separator.tsx`, `switch.tsx`, `table.tsx`, `tabs-variants.ts`, `tabs.tsx`, `textarea.tsx`.
  - 파일 헤더 출처 표기: Hallmark 헤더(`/* Hallmark · genre: editorial-utilitarian · macrostructure: Rail-Workbench · design-system: design.md · designed-as-app */`)는 `globals.css`, `components/AppShell.tsx`, `components/ui/field-variants.ts` 3개에만 있다. `button.tsx`·`card.tsx`·`input.tsx`·`tabs-variants.ts`·`panels.tsx`는 "최신 기준 레포(=kor-travel-map admin)의 recipe, 색상만 보라 팔레트" 주석을 단다. `switch.tsx` 주석이 Checkbox/Switch 사용 규약의 정본(ADR-34).
  - 앱 레벨 공유 컴포넌트(`frontend/src/components/`): `AppShell.tsx`(360줄, 그룹형 Rail `개요/수집 파이프라인/검수/시스템`, 접힘 상태 localStorage 키 `kor-travel-concierge:sidebar-collapsed`, `main-content` id), `panels.tsx`(`Section/Panel/PanelHeader/MetricCard/Metric/CountList/EmptyState`), `detail.tsx`(`DetailSection/DetailRow`), `SectionCard.tsx`, `StatStrip.tsx`(KPI), `CopyButton.tsx`, `HelpTip.tsx`(클릭형 popover 도움말), `ConfirmActionButton.tsx`(AlertDialog 기반 파괴적 액션 확인, `window.confirm` 대체), `LoginForm.tsx`, `QueryProvider.tsx`, `JobStatusLink.tsx`, `JobLogDialog.tsx`, `JobDetailDialog.tsx`, `ReviewUndoSnackbar.tsx`, `RunActionButtons.tsx`, `HomeActionBanner.tsx`, `VWorldMap.tsx`(316줄, maplibre-gl raster source + VWorld WMTS URL `https://api.vworld.kr/req/wmts/1.0.0/{key}/Base/{z}/{y}/{x}.png`, 한국 bounds 고정), `layout/AppErrorPanel.tsx`.
  - 화면 워크스페이스: `CollectWorkspace`, `HarvestConsole`, `JobsDashboard`, `JobDetailView`, `DestinationWorkspace`(876줄), `PlaceDetailView`, `CandidateDetailView`, `ReviewBulkPanel`(741줄), `SettingsPanel`, `StatusDashboard`, `ApiTestPanel`, `RecurringEditDialog`, `review/ReviewWorkspace.tsx`(**4,386줄**), `review/CandidateTable`, `review/ConfirmForm`, `review/SearchResultsPanel`, review 훅 5종(`useCandidateSearch/useReviewKeyboard/useReviewQueue/reviewGroupFacets/searchHitNumber`).
  - 없는 것: `data-table`, `filter-bar`, `pagination-bar`, `status-badge`(badge로 대체), `json-viewer`, `tooltip`, `sonner/toast`, `skeleton`, `breadcrumb`, `alert` — `kor-travel-map` admin `components/ui/`(31개: `alert, breadcrumb, data-table, form-field*, native-select, skeleton, sonner, tooltip, button-variants.ts, badge-variants.ts` 포함)와 비교하면 concierge는 부분집합이며 `switch.tsx`·`label.tsx`는 concierge에만 있다(`F:/dev/kor-travel-common-survey/ktm-main/packages/kor-travel-map-admin/frontend/src/components/ui/` 목록 대조).
  - map admin과의 구체 차이: map은 `button-variants.ts`를 분리하고 Hallmark 헤더를 `button.tsx`에 두지만 concierge는 변형을 `button.tsx` 안에 두고 헤더가 없다. 동작 계약(`loading` 시 `aria-disabled`+포커스 유지+`blockBusyActivation`)은 동일 패턴이다. map은 `@tanstack/react-table`·`sonner`를 쓰고 `zod`/`react-hook-form`/`shadcn` CLI가 없으며 `next 16.2.12` 고정·`eslint ^10.8.0`인 반면 concierge는 `next ^16.2.7`·`eslint ^9.39.4`·`zod 4`·RHF 7·`shadcn` CLI를 쓴다(map `package.json` 대조). 토큰 파일 위치도 다르다(concierge `frontend/tokens.css` 루트, map은 `src/app/globals.css` 내부 — map 저장소에 `tokens.css` 없음).
- **상태/데이터**
  - `@tanstack/react-query ^5.40.0`(설치 5.101.0), `react-hook-form ^7.51.5`(7.77.0), `@hookform/resolvers ^3.4.2`(3.10.0), `zod ^4.4.3`(4.4.3). **zustand 없음**(`docs/architecture.md` §7 "Zustand는 현 단계에서 도입하지 않는다"). `@tanstack/react-table` 없음.
  - API 클라이언트 생성 도구(openapi-typescript 등) **없음**. `frontend/src/lib/api.ts`(1,668줄, export 158개)에 타입과 호출 함수를 수기로 유지. 공통 `requestJson<T>()`가 `${API_BASE_URL}${path}`(기본 빈 문자열 = same-origin BFF)로 fetch, 실패 시 `ApiRequestError(status, body, message)`를 던지고 `formatApiErrorDetail`이 `detail/message/error` 키를 순서대로 해석. 401이면 `window.location.assign('/login?next=…')`. `ListEnvelope<T>` 타입이 백엔드 목록 envelope와 1:1.
  - 폴링 상수: `RUN_QUEUE_REFETCH_INTERVAL_MS 10_000`, `RUN_HISTORY_REFETCH_INTERVAL_MS 60_000` (`lib/api.ts` 264~268줄).
- **인증 경계** (`frontend/src/proxy.ts`, `frontend/src/lib/auth.ts` 548줄, `frontend/src/app/api/auth/{login,logout}/route.ts`, `frontend/src/app/api/v1/[...path]/route.ts`, `frontend/src/lib/auth-audit.ts`)
  - Next 16 `proxy.ts`(구 middleware)가 `/login`, `/api/auth/*`, `/_next/*`, `/favicon.ico` 외 전부에 세션을 요구. API 경로는 `401 {error:"AUTH_REQUIRED"}`, 페이지는 `/login?next=`로 redirect.
  - 세션 쿠키 `ktc_ui_session`, TTL 8시간, HMAC 서명 payload(`aud/exp/fp/iat/sid/sub/v`), 비밀번호 PBKDF2-SHA256 310,000회(`KTC_ADMIN_PASSWORD_HASH`), 세션 secret 최소 32자(`KTC_UI_SESSION_SECRET`), 폐기 세션은 프로세스 메모리 Map, 로그인 실패 5회/10분 rate limit, same-origin 검사(Origin 헤더 부재는 거부 — 2026-09-04 docker-manager와 정렬), `KTC_UI_PUBLIC_ORIGINS`로 TLS 종단 프록시 뒤 허용 origin 명시.
  - BFF catch-all `/api/v1/[...path]`: `runtime="nodejs"`, `force-dynamic`, hop-by-hop 및 `x-api-key`/`x-ktc-actor`/`x-ktc-admin-proxy-secret` 헤더 제거 후 서버 전용 `BACKEND_API_KEY`를 `X-API-Key`로 주입, 세션 유효 시 `X-KTC-Actor`+`X-KTC-Admin-Proxy-Secret`(`KTC_ADMIN_PROXY_SECRET`) 추가, `request.signal`을 upstream에 전달하고 abort 시 499. 로그인/로그아웃 이벤트는 `auth-audit.ts`가 백엔드 `/api/v1/admin/auth-events`로 전달.
- **라우팅/화면 목록** (`frontend/src/app/`): 페이지 11개 — `/`(결과, `DestinationWorkspace`+지도), `/collect`, `/jobs`, `/jobs/[jobId]`, `/review`, `/review/[id]`, `/place/[id]`, `/settings`, `/status`, `/api-test`, `/login`; `error.tsx`, `global-error.tsx`. Route Handler 3개(`/api/auth/login`, `/api/auth/logout`, `/api/v1/[...path]`). **admin 화면 11 / 사용자 화면 0**. 페이지 컴포넌트는 대부분 서버 컴포넌트 껍데기 + `"use client"` 워크스페이스 조합(`app/page.tsx`는 RSC, `app/review/page.tsx`는 client).
- **반응형/모바일**: Tailwind 기본 breakpoint(`screens` 재정의 없음). 접두 사용량 `sm:` 15, `md:` 12, `lg:` 128, `xl:` 8, `2xl:` 0 → 데스크톱 우선, `lg`(1024px) 단일 분기가 지배적. `lib/use-is-mobile.ts`는 `(max-width: 767px)` matchMedia + `useSyncExternalStore`로 SSR-safe 판정하며 `DestinationWorkspace`·`ReviewWorkspace`에서 "모바일=새 페이지 / PC=모달" 분기. `design.md`: 데스크톱 Rail 16rem/접힘 4rem, 모바일 가로 스크롤 메뉴, 320/375/414/768px에서 문서 가로 스크롤 금지. 터치 밀도: 컨트롤 36px/30px 두 종류(`--control-height`), `min-h-11`/`touch-manipulation` 사용 0건(ADR-29의 44px 터치 규칙은 2026-08 리디자인에서 map 기준 36px로 대체됨 — `design.md` "컨트롤 높이" 절).
- **i18n / 접근성 / focus / reduced-motion**: i18n 라이브러리 없음(`html lang="ko"`, 문자열 한국어 하드코딩, `toLocaleString("ko-KR")` 사용). `aria-*` 156회, `focus-visible` 68회, 전역 `:focus-visible` 2px brand outline, nav active는 `aria-current`+좌측 2px mark, 로딩 버튼은 라벨 유지+spinner 겹침, reduced-motion 전역 규칙(spinner 예외) — `design.md` "상태와 접근성", `globals.css`.
- **테스트·품질**
  - `vitest ^4.1.9`(4.1.9), `frontend/vitest.config.ts` environment `node`, include `src/**/*.test.ts`(18개: `lib/*.test.ts` 14 + `components/review/*.test.ts` 4). CLAUDE.md 기준 229 케이스.
  - Playwright는 별도 패키지 `tests/`(`@playwright/test ^1.44.0`, 설치 1.60.0): chromium 단일 프로젝트, `workers: 1`, `fullyParallel: false`, webServer로 backend `127.0.0.1:18080`·frontend `127.0.0.1:13100` 자동 기동(`tests/scripts/start-backend.mjs`, `start-frontend.mjs`, `seed_e2e.py`), `KTC_LIVE_E2E=1`이면 n150 live 전용 `live-shell.spec.ts`(5 test)만, 로컬은 `ktc.spec.ts`(45 test).
  - ESLint: `frontend/eslint.config.mjs` flat config = `eslint-config-next/core-web-vitals` + `eslint-config-next/typescript`만(추가 플러그인 없음). `eslint ^9.39.4`(9.39.4). react-doctor·prettier 설정 파일 **없음**(추적 파일에 없음).
  - `frontend/tsconfig.json`: `strict: true`, `target es2017`, `moduleResolution bundler`, `paths @/* → ./src/*`, `exclude`에 `src/**/*.test.ts`, `vitest.config.ts`(테스트는 tsc 검사 밖).
- **빌드/배포**: `frontend/next.config.mjs`는 `allowedDevOrigins: ["127.0.0.1"]`, `reactStrictMode: true`만(output/transpilePackages/images 설정 없음). `frontend/Dockerfile`: `node:22-slim`, `npm ci`, `EXPOSE 3000`, **`CMD ["npm","run","dev"]`**(개발 서버, 파일 헤더 "초안") — prod도 같은 이미지가 쓰이는지는 미확인(docker-manager 소관). 포트: dev 3000, Compose host `12605 → 3000`, `dev:live` 12605.
- **디자인 문서**: `design.md`(루트, 2026-08-31, Hallmark 형식: 방향/색상과 표면/타이포와 밀도/레이아웃과 컴포넌트/상태와 접근성)와 `frontend/docs/DESIGN-RULES.md`(47줄, 10개 적용 원칙 + 반응형 + 금지 + 적용 위치). 핵심: 장르 editorial-utilitarian, Rail-Workbench, 보라 브랜드 유지(초록 금지), flat `border + rounded-panel`(shadow는 modal/popover만), Pretendard, 본문 15px/보조 13.5px·12px/제목 24px, `tabular-nums`, 한국어 라벨 uppercase 금지, KPI는 `StatStrip`, 금지 패턴: 임의 hex·순수 검정·큰 gradient·유리 효과·중첩 카드·색상만의 상태 표현·페이지별 recipe.

## 4. 백엔드

### 4.1 `ktc` (`backend/`, 래퍼 `etl/`·`mcp/`·`scheduler/`)

- **python 버전/빌드/lockfile**: `Dockerfile.python` `FROM python:3.11-slim`; 문서는 "Python 3.10+"(`AGENTS.md`, `SKILL.md`). **빌드 시스템 없음**(`pyproject.toml`/`setup.cfg` 부재), **lockfile 없음**. 의존은 `backend/requirements.txt`(하한 `>=` 핀 + `mcp<2` 상한 1건 + `python-vworld-api @ https://github.com/digitie/python-vworld-api/archive/a1fea840531f0b4d8e1b6a0db85e15063532602d.zip` 커밋 아카이브 핀). `etl/requirements.txt`·`mcp/requirements.txt`·`scheduler/requirements.txt`는 `-r ../backend/requirements.txt` 뒤에 추가분만 선언(etl: `google-api-python-client>=2.122.0`, `ffmpeg-python>=0.2.0` 등; mcp: `mcp>=1.2.0`; scheduler: `apscheduler>=3.10.4`, `psycopg[binary]>=3.1.18`). `Dockerfile.python`은 네 파일을 한 번에 `pip install`한다. 2026-09-04 장애(전이 의존 `mcp` 2.1.1 유입)로 `mcp<2`를 직접 핀 — 하한 전용 핀 방식의 대표적 리스크 사례(`docs/journal.md` 2026-09-04).
- **프레임워크·핵심 의존 선언 범위**(`backend/requirements.txt`): `fastapi>=0.110.0`, `uvicorn>=0.28.0`, `sqlalchemy>=2.0.28`, `asyncpg>=0.29.0`, `geoalchemy2>=0.14.7`, `alembic>=1.13.1`, `APScheduler>=3.11.0`, `pydantic>=2.6.4`, `pydantic-settings>=2.2.1`, `google-generativeai>=0.4.1`, `requests>=2.31.0`, `httpx>=0.27.0`, `prometheus-client>=0.20.0`, `python-dotenv>=1.0.1`, `boto3>=1.34.0`, `youtube-transcript-api`, `yt-dlp`, `faster-whisper`, `pyproj`, **`pytest>=8.1.1`, `pytest-asyncio>=0.23.5`(런타임 requirements에 테스트 의존 포함)**. structlog·typer·tenacity·dagster·psycopg(backend 본체)·testcontainers **없음**.
- **앱 구성** (`backend/main.py`)
  - 앱 팩토리 `create_app()`: `FastAPI(title="Travel Concierge Admin UI API", version="0.1.0", lifespan)`; lifespan에서 위험 인증 구성 경고 후 `init_db()`.
  - 미들웨어: `CORSMiddleware(allow_origins=settings.cors_allow_origins, allow_credentials=True, allow_methods/headers="*")`, HTTP 메트릭 수집 `@app.middleware("http")`.
  - 라우터: `backend/ktc/api/routes.py`(**3,759줄 단일 파일**) `router = APIRouter(prefix=API_V1_PREFIX, dependencies=[Depends(require_api_key)])`; 라우트 데코레이터 62개. `tags=`/`operationId` 지정 **없음**(grep 0건). 경로 그룹: `/admin/*`(BFF 전용: `login-events`, `public-api-keys`, `auth-events`), `/destinations/*`(목록·facets·export·unmatched·candidates·bulk·audit·merge-suggestions·correct·deep-research), `/runs/*`, `/harvest*`, `/source-targets/*`, `/features/{snapshot,changes}`, `/themes*`, `/categories*`, `/settings`, `/audit-logs`, `/storage/rustfs`, `/place-search*`, `/videos/{id}/transcript`, `/keywords`, `/jobs/poi-batch`, `/metrics`. 버전 없는 경로는 `/`, `/health`, `/metrics`(app 레벨).
  - 에러 envelope: 커스텀 `exception_handler` **없음**(grep 0건) → FastAPI 기본 `{"detail": …}`/422 validation 응답. 프론트 `formatApiErrorDetail`이 `detail/message/error` 3키를 모두 해석해 흡수한다. API 계약 문서의 오류 표: 400(cursor), 422(검증), 401/403(인증·scope), 409/413(bulk).
  - 페이지네이션: `backend/ktc/services/list_pagination.py`(142줄) — `ListPage` 데이터클래스 `{items,next_cursor,has_more,total,newest_id,newer_than}`, cursor는 URL-safe base64 versioned JSON(`_CURSOR_VERSION=1`, 최대 4,096자, ID 0~2,147,483,647), endpoint·정렬·정규화 filter의 SHA-256 fingerprint, `ensure_repeatable_read()`로 REPEATABLE READ. features API는 별도 sequence cursor(문서 정본 `docs/list-api-contract.md`, ADR-37).
  - 인증 (`backend/ktc/core/security.py` 268줄): 헤더 `X-API-Key`(정적 `API_KEYS`=admin, DB `public_api_keys` SHA-256 해시+scope `read|admin`), VWorld식 `?key=`는 DB read 키만, `X-KTC-Actor`/`X-KTC-Admin-Proxy-Secret` + `KTC_ADMIN_TRUSTED_PROXY_CIDRS`로 BFF 관리자 proxy 인증, `/api/v1/admin` 하위는 proxy 전용, `READ_SCOPE_EXACT_PATHS`/`READ_SCOPE_PATH_PATTERNS` deny-by-default(ADR-36), `APP_ENV in {local,test,e2e}` 무인증 우회, `API_TRUSTED_CLIENT_CIDRS` 무키 우회(read), `/metrics`는 CIDR 또는 `PROMETHEUS_METRICS_API_KEY`. 비밀번호 해시(PBKDF2)와 세션은 Next 측 담당(절 3). argon2 없음.
  - rate limit: 백엔드 HTTP rate limit **미확인/없음**(로그인 rate limit은 Next `lib/auth.ts`, LLM 호출 제한은 `ktc/etl/gemini_rate_limiter.py`).
- **OpenAPI**: export 스크립트·`openapi.json` 저장·CI drift 검사 **없음**(`git grep openapi.json` 0건, `.github/` 부재). FastAPI 자동 문서만. 태그/operationId 규약 없음. 버전 관리는 `/api/v1` prefix(ADR-24)와 문서(`docs/*-api*.md`)의 "마이그레이션 노트"로 수행.
- **설정** (`backend/ktc/core/config.py` 409줄): `class Settings(BaseSettings)`, `SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=True, extra="ignore")`, **env_prefix 없음**(필드명 = 대문자 env 이름, `.env.example`과 1:1 규칙을 docstring에 명시). `.env.example`(308줄, 키 약 105개) 절 구성: 0 고정 host port, 1 프론트엔드(`NEXT_PUBLIC_VWORLD_SERVICE_KEY`, `BACKEND_ORIGIN`, `BACKEND_API_KEY`, `KTC_ADMIN_*`, `KTC_UI_*`), 1.5 실행 환경·인증(`APP_ENV`, `API_AUTH_ENABLED`, `API_KEYS`, `PUBLIC_API_KEY_CACHE_TTL_SECONDS`, `*_CIDRS`, `PROMETHEUS_*`), 2 백엔드·ETL(`DATABASE_URL`, `KTC_TEST_PG_DSN`, Gemini/DeepSeek/`AI_PREPROMPT`/`LLM_RETRY_*`/`GEMINI_RATE_*`, YouTube, transcript/whisper, RustFS 15종, `RAW_MEDIA_STORE_ENABLED`, 지오코딩 키, `KOR_TRAVEL_GEO_V2_*`, `GOOGLE_PLACE_SEARCH_ENABLED`), 3 MCP(`MCP_WRITE_ENABLED`, `MCP_TRANSPORT`, `MCP_HOST/PORT`, `MCP_STREAMABLE_HTTP_PATH`), 4 스케줄러(`SCHEDULER_*`, `SOURCE_SCAN_*`, `CRAWL_*`), 5 프로덕션 예시. 접두 규약: 앱 고유는 `KTC_*`, 나머지는 도메인명(ADR-27 번호 오기 항목: 패키지명 `ktc`, `KTC_*` env, DB `kor_travel_concierge`).
- **관측성**: 로깅은 표준 `logging` + `ktc/core/logging.py` `mask_secret()`(19줄) — structlog 없음. 메트릭(`backend/ktc/telemetry.py`): `ProcessCollector(namespace="ktc")`, `ktc_http_requests`, `ktc_http_request_duration_seconds`, `ktc_run_actions`, `ktc_crawl_runs`, `ktc_crawl_run_errors`, `ktc_crawl_run_metrics_refresh_success` → 접두 `ktc_`(docker-manager `ktdm_*`와 정렬, `docs/tasks.md` 완료 항목). health: `GET /health → {"status":"ok"}`(DB 확인 없음), `/ready` **없음**. Compose healthcheck는 `/health` 폴링.
- **DB**: PostgreSQL + PostGIS(`postgresql+asyncpg://…/kor_travel_concierge`), 스키마 분리 없음(기본 schema, `alembic/env.py` `include_schemas=False`). Alembic: 루트 `alembic.ini`(`script_location = backend/alembic`, `prepend_sys_path = backend`, `timezone = UTC`), `backend/alembic/versions/` 29개, 파일명 `YYYYMMDD_NNNN_slug.py`(예: `20260901_0029_transcript_attempt_run_index.py`). 세션: `create_async_engine(pool_pre_ping=True)`, `async_sessionmaker(expire_on_commit=False)`, `get_session`/`get_repeatable_read_session` 의존성. `init_db()`는 `pg_advisory_xact_lock(176)`로 직렬화 후 PostGIS 확장 보장, **local/test/e2e에서만 `create_all`**, 비-local은 Alembic 소유. 공간: `geoalchemy2` + `ktc/core/spatial.py`(`ST_SetSRID(ST_MakePoint)`, EPSG:4326), `travel_places.geom geometry(Point,4326)`. DB 서버는 `python-kraddr-geo`의 PostgreSQL/PostGIS 재사용(ADR-25); docker-manager는 전용 `kor-travel-concierge-postgres` 12600을 배정(`ktdm-main/docs/ports.md` 28·45행).
- **백업/복원**: 저장소 내 스크립트 **없음**(미확인 — docker-manager 소관으로 추정). Dagster **없음**(소비자인 map 측). CLI: `ktcctl`(bash) → `python -m ktc.cli {api|mcp|scheduler|etl}`(argparse, typer 아님; `backend/ktc/cli.py` 83줄). 스케줄러: `scheduler/worker.py` APScheduler 단일 실행자, `crawl_runs` claim + PostgreSQL advisory lock lease(ADR-13). MCP: `backend/ktc/mcp_server/server.py` `FastMCP("kor-travel-concierge")`(mcp 1.x API), `tools.py` `@server.tool` 등록, transport stdio/streamable-http(`/mcp`), `MCP_WRITE_ENABLED` 게이트, prod는 Caddy basic_auth로 보호.
- **테스트**: `backend/tests/` 평면 구조 62개 `test_*.py`(unit/integration 분리 없음), `backend/pytest.ini` `asyncio_mode = auto`, `testpaths = tests`, `addopts = -q`. `conftest.py` `engine` fixture는 `KTC_TEST_PG_DSN` 없으면 skip(실제 disposable PostGIS, testcontainers 아님), `before_flush` 훅으로 geom/FK 스텁 보정. coverage gate **없음**. **ruff/mypy 설정 파일 없음**(`ruff.toml`/`pyproject` 부재) — journal에 "변경 파일 Ruff 통과" 기록이 반복되나 도구 구성은 코드에 없고 2026-06 기록에는 "backend venv에는 ruff/mypy가 없어 별도 lint/type gate는 실행하지 못했다"(`docs/journal.md` 1770행). import-linter 없음. `AGENTS.md` 체크리스트의 "백엔드 파이썬 코드 스타일 및 린트 검사 통과"는 도구 지정이 없다.

## 5. 문서·에이전트 규약

- **진입 파일**
  | 파일 | 길이 | 역할 |
  |---|---:|---|
  | `AGENTS.md` | 200줄 | 목표, Think/Simplicity/Surgical/Goal-Driven 원칙, **문서 언어 정책(모든 md 한글, 식별자·명령·벤더명만 영문)**, 식별자 표, 개발 환경 정책, 읽기 순서, **지시 우선순위**, DO NOT 10개(main 직접 푸시·키 평문 커밋·YouTube 할당량·Windows 앱 경로·마이그레이션 누락·RustFS 자동 삭제·매칭 실패 자동 확정·PowerShell 작업·push 전 보안 감사 생략·배포 후 로그인 검증 생략), push 전 보안 감사 절차(grep 패턴 포함), 작업 후 체크리스트 |
  | `CLAUDE.md` | 288줄 | 세션 진입점: 프로젝트 현황(T-NNN 완료 요약), 잔존 부채, 브랜치 상태(`codex/*`), 로컬 레이아웃(일부 경로가 `backend/app/`로 구식 — 실제는 `backend/ktc/`), 빠른 명령, ADR 인덱스(ADR-1~35, 45까지의 최신분 누락), 작업 후 의무 |
  | `SKILL.md` | 152줄 | 에이전트 매뉴얼: 정체성, 빠른 시작, DO NOT 8개, 자주 묻는 작업(스키마/Gemini/ETL/RustFS/MCP/E2E), 도메인 어휘 표, 체크리스트 |
  | `design.md` | 55줄 | 디자인 시스템 정본(절 3 참고) |
  | `README.md` | 약 130줄 | 제품 소개, 시스템 구성도, 시작하기(Compose/단독/E2E), 참고 문서, 라이선스 |
  - 지시 우선순위(`AGENTS.md` "지시 우선순위"): 사용자 요청 → `AGENTS.md` → `SKILL.md` → `docs/architecture.md`·`docs/decisions.md` → `docs/tasks.md`·`docs/journal.md`·`README.md` → 기존 코드와 테스트.
  - 언어 정책: 모든 Markdown 한글, 예외 목록 명시(코드 식별자, 명령·경로, 외부 공식 용어, 벤더명, ADR/CHANGELOG/ISO 8601/semver 라벨, 로그 캡처).
- **docs/ 트리와 규약**
  | 문서 | 길이 | 규약 요약 |
  |---|---:|---|
  | `docs/architecture.md` | 714줄 | 설계 기준, 전체 구조, UX 표면(웹/MCP), ETL 4단계, 비동기 모델, DB 엔티티 13절, 프론트 스택, 전환 후보 |
  | `docs/decisions.md` | 1,445줄 | ADR-1~45 본문(핵심) + 말미 "이력·대체·보류 ADR (요약)". 형식: `## ADR-N: 제목` / 상태·날짜·결정자 / 컨텍스트·결정·근거·결과(긍정/부정)·관련. 단일 파일(adr/ 디렉터리 없음). ADR-27 번호 중복(포트 정책 vs 배포명) 기록 |
  | `docs/tasks.md` | 712줄 | `T-NNN` ID(고유 164개, 최대 T-193), 절 `진행 중`/`대기 (우선순위 순)`/`완료`, Agent A/B 두 트랙 병렬 |
  | `docs/journal.md` | 3,385줄 | 역시간순 작업 일지, `## YYYY-MM-DD: 제목` |
  | `docs/dev-environment.md` | 488줄 | Linux/WSL2 환경, RustFS, 프론트, ETL, MCP, 스케줄러, Compose 검증, E2E, 트러블슈팅, prod 배포(ADR-28), Gemini 티어 |
  | `docs/provider-policy.md` | 318줄 | 외부 provider 정책 매트릭스, 릴리스 게이트(G10), 코드 충돌 지점 C-1~C-7, kill switch 3종(`RAW_MEDIA_STORE_ENABLED`, `GOOGLE_PLACE_SEARCH_ENABLED`, `VISUAL_EXTRACTION_ENABLED`), ADR-15 재검토 초안, 결정 필요 항목 11개 |
  | `docs/list-api-contract.md` | 205줄 | 목록 API 공통 envelope·cursor·정렬·filter 정규화·경량 payload·`queue_reason` enum 14종·프런트 전환 |
  | `docs/themes-api.md` | 194줄 | `/themes`, `/themes/places`, `/themes/video/{id}/places`(≥5 POI 게이트), POI item 스키마, `include=sources`, 오류 코드, 파괴적 변경 마이그레이션 노트 |
  | `docs/feature-export-api.md` | 205줄 | `/features/snapshot|changes`, sequence cursor, item payload(`place.address` 행정코드), operation 의미, 오류, 스키마 확장·재발행 |
  | `docs/improvement-roadmap-2026-07.md` | 1,360줄 | 진단→채택/기각→목표 상태→실행 계획(PR-NN 블록) |
  | `docs/pr-review-2026-06.md` | 126줄 | PR 리뷰 종합(P0~P3 TODO, 횡단 주제) |
  | `docs/cross-repo-consistency-actions-2026-06-10.md` | 97줄 | map 소비자 구현과의 정합 액션(TA-) |
  | `docs/youtube-feature-pipeline-plan.md`, `plan-t172-*`, `plan-t173-*`, `e2e-report-2026-06-20-*` 3종 | — | 계획·리포트 |
  - 없는 것: `tasks-rule`/`tasks-done`, `adr/` 디렉터리, `runbooks/`(prod 런북은 gitignore된 `docs/deploy-runbook.local.md`, `docs/prod-access.local.md`), `reviews/`, `archive/`, `resume`.
- **개발 환경 정본**: Linux/WSL2 bash(ADR-23/ADR-33). PowerShell/cmd 금지(E2E fallback 예외). `.gitattributes` `* text=auto eol=lf`. 앱 런타임은 Docker Compose 단일 호스트(ADR-18).
- **worktree 정책**: 명문 규칙은 없으나 `claude.json`/`codex.json`/`opencode.json`/`antigravity.json`/`.codex/config.toml`의 codegraph·filesystem MCP `cwd`가 각각 `F:\dev\kor-travel-concierge-claude|codex|opencode|antigravity`로 고정 → 에이전트별 worktree 운영이 관행(추정). `AGENTS.md`도 "각 git worktree에도 런북을 같은 경로로 복사"라고 언급.
- **codegraph**: `.gitignore`에 `.codegraph/`, MCP 설정 4벌에 `@colbymchenry/codegraph serve --mcp` 등록, `AGENTS.md`는 codegraph 명령도 Linux에서 실행하도록 강제.
- **리뷰 정책**: `AGENTS.md`에 공식 규칙은 없으나 `CLAUDE.md`(T-185 "3개 agent의 적대적 검토를 세 번 교차 반복")와 `docs/journal.md`(40건)·`docs/tasks.md`(25건)에 "적대적 리뷰/검토" 관행이 기록됨 → 다중 에이전트 적대적 리뷰가 사실상 규범(문서화된 "2인" 규칙은 미확인).
- **PR/브랜치**: `main` 직접 푸시 금지, 브랜치 `codex/*`(예: `codex/admin-login-api-keys`), PR 스쿼시 제목 `feat|fix|docs|test|deps: … (#NNN)`.
- **보안 감사**: push 전 `git diff --cached --name-only`에 `*.local.md`/`.env*`(예외 `.env.example`)/`prod-access*` 부재 확인 + `grep -nEi '(api[_-]?key|secret|password|…)'` 스캔 절차가 `AGENTS.md`에 명문화. `.gitignore`가 `*.local.md`, `docs/deploy-runbook.local.md`, `docs/prod-access.local.md`, `.claude/settings.local.json`, `.local/`, `.codegraph/`, `.playwright-mcp/`를 제외.
- **에이전트 자산**: `.claude/agents/`(api-designer, backend-developer, frontend-developer, mobile-developer, ui-designer — 범용 페르소나, `model: opus`), `.claude/skills/`(postgres, design-postgis-tables, pgvector-semantic-search 등 8종)이 `.agents/`·`.opencode/`·`.codex/`에 동일 내용으로 미러링(합계 71 파일).

## 6. CI·배포·운영

- **CI**: `.github/` 디렉터리 **없음** → GitHub Actions workflow 0개, gate 없음. `.pre-commit-config.yaml` 없음. 품질 게이트는 사람이 `AGENTS.md` 체크리스트를 수동 실행(pytest, `npm run lint/type-check/build`, Playwright).
- **Compose**: `docker-compose.yml` 단일 파일 — `api`(`python -m ktc.cli api --host 0.0.0.0 --port 8000`, host `${API_HOST_PORT:-12601}:8000`, healthcheck `/health`), `mcp`(`12602:12402`, streamable-http `/mcp`), `scheduler`(포트 없음), `frontend`(`12605:3000`, `BACKEND_ORIGIN=http://api:8000`), 선택 profile `embedded-rustfs`(`rustfs/rustfs:latest`, 12101/12105). 공통 env anchor `x-python-env`. `env_file: ${APP_ENV_FILE:-.env}`로 prod env 파일 override. `extra_hosts host.docker.internal:host-gateway`로 호스트 PostgreSQL 5432·RustFS 12101 접근.
- **이미지**: `Dockerfile.python`(python:3.11-slim, apt ffmpeg, 4개 requirements 설치, `PYTHONPATH=/app:/app/backend`, `FFMPEG_PATH=/usr/bin/ffmpeg`), `frontend/Dockerfile`(node:22-slim, dev 서버).
- **포트 할당**(ADR-27, `ktdm-main/docs/ports.md` 28행 `conc 12600-12699`): API 12601, MCP 12602(컨테이너 내부 12402), Web 12605, RustFS S3 12101/콘솔 12105(외부 고정 서비스), PostgreSQL 5432(호스트) 또는 docker-manager 전용 12600, E2E backend 18080/frontend 13100, 단독 dev 3000/12601.
- **prod(n150) 규약**: prod는 `kor-travel-docker-manager`가 올리고(ADR-28) 공식 도메인 5개(Web/API/MCP/S3-API/S3-콘솔)를 `deploy/Caddyfile`이 Host 기반으로 고정 포트에 프록시(자동 TLS, MCP는 basic_auth 기본 ON + 잠금 기본 해시 fail-safe). `APP_ENV=production`, `API_KEYS`, `BACKEND_API_KEY`, `FORWARDED_ALLOW_IPS=*`, `KTC_ADMIN_PASSWORD_HASH`. 배포 후 로그인 POST(200 + Set-Cookie) 검증 의무(`AGENTS.md` DO NOT 10). 상세 런북은 gitignore된 `docs/deploy-runbook.local.md`(미열람, 존재 여부 미확인).
- **시크릿 처리**: `.env`/`.env.production` gitignore, `.env.example`은 placeholder만, 도메인도 env로만 주입, 로그 마스킹 `mask_secret`, DB 공개 키는 SHA-256 해시+끝 6자 hint만 저장.
- **운영 스크립트**: `scripts/start-live.sh`(dev 전용, 고정 포트 점유 시 사용자 확인 후 회수), `scripts/stop-fixed-ports.sh`(포트 회수 — README는 "python-krtour-map에서 차용"), `scripts/verify-docker-compose.sh`(smoke), `scripts/verify_rustfs.py`, `scripts/init_rustfs_buckets.py`, `scripts/backfill-place-admin-codes.py`(geo v2 행정코드 백필).

## 7. 외부 연동 (cross-repo)

| 상대 | 방향 | 방식 | 근거 |
|---|---|---|---|
| `kor-travel-geo` v2 | concierge → geo | `httpx`로 `{KOR_TRAVEL_GEO_V2_BASE_URL}/v2/reverse`, `/v2/regions/within-radius` 호출, 키 `KOR_TRAVEL_GEO_V2_API_KEY`(비면 `VWORLD_SERVICE_KEY` 대체), 결과를 `travel_places` 행정코드에 저장(`ADMIN_CODE_SOURCE="kor-travel-geo-v2"`) | `backend/ktc/etl/admin_region_service.py` 109·232·274·321행, `config.py` 242~244·355행 |
| `kor-travel-map` | map → concierge | Dagster provider `kor-travel-concierge-youtube`가 `/api/v1/features/snapshot|changes`를 DB `read` 키(`X-API-Key`)로 pull; `feature_id` 생성은 map 책임 | `docs/feature-export-api.md`, `docs/cross-repo-consistency-actions-2026-06-10.md` |
| PinVi | 간접 | map이 만든 `feature_id`/`feature_snapshot`을 PinVi POI row에 저장, concierge DB 직접 접근 없음 | `docs/feature-export-api.md` "기본 원칙" |
| `kor-travel-docker-manager` | 정책 소유 | 포트 대역(`conc` 126xx), prod 오케스트레이션·도메인, 로그인 CSRF Origin 검사 정렬, Prometheus namespace 정렬 | ADR-27/28, `docs/tasks.md` 완료 항목, `ktdm-main/docs/ports.md` |
| `python-kraddr-geo` | 인프라 공유 | 같은 PostgreSQL/PostGIS 서버, 별도 DB `kor_travel_concierge` | ADR-25, `.env.example` DATABASE_URL |
| `python-vworld-api` | 라이브러리 | `from vworld import AsyncVworldClient, VworldError, VworldNoDataError` 직접 사용, wrapper 금지(ADR-19); 핀은 GitHub 커밋 아카이브 URL | `backend/requirements.txt`, `ktc/etl/geocoding.py` 33행, `geocode_service.py` 18행 |
| VWorld WMTS | 브라우저 | `maplibre-gl 6.0.0` raster source 직접 구성, `NEXT_PUBLIC_VWORLD_SERVICE_KEY` 브라우저 노출; `maplibre-vworld-react`/`maplibre-vworld-js`·vworld-map 벤더 tgz **미사용** | `frontend/src/components/VWorldMap.tsx` 291행, `package.json` |
| Kakao/Naver/Google Places/Gemini/DeepSeek/YouTube | 직접 | `httpx` 직접 호출(`dapi.kakao.com`, `naveropenapi.apigw.ntruss.com`, `openapi.naver.com`, `places.googleapis.com`, `generativelanguage.googleapis.com`), `google-api-python-client`(YouTube) | `ktc/etl/geocoding.py` 525·665행, `place_search.py` 30·32행, `gemini_client.py` 20행 |
| ServiceToken | 없음 | 서비스 간 인증은 `X-API-Key`(DB read 키)와 BFF shared secret뿐, 공통 ServiceToken 개념 **없음** | `security.py` |
| `digitie/python-*-api` 13종 | 미사용 | `python-vworld-api` 외 사용 흔적 없음(미확인: 전이 의존) | `requirements.txt` |

## 8. 공통화 후보

| # | 영역 | 근거 경로 | 신뢰도 | 비고 |
|---|---|---|---|---|
| 1 | Tailwind v4 CSS-first 기반 토큰 파일(`--ktc-*` 3단 매핑: 원시 → 의미 → shadcn) | `frontend/tokens.css`, `frontend/src/app/globals.css` | high | 접두를 공통 접두로 바꾸고 브랜드 색만 앱별 override하는 구조로 일반화 가능. `@config` JS config 잔존은 정리 대상 |
| 2 | Base UI 기반 shadcn `base-nova` 프리미티브 18종(button/input/dialog/alert-dialog/select/tabs/field/…) | `frontend/src/components/ui/*`, `frontend/components.json` | high | map admin과 동일 계보(주석 "최신 기준 레포"), 변형 분리 방식만 다름 |
| 3 | Button 동작 계약(`loading` → `aria-disabled`+`aria-busy`+spinner 겹침, `disabledReason` title, `blockBusyActivation`) | `frontend/src/components/ui/button.tsx` 55~115행, map `button.tsx` 25~57행 | high | 선행 보고서 §3.3 "map Button 계약"과 동일하므로 공통 Button의 기준 동작으로 채택 가능 |
| 4 | Rail-Workbench `AppShell`(그룹 nav, 접힘 상태 localStorage, `aria-current`, 모바일 가로 스크롤 메뉴, main-content 스킵 대상) | `frontend/src/components/AppShell.tsx`, `design.md` | high | nav 항목만 앱별 주입 |
| 5 | 대시보드 조각 `panels.tsx`(Section/Panel/PanelHeader/MetricCard/Metric/CountList/EmptyState), `StatStrip`, `SectionCard`, `detail.tsx` | `frontend/src/components/panels.tsx`, `StatStrip.tsx`, `SectionCard.tsx`, `detail.tsx`, ADR-34 | high | 이미 "화면 로컬 재정의 금지·단일 출처" 규약 |
| 6 | `ConfirmActionButton`(AlertDialog), `HelpTip`(클릭형 popover), `CopyButton` | `frontend/src/components/ConfirmActionButton.tsx`, `HelpTip.tsx`, `CopyButton.tsx`, ADR-34 | high | 작은 UI 부품 후보(선행 보고서 표 §2와 일치) |
| 7 | 관리자 로그인 + BFF 프록시 패턴(Next `proxy.ts`, HMAC 세션 쿠키, PBKDF2, rate limit, same-origin 검사, catch-all `/api/v1/[...path]` 키 주입, auth audit 전달) | `frontend/src/proxy.ts`, `lib/auth.ts`, `app/api/v1/[...path]/route.ts`, `lib/auth-audit.ts`, ADR-32 | high | geo PR #399와 같은 형태로 만들었다고 ADR-32가 명시 → 이미 두 저장소에 복제됨. docker-manager와 CSRF 정렬 이력도 있음 |
| 8 | 목록 API 공통 envelope + watermark keyset cursor(`{items,next_cursor,has_more,total,newest_id,newer_than}`, fingerprint, REPEATABLE READ) | `backend/ktc/services/list_pagination.py`, `docs/list-api-contract.md`, ADR-37, `frontend/src/lib/api.ts` `ListEnvelope<T>` | high | Python 모듈 + TS 타입 + 문서 규약을 한 묶음으로 공통화 가능 |
| 9 | `X-API-Key` 인증 의존성(정적 admin 키 + DB 발급 키 SHA-256/scope `read|admin` + deny-by-default 경로 목록 + APP_ENV 로컬 우회 + trusted CIDR) | `backend/ktc/core/security.py`, `services/public_api_key_service.py`, ADR-24/36 | medium | 경로 allowlist는 앱별 주입 필요; 다른 형제(geo/map)의 인증 방식과 대조 필요 |
| 10 | pydantic-settings `Settings` 관례(`env_file=".env"`, `case_sensitive=True`, `extra="ignore"`, 필드명=env명, `.env.example` 1:1 동기화 규칙, `mask_secret`) | `backend/ktc/core/config.py` 68~80행, `ktc/core/logging.py` | medium | env_prefix 미사용이라 공통 접두 정책과 충돌 가능 |
| 11 | Prometheus 메트릭 접두 `<app>_` + `ProcessCollector(namespace)` + HTTP 요청 미들웨어 | `backend/ktc/telemetry.py`, `backend/main.py` `collect_http_metrics` | high | docker-manager `ktdm_*`와 이미 정렬한 관례 → 공통 규칙으로 승격 가능 |
| 12 | Alembic 관례(파일명 `YYYYMMDD_NNNN_slug`, 루트 `alembic.ini` + `backend/alembic`, local만 `create_all`, advisory lock bootstrap) | `alembic.ini`, `backend/alembic/versions/`, `backend/ktc/core/database.py` 143~174행 | medium | 명명 규칙은 공통 규칙 후보, bootstrap 로직은 앱 고유 |
| 13 | 고정 포트 대역 정책(126xx, docker-manager 단일 출처)과 `stop-fixed-ports.sh`/`start-live.sh` 포트 회수 스크립트 | ADR-27, `scripts/stop-fixed-ports.sh`, `scripts/start-live.sh`, README("python-krtour-map에서 차용") | high | 이미 형제 저장소 간 복제된 스크립트 → 공통 도구 후보 |
| 14 | 디자인 규칙 문서 형식(`design.md` Hallmark 절 구성 + `docs/DESIGN-RULES.md` 적용 원칙/반응형/금지/적용 위치) | `design.md`, `frontend/docs/DESIGN-RULES.md`, ADR-29 | high | 색 톤·장르·금지 패턴 규칙을 common 규칙 문서의 템플릿으로 |
| 15 | 문서·에이전트 규약(AGENTS/CLAUDE/SKILL 역할 분담, 지시 우선순위, 한글 문서 정책, T-NNN/ADR/journal 형식, push 전 보안 감사 절차, `*.local.md` gitignore) | `AGENTS.md`, `CLAUDE.md`, `SKILL.md`, `docs/tasks.md`, `docs/decisions.md`, `.gitignore` | high | canview 구조와 대조해 common 규약으로 통합 가능 |
| 16 | 접근성·모션 레시피(전역 `:focus-visible` 2px outline, reduced-motion 전역 축소+spinner 예외, `aria-current` nav, 로딩 버튼 라벨 유지) | `frontend/src/app/globals.css`, `design.md` "상태와 접근성" | high | CSS 조각으로 그대로 공통화 가능 |
| 17 | `useIsMobile`(matchMedia + `useSyncExternalStore`, 767px) 및 "모바일=페이지/PC=모달" 분기 규약 | `frontend/src/lib/use-is-mobile.ts`, `DestinationWorkspace.tsx`, `ReviewWorkspace.tsx` | medium | breakpoint 값은 common 정책으로 합의 필요 |
| 18 | `requestJson`/`ApiRequestError`/`formatApiErrorDetail` fetch 래퍼(401 → 로그인 redirect) | `frontend/src/lib/api.ts` 506~596행 | medium | 에러 envelope가 백엔드마다 달라 3키 해석 로직이 생김 → common 에러 envelope 정의와 함께 정리 |
| 19 | Playwright 하니스 구조(별도 `tests/` 패키지, webServer 자동 기동 스크립트, live/local 스위트 분리, `workers: 1`) | `tests/playwright.config.ts`, `tests/scripts/*.mjs`, `tests/e2e/*.spec.ts` | medium | 포트·seed는 앱 고유 |
| 20 | 외부 provider 정책 매트릭스·kill switch 문서 형식 | `docs/provider-policy.md` | low | 내용은 concierge 고유지만 "약관 확인일·버전·TTL·attribution" 표 형식은 map/pinvi에도 적용 가능 |
| 21 | MCP 서버 노출 규약(streamable-http `/mcp`, 쓰기 게이트 env, 프록시 basic_auth fail-safe) | `docker-compose.yml` mcp 서비스, `deploy/Caddyfile`, ADR-28 | low | docker-manager도 MCP를 가질 경우 규칙 공통화 |

## 9. 이 저장소 고유 차이·주의점

| 영역 | 내용 | 공통화 시 영향 |
|---|---|---|
| 라이선스 | MIT(형제 geo/map/weather는 GPL-3.0, 선행 보고서 §9) | common이 GPL-3.0이면 concierge가 common을 소비할 때 라이선스 결합 검토 필요; concierge 코드를 common으로 이식할 때는 MIT → GPL 방향이라 허용되나 저작권 표기 유지 필요 |
| Tailwind 설정 방식 | v4 엔진 + `@config tailwind.config.ts` 혼합(`@theme` 미사용), 토큰은 `--ktc-*` 3단 매핑, `globals.css`에 구 fallback 값 블록 잔존 | 공통 토큰을 `@theme`로 배포하면 JS config의 `colors` 매핑과 이중 정의가 됨 → `tailwind.config.ts` 제거 계획 필요 |
| 색 톤 | 보라 브랜드(`#7c3aed`), 짙은 보라 Rail(`#2e1065`), 웜그레이/크림 surface. map/geo 계열의 초록/teal과 의도적으로 다름(`design.md` "초록색 브랜드 팔레트로 교체하지 않는다") | common 토큰은 브랜드 hue를 앱별 override 가능하게 설계해야 함; 상태색·surface·radius·shadow는 map 값과 동일 계열 |
| 다크 모드 | `.dark` 값은 정의됐으나 토글 없음, light 전용 운영 콘솔 | common이 다크 기본을 요구하면 concierge는 검증되지 않은 dark 값이 노출됨 |
| 프리미티브 세트 | Base UI 단일 계열, Radix 0개, `shadcn` CLI가 dependencies에 포함, `data-table`/`tooltip`/`sonner`/`skeleton` 없음 | map 기준 세트로 확장 시 신규 도입; 기존 E2E 셀렉터가 Base UI DOM 계약에 결합(ADR-34 부정 결과) |
| 화면 크기 | `ReviewWorkspace.tsx` 4,386줄, `routes.py` 3,759줄, `api.ts` 1,668줄의 거대 단일 파일 | 공통 부품 추출 시 리팩터링 비용 큼; 라우터 단일 파일이라 태그/모듈 분리부터 필요 |
| 백엔드 패키징 | `pyproject.toml`/lockfile 없음, 하한 전용 `requirements.txt` 4벌, 테스트 의존이 런타임 requirements에 포함, `python-vworld-api`는 커밋 아카이브 URL 핀 | "라이브러리/플랫폼 버전 일치화" 정책 적용 시 uv/pyproject 전환과 lock 도입이 선행돼야 함; 2026-09-04 `mcp` 2.x 유입 장애가 핀 부재의 실증 사례 |
| 린트/타입 도구 | ruff/mypy 설정 없음(journal은 ad hoc Ruff 실행 기록), eslint는 next 기본 프리셋만, prettier 없음 | common의 ruff/mypy/eslint 규칙을 도입하면 기존 코드 대량 위반 가능(journal 985행 "기존 미사용 import 12건") |
| CI 부재 | `.github/` 없음, pre-commit 없음 | common 정책의 gate(OpenAPI drift, lint, 버전 일치)를 적용하려면 CI를 처음부터 신설 |
| OpenAPI | export/저장/drift 검사 없음, tags/operationId 없음, 계약은 md 문서 4종이 정본 | common OpenAPI 규약 도입 시 라우터에 태그·operationId 부여와 export 스크립트 신설 필요 |
| 인증 모델 | 관리자 단일 계정(Next 세션) + `X-API-Key`(DB read/admin) + BFF shared secret; ServiceToken 없음; 로그인 rate limit·세션 폐기가 프로세스 메모리 | 공통 ServiceToken/세션 저장소를 도입하면 ADR-32 "다중 인스턴스 시 Redis/PostgreSQL 필요" 부채와 함께 처리 |
| 지도 | `maplibre-gl` 직접 + VWorld WMTS URL 하드코딩, 공유 라이브러리(`maplibre-vworld-react`) 미사용, 브라우저에 VWorld 키 노출(`NEXT_PUBLIC_*`) | common map view를 도입하면 `VWorldMap.tsx` 316줄 대체 가능하나 마커 번호/한국 bounds 등 앱 고유 로직 분리 필요 |
| 개발 환경 | Linux/WSL2 bash 전용, PowerShell 금지(E2E fallback만), 에이전트별 worktree cwd가 Windows 경로로 MCP 설정에 박힘 | common 개발 규약이 Windows PowerShell 정본이면 ADR-23/33과 정면 충돌 |
| 반응형 | `lg:` 편중, 컨트롤 36/30px(44px 터치 규칙 폐기), `useIsMobile` 767px | common PC/Mobile 규칙에서 breakpoint·터치 밀도를 정하면 concierge는 재조정 대상 |
| 데이터 정책 | provider 약관 게이트(YouTube 원본 저장, Google Places 표시 등)와 kill switch 3종, RustFS 무기한 보존 | common export 규약(feature/POI 필드 경계) 정의 시 `docs/provider-policy.md` C-6 "provider 원본 vs 파생 필드 경계" 결정과 동기화 필요 |
| 문서 이력 | `CLAUDE.md` 레이아웃 절이 `backend/app/`·`ktc.mcp_server/`·`tests\.tmp\e2e.db` 등 구식 경로를 포함, ADR 인덱스가 ADR-35까지만 | common 규약 도입 시 정본 문서 최신화 선행 |

## 10. 버전 표

| 항목 | 선언 범위(근거) | lockfile/이미지 설치 버전 |
|---|---|---|
| node | `engines.node >=22` (`frontend/package.json`); 문서 "Node.js 20+"(`AGENTS.md`) | 이미지 `node:22-slim`(`frontend/Dockerfile`); 정확 패치 버전 미확인 |
| npm | 미선언(`packageManager` 없음) | `package-lock.json` lockfileVersion 3 |
| next | `^16.2.7` | 16.2.7 |
| react / react-dom | `^19.2.8` | 19.2.8 |
| typescript | `^5.4.5` (frontend), `^5.4.5` (tests) | 5.9.3 (frontend) |
| tailwindcss | `^4.3.1` | 4.3.1 |
| @tailwindcss/postcss | `^4.3.1` | 4.3.1 |
| @base-ui/react | `^1.5.0` | 1.5.0 |
| radix-ui | 미사용 | lock 내 `@radix-ui/*` 0개 |
| shadcn (CLI) | `^4.10.0` (dependencies) | 4.10.0 |
| lucide-react | `^1.17.0` | 1.17.0 |
| tw-animate-css | `^1.4.0` | 1.4.0 |
| pretendard | `1.3.9` | 1.3.9 |
| eslint / eslint-config-next | `^9.39.4` / `^16.2.7` | 9.39.4 / 16.2.7 |
| vitest | `^4.1.9` | 4.1.9 |
| playwright (`@playwright/test`) | `^1.44.0` (`tests/package.json`) | 1.60.0 (`tests/package-lock.json`) |
| @tanstack/react-query | `^5.40.0` | 5.101.0 |
| zod | `^4.4.3` | 4.4.3 |
| zustand | 미사용 | — |
| react-hook-form / @hookform/resolvers | `^7.51.5` / `^3.4.2` | 7.77.0 / 3.10.0 |
| maplibre-gl | `^6.0.0` | 6.0.0 |
| class-variance-authority / clsx / tailwind-merge | `^0.7.1` / `^2.1.1` / `^3.6.0` | 0.7.1 / 2.1.1 / 3.6.0 |
| postcss / autoprefixer | `^8.4.38`(override `$postcss`) / `^10.4.19` | 8.5.15 / 10.5.0 |
| python | 이미지 `python:3.11-slim`; 문서 3.10+ | 3.11(패치 미확인), lockfile 없음 |
| fastapi | `>=0.110.0` | 미확인(lock 없음) |
| uvicorn | `>=0.28.0` | 미확인 |
| pydantic / pydantic-settings | `>=2.6.4` / `>=2.2.1` | 미확인 |
| sqlalchemy | `>=2.0.28` | 미확인 |
| alembic | `>=1.13.1` | 미확인 |
| asyncpg | `>=0.29.0` | 미확인 |
| psycopg | `psycopg[binary]>=3.1.18` (scheduler만) | 미확인 |
| geoalchemy2 | `>=0.14.7` | 미확인 |
| APScheduler | `>=3.11.0` (backend), `apscheduler>=3.10.4` (scheduler) | 미확인 |
| mcp | `<2` (backend), `>=1.2.0` (mcp) → 1.x | journal 기록 로컬 해석 1.29.1(2026-09-04) |
| prometheus-client | `>=0.20.0` | 미확인 |
| httpx | `>=0.27.0` | 미확인 |
| python-vworld-api | GitHub 아카이브 커밋 `a1fea840…` | 해당 커밋 |
| ruff / mypy / pytest | 설정 없음 / 설정 없음 / `pytest>=8.1.1`, `pytest-asyncio>=0.23.5` | 미확인 |
| dagster | 미사용 | — |

## 11. 미확인·열린 질문

1. Python 런타임 실제 설치 버전(lockfile 부재)과 fastapi/sqlalchemy 등 현재 prod 컨테이너의 정확한 버전 — `pip freeze` 산출물이 저장소에 없다.
2. `frontend/Dockerfile`이 `npm run dev`를 실행하는데 prod(n150)에서도 같은 이미지·명령을 쓰는지(docker-manager 소관, `docs/deploy-runbook.local.md` 미열람).
3. ruff/mypy 규칙(select, line-length, strict)이 어디에도 없어 journal의 "Ruff 통과"가 어떤 설정으로 실행됐는지 알 수 없다.
4. `@hookform/resolvers 3.10.0`과 `zod 4.4.3` 조합의 호환 여부(코드 상 동작 중으로 보이나 별도 검증 안 함).
5. `ADR-29`가 도입한 44px 터치 규칙·uppercase 라벨이 2026-08 리디자인(`design.md`)에서 뒤집혔는데 ADR로 기록되지 않았다(ADR-34 이후 디자인 관련 ADR 없음) — 정본 충돌 여부.
6. `CLAUDE.md` 레이아웃/ADR 인덱스가 구식(ADR-36~45 누락, `backend/app/` 경로)인 이유와 갱신 계획.
7. 백엔드 HTTP rate limit 부재가 의도인지(외부 read 키 노출 시 방어선은 CIDR/키 폐기뿐).
8. `docs/provider-policy.md` 결정 대기 항목(ADR-15 재검토, features export 필드 경계 C-6)이 common의 POI/feature 공급 규약 설계에 어떤 제약을 주는지.
9. `.claude/agents`·`.codex/agents` 페르소나 6종이 실제 워크플로에서 쓰이는지(범용 템플릿 텍스트, 저장소 특화 내용 없음).
10. 백업/복원 절차의 소재(저장소에 없음; docker-manager 또는 로컬 런북 추정).
11. `tests/e2e/ktc.spec.ts`가 요구하는 `KTC_TEST_PG_DSN` 등 E2E 인프라가 CI 없이 어디서 정기 실행되는지(n150 수동 실행으로 추정).
12. 선행 보고서(`kor-travel-common-library-review.md` §2)가 concierge를 "작은 UI 부품 후보, map 전체 구현과 동일하다고 볼 근거 없음"으로 평가했는데, 본 조사에서는 button/card/input/tabs/field/AppShell이 map recipe를 명시적으로 이식한 것으로 확인됐다(주석 "최신 기준 레포"). 다만 map의 `button-variants.ts` 분리·Hallmark 헤더·`data-table` 등은 없으므로 "동일 구현"은 아니고 "같은 계보의 부분집합"이 정확하다.

## 12. 근거 파일 목록

조사에서 실제로 읽은(전체 또는 지정 절) 파일:

1. `LICENSE`
2. `README.md`
3. `AGENTS.md`
4. `CLAUDE.md` (1~30, 144~200, 243~288행 + 헤딩)
5. `SKILL.md`
6. `design.md`
7. `CHANGELOG.md`
8. `.env.example` (키 목록·절 헤더)
9. `.gitignore`, `.gitattributes`, `.dockerignore`
10. `alembic.ini`
11. `docker-compose.yml`
12. `Dockerfile.python`
13. `deploy/Caddyfile`
14. `ktcctl`, `scripts/ktcctl`
15. `scripts/start-live.sh`, `scripts/stop-fixed-ports.sh`, `scripts/verify-docker-compose.sh`, `scripts/verify_rustfs.py`, `scripts/init_rustfs_buckets.py`, `scripts/backfill-place-admin-codes.py` (헤더)
16. `claude.json`, `codex.json`, `opencode.json`, `antigravity.json`, `.codex/config.toml`
17. `.claude/agents/frontend-developer.md`, `.claude/agents/ui-designer.md` (헤더)
18. `frontend/package.json`, `frontend/package-lock.json` (버전 추출)
19. `frontend/components.json`
20. `frontend/tailwind.config.ts`
21. `frontend/postcss.config.mjs`
22. `frontend/next.config.mjs`
23. `frontend/eslint.config.mjs`
24. `frontend/tsconfig.json`
25. `frontend/vitest.config.ts`
26. `frontend/Dockerfile`, `frontend/.dockerignore`
27. `frontend/tokens.css`
28. `frontend/src/app/globals.css`
29. `frontend/docs/DESIGN-RULES.md`
30. `frontend/src/app/layout.tsx`, `app/page.tsx`, `app/review/page.tsx`, `app/login/page.tsx`, `app/error.tsx`
31. `frontend/src/proxy.ts`
32. `frontend/src/app/api/v1/[...path]/route.ts`
33. `frontend/src/app/api/auth/login/route.ts`
34. `frontend/src/lib/auth.ts` (1~70행 + export 목록), `frontend/src/lib/auth-audit.ts` (헤더)
35. `frontend/src/lib/api.ts` (1~80, 500~600행 + export 목록)
36. `frontend/src/lib/use-is-mobile.ts`, `frontend/src/lib/utils.ts`
37. `frontend/src/components/AppShell.tsx` (1~100행)
38. `frontend/src/components/ui/button.tsx`, `input.tsx`, `switch.tsx` (전체/주요 절), 나머지 `components/ui/*` 헤더
39. `frontend/src/components/panels.tsx`, `detail.tsx`, `StatStrip.tsx`, `SectionCard.tsx` (export), `HelpTip.tsx`, `ConfirmActionButton.tsx`, `VWorldMap.tsx` (헤더/타일 URL)
40. `backend/requirements.txt`, `etl/requirements.txt`, `mcp/requirements.txt`, `scheduler/requirements.txt`
41. `backend/pytest.ini`
42. `backend/main.py`
43. `backend/ktc/api/__init__.py`, `backend/ktc/api/routes.py` (1~60행, 라우터 정의, 경로 목록)
44. `backend/ktc/core/config.py` (1~92행 + grep), `core/security.py` (1~90행 + 정의 목록), `core/database.py`, `core/logging.py`, `core/spatial.py`
45. `backend/ktc/telemetry.py` (메트릭 정의), `backend/ktc/cli.py`
46. `backend/ktc/services/list_pagination.py`
47. `backend/ktc/models/base.py`
48. `backend/ktc/etl/admin_region_service.py`, `geocoding.py` (헤더), `geocode_service.py`/`place_search.py`/`gemini_client.py` (URL grep)
49. `backend/ktc/mcp_server/server.py`, `tools.py` (등록 grep), `mcp/server.py`, `scheduler/worker.py`, `etl/runner.py` (헤더)
50. `backend/alembic/env.py` (1~40행), `backend/alembic/versions/` 파일명 목록
51. `backend/tests/conftest.py`
52. `tests/package.json`, `tests/package-lock.json`, `tests/playwright.config.ts`, `tests/scripts/start-backend.mjs`, `tests/e2e/ktc.spec.ts`·`live-shell.spec.ts` (헤더)
53. `docs/provider-policy.md` (헤딩, §0~1, §3~5, §7)
54. `docs/list-api-contract.md`
55. `docs/themes-api.md`
56. `docs/feature-export-api.md` (헤딩, 1~40행)
57. `docs/architecture.md` (헤딩, §7~8)
58. `docs/decisions.md` (ADR 목록, ADR-24/27/28/29/32/33/34/36/37 본문, 이력 절)
59. `docs/tasks.md` (1~40행, ID 통계), `docs/journal.md` (1~25행, ruff/적대적 리뷰 grep)
60. `docs/dev-environment.md` (헤딩, §4), `docs/pr-review-2026-06.md` (§3), 기타 docs 헤딩
61. 외부 대조: `F:/dev/kor-travel-geo-fixes/docs/kor-travel-common-library-review.md` (§2, §3.3, §7.3, concierge 언급), `F:/dev/kor-travel-common-survey/ktm-main/packages/kor-travel-map-admin/frontend/package.json`·`src/components/ui/` 목록·`button.tsx` 헤더, `F:/dev/kor-travel-common-survey/ktdm-main/docs/ports.md`·`config/docker-targets.yml` (conc 행)
