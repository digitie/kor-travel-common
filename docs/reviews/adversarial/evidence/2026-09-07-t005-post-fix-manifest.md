# T-005 수정 후 독립 리뷰 manifest

- Candidate: `f0509970b291a4e1f30ac5499150953ca80ab447`.
- Base: `3bec3eb0d17b986a9140c4f8ba876beb596d560a`. 최초 candidate `409b95c692c073807906e2c1546f022c59a7499c`와 base의 트리는 동일하다.
- 범위: base부터 candidate까지 전체 delta와 자신의 최초 finding 재검증. 코드·회귀 시험·versions 규약·고정 입력 evidence를 대조한다.
- 정본: [T-005](../../../tasks/T-005-versions-registry.md), [versions](../../../standards/versions.md), [workflow](../../../runbooks/agent-workflow.md).
- 격리: 각자의 detached worktree에서 시작·종료 SHA 및 clean 확인. 두 수정 후 원본이 확정되기 전에는 상대의 새 결과를 공유하지 않는다.
- 영역: A는 npm 설치·이름·수치·런타임 범위, B는 정책·예외·차단·CLI·evidence. 두 reviewer 모두 전체 수정의 회귀를 확인한다.
- 실행: Python 3.11+ 전체 unittest, 자체 검사, SPDX, 문서 link/plan, base diff --check, 최초 실패 사례와 수정 경계 고장 주입. 115 tests 성공은 독립 검증을 생략하는 근거가 아니다.
- 입력: 최초 7개 소비자 고정 commit·48파일은 inputs.json에 있고, 수정 후 digest는 post-fix.json에 있다. 원본 보고는 덮어쓰지 않았다. 소비자 Git object는 읽기 전용이며 소비자 저장소에는 쓰지 않는다.
- 범위 밖: 제품·소비자 build/e2e/배포, npm·PyPI 게시, T-005a/b 파서 확장, T-009 전체 CI, 전체 SemVer 문법 구현. 실행하지 않은 항목은 NOT_RUN으로 기록한다.

## 공통 요청 원문

위 candidate/base에서 독립 full post-fix 적대적 리뷰를 수행한다. 자신의 최초 finding을 원 ID·심각도로 재판정하고 전체 수정의 누락·오탐·false OK·입력 오류·규범 불일치를 공격한다. 코드나 다른 작업자의 변경을 고치지 말고 지정한 새 reviewer 원본 파일만 작성한다. 실행 ID·시각·실제 SHA·clean·실행 명령과 결과·미검토·finding disposition·BLOCK/CONDITIONAL/PASS를 남긴다. 상대 reviewer의 새 결과는 읽지 않는다. 원본 마지막에는 개행 하나만 둔다.
