# Common #31 고정 phase 예약 분산 독립 FULL 리뷰 B

- execution_id: common31-scheduling-review-b-20261015
- 시작: 2026-10-15T11:09:27Z, 종료: 2026-10-15T11:18:00Z.
- 전문 영역: Python 패키징·순수 코어 경계·달력/실행 정합·문서 수용 범위.
- **merge verdict: PASS — P0/P1/P2/P3 finding 없음, OPEN 0.** 필수 CI와 다른 독립 리뷰의 판정은 merge 담당이 별도 확인한다.

## 요청·기준선·격리

요청: Common31 공용 scheduling 제품의 전체9파일을 소비자 집중 cron 근거, 고정 phase/횟수·간격·신선도/DST, core-only import·의존성·문서/수용 범위 관점에서 독립 검토한다. 소스 편집·운영 호출은 하지 않고 다른 리뷰어 원문/모형을 읽지 않는다.

- immutable HEAD: 41b672c562c059a1f41f459925364459e320bc16.
- base: 8d04353464ccfb4c1efe5c4725274581e4110600, 제품/가이드 commit c12e0a7b9de907b9597371a0de5fa052d8bfcc7d.
- manifest: docs/reviews/adversarial/evidence/2026-10-15-scheduling-phase-manifest.md.
- AGENTS·문서 라우터·resume·workflow·T-319 수용 설계·관련 Python 규약을 읽었다. Git object-only 전체 diff와 별도 detached worktree /home/digitie/dev/kor-travel-common-review-b-scheduling-20261015를 사용했다. 시작/종료 HEAD 동일, porcelain 출력 모두 빈 상태다. 테스트용 dependency symlink는 본인 생성분만 제거했으며 추적 파일 변경0이다. CodeGraph init/status는 완료·up-to-date다.
- 전체9파일: scheduling.py, test_scheduling.py, Python README, dagster-adoption §13, T-319, CHANGELOG, journal, resume, manifest. 소비자·인증·OpenAPI/DTO·dependency/lock·서비스 설정은 변경 범위가 아니다.

## 공격한 계약과 판단

1. interval/phase는 keyword-only native int만 받으며 bool·잘못된 타입·범위를 거절한다. 분 주기는60의 약수, 정시 주기는1440의 약수만 허용하므로 7/90분을 clock 경계에서 불균일하게 배치하지 않는다. 모든 유효 phase가 자정·월·연도 경계에서 정해진 순환 간격과 횟수를 유지한다. 반환 cron 최대 길이는 독립 전수 검사에서70자다. 무한 입력/예약표·동적 재배정·hash/random/clock 조회가 없고 출력/메모리 구조가 작다.
2. Weather acc8의 provider catalog와 dedicated 제외 집합을 실제 Git AST로 읽어 external9를 확인했다. _weather_schedule이 coalescing_schedule에 kwargs를 그대로 전달하고 external loop가15 */3을 쓴다. Transport15a928b의 airport/highway 두 job은 */5다. 소비자 모듈을 import하거나 source를 수정하지 않았다. 두 소비자 근거가 있고 도메인 phase 표는 소비자가 소유한다.
3. KST/UTC에서 Weather 각8회/일·합계72, Transport 각288회/일이라는 예약 횟수와 고정 간격은 실제 SDK 달력과 일치한다. 이는 완료된 수집량·provider 발표 직후의 신선도·동시 run 수/CPU 총량 보장이 아니다. 가이드는 발표/격자/lookback·수집량/lineage·첫 tick·coalescing/복구·운영 CPU/RSS 실측을 소비자 gate로 남긴다. 후보 phase를 이번에 배포한 것처럼 쓰지 않는다.
4. DST는 scheduler wall-clock 의미이며 임의 지역의 고정 elapsed-time/매일 같은 횟수를 보장하지 않는다고 명시한다. 실제1.13.24 시험의 NY 봄 전환 예시는23시간 간격을 확인한다. 다른 DST 지역/가을 전환·운영 daemon 지연은 이 함수가 해결했다고 주장하지 않는다.
5. 순수 모듈에는 import 자체가 없고 __init__도 eager framework import를 하지 않는다. 오프라인으로 만든 wheel을 의존성 없는 새 Python 환경에 설치해 실제 소스 바이트와 일치함을 확인했다. wheel의 unconditional Requires-Dist는0이다. Dagster/auth/schema·HTTP provider·저장소·예약 실행 권한을 새로 갖지 않는다. 기존 coalescing/failure 이후 다음 예약 계약은 기존 시험으로 유지한다.
6. 신규 source/test의 GPL SPDX/저작권 헤더와 한국어 설명을 확인했다. 배포 tag/버전 재발행이나 moving-ref 채택은 없다. 문서는 순수 함수의 합성 microbenchmark를 운영 RSS/속도 절감률과 분리하고 소비자 적용/운영 수집량·freshness·취소·live gate를 NOT_RUN으로 유지한다. T-319의 전역 완료를 선언하지 않는다.

