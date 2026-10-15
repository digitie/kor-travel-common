# Common32 HTTP health post-fix 독립 재검토 B

- 실행 ID: common32-http-health-post-fix-review-b-20261016. 검토자 /root/geo_timeout_analysis, core-only 패키징·소비자·CLI 계약 관점.
- 독립 격리 시작: 2026-10-15T17:59:37Z. 검증 종료: 2026-10-15T18:00:29Z 이후 UTC.
- 요청 원문 요지: root 지정 immutable b483f5fc02f524f3c3aa6ea90f029835bdc9fcfd, 제품001b03eb9a6b85bb7921d4d55a7f7fdf265c1160/basec7b55aec8e2de6ac70b8f2ef21e2fc18df87c0ce에서 이전 B-P2-01과 전체5파일+manifest delta를 검토한다. 이전 본인 corrected 원문을 계승하되 peer raw를 읽지 않고, 제품 편집·운영 호출 없이 로컬 wheel/loopback만 검증한다.
- manifest: docs/reviews/adversarial/evidence/2026-10-16-http-health-post-fix-manifest.md. 제품5개 blob SHA와 전체6파일 diff를 직접 확인했다.
- 격리: /home/digitie/dev/kor-travel-common-review-http-health-b-postfix-20261016, 새 detached WT. 시작·종료 exact HEAD 및 tracked clean을 확인했다. 초기 WT·wheel·모형·FAIL·원문은 그대로 보존했다.
- **Verdict: PASS. B-P2-01 FIXED. 새 미해결 P0/P1/P2 없음. 소비자 통합·운영 개선 승인으로 확대하지 않는다.**

## 본인 finding과 전체 delta

http_health.py의 유일한 실행 코드 변경은 len(status)<2를 len(status)!=3으로 바꾸는 한 조건이다. 제품 blob의 나머지 모든 바이트가 같음을 직접 확인했다. HTTP/1.1 200 CRLF CRLF라는 필수 SP 누락 반례는 이제 False이며, HTTP/1.1 200 SP CRLF CRLF의 빈 이유 문구는 계속 True다.

새 회귀는 HTTP/1.0·1.1 누락 SP 거부2건, 빈 이유 문구의 필수 SP 유지2건이다. 기존16조건 독립 모형을 새로 설치한 Python3.11 wheel에서 다시 실행해 초기15PASS/1FAIL이 새16PASS/0FAIL로 바뀌었다. 이는 실제 ephemeral loopback 서버와 GET 함수·CLI를 사용한 결과이며 제품의 parser를 흉내 낸 모형으로 대체하지 않았다. 초기 B-P2-01을 FIXED로 닫는다.

기존 redirect Location 유무 거부·503·중복 framing·정상200/299·GET /v1/healthz 한 번·조용한 잘못된 인자·실제 CLI200/503·help 계약도 같은 모형에서 유지됐다. 누락 SP를 거부하면서 reason 자체를 필수 텍스트로 바꾸는 회귀가 없다. 함수 signature, 기본값, deadline/cap/socket 정리, CLI0/1/2 동작, dependency/API 경계를 바꾸는 추가 실행 코드가 없다.

journal/resume는 초기 실패·204/44와 새208/48을 분리하며 이전 원문과 wheel 보존을 명시한다. 가이드는 이유가 없어도 SP가 필요하다고 계약을 구체화한다. 소비자 pin/이미지/healthy·CPU/UI를 후속으로 남긴다. 초기 manifest와 서로 다른 결과를 합산하거나 운영 성능을 선언하는 변경이 없다.

## 독립 패키징·실행

새 detached source에서 uv build --offline --wheel을 직접 실행했다. wheel SHA b0efb0f0cbb3a0b772fb205af4ef1dc8a8d690d28ed0dfa1ee61a3edcf8f3096가 지정 산출물과 일치한다. 새 빈 Python3.11.15 venv에 offline/no-index 일반 의존 해석 설치와 pip check를 통과했다. distribution은 kor-travel-common 하나이고, 설치 모듈 SHA dafb57227662e1298675017be9de04ad602cbeb1a383dcb029e387792c9ec4f6가 제품 blob과 같다. module import 뒤 Dagster/HTTPX/FastAPI/SQLAlchemy/pydantic 로딩은0이다.

pyproject.toml·uv.lock 및 http_health 외 기존 패키지 파일은 c7b와 Git blob가 모두 같다. 이전 전체 검토의 core stdlib/선택 extra/API·Python3.11 경계가 보존된다. 새 공개 의존·console script·export 또는 앱별 환경/재시작 정책을 추가하지 않는다.

독립 WT의 실제 __file__을 먼저 assert한 후 대상48시험을 실행해 **48PASS/0.29s**를 확인했다. Ruff도 직접 PASS했다. 초기에 독립 실행한 c7b 전체204는 그대로 보존한다. 새208 전체102.11s는 작성자 검증이며 본인이 다시 전체 실행한 것으로 합산하지 않는다. 한 조건의 수정 전체와 관련48·동일 독립16·core-only 설치를 재검증한 범위다.

별도 Common31 phase branch 미포함과 소비자 통합 pin에서 예약 코드를 보존해야 하는 기존 한계는 그대로다. 실제 앱의 경로·timeout·라이프사이클, 반복 CPU/메모리·건강 판정·live UI는 Common 로컬 시험만으로 통과 처리하지 않는다.

## 증거

모든 파일은 private .playwright-mcp 아래다.

- common32-http-health-postfix-packaging-b-20261016.json: d86aeb28e889995a1adff2693532a3f2be2f4b632f1c45958c1bcea147843efb.
- common32-http-health-postfix-model-b-20261016.json: 85664aaf242e7c3fecc578dbf70a59cddf2f205e042a68b257f7118fc612d253.
- common32-http-health-postfix-targeted-b-20261016.log: 5d25aa5614ba2e77413b54b0661b6b9267e16893d0878479e9c3dee2fb148187.
- common32-http-health-postfix-ruff-b-20261016.log: 82b3e6a6c090a57601d22943bd23fca9218d1031dbe5a7b754092f9a156b4f18.
- 자체 실행 source: common32-http-health-postfix-check-b-20261016.py 및 postfix-model-b py. 이전 B 원문/정정본/초기 반례는 덮어쓰지 않았다.

peer raw 미열람, source/제품 수정0, 외부 HTTP/SSH/PG/Docker/운영0, 모든 실행 세션 종료. 실제 consumer acceptance·CI와 merge 판단은 root 후속이다.
