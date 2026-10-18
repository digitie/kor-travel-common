# Common #39 독립 적대적 리뷰 — Popper r2

판정: **PASS — COMMON_SOURCE_ONLY**, OPEN **P0 0 / P1 0 / P2 0**. r1의 본인 지적 B-P2-01·B-P2-02는 독립 재현으로 **CLOSED**다. 이 판정은 지정된 Common 불변 소스와 로컬 fixture 범위이며 소비자 merge/deploy, PostgreSQL 실환경·외부 제공자·운영 수용 판정이 아니다.

## 실행과 결박

- 리뷰어: /root/review_finish_b, Popper 관점. 다른 리뷰어의 새 결과·모형·보고서를 보지 않았다. 본인 r1 지적과 exact 소스를 기준으로 검증했다.
- 날짜: 2026-10-18 KST. 보고서 고정: 2026-10-18T01:46:27.897438+00:00. 시작의 정밀 timestamp는 별도 고정하지 않았다.
- Manifest: /home/digitie/dev/reverse-address-review-manifest-20261018-r2.json
- Manifest SHA256: 3bbc3ae25d6c70a7fb36afc3229c81d411dc3f2c17117ef5386bc4de394d9d91
- 정식 Common 범위: base c48595880aaad4367802ad71af2525a8a5e17c6a → head 0f768a1974a65bfade4c0fa3c79b897c9663e1a6. 전체 11파일 변경을 검토했다.
- 이전 본인 검토 head: 812b291659e40564595c3c28b7e8d51cbcc46df9. r1→r2 변경 5파일(두 제품 모듈·두 테스트·기능 가이드)을 전체 읽고 변경 함수의 연결 경로까지 다시 검토했다. 불변인 address_dagster.py·pyproject·CI·uv.lock·문서 라우터도 base 대비 전체 delta/기존 연결 검토에 포함했다.
- Common AGENTS/CLAUDE/SKILL 및 리뷰/runbook 지침은 r1에서 읽은 동일 지침을 적용했다. 저장소 작업 트리의 소비자 타입 보정/WIP는 검토·복제하지 않고, 모든 제품·테스트는 git show head:path에서 가져왔다.
- Weather 2a8481f / Transport 60e4137는 manifest상 문맥 참조일 뿐 정식 소비자 게이트로 집계하지 않았다. 소비자 미커밋 보정도 제외했다.
- source/git/기존 파일 수정 0. 실제 SSH/운영 Docker/DB/SDK/provider/브라우저/private/env/auth 접근 0. Daemon start/restore 0. OFF 정책을 바꾸지 않았으며 실제 현재 OFF 상태를 재관측한 것으로 주장하지 않는다.
- 소유 임시 디렉터리에만 pinned 모듈과 파일 SQLite를 만들고 종료 때 제거했다. 영구 작성물은 이 보고서 하나다.

## 이전 지적 closure

### B-P2-01 CLOSED — 정상 Kakao 무결과가 앞선 VWorld 오류를 종결한다

- 정정 위치: packages/py/kor-travel-common/src/kortravelcommon/address_providers.py:232–237.
- 기존 오류: VWorld 예외 뒤 Kakao 정상 HTTP200/documents=[]도 vworld_failed로 저장되어 +120초 재시도, next_refresh_at=None이었다.
- 독립 동일 반례: 실제 r2 reverse()에서 _vworld만 합성 async 예외로 주입하고, HTTPX MockTransport가 정상 documents=[]를 반환했다. 실제 refresh_reverse_addresses와 파일 SQLite 저장까지 연결했다. SDK·실 네트워크 0.
- 결과: status=success, processed=1, requests=1, failed=0, remaining=0. DB status=not_found, next_retry_at=None, resolved_at=None, 2026-01-01 00:00 UTC 확인의 next_refresh_at=2026-07-01 00:00 UTC.
- 연결 음성: 두 제공자 모두 실패하면 유한 코드 kakao_failed를 유지한다. 두 정상 무결과는 None, VWorld 정상 주소는 Kakao 실패 대역을 호출하지 않고 성공한다.
- 결론: 정상 fallback과 오류가 구별되고 정상 무결과의 달력 6개월 저장 계약을 회복했다. r1 실패 기록은 변경하지 않았다.

### B-P2-02 CLOSED — 동일 좌표의 정상 무결과를 재사용한다

