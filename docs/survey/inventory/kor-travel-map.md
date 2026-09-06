# kor-travel-map 인벤토리

- 기준 커밋: `c494e227e010565be295de3f9670b2f7c8c20944` (2026-09-06 09:20 +0900, "docs: 게이트 독스트링에 남은 거짓 진술 둘을 정정한다 (#1165)") — `git -C F:/dev/kor-travel-common-survey/ktm-main rev-parse HEAD`로 확인
- 조사일: 2026-09-06
- 조사 경로: `F:/dev/kor-travel-common-survey/ktm-main` (읽기 전용, 파일 생성·수정 없음)
- 라이선스: `LICENSE` 첫 줄 `GNU GENERAL PUBLIC LICENSE / Version 3, 29 June 2007` (사실). `pyproject.toml` `license = { text = "GPL-3.0-or-later" }`. 단, npm workspace 패키지 `packages/map-marker-react/package.json`과 `packages/kor-travel-map-user-client/package.json`은 `"license": "MIT"`를 선언한다(map-marker-react README §라이선스: PinVi(proprietary)와 GPL 본체 양쪽에서 import 가능하도록 ADR-029로 의도적 분리).
- 저장소 규모: 커밋 2,590건(main), 최초 커밋 2026-05-24 (`git log --format=%ad`)
- 표기 규약: **사실** = 파일에서 직접 확인 / **후보** = 공통화 판단용 해석 / **추정** = 정황 근거 / **미확인** = 조사 범위에서 확인 못 함

## 1. 저장소 개요와 역할

1. `kor-travel-map`은 한국 공공 API(`python-*-api` 13종)와 형제 앱 `kor-travel-concierge`의 REST export를 단일 `Feature` 계약(place/event/notice/price/weather/route/area 7종)으로 정규화해 PostgreSQL/PostGIS에 저장하고 REST/OpenAPI로 제공하는 "독립 데이터 프로그램 + 내부 Python 라이브러리"다(`README.md` 1~14행, `AGENTS.md` §목표·§역할).
2. v1 구현은 `v1` 브랜치에 보존되고 main은 orphan v2 재시작이다(ADR-001, `CLAUDE.md` §2). 루트 `kor-travel-map-spec.docx`(77KB)가 v1 스펙 참고본이다.
3. 운영 모델은 ADR-045 이후 "Docker 독립 프로그램 + 독립 DB(`kor_travel_map`)/Dagster metadata DB(`kor_travel_map_dagster`) + OpenAPI 경계"다. PinVi 등 외부 소비자는 DB 직접 접근·Python import 없이 HTTP로만 호출한다(`AGENTS.md` §외부 경계).
4. 메인 Python 패키지 `src/kortravelmap/`은 FastAPI/Uvicorn 의존이 없는 async 라이브러리이고, REST backend는 별도 distribution `packages/kor-travel-map-api/`(`kortravelmap.api`), Dagster code location은 `packages/kor-travel-map-dagster/`(`kortravelmap.dagster`), admin UI는 `packages/kor-travel-map-admin/frontend/`가 소유한다(ADR-020/055, `pyproject.toml` import-linter forbidden contract).
5. 사용자는 내부 운영자다. admin UI는 "비전문가도 다룰 수 있는 데이터 수집·관리·백업·복원용 admin UI와 CLI"를 목표로 하며(`AGENTS.md` §목표 4), `design.md`는 "internal ops console"로 장르를 고정한다.
6. 형제 프로젝트는 `kor-travel-geo`(geocoding REST v2, 12501), `kor-travel-concierge`(feature 후보 provider, 12601), `kor-travel-docker-manager`(PostGIS/RustFS/관측 인프라 소유, prod n150 배포 lane), PinVi(feature consumer, 12801/12805)이며 cross-repo 계약 정본은 `docs/integration-map.md`(531행)다.
7. 문서 언어 정책은 "모든 Markdown/RST는 한국어, 식별자·URL·env·명령어는 원문" (`AGENTS.md` §문서 언어 정책)이고 vendored agent 원문(`.claude/`, `.agents/`, `.codex/`, `.opencode/`)만 ADR-059 예외다.
8. 개발 환경 정본은 Linux/WSL이다. Windows에서는 WSL `/mnt/f/dev/kor-travel-map-<agent>`에서 Linux `git`/`gh`/`codegraph`/Node/npm을 실행하고, Playwright e2e는 n150 Linux 우선·Windows 브라우저 fallback이다(`AGENTS.md` §개발 환경 정책, `docs/dev-environment.md` 1~11행).
9. 설계 우선순위는 "정확성·보안 → 단일 정본/설계적 우월성 → 단순성 → 확장성 → 실측 성능 → 호환성"이며(ADR-066~075, `CLAUDE.md` §1), 2026-07-26 사용자 지시로 서비스 전 단계에서 prod 보전·호환성은 비제약이다(`AGENTS.md` §목표).

## 2. 저장소 구조

최상위 트리(`ls -la`, 사실):

```text
.agents/ .claude/ .codex/ .gemini/ .opencode/   vendored agent/skill 원문 + MCP 설정
.github/workflows/                              ci · lint · openapi · frontend · docker-images · postgis-only
.pre-commit-config.yaml  .npmrc  .gitattributes .mcp.json  claude.json  antigravity.json  opencode.json
AGENTS.md  CLAUDE.md  SKILL.md  README.md  CHANGELOG.md(303KB)  LICENSE  kor-travel-map-spec.docx
alembic/ (baseline · versions · legacy_versions · retired_versions · env.py)  alembic.ini
contracts/ (cache-target-source-v1-golden.json · feature-alias-map-v1-golden.json · vnext/)
docker/ (api.Dockerfile · frontend.Dockerfile · dagster.Dockerfile · c7-playwright.Dockerfile · entrypoint·schema 스크립트)
docker-compose.yml(52KB) · .host.yml · .local-dev.yml · .external-db.yml · .external-infra.yml · .external-object-store.yml
docs/ (adr 57 · architecture 23 · archive 18 · etl 19 · reports 94 · runbooks 14 · sprints 6 · removal-manifests 1 + 루트 문서 30여 개)
live-e2e-backup-runner/ (backup.sh · restore.sh · swap.sh)
package.json (npm workspaces root) · package-lock.json(381KB, lockfileVersion 3)
packages/ (kor-travel-map-admin · kor-travel-map-api · kor-travel-map-dagster · kor-travel-map-user-client · map-marker-react)
pyproject.toml (메인 Python 패키지) · resources/ · scripts/(90여 개) · src/kortravelmap/ · tests/(unit 177 · integration 146 · lint 29 py)
```

| 패키지/앱 | 경로 | 종류 | 정체성 |
|---|---|---|---|
| kor-travel-map (메인) | `src/kortravelmap/` + 루트 `pyproject.toml` | Python (setuptools) | `import kortravelmap as ktm`, CLI `ktmctl`, env prefix `KOR_TRAVEL_MAP_*` |
| kor-travel-map-api | `packages/kor-travel-map-api/` | Python (setuptools) | `kortravelmap.api`, FastAPI, env prefix `KOR_TRAVEL_MAP_API_*`, `openapi{,.user,.service}.json` 커밋 |
| kor-travel-map-dagster | `packages/kor-travel-map-dagster/` | Python (setuptools) | `kortravelmap.dagster.definitions`, `[tool.dagster] module_name` |
| kor-travel-map-admin-frontend | `packages/kor-travel-map-admin/frontend/` | npm workspace (Next.js) | 포트 12705, `"private": true` |
| @kor-travel-map/map-marker-react | `packages/map-marker-react/` | npm workspace (TS 소스 share) | MIT, `"private": true`, registry 게시 금지(ADR-043) |
| @kor-travel-map/user-client | `packages/kor-travel-map-user-client/` | npm workspace (타입 산출물) | `openapi.user.json` → `src/types.ts`, 런타임 코드 없음 |

npm workspaces(루트 `package.json` `workspaces`): `packages/map-marker-react`, `packages/kor-travel-map-admin/frontend`, `packages/kor-travel-map-user-client` (사실). 루트 `package.json`은 "frontend workspace 해석 전용"이며 `dependencies`는 `@next/env@16.2.12` 하나뿐이다. Python 3개 패키지는 같은 저장소 editable install(`uv pip install -e .`, `-e packages/kor-travel-map-api`, `-e packages/kor-travel-map-dagster`)로 연결되고 Python lockfile(`uv.lock`/`poetry.lock`/`requirements*.txt`)은 **없다**(`ls` 확인, 사실).

## 3. 프론트엔드

### 3.1 kor-travel-map-admin-frontend (`packages/kor-travel-map-admin/frontend`)

**프레임워크/런타임** (`package.json`, 루트 `package.json`, `.npmrc`, 사실)

| 항목 | 선언 | 비고 |
|---|---|---|
| next | `16.2.12` (exact) | 루트 `overrides.next.postcss=8.5.23`, `sharp=0.35.3`; `scripts/verify-next-sharp.mjs`가 optimizer ABI smoke |
| react / react-dom | `^19.2.6` | lock 19.2.8 |
| typescript | `^5.9.3` | lock 5.9.3; `tsconfig.json` `strict: true`, `target ES2022`, `moduleResolution bundler`, `paths @/* → ./src/*` |
| node engines | `^22.22.2 \|\| ^24.15.0 \|\| >=26.0.0` | CI·Dockerfile은 `22.23.1` 고정 (`frontend.yml`, `docker/frontend.Dockerfile` digest 핀) |
| npm | `12.0.1` exact (`engines.npm`, `packageManager: npm@12.0.1`) | `.npmrc` `engine-strict=true`, `strict-allow-scripts=true`; 모든 CI/Dockerfile 명령이 `npx --yes npm@12.0.1 …` |
| 패키지 매니저/lockfile | npm, 루트 `package-lock.json` lockfileVersion 3 | 하위 워크스페이스 lockfile 없음 |
| allowScripts | `esbuild@0.28.1`, `unrs-resolver@1.12.2` | 루트 `package.json`; `tests/unit/test_frontend_dependency_security.py`가 정확히 이 집합을 잠금 |

**스타일** (사실)

- tailwindcss `^4.3.0` (lock 4.3.3), `@tailwindcss/postcss` `^4.3.0` (lock 4.3.3). `postcss.config.mjs`는 `@tailwindcss/postcss` 플러그인 하나. `tailwind.config.*` **없음**(`components.json` `tailwind.config: ""`).
- v4 CSS-first: `src/app/globals.css` 상단 `@import "tailwindcss"; @import "tw-animate-css";` → `@custom-variant` 6개(`data-checked`, `data-active`, `data-interactive`, `data-horizontal`, `data-vertical`, `dark (&:is(.dark *))`) → `@theme inline` → `@utility duration-fast/duration-base` → `:root` → `@layer base` → `.dark` → `@media (prefers-reduced-motion: reduce)`.
- 토큰 정본: `globals.css`의 `:root`/`.dark` + `@theme inline`이 곧 토큰 파일이며 별도 `tokens.css` 없음(`design.md` §Exports, `globals.css` 헤더 주석). `design.md` §Theme는 "토큰 NAME은 shadcn 이름 유지, 값은 OKLCH"로 명시.
  - 표면/잉크: `--surface-page` oklch(97.8% 0.003 128) · `--surface-subtle` · `--surface-muted`(= `--border`) · `--card` · `--text-primary` oklch(30% …) · `--text-secondary` · `--text-tertiary`(54%, AA 4.5:1 재측정으로 56%→54% 하향) · `--text-disabled` · `--icon-default`
  - hairline 2종: `--border`(장식, 대비 요건 없음) vs `--control-line` oklch(61% 0.012 145)(컨트롤 경계, WCAG 1.4.11 3:1 이상, `--input` alias)
  - brand: `--brand` oklch(51.4% 0.081 169) · `--brand-hover` · `--brand-tint` · `--brand-foreground`
  - status 4쌍: `--success/-tint`, `--warning/-tint`, `--info/-tint`, `--destructive/-tint`
  - focus/overlay/compare: `--focus` oklch(45% 0.09 169) · `--overlay`(유일한 alpha 색) · `--compare-a/b`
  - shadcn alias 유지: `--background/--foreground/--primary/--secondary/--muted/--accent/--popover/--ring/--input/--chart-1..5/--sidebar-*`
  - radius 2종: `--radius-control` 6px · `--radius-panel` 8px; `--radius-xs/sm/md`→control, `--radius-lg/xl/2xl/3xl/4xl`→panel로 collapse
  - 타입 스케일 7단계: `--text-2xs` 12 · `--text-xs` 13.5 · `--text-sm` 15(본문, `--text-base` alias) · `--text-md` 17 · `--text-lg` 20 · `--text-xl` 24 · `--text-2xl` 30 (px); line-height 토큰 동봉
  - 크기: `--control-h` 36px(`h-control`) · `--control-h-sm` 30px(`h-control-sm`) · `--rail` 22rem(`w-rail`) — `--spacing-control*`/`--container-rail`로 등록
  - 모션: `--ease-out` cubic-bezier(0.16,1,0.3,1) · `--ease-in` · `--duration-fast` 100ms · `--duration-base` 150ms (`--dur-*`는 alias); `--default-transition-duration/timing-function` 재정의
  - 그림자: `--shadow-elevated`(popover) · `--shadow-modal`(dialog) — rest 상태 그림자 없음; `--shadow-card*`는 정의만
  - z-index 토큰: **없음**(사실; skip link만 `focus:z-50` 유틸 직접 사용, `admin-shell.tsx:224`)
