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
아직 종료하지 않은 동기 호출은 프로세스당 4개로 제한한다. timeout 뒤에도 실제 종료까지
slot을 점유하며, 용량 부족은 `DeadlineExceeded`로 전달한다. 확인 실패를 정상/빈 큐로 바꾸지 않는다.
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


## 8. Transport 채택 사례 (2026-10-04)

Weather PR #72와 common PR #24의 Python 코어 및 PR #25의 보강 코드를 transport가 고정하여 사용한다.
도메인 `CollectionRun` SQL은 transport에 둔다. `0024` migration의 `orchestrator_run_id`·`heartbeat_at`을
추가하고 전용 collector session의 flush/commit에서 status·owner를 잠가 늦은 게시를 거절한다.
부분 commit은 보존하며 terminal Dagster 실행의 running 기록만 회수한다. metadata 조회 실패는
죽은 worker의 근거가 아니며, 없는 run은 4시간 실행 상한보다 긴 5시간 grace와 heartbeat CAS를 거친다.

수집 정책은 앱이 결정한다. Transport의 KRIC는 실패·강제 종료도 마지막 시도부터 48시간을 지키며,
버스 기준정보는 성공 후 72시간, 철도 기준정보는 성공 후 48시간을 보호한다. 유가·장소의 과금과
provider receipt를 generic retry로 우회하지 않는다. 자동 인프라 재시도는 멱등 공항·고속도로·휴게소
기준정보에 1회만 허용하며 provider 실패는 `Failure(allow_retries=False)`와 run tag 정책으로 막는다.

UI `0.1.0-dev.2`는 5분·4시간·8시간 cron, 키보드 진입 가능한 두 표, terminal 경과 시간을 제공한다.
Transport는 최근 30건 외 진행 중 목록을 별도로 합쳐 중복 제거하고 job의 `dagster/max_runtime`을
공통 snapshot에 전달한다. 실패 event는 location tag와 UUID를 함께 제한하여 페이지를 넘겨 읽는다.
작업별 GraphQL·본문 크기·시간 상한과 인증·Origin은 소비자가 유지한다.

**실제 instance**: transport의 `backend/dagster_home/dagster.yaml`은 전용 instance용이다.
공용 daemon 운영에서는 Manager가 소유한 instance YAML의 monitoring, `run_retries.enabled`,
`retry_on_asset_or_op_failure=false`, project/job tag concurrency를 별도로 확인해야 한다.
code-server의 YAML만 바꾸고 shared instance가 바뀌었다고 보고하면 안 된다. candidate의 격리
instance 결과와 운영 shared instance의 활성 설정/worker 종료 결과를 evidence에서 구분한다.

### native retry가 비활성화된 공용 instance

Transport의 실제 shared instance는 monitoring만 활성화되어 있었다. job의 `dagster/max_retries`
태그는 instance의 native retry를 켜지 않는다. 이때 다음 fallback sensor를 사용한다.

```python
from kortravelcommon.dagster import RecoveryPolicy, infrastructure_retry_sensor

worker_retry = infrastructure_retry_sensor(
    name="transport_infra_retry_airport_collection_job",
    project="transport", location_name="kor-travel-transport", job=airport_collection_job,
    policy=RecoveryPolicy(14400, idempotent=True, infrastructure_retries=1),
)
# 소비자의 Definitions(sensors=[worker_retry, ...])에 등록한다.
```

