<!-- SPDX-License-Identifier: GPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie) -->

# Common 두 번째 Python post-fix — Popper 독립 원본

- 실행 ID: POPPER-COMMON-TRANSPORT-PYTHON-FINAL-20261004-01
- 시작: 2026-10-04T15:55:56.0894790+09:00
- 검토/검증 종료: 2026-10-04T16:00:06.5144568+09:00
- 원래 base: `090f98429453d8882150eb9e56ccae98e0e353a2`
- 직전 검토: `7ee00152c2f7b3877ff3bedcd61a58ec15122d89`
- 전달/실제 관찰 candidate: `f0d27b4cca2aae9c2f58e2ed12bbf5495d12fcc0`
- 전문 영역/범위: Python 복구 인계·native 예산·스토리지 오류·deadline/순환 조회와 전체 base delta의 공개 UI/패키징/가이드 계약.
- 격리: Windows Git 고정 객체만 읽고 diff에서 `docs/reviews/**`를 제외했다. peer 원본/결과, 다른 작업자의 작업트리 source를 열지 않았다. 설치 환경을 변경하지 않고 객체 snapshot을 임시 디렉터리/메모리에서 실행했다. 저장소 source/build와 과거 원본을 수정하지 않았으며 이 원본만 생성한다.
- 전달 정보: 부모가 PR25 CI8개 SUCCESS, Python54/ruff PASS를 보고했다. CI API의 독립 검증으로 합산하지 않는다.

## 판정

**BLOCK — 기존 네 Python finding은 FIXED, 새 B-P1-03 한 건 OPEN.** 잔여/신규 P0=0/P1=1/P2=0/P3=0이다. 정상 metadata 오류 후 native OFF를 유지하면 동일 key로 회복하지만, parent 억제가 commit된 뒤 child가 만들어지기 전에 native ON으로 전환하면 양쪽 복구가 모두 사라지는 경계가 남는다. 문서의 daemon drain은 동시 실행을 줄이지만 이 durable 반쪽 인계 상태의 존재/해소를 확인하는 계약은 아니다.

## 실제 검증

candidate의 Python source와 test_recovery.py를 Windows Git에서 임시 snapshot으로 읽고 기존 venv를 그대로 사용했다.

- Python3.13.14 / Dagster **1.13.24**: candidate test_recovery.py **54 PASS**, 7.62초.
- Python3.11.15 / Dagster **1.9.0** floor: 같은 candidate **54 PASS**, 8.63초.
- 두 버전 추가 실제 probe: fallback request/성공 child 뒤 원 FAILED parent의 native 필터 결과가 비어 있음 **PASS**. 이전 중복 자격 잔존은 해결됐다.
- 두 버전 추가 실제 evaluate_tick: parent add_run_tags가 commit한 뒤 ConnectionError를 반환하도록 주입 → cursor=None·child0·parent max_retries0/will_retryfalse. 이어 native ON 때 fallback 요청0/native 필터 후보0 **재현**.
- 동일 실패 상태에서 native OFF를 유지한 대조: 같은 pending 요청을 다시 준비함 **PASS**. 새 finding을 모든 metadata 오류가 영구 누락되는 것으로 확대하지 않는다.
- base→candidate `git diff --check`(review 제외): **PASS**.
- full UI/build/pack/install/CI API/실제 운영 daemon launch/live: **NOT_RUN(부모 및 소비자 gate)**. 실제 shared instance의 전환을 실행했다고 세지 않는다. native 필터와 실제 metadata 상태/evaluate_tick까지 독립 검증했다.

## 기존 finding closure

- **B-P1-01 FIXED**: 일반 sensor가 전체 metadata 평가를 deadline 안에서 수행하고 예외/timeout 때 cursor를 반환하지 않는다. 두 버전 actual evaluate_tick 회귀가 통과했다.
- **B-P1-02 FIXED**: `dagster.py:213–228`에서 유효한 auto_retry child.parent와 native/fallback parent tag 조회로 이미 발급된 child를 찾는다. 상태가 SUCCESS/CANCELED여도 parent를 재발급하지 않는다. `248–250`에서 원 parent native 예산/will_retry도 닫고 child의 잔여 예산만 전달한다. 정상 요청 발급 뒤 native 필터가 원 parent를 거절하는 것을 두 버전에서 재현했다. 아래 새 finding은 예산 초과가 아니라 요청 발급 전 실패의 인계 유실이다.
- **B-P2-01 FIXED**: `170–180`에서 명시적 선택의 None/empty 구분과 partial resolved graph를 검사하고, `189–196`에서 실행 plan의 일부 step을 거절한다. 두 subset 경로의 actual evaluate_tick 시험이 두 버전 모두 PASS했다.
- **B-P2-02 FIXED**: `258,273–277`의 5초 soft budget은 최소 한 row를 완료한 뒤 완료 cursor를 반환하며 외부10초 상한을 유지한다. 느린 정상 prefix를 checkpoint한 다음 tick이 뒤 복구 후보에 도달하는 시험이 두 버전 모두 PASS했다.