- 라이트/다크: `.dark` 블록이 같은 이름으로 dark 값을 정의하지만 **토글은 마운트되지 않음**(`design.md` §Theme "no toggle mounted"; `dark:` 유틸 사용 1건).
- 폰트: 본문/UI = Pretendard Variable — `pretendard@1.3.9` npm 패키지의 `dist/web/variable/pretendardvariable-dynamic-subset.css`를 `layout.tsx`에서 import; mono = Geist Mono `next/font/google` (`--font-geist-mono`). `--font-sans` 스택: `var(--font-pretendard,"Pretendard Variable"), Pretendard, "Noto Sans KR", "Apple SD Gothic Neo", "Malgun Gothic", system-ui, sans-serif`. Geist Sans는 제거됨(2026-08-18 hallmark audit이 "한글 전용 서체 없음"을 지적한 뒤 정정).
- 아이콘: `lucide-react` `^1.17.0` (lock 1.27.0). 애니메이션: `tw-animate-css` `^1.4.0`. `class-variance-authority` 0.7.1, `clsx` 2.1.1, `tailwind-merge` 3.6.0 (`src/lib/utils.ts` `cn`).

**UI 프리미티브** (사실)

- `@base-ui/react` `^1.5.0` (lock 1.6.0). radix-ui **없음**. 사용 서브패스: `alert-dialog`, `button`, `checkbox`, `dialog`, `input`, `merge-props`, `use-render`, `popover`, `separator`, `tabs`, `tooltip`.
- shadcn CLI는 **설치하지 않음** — `test_frontend_dependency_security.py`가 `"shadcn" not in devDependencies`를 단언하고, `@import "shadcn/tailwind.css"` 부재와 "사용 중인 named data-variant를 저장소가 직접 소유"(`test_frontend_owns_every_named_shadcn_css_token_it_uses`)를 잠근다.
- `components.json`: `$schema https://ui.shadcn.com/schema.json`, `style: "base-nova"`, `rsc: true`, `tsx: true`, `tailwind.css: src/app/globals.css`, `baseColor: neutral`, `cssVariables: true`, `prefix: ""`, `iconLibrary: lucide`, `rtl: false`, `aliases {components:@/components, utils:@/lib/utils, ui:@/components/ui, lib:@/lib, hooks:@/hooks}`, `menuColor: default`, `menuAccent: subtle`, `registries: {}`.

**컴포넌트 인벤토리** (`git ls-files`, 사실 — 모든 파일 첫 줄에 `Hallmark · genre: editorial-utilitarian · macrostructure: Rail-Workbench · design-system: design.md · designed-as-app` 스탬프)

`src/components/ui/` 30개(테스트 제외): `alert-dialog.tsx`, `alert.tsx`, `badge.tsx` + `badge-variants.ts`, `breadcrumb.tsx`, `button.tsx` + `button-variants.ts`, `card.tsx`, `checkbox.tsx`, `data-table.tsx`(799행, TanStack Table v8 + Virtual, `"use no memo"` 2곳), `dialog.tsx`, `field.tsx` + `field-variants.ts`, `form-field-input.tsx`, `form-field-shared.ts`, `form-field.ts`, `form-select.tsx`, `form-textarea.tsx`, `input.tsx`, `native-select.tsx`, `native-select-option.tsx`, `popover.tsx`, `separator.tsx`, `skeleton.tsx`, `sonner.tsx`, `table.tsx`, `tabs.tsx` + `tabs-variants.ts`, `textarea.tsx`, `tooltip.tsx`. 테스트: `data-table.test.tsx`, `form-field-input.test.tsx`.

`src/components/` 앱 레벨 공유 26개(테스트 제외): `admin-shell.tsx`(510행, Rail-Workbench 셸·skip link·collapsible rail), `admin-region-autosearch.tsx`, `app-error-panel.tsx`, `confirm-dialog.tsx`(`useConfirm` provider), `copy-button.tsx`, `detail-list.tsx`, `empty-state.tsx`, `entity-link.tsx`, `feature-associations.tsx`, `feature-detail-view.tsx`(1,406행), `feature-kind-detail-panel.tsx`, `feature-price-panel.tsx`, `feature-state-badges.tsx`, `feature-weather-panel.tsx`, `filter-bar.tsx`, `help-tip.tsx`, `json-viewer.tsx`, `login-form.tsx`, `multi-filter-combobox.tsx`, `pagination-bar.tsx`(290행, cursor/offset pager), `section-card.tsx`, `selectable-row.tsx`(roving tabindex), `stat-strip.tsx`, `status-badge.tsx` + `status-badge-variants.ts`, `vworld-map-view.tsx`(1,858행, maplibre-gl 직접 사용).

출처 주석: `src/lib/vworld-style.ts` 3행 "`digitie/maplibre-vworld-react` a7cb0f8의 vworld-map-core/web 경계를 admin UI에 필요한 범위만 포팅" (사실). `data-table.tsx` 헤더는 "admin/ops UI의 모든 테이블이 본 컴포넌트로 통일(2026-06-17), 기본 `manualSorting=true`(서버 정렬)"을 명시. Hallmark 스탬프 외 shadcn 원본 출처 주석은 없음.

**상태/데이터** (사실)

- `@tanstack/react-query` `^5.100.14` (lock 5.101.4): `src/providers/query-client-provider.tsx`가 `refetchOnWindowFocus: false`, `retry: 1`, `staleTime: 0` 기본. `useQuery/useMutation` 사용 파일 22개.
- `zustand` `^5.0.14`: `src/state/map.ts`(viewport/featureViewMode/selectedFeatureId/activeFeatureKinds/activeCategoryCodes).
- `react-hook-form`, `zod`, `@hookform/resolvers`: frontend에 **없음** — `test_frontend_dependency_security.py`가 부재를 단언. 폼은 controlled `useState` + `src/lib/form-validation.ts`(`FieldRule`, `firstErrorField`) (사실). zod 4.4.3은 `map-marker-react`의 peer/devDependency로만 존재.
- API 타입 생성: `openapi-typescript` `^7.13.0` → `gen:types`: `../../kor-travel-map-api/openapi.json -o src/api/types.ts`; `gen:types:check` CI drift gate. `src/api/*.ts` 도메인 모듈 20여 개.
- fetch 래퍼 `src/api/client.ts`: `BASE_URL = "/api/proxy"`, `credentials: "same-origin"`, `ApiClientError{status,path,problem: ProblemDetail|null, retryAfterSeconds}`, `getJson/postJson/putJson/patchJson/deleteJson/postFormData/pathWithQuery`, `Idempotency-Key` sessionStorage 보관(`withIdempotencyKey`, `withDomainIdempotencySubmission`, fingerprint), 로그아웃 이벤트 구독(`subscribeAdminLogout`).

**인증 경계** (사실)

| 계층 | 파일 | 내용 |
|---|---|---|
| Next middleware | `middleware.ts` | 공개 경로(`/login`, `/api/build-info`, `/api/auth/*`, `/_next/*`) 외 전부 세션 검증; `/api/*`는 `401 {error:"AUTH_REQUIRED"}`, 페이지는 `/login?next=` redirect |
| 세션 | `src/lib/auth.ts` | 쿠키 `ktm_admin_session`, TTL 8h, `httpOnly` + `sameSite: "strict"`, HMAC 서명 payload `{aud:"kor-travel-map-admin", exp, fp, iat, sid(32B), sub, v:1}`, secret ≥32자(`KOR_TRAVEL_MAP_UI_SESSION_SECRET`), 비밀번호 `pbkdf2_sha256` 310,000회(`KOR_TRAVEL_MAP_UI_ADMIN_PASSWORD_HASH`), 로그인 실패 5회/10분 rate limit, 프로세스 메모리 revoked-session Map, `requestHasSameOrigin` Origin 화이트리스트 CSRF 방어, `KOR_TRAVEL_MAP_UI_TRUST_PROXY_HEADERS` |
| 로그인/로그아웃 | `src/app/api/auth/login/route.ts`, `logout/route.ts` | JSON POST, 403 INVALID_ORIGIN / 429 RATE_LIMITED + Retry-After / 503 AUTH_MISCONFIGURED, `src/lib/auth-audit.ts`로 감사 이벤트 기록 |
| ops live ticket | `src/app/api/auth/live-ticket/route.ts` | WS `/v1/ops/live`용 60초 HMAC ticket, subprotocol로만 전달(README §환경변수) |
| BFF proxy | `src/app/api/proxy/[...path]/route.ts` + `src/lib/proxy.ts` | 내부 base `KOR_TRAVEL_MAP_API_INTERNAL_URL`(기본 127.0.0.1:12701); 전달 허용 요청 헤더 `accept/content-type/idempotency-key/if-match/user-agent`; 백엔드 신원 전달 `X-Kor-Travel-Map-Actor`(로그인 username) + `X-Kor-Travel-Map-Admin-Proxy-Secret`(`KOR_TRAVEL_MAP_ADMIN_PROXY_SECRET`); 수동 Feature 생성 경로에만 `X-Kor-Travel-Map-Admin-Feature-Create-Token`; 응답 헤더 전달 `content-type/content-disposition/etag/idempotency-replayed/location/retry-after/x-request-id`; 오류는 RFC7807 `application/problem+json` |
| geo BFF | `src/app/api/geo/[...path]/route.ts` | `KOR_TRAVEL_GEO_API_KEY`(32자 영숫자 정규식)를 `X-KTG-API-Key` 헤더로 전송, 미구성 시 503 `GEO_API_KEY_NOT_CONFIGURED` |
| 빌드 정보 | `src/app/api/build-info/route.ts` | `src/generated/frontend-build-info.ts`(Dockerfile이 `scripts/frontend-source-digest.mjs`로 생성) |

백엔드 측 대응: `kortravelmap.api.auth.require_admin_frontend`가 proxy secret + actor + trusted CIDR(`KOR_TRAVEL_MAP_API_ADMIN_TRUSTED_PROXY_CIDRS`)를 검증한다(§4.2).

**라우팅/화면 목록** (`git ls-files src/app`, 사실): `page.tsx` 24개 = admin 14(`/admin/backups`, `/admin/curations/candidates`, `/admin/dedup-reviews`, `/admin/enrichment-reviews`, `/admin/features`, `/admin/features/curated`, `/admin/features/dedup-reviews`, `/admin/features/enrichment-reviews`, `/admin/features/new`, `/admin/files`, `/admin/issues`, `/admin/offline-uploads`, `/admin/poi-cache-targets`, `/admin/settings`) + ops 5(`/ops/cache-target-streams`, `/ops/consistency`, `/ops/datasets`, `/ops/logs`, `/ops/pipeline`) + 공용 5(`/`, `/features`, `/features/[featureId]`, `/curated-features`, `/login`). route handler 6개. 사용자(공개) 화면은 없음 — 전부 로그인 뒤 운영자 화면(`/login`만 공개). `error.tsx`/`global-error.tsx` 존재. 각 화면 ↔ 백엔드 API 대응표는 frontend `README.md` §주요 페이지(255~282행).

