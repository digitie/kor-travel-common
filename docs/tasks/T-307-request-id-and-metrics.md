# T-307 C2 request_id(`trust_incoming`·형식 검증) + C3 metrics(표준 라벨·센티널·multiproc; 접두 인자)

- 상태: BLOCKED
- 우선순위: P1
- Gate: 단위 테스트
- 선행: T-304, T-310

## 목표

요청 ID 정책이 서버 발급 강제(ktdm)·클라이언트 수용(ktw·pinvi)·없음(kta·ktc)으로 갈리고([be §2.3](../survey/cross/backend.md)), HTTP 메트릭은 5개 구현이 같은 세 지표를 만들면서 접두 6종·경로 라벨 2종·상태 라벨 3종·미매칭 센티널 4종을 쓴다([be §2.4](../survey/cross/backend.md)). 이 task는 `[api]` extra에 (1) 순수 ASGI `RequestIdMiddleware`(형식 검증·`trust_incoming` 옵션·contextvar·logging Filter·structlog 선택 훅)와 (2) `HttpMetrics`(접두 인자, 표준 라벨 `method,route,status_code`, 미매칭 센티널, multiprocess, `/metrics` 엔드포인트 헬퍼)를 넣는다. 접두·헤더 이름은 인자이며 앱 소유다.

## 고정 결정

- [design-brief](../plan/design-brief.md) D-14(M4 `X-Request-ID` 즉시 MUST; 형식 UUID v4/v7·ULID·≤128자 ASCII; 검증 실패 시 서버 발급; `trust_incoming=False` 앱 옵션), D-15(2차 C2·C3; 표준 HTTP 3지표·라벨·센티널·multiproc; 접두는 인자; 신규 `kt<x>_` MUST, map `kor_travel_map_`·pinvi `pinvi_api_`는 기한부 예외 review 2026-12), D-22. ADR-009·ADR-011 — [ADR 색인](../adr/README.md). 규칙 정본: [openapi](../standards/openapi.md) `X-Request-ID` 절, [backend-stack](../standards/backend-stack.md) 메트릭 접두 절.
- 메트릭 접두 map·pinvi 예외는 **열림(O-12, 사용자 확인 필요)**; 기본값 = 기한부 예외(대시보드 5종 영향 평가 후 재판정, [ci §1.13](../survey/cross/ci-deploy.md)). 이 task는 접두를 강제하지 않고 문서 규칙만 참조한다.
- 표준 지표: `<prefix>http_requests_total{method,route,status_code}`, `<prefix>http_request_duration_seconds`(버킷 geo·pinvi 동일 11개 기본, 인자로 교체), `<prefix>http_requests_in_progress{method}`. 미매칭 센티널 기본 `__unmatched__`(map·pinvi), 인자로 `/<unmatched>`·`other` 등 기존 값 유지 가능. 라벨 정규화 콜백(ktc) 옵션.
- `/metrics`는 `include_in_schema=False` + 인증 의존성은 앱 주입(Bearer/`X-API-Key`/`?key=` 상이, [oa §6 Q11](../survey/cross/openapi.md)); production fail-closed 판단은 앱 settings.
- 요청 ID 형식 검증 규칙만 공통, 발급 주체(BFF vs 백엔드)는 앱 결정([be §7-5](../survey/cross/backend.md), [oa §6 Q9](../survey/cross/openapi.md)).

## 구현 범위

1. `kortravelcommon/api/request_id.py`: `RequestIdMiddleware(app, *, header="X-Request-ID", trust_incoming=True, validator=is_valid_request_id, generator=new_request_id, expose_duration_header=False)`(순수 ASGI, starlette `BaseHTTPMiddleware` 미사용), `current_request_id()`, `RequestIdLogFilter`, `bind_structlog_contextvars()`(structlog import 가능할 때만). 검증기: UUID v4/v7 또는 ULID, ≤128자 ASCII, 제어문자 금지.
2. `kortravelcommon/api/metrics.py`: `HttpMetrics(prefix, *, registry=None, buckets=DEFAULT_BUCKETS, unmatched="__unmatched__", label_normalizer=None, multiprocess_env="PROMETHEUS_MULTIPROC_DIR")`, `HttpMetricsMiddleware`(route template 해석, 미매칭 센티널), `metrics_endpoint(metrics, *, dependencies=())`, `build_registry(multiprocess: bool)`(`MultiProcessCollector` 분기), prometheus_client 부재 시 `_NoopMetric`(geo)로 폴백. DB pool gauge·엔진 쿼리 훅은 T-306 `on_engine_created`에 연결하는 헬퍼(후보).
3. 테스트: 헤더 echo/생성/거부(길이 129·비ASCII·`trust_incoming=False`), 응답 헤더 항상 존재, contextvar가 요청 간 누수 없음, 로그 레코드에 request_id 주입, 메트릭 이름·라벨 집합 정확 일치, 미매칭 경로 센티널, multiprocess 디렉터리 모드에서 수집, `/metrics`가 스키마에 없음, starlette 0.4x/1.6 양쪽.
4. `docs/standards/openapi.md` `X-Request-ID` 절과 `backend-stack.md` 메트릭 절에 사용 예 링크(standards-be 소유자와 합의).

