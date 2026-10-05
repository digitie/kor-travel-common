# Common HTTP helper 독립 적대 리뷰 — 수정 전 dirty 후보
판정 BLOCK. P2 3건(CI 의존 누락, 실제 httpx 인증 flow의 body cap 우회, cooperative custom stream 정리의 deadline 초과)과 P3 timeout request metadata 1건을 기록한다. 표준 AsyncHTTPTransport의 cleanup 지연은 재현하지 못했으므로 custom transport 경계와 분리했다.
기준 HEAD 7dc1d6dda955b9b836cb3f24d6fd5bcd37fabe52. /home/digitie/dev/kor-travel-common-map-recovery의 dirty4파일을 git archive+사본으로 /tmp/common-map-http-recovery-independent에 고정했다. 제품/원본/설치 수정 없음. 다른 리뷰어 결과·원문 열람 없음. 모든 실행은 WSL Ubuntu-26.04. 현재 구현자는 수정 중이므로 이 문서는 보고서와 함께 저장한 file SHA의 최초 dirty snapshot만 판정한다.

## P2 H-01: clean CI 설치 경로가 httpx를 설치하지 않는다
packages/py/kor-travel-common/pyproject.toml:17-19, .github/workflows/python-package.yml:25, tests/test_http.py:7.
httpx는 http extra에만 추가되고 dev에는 없다. CI는 uv sync --locked --extra dev --extra dagster이다. frozen uv.lock에서 dev+dagster 전이 폐쇄56 packages를 계산했으며 httpx는 없다. 새 test_http.py unconditional import 때문에 clean collection이 실패한다.
pytest 필수 modules만 기존 설치에서 본인 임시 path로 읽기 symlink하고 Python -S/pytest autoload off로 httpx 없는 환경을 구성해 실제 frozen test_http.py를 수집했다. exit2, ModuleNotFoundError: No module named httpx 재현(0.08s). 이는 fresh network uv install을 수행한 결과는 아니며 lock closure+격리 import path의 직접 재현이다. 처음 자체 probe는 pytest의 py shim을 누락해 pytest import에서 실패했고 이를 보완한 뒤 위 제품 collection 실패를 확인했다.
수정 권고: dev extra에 httpx를 포함하거나 CI 설치에 --extra http를 명시하고 lock을 함께 갱신한다. no-extra core wheel smoke는 kortravelcommon/httpx를 eager import하지 않는 기존 경계를 유지한다.

## P2 H-02: 표준 DigestAuth 중간 401 응답은 cap 전에 전체 누적된다
src/kortravelcommon/http.py:54. AsyncClient.stream은 helper가 response를 얻기 전에 auth flow를 처리한다. 표준 httpx.DigestAuth는 challenge401을 읽고 두 번째 request를 만들면서 그 중간 body를 aread한다.
actual AsyncHTTPTransport + 본인 loopback HTTP/1.1 서버에서 DigestAuth user/pass, 중간401 body16777216 bytes, max_response_bytes1024로 실행했다. helper는 최종200 body2 bytes를 정상 반환했지만 request2회/중간16MiB 소비, tracemallocpeak35369440 bytes였다. MockTransport에서도16MiB/peak33597144 bytes로 같은 actual auth flow를 확인했다. body cap을 error status에도 적용한다는 계약과 모순된다. 응답 본문을 읽는 response event hook도 같은 before-yield 경계이므로 정책 확인 대상이다(본 리뷰에서 별도 hook 실행은 하지 않았다).
수정 권고: helper에서 auth=None을 명시해 자동 auth retry를 막고 인증은 소비자 명시 header/Bearer로 제한하는 계약을 문서화한다. response event hooks가 있는 client를 fail-closed 거부하거나 cap 이전 본문 소비가 불가능한 조립 경계를 보장한다. Header 기반 인증·쿠키·URL allowlist는 소비자 소유로 남긴다. auth/response hook가 있는 client에서 의도치 않은 요청이 실제 서버로 나가기 전에 거부되는지도 회귀 검증한다.

