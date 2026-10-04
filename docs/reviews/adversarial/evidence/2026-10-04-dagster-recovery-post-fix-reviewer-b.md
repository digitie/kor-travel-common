# Reviewer B post-fix 원본 적대 리뷰

실행 ID: `B-20261004-DAGSTER-RECOVERY-POSTFIX-01`

- 검토 시각: `2026-10-04T10:15:01+09:00`~`10:18+09:00`.
- common: base `be7f21f2a645f4ce882b3d841487e1b40ad23425`, post-fix `50d2db4c7c7e0154dd863defb62d4b9fa3b5bec3`.
- weather: base `5da6e158dccc8ea98e8301078ce9610525da0ebf`, post-fix `1218c8f656408d04f745bf5773ec910a36538bc5`.
- 최초 후보 대비 수정과 원래 base 대비 전체 변경 범위를 확인했다.
- 격리: 고정 Windows Git commit 객체의 show/diff/rev-parse, 객체 내 tgz 바이트와 고정 Python AST만 읽었다. source 수정·checkout·빌드·운영 조작은 하지 않았다.
- 동일 post-fix manifest를 읽었으며 상대 reviewer의 post-fix 결과는 받거나 열람하지 않았다.

**Verdict: PASS**

내 원본 finding 네 건은 모두 **FIXED**로 재확인했다. 새 P0/P1/P2/P3 finding은 발견하지 않았다. 이 verdict는 검토한 코드와 계약에 대한 판정이며, 사용자 필수 live e2e·최종 회귀·CI 완료를 대신하지 않는다.

## 원본 finding closure

| finding | 판정 | 독립 확인한 근거 |
|---|---|---|
| B-P2-01 특보 전체 fact 누적 | FIXED | 특보도 KMA_STAGE_VALUES/KMA_STAGE_SOURCES에서 flush_alert_batch로 게시하고 fact/source buffer를 clear한다. 전체 normalized_values_total은 flush 뒤에도 유지한다. run 전체에는 location ID 집합만 유지한다. |
| B-P2-02 회수 첫 페이지 starvation | FIXED | started_at/run_id 복합 keyset과 tie-breaker로 bounded page를 순회한다. 생존 첫 페이지에서 회수 0건이어도 다음 cursor로 진행한다. |
| B-P2-03 동적 정책 입력 허용 | FIXED | 상한은 bool을 제외한 실제 int, 멱등성은 실제 bool만 허용한다. 고정 commit AST로 nan/inf/float/string/bool 여덟 경계가 ValueError로 거절됨을 직접 실행했다. |
| B-P2-04 architecture 게시 계약 충돌 | FIXED | 기존 architecture가 수집/provider/parse/DB/lease 실패 모두의 부분 commit 보존·누적 예산을 설명한다. 과거 전체 staging 메모리 실측을 역사로 구분하고 lazy chunk/특보 incomplete 계약을 갱신했다. |

### B-P2-01 재공격

복수 notice가 같은 location에 매칭되는 상황을 따라 읽었다. 어느 batch에서든 빠진 location은 alert_skipped_locations의 union에 남아 이후 notice 성공으로 누락이 숨겨지지 않는다. alert_locations_published는 어느 batch에서도 게시된 location이 없는 경우와 일부 notice가 게시된 경우를 구분한다.

현재 notice가 fan-out 도중 flush될 때 source를 다시 넣으므로 후속 fact에도 lineage/run ownership이 포함된다. raw-only source는 25개 상한에서 별도로 게시한다. skip 재시도는 최대 5,000개 fact staging 안에서 수행하며 이전 전체 fact를 계속 붙잡지 않는다.

새 테스트의 전국 100 target × 3 notice, 이전 notice skip/이후 성공, flush 뒤 예산 초과/20개 commit 보존을 읽었다. 기존 skip/starved/partial 정책 시험도 delta와 함께 확인했다.

### B-P2-02 재공격

첫 페이지가 모두 살아 있는 경우, 같은 started_at인 행들, 페이지에서 terminal 행을 제거한 뒤 다음 페이지, 마지막 정확히 limit개인 페이지 뒤 빈 페이지를 검토했다. cursor는 읽은 페이지의 마지막 원래 key를 사용하므로 회수 UPDATE 때문에 뒷부분이 건너뛰어지지 않는다.

metadata 조회는 앱 transaction 밖에서 수행하며 기존 missing-ID heartbeat CAS를 보존한다. 두 행을 같은 started_at으로 만든 limit=1 회귀 시험이 추가되었다.

### B-P2-03 직접 실행

고정 common source에서 RecoveryPolicy 클래스 AST만 메모리로 추출해 다음 입력을 실행했다.

- max_runtime_seconds: nan, inf, 1.5, "300", True
- idempotent="false", infrastructure_retries=1
- infrastructure_retries=1.5
- infrastructure_retries=True

