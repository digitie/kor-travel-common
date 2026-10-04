<!-- SPDX-License-Identifier: GPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie) -->

# Common Python fallback 포함 후보 — Popper 독립 적대적 원본

- 실행 ID: POPPER-COMMON-TRANSPORT-PYTHON-20261004-01
- 종류/관점: 원래 base 대비 전체 후보, Python 재시도·metadata 장애·동시성·deadline·공개 계약·패키징
- 시작: 2026-10-04T15:16:40.0616275+09:00
- 검토/검증 종료: 2026-10-04T15:24:44.6189221+09:00
- 전달/실제 관찰 candidate: `b324b0afdc27f268e6e6aaee1f6d7d2f42e4743b`
- base: `090f98429453d8882150eb9e56ccae98e0e353a2`
- 전달 정보: Draft PR #25 최신 CI 8개 SUCCESS, 부모가 Python40/UI42/pack PASS를 보고했다. 이를 본인의 실행 결과로 합산하지 않는다.
- 격리: 모든 저장소 소스는 Windows Git 고정 객체에서 읽었다. diff에서 `:(exclude)docs/reviews/**`를 적용하여 peer 결과 전체를 제외했다. 다른 리뷰어 원본·결과나 편집 중인 작업트리 소스를 열지 않았다. 재현은 객체 소스를 메모리 모듈로 실행했으며 저장소 source/build를 바꾸지 않았다. 이 원본만 생성한다.

## 판정

**BLOCK. P0 0개, P1 2개, P2 1개, P3 0개.** 정상적인 metadata 일시 장애에서 자동 복구가 영구 누락되는 경우와 native/fallback 전환에서 총 재시도 상한을 초과하는 경우를 확인했다. 이전 B-P3-01 주석 오류는 수정된 상태다. 이 판정은 b324 후보에만 적용한다. 검토 중 부모가 설명한 수정 설계는 새 고정 객체를 받기 전 closure로 인정하지 않는다.

## 범위

review 디렉터리를 제외한 17개 파일 전체 diff를 읽었다. Python dagster.py/deadline.py/test_recovery.py, UI 표시 함수/keyboard region/CSS/42-test 후보 및 버전/lock/smoke, CHANGELOG/가이드/task/journal/resume가 대상이다. 기존 helper와 새 fallback의 상호작용 및 공개 extras/빌드 설정도 확인했다. 실제 transport 후보 코드는 이번 범위 밖이다.

## 실제 실행 근거

Windows Git 객체의 Python 소스를 WSL Python에서 메모리 module로 주입하고 실제 DagsterInstance.local_temp/Definitions/remote origin/실패 event를 사용했다. 테스트에 쓰는 DB와 module은 별도 임시 상태이며 저장소 구현을 수정하지 않았다.

- Dagster **1.9.0 / Python3.11** 실제 sensor.evaluate_tick: callback metadata ConnectionError 뒤 cursor 전진, 다음 정상 tick의 RunRequest 0개 **재현**.
- Dagster **1.13.20 / Python3.13** 실제 sensor.evaluate_tick: 같은 실패 event 유실 **재현**. 이 로컬 환경 버전은 실제 import 결과이며 1.13.24를 실행했다고 보고하지 않는다. 첫 실행의 이전 버전 import 경로 차이는 수정하여 재실행했다.
- Dagster1.9.0: parent/root lineage를 가진 native retry_number=1 실패 run에 policy max1의 fallback request attempt1이 추가 발급됨 **재현**.
- Dagster1.9.0: op_selection=['first'] parent에 대한 fallback RunRequest는 selection이 없고 전체 두-op job을 대상으로 함 **재현**.
- Windows Python3.14.3에서 candidate deadline 객체 실행: timeout된 실제 호출 네 개가 slot을 계속 소유하고 다섯 번째 호출은 실행되지 않음, 네 호출 종료 뒤 용량 회복, Thread.start 실패 때 용량 반환 **PASS**. 처음 cp949 decode 실패는 UTF-8 명시 후 다시 실행했다.
- base→candidate review 제외 `git diff --check`: **PASS**.
- 전체 pytest/UI build/pack/install/CI API/live/실제 shared daemon: **NOT_RUN(부모 및 소비자 gate; 독립 focused 재현만 실행)**. 직전 common 후보에서 실행한 UI 38개 함수 경계와 package-path assertion은 같은 실행 코드의 이전 evidence이며 이번 전체 suite rerun으로 세지 않는다.

## Findings

### B-P1-01 — metadata 오류/timeout은 실패 이벤트를 소비해 복구를 영구 유실한다

