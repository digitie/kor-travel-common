# Common39 FULL post-fix r3 — James 독립 원문

- Review ID: COMMON39-JAMES-R3. Reviewer: /root/review_finish_a.
- 렌즈: 신뢰 경계·공개 API·상태 진실성·실패 후 재개, 기존 로그/캐시/소유권 보호.
- **판정: PASS — 고정 Common 소스·독립 fixture 범위. OPEN P0=0 / P1=0 / P2=0 / P3=0.**
- CI 완료나 소비자 정식 수용·배포 PASS를 뜻하지 않는다.
- base: c48595880aaad4367802ad71af2525a8a5e17c6a.
- head: 14115ba99ab5d72d4f381d25b2dca810b24914d6.
- 이전 검토 제품: 0f768a1974a65bfade4c0fa3c79b897c9663e1a6.
- Manifest: /home/digitie/dev/reverse-address-common-review-manifest-20261018-r3.json.
- Manifest SHA256: 90eb2c39add81093deee1cc4ff84a9bf4655a8c4852e6333a18bf00018a3047e.
- 시작: 2026-10-18 UTC 본 세션, 시작 분·초 사전 계측 없음. 종료는 문서 끝에 기록한다.
- 새 상대 reviewer 결과/보고서는 열람하지 않았다. Git diff에 포함된 이전 r1/r2의 역사적 closure는 이번 r3 독립 판정 근거로 사용하지 않았다.

## 격리와 FULL 범위

Common AGENTS/runbook/review 기록 규칙을 기존 검토에 이어 적용했다. immutable git show/diff로 base→head 전체를 검토했다. 전체 변경은 21파일 2336+/2-이며, 기존 제품 3모듈·테스트·가이드·extras/lock/CI와 과거 closure 보존 문서가 포함된다. 역사적 review artifact는 과거 제품0f768a1의 기록으로만 구분한다.

이번 제품 delta는 reverse_address.py의 다섯 함수다.

- DatabaseAddressSource.has_work.
- 신규 _failed_targets / pending_failures / retries.
- refresh_reverse_addresses의 callbacks 및 완료 판단.

address_providers.py와 address_dagster.py, pyproject.toml, uv.lock는 이전 검토 제품0f768a1과 byte 동일하다. AST로 비교했을 때 lease claim/fence/prepare/advance/release/save, 캐시 reuse/projections, 달력 계산/좌표 검증/테이블 선언은 변경되지 않았다. 가이드는 새 callback 연결과 AUTO=false 수동 재개/원천 제거 정리를 설명한다.

시작·종료 worktree에 tracked 변경은 없고 작성자 미추적 .verify-address-common.log와 .verify-address-common-r2.log가 있었다. 내용을 읽거나 수정하지 않았다. 검증은 Git object의 메모리 compile 또는 자동 정리되는 소유 임시 복사로 실행했다. 소비자 미커밋 WIP는 읽지 않았으며 연결되었다는 의뢰 정보를 소비자 정식 승인으로 사용하지 않았다.

소스·index·branch·운영 변경0. SSH/Docker/실제 provider/키/운영 DB/Daemon 시작0. SQLite는 신규 인메모리 fixture뿐이다. SDK의 외부 요청은 없으며 기존 provider 회귀는 MockTransport + 실제 socket.connect 거절 상태다. Dagster 실제 job/instance는 실행하지 않았다. 영구 신규 파일은 이 보고서뿐이다.

## 새 수정의 독립 RED→GREEN

### 1. AUTO=false 수동 오류가 backoff 후 이어지고 성공 후 종료한다

관련 위치: reverse_address.py:464–495,598–610,628–629,696–704.

두 제품의 실제 함수를 별도 메모리 모듈로 로드했다. 활성 위치1개와 유한 실패 resolver를 사용하고, source.page/lookup(이전 API) 또는 source.page/retries + pending_failures(새 API)를 연결했다. 첫 force 호출 후 sensor의 pending 판단을 실제 has_work(automatic=False)로 조회했다.

| 관측 | 이전0f768a1 | 새14115ba |
| --- | --- | --- |
| 첫 수동 실패 remaining | 0 | **1** |
| backoff 60초 시 has_work | False | False |
| 121초 시 has_work | False | **True** |
| due 뒤 provider 정상으로 전환 | 재개가 없어 error 잔류 | **1회 재시도, ok** |
| 성공 뒤 AUTO=false, 200일 후 has_work | — | False |

