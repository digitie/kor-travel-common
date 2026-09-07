# kor-travel-common Python 백엔드 스택 규약

이 문서는 [규칙 문서 색인](README.md)에 속한 Python 백엔드(FastAPI·SQLAlchemy·alembic·Dagster) 공통 규약과 공통 패키지 `kor-travel-common`(import `kortravelcommon`)의 구조 정본이다. 정본 지위: **확정 초안(문서)** — [브리프](../plan/design-brief.md) D-15·D-06·D-07·D-11을 규칙 ID `BE-n`으로 옮긴 것이며, 패키지 실물(T-302 골격·T-305 quality 산출물·T-310 py-v0.1.0)과 대조해 확정하는 task가 남아 있다. 확정 task: T-302. 마지막 갱신: 2026-09-06.

REST/OpenAPI 계약(에러 본문·health 경로·요청 ID·헤더 이름)은 [openapi](openapi.md)가 정본이고 이 문서는 구현 모듈만 정한다. 버전 값(floor/recommended)은 [versions](versions.md)와 `versions.json`이 정본이며 이 문서는 값을 복제하지 않는다.

## 1. 목표와 기준

- 7개 저장소 Python 코드 19개 항목을 비교한 결과, 설정 클래스 6곳·메트릭 5곳·공개 API 키 함수 4곳(본문 동일)·OpenAPI export 4곳·alembic env 3곳(동형)·ruff 기본 규칙 5곳이 이미 수렴해 있다(사실: [backend 횡단 비교](../survey/cross/backend.md) §2.19). 공통 패키지는 이 수렴 구간만 담고, 도메인 결합 부분(§10)은 담지 않는다.
- 런타임 공유 백엔드나 SSO는 만들지 않는다. 얇은 계약 코드(problem 핸들러·request-id·export/drift·health·time·quality 산출물)만 배포한다(`be` §6; `oa` §3.5).
- 공통 패키지는 앱 → common 단방향이며 앱 도메인 모듈·지도 엔진·provider 라이브러리(`python-*-api`)·인증 서버를 import하지 않는다. 저장소·키를 주입받는 공용 인증 프리미티브는 common API로 제공한다([ADR-015](../adr/015-common-shared-systems-scope.md)).
- 앱의 env 이름·접두·메트릭 이름·응답 형식·경로는 배포 계약이다. 공통 모듈은 이름을 인자로 받고, 기본값이 계약을 바꾸는 경우 opt-in으로만 둔다.

## 2. 문서 사용법

| 변경 대상 | 상세 정본 |
|---|---|
| Python floor·이미지·lockfile 의무·라이브러리 범위 값 | [versions](versions.md)·`versions.json`(값), 이 문서 §3(규칙) |
| ruff·mypy·import-linter·pre-commit 베이스 | 이 문서 §4, 산출물은 T-305 `templates/python/*`(미생성) |
| settings·logging·metrics·health·errors·time 규약 | 이 문서 §5, 계약은 [openapi](openapi.md) M3~M5·M7 |
| DB 엔진·alembic·테스트 하네스 | 이 문서 §6·§7 |
| 공통 패키지 구조·extras·모듈 우선순위 | 이 문서 §8, 결정 이유는 [ADR-011](../adr/011-python-common-package.md)([ADR 색인](../adr/README.md)) |
| 배포 채널(git 태그·wheel)·소비 방법 | 이 문서 §9, 절차는 [release](../runbooks/release.md)·[consumer adoption](../runbooks/consumer-adoption.md) |
| 공통화 금지 목록 | 이 문서 §10 |
| 예외 등록 | [openapi-exceptions.yaml](openapi-exceptions.yaml)(`BE-n` 규칙 허용), 버전 값 예외는 `versions.json` `exceptions[]` |
| 라이선스·패키지 메타데이터 | [licensing](licensing.md) §6 |
| CI 재사용 워크플로(`python-quality.yml`) | [ci-deploy](ci-deploy.md) §3 |

## 3. 런타임·빌드 기준선

