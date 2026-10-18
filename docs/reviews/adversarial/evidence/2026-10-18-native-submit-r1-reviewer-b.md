# Common41 FULL 독립 적대 리뷰 — Popper B r1

## 판정

**BLOCK — OPEN P0=0 / P1=1 / P2=0 / P3=0.**

native run ID 유일성은 검증되지만, 동일 run을 제출하는 두 요청의 stale NOT_STARTED snapshot이 실행 중 run을 다시 QUEUED로 되돌릴 수 있다. 실제 SDK1.13.24와1.13.25의 소유 SQLite에서 재현했다. 이 원문은 exact23e477 제품에 대한 판정이며, 작성자의 후속 수정/문서/재시작 시험은 포함하지 않는다.

## 전달 요청 원문

> Common41 독립 적대 리뷰 시작. 정확 제품 commit23e4775cf883b672ababad1b291bddd3441c9c63 base27cd146ed9e83d3ef481757d2b48e16f232dc88c WT /home/digitie/dev/kor-travel-common-codex-native-submit-20261018. diff 전체와 실제 SDK .24/.25 native unique run/retry/NOT_STARTED resume/permission/selector/config/tags/native schema 보존/CLI/lazyimports 검토. 다른 reviewer원문보지말고 반례실행. A는 추가재시작회귀/문서진행중이라 그 후 delta 리뷰 가능. 소스수정금지 운영SSH/providerDocker금지. own sterile SQLite/native instance/loopback 허용, daemon/실jobworker기동금지. 외부MD 결과, P0–P3 정확위치/재현/판정/hash. root소유fixture ports24101/24301/24102/24105/24305/24602 및공용PG15436 건드리지 말 것. userrequires2reviews. 특히 single request concurrentcreate/submit duplicate worker/run과 failure-aftercreate recovery.

## 불변 입력·시각·격리

- base: 27cd146ed9e83d3ef481757d2b48e16f232dc88c.
- head: 23e4775cf883b672ababad1b291bddd3441c9c63.
- source repository: /home/digitie/dev/kor-travel-common-codex-native-submit-20261018.
- 별도 manifest JSON은 이번 전달에 없었다. 위 실제 메시지의 exact commit으로 Git blobs를 읽었으며 branch checkout/index/source 변경0.
- 전체 delta6파일1665삽입/2삭제. path+NUL+headSHA256+LF를 정렬 결합한 binding SHA256 a869125812f34e6a394d983d35f75f29a1b78c179cc7313cc576160cdff11dea.
- 소유 fixture root: /home/digitie/dev/common41-popper-r1-e0e67a911f. Git object에서 package src/tests/pyproject를 이 경로에만 복사했다.
- start.json의 UTC에 시작 시각을 보존했고, 검사 마지막 수집 UTC는2026-10-18T04:41:39Z 이후다. 완료 UTC는 말미에 기록한다.
- 실제 CI/저자 시험 결과로 나의 판정을 대신하지 않았다. 새 peer 리뷰/모형은 읽거나 요청하지 않았다. 과거 완료된 Common38 리뷰를 앞선 별도 계보 조사에서 읽은 사실은 있으나 Common41 새 결과와 무관하다.
- SDK dependency interpreter는 읽기 전용으로 사용했다. .25: native-submit WT package .venv Python3.12 / .24: concierge-codex-dagster .venv. 실제 distribution version 세 개(dagster/graphql/webserver)가 각각 모두1.13.25/1.13.24임을 확인했다.
- 실행 환경은 PATH/HOME/PYTHONPATH/PYTHONDONTWRITEBYTECODE/PYTEST_DISABLE_PLUGIN_AUTOLOAD만 명시한 sterile env. HOME/PYTHONPATH는 소유 root/src이며 pytest cache를 끄고 confcutdir를 소유 root로 제한했다.
- 실제 SQLite instance, native schema/config/run storage/coordinator를 사용했다. fixture op는 실행되면 AssertionError를 내고 QueuedRunCoordinator를 써 worker를 실행하지 않는다. get_remote_job/plan RPC만 소유 in-memory job snapshot으로 대체했다. 기존 author fixture source를 조립 보조로 재사용했지만 아래 새 경합/계약 검사는 별도 작성해 실제 adapter/SDK를 호출했다.
- provider/운영/SSH/Docker/Daemon/실jobworker/PG/secret/env 파일 접근0, HTTP/socket 서버 기동0. parent가 지정한 포트/PG를 건드리지 않았다.

## C41-B-P1-01 — 동시 replay의 stale submit이 STARTED run을 QUEUED로 역행시킨다

- 심각도 P1, disposition OPEN.
- 위치: packages/py/kor-travel-common/src/kortravelcommon/dagster_webserver.py:135–154, 핵심153–154.
- native 연결: SDK1.13.25 dagster/_core/instance/methods/run_launcher_methods.py:47의 submit_run은 run을 읽어 SubmitRunContext에 담는다. dagster/_core/run_coordinator/queued_run_coordinator.py:308의 submit_run은 그 context 상태가 NOT_STARTED면 enqueue event를 쓴다. dagster/_core/storage/runs/sql_run_storage.py:173의 handle_run_event는 runs.status를 새 event 상태로 갱신하며 STARTED→QUEUED를 CAS로 차단하지 않는다. .24도 같은 실제 결과다.

