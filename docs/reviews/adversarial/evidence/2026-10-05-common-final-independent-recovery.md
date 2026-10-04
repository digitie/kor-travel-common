# common 독립 기능·복구 리뷰 원문

- 리뷰어: recovery reviewer (/root/review_recovery_final)
- 날짜: 2026-10-05
- 고정 repository: /mnt/f/dev/kor-travel-common-geo-dashboard
- base: 589a01ef63ff1ce81960e3d531874b5e4c892995
- candidate: 3194a0b6c81d64a75dc937f177588a300944b2af
- 판정: **BLOCK**
- 열린 finding: P1 1건. 제품 코드 수정 없음.

## 독립성·실행 경계

두 저장소를 Linux git archive로 /tmp/recovery-final-independent/{common,geo}에 추출했다. 기존 checkout의 미커밋 변경은 복사·수정하지 않았다. 기존 /home/digitie/dev/kor-travel-geo-codex-dagster-common-test/.venv/bin/python은 실행만 재사용했으며 설치를 바꾸지 않았다. 고정 common source와 고정 Geo source를 PYTHONPATH에 명시했다. 다른 현행 리뷰어 보고서와 부모 journal의 판정은 보지 않았다. 부모가 제공한 65 PASS는 합산하지 않았다. 아래 65 PASS는 본인이 고정 사본에서 별도 실행한 결과다.

범위는 Python 복구 기능이며 UI, package 설치, CI, 운영 daemon/worker 장애 주입, 외부 DB/서비스는 NOT_RUN이다. 실제 Dagster multiprocessing crash fixture와 SQLite Dagster storage는 로컬에서 실행했다.

## B-P1-01 — 완료 phase 저장 전에 metadata RPC를 기다려 같은 tail을 영구 반복한다

- 위치: packages/py/kor-travel-common/src/kortravelcommon/dagster.py:319, :325
- 관련 위치: :275 마지막 STEP_FAILURE 페이지 처리, :306 native/fallback child 조회, :430 전체 10초 deadline.
- 상태: OPEN
- 영향: 유한한 정상 metadata 지연만으로 자동 복구가 진행되지 않는다. 느린 최종 step 페이지까지 이미 검증했어도 complete checkpoint가 sensor cursor에 남지 않아 다음 tick이 같은 tail을 다시 읽는다. 복구 진행 보장이라는 기능 요구를 깨므로 P1로 판단한다.

### 실제 재현

본인 test_findings.py::test_slow_postscan_metadata_loses_complete_checkpoint에서 실제 time.sleep을 사용했다.

1. SQLite DagsterInstance.local_temp에 멱등 job의 RUN_EXCEPTION / DagsterSubprocessError 실패를 기록했다.
2. RUN_FAILURE 조회를 매번 3.1초, STEP_FAILURE를 두 페이지 각각 5.1초로 설정했다. 각 step 기록은 FRAMEWORK_ERROR / ChildProcessCrashException이며 provider/user 실패가 없다.
3. 첫 tick은 첫 페이지 뒤 incomplete steps cursor를 정상 저장한다.
4. active run 조회 하나만 2.1초로 설정했다. 최종 페이지가 끝난 시점은 약 8.2초지만 코드가 complete phase 반환 전에 active 조회를 수행한다.
5. 두 번째와 세 번째 tick 모두 외부 10초 deadline이 만료되어 DeadlineExceeded를 발생시켰다. 늦게 반환되는 complete 결과는 sensor에 반영되지 않았다.
6. 요청은 0건, cursor는 첫 tick의 incomplete cursor, step 호출은 [None, "tail", "tail"]이었다. 각 지연은 유한하며 예외/고장난 storage를 주입하지 않았다.

출력: PROVEN common: complete tail was scanned twice; no request and unchanged incomplete cursor

권고: 마지막 step 페이지 검증 직후, 추가 native child/dedup/active RPC에 들어가기 전에 남은 예산을 확인하고 complete phase와 해당 RUN_FAILURE storage ID를 반환한다. 다음 tick에서 tail을 읽지 않고 scope·budget·중복을 재검증해야 한다. metadata RPC 이후의 현재 체크도 유지할 필요가 있다.