| ID | 규칙 | 현행 근거 | 정합 task |
|---|---|---|---|
| BE-1 | 공통 패키지는 `requires-python = ">=3.11"`이며 3.11 문법으로 쓴다(PEP 695 제네릭 등 3.12 전용 문법 금지; CI가 3.11 인터프리터로 컴파일 검사). 앱 `requires-python`은 앱 소유이고 3.12 상향은 Phase 4 앱별 결정(O-7). 컨테이너 이미지는 `python:3.12-slim` digest 핀 권장, 3.13 허용, 3.11-slim이 floor | map·weather·ktdm 3.11 / airport·geo·pinvi 3.12; geo `cli/main.py:92` PEP 695(`be` §2.1); floor 정정값은 [survey README](../survey/README.md) §6.2 | T-302(3.11 문법 검사) |
| BE-2 | `pyproject.toml` + `uv.lock`이 의무다. CI와 Docker는 모두 `uv sync --locked`로 설치하고 lock을 소비하지 않는 `pip install -e`는 금지한다. `requirements.txt`(concierge)와 Poetry 매니페스트(ktdm)는 uv로 전환한다. uv 버전은 `versions.json` | weather만 CI·Docker 일관(`be` §2.1); airport Docker pip, pinvi CI·Docker pip; concierge `mcp<2` 사고(`vm` §7.3) | concierge T-450, ktdm T-471, airport T-482, pinvi T-484, geo T-440 |
| BE-3 | 공통 패키지 `[api]` extra의 FastAPI·Starlette 범위: `fastapi>=0.115`, starlette 범위는 선언하지 않고 CI에서 0.4x/1.6 매트릭스로 호환을 보증한다. map `starlette>=0.40,<1.0` 상한은 T-480 재검증 전까지 예외 | airport·weather·pinvi lock starlette 1.6.0 + httpx 0.28.1, map 상한 주석(`be` §2.1; `oa` Q7) | T-302(매트릭스), T-480 |
| BE-4 | provider 라이브러리(`python-*-api`)는 `git+https://…@<sha>` 또는 불변 태그로만 핀한다. `@main` 등 이동 참조는 금지한다. SHA 정렬 주체는 각 저장소이며 common `versions.json` `providers` 절은 보고만 한다(O-16). 같은 라이브러리의 두 배포 경로(weather vendored path vs map git+sha)는 T-505 정리 요청 대상 | pinvi etl `python-kasi-api@main`, kma SHA 불일치(`be` §5.1) | pinvi T-484, T-505 |
| BE-5 | 기존 앱의 하한 전용 선언(`>=` only)은 lock 도입과 함께 `versions.json` floor 이상으로 상향하고, `blocked[]`(예: `mcp>=2`)는 선언 상한으로도 막는다 | ktdm `fastapi ^0.110`(두 minor 세대 차이), concierge `>=`만(`be` §2.1) | ktdm T-471, concierge T-450 |

## 4. 품질 게이트

C20 quality 산출물은 코드가 아니라 설정 파일이며 `templates/python/`(T-305)에서 배포한다. 앱은 파일을 저장소에 복사하고 머리 주석의 common 버전으로 drift를 추적한다(추정: ruff `extend`는 로컬 경로만 받으므로 패키지 데이터 참조 대신 복사한다 — T-305에서 확정).

| ID | 규칙 | 현행 근거 |
|---|---|---|
| BE-6 | ruff 베이스: `line-length = 100`, `select = ["E","F","I","UP","B","ASYNC"]`. 앱은 `[tool.ruff] extend = "ruff-common.toml"`로 참조하고 규칙군을 더할 수만 있다(빼려면 `per-file-ignores`). `target-version`은 앱 소유. **`ruff format` 규칙은 common에 없다**(앱 선택; ktdm은 재포맷 금지 상태로 업그레이드) | ruff 설정 5곳 모두 `line-length=100` + `E,F,I,UP,B,ASYNC` 공통(`be` §2.17) |
| BE-7 | baseline: 0에서 도입하는 앱(airport·concierge)은 첫 PR에서 `per-file-ignores`·`extend-exclude` baseline으로 시작하고, 신규 파일에는 baseline을 적용하지 않으며 분기 감사(T-506)에서 축소한다 | airport·concierge ruff 없음(`be` §2.17); 매트릭스 §2.4 C20 비고 |
| BE-8 | mypy 베이스: `strict = true`, `plugins = ["pydantic.mypy"]`, `warn_unused_ignores = true`. `[[tool.mypy.overrides]]` baseline 허용(모듈 단위, 사유 주석 필수) | geo·map·weather·pinvi strict(`be` §2.17) |
| BE-9 | import-linter 계약 템플릿: layers `api > cli > client > loaders > infra > core > dto`(앱이 자기 계층으로 치환), forbidden `core`·`dto` → `fastapi`·`starlette`·`uvicorn`. 공통 패키지 자체도 `kortravelcommon` core 모듈이 stdlib+pydantic만 import하는 계약을 CI에서 검사한다 | geo layers, map forbidden 3종(`be` §2.17·§3 전제) |
| BE-10 | pre-commit 템플릿은 `repo: local` + `language: system`(map 방식)으로 두어 hook rev와 lock 버전이 어긋나지 않게 한다. hook에 별도 rev를 두는 방식(geo ruff v0.7.4/mypy v1.13.0 vs lock 0.16/2.3)은 금지 | geo·map pre-commit(`ci` §1.4) |
| BE-11 | CI는 [ci-deploy](ci-deploy.md) `python-quality.yml`(Phase 4, T-401) inputs로 `ruff check`·`ruff format --check`(옵션)·mypy·lint-imports·`alembic check`·pytest를 호출한다. 게이트 폭은 inputs로 조절하되 `ruff check`·pytest는 끄지 못한다 | `ci` §2.1 |

