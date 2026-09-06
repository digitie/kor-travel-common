# 횡단 비교 — OpenAPI·REST 규약 (7개 FastAPI 백엔드)

- 작성일: 2026-09-06
- 성격: 읽기 전용 조사 결과. 조사 대상 저장소는 수정하지 않았다. 본 문서는 `kor-travel-common`이 정할 공통 REST/OpenAPI 규약과 공통 코드 후보의 근거 자료다.
- 표기: **사실** = 커밋된 파일에서 직접 확인. **후보** = common 설계 제안. **추정** = 코드 정황으로 판단했으나 실행·문서로 확정하지 못함. **미확인** = 조사 범위 안에서 확인하지 못함.
- 선행 검토 보고서(`F:/dev/kor-travel-geo-fixes/docs/kor-travel-common-library-review.md`, 2026-09-05)는 UI 공통화에 집중했고 백엔드 계약은 "통합 근거 부족"으로 정리했다. 본 문서는 그 결론을 백엔드 계약 관점에서 재검증한다(§3.5 참조).

## 0. 기준 커밋

| 저장소 | 체크아웃 경로 | 커밋 | 조사한 FastAPI 앱 |
|---|---|---|---|
| kor-travel-geo | `F:/dev/kor-travel-geo-fixes` | `1d9d74d` | `src/kortravelgeo/api/app.py` (`create_app`) |
| kor-travel-map | `F:/dev/kor-travel-common-survey/ktm-main` | `c494e227` | `packages/kor-travel-map-api/src/kortravelmap/api/app.py` (`create_app`, 모듈 `app`) |
| kor-travel-weather | `F:/dev/kor-travel-weather` | `6003da9` | `packages/kor-travel-weather-api/src/kortravelweather_api/app.py` (`create_app`, 모듈 `app`) |
| kor-travel-airport | `F:/dev/kor-travel-common-survey/kta-main` | `2bb1111` | `backend/app/main.py` (`create_app`) |
| pinvi | `F:/dev/kor-travel-common-survey/pinvi` | `9af25e5` | `apps/api/app/main.py` (모듈 `app`) |
| kor-travel-concierge | `F:/dev/kor-travel-concierge` | `7945305` | `backend/main.py` (`create_app`, 모듈 `app`) |
| kor-travel-docker-manager | `F:/dev/kor-travel-common-survey/ktdm-main` | `862562d` | `backend/src/kor_travel_docker_manager/main.py` (모듈 `app`) |

이하 표에서 열 이름은 geo / map / weather / airport / pinvi / concierge / ktdm 으로 줄인다. 경로는 각 저장소 상대 경로다.

## 1. 방법

실행한 읽기 명령(요지):

- `git -C <repo> rev-parse --short HEAD` 로 기준 커밋 확인.
- `rg -t py "FastAPI\("` 로 앱 팩토리 위치 확인(테스트 파일 제외).
- 각 앱의 팩토리 파일, 예외 핸들러 모듈, 인증 의존성 모듈, 라우터 정의(`APIRouter(`/`prefix=`/`tags=`), 페이지네이션 파라미터(`Query(`), ETag/`If-Match`/`Idempotency-Key`/`Retry-After` 사용처, health/metrics 경로, OpenAPI export 스크립트, `.github/workflows/*.yml`, 프론트 `package.json`의 typegen 스크립트를 `sed`/`grep`/`rg` 로 읽었다.
- 커밋된 OpenAPI JSON(geo `openapi.json`, map `openapi.json`·`openapi.user.json`·`openapi.service.json`, weather `packages/kor-travel-weather-api/openapi.json`, airport `docs/openapi.json`)은 스크래치패드에 둔 파이썬 스크립트로 `info`/`servers`/`securitySchemes`/`x-*` 확장/`operationId`/태그/에러 스키마명을 추출했다(조사 대상 저장소에는 아무 파일도 만들지 않았다).
- 라이브러리 버전은 `pyproject.toml`/`requirements.txt` 범위와 `uv.lock`(존재하는 경우)로 읽었다. 로컬 `.venv`/`node_modules`는 보지 않았다.

읽은 주요 파일은 §7 근거 파일 목록에 있다.

## 2. 항목별 비교표

### 2.1 앱 팩토리 · title · version · servers · docs 경로

| 항목 | geo | map | weather | airport | pinvi | concierge | ktdm |
|---|---|---|---|---|---|---|---|
| 생성 방식 | `create_app()` 팩토리 (`api/app.py:150`) | `create_app()` + 모듈 `app = create_app()` (`app.py:1381`) | `create_app(settings, repository)` + 모듈 `app` (`app.py:76,270`) | `create_app(settings)` (`main.py:113`) | 모듈 레벨 `app = FastAPI(...)` (`main.py:83`) | `create_app()` + 모듈 `app` (`main.py:51,121`) | 모듈 레벨 `app = FastAPI(...)` (`main.py:235`) |
| `title` | `settings.api_title` = `kor-travel-geo` (`settings.py:50`) | `kor-travel-map-api` | `kor-travel-weather API` | `settings.app_name` → export본 `parking-radar` | `Pinvi API` | `Travel Concierge Admin UI API` | `Docker Manager UI API` |
| `version` | 패키지 `__version__` (export본 `0.1.0`) | 패키지 `__version__` (export본 `0.2.0-dev`) | 패키지 `__version__` (export본 `0.1.0.dev0`) | 미지정 → FastAPI 기본 `0.1.0` | 패키지 `__version__` | 하드코딩 `"0.1.0"` | 하드코딩 `"0.1.0"` |
| `description` | 없음 | 있음(ADR-005/035 언급) | 있음 | 없음 | 있음 | 있음 | 있음 |
| `servers` | 미지정 | **명시적 `servers=[]`** (ADR-031, drift 안정성 사유; `app.py:830-832`) | 미지정 | 미지정 | 미지정 | 미지정 | 미지정 |
| 응답 클래스 | `ORJSONResponse` 기본 | 기본 JSONResponse | 기본 | 기본 | 기본 | 기본 | 기본 |
| docs/openapi 경로 | `/v1/docs`, `/v1/openapi.json` (`app.py:158-159`) | 기본 경로; **production에서 `docs_url`/`redoc_url` = None** (`app.py:819-820`) | 기본 | `enable_api_docs` 설정으로 3개 모두 on/off (`main.py:155-157`, 기본 True) | `/docs`, `/redoc` 고정 | 기본 | 기본 |
| OpenAPI 버전(export본) | 3.1.0 | 3.1.0 | 3.1.0 | 3.1.0 | (export 없음) | (export 없음) | (export 없음) |
| 경로 수(export본) | 108 | 161 (admin) / 29 (user) / 27 (service) | 16 | 21 | 미확인 | 미확인 | 미확인 |

사실: `servers`를 커밋 산출물에 넣지 않는 것은 7개 앱 모두 동일한 결과(map만 의도적으로 명문화).

### 2.2 라우터 prefix · 태그 · 버전 정책

| 항목 | geo | map | weather | airport | pinvi | concierge | ktdm |
|---|---|---|---|---|---|---|---|
| 버전 prefix | `/v1`(VWorld 호환) + `/v2`(provider 중립, POST 고정) 병존 (`app.py:166-175`) | 전 표면 `/v1` (admin/ops 포함, ADR-048) | `/v1/weather`, `/v1/admin` (`routers/weather.py:26-27`) | `/v1` 단일 router (`main.py:1012`, ADR-005) | **버전 없음** (`api_router = APIRouter()`; `docs/api/common.md` §13 "v1.0 단계 prefix `/`") | `/api/v1` (`routes.py:82-84`) | `/api/v1` (`main.py:264-267`) |
| 비버저닝 예외 | `/metrics` | `/health`, `/version`, `/metrics` | `/health`, `/version`, `/metrics` | `/health` | (전부 비버저닝) | `/`, `/health`, `/metrics` | `/health`, `/metrics` |
| 라우터 분할 | 기능별 11개 모듈, prefix는 include 시 지정 | 30여 모듈, `include_router(prefix="/v1", dependencies=[...])`로 principal별 게이트 | 2 router(공개/admin) | 단일 `APIRouter()` 안에 admin 경로 혼재 (`/v1/admin/*`) | 도메인별 router에 prefix 부여(`/trips`, `/trips/{trip_id}/pois`, `/users/me`, `/auth/oauth` …) | 단일 router + 전역 `Depends(require_api_key)` | auth/admin/containers/ws 4 router |
| 태그 | 라우터별 단일 태그(`health`,`address`,`search`,`zipcode`,`pobox`,`admin`,`ops`+`dagster`,`v2`,`v2-dataset`) | 라우터별 kebab-case(`admin-*`,`ops-*`,`service-*`,`features`,`public` …, 32종) | `weather`,`admin`,`system` | **태그 없음**(export본 `tags` 전부 null) | 라우터별(`auth`,`trips`,`pois`,`features`,`geo`,`regions`,`public`,`mcp`,`webhooks` …) | 미확인(`tags=` 미검출) | `auth`,`admin`,`containers`,`websocket` |
| 최상위 `tags` 메타데이터 | 없음 | 없음 | 없음 | 없음 | 미확인 | 미확인 | 미확인 |
| 경로 분류 레지스트리 | 없음 | **`route_policy.py`**: 모든 route를 6 정책(public-unauthenticated/public-keyed/service/operator/debug/metrics)으로 등록, 기동 시 배선 검증 | 없음 | 없음 | 없음 | `READ_SCOPE_EXACT_PATHS` deny-by-default 목록 (`security.py:34-49`) | 없음 |
| 버전 승격 정책 | v1(호환)·v2(중립) 동시 제공, ADR-038/060 | pre-1.0 in-place; GA 후 `/v2` + major별 export 파일 (`export_openapi.py:56-59`) | 미확인 | 무-호환 clean cut (ADR-005) | `Deprecation`/`Sunset` 헤더 사용 예정(문서) | "필요 시 `/api/v2` router 추가" 주석 | 미확인 |

