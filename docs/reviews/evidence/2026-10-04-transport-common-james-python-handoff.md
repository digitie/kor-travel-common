<!-- SPDX-License-Identifier: GPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie) -->

# Common durable retry 인계 독립 최종 재리뷰 — James 원본

- 실행 ID: `james-common-python-handoff-430a9-20261004T071405Z`
- 시작: 2026-10-04 07:14:05 UTC / 16:14:05 KST
- 종료: 2026-10-04 07:21:55 UTC / 16:21:55 KST
- 전문 범위: 소비자 공개 계약·UI/API/CSS와 Python 이벤트/cursor·deadline·native/fallback 예산·인계 복원.
- 원래 기준선: `090f98429453d8882150eb9e56ccae98e0e353a2`.
- 직전 본인 후보: `f0d27b4cca2aae9c2f58e2ed12bbf5495d12fcc0`.
- 실제 검토 후보: `430a9e9cd5429204579792b1d4f8e399366dcb2f`.
- 저장소: `F:/dev/kor-travel-common-recovery`.
- 격리: Windows Git 고정 객체의 show/diff만 사용했다. 전체 변경 목록에서 `:(exclude)docs/reviews/**`를 적용했고 상세 diff는 구현·가이드의 명시적 경로만 조회했다. 상대 원본·결과를 읽지 않았고 기존 본인 원본을 수정하지 않았다. 구현·venv·설치를 변경하지 않고 이 새 evidence 원본만 작성한다.

## 범위와 검증 환경

원래 기준선 대비 전체 공용 변경 목록, 직전 후보 대비 `dagster.py`·테스트·adoption 가이드의 전체 delta를 읽었다. source는 고정 Git 객체에서 읽어 JSON stdin으로 기존 WSL Python에 전달했다. 임시 모듈과 임시 테스트 파일을 사용하여 움직이는 worktree source를 import하지 않았다.

- Python 3.13 / Dagster 1.13.24, `/tmp/transport-recovery-venv`: **56 passed in 8.77s**.
- Python 3.11 / Dagster 1.9.0, `/tmp/common-dagster-floor`: **56 passed in 9.53s**.
- 같은 56개 고유 테스트를 두 버전에서 각각 실행했다. skip·0 test를 통과로 합산하지 않았다.
- 추가 인계 probe는 별도 `DagsterInstance.local_temp()`의 실제 run/event 저장소와 `SensorDefinition.evaluate_tick`을 사용했다. SQL commit 응답 오류 및 native 설정 값은 시험에서 주입했으며 운영 DB/config 변경이라고 주장하지 않는다.

UI runtime/CSS·deadline 모듈은 직전 후보와 동일하다(`git diff --quiet` exit 0). 앞선 본인의 cron 범위·terminal elapsed·접근성/CSS 검토 결과가 유지된다. 앱 인증·GraphQL·URL·SQL·instance 운영을 common이 소유하지 않는 공개 계약도 유지된다. 새 pending 태그 상수와 repository keyword는 additive API이며 앱 도메인/provider 의존성을 추가하지 않았다.

## 본인 finding disposition

| ID | 검증 근거 | 최종 상태 |
| --- | --- | --- |
| A-P1-01 | 일반 sensor의 metadata 예외/timeout은 cursor를 소비하지 않는다. 실제 저장 실패와 evaluate_tick의 오류→복구 재평가 회귀를 두 버전에서 실행했다. | FIXED |
| A-P2-02 | 목록·cursor·event·step·scope·active·child 검사와 인계 metadata 쓰기까지 bounded callback 안에 있다. 늦은 worker가 context cursor를 직접 변경하지 않는다. | FIXED |
| A-P2-03 | native bookkeeping을 제거한 fresh child가 resume가 아니며 custom 태그는 보존된다. pending 표식도 child에서 제거한다. | FIXED |
| A-P2-04 | 5초 inner checkpoint·10초 hard deadline·완료 행 뒤 이어가기 회귀가 두 버전에서 통과했다. 직전 본인 실제 100 × 0.12초 순회 probe의 구현이 변경되지 않았으며 42→84→100건/head 결과가 유지되는 코드 경계다. | FIXED |
| A-P2-05 | `dagster.py:153–158,215–234,239–262,269–312`가 native 억제와 pending=true를 함께 쓰고, native ON에서도 pending 인계를 계속 처리한다. 실제 ACK 유실→native ON→동일 key 복원→SUCCESS child→pending=false를 추가 probe로 확인했다. | FIXED |

### A-P2-05의 독립 추가 재현

1. 정책 예산 3인 sample job에 실제 START_TIMEOUT 실패 이벤트를 저장한다.
2. `add_run_tags` wrapper가 원래 메서드로 commit한 뒤 ConnectionError를 던진다. evaluate_tick은 실패하고 context cursor는 None이다.
3. 저장된 parent는 native max_retries=0, will_retry=false, infra_retry_pending=true다. child는 아직 없다.
4. 새 nonpending 실패를 하나 더 만든 뒤 native ON을 주입한다. production에서 저장됐을 수 있는 이전 parent cursor로 평가하면 빈 끝페이지를 거쳐 head로 복귀한다. 다음 head 평가에서 pending parent의 같은 `test/infra/{parent_id}/1` key 요청이 복원된다. 새 nonpending 실패는 요청하지 않는다.
5. child의 native 잔여 예산은 2, pending 태그는 없다. 실제 native `should_retry(parent, instance)`는 False다.
6. 요청 태그로 SUCCESS child를 저장한 뒤 head로 재평가하면 요청 없이 parent pending=false가 된다. 이후 native ON 평가도 요청하지 않는다.
7. native OFF로 다시 바꾸면 아직 처리하지 않은 신규 실패만 fallback으로 요청되고, 완료된 원래 parent는 다시 발급하지 않는다.

