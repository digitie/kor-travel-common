<!-- SPDX-License-Identifier: GPL-3.0-only -->

# Common 완료 phase 체크포인트 — 독립 적대 리뷰 원본

- 실행 ID: COMMON-PHASE-A-20261005-3194a0b.
- 리뷰어: James (/root/review_ui).
- 시각: 2026-10-04 22:29:12~22:31:45 UTC / 2026-10-05 07:29:12~07:31:45 KST.
- 저장소: F:/dev/kor-travel-common-geo-dashboard.
- base: f801f01b2dc34b642a64bbf847fa268ac172e4ed.
- 실제 고정 candidate: 3194a0b6c81d64a75dc937f177588a300944b2af (Git rev-parse 확인).
- 범위: factory·child 테스트·guide의 완료 phase/failure_storage_id delta. UI426 제품은 변경 없음.
- 판정: **BLOCK**, 신규 C-PHASE-P1-01.

## 격리·검증 방법

고정 Git show/diff/archive만 읽었다. 상대 보고서·통합 판정은 참조하지 않았다. source/mirror/dependencies/install/외부 DB·컨테이너는 변경하지 않았다. /tmp/james-common-phase-3194a0b의 자체 snapshot에서 기존 Geo venv Python3.12.13/Dagster1.13.24를 PYTHONPATH로 재사용했다. 공격은 본인 local_temp SQLite instance에만 적용했다.

## EXECUTED

- 고정 tests/test_child_crash.py + tests/test_recovery.py: **65 PASS, 43.72초**. RUN_FAILURE3.1초 + STEP_FAILURE5.1초의 실제 유한 지연에서 partial→completed→요청1 회귀를 직접 실행했다.
- 자체 실제 Dagster event/storage 공격: 완료 checkpoint 이후 동일 run에 provider STEP_FAILURE를 실제 report_dagster_event로 추가하고 다음 tick을 실행했다. STEP record를 모의하거나 failure ID를 위조하지 않았다. 결과는 신규 P1 아래와 같다.
- 최신 RUN_FAILURE 이벤트를 실제 추가해 ID가 변경되면 이전 완료 checkpoint를 폐기하고 provider 오류를 다시 검사하여 요청0인 대조군을 확인했다.
- 별도 경계 공격: 기존 3필드 checkpoint 읽기/안전한 재검사 후 요청1, native ON pending 없음에서 요청0, attempt 예산 소진에서 요청0 PASS. bool을 int처럼 사용하거나 잘못된 phase/storage ID를 주는 checkpoint 8개는 ValueError로 거부했다.

기존 C-CHILD-P1-01(P1)은 f801의 실제 여러 유한 페이지 진행 개선으로 **CLOSED 유지**한다. 신규 결함은 완료 검사 재사용의 안전성 회귀이며 기존 원문은 변경하지 않았다.

## C-PHASE-P1-01 — RUN_FAILURE ID가 같은 늦은 provider 기록을 완료 검사에서 건너뜀 (P1)

- 위치: packages/py/kor-travel-common/src/kortravelcommon/dagster.py:251-255; 완료 값 생성:325-330.
- 원인: 완료 phase를 같은 RUN_FAILURE storage ID로만 검증하고 STEP_FAILURE 조회를 전부 건너뛴다. 종료 이벤트 ID는 이후 step 오류 기록의 추가를 막거나 event log 전체가 불변임을 증명하지 않는다.
- 실패 시나리오: 자식 FRAMEWORK_ERROR/ChildProcessCrashException 기록을 검증한 뒤 인계 예산이 부족하여 complete=true checkpoint를 반환한다. 인계 전 다음 tick까지 같은 run의 provider USER_CODE_ERROR/ValueError STEP_FAILURE가 늦게 저장된다. 새로운 RUN_FAILURE가 없으므로 종료 이벤트 ID는 그대로다.
- 실제 재현: 자체 SQLite run에 실제 유효 STEP_FAILURE와 RUN_EXCEPTION/DagsterSubprocessError를 기록하고 elapsed9 경계만 clock 모의하여 complete checkpoint를 받았다. 처음에는 요청0·태그 쓰기0이었다. 다음으로 실제 provider STEP_FAILURE를 append한 뒤 실제 evaluate_tick을 실행했다.
  - RUN_FAILURE storage ID: 계속3.
  - 완료 checkpoint: [run,실제 STEP cursor,1,true,3].
  - 완료 checkpoint resume: **RunRequest1, native 억제/pending 태그 쓰기1**.
  - 같은 실제 이력을 cursor 없이 검사한 대조군: **RunRequest0**.
  - 새 RUN_FAILURE를 append해 ID를 바꾼 대조군: **RunRequest0**.
