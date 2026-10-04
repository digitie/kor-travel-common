# Reviewer A 원본 post-fix 적대 리뷰

- 실행 ID: `A-POSTFIX-20261004-50d2db4c-1218c8f6`
- 시작 기록 시각: `2026-10-04 01:14:43 UTC`
- 종료 기록 시각: `2026-10-04 01:16:06 UTC`
- common base: `be7f21f2a645f4ce882b3d841487e1b40ad23425`
- common post-fix candidate: `50d2db4c7c7e0154dd863defb62d4b9fa3b5bec3`
- weather base: `5da6e158dccc8ea98e8301078ce9610525da0ebf`
- weather post-fix candidate: `1218c8f656408d04f745bf5773ec910a36538bc5`
- 격리: Windows Git의 고정 commit `show`, `diff`, `rev-parse`로 객체만 읽었다. manifest와 본인 원본 finding을 기준으로 재검토했다. 소스 수정·빌드·테스트 실행은 하지 않았다. 상대 post-fix report는 제공받거나 참조하지 않았다. 이 원본 report 파일 생성만 수행했다.
- 판정: **CONDITIONAL — 본인 finding은 모두 코드상 CLOSED이며 신규 blocking finding은 없다. 최종 live UI e2e·전체 회귀·clean artifact 설치·CI evidence가 확정된 뒤 merge 가능하다. 현재 진행 중인 검증의 통과를 주장하지 않는다.**

## 본인 finding closure

| 원본 ID | disposition | 고정 candidate에서 확인한 근거 |
|---|---|---|
| A-P2-01 | CLOSED | common `packages/ui/dagster.css:19,21`이 배포된 `--kt-destructive`를 사용한다. 운영 CSS의 모든 토큰 이름을 실제 tokens.css와 대조하는 회귀 시험을 추가했다. 브라우저 computed color/border는 최종 live evidence 대상이다. |
| A-P2-02 | CLOSED | component가 schedule과 repository 문맥을 함께 보존한다. key/확장 상태는 JSON으로 직렬화한 location/repository/schedule 복합 identity이다. `scheduleUrl(name, repository)`로 링크 문맥을 전달하며 기존 1인자 weather callback은 호환된다. 동명 schedule을 가진 transport/geo 두 repository의 독립 확장과 링크 회귀 시험을 추가했다. |
| A-P3-01 | CLOSED | root의 공개 `data-slot`, 선택 `testId`, refresh/error/summary/run-table/schedule-table/detail 슬롯을 추가하고 공개 계약에 기록했다. 최근 실행 표에 가시적인 `상세` column header를 제공한다. root 슬롯·testId·header 회귀 assertion을 확인했다. |
| A-P3-02 | CLOSED | weather globals의 desktop 외부 좌우/상단 margin 및 두 mobile breakpoint의 좌우 margin selector에 `.main > .kt-dagster-operations`를 포함한다. 공용 내부 간격과 consumer의 외부 gutter 책임을 적용 가이드에 명시했다. 실제 viewport 정렬은 최종 live evidence 대상이다. |

## 추가 delta와 공격 시나리오

원래 base 대비 전체 변경 범위를 다시 확인하고 최초 candidate 이후 변경된 source·공개 계약·적용 가이드·의존성 metadata·회귀 시험을 읽었다. 생성된 대형 lock의 모든 transitive dependency를 독립 감사한 것은 아니다.

