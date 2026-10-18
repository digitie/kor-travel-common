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

공식 upstream 구현은 Dagster 태그 1.13.24 및 1.13.25의
[GraphQL schema](https://github.com/dagster-io/dagster/blob/1.13.25/python_modules/dagster-graphql/dagster_graphql/schema/__init__.py),
[native run lifecycle](https://github.com/dagster-io/dagster/blob/1.13.25/python_modules/dagster-graphql/dagster_graphql/implementation/execution/run_lifecycle.py),
[webserver](https://github.com/dagster-io/dagster/blob/1.13.25/python_modules/dagster-webserver/dagster_webserver/webserver.py)를
설치된 두 버전 원문과 대조했다.
