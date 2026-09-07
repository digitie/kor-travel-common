# kor-travel-common 완료 task archive

완료·종료 task를 newest-first로 이동해 기록한다. 요약 행의 형식은 [tasks-rule](tasks-rule.md) §4와 같은 5열이며 상세 파일은 `docs/tasks/`에 유지한다.

## 완료 목록

| ID | 상태 | 우선순위 | 작업 | 선행 |
|---|---|---:|---|---|
| [T-104](tasks/T-104-design-tokens-standard.md) | DONE | P0 | docs/standards/design-tokens.md 확정(패키지 실물과 대조·규칙 ID TK-n) | T-101 |
| [T-021](tasks/T-021-ktc-ktdm-license-l8.md) | DONE | P1 | ktc·ktdm 라이선스 정렬(L8) 결정 반영: 결정 기록·각 저장소 PR 요청 문서 | 없음 |
| [T-020](tasks/T-020-pinvi-license-l6.md) | DONE | P0 | pinvi 라이선스 결정(L6) 반영: 결정 기록·pinvi PR 요청 문서·common 소비 gate 해제 조건 | 없음 |
| [T-102](tasks/T-102-map-vocabulary-shim.md) | DONE | P0 | 레거시 어휘 별칭 shim `aliases/map-vocabulary.css`(map·weather·geo 공통 이름 → `--kt-*`) + weather `--rail`·font 오버라이드 예제 + 별칭 충돌 검사 스크립트 (2026-09-08, PR #15) | T-101 |
| [T-101](tasks/T-101-tokens-package.md) | DONE | P0 | packages/tokens(tokens.css map 값+.dark·theme.css `kt-`·shadcn.css·base.css·base.scoped.css·dark-class/media.css) + 생성물(tokens.json·tokens.ts·tailwind-preset.cjs; 정본 CSS) + 루트 npm workspace·lock + `npm pack` 설치 스모크 (2026-09-07, PR #12) | T-003, T-004 |
| [T-011](tasks/T-011-consumer-manifest-schema.md) | DONE | P1 | 소비자 매니페스트 스키마 `consumer-manifest.v1` + `tools/validate_manifest.py` + 7 소비자 초기 매니페스트 초안 | T-005, T-016 |
| [T-016](tasks/T-016-common-shared-systems-scope.md) | DONE | P0 | 공용 시스템 범위 재정의와 전체 계획 동기화 (2026-09-07, PR #9) | 없음 |
| [T-005c](tasks/T-005c-workflow-static-report.md) | DONE | P2 | workflow 고정 참조·CI Node 선언의 정적 보고 (2026-09-07, PR #8) | T-005, T-009 |
| [T-005b](tasks/T-005b-check-versions-poetry-requirements.md) | DONE | P2 | check_versions: `poetry.lock`·`requirements.txt` 파서 + `NO_LOCK` 보고 | T-005 |
| [T-005a](tasks/T-005a-check-versions-uv-lock.md) | DONE | P1 | check_versions: `uv.lock` 파서 | T-005 |
| [T-009](tasks/T-009-ci-hardening.md) | DONE | P1 | common CI 하드닝(permissions·concurrency·timeout·ubuntu-24.04·액션 SHA 핀)·`tools` windows 매트릭스·`secret-scan`·`check-versions(report)` job·branch protection 문서·redaction guard (2026-09-07, PR #5) | T-002, T-003 |
| [T-015](tasks/T-015-common-delivery-plan.md) | DONE | P0 | npm·PyPI 미게시와 common 구현·외부 릴리스 선행 분리 (2026-09-07, PR #4) | T-005 |
| [T-006](tasks/T-006-npm-scope-pypi-name.md) | DONE | P1 | 공개 registry 이름 확보 철회와 패키지 식별자 확정 (2026-09-07, PR #4) | T-015 |
| [T-005](tasks/T-005-versions-registry.md) | DONE | P0 | versions.json v1 + `tools/check_versions.py`(npm lock v3·report·판정 어휘) + `docs/standards/versions.md` + 7 소비자 현재값·예외 등록 (2026-09-07, PR #3) | 없음 |
| [T-003](tasks/T-003-notices-provenance-spdx.md) | DONE | P0 | 고지·출처 파일(NOTICE·THIRD_PARTY_NOTICES·LICENSES/·PROVENANCE·CONTRIBUTING)·SPDX 헤더 규약·tools/check_spdx.py (2026-09-07, PR #2) | 없음 |
| [T-013](tasks/T-013-plan-handoff-closure.md) | DONE | P0 | PR #1·로컬 초안 통합과 순차 실행 계획·인계 마무리 (2026-09-06, PR #1) | 없음 |
| [T-008](tasks/T-008-architecture-docs.md) | DONE | P0 | docs/architecture/*(README·packages·style-delivery·consumers·adoption-readiness)·`docs/integration-map.md` 초기판 (2026-09-06, PR #1) | 없음 |
| [T-007](tasks/T-007-runbooks-conventions-templates.md) | DONE | P0 | runbook 본문(agent-workflow·consumer-adoption·release)·`docs/standards/agent-conventions.md`·templates/ (2026-09-06, PR #1) | 없음 |
| [T-004](tasks/T-004-adr-index.md) | DONE | P0 | ADR-001~012 + `docs/adr/README.md` 단일 색인 (2026-09-06, PR #1) | 없음 |
| [T-002](tasks/T-002-doc-validators.md) | DONE | P0 | 문서 검증 도구 정정(절대 링크 금지·산문 오탐·Windows 동작·LF)·validator 회귀 테스트·docs.yml 정비 (2026-09-06, PR #1) | 없음 |
| [T-001](tasks/T-001-entry-docs.md) | DONE | P0 | 진입 문서·문서 지도·canview 대조표(AGENTS·CLAUDE·SKILL·README·docs/README·dev-environment·canview-checklist·PR 템플릿) (2026-09-06, PR #1) | 없음 |
