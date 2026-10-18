# Common38 ff849 wholewheel union — Popper independent delta review r2

**PASS_SOURCE_AND_INSTALLED_UNION_FIXTURES_ONLY. OPEN P0=0 / P1=0 / P2=0 / P3=0.**
이 판정은 Common38과 Common41을 같은 공식 wheel에 보존한 exact ff849 source/artifact 통합 범위다. 운영 daemon 기동·실수집 완주·운영 CPU/RSS·공유 host image 적용을 완료로 판정하지 않는다.

## 요청·불변 경계·격리

- repo **/home/digitie/dev/kor-travel-common-codex-pool-reconcile-20261018**.
- 이전 독립 PASS **061008f21550e83ddf9d08b3836e116d60cab42a** → 제품 **ff849ea8447c6d2cca1ffa653cfcbe2b2ffa6b32**.
- 실제 부모는 **061008f21550e83ddf9d08b3836e116d60cab42a** 및 main **f9148734b59023cec91ce8fdd44fad6f72d68322** 두 개다.
- 외부 wheel: /home/digitie/dev/common38-union-artifacts-c-20261018/kor_travel_common-0.1.0.dev0-py3-none-any.whl.
- wheel 관찰 **63,151B / SHA256 1abf0547a7b7fbe76284b69c375e83d953788b83a05fbd6720957a869f865b53**, 전달과 일치.
- 본인061 원문 **/home/digitie/dev/common38-main-reconcile-review-popper-r1.md**, SHA256 **90835861892c9197f1e047751479c8d4ca312dbf8de99eb1337e8591a3a72675**를 보존한다.
- 본인 Common41 제품892/finaldocs7d46 원문 **/home/digitie/dev/common41-review-popper-r4.md**, SHA256 **a5a00903ea0154e9f1d746579a90b6d83cb867666c84f6f2d1ebb98189a9e151**를 연결한다. 다른 reviewer의 새로운 결과를 복사해 PASS로 세지 않았다.
- 별도 manifest 파일은 전달되지 않았고 두 immutable parent/head 및 wheel SHA를 요청 그대로 검증했다. Git show/diff/archive만 썼다. shared WT/index/branch/refs/기존 제품파일·운영을 변경하지 않았다.
- root가 현재 WT에 복사했다고 알린 untracked daemon-pool review 원문은 읽지 않았다. 새 상대 통합 review 원문/모형도 요청·열람하지 않았다.
- WSL Ubuntu-26.04, own ext4 fixture **/home/digitie/dev/common38-union-popper-dl5i_e67**. 현재 기록 확정 UTC **2026-10-18T05:46:52.545279+00:00**.
- AGENTS.md, docs/README/resume, T-319 관련 pool 절과 agent-workflow/dagster-adoption 정본을 읽었다. 최초 추정 T-319-daemon-pool.md는 없었으므로 git ls-tree로 실제 **docs/tasks/T-319-dagster-recovery.md**를 찾아 관련 절을 확인했다. 다른 파일로 조용히 대체해 존재했다고 주장하지 않는다.

## 전체 delta와 merge 정합

061..ff849는23파일3400+/5-다. main41의 module/test/CLI/extra/workflow와 docs/archive가 들어오고 기존 daemon source를 고치는 merge resolution은 없다. diff-check EXIT0.

직접 Git byte 대조:
- 061의 **추적 src 파일16개 전부 동일**, 새 dagster_webserver.py 한 개만 추가된다. daemon_pool.py 및 _daemon_pool_plugin.py·기존 pool tests도 보존된다.
- main f914의 **src 파일15개 전부 동일**, daemon_pool.py 및 _daemon_pool_plugin.py 두 개만 추가된다.
- native webserver module/tests는 f914 제품892와 byte 동일하다. Common41의 timeout/fresh-status/same-connection/context/failure 계약을 과거 초안으로 되돌리지 않았다.
- wholewheel은 Python16개+typing/metadata를 함께 담는다. 기존14개 main wheel과 daemon2개를 서로 다른 distribution/RECORD로 혼합한 배포가 아니다.

중요 source SHA256:
- packages/py/kor-travel-common/src/kortravelcommon/daemon_pool.py: **b16fd932b13a029f466633b6e31dd25936898c23041e964734c2c058f5d85313**.
- packages/py/kor-travel-common/src/kortravelcommon/_daemon_pool_plugin.py: **07fe6573bafc906e2ce47baa6c0b79902eea551d341c6a0f73b4435bb61a8521**.
- packages/py/kor-travel-common/src/kortravelcommon/dagster_webserver.py: **90e06b70e77258cef25c5c6f0e6e9100458480d1ff1bb7e58cf745606992240f**.
- packages/py/kor-travel-common/pyproject.toml: **d5e804c4c59c4656d18e55371ac7578ce12fb0028d1ce35c41f0acd51489dcb3**.
- packages/py/kor-travel-common/uv.lock: **c84d92981d3fb4d769a44e77f2623c5dfeec5e741b88940738bb5bf7d91c80b0**.

