# Common PR32 독립 FULL 리뷰 A

- execution ID: `common32-http-health-review-a-20261016`
- reviewer: `/root/review_finish_a`, HTTP 파싱·시간 예산·메모리·CLI 관점. 제품 작성자가 아니며 상대 리뷰 원문·모형은 `NOT_READ`.
- 기록 가능한 실행 구간: `2026-10-15T17:40:01.155208Z`(독립 모형 파일 생성)~`2026-10-15T17:42:45Z`(최종 Git 객체·manifest 재확인). 소스·규칙의 선행 읽기는 이보다 앞서 수행했으며 별도 시작 시각은 계측하지 않았다.
- verdict: **CONDITIONAL**, P0/P1 0건, **P2 1건 OPEN**, P3 0건. 아래 상태 줄 검증을 수정하고 반례를 거부하는 후속 immutable commit을 재검토할 것을 권고한다.

## 요청 원문

> 두delta원문고정후 Common32 신규함수·CLI 독립FULL reviewerA 이어부탁드립니다. root작성자 WT `/home/digitie/dev/kor-travel-common-codex-http-health` immutable reviewHEAD c7b55aec8e2de6ac70b8f2ef21e2fc18df87c0ce/product10ed1bb968c286a88396ac43ddfa66780f75f9d5/base8d043... main. PR32draft생성attach완료. repo manifest `docs/reviews/adversarial/evidence/2026-10-16-http-health-manifest.md` 두reviewer동일. AGENTS/README/resume/taskT319/workflow필요문맥읽고9파일FULL(8product+manifest)·stdlibIPv4loopbackGET/monotoniconebudget16KiBheaderstrict2xx/CLIquiet0,1,2 파싱·메모리·timeout·실패·함수3.11계약관점공격. 다른reviewerC는packaging/consumer범위라peerrawNO. ownimmutablearchive순수모형/로컬ephemeral socket시험가능, actualSSH/외부HTTP/PG/Docker/운영0. root전체204/신규44/ruff/core-onlywheel·CLI실제2cases/문서337(336pass1skip)증거private common-http-health-*root*json, wheel+venv `/home/digitie/dev/common-http-health-proof-root-20261016` 읽기만; 본인은독립테스트만수로구분. prototype단일CPU값은현재전체모듈실측아니라문서에명시. Common31phasebranch코드미포함→소비자통합pin에서보존필수. 제품수정말고원문/SHA+실제반례제출, manifest요청원문·실행ID기록. 원본dirty체크아웃보존/notalone.

> 방금 전달한 Common32 reviewerA 전체 요청을 이어 실행해주세요. 종료와동시에전달돼재개트리거합니다. immutablec7b55aec8e2de6ac70b8f2ef21e2fc18df87c0ce, manifest docs/reviews/adversarial/evidence/2026-10-16-http-health-manifest.md, source root작성자9files stdlibHTTPhealth/onebudget/header16KiB/CLIquiet. HTTP파싱·deadline·메모리독립FULL, peerC결과NOTREAD·제품수정0·실제외부/SSH/PG/Docker0·로컬ephemeral socket허용. 이전메시지에전체경계/증거/실행ID요청있으니그대로준수.

## 고정 대상과 격리

- review HEAD: `c7b55aec8e2de6ac70b8f2ef21e2fc18df87c0ce`; 실제 부모: `10ed1bb968c286a88396ac43ddfa66780f75f9d5`.
- 제품 base: `8d04353464ccfb4c1efe5c4725274581e4110600`.
- manifest SHA256: `e872a2349122caad286296dc80ec97102d2ab1d0797ddfdd56a3005f901d3e33`.
- Git archive SHA256: `689211d6a8e1136f70620939bc6d1abfe3d8358204c8931412d37357ee52c233`.
- 실제 검토: base→HEAD 전체 9파일. `CHANGELOG.md`, `docs/journal.md`, `docs/resume.md`, manifest, `docs/runbooks/http-health-probe.md`, `docs/tasks/T-319-dagster-recovery.md`, Python 패키지 README, `http_health.py`, `test_http_health.py`를 읽었다. 제품 8 blob SHA는 manifest와 모두 일치했다.
- 핵심 모듈 SHA256: `b397f920b2ad3e535eb0a06019889d9da1d7cc97e54278f065a92c47f73159e9`.
- 저장소 AGENTS와 docs README/resume/T319/적대 리뷰 workflow를 확인했다. 새 독립 모듈이라 CodeGraph 인덱스를 생성·갱신하지 않고 Git 객체와 실제 import 경계를 읽었다.
- 독립 시험은 위 객체의 `/tmp/common32-http-health-review-a-20261016-q_nj0nb5` archive에서 실행했다. 원본 WT는 전후 clean이며 제품 수정·checkout·설치 변경은 0이다.

## A-P2-01 — 상태코드 뒤 필수 공백이 없는 상태 줄을 정상으로 판정

- 위치: `packages/py/kor-travel-common/src/kortravelcommon/http_health.py:62–69`, 특히 `len(status) < 2` 조건.
- 재현: 실제 IPv4 loopback 임시 서버가 다음 바이트만 전송하고 닫는다. 실제 archive의 `check_http_health`가 두 경우 모두 `True`를 반환했다.

