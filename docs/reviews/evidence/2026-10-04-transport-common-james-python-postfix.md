<!-- SPDX-License-Identifier: GPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie) -->

# Common Python fallback 수정 후보 독립 재리뷰 — James 원본

- 실행 ID: `james-common-python-postfix-7ee001-20261004T063539Z`
- 시작: 2026-10-04 06:35:39 UTC / 15:35:39 KST
- 종료: 2026-10-04 06:42:08 UTC / 15:42:08 KST
- 전문 범위: 소비자 공개 계약·UI/API/CSS와 Python 이벤트 복구·cursor·deadline·중복 예약 경계.
- 기준선: `090f98429453d8882150eb9e56ccae98e0e353a2`.
- 수정 전 본인 검토 후보: `b324b0afdc27f268e6e6aaee1f6d7d2f42e4743b`.
- 실제 재검토 후보: `7ee00152c2f7b3877ff3bedcd61a58ec15122d89`.
- 저장소: `F:/dev/kor-travel-common-recovery`.
- 격리: Windows Git 고정 객체만으로 전체 변경 목록·관련 소스를 읽었다. 모든 delta 조회에서 `:(exclude)docs/reviews/**` 또는 구현 파일의 명시적 pathspec을 사용했다. 상대 보고서·결과를 읽지 않았으며 기존 본인 원본도 변경하지 않았다. 구현 소스·설치·venv를 수정하지 않고 이 evidence 원본만 작성한다.

## 검토 범위와 실행 근거

원래 기준선 대비 전체 변경 목록과 Python 모듈·테스트·공개 가이드·CHANGELOG를 검토했다. b324 이후 source 변경은 `dagster.py`와 해당 테스트이며 UI runtime·CSS·deadline 모듈은 이전 독립 검토 후보와 같다. 일반 polling sensor로 바뀌었고, 실패 실행 100건 조회부터 이벤트·scope·budget·active 검사와 SensorResult 생성까지 하나의 bounded call에서 처리한다. repository 인자는 additive keyword로 제공된다.

고정 Git 객체의 두 모듈과 테스트를 JSON stdin으로 WSL에 전달했다. 임시 모듈·임시 테스트 파일을 사용하여 움직이는 worktree source를 import하지 않았다. 기존 `/tmp/transport-recovery-venv`(Python 3.13/Dagster 1.13.24) 및 `/tmp/common-dagster-floor`(Python 3.11/Dagster 1.9.0)를 변경 없이 사용했다. 각 버전에서 동일한 고정 후보 테스트를 49개씩 직접 실행했다.

- Dagster 1.13.24: `49 passed in 6.44s`.
- Dagster 1.9.0: `49 passed in 7.08s`.
- skipped/0 test를 통과로 집계하지 않았다. 49개의 고유 시나리오를 두 버전에서 각각 실행한 결과다.

## 본인 이전 finding closure

| ID | 재검토 위치·결과 | 판정 |
| --- | --- | --- |
| A-P1-01 | `dagster.py:222–270`. 일반 `@sensor`가 예외를 전달하며 cursor를 변경하는 SensorResult는 정상 완료 후에만 반환한다. 실제 이벤트 저장·`evaluate_tick`에서 metadata 예외 후 같은 context cursor 유지·복구 후 RunRequest 생성 테스트를 두 버전에서 실행했다. 원래 run_failure_sensor의 error reaction/cursor 소비 경로를 제거했다. | FIXED |
| A-P2-02 | `dagster.py:222–270`. run 목록·cursor 존재 확인·실패/step 이벤트·scope·active 조회를 callback 내부로 옮겼다. metadata 대기·timeout 뒤 cursor 미전진 및 복구 후 재평가 테스트를 두 버전에서 실행했다. worker는 context cursor를 직접 변경하지 않는다. | FIXED |
| A-P2-03 | `dagster.py:200–214`. 원본의 `dagster/` 태그를 제거한 뒤 job 정의·현재 policy·위치·부모·budget을 적용한다. 이전 auto_retry_run_id/will_retry/resume/failure 태그 제거, custom source 태그 보존, fresh child가 resume retry가 아님을 두 버전에서 검증했다. | FIXED |