새 동작은 자동 달력 갱신을 켜서 우회하는 방식이 아니다. 이미 시작한 수동 cycle만 오류까지 완료하도록 보존하며, backoff 중 불필요한 sensor run을 만들지 않는다. 성공한 뒤 cycle을 종료하고 AUTO=false를 계속 존중한다.

### 2. 원천에 없는 오류11개가 활성 재시도 슬롯을 빼앗지 않는다

관련 위치: reverse_address.py:498–520,628–629.

두 제품에 동일한 “unfinished manual cycle + 활성 live 위치 오류1개 + 더 오래된 source 부재 오류11개”를 실제 store 메서드로 만들었다. 이전 head는 store.retries의 limit10을 먼저 적용하고 lookup에서 없는 source를 버리므로 모든 슬롯을 낭비한다.

| 관측 | 이전0f768a1 | 새14115ba |
| --- | --- | --- |
| 한 번의 재개 provider requests | 0 | **1** |
| 활성 live의 저장 status | error | **ok** |
| remaining | 0(오류가 남았는데 종료) | 0(활성 오류 해소 후 종료) |

새 source.retries는 provider_id가 고정된 _joined와 활성 source SELECT를 먼저 결합하고 status/error 및 due 조건 후 limit를 적용한다. source에 없는 과거 오류 row가 살아 있는 오류를 밀어내는 반례가 해소됐다.

### 3. 삭제·비활성 원천은 provider 없이 한 번 정리한다

새 제품에서 수동 실패 후 source를 각각 DELETE 또는 enabled=False로 바꾸었다(소유 in-memory source fixture에만 적용).

- has_work(automatic=False)는 마지막 정리1회를 허용했다.
- pending_failures는 현재 활성 source 오류만 보아 False였다.
- 정리 실행의 추가 provider 호출은 0.
- 그 뒤 has_work=False, 영구 manual-cycle 대기 없음.

source를 버린다는 의미로 원래 파생 오류 row를 삭제하지 않는다. 활성 집합의 실행/상태 판단에서 제외한다는 경계를 유지한다.

### 4. 좌표 변경과 callback 오류의 복구 경계

독립 추가 음성 fixture:

- 실패 뒤 retry 시각 전 longitude를 127→129로 바꾸면 has_work=True, source.retries의 target은129였다. 이전 좌표 backoff를 새 좌표에 적용하지 않고 새 좌표를 한 번 조회·저장했다.
- 정상 결과를 저장한 뒤 pending_failures callback에 예외를 주입했다. 예외는 은폐되지 않았고 finally가 owner를 해제했다.
- 다음 실행은 남은 manual-cycle을 정리했으며 이미 저장한 결과 때문에 추가 provider HTTP는0이었다.
- inspect.signature에서 pending_failures가 필수 keyword-only임을 확인했다. 이를 생략한 호출은 binding 단계에서 TypeError이며 잘못된 잔여 판단으로 조용히 완료 처리하지 않는다.

## 공개 API·상태 계약 검토

새 API는 다음 조합이다.

    refresh_reverse_addresses(
        source.store,
        resolver,
        source.page,
        source.retries,
        pending_failures=source.pending_failures,
        ...,
    )

retries는 원천 필터를 거친 AddressTarget 시퀀스를 반환하고 pending_failures는 현재 활성 원천의 실패 존재 여부를 반환한다. 더 이상 store.retries의 key 목록에 lookup을 사후 적용하는 계약이 아니다. source가 소유한 필터가 page/retries/pending_failures에서 일치해야 한다는 소비자 책임은 남는다.

이 API는 basec485958에는 없던 미머지 신규 기능의 계약 정리다. 기존 릴리스 함수의 signature를 조용히 바꾼 변경으로 판단하지 않는다. 가이드에 필수 callback과 새 positional 인자가 명시돼 있다. 다만 소비자는 새 pin과 호출자를 함께 반영해야 하며, old caller가 새 패키지에 자동 호환된다고 주장할 수 없다.

status/remaining은 수동 실패가 남으면 remaining1을 유지한다. summary의 manual_cycle/in_progress가 “재개 대기”를 나타내는 동안 due는 backoff 조건에 따라0일 수 있다. 이를 실제 worker가 현재 실행 중이라는 증거로 바꾸면 안 된다. 이전0f의 유효 lease 검사도 그대로여서 완료 후 만료 owner만으로 영구 진행을 표시하지 않는다.

현재 source 밖 오류를 제외하는 것은 원천·주소·좌표/fact 수정이나 오류 삭제가 아니다. 재활성화된 원천은 해당 시점 좌표·오류/due 조건으로 다시 판단한다. 자동 calendar refresh OFF와 이미 시작한 수동 작업의 완료 책임을 분리한 현재 동작은 요청과 맞는다.

