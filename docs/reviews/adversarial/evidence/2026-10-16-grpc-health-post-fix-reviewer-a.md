# Common33 proxy postfix 독립 리뷰 A

- 실행 ID: COMMON33-PROXY-POSTFIX-A-20261016.
- 시작(격리 checkout 생성): 2026-10-15T20:56:11.865024+00:00.
- 종료: 2026-10-15T20:58 UTC.
- 전문 영역: RPC target 귀속·proxy·quiet·논리 deadline·실패 격리.
- review HEAD `d247d19299fddc79f33f3192980111419f886163`, 제품 `1511e3d601ee83dcc3103fb9f45f2cf5754110e7`, base `3ed16d1050bb55b87cc5005c11df3490d88205b6`.
- manifest `docs/reviews/adversarial/evidence/2026-10-16-grpc-health-proxy-postfix-manifest.md`, SHA256 `67a002aa4b2fb394c23eb11613613b85d5db72df1b141604ae7f6439a928d5ba`.
- 범위: manifest 포함 9파일 전체 delta와 초기 FULL 리뷰 문맥. 별도 detached worktree 시작·종료 clean, 검증 후 제거 완료.
- 요청: 고정 postfix를 독립 검토하고 설치된 새 wheel에서 closed-target→다른 healthy proxy 반례와 direct target/quiet를 재실행해 기존 P2를 닫는다. 제품/운영 수정·상대 리뷰 원문 접근은 하지 않는다.
- 판정: **PASS / P0·P1·P2 OPEN 0**.

## A-P2-01 FIXED

`grpc_health._probe`의 제품 delta는 채널 옵션 `('grpc.enable_http_proxy', 0)` 한 줄이다. 기존 retries0·4MiB cap·공유 논리4초·response/parser/profile·legacy 함수/CLI는 변경하지 않았다.

독립 검증은 monkeypatch 없는 **실제 설치 wheel**의 `python -I -m kortravelcommon.grpc_health`를 사용했다. wheel SHA `63bf13f3d16689b6ae877edf57f19897eec81e50d846ce077ff6b22207dcfcfb`, 설치 site-packages의 실제 모듈 SHA `2aa9cccee16c65d04590c4c4ef2c2c7404ea7c27ef932df731bb84a7398a8f15`가 immutable source와 일치함을 직접 확인했다.

자기 loopback CONNECT proxy는 연결을 받으면 **다른 합성 건강 서버로 터널하도록 실제로 준비**했다. target 포트는 bind만 한 socket을 유지해 닫힌 상태를 보장했다. 기본 direct healthy0/closed1, grpc_proxy/http_proxy/https_proxy 각각 healthy0/closed1의 **8개 실제 subprocess 조건 모두 예상 종료 및 stdout/stderr0**이었다. proxy handler 종료 뒤 accept backlog까지 확인했으며 TCP 연결은 0이었다. 따라서 원 HEAD에서 재현한 closed-target false healthy와 proxy 오류 stderr 경로가 새 설치본에서 차단된다. 실제 서버/운영 proxy 환경이 아니라 합성 로컬 모형이다.

재현: `common33-postfix-installed-proxy-review-a-20261016.py`.
결과: `common33-postfix-installed-proxy-review-a-20261016.json`, SHA256 `951be0fb59c7daee244b7a972a86fe8a93e8ee3a5a442d6e4868342c05bad963`.

## 전체 delta와 회귀

- manifest에 고정된 8개 파일과 manifest 자체 SHA를 직접 확인하고 전체 변경을 읽었다.
- 새 실제 proxy 회귀는 정상 live/ready, 손상 정의, 닫힌 target 및 proxy 변수3종의 quiet/연결0을 검증한다. proxy 종료 후 backlog 확인과 닫힌 포트의 bind 유지가 있어 늦은 연결·포트 재사용을 성공으로 놓치지 않는다.
- 기존 parser/legacy, scheduling, http_health, pyproject 및 uv.lock byte-identical을 직접 확인했다. 새 options가 legacy API에 소급 적용됐다는 주장은 문서에도 없다.
- 가이드/task/변경 이력은 proxy 미사용·정확 target 귀속과 소비자의 명시 새 CLI 채택을 설명한다. 초기 cold CPU/RSS 측정은 과거 소스 증거이며 이번 옵션 수정의 재측정으로 표시하지 않는다.
- 새 grpc_health와 기존 dagster_health 저장소 회귀를 독립 실행해 **125 PASS / 4.85초**. 원113·author338과 반복/중복 합산하지 않는다. Python3.11/Dagster distribution1.13.25 환경이며 별도1.13.24·full suite 재실행은 이 리뷰에서 NOT_RUN이다.
- 원문 로그 `common33-postfix-grpc-tests-a-20261016.log`를 보존했다. 제품 source 수정 0, peer 원문/결과 NOT_READ.

## 한계와 종료

소스/postfix 승인이다. 실제 소비자 pin/HC override/ARM64 CPU·RSS·DB·복구·배포/live는 미실행이다. 기존 논리4초는 Python bootstrap·decode/close의 hard process wall 보장이 아니다. liveness와 readiness는 다른 계약이며 CPU 개선 보장도 추가되지 않았다.

외부 HTTP/SSH/DB/Docker/운영 호출·변경 0. 자기 ephemeral loopback 서버·proxy·스레드와 subprocess는 모두 종료했다. 작성자 checkout은 수정하지 않았고 독립 detached worktree도 clean 확인 뒤 제거했다. 초기3ed16d1 원문과 P2 반례는 보존하며 이 새 판정으로 덮지 않는다.
