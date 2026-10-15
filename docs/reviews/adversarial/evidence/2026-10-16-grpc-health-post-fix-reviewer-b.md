# Common33 proxy postfix 독립 제품 재리뷰 B

판정 **PASS**, 열린 P0/P1/P2/P3=0/0/0/0. 최초 FULL의 패키징·호환·리소스·CLI·consumer guide 관점을 계승하고 현재9파일 delta를 전부 검토했다. 운영 채택/CPU 개선 승인이 아니다.

- 실행 ID: COMMON33-PROXY-POSTFIX-MANAGER-B-20261016.
- 고정 review HEAD: d247d19299fddc79f33f3192980111419f886163.
- 제품 commit: 1511e3d601ee83dcc3103fb9f45f2cf5754110e7.
- base: 3ed16d1050bb55b87cc5005c11df3490d88205b6.
- manifest: docs/reviews/adversarial/evidence/2026-10-16-grpc-health-proxy-postfix-manifest.md SHA256 67a002aa4b2fb394c23eb11613613b85d5db72df1b141604ae7f6439a928d5ba.
- handoff: common33-proxy-postfix-handoff-c-20261016.json SHA256 2f2a9ef3dec0f0161fb090633652dae68c73a17bb3e82063a5f57b2c1404041d.
- 계승 본인 FULL: common33-grpc-health-review-manager-b-20261016.md SHA256 af078856f5d087c9e0713b7f0551d34ca941f1dacd5c60f4730a50fc77fba018. 이 원문과 최초 wheel·실패·검증 환경은 보존했다.
- WSL Ubuntu-26.04 Linux, 자체 detached worktree /home/digitie/dev/kor-travel-common-review-manager-b-33-20261016. clean 확인 후 정확 새 HEAD로 이동했다. 진입/종료 source clean, 제품/다른 작업자 변경0.
- 본인 새 검증 증거 시작 UTC 2026-10-15T20:57:38.009009+00:00, 종료 2026-10-15T21:00:03.827535+00:00.
- Common AGENTS/SKILL 라우터/정본 workflow/문서 규칙과 초기 FULL의 규칙을 계승했다. 독립 수동 call/import/packaging trace를 사용했다.
- peer original/postfix raw **NOT_READ**. manifest와 작성자 handoff/제품 회귀는 읽었으나 다른 리뷰어 원문/모형은 읽지 않았다. 작성자 수치를 본인 실행으로 합산하지 않았다.
- SSH/운영/소비자/DB/SDK/Docker/외부 HTTP/intent/freeze/attempt **NOT_RUN/0**. 네트워크는 자체 ephemeral loopback gRPC/CONNECT fixture뿐이다.

**FULL delta 범위**

CHANGELOG.md, docs/journal.md, docs/resume.md, 새 proxy-postfix-manifest.md, 새 proxy-postfix-wheel.json, docs/runbooks/dagster-adoption.md, docs/tasks/T-319-dagster-recovery.md, grpc_health.py, tests/test_grpc_health.py의9파일을 전부 읽었다. manifest의 표8개 SHA와 manifest 자신의 SHA를 직접 검증했다.

제품 grpc_health.py는 base와 직접 문자열 대조해 options에 grpc.enable_http_proxy=0을 넣은 한 줄 이외 bytes 차이가 없었다. retries0/수신4MiB/기본 공유4초 논리 budget/기대 repository·wire profile/parser/quiet CLI 계약은 보존됐다. 기존 dagster_health.py, scheduling.py, http_health.py, pyproject.toml, uv.lock은 base와 byte 동일하다. 따라서 이전 legacy API에 새 proxy 차단을 소급 주장하지 않는 guide와 정합한다.

추가 회귀의 실제 subprocess env, loopback TCP proxy, 종료 뒤 accept backlog/handler 회수, 닫힌 target의 bind socket 유지도 읽었다. 잘못된 target이 다른 서버로 우회해도 success로 세면 안 된다는 계약에 맞는다. 새 옵션은 환경변수를 삭제하거나 프로세스 전역 상태를 바꾸지 않고 해당 채널에만 적용된다.

**proxy 경계 finding closure — 독립 RED/GREEN**

manifest가 설명한 proxy 우회 경계는 본인 최초 FULL에서 발견하지 못했다. 최초 원문을 바꾸지 않고 이번 재리뷰에서 별도 독립 실제 반례를 만들었다.

본인의 이전 wheel을 설치한 기존 grpc-only venv를 사용했다. target socket은 bind 상태지만 listen하지 않게 유지했다. 별도 로컬 HTTP CONNECT proxy가 target 요청을 무시하고 다른 건강한 gRPC 서버로 터널링했다. 이전 live CLI가 exit0으로 끝났고 proxy 연결과 다른 서버의 Check가 관측됐다. 닫힌 지정 target을 정상으로 오인하는 **RED 1건**이며 실제 운영 실패가 아니다. 다른 리뷰어 모형을 사용하지 않았다.

