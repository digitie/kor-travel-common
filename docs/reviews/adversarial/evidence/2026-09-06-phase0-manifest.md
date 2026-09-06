# Phase 0 독립 적대적 리뷰 공통 manifest

- Review ID: 2026-09-06-phase0
- Candidate: `d3712a8c965c3193a5af13cacd6d22c603e0cfe4`
- Base: `b92fabe` (PR #1의 main 기준선)
- Parent: `09104ed0fa7f8564936fbbc3b9c17057f86d3e7c`
- 사용자 요청: 로컬 Claude 작업과 PR #1 통합·업무 계획·문서 인계 마무리, 불확실한 주장 직접 검증, 전문 영역 2인 적대적 리뷰, draft PR·주기적 push, 순차 실행 task.
- 범위: PR #1 전체 문서·ADR·standards·task·템플릿·도구·테스트·CI. 초안의 코드·정본 충돌·숨은 선행·외부 승인·출처·미실행 성공 처리를 공격한다.
- 범위 밖: 소비자 저장소 수정, 패키지 구현·실제 배포·라이선스 승인. 조사 스냅샷 전면 재조사는 하지 않고 finding에 필요한 근거만 확인한다.
- 기준 정본: `AGENTS.md`, `docs/README.md`, `docs/architecture/README.md`, 관련 accepted ADR·standards, `docs/tasks-rule.md`, `docs/tasks/T-013-plan-handoff-closure.md`, `docs/runbooks/agent-workflow.md` §5, 리뷰 template.
- 수용 기준: 원장·상세 일치와 실행 가능한 순서, 후보·미확인·실패와 성공의 구분, 소비자 코드·계약·권리 경계 보존, 모든 필수 gate 추적, 실제 도구가 문서 계약과 일치, 두 독립 원본·post-fix 재확인.
- 실행 가능: Python 문서 링크·plan·전체 unittest·git diff --check. 스코프에 맞는 공격 fixture 추가 실행은 임시 디렉터리에서 가능하다. 실물 패키지·소비자 빌드/e2e는 NOT_RUN(이번 기준선에 패키지 없음).
- 격리: reviewer별 detached worktree `review-phase0-a`·`review-phase0-b`. 시작·종료 HEAD와 clean 상태를 기록한다. main checkout 작업 상태를 candidate로 읽지 않는다.
- Reviewer A 전문 영역: Python 도구·버전 판정·입력 오류·CI 및 실패 시 gate 무결성.
- Reviewer B 전문 영역: 계획 DAG·순차 인계·UI/Python 계약·출처·외부 승인·정본 충돌.

## 두 리뷰어에게 전달한 공통 요청

위 immutable candidate와 base를 확인한 뒤 전문 영역에서 독립 적대적 리뷰한다. 상대 reviewer 결과를 요청하거나 읽지 않는다. 기존 작성자·테스트 성공·accepted 표기만으로 신뢰하지 않는다. 정상 경로뿐 아니라 오입력·누락·실패·잘못된 순서·외부 승인 없이 실행할 때의 문제를 찾는다. finding마다 ID(A/B-Pn-NN), 위치, 근거, 재현 또는 실패 시나리오, 영향, 최소 수정 권고를 기록한다. 취향이나 미래 구현 자체의 부재는 finding으로 만들지 않으며 부재를 성공으로 표시하거나 실행 계획이 막히는 경우는 finding이다.

원본 보고서는 reviewer별 evidence 파일 하나에만 작성한다. 실행 ID·전문 영역·시작/종료 시각·실제 hash·clean 검증·검토 범위·실행한 명령/결과·NOT_RUN·공격한 시나리오·남은 불확실성·최종 verdict(BLOCK/CONDITIONAL/PASS)를 포함한다. 코드·정책 파일은 수정하지 않는다. 자신의 원본이 확정되기 전 다른 reviewer에게 finding을 전달하지 않는다.
