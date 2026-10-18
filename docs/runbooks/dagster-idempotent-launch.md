# native Dagster의 영속 요청 식별자

## 범위와 상태

Transport·Weather 주소 수동 갱신에서 HTTP 응답 유실 뒤 같은 요청을 다시 보내도
native run 하나를 사용하기 위한 opt-in 후보다. 기본 Common import와 기존 native
GraphQL mutation은 유지한다. 소비자 BFF·배포는 각 저장소가 소유하며 운영은 미실행이다.
이 초안은 구현·두 독립 적대적 리뷰·CI 완료를 뜻하지 않는다.

## 진입점과 공개 계약

- 같은 프로세스에서 python -m kortravelcommon.dagster_webserver 로 native CLI를 호출한다.
  기존 CLI 인자를 그대로 전달하며 새 서비스나 provider/DB를 만들지 않는다.
- 추가 mutation은 launchIdempotentRun(requestId: String!, executionParams: ExecutionParams!)다.
  성공 결과 IdempotentLaunchRunSuccess는 run과 replayed를 제공하고 native 오류 union을 유지한다.
- 정규 UUID와 location/repository/job selector로 UUIDv5 run ID를 결정한다.
  같은 요청의 config·selector·tags가 다르면 충돌로 거절한다. 권한 검사는 replay에도 적용한다.
- native 저장소의 유일 run ID가 응답 유실·늦은 생성·webserver 재시작을 넘는 식별자다.
  NOT_STARTED만 같은 run의 제출을 재개하고 queued/실행/종료 상태는 기존 run을 반환한다.
- 지원하지 않는 preset·선택 실행·재실행 형태는 명시 거절한다. native permission/config
  검증을 우회하거나 SDK/vendor 본문을 복사하지 않는다.

## 검증과 한계

1. SDK1.13.24에서 기존 mutation 41개와 CLI --help를 유지한 schema 확장 최소 실험은 통과했다.
2. SDK1.13.24/.25의 owned SQLite에서 생성·제출 중단·동시 요청·충돌·권한을 검증할 예정이다.
3. 실제 provider·소비자 UI·운영 DB·daemon은 실행하지 않는다. 독립 리뷰와 소비자 연결은 후속이다.
4. native CLI는 schema factory 인자가 없어 opt-in 진입점에서 native app의 webserver 클래스
   binding만 Common subclass로 교체한다. SDK 파일은 변경하지 않는다.

기존 UNKNOWN 반례와 원문 판정은 보존한다. TTL 뒤 재제출이나 영구 메모리 guard를
영속 식별자의 대안으로 사용하지 않는다.
