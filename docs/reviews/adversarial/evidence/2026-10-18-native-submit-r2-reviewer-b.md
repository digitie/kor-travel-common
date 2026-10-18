# Common41 post-fix 독립 적대 리뷰 — Popper B r2

**판정 BLOCK / OPEN P0=0, P1=1, P2=0, P3=0.**

기존 C41-B-P1-01의 정상 동시-submit 경합은 SQLite .24/.25에서 CLOSED다. 다만 별도 PostgreSQL lock-session이 사라질 때 같은 상태 역행이 다시 발생하는 C41-B-P1-02를 실제 소유 PG에서 재현했다. 원23e BLOCK 보고서는 수정하지 않았다.

## 요청·불변 입력·격리

최초 요청은 /home/digitie/dev/common41-review-popper-r1.md에 전문 보존했다. 이번 후속 parent 지시는 다음과 같다.

> Common38 최신main정합 독립리뷰 진행. ... A41fix freeze되면P1closure우선으로돌아갈예정.

> 네 2704830 P1closure우선. 실제PG필요하면 root소유127.0.0.1:15436 weather/weather 신규DB common_native_review_b 생성사용허용(기존DB변경금지), ownSQLite/.24/.25새lock/freshread/nativepool미점유도확인. 원문23eBLOCK보존. 38진행끝난부분유지후41끝나면38복귀.

소유 테스트 credential은 parent가 제공한 격리 fixture 전용이며 운영 credential/env를 읽지 않았다. 이 인용은 실제 전달 메시지이며 별도 운영 URL/비밀 파일 내용은 없다.

- base27cd146ed9e83d3ef481757d2b48e16f232dc88c.
- 이전제품23e4775cf883b672ababad1b291bddd3441c9c63.
- exact수정2704830e98c4353e9770368eb1aea21833015b4a.
- WT/home/digitie/dev/kor-travel-common-codex-native-submit-20261018의 Git object만 읽었다. source/index/branch 변경0.
- 소유 복사/fixture: /home/digitie/dev/common41-popper-r2-916a61c1f9.
- 시작 UTC2026-10-18T04:51:36.141411Z, 마지막 증거수집04:56:15Z, 종료는 말미 기록.
- 원본과 같은 Python .24/.25 환경을 읽기 전용으로 사용하고 source는 exact270에서 복사했다. sterile env/HOME/PYTHONPATH/confcutdir/cache-off 유지.
- 새 peer 리뷰/결과는 읽거나 요청하지 않았다. A는 작성자이며 root 요청에 따라 이전 원반례 및 새 실패 interleaving만 전달했다.
- 실제 PostgreSQL은 parent가 허용한 신규DB common_native_review_b만 생성/사용했다. 기존DB DDL/DML·운영·SSH·Docker·provider·daemon·실worker 실행0.

## 변경 전체 확인

23e→270은 module/extra/lock/tests와 중간 문서 이력 포함7파일506삽입/33삭제다. 실제 lock 구현, main27cd→270의 기존 전체 기능 연결, 새 시험, 문서 전체 delta를 읽었다. module SHA256 45a9fce0bbbd54b36618149e1273978a23880d22f4719ca04d3d8f8f64b3b254.

새 _submission_lock:
- SQLite native run DB의 parent 아래 소유0700 디렉터리/UUID별 regular0600 single-link 파일에 nonblocking flock. unlink하지 않아 inode split race를 피하고 FD close/process exit로 해제.
- PG native run storage의 URL을 사용한 별도 NullPool engine/session에 pg_try_advisory_lock. native engine checkout을 잡은 채 submit하지 않으려는 구조다. 새 pg extra와 SDK별0.29.24/.25 검사를 추가.
- 잠금 안에서 run을 새로 읽고 _same_request 후 NOT_STARTED만 submit한다. queued/진행/종료는 submit하지 않는다.
- permission/selector/config/hash/native schema/CLI/lazy import의 기존 경계는 변경하지 않는다.

## 기존 C41-B-P1-01 — 정상 경합 CLOSED

실제 .24/.25 SQLite에서:
1. create이후submit전중단으로 NOT_STARTED1행.
2. 첫 replay가 실제 native submit의 coordinator 입구에서 지연.
3. 두 번째 replay는 SubmissionBusyError로 즉시 거절되며 두 번째 coordinator 호출0.
4. 첫 제출 완료 뒤 native PIPELINE_START를 저장.
5. 재전송은 기존STARTED를 반환하고 추가enqueue0.

새 own tests/test_popper_sqlite_closure.py는 이전 반례를 보존한 채 별도 작성했다. actual adapter/native coordinator/storage를 호출하고 성공을 위해 알고리즘을 재작성하지 않았다.
- .25: exact product44 + own1 =45PASS/14.90초.
- .24: exact product44 + own1 =45PASS/14.57초.
- 제품44에는 프로세스재개/response-loss/일반경합/lock-exception/crash-release 및 이전39계약 회귀가 포함된다.
- own closure SHA256 7aaa2b72e89aaf441e01cebf6b485813e10c8e110e6da5bf580102cabbb779a3.
- sqlite25.stdout SHA256 8e56958bfd23d92845713f441e869205801f6a25653ba9157e7fc868068039cf.
- sqlite24.stdout SHA256 762f986e49435dced57ec2753f693ada67c8a8c1307f195cb091bd57147726a6.

이는 정상 lock 생존 동안의 P1-01 closure이며 아래 session-loss 실패를 닫지 않는다.

## C41-B-P1-02 — PG 잠금 세션 단절 뒤 기존 submit이 계속돼 STARTED를 재enqueue

