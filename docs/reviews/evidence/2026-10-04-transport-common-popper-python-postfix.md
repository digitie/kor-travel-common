<!-- SPDX-License-Identifier: GPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie) -->

# Common Python post-fix — Popper 독립 적대적 원본

- 실행 ID: POPPER-COMMON-TRANSPORT-PYTHON-POSTFIX-20261004-01
- 시작: 2026-10-04T15:35:44.5576758+09:00
- 검토/검증 종료: 2026-10-04T15:44:49.0985016+09:00
- 원래 base: `090f98429453d8882150eb9e56ccae98e0e353a2`
- 직전 검토: `b324b0afdc27f268e6e6aaee1f6d7d2f42e4743b`
- 전달/실제 관찰 candidate: `7ee00152c2f7b3877ff3bedcd61a58ec15122d89`
- 범위: 자기 finding closure와 전체 base delta의 Python/공개 UI/패키징/복구 가이드. source read-only. 모든 저장소 source는 Windows Git 고정 객체로 읽었다. diff의 `docs/reviews/**`를 전체 제외해 peer 원본·결과를 읽지 않았다. 테스트는 Git 객체에서 임시 snapshot/메모리 모듈을 생성해 실행하며 저장소 source/build·기존 보고서를 수정하지 않았다. 이 원본만 생성한다.
- 전달 정보: 부모가 후보 GitHub CI 전체 SUCCESS(37182998435/37182998326), Python49/ruff PASS를 보고했다. CI API를 독립 조회했다고 세지 않는다.

## 판정

**BLOCK.** 기존 B-P1-01은 FIXED다. B-P1-02와 B-P2-01은 추가 경로가 남아 OPEN이며, 정상적으로 느린 metadata batch의 무진전 B-P2-02가 신규 OPEN이다. 잔여/신규 수는 P0=0, P1=1, P2=2, P3=0이다. 부모가 검토 중 설명한 추가 수정 계획은 이번 immutable 후보의 closure로 세지 않는다.

## 실제 검증

고정 객체의 `dagster.py`, `deadline.py`, `__init__.py`, `test_recovery.py`를 임시 디렉터리로 가져와 source import를 고정하고 기존 venv는 바꾸지 않았다.

- Python3.13.14 / Dagster **1.13.24**, candidate test_recovery.py: **49 PASS**, 6.21초.
- Python3.11.15 / Dagster **1.9.0** floor, 같은 candidate test_recovery.py: **49 PASS**, 7.29초.
- 위 시험은 실제 evaluate_tick의 metadata exception/timeout cursor 보존·재평가, head 순환, native count, 원천 scope와 태그 제거를 포함한다. 초기 modern 시험 뒤 별도 probe에서 Dagster DefinitionsLoadContext의 폐기된 instance weakref를 만났으므로 추가 probe는 새 process로 분리하여 성공적으로 재실행했다. 후보 테스트 49개가 실패한 것으로 해석하지 않는다.
- 실제 Dagster1.9.0/1.13.24에서 resolved_op_selection만 지정한 두-op parent의 전체 fallback 발급을 재현했다.
- 실제 Dagster1.9.0 native 필터에서 fallback 완료 후 원 FAILED parent의 native 재시도 자격이 남음을 확인했다. 1.13.24에서는 native ON 때 failure를 기록해 will_retry=true를 만든 후 OFF→fallback SUCCESS→native 필터 평가로 같은 자격 잔존을 확인했다.
- 1.13.24에서 이미 성공한 native child와 auto_retry_run_id를 가진 원 FAILED root가 fallback으로 다시 발급되는 것도 재현했다.
- 삭제된 cursor를 전달하면 head로 복귀하며, 초기 역사 FAILED는 이후 정상 SUCCESS가 있어도 재발급되는 현재 정책을 1.9.0에서 관찰했다.
- 정상적인 느린 100개 metadata row를 대상으로 10초 경계를 10ms로 축소한 비율 실험: 두 tick이 같은 head에서 timeout되고 cursor=None 유지 **재현**. 실제 운영 metadata가 이만큼 느리다고 주장하지 않는다.
- base→candidate review 제외 `git diff --check`: **PASS**.
- UI/pack/install/live/운영 daemon native child 실제 launch/CI API: **NOT_RUN(부모 및 소비자 gate)**. 이전 UI 함수·패키징 검토와 같은 runtime이며 source/public 경로가 유지됨을 diff로 확인했다. 실제 shared instance 실행을 이번 Python local 테스트로 대체하지 않는다.

