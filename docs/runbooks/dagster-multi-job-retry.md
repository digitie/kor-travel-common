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

## 사용 예와 한계

Dagster extra를 설치한 소비자가 이미 소유한 JobDefinition과 명시 policy만 넘긴다.

    from kortravelcommon.dagster import infrastructure_retry_sensor_for_jobs

    collection_retry = infrastructure_retry_sensor_for_jobs(
        name="collection_infrastructure_retry",
        project="example",
        location_name="example.collection",
        jobs={
            selected.name: (selected, retry_policies[selected.name])
            for selected in idempotent_jobs
        },
    )

mapping은 비어 있지 않고 key와 job.name이 같아야 하며 모든 policy는 멱등·양수 retry 예산을 명시해야 한다. partition job은 기존처럼 거절한다. 입력 mapping/pair는 등록 때 고정한다. 기본 RUNNING/minimum_interval_seconds=60이므로 소비자는 새 factory 등록 전에 이전 센서와의 전이를 계획한다. 예제는 앱 설정이나17개 job의 정책을 생성하지 않는다.

단일 factory는 한 번의 최대100개 초기 failure page를 공유한다는 뜻이다. 적격 후보마다 event 이력·기존 child·active 조회가 있으므로 **tick 전체 SQL이1회라는 뜻은 아니다**. 5초는 협력 budget이며 blocking metadata 호출의 hard timeout은 아니다. 요청 직전8초 인계 여유 검사와10초 외부 deadline은 기존대로다. 조회 오류는 성공 cursor로 소비하지 않고 pending 인계는 재시작 후 같은 run_key로 재제안한다. 별도 실행 UUID 발급·submit 성공/physical worker 사망을 이 함수가 증명하지 않는다.

동시 수동 launch나 서로 다른 센서 사이의 원자적 once는 보장하지 않는다. 같은 run_key라도 서로 다른 sensor origin의 중복 억제를 대신하지 않으므로 이전 센서와 새 센서를 동시에 켜지 않는다. consumer DB lease/queue 제한·원천 멱등 upsert는 그대로 필요하다.

## 로컬 검증과 미실행 gate

구현 제품1b599c4 기준 잠긴 Dagster1.13.25 전체443PASS, 신규22개와 기존 단일56개를 합한78PASS, 별도 Dagster1.13.24의 다중/단일/incarnation 관련161PASS를 확인했다. 새17-job 회귀는 이전 API에서1FAIL 후 통과했다. 로컬 SQLite의 합성 run/event만 사용했고 provider/PG/외부 서비스는 호출하지 않았다.

Python3.11 빈 venv에 core-only wheel을 설치해 Dagster/SQLAlchemy import가 없음을 확인했다. 별도 설치 wheel의 새 함수/전체 dagster.py bytes를 소스와 대조하고1.13.24 dependency tree에서 import했다. 소비자 pin/이미지·센서 등록·실제 worker 유실 후 복구·live UI·운영 CPU/RSS 효과는 NOT_RUN이다. 두 독립 리뷰와 최종 CI도 별도 gate다.
