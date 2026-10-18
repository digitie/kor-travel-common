# native Dagster의 영속 요청 식별자

## 범위와 상태

Transport·Weather 주소 수동 갱신에서 응답 유실 뒤 같은 요청을 다시 보내도 native run 하나를
사용하기 위한 opt-in adapter다. 기존 query/subscription/mutation과 기본 Common import는 유지한다.
소비자 BFF·UI·pin·배포는 각 저장소가 소유한다. 독립 리뷰·CI·운영 수용은 별도로 확인하며
이 가이드를 운영 완료나 CPU 절감 증거로 사용하지 않는다. Daemon은 이 모듈이 시작하지 않는다.
기존 UNKNOWN 반례와 Transport86 r3 원문 판정은 변경하지 않는다.

## 실행과 지원 버전

Common의 선택 extra인 dagster-webserver를 설치한 native webserver 환경에서 실행한다.

    python -m kortravelcommon.dagster_webserver -h 127.0.0.1 -p 3000 -w workspace.yaml

upstream CLI 인자를 그대로 전달하고 같은 프로세스의 native app에 schema subclass만 연결한다.
SDK/vendor 파일·CLI 본문을 복사하거나 별도 앱 서버·프로세스·DB/schema를 추가하지 않는다.
Dagster·dagster-graphql·dagster-webserver가 모두 1.13.24 또는 모두 1.13.25여야 한다.
기본 import에는 SDK가 필요 없고 기존 native CLI를 선택하면 새 field가 생기지 않는다.

## GraphQL 계약

추가 field는 다음과 같다. 기존 LaunchRunResult의 오류 유형들을 유지하고 성공 유형만 확장한다.

    launchIdempotentRun(requestId: String!, executionParams: ExecutionParams!)
        -> IdempotentLaunchRunResult!

성공 IdempotentLaunchRunSuccess는 native Run인 run과 Boolean replayed를 제공한다.
replayed=false는 이 호출이 run을 만들었다는 뜻이며 수집 성공을 뜻하지 않는다.
replayed=true는 기존 run의 현재 상태를 반환했다는 뜻이다. FAILURE/CANCELED도 성공한
수집으로 표시하지 말고 native run 상태와 링크를 사용자에게 전달해야 한다.

- requestId는 하이픈이 있는 UUID 문자열이다. 대문자는 소문자로 정규화하며 UUIDv5의
  입력은 location/repository/job과 정규 UUID다. 다른 job의 같은 요청 UUID는 별도 run이다.
- UUID namespace와 canonical 입력은 영속 계약이므로 배포 뒤 임의 변경하지 않는다.
- 같은 selector/UUID의 config·사용자 tags가 다르면 ConflictingExecutionParamsError다.
  config는 native parser로 정규화한 JSON이며 key/tag 순서는 identity에 영향을 주지 않는다.
- native job launch permission은 기존 run 조회에도 먼저 적용한다. native config 검증과
  실행 계획/원천은 create_valid_pipeline_run을 그대로 호출한다. 새 field는 인증 경계를
  따로 만들지 않으며 소비자는 기존 BFF 인증·CSRF·selector allowlist를 유지해야 한다.
- 전체 job 실행만 지원한다. preset, stepKeys(빈 배열 포함), solid/asset/check 선택,
  parent/root lineage와 default 외 mode는 명시 거절한다.
- 중복 tag key, 내부 kortravel/idempotent-request-sha256과 dagster/ 예약 태그는 거절한다.
  예외 dagster/code_location은 selector.repositoryLocationName과 정확히 같을 때만 허용한다.
  이 태그는 소비자의 previous/active 조회 범위를 보존한다.
- 지원하지 않는 형태나 충돌 오류에는 입력 config/tag 값을 출력하지 않는다.
  RPC/config/DB/submit 오류는 native 오류 경로로 전달하며 무차별 성공으로 바꾸지 않는다.

## 영속성과 재개 경계