- **실패 로그 pagination:** eventConnection의 page 크기를 1,000으로 줄이고 afterCursor/cursor/hasMore를 추가했다. client는 한 page의 이벤트만 유지하고 최대 20 page를 조회한다. 뒤 page의 RunFailureEvent를 찾아 표시하는 회귀 시험을 확인했다. cursor 미변경/누락 또는 hasMore=false에서 종료하며 마지막 step failure fallback을 보존한다.
- **조회 정지와 예산:** client 및 server proxy fetch에 10초 AbortSignal timeout이 있다. failure detail loop는 시작 후 20초 안에서 다음 요청을 시작하는 예산을 사용한다. 이는 전체 조회가 정확히 20초 안에 끝난다는 계약이 아니며 마지막 요청의 최대 10초가 추가될 수 있다. runbook이 이 의미를 정확히 적었다. detail 조회의 timeout/오류는 null로 반환하여 FAILURE 상태를 숨기지 않는다.
- **cursor로 tenant 우회:** cursor는 null 또는 길이 512 이하 문자열 변수로만 허용한다. server 소유 runId/tag filter와 GraphQL 문서가 유지되므로 새 cursor가 repository scope를 override하거나 raw mutation을 전달하는 경로를 찾지 못했다. 선택 cursor가 없던 기존 operation 호출도 수용한다.
- **표시 및 callback 회귀:** schedule callback 문맥 추가가 weather의 1인자 함수 사용을 막지 않는다. JSON composite identity는 임의 delimiter 충돌을 피한다. maxRuntimeSeconds 판정·React text escaping·pending refresh 억제·requestVersion guard가 유지된다. 마지막 확인 시간도 명시적으로 Asia/Seoul을 사용하도록 수정되었다.
- **로그인/메뉴:** 후속 delta가 기존 auth adapter나 shared LoginForm/AppMenu를 변경하지 않았다. 최초 리뷰에서 확인한 local redirect sanitize, password clear, inFlight guard, consumer 소유 logout/Link/pathname 계약이 유지된다.
- **새 적용 가이드:** common/consumer 책임, 전체 SHA 의존성, native instance 설정 선행, 비멱등 작업의 자동 재시도 금지, NOT_STARTED 예외, RPC/DB 상한, terminal/lease CAS, pagination, raw/fact staging, 부분 commit/replay, deadline의 thread 비취소 경계, UI scope와 외부 여백, 운영 NOT_RUN 구분이 코드와 맞는다. 다른 소비자 채택을 완료로 표시하지 않는다.
- **회수·메모리 후속 변경:** strict RecoveryPolicy 정수/boolean 검증, 회수 후보의 started_at/run_id keyset, 특보 bounded staging 및 전체 normalized 예산, notice별 skip을 run 전체 incomplete 집합에 보존하는 변경과 회귀 시험을 읽었다. 첫 생존 page 뒤 terminal 행을 누락하지 않는 방향이고, 이후 notice 성공이 이전 skip을 제거하지 않는다. 본 reviewer의 관점에서 신규 P0/P1/P2는 찾지 못했다. 실제 DB race·process 종료·native retry는 실행하지 않았다.
- **artifact metadata:** weather pyproject 두 곳과 uv.lock이 동일 common `50d2db4c...`를 고정한다. vendor README의 SHA도 일치한다. common smoke와 weather lock의 UI integrity가 같은 새 sha512로 갱신되어 있다. archive digest 재계산 및 clean 설치의 실제 통과는 작성자가 진행 중인 final evidence 대상으로 남긴다.

## 신규 findings

신규 blocking finding 없음. 본인 원본의 네 finding은 위 근거로 코드상 닫았다. CSS·ARIA·viewport의 실제 동작과 artifact 재현성은 정적 검토만으로 통과를 확정하지 않는다.

## 검증과 미검증 경계

manifest의 common Python21/UI34, Python3.11+Dagster1.9 floor21 및 weather 회수/특보25 통과 기록을 읽었다. 독립 실행한 결과로 주장하지 않는다. 최종 전체 Python/frontend 회귀·CI·clean tarball 설치·live browser e2e는 진행 중이다.

merge 전 final evidence에는 실제 브라우저의 로그인 실패/성공/로그아웃·메뉴 선택, 실패 로그 표시/조회 재시도, job별 상한, schedule 확장/링크, 작은 viewport, computed 오류 색상/테두리 및 gutter 정렬이 포함되어야 한다. 최신 두 candidate에 대한 최종 검증과 두 reviewer post-fix disposition을 연결한다.

운영 Dagster 장애 주입·shared daemon 설정 반영·launcher의 OS process 종료·native retry child 실행·운영 RSS·다른 앱 채택은 이 검토에서도 **NOT_RUN**이다. 코드 merge의 검증과 운영 배포 완료를 구분하는 현재 문서의 제한은 적절하다.
