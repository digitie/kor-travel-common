# T-015 세 번째 수정 후 독립 리뷰 manifest

- Candidate: `95c139fdea523910fb5f1bdd32f5bae728df2915`.
- Base: `d1c7263de5c3ce930fbcdc234052bc7e98c1d2f1`. 원 PR base: `659aa6dd3cb319761e8f7290155e025b11029c83`.
- 범위: 10파일 delta. 규범 변경은 T-109·T-212의 발행 복제 제거·정본 연결·자산 확인 두 파일이며 나머지는 리뷰·상태 기록이다. 누적 9개 finding의 회귀를 확인한다.
- 정본: [T-015](../../../tasks/T-015-common-delivery-plan.md), [release](../../../runbooks/release.md), [직전 통합](../2026-09-07-t015-post-fix-02.md). 이전 두 원본은 확정되어 열람 가능하다.
- A 영역: 정본·task 실행 경로·A-P1-03의 실패 전파. B 영역: source·자동 태그 생성 우회·B-P1-06. 둘 다 전체 delta를 확인하고 원 ID·심각도를 유지한다.
- 검증: detached 시작/종료 candidate·clean, link·plan·unittest·diff 검사, 현재 규범의 발행 명령 전수 검색, 두 자산 확인 블록 정상/실패·정본 연결. 변경되지 않은 정본과 코드의 이전 직접 검증은 동일성을 확인하고 범위를 명시해 재사용할 수 있다.
- 자체 확인: Windows 115 tests·skip 0(12.916초), 최종 link 254문서·2077대상·plan101·diff 오류 0. 이전 실패 3건 재현과 수정된 자산 명령 6개 mock 기대 결과 확인. reviewer 독립 검증을 대신하지 않는다.
- 범위 밖: 실제 패키지/CI 구현·태그/Release·소비자 실행·다른 저장소 쓰기. 해당 미실행은 후속 task에 남는다. npm/PyPI 조회·예약·게시·재평가는 사용자 제외다. PR #4 병합 후 대기하며 다음 task를 시작하지 않는다.

## 공통 요청 원문

지정 candidate/base의 독립 full post-fix 리뷰를 수행한다. 자신의 기존 finding과 전체 delta의 회귀를 검토하고 새 원본만 작성한다. 이번 두 원본 확정 전 상대의 새 결과를 읽지 않는다. 실행 ID·시각·요청·실제 hash·clean·검증·미검토·원 ID별 disposition·verdict를 기록한다. 변경되지 않은 배경의 긴 재서술 대신 기존 확정 원본을 연결하며 새 검증과 재사용을 구분한다. 다른 작업자 파일을 고치거나 되돌리지 않는다.
