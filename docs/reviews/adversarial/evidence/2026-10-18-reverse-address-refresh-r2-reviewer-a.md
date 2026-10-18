# Common #39 James 독립 post-fix FULL 리뷰 r2

- Review ID: COMMON39-JAMES-R2 / reviewer 실행 ID: /root/review_finish_a.
- 전문 관점: 관리자 실행·API/UI 상태의 진실성, provider 오류/비밀 경계, 원천 보존, 공개 계약과 소비자 연결.
- **판정: PASS — Common 고정 소스 범위. OPEN P0=0 / P1=0 / P2=0 / P3=0.**
- 이전 본인 A-P1-01, A-P2-02: **FIXED**. 원 r1 보고서는 수정하지 않았다.
- Manifest: /home/digitie/dev/reverse-address-review-manifest-20261018-r2.json.
- Manifest SHA256: 3bbc3ae25d6c70a7fb36afc3229c81d411dc3f2c17117ef5386bc4de394d9d91.
- Common base: c48595880aaad4367802ad71af2525a8a5e17c6a.
- Common head: 0f768a1974a65bfade4c0fa3c79b897c9663e1a6.
- 비교한 이전 head: 812b291659e40564595c3c28b7e8d51cbcc46df9.
- 소비자는 문맥만: Weather 2a8481fd27a99bc22487fca4ac76875150440cd0 / Transport 60e41371aa9d7a6b031ec9cee41caada636c7d97.
- 이번 세션 시작은 2026-10-18 UTC이며 시작 분·초 별도 계측은 하지 않았다. 종료 시각은 끝에 기록한다.
- 다른 reviewer의 새 결과/보고서와 작성자 검증 로그는 읽지 않았다.

## 기준선·범위·변경 보존

기존에 읽은 Common AGENTS/runbook/review 기록 규칙을 적용하고, 새 고정 AGENTS/문서 지도/주소 가이드와 Git object를 재확인했다. HEAD 이동이나 미커밋 내용으로 대체하지 않았다.

base→head 전체 변경은 11파일, 1634+/2-다. 제품은 reverse_address.py 668줄, address_providers.py 240줄, address_dagster.py 82줄이며, 세 테스트 파일·가이드·문서 링크·extras/uv.lock·CI 연결까지 검토했다. r1→r2의 직접 수정은 5파일 188+/10-이다.

AST 비교상 변경된 기존 함수는 ReverseAddressStore.reuse/save, DatabaseAddressSource.summary, refresh_reverse_addresses, provider reverse 래핑/내부 _reverse 및 신규 로그 필터다. address_dagster.py는 r1과 동일하다. lease 획득/갱신/late-write fence/release, 원천 SELECT·좌표 검증·달력 계산, DB URL/engine 생성과 테이블 스키마는 이 수정에서 바뀌지 않았다.

Common worktree의 시작·종료 tracked 변경은 없고 미추적 작성자 .verify-address-common.log / .verify-address-common-r2.log만 있었다. 파일 내용은 읽지 않았다. 소비자 WIP와 타입 보정은 범위 밖이며 읽거나 되돌리지 않았다. 필요한 실행은 git show에서 메모리 compile 또는 자동 정리되는 소유 임시 복사로 수행했다.

새 영구 산출물은 이 보고서 하나다. 코드·Git·운영 변경, SSH/Docker, 실제 DB·provider 요청·자격정보 읽기, Daemon 시작은 하지 않았다. fixture는 in-memory SQLite와 HTTPX MockTransport만 사용했으며 socket.connect를 거절했다. VWorld public SDK의 mock 전송/파싱은 사용했지만 Dagster 실제 인스턴스/실행은 만들지 않았다.

## 이전 지적 해결

### A-P1-01 — 정상 VWorld HTTPX INFO에 키/URL 노출: FIXED

수정 위치:
- packages/py/kor-travel-common/src/kortravelcommon/address_providers.py:19–38.
- 같은 파일 :213–218.

ContextVar가 해당 reverse() 요청 문맥에서만 HTTPX/현재 HTTPcore 로그를 차단한다. reverse()의 finally는 토큰을 되돌린다. 전역 logger level을 켰다 끄는 방식이 아니므로 같은 시점 다른 스레드의 정상 로그를 막지 않는다.