## 범위 밖

structlog JSON 로깅 설정 함수(C2 로깅 본체는 앱 소유 유지; `configure_logging`은 후속 재평가), 에러 본문 `request_id` 주입(T-308 C5가 `current_request_id()`를 사용), 앱별 접두 변경·대시보드 갱신(O-12·T-480/T-484), `/metrics` 인증 방식 통일(앱 소유), Dagster 메트릭 서버(T-308 C18).

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다.

```text
packages/py/kor-travel-common/src/kortravelcommon/api/request_id.py
packages/py/kor-travel-common/src/kortravelcommon/api/metrics.py
packages/py/kor-travel-common/tests/api/{test_request_id.py,test_metrics.py}
docs/standards/openapi.md                       # X-Request-ID 사용 예 링크(standards-be 합의)
docs/standards/backend-stack.md                 # 메트릭 절 링크(standards-be 합의)
```

## 수용 기준

- T-302의 공개 facade 계약에 따라 내부 api 구현과 최상위 공개 모듈 재수출을 함께 완성한다. wheel 설치본의 문서 예시 import가 통과하고 core-only import에는 프레임워크 의존이 새지 않는다.

- [ ] 유효한 UUID v4/v7·ULID 수신 값은 그대로 echo되고, 129자·비ASCII·제어문자 값은 폐기 후 서버 발급값으로 대체되며, `trust_incoming=False`면 항상 서버 발급이다(각각 테스트 1개 이상).
- [ ] 모든 응답(에러 포함)에 `X-Request-ID`가 있고 `current_request_id()`가 핸들러·백그라운드 로그 필터에서 같은 값을 돌려준다.
- [ ] `HttpMetrics("ktx_")` 등록 후 `generate_latest()` 출력에 정확히 `ktx_http_requests_total`·`ktx_http_request_duration_seconds`·`ktx_http_requests_in_progress`가 있고 라벨이 `method,route,status_code`(in_progress는 `method`)다.
- [ ] 미등록 경로 요청이 `route="__unmatched__"`로 집계되고 인자로 바꾼 센티널도 반영된다.
- [ ] `PROMETHEUS_MULTIPROC_DIR` 설정 시 `MultiProcessCollector` 경로로 수집되고, prometheus_client 미설치 venv에서 미들웨어 import가 실패하지 않는다(noop).
- [ ] `/metrics`가 OpenAPI 산출물에 없다(`export --check` fixture와 결합).
- [ ] pytest 테스트 수 ≥ 16, skip 0, starlette 두 버전 green; `mypy --strict`·`ruff`·`lint-imports` 통과.

## 검증 명령

```bash
cd packages/py/kor-travel-common
uv sync --locked --all-extras && uv run pytest tests/api/test_request_id.py tests/api/test_metrics.py -q
uv pip install --python .venv/bin/python "starlette<1.0" && uv run pytest tests/api -q
PROMETHEUS_MULTIPROC_DIR=$(mktemp -d) uv run pytest tests/api/test_metrics.py -q -k multiprocess
uv run mypy --strict src && uv run ruff check src tests && uv run lint-imports
```

## evidence

이 파일 하단 "실행 기록"에 테스트 수·starlette 버전별 결과·multiprocess 모드 결과를 남긴다. map·pinvi 대시보드 영향 평가는 O-12 결정 문서(T-480·T-484 evidence)로 넘기고 여기서는 `NOT_RUN(앱 task)`.

## rollback·release 차단 조건

- 패키지 내부 모듈이라 `git revert` 1회로 원복된다.
- 미들웨어가 `BaseHTTPMiddleware`에 의존하거나(스트리밍·starlette 버전 차이 위험) 검증 실패 값을 그대로 echo하면 `py-v0.1.x`에 포함하지 않는다. 메트릭 이름이 접두 없이 고정되면 map·pinvi 예외를 적용할 수 없으므로 릴리스 차단.
