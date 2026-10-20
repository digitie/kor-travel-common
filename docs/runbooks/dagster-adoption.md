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
tick 예산과 연속 실패 경보는 [§19](#19-회수-sensor의-tick-예산과-정체-경보)의 opt-in 인자를 사용한다.

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

## 12. 호스트 이전과 중지 상태 복구

이 절은 Geo 이전 과정에서 확인한 Dagster 1.13.24 동작을 같은 제어 평면을 사용하는
소비자가 재검증할 때 참고하는 절차다. 새 공용 Python API나 모든 소비자의 이전 완료를
뜻하지 않는다. Docker·workspace의 생명주기는 Manager가 소유하고, 앱의 실행 정책과
데이터·백업·인증은 각 소비자가 소유한다. 앱별 실행 상한·메모리·DB pool 튜닝은 보존한다.

### 실행이 없는지 확인하기

`dagster code-server start`의 proxy와 관리되는 `dagster api grpc` 자식은 같은 RPC를
모두 지원하지 않는다. 이 버전의 proxy는 `GetCurrentRuns`를 전달하지 않아
`UNIMPLEMENTED`를 반환한다. 이를 빈 실행 목록으로 처리하면 안 된다. 실제 실행을
관리하는 API 자식의 지원 RPC와 metadata의 활성 run·진행 중 tick을 함께 확인한다.
proxy가 정상이어도 자식 load error가 있을 수 있으므로 §10의 로딩 검사도 유지한다.
조회 실패·시간초과·응답 오류·조회 중 child 교체는 실행 없음의 증거가 아니다.

중지된 schedule도 scheduler가 `ScheduleInstigatorData.last_iteration_timestamp`를
기록할 수 있다. 이 버전은 처음 값이 없을 때와 checkpoint 간격이 지났을 때 해당 값을
갱신하며 `STOPPED`·cron·`start_timestamp`를 보존한다. 이 필드 차이만으로 재활성화나
작업 실행을 단정하지 않는다. 전환용 snapshot을 비교할 때 정상 checkpoint만 구분하고
상태·origin·cron·시작 시각·sensor cursor의 차이는 계속 검증한다. 변경된 checkpoint는
유한한 숫자·비역행·관측 시간 범위를 확인하며, 비교를 맞추려고 DB 값을 되돌리지 않는다.
업그레이드 후에는 실제 설치 SDK의 해당 경로와 설정을 다시 확인한다.

### 파일과 코드 등록 순서

호스트 파일을 rename으로 교체해도 이미 생성된 file bind mount는 이전 inode를 볼 수
있다. daemon·web·code server가 실제로 읽는 instance/workspace와 호스트 파일을 각각
확인한다. 호스트 SHA만 같거나 compose 경로가 맞다는 이유로 실제 mount도 같다고
가정하지 않는다. 필요한 서비스만 갱신하고 다른 code location 전체를 reload하는
workspace reload로 우회하지 않는다. 전체 stack·DB·실행 worker 재시작도 별도 범위로
판단한다. workspace reload 자체가 DB를 재시작한다는 뜻은 아니다. 같은 inode에 설정을 쓸 때도
부분 쓰기·parser 관측 가능성을 고려하고, 변경 후 실제 mount와 native 조회로 확인한다.

1. 새 code server를 자동 예약이 중지된 상태로 준비하고 실제 설치 코드·storage·권한을 확인한다.
2. 기존 location의 예약을 중지하고 실제 worker·활성 run·진행 중 tick이 없는지 확인한 뒤 정상 종료한다.
3. 새 workspace에 등록한 뒤 native `RepositoryLocation` 로딩과 앱별 scope를 확인한다.
4. 실제 설정에서 부작용이 없는 검증 job을 정해 큐 제출·실제 worker 실행·terminal 결과까지 확인한다.
5. 실패 감지·제한된 재시도 sensor와 필요한 schedule을 앱별로 복원하고 최초 완료 tick을 별도 확인한다.

Geo처럼 backup 설정이 이미 비활성화된 경우의 due 조회 job은 검증 후보가 될 수 있다.
실제 설정·출력·DB 작업 및 artifact 변화가 없음을 확인해야 하며, 운영 값을 임의로 바꿔
검증 전용 성공을 만들지 않는다. repository가 보이거나 HTTP 200인 것만으로 daemon의
큐 소비와 실행 성공을 증명할 수 없다. 완료 뒤에도 이전 호스트의 정본 배포 설정이
폐기된 code server를 다시 올리지 않도록 Manager의 배치 설정을 함께 정리한다.

### 시작 RPC의 시간 예산과 실행 증거

Dagster 1.13.24에서 daemon → code-server proxy → API child의 시작 RPC는 두 구간이다.
실제 이전 검증에서는 기본 60초 deadline이 만료된 뒤 같은 run의 늦은 worker와 큐 재처리가
겹쳤다. 바깥 run-monitor의 STARTING 상한만 늘려서는 안쪽 RPC deadline이 바뀌지 않는다.

부모 RPC에는 자식 RPC보다 여유를 두고, STARTING monitor는 부모 RPC보다 길게 둔다.
해당 ARM64 배포에서 검증한 proxy 300초·daemon 360초·monitor 600초는 소비자별 예시다.
이를 모든 앱의 공통 기본값으로 고정하거나 기존 자원·배치·동시성 튜닝을 바꾸지 않는다.
`DAGSTER_GRPC_TIMEOUT_SECONDS`는 StartRun 전용 변수가 아니라 일반 RPC 기본값이다.
schedule·sensor·repository·shutdown의 별도 시간 예산도 함께 대조하고 영향 범위를 기록한다.
env 파일을 편집한 것만으로 이미 실행 중인 두 구간에 설정이 반영됐다고 가정하지 않는다.

응답 timeout 뒤에는 알려진 run과 worker를 먼저 정산한다. 기존 FAILURE를 SUCCESS로
덮거나 결과가 불명확한 제출을 반복하지 않는다. 부작용 없는 새 검증 run을 사용한 경우에도
그 run의 큐 이벤트·정확한 repository origin·worker·terminal SUCCESS와 업무 출력·백업
불변을 함께 연결해야 한다. 과거 실패 이력과 새 검증 성공은 별도 증거로 보존한다.

### 정본 origin과 상태 비교

복원할 sensor·schedule은 실제 workspace/저장 상태의 정본 origin으로 조회한다.
endpoint와 location 이름이 같아도 serialized origin ID가 같다는 뜻은 아니다.
이 버전에서는 `GrpcServerCodeLocationOrigin.use_ssl=None`과 명시적 `False`가
비TLS 연결을 사용하면서도 서로 다른 origin ID를 만들었다. selector 일치만 확인하거나
ID 비교를 완화하지 말고 origin ID·selector와 실제 정의의 interval/type 또는 cron/timezone을
함께 비교한다. 다른 버전에 이 생략 규칙을 그대로 적용하지 않는다.

중지 schedule의 합법 checkpoint 차이를 정산할 때도 원본 snapshot과 실제 관측 snapshot을
보존한다. 검토한 특정 상태의 전체 SHA를 새 CAPTURE와 다시 비교하고 ACTIVATE 직전
전체 snapshot CAS를 유지한다. 실행 중 임의 상태를 정상화하거나 새 checkpoint를
자동 승인하는 예외로 넓히지 않는다.

### healthcheck 비용과 상태 판정

컨테이너 health와 개별 job 실패를 구분한다. 높은 CPU에서는 짧은 probe의 생성 비용,
동시 job, 열에 따른 클럭 제한을 나눠 관측한다. 메모리 점유나 load 한 값만으로 원인을
단정하지 않는다. CS의 경량 gRPC probe를 매번 Dagster 전체 import라고 분류하지 않고,
프로세스·컨테이너 소속은 실제 PID/CID로 연결한다.

daemon CLI를 HTTP 200이나 GraphQL `healthy`만으로 대체하면 thread 정지를 놓칠 수 있다.
검증한 배포의 CLI heartbeat tolerance 설정은 300초였고, 같은 SDK GraphQL 경로의
기본 tolerance는 1800초였다. 실제 판정은 heartbeat 시각에 interval(기본 30초)과
tolerance를 합산한다. 경량화하더라도 같은 instance·required daemon 집합·heartbeat
시각·interval·tolerance와 오류 처리 계약을 보존한다. 기존 CS의 child 복구·진행 중 run 보호·orphan reaper도 유지한다.

### sensor·백업 복원과 UNKNOWN

새 instance에 처음 등록하는 run-status sensor는 대상의 event high-water를 기준으로
복원한다. 확정한 high-water의 유효 `RunStatusSensorCursor`를 STOPPED 상태에 저장하고
같은 instance에서 다시 읽어 확인한 뒤 public `start_sensor`를 호출한다. cursor가 None이거나
유효하지 않으면 첫 tick이 그때의 최신 event부터 시작할 수 있으므로 start만으로
활성화와 첫 tick 사이 실패가 보호되는 것은 아니다. 전환 중 새 실패를 놓치지 않도록
활성화 직전에 high-water를 다시 올리지 않는다.
같은 instance에서 재시작할 때는 기존 cursor와 미처리 실패를 보존한다. 다른 instance의
cursor를 복사하면 기존 실패를 대량 재생하거나 새 실패를 놓칠 수 있다.
일반 retry sensor는 cursor를 새로 둬도 과거 실패를 다시 검색할 수 있으므로 실제
필터와 대상 이력을 확인한다. public `start_sensor`·`start_schedule`의 새 시작 시각을
확인하고, 첫 tick의 오류·run key·새 run을 관측한다. 단순히 RUNNING 상태를 쓰는 것과
첫 tick 성공은 구분한다. 다음 cron 시각을 계산한 것은 실제 cron 실행 증거가 아니다.

백업 catalog와 실제 파일은 별도로 이전한다. available 상태여도 대상 파일이 없을 수
있고, 보존 기간 설정 변경은 기존 `expires_at`을 연장하지 않는다. 소비자의 실제 보존
정책·최소 보존 개수·경로 허용목록을 확인한 뒤 janitor를 복원한다. 큰 파일은 작은
고정 크기 chunk로 전체 checksum을 검사해 메모리 사용량이 파일 크기에 비례하지 않게
한다. 새 비공개 경로로 복사해 검증한 뒤 기존 파일을 덮어쓰지 않고 공개하며, 임시
hardlink가 남으면 삭제 후에도 공간이 회수되지 않으므로 소유 임시 파일의 정리도 추적한다.
실제 API와 worker의 UID·파일 접근을 확인하고 광범위한 쓰기 권한 부여로 해결하지 않는다.

전환·제출 응답의 timeout은 미실행을 의미하지 않는다. 알려진 operation/run/Exec ID,
controller 상태와 실제 metadata를 먼저 조회하고, 결과를 모르는 요청을 반복 제출하거나
강제 종료·경쟁 rollback하지 않는다. 부분 성공은 별도 복구 상태로 남기며 기존 실패와
최초 실행 증거를 보존한다. 운영 주소·DSN·cookie·토큰·원본 로그는 소비자의 비공개
운영 기록에만 두고, 공개 evidence에는 검증 범위와 미관측 항목을 구분한다.


확인한 공식 원문은 Dagster **1.13.24**의
[proxy servicer](https://github.com/dagster-io/dagster/blob/1.13.24/python_modules/dagster/dagster/_grpc/proxy_server.py),
[scheduler checkpoint](https://github.com/dagster-io/dagster/blob/1.13.24/python_modules/dagster/dagster/_scheduler/scheduler.py),
[run-status cursor 초기화](https://github.com/dagster-io/dagster/blob/1.13.24/python_modules/dagster/dagster/_core/definitions/run_status_sensor_definition.py),
[workspace reload](https://github.com/dagster-io/dagster/blob/1.13.24/python_modules/dagster/dagster/_core/workspace/context.py)다.
소비자의 실제 설치 버전과 원문을 함께 대조한다.

## 13. 명시적인 고정 phase로 예약 시작 분산

`kortravelcommon.scheduling.staggered_cron(*, interval_minutes, phase_minutes)`은
Dagster import·환경변수·clock 조회·랜덤·해시·전역 예약표 없이 5필드 cron 문자열을 만든다.
phase 표는 소비자가 이름별 상수로 소유한다. 재시작이나 다른 job 추가로 기존 phase를
다시 배정하지 않는다. 저장된 스케줄을 바꾸거나 새 실행을 만드는 함수는 아니다.

```python
from kortravelcommon.scheduling import staggered_cron

cron = staggered_cron(interval_minutes=180, phase_minutes=27)
# 기존 coalescing_schedule(..., cron_schedule=cron, execution_timezone="Asia/Seoul")
```

지원하는 interval은 1,2,3,4,5,6,10,12,15,20,30,60,120,180,240,360,480,720,1440분이다.
즉 60분의 약수인 분 주기 또는 24시간의 약수인 정시 주기만 허용한다.
90분·7분처럼 clock을 이 방식으로 동일 간격 분할하지 못하는 주기는 `ValueError`다.
두 인수는 bool 아닌 정수이며 잘못된 타입은 `TypeError`,
`0 <= phase_minutes < interval_minutes` 위반은 `ValueError`다.

### 소비자 후보와 적용 순서

Weather acc8 external 9개가 `15 */3 * * *`에 모이는 관찰과 Transport 15a928b의
airport/highway `*/5 * * * *`가 공통화 근거다. 후보는 다음과 같다.

| 소비자 | interval | 고정 phase 후보 | DST 없는 clock의 예약 횟수 |
| --- | --- | --- | --- |
| Weather external 9개 | 180분 | 7,27,47,67,87,107,127,147,167 | 각8회/일, 합계72회/일 |
| Transport airport/highway | 5분 | 각각1/3분 | 각각288회/일 |

실제 Dagster 달력에서 Weather 후보의 동일 분 예약은 기존9개에서 최대1개로 나뉜다.
이 수치는 예약 시작 충돌이며 오래 실행되는 run의 동시성이 1이라는 뜻이 아니다.
이 변경만으로 전체 일일 원천 호출량·CPU 총량이 줄었다고 주장하지 않는다.
기존 job/config·수집 범위·source lineage·unique/upsert·timeout·max concurrency·coalescing은
그대로 유지하고 소비자 PR에서 phase만 핀한다. 정확한 시각보다 안정적 분산이 목적이다.

provider의 발표 시각·격자·lookback은 provider public API와 소비자 정책이 소유한다.
phase를 앞당기면 아직 발표되지 않은 값을 만날 수 있으므로 단순 cron 횟수 동등만으로
수집량·데이터 신선도 동등을 확정하지 않는다. 새 schedule을 켠 뒤 첫 실제 tick,
동일 입력/기간의 수집량·source/fact lineage·freshness·취소/복구와 RSS/PSS/CPU를 확인한다.
현재 Common 후보의 소비자 적용·운영 개선 실측은 **NOT_RUN**이다.

### clock과 실행 정책의 경계

helper에는 timezone 인수가 없다. scheduler에 `Asia/Seoul` 또는 검토한 timezone을 명시한다.
KST/UTC처럼 DST가 없는 clock에서는 자정·월/연도 경계를 포함해 interval 간격을 보존한다.
DST가 있는 지역에서는 cron의 wall-clock 의미를 따르므로 하루가 23/25시간이거나
시각이 건너뛰거나 반복될 수 있다. 고정 elapsed-time 간격이나 임의 DST 지역의 같은
실행 횟수를 보장하지 않는다. 실제 Dagster 달력/설치 버전으로 전환일을 별도 확인한다.

daemon 지연·중지 후 catch-up·tick coalescing·재시도·실제 run 시작 시각은 기존 Dagster와
소비자 계약이다. 이 helper는 실행 슬롯·reservation lock·중복 실행 방지를 구현하지 않는다.
기존 `coalescing_schedule` 및 instance 동시성 제한을 함께 유지한다. phase는 예약된
cron 위치만 고정하며 metadata 장애를 정상으로 바꾸거나 실패 작업을 자동 재실행하지 않는다.


## 14. 생존·정의 준비 조회와 복구 동작 분리

grpc_health는 **조회만** 하는 선택 모듈이다. Common31의 예약 분산과 Common32의
strict HTTP 코드를 함께 보존한 feature 기준선에서 추가했다. Common merge만으로
Manager의 effective Compose override나 소비자 이미지는 바뀌지 않는다.

| API | 확인하는 상태 | 확인하지 않는 상태 |
|---|---|---|
| grpc_code_server_is_live(port) | IPv4 loopback의 DagsterApi 표준 SERVING | 자식 정의 로딩·worker·run·DB·provider·수집 진척 |
| grpc_code_server_is_ready(port, repository_name=...) | 생존 + 지원 wire/profile의 기대 repository/symbol/pointer 일치 | 모든 실행 슬롯 여유·run 성공·worker 사망 |
| 기존 code_server_is_healthy(port) | 기존 proxy/자식 응답 계약, RPC별4초 | 새 공유 deadline·기대 repository 확인 |

선택 설치는 pip install 'kor-travel-common[grpc-health]'이다. 기본 core와 기존
dagster/http extra를 바꾸지 않는다. liveness에는 Dagster 설치가 필요 없다.
readiness는 소비자에 이미 설치된 Dagster distribution의 생성 protobuf 파일을 직접
읽으며 Dagster 본체·SQLAlchemy·앱을 import하지 않는다. 초기 지원1.13.24/1.13.25의
생성 wire bytes가 같음을 로컬 설치본으로 대조했다. 미지원 버전·metadata·빈/손상 응답,
누락·중복 repository/pointer·구조화 load error는 실패다. 오류명 substring으로
정상/실패를 정하지 않는다. source 근거는 Dagster 각 버전의
_grpc/__generated__/dagster_api_pb2.py, _grpc/server.py, _grpc/types.py다.

~~~bash
python -I -m kortravelcommon.grpc_health 12703 --check live
python -I -m kortravelcommon.grpc_health 12703 --check ready --repository __repository__
~~~

새 채널은 grpc.enable_http_proxy=0으로 grpc_proxy/http_proxy/https_proxy 등
proxy 환경을 무시한다. 논리 target을127.0.0.1로 적는 것만으로 proxy 우회를 막을 수는
없으므로 이 옵션을 제거하면 안 된다. 실제 로컬 회귀는 정상/손상 응답과 닫힌 target에서
proxy 연결0·조용한 종료를 확인한다. 기존 legacy API/CLI에는 이 새 격리 계약을 소급해
주장하지 않으며 소비자는 새 CLI로 명시 전환해야 한다.

새 CLI는 출력 없이 성공0/조회 실패1/잘못된 인자2로 끝난다. 기존
python -m kortravelcommon.dagster_health PORT의 인자·종료 코드는 보존한다.

새 함수의 timeout_seconds 기본4초, 허용 범위는0초 초과~4초 이하다.
두 RPC·optional import·응답 해석·channel 정리가 하나의 monotonic **논리 예산**을
공유한다. 첫 RPC가3초를 쓰면 다음 RPC에는 남은1초 이하만 준다. Python import,
protobuf/JSON 해석·channel close를 강제 선점하는 프로세스 hard wall 보장은 아니다.
초과 뒤 성공을 반환하지 않으며 Docker timeout에는 실제 bootstrap/cleanup 여유를
별도 실측한다. timeout을 맹목적으로 늘려 건강해 보이게 만들지 않는다.

health 조회에서 subprocess/reaper·run DB FAILED 기록·os.kill/PID1 종료·worker
/proc 스캔을 하지 않는다. False는 worker 사망 증거가 아니다. 복구는 기존
Common recovery 정책과 소비자 별도 경계에서 exact project/location/full origin/run
identity·container incarnation·활성 run·physical worker를 확인한다. worker 관측이
UNKNOWN이면 destructive action과 retry를 보류한다. 정상 cancel ACK·물리 종료·DB
terminal·partial facts/source lineage 보존을 분리하고 durable once/유한 retry를
유지한다. 이 변경은 새 운영 supervisor 서비스나 자동 lifecycle을 도입하지 않는다.

소비자 전이 순서는 Common exact pin/lock 설치 → effective HC가 이 CLI인지 확인 →
기존 health의 reaper/kill/run 변경 책임을 별도 복구 경계에 명시 → idle/active/지연/
load error/UNKNOWN에서 검증 → 두 리뷰·이미지·live다. Manager의 기존 override를
그대로 두고 Common만 설치한 상태를 무부작용 전환 완료로 세면 안 된다.

사용자는 초 단위 실행 시각 일치를 요구하지 않는다. health cadence와 시작 phase는
동일 workload의 probe wall/CPU·자식 준비 시간·동시 probe 수를 측정해 분산한다.
Docker interval/start-period/timeout 최적값을 모든 앱에 동일 수치로 고정하지 않는다.
예약 분산은 §13의 일일 횟수·간격·공식 발표 계약을 보존하고 run 동시성/신선도 보장과
분리한다.

[로컬 합성 CLI 측정](../reviews/adversarial/evidence/2026-10-16-grpc-health-local-measurements-final.json)은
x86 WSL/Python3.11 차가운 CLI 각3표본이며 부모 wall에는 interpreter와 관측 hook이
포함된다. peak RSS는 실행 후 /proc/self/status VmHWM이며 PSS가 아니다.
기존 Common ready 대비 새 ready의 CPU/RSS 절감은 입증하지 않았다. live는 정의 조회를
생략하는 다른 계약이므로 ready와의 차이를 동등 기능 절감률로 표현하지 않는다.
운영 ARM64·server CPU/DB·worker 실패/복구·실제 소비자 E2E 효과는 NOT_RUN이다.

## 15. 컨테이너 재시작 뒤 native 실행 정산

### 소유권과 적용 순서

순수 live health는 DB 쓰기·PID 종료·orphan 정산을 하지 않는다.
DefaultRunLauncher는 Dagster1.13.24에서 worker-health 검사를 지원하지 않으므로
run monitoring을 켜는 것만으로 사라진 STARTED worker를 즉시 찾지 못한다.
같은 gRPC 서버가 추적 중인 worker의 종료는 서버 자체 감독이 FAILURE로 기록하지만,
서버 교체로 그 목록이 사라지면 실행별 max-runtime까지 남을 수 있다.
앱 sync/load-job lease 수렴 센서는 native run 상태 변경과 다른 책임이다.

Weather·Geo처럼 동일한 공백을 가진 소비자는
kortravelcommon.dagster_recovery.native_incarnation_recovery_sensor를 명시적으로
등록할 수 있다. 이 센서는 **재시작 전 worker 유실의 native 실패 정산만** 수행한다.
현재 instance의 launcher가 정확히 DefaultRunLauncher인 경우만 진행한다.
Docker/K8s 등 외부 launcher·custom subclass·조회 불능은 정산 없이 보류한다.
code-server init 교체로 외부 worker의 사망을 추정하면 안 된다.
기본 STOPPED이고 실제 배포의 PID namespace·origin·clock 검증 후 별도로 활성화한다.
Common 코드/로컬 시험 완료를 소비자 배포·운영 복구 완료로 집계하지 않는다.

~~~python
from kortravelcommon.dagster_recovery import native_incarnation_recovery_sensor

native_recovery = native_incarnation_recovery_sensor(
    name="weather_native_incarnation_recovery",
    project="weather",
    location_name="weather_location",
    repository_origin_id=expected_repository_origin_id,
    grace_seconds=60,
)
~~~

expected_repository_origin_id는 소비자 workspace 정본의 실제
RemoteRepositoryOrigin.get_id()이며 hostname/port/SSL 기본값을 추측해 만들지 않는다.
동일 location 이름의 다른 호스트·origin을 승인하면 정상 worker를 오판할 수 있다.
예전 use_ssl=None과 명시 false의 차이도 실제 origin 일치 검증에 포함한다.
프로젝트·job tag가 있으면 origin과 모순되지 않아야 하며 무태그 이전 실행도
정확한 persisted origin과 Default launcher 연결 태그가 있을 때만 대상이다.
현재 launcher가 바뀌었어도 과거 외부 worker가 살아 있을 수 있으므로 run별
.dagster/grpc_info의 host/port 또는 socket/use_ssl도 실제 origin과 비교한다.
태그 누락·깨진 JSON·중복/알 수 없는 필드·타입/주소/SSL 모순은 보류한다.
SDK Default는 use_ssl=True만 태그에 남기므로 origin의 None/false는 태그 필드 부재와
대응하고 true는 명시 true와 대응한다. 임의 legacy JSON을 canonical로 정정하지 않는다.
증거 태그 없는 이전 실행은 자동 정산하지 않아 수동 확인이 필요할 수 있다.

### 정산 조건·메모리·clock

Linux64 Docker의 **private PID namespace** 안에서만 사용한다. host PID namespace를
공유하는 배포에 등록하지 않는다. init은 /proc/1이며 user-code child/reload 시각을
anchor로 쓰지 않는다. Docker 표식·PID namespace·같은 cgroup·boot ID·PID1 시작 ticks를
확인한다. 이 자료는 신뢰된 배포 전제의 교차 확인이며 컨테이너 보안 인증은 아니다.
PID1 시작 tick은 `/proc/1/task/1/stat`의 leader TID1을 두 번 읽어 같은 값인지 확인한다.
[Linux procfs의 task별 경로](https://docs.kernel.org/filesystems/proc.html)는
프로세스 PID와 task TID를 명시하므로 호출한 user-code 스레드나 reload child를 고르지 않는다.
반환 stat의 PID1 표기 검증도 유지한다. 경로 부재·손상·두 표본 불일치는 UNKNOWN이며
일반 `/proc/1/stat`로 fallback하지 않는다.

격리된 ARM64 QEMU 검증에서 일반 `/proc/1/stat`의 tick이 읽는 스레드별로 달랐고,
명시한 leader 경로는 세 호출에서 host PID1 시작 tick과 같았다. 일반 native Dockerexec
스레드 표본에서는 같은 차이가 나타나지 않았다. 이 반례는 에뮬레이션 경로 선택 결함의
근거이며 운영 native 장애나 새 센서의 실제 복구 성공을 뜻하지 않는다. 기존 실패·cursor는
보존하고 clock 경로 수정만으로 cursor를 자동 초기화하지 않는다.


**센서 활성화 전 소비자 필수 전제:** 해당 exact gRPC origin endpoint는 단일
code-server가 독점 소유해야 한다. 같은 origin을 공유하는 구/신 컨테이너의 동시
생존·rolling/blue-green overlap·여러 서버로 분기하는 proxy/LB routing은 지원하지 않는다.
private PID namespace와 origin 일치는 구 worker가 죽었다는 충분한 증거가 아니다.
소비자는 기존 배포 절차의 구 init/PID·시작 ticks와 worker 소멸, 구 cgroup의
비어 있음/소멸을 확인한 뒤 신 서버로 넘기는 serial 교체 증거를 활성화 근거에 포함한다.
PID/cgroup 경로가 재사용되면 경로 이름만으로 과거 프로세스 소멸을 판정하지 않는다.
이 배포 전제와 물리 소멸이 미확인/UNKNOWN이면 기본 STOPPED를 유지하고 활성화하지 않는다.
이 센서 자체는 구 namespace의 살아 있는 worker나 외부 routing을 조회·증명하지 않는다.
rolling overlap을 지원하려면 별도 worker 사망 증거가 필요하며 현재 API만으로
안전하다고 선언하지 않는다. 새 supervisor/health kill/전역 retry를 추가하는 요구가 아니다.

NTP adjtimex(modes=0) 읽기에서 정상 동기화·최대 오차1초 이내가 확인돼야 한다.
다른 ABI·권한/파일 부재·미동기화·leap 전환·불확실한 realtime/boottime 표본은
UNKNOWN으로 보류한다. 이 호출은 clock을 조정하지 않는다. 저장한 동일 boot의
epoch 기준에서1초 넘는 변화가 관측되면 기존 cursor를 보존하고 보류한다.
과거 NTP 변경 이력 전체를 증명하지는 못한다. clock 변경으로 보류된 cursor를
자동 초기화하지 않으며 운영자가 원인·기준을 확인한 뒤 재설정한다.

첫 tick은 init/clock 기준 기록만 한다. 이후 정확한 origin의 native STARTED이고
start_time이 검증된 init 시작의 보수적 하한보다 grace(최소60초)만큼 이른 경우만
정산한다. 현재 incarnation의 정상 장기 run·같은 컨테이너 reload·STARTING·QUEUED·
CANCELING·start_time 누락·경계 동등 값은 대상이 아니다. 기본100개 page·최대5page와
tick당 협력적5초 예산으로 메모리/조회량을 제한한다. DB 호출 자체의 hard timeout은
아니므로 소비자 metadata DB/RPC 예산이 별도로 필요하다.

완료 page cursor를 센서 저장소에 유지하고 완주하면 head부터 재확인한다.
중간 조회/쓰기 실패는 cursor 성공 반환 없이 실패하므로 같은 후보를 다시 확인한다.
incarnation 전체를 영구 완료 표시하여 늦게 나타난 이전 실행을 누락하지 않는다.
쓰기 직전 init/clock·실행 status/start_time/origin을 재조회하며 이미 terminal이면
아무것도 쓰지 않는다. 공식 report_run_failed와 구조화 RUN_WORKER_RESTART 사유를 쓴다.
이는 원자 CAS가 아니다. 최종 재조회와 쓰기 사이 외부 수동 terminal 기록 경쟁은
기존 run-monitoring과 같은 잔여 한계이며 새 outbox/직접 runs-table UPDATE로 숨기지 않는다.

### 실패 재시도와 서버 복구는 별도다

이 센서는 RunRequest를 만들지 않는다. 실패 뒤 재시도는 기존
infrastructure_retry_sensor의 exact project/location/job·멱등 선언·허용 사유·상한·
이미 발급된 child 검사를 재사용한다. native retry가 활성화됐으면 기존 위임 계약을
유지한다. Weather는 retry tag만 설정한 상태와 실제 센서 등록/instance 활성화를
구분해야 하고, Geo의 backup_verify 이외 비멱등 job을 자동 retry로 넓히지 않는다.

이 센서도 code location이 로드되지 않으면 실행되지 않는다. SERVING proxy 뒤의
hung child를 재시작시키거나 PID1 kill의 모든 효과를 대체하지 않는다.
따라서 Manager의 기존 health reaper/PID 종료를 제거하는 변경은 이 센서 추가만으로
완전 동등 복구가 되었다고 판단하지 않는다. 서버 복구의 운영 소유자/수동 대응을
별도로 정하고 실제 run worker 유실·정상 장기 실행·동시 타 location 보존을 검증한다.

Common의 순수 fixture·로컬 Dagster native 이벤트 검증은 소비자 SDK/이미지 채택,
실제 컨테이너 재시작·첫 tick·큐 해소·수집 신선도·CPU/RSS·live E2E의 대체가 아니다.
이 가이드 추가 시점의 운영·소비자 검증은 NOT_RUN이다.

### Common36 격리 실측 기록의 범위

[실제 r2 역사 부분 검증](../reviews/adversarial/2026-10-16-common36-historical-partial-closure.md)은
ARM64/QEMU lab의 fault1·공식 부모 실패·단일 child SUCCESS와 사후 센서별2tick/중복0를
확인했다. control 두 개가 이미 성공한 뒤의 tick이므로 정상 control을 계속 실행한 채
두 tick을 관측하는 원 전체 LIVE gate는 HOLD다. 원 controller 실패와 r3의
timeout/background OOM·별도 정상 정리는 보존한다. 이 기록은 위 활성화 조건을
완화하지 않으며 native ARM 운영 복구·성능/소비자 live 완료의 근거로 확대하지 않는다.

후속 [native 실제 종결](../reviews/adversarial/2026-10-16-common36-native-live-closure.md)은
별도 WSL amd64/SDK1.13.24에서 두 control을 STARTED로 유지한 postchild2tick/센서와
단일 child·정상 종료를 실제 검증했다. ARM 원 부분 기록·실패는 그대로 보존하며
이 관측은 활성화 전제·소비자 live/운영 성능 gate를 완화하지 않는다.

## 16. 여러 job의 실패 scan 공유

동일 project/location에서 여러 멱등 job의 인프라 재시도가 필요하면
[infrastructure_retry_sensor_for_jobs 적용 안내](dagster-multi-job-retry.md)를 따른다.
기존 단일 factory와 같은 엄격 판정을 사용하며 소비자 native 설정을 켜지 않는다.
Common34의 incarnation FAILED 정산과 재시도 요청 발급은 서로 다른 책임이다.

## 17. 이미지 빌드의 stdlib bytecode 준비

반복하는 짧은 Python/health 프로세스는 site-packages bytecode만 준비돼 있어도
stdlib 소스의 bytecode가 없으면 이를 다시 컴파일할 수 있다.
동일 interpreter/module 집합의 별도 prefix 진단은 이 비용의 존재를 보여 줬지만,
CLI 도입만으로 전체 서비스 CPU·메모리·health wall이 개선됐다고 판정하지 않는다.

새 core-only CLI는 **이미지 빌드 때 명시적으로 한 번만** 실행한다.
Common을 설치한 뒤, 최종 이미지에서 쓰는 바로 그 interpreter로 다음 명령을 실행한다.
빌드 계정에는 stdlib 내부 cache 경로의 쓰기 권한이 필요하다.

    RUN python -m kortravelcommon.build_bytecode --stdlib

가상환경을 쓰면 최종 interpreter의 절대 경로를 사용한다. 다른 stage/interpreter가
만든 pyc를 복사해 호환된다고 가정하지 않는다. 후속 layer에서 stdlib를 다시
복사하거나 bytecode를 제거하면 준비 효과가 사라질 수 있다. 설치된 Python 버전과
source bytes에 맞는 checked-hash pyc·최종 이미지 내 보존 여부를 확인한다.

### 범위와 실패

sysconfig의 stdlib만 대상으로 compileall worker1·optimize0·checked-hash로 준비한다.
기존 timestamp cache도 checked-hash로 다시 만든다. site-packages/dist-packages 및
test/tests/idle_test 하위는 제외한다. 소비자 패키지의 bytecode 준비는 별도 빌드 책임이며
UV_COMPILE_BYTECODE만으로 이 stdlib 경계가 해결됐다고 간주하지 않는다.

임의 source path 인자는 제공하지 않는다. 디렉터리 symlink는 따라가지 않고 외부 source
symlink는 생략한다. 외부로 향하는 cache 디렉터리·기존 pyc symlink·별도 pycache prefix는
실패로 거절한다. 조용히 읽지 못한 하위 디렉터리·빈 대상·문법/권한 실패도 exit1이다.
실패 전에 일부 정상 pyc가 생길 수 있으며 rollback/삭제를 하지 않는다. 실패한 빌드
layer를 성공으로 승격하거나 자동 재시도하지 말고 원인을 확인한다.

이 CLI는 신뢰하는 단일 writer 이미지 빌드용이다. 동시에 source·symlink를 바꾸는
공격자에 대한 파일 시스템 sandbox/원자 snapshot을 제공하지 않는다. source를 고정하고
다른 빌드 작업과 동시에 이 디렉터리를 수정하지 않는다.

### 런타임과 효과 검증

entrypoint/health 함수에서 자동 실행하지 않는다. PYTHONDONTWRITEBYTECODE와 -I 등
기존 런타임 환경·격리 옵션을 변경하지 않는다. 해당 설정은 유효한 pyc 읽기를 막는
기능이 아니며 이 CLI의 명시적 컴파일은 별도다. CLI는 provider·DB·Dagster 본체·앱을
import하거나 실행하지 않으며 source 파일·설정·수집 시각·재시도 정책을 바꾸지 않는다.

소비자는 최종 source/image/interpreter·설치 package·Config/Env를 결박하고 기존 health
argv 그대로 cold import/전체 health의 wall·self CPU·RSS와 pyc 유효성·소스 해시를 비교한다.
cold prime과 warm 반복, 동일 bytecode가 다음 layer에도 남는지, 계측 자체 부하와 실제
동시 workload를 나눠 기록한다. 새 이미지 빌드·배포와 전후 CPU 감소는 이 Common
소스/fixture/wheel 검증으로 대체하지 않는다. 미실행 소비자 gate는 NOT_RUN으로 둔다.

## 18. daemon 전용 PostgreSQL 연결 재사용

`kor-travel-common[daemon-pool]`의 `kor-travel-dagster-daemon`은 명시적 opt-in이다.
기존 `dagster-daemon` 명령과 다른 서비스의 storage 기본값은 바꾸지 않는다.
지원 설치 조합은 Dagster1.13.24 / dagster-postgres0.29.24 / SQLAlchemy2.0.54다.
소비자는 원 requirements의 나머지 버전·hash를 유지하고 이 조합을 별도 검증한다.
버전이 다르면 이 진입점은 거절한다.

### 소비자 설정과 같은 프로세스 호출

이 진입점은 원 `dagster-daemon` console entry point를 배포판 metadata에서 확인하고
동일 Python 프로세스에서 호출한다. SDK의 instance/engine 필드·controller를 교체하거나
SDK 함수를 monkeypatch하지 않는다. 별도 preflight 프로세스에서 instance를 최적화한 뒤
exec하는 방식은 새 daemon instance에 전달되지 않으므로 사용하지 않는다.

지원하는 원 YAML storage 형태는 다음과 같다. URL 값은 문서·로그에 넣지 않는다.

```yaml
storage:
  postgres:
    postgres_url:
      env: KOR_TRAVEL_DAGSTER_SHARED_PG_URL
    should_autocreate_tables: false
```

소비자는 daemon에만 `KOR_TRAVEL_DAGSTER_DAEMON_POSTGRES_URL`을 제공한다.
값은 원 shared URL과 정확히 같아야 한다. 기존 plugin 쿼리, 다른 driver,
literal URL/custom instance 설정은 거절한다. 실제 명령은 기존 argv에서 실행 파일만
`kor-travel-dagster-daemon`으로 바꾼다. `run`의 원 옵션과 SDK 신호 처리는 유지한다.
최상위·run help/version 및 기타 기존 명령은 원 CLI에 위임하며 pool을 켜지 않는다.
숨김 --instance-ref(분리값/등호값)는 run의 YAML 검증을 우회하므로 이 profile에서 거절한다.

wrapper는 자기 프로세스의 shared URL에만 SQLAlchemy 공식 plugin 이름을 추가하고
종료 시 원 환경을 복원한다. 다른 컨테이너·공유 YAML·운영 자격증명은 수정하지 않는다.
이 YAML의 InstanceRef는 해석 전 `{env: ...}`를 보존한다. DefaultRunLauncher로
외부 CS에 전달되면 CS의 원 환경에서 URL을 해석하므로 plugin이 설치되지 않은 CS에
daemon의 해석된 URL을 보내지 않는다. literal/custom storage와 local code-server
자식 환경 전달은 이 지원 계약에 포함하지 않는다. 소비자는 외부 workspace 경로와
실제 ref 직렬화를 검증한 뒤 활성화한다.

### 풀 상한·timeout·정리

plugin은 `postgresql+psycopg2`의 명시적 NullPool 생성에만 적용한다.
활성화 뒤 최초 run/event/schedule 세 primary engine에 각각 pool_size2/max_overflow2,
pool_timeout1초/pool_recycle3600초를 쓴다. primary pooled 연결 상한12, 유휴 보관 상한6이다.
이는 pooled primary 세 engine의 합계이며 프로세스 전체·PG 전체 접속이나 worker 수의 상한은 아니다.
공식 DefaultRunLauncher의 gRPC start_run은 같은 프로세스에서 InstanceRef를 해석해 임시
Instance를 만든다. 네 번째 이후 engine은 원 NullPool·원 연결 수명 그대로 두며 primary
registry에 넣지 않는다. 임시 Instance의 연결은 원 SDK가 사용 후 닫는다.
primary 생성 슬롯은 engine_created 이전에 잠금으로 세 개만 예약한다. 생성 실패의 슬롯도
해당 활성화 종료까지 유지하므로 추가 QueuePool로 무제한 대체하지 않는다.
이미 pool 옵션이 있으면 primary/임시 구분 없이 거절한다.

원 AUTOCOMMIT·URL connect timeout/options·statement_timeout·lock_timeout을
그대로 둔다. 새 SET·schema 존재 캐시는 추가하지 않는다.
idle 연결이 끊긴 뒤 첫 tick이 실패하는 신규 회귀를 막기 위해 SQLAlchemy 공식
pool_pre_ping=True로 checkout 시 검증·재연결한다. 내부 ping SQL 비용은 기존 workload
SQL count와 별도로 측정한다. 실행 중 연결 단절/transaction 재시도 범위는 바꾸지 않는다.
QueuePool checkout TimeoutError도 SDK 기존 retry/backoff 대상이다.
따라서 전체 대기는1초로 끝나지 않으며 최대6회 연결 시도와 기존 backoff를 포함한다.
중첩 checkout·pool 포화·heartbeat/tick 지연을 별도로 검증해야 한다.

QueuePool의 public connect()를 좁게 확장해 super().connect() 이전에 PID scope를 검사한다.
SQLAlchemy의 pre_ping은 checkout 이벤트보다 먼저 실행되므로 이벤트 검사만으로는
부모 연결의 ping/close를 막지 못한다. 이후 connect record/checkout PID 검사도 유지한다.
fork된 자식은 부모 pool의
활성 범위를 사용할 수 없으며 새 프로세스/새 instance에서 원 설정을 해석해야 한다.
부모 socket을 강제로 닫거나 같은 raw connection을 여러 thread에서 공유하지 않는다.
최대 세 primary engine의 strong registry는 수명 동안만 유지하고 종료 finally에서 현재 pool을
dispose한다. dispose/recreate는 pool 생성 PID를 검사하고 대여 중인 세대를 거절한다.
recreate는 유휴 연결도 남아 있으면 거절한다. 따라서 close=False로 살아 있는 이전 세대를
떼어놓아 연결 상한·종료 집계를 우회할 수 없다. 기본 close=True는 유휴 연결을 닫은 뒤
빈 pool만 재생성한다. 활성화마다 별도 scope identity를 부여하고 connect에서 검사하여
같은 PID의 다음 활성화에서도 이전 engine/pool을 다시 사용하지 못한다.
connect/dispose/recreate는 같은 pool별 잠금으로 직렬화하여 대여 검사와 세대 교체 사이의
thread 경합을 막는다. 반환은 이 잠금을 쓰지 않아 포화 중 대기 checkout을 깨울 수 있다.
재생성이 끝난 이전 pool은 퇴역 상태로 고정하므로 이미 옛 참조를 받은 thread도 다시
대여할 수 없다. 재생성된 pool은 원 활성화 identity를 그대로 계승하므로 다음 활성화에서
옛 engine을 dispose해도 새 수명의 미등록 engine으로 회생하지 않는다. fork PID 검사는 상속된 전역·pool 잠금에 들어가기 전에 수행한다.
자식 finally도 부모 잠금이나 연결 I/O 없이 실패한다.
SDK가 도중에 engine.dispose하여 빈 pool을 재생성했어도 현재 pool을 종료 시 닫는다.
원 SDK instance.dispose만으로는 schedule engine 정리가 보장되지 않는다.

원 CLI 종료를 먼저 마친 뒤 연결 반환 여부를 확인한다. 미반환/정리 오류가 있으면
성공으로 간주하지 않는다. 기존 nonzero SystemExit/예외는 덮지 않고 정리 미완료를
고정 메시지로 별도 기록한다. 원 정상 종료 중 정리 실패는 오류로 끝난다.
자동 worker 취소·강제 kill·schema 변경·원 설정 복구 재시도는 하지 않는다.

### 검증 범위

가짜 DBAPI 연결 재사용·상한/포화·옵션 보존·thread/PID·dispose·CLI 위임·환경 복원,
wheel entry point 및 source-only InstanceRef 검증은 라이브러리 회귀 대상이다.
SDK/실제 격리 PG에서는 원 NullPool과 같은 workload·결과·timeout/SQL 수를 비교하고
공식 CLI SIGTERM·primary 세 engine 정리·원 CS ref를 확인한다.
실제 DefaultRunLauncher/start_run의 임시 from_ref 경로도 RPC 대역과 격리 PG에서 실행해,
primary 세 QueuePool 보존·임시 세 NullPool 반복 생성/성공·오류 정리를 확인한다.
단순 ref 직렬화나 cap0 CLI heartbeat만으로 job launch 성공을 검증했다고 하지 않는다.
운영 DB로 시험하지 않는다.

소비자 실제 CPU/RSS·PG 접속 수·pool 대기·tick 지연·수집 신선도·정상 종료는 별도다.
격리 반복 읽기에서 연결 수가 줄어도 운영 전체 CPU 감소율이나 공유 PG CPU 중 daemon
기여도를 뜻하지 않는다. 다른 프로세스의 연결·schema reflection SQL 자체도 이 변경으로
자동 제거되지 않는다. 계측 후 작은 소비자 opt-in부터 적용한다.


### native webserver와 같은 wheel에 포함할 때

daemon-pool과 dagster-webserver extra는 합집합으로 설치할 수 있다. daemon extra의
검증 profile(Dagster1.13.24/PG0.29.24/SQLAlchemy2.0.54)이 전체 resolve에도 적용된다.
두 console entrypoint와 SQLAlchemy plugin이 같은 whole wheel에 들어가며,
webserver는 [native 멱등 제출 가이드](dagster-idempotent-launch.md)의 별도 process에서
실행한다. daemon 전용 DSN/plugin을 webserver에 활성화하지 않는다. 이 소스 정합은
공유 host 배포·consumer pin·실수집·CPU/RSS 수용 완료를 뜻하지 않는다.

## 19. 회수 sensor의 tick 예산과 정체 경보

weather `weather_sync_recovery`·transport `transport_worker_recovery`처럼 `reconciliation_sensor`
위에 만든 회수 sensor는 tick 예산·cursor·정체 경보가 없어, 회수 콜백이 계속 실패해도 수집
정체가 몇 시간 동안 드러나지 않았다. 다음 인자는 모두 opt-in이며 생략하면 기존 동작과 같다.
의미의 정본은 `kortravelcommon.dagster` 모듈 docstring이다.

```python
from kortravelcommon.dagster import reconciliation_sensor

def reconcile(context, remaining):
    # remaining()이 줄면 다음 page를 시작하지 않는다. statement/lock timeout은 앱이 둔다.
    ...

def alert(context, clock):
    # clock.key·first_failed_at·last_failure(형식 이름과 SQLSTATE)만 경보에 싣는다.
    ...

recovery = reconciliation_sensor(
    name="worker_recovery", reconcile=reconcile, required_resource_keys={"repository"},
    budget_seconds=40, on_stall=alert,
)
```

- `budget_seconds`를 주면 콜백은 `(context, remaining)` 두 인자를 받는다. 대기는 같은 예산에서
  끊기며 sensor 전용 1-slot 때문에 끝나지 않은 이전 콜백과 겹쳐 실행하지 않는다(다음 tick은
  `DeadlineExceeded`). 끊긴 thread는 강제 종료되지 않으므로 DB statement/lock timeout을 예산보다
  짧게 둔다. Dagster의 sensor 평가 상한(기본 60초)보다 작게 잡는다.
- `on_stall`을 주면 콜백 예외는 tick 실패 대신 `context.log`의 오류 로그와 정체 시계로 남는다.
  첫 실패 뒤 `stall_after_seconds`(기본 900)에 경보하고 `realert_after_seconds`(기본 3600)마다
  다시 부른다. 경보 콜백이 실패하면 다음 tick에 재시도한다. 시계는 sensor cursor(`stall:` 접두
  JSON)에 저장하므로 이 모드에서는 sensor cursor를 factory가 소유한다. keyset 위치는 소비자
  DB에 둔다(콜백에서 `context.update_cursor`를 쓰지 않는다). 경보 전송 채널·수신자는 소비자 소유다.
  cursor·경보에는 예외 원문이 없지만 `context.log` traceback에는 기존 tick 실패처럼 남는다.
- 콜백이 멈추는 정체는 `budget_seconds`를 함께 줘야 기록된다. 예산이 없으면 Dagster의 sensor
  평가 timeout이 tick을 먼저 끊어 시계가 시작되지 않는다. 예산과 `on_stall` 소요 시간의 합도
  평가 상한 안에 둔다. 넘으면 경보가 나갔어도 경보 시각이 저장되지 않아 다음 tick에 다시 경보한다.
- 정체 시계는 Dagster와 무관한 `kortravelcommon.stall`(`StallClock`·`observe_failure`·`due_alert`·
  `mark_alerted`·`to_dict`/`from_dict`)로 다른 저장소(앱 DB 등)에도 쓸 수 있다.
- `kortravelcommon.pg_errors.pg_error_info(exc)`는 SQLAlchemy·asyncpg·psycopg 3·psycopg2 예외
  연쇄에서 SQLSTATE·제약 이름·primary message만 꺼낸다(driver import 없음). 어떤 SQLSTATE를
  재시도·경보할지는 소비자의 도메인 SQL과 함께 소비자가 정한다.
- `call_with_deadline(..., slots=threading.BoundedSemaphore(n))`는 프로세스 공용 4-slot 대신 호출자
  전용 slot을 같은 의미로 쓴다.

DB schema·트랜잭션·도메인 SQL과 경보 정책 값은 계속 소비자 소유다. 이 절은 common 단위
시험만 근거로 하며 소비자 채택·실제 경보 도달·운영 정체 감지는 각 소비자 PR에서 확인한다.
