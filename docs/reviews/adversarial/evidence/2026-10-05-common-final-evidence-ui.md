<!-- SPDX-License-Identifier: GPL-3.0-or-later -->

# Common 최종 6필드 체크포인트 — 독립 리뷰 원본

- 실행 ID COMMON-FINAL-A-20261005-73e3ff8; 리뷰어 James (/root/review_ui).
- 관측 2026-10-04 23:02:17~23:05:49 UTC / 2026-10-05 08:02:17~08:05:49 KST.
- 저장소 F:/dev/kor-travel-common-geo-dashboard.
- base589a01ef63ff1ce81960e3d531874b5e4c892995.
- 실제 immutable candidate73e3ff8b9398e533806d2d1a8435292570169de3, Git rev-parse 확인.
- 후속 ab21→73e3 delta와 원 base의 전체 공용 계약을 기존 본인 독립 검토 맥락에서 평가했다.
- **최종 판정 PASS (독립 소스·실행 검증 범위)**. 신규 finding 없음. 외부 merge gate 완료를 뜻하지 않는다.

## 격리·전체 범위

이동 HEAD/worktree 소스 대신 고정 Git show/diff/archive를 읽었다. 자체 /tmp/james-common-final-73e3ff8 archive와 기존 Geo venv Python3.12.13/Dagster1.13.24를 PYTHONPATH로 사용했다. 본인 SQLite instance·공격 파일만 생성하고 제품/설치/mirror/사용자 dirty 파일/외부 서비스를 변경하지 않았다. 다른 reviewer 원문·통합 판정·closure는 읽지 않았다.

원 base delta의 공개 UI·CSS·모델·타입·guide·Python 복구·테스트·smoke 계약을 본인 앞선 독립 리뷰와 연결해 확인했다. UI source/package/CSS/tokens는 이전 PASS UI426와 고정 diff가 동일하며, Geo 최종51건에서 실제 dev.3 vendor 소비를 재검증했다. 이번 직접 Python 검토는 6필드 검증·완료/부분 phase·마지막 STEP ID·새 종료 사유·provider/unknown·native·예산·legacy 호환성과 시간/메모리 상한이다.

## full/light 독립 판단

고정 AGENTS.md §5/8 및 agent-workflow.md §5의 규칙은 ab21과 동일함을 확인했다. 작성자와 별도로 **full 대상**이라고 판단한다. 원 base delta는 공개 UI/API/CSS, Python 복구 및 비면제 runbook을 변경하며 light의 오탈자·공백·동일 의미 link만 조건을 충족하지 않는다. 두 전문 reviewer의 immutable 독립 리뷰 및 post-fix gate가 필요하다.

원본 리뷰·disposition/index만 보존하는 문서 전용 closure artifact는 runtime 변경과 구분하며 같은 리뷰를 재귀적으로 재시작하는 예외 대상이다. 규범/코드/gate 변경은 그 예외에 포함되지 않는다. 후속 closure commit의 HEAD를 이 소스 기준선으로 바꾸지 않았다.

## EXECUTED·결과

1. 고정 child_crash/recovery **69 PASS,99.19초**. 실제 os._exit42, 100+1페이지 각5.1초, RUN_FAILURE3.1초/STEP5.1초/active2.1초, 늦은 child를 RUN_FAILURE 뒤 및 완료 phase 뒤 저장한 두 실제 SQLite 지연 회귀를 직접 실행했다.
2. 본인 C-MERGE-P2-01의 실제10초 outer deadline/3.1초 RUN·5.1초 STEP/실제 event ID 이력을 재실행했다. 이전 complete→run→head 영구 순환 대신 [8.21초,3.11초] 두 tick에서 요청1·태그 쓰기1·잔여예산0으로 진행했다. 같은 이력 fast 대조군도 요청1이다.
3. 본인 C-PHASE-P1-01의 실제 provider append 재현: 최신 RUN_FAILURE ID3가 같아도 새 STEP ID는 완료 cache를 무효화하고 partial로 돌아간다. 다음 tick의 provider 검사는 요청0·태그0; cold와 changed RUN_FAILURE 대조군도0.
4. legacy3·legacy5는 종료 사유부터 재검증한다. nativeON pending없음 요청0·budget소진 요청0, 기존 invalid checkpoint8개 및 신규6필드 잘못된 STEP ID 타입3개 거부 PASS.
5. 완료 이후 metadata 오류→partial cursor 보존→복원 후 provider 거부, 새 RUN_FAILURE의 STEP_FAILURE 사유, 새 unknown framework 클래스 모두 실제 SQLite에서 요청0·pending 쓰기0 PASS.
6. cursor는 한 run과 opaque event cursor/상수 개수의 ID·count만 보존한다. 100run/100event page·tick 요청1·기존 bounded4 worker 구조를 검토했다. 실제 RSS 감소율을 측정하지 않았다.

