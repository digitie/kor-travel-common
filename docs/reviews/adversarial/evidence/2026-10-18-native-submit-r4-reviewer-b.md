# Common41 Popper FULL post-fix r4 — native policy preservation

**PASS_SOURCE_AND_SCOPED_OWN_FIXTURES_ONLY. OPEN P0=0 / P1=0 / P2=0 / P3=0.**
제품89291f3 및 최종 docs7d46df6에 대한 판정이다. 기존23e/270/a68 REQUEST_CHANGES 보고서는 수정하지 않았다. C41-B-P1-01, C41-B-P1-02 CLOSED 유지, **C41-B-P2-01 statement_timeout 소실 CLOSED**. 전체 suite PASS·운영/실 provider/worker/Daemon 수용 판정은 아니다.

## 관찰 불변 경계

- repository /home/digitie/dev/kor-travel-common-codex-native-submit-20261018.
- base **27cd146ed9e83d3ef481757d2b48e16f232dc88c**.
- 이전 제품 **a68d0495acc38906c31b95b1d0db163bd8f96f5b**, 이전 docs3093d2169e2ad9a4c536ed457d1f6e61918f73a0.
- 제품 **89291f36d731ab906161b96757522e1cd833b4ef**, 최종 docs **7d46df6341b9bc6d5a2bfa69f80e162bebd71422**.
- 모듈 SHA256 **90e06b70e77258cef25c5c6f0e6e9100458480d1ff1bb7e58cf745606992240f**.
- tests SHA256 **7979b71b113707095151c01b0c92dbae8d4de674c18d9f4a920cc3aee4042b5d**.
- pyproject SHA256 **65d5b4e293e84c72c64c3aa524664b8114092432d85c76e1eaaf14f70d45d4cd**; lock SHA256 **dd2f646a026b3057e67f46056c4ea22004d598a5949c9369c373c88632b70805**.
- 제품→docs에서 runtime/tests/extra/lock/workflow 전부 byte 동일. docs4파일61+뿐이다. base..final9파일2507+/2-, diff-check EXIT0.
- own fixture 시작 2026-10-18T05:18:18.855214+00:00; 기록 확정 2026-10-18T05:28:31.814767+00:00 UTC. immutable Git object를 읽고 소유 ext4 archive/venv에만 기록했다. shared source/index/branch/refs/WT를 바꾸지 않았다. 새 peer 원문/모형을 읽거나 요청하지 않았다.
- 원문 요청의 불변 commit으로 검증했으며 별도 manifest는 이번 전달에 없었다. 제품 source 확인 후 저자 handoff는 읽지 않고 최종 docs Git delta만 읽었다.

## P2 closure — 원 native 연결 정책 소실

원인 위치 a68 dagster_webserver.py:216–231: URL로 만든 별도 NullPool은 PostgresRunStorage.optimize_for_webserver의 connect listener를 놓쳤다. 본인 원 실제 .24/.25 PG에서 321ms→제출 안0→밖321ms를 보존했다.

수정 위치 dagster_webserver.py:148–167, :233:
- _submission_engine은 native Pool.recreate()와 Engine을 사용한다. creator/connect listener와 execution_options, dialect/url/echo/hide_parameters를 계승한다. 별도 SQL SET 또는 native SDK 구현 본문을 복제하지 않는다.
- native 기본 NullPool 및 optimize_for_webserver QueuePool exact type만 허용한다. custom subclass는 recreate 전에 거절한다.
- 원 pool을 checkout하지 않으면서 요청 전용 pool을 만들고 finally dispose한다. bound native RunStorage SQL은 기존과 같이 이 물리 연결을 사용한다. 임의 Engine before_cursor_execute 등 모든 event를 복제한다는 주장은 docs에 없고 실제 검증 native 정책 범위로 한정했다.

### 직접 실제 PostgreSQL 검증

Root가 허용한 loopback15436의 **본인 소유 common_native_review_b**만 재사용했다. 새 운영 DB/기존 app DB를 건드리지 않았으며 실제 provider/worker/daemon을 기동하지 않았다. own DB의 synthetic run 행과 native 상태 이벤트만 사용했다.

