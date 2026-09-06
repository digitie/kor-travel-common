# 열린 task 원장

이 원장은 열린 task의 요약·선행 관계를 관리한다. 수용 기준·외부 선행·검증·evidence는 상세 파일, 현재 다음 한 작업은 [resume](resume.md), 실행 선택과 단계별 출구는 [통합 계획](plan/integration-plan.md)이 정본이다. 작성 문법은 [task 규칙](tasks-rule.md)을 따른다.

총 96개의 상세 작업이 있다. 완료 6개는 완료 원장에 보존하고 열린 90개는 아래 표에서 관리한다. 패키지 실물·소비자 검증이 필요한 task는 해당 gate를 닫기 전 DONE으로 옮기지 않는다.

## 실행 대기열

T-013 문서·계획 인계를 마쳤다. 다음은 T-003 잔여(원문 고지·SPDX 검사), T-005 잔여(소비자 실제 현재값·보고), T-009(CI 하드닝) 순으로 한 작업씩 선택한다. 각 task의 선행·외부 선행 충족이 우선이며, 충족되지 않으면 BLOCKED 이유를 기록하고 독립적인 다음 항목으로 넘어간다.

그 이후 아래 표에서 모든 선행이 DONE인 항목만 선택한다. 기반 → 토큰 → UI → Python → 소비자 → 운영 분류 안에서 P0~P3 우선, 동순위는 ID 순이다. 외부 전용 T-006·T-014·T-020·T-021·T-430은 외부 evidence를 기다리고 common 구현을 막지 않는 다른 READY 항목을 진행한다. rc 검증·정식 채택 경계는 [통합 계획 §4](plan/integration-plan.md#4-rc-검증과-정식-채택)를 따른다.

완료 요약은 [완료 원장](tasks-done.md)에 보존한다. 선행 값의 정본은 아래 표와 상세 metadata이며, 브리프의 과거 task 목록은 최초 설계 근거다.

## 저장소 기반

| Task | 상태 | 우선순위 | 제목 | 선행 |
|---|---|---|---|---|
| [T-003](tasks/T-003-notices-provenance-spdx.md) | READY | P0 | 고지·출처 파일(NOTICE·THIRD_PARTY_NOTICES·LICENSES/·PROVENANCE·CONTRIBUTING)·SPDX 헤더 규약·tools/check_spdx.py | 없음 |
| [T-005](tasks/T-005-versions-registry.md) | READY | P0 | versions.json v1 + `tools/check_versions.py`(npm lock v3·report·판정 어휘) + `docs/standards/versions.md` + 7 소비자 현재값·예외 등록 | 없음 |
| [T-005a](tasks/T-005a-check-versions-uv-lock.md) | BLOCKED | P1 | check_versions: `uv.lock` 파서 | T-005 |
| [T-005b](tasks/T-005b-check-versions-poetry-requirements.md) | BLOCKED | P2 | check_versions: `poetry.lock`·`requirements.txt` 파서 + `NO_LOCK` 보고 | T-005 |
| [T-006](tasks/T-006-npm-scope-pypi-name.md) | BLOCKED | P1 | npm scope `@kor-travel`·PyPI 이름 가용성 확인·확보(사용자 계정 작업; 실패 시 개명) | 없음 |
| [T-009](tasks/T-009-ci-hardening.md) | READY | P1 | common CI 하드닝(permissions·concurrency·timeout·ubuntu-24.04·액션 SHA 핀)·`tools` windows 매트릭스·`secret-scan`·`check-versions(report)` job·branch protection 문서·redaction guard | T-002 |
| [T-010](tasks/T-010-reusable-workflows-stage1.md) | BLOCKED | P1 | 재사용 워크플로 1단계(`versions-check`·`contrast-check`·`docs-check`) + `workflows-selftest` fixture + `consumers.pins.json` + consumer-smoke | T-005, T-009, T-101, T-103 |
| [T-011](tasks/T-011-consumer-manifest-schema.md) | BLOCKED | P1 | 소비자 매니페스트 스키마 `consumer-manifest.v1` + `tools/validate_manifest.py` + 7 소비자 초기 매니페스트 초안 | T-005 |
| [T-012](tasks/T-012-collect-manifests.md) | BLOCKED | P2 | tools/collect_manifests.py → `docs/integration-map.md` 생성 + `docs/architecture/adoption-readiness.md` gate 표 갱신 | T-010, T-011 |
| [T-014](tasks/T-014-ports-130xx.md) | BLOCKED | P3 | common 포트 `130xx` 로컬 점유 확인·확정 + ktdm `docs/ports.md` sibling(airport 140xx·weather 141xx·common 130xx) 등록 요청 + `-latest` 접미 질의 | 없음 |
| [T-020](tasks/T-020-pinvi-license-l6.md) | BLOCKED | P0 | pinvi 라이선스 결정(L6) 반영: 결정 기록·pinvi PR 요청 문서·common 소비 gate 해제 조건 | 없음 |
| [T-021](tasks/T-021-ktc-ktdm-license-l8.md) | BLOCKED | P1 | ktc·ktdm 라이선스 정렬(L8) 결정 반영: 결정 기록·각 저장소 PR 요청 문서 | 없음 |

## 디자인 토큰

| Task | 상태 | 우선순위 | 제목 | 선행 |
|---|---|---|---|---|
| [T-101](tasks/T-101-tokens-package.md) | BLOCKED | P0 | packages/tokens(tokens.css map 값+.dark·theme.css `kt-`·shadcn.css·base.css·base.scoped.css·dark-class/media.css) + 생성물(tokens.json·tokens.ts·tailwind-preset.cjs; 정본 CSS) + 루트 npm workspace·lock + `npm pack` 설치 스모크 | T-003, T-004 |
| [T-102](tasks/T-102-map-vocabulary-shim.md) | BLOCKED | P0 | 레거시 어휘 별칭 shim `aliases/map-vocabulary.css`(map·weather·geo 공통 이름 → `--kt-*`) + weather `--rail`·font 오버라이드 예제 + 별칭 충돌 검사 스크립트 | T-101 |
| [T-103](tasks/T-103-kt-contrast-ux-lint.md) | BLOCKED | P1 | tools/kt_contrast.py(report·`contrast-baseline.json`) + `tools/ux_lint.py`(금지 7종+window.confirm, 전체 report·diff fail) + 4앱 오버라이드 예제 보고 | T-101 |
| [T-104](tasks/T-104-design-tokens-standard.md) | BLOCKED | P0 | docs/standards/design-tokens.md 확정(패키지 실물과 대조·규칙 ID TK-n) | T-101 |
| [T-105](tasks/T-105-ux-guide-standard.md) | READY | P1 | docs/standards/ux-guide.md 확정(UX-Gn.m·MUST/SHOULD·C1~C22·baseline·예외) | 없음 |
| [T-106](tasks/T-106-responsive-web-standard.md) | BLOCKED | P1 | docs/standards/responsive-web.md 확정 | T-108 |
| [T-107](tasks/T-107-frontend-stack-templates.md) | BLOCKED | P1 | docs/standards/frontend-stack.md 확정 + `templates/eslint/*.mjs`·tsconfig base·postcss·components.json 조각 | T-003 |
| [T-108](tasks/T-108-playwright-baseline.md) | READY | P1 | templates/playwright.baseline.ts(6폭 스크린샷) + 기준선 캡처 절차(consumer-adoption 절) | 없음 |
| [T-109](tasks/T-109-tokens-v0-1-0-release.md) | BLOCKED | P1 | tokens `v0.1.0-rc.1` → map·weather 검증 → `tokens-v0.1.0` 정식 + SHA256SUMS | T-101, T-102, T-103, T-104, T-010, T-108 |

## React UI

| Task | 상태 | 우선순위 | 제목 | 선행 |
|---|---|---|---|---|
| [T-201](tasks/T-201-ui-package-skeleton.md) | BLOCKED | P0 | packages/ui 골격(ESM·d.ts·subpath exports·`'use client'`/`'use no memo'` 보존·peer react ^19·인라인 아이콘·`cn` extendTailwindMerge·noUncheckedIndexedAccess) + base-ui 사실 확인 3건 기록 + pack 스모크(webpack/Turbopack) | T-109 |
| [T-203](tasks/T-203-ui-small-components.md) | BLOCKED | P0 | ui 1차 소형 13종(Badge·Skeleton·Separator·Card·Alert·Input·Textarea·NativeSelect·Field·EmptyState·SectionCard·FilterBar·StatStrip) + 단위 테스트(vitest+RTL+jsdom) | T-201 |
| [T-204](tasks/T-204-ui-contract-standard.md) | BLOCKED | P0 | docs/standards/ui-contract.md 확정(data-slot·testid·heading·sr-only·geo 셀렉터 대응·SemVer 0.x) | T-203 |
| [T-205](tasks/T-205-ui-button-error-panel.md) | BLOCKED | P1 | Button(D-09 계약)·AppErrorPanel·error-recovery | T-203, T-212 |
| [T-206](tasks/T-206-ui-overlay-table-checkbox.md) | BLOCKED | P1 | overlay 세트(Dialog(hasUnsavedInput·viewportProps)·AlertDialog·Popover·Tooltip·Tabs·Breadcrumb·HelpTip) + Table primitive + native Checkbox | T-205 |
| [T-208](tasks/T-208-ui-data-table-pager.md) | BLOCKED | P1 | DataTable(manualSorting 기본 true·removal·testid·sr-only·4상태) + OffsetPager/CursorPager | T-206 |
| [T-209](tasks/T-209-ui-copy-json-detail-status.md) | BLOCKED | P2 | CopyButton·JsonViewer·DetailList(`onNotify` 주입)·StatusBadge(사전 주입형) | T-206 |
| [T-210](tasks/T-210-ui-admin-header-form.md) | BLOCKED | P2 | AdminPageHeader·AdminSkipLink·AdminRailGrid + FormFieldInput/FormSelect/FormTextArea + form-validation(헤드리스) | T-206 |
| [T-211](tasks/T-211-ui-registry-channel-drift.md) | BLOCKED | P3 | 레지스트리 채널(셸 골격·로그인 페이지·playwright 기준선 템플릿) + `tools/ui_drift.py`(npm 소비자 로컬 패치 탐지) | T-210 |
| [T-212](tasks/T-212-ui-v0-1-0-release.md) | BLOCKED | P1 | ui `v0.1.0` rc → map + pinvi admin(L6) 또는 airport 검증 → 정식 | T-203, T-204 |
| [T-213](tasks/T-213-ui-v0-2-0-release.md) | BLOCKED | P1 | ui `v0.2.0`(Button·overlay·Table·DataTable·Pager·Copy/Json/Detail·Header/Form) rc → 정식 | T-208, T-209, T-210 |

## Python 공통

| Task | 상태 | 우선순위 | 제목 | 선행 |
|---|---|---|---|---|
| [T-301](tasks/T-301-openapi-standard.md) | READY | P0 | docs/standards/openapi.md 확정 + `openapi-exceptions.yaml` 초기 등록 + 헤더·X-Request-ID 형식 규칙 | 없음 |
| [T-302](tasks/T-302-python-package-skeleton.md) | BLOCKED | P0 | packages/py/kor-travel-common 골격(hatchling·extras·3.11 문법 검사·uv.lock·starlette 0.4x/1.6 CI 매트릭스) + `docs/standards/backend-stack.md` 확정 | T-003 |
| [T-303](tasks/T-303-openapi-export-cli.md) | BLOCKED | P0 | C12 openapi export CLI(`--check`·profile 콜백·결정적 직렬화) + typegen 규약 템플릿 | T-302 |
| [T-304](tasks/T-304-health-and-time.md) | BLOCKED | P1 | C4 health(`/health`·`/readyz`·`/version`·alias 옵션) + C13 time | T-302 |
| [T-305](tasks/T-305-quality-baseline.md) | BLOCKED | P1 | C20 quality 산출물(ruff extend·mypy·import-linter·pre-commit·CI 템플릿; format 미포함) + common 자기 적용 | T-302 |
| [T-306](tasks/T-306-settings-db-api-key.md) | BLOCKED | P1 | C1 settings 베이스 + C9 db 엔진 팩토리 + C7 public_api_key | T-304, T-310 |
| [T-307](tasks/T-307-request-id-and-metrics.md) | BLOCKED | P1 | C2 request_id(`trust_incoming`·형식 검증) + C3 metrics(표준 라벨·센티널·multiproc; 접두 인자) | T-304, T-310 |
| [T-308](tasks/T-308-api-third-tier-modules.md) | BLOCKED | P2 | C5 errors/problem(`exclude_paths`)·C16 security_headers·C17 cors·C8 trusted_proxy·C11 testing·C10 alembic 템플릿·C15 http·C18 dagster | T-306, T-307 |
| [T-309](tasks/T-309-openapi-typegen-drift-workflows.md) | BLOCKED | P1 | 재사용 워크플로 2단계(`openapi-drift.yml`·`typegen-drift.yml`) + selftest | T-303, T-010 |
| [T-310](tasks/T-310-py-v0-1-0-release.md) | BLOCKED | P1 | py-v0.1.0(1차) → weather-api·map-api·airport 검증 → 정식(wheel 자산) | T-303, T-304, T-305, T-309 |
| [T-311](tasks/T-311-py-v0-2-0-release.md) | BLOCKED | P1 | Python 0.2 모듈 rc 검증·wheel 발행 | T-308, T-309, T-310 |

## 소비자 이관

| Task | 상태 | 우선순위 | 제목 | 선행 |
|---|---|---|---|---|
| [T-401](tasks/T-401-reusable-workflows-quality.md) | BLOCKED | P1 | 재사용 워크플로 3단계(`node-quality.yml`·`python-quality.yml`) + selftest(concierge CI 신설용) | T-010 |
| [T-402](tasks/T-402-visual-baseline-capture.md) | BLOCKED | P2 | 7앱 시각 회귀 기준선 초기 캡처(앱별 evidence; 미실행 NOT_RUN) | T-108 |
| [T-403](tasks/T-403-consumer-ci-alignment.md) | BLOCKED | P1 | 공통 CI 정렬: Node 20→22(ktdm·geo·wx)·액션 SHA 핀·`check_versions` report job 삽입·매니페스트 커밋(7 저장소) | T-010, T-011 |
| [T-410](tasks/T-410-map-tokens-adoption.md) | BLOCKED | P0 | map: `globals.css` → `@import "@kor-travel/tokens"` + 빈 brand 오버라이드 + 매니페스트(값 diff 0) + LICENSE 전문 복원(L9)·`license` 필드 | T-109 |
| [T-411](tasks/T-411-map-ui-v01-shim.md) | BLOCKED | P1 | map: ui v0.1 소형 shim 채택 + `@source` + `verify:frontend-eslint` 집합 갱신 | T-212, T-410 |
| [T-412](tasks/T-412-map-ui-v02-adoption.md) | BLOCKED | P1 | map: ui v0.2 채택(Checkbox 호출부 3파일) + `data-table.test.tsx` 이관 + `ux_lint` report | T-213, T-411 |
| [T-413](tasks/T-413-map-framework-bump.md) | BLOCKED | P2 | map: Next 16.3·base-ui 1.8·Playwright 1.63 상향(`verify-next-sharp.mjs`·`test_frontend_dependency_security.py`·이미지 동반, 별도 PR) | T-005 |
| [T-420](tasks/T-420-pinvi-license-l6.md) | BLOCKED | P0 | pinvi: L6 결정 반영 PR(루트 LICENSE·README/AGENTS 정합·`apps/api` pyproject·maplibre 문서 정정) | T-020 |
| [T-421](tasks/T-421-pinvi-admin-tokens.md) | BLOCKED | P1 | pinvi: admin `--color-admin-*`→`--kt-*` 오버라이드 + `base.scoped.css` + 매니페스트(사용자 표면 무변경 e2e) | T-420, T-109 |
| [T-422](tasks/T-422-pinvi-admin-ui.md) | BLOCKED | P1 | pinvi: ui v0.1/v0.2 채택(`AdminTable` 어댑터 유지·`cn` 재수출·44px 예외 등록·webpack 빌드) | T-422a, T-422b |
| [T-422a](tasks/T-422a-pinvi-admin-ui-v01.md) | BLOCKED | P1 | pinvi admin UI 0.1 소형 부품 채택 | T-212, T-421 |
| [T-422b](tasks/T-422b-pinvi-admin-ui-v02.md) | BLOCKED | P1 | pinvi admin UI 0.2 부품 채택 | T-213, T-422a |
| [T-430](tasks/T-430-airport-wip-merge.md) | BLOCKED | P0 | airport: WIP `codex/shadcn-ui-foundation` 병합(값 유지·`cn`→clsx+twMerge·devDeps 이동·Button D-09 레시피) | 없음 |
| [T-431](tasks/T-431-airport-tokens-adoption.md) | BLOCKED | P1 | airport: tokens 채택(alias 재매핑 유지·`dark-media.css`·contrast baseline) + 매니페스트 | T-430, T-109 |
| [T-432](tasks/T-432-airport-small-ui.md) | BLOCKED | P2 | airport: 소형 ui 채택(백업·collector 패널: Alert·StatStrip·SectionCard·EmptyState) | T-431, T-212 |
| [T-433](tasks/T-433-airport-ts7-exception-hygiene.md) | BLOCKED | P2 | airport: TS 7 예외 등록·ESLint 도입 판정·절대 링크 상대화·prod placeholder 치환·`engines` 선언 | T-005 |
| [T-440](tasks/T-440-geo-node22-uvlock.md) | BLOCKED | P1 | geo: Node 22 CI + `uv.lock` 도입 + pre-commit rev 정렬 | T-005 |
| [T-441](tasks/T-441-geo-theme-unify-tokens.md) | BLOCKED | P1 | geo: `@config` 실효값 빌드 검증 → `@theme` 단일화·`tailwind.config.ts` 삭제 → tokens 채택(`--ui-*` 별칭 유지) + contrast baseline + 매니페스트 | T-109 |
| [T-443](tasks/T-443-geo-react19.md) | BLOCKED | P2 | geo: React 19 업그레이드(ADR-019 갱신, 별도 PR, 실검증) | T-440 |
| [T-444](tasks/T-444-geo-baseui-ui-v02.md) | BLOCKED | P2 | geo: radix→base-ui 이관(12파일·`asChild` 17곳) + ui v0.2 채택(셀렉터 diff evidence; VirtualTable 잔류) | T-443, T-441, T-213 |
| [T-450](tasks/T-450-concierge-pyproject-uvlock.md) | BLOCKED | P0 | concierge: `pyproject.toml`·`uv.lock`(`mcp<2` blocked)·ruff/mypy baseline 도입 | T-305 |
| [T-451](tasks/T-451-concierge-ci-dockerfile.md) | BLOCKED | P0 | concierge: CI 신설(재사용 워크플로 호출·versions-check) + production `frontend/Dockerfile` 정리 | T-401, T-450 |
| [T-453](tasks/T-453-concierge-theme-tokens.md) | BLOCKED | P1 | concierge: hex fallback 블록 제거 → `@config`→`@theme inline` → `--ktc-*`를 `--kt-*` 오버라이드로 + contrast baseline + 매니페스트 | T-451, T-109 |
| [T-454](tasks/T-454-concierge-ui-v02.md) | BLOCKED | P2 | concierge: ui v0.2 채택(18종 shim·base-ui 1.8·`render` 9줄) | T-021, T-453, T-213 |
| [T-460](tasks/T-460-weather-next16-vitest4-node22.md) | BLOCKED | P1 | weather: Next 16·Vitest 4·Node 22 CI·eslint-config-next 16·`moduleResolution: bundler`·react-query 미사용 정리·CI vitest/mypy 추가(별도 PR) | T-005 |
| [T-461](tasks/T-461-weather-tokens-css-swap.md) | BLOCKED | P0 | weather: `app/tokens.css` → `@kor-travel/tokens/tokens.css` + `aliases/map-vocabulary.css` + navy·`--rail`·font 오버라이드 + 매니페스트(6폭 diff 0 evidence) | T-109 |
| [T-462](tasks/T-462-weather-tailwind-v4-intro.md) | BLOCKED | P1 | weather: Tailwind v4 도입(theme+utilities, preflight 제외) + `@theme inline` 1:1 매핑 | T-460, T-461 |
| [T-463](tasks/T-463-weather-shell-panels-forms-login.md) | BLOCKED | P1 | weather: 셸/패널·표/폼·로그인 → common 컴포넌트 3분할 PR, 해당 CSS 절 삭제 | T-462, T-213 |
| [T-464](tasks/T-464-weather-preflight-domain-css.md) | BLOCKED | P2 | weather: preflight 활성화 + 잔존 도메인 CSS `@layer components` + 마커 색 토큰화 + 셸 문서-코드 불일치 해소 | T-463 |
| [T-470](tasks/T-470-ktdm-next16-react19-upgrade.md) | BLOCKED | P1 | ktdm: Next 16·React 19·ESLint 9·Node 22 CI 업그레이드(재포맷 금지, recharts 3·`target es5` 실검증, 별도 PR) | T-005 |
| [T-471](tasks/T-471-ktdm-poetry-to-uv.md) | BLOCKED | P1 | ktdm: Poetry→`uv.lock`·하한 상향·CI 핀 정리 + quality baseline | T-305 |
| [T-472](tasks/T-472-ktdm-tokens-adoption.md) | BLOCKED | P2 | ktdm: tokens 채택(`@theme`→`--kt-*`·Ember 값 유지·tint 4종) + contrast baseline + 매니페스트 | T-470, T-109 |
| [T-473](tasks/T-473-ktdm-ui-partial.md) | BLOCKED | P3 | ktdm: ui 부분 채택(StatStrip·AppErrorPanel·SectionCard; `ops-*` 잔존 허용) | T-021, T-472, T-213 |
| [T-480](tasks/T-480-map-api-py-first.md) | BLOCKED | P1 | map-api: py 1차 채택(export CLI·health·time·quality) + `type` URI·429 코드 정렬 + pinvi/ktdm pin 갱신 PR 동반 | T-310 |
| [T-481](tasks/T-481-weather-api-py-first.md) | BLOCKED | P1 | weather-api: py 1차 채택 + `--check` 전환 + airkorea 스냅샷 정본 결정(L15) + Python 3.11/3.12/3.13 정합 | T-310 |
| [T-482](tasks/T-482-airport-py-first.md) | BLOCKED | P1 | airport: py 1차 채택 + `code`/`request_id` additive + 스펙 422 정합 + `--check` CI + Docker `uv sync --locked` 정리 | T-310 |
| [T-483](tasks/T-483-geo-py-second.md) | BLOCKED | P2 | geo: py 2차(health alias 병행·securitySchemes+typegen 재생성·admin problem+json opt-in·request-id) | T-311, T-440 |
| [T-484](tasks/T-484-pinvi-py-lock-export-drift.md) | BLOCKED | P2 | pinvi: `uv.lock` CI·Docker 소비 + etl `@main` 제거 + export 파이프라인·drift CI + request-id(additive) | T-311, T-420 |
| [T-485](tasks/T-485-concierge-py-first.md) | BLOCKED | P2 | concierge: py 1차(export·request-id·quality) + features export 계약 문서화(map provider 동시 수정 계획) | T-451, T-311 |
| [T-486](tasks/T-486-ktdm-py-second.md) | BLOCKED | P3 | ktdm: py 2차(request-id `trust_incoming=False`·quality baseline) | T-471, T-311 |

## 운영·재평가

| Task | 상태 | 우선순위 | 제목 | 선행 |
|---|---|---|---|---|
| [T-501](tasks/T-501-release-runbook-rehearsal.md) | BLOCKED | P1 | 릴리스 runbook 1회 완주 검증(rc→소비자 PR→정식→되돌리기 리허설) | T-109, T-212 |
| [T-502](tasks/T-502-gate-promotion-enforce-fail.md) | BLOCKED | P2 | gate 승격: `check_versions`·`kt_contrast`·`ux_lint`를 소비자별 2회 green 후 `enforce: fail`(common PR) + 승격 절차 runbook | T-403, T-103 |
| [T-503](tasks/T-503-adoption-report-2026-q4.md) | BLOCKED | P2 | 회수 지표 1회차 보고 `docs/reports/adoption-2026-Q4.md` 정리 | T-411, T-461 |
| [T-505](tasks/T-505-shared-library-marker-palette-request.md) | BLOCKED | P3 | 공유 라이브러리·마커 팔레트 정본 결정 요청 문서(`maplibre-vworld-react` npm·`license`·`vworld-style.ts` 중복·airkorea 이중 경로·kma/kasi SHA·P-01~16 hex) | T-008 |
| [T-506](tasks/T-506-quarterly-drift-audit.md) | BLOCKED | P2 | 분기별 cross-repo drift 감사 runbook + 첫 실행 + 조사 기준 커밋 갱신 절 | T-012 |
| [T-507](tasks/T-507-reevaluate-publishing-and-baselines.md) | BLOCKED | P3 | 재평가: 공개 npm/PyPI 게시·Renovate·Vitest 5·Node 24/26·react-table 9·lucide 1.x·mypy 2·TS 7 → `versions.json` 갱신 | T-006, T-005 |
| [T-508](tasks/T-508-deferred-items-reevaluation.md) | BLOCKED | P3 | 보류 항목 재평가(api-client-core·pagination 코덱·VirtualTable 흡수·ConfirmDialog API·토스트·전면 레지스트리) | T-213, T-310 |
