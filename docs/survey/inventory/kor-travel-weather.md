# kor-travel-weather 인벤토리

- 기준 커밋: `6003da995fa4b35799f9dadc406c6ba2878bfbae` (`main`, 2026-09-05 "fix(admin): match kor-travel-geo session login boundary")
- 조사일: 2026-09-06
- 조사 경로: `F:/dev/kor-travel-weather` (원격 `https://github.com/digitie/kor-travel-weather.git`)
- 라이선스: GPL v3. `LICENSE` 1~2행 "GNU GENERAL PUBLIC LICENSE / Version 3, 29 June 2007"; `pyproject.toml` `license = { text = "GPL-3.0-or-later" }`; README "라이선스" 절 "GPL-3.0-or-later"
- 표기 규칙: 본문에서 **사실**은 근거 경로를 붙여 서술하고, **후보/추정/미확인**은 그 단어를 명시한다. 파일 경로는 저장소 상대 경로다.

## 1. 저장소 개요와 역할

- 제품 정체성: 대한민국 전역의 관측·예보·기상특보·대기질을 모아 제공하는 **독립 날씨 데이터 소스**다. 장소/축제/가격 같은 지도 도메인은 소유하지 않는다 (`README.md` 1~6행, `AGENTS.md` "범위" 절).
- 사용자: 직접 사용자는 운영자(admin UI)뿐이고, 최종 소비자는 형제 프로젝트 PinVi와 `kor-travel-map`이다. 두 소비자는 DB를 읽지 않고 REST/OpenAPI(`/v1/weather/resolve`, `/v1/weather/nearby`)만 사용한다 (`docs/integration-map.md` 표, `docs/architecture/rest-api.md` "Consumer adapter boundary").
- 실행 표면 4개: `src/kortravelweather` 공용 도메인/설정/repository, `packages/kor-travel-weather-api` FastAPI, `packages/kor-travel-weather-dagster` Dagster 자산/스케줄, `packages/kor-travel-weather-admin/frontend` Next.js 운영 UI (`README.md` "저장소 구조", `docs/architecture/architecture.md` "Package boundaries").
- provider: `python-kma-api`(git 핀), `python-airkorea-api`(저장소 내 snapshot 0.4.0), 그리고 9개 외부 provider(Open-Meteo, wttr.in, WeatherAPI, OpenWeatherMap, Visual Crossing, Tomorrow.io, Weatherbit, Weatherstack, AccuWeather) (`README.md` "목표", `src/kortravelweather/settings.py` `SUPPORTED_PROVIDER_KEYS`).
- 이식 기원: `kor-travel-map` 2026-08-30 `main` 커밋 `41aaa86c…`을 기반으로 weather DTO·KMA raw payload 보존·admin weather panel UX를 이식했다 (`README.md` "원본 이식 기록"). ADR 번호(020/048/062/072/074/089)도 map의 번호 체계를 그대로 유지한다 (`docs/adr/README.md`).
- 운영 UI는 "`kor-travel-map` admin과 같은 좌측 rail·카드형 page header·4pt spacing과 navy design token"을 사용한다고 명시한다 (`README.md` "운영 모델" 하단, `packages/kor-travel-weather-admin/frontend/design.md`).
- 인증 경계는 최근 두 커밋(`9d1a325`, `6003da9`)에서 `kor-travel-geo`의 signed-session 계약에 맞췄고 Basic Auth를 Dagster gateway로 격리했다 (`git show 6003da9`, §3.1 인증 경계 참조).
- 개발 규칙(`AGENTS.md`): `main` 직접 push 금지, KMA 격자/발표 시각 재구현 금지, timezone-aware KST 입력, unique key + upsert, admin write fail-closed, "API DTO 변경 시 OpenAPI export와 TypeScript client 타입을 같이 갱신", 문서·주석 한국어 기본.

## 2. 저장소 구조

최상위 트리(추적 파일 기준, `git ls-files`):

```text
.github/workflows/ci.yml        단일 CI 워크플로
AGENTS.md                       작업 규칙 (39행)
README.md                       개요·빠른 시작·구조 (167행)
LICENSE                         GPL v3
pyproject.toml / uv.lock        루트 Python 프로젝트 (setuptools, uv lock)
alembic.ini / alembic/          마이그레이션 (versions 0001~0008)
compose.yaml                    로컬/운영 Compose (db/api/dagster/dagster-gateway/migrate/prometheus/web)
conftest.py                     루트 pytest PostgreSQL 격리 fixture
deploy/                         Dockerfile 3종, n150 override, nginx gateway, prometheus
docs/                           architecture/adr/etl/migrations/runbooks + 단일 문서 6종
packages/kor-travel-weather-api/        FastAPI 패키지 + openapi.json
packages/kor-travel-weather-dagster/    Dagster 패키지
packages/kor-travel-weather-admin/frontend/   Next.js admin (npm 단일 프로젝트)
packages/python-airkorea-api/   python-airkorea-api 0.4.0 snapshot (50개 파일)
src/kortravelweather/           공용 도메인·설정·repository·providers
tests/                          루트 단위/통합 테스트
```

| 패키지/앱 | 경로 | 종류 | 비고 |
| --- | --- | --- | --- |
| kor-travel-weather (core) | `src/kortravelweather` | Python (setuptools, uv) | import명 `kortravelweather`, CLI `ktwctl` |
| kor-travel-weather-api | `packages/kor-travel-weather-api` | Python FastAPI | `[tool.uv.sources] kor-travel-weather = { path = "../..", editable = true }` |
| kor-travel-weather-dagster | `packages/kor-travel-weather-dagster` | Python Dagster | 동일한 path 의존 |
| kor-travel-weather-admin-frontend | `packages/kor-travel-weather-admin/frontend` | Next.js 15 / React 19 | `package.json` `name: kor-travel-weather-admin-frontend`, private |
| python-airkorea-api | `packages/python-airkorea-api` | Python 라이브러리 snapshot | 루트 `[tool.uv.sources] python-airkorea-api = { path = ... }` |

- 모노레포 형태: npm workspaces 아님(루트 `package.json` 없음). Python은 루트 `pyproject.toml` 하나가 `pytest.ini_options.testpaths/pythonpath`로 하위 패키지를 묶는 "단일 uv 프로젝트 + path 의존" 구조다. 사실.
- 루트에 `.venv`, `.mypy_cache`, `pytestdebug.log`, `.tmp_dagster_home_*`가 있으나 추적 대상 아님(`.gitignore`).

## 3. 프론트엔드

### 3.1 kor-travel-weather-admin-frontend (`packages/kor-travel-weather-admin/frontend`)

**프레임워크/런타임** (`package.json`, `package-lock.json` lockfileVersion 3)

| 항목 | 선언 | lockfile 설치 |
| --- | --- | --- |
| next | `^15.2.0` | 15.5.24 |
| react / react-dom | `^19.0.0` | 19.2.8 |
| typescript | `^5.7.3` | 5.9.3 |
| node engines / packageManager | 없음 (`package.json`에 `engines`/`packageManager` 키 없음) | CI `node-version: 20` (`.github/workflows/ci.yml`), Docker `node:22-alpine` (`deploy/Dockerfile.web`) |
| 패키지 매니저 | npm (`npm ci`), `.nvmrc`/`.node-version` 없음 | — |

CI(Node 20)와 Docker(Node 22)의 Node 메이저가 다르다. 사실.

**스타일**

- tailwindcss: **없음**. `package.json` 의존성에 tailwindcss/@tailwindcss/postcss 없음, `package-lock.json`에도 없음. `postcss` 8.4.31은 next의 전이 의존성으로만 존재. `postcss.config.*`, `tailwind.config.*`, `components.json` 모두 부재(존재 여부 `ls`로 확인).
- 스타일 구성: `app/globals.css`(2,334행) + `app/tokens.css`(161행) = **2,495행의 손수 작성 CSS**. `globals.css` 10행 `@import "./tokens.css";` 외 다른 `@import` 없음. `app/layout.tsx`에서 `import "./globals.css"`로 전역 로드.
- `globals.css` 헤더(1~9행): "kor-travel-map admin visual source … Rail-Workbench recipe … Hallmark · pre-emit critique: P5 H5 E4 S5 R5 V5 · contrast: pass · nav: N3 · footer: Ft2 · responsive: pass". Hallmark 스킬 산출물임을 스스로 표기.
- `globals.css` 절 구성(주석 구분선 기준, 행 범위와 규칙 블록 수는 조사 스크립트 집계):

| 행 범위 | 행 수 | 규칙 블록 | 절 이름(주석 원문 요약) | 성격 |
| ---: | ---: | ---: | --- | --- |
| 1–243 | 243 | 32 | 헤더 + base reset(`*`, `html`, `body`, `h1~h3`, `a`, `button`, `code`, `table`…) | 전역 element 스타일 |
| 244–413 | 170 | 21 | "Shared map shell: flat 17rem rail + card header" | 공유 shell |
| 414–505 | 92 | 11 | PageHeader | 공유 shell |
| 506–536 | 31 | 2 | Content margins ("match map's main px-6 py-6") | 공유 shell |
| 537–744 | 208 | 30 | "Shared data surfaces: map's hairline panels, controls and tables" | 공유 primitives |
| 745–914 | 170 | 24 | Dashboard and data cards | 공유 primitives |
| 915–1376 | 462 | 63 | Weather map workbench | 도메인 |
| 1377–1648 | 272 | 39 | Catalog / provider settings forms | 공유 form + 도메인 |
| 1649–1788 | 140 | 19 | Dagster operations | 도메인 |
| 1789–1889 | 101 | 15 | "Login: the same standalone shell, card and form rhythm as kor-travel-geo" | 공유 login |
| 1890–1909 | 20 | 5 | `@keyframes spin` + `prefers-reduced-motion` | 공유 모션 |
| 1910–2142 | 233 | 42 | "Responsive map breakpoints copied from kor-travel-map's rail behavior" (`max-width: 62rem`, `42rem`) | 반응형 |
| 2143–2202 | 60 | 12 | Weather-aware map markers | 도메인 |
| 2203–2251 | 49 | 8 | "WeatherMarker primitive from digitie/maplibre-vworld-react" 호환 | 도메인(벤더 호환) |
| 2252–2335 | 84 | 12 | Native MapLibre weather clusters | 도메인 |