### 2.3 operationId 규약

| 항목 | 전 앱 공통 |
|---|---|
| 생성 규칙 | 사실: 7개 앱 모두 FastAPI 기본(`{함수명}_{경로}_{메서드}`)을 그대로 쓴다. `generate_unique_id_function` 사용처 없음(전 저장소 `rg` 0건). 예: geo `geocode_v2_v2_geocode_post`, map `get_public_health_health_get`, weather `list_locations_v1_weather_locations_get`, airport `airports_v1_airports_get`. |
| 소비처 | 사실: geo UI(`types/api.gen.ts`), map admin(`src/api/types.ts`), map user-client(`src/types.ts`)는 모두 `paths`/`components["schemas"]` 타입만 쓰고 operationId는 참조하지 않는다. weather는 `custom_openapi`에서 `operationId.split("_")[0]`을 mutation 판별에 사용(`app.py:247-258`) — 유일한 내부 소비처. |
| 의미 | 후보: 어떤 앱도 operationId를 외부 계약으로 쓰지 않으므로 공통 규칙 도입 비용이 낮다(weather의 내부 사용은 함수명 접두 규칙을 유지하면 무영향). |

### 2.4 인증 스킴과 OpenAPI `securitySchemes`

| 항목 | geo | map | weather | airport | pinvi | concierge | ktdm |
|---|---|---|---|---|---|---|---|
| 공개 read 인증 | `X-KTG-API-Key` 헤더 또는 VWorld 호환 `?key=` (`public_api_key.py:23-45`); 신뢰 proxy 컨텍스트면 통과 | `X-Kor-Travel-Map-Api-Key` 헤더(`?key=`는 T-VN-H01로 제거) 또는 ServiceToken | 없음(공개 read 무인증) | 없음 | 없음(공개 `/public/*`), 사용자 경로는 세션 | `X-API-Key` 헤더(정적 admin 키·DB 발급 read 키) 또는 DB read 키 `?key=` | 없음(현재 공개 surface 없음; `require_public_api_key`는 `/metrics` opt-in 게이트에만) |
| 서버 간 토큰 | 없음(공개 키가 서버 간 용도 겸함) | `X-Kor-Travel-Map-Service-Token` (`ServiceToken`), `X-Kor-Travel-Map-Ops-Token`+`X-Kor-Travel-Map-Ops-Scope` (`OpsToken`+`OpsScope`) | `x-admin-token` (`AdminToken`) | 없음 | 발신측: map ServiceToken/OpsToken 헤더 상수 보유(`clients/kor_travel_map*.py`) | 정적 `X-API-Key` (admin scope) | 없음 |
| 관리자(브라우저) 인증 | Next.js proxy가 주입하는 `x-ktg-actor`/`x-ktg-roles`/`x-ktg-admin-proxy-secret` + peer CIDR (`security.py:104-106`) | `X-Kor-Travel-Map-Admin-Proxy-Secret`+`X-Kor-Travel-Map-Actor`+CIDR (`AdminBFF`), 수동 생성 전용 `AdminFeatureCreateBFF` | admin UI BFF가 `x-admin-token` 주입 (`frontend/app/api/weather/[...path]/route.ts`, 추정) | 없음(admin 경로 무인증; ADR-005 "인증은 범위 밖") | 쿠키 `pinvi_access`(JWT)/`pinvi_refresh` HttpOnly SameSite=Lax; 모바일은 `Authorization: Bearer` (`deps.py:44-60`) | `X-KTC-Admin-Proxy-Secret`+`X-KTC-Actor`+CIDR (`security.py:29-30,186-206`) | 서명 쿠키 `ktdm_admin_session` HttpOnly SameSite=strict + Origin 검사 (`auth_service.py:20,145-163`) |
| metrics 인증 | 없음(추정; `/metrics` 에 의존성 없음, GeoIP 게이트는 적용) | `Authorization: Bearer <metrics_token>`; production 미설정 시 403 (`auth.py:963-1000`) | `Authorization: Bearer` 또는 `x-metrics-token` (`app.py:167-190`) | metrics 없음 | 미확인 | `X-API-Key`(전용 키) 또는 forwarded 헤더 없는 loopback (`security.py:218-245`) | `KTDM_METRICS_REQUIRE_KEY=1`일 때만 `?key=` |
| `securitySchemes` 선언 | **없음**(export본 `securitySchemes: None`); 키는 `Header()`/`Query()` 파라미터로만 노출 | `APIKeyHeader(..., scheme_name=...)`+`Security` 자동 선언 6종, `OpsScope`/`PublicApiKey`/`AdminFeatureCreateBFF`는 수동 주입, per-operation `security`는 route policy matrix로 계산 (`app.py:396-480`) | `custom_openapi`가 `AdminToken` 1종 수동 주입, `/v1/admin/*`에 `security` 부여 (`app.py:223-243`) | 없음 | 미확인(export 없음; `Cookie()`/`Header()` 파라미터 방식이라 추정 없음) | `APIKeyHeader` + `Security` → 자동 선언(scheme 이름은 기본값, 미확인) | 추정 없음(`request.cookies` 직접 읽음) |
| OpenAPI `x-` 확장 | 없음 | `x-required-service-scope` (`openapi_extra`, `curation_snapshots.py:299,341,438`, `cache_target_streams.py:704,782`) | 없음 | 없음 | 미확인 | 미확인 | 미확인 |

사실: 헤더 이름 접두 규칙이 앱마다 다르다 — geo `X-KTG-*`, map `X-Kor-Travel-Map-*`, concierge `X-KTC-*`, weather 소문자 `x-admin-token`. "관리자 BFF가 actor + proxy secret + CIDR로 백엔드에 신원을 넘긴다"는 구조는 geo·map·concierge 3곳에 같은 모양으로 구현돼 있다(각각 별도 코드).

### 2.5 에러 응답 envelope · HTTP 상태 매핑 · 예외 핸들러

| 항목 | geo | map | weather | airport | pinvi | concierge | ktdm |
|---|---|---|---|---|---|---|---|
| 본문 형식 | **경로별 3종**: v1 VWorld error object / v2 `{status:"ERROR", query_id, error:{code,message,hint?,field?}}` / legacy `{response:{status:"ERROR",errorCode,errorMessage,hint?}}` (`responses.py:52-95`) | RFC 7807 `application/problem+json` `{type:"https://kor-travel-map/errors/<code-kebab>", title, status, detail, code, request_id, errors[], details?}` (`app.py:648-681`) | RFC 7807 `Problem{type:"about:blank", title, status, detail, code, request_id, errors[]}` (`response.py:79-88`, `app.py:54-70`) | RFC 7807 `{type:"about:blank", title:<HTTP phrase>, status, detail, instance:<path>}`; `code`/`request_id` 없음 (`main.py:160-195`) | `{error:{code, message, details?}}` (`core/errors.py:25-32`) | FastAPI 기본 `{detail}`; 일부 409/400은 `detail={code,message,...}` dict (`routes.py:318-327,3210-3226`) | FastAPI 기본 `{detail}`; 배포 계약 오류 3종만 `{detail, request_id}` (`main.py:323-357`) |
| media type | `application/json` | `application/problem+json` | `application/problem+json` | `application/problem+json` | `application/json` | `application/json` | `application/json` |
| 기계 코드 체계 | `E0100`…`E0503` 클래스 상수 + `http_status` (`exceptions.py:6-84`) | 상태→`UPPER_SNAKE` 사전(`_ERROR_CODE_BY_STATUS`, `app.py:127-140`) + 도메인 코드 | `HTTP_ERROR`/`VALIDATION_ERROR` 2종만 | 없음 | 상태→코드 사전(`TOKEN_INVALID`,`PERMISSION_DENIED`,`RESOURCE_NOT_FOUND`,`VERSION_CONFLICT`,`RATE_LIMITED`,`VALIDATION_ERROR`,`SERVICE_UNAVAILABLE`,`INTERNAL_ERROR`; `errors.py:63-74`) + 도메인 코드 | 소문자 snake(`invalid_cursor`,`invalid_params`, 후보 충돌 코드) | 대문자 문자열 detail(`AUTH_REQUIRED`,`INVALID_API_KEY`) + dict code |
| 검증 오류 | **400**(FastAPI 422 억제, ADR-061); OpenAPI에서 422 제거하고 400 envelope 선언 (`app.py:205-260`) | 422 `VALIDATION_ERROR`, `errors`=pydantic 원본 (`app.py:881-906`) | 422 `VALIDATION_ERROR`, `_safe_errors`로 loc/msg/type만 (`app.py:33-50`) | 422, `detail`=errors 배열 | 422, `details.errors` (`_json_safe`) | 기본 422 `HTTPValidationError` | 기본 422 |
| 처리되지 않은 예외 | 미확인(등록 핸들러 없음; DBAPIError/TimeoutError는 503/500 도메인 오류로 변환) | `Exception` 핸들러 → 500 `INTERNAL_ERROR` problem+json, 스택은 로그만 (`app.py:1035-1067`) | 없음(추정 Starlette 기본 text/plain 500) | 없음 | `Exception` 핸들러(보안 헤더 유지, `main.py:105-109`) | 없음 | 없음 |
| 등록 핸들러 | `KorTravelGeoError`, `StarletteHTTPException`, `SQLAlchemyTimeoutError`, `DBAPIError`, `RequestValidationError`, pydantic `ValidationError` | `StarletteHTTPException`, `RequestValidationError`, 도메인 command 4종, geo client 2종, `CacheTargetStreamConflict`, `SubtypeDetailError`, `Exception` | `HTTPException`, `RequestValidationError` | `HTTPException`, `RequestValidationError` | `HTTPException`, `RequestValidationError`, `Exception` | 없음 | 배포 계약 오류 3종 |
| OpenAPI 상 에러 선언 | v2: `V2ErrorEnvelope` 400/401; legacy: `LegacyErrorEnvelope` 400/401 주입; VWorld: `VWorldErrorEnvelope` | 모든 4xx/5xx + `default`를 `ProblemDetail`로 주입, `HTTPValidationError` 제거 (`app.py:358-393`) | `/v1/*` 422, admin 401, `{id}` 경로 404, mutation 409를 `Problem`으로 주입 | **불일치**: 와이어는 problem+json, 스펙은 FastAPI 기본 `HTTPValidationError` 422만 | 미확인 | 미확인 | 미확인 |
| 요청 ID 헤더 | 입력 `x-request-id`/`traceparent`를 admin 컨텍스트에 읽음(`security.py:174-175`); 응답 헤더 미확인 | `X-Request-ID` 수신 시 재사용, 없으면 uuid4 발급, 응답에 설정 (`app.py:1069-1081`, `response.py:115-123`) | `x-request-id` 수신/발급 + `x-duration-ms` (`app.py:103-127`) | 없음 | `X-Request-Id` 수신/발급 (`middleware/request_id.py`) | 없음 | **항상 서버 발급**(클라이언트 값 불신, 스푸핑 방지; `main.py:243-262`), CORS `expose_headers` |

