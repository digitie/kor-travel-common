<!-- SPDX-License-Identifier: GPL-3.0-or-later -->

# 공통 Python 자식 프로세스 복구 독립 post-fix 리뷰 — Popper 원본

실행 ID: POPPER-COMMON-CHILD-92EBFA60-20261005-065803

시작: 2026-10-05T06:58:03.349072+09:00. 종료: 2026-10-05T07:02:16.716754+09:00.

판정: **PASS — 본 공통 delta 범위**. 최초 `B-G-P1-03`은 아래 고정 common 후보에서 **CLOSED**다. 새 P0/P1/P2/P3 finding은 확인하지 못했다. 이 판정은 아직 별도 검토하지 않은 geo 후속 후보, live E2E, CI 또는 운영 배포의 통과 판정이 아니다.

## 고정 대상과 격리

- 저장소: `F:\dev\kor-travel-common-geo-dashboard` / `/mnt/f/dev/kor-travel-common-geo-dashboard`.
- 실제 base: `426de4fbad35282bb558712d922c06268e9aba62`.
- 실제 candidate: `92ebfa60ef976d830c08b353de633103650175ad`.
- Linux Git 객체의 SHA와 전체 diff를 확인했다. 변경은 Python `dagster.py`, 신규 crash fixture/테스트, 운영 가이드 네 파일이다. UI·vendor·패키지 public 타입/의존성 선언은 이 delta에서 변하지 않았다.
- 고정 `git archive` scratch: `/tmp/popper-common-child-92ebfa60-20261005`. common 소스를 `PYTHONPATH` 맨 앞에 둬 설치된 구버전과 분리했다. Python 3.12.13 / Dagster 1.13.24 가상환경을 읽기 전용 재사용했다. 설치·외부 원본·부모 mirror·저장소 소스·DB·provider를 변경하지 않았다.
- 다른 리뷰어 원문/결과 및 부모가 전달한 RED/GREEN 로그는 읽지 않았다. 본인의 최초 geo 원본과 실제 fixture를 재사용했다.

## EXECUTED

1. 후보 공통 Python 전체 테스트를 본인 고정 snapshot에서 실행: **63 PASS, 14.39초**. 실제 `os._exit(42)` fixture도 포함된다. 로그: scratch의 `original-common-tests.log`.
2. 최초 geo9db391에서 실패했던 **동일한 본인** `/tmp/popper-geo-9db39180-20261005/native_crash_fallback_probe.py`를 새 common `PYTHONPATH`로 실행: **exit 0**. 실제 multiprocess child 종료와 local SQLite run/event store를 사용했다. native OFF, `RUN_EXCEPTION`, 재시도 요청 **1개**가 반환됐다. 로그: `original-geo-native-crash-postfix.log`. 실제 geo 백업/provider는 실행하지 않았다.
3. 본인 추가 실제 SQLite 이벤트 저장소 경계 테스트: **8 PASS, 2.85초**. 로그: `independent-boundary-tests.log`.
   - STEP_FAILURE 102개 중 마지막에 일반 provider 오류를 저장했다. 실제 페이지 조회는 `(100, has_more=True)` 후 `(2, has_more=False)`였고, 재시도는 차단됐다.
   - 두 번째 이벤트 페이지 조회만 ConnectionError를 내게 했다. 실패 tick은 cursor를 소비하지 않았고, 저장소 복원 뒤 동일 대상을 평가해 요청 1개를 반환했다.
   - 실제 child-crash 분류에서도 native retry_number=1, fallback attempt=1, 음수/NaN 예산 태그는 재시도를 차단했다.
   - 명시 op selection은 증명된 crash여도 전체 실행으로 확대하지 않았다.
   - native OFF 요청 뒤 native ON으로 전환한 pending 부모는 동일 run key로 인계를 계속했다. child의 native 잔여 예산은 0이고 pending 태그를 상속하지 않았다. child가 발급된 이후 추가 요청은 없었다.

추가 harness의 초기 ErrorSource import 경로와 SQLite 기본 이벤트 정렬 가정을 본인 scratch에서 수정했다. 이는 후보 소스 결함이 아니며 수정 후 위 8건을 재실행했다. 저장소 구현은 수정하지 않았다.

동일 fixture 실행의 핵심 환경은 다음과 같다. 재사용 가상환경의 Python으로 실행하며 `PYTHONPATH` 순서는 아래와 같다.

```text
/tmp/popper-common-child-92ebfa60-20261005/packages/py/kor-travel-common/src
/tmp/popper-geo-9db39180-20261005/src
/tmp/popper-geo-9db39180-20261005/kor-travel-geo-dagster/src
fixture: /tmp/popper-geo-9db39180-20261005/native_crash_fallback_probe.py
```

## B-G-P1-03 disposition

최초 원인은 pinned430의 RUN_EXCEPTION 제외 및 모든 STEP_FAILURE 제외로 실제 multiprocess ChildProcessCrashException이 영구 skip된 것이었다. 신규 `packages/py/kor-travel-common/src/kortravelcommon/dagster.py:185-240`은 RUN_EXCEPTION + DagsterSubprocessError에 한해 별도 경로를 열고, 최소 하나의 crash 기록 및 모든 STEP_FAILURE의 FRAMEWORK_ERROR / ChildProcessCrashException / user_failure_data 없음 조건을 요구한다.

이는 일반 RUN_EXCEPTION 전체 허용이 아니다. 실제 최초 fixture에서 요청 0→1이 되었고, 일반 provider/user/unknown/no-evidence 및 다음 페이지에 섞인 provider 실패는 차단됐다. 기존 최소 retry 예산·origin/project/location·선택 범위·native pending 인계 검사도 유지됐다. **CLOSED, 최초 severity P1 유지**. 최초 geo FAIL 원본을 수정하지 않았다.

## READONLY와 남은 운영 경계

전체 delta 및 기존 factory의 metadata 오류, cursor 순환, run key, config replay, native/fallback 총예산, 부모 pending 저장/child 미상속을 읽었다. 100개 이벤트씩 검사하며 한 페이지만 보고 안전하다고 결론내리지 않는다. cursor가 전진하지 않으면 예외로 보류한다. event 이력 조회까지 전체 10초 bounded call 안에 있으며, 기존 4개 장수 thread 상한은 그대로다.

deadline은 대기 상한이며 thread 강제 종료가 아니다. timeout 이후 늦은 metadata 쓰기는 기존 durable pending 인계 계약에 의존한다. 동시 수동 run과 domain 데이터 게시 안전성은 소비자 lease 및 shared coordinator가 별도로 보호해야 한다. 이번 변경이 이를 대체한다고 주장하지 않는다.

라이선스/SPDX 및 Python package 경계는 유지됐다. 이번 delta는 UI tarball이나 TypeScript 공개 계약을 바꾸지 않는다.

## NOT_RUN

Dagster 1.9 최소 버전 재실행, 실제 shared daemon/launcher 및 native ON worker-crash 통합, 실제 PostgreSQL, 실제 geo 백업 재실행, frontend/live E2E, RSS/전체 동시 run 부하, CI 직접 실행과 wheel 재설치는 수행하지 않았다. 부모의 common 63 PASS 및 기존430 RED/신규 GREEN 보고는 독립 수행 근거에 합산하지 않았다.

`B-G-P1-01`/`B-G-P1-02`는 geo 소비자 코드 finding으로 이 공통 delta 판정의 대상이 아니다. 별도 고정 geo 후속 후보에서 검토해야 한다.