- 클래스 명명: BEM 아님. 단일 소문자 kebab-case 클래스 + 상태 modifier 클래스(`.active`, `.selected`, `.on`/`.off`/`.warn`, `.primary`/`.secondary`/`.ghost`/`.danger`, `.loading`, `.error`, `.empty`)를 조합한다. CSS에 등장하는 **고유 클래스 선택자 170개**, TSX에서 실제 사용하는 고유 클래스 토큰 142개, 최상위 규칙 블록 약 277개, `var(--…)` 참조 294회, 하드코딩 색상 23곳(모두 2143행 이후 marker/cluster 절: `#d98b20`, `#526b90`, `#2563a8`, `#b13b4a`, `#183b66` 등). 사실(grep 집계).
- bare element 선택자 23종(`a`, `body`, `button`(+`:hover/:active/:disabled`), `code`, `h1~h3`, `html`, `pre`, `small`, `table/thead/tbody/td/th`, `textarea`…). 전역 `button`/`table` 재정의가 존재하므로 공통 CSS를 주입할 때 충돌 대상이 된다. 사실.
- 토큰 파일 `app/tokens.css`(161행, 헤더 주석 "Shared token source: kor-travel-map admin design system"): 형식은 `:root { --… }` + `.dark { --… }`. 요약:
  - 색: oklch 팔레트 `--surface-page/subtle/muted`, `--card`, `--text-primary/secondary/tertiary/disabled`, `--icon-default`, `--control-line`, `--brand`(navy `oklch(47% 0.14 255)`), `--brand-hover/tint/foreground`, `--success/-tint`, `--warning/-tint`, `--info/-tint`, `--destructive/-tint`, `--focus`.
  - shadcn 호환 별칭: `--background`, `--foreground`, `--popover(-foreground)`, `--primary(-foreground)`, `--secondary(-foreground)`, `--muted(-foreground)`, `--accent(-foreground)`, `--border`, `--input`, `--ring`, `--radius`, `--radius-sm/md/lg/xl/2xl`. 사실. 이 이름은 shadcn/ui v4 `@theme inline` 매핑 이름과 일치한다(후보: 전환 시 1:1 대응 가능).
  - 간격: `--space-3xs…2xl`(0.125rem~4rem, "four-point rhythm"). radius: `--radius-control 0.375rem`, `--radius-panel 0.5rem`. 컨트롤 높이 `--control-h 2.25rem`, `--control-h-sm 1.875rem`. rail 폭 `--rail 17rem`.
  - 폰트: `--font-sans`(`var(--font-geist)`, `var(--font-pretendard)`, Pretendard, "Noto Sans KR", …), `--font-mono`(`var(--font-geist-mono)`, ui-monospace…). `--font-display/body/heading`은 `--font-sans` 별칭.
  - 모션: `--ease-out`, `--ease-in`, `--duration-fast 100ms`, `--duration-base 150ms`, `--dur-fast`. 그림자 `--shadow-card(none)`, `--shadow-elevated`, `--shadow-modal`. z-index 토큰 **없음**.
  - 레거시 별칭 `--color-ink/paper/panel/rule/accent/danger/warning/info…` 15종(라이트/다크 양쪽 정의).
- 라이트/다크: `.dark` 블록이 tokens.css에 정의돼 있으나, TSX/JS에서 `dark` 클래스·`data-theme`·`prefers-color-scheme`를 다루는 코드는 grep 결과 없음. 사실: 다크 팔레트는 존재하지만 런타임 토글 없음(사실상 라이트 전용).
- 폰트 로딩: `app/layout.tsx`와 컴포넌트에 `next/font` import 없음(grep). 따라서 `--font-geist`/`--font-pretendard` CSS 변수는 어디서도 정의되지 않고 로컬 설치 "Geist"/"Pretendard Variable"/"Noto Sans KR"/system-ui fallback으로 렌더된다. 추정(브라우저 렌더 미확인).
- 아이콘: `lucide-react` `^0.468.0`(설치 0.468.0). 7개 파일에서 사용.
- 애니메이션: `tw-animate-css` 없음. `@keyframes spin` 1개.

**UI 프리미티브**

- radix-ui / `@base-ui/react`: 없음. shadcn CLI·`components.json`: 없음. `components/ui/` 디렉터리: 없음. 사실.

**컴포넌트 인벤토리** (`components/`, `lib/`)

| 파일 | 행 | 역할 | 헤더/출처 표기 |
| --- | ---: | --- | --- |
| `components/admin-shell.tsx` | 158(추정, 5,463B) | `AdminShell`(rail nav 8항목 + 로그아웃 footer + skip-link, `/login`은 shell 없이 `main.login-content`), `PageHeader`(section/path/title/actions/description) | 3행 `/* Hallmark · genre: editorial-utilitarian · macrostructure: Rail-Workbench · design-system: kor-travel-map */`; 주석 "Keep the same flat rail recipe as kor-travel-map", "Keep login visually standalone, as in kor-travel-geo" |
| `components/auth/LoginForm.tsx` | 103 | 로그인 form (username 기본 `admin`, 503/429/403/401 메시지 분기, `aria-live` error) | 출처 주석 없음(커밋 `9d1a325`에서 geo 정렬로 추가) |
| `components/location-admin.tsx` | 188 | 위치 카탈로그 목록/검색/생성/enabled 토글, PAGE_SIZE 100 | — |
| `components/vworld-map-view.tsx` | 636 | `VWorldMapView`, `useVWorldMap`, `VWorldWeatherClusters`(MapLibre `cluster:true` source + DOM marker portal) | 30~35행 "React/MapLibre boundary modelled on digitie's maplibre-vworld-react `vworld-map-web` package. The app keeps the adapter local because that GitHub monorepo intentionally does not publish an npm package" |
| `components/weather-map.tsx` | 500 | `/weather` workbench: 검색·Map/List 탭·inspector·marker batch(60개 단위) | 113~116행 URL 길이 주석 |
| `lib/api.ts` | 317 | 손수 작성한 DTO 타입(`ApiEnvelope`, `PageMeta`, `Location`, `WeatherValue`, `Provider`…)과 `request<T>()` fetch 래퍼(`/api/weather` proxy 경유, `cache: "no-store"`, 실패 시 `detail`로 `Error` throw) | — |
| `lib/dagster.ts` | 58 | GraphQL 스냅샷 질의 → `/api/dagster/graphql` | — |
| `lib/session.ts` | 493 | HMAC 세션·PBKDF2 검증·durable revocation/rate-limit 클라이언트 | 주석 "matching kor-travel-geo's session contract" |
| `lib/origin.ts` | 28 | Origin allowlist CSRF | 주석 "Match the Docker Manager's exact configured frontend-origin contract" |
| `lib/navigation.ts` | 27 | `sanitizeLocalPath` (open-redirect 방지) | — |
| `lib/vworld-style.ts` | 78 | VWorld WMTS style/URL 빌더, key redaction | 주석 "follows digitie's maplibre-vworld-react repository (vworld-map-core + vworld-map-web)" |
| `lib/weather-clusters.ts` | 64 | GeoJSON cluster source 빌더 | — |

- 지정 목록 대조: admin-shell ○, login-form ○, vworld map view ○(로컬 재구현), filter-bar/pagination-bar/status-badge/data-table/empty-state/section-card/stat-strip/copy-button/json-viewer/confirm-dialog/help-tip **별도 컴포넌트 없음**. 해당 역할은 CSS 클래스(`.toolbar`, `.pagination`, `.status.on/off/warn`, `.table-wrap`, `.empty`, `.panel`, `.summary-card`, `.metric-tile`)로만 존재하고 각 page.tsx에 마크업이 인라인돼 있다. 사실.
- `className` 속성 총 220개(13개 TSX 파일, 라인 기준 180행), 동적 템플릿 className 19곳. `style={}` 인라인은 `vworld-map-view.tsx` 1곳.

**상태/데이터**

- `@tanstack/react-query` `^5.66.8`(설치 5.102.8)가 선언돼 있으나 **어떤 파일에서도 import하지 않는다**(grep). 실제 데이터 흐름은 `useState`/`useEffect`/`useCallback` + `lib/api.ts` 직접 호출. 사실(미사용 의존성).
- zustand, react-hook-form, zod: 없음. 폼은 uncontrolled/`useState`.
- API 클라이언트 생성: openapi-typescript 등 **생성기 없음**. `lib/api.ts` 타입은 수작업이며 `AGENTS.md`의 "OpenAPI export와 TypeScript client 타입을 같이 갱신" 규칙은 자동화되지 않음. 사실.
- 오류 처리: backend `application/problem+json`의 `detail`을 `Error.message`로 전달; 화면은 `error` 문자열을 `.notice.error`/`.login-error` 등에 표시.

**인증 경계** (커밋 `6003da9` 검증 포함)

