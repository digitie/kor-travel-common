# kor-travel-common 결정 레지스터 초안 (coordinator draft, 2026-09-06)

근거: `F:/dev/kor-travel-common/docs/survey/inventory/*.md`, `docs/survey/cross/*.md`(design-tokens, ux-patterns, openapi, backend, version-matrix, docs-conventions, ui-components; ci-deploy·licensing·canview-structure는 작성 중). 선행 보고서 geo `docs/kor-travel-common-library-review.md`(2026-09-05).
사용자 전제: (1) Tailwind v4 기반이 아닌 앱은 v4로 전환, (2) 라이브러리/플랫폼 버전 일치화 정책 포함, (3) airport Admin·PinVi Admin 포함, (4) 코드 + 규칙(색상 톤·UX·OpenAPI·PC/Mobile Web) 산출, (5) canview 구조·AGENTS.md 내용 채택, (6) GPL-3, Tailwind v4 + shadcn/ui + React + Next.js.

표기: 결정 = 이 초안의 선택. 대안 = 기각한 선택. 근거 = 조사 문서 절. 결과 = 소비자 영향. 열림 = 사용자/후속 확인 필요.

## A. 저장소 범위·구조

### D-01 배포 단위(패키지 경계)
- 결정: 5개 배포 단위 + 규칙 문서 + 템플릿.
  1. `packages/tokens` → npm `@kor-travel/tokens`: `tokens.css`(`--kt-*` :root/.dark, Tailwind 무관), `theme.css`(v4 `@theme inline` 연결 + `@utility duration-*`), `shadcn.css`(shadcn alias 고정 의미), `base.css`(focus 단일 레시피·hairline 2종·reduced-motion·cursor), `dark-class.css`/`dark-media.css`, `tokens.json`(DTCG)·`tokens.ts`·`tailwind-preset.cjs`(v3/NativeWind용), `bin/kt-contrast`(대비 검사).
  2. `packages/ui` → npm `@kor-travel/ui`: React 19 admin UI. 1차 소형 컴포넌트, 2차 Button/overlay/Table/DataTable/Pager/CopyButton/JsonViewer/DetailList/StatusBadge/AdminPageHeader. peer: react ^19.2, @base-ui/react ^1.8, tailwindcss ^4.3(소비자 `@source` 등록), lucide-react ^1.
  3. `packages/config` → npm `@kor-travel/config`: eslint flat config base(next·react-hooks·jsx-a11y·import·금지 패턴 규칙), tsconfig base, prettier 설정, vitest 공통 setup, `versions.json` 대조 스크립트의 JS 부분.
  4. `packages/api-client-core` → npm `@kor-travel/api-client-core`: problem+json 파싱·`ApiError`·Retry-After·타임아웃·Idempotency-Key 슬롯(query key·인증·캐시는 앱 소유). 3차.
  5. `packages/py/kor-travel-common` → Python dist `kor-travel-common`, import `kortravelcommon`, extras `api`/`db`/`dagster`/`testing`/`http`: settings·time·errors·health·metrics·request_id·problem·envelope·pagination·security(공개 API 키·trusted proxy·metrics bearer)·openapi export CLI·alembic 템플릿·testing 픽스처·quality(ruff/mypy/import-linter 베이스).
  6. `docs/standards/*`: design-tokens, ux-guide, responsive-web(PC/Mobile), openapi, versions(정책+매트릭스), frontend-stack, backend-stack, agent-conventions(공통 AGENTS 절·docs 트리·tasks-rule·review gate), ci-deploy(포트·서비스명·CI 템플릿).
  7. `templates/`: AGENTS 공통 절, CLAUDE.md 포인터, agent 설정 파일(geo 형식), alembic env, `.github` 재사용 워크플로 호출 예, renovate/dependabot 설정, 소비자 PR 본문.
  8. `versions.json`(루트, schema `kor-travel-common.version-registry.v1`) + `tools/check_versions.py`.
