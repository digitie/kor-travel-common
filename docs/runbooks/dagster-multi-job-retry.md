# 단일 센서로 여러 job의 인프라 재시도 처리

이 문서는 [T-319](../tasks/T-319-dagster-recovery.md)의 추가 API 설계와 소비자 채택 경계를 기록한다. 기존 [Dagster 가이드](dagster-adoption.md)의 정책을 대체하지 않는다. 기준은 Common34 d1aa4bb이며 dagster_recovery.py와 소비자 코드는 변경하지 않는다.

## 설계와 수용 기준

Weather의17개 job은 멱등 infra retry1을 선언하지만 공유 instance native retry가 비활성이라 태그만으로 새 실행이 생성되지 않는다. 작업별 센서17개 대신 단일 센서가 명시한 job/policy mapping을 공유한다. 중앙 native를 켜면 최종 STEP_FAILURE 외의 원인불명/초기화 오류와 이전 provider 실패 뒤 crash도 재시도되어 기존 정책과 같지 않으므로 이번 변경에서 활성화하지 않는다.

추가 factory infrastructure_retry_sensor_for_jobs(..., jobs={job.name: (job, policy)})는 기존 단일 infrastructure_retry_sensor와 같은 내부 판정을 사용한다. 기존 단일 API의 signature·기본 RUNNING·RunRequest 형태를 유지한다.

- tick당 project FAILURE run 최대100 한 페이지·동일5초 협력 budget·외부10초 deadline과 단일 cursor를 공유한다. job 수만큼 scan/thread를 만들지 않는다.
- 정확 project/location/repository/job allowlist, 명시 멱등 policy, 부분 선택/불완전 plan 거부, 이전 provider/사용자 step 실패 이력 거부를 보존한다.
- native/manual/Common child 중복과 같은 job active를 확인한다. policy 예산·deterministic run_key·pending 인계 원계를 유지하고 다중 factory 요청에만 명시 job_name을 추가한다.
- native ON 때 pending 외 위임, pending 완료 뒤 중복 억제는 기존 계약을 따른다. native를 켜는 기능은 아니다.
- 한 tick 최대1 RunRequest를 유지한다. 공유 cursor/checkpoint와 느린 metadata/예외/재시작 후 인계 회귀를 확인한다.
- 로컬 실제 Dagster+SQLite와 모형만 사용한다. 외부 서비스·provider·PG·실제 job·소비자 배포·CPU/RSS 효과는 NOT_RUN이다.

## 채택 절차

구현·wheel·기존 회귀와 두 독립 리뷰가 끝난 고정 SHA를 소비자가 별도 PR로 채택한다. Weather pin/센서 등록은 이번 Common PR에 포함하지 않는다. 이전 job별 센서와 새 다중 센서를 동시에 RUNNING으로 두지 않는다. 미완료 pending/기존 child/cursor를 먼저 정산하고, metadata 오류나 물리 worker UNKNOWN을 종료 성공으로 취급하지 않는다. 실행 시각·poll 위상 분산은 실측 후 정하되 원천 수집 횟수·발표 시각 계약과 catch-up 억제를 보존한다.

현재 상태: 설계만 고정했으며 구현·검증·독립 리뷰·운영 채택은 후속이다.
