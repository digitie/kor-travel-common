# T-481a weather-dagster: 로컬 수집 결과 tag 함수를 공통 구현으로 교체

- 상태: BLOCKED
- 우선순위: P2
- Gate: 소비자 CI(python)
- 선행: T-313
- 소유 저장소: kor-travel-weather
- 병렬: 묶음 B(T-482a와 독립)

출처는 [공통화 재조사·계획(2026-11-17)](../plan/commonization-plan-2026-11-17.md)의 §3.4·§4.5(K-40)이다. 근거 위치(file:line)와 차이 분석은 그 문서가 정본이며 여기서 반복하지 않는다.

## 목표

`kortravelweather_dagster/definitions.py:399-418`의 `_record_collection_outcome`을 지우고 `kortravelcommon.dagster.record_collection_outcome`을 쓴다.

## 고정 결정

- tag 문자열과 순위 규칙은 공통 구현(T-313)이 정본이다. 관리자 프론트는 바뀌지 않는다.
- 이 저장소는 다른 팀이 유지한다.

## 구현 범위

1. `kor-travel-common` 핀을 T-313이 들어간 커밋으로 올린다(루트와 dagster 패키지 `pyproject.toml`, `uv.lock`).
2. 로컬 함수와 그 시험을 지우고 호출부를 공통 import로 바꾼다.

## 범위 밖

수집 로직, 새 outcome 값, 관리자 UI.

## 대상 저장소·브랜치·PR·되돌리기

- 저장소 `digitie/kor-travel-weather`. 이 저장소(common)의 작업이 아니다. 그 저장소의 규칙·리뷰·CI를 따른다.
- 브랜치: `docs/…` 또는 `agent/<agent>-<task>` 형식의 작업 브랜치, `origin/main`에서 분기. PR 1개.
- 되돌리기: `git revert <merge-sha>` 1회.
- 그 저장소의 backlog에는 이 task를 가리키는 포인터 한 줄만 두고 수용 기준을 복제하지 않는다.

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다.

```text
pyproject.toml, packages/kor-travel-weather-dagster/pyproject.toml, uv.lock
packages/kor-travel-weather-dagster/src/kortravelweather_dagster/definitions.py
packages/kor-travel-weather-dagster/tests/**
```

## 수용 기준

- [ ] 저장소에 `_record_collection_outcome` 정의가 0개다(grep).
- [ ] `python` job이 통과하고 Dagster 패키지 시험 수가 로컬 함수 시험을 뺀 만큼만 준다.
- [ ] 핀 커밋이 세 `pyproject.toml` 자리와 `uv.lock`에서 같다.

## 검증 명령

```bash
uv sync --locked && uv run pytest -q packages/kor-travel-weather-dagster
```

## evidence

PR의 CI 결과.

## rollback·release 차단 조건

- `git revert` 1회(핀 포함).
