# T-314 회수 sensor가 소비자 cursor와 정체 시계를 callback에 전달

- 상태: READY
- 우선순위: P2
- Gate: Python 단위·wheel 설치·2인 리뷰
- 선행: 없음
- 소유 저장소: kor-travel-common
- 병렬: 묶음 D(언제든)

출처는 [공통화 재조사·계획(2026-11-17)](../plan/commonization-plan-2026-11-17.md)의 §3.4·§4.9(K-42)이다. 근거 위치(file:line)와 차이 분석은 그 문서가 정본이며 여기서 반복하지 않는다.

## 목표

공통 `reconciliation_sensor`가 sensor cursor를 소유해서 weather와 transport는 keyset 위치를 프로세스 메모리에 두고, weather는 공통의 비공개 cursor 접두 `stall:`을 직접 다시 읽는다. callback이 현재 정체 시계와 자기 하위 cursor를 공식 인자로 받게 한다.

## 고정 결정

- 기존 호출 모양은 그대로 동작한다(추가만).
- 회수 SQL·lease·fencing은 계속 소비자 소유다([dagster-adoption](../runbooks/dagster-adoption.md) §4·§19).
- Map의 회수 sensor는 대상이 아니다(주기·반환형·시계가 달라 factory에 맞지 않는다).
- weather는 공통 cursor의 `stall:` 접두와 그 뒤의 JSON을 직접 읽는다(`kortravelweather_dagster/sync_recovery.py:64-65,119-127`, 커밋 `e68f16a`). 그 문자열 모양을 이 task가 바꾸지 않는다. 소비자 구획은 그 파서가 그대로 읽히는 자리에 둔다.

## 구현 범위

1. callback이 선택적으로 `ReconcileTick(clock, consumer_cursor)`를 받고 새 `consumer_cursor`(짧은 문자열, 길이 상한)를 돌려줄 수 있게 한다.
2. 공통 cursor 형식에 소비자 구획을 추가하되 옛 cursor(구획 없음)를 읽을 수 있다.
3. 정체 경보 한 줄을 만드는 `format_stall_alert(event, clock, now)`를 `stall.py`에 둔다.
4. 단위 시험: 옛 callback 호환, 옛 cursor 호환, 소비자 cursor 왕복, 길이 상한 초과 거절, 정체 시계 전달.
5. 가이드 §19 갱신.

## 범위 밖

weather·transport의 채택(그 저장소가 이 API가 나온 뒤 정한다), Map sensor.

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다.

```text
packages/py/kor-travel-common/src/kortravelcommon/{dagster,stall}.py
packages/py/kor-travel-common/tests/test_reconciliation_sensor.py
docs/runbooks/dagster-adoption.md, CHANGELOG.md
```

## 수용 기준

- [ ] 기존 `test_reconciliation_sensor.py`가 수정 없이 통과한다.
- [ ] 옛 형식 cursor로 시작한 sensor가 첫 tick에서 예외 없이 새 형식으로 넘어간다.
- [ ] 소비자 cursor가 tick 사이에 보존되고 code-server 재시작(새 프로세스)을 흉내 낸 시험에서도 남는다.
- [ ] 호환 시험: weather `e68f16a`의 `_alerted_stall`과 같은 판독(접두 `stall:` 뒤를 `json.loads`해 `StallClock.from_dict`)이 새 형식 cursor에서도 같은 결과를 낸다. 소비자 cursor가 있을 때와 없을 때 둘 다 확인한다.

## 검증 명령

```bash
cd packages/py/kor-travel-common
uv sync --locked --extra dev --extra dagster && uv run pytest -q tests/test_reconciliation_sensor.py tests/test_stall_pg_errors.py
```

## evidence

시험 출력. 소비자 실측은 `NOT_RUN(소비자 저장소)`.

## rollback·release 차단 조건

- 추가만 하는 변경. `git revert` 1회.
- 옛 cursor를 읽지 못하거나 위 호환 시험이 실패하면 병합하지 않는다.
