# Phase 0 post-fix 통합 판정

- Review ID: 2026-09-06-phase0-postfix, full.
- 상태: COMPLETE. 최종 verdict: BLOCK(A-P1-05 잔여).
- 기준선: `12fb3a816e5ebbdf9822a2c17ea7ad5534195fb9`; base `d3712a8c965c3193a5af13cacd6d22c603e0cfe4`.
- 시각·실행 ID·격리·실제 관찰 hash: [A 원본](evidence/2026-09-06-phase0-postfix-reviewer-a.md), [B 원본](evidence/2026-09-06-phase0-postfix-reviewer-b.md). 같은 [manifest](evidence/2026-09-06-phase0-postfix-manifest.md)로 독립 실행한 뒤 원본을 확정했다.
- 최초 finding: [Phase 0 report](2026-09-06-phase0.md).

## disposition

A-P1-01·02·03·04·A-P2-01은 FIXED. B-P1-01~06·B-P2-07~08도 FIXED. A-P1-05는 OPEN이다. 최초 fixture는 고쳤지만 Python 선언에서 실제 revision이 아닌 fragment를 고정 ref로 판단하는 경계가 남았다. 심각도 P1은 유지하며 뒤의 후보에서 원 reviewer가 확인해야 닫힌다.

A verdict BLOCK, B verdict PASS. B의 pinvi·airport 경로 순차 시뮬레이션은 28개 assertion 통과했으며 실제 외부 승인·설치 결과가 아니다. Windows·WSL에서 A가 65 tests/skip 0·193문서/1699target·96task 오류 0을 실행했다. B의 별도 Windows 검사도 같은 결과다. 실행하지 않은 패키지·소비자 gate와 각 reviewer의 검증 한계는 원본에 보존했다.

## 다음 기준선

coordinator는 Python @rev·npm fragment·uv resolved SHA를 구분하는 수정과 추가 회귀를 적용하고 있다. 최초 추가 회귀 3 subtest 실패를 재현했으며 수정 후 전체 67 tests가 Windows에서 성공했다. 이것은 이 report 기준선의 PASS가 아니다. 미커밋 인계 정합을 포함한 다음 immutable commit에서 두 리뷰어가 다시 확인한다.
