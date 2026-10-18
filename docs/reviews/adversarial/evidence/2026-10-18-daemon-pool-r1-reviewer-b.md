# Common38 최신 main 정합 — Popper B 독립 FULL 리뷰

**판정 PASS_SOURCE_AND_OWN_WHEEL_FIXTURE_ONLY. OPEN P0/P1/P2/P3=0.**

exact061 통합 source, 잠금 metadata, 실제 정식 wheel과 독립 fakeDBAPI 계약에서 새 차단 결함을 찾지 못했다. 원92d의 두 리뷰 결론을 복사해 판정한 것이 아니다. 이번 exact 통합 HEAD의 CI/운영/daemon/실PG 수용은 별도이며 수행했다고 주장하지 않는다.

## 실제 전달 요청

> Common41 A수정대기 동안 Common38 최신main정합 독립리뷰 진행. 별도WT /home/digitie/dev/kor-travel-common-codex-pool-reconcile-20261018 current061008f (fullSHA확인), 부모92d+main27cd merge. authorC이며 기존92d pool/CLI 제품 동일, mainreverse-address제품보존, exactdaemon-pool 제약으로mainlock dagster.25→.24/SQLA2.1.3→2.0.54 의도적정합. diff main27cd→061 전체로 source/fullreview하되 기존92d 두리뷰복사판정불가; 실제독립focused반례/lockmetadata불일치/정식wheelentrypoint+lazyimport 검증. 운영/SSH/daemon기동0, 자신의fixture만. 원격38push/merge금지 source수정0. 가능하면오래된PR본문 gate와 현정합source만범위구분해서 원문보고hash. A41fix freeze되면P1closure우선으로돌아갈예정.

중간 parent 지시에 따라 Common41 post-fix 검토를 먼저 수행하고 다시 이 검토로 복귀했다. 두 작업 source/보고서/fixture를 구분한다.

## 입력·격리·검사 경계

- base27cd146ed9e83d3ef481757d2b48e16f232dc88c.
- actual head061008f21550e83ddf9d08b3836e116d60cab42a.
- 실제 부모 순서92d5cf16ad85c2b6cdd0140226066374ae345917 / 27cd146ed9e83d3ef481757d2b48e16f232dc88c.
- main→head 전체13파일1430삽입/84삭제.
- changed path+NUL+SHA256+LF binding22f1e38725e1255bd1ba1e833df817cd9b80a831b1e9140472fe5dedd12c6ce8.
- Git immutable blobs만 읽었다. source/index/branch/PR/원격 push/merge/CI 변경0.
- 소유 package export와 fixture: /home/digitie/dev/common38-reconcile-popper-6c2323ef83.
- 시작 UTC2026-10-18T04:50:15.397830Z. 종료 시각 말미 기록.
- Common AGENTS/SKILL/문서 라우터·현재상태·review/agent runbook은 앞선 동일main 계보 검토에서 읽었고, 이번13파일의 source/tests/config/docs delta를 직접 읽었다. 새 peer 리뷰는 읽지 않았다.
- dependency interpreter는 이 WT .venv를 읽기 전용으로 사용했다. 실제 metadata dagster1.13.24/dagster-postgres0.29.24/SQLAlchemy2.0.54/pytest9.1.1을 확인했다.
- whitelist env, 소유 HOME/PYTHONPATH/confcutdir, bytecode/cache/plugin auto load off로 실행했다. 운영/private/env/SSH/Docker/provider 접근0.
- 이 Common38 검토에서 실제 PG/daemon/worker/네트워크 호출0. Common41의 별도 허용 신규PG 반례를 이 pool 수용으로 섞지 않는다.

## 전체 source·merge 정합

