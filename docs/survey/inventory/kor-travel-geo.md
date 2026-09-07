# kor-travel-geo 인벤토리

- 기준 커밋: `1d9d74d3a852bbaaa09144b75bb69b99a58a6002` (2026-09-05 15:02 +0900, "docs: kor-travel-common 공통 라이브러리 도입 검토 보고서 (#546)")
- 조사일: 2026-09-06
- 조사 경로: `F:/dev/kor-travel-geo-fixes` (읽기 전용, 파일 수정·생성 없음)
- 라이선스: GPL-3.0-only — `LICENSE` 첫 줄 `GNU GENERAL PUBLIC LICENSE` / 둘째 줄 `Version 3, 29 June 2007`. `pyproject.toml` `license = { text = "GPL-3.0-only" }`, `kor-travel-geo-dagster/pyproject.toml` 동일. UI 패키지(`kor-travel-geo-ui/package.json`)에는 `license` 필드가 없다(사실).
- 표기 규약: **사실** = 파일에서 직접 확인, **후보** = 공통화 가능성 판단, **추정** = 정황 근거, **미확인** = 이번 조사에서 확인하지 못함.
- 선행 보고서 `docs/kor-travel-common-library-review.md`(2026-09-05, PR #546)는 기준 커밋 `daf079b5`를 근거로 한다. `git merge-base --is-ancestor daf079b5 HEAD`가 참이며, `daf079b5..HEAD` 사이 변경 파일은 `docs/journal.md`, `docs/kor-travel-common-library-review.md`, `docs/resume.md` 3개뿐이다(사실). 따라서 §12의 코드 링크 [G1]/[G3]/[G4]/[G6]는 HEAD와 바이트 동일하다. 표본 검증 결과는 §9 끝에 둔다.

## 1. 저장소 개요와 역할

1. `kor-travel-geo`(Python 패키지 `kortravelgeo`, CLI `ktgctl`, env prefix `KTG_*`, DB `kor_travel_geo`)는 행정안전부 주소기반산업지원서비스 원천을 PostgreSQL + PostGIS에 적재해 제공하는 한국 주소 지오코딩·리버스 지오코딩 라이브러리이자 FastAPI REST API다 (`README.md` 1~14행, `AGENTS.md` "목표"·"식별자").
2. REST 표면은 둘이다. `v1`(`/v1/address/*`)은 vworld.kr API와 100% 호환을 목표로 하고 자체 확장은 `x_extension` 키에만 둔다. `v2`(`/v2/*`)는 자체 후보 목록(candidate) 스키마다 (`AGENTS.md` "목표", ADR-038, `docs/api-reference/README.md`).
3. 사용자는 외부 개발자(공개 REST v1/v2, Python `AsyncAddressClient`)와 내부 운영자(admin UI·CLI)로 나뉜다. `kor-travel-geo-ui`는 "사용자 대상 서비스 UI가 아니라 내부 운영 도구"로 명시된다 (`README.md` 12행, `docs/architecture/frontend-package.md` A1.1).
4. 이전 SpatiaLite/SQLite 구현은 `v1` 브랜치에 보존되고 `main`은 PostGIS 재구현이다(ADR-001, `AGENTS.md` "역할").
5. 형제 프로젝트 연동: PostgreSQL/RustFS/Prometheus/Grafana는 `kor-travel-docker-manager`가 띄우는 공용 인프라에 접속만 한다(ADR-045, ADR-048, `docs/ports.md`). 포트 대역 `1250x`(API 12501, Dagster 12502, UI 12505, geo 전용 PostgreSQL 12500)를 manager가 source of truth로 정한다.
6. 백업/복원·적재 오케스트레이션은 형제 `kor-travel-map`의 독립 Dagster 청사진을 1:1 이식한 `kor-travel-geo-dagster`가 담당한다(ADR-066, `docs/architecture/dagster-boundary.md`).
7. 지도 기능은 형제 공유 라이브러리 `digitie/maplibre-vworld-react`를 GitHub tarball SHA로 소비하고, geo 특화 UX만 `components/vworld/CoordinateMap.tsx` domain wrapper에 둔다(ADR-028/032/063).
8. admin UI의 look and feel은 2026-08-31 T-302/T-303에서 최신 `kor-travel-map` admin Workbench 기준으로 동기화됐고(색 토큰은 geo blue 유지), 이 반복 동기화 비용이 선행 보고서의 공통화 동기다(`docs/journal.md` 86~153행, `docs/resume.md` 29~44행).
9. 여러 AI 에이전트(Claude Code / ChatGPT Codex / Antigravity / opencode)가 고정 worktree에서 병행 작업하는 운영 방식 자체가 검증 대상이며, 관련 규약이 `AGENTS.md`·`SKILL.md`·`docs/runbooks/`에 상세하다(ADR-034/041/065).

## 2. 저장소 구조

최상위(사실, `ls -la` 기준):

```
.agents/  .claude/  .codex/  .opencode/  .hallmark/  .github/workflows/
AGENTS.md  CLAUDE.md  SKILL.md  README.md  CHANGELOG.md  design.md  LICENSE
pyproject.toml  alembic.ini  alembic/  sql/  src/kortravelgeo/  tests/  scripts/
docker/api.Dockerfile  openapi.json  .pre-commit-config.yaml  .mcp.json
.env.example  .env.dev.example  .env.prod.example  .gitattributes  .gitignore
antigravity.json  claude.json  opencode.json
kor-travel-geo-ui/        # Next.js admin/debug UI (npm 단일 패키지)
kor-travel-geo-dagster/   # Dagster code location (별도 Python distribution)
docs/                     # adr/ architecture/ api-reference/ deploy/ runbooks/ + t0NN 리포트 다수
```

모노레포 workspace 도구는 없다. Python 2개 distribution + npm 1개 패키지가 한 git 저장소에 나란히 있다(사실: 루트에 `package.json`·workspace 설정 없음, `uv.lock`/`poetry.lock`/`requirements*.txt` 없음).

| 디렉터리 | 역할 | 근거 |
|---|---|---|
| `src/kortravelgeo/{dto,core,infra,loaders,client.py,api,cli}` | 계층형 백엔드. 의존 방향 `dto → core → infra → client → api/cli` (import-linter 강제) | `pyproject.toml [tool.importlinter]`, `docs/architecture/architecture.md` 34~48행 |
| `src/kortravelgeo/api/routers/` | `admin.py dagster.py dataset.py geocode.py healthz.py pobox.py reverse.py search.py v2.py zipcode.py` | `ls` |
| `alembic/versions/` | `0001`~`0026` 마이그레이션 26개 (`NNNN_<task>_<slug>.py`) | `ls alembic/versions` |
| `sql/` | `ddl/001_schema.sql`, `indexes.sql`, `mv.sql`, `postload.sql` | `ls sql` |
| `tests/unit`(141 파일) / `tests/integration`(34 파일) / `tests/fixtures` | pytest | `find` 카운트 |
| `scripts/` | `export_openapi.py`, `frontend_check.sh`, `docker_app.sh`, `deploy_app.py`, `agent_env.sh`, benchmark/run_tNNN 스크립트 30여 개 | `ls scripts` |
| `kor-travel-geo-ui/` | `app/ components/{ui,admin,auth,debug,layout,metrics,vworld} lib/ types/ tests/{unit,e2e} docs/ scripts/` | `find kor-travel-geo-ui -maxdepth 2` |
| `kor-travel-geo-dagster/` | `src/kortravelgeo_dagster/*.py`(12), `tests/`(10), `docker/{dagster.Dockerfile,dagster.yaml}`, `pyproject.toml` | `find` |
| `docs/adr/` | ADR-001~067 (040/042/046 삭제, README 색인) | `ls docs/adr` |
| `docs/architecture/` | `architecture.md backend-package.md(1694행) frontend-package.md(362행) data-model.md dagster-boundary.md external-apis.md address-db-schema.md` | `ls` |
| `docs/api-reference/` | `v1/ v2/ library/ operators/ llm-summary.md` | `find` |
| `docs/runbooks/` | `agent-workflow.md agent-failure-patterns.md restore-drill-runbook.md README.md` | `ls` |
| `docs/deploy/` | `docker-compose.geo-source-vol.yml`, `staging-full-load.md` | `ls` |

## 3. 프론트엔드

### 3.1 kor-travel-geo-ui (`kor-travel-geo-ui/`)

**프레임워크/런타임** (사실, `package.json`·`package-lock.json` lockfileVersion 3)

| 항목 | 선언 | lockfile 설치 |
|---|---|---|
| next | `^16.2.12` | 16.2.12 |
| react / react-dom | `^18.3.1` | 18.3.1 |
| typescript | `^5.9.3` | 5.9.3 |
| @types/react | `^18.3.27` | 18.3.31 |
| node engines | `package.json`에 `engines` 없음. Dockerfile `node:22-alpine`, CI `node-version: "20"`, ADR-019 "Node 20.9 이상" | — |
| packageManager 필드 | 없음. lockfile은 npm(`package-lock.json`) | — |

`"type": "module"`, scripts: `dev`=`next dev`, `build`, `start`, `lint`=`eslint .`, `type-check`=`tsc --noEmit`, `test`=`vitest run`, `test:e2e`=`playwright test`, `gen:types`=`node scripts/gen-types.mjs`. 포트는 스크립트에 박지 않고 `npm run dev -- --port 12505`로 넘긴다(`README.md`, ADR-048). Dockerfile은 `ENV PORT=12505`.

**React 18 유지 이유(문서 근거)**: ADR-019(2026-05-23) "React는 Next.js 16.2.6의 peer 범위가 허용하는 React 18.3.1을 유지한다 … Next.js 16.2.6은 npm registry 기준 React 18과 React 19를 모두 peer로 허용한다". ADR-020 49행: React 18 소비자와 upstream zod v4 peer를 맞추려 `zod ^4.4.3`을 직접 의존성으로 둔다. `components/ui/button.tsx` 7~8행 주석: "React 18에서는 radix Trigger asChild가 ref를 넘기므로 forwardRef가 필수". React 19로 올리지 않는 적극적 차단 사유(예: 라이브러리 비호환)를 명시한 문서는 찾지 못했다(미확인 → §11).

**스타일**

- tailwindcss `^4.0.0` 선언 / 4.3.1 설치, `@tailwindcss/postcss` `^4.0.0` / 4.3.1, postcss 8.5.15. `postcss.config.mjs`는 `@tailwindcss/postcss` 플러그인만(사실).
- 설정 방식은 **혼합(mixed)**이다(사실). `app/globals.css` 7~10행 `@import "tailwindcss" source(none);` + `@source "../app"`, `"../components"`, `"../lib"`(자동 소스 탐지 끔 — CHANGELOG/test-results 프로즈의 `shadow-[var(--…)]`가 스캔되어 파싱이 죽는 문제 회피 주석). 15~76행 `@theme inline { --color-* , --text-2xs…2xl(+--line-height), --spacing-control, --radius-*, --font-sans/heading }`. **78행 `@config "../tailwind.config.ts";`** 로 v3식 `tailwind.config.ts`(`theme.extend.colors` 43개: `background/foreground/card/popover/primary/secondary/accent/destructive/border/input/ring/text.*/surface.*/ink/muted/line/panel/brand/brand-tint/info/success/warn/danger`)를 여전히 불러온다. `tailwind.config.ts`의 `content: [...]`는 v4에서 무시되고 `@source`가 대신한다(추정: v4 동작 규칙; 파일에는 둘 다 존재). `kor-travel-geo-ui/CHANGELOG.md` Unreleased: "Tailwind CSS를 v3 → v4로 전환했다 … `@config "../tailwind.config.ts"`(기존 테마 설정 보존)". `components.json`의 `tailwind.config`도 `tailwind.config.ts`를 가리킨다.
- 토큰 파일: `app/globals.css`(3,750행) 단일. `:root`(91~177행)에 OKLCH 원색 `--color-paper*/--color-ink*/--color-muted*/--color-rule*/--color-accent/--color-brand-ink/--color-info/warning/danger/success(+-surface)/--color-code*/--color-overlay`, 폰트 `--font-display`("Pretendard Variable" 우선), `--font-body`("Noto Sans KR" 우선), `--font-mono`("IBM Plex Mono"), 간격 `--space-3xs…2xl`(0.25~4.5rem, 4px 기반), 의미 토큰 `--surface-page/card/subtle/muted/row`, `--text-strong/primary/secondary/tertiary/disabled`, 단축 별칭 `--bg/--panel/--surface/--ink/--muted/--line/--brand/--brand-ink/--info/--warn/--danger/--ok`, 그림자 `--shadow-card/-hover/-button/-modal`, 반경 `--radius-control 0.375rem`/`--radius-panel 0.5rem`, 컨트롤 높이 `--control-h 2.25rem`/`--control-h-sm 1.875rem`, 포커스 `--focus`, 모션 `--duration-fast 100ms/normal 150ms/long 420ms`, `--ease-default/in/in-out`, z-index `--z-base 1/raised 10/dropdown 100/sticky 200/modal 400/toast 500`. 2418~2460행 `@layer base`에서 shadcn 호환 `--ui-*`와 `--background/--primary/...` 별칭을 다시 매핑한다(3중 별칭 계층: OKLCH 원색 → 의미 토큰 → `--ui-*`/shadcn 짧은 이름).
- 라이트/다크: **라이트 전용**(사실). `prefers-color-scheme`, `.dark`, `[data-theme]` 블록 없음(`grep` 0건; "dark" 문자열 1건은 주석).
- 폰트: `@font-face`·`next/font`·Google Fonts 로딩 없음(사실). 시스템 설치 폰트 fallback stack에 의존(추정).
- 아이콘: lucide-react `^0.468.0` / 0.468.0.
- 애니메이션: `tw-animate-css`·`tailwindcss-animate` 미설치(사실). `globals.css` 2365~2395행 자체 `@keyframes ui-fade-in/ui-scale-in` + `.ui-overlay[data-state=open]`. 2398~2416행 `prefers-reduced-motion: reduce`에서 animation 0.01ms·transition 0s(visibility 전환 버그 회피 주석).
- Hallmark 흔적: `globals.css` 1~2행 `/* Hallmark · pre-emit critique … macrostructure: Workbench · theme: custom blue · nav: N3 side rail … genre: modern-minimal */`, `.hallmark/log.json`(2026-08-13, brief "kor-travel-geo 내부 운영 콘솔 전체 개편"), `.hallmark/preflight.json`.

**UI 프리미티브**

- `radix-ui` 통합 패키지 `^1.4.3` 선언 / 1.6.0 설치, lockfile에 `@radix-ui/*` 하위 121개(사실). `@base-ui/react`·`@base-ui-components/react` 미설치. `shadcn` CLI는 devDependency에 없음(수동 설치 추정).
- `components.json`(사실): `style: "radix-nova"`, `rsc: true`, `tsx: true`, `tailwind: {config: "tailwind.config.ts", css: "app/globals.css", baseColor: "neutral", cssVariables: true, prefix: ""}`, `iconLibrary: "lucide"`, `rtl: false`, aliases `components=@/components, utils=@/lib/utils, ui=@/components/ui, lib=@/lib, hooks=@/hooks`(`hooks/` 디렉터리는 존재하지 않음 — 사실), `menuColor: "default"`, `menuAccent: "subtle"`, `registries: {}`.
- `lib/utils.ts`는 표준 `cn = twMerge(clsx(...))`. cva `^0.7.1`, tailwind-merge `^3.6.0`, clsx `^2.1.1`.

**컴포넌트 인벤토리** (`components/ui/*` 전체 26개, 사실)

| 파일 | 행 | 기반 | 헤더/출처 메모 |
|---|---|---|---|
| `alert-dialog.tsx` | 160 | radix `AlertDialog` | shadcn 형식(세미콜론 없음) |
| `alert.tsx` | 68 | cva | shadcn |
| `badge.tsx` / `badge-variants.ts` | 21 / 23 | cva `tone: neutral/brand/ok/warn/error/info` | `color-mix()` 기반 tint |
| `button.tsx` / `button-variants.ts` | 33 / 41 | radix `Slot.Root` + `forwardRef` | 7~8행 React 18 forwardRef 주석. variants `default/outline/secondary/ghost/destructive/destructive-solid/link`, sizes `default/sm/xs/lg/icon/icon-sm/icon-xs/icon-lg`, 높이 `h-control`/`h-control-sm` |
| `card.tsx` | 110 | div | `size: default/sm`, `CardTitle role="heading" aria-level=2` |
| `checkbox.tsx` | 36 | radix `Checkbox` | |
| `collapsible.tsx` | 28 | radix `Collapsible` | |
| `dialog.tsx` | 142 | radix `Dialog` | |
| `field.tsx` | 224 | cva | shadcn Field |
| `input.tsx` | 31 | native | `size: default(36px)/sm(30px)` "map workbench의 두 컨트롤 높이" 주석 |
| `label.tsx` | 24 | radix `Label` | |
| `native-select.tsx` | 51 | native `<select>` | "Radix Select는 의도적으로 미사용: 단위 테스트가 `fireEvent.change`로 구동" 주석 |
| `popover.tsx` | 46 | radix `Popover` | |
| `progress.tsx` | 32 | radix `Progress` | |
| `separator.tsx` | 28 | radix `Separator` | |
| `skeleton.tsx` | 16 | div | |
| `tabs.tsx` | 69 | radix `Tabs` | |
| `toaster.tsx` | 62 | radix `Toast` + zustand `useToastStore` | |
| `tooltip.tsx` | 55 | radix `Tooltip` | |
| `JsonBlock.tsx` | 56 | 자체 | "pre.json-box는 e2e CSS 셀렉터 계약" + 복사 버튼(clipboard 없으면 전체 선택 폴백) |
| `PageHeader.tsx` | 59 | 자체 | `usePathname` + `ADMIN_NAV_GROUPS` 소비 |
| `Panel.tsx` | 49 | 자체 | "`<section className="panel">` + `.panel-header h2` 구조는 e2e 계약", `data-ui="panel"` |
| `StatusBadge.tsx` | 23 | `Badge` 래퍼 | 6px dot + text, `severityClass` 매핑(`lib/consistency.ts` 의존) |
| `VirtualTable.tsx` | 409 | TanStack Table + Virtual | 아래 계약 참조 |

앱 레벨 공유 컴포넌트(사실): `components/layout/AppShell.tsx`(347행, rail/drawer/collapsed rail, `DRAWER_MEDIA_QUERY = "(max-width: 1023px)"`, localStorage `kor-travel-geo:sidebar-collapsed`), `AppErrorPanel.tsx`(87, `lib/error-recovery.ts` 연동), `DocumentNavLink.tsx`(58, `prefetch={false}` + document navigation), `components/auth/LoginForm.tsx`(96, 자체 폼, shadcn 미사용), `components/admin/shared/`: `ActionResultPanel EmptyState HelpTip(Popover) IssueList(Alert) JsonDetails KeyValueGrid MetricTile(Skeleton) NumberField(Field+Input) RefreshButton TypedConfirmField WizardSteps YyyymmField AdminTabs(Tabs) ConfirmActionDialog(AlertDialog+RoleRequirementNote)`, `components/admin/RoleRequirementNote.tsx`(T-226, 백엔드 `security.py` 역할명 미러), `components/admin/PerfValidationSummary.tsx`, `components/vworld/{CoordinateMap,LazyCoordinateMap,map-utils}`, `components/metrics/WebVitalsReporter.tsx`. 출처 표기: 파일 헤더에 "map에서 이식" 같은 명시적 출처 주석은 없고, `input.tsx`·`admin-pages.ts`·`globals.css` 주석에 "최신 map Workbench 기준" 언급만 있다(사실). 선행 보고서가 말한 Pinvi식 "이식했다" 헤더는 geo에 없다.

**VirtualTable 계약**(사실, `components/ui/VirtualTable.tsx` 20~96행): `export type VirtualColumn<T> = { key; header; headerCell?; cell(row); sortValue?(row); align?; cellClassName?; rowHeader?; width? }`. props `rows, columns, rowKey(row)=>string, getSearchText?, searchPlaceholder="검색", emptyHint="결과가 없습니다.", initialSortKey/Dir, caption?, getRowClassName?, onRowClick?, toolbarExtras?, wrapCells, as: "table"|"grid" (기본 `"grid"`), compact, hideHeader, height=360, rowHeight=44`. 정렬·검색은 **클라이언트**(`getSortedRowModel`/`getFilteredRowModel`, `sortDescFirst:false`, `sortUndefined:"last"`). `as="grid"`는 `useVirtualizer` + ARIA grid, `as="table"`은 semantic `<table>`(caption, `<th scope>`, 가상화 없음). 파일 상단에 `react-hooks/incompatible-library` eslint disable(TanStack 훅 오탐). 테스트 `tests/unit/virtual-table.test.tsx`, `virtual-table-scroll.test.tsx`. 서버 페이지네이션/`manualSorting` 개념은 없다 — map/Pinvi `DataTable`(TanStack `ColumnDef` + `manualSorting`)과 계약이 다르다는 선행 보고서 §3.4 주장은 현재 커밋에서도 유효하다.

**상태/데이터**

- `@tanstack/react-query` `^5.90.10`/5.101.0. `app/providers.tsx`에 `QueryClient(staleTime 60s, refetchOnWindowFocus false, retry: ApiError<500이면 0, 그 외 2회)`. 문서 `frontend-package.md` A3.5는 `lib/queryClient.ts`를 말하지만 그 파일은 없다(사실 — 문서 drift).
- zustand `^5.0.14`/5.0.14: `lib/toast.ts`, `lib/stores/{consistency-analysis-store,regions-within-radius-store}.ts`.
- react-hook-form `^7.77.0`/7.79.0 + `@hookform/resolvers` 5.4.0 + zod `^4.4.3`/4.4.3. `lib/schemas.ts`는 pydantic v2 수동 mirror(한국 좌표 범위 123~132/32~39 등), `lib/schemas.gen.ts`는 생성된 schema 이름 목록.
- API 클라이언트 생성: `openapi-typescript` `^7.10.1`/7.13.0, `scripts/gen-types.mjs`가 루트 `openapi.json` → `types/api.gen.ts` + `lib/schemas.gen.ts`. `scripts/check-sync.sh`가 `git diff --exit-code`로 drift 검사. eslint ignore에 두 생성물 포함.
- fetch 래퍼 `lib/api.ts`(628행): `API_BASE = NEXT_PUBLIC_API_BASE_URL ?? "/api/proxy"`, `backendPath()`가 `/v1`·`/v2` 아닌 경로에 `/v1` 접두, `requestJson/postJson/patchJson/deleteJson`, `class ApiError {status; body; detail}`, `getErrorMessage()`가 `detail ?? error ?? message` 우선. 401이면 `/login?next=` 로 `window.location.assign`. 공개 API key는 메모리 변수 `activePublicApiKey`에만 보관(XSS 회피 주석).

**인증 경계**(사실)

| 층 | 파일 | 내용 |
|---|---|---|
| 사전 렌더 게이트 | `proxy.ts`(Next 16 `proxy` 규약, Node 런타임) | `PUBLIC_PATHS = {/login, /api/metrics}`, prefix `/api/auth/`, `/_next/`, `/favicon.ico`. 세션 없으면 `/api/*`는 401 `{error:"AUTH_REQUIRED"}`(no-store), 그 외 `/login?next=` 리다이렉트. 유효 세션이면 `x-ktg-pathname` 헤더 주입 |
| 세션 검증 | `lib/auth.ts`(672행) | 쿠키 `ktg_ui_session`, TTL 8h, HMAC 서명 payload `{aud:"kor-travel-geo-ui", exp, fp(UA fingerprint), iat, sid(32B), sub, v:1}`, PBKDF2-SHA256 310,000회 password hash, secret ≥32자, 로그인 실패 5회/10분. revocation map·실패 카운터는 `globalThis.__ktgRevokedSessionIds/__ktgLoginFailures`(이슈 #513 주석: 번들러가 레이어별로 모듈을 따로 emit하므로 globalThis 고정). 프로세스 재시작 시 소실 |
| 방어 심층 | `lib/session-guard.ts` + `app/admin/layout.tsx` | `requireSession()`이 서버 컴포넌트에서 재검증. 주석: "layout `redirect()`는 권한 경계로 충분치 않다(RSC 스트림·client nav 스킵)" |
| 로그인/로그아웃 | `app/api/auth/{login,logout}/route.ts` | same-origin 검사(`requestHasSameOrigin`, `KTG_UI_PUBLIC_ORIGINS`로 TLS 종단 보정), durable rate limit(`checkDurableLoginRateLimit` — 백엔드 `ops.audit_events` 조회) 우선, 실패 시 process-local. 감사 이벤트를 `POST /v1/admin/auth-events`로 백엔드 저장(`lib/auth-audit.ts`) |
| 백엔드 신원 전달 | `lib/proxy.ts` + `app/api/proxy/[...path]/route.ts` | 브라우저 헤더는 `accept/content-type/user-agent`만 통과. 서버가 `X-KTG-Actor`(admin username), `X-KTG-Roles`(`KNOWN_ADMIN_ROLES` 전체), `X-KTG-Admin-Proxy-Secret`(`KTG_ADMIN_PROXY_SECRET`) 주입. 대상은 `/v1/*`·`/v2/*`만(그 외 403). 응답 헤더는 `content-type/cache-control/retry-after/content-disposition`만 relay. 클라이언트 abort는 499 |
| 역할 | `lib/roles.ts` | `source_file_viewer/source_file_manager/rebuild_operator/destructive_admin` + 한국어 라벨. 백엔드 `api/security.py` ROLE_* 미러(표시용) |
| CSRF | 쿠키 `SameSite=Strict` + origin 검사 | 별도 CSRF 토큰 없음(사실) |

ADR-013(2026-05-22, "내부망 전용, 앱 인증 없음")은 ADR-064(2026-06-23)로 대체됐다: 단일 admin 세션 로그인, UI proxy shared secret, 백엔드 `require_role` 전역 게이트, 공개 API key(`ops.public_api_keys`, SHA-256 hash). `kor-travel-geo-ui/SKILL.md` 6행은 아직 "애플리케이션 인증은 두지 않는다"라고 적혀 있다(사실 — 문서 drift). 2026-09-04 journal: docker-manager와 로그인 일치화 요청은 "백엔드는 세션을 직접 검증하지 않고 UI가 trusted proxy로 헤더 주입"(ADR-049 #5) 구조와 충돌해 사용자가 취소했다.

**라우팅/화면 목록**(사실, `find app -type f`)

- admin 13 라우트: `/admin`(홈), `/admin/source-files`, `/admin/files`, `/admin/consistency`, `/admin/consistency/[report_id]`, `/admin/backups`, `/admin/dagster`, `/admin/ops`, `/admin/logs`, `/admin/tables`, `/admin/cache`, `/admin/settings`, `/admin/load`(레거시 스텁, 네비 비노출). 네비 IA는 `lib/admin-pages.ts` `ADMIN_NAV_GROUPS`: 데이터 관리 / 수집 파이프라인 / 모니터링 / 시스템 (주석: "최신 map admin의 작업 중심 IA를 geo 도메인에 맞춰 적용").
- debug 4: `/debug/geocode`, `/debug/reverse`, `/debug/normalize`, `/debug/explain`.
- 기타: `/`, `/login`, `error.tsx`, `global-error.tsx`.
- route handlers 6: `/api/auth/login`, `/api/auth/logout`, `/api/metrics`, `/api/metrics/web-vitals`, `/api/proxy/[...path]`, `/api/runtime-config`.
- 사용자(일반 소비자) 화면: 0.

**반응형/모바일**(사실)

- 브레이크포인트: `globals.css` `@media (max-width: 1023px)`(2263, 2911, 3368행 — 사이드바 → drawer), `(min-width: 1024px)`(3314), `(min-width: 768px)`(3579), `(min-width: 640px) and (max-width: 1023px)`(3714, 태블릿 상태 strip 3열), `(hover: hover) and (pointer: fine)`(2565/2780/2886/3736 — hover 효과를 포인터 기기로 한정). Tailwind 기본 `sm/md/lg` 유틸도 병용(추정).
- 모바일 전용 처리: `AppShell` off-canvas drawer(`inert`, `aria-modal`, body scroll lock, `useModalA11y`로 포커스 트랩/복귀), 좁은 화면 320/375px 오버플로 이슈 #514 수정 주석(`Panel.tsx`). 터치 밀도: `docs/DESIGN-RULES.md` 5번 "standalone 컨트롤 36px/30px, nav·checkbox hit area 최소 44px".
- PC/Mobile 분기: CSS 미디어 쿼리 + `window.matchMedia(DRAWER_MEDIA_QUERY)` 훅. 별도 모바일 앱·UA 분기 없음.

**i18n / 접근성 / focus / reduced-motion**(사실)

- i18n 라이브러리 없음(`next-intl`/`i18next` 미검출). `app/layout.tsx` `<html lang="ko">`, 모든 UI 문구 한국어 하드코딩. `metadata.title.template = "%s · Geocoder Admin UI"`.
- 접근성: `lib/use-modal-a11y.ts`(T-227: 포커스 진입·Tab 트랩·Escape·복귀), Panel `h2` 접근명 규칙, CardTitle heading role, VirtualTable ARIA grid/semantic table 이중 모드, StatusBadge dot+text(T-299 색각 구분성), e2e `*-a11y.spec.ts` 4개(backups/consistency/ops/source-files).
- focus 레시피: `button-variants.ts` `focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-focus`, `@layer base * { outline-color: color-mix(var(--ui-ring) 50%) }`, T-300 opaque focus ring(journal 2026-08-31).
- reduced-motion: 위 스타일 절 참조(전역 0s 규칙).

**테스트·품질**(사실)

| 도구 | 파일 | 규칙 |
|---|---|---|
| eslint `^9.39.4` + `eslint-config-next` 16.2.12 | `eslint.config.mjs` | flat config, `core-web-vitals`만. off: `import/no-anonymous-default-export`, `react-hooks/set-state-in-effect`. ignores `.next, node_modules, types/api.gen.ts, lib/schemas.gen.ts` |
| tsconfig | `tsconfig.json` | `strict: true`, `target ES2022`, `moduleResolution bundler`, `paths @/* + vworld-map-core/web → node_modules/maplibre-vworld-react/packages/*/src` |
| vitest `^4.1.8`/4.1.9 | `vitest.config.ts` | jsdom, globals, `tests/unit/**/*.{test,spec}.{ts,tsx}`, `tests/setup.ts`(jest-dom, localStorage shim, createObjectURL shim). 43 파일(journal: 204~210 tests) |
| @testing-library/react 16.3.2, jsdom 25 | | |
| playwright `^1.57.0`/1.61.0 | `playwright.config.ts` | baseURL `http://127.0.0.1:12505`, projects chromium+firefox, `PLAYWRIGHT_MOCK_LOGIN=1`이면 `tests/e2e/mock-auth-setup.ts` globalSetup + storageState. `tests/e2e/*.spec.ts` 23개 + `tests/e2e/live/*.spec.ts` 17개(운영 대상 read-only) |
| React Doctor | `README.md`, `SKILL.md`, `AGENTS.md` 체크리스트 | `npx react-doctor@latest . --offline --verbose --json` 모든 프론트 작업 후 필수 |
| 게이트 스크립트 | `scripts/frontend_check.sh` | Windows npm이면 즉시 실패, Linux에서 `gen:types → lint → type-check → test → build` |

**빌드/배포**(사실)

- `next.config.mjs`: `reactStrictMode: true`, `allowedDevOrigins`(env `KTG_UI_ALLOWED_DEV_ORIGINS`), `turbopack.resolveAlias`(vworld-map-core/web → source), `transpilePackages: ["maplibre-vworld-react"]`, webpack alias fallback(주석: turbopack 키 없으면 Next 16 build hard-fail). `output` 미지정(standalone 아님), `images` 미지정.
- `Dockerfile`: `node:22-alpine` 3-stage(deps `npm ci` → builder `npm run build` → runner `npm run start`), `PORT=12505`, `.next`+`node_modules` 전체 복사.
- 실행: 루트 `scripts/docker_app.sh`(host 네트워크 기본, `KTG_ENV_FILE` 순서로 env 주입), `scripts/deploy_app.py`(n150 amd64 / odroid arm64 노드, `--remote-env-file`).

**디자인 문서**(사실)

- 루트 `design.md`(54행): 장르 "editorial-utilitarian", 구조 Workbench(좌측 레일 + header band + 작업 캔버스), 풋터 없음(레일 로그아웃만), 색은 `globals.css` OKLCH 토큰만·"최신 map admin의 녹색 팔레트를 복사하지 않는다", 서체 Pretendard/Noto Sans KR/IBM Plex Mono + `tabular-nums`, 4px 간격 토큰, 카드 중첩 금지, 모션은 `transform/opacity`만, 공통 시각 계약 중심은 `Panel, Card, PageHeader, DocumentNavLink`.
- `kor-travel-geo-ui/docs/DESIGN-RULES.md`(73행): StyleSeed(`styleseed-demo.vercel.app/llms.txt`) 해석본. 단일 accent, 5단계 텍스트 토큰, 8px 카드 반경(16px 미적용), 4%/12% 그림자 상한, 36/30px 컨트롤·44px hit area, label 13.5px/table header 12px, dot+text 상태, KPI 36px, 모션 토큰, 금지 목록(순수 `#000`, 브랜드색 큰 면, 카드 중첩, 임의 dropdown 필터, 강한/유색 shadow, viewport 비례 폰트).
- `kor-travel-geo-ui/docs/ARCHITECTURE.md`, `TASKS.md`(T-021~026 체크리스트, 갱신 정체).
- 색 톤 이력: T-298 teal→blue(2026-08-27, PR #540) → T-301 사용자 레퍼런스 blue(`#2563EB/#1D4ED8/#DBEAFE` OKLCH 역변환, hue 262.9/chroma 0.215) (`docs/resume.md` 45~62행). `.hallmark/log.json`의 "chromatic-teal"은 이전 톤 기록.

## 4. 백엔드

### 4.1 kortravelgeo (`src/kortravelgeo/`, 루트 `pyproject.toml`)

- python `>=3.12`, 빌드 setuptools(`setuptools>=75`, namespace discovery `namespaces = true`, ADR-015 implicit namespace `kortravel`). **lockfile 없음**(사실: `uv.lock`/`poetry.lock`/`requirements*.txt` 부재). SKILL.md 빠른 시작은 `uv venv && uv pip install -e ".[api,dev]"`, CI는 `pip install -e ".[api,loaders,dev]"` — 설치 버전은 매 실행 최신 해석(사실).
- 의존 선언 범위(사실):

| 그룹 | 패키지 |
|---|---|
| 기본 | `pydantic>=2.9,<3` `pydantic-settings>=2.5` `sqlalchemy[asyncio]>=2.0.35` `geoalchemy2>=0.15` `psycopg[binary,pool]>=3.2` `anyio>=4.5` `typer>=0.12` `httpx>=0.27` `tenacity>=9.0` `rapidfuzz>=3.10` `structlog>=24.4` `orjson>=3.10` `alembic>=1.13` |
| `api` | `fastapi>=0.115` `uvicorn[standard]>=0.32` `prometheus-client>=0.21` `maxminddb>=2.6,<3` |
| `loaders` | `gdal>=3.8`(시스템 GDAL과 동일 버전 핀, ADR-008) `geopandas>=1.0` `shapely>=2.0` `fiona>=1.10` `pyogrio>=0.10` |
| `dev` | `pytest>=8.3` `pytest-asyncio>=0.24` `pytest-postgresql>=6.1` `testcontainers[postgres]>=4.8` `ruff>=0.7` `mypy>=1.13` `import-linter>=2.0` `hypothesis>=6.115` `pre-commit>=4.0` |

  `asyncpg` 없음(psycopg 3 async). `structlog`는 선언돼 있으나 `src/` 내 `import structlog` 0건(사실). `testcontainers`/`pytest_postgresql`/`hypothesis`도 `tests/` 내 사용 0건(사실) — 선언만 남은 의존성.

- 앱 구성(사실, `api/app.py`): `create_app()` → `FastAPI(title=settings.api_title, version=__version__("0.1.0"), default_response_class=ORJSONResponse, lifespan, docs_url="/v1/docs", openapi_url="/v1/openapi.json")`. 라우터 prefix: `/v1`(healthz, geocode, reverse, search, zipcode, pobox, dagster), `/v1/admin`(admin — `APIRouter(dependencies=[Depends(require_role(*KNOWN_ADMIN_ROLES))])`), `/v2`(v2), `/v2/dataset`(dataset). `/metrics`는 `include_in_schema=False`. `/debug`·`/ops` prefix는 없고 `/v1/ops/dagster/*`는 dagster 라우터 안에 있다.
- 미들웨어(사실): `install_geoip_gate`(`@app.middleware("http")`, ADR-037 한국 IP만, `KTG_GEOIP_GATE_MODE strict|permissive|off`), `_install_admission_control`(429 `RateLimitError E0200`, `Retry-After: 1`), `_install_performance_monitoring`(`@app.middleware("http")`, slow request 로깅·Prometheus), `ClientDisconnectCancellationMiddleware`(`/v1/address/`·`/v2/` 경로 499). **CORS 미들웨어 없음** — `Settings.api_cors_origins`와 `.env.prod.example` `KTG_API_CORS_ORIGINS`는 선언만 있고 `CORSMiddleware` import 0건(사실). lifespan은 Dagster reconciler, table stats/pg_stat 캡처, runtime warm, slow observability, source janitor 백그라운드 태스크 7개.
- 에러 envelope(사실, `api/responses.py` `error_payload`): 경로별 3종 — v1 vworld 경로는 VWorld error object, `/v2/*`는 `{status:"ERROR", query_id, error:{code, message, hint?, field?}}`(`V2ErrorEnvelope`), 그 외 legacy `{response:{status:"ERROR", errorCode, errorMessage, hint?}}`(`LegacyErrorEnvelope`). 핸들러: `KorTravelGeoError`(base, ADR-014), `StarletteHTTPException`, SQLAlchemy `TimeoutError`/`DBAPIError`, `RequestValidationError`/`ValidationError` → 400(ADR-061, FastAPI 422 제거를 `_install_openapi_customization`이 OpenAPI에도 반영). `hint`는 입력값 미노출 sanitized 요약(8항목/600자 상한).
- 페이지네이션(사실, `docs/api-reference/v2/conventions.md` §3): endpoint마다 다르다 — geocode `limit`(≤100, total 없음), reverse 페이징 없음(`radius_m`), search `page/size`(≤100)+`total`(`Page` 상속), regions 그룹 배열. admin은 `limit`/`since` query(`GET /v1/admin/loads`), `ConsistencySamplePage{total}`. 공통 페이지 DTO 하나로 통일돼 있지 않다.
- 인증(사실, `api/security.py`): 헤더 `x-ktg-actor`, `x-ktg-roles`, `x-ktg-admin-proxy-secret`(hmac 비교). peer가 `KTG_ADMIN_TRUSTED_PROXY_CIDRS`(없으면 `geoip_trusted_proxies`) 안일 때만 신뢰. 역할 `source_file_viewer / source_file_manager / rebuild_operator / destructive_admin / scheduler`(+ 헤더 불가 `system`). `require_role(*roles)` 의존성. 공개 API key(`api/public_api_key.py`): query `key` 또는 header `X-KTG-API-Key`, DB `ops.public_api_keys` SHA-256 hash, trusted proxy identity면 우회. 세션·ServiceToken·argon2 없음(pbkdf2는 UI 쪽).
- rate limit(사실): admission control(동시성 상한 `KTG_API_MAX_CONCURRENCY`·scope별, timeout 429), 로그인 실패 제한은 UI+audit 기반. 토큰 버킷식 per-key 제한은 없음(미확인: `admin_repo` 내부 제한 유무).
- OpenAPI(사실): `scripts/export_openapi.py`(`create_app().openapi()` → `json.dumps(sort_keys, indent 2)` → 루트 `openapi.json`, `--check`로 drift). `.github/workflows/openapi.yml`이 PR/push마다 검사. `openapi.json`: OpenAPI 3.1.0, title `kor-travel-geo`, version 0.1.0, paths 108(`/v1/admin` 91, `/v1/address` 5, `/v1/ops` 4, `/v2/*` 6, healthz/readyz), schemas 218, tags `address pobox search zipcode admin health ops dagster v2-dataset v2`. operationId는 FastAPI 기본(`geocode_v1_address_geocode_get` 식)이며 커스텀 규약 없음. UI `gen:types`가 이 파일을 소비하고 CI가 생성물 커밋 여부를 검사.
- 설정(사실, `settings.py`): `SettingsConfigDict(env_prefix="KTG_", env_file=".env", extra="ignore", frozen=True)`, `SecretStr` 키. `.env.example` 키군: `KTG_PG_*`(DSN 기본 `postgresql+psycopg://<user>:<password>@127.0.0.1:12500/kor_travel_geo`, pool, statement_timeout, search_path `public,x_extension`), `KTG_API_*`(title, CORS, radius, concurrency, admission), `KTG_GEOIP_*`, `KTG_ADMIN_TRUSTED_PROXY_CIDRS`/`KTG_ADMIN_PROXY_SECRET`/`KTG_UI_PUBLIC_ORIGINS`, 외부 키 `KTG_JUSO_API_KEY`/`KTG_JUSO_COORD_API_KEY`/`KTG_VWORLD_API_KEY`/`KTG_EPOST_API_KEY` + URL, `KTG_CACHE_*`, `KTG_LOG_LEVEL`/`KTG_LOG_FORMAT=json`, `KTG_LOADER_*`, `KTG_UPLOAD_SET_*`, `KTG_OPS_TABLE_STATS_*`, `KTG_DAGSTER_*`, `KTG_RUSTFS_*`, `KTG_BACKUP_*`. `.env.dev.example`/`.env.prod.example`이 dev/prod 프로파일(docker `--env-file` 호환 형식 규칙 주석).
- 관측성(사실): 로깅은 stdlib `logging`(`_LOGGER`, `kortravelgeo.api.performance` 로거). `log_format: Literal["json","console"]` 설정은 있으나 JSON 포매터 배선 위치는 미확인. 메트릭 접두 **`ktg_`**(T-305, 2026-09-04: `kor_travel_geo_` → `ktg_`; API 43~44개 `infra/metrics.py`, UI 5개 `lib/metrics.ts` `ktg_ui_http_requests_total` 등). health `GET /v1/healthz`(`{"status":"ok"}`), ready `GET /v1/readyz`(`ReadinessResponse{status, ready, degraded, components{database,pool,admission}}`, pool 포화 503). Web Vitals는 UI `/api/metrics/web-vitals`.
- DB(사실): PostgreSQL + PostGIS, 확장은 `x_extension` 스키마(ADR-018), 운영 메타데이터 `ops` 스키마(ADR-033: `audit_events`, `public_api_keys`, `table_stats_snapshots`, `pg_stat_statements_snapshots`…), staging 스키마 `KTG_LOADER_TEMP_SCHEMA`. alembic `alembic/versions/0001~0026`, `alembic.ini` `sqlalchemy.url`에 dev DSN 하드코딩. 엔진 `infra/engine.py` `create_async_engine(pool_pre_ping, pool_recycle, connect_args options=-c statement_timeout/-c search_path, prepare_threshold)`, raw SQL repository(ADR-004), MV `mv_geocode_target` swap(ADR-017/036 `ALTER DATABASE RENAME` hot-swap).
- 백업/복원(사실): 병렬 directory dump + tar.zst(ADR-030), RustFS(S3 호환) 아카이브(`infra/rustfs.py`, boto3는 dagster 쪽 선언), restore drill(`docs/runbooks/restore-drill-runbook.md`), hot-swap. CLI `ktgctl` typer 구조: 루트 명령 `init-db`, `seed-consistency-registry`; 하위 앱 `load(juso, daily-juso, parcel-links, daily-parcel-links, roadaddr-entrances, locsum, navi, shp, shp-all, sppn-makarea, pobox, bulk, epost, all-sidos)`, `refresh mv`, `validate(consistency, data-quality-samples)`, `jobs(list,status,cancel)`, `backup(create,list,show,delete,copy,verify,reconcile-source,janitor,restore-drill)`, `restore create`, `serving hot-swap-plan`, `geoip check`, `janitor run`.
- 테스트(사실): `pytest` `asyncio_mode=auto`, `testpaths=["tests"]`, marker `longrun`. unit 141 파일(journal 2026-09-04: 1,395 passed), integration 34 파일은 `KTG_TEST_PG_DSN` 외부 DB 지정 시 opt-in, `tests/integration/_pg_guard.py`가 보호 DB 이름을 세그먼트 매칭으로 거부(issue #523/#525). coverage gate 없음(`pyproject`·CI에 `cov` 0건). ruff `line-length=100`, `target py312`, select `E F W I N UP B A C4 SIM TCH RUF ASYNC`, per-file-ignores 다수(api/cli/client/core/dto/infra/loaders의 TC00x). mypy `strict=true`, `pydantic.mypy` 플러그인, 대상 `src/kortravelgeo scripts/export_openapi.py`. import-linter layers 계약 `api > cli > client > loaders > infra > core > dto`, 예외 1건 `api.routers.admin -> loaders`. pre-commit: ruff v0.7.4(`--fix`), mypy v1.13.0, local import-linter.

### 4.2 kortravelgeo-dagster (`kor-travel-geo-dagster/`)

- python `>=3.12`, setuptools, 일반 패키지(`namespaces=false`, ADR-066 §6), lockfile 없음. 의존 `kor-travel-geo==0.1.0`(main lib 단방향 소비), `dagster>=1.9,<2`, `dagster-webserver>=1.9,<2`, `dagster-postgres>=0.25,<1`, `boto3/botocore>=1.34,<2`, `httpx>=0.27,<1.0`. dev `pytest pytest-asyncio ruff mypy`. ruff/mypy 설정은 루트와 동일 select·strict, `[tool.dagster] module_name = "kortravelgeo_dagster.definitions"`.
- 정의(사실, `definitions.py`): `Definitions(jobs=[MV_REFRESH, BACKUP, DB_BACKUP, DB_RESTORE, FULL_LOAD, CONSISTENCY, SOURCE_REBUILD, BACKUP_MAINTENANCE], schedules=BACKUP_SCHEDULES+BACKUP_MAINTENANCE_SCHEDULES, sensors=BACKUP_SENSORS)`. `@op`/`@job` 기반이며 `@asset`은 0개(사실, grep). `@schedule` 3개(`backup.py`, `backup_maintenance.py` ×2 — 예: `backup_retention_janitor_daily` 06:00 KST STOPPED 기본), `@run_failure_sensor` 1개. resources `admin_api`(ADR-066 온램프, `scheduler` 역할로 `/v1/admin/backups/scheduled/run-due` 호출), `client`(`AsyncAddressClient`), `rustfs`, `settings`(`KTG_*`), `failure_notifier=None`. 3-way fallback(value → real resource → missing-guard RuntimeError).
- 배포: `docker/dagster.Dockerfile`(python:3.12-slim 2-stage, GDAL+`[loaders]`, postgresql-client-16+zstd, `USER appuser`, port 12502, webserver CMD / daemon은 compose `command:`), `docker/dagster.yaml`(`storage.postgres.postgres_url env KTG_DAGSTER_PG_URL`, telemetry off). API는 webserver GraphQL만 조회(`api/_dagster_client.py`, SSRF allowlist `KTG_DAGSTER_ALLOWED_HOSTS`). admin `/admin/dagster`는 `KTG_DAGSTER_PUBLIC_URL`을 iframe 임베드.
- 테스트: `tests/test_*.py` 10개(definitions/backup/execute 계열).

## 5. 문서·에이전트 규약

**진입 파일**(사실)

| 파일 | 행 | 역할 |
|---|---|---|
| `AGENTS.md` | 225 | 목표, Think Before Coding/Simplicity/Surgical/Goal-Driven/Practical Bias 원칙, 문서 언어 정책(한국어), 식별자 표, Linux-only 개발 환경(ADR-065), 에이전트 worktree/CodeGraph, 지시 우선순위 7단계, DO NOT 11개, 제공자 API 원칙, 작업 후 체크리스트, **push 전 보안 감사 절차 6단계**, 검증 명령 |
| `CLAUDE.md` | 116 | Claude 세션 컨텍스트(정본 위임표, 프로젝트 현황 2026-06-18, 포트, 빠른 검증, CodeGraph, 핵심 ADR 발췌, 환경 복구). main 저장소 경로를 `F:/dev/python-kraddr-geo`로 적어 옛 이름 잔존 |
| `SKILL.md` | 145 | 에이전트 매뉴얼: 정체성·식별자, 개발 환경, 빠른 시작, 디렉터리 지도, DO NOT 17개(구 ADR-002/008/014/015 이관), 자주 묻는 작업, 도메인 어휘, 체크리스트 |
| `design.md` | 54 | UI 디자인 시스템(§3 참조) |
| `README.md` | 203 | 입구: 상태, 제공 표면, 문서 지도, 환경 요약, 라이브러리 예제, 검증, 법적 고지 |
| `kor-travel-geo-ui/{README,SKILL}.md` | 200+/21 | UI 패키지 진입(SKILL은 ADR-064 이전 문장 잔존) |

지시 우선순위(`AGENTS.md`): 사용자 요청 > AGENTS.md > SKILL.md > architecture/adr/data-model/backend·frontend-package/agent-guide/external-apis > README·나머지 docs > 기존 코드·테스트 > 최소·되돌릴 수 있는 가정. 언어 정책: 모든 Markdown/RST 한국어, 공식 필드명·코드 식별자·명령어·URL·제공자 원문만 영어.

**docs/ 트리와 규약**(사실)

| 문서 | 규약 |
|---|---|
| `docs/tasks.md`(90) / `tasks-done.md`(1074) / `tasks-rule.md`(78) | 열린 `[ ]`만 tasks.md, 완료는 tasks-done newest-first. ID `T-NNN`, 하위 `T-NNNa`, 한정자 `T-219 M4`, 종료 `T-NNN 종료(no-go)`. 번호대: T-1xx 성능/기능/geocoder, T-2xx Admin UI+적재/백업(ADR-050). 마커 `[ ]/[x]/[~]`, `✅`/취소선 |
| `docs/resume.md`(1051) | 진척 정본 + "다음 한 작업". 세션 시작 시 tasks.md와 함께 필독 |
| `docs/journal.md`(6403) | 역시간순 작업 일지, 엔트리 `## YYYY-MM-DD (T-NNN — 제목, by <agent>)` |
| `docs/adr/`(README 색인 119행) | `NNN-<slug>.md`, 상태 `proposed/accepted/superseded by`, 결정자 `agent|human`. 핵심 구조 결정만 ADR; 순수 개발 규칙은 SKILL §4로 이관(stub 유지), 완전 중복은 삭제 표기. 다음 후보 ADR-068. `docs/decisions.md`는 9행 stub |
| `docs/agent-guide.md`(417) | 첫 진입 프로토콜, 결정·기록 5종(decisions/resume/journal/tasks/CHANGELOG), ADR·journal·resume 형식, 변경 분류별 체크리스트, PR 워크플로(ADR-021), branch `agent/<agent>-<task>`·`agent/<agent>-idle`, Squash and merge 권장, PR 리뷰 세 표면(conversation/review body/inline thread) 확인 프로토콜, fixup PR 재리뷰 금지 |
| `docs/runbooks/` | `agent-workflow.md`(1-PR 흐름·4 게이트·미러·Playwright), `agent-failure-patterns.md`, `restore-drill-runbook.md` |
| `docs/architecture/`, `docs/api-reference/` | 정본 사양·API 문서(v1/v2/library/operators + `llm-summary.md`) |
| `docs/t0NN-*.md`, `postmerge-review-fixups-*.md` | task 리포트·사후 리뷰 기록(archive 성격, 별도 archive 디렉터리 없음) |
| `docs/ai-tooling.md`, `codegraph-worktree.md`, `dev-environment.md`, `ports.md`, `windows-reinstall-recovery.md`, `dev-environment-recovery.md` | 환경 |

**개발 환경/리뷰 정책**(사실)

- 정본 환경: **Linux-only(WSL 포함)**(ADR-065; ADR-034→041→065 변천). Git source of truth는 Linux `git`이 읽는 `/mnt/f/dev/kor-travel-geo-*` worktree, 설치·테스트·장기 실행은 WSL ext4 미러(`rsync --delete`, `data -> /mnt/f/dev/geodata` 심볼릭 링크), `source scripts/agent_env.sh`. Windows PowerShell은 표준 개발 경로가 아님. Playwright는 n150 Linux 우선, Windows fallback 시 사유 기록.
- worktree: 에이전트별 고정(`kor-travel-geo-{codex,claude,antigravity}`, `.codex/`·`.opencode/`도 존재), idle branch `agent/<agent>-idle`. CodeGraph: worktree마다 `codegraph init -i` 1회, 이후 `codegraph sync && codegraph status`; MCP `.mcp.json`(codegraph, filesystem), `.codex/config.toml`(codegraph/playwright/sequential-thinking/filesystem), `antigravity.json`, `opencode.json`. 서브에이전트 `.claude/agents/*.md`(api-designer/backend-developer/frontend-developer/mobile-developer/ui-designer), `.codex/agents/*.toml`(+ui-fixer), `.opencode/agent/*.md`. 스킬 `.agents/skills/`(postgres 계열 8종 정본) → `.claude/skills/`, `.opencode/skill/`.
- 리뷰 정책: "두 독립 적대적 리뷰"는 `docs/journal.md`·`resume.md`·`tasks-done.md`·`v2-cleanslate-optional-data-accuracy.md`에 실행 기록으로만 나타나고, `AGENTS.md`/`SKILL.md`/`agent-guide.md`/`runbooks/`/`tasks-rule.md`에는 규칙으로 성문화돼 있지 않다(사실, grep 0건). 성문 규칙은 "CI green 후 즉시 머지 금지, Squash and merge, fixup PR 재리뷰 금지, branch protection(ruff/mypy/lint-imports/pytest/OpenAPI drift/frontend)".
- 보안 감사: `AGENTS.md` "Remote push 전 보안 감사 절차": staged diff 육안 확인, secret/hash/DSN/IP grep, 로컬 비밀 파일 미추적 확인, `git add -A` 금지, 인증·세션·키 변경 시 `/security-review` 스킬. 구체 패턴은 gitignored `docs/deploy-runbook.local.md`·`docs/prod-access.local.md`(`.gitignore` `*.local.md`, 워크트리별 수동 복사).
- 커밋 규약: Conventional Commits 형식 `docs: …`(HEAD 커밋 제목) 관찰. 명시 규칙 문서는 미확인.

## 6. CI·배포·운영

- `.github/workflows/ci.yml`(사실): job `backend`(ubuntu, Python 3.12, apt `gdal-bin libgdal-dev`, `pip install gdal==$(gdal-config --version)` + `.[api,loaders,dev]`, `ruff check . / mypy src/kortravelgeo scripts/export_openapi.py / lint-imports / pytest -q`), job `frontend`(Node 20, `npm ci`, `npm run gen:types`, `git diff --exit-code -- types/api.gen.ts lib/schemas.gen.ts`, lint/type-check/test/build). Playwright는 CI에 없음.
- `.github/workflows/openapi.yml`: `pip install -e ".[api]"` 후 `python scripts/export_openapi.py --check --output openapi.json`.
- pre-commit: ruff/mypy/import-linter(§4.1).
- Docker: `docker/api.Dockerfile`(python:3.12-trixie, GDAL 버전 일치 검사, postgresql-client-16+zstd, port 12501), `kor-travel-geo-ui/Dockerfile`(node:22-alpine, 12505), `kor-travel-geo-dagster/docker/dagster.Dockerfile`(12502). compose 파일은 저장소에 없고 `docs/deploy/docker-compose.geo-source-vol.yml`은 docker-manager에 넣을 override 정본. dev 실행은 `scripts/docker_app.sh`(host 네트워크 기본, 점유 컨테이너 강제종료 확인), prod는 `kor-travel-docker-manager` + `.env.prod`(gitignored) 또는 노드 `/etc/kor-travel-geo/app.env`.
- 포트(`docs/ports.md`, ADR-048): geo PostgreSQL 12500(manager ADR-37 이후 전용 인스턴스), API 12501, Dagster 12502, UI 12505; RustFS 12101/12105; Grafana 12205, cAdvisor 12301, Prometheus 12401; concierge 12601/12602/12605, map 12701/12702/12705, pinvi 12801/12805, manager 12901/12905. Prometheus scrape: API `/metrics`, UI `/api/metrics`.
- prod(n150) 규약: `scripts/deploy_app.py` 노드 `n150=deploy@<internal-host>,linux/amd64`, `odroid=…,linux/arm64`; 공개 도메인은 추적 파일에 두지 않음(`.env.prod.example` placeholder만, `KTG_DAGSTER_PUBLIC_URL`은 공개값으로 커밋 가능 명시). 배포·검증 반복 실수는 gitignored `docs/deploy-runbook.local.md`.
- 시크릿: `SecretStr`, `.env*` gitignore(`.example`만 추적), PBKDF2 hash/HMAC secret은 UI `.env.local`, 공유 `KTG_ADMIN_PROXY_SECRET`은 API·UI 양쪽 env. `.gitattributes`로 `*.py *.toml *.md *.txt *.yml *.yaml *.sh` LF 고정.

## 7. 외부 연동 (cross-repo)

| 대상 | 방식 | 근거 |
|---|---|---|
| kor-travel-docker-manager | 공용 인프라(PostgreSQL/RustFS/Prometheus/Grafana) 접속만, 포트 정본, prod compose 소유. 코드 호출 없음(`src`·`ui` grep 0건; `lib/proxy.ts` 124행에 concierge #111 참조 주석만) | ADR-045/048, `docs/ports.md` |
| kor-travel-map | Dagster 청사진 이식(ADR-066), admin UI look&feel 동기화 원본(T-302/303), `@theme inline` 주석 "최신 kor-travel-map과 공유하는 7단계 type scale". 런타임 호출 없음 | `globals.css` 12행, `docs/journal.md` 131행 |
| concierge / pinvi / weather | 런타임 연동 없음(사실: grep 0건). 포트표에서만 참조 | `docs/ports.md` |
| ServiceToken | 해당 없음(사실: `ServiceToken`/`service_token` 0건). 서비스 간 신원은 `X-KTG-*` 헤더 + shared secret + trusted CIDR | `api/security.py` |
| `maplibre-vworld-react` | `package.json` `"maplibre-vworld-react": "https://github.com/digitie/maplibre-vworld-react/archive/95b49d3c9afc7bef3af508e025df09ba6fc90494.tar.gz"`(lock resolved 동일, version `0.0.0`). 로컬 `F:/dev/maplibre-vworld-react` HEAD가 정확히 `95b49d3`(2026-07-24 "fix(web): break reentrant jumpTo/fitBounds recursion …")이다(사실). 소비 경계는 `lib/vworld.ts`(심층 경로 `packages/vworld-map-web/src/*` 재수출, barrel 회피 이유 주석). alias를 tsconfig/vitest/next.config 3곳에 유지. **문서 drift**: `README.md`·`docs/architecture/architecture.md`·ADR-063·`kor-travel-geo-ui/README.md`는 여전히 `a7cb0f8f…`를 "현재 고정 SHA"로 적고 있다(사실) | `package.json` 26행, `lib/vworld.ts` |
| `maplibre-vworld-js` | ADR-063으로 의존성 제거됨. `AGENTS.md`·`SKILL.md`에는 "적극 수정 대상"·"경계"로 아직 언급(문서 잔존) | ADR-063 |
| `python-*-api` 13종, `python-kraddr-base` | `pyproject.toml`·`src`에 의존·import 0건(사실). 외부 API(vworld/juso/epost)는 `httpx.AsyncClient`+`tenacity`로 `infra/external_api.py`에서 직접 호출 | `docs/architecture/external-apis.md` |
| vworld-map-* 벤더 tgz | 별도 tgz 벤더링 없음. GitHub archive tarball URL만 | `package.json` |
| Dagster(자체) | API → webserver GraphQL(12502) 관측, Dagster → API `admin_api` 리소스(온램프, `scheduler` 역할) | ADR-066, `resources.py` |

## 8. 공통화 후보

| # | 영역 | 근거 경로 | 신뢰도 | 비고 |
|---|---|---|---|---|
| 1 | 의미 토큰 계약(surface/text/brand/status/focus/radius/control 높이/motion/z-index 이름) | `kor-travel-geo-ui/app/globals.css` 91~177행, `@theme inline` 15~76행 | high | 이름은 map 어휘와 이미 정렬(주석). 값(blue)은 앱 소유. OKLCH 원색→의미→shadcn 별칭 3층 구조 중 의미층만 공유 후보 |
| 2 | 7단계 type scale + control 36/30px + radius 6/8px 규약 | `globals.css` `--text-2xs…2xl`, `--control-h*`, `docs/DESIGN-RULES.md` 5~6번 | high | T-303에서 map 스케일로 맞춘 값 |
| 3 | `Badge`/`StatusBadge`(tone + 6px dot + text) | `components/ui/badge-variants.ts`, `StatusBadge.tsx` | high | `severityClass` 의존은 앱에 남김 |
| 4 | `Button`(radix Slot/asChild/forwardRef) | `components/ui/button.tsx`, `button-variants.ts` | medium | React 18 forwardRef·Radix 엔진 차이가 map/Pinvi(Base UI/native)와 충돌 — 선행 보고서 §3.3 동일 |
| 5 | `Input`(size default/sm), `NativeSelect`, `Field`, `Label`, `Checkbox` | `components/ui/{input,native-select,field,label,checkbox}.tsx` | medium | native-select는 테스트 구동 방식 계약이 명시돼 있어 공통화 시 보존 필요 |
| 6 | `Panel`/`Card`/`PageHeader` 섹션 컨테이너 규약 | `components/ui/{Panel,card,PageHeader}.tsx`, `design.md` "일관성 규칙" | medium | `Panel`은 e2e 셀렉터 계약(`section.panel .panel-header h2`)을 가짐 |
| 7 | `EmptyState`, `MetricTile`, `KeyValueGrid`, `HelpTip`, `IssueList`, `RefreshButton`, `WizardSteps` | `components/admin/shared/*` | high | 도메인 무관 소형 부품 |
| 8 | `ConfirmActionDialog` + `TypedConfirmField` + `RoleRequirementNote` 패턴 | `components/admin/shared/ConfirmActionDialog.tsx`, `TypedConfirmField.tsx` | medium | 역할 라벨은 앱 주입 |
| 9 | `useModalA11y`(포커스 트랩·복귀·Escape) | `lib/use-modal-a11y.ts` | high | 드로어·다이얼로그 공용, 테스트 `app-shell-drawer.test.tsx` |
| 10 | AppShell 구조(rail/collapsed rail/drawer/`inert`/scroll lock, 1023px 분기) | `components/layout/AppShell.tsx`, `globals.css` 2911~/3368~ | medium | 메뉴·라우트·로그아웃은 앱 소유. Workbench 구조는 map과 이미 동형 |
| 11 | `JsonBlock`(복사 폴백), `JsonDetails` | `components/ui/JsonBlock.tsx`, `admin/shared/JsonDetails.tsx` | high | e2e 셀렉터 `pre.json-box` 계약 주의 |
| 12 | Toast 스토어 + Toaster(zustand, tone별 duration) | `lib/toast.ts`, `components/ui/toaster.tsx` | medium | radix Toast 의존 |
| 13 | `VirtualTable`(`VirtualColumn<T>` 선언형, grid/table 이중 모드) | `components/ui/VirtualTable.tsx` | low | map/Pinvi `DataTable`과 계약(서버 정렬 vs 클라이언트 정렬)이 달라 후속 단계 |
| 14 | reduced-motion 전역 규칙 + 자체 keyframes(`ui-fade-in/ui-scale-in`) | `globals.css` 2365~2416행 | high | 0s transition 근거 주석 포함 |
| 15 | `DESIGN-RULES.md`·`design.md` 규칙(금지 목록, 44px hit area, 8px radius, 그림자 상한) | `kor-travel-geo-ui/docs/DESIGN-RULES.md`, `design.md` | high | 규칙(문서) 산출물 후보. 색 톤은 제품별 |
| 16 | Tailwind v4 CSS-first 구성 규약(`source(none)` + 명시 `@source`, `@theme inline`, `@config` 브리지 제거 계획) | `globals.css` 3~10행, 78행, `postcss.config.mjs` | high | v4 전환 함정(프로즈 스캔 파싱 오류) 기록이 규칙 후보 |
| 17 | shadcn `components.json` 기준값(style, baseColor neutral, cssVariables, aliases) | `kor-travel-geo-ui/components.json` | medium | `radix-nova` style은 Base UI 앱과 다름 |
| 18 | OpenAPI export/drift 게이트 + openapi-typescript 생성물 커밋 검사 | `scripts/export_openapi.py`, `.github/workflows/openapi.yml`, `kor-travel-geo-ui/scripts/{gen-types.mjs,check-sync.sh}`, `ci.yml` frontend job | high | 규칙+도구 후보. 생성물은 `types/api.gen.ts`, `lib/schemas.gen.ts` |
| 19 | BFF 프록시 패턴(헤더 allowlist, `X-KTG-Actor/Roles/Admin-Proxy-Secret` 주입, 499 처리, 응답 헤더 필터) | `lib/proxy.ts`, `app/api/proxy/[...path]/route.ts` | medium | 헤더 접두(`X-KTG-`)는 앱 식별자. 구조만 공통 규칙 후보; 세션 저장은 통합 금지(journal 2026-09-04) |
| 20 | 세션 쿠키·PBKDF2·rate limit 파라미터(8h, 310k iter, 5회/10분, HMAC) | `lib/auth.ts` 4~26행 | low | docker-manager와 "거의 동일"(journal)하나 revocation 저장이 다름. 규칙 문서 후보만 |
| 21 | 에러 envelope 규약(v2 `{status, query_id, error{code,message,hint?,field?}}`, 400 통일, hint sanitize) | `api/responses.py`, ADR-060/061 | medium | v1 vworld 호환은 geo 고유. v2 envelope는 형제 서비스 규약 후보 |
| 22 | health/ready 규약(`/v1/healthz` `{status:"ok"}`, `/v1/readyz` `{status, ready, degraded, components}` + pool 포화 503) | `api/routers/healthz.py`, `dto/health.py` | high | |
| 23 | Prometheus 메트릭 명명(`<svc>_` 접두, route template label, `:id` 정규화, method allowlist, `/<unmatched>`) | `infra/metrics.py`, `lib/metrics.ts`, `frontend-package.md` A7 | high | T-305 접두 변경 경험 |
| 24 | pydantic-settings 규약(`env_prefix`, `SecretStr`, `frozen`, `.env.{dev,prod}.example` 프로파일, docker `--env-file` 호환 형식) | `settings.py` 32~38행, `.env.*.example` | high | |
| 25 | ruff/mypy/import-linter/pre-commit 기준선(select 세트, line-length 100, strict, layers 계약) | `pyproject.toml`, `.pre-commit-config.yaml`, dagster `pyproject.toml`(주석 "repo root와 동일") | high | 두 distribution이 이미 복제 중 |
| 26 | 통합 테스트 DB 보호 가드(`_pg_guard.py`, `KTG_TEST_PG_DSN`, 세그먼트 매칭, 거부 시 세션 실패) | `tests/integration/_pg_guard.py`, `conftest.py` | medium | 규칙+도구 후보 |
| 27 | Dagster code-location 규약(별도 distribution, 리소스 3-way fallback, `@op` 모듈 `from __future__ import annotations` 금지, STOPPED 기본 스케줄) | `kor-travel-geo-dagster/{pyproject.toml,definitions.py}`, `docs/architecture/dagster-boundary.md` | medium | map에서 이식된 청사진 |
| 28 | 문서·에이전트 규약(AGENTS/CLAUDE/SKILL 역할 분리, tasks/tasks-done/tasks-rule, ADR 형식·stub 정책, journal/resume 형식, push 전 보안 감사, `*.local.md`) | `AGENTS.md`, `docs/tasks-rule.md`, `docs/adr/README.md`, `docs/agent-guide.md` | high | 규칙 산출물 후보 |
| 29 | 포트 대역 규약(`12N0x`: 0=DB, 1=API, 2=worker/aux, 5=UI) | `docs/ports.md`, ADR-048 | high | manager가 정본 |
| 30 | 검증 게이트 스크립트 패턴(`frontend_check.sh` Windows npm 차단, `agent_env.sh`, React Doctor 필수) | `scripts/frontend_check.sh`, `scripts/agent_env.sh` | medium | |

## 9. 이 저장소 고유 차이·주의점

| 영역 | 내용 | 공통화 시 영향 |
|---|---|---|
| React 18 / radix-ui | React 18.3.1 + `radix-ui` 1.6.0(121 하위 패키지). map/Pinvi/concierge는 React 19 + Base UI(선행 보고서 §2). `Button`은 `forwardRef`+`Slot` 필수 | 공통 UI를 React 19/Base UI 기준으로 만들면 geo는 업그레이드 선행 필요. 지원 조합 실검증 없이는 채택 불가 |
| Tailwind 혼합 모드 | v4 CSS-first이지만 `@config "../tailwind.config.ts"`로 v3 `theme.extend.colors`를 계속 로드. `--ui-*`/shadcn 짧은 이름/의미 토큰 3층 별칭 | 사용자 전제(1) "v4 전환"은 이미 됐으나 `@config` 잔존 제거·토큰 계층 단순화가 별도 작업 |
| `source(none)` 명시 @source | CHANGELOG·test-results 프로즈 스캔이 v4 파서를 죽여 자동 탐지를 껐음 | 공통 패키지 배포 시 소비 앱에 `@source` 명시 등록이 필수(선행 보고서 §7.3 [E1]과 일치) |
| 라이트 전용 | 다크 모드 없음 | 토큰 계약이 다크를 요구하면 geo는 값 추가 필요 |
| 폰트 미번들 | Pretendard/Noto Sans KR/IBM Plex Mono를 시스템 폰트로만 참조 | 공통 폰트 로딩 정책(next/font 등) 결정 필요 |
| e2e 셀렉터 계약 | `section.panel .panel-header h2`, `pre.json-box`, `span.status` 등 DOM 계약이 컴포넌트 주석에 명시 | 공통 컴포넌트가 마크업을 바꾸면 geo e2e 40개 스펙 회귀 |
| VirtualTable 계약 | 클라이언트 정렬·검색, `VirtualColumn<T>`; 서버 페이지네이션 없음 | map/Pinvi `DataTable`과 통합 시 정렬 소유 명시 필요(선행 보고서 §3.4) |
| 인증 경계 | Next가 세션 검증, 백엔드는 trusted proxy 헤더만 신뢰(ADR-049 #5/064). revocation은 in-process `globalThis` | 로그인 폼 공통화는 가능하나 세션 저장·역할 판정 통합은 기존 ADR과 충돌(2026-09-04 취소 사례) |
| `maplibre-vworld-react` 소비 | GitHub tarball SHA + 심층 source 경로 + 3곳 alias + `transpilePackages`. npm 미공개 | 지도 부품은 공통 라이브러리 중복 금지 대상; 대신 npm 배포 전환이 선행 과제 |
| 문서 drift | 지도 SHA(`a7cb0f8` vs `95b49d3`), `lib/queryClient.ts` 부재, UI SKILL "인증 없음", `components.json` `hooks` alias, CLAUDE.md `python-kraddr-geo` 경로, `.claude/settings.json` statusLine, frontend-package.md A2 `docs/` 목록 | 공통 규칙 문서를 만들 때 geo 문서를 정본으로 복사하면 안 됨 |
| 선언만 남은 의존성 | `structlog`, `testcontainers`, `pytest-postgresql`, `hypothesis` 미사용; CORS 설정 미배선 | 백엔드 공통 기준선 정할 때 "선언 = 사용"으로 가정 금지 |
| lockfile 없음(Python) | uv/poetry lock 부재, CI가 매번 최신 해석 | 사용자 전제(2) 버전 일치화는 geo에 lock 도입이 선행 |
| Linux-only 개발 환경 | Windows PowerShell 비표준, WSL ext4 미러, n150 Playwright | common의 개발 환경 정본을 정할 때 geo와 다른 저장소(Windows 기반이면) 사이 조정 필요 |
| GPL-3.0-only | 코드·문서 모두 GPL | common 라이선스 결정 전 파일별 출처 확인(선행 보고서 §9) |
| 에러 envelope 3종 병존 | v1 vworld / v2 / legacy | 공통 규약은 v2 형태만 후보 |
| 메트릭 접두 `ktg_` | 2026-09-04 dual-emission 없이 즉시 전환 | 공통 명명 규칙 채택 시 접두는 서비스별 유지 |

**선행 보고서 §12 근거 표본 검증**(사실, HEAD 기준)

| 링크 | 검증 | 결과 |
|---|---|---|
| [G1] `kor-travel-geo-ui/package.json` | next `^16.2.12`, react `^18.3.1`, tailwindcss `^4.0.0`, `radix-ui ^1.4.3`, TanStack Table/Virtual 존재 | 유효(선언 범위 일치). lockfile 설치는 next 16.2.12 / react 18.3.1 / tailwindcss 4.3.1 / radix-ui 1.6.0 |
| [G3] `components/ui/button.tsx` | `Slot.Root`, `asChild`, `React.forwardRef`, React 18 주석 | 유효 |
| [G4] `components/ui/VirtualTable.tsx` | `VirtualColumn` 계약, 클라이언트 검색·정렬, 기본 `as="grid"`, `as="table"` 모드 | 유효 |
| [G6] `lib/auth.ts` | `globalThis.__ktgRevokedSessionIds` in-process revocation | 유효. 보강: 로그인 rate limit은 백엔드 audit 기반 durable 경로(`checkDurableLoginRateLimit`)가 우선이라 "프로세스 메모리 기반"은 revocation에만 해당 |
| [G7] `docs/journal.md` | 2026-09-04 엔트리(24~40행)에 로그인 일치화 취소 경위 | 유효 |
| [G2] `docs/resume.md` | T-302(38행)·T-303(29행) map 동기화 기록 | 유효 |
| [L1] `LICENSE` | GPL v3 문서 | 유효 |
| §2 표 "geo admin Tailwind `^4.0.0`" | 선언은 일치하나 `tailwind.config.ts`+`@config` 잔존(혼합 모드)은 보고서에 없음 | 보강 사항 |

## 10. 버전 표

| 항목 | 선언 범위 | lockfile 설치 버전 | 근거 |
|---|---|---|---|
| node | `engines` 없음; Dockerfile node:22-alpine; CI node 20; ADR-019 ≥20.9 | — | `Dockerfile`, `ci.yml` |
| npm | 미지정(`packageManager` 없음) | lockfileVersion 3 | `package-lock.json` |
| next | `^16.2.12` | 16.2.12 | `package.json` |
| react / react-dom | `^18.3.1` | 18.3.1 / 18.3.1 | |
| typescript | `^5.9.3` | 5.9.3 | |
| tailwindcss | `^4.0.0` | 4.3.1 | |
| @tailwindcss/postcss | `^4.0.0` | 4.3.1 | |
| postcss | `^8.5.15` | 8.5.15 | |
| radix-ui | `^1.4.3` | 1.6.0 (`@radix-ui/*` 121) | |
| @base-ui/react | 없음 | 미설치 | |
| shadcn(CLI) | 없음 | 미설치 (`components.json` style `radix-nova`) | |
| lucide-react | `^0.468.0` | 0.468.0 | |
| eslint / eslint-config-next | `^9.39.4` / `^16.2.12` | 9.39.4 / 16.2.12 | |
| vitest / @vitejs/plugin-react | `^4.1.8` / `^4.7.0` | 4.1.9 / 4.7.0 | |
| @playwright/test | `^1.57.0` | 1.61.0 | |
| @testing-library/react / jest-dom / jsdom | `^16.3.0` / `^6.9.1` / `^25.0.1` | 16.3.2 / — / 25.0.1 | |
| @tanstack/react-query | `^5.90.10` | 5.101.0 | |
| @tanstack/react-table / react-virtual | `^8.21.3` / `^3.14.3` | 8.21.3 / 3.14.3 | |
| zod | `^4.4.3` | 4.4.3 | |
| zustand | `^5.0.14` | 5.0.14 | |
| react-hook-form / @hookform/resolvers | `^7.77.0` / `^5.4.0` | 7.79.0 / 5.4.0 | |
| maplibre-gl | `^5.24.0` | 5.24.0 | |
| maplibre-vworld-react | GitHub archive `95b49d3c…` | 0.0.0 (tarball) | |
| openapi-typescript | `^7.10.1` | 7.13.0 | |
| class-variance-authority / tailwind-merge / clsx | `^0.7.1` / `^3.6.0` / `^2.1.1` | 0.7.1 / 3.6.0 / 2.1.1 | |
| tw-animate-css | 없음 | 미설치 | |
| python | `>=3.12` | lockfile 없음(CI/Docker 3.12) | `pyproject.toml`, `api.Dockerfile` |
| fastapi | `>=0.115` (api extra) | 미확인 | |
| uvicorn | `>=0.32` [standard] | 미확인 | |
| pydantic / pydantic-settings | `>=2.9,<3` / `>=2.5` | 미확인 | |
| sqlalchemy | `[asyncio]>=2.0.35` | 미확인 | |
| alembic | `>=1.13` | 미확인 (versions 0001~0026) | |
| asyncpg | 없음 | — | |
| psycopg | `[binary,pool]>=3.2` | 미확인 | |
| geoalchemy2 | `>=0.15` | 미확인 | |
| ruff | `>=0.7` (pre-commit v0.7.4; 로컬 캐시 0.15.12 관찰) | 미확인 | `.ruff_cache/0.15.12` |
| mypy | `>=1.13` (pre-commit v1.13.0) | 미확인 | |
| pytest / pytest-asyncio | `>=8.3` / `>=0.24` | 미확인 | |
| import-linter | `>=2.0` | 미확인 | |
| dagster / dagster-webserver / dagster-postgres | `>=1.9,<2` / `>=1.9,<2` / `>=0.25,<1` | 미확인 | dagster `pyproject.toml` |
| prometheus-client | `>=0.21` | 미확인 | |
| structlog | `>=24.4` (미사용) | 미확인 | |
| typer / httpx / tenacity | `>=0.12` / `>=0.27` / `>=9.0` | 미확인 | |
| gdal(python) | `>=3.8`, 시스템 `gdal-config --version` 핀 | 이미지별 | `api.Dockerfile` |
| PostgreSQL 서버 | 16 (client `postgresql-client-16`) | — | `api.Dockerfile` 주석 |

## 11. 미확인·열린 질문

1. React 19로 올리지 않는 적극적 사유(라이브러리 비호환·Radix 문제 등)를 기록한 문서를 찾지 못했다. ADR-019의 "peer 범위가 허용하는 18.3.1 유지"가 유일한 근거다. 사용자 전제(2) 버전 일치화 시 geo React 19 업그레이드 가능성은 실검증이 필요하다.
2. `tailwind.config.ts`의 `theme.extend.colors`(43개)와 `@theme inline`(`--color-*` 33개)이 겹치는 이름(`background/card/primary/...`)에서 어느 쪽이 유틸리티 클래스에 실효하는지는 빌드 출력으로 확인하지 않았다(미확인).
3. Python 설치 버전(fastapi/pydantic/sqlalchemy 등)은 lockfile이 없어 확정 불가. 운영 이미지의 실제 버전은 `pip freeze` 없이는 미확인.
4. `KTG_LOG_FORMAT=json`이 실제 JSON 포매터를 어디서 배선하는지(`structlog` 미사용) 미확인.
5. CORS 미들웨어가 없는데 `.env.prod.example`이 `KTG_API_CORS_ORIGINS`를 설정하는 이유(리버스 프록시에서 처리하는지) 미확인.
6. "두 독립 적대적 리뷰"가 규칙인지 관행인지 — 성문 규칙 파일이 없다. common 리뷰 정책을 세울 때 geo의 실제 절차(리뷰어 A/B 분담, 근거 파일)는 `docs/tasks-done.md`·journal에서 추가 추출이 필요하다.
7. `docs/deploy-runbook.local.md`·`docs/prod-access.local.md`(gitignored)의 내용은 조사 범위 밖이라 배포 체크리스트·시크릿 스캔 패턴의 정확한 내용은 미확인.
8. `maplibre-vworld-react` npm 배포 전환 계획의 현재 상태(ADR-063 "후속") 미확인 — 로컬 저장소 HEAD와 geo 핀이 같은 SHA라는 사실만 확인.
9. Pinvi/map 쪽 `DataTable`과 geo `VirtualTable`의 호출부 수(각 앱에서 몇 화면이 어떤 모드로 쓰는지)는 geo 쪽만 부분 확인(`TableStatsPanel`, 백업 artifact 목록 semantic table 등). 정확한 사용 매트릭스는 미확인.
10. `kor-travel-geo-ui/docs/TASKS.md`가 T-026 이후 갱신되지 않은 것으로 보이는데 의도적 stub인지 미확인.
11. 폰트: Pretendard/Noto Sans KR가 운영 n150 컨테이너/브라우저에서 실제로 어떻게 해석되는지(설치 여부) 미확인.

## 12. 근거 파일 목록

조사에서 실제로 열어 본 파일(저장소 상대 경로, 기준 커밋 `1d9d74d`):

1. `LICENSE` (첫 3행)
2. `README.md`
3. `AGENTS.md`
4. `CLAUDE.md`
5. `SKILL.md`
6. `design.md`
7. `CHANGELOG.md` (1~40행)
8. `pyproject.toml`
9. `alembic.ini`, `alembic/versions/` 목록
10. `.pre-commit-config.yaml`
11. `.github/workflows/ci.yml`
12. `.github/workflows/openapi.yml`
13. `.env.example`, `.env.dev.example`, `.env.prod.example`
14. `.gitignore`, `.gitattributes`, `.dockerignore`, `.mcp.json`, `.claude/settings.json`, `.codex/config.toml`, `.hallmark/log.json`
15. `docker/api.Dockerfile`
16. `docs/deploy/docker-compose.geo-source-vol.yml`
17. `scripts/export_openapi.py`, `scripts/frontend_check.sh`, `scripts/docker_app.sh`(1~40행), `scripts/deploy_app.py`(1~60행), `scripts/agent_env.sh`(1~40행)
18. `openapi.json` (구조 요약: paths/tags/schemas 카운트)
19. `src/kortravelgeo/api/app.py` (1~260행, 430~480행)
20. `src/kortravelgeo/api/responses.py` (1~200행)
21. `src/kortravelgeo/api/security.py` (1~140행 + 정의 grep)
22. `src/kortravelgeo/api/public_api_key.py` (1~50행)
23. `src/kortravelgeo/api/middleware/geoip_gate.py` (1~40행)
24. `src/kortravelgeo/api/routers/healthz.py` (1~80행)
25. `src/kortravelgeo/settings.py` (1~80행), `src/kortravelgeo/version.py`
26. `src/kortravelgeo/infra/metrics.py` (메트릭 이름 grep), `src/kortravelgeo/infra/engine.py` (1~60행)
27. `src/kortravelgeo/dto/common.py` (1~80행), `dto/admin.py`(grep)
28. `src/kortravelgeo/cli/main.py` (typer 구조 grep)
29. `tests/integration/conftest.py` (1~60행), `tests/integration/_pg_guard.py` (1~45행)
30. `kor-travel-geo-dagster/pyproject.toml`, `src/kortravelgeo_dagster/definitions.py`(1~80행), `resources.py`(234~262행), `docker/dagster.Dockerfile`, `docker/dagster.yaml`
31. `docs/kor-travel-common-library-review.md` (전문)
32. `docs/adr/README.md`, `013-internal-only-ui-no-app-auth.md`, `019-nextjs-16-security-floor.md`, `028-maplibre-vworld-domain-wrapper-boundary.md`, `034-…`, `041-…`, `048-…`, `061-…`, `063-…`, `064-…`, `065-…`, `066-…` (헤드)
33. `docs/architecture/architecture.md` (1~80행 + 헤딩), `docs/architecture/frontend-package.md` (전문), `docs/architecture/backend-package.md` (헤딩·페이지네이션 grep), `docs/architecture/dagster-boundary.md` (헤딩), `docs/architecture/external-apis.md` (1~40행)
34. `docs/api-reference/README.md`, `docs/api-reference/v2/conventions.md` (1~60행)
35. `docs/tasks-rule.md`, `docs/tasks.md`, `docs/resume.md` (1~70행 + grep), `docs/journal.md` (24~153행 + grep), `docs/decisions.md`
36. `docs/agent-guide.md` (헤딩, 290~330행, 364~395행), `docs/runbooks/README.md`, `docs/runbooks/agent-workflow.md` (헤딩·grep), `docs/ai-tooling.md`, `docs/codegraph-worktree.md` (1~40행), `docs/dev-environment.md` (1~60행), `docs/ports.md`
37. `kor-travel-geo-ui/package.json`, `package-lock.json` (버전 추출), `components.json`, `tailwind.config.ts`, `postcss.config.mjs`, `next.config.mjs`, `tsconfig.json`, `eslint.config.mjs`, `vitest.config.ts`, `playwright.config.ts`, `Dockerfile`, `.dockerignore`, `.gitignore`, `.env.local.example`
38. `kor-travel-geo-ui/README.md` (1~80행), `SKILL.md`, `CHANGELOG.md` (1~60행), `docs/DESIGN-RULES.md`, `docs/ARCHITECTURE.md`, `docs/TASKS.md`
39. `kor-travel-geo-ui/scripts/gen-types.mjs`, `scripts/check-sync.sh`
40. `kor-travel-geo-ui/app/globals.css` (1~200행, 2360~2475행, 구조 grep), `app/layout.tsx`, `app/providers.tsx`, `app/admin/layout.tsx`, `app/api/proxy/[...path]/route.ts`, `app/api/auth/login/route.ts`, `app/` 라우트 목록
41. `kor-travel-geo-ui/proxy.ts`, `lib/auth.ts` (1~140행), `lib/session-guard.ts`, `lib/session-headers.ts`, `lib/proxy.ts` (1~120행), `lib/roles.ts`, `lib/api.ts` (1~120행), `lib/utils.ts`, `lib/toast.ts`, `lib/schemas.ts` (1~40행), `lib/use-modal-a11y.ts` (1~40행), `lib/admin-pages.ts`, `lib/vworld.ts`, `lib/metrics.ts` (grep)
42. `kor-travel-geo-ui/components/ui/*` 26개 헤더 + `button.tsx`, `button-variants.ts`, `badge-variants.ts`, `Panel.tsx`, `StatusBadge.tsx`, `card.tsx`(1~40행), `VirtualTable.tsx`(1~140행 + export grep)
43. `kor-travel-geo-ui/components/admin/shared/*` 헤더, `EmptyState.tsx`, `ConfirmActionDialog.tsx`(1~40행), `components/admin/RoleRequirementNote.tsx`, `components/layout/AppShell.tsx`(grep + 60~70행), `components/auth/LoginForm.tsx`(헤더), `components/vworld/CoordinateMap.tsx`(1~60행)
44. `kor-travel-geo-ui/tests/setup.ts`, `tests/unit/`·`tests/e2e/` 목록
45. `F:/dev/maplibre-vworld-react` git HEAD/`git log -1 95b49d3` (SHA 대조용, 읽기 전용)
