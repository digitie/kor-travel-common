<!-- SPDX-License-Identifier: GPL-3.0-only -->

# 공통 복구 센서 checkpoint 기능 독립 리뷰 — Popper 원본

실행 ID: POPPER-COMMON-CHECKPOINT-F801F01B-20261005-071944

시작: 2026-10-05T07:19:44.509314+09:00. 종료: 2026-10-05T07:25:07.042375+09:00.

판정: **FAIL**. 두 느린 step 페이지를 이어 읽는 기본 수정은 통과했으나, 완료 이력 이후 인계가 같은 checkpoint에서 반복 보류되는 추가 정상 지연 경계 `B-C-P1-01`이 재현됐다. 부모의 예정 수정이나 다른 리뷰어 결과는 이 원본에 반영하지 않았다.

## 고정 대상과 격리

- 저장소: `F:\dev\kor-travel-common-geo-dashboard` / `/mnt/f/dev/kor-travel-common-geo-dashboard`.
- 실제 base: `92ebfa60ef976d830c08b353de633103650175ad`.
- 실제 candidate: `f801f01b2dc34b642a64bbf847fa268ac172e4ed`.
- Linux Git 고정 객체의 전체 delta를 읽었다. 본인 `git archive` 사본은 `/tmp/popper-common-checkpoint-f801f01b-20261005`이다.
- 재사용 가상환경은 Python 3.12.13 / Dagster 1.13.24이며, 고정 common 소스를 `PYTHONPATH`로 우선했다. 원본 저장소·부모 mirror·설치 환경·운영 DB·외부 provider를 변경하지 않았다. 시험 저장소는 본인 local SQLite DagsterInstance만 사용했다.
- 다른 리뷰어 결과/원문과 부모 실행 로그를 읽지 않았다. 이전 본인 테스트만 재사용했다. UI 제품 코드 및 vendor는 이 delta에서 변하지 않았다.

## EXECUTED

1. 후보 공통 원래 테스트: **64 PASS, 23.71초**. 실제 multiprocess `os._exit(42)` fallback fixture와 두 STEP_FAILURE 페이지 각각 실제 5.1초 지연의 재개 테스트를 포함한다. 첫 partial tick의 태그 쓰기 0, 다음 tick 요청 1 및 child 잔여 native 예산 0 조건도 통과했다. 로그: scratch의 `original-tests.log`.
2. 이전 본인 실제 SQLite 추가 경계 테스트: **8 PASS**. provider 오류가 실제 102개 이벤트 중 두 번째 페이지에 있을 때 차단, page2 저장소 오류 후 cursor 미소비/복원, native/fallback 예산, 명시 선택 제외 및 native ON pending 인계를 확인했다.
3. 새로운 checkpoint 재개 경계: **6 PASS, 2.89초**. 최초 partial checkpoint 뒤 provider 오류 제외, 조회 오류와 복원, native ON 미인계 보류, project 변경, 손상된 retry 예산, run 삭제를 검사했다. 이 여섯 테스트는 5초 작업 예산의 분기를 가상 monotonic 값으로 만들었으며 실제 5.1초 RPC 시간 시험이라고 주장하지 않는다. 로그: `independent-resume-tests.log`.
4. 실제 정상 지연의 완료 checkpoint 시험: **1 FAIL**. RUN_FAILURE 조회에 실제 3.1초, STEP_FAILURE 페이지 조회에 실제 5.1초를 더했고, 세 sensor tick을 실행했다. 앞의 8건과 함께 실행한 결과는 **8 PASS / 1 FAIL, 27.82초**였다. 로그: `independent-regressions.log`.

본인 추가 회귀는 합계 **14 PASS / 1 FAIL**이다. 원래 64건과 구분했다. 위 지연은 본인 fixture의 read 경계에서만 주입했으며 외부 서비스나 운영 DB를 느리게 만들지 않았다.

## B-C-P1-01 — 완료 checkpoint에서도 느린 빈 tail을 재조회해 인계가 영구 보류된다

위치: `packages/py/kor-travel-common/src/kortravelcommon/dagster.py:245-275`, 특히 `315-318`; checkpoint run 재개 `358-360`.