- 대안: 단일 거대 패키지(비권고, 선행 §6), 모노레포 통합(과도), 규칙만·코드 없음(사용자 전제 4 위반).
- 근거: 선행 §7.1(토큰+UI 두 패키지에서 시작), backend §3 C1~C20(비인증 인프라 모듈 근거), openapi §5 C1~C11, ui-components §4, design-tokens §3.6.3.
- 결과: 앱 → ui → tokens, 앱 → py 단방향. common은 앱 도메인 모듈·지도 엔진·인증 서비스 import 금지.

### D-02 저장소 구조(canview 대응)
- 결정: canview 계층형 문서 구조를 채택하고 하드웨어·차량 항목은 제외. 추가: `CLAUDE.md`(40줄 이하 포인터), `docs/standards/`, `docs/survey/`, `docs/plan/`, `docs/dev-environment.md`, `docs/integration-map.md`(소비자별 채택 버전표), `packages/`, `templates/`, `versions.json`. `docs/decisions.md`는 canview와 동일하게 유지(색인; 다음 번호 정본).
- 근거: docs-conventions §4 대응표, canview-structure-checklist(작성 중).

### D-03 개발 환경 정본(common 자체)
- 결정: Linux/WSL bash를 정본으로, Windows Git Bash/PowerShell은 문서·검증 보조. CI = ubuntu. 임시 worktree 프로필(canview ADR-003 방식): 기본 `F:/dev/kor-travel-common` 작업 브랜치, 필요 시 `F:/dev/kor-travel-common-wt/<agent>-<task>`.
- 대안: canview처럼 Windows native 정본(소비자 6/7이 WSL 정본이라 불일치).
- 근거: docs-conventions §2 C1·C2.
- 결과: runbook 명령은 bash 표기, PowerShell 블록은 두지 않음. `python3`/`uv run` 표기.

### D-04 리뷰 gate
- 결정: common 자체는 canview full gate(2인 독립·immutable 기준선·evidence·P0~P3·disposition 4종·post-fix 재검토)를 비단순 변경 전부에 적용. 소비자용 표준은 full/light 2단계(docs-conventions C7) — full 대상: 정책 문서·계약·인증·공용 primitive·토큰·OpenAPI 산출물.
- 열림: light 판정 주체(Q4) → PR 작성자가 아닌 merge 담당이 판정, 근거를 PR 본문에.

### D-05 task 원장 형식
- 결정: common 자체는 canview 5열 표 + `READY/BLOCKED/IN_PROGRESS/DONE` + `validate_plan.py`. 소비자 표준은 체크박스 원장 허용 + 상태 대응표(docs-conventions C6). ID 대역은 `docs/tasks-rule.md` §2.

## B. 프론트엔드 스택·버전 정렬