원 반례와 같은 공개 VworldClient + MockTransport + 메모리 INFO handler를 두 head에 적용했다. 가짜 canary만 사용했고 실제 네트워크는 금지했다.

| 경로 | 이전 812b291 | 새 0f768a1 |
| --- | --- | --- |
| 정상 VWorld 주소 | canary/요청 URL 로그 노출 | canary 비노출, 정상 주소 |
| VWorld 500 | canary/요청 URL 로그 노출 | canary 비노출, 유한 vworld_failed |
| VWorld 500 → Kakao 정상 무결과 | 오류 반환, primary canary 노출 | 정상 None, canary 비노출 |

세 경로 모두 병렬 스레드의 parallel-visible 로그와 reverse 종료 후 outside-visible 로그는 유지됐다. 따라서 원 P1의 RED→GREEN 및 오류 후 문맥 복원이 확인됐다. 운영 logger 수집기나 미래 HTTP 라이브러리 버전의 모든 logger를 검증했다는 뜻은 아니다.

### A-P2-02 — 만료 owner의 영구 진행 표시: FIXED

수정 위치:
- packages/py/kor-travel-common/src/kortravelcommon/reverse_address.py:509–526.

이제 cursor/manual-cycle 잔여와, 아직 유효한 lease의 owner만 in_progress에 반영한다.

원 반례의 실제 순서 claim → prepare → save(정상 주소) → advance → complete_cycle을 in-memory SQLite에서 실행하고 release 전 crash를 모형화했다. lease를 만료시킨 뒤 실제 summary/has_work를 양 head에서 호출했다.

| 조건 | 이전 812b291 | 새 0f768a1 |
| --- | --- | --- |
| 유효 owner | in_progress=True | True 유지 |
| 완료·cursor 빈 값·force False·lease 만료·due0 | in_progress=True, has_work=False | **in_progress=False**, has_work=False |
| 같은 만료 owner에 실제 cursor 잔여 | True | True 유지 |

완료된 배치의 유령 진행 표시를 없애면서 실제 재개할 커서를 숨기지 않는다. 실제 worker/lease 경합 PostgreSQL 실험은 본인이 실행하지 않았다.

## 새 수정의 독립 공격·회귀 확인

### 재시도·작은 배치의 진행성

refresh_reverse_addresses:594–611은 페이지 진행 슬롯을 먼저 두고 재시도를 교차 배치한다. 중복 key가 페이지 측에 다시 나타나면 cursor를 진전시킨다. 결과 저장 전 lease 갱신과 저장 후 cursor 기록, 예외 시 release는 그대로다.

본인 fixture에서 a는 항상 유한 provider 오류, b는 정상이고 batch_size=1, 세 tick의 가상 시각을 각각 1시간 간격으로 설정했다.

- 이전 head 실제 호출: ["a", "a", "a"].
- 새 head 실제 호출: **["a", "b", "a"]**.

작은 배치에서 독성 재시도 하나가 다음 위치를 가로막던 반례가 해결됐고 재시도 자체도 사라지지 않았다. 모든 신규 유입률에 대한 지연 SLA나 대규모 실제 처리량을 증명한 것은 아니다.

### 정상 무결과 재사용·수동 cycle·원천 보존

reuse:270–276은 ok/not_found를 함께 재사용하고 checked_at으로 최신 확인을 고른다. save:344–349는 실제 provider 확인일/다음 갱신일을 연장하지 않고, 무결과 재사용에 허구의 resolved_at을 만들지 않는다. 기존 동일 좌표의 마지막 정상 주소를 보존하는 기본 규칙은 유지된다.

본인 fixture는 위치 77개/좌표 5종, 수동 force, batch_size=7이다. 11회 분할 실행으로 끝까지 진행했다.

| 항목 | 이전 head | 새 head |
| --- | --- | --- |
| provider 정상 무결과 호출 | 77회 | **5회** |
| 처리 완료 batch | 11 | 11 |
| 77개 status | not_found | not_found |
| 새 payload/resolved_at | None/None | None/None |
| 입력 key·좌표 tuple | 불변 | 불변 |