| 요소 | 파일 | 내용 |
| --- | --- | --- |
| Middleware | `middleware.ts`(96행) | matcher `/((?!_next/static\|_next/image\|favicon.ico).*)`. `/login`은 이미 유효 세션이면 `next`로 redirect. `/api/auth/login`·`/api/auth/logout`은 공개. **`NODE_ENV !== "production"`이면 인증 전체 bypass**(54행). production: 자격 env 없으면 503, 세션 secret 검증 실패 503, 상태 변경 메서드(POST/PATCH/PUT/DELETE)는 `isAllowedOrigin` 아니면 403, 세션 검증 + durable revocation 확인 후 통과, 실패 시 HTML 요청은 `/login?next=` redirect, 그 외 401 |
| 세션 | `lib/session.ts` | 쿠키 `ktw_admin_session`, 8h, HttpOnly, `SameSite=Strict`, `secure`(prod 또는 x-forwarded-proto https). 값 = base64url(JSON payload) + "." + HMAC-SHA256(WebCrypto). payload `{aud:"kor-travel-weather-admin-ui", exp, fp(user-agent fingerprint), iat, sid(32B), sub, v:1}`. secret은 `WEATHER_UI_SESSION_SECRET`(prod 32자 이상, placeholder 거부) 없으면 `username:password` |
| 비밀번호 | `lib/session.ts` `verifyAdminLogin`/`verifyPassword` | `WEATHER_UI_PASSWORD_HASH`(`pbkdf2_sha256$iterations$salt$hash`, 310,000회, 100k~2M 허용) 우선, 없으면 `WEATHER_UI_PASSWORD` constant-time 비교 |
| 로그인 route | `app/api/auth/login/route.ts`(260행) | Origin 검사 → env 검사 → client IP bucket(`WEATHER_UI_TRUST_PROXY=true`일 때만 XFF 마지막 값 신뢰, 없으면 loopback origin일 때만 `ip:untrusted`, 아니면 503) → SHA-256 bucket을 API `/v1/admin/login-rate-limit/check|failure|success`로 PostgreSQL 공유 rate-limit(5회/10분) + 프로세스 메모리 rate-limit → 4KB body 제한 → 검증 → 기존 세션 revoke → 새 쿠키 |
| 로그아웃 | `app/api/auth/logout/route.ts` | Origin 검사, 발급된 세션만 durable revoke(`/v1/admin/session-revocations/revoke`), 쿠키 만료 |
| CSRF | `lib/origin.ts` | `WEATHER_UI_PUBLIC_ORIGINS`/`WEATHER_UI_PUBLIC_ORIGIN` allowlist, Origin 헤더 부재는 항상 거부, 비-prod에서만 same-origin fallback |
| 백엔드 신원 전달 | `app/api/weather/[...path]/route.ts`(78행) | `WEATHER_API_INTERNAL_URL`로 proxy, 헤더는 `accept`/`content-type`/`if-none-match`/`x-request-id`만 전달, `x-admin-token`을 서버에서 주입(`WEATHER_ADMIN_TOKEN` 또는 `KOR_TRAVEL_WEATHER_ADMIN_TOKEN`), 본문 1 MiB 상한, 응답에 `cache-control: no-store, private`와 `x-request-id` 반사. **사용자 신원(username)은 백엔드로 전달하지 않는다** |
| Dagster proxy | `app/api/dagster/graphql/route.ts` | `DAGSTER_UI_INTERNAL_URL`로 GraphQL POST 전달(1 MiB 상한) |

- 커밋 `6003da9` 내용(`git show --stat`): 8 files, +37/−49. `middleware.ts`에서 `WWW-Authenticate: Basic …` 헤더와 `Authorization: Basic` 파싱/`atob` fallback 경로를 제거하고 "Keep the web surface session-only, matching kor-travel-geo. Basic Auth is reserved for the separately protected Dagster gateway" 주석으로 대체. `README.md`, `compose.yaml`, `deploy/README.md`, `deploy/n150.md`, `docs/architecture/admin-ui.md`, `docs/runbooks/docker-app.md`, frontend `.env.example`의 Basic Auth 문구를 세션 전용으로 수정. 사실.
- 직전 커밋 `9d1a325`(21 files, +1,115/−306): `LoginForm.tsx` 신설, `lib/session.ts` 대폭 개정(+458), `alembic/versions/0008_admin_login_rate_limits.py`, API `/v1/admin/login-rate-limit/*` 3개 endpoint, `repository.py` +112, `session.test.ts` 신설. 사실.
- geo와의 일치 검증(`F:/dev/kor-travel-geo-fixes` @ `1d9d74d`, `kor-travel-geo-ui/lib/auth.ts` 4~26행 대조):

| 상수 | geo `lib/auth.ts` | weather `lib/session.ts` | 일치 |
| --- | --- | --- | --- |
| PBKDF2 알고리즘/반복 | `pbkdf2_sha256`, 310,000 | 동일 | ○ |
| 세션 TTL | 8h (`SESSION_TTL_SECONDS`) | 8h (`SESSION_MAX_AGE`) | ○ |
| HMAC, 버전 1, sid 32B, secret 최소 32자, clock skew 60s, cookie 최대 2048B, base64url 정규식 | 동일 값 | 동일 값 | ○ |
| 로그인 실패 한도 | 5회/10분 | 5회/10분 | ○ |
| SameSite | strict | strict | ○ |
| 쿠키 이름 | `ktg_ui_session` | `ktw_admin_session` | ✕(서비스별) |
| audience | `kor-travel-geo-ui` | `kor-travel-weather-admin-ui` | ✕(서비스별) |
| 백엔드 신원 전달 | `X-KTG-Actor`, `X-KTG-Roles`, `X-KTG-Admin-Proxy-Secret` (`kor-travel-geo-ui/lib/proxy.ts` 88~92행) | `x-admin-token`만 | ✕ |

결론: 세션 서명·비밀번호 해시·rate-limit **계약은 상수 수준까지 일치**하지만, 백엔드로의 신원/역할 전달 방식은 다르다(weather는 단일 admin token). 선행 검토 보고서 §3.6 "인증은 유사한 화면 아래 다른 경계를 가진다"는 결론과 부합하며, weather의 경우 프론트 세션 층은 geo와 동일 계약이라는 점을 추가로 확인했다.

**라우팅/화면 목록** (`app/`)

| 경로 | 파일 | 종류 | 행 |
| --- | --- | --- | ---: |
| `/` | `app/page.tsx` | admin 개요(health, catalog 수, 최근 run) | 104 |
| `/weather` | `app/weather/page.tsx` + `weather-map.tsx` | admin 지도 workbench | 43 |
| `/locations` | `app/locations/page.tsx` + `location-admin.tsx` | admin | 15 |
| `/datasets` | `app/datasets/page.tsx` | admin | 38 |
| `/sync-runs` | `app/sync-runs/page.tsx` | admin | 89 |
| `/settings/providers` | `app/settings/providers/page.tsx` | admin(credential CRUD) | 181 |
| `/admin/dagster` | `app/admin/dagster/page.tsx` | admin | 74 |
| `/api-test` | `app/api-test/page.tsx` | admin | 83 |
| `/login` | `app/login/page.tsx` + `LoginForm.tsx` | 인증 | 51 |
| route handlers | `app/api/auth/login`, `app/api/auth/logout`, `app/api/dagster/graphql`, `app/api/weather/[...path]` | 서버 | — |

admin 화면 8개, 로그인 1개, 사용자(비운영자) 화면 0개. `docs/architecture/admin-ui.md`의 IA 표와 일치(단, 문서 표에는 `/settings/providers`가 빠져 있음. 사실).

**반응형/모바일**

- breakpoints: `@media (max-width: 62rem)`(rail → 가로 strip, `grid-template-columns: minmax(0,1fr)`), `@media (max-width: 42rem)`(헤더/패딩 축소) 2개만 존재. min-width 계열 없음. 사실.
- `design.md`: "layout must remain contained at 320px, 375px, 414px, and 768px. Only the mobile navigation strip may scroll horizontally"; `docs/architecture/admin-ui.md`: "320px 폭에서도 버튼·입력은 44px touch target". CSS에서 `min-height: 2.75rem`(44px)은 marker/cluster 3곳(2150, 2213, 2258행)에서만 확인; 일반 버튼은 `--control-h 2.25rem`(36px). 문서의 44px 주장은 일반 컨트롤에 대해선 **미확인**.
- PC/Mobile 분기: CSS media query만. JS UA 분기·별도 모바일 라우트 없음.
- `design.md`의 "desktop rail collapses to 4rem and remembers the choice in local storage"는 `admin-shell.tsx`/`globals.css`에 `localStorage`·collapsed 코드가 없어 **미구현**(grep 결과 없음). 또한 `design.md`는 "16rem sticky rail", `tokens.css`는 `--rail: 17rem`, `globals.css` 244행 주석은 "17rem rail"로 값이 어긋난다. 사실(문서-코드 불일치).

**i18n / 접근성 / focus / reduced-motion**

- `<html lang="ko">`, 모든 UI 문자열은 한국어 하드코딩, i18n 라이브러리 없음. 날짜는 `toLocaleString("ko-KR")`.
- 접근성: skip-link(`.skip-link` → `#main-content`), `aria-current="page"`, `aria-label`, `aria-busy`, `role="alert"`, `aria-live="assertive"`, `aria-invalid`, `aria-describedby` 사용(`admin-shell.tsx`, `LoginForm.tsx`).
- focus: `:focus-visible` 규칙 9곳, `--focus`/`--ring` 토큰.
- reduced-motion: `globals.css` 1899~1908행 전역 `prefers-reduced-motion: reduce` → animation/transition 0.01ms.

**테스트·품질**

- vitest `^3.0.5`(3.2.7), `vitest.config.*` 없음, 스크립트 `vitest run --passWithNoTests`. 테스트 4개: `lib/navigation.test.ts`, `lib/session.test.ts`, `lib/vworld-style.test.ts`, `lib/weather-clusters.test.ts`(모두 순수 함수). 컴포넌트/E2E 테스트 없음. playwright 없음(`.gitignore`의 `.e2e-win/` 주석은 map에서 상속된 흔적).
- eslint 9(9.39.5) flat config: `eslint.config.mjs`가 `FlatCompat`로 `next/core-web-vitals`만 확장. 추가 플러그인/규칙 없음. react-doctor 없음.
- tsconfig: `strict: true`, `target ES2022`, `moduleResolution: "node"`(bundler 아님), `paths @/* → ./*`, `plugins: [{name:"next"}]`. `type-check` 스크립트는 `next typegen && tsc --noEmit`.
- CI frontend job은 `npm run lint`, `type-check`, `build`만 실행하고 **`npm test`(vitest)는 실행하지 않는다**(`.github/workflows/ci.yml` frontend job). `AGENTS.md` "변경 후 확인"에는 `npm test`가 포함돼 있어 규칙과 CI가 어긋난다. 사실.

**빌드/배포**

