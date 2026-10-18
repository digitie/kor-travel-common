# Common38 061008f 독립 FULL 리뷰 — A/James

- 실행 ID: common38-independent-a-061008f-20261018
- 시작 UTC 원시 시각: 별도 기록하지 않아 복원하지 않는다. 종료 UTC: 2026-10-18T05:24:55.366028+00:00
- 전문 렌즈: 소비자 공개 CLI/extra/plugin 계약, 상태·오류 진실성, lifecycle/fork/임시 Instance 연결, main 통합 보존.
- 작성자가 아니다. 현재 peer 새 원문/모형을 읽거나 요청하지 않았다. parent가 전달한 peer PASS는 본 판정 근거로 사용하지 않았다.
- 전달된 통합 manifest: 별도 manifest 파일은 지정되지 않았고 아래 exact commit/WT 요청이 기준이다.
- 관찰 HEAD: 061008f21550e83ddf9d08b3836e116d60cab42a
- 통합 비교 main: 27cd146ed9e83d3ef481757d2b48e16f232dc88c
- 원 pool 제품: 92d5cf16ad85c2b6cdd0140226066374ae345917
- 원 pool 개발 base: c48595880aaad4367802ad71af2525a8a5e17c6a
- merge 두 부모 92d5cf1 +27cd146, main→통합13파일1430+/84-.
- 격리: 위 Git object를 git archive로 /home/digitie/dev/common38-review-a-6cln7143에 추출했다.
  원 WT status는 시작/종료 모두 clean, HEAD 동일. source/index/branch/peer파일 편집0.
- Common AGENTS, SKILL 라우터, README/resume, T319, agent-workflow/review 규칙,
  guide§18과13파일 full delta/두 모듈 연결·670줄 회귀를 확인했다.
  기존 과거 manifest3개는 당시 제품/실패 범위를 확인하는 역사 자료로만 읽었고 새 peer 보고서는 읽지 않았다.

## 판정

**CONDITIONAL — 제품 SOURCE PASS, OPEN P0=0/P1=0/P2=0/P3=1.**

제품 기능 차단 결함은 발견하지 못했다. P3 CHANGELOG 정산이 남아 있고 parent는
Common41 main 통합 뒤38의 공개 기능 항목을 추가해 닫겠다고 수용했다.
이것은 Common38 운영 적용·성능·실수집 완료 판정이 아니며 새로운 운영 승인 요건도 만들지 않는다.
향후41과 합친 wheel/CLI 합집합은 아직 이 exact061에 없으므로 후속 통합 검토 범위다.

## C38-A-P3-01 — 공개 daemon CLI/extra/plugin의 CHANGELOG 누락 (OPEN)

- 위치: CHANGELOG.md:9 Unreleased, AGENTS.md §8/agent-workflow.md §6 기록 규칙.
- 실패 조건: 이 PR로 kor-travel-common[daemon-pool], kor-travel-dagster-daemon console script,
  SQLAlchemy plugin이 새로 공개되지만 현재 CHANGELOG에는 daemon/pool/연결 재사용 항목이 없다.
  실제 rg 검색 결과0이며 CHANGELOG는13개 변경 파일에도 없다.
- 영향: guide/task에는 설명이 있지만 패키지 소비자 변경 이력에서 opt-in 기능과 exact 지원 조합을 찾지 못한다.
  기능·안전 결함으로 확대하지 않는다.
- 권고: Unreleased Python 절에 opt-in extra/정식CLI/plugin과 검증 조합/운영 미검증의
  짧은 additive 항목을 추가한다. 기존 역사 삭제나 제품 재구현은 불필요하다.
- disposition: parent 수용, 후속41/main+38 통합 때 정산 예정. 현재061에는 OPEN을 그대로 유지한다.

## 독립 검증과 공격 범위

1. 원92d 대비 daemon_pool.py/_daemon_pool_plugin.py/test_daemon_pool.py bytes exact.
   모듈 SHA256:
   - _daemon_pool_plugin.py: 07fe6573bafc906e2ce47baa6c0b79902eea551d341c6a0f73b4435bb61a8521
   - daemon_pool.py: b16fd932b13a029f466633b6e31dd25936898c23041e964734c2c058f5d85313
   - tests: 9f9f9d613e192457d55fd5e3e58ce85dfa779c67682bbe0980056d7f1bed6761
   main27의 기존 Python source/tests28파일도 모두 동일하다.
