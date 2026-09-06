# kor-travel-common 공통 규칙(standards) 색인

- 정본 지위: 이 문서는 `docs/standards/` 규칙 문서의 **색인**이며 규범 본문을 갖지 않는다. 각 규칙의 정본은 아래 표의 문서다. 상위 문서 지도는 [docs/README.md](../README.md), 결정 배경은 [ADR 색인](../adr/README.md), 확정 결정 레지스터는 [설계 브리프](../plan/design-brief.md)다.
- 확정 task: 표의 "확정 task" 열. 마지막 갱신: 2026-09-06(브리프 확정판 기준 초안).

## 1. 이 디렉터리의 역할

`docs/standards/`는 소비 저장소 7곳(kor-travel-airport·concierge·docker-manager·geo·map·weather, pinvi)이 **공통으로 따라야 할 규칙**을 둔다([문서 유지보수 runbook](../runbooks/documentation-maintenance.md) §1). 특정 앱만의 예외는 각 규칙 문서가 지정한 예외 레지스트리 또는 소비자 매니페스트(`kor-travel-common.lock.json`, 브리프 D-19)에 두고, 조사 기록은 [`docs/survey/`](../survey/README.md)에 둔다. 조사는 근거이지 규칙이 아니다.

규칙 문서는 실물(패키지·도구·워크플로)보다 먼저 쓰인 **정본 초안**이며, 실물과 대조해 확정하는 task가 남아 있다(브리프 §7). 확정 전에도 신규 코드는 이 문서를 따르고, 실물과 문서가 어긋나면 문서를 고치는 PR이 실물 PR과 같은 리뷰 gate를 지난다.

## 2. 문서 목록

| 문서 | 한 줄 | 적용 대상 | 검증 수단 | 규칙 ID | 확정 task |
|---|---|---|---|---|---|
| [design-tokens.md](design-tokens.md) | `--kt-*` 토큰 계약: 정본 CSS·계층·역할·shadcn alias·프로필·오버라이드·다크·대비·값 형식·폰트·별칭 shim | tokens 소비 앱 전부(admin 6 + pinvi admin; consumer 프로필은 의미 이름만) | `tools/kt_contrast.py`(report + `contrast-baseline.json`), `packages/tokens` 생성물 diff | `TK-n` | T-104(선행 T-101) |
| [ux-guide.md](ux-guide.md) | UX 규칙 G0~G9(셸·목록·상세·피드백·상태·위험 작업·로그인·도움말·접근성), 충돌 결정 C1~C22, 금지 패턴, 위반 baseline | admin 표면 전부 + 사용자 표면 장 | `tools/ux_lint.py`(전체 report + `--base <sha>` diff fail), 2인 리뷰 | `UX-Gn.m` | T-105 |
| [responsive-web.md](responsive-web.md) | 표면 분류·breakpoint·검사 폭·터치·타이포 하한·안전영역·overflow·다크 기본·모바일 셸 | 전 앱(웹); 모바일 앱은 터치·안전영역만 | 6폭 시각 기준선(`templates/playwright.baseline.ts`), e2e 320px 게이트 | `RW-n` | T-106 |
| [frontend-stack.md](frontend-stack.md) | Next/React/TS/Tailwind/shadcn/base-ui/ESLint/Vitest/Playwright 표준 구성 파일·품질 게이트·`kt-`·`cn`·금지 사항 | 프론트엔드 앱 전부 | `tools/check_versions.py`, 재사용 워크플로 `node-quality.yml`, consumer-smoke | `FS-n` | T-107 |
| [ui-contract.md](ui-contract.md) | `@kor-travel/ui` 공개 계약: data-slot·testid·heading·sr-only·prop 기본값·geo/pinvi 대응·SemVer 0.x | ui 소비 앱(React 19) | `packages/ui` 단위 테스트, consumer-smoke, `tools/ui_drift.py` | `UC-n` | T-204(선행 T-203) |
| [openapi.md](openapi.md) | OpenAPI/REST 규약 3계층(MUST/SHOULD/MUST NOT)·헤더·`X-Request-ID`·health·export | 7개 FastAPI 백엔드 | `openapi-drift.yml`·`typegen-drift.yml`, 예외 레지스트리 | `M-n`/`S-n`/`N-n` | T-301 |
| [openapi-exceptions.yaml](openapi-exceptions.yaml) | OpenAPI 규약 예외 레지스트리(`{app, rule, surface, reason, sunset, review, owner}`) | 예외 보유 앱 | drift 워크플로가 읽음 | — | T-301 |
| [backend-stack.md](backend-stack.md) | Python 공통 패키지 구조·extras·3.11 호환·품질 도구 베이스·메트릭 접두 | 7개 백엔드 | `python-quality.yml`, `python-package` job | 문서 정의 | T-302 |
| [ci-deploy.md](ci-deploy.md) | common CI job·재사용 워크플로·릴리스·포트·명명·Dockerfile/compose 규약 | 전 저장소 | selftest·consumer-smoke | 문서 정의 | T-009·T-010 |
| [licensing.md](licensing.md) | GPL-3.0-or-later·고지 파일·SPDX 헤더·추출 gate | common + 이식 파일 전부 | `tools/check_spdx.py` | 문서 정의 | T-003 |
| [versions.md](versions.md) | 정렬 기준선(floor/recommended/exceptions)·핀 정책·판정 어휘·승격 권한 | 전 저장소 | `tools/check_versions.py` + `versions.json` | 문서 정의 | T-005 |
| [agent-conventions.md](agent-conventions.md) | 소비 저장소에 배포하는 AGENTS 공통 절·리뷰 gate·task 원장 SHOULD | 7개 저장소 | 문서 검증 | 문서 정의 | T-007 |

