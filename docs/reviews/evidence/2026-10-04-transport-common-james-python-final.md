<!-- SPDX-License-Identifier: GPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie) -->

# Common Python fallback 두 번째 수정 후보 독립 재리뷰 — James 원본

- 실행 ID: `james-common-python-final-f0d27-20261004T065552Z`
- 시작: 2026-10-04 06:55:52 UTC / 15:55:52 KST
- 종료: 2026-10-04 07:02:39 UTC / 16:02:39 KST
- 전문 범위: 소비자 공개 계약·UI/API/CSS와 Python 이벤트 복구·cursor·deadline·native/fallback 전환.
- 원래 기준선: `090f98429453d8882150eb9e56ccae98e0e353a2`.
- 직전 본인 후보: `7ee00152c2f7b3877ff3bedcd61a58ec15122d89`.
- 실제 검토 후보: `f0d27b4cca2aae9c2f58e2ed12bbf5495d12fcc0`.
- 저장소: `F:/dev/kor-travel-common-recovery`.
- 격리: Windows Git 고정 객체의 show/diff로만 구현을 읽었다. 전체 delta 목록에는 `:(exclude)docs/reviews/**`를 적용했고 상세 diff는 구현·가이드의 명시적 경로만 사용했다. 상대 원문·결과를 읽지 않았다. 기존 본인 원본, 구현 소스, venv, 설치를 변경하지 않았고 이 새 원본 evidence만 작성한다.

## 범위와 실행 환경

원래 기준선 대비 전체 delta 목록 및 직전 후보 대비 Python 모듈·테스트·adoption 가이드 전체 변경을 읽었다. UI runtime·CSS·deadline 모듈은 직전 독립 검토 후보와 동일하다(`git diff --quiet` exit 0). 공개 factory의 repository 인자는 additive keyword이고 인증·URL·도메인 SQL·운영 instance는 소비자 소유라는 경계를 유지한다.

고정 후보의 모듈·테스트를 Windows Git에서 읽어 JSON stdin으로 전달한 뒤 임시 모듈·임시 테스트 파일로 실행했다. 움직이는 worktree source를 import하지 않았다. 기존 WSL 환경을 변경하지 않았다.

- `/tmp/transport-recovery-venv`: Python 3.13 / Dagster 1.13.24, **54 passed in 7.42s**.
- `/tmp/common-dagster-floor`: Python 3.11 / Dagster 1.9.0, **54 passed in 8.82s**.
- 각 버전에서 같은 54개 고유 테스트를 실행했다. skip이나 0 test를 통과로 합산하지 않았다.
- 추가 probe는 별도 `DagsterInstance.local_temp()` 저장소와 실제 `SensorDefinition.evaluate_tick`을 사용했다. 아래 latency/commit-response 오류는 주입한 것이며 운영 DB 실측이라고 주장하지 않는다.

## 이전 finding closure

| ID | 수정·재검증 근거 | 상태 |
| --- | --- | --- |
| A-P1-01 | 일반 sensor가 metadata 오류/timeout 때 cursor를 변경하는 SensorResult를 반환하지 않는다. 실제 저장 이벤트·evaluate_tick의 오류 후 같은 실패 재요청 회귀를 두 Dagster 버전에서 실행했다. | FIXED 유지 |
| A-P2-02 | 전체 조회·검사·결과 준비를 10초 bounded call 안에서 실행한다. callback 이전의 실패 센서 이벤트 조회 경로를 제거했다. | FIXED 유지 |
| A-P2-03 | 이전 native bookkeeping 태그를 제거한 뒤 현재 job/policy·scope·잔여 budget을 적용한다. fresh child의 resume 태그가 사라지고 custom 태그가 보존되는 회귀가 두 버전에서 통과했다. | FIXED 유지 |
| A-P2-04 | `dagster.py:257–299`는 5초 inner budget 뒤 마지막 완전히 판정한 행까지 checkpoint한다. 실제 100건 × 0.12초 정상 응답을 주입해 3개 tick으로 모두 진행했다. | FIXED |

A-P2-04의 실제 결과는 `tick 1 elapsed 5.05 checked 42 checkpoint 41`, `tick 2 elapsed 5.05 checked 84 checkpoint 83`, `tick 3 elapsed 1.92 checked 100 checkpoint head`였다. 100개 고유 run을 정확히 한 번씩 확인했고 모든 tick이 실제 10초 hard deadline 안에 끝났다. 기존의 동일 페이지 무한 반복은 재현되지 않았다. inner budget은 행 사이에서 확인하며, 단일 판정이 hard deadline을 넘을 때는 안전하게 cursor를 유지하는 현재 계약을 구별한다.

이전 P0/P1/P2 중 열린 본인 finding은 없다. 추가 P0/P1은 확인하지 않았다.

## 새 finding

### A-P2-05 — parent 예산 저장 응답 유실 뒤 native ON 전환 시 복구 소유권이 사라짐

