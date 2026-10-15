# Dagster gRPC 생존·정의 준비 조회 최종 리뷰

- 실행 ID: COMMON33-GRPC-HEALTH-CLOSURE-20261016. Coordinator: root.
- 상태: COMPLETE. 최종 verdict: PASS / P0·P1·P2 OPEN 0.
- 최초 FULL: review3ed16d1050bb55b87cc5005c11df3490d88205b6, 제품6ffc243cd590fa0bd09a819269dc18edecda4264, baseb76623266446a3c1e5729e5bc6876a2638af9a27.
- post-fix: reviewd247d19299fddc79f33f3192980111419f886163, 제품1511e3d601ee83dcc3103fb9f45f2cf5754110e7.
- 범위: [FULL manifest](evidence/2026-10-16-grpc-health-isolation-manifest.md)의14파일과 [post-fix manifest](evidence/2026-10-16-grpc-health-proxy-postfix-manifest.md)의9파일.
- 이 closure는 원문·disposition·검증 범위·index만 기록하며 제품·규범·소비자 pin을 바꾸지 않는다.

## 독립 원문

두 전문 reviewer는 같은 immutable 기준선·manifest에서 검토했다. 두 단계 모두 상대 원문을 읽지 않았으며, root는 원문이 고정된 뒤 전체를 읽었다. 아래 파일은 인계 원문과 SHA256이 동일하다. 실제 시각·격리 clean·전달 요청·실패와 한계는 각 원문에 보존한다.

| 단계 | 전문 영역·판정 | 원문 SHA256 |
| --- | --- | --- |
| [초기 A](evidence/2026-10-16-grpc-health-reviewer-a.md) | RPC·parser·deadline·실패 격리 / CONDITIONAL·P2 1 OPEN | b356b82804b836a7e064f6019a9d948f3e579182eb855b5171beed299065a88b |
| [초기 B](evidence/2026-10-16-grpc-health-reviewer-b.md) | core/선택 dependency·패키징·CLI·호환 / PASS·신규0 | af078856f5d087c9e0713b7f0551d34ca941f1dacd5c60f4730a50fc77fba018 |
| [수정 A](evidence/2026-10-16-grpc-health-post-fix-reviewer-a.md) | 동일9파일·실제 설치 proxy 반례 재검증 / PASS | 03d7d65cd4da13f970344847e819e1a065ae73efd1bb31a7970d21e8e534e129 |
| [수정 B](evidence/2026-10-16-grpc-health-post-fix-reviewer-b.md) | 동일9파일·빈 환경 설치·독립 RED/GREEN / PASS | b05b199826ab2ed287fcc39304a440966302672177cce85a9e73c0565bda12a2 |

## Finding과 disposition

A-P2-01은 loopback 문자열만으로 실제 target 귀속을 보장하지 못하는 문제다. grpc_proxy가 닫힌 target 요청을 다른 건강한 서버로 터널하면 false healthy가 되고, 거절 proxy는 정상 target을 실패·비quiet로 만들었다. B는 최초 FULL에서 이 경계를 놓쳤음을 보존하고 post-fix 때 자기 옛 wheel로 같은 유형의 RED를 독립 재현했다.

상태 FIXED: 새 채널에 grpc.enable_http_proxy=0을 명시했다. retries0·논리4초·수신4MiB·parser·wire profile·기존 legacy API는 유지한다. A는 실제 설치 wheel의8조건, B는 별도 실제 설치21조건에서 proxy 연결0·정확 target·quiet를 확인했다. 회귀는 proxy backlog와 handler 종료까지 확인하고 닫힌 target의 bind socket을 유지한다. 추가 P1/P2 및 미해결 finding은 없다.

## 검증과 한계

- 작성자 수정 후 전체 Python338PASS, 신규60PASS 및 별도 Dagster1.13.24 신규60PASS, Ruff·wheel 설치·pip check PASS.
- 독립 A: 관련125PASS, 실제 설치 proxy8조건 PASS. 독립 B: 관련125PASS(1.13.25),60PASS(1.13.24), 새4개 빈 환경 설치/pip check·wheel Python8파일 일치, 기존 독립35조건과 proxy21조건 PASS. 서로 겹치는 결과를 합산하지 않는다.
- 새 wheel SHA63bf13f3d16689b6ae877edf57f19897eec81e50d846ce077ff6b22207dcfcfb.
- 초기 proxy RED·원문, B의 최초 무핀 미지원1.13.26 결과2FAIL/111PASS, A의 초기 fixture setup 오류를 그대로 보존한다. 지원 버전 확인 뒤 성공한 결과와 구분한다.
- Common31과32는 feature 통합 기준선에 함께 포함됐으며 각각의 [예약 분산](2026-10-15-scheduling-phase.md)·[HTTP 조회](2026-10-16-http-health-closure.md) 독립 판정과 제품 바이트를 보존한다.
- [적용 가이드](../../runbooks/dagster-adoption.md#14-생존정의-준비-조회와-복구-동작-분리)의 소비자 exact pin/lock·이미지·effective HC·복구 경계 전환은 별도 gate다. 새 liveness는 정의/worker/DB 준비를 보장하지 않는다.
- 논리4초는 Python bootstrap/import/decode/close를 강제 선점하는 process timeout이 아니다. x86 합성 cold 표본에서 동등 ready CPU/RSS 절감은 입증되지 않았다. 실제 ARM64 CPU/RSS·서버/DB 비용·장애 복구·소비자 UI는 NOT_RUN이며 이 라이브러리 소스 판정으로 대체하지 않는다.
- 이 closure의 문서 링크713개/로컬 대상2849개 오류0, task109개 metadata/DAG 오류0, 도구337개 중336PASS/플랫폼1SKIP(65.114초), diff 검사를 통과했다. 최종 CI는 해당 commit에서 다시 확인한 뒤 병합한다. 운영/외부 HTTP/SSH/DB/Docker 변경0이다.
