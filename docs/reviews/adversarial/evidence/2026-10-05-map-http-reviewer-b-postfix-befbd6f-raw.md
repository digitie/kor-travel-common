<!-- SPDX-License-Identifier: GPL-3.0-or-later -->
# Common HTTP FULL post-fix 독립 리뷰 — befbd6f 원문

실행 ID J-COMMON-HTTP-POSTFIX-20261005-02. 검토 시작UTC 2026-10-05T07:56:34.179203+00:00.
기준7dc1d6dda955b9b836cb3f24d6fd5bcd37fabe52 → 고정후보befbd6fdb68127cd3f800651bd888cc44ebfbe34.
clean HEAD, own Git archive /tmp/james-common-map-http-postfix-befbd6f. archive SHA25669259b8ad97a8d68306857bfe89a7ba33da7b1efaa5c2b80647ca17e3c06eee2. manifest15파일 SHA모두 일치. peer md/json 내용은 읽지 않고 hash만 검증했다. 소스·root 설치를 수정하지 않았다.

판정 CONDITIONAL. 공개 Python HTTP/extra/PEP561/guide/runbook/task 변경은 FULL 대상이다. docs/evidence-only closure 예외와 구분했다.

B-P1-01 FIXED(P1 유지): dev 직접 httpx 선언과 lock이2f 사본과 동일하다. 이전 독립 clean dev+dagster 설치57packages 성공을 실제 동일 manifest로 연결했다. 이 후보src를 PYTHONPATH로 명시하고 그 clean 환경에서 전체93 tests PASS,0skip,100.12초. 기존 의존성 누락은 닫혔다.

B-P2-01 FIXED(P2 유지): 정상 완료 뒤 slow cleanup failure가 이제 BoundedResponseError가 된다. 새24 HTTP 회귀가 PASS. 기존 .03초 deadline/.35초 close는 .081초, callerCancel은 .061초에 원CancelledError 유지. guide가 RequestError/외부cancel 뒤client폐기를 명시한다.

B-P2-02 OPEN — raw transport cleanup exception이 RequestError 계약과 원본문 실패를 깨뜨림.
위치 packages/py/kor-travel-common/src/kortravelcommon/http.py:101-110; docs/runbooks/dagster-adoption.md:286-288.
고정 helper에 공식 HTTPX AsyncResponseStream를 주입하고 cooperative raw core stream aclose가 httpcore.ReadError("fixture cleanup error")를 즉시 내도록 했다. 본문 정상(delay0)과 읽기timeout(delay.1,total.03) 둘다 raw httpcore.ReadError로 반환됐으며 isinstance(error,httpx.RequestError)는false. 후자는 원 ReadTimeout이 덮였다. AsyncResponseStream.aclose 자체는 httpcore exception을 HTTPX로 mapping하지 않는다. finally가 TimeoutError/httpx.HTTPError만 분류하기 때문이다.
영향: RequestError 뒤client폐기라는 가이드를 따르는 소비자는 cleanup실패를 해당경로로 처리하지 못하고, 본문 실패/취소 원예외를 보존한다는 공개계약이 깨진다. 실제운영소켓의 cleanup오류를 유도한 것이 아니라 공식 wrapper를 사용한 cooperative faultfixture임을 구분한다.
최소수정: cleanup의 일반 Exception을 분류하고 완료body이면 안전한BoundedResponseError로알리며 진행중본문실패/외부cancel의 원예외는 유지한다. rawhttpcore/OSError와 정상/timeout/cancel 조합 회귀가 필요하다.

EXECUTED:24HTTP tests PASS; 기존deadline/cancel/압축/shape/cap 공격; rawcore close오류2조합; 전체93tests; 새wheel/sdist build, http-extra clean wheel 설치8packages, package 내py.typed 존재 및HTTP소스hash일치 확인. wheelSHA cf841c5452957b84e4016d3f7e1d8696175909d14e73896079ed8e37a5bae2f6.
실제localhost wheelprobe는 gzip거부(.012초), slowdeadline(.061초)을확인했다. 처음/ok는아주짧은.06초 cold-start예산에서ReadTimeout(.126초)이발생해그정상case를PASS로세지않았다. 취소된own socket의IncompleteReadError도harness기록에남겼다.
base→후보 전체 제품·lock·README·CHANGELOG·guide·task delta, journal/resume의진행중/외부검증미완료표현도검토했다. peer원문은제외했다.

NOT_RUN: 최신95tests(이보고서이후후보), HTTPX.27/Python3.11·3.12, 외부CI/tools337, Map actualadapter/last-good/N150/운영/merge. last-good상태는앱소유이며 helper가HTTP200degraded를정상빈캐시로확정하지않도록가이드계약을확인했다.

재현 /tmp/james-common-map-http-postfix-befbd6f/cleanup-exception-probe.py:
PYTHONPATH=/tmp/james-common-map-http-postfix-befbd6f/packages/py/kor-travel-common/src /tmp/transport-recovery-venv/bin/python /tmp/james-common-map-http-postfix-befbd6f/cleanup-exception-probe.py

이원문은후속1f8e339결과로덮지않는다.

검토 종료/보존UTC: 2026-10-05T08:02:53.853992+00:00