시나리오: 유한한 crash 이력 검사는 끝났지만 RUN_FAILURE 조회 3.1초와 STEP_FAILURE 조회 5.1초가 함께 필요하다. 각 RPC는 전체 10초보다 짧고 tick도 약 8.2초에 정상 종료한다. 그러나 metadata 인계 전 8초 guard에서 완료된 마지막 event cursor를 다시 `_StepCheckpoint`로 저장한다. checkpoint에는 검증 완료 phase가 없으므로 다음 tick도 빈 tail을 다시 5.1초 동안 조회한다. 같은 8초 guard에 도달해 동일 checkpoint를 다시 저장한다.

재현: 실제 local SQLite store에 framework ChildProcessCrashException STEP_FAILURE 102개를 저장했다. 실제 `get_records_for_run()` 앞에 위 지연만 추가했다. 본인 `test_popper_slow_completion.py`에서 실제 `evaluate_tick()`을 세 번 실행한 결과:

```text
tick1: STEP_FAILURE 100건, has_more=True, checkpoint crashed_steps=100
tick2: 나머지 2건, has_more=False, checkpoint crashed_steps=102
tick3: 0건, has_more=False, tick2와 같은 checkpoint
요청 합계: 0
metadata 태그 쓰기: 0
```

tick2 이후 같은 정상 지연이면 더 검사할 이력이 없는데도 매 tick 같은 cursor가 반복된다. 세 tick 내 인계 요청이 있어야 한다는 assertion이 실패했다. 이는 outer deadline 초과나 RPC 예외가 아니라 정상 반환 뒤의 기능 정체다. 실제 SQLite 이력 및 cursor를 사용했으며 provider 오류를 섞거나 retry 예산을 손상시키지 않았다.

영향: 정상적으로 유한한 이력을 다 읽어도 해당 job의 실패를 재예약하지 못한다. checkpoint는 이 run 하나만 재개하므로 같은 센서의 다른 실패 run 처리도 지연된다. 부모 pending 쓰기를 늦게 수행하지 않는 보호는 확인됐으나 자동 복구의 진행성은 보장되지 않는다.

권고 및 closure 조건: 검증을 완료한 단계와 계속 읽어야 하는 단계를 구분해 보존한다. 완료된 증거 재사용은 같은 failure event/실행 범위라는 조건을 확인해야 하며, 새 실패 이벤트나 provider 이력이 안전 검사 없이 누락돼서는 안 된다. 다음 tick에서는 불필요한 느린 빈 tail 반복 없이 scope/예산/child/active 검증과 인계를 진행할 수 있어야 한다. 동일 3.1초+5.1초 fixture가 유한 tick 내 요청 1개를 내고, 변경된 failure event 및 provider 오류는 다시 검사·차단하는 회귀가 필요하다.

상태: **OPEN, P1**. 부모의 후속 수정 예정 통보만으로 닫지 않았다. 최초 child-crash 분류 `B-G-P1-03`은 이 finding과 별개이며 정상 지연 환경의 실제 child fixture는 이번 후보에서도 통과했다.

## READONLY 및 확인한 계약

checkpoint에는 run ID·event cursor·crash 수를 저장하고, 재개 시 현재 run을 다시 조회한다. project/location/job/명시 선택 및 실패 원인의 가드는 유지됐다. provider 혼합 오류를 발견하기 전에는 재시도 요청이나 부모 native 억제 태그를 쓰지 않았다. 저장소 오류는 실패 tick의 cursor를 소비하지 않았으며 복원 후 다시 진행했다.

native ON이고 pending 인계가 없으면 재개된 run도 자동 재예약하지 않는다. 손상된 native/fallback retry 횟수는 차단됐고, 삭제된 run의 checkpoint는 run 부재를 정상 처리했다. 유한 페이지당 100건과 기존 bounded-call thread 상한은 유지됐다.

UI smoke manifest/lock/prepare-lock의 dev.2→dev.3 파일명·version 정정과 신규 fixture SPDX를 읽었다. UI 제품 코드와 공용 공개 타입은 이 delta에서 변경하지 않았다. 실제 packed smoke 재빌드는 수행하지 않았다.

## NOT_RUN

Dagster 최소 1.9 재실행, 실제 shared daemon/native ON worker 통합, PostgreSQL 및 domain 게시, geo 후속 후보, UI/browser/live E2E, CI 직접 실행, RSS/동시 run 부하 및 wheel/npm 재설치는 수행하지 않았다. 부모의 64 PASS 결과를 본인 직접 결과에 합산하지 않았다.

P0/P2/P3의 추가 확정 finding은 없다. 새 immutable 후보에서 완료 phase 및 새로운 실패 이벤트 회귀를 독립 재검증해야 한다. 이전 원본 보고서들은 변경하지 않았다.
