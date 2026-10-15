# Common32 HTTP health 독립 FULL 리뷰 B

- 실행 ID: common32-http-health-review-b-20261016. 검토자 /root/geo_timeout_analysis, backend·core-only 패키징·소비자 상태/CLI 계약 관점.
- 독립 격리 실행 시작: 2026-10-15T17:38:49Z(새 detached worktree 생성). 종료: 2026-10-15T17:43 이후 UTC.
- 요청: root가 지정한 c7b55aec8e2de6ac70b8f2ef21e2fc18df87c0ce 전체9파일을 검토한다. 제품10ed1bb968c286a88396ac43ddfa66780f75f9d5, base8d04353464ccfb4c1efe5c4725274581e4110600. A의 HTTP/parser 결과는 읽지 않는다. source/제품 수정·실제 SSH/외부 HTTP/PG/Docker/운영은0, 독립 loopback·wheel 설치만 허용.
- manifest: docs/reviews/adversarial/evidence/2026-10-16-http-health-manifest.md.
- 격리: /home/digitie/dev/kor-travel-common-review-http-health-b-20261016, exact c7b detached. 시작·종료 tracked status 모두 clean. 원 작성 WT와 source는 수정하지 않았다.
- **판정: CONDITIONAL. P0/P1 없음. B-P2-01 OPEN 1건, 최소 수정·회귀를 권고한다.**

## B-P2-01 — status-code 뒤 구분자가 없는 응답을 정상 판정

위치: packages/py/kor-travel-common/src/kortravelcommon/http_health.py:62~68.

실제 3.11 core-only 설치 wheel에서 loopback 서버가 아래 바이트를 반환하면 check_http_health가 True다.

    HTTP/1.1 200\r\n\r\n

상태 줄을 공백으로 두 번 나눈 결과가 두 요소여도 len(status)<2 조건을 통과한다. 이유 구문이 빈 정상 응답인 HTTP/1.1 200 공백 CRLF는 그대로 허용하되, 상태 코드 뒤 구분자 자체가 없는 반례도 성공한다.