- 위치: `packages/py/kor-travel-common/src/kortravelcommon/dagster.py:166–178,208–218`; `tests/test_recovery.py:296–306`의 callback 직접 호출 시험.
- 근거: factory는 run_failure_sensor callback에 call_with_deadline을 적용한다. Dagster의 실제 RunStatusSensorDefinition 평가 wrapper는 callback 오류를 RunStatusSensorExecutionError로 잡아 DagsterRunReaction.error를 반환하면서 해당 실패 event cursor를 전진시킨다. 따라서 callback 직접 호출에서 ConnectionError가 발생한다는 사실이 daemon 재평가를 보장하지 않는다. callback 밖의 status-change/run-record 조회도 이 10초 deadline 안에 들어 있지 않다.
- 실제 재현: empty sensor 첫 tick을 초기화 → remote origin/location/repository가 맞는 STARTED run 생성 → UNEXPECTED_TERMINATION event 기록 → get_records_for_run을 ConnectionError로 교체 → evaluate_tick. 이전 cursor와 달라지고 reaction.error.cls_name=ConnectionError. 원 메서드를 복원하고 반환 cursor로 다음 tick을 평가하면 RunRequest=0. Dagster1.9.0과1.13.20 모두 동일했다.
- 영향: 일시 DB 장애나 네 개 deadline slot 포화가 자동 회복되어도 해당 infrastructure failure는 다시 검사하지 않는다. 5분 schedule이 있는 소비자라도 실패한 실행의 복구 의미/전용 작업의 재시도는 사라진다. 새로운 정상 tick을 기다리는 것으로 실패 run의 재시도 계약을 대신할 수 없다.
- 권고: metadata 오류 시 failure event를 완료 처리하지 않는 durable cursor/pending 설계를 사용한다. 일반 sensor에서 bounded 실패 후보를 조회하고 모든 조회가 끝난 뒤에만 cursor를 ACK하거나, 실패한 후보를 durable pending으로 별도 저장한다. active run 때문에 합쳐진 실패도 필요하면 다시 평가하되 결정적 run key로 중복을 막는다. actual evaluate_tick 및 다음 tick까지 검사하는 회귀 시험을 추가한다. 모든 후보/status/event 조회를 같은 deadline 안에 둔다.
- disposition: OPEN, source 수정 없음.

### B-P1-02 — native/fallback 전환 때 같은 복구 체인의 재시도 예산이 초기화된다

- 위치: `dagster.py:145–146,170–175,188–205`; `RecoveryPolicy.tags:58–63`.
- 근거: fallback은 custom infra_retry_attempt만 읽고 native dagster/retry_number를 읽지 않는다. parent/root/retry_number lineage는 제거한 뒤 policy.tags가 원래 dagster/max_retries를 다시 부여한다. 현재 native enabled가 true인지 확인하는 것만으로 이미 소모한 과거 예산과 미래 설정 전환을 막을 수 없다.
- 실제 재현: policy.infrastructure_retries=1. 원 run 실패 후 native child에 root_run_id/parent_run_id와 dagster/retry_number='1'을 설정하고 그 child도 infrastructure 실패로 기록한다. native OFF instance에서 fallback callback은 customattempt 기본0으로 취급하여 RunRequest attempt='1'을 추가 발급했다. 즉 이미 native로 한 회 재시도한 후 총 두 번째 재시도가 생긴다.
- 반대 전환: fallback attempt1에는 dagster/max_retries='1'이 남고 native lineage는 새 root가 된다. 이후 instance native ON으로 바뀌면 native는 새 group에 한 회를 더 허용할 수 있다. Dagster1.9의 native reexecution 코어가 group 길이와 MAX_RETRIES_TAG로 예산을 계산함도 읽었다. 이 반대 방향은 정적 코드 확인이며 daemon end-to-end 실행으로 세지 않는다.
- 영향: 제한된 자동 infrastructure retry라는 공용 계약을 깨고 provider/launcher/메모리 비용을 계획보다 늘린다. 설정 롤아웃 중 old failure가 남는 상황에 적용된다.
- 권고: native와 fallback의 소모 예산을 공통으로 계산하고 잘못된 두 count 값은 fail-closed한다. parent 체인 또는 검증된 누적 태그를 보존하며, 새 child의 native max_retries는 남은 예산만 허용하도록 한다. native→fallback 및 fallback→native 양쪽 전환을 시험한다. pending native child/예약이 이미 존재할 때도 중복을 거절한다.
- disposition: OPEN, source 수정 없음.

### B-P2-01 — 부분 선택 parent를 전체 job으로 확대하여 재실행한다

