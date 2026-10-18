# Common41 a68 post-fix FULL delta — Popper B r3

**판정 CONDITIONAL / REQUEST_CHANGES. OPEN P0=0 / P1=0 / P2=1 / P3=0.**

기존 C41-B-P1-01 정상 경합과 C41-B-P1-02 PG 잠금 세션 단절 후 run 상태 역행은 CLOSED다. 그러나 별도 제출 connection이 native webserver의 statement_timeout을 잃는 P2를 실제 두 SDK/소유 PG에서 확인했다. 원23e/270 BLOCK 보고서는 수정하지 않는다. 새 제품 전의 소비자 gate를 이 판정으로 대신하지 않는다.

## 실제 요청 원문

> Common41 제품 a68d0495acc38906c31b95b1d0db163bd8f96f5b 정식 독립 재리뷰 진행해 주세요. P1-02 실제 owned PG session-loss 반례와 same-connection fencing/재연결 거절/다른 context 영향, console alias를 검증. 이전 finding closure 및 새 회귀 포함 exact commit raw report와 hash 부탁합니다. 다른 reviewer 원문 읽지 말고, 운영/daemon 변경 금지. 본인 DB만 사용. Common38 061 PASS 보고서는 보존.

이후 parent가 최종 docs3093d216의 제품동등과 docs delta 정확성을 요청했다. 검토 도중 parent가 새 timeout P2 발견/작성자 수정 요청 사실을 알려줬다. 새 peer 원문이나 모형을 읽지 않고 아래 SHOW 기반 반례를 별도로 실행했다. 따라서 timeout 경계에 대한 최초 발견 귀속은 외부 정보이며 아래 실제 검증은 본인 귀속이다.

## 기준선·시간·격리

- base27cd146ed9e83d3ef481757d2b48e16f232dc88c.
- 원23e4775cf883b672ababad1b291bddd3441c9c63, 이전2704830e98c4353e9770368eb1aea21833015b4a.
- 제품a68d0495acc38906c31b95b1d0db163bd8f96f5b.
- 최종 docs head3093d2169e2ad9a4c536ed457d1f6e61918f73a0.
- WT/home/digitie/dev/kor-travel-common-codex-native-submit-20261018의 immutable Git blobs만 읽었다. source/index/branch/PR/CI 변경0.
- 소유 export/시험 root/home/digitie/dev/common41-popper-r3-71a1d6a7c2.
- 시작 UTC2026-10-18T05:02:52.981762Z. 완료 UTC말미 기록.
- parent의 이전 scoped 허용 신규DB common_native_review_b만 사용. 기존 애플리케이션 DB/운영/SSH/Docker/provider/실worker/daemon 조작0.
- 두 소유 venv에 새 정식 wheel을 no-deps 설치했다. 의존성은 read-only 기존 .24/.25 site-packages 경로만 참조한다. 기존 공유 venv를 변경하지 않았다.
- whitelist 환경/소유 HOME/confcutdir/cache-off/plugin auto-load off. private 운영/env/auth 파일 접근0. 자신의 fixture 연결정보 파일은0600 .private.py로 보존하고 stdout은 safe projection만 출력했다.
- 새 peer 리뷰/결과를 보거나 요청하지 않았다.

## 제품 변경과 연결 source

270→a68은 module의 ContextVar 연결 adapter, 정식 console alias/tests 및 그때 문서7파일 delta다. 새 함수는 instance의 run_storage.connect에 current binding이 있으면 같은 advisory 소유 SQLAlchemy connection을 돌려주는 얇은 wrapper를 설치한다. 다른 storage/thread/context는 원 connect factory를 사용한다. connection.closed/invalidated이면 재연결을 거절하고 binding은 finally에서 복원한다.

전체 연결에서 permission/selector/config/digest/native create/unique 충돌/queued-only coordinator/NOT_STARTED resume와 schema/CLI의 이전 계약을 다시 확인했다. 기존 raw와 source 변경을 섞지 않았다.

## C41-B-P1-01 CLOSED 유지

정상 SQLite 경합은 같은 run 제출을 lock busy로 거절하고 fresh status를 읽는다. 이전 own closure를 별도 export에서 재실행했고 아래 새 wheel 양SDK56PASS에 포함했다. 실제 run 행1개/추가 enqueue0/STARTED replay를 검증했다. 이 결과가 PG timeout 경계를 닫는 것은 아니다.

## C41-B-P1-02 CLOSED — 실제 PG session-loss

