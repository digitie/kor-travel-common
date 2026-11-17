# T-484a pinvi-etl: job별 재시도 sensor 5개를 다중 job sensor 1개로

- 상태: READY
- 우선순위: P2
- Gate: 소비자 CI(etl)·배포 뒤 sensor 확인
- 선행: 없음
- 소유 저장소: pinvi
- 병렬: 묶음 A

출처는 [공통화 재조사·계획(2026-11-17)](../plan/commonization-plan-2026-11-17.md)의 §3.4·§4.6(K-41)이다. 근거 위치(file:line)와 차이 분석은 그 문서가 정본이며 여기서 반복하지 않는다.

## 목표

pinvi ETL은 `infrastructure_retry_sensor`를 job마다 하나씩 5개 만든다. 공통의 `infrastructure_retry_sensor_for_jobs`로 바꾸면 실패 조회가 한 번이 되고 sensor tick이 준다.

## 고정 결정

- 공통 구현과 사용 규칙은 [dagster-multi-job-retry](../runbooks/dagster-multi-job-retry.md)와 [dagster-adoption](../runbooks/dagster-adoption.md) §16이 정본이다.
- 재시도 대상 job 집합과 각 job의 `RecoveryPolicy`는 바꾸지 않는다.
- asset job을 다시 주입하는 지금 방식(`with_updated_job`)이 필요한 이유를 유지한다.

## 구현 범위

1. `apps/etl/pinvi/etl/definitions.py:88-97`의 sensor 목록을 `_for_jobs` 하나로 바꾼다.
2. 새 sensor의 기본 상태를 옛 sensor들과 같게 둔다. 이름이 바뀌므로 옛 sensor 상태는 넘어오지 않는다.
3. ETL 단위 시험에서 sensor 수와 대상 job 집합을 단언한다.
4. 필요하면 `kor-travel-common` 핀을 올린다(현재 `c289b46`에 `_for_jobs`가 있다).

## 범위 밖

재시도 정책 값, 다른 sensor, 운영 instance 설정.

## 대상 저장소·브랜치·PR·되돌리기

- 저장소 `digitie/pinvi`. 이 저장소(common)의 작업이 아니다. 그 저장소의 규칙·리뷰·CI를 따른다.
- 브랜치: `docs/…` 또는 `agent/<agent>-<task>` 형식의 작업 브랜치, `origin/main`에서 분기. PR 1개.
- 되돌리기: `git revert <merge-sha>` 1회.
- 그 저장소의 backlog에는 이 task를 가리키는 포인터 한 줄만 두고 수용 기준을 복제하지 않는다.

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다.

```text
apps/etl/pinvi/etl/definitions.py
apps/etl/tests/**
docs/journal.md, docs/resume.md, docs/tasks.md
```

## 수용 기준

- [ ] Definitions의 인프라 재시도 sensor가 1개이고 대상 job 집합이 바꾸기 전 5개와 같다(시험).
- [ ] `etl` workflow가 통과한다.
- [ ] 배포 뒤 옛 sensor 5개가 목록에 없고 새 sensor가 의도한 상태(RUNNING/STOPPED)다. 확인하지 못하면 `NOT_RUN(배포)`로 남긴다.

## 검증 명령

```bash
# pinvi/apps/etl
uv sync --locked && uv run pytest -q
```

## evidence

PR의 시험 출력. 배포 뒤 sensor 목록은 pinvi journal에 남긴다.

## rollback·release 차단 조건

- `git revert` 1회. 되돌리면 옛 sensor 5개가 기본 상태로 다시 생긴다.
