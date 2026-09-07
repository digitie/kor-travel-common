# kor-travel-common 에이전트 운영 Runbook

이 디렉터리에는 반복 실행 절차만 둔다. 배포 단위·계약 설계는 [architecture](../architecture/README.md), 공통 규칙은 [standards](../standards/README.md), 작업 정본은 [tasks](../tasks.md)와 `docs/tasks/`, 전체 문서 선택은 [문서 지도](../README.md)를 따른다.

모든 runbook을 작업 시작 때 읽지 않는다. 현재 상황에 해당하는 문서만 연다.

| 문서 | 읽는 시점 | 책임 |
|---|---|---|
| [agent workflow](agent-workflow.md) | branch 생성, 구현 검증, 2인 리뷰, PR, merge를 수행할 때 | branch/worktree, CodeGraph, gate, 독립 적대적 리뷰, 보안 감사, 정리 |
| [documentation maintenance](documentation-maintenance.md) | 문서·ADR·task·review를 만들거나 이동할 때 | 정본 관계, 갱신 조건, 누적 기록, link 검증 |
| [consumer adoption](consumer-adoption.md) | 소비 저장소(kor-travel-*, pinvi)에 common 패키지·규약을 도입하거나 버전을 올릴 때 | 이관 순서, 검증 계층, 되돌리기, 소비자 PR 본문 |
| [branch protection](branch-protection.md) | required check·GitHub ruleset 설정을 검토할 때 | 실제 check 이름·PR 필수·linear history·변경 검증 |
| [release](release.md) | common 패키지·규약 버전을 발행할 때 | 버전 규칙, tarball 검증, 소비자 스모크, 기록 |
| [failure patterns](agent-failure-patterns.md) | 실제 실패를 분류하거나 반복을 막을 때 | 환경·패키징·스타일·소비자 통합 실패의 진단과 복구 |

새 반복 절차를 추가할 때 설계 결정이나 일회성 작업 로그를 이 디렉터리에 넣지 않는다. 설계 결정은 ADR, 현재 구조는 architecture, 일회성 결과는 task·review·journal에 둔다.