이전과 같은 실제 PG 실패 순서를 .25와 .24에서 각각 실행했다.
1. native create 후 submit전예외로 NOT_STARTED1행.
2. 첫 replay가 advisory session lock을 잡고 NOT_STARTED SubmitRunContext를 native coordinator에 넘긴 직후 지연.
3. 신규 소유DB의 granted advisory backend 정확히1개만 pg_terminate_backend로 종료.
4. 두 번째 replay가 enqueue하고 native PIPELINE_START를 저장해 STARTED를 확인.
5. 첫 요청을 해제한다.

수정 후 결과:
- first_error=RuntimeError, 실패 요청이 성공 반환하지 않음.
- authoritative final run status=STARTED, 요청 run row1개.
- 실패 뒤 같은 UUID의 새 replay도 같은 run/STARTED를 반환.
- native run SQL은 죽은 기존 connection에서 실패하고 새 connection으로 재연결하지 않는다.
- 실제 worker/daemon은 실행하지 않았다.

safe pg-loss-postreplay25.safe.json 및24:
SHA25632d712b8ba982bacac6e3e48525a128c04ddfcfcaa8e9b314c48d1455260c85d(두 버전 결과 JSON이 byte동일).

native eventlog는 원래 run store와 atomic commit이 아니므로 ENQUEUED→START→ENQUEUED→ENGINE_EVENT→PIPELINE_FAILURE 시도 행이 남았다. 이는 실제 run의 QUEUED/FAILURE나 실제 worker 실패를 뜻하지 않는다. authoritative run은 STARTED이며 같은 요청은 실패 반환/후속 replay다. 이 eventlog 시도 한계는 root가 요청한 지원 경계와 최종 문서156–160에 명시되어 있다. event log를 고쳐 숨기거나 이것을 source failure/수집 완료로 확대하지 않는다.

이전 PG 정리 시도가 UNKNOWN이었던 소유DB는 이번 시작시 실제 absent로 확인되어 새로 생성했다. 예전 UNKNOWN 보고서를 성공으로 고치지 않고 후속 관찰만 기록한다. 새 fixture DB 정리는 parent의 반복 불필요 지시에 따라 시도하지 않았으며 잔존 가능하다. 이 DB의 STARTED는 실행하지 않는 fixture 이벤트 상태이며 실제 worker가 아니다.

## Context/다른 thread/native pool 분리

실제 PostgresRunStorage와 실제 PG backend ID 비교를 수행했다.
- guard 안에서 storage.connect는 advisory를 가진 동일 backend를 반환.
- guard 내부 native _engine.connect 호출0(소유 counting wrapper로 확인).
- 다른 thread의 storage.connect는 원 native factory 호출1, 다른 backend.
- 다른 thread가 읽은 뒤 원 context는 여전히 같은 bound backend.
- guard 종료 후 원 native factory가 다시 사용된다.
- 같은 run 중첩 lock은 SubmissionBusyError로 즉시 거절.
safe pg-context.safe.json SHA256d374b26f751277158b554b677a121b03aefe9825ab2537ead78f544886a2770e.

기존 product tests의 closed/invalidated 강제값 거절, context 복원/다른thread와 프로세스 crash-release도 양SDK 새 wheel에서 직접 실행했다.

## C41-B-P2-01 OPEN — native webserver statement_timeout 소실

- 위치 packages/py/kor-travel-common/src/kortravelcommon/dagster_webserver.py:216–220 부근(create_engine의 별도 NullPool 연결), _bound_run_connection119–143 및 native submit critical section.
- 실패 조건: native PostgresRunStorage.optimize_for_webserver가 connect hook으로 statement_timeout을 설정한 실제 webserver instance.
- 새 연결은 postgres_url과 connect_timeout5/AUTOCOMMIT만 받아 native engine의 connect event 설정을 잃는다. 같은 연결 binding이 이제 authoritative native run SQL을 이 별도 연결로 보내므로 원 제한도 잃는다.

독립 실행:
1. 소유 PostgresRunStorage를 생성해 실제 optimize_for_webserver(statement_timeout=321,pool_recycle=60,max_overflow=1)을 호출.
2. 원 storage.connect에서 SHOW statement_timeout.
3. 실제 _submission_lock 안의 storage.connect에서 같은 SHOW.
4. guard 종료 뒤 원 storage.connect에서 다시 SHOW.

두 SDK 모두:
- native_before=321ms.
- inside_submission=0.
- native_after=321ms.
- timeout_preserved=false.

이 반례는 장시간 쿼리/실제 lock wait를 발생시키지 않고 실제 PG session 설정만 조회했다. 실제 native source의 optimize_for_webserver가 _engine connect event로 timeout을 부여하는 것도 직접 읽었다. URL options에만 있는 값이 아니므로 URL 보존만으로 충분하지 않다.

