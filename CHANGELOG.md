# CHANGELOG

이 문서는 소비자에게 보이는 변경(패키지 공개 API·CSS·규칙·템플릿)을 기록한다. 형식은 Keep a Changelog(`https://keepachangelog.com/ko/1.1.0/`)를 따르되 단일 파일 안에 패키지별 절(`tokens`/`ui`/`py`/`standards`)을 둔다(브리프 D-18·D-31). 릴리스 시 해당 패키지 절만 `## [<pkg>-vX.Y.Z] - YYYY-MM-DD`로 옮기고 나머지는 `[Unreleased]`에 남긴다. 절차는 [release runbook](docs/runbooks/release.md), 버전 규칙은 [versions](docs/standards/versions.md)가 정본이다. 내부 구현 일지는 [journal](docs/journal.md)에 둔다.

절 제목(`Added`/`Changed`/`Deprecated`/`Removed`/`Fixed`/`Security`/`Breaking`)은 영어, 항목 본문은 한국어다. 0.x minor의 파괴 변경(토큰 이름/의미·`data-slot`/`data-testid`·prop 기본값·정렬 모드·CSS 파일 경로)은 해당 패키지 절에 `#### Breaking`과 이관 절(전→후·alias 유지 기간)을 반드시 두고, patch에는 `Breaking`이 있을 수 없다(D-31).

## [Unreleased]

### tokens

#### Added

- `@kor-travel/tokens` 계약 초안: `--kt-*` 의미 토큰(surface 4·text 4·icon·border·control-line·brand 4·focus·status 4+tint·overlay·radius 2·control 2·rail·duration 2·ease 2·shadow 2·z 5·font 스택), admin/consumer 프로필, `.dark` 값 완비·활성화 opt-in, 대비 검사 규칙, 정본 `tokens.css`와 생성물(`tokens.json`·`tokens.ts`·`tailwind-preset.cjs`), 레거시 어휘 shim `aliases/map-vocabulary.css`. 패키지 실물은 T-101([design tokens](docs/standards/design-tokens.md)).

### ui

#### Added

- `@kor-travel/ui` 계약 초안: React 19 전용(peer `^19.0.0`), overlay만 `@base-ui/react`·비-overlay는 native + `useRender`, `kt-` 접두 유틸리티만 사용, Button·DataTable 계약(`manualSorting` 기본 `true`), 마크업 계약(`data-slot`·`data-testid`·heading·sr-only), `@kor-travel/ui/cn`. 패키지 실물은 T-201([ui contract](docs/standards/ui-contract.md)).

### py

#### Added

- `kor-travel-common`(import `kortravelcommon`) 구조 초안: hatchling, `requires-python >=3.11`, core는 stdlib+pydantic, extras `[api]`·`[db]`·`[dagster]`·`[testing]`·`[http]`, 모듈 우선순위(export CLI·health·time·quality → settings·db·request_id·metrics → errors·security_headers·cors·trusted_proxy·testing·alembic·http·dagster), 인증은 범위 밖. 패키지 실물은 T-302([backend stack](docs/standards/backend-stack.md)).

### standards

#### Added

- 규칙 문서 초안 9종(`docs/standards/`: design-tokens·ux-guide·responsive-web·frontend-stack·ui-contract·openapi·backend-stack·ci-deploy·licensing·versions·agent-conventions)과 예외 레지스트리 `openapi-exceptions.yaml`.
- 버전 레지스트리 `versions.json` v1(floor/recommended/exceptions/blocked/enforce)과 `tools/check_versions.py` report 모드, 소비자 매니페스트 규약 `kor-travel-common.consumer-manifest.v1`.
- 소비자 배포 템플릿 `templates/`(AGENTS 공통 절·CLAUDE 포인터·consumer PR·채택 체크리스트·dependabot·ESLint 조각).
- 배포 채널·태그·SemVer 0.x 규칙, 소비자 채택·릴리스 runbook, 2인 독립 적대적 리뷰 gate, PR 본문 6항목 템플릿.
- 저장소 골격: canview 계층 문서(`AGENTS.md`→`docs/README.md`→`docs/resume.md`→task), ADR-001~012, 리뷰 archive, validator 2종(`validate_document_links`·`validate_plan`)과 회귀 테스트 40건, CI `docs` job.
- 고지·출처 파일: `NOTICE`, `THIRD_PARTY_NOTICES.md`, `PROVENANCE.md`, `CONTRIBUTING.md`(SPDX 헤더·AI 보조 생성물 조항).
