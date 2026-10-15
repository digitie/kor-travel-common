# Common PR30 RPC·복구 가이드 독립 FULL 리뷰 A

- execution_id: `A-COMMON-GUIDE-RPC-20261015-FULL`
- 전문 영역: Dagster 실제 동작, 소비자의 복구 실행 계약, 잘못된 성공·원인·보장 표현.
- 실행 기록 시작: 2026-10-15T05:46:42Z. 해당 시각 전에도 초기 object-only 정적 읽기를 수행했으며 그 초기 시각은 별도 기록하지 못했다.
- 종료: 2026-10-15T05:49:45Z.
- 최종 verdict: **PASS / OPEN P0·P1·P2·P3 0**. 고정 commit과 명시된 후속 문서 bytes에 대한 판정이다. 운영·소비자 전체 완주를 승인하거나 재실행한 결과가 아니다.

## 요청·기준선·격리

전달받은 요청은 “Common PR30 최신 HEAD ae5ca6c5bfaf6e514cc2d5b41855c14af67d3de7, 새 two-file delta vs091d4fe1 + docs/runbooks/dagster-adoption.md 전체 맥락 적대 리뷰. RPC300/360/600 일반RPC성격, SSL None canonical identity, STOPPED checkpoint freeze/CAS, healthCPU attribution, janitor freshstart vs cronNOTRUN 주장 검사. 타인 새raw NOT_READ, 운영 호출/제품수정 없이”다. 후속 요청은 해당 HEAD와 root가 추가한 health tolerance 문구 델타를 함께 검토하고 최신 파일 SHA를 고정하는 것이다.

- 실제 commit: `ae5ca6c5bfaf6e514cc2d5b41855c14af67d3de7`.
- 실제 단일 parent: `091d4fe1dda8eacf43b453ad39b4f2e42e9e80fc`.
- 정확한 변경: `docs/runbooks/dagster-adoption.md` 44줄 추가, `docs/journal.md` 9줄 추가. 코드/API/설정 변경 없음.
- 격리: commit object-only. `git show`/`git diff`로 두 파일 델타와 가이드 전체를 읽었다. 시작 HEAD 일치·porcelain 빈 상태를 확인했다.
- root가 후속 문구를 작성한 뒤 종료 상태는 ` M docs/runbooks/dagster-adoption.md` 한 파일이다. 이는 숨기지 않고 추가 검토 대상으로 구분한다. HEAD 내용과 mutable WT를 같은 기준선이라고 부르지 않는다. 최종 후속 가이드의 전체 SHA는 `3819e84cf3864457e419989d06cd9ce0dceef7d8a08f50eb011d1f3036d89454`다. 이 파일의 health 문단만 원래 HEAD 문단으로 역변환하면 HEAD 가이드 bytes와 정확히 같다. 후속 최종 commit은 아직 검토하지 않았으며, 이 승인 범위는 이 고정 bytes와 일치하는 내용이다.
- HEAD 가이드 SHA: `db9b6eddf07c7749955bc0f6c74319318e8959ab018fd56bfd851f44c9befaa4`.
- HEAD journal SHA: `d6658a7c51751f4e08d9b10796ca799ba37e3b611e8a1a0b11110292f0681469`.

운영/네트워크/SSH/Docker/API/DB/browser 호출 0, 제품·문서 편집 0, 다른 리뷰어 raw NOT_READ. A 전용 로컬 모델과 이 원문만 작성했다. 저장 ACK·로그는 root의 운영 증거이며 이를 A가 새로 실행한 운영 시험으로 집계하지 않았다. 기존 리뷰 원문은 보존했다.

## Finding disposition

