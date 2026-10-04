# common 최종 evidence 후보 독립 기능·복구 리뷰 원문

- execution ID: /root/review_recovery_final / recovery-evidence-independent
- 전문 영역: Python Dagster 기능·복구·checkpoint·시간 예산
- 검증 시작: 2026-10-04T23:02:31Z (격리 사본 directory 생성 시각)
- 검증 종료: 2026-10-04T23:07:47Z
- 작성일: 2026-10-05 KST
- repository: /mnt/f/dev/kor-travel-common-geo-dashboard
- manifest base: 589a01ef63ff1ce81960e3d531874b5e4c892995
- 실제 source candidate: **73e3ff8b9398e533806d2d1a8435292570169de3**
- 직전 검토 source: ab21cc3b7b77e5e6d6cd277ca64840761fc4d7a4
- 검토 범위 판정: **PASS**
- 열린 actionable finding: 0건. 기존 본인 B-P1-01: **FIXED 유지**.
- review 분류 의견: **FULL**, review closure artifact 예외 **부적용**.

## 독립성과 수행 범위

새 immutable source를 Linux git archive로 /tmp/recovery-evidence-independent/common에 추출했다. Geo도4c59efe3a778fb160b7d0a4fde2ca08967bf1531에서 별도 archive했다. original dirty checkout, 부모 후속 문서 HEAD, 설치된 editable source를 검토 source로 쓰지 않았다.

기존 /home/digitie/dev/kor-travel-geo-codex-dagster-common-test/.venv/bin/python을 실행만 재사용하고 본인 fixed common/src + Geo/src + Geo Dagster/src를 PYTHONPATH에 지정했다. product code는 수정하지 않았다. /tmp 테스트 script와 본인 보고서만 작성했다. 다른 현행 리뷰어 원문·판정과 부모 journal 결과는 열람하지 않았다. 이전 본인 원문은 수정하지 않았다.

본인 실행 결과만 아래에 기록하며 제공된 69 PASS를 합산하지 않았다. SQLite local_temp, 로컬 실제 Dagster multiprocessing crash, Fake SQL이 본인 수행 범위다. external PG/PostGIS·RustFS·서비스, UI, 운영 daemon/worker 장애 주입, 전체 저장소 gate, package 설치, CI는 **NOT_RUN(이번 reviewer 범위 밖)**이다.

## 전체 delta 검토와 full/closure 판단

base→최종의 Python 복구 delta는 dagster.py, tests/crash_fixture.py, tests/test_child_crash.py이다. 이전 본인 검토에서 pagination/시간 예산·scope·native/fallback 중복·멱등 retry 예산 및 실제 child crash를 검토했고 새 고정 source에서 관련 전체 69개를 다시 실행했다. UI 부분은 이 reviewer의 전문 범위가 아니므로 이번 PASS에 포함하지 않는다.

직전 ab21→최종의 모든 delta 세 파일을 확인했다:

1. dagster.py: 마지막 STEP storage ID를 checkpoint에 추가한다. 최신 failure ID와 저장된 RUN/STEP 최대 ID가 일치할 때만 complete를 재사용하며 최신 STEP의 child crash 속성도 검사한다. 새로운 failure는 partial로 전환하고 다음 tick에 실제 RUN_FAILURE+cursor 이후 step 이력을 검증한다.
2. tests/test_child_crash.py: 늦은 child를 RUN_FAILURE 뒤/완료 checkpoint 뒤에 기록하는 실제 SQLite·3.1/5.1초 회귀 두 사례를 추가한다. provider 거부 시험은 partial 전환 다음 tick까지 검증한다.
3. docs/runbooks/dagster-adoption.md: 6필드 증거·partial 재검증·3/5필드 이전 형식 계약을 코드와 일치시킨다.

source 동작과 runbook 규범이 변경되어 단순 review closure artifact가 아니다. common agent-workflow §5의 runbook 비면제 및 code/build/config 면제 제외 조건에 따라 FULL 재검토가 맞다는 독립 의견이다. 최종 merge gate 전체 판정은 담당자의 다른 전문 reviewer 결과·필수 gate와 함께 판단해야 한다.

## 공격한 경계와 결과