### D-06 정렬 기준선(2026-09, 후보 A "최소 이동" 기반 + 일부 최신)
| 축 | 기준선 | 근거 |
|---|---|---|
| Node | 22 LTS 실행(Docker `node:22-bookworm-slim`), engines `^22.22.0 \|\| ^24.15.0`; 2026-10 이후 24로 상향 검토 | version-matrix §5.1(모든 이미지 22, Node 20 EOL) |
| npm | Node 동봉 11.19.x 기준, 허용 `>=11.19 <13`; 저장소별 `packageManager` 정확 핀 허용(map 12.0.x 유지 가능) | §5.1·Q3 |
| Next.js | 16.3.x(`^16.3.4`) | §5.1 |
| React | 19.2.x(`^19.2.8`) | §5.1 |
| TypeScript | **5.9.x** 기준선; TS 7은 typescript-eslint 지원(peer `<6.1`) 전까지 "추적 예외"(airport). airport는 ESLint 도입 시점에 5.9로 정렬 | §4.4·§6 |
| Tailwind | 4.3.x(`^4.3.3`) + `@tailwindcss/postcss` 동일 | §5.1 |
| primitive | `@base-ui/react` ^1.8 | ui-components §5.4 |
| shadcn CLI | 4.21.x, **devDependencies**에만 | version-matrix §7.1(concierge dependencies 배치 지적) |
| lucide-react | ^1.41 | §5.2 |
| ESLint | 10.x + typescript-eslint 8.x + eslint-config-next 16.3.x | map 선례, dm 8 EOL |
| Vitest | 4.1.x(5.0은 다음 분기 재검토; Node 22.12+ 전제) | §5.1 |
| Playwright | 1.63.x | §5.1 |
| react-query / react-table / react-virtual | 5.x / **8.21.x**(9는 breaking 미조사) / 3.14.x | §5.3 |
| zod / RHF / resolvers / zustand | 4.x / 7.8x / 5.x / 5.x | §4.2 |
| maplibre-gl | 5.24.x(공유 라이브러리 peer) — concierge 6.0은 예외 등록, `maplibre-vworld-*` 6 지원 시 재정렬 | Q5 |
| Python | `requires-python >=3.12`, 이미지 `python:3.12-slim`(3.13 허용) | backend §5.3·Q1 |
| 잠금 도구 | **uv**(uv.lock 커밋, CI·Docker `--locked`); Poetry(ktdm)·requirements.txt(concierge)는 uv로 전환 task | version-matrix Q10·11 |
| FastAPI 계열 | fastapi 0.141.x, starlette 1.6.x(map `<1.0` 상한 재검증 task), uvicorn 0.52.x, pydantic 2.13.x, pydantic-settings 2.15.x | §4.3 |
| SQLAlchemy / alembic | 2.0.5x / 1.19.x(map `<1.20` 상한 재검토) | §4.3 |
| asyncpg / psycopg | 0.31.x / 3.3.x(앱 선택) | §4.3 |
| structlog / prometheus-client / httpx / tenacity / typer | 26.x / 0.26.x / 0.28.x / 9.x / 0.27.x | §4.3 |
| dagster | 1.13.x | §4.3 |
| pytest / pytest-asyncio / ruff / mypy / import-linter / testcontainers | 9.1.x / 1.4.x / 0.16.x / 2.3.x / 2.15 / 4.15.x | §4.3 |
| PostgreSQL/PostGIS | 별도 트랙(현 16+3.5 digest 핀 유지) — 라이브러리 정렬 범위 밖 | Q9 |
| GitHub Actions | checkout v7 / setup-node v7 / setup-python v7 / setup-uv v10, SHA 핀 | §4.4 |

### D-07 핀 정책
- 결정: 계층별 하이브리드(P3) — 플랫폼·프레임워크·툴체인(node, npm, python, uv, next, react, typescript, tailwindcss, @tailwindcss/postcss, @base-ui/react, eslint+config, vitest, @playwright/test, fastapi, starlette, sqlalchemy, alembic, pytest, ruff, mypy, dagster)은 **정확 핀 + `versions.json` 대조**, 나머지는 caret + lockfile. 공유 renovate preset(P4)은 Renovate 앱 설치 가능 시; 아니면 `templates/dependabot.yml`. `tools/check_versions.py`는 1단계 "보고", 2단계 "실패".
- 근거: version-matrix §7.2·7.3(dm runtime-pin-registry 형식 차용).

