# T-015 두 번째 수정 후 독립 리뷰 manifest

- Candidate: `d1c7263de5c3ce930fbcdc234052bc7e98c1d2f1`.
- Base: `ae86185ff103156ffd516b572cf97d401f4a3d31`. 원 PR base는 `659aa6dd3cb319761e8f7290155e025b11029c83`이다.
- 범위: 14개 파일의 전체 post-fix delta와 누적 7개 finding의 회귀. 발행 명령 정본 단일화·실패 시 중단·원격 peeled SHA 대조와 릴리스 CI 구현 선행 task를 검토한다.
- 정본: [T-015](../../../tasks/T-015-common-delivery-plan.md), [ADR-014](../../../adr/014-common-implementation-without-registry-publishing.md), [release](../../../runbooks/release.md), [CI](../../../standards/ci-deploy.md), [직전 통합](../2026-09-07-t015-post-fix.md).
- A 영역: 정보 정본·agent 실행 가능성·DAG·CI 선행. B 영역: tag/push/Release 실패·source SHA·CI 검증 경로. 둘 다 전체 수정의 회귀와 자신의 기존 finding을 확인한다.
- 격리: 각 detached worktree의 시작/종료 SHA·clean을 직접 확인한다. 이번 새 원본 둘이 확정되기 전 상대 결과를 읽지 않는다. 이전 확정 원본은 열람 가능하다.
- 검증: link·plan·115 unittest·base diff check, 실제 bash 발행 절의 정상/실패 mock 및 중복 명령 제거, CI trigger·checkout SHA·후보 보존 이전 선행의 실행 가능성을 확인한다. 모델 검증을 실제 발행 성공으로 집계하지 않는다.
- 자체 확인: Windows 115 tests·skip 0, link 250문서·2052대상, plan101·diff 성공. WSL bash mock 10개 시나리오 성공. 이는 reviewer 독립 검증을 대신하지 않는다.
- 범위 밖: workflow 구현은 T-009·T-101·T-201·T-302 소유이며 이번에는 계획과 수용 기준만 보완했다. 실제 release branch CI·package build/install·candidate tag·Release·소비자 실행은 NOT_RUN이다. npm/PyPI 조회·예약·게시·게시 재평가는 사용자 범위 제외다. 다른 저장소를 수정하지 않는다.
- 종료 조건: 현재 PR #4를 검증·머지한 뒤 대기한다. 다음 task 구현을 시작하지 않는다.

## 공통 요청 원문

위 candidate/base에서 독립 full post-fix 적대적 리뷰를 수행한다. 기존 finding은 원 ID·심각도로 재판정하고 전체 수정에서 새 회귀를 찾는다. 다른 작업자의 변경을 고치지 말고 지정한 새 reviewer 원본 파일만 작성한다. 실행 ID·시각·전달 입력·실제 SHA·clean·검증 명령과 결과·미검토·finding disposition·BLOCK/CONDITIONAL/PASS를 남긴다. 상대 reviewer의 이번 새 결과는 읽지 않는다. 원본 마지막에는 개행 하나만 둔다.