## P2 H-03: 전체 deadline은 cooperative custom stream cleanup을 제한하지 않는다
src/kortravelcommon/http.py:53-54,85.
body timeout이 발동해도 client.stream의 __aexit__가 response.aclose를 기다린다. 한번 발생한 asyncio timeout cancellation 뒤 정리 await에는 추가 deadline이 없을 수 있다.
Custom httpx.AsyncByteStream이 body에서 sleep1s, aclose에서 협조적으로 sleep0.25s를 할 때 total_timeout_seconds0.04지만0.2910669s 뒤에 ReadTimeout을 받았다. aclose가 끝나지 않으면 helper도 완료하지 못하는 구조이다. cancel을 무시하는 악의적 coroutine을 쓴 반례가 아니라, 취소를 정상 수용하는 stream의 느린 정리이다.
반면 실제 표준 AsyncHTTPTransport/loopback trickle는0.06s budget에서0.0637778s, caller cancel은0.0031903s로 끝났다. 이 표준 transport의 cleanup 지연은 이번에 재현하지 못했다. httpcore backend는 TLS wrap standard_compatible=False를 쓰는 source도 확인했다; TLS/HTTP2 별도 실행은 미실행이다.
수정 권고: reading elapsed deadline과 최대50ms 정도의 별도 close budget을 명시하고 cleanup도 유한하게 기다리는 구현·slow-close 회귀를 추가한다. coroutine 경계에서 cancel-suppressing custom transport를 강제로 종료할 수 없다는 제한은 별도로 문서화한다. asyncio.wait_for도 cancellation 완료를 기다리므로 악의적 취소 억제 코드를 hard-kill하는 보장으로 표현하지 않는다.

## P3 H-04: total deadline의 ReadTimeout에는 request가 없다
src/kortravelcommon/http.py:86.
직접 total timeout을 재현한 뒤 exception.request 접근은 RuntimeError: request instance not set을 발생시켰다. 다른 BoundedResponseError는 request를 보존한다. 표준 httpx RequestError 소비자의 logging/URL 판정과 일관되도록 outer deadline 실패도 request metadata를 연결하는 것을 권고한다. 현재 Map 소비자가 이 속성을 읽어 실패하는 사례는 검증하지 않았다.

## 정상 경계 직접 검증
독립 frozen 사본에서 Common full pytest89 PASS(98.76s). 신규20 테스트 포함이며 부모 실행과 합산하지 않는다.
actual standard AsyncHTTPTransport + 본인127.0.0.1 ephemeral loopback에서:
- 모든 request Accept-Encoding identity.
- gzip response/oversized chunked body 거부.
- client follow_redirects=True여도302가 그대로 반환되고 target request 없음.
-401 status/body 보존; JSON 및 HTTP raise_for_status 의미는 호출자 소유.
- trickle 전체 timeout과 caller CancelledError 전파 정상(위 수치).
MockTransport 기존 테스트는 declared oversized/negative/malformed Content-Length를 body 미소비로 거부, 압축4형태 디코더 이전 거부, 동일 cap의500 오류, finite size/deadline 입력을 검증하며 본인89 실행에서 통과했다.
Python>=3.11에 asyncio.timeout 사용은 선언과 맞고, http optional extra>=0.27,<1.0은 eager core import를 추가하지 않는다. wheel 빌드·httpx0.27 및Python3.11 직접 실행은 미실행이다.
ruff check src/kortravelcommon/http.py tests/test_http.py PASS; mypy --strict src/kortravelcommon/http.py PASS. 최초 --follow-imports=skip 자체 타입 probe는 httpx.RequestError를 Any로 취급하여 inheritance 오탐이 발생했고, dependency types를 읽는 올바른 strict 실행으로 PASS 확인했다.

## 명령·원문 근거
재사용 Python /home/digitie/.cache/map-common-recovery-venv/bin/python, httpx0.28.1/Python3.13 runtime. source PYTHONPATH는 본인 frozen packages/py/kor-travel-common/src.
- cd /tmp/common-map-http-recovery-independent/packages/py/kor-travel-common; PYTHONPATH=src <python> -m pytest -q →89PASS.
- PYTHONPATH=packages/py/kor-travel-common/src <python> probe_adversarial.py → auth/cleanup/CI closure 반례.
- 같은 PYTHONPATH <python> probe_real_transport.py → standard HTTP socket transport 반례·정상 경계.
- <python> probe_ci_missing_dep.py → 예상 product collection exit2.
- <python> -m ruff check src/kortravelcommon/http.py tests/test_http.py; <python> -m mypy --strict src/kortravelcommon/http.py →PASS.
adversarial-helper-evidence.json, real-transport-evidence.json, ci-missing-httpx.log, fixed-dirty-source-sha256.json을 본인 /tmp에 보존했다. loopback fixture 외 외부서비스/운영DB/N150/실제Map mutation/fullcandidate 리뷰는 미실행이며 코드 변경은 하지 않았다. 이 BLOCK은 수정 후 고정 후보 closure와 별개로 불변 보존해야 한다.
