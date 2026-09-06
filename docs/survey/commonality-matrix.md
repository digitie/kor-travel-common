# 공통화 매트릭스 (kor-travel-common 설계 입력)

- 조사일: 2026-09-06. 기준 커밋·경로·약칭은 [README.md](README.md) §2.1을 따른다(airport `2bb1111`, WIP `99b3f98`; concierge `7945305`; docker-manager `862562d`; geo `1d9d74d`; map `c494e227`; weather `6003da9`; pinvi `9af25e5`).
- 성격: 인벤토리 7편과 횡단 10편의 사실을 한 표로 접은 **종합**이다. 새 사실은 없고, 셀마다 근거 문서 절을 적었다. 판정(●◐○×)과 신뢰도·난이도는 **후보**이며 결정이 아니다.
- 범례: **●** 동일(바이트 동일 또는 props/계약 동일, 색 토큰·import 경로 차이만) · **◐** 유사(같은 목적·같은 계보이나 계약 일부 상이) · **○** 상이(엔진·계약·설계가 다름) · **×** 없음. 열이 앱에 해당하지 않으면 **—**.
- 근거 열의 `inv/<app> §n`은 `inventory/<app>.md`, `vm §n`은 `cross/version-matrix.md`, `dt`는 `cross/design-tokens.md`, `ui`는 `cross/ui-components.md`, `ux`는 `cross/ux-patterns.md`, `be`는 `cross/backend.md`, `oa`는 `cross/openapi.md`, `ci`는 `cross/ci-deploy.md`, `dc`는 `cross/docs-conventions.md`, `cv`는 `cross/canview-structure-checklist.md`, `lic`는 `cross/licensing.md`를 뜻한다.

## 1. 영역 × 앱 매트릭스

### 1.1 판정 기준(원형)

- UI 행은 **map admin**(`packages/kor-travel-map-admin/frontend`)을 원형으로 놓고 판정했다. 근거: weather·geo·concierge·pinvi admin·docker-manager가 각자 "map admin의 Rail-Workbench 구조·컴포넌트 계약을 따르되 색상톤은 유지"를 문서로 선언했고(`dt` §3.3, `ux` §1.13), pinvi admin 28 primitive는 map 소스 복사본이다(`ui` §2.1). 따라서 map 열은 정의상 ●이며, 다른 열의 ●/◐는 map 대비다.
- 백엔드 행은 `be` §2.19의 "동일/유사 구현 수"를 기준으로, 다수 패턴에 속하면 ◐, 그 패턴의 원형(주로 map·geo)이면 ●, 설계가 다르면 ○으로 적었다.
- 규약·CI·버전 행은 각 횡단 문서가 제안한 공통 초안(`dc` §3, `ci` §2·§3, `vm` §5.1 후보 A, `oa` §3, `ux` §2~§3)과의 거리다.
- pinvi-user-web·pinvi-mobile 열은 admin 원형과 계보가 다르므로 대부분 ○/×이며, 사용자 표면 규칙은 별도 장(`ux` §3.1)으로 다룬다.

### 1.2 UI 토큰·프리미티브·컴포넌트군

| 영역 | airport(main / WIP) | concierge | docker-manager | geo | map | weather | pinvi-admin | pinvi-user-web | pinvi-mobile | 근거 |
|---|---|---|---|---|---|---|---|---|---|---|
| UI 토큰(의미 역할·형태) | ○ 자체 어휘 `--color-*`, 16/10px, alpha line / WIP는 shadcn 변수를 `--color-*`에 브릿지 | ◐ `--ktc-*` 3단 매핑, 6/8·36/30, hex | ◐ `@theme` OKLCH 20색, 6/8, z 7단 | ◐ 3층 alias(`--color-*`→의미→`--ui-*`), 6/8·36/30, 7단 | ● 원형(`globals.css` `:root/.dark`+`@theme inline`) | ● map 값 복사(hue만 navy), 순수 CSS | ◐ `--color-admin-*`, 6/8·36/30·7단, hex | ○ Airbnb preset(8/14/20/32, 44px, hex) | ○ 같은 v3 preset + TS 상수 | `dt` §3.1.1~3.1.4, §3.2, §3.3; `inv/kor-travel-airport` §3.1·§3.2 |
| 프리미티브 엔진 | × / WIP `@base-ui/react` 1.8 `base-nova` | ● `@base-ui/react` 1.5 `base-nova` | × (`ops-*` CSS) | ○ `radix-ui` 1.6 `radix-nova` | ● `@base-ui/react` 1.6 `base-nova`, CLI 미사용 | × | ◐ `@base-ui/react` 1.8 overlay 4종만 | ○ 자체 `useModalDialog` | × RN | `ui` §2.3, §5.1, §6.1; `vm` §1.3 |
| 버튼 | ○ native+CSS / WIP shadcn 기본 레시피(`loading` 없음, `disabled:opacity-50`) | ◐ map 구조 동일(`destructive`에 `aria-expanded:` 누락만) | ○ `ops-button` CSS | ○ radix `Slot`+`forwardRef`, `loading` 없음, `asChild` 12곳 | ● `loading`=`aria-disabled`+`aria-busy`, `render` prop | ○ `.button.primary` CSS | ○ native+`forwardRef`, `type='button'` 명시, loading 계약은 map과 동일, `render` 없음 | ○ native 44px, `disabled={disabled\|\|loading}` | ○ RN `Button` | `ui` §3.1; `ux` §1.5 |
| 입력(Input/Textarea/NativeSelect) | ○ native+CSS | ◐ base-ui `Input`; `select.tsx` 331에 base-ui Select 동봉 | ○ `ops-input` | ◐ native, `size` variant, `forwardRef` | ● | ○ `.field` CSS | ◐ native로 재작성, 클래스 동일 계열 | ○ `forms/FormField` 44px/16px | ○ `Field` in `ui.tsx` | `ui` §2.1, §4.1 |
| 필드(Field/FormField) | × | ◐ `field.tsx` 241(`FieldMessage` 없음) + rhf/zod | ○ `ops-field` + `aria-live` | ◐ `field.tsx` 224 + rhf/zod | ● `field.tsx` 265 + `form-field-*` + `form-validation.ts` | × | ◐ `field.tsx` 272 + `form-field-*` 이식 | ○ 슬롯 규칙(메시지 1슬롯 예약)은 동일 | ○ | `ui` §2.1; `ux` §1.4, G3.3 |
| 다이얼로그(Dialog/AlertDialog/Popover/Tooltip) | × | ◐ base-ui, Root/Trigger/Close 재수출 | ○ 자체 `ops-modal`, ESC·초기 포커스 자체 처리 | ○ radix `Portal/Overlay/Content`, `use-modal-a11y` | ● base-ui `Popup/Backdrop/Viewport` | × | ◐ base-ui + `hasUnsavedInput`·`viewportProps`·`data-pv-surface` | ○ `createPortal`+`useModalDialog`(inert·trap) | × | `ui` §3.4; `ux` §1.5 G4.8 |
| 배지(Badge) | ○ `.tone-*` CSS | ◐ `useRender`, 10 variant 동일 | ○ `.ops-status-badge` | ○ `tone` 축(neutral/brand/ok/warn/error/info) | ● | ○ `.status.on/off/warn` | ◐ 순수 `<span>`, variant 동일 | × | ○ 중립 1종 | `ui` §2.1, §3.4, §4.1 |
| 상태 배지(StatusBadge+`statusLabel`) | ○ 도메인 5단계(`full/critical/…`) | ○ `display-labels.ts` 함수, variant 이름은 map과 동일 | ○ `getStatusConfig`, tone `ok/warn/danger` | ○ `severityClass` 3-tone(CANCELLED→warn) | ● `status-label.ts` 5-tone, 라벨 유일성 테스트 | × raw 문자열 | ● 값 무변경 이식 + 잠금 테스트 | × | ○ 화면 로컬 `STATUS_LABELS` | `ux` §1.6, §4 C9; `ui` §2.2 |
| 데이터 테이블 | ○ `<table>`+모바일 카드 | ○ shadcn `Table`+도메인 `CandidateTable` | ○ `<table>` 원장 | ○ `VirtualTable`(클라이언트 정렬·검색, grid 기본) | ● `data-table.tsx` 799(`manualSorting=true`, 선택·가상화·4상태) | ○ `<table>`/카드 | ◐ 이식 853 + `AdminTable` 어댑터(`manualSorting=false`, `mobileCard`, testid 계약) | × | × | `ui` §3.2, §3.3; `ux` §1.3, §4 C10 |
| 필터바 | ○ select control band | ○ URL 상태 + 검색 패널(공용 파일 없음) | × | ○ `Panel` 내 `NativeSelect`/`Checkbox` | ● `FilterBar/FilterField/FilterActions` | ○ 검색 input | ◐ 이식 + `AdminPage.FilterBar` 위임(24 소비처) | × | × | `ui` §2.2, §4.1; `ux` §1.3 |
| 페이지네이션 | × (`days`/`limit`) | ○ 도메인 내 3파일 | × (`limit`만) | × | ● `OffsetPager/CursorPager` 290 | ○ offset 상태(UI 미확인) | ◐ 이식 | × | × | `ui` §2.2; `ux` §1.3 |
| 빈 상태 | ○ `notice` | ○ `panels.tsx EmptyState` | ○ `<p>` 가운데 | ○ 14줄 `<p>` | ● 좌정렬·제목+이유+행동, `framed`/`size` | ○ `.empty` | ◐ 이식 | ○ `FullPageMessage` 좌정렬 | ○ 가운데 | `ui` §2.2; `ux` §1.5 G4.4, C11 |
| 섹션 카드 | ○ `.metric-card` | ● `SectionCard` props 완전 동일 | ○ `ops-*` 패널 | ◐ `Panel`(title:string, e2e 셀렉터 계약) | ● | ○ `.panel` | ◐ 이식 + `AdminPage.Section` 위임 | ○ `SettingsSurface` | ○ `Card` | `ui` §2.2, §4.1; `ux` G3.1 |
| 스탯 스트립 | ○ `detail-ribbon` | ◐ loading/testId 없음, tone 로컬 타입 | ◐ props 거의 동일(`help` 없음, `title` 있음), CSS 기반, tone `ok/warn/danger` | ○ `MetricTile` | ● | ○ `.summary-card`/`.metric-tile` | ◐ 이식 | × | × | `ui` §2.2, §4.1; `inv/kor-travel-docker-manager` §3.1 |
| 복사(CopyButton) | × | ○ outline `Button`+텍스트 라벨 | ○ `CopyableCommand`(CLI 명령) | ○ `JsonBlock` 내 복사 | ● 아이콘 스왑 + sonner 폴백 | × | ◐ sonner 제거→inline 상태(피드백 채널 상이) | × | × | `ui` §2.2, §4.2; `ux` §1.9 |
| JSON 뷰어 | × | × (`<pre>`) | ○ raw `<pre>` | ○ `JsonBlock`(`pre.json-box` e2e 계약) + `JsonDetails` | ● | × | ◐ 이식 | × | × | `ui` §2.2; `ux` §1.9 |
| admin shell | × 셸 없음(단일 대시보드) | ◐ `AppShell` 360, map 이식, 16rem/4rem, strip | ◐ `AppShell` 259, 동일 `data-slot` 이름, CSS 클래스, strip | ○ drawer(`inert`·trap), 347 | ● `admin-shell.tsx` 510(nav 정본·접힘·breadcrumb) | ○ rail 17rem, 접힘 없음, 평면 nav, 순수 CSS | ◐ `admin-shell-parts`만 이식(skip link·헤더·rail 그리드), nav는 `layout.tsx`, 접힘 5rem | ○ 하단 탭바 `AppShell` | ○ Stack 헤더 | `ux` §1.1, §1.2, §4 C1~C4; `ui` §2.2, §4.3 |
| 로그인 폼 | × 무인증(ADR-003) | ◐ map 형태(`Field/Input`, `useSearchParams`) | ○ `LoginScreen`(`ops-auth-*`, `onLogin` 콜백) | ○ 아이콘 타일 카드, 순수 CSS | ● 타이포 워드마크, 상시 live region | ○ geo 동일 마크업, `sanitizeLocalPath` | ○ `/admin/login` 페이지 + zod `validateForm` | ○ `(auth)/login` | ○ | `ui` §3.4; `ux` §1.8, §4 C15 |
| 확인 다이얼로그 | ○ `window.confirm` | ○ `ConfirmActionButton`(기본 라벨 "삭제") | ○ `window.confirm`(영향 대상 수 명시) | ○ `ConfirmActionDialog`+`TypedConfirmField`+`RoleRequirementNote` | ● `useConfirm` Provider(generic 라벨 거부; `window.confirm` 잔존 2) | ○ `window.confirm` | × 이식 없음 | ○ 제어형 `ConfirmDialog`(기본 라벨 '확인') | ○ `lib/confirm.ts` | `ui` §2.2, §3.4, §4.3; `ux` §1.5, §4 C7 |
| 도움말(HelpTip) | × | ◐ popover-only, 20px | × | ◐ popover-only(radix), 20px | ● tooltip+popover, 40px 히트 | × | ◐ 이식 | × | × | `ux` §1.9, §4 C17; `ui` §4.1 |
| 지도 뷰 | × | ○ `maplibre-gl` **6.0** 직접 + WMTS URL | × | ○ `maplibre-vworld-react` tarball(유일 소비자) + `CoordinateMap` | ● `vworld-map-view.tsx` 1858 + `vworld-style.ts` 포팅, `map-marker-react` | ○ 로컬 재구현(`vworld-style.ts` 중복) | ○ `vworld-map-web` tgz `file:` | ○ 동일 tgz + `vworldPrimitives` facade | ○ `vworld-map-rn` tgz | `ux` §1.10, §4 C22; `ui` §4.3; `vm` §1.5 |

