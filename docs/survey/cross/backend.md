# 횡단 비교 — Python 백엔드 공통 코드 후보 비교

- 작성일: 2026-09-06
- 성격: 읽기 전용 조사 결과. 코드 이동·패키지 발행·정책 확정을 뜻하지 않는다.
- 범위: kor-travel-airport(kta) · kor-travel-concierge(ktc) · kor-travel-docker-manager(ktdm) · kor-travel-geo(geo) · kor-travel-map(map) · kor-travel-weather(ktw) · PinVi(pinvi apps/api, apps/etl)의 Python 코드.
- 표기 규약: **사실** = 조사 커밋의 파일에서 직접 확인. **후보** = 사실을 근거로 한 공통화 제안. **추정** = 근거가 간접적이거나 실행 검증을 하지 않음. **미확인** = 확인하지 못함.
- 약어: 각 저장소 상대 경로는 `kta:`, `ktc:`, `ktdm:`, `geo:`, `map:`, `ktw:`, `pinvi:` 접두로 적는다.

## 0. 기준 (조사 커밋)

| 약어 | 저장소 | 로컬 체크아웃 | 커밋 | Python 패키지 위치 |
|---|---|---|---|---|
| kta | kor-travel-airport | `F:/dev/kor-travel-common-survey/kta-main` | `2bb1111` | `backend/` (`app` 패키지) |
| ktc | kor-travel-concierge | `F:/dev/kor-travel-concierge` | `7945305` | `backend/ktc`, `etl/`, `mcp/`, `scheduler/` |
| ktdm | kor-travel-docker-manager | `F:/dev/kor-travel-common-survey/ktdm-main` | `862562d` | `backend/src/kor_travel_docker_manager` |
| geo | kor-travel-geo | `F:/dev/kor-travel-geo-fixes` | `1d9d74d` | `src/kortravelgeo`, `kor-travel-geo-dagster/` |
| map | kor-travel-map | `F:/dev/kor-travel-common-survey/ktm-main` | `c494e227` | `src/kortravelmap`, `packages/kor-travel-map-api`, `packages/kor-travel-map-dagster` |
| ktw | kor-travel-weather | `F:/dev/kor-travel-weather` | `6003da9` | `src/kortravelweather`, `packages/kor-travel-weather-api`, `packages/kor-travel-weather-dagster`, `packages/python-airkorea-api` |
| pinvi | pinvi | `F:/dev/kor-travel-common-survey/pinvi` | `9af25e5` | `apps/api/app`, `apps/etl/pinvi` |

선행 보고서 `F:/dev/kor-travel-geo-fixes/docs/kor-travel-common-library-review.md`(2026-09-05)의 geo 기준 커밋은 `daf079b`이고 본 조사의 geo 커밋 `1d9d74d`는 그 이후다. pinvi 기준 커밋도 선행 보고서(`2396d65`)와 다르다(`9af25e5`).

## 1. 방법

실행한 읽기 명령(조사 대상 저장소에는 어떤 파일도 만들지 않았다):

- 빌드/설정 파일 목록: 각 저장소에서 `git ls-files | grep -E '(pyproject\.toml|requirements.*\.txt|uv\.lock|alembic\.ini|conftest\.py|\.pre-commit-config\.yaml|\.github/workflows/.*\.ya?ml|Dockerfile.*)'`.
- 패턴 탐색: `git grep -n -E` 로 `BaseSettings|env_prefix`, `structlog|basicConfig|dictConfig`, `prometheus_client|CollectorRegistry|generate_latest`, `"/health|/readyz|/healthz`, `create_async_engine|create_engine\(|pool_size|pool_pre_ping`, `CORSMiddleware|X-Content-Type-Options|Strict-Transport-Security`, `^class \w+(Error|Exception)\(`, `tenacity|AsyncRetrying|httpx\.AsyncClient\(`, `argon2|pbkdf2|CryptContext|ServiceToken|set_cookie\(|samesite`, `pg_dump|pg_restore`, `^@(op|job|asset|schedule|sensor|run_failure_sensor|resource)\b`, `python-[a-z-]+-api @ (git\+https|https)`.
- 파일 열람: `sed -n` 범위 읽기로 아래 §8 근거 파일을 확인했다.
- 설치 버전: `uv.lock` 이 있는 kta·ktw·pinvi(api)에서 `name = "..."` / `version = "..."` 쌍을 읽었다. lockfile이 없는 geo·map·ktdm·ktc는 선언 범위만 적는다.
- 이력: `git log --oneline -- <path>` 로 geo 메트릭 접두 변경 커밋과 ktc 최근 커밋을 확인했다.

실행하지 않은 것: 테스트·빌드·설치·Docker 빌드. 따라서 "동작한다/호환된다"는 판단은 모두 추정이다.

## 2. 비교표

유사도 표기: **동일**(함수/구조가 사실상 복제), **유사**(같은 목적·다른 세부), **상이**(목적은 같으나 설계가 다름), **없음**.

### 2.1 빌드 시스템 · Python 버전 · lockfile

| 항목 | kta | ktc | ktdm | geo | map | ktw | pinvi |
|---|---|---|---|---|---|---|---|
| 빌드 백엔드 | setuptools (`backend/pyproject.toml`) | 없음. `requirements.txt` 4종(`etl/mcp/scheduler`가 `-r ../backend/requirements.txt` 포함) | poetry-core (`backend/pyproject.toml`) | setuptools ×2 (루트, `kor-travel-geo-dagster/`) | setuptools ×3 (루트, api, dagster; `kortravelmap.*` namespace) | setuptools ×4 (루트, api, dagster, `python-airkorea-api`) | hatchling ×2 (`apps/api`, `apps/etl`) |
| `requires-python` | `>=3.12` | 없음(Docker `python:3.11-slim`) | `^3.11` | `>=3.12` | `>=3.11` | `>=3.11` | `>=3.12` |
| CI Python | 3.12 (`uv sync --locked`) | CI 없음(`.github` 없음) | 3.11 (`pip install -e ./backend` + `ruff==0.16.4 httpx==0.28.1 pytest==9.1.1`) | 3.12 (`pip install -e ".[api,loaders,dev]"`) | 3.11/3.12/3.13 matrix (`pip install -e`) | 3.12 (`uv sync --locked`) | 3.12 (`pip install -e ".[dev]"`) |
| Docker Python | `python:3.12-slim`, `pip install -e ".[dev]"` | `python:3.11-slim`, `pip install -r` ×4 | 미확인(compose에 backend 이미지 정의 없음; 호스트 실행 추정) | `python:3.12-trixie`(api), `python:3.12-slim`(dagster), `pip install -e`/`--prefix` | `python@sha256:57cd…` digest 핀, `pip install --prefix=/install` | `uv:0.11.21` + `python:3.13-slim`, `uv sync --locked --no-dev` | `python:3.12-slim@sha256:7a8b…`, `pip install -e .` |
| lockfile | `backend/uv.lock` | 없음 | 없음(poetry.lock 미커밋) | 없음 | 없음 | `uv.lock`(루트) | `apps/api/uv.lock` |
| 설치기 일치성 | CI는 uv, Docker는 pip(lock 미사용) | pip | pip | pip | pip | uv 일관 | CI/Docker pip(lock 미사용) |
| 라이선스 선언 | 없음(미확인) | (루트 LICENSE MIT, 선행 보고서) | (MIT, 선행 보고서) | `GPL-3.0-only` | `GPL-3.0-or-later` | `GPL-3.0-or-later` | `MIT` |

사실(설치 버전, lockfile 기준): fastapi `0.141.1`(kta·ktw·pinvi), sqlalchemy `2.0.52`(3곳 동일), pydantic-settings `2.15.0`(3곳 동일), pydantic `2.13.4/2.13.5`, httpx `0.28.1`, alembic `1.19.1`, starlette `1.6.0`, uvicorn `0.52.3/0.52.4`, prometheus-client `0.26.0`(ktw·pinvi), structlog `26.1.0`(pinvi), tenacity `9.1.4`(pinvi), pytest `9.1.1`, ruff `0.16.3/0.16.5`, mypy `2.3.1`.

버전 일치화 관점의 충돌(사실):

- `map:packages/kor-travel-map-api/pyproject.toml` 은 `starlette>=0.40,<1.0` 을 명시하며 주석에 "starlette 1.0+ TestClient은 httpx 2.x를 요구"라 적었다. 반면 kta·ktw·pinvi lockfile은 starlette `1.6.0` + httpx `0.28.1` 조합이다. 공통 패키지가 fastapi/starlette 범위를 정하면 map의 상한과 먼저 충돌한다.
- `ktdm:backend/pyproject.toml` 은 `fastapi = "^0.110.0"`, `uvicorn = "^0.28.0"` (poetry caret = `>=0.110,<0.111`). 추정: ktdm은 fastapi 0.110 계열에 고정돼 있어 다른 앱(0.141)과 두 minor 세대 차이가 난다. lockfile이 없어 실제 설치 버전은 미확인.
- geo `cli/main.py:92` 는 PEP 695 문법(`def _run_with_cli_lock[T](...)`)을 쓴다(사실). geo는 3.11로 내릴 수 없고, map·ktw·ktdm은 3.11 floor다. 공통 패키지는 3.11 호환 문법으로 써야 하거나(후보) 세 앱의 floor를 3.12로 올려야 한다(정책 결정 필요).
- `ktc:backend/requirements.txt` 는 상한 없는 `>=` 만 쓰고 `mcp<2` 를 최근 긴급 고정했다(커밋 `7945305`). lockfile이 없어 재현 빌드가 되지 않는다.

### 2.2 설정 (pydantic-settings)

| 항목 | kta | ktc | ktdm | geo | map | ktw | pinvi |
|---|---|---|---|---|---|---|---|
| 파일 | `backend/app/core/config.py` | `backend/ktc/core/config.py:68-` | `main.py:47-51`(`load_dotenv`), `services/auth_service.py`(`os.environ`) | `src/kortravelgeo/settings.py:29-37` | `src/kortravelmap/settings.py:34-51`, `packages/kor-travel-map-api/src/kortravelmap/api/settings.py:342-357` | `src/kortravelweather/settings.py:55-67` | `apps/api/app/core/config.py:609-616` |
| 클래스 | `Settings` | `Settings` | 없음(pydantic-settings 선언만, 미사용) | `Settings` | `KorTravelMapSettings` + `ApiSettings` | `WeatherSettings` | `Settings` |
| `env_prefix` | 없음 | 없음(필드명이 대문자 env 이름) | `KTDM_*` 수동 | `KTG_` | `KOR_TRAVEL_MAP_` / `KOR_TRAVEL_MAP_API_` | `KOR_TRAVEL_WEATHER_` | 없음(필드가 `pinvi_*`) |
| `.env` 로딩 | `.env` | `.env`, `case_sensitive=True` | `get_env_path()` 루트 `.env` | `.env`, `frozen=True` | `.env` | `(ROOT/.env, .env)` 튜플 | `.env` |
| `extra` | ignore | ignore | — | ignore | ignore | ignore | ignore |
| 비밀 처리 | 평문 str | 평문 str(`mask_secret` 헬퍼) | 평문 env | `SecretStr` | `SecretStr` + `hide_input_in_errors` | `SecretStr` + `AliasChoices` 레거시 이름 | `hide_input_in_errors` + `__init__`에서 ValidationError input 재작성(`<redacted>`) |
| 접근자 | `@lru_cache get_settings()` | `@lru_cache get_settings()` | — | 모듈 싱글턴 `get_settings()`/`set_settings()` | 없음(호출마다 `KorTravelMapSettings()`) | `@lru_cache(maxsize=1)` | `@lru_cache` + 모듈 전역 `settings`(`config.py:2532`) |
| fail-closed 프로파일 | 없음 | `APP_ENV` local 우회 | 없음 | 없음 | `ApiSettings.profile` production 검증 | `environment` 기본 `production`, `require_admin_token()` | `pinvi_environment` |
| 유사도 | 유사 | 유사 | 상이 | 유사 | 유사 | 유사 | 유사 |