## Closure

### B-P1-01 — FIXED: callback 예외의 실패 event 소비

`packages/py/kor-travel-common/src/kortravelcommon/dagster.py:222–270`이 일반 sensor로 전체 후보/event/검사를 deadline 안에서 수행한다. 예외/timeout 때 context.update_cursor를 호출하지 않으며 결과가 반환된 후 SensorResult로만 cursor를 전달한다. timeout된 늦은 thread도 context를 수정하지 않는다. actual evaluate_tick 회귀가 두 버전 모두 PASS하여 기존 run_failure_sensor의 예외 ACK 문제는 해결됐다. 아래 느린 batch 무진전은 별도 새 P2다.

### B-P1-02 — OPEN: 개별 count는 합산했지만 원 parent/전체 체인의 예산은 남는다

- 위치: `dagster.py:185–201,204–219,234–260`.
- 수정 확인: source run의 custom+native count를 합산하고, fallback child의 native max_retries를 잔여치로 낮춘다. native child 자신에서 이미 소모한 count를 무시했던 경로는 해결됐다.
- 잔여 A 실제 재현(Dagster1.13.24): policy max1인 원 run을 native ON 상태에서 infrastructure failure로 기록한다. 원 parent에 will_retry=true가 설정된다. OFF 상태에서 새 sensor가 fallback attempt1/native budget0을 발급하고 그 child를 SUCCESS로 생성한다. 원 parent는 FAILED/max_retries1/will_retrytrue 그대로이며 fallback child의 Dagster parent attribute는 None이다. `filter_runs_to_should_retry([parent])`는 여전히 원 parent를 허용했다. native ON 복귀 시 기존 native daemon cursor가 해당 pending 실패를 처리하면 총 두 번째 retry가 가능하다. 실제 daemon launch는 실행하지 않았으며 상태 생성과 실제 native 필터 자격 평가까지 검증했다. floor1.9에서도 원 parent의 group에 native 자식이 없어 동일 자격이 남는다.
- 잔여 B 실제 재현(1.13.24): 원 FAILED root에 native child SUCCESS(root_run_id/parent_run_id와 retry_number1)를 생성하고 root.auto_retry_run_id를 해당 child ID로 기록한다. 이후 native OFF sensor는 원 root의 count0과 현재 active 없음만 보고 fallback attempt1을 다시 발급했다. 이미 성공한 같은 native 복구 체인이 재시도 예산1을 추가 소비한다. 순환 스캔은 child 실패가 없어도 과거 원 FAILED root를 다시 만난다.
- 영향: child count만으로 같은 복구 체인의 소모 예산/예약을 확인하지 못한다. 활성 native↔fallback 설정 전환 및 성공한 native chain의 역사 스캔에서 총 상한과 중복 방지 계약이 깨진다.
- 권고: 실제 기존 native child/auto_retry_run_id/run_group을 조회하여 parent를 재발급하지 않고 복구 체인의 현재 leaf/누적 예산을 확인한다. fallback을 인계한 원 parent의 native 자격도 durable하게 닫아야 한다. metadata 실패/timeout 뒤 claim과 request가 분리되어 영구 누락되지 않도록 설계한다. child budget0만으로 원 parent가 native에서 소모 완료되었다고 판단하지 않는다. 양 방향 전환 및 SUCCESS/CANCELED/FAILED 기존 child별 회귀를 추가한다.
- disposition: OPEN.

### B-P2-01 — OPEN: resolved subset만 지정한 parent 확대 경로가 남는다