native run ID 유일 키가 늦은 생성·응답 유실·webserver 프로세스 재시작을 넘는 기준이다.
현재 메모리의 TTL이나 영구 guard에 의존하지 않는다. native NOT_STARTED만 같은 run ID로
submit_run을 재개한다. QUEUED/STARTING/STARTED/CANCELING/종료 상태는 새 run/제출 없이
그대로 반환한다. native 행을 삭제하면 이 보존 조건도 사라지므로 소비자는 이를
영구적인 외부 업무 exactly-once 보장으로 확대해서는 안 된다.

추가 field는 공식 QueuedRunCoordinator만 지원한다. 즉시 launcher를 실행하는 coordinator나
subclass/custom coordinator는 명시 거절한다. 동시 native unique 충돌만 재조회하며 다른
예외는 유지한다. 같은 run ID에 대한 실제 enqueue/dispatch/worker 수명은 native queue
계약을 따른다. 이 adapter가 별도 semaphore나 새로운 coordinator/worker를 만들지 않는다.

## 제출 경합 후속 수정

초기 제품23e4775의 native unique 검증은 run 한 개만 확인했다. 독립 리뷰가
NOT_STARTED 제출 context A 지연→B enqueue/STARTED→A 재enqueue로 상태가 QUEUED로
퇴행하는 P1을 발견했고, 작성자도 원 반례 1 FAIL을 재현했다. 초기 두 리뷰 원문과
첫 제품은 그대로 보존한다. run 한 개라는 사실을 worker 중복 방지 완료로 확대하지 않는다.

제품2704830은 run별 cross-process critical section 안에서 다시 읽은 상태와 submit을
직렬화한다. 같은 요청의 제출 중에는 native PythonError 경로의 SubmissionBusyError를
반환한다. 소비자는 같은 UUID로 재시도하고 이를 새 요청 성공으로 표시하지 않는다.

- SQLite는 POSIX 로컬 파일 저장소를 지원한다. native DB 옆 0700 디렉터리의 UUID별0600
  일반 파일에 flock을 건다. lock 파일은 빈 metadata이며 해제 뒤에도 재사용한다.
  활성 중 unlink하면 inode가 갈라질 수 있어 자동 삭제하지 않는다. offline 정리는
  인스턴스의 모든 webserver가 멈춘 상태에서만 운영자가 판단한다.
- PostgreSQL은 native PostgresRunStorage의 같은 URL과 검증한 .29.24/.29.25 조합을 사용한다.
  token provider/custom 저장소는 지원하지 않는다. 별도 NullPool connection의 session
  advisory try-lock을 사용하며 기존 native engine의 checkout을 점유하지 않는다.
  URL의 driver/options는 보존한다. 연결은 connect_timeout=5이며 lock busy는 대기하지 않는다.
- 프로세스/connection 종료가 OS/session lock을 해제한다. TTL이나 영구 guard를 사용하지 않는다.
  해제 오류 때도 connection을 닫고, 원래 제출 오류가 있으면 그 오류를 보존한다.
  네트워크 단절의 server session 감지 시간은 PostgreSQL의 기존 연결 계약을 따른다.
- 동일 native run을 이 field 밖의 임의 Python 코드로 직접 제출하는 writer까지 잠그지는 않는다.
  SQLite의 서로 다른 호스트/NFS 잠금이나 Windows native 실행은 이번 지원 범위가 아니다.

## 작성자 검증과 남은 gate

- .24와 .25 각각 실제 schema 41+1 fields, 기존 field return type/CLI 인자, 권한·설정 오류,
  SQLite 유일 생성·동시 생성·늦은 첫 생성·응답 유실·내용 충돌을 포함해 41 PASS.
- 별도 Python 프로세스에서 같은 owned SQLite를 재개해 NOT_STARTED→QUEUED와 run 한 개를
  확인했다. job 정의는 fixture이며 실제 job/provider/daemon/외부 DB는 실행하지 않았다.
  RPC 대신 소유 in-memory 정의와 실행 계획을 주입했고 native create/submit/저장은 실행했다.