**반응형/모바일** (사실/추정)

- Tailwind 기본 breakpoint만 사용(커스텀 `--breakpoint-*` 없음). `src/` 내 사용 횟수: `lg:` 69, `md:` 29, `xl:` 23, `sm:` 7, `2xl:`/`max-*:` 0.
- `admin-shell.tsx`: `lg` 미만은 상단 가로 스크롤 nav(`overflow-x-auto`), `lg` 이상은 좌측 rail(`lg:grid-cols-[16rem_minmax(0,1fr)]`, collapsed `4rem`, `lg:sticky lg:h-dvh`). 헤더 밴드는 `md:flex-row`.
- 모바일 전용 처리·터치 밀도(`pointer-coarse`, `touch-*`)·PC/Mobile 분기 코드는 **없음**(grep 0건). `docs/architecture/admin-frontend-design-rules.md`가 "데스크톱 우선 운영 콘솔"을 명시. → PC 전용 admin으로 판단(추정).

**i18n / 접근성 / focus / reduced-motion** (사실)

- i18n 라이브러리 없음. `<html lang="ko">`, 한국어 카피, 숫자 `Intl.NumberFormat("ko-KR")`/`toLocaleString("ko-KR")`. 상태 문구 정본은 `src/lib/status-label.ts` 하나(`statusLabel()`, `toneFor()`, 134키; `status-label.test.ts`가 "같은 라벨=같은 tone" 회귀 잠금).
- 접근성: `aria-label` 227 · `aria-hidden` 71 · `aria-busy` 40 · `aria-disabled` 23 · `aria-live` 17 · `aria-sort` 10 등; skip link(`sr-only focus:not-sr-only`)→`<main tabIndex={-1}>`; 가상화 테이블은 `role=table/row/columnheader/cell` + `aria-rowcount/rowindex` 명시; eslint `jsx-a11y-x` 6개 규칙 warn.
- focus 레시피 1종: `globals.css @layer base` `:focus-visible { outline: 2px solid var(--focus); outline-offset: 2px }` 단독 발행. 컴포넌트는 `focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-focus`(button/badge)만 재선언. 링을 끄는 자리는 닫힌 목록 4개(`DialogContent`, `AlertDialogContent`, `PopoverContent`, `AdminShell <main>`) + 대체 링 1개(`MultiFilterCombobox` 안쪽 Input)이며 수단은 `focus-visible:outline-0`만 허용, `outline-none` 전면 금지(v4 `--tw-outline-style` 오염 근거).
- reduced-motion: 전역 `@media (prefers-reduced-motion: reduce)`에서 모든 animation/transition 0.01ms, `.transition-opacity`/`[data-motion="crossfade"]`만 150ms opacity 유지, 로딩 스피너(`[data-slot="button-spinner"] svg`, Sonner loading)는 1.6s로 계속 회전, Skeleton은 `motion-reduce:animate-none`.
- 전환 규칙: `transition-all`/`transition-colors`/맨 `transition` 금지, 항상 `transition-[color,background-color,border-color,…]` 열거(v4가 `outline-color`를 전환 목록에 넣어 링이 페이드되는 문제).

**테스트·품질** (사실)

| 도구 | 설정 | 내용 |
|---|---|---|
| vitest `^4.1.7`(4.1.10) | `vitest.config.ts` | `@vitejs/plugin-react` + `vite-tsconfig-paths`, 기본 node env, 컴포넌트 테스트는 `// @vitest-environment jsdom` 프래그마; `jsdom` 25.0.1, `@testing-library/react` 16.3.2; 테스트 파일 42개(`src/**/*.test.*` + `tests/`) |
| Playwright `1.60.0`(exact) | `playwright.config.ts`, `playwright.live.config.ts`, `playwright.cache-target-streams.live.config.ts` | mocked suite 30 spec(`e2e/*.spec.ts`, `page.route` 가로채기, deny proxy 격리, `timezoneId: "UTC"`, storageState auth setup) + live suite 29 spec(`e2e/live/*.live.spec.ts`, prod 실데이터); `webServer` 없음(서버는 WSL/n150 외부 기동); c7 Playwright 이미지 `mcr.microsoft.com/playwright:v1.60.0-noble@sha256:…` |
| react-doctor `^0.9.1` | `doctor.config.json` | `react-doctor --scope full --no-score --no-telemetry --no-respect-inline-disables --blocking warning .`; 예외 3파일(`src/api/live.ts` effect 규칙 2, `datasets-client.tsx` no-event-handler, `data-table.tsx` redundant-roles 2) — `scripts/verify-react-doctor-config.mjs`가 설정 파일 내용·금지 우회 파일(`.oxlintignore`, `knip.json` 등)·`.gitattributes`/`.gitignore` exact 내용·doctor 명령까지 바이트 단위로 잠금 |
| eslint `^10.8.0` flat | `eslint.config.mjs` | `typescript-eslint` 8.65.0 recommended, `eslint-plugin-import-x` 4.17.1(+ `eslint-import-resolver-typescript`), `eslint-plugin-react-x` 5.18.0 / `react-dom` 5.18.0 recommended(hooks 중복 규칙 9개 off), `eslint-plugin-jsx-a11y-x` 0.2.0, `eslint-plugin-react-hooks` 7.1.1 `recommended-latest`(React Compiler 규칙 포함, `incompatible-library` off는 `data-table.tsx` 1파일만), `@next/eslint-plugin-next` recommended + core-web-vitals; `eslint-config-next` 미사용(테스트가 부재 단언); `lint: eslint . --max-warnings 0` |
| ESLint 계약 검증 | `scripts/verify-frontend-eslint-config.mjs` | effective config severity 단언, `"use no memo"` 정확히 2곳(DataTable/VirtualizedTable), inline suppression 0건, lint 대상 파일 집합 = `src/**`+`e2e/**` 전수 |
| type-check | `package.json` | `tsc --noEmit && tsc -p e2e/tsconfig.json --noEmit && tsc -p tsconfig.tooling.json --noEmit` — `tsconfig.tooling.json`은 playwright/vitest config 자체를 검사(2026-08-12 `parsedBaseURL` ReferenceError 사고 기록) |
| npm 보안 | 루트 `package.json` | `audit:high`(`--omit=dev`, 차단), `audit:dev`(비차단), `verify:npm-tree`(npm 12.0.1 강제 + `npm ls --all` problems 0), `postinstall` `patch-redocly-openapi-core.mjs`(@redocly/openapi-core 1.34.17 minimatch API vendor patch) |
| Python 측 게이트 | `tests/unit/test_frontend_dependency_security.py` | `package.json`·`package-lock.json`·Dockerfile·workflow·`.npmrc`의 핀/overrides/명령 순서를 pytest로 단언(224행) |

**빌드/배포** (사실)

- `next.config.ts`: `reactStrictMode`, `allowedDevOrigins`(127.0.0.1/localhost + env), `turbopack.root = ../../..`, `output: "standalone"`, `outputFileTracingRoot`, `transpilePackages: ["@kor-travel-map/map-marker-react"]`, `productionBrowserSourceMaps: false`, `poweredByHeader: false`. basePath 없음(옵션 A standalone).
- `docker/frontend.Dockerfile`: 3-stage(deps/builder/runner), `node:22.23.1-bookworm-slim@sha256:…` 핀, `npx --yes npm@12.0.1 ci --workspaces --include=optional` → `verify:npm-tree` → `verify:next-sharp`, `NEXT_PUBLIC_*` build ARG, `frontend-source-digest.mjs`로 build-info 생성, standalone 출력, non-root `nextjs`, `PORT=12705`, `HOSTNAME=0.0.0.0`.
- 스크립트: `dev: next dev --port 12705 --hostname 127.0.0.1`, `start: next start --port 12705 --hostname 127.0.0.1`.
- `.env.example`: `NEXT_PUBLIC_VWORLD_API_KEY`(geo의 `KOR_TRAVEL_GEO_VWORLD_API_KEY`와 동일 값 공유, 별도 발급 금지), `NEXT_PUBLIC_KOR_TRAVEL_MAP_API`, `NEXT_PUBLIC_KOR_TRAVEL_MAP_DAGSTER_URL`, `NEXT_PUBLIC_KOR_TRAVEL_GEO_BASE_URL`, server-only `KOR_TRAVEL_GEO_API_KEY`, `KOR_TRAVEL_MAP_API_INTERNAL_URL`, `KOR_TRAVEL_MAP_ADMIN_PROXY_SECRET`, `KOR_TRAVEL_MAP_ADMIN_FEATURE_CREATE_TOKEN`, `KOR_TRAVEL_MAP_UI_ADMIN_USERNAME/PASSWORD_HASH/SESSION_SECRET/TRUST_PROXY_HEADERS`, `NEXT_PUBLIC_DISABLE_OPS_LIVE`.

**디자인 문서** (사실)

| 문서 | 성격 | 핵심 |
|---|---|---|
| `frontend/design.md` (27.5KB) | **잠금(locked) 디자인 시스템 정본**. `hallmark audit` 2026-08-18 → `hallmark redesign` 산출. 모든 restyled 파일에 스탬프 강제 | 장르 `editorial-utilitarian`; macrostructure `Rail-Workbench`(rail → 헤더 밴드 → FilterBar → DataTable → inspector rail) + 변형 knob 6종(list/detail/map/form/dashboard/login); 금지: card-in-card, icon-tile KPI grid, 떠 있는 그림자 헤더 카드, dashed-border 가운데 정렬 empty state, glass/gradient/blob, emoji, 비대화 컨테이너 hover elevation; 테마(OKLCH, 대비 실측치 표기), hairline 2종, focus 규칙, States(흐림은 자식 래퍼에만 `opacity-55`), Microinteractions(silent success, `useConfirm` 동사 라벨, 트리거 버튼 `loading`), CTA voice(variant별 경계 규칙), Status colour semantics(5 tone), Copy(`—` null glyph, `·` 구분, 값 없으면 단위도 제거), **금지 패턴 grep 게이트 7종**: ①`transition-all`/`transition-colors`/맨 `transition` ②`text-[Npx]` ③`rounded-(2xl\|3xl\|4xl\|[)` ④raw `#hex`/`oklch(`/`rgb(` ⑤팔레트 alpha `bg-x/NN` ⑥`outline-none` ⑦`aria-disabled:opacity-`/`aria-busy:opacity-`(백틱 주석 인용은 제외: ``rg -n -- '<패턴>' src \| rg -v -- '`<패턴>`'``) |
| `docs/architecture/admin-frontend-design-rules.md` | 2026-06-18 StyleSeed 기반 규칙(구) | "정보는 카드 안에 둔다", KPI `36px:18px`, `space-y-6` 리듬 — `design.md`와 **충돌**(§9 참조) |
| `docs/reports/hallmark-audit-admin-frontend-2026-08-18.md` | 감사 원문 | 29 primitives·27 routes 대상, C1 focus ring, C2 `--info` blue-500 3.7:1 등 |
| `docs/runbooks/admin-ui-screen-checklist.md` | 화면별 점검 | 16 route 필터/cursor/빈·에러/kill-switch/a11y/e2e 매트릭스 |

금지 패턴 grep 게이트의 **자동화 스크립트는 tracked 파일에서 발견하지 못했다**(`git grep -E 'rounded-\(2xl|금지 패턴' -- ':!*.md' ':!*.css'`는 패턴 이름을 주석으로 인용한 컴포넌트 4개만 매칭). `design.md`는 "스크립트는 이 목록을 따른다"고 쓰지만 CI workflow/`scripts/`/`tests/lint`에 해당 게이트는 없다 → 미확인(수동 `rg` 절차로 추정).

## 4. 백엔드

### 4.1 kor-travel-map (메인 라이브러리, `src/kortravelmap/` + 루트 `pyproject.toml`)