이전 P1은 닫혔다. 추가 P0/P1은 확인하지 않았다.

## 새 finding

### A-P2-04 — 100건 페이지의 누적 조회 시간이 deadline을 넘으면 cursor가 영구 정지함

- 위치: `packages/py/kor-travel-common/src/kortravelcommon/dagster.py:229–259,267–270`; `docs/runbooks/dagster-adoption.md`의 100건 순회·전체 조회 10초 계약.
- 근거: 요청이 없는 페이지는 100건을 모두 조회·검사해야 SensorResult가 반환된다. 각 조회는 정상 반환해도 누적 시간이 10초를 넘으면 완료된 검사까지 전부 버리고 cursor를 유지한다. 다음 tick은 같은 페이지를 처음부터 처리한다. 원래 metadata 장애의 이벤트 유실은 해결됐지만, 느린 정상 응답에서 진전이 없는 새 실패 형태다.
- 실제 재현: 고정 후보 `SensorDefinition.evaluate_tick`과 isolated `DagsterInstance`를 사용했다. 첫 페이지에 scope가 맞는 100개 FAILED run을 주입했고, 각 RUN_FAILURE 조회가 0.12초 후 정상 UNKNOWN 이벤트를 반환하도록 했다. UNKNOWN은 안전하게 생략되는 기록이므로 전체 페이지를 확인해야 한다. 실제 후보의 10초 timeout을 단축하지 않고 두 tick을 실행했다.
- 출력 1: `tick 1 elapsed 10.0 cursor head records_started 84`; 이어서 `worker_finished 100 next_tick_will_repeat_same_page`.
- 출력 2: `tick 2 elapsed 10.0 cursor head records_started 84`; 이어서 `worker_finished 100 next_tick_will_repeat_same_page`.
- 각 worker는 약 12초 뒤 100개 조회를 모두 끝냈지만 그 SensorResult는 이미 버려졌다. cursor는 두 tick 모두 `head`로 유지됐다. 호출 자체의 예외나 영구 정지 없이도 재현되었다. 지연은 시험에서 주입했으며 운영 DB의 실제 latency를 측정했다는 뜻은 아니다.
- 영향: 100개의 생략 대상 실패가 앞 페이지를 차지하고 metadata 왕복/저장이 느리면 센서가 계속 timeout된다. 페이지 뒤의 복구 대상과 이후 순회로 나아가지 못한다. 프로세스당 4개 상한은 메모리를 제한하지만 순회 진행을 복구하지는 않는다.
- 최소 수정 권고: outer deadline보다 이른 내부 처리 시간 예산을 두고, 이미 완전히 판정한 마지막 run까지의 cursor를 SensorResult로 반환한다. 다음 기록은 다음 tick에서 이어서 검사한다. pending metadata 호출이 끝나지 않은 경우에는 기존 cursor를 유지해야 한다. 늦게 끝난 thread에서 context를 변경하지 않는 현재 경계는 유지한다. 단순 고정 page 크기 축소만으로 임의 latency의 누적 timeout을 보장할 수는 없다. 각 호출이 정상 완료하지만 전체 100건이 10초를 넘는 회귀 시험을 추가한다.
- 상태: OPEN. P2 수정 권고이며 수정 또는 owner·task·gate·기한을 갖춘 정식 DEFERRED disposition이 필요하다.

## 추가 공격과 결과