## 기존 신뢰·로그·캐시·소유권 회귀

- 이전 본인 A-P1-01(HTTPX key/URL 로그) 및 A-P2-02(만료 owner 표시)의 수정 코드는 byte/AST 동일하다. 새 집중 테스트에서 정상/오류 MockTransport canary 비노출·병렬/후행 로그 보존 및 만료 owner 상태 회귀도 실행됐다.
- VWorld 우선·Kakao 정상 무결과 보조 분류는 그대로다. 원천 payload/좌표를 재작성하는 새 provider 구현은 없다.
- 정상 주소/정상 무결과 좌표 캐시와 실제 checked_at/next_refresh_at 보존, 부분 수동 cycle 중 같은 결과 재호출 방지 코드는 유지된다.
- lease 만료 후 늦은 쓰기 차단과 이전 owner의 release가 새 owner를 지우지 않는 경계도 기존 집중 테스트로 재실행했다.
- 페이지 우선/재시도 교차, 중복 page key cursor advance 및 작은 배치 진행 보호는 보존됐다.
- address_dagster의 현재 location/job active-run 필터와 fixed force job/sensor 등록은 byte 동일하다. Daemon을 start/restore하는 코드가 추가되지 않았다.
- Common의 수동 cycle은 실제 run 수명/관리자 HTTP 요청의 멱등성을 대신하지 않는다. Weather 소비자에서 별도로 검토 중인 BFF 예약/표시 문제를 Common 수정으로 자동 해결됐다고 닫지 않는다.

## 본인이 실행한 검증

| 항목 | 독립 결과 | 제한 |
| --- | --- | --- |
| Manifest SHA·exact commit·시작/종료 tracked status | 일치, tracked clean | 미추적 작성자 로그 보존 |
| 고정 test_reverse_address.py + test_address_providers.py | **27 PASS**, 0.94초, skip0/exit0 | 소유 임시 Git-object 복사, Python -I -B, --noconftest, -p no:cacheprovider |
| AUTO=false 수동 실패 두 head 실제함수 | RED→GREEN | 신규 in-memory SQLite |
| unfinished manual + orphan 오류11 두 head | RED→GREEN | source join/limit 실제 SQLAlchemy 경로 |
| 삭제/비활성 정리 각각 | provider 추가0·한 번 종료 | 실제 원천 운영 변경 아님 |
| 좌표 변경, 필수 callback, 완료 callback 예외/재개 | PASS | 실제함수/서명, 외부 요청0 |
| base→head git diff --check | PASS | 소스 변경0 |

Root Common505/Ruff PASS 및 새4회귀 결과는 의뢰 정보다. 본인 검증과 합산하지 않는다. **의뢰 시 Common CI 일부 진행 중이었으며, 본인은 새 CI 상태를 조회/완료 확인하지 않았다. 진행 중 CI를 PASS로 집계하지 않는다.**

## 한계와 판정 범위

새 OPEN P0/P1/P2는 찾지 못했다. PASS는 고정14115ba Common 소스와 위 실제 실행 fixture에 한정한다.

- 실제 PostgreSQL row-lock/fencing·드라이버·격리수준·migration, 실제 provider 권한/이용조건/대형 응답/timeout/RSS/쿼터는 NOT_RUN.
- 실제 Dagster instance/job/sensor/Daemon과 실제 Admin 예약·UI·배포는 NOT_RUN.
- 두 소비자의 이번 WIP는 새 manifest의 정식 제품 baseline이 아니므로 읽거나 PASS 처리하지 않았다. pin/caller/DTO/UI/최종 CI는 별도 고정 소비자 리뷰 대상이다.
- 27개는 전체505 재실행이 아니다. address_dagster 테스트는 이번에 실제 SDK로 실행하지 않았고 정적/byte 보존 확인만 했다.
- 과거 closure의0f 제품 PASS는 역사로 보존하며 이번14115 제품/CI 수용으로 확대하지 않는다.
- HTTP hard realtime·모든 새/삭제 동시 변경·전원 손실 전 지점·미래 dependency logger 구조는 완전 검증하지 않았다.
- 원천 주소·관리자 좌표·과거 fact 보존, VWorld 우선/Kakao 보조, 위치별 달력6개월과 관리자 수동 예약, **Daemon OFF 유지** 조건은 바꾸지 않았다. 이번 검토는 Daemon ON 허가가 아니다.

종료 UTC: 2026-10-18T02:13:06.253201+00:00