1. daemon_pool.py116행, _daemon_pool_plugin.py183행, test_daemon_pool.py670행 전체를 읽었다. 세 파일은92d와 실제 byte equality를 확인했다.
2. main의 기존 package src 및 reverse-address 회귀15개 tracked 경로는 전부 main과 byte동일이다. 기존 주소 summary/current source+좌표 join을 pool 통합이 되돌리지 않았다.
3. 추가 cli/plugin은 명시 opt-in이다. 원 SDK official daemon console entrypoint/버전 확인, 동일 프로세스 호출, 원 argv, shared env finally 복원, 기존 timeout/InstanceRef 원형 보존을 읽었다. 숨김 instance-ref 우회는 거절한다.
4. 최초3constructor를 global lock 아래 예약하고 primary3개만 bounded QueuePool/strong registry에 넣는다. 이후 임시 engine은 원 NullPool이며 registry에 추가하지 않는다. 생성실패slot도 activation까지 보수적으로 유지한다.
5. public connect 전 creatorPID/scope/retired 검사로 pre_ping 이전 자식/과거pool 접근을 막는다. connect/dispose/recreate는 pool별 RLock, oldpool retired와 원scope계승을 유지한다. 반환은 이 lock을 안 잡아 포화 대기를 해제할 수 있다.
6. cleanup은 현재 engine.pool을 dispose하고 미반환/정리오류를 성공으로 위장하지 않는다. 원 nonzero CLI 예외를 보존한다. primary12접속상한은 pooled3×(2+2)만의 범위이며 임시SDK/프로세스 전체상한은 아니다.
7. workflow는 daemon-pool+reverse-address extras 합집합을 설치한다. 기존 main의 provider 고정 VCS dependency를 유지한다.
8. guide/T319/역사 manifests와 journal/resume은 source 정합/저자 검증/운영 NOT_RUN을 구분한다. 과거44cf/1aada/e0 원문 hash가 현재061 source hash와 다른 것은 각 당시 manifest의 명시된 기준이며 현재 제품 hash로 속이지 않는다.

## lock·metadata 직접 검증

TOML 전체 package record를 name/version/source key로 대조했다.
- 원92d64개 →06165개. 삭제0. 추가는 main 고정 python-vworld-api0.1.0의 exact VCS commit3b174abea1a1e734c60a9c2522b2844474a1ec71 하나다.
- 원92d 기존 외부 package의 version/source/artifact record는 모두 같다. kor-travel-common 자신의 optional dependency/metadata만 통합되었다.
- main62개→06165개. 의도한 Dagster/pipes/shared1.13.25→1.13.24, SQLAlchemy2.1.3→2.0.54를 확인했다. dagster-postgres0.29.24/psycopg2-binary2.9.13/greenlet3.5.6이 추가됐다.
- pyproject daemon-pool exact 요구와 실제 locked interpreter metadata가 일치한다. reverse-address의 SQLAlchemy>=2.0,<3 범위에도 맞는다.
- 새 Common41 module/extra는 이061에 포함되지 않는다. future41+pool 통합이 끝났다고 주장하지 않는다. 그 후 새 extra를 합치면 webserver/GraphQL/PG SDK를 .24로 같이 정합하고 새 immutable HEAD를 검토해야 한다.

## 직접 실행

### 제품 focused source

exact Git export에서 test_daemon_pool.py + test_reverse_address.py를 직접 실행:
**62PASS /2.41초.**
stdout SHA256715fa70f3146ccfa81587f31f9e2fab520930fd802d91b9c80a9638ae6c1687e.

실제 SQLAlchemy2.0.54/fake DBAPI와 SQLite 주소엔진 fixture 범위다. 실제 PG 연결/official daemon main 실행은 하지 않았다. 저자 문서의 관련72PASS를 이 숫자로 바꿔 인용하지 않는다.

### 독립 own fixture

tests/test_popper_pool_union.py를 별도로 작성했다. **4PASS/2.27초**, 새 wheel의 installed directory에서 실행했음을 __file__로 확인했다.

- 실제 wheel metadata의 console script/SQLAlchemy plugin entrypoint와 daemon-pool+reverse-address 두 extras 공존. 원 official CLI loader의 metadata/version 확인 및 Click 함수 load까지만 실행, daemon main은 호출하지 않음.
- 실제 plugin+SQLAlchemy Engine/DefaultDialect/NullPool/fakeDBAPI에서 primary3 뒤 임시100engine을 생성하고 성공/예외를 반복. 연결100개 모두 닫힘, registry3/slots3 유지 및 종료시0 확인. 원 AUTOCOMMIT/connect_args를 덮지 않는 것 확인.
- 부모 PID를 가짜 child로 바꾸어 connect/dispose/recreate가 ping/close/rollback I/O 전에 거절되는지 확인. 같은 PID의 새activation에서 과거scope pool 접속 거절.
- 별도소유 YAML과 fake원CLI의 SystemExit9로 wrapper scope/원shared env복원/종료코드 보존. 실제 daemon/DB는 실행하지 않음.