- `next.config.ts`: `reactStrictMode: true`만. `output: "standalone"` 없음, `transpilePackages`/`images` 없음.
- `deploy/Dockerfile.web`: `node:22-alpine` 3-stage(dependencies → builder → runner), `npm ci --ignore-scripts`, `NEXT_PUBLIC_VWORLD_API_KEY`를 build ARG로 inline, runner는 `node_modules`+`.next`+`next.config.ts`+`middleware.ts` 복사 후 `npm run start -- --hostname 0.0.0.0 --port 14105`.
- 포트: dev/start 모두 `--hostname 127.0.0.1 --port 14105`.

**디자인 문서**

- `packages/kor-travel-weather-admin/frontend/design.md`(45행, 영어). 핵심: "follows the current kor-travel-map admin shell and component contract. The weather domain changes only the content and primary accent hue"; Rail-Workbench; 4pt; 6px/8px radius; 36px/30px controls; Pretendard-first + Geist; hairline-only surfaces; brand navy; 검증 명령 `npm run lint/type-check/build`; 320/375/414/768 컨테인 규칙. 금지 패턴 목록은 없음. 색 톤 정의는 `tokens.css`가 정본.
- `docs/architecture/admin-ui.md`(70행): IA 표, UX contract(rail 62rem, Map/List 탭, loading/empty/error 동일 위치, 인증/CSRF), Configuration(env 목록, TRUST_PROXY, rate-limit, revocation, Fernet).

## 4. 백엔드

### 4.1 kor-travel-weather core (`src/kortravelweather`, 루트 `pyproject.toml`)

- python: `requires-python = ">=3.11"`; `ruff target-version = "py311"`; `mypy python_version = "3.11"`. CI는 3.12(`setup-python`), Docker는 `python:3.13-slim`(`deploy/Dockerfile.python`). `.python-version` 없음. **선언/CI/컨테이너 세 곳의 Python 버전이 다르다**. 사실.
- 빌드: setuptools(`setuptools>=68`, `package-dir {"" = "src"}`), lockfile `uv.lock`(version 1, revision 3, `requires-python >=3.11`), Docker `ghcr.io/astral-sh/uv:0.11.21`.
- 핵심 의존 선언(루트 `pyproject.toml`): `pydantic>=2.7`, `pydantic-settings>=2.4`, `sqlalchemy>=2.0`, `alembic>=1.13,<2`, `psycopg[binary]>=3.2,<4`, `fastapi>=0.115`, `httpx>=0.27,<1`, `uvicorn[standard]>=0.30`, `cryptography>=42`, `prometheus-client>=0.20,<1`, `python-kma-api @ git+…@0868b76b…`, `python-airkorea-api`(path), `pyproj>=3.5`. extras `dev`(pytest>=8, pytest-asyncio>=0.23, ruff>=0.9, mypy>=1.13), `dagster`(dagster>=1.9,<2, dagster-webserver>=1.9,<2). asyncpg/structlog/typer/tenacity/argon2 **미선언**(uv.lock에 structlog 26.1.0은 전이 의존으로만 존재, `src`에서 import 없음).
- 설정(`settings.py` 437행): `WeatherSettings(BaseSettings)`, `env_prefix="KOR_TRAVEL_WEATHER_"`, `env_file=(ROOT_ENV_FILE, ".env")`(루트 `.env` 우선), `extra="ignore"`, 모든 필드에 `validation_alias` 명시. `environment` 기본값 **`production`**(env 미설정 시 fail-closed). `database_url` validator가 `postgresql://`/`postgresql+psycopg://`만 허용. secret은 `SecretStr`, 빈 문자열은 None 처리. `require_admin_token()`(prod: 16자 이상, 약한 토큰 목록 거부), `require_metrics_token()`(prod: admin token과 달라야 함), `require_credential_encryption_key()`(Fernet 검증). `get_settings()`는 `lru_cache`.
- `.env.example` 키 요약(루트): core(`ENV`, `DATABASE_URL`, `GIT_COMMIT`), provider key 10종, `ENABLED_PROVIDERS` JSON 배열, run budget 6종(`MAX_GRIDS_PER_RUN` 등), `ADMIN_TOKEN`, `METRICS_TOKEN`, `METRICS_PORT`, `CREDENTIAL_ENCRYPTION_KEY`, `CORS_ORIGINS`, `API_BASE_URL`, `NEXT_PUBLIC_VWORLD_API_KEY`, compose 전용 `POSTGRES_*`, `WEATHER_UI_USER/PASSWORD/PASSWORD_HASH/SESSION_SECRET/PUBLIC_ORIGIN`.
- 관측성(`metrics.py` 614행): 표준 `logging`(structlog 아님). 메트릭 접두 **`ktw_`**(커밋 `f530531`에서 `kor_travel_weather_`에서 개명; `docs/observability.md`). 지표: `ktw_http_requests_total{method,route,status_class}`, `ktw_http_request_duration_seconds`, `ktw_http_requests_in_flight`, `ktw_provider_requests_total{provider,dataset,outcome}`, `ktw_provider_request_duration_seconds`, `ktw_sync_runs_{started,finished,active}`, `ktw_sync_{requests,source_records,values}_total`, `ktw_sync_stale_recovered_total`, `ktw_metrics_errors_total`, `ktw_metrics_server_up`, `ktw_metrics_server_bind_failures_total`. 라벨은 allow-list(`_KNOWN_PROVIDERS`, `_KNOWN_DATASETS`, `_FIXED_ROUTES`)로 축약해 cardinality를 고정. `PROMETHEUS_MULTIPROC_DIR` 다중 프로세스 수집기(dead-PID gauge 정리, 손상 mmap 격리) 자체 구현. `start_metrics_server(port)`로 Dagster worker 14103 노출.
- DB(`repository.py` 2,397행): SQLAlchemy 2.0 ORM `DeclarativeBase`, `create_engine` + `sessionmaker(expire_on_commit=False)`(동기), `AwareDateTime` TypeDecorator, 테이블 9개 모두 `weather_` 접두(`weather_locations`, `weather_source_records`, `weather_values`, `weather_current_values`, `weather_sync_runs`, `weather_sync_run_sources`, `weather_provider_credentials`, `weather_admin_session_revocations`, `weather_admin_login_rate_limits`). PostgreSQL 스키마 분리 없음(public). PostGIS 미사용: 근접 검색은 위경도 bounding box + 지구 반경 6371.0088km 계산(1938~1944행). provider credential은 Fernet 암호화, 세션 revocation은 SHA-256 digest 저장. `docs/adr/074-write-safety.md`: `weather_values`/`weather_source_records`에 UPDATE/DELETE 금지 trigger.
- CLI(`cli.py`): **argparse** `ktwctl`, 하위 명령 `init-db` 하나(insert-only bootstrap). typer 없음.
- 백업/복원: 스크립트 없음. `deploy/README.md`는 `weather-postgres` 볼륨 삭제 전 "운영 백업 확인"만 언급. 미확인(백업 절차 문서 부재).
- 테스트: 루트 `tests/` 6파일 58개 + api 26개 + dagster 21개 = **105개 test 함수**(grep `def test_`). 실 PostgreSQL 사용(`conftest.py` autouse TRUNCATE; 기본 DSN `127.0.0.1:15432/weather_test`, CI는 `services.postgres:16` 5432). testcontainers 없음. coverage gate 없음. `pytest asyncio_mode = "auto"`.
- 정적 검사: ruff `line-length 100`, `select = ["E","F","I","UP","B","ASYNC","RET","SIM"]`; mypy `strict = true`이나 **CI에서 mypy 미실행**(ruff check + pytest만). import-linter 없음(`.gitignore`/`.dockerignore`의 `.import_linter_cache/`는 map 상속 흔적).

### 4.2 kor-travel-weather-api (`packages/kor-travel-weather-api`)

- `pyproject.toml`: setuptools, `>=3.11`, deps `kor-travel-weather`(editable path `../..`), `fastapi>=0.115`, `uvicorn[standard]>=0.30`; dev `httpx`, `pytest`, `pytest-asyncio`. 자체 lockfile 없음(루트 `uv.lock` 공유). `__version__ = "0.1.0.dev0"`.
- 앱 팩토리: `create_app(settings=None, repository=None)` (`app.py` 272행). production이면 생성 시점에 `require_admin_token()`/`require_metrics_token()` 호출(fail-closed). 비-prod에서 `repository.create_schema()`.
- 라우터 prefix: `APIRouter(prefix="/v1/weather", tags=["weather"])`, `APIRouter(prefix="/v1/admin", tags=["admin"])`(`routers/weather.py` 26~27행). 시스템 경로 `/health`, `/version`(`tags=["system"]`), `/metrics`(`include_in_schema=False`). `/debug`, `/ops`, `/v2` 없음.
- 미들웨어: `CORSMiddleware`(`cors_origins` 설정 시, `allow_credentials=False`, 메서드 GET/POST/PATCH/PUT/DELETE), `@api.middleware("http") request_context`(`x-request-id` 수용/생성, 응답에 `x-request-id`·`x-duration-ms`, `/metrics` 제외 HTTP 지표 기록).
- 에러 envelope: `HTTPException`·`RequestValidationError` 핸들러가 `application/problem+json`으로 `Problem{type:"about:blank", title, status, detail, code("HTTP_ERROR"/"VALIDATION_ERROR"), request_id, errors[]}` 반환(`response.py`, `app.py _problem`).
- 성공 envelope: `{data, meta{request_id, generated_at(KST ISO), duration_ms, page{limit, offset, returned, total|null}|null}}`(`response.py` `Envelope[T]`, `make_meta`). 페이지네이션은 `limit`/`offset` Query(`ge=1, le=1000` 등 경로별 상한). cursor 없음.
- 인증: `auth.py` `require_admin` — `x-admin-token` 헤더를 `secrets.compare_digest`로 비교. 개발 환경에서 token 미설정이면 허용, prod fail-closed. argon2/pbkdf2 등 사용자 계정 개념 없음(단일 공유 토큰). ServiceToken 없음.
- rate limit: API 자체 rate limit 없음. 단, admin UI 로그인용 `/v1/admin/login-rate-limit/{check,failure,success}`와 `/v1/admin/session-revocations/{check,revoke}`(PostgreSQL 저장)를 제공한다(`routers/weather.py` 889~980행; `openapi.json`에는 이 5개 경로가 **포함되지 않음** — export 시점 이후 추가됐거나 `include_in_schema` 처리로 추정. 미확인).
- OpenAPI: `scripts/export_openapi.py`가 `KOR_TRAVEL_WEATHER_ENV=development` 강제 후 `app.openapi()`를 `openapi.json`(indent 2, ensure_ascii False)에 기록. CI "Check OpenAPI is exported" step이 재생성 후 `git diff --exit-code`로 drift 검사. 문서 버전 `openapi: 3.1.0`, `info.version 0.1.0.dev0`, 경로 16개/오퍼레이션 18개/스키마 31개, `securitySchemes.AdminToken`(apiKey, header `x-admin-token`). `custom_openapi()`가 `/v1/*`에 422, `/v1/admin/*`에 401·security, `{location_id}`/`{run_id}`에 404, admin 쓰기에 409 Problem 응답을 주입. operationId는 FastAPI 기본(`list_locations_v1_weather_locations_get`) — 명시 규약 없음. `servers`/`tags` 메타 없음.
- 테스트: `tests/test_weather_api.py` 26개, `TestClient(create_app(settings, repository))`, 실 PostgreSQL.