- 위치: `dagster.py:170–171,215–219`.
- 수정 확인: 명시적 op/asset/check selection은 제외한다.
- 잔여 실제 재현(1.9.0/1.13.24): first/second 두-op job에 `create_run_for_job(...resolved_op_selection={'first'}, op_selection=None)`을 사용한다. source run.op_selection은 None, resolved_op_selection은 first다. infrastructure failure 뒤 sensor.evaluate_tick이 전체 request_job sample의 RunRequest 하나를 발급했다. source의 subset은 보존되지 않는다.
- 영향: 공개 API의 부분 실행이 의도하지 않은 추가 op로 확대된다. step_keys_to_execute 등 별도 reexecution 선택 경계도 이 조건에 포함되지 않으므로 final 후보에서 검증이 필요하다.
- 권고: resolved 선택이 전체 job graph 집합과 다른 경우 및 step 선택을 명시적으로 거절한다. empty/None/전체 선택의 의미를 구별하고 선택 경계 자체를 시험한다.
- disposition: OPEN.

### B-P2-02 — 신규 OPEN: 정상적으로 느린 첫 batch가 매 tick timeout되면 다음 페이지에 도달하지 않는다

- 위치: `dagster.py:229–261,269–272`.
- 근거: 100개 후보를 모두 확인하거나 request를 반환하기 전까지 완료 cursor를 전진시키지 않는다. metadata 조회가 예외 없이 반환해도 첫 100개의 누적 지연이 10초보다 길면 매 tick 같은 head를 반복한다. 모두 unknown/foreign/provider 실패인 prefix 뒤 infrastructure 실패가 있으면 그 뒤 복구 행에는 도달하지 못한다.
- 재현: 실제 1.13.24 evaluate_tick에 unknown 실패 100개를 제공하고 각 event 조회를 3ms 지연했다. 동일 비율을 짧게 확인하기 위해 deadline만10ms로 축소했다. 두 tick 모두 DeadlineExceeded, context.cursor=None, 조회 cursor=[None,None]. 늦은 thread는 끝나지만 반환되지 않은 완료 진전은 보존되지 않는다. 이는 축소 실험이며 운영 10초 미만의 실제 성능을 측정한 결과가 아니다.
- 영향: CPU/DB가 꾸준히 느린 상태에서는 연결이 정상이어도 오래된 첫 페이지 때문에 회수가 계속 지연된다. strict timeout fail-closed 자체는 필요하지만 bounded page 크기만으로 진전까지 보장하지 않는다.
- 권고: 외부 deadline보다 짧은 작업 시간 예산을 두고 최소 한 row의 완전한 판단 뒤 안전한 마지막 완료 cursor를 반환한다. 개별 조회가 timeout/오류라면 해당 row를 ACK하지 않는다. 느린 정상 prefix→다음 페이지 후보를 actual evaluate_tick으로 시험한다.
- disposition: OPEN.

## 추가 공격 결과/범위 제한

repository/job origin 검사와 originless의 project/location 태그 요구가 명시되어 다른 repository의 동명 job에 대한 factory 경계가 강화됐다. native 상태 태그는 source에서 제거하고 job 정의의 실행 태그만 재적용한다. 이전 P3 공개 duration 주석은 실제 한국어 계약으로 유지된다. UI version/lock/public export·GPL 고지와 Python optional extra 경계에 새 회귀를 찾지 않았다.

cursor 삭제/retention reset과 head 순환은 동작했다. 초기 소개 시 역사 실패를 재예약하고 이미 정상 새 tick 성공 뒤에도 원 실패를 재평가하는 것은 현재 전체 실패 순환 정책이다. 이 사실을 새로운 timestamp 기반 skip 규칙으로 임의 해석하지 않는다. 다만 같은 복구 체인의 이미 성공한 native child를 무시하는 것은 B-P1-02의 실제 중복이다. 오래된 정상 실패가 많을 때 한 순회의 지연은 가이드에 남아 있다.

결정적 run key는 같은 sensor의 동일 parent 요청 재평가를 dedup하지만 예산/체인 판단을 대신하지 않는다. sensor 확인과 수동 발화 사이 경쟁은 coordinator job limit/소비자 lease가 소유한다. 실제 shared manager 설정, transport DB migration·late commit fence·receipt/RSS·live 브라우저는 별도 transport immutable 후보와 실행 evidence에서 확인해야 한다. source 수정은 하지 않았다.
