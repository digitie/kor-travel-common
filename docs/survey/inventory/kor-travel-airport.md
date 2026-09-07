# kor-travel-airport 인벤토리

- 기준 커밋: `2bb1111fc322843de40a35276613feb4d67bac5b` (2026-09-06 08:09:18 +0900, "docs: record kor-travel-airport rename n150 verification and PR #16 redeploy (#17)")
- 조사일: 2026-09-06
- 조사 경로: `F:/dev/kor-travel-common-survey/kta-main` (정본 체크아웃, 작업 트리 clean — `git status --short` 출력 없음)
- 추가 조사 경로(WIP 브랜치, 읽기 전용): `F:/dev/kor-travel-airport` @ `codex/shadcn-ui-foundation` = `99b3f98e130b9dd6ae8525333c41672559d39144` (§3.2)
- 라이선스: GPL-3.0 — `LICENSE` 1~2행 "GNU GENERAL PUBLIC LICENSE / Version 3, 29 June 2007"
- 추적 파일 수: 201 (`git ls-files | wc -l`)
- 표기 규약: 본문에서 **사실**은 근거 경로를 붙인 서술, **후보**는 공통화 판단, **추정**은 근거가 간접적인 판단, **미확인**은 조사에서 확인하지 못한 것.

> 선행 검토 보고서 `F:/dev/kor-travel-geo-fixes/docs/kor-travel-common-library-review.md`(2026-09-05)는 대상 저장소를 geo/map/weather/concierge/docker-manager/Pinvi 6종으로 한정했고, `airport`·`parking` 문자열이 본문에 한 번도 등장하지 않는다(`grep -n -i -E 'airport|parking|kta'` 결과 0건). 따라서 이 저장소에 대한 선행 결론은 없으며, 본 문서가 최초 인벤토리다. 선행 보고서의 일반 권고(§7.2 "CI·lint·TypeScript 설정은 별도 검토", §7.3 "사전 빌드 CSS + CSS 변수 우선") 중 이 저장소 사실과 충돌하는 부분은 §9에서 명시한다.

## 1. 저장소 개요와 역할

1. 저장소 식별자는 `kor-travel-airport`이지만 배포되는 웹앱의 브랜드/화면 표시 이름은 계속 `parking-radar`다. 2026-09-06 ADR-007로 저장소·패키지·n150 운영 식별자만 개명했고, Next.js `metadata.title`, 백엔드 `Settings.app_name`, 백업 파일명 접두어(`parking-radar-<ts>.dump`), 쿠키/localStorage 키(`parking-radar-selection`, `parking-radar:dashboard-selection:v1`)는 그대로다 (`README.md` 1~7행, `CLAUDE.md` §1, `docs/adr/007-repo-rename-kor-travel-airport.md`, `frontend/src/app/layout.tsx`, `backend/app/core/config.py`, `frontend/src/lib/dashboard-preferences.ts`).
2. 제품 정체성: 국내 공항 주차장의 현재 잔여 주차면과 최근 7일 흐름, 요일×시간 패턴, 임계치 이벤트, 비행편 오버레이, 주차요금 계산을 제공하는 **반응형 사용자용 대시보드**다. 로그인/회원 기능은 범위 밖으로 명시돼 있다 (`docs/project-brief.md` "제외" 절, `README.md` "핵심 기능").
3. 사용자: 자가용으로 공항에 가는 여행객, 주차 혼잡 패턴을 보는 운영/기획 사용자 (`docs/project-brief.md` "목표 사용자").
4. **별도 admin 앱은 없다.** 운영 표면은 같은 단일 페이지 안의 백업/복원 패널(`frontend/src/components/backup-panel.tsx`)과 `/v1/admin/*` 엔드포인트(수집 상태, 백업 목록/생성/다운로드/복원)이며, 앱 레벨 인증 없이 내부망/게이트웨이 보호를 전제로 한다 (`docs/adr/003-unauthenticated-backup-network-restriction.md`, `backend/app/main.py` 692~880행). 사용자 지시의 "kor-travel-airport Admin"은 이 패널·엔드포인트 묶음으로 해석해야 한다(§9 참고).
5. 스택: FastAPI + SQLAlchemy 2(async) + PostgreSQL 16 + Alembic / Next.js App Router + React + TypeScript / pytest + Vitest + Playwright / Docker Compose (`README.md` "기술 스택", `docs/architecture/architecture.md`).
6. 형제 프로젝트 연동은 **코드 호출이 아니라 라이브러리 소비와 규약 이식**이다. 백엔드는 `python-krairport-api`(krairport)와 `python-kasi-api`(kasi)를 git 커밋 고정으로 소비하고(ADR-004/006), 문서 구조·OpenAPI export·`/v1` 버저닝은 `kor-travel-map`에서, DB 분리 compose 패턴은 `kor-travel-docker-manager`에서 가져왔다 (`backend/pyproject.toml`, `docs/adr/004-*.md`, `docs/adr/005-*.md`, `docs/tasks-done.md` T-028/T-032). geo/weather/concierge/pinvi 서비스에 대한 HTTP 호출은 없다(§7).
7. 운영: n150(`<prod-address>`)에서만 Docker/PostgreSQL을 실행하고, 13번(`<prod-address>`)은 읽기 전용 legacy다. 공개 포트는 DB `14000`(loopback), API `14001`, web `14002`, 외부 도메인 `https://<prod-host>` / `https://<prod-host>` (`README.md` "<prod-address> 운영 배포", `docs/runbooks/deployment.md`).
8. 진행 중 initiative: WIP 브랜치 `codex/shadcn-ui-foundation`이 T-033(Tailwind v4 + shadcn/ui 기반 도입)을 커밋했고, 후속 T-034~T-038(컴포넌트 교체, 라우트 기반 앱 셸, 과거 자료 조회, Hallmark 재감사/재설계)이 `docs/tasks.md`에 등록돼 있다(§3.2).

## 2. 저장소 구조

최상위 트리(`git ls-files` 기준, 디렉터리별 파일 수):

| 경로 | 파일 수 | 역할 | 근거 |
|---|---|---|---|
| `AGENTS.md` / `CLAUDE.md` / `SKILL.md` / `design.md` / `README.md` | 5 | 에이전트·사람 진입 문서(§5) | 루트 |
| `LICENSE` | 1 | GPL-3.0 | 루트 |
| `.agents/skills/` | 23 | 벤더링된 postgres 계열 skill 7종(timescale/pg-aiguide 원본, Apache-2.0) | `.agents/skills/postgres/SKILL.md` 18~19행 |
| `.claude/skills/` | 15 | `.agents/skills/`와 같은 skill의 사본(`agents/openai.yaml` 제외) | `git ls-files .claude/skills` |
| `.claude/agents/` | 6 | 역할 에이전트 md 5종 + README | `.claude/agents/README.md` |
| `.codex/agents/`, `.codex/config.toml` | 7 | Codex용 역할 에이전트 toml 6종 + MCP 설정 | `.codex/config.toml` |
| `.hallmark/` | 2 | Hallmark preflight/log 기록 | `.hallmark/preflight.json` |
| `.github/workflows/ci.yml` | 1 | CI 3 job(§6) | |
| `backend/` | 27 | FastAPI 앱 `app/`, `alembic/`, `tests/`, `pyproject.toml`, `uv.lock`, `Dockerfile`, `entrypoint.sh` | |
| `frontend/` | 28 | Next.js 앱(`src/app`, `src/components`, `src/lib`, `tests/`, `e2e/`) | |
| `docs/` | 47 | 정본 문서(§5) | |
| `scripts/` | 12 | 배포/컷오버/마이그레이션/OpenAPI export 스크립트 | |
| `deploy/odroid/` | 3 | legacy ODROID 배포(의도적으로 종료되는 스크립트) | `deploy/odroid/README.md` |
| `docker-compose*.yml` | 4 | app / db / live / odroid(disabled) | §6 |
| `.env.example`, `.env.server14.example`, `.gitattributes`, `.gitignore`, `.dockerignore` | 5 | 설정 예시·git 규약 | |

- 모노레포가 아니다. npm workspace/uv workspace 선언 없음 (`frontend/package.json`, `backend/pyproject.toml`).
- 프론트 1개(`frontend/`), 백엔드 패키지 1개(`backend/`, 배포 이름 `kor-travel-airport-backend`).

## 3. 프론트엔드

### 3.1 parking-radar 웹앱 — main (`frontend/`)

**프레임워크/런타임** (`frontend/package.json`, `frontend/package-lock.json` lockfileVersion 3)

| 항목 | 선언 | 설치(lock) |
|---|---|---|
| next | `^16.3.2` | 16.3.2 |
| react / react-dom | `^19.2.8` | 19.2.8 |
| typescript | `^7.0.2` | 7.0.2 |
| node | `engines` 없음. Dockerfile `node:22-alpine`, CI `node-version: "22"` | — |
| packageManager | 필드 없음. lockfile은 `package-lock.json`(npm) | — |
| 스크립트 | `dev`/`start` = `next dev|start --hostname 0.0.0.0 --port 3000`, `test`=`vitest`, `test:e2e`=`playwright test`, `e2e:install` | — |

- `lint`/`typecheck` 스크립트 없음. CI는 `npx tsc -p tsconfig.test.json --noEmit`를 직접 호출한다 (`.github/workflows/ci.yml` frontend job).
- ESLint·Prettier 미설치·미설정(`package.json`, lock에 `eslint` 없음, 저장소 전체 `grep -r -i eslint` 결과는 벤더링된 `.claude/agents/backend-developer.md` 1건뿐).