정식 별도 venv2454: Python3.11.15 / Dagster1.13.24 / dagster-postgres0.29.24 / **SQLAlchemy2.0.54 정식 PyPI cp311 wheel, HAS_CYEXTENSION=true**.
두 번째 별도 venv25: Python3.12 / Dagster1.13.25 / dagster-postgres0.29.25 / **SQLAlchemy2.1.3**. 저자의 .25/2.1.5 검증을 본인 결과로 합산하지 않았다.

각 환경에서 실제 native 기본 NullPool와 native optimize QueuePool에 대해:
1. native policy80ms → submission80ms → 기존 연결80ms. native NullPool 시험도 SDK 자체 set_pg_statement_timeout 함수를 원 pool connect 정책으로 설치했다.
2. bound 연결에서 SELECT pg_sleep(0.3)가 SQLSTATE57014로 **약0.081초**에 취소됐다. 이후 같은 connection의 SELECT1과 정상 unlock이 성공했다(AUTOCOMMIT 보존).
3. QueuePool의 size+max_overflow 전량을 대여해 둔 채 submission이 별도 backend로 열렸다. 원 pool checkedout 증가0, 기존 연결은 계속 살아 있고 policy도 유지됐다.
4. same-context storage.connect는 bound connection을 사용하고 original engine factory 호출0. 다른 thread는 original factory1회/다른 backend이며, 끝나면 원 factory로 복원된다. 같은 run 중첩은 즉시 busy다.

기존 P1-02 반례도 두 환경에서 실제 PG 재실행: 첫 NOT_STARTED coordinator를 멈춘 뒤 **정확한 own DB advisory backend1개만 종료**, 두 번째 동일 UUID를 enqueue/STARTED로 진행시킨 다음 첫 요청을 놓았다. 첫 요청 RuntimeError, request당 row1, 최종 STARTED, 이후 같은 UUID replay STARTED가 유지됐다. 실제 job은 실행하지 않았다.

이때 native 별도 eventlog에는 늦은 PIPELINE_ENQUEUED/ENGINE_EVENT/PIPELINE_FAILURE 실패시도 기록이 남는다. **authoritative RunStorage 상태가 STARTED라는 것과 구분**한다. 이는 앞선 root 허용/guide에 명시된 경계이며 eventlog까지 되돌리거나 성공으로 감추는 fix가 아니다. 두 P1 및 P2 closure는 각기 이 좁은 주장이다.

## 직접 실행과 실패/미완료 이력

- exact 새 policy 단위시험 **3 PASS/48 deselected**씩: .24/2.0.54 **1.50s**, .25/2.1.3 **1.33s**. native creator/listener·full original checkout 분리·cleanup·custom pool pre-recreate 거절.
- 본인 기존 actual native schema/type/argument/default 보존·terminal SUCCESS/FAILURE/CANCELED 재제출0·새 remote 실패0행·요청 tag충돌·version 혼합거절·SQLite stale replay closure **8 PASS**씩: **11.78s / 11.68s**.
- 정식 .24의 product 별도 프로세스 재개 항목 **1 PASS/5.17s(wall6.08)**. 원 source 함수/30초 child 예산을 바꾸지 않았다.
- 최초 pip 확인은 own venv에 pip가 없어서 exit1이었고 uv pip --python으로 정식 wheel 설치했다. dependency/제품 실패가 아니다.
- 최초 .24 추가 실험은 cp312 캐시 SQLAlchemy2.0.54를 py311 path 앞에 둔 pure fallback이었다. 이 환경의59개 묶음은100초에 timeout됐다. **ABI 다른 캐시 실험은 정식2.0.54 수용 근거에서 제외**하고 이력만 보존한다.
- 정식 cp311 .24/2.0.54의59개 묶음도 총75초 예산 종료로 NOT_COMPLETED. stdout 기준 **39 PASSED**, 다음 정확한 test는 **test_separate_process_resumes_not_started_native_run**이었다. 이를 위에서 bounded 단독1PASS로 재검증했다. 당시 누적 suite 지연의 근본 환경 원인은 미확정이며 단독 성공만으로 전체 timeout을 PASS로 바꾸지 않는다.
- .25/2.1.3의59개 묶음은 총75초 종료, **52 PASSED**(제품51 전부+본인 native field1), 다음은 **test_real_persisted_terminal_run_never_resubmitted[PIPELINE_SUCCESS]**. 남은 본인8개는 별도11.68s에 모두 통과했다. 이를 새59개 단일 전체 실행 PASS로 합산하지 않는다.
- broad full suite/전체 locked565는 본인 NOT_RUN이며 author docs의565/PG58/SQLite51 수치를 본인 검사로 쓰지 않는다. 이번 source fix와 직접 관련된 새3/PG policy·pool·session-loss는 위 별도 실행에서 통과했다. 무실패 진행만으로 timeout을 해소했다고 주장하지 않는다.
- own PG DB는 이전 root 지시에 따라 보존했고 반복 DROP/cleanup을 시도하지 않았다. 실제 worker를 만들지 않은 synthetic rows/실험 파일만 남는다.

