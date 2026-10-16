# T-319 Dagster 실행 복구 프리미티브

- 상태: IN_PROGRESS
- 우선순위: P1
- Gate: Python 단위·wheel 설치·weather 소비자 회귀·2인 리뷰
- 선행: 없음
- 외부 선행: common·weather PR 병합 및 공유 instance 설정 적용·운영 장애 복구 실측

사용자가 weather의 반복 실패·영구 정지 방지와 transport·map·pinvi·geo로 확산 가능한
Python 공통 코드를 요청했다. 문서의 단계별 Python task 순서보다 이번 사용자 요청을
우선하며 다른 task의 미구현 모듈은 완료로 표시하지 않는다.

## 범위와 근거

| 저장소 | 확인한 main | 가져온 계약 |
|---|---|---|
| weather | `5da6e15` | provider별 job·부분 게시·source lineage·unique key·run monitoring |
| transport | `6b772376` | run group 제한·job의 max runtime 태그 |
| map | `a68c2b7d` | 작업 종류별 슬롯 예약·취소 상한·run 완주 탐침 원칙 |
| pinvi | `80c92b6c` | 비멱등 outbox는 worker 재개/재시도 금지 |
| geo | `3f4ddc2d` | 생존 조회 장애를 worker 사망으로 해석하지 않음·lease와 orchestrator 분리 |

`packages/py/kor-travel-common`만 실행 정책·동기 deadline·중복 예약 방지·주입형 회수 sensor를
소유한다. DB schema·provider·계정·배포 lifecycle은 소비자에 남긴다. UI 추출은
[T-216](T-216-dagster-operations.md)에서 기록한다. transport/map/pinvi/geo 자체 변경은
이번 요청의 후속 확산 대상이며 이번 후보에서 채택 완료로 표시하지 않는다.

## 수용 기준

### 2026-10-15 고정 phase 예약 분산 — 수용 설계

사용자 요청에 따라 `kortravelcommon.scheduling.staggered_cron`을 추가한다.
Weather acc8의 external 9개가 같은 3시간 cron을 사용하고 Transport 15a928b의
airport/highway가 같은 5분 cron을 사용한 관찰이 공통화 근거다.
앱별 phase 표와 provider 발표 시각·수집 범위·실제 배포는 소비자가 소유한다.

- keyword-only 정수 `interval_minutes`, `phase_minutes`로 5필드 cron 문자열을 만든다.
  bool·잘못된 타입과 범위는 거절한다. phase는 명시적으로 고정하며 해시·랜덤·슬롯 수를 쓰지 않는다.
- 60분 약수인 분 주기 또는 24시간 약수인 정시 주기만 허용한다.
  5·180·1440분은 허용하며 7·90분은 거절한다. `0 <= phase < interval`이다.
- 실제 Dagster 달력으로 일일 횟수·간격·phase와 자정·월 경계를 확인한다.
  Weather 후보 phase 7,27,47,67,87,107,127,147,167은 합계72회/일,
  Transport 후보 phase1/3은 각각288회/일을 보존한다. 다른 phase 추가가 기존 cron을 바꾸지 않는다.
- 순수 helper는 Dagster를 import하지 않으며 core-only wheel에서 동작한다.
  시간대는 소비자 scheduler가 소유하고 KST/UTC 같은 DST 없는 clock에서 간격을 검증한다.
  DST 전환·daemon 지연·coalescing·실제 run 동시성은 cron 분산과 별개다.
- 운영 CPU/RSS·수집량·신선도 개선은 소비자 실측 전 NOT_RUN이다.
  이번 Common 후보에는 자동 runtime 설정·서비스·소비자 pin 변경을 넣지 않는다.

구현·wheel·필수 문서 gate 후 동일 immutable 후보를 두 명이 독립 리뷰한다.
소비자 채택·실측과 병합 전 승인 상태를 이 설계의 달력 검증 결과로 대체하지 않는다.

- [x] metadata 장애 시 중복 예약을 만들지 않으며 외부 location의 동명 job은 막지 않는다.
- [x] 멱등성을 명시하지 않은 job은 native 자동 재시도를 상속하지 않는다.
- [x] deadline 뒤 client 재사용 금지 계약과 daemon/instance 설정 선행을 문서화한다.
- [x] wheel에서 core-only import·dagster extra·테스트가 동작한다.
- [x] 두 독립 reviewer가 동일 commit 기준선과 post-fix를 검토한다.