### 4.3 kor-travel-weather-dagster (`packages/kor-travel-weather-dagster`)

- `pyproject.toml`: deps `kor-travel-weather`(path), `dagster>=1.9,<2`, `dagster-webserver>=1.9,<2`; 설치 1.13.20.
- `definitions.py`: 자산 3개 `kma_weather_sync`, `airkorea_weather_sync`, `external_weather_sync`; job 3개 `kma_weather_job`, `airkorea_weather_job`, `external_weather_job`(`define_asset_job` 후 `.resolve()`); 스케줄 3개 `hourly_kma_weather`(`0 * * * *`), `hourly_airkorea_weather`(`10 * * * *`), `hourly_external_weather`(`15 * * * *`), 모두 `Asia/Seoul`, `DefaultScheduleStatus.RUNNING`. 리소스 `KmaClientResource`, `WeatherRepositoryResource`, `AirKoreaResource`, `ExternalWeatherProviderResource`(`ConfigurableResource`). import 시 `KOR_TRAVEL_WEATHER_METRICS_PORT`로 metrics 서버 기동.
- 운영: `dagster dev -m kortravelweather_dagster.definitions -p 14102`, `DAGSTER_HOME=/opt/dagster/home` 볼륨, `PROMETHEUS_MULTIPROC_DIR` tmpfs(`compose.yaml`).
- 테스트: `tests/test_kma_weather.py` 21개(grid dedupe, quota, atomic publish 등; `docs/test-strategy.md`).

### 4.4 python-airkorea-api snapshot (`packages/python-airkorea-api`)

- `pyproject.toml`: `python-airkorea-api 0.4.0`, `>=3.10`, GPL-3.0-or-later, deps `pydantic>=2.7`, `pyproj>=3.5`, `httpx>=0.27`; CLI `airkorea`; ruff `line-length 100`, select `E,F,I,UP,B`; mypy strict; pytest `-m 'not integration'`.
- README 하단(루트 `README.md` "저장소 구조" 절): `python-airkorea-api` 커밋 `9b00dd654f248821798688a1e4afb6edbfd4779f`에서 복사한 snapshot. 추적 파일 50개(`src/airkorea/*.py` 14개, `tests/*` 12개, `docs/*.md` 11개: `journal.md`, `resume.md`, `tasks.md`, `repeated-mistakes.md`, `decisions.md`, `documentation-style.md`, `testing.md`, `troubleshooting.md`, `library-surface.md`, `implementation-status.md`, `debug-fixtures.md`).
- 이 snapshot은 GitHub `digitie/python-airkorea-api`와 **중복 보관**이다(공통 라이브러리 중복 금지 대상과 직접 충돌). `deploy/Dockerfile.python`도 이 경로를 `uv sync` 전에 복사한다. 사실.

## 5. 문서·에이전트 규약

- 진입 파일:

| 파일 | 행/크기 | 역할 | 언어 |
| --- | --- | --- | --- |
| `AGENTS.md` | 39행 / 1,762B | 범위, 식별자 정본 표(distribution/import/API/Dagster/env prefix/provider), 개발 규칙 8개, 변경 후 확인 명령 3줄, PR 규칙 | 한국어 |
| `README.md` | 167행 / 9,842B | 개요·목표·운영 모델·빠른 시작·구조·소비자 계약·이식 기록·라이선스 | 한국어 |
| `packages/kor-travel-weather-admin/frontend/design.md` | 45행 | admin 디자인 계약 | 영어 |
| `docs/weather-api.md` | 100행 | 소비자용 API 계약 | **영어**(다른 docs는 한국어) |
| `CLAUDE.md`, `SKILL.md`, `.claude/`, `.codex/` | 없음 | — | — |

- 지시 우선순위: 명시 규정 없음. `AGENTS.md` 하나가 정본이며 하위 패키지 README가 실행 명령을 보완한다(`docs/dev-environment.md` "package README의 `cd ../..`도 이 root 경계를 명시한다"). 미확인(우선순위 문장 부재).
- 언어 정책: `AGENTS.md` "문서·주석은 한국어를 기본으로 하되 코드 식별자, URL, provider 원문은 그대로 둔다". 실제로 `docs/weather-api.md`와 `design.md`, 코드 주석 상당수(`session.ts`, `metrics.py` 등)는 영어다. 사실(정책과 부분 불일치).
- `docs/` 트리(총 634행, `wc -l`):

| 디렉터리/파일 | 내용 | 규약 |
| --- | --- | --- |
| `docs/adr/README.md`, `072-*.md`, `074-*.md`, `089-*.md` | ADR 3편(각 6~8행) + 적용 표 | 번호는 `kor-travel-map` 체계 상속(020/048/062/072/074/089/101 중 파일은 3개만 존재) |
| `docs/decisions.md` | Decisions index(15행) | ADR 요약 목록, ADR-101(KMA 특보) 추가 |
| `docs/architecture/*.md` 7편 | architecture, admin-ui, backend-package, dagster-boundary, data-model, provider-contract, rest-api | 정본 설계 문서 |
| `docs/etl/*.md` 2편 | KMA ETL 절차, normalization | — |
| `docs/migrations/001-external-providers.md` | provider 활성화 절차 | — |
| `docs/runbooks/README.md`, `docker-app.md` | 기동 순서·포트·migration head(`0008`) | — |
| `docs/dev-environment.md`, `test-strategy.md`, `observability.md`, `integration-map.md`, `weather-api.md` | 단일 문서 | — |
| `tasks/`, `tasks-rule/`, `tasks-done/`, `journal/`, `resume/`, `reviews/`, `archive/` | **없음** | task ID 체계 없음 |

- 개발 환경 정본: `README.md` 빠른 시작이 `cd /mnt/f/dev/kor-travel-weather`(WSL 경로)와 `set -a; . .env; set +a`, `TMPDIR=/tmp`를 사용 → **Linux/WSL 셸이 정본**. PowerShell 안내 없음. 사실.
- worktree 정책·codegraph: `.gitignore`가 `.codegraph/`를 무시하며 "자세히는 docs/codegraph-worktree.md"를 가리키지만 그 문서는 **존재하지 않는다**(map에서 상속된 잔재). worktree 정책 문서 없음.
- 리뷰 정책: 2인 적대적 리뷰 등 명문 규정 없음. `AGENTS.md` "PR은 초안으로 먼저 만들고, 기능 단위로 작은 커밋". 커밋 메시지는 `type(scope): subject` 형식(`fix(admin):`, `feat(web):`, `perf(api):`), 브랜치 접두 `feat/`, `fix/`, `perf/`(`git branch -a`). PR #18~#22 머지 이력.
- 보안 감사: push 전 스캔 규정 없음. `.gitignore`의 `*.local.md` 주석이 "정본 위치/절차는 AGENTS.md §prod 배포 & 보안 감사"를 가리키나 이 저장소 `AGENTS.md`에 그 절이 **없다**(map 상속 잔재). `.security-audit-patterns.local` ignore만 존재.

## 6. CI·배포·운영

- `.github/workflows/ci.yml`(유일한 워크플로): 트리거 `push`(main, `feat/**`), `pull_request`. job `python`(ubuntu, `services.postgres:16`, Python 3.12, `astral-sh/setup-uv@v5`, `uv sync --locked --extra dev --extra dagster`, `alembic upgrade head`, `pytest -q`, `ruff check .`, `promtool check config/rules`(prom/prometheus:v3.5.0 docker), OpenAPI export drift). job `frontend`(Node 20, `npm ci --ignore-scripts`, `lint`, `type-check`, `build`). gate 부재: mypy, vitest, 보안 스캔, Docker build 검증.
- pre-commit: 없음.
- compose: `compose.yaml`(7 서비스: `db` postgres:16-alpine shm 1g, `api`, `dagster`, `dagster-gateway` nginx Basic Auth, `migrate` one-shot `alembic upgrade head`, `prometheus` v3.5.0, `web`), `deploy/compose.n150.yaml`(api/dagster-gateway/web 포트를 `<prod-address>`로 `!override`, `WEATHER_UI_TRUST_PROXY=true`, 공개 origin).
- 포트 할당(`deploy/README.md` 표): 14100 PostgreSQL, 14101 API, 14102 Dagster(gateway 경유), 14103 Dagster worker metrics(compose 내부 `expose`만), 14104 Prometheus(loopback), 14105 web. 기본 바인딩 모두 `127.0.0.1`.
- prod(n150) 규약(`deploy/n150.md`): 호스트 `digitie@<prod-address>`, 경로 `~/kor-travel-weather`, `.env` 모드 600, 배포는 `git pull --ff-only` + `docker compose --env-file .env -f compose.yaml -f deploy/compose.n150.yaml up -d --build`. 도메인 `https://<prod-host>`, `https://<prod-host>`(Basic Auth), `https://<prod-host>`. HAProxy upstream 매핑 명시. Prometheus 14104는 공개하지 않음.
- 시크릿: `.env`(untracked), compose `secrets.metrics_token.environment` native secret으로 `/run/secrets/metrics.token` 마운트, admin token/metrics token/Fernet key/session secret은 compose interpolation `:?` 필수. Docker 이미지에 secret 미포함(`.dockerignore` `.env*`).
- Dockerfile: `deploy/Dockerfile.python`(python:3.13-slim + uv 0.11.21, `INSTALL_DAGSTER` ARG로 API/Dagster 이미지 분기, airkorea snapshot 선복사), `deploy/Dockerfile.web`, `deploy/Dockerfile.dagster-gateway`(nginx:1.27-alpine, `openssl passwd -apr1`로 htpasswd 생성, POST에 same-origin Origin 요구).