### D-08 Tailwind v4 전환 대상과 방식
- 결정: 
  - weather admin: 순수 CSS → v4 CSS-first + `@kor-travel/tokens` + Next 15→16 + Vitest 3→4. 셸은 common 이관 시 교체.
  - airport: WIP 브랜치 `codex/shadcn-ui-foundation`(v4 + shadcn base-nova + base-ui 1.8)을 v4 기반으로 채택하되, 토큰을 `--kt-*` admin 프로필(6/8, 36/30, control-line 3:1)로 정렬. `tokens.css` alpha line은 제거.
  - docker-manager: v4 설치 유지, `ops-*` 146줄 + 유틸리티 혼용 → 토큰·common UI로 정리; Next 14→16, React 18→19, ESLint 8→10 선행.
  - geo: `@config tailwind.config.ts` 제거(v3 잔존 hex와 `@theme` 이중 정의 해소), radix→base-ui, React 18→19.
  - concierge: `@config`·hex fallback 블록 제거, `--ktc-*`를 `--kt-*` 오버라이드로 재해석.
  - pinvi web: admin은 `@theme` 스코프 유지(`[data-pv-surface='admin']`)로 `--kt-*` 매핑; 사용자 표면은 v3 preset `@config` 유지(consumer 프로필)하되 `tokens.json/ts` 재수출 검토(3차).
  - pinvi mobile: NativeWind 4/Tailwind 3 **문서화된 예외**(NativeWind 5 GA 시 재평가). 정렬 정책 범위에서 "예외 등록".
- 근거: design-tokens §3.6.7, ui-components §4.3, version-matrix §5.2.

### D-09 프리미티브 엔진과 React 범위
- 결정: overlay(Dialog/AlertDialog/Popover/Tooltip/Tabs)는 `@base-ui/react`; 비-overlay(Button/Checkbox/Input/Separator/Badge)는 native 우선 + `useRender`로 `render` 합성 지원. `@kor-travel/ui`는 **React 19 전용**(ref prop, forwardRef 없음). React 18 앱(geo, ktdm)은 tokens부터 채택하고 React 19 업그레이드 후 ui 채택.
- Button 계약: `type="button"` 명시 기본, `loading` = `aria-disabled`+`aria-busy`+spinner+포커스 유지(map 의미), `disabled`는 native, root opacity 금지(라벨 래퍼 흐림), variant 7종·size 4+icon.
- 대안: radix(변경 파일 12 vs base-ui 29), React 18 동시 지원(forwardRef 유지 비용).
- 근거: ui-components §3.1·§5.
- 열림: base-ui Button `type` 기본값·Checkbox hidden input·Toast API(미확인) → 구현 task에서 소스 확인.

### D-10 UI 배포 방식
- 결정: npm 패키지(ESM + d.ts + Tailwind 소스 클래스; 소비자는 `@source "../node_modules/@kor-travel/ui"` 등록 + `@kor-travel/tokens/theme.css`)를 1차. shadcn 레지스트리(`registry.json`)는 2차 선택(복사 소유가 필요한 앱용). 토큰 이름은 클래스에 공통 이름(`bg-surface-page`, `h-control`) 사용, 앱은 `theme.css`가 제공하는 별칭으로 정합.
- 근거: ui-components §6.2·6.3, 선행 §7.3(`@source`).

### D-11 npm 배포 채널
- 결정: **GitHub Release tarball**(태그 `tokens-vX.Y.Z`, `ui-vX.Y.Z`, `config-vX.Y.Z`; 자산 `kor-travel-<pkg>-X.Y.Z.tgz`)을 URL로 설치, lockfile `integrity`로 고정. package.json `name`은 `@kor-travel/<pkg>`로 두어 npm org 확보 시 이름 변경 없이 publish. Python은 `git+https://github.com/digitie/kor-travel-common.git@py-vX.Y.Z#subdirectory=packages/py/kor-travel-common`(lock에 sha).
- 대안: GitHub Packages(설치 인증 필요), 공개 npm(`@kor-travel` org 존재 여부 미확인 — 403; 사용자 확인 필요), git URL + prepare(모노레포 subpath 불편).
- 근거: backend §5.2(git+sha 관례), 선행 §8.
- 열림: npm org `kor-travel` 생성 가능 여부(사용자 계정 작업).

