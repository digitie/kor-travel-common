<!-- SPDX-License-Identifier: GPL-3.0-only -->

# Common 최종 수정 후보 — 독립 merge post-fix 리뷰 원본

- 실행 ID COMMON-MERGE-A-20261005-ab21cc3; James (/root/review_ui).
- 시각 2026-10-04 22:47:34~22:52:04 UTC / 2026-10-05 07:47:34~07:52:04 KST.
- 저장소 F:/dev/kor-travel-common-geo-dashboard.
- 원 base589a01ef63ff1ce81960e3d531874b5e4c892995; 실제 immutable candidate ab21cc3b7b77e5e6d6cd277ca64840761fc4d7a4.
- 직접 후속 delta3194a0b→ab21 및 기존 UI426·Python 단계별 독립 리뷰 맥락의 전체 base delta를 검토했다.
- **최종 verdict CONDITIONAL**, 신규 P2 아래. 기존 P1은 FIXED.

## 독립 full/light 판단

작성자 판단을 대신 사용하지 않고 고정 AGENTS.md §5/8과 agent-workflow.md §5를 직접 읽어 **full 대상**으로 판단했다. base→candidate는 packages 공개 UI/API/CSS와 Python 복구 동작 및 비면제 runbook을 변경한다. 오탈자나 의미 동일 link만 바꾸는 light 조건을 충족하지 않는다. 두 전문 reviewer의 독립 immutable 검토·post-fix 검토·필수 gate가 필요하다.

후속 원본 보고서 보존·disposition/index만의 closure artifact는 런타임 변경과 구분되며 동일 리뷰를 재귀적으로 다시 시작할 필요가 없다는 예외는 적용 가능하다. 규범·코드·gate를 바꾸면 이 예외는 사용할 수 없다. 본 보고서는 문서 전용 후속 commit을 source candidate로 혼동하지 않는다.

## 격리·범위

고정 Git show/diff/archive로 읽었고 rev-parse로 실제 SHA를 확인했다. source archive /tmp/james-common-merge-ab21cc3를 사용하며 다른 reviewer 원문/통합 판정은 읽지 않았다. source/install/mirror/공유 DB를 수정하지 않았다. 기존 Geo venv Python3.12.13/Dagster1.13.24를 PYTHONPATH로 읽기 재사용하고 자체 SQLite만 사용했다.

base→candidate 13개 제품·guide·changelog 파일의 scope를 확인했다. UI source/package/tokens는 이전 본인 검토426와 고정 diff 동일, 소비자 dev.3 vendor의 실제 UI 의미는 Geo596b 단위51건에서 재확인했다. 이번 직접 runtime 공격은 완료/부분 phase, 늦은 provider·framework 기록, 최신 failure ID, native·예산·타입 경계에 집중했다. 전체 UI 빌드나 다른 reviewer 영역을 실행했다고 주장하지 않는다.

## EXECUTED

- 고정 child_crash + recovery: **67 PASS,67.14초**. 실제 os._exit42 및 RUN_FAILURE3.1초/STEP5.1초/active2.1초의 유한 지연 회귀를 포함한다.
- 기존 실제 SQLite late-provider 재현: completed cursor 이후 동일 RUN_FAILURE ID3를 유지하며 provider STEP_FAILURE를 append해도 resume0request·쓰기0. cold 및 changed RUN_FAILURE 대조군도0request.
- legacy3필드/type invalid8/nativeON pending없음/attempt소진 공격 PASS.
- 실제10초 outer deadline을 유지한 추가 late-framework 지연 공격은 아래 새P2를 재현했다.

## 기존 finding disposition

- C-CHILD-P1-01(P1): FIXED 유지. 여러 유한 페이지가 cursor로 진행하고 검사 중 태그를 쓰지 않는다.
- C-PHASE-P1-01(P1): FIXED. 기존 SQLite provider 후속 기록 재현이 요청0·태그0으로 바뀌었다. severity와 과거 원문은 변경하지 않았다.

## C-MERGE-P2-01 — 늦은 정상 framework 기록과 느린 조회에서 복구 phase가 영구 순환함 (P2)