| 시나리오 | 근거·판정 |
| --- | --- |
| native/fallback 총 budget | 후보는 native retry_number와 common infra attempt를 합산하고 fresh child의 native max_retries에 잔여 예산을 넣는다. malformed/상한 도달·native 위임 테스트 두 버전 PASS. native daemon 전환의 전체 실제 launcher 실행은 NOT_RUN. |
| job/project/location/repository origin | origin repository/job를 함께 검사하고 origin 없는 실행에는 project/location 태그를 요구한다. foreign origin·scope 테스트 두 버전 PASS. 소비자 custom repository 이름은 새 keyword로 주입 가능하다. |
| provider/부분 실행 | 실제 저장 실패 reason 필터·step 실패·op 선택 제외 테스트 PASS. partition은 factory에서 거절한다. asset/check 부분 선택도 guard가 있다. provider 실제 호출은 NOT_RUN. |
| 초기 과거 실패 | 센서를 만들기 전에 저장된 START_TIMEOUT 실패가 최초 tick의 재시도 대상임을 별도 실제 instance probe로 확인했다. 기존 실패 센서처럼 시작 시 역사 이벤트를 모두 건너뛰지 않는다. 배포 시 프로젝트 태그가 붙은 과거 실패도 대상이 된다는 운영 영향이 있다. |
| retention으로 cursor run 삭제 | 실제 저장 run ID를 삭제하고 그 ID를 cursor로 전달했다. head로 복귀하여 살아 있는 기존 실패의 동일 run key를 반환하는 별도 probe PASS. 삭제된 cursor 때문에 순회가 영구 멈추지 않는다. |
| 중복 선택·run key | 같은 실패를 다시 선택해도 같은 key다. 그 key와 실제 daemon sensor_name 태그를 갖는 SUCCESS child를 저장하고 Dagster의 실제 `fetch_existing_runs`에 요청을 전달했다. 기존 child를 반환하여 dedupe 조회 경로 PASS. 전체 daemon submit은 실행하지 않았다. |
| 한 tick 발급량·head 순환 | 49 테스트에 actual evaluate_tick의 한 요청 및 끝페이지→head→새 실패 재조회 경로가 포함되어 두 버전 PASS. |
| 메모리·deadline | timeout된 호출은 실제 종료까지 slot을 유지하며 4개 상한이 유지된다. 후보 deadline module은 b324와 동일하다. 이번 테스트의 짧은 deadline 회복도 PASS. 전체 운영 RSS는 NOT_RUN. |

이미 성공한 child가 있는 부모 실패도 scan에서 같은 RunRequest를 다시 선택할 수 있으며 daemon key 조회가 중복 실행을 막는다. 이런 부모가 많으면 한 요청씩 cursor를 진행하는 순회가 느려진다. 가이드는 과거 실패가 많을 때 한 순회 지연을 명시한다. 이번 실행에서는 재선택 자체를 중복 실행으로 오판하지 않았다. 실패 기록 보존량과 최초 활성화의 역사 재시도 영향은 소비자 배포에서 확인해야 한다.

## CI 및 미실행 범위

`gh pr view 25 --repo digitie/kor-travel-common --json headRefOid,url`에서 검토 SHA를 직접 확인했다. `gh pr checks ... --json name,state,link`에서 docs, tools Windows/Linux, secret-scan, check-versions, packages, recovery Python 3.11/3.13의 8개 SUCCESS를 확인했다. [주 CI](https://github.com/digitie/kor-travel-common/actions/runs/37182998435)와 [Python CI](https://github.com/digitie/kor-travel-common/actions/runs/37182998326)를 고정 후보 근거로 사용했다.

- `NOT_RUN`: 운영 shared daemon/RPC의 전체 submit, native 전환·worker kill·hard hang·OS 종료·provider 호출·운영 RSS.
- `NOT_RUN`: transport 후보·backend CI·운영/배포 UI live E2E. 이번 리뷰는 common만 대상으로 한다.
- `NOT_RUN`: 이번 실행의 UI tarball·build·브라우저 재실행. UI runtime은 본인 이전 검토 후보와 동일하며 후보 packages CI 성공과 실제 소비자 검증은 구별한다.
- 기존 review의 Dagster 1.9 event probe 미확정은 이번 후보의 49 테스트 PASS로 대체되는 새 근거다. 이전 원본은 고치지 않았다.
- 상대 원본을 사용하지 않았다. 수정 후 후보는 별도의 원본 재검토로 기록한다.

## 판정

**CONDITIONAL** — 기존 A-P1-01·A-P2-02·A-P2-03는 FIXED이고 고정 후보 테스트 49개가 Dagster 1.13.24 및 1.9.0에서 각각 통과했다. 새 A-P2-04의 수정 또는 규정에 맞는 disposition이 남아 있다. CI 성공만으로 지연 응답 시 순회 진행의 결함을 닫지 않는다.