- 심각도 P1, OPEN.
- 위치 packages/py/kor-travel-common/src/kortravelcommon/dagster_webserver.py:184–208 및259–265.
- guard의 PG session은 native run storage submit connection과 별개다. lock session이 끊겨 서버에서 advisory lock을 해제해도, 이미 critical section 안에 있는 Python 호출/native coordinator는 취소·fencing되지 않는다. unlock 시 오류를 뒤늦게 내는 것은 이미 실행한 상태 변경을 되돌리지 않는다.

### 실제 재현

parent 허용 신규 DB를 생성했고 실제 Dagster1.13.25/PostgresRunStorage0.29.25를 사용했다. run storage만 신규PG, event storage는 소유SQLite다. remote job/plan RPC만 소유 in-memory fixture로 대체했으며 create_run/submit_run/native 저장소/PG session advisory는 실제 함수다.

1. create후submit전소유예외로 NOT_STARTED1행을 만든다.
2. 같은 request의 첫 replay가 새 PG advisory lock을 획득하고, native coordinator에 이미 NOT_STARTED snapshot을 전달한 직후 지연한다.
3. 신규DB의 pg_locks에서 해당DB granted advisory backend가 정확히1개임을 확인하고 그 backend만 pg_terminate_backend로 종료한다. 전체PG나 다른DB/backend는 종료하지 않는다. 이는 실제 잠금 연결 단절을 재현한다.
4. 둘째 같은 request는 해제된 advisory lock을 획득해 native enqueue한다.
5. native PIPELINE_START 이벤트를 저장하고 실제 run status가 STARTED임을 재조회한다.
6. 첫 호출을 풀면 기존 stale SubmitRunContext가 다시 enqueue한다. 첫 요청은 finally unlock에서 OperationalError를 내지만 이미 쓰기는 끝난 뒤다.

안전 결과투영:
- same_id=true, row_count=1.
- calls=[NOT_STARTED, NOT_STARTED].
- events=[PIPELINE_ENQUEUED, PIPELINE_START, PIPELINE_ENQUEUED].
- final=QUEUED.
- first_error=OperationalError.

safe 원문: pg-lock-loss.safe.json, SHA256 c6968c5d2e8176fcc1bb00b43b7b6f0b5811d7bd0b00194861e968521a06d851. 경로는 위 소유fixture root 아래다. 실제 프로그램은 fixture 연결정보가 포함된 .private.py로 보존했고 공개 보고서에 값을 복제하지 않는다. 이미 root와 A에게 interleaving을 즉시 전달했다.

native GraphQL 요청은 별도 thread에서 실행되므로 단일 webserver 프로세스에서도 가능한 경합이다. backend 연결 종료는 PG 재시작과 동일한 전체 DB 실패만을 뜻하지 않는다. lock session만 네트워크/관리/idle 정책 등으로 끊기는 동안 native storage의 다른 연결은 살아 있을 수 있다.

영향: run 한 개 보존과 별개로 실행 상태를 queue로 역행시키며 native daemon이 재선택할 수 있는 상태를 만든다. 실제 daemon/두 번째 worker는 금지 범위이므로 실행하지 않았다. 원외부효과 중복을 발생시켰다고 주장하지 않고, 그 전제인 실제 run-state 역행과 재enqueue를 입증했다.

권고: session lock 생존과 native enqueue가 별도 연결의 독립 I/O인 점을 해결해야 한다. unlock 실패를 보고하거나 추가 선행 SELECT만 하는 것으로 이미 진행한 stale submit을 fence할 수 있다고 주장하지 않는다. native 상태 전이의 원자성/claim, 동일 요청의 추가 보호와 지원 프로세스 범위를 명확히 하고 locksession-loss 반례를 고정해야 한다. 실제 수정은 작성자 소유이며 본인은 제품을 수정하지 않았다.

## 준비 실패와 미정산 경계

다음은 제품 반례/PASS와 구분한다.
- 최초 fixture CREATE DATABASE를 psycopg2 connection context 안에서 실행해 ActiveSqlTransaction으로 실패했다. 별도 autocommit connection으로 고친 뒤 신규DB를 생성했다.
- 다음 fixture는 새 native_storage_config 인자를 빠뜨려 TypeError였다. 실제 제품 테스트 fixture의 새 signature를 읽고 소유 r3 파일로 정정했다. 같은 소유 신규DB가 비어 있음을 확인하고 실제 반례를 실행했다.
- 이후 nativepool 미점유 양성+DB정리를 함께 한 보조프로그램은30초 timeout이었다. 별도 bounded cleanup은 QueryCanceled로 끝났다. 성공 투영이 없어 미점유/정리완료로 세지 않는다. 이 보조실패가 성공한 위 session-loss 결과를 바꾸지 않는다.
- 소유 신규DB는 잔존 가능하며 parent에게 미정산을 알렸다. 기존DB/다른세션 종료/재시도는 하지 않았다. 삭제완료를 주장하지 않는다. 새source/daemon/process 운영변경은 없다.

## 남은 범위

PG session-loss는 실제SDK.25에서 실행했으며 .24 PG 동등 실패를 새로 실행한 것은 아니다. SQLite 정상closure는 양SDK 직접 실행했다. PG busy/release/nativepool 미점유 전체 수용, 운영/실provider/실worker/daemon/HTTP/브라우저·소비자·Manager 배포, 새 wheel 설치/fullpackage/최종CI는 NOT_RUN 또는 위 실패 한계다.

이 원문은270 제품까지 고정하며 A의 이후 docs/fix는 포함하지 않는다. parent의 기존 merge/deploy 권한을 철회하거나 새로운 사용자 승인 조건으로 확대하지 않는다. source/lock 제품을 바꾼 새 HEAD와 P1-02 반례 closure가 후속이다.

종료 UTC: 2026-10-18T04:57:06.070298+00:00