### 1.3 상태·데이터·인증

| 영역 | airport | concierge | docker-manager | geo | map | weather | pinvi-admin | pinvi-user-web | pinvi-mobile | 근거 |
|---|---|---|---|---|---|---|---|---|---|---|
| 상태·폼 라이브러리 | × `useState`만 | ○ react-query + rhf + zod 4 | ◐ react-query만(zod·rhf는 GM-19에서 제거) | ○ react-query + zustand + rhf + zod | ● react-query + zustand, rhf 없음, `form-validation.ts` | × react-query 선언만 import 0 | ◐ react-query(`AdminQueryProvider`), rhf·zustand 선언만 | ○ raw fetch + zod `validateForm` | ○ react-query + zustand(`@pinvi/state`) | `vm` §1.4; `inv/*` §3 상태/데이터 |
| API 클라이언트 생성(typegen) | × 수기 `types.ts` | × 수기 `api.ts` 1,668 | × 수기 `api.ts` 580 | ● `openapi-typescript` 7.13 + `check-sync.sh` | ● `gen:types`/`gen:types:check` + user-client 패키지 | × 수기 `lib/api.ts` | × 수기 `ApiClient` + Zod 이중 유지 | × 동일 | × 동일 | `oa` §2.11, S10; `ui` — |
| fetch 래퍼·에러 파싱 | ◐ `ApiError(detail,status)` no-store | ◐ `ApiRequestError` 3키 해석, 401→`/login` | ◐ `ApiError{code,message,requestId}` + `humanizeError` | ◐ `ApiError.detail`, 401→`/login` | ● `ApiClientError{problem,retryAfter}` + Idempotency-Key 슬롯 | ○ `detail`→`Error.message` | ◐ `ApiClient`(timeout status 0, Retry-After, 409 VERSION_CONFLICT) | ◐ 동일 패키지 | ◐ 동일 + Bearer 회전 | `oa` §5 C10; `inv/*` §3 |
| 프론트 인증 경계 | × 무인증 allowlist proxy | ● Next `proxy.ts` + HMAC 세션 + PBKDF2 + BFF 키 주입(geo #399 형태) | ○ Next 서버 코드 0, 백엔드 서명 쿠키 SameSite=strict | ● 원형(`proxy.ts`·`lib/auth.ts`·`X-KTG-*` 주입) | ● `middleware.ts` + 동일 상수 + `X-Kor-Travel-Map-*` | ◐ 세션 상수는 geo와 동일, 신원 전달은 `x-admin-token`만, 비-prod bypass | ○ 백엔드 JWT 쿠키 + 클라이언트 `AdminGuard`(404 은닉) | ○ 동일 JWT | ○ Bearer + SecureStore | `be` §2.8; `inv/kor-travel-weather` §3.1 표; `ui` §3.4 |

### 1.4 백엔드(Python)

| 영역 | airport | concierge | docker-manager | geo | map | weather | pinvi(api/etl) | 근거 |
|---|---|---|---|---|---|---|---|---|
| settings | ◐ `BaseSettings`, prefix 없음, CSV→list | ◐ prefix 없음, `case_sensitive`, 프런트 키 혼입 | ○ pydantic-settings 미사용(`os.environ`) | ◐ `KTG_`, `SecretStr`, `frozen` | ● `KOR_TRAVEL_MAP_`/`_API_`, profile fail-closed | ◐ `KOR_TRAVEL_WEATHER_`, prod 기본, 토큰 강도 검증 | ◐ `pinvi_*` 필드, 2,500행, redacted ValidationError | `be` §2.2, C1 |
| logging | × stdlib | × stdlib + `mask_secret` | ○ stdlib + 월간 롤링 + request-id 필터(서버 발급) | ○ `structlog` 선언·`log_format` 설정만, 구현 0 | ○ `log_format` 설정만 | ◐ request-id/duration 미들웨어 | ● structlog JSON + contextvars | `be` §2.3, C2 |
| metrics | × | ◐ `ktc_` + `ProcessCollector(namespace)` | ○ 수기 렌더 `ktdm_`, client 미사용 | ◐ `ktg_`(T-305), noop 폴백, DB 훅 | ◐ `kor_travel_map_`, 자체 registry, surface 라벨 | ◐ `ktw_`, allow-list 라벨, multiproc 청소 | ◐ `pinvi_api_`, multiproc | `be` §2.4, C3 |
| health/ready | ○ `/health`가 DB count 실행 | ◐ `/health` 정적 | ◐ `/health` 정적 | ○ `/v1/healthz` + `/v1/readyz`(유일한 deep readiness) | ● `/health`+`/version`+`/v1/ops/health-deep` | ● `/health`+`/version` | ◐ `/health`+`/health/db`+도메인 2종 | `be` §2.5, C4; `oa` §2.10 |
| errors(응답 형식) | ◐ RFC7807(`code`·`request_id` 없음, 스펙 422 불일치) | ○ FastAPI `{detail}` | ○ `{detail}`+계약 오류 3종 `{detail{code,…},request_id}` | ○ 경로별 3종(VWorld/v2/legacy), 검증 400 | ● `ProblemDetail{type,title,status,detail,code,request_id,errors}` | ● `Problem` 동형(코드 2종만) | ○ `{error:{code,message,details}}` | `oa` §2.5, §4; `be` §2.10, C5 |
| pagination | × | ○ keyset cursor + fingerprint, `{items,next_cursor,has_more,total,newest_id,newer_than}` | × `limit` | ○ 3형(page/size, limit, cursor) | ● `page_size`+HMAC cursor, `meta.page{page_size,next_cursor,total?}` | ◐ `limit/offset`, `meta.page{limit,offset,returned,total}` | ○ `limit`+cursor, `meta{cursor,has_more}`; admin page/limit | `oa` §2.6, S2; `be` C6 |
| auth(백엔드) | × | ◐ 공개키 함수 동일 + `X-KTC-*` proxy 신뢰 + scope | ◐ 공개키 동일 + pbkdf2 서명 쿠키 + Origin | ◐ 공개키 동일 + `x-ktg-*` + 역할 5종 | ● 공개키 동일 + ServiceToken/OpsToken/RoutePolicy 6종 | ○ `x-admin-token` 단일 정적 토큰 | ○ argon2id + JWT + RBAC(404 은닉) + rate-limit | `be` §2.8, C7·C8; `oa` §2.4 |
| db 엔진·세션 | ◐ asyncpg(+aiosqlite), 골격 동일, Alembic head 검증 | ◐ asyncpg, 전역 engine | ○ SQLite sync | ◐ psycopg async, `options` GUC | ● asyncpg, `normalize_async_dsn`, 권한 경계 검증 | ○ psycopg **sync** | ◐ asyncpg, `server_settings` 타임아웃 3종 | `be` §2.6, C9 |
| alembic | ● env.py 동형, `NNNN_slug`, CI `check` | ● env.py 동형, `YYYYMMDD_NNNN_slug` | × `create_all` | ○ sync, raw SQL, `search_path` | ○ 300 baseline 봉인(도메인 결합) | ◐ sync, `NNNN_slug`, compose `migrate` | ◐ async + advisory lock, `%Y%m%d_%H%M` | `be` §2.7, C10 |
| testing 픽스처 | ◐ sqlite 기본/PG DSN, TRUNCATE | ◐ DSN 없으면 skip | ○ SQLite mock | ◐ DSN + `_pg_guard` | ● testcontainers digest 핀, session loop | ◐ DSN TRUNCATE | ● testcontainers + `alembic upgrade head`, 4-shard | `be` §2.16, C11 |
| 품질 게이트(ruff/mypy/import-linter) | × 없음 | × 없음 | ◐ ruff(E,F,I,UP,B,ASYNC) | ● ruff+mypy strict+import-linter+pre-commit | ● + coverage 80/70/80 + `ruff format` | ◐ ruff + mypy strict(CI 미실행) | ◐ ruff(+S,RUF) + mypy strict | `be` §2.17, C20 |
| openapi export·drift | ◐ export만, CI 없음 | × | × | ● `--check` + `openapi.yml` | ● profile 3종 + `--check` + 표면 테스트 | ◐ export + `git diff --exit-code` | × (map 스펙 소비자 검증만) | `oa` §2.11, M1; `be` §2.18, C12 |

### 1.5 규약·CI·버전

| 영역 | airport | concierge | docker-manager | geo | map | weather | pinvi | 근거 |
|---|---|---|---|---|---|---|---|---|
| 문서·에이전트 규약 | ◐ 5원칙 동일, `adr/` 파일, runbooks 9, `hostile-review.md`(유일한 성문 2인 리뷰), 절대 경로 링크 | ◐ `decisions.md` 단일, T-NNN, CI 없음, worktree 암묵 | ◐ `decisions.md`, `bindings.md`(중복 선언 결박), tasks-done ID 재사용 이력 | ● map 계보(`agent-guide.md`, tasks-rule, ADR 파일) | ● 원형(tasks-rule·acceptance·archive·ledger lint·redaction) | ○ AGENTS 39줄, CLAUDE/SKILL/task 체계 없음, map 잔재 링크 | ◐ `decisions.md`, execplan, ADR>AGENTS 우선순위 | `dc` §1.1~1.9, §1.15~1.19 |
| 개발 환경 정본 | ◐ WSL2 1차, PowerShell 보조 | ● Linux/WSL 전용(ADR-23/33) | ● Linux/WSL 전용 | ● Linux-only(ADR-065) | ● Linux/WSL | ◐ 미명시(README가 WSL 경로) | ● Linux-only(ADR-051; 설정 파일은 Windows 경로) | `dc` §1.11, §2 C1 |
| CI 게이트 폭 | ○ 3~5종 + prod `live-e2e` | × CI 없음 | ○ lint/test, SHA 핀 | ◐ + openapi/typegen drift | ● 10종+, verify 스크립트 | ○ vitest·mypy 미실행 | ● aggregate gate·provenance·contract pin | `ci` §1.1~1.3, §2.2 |
| 버전 핀·lock 관행 | ◐ `uv.lock` CI만, Docker pip, TS 7 | ○ 하한만, lock 없음(`mcp<2` 사고) | ○ Poetry lock 없음, CI 정확 핀 3종 | ○ lock 없음, pre-commit 구버전 | ● exact 핀 + `verify-*.mjs` + pytest 잠금 + npm 12.0.1 | ● `uv.lock` CI·Docker `--locked` | ◐ lock 무결성 검사, `uv.lock` 미소비, override 정확 핀 | `vm` §2.1, §3.6, §7.1 |
| UX 가이드 계보(design.md) | ○ modern-minimal 독자, 영문 | ● map 구조 선언 + 보라 유지 | ◐ Ember, Rail-Workbench, `dashboard-ui.md` UX 계약 | ◐ Workbench drawer, StyleSeed 규칙 | ● 잠금 정본(금지 패턴 7종) | ◐ map 계약 선언, 코드 불일치 2건 | ◐ admin 구조만 이식 / user Airbnb 잠금 | `ux` §1.13, §2, §4; `dc` §1.20 |
| OpenAPI 규약 준수(M1~M9) | ○ export만, `/v1`, 태그 없음, 스펙-와이어 불일치 | ○ `/api/v1`, `{detail}`, 산출물 없음 | ○ `/api/v1`, `{detail}`, 산출물 없음 | ○ v1 VWorld 예외, 400, `securitySchemes` 미선언 | ● 원형 | ◐ `type about:blank`, offset, 소문자 헤더 | ○ `/` prefix, `{error}`, 정수 `If-Match`+409, 산출물 없음 | `oa` §3, §4 |
| PC/Mobile 대응 | ◐ 반응형 단일 페이지(860/560px), 320px 게이트 | ◐ PC-first, `useIsMobile` 767, 모달↔페이지 분기 | ◐ PC-first, 표만 스크롤 | ◐ PC-first + drawer | ● PC 전용(모바일 분기 없음) | ◐ 62rem/42rem, 44px 미검증 | ◐ admin `mobileCard`, 36/30px 예외 2쪽 / user mobile-first 44px 탭바 | `ux` §1.11, §3 |

## 2. 후보별 판정표

열 정의 — **배포 단위**: tokens 패키지(npm, CSS·JSON·TS·v3 preset) / ui 패키지(npm 또는 shadcn registry) / fe-core 패키지(npm, 프레임워크 무관 TS) / python 패키지(`kortravelcommon`, extras) / 규약 문서(`docs/standards/*`) / CI 템플릿(`workflow_call`) / 도구(스크립트). **신뢰도**: 사실 근거의 강도(구현 수·동일성). **난이도**: 소비 앱의 공개 계약·e2e·배포 변경 정도.

### 2.1 토큰·스타일

| 영역 | 배포 단위 | 1차 소비자 | 신뢰도 | 난이도 | 근거 | 보류/제외 사유 |
|---|---|---|---|---|---|---|
| 의미 토큰 계약(`--kt-*` 후보: surface 4·text 4·icon·border/control-line·brand 4·focus·status 4+tint·overlay·radius 2·control 2·rail·duration 2·ease 2·shadow 2·z 5) + `tokens.css`(map 기본값, `.dark` 완비) | tokens 패키지 | map·weather·geo·concierge·pinvi-admin·ktdm(admin 프로필) | 높음 | 중 | `dt` §3.3, §3.6.1~3.6.2; 6개 admin이 역할명 수렴 | 접두(`--kt-` vs `--ktc-`)·`--input`/`--accent` 의미 고정 결정 필요(§4.2) |
| `theme.css`(`@theme inline` 매핑 + `@utility duration-*`) | tokens 패키지 | Tailwind v4 앱 5개 + airport WIP | 높음 | 중 | `dt` §3.6.3; map·geo·pinvi admin이 이미 같은 형태 | `@config` 잔존 앱(geo·concierge·pinvi)은 config의 동일 utility 이름 제거 선행; `@config`/`@theme` 우선순위 미확인 |
| `shadcn.css`(shadcn alias → `--kt-*`) | tokens 패키지 | map·geo·concierge·pinvi-admin·airport WIP | 높음 | 낮 | `dt` §3.2.3 | `--input`(경계 vs 배경)·`--accent` 의미 통일 선행 |
| `base.css`(focus 단일 레시피, hairline 2종, reduced-motion+스피너 예외, `button cursor`) | tokens 패키지(선택) | 전 admin | 높음 | 낮 | `dt` §3.4.1; `ux` G9.1·G9.3; map·pinvi·concierge 규칙 일치 | geo의 `outline-color: color-mix` 반투명 기본과 충돌 → geo 정렬 필요 |
| `tokens.json`(DTCG)·`tokens.ts`·`tailwind-preset.cjs`(v3) | tokens 패키지 | pinvi mobile(NativeWind 4), pinvi `@pinvi/design-tokens` 재수출 | 중 | 중 | `dt` §3.6.3; pinvi DESIGN.md·ktdm DESIGN.md가 DTCG 병기 | 값 정본이 CSS인지 JSON인지 결정; consumer 프로필(44px·8/14/20/32)은 pinvi 소유 |
| 밀도 프로필 2종(`admin` 6/8·36/30·15px·7단 / `consumer` 8/14/20/32·44px·16px) + 표면 스코프 기법(`[data-*-surface]`) | 규약 문서 + tokens | 전 앱 | 높음 | 낮 | `dt` §3.6.5; pinvi `[data-pv-surface='admin']` 선례 | 타입 스케일은 `@theme`(비inline)이어야 변수 가리기가 동작 |
| 브랜드 오버라이드 허용 목록(brand 4·focus·paper 4·ink 4; status 기본값 유지 권장) | 규약 문서 | 전 앱 | 높음 | 낮 | `dt` §3.6.4, §3.3 | — |
| 대비 계산기 `kt-contrast`(3:1 컨트롤 경계·4.5:1 본문, light/dark 동일 쌍) | 도구(CI) | geo·concierge·ktdm·airport(현재 미달) | 높음 | 중 | `dt` §3.4.2; map만 수치 검증 | 미달 앱은 값 재조정이 선행(계약 위반 상태로 도입되면 CI red) |
| 다크 모드 슬롯(`.dark` 값 필수, 활성화는 `dark-class.css`/`dark-media.css` 앱 선택) | tokens 패키지 + 규약 | map·weather·concierge(값 보유), airport(media) | 중 | 낮 | `dt` §3.2.2, §3.6.6 | 토글 없는 앱의 검증 의무 수준 결정(§4.2) |
| 마커 팔레트 P-01..P-16 | **제외**(규칙만) | map·pinvi | — | — | `dt` §3.5 | 같은 코드에 다른 hex 두 벌; 정본은 `marker_color` 소유자(map)가 확정해야 함 |
| 폰트 스택 문자열(`--kt-font-sans` Pretendard 우선) | tokens 패키지; 로딩은 앱 | 전 앱 | 중 | 낮 | `dt` §3.1.4, §4; `ux` C12 | 로딩 방식(npm pretendard vs next/font vs 미로드)은 앱 결정 |

### 2.2 UI 컴포넌트

| 영역 | 배포 단위 | 1차 소비자 | 신뢰도 | 난이도 | 근거 | 보류/제외 사유 |
|---|---|---|---|---|---|---|
| `badge-variants` + `Badge` | ui 패키지 | map·pinvi-admin·concierge(소비 8/2/17) | 높음 | 낮 | `ui` §4.1; 10 variant 동일 | `render` prop 채택 여부; geo `tone`→`variant` 매핑 |
| `Skeleton`·`Separator`(native `role=separator`)·`Card` 7종·`Alert` | ui 패키지 | map·geo·concierge·pinvi-admin | 높음 | 낮 | `ui` §4.1 | `AlertActions` 유무 합의 |
| `Input`·`Textarea`·`NativeSelect(+Option)` (native 우선) | ui 패키지 | map·pinvi-admin·geo·concierge | 높음 | 낮 | `ui` §4.1, §5.4 | React 18 소비자용 `forwardRef` 유지 여부 |
| `Field`(+variants, `FieldMessage`) | ui 패키지 | map·pinvi-admin·geo·concierge | 높음 | 낮 | `ui` §4.1 | — |
| `EmptyState`·`SectionCard`·`FilterBar/FilterField/FilterActions`·`StatStrip` | ui 패키지 | map·pinvi-admin·concierge(SectionCard props 동일)·ktdm(StatStrip) | 높음 | 낮 | `ui` §4.1, §2.2; `ux` G2.1·G3.1·G4.4 | StatStrip tone은 `StatusTone` 5종으로 통일(ktdm `ok/warn/danger` alias) |
| `HelpTip`(tooltip+popover, 40px 히트) | ui 패키지(1차 후반) | map·pinvi-admin·geo·concierge | 높음 | 낮 | `ui` §4.1; `ux` G8.1 | overlay 엔진 결정에 종속 |
| `button-variants`(레시피) | ui 패키지 | map·geo·concierge | 높음 | 낮 | `ui` §4.1 | 토큰 별칭 계층(`ui` §6.3) 선행 |
| `AppErrorPanel` + `error-recovery`(chunk/RSC 1회 reload) | ui 패키지 | map·geo·concierge·ktdm·pinvi(5앱 동일 계보), weather·airport 신규 | 높음 | 낮 | `ui` §3.4, §4.1; `ux` G4.3, C19 | `Alert`/`Button` 이후 |
| `Button`(`type='button'` 기본, `loading`=aria-disabled+포커스 유지, `disabledReason`) | ui 패키지(2차) | map·concierge·pinvi-admin | 중 | 중 | `ui` §3.1, §4.2 | 세 계열(map/pinvi native/airport shadcn 기본) 합의; geo `asChild` 17곳; pinvi user 계약은 별도 |
| overlay 세트(`Dialog`·`AlertDialog`·`Popover`·`Tooltip`·`Tabs`·`Breadcrumb`, base-ui) | ui 패키지(2차) | map·concierge·pinvi-admin·airport WIP | 중 | 중~높 | `ui` §3.4, §4.2, §5.2 | 엔진 결정(§4.2); geo 12파일 재작성 + `asChild`→`render`; pinvi 확장(`hasUnsavedInput`, testid) 흡수 여부 |
| `Table` primitive(엔진 무관 선택 열 셀렉터 `data-slot=checkbox`, `stickyHeader`, `containerTestId`) | ui 패키지(2차) | map·pinvi-admin·concierge | 중 | 중 | `ui` §3.2 | pinvi 확장 4종 흡수 |
| `DataTable`(TanStack v8, `manualSorting` 2모드, 선택, 가상화 ARIA, 4상태) | ui 패키지(2차) | map·pinvi-admin | 중 | 높 | `ui` §3.3, §4.2; `ux` C10 | pinvi testid·sr-only 계약, geo `VirtualTable` 검색·`rowHeader` 흡수 여부; react-table 9.x 미검토 |
| `OffsetPager/CursorPager` | ui 패키지(2차) | map·pinvi-admin | 중 | 낮 | `ui` §4.2; `ux` G2.4 | 타 앱 수요 미확인 |
| `CopyButton`·`JsonViewer`·`DetailList`(피드백 채널 prop 주입) | ui 패키지(2차) | map·pinvi-admin·geo | 중 | 중 | `ui` §4.2, §7-5; `ux` G8.2·G8.3 | 토스트 정책 결정 |
| `StatusBadge` 계열(tone 테이블·`statusLabel` 사전 주입형) | ui 패키지(2차) | map·pinvi-admin | 중 | 중 | `ui` §4.2; `ux` G5.1~G5.4 | 사전은 앱 소유; geo CANCELLED 의미 확인 |
| `AdminPageHeader`/`AdminSkipLink`/`AdminRailGrid`(셸 골격만) | ui 패키지(2차) | pinvi-admin(이미 분리)·geo `PageHeader`·weather·ktdm | 중 | 중 | `ui` §4.2; `ux` G1.3·G1.5·G1.8 | nav·로그아웃·접힘·RBAC는 앱 소유 |
| `FormFieldInput/FormSelect/FormTextArea` + `form-validation.ts` | ui 패키지(2차) | map·pinvi-admin | 중 | 낮 | `ui` §4.2; `ux` G3.3·G3.4 | rhf/zod 앱(concierge·geo)과 공존 설계(헤드리스) |
| 토스트 어댑터 | 규약 문서 우선 | — | 낮 | — | `ui` §3.4, §7-5; `ux` C8 | 엔진 4종·없음 2앱; 정책(G4.1)만 통일 |
| `AdminShell` nav/로그아웃/접힘/RBAC, `LoginForm/LoginScreen`, `ConfirmDialog` API, `SelectableRow`·`EntityLink`·`MultiFilterCombobox`·`feature-*` 패널, `vworld-map-view` 계열, pinvi 사용자 UI(`ui/Button`·`Dialog`·`ConfirmDialog`), pinvi `AdminTable` 어댑터, weather·airport main·ktdm 순수 CSS 컴포넌트 | **보류/제외** | — | — | — | `ui` §4.3 | 신뢰 경계·도메인·지도 라이브러리 중복 금지·v4 전환 선행(§4.1·§4.2) |
| 배포 방식(A 자체 shadcn registry / B npm 패키지 / C 소스 복사 유지) | 결정 | — | — | — | `ui` §6.2 | 어느 쪽이든 토큰 별칭 계층 선행; DataTable류는 B 유리(추정) |

### 2.3 프론트 데이터·클라이언트·규칙

| 영역 | 배포 단위 | 1차 소비자 | 신뢰도 | 난이도 | 근거 | 보류/제외 사유 |
|---|---|---|---|---|---|---|
| `@kor-travel/api-client-core`(problem+json 파싱→`ApiError{code,status,requestId,details,retryAfterSeconds}`, `Retry-After`, timeout status 0, Idempotency-Key 슬롯) | fe-core 패키지 | map·pinvi·geo·airport(각자 `ApiError` 보유) | 중 | 중 | `oa` §5 C10; 선행 §5 "query key·인증·재시도는 앱" 유지 | 앱별 `ApiError` 형태가 달라 어댑터 단계 필요 |
| `@kor-travel/openapi-typegen`(openapi-typescript 7.x 고정 래퍼, `gen`/`check`, schema 이름 목록) | fe-core 패키지 + CI | geo·map(기존), weather·airport·concierge·ktdm(수기→생성) | 높음 | 중 | `oa` §2.11, S10, C9 | pinvi는 Zod 이중 유지 정책과 관계 결정(Q5) |
| BFF proxy 골격(헤더 allowlist, `X-<App>-Actor`/`-Admin-Proxy-Secret` 주입, 499, problem+json 변환, `Idempotency-Key`/`If-Match` 전달) | 규약 문서(+ 선택 헬퍼) | map·geo·concierge·airport(allowlist 원형)·weather | 높음 | 중 | `inv/kor-travel-map` §8-13, `inv/kor-travel-airport` §8-7, `inv/kor-travel-geo` §8-19 | 세션 저장·역할 판정은 앱 소유(선행 §3.6, geo 2026-09-04 취소 사례) |
| 세션 서명/PBKDF2/rate-limit 순수 함수(8h·310k·5회/10분·HMAC v1) | 규약 문서(코드 공유는 보류) | geo·map·concierge·weather(상수 일치), ktdm(유사) | 중 | 높 | `inv/kor-travel-weather` §3.1 표·§8-2; `inv/kor-travel-geo` §8-20 | revocation 저장소·신원 전달이 앱마다 달라 파라미터화 후에도 신뢰 경계 |
| `useModalA11y`/모달 행동 계약(포커스 이동·trap·Escape·복원·scroll lock·"두 스택 금지") | 규약 문서(+ 훅 후보) | geo·pinvi-user·ktdm | 중 | 낮 | `ux` G4.8, C18; `inv/kor-travel-geo` §8-9 | 엔진 무관 계약만; 구현은 후속 |
| PC/Mobile 분기 훅(`useMobileWebLayout` 뷰포트+포인터, `useIsMobile` 767) | fe-core 패키지(선택) | pinvi-user·concierge | 중 | 낮 | `ux` §3.1·§3.4; `inv/pinvi` §8-23 | breakpoint 값 합의(§4.2) |
| 접근성·모션 CSS 조각(focus/reduced-motion/skip-link/overflow-x clip) | tokens `base.css` | 전 앱 | 높음 | 낮 | `ux` G9; `inv/*` §8 | 위 §2.1 `base.css`와 동일 항목 |

### 2.4 Python 패키지(`kortravelcommon`, extras: core/api/db/dagster/testing/http)

| 영역 | 배포 단위 | 1차 소비자 | 신뢰도 | 난이도 | 근거 | 보류/제외 사유 |
|---|---|---|---|---|---|---|
| C4 `health`(`/health` liveness·`/readyz` deep(geo 알고리즘)·`/version`) | python `[api]` | 7곳 전부 | 높음 | 낮 | `be` C4; `oa` M5·C6 | geo `/v1/healthz` 경로 이동은 probe·Prometheus 설정 동반(별칭 병행) |
| C12 `openapi` export CLI(`--check`, profile 콜백, 결정적 직렬화) | python `[api]` + CI | airport·geo·map·weather(교체), concierge·ktdm·pinvi(신규) | 높음 | 낮 | `be` C12; `oa` M1·M9·C7 | — |
| C13 `time`(`KST=ZoneInfo`, `kst_now/utc_now`, aware 검증) | python `[core]` | airport·map·weather·pinvi | 높음 | 낮 | `be` C13, §2.12 | ktdm naive UTC·weather 고정 오프셋 전환은 명시 결정 |
| C20 `quality`(ruff 베이스 `line-length=100`, `E,F,I,UP,B,ASYNC`; mypy strict; import-linter·pre-commit·CI 템플릿) | 규약 산출물(`[tool.ruff] extend`) | ruff 5곳·mypy 4곳; airport·concierge 신규 | 높음 | 낮~중 | `be` §2.17, C20 | airport·concierge는 0에서 도입(위반 대량 가능); ktdm `ruff format` 전체 금지 |
| C1 `settings` 베이스(`.env` 튜플·`extra=ignore`·SecretStr 마스킹·싱글턴) | python `[core]` | 6곳(ktdm 신규) | 높음 | 중 | `be` C1 | env 이름·접두는 절대 불변(배포 계약) |
| C9 `db`(`normalize_dsn`, `make_async_engine` asyncpg/psycopg 흡수, session factory, `get_db`, 메트릭 훅) | python `[db]` | airport·concierge·map·pinvi·geo | 높음 | 중 | `be` C9 | weather sync는 별도 함수 |
| C7 `auth.public_api_key`(생성/해시/매칭 4곳 동일 + 추출 + TTL 캐시 + 저장소 Protocol) | python `[api]` | concierge·ktdm·geo·map | 높음 | 중 | `be` §2.8, C7; `oa` C5(d) | 저장 스키마는 앱 소유 |
| C3 `metrics`(접두 정책 `<svc>_`, 표준 HTTP 3지표·라벨·미매칭 센티널·multiproc·DB pool) | python `[api]` | concierge·geo·map·weather·pinvi | 높음 | 중~높 | `be` §2.4, C3 | 접두 규약 결정(map·pinvi 이름 변경 → 대시보드 회귀) |
| C2 `logging`(structlog JSON + request-id 미들웨어 `trust_incoming` 옵션 + `mask_secret`) | python `[api]` | pinvi(구현)·geo·map(설정만)·weather·ktdm | 중 | 중 | `be` C2; `oa` M4·C2 | 요청 ID 발급 정책(§4.2) |
| C5 `errors`(예외 베이스 `code/http_status/hint` + RFC7807 `ProblemDetail` 핸들러 + OpenAPI 주입) | python `[api]` | map·weather(교체), airport(additive), geo v2/admin(opt-in) | 중 | 높 | `be` C5; `oa` M3·N1·C1 | pinvi `{error:{}}`·concierge/ktdm `{detail}`·geo v1은 breaking → v2 시점 |
| C8 `auth.trusted_proxy`(CIDR + 비밀 상수시간 비교 + actor/roles 파싱; 헤더 이름 인자) | python `[api]` | concierge·ktdm·geo·map | 중~높 | 중 | `be` C8; `oa` C5(b) | 헤더 접두 통일은 별도 정책 |
| C11 `testing`(testcontainers PostGIS 픽스처 + 외부 DSN 가드 + TRUNCATE + loop-scope 가이드) | python `[testing]` | map·pinvi / geo·concierge·weather·airport | 중 | 중 | `be` §2.16, C11 | 두 계열 모두 지원해야 채택 |
| C10 `alembic` 템플릿(async env.py 골격·NullPool·advisory lock·`alembic check` CI) | 템플릿(cookiecutter류) | airport·concierge·weather·pinvi | 중 | 낮~중 | `be` §2.7, C10 | geo·map은 도메인 가드로 제외 |
| C15 `http`(AsyncClient 팩토리·tenacity 재시도 정책·이벤트 훅) | python `[http]` | geo·pinvi·weather·concierge·map | 중 | 중 | `be` §2.11, C15 | — |
| C16 `security_headers`(HSTS 조건 옵션), C17 `cors`(csv 파서) | python `[api]` | airport·pinvi / concierge·ktdm·airport | 중 | 낮 | `be` §2.9, C16·C17 | HSTS 전달 헤더 신뢰 정책 결정 |
| C18 `dagster`(3단 리소스 폴백·실패 통지 어댑터·`dagster.yaml` 템플릿) | python `[dagster]` | geo·map·pinvi·weather | 중 | 중 | `be` §2.14, C18 | op/job vs asset 무관 |
| C3'·C4' 페이지네이션 코덱(`page_size`+cursor HMAC+fingerprint, offset 변형), envelope `Meta/PageMeta/Envelope[T]` | python `[api]` | map(교체), 신규 표면 | 낮~중 | 높 | `be` C6; `oa` S1·S2·C3·C4 | 이름 충돌(`limit`/`page_size`, `has_more`/`next_cursor`) 합의 |
| C19 `cli.mutex`(PG advisory lock + skip exit 3), C21 백업 산출물 규약(파일명·sha256·manifest) | python `[core]` / 규약 문서 | geo·map / ktdm·airport·pinvi·geo | 약~중 | 낮 | `be` C19·C21 | typer 공통화 근거 없음(geo만) |
| C14 `geo_primitives`(`Point`, `normalize_crs`만) | python `[core]` | geo·map·pinvi | 낮 | 중 | `be` C14, §4 | 한국 좌표 경계 상수는 3값이 달라 **공통 상수 금지** |
| 도메인 결합 부분(geo loaders/GeoIP/VWorld 형식, map RoutePolicy·ServiceToken·300 baseline, pinvi JWT/RBAC/M05, ktdm compose/pin registry, ktc LLM/APScheduler/MCP, ktw provider, kta 스케줄러), 서비스 간 클라이언트, 비밀번호/세션/CSRF, 기존 공유 라이브러리 재래핑 | **제외** | — | — | — | `be` §4; 선행 §7.2·ADR-006 | — |
| 배포 방식(A `git+https@<sha>`+태그 / B path / C 사내 index / D wheel URL) | 결정 | — | — | — | `be` §5.2 | A 기본 후보; geo·map·ktdm·concierge는 lock 도입 선행 |

### 2.5 규약 문서(`docs/standards/*` 후보)

| 영역 | 배포 단위 | 1차 소비자 | 신뢰도 | 난이도 | 근거 | 보류/제외 사유 |
|---|---|---|---|---|---|---|
| 색상 톤 규칙(역할·대비·hairline 2종·불투명 tint·alpha 정책·raw 색 금지·오버라이드 허용 목록·다크 슬롯) | 규약 문서 | 전 admin | 높음 | 낮 | `dt` §3.3, §3.4.1, §3.6.4 | 값은 앱 소유 |
| UX 가이드 G0~G9(셸·목록·상세·피드백·상태 5-tone·위험 작업·로그인·도움말·접근성·모션·타이포) | 규약 문서 | 전 admin(사용자 표면은 별도 장) | 높음 | 낮 | `ux` §2 | 충돌 C1~C22 결정(§4.2) |
| PC/Mobile Web 규약(표면 분류·breakpoint sm/md/lg/xl·검사 폭 320/375/414/768/1024/1440·터치 36/30 vs 44 vs 48·안전영역·overflow-x clip·light 기본) | 규약 문서 | 전 앱 | 높음 | 낮 | `ux` §3 | weather 62/42rem·airport 860은 재조정 대상 |
| 금지 패턴 grep 게이트 7종(map) + Hallmark 클래스 ESLint 가드(pinvi) | 도구 + 규약 | map(스크립트 부재)·pinvi | 중 | 낮 | `ux` G0.3; `inv/kor-travel-map` §8-5; `inv/pinvi` §8-7 | map 스크립트 소재 미확인 |
| OpenAPI·REST 규약 MUST M1~M9 / SHOULD S1~S13 / MUST NOT N1~N8 + 헤더 이름 레지스트리 | 규약 문서 | 7개 백엔드 | 높음 | 앱별 낮~높 | `oa` §3, §4, C11 | geo v1·pinvi envelope는 문서화된 예외 |
| 포트 대역 규칙(ktdm `docs/ports.md` 인용, 슬롯 명문화, sibling 140xx/141xx 등록, common 130xx) | 규약 문서(정본은 ktdm) | 전 앱 | 높음 | 낮 | `ci` §3.1 | 정본 이원화 금지; airport 14002 예외 결정 |
| 서비스명·컨테이너명·이미지·볼륨·네트워크·env 접두·약칭 표준 | 규약 문서 | 전 앱 | 중 | 중 | `ci` §3.2 | 이름 변경은 앱 스크립트 동반 |
| Dockerfile·compose 최소 규약(멀티스테이지·non-root·HEALTHCHECK 1곳·digest 병기·OCI revision·`.gitattributes`) | 규약 문서 | 전 앱(현재 non-root 4/18) | 중 | 중 | `ci` §1.6, §3.3 | ktdm은 컨테이너 아님(예외) |
| AGENTS.md 공통 절 A~I(5원칙·Ruthless Review·언어·우선순위·읽기 정책·절대 금지 5·완료와 push·기록 갱신·환경 진입점) | 규약 문서(배포 절) | 7개 저장소 | 높음 | 낮 | `dc` §3.1; 5원칙은 6곳 글자 단위 동일 | geo 추가 불릿·pinvi ADR 우선순위·SKILL 라우터화 결정 |
| `docs/` 트리 표준·`tasks-rule` 공통 규약·archive 규약(map §8)·ADR 파일 형식·journal/resume 형식·CHANGELOG | 규약 문서 | 7개 저장소 | 높음 | 중 | `dc` §3.2, §3.3; `cv` §3 | 원장 형식(체크박스 vs 5열 표) 미결 |
| review gate 공통 규약(2인 독립·immutable 기준선·P0~P3·disposition 4종·full/light) | 규약 문서 + TEMPLATE | 7개 저장소(kta만 성문, 나머지 관행) | 높음 | 중 | `dc` §1.5, §3.4; `cv` §3.3 | full/light 판정 주체 |
| 라이선스·출처 규약(`NOTICE`·`THIRD_PARTY_NOTICES`·`PROVENANCE`·`LICENSES/`·SPDX 헤더·패키지 메타데이터) | 규약 문서 + 린트 | common 자체 + 이식 파일 전부 | 높음 | 낮 | `lic` §3.3~3.5, L1~L5 | — |
| 버전 일치 정책(P3 계층별 하이브리드 + P4 renovate preset) + `version-registry.v1` JSON 형식 + `verify` 스크립트 | 규약 문서 + 도구 | 7개 저장소 | 높음 | 중 | `vm` §7.2, §7.3; ktdm pin registry·map verify·pinvi lock 무결성·weather `--locked` 선례 | Renovate 설치 가능 여부 미확인; 봇 없이는 "격차 보고" 단계부터 |
| 개발 환경·worktree·CodeGraph 불변 조건(OS 미규정, 프로필 선언 위임) | 규약 문서 | 7개 저장소 | 높음 | 낮 | `dc` §2 C1·C2, §3.5 | common 자체 정본 OS(§4.2) |
| provider 정책 매트릭스·kill switch 문서 형식(concierge), `dashboard-ui.md` UX 계약(ktdm), Hallmark 기록 형식(airport) | 규약 문서(템플릿) | map·pinvi / 전 admin / 전 앱 | 낮~중 | 낮 | `inv/kor-travel-concierge` §8-20, `inv/kor-travel-docker-manager` §8-21, `inv/kor-travel-airport` §8-22 | Hallmark 스킬 본문 인용 금지(lic B3) |

### 2.6 CI 템플릿·도구

| 영역 | 배포 단위 | 1차 소비자 | 신뢰도 | 난이도 | 근거 | 보류/제외 사유 |
|---|---|---|---|---|---|---|
| `python-quality.yml`(installer uv/pip, pre-install, ruff/format/mypy/import-linter/alembic/pytest/coverage, db-image) | CI 템플릿 | airport·ktdm·geo·weather·pinvi; concierge 신설 | 높음 | 중 | `ci` §2.1, §2.2 | required check 이름은 입력으로 개방 |
| `node-quality.yml`(npm 핀, lockfile 무결성, audit high/dev, typegen drift, lint 0 warn, test, build) | CI 템플릿 | 전 프론트 | 높음 | 중 | `ci` §2.1 | npm 12.0.1 vs 11.19.1 정책 종속 |
| `openapi-drift.yml`, `typegen-drift` | CI 템플릿 | geo·map·weather(교체), 나머지 신규 | 높음 | 낮 | `ci` §2.1; `oa` C8 | — |
| `docs-check.yml`(링크·redaction·task ledger) | CI 템플릿 + 도구 | common 자체·map(redaction 이관) | 중 | 낮 | `ci` §2.1, §4; `cv` §1.3 | redaction 적용 범위 정책 |
| `secret-scan.yml`(AGENTS 수동 절차 스크립트화) | CI 템플릿 | 전 앱(현재 CI 0) | 중 | 낮 | `ci` §2.1; `dc` §1.16 | 외부 스캐너 채택 여부 |
| `docker-build.yml`(buildx·산출물 대조·기동 확인), `aggregate-gate.yml`(경로 규칙 입력형) | CI 템플릿 | map·pinvi(원형), concierge | 중 | 중 | `ci` §2.1 | — |
| 하드닝 기본값(`permissions: contents: read`, concurrency, timeout, `ubuntu-24.04`, head SHA checkout, 액션 SHA 핀) | CI 템플릿 기본값 | 전 앱 | 높음 | 낮 | `ci` §1.3, §2.1 | 액션 major(v4/v5 유지 vs v7) 결정 |
| common 자체 CI(`docs`·`workflows-selftest`·`packages`(npm pack→tarball 설치)·`python-package`·`consumer-smoke`·`secret-scan`) | common `.github/workflows` | common | 중 | 중 | `ci` §4; 선행 §7.3·§10 | 현재 `docs.yml`은 링크 17건 실패 상태(`cv` §1.3) |
| 문서 검증 도구(`validate_plan.py`·`validate_document_links.py`·`test_plan_validation.py`) | 도구(common 보유) | common; 소비 저장소는 선택 | 높음 | 낮 | `cv` §1.2, §4 | 원장 형식·절대 접두·CRLF(§4.2) |
| 프론트 툴체인 무결성(`verify-npm-tree`·`verify-next-sharp`·lockfile integrity) | 도구 | map·pinvi(원형) → 전 앱 | 중 | 중 | `vm` §3.6; `ci` §1.5 | 정확 핀 상수 관리 주체 |

## 3. 버전 정렬 격차 요약

### 3.1 후보 기준선(`vm` §5.1 후보 A, 결정 아님)

Node 22.x(CI 20 사용처 22로) · npm 11.19.x 또는 12.0.2 · Next 16.3.x · React 19.2.x · TypeScript 5.9.3 · Tailwind 4.3.3 · Base UI 1.8.0 · ESLint 9.39+/10 · Vitest 4.1.x · Playwright 1.63 · Python `>=3.12`, 이미지 3.12-slim · FastAPI 0.141/Starlette 1.6/uvicorn 0.52/pydantic 2.13 · SQLAlchemy 2.0.52/alembic 1.19 · dagster 1.13 · pytest 9.1/pytest-asyncio 1.4 · ruff 0.16/mypy 2.3 · PostgreSQL 16+PostGIS 3.5 digest 핀 · Actions v4/v5+SHA 핀. 최신 안정 대조는 `vm` §4.

### 3.2 앱별 major 격차와 선행 작업(`vm` §5.2·§1.8·§2.1, `ui` §2.3, `dt` §3.6.7)

| 앱 | major 격차 | minor·툴체인 격차 | 선행 작업(공통 소비 전) | 난이도(추정) |
|---|---|---|---|---|
| airport(main) | **Tailwind 미도입**(순수 CSS 1,844행) → WIP `99b3f98`이 v4.3.3+shadcn `base-nova` 전환 중; **TypeScript 7.0.2**(typescript-eslint peer `<6.1.0` 밖, 5.9 하향 또는 정책 결정 — `vm` §6) | next 16.3.2→16.3.4; `@types/node` 26 | WIP 머지 여부 확정; ESLint·ruff 신규 도입; Docker에서 `uv.lock` 소비; `engines` 선언; `cn@0.2.5`→clsx+tailwind-merge; `--muted/--accent/--radius` 별칭 충돌 회피(`inv/kor-travel-airport` §3.2); 다크 media→class 여부 | 낮~중 |
| concierge | `@hookform/resolvers` 3→5; `maplibre-gl` 6.0(공유 라이브러리 peer `^5.24` 밖) | next 16.2.7→16.3; base-ui 1.5→1.8; lucide 1.17→1.41; TS `^5.4.5` 하한 상향 | **CI 신설**; **Python lock 도입**(`requirements.txt` 4벌 하한만, `mcp<2` 사고); `@config` JS config 제거; `shadcn` CLI dependencies 위치; ruff/mypy 신규; `frontend/Dockerfile` dev 서버 이미지 | 중~높 |
| docker-manager | **Next 14→16(2 major)**, **React 18→19**, ESLint 8→9/10(+`eslint-config-next` 14→16), lucide 0.363→1.x; **shadcn/base-ui 미도입**(`ops-*` CSS 146줄+유틸 179줄 혼용) | tailwind 4.3.1→4.3.3; `tsconfig target es5`; `next lint` 제거 대비 | Poetry→lock(uv) 도입; fastapi `^0.110`·uvicorn `^0.28`·ruff `^0.3`·mypy `^1.9` 하한 상향; CI Node 20→22; `pytest ^8` vs CI 9.1.1 정리; 프리미티브 도입 자체가 선행 | **높음** |
| geo | **React 18→19**(ADR-019가 18 유지 명시; 차단 사유 문서 없음), **Radix→Base UI**(12파일 재작성, `asChild` 17곳 — `ui` §5.2), lucide 0.468→1.x, jsdom 25→30 | next 16.2.12→16.3; tailwind 4.3.1→4.3.3; `@config` 잔존 제거; pre-commit ruff 0.7.4/mypy 1.13.0 → 0.16/2.3 | CI Node 20→22; **Python lock 도입**; lock 2026-07-28 이후 미갱신; `source(none)`+`@source` 명시 규약 유지 | **높음**(UI) / 중(Python) |
| map | TS 6.0.3(map-marker-react) vs 5.9.3(admin) | next 16.2.12→16.3(`verify-next-sharp.mjs` 상수 동반); base-ui 1.6→1.8; Playwright 1.60→1.63(+이미지) | **Python lock 도입**; `starlette<1.0`·`alembic<1.20` 상한 재검토; npm 12.0.1 강제와 pinvi 11.19.1 합의; `ubuntu-latest` | 낮~중 |
| weather(admin) | **Tailwind 미도입**(2,495행 CSS, 170 클래스, bare element 23종 — 전환 정량 `inv/kor-travel-weather` §9.1), **Next 15.5→16**, Vitest 3.2→4/5, `eslint-config-next` 15→16, react-hooks plugin 5→7 | `moduleResolution: node`→bundler; react-query 미사용 선언 정리; `@types/node` 22 | CI Node 20→22; CI에 vitest·mypy 추가; Python 선언 3.11/CI 3.12/Docker 3.13 정합; `python-airkorea-api` 벤더링 정리; 셸 문서-코드 불일치(17rem·접힘 없음) 해소 | 중~높 |
| pinvi web/admin | `@hookform/resolvers` 3→5(선언만), jsdom 25→30, lucide 0.460→1.x | react 19.2.6(override)→19.2.8; TS `^5.6.0` 하한; base-ui 1.8(이미 최신) | `uv.lock`을 CI·Docker에서 실제 소비; `@config` v3 preset ↔ `@theme` 이중 정본 해소; webpack 강제(ADR-066) 하에서 common 패키지 검증; **라이선스 결정 선행**(§4.1 B1) | 중 |
| pinvi mobile | **Tailwind 3.4.19 유지**(NativeWind 4; v5는 preview) — v4 전환은 외부 의존 | expo 57 문서(SDK 56 표기) 정합 | NativeWind 5 GA 대기; 전환 시 web Dockerfile 중첩 `node_modules` 전략·lockfile·preset 소비 방식 동시 변경(`inv/pinvi` §3.2); RN 정확 핀(react 19.2.6·RN 0.86.3)이 web React까지 묶음 | **높음**(외부) |

### 3.3 전환 트랙(공통 소비 순서에 영향)

| 트랙 | 대상 | 근거 |
|---|---|---|
| Tailwind v4 도입(미도입→도입) | weather admin, airport main(WIP 진행 중), pinvi mobile(v3→v4, NativeWind 5 대기) | `vm` §1.2·§1.7; `inv/kor-travel-weather` §9.1; `inv/kor-travel-airport` §3.2 |
| `@config` v3 config 잔존 제거(CSS-first 단일화) | geo, concierge, pinvi web | `dt` §3.1.1, §3.6.3; `inv/kor-travel-geo` §9 |
| React 18→19 | geo, docker-manager | `vm` §5.3; `ui` §2.3(base-ui peer는 18 허용 — 업그레이드와 독립 가능) |
| Next 14/15→16 | docker-manager(14.2.35), weather(15.5.24) | `vm` §5.3(Async Request API·`proxy` 규약·`next lint` 제거) |
| Radix→Base UI(엔진 결정 시) | geo | `ui` §5.2 |
| 프리미티브 도입 자체 | docker-manager, weather, airport main | `ui` §4.3 |
| TypeScript 기준선 | airport 7.0.2 → 5.9(또는 6.x 경유) | `vm` §6; 열린 질문 1 |
| ESLint 8→9/10 | docker-manager; airport는 0에서 도입 | `vm` §1.6 |
| Vitest 3→4/5 | weather | `vm` §1.6 |
| Node 20 CI→22 | docker-manager, geo, weather(Node 20 EOL 2026-04-30) | `vm` §1.1, §4.4 |
| npm 실행기 정책 | map 12.0.1 vs pinvi 11.19.1 vs 동봉 10.9 | `vm` §3.2, 열린 질문 3 |
| Python lockfile 도입 | geo, map, docker-manager, concierge | `vm` §2.1, §7; `be` §5.3 |
| Python floor 3.11 vs 3.12 | map·weather·docker-manager(3.11) vs airport·geo·pinvi(3.12); geo는 PEP 695 사용 | `be` §2.1, §7-1 |
| lockfile 소비 일관화 | airport Docker pip, pinvi CI·Docker pip | `vm` §2.1 |
| lucide-react 0.x→1.x | docker-manager, geo, weather, pinvi | `vm` §1.3(breaking 내용 미조회) |
| starlette/alembic 상한 | map `starlette<1.0`, `alembic<1.20` | `vm` §2.2·§2.3; `oa` Q7 |
| provider git SHA 정렬 | `python-kma-api`(map ≠ weather), `python-kasi-api`(airport SHA vs pinvi etl `@main`), `python-airkorea-api`(weather path vs map SHA) | `vm` §2.7; `be` §5.1 |
| PostgreSQL/PostGIS major | 전 앱 16+3.5(최신 18+3.6) — 라이브러리 정렬과 분리 권고 | `vm` §3.4, §5.1 |
| Prometheus major | ktdm·pinvi v2.53.1 vs weather v3.5.0 | `vm` §3.4; `ci` §1.13 |

## 4. 차단 항목과 열린 결정

### 4.1 차단 항목(권리·계약 확인 전 이동 금지)

| ID | 항목 | 이유 | 해제 조건 | 근거 |
|---|---|---|---|---|
| B1 | pinvi의 모든 파일(자체 코드 P4, 이식 코드 P1·P2 포함) | 루트 `LICENSE` 없음, README "비공개(사내)" vs AGENTS "공개" 상충, `apps/api` MIT | 권리자의 라이선스 선언(L6) | `lic` §2.2 D4, §3.6, §4 B1 |
| B2 | pinvi 벤더 tgz(`vworld-map-*`)·`maplibre-vworld-react` 소스 | 이미 분리된 공유 라이브러리(중복 금지) + 패키지 라이선스 메타데이터 부재 | 영구 금지; common은 의존만. npm 게시·`license` 필드는 L7 | `lic` §2.5, §4 B2; `ui` §4.3 |
| B3 | Hallmark `SKILL.md` 본문·참조 문서 | 저작자·라이선스 미확인("Powered by Together AI"만) | 원천 확인 전 규칙 문서에 문장 인용 금지; 스탬프 형식만 채택 | `lic` §2.5, §3.2, §4 B3 |
| B4 | concierge `AppShell.tsx`·`globals.css`가 참조한 map IA·토큰 값 | 코드 복사인지 개념 참조인지 미확인(MIT 저장소 안의 GPL 코드 가능성) | 파일 diff로 확정 후 `PROVENANCE`에 기록 | `lic` §4 B4 |
| B5 | pinvi 락파일 `@radix-ui/*` 21개 | 직접 선언 없이 전이 — 고지 누락 위험 | 역추적(`npm ls`) | `lic` §4 B5 |
| B6 | shadcn 생성 컴포넌트(map M1·geo G1·concierge C1) | 생성 시점 shadcn 버전 미기록 | shadcn `LICENSE.md` 원문 확보 후 MIT 고지 | `lic` §4 B6 |
| B7 | `python-*-api` 13종 중 라이선스 미확인 저장소 | GitHub 확인은 kma·kasi·vworld·kraddr-base만 | 각 `LICENSE` 확인 후 `THIRD_PARTY_NOTICES` | `lic` §4 B7 |
| B8 | 봇 계정(Codex·Claude) 커밋분 | 권리 귀속 미확인 | `CONTRIBUTING`에 "AI 보조 생성물은 권리자가 GPL로 배포" 명시(후보) | `lic` §4 B8 |
| B9 | ktc·ktdm이 common **코드**를 링크하는 것 | MIT 앱이 GPL 라이브러리를 배포 시 결합물 GPL(FAQ `#IfLibraryIsGPL`) | 루트 GPL 정렬(권고) 또는 common §7 추가 허가 결정(L8) | `lic` §3.6, §6-2 |
| B10 | map·pinvi·docker-manager·concierge 간 sha256 pin 계약(OpenAPI 스펙·M05 provenance·pinset) | common이 흡수하면 세 저장소 릴리스가 동시 결합 | 흡수 부적합 — 규약만 | `inv/kor-travel-docker-manager` §9; `oa` §4 map |

### 4.2 열린 결정 목록(설계 단계)

| # | 결정 | 선택지·현황 | 근거 |
|---|---|---|---|
| D1 | 프리미티브 엔진 | Base UI(29 파일 소비: map·concierge·pinvi admin·airport WIP) vs Radix(geo 12) — Base UI 채택 + 비-overlay는 native 우선이 변경 최소(후보) | `ui` §5.1~5.4, §7-1·3 |
| D2 | UI 배포 방식 | A 자체 shadcn registry / B npm 패키지(ESM+CSS, `@source` 등록) / C 소스 복사+정본 지정 / 이원화 | `ui` §6.2, §7-8; 선행 §7.3 |
| D3 | 토큰 접두·CSS 배포 형태 | `--kt-`(충돌 0) vs `--ktc-`(concierge 125회 사용, 승격 경로); `tokens.css`/`theme.css`/`shadcn.css`/`base.css` 분리; 사전 빌드 CSS(선행 §7.3) vs v4 소스 | `dt` §3.6.1, §3.6.3, §5-1 |
| D4 | shadcn alias 의미 고정 | `--input`(컨트롤 경계 vs airport WIP 입력 배경), `--accent`(brand-tint vs geo surface-muted) | `dt` §3.2.3 |
| D5 | 다크 모드 | 값 정의 필수 + 활성화 앱 선택(class vs media) vs "정의 필수, 검증 선택"; 토글 도입 계획 유무 | `dt` §3.6.6, §5-6; `ux` C14 |
| D6 | 모바일 앱(pinvi mobile) 취급 | 정렬 정책 범위 제외 vs Tailwind 3 예외 등록; RN 정확 핀이 web React를 묶는 구조 존중 여부; DTCG/TS 토큰 출력 제공 여부 | `vm` 열린 질문 8; `dt` §3.6.7 |
| D7 | pinvi 사용자 표면 포함 범위 | 코드 제외(선행 §1)·규칙 문서 공유(consumer 프로필) | `ux` §1.14, §3.1; `dt` §5-7 |
| D8 | 개발 환경 정본(common 자체·공통 절) | canview Windows PowerShell vs 6개 저장소 Linux/WSL — OS 미규정·프로필 위임(후보), common 자체는 Linux/WSL(후보); 경로 표기 `F:/` vs `/mnt/f/`; 설정 파일 템플릿 형식(geo 이식형) | `dc` §2 C1·C13; `cv` Q4 |
| D9 | worktree 프로필 | 고정(geo·map·pinvi·ktdm) vs 임시(canview) — 불변 조건만 공통 | `dc` §2 C2 |
| D10 | TypeScript 기준선 | 5.9.3 통일(airport 하향) vs 6.x 경유 vs 7 대기; airport의 7 채택 사유 미문서 | `vm` §6, 열린 질문 1 |
| D11 | Node/npm 기준선 | Node 22 우선 vs 24 Active LTS; npm 11.19.x(동봉) vs 12.0.2(별도 설치) | `vm` §5.1, 열린 질문 2·3; `ci` 열린 질문 2 |
| D12 | Python floor·이미지 | common 3.11 호환 vs 앱 floor 3.12 상향; 이미지 3.12 vs 3.13(weather) | `be` §7-1; `vm` 열린 질문 4 |
| D13 | Python lockfile 도구·소비 | uv 통일(ktdm Poetry 매니페스트); CI·Docker `--locked` 강제; 하한 전용 선언에 상한 부여 | `vm` 열린 질문 10·11; `be` §7-9 |
| D14 | 버전 핀 정책·레지스트리·자동 갱신 | P1 전면 정확 핀 / P2 caret+lock / **P3 계층별 하이브리드** / P4 renovate preset / P5 dependabot; `version-registry.v1` 형식; Renovate 설치 가능 여부; provider SHA 포함 여부 | `vm` §7.2, §7.3, 열린 질문 7·12 |
| D15 | 인증 범위 | 로그인·세션·CSRF·역할 판정은 앱(선행 §3.6 유지); 공개 API 키·trusted proxy 원시 함수·request-id·세션 상수 규칙 문서만 | `be` §2.8, C7·C8; `inv/kor-travel-geo` §9 |
| D16 | 요청 ID 정책 | 서버 발급 강제(ktdm) vs 검증 후 echo(map·weather·pinvi); BFF 체인의 발급자 | `oa` M4, Q9; `be` §7-5 |
| D17 | 에러 envelope·검증 코드 | RFC7807+`code`+`request_id` 통일 시 pinvi `{error}`·concierge/ktdm `{detail}`·geo v1/v2 전환 시점; 422 vs geo 400; 429 코드명 | `oa` M3, Q1~Q3, §4 |
| D18 | health 경로·readiness 표준 | `/health`(6) vs geo `/healthz`; `/readyz` 채택; 소비자 probe 변경 범위 | `oa` M5, N8; `be` §7-7 |
| D19 | 메트릭 접두 | `kt<x>_`(ktc·ktdm·ktg·ktw) vs map `kor_travel_map_`·pinvi `pinvi_api_` — 대시보드 회귀 범위 미확인 | `be` §7-4; `inv/kor-travel-map` §9 |
| D20 | 헤더 이름 접두 | 풀네임(`X-Kor-Travel-Map-*`) vs 약어(`X-KTG-*`, `X-KTC-*`) | `inv/kor-travel-map` §8-18; `oa` §2.4, C11 |
| D21 | 버전 prefix·페이지네이션 이름 | `/v1` vs `/api/v1` vs `/`; `page_size`/`next_cursor`(map) vs `limit`/`has_more`; pinvi 정수 `If-Match`+409 vs ETag+412 | `oa` Q4, Q6, S2, S5 |
| D22 | typegen vs Zod | pinvi Pydantic↔Zod 이중 유지와 `openapi-typescript`의 관계 | `oa` Q5 |
| D23 | starlette/alembic 상한 | map `starlette<1.0` 사유 재검증(다른 3앱은 1.6.0 설치) | `oa` Q7; `be` §7-2 |
| D24 | 라이선스 정렬 | ktc·ktdm·pinvi를 GPL-3.0-or-later로 정렬(권고) vs common §7 추가 허가; pinvi 공개/비공개; geo `-only` 유지 여부; `maplibre-vworld-react` MIT 재선언 여부; kta·weather 버전 고지 | `lic` §3.6, §6-1~4 |
| D25 | 고지·헤더·메타데이터 규약 | SPDX 헤더 + `Origin/Derived-From/Modified`; Hallmark 스탬프와의 줄 순서; npm/PEP 639 필드 | `lic` §3.3~3.5 |
| D26 | AGENTS 공통 절 세부 | geo Goal-Driven 추가 불릿 포함 여부; SKILL 라우터화; pinvi "ADR > AGENTS" 예외; 지시 우선순위 9단계 | `dc` §2 C4·C5, §5 Q1~Q3 |
| D27 | task 원장 형식·문서 도구 | 체크박스 원장(`dc` §3.3) vs 5열 표(common `validate_plan.py`); `docs/decisions.md` 유무; 절대 링크 접두 허용; 도구 언어(Python vs Node); `.py` CRLF | `cv` §5 Q1~Q3·Q5·Q6; `dc` §5 Q5 |
| D28 | review gate | full/light 경계와 판정 주체; 상태 어휘(`IN_REVIEW/COMPLETE/POST_FIX_REVIEW/PASS`)·post-fix 명명 | `dc` §2 C7, §5 Q4; `cv` §3.3 R3.2·R3.6 |
| D29 | ADR 저장 형식 | 파일당 1개(kta·geo·map·wx) vs 단일 `decisions.md`(conc·ktdm·pinvi); wx의 map 번호 미러 금지 | `dc` §2 C8, §5 Q9 |
| D30 | journal/resume archive | map §8(220KiB) 채택 시 conc·ktdm·geo·pinvi 분리 시점 | `dc` §2 C9 |
| D31 | 포트·명명 | airport web 14002 예외 vs 14005 이전; 컨테이너 `-latest` 접미; common 130xx 대역; compose 서비스명 고정 어휘 | `ci` 열린 질문 3·4·11, §3 |
| D32 | CI 정책 | 재사용 워크플로 cross-repo 호출 조건; 액션 major(v4/v5+SHA vs v7); prod 호출 job(kta `live-e2e`) 허용 여부; secret 스캐너; redaction 적용 범위; arm64 포함 | `ci` 열린 질문 1·5·6·7·10; `vm` §5.1 |
| D33 | UX 충돌 규칙 | 접힌 rail 4rem vs 5rem; strip vs drawer; 컨트롤 36/30 vs 44(pinvi admin 예외 2쪽); 확인 다이얼로그 동사 라벨·`window.confirm` 금지; 토스트 정책·엔진; 상태 tone 이름(geo CANCELLED); dirty 이탈 경고; 로그인 아이콘 타일; HelpTip popover-only 허용; Hallmark 스탬프 형식 | `ux` §4 C1~C21, §5 |
| D34 | breakpoint·검사 폭 | sm/md/lg/xl 채택; weather 62/42rem·airport 860 재조정; 검사 폭 320/375/414/768/1024/1440 | `ux` §3.2, C3 |
| D35 | "kor-travel-airport Admin"의 정의 | 현재 무인증 백업 패널·`/v1/admin/*` vs T-035 이후 분리 라우트 | `inv/kor-travel-airport` §9, §11-9; `ux` §5-5 |
| D36 | 마커 팔레트 정본·`map-marker-react` 게시 | map(Tableau) vs pinvi(Material) hex; ADR-043 게시 보류 해제 | `dt` §3.5, §5-2 |
| D37 | 지도 스타일 빌더 배포 경로 | `vworld-style.ts` 중복(map·weather)·pinvi tgz·geo tarball — `maplibre-vworld-react` npm 배포 정책과 함께 | `ux` §1.10, C22; `inv/kor-travel-geo` §9 |
| D38 | Python 패키지 배포 채널 | A `git+https@<sha>`+태그(기본 후보) / B path / C 사내 index / D wheel URL; npm은 D2와 연동 | `be` §5.2 |
| D39 | 관측 스택 결선 | Prometheus major(v2 vs v3)·ktdm scrape에 map·concierge·pinvi job 부재를 common 규약으로 둘지 ktdm 소유로 둘지 | `ci` §1.13, 열린 질문 9 |
| D40 | 폰트 로딩 책임 | 스택 문자열은 common, 로딩(npm pretendard/next/font/미로드)은 앱 | `dt` §5-8; `ux` C12 |
| D41 | 선언만 남은 의존성 처리 | weather react-query, pinvi rhf·next-intl·zustand(web), geo structlog·testcontainers·hypothesis, map log_format — 정렬 표에서 "미사용 선언" 구분 | `inv/*` §9; `be` §7-10·11 |

## 5. 근거 문서

- 인벤토리: `inventory/kor-travel-airport.md` §3·§4·§8·§9·§10, `inventory/kor-travel-concierge.md` §3·§4·§8·§9·§10·§11, `inventory/kor-travel-docker-manager.md` §3·§4·§8·§9·§10, `inventory/kor-travel-geo.md` §3·§4·§8·§9·§10, `inventory/kor-travel-map.md` §3·§4·§8·§9·§10, `inventory/kor-travel-weather.md` §3·§4·§8·§9·§9.1·§10, `inventory/pinvi.md` §3·§4·§8·§9·§10.
- 횡단: `cross/version-matrix.md` §1~§7·열린 질문, `cross/design-tokens.md` §3~§5, `cross/ui-components.md` §2~§7, `cross/ux-patterns.md` §1~§5, `cross/backend.md` §2~§7, `cross/openapi.md` §2~§6, `cross/ci-deploy.md` §1~§4·열린 질문, `cross/docs-conventions.md` §1~§5, `cross/canview-structure-checklist.md` §1~§5, `cross/licensing.md` §2~§6.
- 이 문서가 직접 저장소를 다시 읽은 항목은 없다. 문서 간 수치 불일치의 재확인 결과는 [README.md](README.md) §6.2에 있다.