## 새 wheel/배포 경계

Hatchling을 read-only dependency로 불러 exact Git archive에서 새 wheel을 독립 빌드했다.
**58,563B / SHA256 14dd0d99c97ad561c529722c9a64a8bf076920e25fc4d722226202980297dfc9**.
author hash를 다운로드하거나 복사한 것이 아니라 독립 빌드 뒤 비교했으며 byte 동일하다.
Python14개 Git exact, RECORD21행 중 nonself20개 digest/size를 전수 확인했다.
new own venv24/25/2454에 --no-deps로 wheel을 설치했다. 테스트 import path가 own installed wheel임을 assert했다. borrow한 SDK dependency dirs는 읽기 전용이다. console alias/CLI lazy import는 product 실행 로그에 PASS이며 module source/metadata가 정렬된다.

기존92d daemon-pool은 이 main 기반 wheel에 없다. whole host image가 daemon pool feature를 잃지 않도록 Common38 통합 wheel 계약을 별도로 보존해야 한다. 이 보고서는 기존 운영 image를 이 후보 wheel로 바꿔도 된다는 일반 판정이 아니다. 추가프로세스/컨테이너/daemon 기동은 수행하지 않았다. exact SDK/official pools/URL-storage/QueuedRunCoordinator 한계 및 multi-replica 앱 admission은 그대로다.

## 최종 docs delta

892→7d46은 CHANGELOG/journal/resume/guide4개61+뿐이다. 원23e·270·a68 실패와 초기 NullPool/connect_timeout5 기록은 당시 제품 이력임을 표시하고 최신 Pool.recreate 절을 추가했다. custom Engine event 전체복제 미보장, official pools 한정, Common38 미통합·daemon CLI 보존 후속, 운영 NOT_RUN, root 소유 최종 CI/독립 리뷰/소비자 gate를 구분한다.

docs의 author SQLite51/PG58/locked565·.25 SQLA2.1.5 및 준비 실패 기록은 저자 귀속으로 읽었고 본인 숫자와 섞지 않았다. 새 원문 또는 검증을 소급 PASS로 덮은 부분은 찾지 못했다. 새 archive는 root 소유 후속이며 본인이 추가하지 않았다.

## 소유 근거/미실행

