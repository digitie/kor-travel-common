# 배포 단위와 공개 계약

- 정본 지위: 배포 단위별 이름·경로·exports·peer·채널·소비자·공개 계약의 정본(초안). 확정 task: T-008(★이번 PR) → T-101(tokens)·T-201(ui)·T-302(py)에서 실물과 대조해 확정. 마지막 갱신: 2026-09-06.
- 근거: [브리프](../plan/design-brief.md) D-01·D-09·D-10·D-11·D-15·D-31·D-33, `docs/survey/cross/design-tokens.md` §3.6.3, `docs/survey/cross/ui-components.md` §4·§6.2, `docs/survey/cross/backend.md` §5.2·§5.3, `docs/survey/cross/licensing.md` §3.5.

이 문서는 [아키텍처 개요](README.md) §1의 배포 단위를 단위별로 펼친다. 값·파일의 정본은 각 패키지 실물이며, 여기에는 이름·경계·계약(SemVer 대상)만 둔다. "후보" 표기는 T-101·T-201·T-302에서 확정한다.

## 1. 요약표

| 배포 단위 | 이름 | 경로 | 채널·태그 | peer | 1차 소비자 |
|---|---|---|---|---|---|
| tokens | `@kor-travel/tokens`(잠정, O-5) | `packages/tokens` | GitHub Release `tokens-vX.Y.Z`, 자산 `kor-travel-tokens-X.Y.Z.tgz` + `SHA256SUMS` | 없음(`theme.css`는 소비자 Tailwind ≥4.3.0 빌드 컨텍스트 필요) | map·weather → pinvi admin(L6)·airport(WIP 병합 후) |
| ui | `@kor-travel/ui`(잠정, O-5) | `packages/ui` | `ui-vX.Y.Z`, 자산 `kor-travel-ui-X.Y.Z.tgz` + `SHA256SUMS` | `react`·`react-dom` `^19.0.0`, `@kor-travel/tokens`의 호환 minor 하나, `@base-ui/react` ≥1.6(권장 1.8), `@tanstack/react-table` ^8.21·`@tanstack/react-virtual` ^3.14(DataTable subpath만) | map·pinvi admin(L6) 또는 airport 소형 부품 |
| py | PyPI 이름 `kor-travel-common`, import `kortravelcommon` | `packages/py/kor-travel-common` | git 태그 `py-vX.Y.Z` + wheel 자산; 소비자는 `git+https://github.com/digitie/kor-travel-common.git@py-vX.Y.Z#subdirectory=packages/py/kor-travel-common`(lock sha) | `requires-python >=3.11`; core는 pydantic만, 나머지는 extras | map-api·weather-api·airport → geo → pinvi·concierge·ktdm(L8 후) |
| 규칙 문서 | `docs/standards/*` | `docs/standards` | common 태그와 동반(문서 자체는 버전 없음, 규칙 ID 불변) | — | 전 소비자 |
| 템플릿 | `templates/*` | `templates` | 복사 시점의 common 커밋을 앱이 기록 | — | 전 소비자 |
| 레지스트리·도구 | `versions.json`, `tools/*.py`, `.github/workflows/*.yml`(재사용) | 루트·`tools`·`.github/workflows` | 소비자 CI가 태그/SHA로 호출(`@main` 금지) | Python 3.11+ stdlib(Windows Tier 2) | 전 소비자 |

공개 npm/PyPI 게시와 Renovate는 Phase 5(T-507)에서 재평가한다. 전제는 common 저장소 공개(O-15).

## 2. `@kor-travel/tokens`

### 2.1 exports(후보, T-101 확정)