## 7. 외부 연동 (cross-repo)

| 대상 | 방향 | 방식 | 근거 |
| --- | --- | --- | --- |
| kor-travel-map, PinVi | weather → 소비자 | REST `/v1/weather/resolve`, `/nearby`, `/markers`; DB 직접 접근 없음 | `docs/integration-map.md`, `docs/architecture/rest-api.md` |
| kor-travel-map | 코드 이식 원본 | 커밋 `41aaa86c…` 기준 DTO/ETL/admin UI 패턴 이식; CSS 토큰 "copied from kor-travel-map" | `README.md` "원본 이식 기록", `tokens.css` 1~4행 |
| kor-travel-geo | 인증 계약 정렬 | PBKDF2/HMAC 세션/rate-limit 상수 일치(§3.1 표) | `lib/session.ts`, 커밋 `9d1a325`/`6003da9` |
| kor-travel-docker-manager | 패턴 차용 | Origin allowlist CSRF 계약 | `lib/origin.ts` 주석, `docs/architecture/admin-ui.md` "Docker Manager와 동일하게" |
| python-kma-api | 의존 | git 핀 `@0868b76bd4b7de96b20f667e431c3f43b67cb537`(uv.lock `python-kma-api 0.1.0`) | 루트 `pyproject.toml` |
| python-airkorea-api | 의존(벤더) | 저장소 내 snapshot path 의존(0.4.0, 원 커밋 `9b00dd65…`) | `[tool.uv.sources]`, `README.md` |
| maplibre-vworld-react | **미의존** | npm 패키지 부재를 이유로 `components/vworld-map-view.tsx`·`lib/vworld-style.ts`에 로컬 재구현; CSS도 "WeatherMarker primitive from digitie/maplibre-vworld-react" 호환 형태 유지 | `vworld-map-view.tsx` 30~35행, `globals.css` 2203행 |
| vworld-map-* 벤더 tgz | 없음 | `package.json`에 file:/tgz 의존 없음 | `package.json` |
| ServiceToken / 서비스 간 인증 | 없음 | admin `x-admin-token` 단일 토큰; 공개 read는 무인증 | `auth.py` |
| Concierge, docker-manager 런타임 호출 | 없음 | — | grep 결과 없음 |

## 8. 공통화 후보

| # | 영역 | 근거 경로 | 신뢰도 | 비고 |
| ---: | --- | --- | --- | --- |
| 1 | 디자인 토큰(oklch 팔레트, spacing, radius, control 높이, 모션) | `frontend/app/tokens.css` 6~100행 | high | 헤더가 "kor-travel-map admin design system" 복사본임을 명시. shadcn 이름(`--background`…)까지 이미 갖춰 `@theme inline` 매핑이 직접 가능 |
| 2 | 세션 서명/PBKDF2/rate-limit 순수 함수 | `frontend/lib/session.ts` 317~584행 | high | geo `lib/auth.ts`와 상수·알고리즘 동일. 쿠키명·audience만 파라미터화하면 공유 가능. 단 선행 보고서 §3.6대로 세션 저장·신원 전달은 앱 소유로 남김 |
| 3 | Origin allowlist CSRF 검사 | `frontend/lib/origin.ts` | high | docker-manager 계약을 그대로 따른다고 주석 |
| 4 | `sanitizeLocalPath` open-redirect 방지 | `frontend/lib/navigation.ts` + test | high | 순수 함수, 테스트 동반 |
| 5 | Admin shell(rail + PageHeader + skip-link + logout footer) | `components/admin-shell.tsx`, `globals.css` 244~536행 | high | "same flat rail recipe as kor-travel-map". 헤더 슬롯(section/path/title/actions) 계약 |
| 6 | 로그인 화면(standalone card + form + 상태 메시지 분기) | `components/auth/LoginForm.tsx`, `globals.css` 1789~1889행 | high | "same … as kor-travel-geo" 명시 |
| 7 | 서버측 API proxy route handler(헤더 allow-list, admin token 주입, 본문 상한, request-id 반사) | `app/api/weather/[...path]/route.ts` | medium | geo는 신원 헤더까지 전달하므로 헤더 정책을 옵션화해야 함 |
| 8 | 패널/테이블/폼/버튼/상태 배지 CSS primitives | `globals.css` 537~914행(`.panel`, `.table-wrap`, `.button.primary/secondary/ghost/danger`, `.status.on/off/warn`, `.field`, `.toolbar`, `.pagination`) | high | 컴포넌트가 아니라 CSS만 있으므로 common의 shadcn 컴포넌트로 대체하는 형태 |
| 9 | reduced-motion·focus-visible·skip-link 접근성 레시피 | `globals.css` 1899~1908행, `:focus-visible` 9곳, `.skip-link` | high | 규칙(UX 가이드) 산출물 |
| 10 | 반응형 규칙(62rem rail 전환, 42rem 압축, 320/375/414/768 컨테인) | `globals.css` 1913~2142행, `design.md` | medium | breakpoint 값을 common 규칙으로 고정 가능. 44px 터치 규칙은 코드로 미검증 |
| 11 | REST envelope `{data, meta{request_id, generated_at, duration_ms, page}}` + `application/problem+json` Problem | `packages/kor-travel-weather-api/src/kortravelweather_api/response.py`, `app.py` `_problem` | high | ADR-048 계열; map 기원. 공통 pydantic 모델/예외 핸들러 후보 |
| 12 | `x-request-id`/`x-duration-ms` 미들웨어 + HTTP 지표 훅 | `app.py` `request_context` | high | 저장소 간 동일 헤더명 확인 필요(geo/map 인벤토리 참조) |
| 13 | OpenAPI export 스크립트 + CI drift 검사 | `scripts/export_openapi.py`, `ci.yml` "Check OpenAPI is exported" | high | 규칙 산출물(OpenAPI 규약). operationId/tag 규약은 미정 |
| 14 | 저-cardinality Prometheus 계측 모듈(allow-list 라벨, multiprocess 정리) | `src/kortravelweather/metrics.py` | medium | 접두(`ktw_`)와 allow-list만 파라미터화하면 재사용 가능. 614행으로 무거움 |
| 15 | pydantic-settings 규약(env prefix, root .env 우선, prod 기본, secret 검증, 약한 토큰 목록) | `src/kortravelweather/settings.py` 40~70행, 336~373행 | medium | 규칙 문서화 후보. 코드 공유는 prefix 파라미터화 필요 |
| 16 | Alembic 레이아웃(루트 `alembic/`, `NNNN_snake` 파일명 = revision id, compose `migrate` one-shot) | `alembic/versions/*.py`, `compose.yaml` `migrate` | high | 규칙 산출물 |
| 17 | ruff/mypy 기본 설정(`line-length 100`, `select E,F,I,UP,B,ASYNC,RET,SIM`, `mypy strict`) | 루트 `pyproject.toml` | high | airkorea snapshot은 `E,F,I,UP,B`로 부분집합 |
| 18 | 테스트 전략(실 PostgreSQL, TRUNCATE 격리, CI service container) | `conftest.py`, `ci.yml` | medium | testcontainers 미사용. 다른 저장소와 방식 비교 필요 |
| 19 | Compose 포트 대역/loopback 바인딩/n150 override 규약 | `deploy/README.md`, `deploy/compose.n150.yaml` | high | 141xx 대역 사용. 저장소별 대역 표를 common 규칙으로 |
| 20 | Dagster metrics/PROMETHEUS_MULTIPROC_DIR 운영 패턴 | `compose.yaml` dagster 서비스, `definitions.py` `_start_metrics_server_from_env` | low | Dagster 사용 저장소(map?)에 한정 |
| 21 | VWorld MapLibre 어댑터 | `components/vworld-map-view.tsx`, `lib/vworld-style.ts` | medium | 이미 분리된 `maplibre-vworld-react`와 중복이므로 common이 아니라 **기존 라이브러리 소비로 전환**할 후보(npm 배포 부재가 원인) |
| 22 | python-airkorea-api snapshot | `packages/python-airkorea-api` | high | 공통화가 아니라 **중복 제거** 대상(GitHub `digitie/python-airkorea-api` git 핀으로 전환) |
| 23 | Provider transport 경계(`ProviderError` 분류, `redact_secrets`, `source_record_key` 해시) | `src/kortravelweather/providers/base.py` | low | python-*-api 패밀리와 역할 중복 여부 확인 필요 |

## 9. 이 저장소 고유 차이·주의점