## 새 finding

### B-P1-03 — parent native 억제만 저장된 반쪽 인계를 native ON이 영구 방치한다

- 위치: `packages/py/kor-travel-common/src/kortravelcommon/dagster.py:154–155,245–254,260–261`; `docs/runbooks/dagster-adoption.md:199–212`.
- 근거: request를 반환하기 전 parent의 max_retries0/will_retryfalse를 durable하게 저장한다. 이 저장 후 응답 유실/outer deadline/요청 제출 실패에는 아직 child가 없다. native OFF에서는 다음 tick에 재발급하지만 native ON에서는 후보 조회 전에 즉시 위임 SkipReason을 반환한다. 억제된 parent는 native에서도 재시도할 수 없다. pending 인계를 나타내는 별도 durable marker/child 생성 ACK/전환 시 재확인 경로가 없다.
- 실제 재현(1.13.24 및1.9.0): 정책 max1인 scope-matching infrastructure FAILED run 생성. add_run_tags를 original 메서드로 먼저 실행하고 그 뒤 ConnectionError('commit ACK lost')를 발생시킨다. sensor.evaluate_tick은 오류를 전달하며 cursor=None이다. DB parent는 max_retries='0', will_retry='false'이고 등록된 child는0개다. 메서드를 복원하고 native enabled=True로 바꿔 tick을 평가하면 request0개. 같은 parent의 실제 native filter도0개다. ON을 유지하면 두 조건이 다음 tick에도 그대로이며 자동 회복 경로가 없다. OFF로 되돌린 대조는 request1개로 회복했다.
- 운영 형태: 정상적인 commit 응답 유실 또는 parent tag가 늦게 저장되는 timeout 후 old daemon/code-server를 drain하고 native를 활성화할 때 발생할 수 있다. 이미 저장된 parent 상태는 drain으로 되돌아가지 않는다. parent-tag commit 뒤 RunRequest가 반환되기 전 process crash도 같은 durable 상태를 남긴다. process/운영 daemon crash 자체는 이번 실행에서 주입하지 않았으며 같은 저장 순서의 실패 형태다.
- 영향: 재시도 예산을 한 회도 실제 실행하지 않았는데 원 FAILED run이 native와 fallback 모두에서 영구 중지된다. 가이드의 "제출 실패에는 같은 key로 다시 준비"는 native OFF를 유지할 때만 성립한다.
- 권고: parent 억제와 함께 durable pending 인계를 기록하고 child ACK가 없으면 native ON에서도 제한적으로 그 인계를 완료하도록 한다. 또는 전환 절차에 반쪽 인계 식별/재제출/closure를 실제로 수행하는 검증 가능한 gate를 구현해야 한다. 단순 daemon drain이나 일반 위험 수용으로는 상태를 닫을 수 없다. commit ACK 유실/late thread/제출 실패/process restart 후 native 전환을 actual evaluate_tick으로 검사한다. pending 복구는 같은 run key와 소모 예산을 유지하고 이미 만들어진 child가 있으면 반복하지 않아야 한다.
- disposition: OPEN. source 수정 없음.

## 추가 공격 결과와 불확실성

native/fallback child 조회는 limit1과 parent UUID로 제한되어 전체 과거 child를 메모리에 모으지 않는다. invalid/다른 parent의 auto_retry pointer를 신뢰하지 않고 일반 parent tag 조회를 보조로 사용한다. prior native 상태 태그는 source에서 복사하지 않고 현재 job 설정만 적용한다. origin/repository/job 경계, provider/step/unknown/cancel 제외, 숫자 예산 검사, head/retention cursor reset은 유지된다.

동시 수동 발화/서로 다른 설정 daemon 사이 조회와 request의 비원자성은 coordinator/소비자 lease 및 전환 drain이 소유한다. 이번 보고서는 서로 다른 설정 daemon을 동시에 띄워야만 새 finding이 생긴다고 주장하지 않는다. 늦은 thread는 context cursor를 변경하지 않지만 parent metadata write를 수행할 수 있으므로 새로운 인계 상태가 필요하다.

초기 역사 실패의 재평가와 순회 지연은 가이드에 명시됐다. 이미 native/fallback child가 있는 역사 parent는 이제 제외된다. UI dev.2·공개 경로·CSS·라이선스/optional extra에 이번 delta의 새 회귀를 찾지 않았다. 운영 shared manager YAML/launcher/RSS, transport migration/fence/receipt와 live 브라우저는 별도 immutable transport 후보 및 부모 evidence의 범위다.
