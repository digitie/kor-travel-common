# Common HTTP 최종 FULL 독립 적대 리뷰 — 복구·메모리 담당

- 판정: **PASS**. 고정 Common 전체 delta에서 남은 차단 finding을 발견하지 않았다. Common 코드·계약 판정이며 Map/PinVi 채택·N150 운영 완료 판정은 포함하지 않는다.
- 기준선: `7dc1d6dda955b9b836cb3f24d6fd5bcd37fabe52`.
- 검토 후보: `1f8e339c7c79f86f8952b0d4c326ab4dae56bee8`.
- 원본: `/home/digitie/dev/kor-travel-common-map-recovery`. `git archive`로 독립 고정 사본 `/tmp/common-map-http-1f8e339-recovery-independent`을 생성했다.
- 실행일: 2026-10-05. Ubuntu-26.04 WSL Linux, Python 3.13, HTTPX 0.28.1, Dagster 1.13.24. 기존 `/home/digitie/.cache/map-common-recovery-venv/bin/python`을 읽기 재사용하고 PYTHONPATH는 고정 사본의 src를 명시했다.
- 소유권: 원본 제품·설치·Git/index·외부 서비스/DB 수정 없음. 테스트·빌드·npm 의존 설치는 본인 /tmp에서만 했다. 상대 reviewer-b md/json 내용은 열람하지 않고 SHA256만 계산했다.

## 전체 범위와 무결성

AGENTS.md·SKILL.md 라우터와 해당 task/runbook을 따랐다. 이전 2f7 전체 검토에 이어 최신 기준선→후보 전체 16파일 delta를 직접 대조했다. 신규 HTTP 공개 모듈, 테스트, py.typed, pyproject/uv.lock, README, CHANGELOG, Dagster 적용 가이드, T-319/journal/resume와 evidence metadata를 검토했다. 이전 core/Dagster 구현·UI 구현은 이 delta에서 바뀌지 않는다.

manifest `docs/reviews/adversarial/evidence/2026-10-05-map-http-manifest.json`의 base가 정확하고 15개 파일 SHA256이 모두 일치했다. manifest 자체 SHA256: `718b0351c95c2adac66769b5f3e7cf3ae1e40445a4f743374f27a0160a3c5a9b`.
HTTP 원문 SHA256: `cbb6d44f3635807579cefdbf64d9431c3fc2b46d30b50ccb9ed77602d45d5f2d`.
테스트 원문 SHA256: `3e11aac7b341e27d5fcb0334f715341ede4d99c2a7b2211575030fe96991431d`.
own 기존 BLOCK 원문은 byte 동일하다. 상대 evidence는 bytes hash만 검증했다. 문서 링크 검사 도구의 자동 전체 scan은 수행했으나 상대 finding 본문을 모델에 제공하지 않았다.

## 기존 finding closure

| finding | 심각도 | 독립 재검증·처리 |
|---|---|---|
| H01 clean dev+dagster CI에 httpx 누락 | P2 | CLOSED. dev에 httpx 직접 선언, uv.lock 의존 closure 60개에서 httpx 포함. wheel METADATA의 http/dev extra와 모듈 bytes 확인. |
| H02 DigestAuth 중간 401 body cap 우회 | P2 | CLOSED. build_request/send(auth=None), response hook preflight 거부. 기본 DigestAuth client의 MockTransport 16MiB 401 시 요청 1개·Authorization 없음·64KiB raw chunk 1개에서 cap 오류, tracemalloc peak 73,398 bytes. 실제 표준 AsyncHTTPTransport localhost에서도 큰 401 Content-Length를 body 누적 전에 차단하고 요청 1개. |
| H03 cleanup이 읽기 deadline을 무한 연장 | P2 | CLOSED. 읽기 40ms 뒤 cooperative close 50ms에서 ReadTimeout 유지, 실제 91.04ms. 취소를 무시하는 임의 transport 강제 종료 불가 한계는 가이드에 명시. |
| H04 timeout exception의 request 없음 | P3 | CLOSED. ReadTimeout.request.url이 http://test.invalid/path이고 cleanup 실패 오류에도 원래 request가 있다. |
| H05 정상 body 뒤 close 실패를 200 성공으로 반환 | P2 | CLOSED. http.py:89,103-108. 동일 slow close 250ms 재현은 50.72ms 뒤 BoundedResponseError; close의 httpx.ReadError도 BoundedResponseError. 이전 2f7에서 두 경우 모두 200 반환했던 재현을 고정 후보에서 다시 실행했다. |
| H06 raw stream union 타입 strict 실패 | P2 | CLOSED. http.py:82-85 AsyncByteStream isinstance narrowing. 동일 mypy --strict 명령이 성공하며 wheel에 py.typed 포함. |

추가 raw cleanup 오류 경계도 독립 검증했다. `OSError`와 `httpcore.ReadError` 각각에서 정상 본문·body timeout·크기 cap·외부 취소 총 8경우를 실행했다. 정상은 BoundedResponseError, 나머지는 기존 ReadTimeout/크기 BoundedResponseError/CancelledError를 보존한다. Exception catch는 CancelledError를 삼키지 않는다.

## 직접 실행

고정 사본 package cwd에서 다음 명령을 실행했다.

