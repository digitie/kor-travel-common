# Common39 FULL post-fix r4 — James 독립 원문

- Review ID: COMMON39-JAMES-R4. Reviewer 실행 ID: /root/review_finish_a.
- 관점: 신뢰 경계·공개 API·상태 진실성·회귀 및 새 누락/재시도 결함 탐색.
- **판정: PASS — 고정 Common 소스·실행 fixture 범위. OPEN P0=0 / P1=0 / P2=0 / P3=0.**
- base: c48595880aaad4367802ad71af2525a8a5e17c6a.
- head: c067a7f6a11b106931a73cd7465503d90e54d976.
- 이전 제품: 14115ba99ab5d72d4f381d25b2dca810b24914d6.
- Manifest: /home/digitie/dev/reverse-address-common-review-manifest-20261018-r4.json.
- Manifest SHA256: 509036aca1b4d83ce190a42317cb007c3ca6515d3c7a225ae8151b89eb20659f.
- 시작: 2026-10-18 UTC 본 세션, 시작 분·초 사전 계측 없음. 종료는 끝에 기록.
- 새 peer 보고서·결과는 열람하지 않았다. 의뢰에 적힌 이전 B finding의 실패조건만 독립적으로 재현했다.
- 소비자 정식 리뷰/CI/배포 승인과 진행 중 Common CI 완료를 뜻하지 않는다.

## 격리·FULL 범위

Common AGENTS/runbook/review 기록 규칙을 앞선 검토에 이어 적용했다. base→head 21파일 2438+/2- 전체 변경의 제품·계약·설정 범위를 확인했고, 이전 FULL의 불변 부분과 새 delta를 Git object로 대조했다. 기존 r1/r2 closure archive는 역사적 원문으로 보존되는 범위이며 이번 r4 새 peer 판정으로 사용하지 않았다.

14115→c067 제품/가이드/시험 변경은 3파일이다.

- reverse_address.py: reuse의 same-cycle 유효기간, page의 SQL eligible 선택/5인자, 신규 _work, has_work의 전역 eligible 판단, refresh의 verified 조건/앞뒤 cursor wrap.
- test_reverse_address.py: 기존 mirrored list helper를 실제 SQL DatabaseAddressSource로 전환하고 새4회귀.
- docs/reverse-address-refresh.md: 새 callback과 cursor 순환·동일 cycle 만료 계약.

provider/Dagster 모듈, pyproject/lock는 이전 제품과 byte 동일하다. 기존 claim/fence/prepare/save/advance/release·좌표 identity·시간 계산·원천 보존 테이블 계약을 회귀 관점으로 재검토했다. 바뀐 page와 조건이 owner fence를 우회하는지도 별도 공격했다.

시작/종료 tracked status는 clean이고 작성자 미추적 .verify-address-common.log / .verify-address-common-r2.log가 있었다. 내용을 읽거나 수정하지 않았다. Git object의 메모리 compile 또는 종료 시 제거되는 소유 임시 복사만 실행했다. 소비자 WIP는 읽지 않았다.

운영/SSH/Docker/실제 provider·키·운영 DB/Daemon 시작0, source/index/branch 변경0. SQLite는 새 in-memory fixture만, provider HTTP는 MockTransport만 사용하고 socket.connect는 거절했다. Dagster 실제 인스턴스나 job은 실행하지 않았다. 이 보고서 외 새 영구 파일은 없다.

## 독립 이전→새 제품 대조

### 1. HTTP 중 cursor 앞 신규 위치가 생겨도 수동 오류가 숨기지 않는다

위치: reverse_address.py:417–428,465–497,642–649,708–713.

실제 SQL source에 z 한 곳을 두고 force·batch1로 실행했다. z resolver가 유한 실패를 반환하기 직전, 소유 fixture source에 key=a를 삽입했다. page snapshot 뒤에 생긴 앞쪽 위치이므로 단순 “처음에 미리 넣은 위치”만으로 시험하지 않았다.

| 관측 | 이전14115 | 새c067 |
| --- | --- | --- |
| 다음 has_work(automatic=False) | False | **True** |
| 앞쪽 a 저장 | 없음 | **ok** |
| provider 순서 | z | **z, a** |

새 end wrap은 뒤쪽 eligible이 없지만 앞쪽 eligible이 있으면 cursor를 빈 값으로 영속 저장하고 remaining=True로 남긴다. 다음 실행은 시작 쪽 SQL 선택으로 그 위치를 처리했다. 지속 실패 z의 backoff가 신규 위치를 가리는 이전 반례가 해소됐다.

이는 “실제 장애가 운영에서 발생했다”는 주장이 아니라 고정 함수/SQL source의 재현 결과다.