## 독립 실행 증거

- Dagster **1.13.24**, detached 소스의 신규 pytest **70 PASS/1.33초**. actual calendar와 임시 SQLite/public coalescing API를 쓰며 production DB/job 실행은 없다.
- 독립 전수 모형: 입력/범위 등 **2967조건**, 두 timezone의 모든 지원 phase **7416조합**, leap/month 및 year 경계 **109440 native tick**을 별도 arithmetic oracle과 대조했다. 같은 검사를 pytest70과 합산하지 않는다. 결과 common31-scheduling-model-b-20261015.json SHA256 0da5151b03ef13d7badeba702eec586e4d114e1a0ebe41eefcd44109b649a001.
- uv build --offline로 sdist→wheel 빌드 및 fresh core-only wheel 설치 PASS. wheel SHA256 ca9505acefb5a9b1ce440c7f4ae649635b5c9e5e28530a5ed84b5bfbdfcb012e. hash seed가 다른 새2프로세스 모두 Dagster 미설치/미import·기존9phase 동일·wheel/source 바이트 일치. 소비자 AST/core 결과 common31-core-consumers-model-b-20261015.json SHA256 4ad2b0809ac71d1b98414edec11764624a5c5502e9ee2d430845fece2f1f4b57.
- 관련 source/test Ruff PASS, git diff --check PASS.
- 최종 HEAD 문서 링크694/target2808 오류0, plan109 오류0. unittest337 실행 **336 PASS/1 SKIP**; skip을 통과로 세지 않는다. 작성자230 전체 Python/별도70/calendar·microbenchmark와 B 검증을 합산하지 않는다.
- 초기 문서 unittest는 잘못된 tools/tests 경로에서 discovery가 실패했다. 올바른 tests 경로의 첫 실행은 MDX npm 의존성 부재로38 FAIL/3 ERROR/1 SKIP였으며 원 로그를 보존했다. 동일 lock의 기존 node_modules를 본인 worktree에 임시 연결한 뒤 최종337 결과를 확인하고 symlink만 제거했다. 소비자 AST 모형의 최초 coalescing 직접 호출 가정은 실제 Weather wrapper로 수정했다. 제품 소스나 판정 조건을 완화하지 않았다.

## 한계와 후속

운영 네트워크·SSH/Docker/API/DB·프로파일링·서비스/일정 변경0, 타 reviewer 결과 NOT_READ다. 소비자 source/pin 변경, 실제 수집량/freshness SLO, 운영 concurrency/CPU/RSS, 장애·취소 복구, live E2E는 **NOT_RUN(소비자 PR 소유)**이다. 이 source verdict를 소비자 개선 완료나 운영 PASS로 확대하지 않는다. B의 Common 제품 source 수정0이며 Manager author 작업도 별도 소유 범위로 보존했다.
