# T-314 회수 sensor의 선택형 소비자 cursor와 정체 시계 전달

- 상태: READY
- 우선순위: P3
- Gate: Python 단위·wheel 설치·2인 리뷰
- 선행: 없음
- 소유 저장소: kor-travel-common
- 병렬: 언제든. 다른 Python PR과 dev 번호가 겹치면 rebase

출처는 [공통화 재조사·계획(2026-11-17)](../plan/commonization-plan-2026-11-17.md)의 §3.4·§4.9(K-42)이다. 근거 위치(file:line)와 차이 분석은 그 문서가 정본이며 여기서 반복하지 않는다.

## 목표

공통 `reconciliation_sensor`가 sensor cursor를 소유해서 weather와 transport는 keyset 위치를 프로세스 메모리에 두고, weather는 공통의 비공개 cursor 접두 `stall:`을 직접 다시 읽는다. callback이 현재 정체 시계와 자기 하위 cursor를 공식 인자로 받게 한다.

## 고정 결정

- 기존 호출 모양은 그대로 동작한다(추가만).
- 회수 SQL·lease·fencing은 계속 소비자 소유다([dagster-adoption](../runbooks/dagster-adoption.md) §4·§19).
- 새 기능을 **켜지 않은** 호출자의 cursor는 지금과 byte 단위로 같다(`stall:` + 시계 JSON 또는 `null`). 소비자 구획은 켠 호출자에게만 쓴다.
- `StallClock.from_dict`는 엄격한 채로 둔다(필드가 더 있으면 거절). weather가 cursor를 직접 읽는 지금 방식(`sync_recovery.py:119-125`)은 켜지 않는 한 그대로 동작한다. 켜는 호출자는 cursor를 직접 읽는 것을 그만두고 `ReconcileTick.clock`을 써야 한다.
- Map의 회수 sensor는 대상이 아니다(주기·반환형·시계가 달라 factory에 맞지 않는다).
- T-026의 버전 규칙을 따른다.

## 구현 범위

1. `reconciliation_sensor`에 선택 인자를 더한다. 켜면 callback이 `ReconcileTick(clock, consumer_cursor)`를 받고 새 `consumer_cursor`(짧은 문자열, 길이 상한)를 돌려줄 수 있다.
2. 켠 호출자의 cursor 형식을 새로 정한다(접두를 달리해 옛 형식과 구분). 옛 형식 cursor에서 시작해도 첫 tick에 예외 없이 넘어간다.
3. 정체 경보 한 줄을 만드는 `format_stall_alert(event, clock, now)`를 `stall.py`에 둔다.
4. 단위 시험: 켜지 않은 호출자의 byte 동일성, 켠 호출자의 cursor 왕복·길이 상한·옛 cursor에서의 전환, 정체 시계 전달.
5. 가이드 §19 갱신. 켜는 절차(cursor 직접 판독 제거)를 적는다.

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

- [ ] 켜지 않은 호출자: 같은 시계에 대해 cursor 문자열이 `97f8ed9`의 인코더 출력과 byte 단위로 같다(시험).
- [ ] 그 cursor에서 weather `8c3b474`의 `_alerted_stall`과 같은 판독(접두 `stall:` 뒤를 `json.loads`해 `StallClock.from_dict`)이 바꾸기 전과 같은 값을 낸다(시험).
- [ ] 기존 `test_reconciliation_sensor.py`와 `test_stall_pg_errors.py`가 수정 없이 통과한다.
- [ ] 켠 호출자: 소비자 cursor가 tick 사이에 보존되고, 옛 형식 cursor로 시작해도 첫 tick이 예외 없이 끝난다.
- [ ] `pyproject.toml` 버전이 올랐다.

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