own test SHA256c8313b54f6842278f13ee7760972712d0e1836811e6aa0f3a7bead0e145b7e56.
stdout SHA256340bcba17ea38668746dd3a2e7cf4442e360b54b48b30f1288e2ab2b3c7b58d2.

### 정식 wheel 새 build/install/RECORD

소유 Git export에서 cached hatchling1.32.0과 cached build dependency를 읽어 새 wheel을 생성했다. 공유cache에 쓰지 않고 -B로 import했으며 네트워크0. uv --no-index/--no-deps/--no-cache target install도 소유 installed directory에만 했다. global venv/package를 바꾸지 않았다.

- wheel kor_travel_common-0.1.0.dev0-py3-none-any.whl,57609bytes.
- SHA2565207fcd510ebd31b4752c311d93b6cc0c4ca8a0ede86b3533a86b339374e70b4.
- ZIP중복entry0, RECORD의 nonself21개 hash/size 전부검증.
- package16개 파일을 exact061 Git source와 byte/hash equality로 확인.
- console script kor-travel-dagster-daemon→kortravelcommon.daemon_pool:main.
- SQLAlchemy plugin kortravel_daemon_pool→kortravelcommon._daemon_pool_plugin:DaemonPoolPlugin.
- 실제 installed METADATA의 daemon-pool .24/0.29.24/2.0.54 및 reverse-address VCS 고정/SQLAlchemy 범위 일치.
- 별도 -I process에서 installed core+daemon_pool import 뒤 dagster*/SQLAlchemy 미import를 확인했다(lazy PASS). plugin import의 SQLAlchemy 의존은 opt-in이다.

wheel 빌드는 package 정식 backend를 사용했으며 SDK/entrypoint 소스나 RECORD를 손으로 만들지 않았다. code는 dev version0.1.0.dev0이며 불변 제품/산출물 hash를 함께 기록한다. 이 wheel이 소비자에 실제 설치됐다는 뜻은 아니다.

## 준비 실패 정산

- 처음 dependency 목록에 hatchling을 함께 조회해 PackageNotFoundError가 났고 which uv도 PATH에서 찾지 못했다. 각각 개별metadata를 확인하고 기존 /home/digitie/.local/bin/uv 및 cached backend를 사용했다. 제품실패가 아니다.
- 첫 focused 실행은 존재하지 않는 test_reverse_address_engine.py를 지정해 tests0/exit4였다. rg/실제 파일목록으로 test_reverse_address.py를 찾아62PASS를 회수했다.
- 최초 own installed-wheel 시험은 pyproject의 pythonpath=src가 PYTHONPATH보다 앞서 source export를 import한 탓에 provenance assertion1FAIL/나머지3PASS였다. -o pythonpath=installed로 명시해 실제wheel4PASS를 확인했다. 원실패를 남겼고 제품을 고치거나 assertion을 없애지 않았다.
- git diff --check main..061 exit0. 새CI/원격PR 조작은 하지 않았다.

## 옛 PR본문·운영 gate와의 구분

원PR38의 body는 임시 Instance 네 번째engine P1을 아직 미해결로 설명한다. 기존92d의 두 확정 SOURCE_PASS/격리 SDK fixed 증거는 앞선 별도 상태보고에 기록했고 본061도 그 제품을 실제 보존함을 확인했다. 그러나 그 옛14CI나 두리뷰를 새061의 exact CI/이번리뷰 대체로 사용하지 않았다.

061이 아직 원격PR38에 반영됐거나 merge됐다고 주장하지 않는다. source 정합 PASS와 실제 opt-in/새소비자image·health·dispatch·수집신선도·CPU/RSS/연결수 수용은 분리한다. 현재 daemon OFF 정책을 유지하고 이번 검토를 이유로 실제 daemon을 시작하거나 새 사용자승인을 요구하지 않는다. root의 기존 merge/deploy 권한도 철회하지 않는다.

## 미실행 한계

whole repository full suite/Ruff/문서 도구 전체/새CI, 실제 SDK official start_run/PG/fork OS process/native daemon 신호/운영 CPU/RSS·소비자 배포는 이번 검토에서 NOT_RUN이다. fake PID/DBAPI 검증을 실제 fork/PG실측으로 확대하지 않는다. source/lock/새정식wheel 및 실제SQLA focused 범위에서 새OPEN0인 판정이다.

종료 UTC: 2026-10-18T05:00:57.367958+00:00
