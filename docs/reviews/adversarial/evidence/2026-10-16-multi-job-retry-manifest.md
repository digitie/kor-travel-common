# 다중 job retry 독립 리뷰 manifest

- 요청: 반복 수집 실패/영구 정지 방지·메모리/CPU 부하 분산 공통화.
- 기준 base: d1aa4bbacab87af9ebae08757bd3fcb80f748fe9(Common34).
- 제품 commit: 1b599c4663737c468ce163af03d446beb3d210fc. 문서 포함 검토 commit은 동일 PR35의 고정 handoff에서 두 reviewer에게 똑같이 전달한다.
- 작성자: C. reviewer는 동일 immutable source에서 서로 다른 계약/복구·패키징/예산 관점으로 독립 검토하고 서로의 결과를 읽지 않는다.
- 범위 밖: 중앙 native 설정 활성화, 소비자 pin/등록·스케줄 변경, 운영/외부 서비스·PG·실제 job, Common34 dagster_recovery.py, health·HTTP·phase·의존성 파일 변경.

## 전체9파일

- packages/py/kor-travel-common/src/kortravelcommon/dagster.py
- packages/py/kor-travel-common/tests/test_multi_job_retry.py
- docs/runbooks/dagster-multi-job-retry.md
- docs/runbooks/dagster-adoption.md
- docs/tasks/T-319-dagster-recovery.md
- docs/resume.md
- docs/journal.md
- CHANGELOG.md
- docs/reviews/adversarial/evidence/2026-10-16-multi-job-retry-manifest.md

## 계약·공격 범위

[T-319](../../../tasks/T-319-dagster-recovery.md)와 [가이드](../../../runbooks/dagster-multi-job-retry.md)를 따른다.
기존 단일 API/RunRequest 호환, 명시 다중 target·config/policy 귀속, 100개 초기 page·공유5초 budget/
10초 deadline·cursor/step checkpoint, 부분 선택/이전 provider 실패·불명 사유 제외,
native/manual/Common child 중복·같은 job active·native ON pending 인계·재시작/오류를 공격한다.
기존 pytest에는 로컬 SQLite/loopback만 사용한다. 소비자 운영 gate를 로컬 PASS로 대체하지 않는다.

## 작성자 검증과 실행 가능 명령

패키지 디렉터리에서 잠긴 venv로 ruff check . / python -m pytest -q / uv build를 수행했다.
전체443PASS(1.13.25), 관련78PASS(신규22포함), 별도1.13.24 관련161PASS,
core-only3.11 wheel/설치 bytes·새 API import는 작성자 검증이며 독립 reviewer 실적으로 합산하지 않는다.
root 문서 links/plan·도구 unittest(336PASS/1SKIP)·diff를 확인한다.
소비자 배포/실제 복구·CPU/RSS/live E2E와 독립 두 리뷰는 NOT_RUN이다.

## 독립 리뷰 종결 기록

고정03396709 전체9파일에 대한 [A 원문](2026-10-16-multi-job-retry-reviewer-a.md)과
[B 원문](2026-10-16-multi-job-retry-reviewer-b.md)(팀 D)를 bytes 그대로 보존했다.
[통합 판정](../2026-10-16-multi-job-retry-closure.md)은 두 PASS/OPEN0이다.
위 검토 기준 manifest는03396709 Git object에 그대로 남고 이 절은 그 이후 closure 기록이다.
제품·수용 계약은 바꾸지 않으며 소비자 운영과 종결 commit CI/merge는 별도다.


## 최종 Common34 기준선 문서 통합

원 검토03396709/closure58d2426은 immutable 이력으로 보존한다. Common34의 최종
`4ad615e2abb0f11f846dead8381ef91d923a0f1d` 위로 올린 후 packages 전체 tree가
03396709와 동일함을 확인했다. A/D 원문·원 closure 보고서와 Common34 원문6개는
바이트 그대로이며 새 제품 판정/독립 테스트 수를 추가하지 않는다. 문서 충돌은 양쪽
절을 보존해 정산했다. 새 HEAD CI·Common34 선행 병합·소비자 운영 gate는 별도다.