| 영역 | 내용 | 공통화 시 영향 |
| --- | --- | --- |
| Tailwind 부재 | 유일하게 Tailwind가 전혀 없는 앱. 2,495행 손수 CSS, 170개 클래스, 23개 bare element 규칙 | v4 전환은 "설정 추가"가 아니라 "스타일 시스템 교체". §9.1 정량화 참조 |
| 미사용 의존성 | `@tanstack/react-query` 선언·설치되었으나 import 0건 | 버전 일치화 시 제거 또는 실제 채택 결정 필요 |
| DTO 타입 수작업 | `lib/api.ts` 타입이 `openapi.json`과 수동 동기화 | common의 OpenAPI 규칙(생성기 채택)과 충돌하지 않지만 도입 작업 발생 |
| 인증 bypass | `middleware.ts` 54행: 비-production은 인증 전체 생략 | 공통 미들웨어로 대체 시 개발 편의 동작을 보존할지 결정 |
| 백엔드 신원 전달 없음 | proxy가 `x-admin-token`만 주입, 사용자명 미전달; API는 단일 토큰·역할 없음 | geo식 actor/roles 헤더를 common 규약으로 삼으면 API 측 변경 필요 |
| 다크 모드 | 토큰은 있으나 토글 없음 | common 다크 정책 채택 시 무료로 적용되지만 검증된 적 없음 |
| 폰트 미로딩 | `next/font` 없음, `--font-geist`/`--font-pretendard` 미정의 | common 폰트 규칙(pretendard 로딩 방식) 적용 필요 |
| Node/Python 버전 불일치 | Node CI 20 vs Docker 22; Python 선언 3.11 vs CI 3.12 vs Docker 3.13 | 버전 일치화 정책의 직접 대상 |
| Next 15 | 형제 앱들(선행 보고서 §2 표: geo/map/concierge/PinVi Next 16.x)보다 한 메이저 낮음 | common이 Next 16 기준이면 업그레이드 선행 |
| `moduleResolution: node` | 최신 Next 템플릿의 `bundler`가 아님 | common 패키지 `exports` 해석에 영향(사전 검증 필요) |
| CI에서 vitest·mypy 미실행 | `AGENTS.md`는 `npm test` 요구, `mypy strict` 선언만 존재 | common 품질 gate 규칙과 차이 |
| ADR 번호 상속 | 파일 3개(072/074/089)만 있고 나머지 번호는 map 참조 | 규칙 문서 정본 위치를 common으로 옮길 때 번호 충돌 주의 |
| 문서 잔재 | `.gitignore`가 존재하지 않는 `docs/codegraph-worktree.md`, `AGENTS.md §prod 배포 & 보안 감사`를 참조 | 공통 `.gitignore`/AGENTS 템플릿 정리 대상 |
| 벤더 snapshot | `python-airkorea-api` 50파일 + 자체 docs 규약(journal/resume/tasks) 동봉 | 중복 금지 원칙과 충돌 |
| 메트릭 접두 | `ktw_`(최근 개명) | common 메트릭 접두 규칙(`ktg_` 등)과 일관성 있음 |
| Dagster 포함 | 다른 저장소에 없을 수 있는 실행 표면 | 공통화 범위에서 제외하거나 별도 모듈 |
| 영어 문서 혼재 | `docs/weather-api.md`, `design.md`, 코드 주석 대부분 영어 | 언어 정책 규칙 수립 시 예외 목록 필요 |

### 9.1 Tailwind v4 전환 예상 작업 범위 (정량, 추정)

기준: 사실 집계는 `wc -l`, grep, 조사 스크립트 결과. 분류·비율은 추정.

| 구분 | 수치 | 근거 |
| --- | ---: | --- |
| 교체 대상 CSS 총 행 | 2,495행 (`globals.css` 2,334 + `tokens.css` 161) | `wc -l` |
| CSS 고유 클래스 선택자 | 170개 | grep `\.[a-zA-Z][\w-]*` unique |
| 최상위 규칙 블록 | 약 277개 | grep |
| bare element 규칙 | 23종 | grep |
| `className` 속성 / 파일 | 220개 / 13 TSX 파일 (`app/page.tsx` 20, `api-test` 14, `datasets` 5, `sync-runs` 10, `weather` 4, `admin/dagster` 14, `settings/providers` 20, `admin-shell.tsx` 26, `location-admin.tsx` 19, `vworld-map-view.tsx` 6, `weather-map.tsx` 33, `LoginForm.tsx` 9; 라인 기준 180) | grep -c/-o |
| 동적 className | 19곳 | grep `className={` |
| 신규/수정 설정 파일 | `package.json`(tailwindcss, `@tailwindcss/postcss` 추가, react-query 제거 여부), `postcss.config.mjs` 신규, `components.json` 신규(shadcn 채택 시), `app/globals.css` 재작성, `app/tokens.css` → `@theme` 블록 | 파일 부재 확인 |
| 총 손대는 파일 | 약 18개(CSS 2 + TSX 13 + `layout.tsx` + `package.json` + `postcss.config.mjs` [+ `components.json`]) | — |

절별 처리 추정(행 기준, `globals.css` 절 표 참조):

| 처리 | 절 | 행 합계 | 비율 |
| --- | --- | ---: | ---: |
| Tailwind preflight로 대체(삭제) | base reset(1–243) | 243 | 10% |
| common 공유 컴포넌트/유틸리티로 대체 | shell(244–536), data surfaces(537–744), cards(745–914), forms 중 공통(1377–1648 일부), login(1789–1889), 모션(1890–1909) | 약 1,000~1,190 | 40~48% |
| 유틸리티 variant(`max-lg:` 등)로 흡수 | responsive(1910–2142) | 233 | 9% |
| 도메인 CSS로 잔존(`@layer components` 또는 CSS module) | workbench(915–1376), Dagster(1649–1788), markers/clusters(2143–2335) | 약 795~875 | 32~35% |

- 토큰은 shadcn 변수명을 이미 사용하므로 `tokens.css` 161행 중 색/radius 부분은 `@theme inline { --color-background: var(--background); … }` 매핑으로 거의 1:1 이전 가능(추정). `--space-*`, `--control-h`, `--rail`은 `@theme`의 `--spacing-*`/커스텀 변수로 유지.
- 하드코딩 marker 색 23곳은 도메인 토큰(`--weather-marker-*`)으로 승격해야 common 색 규칙과 분리된다(후보).
- 위험: 전역 `button`/`table`/`a` 규칙에 의존하는 마크업이 preflight 도입 후 무스타일이 되므로 13개 TSX 전부를 확인해야 한다. `design.md`가 요구하는 320~768px 컨테인 검증을 대체 수단(playwright 없음) 없이 수동으로 해야 한다.
- 전환 규모 감각: TSX 220개 className 속성의 클래스 문자열을 전량 교체하는 작업이며, 컴포넌트 수가 적어(파일 13개) 리팩터링 단위는 작지만 CSS 절대량(2.5k행)은 형제 앱의 shadcn 기반보다 크다(비교 수치는 다른 인벤토리 참조. 미확인).

## 10. 버전 표

| 항목 | 선언 범위 | lockfile 설치 버전 | 근거 |
| --- | --- | --- | --- |
| node | 없음 | CI 20 / Docker `node:22-alpine` | `ci.yml`, `Dockerfile.web` |
| npm | 없음 | lockfileVersion 3 | `package-lock.json` |
| next | `^15.2.0` | 15.5.24 | `package.json`, `package-lock.json` |
| react / react-dom | `^19.0.0` | 19.2.8 | 〃 |
| typescript | `^5.7.3` | 5.9.3 | 〃 |
| tailwindcss | 없음 | 없음 | 〃 |
| @tailwindcss/postcss | 없음 | 없음(postcss 8.4.31 전이) | 〃 |
| @base-ui/react / radix-ui | 없음 | 없음 | 〃 |
| shadcn | 없음 | 없음 | `components.json` 부재 |
| lucide-react | `^0.468.0` | 0.468.0 | `package.json` |
| eslint / eslint-config-next / @eslint/eslintrc | `^9.0.0` / `^15.5.24` / `^3.3.6` | 9.39.5 / 15.5.24 / 3.3.6 | 〃 |
| vitest | `^3.0.5` | 3.2.7 | 〃 |
| playwright | 없음 | 없음 | — |
| @tanstack/react-query | `^5.66.8` | 5.102.8 (import 0건) | 〃 |
| zod / zustand / react-hook-form | 없음 | 없음 | 〃 |
| maplibre-gl | `^5.24.0` | 5.24.0 | 〃 |
| @types/node / @types/react | `^22.13.0` / `^19.0.0` | 22.20.1 / 19.2.18 | 〃 |
| python | `>=3.11` | CI 3.12 / Docker 3.13-slim / uv.lock `requires-python >=3.11` | `pyproject.toml`, `ci.yml`, `Dockerfile.python` |
| uv | — | Docker `uv:0.11.21`, CI `setup-uv@v5` | 〃 |
| fastapi | `>=0.115` | 0.141.1 | `uv.lock` |
| starlette | (전이) | 1.6.0 | 〃 |
| pydantic / pydantic-settings | `>=2.7` / `>=2.4` | 2.13.5 / 2.15.0 | 〃 |
| sqlalchemy | `>=2.0` | 2.0.52 | 〃 |
| alembic | `>=1.13,<2` | 1.19.1 | 〃 |
| psycopg[binary] | `>=3.2,<4` | 3.3.4 | 〃 |
| asyncpg | 없음 | 없음 | 〃 |
| httpx | `>=0.27,<1` | 0.28.1 | 〃 |
| uvicorn[standard] | `>=0.30` | 0.52.4 | 〃 |
| prometheus-client | `>=0.20,<1` | 0.26.0 | 〃 |
| cryptography | `>=42` | 50.0.1 | 〃 |
| pyproj | `>=3.5` | 3.7.2 | 〃 |
| dagster / dagster-webserver | `>=1.9,<2` (extra) | 1.13.20 / 1.13.20 | 〃 |
| ruff | `>=0.9` (dev) | 0.16.5 | 〃 |
| mypy | `>=1.13` (dev) | 2.3.1 | 〃 |
| pytest / pytest-asyncio | `>=8` / `>=0.23` | 9.1.1 / 1.4.0 | 〃 |
| structlog | 없음(전이) | 26.1.0 | 〃 |
| typer / tenacity / argon2-cffi | 없음 | 없음 | 〃 |
| python-kma-api | git `@0868b76b…` | 0.1.0 (git) | 〃 |
| python-airkorea-api | path | 0.4.0 (directory) | 〃 |
| PostgreSQL | — | compose `postgres:16-alpine`, CI `postgres:16` | `compose.yaml`, `ci.yml` |
| Prometheus | — | `prom/prometheus:v3.5.0` | 〃 |
| nginx(gateway) | — | `nginx:1.27-alpine` | `Dockerfile.dagster-gateway` |

