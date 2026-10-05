<!-- SPDX-License-Identifier: GPL-3.0-or-later -->
# Common HTTP 최종 FULL post-fix 독립 리뷰 — James

실행 ID: J-COMMON-HTTP-POSTFIX-20261005-03
역할: UI 소비자/API 계약·취소·관측 메모리·장애 복구
시작 UTC: 2026-10-05T08:03:25.233092+00:00
종료 UTC: 2026-10-05T08:05:58.379817+00:00
저장소: /home/digitie/dev/kor-travel-common-map-recovery
기준선: 7dc1d6dda955b9b836cb3f24d6fd5bcd37fabe52
실제 최종 검토 객체: 1f8e339c7c79f86f8952b0d4c326ab4dae56bee8
격리: own Git archive /tmp/james-common-map-http-postfix-1f8e339
archive SHA256: 858fd1a08da42211ff8a160c9623b95bd6dab1901094d5d0e20ec6cbb8285ab3

**최종 독립 리뷰 판정: PASS.** 새 P0/P1/P2/P3 finding은 없다. 기존 B-P1-01·B-P2-01·B-P2-02는 원래 심각도를 유지해 FIXED로 닫는다. 이 판정은 고정 공통 코드·패키지·가이드 리뷰 범위다. 최종 외부 CI, 실제 Map/PinVi 소비자 적용·N150 live·운영·merge 완료를 뜻하지 않는다.

## 격리·FULL 판정

시작/종료 모두 repository HEAD가 후보와 같고 porcelain이 비어 있었다. 최종 manifest docs/reviews/adversarial/evidence/2026-10-05-map-http-manifest.json의15개 파일 SHA256을 고정 Git blobs와 전부 대조했다. peer reviewer-a md/json과 기타 보존 evidence는 bytes hash만 계산했고 내용을 읽지 않았다. 제품 소스·root 설치·운영 서비스/외부 DB를 수정하지 않았다. 본인의 /tmp snapshot·probe·venv/wheel만 만들었다.

AGENTS/문서 라우터/agent workflow의 공개 packages API 및 runbook 비면제 규칙에 따라 작성자와 별개로 **FULL 대상**이라고 판단한다. 신규 HTTP API·선택 extra·PEP561 marker·실패 처리와 적용 가이드가 추가됐다. 일반 light/오탈자 면제를 적용하지 않는다. 이미 끝난 리뷰의 원문·hash·disposition만 보존하는 후속 closure artifact는 제품 변경과 구분할 수 있지만 이번 runtime 후보는 그 예외가 아니다.

기준선→최종 전체16파일 delta를 검토했다. 공개 http.py/test_http.py 전체, pyproject/uv.lock, py.typed, README/CHANGELOG/guide/task, journal/resume의 새 상태 문구를 읽었다. review 원문4파일은 metadata/hash만 검사했다. UI/tokens/Dagster factory 범위가 기준선과 byte-wise 변경 없음을 Git diff로 확인했다.

## 기존 finding disposition

### B-P1-01 — P1 / FIXED

dev extra가 httpx>=0.27,<1.0을 직접 선언하고 uv.lock의 dev/http dependency 및 metadata가 일치한다. 이전2f7a927 own clean dev+dagster sync와 현재 최종의 pyproject/uv.lock bytes가 동일함을 고정 Git으로 재확인했다. 해당 clean 환경은 Python3.13.14/httpx0.28.1/Dagster1.13.25,57packages를 독립 설치했고 full92 PASS를 확인했다. befbd6f 고정 src에서 full93 PASS도 확인했다. 재사용 환경에만 우연히 있던 httpx가 clean CI 의존성 누락을 가리는 문제는 닫혔다.

### B-P2-01 — P2 / FIXED

http.py의 read deadline과 cleanup 예산을 분리했고 정상 본문 뒤 cleanup 실패를 BoundedResponseError로 알린다. 실패·외부 cancel 뒤 client 폐기를 guide가 앱 책임으로 명시한다.

기존 독립 slow-close 재현을 최종 source에서 다시 실행했다. total .03초와 cooperative close .35초에서 ReadTimeout은 .081초, caller cancel은 .061초에 CancelledError로 반환돼 읽기 예산+별도50ms 범위에 들어왔다. underlying close가 완료되지 않는 상태를 성공으로 숨기지 않는 회귀도26 HTTP tests에 포함된다. 종료를 억제하는 임의 transport를 강제 종료한다는 주장은 하지 않고 지원 경계를 문서화했다.

### B-P2-02 — P2 / FIXED

befbd6f에서 공식 HTTPX AsyncResponseStream의 raw httpcore.ReadError가 cleanup에서 원 ReadTimeout을 덮거나 RequestError 밖으로 빠졌던 재현을 최종 source에 재실행했다. 일반 Exception 분류와 completed 상태가 다음6개 조합 모두 기대대로 동작했다.

- httpcore.ReadError/OSError × 정상 body: BoundedResponseError, RequestError=true, request URL 보존.
- 두 오류 × 읽기 timeout: 원 ReadTimeout 유지, RequestError=true, request URL 보존.
- 두 오류 × caller cancel: 원 CancelledError 유지.