fixture: **/home/digitie/dev/common41-popper-r4-544a1y0p**.
- /home/digitie/dev/common41-popper-r4-544a1y0p/pg-policy-2454.safe.json: SHA256 **3fa9083f73218dbbeeb3e9da0be063aa8f9d04932523764b4d49b6973fe3b8ad**.
- /home/digitie/dev/common41-popper-r4-544a1y0p/pg-policy25.safe.json: SHA256 **d53001cdf3a3acd111e8d53ebc57f9a0c3132e3d53447be1f01f50a3d7bf6281**.
- /home/digitie/dev/common41-popper-r4-544a1y0p/pg-context-2454.safe.json: SHA256 **d374b26f751277158b554b677a121b03aefe9825ab2537ead78f544886a2770e**.
- /home/digitie/dev/common41-popper-r4-544a1y0p/pg-context-25.safe.json: SHA256 **d374b26f751277158b554b677a121b03aefe9825ab2537ead78f544886a2770e**.
- /home/digitie/dev/common41-popper-r4-544a1y0p/pg-postreplay24-2454.safe.json: SHA256 **32d712b8ba982bacac6e3e48525a128c04ddfcfcaa8e9b314c48d1455260c85d**.
- /home/digitie/dev/common41-popper-r4-544a1y0p/pg-postreplay25-25.safe.json: SHA256 **32d712b8ba982bacac6e3e48525a128c04ddfcfcaa8e9b314c48d1455260c85d**.
- /home/digitie/dev/common41-popper-r4-544a1y0p/resume-single2454.stdout.txt: SHA256 **f8eda3a215da85c1b58faab3cf2ea417741622cd1b1d313119b705235d974208**.
- /home/digitie/dev/common41-popper-r4-544a1y0p/own8-2454.stdout.txt: SHA256 **adf07cd59b4d50ab37f561b45db0c2504644beda6358752651ad83d2193222b0**.
- /home/digitie/dev/common41-popper-r4-544a1y0p/own8-25.stdout.txt: SHA256 **2b68a0c185780c142bba4987e48ad2c1c586168985a976a4058cd0e13c0560b5**.
- /home/digitie/dev/common41-popper-r4-544a1y0p/focused-formal2454.stdout.txt: SHA256 **d51502a14c405fd006fdc9875d5998632675a2306d93b783f3cc7ad490194ccd**.
- /home/digitie/dev/common41-popper-r4-544a1y0p/focused-formal25.stdout.txt: SHA256 **ad32eb03fc2ee5d9d6b4017c305ecdaed0ed7ef9ca3f7e1e20aed1a83c127ab5**.

Production/SSH/Docker/provider/daemon/실 worker/서비스 DB/외부 실호출/새 CI/PR 변경 NOT_RUN. exact CI 상태를 새로 조회하거나 진행 중인 CI를 SUCCESS로 세지 않았다. 소유 PG 실험은 운영 검증을 대신하지 않으며 root 기존 실행 권한을 철회하거나 새 사용자 승인요건을 만들지 않는다.

## 실제 전달 요청 원문

Common41 새제품89291f36d731ab906161b96757522e1cd833b4ef freeze. 소비자r4 결과고정후 finalpostfix독립재리뷰 우선 부탁. nativePool.recreate+Engine로creator/options/listener계승; 원pool전량대여·timeout80ms취소·lockloss authorPASS. 본인 timeout P2closure 및 전체delta/cleanup/원poolcontext분리 회귀 직접검증 .24/SQLA2.0.54 포함. peer새결과미열람 raw/hash 부탁드립니다.

후속:

Common41 finaldocs freeze7d46df6341b9bc6d5a2bfa69f80e162bebd71422, 제품892동일. 최종제품판정후 guide/journal/resume/CHANGELOG4files delta도검토해final binding부탁드립니다. rootarchive 원문/closure/index 곧추가예정(정책불변).

환경 후속:

실제 검증 환경은있는그대로기록하면됩니다. ABI맞지않는캐시우선주입보다별도정식venv에SQLA2.0.54설치하거나 본인2.1.3검증한계를명시해주세요. 2.0.54확보불가만으로새failure로세지말고, 직접확인한정식환경결과에근거해판정해주세요. runtime2.0.54 author/C검증은독립성상본인검증에합산하지않습니다.

timeout 후속:

59전체timeout은NOT_COMPLETED로보존하되, 마지막39번째실제test명/정체원인은정확히확인해주세요. source새변경과무관한fixture/environment라면근거로구분하되 단순무실패진행만으로해소하지않기. 전체반복대신그case1개를bounded단독재현하면충분합니다. nativePG/P2closure 직접검증결과와별도로report해주시면됩니다.
