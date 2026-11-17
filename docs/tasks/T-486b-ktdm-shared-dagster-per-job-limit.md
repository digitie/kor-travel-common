# T-486b ktdm: 공용 Dagster instance의 job별 한도와 run_retries 결정 자료와 구현

- 상태: BLOCKED
- 우선순위: P2
- Gate: 소유자 결정 기록·backend 시험·공용 instance 수용
- 선행: 없음
- 외부 선행: 소유자 재결정. 2026-11-17 영향 자료가 차단 조건(map의 동시 run 감소)에 걸려 권고안을 구현하지 않았다. 아래 "영향 자료와 결정"의 (가)~(다) 중 선택
- 소유 저장소: kor-travel-docker-manager
- 병렬: 묶음 D(언제든)

출처는 [공통화 재조사·계획(2026-11-17)](../plan/commonization-plan-2026-11-17.md)의 §3.4·§4.9(K-46)이다. 근거 위치(file:line)와 차이 분석은 그 문서가 정본이며 여기서 반복하지 않는다.

## 영향 자료와 결정(2026-11-17)

소유자 결정(2026-11-17): "공용 Dagster의 job별 실행 한도와 재시도 설정 (T-486b): 영향 자료를 먼저 만들고, 구현은 결정 뒤에 합니다 — 추천안대로". 권고안은 공용 `dagster.yaml`의 concierge 리터럴 다섯을 `kortravelcommon/job` 값별 한도 1(`applyLimitPerUniqueValue`) 일반 규칙 하나로 바꾸고 `run_retries` 블록을 더하는 것이다. 자료가 권고를 뒷받침하면 구현하기로 했다.

방법: 운영 공용 Dagster webserver(n150)에 읽기 전용 GraphQL `runsOrError(filter:{createdAfter: 30일 전}, limit 250 페이지)` — 최근 30일 41,116 run(2026-10-18~11-17). 위치(`dagster/code_location`)×`kortravelcommon/job` 값과 job 이름별로 같은 값의 최대 동시 실행(start→end)과 최대 동시 존재(생성→end, QUEUED 포함)를 셌다. 렌더링된 instance 설정을 읽기 전용으로 확인했다. 코드 기준: Manager `7e9d60f`, Map `377bc8e3`, weather·transport·pinvi main. 더 자세한 쌍별 질의는 호스트 I/O guard가 보류해 하지 않았다.

렌더링된 공용 instance 설정(Manager release `2c3f95b6`, 호스트 override 없음): 전역 동시 6, 위치별 map 10·pinvi 10·geo 10·weather 10·transport 3·concierge 2, concierge 리터럴 다섯(각 1), `kor_travel_map.feature_update_request_id`(key만) 4. `run_retries` 블록은 없고 `run_monitoring.max_resume_run_attempts`는 0.

| tenant | 30일 run | job tag 있는 run | 값 수 | 같은 값 최대 동시 실행 / 동시 존재 | 같은 값이 겹칠 수 있는 경로 | 값별 한도 1이 동시성을 줄이는가 |
|---|---|---|---|---|---|---|
| map | 8,864 | 1,458 | 33 | `feature_update_request_worker` 2 / 11. `mois_licenses`·`visitkorea_festivals` 2 / 2. 나머지 1 / 2 이하 | `feature_update_request_queue_sensor`가 15초 tick마다 run_key가 다른 worker run을 최대 10개 낸다. 모두 같은 값 `map/feature_update_request_worker`이고, instance가 의도적으로 동시 4를 허용한다. 관리자 수동 실행과 schedule, geo 릴리스 sensor가 적재 job을 겹치게 할 수 있다 | **예.** worker가 설계값 4에서 1로 줄고 적재 job이 직렬화된다 |
| pinvi | 18,442 | 18,442 | 8 | 1 / 2 | schedule만. standalone 사본에 이미 같은 규칙 | 아니오 |
| concierge | 13,810 | 13,810 | 5 | 1 / 1 | 이미 리터럴 다섯으로 제한 | 아니오(일반 규칙과 같다) |
| weather·transport | 0(odroid로 이전) | — | — | 측정 안 함 | standalone 사본에 이미 같은 규칙 | 아니오 |
| geo | 0 | — | — | — | — | — |

재시도: `dagster/retry_number` tag가 있는 run은 없었다. `dagster/max_retries`는 map 0(1,458건, 나머지는 tag 없음), concierge 0, pinvi 0(13,754건)·1(4,688건, 멱등 job 다섯). pinvi·weather·transport standalone 사본은 `run_retries: {enabled: true, max_retries: 0, retry_on_asset_or_op_failure: false}`다. 이 블록을 공용 instance에 넣으면 `max_retries≥1` tag가 있는 pinvi job 다섯만 재시도하게 된다. 안전하지만 pinvi의 운영 동작이 바뀌므로 따로 결정한다.