`UNEXPECTED_TERMINATION`, `START_TIMEOUT`, `RUN_WORKER_RESTART` 이벤트를 허용한다.
멀티프로세스 자식 종료는 `RUN_EXCEPTION` + `DagsterSubprocessError`이고, 모든 step 실패가
`FRAMEWORK_ERROR` + `ChildProcessCrashException`이며 user failure가 없는 경우에만 허용한다.
적어도 하나의 자식 종료 기록을 요구한다. 실패 이력은 100건씩 끝까지 검사하므로 뒤 페이지에
provider 오류가 섞여 있어도 제외한다. 느린 유한 페이지는 5초 작업 예산 뒤 마지막 검사 위치를
sensor cursor에 저장해 다음 tick에서 이어 읽는다. 부분 검사 중에는 재시도 요청이나 native 억제
태그를 쓰지 않는다. 전체 sensor의 10초 제한과 인계 전 잔여 시간 검사는 이 검사에도 적용된다.
검사가 끝났지만 인계 예산이 부족하면 완료 phase도 저장한다. 느린 마지막 STEP 조회 직후에는 추가 중복·활성 실행 조회 전에 완료 위치를 저장해, 전체 deadline이 이 지점을 지우지 않게 한다. 다음 tick에서 RUN_FAILURE와
STEP_FAILURE 중 최신 이벤트를 함께 조회하고, RUN_FAILURE와 검증한 마지막 STEP의 storage ID 중 최대값이 그대로일 때만 완료 검증을
재사용한다. 최신 기록이 검증한 STEP이면 저장된 종료 사유와 명시적 child crash 증거를 사용한다.
새 step 실패가 추가되면 부분 phase로 돌아가 다음 tick에서 종료 사유와 cursor 이후 기록을
확인한다. 새 provider 오류는 거부하고 늦은 정상 child crash만 있는 이력은 복구를 계속한다.
기존 3/5필드 checkpoint는 종료 사유부터 다시 검증하며 새 6필드 형식으로 전진한다.
일반 step/provider 실패·취소·원인 불명은 재예약하지 않는다. 실제 자식 `os._exit(42)`와
native retry OFF인 격리 SQLite instance로 fallback 요청 1개와 잔여 예산 0을 검증한다.
project/location을 함께 검증하고, 실행 중인 같은 job은 합친다. 재시도 횟수와 부모 run ID를
공통 태그에 기록하며 결정적인 run key로 이벤트 재평가를 중복 제거한다. run config를 보존해
전체 멱등 job을 다시 실행한다. repository origin도 기본 `__repository__`와 일치해야 하며,
다른 이름은 factory의 `repository_name`에 주입한다. origin 없는 실행은 project/location 태그를
함께 요구한다. partition job과 부분 op/asset 선택 실행은 지원하지 않는다. native retry 횟수도
같은 예산에 합산하고 이미 발급된 native/fallback child를 확인한다. fallback child뿐 아니라
원 parent의 native 예산도 요청 반환 전에 닫는다. 제출 실패에는 같은 run key로 다시 준비한다.
억제 태그와 `kortravelcommon/infra_retry_pending=true`를 같은 metadata 쓰기에 남긴다.
저장 응답이 유실되거나 제출 전에 native retry를 켜도 이 표식이 있는 인계는 fallback이
마무리한다. 발급된 child를 확인하면 표식을 false로 닫고, child에는 표식을 상속하지 않는다.
실행 계획의 일부 step 또는 resolved op subset도 전체 job으로 확대하지 않는다.

일반 polling sensor가 실패 실행 100건씩 확인하고 한 tick에 한 실행만 재예약한다. batch 끝에서
새 실패부터 다시 확인하며, metadata 장애·10초 timeout에는 cursor를 전진시키지 않는다.
느리지만 정상인 조회에서는 5초 작업 예산 뒤 마지막 완료 행을 저장해 다음 tick에서 이어간다.
run failure callback 예외도 이벤트를 소비하는 Dagster 동작을 피하기 위한 경계다. 전체 조회는
10초/동시 4개 상한이며 metadata 장애는 sensor tick 실패로 전달한다. native retry 활성화 시
미완료 인계만 처리하고 새 실패는 native에 위임한다. 오래된 실패가 많으면 한 순회만큼 복구가 지연될 수 있다.
native retry 설정 전환은 기존 daemon/code-server를 drain한 뒤 수행하여 서로 다른 설정의
daemon을 동시에 두지 않는다. fresh sensor의 최초 순회는 기존 scope의 미재시도 실패도 대상이다.