**스타일** — main은 **Tailwind를 전혀 사용하지 않는다** (사실: lock에 `tailwindcss`/`@tailwindcss/postcss` 없음, `postcss.config.*` 없음, `tailwind.config.*` 없음).

- 구성: 순수 CSS 2파일. `frontend/src/app/tokens.css`(56행, "Hallmark stamp" 헤더, OKLCH 토큰) + `frontend/src/app/globals.css`(1,844행, `@import "./tokens.css"` 후 의미 별칭·컴포넌트 클래스·미디어 쿼리).
- 토큰 목록(`tokens.css`):
  - 색: `--color-canvas`, `--color-surface`, `--color-surface-raised`, `--color-ink`, `--color-muted`, `--color-line`, `--color-accent`, `--color-accent-strong`, `--color-accent-soft`, `--color-button-bg`, `--color-button-ink`, `--color-teal`, `--color-red`, `--color-yellow`, `--color-input`, `--color-grid`, `--color-sticky` (전부 `oklch()`).
  - 그림자: `--shadow-card`, `--shadow-focus`.
  - radius: `--radius-card: 16px`, `--radius-control: 10px`.
  - 폰트: `--font-sans: "Pretendard Variable", "Apple SD Gothic Neo", "Noto Sans KR", system-ui, sans-serif`, `--font-mono: "JetBrains Mono", "Consolas", monospace`.
  - 간격: `--space-1`(4px) ~ `--space-10`(40px) 8단계.
  - 모션·z-index 토큰: **없음**. `design.md`는 "160ms opacity/transform"을 규정하지만 CSS 토큰으로 존재하지 않는다(`grep transition` 결과 reduced-motion 규칙 1건만).
