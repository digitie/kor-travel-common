# T-304 C4 health(`/health`·`/readyz`·`/version`·alias 옵션) + C13 time

- 상태: BLOCKED
- 우선순위: P1
- Gate: 단위 테스트
- 선행: T-302

## 목표

liveness는 7곳 모두 유사하지만 경로가 `/health`(6) vs `/healthz`(1)로 갈리고 deep readiness는 geo 하나뿐이며 airport `/health`는 DB를 질의한다([be §2.5](../survey/cross/backend.md), [oa §2.10](../survey/cross/openapi.md)). 이 task는 `[api]` extra에 라우터 팩토리 `health_router()`(`/health` 무의존 liveness · `/readyz` 의존성 점검 503 · `/version`)를, core에 `kortravelcommon.time`(`KST=ZoneInfo`, `kst_now/utc_now`, aware 검증)을 넣는다. 기존 경로는 alias 옵션으로 유지해 소비자 probe(pinvi `admin/system.py`, ktdm healthcheck, Prometheus)를 깨지 않는다.

## 고정 결정

- [design-brief](../plan/design-brief.md) D-14(M5 `/health`·`/readyz`·`/version` 신규 MUST/기존 SHOULD, geo `/v1/healthz` 별칭 무기한, N8 liveness에서 외부 의존성 금지, M7 tz-aware), D-15(C4·C13 1차, core는 stdlib+pydantic), D-22. ADR-009·ADR-011 — [ADR 색인](../adr/README.md). 규칙 정본: [openapi](../standards/openapi.md), [backend-stack](../standards/backend-stack.md).
- readiness 알고리즘은 geo `ReadinessResponse{status, ready, degraded, components}`(DB 프로브 타임아웃·pool 이용률·503)를 원형으로 하되 개별 체크는 앱이 콜러블로 주입한다([be C4](../survey/cross/backend.md)). `/version`은 map·weather 형식(`{service, version, git_commit}`)을 기본으로, map의 `{data, meta}` envelope는 `wrap` 콜러블 옵션으로 보존한다(계약 무변경, T-480 조건).
- 시간: `KST = ZoneInfo("Asia/Seoul")`(kta·map·pinvi), `kst_now/utc_now` 이름(map·ktw·pinvi 동일), `check_aware_datetime`(map ADR-019). ktw 고정 오프셋·ktdm naive UTC 전환은 앱 명시 결정([be §2.12](../survey/cross/backend.md)) — 이 task는 강제하지 않는다.
- 근거 정정: readiness 경로 표기는 `/readyz`([survey/README §6.2](../survey/README.md)).

## 구현 범위

1. `kortravelcommon/time.py`(core, stdlib만): `KST`, `UTC`, `kst_now()`, `utc_now()`, `to_kst(dt)`, `to_utc(dt)`, `check_aware_datetime(value, *, field=None)`(naive면 `ValueError`), `ensure_aware(value, *, assume=None)`. kta의 `align_to_interval`·`split_by_local_day`는 포함 후보(리뷰에서 결정; 미포함 시 T-482에서 앱 잔류).
2. `kortravelcommon/api/health.py`(`[api]`): `health_router(service_name, version, *, git_commit=None, readiness_checks=(), aliases={}, wrap=None, include_in_schema=True, readiness_timeout_s=2.0) -> APIRouter`. `/health`는 어떤 I/O도 하지 않는다. `/readyz`는 체크를 타임아웃 안에서 병렬 실행해 하나라도 실패·타임아웃이면 503과 `components[]`를 반환한다. `aliases={"/v1/healthz": "/health", "/v1/readyz": "/readyz"}`처럼 같은 핸들러를 legacy 경로에 추가 등록한다.
3. 응답 모델 `HealthResponse`·`ReadinessResponse`·`VersionResponse`(pydantic v2)와 OpenAPI 503 선언.
4. 단위 테스트(httpx `TestClient`): liveness가 체크를 호출하지 않음, readiness 성공/실패/타임아웃 3분기, alias 등록, `wrap` 적용, `include_in_schema=False` 시 스키마 제외, starlette 0.4x/1.6 양쪽.
5. `docs/standards/openapi.md` M5·N8 절에 팩토리 사용 예와 alias 규칙을 링크(standards-be 소유자와 합의).

## 범위 밖

request-id·metrics(T-307), problem+json(T-308), 앱별 경로 이동 PR과 probe·Prometheus 설정 변경(T-480~T-486, 특히 geo T-483 별칭 병행), `/metrics` 엔드포인트(T-307), 좌표 경계 상수(C14 보류·공통화 금지), ktdm naive UTC 전환 결정(T-486).

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다.

```text
packages/py/kor-travel-common/src/kortravelcommon/time.py
packages/py/kor-travel-common/src/kortravelcommon/api/health.py
packages/py/kor-travel-common/tests/test_time.py
packages/py/kor-travel-common/tests/api/test_health.py
docs/standards/openapi.md                      # M5·N8 예시 링크(standards-be 합의)
```

## 수용 기준

- [ ] `kortravelcommon.time`이 fastapi·pydantic 없이 import되고(`python -c "import kortravelcommon.time"`, `[api]` 미설치 venv), `check_aware_datetime(datetime(2026,9,6))`가 `ValueError`, aware 값은 그대로 반환된다.
- [ ] `kst_now().tzinfo.key == "Asia/Seoul"`, `utc_now().utcoffset() == timedelta(0)`.
- [ ] `/health`가 readiness 체크를 한 번도 호출하지 않음을 mock 카운트로 단언한다(N8).
- [ ] `/readyz`가 체크 실패·타임아웃 시 503과 `components` 항목별 상태를 반환하고, 성공 시 200 `ready: true`.
- [ ] alias로 등록한 `/v1/healthz`·`/v1/readyz`가 원 경로와 같은 본문을 반환하고 OpenAPI에 두 경로가 모두 있다(또는 `include_in_schema` 옵션대로 제외).
- [ ] `wrap=lambda body: {"data": body, "meta": {...}}` 옵션으로 map 형식 응답이 재현된다.
- [ ] pytest 테스트 수 ≥ 12, skip 0, starlette 두 버전 모두 green; `mypy --strict`·`ruff`·`lint-imports` 통과.

## 검증 명령

```bash
cd packages/py/kor-travel-common
uv sync --locked --all-extras && uv run pytest tests/test_time.py tests/api/test_health.py -q
python3 -m venv /tmp/ktc-core && /tmp/ktc-core/bin/pip install . && /tmp/ktc-core/bin/python -c "import kortravelcommon.time"
uv pip install --python .venv/bin/python "starlette<1.0" && uv run pytest tests/api/test_health.py -q
uv run mypy --strict src && uv run ruff check src tests && uv run lint-imports
```

## evidence

이 파일 하단 "실행 기록"에 테스트 수·starlette 버전별 결과·core-only import 결과를 남긴다. 소비자 probe 호환(pinvi·ktdm·Prometheus) 확인은 각 앱 task evidence이며 여기서는 `NOT_RUN(앱 task)`.

## rollback·release 차단 조건

- 패키지 내부 모듈이라 `git revert` 1회로 원복된다.
- `/health`가 I/O를 수행하거나 alias 없이 legacy 경로가 사라지는 구현이면 `py-v0.1.0-rc`(T-310)에 포함하지 않는다. `time`이 `[api]` 의존을 끌어오면 geo·map import-linter 계약 위반이므로 릴리스 차단.