- 위치: `packages/py/kor-travel-common/src/kortravelcommon/dagster.py:245–254,257–261`; `docs/runbooks/dagster-adoption.md`의 native 설정 전환 drain 조건.
- 근거: fallback 요청을 반환하기 전에 parent의 native 예산을 0·will_retry=false로 닫는다. durable pending handoff 상태는 기록하지 않는다. 이 저장이 commit됐지만 응답이 유실되어 평가가 실패하면 child도 RunRequest도 없는 상태가 남는다. native가 계속 OFF이면 같은 실패를 재평가하여 회복하지만, ON으로 전환하면 factory 전체가 즉시 위임하여 복구를 맡지 않는다. native도 닫힌 parent 예산을 보고 재시도하지 않는다.
- 실제 재현: 실제 START_TIMEOUT 실패 run을 저장했다. `add_run_tags` wrapper가 원래 메서드로 태그를 commit한 뒤 `ConnectionError('commit response lost')`를 던지도록 했다. evaluate_tick 예외 후 cursor는 None, 저장소에는 parent 1개만 있고 parent의 max_retries=0·will_retry=false였다. 해당 실패 평가가 종료된 뒤 native ON을 주입하여 재평가했다. fallback 요청 0개, 실제 Dagster `should_retry(parent, instance)`는 False였다. native OFF를 유지한 대조 경로는 다시 요청 1개를 만들었다.
- 실제 출력: `after committed response error: no child, parent max_retries 0 will_retry false`; `native enabled after failed evaluation finished: fallback_requests 0 native_should_retry False skip native run retry에 위임합니다.`
- 영향: metadata commit 응답 오류 또는 요청 준비/전달 실패와 native OFF→ON 전환이 겹치면, 처리 중 callback이 없어도 미제출 실패가 양쪽 재시도 경로에서 제외된다. 일반적인 native OFF 복구 경로는 정상이며, 이 finding은 설정 전환 경계에 한정된다. 실제 운영 설정을 변경한 테스트는 실행하지 않았다.
- 최소 수정 권고: parent 예산 종료와 함께 durable pending handoff를 기록하고 native ON 후에도 미완료 handoff를 회수하거나, 운영 전환 gate를 구체화한다. 후자를 선택한다면 drain에 더해 **예산이 닫혔지만 child가 없는 parent/미제출 fallback 요청을 검사하고 native OFF 상태에서 복구 완료를 확인하기 전에는 ON으로 전환하지 않는다**는 조건과 재현 검증을 명시한다. 단순히 daemon/code-server를 drain한다는 표현만으로 이미 종료된 실패 평가의 누락을 확인할 수는 없다. native OFF인 동안 같은 run key로 다시 준비할 수 있다는 기존 보장은 유지한다.
- 상태: OPEN. P2이며 runtime 수정 또는 규정에 맞는 owner·task·gate·기한의 DEFERRED/disposition이 필요하다. 문서로 제한한다면 해당 전환 gate가 구체적이고 검증 가능해야 한다.

## 추가 공격과 확인한 계약

| 시나리오 | 결과 |
| --- | --- |
| 부분 graph/plan 확대 | resolved_op_selection subset 및 step execution plan subset을 실제 Dagster run으로 만든 테스트가 두 버전에서 통과했다. op/asset/check 선택도 guard로 제외한다. full graph/plan의 재시도는 유지한다. |
| 이전 native/fallback child | 저장된 SUCCESS native child와 fallback child가 있는 부모에 중복 요청을 발급하지 않는 새 테스트 두 버전 PASS. parent UUID 기반 조회이므로 다른 부모의 정상 child를 동일 재시도로 선택하지 않는다. |
| 태그 scope·예산 | repository/job origin·project/location 및 malformed budget guard를 다시 읽고 두 버전 회귀 실행. native 횟수와 fallback 횟수를 합산하며 child는 잔여 native 예산을 갖는다. parent budget 종료는 요청 반환 전에 저장된다. 이 마지막 side effect의 전환 오류는 A-P2-05로 구별했다. |
| metadata 오류/timeout 후 진행 | context cursor가 유지되고 저장소 복구 후 같은 실패가 요청되는 두 버전 회귀 PASS. inner checkpoint 뒤 다음 tick의 이어가기와 hard deadline은 별도 실제 지연 probe로 검증했다. |
| 첫 활성화·retention | 초기 역사 실패도 scoped retry 대상이라는 가이드가 새로 명시됐다. 삭제된 cursor는 head로 복귀하는 직전 본인 실제 probe 근거와 해당 로직이 유지된다. 기존 child를 확인하므로 완료한 역사 부모의 중복 선택 비용도 줄였다. |
| 동시 실행·memory | 한 tick 한 요청, 실패 scan 100건, 5초 checkpoint, 10초 대기, 살아 있는 callback 최대 4개가 유지된다. queue concurrency와 도메인 DB lease는 소비자 gate이며 실제 launcher race/RSS를 시험했다고 주장하지 않는다. |

## CI와 NOT_RUN

`gh pr view 25 --repo digitie/kor-travel-common --json headRefOid,url`에서 f0d27 후보를 직접 확인했다. `gh pr checks ... --json name,state,link`에서 docs, tools Windows/Linux, secret-scan, check-versions, packages, recovery Python 3.11/3.13의 8개 SUCCESS를 직접 확인했다. [주 CI](https://github.com/digitie/kor-travel-common/actions/runs/37183873302)와 [Python CI](https://github.com/digitie/kor-travel-common/actions/runs/37183873329)가 고정 후보 근거다.

- `NOT_RUN`: 운영 native 설정 변경, shared daemon/RPC 전체 제출·worker kill/hard hang·OS 종료·provider 호출·운영 RSS.
- `NOT_RUN`: transport 후보·backend CI·소비자 live UI E2E. 이번 리뷰는 common만 대상으로 한다.
- `NOT_RUN`: 이번 실행의 UI tarball/build/브라우저 재실행. UI delta는 이전 독립 검토 범위와 동일하고 후보 packages CI는 직접 확인했지만 실제 소비자 검증과 구별한다.
- 상대 원본/결과를 사용하지 않았고 이전 본인 원본도 수정하지 않았다. 이후 후보는 별도 report로 재검토해야 한다.

## 판정

**CONDITIONAL** — A-P1-01·A-P2-02·A-P2-03·A-P2-04는 모두 FIXED이며 고정 후보의 54개 테스트가 Dagster 1.13.24 및 최소 1.9.0에서 각각 통과했다. 설정 전환 경계의 A-P2-05 수정 또는 구체적인 운영 gate/disposition이 남아 있다.