실측 시간은 정상0~.001초, timeout .031초, cancel .010~.011초였다. 실제 운영 소켓의 raw cleanup 오류를 유도했다는 의미가 아니라 공식 wrapper를 사용한 독립 cooperative fault fixture다. 소비자의 RequestError/client 폐기 및 원 취소 전파 계약이 닫혔다.

## 직접 실행 검증

- 최종 고정 사본 HTTP tests: **26 PASS,0 skipped**,0.44초.
- 원 slow-close/cancel/압축/cap/unknown JSON shape 공격과 신규 rawcore/OSError6조합 직접 실행.
- 최종 sdist/wheel 독립 build 및 새 http-extra venv에 offline clean wheel 설치(8packages). 설치 module이 source tree가 아닌 실제 site-packages임을 확인했다.
- wheel의 http.py SHA256이 manifest source와 일치하고 py.typed가 포함됨을 확인했다. LICENSE/NOTICE 포함도 검사했다.
- 설치한 최종 wheel을 자신의 localhost 실제 socket에서 확인했다. 정상 JSON .063초(건강 case의1초 예산), gzip 거부 .003초, 매 .03초 도착하는 slow body는 전체 .06초에서 .061초 ReadTimeout. 실제 server가 세 요청 모두 Accept-Encoding:identity를 확인했다.
- 최종 HTTP module strict mypy: Success,1 source file.
- 동일 dependency config의 독립 clean dev+dagster 설치, 이전 고정2f full92 PASS(108.10초), bef full93 PASS(100.12초)는 각 기준선에만 집계했다. 마지막 두 HTTP 회귀가 추가된 최종 full95를 재실행했다고 주장하지 않는다.

최종 wheel SHA256: b040b48b4db1b37b2158ef682f1a3901a01a9c18a6e32507799d465a5cbec1c6
최종 http.py SHA256: cbb6d44f3635807579cefdbf64d9431c3fc2b46d30b50ccb9ed77602d45d5f2d

## 소비자 계약과 남은 불확실성

HTTP status와 JSON 의미, URL allowlist/auth header, client 수명 및 자동 재시도 정책은 앱 소유다. helper는 정상/오류 body cap을 적용하고 redirect·HTTPX auth flow·response hook의 중간 buffering을 차단한다. 임의 client transport의 자체 재시도/취소 억제까지 강제 금지한다고 가정하지 않는다.

[]/malformed/missing results/HTTP200 degraded를 정상 빈 목록으로 캐시하면 안 된다. 마지막 정상 snapshot, checked_at·stale 경고, 별도 active runs의 bounded 조회와 truncation 경고는 guide의 소비자 계약이며 이 HTTP 모듈이 직접 저장하지 않는다. 실제 Map cache/선택 상세가 이 계약을 지키는지는 Map 고정 후보 리뷰와 live gate에서 검증해야 한다.

write RequestError는 원격 미실행의 증거가 아니다. 기존 uncertain outcome·frozen idempotency UUID/body·claim recovery를 유지해야 한다. body limit을 JSON 객체의 최종 메모리/RSS 상한이나 전체 시스템 failure isolation의 실측으로 해석하지 않는다. exception 문자열은 일반화되지만 request/traceback에 포함된 URL·header 비밀의 로깅 redaction은 소비자 소유다.

NOT_RUN: 최종 full95, HTTPX0.27 floor, Python3.11/3.12, 최종 GitHub CI/tools337 전체, 실제 Map/PinVi adapter·last-good/로그인·모바일·N150 live, 운영 worker kill/RSS·재구축·PR/merge. 부모 실행 결과를 본인 직접 실행으로 집계하지 않았다.

## 원문·재현 보존

이전 precommit BLOCK 원문 common-map-http-review-ui.md와2f/bef CONDITIONAL 원문은 변경하지 않았다. 최종 PASS로 과거 severity/실패 재현을 덮지 않는다.

own scratch /tmp/james-common-map-http-postfix-1f8e339:
- cleanup-final-probe.py SHA256 a08bf0c91500d604253ebb58fcd4011a2649b09c509d0185e45c43594275c065
- adversarial-probe.py SHA256 e6f5db511213e5756b35700e8d62a5999cbfe50d93ab0a77d207520fcbfe3312
- native-probe.py SHA256 01c5b5260d64a966af70c0d23cdc44adb642e2fa68ebb983b89c3d13dd7c7ef3
- cleanup-final-result.jsonl SHA256 c8a43530626161fae7dc0217e3a38b599b40a680d8c821749af1dad769ff42a0
- native-result.jsonl SHA256 bcf9de5e66a2ab551047ad5999cecab1bf64f4433cc533d4b5fde2b5ba72f846
- unit-result.txt SHA256 cf9b536bfc17e583f86e2a4c33f085ee24f3089c45165e3a7cec0106c6892f56
- mypy-result.txt SHA256 5d4b6d285b77932e3d08212c3b4974d0a803f98ec60408ac6ccf6a063fa6c19e

재현:
PYTHONPATH=/tmp/james-common-map-http-postfix-1f8e339/packages/py/kor-travel-common/src /tmp/transport-recovery-venv/bin/python /tmp/james-common-map-http-postfix-1f8e339/cleanup-final-probe.py
/tmp/james-common-map-http-postfix-1f8e339/wheel-http/bin/python /tmp/james-common-map-http-postfix-1f8e339/native-probe.py