| subpath | 내용 | Tailwind 의존 |
|---|---|---|
| `.`(= `./tokens.css`) | `:root { --kt-* }` + `.dark { --kt-* }` 순수 CSS(값 정본) | 없음 |
| `./theme.css` | `@import "./tokens.css"` + `@theme inline`(`--color-kt-*`·`--spacing-kt-*`·`--radius-kt-*`·`--font-kt-*`·`--shadow-kt-*`·`--ease-kt-*`) + `@theme`(`--text-kt-*`) + `@utility duration-kt-*` | v4 |
| `./shadcn.css` | shadcn alias(`--background`…`--ring`, `--radius`) = `--kt-*` 참조, 의미 고정 | 없음 |
| `./base.css` | `:focus-visible` 단일 레시피, hairline 2종, reduced-motion(+스피너 예외), `button:not(:disabled){cursor:pointer}` | 없음 |
| `./base.scoped.css` | 위 base를 `[data-kt-surface]` 스코프로 한정한 변형 | 없음 |
| `./dark-class.css` / `./dark-media.css` | `@custom-variant dark (&:is(.dark *))` / `prefers-color-scheme` 래퍼 | v4 |
| `./aliases/map-vocabulary.css` | map·weather·geo 공통 레거시 이름 → `var(--kt-*)` shim(T-102) | 없음 |
| `./tokens.json` | DTCG 형식 생성물(의미 이름·값·프로필) | 없음 |
| `./tokens.ts` | TS 상수 생성물(ESM + d.ts) | 없음 |
| `./tailwind-preset.cjs` | Tailwind v3/NativeWind 4 preset 생성물(pinvi mobile 대비, O-8) | v3 |

파일별 소비 규칙은 [스타일 배포](style-delivery.md)가 정본이다.

### 2.2 공개 계약(SemVer 대상)

| 항목 | 파괴(0.x minor / 1.x major) | 비파괴(patch) |
|---|---|---|
| 토큰 이름·의미(`--kt-*` 역할 목록: surface 4·text 4(+strong)·icon·border·control-line·brand 4·focus·status 4+tint·overlay·radius 2·control 높이 2·rail·duration 2·ease 2·shadow 2·z 5·font 스택) | 이름 변경·삭제·의미 변경(폐기 시 1 minor alias 유지) | 이름 추가 |
| `kt-` 유틸리티 이름(`theme.css`가 정의하는 `--color-kt-*` 등) | 변경·삭제 | 추가 |
| 파일 경로(subpath) | 변경·삭제 | 추가 |
| shadcn alias 의미(`--input`=control-line, `--accent`=brand-tint, `--radius`=radius-control, `--border`=장식) | 의미 변경 | — |
| 프로필 이름(`admin`·`consumer`)과 admin 값 | 이름 변경, admin 값 변경 | consumer는 의미 이름만(값은 pinvi 소유) |
| 기본값(map 값)·`.dark` 값 | — (값 변경은 patch 허용) | 값 변경은 `CHANGELOG.md` 기재 + 소비자 6폭 시각 diff evidence(D-21) |
| 생성물(`tokens.json`·`tokens.ts`·`tailwind-preset.cjs`) 스키마 | 스키마 변경 | 값 동기화(빌드 diff 검사) |

### 2.3 라이선스·동봉

tarball에 `LICENSE`·`NOTICE`·`THIRD_PARTY_NOTICES.md` 동봉, `package.json` `license: "GPL-3.0-or-later"`(D-17, `lic` §3.5). 원천 값은 map `globals.css`이며 `PROVENANCE.md`에 기록한다.

## 3. `@kor-travel/ui`

### 3.1 구성(후보, T-201 확정)

- 형태: ESM + d.ts + Tailwind 소스 클래스(`kt-` 접두 유틸리티만), `'use client'`·`'use no memo'` 지시문 보존, `noUncheckedIndexedAccess: true` 타입 검사, 인라인 SVG 아이콘.
- exports: 루트 barrel + 컴포넌트 그룹별 subpath(예: `./button`, `./data-table`, `./cn`, `./overlay`). DataTable·Pager처럼 무거운 peer가 필요한 항목은 별도 subpath로 두어 루트 import가 `@tanstack/*`를 요구하지 않게 한다.
- `@kor-travel/ui/cn` = `clsx` + `extendTailwindMerge`(`kt-` 그룹 등록). `clsx`·`tailwind-merge`는 dependencies(peer 아님).
- 엔진: overlay(Dialog·AlertDialog·Popover·Tooltip·Tabs·Breadcrumb·HelpTip)만 `@base-ui/react`; 비-overlay(Button·Checkbox·Input·Textarea·NativeSelect·Separator·Badge)는 native 요소 + `useRender`로 `render` 합성 선택 지원(D-09).
- UI 0.1·0.2의 tokens peer는 모두 `~0.1.0`이다. 독립 패키지의 minor 번호를 일치시키지 않으며 변경은 [ADR-013](../adr/013-package-release-execution-contract.md)을 따른다. Base UI `useRender` helper는 0.1부터 peer·개발 의존에 필요하고 overlay 구현은 0.2에서 추가한다.
- 릴리스 단위: `v0.1.0` = 소형 13종(Badge·Skeleton·Separator·Card·Alert·Input·Textarea·NativeSelect·Field·EmptyState·SectionCard·FilterBar·StatStrip, T-203), `v0.2.0` = Button·AppErrorPanel·overlay 세트·Table·Checkbox·DataTable·Pager·CopyButton·JsonViewer·DetailList·StatusBadge·AdminPageHeader·AdminSkipLink·AdminRailGrid·Form*(T-205~T-210).
- 테스트 하네스: vitest + RTL + jsdom, axe opt-in, showcase 없음(consumer-smoke 대체, D-33).
- base-ui 미확인 3건(Button `type` 기본, Checkbox hidden input, Toast API)은 T-201에서 소스 확인 전 릴리스 금지.

