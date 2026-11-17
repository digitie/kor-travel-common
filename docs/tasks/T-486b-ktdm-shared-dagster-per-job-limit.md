# T-486b ktdm: 공용 Dagster instance의 job별 한도와 run_retries 결정

- 상태: READY
- 우선순위: P2
- Gate: 결정 기록·backend 시험·공용 instance 수용
- 선행: 없음
- 소유 저장소: kor-travel-docker-manager
- 병렬: 묶음 D(언제든)

출처는 [공통화 재조사·계획(2026-11-17)](../plan/commonization-plan-2026-11-17.md)의 §3.4·§4.9(K-46)이다. 근거 위치(file:line)와 차이 분석은 그 문서가 정본이며 여기서 반복하지 않는다.

## 목표

공용 `dagster.yaml`에는 `kortravelcommon/job`의 값별 한도가 없고 concierge 값 다섯 개만 리터럴로 있다. `run_retries` 블록도 없다. 공통 가이드는 daemon 소유 저장소에 그 규칙을 두라고 한다. 일반 규칙 하나로 바꿀지, 지금대로 둘지 결정하고 결정을 구현한다.

## 고정 결정

- 공통 쪽 기대는 [dagster-adoption](../runbooks/dagster-adoption.md) §3이다.
- Manager는 범용으로 유지한다. 서비스 값 리터럴을 일반 규칙으로 바꾸는 방향이 그에 맞다.
- 운영 동작이 바뀐다(모든 tenant의 같은 job이 동시 1개로 묶인다). 영향 확인이 먼저다.

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