실제 출력: `A-P2-05 FIXED: ACKlost -> pending persisted -> native ON old cursor head -> same key restored -> SUCCESS child -> pending false`; `native fresh nonpending failure delegated; child pending absent; parent native disabled; child native remaining budget2 PASS`; `native ON -> OFF filter broadens safely; completed original parent not reissued PASS`.

설치된 Dagster 1.13.24의 SQLRunStorage.add_run_tags 및 SQLite connect 구현도 읽었다. 이 backend는 run body와 tag index를 transaction 안에서 갱신한다. 이번 실제 commit→응답 유실 probe는 해당 저장소에서 수행했다. 임의 custom storage plugin의 원자성이나 운영 PostgreSQL 장애를 검증했다고 확장하지 않는다.

## 추가 공격 시나리오

| 공격 대상 | 확인 내용 |
| --- | --- |
| cursor/filter 전환 | native ON은 project와 pending=true를 함께 조회한다. 이전 all-failure cursor에서 끝/head로 순환한 뒤 pending을 복원했다. native OFF로 범위를 넓힌 뒤 완료 부모의 재발급이 없음을 확인했다. filter 변경은 즉시 모든 과거 실패를 요청하지 않는다. |
| child 상속/중복 예산 | pending은 job 태그 재적용 뒤 명시적으로 제거한다. native/fallback 횟수를 합산하고 child에 잔여 예산만 남긴다. 기존 SUCCESS native/fallback child 조회·budget exhausted 회귀를 두 버전에서 실행했다. |
| scope 오염 | project/location/repository/job origin을 함께 제한하고 malformed attempt를 fail-closed한다. parent UUID 기반 child 조회 및 다른 위치의 동명 job 방어를 검토했다. 새 pending 예외가 source scope 검사를 우회하지 않는다. |
| 선택 확대 | op/asset/check 선택, resolved graph subset, execution plan step subset을 제외하는 테스트가 두 버전에서 통과했다. |
| provider·원인 누락 | explicit 세 가지 인프라 reason만 허용한다. step 실패와 UNKNOWN/누락은 요청하지 않는다. native ON의 일반 실패는 native가 소유하며 pending 인계만 common이 마무리한다. |
| 오류/장애 thread | metadata 예외는 tick 실패로 전달하고 cursor를 진행시키지 않는다. 살아 있는 timeout callback은 실제 종료까지 4개 slot 상한을 유지한다. 강제 thread 종료를 보장하는 것으로 표현하지 않는다. |
| 역사 실패·retention | fresh sensor가 scoped 미재시도 역사 실패도 순회한다는 가이드가 유지된다. 삭제된 cursor의 head 복귀와 완료 child의 반복 선택 방어가 유지된다. 오래된 실패가 많을 때 순회 지연이 있을 수 있다는 설명도 있다. |

이번 후보에서 추가 조치가 필요한 P0/P1/P2/P3 finding은 확인하지 않았다. 취향 차이나 실행하지 않은 운영 계약을 발견된 코드 결함으로 집계하지 않았다.

## CI와 남은 불확실성

`gh pr view 25 --repo digitie/kor-travel-common --json headRefOid,url`로 검토 SHA를 직접 확인했다. `gh pr checks ... --json name,state,link`에서 docs, tools Windows/Linux, secret-scan, check-versions, packages, recovery Python 3.11/3.13의 8개 SUCCESS를 직접 확인했다. [주 CI](https://github.com/digitie/kor-travel-common/actions/runs/37184964291)와 [Python CI](https://github.com/digitie/kor-travel-common/actions/runs/37184964141)가 고정 후보 근거다.

- `NOT_RUN`: shared 운영 daemon/RPC의 실제 submit·NOT_STARTED child 생성 뒤 launcher 제출 사이의 crash/resume·native 설정 변경·worker kill/hard hang·OS 종료·provider 호출·운영 RSS. child 발급 이후의 실제 실행 복구는 Dagster daemon/launcher 영역이며 SUCCESS child로 끝낸 본 probe와 구별한다.
- `NOT_RUN`: 운영 SQL 장애·custom run storage의 tag 원자성·동시에 서로 다른 native 설정을 가진 daemon. 가이드는 설정 전환 시 daemon/code-server drain을 요구한다.
- `NOT_RUN`: transport 후보·backend CI·소비자 live UI E2E. 이번 판정은 common 고정 후보만 대상으로 한다.
- `NOT_RUN`: 이번 실행에서 UI tarball/build/브라우저 재실행. UI runtime이 동일함과 packages CI 성공은 확인했으며 실제 소비자 검증을 대신하지 않는다.
- timeout callback을 실제 중단시키지 않는 제약, 원인 누락을 임의로 인프라 실패로 추정하지 않는 정책, queue concurrency·소비자 DB lease·서비스 관리자의 restart 책임을 유지해야 한다.

## 판정

**PASS** — 본인 A-P1-01·A-P2-02·A-P2-03·A-P2-04·A-P2-05는 모두 FIXED다. 고정 후보 56개 테스트가 Dagster 1.13.24 및 최소 1.9.0에서 각각 통과했고, 실제 metadata commit ACK 유실과 cursor/filter 전환을 포함한 인계 복원을 별도로 확인했다. 새 actionable finding은 없다. 운영·transport 검증은 위 NOT_RUN 범위로 남는다.