## 확인한 정상 동작

- 명시적으로 멱등성이 허용된 job만 sensor 적용 가능하고 읽기 전용 worker 장애의 retry 예산이 1회로 제한된다.
- 일반 op/provider 실패, user_failure_data, 알 수 없는 실패, 다른 location/repository/job origin, 부분 op/asset/check/plan 선택은 재실행으로 확대하지 않는다.
- native child와 완료된 fallback child가 parent 예산을 다시 사용하지 않는다. pending handoff가 저장 응답 유실과 native OFF→ON을 견딘다.
- 실패 이력은 limit=100이며 느린 중간 페이지 뒤 cursor가 저장된다.
- 기본 RUN_FAILURE 3.1초 + STEP_FAILURE 5.1초 두 페이지 사례는 독립 실행한 기존 테스트에서 3 tick 뒤 요청 1건, step 조회 2회, parent metadata write 1회였다. B-P1-01은 여기에 정상 active 조회 2.1초를 추가한 별도 경계다.
- 추가 본인 테스트: 새 RUN_FAILURE storage ID는 incomplete/complete 두 phase 모두 무효화하고 첫 step 페이지부터 검증하며 이후 provider 실패를 차단한다.
- checkpoint 뒤 tail 조회 오류는 cursor를 소비하지 않고 같은 tail에서 복원된다.
- complete checkpoint 상태의 handoff ack 유실 뒤 native를 켜도 동일 request key로 복원되고 tail을 다시 읽지 않는다.
- 시간 7.999초/8.0초 경계에서 request 발급/complete checkpoint 반환이 각각 정확했다. 이는 추가 RPC 이전 예산 확인을 검증한 것은 아니다.

## 본인 실행 결과

공통 실행 환경:
```bash
PYTHONPATH=/tmp/recovery-final-independent/common/packages/py/kor-travel-common/src:/tmp/recovery-final-independent/geo/src:/tmp/recovery-final-independent/geo/kor-travel-geo-dagster/src
/home/digitie/dev/kor-travel-geo-codex-dagster-common-test/.venv/bin/python
```

- 고정 common packages/py/kor-travel-common에서 python -m pytest -q tests/test_recovery.py tests/test_child_crash.py: **65 passed in 43.35s**.
- /tmp/recovery-final-independent/test_independent.py 전체: **11 passed in 2.65s** 중 common 사례는 6개, Geo 사례는 5개다. 두 저장소 PASS 수를 합쳐 common gate로 세지 않는다.
- test_findings.py 전체: **2 passed in 30.79s**는 common 1건과 Geo 1건의 결함이 실제 존재함을 단언한 재현 시험이다. 제품 정상 동작 gate로 세지 않는다.
- mutation-common: 임시 별도 source 사본에서 failure_storage_id 무효화 분기를 제거하고 새 failure 검증 2개를 실행하니 **2 failed in 1.40s**. 각각 old cursor 재사용과 complete phase의 step 조회 생략을 단언에서 잡았다. candidate 사본은 변경하지 않았다.

증거:
- /tmp/recovery-final-independent/common-test.log SHA256 6c67882a6bce99a43a36f29f8e410abd766e4bd07417e8c1c839ebc0ececfbfc
- /tmp/recovery-final-independent/test_independent.py SHA256 ca59fd4b79131c2a263b5d9552786accdc5b3b9278f366b46657c69fe831bbb5
- /tmp/recovery-final-independent/test_findings.py SHA256 bfffabaed39dbb0787cd274f3340427b94dab98ab93ae1faffb116bac56d385f
- /tmp/recovery-final-independent/findings-test.log SHA256 536d307a683a0178e4774305650e0a04229411564e6985a5774541d8bfafe0f9

현재 candidate의 B-P1-01을 수정하거나 전제를 반증한 뒤 동일 지연 사례와 기존 65개를 재실행하여 독립 post-fix 검토해야 한다.
