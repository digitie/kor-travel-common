# T-484a pinvi: job별 재시도 sensor 5개를 다중 job sensor 1개로(API 정적 목록 포함)

- 상태: READY
- 우선순위: P3
- Gate: 소비자 CI(api·etl·web)·배포 뒤 sensor 확인
- 선행: 없음
- 소유 저장소: pinvi
- 병렬: 묶음 A

출처는 [공통화 재조사·계획(2026-11-17)](../plan/commonization-plan-2026-11-17.md)의 §3.4·§4.6(K-41)이다. 근거 위치(file:line)와 차이 분석은 그 문서가 정본이며 여기서 반복하지 않는다.

## 목표

pinvi ETL은 `infrastructure_retry_sensor`를 job마다 하나씩 5개 만든다. 공통의 `infrastructure_retry_sensor_for_jobs`로 합치면 실패 조회가 한 번이 된다. 다만 pinvi API가 sensor 이름 다섯 개를 정적 목록으로 갖고 있어 ETL만 바꿀 수 없다. 배포물 둘(api, etl)과 관리자 화면이 함께 바뀐다.

## 고정 결정

- 공통 구현과 사용 규칙은 [dagster-multi-job-retry](../runbooks/dagster-multi-job-retry.md)와 [dagster-adoption](../runbooks/dagster-adoption.md) §16이 정본이다.
- 재시도 대상 job 집합과 각 job의 `RecoveryPolicy`는 바꾸지 않는다.
- 다중 job sensor는 `jobs=[…]`를 대상으로 하고 job 이름으로 run을 요청한다. asset job을 다시 주입할 때는 `with_updated_jobs([다시 주입할 asset job 전부])`를 쓴다. `with_updated_job(j)`는 대상을 그 job 하나로 바꿔 버리므로 쓰지 않는다.
- 합친 sensor는 한 tick(60초)에 RunRequest를 하나만 낸다. 여러 job이 같은 때 인프라 실패하면 재시도가 tick마다 하나씩 나간다. 지금(job별 sensor)은 같은 tick에 각각 나간다.
- weather는 이 구현을 env로 꺼 둔 상태라(기본 false) pinvi의 채택이 첫 운영 사용이 될 수 있다. 배포 뒤 관찰을 수용 기준에 둔다.

## 구현 범위

1. `apps/etl/pinvi/etl/definitions.py:88-97`의 sensor 목록을 `_for_jobs` 하나로 바꾸고 `with_updated_jobs([...])`로 다섯 asset job을 다시 주입한다.
2. `apps/api/app/services/admin_etl.py`의 `PINVI_ETL_SENSORS`(지금 sensor 다섯, 각 `job_name` 하나)와 그 모델을 바꾼다. `job_name`을 `job_names` 목록으로 할지 비울지 정하고 API 문서·스키마에 반영한다.
3. 관리자 화면이 그 목록을 그리는 곳을 새 모양에 맞춘다.
4. 배포 순서를 정한다(API 먼저, ETL 다음). 사이 구간에 목록과 Definitions가 어긋나도 관리자 화면이 깨지지 않게 한다.
5. 새 sensor의 기본 상태를 확인한다. 공통 구현은 RUNNING이 기본이다. 이름이 바뀌므로 옛 sensor 상태는 넘어오지 않는다.
6. ETL 단위 시험에서 sensor 수, sensor의 대상 job 다섯 개, job별 정책을 단언한다.

## 범위 밖

재시도 정책 값, 인프라 재시도가 아닌 다른 sensor, 운영 instance 설정.

## 대상 저장소·브랜치·PR·되돌리기

- 저장소 `digitie/pinvi`. 이 저장소(common)의 작업이 아니다. 그 저장소의 규칙·리뷰·CI를 따른다.
- 브랜치: `docs/…` 또는 `agent/<agent>-<task>` 형식의 작업 브랜치, `origin/main`에서 분기. PR 1개.
- 되돌리기: `git revert <merge-sha>` 1회.
- 그 저장소의 backlog에는 이 task를 가리키는 포인터 한 줄만 두고 수용 기준을 복제하지 않는다.

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다.

```text
apps/etl/pinvi/etl/definitions.py, apps/etl/tests/**
apps/api/app/services/admin_etl.py, apps/api/app/schemas/**(해당 모델), apps/api/tests/**
apps/web/**(관리자 ETL 화면), docs/api/**
docs/journal.md, docs/resume.md, docs/tasks.md
```

## 수용 기준

- [ ] Definitions의 인프라 재시도 sensor가 1개이고 **그 sensor의 대상 job**이 바꾸기 전 5개와 같다(시험. sensor 수만 세지 않는다).
- [ ] `apps/etl/tests/test_admin_etl_definition_lists.py`가 통과한다(API 정적 목록과 Definitions의 일치).
- [ ] 두 job이 같은 scan에서 실패했을 때 첫 tick에 하나, 다음 tick에 나머지가 요청되는 시험이 있다.
- [ ] `api`·`etl`·`web` workflow와 Aggregate CI가 통과한다.
- [ ] 배포 뒤 옛 sensor 5개가 목록에 없고 새 sensor가 의도한 상태다. 확인하지 못하면 `NOT_RUN(배포)`로 남긴다.

## 검증 명령

```bash
# pinvi
(cd apps/etl && uv sync --locked && uv run pytest -q)
(cd apps/api && uv sync --locked && uv run pytest -q tests/unit)
npm run typecheck --workspace apps/web
```

## evidence

PR의 시험 출력. 배포 뒤 sensor 목록은 pinvi journal에 남긴다.

## rollback·release 차단 조건

- `git revert` 1회. 되돌리면 옛 sensor 5개가 기본 상태로 다시 생긴다.