### 2.6 페이지네이션 · 정렬 · 필터

| 항목 | geo | map | weather | airport | pinvi | concierge | ktdm |
|---|---|---|---|---|---|---|---|
| 요청 파라미터 | v1/v2 search: `page`+`size`(기본 10, 최대 100; `dto/common.py:85-87`); admin: `limit`(기본 50~500, 최대 최대 5000) 다수; 일부 `page`/`page_size`/`order_by` (`admin.py:2618-2621`); v2 dataset history: `limit`+`cursor` | **`page_size`+opaque `cursor`** 표준(ADR-048, `rest-api.md` §1.6); bounded top-N만 `limit`(최대 500) | `limit`(최대 1000)+`offset` (`routers/weather.py:388-391,722-723`) | 목록 페이지네이션 없음; 분석 `days`/`limit` 상한 | `limit`+`cursor` 기본, Admin 일부 `page`+`limit` (`docs/api/common.md` §5) | `limit`+`cursor`; 범위 밖 `limit`는 422, cursor 훼손은 400 `invalid_cursor` (`docs/list-api-contract.md`) | `limit`(최대 500) |
| 응답 필드 | search: `total`; dataset: `next_cursor`; dagster: `event_cursor`+`event_has_more` | `meta.page{page_size, next_cursor(null=끝), total?}`; `total`은 `include_total=true` opt-in | `meta.page{limit, offset, returned, total?}` (`response.py:15-21`) | 없음 | `meta{cursor, has_more, total?, page?, limit?, version?}` (`schemas/envelope.py`); admin 일부 스키마는 `next_cursor` 필드 사용(`schemas/admin.py:503,609`) — 문서와 이름 불일치 | `{items, next_cursor, has_more, total, newest_id, newer_than}`; feature export는 `{items,next_cursor,has_more}` | 없음 |
| cursor 무결성 | 미확인 | feature search cursor = `base64url(payload).base64url(hmac_sha256)`, query fingerprint 포함, 위조 시 `FEATURE_SEARCH_CURSOR_TAMPERED` 422 (`rest-api.md` §1.6.1, `features.py:105-127`) | 해당 없음 | 해당 없음 | opaque base64 JSON(문서) | versioned JSON + endpoint/sort/filter SHA-256 fingerprint, 재사용 시 400 | 해당 없음 |
| 캡 정책 | 엔드포인트별 상이(100/200/500/1000/2000/5000) | 2-tier: 기본 50/최대 200, 지도 100/최대 500 | 100~5000 상이 | 16/100 | 기본 20/최대 100; admin `limit ∈ {50,100,200,500}` | endpoint별(20/100~500, 2000) | 100/500 |
| 정렬 | `order_by` 문자열 1곳 | `sort`(Literal enum `name|updated_at|created_at|kind|provider|issue_count`) + `order` `asc|desc` (`admin_features.py:128-136`) | 없음 | 없음 | 문서 §7 존재, 상세 미확인 | `sort`(`latest|mention_count|name|category`, 프론트 타입 기준; 백엔드 파라미터명 추정) | 없음 |
| 필터 규약 | 미확인 | 다중값은 단수 반복(`?kind=a&kind=b`), lifecycle은 `status`, 범위 `min_*/max_*`, 시각 `*_from/*_to`, 자유 검색 `q` (`rest-api.md` §1.9) | `search`, `enabled`(schema 제외) | `airport_code`, `parking_lot_id`, `days`, `interval_minutes` | 미확인 | filter는 cursor fingerprint에 포함 | `role`, `event_type`, `outcome`, `refresh` |

### 2.7 시간 · 좌표 · 단위

| 항목 | geo | map | weather | airport | pinvi | concierge | ktdm |
|---|---|---|---|---|---|---|---|
| 좌표 필드명 | v1 `Point{x=lon, y=lat}` (`dto/common.py:71-75`); v2 입력 `lon`/`lat`(ADR-060 §7: 출력 `{x,y}`→`{lon,lat}`는 최하위 breaking) | 평면 `lon`/`lat`; bbox는 float 4개 `min_lon,min_lat,max_lon,max_lat` (`features.py:972-975`, `rest-api.md` §1.8) | query `lat`/`lon`(ge 33~43 / 124~132), body `latitude`/`longitude` (`routers/weather.py:232-233,493-494`) | 좌표 없음 | `(lon, lat)` 순서, `{"lon","lat"}` 또는 GeoJSON; bbox 문서 예시는 `sw_lng,sw_lat,ne_lng,ne_lat` (`docs/api/common.md` §4.2) | `latitude`/`longitude`(±90/±180) (`routes.py:176-197`) | 좌표 없음 |
| SRID/CRS | `EPSG:4326` 정규화(`normalize_crs`), 한국 범위 `123<lon<132, 32<lat<39` | 4326 (ADR-012) | 4326 추정(범위 검증만) | — | EPSG:4326(문서) | 미확인 | — |
| 거리 단위 | v2 반경 `_m`/`_km` suffix 규약(ADR-060 §7) | `_m`/`_km` 규약(추정, rest-api.md) | `radius_km` | — | 미확인 | 미확인 | — |
| 시간 표현 | `ServiceMeta.time: str`(VWorld 호환); DTO `datetime` 기본 직렬화(tz 정책 미확인) | ISO 8601 KST-aware(`rest-api.md` §1.8); `AwareDatetime` 사용 1곳 | `from`/`to`는 **tz-aware 필수**(validator, `routers/weather.py:262-264`); `meta.generated_at`은 KST ISO (`response.py:59`) | 저장·직렬화 UTC(`serialize_utc` 12회), 표시용 `Asia/Seoul`; 날짜 파라미터는 문자열 | UTC 저장 → 응답 ISO 8601 + offset; offset 없는 입력은 KST 해석(문서 §4.1) | `.isoformat()` 직렬화(tz-aware 여부 미확인) | DB naive UTC(`_time.py`), 응답 직렬화 미확인 |

### 2.8 ETag · 조건부 요청 · 멱등성

| 항목 | geo | map | weather | airport | pinvi | concierge | ktdm |
|---|---|---|---|---|---|---|---|
| ETag | 없음(HTTP ETag 미사용; S3 part etag만) | strong ETag `"<row_revision>"` (`http_revision.py:14-17`, `admin_features.py:1129-1130`); public GET `If-None-Match`/304, CORS가 `ETag` 노출 (`cors.py:71-76`) | 없음 | 없음 | 없음(소비자로서 map ETag 사용) | 없음 | 없음 |
| 낙관적 동시성 | 없음 | correction PATCH `If-Match` 필수: 누락 428, 형식 오류 422, 불일치 412 (`admin_features.py:1252-1268`); `GET /v1/admin/features/{id}/revision`이 correction용 ETag 제공(`openapi-admin-contract.md:238`) | 없음 | 없음 | `If-Match: <int version>`(따옴표 없는 정수) → 불일치 **409 `VERSION_CONFLICT`** (`pois.py:194-215`, `trips.py:487`); admin feature request는 412 (`admin/features.py:94`) | 후보 revision 충돌은 409 dict detail (`CandidateRevisionConflictError`) | 없음 |
| Idempotency-Key | 없음 | UUID `Idempotency-Key`; 재생 시 `Idempotency-Replayed: true`, fingerprint 불일치 409 `IDEMPOTENCY_KEY_REUSED` (`app.py:908-953`, `domain_command_registry.py`) | 없음 | 없음 | 소비자로서 map 쪽에 전송 | 없음 | 없음 |