- 위치 packages/py/kor-travel-common/src/kortravelcommon/dagster.py:395-410; 같은 기록을 failure_event로 전달하는411-415.
- 시나리오: 실제 RUN_EXCEPTION/DagsterSubprocessError 전에 유효 child crash1개가 있고, 같은 run에 유효 FRAMEWORK_ERROR/ChildProcessCrashException/user_failure_data=None 기록1개가 늦게 저장된다. provider/unknown 오류는 전혀 없다. RUN_FAILURE 조회3.1초·STEP 조회5.1초는 정상 유한 응답이다.
- 재현: 실제 DagsterInstance.report_dagster_event와 SQLite records를 사용했다. storage record 종류/ID를 위조하지 않았고 실제10초 outer deadline을 변경하지 않았다. 6tick 결과:
  - durations [8.21,3.1,0.0,8.21,3.1,0.0].
  - phase [complete,run,head,complete,run,head].
  - 요청0·태그0.
  - 같은 변하지 않은 실제 이력의 빠른 cold scan은 요청1.
- 원인: completed checkpoint의 최신 RUN_FAILURE+STEP_FAILURE 조회가 STEP_FAILURE를 반환하면, 그 record를 RUN_FAILURE처럼 retry_failed_run에 전달한다. 종료 사유가 없어 Skip되고 cursor가 run→head로 이동한다. 다음 cold scan은 전부 유효함을 증명하지만8.2초 때문에 다시 complete를 저장하여 동일 순환이 반복된다.
- 영향: provider 안전성은 지키지만 유효한 자식 종료 복구가 안정적인 지연·늦은 저장 조합에서 진행하지 않는다. 일반적인 실제 Dagster 실행에서 이 ordering의 발생 빈도는 측정하지 않았다. delayed/backfill event 경계의 기능 결함으로 P2다.
- 최소 수정: 최신 STEP 변경은 완료 캐시를 무효화하되 실제 RUN_FAILURE와 새 STEP 안전 검증을 단계별로 계속 진행하도록 한다. provider/user/unknown은 요청0·태그0을 유지하고, 늦은 유효 framework만 있는 이력은 고정 latency에서도 유한 tick 안에 요청1이어야 한다.
- disposition 필요조건: 수정 및 이 실제 지연 회귀, 또는 P2 연기 규칙에 맞는 owner·상세 task·gate·기한이 필요하다. 해당 disposition 없이 전체 PASS로 표시하지 않는다.

## 재현 산출물

/tmp/james-common-merge-ab21cc3:
- late_provider_probe.py SHA25672ace6cdb9f58db4d65f1702db32e78a387d2cb141f9cba4752bdc29063fb4e7.
- late_crash_liveness_probe.py SHA25610aad60bad6bfa29438170db23eaea916b5a436730e47a3efef1f91a31910a5a.
- phase_boundary_probe.py SHA25658b6458b337cd80bf21089f6c36204f016f5e6fcec6df6f73866177032155d2a.

```bash
cd /tmp/james-common-merge-ab21cc3
PYTHONPATH=/tmp/james-common-merge-ab21cc3/packages/py/kor-travel-common/src TMPDIR=/tmp TMP=/tmp TEMP=/tmp /home/digitie/dev/kor-travel-geo-codex-dagster-common-test/.venv/bin/python late_crash_liveness_probe.py
# 같은 환경에서 late_provider_probe.py, phase_boundary_probe.py도 실행했다.
cd packages/py/kor-travel-common
PYTHONPATH=/tmp/james-common-merge-ab21cc3/packages/py/kor-travel-common/src TMPDIR=/tmp TMP=/tmp TEMP=/tmp /home/digitie/dev/kor-travel-geo-codex-dagster-common-test/.venv/bin/python -m pytest -q tests/test_child_crash.py tests/test_recovery.py
```

## NOT_RUN·최종 판정

Dagster1.9/native daemon/PG/provider/CI/clean package build·install/live는 직접 수행하지 않았다. 단일 storage 호출 자체>10초의 기존 강제 스레드 중단 불가 한계도 그대로다. 다른 reviewer 결과를 읽거나 부모 gate를 본인 PASS로 산입하지 않았다.

**CONDITIONAL**. 기존 본인 P1은 수정됐고 실제67건은 통과한다. 새 P2의 수정 또는 규칙에 맞는 명시적 연기 disposition과 full gate 확인이 남는다.