## lock·CLI·plugin·process 계약

- 061 lock의 **외부64 package entries가 전체 parsed object(versions/sources/artifacts/dependencies 포함) 그대로**다. 삭제/변경0, webserver 관련18개만 추가돼 외부82개다. 자신의 kor-travel-common optional metadata만 합집합에 맞게 바뀐다.
- 최종 lock: Dagster/GraphQL/webserver **1.13.24**, dagster-postgres **0.29.24**, SQLAlchemy **2.0.54**. daemon-pool extra의 기존 exact .24/2.0.54가 webserver .24–.25 허용 범위와 함께 resolve된다. main41 단독의 .25 profile을 조용히 운영 .24에 덮지 않는다.
- pyproject의 console_scripts는 **kor-travel-dagster-daemon → kortravelcommon.daemon_pool:main**, **kor-travel-dagster-webserver → kortravelcommon.dagster_webserver:main** 두 개다. SQLAlchemy entrypoint **kortravel_daemon_pool → kortravelcommon._daemon_pool_plugin:DaemonPoolPlugin**가 유지된다.
- workflow는 기존 daemon-pool/reverse-address extras에 dagster-webserver를 추가해 같은 union을 검증한다. SDK 외부 버전/artifact 교체, daemon command·health·instance 정책 변화는 이 merge에 없다.
- daemon wrapper는 same-process official dagster-daemon loader/argv를 유지하고 run만 activation/동일 DSN plugin을 적용한다. should_autocreate_tables=false/env StringSource·hidden instance-ref 금지·값 없는 오류·원 exit code 복원 계약은 그대로다.
- primary3만 QueuePool2+2, 이후 temporary engines는 원 NullPool이다. 12는 **primary pooled 상한**이고 process 전체 backend 상한이 아니다. strong registry/예약/예외/fork PID-before-lock·scope identity·retired pool/dispose 제약이 보존된다.
- webserver는 별도 프로세스에서 daemon DSN/plugin을 활성화하지 않는다. 새 _submission_engine은 공식 native NullPool/QueuePool exact type만 받으므로 DaemonQueuePool을 억지로 재사용하지 않는다. 올바른 process 경계를 명시하고 잘못 섞는 경우 fail-closed다.

## 직접 wholewheel 설치·재현

1. 제공 wheel의 RECORD23행에서 nonself22개의 SHA256/size를 전수 확인했다. Python16개의 zip bytes는 ff849 Git source와 전부 동일하다.
2. exact Git archive에서 Hatchling으로 독립 재빌드한 wheel이 **제공 wheel과 byte 동일 / SHA1abf0547… /63,151B**였다. 작성자 artifact를 복사해 rebuild라고 부르지 않았다.
3. 별도 own Python3.11.15 venv에 제공 wheel을 --no-deps로 설치했다. 읽기 전용 기존 SDK dependency dirs를 사용하며 **Dagster1.13.24/PG0.29.24/SQLAlchemy2.0.54(정식 cp311 wheel)**를 actual metadata로 assert했다. Common import/distribution provenance가 새 own venv임을 확인했다.
4. exact 제품 daemon_pool34 + reverse_address28 + **본인 통합6 =68 PASS/16.13초**, exit0, skip0. -I -B, PYTEST_DISABLE_PLUGIN_AUTOLOAD=1, --noconftest -c /dev/null -p no:cacheprovider 및 sterile HOME/TMPDIR/PATH로 기존 conftest/env를 차단했다. 제품 source/test assertion을 고치지 않았다.
5. 본인6개 의미:
   - 설치 metadata의 두 scripts·plugin·runtime3versions·new distribution provenance.
   - fresh interpreter에서 core+daemon_pool+dagster_webserver를 import해 **dagster/sqlalchemy import0** 확인.
   - **plugins.register 대역 없이** SQLAlchemy의 공식 entrypoint loader로 plugin을 load. inactive 거절, activation 안 primary3와 임시40개가 NullPool 유지/registry3/slot3, 종료 뒤 owner/registry/slot0.
   - daemon primary pool을 webserver submission engine에 주면 명시 거절, 별도 native NullPool engine clone은 daemon activation/slot을 건드리지 않음. lazy creator는 실제 DB 연결 시 AssertionError인 fixture라 DB/provider 연결은 없었다.
   - actual native schema query/기존 mutation fields 보존+launchIdempotentRun 한 개만 추가, official daemon loader callable 확인(daemon run 실행 아님).
   - 두 **실제 설치 console alias --help** exit0. daemon run/worker/start를 실행하지 않았다.

현재 source에서 새 결함을 찾지 못했다. 같은 함수의 소유 모델을 새로 구현해 PASS로 세지 않았고 실제 설치 wheel/module/공식 SQLAlchemy loader·Engine을 사용했다. 기존 reverse-address/source selector/MAX/수동 cycle 보존은 byte equality와 actual 제품28개로 새 runtime에 다시 연결했다.