2. uv.lock 구조 대조: 원92d 외부64package의 version/source/artifact 변경0,
   고정 python-vworld-api 하나 추가. kor-travel-common 자체 optional dependency/metadata만 합집합이다.
   exact daemon profile(.24/.29.24/SQLAlchemy2.0.54)과 main reverse-address pin이 함께 남고
   workflow가 두 extra를 모두 설치한다. main 대비 지원 SDK downgrade는 명시 profile 의도이며 숨은 무관 upgrade로 보지 않았다.
3. SQLAlchemy2.0.54 actual library/fake DBAPI 원회귀34 PASS1.34초.
   별도 own6 PASS0.13초. 마지막에는 SDK import를 명시 거절하는 MetaPathFinder와
   PYTEST_DISABLE_PLUGIN_AUTOLOAD=1/--noconftest/-p no:cacheprovider 환경에서
   두 세트를 함께 **40 PASS1.23초**로 실행했다. 실제 Dagster/PG import·호출0.
4. own fixture는 24개 동시 engine 생성 중 primary3/temporary21, 임시63회 fake 연결 즉시close,
   primary12개 대여·종료close, 실제 소유 fork 자식의 connect/dispose/recreate/activation 선행거절,
   부모 fake 연결 유지, 퇴역 bound-connect/다음scope 차단, busy cleanup의 원예외 보존,
   URL options/DSN 원본 보존, 실패 생성 슬롯 제한과 다음scope 초기화를 확인했다.
   알고리즘을 별도 구현해 통과시킨 것이 아니라 exact 패키지의 plugin/activation/SQLAlchemy Pool을 호출했다.
5. 동시성/source tracing: pool lifecycle RLock은 checkout 시작과 dispose/recreate를 직렬화하고
   반환은 막지 않는다. creator PID 검사가 inherited lock/pre_ping 앞에 있다.
   recreate는 원 scope를 계승하고 old pool을 retire한다. delayed engine registration은 old activation을 거절한다.
   primary 슬롯은 engine_created 전에 global lock으로 예약하며 실패 슬롯도 수명 동안 보수적으로 유지한다.
6. 네 번째 이후 공식 임시 Instance는 원 NullPool 유지/registry 제외여서 launch를 막지 않는다.
   상한12는 primary pooled 연결에만 적용되며 프로세스 전체/worker 수로 확대하지 않는 guide와 일치한다.
   원 URL/AUTOCOMMIT/options와 SDK retry/backoff를 바꾸지 않으며 timeout1초를 전체 상한이라 주장하지 않는다.
7. 공식 CLI metadata loader/version/argv, literal/custom/hidden-ref 거절, env finally복원,
   임시 StringSource가 외부 CS에서 원 env로 해석되는 지원 한계를 연결 확인했다.
   core import에는 SDK eager import가 없고 공식 plugin registry를 사용하며 SDK body 복사/수정은 없다.
8. 소유 archive에서 wheel build 성공. 57,609B,
   SHA256 0ddc73ea819c0675e341126360dcdd26925eb3f718b93e0f6378d2caee9b2cc7.
   Python15개 source exact/RECORD22 hash·size 검증.
   zip wheel 우선 sys.path에서 실제 distribution entrypoint load로 daemon CLI/plugin이 정식 함수·클래스에
   연결됨을 확인하고 lazy create_engine/plugin/URL보존을 실행했다.
   SDK import를 거절하고 creator는 실제 DB 연결 시 즉시 실패하도록 설정했다.
   이는 native CLI의 실제 daemon 실행/설치 소비자 수용이 아니다.
9. 링크766문서2969targets 오류0, plan109 오류0, 세 제품/회귀 파일 Ruff PASS,
   git diff --check 27cd146..061008f PASS. source WT clean을 재확인했다.

## 초기 자체 검증 실패 (제품 finding과 분리)

