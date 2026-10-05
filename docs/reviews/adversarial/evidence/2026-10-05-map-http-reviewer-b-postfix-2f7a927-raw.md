<!-- SPDX-License-Identifier: GPL-3.0-or-later -->
# Common HTTP FULL post-fix 독립 리뷰 — 2f7a927 원문

실행 ID J-COMMON-HTTP-POSTFIX-20261005-01. 소스 고정 2026-10-05T07:48:54.300559+00:00. 종료 시각은 보존 메타데이터에 기록한다.
기준 7dc1d6dda955b9b836cb3f24d6fd5bcd37fabe52 → 고정 후보 2f7a9277c7191bb87e91593a37d53ad6e3ed2065.
clean HEAD를 확인하고 own Git archive /tmp/james-common-map-http-postfix-2f7a927에서 검사했다. archive SHA256 06943eee4e6fc530490a6e3900b7000e6baa89ead07189aef7bc20b1810226ed. manifest14개 파일 SHA 모두 일치했다. peer reviewer-a md/json은 내용 열람 없이 bytes hash만 검사했다. 제품 파일·root 설치 환경을 변경하지 않았다.

판정 CONDITIONAL. 공개 Python/extra/실패 계약과 guide/runbook/task 변경은 FULL이다. docs-only closure 예외와 제품 변경을 구분했다.

B-P1-01 FIXED (P1 유지): dev에 httpx가 직접 선언되고 lock이 일치한다. 자신의 별도 clean .venv에 uv sync --locked --offline --extra dev --extra dagster를 실행해57개 package 설치를 확인했다. Python3.13.14/httpx0.28.1/Dagster1.13.25에서 전체92 tests PASS,0skip,108.10초였다.

B-P2-01 OPEN (P2 유지, 부분 개선): 예전 .03초 deadline+.35초 close 재현은 .081초로 줄어 새50ms cleanup 예산을 준수했다. caller cancel도 .061초에 CancelledError를 유지했다. 하지만 http.py:86-101은 정상 body 읽기 뒤 cleanup 실패를 삼켜200을 반환한다. slow cooperative close(.35초)가50ms에 취소되면 underlying.closed=false, response.extensions={}이다. 원 Response.is_closed=true라 재aclose도 underlying close를 실행하지 않는다. 공식 httpcore PoolByteStream와 HTTPX AsyncResponseStream를 사용한 별도 pool fixture에서도 status200/pending_requests1/reassignedfalse/streammarkedclosedtrue를 재현했다. 실제 운영 TCP pool 고갈을 유도한 것은 아니다.
가이드의 “정리 실패 뒤 client 폐기”를 성공 응답 caller가 관측할 표식이 없다. polling 재사용 client에 정리 실패가 누적될 수 있다. 최소 조치: 완성 body에서도 정리 실패를 RequestError 또는 명확한 response 상태로 알리고, 본문 실패/취소의 원 예외를 유지한 채 client 회수 계약을 검증한다.

EXECUTED: 23 HTTP tests PASS; 위 기존·잔여 cleanup 공격; independent clean extra 설치 및92 tests; own wheel/sdist build; 별도 core-only wheel install(httpx없음,core import성공), http-extra wheel install(8packages,Httpx0.28.1,실제site-packages module확인); 설치 wheel로 실제 localhost JSON/gzip/trickle(전체 .06초에서 .062초 ReadTimeout) 검증. 압축은body읽기전거부, headeridentity실측. DigestAuth/hook 차단 회귀도23/92에 포함한다.
JSON 의미/last-good stale 상태는 Common HTTP에 내장되지 않고 앱 소유라는 guide 계약을 확인했다. malformed/degraded200을 정상 빈 snapshot으로 저장하면 안 된다. write RequestError를 미실행으로 단정하거나 자동 재발행하면 안 된다.

검토: base→candidate 제품/extra/lock/README/CHANGELOG/guide/task 전체 delta. journal/resume 변경의 진행중·소비자NOT_RUN 표현도 확인했다. peer 원문 제외, 원본 보존hash검사만 수행했다.
NOT_RUN: HTTPX0.27 floor/Python3.11·3.12, 외부CI/tools337 전체, Map actual adapter/last-good/N150 live/운영/PR merge. 부모 검증을 자신의 실행으로 집계하지 않았다.

공격 스크립트: /tmp/james-common-map-http-postfix-2f7a927/{adversarial-probe.py,cleanup-observability-probe.py,pool-cleanup-probe.py,native-probe.py}.
이 원문을 후속 befbd6f 후보의 결과로 덮어쓰지 않는다.

원문 보존 UTC: 2026-10-05T07:55:56.329920+00:00