## 11. 미확인·열린 질문

1. `openapi.json`에 `/v1/admin/session-revocations/*`와 `/v1/admin/login-rate-limit/*` 5개 경로가 없다. CI drift 검사가 통과했다면 `include_in_schema=False`일 가능성이 있으나 `routers/weather.py` 해당 데코레이터 옵션을 직접 확인하지 않았다. 미확인.
2. 브라우저에서 실제 렌더되는 폰트(Geist/Pretendard 로컬 설치 여부)와 `.dark` 팔레트의 시각 검증은 수행하지 않았다. 미확인.
3. `docs/architecture/admin-ui.md`의 "320px에서 44px touch target" 주장에 대응하는 일반 컨트롤 CSS를 찾지 못했다(`--control-h 36px`). 실제 렌더 크기 미확인.
4. `design.md`의 rail 접기(4rem, localStorage) 기능이 제거된 것인지 미구현인지 git 이력으로 추적하지 않았다.
5. `kor-travel-map` 원본(`41aaa86c…`)의 tokens/globals와 weather 복사본 간 drift 정도는 map 인벤토리와 대조가 필요하다.
6. Python 3.11/3.12/3.13 중 운영 정본이 무엇인지(Docker 3.13이 실제 운영) 문서에 명시가 없다.
7. `@tanstack/react-query` 미사용의 의도(향후 채택 예정 vs 잔재) 미확인.
8. 백업/복원 절차 부재가 의도된 것인지(n150 볼륨 백업이 외부 절차인지) 미확인.
9. `weather_*` 테이블을 별도 PostgreSQL 스키마로 분리할 계획 여부 미확인(현재 public).
10. 선행 보고서 표의 weather 행("`^15.2.0` / `^19.0.0`, 자체 tokens.css·CSS, Tailwind 직접 의존성 없음")은 본 조사로 재확인됐다. 보고서 §7.3 "사전 빌드 CSS + CSS 변수 우선"은 weather의 현 구조와 호환되지만, 사용자 전제 (1) "Tailwind v4로 전환"과는 방향이 다르므로 설계 단계에서 양자택일이 필요하다(열린 결정).
11. Dagster gateway Basic Auth의 비밀번호가 `WEATHER_UI_PASSWORD`와 동일 변수를 공유한다(`compose.yaml` `DAGSTER_UI_PASSWORD: ${WEATHER_UI_PASSWORD…}`). PBKDF2 해시만 설정한 배포에서 gateway 비밀번호 운용 방식은 문서상 "평문 값은 Dagster gateway 등 별도 호환 경계에서만 사용"으로만 설명된다. 운영 실제 미확인.

## 12. 근거 파일 목록 (실제로 읽은 파일)

루트 및 설정
1. `AGENTS.md`
2. `README.md`
3. `LICENSE`(1~3행)
4. `pyproject.toml`
5. `uv.lock`(패키지 버전 추출)
6. `.env.example`
7. `.gitignore`
8. `.gitattributes`
9. `.dockerignore`
10. `conftest.py`
11. `alembic.ini`
12. `alembic/env.py`
13. `alembic/versions/0001_weather_source.py` ~ `0008_admin_login_rate_limits.py`(헤더)
14. `compose.yaml`
15. `.github/workflows/ci.yml`

deploy
16. `deploy/README.md`
17. `deploy/n150.md`
18. `deploy/compose.n150.yaml`
19. `deploy/Dockerfile.web`
20. `deploy/Dockerfile.python`
21. `deploy/Dockerfile.dagster-gateway`
22. `deploy/nginx/dagster-gateway.conf`
23. `deploy/prometheus/prometheus.yml`
24. `deploy/prometheus/alerts.yml`(1~40행)

docs
25. `docs/dev-environment.md`
26. `docs/decisions.md`
27. `docs/adr/README.md`, `docs/adr/072-weather-bitemporal.md`, `docs/adr/074-write-safety.md`, `docs/adr/089-current-summary-fact-reference.md`
28. `docs/architecture/admin-ui.md`
29. `docs/architecture/architecture.md`
30. `docs/architecture/backend-package.md`
31. `docs/architecture/dagster-boundary.md`
32. `docs/architecture/data-model.md`
33. `docs/architecture/provider-contract.md`
34. `docs/architecture/rest-api.md`
35. `docs/etl/kma-weather-etl.md`, `docs/etl/weather-feature-normalization.md`
36. `docs/migrations/001-external-providers.md`
37. `docs/observability.md`
38. `docs/test-strategy.md`
39. `docs/runbooks/README.md`, `docs/runbooks/docker-app.md`
40. `docs/integration-map.md`
41. `docs/weather-api.md`(1~50행)

core / API / Dagster
42. `src/kortravelweather/__init__.py`
43. `src/kortravelweather/settings.py`
44. `src/kortravelweather/metrics.py`
45. `src/kortravelweather/cli.py`(grep)
46. `src/kortravelweather/repository.py`(1~50행, 클래스/테이블 grep, 1938~1944행)
47. `src/kortravelweather/models.py`(클래스 목록)
48. `src/kortravelweather/providers/base.py`(1~60행, grep)
49. `src/kortravelweather/alerts.py`(1~25행)
50. `packages/kor-travel-weather-api/pyproject.toml`
51. `packages/kor-travel-weather-api/README.md`
52. `packages/kor-travel-weather-api/openapi.json`(구조 집계)
53. `packages/kor-travel-weather-api/scripts/export_openapi.py`
54. `packages/kor-travel-weather-api/src/kortravelweather_api/__init__.py`
55. `packages/kor-travel-weather-api/src/kortravelweather_api/app.py`
56. `packages/kor-travel-weather-api/src/kortravelweather_api/auth.py`
57. `packages/kor-travel-weather-api/src/kortravelweather_api/response.py`
58. `packages/kor-travel-weather-api/src/kortravelweather_api/routers/weather.py`(1~120행, 라우트 grep)
59. `packages/kor-travel-weather-api/tests/conftest.py`, `tests/test_weather_api.py`(1~40행)
60. `packages/kor-travel-weather-dagster/pyproject.toml`
61. `packages/kor-travel-weather-dagster/README.md`
62. `packages/kor-travel-weather-dagster/src/kortravelweather_dagster/definitions.py`
63. `packages/kor-travel-weather-dagster/src/kortravelweather_dagster/resources.py`(1~60행)
64. `packages/kor-travel-weather-dagster/src/kortravelweather_dagster/tests_placeholder.py`, `tests/conftest.py`
65. `packages/python-airkorea-api/pyproject.toml`, `README.md`(1~40행), `CHANGELOG.md`(1~20행), `docs/` 목록

frontend
66. `packages/kor-travel-weather-admin/frontend/package.json`
67. `packages/kor-travel-weather-admin/frontend/package-lock.json`(버전 추출)
68. `packages/kor-travel-weather-admin/frontend/tsconfig.json`
69. `packages/kor-travel-weather-admin/frontend/eslint.config.mjs`
70. `packages/kor-travel-weather-admin/frontend/next.config.ts`
71. `packages/kor-travel-weather-admin/frontend/next-env.d.ts`
72. `packages/kor-travel-weather-admin/frontend/.env.example`
73. `packages/kor-travel-weather-admin/frontend/design.md`
74. `packages/kor-travel-weather-admin/frontend/middleware.ts`
75. `packages/kor-travel-weather-admin/frontend/app/layout.tsx`
76. `packages/kor-travel-weather-admin/frontend/app/globals.css`(헤더, 절 구분선, media/keyframes, 집계)
77. `packages/kor-travel-weather-admin/frontend/app/tokens.css`
78. `packages/kor-travel-weather-admin/frontend/app/page.tsx` 및 `admin/dagster`, `api-test`, `datasets`, `locations`, `login`, `settings/providers`, `sync-runs`, `weather`의 `page.tsx`(각 1~20행 + className 집계)
79. `packages/kor-travel-weather-admin/frontend/app/api/auth/login/route.ts`
80. `packages/kor-travel-weather-admin/frontend/app/api/auth/logout/route.ts`
81. `packages/kor-travel-weather-admin/frontend/app/api/weather/[...path]/route.ts`
82. `packages/kor-travel-weather-admin/frontend/app/api/dagster/graphql/route.ts`
83. `packages/kor-travel-weather-admin/frontend/components/admin-shell.tsx`
84. `packages/kor-travel-weather-admin/frontend/components/auth/LoginForm.tsx`
85. `packages/kor-travel-weather-admin/frontend/components/location-admin.tsx`(1~30행)
86. `packages/kor-travel-weather-admin/frontend/components/vworld-map-view.tsx`(1~60행)
87. `packages/kor-travel-weather-admin/frontend/components/weather-map.tsx`(1~30행, 주석 grep)
88. `packages/kor-travel-weather-admin/frontend/lib/api.ts`(1~30행, 120~150행, export grep)
89. `packages/kor-travel-weather-admin/frontend/lib/dagster.ts`(1~30행)
90. `packages/kor-travel-weather-admin/frontend/lib/session.ts`
91. `packages/kor-travel-weather-admin/frontend/lib/origin.ts`
92. `packages/kor-travel-weather-admin/frontend/lib/navigation.ts`
93. `packages/kor-travel-weather-admin/frontend/lib/vworld-style.ts`(1~30행)
94. `packages/kor-travel-weather-admin/frontend/lib/weather-clusters.ts`(1~30행)

git / 외부 대조
95. `git show --stat 6003da9`, `git show 6003da9 -- middleware.ts .env.example compose.yaml docs/architecture/admin-ui.md README.md`
96. `git show --stat 9d1a325`, `git show --stat f530531`, `git log --oneline -30`, `git branch -a`, `git remote -v`
97. `F:/dev/kor-travel-geo-fixes/kor-travel-geo-ui/lib/auth.ts`(4~26행, 상수 grep) 및 `lib/proxy.ts`(헤더 grep) — 읽기 전용 대조
98. `F:/dev/kor-travel-geo-fixes/docs/kor-travel-common-library-review.md`(§2 표, §3.5, §3.6, §7.3, §9, 근거 [W1][W2][L3])