### 실제 재현 순서

1. 동일 request를 adapter._launch로 한 번 생성한다. instance.submit_run 입구의 소유 예외로 create 이후 제출 전 중단시켜 native DB에 NOT_STARTED1행을 남긴다.
2. 원 instance.submit_run을 복원하고 같은 request를 두 개의 Context로 재전송한다.
3. 첫 요청은 native instance.submit_run이 NOT_STARTED를 읽어 coordinator로 전달한 직후 Event로 지연시킨다. 저장소/SDK 함수를 재구현하지 않는다.
4. 둘째 요청은 원 native coordinator로 정상 enqueue하여 QUEUED가 된다.
5. 실제 worker/daemon을 실행하지 않고 native instance.report_dagster_event(PIPELINE_START)로 실행 시작 상태를 저장한다. 실제 저장소 재조회가 STARTED임을 확인한다.
6. 첫 요청을 풀면 native coordinator가 이전 SubmitRunContext.NOT_STARTED로 enqueue event를 다시 쓴다.

실제 결과(.24/.25 동일):
- native row 수1.
- 요청 두 개가 같은 run ID를 반환.
- event 순서 PIPELINE_ENQUEUED → PIPELINE_START → PIPELINE_ENQUEUED.
- 최종 DB status QUEUED. 기대 STARTED assertion이 실패했다.
- 따라서 단일 row/ID만으로 worker 제출의 exactly-once를 증명할 수 없다. 이미 실행 중인 run을 queue에 다시 노출하여 daemon의 후속 재선택/상태 정산 오염 위험을 만든다. 실제 두 번째 worker 실행은 금지 범위라 수행하지 않았고 실행됐다고 주장하지 않는다.

이 반례는 복수 replica에서만 가능한 가정이 아니다. 실제 native dagster_webserver/graphql.py:239–249는 각 query를 run_in_threadpool(graphql_execution_thread,...)로 실행하므로 단일 기본 webserver 프로세스도 동시 thread 제출을 처리한다.

### 반례 파일·실행

- tests/test_popper_native_race.py SHA256 abde201bcfff1352c0d6ced8538b9f1a970546a447669b7597766a410cbc1eb3.
- own-race25.stdout.txt SHA256 8dafb4b4358de8bc5748edd64a286195f1e4532cbff45cb74ac33612d643236a.
- combined24.stdout.txt SHA256 9eab9f8739b198ab4ed90d8fe6e1c67f5c9131bdc6a4a65078b64ea46b5e34ac.
- 경로는 모두 위 소유 fixture root 아래다.

.25 실행: 1FAILED/1.66초. .24는 제품39개와 함께 실행해 39PASSED+이 반례1FAILED/11.68초였다. 이 실패를 예전 product PASS에 합쳐 성공으로 표시하지 않았다. root에 즉시 전달했고 root 요청에 따라 A에게 이 반례 source/실행방법만 직접 전달했다. 새 peer 리뷰는 공유하지 않았다.

권고: 같은 native instance/run의 fresh status 재조회와 submit을 요청 간 직렬화하고, crash 후 NOT_STARTED 재개를 보존한다. 단순 추가 get_run_by_id만으로 그 뒤 enqueue event까지의 race가 제거되지는 않는다. SQLite/PG 및 다중 프로세스 범위를 실제로 검증하고, stale context가 queued/started/terminal 상태를 되돌리지 않는 반례를 유지해야 한다. 실제 수정은 작성자 소유이며 본 리뷰는 제품을 수정하지 않았다.

## 직접 수행한 나머지 검증

### 전체 source/의존·배포 계약 읽기

- dagster_webserver.py226행 전체, tests471행 전체, runbook32행, pyproject/workflow 전체 diff 및 lock delta를 검토했다.
- opt-in import는 표준 라이브러리만 읽고 schema/main에 진입할 때 SDK를 지연 import한다. _check_versions는 세 SDK distribution의 동일 버전 및1.13.24/.25만 허용한다.
- 새 extra는 dagster-webserver/GraphQL .24–.25, 기존 dagster extra는 유지한다. 잠금 package62→80, 기존 distribution 제거/버전 이동0, 추가18개는 webserver/GraphQL 의존성이다. 기존 공통 패키지의 optional metadata만 바뀌었다.
- CLI는 같은 프로세스에서 native app.DagsterWebserver binding을 Common subclass로 선택 교체하고 원 CLI argv를 전달한다. 영구 SDK 파일/vendor 본문을 변경하지 않는다. 현재 새 모듈에 pool 기능이 있다고 주장하지 않는다(Common38은 별도).
- schema는 기존 roots/types를 사용하고 mutation 하나를 추가한다. 기존 launchRun 등을 전부 바꾸는 교체가 아니다.
- request UUID는 scope(location/repository/job)+UUIDv5 identity, body는 config+requested tags canonical SHA다. replay도 job selector 권한을 확인하고 origin/config/request digest/요청 tag/lineage/selection을 비교한다. 다른 selector scope의 같은 UUID는 다른 run identity라는 구현 범위로 읽었다.
- 지원하지 않는 preset/step/asset/op 선택/lineage/reserved tags/mode는 명시 거절하고 config 검증은 실제 native create_valid_pipeline_run을 재사용한다. exact QueuedRunCoordinator만 허용한다.
- source에는 새 DB schema/migration/별도 storage/daemon/service가 없다. 원 run uniqueness와 native storage의 내구성을 재사용하지만 위 submit 경합까지 보장하지는 않는다.

