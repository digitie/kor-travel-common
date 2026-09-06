# pinvi 인벤토리

- 기준 커밋: `9af25e58cf77b360188a69e26a36a0588063aa8b` (`git rev-parse HEAD`; shallow clone이라 `git log`는 1건 — `chore(m05): Map 스냅샷 핀을 5e484fb8로 옮긴다 (#534)`)
- 조사일: 2026-09-06
- 조사 경로: `F:/dev/kor-travel-common-survey/pinvi` (브랜치 `main`, `git status` 변경 없음 — 읽기 전용 확인)
- 라이선스: **루트 `LICENSE` 파일 없음** (사실, `ls LICENSE*` 실패). `README.md` "라이선스" 절은 "별도 명시 전까지 비공개(사내). `LICENSE`는 v2 코드 작성 단계 진입 시 결정."이라고 적는다. 반면 `AGENTS.md` "운영 도메인 / 시크릿 비노출" 절은 "이 repo는 **공개**다"라고 적어 두 문서가 상충한다(사실). `apps/api/pyproject.toml`에는 `license = { text = "MIT" }`가 패키지 메타데이터로만 선언돼 있다(사실). 선행 보고서(`F:/dev/kor-travel-geo-fixes/docs/kor-travel-common-library-review.md` §9 [P6])의 "Pinvi 루트 LICENSE 부재" 결론과 일치한다.
- 표기 규칙: 본 문서의 주장은 **사실**(파일에서 직접 확인) / **후보**(공통화 제안) / **추정**(정황 근거) / **미확인**(확인 못 함)으로 구분한다. 근거 경로는 저장소 상대 경로다.

## 1. 저장소 개요와 역할

1. Pinvi는 "한국 여행 계획·기록·공유 애플리케이션"으로, 한국 공공 API에서 모은 지도·날씨·이벤트·가격·공지·경로·구역 데이터를 사용해 사용자가 여행을 계획하고 이동 중 컨텍스트를 확인하고 결과를 기록·공유하도록 돕는 **사용자 대면 제품**이다 (`README.md` 1~5행, `AGENTS.md` "정체성").
2. 저장소는 npm workspaces + Python 두 생태계를 가진 모노레포다: `apps/api`(FastAPI), `apps/web`(Next.js 사용자 UI + Admin), `apps/mobile`(Expo Dev Client), `apps/etl`(Dagster), `packages/*`(TS 공용 7종), `infra/`, `docs/`, `contracts/`, `scripts/` (`package.json` `workspaces`, `README.md` "구성").
3. 지도 feature 도메인(정규화·저장·provider 변환·dedup)은 소유하지 않고 형제 저장소 `kor-travel-map`의 **OpenAPI HTTP 계약**(API/Admin API `:12701`)으로 소비한다. Pinvi는 `feature`/`provider_sync` 스키마에 DDL·ORM·직접 SQL을 두지 않는다 (`AGENTS.md` "책임 경계", ADR-003/026/027, `docs/kor-travel-map-integration.md`).
4. 주소·지오코딩·행정구역은 `kor-travel-geo` v2 REST를 직접 호출한다(ADR-025). 운영 배포는 `kor-travel-docker-manager`(`ktdctl`)가 1차 경로이고 포트 대역도 그 저장소의 target 대역을 따른다(ADR-040/042). AI companion은 `kor-travel-concierge`의 기존 계약을 소비하며 Pinvi 안에 AI provider 구현을 두지 않는다(`docs/tasks-rule.md` §10, ADR-020).
5. 지도 클라이언트는 형제 저장소 `maplibre-vworld-react`의 `vworld-map-web`/`vworld-map-core`/`vworld-map-rn`을 npm 발행 없이 **vendored tarball(`file:`)** 로 소비한다(ADR-044/046). 웹은 `NEXT_PUBLIC_VWORLD_API_KEY`, 모바일은 서버 발급 토큰(`GET /mobile/vworld/token`)을 쓴다(ADR-043/045).
6. 현 단계는 Sprint 1~5 릴리스(v0.1.0 2026-06-13, v0.2.0 2026-06-30) 이후 Sprint 6(v1.0.0) 진행 중이며, 열린 작업은 M05(kor-travel-map 페어 활성화·provenance) 계열과 모바일 T-320뿐이다 (`docs/sprints/README.md`, `docs/tasks.md`).
7. 디자인은 Airbnb 톤 reference(`DESIGN.md`)를 2026-08-18 "Hallmark 잠금 시스템"으로 고정했고, 토큰 정본은 `packages/design-tokens`(Tailwind v3 preset 형식)다. Admin 표면은 2026-09-01 T-356으로 `kor-travel-map` admin의 프리미티브 28종 + DataTable을 "색상톤만 제외하고" 이식했으며, 그 과정에서 `apps/web`만 Tailwind v4로 올렸다 (`docs/journal.md` 106행~, `docs/tasks-done.md` 113행~).
8. 여러 AI 도구(Claude/Codex/Antigravity/Cursor/Copilot)를 동시에 지원하는 문서 체계(`CLAUDE.md`↔`AGENTS.md` 동기, ADR-016)와 Linux 전용 개발·git·CodeGraph 정책(ADR-051), 에이전트별 고정 worktree(ADR-017)를 가진다.

## 2. 저장소 구조

최상위 트리(사실, `ls -la`):

```
.agents/ .claude/ .codex/ .gemini/ .github/ .hallmark/
.dockerignore .editorconfig .env.example .env.mcp-telegram.example .gitattributes .gitignore
.prettierignore .prettierrc.json
AGENTS.md CHANGELOG.md CLAUDE.md DESIGN.md README.md SKILL.md
airbnb-marker-palette.html antigravity.json claude.json codex.json
apps/ contracts/ docs/ infra/ packages/ scripts/ tests/
package.json package-lock.json tsconfig.base.json
```

npm workspaces(`package.json` `workspaces`): `apps/web`, `apps/mobile`, `packages/*`. `apps/api`·`apps/etl`은 Python 패키지(hatchling)이며 npm workspace가 아니다(사실).

| 디렉터리 | 역할 | 근거 |
| --- | --- | --- |
| `apps/api` | FastAPI 백엔드(`app/` 패키지, `alembic/`, `tests/`, `uv.lock`, `Dockerfile`) | `apps/api/pyproject.toml` |
| `apps/web` | Next.js 16 App Router — 사용자 UI(`(app)`, `(auth)`, 랜딩, 법무, 공유 뷰) + Admin(`(admin)`) | `apps/web/package.json`, `apps/web/app/` |
| `apps/mobile` | Expo SDK 57 Dev Client + Expo Router + NativeWind 4 (Tailwind v3) | `apps/mobile/package.json`, `apps/mobile/tailwind.config.js` |
| `apps/etl` | Dagster code location `pinvi.etl.definitions` (asset 6, job 7, schedule, sensor) | `apps/etl/pyproject.toml`, `apps/etl/pinvi/etl/definitions.py` |
| `packages/api-client` | fetch wrapper `ApiClient` + endpoint 함수 + TanStack Query key factory + WebSocket 클라이언트 | `packages/api-client/src/index.ts` |
| `packages/design-tokens` | 색/타이포/간격/모션 TS 상수 + `tailwind-preset.cjs` (웹·모바일 공용 정본) | `packages/design-tokens/` |
| `packages/domain` | 플랫폼 무관 순수 로직(거리·정렬·검증·공유링크·업로드·마커 스타일), DOM/next/RN import 금지 | `packages/domain/package.json` description |
| `packages/hooks` | `useDebounce`, `useUserLocation`(어댑터 주입) | `packages/hooks/src/index.ts` |
| `packages/i18n` | `messages/ko.json` (Auth 17·Common 7·Trip 4 키) | `packages/i18n/` |
| `packages/schemas` | Zod 스키마(API I/O·폼), envelope/좌표 공통 | `packages/schemas/src/common.ts` |
| `packages/state` | zustand `createAuthStore(storage)`, `useUiStore` | `packages/state/src/index.ts` |
| `contracts/` | kor-travel-map service/M05 pair provenance, 활성화 receipt trust, reviewer roster JSON 4종 | `contracts/*.json` |
| `infra/` | `docker-compose.yml`(dev, host network), `docker-compose.app.yml`(smoke/prod), `.env.prod.example`, `n150/`, `nginx/`, `grafana/`, `prometheus/`, `postgres/`, `blackbox/`, `cloudflare/`, `odroid/`(퇴역) | `infra/` |
| `scripts/` | dev-up/down, docker-app, backup/restore/hotswap, m05_* 증적, provenance 검증, `check-lockfile-integrity.mjs`, `pr_review_monitor.py`, `n150-playwright-runner.sh` | `scripts/README.md` |
| `tests/` | `load/api_p95_latency.py`, `security/csp_cors_rate_limit.py` (저장소 레벨 gate 스크립트) | `tests/` |
| `docs/` | §5 참조 | `docs/` |

## 3. 프론트엔드

### 3.1 apps/web — Next.js 사용자 UI + Admin (`apps/web`)

**프레임워크/런타임** (사실, `apps/web/package.json`, `package.json`, `package-lock.json`)

| 항목 | 선언 | 설치(lockfile) |
| --- | --- | --- |
| next | `16.3.3` (exact) | 16.3.3 |
| react / react-dom | `^19.0.0` (루트 `overrides` `19.2.6`) | 19.2.6 |
| typescript | `^5.6.0` | 5.9.3 |
| node engines | 루트 `engines.node >=20`, `engines.npm >=11`; CI·Dockerfile은 Node 22 | — |
| packageManager 필드 | 없음(사실). CI가 `npm install -g npm@11.19.1`로 고정 (`.github/workflows/web.yml`) | — |
| lockfile | `package-lock.json` lockfileVersion 3 (루트 단일), 무결성 하한 99% 가드 `scripts/check-lockfile-integrity.mjs` | — |

**스타일** (사실)

