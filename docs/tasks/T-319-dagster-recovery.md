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