## 본인 finding disposition

- C-CHILD-P1-01(P1): FIXED 유지. 느린 여러 유한 페이지의 checkpoint 진행.
- C-PHASE-P1-01(P1): FIXED 유지. 완료 뒤 provider 기록은 새 ID로 invalidate하고 거부.
- C-MERGE-P2-01(P2): **FIXED**. 마지막 검증 STEP ID를 저장하고 matching STEP의 child crash 속성을 확인하므로, 정상 늦은 child를 종료 이벤트로 잘못 해석하지 않는다. 새 기록은 partial phase로 돌아가 유한 tick에 실제 종료 사유·cursor 이후 이력을 검증한다. 본인 실제 지연 재현 요청1로 폐쇄했다.
- 신규 P0/P1/P2/P3 finding 없음. 기존 severity·원문은 수정하지 않았다.

## 자체 재현 파일·명령

/tmp/james-common-final-73e3ff8:
- late_crash_liveness_probe.py SHA256bd7190d7f842be82191422068cb31141f0dfdd8ba9dd186287a2625b95a25164.
- late_provider_probe.py SHA2566ba3db8f603428d4a49307e9001f3fda0b0635742d8379f9211856f2eca43360.
- phase_boundary_probe.py SHA25658b6458b337cd80bf21089f6c36204f016f5e6fcec6df6f73866177032155d2a.
- extra_safety_probe.py SHA2567f361d2f02ad773d15e6b47aa60f5f4e7dfa19cd07f581d50ed5bd9343bfe6d7.

```bash
cd /tmp/james-common-final-73e3ff8
PYTHONPATH=/tmp/james-common-final-73e3ff8/packages/py/kor-travel-common/src TMPDIR=/tmp TMP=/tmp TEMP=/tmp /home/digitie/dev/kor-travel-geo-codex-dagster-common-test/.venv/bin/python late_crash_liveness_probe.py
# 같은 환경에서 late_provider_probe.py, phase_boundary_probe.py, extra_safety_probe.py도 실행.
cd packages/py/kor-travel-common
PYTHONPATH=/tmp/james-common-final-73e3ff8/packages/py/kor-travel-common/src TMPDIR=/tmp TMP=/tmp TEMP=/tmp /home/digitie/dev/kor-travel-geo-codex-dagster-common-test/.venv/bin/python -m pytest -q tests/test_child_crash.py tests/test_recovery.py
```

## NOT_RUN·한계·판정

실제 PG/production daemon/provider·Dagster1.9, clean wheel/tarball install/build, CI·직접 live UI/픽셀·전체 소비자 gate는 본인이 수행하지 않았다. 단일 storage 호출 자체가10초를 넘으면 기존 deadline이 daemon thread를 강제 종료하지 못하며 bounded slot은 종료까지 점유한다. 새 checkpoint가 임의의 metadata 지연을 모두 해결한다고 주장하지 않는다.

**PASS**: 본인 모든 코드 finding은 재현으로 수정 확인됐으며 잔여 finding이 없다. 사용자 요청의 두 독립 full 원본·필수 CI·소비자 native/live gate를 merge 담당이 따로 확인해야 한다. 이 원본은 미실행 gate를 PASS로 집계하지 않는다.
