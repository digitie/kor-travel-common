# kor-travel-common 문서 지도

이 문서는 상세 문서를 고르는 단일 진입점이다. 현재 상태는 [resume](resume.md), 작업 범위는 [tasks](tasks.md), 배포 단위·의존 방향은 [architecture](architecture/README.md), 소비 저장소 전체가 따르는 규칙은 [standards](standards/README.md)가 각각 정본이다. 확정 task: T-001 · 마지막 갱신: 2026-09-06.

## 읽기 단계

| 단계 | 읽는 경우 | 문서 |
|---|---|---|
| 반드시 | 모든 저장소 작업 | `AGENTS.md`, 이 문서, `docs/resume.md`, 해당 task가 있으면 그 상세 파일 |
| 필요 시 | 변경 분야가 정해졌을 때 | 아래 분야별 인덱스와 관련 상세 문서 한두 개 |
| 특수 | 리뷰·과거 원인·결정 이력·근거 재검증·복구가 필요할 때 | `reviews/`, `journal.md`, 관련 ADR, `survey/`, failure patterns |

이미 task가 지정됐으면 `tasks.md` 전체를 읽지 않는다. task가 없는 문서·review 작업은 관련 runbook 또는 template을 진입점으로 삼는다. ADR·review·journal·survey는 기본 요구사항이 아니라 이력·근거 자료이므로 현재 작업과 직접 관련된 항목만 검색한다.

## 정본 관계

```text
AGENTS.md                     모든 작업의 규칙·금지선
└─ docs/README.md             문서 라우터
   ├─ architecture/           배포 단위·의존 방향·스타일 배포·소비자·채택 준비
   ├─ standards/              소비 저장소 전체가 따르는 공통 규칙(토큰·UX·반응형·스택·UI 계약·OpenAPI·CI·라이선스·버전·에이전트)
   ├─ survey/                 기준 커밋 고정 조사(근거, 규범 아님)
   ├─ plan/                   설계 브리프(결정 레지스터)·통합 계획(Phase·중단 조건)
   ├─ tasks.md + tasks/       실행 범위·수용 기준
   ├─ adr/                    구조적 결정과 변경 이력(단일 색인)
   ├─ runbooks/               반복 작업 절차
   └─ reviews/ + journal.md   감사·작업 이력
```

- architecture는 현재 구현이 따라야 할 설계(배포 단위·의존 방향·계약 위치)를 설명한다.
- standards는 소비 저장소 전체가 따르는 규칙을 규칙 ID와 MUST/SHOULD로 정의한다. 값이 machine-readable 파일(`packages/tokens/tokens.css`, `versions.json`, `standards/openapi-exceptions.yaml`)에 있으면 그 파일이 정본이고 문서는 의미와 불변 조건만 둔다. `openapi-exceptions.md`는 YAML에서 생성한 읽기 전용 검토 표다.
- ADR은 왜 그 설계를 선택했는지 기록하며, 뒤집을 때 이전 ADR을 삭제하지 않는다.
- task는 architecture·standards를 구현하는 원자 범위와 acceptance를 정의한다. task가 architecture를 재정의하지 않는다.
- review는 특정 commit/diff에 대한 역사 기록이다. finding을 반영해 architecture·standards·ADR·task를 갱신하되 과거 report를 현재 정본처럼 사용하지 않는다.
- runbook은 작업 방법만 설명하며 제품 설계를 결정하지 않는다.
- survey는 어느 커밋에서 무엇을 관찰했는지의 스냅샷이고, plan은 그 근거로 확정한 결정 레지스터와 순서다. 둘 다 규칙이 아니며 규칙은 standards·ADR에 옮겨 적는다.

## 아키텍처

먼저 [아키텍처 개요](architecture/README.md)를 읽고 필요한 문서만 선택한다.

| 관심사 | 상세 문서 |
|---|---|
| 배포 단위·의존 방향·경계·자체 툴체인 | [packages](architecture/packages.md) |
| 토큰·CSS·UI 패키지가 소비자에 닿는 방식(npm·`@source`·scoped) | [style delivery](architecture/style-delivery.md) |
| 소비자 7개·표면·첫 소비자 순서·외부 선행 | [consumers](architecture/consumers.md) |
| 소비자별 채택 gate 추적표 | [adoption readiness](architecture/adoption-readiness.md) |
| canview 항목별 채택·변형·제외 대조 | [canview checklist](architecture/canview-checklist.md) |
| 소비자별 현재 채택 버전(생성물, 수기 편집 금지) | [integration map](integration-map.md) |

## 규칙(standards)

먼저 [standards 색인](standards/README.md)에서 규칙 문서를 고른다. 규칙 문서는 실물 패키지와 대조해 확정하는 task가 남은 정본 초안이며 각 문서 머리에 그 상태를 적는다.