### 3.2 공개 계약(SemVer 대상)

| 항목 | 내용 | 파괴 판정 |
|---|---|---|
| 마크업 계약 | data-slot·testid·heading 구조·sr-only 문구·geo e2e 셀렉터 대응 — 정본 [ui-contract](../standards/ui-contract.md) | 변경은 0.x minor(이관 절 필수) / 1.x major |
| prop 기본값 | Button `type="button"`; DataTable `manualSorting` 기본 `true`(map 호출부 무변경; pinvi `AdminTable` 어댑터가 `false` 명시), `enableSortingRemoval`·`initialSorting`·`rowTestId`·`containerTestId`·`stickyHeader`·`rowSelectionLabel`; Dialog `hasUnsavedInput`·`viewportProps` | 기본값 변경 = 파괴 |
| 정렬 모드·4상태 | DataTable loading/empty/error/data 계약, sr-only 로딩 문구 | 파괴 |
| variant·size 이름 | Button variant 7종(default/outline/secondary/ghost/destructive/destructive-solid/link), size 8종(default/sm/xs/lg/icon/icon-sm/icon-xs/icon-lg; xs·lg·icon-xs·icon-lg는 deprecated alias) | 삭제·의미 변경 = 파괴; deprecated alias는 1 minor 유지 |
| 키보드·포커스 동작 | overlay: Escape 닫기·초기 포커스·복원·trap; Tabs 화살표 이동; DataTable 정렬 헤더 Enter/Space; Checkbox Space; Button `loading` 시 포커스 유지(`aria-disabled`+`aria-busy`, `onClick` 차단, native disabled 안 걺), `disabled`=native + `disabledReason`→`title`, root opacity 금지 | 동작 변경 = 파괴 |
| CSS 클래스 | `kt-` 접두 유틸리티만 사용; 소비자 필수 2줄(`@import "@kor-travel/tokens/theme.css"` + `@source "../node_modules/@kor-travel/ui"`) | 필수 등록 방식 변경 = 파괴 |
| peer 범위 | React `^19.0.0`(ref prop, forwardRef 없음), tokens의 호환 minor 하나 | peer 상향 = minor(이관 절) |
| 앱 소유 | 토스트 엔진(정책 UX-G4.1만), 모달 엔진 선택, 셸 nav·RBAC, 검색 툴바·`rowHeader`(geo `VirtualTable` 잔류) | — |

React 18 앱(geo·ktdm)은 tokens부터 채택하고 React 19 업그레이드(T-443·T-470) 뒤 ui를 채택한다.

### 3.3 검증·동봉

common CI `packages` job: build → `npm pack` → tarball 설치 → webpack·Turbopack 양쪽 `next build` 스모크. tarball에 `LICENSE`·`NOTICE`·`THIRD_PARTY_NOTICES.md` 동봉(shadcn/ui MIT·@base-ui/react MIT·cva Apache-2.0 고지). `tools/ui_drift.py`(T-211)가 npm 소비자의 로컬 우회 패치를 탐지한다.

## 4. `kor-travel-common`(Python)

### 4.1 구성