### 2.9 rate limit · 과부하 응답

| 항목 | geo | map | weather | airport | pinvi | concierge | ktdm |
|---|---|---|---|---|---|---|---|
| 방식 | 동시성 admission control → 429 `E0200` + `Retry-After: 1` + `Cache-Control: no-store` (`app.py:585-598`); pool 포화는 503 | 429 `TOO_MANY_REQUESTS`; 잠금 경합 409 `LOCK_BUSY`+`Retry-After`; 문서상 `RateLimit-*` 헤더(구현 미확인) | API 전역 제한 없음; admin 로그인 rate-limit bucket 엔드포인트(BFF용) | 수동 수집이 상류 quota 초과 시 429 문자열 detail | 전역 `RateLimitMiddleware`(memory/Postgres fixed window) → 429 `RATE_LIMITED`/`RATE_LIMIT_BLOCKED` + `Retry-After`, CORS `expose_headers=["Retry-After"]` | 없음 | 로그인·비밀번호 변경 429 + `Retry-After` |

### 2.10 health · ready · metrics 경로

| 항목 | geo | map | weather | airport | pinvi | concierge | ktdm |
|---|---|---|---|---|---|---|---|
| liveness | `/v1/healthz` → `{status:"ok"}` | `/health` → `{data:{status,service}, meta}` | `/health` → `{status,service,version}` | `/health` → `{status,database,seeded,release_sha}` (**DB 질의 포함**, 순수 liveness 아님) | `/health` | `/health` → `{status:"ok"}` (+ `/` 환영 메시지) | `/health` → `{status:"healthy",service}` |
| readiness | `/v1/readyz` → `ReadinessResponse{status,ready,degraded,components}`; 저하 시 503 | `/v1/ops/health-deep`(operator 인증) | 없음 | 없음 | `/health/db`, `/health/cache-target-sync`, `/health/feature-reference-reconciliation`(503 모델 선언) | 없음 | 없음 |
| version | 없음(OpenAPI `info.version`만) | `/version` → `{data:{version,kor_travel_map_version,openapi_version,commit}}` | `/version` → `{service,version,git_commit}` | `/health.release_sha` | 없음 | 없음 | 없음 |
| Prometheus | `/metrics`(schema 제외) | `settings.prometheus_metrics_path`(기본 `/metrics`, schema 제외, Bearer) + `/v1/ops/metrics` JSON | `/metrics`(schema 제외, token) | 없음 | `settings.pinvi_prometheus_metrics_path`(schema 제외) | `/metrics`(schema 제외, key/loopback) | `/metrics`(schema 제외, opt-in key) |

### 2.11 OpenAPI export · CI drift 검사 · 프론트 타입 생성

| 항목 | geo | map | weather | airport | pinvi | concierge | ktdm |
|---|---|---|---|---|---|---|---|
| export 스크립트 | `scripts/export_openapi.py` (`--output`, `--check`; `sort_keys=True`, `ensure_ascii=False`) | `packages/kor-travel-map-api/scripts/export_openapi.py` (`--profile admin/user/service/all`, `--check`; 미참조 schema·securityScheme 가지치기, user profile에 raw 필드 금지 목록) | `packages/kor-travel-weather-api/scripts/export_openapi.py` (`--check` 없음; `KOR_TRAVEL_WEATHER_ENV=development` 강제) | `scripts/export_openapi.py` (인메모리 SQLite 설정으로 export; `--check` 없음) | **없음**(vendored map 스펙 3종만 `apps/api/tests/contract/`) | **없음** | **없음** |
| 저장 위치 | 저장소 루트 `openapi.json` | `packages/kor-travel-map-api/openapi.json`·`openapi.user.json`·`openapi.service.json` | `packages/kor-travel-weather-api/openapi.json` | `docs/openapi.json` | — | — | — |
| CI drift | `.github/workflows/openapi.yml`: `export_openapi.py --check` (PR/push main) | `.github/workflows/openapi.yml`: `--profile all --check`; `tests/test_openapi_contract_is_the_production_surface.py`가 환경 의존 route의 계약 유입 차단 | `.github/workflows/ci.yml:61-66`: export 후 `git diff --exit-code` | **없음**(ADR-005가 후속 과제로 명시) | `api.yml`이 vendored map 스펙 sha256 pin 일치성 검사(소비자 측 drift) | `.github` 디렉터리 없음 | `ci.yml`은 `type-check`만 |
| 프론트 typegen | `openapi-typescript ^7.10.1`; `scripts/gen-types.mjs` → `types/api.gen.ts` + `lib/schemas.gen.ts`(schema 이름 목록); 런타임 Zod mirror는 수작업 `lib/schemas.ts`; CI `git diff --exit-code` | `openapi-typescript ^7.13.0`; admin `gen:types` → `src/api/types.ts`, `gen:types:check`; user-client `src/types.ts`; `frontend.yml`이 두 곳 `--check`; 루트 `postinstall`이 `@redocly/openapi-core` 패치 | 없음 — `frontend/lib/api.ts`에 수기 타입(`ApiEnvelope<T>`, `PageMeta`) | 없음 — `frontend/src/lib/types.ts` 수기 | 없음 — Pydantic(`apps/api/app/schemas`) ↔ Zod(`packages/schemas`) 이중 유지, `packages/api-client`가 envelope Zod로 파싱 | 없음 — `frontend/src/lib/api.ts` 수기(`ListEnvelope<T>`) | 없음 — `DashboardClient.tsx` 내 `apiJson<T>` 수기 |
| 소비자 계약 pin | — | 제공자: `contracts/vnext/openapi-diff-v1.json`에 profile별 baseline sha256 | — | — | 소비자: `tests/unit/test_kor_travel_map_contract.py`가 upstream commit + sha256을 상수로 pin, 경로·필드·타입 계약 검증 | 제공자: `docs/feature-export-api.md`(map provider가 소비) | 소비자: `c6c_deployment.py`가 map OpsToken fixture 호출 |

### 2.12 라이브러리·플랫폼 버전(설계 전제 (2) 검증용)

| 항목 | geo | map | weather | airport | pinvi | concierge | ktdm |
|---|---|---|---|---|---|---|---|
| Python | `>=3.12` | `>=3.11` | `>=3.11` | `>=3.12` | `>=3.12` | 미확인(`pyproject.toml` 없음) | 미확인 |
| fastapi 요구 | `>=0.115` | `>=0.115` | `>=0.115` | `>=0.141,<1.0` | `>=0.115` | `>=0.110.0` (`requirements.txt`) | `^0.110.0` (poetry 표기) |
| starlette 요구 | 미지정 | **`>=0.40,<1.0`** (httpx 0.x 호환 사유 주석) | 미지정 | 미지정 | 미지정 | 미지정 | 미지정 |
| pydantic 요구 | `>=2.9,<3` | `>=2.7` | `>=2.7` | 미지정(`pydantic-settings>=2.15`) | `>=2.9` | `>=2.6.4` | `^2.6.0` |
| lockfile 설치본 | 없음(`uv.lock` 미존재) | 없음(루트 `package-lock.json`만) | `uv.lock`: fastapi 0.141.1 / pydantic 2.13.5 / starlette **1.6.0** / uvicorn 0.52.4 | `backend/uv.lock`: fastapi 0.141.1 / pydantic 2.13.4 / starlette **1.6.0** | `apps/api/uv.lock`: fastapi 0.141.1 / pydantic 2.13.4 / starlette **1.6.0** / uvicorn 0.52.3 | 없음 | 없음(`poetry.lock` 미존재) |

사실: lockfile이 있는 3개 앱은 starlette 1.6.0을 설치하는데 map은 `starlette<1.0`을 명시적으로 고정한다(`packages/kor-travel-map-api/pyproject.toml:36-38`, TestClient/httpx 2.x 이슈). 버전 일치화 정책은 이 충돌을 먼저 풀어야 한다. `route_policy.py` 모듈 docstring은 FastAPI 0.136+의 lazy `_IncludedRouter` 변화를 다루므로 map은 신형 FastAPI를 이미 고려하고 있다.

## 3. 공통 OpenAPI·REST 규약 초안 (필수 / 권장 / 금지)

각 항목에 근거(현행 앱)와 도입 시 충돌 앱을 적는다. "필수"는 common 정책 채택 시 모든 백엔드가 맞춰야 하는 것, "권장"은 신규 표면과 개편 시 적용, "금지"는 신규 코드에서 막을 것.

### 3.1 필수 (MUST)