- 정정 위치: reverse_address.py:258–281(status in ok/not_found, checked_at 순서),344–349(재사용 시 확인일/다음 확인일 유지 및 정상 무결과에서 해결시각 조작 방지),645–647(정상 무결과 payload 처리).
- 독립 반례: 실제 DatabaseAddressSource SQL keyset·lookup·ReverseAddressStore·refresh_reverse_addresses, 같은 좌표 50개 서로 다른 key의 파일 SQLite를 사용했다.
- 결과: 정상 None에 provider calls=1, reused=49, remaining=0. payload=None/resolved_at=None, next_retry_at=None, next_refresh_at=달력 6개월을 확인했다.
- 날짜·cycle 경계: 30일 뒤 새 target에 재사용해도 checked_at/next_refresh_at 연장 0. 만료일에는 제공자를 다시 한 번 호출한다. force 7개 배치로 부분 재개한 50개는 한 cycle·한 제공자 호출로 완료하고, 완료 뒤 새 force cycle은 새로운 1회 조회를 한다.
- 이전 정상 주소 보존 경계: 같은 좌표에 과거 정상 주소가 있었는데 새 정상 무결과를 얻어 재사용하는 경우, 기존 payload와 실제 과거 resolved_at을 보존하고 status=not_found로 구별하는 현재 save 정책을 확인했다. 이 보존 정책을 임의로 주소 삭제로 바꾸지 않았다.
- 결론: 주소 존재/무결과 양쪽의 좌표 캐시·실제 확인일·수동 cycle 경계가 유지된다.

## 새 동시성·재시도·누락 검토

새 OPEN P0/P1/P2는 발견하지 않았다.

1. **반복 실패의 cursor 기아**: reverse_address.py:594–611은 page 슬롯을 먼저 주고 retry를 번갈아 둔다. 합성 provider 한 번이 31초를 소비하여 run 예산을 넘기는 조건과 batch_size=1에서, poison 첫 위치 이후의 신규 3위치가 후속 tick에 모두 정상 저장됐다. 한 위치의 반복 실패가 다음 위치를 영구히 막는 반례는 r2에서 성립하지 않았다.
2. **retry와 page 중복**: 초기 두 실패를 만든 8개 서로 다른 좌표를 batch_size=2로 재개했다. 같은 key가 retry와 page에 겹쳐도 모든 key가 결국 ok로 저장되고 누락되지 않았다. 중복 page key의 cursor advance 추가가 연결되는 것을 확인했다.
3. **실행 중 source 변화**: cursor 뒤 target 삭제 및 cursor 앞쪽 새 key 삽입 후 유한한 후속 실행에서 남은 target과 새 key를 모두 저장했다. 실제 DB source keyset을 사용했고 임의 순서 callback으로 cursor 정확성을 주장하지 않았다.
4. **HTTP 중 lease 만료/인수**: 이전 resolver 응답 중 실제 두 번째 store.claim을 +91초에 수행했다. 새 owner가 획득했으며 이전 save는 OwnershipLost, late payload row는 없고 finally의 old release가 새 owner를 지우지 않았다. HTTP 도중 DB transaction을 유지해 takeover를 막는 경로도 없었다.
5. **동시 첫 claim**: 두 SQLite thread가 control SELECT를 동시에 마친 뒤 INSERT/UPDATE하게 하여 5회 반복했다. 각 회 winner1/loser1, 예외0. +89초 재획득 거절, +91초 인수 성공, old save/advance/complete 3개 모두 거절, old release 뒤 새 owner 보존을 매회 확인했다. 이는 SQLite 증거이며 PG 행락/격리 결과로 확대하지 않는다.
6. **commit 후 cursor 전 중단**: 실제 결과 저장 뒤 두 번째 advance에 예외를 주입했다. 다음 실행은 저장 결과를 읽어 provider 총 호출1을 유지했다.
7. **로그 context**: address_providers.py:19–38,213–218의 ContextVar 필터/ finally 복원을 검토했다. 합성 VWorld coroutine 내부의 저수준 HTTPX canary 로그는 차단되고, 별도 thread와 종료 뒤 HTTPX 로그는 보존됐다. 예외 뒤 context가 남지 않음을 확인했다. 이 검증은 실제 VWorld SDK/실제 네트워크 실행으로 집계하지 않았다.
8. **소유권 표시**: summary의 live owner 판단은 lease 만료를 확인한다. cursor/force pending은 여전히 진행 필요로 남긴다. 만료 lease만 있는 완료 상태가 영구 실행 중으로 표시되는 이전 경계를 pinned 회귀에서 확인했다.

## 실행한 검사

실제 코드 객체만 소유 임시 패키지로 뽑아 빈 __init__로 무관한 package/SDK 초기화를 차단했다. 읽기 전용 Common venv interpreter, -I -B, 소유 HOME/TMPDIR/cwd, PYTEST_DISABLE_PLUGIN_AUTOLOAD=1, /dev/null pytest config를 사용했다.

| 검사 | 독립 결과 |
| --- | --- |
| pinned test_reverse_address.py 전체 + provider body budget/slow-drip 2개 | 17 PASS / 0 FAIL |
| 이전 지적 및 manual/cache/poison/retry/lifecycle/log 경계의 자체 20개 명명 시나리오 | 20 조건 PASS |
| VWorld 실패→Kakao 정상 무결과→실제 파일 SQLite 저장 별도 통합 연결 | PASS, not_found/6개월/no retry |
| 동시 최초 claim 및 만료 owner 음성 5회 | 매회 winner1/loser1 및 stale 작업3개 거절 PASS |
| git diff --check base..head | PASS |
| 실제 PostgreSQL·실제 제공자·실제 SDK·소비자 브라우저·배포 | NOT_RUN |

