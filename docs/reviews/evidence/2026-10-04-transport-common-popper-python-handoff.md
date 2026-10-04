<!-- SPDX-License-Identifier: GPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie) -->

# Common 최종 pending 인계 — Popper 독립 적대적 원본

- 실행 ID: POPPER-COMMON-TRANSPORT-HANDOFF-20261004-01
- 시작: 2026-10-04T16:14:02.8538565+09:00
- 검토/검증 종료: 2026-10-04T16:19:02.4275000+09:00
- 원래 base: `090f98429453d8882150eb9e56ccae98e0e353a2`
- 직전 검토: `f0d27b4cca2aae9c2f58e2ed12bbf5495d12fcc0`
- 전달/실제 관찰 candidate: `430a9e9cd5429204579792b1d4f8e399366dcb2f`
- 전문 영역: native/fallback 인계·cursor·metadata 장애·deadline·예산·부분 선택·공개 패키지 경계.
- 격리: Windows Git 고정 객체만 읽었다. diff에서 `docs/reviews/**`를 전체 제외하여 peer 원본/결과와 다른 작업자의 편집 source를 읽지 않았다. 기존 venv를 설치 변경 없이 사용하고 객체 source/test만 임시 snapshot으로 실행했다. source/build/기존 원본을 수정하지 않았으며 이 evidence만 생성한다.
- 전달 정보: 부모가 PR25 CI8개 GREEN(37184964291/37184964141)을 보고했다. CI API를 본인이 독립 확인한 것으로 세지 않는다.

## 판정

**PASS. B-P1-03 FIXED. 신규/잔여 P0/P1/P2/P3는 0개다.** 이전 Python의 B-P1-01/B-P1-02/B-P2-01/B-P2-02 및 공개 주석 B-P3-01 closure도 유지된다. 이 판정은 common 후보 코드 계약이며 실제 shared instance 설정·transport 도메인 migration/fence·live UI gate를 대체하지 않는다.

## 실제 검증

candidate `__init__.py`, `dagster.py`, `deadline.py`, `test_recovery.py`를 Windows Git 객체에서 가져와 임시 snapshot으로 source import를 고정했다.

- Python3.13.14 / Dagster **1.13.24**: candidate test_recovery.py **56 PASS**, 8.30초.
- Python3.11.15 / Dagster **1.9.0** floor: 같은 candidate **56 PASS**, 9.69초.
- 두 버전 추가 독립 probe A: parent tag commit 후 ConnectionError('commit ACK lost') → 실제 evaluate_tick cursor 미전진 → native ON → 동일 run key 요청 복원 → SUCCESS child 생성 → cursor/head 순환 → pending false 및 추가 요청 없음 **PASS**.
- 두 버전 추가 독립 probe B: add_run_tags를 대기시켜 바깥 deadline(실험에서는10ms) timeout → cursor 미전진 → release 후 늦은 parent commit → 해당 thread 종료/slot 반환을 확인 → native ON → 같은 요청 복원 → SUCCESS child 확인 후 pending false **PASS**. 이는10초 production 상한을10ms로 축소한 실제 지연 저장 실험이며 운영 DB latency 측정이 아니다.
- 위 probe에서 child에 pending 태그가 상속되지 않고, 원 parent의 실제 native filter 결과가 비어 중복 예산을 사용하지 않음을 두 버전에서 assert **PASS**.
- base→candidate review 제외 `git diff --check`: **PASS**.
- full UI/build/pack/install/CI API/운영 daemon 실제 child launch/shared YAML/live UI/RSS: **NOT_RUN(부모 및 소비자 gate)**. actual evaluate_tick/local metadata/native 필터와 full recovery 시험 결과만 독립 실행으로 기록한다.

## B-P1-03 closure — FIXED

위치: `packages/py/kor-travel-common/src/kortravelcommon/dagster.py:156–158,216–234,243,255–262,269–284`.

native 억제의 max_retries0/will_retryfalse와 `infra_retry_pending=true`가 같은 add_run_tags metadata 쓰기에 들어간다. 응답이 유실되거나 늦게 완료된 저장은 완성되지 않은 인계의 표식을 남긴다. native ON에서 polling filter는 pending 행만 읽고 callback도 해당 행은 native 위임으로 건너뛰지 않는다. 새 실패에 대한 native 소유권은 유지한다.

child의 native 예산은 잔여치이며 원 parent는 native에서 계속 억제된다. 동일 parent/attempt의 결정적 key로 미완료 요청을 다시 준비한다. 기존 native/fallback child를 확인한 후에만 pending을 false로 닫고 child의 태그에서는 pending을 제거한다. 그러므로 child 확인 전 응답/제출 오류는 미완료 표식을 보존하고, child 확인 뒤 pending-clear 응답 유실은 이미 발급된 child가 존재하는 안전한 상태다.