### D-12 토큰 접두·계층·프로필
- 결정: 접두 `--kt-*`(전 저장소 0회). 계층 semantic ← app override(2단). shadcn alias 의미 고정(`--input`=control-line, `--accent`=brand-tint). 프로필 `admin`(6/8, 36/30, 15px, 7단)·`consumer`(8/14/20/32, 44px, 16px). 오버라이드 허용 목록: brand 4 + focus + paper 4 + ink 4(hue) — 형태·타입·모션은 프로필로만. 다크: 모든 semantic은 `.dark` 값 필수(map 기본 제공), 활성화는 앱 선택, 토글 없는 앱은 `color-scheme: light`.
- 근거: design-tokens §3.6.
- 결과: concierge `--ktc-*` 125회는 `--kt-*` 오버라이드 + 앱 접두 확장(`--ktc-shell-*`)으로 이관.
- 열림: 마커 팔레트 P-01~16 hex 정본(map Tableau vs pinvi Material) — common 범위 밖, map 소유로 확정 요청.

### D-13 UX 가이드·PC/Mobile 규약
- 결정: ux-patterns §2 G0~G9를 `docs/standards/ux-guide.md`(admin 장 + 사용자 표면 장 분리), §3을 `docs/standards/responsive-web.md`(admin=PC-first+최소 모바일 보장 ≥320px, 사용자 웹=mobile-first, breakpoint sm640/md768/lg1024/xl1280, 검사 폭 320/375/414/768/1024/1440, 터치 타깃 admin 24/36 · 사용자 44 · 모바일 48). 충돌 §4 C1~C22는 제안대로(4rem rail, 1024 전환, strip 기본+drawer 옵션, 동사 라벨 확인 다이얼로그·`window.confirm` 금지, 성공 토스트 정책 통일·엔진 앱 선택, 5-tone 상태, Pretendard 1순위 스택·로딩 앱 책임, light 기본).
- 열림: dirty 이탈 경고 정책(Q2), pinvi 44px 예외 2페이지(Q3), Hallmark 스탬프 형식(Q7), 규칙 ID 체계(Q9 — common 규칙 ID `UX-Gn.m` 신규 발급, 앱 M/C 번호는 출처 인용).

## C. 백엔드·API

### D-14 OpenAPI/REST 규약
- 결정: openapi §3 MUST(M1~M9)/SHOULD(S1~S13)/MUST NOT(N1~N8)을 `docs/standards/openapi.md`로 채택. 예외 레지스트리: geo v1(VWorld 호환), geo v2 envelope(`query_id`↔`request_id` 대응), pinvi 모바일 고정 계약(`{error:{}}`, 정수 If-Match)은 v2 prefix 시점에 묶음. 검증 오류 상태는 422 기본, geo 400 예외. 429 코드는 `TOO_MANY_REQUESTS`(map) 채택하고 상태→코드 사전은 common 소유·앱 덮어쓰기 허용. `X-Request-ID`는 형식 검증 통과 시 echo, `trust_incoming=False` 옵션(ktdm).
- 근거: openapi §3·§4·§6.

### D-15 Python 공통 모듈 우선순위
- 결정: 1차 health·openapi export·time·quality(C4·C12·C13·C20) → 2차 settings·db·public_api_key·metrics(C1·C9·C7·C3) → 3차 logging·errors/problem·testing·dagster·http·security_headers·cors·trusted_proxy·alembic 템플릿 → 보류 pagination·geo_primitives·cli.mutex·backup spec. 메트릭 접두 `kt<x>_`(geo 선례); map·pinvi 변경은 대시보드 영향 평가 후.
- 근거: backend §3·§4·§7.
- 결과: 인증(비밀번호·세션·CSRF·JWT)은 범위 밖 유지(선행 §3.6).