sensor 확인과 다른 수동/예약 발화는 원자적이지 않다. shared coordinator의 job limit과 소비자
DB lease를 함께 적용한다. DB lease는 중복 provider 호출을 막지만 queued run의 메모리 제한을
대신하지 않는다. 같은 instance에서 운영 daemon과 sensor가 실제 실행되는지도 배포 후 확인한다.

## Geo 구성의 공용 운영 UI 채택

`@kor-travel/ui/dagster-operations`의 `DagsterOperations`에 앱이 범위가 적용된
`snapshot`, `runUrl`, `scheduleUrl`, `onRefresh`를 제공한다. `showRunDetails`와
`showRepositories`를 켜면 목록/상세와 코드 위치를 함께 표시한다. `selectedRunId`와
`onSelectRun`으로 선택을 제어하고 `renderRunDetail`로 앱의 실패 확인·백업 다운로드를
그대로 연결한다. 선택 실행이 최근 목록 밖에 있으면 콜백에는 `null`이 전달되므로
앱은 제어 중인 ID로 상세를 조회한다. 외부 작업 실행·재시도 권한은 앱이 소유한다.

repository의 선택 `sensors`, schedule의 `lastTick`, `timezone`, `overdue`는 API가
확인한 값만 전달한다. 조회 실패 시 `error`와 마지막 성공 snapshot을 함께 넘기면
마지막 결과임을 명확히 표시한다. 인증 실패를 빈 정상 snapshot으로 바꾸지 않는다.
`schedule.jobName`은 `string | null`이다. 작업 이름을 모르는 API는 null을 전달하고,
문자열 함수에 전달하는 소비자는 `jobName !== null`로 좁힌다. 스케줄 이름을 작업 이름으로 추측하지 않는다.
`scheduleUrl`의 repository 인자를 자체 `jobName: string` 타입으로 좁혀 선언했던 소비자는
공용 `DagsterRepository` 타입을 사용하고 nullable 값을 좁힌다. 콜백이 실제로 받는 공용 타입을 축소하지 않는다.
행은 50개씩 렌더링하며 검색·집계는 전달된 전체 실행에 적용한다. 서버는 최근 종료
실행과 오래된 활성 실행을 모두 포함하되 응답 상한·취소 가능한 요청·polling을 적용한다.
CSS는 `@kor-travel/ui/dagster.css`, 토큰은 `@kor-travel/tokens/tokens.css`를 로드한다.


## PinVi 후속 — 실행 상한 미확인 (2026-10-05)

`DagsterRun.maxRuntimeSeconds`는 양수이면 실제 cap, 생략하면 기존 600초 지연 heuristic,
명시적 `null`이면 cap 미확인이다. `null` run은 cap 기반 stalled count에 넣지 않고 상세에
미확인으로 표시한다. 생략의 상세는 “지연 판단 기준”으로 구분하여 실제 daemon 설정인 척하지 않는다.
UI `0.1.0-dev.4`로 새 artifact를 만들며 기존 dev.3 bytes를 바꾸지 않는다.
PinVi가 run tag를 확인해 숫자 또는 null을 전달한다. 운영 RSS·shared daemon 배포는 NOT_RUN이다.

## 실제 code location 자동 탐색 gate

