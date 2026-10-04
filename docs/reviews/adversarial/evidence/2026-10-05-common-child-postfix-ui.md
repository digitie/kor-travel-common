<!-- SPDX-FileCopyrightText: 2026 digitie -->
<!-- SPDX-License-Identifier: GPL-3.0-or-later -->

# Common 자식 프로세스 복구 변경 — 독립 적대 리뷰 원본

- 실행 ID: `COMMON-CHILD-A-20261005-92ebfa60`.
- 관찰: `2026-10-04 21:58:15~22:03:08 UTC` / `2026-10-05 06:58:15~07:03:08 KST`.
- 저장소: `/mnt/f/dev/kor-travel-common-geo-dashboard`.
- 실제 base: `426de4fbad35282bb558712d922c06268e9aba62`.
- 실제 후보: `92ebfa60ef976d830c08b353de633103650175ad`.
- 범위: 고정 Git의 Python factory·신규 테스트 2파일·채택 가이드, 총 4파일. UI와 vendor tarball 변경은 없다.
- 격리: 제품 source·설치·부모 mirror·다른 reviewer 자료·외부 provider·PG는 변경하거나 사용하지 않았다. 고정 archive를 `/tmp/james-common-child-92ebfa60`에 풀고 geo의 기존 Python을 읽어 실행했다. 자체 SQLite와 scratch 공격 파일만 썼다. 실행은 Python3.12.13 / Dagster1.13.24다.

## 판정

**BLOCK — C-CHILD-P1-01을 수정하거나 근거로 기각하고 고정 후보로 재확인해야 한다.**

실제 os._exit(42) 분류와 기존 budget/scope 회귀는 통과했다. 그러나 새 페이지 반복의 liveness는 전체 sensor 대기 상한만으로 보장되지 않는다.

## C-CHILD-P1-01 / P1 — 느린 정상 이력이 tick마다 처음부터 재검사되어 복구와 뒤의 실패를 계속 막는다

- 위치: `packages/py/kor-travel-common/src/kortravelcommon/dagster.py:211-238`, `:337-343`.
- 실패 시나리오: 최신 대상 run이 적격 RUN_EXCEPTION/DagsterSubprocessError이고 STEP_FAILURE는 100건+1건의 유한한 두 페이지다. 모든 기록은 FRAMEWORK_ERROR/ChildProcessCrashException/user_failure_data=None으로 유효하다. metadata 각 페이지가 5.1초에 정상 반환한다.
- 원인: STEP_FAILURE loop 내부에는 시간 확인이나 지속 checkpoint가 없다. 외부 10초 대기는 끝나지만 worker는 계속 다음 페이지를 읽는다. 다음 tick은 run 및 step cursor를 처음부터 다시 시작한다.
- 실제 독립 재현: 순수 실패 실행 두 개를 자체 SQLite에 생성했다. 오래된 적격 실패와 더 최신의 적격 자식 종료다. STEP_FAILURE 조회에만 정상적인 두 페이지와 5.1초 지연을 주입하고 실제 SensorDefinition.evaluate_tick을 두 번 실행했다. 10초 상한은 변경하지 않았다.
- 관찰: 두 tick 모두 10.0초에 DeadlineExceeded. 페이지 방문은 [None, page-2, None, page-2], sensor cursor는 미전진, 오래된 실패는 한 번도 검사되지 않았다. 늦게 완료한 worker는 최신 부모를 pending=true/max_retries=0으로 바꿨지만 호출자에게 RunRequest가 전달되지 않아 child는 0개였다. 실제 worker 종료를 기다린 뒤 instance를 닫아 하네스의 DB close 경합을 배제했다.
- 영향: 같은 metadata 지연이 유지되면 해당 자동 복구와 그 뒤의 실패 처리가 계속 진전하지 않는다. run monitoring이나 단순 다음 tick이 이 진행 문제를 해결하지 않는다. 모든 앱의 장애나 4개 thread slot 고갈을 실제로 재현했다고 주장하지는 않는다.
- 최소 수정: 부분 이력 검사만으로 재시도를 허용하지 않으면서 한 run의 검사 진행을 지속 checkpoint하여 다음 tick에서 이어가거나, 시간 예산을 소진한 run을 명시적으로 격리하고 뒤 run 검사를 진전시킨다. 전체 검사 완료 전 provider/mixed-page를 허용하면 안 된다. timeout 뒤의 worker가 불필요하게 검사·metadata 쓰기를 계속하는 범위도 줄여야 한다.
- 검증 조건: 같은 두 페이지 지연에서 복구 또는 명시적 격리와 뒤 실패의 진행이 확인되고, 뒤 페이지 provider 기록은 계속 거부되어야 한다.

### 재현 파일과 명령

파일: `/tmp/james-common-child-92ebfa60/slow_pages_probe.py`\
SHA256: `978fd049d0dda2c7b1fba2944745d1add49403a6e3ba101db254f09885c5330b`

```bash
cd /tmp/james-common-child-92ebfa60
PYTHONPATH=/tmp/james-common-child-92ebfa60/packages/py/kor-travel-common/src \
TMPDIR=/tmp TMP=/tmp TEMP=/tmp \
/home/digitie/dev/kor-travel-geo-codex-dagster-common-test/.venv/bin/python slow_pages_probe.py
```

독립 실행 exit 0의 assertion은 결함을 확인하는 assertion이다.

```json
{"actual_deadline_seconds":10,"valid_finite_pages":2,"delay_per_page_seconds":5.1,"tick_durations":[10.0,10.0],"pages":[null,"page-2",null,"page-2"],"cursor_progress":false,"older_checked":[],"parent_pending":true,"parent_native_budget":"0","issued_children":0}
```

## EXECUTED

- 고정 `tests/test_child_crash.py`: **7 PASS / 5.10초**. 실제 multiprocess os._exit(42), RunRequest 1개·child native 잔여 예산 0을 포함한다.
- 고정 `tests/test_recovery.py`: **56 PASS / 9.05초**. 기존 scope·부분 선택·native/fallback budget·인계·metadata 오류 회귀를 포함한다.
- 자체 10초 실제 deadline/두 페이지/두 tick liveness 공격: 위 결함 재현.
- classifier의 provider·user_failure·unknown·no-evidence·뒤 페이지 mixed 실패는 신규 테스트에서 거부됨을 확인했다.
- Git pathspec의 WSL quoting 실패 1회는 명령 오류로 구분하고 명시적 4파일 경로로 source를 읽었다. 제품 결함으로 세지 않았다.

## NOT_RUN·한계

- native retry ON daemon과 실제 event consumer 통합, Dagster1.9 floor, 실제 PG·provider·운영 장애 및 메모리/RSS는 NOT_RUN이다.
- STEP_FAILURE 페이지 지연은 controlled fault injection이다. 실제 운영 SQLite/PG가 반드시 이 속도로 동작한다고 주장하지 않는다.
- 메모리는 매번 100개 event 페이지를 읽도록 제한되지만 CPU·I/O 작업의 총량과 한 실행의 계속 진행 문제는 별개다.
- 부모의 63 PASS 전달을 인용해 통과로 세지 않았다. 위 63건은 본인이 고정 scratch에서 직접 수행한 결과다.
- UI/common426 관련 기존 독립 PASS는 이 신규 Python 변경의 PASS 근거로 사용하지 않았다.
- 본 원문 SHA256은 파일 생성 뒤 별도로 전달한다.