- tailwindcss `^4.3.3` → 4.3.3. 단, npm이 루트에는 `tailwindcss@3.4.19`(모바일 NativeWind용)를, `apps/web/node_modules`에 4.3.3을 **중첩** 설치한다(`package-lock.json`; `apps/web/Dockerfile` 주석이 이 중첩에 의존한다고 명시).
- 설정 방식: **v4 CSS-first + `@config` 혼합(mixed)**. `apps/web/app/globals.css`는 `@import 'tailwindcss'` 뒤 `@config '../tailwind.config.ts'`로 v3 preset을 그대로 읽고, admin 전용 토큰만 `@theme` 블록에 둔다. `apps/web/tailwind.config.ts`(preset + content 배열)가 잔존한다. `postcss.config.mjs`는 `@tailwindcss/postcss` 단일 플러그인(autoprefixer 없음).
- 토큰 정본은 `packages/design-tokens/tailwind-preset.cjs`(v3 preset 형식) 하나다. globals.css 주석: "`@theme`로 옮겨 적으면 두 곳이 조용히 드리프트한다(웹만 v4, 모바일은 NativeWind 4 + Tailwind v3 유지)". 이 주석은 "ADR"이라고 적지만 `docs/decisions.md`에 Tailwind v4 관련 ADR은 없다(사실, `grep` 0건 — 결정은 `docs/journal.md` T-356 엔트리와 `docs/tasks-done.md`에만 기록).
- preset 토큰 요약: 색(`primary` #ff385c/`active`/`disabled`, `cta` #e00b41/`hover` #c8093a, `focus`, `luxe`, `plus`, `canvas`, `surface-soft`/`-strong`, `hairline`/`-soft`, `border-strong`, `ink`/`body`/`muted`/`muted-soft`, `star-rating`, `on-primary`, `error-text`/`-hover`/`error-bg`, `success-text`/`-bg`, `legal-link`, `scrim`, `marker.p-01`~`p-16`), fontFamily `sans`(Pretendard Variable 스택)/`mono`(시스템 mono), borderRadius sm 8/md 14/lg 20/xl 32px, boxShadow `card`/`overlay`(≤8% opacity 2티어), zIndex `nav`30/`panel`40/`overlay`50/`modal`60/`toast`70, spacing `section` 64px, minHeight/minWidth `touch` 44px, transitionDuration `fast`100/`normal`200/`moderate`300, timingFunction `pinvi` cubic-bezier(0.2,0,0,1).
- admin 전용 `@theme` 변수(globals.css): `--radius-control` 6px, `--radius-panel` 8px, `--spacing-control` 36px, `--spacing-control-sm` 30px, `--spacing-rail`/`--container-rail` 22rem, `--text-2xs` 12px, `--text-md` 17px, `--ease-admin-out/in`, `--color-admin-line` #dddddd(장식), `--color-admin-control-line` #767676(컨트롤 경계, #f7f7f7 위 4.24:1 실측 주석), `--color-admin-page/subtle/muted`, `--color-admin-success/danger/warning/info` + `-tint`(불투명), `--color-admin-brand-tint` #ffeef1 / `-brand-ink` #c8093a. `[data-pv-surface='admin']`에서 `--text-xs/sm/base/lg/xl/2xl`를 13.5/15/15/20/24/30px로 가려 KTM 7단 타이포를 admin subtree에만 적용한다(`apps/web/app/(admin)/layout.tsx`가 표식을 건다).
- `:root` 앱 셸 변수: `--app-tabbar-h` 56px, `--tm-nav-h` 56px, `--tm-trip-tab-h` 44px, `--tm-panel-w-left` 340px, `--tm-panel-w-right` 320px.
- 라이트/다크: **다크 모드 없음**(사실 — `dark:` 사용 0건, `prefers-color-scheme` 0건; `docs/architecture/frontend.md` §3.2 "다크 모드 없음 v1"; `DESIGN.md` "Airbnb does not have a dark mode").
- 폰트: npm `pretendard` `^1.3.9` → 1.3.9, `globals.css`가 dynamic subset CSS를 `@import`(self-hosted, `font-display: swap`, 외부 CDN 금지). `word-break: keep-all` + `overflow-wrap: break-word`.
- 아이콘: `lucide-react` `^0.460.0` → 0.460.0. Maki 아이콘은 `vworld-map-web`의 `MakiMarker`가 담당하며, `frontend.md` §1이 말하는 `apps/web/public/maki/`는 현재 트리에 **없다**(사실, `public/`에는 favicon·앱 아이콘·`site.webmanifest`만 존재).
- 애니메이션: `tw-animate-css` 없음(lockfile 부재). 모션은 preset duration/easing 토큰만.

**UI 프리미티브** (사실)

- `@base-ui/react` `^1.7.0` → 1.8.0 — **admin 오버레이 전용**(`components/admin/ui/{dialog,alert-dialog,popover,tooltip}.tsx`). button/input/checkbox/separator/badge/breadcrumb 등은 이식하면서 base-ui 의존을 제거하고 네이티브 요소로 재작성했다(각 파일 헤더 주석).
- radix-ui: 직접 의존 없음. lockfile에 `@radix-ui/react-dialog@1.1.23` 등이 있으나 `apps/web/package.json`에는 없다(전이 의존, 상위 패키지 미확인).
- shadcn CLI: 없음. `components.json` 없음(사실). `docs/architecture/frontend.md`·`docs/spec/v8/03-frontend.md`가 "shadcn/ui + Radix Primitives"를 채택 스택으로 적지만 코드는 그렇지 않다(문서 stale, 사실).
- 보조: `class-variance-authority` 0.7.1, `clsx` 2.1.1, `tailwind-merge` 3.6.0(admin `cn` 전용; `lib/admin/cn.ts`가 `extendTailwindMerge`로 `rounded-control/panel`, `h-control/control-sm`, `w-rail`, `text-2xs/md` 그룹을 등록).

**컴포넌트 인벤토리** (사실, `find components -type f`)

`components/ui/*` (사용자 표면 프리미티브, 3개): `Button.tsx`(변형 primary/secondary/ghost/danger, 크기 md 44px/sm 36px→coarse pointer 44px/lg 48px, 8상태, `ButtonLink`), `Dialog.tsx`, `ConfirmDialog.tsx` (둘 다 `lib/useModalDialog.ts` 496줄 기반 portal 모달). 헤더에 `Hallmark · component: … · theme: pinvi-locked(DESIGN.md)` 마커.

`components/admin/ui/*` (KTM 이식 프리미티브 26개): `alert-dialog.tsx`, `alert.tsx`, `badge-variants.ts`, `badge.tsx`, `breadcrumb.tsx`, `button-variants.ts`, `button.tsx`, `card.tsx`, `checkbox.tsx`, `data-table.tsx`(853줄), `dialog.tsx`, `field-variants.ts`, `field.tsx`, `form-field-input.tsx`, `form-field-shared.ts`, `form-field.ts`, `form-select.tsx`, `form-textarea.tsx`, `help-tip.tsx`, `input.tsx`, `native-select-option.tsx`, `native-select.tsx`, `popover.tsx`, `separator.tsx`, `skeleton.tsx`, `table.tsx`, `textarea.tsx`, `tooltip.tsx`. 모든 파일 첫 주석이 출처를 명시한다: "kor-travel-map admin `src/components/ui/<name>.tsx`에서 이식(T-356)" 또는 "KTM `packages/kor-travel-map-admin/frontend/src/components/ui/<name>`에서 이식(T-356)", 이어서 "원문에서 바꾼 부분"(import 경로 `@/lib/utils`→`@/lib/admin/cn`, 색 토큰 치환표 `bg-card→bg-canvas`, `border-border→border-admin-line`, `text-text-primary→text-ink`, `bg-brand→bg-primary`, `border-input→border-admin-control-line` 등, `data-interactive:`→`data-[interactive]:`, base-ui 제거 여부). 12개 파일은 KTM의 `// Hallmark · genre: editorial-utilitarian · macrostructure: Rail-Workbench · design-system: design.md` 마커를 그대로 보존한다(사실, `grep -rl` 12건).

`components/admin/*` (앱 레벨 admin 부품 22개): `AdminPage.tsx`, `AdminQueryProvider.tsx`, `AdminTable.tsx`(KTM `DataTable` 위 어댑터, 소비 페이지 36곳 무수정, `manualSorting=false` 기본, `mobileCard` 모바일 카드), `DataTable.tsx`(하위호환 shim), `Placeholder.tsx`, `admin-shell-parts.tsx`(KTM `admin-shell.tsx` **부분** 이식: skip link·헤더 밴드·rail 그리드), `copy-button.tsx`(sonner 제거→인라인 aria-live), `detail-list.tsx`, `empty-state.tsx`, `filter-bar.tsx`, `json-viewer.tsx`, `pagination-bar.tsx`, `section-card.tsx`, `stat-strip.tsx`, `status-badge.tsx`, `status-badge-variants.ts`, 도메인 패널 `KorTravelMapCurationCollectionImportPanel.tsx`, `KorTravelMapCurationCutoverBackfillPanel.tsx`, `NoticeAttachmentPanel.tsx`, `NoticePlanEditor.tsx`, `NoticePoiEditor.tsx`, `RestoreHotswapDialog.tsx`. 이식 파일들은 모두 위와 같은 출처 헤더를 가진다.

앱/사용자 표면 공유: `components/app/{AppShell,PublicChrome,SettingsSurface,Wordmark}.tsx`, `components/forms/{FormField,FormSelect,FormTextArea,ResendVerificationButton}.tsx`, `components/feedback/{FullPageMessage,PageLoading,RouteError}.tsx`, `components/navigation/DocumentNavLink.tsx`("kor-travel-geo T-278 이식" 주석, `app/(admin)/admin/layout.tsx` 48행), `components/map/{FeatureDetailCardBody,FeatureDetailModal,FeatureDetailModalController,FeatureMapView,FeatureRequestDialog,LocationConsentDialog,MapSearchBox,MapView,vworldPrimitives}.tsx`(`vworldPrimitives.tsx`가 `vworld-map-web` dynamic import 단일 facade), `components/notice-plans/*` 2, `components/trips/*` 17. login-form은 별도 컴포넌트가 아니라 `app/(auth)/login/page.tsx`에 있다(추정 — 페이지 파일만 존재).

**상태/데이터** (사실)

- `@tanstack/react-query` `^5.59.0` → 5.102.8, 37개 파일에서 사용. Provider는 admin에만 `AdminQueryProvider`로 마운트하고 "다른 route group은 raw fetch 유지"(주석). `@tanstack/react-table` 8.21.3, `@tanstack/react-virtual` 3.14.10(admin DataTable).
- `zustand` `^5.0.0` → 5.0.15 — `packages/state`에만 있고 `apps/web` 소스에서 import 0건(사실, grep).
- `react-hook-form` `^7.54.0` → 7.87.0, `@hookform/resolvers` 3.10.0 — **선언만** 있고 `apps/web` 소스에서 사용 0건(사실). `zod` `^4.4.3` → 4.5.4(루트 hoist는 3.25.76, `@expo/cli`·`eslint-plugin-react-hooks`가 zod3 의존).
- API 클라이언트: 코드 생성기 없음(openapi-typescript 등 부재, 사실). `packages/api-client/src/client.ts`의 수작업 `ApiClient`(baseUrl/`getAuthToken`/`onUnauthorized`/`fetcher`/`timeoutMs` 기본 30s, 타이머가 body 소비 완료까지 유지, 타임아웃은 `status: 0` + `REQUEST_TIMEOUT` 코드, `Retry-After` 1~300초 파싱, `isVersionConflictError` 409 `VERSION_CONFLICT`). 응답은 `packages/schemas/src/common.ts`의 `SuccessEnvelopeSchema`/`ErrorEnvelopeSchema`로 파싱.
- 웹 인스턴스: `apps/web/lib/api.ts`(`NEXT_PUBLIC_PINVI_API_URL` 기본 `http://localhost:12801`, 401→`/login`). 여러 admin 컴포넌트가 `new ApiClient(...)`를 각자 생성한다(사실, 예 `components/admin/KorTravelMapCurationCollectionImportPanel.tsx`).

**인증 경계** (사실)

- Next `middleware.ts`/`proxy.ts` 없음. route handler는 `app/(admin)/admin/grafana/health/route.ts` 1개뿐. 브라우저가 API 도메인을 **직접** 호출하며(BFF 없음) 인증은 백엔드 httpOnly cookie다: `pinvi_access`(HS256 JWT 15분) + `pinvi_refresh`(opaque, DB에는 hash) `SameSite=Lax`, `Secure`는 `PINVI_ENVIRONMENT=production`일 때만 (`apps/api/app/core/session_cookies.py`, `docs/api/common.md` §3).
- CSRF 토큰 없음 — `SameSite=Lax` + OAuth state/PKCE hash(`docs/api/README.md`). CORS는 웹 origin만 허용, `allow_credentials=True`, `expose_headers=["Retry-After"]` (`apps/api/app/main.py`).
- Admin 가드는 클라이언트 `app/(admin)/admin/layout.tsx`(`/auth/me` 조회 후 로그인/권한 확인/권한 없음/정상 4트리)이고, 권한 정본은 서버 `require_role`(거부 시 404 은닉)이다 (`apps/api/app/core/rbac.py`, `docs/architecture/admin-rbac.md`).
- 모바일은 `/mobile/auth/*`로 토큰을 body로 받아 SecureStore에 보관하고 `Authorization: Bearer`로 붙인다 (§3.2).

**라우팅/화면 목록** (사실, `find app -name page.tsx`)

| 그룹 | page.tsx 수 | 대표 경로 |
| --- | --- | --- |
| `(admin)/admin` | 42 | `/admin`, users(+`[user_id]`), rbac, trips(+`[trip_id]`), pois(+`[poi_id]`), notice-plans(+new,`[planId]`), files, feature-requests, feature-reference-reconciliations, features(+`[feature_id]/{overrides,sources,weather-values}`, change-requests), audit(+location), incidents, abuse, dsr, moderation, emails, etl, provider-sync, dedup-review, integrity, api-calls, debug/logs, debug/request/`[request_id]`, backup, grafana, mcp-tokens, retention, system, category-mapping, seed, reset, login |
| `(app)` | 11 | `/trips`, `/trips/[tripId]`, `/trips/map-shell`, `/map`, `/notice-plans`, `/files`, `/settings/{consents,dsr,mcp-tokens,moderation,telegram}` |
| `(auth)` | 6 | `/login`, `/signup`, `/signup/verify-pending`, `/verify-email`, `/profile`, `/profile-complete` |
| 루트/기타 | 3 | `/`(랜딩, Narrative Workflow), `/legal/[slug]`, `/shared/[tripId]/[token]` + `not-found.tsx`, `error.tsx`, `global-error.tsx`, `loading.tsx` |

**반응형/모바일** (사실)

- Tailwind 기본 breakpoint만 사용: `sm:` 62 / `md:` 135 / `lg:` 117 / `xl:` 20 / `2xl:` 1회(grep). 커스텀 screens 없음.
- PC/Mobile 분기는 `lib/useMobileWebLayout.ts`(`(max-width: 1023px), (pointer: coarse) and (hover: none)` — UA 스니핑 제거) 결과를 `AppShell`이 `data-mobile-layout` 속성으로 걸고, `globals.css`의 **unlayered** 규칙이 `.lg:hidden` 유틸을 이기도록 한다(v4 네이티브 캐스케이드 레이어 대응, 주석에 N150 e2e 회귀 근거).
- 앱 셸: 데스크톱 상단 nav(`lg:flex`) + 모바일 고정 하단 탭바(`--app-tabbar-h` 56px, `env(safe-area-inset-bottom)`), `.app-shell-main` 하단 패딩.
- 터치 밀도: 사용자 표면 44px(`min-h-11` 83건, `size-11` 18건, `.touch-target`), `Button` `sm`은 `[@media(pointer:coarse)]:min-h-11`. Admin은 KTM 36/30px 컨트롤 유지(globals.css 주석이 사유를 적음), `AdminTable`의 `mobileCard`로 `md:hidden` 카드 목록, admin 사이드바는 `lg` 미만에서 가로 스크롤 nav(`app/(admin)/admin/layout.tsx` 247행).
- viewport: `app/layout.tsx` `viewportFit: 'cover'`, `themeColor: '#ffffff'`, PWA `site.webmanifest`.

**i18n / 접근성 / focus / reduced-motion** (사실)

- `next-intl` `^4.13.7` → 4.14.2 선언, `packages/i18n/messages/ko.json` 존재하지만 `apps/web`에서 `useTranslations`/`next-intl` import **0건**(grep). UI 문자열은 컴포넌트에 한국어 하드코딩 — `docs/conventions/coding-style.md` §3.8 규칙과 불일치(사실).
- 접근성 레시피: `.focus-ring` = `focus-visible:outline-2 outline-offset-2 outline-focus`(outline 사용 이유: transition 유틸과 무관하게 즉시 표시), `prefers-reduced-motion: reduce` 전역 0.01ms, 커스텀 `.checkbox` 20px, `button:not(:disabled){cursor:pointer}` 복원(v4 preflight 제거 대응), 상태 UI 4종(empty/loading/error/success), `role=status`/`aria-busy`/`aria-live` 사용, e2e `form-a11y`, `auth-form-a11y`, `dialog-focus`.
- 모달 계약: 사용자 표면은 `lib/useModalDialog`(body 직계 portal + `inert`, 전역 스냅샷 1개, Escape/Tab 최상단만, busy 시 실수 경로 잠금), admin은 base-ui. ESLint가 양방향 import 경계를 강제한다(`eslint.config.mjs` T-356/T-357).

**테스트·품질** (사실)

| 도구 | 설정 | 비고 |
| --- | --- | --- |
| vitest `^4.1.10` → 4.1.11 | `vitest.config.ts`: jsdom 단일 환경, `globals: true`, oxc automatic JSX(`@vitejs/plugin-react` 미사용), `tests/**/*.test.{ts,tsx}`, setup `@testing-library/jest-dom/vitest` | `tests/` 27개 |
| playwright `^1.56.0` → 1.63.0 | `playwright.config.ts`(mock e2e, `npm run build && next start -p 12805`, chromium), `playwright.admin-live.config.ts`, `playwright.live-mutating.config.ts` | `e2e/*.e2e.ts` 56 + `*.live.ts` 12 |
| eslint `^9.16.0` → 9.39.5 | `eslint.config.mjs`: `eslint-config-next/core-web-vitals` + `/typescript`(16.3.3) + Hallmark 클래스 가드(`no-restricted-syntax` Literal/TemplateElement 정규식: `bg-white`/`text-white`/`bg-black/`, `shadow-sm..2xl`, `z-[`, `text-[N`, h-8/9/10 컨트롤) + `no-restricted-imports`(kakao SDK, admin↔사용자 모달 스택 양방향, `@base-ui/react` 사용자 표면 금지) | react-doctor 없음(grep 0) |
| tsconfig | `tsconfig.base.json`: `strict`, `noUncheckedIndexedAccess`, `noImplicitOverride`, `noFallthroughCasesInSwitch`, `verbatimModuleSyntax`, `isolatedModules`, `moduleResolution: Bundler`; web은 `jsx: preserve`, `@/*` alias | — |
| prettier 3.9.6 | 루트 `.prettierrc.json`: printWidth 100, singleQuote, trailingComma all, LF | `.editorconfig`, `.gitattributes` LF |
| scripts | `lint: eslint .`, `typecheck: tsc --noEmit`, `test: vitest run`, `test:e2e*` | 루트 `npm run lint/typecheck/test/build --workspaces` |

**빌드/배포** (사실)

- `next.config.mjs`: `reactStrictMode`, `poweredByHeader: false`, `/admin/grafana` CSP `frame-src` 헤더, `transpilePackages`(`@pinvi/*` 7종 + `vworld-map-core` + `vworld-map-web`). `output: 'standalone'` 아님, `images` 설정 없음.
- `build: next build --webpack` — Next 16 Turbopack이 `vworld-map-web` 청크를 깨뜨려 webpack 고정(ADR-066). `dev`/`start` 포트 12805.
- `apps/web/Dockerfile`: `# syntax=docker/dockerfile:1.7.1-labs@sha256…` 첫 줄 필수, `node:22-bookworm-slim@sha256…` 3단계(deps/build/runtime), `COPY --parents apps/*/package.json packages/*/package.json` + `apps/*/vendor/`, `npm ci`, 빌드 ARG `NEXT_PUBLIC_*`, 런타임 `PORT=3000` + HEALTHCHECK, `scripts/validate-image-provenance.sh`로 `PINVI_SOURCE_REVISION` 검증, OCI revision 라벨. 주석에 "런타임 우선순위가 필요해지면 정답은 `output: 'standalone'`"이라고 남김.

**디자인 문서** (사실)

- `DESIGN.md`(451줄): 상단 "Pinvi 적용 메모"(StyleSeed 규칙 병행, shadow ≤8%) + Airbnb reference(색·타이포·레이아웃·elevation·컴포넌트·반응형 744/1128/1440 breakpoints·터치 타깃) + **"Hallmark 잠금 시스템 (2026-08-18)"**: Genre `modern-minimal`; macrostructure family(마케팅 `/`=Narrative Workflow, 앱=Workbench(카드 안 카드 금지, hairline row divider), 콘텐츠=Long Document `max-w-[65ch]`); 공개 chrome nav N1/footer Ft2; Theme 표(hex+OKLCH, `paper/paper-2/rule/ink/accent/cta/focus/error/success`); 대비 결정 C5(흰 라벨은 Rausch 3.5:1 미달→본문 크기 CTA는 `cta` #e00b41 4.9:1, Rausch는 아이콘·워드마크·포커스·≥24px 전용); Typography(Pretendard Variable 700/400, 12px 이하 금지, mono 시스템 스택, keep-all); Spacing/Shape/Elevation(4pt, radius 8/14/full, 그림자 2티어, z-index 5단); Motion(단일 easing, 100/200/300ms, overshoot·scale 금지, reduced-motion 전역); Microinteractions(조용한 성공, `window.confirm` 금지, 툴팁 hover 800ms/focus 0ms, 44px); CTA voice(`components/ui/Button.tsx` 8상태); per-page allowances; 공유/차이 허용 목록; 집행은 `eslint.config.mjs`; 모달 계약 + **admin 예외(T-356)**; Exports(`tokens.css` OKLCH, Tailwind v4 `@theme` 예시 — "현재는 v3 preset이 정본" 주석, W3C 토큰 JSON, shadcn 변수 매핑).
- `docs/design/styleseed-rules.md`(9절: 적용 범위 `apps/web`·`apps/mobile`·`packages/design-tokens`, 색/토큰, 레이아웃 리듬 `p-6`, 타이포 2:1 숫자/단위, 상태 UI 4종, 접근성 44px, Motion, Form, 우선순위 접근성>ADR>브랜드>StyleSeed).
- `docs/design/marker-palette.md`(16색 P-01~P-16 + maki 매핑, 브랜드 색 확정 시 ADR 교체), `airbnb-marker-palette.html`(시각 미리보기), `.hallmark/log.json`(2026-08-18 공개 표면, 2026-08-21 admin M04/M05)·`.hallmark/preflight.json`.
- `docs/architecture/frontend.md`(795줄)는 스택 표가 stale하다: Next.js 15 / Tailwind 3.4+ / shadcn+Radix / 모바일 Tamagui 후보 / `public/maki` / `feature-flags` 패키지 — 코드는 Next 16 / Tailwind 4(web) / base-ui / NativeWind / maki 없음 / feature-flags 없음(사실).

### 3.2 apps/mobile — Expo Dev Client 앱 (`apps/mobile`)

**프레임워크/런타임** (사실, `apps/mobile/package.json`, 루트 `overrides`, lockfile)

| 항목 | 선언 | 설치 |
| --- | --- | --- |
| expo | `~57.0.16` (루트 `dependencies.expo`도 `~57.0.16` — hoist 사유 주석은 `docs/resume.md` 2026-09-05) | 57.0.20 |
| expo-router / expo-dev-client / expo-location / expo-secure-store | `~57.0.x` | 57.0.19 / 57.0.18 / 57.0.16 / 57.0.3 |
| react-native | `0.86.3` (루트 override) | 0.86.3 |
| react-native-reanimated / worklets | `4.6.0` / `0.12.1` (루트 override) | 4.6.0 / 0.12.1 |
| react / react-dom | `^19.2.3` (override 19.2.6) | 19.2.6 |
| nativewind | `^4.1.23` | 4.2.6 |
| tailwindcss (devDependency) | `^3.4.15` | 3.4.19 (루트 hoist) |
| @maplibre/maplibre-react-native | `^11.3.4` | 11.3.8 |
| vworld-map-rn / vworld-map-core | `file:vendor/*-1.0.0.tgz` | 1.0.0 |
| eslint-config-expo | `~57.0.2` | 57.0.2 |
| `expo.install.exclude` | react, react-dom, react-native-reanimated, react-native-worklets, typescript (의도적 편차) | — |

- Expo Go 미사용, EAS Build(`eas.json` development/preview/production), Android `minSdkVersion 24`(`expo-build-properties`), New Architecture 기본, `app.json` `extra.pinvi.vworld.keySource: server-issued`, 번들 키 없음(ADR-043/045).
- 스타일: `tailwind.config.js` `presets: [nativewind/preset, @pinvi/design-tokens/tailwind-preset]`, `global.css`는 v3 지시어(`@tailwind base/components/utilities`), `babel.config.js` `nativewind/babel` + `jsxImportSource`, `metro.config.js` `withNativeWind` + workspace `watchFolders`, `nativewind-env.d.ts`.
- 토큰 공유 방식: (1) 동일 preset으로 className 토큰(`bg-canvas`, `text-ink`, `border-hairline`, `rounded-md` 등), (2) RN prop 값이 필요한 곳은 `import { colors } from '@pinvi/design-tokens'`(`components/ui.tsx` — `ActivityIndicator color`, `placeholderTextColor`). `packages/domain/src/{marker,poiDetail}.ts`도 `MARKER_PALETTE`를 소비한다.
- UI 키트: `components/ui.tsx` 단일 파일(Screen/Heading/Subheading/Body/Muted/Card/Button/Field/ErrorBanner/EmptyState/ErrorView/Loading/Checkbox…) + `components/TripDayHeader.tsx`. 웹과 "각자 구현"(frontend.md §2.1). 주의: 모바일 `Button` primary는 `bg-primary` + `text-white`를 쓰는데, 웹 Hallmark 가드는 `text-white`를 금지하고 본문 CTA에 `cta`를 쓰도록 한다(사실 — 규칙 적용 범위가 웹 lint에만 있음).
- 인증/상태: `lib/tokens.ts`(SecureStore), `lib/api.ts`(Bearer + `/mobile/auth/refresh` 회전, in-flight 공유), `lib/storage.ts`(AsyncStorage → zustand `StateStorage`), `lib/stores.ts`, `lib/auth.tsx`(AuthProvider), `lib/location.ts`(expo-location → `LocationAdapter`), `lib/config.ts`(`EXPO_PUBLIC_PINVI_API_URL` 또는 `extra.pinvi.apiBaseUrl`), `lib/oauth.ts`.
- 라우트: `app/_layout.tsx`(SafeArea→Query→Auth), `(auth)/{login,signup,verify-email}`, `(app)/{index,map,profile,notice-plans/index,settings/{index,consents,mcp-tokens,telegram},trips/{index,new,[tripId]/{index,edit,poi/[poiId]}}}`, `shared/[tripId]/[token]` — 웹과 같은 트리 명명(frontend.md §8).
- 테스트/품질: `eslint.config.js`(`eslint-config-expo/flat`, `--max-warnings 0`), `tsconfig.json`(`jsx: react-jsx`, `allowJs: true`), 단위 테스트 없음(사실), CI `mobile.yml` typecheck + lint 필수, `expo-doctor@1.20.2` 정보성.
- Tailwind v4 전환 정책과의 관계(사실 근거): `docs/journal.md` 106행~ T-356: "Tailwind v3 → v4 (웹만). admin만 올리는 것은 불가능… NativeWind가 하드 의존하는 v3 내부 경로 3개(`lib/util/flattenColorPalette`, `plugin`, `lib/cli/build`)가 온전하다. NativeWind 5는 v4를 받지만 아직 preview고 `latest`는 4.2.6이라 모바일은 v3 유지." `apps/web/Dockerfile` 주석: "mobile이 v4로 올라가면 중첩이 사라지고 프로덕션 빌드가 깨진다"(런타임 `node_modules` 복사 전략이 중첩에 의존). 즉 모바일 v4 전환은 NativeWind 5 안정화가 선결 조건이고, 전환 시 웹 Dockerfile·lockfile·preset 소비 방식(`@config`)이 함께 바뀐다(사실+추정).

### 3.3 packages/* (공용 TS) 요약

- 전 패키지 `"main": "./src/index.ts"` 소스 배포(빌드 산출물 없음), `tsconfig`는 base 상속 + `noEmit`, `typecheck` 스크립트만(`domain`·`schemas`는 `vitest run` 테스트 보유, CI `npm test --workspaces`). 사용자 표면·모바일 공유가 목적이며 `next/*`·`react-native/*`·DOM import 금지 규칙(frontend.md §6.3; ESLint 강제는 **미확인** — `packages/*`에 eslint 설정 없음).
- `@pinvi/api-client` 의존: `@pinvi/schemas`, `zod`. `@pinvi/domain` 의존: api-client, design-tokens, schemas. `@pinvi/state`: zustand + react peer. `@pinvi/hooks`: react peer.

## 4. 백엔드

### 4.1 apps/api — FastAPI (`apps/api`)

- python: `requires-python >=3.12` (`pyproject.toml`), CI/Docker `3.12`. `.python-version` 없음.
- 빌드 시스템: **hatchling** (`[build-system]`), `[tool.hatch.build.targets.wheel] packages=["app"]`, `force-include`로 루트 `contracts/*.json` 4종을 `app/_contract_data/`에 패키징. lockfile: `apps/api/uv.lock`(384KB) 존재. 단 `Dockerfile`·CI는 `pip install -e ".[dev]"`를 쓰며 uv.lock을 읽지 않는다(사실) — 문서(`README.md`, `docs/conventions/coding-style.md`)는 `uv` 권장.
- 프레임워크·핵심 의존 선언 범위 → `uv.lock` 버전: fastapi `>=0.115` → 0.141.1; uvicorn[standard] `>=0.32` → 0.52.3; pydantic `>=2.9` → 2.13.4; pydantic-settings `>=2.6` → 2.15.0; sqlalchemy[asyncio] `>=2.0.36` → 2.0.52; asyncpg `>=0.30` → 0.31.0; alembic `>=1.14` → 1.19.1; argon2-cffi `>=23.1` → 25.1.0; passlib[argon2] `>=1.7`; python-jose[cryptography] `>=3.3` → 3.5.0; httpx `>=0.27` → 0.28.1; tenacity `>=9.0` → 9.1.4; structlog `>=24.4` → 26.1.0; python-multipart; email-validator; slowapi `>=0.1.9`; resend `>=2.4`; boto3 `>=1.35`; cryptography `>=43`; prometheus-client `>=0.22` → 0.26.0. dev: pytest `>=8.3` → 9.1.1, pytest-asyncio, pytest-split, ruff `>=0.7` → 0.16.3, mypy `>=1.13` → 2.3.1, types-passlib, testcontainers[postgres] `>=4.8` → 4.15.0, freezegun, vcrpy. **psycopg·typer·dagster·import-linter·pytest-cov 없음**(사실).
- 앱 구성: `app/main.py`가 모듈 레벨 `app = FastAPI(title="Pinvi API", docs_url="/docs", redoc_url="/redoc", lifespan=…)`를 만든다(팩토리 함수 없음). lifespan에서 kor-travel-map/geo/kakao/naver 클라이언트와 outbox·sync 워커 13개를 `async with`로 묶는다. 라우터: `app/api/v1/__init__.py`의 `api_router = APIRouter()`(prefix 없음)에 `healthz`, `auth(/auth)`, `oauth`, `users`, `mobile(/mobile)`, `telegram_targets`, `trip_telegram_targets`, `trips(/trips)`, `pois`, `ws`, `notice_plans`, `public`, `features`, `geo`/`regions`, `search`, `storage`, `mcp(/mcp)`, `webhooks/resend`, `admin_router`(자체 prefix 없음; 하위 라우터가 `/admin/*` 추정 — `docs/api/admin.md`) 순으로 포함. 따라서 실제 URL은 `/health`, `/trips` 등 **`/v1` prefix 없음**(사실). `docs/api/common.md` 상단 ADR-030 박스는 "`/v1` 노출"이라 하고 §13은 "prefix는 `/`"라 해 문서 내부 불일치(사실).
- 미들웨어(등록 순): `LocationAuditMiddleware`, `RateLimitMiddleware`(ADR-038: production/staging은 Postgres fixed-window `app.rate_limit_buckets`, 그 외 memory; 키는 HMAC-SHA256 해시; 429 `RATE_LIMITED` + `Retry-After`; admin override `RATE_LIMIT_BLOCKED`), `GeofenceMiddleware`(ADR-018, `CF-IPCountry` 등), `RequestIdMiddleware`(`X-Request-Id`), `PrometheusMetricsMiddleware`, `CORSMiddleware`, `SecurityHeadersMiddleware`(HSTS/CSP/nosniff/Referrer-Policy/Permissions-Policy geolocation=(self)/X-Frame-Options DENY — `docs/api/common.md` §11, `tests/security/csp_cors_rate_limit.py`).
- 에러 envelope: `app/core/errors.py` — `HTTPException` → `{"error": {"code","message","details?"}}`(detail이 dict면 그대로, 아니면 status→code 기본 매핑 400/422 `VALIDATION_ERROR`, 401 `TOKEN_INVALID`, 403 `PERMISSION_DENIED`, 404 `RESOURCE_NOT_FOUND`, 409 `VERSION_CONFLICT`, 429 `RATE_LIMITED`, 503 `SERVICE_UNAVAILABLE`, 기타 `INTERNAL_ERROR`), `RequestValidationError` → 422 `VALIDATION_ERROR` + `details.errors`, 미처리 예외 → 500 + 보안 헤더. 표준 코드 12종 표는 `docs/api/common.md` §2.3, `docs/architecture/api-contract.md`.
- 응답 스키마: `app/schemas/envelope.py` `Envelope[T]{data}` / `EnvelopeWithMeta[T]{data, meta{cursor,has_more,total,page,limit,version}}` (Python 3.12 generic 문법). 프론트 Zod 대응은 `packages/schemas/src/common.ts`.
- 페이지네이션: 사용자 대면은 cursor(`limit` 기본 20 최대 100), Admin은 page/limit(`docs/api/common.md` §5는 `limit 50/100/200/500`, `docs/api/admin.md`는 `page_size 1~200 기본 50` — 문서 간 불일치 후보). Optimistic lock `If-Match: <version>` → 409 `VERSION_CONFLICT`. 좌표 `{lon,lat}` lng-first, datetime ISO 8601 `+09:00`, id 필드 `<entity>_id`, 생성 201.
- 인증: Argon2id(`passlib` CryptContext `argon2__type="ID"`), JWT HS256(`python-jose`), refresh opaque `secrets.token_urlsafe`, cookie `pinvi_access`/`pinvi_refresh`, Bearer 선택, RBAC `require_role(*roles)` `Role = user|admin|operator|cpo`(거부 404), Admin audit hash chain(ADR-034), MCP read-only 토큰(`/mcp/tools`, `/mcp/sse`, `PINVI_MCP_JWT_SECRET`, ADR-019). 외부 서비스 토큰: kor-travel-map `X-Kor-Travel-Map-Service-Token`(서비스), `X-Kor-Travel-Map-Api-Key`(public read fallback), ops read/cancel, cache-target command/consumer/restore-fence/recovery 역할별 분리(ADR-059), `KOR_TRAVEL_MAP_FEATURE_REQUEST_TOKEN`(외부 정본 이름 예외); kor-travel-geo는 `key=<PINVI_VWORLD_API_KEY>` query(ADR-048).
- OpenAPI: FastAPI 자동 생성 `/docs`·`/redoc`·`/openapi.json`만 있고 **자체 OpenAPI export 스크립트·저장 파일·drift 검사 없음**(사실, `find -name openapi*.json` 결과는 vendored KTM 스냅샷뿐). 대신 kor-travel-map 계약 스냅샷 3종(`apps/api/tests/contract/kor-travel-map-openapi-{user,service,admin}.json`) + golden 2종을 핀 커밋과 byte 동일성으로 CI 검증(`api.yml` `contract-pin-consistency`)하고 매일 `contract-staleness`로 Map main 대비 드리프트를 경고한다. 태그는 라우터별 `tags=["trips"]` 등(operationId 규약 미확인). `docs/test-strategy.md` §8이 말하는 `.github/workflows/openapi.yml`·`security.yml`은 존재하지 않는다(사실).
- 설정: `app/core/config.py` `Settings(BaseSettings)` `model_config = SettingsConfigDict(env_file=".env", …)`(610행). `env_prefix` 선언은 grep에 없고 필드명이 `pinvi_environment`처럼 `pinvi_` 접두를 직접 가진다(사실; 환경변수 `PINVI_*`). `PinviEnvironment = development|test|smoke|isolated|staging|production`. 루트 `.env.example` 200키(`PINVI_*` 대다수, `NEXT_PUBLIC_*` 7, `EXPO_PUBLIC_PINVI_API_URL`, `DATA_GO_KR_SERVICE_KEY`, `KOR_TRAVEL_MAP_FEATURE_REQUEST_TOKEN`), `apps/api/.env.example` 별도, `infra/.env.prod.example` placeholder 템플릿. 단위 테스트 `test_compose_delivers_declared_settings.py`가 compose ↔ 설정 선언 정합을 검사.
- 관측성: structlog JSON(`app/core/logging.py`: `merge_contextvars`, `add_log_level`, `TimeStamper(iso, utc=False)`, `dict_tracebacks`, `JSONRenderer`, stdlib bridge). 메트릭 접두 **`pinvi_api_`**(`http_requests_total`, `http_request_duration_seconds`, `http_requests_in_progress`, `db_pool_connections{state}`; route 라벨은 FastAPI 템플릿; `PROMETHEUS_MULTIPROC_DIR`; `/metrics` 경로·제외 경로 설정). health: `GET /health`, `/health/db`(503 `DB_UNAVAILABLE`), `/health/cache-target-sync`, `/health/feature-reference-reconciliation`, 문서상 `/health/external`. Sentry/Loki는 문서(`docs/integrations/{sentry,loki}.md`)와 env 키만 확인. Grafana 대시보드 5종 `infra/grafana/dashboards/*.json`.
- DB: PostgreSQL 16 + PostGIS 3.5(`postgis/postgis:16-3.5-alpine`), 스키마 `app`(Pinvi 소유), `ops`(Dagster), `x_extension`(pgcrypto/pg_trgm/PostGIS, ADR-008), `feature`/`provider_sync`(KTM 소유, 접근 금지). Alembic: `apps/api/alembic/`(`env.py` async engine NullPool + 명시 commit + `pg_advisory_xact_lock` 직렬화, `version_table_schema="app"`, `CREATE SCHEMA IF NOT EXISTS app/x_extension`), `alembic.ini` `file_template = %Y%m%d_%H%M_%slug`, `versions/`는 ADR-065 재기준화로 2개(`20260824_0100_app_schema_baseline.py`, `20260824_0101_m05_activation_contract.py`) + `baselines/*.sql`. 명명 규약 `pk_/fk_/ix_|idx_/uq_/ck_/trg_` + 짧은 alias 표(`docs/conventions/database.md`). 세션: 단일 글로벌 `create_async_engine`(`pool_pre_ping`, `server_settings` `lock_timeout 30s`/`idle_in_transaction_session_timeout 60s`/`statement_timeout 600s`), `async_sessionmaker(expire_on_commit=False)`. 운영 role 토폴로지: owner/schema owner/migration owner/migrator/app runtime 분리(`infra/postgres/bootstrap-pinvi-runtime-role.sh`, `docker-compose.app.yml`).
- 백업/복원: `scripts/backup-db.sh`(pg_dump custom + sha256), `restore-db.sh`, `restore-hotswap.sh`, `trusted-{backup,hotswap}-entrypoint.py`, `m05_*` 증적/lease/forensics, compose `app-backup`(maintenance profile, root-only), ADR-022/060/065. Dagster는 `apps/etl`(§4.2). CLI: `[project.scripts]` 6종(`pinvi-admin-bootstrap`, `pinvi-cache-target-*` 4, `pinvi-feature-uuid-cutover`) — 모두 `argparse` 기반 `main`(사실, typer 없음).
- 테스트: `tests/unit`(91 파일, PostGIS 불필요), `tests/integration`(89 파일; `conftest.py`가 testcontainers PostGIS session 1회 + `alembic upgrade head` + 테스트마다 TRUNCATE, 함수 스코프 엔진 NullPool, ASGITransport httpx), `tests/contract`(vendored 스냅샷/golden), `tests/integration/kor_travel_map/test_public_auth_live.py`(`PINVI_KOR_TRAVEL_MAP_LIVE_SMOKE=1` opt-in). CI: unit + `alembic upgrade head` sanity + wheel 검증 1 job, integration `pytest-split` 4 shard. **coverage gate 없음**(사실 — pytest-cov 미설치, CI 단계 없음; `docs/test-strategy.md`는 "warn→blocker 단계적"). ruff: `line-length 100`, `target-version py312`, `select E,F,W,I,UP,B,RUF,S,ASYNC`, `ignore E501,S101`, `per-file-ignores tests S105/S106/S107`, `exclude alembic/versions`. mypy: `strict`, `plugins pydantic.mypy`, 외부 모듈 `ignore_missing_imports`(resend/jose/boto3/prometheus_client). import-linter: `docs/conventions/coding-style.md` §2.5·`docs/architecture.md` §2.1이 계약 예시를 적지만 pyproject·CI에 **없음**(사실).

### 4.2 apps/etl — Dagster (`apps/etl`)

- python `>=3.12`, hatchling, `allow-direct-references = true`. **lockfile 없음**(uv.lock 부재, 사실). 의존: `dagster>=1.9`, `dagster-webserver>=1.9`, `sqlalchemy[asyncio]>=2.0`, `asyncpg>=0.30`, `httpx>=0.27`, `python-kasi-api @ git+https://github.com/digitie/python-kasi-api.git@main`(브랜치 직접 참조, 핀 없음 — 사실), `structlog>=24.4`; dev pytest/pytest-asyncio/ruff/mypy. `[tool.ruff] line-length 100`, `[tool.dagster] module_name = "pinvi.etl.definitions"`.
- 구성: `pinvi/etl/definitions.py` `Definitions(assets=6, jobs=7, schedules, sensors=[pinvi_run_failure_sensor], resources={db: PinviDatabaseResource(EnvVar PINVI_DATABASE_URL), kasi: KasiResource(DATA_GO_KR_SERVICE_KEY)})`. 자산: `pinvi_email_outbox`, `pinvi_kasi_special_days`, `pinvi_location_log_archive`, `pinvi_pii_retention`, `pinvi_telegram_system_outbox`, `pinvi_trip_day_rise_sets`; `schedules.py` cron(예 `30 3 * * *`); `sql/{outbox,retention}.py`. ADR-050 app-owned job 표준(retry/backoff, idempotency, failure notification, destructive dry-run gate).
- Dockerfile `python:3.12-slim@sha256…`, webserver 12802 고정(ADR-047), provenance 검증 동일. 테스트 9 파일(`tests/test_definitions.py` 로드 테스트 등). CI `etl.yml`: `sanity`(ruff + pytest) + `docker-image`(빌드 후 code location import). mypy는 CI에 없음(사실).

## 5. 문서·에이전트 규약

**진입 파일** (사실, `wc -l`)

| 파일 | 줄 | 역할 |
| --- | --- | --- |
| `CLAUDE.md` | 222 | Claude 1쪽 진입 요약(현 단계, ADR 현황 ADR-001~056 요약, 절대 금지 6개, 체크리스트, 빠른 문서 검색 표) |
| `AGENTS.md` | 445 | 정책 정본(사고 원칙 5절, 도구별 진입 표, 문서 언어 정책, 식별자, 의존 저장소 표, worktree/CodeGraph, Linux-only, 지시 우선순위, 릴리스 로드맵, 진입 절차, 커밋/PR, 시크릿 비노출, push 전 보안 감사, Telegram MCP, 책임 경계) |
| `SKILL.md` | 281 | 도메인 어휘, 빠른 시작, 디렉터리 지도, DO NOT 22항, 자주 묻는 작업 |
| `README.md` | 244 | 정체성, 구성, 포트, 빠른 시작, 문서 지도 |
| `DESIGN.md` | 451 | §3.1 디자인 문서 |
| `CHANGELOG.md` | 437 | 사용자 가시 변경(Unreleased 상단) |

- 지시 우선순위(`AGENTS.md`): 1 accepted ADR(`docs/decisions.md`) → 2 `AGENTS.md` → 3 `SKILL.md` → 4 `docs/agent-guide.md` → 5 `docs/sprints/SPRINT-N.md` → 6 개별 문서 → 7 `docs/journal.md`. `CLAUDE.md`↔`AGENTS.md` fact drift 방지 동기 규칙(ADR-016), 한국어 문서 정책(ADR-009: 식별자·명령·URL만 영문).
- 도구 설정: `claude.json`/`codex.json`/`antigravity.json`/`.codex/config.toml`/`.gemini/mcp.json`에 MCP 서버 `playwright`, `sequential-thinking`, `codegraph`(`@colbymchenry/codegraph serve --mcp`), `mcp-telegram`(`scripts/mcp_telegram_start.py`)을 등록. **`cwd`가 `F:\dev\pinvi-claude` 같은 Windows 경로이고 `C:\Python314\python.exe`를 호출**해 ADR-051 Linux-only 정책과 어긋난다(사실). `.claude/agents/*.md` 5종(api-designer, backend-developer, frontend-developer, mobile-developer, ui-designer), `.codex/agents/*.toml` 6종, `.claude/skills/` + `.agents/skills/` postgres 계열 skill 7종을 두 디렉터리에 복제, `.claude/settings.json`은 `expo@claude-plugins-official` 플러그인만.

**docs/ 트리** (사실, `ls docs`)

| 경로 | 내용 | 규약 |
| --- | --- | --- |
| `docs/decisions.md` (3263줄) | ADR-001~ADR-067 단일 파일 | 포맷 `## ADR-NNN: 요약` + 상태/날짜/결정자/컨텍스트/결정/근거/결과/후속, superseded는 본문 보존 (`docs/agent-guide.md` §3) |
| `docs/journal.md` (11935줄) | 역시간순 작업 일지 | `## YYYY-MM-DD (agent) — 제목`, 작업/변경/결정/발견/다음 필드 |
| `docs/resume.md` (5604줄) | 진척 + "다음 한 작업" 정본 | 작업 마무리마다 갱신 |
| `docs/tasks.md` (23줄) / `docs/tasks-done.md` (1561줄) / `docs/tasks-rule.md` (109줄) | 열린 `[ ]`만 / 완료 아카이브 / 규약 | Task ID `T-NNN`, 하위 `T-NNN<letter>`, 파생 `T-NNN-<slug>` (실제로는 `T-VN-41F1D-D1`, `T-VN-M05-…` 같은 확장 ID도 사용); 마커 `[ ]`/`[x]`/`[~]`(코드에는 `[/]`도 등장); 완료 워크플로 7단계; 선점/충돌 회피 기록; "`kor-travel-map` 저장소의 task 분리 정책을 적용" |
| `docs/sprints/SPRINT-1..6.md` + `README.md` | Sprint 계획·DoD·릴리스 표 | 진입 게이트 |
| `docs/runbooks/` 25 | local-dev, docker-app, deploy(N150), backup-restore, observability, admin, admin-live-e2e, live-mutating-e2e, v100-live-gate, codegraph-worktrees, pr-review-sprint4, secrets, korea-only, mcp-server, security-incidents, retention-execution, cache-target-causal-canary, odroid-docker(퇴역) 등 | 인덱스 `README.md` |
| `docs/reviews/` 5 | 2026-06 PR 리뷰 기록 + kor-travel-map cross-repo decisions | — |
| `docs/audit/` 2 | 2026-06-06 문서·구현 정합성 감사, 2026-06-29 위협 모델 | 발견 ID `P-/A-/C-/D-` |
| `docs/execplan/` 29 | task별 실행 계획(`<task-name>.md`) | 다중 경계 작업 시 필수(`AGENTS.md`) |
| `docs/architecture/` 15 + `architecture.md` | frontend, admin-rbac, api-contract, backup-restore, dagster-etl-bridge, expo-implementation-plan, korea-only-policy, map-marker-design, mcp-server/tools, notice-plans, user-location, websocket-broker 등 | — |
| `docs/api/` 15 | common + 도메인 13 + README | 코드 구현 전 문서 우선 |
| `docs/integrations/` 13 | kor-travel-map-rest-api, kor-travel-geo, maplibre-vworld, kakao-map, kakao-naver-local, kasi, resend, social-login, telegram, sentry, loki, gemini | — |
| `docs/conventions/` 6 | coding-style, database, testing, geospatial, normalization + README | ADR 우선 |
| `docs/compliance/` 4, `docs/legal/` 5, `docs/spec/v8/` 7, `docs/design/` 2, `docs/data-sources/` 1 | 법무·SPEC V8 적용 노트 등 | — |
| 기타 | `agent-guide.md`(377), `agent-workflow.md`(115), `agent-failure-patterns.md`, `dev-environment.md`(291), `test-strategy.md`(147), `data-model.md`, `postgres-schema.md`, `kor-travel-map-integration.md`(329), `kor-travel-map-requirements.md`, `v1-to-v2-mapping.md`, `decisions-needed-2026-06-06.md` | — |

**개발 환경·워크플로** (사실)

- 정본: **Linux/WSL**(ADR-051). git/편집/commit/push/PR/의존성/pytest/Docker/dev server/lint/typecheck/build/Vitest 모두 Linux. Windows `git.exe`·`/mnt/c` shim 금지. Playwright는 **N150 x86_64 Docker runner 전용**(`scripts/n150-playwright-runner.sh`), 불가 시 gate 중단. 단 `docs/conventions/coding-style.md` §1은 "불가 시 Windows fallback"이라고 적어 정책과 불일치(사실).
- worktree: 에이전트별 고정 `pinvi-claude`/`pinvi-codex`/`pinvi-antigravity`(ADR-017), 브랜치 `agent/<agent>-<task>` from `origin/main`, CodeGraph `init -i`/`sync`/`status`, `.codegraph/` gitignore, 코드 수정 전 `codegraph_explore` 영향도 평가 의무.
- 리뷰: `docs/runbooks/pr-review-sprint4.md`(리뷰→코멘트→직접 수정→기반 라이브러리 PR 우선→sync→머지), `codex-pr-review.yml`/`codex-pr-monitor.yml`(5분 cron, 외부 API 키 없이 reminder 댓글). "전문 리뷰어 2명 적대적 리뷰 + 교차검증"은 `docs/journal.md`(79회)·`tasks-done.md`(33회)에 반복 기록된 **관행**이며 `AGENTS.md`·`CLAUDE.md`·`agent-guide.md`에 명문 규칙은 없다(사실, grep 0건).
- 브랜치/PR: `feat/ fix/ chore/ docs/ refactor/ adr/ agent/<agent>-<topic>`, 커밋 `<scope>: <verb> <object>`(scope api/web/etl/infra/docs/chore/adr/tests/packages/<name>), PR 본문 템플릿(동기/변경/영향/검증/문서/관련), squash merge, ruleset `main-pr-only`(PR 필수, linear history, force push·삭제 차단, bypass 없음), required check는 `Aggregate CI gate` 하나.
- 보안 감사: push 직전 `git diff --cached` 파일명·비밀 패턴 grep(정규식 `api[_-]?key|secret|password|token|pbkdf2_sha256|AKIA…|PRIVATE KEY`), `*.local.md`(`docs/deploy-runbook.local.md`, `docs/prod-access.local.md`)·`.env*`·`.env.mcp-telegram` gitignore, 실제 도메인은 `*.example.com` placeholder(ADR-047). "kor-travel-concierge AGENTS.md 동일 패턴"이라고 명시.
- 완료 알림: PR 생성 후 `mcp-telegram` `send_message`(credential은 worktree 로컬 `.env.mcp-telegram`).

## 6. CI·배포·운영

- `.github/workflows/`(사실 7개): `api.yml`(ruff check/format, m05 스크립트 lint + `bash -n`, mypy --strict, pytest unit, alembic upgrade head on PostGIS service, wheel provenance 검증, integration 4-shard, docker-provenance-image, contract-pin-consistency, 일일 contract-staleness), `web.yml`(npm 11.19.1 핀, lockfile integrity, `npm run lint/typecheck/test/build --workspaces`, docker-image 빌드+기동 확인, e2e Playwright mock + live-mutating `--list` 카탈로그 검증), `mobile.yml`(typecheck, lint, expo-doctor 정보성), `etl.yml`(sanity, docker-image), `aggregate-ci.yml`(변경 경로별 required check 대기, deadline 40분/timeout 45분), `codex-pr-review.yml`, `codex-pr-monitor.yml`. 모든 job이 exact PR head SHA를 체크아웃. `README.md`의 `docker-images.yml`(GHCR push)은 파일이 없고 `docs/runbooks/deploy.md`가 폐지를 명시(사실).
- pre-commit: `.pre-commit-config.yaml` 없음(사실). husky 등도 없음.
- Docker compose: `infra/docker-compose.yml`(dev; `network_mode: host`, postgres 5432, rustfs 12101/12105, dagster profile `etl` 12802, observability profile cadvisor 12301/prometheus 12401/grafana 12205), `infra/docker-compose.app.yml`(smoke/prod; 이미지 digest 핀, `app-postgres`/`app-db-runtime-role`/`app-rustfs`/`app-api` 127.0.0.1:12801/`app-web` 12805/`app-dagster` 12802/`app-backup`(maintenance)/`app-migrator`/`app-legacy-rebaseline-migrator`/observability). 포트 규약은 `kor-travel-docker-manager` target 대역(ADR-042/047): API 12801, Web 12805, Dagster 12802, kor-travel-map 12701, RustFS 12101/12105, Grafana 12205, cAdvisor 12301, Prometheus 12401, kor-travel-geo 12501(문서).
- prod(N150): 단일 노드 Ubuntu 26.04(ADR-067), `ktdctl pinvi-pair rebuild-pinned --confirm`(로컬 빌드 `pinvi-{api,web,dagster}:latest-main`, GHCR 미사용), 이미지 provenance(`org.opencontainers.image.revision`, `io.pinvi.build.environment`, `git archive` exact context), fallback `scripts/deploy-node.sh`(`PINVI_DOCKER_MANAGER_UNAVAILABLE=1` + fresh stack 한정), `infra/.env.prod`(gitignore)만 실제 도메인, Cloudflare Tunnel + WAF 한국 전용(`infra/cloudflare/waf-korea-only.md`, 선택 nginx GeoIP2 `infra/nginx/`).
- 시크릿: GitHub Actions secret 0개(`docs/runbooks/secrets.md`, `.github/workflows/README.md`), 외부 LLM API 키 미사용, CI 더미 값은 YAML 평문, 운영 시크릿은 `.env.prod`/docker-manager `.env`.

## 7. 외부 연동 (cross-repo)

| 대상 | 방식 | 근거 |
| --- | --- | --- |
| kor-travel-map | OpenAPI HTTP `:12701`(`/v1/features/*`, `/v1/public/*`, `/v1/service/*`, `/v1/admin/*`, `/v1/ops/*`); 클라이언트 `apps/api/app/clients/kor_travel_map*.py` 8종(httpx lifespan 재사용, 5xx→503 `FEATURE_SERVICE_UNAVAILABLE`); 헤더 `X-Kor-Travel-Map-Service-Token`/`X-Kor-Travel-Map-Api-Key`; 계약 스냅샷 vendoring + CI byte-equality + 일일 staleness; `contracts/*.json` provenance(release revision·sha256·capability generation) + M05 pair provenance; env `PINVI_KOR_TRAVEL_MAP_*` 40여 키 | `docs/kor-travel-map-integration.md`, `docs/integrations/kor-travel-map-rest-api.md`, `.github/workflows/api.yml`, `.env.example` |
| kor-travel-geo | v2 REST 직접(`/v2/geocode|reverse|search`, `/v2/regions/within-radius`), `key=<PINVI_VWORLD_API_KEY>` query, 클라이언트 `app/clients/kor_travel_geo.py`, 포트 12501(문서) | ADR-025/048/049, `docs/integrations/kor-travel-geo.md` |
| kor-travel-docker-manager | 운영 배포·포트 대역·M05 execution identity/pinset; Pinvi는 `ktdctl` 사용자 | ADR-040/042, `docs/runbooks/deploy.md`, `docs/tasks.md` |
| kor-travel-concierge | AI companion 호출 계약 소비 예정(v1.1+), `*.local.md`·push 전 감사 패턴 동일 | ADR-020, `docs/tasks-rule.md` §10, `AGENTS.md` |
| kor-travel-weather | 직접 의존·호출 **미확인**(코드·env에 weather 서비스 참조 없음; 날씨는 kor-travel-map `/v1/features/{id}/weather` 경유) | `docs/kor-travel-map-integration.md` §3 |
| `python-*-api` | `apps/etl`이 `python-kasi-api`(git main) 직접 의존; 그 외 provider 13종은 kor-travel-map 내부 책임 | `apps/etl/pyproject.toml`, `AGENTS.md` 의존 표 |
| `python-kraddr-base` | 문서 표에만 등장, 직접 의존 없음 | `AGENTS.md` |
| `maplibre-vworld-react` | `vworld-map-web@1.0.0`(`apps/web/vendor/*.tgz`), `vworld-map-core@1.0.0` + `vworld-map-rn@1.0.0`(`apps/mobile/vendor/*.tgz`), `file:` 핀, `transpilePackages`, Dockerfile `COPY --parents apps/*/vendor/`; peer `maplibre-gl ^5.24.0`, `zod ^4.4.3`; 라이선스 MIT(문서); 갱신 시 tarball + lockfile + provenance 기록 | ADR-044/046, `docs/integrations/maplibre-vworld.md` |
| `maplibre-vworld-js` / `maplibre-vworld` | ADR-046으로 의존 삭제(현재 package.json에 없음) | ADR-046 |
| 기타 | Kakao Local/Naver Local(서버측 display-only, ADR-054), Google OAuth(활성), Naver/Kakao OAuth(future), Resend(webhook Svix 서명), Telegram bot/outbox, RustFS S3(boto3 presigned), KASI(ETL), Sentry/Loki(문서) | `apps/api/app/clients/`, `docs/integrations/` |

## 8. 공통화 후보

| # | 영역 | 근거 경로 | 신뢰도 | 비고 |
| --- | --- | --- | --- | --- |
| 1 | Admin UI 프리미티브 26종(base-ui 오버레이 4 + 네이티브 재작성 22) | `apps/web/components/admin/ui/*` 헤더(“KTM …에서 이식(T-356)” + 색 토큰 치환표) | high | 이미 map→pinvi 이식이 발생. 치환표가 “구조는 공유, 색은 앱 소유”를 그대로 보여줌. 선행 보고서 §3.1과 일치 |
| 2 | Admin 앱 레벨 부품: filter-bar, pagination-bar, status-badge(+variants), stat-strip, section-card, empty-state, detail-list, json-viewer, copy-button, help-tip, skip link/헤더 밴드 | `apps/web/components/admin/{filter-bar,pagination-bar,status-badge,stat-strip,section-card,empty-state,detail-list,json-viewer,copy-button,admin-shell-parts}.tsx` | high | copy-button은 sonner 의존을 인라인 aria-live로 대체 — 토스트 의존성 없는 계약이 후보 |
| 3 | DataTable(853줄, TanStack table+virtual) + `AdminTable` 어댑터 계약 | `apps/web/components/admin/ui/data-table.tsx`, `components/admin/AdminTable.tsx` | medium | 서버 정렬 기본값(`manualSorting`)·`enableSortingRemoval` 3-state 함정·testid 계약·모바일 카드 등 공개 계약이 큼 — 후속 단계 |
| 4 | Admin 토큰 구조 규약(radius-control 6/panel 8, control 36/30px, rail 22rem, hairline 2종·컨트롤 경계 3:1, 불투명 status tint, brand tint≠danger tint, 7단 타이포 12/13.5/15/17/20/24/30) | `apps/web/app/globals.css` `@theme` + `[data-pv-surface='admin']` | high | 값·근거(대비 실측)가 주석에 남아 있어 규칙 문서화에 바로 쓸 수 있음. 브랜드 색은 앱 매핑 |
| 5 | `cn` = clsx + `extendTailwindMerge`(커스텀 그룹 등록) | `apps/web/lib/admin/cn.ts` | high | KTM `twMerge(clsx())`와 다른 이유가 주석에 있음 — common은 등록형이어야 함 |
| 6 | 접근성 레시피: `.focus-ring`(outline), reduced-motion 전역, 44px 터치(`min-h-touch`, coarse pointer 승격), 20px checkbox, `button{cursor:pointer}` 복원, forced-colors 폴백 | `apps/web/app/globals.css`, `components/ui/Button.tsx`, `docs/journal.md` T-356 | high | 규칙 산출물(UX 가이드) 후보 |
| 7 | Hallmark ESLint 가드(`no-restricted-syntax` 클래스 리터럴 정규식) + 경계 `no-restricted-imports` 패턴 | `apps/web/eslint.config.mjs` | medium | 규칙 세트는 앱 토큰 이름에 의존 — 공통은 “가드를 만드는 방식”과 기본 패턴(임의 z/px/shadow 금지) |
| 8 | 모달 계약(inert 격리·스택 최상단만 키 처리·포커스 복원 순서·busy 잠금·요청 수명 `status 0` 타임아웃) | `DESIGN.md` “모달 계약”, `apps/web/lib/useModalDialog.ts`, `packages/api-client/src/client.ts` | medium | admin(base-ui)과 사용자(수제) 두 구현이 공존 — 공통은 **계약 문서 + e2e(dialog-focus)** 우선, 구현은 후속 |
| 9 | API envelope·에러 코드·페이지네이션·좌표·시간 규약(`{data,meta}`, `{error:{code,message,details}}`, 표준 코드 12종, cursor, `If-Match`, `(lon,lat)`, ISO8601+09:00) + Python/Zod 쌍 | `apps/api/app/core/errors.py`, `app/schemas/envelope.py`, `packages/schemas/src/common.ts`, `docs/api/common.md`, `docs/architecture/api-contract.md` | high | OpenAPI 규칙 산출물의 직접 근거. `/v1` prefix 문서 불일치는 common에서 확정 필요 |
| 10 | `ApiClient` fetch wrapper(타임아웃 body 소비까지, `Retry-After`, 409 `VERSION_CONFLICT`, 401 훅, fetcher 주입) | `packages/api-client/src/client.ts`, `apps/web/tests/apiClient*.test.ts` | medium | 선행 보고서는 “앱에 유지” 권고 — 도메인 endpoint는 앱, **wrapper 코어**만 후보 |
| 11 | 미들웨어 세트: RequestId(`X-Request-Id`), SecurityHeaders, Prometheus(route 템플릿 라벨, `<svc>_api_` 접두, multiproc), RateLimit(Postgres fixed-window/memory, HMAC 키) | `apps/api/app/middleware/*.py`, `docs/api/common.md` §8/§11/§12 | medium | 메트릭 접두(`pinvi_api_` vs geo `ktg_`) 규칙 통일 후보 |
| 12 | structlog JSON 설정(`configure_logging`, KST iso, contextvars) | `apps/api/app/core/logging.py` | high | 작고 의존 적음 |
| 13 | health 규약(`/health`, `/health/db` 503 `DB_UNAVAILABLE`, 메트릭 제외) | `apps/api/app/api/v1/healthz.py`, `docs/api/health.md` | high | Docker HEALTHCHECK·blackbox 프로브와 결합 |
| 14 | pydantic-settings 규약(`<SVC>_*` 접두 필드, environment literal, `.env.example` 동기 테스트) | `apps/api/app/core/config.py`, `tests/unit/test_compose_delivers_declared_settings.py` | medium | 외부 소유 토큰 이름 예외(`KOR_TRAVEL_MAP_FEATURE_REQUEST_TOKEN`) 규칙 포함 |
| 15 | ruff/mypy 프로파일(select E,F,W,I,UP,B,RUF,S,ASYNC / line 100 / py312 / mypy strict + pydantic plugin / alembic 제외) | `apps/api/pyproject.toml`, `apps/etl/pyproject.toml` | high | 버전 일치 정책(ruff 0.16.x, mypy 2.3.x)의 기준점 |
| 16 | TS 기반 설정: `tsconfig.base.json`(strict + noUncheckedIndexedAccess + verbatimModuleSyntax), prettier(100/singleQuote), `.editorconfig`, `.gitattributes` LF | 루트 파일들 | high | 도구 규칙 산출물 |
| 17 | 테스트 하네스: testcontainers PostGIS + `alembic upgrade head` + TRUNCATE 격리 + 함수 스코프 엔진; pytest-split 샤딩; vitest 4 jsdom+RTL+oxc | `apps/api/tests/integration/conftest.py`, `.github/workflows/api.yml`, `apps/web/vitest.config.ts` | medium | geo/map 하네스와 비교 후 통일 |
| 18 | Alembic 규약(`file_template`, `version_table_schema`, advisory lock 직렬화, async commit, `x_extension`, 명명 `pk_/fk_/ix_/uq_/ck_/trg_`) | `apps/api/alembic.ini`, `alembic/env.py`, `docs/conventions/database.md` | medium | DB 규칙 산출물 |
| 19 | Dockerfile 패턴(digest 핀, provenance 라벨·검증 스크립트, `COPY --parents` workspace manifest, HEALTHCHECK, `npm ci`) | `apps/web/Dockerfile`, `apps/api/Dockerfile`, `scripts/validate-image-provenance.sh` | medium | docker-manager 규약과 함께 검토 |
| 20 | CI 패턴(aggregate gate, exact head SHA, lockfile integrity 가드, 이미지 기동 확인, 계약 핀 정합 + 일일 staleness) | `.github/workflows/{aggregate-ci,web,api}.yml`, `scripts/check-lockfile-integrity.mjs` | medium | OpenAPI drift 검사 규칙의 실물 예시(단 자체 API가 아니라 소비 계약 대상) |
| 21 | 문서·에이전트 규약(AGENTS/CLAUDE/SKILL 3층 + ADR-016 동기, `docs/decisions.md` ADR 포맷, journal/resume, tasks-rule T-ID, execplan, push 전 보안 감사, `*.local.md`, 에이전트별 worktree + CodeGraph, Telegram 완료 알림) | `AGENTS.md`, `docs/agent-guide.md`, `docs/tasks-rule.md`, `docs/runbooks/codegraph-worktrees.md` | high | concierge·map과 “동일 패턴”이라고 스스로 명시 — common 규칙의 정본화 대상 |
| 22 | 디자인 토큰 패키지 구조(TS 상수 + Tailwind preset 이중 export, motion/spacing/typography 분리, 웹·모바일 공용) | `packages/design-tokens/` | medium | 값(Airbnb/Rausch)은 Pinvi 소유; **구조와 의미 토큰 이름**만 후보 |
| 23 | PC/Mobile 분기 규칙(`useMobileWebLayout` 미디어쿼리 + data-attribute + unlayered override, 하단 탭바 높이 변수, `100dvh` 상수 금지) | `apps/web/lib/useMobileWebLayout.ts`, `globals.css`, `DESIGN.md` 앱 셸 계약 | medium | PC/Mobile Web 규칙 산출물 |
| 24 | vendored tarball `file:` 핀 + provenance 기록 방식(maplibre-vworld-react) | ADR-044/046, `apps/*/vendor/`, `apps/web/Dockerfile` | medium | 공유 라이브러리 배포 방식(npm 미발행) 정책 통일 대상 |
| 25 | 포트 대역 규칙(12xxx, docker-manager 정본) + `*.example.com` placeholder + 0 GitHub secret 정책 | ADR-042/047, `docs/runbooks/README.md` §2.2, `docs/runbooks/secrets.md` | high | 플랫폼 규칙 |
| 26 | Pretendard self-host 로딩 규칙 + 한글 줄바꿈(keep-all) + 시스템 mono 스택 | `apps/web/app/globals.css`, `DESIGN.md` Typography | high | 색 톤과 분리 가능한 타이포 규칙 |

## 9. 이 저장소 고유 차이·주의점

| 영역 | 내용 | 공통화 시 영향 |
| --- | --- | --- |
| 라이선스 | 루트 LICENSE 없음, README "비공개(사내)" vs AGENTS "공개 repo" 상충, api pyproject MIT 표기 | GPL-3.0 common으로 코드 추출 전 파일별 권리 확인 필요(선행 보고서 §9와 동일 결론) |
| Tailwind 이중 버전 | web v4.3.3(중첩) / mobile v3.4.19(root hoist, NativeWind 4) | 모바일 v4 전환은 NativeWind 5 안정화 선결; web Dockerfile 런타임 복사 전략이 중첩에 의존해 모바일 전환 시 함께 손봐야 함 |
| 토큰 정본 형식 | v3 preset `.cjs`를 v4 `@config`로 읽음; `@theme` 이전 시 웹/모바일 드리프트 경고 | common이 v4 CSS-first(`@theme`)를 표준으로 삼으면 Pinvi는 preset↔CSS 변수 이중 정본 문제를 먼저 풀어야 함 |
| Next 16 + webpack 강제 | ADR-066: Turbopack이 `vworld-map-web` 청크를 깨뜨림 | common 배포 패키지도 webpack/Turbopack 양쪽 검증 필요 |
| 두 UI 스택 공존 | 사용자 표면(수제 Button/Dialog/useModalDialog, 44px) vs admin(KTM 이식, base-ui 오버레이, 36px) — ESLint가 경계 강제 | common admin UI는 admin 표면에만 들어가야 하며 사용자 표면 규칙(Hallmark 잠금)과 충돌하지 않게 범위 CSS 필요(선행 보고서 §7.3와 일치) |
| base-ui 사용 범위 | overlay 4종만; button/input/checkbox는 네이티브 재작성(`render`/`asChild` 미제공, 기본 `type="button"`) | map(Base UI 전면)·geo(Radix)와 버튼 계약이 다름 — 선행 보고서 §3.3 재확인 |
| 색 토큰 | Airbnb Rausch/cta 단일 accent, OKLCH 병기, 다크 모드 없음, 마커 16색은 데이터용 | common 색 톤 규칙은 “의미 토큰 이름 + 대비 규칙”만; 값은 Pinvi 유지. 다크 모드 요구 시 Pinvi에 신규 부담 |
| 선언만 있는 의존 | next-intl·react-hook-form·@hookform/resolvers·zustand(web) 사용 0건; i18n 카탈로그 28키 | 버전 일치화 표에서 “미사용 선언”을 구분해야 오판을 막음 |
| OpenAPI | 자체 스펙 export/drift 없음; 대신 kor-travel-map 계약 스냅샷 byte-equality + staleness | common OpenAPI 규칙 도입 시 Pinvi는 export 파이프라인을 새로 만들어야 함; `/v1` prefix 문서 불일치 해소 필요 |
| 문서와 코드의 stale 지점 | frontend.md(Next 15/Tailwind 3.4/shadcn+Radix/public/maki/feature-flags), test-strategy(openapi.yml/security.yml/import-linter/coverage), workflows README(docker-images.yml), coding-style(Windows fallback), CLAUDE.md ADR 현황(056까지) vs decisions(067) | common 규칙을 참조할 때 코드를 정본으로 삼고 문서를 재검증해야 함 |
| 개발 환경 | Linux-only 정책이지만 MCP 설정 파일의 cwd/python 경로는 Windows | common 규칙(개발 환경 정본)에서 도구 설정 파일 템플릿까지 포함해야 실효 |
| 운영 복잡도 | M05/cache-target provenance, receipt, lease, 역할별 토큰 등 kor-travel-map 페어 운영 코드가 API·CI·compose 전반에 얽힘 | 공통화 대상 아님; common은 이 계약을 건드리지 않는 경계 명시 필요 |
| 모바일 | Expo SDK 57/RN 0.86.3/reanimated 4.6.0 루트 override, `expo` 루트 의존(hoist 사유), `expo.install.exclude` 의도적 편차 | 라이브러리 버전 일치 정책에서 RN 생태계는 별도 트랙(웹 정책과 강제 동기 불가) |
| 응답/좌표 규약 | `(lon,lat)` lng-first, `COORD_INPUT_BOUNDS`/`SERVICE_AREA_BOUNDS`, `coord_source device|map_pick` 동의 게이트(ADR-063/064) | geo/map과 좌표 규약이 같은지 common에서 대조 |
| 테스트 규모 | API unit 91 + integration 89 파일, web e2e 56 mock + 12 live, vitest 27, N150 격리 e2e 169건 통과 기록 | common 도입 PR은 이 게이트를 전부 통과해야 함(회귀 비용 큼) |
| 리뷰 관행 | “적대적 리뷰 2인 + 교차검증”이 관행이나 문서 규칙 아님 | common 리뷰 정책 명문화 시 Pinvi는 관행을 규칙으로 승격하면 됨 |

## 10. 버전 표

| 패키지 | 선언 범위 (위치) | 설치 버전 (lockfile) |
| --- | --- | --- |
| node | `engines.node >=20` (루트) / CI·Docker 22 | — |
| npm | `engines.npm >=11` (루트) / CI 11.19.1 | — |
| next | `16.3.3` (apps/web) | 16.3.3 |
| react / react-dom | `^19.0.0` (web), `^19.2.3` (mobile), override `19.2.6` | 19.2.6 |
| typescript | `^5.6.0` (루트·web·mobile·packages) | 5.9.3 |
| tailwindcss | `^4.3.3` (web) / `^3.4.15` (mobile) | 4.3.3 (apps/web 중첩) / 3.4.19 (루트) |
| @tailwindcss/postcss | `^4.3.3` (web) | 4.3.3 |
| @base-ui/react | `^1.7.0` (web) | 1.8.0 |
| radix-ui | 직접 선언 없음 | `@radix-ui/react-dialog` 1.1.23 등 전이 |
| shadcn | 없음 | 없음 |
| lucide-react | `^0.460.0` (web) | 0.460.0 |
| eslint / eslint-config-next / eslint-config-expo | `^9.16.0` / `16.3.3` / `~57.0.2` | 9.39.5 / 16.3.3 / 57.0.2 |
| vitest | `^4.1.10` (web, domain, schemas) | 4.1.11 |
| @playwright/test | `^1.56.0` (web) | 1.63.0 |
| @tanstack/react-query | `^5.59.0` (web, mobile) | 5.102.8 |
| @tanstack/react-table / react-virtual | `^8.20.5` / `^3.10.8` (web) | 8.21.3 / 3.14.10 |
| zod | `^4.4.3` (web, mobile, api-client, domain, schemas) | 4.5.4 (루트 hoist 3.25.76) |
| zustand | `^5.0.0` (web, mobile, state) | 5.0.15 |
| react-hook-form / @hookform/resolvers | `^7.54.0` / `^3.9.0` (web) | 7.87.0 / 3.10.0 |
| maplibre-gl | `^5.24.0` (web) | 5.24.0 |
| vworld-map-web / -core / -rn | `file:` 1.0.0 | 1.0.0 |
| next-intl | `^4.13.7` (web) | 4.14.2 |
| pretendard | `^1.3.9` (web) | 1.3.9 |
| class-variance-authority / clsx / tailwind-merge | `^0.7.1` / `^2.1.1` / `^3.6.0` (web) | 0.7.1 / 2.1.1 / 3.6.0 |
| prettier | `^3.3.3` (루트) | 3.9.6 |
| expo / expo-router / react-native | `~57.0.16` / `~57.0.16` / `0.86.3` | 57.0.20 / 57.0.19 / 0.86.3 |
| nativewind / @maplibre/maplibre-react-native | `^4.1.23` / `^11.3.4` | 4.2.6 / 11.3.8 |
| python | `>=3.12` (api, etl) / CI·Docker 3.12 | — |
| fastapi | `>=0.115` (api) | 0.141.1 (`apps/api/uv.lock`) |
| uvicorn | `>=0.32` | 0.52.3 |
| pydantic / pydantic-settings | `>=2.9` / `>=2.6` | 2.13.4 / 2.15.0 |
| sqlalchemy | `>=2.0.36` (api), `>=2.0` (etl) | 2.0.52 |
| alembic | `>=1.14` | 1.19.1 |
| asyncpg | `>=0.30` (api, etl) | 0.31.0 |
| psycopg | 없음 | 없음 |
| httpx / tenacity / structlog | `>=0.27` / `>=9.0` / `>=24.4` | 0.28.1 / 9.1.4 / 26.1.0 |
| prometheus-client | `>=0.22` | 0.26.0 |
| argon2-cffi / python-jose | `>=23.1` / `>=3.3` | 25.1.0 / 3.5.0 |
| ruff | `>=0.7` (api, etl) | 0.16.3 |
| mypy | `>=1.13` (api, etl) | 2.3.1 |
| pytest / testcontainers | `>=8.3` / `>=4.8` | 9.1.1 / 4.15.0 |
| dagster / dagster-webserver | `>=1.9` (etl) | 미확인 (etl lockfile 없음) |
| typer | 없음 | 없음 |

## 11. 미확인·열린 질문

1. `admin_router` 하위 라우터의 실제 prefix(`/admin/*`)는 문서로만 확인했고 `app/api/v1/admin/*.py` 각 파일의 `APIRouter(prefix=…)`는 열지 않았다(추정).
2. `Settings`의 `env_prefix`/`extra` 정책과 필드 전체(600행 이후)는 읽지 않았다 — `PINVI_*` 매핑은 필드명 기반 추정.
3. `@radix-ui/*` 전이 의존의 상위 패키지(어느 의존이 끌어오는지) 미확인.
4. `apps/etl` 설치 버전(dagster 등)은 lockfile이 없어 미확인.
5. `docs/integrations/{sentry,loki}.md`가 말하는 Sentry/Loki 실제 배선 코드(초기화 호출) 미확인 — env 키와 문서만 확인.
6. `packages/*`에 ESLint 설정이 없어 frontend.md §6.3의 `no-restricted-imports` 강제가 실제 동작하는지 미확인(루트 `npm run lint --workspaces --if-present`는 web/mobile만 실행).
7. `apps/web/e2e` live 스위트가 요구하는 N150 격리 스택 구성(`scripts/n150-playwright-runner.sh`, `docs/runbooks/live-mutating-e2e.md`)의 세부는 읽지 않았다.
8. `DESIGN.md` Exports의 `tokens.css`/W3C JSON/shadcn 변수 매핑이 실제 파일로 존재하는지 — 저장소에서 대응 파일을 찾지 못했으므로 문서 내 예시로 판단(추정).
9. `docs/architecture/frontend.md` §2의 `packages/feature-flags`, `packages/state/{selected-poi,map-viewport}-store.ts`, `packages/hooks/useOptimisticPatch.ts`는 실제 트리에 없다(사실) — 계획 잔재인지 폐기인지 미확인.
10. 모바일 `text-white` 사용과 웹 Hallmark 가드의 불일치가 의도된 예외인지(RN에는 `on-primary` 토큰이 preset에 있음) 미확인.
11. 선행 보고서(2026-09-05, pinvi `2396d65` 기준)와 본 조사(`9af25e5`) 사이에 `apps/web/package.json`·admin UI 구조의 변화는 없어 보이나(버전·파일 목록 일치) diff로 확인하지는 않았다.
12. `README.md`의 "비공개(사내)" 문구와 `AGENTS.md`의 "공개 repo" 문구 중 어느 쪽이 현재 GitHub 가시성인지 미확인.

## 12. 근거 파일 목록

조사에서 실제로 읽은 파일(저장소 상대 경로, 전부 `F:/dev/kor-travel-common-survey/pinvi/` 아래):

1. `README.md`
2. `AGENTS.md`
3. `CLAUDE.md`
4. `SKILL.md` (1~140행)
5. `DESIGN.md`
6. `CHANGELOG.md` (1~60행)
7. `package.json`, `package-lock.json`(스크립트로 버전 추출), `tsconfig.base.json`
8. `.env.example`(키 목록), `.prettierrc.json`, `.editorconfig`, `.gitignore`, `.dockerignore`, `.gitattributes`
9. `claude.json`, `codex.json`, `antigravity.json`, `.codex/config.toml`, `.gemini/mcp.json`, `.claude/settings.json`
10. `.hallmark/preflight.json`, `.hallmark/log.json`
11. `contracts/*.json` 4종(헤더)
12. `scripts/README.md`, `scripts/dev-up.sh`(1~60행), `scripts/check-lockfile-integrity.mjs`(1~30행)
13. `tests/security/csp_cors_rate_limit.py`(1~30행)
14. `.github/workflows/README.md`, `web.yml`, `api.yml`, `etl.yml`, `mobile.yml`, `aggregate-ci.yml`, `codex-pr-monitor.yml`, `codex-pr-review.yml`
15. `infra/docker-compose.yml`, `infra/docker-compose.app.yml`, `infra/.env.prod.example`(1~40행), `infra/n150/README.md`, `infra/nginx/README.md`
16. `apps/web/package.json`, `next.config.mjs`, `tsconfig.json`, `postcss.config.mjs`, `tailwind.config.ts`, `eslint.config.mjs`, `vitest.config.ts`, `playwright.config.ts`, `playwright.admin-live.config.ts`, `playwright.live-mutating.config.ts`, `Dockerfile`, `.gitignore`
17. `apps/web/app/globals.css`, `app/layout.tsx`, `app/(admin)/layout.tsx`, `app/(admin)/admin/layout.tsx`(1~80행 + grep), `app/(app)/layout.tsx`, `app/(auth)/layout.tsx`, `app/page.tsx`(1~40행), `app/(app)/map/page.tsx`(1~30행)
18. `apps/web/components/admin/ui/*`(전 파일 헤더 12행), `components/admin/*`(전 파일 헤더 10행), `components/ui/*`, `components/app/*`, `components/forms/*`, `components/feedback/*`(헤더), `components/ui/Button.tsx`(10~90행), `components/admin/AdminTable.tsx`(1~60행), `components/map/MapView.tsx`(1~50행), `components/map/vworldPrimitives.tsx`(1~60행), `components/app/AppShell.tsx`(grep)
19. `apps/web/lib/api.ts`, `lib/admin/cn.ts`, `lib/useMobileWebLayout.ts`, `tests/vitest.setup.ts`
20. `apps/mobile/package.json`, `app.json`, `eas.json`, `tailwind.config.js`, `global.css`, `babel.config.js`, `metro.config.js`, `nativewind-env.d.ts`, `eslint.config.js`, `tsconfig.json`, `README.md`(1~80행 + grep), `components/ui.tsx`, `app/_layout.tsx`, `lib/api.ts`(1~60행), `lib/tokens.ts`, `lib/config.ts`, `lib/storage.ts`
21. `packages/*/package.json` 7종, `packages/design-tokens/tailwind-preset.cjs`, `packages/design-tokens/src/{colors,index,motion,spacing,typography}.ts`, `packages/api-client/src/index.ts`, `packages/api-client/src/client.ts`(1~120행), `packages/schemas/src/common.ts`, `packages/schemas/src/index.ts`(1~40행), `packages/schemas/tsconfig.json`, `packages/hooks/tsconfig.json`, `packages/hooks/src/index.ts`, `packages/hooks/src/useUserLocation.ts`(1~40행), `packages/state/src/index.ts`, `packages/state/src/auth-store.ts`, `packages/i18n/src/index.ts`, `packages/i18n/messages/ko.json`(키), `packages/domain/src/marker.ts`(1~30행)
22. `apps/api/pyproject.toml`, `alembic.ini`, `alembic/env.py`(1~80행), `Dockerfile`, `.env.example`(1~40행), `uv.lock`(버전 grep)
23. `apps/api/app/main.py`, `app/core/config.py`(1~120행 + grep), `app/core/errors.py`, `app/core/logging.py`, `app/core/session_cookies.py`, `app/core/security.py`(1~80행), `app/core/rbac.py`(1~50행), `app/api/v1/__init__.py`, `app/api/v1/healthz.py`(1~60행), `app/api/v1/admin/__init__.py`(grep), `app/middleware/prometheus.py`(1~80행), `app/db/session.py`(1~60행), `app/schemas/envelope.py`, `app/mcp/server.py`(1~40행), `app/commands/*.py`(grep)
24. `apps/api/tests/conftest.py`, `tests/integration/conftest.py`(1~80행), `tests/unit`·`tests/integration`·`tests/contract` 목록
25. `apps/etl/pyproject.toml`, `Dockerfile`(1~40행), `pinvi/etl/definitions.py`, `pinvi/etl/schedules.py`(1~40행), `tests/` 목록
26. `docs/architecture/frontend.md`, `docs/architecture/api-contract.md`(1~60행), `docs/architecture/admin-rbac.md`(1~50행), `docs/architecture.md`(1~80행)
27. `docs/design/styleseed-rules.md`, `docs/design/marker-palette.md`(1~60행)
28. `docs/conventions/README.md`, `coding-style.md`, `testing.md`(1~150행), `database.md`(1~70행)
29. `docs/api/common.md`, `docs/api/README.md`(1~60행), `docs/api/health.md`(1~40행), `docs/api/admin.md`(grep)
30. `docs/kor-travel-map-integration.md`, `docs/integrations/maplibre-vworld.md`(1~70행), `docs/integrations/kor-travel-geo.md`(1~60행)
31. `docs/tasks.md`, `docs/tasks-rule.md`, `docs/tasks-done.md`(1~40행, 113~140행), `docs/resume.md`(1~60행), `docs/journal.md`(1~40행, 106~175행 + grep), `docs/decisions.md`(ADR 목록 grep, ADR-011/046/051/066 본문)
32. `docs/agent-guide.md`, `docs/agent-workflow.md`, `docs/dev-environment.md`(1~120행), `docs/test-strategy.md`, `docs/agent-failure-patterns.md`(1~30행)
33. `docs/runbooks/README.md`(1~50행), `deploy.md`(1~60행), `observability.md`(1~80행), `codegraph-worktrees.md`(1~60행), `pr-review-sprint4.md`(1~60행), `local-dev.md`(1~50행), `secrets.md`(1~40행), `admin.md`(1~40행)
34. `docs/sprints/README.md`(1~50행), `docs/spec/v8/03-frontend.md`(1~60행), `docs/spec/v8/04-admin.md`(1~40행), `docs/postgres-schema.md`(1~40행), `docs/audit/2026-06-06-doc-impl-audit.md`(1~20행)
35. 외부 참조: `F:/dev/kor-travel-geo-fixes/docs/kor-travel-common-library-review.md`(전문)
