# Dagster 공통 로직 적용 가이드

weather에서 검증한 실행 복구 구조를 transport·map·pinvi·geo로 확산할 때 사용하는 가이드다.
공용 API는 [Python 패키지](../../packages/py/kor-travel-common/README.md), UI 계약은
[Dagster 운영 표시](../standards/ui-contract.md#48-dagster-운영-표시t-216-개발-후보)가 정본이다.
적용 작업과 배포는 각 소비자 저장소 PR에서 수행한다. 이 문서는 다른 앱의 채택 완료를 뜻하지 않는다.

## 1. 의존성 고정과 책임

Python dependency는 병합된 common의 **전체 commit SHA**와
`#subdirectory=packages/py/kor-travel-common`을 고정하고 소비자 lock을 갱신한다.
Dagster 실행 환경에는 `kor-travel-common[dagster]`를 설치한다. API 전용 환경은 core-only
패키지를 설치해도 Dagster를 import하지 않는다. `@main` 등 이동 참조는 사용하지 않는다.

common은 정책 태그·중복 예약 방지·주입형 회수 sensor·동기 호출 deadline·표시 UI를 소유한다.
소비자는 DB schema/transaction·provider·인증·run 소유권·멱등성·실제 daemon/launcher 배포를
소유한다. provider client의 자체 구현이나 도메인 SQL을 common으로 복사하지 않는다.

## 2. job과 schedule

```python
from dagster import define_asset_job
from kortravelcommon.dagster import RecoveryPolicy, coalescing_schedule

project = "transport"
location = "앱의 실제 code location 이름"
policy = RecoveryPolicy(
    max_runtime_seconds=7200,
    idempotent=True,
    infrastructure_retries=1,
)
collect = define_asset_job(
    "collect", tags=policy.tags(project=project, job_name="collect")
)
schedule = coalescing_schedule(
    project=project, location_name=location, job=collect,
    name="hourly_collect", cron_schedule="0 * * * *",
    execution_timezone="Asia/Seoul",
)
```

예약은 현재 location의 동일 job이 QUEUED·STARTING·STARTED·CANCELING이면 합친다.
foreign location의 동명 job은 막지 않는다. NOT_STARTED 기록은 제출되지 않은 기록일 수
있으므로 예약을 영구 차단하지 않는다. metadata 조회 장애는 tick 실패로 전달한다.
consumer의 기존 `should_execute`도 주입하여 보존한다.

실행 상한은 job의 실제 처리량에 맞춘다. weather의 외부 sweep은 13시간 실측 때문에
16시간 상한을 유지하며 최신성 KMA/AirKorea는 2시간, regional은 6시간이다. 이를 다른 앱에
무조건 복사하지 않는다. timeout은 hang을 회수하는 상한이며 목표 처리 시간 SLO가 아니다.

`idempotent=True`는 전체 재실행이 unique key/upsert 또는 외부 시스템의 idempotency key로
안전하다는 뜻이다. Pinvi email/Telegram outbox, geo restore 같은 비멱등 작업은 기본
재시도 0회를 유지한다. 문자열 `"false"`·float·boolean 상한 같은 동적 잘못된 입력은 거절한다.
provider/op 오류는 provider의 제한된 재시도와 다음 정상 tick에 맡기며 native run retry는
worker/launcher 장애만 맡긴다. 수동 취소는 자동으로 되살리지 않는다.

## 3. 실제 daemon 설정과 메모리

[instance 설정 예시](../../packages/py/kor-travel-common/README.md#instance-설정)를 실제
daemon의 YAML에 병합한다. 태그만 넣어서는 run monitoring/retry가 켜지지 않는다.
shared plane은 소비자의 YAML을 사용하지 않을 수 있으므로 daemon 소유 저장소에서 적용한다.
`run_coordinator`와 `concurrency.runs`를 혼용하지 않는다. 기존 pools/그룹 제한은 보존한다.

`kortravelcommon/job` 값별 동시성 1과 project별 예산을 둔다. weather의 project 6/외부그룹 3은
다른 앱의 슬롯을 남기는 예시이며 모든 소비자에 같은 값을 적용하는 정책은 아니다.
자산 job을 직접 resolve하면 `default_executor_def=multiprocess_executor.configured(
{"max_concurrent": 1})`를 적용하고 실제 resolved job의 executor 설정을 검사한다.

fact/raw payload를 run 전체에 모으지 않는다. 작은 batch와 한 provider 응답만 유지하고,
fact 수·source 수·payload bytes를 함께 제한한다. 값이 없는 응답도 raw buffer를 비운다.
fan-out 경로도 같은 staging 상한을 적용한다. 전체 normalized 생성 예산은 batch flush나
upsert no-op 이후에도 누적한다. ID/count/skip 집합만 run 전체에서 유지한다.
모든 batch에 source lineage를 포함하고, 부분 commit 뒤 실패해도 누적 count와 raw를 보존한다.
실행 전체의 all-or-nothing 계약을 바꾸면 소비자의 architecture·테스트도 함께 갱신한다.

## 4. 수집 행의 소유권과 회수 sensor

소비자는 수집 행에 Dagster run ID, heartbeat, running/terminal 상태를 연결한다.
각 게시 transaction은 수집 행의 상태를 잠금/CAS로 확인하며, 회수된 worker의 늦은 게시를
거절해야 한다. terminal worker는 즉시 회수하고, 생존 확인된 worker는 오래된 heartbeat만으로
죽이지 않는다. 조회 장애는 사망으로 간주하지 않는다. metadata에 없는 ID는 충분한 lease
grace가 만료되고 UPDATE 시 heartbeat까지 다시 만료된 경우에만 회수한다.

```python
from kortravelcommon.dagster import reconciliation_sensor

def reconcile(context):
    repository = context.resources.repository.create_repository()
    try:
        # 앱이 소유한 SQL/CAS. Dagster 조회는 DB transaction 밖에서 한다.
        return repository.reconcile_workers(context.instance)
    finally:
        repository.engine.dispose()

recovery = reconciliation_sensor(
    name="worker_recovery", reconcile=reconcile,
    required_resource_keys={"repository"},
)
# Definitions(..., sensors=[recovery])
```

회수 후보는 stable keyset(`started_at`, `run_id`)으로 bounded page를 순회하거나 sensor cursor로
이어 읽는다. 첫 페이지가 생존 행으로 가득해도 뒤 terminal 행을 영구 누락하지 않는다.
connection·lock·statement·RPC 대기 상한을 소비자 환경에 맞춰 설정한다.
legacy 무소유 행은 별도 lease 회수로 이관하며 신규 소유권 migration을 코드보다 먼저 적용한다.

## 5. 동기 호출 정지

```python
from kortravelcommon.deadline import DeadlineExceeded, call_with_deadline

try:
    response = call_with_deadline(lambda: client.fetch(target), timeout_seconds=120)
except DeadlineExceeded:
    # 해당 client의 다음 dataset/close와 경합하지 않고 step을 끝낸다.
    raise
```

대기만 제한하며 daemon thread를 강제로 종료하지 않는다. timeout 뒤 동일 client를 재사용하거나
close하지 않는다. async client는 제공자의 public timeout/cancellation 계약을 사용한다.
worker process 회수는 run monitoring/launcher가 소유하며, daemon/code server 자체 중단은
서비스 관리자의 restart/healthcheck가 필요하다. OS process의 실제 종료도 운영에서 확인한다.

## 6. 공용 운영 UI

소비자가 scope를 제한한 `DagsterSnapshot`과 label/URL/새로고침 콜백을 주입한다.
`@kor-travel/ui/dagster.css`와 tokens를 가져오며 패키지의 Tailwind 클래스를 소비자 빌드에서
탐지한다. 앱 페이지의 바깥 여백은 소비자가 제공한다.
`scheduleUrl(name, repository)`는 복수 repository의 동명 schedule도 구별한다.
`testId`와 공개 `data-slot`을 e2e selector로 사용한다. 인증·GraphQL proxy·수동 실행/취소는
소비자에 남긴다. run의 `maxRuntimeSeconds`를 전달하여 긴 batch를 거짓 정체로 표시하지 않는다.
공용 로그인 폼과 메뉴도 소비자의 auth/Link/pathname을 주입해 사용한다.

## 7. PR 검증과 운영 확인

소비자 PR에서 최소한 다음 실패 경계를 재현한다.

- 동일 job pending/active에서 중복 예약 억제, foreign 동명 job·정상 terminal 뒤 예약 허용.
- worker 중단/metadata 유실/조회 장애, heartbeat 갱신과 회수 경쟁, 늦은 게시 거절.
- 첫 페이지 생존/다음 페이지 terminal, 전체 생성 예산과 raw-only/전국 fan-out의 메모리 상한.
- 부분 commit 뒤 replay의 중복 방지·lineage·count, timeout 뒤 client 미재사용.
- 실제 instance 설정 수용과 resolved executor, 패키지 설치·소비자 전체 회귀·CI.
- 실제 브라우저 로그인 실패/성공/로그아웃·메뉴·실패 원인·상한·새로고침·상세 링크,
  작은 viewport·computed 오류 색상·여백 정렬.

합성 Python allocation과 운영 전체 RSS는 구분한다. 운영 배포 뒤 launcher crash/hard hang/
취소/native retry child 실행과 shared host RSS를 확인한다. 실행하지 않은 배포 검증은
`NOT_RUN`으로 남긴다. 독립 2인 리뷰와 post-fix 재검토 evidence를 PR에 연결한다.
