# kor-travel-common ADR — Architecture Decision Records

**다음 후보 번호는 ADR-017이다.**

- 정본 지위: ADR의 단일 색인. 별도 `docs/decisions.md`는 두지 않는다(D-02·D-27, 이중 색인 금지). 확정 task: T-004(★이번 PR). 마지막 갱신: 2026-09-06.

kor-travel-common의 구조적 결정은 파일당 하나의 ADR로 둔다. 파일명은 `NNN-<slug>.md`(3자리·소문자 kebab), H1은 `# ADR-NNN: 제목`, 머리 불릿에 `상태`·`날짜`가 필수이고 `근거 문서`·`Supersedes`는 선택이다. 본문 절은 컨텍스트 → 결정 → 대안 검토 → 결과 → 후속·적용 위치 순서다. 이 색인은 번호·제목·상태를 관리하며 상위 인덱스는 [문서 지도](../README.md)다.

## 규칙

1. 배포 단위·의존 방향·공개 계약·배포 채널·라이선스·저장소·문서 구조처럼 여러 소비 저장소에 영향을 주는 결정만 ADR로 기록한다. 결정의 근거는 [브리프](../plan/design-brief.md)의 결정 레지스터(D-xx)와 조사 문서 절을 인용한다.
2. 공통 정책은 `AGENTS.md`, 작업별 문서 선택은 `SKILL.md`, 공통 규칙 본문은 `docs/standards/`, task 규칙과 반복 절차는 `docs/tasks-rule.md`와 `docs/runbooks/`에 둔다. ADR은 "왜"와 "무엇을 대체했는가"만 답하고 현재 설계 전체를 복제하지 않는다.
3. 결정을 뒤집을 때는 새 ADR을 만들고 이전 ADR의 상태를 `superseded by ADR-XXX`(부분이면 `partially superseded by ADR-XXX`)로 바꾼다. ADR을 삭제하거나 본문을 다시 쓰지 않는다. 상태 뒤에 ` — ` 보충 문구를 둘 수 있다(예: 열린 결정 O-n 대기).
4. ADR 본문과 코드·규칙 문서·테스트는 같은 PR에서 동기화한다. 사용자 확인이 필요한 항목은 `proposed` 또는 상태 보충 문구로 남기고 기본값을 명시한다.
5. 다음 번호는 이 색인 표의 최댓값 + 1로 배정하고 이 문서 상단의 "다음 후보 번호"를 같은 PR에서 갱신한다.

## 목록

| ADR | 제목 | 상태 |
|-----|------|------|
| [ADR-001](001-purpose-boundary-and-deliverables.md) | kor-travel-common의 목적·경계·배포 단위 | partially superseded by ADR-015 |
| [ADR-002](002-canview-layered-docs-and-review-archive.md) | canview 계층형 문서 정보구조와 누적 독립 리뷰 아카이브 채택 | accepted |
| [ADR-003](003-linux-wsl-canonical-env-windows-tier2-worktree.md) | 개발 환경 정본(Linux/WSL)·Windows Tier 2·임시 worktree | partially superseded by ADR-016 |
| [ADR-004](004-gpl-3-0-or-later-and-provenance-gate.md) | 라이선스 GPL-3.0-or-later와 출처 고지·추출 gate | accepted |
| [ADR-005](005-release-channel-immutable-tags-semver-0x.md) | 배포 채널(GitHub Release tarball·git 태그·wheel)·태그 불변·SemVer 0.x | partially superseded by ADR-013, ADR-014 |
| [ADR-006](006-design-token-contract.md) | 디자인 토큰 계약(`--kt-*`·`kt-` 네임스페이스·계층·프로필·다크·대비·정본 CSS) | accepted — O-4(네임스페이스)·O-11(다크)·O-13(마커 정본)은 기본값으로 진행 |
| [ADR-007](007-react-ui-package-delivery.md) | React UI 패키지 배포 방식(npm 1차·React 19 전용·overlay base-ui/비-overlay native·마크업 계약·레지스트리 2차) | partially superseded by ADR-013 |
| [ADR-008](008-version-alignment-policy.md) | 라이브러리·플랫폼 버전 일치 정책(floor/recommended/exceptions·lockfile 의무·판정 어휘·승격 권한) | accepted — O-6·O-7·O-10·O-17·O-18은 기본값으로 진행 |
| [ADR-009](009-openapi-rest-conventions.md) | OpenAPI/REST 규약 3계층과 예외 레지스트리·health 경로 | accepted — O-14(429 코드명·geo v2 시점·pinvi Zod)는 기본값으로 진행 |
| [ADR-010](010-consumer-adoption-model.md) | 소비자 채택 모델(매니페스트·첫 소비자 순서·라이선스 gate·채택 PR 규격·시각 기준선·NOT_RUN) | partially superseded by ADR-013 |
| [ADR-011](011-python-common-package.md) | Python 공통 패키지 구조(extras·3.11 호환·모듈 우선순위·인증 범위 밖·메트릭 접두) | partially superseded by ADR-015 — O-7(앱 floor 3.12 시점)·O-12(메트릭 접두 map·pinvi)는 기본값으로 진행 |
| [ADR-012](012-tailwind-v4-migration-policy.md) | Tailwind v4 전환 정책(대상·순서·4단 PR·pinvi mobile 예외 보류) | proposed — O-8(pinvi mobile Tailwind 3 예외) 사용자 승인 대기; 나머지 항목은 기본값으로 진행 |
| [ADR-013](013-package-release-execution-contract.md) | 패키지 릴리스 순서·호환 범위·검증 소비자 계약 | partially superseded by ADR-014 |
| [ADR-014](014-common-implementation-without-registry-publishing.md) | npm·PyPI 미게시와 common 구현·외부 릴리스 분리 | accepted |
| [ADR-015](015-common-shared-systems-scope.md) | 공용 시스템 범위(위젯·토큰·코어 로직·로그인) | accepted |
| [ADR-016](016-mdx-parser-for-ux-lint.md) | UX 검사기의 MDX 문법 해석을 표준 파서에 위임 | accepted |