### D-16 소비자 첫 대상과 순서
- 결정: 토큰·UI 1차 공동 소비자 = **map admin + pinvi admin**(이식 관계 명시, 선행 §1). 2순위 concierge(map 계열 계약 동일), airport(WIP 병합 후). geo·ktdm은 React 19 선행 후. weather는 Tailwind v4 전환과 동시에 셸 교체. Python 1차 = map-api·weather-api·airport(problem+json 이미 근접), 2차 geo v2/admin, 3차 pinvi·concierge·ktdm(breaking 묶음).
- 근거: ui-components §4, openapi §4, 선행 §10 단계.

## D. 라이선스·운영

### D-17 라이선스
- 결정: common = GPL-3.0-or-later(LICENSE 존재). 추출 원본이 GPL(geo/map/weather/airport)이면 그대로, MIT(concierge/ktdm)이면 MIT 고지 보존 후 GPL 결합, pinvi(LICENSE 없음)는 **LICENSE 추가 전 코드 추출 보류**. 서드파티(shadcn·base-ui·radix MIT, tw-animate-css MIT, Pretendard OFL)는 NOTICE에 고지. 소비 앱(MIT/미표기)이 GPL 라이브러리를 사용하는 조건은 licensing 조사 결과로 확정(작성 중).
- 열림: licensing.md 결론 반영.

### D-18 CI·릴리스
- 결정: common CI = docs 검증(link·plan) + 패키지 빌드/테스트/`npm pack` 설치 스모크 + kt-contrast + check_versions(보고). 재사용 워크플로 제공: `openapi-drift.yml`, `typegen-drift.yml`, `node-quality.yml`, `python-quality.yml`, `docs-links.yml`. 릴리스: 패키지별 태그, CHANGELOG `[Unreleased]`→버전 절, 소비자 스모크(map·pinvi PR) 후 정식.
- 열림: ci-deploy.md 결론(포트·서비스명 표준) 반영.

## E. 통합 계획 단계(초안)
- Phase 0(현재 PR): 저장소 골격, 조사, 규칙 초안, ADR, 계획, task.
- Phase 1(T-0xx/T-1xx): versions.json·check_versions·config 패키지·재사용 워크플로; tokens 패키지 + kt-contrast; map·pinvi admin 토큰 채택; airport WIP 병합·토큰 정렬.
- Phase 2(T-2xx): ui 1차(소형) → map·pinvi·concierge; ui 2차(Button·overlay·Table·DataTable·Pager) → 동일 3앱.
- Phase 3(T-3xx): py 1차(health·openapi·time·quality) → map-api·weather-api·airport; 2차(settings·db·api key·metrics); 3차(problem·request-id·envelope) → geo v2/admin.
- Phase 4(T-4xx): 앱별 정렬·전환 — weather(v4·Next16·Vitest4·셸), ktdm(Next16·React19·ESLint10·v4 정리·uv), geo(React19·base-ui·@config 제거·uv), concierge(@config 정리·uv·CI 신설·`--kt-` 이관), airport(TS5.9·ESLint·CI drift·admin 정의), pinvi(admin `--kt-` 매핑·export·CI drift), 공통(lockfile·Node22 CI·Actions v7).
- Phase 5(T-5xx): 릴리스 운영, 분기별 drift 감사(cross-repo), renovate/dependabot, 회수 측정(선행 §11 지표).

## F. 인벤토리에서 추가 확인된 사실과 보정(coordinator 메모)