ACK 유실과 늦은 commit 모두 이전 후보의 "native ON 시 양쪽 request0"을 재현하는 동일 조건으로 공격했다. 이번에는 native ON에서 request가 복원되고 child 생성 뒤 pending이 닫혔다. source 수정 없이 두 버전에서 확인하여 B-P1-03을 **FIXED**로 판정한다.

## 전체 복구 계약 재검토 및 공격 시나리오

원 base 대비 review 제외17개 변경 파일의 범위와 기존 검토 결과를 연결하고, f0 이후 전체 source/documentation delta를 읽었다. Python 복구 추가207줄, deadline 상한, 공개 UI/model/CSS 및 dev.2 lock/smoke/가이드가 전체 변경 범위다.

1. **native ON→OFF→ON/이미 성공한 child:** 원/native count 합산, 기존 child.parent 검증과 parent-tag limit1 조회, 원 parent 억제, child 잔여 예산이 유지된다. 56개 시험의 기존 native/fallback SUCCESS child 제외와 추가 probe의 native filter 거절이 통과했다. 설정 전환은 가이드대로 기존 daemon/code-server drain을 전제로 하며 서로 다른 설정의 controller 동시 실행에 전역 원자성을 주장하지 않는다.
2. **스토리지 오류/늦은 thread:** 일반 sensor의 전체 조회/검사를 deadline으로 감싸고 결과 반환 전 context cursor를 변경하지 않는다. 늦은 thread의 metadata 저장은 pending 표식을 남기므로 다음 tick에 복원된다. timeout된 thread가 끝나기 전 slot을 계속 보유하는 네 개 상한도 기존 계약 그대로다. 영구 hang 네 개의 process restart/health 경계는 남는다.
3. **cursor와 filter 전환:** native ON은 pending만, OFF는 scope 실패 전체를 순환한다. 현재 cursor보다 앞쪽 pending은 head 순환에서 다시 읽으며 삭제된 cursor는 reset한다. 실제 probe는 반환 cursor로 진행한 후 head로 돌아와 pending false closure를 확인했다. 완료한 row만5초 soft budget checkpoint하고 metadata 오류/10초 timeout에는 incomplete row를 ACK하지 않는다.
4. **부분 선택 확대:** 명시적 op/asset/check, partial resolved graph 및 partial execution plan을 제외하는 두 버전 회귀가 통과했다. pending 표식이 있어도 동일 scope/reason/selection/budget 검사를 적용하여 인계라는 이유로 안전 검사를 우회하지 않는다.
5. **provider/unknown/cancel/잘못된 count:** 명시적 infrastructure reason allowlist와 recorded STEP_FAILURE 제외를 유지한다. ASCII decimal/길이/예산 검사가 native+fallback 모두에 적용된다. 실패 원인이 없거나 취소된 실행을 자동으로 되살리지 않는다.
6. **origin/tag 신뢰:** remote origin의 location/repository/job과 project를 검사하며 originless는 명시적 project/location 태그를 요구한다. pending 태그도 scope나 failure reason을 대체하지 않는다. 수동 Dagster metadata 수정자는 trusted operator라는 경계이며 임의 태그를 외부 권한으로 해석하지 않는다.
7. **중복/상속:** child 생성 이후 pending tag를 닫으며 SUCCESS/CANCELED/FAILED child가 존재하면 parent를 재발급하지 않는다. pending은 job/source 태그 병합 후에도 pop하여 child에 남지 않는다. 결정적 key는 같은 sensor의 재평가를 dedup한다. 수동 발화/별도 controller 경쟁의 provider 보호는 coordinator job limit과 소비자 DB lease가 소유한다.
8. **공개 UI/패키징:** 기존 terminal duration/cron fallback/keyboard region과 dev.2 버전·public export·CSS/lock/tarball 이름·고지·optional Dagster extra가 이번 delta에서 바뀌지 않았다. 가이드는 SQL/receipt/실제 manager instance를 소비자 소유로 유지하며 새로운 pending 복구 계약을 설명한다. 새로운 UI/패키지 계약 결함을 찾지 않았다.

## 남은 불확실성/범위 밖

실제 shared manager YAML/launcher·동시 controller drain 실행·consumer SQL lease·운영 RSS·live 브라우저는 이번 local Python 검증으로 완료되지 않는다. SDK 저장소가 parent의 다중 tag 쓰기를 정상 transaction으로 저장한다는 전제 아래 검증했으며 custom storage가 이를 부분 저장하는 구현은 범위 밖이다. RunRequest 및 실패 event/run metadata를 operator가 수동 삭제하거나 code/config/policy를 바꾸는 행위까지 동일 key 복구 보장으로 확대하지 않는다. metadata/event가 완전히 유실되면 원인 확인 실패를 정상 infrastructure failure로 추측하지 않는 기존 fail-closed 경계가 유지된다.

새 finding 없음. 원본 source 수정 없음.