| # | 규약 | 근거(현행 사실) | 충돌 |
|---|---|---|---|
| M1 | OpenAPI 산출물을 저장소에 커밋하고, `export_openapi --check`를 CI 필수 검사로 둔다. 산출물은 `sort_keys`·`indent=2`·`ensure_ascii=False`로 결정적으로 직렬화한다. | geo/map은 `--check` + workflow, weather는 export+`git diff` 게이트. airport는 export만 있고 CI 없음(ADR-005 결과 부정 항목). | pinvi·concierge·ktdm: 산출물 자체 없음. pinvi 문서(`docs/api/README.md` §5)는 "OpenAPI export 갱신"을 요구하지만 실체가 없다. |
| M2 | `servers`는 export 산출물에 넣지 않는다(`servers=[]` 또는 export 후 제거). | map ADR-031 사유(호스트별 drift). 나머지 6앱도 결과적으로 없음. | 없음 |
| M3 | 에러 본문은 RFC 7807 `application/problem+json`으로 통일하고 확장 멤버 `code`(UPPER_SNAKE), `request_id`, `errors[]{field,message}`를 필수로 둔다. 모든 4xx/5xx와 `default`를 OpenAPI에 `ProblemDetail`로 선언하고 자동 `HTTPValidationError`는 제거한다. | map(`_error_response`+`_augment_problem_responses`), weather(`Problem`)가 이미 일치. airport는 problem+json이나 `code`/`request_id` 없음. | geo(3종 envelope, ADR-060/061), pinvi(`{error:{}}`), concierge/ktdm(`{detail}`). 마이그레이션 난이도는 §4. |
| M4 | 모든 응답에 `X-Request-ID`를 싣는다. 수신 값은 형식 검증(길이·문자 집합) 후에만 재사용하고, 아니면 서버가 발급한다. 에러 본문 `request_id`와 동일 값. | map/weather/pinvi는 echo-or-generate, ktdm은 항상 서버 발급(스푸핑 사유). | airport/concierge 미구현, geo 응답 헤더 미확인. ktdm 정책과의 절충은 "검증 통과 시에만 echo"로 둔다(후보). |
| M5 | 비버저닝 운영 경로는 `/health`(무의존 liveness), `/readyz`(의존성 점검, 저하 시 503), `/version`으로 고정하고, `/metrics`는 `include_in_schema=False` + production 토큰 필수. 나머지 업무 경로는 `/v1/...` 아래 둔다. | map(`/health`,`/version`,`/v1/ops/health-deep`), weather(`/health`,`/version`), geo(`/v1/healthz`,`/v1/readyz`). | geo는 health가 `/v1` 아래이고 이름이 `healthz`; airport `/health`가 DB를 질의; pinvi는 전 경로 비버저닝; concierge/ktdm은 `/api/v1`. |
| M6 | 좌표는 필드명 `lon`/`lat`, 배열·GeoJSON은 lon-first, EPSG:4326, bbox는 `min_lon,min_lat,max_lon,max_lat` 4개 float 파라미터. | map 표준(ADR-048), pinvi 문서, geo v2 목표(ADR-060 §7), weather query `lat`/`lon`. | geo v1 `x/y`(VWorld 호환이므로 예외 유지), weather body `latitude`/`longitude`, concierge `latitude`/`longitude`, pinvi bbox 문서 `sw_lng`. |
| M7 | 시각은 ISO 8601에 offset 포함(tz-aware). 입력은 pydantic `AwareDatetime`으로 받고 offset 없는 값은 거부한다(앱이 문서로 KST 해석을 택할 수 있으나 기본은 거부). 저장 tz는 앱 소유. | weather validator("timezone-aware ISO-8601이어야"), map §1.8, pinvi §4.1. | pinvi "offset 없으면 KST 해석"은 완화 규칙; ktdm naive UTC DB는 직렬화 시 offset 부여 필요. |
| M8 | 인증은 `components.securitySchemes`에 선언하고 operation별 `security`를 채운다(`APIKeyHeader(scheme_name=...)`+`Security`, 쿠키는 `apiKey in=cookie`). 쿠키 세션도 스펙에 선언한다. | map 6종, weather 1종. | geo(선언 없음), pinvi/concierge/ktdm(미확인·추정 없음). |
| M9 | export 산출물은 "운영이 실제로 제공하는 표면"이어야 한다. 환경 플래그에 따라 등장하는 route는 export 시 production 자세로 계산하거나 테스트로 차단한다. | map `test_openapi_contract_is_the_production_surface.py`(2026-09-03 M05 attestation 실패 사례). | weather export가 `development` 프로필 강제 — production에서 다른 표면이 노출되는지 미확인. |

### 3.2 권장 (SHOULD)

| # | 규약 | 근거 | 비고 |
|---|---|---|---|
| S1 | 성공 응답은 `{data, meta}` envelope. `meta = {request_id, duration_ms, page?}`. `data`는 payload만(목록은 `{items:[...]}`). | map `Meta`, weather `Meta`, pinvi `EnvelopeWithMeta`(키 상이). | airport는 ADR-005에서 23개 라우트 규모 때문에 명시적으로 미뤘다. geo v2는 `{status, query_id, input, ...}`(ADR-060 §3)로 별개 — geo는 예외로 두고 `query_id`↔`request_id` 대응만 문서화. |
| S2 | 목록은 cursor 페이지네이션: 요청 `page_size`+opaque `cursor`, 응답 `meta.page{page_size, next_cursor(null=끝), total?}`; `total`은 `include_total=true` opt-in. 관리자 표의 페이지 점프가 필요하면 `limit`+`offset` 변형(`meta.page{limit,offset,returned,total}`)을 허용한다. | map 표준, weather offset 변형, pinvi/concierge cursor. | 이름 충돌: `limit`(weather/pinvi/concierge/geo/ktdm) vs `page_size`(map); `has_more`(pinvi/concierge) vs `next_cursor=null`(map). 공통은 `page_size`+`next_cursor`를 택하고 `has_more`는 additive 옵션으로만 둔다(후보). |
| S3 | cursor는 opaque + 버전 + query fingerprint + HMAC 서명. 위조·재사용은 요청 처리 전 4xx. | map §1.6.1, concierge list-api-contract(fingerprint, 서명 미확인). | 상태 코드 충돌: map 422, concierge 400. |
| S4 | 정렬은 `sort`(enum)+`order`(`asc|desc`), 다중값은 단수 반복 파라미터, 자유 검색 `q`, lifecycle `status`, 범위 `min_*/max_*`, 시각 `*_from/*_to`. | map §1.9. | geo `order_by`, concierge `sort` 값 체계 상이. |
| S5 | 낙관적 동시성은 strong ETag `"<revision>"` + `If-Match`(누락 428, 불일치 412, 형식 오류 422); 조건부 GET은 `If-None-Match`/304; CORS는 `ETag`, `Retry-After`, `X-Request-ID`를 expose. | map. | pinvi는 정수 `If-Match` + 409 `VERSION_CONFLICT`(문서·클라이언트·모바일까지 고정). 전환 비용 높음 → pinvi 예외 또는 장기 과제. |
| S6 | 재시도 가능한 비멱등 POST는 UUID `Idempotency-Key`, 재생 시 `Idempotency-Replayed: true`, 본문 불일치 409. | map. | 다른 앱은 미도입; 공통 라이브러리가 제공하면 opt-in. |
| S7 | 429는 `Retry-After` 필수, 코드는 하나로 통일(`RATE_LIMITED` 또는 `TOO_MANY_REQUESTS`). | pinvi `RATE_LIMITED`, map `TOO_MANY_REQUESTS`, geo `E0200`. | 열린 질문 Q3. |
| S8 | operationId는 `{tag}_{함수명}`(또는 함수명 단독)으로 안정화하는 `generate_unique_id_function`을 공통 제공. | 현재 소비처가 없어 비용 0; weather 내부 `split("_")[0]` 판별은 함수명 접두 유지 시 무영향. | SDK 생성(hey-api 등) 도입 시 기본 operationId는 경로 변경마다 바뀌는 문제. |
| S9 | 태그는 kebab-case 라우터 단위, 최상위 `openapi_tags`로 설명 제공. | map 태그 체계. | airport 태그 없음, concierge 미확인. |
| S10 | 프론트 타입은 `openapi-typescript` 7.x를 단일 버전으로 고정, 스크립트 `gen:types`/`gen:types:check`, 출력 경로 `src/api/types.ts`(또는 `types/api.gen.ts`) 하나로 통일, CI에서 `--check`. | map 두 패키지, geo. | weather/airport/concierge/ktdm/pinvi는 수기 타입. pinvi는 Zod 이중 유지 정책이라 `openapi-typescript`가 아니라 "OpenAPI→Zod 검증 테스트"가 더 맞을 수 있음(Q5). |
| S11 | 브라우저 노출 표면에만 CORS를 적용하고, service/operator/metrics 표면은 CORS를 광고하지 않는다. | map `SurfaceScopedCORSMiddleware`. | pinvi/ktdm/concierge는 앱 전역 `allow_methods=["*"]`, `allow_headers=["*"]`. |
| S12 | production에서 `docs_url`/`redoc_url`을 끄고 `/openapi.json`은 유지한다. | map ADR-066 D-1. | airport는 설정 하나로 3개를 함께 끔(`/openapi.json`까지 사라짐). |
| S13 | 여러 principal이 있으면 profile별 export(admin/user/service)와 가지치기, user profile의 raw 필드 금지 목록을 둔다. | map `export_openapi.py --profile`. | 단일 principal 앱은 불필요. |