| 항목 | 값 |
|---|---|
| 빌드 | hatchling, `requires-python >=3.11`(3.11 문법; PEP 695 미사용), `uv.lock` 커밋, CI `--locked` |
| core 의존 | stdlib + pydantic(C1 settings 도입 시 pydantic-settings 포함 여부는 T-302 확정). geo·map import-linter 계약과 정합 |
| extras | `[api]`(fastapi·starlette·prometheus-client; starlette 범위 미선언 + CI 0.4x/1.6 매트릭스), `[db]`(sqlalchemy; asyncpg/psycopg는 앱 선택), `[http]`(httpx·tenacity), `[dagster]`, `[testing]`(testcontainers·pytest 플러그인) |
| 모듈 우선순위 | 1차 C12 openapi·C4 health·C13 time·C20 quality → 2차 C1 settings·C9 db·C7 public_api_key·C2 request_id·C3 metrics → 3차 C5 errors/problem·C16 security_headers·C17 cors·C8 trusted_proxy·C11 testing·C10 alembic·C15 http·C18 dagster → 보류 C6 pagination·C14 geo_primitives·C19 cli.mutex·C21 백업 규약(D-15) |
| 메타데이터 | `license = "GPL-3.0-or-later"` + PEP 639 `license-files`(`LICENSE`·`NOTICE`·`THIRD_PARTY_NOTICES.md`) |

### 4.2 공개 계약(SemVer 대상)

| 항목 | 내용 | 파괴 판정 |
|---|---|---|
| 모듈 경로·시그니처 | `kortravelcommon.<module>` 공개 함수·클래스·pydantic 모델 필드 | 삭제·시그니처 변경 = 파괴 |
| CLI | openapi export `--check`·profile 콜백·결정적 직렬화(`sort_keys`·`indent=2`·`ensure_ascii=False`) | 인자·출력 형식 변경 = 파괴(산출물 diff를 만들면 map pin 갱신 PR 동반 없이 머지 금지, D-14) |
| health | `/health`(liveness)·`/readyz`·`/version`, 기존 경로 alias 옵션(geo `/v1/healthz` 무기한 예외) | 경로·상태 코드 변경 = 파괴 |
| ProblemDetail | `type`·`title`·`status`·`detail`·`code`·`request_id`·`errors[]{field,message}`; 429 코드 기본 `TOO_MANY_REQUESTS`(앱 덮어쓰기) | 필드 삭제·의미 변경 = 파괴; 필드 추가 = additive |
| request_id | `X-Request-ID` UUID v4/v7 또는 ULID, ≤128자 ASCII, 검증 실패 시 서버 발급, `trust_incoming` 옵션(ktdm `False`) | 형식 규칙 변경 = 파괴 |
| metrics | 표준 HTTP 3지표·라벨·미매칭 센티널·multiproc; 접두는 인자(신규 `kt<x>_`, map·pinvi 기한부 예외 D-22) | 지표 이름·라벨 변경 = 파괴 |
| quality 베이스 | ruff `extend` 베이스(`line-length=100`, `E,F,I,UP,B,ASYNC`), mypy strict 베이스, import-linter 계약 템플릿, pre-commit 템플릿; format 규칙 미포함 | 규칙 추가는 minor(앱 per-file-ignores baseline) |
| 인증 | 범위 밖(비밀번호·세션·CSRF·JWT·RBAC) | — |

### 4.3 검증·동봉

common CI `python-package` job: `uv build` → wheel 설치 → starlette 매트릭스 테스트. 릴리스는 wheel 자산과 git 태그를 병행하며 소비자는 lock sha로 고정한다(Docker 빌드 스테이지에 `git` 필요 — `be` §5.2 A 전제).

## 5. 규칙 문서(`docs/standards/*`)