- 첫 집중 실행은 fixture의 GrapheneRun 속성을 잘못 참조해 2 FAIL/4 PASS였고 runId로
  고쳐 재실행했다. 공유 .24 환경에는 pytest가 없어 소유 별도 .24/.25 venv로 검증했다.
  이 준비 오류를 제품 red→green 반례로 세지 않는다.
- locked 전체 패키지 553 PASS(130.22초)는 추가 프로세스/응답 회귀 두 개를 넣기 전 collection이다.
  두 추가 회귀는 위 41 PASS에 포함한다. 최종 전체/CI는 별도 기록한다.
- wheel 설치 후 두 SDK에서 모듈 SHA와 42 fields를 재확인했다.
  이전 lock에 있던 package version/source 변경은 없고 webserver 선택 extra 의존 18개를 추가했다.
- 작성자는 독립 리뷰어가 아니다. 두 독립 FULL 리뷰, 정확 HEAD CI와 소비자 연결/UI 검증은
  후속이다. 운영·실 provider·SSH·Docker·Daemon 조작은 NOT_RUN이다.

### 제출 경합 수정 뒤 검증

- 제품2704830의 실제 SQLite 집중 회귀: .24 44 PASS(25.99초), .25 44 PASS(24.08초).
  원 반례와 같은 사용자 경합에서 둘째 제출을 busy로 거절한 뒤 첫 enqueue→STARTED→replay가
  ENQUEUED/START만 남고 run 한 개를 유지한다. 별도 프로세스 crash 뒤 잠금 재획득도 포함한다.
- root가 명시 허용한 신규 전용 owned PostgreSQL DB에서만 native create/submit/store를 실행했다.
  .24 45 PASS(34.80초), .25 45 PASS(32.19초)에 서로 다른4 run/pool_size1 동시 제출과
  unlock 오류 시 원예외 보존/session 해제3개를 각 버전에서 추가 PASS했다.
  기존 애플리케이션 DB·운영 DB·job/daemon/provider는 접근하거나 실행하지 않았다.
- 신규 PG fixture 초기화는 SQLAlchemy2.1의 bare PostgreSQL URL이 설치되지 않은 psycopg3를
  선택해 1 ERROR/1 PASS였다. 소유 fixture에 명시 psycopg2 URL을 사용해 재실행했다.
  native 환경의 URL/driver 호환성은 소비자 설치에서 따로 확인한다. 전체 SQLAlchemy pin은 바꾸지 않았다.
- locked 최종 패키지 558 PASS(130.17초), Ruff 전체 PASS. 최종 artifact 설치와 문서 검증은
  후속 journal의 정확 수치를 따른다. 이전553/555는 각 이전 collection의 이력이다.
- tools 첫 실행은 MDX Node 의존성 미설치로 38 FAIL/3 ERROR/1 SKIP였고, owned WT의
  npm ci --ignore-scripts 뒤 337 실행(336 PASS/1 SKIP,73.285초)했다. 기존 실패 로그도 보존한다.
- 독립 리뷰는 root가 작성자를 제외한 두 명에게 별도 배정한다. 이 작성자 검증은 그 수를
  대체하지 않으며 소비자 UI·운영 완료나 CPU/메모리 절감 판정이 아니다.

