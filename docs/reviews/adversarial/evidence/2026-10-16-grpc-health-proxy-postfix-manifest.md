# gRPC health proxy 우회 post-fix manifest

- 실행 식별자: COMMON33-PROXY-ISOLATION-POSTFIX-20261016.
- 이전 고정 review HEAD: 3ed16d1050bb55b87cc5005c11df3490d88205b6.
- 제품 proxy 옵션 commit: 1511e3d601ee83dcc3103fb9f45f2cf5754110e7.
- [초기 FULL manifest](2026-10-16-grpc-health-isolation-manifest.md)의 전체 문맥을 유지한다.
  아래8파일과 이 manifest의 delta를 동일 immutable review HEAD에서 두 명이 재검토한다.
- 독립 reviewer A의 실제 재현: grpc_proxy CONNECT로 정상 target이 실패/비quiet였고,
  별도 터널에서는 닫힌 target을 다른 합성 건강 서버로 바꿔 false healthy를 만들었다.
  원 source/실패/모형은 보존하며 새 결과로 덮지 않는다.
- 제품 변경은 새 채널의 grpc.enable_http_proxy=0 한 옵션이다. 기존 retry0, logical4초,
  response/parser/profile/기존 public API/CLI·dependency/recovery·phase/HTTP 계약은 그대로다.
- 새 actual subprocess 회귀12조건: grpc_proxy/http_proxy/https_proxy 각각 live/ready,
  정상/손상 정의와 닫힌 target, quiet stdout/stderr, proxy TCP 연결0.
  handler 종료와 accept backlog를 닫은 뒤 연결0을 확인한다. 닫힌 target의 socket을
  바인드 상태로 유지해 재할당 race를 막는다.
- reviewer는 동일 HEAD에서 독립 재검토하며 상대 원문을 읽지 않는다.

| 파일 | SHA256 |
|---|---|
| CHANGELOG.md | 14aef70df3c591095eca163690a99c8067539743d96dc4de6f6fe2e6925ed42b |
| docs/journal.md | 108a18ad71f09c33e286ee0595c82ffe482b599d6571536fcfd805d985e7bf9e |
| docs/resume.md | 4523850f77ff69640bf03cca0c08b333c9267f7065a2460e0287a8e4c3d78cac |
| docs/reviews/adversarial/evidence/2026-10-16-grpc-health-proxy-postfix-wheel.json | 8c7a6ac1fb53cbceb919750cd7125f0c81b5464e362519defdbacfe8becc82bd |
| docs/runbooks/dagster-adoption.md | f215a4f6f98c47ebf3aa4006cfecb04d7af030104078be02e1d842789c447edb |
| docs/tasks/T-319-dagster-recovery.md | 0530f045aebb11b323bb3e52707dda812dc650eb1437b474e91f4b36b6a390db |
| packages/py/kor-travel-common/src/kortravelcommon/grpc_health.py | 2aa9cccee16c65d04590c4c4ef2c2c7404ea7c27ef932df731bb84a7398a8f15 |
| packages/py/kor-travel-common/tests/test_grpc_health.py | a70961954854e8a83db6e4b56bfbd1c5a8832e8fa849ed349b7974269ebe4b43 |

## 작성자 실제 검증

- 새 proxy 회귀를 기존 source에서 먼저 실행: 정상 live가1로 끝나는1FAIL RED 보존.
- 수정 후 Python3.11/Dagster1.13.25 전체338PASS/104.81초(신규60 포함),
  별도 Dagster1.13.24 신규60PASS/2.09초·ruff PASS.
- 새 wheel SHA63bf13f3d16689b6ae877edf57f19897eec81e50d846ce077ff6b22207dcfcfb.
  새 core-only/grpc-only 빈 venv 정상 설치/pipcheck·설치 source SHA 동일.
  실제 설치 CLI6조건에서 proxy 연결0/quiet, core 의존 누락1·grpc-only 정상0 확인.
- 설치 증거는 grpc-health-proxy-postfix-wheel.json이다. 이전 wheel/설치 venv/측정 원문은 보존한다.
- 최초 cold CPU/RSS 표본은6ffc 소스의 과거 증거이며 이 proxy 옵션 수정의 재측정으로
  주장하지 않는다. 운영 CPU/RSS 개선을 보장하거나 측정했다고 표시하지 않는다.
- 문서 link708/2839targets·plan109·diff PASS, 도구337=336PASS/1플랫폼SKIP를 확인했다.
  실제 원문과 SHA는 root에 인계한다.
- 두 독립 post-fix 리뷰·CI·소비자/운영 pin/HC전환·live는 NOT_RUN.
  작성자 SSH/외부 HTTP/운영/DB/Docker 변경0이다.
