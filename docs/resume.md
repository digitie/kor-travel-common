## 2026-10-25 — 남은 높이 지도 작업면 후보

C-MAP-01의 additive UI dev.8을 구현했다. [계약](standards/map-controls.md)과 [검증 기록](reports/2026-10-25-map-workspace.md)을 따른다. 다음은 소비자 채택과 고정 후보 두 독립 리뷰/CI이며 운영 변경은 하지 않는다.

## 2026-10-24 — 공용 지도 작업면 후보

Map Feature 작업면을 common으로 추출하고 Map/Transport/Weather 소비자에 연결한다. 종류 아이콘·30px 필터·지도/목록 탭·건수+좌표/줌·상세 오버레이를 공유한다. [계약과 검증](standards/map-controls.md). UI54·Weather 소비자 반응형2 PASS, 소비자 정확 커밋/CI/최종 리뷰는 진행 중이다. 다음은 소비자 채택 후보 고정과 남은 검증이며 운영 빌드·배포는 사용자 지정 다른 에이전트가 수행한다.

설치 산출물 CI의 옛dev.6 참조를dev.7로 갱신했다. WSL tarball 설치와 Next webpack/Turbopack 빌드 PASS이며
소비자 고정 tarball은 동일하다. Transport 순수 UI는 PR127로 main34f8fab에 반영했고 Map live UI 검증은 진행 중이다.

## 2026-10-23 — workspace 갱신 CPU 후보