| 관심사 | 문서 | machine-readable 정본·검사 |
|---|---|---|
| 디자인 토큰·프로필·다크·대비·오버라이드 | [design tokens](standards/design-tokens.md) | `packages/tokens/tokens.css`, `tools/kt_contrast.py`, 앱 `contrast-baseline.json` |
| UX 규칙(셸·목록·상세·피드백·위험 작업·로그인) | [ux guide](standards/ux-guide.md) | `tools/ux_lint.py`, 앱 baseline |
| PC/Mobile Web·breakpoint·터치 타깃·검사 폭 | [responsive web](standards/responsive-web.md) | `templates/playwright.baseline.ts`(6폭 시각 기준선), e2e 320px 게이트 |
| 프론트엔드 스택·ESLint/tsconfig/postcss 조각 | [frontend stack](standards/frontend-stack.md) | `templates/eslint/*`, `tools/check_versions.py`, `node-quality.yml` |
| UI 마크업 계약·SemVer 0.x·이관 절 | [ui contract](standards/ui-contract.md) | `packages/ui` 단위 테스트, consumer-smoke, `tools/ui_drift.py` |
| OpenAPI/REST 3계층·헤더·health·예외 | [openapi](standards/openapi.md) | `standards/openapi-exceptions.yaml`, drift 워크플로 |
| Python 패키지 구조·extras·모듈 우선순위·품질 도구 | [backend stack](standards/backend-stack.md) | `packages/py/kor-travel-common` |
| CI·재사용 워크플로·포트·컨테이너 명명 | [ci-deploy](standards/ci-deploy.md) | `.github/workflows/*` |
| 라이선스·고지·SPDX 헤더·추출 규칙 | [licensing](standards/licensing.md) | `NOTICE`·`THIRD_PARTY_NOTICES.md`·`PROVENANCE.md`, `tools/check_spdx.py` |
| 라이브러리/플랫폼 버전 일치·판정 어휘·승격 | [versions](standards/versions.md) | `versions.json`, `tools/check_versions.py` |
| 소비자용 AGENTS 공통 절·CLAUDE 포인터·설정 템플릿 | [agent conventions](standards/agent-conventions.md) | `templates/*` |

## 개발환경·도구

| 상황 | 문서 |
|---|---|
| 정본 OS·경로 표기·임시 worktree 프로필·도구 설치·Windows Tier 2·검증 사다리 | [dev environment](dev-environment.md) |
| 문서·계획·버전 검사 도구의 실행과 회귀 시험 | [tools](../tools/README.md) |
| 소비자에 배포하는 설정 조각·PR 규격·체크리스트 | [templates](../templates/README.md) |

branch·PR·리뷰 절차는 dev-environment가 아니라 [agent workflow](runbooks/agent-workflow.md)에 둔다.

## 조사·계획

| 관심사 | 문서 |
|---|---|
| 조사 기준 커밋·문서 목록·읽는 순서·오기 정정(§6.2) | [survey README](survey/README.md) |
| 영역×앱 매트릭스·후보 판정·차단 항목·열린 결정 | [commonality matrix](survey/commonality-matrix.md) |
| 확정 결정 레지스터(D-xx)·열림(O-n)·파일 지도·ADR·task 목록 | [design brief](plan/design-brief.md) |
| Phase 0~5 목표·산출물·완료 기준·중단 조건 | [integration plan](plan/integration-plan.md) |

## 작업·운영·이력

| 목적 | 문서 | 읽는 시점 |
|---|---|---|
| 열린 작업 선택·의존성 | [tasks](tasks.md) | task를 선택하거나 gate를 볼 때 |
| task 작성 규칙 | [tasks rule](tasks-rule.md) | task 생성·완료 때 |
| 완료 task archive | [tasks done](tasks-done.md) | backlog 감사 때 |
| 반복 절차 색인 | [runbooks](runbooks/README.md) | 어느 절차 문서를 열지 고를 때 |
| 표준 개발·2인 리뷰·PR | [agent workflow](runbooks/agent-workflow.md) | 실제 변경을 시작·종료할 때 |
| 소비자에 패키지·규약 도입 | [consumer adoption](runbooks/consumer-adoption.md) | 소비자 PR을 만들 때 |
| 패키지·규약 버전 발행 | [release](runbooks/release.md) | rc·정식 태그를 만들 때 |
| 문서·journal·ADR 유지 | [documentation maintenance](runbooks/documentation-maintenance.md) | 기록을 갱신할 때 |
| 반복 실패 복구 | [failure patterns](runbooks/agent-failure-patterns.md) | 실패가 발생한 뒤 |
| 구조적 결정 | [ADR 색인](adr/README.md) | 기존 결정을 변경할 때 |
| 적대적 리뷰 이력 | [review archive](reviews/README.md) | 리뷰 수행·finding 추적 때 |
| 작업 이력 | [journal](journal.md) | 과거 원인을 추적할 때 |
| 소비자 가시 변경 | [CHANGELOG](../CHANGELOG.md) | 릴리스·규약 변경 때 |

## 탐색 규칙

1. 이 인덱스에서 분야를 고른다.
2. 상세 문서의 제목과 목차를 먼저 확인한다.
3. 필요한 절만 읽고 관련 식별자는 `rg`로 찾는다.
4. 링크가 배경 참고(survey·plan·review·journal)인지 규범 정본(standards·architecture·ADR·task)인지 문서 서두에서 확인한다.
5. 이동·이름 변경 뒤에는 모든 Markdown local link와 plain path reference를 검사한다(`python3 -B -X utf8 tools/validate_document_links.py`).