모두 ValueError였다. 정상 RecoveryPolicy(300, idempotent=True, infrastructure_retries=1)는 기존 runtime/retry/project/job 태그를 그대로 생성했다.

### B-P2-04 문서 대조

weather architecture와 recovery runbook은 새 streaming/부분 게시 계약에서 일치한다. 원천 필드/raw payload/unique replay/CAS를 그대로 유지하며, 운영 RSS를 합성 tracemalloc 결과로 보증하지 않는 제한도 유지했다.

## 추가 변경 검토

### 실패 로그 pagination과 대기 상한

GraphQL eventConnection은 limit1000/afterCursor/cursor/hasMore를 사용한다. 브라우저가 임의 GraphQL이나 foreign repository scope를 넣을 수 없도록 기존 named-operation 허용 목록과 server scope 주입을 유지한다. 선택 cursor는 null 또는 길이 512 이하 문자열만 허용한다.

실패 원인 조회는 한 page만 보관하고 마지막 step failure만 작은 상태로 유지한다. 같은 cursor 반복·hasMore=false·cursor 없음에서는 멈춘다. 최대 20 page 및 20초 다음 요청 시작 예산, 각 fetch 10초 timeout이 있다. 이는 정확한 20초 전체 완료 보장이 아니라 마지막 요청에 최대 10초가 추가될 수 있는 시작 예산이며 문서도 이를 정확히 설명한다.

실패 로그 조회 실패는 FAILURE 목록을 삭제하지 않고 원인 미확인으로 처리한다. 두 번째 page의 RunFailureEvent를 읽는 회귀 시험을 확인했다.

### artifact·의존성·CI

weather root 및 Dagster 패키지 dependency와 uv.lock이 동일 common 전체 post-fix SHA를 가리킨다.

고정 weather tgz 객체를 직접 열어 다음을 확인했다.

- UI archive SHA-256: `1d5ed07dce5f82a631d33d8d505af4c80aab3c0dc9a7775067fc67f71914e5ca`.
- README digest와 일치.
- archive SHA-512와 package-lock node_modules/@kor-travel/ui integrity가 일치.
- archive CSS에 --kt-destructive가 포함되고 --kt-error는 없음.
- archive dist에 새 schedule-detail public slot이 포함됨.
- LICENSE·NOTICE·THIRD_PARTY_NOTICES를 유지.

양 저장소 base 대비 git diff --check는 통과했다. common Python CI는 locked sync 후 --no-sync로 검사하며 core-only wheel import 경계 시험을 유지한다.

원본 보고서의 weather Dagster 1.13.20 표기는 잘못된 버전이었다. 이번 고정 weather uv.lock에서 **1.13.24**를 직접 확인했다. 원본 보고서는 수정하지 않고 여기서 정정한다. 원본의 1.13.20 공식 구현 대조는 그 버전의 참고였으며 실제 소비자 runtime 검증으로 집계하지 않는다.

### 확산 적용 가이드

새 dagster-adoption 가이드는 앱 소유 SQL/DB/provider/auth와 common 소유 정책/예약/sensor/deadline/UI 경계를 유지한다. 전체 SHA 고정, 실제 daemon 설정 선행, 비멱등 outbox 재시도 금지, 직접 resolve한 executor의 실제 설정 확인, 누적 예산/전국 fan-out/raw-only/CAS 회귀를 안내한다.

다른 소비자가 이미 채택했다거나 shared plane 설정을 적용했다고 주장하지 않는다. migration 선행 및 실제 OS process 종료·서비스 관리자 복구 경계도 명시되어 있다.

## 검증과 남은 불확실성

**직접 실행/확인**

- 고정 hash와 전체 delta/source/관련 테스트·문서 재검토.
- RecoveryPolicy AST 여덟 잘못된 입력 거절 및 정상 태그 생성.
- vendor archive digest/lock integrity/실제 CSS·slot 배포 내용 확인.
- 두 저장소 base 대비 git diff --check.

**읽은 evidence**

manifest의 common Python21/UI34, Python3.11+Dagster1.9 floor21, weather 회수/특보25 PASS 기록을 읽었다. 해당 전체 suite를 리뷰어가 독립 재실행한 것은 아니다.

**NOT_RUN**

- 최종 whole pytest/frontend 회귀 및 clean artifact install 결과.
- 최종 live UI e2e·computed style/모바일/로그인/실패 상세 확인.
- 최종 PR CI 및 merge gate.
- shared daemon 설정 배포·운영 launcher crash/hard hang/native retry 장애 주입·OS process 회수·host RSS 실측.

코드 리뷰 finding은 닫혔다. 부모가 진행 중인 live 브라우저/최종 회귀/CI를 실제로 완료하고 evidence를 연결한 뒤 사용자 승인 범위의 merge를 진행할 수 있다.