관찰: 7개 중 6개가 `BaseSettings` + `.env` + `extra="ignore"` 라는 같은 골격이다(사실). 접두·비밀 처리·접근자만 다르다. ktc는 `NEXT_PUBLIC_*` 프런트 변수까지 같은 클래스에 두고 있다(`config.py:82-84`). pinvi `config.py` 는 2,500행이 넘고 M05 계약 상수를 포함한다(사실: `get_settings` 가 2527행).

### 2.3 로깅

| 항목 | kta | ktc | ktdm | geo | map | ktw | pinvi |
|---|---|---|---|---|---|---|---|
| 프레임워크 | stdlib | stdlib | stdlib + 자체 `MonthlyRotatingFileHandler` | stdlib | stdlib | stdlib | structlog(JSON) + stdlib 브리지 |
| 설정 함수 | 없음 | 없음(`core/logging.py` 는 `mask_secret` 만) | `main.py:_configure_logging`(root 핸들러 1회 부착) | 없음 | 없음 | 없음 | `core/logging.py:configure_logging` |
| structlog 의존 | 없음 | 없음 | 없음 | 선언(`structlog>=24.4`) but `src` import 0건(사실) | 없음(설정 필드 설명에 "structlog 로깅 레벨"이라 적혀 있으나 import 0건) | 없음 | 사용 |
| `log_format json/console` 설정 | 없음 | 없음 | 없음 | 있음(`settings.py:101-102`), 소비처 0건(사실) | 있음(`settings.py:532-542`), 소비처 0건 | 없음 | 없음(항상 JSON) |
| 요청 ID | 없음 | 없음 | `X-Request-ID` 서버 발급(클라이언트 값 무시), contextvars + `RequestIdLogFilter` | admin 경로만 `x-request-id`/`traceparent` 읽어 `RequestContext` 에 보관(`api/security.py:174-175`); 전역 미들웨어 없음 | `attach_request_id` 미들웨어, ContextVar 바인딩, 응답 `X-Request-ID` (`api/app.py:1071-1083`); 클라이언트 헤더 수용 여부 미확인 | `x-request-id` 수용 또는 uuid4, 응답 `x-request-id`+`x-duration-ms` (`api/app.py:100-124`) | `X-Request-Id` 수용 또는 uuid4, structlog contextvars 바인딩 |
| 요청 로깅 | 없음 | 메트릭만 | 없음 | 느린 요청 로거 `kortravelgeo.api.performance`(설정 opt-in) | opt-in `ops.api_call_log` 기록 | 메트릭만 | httpx 이벤트 훅으로 외부 호출 로그(민감 쿼리 키 마스킹) |
| 유사도 | 없음 | 없음 | 상이 | 상이 | 상이 | 유사(ktw↔pinvi 요청 ID) | 상이 |

관찰: 실제 구조화 로깅을 구현한 곳은 pinvi 하나다(사실). geo·map은 설정 필드만 있고 구현이 없어 "수요는 있으나 미구현" 상태로 읽힌다(추정). 요청 ID 정책이 셋으로 갈린다: 서버 발급 강제(ktdm, 스푸핑 방지 근거를 주석에 명시), 클라이언트 수용(ktw·pinvi), 없음(kta·ktc).

### 2.4 메트릭 (prometheus-client)

