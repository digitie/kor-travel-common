# T-015 수정 후 독립 리뷰 manifest

- Candidate: `ae86185ff103156ffd516b572cf97d401f4a3d31`.
- Base: `a28c2a726f6940bf9f287188b87b1d5c12a8cd55`. 원 PR base는 `659aa6dd3cb319761e8f7290155e025b11029c83`이다.
- 범위: 16개 파일의 전체 post-fix delta·최초 자기 finding과 변경으로 생긴 회귀. 규범 9개, 기록·독립 원본·통합 report를 함께 대조한다.
- 정본: [T-015](../../../tasks/T-015-common-delivery-plan.md), [ADR-014](../../../adr/014-common-implementation-without-registry-publishing.md), [release](../../../runbooks/release.md), [workflow](../../../runbooks/agent-workflow.md), [최초 통합](../2026-09-07-t015.md).
- A 영역: 현재 정본·agent 실행 가능성·DAG. B 영역: source/tag/asset·0.2 source·원장 왕복·CI·외부 gate. 둘 다 전체 수정의 회귀를 확인한다.
- 격리: 각 detached worktree를 지정 candidate로 전환하고 시작/종료 SHA·clean을 직접 확인한다. 새 post-fix 원본 둘이 확정되기 전 상대의 새 결과를 읽지 않는다. 최초 원본과 통합 finding은 모두 확정되어 열람 가능하다.
- 검증: link·plan·115 unittest·base diff check. release bash 구문, 명시 source/PR base/후보 ancestry, main 후속 minor와 release source 분리, 0.2 보존 및 과거 원장 유지→현재 main 문서 PR 완료·후속 선행 충족을 직접 공격한다. fixture/model은 실제 발행·제품 성공으로 세지 않는다.
- 자체 확인: Windows 115 tests·skip 0, link 246문서·2022대상, plan101·diff 성공. 실제 check_graph 메모리 모델과 WSL bash -n 성공. 이는 reviewer 독립 확인을 대신하지 않는다.
- 범위 밖: 실제 package build/install·candidate tag·Release·소비자 실행·타 저장소 쓰기. npm/PyPI 조회·예약·게시·게시 재평가는 사용자 범위 제외이며 후속 실행을 요구하지 않는다.

## 공통 요청 원문

위 candidate/base에서 독립 full post-fix 적대적 리뷰를 수행한다. 자신의 최초 finding을 원 ID·심각도로 재판정하고 전체 수정의 누락·숨은 선행·source/원장 혼동·실행 불가·미실행 성공 처리를 공격한다. 코드나 다른 작업자의 변경을 고치지 말고 지정한 새 reviewer 원본 파일만 작성한다. 실행 ID·시각·전달 입력·실제 SHA·clean·실행 명령과 결과·미검토·finding disposition·BLOCK/CONDITIONAL/PASS를 남긴다. 상대 reviewer의 이번 새 결과는 읽지 않는다. 원본 마지막에는 개행 하나만 둔다.
