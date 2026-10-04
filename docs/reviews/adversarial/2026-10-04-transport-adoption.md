<!-- SPDX-License-Identifier: GPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie) -->
# Transport 공통 채택 적대 리뷰

상태: POST_FIX_REVIEW. 사용자 요청으로 common PR #25와 transport PR #67을 함께 검증한다.
common 기준선은 `090f98429453d8882150eb9e56ccae98e0e353a2`이다. 독립 리뷰는 상대 원문을
제외한 고정 Git 객체에서 수행했다. CodeGraph 대신 rg·공개 export·소비자 빌드로 추적했다.

## 원본과 수정

UI 후보 `f3e5681`은 James PASS, Popper CONDITIONAL(P3 주석 계약)이었다. `9da1889`에서
주석을 고쳤고 두 post-fix 리뷰 모두 PASS였다. 이후 실제 shared instance의 native retry
비활성화를 확인해 Python fallback을 추가했으므로 원래 UI PASS를 최종 Python PASS로
대신하지 않았다.

Python 포함 후보 `b324b0afdc27f268e6e6aaee1f6d7d2f42e4743b`의 두 원문을 보존한다.

- [James 원문](../evidence/2026-10-04-transport-common-james-python.md): BLOCK,
  SHA256 `dde4d0c52254b7623cc6715133094e477e89010d34fa61be9180b957cdd380ce`.
- [Popper 원문](../evidence/2026-10-04-transport-common-popper-python.md): BLOCK,
  SHA256 `DAAD39768D575FD96E30AEDA992B4CF1F4FE780C68E19C3A540E1A73ED540ACF`.

| finding | 보강 | 상태 |
|---|---|---|
| A-P1-01 / B-P1-01 metadata 오류 후 이벤트 cursor 소비 | 일반 sensor가 batch 준비 성공 후에만 cursor 전달, 실제 evaluate_tick 장애→복원 재현 | 수정·재리뷰 대기 |
| B-P1-02 native/fallback 전환 예산 초기화 | 두 횟수 합산·child native 잔여 예산 | 수정·재리뷰 대기 |
| B-P2-01 부분 실행이 전체 job으로 확대 | op/asset/check selection 제외 | 수정·재리뷰 대기 |
| A-P2-02 이벤트 조회가 boundedcall 밖 | 전체 실패 조회·event·검사·결과 생성에 10초/4개 상한 | 수정·재리뷰 대기 |
| A-P2-03 이전 native 실행 상태 태그 전파 | 앱 custom 태그와 job 정의 설정만 전달 | 수정·재리뷰 대기 |

공통 Python 54 tests와 ruff, 기존 UI 42 tests·build·pack·소비자 lock 검증은 PASS다.
수정 SHA의 CI와 두 독립 post-fix verdict, transport live UI를 완료한 뒤 최종 판정을 갱신한다.
운영 shared coordinator 적용·실제 worker kill/retry child·운영 RSS는 NOT_RUN이다.

## 두 번째 수정

`7ee00152c2f7b3877ff3bedcd61a58ec15122d89` 재리뷰 원문도 보존한다.

- [James 재리뷰](../evidence/2026-10-04-transport-common-james-python-postfix.md): CONDITIONAL,
  SHA256 `9c364927d8c3b8911567e1beab19f86ce41f97ceacb63e7ab243306124d339ed`.
- [Popper 재리뷰](../evidence/2026-10-04-transport-common-popper-python-postfix.md): BLOCK,
  SHA256 `A52530F97EDF7ADFB3A08097BD295D325D5A69A5B466C9D09E3FECD8D1BB4342`.

| finding | 추가 보강 | 상태 |
|---|---|---|
| B-P1-02 native 체인/원 parent 예산 잔여 | 기존 child 조회·원 parent native 예산 0·will_retry false | 수정·재리뷰 대기 |
| B-P2-01 resolved subset | 전체 graph 및 전체 실행 계획과 비교 | 수정·재리뷰 대기 |
| A-P2-04 / B-P2-02 정상 느린 페이지가 반복 timeout | 5초 작업 예산 뒤 완료 cursor를 저장, 다음 tick 재개 테스트 | 수정·재리뷰 대기 |

원문 verdict를 임의로 낮추지 않는다. 새로운 후보의 두 리뷰와 CI가 끝나기 전에는 머지하지 않는다.