같은 공격 proxy를 새 wheel에 적용했다. grpc_proxy/http_proxy/https_proxy 각각에 대해 정상 live, 정상 ready, 손상 wire ready, 닫힌 target live/ready, core-only 의존성 누락, grpc-only live의 **21개 설치 CLI 조건이 PASS**였다. 매 subprocess stdout/stderr는 모두0B, proxy TCP 연결은 모두0건이었다. proxy server 종료·handler join·backlog drain 이후 연결 수를 판정했다. 닫힌 target은 CLI 종료까지 bind 상태로 유지했다.

정상 target live는 해당 서버의 Check만, 정상/손상 ready는 해당 서버의 Check+ListRepositories만 호출했다. 닫힌 target과 core-only 누락은 건강한 우회 서버 호출0이었다. 기대 repository를 검증하는 ready의 실제 설치25 wire도 통과했다. 따라서 주소 문자열만 loopback으로 고정한 옛 경계가 아니라 실제 채널 target 귀속·quiet 경계를 확인했다. manifest의 proxy P2는 현재 제품 범위에서 **CLOSED**다. 기존 legacy의 proxy 동작은 변경하지 않았고 해당 새 보장을 소급하지 않는다.

**패키징·관련 회귀 본인 실행**

- 정확 새 HEAD source의 offline wheel build PASS. SHA256 63bf13f3d16689b6ae877edf57f19897eec81e50d846ce077ff6b22207dcfcfb. 이전 wheel과 새 wheel을 혼용하지 않았다.
- 새 빈 core-only/grpc-only/지원25/지원24 venv에 새 wheel을 각각 offline 설치, pip check 모두 PASS. core/grpc-only에 Dagster·SQLAlchemy가 없음을 확인했다.
- wheel의 모든 Python 파일8개 bytes가 HEAD와 같았다. wheel METADATA는 이전 wheel과 동일해 선택 의존성/기존 extras 계약이 보존됐다.
- 지원 Dagster1.13.25: 관련 legacy+신규 suite **125PASS/5.12초**.
- 별도1.13.24: 신규 health suite **60PASS/1.84초**.
- 본인 이전 installed-wheel 독립35조건을 새 wheel에서 재실행해 **35PASS**. lazy optional import, core/grpc-only 계약, quiet CLI status0/1/2, 예상 repository와 wire 거절, Dagster 본체·SQLAlchemy·앱 미수입을 확인했다.
- 독립 실제 공격 proxy 설치 CLI **21PASS**, 별도 이전 wheel RED1을 보존했다. 125/60/35/21은 서로 합산하지 않는다.
- 변경 source/test ruff와 base→HEAD diff --check PASS.
- 전체338 Python, 전체 docs link/plan/unittest, 다른 Python/OS/ARM64 및 소비자 gate는 본인 NOT_RUN이다. 작성자 수치를 독립 결과로 합산하지 않았다.

**문서·리소스 주장**

guide는 논리 target127.0.0.1만으로 proxy 차단이 안 되므로 옵션을 유지해야 함을 명시한다. 기존 legacy CLI는 새 격리 보장을 갖지 않으며 소비자의 명시 전환이 필요하다고 구분한다. 새 retry0·논리 예산과 조회 전용/복구 권한 분리도 그대로다.

이전 cold CPU/RSS JSON은6ffc 제품의 과거 측정이며 postfix의 재측정으로 주장하지 않는다. 새 ready의 CPU 동등 절감·운영 ARM 성능·server CPU/DB/worker 복구 개선을 추가로 입증한 자료는 없다. 문서도 이 한계와 소비자/운영 NOT_RUN을 유지한다. 본인 proxy fixture 결과를 성능 측정이나 운영 E2E로 세지 않는다.

**최종 disposition과 한계**

새 P1/P2 finding 없음, proxy P2 source closure **PASS**. 최초 본인 FULL의 운영/소비자/지원 버전 한계를 계승한다. 4초는 import/decode/close를 강제 선점하는 hard process timeout이 아니다. 미지원 Dagster ready는 계속 fail-closed이며 exact pin/lock과 actual image/effective HC/timeout 확인이 필요하다. 본인 새 검증은 Python3.11.15 x86 WSL와 로컬 fixture에 한정한다.

새 증거 /home/digitie/dev/common33-proxy-review-manager-b-evidence-20261016:
- index SHA256 eb3b3c5305bfc6c19186487d4a95c488798b665cb51b6f0e843913f76ba1912a.
- 독립 proxy script SHA256 b238fe33d54adced4f9280ae25309db930544af0b8bfa582ab10f4d161834ad7.
- 독립 proxy result SHA256 760024d0bb2796713b9afd40507d2e6bd67f4f0f8813c1b610a09651d745e811.
- 독립 installed35 result SHA256 153fb119216119789dd275826e07ba53f54b50d7909ac10330ae6447518bab22.

새 원문과 자체 ext4 사본은 exclusive 생성했다. 모든 subprocess/server/thread/test 도구는 terminal 회수했다. worktree는 merge/abandon 전 재검토용으로 유지한다.
