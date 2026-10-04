<!-- SPDX-License-Identifier: GPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie) -->
# Transport 공통 채택 최종 코드 판정

- Review ID: TRANSPORT-COMMON-20261004-CLOSURE.
- base: `090f98429453d8882150eb9e56ccae98e0e353a2`.
- immutable runtime candidate: `430a9e9cd5429204579792b1d4f8e399366dcb2f`.
- 두 reviewer는 상대 원문을 제외한 고정 Git 객체를 독립적으로 검토했다.
- [이전 원문·수정 이력](2026-10-04-transport-adoption.md)을 보존한다.

## 원본 판정

- [James](../evidence/2026-10-04-transport-common-james-python-handoff.md): PASS,
  SHA256 `482b2028fed3a119f755bd8f58e675c17210e0cb591f6ac178ed579dfbf2bdb7`.
- [Popper](../evidence/2026-10-04-transport-common-popper-python-handoff.md): PASS,
  SHA256 `2436E274E8231AF22F63EFE7E547BF394084EE048D513064F93D036E4FA2D5BD`.

기존 finding은 모두 FIXED이며 신규·잔여 actionable finding은 없다. 마지막 A-P2-05 /
B-P1-03은 parent 억제 COMMIT 후 ACK 유실 또는 timeout 뒤 지연 COMMIT에서 native ON으로
전환할 때 복구가 사라지는 문제였다. 두 reviewer가 실제 metadata·evaluate_tick·native
retry filter로 pending 인계 복원과 child 확인 후 종료를 각각 검증했다. 심각도를 낮추거나
운영 위험 수용으로 닫지 않았다.

## 검증

- Python 복구 56 tests: Dagster 1.13.24와 floor 1.9.0에서 두 reviewer 각각 PASS.
- 격리 서버에 설치한 wheel도 native 1.13.24에서 56 tests PASS(20.19초).
- ruff PASS, UI 42 tests·build·pack·소비자 설치 PASS.
- 후보 CI 8개 PASS: [공통 CI](https://github.com/digitie/kor-travel-common/actions/runs/37184964291),
  [Python 3.11/3.13 복구](https://github.com/digitie/kor-travel-common/actions/runs/37184964141).
- transport live UI에서 로그인·메뉴·실패/정체·12개 스케줄·키보드/모바일·조회 장애 시
  마지막 결과 유지·다시 시도 복원·native 실패 이벤트 링크를 확인했다.
  [소비자 PR #67](https://github.com/digitie/kor-travel-transport/pull/67)에 캡처를 보존한다.
- 최신 wheel의 복구 모듈 hash와 transport 복구 sensor 4개 등록을 격리 런타임에서 확인했다.

운영 shared coordinator 변경·운영 daemon/launcher 전체 제출·실제 worker kill/retry child·
운영 RSS는 NOT_RUN이다. 실행한 단위/격리 검증과 합산하지 않는다.
소비자 최종 리뷰와 PR 머지 결과는 소비자 기록에 남긴다.

이 closure는 원문·판정·재검증 기록만 추가한다. 런타임은 위 candidate와 같다.
