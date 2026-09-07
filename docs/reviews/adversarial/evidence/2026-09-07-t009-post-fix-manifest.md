# T-009 수정 후 독립 리뷰 manifest

- Candidate: `f15072f4eb6543ead7636250671e8b12d60776e2`.
- 최초 candidate/수정 delta base: `45c238842a0b8b842ba63e9347b2f7218a3b2f0f`. 전체 PR base: `82dec2b939885863100802997f9e7548dffd3c9a`.
- 범위·전문 영역·격리·제외는 [최초 manifest](2026-09-07-t009-manifest.md)를 유지한다. [최초 통합 report](../2026-09-07-t009.md)의 8개 ID와 [T-009](../../../tasks/T-009-ci-hardening.md) 수용 기준을 새 SHA에서 재검토한다.
- 변경: report step source 작성·실제 CI 검증, Windows manifest 기준 경로 resolve와 회귀, 깊은 regex 컴파일 오류, 선택 정책에 일치하는 경로명의 원문 없는 거부, versions 정본과 T-005c 연결, PR template 고지 문구 정렬. 최초 코드/규약 전체를 반복 통독하지 않고 변경 delta와 회귀 영향을 확인한다.
- 검증: 전체 135 tests·skip 0, 두 guard·SPDX·link·plan·diff 및 원 반례 재실행. Windows 경로 별칭, step별 summary, 두 wrapper의 잘못된 정책과 파일/부모 경로 비공개를 확인한다. 선택한 패턴 범위와 임의의 모든 비밀 검출 보증을 구분한다.
- coordinator 로컬 결과: Windows 135 tests·skip 0(40.339초), WSL Python 3.11.15의 135 tests·skip 0(16.945초), link265/2131·plan102·SPDX18·guard324파일 오류 0. 직전 ec34d6a의 실제 PR/release push 5 check 성공과 source 증거는 task에 있다. 이번 candidate CI는 별도 조회하며 이전 run을 이번 SHA 성공으로 세지 않는다.
- 두 reviewer는 기존 원본을 읽을 수 있지만 이번 post-fix 상대 원본은 모두 확정되기 전 읽지 않는다. 각각 detached worktree의 시작/종료 SHA·clean을 기록하고 기본 checkout의 새 post-fix reviewer 파일 하나만 작성한다.

## 공통 요청 원문

같은 candidate에서 독립 full post-fix 리뷰를 수행한다. 원 finding ID·심각도를 유지하고 각각 FIXED/OPEN 여부, 원 반례 재검증, 전체 수정 delta의 회귀와 새 finding을 기록한다. T-005c의 미구현을 DONE 또는 CI 실측으로 세지 않는다. 실제 실행과 재사용/미실행을 구분한다. 검토 트리·다른 작업자 파일은 수정하지 않는다. 원문 값은 출력하지 않고 새 결과는 상대 원본과 독립적으로 확정한다.