- Python `>=3.11`(classifiers 3.11/3.12/3.13, CI matrix 동일). 빌드 `setuptools>=68` + wheel, `package-dir {"" = "src"}`, `include = ["kortravelmap*"]`, `namespaces = true`, `py.typed`. lockfile **없음**(`uv venv && uv pip install -e ".[dev,geo,providers]"` 권장, README §빠른 시작).
- 의존 선언: `pydantic>=2.7`, `pydantic-settings>=2.4`, `sqlalchemy>=2.0`, `geoalchemy2>=0.15`, `asyncpg>=0.29`, `psycopg[binary,pool]>=3.2`, `shapely>=2.0`, `pyproj>=3.6`, `alembic>=1.19.1,<1.20`(named CHECK by-name 비교 의존), `jellyfish>=1.0`, `boto3>=1.34`. extras: `dev`(pytest, pytest-asyncio, pytest-cov, hypothesis, jsonschema, markdown-it-py, ruff, mypy, import-linter, pre-commit, testcontainers[postgres], vcrpy, coverage, httpx), `geo`(geopandas, `gdal==3.8.4`), `providers`(python-*-api 13종 git+sha 핀). `structlog`, `typer`, `tenacity`는 **선언에 없음**(사실; `settings.py:535` 필드 설명에 "structlog 로깅 레벨" 문구만 존재 → §11).
- 계층/구성: `category → dto → core → infra → geocoding → providers → client → cli` 단방향(import-linter `layers` contract). 루트 모듈: `settings.py`(`KorTravelMapSettings`, `env_prefix="KOR_TRAVEL_MAP_"`, `log_format: json|console`), `client.py`(`AsyncKorTravelMapClient`, async-only ADR-002), `geocoding.py`(geo v2 호출, `X-KTG-API-Key` 헤더 951/1035행), `curation_import*.py`, `enrichment.py`, `mois.py`, `offline_upload.py`.
- 에러 envelope: 메인 DTO는 `data/meta/error` 래핑 없음(SKILL §4 7번) — 래핑은 API 패키지 책임.
- 관측성: 표준 `logging` (API `app.py` `logging.getLogger`); json/console 포맷 설정값만 존재. 메트릭은 API 패키지(§4.2).
- DB: PostgreSQL + PostGIS(`postgis/postgis` digest 핀 compose), schema `feature`/`provider_sync`/`ops`, PostGIS extension은 `x_extension` schema(ADR-008), 좌표 `coord`(4326) + `coord_5179`(meter, 반경 검색 전용, `ST_Transform` 술어 금지), ORM은 매핑만·쿼리는 raw SQL `text()`(ADR-004), `psycopg.copy` 30k 파라미터 안전 마진. Alembic: `alembic/`(`baseline/` catalog·sha256·SQL 계약 10파일, `versions/` 8파일 — `300_schema_baseline.py`, `301_m03_…`, `302_m03_…`, `303_m05_…` 등 `NNN_<slug>.py` 명명, `legacy_versions/`, `retired_versions/`), `alembic.ini` `script_location = alembic`. fresh DB는 compose `--profile fresh-init run --rm db-application-schema-fresh-300` one-shot.
- 백업/복원: `scripts/docker-backup.sh`/`docker-restore*.sh`, `live-e2e-backup-runner/`, `docs/backup-restore.md`; `300` baseline부터 restore/hot-swap/PITR 비지원, admin 표면은 artifact 조회·생성만(`docs/deploy.md` 3~6행).
- CLI: `ktmctl` = `kortravelmap.cli.main:main`, **argparse**(typer 아님) 서브커맨드 `status`, `consistency-report`, `import mois`, `dedup-merge`; write/bulk/restore 계열은 `cli/mutex.py` `pg_try_advisory_lock`(ADR-039).
- 테스트: `tests/unit`(177 py), `tests/integration`(146 py, testcontainers PostGIS), `tests/lint`(29 py — `test_import_linter.py`, `test_package_layout.py`, `test_task_ledger_conventions.py`, `test_no_control_characters_in_source.py`, alembic/SQL 계약 검사 다수). pytest `asyncio_mode=auto`, session loop scope, `addopts -ra --strict-markers --strict-config`, markers 7종(unit/integration/e2e/slow/fixture_replay/live/perf_gate), `filterwarnings = error`(예외 3건). coverage `source=src/kortravelmap`, `branch=true`, `fail_under=80`(ADR-032, 실측 94.12% 주석). ruff `line-length=100`, `target py311`, `select = ["E","F","I","UP","B","ASYNC","PIE","PT","RET","SIM","TID"]`. mypy `strict=true`, `warn_unused_ignores`, `plugins=["pydantic.mypy"]`, `mypy_path`에 api/dagster src 포함. import-linter 4 contracts(layers, no fastapi/uvicorn/starlette, no cache libs, no kafka/streaming).

### 4.2 kor-travel-map-api (`packages/kor-travel-map-api`)

- Python `>=3.11`, setuptools, `include = ["kortravelmap.api*"]`, version `0.2.0-dev`(메인과 lockstep). lockfile 없음.
- 의존: `kor-travel-map`, `fastapi>=0.115`, `python-multipart>=0.0.20`, `starlette>=0.40,<1.0`(TestClient httpx 0.x 호환 이유 주석), `uvicorn[standard]>=0.30`, `pydantic>=2.7`, `pydantic-settings>=2.4`, `httpx>=0.27,<1.0`, `prometheus-client>=0.20`. dev: pytest, pytest-asyncio, httpx. ruff/mypy 설정은 메인과 동일.
- 앱 구성: `app.py`(1,400행) `create_app()` 팩토리 + 모듈 레벨 `app`; `lifespan`에서 DB 권한 경계 검증(`assert_runtime_db_privilege_boundary`)·route policy 배선 검증(`assert_route_policy_wiring`)·production `/v1/debug` 표면 거부(`_assert_no_production_debug_surface`). 라우터 28파일(`routers/`), prefix 규약: `/admin/*`(admin-auth, backups, restore, features, files, issues, offline-uploads, poi-cache-targets, curations, theme-feature-candidates, dedup-reviews, enrichment-reviews, feature-requests, manual-provider-dedup-cases…), `/ops/*`(ops, ops/datasets, ops/pipeline, ops/logs, ops-live WS, contract-fixtures), `/service/*`(cache-target-streams, curation-snapshots, feature-alias-maps, feature-reference-reconciliations, feature-requests), 공용 `/features`, `/categories`, `/providers`, `/curations`, `/public/*`, `/weather` — 모두 `/v1` 아래 mount(ADR-048 clean cut, unversioned alias 없음). 비버저닝 liveness `/health`, `/version`(`routers/public_status.py`), readiness `/v1/ops/health-deep`. `/v1/debug/*`는 2026-09-03 제거(CHANGELOG Unreleased).
- RoutePolicy 6종(`route_policy.py`): `public-unauthenticated`, `public-keyed`, `service`, `operator`, `debug`, `metrics` — startup에서 모든 route가 분류·의존성 배선과 일치해야 기동.
- 미들웨어: `@application.middleware("http")` 요청 ID/`X-Request-ID` 부여 + `record_api_call` DB 로그 + duration, Prometheus 계측(`/metrics` 경로 제외), `SurfaceScopedCORSMiddleware`(`cors.py`, public 표면에만 CORS, credential 모드 없음, `KOR_TRAVEL_MAP_API_CORS_ALLOW_ORIGINS` 기본 `["http://localhost:12705","http://127.0.0.1:12705"]`).
- 에러 envelope: RFC7807 `application/problem+json` `ProblemDetail{type, title, status, detail, code, request_id, errors[]}`(`response.py`), `_ERROR_CODE_BY_STATUS`(400 BAD_REQUEST … 503 SERVICE_UNAVAILABLE), 중앙 exception handler(StarletteHTTPException, RequestValidationError, DomainCommandReplay/FingerprintConflict/Pending, GeoAuthNotConfiguredError, GeoRequestError, CacheTargetStreamConflict, SubtypeDetailError, Exception). 성공 envelope `{data, meta}`, `Meta{duration_ms, request_id, page?: PageMeta{page_size, next_cursor, total}, cluster?: ClusterMeta}`, `extra="forbid"`.
- 페이지네이션: cursor + `page_size`(2-티어 캡, `total` opt-in), `next_cursor`는 끝나도 `null` 직렬화; `/v1/features/search` cursor는 `KOR_TRAVEL_MAP_API_CURSOR_SIGNING_SECRET`로 서명(`docs/architecture/rest-api.md` §1.6, `docs/integration-map.md` §2).
- 인증(`auth.py`): 헤더 상수 `X-Kor-Travel-Map-Api-Key`(public keyed, DB 해시 캐시 `public_api_keys`), `X-Kor-Travel-Map-Service-Token`(상수시간 비교), `X-Kor-Travel-Map-Admin-Proxy-Secret` + `X-Kor-Travel-Map-Actor` + trusted CIDR(admin BFF), `X-Kor-Travel-Map-Ops-Token` + `X-Kor-Travel-Map-Ops-Scope`(`ops:read`/`ops:cancel`/`ops:fixture`, actor 코드 상수 `service:pinvi`/`service:docker-manager`), `X-Kor-Travel-Map-Admin-Feature-Create-Token`(SHA-256 digest 비교), `X-Kor-Travel-Map-Cache-Target-Consumer`, `/metrics` `Authorization: Bearer <KOR_TRAVEL_MAP_API_METRICS_TOKEN>`. `APIKeyHeader`를 `Security`로 의존해 OpenAPI `securitySchemes` 자동 선언. 파괴적 `/admin` 작업 kill-switch `KOR_TRAVEL_MAP_API_DESTRUCTIVE_ENABLED`. argon2/pbkdf2는 API 측에 없음(비밀번호 로그인은 Next.js가 담당).
- rate limit: 문서 계약 `429 + RateLimit-* + Retry-After`, lock 경합 `409 LOCK_BUSY + Retry-After: 15`(`rest-api.md` §1.7); idempotency는 UUID `Idempotency-Key` + `ops.domain_commands` ledger(fingerprint 충돌 409). 앱 레벨 전역 rate limiter 미들웨어는 `app.py` grep에서 발견 못 함 → 미확인.
- OpenAPI: `scripts/export_openapi.py` `--profile admin|user|service|all`, `--check`(git working tree 비교); 저장 `openapi.json`(1.45MB, 161 paths), `openapi.user.json`(29 paths, public 정책만, raw/source 필드 제거), `openapi.service.json`(27 paths); `openapi: 3.1.0`, `info.title kor-travel-map-api`, `info.version 0.2.0-dev`. CI `openapi.yml`이 `--profile all --check`. operationId는 FastAPI 기본(`delete_backup_v1_admin_backups__backup_id__delete` 형식, 사실), tags는 라우터별(`admin-backups`, `admin-features`, `ops`, `features`, `categories`, `providers`, `curations`…). 버전은 pre-1.0 `/v1` in-place 갱신, GA 이후 `/v2` + major별 export 파일 예정(export 스크립트 주석).
- 설정: `ApiSettings` `env_prefix="KOR_TRAVEL_MAP_API_"`, `env_file=".env"`. `.env.example` 키: `PROFILE(local-dev|production)`, `HOST/PORT 12701`, `DAGSTER_URL/ALLOWED_HOSTS/REPOSITORY_*`, `BACKUP_*`, `LOG_LEVEL`, `CORS_ALLOW_ORIGINS`, `OPS_PRINCIPAL_REQUIRED`, `OPS_READ/CANCEL/FIXTURE_TOKEN`, `SERVICE_TOKEN`, `ADMIN_MANUAL_FEATURE_CREATE_ENABLED`, `CURSOR_SIGNING_SECRET`, `ADMIN_TRUSTED_PROXY_CIDRS`, `PUBLIC_API_KEY_REQUIRED/CACHE_TTL_S`, `VWORLD_API_KEY`, `PROMETHEUS_METRICS_ENABLED/PATH`, `METRICS_TOKEN`, 라우터 활성 플래그 5종, `DESTRUCTIVE_ENABLED` + 메인 공유 `KOR_TRAVEL_MAP_KOR_TRAVEL_GEO_*`, `KAKAO/NAVER/GOOGLE` 키.
- 관측성: Prometheus 메트릭 접두 **`kor_travel_map_`**(`kor_travel_map_http_requests_total`, `_http_request_duration_seconds`, `_http_requests_in_progress`, `_http_response_size_bytes`, `_http_request_exceptions_total`, `_db_queries_total`, `_db_query_duration_seconds`, `_app_info`; `prometheus.py`). API 호출 로그는 DB `ops` 스키마(`record_api_call`).
- 테스트: `packages/kor-travel-map-api/tests/` 52파일, CI `--cov-fail-under=70`(메인과 coverage 파일 분리).