- 위치: `dagster.py:136–141,202–205`; `docs/runbooks/dagster-adoption.md:196–199`.
- 근거: factory는 partition job만 거절하고 source run의 op_selection/resolved_op_selection/asset_selection/asset check selection을 검사하거나 보존하지 않는다. run_config를 복사해도 실행 범위는 복사되지 않는다. 가이드는 전체 멱등 job의 재실행을 설명하므로 지원 범위를 코드에서 강제할 필요가 있다.
- 실제 재현: 두 독립 op first/second job에서 parent op_selection=['first']로 infrastructure failure를 만든다. 반환 RunRequest에는 op selection 속성이 없으며 asset_selection도 None이다. request_job은 전체 sample이므로 second까지 실행 대상이 된다. subset용 run_config라면 재시도 run의 config validation이 실패할 수도 있다.
- 영향: 수동 subset 복구가 의도하지 않은 추가 provider/asset 작업으로 확대되거나 재시도 config가 유효하지 않게 된다. 현재 transport의 전체 단일-op 채택은 별도 소비자 검증 대상이므로 이 common API 결함을 transport의 실제 회귀로 단정하지 않는다.
- 권고: 전체 job만 지원하는 factory라면 subset/선택 실행 parent를 명시적으로 skip하고 문서에 경계를 적는다. asset selection을 지원하려면 관련 selection을 보존하고 op subset은 별도 job 정의/재실행 API로 지원하거나 fail-closed한다.
- disposition: OPEN, source 수정 없음.

## 다각도 공격 결과와 남은 경계

1. provider/STEP_FAILURE/unknown/cancel: allowlist는 UNEXPECTED_TERMINATION/START_TIMEOUT/RUN_WORKER_RESTART만 허용하고 RUN_EXCEPTION/STEP_FAILURE/UNKNOWN/None 및 FAILURE가 아닌 상태를 제외한다. recorded STEP_FAILURE가 있으면 허용 infrastructure reason이어도 skip한다. 원인 기록 전 강제 종료의 실제 도메인 예약 보호는 소비자 receipt/lease가 소유한다.
2. malformed count: ASCII decimal·최대6자리·상한 확인으로 음수/비ASCII/거대 문자열을 거절한다. native count 누락은 B-P1-02다. 정책 생성 시 int/bool 타입 구분은 유지된다.
3. origin/tag 신뢰: 현재 run_failure_sensor wrapper 자체가 remote origin의 현재 repository/location/job을 matching한다. callback도 project/location을 확인하고 origin이 있으면 origin을 우선한다. tag-only originless callback 단위 테스트가 wrapper의 실제 matching과 같다고 가정해서는 안 된다. 일반 sensor로 수정할 경우 wrapper의 repository matching을 새 구현에 명시적으로 보존해야 한다.
4. 동시 발화: has_active_run 조회와 request 발급은 원자적이지 않으며 문서는 이를 인정하고 coordinator JOB_TAG limit/소비자 DB lease를 요구한다. run key는 같은 sensor의 event 재평가 중복을 막는 계약이다. 서로 다른 이름의 sensor 중복 등록이나 다른 daemon/control-plane 설정 변경까지 전역 mutex라고 주장하지 않는다.
5. config replay: run_config 보존과 schedule/sensor/run_key/native lineage tag 제거는 적절하나 범위 선택은 B-P2-01이다. 최신 코드 배포 후 오래된 run_config의 schema 호환은 소비자가 보장해야 한다.
6. deadline: 실제 종료까지 semaphore slot을 유지하므로 timeout만으로 장수 code-server thread가 무제한 증가하지 않는다. 모든 네 호출이 영구 hang이면 이후 같은 프로세스의 deadline 호출은 즉시 fail-closed한다. daemon thread를 강제로 죽일 수 없으므로 프로세스 관리자의 health/restart 경계가 남는다. 전역 네 slot은 앱별 전용 quota가 아니며 여러 sensor가 공유한다.
7. UI/public packaging: dev.2 버전/락/tarball명/CSS export 일관성은 유지되며 기존 P3 주석 수정도 포함되어 있다. 공개 Python 추가는 optional dagster extra 안에 있고 core-only import 경계/라이선스 헤더가 유지된다. 이번 delta는 provider/SQL 구현을 common에 복사하지 않는다. compression artifact digest/consumer 설치/live 결과는 별도 gate다.

운영 shared instance의 active YAML, 런처 실제 종료, native retry child와 regular fallback의 동시 배포/작동, transport migration/fence/receipt/RSS는 이번 common 객체만으로 완료 판단할 수 없다. 수정 후 새 immutable 후보에서 위 세 finding과 full sensor cursor/selection/예산 전환을 재검토해야 한다.