### 3.3 금지 (MUST NOT)

| # | 규약 | 근거 |
|---|---|---|
| N1 | 와이어와 다른 에러 스키마를 스펙에 남기지 않는다(자동 422 `HTTPValidationError`가 스펙에 있는데 실제는 400/problem+json인 상태). | airport(스펙 422 기본 스키마 vs 와이어 problem+json), geo(ADR-061 이후 422 억제 처리로 해결한 전례). |
| N2 | 신규 표면에서 API 키를 query string으로 받지 않는다. VWorld 호환 `?key=`는 문서화된 legacy 예외로만 유지. | map T-VN-H01(접근 로그·Referer 유출), geo/concierge/ktdm은 여전히 `?key=` 허용. |
| N3 | 신규 표면에서 FastAPI 기본 `{detail}` 에러 본문을 쓰지 않는다. | concierge/ktdm 현행; ktdm `request_context.py` docstring이 스스로 "routes.py는 request_id를 싣지 않는다"를 후속 항목으로 기록. |
| N4 | pydantic 검증 오류의 `input`/`ctx`/`url`을 응답에 그대로 싣지 않는다. | geo ADR-061 결정 3, weather `_safe_errors`. map은 `exc.errors()` 원본을 실음(pydantic 2.x는 기본적으로 `input`을 포함하므로 검토 필요, 추정). |
| N5 | 신규 표면에서 `x`/`y`, `lng`, `latitude`/`longitude` 혼용을 만들지 않는다. | geo v1(VWorld 호환 예외), pinvi bbox 문서 `sw_lng`, weather/concierge body. |
| N6 | 환경 플래그에 따라 있다 없다 하는 route를 커밋 산출물에 넣지 않는다. | map M05 사례. |
| N7 | 커밋 산출물에 호스트별 `servers`를 넣지 않는다. | ADR-031. |
| N8 | liveness `/health`에서 DB 등 외부 의존성을 호출하지 않는다(readiness로 분리). | map public_status docstring, airport `/health`는 DB count 질의. |

## 4. 기존 계약과의 충돌 및 마이그레이션 난이도

난이도: 낮음 = 라우터·핸들러 수정만으로 소비자 무영향, 중간 = 소비자(프론트/타 서비스) 동시 변경 필요하나 단일 저장소, 높음 = 외부 소비자·모바일·pin된 계약까지 변경.

| 앱 | 충돌 항목 | 난이도 | 근거·설명 |
|---|---|---|---|
| map | 거의 없음. `type` URI 접두(`https://kor-travel-map/errors/`)와 `TOO_MANY_REQUESTS` 코드명, `starlette<1.0` 고정만 조정 대상. | 낮음 | 공통 규약의 원형이 map이다. 단, pinvi·docker-manager가 sha256으로 pin한 계약이므로 산출물이 바뀌면 소비자 pin 갱신(`contracts/kor-travel-map-service-provenance-v1.json`, pinvi `test_kor_travel_map_contract.py`)이 뒤따른다. |
| weather | `Problem.code`가 `HTTP_ERROR` 1종; `type`이 `about:blank`; offset 페이지네이션; body 좌표명 `latitude/longitude`; `x-admin-token` 소문자 헤더; export `--check` 부재. | 낮음~중간 | 코드 매핑·`type` 변경은 additive에 가깝다. admin UI가 수기 타입(`frontend/lib/api.ts`)이라 필드 개명은 프론트 동시 수정. |
| airport | `code`/`request_id` 부재; 스펙 422 불일치; 태그·version 미지정; `/health`가 DB 질의; envelope 없음; CI drift 없음; admin 무인증. | 중간 | ADR-005가 envelope·인증을 "실제 외부 소비자가 생기면"으로 미룸. problem+json에 `code`/`request_id`를 더하는 것은 additive라 프론트 `readErrorMessage`(`detail` 읽음) 무영향. envelope 도입은 23 라우트 + 프론트 타입 전면 수정. |
| geo | 에러 envelope 3종 병존(v1 VWorld 호환은 외부 계약), 검증 오류 400, health 경로 `/v1/healthz`, 페이지네이션 3형, v1 좌표 `x/y`, `securitySchemes` 미선언, `?key=` 허용. | 높음(v1) / 중간(v2·admin) | v1은 VWorld 호환이 목적이라 공통 규약 적용 불가 → 명시적 예외. v2는 ADR-060이 이미 "배포 직전 breaking 묶음"을 예정하므로 그 묶음에 problem+json 채택 여부를 포함할 수 있다(단 `query_id` 추적 키와의 관계 정리 필요). admin은 UI(`kor-travel-geo-ui`)가 `ApiError.detail`을 읽으므로 동시 수정. |
| pinvi | `{error:{code,message}}` 형식이 `packages/schemas`(Zod `ErrorEnvelopeSchema`)·`packages/api-client`·모바일(Expo `apps/mobile/lib/api.ts`)까지 고정; 정수 `If-Match`+409; `meta.cursor/has_more`; 비버저닝 경로; 스펙 산출물 없음; bbox `sw_lng`. | 높음 | 모바일 앱 배포 주기까지 얽힌다. 현실적 순서: (1) export+CI drift(추가만), (2) `securitySchemes` 선언, (3) `X-Request-Id`·`request_id` 추가(additive), (4) envelope/에러 형식은 v2 prefix 도입 시점에 묶어서. |
| concierge | `{detail}` 기본 에러; `/api/v1` prefix; list envelope `{items,next_cursor,has_more,total,newest_id,newer_than}`(외부 read 키 소비자 존재: map provider); 소문자 코드; `.github` 부재; 스펙 산출물 없음; `latitude/longitude`. | 중간~높음 | `GET /api/v1/features/snapshot|changes`는 map의 `kor-travel-concierge-youtube` provider가 소비하는 외부 계약(`docs/feature-export-api.md`) — 변경 시 map 쪽 provider 동시 수정. 나머지는 Next BFF 단일 소비자라 중간. |
| ktdm | `{detail}` 기본 에러(3종만 `request_id`); `/api/v1`; 스펙 산출물·typegen 없음; 쿠키 세션 미선언; `?key=` metrics 게이트. | 중간 | 소비자가 자체 Next 프론트(`DashboardClient.tsx` `apiJson<T>`)뿐이라 동시 수정 가능. `X-Request-ID` "항상 서버 발급" 정책은 공통 옵션(`trust_incoming=False`)으로 수용. |

### 3.5 선행 보고서와의 대조

- 선행 보고서 §1은 "백엔드·인증까지 함께 통합할 근거는 부족하다"고 했다. 본 조사도 **런타임 공유 백엔드나 SSO 통합**에는 근거가 없다는 점에 동의한다. 그러나 **계약 규칙과 얇은 코드**(problem+json 핸들러, request-id, export/drift 스크립트, typegen 래퍼)에 대해서는 상황이 다르다: 7개 앱이 에러 본문 7종, 페이지네이션 4형, health 경로 4형, 요청 ID 정책 4형으로 갈라져 있고, 그중 map↔pinvi↔docker-manager↔concierge는 서로의 OpenAPI/REST를 sha256 pin으로 소비한다(§2.11). 즉 규칙 불일치가 이미 저장소 간 비용으로 나타나고 있다. 이는 사용자 전제 (4) "규칙도 common의 산출물"을 뒷받침한다.
- 선행 보고서 §5(표 "React Query hook·API 클라이언트 — 기본적으로 앱에 유지")는 유지한다. 본 조사에서 공유 후보로 보는 것은 **transport·에러 파싱 코어**(problem 파싱, `Retry-After` 파싱, Idempotency-Key 슬롯)뿐이며 query key·인증·재시도 정책은 앱 소유로 둔다(§5 C9).
- 선행 보고서는 airport와 PinVi admin을 다루지 않았다. 본 조사는 airport가 map 관행을 명시적으로 모방(ADR-005)했으나 CI 게이트가 빠져 있고, pinvi는 문서상 export 정책이 있으나 산출물이 없다는 사실을 추가한다(사용자 전제 (3) 포함 근거).

## 5. common 제공 가능 코드 후보와 각 앱 도입 시 변경점

패키지 이름은 후보다(예: Python `kor_travel_common`, npm `@kor-travel/...`). 모든 후보는 "앱 → common" 단방향 의존을 지키고 도메인 모듈을 import하지 않는다(선행 보고서 §5 원칙과 동일).

