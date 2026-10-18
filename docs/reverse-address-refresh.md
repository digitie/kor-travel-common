# 좌표 기반 주소 갱신 구현 가이드

## 목적과 경계

Weather·Transport는 기존 VWorld API를 우선하고 Kakao Local API를 보조로 사용한다.
Geo API나 Geo 데이터 토큰은 이 갱신의 선행 조건이 아니다. 좌표 재탐색과 달리,
같은 좌표에서 행정구역·도로명·지번 주소가 바뀌었는지 확인한다.

소비자가 소유하는 원천 주소, 관리자 입력, 좌표, KMA 격자, 과거 fact는 수정하지 않는다.
최신 확인 주소와 행정구역은 같은 소비자 DB의 파생 테이블에 저장한다.
실패 시 마지막 정상 결과와 그 확인일을 보존하고 재확인 필요 상태로 표시한다.
좌표가 바뀌면 이전 좌표의 파생 주소를 현재 주소로 노출하지 않는다.

## 공통 Python 연결

1. Common의 [reverse-address] extra를 고정 commit으로 설치한다. Dagster는
   [dagster,reverse-address]를 사용한다. VWorld는 기존 python-vworld-api public API를 사용한다.
2. 소비자 Base.metadata에 reverse_address_tables를 등록하고 소비자 Alembic에서
   reverse_address_entries·reverse_address_control을 생성한다.
   과거 migration에는 실행 시점의 Common helper를 호출하지 않고 컬럼을 고정한다.
3. DatabaseAddressSource에 target_key·longitude·latitude·display_name을 label한 SELECT를 전달한다.
   안정적인 target_key를 사용한다. 키셋 조회는 target_key 문자열 순서다.
4. VworldKakaoAddressResolver에 서버 키를 주입하고 refresh_reverse_addresses를 호출한다.
   위치 읽기 인자로 source.page와 source.retries를 전달한다. 재시도는 활성 원천 join을
   먼저 적용한 뒤 최대 10개를 읽어 비활성/삭제 위치의 오류가 슬롯을 독점하지 않는다.
   page callback은 cursor·limit·now·cycle·force의 5개 인자를 받는다. 제공된
   DatabaseAddressSource.page는 실제 due·수동 미확인 위치를 SQL에서 먼저 고른다.
   pending_failures=source.pending_failures를 필수 전달해 현재 활성 원천의 실패만
   수동 cycle의 잔여로 판단한다. 신규 API를 도입한 소비자도 이 인자를 함께 연결한다.
   원천 SELECT는 읽기만 한다. HTTP 호출 중 DB transaction을 유지하지 않는다.
5. address_refresh_definitions로 제한된 address_refresh_job과 10분 간격 sensor를 등록한다.
   sensor는 DB에서 미확인·기한 경과·재시도·중단 배치가 있는지만 읽는다.
   대상이 없으면 새 run이나 provider 호출을 만들지 않는다.

위치별 성공/정상 무결과 확인일에서 달력 6개월 후가 다음 자동 확인일이다.
8월 31일은 다음 해 2월 말일로 맞추며 180일로 환산하지 않는다.
같은 좌표는 정상 주소·정상 무결과를 재사용하지만 실제 제공자 확인일과 다음 갱신일을 연장하지 않는다.
주소 변경 집계는 정규화한 address·region만 비교하며 provider 교체 자체는 변경으로 세지 않는다.

한 run은 기본 50개·30초이며 provider는 순차 호출한다. 한 주소의 외부 timeout 때문에
실제 종료는 진행 중인 한 주소의 timeout만큼 예산을 넘길 수 있다. SDK 내부 재시도는 끈다.
VWorld 실패/무결과이면 Kakao 주소 및 행정구역 API로 fallback한다. worker 요청 간격은
최소 0.5초다. provider 키·요청 URL·원문 예외는 상태/API/Dagster 로그에 남기지 않는다.

## 중단·실패 복구

DB에 커서·수동 cycle·90초 lease를 저장한다. 만료된 owner는 늦게 받은 응답을 쓰거나
새 worker의 lease를 해제할 수 없다. 결과 저장 후 cursor 저장 전에 죽어도 다시 읽어
중복 호출을 피한다. 실패 위치는 지수 backoff(최대 24시간) 후 재시도하며,
자동 sensor가 켜져 있으면 다음 실행에서 이어 처리한다.
자동 달력 갱신을 꺼도 이미 시작한 수동 cycle의 실패는 backoff 후 이어 처리한다.
대기 시간에는 sensor가 새 run을 만들지 않으며 원천이 비활성/삭제되면 한 번 정리 후 끝낸다.
커서는 끝에서 앞쪽으로 순환한다. 대기 중 실패가 있어도 cursor 앞에 새로 생긴 위치,
변경된 좌표와 6개월 due를 처리한다. 같은 수동 cycle의 캐시도 6개월 유효기간을 연장하지 않는다.
커서 진행과 재시도를 번갈아 처리해 반복 실패 1건이 새 위치를 영구히 막지 않는다.
배치 크기 1에서도 신규 위치의 처리 슬롯을 먼저 보장한다.

수동 force는 기한 전에도 전체 위치를 재확인한다. 부분 배치는 같은 cycle을 이어서
완료한 위치를 다시 호출하지 않는다. 수동 요청은 큐 등록 성공일 뿐 주소 갱신 완료가 아니다.
Daemon이 꺼져 있으면 대기하며, UI가 임의로 Daemon을 기동하지 않는다.

## Admin 보안·표시 계약

Admin Dagster 화면에서 전체 주소 수동 갱신·상태 새로고침과 최근 50개 결과를 제공한다.
BFF는 세션과 같은 Origin을 확인하며 서버에서 고정한 자기 프로젝트의
address_refresh_job만 실행한다. 브라우저의 GraphQL·repository·job·run config는 받지 않는다.
UUID requestId를 자기 location의 실행 tag로 조회해 통신 재시도의 중복 예약을 줄인다.
동시 요청의 경합은 DB lease로 격리하며, 수동 run이 lease를 얻지 못하면 실패로 표시한다.
다른 프로젝트 실행은 조회하거나 변경하지 않는다.

서버 키와 DB는 소비자 소유다. 실제 저장·서비스 방식은 각 제공자의 현행 이용 조건과
허용 범위를 확인한 배포 설정에서만 활성화한다. 이 문서는 제공자 이용 허가를 대신하지 않는다.

## 검증·적용 상태

설계와 구현용 PR이다. 로컬 fixture 검증, 두 독립 리뷰, CI, 실제 브라우저 검증 결과는
각 PR의 검증 기록에 적는다. 운영 migration·외부 API 실호출·Daemon 재기동·배포는
이 코드 작업의 성공으로 간주하지 않는다.