영향: submit critical section의 native run SELECT/UPDATE가 기존 webserver의 statement budget 없이 실행되어 행/테이블 lock 경합이나 느린 DB에서 요청·advisory lock·thread 점유를 무기한 늘릴 수 있다. DB lock/timeout 계약 및 실패 신뢰성의 실질적 회귀다. native pool을 점유하지 않는 장점과 별개다.

권고: 지원 SDK의 native webserver 설정을 별도 connection에 보존하고 timeout/lock_timeout 등의 원 계약을 실제 optimized instance에서 회귀로 고정해야 한다. 새 임의 timeout을 상수로 발명하거나 native pool을 잡아 교착을 되돌리지 않는다. 작성자 수정/새 HEAD에서 다시 검토한다. root와 A의 수정 담당에게 scope가 전달됐으며 본인 제품 편집0이다.

## 새 정식 wheel·console alias·양 SDK

소유 Git export에서 캐시된 정식 hatchling backend로 새 wheel을 build했다. 공유cache 쓰기/네트워크0. 두 소유 venv에 no-deps/no-index 설치하고 pytest pythonpath도 실제 wheel site-packages로 명시했다. test provenance가 source export로 바뀌지 않게 했다.

- own wheel58401bytes, SHA256c0fd37b76c692d181cc5a842419c55b299b35a4bd958ad6b215f64bb11f3aac0.
- package Python14개 Git a68 bytes exact, RECORD 총21행 중 nonself hash/size20개 검증.
- 정식 alias kor-travel-dagster-webserver→kortravelcommon.dagster_webserver:main.
- 실제 own alias --help 및 python-m/main 계약·CLI 인자/동일 process/schema 확장을 양SDK에서 검증.
- root/작성자 가이드의 특정 wheel hash81888c56…은 그 작성자 artifact에 귀속한다. 본인의 별도 backend build hash와 같다고 주장하지 않는다. source/RECORD/metadata와 설치 동작을 직접 검증했다.

양SDK 각56PASS:
- .25 29.67초, .24 22.07초.
- exact제품48 + own 기존schema/args/default/terminal/error/version계약7 + own 경합closure1.
- .25 stdout SHA25631ef657d903e6bb0afe07bd0835036b6ff56a5a1d8c06cd8224a86949b1f58e6.
- .24 stdout SHA2566266289041220635ab9b06826df166d665c19843344b3b671435478f34aae691.
- 이 56은 root/작성자562 full/PG53/SQLite48 등을 재인용한 값이 아니다. native PG 실패 반례와 별도 표기했다.

## final docs3093d216 closure

a68→309는 CHANGELOG/journal/resume/runbook4문서만 바뀌었고 packages/.github diff는0이다. source/tests/extra/lock 실제 bytes equality 확인:
- module e6a36f3bbc07149a28c3329b55baa57d1a62039b31dd49c617e28cce7796decd.
- pyproject65d5b4e293e84c72c64c3aa524664b8114092432d85c76e1eaaf14f70d45d4cd.
- tests35e0e294b0799a37085c2208f24f0b565ad4436fe36bb62a49edead425cbaf84.
- lockdd2f646a026b3057e67f46056c4ea22004d598a5949c9369c373c88632b70805.

문서는 원270 P1 실패/후속 source·eventlog 시도 한계, 권위 run 상태, alias와 작성자 검증·CI/소비자/운영 NOT_RUN을 분리했다. 기존553/555/558/562와 각각의 collection 시점을 보존하고 작성자 수치를 독립 reviewer 결과로 주장하지 않는다. 원래270 artifact가 ‘후속 보강 전’으로 정정되어 현재 제품과 혼동되지 않는다.

문서4파일 자체의 추가 P0–P3는 발견하지 않았다. 다만 이 docs closure가 위 timeout P2를 닫거나 새 제품의 전체 PASS를 뜻하지 않는다. base..309 diff-check exit0. 새 CI를 실행하거나 pending을 PASS로 세지 않았다. 작성자 handoff/새 peer 원문은 독립 판정 근거로 읽지 않았다.

## 한계·후속

운영/실 provider/job worker/daemon/SSH/Docker/소비자 BFF·UI/Manager 배포/전체 repository suite/최종CI는 NOT_RUN. 소유 PG 및 native instance에서 발생한 fixture 상태를 실제 수집 성공/실패로 보지 않는다. isolated SQLite/PG 실패 경계와 새 wheel/양SDK 결과만 직접 수행했다.

P1 두 개 CLOSED와 새 P2 OPEN을 구별하며 최종 timeout 수정 제품에 추가 delta closure가 필요하다. root 기존 실행 권한을 철회하거나 새로운 사용자 승인 조건을 만들지 않는다. root 지시에 따라 보고서 고정 후 소비자 r4 검토로 전환한다.

종료 UTC: 2026-10-18T05:10:38.693831+00:00
