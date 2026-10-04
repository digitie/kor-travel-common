<!-- SPDX-License-Identifier: GPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie) -->

# Common Python fallback 독립 적대 리뷰 — James 원본

- 실행 ID: `james-common-python-b324-20261004T061629Z`
- 시작: 2026-10-04 06:16:29 UTC / 15:16:29 KST
- 종료: 2026-10-04 06:27:25 UTC / 15:27:25 KST
- 전문 범위: 소비자 계약·UI/API/CSS·접근성 및 Python 실패 이벤트, 재시도 예약, deadline 경계.
- 전달받은 기준선: common `090f98429453d8882150eb9e56ccae98e0e353a2`.
- 실제 검토 후보: common `b324b0afdc27f268e6e6aaee1f6d7d2f42e4743b`.
- 저장소: `F:/dev/kor-travel-common-recovery`.
- 대상 PR: [common #25](https://github.com/digitie/kor-travel-common/pull/25).
- 격리: Windows Git의 고정 `show`·`diff`로만 소스를 읽었다. 모든 delta 조회에서 `:(exclude)docs/reviews/**`를 적용했다. 상대 리뷰 원문과 결과는 읽지 않았다. 구현 소스·venv·설치를 수정하지 않았다. 이 원본 evidence 파일만 작성한다.

## 범위와 근거

기준선 대비 변경 파일 목록과 Python `dagster.py`, `deadline.py`, `test_recovery.py`, adoption 가이드, CHANGELOG, UI 모델·컴포넌트·CSS·패키지 변경을 검토했다. 앞선 UI 후보에서 검토했던 cron 범위 검증, terminal 경과 시간, 키보드 표 영역·focus 계약은 유지된다. 앱별 인증·GraphQL·URL은 소비자가 소유한다. 이번 검토는 common만 대상으로 하며 transport 후보와 운영 배포를 승인하지 않는다.

Dagster 1.13.24/Python 3.13의 기존 `/tmp/transport-recovery-venv`에서 고정 Git 객체의 두 Python 모듈을 JSON stdin으로 전달하여 별도 모듈로 실행했다. 소스 import에 움직이는 worktree 파일을 사용하지 않았다. `DagsterInstance.local_temp()`의 별도 임시 저장소에 실제 run과 실패 이벤트를 기록하고 `SensorDefinition.evaluate_tick()`을 실행했다. 임시 저장소는 종료 시 제거되었다. 외부 DB·운영 job·provider 호출은 없다.

## Findings

### A-P1-01 — metadata 장애 뒤 실패 이벤트를 영구 소비하여 복구 후 재시도가 유실됨

- 위치: `packages/py/kor-travel-common/src/kortravelcommon/dagster.py:143–179,208–216`; 직접 호출만 검증하는 `packages/py/kor-travel-common/tests/test_recovery.py:test_retry_storage_failure_is_not_interpreted_as_an_empty_queue`.
- 근거: `retry_tick` 내부 metadata 예외는 `run_failure_sensor`의 Dagster 래퍼가 `DagsterRunReaction.error`로 변환한다. 래퍼는 해당 실패 이벤트 뒤로 cursor를 진행시킨다. 설치된 Dagster 1.13.24의 `_core/definitions/run_status_sensor_definition.py`에서 이 경로를 확인했고, `_daemon/sensor.py:995–1015`는 실패 reaction 처리에도 `set_should_update_cursor_on_failure(True)`를 호출한다. 따라서 실패 tick을 표시하는 것과 동일 이벤트를 다시 평가하는 것은 다르다.
- 재현: 센서를 빈 저장소에서 초기화하고 `UNEXPECTED_TERMINATION` 실패 이벤트를 저장한다. 초기 cursor로 정상 `evaluate_tick()`을 호출하면 RunRequest가 1개 나온다. 같은 cursor에서 `instance.get_runs`에 일시적 `ConnectionError`를 주입하면 RunRequest 0개·error reaction 1개·cursor 전진이 나온다. 오류를 제거한 뒤 그 새 cursor로 평가하면 RunRequest 0개이며 `Sensor function returned an empty result`가 된다.
- 실제 출력: `healthy_requests 1`; `failed_requests 0 reactions 1 error ConnectionError: transient metadata outage cursor_advanced True`; `after_restore_requests 0`.
- 영향: 정상적인 일시 DB 장애, deadline 초과 또는 4개 용량 소진 시 멱등 job의 허용된 인프라 재시도가 영구 유실된다. 정기 schedule이 없는 job은 다음 작업을 자동으로 시작할 근거가 사라진다. 수동 cursor 되돌리기가 필요해 사용자 요청의 자동 복구 목표를 깨뜨린다.
- 최소 수정 권고: 일시 오류가 이벤트 소비로 커밋되지 않게 cursor를 직접 소유하는 일반 sensor 또는 동등한 durable 처리 경로를 사용한다. metadata 검사와 요청 준비가 성공한 뒤에만 cursor를 진행시키고, 결정적 run key로 재평가 중복을 막는다. 실제 저장 이벤트·`evaluate_tick`·daemon의 실패 cursor 정책을 포함해 장애 후 동일 이벤트가 다시 평가되는 회귀 검증이 필요하다. 예외를 단순히 `SkipReason`으로 바꾸면 여전히 이벤트가 소비되므로 해결되지 않는다.
- 상태: OPEN. P1이므로 merge BLOCK.

### A-P2-02 — 이벤트 조회가 deadline 밖에서 실행되어 10초/4개 계약이 전체 센서를 보호하지 않음

- 위치: `packages/py/kor-travel-common/src/kortravelcommon/dagster.py:208–216`; `docs/runbooks/dagster-adoption.md:197–198`.
- 근거: `run_failure_sensor`는 소비자 callback을 호출하기 전에 `fetch_run_status_changes`와 `get_run_records`를 동기로 실행한다. `call_with_deadline`은 그 뒤 `retry_failed_run`에만 적용된다. 가이드는 조회 전체에 10초/동시 4개 상한이 있는 것으로 표현한다.
- 재현: 저장된 실패 이벤트가 있는 isolated instance의 `fetch_run_status_changes`를 Event에 대기하도록 주입한다. 별도 평가 thread는 그 조회에 진입하여 정지했고, 그 시점 `call_with_deadline` spy의 호출 횟수는 0이었다. Event를 풀어 평가를 마무리했다. 코드상 대기 Event를 풀지 않으면 해당 조회를 제한하는 common timer나 slot은 없다. 실제 10초 hard hang을 기다리는 테스트는 실행하지 않았다.
- 영향: 초기 cursor 생성 또는 이후 이벤트 조회가 DB/네트워크에서 멈추면 callback의 유한 대기와 메모리 상한을 우회한다. 반복 RPC 호출에 대한 code-server 작업 회수·상한은 외부 Dagster 설정에 맡겨진 상태다.
- 최소 수정 권고: 이벤트·run 조회와 검사를 포함한 전체 공통 평가를 bounded call로 감싼다. 작업 thread에서 context cursor를 변경하지 않고 결과를 반환한 뒤, 완료된 주 평가에서 cursor를 갱신한다. timeout 뒤 뒤늦게 완료되는 thread가 상태를 게시하지 않도록 한다. 전체 조회 상한을 검증하거나 가이드를 실제 보호 범위로 제한해야 한다.
- 상태: OPEN. 실질적인 대기·검증 경계 결함이며 수정 권고.

### A-P2-03 — 새 실행에 이전 native retry bookkeeping 태그가 오염됨

- 위치: `packages/py/kor-travel-common/src/kortravelcommon/dagster.py:180–205`.
- 근거: 6개 identity 태그만 제거하므로 `dagster/auto_retry_run_id`, `dagster/will_retry`, `dagster/is_resume_retry`, `dagster/is_asset_resume_retry`, `dagster/failure_reason` 등의 이전 실행 상태가 남는다. 새 전체 job 실행이라는 계약과 맞지 않는다.
- 재현: 실제 실패 run에 과거 성공 run의 `dagster/auto_retry_run_id`와 `dagster/is_resume_retry=true`를 붙이고 허용된 `START_TIMEOUT` 이벤트를 기록한다. `evaluate_tick`이 만든 RunRequest의 태그로 새 run을 만들면 `child.is_resume_retry=True`다. Dagster의 `get_automatically_retried_run_if_exists(instance, child, [child])`는 새 child와 무관한 과거 성공 run을 반환한다.
- 영향: native retry로 전환한 뒤 신규 child가 실패하면 daemon이 이전 unrelated retry를 이미 생성된 child로 오판하여 재예약을 생략할 수 있다. native 기능이 꺼져 있어도 실행 상태·resume 표시가 잘못된다. 실제 운영 native 전환·launcher 실행은 미실행이며 위 반환 경로는 isolated instance에서 재현했다.
- 최소 수정 권고: 새 실행을 만드는 경우 과거 실행의 retry·failure bookkeeping과 resume 태그를 제거한다. backfill·selection 태그도 이 factory의 전체 non-partition job 계약과 맞는지 명시적으로 정리한다. 소비자 custom 태그·run config와 현재 policy 태그는 보존한다. native 상태 태그가 섞인 원본에서 만든 fresh RunRequest를 회귀 검증한다.
- 상태: OPEN. 일반 사용자의 깨끗한 최초 run에는 영향이 없으나 재시도 상태 이관의 실질적 결함이다.

P0는 확인하지 않았다. P3 추가 finding은 없다.

## 공격 시나리오와 검증 상태

| 검증 | 실제 결과/한계 |
| --- | --- |
| PR 후보 SHA·CI | `gh pr view 25 --repo digitie/kor-travel-common --json headRefOid,url`에서 b324 확인. `gh pr checks ... --json name,state,link`에서 docs, tools Windows/Linux, recovery Python 3.11/3.13, secret-scan, check-versions, packages 모두 SUCCESS(8개)를 직접 확인. [주 CI](https://github.com/digitie/kor-travel-common/actions/runs/37182091009), [Python CI](https://github.com/digitie/kor-travel-common/actions/runs/37182091048). |
| 허용 이유·missing reason·provider·native 위임·scope·budget | 후보의 40개 테스트와 guard를 읽었다. 명시적인 3개 reason만 허용하며 불명확한 원인, 다른 project/location, ASCII가 아닌 budget, step/provider 실패를 fail-closed한다. 상대 리뷰 결과를 근거로 사용하지 않았다. |
| 실제 저장 실패 이벤트·센서 평가 | 1.13.24에서 config 보존 RunRequest 1개, metadata 예외 뒤 cursor 전진·복구 후 이벤트 유실을 재현. 직접 callback 테스트와 구별했다. |
| 실제 STEP_FAILURE 기록 | 실제 event storage에 STEP_FAILURE를 기록한 뒤 START_TIMEOUT 실패를 저장. `evaluate_tick`의 요청 0개·step 실패 SkipReason을 확인. mock records만 사용한 검증과 구별했다. |
| native metadata 오염 | 실제 저장 run·새 child로 이전 auto-retry run 참조 및 resume flag 오염 재현. |
| deadline 용량 | 고정 모듈로 4개 callback을 timeout 후 계속 대기시킨다. 5번째는 호출하지 않고 DeadlineExceeded. 기존 4개 실제 종료 후 새 callback이 42 반환하여 slot 회복 PASS. |
| 전체 이벤트 조회 deadline | callback 이전 fetch에 정지시키고 bounded helper 호출 0회를 확인. 전체 wrapper 경계 결함은 위 A-P2-02. |
| 최소 Dagster 1.9 | 고정 모듈 import·factory 생성은 성공. 추가 native helper는 1.9에 없어 첫 probe는 ImportError. 별도 stored-event probe는 예상 요청 1개가 나오지 않아 assertion 실패했으며 floor 이벤트 평가 통과로 집계하지 않는다. 초기 -1 cursor·local event-index 경계는 이번 실행에서 원인 확정하지 못했다. 운영 소비자 버전은 1.13.24이고 설치/venv를 바꾸지 않았다. |
| 공개 UI/API/CSS·tarball | 원래 base 대비 UI delta를 다시 읽었고 Python 추가 이전 후보와 runtime UI가 동일함을 확인. 앞선 독립 UI 검토의 42 테스트·pack 근거와 이번 후보 packages CI 성공은 구별한다. 이번 실행에서 UI 단위/pack/build를 별도 재실행하지 않았다. |

## 남은 불확실성과 NOT_RUN

- `NOT_RUN`: 실제 shared daemon/launcher worker kill·장기 hang·OS 프로세스 종료·native 전환·운영 RSS·운영 UI live E2E. 운영 설정과 소비자 배포는 부모 및 해당 소비자 gate 소유다.
- `NOT_RUN`: daemon이 실제 run을 submit하는 전체 process integration. event storage/`evaluate_tick` 경로는 실제 실행했으나 RPC daemon submit 경로는 실행하지 않았다. P1의 cursor persistence는 설치된 daemon 구현을 직접 읽어 확인했다.
- 1.13.24 monitoring의 `monitor_started_run`은 healthcheck 실패를 `report_run_failed(run, msg)`로 기록하며 explicit failure reason을 전달하지 않는 경로가 있다. 이 factory는 이를 원인 불명으로 제외한다. 안전한 fail-closed 정책과 일치하지만 hard-kill의 모든 형태를 복구한다는 근거는 되지 않는다. 배포 후 실제 launcher 종료 이벤트의 reason을 확인해야 한다. 원인 누락을 무조건 인프라 오류로 추정하는 변경은 권고하지 않는다.
- callback의 deterministic run key가 같은 sensor 이벤트 재평가를 안정화하더라도 별도 sensor 이름/수동 발화와의 원자적 queue 보장을 대신하지 않는다. 가이드의 job concurrency·소비자 DB lease 요구를 유지해야 한다. 이번 실행에서는 실제 daemon run-key dedupe와 동시 launcher를 실행하지 않았다.
- 이 보고서는 b324 후보만의 원본이다. 이후 수정, 상대 결과, live 검증 또는 CI 결과를 이 파일에 덧붙이지 않는다. 수정 후보는 별도 post-fix 보고서로 재검토해야 한다.

## 판정

**BLOCK** — A-P1-01은 일시 metadata 장애 후 복구해야 하는 정상 경로에서 재시도 이벤트를 영구 유실한다. A-P2-02·A-P2-03도 수정 또는 정식 disposition이 필요하다. CI 8개 성공은 확인했지만 이 이벤트/cursor 경계가 단위 테스트 범위 밖이므로 merge 승인으로 대체할 수 없다.