- 실제 SQLite event 저장으로 RUN_FAILURE 뒤 정상 child STEP가 추가되는 경우: first complete checkpoint에 step_storage_id가 RUN id보다 커지고 최신 STEP evidence를 재사용하여 요청 1건·metadata write 1회로 진행한다.
- complete checkpoint 뒤 정상 child STEP가 추가되는 경우: 다음 tick은 요청 없이 partial로 전환하고 실제 RUN header를 확인한 뒤 cursor 이후 step만 검사한다. 정상 child-only evidence는 다시 complete를 거쳐 요청 1건으로 진행한다.
- late provider failure와 child exception 이름에 USER_CODE_ERROR가 붙은 실패: 요청/metadata write 모두 0건. 정상 child와 provider를 class 이름만으로 혼동하지 않는다.
- 3/5필드 이전 checkpoint에 provider 기록을 cursor보다 앞에 둔 사례: RUN header부터 조회하고 STEP cursor=None으로 전체 이력을 재검증하여 요청을 거부한다. 이전 completed boolean만 신뢰하지 않는다.
- 6필드 step ID의 음수·bool·문자열·None은 ValueError로 거부한다.
- latest STEP가 검증된 ID와 같은 returned storage response라도 error source/class/user_failure_data를 각각 바꾸어 Fake response를 주면 complete evidence를 재사용하지 않고 요청을 거부한다. 이는 actual SQLite event mutation이 아니라 metadata 응답 불일치 주입이다.
- B-P1-01의 실제3.1초 RUN header+5.1초 두 step page+2.1초 active 조회: 3tick 후 요청1건, step page2회. complete 저장 tick의 active IO0회. 앞선 starvation 재현은 계속 FIXED다.
- 새로운 RUN_FAILURE ID에서는 complete→partial 다음 tick에 새로운 실제 header를 확인하여 처음부터 provider 검증한다.
- checkpoint 이후 storage 오류 복원, handoff ack 유실/native OFF→ON, 7.999/8.0초 budget 경계, native child 중복과 재시도1 예산, scope·부분선택 및 provider/op 제외 회귀를 유지했다.

새 actionable 문제는 발견하지 않았다. 이 판단은 복구 코드 범위의 독립 검토이며 운영 daemon 설정·외부 storage의 locking/성능을 실측한 것은 아니다.

## 본인 실행 결과와 시험 판별력

- fixed common에서 python -m pytest -q tests/test_recovery.py tests/test_child_crash.py:
  **69 passed in 100.48s**. 실제3.1/5.1초 late-child 두 회귀와 os._exit(42) fixture를 포함한다. 제공된 수치의 복제가 아니라 본인 새 사본 실행이다.
- 본인 test_evidence.py test_closure.py test_independent.py test_geo_extra.py:
  **29 passed in 30.95s** 중 common17개/Geo12개.
- 본인 test_latest_attributes.py:
  **3 passed in 1.61s**, common latest child source/class/user 속성 검증.
- common 본인 추가 사례는 합계20개이며 Geo12개를 common gate로 세지 않는다.
- 같은 본인 SQLite late-child before/after 시험 두 개에 source만 이전 ab21로 바꾼 negative control:
  **2 failed, 8 deselected in 1.48s**. 둘 모두 요청0건 vs 기대1건 단언에서 실패했다. 예상 failure를 product PASS로 집계하지 않는다.
- 최초 추가 suite는1FAIL/28PASS였다. 본인 이전 시험이 새로운 RUN_FAILURE를 same tick에서 full scan한다고 기대했기 때문이다. 문서화된 새 partial→next tick 계약에 맞추어 first tick의 partial/no-request와 next tick의 cursor=None provider 검증을 모두 단언하도록 본인 테스트만 수정한 뒤29PASS를 확인했다. initial failure 로그를 보존하며 product defect로 숨기지 않는다.
- 두 immutable base→candidate git diff --check는 exit0. 다른 필수 gate의 실행을 뜻하지 않는다.

추가 suite 명령:
```bash
cd /tmp/recovery-evidence-independent
PYTHONPATH=/tmp/recovery-evidence-independent/common/packages/py/kor-travel-common/src:/tmp/recovery-evidence-independent/common/packages/py/kor-travel-common/tests:/tmp/recovery-evidence-independent/geo/src:/tmp/recovery-evidence-independent/geo/kor-travel-geo-dagster/src /home/digitie/dev/kor-travel-geo-codex-dagster-common-test/.venv/bin/python -m pytest -q -s test_evidence.py test_closure.py test_independent.py test_geo_extra.py
```

## 원문 evidence와 SHA256

- common-test.log: 3efc510b4dca6455711a9bd9d887e3af414ea73097ae8efe478c43c7e1e8f048
- independent-tests.log: 8a7589ae87039f59bc73efbd1fbe097c46640a494fc60f7d6f852571eaef67a4
- latest-attributes.log: d48a58c1c02393343bd55f586135f5afc939b24920f9b4e15f042f5b9160497c
- test_evidence.py: 8aa33ba1df58b13fa4320b7388057c1f449a13b8e17828f5367fcaedaec1f0ec
- test_latest_attributes.py: 4c995c1dc5199e2ddecdc06ad8087b44896ce2ebc0821e177acd1fa816a0db62
- test_independent.py: fc73be56786f7e7bc7909b4c4f0c28216c00da8dcfb482f3904d077f741283ae
- old-common-negative-control.log: 7cdfdb301d407ab91c03cea71d042ab587bf039739beccbd80c8cd7fe3a62e9e

위 파일은 /tmp/recovery-evidence-independent/ 아래에 있다. independent-before-adaptation.log에 초기 기대 불일치 결과가 남아 있다. run_negative.py는 candidate test를 이전 source에서 그대로 실행한다.

최종 기능·복구 코드 판정: **PASS**. 미실행 외부/전체 gate에 대한 승인으로 확대하지 않는다.