```bash
PYTHONPATH=src /home/digitie/.cache/map-common-recovery-venv/bin/python -m pytest -q
PYTHONPATH=src /home/digitie/.cache/map-common-recovery-venv/bin/python -m mypy --strict src/kortravelcommon/http.py
/home/digitie/.cache/map-common-recovery-venv/bin/python -m ruff check src/kortravelcommon/http.py tests/test_http.py
uv build --wheel --out-dir /tmp/common-map-http-1f8e339-recovery-independent/wheel-output
```

- 전체 Python **95 PASS, 99.49초**. 신규 HTTP 26개 포함이며 95에 중복 합산하지 않는다.
- HTTP strict mypy PASS, 변경 코드·테스트 ruff PASS.
- uv wheel build PASS. wheel SHA256 `b040b48b4db1b37b2158ef682f1a3901a01a9c18a6e32507799d465a5cbec1c6`.
- wheel의 http.py가 고정 source와 byte 동일하고 py.typed 존재. Python -S + unpacked wheel 경로로 core 및 deadline import 성공, httpx/Dagster import 없음. core-only 경계 검증이며 깨끗한 pip 전체 설치를 수행한 것으로 세지 않는다.
- 본인 `probe_closure.py`, `probe_cleanup_success.py`, `probe_rawclose.py`, `probe_real_transport.py` 실행 PASS. JSON 결과는 고정 사본에 별도 저장했다.
- 실제 asyncio localhost HTTP/1.1 서버와 표준 AsyncHTTPTransport: 압축 gzip 거부, chunked cap 초과 차단, DigestAuth default 비활성, 모든 요청 Accept-Encoding identity, client.follow_redirects=True여도 302 유지·target 요청 0, 401 body 유지. 60ms trickle 예산에 64.04ms ReadTimeout, caller cancellation 2.98ms. MockTransport만으로 transport 동작을 주장하지 않았다.
- `python3 tools/validate_document_links.py`: 594문서/2693 local target, 오류 0. `python3 tools/validate_plan.py`: task109, 오류0.
- `git diff --check baseline candidate` PASS.
- `python3 -m unittest discover -s tests`: 337 실행, **336 PASS + 1 SKIP**, 65.846초. skip은 PASS로 집계하지 않는다.

초기 도구 테스트는 archive에 node_modules가 없어 MDX parser 관련 38 failure/3 error/1 skip이었다. 제품 결함으로 판정하지 않고 본인 /tmp에서 `npm ci --ignore-scripts --no-audit --no-fund`(226 packages, 5초) 후 재실행했다. `rg tools/tests` 첫 경로는 없었으며 실제 tests 경로로 바로잡았다. 실행 중간 실패도 숨기지 않는다.

## 공개 계약·소비자 경계

http extra만 HTTPX 0.x를 추가하고 dev extra가 clean CI 테스트 의존을 직접 가진다. core/Dagster eager import는 변경하지 않았다. uv.lock은 anyio/h11/httpcore/httpx 신규 closure와 common extra metadata 변경으로 한정된다. 응답은 identity raw bytes만 누적하며 byte cap은 누적 전에 검사한다. 반환 materialization은 cap에 비례하는 메모리이며 임의 transport가 이미 만든 큰 chunk나 OS/RSS 전체의 절대 상한을 약속하지 않는다.

HTTP status/JSON/GraphQL semantic 판정·URL allowlist·Bearer/header·client 폐기는 소비자 책임이다. 오류 status에도 cap이 동일하고 redirect/HTTPX auth 재요청은 막는다. RequestError/외부 취소 후 client 폐기, write의 uncertain outcome과 idempotency 보존을 가이드가 명시한다. 본문 성공 뒤 cleanup 실패를 이제 알리므로 가이드와 실제 동작이 일치한다. 읽기 deadline과 별도 50ms close 예산, 악의적으로 취소를 억제하는 transport의 한계를 분리해 기록했다.

Dagster guide의 별도 active 조회·malformed/degraded fail-closed·last good snapshot, Map snapshot 작은 변환 batch+기존 단일 transaction+최종 1회 봉인 규칙은 소비자 경계를 침범하지 않는다. task/journal은 소비자 재구축/live와 shared instance 운영 완료로 표시하지 않는다.

## 실행하지 않은 경계와 보존

NOT_RUN: Python3.11/HTTPX0.27 별도 matrix, TLS/HTTP2, 깨끗한 network uv sync/pip 설치, Map/PinVi consumer 테스트·N150 live·실제 PostgreSQL·provider·운영 worker kill/RSS/shared daemon. 부모의 성공 결과를 본인 실행 결과로 합산하지 않았다. 표준 transport에서 실제 close 지연·연결 누수를 재현한 것으로 주장하지 않는다. 취소 협조 custom stream의 close failure와 실제 표준 transport의 read deadline/cancel을 각각 검증했다.

기존 BLOCK 원문 2개를 그대로 보존하고 SHA를 재확인했다.

- `common-map-http-review-recovery.md`: `3622f7661f03d29e9fab87ef167b7f32c1cfe1b83757868b67089b977d36b496`.
- `common-map-http-postfix-recovery.md`(2f7 BLOCK): `8a818baa26fd63eb2ea3ff26bbfae797a1b5b107b51fdff53388d781913ab23e`.

최종 판정은 고정 1f8e339의 전체 Common delta에 대한 독립 FULL PASS다. 이전 후보 판정을 소급 변경하지 않는다.