### 실제 재실행 결과 — 버전별 분리

| 검사 | SDK1.13.25 | SDK1.13.24 |
|---|---|---|
| exact product test_dagster_webserver.py | 39PASS/11.60초 | 39PASS(반례와 combined 실행11.68초) |
| own 계약 test_popper_contracts.py | 7PASS/2.60초 | 7PASS/2.40초 |
| own stale-submit 경합 | 1FAIL/1.66초 | 1FAIL(combined11.68초) |

제품 시험은 내가 exact Git source에서 직접 실행한 결과이며 A의 보고 수치를 인용한 것이 아니다. 버전 두 개/겹치는 fixture를 합쳐 단일 전체 suite 숫자로 만들지 않는다.

own 계약7개:
1. native query/mutation/subscription 전체 기존 field의 타입뿐 아니라 args 타입/default/description, field description/deprecation 보존.
2–4. 실제 native SQLite에 SUCCESS/FAILURE/CANCELED 각각을 이벤트로 저장한 뒤 같은 request replay가 submit을 부르지 않고 실제 terminal status를 유지.
5. 원격 location lookup OSError를 성공으로 바꾸지 않고 native row0.
6. 기존 run의 request digest tag가 오염되면 replay 거절/row1.
7. 혼합 .24/.25 또는 미지원 .26 version 조합 거절.

own 계약 파일 SHA256 2078e9c6460e189b649b964c9c3bd0e1f6b14263711f1df9182612206ed4b5f1.
product25 stdout SHA256 1889baba3f418dca2476ace17b705341d1a1f58032eacad771d0f5f62cc436cc.

exact product 시험에는 native unique create race, create뒤submit전중단 재개, 늦은create, 권한거절, config/tags 충돌, native GraphQL 오류 union, unsupported input, CLI --help/same-process/lazy imports, InstanceRef 재개 및 nonqueued 거절 등이 있다. 다만 기존 concurrent 시험은 run count/ID/replayed만 확인하여 위 STARTED 뒤 late enqueue를 판별하지 못했다.

git diff --check base..head exit0. 새 CI를 실행하거나 진행 중 CI를 PASS로 계수하지 않았다.

## head 파일 binding

| path | head SHA256 |
|---|---|
| .github/workflows/python-package.yml | 36b89c3e54701ac111fc0f0b02197c2f0bbbf69cb4b6ecd8ee3da968647742bc |
| docs/runbooks/dagster-idempotent-launch.md | 646a91d2d3b4da48ae3103775af0d2321e0da94c955e9cbfd250e67101daaa09 |
| packages/py/kor-travel-common/pyproject.toml | d3140354b7695ee27476be1e4eddd6d55434f6342a3084d7c33b90daccf9801a |
| packages/py/kor-travel-common/src/kortravelcommon/dagster_webserver.py | 1a55cf10f06ce561bc143f2293d0e7b7d8bbaaa786ce7bc8df976b50515593bc |
| packages/py/kor-travel-common/tests/test_dagster_webserver.py | d8ba0042e50e8b77ee2b3ffda8565160e420b31c3f11f68f0b4af6cb7a4122a5 |
| packages/py/kor-travel-common/uv.lock | cf2e1ae56c27549759a9adeedbd7ab93359f07c15840643cf8a09e24977d68ad |

## 한계·미실행

실제 provider/운영 DB/PG advisory locking/실 daemon/실 run worker/HTTP 서비스/소비자BFF·브라우저/Manager 이미지/배포·네트워크는 NOT_RUN이다. 실제 two-worker 시작을 실행한 것이 아니라 그 전제인 run 상태의 역행/재enqueue를 실제 SDK/SQLite에서 입증했다. whole repository514+ 또는 새 wheel 설치/lock 재생성은 수행하지 않았다. native metadata/source와 TOML 잠금/두 SDK 직접실행 범위다.

실제 SDK의 GraphQL root/SQLite/동시 thread 경로 검증을 제품전체 운영 수용으로 확대하지 않는다. parent의 기존 rollout 권한을 철회하거나 새 사용자 승인을 요구하지 않는다. 수정 후에는 새로운 immutable HEAD와 이 반례의 RED→GREEN closure가 필요하다.

실제 fixture 시작 UTC: 2026-10-18T04:38:23.537238+00:00
완료 UTC: 2026-10-18T04:43:27.208478+00:00
