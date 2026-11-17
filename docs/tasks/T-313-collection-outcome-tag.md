# T-313 수집 결과 run tag 기록 함수를 공통 Dagster 모듈에 추가

- 상태: READY
- 우선순위: P1
- Gate: Python 단위·wheel 설치·2인 리뷰
- 선행: 없음
- 소유 저장소: kor-travel-common
- 병렬: 묶음 A

출처는 [공통화 재조사·계획(2026-11-17)](../plan/commonization-plan-2026-11-17.md)의 §3.4·§4.5(K-40)이다. 근거 위치(file:line)와 차이 분석은 그 문서가 정본이며 여기서 반복하지 않는다.

## 목표

`_record_collection_outcome`이 weather와 transport에 같은 본문으로 있고, tag `kortravel/collection-outcome`을 두 관리자 프론트가 읽는다. 정의를 `kortravelcommon.dagster` 한 곳에 둔다.

## 고정 결정

- `[dagster]` extra 안에 둔다. core-only 설치는 Dagster를 import하지 않는다([ADR-011](../adr/011-python-common-package.md)).
- 동작은 두 사본과 같다(동작 보존). tag 문자열을 바꾸지 않는다.
- T-026의 버전 규칙을 이 PR에서 처음 적용한다(dev 번호 올림).

## 구현 범위

1. `COLLECTION_OUTCOME_TAG = "kortravel/collection-outcome"`와 `record_collection_outcome(context, outcome)`을 `dagster.py`에 추가한다.
2. 규칙: `partial`·`deferred`만 기록한다. 순위는 success < deferred < partial이고 낮추지 않는다. instance·run 조회·tag 쓰기에서 난 예외는 삼키고 경고를 한 줄 남긴다. 그 경고도 실패하면 조용히 넘어간다.
3. 단위 시험: 순위 상향, 같은 값·낮은 값 무시, 알 수 없는 값 무시, instance 없음, run 없음, `add_run_tags` 예외, `context.log` 예외.
4. [dagster-adoption](../runbooks/dagster-adoption.md)에 사용 절 추가, README·CHANGELOG 갱신.

## 범위 밖

소비자 채택(T-481a·T-482a), 관리자 UI의 tag 표시, 새 outcome 값.

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다.

```text
packages/py/kor-travel-common/src/kortravelcommon/dagster.py
packages/py/kor-travel-common/tests/test_collection_outcome.py
packages/py/kor-travel-common/pyproject.toml          # 버전
packages/py/kor-travel-common/README.md, docs/runbooks/dagster-adoption.md, CHANGELOG.md
```

## 수용 기준

- [ ] 새 시험 7개 이상이 통과하고 skip 0이다. 기존 시험 수가 줄지 않는다.
- [ ] `record_collection_outcome`이 어떤 입력에서도 예외를 밖으로 내지 않는다(시험으로 단언).
- [ ] weather `definitions.py:399-418`(커밋 `e68f16a`)의 본문과 판정이 같다는 대조 시험(같은 입력 표에 같은 tag 결과)이 있다.
- [ ] core-only 설치에서 `import kortravelcommon`이 Dagster를 import하지 않는다.
- [ ] `pyproject.toml` 버전이 올랐다.

## 검증 명령

```bash
cd packages/py/kor-travel-common
uv sync --locked --extra dev --extra dagster && uv run pytest -q
uv run ruff check . && uv build
```

## evidence

시험 수 전후와 wheel SHA-256. 소비자 채택은 `NOT_RUN(T-481a·T-482a)`.

## rollback·release 차단 조건

- 추가만 하는 변경. `git revert` 1회. 소비자가 핀을 올리기 전에는 영향이 없다.