| # | 후보 | 원형(사실) | 제공 내용(후보) | 앱별 도입 변경점 |
|---|---|---|---|---|
| C1 | `fastapi.problem` — `ProblemDetail`/`ProblemDetailError` 모델, `register_problem_handlers(app, *, type_base, code_by_status, include_validation_input=False)`, `augment_openapi_problem_responses(schema)` | map `app.py` `_error_response`/`_http_error_payload`/`_augment_problem_responses`/`_build_problem_components`, `response.py` `ProblemDetail`; weather `Problem` | 4xx/5xx 통일 핸들러(HTTPException dict detail `{code,message,details}` 통과), 검증 오류 sanitizer(weather `_safe_errors` 방식 기본), unhandled 500 핸들러, OpenAPI 주입 | map: 거의 교체만. weather: `Problem`→공통 모델, `HTTP_ERROR`→상태 사전. airport: additive(`code`,`request_id`) + 스펙 정합. geo: v2/admin만, v1 VWorld 경로는 앱 핸들러 우선(경로 prefix 제외 옵션 필요). pinvi/concierge/ktdm: breaking(§4). |
| C2 | `fastapi.request_id` — `RequestIdMiddleware(header="X-Request-ID", trust_incoming=True, validator=...)`, contextvar, logging `Filter`, `current_request_id()` | map `attach_request_id`+`bind_request_id`; weather `request_context`; pinvi `RequestIdMiddleware`(structlog 바인딩); ktdm `_assign_request_id`+`RequestIdLogFilter` | 순수 ASGI 미들웨어 + 로깅 필터 + structlog 선택 훅 | 4개 앱은 교체, airport/concierge/geo는 신규 추가. ktdm은 `trust_incoming=False`. |
| C3 | `fastapi.envelope` — `Meta`, `PageMeta`(cursor형/offset형 두 변형), `Envelope[T]`, `make_meta(started_at, request, page=...)` | map `response.py`, weather `response.py`, pinvi `schemas/envelope.py` | pydantic v2 제네릭 모델 + `perf_counter` 기반 `duration_ms` | map: `cluster` 확장 필드는 앱 서브클래스. weather: `generated_at`은 앱 확장. pinvi: 키 이름 전환은 §4 조건부. airport/geo: 신규 표면부터. |
| C4 | `fastapi.pagination` — `CursorPageParams`(`page_size`, `cursor`) 의존성, `OffsetPageParams`(`limit`,`offset`), opaque cursor 코덱(`version`+`fingerprint`+HMAC-SHA256, `compare_digest`), keyset 헬퍼 | map `features.py` search cursor(§1.6.1), concierge `services/list_pagination`(fingerprint·watermark), pinvi/geo dataset cursor | 코덱은 저장소 독립(payload dict만 다룸); 위조·불일치 예외 타입을 C1 코드로 매핑 | map: 자체 코덱을 공통으로 치환 가능(서명 키 회전 정책 동일). concierge: 400↔422 코드 선택 필요. 나머지는 신규. |
| C5 | `fastapi.security` — (a) `api_key_header_dependency(header_name, *, scheme_name, resolver, allow_query_param=None)`: `APIKeyHeader`+`Security`로 `securitySchemes` 자동 선언, `hmac.compare_digest` (b) `trusted_proxy_actor_dependency(actor_header, secret_header, roles_header=None, cidrs=...)` (c) `metrics_bearer_dependency(token_getter, *, fail_closed_in_production)` (d) `PublicApiKeyHasher`(sha256, hint, `matches`) | (a) map `_service_token_scheme`, weather `require_admin`, concierge `api_key_header`; (b) geo `security.py`, map `require_admin_frontend`, concierge `resolve_admin_proxy_actor`; (c) map `require_metrics_token`, weather `/metrics`; (d) geo `infra/public_api_keys`, map `infra/public_api_keys`, concierge `public_api_key_service`, ktdm `public_api_key_service` | 헤더 이름은 앱이 주입(접두 `X-KTG-`, `X-Kor-Travel-Map-` 유지 가능), 검증 로직·OpenAPI 선언·에러 코드만 공통 | geo: securitySchemes가 생기는 것 자체가 스펙 변경(typegen 재생성). 세션 쿠키(pinvi/ktdm)는 범위 밖(앱 소유; 선행 보고서 §4 인증 결론 유지). |
| C6 | `fastapi.health` — `health_router(service_name, version, commit_env, readiness_checks=[...])`: `/health`, `/version`, `/readyz` | map `public_status.py`, geo `healthz.py` `ReadinessResponse`, weather `/health`/`/version` | 응답 모델 공통(`{data,meta}` 여부는 옵션) | geo `/v1/healthz`→`/health` 이동은 배포 probe 설정 변경 동반. airport `/health`의 DB 검사는 `/readyz`로 이동. |
| C7 | `openapi.export` CLI — `python -m kor_travel_common.openapi export --app pkg.module:app --output path [--check] [--profile name --policy-attr ...] [--prune]` + `customize_openapi(app, drop_auto_422=..., inject_security=...)` | geo `scripts/export_openapi.py`(`--check`), map(`--profile`, prune, forbidden props), weather/airport(단순 export) | 결정적 직렬화, `--check` 종료 코드, profile 필터는 콜백으로 주입 | 4개 앱은 스크립트 교체, pinvi/concierge/ktdm은 신규. map은 route policy 기반 profile 콜백 유지. |
| C8 | GitHub 재사용 워크플로/composite action — `openapi-drift`(python 설치→`--check`), `typegen-drift`(`npm run gen:types:check`) | geo `openapi.yml`+`ci.yml` frontend job, map `openapi.yml`+`frontend.yml`, weather `ci.yml:61-66` | `uses: digitie/kor-travel-common/.github/workflows/openapi-drift.yml@<tag>` 형태(후보) | concierge는 `.github` 신설. |
| C9 | `@kor-travel/openapi-typegen` — 고정 버전 `openapi-typescript` 래퍼 스크립트(`gen`/`check`), schema 이름 목록 export 옵션(geo `schemas.gen.ts` 방식), 필요 시 redocly 패치 포함 여부 검토 | geo `scripts/gen-types.mjs`, map `gen:types`/`gen:types:check`, map 루트 `patch-redocly-openapi-core.mjs` | 출력 경로·헤더 주석 표준화 | weather/airport/concierge/ktdm admin: 수기 타입 → 생성 타입 전환(점진: 생성본과 수기 타입의 호환 assert부터). pinvi: Zod 정책과의 관계는 Q5. |
| C10 | `@kor-travel/api-client-core` — fetch 래퍼 코어: problem+json 파싱→`ApiError{code,status,requestId,details,retryAfterSeconds}`, `Retry-After` 파싱, 타임아웃(status 0 구분), Idempotency-Key 슬롯 | map admin `client.ts`(ApiClientError, idempotency 슬롯), pinvi `api-client/client.ts`(ApiError, timeout 계약), geo `lib/api.ts`(ApiError.detail), airport `api.ts`(ApiError) | query key·인증·캐시 무효화는 앱 소유(선행 보고서 유지) | 각 앱 `ApiError` 형태가 다르므로 어댑터 단계 필요. |
| C11 | 규칙 문서 — `docs/conventions/rest-api.md`(본 §3), `docs/conventions/openapi-export.md`, 헤더 이름 레지스트리(`X-<App>-Actor` 등 접두 표) | map `docs/architecture/rest-api.md`, geo `docs/api-reference/v2/conventions.md`, pinvi `docs/api/common.md`, concierge `docs/list-api-contract.md`, airport ADR-005 | 각 앱 ADR이 common 문서를 참조하고 예외를 명시하는 구조 | — |

도입 순서 후보: C7+C8(산출물·게이트, 무-breaking) → C2(request id) → C1(에러; map/weather/airport 우선) → C5/C6 → C3/C4(신규 표면부터) → C9/C10.

## 6. 열린 질문

- Q1. geo v1(VWorld 호환)과 v2(`{status, query_id, ...}`) envelope를 공통 규약의 "문서화된 예외"로 둘지, v2 배포 전 breaking 묶음(ADR-060 §9)에 problem+json 채택을 넣을지. `query_id`와 `request_id`를 같은 값으로 둘 수 있는지 미확인.
- Q2. 검증 오류 상태 코드: 6개 앱 422 vs geo 400(ADR-061 사용자 결정). 공통은 422로 두고 geo만 예외로 할지.
- Q3. 429 코드명 `RATE_LIMITED`(pinvi) vs `TOO_MANY_REQUESTS`(map) vs `E0200`(geo). 상태→코드 사전 자체를 common이 소유할지, 앱이 덮어쓸지.
- Q4. pinvi의 정수 `If-Match`+409와 map의 strong ETag `If-Match`+412/428. 모바일 배포 주기를 고려한 전환 시점이 있는지.
- Q5. pinvi의 Pydantic↔Zod 이중 유지 정책과 `openapi-typescript` 생성 타입의 관계. "OpenAPI에서 Zod를 생성"할지, "Zod가 OpenAPI 산출물과 일치하는지 검증하는 테스트"만 둘지.
- Q6. 버전 prefix: `/v1`(geo/map/weather/airport) vs `/api/v1`(concierge/ktdm) vs `/`(pinvi). BFF proxy 뒤에 있는 앱은 외부 경로가 프론트 route handler에서 정해지므로 백엔드 prefix 통일의 실익이 어디까지인지.
- Q7. starlette 버전 정책: map의 `starlette<1.0` 고정 사유(TestClient/httpx 2.x)가 지금도 유효한지. 다른 3개 앱은 starlette 1.6.0을 설치한다.
- Q8. concierge·ktdm·geo·map에 Python lockfile이 없다. 버전 일치화 정책의 검증 단위를 lockfile로 할지 Docker 이미지 라벨로 할지.
- Q9. `X-Request-ID` 수신 값 신뢰 정책(ktdm "불신" vs 나머지 "echo"). 검증 규칙(uuid/ulid, 최대 길이)만 공통으로 두면 양쪽을 수용할 수 있는지.
- Q10. map의 `x-required-service-scope` 확장을 공통 확장 어휘(`x-kor-travel-*`)로 승격할지.
- Q11. metrics 인증: Bearer(map/weather), `X-API-Key`(concierge), `?key=`(ktdm), 없음(geo 추정). Prometheus scrape 설정 호환을 고려한 단일 방식.
- Q12. pinvi `securitySchemes`·에러 선언은 export 산출물이 없어 미확인이다. 실제 `app.openapi()` 결과를 확인하려면 실행이 필요하다(본 조사는 읽기 전용).