| 항목 | kta | ktc | ktdm | geo | map | ktw | pinvi |
|---|---|---|---|---|---|---|---|
| 파일 | 없음 | `backend/ktc/telemetry.py`, `backend/main.py:70-118` | `services/metrics_collector.py:643-`(수작업 텍스트 노출, prometheus_client 미사용) | `src/kortravelgeo/infra/metrics.py` | `packages/kor-travel-map-api/src/kortravelmap/api/prometheus.py` | `src/kortravelweather/metrics.py` | `apps/api/app/middleware/prometheus.py` |
| 이름 접두 | — | `ktc_` | `ktdm_` | `ktg_` (커밋 `daf079b` T-305 #545에서 `kor_travel_geo_` → `ktg_`) | `kor_travel_map_` | `ktw_` | `pinvi_api_` |
| 레지스트리 | — | 기본 `REGISTRY`; PROCESS/PLATFORM/GC 수집기 해제 후 `ProcessCollector(namespace="ktc")` 재등록 | 자체 | 기본 `REGISTRY`; prometheus_client 없으면 `_NoopMetric` | 앱별 `CollectorRegistry(auto_describe=True)` + GC/Platform/Process | scrape/instrumentation 이중 레지스트리 + `PROMETHEUS_MULTIPROC_DIR` 전용 수집기(죽은 gauge 파일 청소, 시그널 훅) | 기본 `REGISTRY`; `PROMETHEUS_MULTIPROC_DIR` 시 `MultiProcessCollector` |
| HTTP 카운터 | — | `ktc_http_requests{method,path,status}` (`_total` 없음) | 없음 | `ktg_api_requests_total{method,route,status_code}` | `kor_travel_map_http_requests_total{method,path,surface,status_code}` | `ktw_http_requests_total{method,route,status_class}` | `pinvi_api_http_requests_total{method,route,status_code}` |
| 히스토그램 버킷 | — | 기본 | — | 0.005…10.0 (11) | 0.005…10.0 + 0.075 (12) | 0.005…30.0 (12) | 0.005…10.0 (11, geo와 동일) |
| 미매칭 경로 라벨 | — | `/unmatched` | — | `/<unmatched>` | `__unmatched__` | 허용 목록 밖은 `other` | `__unmatched__` |
| 라벨 정규화 | — | `label_value()` 정규식 | — | route template | route template + `surface` ContextVar | provider/route 허용 목록 | route template |
| DB 메트릭 | — | 작업 상태 gauge(DB 집계) | — | SQLAlchemy 이벤트 쿼리 카운트/지연 + pool gauge + pg_stat_statements | SQLAlchemy 이벤트 쿼리 카운트/지연(`api/db.py`) | 없음 | pool gauge(scrape 직전 갱신) |
| `/metrics` 보호 | — | CIDR 허용 + 키(`require_prometheus_access`) | `KTDM_METRICS_REQUIRE_KEY` opt-in 키 | GeoIP open path | Bearer 토큰(production 필수) | Bearer/`x-metrics-token`(production 필수) | 비활성 시 404; 인증 미확인 |
| 유사도 | 없음 | 유사 | 상이 | 유사 | 유사 | 유사 | 유사 |

관찰(사실): 5개 구현이 같은 세 지표(요청 수·지연·진행 중)를 만들지만 이름 접두 6종, 경로 라벨 이름 2종(`path`/`route`), 상태 라벨 3종(`status`/`status_code`/`status_class`), 미매칭 센티널 4종이다. ktc `telemetry.py:24-27` 주석은 "kor-travel 계열의 서비스별 네임스페이스 규약(concierge=ktc_, docker-manager=ktdm_)"을 언급한다. 즉 접두 규약이 암묵적으로 존재하나 map(`kor_travel_map_`)과 pinvi(`pinvi_api_`)는 그 규약 밖이다.

### 2.5 health / ready

| 앱 | 경로 | 내용 | 파일 |
|---|---|---|---|
| kta | `/health` | DB `count(*)` 실행 + `release_sha` (DB 의존) | `backend/app/main.py:238-246` |
| ktc | `/health`, `/` | 정적 `{"status":"ok"}` | `backend/main.py:98-100` |
| ktdm | `/health` | 정적 `{"status":"healthy","service":...}` | `main.py:359-361` |
| geo | `/healthz`, `/readyz` | liveness 정적; readiness는 DB 프로브(타임아웃) + pool 이용률(0.8 degraded/saturated) + admission → 503, DTO `ReadinessResponse` | `api/routers/healthz.py`, `dto/health.py` |
| map | `/health`, `/version` | liveness 정적(envelope `data/meta`); `/version` 은 `KOR_TRAVEL_MAP_GIT_COMMIT` | `api/routers/public_status.py:61-105` |
| ktw | `/health`, `/version` | `{status, service, version}`; `git_commit` | `api/app.py:153-164` |
| pinvi | `/health`, `/health/db`, 도메인 health 2종 | `HealthResponse(status, service, version, git_sha)`; `/health/db` 는 `SELECT 1` + latency_ms | `api/v1/healthz.py:31-53`, `schemas/health.py` |

유사도: liveness는 7곳 **유사**, deep readiness는 geo 하나만 **있음**. 경로 이름이 `/health`(6) vs `/healthz`(1)로 갈린다. 다른 서비스를 프로브하는 코드(pinvi `admin/system.py:104-111` 이 `/health`, `/health/live` 를 호출, ktc `RUSTFS_HEALTH_PATH`)가 있어 경로 통일은 소비자 측 변경도 동반한다.

### 2.6 DB 엔진 · 세션

| 항목 | kta | ktc | ktdm | geo | map | ktw | pinvi |
|---|---|---|---|---|---|---|---|
| 드라이버 | asyncpg (+ aiosqlite 이중 방언) | asyncpg (scheduler는 psycopg sync jobstore) | SQLite sync(`pinvi_metrics.db` 파일명, 레거시) | psycopg3 async (`postgresql+psycopg`) | asyncpg 강제(`normalize_async_dsn`) | psycopg3 **sync** (`create_engine`) | asyncpg |
| 팩토리 | `create_engine_and_session_factory(url)` | 모듈 import 시 전역 `engine` 생성 | 모듈 전역 `engine` | `make_async_engine(settings)` | `make_async_engine(dsn, pool_size=5, max_overflow=10, server_settings)` + `make_async_session_factory` | `WeatherRepository(database_url)` 안에서 생성 | 모듈 전역 `engine` |
| pool | 5/5, `pool_recycle=1800`, 테스트 시 `NullPool` | 기본값, `pool_pre_ping` | — | 10/5, `pool_timeout=1s`, `pool_recycle=3600`, `AsyncAdaptedQueuePool` | 5/10 | 10/10, `pool_timeout=15` | `pool_size` 설정(기본 10) |
| 세션 GUC | sqlite PRAGMA | 없음 | PRAGMA busy_timeout/WAL | `options=-c statement_timeout=... -c search_path=public,x_extension`, `prepare_threshold` | `server_settings={"jit":"off"}`(API만) | 없음 | `server_settings` lock_timeout 30s / idle_in_tx 60s / statement 600s |
| JSON 직렬화 | 기본 | 기본 | — | orjson | 기본 | 기본 | 기본 |
| DSN 정규화 | `postgres://`→`+asyncpg` | 없음 | — | `Settings.normalize_pg_dsn` | `normalize_async_dsn` | `postgresql://`→`+psycopg` | 없음 |
| 세션 의존성 | `get_db` (app.state) | `get_session`, `get_repeatable_read_session` | `get_db_session` contextmanager | `AsyncAddressClient.engine` (app.state.client) | `get_session` (lazy 모듈 싱글턴, `set_engine_for_test`) | repository 내부 | `get_db` (모듈 속성 동적 참조로 monkeypatch 허용) |
| 엔진 메트릭 훅 | 없음 | 없음 | 없음 | `install_db_query_metrics` | `_instrument_engine_if_needed` | 없음 | pool gauge만 |
| 기동 시 스키마 검사 | Alembic head 상수 비교(`ALEMBIC_HEAD`) | local env만 `create_all` | `create_all` | 없음 | `assert_runtime_db_privilege_boundary`(ADR-090) | 비production `create_schema` | M05 anchor 검증 |
| 유사도 | 유사 | 유사 | 상이 | 유사 | 유사 | 상이(sync) | 유사 |

관찰: "DSN 정규화 → `create_async_engine(pool, pre_ping, server_settings/options)` → `async_sessionmaker(expire_on_commit=False)`" 골격은 asyncpg 4곳(kta·ktc·map·pinvi)에서 동일하다(사실). 드라이버가 셋(asyncpg / psycopg async / psycopg sync)으로 갈려 있어 `server_settings`(asyncpg) vs `options`(psycopg) 인자 차이를 헬퍼가 흡수해야 한다.

### 2.7 Alembic

| 항목 | kta | ktc | ktdm | geo | map | ktw | pinvi |
|---|---|---|---|---|---|---|---|
| `alembic.ini` | `backend/alembic.ini` | 루트(`script_location = backend/alembic`, `timezone = UTC`) | 없음(create_all) | 루트 | 루트(`post_write_hooks` ruff format/check) | 루트(`%(here)s/alembic`) | `apps/api/alembic.ini` (`file_template = %Y%m%d_%H%M_slug`) |
| `env.py` 실행 방식 | async `async_engine_from_config` + `NullPool` | async(동일 구조) | — | **sync** `engine_from_config`, `connect_args search_path=public,x_extension`, `target_metadata=None`(raw SQL) | async + 300 baseline handoff 가드·`SET ROLE`·`include_object` 제외·`on_version_apply` 봉인 | sync `engine_from_config`, URL `%`→`%%` 이스케이프 | async `create_async_engine` + 자문 락 `pg_advisory_xact_lock(1863432274, 20260824)` + `CREATE SCHEMA app/x_extension` + 명시 `commit()` |
| 스키마 분리 | public | public(`include_schemas=False`) | — | `search_path=public,x_extension` | `include_schemas=True`, feature/provider_sync/ops/x_extension | public | `version_table_schema="app"`, `include_schemas=True` |
| autogenerate 비교 | 기본 | 기본 | — | 없음 | `compare_type`, `compare_server_default` | 기본 | `compare_type`, `compare_server_default` |
| 리비전 명명 | `0001_initial` … `0003_…` (3) | `20260610_0001_slug` … (29) | — | `0001_text_…`, `0007_t042_…` (26) | `300_schema_baseline` … `303` (+ legacy 0001–0104, retired 0200–0236) | `0001_slug` … (8) | `20260824_0100_…`, `0101` (2) |
| 적용 이력 불변 정책 | — | — | — | — | baseline 봉인 | — | `ruff exclude alembic/versions`(byte 불변) |
| CI | `alembic upgrade head` + `alembic check` | 없음 | — | 없음 | integration 테스트 경유 | `alembic upgrade head` | integration + `alembic upgrade head`(subprocess) |
| 유사도 | 동일(kta≈ktc≈pinvi 골격) | 동일 | 없음 | 상이 | 상이 | 유사 | 유사 |

관찰: kta·ktc `env.py` 는 함수 이름·구조까지 거의 같다(사실: 두 파일 모두 `run_migrations_offline / do_run_migrations / run_async_migrations`). map `env.py` 는 300 baseline 이관 가드 때문에 400행이 넘고 도메인 결합이 강하다. 명명 규약은 4종(순번, 날짜+순번, 순번+태스크, baseline 번호대)이다.

### 2.8 인증 · 세션

| 항목 | kta | ktc | ktdm | geo | map | ktw | pinvi |
|---|---|---|---|---|---|---|---|
| 사용자 비밀번호 | 없음 | 없음(로그인은 Next.js) | pbkdf2_sha256 310k, env `KTDM_ADMIN_PASSWORD_HASH` | 없음 | 없음 | 없음 | argon2id(passlib `CryptContext`) |
| 세션/토큰 | 없음 | 없음 | HMAC 서명 쿠키 `ktdm_admin_session`(samesite=strict, 8h) + SQLite 세션 행 | 없음 | 없음(BFF) | 서버는 revocation/rate-limit 저장소만 제공(`/v1/admin/session-revocations/*`, `/v1/admin/login-rate-limit/*`) | JWT HS256 access(10분, `token_version`) + 불투명 refresh(SHA-256 저장), 쿠키 `pinvi_access/refresh`(samesite=lax), 모바일 Bearer, MCP JWT |
| admin 프록시 신뢰 | 없음 | `X-KTC-Actor` + `X-KTC-Admin-Proxy-Secret` + `KTC_ADMIN_TRUSTED_PROXY_CIDRS` | `x-ktdm-proxy-secret` + `KTDM_TRUSTED_PROXY_CIDRS` | `x-ktg-actor` + `x-ktg-roles` + `x-ktg-admin-proxy-secret` + trusted CIDR | `X-Kor-Travel-Map-Actor` + `X-Kor-Travel-Map-Admin-Proxy-Secret` + peer CIDR | `x-admin-token` 정적 토큰 | 없음(자체 JWT) |
| 역할 | 없음 | scope `read/admin` | 단일 admin | `source_file_viewer/manager, rebuild_operator, destructive_admin, scheduler, system` | route policy(`RoutePolicy` enum) + ServiceToken scope | 단일 admin | `user/admin/operator/cpo`, 거부 시 404 |
| 공개 API 키 | 없음 | `?key=`/`X-API-Key`, DB `PublicApiKey`, 32자 영숫자, SHA-256, scope | `?key=`, SQLite `PublicApiKey`, 32자, SHA-256 | `?key=`/`X-KTG-API-Key`, `ops.public_api_keys`, 32자, SHA-256 | `X-Kor-Travel-Map-Api-Key`, `ops.public_api_keys`, 32자, SHA-256, TTL 캐시 | 없음 | 없음 |
| 서비스 간 토큰 | 없음 | 없음 | 없음 | 없음(Dagster는 proxy secret+roles로 admin API 호출) | `X-Kor-Travel-Map-Service-Token` 상수시간 비교, 용도별 digest 5종 | 없음 | map ServiceToken 소비자 |
| 로그인 감사/속도 제한 | 없음 | `login_events`(상한 5000행) | 감사 테이블 기반 5회/10분 | `ops.admin_auth_events`(테스트 존재) | `ops.admin_auth_events` 라우터 | PG 테이블 0005/0008 | rate-limit 미들웨어(memory/postgres 백엔드) |
| 유사도 | 없음 | 유사(공개키·프록시) | 유사(공개키·프록시) | 유사(공개키·프록시) | 유사(공개키·프록시) | 상이 | 상이 |

사실: `generate_public_api_key()`(32자 `ascii_letters+digits`, `secrets.choice`) 와 `hash_public_api_key()`(`strip()` 후 무염 SHA-256) 는 ktc·ktdm·geo·map 네 곳에서 본문이 같고, 주석("32자 CSPRNG 토큰(~190비트)이라 … 느린 KDF 불필요")까지 ktc와 ktdm이 같다. `key_hint = api_key[-6:]`, 상태 `active/revoked` 도 공통이다. 저장소만 ORM(ktc), SQLite ORM(ktdm), raw SQL `ops.public_api_keys`(geo·map)로 다르다.

사실: "프록시 비밀 헤더 + actor 헤더 + 신뢰 CIDR" 패턴이 ktc·ktdm·geo·map에 있으나 헤더 이름은 넷 다 다르다. 비밀번호 해시(pbkdf2 vs argon2)와 세션 방식(서명 쿠키 vs JWT)은 두 앱만 가지고 있고 서로 다르다. 선행 보고서 §3.6의 "로그인·세션·권한·CSRF는 첫 범위에서 제외" 판단과 부합한다.

### 2.9 CORS · 보안 헤더

| 앱 | CORS | 보안 헤더 | 파일 |
|---|---|---|---|
| kta | `CORSMiddleware`(csv 파싱, credentials=False, GET/POST/OPTIONS) + `TrustedHostMiddleware` | 인라인 미들웨어: nosniff, `X-Frame-Options: DENY`, Referrer-Policy, Permissions-Policy, HSTS는 `x-forwarded-proto == https` 일 때 | `backend/app/main.py:199-218` |
| ktc | `CORSMiddleware`(credentials=True, `*` 제거) | 없음 | `backend/main.py:61-67`, `config.py:389-400` |
| ktdm | `CORSMiddleware`(credentials=True, `expose_headers=[X-Request-ID]`) + 로그인 Origin 검사 | 없음 | `main.py:213-251` |
| geo | 백엔드 `CORSMiddleware` 사용 0건(사실). `api_cors_origins` 설정의 소비처 미확인 | 없음(grep 0건) | `settings.py:53` |
| map | `SurfaceScopedCORSMiddleware`: public 표면만, credentials 없음, route별 exact method | 없음(grep 0건) | `api/cors.py` |
| ktw | `CORSMiddleware`(credentials=False) | `/metrics` 오류 응답에만 nosniff | `api/app.py:95-101` |
| pinvi | `CORSMiddleware`(credentials=True, `expose_headers=[Retry-After]`) | `SecurityHeadersMiddleware`: nosniff, Referrer-Policy, `Permissions-Policy: geolocation=(self)`, DENY, CSP `default-src 'none'`, HSTS는 실제 scheme https 또는 production일 때만(`X-Forwarded-Proto` 불신, #344) | `middleware/security_headers.py` |

관찰: ktc `cors_allow_origins` 와 ktdm `_resolve_cors_allow_origins` 는 "csv 분리 후 `*` 제거(credentials와 와일드카드 동시 사용 방지)" 로직이 같다(사실). HSTS 발급 조건은 kta(전달 헤더 신뢰)와 pinvi(불신)가 정반대다 — 공통화 시 정책 결정이 먼저다.

### 2.10 에러 계층 · 응답 형식

| 앱 | 기반 예외 | 속성 | HTTP 응답 형식 | 파일 |
|---|---|---|---|---|
| kta | 없음(`FlightStatusUpstreamError(RuntimeError)` 단발) | — | RFC 7807 `application/problem+json` (`title/status/detail/instance`) | `backend/app/main.py:160-196` |
| ktc | 없음(모듈별 `*Error(RuntimeError/ValueError)` 30여 개) | — | FastAPI 기본 `{"detail": ...}` (사용자 정의 핸들러 미확인) | `backend/ktc/services/place_service.py` 등 |
| ktdm | `DeploymentContractError(ValueError)` 계층, `code` 클래스 속성 | `code` | 409 `{"detail", "request_id"}`; HTTPException detail dict `{code,message}` | `services/errors.py`, `main.py:350-356` |
| geo | `KorTravelGeoError(Exception)` | `code`(E0xxx), `http_status`, `hint` | 경로별 3종: VWorld 호환, v2 `{status, query_id, error:{code,message,hint,field}}`, legacy `{response:{status,errorCode,errorMessage}}` | `exceptions.py`, `api/responses.py` |
| map | `KorTravelMapError(Exception)` | 없음(매핑표는 docstring) | RFC 7807 `ProblemDetail` + `code` + `request_id`; 성공은 `{data, meta{duration_ms,request_id,page,cluster}}` | `core/exceptions.py`, `api/response.py` |
| ktw | `ProviderError(RuntimeError)` | `code`, `retryable`, `status_code` | RFC 7807 유사 `Problem{type,title,status,detail,code,request_id,errors}`; 성공 `Envelope{data, meta{request_id,generated_at,duration_ms,page}}` | `providers/base.py:25-35`, `api/response.py` |
| pinvi | 서비스별 베이스(`BackupServiceError` 등), `code` 클래스 속성 | `code` | `{"error":{"code","message","details"}}`, 상태→코드표(`TOKEN_INVALID`, `RESOURCE_NOT_FOUND`, `VERSION_CONFLICT`…) | `core/errors.py` |

관찰: 응답 형식이 최소 4계열이다(RFC 7807: kta·map·ktw / `{error:{}}`: pinvi / geo 3종 / ktdm `{detail:{}}`). map과 ktw의 `Meta`/`Problem` 은 필드 구성이 유사하며 ktw `settings.py` docstring이 "원본 kor-travel-map" 이라 밝힌다(사실). 예외 베이스에 `code`+`http_status`+`hint` 를 모두 가진 곳은 geo뿐이다. 이름 충돌 주의: pinvi `clients/kor_travel_geo.py:29` 의 `KorTravelGeoError` 와 geo `exceptions.py:6` 의 `KorTravelGeoError` 는 서로 다른 클래스다.

### 2.11 retry · httpx 클라이언트

| 앱 | retry | httpx 구성 | 파일 |
|---|---|---|---|
| kta | provider 라이브러리 위임(미확인) | 스크립트에서 `AsyncClient(timeout=settings.api_timeout_seconds)` | `scripts/migrate_http_history.py:159` |
| ktc | 없음 | 호출마다 `AsyncClient(timeout=10/30)`; `requests` 도 의존 | `api/routes.py:445,1005`, `etl/*` |
| ktdm | 없음(httpx 미사용) | — | — |
| geo | **tenacity** `AsyncRetrying(stop_after_attempt(3), wait_exponential(0.2→2.0), retry_if_exception_type(Timeout/Transport/HTTPStatus))` | 주입 가능한 `http_client`, 기본 `AsyncClient(timeout=5.0)`; RustFS는 `httpx.Timeout(60, connect=10, read=None, pool=10)` | `infra/external_api.py:113-148`, `infra/rustfs.py:203` |
| map | 없음(Dagster `upstream_retry.py` 는 provider 예산 도메인 로직) | 호출마다 `AsyncClient(timeout=settings.dagster_request_timeout_seconds)` | `api/dagster_http.py:164` |
| ktw | 수제 sync 루프 `min(0.5*2**attempt, 5.0)`, `retryable` 분류 | 공유 `httpx.Client(follow_redirects=True)`; `python-airkorea-api` 는 자체 지터 retry | `providers/base.py:279-380`, `python-airkorea-api/src/airkorea/_http.py` |
| pinvi | tenacity **선언만**(lock 9.1.4) — `apps/api/app` 내 import 0건(사실). 클라이언트마다 수제 루프(`max_attempts=3`, `backoff_base 0.2*2**attempt`) | lifespan 당 1개 `AsyncClient` 공유, `api_call_event_hooks` | `clients/kor_travel_geo.py:57-79`, `clients/kakao_local.py`, `main.py:58-73` |

관찰: 지수 백오프 3회는 geo(tenacity)·pinvi(수제)·ktw(수제)가 같은 파라미터 감각(0.2~0.5초 기저, 최대 2~5초)이다. 라이브러리 채택은 geo만 했다.

### 2.12 시간 · 좌표 유틸

| 앱 | 시간 | 좌표/경계 | 파일 |
|---|---|---|---|
| kta | `SEOUL_TZ = ZoneInfo`, `now_utc`, `to_seoul`, `to_utc`, `combine_korean_timestamp`, `align_to_interval`, `split_by_local_day` | 없음 | `backend/app/core/time_utils.py` |
| ktc | `utcnow()` aware UTC | PostGIS `ST_MakePoint(lng, lat)` 헬퍼 | `models/base.py:15`, `core/spatial.py` |
| ktdm | `utcnow()` **naive** UTC(SQLite DateTime 호환 목적 명시) | 없음 | `_time.py` |
| geo | `datetime.now(UTC)` | `Point(x=lon,y=lat)`, `normalize_crs`, `is_korea_lon_lat`: `123<lon<132, 32<lat<39`(개구간); PostGIS 4326↔5179 | `dto/common.py:14-63`, `infra/coordinates.py` |
| map | `KST = ZoneInfo("Asia/Seoul")`, `kst_now`, `check_aware_datetime`(naive 거부, ADR-019) | shapely WKT + 경계 `124–132, 33–39.5`; pyproj Transformer 싱글턴(ADR-030) | `dto/_time.py`, `core/geometry.py:46-50` |
| ktw | `KST = timezone(timedelta(hours=9))`(고정 오프셋), `kst_now` | pyproj | `models.py:20,240` |
| pinvi | `KST = ZoneInfo`, `kst_now`, `utc_now` | 입력 경계 `124–132, 33–43` / 서비스 경계 `lat ≤ 39.5`(두 사각형에 이름 부여, ADR-064) | `core/time.py`, `core/coord_range.py` |

관찰(사실): 한국 좌표 경계 상수가 세 값(geo 개구간 123–132/32–39, map 124–132/33–39.5, pinvi 124–132/33–43 + 39.5)이다. KST 표현이 `ZoneInfo`(kta·map·pinvi) vs 고정 오프셋(ktw)으로, UTC now가 aware(ktc) vs naive(ktdm)로 갈린다. 시간 유틸의 함수 이름(`kst_now`/`utc_now`)은 map·ktw·pinvi가 같다.

### 2.13 백업 · 복원 오케스트레이션

| 앱 | 방식 | 산출물 규약 | 파일 |
|---|---|---|---|
| kta | `pg_dump`/`pg_restore` subprocess, 파일명 문법 `parking-radar-<ts>Z(-tag).dump`, staging 청소, 보존 개수, 용량 상한, 업로드 | `.dump` | `backend/app/services/backup_restore.py` |
| ktc | 없음(grep 0건) | — | — |
| ktdm | 인스턴스별 `docker exec --user postgres pg_dump`(geo, geo_dagster, concierge, map_application, map_dagster, pinvi), `flock`, 오프박스 동기화, in-memory job runner | `<role>-<ts>.dump` + `.sha256` + `.manifest` "3종 세트" | `services/standalone_backup.py`, `offbox_backup_sync.py`, `job_runner.py` |
| geo | `run_backup_job/run_restore_job`, ops 테이블 artifact, RustFS 업로드, 보존 클래스, restore drill/hotswap/scratch DB, Dagster 스케줄 + admin API `run-due` | tar(`kor_travel_geo_backup`) | `infra/backup.py`(2,500행+), `infra/restore_drill.py`, dagster `backup*.py` |
| map | admin backups/restore 라우터 | 미확인 | `api/routers/admin_backups.py` |
| ktw | 없음(grep 0건) | — | — |
| pinvi | 셸 스크립트(`backup-db.sh`, `restore-db.sh`, `restore-hotswap.sh`) 래핑, 단계(`preparing→switching`) 파싱, checksum sidecar, 디스크 가드, schema-swap | `pinvi-*.dump` + sha256 | `services/backup_service.py`, `apps/api/Dockerfile` |

관찰: 같은 PostgreSQL 인스턴스들을 5개의 서로 다른 오케스트레이터가 백업한다(사실). ktdm이 4개 인스턴스를 외부에서 이미 백업하므로 앱 내부 백업은 도메인(artifact 메타·hotswap·restore drill)에 강하게 결합돼 있다. 코드 공통화보다 산출물 규약(파일명·체크섬·manifest) 공유가 현실적이다(후보).

### 2.14 Dagster 정의 패턴

| 항목 | geo | map | ktw | pinvi | ktc / kta / ktdm |
|---|---|---|---|---|---|
| 패키지 | 별도 배포 `kortravelgeo-dagster`(일반 패키지, namespace 아님, `kor-travel-geo==0.1.0` 의존) | `kortravelmap.dagster` namespace 서브패키지 | `kortravelweather_dagster` | `pinvi.etl` (`apps/etl`) | Dagster 없음(ktc는 APScheduler 단일 워커 ADR-13, kta는 asyncio task, ktdm은 없음) |
| 스타일 | `@op`/`@job` (asset 0건) | `@asset` 중심(assets.py 29건) + jobs/schedules/sensors | `@asset` + `define_asset_job` + `ScheduleDefinition` | `@asset` ×6 + `define_asset_job` + schedules + `@run_failure_sensor` | — |
| 리소스 | `@resource` 함수 + `REQUIRED_RESOURCE_KEYS` + `_missing_resource` 가드("value → real @resource → missing-guard") | `@resource` + `DagsterField` + `REQUIRED_RESOURCE_KEYS`(50+) + 동일한 3단 폴백 | `ConfigurableResource` 클래스 | `ConfigurableResource` + `EnvVar` | — |
| 실패 통지 | `failure_notifier` 기본 None | `sensors.py` `run_failure_sensor` | 없음 | Telegram outbox + Sentry | — |
| 스토리지 | dagster-postgres, `docker/dagster.yaml` | dagster-postgres, `docker/dagster.yaml`, DB 기반 schedule override | 미확인 | 미확인 | — |
| 메트릭 | 없음 | 없음 | `start_metrics_server` import 시점 기동 + multiprocess | 없음 | — |
| 유사도 | 유사(map과 골격 동일) | 유사 | 상이 | 상이 | 없음 |

사실: geo `definitions.py` 의 3단 폴백 설명 문구와 `_missing_resource`/`_value_resource` 구현은 map `definitions.py` 와 같고, geo dagster `pyproject.toml` 주석이 "Pinned like map pins ``kor-travel-map``" 이라 밝힌다. op/job(geo) vs asset(나머지) 차이는 공통 헬퍼 설계에 영향을 준다.

### 2.15 CLI

| 앱 | 프레임워크 | 진입점 | 동시 실행 제어 | 파일 |
|---|---|---|---|---|
| kta | 없음(`scripts/*.py`) | — | — | `scripts/export_openapi.py` 등 |
| ktc | argparse | `ktcctl api/mcp/scheduler/etl` (프로세스 런처) | — | `backend/ktc/cli.py` |
| ktdm | argparse | `ktdctl` 다수 서브커맨드 | `fcntl` 파일 락 | `cli.py` |
| geo | **typer** | `ktgctl` + 서브 Typer 9개(load/refresh/validate/jobs/backup/restore/serving/geoip/janitor) | PG advisory lock `cross_process_lock` | `cli/main.py:70-88,147-1043` |
| map | argparse | `ktmctl status/consistency-report/import …`, exit 2/3 규약 | PG advisory lock `try_mutex_lock`(ADR-039) | `cli/main.py` |
| ktw | argparse | `ktwctl init-db` | — | `cli.py` |
| pinvi | argparse(명령 모듈별 console script 6개) | `pinvi-admin-bootstrap` 등 | — | `commands/*.py` |

관찰: typer는 geo만 쓴다(사실). "typer 명령 구조" 공통화의 근거는 약하다. 공통 후보는 프레임워크가 아니라 "변경 명령의 advisory-lock 뮤텍스 + skip exit code"(geo·map)다.

### 2.16 테스트 인프라

| 앱 | DB 제공 방식 | 격리 | 이벤트 루프 | 특이점 | 파일 |
|---|---|---|---|---|---|
| kta | 기본 sqlite+aiosqlite, `TEST_DATABASE_URL` 로 PG 선택 | TRUNCATE | `asyncio_mode=auto` | `PARKING_RADAR_TEST_DATABASE=1` → NullPool | `backend/tests/conftest.py` |
| ktc | `KTC_TEST_PG_DSN` 없으면 skip | drop_all/create_all per test | auto | `before_flush` 로 PostGIS/FK 스텁 | `backend/tests/conftest.py` |
| ktdm | SQLite in-memory 스왑 | — | — | env 핀(`KTDM_RUNTIME_PINS_FILE`) 고정 | `backend/tests/conftest.py` |
| geo | 외부 DSN + `_pg_guard.py`(보호 DB 이름·세그먼트 규칙·`pytest_sessionfinish` 로 거부 시 실패) | 테스트별 | Windows selector loop 정책 강제 | `testcontainers[postgres]` dev 의존 선언, tests 내 import 0건(사실); `pytest-postgresql` 사용 미확인 | `tests/integration/conftest.py`, `_pg_guard.py` |
| map | testcontainers, `postgis/postgis@sha256:dc17…` digest 핀, template0에서 fresh DB | session-scope engine + per-test rollback | `asyncio_default_fixture_loop_scope=session` | markers 7종, `filterwarnings=error`, hypothesis, vcrpy | `tests/integration/conftest.py` |
| ktw | 외부 DSN 기본 `127.0.0.1:15432` | autouse TRUNCATE | — | `KOR_TRAVEL_WEATHER_ENV=development` 강제 | `conftest.py`, `packages/*/tests/conftest.py` |
| pinvi | testcontainers `postgis/postgis:16-3.5-alpine`(태그) + subprocess `alembic upgrade head` | function-scope engine NullPool + TRUNCATE | function loop | 앱 전역 monkeypatch, 앱과 동일 `SESSION_TIMEOUT_SERVER_SETTINGS` 적용, `pytest-split` 4 shard, freezegun | `apps/api/tests/integration/conftest.py` |

관찰: 두 계열이다 — testcontainers(map·pinvi) vs 외부 DSN + skip(geo·ktc·ktw·kta). 이미지 핀 정책(digest vs tag)과 루프 스코프(session vs function)가 다르며, pinvi conftest는 session-scope engine의 "different loop" 문제를, map은 그 해법(`asyncio_default_fixture_loop_scope=session`)을 각각 주석으로 기록한다(사실). 공통 픽스처는 이 두 선택을 파라미터로 노출해야 한다.

### 2.17 품질 게이트

| 항목 | kta | ktc | ktdm | geo | map | ktw | pinvi |
|---|---|---|---|---|---|---|---|
| ruff select | 없음 | 없음 | E,F,I,UP,B,ASYNC (ignore E501,E402) | E,F,W,I,N,UP,B,A,C4,SIM,TCH,RUF,ASYNC | E,F,I,UP,B,ASYNC,PIE,PT,RET,SIM,TID | E,F,I,UP,B,ASYNC,RET,SIM | E,F,W,I,UP,B,RUF,S,ASYNC (ignore E501,S101) |
| line-length | — | — | 100 | 100 | 100 | 100 | 100 |
| target-version | — | — | py311 | py312 | py311 | py311 | py312 |
| `ruff format --check` | — | — | — | — | CI(src, tests) | — | CI |
| mypy | 없음 | 없음 | dev 의존만, 설정 없음 | strict + pydantic plugin, CI | strict + `warn_unused_ignores` + pydantic plugin, 패키지별 CI | strict(설정), CI 실행 여부 미확인 | strict + overrides, CI |
| import-linter | — | — | — | layers `api>cli>client>loaders>infra>core>dto` | layers + forbidden 3종(fastapi/uvicorn/starlette, 캐시 라이브러리, kafka) | — | — |
| coverage | pytest-cov 의존만 | — | — | — | `fail_under=80`(lib), CI api 70 / dagster 80 | — | — |
| pre-commit | — | — | — | ruff v0.7.4, mypy v1.13.0, import-linter | journal 필수, prod 비밀 검사, ruff format, mypy, lint-imports | — | — |
| 기타 게이트 | `alembic check` | — | — | OpenAPI drift | OpenAPI drift 3 profile, Dockerfile 실제 빌드, 작업 원장 lint | OpenAPI drift(git diff) | wheel 설치 검증, 4-shard integration |

사실: ruff를 설정한 5곳 모두 `line-length = 100` 이고 `E,F,I,UP,B,ASYNC` 를 공통으로 포함한다. 그 위에 각 앱이 2~8개 규칙군을 더한다. pre-commit의 ruff/mypy 버전(geo v0.7.4/v1.13.0)은 lockfile 버전(ruff 0.16.x, mypy 2.3.1)보다 훨씬 오래돼 사실상 별개 도구 체인이다(추정: pre-commit hook은 자체 환경을 만들므로 CI와 다른 결과를 낼 수 있음).

### 2.18 OpenAPI export

| 앱 | 스크립트 | 산출물 | CI drift 검사 | 파일 |
|---|---|---|---|---|
| kta | `create_app(Settings(...)).openapi()` → JSON | `docs/openapi.json` | 없음(ci.yml에 openapi 단계 0건) | `scripts/export_openapi.py` |
| ktc | 없음 | — | — | — |
| ktdm | 없음 | — | — | — |
| geo | `create_app().openapi()` sort_keys, `--check` | `openapi.json` | `.github/workflows/openapi.yml` | `scripts/export_openapi.py` |
| map | profile `all/user/service`, `--check` | `openapi.json`, `openapi.user.json`, `openapi.service.json` | `openapi.yml` | `packages/kor-travel-map-api/scripts/export_openapi.py` |
| ktw | `app.openapi()` → JSON | `packages/kor-travel-weather-api/openapi.json` | ci.yml `git diff --exit-code` | `packages/kor-travel-weather-api/scripts/export_openapi.py` |
| pinvi | 자체 export 없음(미확인); map의 `openapi.user/service.json` 스냅샷을 `tests/contract/` 에 두고 sha256 provenance로 검증 | `apps/api/tests/contract/kor-travel-map-openapi-*.json` | api.yml | `.github/workflows/api.yml:289-450` |

사실: kta 스크립트 docstring은 "mirrors kor-travel-map's … convention" 이라 밝히고, 네 스크립트(kta·geo·map·ktw)의 핵심은 `app.openapi()` → `json.dumps(ensure_ascii=False, indent=2)` 로 같다.

### 2.19 유사도 요약 매트릭스

| 항목 | 동일/유사 구현 수 | 상이 | 없음 | 공통화 신호 |
|---|---|---|---|---|
| 설정 클래스 | 6 | 1(ktdm) | 0 | 강 |
| 로깅 | 1(구현) + 2(설정만) | 2 | 2 | 중(수요 있음, 구현 없음) |
| 메트릭 | 5 | 1(ktdm) | 1 | 강(어휘 불일치가 오히려 근거) |
| health | 7 liveness / 1 readiness | — | — | 강 |
| DB 엔진 | 4(asyncpg) + 1(psycopg async) | 1(sync) + 1(sqlite) | — | 중~강 |
| alembic env | 3(동일) + 2(유사) | 2 | 1 | 중 |
| 공개 API 키 | 4(동일 함수) | — | 3 | 강 |
| admin 프록시 신뢰 | 4(유사) | — | 3 | 중(헤더명 상이) |
| 비밀번호/세션 | 0 | 2 | 5 | 없음(공통화 대상 아님) |
| CORS csv 파서 | 3(동일 로직) | 1(map 표면 스코프) | 1 | 중 |
| 보안 헤더 | 2 | — | 5 | 중(정책 충돌) |
| 에러 응답 | 3(RFC7807) | 3 | 1 | 중(형식 합의 필요) |
| retry | 1(tenacity) + 2(수제 동형) | — | 4 | 중 |
| 시간 유틸 | 3(`kst_now`) | 2 | 2 | 중 |
| 좌표 경계 | 0 | 3 | 4 | 없음(값 자체가 다름) |
| 백업 | 0 | 5 | 2 | 없음(규약만) |
| Dagster defs 골격 | 2(geo=map) | 2 | 3 | 중 |
| CLI 뮤텍스 | 2 | 1 | 4 | 약~중 |
| 테스트 픽스처 | 2(testcontainers) + 4(DSN) | — | 1 | 중 |
| ruff 기본 규칙 | 5 | — | 2 | 강 |
| OpenAPI export | 4 | — | 3 | 강 |

## 3. 공통 Python 패키지 후보 (모듈 단위)

전제: 단일 배포 이름(예: `kor-travel-common-py`, import 루트 `kortravelcommon`)에 extras로 분리한다. geo·map은 import-linter로 라이브러리 계층에서 `fastapi/starlette` import를 금지하므로(사실: `map:pyproject.toml` forbidden 계약, geo layers 계약) FastAPI 의존 모듈은 반드시 `[api]` extra 아래에 두고 코어 모듈은 stdlib+pydantic만 의존해야 한다. geo `infra/metrics.py` 의 `_NoopMetric` 폴백은 이 요구를 이미 보여준다.

신뢰도 = 사실 근거의 강도(구현 수·동일성). 도입 난이도 = 소비 앱의 공개 계약(env 이름·메트릭 이름·응답 형식·경로)을 바꾸는 정도.

| # | 모듈(후보) | 내용 | 현재 구현 보유(소비 후보) | 신뢰도 | 도입 난이도 | 비고 |
|---|---|---|---|---|---|---|
| C1 | `settings` | `BaseSettings` 베이스: `.env` 튜플, `extra=ignore`, `hide_input_in_errors`, SecretStr 마스킹된 ValidationError(pinvi), `get_settings/set_settings` 싱글턴(geo 방식), 접두는 앱이 지정 | kta, ktc, geo, map, ktw, pinvi(6) / ktdm은 신규 도입 | 높음 | 중 | env 이름·접두는 절대 바꾸지 않는다(배포 `.env` 계약). 베이스 클래스만 공유 |
| C2 | `logging` | structlog JSON + stdlib 브리지(pinvi `configure_logging`) + 요청 ID contextvars 미들웨어 + 서버발급/수용 정책 옵션(ktdm 근거) + `mask_secret`(ktc) + `RequestIdLogFilter`(ktdm) | pinvi(구현), geo·map(설정만), ktw·ktdm(요청 ID) | 중 | 중 | `[api]` extra. json/console 스위치는 geo·map 설정 필드가 이미 정의 |
| C3 | `metrics` | 접두 정책(`<svc>_`), `http_requests_total{method,route,status_code}`/duration/in_progress 표준 라벨, 미매칭 센티널, route template 해석, 라벨 정규화(ktc), 선택적 prometheus_client(geo noop), multiprocess(ktw·pinvi), DB pool gauge(geo·pinvi), 엔진 쿼리 훅(geo·map) | ktc, geo, map, ktw, pinvi(5) / ktdm은 어댑터 필요 | 높음 | 중~높 | 이름 변경은 대시보드·alert 회귀. geo가 방금 `ktg_` 로 바꾼 직후이므로 접두 정책은 geo 규약(`kt<x>_`)을 따르는 편이 변경 최소(후보). map `kor_travel_map_`, pinvi `pinvi_api_` 가 변경 대상 |
| C4 | `health` | `/healthz` liveness + `/readyz` deep(geo 알고리즘: DB 프로브 타임아웃·pool 이용률·503) + `/version`(git sha) 라우터 팩토리 | 7곳 전부 | 높음 | 낮 | 기존 경로는 alias로 유지. pinvi가 다른 서비스의 `/health` 를 프로브하므로 경로 폐기 금지 |
| C5 | `errors` | 베이스 예외(`code`, `http_status`, `hint`; geo 형태) + RFC 7807 `ProblemDetail{…, code, request_id}`(map·ktw 형태) 핸들러 | kta, map, ktw(형식 일치) / geo, pinvi(형식 상이) | 중 | 높 | pinvi `{error:{}}`·geo 3종은 공개 계약. 핸들러는 opt-in, 예외 베이스만 먼저 |
| C6 | `pagination` | cursor 인코딩(HMAC 서명·fingerprint) + `PageMeta` | ktc(keyset+snapshot), map(cursor, tamper 예외), ktw(offset) | 낮~중 | 높 | 정렬·ID 타입·total 정책이 다름. 선행 보고서 §3.4(테이블 데이터 책임)와 같은 이유로 후순위 |
| C7 | `auth.public_api_key` | `generate/hash/matches` + `?key=`/헤더 추출 + 형태 검증 + TTL 캐시 + 저장소 Protocol(ORM/raw SQL/SQLite는 앱 구현) | ktc, ktdm, geo, map(4, 함수 동일) | 높음 | 중 | 저장 스키마는 앱 소유. `ops.public_api_keys` DDL 템플릿은 geo·map만 공유 가능 |
| C8 | `auth.trusted_proxy` | peer CIDR 검사 + 프록시 비밀 상수시간 비교 + actor/roles 파싱 원시 함수; 헤더 이름은 인자 | ktc, ktdm, geo, map(4) | 중~높 | 중 | 헤더 이름 통일은 별도 정책(선행 보고서 §3.6 "신뢰 경계 통합은 별개" 유지) |
| C9 | `db` | `normalize_dsn(driver=...)`, `make_async_engine(dsn, pool, pre_ping, recycle, statement_timeout, search_path)`(asyncpg `server_settings` / psycopg `options` 흡수), `make_session_factory`, `get_db` 의존성 팩토리, 엔진 메트릭 훅 | kta, ktc, map, pinvi(asyncpg), geo(psycopg) / ktw(sync)는 별도 함수 | 높음 | 중 | 세션 GUC 기본값(pinvi lock/idle/statement, geo statement/search_path)은 앱 인자 |
| C10 | `alembic` 템플릿 | async `env.py` 골격(kta≈ktc≈pinvi), NullPool, settings URL 주입, `%` 이스케이프(ktw), 선택적 advisory lock(pinvi), `alembic check` CI 스텝, `post_write_hooks` ruff(map), `alembic/versions` 포맷 제외(pinvi) | kta, ktc, ktw, pinvi(4) / geo·map은 도메인 가드로 제외 | 중 | 낮~중 | 스크립트 템플릿(cookiecutter류)로 배포, import 의존 없음 |
| C11 | `testing` | testcontainers PostGIS 픽스처(digest 핀 옵션, template0 fresh DB, alembic upgrade), 외부 DSN 가드(geo `_pg_guard` 규칙), TRUNCATE 격리, loop-scope 가이드, Windows selector 정책 | map, pinvi(testcontainers) / geo, ktc, ktw, kta(DSN) | 중 | 중 | `[testing]` extra. 두 계열을 모두 지원해야 채택됨 |
| C12 | `openapi` | `export_openapi(app_factory, output, --check, profiles)` + CI 워크플로 템플릿 | kta, geo, map, ktw(4) / pinvi는 소비자 검증 | 높음 | 낮 | map profile 분기는 콜백으로 |
| C13 | `time` | `KST = ZoneInfo`, `kst_now/utc_now`, `check_aware_datetime`, 한국식 timestamp 파서·간격 정렬(kta) | kta, map, ktw, pinvi(4) / ktc(utcnow) | 높음 | 낮 | ktdm naive UTC와 ktw 고정 오프셋은 전환 시 명시 결정 필요 |
| C14 | `geo_primitives` | `Point(x=lon,y=lat)`, `normalize_crs` 만 | geo, (map·pinvi 유사 타입) | 낮 | 중 | 경계 상수는 세 값이 달라 공통 상수 금지(§4) |
| C15 | `http` | `AsyncClient` 팩토리(`httpx.Timeout` 프로파일), tenacity 기반 재시도 정책(geo 파라미터), api-call 이벤트 훅(pinvi) | geo, pinvi, ktw, ktc, map | 중 | 중 | pinvi는 tenacity를 이미 lock에 가짐 |
| C16 | `security_headers` | nosniff/DENY/Referrer/Permissions/CSP/HSTS 미들웨어, HSTS 조건 옵션(`trust_forwarded_proto`) | kta, pinvi(2) | 중 | 낮 | 기본값은 pinvi(#344, 전달 헤더 불신) 권장(후보) |
| C17 | `cors` | `parse_origins_csv`(와일드카드·credentials 상충 제거) | ktc, ktdm, kta(3) | 중 | 낮 | map 표면 스코프 미들웨어는 map 소유 |
| C18 | `dagster` | `build_definitions(required_keys, defaults, real_resources)` 3단 폴백(geo=map), `run_failure_sensor` 통지 어댑터(pinvi·map), `dagster.yaml` postgres 템플릿 | geo, map, pinvi | 중 | 중 | `[dagster]` extra. op/job vs asset 차이는 무관(리소스 조립 계층) |
| C19 | `cli.mutex` | PG advisory lock 컨텍스트 + skip exit code 3 | geo, map(2) | 약~중 | 낮 | typer/argparse 무관 |
| C20 | `quality`(설정 산출물) | ruff 베이스(`line-length=100`, `E,F,I,UP,B,ASYNC`), mypy strict 베이스, import-linter 계약 템플릿, pre-commit 템플릿, CI 스텝 템플릿 | ruff 5곳, mypy strict 4곳 | 높음 | 낮~중 | 코드가 아닌 규칙 산출물. `[tool.ruff] extend = "…"` 로 참조 |
| C21 | `backup_artifact_spec` | 파일명·sha256 sidecar·manifest 필드 규약 문서 | ktdm 3종 세트, kta, pinvi, geo | 중 | 낮(문서) | 코드 공통화 아님 |

우선순위 제안(후보): 1차 C4·C12·C13·C20(계약 변경 없음, 근거 강함) → 2차 C1·C9·C7·C3(계약 일부 변경, 근거 강함) → 3차 C2·C5·C11·C18·C15·C16·C17·C8·C10 → 보류 C6·C14·C19·C21.

## 4. 공통화하면 안 되는 도메인 결합 부분

| 영역 | 이유(사실 근거) |
|---|---|
| geo: 주소 DTO·geocoder·loaders(GDAL)·GeoIP Korea-only 게이트·admission control·source registry·backup artifact·VWorld 호환 오류 형식 | `pyproject.toml` loaders extra가 시스템 GDAL에 결합; `api/middleware/geoip_gate.py` 는 geo 정책(ADR-037); `api/responses.py` 3종 형식은 외부 계약 |
| map: route policy matrix·`SurfaceScopedCORSMiddleware`·ServiceToken scope/digest·cache-target 프로토콜·alembic 300 baseline handoff·ADR-090 런타임 권한 경계·provider fetcher/retry 예산 | `api/route_policy.py`, `api/cors.py`, `api/settings.py:511-553`, `alembic/env.py` 전체, `infra/db.py:assert_runtime_db_privilege_boundary` |
| pinvi: JWT/refresh/OAuth/RBAC(404 은닉)/rate-limit 정책·geofence·cache-target sync worker·M05 계약 JSON(force-include)·백업 셸 스크립트·서비스 영역 좌표 경계 | `core/security.py`, `core/rbac.py`, `middleware/rate_limit.py`, `pyproject.toml [tool.hatch.build.targets.wheel.force-include]`, `core/coord_range.py` |
| ktdm: docker/compose 오케스트레이션·pinned runtime registry·`docker exec pg_dump`·SQLite 메트릭 DB·HMAC 서명 세션 쿠키·월간 로그 롤링 | `services/standalone_backup.py`, `services/auth_service.py`, `main.py:57-90` |
| ktc: LLM 클라이언트(Gemini/DeepSeek)·YouTube ETL·APScheduler 워커·MCP 서버·int ID 기반 keyset cursor | `etl/*`, `scheduler/worker.py`, `mcp_server/*`, `services/list_pagination.py`(`MAX_DB_INTEGER_ID`) |
| ktw: sync provider 어댑터·Dagster 워커 전용 multiprocess 메트릭 청소·자격증명 암호화 | `providers/base.py`, `metrics.py:70-230`, `settings.py:credential_encryption_key` |
| kta: 주차 도메인·sqlite/PG 이중 방언·lifespan 스케줄러 | `db/session.py`(PRAGMA 분기), `main.py:_run_scheduler` |
| 서비스 간 클라이언트(pinvi `clients/kor_travel_*.py`, geo `api/_dagster_client.py`, map `api/dagster_http.py`) | 선행 보고서 §7.2 "외부 제공자 API 단순 전달 facade 금지" 와 map ADR-006(provider wrapper 금지)에 부합. 공통 라이브러리를 서비스 간 간접 호출 계층으로 만들지 않는다 |
| 한국 좌표 경계 상수 | 세 앱의 값이 다르고 각각 근거 문서(map `geometry.py`, pinvi ADR-064, geo `KOREA_LON_LAT_BOUNDS_MESSAGE`)가 있다. 하나로 합치면 어느 한 앱의 검증이 바뀐다 |
| 비밀번호 해시·세션 저장소·CSRF | ktdm(pbkdf2+서명 쿠키+Origin 검사)과 pinvi(argon2+JWT)는 각자 감사·마이그레이션 이력이 있다. 선행 보고서 §3.6 결론 유지 |
| 기존 공유 라이브러리 | `python-*-api` 13종, `maplibre-vworld-*`, `python-kraddr-base`(map ADR-041로 흡수·archive 후보)는 재래핑 금지. `python-airkorea-api` 는 ktw 안에 vendored path 의존이고 map은 git+sha로 소비한다 — 같은 라이브러리의 두 배포 경로가 공존한다(사실). common의 대상이 아니라 provider 라이브러리 정책의 문제 |

## 5. 빌드/배포 방식 후보

### 5.1 기존 핀 관례(사실)

| 관례 | 사용처 | 예 |
|---|---|---|
| `git+https://github.com/digitie/<lib>.git@<sha>` | kta(2), map(14, `providers` extra), ktw(1) | `python-krairport-api @ git+https://…@cbe4d13…`(kta·map 동일 sha) |
| GitHub archive zip `@<sha>` | ktc(1) | `python-vworld-api @ https://github.com/digitie/python-vworld-api/archive/a1fea84….zip` |
| 이동 브랜치 `@main` | pinvi apps/etl(1) | `python-kasi-api @ git+…@main` — 재현 불가 핀(선행 보고서 §8 "이동하는 Git branch를 직접 참조하지 않는다" 위반 사례) |
| 로컬 path/editable | ktw(`[tool.uv.sources]` path·editable), map·geo·ktw 서브패키지(`pip install -e packages/...`), geo dagster(Dockerfile이 소스 COPY 후 설치) | `python-airkorea-api = { path = "packages/python-airkorea-api" }` |
| 사내 index | 없음(조사한 pyproject·Dockerfile·CI에 `extra-index-url`/`[[tool.uv.index]]` 참조 없음) | — |

같은 provider 라이브러리에 서로 다른 sha가 공존한다: `python-kma-api` map `a75d1e1` vs ktw `0868b76`; `python-kasi-api` kta `51c39c1` vs pinvi `main`. 버전 일치화 정책은 common 코드보다 이 핀 표를 먼저 다뤄야 한다(후보).

### 5.2 후보 비교

| 후보 | 장점 | 단점·전제 | 기존 관례와의 정합 |
|---|---|---|---|
| A. `git+https@<sha>`(또는 `@v0.x.y` 태그 + lock의 sha) | 발행 인프라 불필요; 13종 provider 라이브러리와 같은 방식; uv.lock/pip가 sha를 고정 | Docker 빌드에 `git` 필요(kta·ktw·pinvi Dockerfile은 이미 설치, map api.Dockerfile은 미확인); 비공개 저장소면 토큰 필요; sha 갱신 PR이 앱마다 발생 | **높음**. 선행 보고서 §8 "명시 버전과 lockfile" 원칙과 일치 |
| B. 로컬 path/editable(모노레포 링크·서브모듈) | 개발 중 즉시 반영 | CI/Docker에서 COPY 경로 결합(ktw airkorea·geo dagster 방식); 선행 보고서 §6 "file:../… 결합은 독립 CI에서 재현되지 않음" 지적 | 개발 편의로만 |
| C. 사내 PyPI 호환 index | 정식 wheel·버전 범위 해석·git 불필요 | 인프라·인증·가용성 운영 비용; 현재 어느 앱도 사용하지 않음; GitHub Packages는 PyPI 형식을 제공하지 않음(추정, 미확인) | 낮음(신규) |
| D. wheel 파일을 릴리스 자산으로 배포 후 URL 핀 | index 불필요, sha256 검증 가능 | 릴리스 절차 필요; ktc의 zip 관례와 유사 | 중 |

정합 판단(후보): A를 기본으로, 태그 `vX.Y.Z` 를 만들되 소비자는 `@<sha>` 를 적고 lockfile을 커밋한다. geo·map·ktdm·ktc는 lockfile이 없으므로 도입 전제로 `uv.lock`(또는 `pip-compile`) 채택이 필요하다(§7 열린 질문).

### 5.3 패키지 구성 제안(후보)

- 배포 이름 하나, import 루트 `kortravelcommon`(일반 패키지; geo dagster `pyproject.toml` 주석의 "pkgutil namespace magic 회피" 입장과 정합).
- extras: `core`(기본: settings·time·errors 베이스·geo_primitives; 의존 pydantic·pydantic-settings), `api`(fastapi·starlette·prometheus-client: health·metrics·logging 미들웨어·security_headers·cors·errors 핸들러·openapi), `db`(sqlalchemy; `asyncpg`/`psycopg` 는 앱이 선택), `dagster`, `testing`(testcontainers·pytest 플러그인), `http`(httpx·tenacity).
- 파이썬 floor: 3.11(map·ktw·ktdm 때문) — 단, 앱 floor를 3.12로 올리는 정책이 확정되면 3.12. geo의 PEP 695 사용은 geo 내부에 국한되므로 common에는 영향 없음.
- 버전 범위 정책: fastapi/starlette/httpx는 map의 `starlette<1.0` 상한과 kta·ktw·pinvi의 `starlette 1.6` 실제 설치가 충돌하므로, common의 `[api]` extra 범위를 정하기 전에 map의 PR#60 근거(TestClient·httpx 2.x)를 재검증해야 한다(§7).
- 라이선스: common 루트는 GPL-3.0. 소비 앱 중 pinvi·ktdm·ktc는 MIT, kta는 선언 없음. GPL 라이브러리를 MIT 앱이 링크·배포할 때의 조건은 선행 보고서 §9와 같은 확인 절차가 필요하다(열린 질문).

## 6. 선행 검토 보고서(2026-09-05)와의 관계

| 선행 보고서 주장 | 본 조사 결과 | 판단 |
|---|---|---|
| "백엔드·인증까지 함께 통합할 근거는 부족하다"(§1) | 인증(비밀번호·세션·CSRF)은 동의. 그러나 비인증 인프라 모듈은 근거가 있다: 공개 API 키 함수 4곳 동일, OpenAPI export 4곳 동형, alembic env 3곳 동형, 설정 골격 6곳 동형, 메트릭 5곳 유사 | 부분 상이. "백엔드 전반"이 아니라 "§3 C1~C13 범위"로 좁히면 근거가 성립한다 |
| "Python 공유는 그 뒤 별도 수요 조사와 배포 설계를 거친다"(§7.1) | 본 문서가 그 수요 조사에 해당. 배포 설계는 §5 | 일치 |
| §3.6 인증 경계(geo/map은 Next.js 세션, 백엔드는 프록시 신원) | geo `api/security.py`, map `api/auth.py`, ktc `core/security.py`, ktdm `auth_service.py` 로 재확인. ktw는 저장소만 제공 | 일치 |
| §7.2 "외부 제공자 facade 금지" | pinvi 클라이언트·geo/map Dagster 클라이언트를 §4에서 제외 | 일치 |
| §8 "이동 Git branch 직접 참조 금지" | pinvi `apps/etl/pyproject.toml` 의 `python-kasi-api@main` 은 이 원칙에 어긋난다 | 일치(위반 사례 발견) |
| §12 geo 기준 `daf079b` | 본 조사 geo `1d9d74d` 는 그 이후. `daf079b` 자체가 메트릭 접두 `ktg_` 변경 커밋 | 기준 갱신 |

## 7. 열린 질문

1. Python floor: map·ktw·ktdm을 3.12로 올릴 것인가, common을 3.11 호환으로 쓸 것인가. ktw Docker는 이미 3.13이고 map CI는 3.11~3.13 matrix다.
2. fastapi/starlette 범위: map api의 `starlette<1.0` 상한 근거(PR#60 "starlette 1.0+ TestClient은 httpx 2.x 요구")가 kta·ktw·pinvi의 `starlette 1.6.0 + httpx 0.28.1` 설치 사실과 어떻게 양립하는지 재검증이 필요하다. 실행 검증을 하지 않았으므로 미확인.
3. ktdm의 fastapi `^0.110` 고정: lockfile이 없어 실제 설치 버전 미확인. 버전 일치화 대상 1순위 후보.
4. 메트릭 접두 정책: `kt<x>_`(ktc·ktdm·ktg·ktw)로 통일하면 map(`kor_travel_map_`)·pinvi(`pinvi_api_`)의 대시보드·alert 규칙 변경이 필요하다. 관측 스택(Prometheus/Grafana 설정)은 본 조사 범위 밖이라 영향 범위 미확인.
5. 요청 ID 정책: 서버 발급 강제(ktdm 근거: 로그 스푸핑 방지) vs 클라이언트 수용(ktw·pinvi). 프록시(Next.js BFF) 체인에서 어느 쪽이 발급자인지 결정 필요.
6. HSTS 조건: `X-Forwarded-Proto` 신뢰(kta) vs 불신(pinvi #344). 리버스 프록시 구성에 따라 답이 달라진다.
7. health 경로 이름(`/health` vs `/healthz`)과 readiness 표준(geo `ReadinessResponse`)을 채택할지, 소비자(pinvi system 프로브, compose healthcheck)의 변경 범위는 얼마인지.
8. 라이선스: GPL-3.0 common을 MIT 앱(pinvi·ktdm·ktc)과 kta(선언 없음)가 소비할 때의 조건. kta의 `LICENSE` 파일 존재 여부 미확인.
9. lockfile 없는 앱(geo·map·ktdm·ktc)의 재현 빌드 정책. "버전 일치화"는 lockfile 없이는 검증할 수 없다.
10. geo의 `structlog` 의존과 `log_format` 설정, map의 `log_format` 설정은 구현 예정인가 잔재인가. C2 설계의 첫 소비자를 정하는 데 필요하다.
11. geo dev extras의 `testcontainers`·`pytest-postgresql` 이 실제로 쓰이는지(tests 내 import 0건). C11의 geo 채택 가능성에 영향.
12. pinvi `/metrics` 의 접근 제어(코드에서 인증 미확인)와 map의 `KOR_TRAVEL_MAP_API_*` 프로파일별 요구 사항을 C3 보호 정책 기본값에 반영할지.
13. `python-airkorea-api` 의 두 배포 경로(ktw vendored path vs map git+sha)와 `python-kma-api`·`python-kasi-api` 의 sha 불일치 정리 주체.
14. ktc에 CI가 없고 lockfile도 없다. common 도입 전에 ktc의 최소 게이트(ruff·pytest·CI)를 어디서 정의할지.

## 8. 근거 파일 목록 (저장소 상대 경로)

kor-travel-airport @ 2bb1111

- `kta:backend/pyproject.toml`
- `kta:backend/uv.lock`
- `kta:backend/Dockerfile`
- `kta:.github/workflows/ci.yml`
- `kta:backend/app/core/config.py`
- `kta:backend/app/core/time_utils.py`
- `kta:backend/app/db/session.py`
- `kta:backend/app/main.py` (1-60, 100-260)
- `kta:backend/app/services/backup_restore.py` (1-100)
- `kta:backend/alembic/env.py`, `kta:backend/alembic.ini`
- `kta:backend/tests/conftest.py`
- `kta:scripts/export_openapi.py`

kor-travel-concierge @ 7945305

- `ktc:backend/requirements.txt`, `ktc:etl/requirements.txt`, `ktc:mcp/requirements.txt`, `ktc:scheduler/requirements.txt`
- `ktc:backend/pytest.ini`, `ktc:alembic.ini`
- `ktc:Dockerfile.python`
- `ktc:backend/ktc/core/config.py` (1-130, 380-410)
- `ktc:backend/ktc/core/database.py`
- `ktc:backend/ktc/core/logging.py`
- `ktc:backend/ktc/core/security.py` (1-160)
- `ktc:backend/ktc/core/spatial.py`
- `ktc:backend/ktc/telemetry.py`
- `ktc:backend/main.py` (1-130)
- `ktc:backend/ktc/cli.py`
- `ktc:backend/ktc/models/base.py`
- `ktc:backend/ktc/services/public_api_key_service.py` (1-80)
- `ktc:backend/ktc/services/list_pagination.py` (1-80)
- `ktc:backend/alembic/env.py`
- `ktc:backend/tests/conftest.py`
- `ktc:scheduler/worker.py` (1-60)

kor-travel-docker-manager @ 862562d

- `ktdm:backend/pyproject.toml`
- `ktdm:.github/workflows/ci.yml`
- `ktdm:backend/src/kor_travel_docker_manager/main.py` (1-120, 200-300, 350-380)
- `ktdm:backend/src/kor_travel_docker_manager/database.py` (1-100)
- `ktdm:backend/src/kor_travel_docker_manager/request_context.py`
- `ktdm:backend/src/kor_travel_docker_manager/_time.py`
- `ktdm:backend/src/kor_travel_docker_manager/models.py` (1-40)
- `ktdm:backend/src/kor_travel_docker_manager/api/auth.py` (1-100)
- `ktdm:backend/src/kor_travel_docker_manager/api/security.py`
- `ktdm:backend/src/kor_travel_docker_manager/services/auth_service.py` (1-160)
- `ktdm:backend/src/kor_travel_docker_manager/services/public_api_key_service.py` (1-60)
- `ktdm:backend/src/kor_travel_docker_manager/services/errors.py`
- `ktdm:backend/src/kor_travel_docker_manager/services/metrics_collector.py` (1-80, 640-700)
- `ktdm:backend/src/kor_travel_docker_manager/services/standalone_backup.py` (1-100)
- `ktdm:backend/src/kor_travel_docker_manager/services/job_runner.py` (1-60)
- `ktdm:backend/src/kor_travel_docker_manager/cli.py` (1-80)
- `ktdm:backend/tests/conftest.py`

kor-travel-geo @ 1d9d74d

- `geo:pyproject.toml`, `geo:kor-travel-geo-dagster/pyproject.toml`
- `geo:.github/workflows/ci.yml`, `geo:.github/workflows/openapi.yml`, `geo:.pre-commit-config.yaml`
- `geo:docker/api.Dockerfile`, `geo:kor-travel-geo-dagster/docker/dagster.Dockerfile`
- `geo:src/kortravelgeo/settings.py` (1-140, 360-375)
- `geo:src/kortravelgeo/infra/engine.py`
- `geo:src/kortravelgeo/infra/metrics.py` (1-130, 590-620, 725-760; `git log` 포함)
- `geo:src/kortravelgeo/infra/external_api.py` (1-160)
- `geo:src/kortravelgeo/infra/coordinates.py` (1-60)
- `geo:src/kortravelgeo/infra/backup.py` (1-80)
- `geo:src/kortravelgeo/infra/public_api_keys.py` (1-100)
- `geo:src/kortravelgeo/exceptions.py`
- `geo:src/kortravelgeo/dto/common.py` (1-80), `geo:src/kortravelgeo/dto/health.py`
- `geo:src/kortravelgeo/api/app.py` (1-140), `geo:src/kortravelgeo/api/responses.py` (1-80), `geo:src/kortravelgeo/api/security.py` (1-140), `geo:src/kortravelgeo/api/public_api_key.py` (1-60), `geo:src/kortravelgeo/api/routers/healthz.py`
- `geo:src/kortravelgeo/cli/main.py` (1-100)
- `geo:kor-travel-geo-dagster/src/kortravelgeo_dagster/definitions.py`, `geo:…/resources.py` (1-130)
- `geo:alembic/env.py`, `geo:alembic.ini`
- `geo:tests/integration/conftest.py`, `geo:tests/integration/_pg_guard.py` (1-40)
- `geo:scripts/export_openapi.py` (1-40)
- `geo:docs/kor-travel-common-library-review.md`

kor-travel-map @ c494e227

- `map:pyproject.toml`, `map:packages/kor-travel-map-api/pyproject.toml`, `map:packages/kor-travel-map-dagster/pyproject.toml`
- `map:.github/workflows/ci.yml`, `map:.github/workflows/lint.yml`, `map:.github/workflows/openapi.yml`, `map:.pre-commit-config.yaml`
- `map:docker/api.Dockerfile`, `map:docker/dagster.Dockerfile`
- `map:src/kortravelmap/settings.py` (1-120, 525-560)
- `map:src/kortravelmap/infra/db.py`
- `map:src/kortravelmap/infra/public_api_keys.py` (1-100)
- `map:src/kortravelmap/core/exceptions.py` (1-140)
- `map:src/kortravelmap/core/geometry.py` (1-60)
- `map:src/kortravelmap/dto/_time.py` (1-60)
- `map:src/kortravelmap/cli/main.py` (1-120)
- `map:packages/kor-travel-map-api/src/kortravelmap/api/settings.py` (330-420)
- `map:packages/kor-travel-map-api/src/kortravelmap/api/app.py` (1-120, 500-560, 1068-1090)
- `map:packages/kor-travel-map-api/src/kortravelmap/api/db.py`
- `map:packages/kor-travel-map-api/src/kortravelmap/api/prometheus.py` (1-270)
- `map:packages/kor-travel-map-api/src/kortravelmap/api/cors.py` (1-60, 130-200)
- `map:packages/kor-travel-map-api/src/kortravelmap/api/auth.py` (1-140)
- `map:packages/kor-travel-map-api/src/kortravelmap/api/response.py` (1-80)
- `map:packages/kor-travel-map-api/src/kortravelmap/api/routers/public_status.py` (40-130), `map:…/routers/admin_auth.py` (1-80)
- `map:packages/kor-travel-map-api/scripts/export_openapi.py` (1-40)
- `map:packages/kor-travel-map-dagster/src/kortravelmap/dagster/definitions.py` (1-100)
- `map:alembic/env.py`, `map:alembic.ini`
- `map:tests/conftest.py`, `map:tests/integration/conftest.py` (1-140)

kor-travel-weather @ 6003da9

- `ktw:pyproject.toml`, `ktw:packages/kor-travel-weather-api/pyproject.toml`, `ktw:packages/kor-travel-weather-dagster/pyproject.toml`, `ktw:packages/python-airkorea-api/pyproject.toml`
- `ktw:uv.lock`
- `ktw:.github/workflows/ci.yml`, `ktw:deploy/Dockerfile.python`
- `ktw:src/kortravelweather/settings.py` (1-260, 332-351, 435)
- `ktw:src/kortravelweather/metrics.py` (1-130, 190-345, 380-420)
- `ktw:src/kortravelweather/repository.py` (480-530)
- `ktw:src/kortravelweather/providers/base.py` (1-80, 279-380)
- `ktw:src/kortravelweather/models.py` (20, 240)
- `ktw:src/kortravelweather/cli.py` (1-100)
- `ktw:packages/kor-travel-weather-api/src/kortravelweather_api/app.py` (1-200), `ktw:…/auth.py`, `ktw:…/response.py`, `ktw:…/routers/weather.py` (grep)
- `ktw:packages/kor-travel-weather-api/scripts/export_openapi.py`
- `ktw:packages/kor-travel-weather-dagster/src/kortravelweather_dagster/definitions.py` (1-120), `ktw:…/resources.py` (1-80)
- `ktw:packages/python-airkorea-api/src/airkorea/_http.py` (1-60)
- `ktw:alembic/env.py`, `ktw:alembic.ini`
- `ktw:conftest.py`, `ktw:packages/kor-travel-weather-api/tests/conftest.py`, `ktw:packages/kor-travel-weather-dagster/tests/conftest.py`

pinvi @ 9af25e5

- `pinvi:apps/api/pyproject.toml`, `pinvi:apps/etl/pyproject.toml`, `pinvi:apps/api/uv.lock`
- `pinvi:.github/workflows/api.yml`, `pinvi:.github/workflows/etl.yml`, `pinvi:apps/api/Dockerfile`
- `pinvi:apps/api/app/core/config.py` (600-700, 2527-2532)
- `pinvi:apps/api/app/core/logging.py`, `pinvi:apps/api/app/core/errors.py`, `pinvi:apps/api/app/core/security.py` (1-120), `pinvi:apps/api/app/core/session_cookies.py`, `pinvi:apps/api/app/core/deps.py` (1-120), `pinvi:apps/api/app/core/rbac.py` (1-60), `pinvi:apps/api/app/core/time.py`, `pinvi:apps/api/app/core/coord_range.py` (1-60)
- `pinvi:apps/api/app/db/session.py`
- `pinvi:apps/api/app/main.py` (1-160)
- `pinvi:apps/api/app/middleware/prometheus.py`, `pinvi:…/request_id.py`, `pinvi:…/security_headers.py` (1-100), `pinvi:…/rate_limit.py` (1-60), `pinvi:…/api_call_logging.py` (1-40)
- `pinvi:apps/api/app/api/v1/healthz.py` (1-60), `pinvi:apps/api/app/schemas/health.py` (1-40)
- `pinvi:apps/api/app/clients/kor_travel_geo.py` (1-120)
- `pinvi:apps/api/app/services/backup_service.py` (1-80), `pinvi:apps/api/app/services/auth_session.py` (1-60)
- `pinvi:apps/api/app/commands/admin_bootstrap.py` (1-50)
- `pinvi:apps/api/alembic/env.py`, `pinvi:apps/api/alembic.ini`
- `pinvi:apps/api/tests/conftest.py`, `pinvi:apps/api/tests/integration/conftest.py` (1-120)
- `pinvi:apps/etl/pinvi/etl/definitions.py`, `pinvi:…/resources.py`, `pinvi:…/schedules.py` (1-40), `pinvi:…/sensors.py` (1-40)