새 캐시가 주소를 만들어 내거나 위치를 누락시키지 않았다. source 원천 주소·관리자 좌표·과거 fact의 UPDATE 경로를 추가하지 않았다.

### provider 우선순위·오류 및 로그 경계

VWorld 우선은 그대로이며 정상 주소가 있으면 Kakao를 호출하지 않는다. VWorld 실패 후 Kakao의 정상 빈 documents는 오류가 아니라 정상 무결과로 끝난다. Kakao 실패는 kakao_failed로 정리된다. 요청별 private 문맥은 정상/예외 모두 finally에서 해제된다. HTTP 크기·deadline·낮은 요청 빈도와 SDK retry 0 규칙의 기존 코드는 보존된다.

고정 소비자 source의 주입도 확인했다. 두 소비자는 모두 위 Common0f768a1을 pyproject/lock에 고정하고 동일 AddressResolver/DatabaseAddressSource/refresh 함수에 연결한다. Weather는 서버 SecretStr에서 값을 꺼내 주입하고 Transport는 서버 설정을 주입한다. 관리자 BFF는 고정 자기 location/job의 force config와 세션/같은 Origin 경계를 사용한다. 이는 통합 연결 정적 확인이며 인증·UI·소비자 CI 정식 게이트가 아니다.

## 실제 실행 결과

고정 head의 reverse_address/provider 기존 테스트를 임시 디렉터리에 Git object에서 복사하여 독립 실행했다.

- Python: Common 공개 dependency venv /home/digitie/dev/kor-travel-common-codex-reverse-address-20261018/.venv/bin/python.
- 실행 방식: Python -I -B; sys.path는 소유 Git-object 복사 src; pytest --noconftest -p no:cacheprovider.
- 대상: test_reverse_address.py, test_address_providers.py.
- **23 PASS, 0.66초**, skip0, exit0.
- 실제 socket.connect 금지. SQLite는 신규 in-memory/소유 임시 fixture만.
- 위 표의 RED→GREEN/병렬 로그/lease/cursor/77위치 검증은 본인 별도 actual-function fixture다. 기존 테스트 수와 중복 합산해 큰 총합을 만들지 않는다.

Manifest의 root501 PASS/집중25 PASS/격리 PostgreSQL drill 및 Common CI14 green은 제공된 외부 증거 정보다. 본인이 재실행한 전체 테스트 또는 새 CI 관측으로 승격하지 않는다.

## 판정 한계·운영 조건

- 신규 OPEN finding은 없다. 이전 P1/P2는 위 새 고정 head에서 FIXED다.
- 판단은 Common 소스 및 실행한 fixture에 한정한다. 소비자 CI·최종 타입 보정·브라우저·실제 Admin 수동 예약·실제 운영 배포는 NOT_RUN.
- 실제 PostgreSQL 동시성/row lock/드라이버/스키마와 실제 제공자 키 권한·이용조건·쿼터·실제 응답·운영 로그 sink는 NOT_RUN.
- address_dagster는 전체 정적 재검토했다. 실제 SDK job/sensor 실행은 NOT_RUN이며 고정 자기 location/job 필터와 자동 pending 예약 구조만 확인했다.
- 위치별 달력 6개월/수동 예약 구조는 유지된다. sensor 기본 RUNNING 등록은 실제 Daemon을 켜는 호출이 아니며 새 start/restore 코드가 없다. **Daemon OFF 유지**는 운영 실행자의 별도 계약이며 본인이 시작하지 않았다.
- 정상 무결과의 stale 표시 등 r1에서 확인했지만 finding으로 판정하지 않은 보수적 표현은 이번 closure를 통해 운영 성공으로 확대하지 않는다.
- 향후 의존성의 logger 이름/전송 구조가 바뀌면 canary 비노출 회귀를 재실행해야 한다.
- 원 r1 BLOCK 보고서 및 실패 반례는 보존했다. 이 PASS는 과거 실패를 삭제하거나 소비자 merge/deploy 허가로 대신하지 않는다.

종료 UTC: 2026-10-18T01:45:45.061682+00:00