**결정: 일반 규칙은 채택하지 않는다(구현하지 않음).** 이 파일의 차단 조건("map의 동시 run이 한도에 걸려 줄어드는 것이 확인되면 일반 규칙을 채택하지 않는다")에 걸렸다. Manager PR은 열지 않았다. 소유자가 다시 고를 안:

- (가) concierge 리터럴을 그대로 두고 `run_retries` 블록만 더한다(위 값, pinvi 다섯 job의 재시도가 켜진다).
- (나) map을 값별 규칙에서 빼고 일반 규칙을 쓴다. Dagster의 tag 한도는 code location 범위를 받지 않으므로 그대로는 표현할 수 없다.
- (다) map이 worker run에 요청마다 다른 job tag 값을 달게 한 뒤 일반 규칙을 쓴다(map 코드 변경).
- (라) 지금대로 둔다. 사유와 공통 가이드([dagster-adoption](../runbooks/dagster-adoption.md) §3)와의 차이를 Manager 문서에 적는다(구현 범위 4).

## 목표

공용 `dagster.yaml`에는 `kortravelcommon/job`의 값별 한도가 없고 concierge 값 다섯 개만 리터럴로 있다. `run_retries` 블록도 없다. 공통 가이드는 daemon 소유 저장소에 그 규칙을 두라고 한다. 일반 규칙 하나로 바꿀지, 지금대로 둘지 결정하고 결정을 구현한다.

## 고정 결정

- 공통 쪽 기대는 [dagster-adoption](../runbooks/dagster-adoption.md) §3이다.
- Manager는 범용으로 유지한다. 서비스 값 리터럴을 일반 규칙으로 바꾸는 방향이 그에 맞다.
- 운영 동작이 바뀐다(모든 tenant의 같은 job이 동시 1개로 묶인다). 결정자는 소유자다. 이 task는 영향 확인 자료를 만들고, 결정이 난 뒤 구현한다.
- 영향 확인 자료를 낸 뒤 소유자 결정을 기다린다. 결정 전에는 구현하지 않고, 그 동안 이 task를 BLOCKED(외부 선행: 소유자 결정)로 바꿔 둔다.

## 구현 범위

1. 확인: 각 tenant가 한 job tag 값으로 동시에 여러 run을 내는 경로가 있는가. 특히 map의 queue sensor가 한 tick에 내는 run들의 `kortravelcommon/job` 값.
2. 결정 기록(`docs/decisions.md`): 일반 규칙 채택 여부, `run_retries` 채택 여부와 값.
3. 채택하면: `config/dagster-shared/dagster.yaml`에 값별 한도 규칙을 넣고 concierge 리터럴 다섯을 지운다. host override 렌더러(`shared_dagster_instance.py`)가 dict 값을 받아들이게 하고 시험을 추가한다.
4. 채택하지 않으면: 사유와 공통 가이드와의 차이를 문서에 적는다.

## 범위 밖

tenant별 `run_group` 한도, code_location 한도, 소비자 저장소의 standalone 사본.

## 대상 저장소·브랜치·PR·되돌리기

- 저장소 `digitie/kor-travel-docker-manager`. 이 저장소(common)의 작업이 아니다. 그 저장소의 규칙·리뷰·CI를 따른다.
- 브랜치: `docs/…` 또는 `agent/<agent>-<task>` 형식의 작업 브랜치, `origin/main`에서 분기. PR 1개.
- 되돌리기: `git revert <merge-sha>` 1회 뒤 trusted release 재설치와 instance 설정 재적용.
- 그 저장소의 backlog에는 이 task를 가리키는 포인터 한 줄만 두고 수용 기준을 복제하지 않는다.

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다.

```text
config/dagster-shared/dagster.yaml, config/docker-targets.yml
backend/src/kor_travel_docker_manager/services/shared_dagster_instance.py
backend/tests/test_dagster_shared_config.py
docs/decisions.md, docs/journal.md, docs/tasks.md
```

## 수용 기준

- [ ] 결정 기록에 tenant별 영향 확인 결과(동시 다중 run 경로 유무)가 있다.
- [ ] 채택 시: 렌더링된 instance 설정에 값별 한도 규칙이 있고 concierge 리터럴이 없다. override가 있는 호스트 렌더링 시험이 통과한다.
- [ ] 채택 시: 실제 queue daemon으로 같은 job의 두 번째 run이 대기하는 통합 시험이 통과한다.
- [ ] backend 시험 전체와 ruff가 통과한다.

## 검증 명령

```bash
python -m pytest backend -q && ruff check backend
```

## evidence

결정 기록, 시험 출력, 적용 뒤 공용 instance 관찰(없으면 `NOT_RUN(운영 호스트)`).

## rollback·release 차단 조건

- `git revert` 1회 뒤 설정을 다시 적용한다.
- map의 동시 run이 한도에 걸려 줄어드는 것이 확인되면 일반 규칙을 채택하지 않는다.
