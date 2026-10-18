# Common41 C 독립 수정본 리뷰 — a68 제품 / 3093 문서

## 판정과 불변 기준

**SOURCE_HOLD — P1 두 경계 FIXED, 열린 P2 1건.**

- 제품: a68d0495acc38906c31b95b1d0db163bd8f96f5b
- 문서 최종: 3093d2169e2ad9a4c536ed457d1f6e61918f73a0
- source SHA256: e6a36f3bbc07149a28c3329b55baa57d1a62039b31dd49c617e28cce7796decd
- 저장소: /home/digitie/dev/kor-travel-common-codex-native-submit-20261018
- 원23e FULL 및270 중간 원문은 보존했다. 상대 reviewer 원문/모형은 읽지 않았다.
- 이번 증거는 소유 SQLite와 root가 허용한 local 전용 PostgreSQL DB에 한정한다. 운영/SSH/provider/daemon/worker 실행과 원 source/index/branch 수정은0이다.

## C41-C-P2-02 OPEN — native DB statement timeout 소실

위치:
- packages/py/kor-travel-common/src/kortravelcommon/dagster_webserver.py:216 — 별도 NullPool engine 생성
- 같은 파일:121 — scoped connect가 native run SQL을 이 연결로 보냄

native PostgreSQL run storage의 optimize_for_webserver는 연결 hook에서 statement_timeout을 설정한다. native CLI가 전달한 db_statement_timeout도 이 경로를 쓴다. 새 제출 연결은 postgres_url의 옵션만 복사하고 native engine의 hook을 받지 않는다. 이 별도 연결을 실제 run-storage SQL에 결박하면서 native의 유한 쿼리 제한이 사라진다.

실제 .24/.25 각각 소유 DB에서 다음을 확인했다.

1. 공식 storage.optimize_for_webserver(statement_timeout=80, pool_recycle=30, max_overflow=0).
2. 원 storage.connect의 SHOW statement_timeout은 80ms이고 SELECT pg_sleep(0.2)는 취소된다.
3. _submission_lock 안 storage.connect의 같은 조회는 0이고 같은 SELECT는 성공한다.

두 버전 모두 같은1 RED다. 임의로 새 timeout 정책을 추가하는 대신 실제 native CLI/instance에 설정된 제한을 같은 물리 연결에도 보존해야 한다. 기존 connect_timeout5만으로 SQL 실행 시간이 제한되지는 않는다. 이 측정은 실제 소비자 운영 설정이0이라는 주장이 아니다.

SDK 근거: dagster_webserver/cli.py의 instance.optimize_for_webserver 호출, dagster_postgres/run_storage/run_storage.py:119–137의 connection listener 및 set_pg_statement_timeout. 두 설치 버전을 직접 읽었으며 본인 SELECT는 자기 DB에서만 실행했다.

반례:
- /tmp/common41-review-c-7f11mf80/r3/test_pg.py 마지막 test_bound_run_connection_preserves_native_statement_timeout
- timeout-1.13.24.safe.json / timeout-1.13.25.safe.json
- native_timeout=80ms / bound_timeout=0, native_sleep_cancelled=true / bound_sleep_cancelled=false.
- A/root에 즉시 전달했고 root가 수정 요청을 수용했다. 본인은 제품을 고치지 않았다.

## P1-01 / P1-02 독립 closure

P1-01은 SQLite 두 버전에서 같은 run의 두 번째 제출을 busy로 거절하고, 첫 native enqueue 이후 공식 RUN_START를 기록한 다음 replay해도 STARTED가 유지됨을 확인했다.

P1-02도 본인 actual PG 반례를 만들었다. 잠금을 가진 첫 요청이 native NOT_STARTED SubmitRunContext를 얻은 뒤 멈추고, 자기 advisory backend 하나만 종료했다. 다음 요청이 같은 run을 QUEUED로 제출한 뒤 소유 RUN_START 이벤트를 기록하고 첫 요청을 계속했다.

- 원270: 두 SDK 모두 authoritative STARTED→QUEUED 회귀 RED.
- a68: 두 SDK 모두 authoritative STARTED 유지·run1개·첫 요청은 오류·bound engine 재연결0·같은 UUID의 후속 replay 성공 GREEN.