- `globals.css :root`는 토큰을 의미 별칭(`--bg`, `--surface`, `--ink`, `--muted`, `--line`, `--accent`, `--accent-strong`, `--accent-soft`, `--button-bg`, `--radius`, `--input-bg`, `--grid-line`, `--sticky-bg`, `--font-ui`)으로 재매핑한다(4~28행).
- 라이트/다크: `@media (prefers-color-scheme: dark)`만 사용(`tokens.css` 36~55행, `globals.css` 49행·1595행). 클래스 토글(`.dark`, `data-theme`) 없음, `next-themes` 없음.
- 폰트: Pretendard를 첫 후보로 선언하지만 **폰트 로딩 코드가 없다**(`grep -rn '@font-face|next/font|fonts.googleapis' frontend/src` 결과 0건). 실제 렌더는 사용자 시스템 폰트에 의존한다(사실).
- 아이콘: 없음(lucide 미설치). 애니메이션 라이브러리: 없음.
- Hallmark 규칙 "토큰 밖 임의 색상 금지"(`SKILL.md` §4 #7)에도 불구하고 `globals.css`에 raw `rgba()`/hex가 22건 남아 있다(예: 312~333행 `.tone-*` 배경, 437~530행 차트 stroke/fill `#2563eb`, `#db2777`). 사실.

**UI 프리미티브**: 없음(radix-ui, @base-ui/react, shadcn 모두 lock에 없음). `components.json` 없음. 폼 컨트롤은 네이티브 `select`/`button`/`input`/`details`를 CSS 클래스로 꾸민다(`dashboard-screen.tsx`, `globals.css`).

**컴포넌트 인벤토리** (`frontend/src/components/`, `components/ui/` 디렉터리는 main에 없음)

| 파일 | 행 | 역할 | 헤더 출처 표기 |
|---|---|---|---|
| `dashboard-app.tsx` | 531 | 데이터 로딩·15초 자동 갱신·viewport 모드·선택 복원을 담는 컨테이너 | 없음 |
| `dashboard-screen.tsx` | 750 | 상태 헤더·컨트롤 밴드·현황 표/카드·분석 패널·`mobile-disclosure` | 없음 |
| `history-chart.tsx` | 480 | 최근 7일 SVG 계단형 차트, 터치/hover 툴팁 | 없음 |
| `daily-flight-overlay-chart.tsx` | 439 | 0~24시 7일 겹침 + 비행편 마커 SVG 차트 | 없음 |
| `backup-panel.tsx` | 193 | 백업 목록/생성/다운로드/복원(무인증, 내부망 경고) | 없음 |
| `fee-calculator.tsx` | 164 | 주차요금 계산 폼 | 없음 |

- 앱 레벨 공유 부품(admin-shell, filter-bar, pagination-bar, status-badge, data-table, empty-state, section-card, stat-strip, copy-button, json-viewer, login-form, confirm-dialog, help-tip, vworld map view): **모두 해당 없음**. 상태 배지는 `.tone-*` CSS 클래스(`globals.css` 310~335행)로만 존재한다.
- 파일 헤더에 이식 출처(Hallmark 등)를 적은 컴포넌트는 없다. Hallmark stamp는 `tokens.css` 1행, `globals.css` 1행에만 있다.

**상태/데이터**

- @tanstack/react-query, zustand, react-hook-form, zod: 모두 미설치. 상태는 `useState`/`useEffect`/`startTransition`(`dashboard-app.tsx` 4행).
- API 클라이언트: 수작업 `buildApiClient(apiBaseUrl?)` 팩토리(`frontend/src/lib/api.ts` 90~230행). 모든 경로에 `/v1/`을 직접 붙인다(`/health` 제외). 생성기(openapi-typescript 등) 없음; 타입은 `frontend/src/lib/types.ts`에 수작업 정의.
- fetch 래퍼: `getJson<T>(url, init)` — `cache: "no-store"`, multipart가 아니면 `Content-Type: application/json` 자동, 실패 시 `readErrorMessage`가 `payload.detail`을 읽어 `ApiError(message, status)`를 던진다(`api.ts` 25~90행). RFC7807 응답의 `detail` 필드에 의존한다(ADR-005와 정합).
- 선택 상태 영속: localStorage 우선 + 1년 쿠키 fallback(`frontend/src/lib/dashboard-preferences.ts`).

**인증 경계**

- 앱 레벨 인증 없음(ADR-003). 세션/CSRF/신원 전달 없음.
- Next route handler `frontend/src/app/api/backend/[...path]/route.ts`가 same-origin `/api/backend/*`를 `BACKEND_INTERNAL_URL`로 프록시한다. 특징: 메서드·경로 allowlist(`isAllowedBackendRequest`, 41~84행; `admin/collect` POST는 의도적으로 제외), 요청 헤더는 `accept`/`content-type`만 전달 + `x-forwarded-host`/`x-forwarded-proto` 세팅, 응답 헤더 allowlist, 항상 `cache-control: no-store`, 요청 타임아웃(`BACKEND_PROXY_TIMEOUT_MS` 10s / 백업은 900s)과 본문 읽기 타임아웃 스트림 래퍼, 502/504 시 `{detail, code}` JSON.
- `frontend/next.config.ts`: 보안 헤더 5종(`X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy`, `Permissions-Policy`, `Strict-Transport-Security`)을 전 경로에, `/`와 `/api/backend/*`에는 `Cache-Control: no-store` 추가. `middleware.ts` 없음.

**라우팅/화면**: `app/layout.tsx`(`lang="ko"`), `app/page.tsx`(`/`, `force-dynamic`), `app/api/backend/[...path]/route.ts`. 사용자 화면 1개, admin 화면 0개(백업 패널은 `/` 안의 접힘 섹션). T-035가 `/analytics`·`/history`·`/fees`·`/backup` 라우트 분리를 계획 중(WIP `docs/tasks.md`).

**반응형/모바일**

- CSS 브레이크포인트(`globals.css`): `max-width: 980px`(1312행), `860px`(1306·1331행), `560px`(1550·1823행), `380px`(1585행).
- JS 분기: `useViewportMode()`가 `window.innerWidth < 860`을 `resize` 리스너로 추적(`dashboard-app.tsx` 102~116행; `matchMedia` 아님). SSR/초기값 `null`일 때는 데스크톱 마크업을 `.responsive-desktop`(≤860px에서 `display:none`)으로 렌더한다(`dashboard-screen.tsx` 194~214행).
- 모바일 전용: `<details class="mobile-disclosure">` 접힘 섹션, 카드 그리드(`data-testid="mobile-lot-grid"`), 히트맵 첫 열 고정, 표/차트는 자체 `overflow-x: auto`.
- 루트는 `overflow-x: clip`(html/body), 페이지 전역 `overflow-x: hidden` 금지(`SKILL.md` §4 #6, `design.md` Layout contract).
- 터치: 차트 드래그 임계 `TOUCH_DRAG_THRESHOLD_PX = 12`(`history-chart.tsx` 21행), ≤560px 히트맵 셀 `min-width: 44px`(`globals.css` 1578행).
- 검증 폭: 320/375/414/768(/1440) CSS px(`design.md`, `SKILL.md` §5, `docs/runbooks/testing.md` 255행).

**i18n / 접근성 / focus / reduced-motion**

- i18n 라이브러리 없음. 한국어 문자열 하드코딩. `<html lang="ko">`.
- focus 레시피: `:where(button, input, select, summary, a):focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; box-shadow: var(--shadow-focus); }`(`globals.css` 199~203행) + 차트 hit-target/chip/marker별 focus-visible 규칙(546·645·852·931행).
- reduced-motion: `@media (prefers-reduced-motion: reduce)`에서 `transition-duration`/`animation-duration` 0.01ms, `scroll-behavior: auto`(1836~1843행).
- aria 사용: `aria-*` 속성 backup-panel 4, daily-flight-overlay 5, dashboard-screen 3, history-chart 1건. 접근성 규칙 문서는 `design.md` "Interaction states"(idle/hover/focus-visible/disabled/success/error) 한 단락뿐.

**테스트·품질**

- Vitest 4.1.11: `frontend/vitest.config.ts`(jsdom, `globals: true`, `setupFiles: vitest.setup.ts`, 15s timeout, `e2e/**` 제외, `@` alias). `vitest.setup.ts`는 jest-dom 등록 + in-memory `localStorage` shim.
- 테스트 파일 10개(`frontend/tests/*.test.ts(x)`: api, backend-proxy-route, backup-panel, daily-flight-overlay-chart, dashboard-app, dashboard-preferences, dashboard, fee-calculator, format, history-chart).
- Playwright 1.62.1: `frontend/playwright.config.ts`(chromium 1 project, `E2E_BASE_URL` 기본 `http://127.0.0.1:3000`, json reporter). `frontend/e2e/live-dashboard.spec.ts`는 실제 n150을 대상으로 `/api/backend/health`의 `release_sha`가 `EXPECTED_RELEASE_SHA`와 같은지, collector 상태(300s/180s), 선택 기억, 백업 컨트롤 노출을 검증한다.
- react-doctor: 없음. ESLint: 없음.
- `frontend/tsconfig.json`: `strict: true`, `target ES2022`, `moduleResolution bundler`, `paths @/*`, `tests`/`e2e` 제외; `tsconfig.test.json`이 tests를 별도 포함(`types: vitest/globals, node`).

**빌드/배포**

- `next.config.ts`: `reactStrictMode: true`, `headers()`만. `output`, `transpilePackages`, `images` 설정 없음.
- `frontend/Dockerfile`: `node:22-alpine`, `npm ci && npm run build`, `EXPOSE 3000`, `npm run start`(standalone 아님). 빌드 인자 `NEXT_PUBLIC_API_BASE_URL`, `NEXT_PUBLIC_API_PORT`; 런타임 `BACKEND_INTERNAL_URL=http://localhost:8000` 기본.
- 포트: 컨테이너 3000 → 호스트 `${PUBLIC_WEB_PORT:-14002}`(`docker-compose.yml`).

**디자인 문서**

- `design.md`(38행, **영문**): "modern-minimal workbench + restrained airport-orange accent", 라이트 warm neutral / 다크 blue-charcoal, 16px 패널·10px 컨트롤·1px 보더, 모노스페이스는 timestamp에만, 160ms 모션, OKLCH 토큰 정본 `frontend/src/app/tokens.css`, 레이아웃 계약 5단(상태 헤더→컨트롤 밴드→현황→지연 분석→운영 푸터), 금지 게이트(장식 그라디언트·이탤릭 헤딩·generic hero CTA·page-wide hidden overflow·무한 카드 그리드·small-screen state 누락).
- `docs/reports/hallmark-audit-2026-08-22.md`(36행): 감사 결과와 재설계 결정. `.hallmark/preflight.json`이 scope/mode/target_host를 기록.

### 3.2 WIP 브랜치 `codex/shadcn-ui-foundation` (`F:/dev/kor-travel-airport`, 읽기 전용)

**상태 (사실)**: 지시문은 "dirty, 미커밋"이라 했으나 조사 시점 worktree는 **clean**이다. `git status --short` 출력 없음, `git stash list` 없음, `git diff --stat`/`--cached` 없음, 무시 파일만 `.claude/scheduled_tasks.lock`, `backend/kor_travel_airport_backend.egg-info/`, `frontend/tsconfig.tsbuildinfo`. 브랜치는 main(`2bb1111`) 위 **단일 커밋** `99b3f98e130b9dd6ae8525333c41672559d39144`(2026-09-06 09:51:22 +0900, "feat: add shadcn/ui foundation on Tailwind v4 (T-033)", Co-Authored-By Claude Sonnet 5)이며 `merge-base`가 main HEAD와 같다. `origin`은 `https://github.com/digitie/kor-travel-airport.git`. PR 개설 여부는 미확인(gh 미사용).

**변경 범위** (`git show --stat HEAD`: 61 files, +17,157 / −1,999)

| 구분 | 파일 | 내용 |
|---|---|---|
| 신규 설정 | `frontend/components.json` | `style: "base-nova"`, `rsc: true`, `tsx: true`, `tailwind.config: ""`, `tailwind.css: src/app/globals.css`, `baseColor: neutral`, `cssVariables: true`, `prefix: ""`, `iconLibrary: lucide`, `rtl: false`, aliases `@/components`·`@/lib/utils`·`@/components/ui`·`@/lib`·`@/hooks`(`src/hooks` 디렉터리는 없음), `menuColor: default`, `menuAccent: subtle`, `registries: {}` |
| 신규 설정 | `frontend/postcss.config.mjs` | `@tailwindcss/postcss` 단일 플러그인, autoprefixer 없음(주석으로 명시) |
| 신규 코드 | `frontend/src/lib/utils.ts` | `export { cn } from "cn"` (clsx+tailwind-merge 조합이 아니라 npm `cn` 0.2.5 패키지 재수출) |
| 신규 코드 | `frontend/src/components/ui/button.tsx` | `@base-ui/react/button` + `cva` 기반 shadcn Button(variant 6종, size 9종, `data-slot="button"`) — **JSX에서 아직 사용되지 않음** (커밋 메시지 "No component JSX changed yet") |
| 수정 | `frontend/package.json` | dependencies에 `@base-ui/react ^1.8.0`, `@tailwindcss/postcss ^4.3.3`, `class-variance-authority ^0.7.1`, `cn ^0.2.5`, `lucide-react ^1.41.0`, `postcss ^8.5.28`, `shadcn ^4.21.0`, `tailwindcss ^4.3.3`, `tw-animate-css ^1.4.0` 추가. devDependencies 변화 없음 |
| 수정 | `frontend/package-lock.json` | +8,419행 규모 갱신(설치 버전은 §10) |
| 수정 | `frontend/src/app/globals.css` | 1,844 → 1,932행. 아래 상세 |
| 수정 | `frontend/next.config.ts` | `agentRules: false` 추가(Next 16 자동 생성 `frontend/AGENTS.md`/`CLAUDE.md` 억제 — 루트 2파일만 entry로 두는 정책 유지) |
| 수정 | `.gitignore` | `.playwright-mcp/` 추가 |
| 수정 | `docs/tasks.md` | T-033~T-038 initiative 등록(계획 파일은 사용자 로컬 `C:\Users\digit\.claude\plans\iridescent-finding-parasol.md`를 가리킴 — 저장소 밖) |
| 신규 벤더링 | `.agents/skills/shadcn/*`(15), `.agents/skills/migrate-radix-to-base/*`(10), 동일 사본 `.claude/skills/*`(25) | shadcn/ui 공식 skill(`npx skills add shadcn/ui`). `skills-lock.json`이 source·hash 기록 |
| 변경 없음 | `frontend/src/app/tokens.css` | `git diff --stat main..HEAD -- tokens.css` 출력 없음 — OKLCH 토큰 정본 유지 |

**globals.css 도입 방식 (사실)**

- 헤더: `@import "tailwindcss"; @import "./tokens.css"; @import "tw-animate-css"; @import "shadcn/tailwind.css";` (2~5행). Tailwind v4 CSS-first이며 `tailwind.config.*`는 없다.
- `:root`에 shadcn 시맨틱 변수(`--background`, `--foreground`, `--card`, `--popover`, `--primary`, `--secondary`, `--muted-foreground`, `--accent-foreground`, `--destructive`, `--border`, `--input`, `--ring`, `--chart-1..5`)를 **전부 `var(--color-*)` 토큰 파생값으로 배선**했다(shadcn 기본 회색 팔레트 미사용). 다크 모드는 `tokens.css`의 `prefers-color-scheme` 재정의를 상속하므로 별도 `.dark` 블록을 두지 않았다(주석 7~9행, 1917~1919행).
- **이름 충돌 해결**: 기존 별칭 `--muted`(텍스트 색), `--accent`(강조색), `--radius`(카드 16px)가 shadcn의 `--muted`(배경), `--accent`(배경), `--radius`(기준 radius)와 의미가 달랐다. WIP는 `--muted`→`--color-surface`, `--accent`→`--color-accent-soft`, `--radius`→`--radius-control`(10px)로 재정의하고, 기존 규칙 약 30곳을 `var(--muted-foreground)`, `var(--color-accent)`, `var(--radius-card)`로 고쳤다(diff 전반; 커밋 메시지가 "CLI가 조용히 덮어썼던 충돌"로 설명).
- 말미에 `@theme inline { --font-heading/--font-sans, --color-* ← shadcn 변수, --radius-sm..4xl = calc(var(--radius) * k) }`(1876~1915행)와 `@layer base { * { @apply border-border outline-ring/50 } body { @apply bg-background text-foreground } html { @apply font-sans } }`(1923~1932행).
- shadcn CLI가 주입하려 한 Geist Google Font는 되돌렸고 Pretendard 우선 스택을 유지했다(커밋 메시지; `tokens.css` 무변경으로 확인). 폰트 로딩 코드는 여전히 없다.
- 검증 주장(커밋 메시지, 재현 미확인): 데스크톱·375px에서 픽셀 동일, `npm run build`/vitest 통과.

**common 도입 시 이 브랜치 취급에 대한 근거**

- 이 브랜치는 "토큰 정본을 유지한 채 shadcn 시맨틱 변수로 브릿지"하는 방식의 **실제 작동 사례**다. common이 토큰→shadcn 변수 매핑 규약을 정하면 이 브랜치의 `:root` 블록과 `@theme inline` 블록이 참조 구현이 된다(후보).
- 반대로 common이 `--muted`/`--accent`/`--radius`를 shadcn 의미로 예약하면 main의 기존 별칭과 충돌한다 — 이 브랜치가 이미 겪은 충돌이므로 common 토큰 네이밍은 이 사례를 회피 조건으로 삼아야 한다(사실 기반 권고).
- 다크 모드가 `prefers-color-scheme` 전용(`.dark` 클래스·`@custom-variant dark` 없음)이라, common이 `next-themes`/클래스 토글을 전제로 하면 이 앱은 추가 작업이 필요하다(사실).
- `shadcn`·`postcss`·`@tailwindcss/postcss`가 `devDependencies`가 아닌 `dependencies`에 있고, `cn` 패키지를 쓴다. shadcn 4.21 `base-nova` 스타일의 CLI 기본값인지는 **미확인**. common 버전 일치화 정책이 clsx+tailwind-merge를 요구하면 이 브랜치와 어긋난다.
- 이 브랜치의 후속 T-034(컴포넌트 shadcn 교체)·T-035(pinvi `AppShell` 패턴 모바일 하단 탭바)는 common의 첫 소비 지점이 될 수 있다. common이 확정되기 전에 T-034가 앱 로컬 `components/ui/*`를 늘리면 재이식 비용이 생긴다(추정).

## 4. 백엔드

### 4.1 kor-travel-airport-backend (`backend/`)

**빌드/런타임** (`backend/pyproject.toml`, `backend/uv.lock`, `backend/Dockerfile`)

- `requires-python = ">=3.12"`; 빌드 `setuptools>=69` + wheel(`setuptools.build_meta`); 패키지 `app*`.
- lockfile: `uv.lock`(CI `uv sync --extra dev --locked`). **Docker 이미지는 `pip install -e ".[dev]"`**(uv 미사용, `python:3.12-slim`, `git`·`postgresql-client` apt 설치). 로컬 WSL 1차 테스트는 `python -m pytest`(도구 미지정). 즉 uv/pip 혼용(사실).
- 의존 선언 범위 vs 설치(§10 표 참조): fastapi `>=0.141,<1.0`, sqlalchemy `>=2.0.52,<3.0`, alembic `>=1.19,<2.0`, asyncpg `>=0.31,<1.0`, aiosqlite `>=0.22`, httpx `>=0.28`, pydantic-settings `>=2.15`, python-multipart `>=0.0.32`, uvicorn[standard] `>=0.52`, `python-kasi-api @ git+...@51c39c1b...`, `python-krairport-api @ git+...@cbe4d138...`(PEP 508 direct ref — `[tool.uv.sources]`를 Docker pip가 못 읽어 채택, `docs/journal.md` 2026-08-23 T-030). dev: anyio, pytest `>=9.1`, pytest-asyncio `>=1.4`, pytest-cov `>=7.1`.
- **없음**: structlog, prometheus-client, typer, tenacity, dagster, psycopg, argon2, ruff, mypy, import-linter, testcontainers (pyproject·uv.lock·저장소 grep 결과).

**앱 구성** (`backend/app/main.py` 1,150행 — 라우트 전부 단일 파일)

- 앱 팩토리 `create_app(settings: Settings | None = None) -> FastAPI`(109행). `lifespan`에서 `init_database`, 서비스 객체를 `app.state`에 부착, 샘플 시드, `asyncio.create_task(_run_scheduler(app))`(자체 스케줄러, APScheduler 아님).
- 라우터: `APIRouter()` 1개를 `app.include_router(router, prefix="/v1")`(1012행). `/health`만 앱 직결(238행). 하위 prefix 규약은 경로 문자열로만 존재: `/v1/parking/*`, `/v1/parking/analytics/*`, `/v1/dashboard/*`, `/v1/flights/status`, `/v1/holidays/summary`, `/v1/fees/calculate`, `/v1/admin/*`. `/debug`, `/ops`, `/v2` 없음. `Settings.api_prefix: str = ""`는 선언만 있고 라우터에 적용되지 않는다(`config.py` 40행, main.py grep 결과).
- 미들웨어: `TrustedHostMiddleware`(trusted_hosts 있을 때), `CORSMiddleware(allow_credentials=False, allow_methods=[GET,POST,OPTIONS], allow_headers=[Content-Type])`, 커스텀 `@app.middleware("http") add_security_headers`(nosniff/DENY/Referrer-Policy/Permissions-Policy, `x-forwarded-proto=https`일 때만 HSTS)(198~216행). 프론트 `next.config.ts`와 같은 헤더 집합이 두 곳에 중복 정의돼 있다(사실).
- 에러 envelope: RFC7807 `application/problem+json`. `HTTPException` 핸들러(160~176행)와 `RequestValidationError` 핸들러(178~196행, 422)가 `{type: "about:blank", title, status, detail, instance}`를 반환. 성공 응답 envelope(`{data, meta}`)은 **의도적으로 범위 밖**(ADR-005 "후속").
- 페이지네이션: 규약 없음. `days`/`interval_minutes`/`future_hours`/`limit` 쿼리 파라미터로 범위를 자른다(`api.ts`, main.py 408~460행).
- 인증: 없음(세션/토큰/ServiceToken/argon2 전무). `docs_url`/`redoc_url`/`openapi_url`은 `enable_api_docs`로 게이트(154~158행).
- rate limit: 클라이언트 요청 제한 없음. 외부(data.go.kr) 한도 초과 시 `UPSTREAM_RATE_LIMIT_BACKOFF_SECONDS` 동안 건너뛰는 백오프만 있다(`services/collection.py`, `services/flight_status.py` `KrairportRateLimitError`).

**OpenAPI**

- `scripts/export_openapi.py`: 메모리 SQLite 설정으로 `create_app` 후 `app.openapi()`를 `docs/openapi.json`(2,900행, `sort_keys`, `ensure_ascii=False`)에 기록. 독스트링이 kor-travel-map `packages/kor-travel-map-api/scripts/export_openapi.py` 관행을 따른다고 명시.
- `docs/openapi.json`: `openapi 3.1.0`, `info.title "parking-radar"`, `info.version "0.1.0"`, `servers`/`tags` 없음, operationId는 FastAPI 자동 생성(`parking_current_v1_parking_current_get` 형태). 22 paths, 37 schemas.
- CI drift 검사: **없음**(ADR-005 "결과(부정)"에 명시). 코드의 라우트 22개와 openapi.json 22 paths는 집합이 일치함을 확인(사실). 스키마 수준 최신 여부는 미확인.
- 버전 관리: URL `/v1` 고정, `info.version`은 pyproject `0.1.0`과 별개 하드코딩(FastAPI 기본값).

**설정** (`backend/app/core/config.py`)

- `pydantic_settings.BaseSettings`, `env_file=".env"`, `case_sensitive=False`, `extra="ignore"`, **env prefix 없음**. CSV 문자열을 property로 list화(`supported_airport_codes`, `cors_origins`, `trusted_hosts`), `effective_collect_interval_seconds = max(1, interval − safety_buffer)`.
- `.env.example` 키(요약): `DATABASE_URL`, `RELEASE_SHA`, `APP_TIMEZONE`, `ENABLE_SCHEDULER`, `ENABLE_MANUAL_COLLECT`, `SEED_SAMPLE_DATA`, `USE_SAMPLE_CLIENT_WHEN_NO_KEY`, `ENABLE_INCHEON_COLLECTION`, `ENABLE_INCHEON_FEE_COLLECTION`, `ENABLE_FEE_COLLECTION`, `COLLECT_INTERVAL_SECONDS`, `MANUAL_COLLECT_MIN_INTERVAL_SECONDS`, `UPSTREAM_RATE_LIMIT_BACKOFF_SECONDS`, `API_TIMEOUT_SECONDS`, `ENABLE_FLIGHT_STATUS_MARKERS`, `FLIGHT_STATUS_CACHE_SECONDS`, `HOLIDAY_CACHE_SECONDS`, `AIRPORT_CODES_CSV`, `CORS_ORIGINS_CSV`, `TRUSTED_HOSTS_CSV`, `ENABLE_API_DOCS`, `BACKEND_INTERNAL_URL`, `NEXT_PUBLIC_API_BASE_URL`, `BACKUP_DIR`, `BACKUP_RETENTION_COUNT`, `BACKUP_COMMAND_TIMEOUT_SECONDS`, `BACKUP_UPLOAD_TIMEOUT_SECONDS`, `BACKUP_STORAGE_LIMIT_BYTES`, `DATA_GO_KR_SERVICE_KEY`. `.env.server14.example`은 여기에 `POSTGRES_*`, `PUBLIC_WEB_PORT=14002`, `PUBLIC_API_PORT=14001`, `POSTGRES_BIND_HOST=127.0.0.1`, `POSTGRES_HOST_PORT=14000`, `SCHEDULER_SAFETY_BUFFER_SECONDS=120`, `BACKUP_PROXY_*_MS=900000`을 더한다.

**관측성**

- 로깅: 표준 `logging.getLogger(__name__)`(main.py 106행, collection.py). 구조화 로깅 없음. 포맷 설정은 alembic.ini에만 있음.
- 메트릭: 없음(접두 규약 없음).
- health: `GET /health` → `HealthResponse{status, database, seeded, release_sha}`(DB count 쿼리 포함). 별도 `/ready`/`/version` 없음. `release_sha`는 배포 검증 계약(`scripts/deploy-server14.sh`, e2e).

**DB**

- 스키마 분리 없음(모델에 `schema=` 없음). 테이블 7개: `airports`, `parking_lots`, `collection_runs`, `raw_api_responses`, `parking_snapshots`, `analytics_caches`, `parking_fee_rules`(`backend/app/models.py`). `JSON().with_variant(JSONB, "postgresql")`, `DateTime(timezone=True)`.
- Alembic: `backend/alembic/versions/0001_initial.py`, `0002_integrity_and_freshness.py`, `0003_legacy_source_identity.py` — 파일명 = revision id(`NNNN_slug`). `alembic/env.py`는 `get_settings().database_url`을 asyncpg URL로 정규화해 async 실행. `app/db/session.py`의 `ALEMBIC_HEAD = "0003_legacy_source_identity"` 상수를 PostgreSQL 기동 시 `alembic_version`과 대조해 불일치면 `RuntimeError`(사실 — 마이그레이션 누락 fail-fast). SQLite는 `create_all` + 수동 인덱스.
- 세션: `create_async_engine(pool_pre_ping, pool_recycle=1800, pool_size=5, max_overflow=5; 테스트 시 NullPool)`, `async_sessionmaker(expire_on_commit=False)`, 요청별 `get_db` 의존성.
- PostGIS: 없음.

**백업/복원, 스케줄, CLI**

- 백업/복원: `services/backup_restore.py`가 `pg_dump --format=custom --no-owner --no-acl` / `pg_restore --clean --if-exists --exit-on-error`를 subprocess로 실행, 파일명 정규식 `^parking-radar-[0-9T]{15}Z(-[A-Za-z0-9_-]+)?\.dump$`, 비밀번호는 `PGPASSWORD`로만 전달, 복원 전 자동 pre-restore dump, scheduler 활성 시 409(`docs/architecture/backup-restore.md`). `scripts/n150-backup-cron.sh`가 3일마다 `POST /v1/admin/backups`.
- Dagster: 없음. 스케줄러는 lifespan 내 `asyncio` 태스크.
- CLI(typer): 없음. `scripts/*.py`는 argparse/직접 실행 스크립트(`export_openapi.py`, `migrate_sqlite_to_postgres.py`, `migrate_http_history.py`, `reconcile_parking_lots.py`, `verify_cutover.py`, `observe_cutover.py`).

**테스트**

- `backend/tests/` 평면 구조(unit/integration 분리 없음): `conftest.py` + `test_analytics.py`, `test_api.py`, `test_backup_restore.py`, `test_collection_service.py`, `test_cutover_guards.py`, `test_fee_calculator.py`, `test_flight_status.py`, `test_holidays.py`, `test_lifespan.py`, `test_parsers.py` + `fixtures/`(XML/JSON 4개).
- DB: 기본 `sqlite+aiosqlite`(tmp_path); `TEST_DATABASE_URL`/`DATABASE_URL`이 PostgreSQL이면 `TRUNCATE ... RESTART IDENTITY CASCADE`로 초기화(conftest). testcontainers 없음 — CI는 GitHub `services: postgres:16`.
- `pytest.ini_options`: `testpaths=["tests"]`, `asyncio_mode="auto"`. FastAPI `TestClient` 사용.
- coverage gate: **없음**(`docs/test-strategy.md` "커버리지 현황"에 임계값 미강제라고 명시). ruff/mypy/import-linter: 없음.

## 5. 문서·에이전트 규약

**진입 파일**

| 파일 | 행 | 역할 | 언어 |
|---|---|---|---|
| `CLAUDE.md` | 77 | Claude용 1쪽 요약(정식 정책 아님; 상충 시 CLAUDE.md를 고침) | 한국어 |
| `AGENTS.md` | 201 | 정식 정책(Codex/Antigravity entry). 목표·문서 순서·언어 정책·지시 우선순위·행동 원칙(Think Before Coding 등 5개)·runbook·provider 원칙·백엔드/프론트/테스트 원칙·체크리스트 | 한국어(원칙 소제목만 영문) |
| `SKILL.md` | 66 | 상세 매뉴얼: 계층 책임, 데이터·시간 규칙, 금지 9개, 검증 게이트 명령 | 한국어 |
| `design.md` | 38 | Hallmark 디자인 방향 | **영문** |
| `README.md` | 341 | 사람용 개요·운영·API 목록·문서 인덱스 | 한국어 |

- 지시 우선순위(`AGENTS.md` "지시 우선순위"): 사용자 요청 → AGENTS.md → SKILL.md → `docs/architecture/architecture.md`·`docs/adr/README.md`·`docs/architecture/data-model.md`·`docs/test-strategy.md`·`docs/runbooks/testing.md` → README 및 나머지 docs → 기존 코드·테스트 → 최소 가정.
- 읽기 순서: `CLAUDE.md` → `AGENTS.md` → `SKILL.md` → `docs/architecture/*` → `docs/resume.md` → 코드.
- 언어 정책: 모든 Markdown 한국어, 예외는 벤더링된 `.claude/`, `.codex/`, `.agents/skills/` 원문과 행동 원칙 소제목. `design.md`가 영문인 것은 정책상 예외 목록에 없다(사실 — §9).
- IDE 룰 파일(Copilot/Cursor)은 두지 않는다("drift 회피"). WIP는 Next 16 자동 생성도 `agentRules: false`로 끈다.

**docs/ 트리와 규약**

| 경로 | 내용 | 규약 |
|---|---|---|
| `docs/tasks.md` / `tasks-done.md` / `tasks-rule.md` | 백로그 / 완료 아카이브(역시간순) / 7개 규칙 | task ID `T-NNN`(T-021 ~ T-038 확인). 완료 시 같은 커밋에서 이동 |
| `docs/resume.md` | 현재 상태·다음 한 작업 인수인계 | 매 작업 후 갱신 |
| `docs/journal.md` | 날짜별 작업 일지(역시간순) | 검증 실패·미검증 항목 기록 |
| `docs/adr/001~007-*.md`, `README.md` | ADR 7건 + 작성 규약 | `NNN-<slug>.md`, 필드 순서(상태/날짜/결정자/컨텍스트/결정/근거/결과 긍정/부정/후속), superseded 규칙, 다음 번호 ADR-008. `docs/decisions` 없음 |
| `docs/architecture/*.md` (8 + README) | architecture, data-model, analytics, collection, data-sources, performance, backup-restore, dependencies | |
| `docs/runbooks/*.md` (9 + README) | deployment, migration, testing, remote-command-safety, troubleshooting, agent-failure-patterns, branch-protection, cross-repo-audit-checklist, hostile-review | |
| `docs/reports/hallmark-audit-2026-08-22.md` | Hallmark 감사 | `docs/reviews`·`docs/archive` 없음 |
| `docs/current-state.md`, `project-brief.md`, `dev-environment.md`, `test-strategy.md`, `openapi.json` | 상태 요약·브리프·환경·테스트 계층·API 정본 | |

- 문서 링크에 Windows 절대 경로(`</F:/dev/kor-travel-airport/...>`)를 쓰는 곳이 많다(README 21건, ADR README 7건 등). 다른 체크아웃 경로에서는 깨진다(사실).

**개발 환경·프로세스**

- 정본 환경: **WSL2**. 1차 테스트 WSL2 셸, 2차 WSL2+Docker(`docker compose run --rm --no-deps ...`), Windows PowerShell은 배포/상태 확인 보조이며 테스트 합격 기준이 아님(`AGENTS.md` "WSL 테스트 기준", `docs/dev-environment.md` 표).
- worktree 정책: 없음. kor-travel-map의 에이전트별 worktree/sandbox 브랜치·codegraph 게이트는 "단일 서비스 구조에 맞지 않아" 의도적으로 미이식(`docs/tasks-done.md` T-028, `docs/journal.md` 2026-08-23).
- codegraph: 미사용(저장소 내 언급 없음).
- 리뷰 정책: **2인 적대적 리뷰 게이트** — read-only 서브에이전트 2개(James=프론트/live UI, Popper=백엔드/DB/ops)를 독립 실행, P0/P1/P2 분류, 재현 후 수정, journal 기록(`docs/runbooks/hostile-review.md`). `main` 머지 전 필수.
- 브랜치/PR: `codex/<topic>` feature branch → Draft PR → CI green → hostile review → live E2E → squash merge, 브랜치 자동 삭제. branch protection은 문서화만 되고 **미적용**(`docs/runbooks/branch-protection.md` "404 Branch not protected").
- 보안 감사(push 전 스캔): 문서화된 절차 없음(미확인). 금지 규칙으로 "백업 파일·SQLite·.env·API key 커밋 금지", `git add -A` 금지(`SKILL.md` §4).
- `*.local.md` 규약: 없음. `.claude/settings.local.json`만 gitignore.
- 에이전트 정의: `.claude/agents/*.md`(opus, 범용 역할 5종), `.codex/agents/*.toml`(gpt-5.5 xhigh, 6종, sandbox_mode 지정), `.codex/config.toml`(playwright·sequential-thinking MCP).
- 벤더링 skill은 `.agents/skills`와 `.claude/skills`에 **동일 내용 이중 배치**(main: postgres 7종, WIP: +shadcn, migrate-radix-to-base). WIP는 `skills-lock.json`으로 출처·hash를 고정.

## 6. CI·배포·운영

- `.github/workflows/ci.yml`(push: `main`, `codex/**`; pull_request):
  - `backend`: ubuntu, `services.postgres: postgres:16`, `setup-python 3.12`, `astral-sh/setup-uv@v6`, `uv sync --extra dev --locked`, `uv run alembic upgrade head`, `uv run alembic check`, `uv run pytest tests -q`.
  - `frontend`: `setup-node 22`(npm cache), `npm ci`, `npm run test -- --run`, `npx tsc -p tsconfig.test.json --noEmit`, `npm run build`.
  - `live-e2e`: `E2E_BASE_URL=https://<prod-host>`, `EXPECTED_RELEASE_SHA=${{ pr.head.sha || sha }}`, `playwright install chromium`, `npm run test:e2e` — 실제 운영을 호출하므로 서버가 내려가면 PR이 막힌다(`branch-protection.md`).
  - lint job 없음, OpenAPI drift job 없음, pre-commit 없음.
- Docker compose:
  - `docker-compose.yml`(project `kor-travel-airport`): backend(`${PUBLIC_API_PORT:-14001}:8000`, healthcheck `/health`, `./backups` bind), frontend(`${PUBLIC_WEB_PORT:-14002}:3000`, `depends_on backend healthy`), 외부 네트워크 `kor-travel-airport-net`.
  - `docker-compose.db.yml`(project `kor-travel-airport-db`): `postgres:16-alpine`, `${POSTGRES_BIND_HOST:-127.0.0.1}:${POSTGRES_HOST_PORT:-14000}:5432`, **volume name 고정** `parking-radar_parking_radar_postgres_data`(개명 후에도 유지, ADR-007), 네트워크 생성 측.
  - `docker-compose.live.yml`: 단기 검증용(postgres 55432, backend 8010, 15초 수집).
  - `docker-compose.odroid.yml`: `services: {}` fail-closed 마커.
- 배포: `scripts/deploy-server14.sh` — host/app dir/env file/compose project를 정확값으로 강제(`require_exact` 패턴), `git archive` 후보 tarball 업로드, DB 스택은 없을 때만 기동, 배포 후 `/health.release_sha` 대조. WSL 경유 SSH(`docs/resume.md`). `scripts/deploy-odroid.ps1`은 `throw`로 차단.
- 시크릿: n150 `/home/digitie/apps/kor-travel-airport/.env.server14`에만 존재, `.env.*` gitignore(예시 파일만 추적). CI secret 사용 없음(live-e2e는 공개 URL만).
- git 규약: `.gitattributes`로 `*.sh text eol=lf` 강제(CRLF로 shebang 깨지던 재발 방지, ADR-007 §5). 배포 스크립트 실행 비트는 PR #16에서 100755로 고정(`docs/journal.md` 2026-09-06).

## 7. 외부 연동 (cross-repo)

| 대상 | 방식 | 핀 | 근거 |
|---|---|---|---|
| `python-krairport-api`(`krairport`) | 백엔드 라이브러리 소비: `AsyncKrairportClient.kac_raw_items/iiac_raw_items/kac_flight_status_detail_raw_items` | `git+https://github.com/digitie/python-krairport-api@cbe4d1380dc0…`(커밋 고정, uv.lock 동일) | `pyproject.toml`, `services/collection.py` 11행, `services/flight_status.py` 12~13행, ADR-004 |
| `python-kasi-api`(`kasi`) | `AsyncKasiClient.holidays()` | `@51c39c1b0dd5…` 커밋 고정 | `services/holidays.py` 10~11행, ADR-006 |
| 형제 라이브러리 수정 정책 | 부족하면 이 저장소에 wrapper를 만들지 않고 `F:\dev\<repo>` 로컬 체크아웃을 직접 고친다 | — | `AGENTS.md` "Provider 라이브러리 사용 원칙" |
| `kor-travel-map` | 규약 이식: `/v1` 버저닝·RFC7807·`export_openapi.py`, ADR/runbook/문서 구조 | — | ADR-005, `docs/tasks-done.md` T-028 |
| `kor-travel-docker-manager` | 규약 이식: DB를 별도 compose lifecycle로 분리 | — | `docker-compose.db.yml` 주석, T-032 |
| `pinvi` | 계획상 참조: T-035 `AppShell.tsx` 모바일 하단 탭바 패턴 | — | WIP `docs/tasks.md` |
| geo / weather / concierge / docker-manager 서비스 | HTTP 호출 없음 | — | main.py·services grep |
| ServiceToken / 서비스 간 인증 | 없음 | — | ADR-005 "범위 밖" |
| `maplibre-vworld-*`, `vworld-map-*` 벤더 tgz | 사용 없음(지도 없음) | — | package.json |
| 공공데이터 API(data.go.kr) | 유일한 외부 런타임 의존. 키는 서버 env(`DATA_GO_KR_SERVICE_KEY`)에만 | — | README "데이터 소스" |

## 8. 공통화 후보

| # | 영역 | 근거 경로 | 신뢰도 | 비고 |
|---|---|---|---|---|
| 1 | OKLCH 의미 토큰 계층(색/그림자/radius/폰트 스택/간격 8단계, 다크는 `prefers-color-scheme`) | `frontend/src/app/tokens.css` | high | 값이 아니라 **토큰 이름·역할 규약**을 공통화. 브랜드 값(airport-orange)은 앱 소유 |
| 2 | 토큰 → shadcn 시맨틱 변수 브릿지(`:root` 배선 + `@theme inline` + `.dark` 미사용) | WIP `frontend/src/app/globals.css` 36~59행, 1876~1932행 | high | common의 "shadcn 변수 매핑 레시피" 참조 구현. `--muted`/`--accent`/`--radius` 충돌 회피 조건 포함 |
| 3 | focus-visible 레시피(`outline 2px accent + offset 2px + --shadow-focus`) | `globals.css` 199~203행 | high | UX 가이드 항목 |
| 4 | reduced-motion 전역 규칙 | `globals.css` 1836~1843행 | high | UX 가이드 항목 |
| 5 | 가로 오버플로 규칙(루트 `overflow-x: clip`, 스크롤 영역만 `auto`, `hidden` 금지) | `SKILL.md` §4 #6, `design.md`, `globals.css` 36·42행 | high | PC/Mobile Web 규칙 |
| 6 | 검증 브레이크포인트 세트 320/375/414/768/1440 + JS 모바일 임계 860px | `design.md`, `SKILL.md` §5, `dashboard-app.tsx` 106행, `globals.css` 1306행 | medium | 값 통일 여부는 다른 저장소 조사 결과와 대조 필요 |
| 7 | Next same-origin 백엔드 프록시 route handler(allowlist, 헤더 필터, 타임아웃, 본문 읽기 타임아웃, no-store, 502/504 envelope) | `frontend/src/app/api/backend/[...path]/route.ts`, `tests/backend-proxy-route.test.ts` | high | 다른 앱의 proxy와 비교 후 `createBackendProxy(allowlist, timeouts)`로 추출 가능(후보) |
| 8 | 보안 헤더 집합(nosniff/DENY/Referrer/Permissions/HSTS)이 Next와 FastAPI에 중복 | `frontend/next.config.ts` 3~9행, `backend/app/main.py` 208~216행 | high | 공통 상수/미들웨어 후보 |
| 9 | `ApiError` + `getJson` fetch 래퍼(RFC7807 `detail` 읽기, no-store, multipart 분기) | `frontend/src/lib/api.ts` 25~90행 | medium | react-query 미사용 앱에서도 쓸 수 있는 최소 래퍼 |
| 10 | RFC7807 problem+json 핸들러 2종(HTTPException + RequestValidationError) | `backend/app/main.py` 160~196행, ADR-005 | high | 공통 FastAPI 헬퍼 `install_problem_handlers(app)` 후보 |
| 11 | `/v1` prefix + `/health` 비버저닝 + 무-호환 clean cut 규약 | ADR-005, `main.py` 238·1012행, `route.ts` 41~45행 | high | OpenAPI 규칙 문서 항목 |
| 12 | OpenAPI export 스크립트 + 커밋된 `docs/openapi.json` + (부재한) CI drift 검사 | `scripts/export_openapi.py`, `docs/openapi.json`, ADR-005 후속 | high | common이 `--check` 게이트를 표준화하면 이 저장소의 미해결 후속을 해결 |
| 13 | pydantic-settings CSV→list property 패턴(`cors_origins_csv`, `trusted_hosts_csv`, `airport_codes_csv`) | `backend/app/core/config.py` 50~60행 | medium | env prefix 부재는 common 정책과 조정 필요 |
| 14 | 기본 미들웨어 묶음(TrustedHost + CORS(credentials false) + 보안 헤더) | `main.py` 198~216행 | medium | `install_baseline_middleware(app, settings)` 후보 |
| 15 | KST/UTC 시간 헬퍼(py `time_utils`: `now_utc`, `to_seoul`, `align_to_interval`, `split_by_local_day`; ts `format.ts`: `Intl` 기반 `getSeoulDateParts`, `formatDateTimeWithZone`) | `backend/app/core/time_utils.py`, `frontend/src/lib/format.ts` | medium | 선행 보고서 §7.2 "의미가 일치하는 것만" 조건 적용. 저장 UTC·표시 Asia/Seoul 규칙(`CLAUDE.md` §2)은 규칙으로 공통화 가능 |
| 16 | Alembic head 상수 기동 검증 + CI `alembic upgrade head && alembic check` | `backend/app/db/session.py` 15·102~110행, `ci.yml` | high | 백엔드 규칙 항목 |
| 17 | DB 분리 compose(고정 volume name, 외부 네트워크, loopback 포트) | `docker-compose.db.yml`, `docs/runbooks/deployment.md` "PostgreSQL 별도 컨테이너" | medium | docker-manager 원본 규약과 함께 common compose 템플릿 후보 |
| 18 | 배포 스크립트 가드(정확값 강제) + `/health.release_sha` 배포 대조 + live E2E `EXPECTED_RELEASE_SHA` | `scripts/deploy-server14.sh` 9~31행, `frontend/e2e/live-dashboard.spec.ts` 18~22행, `ci.yml` live-e2e | medium | 운영 규칙 항목 |
| 19 | 문서 규약 세트(CLAUDE 1쪽 + AGENTS 정책 + SKILL 매뉴얼, 우선순위, tasks/tasks-done/tasks-rule/resume/journal, ADR 템플릿·번호 규칙, runbooks/agent-failure-patterns) | `AGENTS.md`, `docs/tasks-rule.md`, `docs/adr/README.md`, `docs/runbooks/README.md` | high | kor-travel-map에서 이미 한 번 이식된 규약이므로 두 저장소 대조로 정본화 가능 |
| 20 | 적대적 리뷰 게이트(James/Popper 2 서브에이전트, P0/P1/P2, 재현 후 수정) | `docs/runbooks/hostile-review.md` | high | 프로세스 규칙 |
| 21 | 벤더링 skill 정책(`.agents/skills` + `.claude/skills` 이중 사본, `skills-lock.json`, 원문 영어 유지) | `.claude/agents/README.md`, WIP `skills-lock.json` | medium | 이중 사본 유지가 규칙인지 도구 제약인지 미확인 |
| 22 | Hallmark 기록 형식(`.hallmark/preflight.json`·`log.json`, `design.md`, `docs/reports/hallmark-audit-*.md`, 금지 게이트 6개) | `.hallmark/*`, `design.md` "Hallmark gate" | medium | UX 가이드/디자인 감사 규칙 후보 |
| 23 | Vitest 구성(jsdom + `globals` + jest-dom + in-memory localStorage shim) + `tsconfig.test.json` 분리 + CI `tsc --noEmit` | `frontend/vitest.config.ts`, `vitest.setup.ts`, `tsconfig.test.json`, `ci.yml` | medium | 도구 규칙 |
| 24 | `.gitattributes *.sh eol=lf`, 실행 비트 100755 유지 | `.gitattributes`, `docs/journal.md` 2026-09-06 | high | 저장소 위생 규칙 |
| 25 | `agentRules: false`(Next 16 자동 AGENTS/CLAUDE 억제) | WIP `frontend/next.config.ts` | medium | common의 Next 설정 규칙 후보 |
| 26 | 형제 python 라이브러리 핀 방식(PEP 508 `git+...@<full sha>`, 로컬 체크아웃 우선 수정) | `pyproject.toml`, `AGENTS.md` provider 원칙 | high | 버전 일치화 정책 항목. uv sources 미사용 이유(Docker pip)도 정책에 반영 필요 |
| 27 | WSL2 정본·PowerShell 보조·1차/2차/배포/live 스모크 4단 검증 | `AGENTS.md` "WSL 테스트 기준", `docs/dev-environment.md` | medium | 다른 저장소 환경 정책과 대조 필요 |

## 9. 이 저장소 고유 차이·주의점

| 영역 | 내용 | 공통화 시 영향 |
|---|---|---|
| Tailwind 부재(main) | main은 Tailwind/PostCSS 자체가 없고 순수 CSS 1,844행. 사용자 전제(1) "v4가 아닌 앱은 v4로 전환"의 대상이며, WIP가 이미 v4.3.3 CSS-first로 전환 중 | common의 Tailwind 소스 배포는 main에서 무의미하고 WIP 머지 이후에만 소비 가능. 선행 보고서 §7.3 "사전 빌드 CSS + CSS 변수 우선"이 이 저장소에는 여전히 유효 |
| "Admin"의 실체 | 별도 admin 앱·라우트·로그인이 없다. 운영 UI = 대시보드 안의 무인증 백업 패널 + `/v1/admin/*` | 전제(3)의 "kor-travel-airport Admin"은 admin-shell/login-form 소비처가 아니라 백업 패널·collector-status 패널 정도. T-035 라우트 분리 후에야 AppShell 소비 가능 |
| 토큰 별칭 충돌 | `--muted`/`--accent`/`--radius`가 shadcn 의미와 충돌해 WIP에서 재명명 | common 토큰 네이밍은 shadcn 예약 이름과 앱 별칭을 분리하는 규칙이 필요 |
| 다크 모드 방식 | `prefers-color-scheme` 전용, 클래스 토글·`next-themes` 없음 | common이 `.dark`/`@custom-variant dark`를 요구하면 추가 작업 |
| 폰트 | Pretendard 선언만 있고 로딩 없음 | common 폰트 규칙(next/font 또는 self-host) 결정 시 이 앱은 실제 렌더가 바뀜 |
| 런타임 세대 | Next 16.3.2 / React 19.2.8 / **TypeScript 7.0.2** / Node 22 | TS 7과 common 툴체인(ESLint 플러그인 등) 호환 검증 필요. React 19라 map/concierge/pinvi와 같은 세대 |
| 품질 도구 부재 | ESLint·Prettier·ruff·mypy·coverage gate 전무. CI는 tsc/vitest/pytest/alembic check만 | common이 lint 규칙을 배포하면 이 저장소는 0에서 도입. 선행 보고서 §7.2 "공통 lint 설정 금지"와 사용자 전제(2) "버전/도구 일치화"가 충돌하므로 결정 필요 |
| shadcn 의존성 위치 | WIP는 `shadcn`, `postcss`, `@tailwindcss/postcss`를 `dependencies`에, `cn` 패키지를 사용 | common 버전 일치화 정책(devDependencies, clsx+tailwind-merge 등)과 대조 필요 |
| 패키지 매니저 | npm(`package-lock.json`), `engines`/`packageManager` 미선언 | 일치화 정책에서 선언 추가 필요 |
| 백엔드 구조 | 라우트 전부 `main.py` 1,150행 단일 파일, 서비스는 `app.state`에 부착, `api_prefix` 설정 미사용 | common 라우터/의존성 규약을 적용하려면 분리 리팩터링 선행 |
| 빌드 도구 혼용 | uv.lock(CI) vs pip -e(Docker) vs setuptools | common의 python 빌드 정책(uv 단일화 등) 적용 시 Dockerfile 변경 필요 |
| 인증 없음 | ADR-003으로 무인증이 "의도된 설계". CORS `allow_credentials=False` | common 인증 부품은 이 앱의 소비 대상이 아님. 선행 보고서 §3.6 결론과 정합 |
| 성공 응답 envelope 없음 | `{data, meta}`·pagination을 명시적으로 미룸(ADR-005) | common OpenAPI 규칙이 envelope를 요구하면 23개 라우트·types.ts·api.ts 전면 변경 |
| OpenAPI 메타 | tags 없음, operationId 자동, `info.version` 하드코딩 | common의 태그/operationId 규약 적용 시 프론트 생성기 도입과 함께 재작업 |
| 문서 링크 | Windows 절대 경로 링크 다수 | common 문서 템플릿은 상대 경로 규칙 필요 |
| design.md 영문 | 언어 정책 예외에 없음 | common 언어 정책에서 design 문서 언어를 명시해야 함 |
| 문서 내부 불일치 | `AGENTS.md` "최근 7일 30분 간격" vs README/`docs/current-state.md` "10분 단위"; `docs/tasks.md` 완료 조건의 포트 `14000/14001`(T-032 이전 값) vs README `14001/14002` | 정본화 시 정정 대상(이 조사에서 수정하지 않음) |
| Hallmark 규칙 위반 잔존 | raw `rgba`/hex 22건 | common 토큰 규칙 적용 시 정리 대상 |
| 운영 결합 CI | live-e2e job이 실제 n150을 호출 | common CI 템플릿에 "운영 호출 job은 required 여부 별도 결정" 항목 필요 |
| 형제 라이브러리 핀 | 커밋 SHA 고정, 태그/버전 없음(양쪽 `0.1.0`) | 버전 일치화 정책이 태그 기반이면 python-*-api 릴리스 태깅 선행 |

## 10. 버전 표

"선언"은 `package.json`/`pyproject.toml` 범위, "설치"는 `package-lock.json`/`uv.lock`. WIP 열은 `F:/dev/kor-travel-airport` @ `99b3f98`.

| 항목 | 선언(main) | 설치(main) | 선언(WIP) | 설치(WIP) |
|---|---|---|---|---|
| node | engines 없음(Dockerfile/CI 22) | — | 동일 | — |
| npm | 미선언(lockfileVersion 3) | — | 동일 | — |
| next | `^16.3.2` | 16.3.2 | `^16.3.2` | 16.3.2 |
| react / react-dom | `^19.2.8` | 19.2.8 | `^19.2.8` | 19.2.8 |
| typescript | `^7.0.2` | 7.0.2 | `^7.0.2` | 7.0.2 |
| tailwindcss | 없음 | 없음 | `^4.3.3` | 4.3.3 |
| @tailwindcss/postcss | 없음 | 없음 | `^4.3.3` | 4.3.3 |
| postcss | 없음(next 내부) | 8.5.23 | `^8.5.28` | 8.5.28 |
| @base-ui/react | 없음 | 없음 | `^1.8.0` | 1.8.0 (`@base-ui/utils` 0.4.0) |
| radix-ui | 없음 | 없음 | 없음 | 없음 |
| shadcn | 없음 | 없음 | `^4.21.0`(dependencies) | 4.21.0 |
| lucide-react | 없음 | 없음 | `^1.41.0` | 1.41.0 |
| tw-animate-css | 없음 | 없음 | `^1.4.0` | 1.4.0 |
| class-variance-authority | 없음 | 없음 | `^0.7.1` | 0.7.1 |
| cn / clsx / tailwind-merge | 없음 | 없음 | `cn ^0.2.5` | cn 0.2.5, clsx 2.1.1(추이), tailwind-merge 없음 |
| eslint | 없음 | 없음 | 없음 | 없음 |
| vitest | `^4.1.11` | 4.1.11 | 동일 | 4.1.11 |
| @playwright/test | `^1.62.1` | 1.62.1 | 동일 | 1.62.1 |
| jsdom / @testing-library/react | `^30.0.1` / `^16.3.2` | 30.0.1 / 16.3.2 | 동일 | 동일 |
| @tanstack/react-query | 없음 | 없음 | 없음 | 없음 |
| zod / zustand / react-hook-form | 없음 | 없음 | 없음 | 없음 |
| maplibre-gl | 없음 | 없음 | 없음 | 없음 |
| python | `>=3.12`(Dockerfile/CI 3.12) | — | 동일 | — |
| fastapi | `>=0.141,<1.0` | 0.141.1 (starlette 1.6.0) | 동일 | 동일 |
| pydantic | 직접 선언 없음 | 2.13.4 | 동일 | 동일 |
| pydantic-settings | `>=2.15,<3.0` | 2.15.0 | 동일 | 동일 |
| sqlalchemy | `>=2.0.52,<3.0` | 2.0.52 | 동일 | 동일 |
| alembic | `>=1.19,<2.0` | 1.19.1 | 동일 | 동일 |
| asyncpg | `>=0.31,<1.0` | 0.31.0 | 동일 | 동일 |
| psycopg | 없음 | 없음 | 없음 | 없음 |
| httpx | `>=0.28,<1.0` | 0.28.1 | 동일 | 동일 |
| uvicorn | `[standard]>=0.52,<1.0` | 0.52.4 | 동일 | 동일 |
| ruff / mypy | 없음 | 없음 | 없음 | 없음 |
| pytest / pytest-asyncio / pytest-cov | `>=9.1` / `>=1.4` / `>=7.1` | 9.1.1 / 1.4.0 / 7.1.0 | 동일 | 동일 |
| dagster | 없음 | 없음 | 없음 | 없음 |
| python-krairport-api / python-kasi-api | git `@cbe4d13…` / `@51c39c1…` | 0.1.0 / 0.1.0 | 동일 | 동일 |

WIP 브랜치는 `backend/`를 건드리지 않았다(`git diff --name-status main..HEAD`에 backend 파일 없음).

## 11. 미확인·열린 질문

1. WIP 브랜치 `codex/shadcn-ui-foundation`의 Draft PR 개설 여부와 CI 결과 — gh 미사용으로 미확인. 커밋 메시지의 "픽셀 동일·build/vitest 통과"도 재현하지 않았다.
2. `cn` 패키지 사용과 `shadcn`/`postcss`의 `dependencies` 배치가 shadcn 4.21 `base-nova` CLI 기본값인지, 수동 선택인지 — 미확인.
3. Pretendard 폰트가 어디서도 로드되지 않는데 Hallmark 시각 검증이 어떤 폰트로 이뤄졌는지 — 미확인.
4. `docs/openapi.json`이 현재 코드의 스키마와 동일한지 — 경로 집합(22)은 일치하나 재생성 비교는 하지 않았다(조사 대상 수정 금지).
5. `Settings.api_prefix`가 선언만 있고 라우터에 적용되지 않는 것이 의도인지 잔재인지 — 미확인.
6. TypeScript 7.0.2가 common의 ESLint/typescript-eslint 도입과 호환되는지 — 미확인.
7. `.agents/skills`와 `.claude/skills` 이중 사본이 규칙(도구별 탐색 경로)인지 단순 복제인지 — README는 "보관"만 언급, 미확인.
8. branch protection 실제 적용 시점 — 문서상 미적용(2026-08-23 확인), 이후 변화 미확인.
9. 사용자 전제(3) "kor-travel-airport Admin"이 현재의 백업 패널/`/v1/admin/*`를 뜻하는지, T-035 이후 `/backup` 등 분리 라우트를 뜻하는지 — 확인 필요.
10. n150 운영 `docker compose ps` 등 실사는 `docs/resume.md` 기록에 의존했고 직접 확인하지 않았다.
11. `AGENTS.md`의 "30분 간격"과 README의 "10분 단위" 중 어느 쪽이 정본인지 — 코드 기본값은 `intervalMinutes = 10`(`api.ts` 186행)이므로 README 쪽이 코드와 일치(사실), AGENTS.md 문구는 오기로 추정.

## 12. 근거 파일 목록

`F:/dev/kor-travel-common-survey/kta-main` 기준(별도 표기 없으면 main @ 2bb1111):

1. `LICENSE`
2. `README.md`
3. `AGENTS.md`
4. `CLAUDE.md`
5. `SKILL.md`
6. `design.md`
7. `.gitattributes`, `.gitignore`, `.dockerignore`
8. `.env.example`, `.env.server14.example`
9. `.github/workflows/ci.yml`
10. `docker-compose.yml`, `docker-compose.db.yml`, `docker-compose.live.yml`, `docker-compose.odroid.yml`
11. `.hallmark/preflight.json`, `.hallmark/log.json`
12. `.claude/agents/README.md`, `.claude/agents/*.md`(헤더), `.codex/agents/*.toml`(헤더), `.codex/config.toml`, `.agents/skills/postgres/SKILL.md`(헤더)
13. `frontend/package.json`, `frontend/package-lock.json`(버전 추출)
14. `frontend/tsconfig.json`, `frontend/tsconfig.test.json`
15. `frontend/next.config.ts`, `frontend/vitest.config.ts`, `frontend/vitest.setup.ts`, `frontend/playwright.config.ts`, `frontend/Dockerfile`
16. `frontend/src/app/tokens.css`, `frontend/src/app/globals.css`(1~60, 190~215, 1300~1340, 1545~1600, 1820~1844행 및 grep)
17. `frontend/src/app/layout.tsx`, `frontend/src/app/page.tsx`, `frontend/src/app/api/backend/[...path]/route.ts`
18. `frontend/src/lib/api.ts`, `frontend/src/lib/dashboard-preferences.ts`, `frontend/src/lib/format.ts`, `frontend/src/lib/types.ts`(헤더)
19. `frontend/src/components/dashboard-app.tsx`(헤더, 98~118행, grep), `dashboard-screen.tsx`(헤더, grep), `history-chart.tsx`, `daily-flight-overlay-chart.tsx`, `backup-panel.tsx`, `fee-calculator.tsx`(헤더)
20. `frontend/e2e/live-dashboard.spec.ts`(1~50행), `frontend/tests/backend-proxy-route.test.ts`(1~30행), `frontend/tests/*` 목록
21. `backend/pyproject.toml`, `backend/uv.lock`(버전 추출), `backend/alembic.ini`, `backend/alembic/env.py`, `backend/alembic/versions/0001_initial.py`(헤더), `backend/entrypoint.sh`, `backend/Dockerfile`
22. `backend/app/main.py`(109~260행, 692~1012행 grep), `backend/app/core/config.py`, `backend/app/core/time_utils.py`, `backend/app/db/session.py`, `backend/app/schemas.py`(1~80행, 클래스 목록), `backend/app/models.py`(1~32행, 클래스 목록)
23. `backend/app/services/collection.py`, `flight_status.py`, `holidays.py`, `backup_restore.py`(헤더·grep)
24. `backend/tests/conftest.py`, `backend/tests/` 목록, `backend/tests/fixtures/` 목록
25. `scripts/export_openapi.py`, `scripts/deploy-server14.sh`(1~40행), `scripts/n150-backup-cron.sh`, `scripts/deploy-odroid.ps1`(헤더), `deploy/odroid/README.md`(헤더)
26. `docs/openapi.json`(메타·경로·스키마 목록)
27. `docs/tasks.md`, `docs/tasks-done.md`(T-028, T-032, 헤더), `docs/tasks-rule.md`, `docs/resume.md`(1~60행), `docs/journal.md`(1~40행, 190~223행)
28. `docs/adr/README.md`, `docs/adr/003-*.md`, `docs/adr/004-*.md`(1~40행), `docs/adr/005-*.md`, `docs/adr/007-*.md`
29. `docs/architecture/README.md`, `architecture.md`, `dependencies.md`, `data-model.md`(1~40행), `backup-restore.md`(1~25행), `performance.md`
30. `docs/runbooks/README.md`, `hostile-review.md`, `agent-failure-patterns.md`, `branch-protection.md`, `cross-repo-audit-checklist.md`(1~30행), `remote-command-safety.md`(1~40행), `deployment.md`(1~80행), `testing.md`(헤딩, 78~152행)
31. `docs/test-strategy.md`, `docs/dev-environment.md`, `docs/project-brief.md`, `docs/current-state.md`(헤딩, 225~290행), `docs/reports/hallmark-audit-2026-08-22.md`

`F:/dev/kor-travel-airport` @ `99b3f98`(WIP, 읽기 전용):

32. `git status --short`, `git stash list`, `git log main..HEAD`, `git show --stat HEAD`, `git diff --name-status main..HEAD`
33. `frontend/components.json`, `frontend/postcss.config.mjs`, `frontend/src/lib/utils.ts`, `frontend/src/components/ui/button.tsx`, `skills-lock.json`
34. `frontend/package.json`(diff), `frontend/package-lock.json`(버전 추출), `frontend/next.config.ts`(diff), `.gitignore`(diff), `docs/tasks.md`(diff)
35. `frontend/src/app/globals.css`(diff 전체, `@theme`/`@layer` grep), `frontend/src/app/tokens.css`(diff 없음 확인)
36. `.agents/skills/shadcn/SKILL.md`(1~40행), `.agents/skills/shadcn/agents/openai.yml`, `.agents/skills/migrate-radix-to-base/SKILL.md`(1~30행)

선행 보고서:

37. `F:/dev/kor-travel-geo-fixes/docs/kor-travel-common-library-review.md`(전체 헤딩, §1~§3, §7~§9; airport 언급 0건 확인)