**A-P3-01 / FIXED — 중간 후속 문구의 CLI·GraphQL 오류 평가 차이 설명.** root가 후속 편집하던 가이드 health 문단은 “CLI의 ignore_errors=True와 GraphQL의 오류 평가도 다르다”라고 했지만 설치된 1.13.24에서는 두 경로 모두 True다. CLI liveness는 `_daemon/cli/__init__.py:129` → `all_daemons_live` → `_daemon/controller.py:418`에서 True를 사용하고, GraphQL `schema/instance.py:93,99` → `_core/instance/methods/daemon_methods.py:118`도 True다. 따라서 같은 신선한 heartbeat.errors가 있어도 이 두 healthy 값은 False로 바뀌지 않는다. 다른 경로인 `all_daemons_healthy`/직접 helper의 기본 ignore_errors=False와 혼동하면 안 된다. 최종 고정 WT health 문단(442~447행)은 오류 평가가 다르다는 주장을 제거했고 interval+tolerance 및 기존 오류 처리 계약 보존만 명시한다. 실제 로컬 SDK 반례·시간 경계 7조건으로 수정 근거를 확인했다.

새 P0/P1/P2 및 남은 P3 finding은 없다. root가 이미 진행 중이라고 전달한 다른 리뷰 결과 원문은 읽지 않았으며, 본 finding은 실제 로컬 설치 SDK를 독립 대조한 결과다.

## 전체 문맥과 공격한 시나리오

- **RPC 예산(가이드 403~418행):** `DefaultRunLauncher`가 proxy client.start_run을 호출하고 proxy.StartRun은 API child client._get_response를 호출한다. client 일반 timeout은 각 프로세스에서 import 시 기본값을 고정한다. STARTING monitor만 늘려도 안쪽 deadline은 바뀌지 않으며 env 편집만으로 running 프로세스가 바뀌지 않는다는 설명이 맞다. general300/360·monitor600은 소비자별 관측 예시로 한정하고 공통 기본값·Geo 자원/배치 튜닝으로 승격하지 않았다. 실제 `default_*_timeout`과 shutdown grace는 general env의 영향을 받거나 별도 env를 우선하므로 별도 예산 비교를 요구하는 문구도 맞다. 문서는 무조건 timeout을 늘리거나 실패 run을 성공으로 덮으라고 하지 않는다.
- **identity(420~428행):** actual local `GrpcServerCodeLocationOrigin`은 None과 False가 모두 비TLS이면서 get_id가 다르다. selector만 같다는 이유로 origin 검증을 느슨하게 하지 않고 정본 stored origin·정의를 함께 비교한다. 다른 버전까지 생략 규칙을 보장하지 않는다.
- **checkpoint(373~381,429~433행):** STOPPED schedule의 정상 last_iteration checkpoint를 run 실행이나 재활성화로 해석하지 않는다. 원본/실측 snapshot 보존·유한/단조/관측 창, 검토한 전체 SHA와 새 CAPTURE 재대조·ACTIVATE full CAS를 유지한다. 실제 실행 중 timestamp 차이를 자동 정상화하거나 비교를 위해 DB를 되돌리라는 예외가 아니다. checkpoint가 CAPTURE 이후 다시 바뀌면 안전하게 막힐 수 있으며 무조건 복원 성공한다는 주장은 없다.
- **CPU·health(435~447행):** job·컨테이너 health, probe 생성 비용·동시 작업·열 제한을 구분하고 PID/CID로 소속을 확인한다. 관측된 backend를 임의 Manager/Transport로 귀속하거나 CS probe를 전부 Dagster full import로 부르는 오류가 없다. 특정 비율의 운영 RSS/CPU 절감·유일 원인을 주장하지 않는다. tolerance300/1800에 기본 interval30을 더하는 실제 판정과 required daemon/instance/오류 처리 계약을 보존한다. 단순 HTTP200·기본 GraphQL healthy로 CLI를 대체하면 지연 허용 범위가 달라질 수 있다는 경계는 맞다.
- **sensor·janitor·UNKNOWN(449행 이후 및 journal 최신 9줄):** 유효 highwater cursor를 STOPPED 상태에 prime/readback 후 publicstart하고 None 첫 tick gap·기존 cursor 보존·다른 instance cursor 이식 위험·일반 retry의 과거 이력 재검색을 구분한다. 새 NOOP 성공과 기존 실패를 별도로 보존한다. Janitor fresh start 및 센서 최초 tick을 실제 다음 cron 실행이나 전체 배치/모든 소비자 완주로 확대하지 않는다. backup catalog/파일/checksum·권한·보존 정책을 따로 확인하고 실제 첫 cron은 NOT_RUN으로 남긴다.
- §1~11의 앱/공통 책임·메모리 상한·수집/transaction·retry 제한·stale UI·건강 probe·tick 조회와 새 §12의 이전 절차를 함께 읽었다. 새 44줄은 provider 재시도나 비멱등 작업을 포괄 재실행하는 공통 API를 추가하지 않는다. 기존 운영 실패·관측하지 못한 범위를 성공으로 바꾸지 않는다.