## 7. 근거 파일 목록 (저장소 상대 경로)

kor-travel-geo (`1d9d74d`):
1. `src/kortravelgeo/api/app.py` (150-260, 585-598)
2. `src/kortravelgeo/api/responses.py` (1-190)
3. `src/kortravelgeo/api/public_api_key.py` (1-66)
4. `src/kortravelgeo/api/security.py` (1-60, 104-106, 165-175)
5. `src/kortravelgeo/api/routers/healthz.py` (22-35)
6. `src/kortravelgeo/api/routers/v2.py` (24-35)
7. `src/kortravelgeo/api/routers/admin.py` (211, 231, 2618-2621)
8. `src/kortravelgeo/api/middleware/geoip_gate.py` (69-76)
9. `src/kortravelgeo/exceptions.py` (6-84)
10. `src/kortravelgeo/dto/common.py` (16-18, 60-87)
11. `src/kortravelgeo/dto/v2.py` (329-363)
12. `src/kortravelgeo/settings.py` (50)
13. `scripts/export_openapi.py`
14. `tests/unit/test_openapi_export.py`
15. `openapi.json` (info/securitySchemes/operationId 추출)
16. `.github/workflows/openapi.yml`, `.github/workflows/ci.yml` (40-62)
17. `kor-travel-geo-ui/package.json` (14, 48), `kor-travel-geo-ui/scripts/gen-types.mjs`, `kor-travel-geo-ui/lib/schemas.gen.ts`, `kor-travel-geo-ui/lib/api.ts` (1-40)
18. `docs/adr/060-v2-api-conventions-dimensions-additive-first.md`, `docs/adr/061-global-validation-error-structured-400-envelope.md`, `docs/api-reference/v2/conventions.md`
19. `pyproject.toml` (10, 23-41)
20. `docs/kor-travel-common-library-review.md` (선행 보고서)

kor-travel-map (`c494e227`):
21. `packages/kor-travel-map-api/src/kortravelmap/api/app.py` (127-140, 200-480, 606-681, 790-1381)
22. `packages/kor-travel-map-api/src/kortravelmap/api/auth.py` (1-16, 83-158, 963-1000)
23. `packages/kor-travel-map-api/src/kortravelmap/api/response.py`
24. `packages/kor-travel-map-api/src/kortravelmap/api/http_revision.py`
25. `packages/kor-travel-map-api/src/kortravelmap/api/route_policy.py` (1-80)
26. `packages/kor-travel-map-api/src/kortravelmap/api/cors.py` (71-76)
27. `packages/kor-travel-map-api/src/kortravelmap/api/routers/public_status.py`
28. `packages/kor-travel-map-api/src/kortravelmap/api/routers/features.py` (105-127, 972-1010)
29. `packages/kor-travel-map-api/src/kortravelmap/api/routers/admin_features.py` (128-136, 1129-1130, 1252-1268, 1574-1576)
30. `packages/kor-travel-map-api/src/kortravelmap/api/routers/curation_snapshots.py` (299, 341, 438), `.../routers/cache_target_streams.py` (704, 782)
31. `packages/kor-travel-map-api/scripts/export_openapi.py` (1-140)
32. `packages/kor-travel-map-api/openapi.json`, `openapi.user.json`, `openapi.service.json`
33. `packages/kor-travel-map-api/tests/test_openapi_contract_is_the_production_surface.py` (1-50)
34. `packages/kor-travel-map-api/pyproject.toml` (10, 34-41)
35. `packages/kor-travel-map-admin/frontend/package.json` (14-15, 63), `packages/kor-travel-map-admin/frontend/src/api/client.ts` (1-30), `src/api/types.ts` (헤더)
36. `packages/kor-travel-map-user-client/package.json` (30-35), `packages/kor-travel-map-user-client/README.md`
37. `.github/workflows/openapi.yml`, `.github/workflows/frontend.yml` (74-89)
38. `docs/architecture/rest-api.md` (§0-§1.9), `docs/architecture/openapi-admin-contract.md` (§1-§3, 238), `docs/adr/048-*.md`, `docs/adr/079-openapi-digest-not-pinned-in-compatible-pair.md`, `docs/adr/README.md` (47)
39. `contracts/vnext/openapi-diff-v1.json`, `scripts/patch-redocly-openapi-core.mjs`, `package.json` (36-43)

kor-travel-weather (`6003da9`):
40. `packages/kor-travel-weather-api/src/kortravelweather_api/app.py`
41. `packages/kor-travel-weather-api/src/kortravelweather_api/auth.py`
42. `packages/kor-travel-weather-api/src/kortravelweather_api/response.py`
43. `packages/kor-travel-weather-api/src/kortravelweather_api/routers/weather.py` (26-27, 232-264, 384-496, 713-745)
44. `packages/kor-travel-weather-api/scripts/export_openapi.py`, `packages/kor-travel-weather-api/openapi.json`
45. `packages/kor-travel-weather-admin/frontend/lib/api.ts` (1-60)
46. `.github/workflows/ci.yml` (61-66), `pyproject.toml`, `packages/kor-travel-weather-api/pyproject.toml`, `uv.lock`, `docs/weather-api.md`, `src/kortravelweather/models.py` (240-241)

kor-travel-airport (`2bb1111`):
47. `backend/app/main.py` (1-320, 692-712, 1012)
48. `backend/app/core/time_utils.py`, `backend/app/core/config.py` (36-58), `backend/app/schemas.py` (292-297)
49. `scripts/export_openapi.py`, `docs/openapi.json`
50. `docs/adr/005-versioned-rest-api-contract.md`
51. `.github/workflows/ci.yml`, `backend/pyproject.toml` (9-19), `backend/uv.lock`
52. `frontend/src/lib/api.ts` (1-60), `frontend/src/lib/types.ts` (1-30)

pinvi (`9af25e5`):
53. `apps/api/app/main.py`
54. `apps/api/app/core/errors.py`, `apps/api/app/core/deps.py` (33-120), `apps/api/app/core/session_cookies.py`
55. `apps/api/app/middleware/request_id.py`, `apps/api/app/middleware/rate_limit.py` (155-250)
56. `apps/api/app/api/v1/__init__.py`, `apps/api/app/api/v1/healthz.py` (28-36, 153-156), `apps/api/app/api/v1/pois.py` (38, 185-215), `apps/api/app/api/v1/trips.py` (480-500), `apps/api/app/mcp/auth.py` (20-50)
57. `apps/api/app/schemas/envelope.py`, `apps/api/app/schemas/geo.py` (1-40), `apps/api/app/schemas/admin.py` (503, 609)
58. `apps/api/app/clients/kor_travel_map.py` (37), `apps/api/app/clients/kor_travel_map_admin.py` (55-58)
59. `apps/api/tests/unit/test_kor_travel_map_contract.py` (1-60), `apps/api/tests/contract/*.json`
60. `.github/workflows/api.yml` (278-349), `apps/api/pyproject.toml` (5-12), `apps/api/uv.lock`
61. `docs/api/README.md`, `docs/api/common.md` (§3-§8, §12-§13), `docs/conventions/coding-style.md` (§2.4)
62. `packages/api-client/package.json`, `packages/api-client/src/client.ts` (1-60), `packages/schemas/src/` (목록)

kor-travel-concierge (`7945305`):
63. `backend/main.py`
64. `backend/ktc/api/routes.py` (60-100, 300-327, 3205-3260)
65. `backend/ktc/core/security.py` (1-245)
66. `backend/requirements.txt` (1, 12-13)
67. `docs/list-api-contract.md`, `docs/feature-export-api.md`
68. `frontend/src/lib/api.ts` (1-70)

kor-travel-docker-manager (`862562d`):
69. `backend/src/kor_travel_docker_manager/main.py` (1-50, 200-396)
70. `backend/src/kor_travel_docker_manager/api/security.py`, `api/auth.py` (22), `api/admin.py` (27-58), `api/routes.py` (68)
71. `backend/src/kor_travel_docker_manager/services/auth_service.py` (20, 120-165), `services/public_api_key_service.py` (1-60)
72. `backend/src/kor_travel_docker_manager/request_context.py`, `_time.py`
73. `backend/pyproject.toml` (11-15), `.github/workflows/ci.yml` (49)
74. `frontend/src/components/DashboardClient.tsx` (97-820, `apiJson` 호출부)

기타:
75. `F:/dev/canview` — 구조 참조만(`AGENTS.md`/`SKILL.md`/`docs`). OpenAPI 관련 내용 없음(`rg` 0건).