- 영향: 이전 안전 정책과 cold scan이 자동 재시도에서 제외하는 provider 실패를 completed resume만 승인한다. provider 호출을 자동 반복하지 않는 공용 계약이 깨진다. delayed logger/backfill 등으로 terminal event 후 step 기록이 추가되는 경계를 보호하지 못한다. 실제 production 장애 발생 빈도나 전체 시스템 전파를 관측했다는 주장은 하지 않는다.
- 최소 수정: 완료 phase의 재사용을 RUN_FAILURE ID뿐 아니라 검증한 STEP/event-log tail의 불변성에 묶거나, 완료 cursor 이후의 새 오류를 안전하게 검사해야 한다. 새로운 provider/user/unknown record는 요청과 억제 태그 쓰기 전에 거부해야 한다. 이때 3.1+5.1초 liveness를 다시 영구 반복으로 되돌리지 않는 회귀가 필요하다.
- 폐쇄 조건: 본인의 실제 SQLite late-provider 재현에서 completed resume도 요청0·태그 쓰기0이며, 부모의 느린 partial→completed→요청1 회귀가 함께 통과해야 한다.

재현 파일:
- /tmp/james-common-phase-3194a0b/late_provider_probe.py
  SHA256 2ccbf710f40dd3ddd1d20b43a8efe314bb4da61ad58b3e025f1c1f556cf3cb88.
- /tmp/james-common-phase-3194a0b/phase_boundary_probe.py
  SHA256 58b6458b337cd80bf21089f6c36204f016f5e6fcec6df6f73866177032155d2a.

```bash
cd /tmp/james-common-phase-3194a0b
PYTHONPATH=/tmp/james-common-phase-3194a0b/packages/py/kor-travel-common/src TMPDIR=/tmp TMP=/tmp TEMP=/tmp /home/digitie/dev/kor-travel-geo-codex-dagster-common-test/.venv/bin/python late_provider_probe.py
PYTHONPATH=/tmp/james-common-phase-3194a0b/packages/py/kor-travel-common/src TMPDIR=/tmp TMP=/tmp TEMP=/tmp /home/digitie/dev/kor-travel-geo-codex-dagster-common-test/.venv/bin/python phase_boundary_probe.py

cd packages/py/kor-travel-common
PYTHONPATH=/tmp/james-common-phase-3194a0b/packages/py/kor-travel-common/src TMPDIR=/tmp TMP=/tmp TEMP=/tmp /home/digitie/dev/kor-travel-geo-codex-dagster-common-test/.venv/bin/python -m pytest -q tests/test_child_crash.py tests/test_recovery.py
```

## NOT_RUN·불확실성

실제 PG/외부 provider/production daemon, Dagster1.9, native daemon 동시 전환, UI/live/CI는 직접 수행하지 않았다. 부모65PASS는 대체 근거로 사용하지 않았고 본인도 위65건을 실행했다. 단일 storage 호출 자체가10초를 넘으면 기존 deadline이 스레드를 강제 중단하지 못하는 한계는 그대로다. 새로운 실제 event append 공격은 저장소 API가 허용하는 안전 경계 검증이며 자연스러운 운영 이벤트의 발생 빈도를 입증하는 부하 테스트는 아니다.

## 최종 판정

**BLOCK**. 유한 지연 liveness와 기존 checkpoint 호환성/타입 검증은 통과했으나, 완료 검사 캐시가 뒤늦은 provider 실패를 재시도로 승인하는 C-PHASE-P1-01이 남는다.