## 독립 검증과 저장 증거

`common-guide-rpc-check-a-20261015.py` SHA `eb96b995a6a78aef49b8831fd38b151800f61073f8005426ac6eef4a5e9a7c32`:

- 새 문서 계약 **14개 정적 assertion**, 실제 로컬 SDK **5조건**, 최종 WT health 한정 델타 **3개 정적 확인** PASS. SDK 조건은 version1.13.24, canonical None/False identity, general default60, general300의 specialized/grace fallback, specialized60/60/180/grace60 explicit 보존이다. 운영 실행 사례 수가 아니다.
- 저장된 canonical ACK를 내부적으로 확인했다. NOOP outer/nested 동일 run SUCCESS·queued event·disabled/enqueuedfalse·backup 불변·기존 실패 보존, 센서 두 개 SKIPPED/0run·다른 세 schedule STOPPED, Janitor fresh start·backup/drillSTOPPED·first_cron_observation NOT_RUN이 문서와 일치한다. ACK SHA는 NOOP `05f7cbad65b70bb1d59f3194edbc234c407d35eed7841e630e7fed26ffe31f01`, sensor `e01e1f5bba726de3d62f9d8907c861c025864cc842ef3931b53fbca19711ccd4`, Janitor `ada6a6aab312013ef072c9574664b75e2d244e2083ec156d82eae914a86f92cf`다. 저장된 과거 운영 결과를 읽은 것으로 신규 live 검증에 합산하지 않는다.

`common-guide-heartbeat-model-a-20261015.py` SHA `ca0cdd2bbe87d2494f699d82361e7508b24429dd2ea67235a4c836e2cadb7ab9`: 실제 SDK helper와 임의 local heartbeat를 사용한 **7조건 PASS**. errors 있는 신선 heartbeat의 CLI/GraphQL 둘 다 healthy, ignore_errors=False 대조, CLI heartbeat+330 포함/초과, GraphQL heartbeat+1830 포함/초과를 검증했다. 실제 daemon/GraphQL API를 호출하지 않았다. 이전 CPU·센서·운영 단계 모형을 반복 실행하거나 재집계하지 않았다.

자체 `git diff --check`는 commit 델타와 후속 WT 모두 PASS다. root 저장 로그의 링크688문서/2797target 오류0, plan109 오류0, unittest337 중336PASS·1SKIP도 끝부분을 읽어 확인했으며 자체 재실행하지 않았다. skip을 PASS에 포함하지 않는다. 이 로그가 후속 마지막 문구에 대해 새로 완주한 결과인지는 이번 읽기만으로 단정하지 않고, root의 진행 중 최종 gate와 구분한다.

## 미실행·한계

새 Dagster 배포·worker 장애 주입·STARTING race 재현·live UI·실제 Janitor cron·전체 batch·모든 소비자 이전·운영 CPU/RSS 효과 측정은 A에서 NOT_RUN이다. 로컬 SDK/API 계약과 저장 증거를 대조한 문서 리뷰다. 정확한 최종 commit 및 PR CI/merge는 root가 수행한다. 이 원문은 기존 가이드/33개 이상 운영 단계 리뷰를 새 FULL 검증 건수로 재집계하지 않는다.