### 4.3 kor-travel-map-dagster (`packages/kor-travel-map-dagster`)

- Python `>=3.11`, setuptools, `include = ["kortravelmap.dagster*"]`, `[tool.dagster] module_name = "kortravelmap.dagster.definitions"`. 의존: `kor-travel-map==0.2.0-dev`, `dagster>=1.9,<2`, `dagster-webserver>=1.9,<2`, `dagster-postgres>=0.25,<1`, `boto3/botocore>=1.34,<2`, `httpx>=0.27,<1.0`. lockfile 없음.
- 자산/스케줄: `assets.py` `@asset` 29개, `schedules.py`가 `ScheduleDefinition`/`define_asset_job` + cron(예: `*/10 * * * *`, `35 * * * *`, `0 1,5,9,13,17,21 * * *`, 월 1회 `10 3 1 * *` 등 30여 건), `sensors.py`/`feature_operation_sensors.py`, `kma_weather.py`, `mois_source_sync.py`, `mcst_features.py`, `offline_uploads.py`, `provider_fetchers.py`, `provider_pagination.py`, `upstream_retry.py`, `runtime_preflight.py`(env allowlist — `KOR_TRAVEL_MAP_API_OPS_*` 존재 시 기동 거부), `maintenance.py`, `file_registry_*`. Dagster metadata DB `kor_travel_map_dagster`, `docker/dagster.Dockerfile`, `docker/dagster.yaml`, `dagster-storage-migrate` compose service.
- 테스트 30파일, CI `--cov-fail-under=80`. ruff/mypy strict 동일.

## 5. 문서·에이전트 규약

**진입 파일** (사실)

| 파일 | 크기 | 역할 |
|---|---|---|
| `CLAUDE.md` | 6.5KB | Claude 전용 1쪽 요약(정책은 AGENTS/SKILL/ADR이 소유). "CLAUDE.md + AGENTS.md 두 파일만 AI entry, Copilot/Cursor 룰 파일 두지 않음" |
| `AGENTS.md` | 20KB | Codex/Antigravity 표준 entry. 목표·행동 원칙(Think Before Coding/Simplicity First/Surgical Changes/Goal-Driven/Practical Bias)·언어 정책·역할·식별자 표·개발 환경·runbook·worktree+codegraph·**지시 우선순위 7단계**(사용자 → AGENTS → SKILL → architecture/ADR/data-model/backend-package/performance/test-strategy/agent-guide/provider-contract → README·docs → 코드·테스트 → 최소 가정)·외부 경계·DO NOT 5·prod 보안 감사·체크리스트 |
| `SKILL.md` | 11.5KB | 매뉴얼: 정체성, 빠른 시작, 디렉토리, **DO NOT 27개**(본문은 "26개"로 표기), 자주 묻는 작업, 도메인 어휘, 체크리스트 |
| `README.md` | 10.8KB | 제품 설명, 운영 모델, 책임 범위, 빠른 시작(WSL), 구조, 핵심 규칙, 검증, 문서 길찾기 |
| `frontend/design.md` | 27.5KB | admin 디자인 시스템 잠금 정본(§3.1) |
| `frontend/README.md` | 19KB | 스택·env·개발·npm 보안·React Doctor·e2e·페이지 표 |
| `.claude/agents/README.md` | — | vendored upstream agent 원문(api-designer/backend-developer/frontend-developer/mobile-developer/ui-designer) 영어 예외 + context-manager 의존을 codegraph로 치환 |

언어 정책: 한국어 문서, 식별자 원문 유지; vendored 디렉터리만 예외(ADR-059).

**docs/ 트리와 규약** (사실)

| 위치 | 규약 |
|---|---|
| `docs/adr/` 57파일, `README.md` 색인 | 파일당 1개 `NNN-<slug>.md`, "다음 후보 = ADR-098"은 README 상단이 정본(다른 문서에 박지 않음 — DA-D-01 drift 회피); 핵심 구조 결정만 ADR, 개발 규칙은 SKILL §4로, provider/ETL은 topic 문서로 이관; superseded 표시 유지 |
| `docs/decisions.md`, `docs/adr045-*.md` | 결정 로그·standalone 전환 계획 |
| `docs/tasks.md` / `tasks-done.md` / `tasks-acceptance.md` / `tasks-rule.md` | 열린 `[ ]`는 tasks.md(한 줄 backlog), 완료는 tasks-done.md, 해제 조건은 tasks-acceptance.md 절, 규약은 tasks-rule.md; **task ID**: `T-NNN`, 하위 `T-NNN<letter>`, 파생 `T-NNN-<slug>`, 묶음 prefix `T-RV-NN`/`T-VN-*`/`T-ADM-*`/`T-C7-*`; 마커 `[ ]`/`[x]`/`[~]`; `tests/lint/test_task_ledger_conventions.py` + `scripts/task_ledger_lint.py`/`check_task_ledger_deletions.py`(CI)가 강제 |
| `docs/journal.md` / `docs/resume.md` | 역시간순 일지(상단 추가) / 진척·"다음 한 작업" 정본; 2026-07-26 이후만 담고 이전은 `docs/archive/`(18파일, 읽기 전용); pre-commit `check_journal_update.py`가 src/tests 변경 시 journal 갱신 강제 |
| `docs/runbooks/` 14파일 | `agent-workflow.md`(표준 1-PR 흐름: worktree → 브랜치 → WSL 편집 → 4 게이트 → PR → CI green → 머지 → 동기화), `agent-failure-patterns.md`, `branch-protection.md`, `docker-app.md`, `c7-prod-live-e2e.md`, `admin-ui-screen-checklist.md`, `cross-repo-audit-checklist.md`(분기 1회 4-repo drift 점검) 등 |
| `docs/reports/` 94파일 | 감사·설계 리포트(`hallmark-audit-…`, `t-vn-*-design-…`, `docs-consistency-audit-…`) |
| `docs/architecture/` 23파일 | `architecture.md`, `data-model.md`, `rest-api.md`(1,300행+), `debug-ui-package.md`, `backend-package.md`, `provider-contract.md`, `performance.md`, `openapi-admin-contract.md`, `public-views-api.md`, `admin-frontend-design-rules.md` 등 |
| `docs/etl/` 19, `docs/sprints/` 6, `docs/removal-manifests/` 1 | provider별 ETL, Sprint 1~5 |
| `CHANGELOG.md` 303KB | Keep a Changelog 형식, `[Unreleased]` 상단 |

**개발 환경·워크플로** (사실)

- 정본 OS: Linux/WSL(Windows PowerShell 금지). NTFS worktree는 보관 위치, 실행은 WSL `/mnt/f/dev/kor-travel-map-<agent>`. 에이전트별 고정 worktree: Codex `F:\dev\kor-travel-map-codex`, Claude `F:\dev\kor-travel-map-claude`, Antigravity `F:\dev\kor-travel-map-antigravity`; 동기화 브랜치 `sandbox/<agent>`; 메인 trunk `F:\dev\kor-travel-map`는 사람 전용.
- codegraph: `@colbymchenry/codegraph` MCP를 `.mcp.json`(Claude: filesystem + codegraph), `claude.json`, `antigravity.json`, `.gemini/mcp.json`, `opencode.json`(instructions: AGENTS.md, SKILL.md)에 등록; `Feature` DTO/`make_feature_id`/provider 변환/`core/scoring.py`/`infra/models.py` 수정 전 `codegraph_explore` 영향도 평가 필수(SKILL §4 27번).
- 리뷰 정책: PR 머지는 CI(`ci`, `lint`, `openapi`) green + **1 review approval**(`AGENTS.md` 체크리스트). "적대 리뷰"는 `docs/runbooks/agent-workflow.md` §5·§7과 `docs/tasks.md`에 언급되나 "2인 적대적 리뷰"를 규정한 문장은 찾지 못함 → 미확인(1인 적대 리뷰 관행으로 추정).
- 브랜치/PR: `feat|fix|chore|docs|refactor|adr/<topic>`, `gh pr create`, 커밋 trailer `Co-Authored-By:`, PR 본문 끝 `🤖 Generated with …`, 실제 게이트 수치만 기재.
- 보안 감사(push 전 필수 4단계): 스테이징에 `*.local.md`/`.env*` 없음 → 일반 비밀 grep → `scripts/check_prod_redaction.py`(pre-commit·CI) → 프로젝트별 민감값 grep(`docs/deploy-runbook.local.md` §6). `*.local.md`(`deploy-runbook.local.md`, `prod-access.local.md`)는 gitignore + `.git/info/exclude`, 각 worktree `docs/`에 복사.
- pre-commit(`.pre-commit-config.yaml`, `minimum_pre_commit_version 3.7.0`): journal-required, prod-redaction, `ruff format --check`, `mypy --strict`, `lint-imports`(모두 local hook, `scripts/run-precommit-check.sh`).

## 6. CI·배포·운영

**GitHub Actions** (`.github/workflows/`, 사실)

| workflow | 트리거 | 게이트 |
|---|---|---|
| `ci.yml` | push/PR | `unit`: Python 3.11/3.12/3.13 matrix, Node 22.23.1 + `npm@12.0.1 ci --workspaces=false --omit=dev --ignore-scripts`, `pip install -e ".[dev]"` + api + dagster editable, `pytest tests/unit tests/lint --cov=src/kortravelmap`, api tests `--cov-fail-under=70`, dagster tests `--cov-fail-under=80`; `integration`: Python 3.13 testcontainers PostGIS, unit coverage 합산 후 fail_under 판정, coverage XML 업로드; `fixture-replay` |
| `lint.yml` | push/PR | `check_task_ledger_deletions.py`, `check_prod_redaction.py`, `ruff check`(src/tests/api/dagster), `ruff format --check src tests`, `mypy --strict -p kortravelmap` / `kortravelmap.api` / `kortravelmap.dagster`, `lint-imports` |
| `openapi.yml` | push/PR | `export_openapi.py --profile all --check` (3 spec 파일 drift 시 실패, ADR-031) |
| `frontend.yml` | push/PR | Node 22.23.1, `npm@12.0.1 ci --workspaces --include=optional`, `audit:high`, `audit:dev`, `verify:npm-tree`, `verify:frontend-eslint`, `lint`, `verify:react-doctor-config`, `doctor`, `verify:next-sharp`, `test`(vitest), `gen:types:check`, user-client `gen:types:check` + `type-check`, `type-check`, `next build`(NEXT_PUBLIC_* 더미 값) |
| `docker-images.yml` | (조건부) | `scripts/docker-buildx.sh`로 production 이미지 전부 빌드, archive 산출 검증 |
| `postgis-only.yml` | manual | `pytest tests/integration --no-cov` |

**Docker/compose** (사실): `docker-compose.yml`(52KB) 서비스 — `postgres`(postgis/postgis digest 핀), `dagster-db-init`, `db-role-bootstrap-300`, `db-application-create-fresh-300`, `db-application-schema-fresh-300`(profile `fresh-init`), `rustfs` + `rustfs-init`(minio/mc), `api`, `frontend`, `dagster`, `dagster-daemon`, `dagster-storage-migrate`; volumes `kor-travel-map-postgres/-mois-source/-rustfs-data/-application-final-permit/-dagster-storage-permit`; secrets `admin-control`, `github_token`. 오버레이: `docker-compose.host.yml`(workstation 기본 host network), `docker-compose.local-dev.yml`(`KOR_TRAVEL_MAP_API_PROFILE=local-dev`), `external-db/infra/object-store.yml`. Dockerfile: `api.Dockerfile`(python digest 핀, OCI label에 git tree/dockerfile sha256/base image id), `frontend.Dockerfile`(§3.1), `dagster.Dockerfile`, `c7-playwright.Dockerfile`.