## 검증 기록

실행 결과와 리뷰 disposition은 같은 PR의 journal·리뷰 기록에 남긴다.
운영 장애 주입·shared plane 배포: `NOT_RUN(이번 작업은 코드 보강·UI 검증·PR 병합 범위)`.
소비자 구현 안내는 [Dagster 적용 가이드](../runbooks/dagster-adoption.md)에 둔다.

코드·단위·소비자 live 검증과 2인 review는 완료했다.
[최종 리뷰](../reviews/adversarial/2026-10-04-dagster-recovery.md),
[PR #24](https://github.com/digitie/kor-travel-common/pull/24),
[weather PR #72](https://github.com/digitie/kor-travel-weather/pull/72)에 증거를 보존한다.
IN_PROGRESS는 외부 운영 배포/채택까지 완료로 세지 않기 위해 유지한다.

## 2026-10-05 Geo 채택·최종 코드 검증

[최종 판정](../reviews/adversarial/2026-10-05-geo-common.md)에 fixed73e3ff8/Geo4c59efe, 두 독립 최종 PASS, 최초 BLOCK와 전체 수정 원문·SHA256, Python69/UI48·Geo UI231·실제 PostgreSQL17·Linux Chromium/Firefox13항목씩의 증거를 보존했다. 메모리는 유한 page·응답·동시성 구조를 적용했고 운영 RSS 실측은 NOT_RUN이다. 운영 설정/다른 앱 채택은 완료로 세지 않는다. 가이드를 포함한 common PR26·Geo PR570의 최종 checks PASS 후 merge한다.

## Map·PinVi HTTP 후속 (2026-10-05)

공용 HTTP 제한을 구현하고 두 독립 리뷰의 clean CI 의존 누락·DigestAuth 중간 응답·느린 정리 finding을 수정했다. API 소비자 채택·재구축·live 검증은 각 Map/PinVi PR에서 수행하며 이 문서에서 완료로 세지 않는다. 고정1f8e339의 두 독립 FULL 리뷰와 finding closure를 [최종 판정](../reviews/adversarial/2026-10-05-map-http-closure.md)에 보존했다. 외부 CI·소비자 운영 live는 별도 gate다.

## 2026-10-06 Map·PinVi 실제 후속 수용

[후속 판정](../reviews/adversarial/2026-10-05-map-health-closure.md)에 Common a960/Map1a3/PinVi005 제품113파일 2인 FULL·최종 가이드·실제 paired 재구축·운영 설치 bytes/identity·여섯 서비스 healthy·Chromium/Firefox UI4·ACL40/D1/D2와 실패 원문을 보존한다. 기존 전역 task IN_PROGRESS는 다른 소비자 운영 채택·공유 DB 장애 주입/RSS까지 완료로 세지 않기 위해 유지한다. 이번 Map/PinVi 후속 구현·실제 수용은 완료했고 최종 문서 포함 CI와 #28/#1303/#576 merge는 다음 gate다.

## 2026-10-16 경량 HTTP 생존 점검 — 수용 설계

Weather API와 Transport backend가 같은 Python urllib HTTP 생존 점검을 반복하며
실제 호스트 단일 표본에서 각각 약3초의 self CPU를 사용했다.
앱의 상태 경로·주기·Docker 재시작 정책은 소비자가 소유한다.

- core-only stdlib 모듈 `kortravelcommon.http_health`는 IPv4 loopback의 명시한
  port/path에 GET 한 번만 보낸다. DNS·TLS·redirect·자동 재시도·provider/DB 호출은 없다.
- 연결/전송/헤더 수신에 하나의 monotonic 전체 예산을 사용하고 최대16KiB 헤더만 읽는다.
  완전한 HTTP/1.0 또는1.1 헤더의2xx만 성공이며 malformed/EOF/timeout/non2xx는 실패다.
- 검증된 함수와 CLI를 제공하며 성공0/실패1/잘못된 인자2, 응답 본문·오류·주소를 출력하지 않는다.
- 실제 loopback 반례·전체 Python·core-only wheel 설치·두 독립 리뷰가 필요하다.
  소비자 exact source 채택과 실제 healthy/CPU/UI 검증 전 운영 효과는 NOT_RUN이다.

## 2026-10-16 health 조회·복구 격리 — 후속 수용 기준

사용자 CPU·반복 실패 분석 후 확인한 여러 소비자의 공통 health 생성 경로가 근거다.
기존 Common health 자체는 조회 전용이지만 소비자 Manager override에는 별도 reaper/
run DB 변경/PID1 종료 동작이 있어 소비자 PR에서 제거·책임 이관을 확인해야 한다.

- 기존 API/CLI·고정 phase·strict HTTP를 보존하고 새 live/ready API를 추가한다.
- optional gRPC lazy import, IPv4 loopback, strict SERVING, 기대 repository/profile 검증,
  공유 logical4초·4MiB 응답 한도·quiet CLI0/1/2를 회귀로 확인한다.
- HC 경로에 run 변경·kill/reaper·DB/앱/Dagster 본체 import·자동 복구를 넣지 않는다.
- 실제 격리 loopback success/error/deadline, Python3.11/core-only/grpc-only wheel,
  cold CLI wall/self CPU/실행 후 RSS를 측정한다. 논리 deadline과 process hard wall을 구분한다.
- 소비자는 measured cadence/phase와 bootstrap 여유를 정한다. 초 단위 시각보다
  일일 횟수/간격/공식 발표·정확한 run 귀속과 UNKNOWN 보존을 우선한다.
- 동일 immutable 후보의 두 독립 적대 리뷰와 소비자 운영 채택은 별도 gate다.
  새 supervisor/서비스·실제 배포/운영 효과는 이번 Common 코드 수용에 포함하지 않는다.

계약·이관과 실측 한계는 [적용 가이드 §14](../runbooks/dagster-adoption.md#14-생존정의-준비-조회와-복구-동작-분리)에 둔다.


### proxy 환경 우회 반례 (후속 수정)

독립 리뷰가 새 health 채널의 proxy 환경 상속을 재현했다. 새 채널에서 HTTP proxy
사용을 명시 차단한다. grpc_proxy/http_proxy/https_proxy 각각 정상·손상 정의·닫힌
target의 실제 subprocess 회귀로 loopback target 귀속·proxy 연결0·quiet를 확인한다.
원 initial manifest/실패 증거는 유지하며 post-fix 두 독립 재검토 전 완료로 세지 않는다.

## Common34 활성화 전제 문서 후속

C-P2-01의 singleton/exclusive gRPC origin·구/신 overlap 미지원·구 init/worker/cgroup
소멸을 확인한 serial 교체 전제를 [가이드 §15](../runbooks/dagster-adoption.md#15-컨테이너-재시작-뒤-native-실행-정산)에 명시했다.
private PID namespace/exact origin만으로 old worker 사망을 증명하지 않는다.
제품/기본 STOPPED는 유지한다. C의 정정 BLOCK 원문을 보존하며 이 문서 delta의 C/A
재검토 전 finding을 FIXED로 닫지 않는다. 소비자 gate·운영 검증과 전역 IN_PROGRESS는 별도다.

## Common34 최종 독립 리뷰 보존

제품 d1aa/활성화 문서7f915의 A/C 최종 PASS와 A-P1-01·C-P2-01 FIXED를
[통합 판정](../reviews/adversarial/2026-10-16-native-incarnation-closure.md)에 기록했다.
최초 C PASS 초안은 정정 BLOCK으로 대체된 이력이며 최종 승인으로 집계하지 않는다.
원문 보관·색인 정산만 추가하며 제품/기본 STOPPED·§15 규범은 변경하지 않는다.
앞 절의 재검토 대기는 이 후속에서 해소됐지만 소비자 실제 활성화/물리 소멸 검증·
운영 E2E·CPU/RSS와 전역 IN_PROGRESS는 여전히 별도다. closure SHA의 CI는 별도 확인한다.

## 2026-10-16 다중 job 인프라 재시도 — 추가 수용 설계

공유 native retry의 정책 확대 없이 단일 센서에서 여러 명시 job의 기존 엄격 판정을 공유한다.
[설계·채택 경계](../runbooks/dagster-multi-job-retry.md)를 따른다. 기존 단일 API와
Common34 incarnation 정산은 유지하고 소비자 코드/배포는 별도다. Python 회귀·실제 SQLite·wheel·
두 독립 리뷰가 필요하며 운영 효과는 NOT_RUN이다.

후보35는 기존 단일 API의 같은 내부 판정에 다중 job dispatch만 추가했다.
로컬 전체443PASS/신규22·기존56 관련78PASS/별도 SDK1.13.24 관련161PASS와
core-only3.11 wheel·설치 바이트를 확인했다. 두 독립 리뷰·소비자 운영 채택은 후속이다.

### Common35 독립 소스 리뷰 종결

고정03396709의 두 독립 subagent FULL9 PASS/OPEN0와 후보 CI8SUCCESS를
[원문·통합 판정](../reviews/adversarial/2026-10-16-multi-job-retry-closure.md)에 보존했다.
제품 변경 없는 closure 이후 최종 문서 HEAD CI·병합은 별도이며 소비자 채택·센서 전이·
운영 복구/CPU/RSS/live의 외부 선행은 그대로다. 전역 상태를 DONE으로 올리지 않는다.

## Common36 PID1 leader clock 소스 종결

제품a34cbd8/고정5d2의 A/C 두 독립 FULL4 SOURCE_PASS·OPEN0와 QEMU 반례/검증 범위를 [최종 판정](../reviews/adversarial/2026-10-16-pid1-leader-clock-closure.md)에 보존했다. 제품·가이드 계약은 같고 원실패/cursor는 보존한다. 실제 새 lab 재드릴·소비자 pin/배포·복구/CPU/RSS는 별도이며 IN_PROGRESS를 유지한다.

## Common36 실제 격리 lab 부분 기록

[별도 역사 판정](../reviews/adversarial/2026-10-16-common36-historical-partial-closure.md)에
r2 fault1/공식 부모 실패/child1SUCCESS와 child 후 센서별2tick·중복0를 확인했다.
control SUCCESS 뒤에만 그 tick이 있어 원 동시 보호 순서는 HOLD다.
r2/r3 controller 실패와 r3 cleanup을 원형 보존하며 운영 완료·전역 DONE으로 세지 않는다.
제품/수용 기준/활성화 전제는 바꾸지 않는다.

## Common36 native 격리 통합 실제 종결

[별도15 gate 판정](../reviews/adversarial/2026-10-16-common36-native-live-closure.md)은
실제 SDK에서 control2가 childSUCCESS 이전 시작해 센서별 후속 완료2tick까지 STARTED를 유지한 뒤
release/SUCCESS·정상stop하는 순서를 검증했다. 원ARM 부분HOLD와 native 초기화실패/정리를 유지한다.
제품/테스트/규범 변경0이며 전역 IN_PROGRESS·소비자 실제 live/운영 성능/병합은 별도다.

## 2026-10-16 stdlib bytecode 빌드 준비 — 수용 설계

여러 서비스의 실제 동일 gRPC import 표본에서 stdlib93모듈의 bytecode가 없고,
site-packages54개는 유효했다. 별도 임시 prefix를 prime한 뒤 동일 import self CPU가
약3.06초에서0.93~0.94초로 줄어든 관찰이 후속 빌드 준비의 근거다.
이는 동일 prefix/단일 진단 범위이며 전체 서비스 CPU 개선 완료를 뜻하지 않는다.

- 새 opt-in 모듈 kortravelcommon.build_bytecode --stdlib만 추가한다.
  현재 이미지 interpreter의 sysconfig stdlib만 compileall 단일 worker로 준비한다.
- checked-hash·optimize0으로 만들고 site-packages/dist-packages/test/tests/idle_test와
  심볼릭 링크의 scope escape·외부 cache 목적지를 배제한다. 임의 source path 인자는 없다.
- 런타임 자동 실행·환경/격리 옵션 변경·파일 삭제·provider/DB/앱/Dagster import는 없다.
  컴파일 실패·권한 부족·잘못된 범위는 nonzero이며 빈 작업을 성공으로 숨기지 않는다.
- 작은 격리 fixture에서 실패/해시 무효화/링크/비root를 확인하고 Python 전체·문서·wheel을
  검증한다. 실제 이미지 stdlib 컴파일과 Docker 재빌드/운영 배포는 소비자 후속이다.
- 같은 immutable source를 두 독립 reviewer가 확인해야 한다. 운영 CPU·메모리·health
  효과는 소비자 실측 전 NOT_RUN이다. 기존 T-319 IN_PROGRESS를 유지한다.

## 2026-10-17 — daemon 전용 PostgreSQL 연결 재사용 설계

사용자가 CPU 개선을 요청했고 같은 공유 instance의 daemon 본체 비용을 분리 측정했다.
PG 전체 CPU는 다른 소비자의 부하도 포함하므로 daemon 원인 비율로 해석하지 않는다.
이번 범위는 Common의 명시적 opt-in 진입점과 SQLAlchemy 공식 CreateEnginePlugin이다.
공유 YAML, SDK private engine/controller, provider와 소비자 배포는 수정하지 않는다.

- Dagster1.13.24 / dagster-postgres0.29.24 / SQLAlchemy2.0.54를 검사한다.
- daemon 전용 DSN은 기존 shared DSN과 동일해야 하며 기존 plugin 쿼리를 거절한다.
  wrapper 자기 프로세스에서만 plugin을 붙이고 공식 dagster-daemon console entry point를
  exec 없이 호출한다. 원 CLI 옵션·신호/종료 흐름은 그대로 두고 환경은 finally 복원한다.
- PostgreSQL/psycopg2의 명시적 NullPool만 생성 전에 bounded QueuePool로 전환한다.
  pool_size2/max_overflow2로 세 engine의 합계 상한은12, 유휴 보관 상한은6이다.
  checkout timeout/recycle은 유한하며 원 statement/lock/connect timeout/options 및
  AUTOCOMMIT은 보존한다. 새 SET 문이나 schema feature cache를 추가하지 않는다.
- plugin은 최대3개 strong registry로 수명 동안 engine을 추적한다. checkout의 PID guard로 fork된 프로세스가
  부모 물리 연결을 재사용하지 못하게 한다. CLI 종료 후 세 engine을 명시 dispose한다.
  SDK 자체 instance.dispose는 schedule storage를 정리하지 않고 PG event dispose는
  watcher만 닫으므로 그것만으로 pool 정리를 완료했다고 간주하지 않는다.
- QueuePool TimeoutError도 SDK의 기존 연결 retry/backoff를 거치므로 한 번의
  pool_timeout을 전체 대기 상한으로 설명하지 않는다. 포화·중첩 checkout을 검증한다.
- fake DBAPI/독립 단위·wheel 설치·문서 필수 검사를 먼저 수행한다. 실제 SDK/PG daemon
  paired 검증·소비자 빌드·root CPU/RSS/신선도 측정과 두 독립 리뷰는 별도 gate다.
  이 설계 문서는 실제 성능 개선이나 소비자 채택 완료를 뜻하지 않는다.

### Common38 pool 수명 동시성 보강(2026-10-17)

- 기존1aada의 순차 busy 검사만으로는 thread checkout과 dispose 사이 경쟁을 막지 못한다.
  pool별 public connect/dispose/recreate를 직렬화하고 반환은 기존 SQLAlchemy 경로를 유지한다.
- 재생성된 새 pool은 원 scope를 계승하며 이전 pool은 퇴역한다. 다음 활성화의 옛 engine
  재생성과 이미 옛 참조를 받은 thread 모두 미등록 pool로 회생하지 못한다.
- fork 자식은 전역·pool 상속 잠금 이전에 거절한다. 자식 finally도 부모 연결 I/O를 하지 않는다.
- own SQLAlchemy2.0.54/fakeDBAPI 새6회귀: 옛1aada는5FAIL/1PASS, 수정본 포함 전체30PASS.
  실제 fork·SDK·PG는 root 전용 검증이며 소비자 전체 CPU 감소율을 뜻하지 않는다.
- CI recovery 설치에는 daemon-pool extra를 명시해 lazy PostgreSQL engine 회귀의 driver를
  제공한다. 가짜 URL은 placeholder를 구조 API로 넣고 secret scanner 예외는 추가하지 않는다.
