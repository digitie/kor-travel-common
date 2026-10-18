# Common41 892 독립 재검토 — 제품 OPEN0, 문서 후속 대기
- 요청: 원 P2 timeout 반례 및 a68→892 전체 변경을 독립 검증. peer 원문/작성자 모형 미열람.
- 불변 제품 HEAD: 89291f36d731ab906161b96757522e1cd833b4ef.
- 원 제품 a68d0495acc38906c31b95b1d0db163bd8f96f5b 및 P1/P2 RED 원문은 보존.
- 모듈 SHA256: 90e06b70e77258cef25c5c6f0e6e9100458480d1ff1bb7e58cf745606992240f.
- 판정: SOURCE_PASS_PRODUCT_DOCS_PENDING. 제품 열린 P0/P1/P2/P3 0. 아래 문서 정정 전 전체 문서 binding은 보류한다.

## 원 P2 closure
a68은 native optimize_for_webserver(80ms) 뒤 제출 연결에서 timeout=0이었다.
892 _submission_engine(148–164)는 native Pool.recreate()로 creator/connect 정책을 계승한다.
동일 own PG 반례의 .24 및 .25 모두 native=bound=80ms이고 pg_sleep(0.2)가 양쪽에서 취소됐다.
별도 PG fixture는 NullPool/QueuePool 각각 URL lock_timeout73ms/connect_timeout3와 native statement_timeout111ms 또는 optimize91ms, AUTOCOMMIT을 보존했다.

## 실제 검증
각 SDK 66 PASS: immutable 제품 집중+기존 자체 SQLite 62, 자체 PG 4.
.24/SQLAlchemy2.0.54: SQLite38.81s; PG3개7.19s+추가 정책1개1.37s.
.25/SQLAlchemy2.1.5: SQLite39.24s; PG3개7.67s+추가 정책1개1.28s.
원 pool size1/overflow0을 전부 점유해도 요청 clone의 물리 backend는 다르고 native checkedout=1 유지.
clone에 checkout listener가 복사되므로 listener 전역 호출 수 대신 실제 native pool.checkedout()으로 분리 측정했다.
기존 session-loss 반례는 STARTED/행1/첫 요청 오류/재연결0을 유지했다.
busy, 서로 다른 run, crash 뒤 재획득, 원 body 예외 identity, 종료 후 소유 session/advisory0도 통과했다.
기존 권한/config/tag/schema/lazy import/console alias 회귀는 immutable focused suite에 포함된다.
console 자식은 기존 설치 a68의 불변 main을 사용하므로 새 wheel 설치 검증이라고 확대하지 않는다.

## 변경과 문서 경계
a68→892는 제품 모듈32행, tests70행과 앞선 a68 문서 정산4파일뿐이며 pyproject/lock/workflow는 그대로다.
standard native NullPool/QueuePool만 허용하고 subclass/custom pool은 recreate 전 거절한다.
공식 Engine 생성/Pool.recreate 확장이며 native SQL 본문을 복사하지 않는다.
892 guide의 현행 PostgreSQL 설명은 아직 '별도 NullPool/connect_timeout5'라서 작성자에게 정정 요청했다.
지원 범위는 검증된 native PostgresRunStorage와 표준 pool이며 임의 custom Engine/event hooks까지 보장한다고 해석하지 않는다.
native eventlog의 먼저 남는 실패 시도는 authoritative run 상태와 비원자적이라는 기존 한계는 유지한다.

## 한계와 소유
직접 테스트는 소유 임시 SQLite와 root가 허용한 신규 전용 PG DB뿐이다.
job/provider/daemon/worker/SSH/production 실행 또는 source 수정은 없었다.
두 SDK source는 불변 Git archive에서 로드했고 shared venv/타인 WT는 변경하지 않았다.
소유 PG DB는 후속 검증을 위해 남겨두며 마지막 정책 fixture에서 소유 연결0을 확인했다.
이 판정은 새 wheel/소비자 최종 pin/전체 CI/운영 수용을 대신하지 않는다.
세부 숫자·fixture/log SHA는 같은 이름 safe.json을 따른다.