**포트 할당** (ADR-047, `CLAUDE.md` §2, `docs/deploy.md`, 사실): API `12701` · admin UI `12705` · Dagster `12702` · Postgres standalone `5432` / **n150 prod `12700`**(127.0.0.1 전용, 프로젝트별 전용 인스턴스: geo 12500 · concierge 12600 · map 12700 · pinvi 12800) · RustFS S3 `12101`/console `12105` · geo `12501`. 대역 규칙: 프로젝트별 `12x00`대(`x00` DB, `x01` API, `x02` Dagster, `x05` web).

**prod(n150) 규약**: production 배포는 `kor-travel-docker-manager` lane이 소유(이미지 pair·pinned runtime manifest v6·rebuild journal v8·C7 attestation, `docs/integration-map.md` §3.1). API image 기본 profile `production`(fail-closed: 세 ops token·cursor secret·metrics token 필수, `/v1/debug` 마운트 거부). 시크릿은 컨테이너별 env 주입(root `.env`·frontend·Dagster에 API 토큰 미주입), `.env` 권한 600 또는 vault(SKILL §4 8번), prod 호스트/IP/도메인은 `*.local.md`에만.

## 7. 외부 연동 (cross-repo)

| 대상 | 방향/방식 | 인증 | 근거 |
|---|---|---|---|
| kor-travel-geo | map → geo `POST /v2/{reverse,geocode}`(backend `geocoding.py`) 및 admin UI `/api/geo/*` BFF | `X-KTG-API-Key` 헤더만(URL query 금지), key는 `KOR_TRAVEL_MAP_KOR_TRAVEL_GEO_API_KEY` / UI `KOR_TRAVEL_GEO_API_KEY`; `X-KTG-Actor/Roles/Admin-Proxy-Secret` 미전송 | `src/kortravelmap/geocoding.py:951,1035`, `frontend/src/app/api/geo/[...path]/route.ts`, `docs/integration-map.md` §4 |
| kor-travel-concierge | map Dagster가 pull `GET /api/v1/features/{snapshot\|changes}` → `FeatureBundle` | concierge DB `read` scope `X-API-Key`; 무-envelope `{items,next_cursor,has_more}` | `docs/integration-map.md` §2·§3, `docs/etl/concierge-feature-etl.md` |
| PinVi | PinVi → map `/v1` public read(`features`, `curations`, `weather`, `public/*`), admin(`/v1/admin/features*`), canonical ops(`/v1/ops/{datasets,pipeline}`), service(`/v1/service/curation-*` detail-snapshot, `feature-alias-maps`) | `X-Kor-Travel-Map-Api-Key` 또는 `X-Kor-Travel-Map-Service-Token`; ops는 `X-Kor-Travel-Map-Ops-Token` + `-Ops-Scope`(`ops:read`/`ops:cancel`, actor 상수 `service:pinvi`); `pinvi:curation-snapshot:read` scope | `integration-map.md` §2·§3, `api/auth.py` |
| kor-travel-docker-manager | 인프라 소유(PostGIS 4 인스턴스·RustFS·Grafana·Prometheus), prod 배포 lane, C6c cancel-probe fixture 호출 | `ops:fixture` scope, actor `service:docker-manager`; Prometheus scrape `Authorization: Bearer` metrics token(현재 docker-manager prometheus.yml에 12701 job 없음 — 문서 기준) | `integration-map.md` §1·§2·§3.5 |
| kor-travel-weather | **언급 없음**(`docs/integration-map.md` 대상 4개 시스템 + geo에 weather 없음; 날씨는 `python-kma-api`/`python-airkorea-api`/`python-khoa-api` 직접 사용) | — | `pyproject.toml` providers extra |
| 공유 라이브러리 `python-*-api` | git URL + commit sha 핀 13종: datagokr, kma, airkorea, khoa, opinet, krex, visitkorea, knps, krforest, krheritage, krairport, mois, mcst (kor-travel-geo·kasi는 주석) | wrapper/adapter 금지, `Protocol`로 입력 shape만 정의, 로컬 `F:\dev\python-*-api` 우선 조회(ADR-044) | `pyproject.toml` `[project.optional-dependencies].providers`, `docs/architecture/provider-contract.md` §12 |
| `python-kraddr-base` | 의존 없음 — ADR-041로 흡수 완료(`PlaceCoordinate` 제외) | — | `pyproject.toml` 주석, SKILL §4 26번 |
| `maplibre-vworld-react` / `maplibre-vworld-js` | npm 의존 **없음**. `src/lib/vworld-style.ts`가 `maplibre-vworld-react@a7cb0f8` core/web 경계를 포팅(ADR-036 v0.1.3 핀 무효, #476에서 dep 제거) | — | `vworld-style.ts:3`, `CLAUDE.md` §2 |
| `vworld-map-*` 벤더 tgz | 해당 없음(저장소 내 tgz/vendor 디렉터리 미발견) | — | `git ls-files` |
| VWorld API key | geo `KOR_TRAVEL_GEO_VWORLD_API_KEY`와 동일 값을 `NEXT_PUBLIC_VWORLD_API_KEY`·`KOR_TRAVEL_MAP_API_VWORLD_API_KEY`로 공유, 별도 발급 금지, PinVi 사용자 UI도 공유 | HTTP referrer 제한 권장 | `frontend/.env.example`, `frontend/README.md` §환경변수 |

## 8. 공통화 후보

| # | 영역 | 근거 경로 | 신뢰도 | 비고 |
|---|---|---|---|---|
| 1 | Tailwind v4 CSS-first 토큰 골격(`@theme inline` + `:root`/`.dark` + shadcn alias 매핑 + `@custom-variant` data-*) | `frontend/src/app/globals.css`, `design.md` §Exports | high | 이미 "토큰 파일 = globals.css" 모델; common은 semantic 이름·크기 규약을 제공하고 브랜드 값(oklch)은 앱이 소유 |
| 2 | 상태 tone 5종 의미 표(success/warning/info/destructive/neutral) + `statusLabel()` 단일 정본 패턴 | `src/lib/status-label.ts`, `design.md` §Status colour semantics | high | tone 의미·라벨 유일성 규약은 제품 무관; 실제 enum→라벨 사전은 앱별 |
| 3 | focus 레시피(`:focus-visible` outline 2px offset 2px 단일 발행, `outline-none` 금지, `focus-visible:outline-0` 예외 닫힌 목록) | `globals.css @layer base`, `design.md` §Focus | high | Tailwind v4 `--tw-outline-style` 함정 문서화 포함 — 규칙 문서로 공통화 가치 큼 |
| 4 | reduced-motion 전역 규칙(스피너 예외 1.6s, Skeleton off, crossfade only) + 전환 열거 규칙(`transition-all/colors` 금지) | `globals.css` 말미, `design.md` §Motion | high | CSS 스니펫 + lint 규칙으로 이식 가능 |
| 5 | 금지 패턴 grep 게이트 7종(raw hex/oklch, `text-[Npx]`, `rounded-2xl+`, 팔레트 alpha, `outline-none`, `transition-all`, `aria-disabled:opacity-`) | `design.md` §금지 패턴 | medium | 규칙은 명문화됐으나 자동화 스크립트 미발견(§11) — common이 스크립트로 제공하면 즉시 채택 가능 |
| 6 | Button 8-state 레시피(CVA, `loading` = `aria-busy`+`aria-disabled` 포커스 유지, 흐림은 라벨 자식 래퍼, `border-transparent` 폭 고정, variant 경계 규칙 3:1) | `src/components/ui/button-variants.ts`, `button.tsx` | high | 선행 리뷰 §3.3이 지적한 대로 geo(Radix Slot/React 18)·PinVi(native button)와 계약이 다름 — 동작 계약 합의가 선행 조건 |
| 7 | Badge/StatusBadge(tint 배경 + tone 잉크, `h-6 text-2xs tabular-nums`, dot+text) | `badge-variants.ts`, `status-badge.tsx`, `status-badge-variants.ts` | high | tone 토큰 이름에만 의존 |
| 8 | headless `DataTable`(TanStack Table v8 + Virtual, `manualSorting` 기본, skeleton/empty/error 상태 표면, 가상화 시 ARIA role 명시, React Compiler opt-out 경계) | `src/components/ui/data-table.tsx`(799행), `data-table.test.tsx` | medium | PinVi가 이미 이식(선행 리뷰 §3.1; 본 조사에서 PinVi 측은 미검증). 행 ID·선택·정렬 소유권 계약 정의 필요 |
| 9 | Rail-Workbench 셸(`AdminShell`: rail nav 그룹·collapsible·skip link·breadcrumb·헤더 밴드 액션 수 제한) | `src/components/admin-shell.tsx`, `design.md` §Macrostructure | medium | nav 정본은 앱별; 셸 골격·a11y(skip link, `<main tabIndex=-1>`)는 공통 |
| 10 | `FilterBar` / `PaginationBar`(cursor·offset pager, `formatCount`, `NULL_GLYPH`) / `EmptyState` / `SectionCard` / `StatStrip` / `DetailList` / `CopyButton` / `JsonViewer` / `HelpTip`(hover 800ms·focus 0ms) / `ConfirmDialog`(`useConfirm`) | `src/components/*.tsx` | high | 모두 Hallmark 스탬프·토큰만 사용; 데이터 의존 없음 |
| 11 | Form 기본형(`FormField`/`FormSelect`/`FormTextarea` + `field-variants` 라벨 레시피 + `form-validation.ts` 프레임워크 비의존 검증·첫 에러 focus) | `src/components/ui/form-*.ts(x)`, `src/lib/form-validation.ts` | medium | react-hook-form/zod 미사용이 concierge(RHF 사용, 선행 리뷰 §2)와 다름 — common은 양쪽을 포용하거나 하나로 정해야 함 |
| 12 | Next.js admin 인증 경계 패턴(middleware 공개 경로 집합 + HMAC 세션 쿠키 + pbkdf2 + Origin CSRF + 로그인 rate limit + 감사 이벤트) | `middleware.ts`, `src/lib/auth.ts`, `src/app/api/auth/*` | medium | geo도 "Next에서 세션 검증 후 신뢰 프록시 신원 전달"(선행 리뷰 §3.6). **세션 secret/역할 판정은 공통화 금지**, 폼·미들웨어 골격·헤더 규약만 후보 |
| 13 | BFF proxy 패턴(`/api/proxy/[...path]`: 헤더 allowlist, `X-<App>-Actor` + `X-<App>-Admin-Proxy-Secret`, 응답 헤더 allowlist, problem+json 변환, `Idempotency-Key`/`If-Match` 전달) | `src/lib/proxy.ts`, `src/app/api/proxy/[...path]/route.ts` | high | 헤더 접두만 앱별(`X-Kor-Travel-Map-*` ↔ `X-KTG-*`) — 접두 파라미터화 가능 |
| 14 | fetch 래퍼(`ApiClientError{status,path,problem,retryAfterSeconds}`, `credentials: same-origin`, `pathWithQuery`, Idempotency-Key sessionStorage 관리) | `src/api/client.ts` | high | RFC7807 파싱은 백엔드 공통 규약(#17)과 짝 |
| 15 | OpenAPI → TS 타입 생성 파이프라인(`openapi-typescript` 7.x, `gen:types` + `gen:types:check` CI drift, user/service spec 분리 산출물 패키지) | `frontend/package.json`, `packages/kor-travel-map-user-client/`, `.github/workflows/frontend.yml` | high | 소비자 vendoring 규약(commit hash pin)까지 문서화됨 |
| 16 | RFC7807 `ProblemDetail{type,title,status,detail,code,request_id,errors[]}` + `{data, meta{duration_ms,request_id,page{page_size,next_cursor,total}}}` envelope + `X-Request-ID` 중앙 핸들러 | `packages/kor-travel-map-api/src/kortravelmap/api/response.py`, `app.py` `_ERROR_CODE_BY_STATUS` | high | `docs/integration-map.md` §3은 "표면별 의도적 차이"를 고정(concierge는 무-envelope) — common은 kor-travel 신규 표면 기본값으로만 |
| 17 | RoutePolicy 기반 표면 분류(public-unauthenticated/public-keyed/service/operator/debug/metrics) + 기동 시 배선 검증 + 표면 범위 CORS | `api/route_policy.py`, `api/cors.py`, `app.py` `assert_route_policy_wiring` | medium | 개념·검증기는 공통화 가능, 정책명은 앱별 |
| 18 | 헤더 명명 규약 `X-<App>-Api-Key` / `-Service-Token` / `-Actor` / `-Admin-Proxy-Secret` / `-Ops-Token` / `-Ops-Scope` + `/metrics` Bearer | `api/auth.py:82-92` | high | geo는 `X-KTG-*` 축약형(§9) — common이 접두 규칙(풀네임 vs 약어)을 정해야 함 |
| 19 | Prometheus HTTP/DB 메트릭 세트(`<app>_http_requests_total`, `_http_request_duration_seconds`, `_http_requests_in_progress`, `_http_response_size_bytes`, `_http_request_exceptions_total`, `_db_queries_total`, `_db_query_duration_seconds`, `_app_info`) | `api/prometheus.py` | high | 접두 `kor_travel_map_`(풀네임) vs geo `ktg_`(선행 과제 문구) — 접두 규약 결정 필요 |
| 20 | OpenAPI export/drift 스크립트 골격(`--profile`, `--check`, working tree 비교, user 프로파일 필드 제거 목록) | `packages/kor-travel-map-api/scripts/export_openapi.py`, `.github/workflows/openapi.yml` | high | 프로파일 3종(admin/user/service) 모델 자체가 재사용 가능 |
| 21 | pydantic-settings `env_prefix` 규약(`<APP>_` 메인 / `<APP>_API_` API, `SecretStr`, `.env.example` 유지) + profile(`local-dev`/`production`) fail-closed 기동 검증 | `src/kortravelmap/settings.py:46`, `api/settings.py:350` | high | 공통 BaseSettings 믹스인 후보 |
| 22 | Python 품질 게이트 세트(ruff `line-length 100` + `select E,F,I,UP,B,ASYNC,PIE,PT,RET,SIM,TID`, mypy `--strict` + pydantic plugin, import-linter layers/forbidden, pytest `--strict-markers --strict-config` + `filterwarnings=error`, coverage `fail_under` 단계 상향, pre-commit local hooks) | 루트 `pyproject.toml`, `.pre-commit-config.yaml`, `lint.yml` | high | 세 Python 패키지가 이미 동일 설정 복제 — 공통 `ruff.toml`/mypy 프리셋 후보 |
| 23 | 프론트 의존성 보안 게이트(npm exact 핀 `12.0.1` + `engine-strict` + `strict-allow-scripts` + `allowScripts` allowlist + `overrides` + `audit:high --omit=dev` + `verify:npm-tree` + Dockerfile/CI 명령 순서를 pytest로 잠금) | 루트 `package.json`, `.npmrc`, `tests/unit/test_frontend_dependency_security.py`, `scripts/verify-*.mjs` | high | 사용자 전제 (2) "버전 일치화 정책"의 구현 모델로 그대로 채택 가능 |
| 24 | ESLint flat 프리셋(typescript-eslint + import-x + react-x/react-dom + jsx-a11y-x + react-hooks recommended-latest + next) + effective-config 검증 스크립트 + react-doctor 설정 잠금 | `eslint.config.mjs`, `scripts/verify-frontend-eslint-config.mjs`, `scripts/verify-react-doctor-config.mjs`, `doctor.config.json` | high | `eslint-config-next` 미사용 결정 포함 |
| 25 | Playwright mocked/live 이중 suite 규약(deny proxy 격리, `timezoneId: UTC`, storageState auth setup, live 전용 config, n150 우선) + `tsconfig.tooling.json`으로 하네스 자체 type-check | `playwright*.config.ts`, `tsconfig.tooling.json`, `e2e/ws-isolation.ts` | medium | 서버 외부 기동 전제는 앱별 |
| 26 | 문서·에이전트 규약(CLAUDE.md 1쪽 + AGENTS.md 정책 + SKILL.md DO NOT, 지시 우선순위, 한국어 정책 + vendored 예외, ADR 색인 "다음 번호는 README 상단만", tasks/tasks-done/tasks-acceptance/tasks-rule + T-ID 체계, journal/resume + archive 분리, runbooks 인덱스, push 전 보안 감사 4단계, `*.local.md`) | `AGENTS.md`, `SKILL.md`, `CLAUDE.md`, `docs/tasks-rule.md`, `docs/runbooks/README.md` | high | canview 참조 모델과 같은 계열; kor-travel 공통 템플릿 후보 |
| 27 | 포트 대역 규약(`12x00` DB / `x01` API / `x02` Dagster / `x05` web, 프로젝트별 전용 PostGIS) + 고정 포트 preflight 스크립트 | `CLAUDE.md` §2, `docs/integration-map.md` §1, `scripts/preflight-ports.sh` | high | docker-manager와 함께 정본 |
| 28 | Dockerfile 규약(base image digest 핀, multi-stage, non-root, OCI revision label, build-arg로 `NEXT_PUBLIC_*` 주입, standalone 출력) | `docker/frontend.Dockerfile`, `docker/api.Dockerfile` | medium | 이미지 provenance label 체계는 map 고유 강도 |
| 29 | 마커 팔레트/maki 매핑 공유 패키지 모델(`@kor-travel-map/map-marker-react`: 소스 share, MIT, registry 비게시, `transpilePackages`) | `packages/map-marker-react/`, `next.config.ts` | medium | PinVi 사용자 UI와 공유 의도(ADR-029) — common 지도 계층 설계 시 참고; `maplibre-vworld-react`와 중복 금지 검토 필요 |
| 30 | 접근성 체크리스트(aria-busy 영역, 가상화 테이블 role 명시, skip link, `disabledReason`/`title`로 비활성 사유 표기, 값 없으면 단위 제거) | `design.md` §States·§Copy, `admin-ui-screen-checklist.md` | high | UX 가이드 문서 산출물로 직행 가능 |

## 9. 이 저장소 고유 차이·주의점

| 영역 | 내용 | 공통화 시 영향 |
|---|---|---|
| Next.js exact 핀 | `next` `16.2.12` exact + 루트 `overrides`(postcss 8.5.23, sharp 0.35.3) + `verify-next-sharp.mjs` ABI smoke + pytest 잠금 | common이 caret 범위를 제시하면 map의 보안 게이트(`test_frontend_dependency_security.py`)와 충돌 — 버전 상향은 map의 lock 갱신 PR을 동반해야 함 |
| npm 12.0.1 exact + Node 22.23.1 | `engines.npm 12.0.1`, `packageManager`, 모든 명령 `npx --yes npm@12.0.1`; CI/Dockerfile Node `22.23.1` | 다른 앱(pnpm/npm 버전 상이)과 워크플로 명령이 다름; common 정책이 "npm 12.0.1"을 채택하면 나머지 앱이 따라야 함 |
| shadcn CLI 미설치·소스 소유 | `components.json`은 `base-nova` 스타일이지만 CLI/registry 미사용, named data-variant 자체 소유를 테스트로 강제 | common이 shadcn registry 배포 모델을 택하면 map은 "registry 아이템 → 소스 복사" 절차가 필요 |
| Base UI 1.x (Radix 아님) | `@base-ui/react` 1.6.0; `render` prop·`mergeProps`/`useRender` 기반 | geo(Radix, React 18)와 프리미티브 엔진 상이(선행 리뷰 §3.3 재확인) |
| react-hook-form/zod 부재 | controlled state + `form-validation.ts`; zod는 map-marker-react peer만 | concierge(RHF)와 폼 계층 불일치 — common Form 프리미티브는 헤드리스로 설계해야 양쪽 수용 |
| OKLCH 토큰 + 실측 대비 수치 | 토큰 값마다 WCAG 대비 실측 주석, hairline 2종 분리(`--border` 장식 / `--control-line` 컨트롤) | common 토큰이 `--border` 하나만 두면 map의 1.4.11 규칙 위반 — 2종 분리 설계 권장 |
| 다크 모드 | `.dark` 정의만, 토글 미마운트 | common이 `data-theme`/`prefers-color-scheme` 전략을 정하면 map은 `@custom-variant dark (&:is(.dark *))` 재정의 필요 |
| 두 디자인 문서 병존 | `design.md`(2026-08-18~, 잠금)와 `docs/architecture/admin-frontend-design-rules.md`(2026-06-18, "정보는 카드 안에", 36px KPI) 충돌; `debug-ui-package.md`는 여전히 후자를 가리킴 | common 색 톤·UX 가이드는 `design.md`를 원본으로 삼되, 구 문서 폐기 여부는 map 측 결정 필요(§11) |
| 금지 패턴 게이트 미자동화 | `design.md` grep 게이트 7종의 스크립트/CI 부재 | common이 lint/스크립트를 제공하면 map이 첫 소비자 |
| PC 전용 | 모바일 분기·터치 밀도 처리 없음, `lg` 기준 rail 전환만 | 사용자 전제 (4) PC/Mobile Web 규칙 중 Mobile은 map에 적용 대상 없음 — PinVi/사용자 앱 규칙과 분리해야 함 |
| Hallmark 스탬프 강제 | 모든 styled 파일 첫 줄 주석 | common 컴포넌트를 그대로 가져오면 스탬프 규약과 충돌하거나 이중 표기 필요 |
| 헤더 접두 풀네임 | `X-Kor-Travel-Map-*`, 메트릭 `kor_travel_map_*`, env `KOR_TRAVEL_MAP_*` | geo `X-KTG-*`/`ktg_` 약어와 불일치 — common 명명 규칙 결정 사항 |
| OpenAPI 3종 프로파일 + 거대 spec | `openapi.json` 1.45MB/161 paths, operationId FastAPI 기본 형식(`func_path_method`) | common OpenAPI 규칙이 operationId 커스텀을 요구하면 생성 타입 이름 전면 변경 → 소비자(PinVi vendoring) 영향 |
| Python lockfile 없음 | `uv pip install -e` + git sha 핀만; pytest/anyio 미고정으로 2026-09-03 CI red 사고 기록 | 사용자 전제 (2) 버전 일치화는 lockfile 도입 결정을 동반해야 함 |
| alembic `<1.20` 상한·`300` baseline·docker-manager permit | schema 초기화가 compose one-shot + final permit 체계에 결박 | DB 초기화/마이그레이션 규약 공통화는 map의 provenance 체계보다 약하게 설계될 가능성 — map은 예외 허용 필요 |
| Linux/WSL 정본 | Windows PowerShell 실행 금지, e2e n150 우선 | canview/다른 저장소가 PowerShell 정본이면 common 개발환경 문서는 저장소별 분기표 필요 |
| CLI argparse | typer 미사용(`ktmctl`) | common CLI 규약이 typer를 전제하면 map은 예외 |
| 로깅 | 표준 logging, structlog 미의존(설정 문구만 존재) | common 관측성 규약이 structlog를 요구하면 map은 신규 의존 |

## 10. 버전 표

| 항목 | 선언 범위(파일) | lockfile 설치 버전 |
|---|---|---|
| node | `^22.22.2 \|\| ^24.15.0 \|\| >=26.0.0` (루트·frontend `engines`); CI/Docker `22.23.1` | (런타임, lock 대상 아님) |
| npm | `12.0.1` exact (`engines`, `packageManager`) | — |
| next | `16.2.12` (frontend), `@next/env 16.2.12` (루트) | 16.2.12 |
| react / react-dom | `^19.2.6` | 19.2.8 / 19.2.8 |
| typescript | `^5.9.3` (frontend, user-client); `^6.0.3` (map-marker-react dev) | 5.9.3 (hoisted) / 6.0.3 (map-marker-react nested) |
| tailwindcss | `^4.3.0` | 4.3.3 |
| @tailwindcss/postcss | `^4.3.0` | 4.3.3 |
| @base-ui/react | `^1.5.0` | 1.6.0 |
| radix-ui | 없음 | — |
| shadcn (CLI) | 없음(금지, 테스트 단언) | — |
| lucide-react | `^1.17.0` | 1.27.0 |
| eslint | `^10.8.0` | 10.8.0 |
| typescript-eslint | `^8.65.0` | 8.65.0 |
| vitest | `^4.1.7` | 4.1.10 |
| @playwright/test | `1.60.0` exact | 1.60.0 |
| @tanstack/react-query | `^5.100.14` | 5.101.4 |
| @tanstack/react-table / react-virtual | `^8.21.3` / `^3.14.3` | 8.21.3 / 3.14.8 |
| zod | 없음(frontend); `^4.4.3` (map-marker-react peer/dev) | 4.4.3 |
| zustand | `^5.0.14` | 5.0.14 |
| react-hook-form | 없음 | — |
| maplibre-gl | `^5.24.0` | 5.24.0 |
| sonner / tw-animate-css / cva / clsx / tailwind-merge / pretendard | `^2.0.7` / `^1.4.0` / `^0.7.1` / `^2.1.1` / `^3.6.0` / `1.3.9` | 2.0.7 / 1.4.0 / 0.7.1 / 2.1.1 / 3.6.0 / 1.3.9 |
| openapi-typescript | `^7.13.0` | 7.13.0 |
| react-doctor | `^0.9.1` | 0.9.1 |
| postcss / sharp (override) | `8.5.23` / `0.35.3` | 8.5.23 / 0.35.3 |
| vite | `^8.0.14` (map-marker-react) | 7.3.6 (hoisted) / 8.1.5 (map-marker-react nested) |
| python | `>=3.11` (3개 pyproject); CI 3.11/3.12/3.13 | lockfile 없음 |
| fastapi | `>=0.115` (api) | 미확인 |
| starlette | `>=0.40,<1.0` (api) | 미확인 |
| uvicorn | `[standard]>=0.30` (api) | 미확인 |
| pydantic / pydantic-settings | `>=2.7` / `>=2.4` | 미확인 |
| sqlalchemy / geoalchemy2 | `>=2.0` / `>=0.15` | 미확인 |
| alembic | `>=1.19.1,<1.20` | 미확인 |
| asyncpg / psycopg | `>=0.29` / `[binary,pool]>=3.2` | 미확인 |
| httpx | `>=0.27,<1.0` (api·dagster), dev extra(메인) | 미확인 |
| prometheus-client | `>=0.20` (api) | 미확인 |
| ruff / mypy / pytest | `>=0.5` / `>=1.10` / `>=8` (dev extra) | 미확인 |
| import-linter / testcontainers | `>=2.0` / `[postgres]>=4` | 미확인 |
| dagster / dagster-webserver / dagster-postgres | `>=1.9,<2` / `>=1.9,<2` / `>=0.25,<1` | 미확인 |
| gdal | `==3.8.4` (geo extra) | 미확인 |
| structlog / typer / tenacity | 선언 없음 | — |

## 11. 미확인·열린 질문

1. Python 설치 버전: lockfile이 없어 fastapi/pydantic/sqlalchemy/dagster 등의 실제 설치 버전은 미확인(CI는 매 실행 최신 해석; `pyproject.toml` `filterwarnings` 주석에 anyio 신규 릴리스로 CI red 사고 기록). common의 "버전 일치화" 정책에 Python lockfile(uv.lock) 도입을 포함할지 결정 필요.
2. `design.md` §금지 패턴 "grep 게이트"의 자동화 스크립트 소재: tracked 파일·CI·pre-commit에서 미발견. 수동 `rg` 절차인지, 로컬 미커밋 스크립트인지 map 측 확인 필요.
3. `docs/architecture/admin-frontend-design-rules.md`(2026-06-18)의 지위: `design.md`와 충돌하는 규칙(카드 안 정보, KPI 36px)이 남아 있고 `debug-ui-package.md`가 여전히 참조. 폐기/갱신 여부 미확인.
4. "2인 적대적 리뷰" 정책: `agent-workflow.md`·`tasks.md`에 "적대 리뷰" 언급은 있으나 인원·절차 정본 문장은 미발견. 실제 관행(1인 Claude 적대 리뷰 vs 2인)은 미확인.
5. structlog: `settings.py:535` 필드 설명에 "structlog 로깅 레벨"이 있으나 의존 선언·import 없음. 실제 로깅 구현이 표준 logging인지(API `app.py`는 표준 logging) 메인 라이브러리 어디에서 json/console 포맷을 적용하는지 미확인.
6. 앱 레벨 rate limit 미들웨어: `rest-api.md` §1.7이 `429 + RateLimit-*` 계약을 정의하지만 `app.py`에서 전역 limiter를 찾지 못함(라우터 단위 구현 여부 미확인). 로그인 rate limit은 Next.js 측(프로세스 메모리)에만 확인.
7. PinVi `data-table.tsx` 이식 주장(선행 리뷰 §3.1)은 PinVi 저장소 조사 담당이 재검증해야 함(본 인벤토리 범위 밖). 선행 리뷰의 map 커밋 `c72456f6`은 본 기준 `c494e227`보다 이전이며, 그 사이 `/v1/debug` 제거(2026-09-03)·hallmark 후속 정정이 있었다.
8. kor-travel-weather와의 연동: `docs/integration-map.md` 대상 시스템에 weather가 없다. weather 서비스가 map의 소비자/공급자 어느 쪽인지, 또는 무관한지 미확인.
9. docker-manager Prometheus의 12701 scrape job은 "현재 없음, 배포 시 추가"(integration-map §2 다이어그램) — 실제 적용 여부는 docker-manager 조사에서 확인 필요.
10. `SKILL.md` §4는 "26개 규칙"이라 쓰지만 실제 항목은 27개(27번 codegraph 영향도). 문서 자체의 소소한 drift.
11. `map-marker-react`가 `zod ^4.4.3`을 peer로 요구하지만 admin frontend는 zod를 설치하지 않는다(hoisted 4.4.3은 map-marker-react devDependency로 설치). 실제 런타임 zod 사용처가 있는지 미확인.
12. `components.json` `style: "base-nova"`가 shadcn 공식 스타일 이름인지(Base UI 대응 프리셋) 미확인 — CLI를 쓰지 않으므로 실효는 없음.

## 12. 근거 파일 목록

저장소 상대 경로(`F:/dev/kor-travel-common-survey/ktm-main/` 기준). 모두 본 조사에서 실제로 열어 읽었다.

1. `LICENSE`
2. `README.md`
3. `CLAUDE.md`
4. `AGENTS.md`
5. `SKILL.md`
6. `CHANGELOG.md` (상단 25행)
7. `package.json` (루트)
8. `package-lock.json` (node로 `packages` 맵 조회)
9. `.npmrc`
10. `.pre-commit-config.yaml`
11. `.gitattributes`
12. `.mcp.json`, `claude.json`, `antigravity.json`, `opencode.json`, `.gemini/mcp.json`
13. `pyproject.toml` (루트)
14. `.env.example` (루트, 키 목록)
15. `alembic.ini`, `alembic/` 디렉터리 목록
16. `scripts/verify-npm-tree.mjs`
17. `scripts/verify-frontend-eslint-config.mjs`
18. `scripts/verify-react-doctor-config.mjs`
19. `scripts/verify-next-sharp.mjs`
20. `scripts/patch-redocly-openapi-core.mjs`
21. `tests/unit/test_frontend_dependency_security.py`
22. `tests/lint/` 목록
23. `.github/workflows/ci.yml`, `lint.yml`, `openapi.yml`, `frontend.yml`, `docker-images.yml`, `postgis-only.yml`
24. `docker/frontend.Dockerfile`, `docker/api.Dockerfile` (상단 40행), `docker/` 목록
25. `docker-compose.yml` (서비스·포트 grep)
26. `docs/integration-map.md` (1~200행, 섹션 헤더, §4)
27. `docs/admin-ui-modernization-gap-audit.md`
28. `docs/architecture/debug-ui-package.md` (상단 40행)
29. `docs/architecture/rest-api.md` (헤더, §1.7)
30. `docs/architecture/admin-frontend-design-rules.md` (상단 60행)
31. `docs/architecture/backend-package.md` (상단 20행)
32. `docs/architecture/` 목록
33. `docs/adr/README.md` (상단 30행)
34. `docs/tasks-rule.md` (상단 60행)
35. `docs/tasks.md` (리뷰 관련 grep)
36. `docs/journal.md` (상단 12행)
37. `docs/dev-environment.md` (헤더, 상단 40행)
38. `docs/codegraph-worktree.md` (헤더)
39. `docs/runbooks/README.md`, `docs/runbooks/agent-workflow.md` (헤더, 90~130행)
40. `docs/deploy.md` (상단 30행)
41. `docs/reports/hallmark-audit-admin-frontend-2026-08-18.md` (상단 30행)
42. `.claude/agents/README.md` (상단 30행), `.agents/.claude/.codex/.opencode/.gemini` 목록
43. `packages/kor-travel-map-admin/README.md`(존재 확인), `packages/kor-travel-map-admin/frontend/README.md` (헤더, 1~80행, 172~188행, 255~282행)
44. `packages/kor-travel-map-admin/frontend/package.json`
45. `packages/kor-travel-map-admin/frontend/components.json`
46. `packages/kor-travel-map-admin/frontend/design.md`
47. `packages/kor-travel-map-admin/frontend/postcss.config.mjs`
48. `packages/kor-travel-map-admin/frontend/next.config.ts`
49. `packages/kor-travel-map-admin/frontend/eslint.config.mjs`
50. `packages/kor-travel-map-admin/frontend/tsconfig.json`, `tsconfig.tooling.json`
51. `packages/kor-travel-map-admin/frontend/vitest.config.ts`
52. `packages/kor-travel-map-admin/frontend/doctor.config.json`
53. `packages/kor-travel-map-admin/frontend/middleware.ts`
54. `packages/kor-travel-map-admin/frontend/.env.example`, `.gitignore`
55. `packages/kor-travel-map-admin/frontend/playwright.config.ts`
56. `packages/kor-travel-map-admin/frontend/src/app/globals.css`
57. `packages/kor-travel-map-admin/frontend/src/app/layout.tsx`
58. `packages/kor-travel-map-admin/frontend/src/lib/utils.ts`, `auth.ts`, `proxy.ts`, `form-validation.ts`, `status-label.ts`, `vworld-style.ts`
59. `packages/kor-travel-map-admin/frontend/src/api/client.ts`
60. `packages/kor-travel-map-admin/frontend/src/app/api/proxy/[...path]/route.ts`, `api/auth/login/route.ts`, `api/geo/[...path]/route.ts`
61. `packages/kor-travel-map-admin/frontend/src/providers/query-client-provider.tsx`, `src/state/map.ts`
62. `packages/kor-travel-map-admin/frontend/src/components/admin-shell.tsx` (grep), `src/components/ui/*.tsx`·`*.ts` 헤더, `button-variants.ts`, `badge-variants.ts`, `data-table.tsx` 헤더, `vworld-map-view.tsx` 헤더
63. `packages/kor-travel-map-api/pyproject.toml`, `.env.example`, `README.md` (상단 60행)
64. `packages/kor-travel-map-api/src/kortravelmap/api/app.py` (1~200행, 1100~1130, 1355~1400, grep)
65. `packages/kor-travel-map-api/src/kortravelmap/api/response.py`, `cors.py`, `auth.py` (상단·상수), `settings.py` (상단·env_prefix), `prometheus.py` (grep), `route_policy.py` (enum), `routers/*.py` (prefix grep), `routers/public_status.py`
66. `packages/kor-travel-map-api/scripts/export_openapi.py` (상단 80행), `openapi.json`/`openapi.user.json`/`openapi.service.json` (paths 수·info)
67. `packages/kor-travel-map-dagster/pyproject.toml`, `src/kortravelmap/dagster/` 목록, `definitions.py`/`schedules.py`/`assets.py` (grep)
68. `packages/kor-travel-map-user-client/package.json`, `README.md` (상단 40행)
69. `packages/map-marker-react/package.json`, `README.md` (상단 40행), `src/*.ts` 헤더
70. `src/kortravelmap/` 목록, `settings.py` (grep), `cli/main.py` (grep), `geocoding.py` (grep)
71. `F:/dev/kor-travel-geo-fixes/docs/kor-travel-common-library-review.md` (§2·§3, map 인용 대조)