공유 daemon의60초 metadata 갱신에서 JSON/serdes·job snapshot 지문 비용을 관찰했다.
[가이드 §20](runbooks/dagster-adoption.md#20-daemon-workspace-metadata-갱신-주기)의 명시적
180초 opt-in 후보는 원240초 실패 유예·CLI·pool·신호 처리를 유지한다. 원SDK 경계와
기존 pool 집중49 PASS/Ruff PASS는 작성자 검증이며 전체·wheel·독립2리뷰·CI는 진행한다.
소비자 배포/CPU·RAM 저감·작업 신선도 수용은 아직 NOT_RUN, 전역T-319 미완이다.

## 2026-10-18 — Common38과 native webserver 통합 후보

이 후보는 PR38의 061008f와 main f914873(Common41 제품89291f3)을 일반 merge한다.
daemon-pool/정식 daemon CLI/SQLAlchemy plugin과 native webserver/정식 alias를 한 wheel에
보존한다. workflow는 두 선택 extra를 함께 검증하고 기존 daemon profile의 SDK .24,
SQLAlchemy2.0.54를 유지한다. 기존 외부64 package entry는 같고 webserver18개만 추가됐다.
원92d pool 소스와 main webserver·주소 소스는 각각 byteexact다.
최종 wholewheel·독립2리뷰·CI·소비자 통합은 이 후보의 정확 HEAD별로 정산한다.
운영 수용·Daemon OFF·Track1·2 우선 및 그 후 collector CPU/RSS 순서는 바꾸지 않는다.
아래 기록은 각 시점의 이력이며 main 기반41 wheel의 daemon 부재 설명도 당시 상태다.
검증: Python3.12.13 locked 전체599 PASS(156.00초), compile·Ruff PASS,
문서777개/2991targets·plan109 오류0. wholewheel63,151B/SHA1abf0547…,
Python16개/RECORD23행/두 CLI·plugin 등록과 core lazy import를 별도 설치에서 확인했다.
작성자는 독립 리뷰어가 아니며 최종2리뷰·CI·소비자/운영 수용은 별도다.

## 2026-10-18 — native 제출 timeout 정책 보존

제품89291f3은 native Pool.recreate로 creator/options/connect listener를 계승한다.
운영 조합 .24/.29.24/SQLAlchemy2.0.54 및 .25에서 SQLite51/전용PG58, locked565 PASS,
[가이드](runbooks/dagster-idempotent-launch.md)에 원a68 timeout1FAIL·후속 wheel을 보존했다.
다음은 root의 독립2리뷰/최종CI·소비자 수용과 미머지 Common38 wholewheel 통합이다.
이 main 기반 wheel에는 daemon pool이 아직 없으므로 기존 daemon wheel을 대체하지 않는다.
운영·provider·worker·Daemon은 NOT_RUN이며 아래는 시점별 기록이다.

## 2026-10-18 — PostgreSQL 제출 연결 fencing

두 번째 P1(lock session 유실 뒤 stale enqueue)을 제품a68d049에서 native run-storage
동일 물리 connection adapter로 보강했다. 두SDK SQLite48/ownedPG53, locked562 PASS와
새 wheel14source/21RECORD·정식 console alias를 작성자가 확인했다.
[가이드](runbooks/dagster-idempotent-launch.md)에 원 실패와 먼저 남을 수 있는 native
eventlog 시도/권위 run상태를 구분했다. 다음은 post-fix 독립2리뷰·최종CI·소비자 수용이다.
운영·실provider·worker·Daemon 실행은 없으며 기존 OFF 정책을 유지한다.

## 2026-10-18 — native 제출 경합 보강

초기23e의 독립 P1(run 한 개여도 stale submit이 STARTED를 QUEUED로 덮음)을 수용해
제품2704830에서 fresh status/submit을 run별 OS/session lock으로 직렬화했다.
SQLite .24/.25 각44, 전용 ownedPG 각45+추가3, locked 전체558 PASS와 새 wheel 설치·14source/20RECORD 검증을 작성자가 확인했다.
[가이드](runbooks/dagster-idempotent-launch.md)에 원 실패·명시 busy 재시도·지원 제한을 남긴다.
다음은 post-fix 두 독립 리뷰와 최종 CI/소비자 gate다. 운영·provider·Daemon은 미실행이다.

## 2026-10-18 — native 멱등 제출 후보

[Common41 가이드](runbooks/dagster-idempotent-launch.md)의 opt-in schema/같은 프로세스 CLI와
native 영속 run ID를 구현했다. .24/.25 각41 집중 PASS, locked553 PASS는 작성자 범위다.
UNKNOWN 원문은 보존한다. 다음은 최종 전체·CI와 작성자를 제외한 두 독립 FULL 리뷰,
소비자 pin/BFF/UI 연결이다. 운영·provider·daemon은 실행하지 않았고 OFF 정책은 유지한다.
아래 기록은 각 시점의 이력이다.

## 2026-10-18 — Common38의 최신 main 정합 후보

PR38 원92d5cf1에 main27cd146을 별도 branch에서 일반 merge했다.
daemon-pool과 reverse-address extra를 합치고 workflow에서 둘을 설치한다.
기존92d의 의존 version/artifact와 daemon pool/CLI 소스, main의 주소 모듈·테스트는
바이트 그대로 보존했다. lock은 기존92d package64개에 main의 고정 VWorld package1개만
추가했다. 격리된 locked 환경에서 관련72 PASS·Ruff·문서 링크·plan을 확인했다.
새 통합 후보의 두 독립 리뷰·CI·원격 PR38 반영/병합은 아직 후속이다.
기존 운영 수용·daemon OFF·Track1·2 선행과 수집기 최적화 순서를 변경하지 않는다.

## 2026-10-18 — 주소 갱신 summary 후속

제품522525a의 두 독립 FULL SOURCE PASS·OPEN0와 CI8 SUCCESS를
[최종 원문·정산](reviews/adversarial/2026-10-18-address-summary-closure.md)에 보존했다.
전체514·새 wheel28·도구334/3SKIP 범위를 구분한다. 소비자 새 pin·CI/UI와 운영은 별도다.
아래 구현 당시 대기 문장은 당시 이력이다.

Transport86 r2의 현재 원천 제외 후에도 최근 정상 확인 시각이 남는 P2를 공통 엔진에서 보정한다.
현재 source와 좌표가 같은 결과만 MAX에 포함하고 과거 행·동일 좌표 마지막 정상일은 보존한다.
작성자 반례 5 FAIL→주소 엔진 28 PASS. 전체 검증·CI·두 독립 리뷰 및 Weather/Transport pin 갱신이
다음 단계다. 운영 적용과 수집기 CPU/RSS 개선 완료로 해석하지 않는다.
사용자 순서에 따라 Track1·2 전체 완료 뒤 수집기 최적화를 진행하며 Daemon OFF는 유지한다.

## 2026-10-16 — Common36 native 격리 복구 실제 완주

[새 native 실제 종결](reviews/adversarial/2026-10-16-common36-native-live-closure.md)은 원 SDK1.13.24/Common5d2에서
bootstrap 직렬 초기화→fault1→공식 부모 실패→child1SUCCESS→control2 STARTED를 유지한 센서별2tick→release/SUCCESS2→정상stop을 검증했다.
원 ARM 부분 증거와 native 초기화 실패/cleanup은 보존하며 과거 결과를 바꾸지 않는다.
이번15 gate PASS는 WSL native amd64 논리 통합 범위다. 소비자 운영/live UI·CPU/RSS·병합과 전역T319는 별도다.
아래는 각 시점의 이력이다.

## 2026-10-16 — Common36 실제 격리 lab 부분 증거

[역사 부분 검증](reviews/adversarial/2026-10-16-common36-historical-partial-closure.md)에
r2 fault1→공식 부모 FAILURE→child1SUCCESS와 사후 센서별2tick/추가child0를 보존했다.
control들은 그 tick 전에 이미 SUCCESS여서 원 동시 보호 LIVE gate는 HOLD다.
r2 controller 실패·r3 timeout/backgroundOOM·별도 cleanup을 성공으로 덮지 않는다.
제품5d2/소스 A·C PASS는 그대로이며 native amd64 계획은 조사만 했다.
다음은 남은 동시 보호 검증 계획 검토·Weather 실제 live UI34/소비자 gate다.
전역 T-319 IN_PROGRESS·PR36 draft/미병합을 유지한다. 아래는 각 시점의 이력이다.

## 2026-10-16 — Common35 기준선 문서 통합

## Common36 소스 리뷰 종결 (2026-10-16)

PID1 leader clock 고정5d2/제품a34cbd8의 두 독립 A/C FULL4 SOURCE_PASS·OPEN0와 후보CI8SUCCESS를 [통합 판정](reviews/adversarial/2026-10-16-pid1-leader-clock-closure.md)에 보존했다. 실제 Common36 lab 재드릴·소비자 이미지/활성화·운영 효과/병합과 전역T319는 후속이다. closure는 제품/규범 변경0이다.

Common34 최종4ad615e 위로 Common35를 다시 올려 두 리뷰 원문·통합 보고서와
활성화 전제 §15를 함께 보존했다. 제품/테스트/의존성 packages tree는 검토03396709와
동일하다. 초기 closure58d2426의 CI8SUCCESS는 그 SHA의 이력이며 새 HEAD CI는 별도다.
PR35는 Common34 feature를 base로 하는 draft를 유지한다. Common34 병합 뒤 최종 main
대상/정확 source pin·소비자 전이/실제 복구·live gate를 따로 정산한다. 운영 변경0이다.

## 2026-10-16 — Common35 다중 job 재시도 소스 리뷰 종결

고정03396709의 두 독립 subagent FULL9 PASS/OPEN0와 CI8SUCCESS를
[통합 보고서](reviews/adversarial/2026-10-16-multi-job-retry-closure.md)에 보존했다.
이번 원문/기록 종결은 제품을 바꾸지 않는다. 다음 작업은 최종 문서 HEAD CI 확인과
PR35 병합 판단이며, 소비자 pin·센서 전이·실제 복구/성능/live는 외부 선행이다.
T-319 전역 상태는 IN_PROGRESS다. 아래 문단은 각 작성 시점의 이력이다.

## 2026-10-16 — Common34 독립 리뷰·문서 정산 완료

제품 d1aa와 문서7f915의 A/C 독립 최종 PASS·열린 P0/P1/P2 0을
[최종 판정](reviews/adversarial/2026-10-16-native-incarnation-closure.md)에 보존했다.
A의 외부 launcher P1과 C의 활성화 전제 P2는 FIXED다. C의 철회된 PASS 초안·정정
BLOCK·후속 FIXED 원문은 모두 바이트 그대로 남겼고 초안을 최종 승인으로 세지 않는다.
이번 closure는 제품/§15 규범 변경0이다. 새 closure HEAD CI 확인과 소비자 운영 gate는
별도이며 전역 T-319 IN_PROGRESS·기본 STOPPED를 유지한다.

## 2026-10-16 — Common34 활성화 전제 문서 보완

C의 정정 리뷰 C-P2-01을 수용해 [가이드 §15](runbooks/dagster-adoption.md#15-컨테이너-재시작-뒤-native-실행-정산)에
singleton/exclusive origin·overlap 미지원·serial 교체의 구 init/worker/cgroup 소멸 증거를
활성화 전제로 명시했다. 제품·기본 STOPPED·핀·이미지는 d1aa와 같다.
새 immutable 문서 delta의 C-P2 재검토와 A 독립 재검토·최종 CI가 후속이며,
C 최초 PASS 초안을 최종 승인으로 세지 않는다. 소비자 운영 검증은 별도다.

## 2026-10-16 — 다중 job 인프라 재시도 후보

기존 단일 retry factory와 같은 엄격 판정을 공유하는 다중 factory를 추가했다.
최대100개 초기 failure page·tick budget/cursor를 공유하고 요청은 한 tick 최대1개다.
[가이드](runbooks/dagster-multi-job-retry.md)를 따른다. Python443/관련78·별도1.13.24 관련161,
core-only3.11 wheel/설치 source를 확인했다. 두 독립 리뷰·CI·소비자 pin/센서 전이·
실제 복구/CPU/RSS/live는 후속이며 중앙 native 설정과 Common34 정산 소스는 유지했다.

## 2026-10-16 — proxy 환경 우회 P2 후속 수정

독립 리뷰의 실제 loopback CONNECT/정상 오인 반례를 반영해 새 gRPC 채널에서 proxy를
명시 비활성화했다. 전체338PASS/새60PASS·별도1.13.24 60PASS와 새 wheel 설치/
proxy 격리 회귀를 확인했다. 원문·초기 manifest는 보존하고 post-fix 두 리뷰·CI·
소비자/운영 채택은 아직 후속이다. 기존 legacy API의 동작은 그대로다.

## 2026-10-16 — health 조회와 복구 분리 후보

Common31 phase와 Common32 strict HTTP를 보존한 feature 통합점에서 새 gRPC live/ready
API·quiet CLI를 추가했다. 기존 API는 유지하고 새 두 RPC는 하나의 논리4초를 공유한다.
health는 DB/run/프로세스 변경을 하지 않는다. 소비자 Manager override의 reaper/kill
제거·복구 경계 이관과 실제 적용은 별도 작업이다.
[가이드 §14](runbooks/dagster-adoption.md#14-생존정의-준비-조회와-복구-동작-분리)를 따른다.
로컬 wheel/합성 CLI 수치는 운영 절감 효과가 아니다. 두 독립 리뷰·CI·소비자 채택은 후속이다.

## 2026-10-16 — HTTP 상태 줄 부정 응답 보강

초기 후보의 두 독립 리뷰가 상태 코드 뒤 SP 누락을 건강한 응답으로 오인하는 P2를 재현했다.
split 결과3요소를 요구하고 빈 이유 문구의 정상 응답은 유지했다.
전체 Python208PASS(신규48포함)·ruff·새 core-only wheel 설치/동일source·실제CLI3조건을 확인했다.
고정 post-fix의 두 독립 재검토와 CI·소비자 채택/실측은 후속이며 이전 결과를 덮지 않는다.
[계약](runbooks/http-health-probe.md)을 따른다.

## 2026-10-16 — 경량 HTTP 생존 점검 후보

[T-319](tasks/T-319-dagster-recovery.md)의 core-only HTTP 점검 함수·CLI와
[적용 가이드](runbooks/http-health-probe.md)를 추가했다. Python204PASS(신규44포함),
core-only wheel 정상 설치·실제 loopback CLI200/503·ruff·문서 링크/plan·도구336PASS/1SKIP를 확인했다.
두 독립 리뷰·소비자 exact pin/이미지·운영 healthy/CPU/UI는 후속이다.
이 후보의 기준 main은8d04353이며 별도 고정 phase 예약 PR을 포함했다고 주장하지 않는다.
소비자는 예약 개선을 보존하는 통합 commit을 다시 고정하고 관련 회귀를 수행해야 한다.

## 2026-10-15 — 고정 phase 예약 분산 독립 리뷰 완료

고정 `41b672c`의 독립 FULL 2인 PASS / OPEN 0과 CI 8개 SUCCESS를 확인했다.
[원문·판정](reviews/adversarial/2026-10-15-scheduling-phase.md)을 후속 문서로 보존한다.
제품 Python 바이트와 Weather 소비자 pin은 그대로다. 소비자 운영 gate를 이 소스 리뷰로
대체하지 않으며 실제 배포·첫 tick·수집량·freshness·CPU/RSS·복구·live는 후속이다.
archive commit의 문서 gate와 최종 CI 확인 후, 소비자 운영 결과와 함께 병합을 판단한다.

## 2026-10-15 — 고정 phase 예약 분산 후보

T-319에 Dagster import 없는 `staggered_cron`과 적용 가이드 §13을 추가했다.
같은 일일 예약 횟수·간격·자정/월경계·DST 한계·coalescing 보존을 실제 SDK 달력으로
검증했고 Python 전체230PASS·core-only wheel 검증을 마쳤다. 두 독립 리뷰·CI·
소비자 pin/실제 수집량·freshness·운영 RSS/CPU 검증은 후속이며 아직 병합하지 않는다.
[검토 범위](reviews/adversarial/evidence/2026-10-15-scheduling-phase-manifest.md)를 따른다.

## 2026-10-06 — Map·PinVi 공통 Dagster 구현·재구축·live·머지 완료

[Common #28](https://github.com/digitie/kor-travel-common/pull/28) → [Map #1303](https://github.com/digitie/kor-travel-map/pull/1303) → [PinVi #576](https://github.com/digitie/pinvi/pull/576) 순서로 병합했다. Common·Map은 merge commit, PinVi는 main ruleset의 squash-only·linear history 정책에 따라 squash로 병합했다. PinVi 재구축 원본0058369와 검증 HEAD92d0f40는 remote tags codex/pinvi-map-runtime-20261006·codex/pinvi-map-reviewed-20261006 및 유지한 feature branch에 원본 이력을 보존했다. 저장소 설정은 변경하지 않았다. 최종 문서 포함 HEAD의 필수 CI, Common·Map main ancestry와 PinVi 보존 참조, 병합 tree 일치를 확인했다. 실제 paired 재구축, 두 독립 FULL 제품 리뷰·가이드 리뷰·최종 문서 리뷰, Chromium/Firefox×Map/PinVi live UI4건·8캡처, ACL40·D1 11건·D2 normal/attempt0·소유 fixture 정리·잔존0 검증을 완료했다.

머지 후 운영 API/UI/Dagster 여섯 이미지의 healthy 상태·설치 코드·배포 source·committed transaction이 기존 성공 증거와 같음을 실제 read-only 재확인했다. 최종 제품 Common a960bdb/Map1a3c467/PinVi0058369에 문서만 추가됐으며 재구축·장애 주입을 머지 HEAD에서 새로 실행한 것으로 집계하지 않는다. 격리 Map native raise/crash/stall·동시 정상 run·수동 복구는 관련 설치 코드/버전 불변 범위에 한정한다. 공유 운영 worker 장애 주입·운영 RSS 감소율은 미실측이다.

T-319/T-216의 외부 소비자 확대·운영 RSS 등 전역 잔여는 IN_PROGRESS로 유지한다. Common PNG는 UTF-8-only 검사 계약에 따라 고정 Map commit·Common Git history에 원본을 보존하며 검사 정책을 완화하지 않았다.

[머지 후 실제 상태 증거](reviews/adversarial/evidence/map-health-2026-10-05/final-postmerge-runtime-attestation.json), [가이드·실패·리뷰·수용 이력](reviews/adversarial/2026-10-05-map-health-closure.md). 아래 문단은 각 작성 시점의 이력이며 이 절이 최신 상태다.

## 2026-10-06 — Map·PinVi 공통 Dagster 실제 재구축·live 수용 완료

Common a960bdb, Map 1a3c467, PinVi 0058369의 제품113파일 두 독립 FULL 리뷰와 가이드 리뷰를 통과했다. 공용 Python은 bounded HTTP·경량 child health·실행 복구 정책을 제공하며 앱의 operation/lease/claim·비멱등 쓰기 계약을 유지한다. 요청별 응답4MiB/10초와 정리50ms, DB pool/step 제한·100개 batch를 적용했다. Map tick 조회의 오래된 batch history 정렬 지연은 상태 조건을 명시하여 native indexed LIMIT 경로로 줄였고 실제 summary/UI 복구를 확인했다.

운영 paired 재구축과 설치 source·관련 Common bytes·실제 이미지 identity·여섯 서비스 healthy를 검증했다. Chromium/Firefox×Map/PinVi 실제 UI4건과 캡처8개를 직접 확인했다. ACL40·D1 11건·D2 정상 수용/validator·소유 fixture purge1/7·잔존0/ACTIVE없음/BLOCKED없음까지 통과했다. Common의 ESM export를 읽기 위한 type=module은 별도 테스트 이미지 package.json에만 추가하고 실제 마지막 layer/semantic delta를 증명했다. 앞선 모든 실패·초기 BLOCK와 수정 후 PASS 원문은 보존한다.

격리 native Dagster에서 실제 raise·worker crash·stall/timeout 뒤 수동 재시도와 동시 정상 job을 확인했다. 최종 Map 운영 Dagster 이미지의 관련 설치 코드와 버전이 이전 격리 이미지와 같은지, 실제 최종 이미지 ID가 배포 기록과 맞는지 독립 검증했다. 이 결과는 해당 불변 코드 범위에 한정해 이어받는다. 공유 운영 DB의 worker 장애 주입이나 운영 RSS 감소율 실측으로 설명하지 않는다. 유한 응답·batch·동시성 구조와 합성 메모리 측정은 운영 RSS와 구분한다. 기존 인간 dirty checkout·외부 transport/HAProxy 후속은 보존한다.

다음 한 작업은 문서 포함 exact HEAD CI 통과 후 Common #28 → Map #1303 → PinVi #576 순서로 merge commit 병합하는 것이다. 제품 Git pin의 ancestry를 보존한다. 이 절이 현재 상태이며 아래의 진행 중/NOT_RUN 문단은 이전 시점의 이력이다.

[실제 검증·리뷰 원문과 실패 이력](reviews/adversarial/2026-10-05-map-health-closure.md), [공통 적용 가이드](runbooks/dagster-adoption.md).

## 2026-10-05 — metadata map의 serdes marker 차단 (진행 중)

99d8 고정 후보 재리뷰에서 library versions와 pointer dictionary의 typed marker가 경량 검증을 우회하는 P2를 확인했다. 다섯 reserved serdes marker를 거부하되 정상 Map default 이름 __repository__는 허용한다. 실제 isolated CLI 정상 default repository와 두 공격 응답, 모든 marker 회귀를 포함한 health65 PASS를 확인했다. 이전99 전체146 PASS는 이전 소스 증거이며 새 후보의 두 독립 FULL 리뷰·CI·운영 재구축/live가 남았다. [가이드 §10](runbooks/dagster-adoption.md#10-code-server-자식-로딩을-확인하는-경량-건강-점검)에 지원 경계를 보완했다.

## 2026-10-05 — 경량 health의 표준 metadata profile 보강 (진행 중)

독립 리뷰에서 e0b5e31 후보의 null/미등록 code pointer와 executable/entry point 잘못된 타입이 실제 Dagster 역직렬화에서는 거부되지만 경량 CLI에서는 정상 처리되는 P2를 확인했다. 기존 PASS/BLOCK 판정은 그대로 보존한다. module/file/package pointer와 nullable metadata 타입을 검증하고, stateful/custom typed metadata·알려지지 않은 필드는 실패로 판정한다. 지원 profile과 확장 방법은 [가이드 §10](runbooks/dagster-adoption.md#10-code-server-자식-로딩을-확인하는-경량-건강-점검)에 명시했다. schema 변경 후 전체 Python139 PASS, 실제 isolated CLI 7건을 포함한 health51 PASS를 각각 확인했으며 합산하지 않는다. 새 고정 후보의 두 독립 리뷰·CI·운영 재구축/live가 남았다.

## 2026-10-05 — Map code-server의 빈 reply 오인 방지 (진행 중)

T-319의 공용 `dagster_health`는 proxy SERVING 뒤 실제 `ListRepositoriesResponse` protobuf/JSON을 검증한다. Map 최신 main의 substring 점검이 빈/잘못된 reply를 정상으로 판정한 독립 적대 리뷰 반례를 반영했다. 전체 Dagster import 없이 설치된 생성 protobuf를 사용하며 각 RPC 4초·수신 4MiB·channel 정리와 fail-closed를 적용한다. [가이드 §10](runbooks/dagster-adoption.md#10-code-server-자식-로딩을-확인하는-경량-건강-점검)에 소비자 채택·재시작 정책 경계를 기록했다. 새 고정 후보 2인 리뷰·CI·실제 paired 재구축/live는 진행 중이다.

# 현재 상태와 다음 한 작업

## 2026-10-05 — Map·PinVi HTTP 최종 독립 리뷰

고정1f8e339의 두 독립 FULL 리뷰 PASS와 모든 finding FIXED, Python95/HTTP26·strict 타입·wheel·문서 도구 검증을 [최종 판정](reviews/adversarial/2026-10-05-map-http-closure.md)에 보존했다. 소비자 실제 재구축/live 및 공통 PR28 exact CI gate는 후속이다.

## 2026-10-05 Map·PinVi HTTP 후보

[T-319](tasks/T-319-dagster-recovery.md)의 HTTP 응답 cap·deadline·별도 정리 예산과 dev 의존을 보강했다. 신규 26개 HTTP 회귀가 통과했다. 두 독립 사전 리뷰 원문은 보존하고 고정 후보 전체 post-fix 리뷰·CI는 진행 중이다. 소비자 재구축·live는 해당 저장소 검증이며 현재 완료로 표시하지 않는다.


현재 상태의 정본이다. 정책은 [AGENTS](../AGENTS.md), 문서 선택은 [문서 지도](README.md), 상세 상태·선행은 [task 원장](tasks.md)을 따른다. 마지막 갱신: 2026-10-05, Codex.

## 현재 상태

2026-10-04 사용자 요청: [T-319](tasks/T-319-dagster-recovery.md) Python 실행 복구와 [T-216](tasks/T-216-dagster-operations.md) 공용 Dagster UI 코드·2인 리뷰·live UI·회귀·코드 후보 CI가 완료되었다. [최종 리뷰](reviews/adversarial/2026-10-04-dagster-recovery.md), common PR #24와 weather PR #72에 증거를 보존했다. 다른 소비자 확산과 운영 배포는 미실행이다.

사용자 요청 T-215 공용 로그인·메뉴·6개 실제 프로젝트 테마 예시를 구현했다. 최신 React/Next의 WSL 빌드·단위·tarball 설치·브라우저 검증, 두 독립 post-fix 리뷰와 후보 CI가 통과했다. [최종 리뷰](reviews/adversarial/2026-09-29-t215-wsl-post-fix.md)와 [PR #23](https://github.com/digitie/kor-travel-common/pull/23)이 evidence다. 기존 T-301 작업 checkout과 PR #22는 보존했다.

## 다음 한 작업

common #24·weather #72는 main에 머지되었다. transport 채택을 위한 Python `430a9e9`와 UI `0.1.0-dev.2`의 두 독립 리뷰·CI·격리 소비자 live UI가 통과했다. [common PR #25](https://github.com/digitie/kor-travel-common/pull/25)와 [최종 코드 판정](reviews/adversarial/2026-10-04-transport-adoption-closure.md)에 증거를 보존했다. transport PR #67은 머지 완료했다. 운영 shared coordinator 전환·worker kill·RSS 측정은 NOT_RUN이다. T-301 원본 변경은 보존한다.

## 시작 파일과 검증

[T-215](tasks/T-215-shared-login-menu.md), [예시 실행 안내](../packages/ui/examples/README.md), [최종 리뷰](reviews/adversarial/2026-09-29-t215-wsl-post-fix.md)를 확인한다. 일반 명령은 [개발 환경](dev-environment.md#6-검증-명령-사다리), branch·리뷰·merge는 [agent workflow](runbooks/agent-workflow.md)를 따른다.

## 유지할 제한과 외부 선행

- common 저장소만 수정한다. npm/PyPI에 게시하지 않는다. 공용 라이브러리는 GPL-3.0-or-later이며 기존 외부 원문의 출처·고지는 보존한다.
- 실제 소비자 build/e2e·MDX compile/render·baseline 등록은 해당 이관 task 소유다. Airport dark 예제는 예상 FAIL이며 T-431 외부 gate를 유지한다.
- T-020·T-021은 common의 GPL 결정·요청 문서 완료다. 외부 LICENSE 반영·소비자 채택을 완료로 세지 않는다. T-420·T-430·T-443과 pinvi mobile 예외 등 외부 상태는 각 상세 task에서 확인한다.
- 소비자 저장소·registry·외부 CI를 실행하지 않은 검증은 `NOT_RUN`으로 남긴다. 과거 조사 수치와 후보 값을 현재 정상값으로 사용하지 않는다.

## 인계 자료

[통합 계획](plan/integration-plan.md) · [architecture](architecture/README.md) · [standards](standards/README.md) · [ADR](adr/README.md). 역사·survey 전체를 시작할 때 통독하지 않는다.

## 2026-10-05 geo 대시보드 후속

[T-216](tasks/T-216-dagster-operations.md)의 `dev.3` 후보: 목록/상세·tick·검색·50행 pagination. 기존 작업 branch를 보존한다. [최종 판정](reviews/adversarial/2026-10-05-geo-common.md)에 두 코드 PASS·69 Python/48 UI·소비자 live와 실패 수정 원문을 보존했다. common PR26·Geo PR570의 문서 포함 최종 checks가 통과한 뒤 순서대로 merge한다. 운영 배포·RSS 측정·다른 소비자 확산은 후속이며 완료로 세지 않는다.

## 2026-10-05 PinVi 채택 후속

Common dev.6의 두 독립 post-fix PASS, UI50·tarball smoke와 PinVi 실제 N150 live 4PASS를 [최종 판정](reviews/adversarial/2026-10-05-pinvi-common.md)에 보존했다. [Common #27](https://github.com/digitie/kor-travel-common/pull/27)과 [PinVi #575](https://github.com/digitie/pinvi/pull/575)에 최종 CI/머지 게이트를 결박했다. 이후 운영 검증은 별도 배포 요청에서 진행한다. Common #26/Geo #570은 merge 완료. 운영 shared daemon/worker kill/RSS는 NOT_RUN이다. 기존 T-301 원본 변경은 보존한다.