## 3. 규칙 수준 어휘

| 표기 | 뜻 | 위반 시 |
|---|---|---|
| **MUST** | 신규 코드는 예외 없이 따른다. 기존 잔존 위반은 앱별 baseline에 등록하고 신규 위반만 fail | diff-based fail(도구가 있을 때) 또는 리뷰 BLOCK |
| **SHOULD** | 따르는 것이 기본이며, 벗어날 때는 PR 본문 또는 예외 레지스트리에 사유·`until`을 적는다 | report 항목, 리뷰 finding P2/P3 |
| **MAY** | 허용 선택지 | — |
| **열림(O-n)** | 사용자 확인이 필요한 결정. 문서는 브리프 §2의 기본값을 적고 "열림(사용자 확인 필요)"으로 표시한다 | 기본값으로 진행 |

각 규칙 문서는 규칙마다 ID와 수준을 적는다. 사실(조사에서 확인)·후보(제안)·추정·미확인 구분은 조사 문서 표기 규약을 그대로 쓴다([survey README](../survey/README.md) 머리).

## 4. 강제 수준과 규칙 4축의 정본·검사·예외

강제 수준은 `report → warn → fail` 3단이며 승격은 common `versions.json`의 `consumers.<repo>.enforce`가 소유한다(브리프 D-07·D-30, [versions.md](versions.md)). 코드 규칙 게이트(`ux_lint`·`kt_contrast`)는 전체 report + diff-based fail이다.

| 축 | 정본 문서 | 검사 도구 | 예외·baseline 위치 |
|---|---|---|---|
| 색상 톤 | [design-tokens.md](design-tokens.md) | `tools/kt_contrast.py` | 앱 `contrast-baseline.json`(매니페스트 `contrast.baseline`) |
| UX | [ux-guide.md](ux-guide.md) | `tools/ux_lint.py` | 앱 baseline(매니페스트 `ux_gate.baseline`) |
| OpenAPI | [openapi.md](openapi.md) | `openapi-drift.yml`·`typegen-drift.yml` | [openapi-exceptions.yaml](openapi-exceptions.yaml) |
| PC/Mobile | [responsive-web.md](responsive-web.md) | 6폭 시각 기준선 + e2e | 각 문서의 예외 절 + 매니페스트 `exceptions[]` |

## 5. 작업별 읽기 순서

| 작업 | 먼저 읽는 문서 |
|---|---|
| 앱에 tokens 채택 | [design-tokens.md](design-tokens.md) → [responsive-web.md](responsive-web.md) §8 → [consumer adoption runbook](../runbooks/consumer-adoption.md) |
| 앱에 ui 채택 | [ui-contract.md](ui-contract.md) → [frontend-stack.md](frontend-stack.md) §4~§5 → [ux-guide.md](ux-guide.md) 해당 장 |
| 새 admin 화면 구현 | [ux-guide.md](ux-guide.md) → [responsive-web.md](responsive-web.md) → [ui-contract.md](ui-contract.md) 컴포넌트 표 |
| Tailwind v4 전환·프레임워크 업그레이드 | [frontend-stack.md](frontend-stack.md) → [versions.md](versions.md) → [통합 계획](../plan/integration-plan.md) |
| 백엔드 계약·모듈 | [openapi.md](openapi.md) → [backend-stack.md](backend-stack.md) |
| CI·릴리스·포트 | [ci-deploy.md](ci-deploy.md) → [release runbook](../runbooks/release.md) |
| 코드 이식·고지 | [licensing.md](licensing.md) |

## 6. 변경 규칙

- `docs/standards/*`는 리뷰 gate **비면제** 대상이다(브리프 D-04). 오탈자·동의 링크 수정만 면제이며 작성자가 아닌 merge 담당이 승인한다.
- 규칙이 바뀌면 같은 PR에서 `CHANGELOG.md`, 관련 [consumer adoption runbook](../runbooks/consumer-adoption.md) 절, 영향받는 ADR 상태를 갱신한다([문서 유지보수 runbook](../runbooks/documentation-maintenance.md) §2).
- 패키지 공개 계약(토큰 이름·의미, data-slot·testid, prop 기본값, CSS 파일 경로)을 바꾸는 규칙 변경은 [ui-contract.md](ui-contract.md) §9의 SemVer 0.x 파괴 항목 절차(rc → 소비자 PR 검증 → `### Breaking` + 이관 절)를 따른다.
- 같은 규범을 두 문서에 복제하지 않는다. 상위 문서는 한두 문장 요약 + 정본 링크만 둔다.
- 조사 문서(`docs/survey/`)의 오기 정정 값은 [survey README](../survey/README.md) §6.2를 따른다. 규칙 문서는 정정된 값을 인용한다.

## 7. 근거

- 파일 지도·소유자·확정 task: [설계 브리프](../plan/design-brief.md) §3·§6.
- 문서 종류별 책임: [문서 유지보수 runbook](../runbooks/documentation-maintenance.md) §1.
- 규칙 문서 후보 목록과 판정: [commonality-matrix](../survey/commonality-matrix.md) §2.5.
- canview 구조 모델(절 제목·규약 어휘): [canview 구조 체크리스트](../survey/cross/canview-structure-checklist.md) §2·§3.