```python
b"HTTP/1.1 200\r\n\r\n"
b"HTTP/1.0 204\r\n\r\n"
```

- 원인: `split(b" ", 2)` 결과가 `[version, code]` 두 조각이어도 허용된다. HTTP 상태 줄은 `version SP status-code SP [reason-phrase] CRLF` 형태이므로 이유 문구가 비어 있어도 두 번째 SP는 있어야 한다.
- 영향: 잘못된 프로토콜 응답을 healthy로 오인한다. 함수 docstring의 프로토콜 오류 `False`, runbook 23행의 완전한 HTTP/1.0·1.1 헤더 계약에 맞지 않는다. 일반 정상 서버의 성공 경로를 깨는 문제로 확대하지 않고, 비정상 응답의 fail-closed 누락으로 P2 판정했다.
- 최소 수정: split 결과 3조각을 요구한다. 이유 문구 자체의 존재는 요구하지 않아 `b"HTTP/1.1 200 \r\n\r\n"`는 허용하고 위 두 바이트열은 거부하는 회귀를 추가한다. 제품 수정은 작성자에게 맡겼다.
- 증거: 아래 JSON의 `malformed_status_counterexamples` 2건. 기대 거부에 대한 **현재 RED**이며 통과 수에 합산하지 않았다.

## 독립 확인 결과

Python **3.11.15**에서 실제 archive 함수를 실행했다. 작성자의 204/44 시험, wheel 검증, 문서 337건은 재실행하거나 본인 결과로 합산하지 않았다.

- 자체 모형 **29개 검증군**이 기대 결과를 충족했다. 그 안의 실제 로컬 응답 21조건은 200/204/206/299, 3xx 두 형태, 503, 100 뒤 200, 잘못된 protocol/줄바꿈/미완료/헤더 형식/obs-fold/제어문자, 대소문자 혼합 중복 Content-Length, CL+TE, 잘못된 CL/TE, chunked 헤더, 16,384/16,385바이트 경계를 포함한다. 별도의 위 두 malformed-status RED는 통과가 아니다.
- 본문이 오지 않는 큰 Content-Length 응답도 헤더 이후 즉시 판정했다. 마지막 recv에 본문 일부가 섞일 수 있다는 문구가 코드와 맞는다.
- 느린 헤더의 총 예산 0.12초 시험은 약 0.120845초에 실패했다. 이는 로컬 표본이며 OS 스케줄 지연까지 포함한 절대 wall-time 보장이 아니다.
- 실제 함수에 socket/monotonic 대역만 주입하여 connect/send/recv가 4→3→2초의 남은 예산을 공유함을 확인했다. 단계별 OSError와 정상 반환 모두 socket context를 정리했다. parse 후 deadline 재검사도 남아 있다.
- 잘못된 인자 12조건은 socket 생성 이전 ValueError였다. bool·범위·비유한 값·경로 검증을 읽고 확인했다.
- 실제 `python -S -m kortravelcommon.http_health`의 잘못된 인자 6조건은 stdout/stderr 없이 종료2, 임시 서버 200/503은 조용히 종료0/1이었다. Python3.11 AST도 파싱했다.
- AF_INET 주소가 고정되고 DNS/TLS/proxy/redirect/retry가 없으며 import는 표준 라이브러리뿐이다. 헤더 저장은 16KiB로 제한되고 recv는 최대1KiB다. bytes/split 사본이 있어 전체 Python heap이16KiB라는 뜻은 아니며 문서도 그런 보장을 하지 않는다.
- CL/TE 중복·모순과 제어문자 거부, 함수와 CLI 오류 구분, 본문 의미를 확인하지 않는 한계는 일치한다. 전체 HTTP 구현이나 앱·DB·Dagster 상태 검사로 평가하지 않았다.
- 문서는 prototype 단일 CPU 표본을 이 최종 CLI/전체 파서의 운영 측정과 구분한다. 실제 CPU/메모리 개선·consumer 채택·운영 healthy/live는 `NOT_RUN`이다. 별도 예약 분산 branch가 이 HEAD에 포함되지 않는다는 점과 소비자 통합 pin의 보존 요구도 명시돼 있다.

## 원문 증거와 한계

- 자체 모형: `common32-http-health-review-a-model-20261016.py`, SHA256 `45e4cf6c5e4d8cb8b3ad02b1b25635b54c4ed8c356e48b5aa90b28e19c04f6c5`.
- 자체 결과: `common32-http-health-review-a-model-20261016.json`, SHA256 `f615e28760508676adc4f88b8cd66180cf33a7d0eeee9eb3367aaddde4f1e208`.
- 외부 HTTP/SSH/PG/Docker/운영 mutation/브라우저 실행 0. 허용된 임시 loopback 서버와 자체 종료되는 CLI만 사용했고 모든 자식·서버 thread와 tool을 회수했다.
- packaging/extras/consumer 설치는 소스 문맥 확인까지이며 독립 wheel 설치를 수행하지 않았다. 상대 리뷰 결과를 근거로 승인하지 않았다.
- 후속 수정은 이 원문을 덮지 않고 새 immutable HEAD와 별도 addendum에서 판정한다.