| 문서 | 규칙 ID | 검사 도구 | 예외 형식 |
|---|---|---|---|
| [design-tokens](../standards/design-tokens.md) | TK-n | `tools/kt_contrast.py` | 앱 `contrast-baseline.json`(미달 쌍 + `until`) |
| [ux-guide](../standards/ux-guide.md) | UX-Gn.m(MUST/SHOULD) | `tools/ux_lint.py`(금지 7종 + `window.confirm`) | 앱 baseline(`ux_gate.baseline`) |
| [responsive-web](../standards/responsive-web.md) | — | `templates/playwright.baseline.ts` 6폭 | 앱 예외(pinvi admin 44px 2쪽 O-21) |
| [openapi](../standards/openapi.md) | M1~M9 / S1~S13 / N1~N8 | `openapi-drift.yml`·`typegen-drift.yml` | `docs/standards/openapi-exceptions.yaml` |
| [versions](../standards/versions.md) | 판정 어휘 `OK/BELOW_FLOOR/ABOVE_MAX/NOT_RECOMMENDED/NO_LOCK/NO_ENGINES/FLOATING_REF/BLOCKED/EXEMPT/EXEMPT_EXPIRED` | `tools/check_versions.py` | `versions.json` `exceptions[]`(`until` 필수) |
| [frontend-stack](../standards/frontend-stack.md) / [backend-stack](../standards/backend-stack.md) | — | `templates/eslint/*.mjs`, quality 베이스 | 앱 baseline |
| [ci-deploy](../standards/ci-deploy.md) | 하드닝·명명·포트 | 재사용 워크플로 selftest | 앱 예외(airport 14002) |
| [licensing](../standards/licensing.md) | SPDX 헤더·고지·추출 gate | `tools/check_spdx.py` | 없음(common 파일은 즉시 fail) |
| [agent-conventions](../standards/agent-conventions.md) | AGENTS 공통 절 A~I·원장 SHOULD | `validate_plan.py`·`validate_document_links.py` | 소비자 로컬 절 |

규칙 문서는 코드 링크가 아니므로 라이선스 정렬(L8) 전에도 참조할 수 있다. 규칙 ID는 재번호하지 않고 폐기 시 `deprecated`로 남긴다.

## 6. 템플릿·레지스트리·도구

| 항목 | 경로 | 소비 방식 | 소유 이전 |
|---|---|---|---|
| AGENTS 공통 절·CLAUDE 포인터·에이전트 설정 | `templates/AGENTS.common.md`·`templates/CLAUDE.pointer.md`·`templates/agent-config/*` | 복사 | 복사 후 앱 소유, drift는 분기 감사(T-506) |
| 소비자 PR 본문·채택 체크리스트 | `templates/consumer-pr.md`·`templates/consumer-adoption-checklist.md` | 복사 | 앱 PR |
| ESLint·tsconfig·postcss·components.json 조각 | `templates/eslint/*.mjs` 외(T-107) | 복사 | 앱 |
| dependabot | `templates/dependabot.yml` | 복사 | 앱(Renovate 미설치, O-18) |
| playwright 6폭 기준선 | `templates/playwright.baseline.ts`(T-108) | 복사 | 앱(evidence는 PR에만) |
| 레지스트리 | `versions.json`(schema `kor-travel-common.version-registry.v1`) | `check_versions` 입력 | common 소유(`enforce` 포함) |
| 매니페스트 스키마 | `kor-travel-common.consumer-manifest.v1`(T-011) | 소비자 `kor-travel-common.lock.json` | 소비자 파일, 스키마는 common |
| 도구 | `tools/check_versions.py`·`kt_contrast.py`·`ux_lint.py`·`validate_manifest.py`·`collect_manifests.py`·`check_spdx.py`·`ui_drift.py` | 재사용 워크플로 또는 체크아웃 fallback | common |
| 재사용 워크플로 | Phase 1 `versions-check`·`contrast-check`·`docs-check` → Phase 3 `openapi-drift`·`typegen-drift` → Phase 4 `node-quality`·`python-quality` | `uses: digitie/kor-travel-common/.github/workflows/<name>.yml@<tag|sha>` | common; job `name:` 입력 개방 |

도구는 Python 3.11+ stdlib에서 Windows에서도 동작해야 하며 CI `tools` job이 ubuntu+windows 매트릭스로 보증한다(D-03).

### Python 공개 import와 릴리스 경계

공개 경로 `kortravelcommon.health`·`request_id`·`metrics`는 내부 `api.*`의 얇은 facade다. T-302가 facade·extras import-linter 경계를 만들고 T-304·T-307이 실제 재수출을 완성한다. 최상위 import는 프레임워크를 eager import하지 않으며 core-only와 `[api]` wheel 설치를 별도 검증한다. 1차 모듈은 T-310의 0.1, T-306~T-308은 [T-311](../tasks/T-311-py-v0-2-0-release.md)의 0.2로 발행한다.