조립용 임시 `Definitions` 객체는 모듈 전역에 남기지 않는다. `_base_defs` 같은 private 이름도
Dagster 자동 탐색은 포함하며, 최종 `defs`와 함께 남으면 gRPC가 code location을 로드하지 못한다.
소비자에서 `dagster job list -m <module> -d <working-directory>`와 실제 gRPC import 경로를 확인한다.
단순 Python import/`defs.get_repository_def()` 검사만으로 배포 로딩 gate를 대신하지 않는다.
PinVi 채택에서 실제 이전 실패→후보 성공을 회귀로 확인했다(PinVi PR #575).

## 모바일 표와 기본 옵션 gate

UI dev.6은 표 영역 내부 가로 스크롤과 공통 grid child의 `min-width: 0`을 함께 적용한다.
`showRunDetails=false` 기본 경로도 별도 검증한다. 표에 최소 너비만 주면 unclassed grid wrapper가
min-content를 페이지로 전파할 수 있다. 320/390/640px에서 문서 폭이 viewport를 넘지 않고,
focus 가능한 표 영역에서 ArrowRight로 스크롤되는지 확인한다. 상세 표시 경로만 검사하지 않는다.


## 9. GraphQL·상태 조회의 응답과 대기 상한

API 환경은 `kor-travel-common[http]`를 전체 SHA에 고정하고 lock을 갱신한다.
`kortravelcommon.http.bounded_request`는 기본 4MiB plain 응답, 읽기 전체 10초와
별도 정리 최대 50ms를 적용한다. 압축 헤더는 해제 전에 거부하며 오류 status에도 같은
상한을 적용한다. redirect와 HTTPX 인증 재요청은 비활성화한다. Bearer 등 인증 header,
URL 허용목록과 client 수명은 앱이 관리한다. body를 먼저 읽을 수 있는 response hook는
거부한다. 표준 HTTPX 또는 취소에 협조하는 transport만 지원하며 취소를 억제하는
임의 transport의 강제 종료는 보장하지 않는다. 본문 실패는 원래 예외를 유지하고 정상 본문 뒤 정리 실패도 `BoundedResponseError`로 알린다.
`httpx.RequestError` 뒤에는 client를 폐기하고, 가능하면 조회 단위로 client 수명을 제한한다.
외부 취소 뒤 client 폐기도 앱 책임이다.

```python
from kortravelcommon.http import bounded_request

response = await bounded_request(client, "POST", graphql_url,
    json={"query": query, "variables": variables},
    max_response_bytes=4 * 1024 * 1024, total_timeout_seconds=10)
response.raise_for_status()
payload = response.json()
if not isinstance(payload, dict):
    raise ValueError("GraphQL 응답은 객체이어야 합니다.")
```

`BoundedResponseError`는 `httpx.RequestError`다. write 요청에서 이런 실패를 성공이나
미실행으로 단정하지 않는다. 앱의 기존 uncertain outcome·idempotency key·claim 복구
절차를 유지한다. provider 업무 실패를 새 run으로 무조건 복제하지 않는다.

대시보드는 최근 완료 목록과 별도 활성 실행 목록을 함께 조회해 오래된 STARTED를
숨기지 않는다. 활성 목록을 자르면 정상 전체 집계로 표시하지 않고 degraded로 알린다.
잘못된 results shape와 HTTP 200 degraded 응답은 정상 빈 목록으로 캐시하지 않는다.
UI는 마지막 정상 snapshot과 조회 시각·장애 경고를 함께 유지한다.

Map처럼 전체 snapshot의 완료 봉인이 필요한 적재는 batch마다 봉인하거나 부재 행을
삭제하지 않는다. 변환은 작은 batch로 나누되 기존 단일 transaction과 최종 한 번 봉인을
유지한다. 각 worker의 executor 동시성·DB pool도 함께 줄여 프로세스별 메모리 곱셈을 막는다.

## 10. code-server 자식 로딩을 확인하는 경량 건강 점검

`code-server start`의 proxy `DagsterApi` health는 자식 load error에도 SERVING일 수 있다.
`python -I -m kortravelcommon.dagster_health <loopback-port>`를 `[dagster]`가 설치된 이미지에서
실행한다. 공통 `code_server_is_healthy(port)`는 proxy health 뒤 자식 `ListRepositories`를
각 4초·수신 4MiB 상한으로 호출하고 channel을 닫는다. 빈 protobuf, 손상 wire/JSON,
중복 JSON 필드, 다른 class, 누락/손상 repository symbol은 모두 실패한다. 정상 빈 symbol
목록은 정상 `ListRepositoriesResponse` schema이면 허용한다.

Dagster 전체를 import하지 않고 설치된 Dagster의 생성 protobuf를 파일로 로드한다.
wire schema를 복제하지 않으며 설치 경로/프로토콜 변경도 정상으로 오인하지 않는다.
이 호출은 health 판정만 한다. Docker `unhealthy`는 자동 재시작을 의미하지 않으므로
소비자의 watchdog/launcher·native run monitoring·중지 복구 정책을 별도로 유지한다.
CLI 기동·두 RPC를 포함하도록 컨테이너 healthcheck timeout은 15초 이상으로 두고,
실제 사용 Dagster 버전·이미지에서 성공/빈 응답/load error/deadline을 확인한다.

Map standalone 채택의 실제 protobuf 빈·잘못된 reply가 기존 substring probe에서
healthy로 통과한 적대 리뷰 반례가 승격 근거다. Manager와 Map의 같은 proxy/자식 로딩
계약 비용을 공통 Python으로 줄이며 Manager 운영 watchdog은 이 변경으로 대체하지 않는다.
새 공통 후보·Map 채택의 운영 재구축/live gate는 아직 NOT_RUN이다.

건강 점검의 JSON 지원 profile은 현재 소비자가 쓰는 `ModuleCodePointer`, `FileCodePointer`,
`PackageCodePointer`와 표준 문자열/목록/nullable metadata다. 포인터 필드·working directory,
executable/entry point/image, library versions와 plain JSON container context도 검증한다.
Custom/autoload pointer, stateful `defs_state_info`, typed container context와 새/알려지지 않은
필드는 정상으로 추측하지 않고 실패한다. 이 profile은 임의 Dagster serdes 객체의 대체물이
아니며 해당 location을 채택하려면 고정 Dagster 버전의 실제 positive/negative reply 회귀와
명시적 공통 profile 확장이 먼저다. 현재 Map 운영 module location에서 실제 CLI를 확인한다.

Library versions와 repository pointer dictionary의 Dagster serdes marker 키
(`__class__`, `__enum__`, `__set__`, `__frozenset__`, `__mapping_items__`)도 거부한다.
일반 repository 이름 `__repository__`는 marker가 아니며 Map Definitions의 정상
default 이름으로 허용한다. 실제 serializer/isolated CLI 정상 control을 유지한다.

## 11. 최신 tick 조회의 저장소 작업 상한

Dagster 1.13.24의 repository batch loader는 `ticks(limit: 3)`만으로 전체 tick 이력의 rank 작업을 제한하지 않는다. 실제 Map 요약은 sensor tick 저장소의 15초 statement timeout 때문에 실패했으며, API의 공통 HTTP 10초 deadline이 먼저 `unavailable`로 반환했다. HTTP·응답 cap을 늘리거나 공유 DB의 이력을 삭제하지 않는다.

Map·PinVi처럼 최신 3건을 표시하는 요약은 `ticks(limit: 3, statuses: [STARTED, SKIPPED, SUCCESS, FAILURE])`를 사용한다. 실제 설치 schema의 네 상태를 전부 포함하므로 실패·진행 중 tick을 숨기지 않는다. 이 버전에서는 nonempty `statuses`가 batch loader를 우회하고 selector별 최신 LIMIT 조회를 사용한다. 실제 Map의 같은 query는 2.077초에 정상 응답했으며 state당 최대 3건을 유지했다. [독립 진단·조회 검증](../reviews/adversarial/evidence/map-health-2026-10-05/review-summary-tick-query-recovery.md)을 참조한다.

이 query 선택은 소비자 API가 소유한다. 공통 Python HTTP 코드는 요청 전체 deadline·응답 바이트 상한·연결 정리를 계속 적용한다. Dagster를 업그레이드할 때는 실제 enum과 resolver 경로를 다시 확인한다. 새 tick 상태가 추가되면 전체 상태 선택과 검증을 함께 갱신한다. selector의 legacy NULL 값과 timestamp 동률에서 두 저장소 경로가 완전히 같다고 주장하지 않는다. 수용 기준은 소유 instigation의 최신 최대 3건과 모든 현재 상태·오류 정보를 보존하는 것이다.