- 첫 own fixture가 create_engine의 pool_*→Pool 인자 번역을 누락해5FAIL1PASS였다.
- 번역 정정 후1FAIL5PASS는 수동 DefaultDialect에 DBAPI.Error가 없어 원 PoolScopeError가
  fixture InvalidRequestError에 가려진 경우였다.
- FakeDBAPI.Error를 넣은 첫 정정에도 paramstyle 누락으로5FAIL1PASS였다.
  fake DBAPI에 paramstyle=named를 제공해 own6 PASS/마지막 combined40 PASS를 확인했다.
- 위는 소유 fixture만 고쳤고 제품/원회귀는 수정하지 않았다.
  원 Console 출력은 대화에 남으며 소유 own-initial-fixture-issues.txt에 준비 실패를 기록했다.
- 최초 manifest 경로를 evidence 하위가 아닌 상위로 읽으려던 cat은 file-not-found였고 검증0이다.
  git diff --name-only에서 정확 evidence 경로3개를 찾아 확인했다.
- 소유 archive 안 준비실패 MD 때문에 첫 링크수767이었고 그 소유 기록을 txt로 옮긴 뒤
  정본 링크수766/2969/0을 재확인했다. 원 repo 문서는 변경하지 않았다.

## NOT_RUN / 해석 한계

- 실제 provider, 운영/SSH, Docker, 실제 SDK daemon/job/worker, 실제 PG/SQLite DB 연결,
  소비자 이미지/CLI 실제 배포, native SIGTERM, 운영 CPU/RSS·freshness는 실행하지 않았다.
- 설치된 interpreter에는 SDK .24가 있지만 test에서는 해당 imports를 명시 금지했다.
  metadata/SQLAlchemy2.0.54와 fake DBAPI 검증을 실제 SDK/PG gate로 확대하지 않는다.
- parent의 기존 native DefaultRunLauncher/PG/consumer 증거는 본인 실행으로 재집계하지 않는다.
- 기존 main 기능은28개 source/tests bytes 보존을 확인했으며 모든 주소/기타 패키지 회귀를 새로 실행하지 않았다.
- 새 CI를 실행/관찰하지 않았으며 작성자 journal의72PASS나 원격 CI를 본인 검사로 세지 않는다.
- Common41 신규 webserver adapter는 이 snapshot에 없으므로 그 통합/wholewheel 동등성은 후속이다.
- Fork 후 이미 대여한 raw connection을 임의 Python 코드가 직접 사용하는 동작까지 pool 경계가 가로채는
  계약으로 확대하지 않는다. 공식 pool checkout/dispose/recreate/activation 경계를 검증했다.
- 원 tmp fixture와 source archive는 감사 재현용으로 보존하며 다른 프로세스/DB/소스 정리0.

## 실제 전달받은 요청 원문

소비자 a68 pin 갱신/push 완료 Weather115 5d8547e8b377176fc2669e29fbe163b72209cb18, Transport86 bb191137406b95a43f6ed8e477b35b786f88df0d. 실제 native delay 각1PASS, full/UI 진행. B/C a68 독립리뷰 중. Common41 문서·전체검증 마무리 후 Common38 통합061008f21550e83ddf9d08b3836e116d60cab42a 독립 FULL 검토 부탁드립니다. C가 통합 작성했고 B는 source/ownwheelPASS. A는38 비저자로 독립 검토 가능; peer보고서 읽지 마세요. WT /home/digitie/dev/kor-travel-common-codex-pool-reconcile-20261018. 추후41 main 통합 delta도 별도검토할 계획.

후속 소유권/보류 해제 원문:

7d46 freeze확인. Common41 WT 제품/docs 편집은여기서완료로보고 root가review archive/closure/index 소유권받겠습니다. handoff외추가커밋전알려주세요. A는Common38 독립리뷰재개;41머지완료뒤061에main합친통합delta는추가검토요청드리겠습니다.

P3 disposition 원문:

P3 CHANGELOG 누락 수용합니다. Common41머지후38통합할때 daemon-pool extra/CLI/plugin 항목 추가해닫겠습니다. 현재061원문은 P3 OPEN그대로고정해주세요. 통합delta검토때문서해소확인 요청하겠습니다.
