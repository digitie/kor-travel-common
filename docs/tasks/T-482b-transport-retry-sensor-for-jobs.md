# T-482b transport-dagster: job별 재시도 sensor 3개를 다중 job sensor 1개로

- 상태: READY
- 우선순위: P3
- Gate: 소비자 CI(backend)·배포 뒤 sensor 확인
- 선행: 없음
- 소유 저장소: kor-travel-transport
- 병렬: 묶음 A

출처는 [공통화 재조사·계획(2026-11-17)](../plan/commonization-plan-2026-11-17.md)의 §3.4·§4.6(K-41)이다. 근거 위치(file:line)와 차이 분석은 그 문서가 정본이며 여기서 반복하지 않는다.

## 목표

`backend/app/dagster/definitions.py:1041-1048`의 job별 `infrastructure_retry_sensor` 3개를 `infrastructure_retry_sensor_for_jobs` 하나로 바꾼다.

## 고정 결정

- T-484a와 같다. 대상 job 집합(공항·고속도로·휴게소 기준정보 수집)과 `RecoveryPolicy` 값을 바꾸지 않는다.
- 합친 sensor는 한 tick에 RunRequest를 하나만 낸다. 세 job이 같은 때 인프라 실패하면 재시도가 tick마다 하나씩 나간다.
- 이 저장소는 다른 팀이 유지한다.

## 구현 범위

1. sensor 목록을 `_for_jobs` 하나로 바꾼다. 새 sensor의 기본 상태를 옛 것과 같게 둔다.
2. sensor 수와 대상 job 집합을 단언하는 시험.

## 범위 밖

재시도 정책 값, 회수 sensor.

## 대상 저장소·브랜치·PR·되돌리기

- 저장소 `digitie/kor-travel-transport`. 이 저장소(common)의 작업이 아니다. 그 저장소의 규칙·리뷰·CI를 따른다.
- 브랜치: `docs/…` 또는 `agent/<agent>-<task>` 형식의 작업 브랜치, `origin/main`에서 분기. PR 1개.
- 되돌리기: `git revert <merge-sha>` 1회.
- 그 저장소의 backlog에는 이 task를 가리키는 포인터 한 줄만 두고 수용 기준을 복제하지 않는다.

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다.

```text
backend/app/dagster/definitions.py
backend/tests/**
```

## 수용 기준

- [ ] 인프라 재시도 sensor가 1개이고 그 sensor의 대상 job이 바꾸기 전 3개와 같다(시험).
- [ ] `backend` job이 통과한다.
- [ ] 배포 뒤 옛 sensor가 목록에 없다. 확인하지 못하면 `NOT_RUN(배포)`.

## 검증 명령

```bash
cd backend && uv sync --locked --extra dev && uv run pytest -q
```

## evidence

PR의 CI 결과와 배포 뒤 기록.

## rollback·release 차단 조건

- `git revert` 1회.