- airport "Admin"의 실체: 별도 admin 앱·로그인 없음. 운영 UI = 대시보드 안 무인증 백업 패널 + `/v1/admin/*`(ADR-003 무인증 의도). → D-16 보정: airport 1차 채택 범위는 tokens + 소형 컴포넌트(StatStrip·SectionCard·EmptyState·Alert)이며 AdminShell/LoginForm 소비는 T-035 라우트 분리 이후로. 사용자 확인 필요(열림).
- map은 `next 16.2.12` exact + npm 12.0.1 exact + Node 22.23.1 + `tests/unit/test_frontend_dependency_security.py`가 Dockerfile/CI 명령 순서·overrides를 잠금. → 기준선 상향 PR은 map의 lock 갱신·테스트 상수 갱신을 동반해야 함(T-41x에 명시).
- 헤더 명명: map `X-Kor-Travel-Map-*`(풀네임) vs geo `X-KTG-*`(약어). → D-14 보정: 헤더 접두는 앱 식별자로 두되 **형식 규칙**(`X-<AppId>-Api-Key|Service-Token|Actor|Admin-Proxy-Secret|Ops-Token`)만 공통, AppId는 저장소 identity 표 소유. 메트릭 접두는 `kt<x>_`(ktc/ktdm/ktg/ktw 선례) 권장, map `kor_travel_map_`·pinvi `pinvi_api_`는 대시보드 영향 평가 후 이관(P2).
- concierge: `.github` 없음, pyproject/lock 없음, ruff/mypy 설정 없음, `ReviewWorkspace.tsx` 4,386줄. → T-45x는 (1) uv/pyproject 도입 (2) CI 신설 (3) 공통 quality 프리셋 도입(위반은 baseline 허용 목록으로 시작) 순서.
- docker-manager: systemd + venv + rsync 배포(컨테이너 아님), Next 14/React 18 유지 사유 문서 없음, poetry 선언 + lock 없음, `ruff format` 전체 실행 금지 관례. → T-47x는 대규모 재포맷 PR을 별도로 분리하고 포맷터 통일은 "신규/변경 파일만" 정책으로 시작.
- weather: Tailwind 부재, 2,495행 CSS·170 클래스·13 TSX·220 className 속성. 예상 처리: preflight 대체 10%, common 컴포넌트 대체 40~48%, 반응형 유틸 흡수 9%, 도메인 CSS 잔존 32~35%. `@tanstack/react-query` 미사용 선언. → T-46x 규모 근거.
- pinvi: 두 UI 스택(사용자 수제 44px vs admin KTM 이식 36px) + ESLint 경계 강제; `[data-pv-surface='admin']` 변수 가리기; Next 16 + webpack 강제(Turbopack이 vworld-map-web 청크 파손, ADR-066); LICENSE 없음·README "비공개" vs AGENTS "공개" 상충; 자체 OpenAPI export 없음. → common UI는 admin 표면 스코프에만, 패키지는 webpack/Turbopack 양쪽 검증 task 포함.
- geo: `radix-ui` 통합 패키지, `<Button asChild>` 12곳 + `*Trigger asChild` 5곳, VirtualTable 13 소비 파일(as="table" 26회), Toast 스토어 소비 0. `tailwind.config.ts` raw hex와 `@theme` 이중 정의(우선순위 미확인). ADR-019(Next 16 보안 floor, React 18 유지 명시). → T-44x: React 19 업그레이드 ADR 갱신 + base-ui 이관 + @config 제거 + VirtualTable→DataTable은 별도 결정(검색 툴바·rowHeader 흡수 여부).
- 공유 라이브러리 중복: weather `lib/vworld-style.ts`·`vworld-map-view.tsx`와 map `src/lib/vworld-style.ts`, pinvi vendored `vworld-map-*.tgz`, geo만 `maplibre-vworld-react` 소비. `python-airkorea-api`가 weather vendored path + map git+sha 이중 경로. → common 범위 밖이나 통합 계획에 "공유 라이브러리 배포 정책(npm/PyPI 미발행 상태 정리)" task를 둠(T-5xx).
- 마커 팔레트 P-01~16: map(Tableau) vs pinvi(Material) hex 상이 — 데이터 소유자(map) 정본 확정 task를 계획에 포함(common 소유 아님).
- 문서 검증 도구: canview `validate_document_links.py`는 절대 접두(`F:/dev/...`)를 허용하나 common은 상대 링크만 허용(절대 링크 오류 처리)로 변경(docs-conventions C11).
