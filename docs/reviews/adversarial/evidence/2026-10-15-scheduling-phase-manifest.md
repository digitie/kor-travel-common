# 고정 phase 예약 분산 독립 리뷰 manifest

- 제품/가이드 기준 commit: `c12e0a7b9de907b9597371a0de5fa052d8bfcc7d`.
- base/parent: `8d04353464ccfb4c1efe5c4725274581e4110600`.
- 이 manifest와 최신 검증 journal/resume만 후속 문서 commit으로 함께 보존한다.
  리뷰 시작 시 전달된 최종 HEAD의 전체 base diff를 두 reviewer가 각각 확인한다.
- task: [T-319 수용 설계](../../../tasks/T-319-dagster-recovery.md).
- 계약/경계: [가이드 §13](../../../runbooks/dagster-adoption.md#13-명시적인-고정-phase로-예약-시작-분산),
  [Python 규약](../../../standards/backend-stack.md), [workflow](../../../runbooks/agent-workflow.md).
- 범위: scheduling 공개 pure helper·실제 Dagster 달력 회귀·Python README·가이드·
  CHANGELOG·task·journal·resume·본 manifest. 소비자 소스/pin·runtime·서비스·배포 변경은 없다.

## 근거와 수용 조건

Weather `acc8c71fb2dfb60f10654403081b7b4b21d75f62`의
`packages/kor-travel-weather-dagster/src/kortravelweather_dagster/definitions.py` external
스케줄 loop는 같은 3시간 cron을 쓴다. Transport
`15a928b07c7a30415cfa3d81ba5ee412e79981f5`의 `backend/app/dagster/definitions.py`는
airport/highway에 같은5분 cron을 쓴다. 두 소스의 git object만 읽었고 변경하지 않았다.

지원 주기/phase 타입과 범위, clock을 정확히 나누지 않는 주기 거절, 재시작 동일성,
예약 추가 독립성, 실제 SDK 달력의 count/간격/phase·자정/월/연도/DST 경계,
기존 coalescing/failure 후 새 예약 의미 보존, core-only 무Dagster import를 검토한다.
수집량·provider 발표 시각·freshness·실제 동시성/CPU 개선의 거짓 보장도 공격 대상으로 둔다.

## 작성자 검증

- locked dev+dagster 전체 pytest230PASS, ruff PASS, uv build PASS.
- 운영과 같은 Dagster1.13.24 별도 로컬 환경의 신규 달력/예약 시험70PASS.
- core-only wheel 격리 설치: Dagster 미설치·미import, hash seed가 다른 새 프로세스2개
  모두 기존9 phase cron 동일. 패키지 runtime 의존 추가0.
- 문서 link693/target2803 오류0, plan109 오류0, unittest337=336PASS/1SKIP, diff PASS.
- 순수 helper10만회 x86 로컬 tracemalloc peak916바이트·current80바이트,
  wall0.931147초/processCPU0.931098초. SDK/run·운영 RSS/실제 절감률과 구분한다.
- 최초 zip strict 누락 ruff 실패와 미설정 Git identity는 로컬 도구 문제로 수정했다.
  실패를 숨기거나 제품/운영 실패로 바꿔 집계하지 않는다.

검증 명령은 workflow의 Python/문서 gate이며, 신규 회귀는
`packages/py/kor-travel-common/tests/test_scheduling.py`다.
두 독립 FULL 리뷰·최종 CI는 PENDING. 소비자 적용·운영 수집/취소·RSS/PSS/CPU·live E2E는
NOT_RUN(후속 소비자 PR 소유). 검토 원문은 각 execution ID·시간·고정 HEAD·scope·
finding ID/severity/disposition·verdict·한계를 보존하고 상대 reviewer 결과를 읽지 않는다.