17과20은 독립 실행 단위가 다른 수치이므로 원저자 전체501/CI14나 다른 리뷰어 결과와 합산하지 않는다. manifest의 Root PostgreSQL17 row-lock/fencing/dedup PASS·전체501·CI14 green은 의뢰자가 제공한 외부 증거이며 본인의 PG/CI 재실행 증거가 아니다.

## 검증 한계·후속 게이트

- PostgreSQL 동시 최초 INSERT/savepoint, row lock/statement timeout, real driver 및 접속 단절·전원 손실·실제 OS process kill의 전 지점은 실행하지 않았다. 이번 SQLite/fake를 실제 PG 검증으로 표시하면 안 된다.
- run budget은 시작 전에 이미 준비한 source/retry DB 조회나 진행 중 주소 호출을 즉시 중단시키는 hard realtime 보장이 아니다. 문서의 한 주소 timeout 초과 가능성, batch 최대500/30초 기본 및 90초 lease를 소스로 검토했으나 실제 외부 timeout/실행 RSS는 측정하지 않았다.
- Kakao 128KiB body 제한은 pinned 회귀에서 통과했다. VWorld 외부 SDK의 응답 전체 읽기/파싱 메모리까지 Common timeout만으로 상한을 증명할 수는 없다. r1에 기록한 비정상 대형 SDK 응답·worker 최대 RSS의 미검증 한계는 유지하며, 이번 PASS를 임의 제공자 payload 크기의 OOM 부재 보장으로 사용하지 않는다.
- 코드가 원천/관리자 좌표/fact 테이블을 쓰지 않고 파생 두 테이블만 갱신하는 경계를 확인했다. 실제 소비자 migration/schema/최종 DTO/UI·Admin 예약·provider 이용조건·배포 상태 수용은 소비자별 게이트다.
- pyproject의 reverse-address extra/불변 VWorld git pin, uv.lock 및 CI의 extra 설치, core-only 패키지 경계는 변경 소스로 확인했다. 새 wheel 실제 설치/모든 Python 환경은 NOT_RUN.
- address_dagster의 10분 sensor/현재 location active-run 필터/force job 연결은 정적으로 검토했다. 센서 등록의 RUNNING 선언은 실제 Daemon ON 증거가 아니며 OFF 정책을 재개할 권한이나 운영 실행을 이 리뷰가 제공하지 않는다.
- 향후 head 변경은 이 PASS에 자동 포함되지 않는다. 소비자 미커밋 타입 수정 및 향후 consumer CI를 Common 판정에 끼워 넣지 않는다.

## exact head 변경 객체 SHA256

| 파일 | SHA256 |
| --- | --- |
| .github/workflows/python-package.yml | 0ca74a1ec6ee1adb89f3071b93cb3a11d007131de18f066f267b797bd5e881d5 |
| docs/README.md | b68c3b4e4f96acd2dc71e81103dfda316cfb828c6797df254c2dd4f13dd6fd20 |
| docs/reverse-address-refresh.md | d62ee2596f99ce7bd1c11f62d6904d061e87a96d210144205e51c48fdc97c638 |
| packages/py/kor-travel-common/pyproject.toml | d0dc8ef64a6753f9e353918489ac39e273136196fa25ec41ca1119a9b033b9e9 |
| packages/py/kor-travel-common/src/kortravelcommon/address_dagster.py | 193cadfe6273dadd4161c9f6043679ced94dddb2ebb463dcb946105c38b89d02 |
| packages/py/kor-travel-common/src/kortravelcommon/address_providers.py | 76458d10de97ea48cb66bcd33049d8518d9907d4ab2aa3c16c5c2e8959200e4d |
| packages/py/kor-travel-common/src/kortravelcommon/reverse_address.py | 25b6264eb908c9dcdadf7c820d168ff3249c8e959f728ba7150fb1daeda6617f |
| packages/py/kor-travel-common/tests/test_address_dagster.py | 165eeab8241843c5293ae86aaba86dbdeb331486c9b8a0b7d74ed6019bbc7885 |
| packages/py/kor-travel-common/tests/test_address_providers.py | 9dc413aadd1eefa3559b7d8072a55f7822a4526ea84fdfcb1a563bbf2fadbea4 |
| packages/py/kor-travel-common/tests/test_reverse_address.py | e0eee2aa12df7c3957e8c8e30143e918ce235296b9db2dc9271572df031f686f |
| packages/py/kor-travel-common/uv.lock | b982aa676a90d856a6dcf7a10ccfc6b5e1d8a37aedccf48cef0f62289e2e9599 |