### 4.1 산출물 예시(T-305에서 실물과 대조)

앱이 복사하는 `ruff-common.toml`(머리 주석의 버전으로 drift 추적):

```toml
# kor-travel-common quality base — py-v0.1.0 (변경은 common PR로만)
line-length = 100

[lint]
select = ["E", "F", "I", "UP", "B", "ASYNC"]
```

앱 `pyproject.toml`에서의 참조(규칙군 추가만 허용, 제외는 baseline으로):

```toml
[tool.ruff]
extend = "ruff-common.toml"
target-version = "py312"

[tool.ruff.lint]
extend-select = ["RUF", "S"]

[tool.ruff.lint.per-file-ignores]
"tests/**" = ["S101"]

[tool.mypy]
strict = true
plugins = ["pydantic.mypy"]
warn_unused_ignores = true

[tool.importlinter]
root_package = "kortravelweather_api"

[[tool.importlinter.contracts]]
name = "core stays framework-free"
type = "forbidden"
source_modules = ["kortravelweather_api.core", "kortravelweather_api.dto"]
forbidden_modules = ["fastapi", "starlette", "uvicorn"]
```

## 5. 런타임 규약

| ID | 모듈(C-ID) | 규칙 | 현행 근거 | task |
|---|---|---|---|---|
| BE-12 | `settings`(C1) | `BaseSettings` 베이스: `.env` 튜플(`(ROOT/.env, .env)`), `extra="ignore"`, `hide_input_in_errors=True`, 비밀은 `SecretStr`, ValidationError의 input을 `<redacted>`로 재작성(pinvi), `get_settings()/set_settings()` 싱글턴(geo 방식). **env 접두·이름은 앱 소유이며 불변**(배포 `.env` 계약). 신규 앱은 `KOR_TRAVEL_<APP>_`, 기존 `KTG_`·`KTC_`·`KTDM_`·`PINVI_`는 유지. 앱당 접두 하나(airport 접두 없음 44키·concierge 혼합은 정리 대상) | 6/7 동일 골격(`be` §2.2); 접두 집계(`ci` §1.11·§3.2) | T-306 |
| BE-13 | `logging`·`request_id`(C2) | 순수 ASGI `RequestIdMiddleware(header="X-Request-ID", trust_incoming=True, validator=…)` + contextvar + stdlib `Filter` + structlog 선택 훅 + `mask_secret`. 형식 검증·발급 규칙은 [openapi](openapi.md) M4·M4.1. JSON/console 스위치는 geo·map 설정 필드 이름(`log_format`)을 그대로 소비 | pinvi 구현, geo·map 설정만, ktdm 서버 발급 필터(`be` §2.3) | T-307 |
| BE-14 | `metrics`(C3) | 표준 HTTP 3지표 `<prefix>http_requests_total{method,route,status_code}`·`<prefix>http_request_duration_seconds{method,route}`·`<prefix>http_requests_in_progress{method}`, 라벨 값은 route template, 미매칭 센티널 `__unmatched__`, 라벨 정규화, `PROMETHEUS_MULTIPROC_DIR` 지원, DB pool gauge·엔진 쿼리 훅 옵션, prometheus_client 부재 시 noop(geo). **접두는 인자**이며 신규 서비스는 `kt<x>_` MUST(D-22), map `kor_travel_map_`·pinvi `pinvi_api_`는 기한부 예외(review 2026-12, 대시보드 영향 평가 후 재판정, O-12). `/metrics`는 `include_in_schema=False` + production 토큰 필수, 방식은 Bearer 권장(후보; `X-API-Key`·`?key=`는 앱 예외) | 5곳 유사, 접두 6종·라벨 이름 2종·센티널 4종(`be` §2.4) | T-307 |
| BE-15 | `health`(C4) | `health_router(service_name, version, commit_env, readiness_checks=[…], aliases=[…])`가 `/health`·`/readyz`·`/version`을 만든다. readiness는 geo 알고리즘(DB 프로브 타임아웃·pool 이용률 0.8 degraded·admission → 503). 기존 경로(geo `/v1/healthz`)는 `aliases`로 병행하고 폐기하지 않는다(pinvi가 타 서비스 `/health`를 프로브). envelope(`{data,meta}`) 여부는 옵션 | 7곳 liveness, geo만 readiness(`be` §2.5; `oa` M5) | T-304 |
| BE-16 | `errors`·`problem`(C5) | 베이스 예외 `KorTravelError(code, http_status, hint)`(geo 형태) + `register_problem_handlers(app, *, type_base, code_by_status, exclude_paths=[…], include_validation_input=False)` + `augment_openapi_problem_responses(schema)`. 핸들러는 **opt-in**이며 `exclude_paths`로 geo v1 VWorld 경로처럼 앱 핸들러가 우선하는 접두를 제외한다. 본문 계약은 [openapi](openapi.md) M3·M3.1~M3.3·S7.1 | map·weather 형식 일치, airport additive(`be` §2.10; `oa` §5 C1) | T-308 |
| BE-17 | `security_headers`(C16)·`cors`(C17)·`trusted_proxy`(C8) | 보안 헤더 미들웨어(nosniff·`X-Frame-Options: DENY`·Referrer-Policy·Permissions-Policy·CSP·HSTS)는 **HSTS 발급 시 `X-Forwarded-Proto`를 불신**(pinvi #344)이 기본이고 `trust_forwarded_proto=True`는 앱 옵션. CORS csv 파서는 `*`와 credentials 동시 사용을 제거하고 브라우저 표면에만 적용(S11). trusted proxy는 CIDR + 비밀 상수시간 비교 + actor/roles 파싱 원시 함수만 제공하며 헤더 이름은 인자([openapi](openapi.md) M8.1) | airport·pinvi 보안 헤더 정반대 조건, ktc·ktdm csv 파서 동일(`be` §2.9·§2.8) | T-308 |
| BE-18 | `public_api_key`(C7) | `generate_public_api_key()`(32자 `ascii_letters+digits`, CSPRNG)·`hash_public_api_key()`(strip 후 무염 SHA-256)·`matches()`·`key_hint`(`[-6:]`)·상태 `active/revoked`·TTL 캐시·저장소 `Protocol`. 저장 스키마와 `?key=` 허용 여부는 앱 소유(N2) | ktc·ktdm·geo·map 본문 동일(`be` §2.8) | T-306 |
| BE-19 | `time`(C13) | `KST = ZoneInfo("Asia/Seoul")`, `kst_now()`, `utc_now()`(aware), `check_aware_datetime()`(naive 거부), 한국식 timestamp 파서·간격 정렬(airport). 고정 오프셋 `timezone(timedelta(hours=9))`(weather)과 naive UTC(ktdm)는 전환 시 명시 결정([openapi-exceptions.yaml](openapi-exceptions.yaml) ktdm M7) | map·weather·pinvi 함수 이름 동일(`be` §2.12) | T-304 |
| BE-20 | `http`(C15) | `httpx.AsyncClient` 팩토리(`httpx.Timeout` 프로파일), tenacity 재시도 정책(geo 파라미터: 3회, 지수 0.2→2.0초), api-call 이벤트 훅(민감 쿼리 키 마스킹). 호출마다 `AsyncClient`를 만드는 관행은 lifespan 공유로 전환 권고 | geo tenacity, pinvi·weather 수제 동형(`be` §2.11) | T-308 |
| BE-21 | `dagster`(C18) | `build_definitions(required_keys, defaults, real_resources)` 3단 폴백(value → real `@resource` → missing-guard; geo=map 동일), `run_failure_sensor` 통지 어댑터, `dagster.yaml` postgres 템플릿. op/job vs asset 스타일은 앱 소유 | geo·map 골격 동일(`be` §2.14) | T-308 |
| BE-22 | 인증 공용 코어·앱 소유 경계 | 비밀번호 해시·세션/토큰·CSRF·JWT·RBAC 검증 프리미티브와 주입 인터페이스는 common에 둘 수 있다. 사용자·세션 저장소, 키·비밀, 외부 IdP, 역할/라우트 판정과 운영 rate limit은 앱이 소유한다. 세션 상수(8h·PBKDF2 310k·5회/10분)는 구현 task에서 계약을 고정한다 | ADR-015·T-312 | T-312 |

### 5.1 사용 예시(후보 API — T-304·T-307·T-308에서 확정)

```python
from fastapi import FastAPI
from kortravelcommon.health import health_router
from kortravelcommon.metrics import HttpMetricsMiddleware
from kortravelcommon.problem import register_problem_handlers
from kortravelcommon.request_id import RequestIdMiddleware

app = FastAPI(title="kor-travel-weather API", servers=[])
app.add_middleware(RequestIdMiddleware, header="X-Request-ID", trust_incoming=True)
app.add_middleware(HttpMetricsMiddleware, prefix="ktw_")
register_problem_handlers(
    app, type_base="about:blank", code_by_status={429: "TOO_MANY_REQUESTS"}, exclude_paths=[]
)
app.include_router(
    health_router(
        service_name="kor-travel-weather-api",
        version=__version__,
        commit_env="KOR_TRAVEL_WEATHER_GIT_COMMIT",
        readiness_checks=[db_probe],
        aliases=[],
    )
)
```

인자 이름은 후보이며 확정값은 패키지 docstring과 [openapi](openapi.md)가 정본이다. 미들웨어 등록 순서는 request-id → metrics → 앱 미들웨어 순으로 두어 메트릭·로그에 요청 ID가 먼저 바인딩되게 한다.

## 6. DB·alembic 규약

| ID | 규칙 | 현행 근거 | task |
|---|---|---|---|
| BE-23 | `db`(C9): `normalize_dsn(url, driver=…)`(`postgres://`·`postgresql://` → `+asyncpg`/`+psycopg`), `make_async_engine(dsn, *, pool_size, max_overflow, pool_timeout, pool_recycle, pre_ping=True, statement_timeout, search_path, server_settings)`가 asyncpg `server_settings`와 psycopg `options`를 흡수, `make_session_factory(expire_on_commit=False)`, `get_db` 의존성 팩토리, 엔진 메트릭 훅. sync(weather psycopg)는 별도 함수. 세션 GUC 기본값(lock/idle/statement timeout, search_path)은 앱 인자 | asyncpg 4곳 동일 골격, psycopg async 1, sync 1, SQLite 1(`be` §2.6) | T-306 |
| BE-24 | alembic 템플릿(C10): async `env.py` 골격(airport≈concierge≈pinvi), `NullPool`, settings URL 주입, `%`→`%%` 이스케이프(weather), 선택적 `pg_advisory_xact_lock`(pinvi), `compare_type`·`compare_server_default`, CI `alembic upgrade head` + `alembic check`, `alembic/versions`는 ruff format 제외(byte 불변). 적용된 리비전 파일은 수정하지 않는다. 리비전 명명은 신규 앱 `NNNN_slug`(airport·weather) 권장, 기존 명명(`YYYYMMDD_NNNN_slug`·baseline 번호대)은 유지. geo(raw SQL)·map(300 baseline 봉인)은 도메인 가드로 템플릿 대상 밖 | 명명 4종, env 동형 3곳(`be` §2.7) | T-308 |
| BE-25 | PostgreSQL/PostGIS major는 라이브러리 정렬 범위 밖 별도 트랙(현 16 + 3.5 digest 핀). 앱 간 DB 이름·인스턴스 경계는 ktdm `docs/ports.md`가 정본 | `vm` §3.4; `ci` §1.8 | — |

## 7. 테스트 하네스

| ID | 규칙 | 현행 근거 | task |
|---|---|---|---|
| BE-26 | `testing`(C11) `[testing]` extra는 두 계열을 모두 지원한다: (a) testcontainers PostGIS 픽스처(이미지 digest 핀 옵션, template0 fresh DB, `alembic upgrade head`), (b) 외부 DSN + `_pg_guard`(보호 DB 이름·세그먼트 규칙·거부 시 세션 실패) + skip. 격리는 TRUNCATE 기본, loop scope는 `asyncio_default_fixture_loop_scope`를 명시(session 또는 function)하고 Windows selector 정책을 포함 | testcontainers(map·pinvi) vs DSN(geo·ktc·wx·kta)(`be` §2.16) | T-308 |
| BE-27 | pytest·pytest-asyncio 값은 `versions.json`(floor 8 / 0.23). `filterwarnings = error` 권장(map). 0 test·skip을 통과로 집계하지 않고 미실행은 `NOT_RUN(사유)`로 남긴다(D-25) | map `filterwarnings=error`(`be` §2.16) | — |
| BE-28 | 공통 패키지 자체 테스트: 단위 테스트는 stdlib+pytest, `[api]` 테스트는 starlette 0.4x/1.6 매트릭스, `[db]`·`[testing]`은 testcontainers(Linux CI만; Windows는 Tier 2라 제외, D-03) | — | T-302 |

## 8. 공통 패키지 구조와 모듈 우선순위

배포 이름 `kor-travel-common`, import 루트 `kortravelcommon`(일반 패키지, namespace 아님), 빌드 백엔드 hatchling, 경로 `packages/py/kor-travel-common`(D-15).

| extra | 의존 | 모듈 |
|---|---|---|
| (core, 기본) | stdlib + pydantic + pydantic-settings | `settings`, `time`, `errors`(베이스 예외만), `public_api_key`(해시·생성 함수) |
| `[api]` | fastapi, starlette, prometheus-client | `openapi`(export CLI), `health`, `request_id`, `metrics`, `problem`(핸들러), `security_headers`, `cors`, `trusted_proxy`, `envelope`(보류 C6 제외) |
| `[db]` | sqlalchemy(asyncpg/psycopg는 앱 선택) | `db` |
| `[dagster]` | dagster, dagster-postgres | `dagster` |
| `[testing]` | pytest, testcontainers | `testing` |
| `[http]` | httpx, tenacity | `http` |

geo·map은 import-linter로 라이브러리 계층의 `fastapi/starlette` import를 금지하므로 core는 stdlib+pydantic만 의존해야 한다(BE-9). 우선순위(D-15):

| 순위 | 모듈 | 선정 근거 | task |
|---|---|---|---|
| 1차 | C12 `openapi` export CLI(`--check`·profile 콜백·결정적 직렬화), C4 `health`(alias 옵션), C13 `time`, C20 `quality` 산출물 | 계약 무변경·근거 강함(export 4곳 동형, health 7곳, ruff 5곳; `be` §3 우선순위 제안) | T-303, T-304, T-305 |
| 2차 | C1 `settings`, C9 `db`, C7 `public_api_key`, C2 `request_id`(`trust_incoming`), C3 `metrics`(접두 인자) | 계약 일부 변경·근거 강함 | T-306, T-307 |
| 3차 | C5 `errors/problem`(opt-in, `exclude_paths`), C16 `security_headers`, C17 `cors`, C8 `trusted_proxy`, C11 `testing`, C10 alembic 템플릿, C15 `http`, C18 `dagster` | 정책 결정 동반 | T-308 |
| 보류 | C6 `pagination`(이름 충돌 `limit`/`page_size`·`has_more`/`next_cursor`), C14 `geo_primitives`(좌표 경계 상수 공통화 금지), C19 `cli.mutex`(geo·map 2곳), C21 백업 산출물 규약(문서만) | 근거 약함 또는 값 상이 | T-508 재평가 |

첫 소비자는 map-api·weather-api·airport(1차), geo(2차), pinvi·concierge·ktdm(3차, L8 후 breaking 묶음)이다(D-16). concierge·ktdm은 L8 전에는 규칙 문서 참조까지만 한다.

### 8.1 앱별 1차 채택 변경점

| 앱 | 교체 대상(현행) | 신규 도입 | task |
|---|---|---|---|
| map-api | `scripts/export_openapi.py`(profile 콜백 유지), `routers/public_status.py`, `dto/_time.py`, ruff·mypy 설정 | — | T-480 |
| weather-api | `scripts/export_openapi.py`(`--check` 추가), `/health`·`/version`, `KST` 고정 오프셋 → `ZoneInfo` | quality baseline | T-481 |
| airport | `scripts/export_openapi.py`, `/health`(DB 질의 → `/readyz`), `core/time_utils.py` | ruff·mypy 신규, `--check` CI, Docker `uv sync --locked` | T-482 |
| geo | `scripts/export_openapi.py`, `routers/healthz.py`(alias 병행), request-id | securitySchemes 선언 + typegen 재생성, admin problem+json opt-in | T-483 |
| pinvi | `middleware/request_id.py`, `core/time.py` | export 파이프라인·drift CI, `uv.lock` CI·Docker 소비, etl `@main` 제거 | T-484 |
| concierge | — | export·request-id·quality 전부 신규(CI 신설 T-451 선행) | T-485 |
| ktdm | `request_context.py`(`trust_incoming=False`) | quality baseline, uv 전환(T-471) | T-486 |

## 9. 배포·소비

| ID | 규칙 | 근거 |
|---|---|---|
| BE-29 | 배포 채널은 git 태그 + wheel 자산 병행이다. 소비자 선언: `kor-travel-common[api] @ git+https://github.com/digitie/kor-travel-common.git@py-vX.Y.Z#subdirectory=packages/py/kor-travel-common` 이고 `uv.lock`이 커밋 sha를 고정한다. GitHub Release 자산 `kor_travel_common-X.Y.Z-py3-none-any.whl` + `SHA256SUMS`를 URL 핀 대안으로 제공한다(Docker 빌드 스테이지에 `git`이 없을 때) | `be` §5.2 후보 A+D; D-11 |
| BE-30 | 태그 `py-vX.Y.Z`는 불변이고 같은 버전을 재발행하지 않는다. `@main`·브랜치 참조는 금지. 소비자 범위는 `~0.N`(0.x 동안 minor = 파괴 허용, `-rc.N` → 소비자 PR 검증 → 정식; D-31). CHANGELOG는 단일 파일에 패키지별 H3 | D-11·D-31; 절차는 [release](../runbooks/release.md) |
| BE-31 | 배포물에는 `LICENSE`·`NOTICE`·`THIRD_PARTY_NOTICES.md`를 동봉하고 `license = "GPL-3.0-or-later"`(PEP 639 `license-files`)를 선언한다 | [licensing](licensing.md) §6 |
| BE-32 | common 자체 CI `python-package` job: `uv build` → wheel 설치 → import 스모크 → starlette 매트릭스. npm/PyPI에는 게시하지 않음([ADR-014](../adr/014-common-implementation-without-registry-publishing.md)) | [ci-deploy](ci-deploy.md) §9 |

## 10. 공통화 금지 목록

다음은 common에 넣지 않는다(`be` §4). 소비자 한 곳에 있다는 이유만으로 공통화하지 않는다.

| 영역 | 이유(사실 근거) |
|---|---|
| geo: 주소 DTO·geocoder·GDAL loaders·GeoIP Korea-only 게이트·admission control·source registry·backup artifact·VWorld 호환 오류 형식 | GDAL 시스템 결합, ADR-037 정책, 외부 계약 |
| map: route policy matrix·`SurfaceScopedCORSMiddleware`·ServiceToken scope/digest·cache-target 프로토콜·alembic 300 baseline·ADR-090 런타임 권한 경계·provider fetcher/retry 예산 | 도메인 결합, 400행 `env.py` |
| pinvi: JWT/refresh/OAuth/RBAC(404 은닉)/rate-limit·geofence·cache-target sync·M05 계약 JSON·백업 셸 스크립트·서비스 영역 좌표 경계 | 감사·마이그레이션 이력 보유 |
| ktdm: docker/compose 오케스트레이션·runtime pin registry·`docker exec pg_dump`·SQLite 메트릭 DB·HMAC 서명 세션 쿠키·월간 로그 롤링 | 운영 도구 자체 |
| concierge: LLM 클라이언트·YouTube ETL·APScheduler 워커·MCP 서버·int ID keyset cursor | 도메인 |
| weather: sync provider 어댑터·Dagster 전용 multiprocess 메트릭 청소·자격증명 암호화 | 도메인 |
| airport: 주차 도메인·sqlite/PG 이중 방언·lifespan 스케줄러 | 도메인 |
| 서비스 간 클라이언트(pinvi `clients/kor_travel_*.py`, geo·map Dagster 클라이언트) | 선행 보고서 §7.2 facade 금지, map ADR-006 |
| 한국 좌표 경계 상수 | 세 앱의 값이 다르고 각각 근거 문서가 있다(geo 123–132/32–39 개구간, map 124–132/33–39.5, pinvi 124–132/33–43 + 39.5) |
| 비밀번호 해시·세션 저장소·CSRF | BE-22 |
| 기존 공유 라이브러리 재래핑(`python-*-api` 13종, `maplibre-vworld-*`, `python-kraddr-base`) | D-01·D-23; 라이선스 B2 |
| 백업 오케스트레이터 | 5개 구현이 각자 도메인 결합; 산출물 규약(파일명·sha256·manifest)만 문서(C21 보류) |

## 11. 예외 등록과 검증 gate

- 규약 예외(`BE-n`)는 [openapi-exceptions.yaml](openapi-exceptions.yaml)에 같은 형식으로 등록한다(초기: map `starlette<1.0` BE-3). 버전 값 예외(floor 미달·상한)는 `versions.json` `exceptions[]{repo,key,installed,reason,until,review}`가 정본이며 `tools/check_versions.py`가 판정한다(D-07). 둘 다 해당하면 양쪽에 같은 사유로 등록한다.
- 메트릭 접두 예외(map·pinvi)는 소비자 매니페스트 `exceptions[]`에 `review: 2026-12`로 두고 T-307에서 대시보드 영향을 평가한다(O-12).

| gate | 명령 | 실패 조건 |
|---|---|---|
| 3.11 문법 | 3.11 인터프리터 `python3 -m compileall packages/py/kor-travel-common/src` + 단위 테스트 | 3.12 전용 문법·API |
| import 계약 | `lint-imports`(common 자체 계약) | core가 fastapi/starlette import |
| starlette 매트릭스 | `uv run --with "starlette<1.0" pytest` / `--with "starlette>=1.6"` | 어느 쪽에서든 실패 |
| 패키지 | `uv build` → 임시 venv에 wheel 설치 → `python3 -c "import kortravelcommon"` | 빌드·설치·import 실패, LICENSE 동봉 누락 |
| 소비자 | 1차 소비자(map-api·weather-api·airport) CI green + OpenAPI 산출물 무변경 또는 pin 갱신 동반(M10) | drift, pin 미갱신 |
| 문서 | 이 문서·`templates/python/*` 변경은 2인 독립 리뷰(D-04 비면제) | — |

## 12. 열린 결정

| # | 항목 | 기본값 | 상태 |
|---|---|---|---|
| O-7 | 앱 Python floor 3.12 시점 | Phase 4 앱별; common 3.11 호환 | 열림(사용자 확인 필요) |
| O-12 | 메트릭 접두 map·pinvi | 기한부 예외(review 2026-12) | 열림(사용자 확인 필요) |
| O-14 | 429 코드명 등 | [openapi](openapi.md) §8 | 열림(사용자 확인 필요) |
| O-16 | provider SHA 정렬 주체 | 저장소 소유, common은 보고 | 열림(사용자 확인 필요) |
| — | `/metrics` 인증 방식 | Bearer 권장, 앱 예외 | 후보(`be` §7-12) |
| — | ruff 베이스 배포 방식(복사 vs 패키지 데이터) | 복사 + 머리 주석 버전 | 후보(T-305) |
| — | C2 첫 소비자(geo·map `log_format` 설정이 구현 예정인지 잔재인지) | pinvi 구현을 원형으로, geo·map은 설정 필드만 소비 | 후보(`be` §7-10) |

## 13. 근거

- [브리프](../plan/design-brief.md) D-01·D-06·D-07·D-11·D-15·D-16·D-22·D-25·D-31·O-7·O-12·O-16.
- [backend 횡단 비교](../survey/cross/backend.md) §2.1~§2.19(항목별 사실), §3(C1~C21), §4(금지 목록), §5(배포 후보), §6(선행 보고서 대조), §7(열린 질문).
- [openapi 횡단 비교](../survey/cross/openapi.md) §2.12(라이브러리 버전), §5(C1~C11 코드 후보), Q7·Q9·Q11.
- [version-matrix 횡단 비교](../survey/cross/version-matrix.md) §2(백엔드 매트릭스), §3.4, §7.2·§7.3(핀 정책·`blocked`).
- [ci-deploy 횡단 비교](../survey/cross/ci-deploy.md) §1.4(pre-commit), §1.11(env 접두 집계), §2.1(`python-quality.yml`), §3.2(env 접두 표준).
- [공통화 매트릭스](../survey/commonality-matrix.md) §1.4·§2.4·§4.2 D12~D19·D23·D38.