### 2. backoff뿐이면 sensor가 빈 run을 만들지 않는다

위치: :465–497.

a/b/c가 모두 실패한 뒤, 30초에 수동 force·batch1을 호출하고 60초의 pending을 읽었다.

| 관측 | 이전14115 | 새c067 |
| --- | --- | --- |
| provider requests | 0 | 0 |
| 아무 일 없이 소비한 skipped row | 1 | **0** |
| has_work(automatic=False), 아직 backoff | True | **False** |

새 _work와 global source 조회는 단순 cursor 뒤 row 존재 여부와 달리, 지금 처리 가능한 대상이 있는지를 판정한다. manual-cycle은 실패 때문에 유지되지만 due 전 불필요한 run은 억제된다. 실제 sensor 실행 대신 sensor가 호출하는 실제 source.has_work를 검증했다.

### 3. 같은 manual cycle도 6개월이 지나면 verified/cache 양쪽이 만료된다

위치: :258–276,670–676.

a/b는 동일 좌표 정상 주소, z는 다른 좌표의 지속 실패다. 첫 force cycle 뒤 200일을 진행시킨 가상 aware 시각으로 같은 cycle을 재개했다.

| 관측 | 이전14115 | 새c067 |
| --- | --- | --- |
| store.reuse(...force=True)에 만료 cache 반환 | True | **False** |
| a의 새 provider 조회 | 0 | **1** |
| a resolved_at | 최초 확인일 잔류 | **새 확인일** |

새 reusable cache는 cycle 일치 외 next_refresh_at>now를 요구한다. verified 분기도 같은 만료 기준이다. SQL _work가 expired row를 다시 고르고 cursor wrap이 이를 읽으므로 조건 하나만 고치고 실제 실행에서 영원히 건너뛰는 형태가 아니었다. b의 같은 좌표는 새 확인 결과를 재사용하며 확인일을 허구로 연장하는 변경도 없다.

### 4. 정상 prefix가 batch1을 소비하지 않는다

위치: :417–428,465–475.

a/b를 정상 확인한 뒤 아직 주소가 없는 z를 추가하고, 자동 실행을 batch1로 호출했다.

| 관측 | 이전14115 | 새c067 |
| --- | --- | --- |
| requests | 0 | **1** |
| skipped | 1 | **0** |
| z 저장 | 없음 | **ok** |

eligible을 SQL에서 limit 이전에 적용한 효과가 실제 함수에서 확인됐다. 전체 자료를 Python에 가져와 필터링하는 구현이 아니며, page의 반환 수는 SQL limit에 의해 제한된다. 다만 실제 대규모 SQL query-plan/CPU/RSS 측정은 하지 않았다.

## 새 wrap의 ownership 공격

첫 page 읽기에서 원 owner의 lease가 끝나고 다른 owner가 +91초에 인수하도록 소유 fixture를 구성했다. 원래 cursor는 z이고 앞쪽 a가 남아 있어 wrap이 필요한 조건이다.

새 reset-cursor의 store.advance는 기존 owner fence를 사용했다. 결과:

    OwnershipLost 발생
    provider calls == 0
    control.owner == "new-owner"

finally의 이전 owner release가 새 owner를 지우지 않았다. 새 wrap이 무조건 cursor를 덮어쓰거나 lease를 잃은 worker가 외부 조회를 시작하는 회귀를 만들지 않았다. 이는 SQLite 실제 메서드 증거이며 PG row-lock/전원 손실 재현으로 확대하지 않는다.

## 공개 API·상태·이전 보호 재검토

새 callback 계약은 다음과 같다.

    page(cursor, limit, now, cycle, force)
    retries(now, limit)
    pending_failures()

refresh_reverse_addresses의 첫 page, wrap page, 종료 lookahead 모두 다섯 page 인자를 전달한다. bound DatabaseAddressSource.page가 실제로 이 다섯 인자를 받는지 inspect.signature binding으로 확인했다. pending_failures는 필수 keyword-only를 유지한다.

DatabaseAddressSource.page의 now=None 기본 2인자 호출은 기존 단순 원천 조회로 남아 있지만, refresh 경로는 항상 aware now와 cycle/force를 전달하여 SQL _work를 적용한다. 미머지 신규 API의 소비자는 bound source 메서드를 전달해야 하며, 옛 2인자 custom callback이 새 refresh에 자동 호환되는 것은 아니다. 가이드가 이 변경을 명시한다.

