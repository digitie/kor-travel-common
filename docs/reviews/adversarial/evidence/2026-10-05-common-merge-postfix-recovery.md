# common merge 후보 독립 post-fix 기능·복구 리뷰 원문

- 리뷰어: /root/review_recovery_final
- 날짜: 2026-10-05
- repository: /mnt/f/dev/kor-travel-common-geo-dashboard
- base: 589a01ef63ff1ce81960e3d531874b5e4c892995
- immutable source candidate: **ab21cc3b7b77e5e6d6cd277ca64840761fc4d7a4**
- 이전 독립 검토 source: 3194a0b6c81d64a75dc937f177588a300944b2af
- 검토 범위 코드 판정: **PASS**
- 기존 B-P1-01: **FIXED**, 신규 actionable finding: 0건.

## 독립성·고정과 범위

새 후보를 Linux git archive로 /tmp/recovery-postfix-independent/common에 새로 추출하고, Geo596b7d177517f3b53cb811e36720d9af9bba582b도 같은 방식으로 별도 고정했다. 원본 미커밋 변경을 복사하거나 수정하지 않았다. 현재 HEAD의 후속 문서 커밋을 code source로 사용하지 않았다. 기존 AGENTS.md 지침과 관련 runbook의 규칙을 유지하며 변경된 채택 가이드를 검토했다. 다른 현행 리뷰어 결과나 부모 journal 판정은 읽지 않았다.

기존 Python /home/digitie/dev/kor-travel-geo-codex-dagster-common-test/.venv/bin/python을 설치 변경 없이 재사용했고 PYTHONPATH로 본인 fixed common/src, fixed Geo/src, fixed Geo Dagster/src를 주입했다. 추가 테스트는 본인 /tmp에서만 편집했다. 제품 source는 수정하지 않았다.

본인 실행만 아래에 집계한다. 부모가 제공한 이전 PASS나 실제 PG/UI 근거는 합산하지 않았다. UI, 외부 서비스/DB, 운영 daemon 장애 주입, package 설치, 전체 저장소 gate, CI는 **NOT_RUN(이번 독립 재검토의 범위 밖)**이다.

## B-P1-01 closure — 추가 IO 전에 complete checkpoint 저장

이전 finding은 마지막 STEP_FAILURE 검증까지 8.2초가 걸린 뒤 active run 조회 2.1초를 더 기다려 outer 10초 timeout을 넘고 같은 tail을 반복하는 문제였다.

수정 위치: packages/py/kor-travel-common/src/kortravelcommon/dagster.py:288–293. 마지막 step 검증 직후 subprocess evidence와 예산을 검사해 complete phase·cursor·RUN_FAILURE storage ID를 추가 native/dedup/active IO 전에 반환한다. 기존 인계 직전 budget 검사도 남아 있다.

본인 test_closure.py::test_slow_postscan_metadata_closure는 이전과 동일한 SQLite instance, 실제 RUN_FAILURE 3.1초, STEP_FAILURE 두 페이지 각각 5.1초, active run 조회 2.1초를 사용했다.

- 첫 tick: incomplete checkpoint.
- 두 번째 tick: 최종 tail까지 검증하고 complete checkpoint. active run 조회는 아직 **0회**.
- 세 번째 tick: scope와 중복·active를 검사해 **RunRequest 1건**, 잔여 native retry 태그 0.
- 전체 step 페이지 호출: **[None, "tail"]**, tail 중복 읽기 없음.
- 출력: CLOSED common: 3 ticks, 1 request, 2 step pages, no postscan RPC before complete checkpoint.

따라서 이전 P1의 실제 지연 재현은 정상 복구로 바뀌었고 FIXED로 판정한다.

## 추가 확인

- 완료 checkpoint 조회는 RUN_FAILURE+STEP_FAILURE 중 최신 1건을 읽는다. 늦은 provider STEP_FAILURE가 새 RUN_FAILURE 없이 추가되어도 completed cursor와 cold evaluation 모두 요청을 발급하지 않는다. 새 failure storage ID의 기존 본인 시험도 통과했다.
- 최신 RUN_FAILURE storage ID가 바뀌면 incomplete/complete phase 모두 첫 step 페이지부터 다시 검증하여 provider failure를 차단한다.
- tail storage 오류 후 cursor를 소비하지 않고 같은 tail에서 복원한다.
- complete handoff ack 유실 후 native retry ON으로 바뀌어도 동일 key의 요청으로 복원하고 step tail을 다시 읽지 않는다.
- 7.999초/8.0초의 최종 budget 경계, native 중복 방지, scope/부분 선택, provider/op 실패 제외, retry1 예산, 실제 child crash 회귀가 통과했다.
- complete phase가 새로운 STEP_FAILURE를 만나면 재사용을 중단하는 fail-closed 동작이며, 새로운 provider failure를 자동 재시도하지 않는다.

## 본인 수행 결과와 negative control

1. fixed common packages/py/kor-travel-common에서 python -m pytest -q tests/test_recovery.py tests/test_child_crash.py:
   **67 passed in 65.84s**.
2. /tmp/recovery-postfix-independent에서 test_closure.py test_independent.py test_geo_extra.py:
   **19 passed in 29.60s** 중 common 사례는 7개, Geo 사례는 12개다. Geo PASS를 common gate에 합산하지 않았다.
3. same closure test에 common source만 이전 immutable3194a0b로 바꾼 별도 process:
   **1 failed in 19.41s**, 최종 tail 뒤 DeadlineExceeded. 새 테스트가 구결함을 실제로 판별하는 negative control이다. 예상 실패를 product PASS로 세지 않는다.

추가 시험 실행:
```bash
cd /tmp/recovery-postfix-independent
PYTHONPATH=/tmp/recovery-postfix-independent/common/packages/py/kor-travel-common/src:/tmp/recovery-postfix-independent/common/packages/py/kor-travel-common/tests:/tmp/recovery-postfix-independent/geo/src:/tmp/recovery-postfix-independent/geo/kor-travel-geo-dagster/src /home/digitie/dev/kor-travel-geo-codex-dagster-common-test/.venv/bin/python -m pytest -q -s test_closure.py test_independent.py test_geo_extra.py
```

## 증거 원문

- /tmp/recovery-postfix-independent/common-test.log — SHA256 c748adfb44396bfc55f953aa9659ab75c01d093a7461687976df6afc2d6854cd
- /tmp/recovery-postfix-independent/postfix-tests.log — SHA256 8f5a68d85e685a81ec830ccb26f48fe29f9be946845ca5f827ba4f16c77f4f29
- /tmp/recovery-postfix-independent/test_closure.py — SHA256 15d75e90edac5528ced8fed38d41b899e2f743f6303b78aa85efe94b51cff696
- /tmp/recovery-postfix-independent/test_independent.py — SHA256 257b7f7051ddec33b8eb6e18a186d5627d364413959b609d2f7b303307c20933
- /tmp/recovery-postfix-independent/old-common-negative-control.log — 동일 closure의 구후보 실패 원문.
- /tmp/recovery-postfix-independent/run_negative.py — source 교체만으로 negative control을 실행하는 본인 script.

이 PASS는 고정 코드의 기능·복구 범위에 대한 판정이다. 미실행 외부 gate나 전체 merge 승인으로 확대하지 않는다.