새 ContextVar adapter는 현재 storage/요청에만 연결을 결박하고 다른 thread/context에는 original connect를 사용한다. closed/invalidated 연결은 새 checkout으로 복구하지 않는다. 원 schema/권한/shape/digest 검증과 CLI 연결 회귀는 유지됐다. console alias는 실제 설치 wheel의 entrypoint와 --help를 실행해 확인했다.

native eventlog는 원래 run storage와 원자적 한 commit이 아니다. 실패한 늦은 시도의 enqueue/실패 event가 먼저 남을 수 있다는 문서 한계를 유지한다. 이번 closure는 authoritative run 상태와 반환 오류를 확인한 것이며 eventlog 전체의 원자성·외부 업무 exactly-once·worker 단일 실행을 증명하지 않는다.

## 직접 실행 결과와 fixture 오류 정산

immutable 제품을 새 scratch에 복사하고 offline wheel을 빌드한 뒤 자기 venv 두 개에 설치했다. .24/PG.29.24/SQLAlchemy2.0.54와 .25/PG.29.25/SQLAlchemy2.1.5를 사용했다. 기존 readonly venv와 원 WT를 변경하지 않았다. 나머지 transitive package는 offline cache에서 해석된 소유 시험 환경이며 소비자 lock 전체 동일을 주장하지 않는다.

| SDK | SQLite 기존 집중 | 독립 SQLite | 실제 PG 독립 종합 | 새 timeout 반례 |
|---|---:|---:|---:|---:|
| 1.13.24 | 48 PASS | 11 PASS | 2 PASS | 1 FAIL |
| 1.13.25 | 48 PASS | 11 PASS | 2 PASS | 1 FAIL |

PG 종합은 동시 busy/NOT_STARTED 복구·STARTED 보존·다른 run 병렬 잠금·본문 예외 보존·소유 child crash 해제·native pool size1을 모두 빌린 상태에서 별도 잠금 취득·해제 후 정상 사용·자기 session 단절 후 원예외/재획득·최종 연결/잠금0을 포함한다. job/worker/daemon은 실행하지 않았다. server 종료는 소유 DB에 본인이 만든 advisory session만 대상으로 했다.

PG fixture의 첫 실패들을 제품 실패로 세지 않는다. r2에서 psycopg2 context가 connection 자체를 닫지 않는 점을 발견해 명시 close로 정정했으나, 관측 연결만이 원인이라고 단정했던 중간 설명은 불완전했다. 추가로 본인이 만든 optimize_for_webserver native QueuePool이 SDK RunStorage.dispose(no-op) 이후에도 유휴 연결1개를 보관함을 확인했다. fixture가 도입한 native engine을 명시 dispose한 뒤 두 SDK PG 종합2개씩이 통과했다. 원 fixture와 실패 log는 그대로 보존했다. 이 시험용 정리는 제품의 storage lifecycle 정책을 변경한 것이 아니다.

첫 자기 DROP의 client timeout은 root의 RO 진단으로 CheckpointStart 대기임을 확인했고 자연 완료했다(다음 RO에서 DB 부재). 현재 재시험용 common_native_review_c를 새로 사용 중이며, 추가 timeout fix 재검증을 위해 남겼다. 기존 공유 DB를 변경하거나 root의 다른 session을 종료하지 않았다.

## 문서 delta와 다음 단계

a68→3093은 CHANGELOG/journal/resume/가이드4파일만60+/3-이며 packages/.github는 byte exact다. 문서는 원270 실패·same-connection 보강·console alias·eventlog/권위 상태의 구분·작성자 검증과 독립 gate·운영 미실행을 구분한다. 과거270 artifact 절도 후속 보강 전이라고 표시했다. 작성자 수치를 본인 PASS 수로 합산하지 않았다.

다음은 native statement_timeout 보존 fix의 exact source와 반례 closure다. 그 뒤 최종 문서/CI/소비자 pin 수용은 root가 별도 정산한다. 이 보고서는 merge 또는 운영 승인으로 쓰지 않는다.

기계 증거: /home/digitie/dev/common41-independent-review-c-r3-20261018.safe.json
SHA256 6d348eaf0544a2b0c4b40fe5d0d750ec90c59ea8f2619dc56b261ad423f8c4f1.
scratch: /tmp/common41-review-c-7f11mf80/r3.