[RFC9112 §4](https://www.rfc-editor.org/rfc/rfc9112.html#section-4)(2022-06, 조회2026-10-16)의 상태 줄 문법은 이유를 생략해도 code 뒤 SP를 서버에 요구한다. 같은 절이 수신자 관대한 파싱도 허용한다는 점을 함께 고려했다. 따라서 이를 일반 HTTP 클라이언트의 보안 취약점으로 단정하지 않는다. 이 task가 명시한 malformed 실패·완전한 헤더를 요구하는 생존 판정에는 예외가 남는다는 finding이다.

영향: 불완전한 상태 줄을 낸 loopback 서비스를 건강하게 판정할 수 있다. 현재 소비자 배포는0이며 정상 서버의200 동작을 깨뜨리는 반례는 아니다. 권고: split 결과 세 요소를 요구하는 최소 조건과, code 뒤 SP 누락 거부/빈 이유 구분자 유지 회귀를 함께 추가한다. 수정은 작성자 소유로 남겼다.

독립 모형 common32-http-health-model-b-20261016.json: 16조건 중15PASS/이 반례1FAIL이다. 이1FAIL을 정상시험 PASS에 합산하지 않는다. 모형은 installed Python3.11.15 모듈의 실제 소켓 GET을 사용했으며 외부 서버는 접근하지 않았다.

## 패키징과 기존 경계

새 detached 소스에서 uv build --offline --wheel을 직접 실행했다. 별도 빈 Python3.11.15 venv에 로컬 wheel을 --offline --no-index로 일반 의존 해석하여 설치하고 pip check를 통과했다. 설치된 distribution은 kor-travel-common 하나뿐이다. import 후 dagster/httpx/pydantic/fastapi/sqlalchemy 로딩은0, 설치 http_health SHA b397f920b2ad3e535eb0a06019889d9da1d7cc97e54278f065a92c47f73159e9가 제품 blob과 같다.

독립 wheel SHA는1fe9b2fef4f2e3e4743a2f5e7d1ad549e8fd20db2293494df5d77e4b733f3769로 작성자 wheel과 동일했다. METADATA의 Requires-Python>=3.11과 모든 Requires-Dist가 optional-extra 조건을 갖는 것을 직접 확인했다. 새 모듈의 top-level import는 math/socket/time뿐이며 __init__이 프레임워크를 eager import하지 않는다.

base의 기존 runtime6개(__init__, dagster, dagster_health, http, runtime, time)와 pyproject.toml·uv.lock은 Git blob가 전부 동일하다. 기존 Dagster/HTTP extra API나 의존 범위를 바꾸지 않았다. 공개 진입점은 module 함수 및 python -m CLI이며 새 console-script 선언을 요구하지 않는다. manifest8개 제품 파일 SHA와 실제 전체9파일 diff를 대조했다.

## 함수·CLI·소비자 계약 확인

함수는 IPv4 127.0.0.1에만 직접 연결하고 DNS/TLS/provider/DB를 호출하지 않는다. 인자 검증은 socket 전에 끝나며 연결·send·recv에 monotonic 잔여 예산을 나누어 쓴다. 본문이나 health JSON 의미를 판정하지 않으며 retry/redirect/재시작도 없다. 헤더를 조립하는 bytearray는16KiB, recv는최대1KiB이며 parsing 때 bytes/list 사본이 생기므로 전체 프로세스 RSS16KiB라는 뜻은 아니다.

독립 3.11 loopback·CLI 모형에서 200/299, redirect Location 유무 모두 실패,503, mixed-case 중복 framing 거부, 실제 /v1/healthz GET 한 번·loopback Host, 정상200/실패503 CLI와 조용한 잘못된 port/path/timeout/옵션을 확인했다. --help만 사용법 출력하는 문서 계약과 같다. 잘못된 인자 값·오류/경로 canary는 stdout/stderr에 나타나지 않았다.

AGENTS/문서 지도/resume/T319/관련 architecture·backend-stack·workflow·manifest 및 변경된 전체 문서9파일을 읽었다. 새 모듈에 기존 호출자가 없고 제품 편집을 하지 않아 CodeGraph 영향 그래프 대신 rg·Git 전체 diff/바이트 대조를 사용했다.

소비자의 경로·Docker timeout·시작/import 비용·주기·재시작 정책 소유권은 가이드에 남아 있다. 함수4초가 Docker5초 안 종료를 보장하지 않는다는 한계도 명시된다. prototype CPU 단일 표본과 이 CLI의 실제 성능을 구분하고, 실제 소비자 pin/설치/운영 healthy·CPU·메모리·UI를 완료로 기록하지 않는다. 별도 Common31 phase branch를 포함하지 않는 사실과 소비자 통합 pin에서 기존 예약 코드를 보존하고 재검증할 gate가 resume/journal/manifest에 명시된다.

## 직접 실행한 검증과 한계

- 새 독립 소스의 import 경로를 직접 assert한 뒤 전체 Python **204PASS/102.28s**를 실행했다. 로그 common32-full-python-b-20261016.log SHA9023e1da71ed9ee6d4abbaba4f906ff844023d8f314fd5b4394d1fa9d542f944.
- Ruff actual c7b **PASS**. 로그 common32-ruff-b-20261016.log SHA82b3e6a6c090a57601d22943bd23fca9218d1031dbe5a7b754092f9a156b4f18.
- core-only 패키징 JSON common32-http-health-packaging-b-20261016.json SHA49ef731088a9372ffcfbd37fef5f33d823d81aa4ea0e511c0b299ad3bb15afb0.
- 자체 loopback/CLI 모형 JSON SHA1057da6ada29a3bd44c7ae608d33f018472f70471631f9ee5e96e3c4c413a039, 모형 소스 SHA4aae5df30564a40bc1c3f50280feeb8af13d1ded627117a31388deb9a96ddcee.
- 최초 단독44 실행은 PowerShell의 $PWD 선확장으로 작성자 WT를 import한 한계를 발견했다. 그 실행은 독립44 gate로 집계하지 않는다. 후속 전체204는 subprocess env의 명시 PYTHONPATH와 실제 __file__ assert로 독립 WT를 입증한 새 실행이다.
- 전체204는 잠긴 all-extras Python3.13.14 환경의 실행파일을 읽기 재사용했고 source·cache는 본인 WT다. 별도3.11은 빈 core-only wheel 실제 설치·모형/CLI이며 전체204를3.11에서 실행했다고 주장하지 않는다.
- 문서 validator·전체 도구337은 작성자 원문을 읽은 상태이며 본인이 재실행했다고 계산하지 않는다.
- target/외부 HTTP/SSH/PG/Docker·서비스·환경 변경·제품 편집0. Python 테스트의 자체 ephemeral fixtures와 명시한 loopback만 실행했다. 두 독립 리뷰 후 finding disposition·소비자 통합/실측은 root 후속이다.