수동 force에서 _work는 현재 due 또는 다른 cycle의 정상 미확인 결과를 고르며, 실패 row는 next_retry/좌표 변경 조건을 존중한다. 누락 row는 LEFT JOIN의 target_key NULL 조건으로 처리한다. page와 sensor가 같은 eligible 의미를 사용하여 “sensor는 켜지는데 worker는 기다리는 row만 읽는” 불일치를 줄였다.

AUTO=false에서도 이미 시작한 manual-cycle 실패의 backoff 재개, 삭제/비활성 원천 정리1회, orphan 오류11개의 retry-slot 독점 방지 수정은 유지된다. 해당 이전 회귀는 새 실제 SQL helper로도 실행됐다.

summary의 in_progress는 유효 lease 또는 cursor/manual pending을 의미한다. backoff pending을 실제 실행 중 worker라고 표현하지 않는 소비자 책임은 남는다. 만료 owner만 남은 완료 상태의 이전 본인 지적 수정은 그대로다.

VWorld 우선/Kakao 보조, 정상 무결과 분류/캐시, 원천 주소·관리자 좌표·fact를 별도 파생 결과와 분리하는 경계, HTTPX/HTTPcore private ContextVar 로그 보호는 변경되지 않았다. 실제 MockTransport 정상/오류 로그 및 후행·병렬 로그 보존 회귀도 집중 실행에 포함됐다. 재시도/커서의 새로운 문자열이나 provider 원문을 API/log로 출력하는 경로는 추가되지 않았다.

address_dagster는 byte 동일하며 pending callback에 따라 fixed own-location/job의 실행을 예약한다. 실제 Daemon을 시작하거나 자동 복구시키는 변경은 없다. BFF request-id의 원자적 예약이나 소비자 replay 상태 표시는 이 Common 수정의 해결 범위가 아니며 별도 소비자 판정을 유지해야 한다.

## 본인 검증 결과

| 검증 | 결과 | 범위 |
| --- | --- | --- |
| Manifest SHA·exact commit·tracked status | 일치/clean | 작성자 미추적 로그 보존 |
| 고정 test_reverse_address.py + test_address_providers.py | **31 PASS**, 1.31초, skip0/exit0 | Git-object 임시 복사, Python -I -B, --noconftest, -p no:cacheprovider |
| HTTP 중 prefix 삽입·global pending·처리 | 이전 RED → 새 GREEN | 인메모리 SQL source/실제 함수 |
| backoff-only 수동 run 판정 | 이전 RED → 새 GREEN | provider0, pending False |
| 같은 cycle200일 cache/verified 만료 | 이전 RED → 새 GREEN | expired cache 거절 + 실제 재조회 |
| healthy prefix batch1 | 이전 RED → 새 GREEN | eligible SQL limit |
| wrap 직전 owner 인수 | stale 작업 거절·외부호출0·새 owner 보존 | 실제 함수/SQLite |
| 5인자 bound page·필수 pending callback | signature binding 확인 | 실제 consumer import 아님 |
| base→head diff --check | PASS | 변경0 |

root 엔진23/전체509/Ruff 및 소유 PostgreSQL17 drill 결과는 의뢰된 외부 증거이며 위 수치와 합산하지 않는다. **의뢰 시 최신 CI가 진행 중이었고 본인은 새 CI 완료 상태를 조회하지 않았다. 진행 중 CI를 PASS로 집계하지 않는다.**

## 판정 한계

새 OPEN P0/P1/P2는 발견하지 못했다. PASS는 exact c067a7f의 Common source와 위 fixture 범위다.

- 실제 PostgreSQL·Numeric/Float planner/행락·migration·드라이버, 실제 provider 권한/이용조건/대형 응답/속도/메모리는 NOT_RUN.
- 실제 Dagster SDK instance/job/sensor·실제 브라우저/관리자 API·소비자 최종 CI·배포는 NOT_RUN.
- 소비자 WIP 및 그 formal gate는 별도이며 새 Common pin/callback 연결의 승인으로 이 보고서를 사용할 수 없다.
- 31개는 전체509 재실행이 아니다. 실제 address_dagster 실행은 하지 않았다.
- 기존 historical closure 원문과 실패 보고서는 수정하지 않았다. 과거 PASS를 새 제품의 CI·운영 효과로 확대하지 않았다.
- cursor 순환의 모든 동시 원천 변동·시계 역행·프로세스 강제 종료 지점을 완전 증명한 것이 아니다. 실제 장시간/대량 처리의 CPU·RSS·SQL query-plan도 측정하지 않았다.
- 최종 의미는 VWorld 우선/Kakao 보조, 위치별 달력6개월과 Admin 수동 예약, 원천 보존이다. **Daemon OFF 정책을 유지하며 시작/restore는 실행하지 않았다.**

종료 UTC: 2026-10-18T02:25:09.295894+00:00