공식 upstream 구현은 Dagster 태그 1.13.24 및 1.13.25의
[GraphQL schema](https://github.com/dagster-io/dagster/blob/1.13.25/python_modules/dagster-graphql/dagster_graphql/schema/__init__.py),
[native run lifecycle](https://github.com/dagster-io/dagster/blob/1.13.25/python_modules/dagster-graphql/dagster_graphql/implementation/execution/run_lifecycle.py),
[webserver](https://github.com/dagster-io/dagster/blob/1.13.25/python_modules/dagster-webserver/dagster_webserver/webserver.py)를
설치된 두 버전 원문과 대조했다.


### 2704830 artifact·문서 확인(후속 보강 전)

제품2704830의 새 wheel은 57,664 bytes이며 SHA256은
ec557447713516047e111d9d9bd1177af1e6dab995c9de78854195505d15e5da다.
패키지 Python14개를 Git source와 비교하고 RECORD20행을 검증했다.
별도 .24/.25 venv에 no-deps 설치한 뒤 source SHA와 schema42 fields가 일치했다.
기존 default core import의 lazy SDK 경계도 집중 회귀에 포함된다.

문서 local links765/2967 오류0·plan109 오류0를 확인했다. 이 수치는 검증 당시 문서 tree이며
후속 기록에 따라 target 수만 늘 수 있다. 독립 post-fix 판정과 정확 최종 HEAD CI는 root가
별도 정산한다. CI 진행 중인 job을 성공으로 포함하지 않는다.


## PostgreSQL 잠금 session 유실 후속 수정

2704830의 별도 session lock만으로는 충분하지 않았다. 독립 리뷰가 lock backend만 끊긴 뒤
첫 coordinator 호출이 늦게 계속되어 다른 요청의 STARTED를 QUEUED로 되돌리는 P1을 발견했다.
작성자도 같은 실제 owned PG 시나리오에서 원270의 1 FAIL을 보존했다.

제품a68d049는 opt-in instance의 run-storage connect factory를 얇은 ContextVar adapter로
연결한다. 현재 제출의 native run 조회/쓰기만 advisory를 가진 같은 SQLAlchemy connection을
사용한다. closed/invalidated면 재연결을 거절하고, 다른 thread/context와 기존 mutation은
원래 factory를 사용한다. SDK 구현/SQL 상태 전이 본문은 복사하지 않는다.
context 복원과 connection 종료는 오류에도 수행한다.

실제 native eventlog와 run storage는 원래 원자적 한 commit이 아니다. 잠금 유실 뒤 첫
요청이 실패하더라도 eventlog에 enqueue/실패 시도 이벤트가 먼저 남을 수 있다.
이를 실제 QUEUED/FAILURE 상태나 수집 완료로 해석하지 않는다. authoritative native run
상태를 확인하며 이 요청은 성공으로 반환하지 않는다. 같은 UUID의 다음 요청은 유지된
실제 STARTED/종료 상태를 replay한다. 이 한계를 감추려고 원 native eventlog를 수정하지 않는다.

- .24와 .25 각각 SQLite 집중48 PASS(28.97초/28.09초), owned PG 전체53 PASS(29.05초/37.33초).
  PG lock backend 하나를 종료한 뒤 실제 run STARTED 유지·행1개·첫 요청 오류·그 actor의
  새 PG 연결0·same-ID replay를 확인했다. 실제 worker/daemon은 실행하지 않았다.
- 최종 locked 전체562 PASS(131.43초)와 Ruff 전체 PASS다. 앞선553/555/558은 당시 후보 이력이다.
- native CLI의 정식 console alias kor-travel-dagster-webserver를 추가했다.
  python -m 진입도 유지하며 둘 다 같은 main을 호출한다. 두 설치 wheel의 실제 --help를 확인했다.
- a68 wheel은 58,401B, SHA256
  81888c56e669e7b0d908c7875bb3e31f337ee529813e4c11e1e7f4179180ced3이다.
  Python14개 Git exact·RECORD21행·정식 entrypoint를 확인했고 두SDK no-deps 설치 뒤
  모듈 source SHA와 schema42 fields가 일치했다. 문서만 바꾼 후속 HEAD는 이 제품을 유지한다.
- scanner가 ContextVar 복원값의 token 변수명을 오탐해 previous_binding으로 명료화했다.
  검사 예외/ignore는 추가하지 않았다. 최종 post-fix 두 독립 판정/CI·소비자 gate는 root가 별도 정산한다.