## docs/과거 원문·한계

새 resume/adoption/journal/CHANGELOG는 native webserver와 daemon-pool의 합집합, 기존64 entries/profile .24 유지, 두CLI/plugin/wholewheel, 별도 process·daemon DSN 미활성화와 소비자/운영 gate 미완료를 구분한다. 기존 main41 wheel의 daemon 부재 설명은 당시 기록으로 남기고 최신 union 절에서 정정한다. source/운영을 완료로 소급 표시하는 충돌은 찾지 못했다.

061 대비 새 archive는 이미 끝난 Common41 source 리뷰/CI의 역사다. 현재 Common38 새 상대 보고서가 아니며 이번 판정의 근거로 읽거나 합산하지 않았다. root 새 untracked evidence는 아예 열지 않았다. author resume의 locked599/156.00초·문서777/2991·plan109는 작성자 귀속이며 본인 전체599나 fresh CI 수치가 아니다.

이번 리뷰는 실제 PG·소비자 이미지·ARM build·운영 CLI/Daemon/worker/실수집/provider/SSH/Docker/CPU·RSS/새CI **NOT_RUN**이다. 본인 이전 Common41 r4의 PG timeout80ms/lockloss actual closure는 관련 main webserver byte 동일성의 연결 근거이고 이번 통합본에서 PG를 다시 실행한 것으로 세지 않는다. 본인 DB는 root 지시대로 그대로 보존했다. source PASS가 root 기존 merge/deploy 권한을 철회하거나 새 사용자 승인요건을 만들지 않는다.

준비 단계의 존재하지 않는 task path1회 이외 실행 실패/timeout/skip은 없었다. 불필요한 broad 전체suite·이미지·운영 테스트를 다시 돌리지 않았다.

## 소유 증거

- /home/digitie/dev/common38-union-popper-dl5i_e67/tests/test_popper_union.py: SHA256 **24d8effc34d99e12debfae2e2be6ee3b9e6f61fedab63ea599ad4c34d0ad1793**.
- /home/digitie/dev/common38-union-popper-dl5i_e67/focused.stdout.txt: SHA256 **d7cf0e2ce671f5ef0894f4a9af083c157e4a59d8f2ce997a782c05d54eb93aef**.
- /home/digitie/dev/common38-union-popper-dl5i_e67/focused.stderr.txt: SHA256 **e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855**.
- /home/digitie/dev/common38-union-popper-dl5i_e67/install.stderr.txt: SHA256 **52b7dfceda526c807bc8e95bc4ee54e77a1e2b3ae28162477d9fcf4d59f3e26b**.
- /home/digitie/dev/common38-union-popper-dl5i_e67/build.stdout.txt: SHA256 **72a28361920e7a61c04afdafc34b0a525da5b10d25d19d40a988d20d735a69fc**.

## 실제 전달 요청 원문

Common38 최종 통합 ff849ea8447c6d2cca1ffa653cfcbe2b2ffa6b32 독립 delta 적대리뷰 진행해 주세요. WT /home/digitie/dev/kor-travel-common-codex-pool-reconcile-20261018. 이전061 판정 대비 main f914(Common41) 통합, 런타임 Dagster1.13.24 SQLA2.0.54/외부64entry보존, 공식 wholewheel 두CLI+plugin/lazy 검토. 원문 고정 보고해주세요. wheel /home/digitie/dev/common38-union-artifacts-c-20261018/kor_travel_common-0.1.0.dev0-py3-none-any.whl SHA1abf0547a7b7fbe76284b69c375e83d953788b83a05fbd6720957a869f865b53. 운영조작금지.

실행 후속:

지금 실행 요청: Common38 최종 ff849ea8447c6d2cca1ffa653cfcbe2b2ffa6b32 독립 delta 적대리뷰. 앞선 send_message idle이라 실행되지않았습니다. WT /home/digitie/dev/kor-travel-common-codex-pool-reconcile-20261018.061 대비mainf914 union, Dagster1.13.24 SQLA2.0.54/외부64entry보존/wholewheel 두CLI+plugin lazy. wheel /home/digitie/dev/common38-union-artifacts-c-20261018/kor_travel_common-0.1.0.dev0-py3-none-any.whl SHA1abf0547a7b7fbe76284b69c375e83d953788b83a05fbd6720957a869f865b53. 독립 원문고정후 보고. 운영0. 다음Geo590/591 및Manager513review 예정.

untracked 주의 후속:

Common38 WT에 root가 docs/reviews/adversarial/evidence/2026-10-18-daemon-pool-* 원문·sourceCI 4개 untracked 복사했습니다. 제품HEAD ff849 불변이며 리뷰결과/상대원문은 읽지마세요. 독립검토에는 git ff849 snapshot 사용 바랍니다.
