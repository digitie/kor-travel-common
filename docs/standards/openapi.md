# kor-travel-common OpenAPI·REST 규약

이 문서는 [규칙 문서 색인](README.md)에 속한 7개 FastAPI 백엔드 공통 REST/OpenAPI 규약의 정본이다. 정본 지위: **확정 초안** — [브리프](../plan/design-brief.md) D-14를 규칙 ID로 옮긴 것이며, 실물 도구(T-303 export CLI·T-309 drift 워크플로)와 소비자 채택(T-480~T-486)에서 대조해 확정하는 task가 남아 있다. 확정 task: T-301. 마지막 갱신: 2026-09-09.

규칙 ID `M1~M9`(MUST)·`S1~S13`(SHOULD)·`N1~N8`(MUST NOT)은 조사 문서 [openapi 횡단 비교](../survey/cross/openapi.md) §3의 번호를 그대로 쓴다. common이 보강한 하위 규칙은 `M3.1`처럼 점 번호를 붙였고, `M10`은 [ADR-009](../adr/009-openapi-rest-conventions.md) 결정 7의 교차 저장소 MUST다. 예외는 [openapi-exceptions.yaml](openapi-exceptions.yaml)에만 등록한다.

## 1. 목표와 기준

- 7개 백엔드(geo·map·weather·airport·pinvi·concierge·ktdm)는 에러 본문 7종, 페이지네이션 4형, health 경로 4형, 요청 ID 정책 4형으로 갈라져 있고, map↔pinvi↔ktdm↔concierge는 서로의 OpenAPI 산출물을 sha256 pin으로 소비한다(사실: `oa` §2.5·§2.6·§2.10·§2.11·§3.5). 규약 불일치가 이미 저장소 간 비용으로 나타나므로 규칙은 코드보다 먼저 배포한다.
- 원형은 map(`packages/kor-travel-map-api`)이다. map이 이미 지키는 규칙은 map 기준으로 문장을 고정했고, map만 조정하는 항목은 `type` URI·429 코드·`starlette<1.0` 셋뿐이다(`oa` §4).
- 기존 계약을 깨지 않는다. 신규 표면에는 MUST, 기존 표면에는 SHOULD + 예외 등록으로 적용 강도를 나눈다(§3). 예외에는 반드시 `review` 날짜가 있고, `sunset: null`은 "무기한"이지 "검토 면제"가 아니다.
- 인증 서버·사용자 데이터·운영 정책은 이 규약의 범위 밖이다. 공통은 로그인 UI/인증 프리미티브의 계약과 `securitySchemes` 선언 형식·헤더 이름 형식을 정하며, 저장소·키·역할 정책은 앱이 주입한다([ADR-015](../adr/015-common-shared-systems-scope.md), T-312).

## 2. 문서 사용법

| 변경 대상 | 상세 정본 |
|---|---|
| 규칙의 적용 강도(즉시/신규/기존)와 예외 등록 | 이 문서 §3·§6 |
| 예외 항목의 실제 값 | [openapi-exceptions.yaml](openapi-exceptions.yaml) |
| Python 구현(export CLI·health·request-id·problem 핸들러·time) | [backend-stack](backend-stack.md) §5·§8 |
| drift·typegen CI 워크플로 계약 | [ci-deploy](ci-deploy.md) §3 |
| `openapi-typescript` 버전 값 | [versions](versions.md)·`versions.json` |
| 소비 저장소 매니페스트의 `openapi.exceptions` 항목 | [consumer adoption](../runbooks/consumer-adoption.md) |
| 결정 이유 | [ADR-009](../adr/009-openapi-rest-conventions.md)([ADR 색인](../adr/README.md)) |
| 현행 앱별 사실 | [openapi 횡단 비교](../survey/cross/openapi.md) §2·§4 |

용어: **표면**(surface) = 한 앱이 한 principal에게 노출하는 경로 집합(예: map `admin`/`user`/`service` profile, geo `/v1`·`/v2`). **신규 표면** = 새 앱, 새 버전 prefix, 새 라우터 모듈. **기존 표면** = 조사 기준 커밋([survey README](../survey/README.md) §2.1)에 존재하는 경로.

## 3. 적용 계층

| 계층 | 규칙 | 적용 | 근거 |
|---|---|---|---|
| 1. 즉시 MUST | M2·M4·M9·N6·N7 | 모든 표면. 응답 본문을 바꾸지 않는 additive 변경이므로 예외는 task 완료 시점까지의 기한부(`sunset` 필수)만 허용 | D-14; `oa` §3.1 M2·M4·M9, §3.3 N6·N7 |
| 2. 신규 MUST · 기존 SHOULD + 예외 | M1·M3·M5·M6·M7·M8·N1~N5·N8 | 신규 표면은 MUST. 기존 표면은 SHOULD이며 미준수 항목을 `openapi-exceptions.yaml`에 등록(`sunset` null 허용, `review` 필수) | D-14; `oa` §4 앱별 난이도 |
| 3. SHOULD | S1~S13 | 신규 표면과 개편 시 적용. 미준수는 예외 등록 없이도 허용하되 소비자 매니페스트에 "미채택"으로 보고 | D-14; `oa` §3.2 |

`M10`은 응답 형식을 바꾸는 즉시 적용 규칙이 아니라 map 산출물과 이를 sha256으로 고정한 소비자 저장소의 PR 순서를 묶는 **교차 저장소 MUST**다. map 산출물을 바꾸는 PR은 pinvi·ktdm pin 갱신 evidence를 함께 제시해야 하며, common이 소비자 저장소를 직접 수정하지 않는다.

계층 2에서 "기존 표면 SHOULD"는 검사에서 report만 내고 fail하지 않는다. fail 승격은 `versions.json`의 `consumers.<repo>.enforce`가 소유하는 3단 강제 수준(D-07·D-30)을 따른다.

## 4. 규칙

### 4.1 MUST

| ID | 계층 | 규칙 | 현행 근거 | 검사 수단 | 예외 여부 | 정합 task |
|---|---|---|---|---|---|---|
| M1 | 신규 MUST·기존 SHOULD+예외 | OpenAPI 산출물을 저장소에 커밋하고 `export --check`를 CI 필수 검사로 둔다. 직렬화는 결정적이어야 한다: `sort_keys=True`, `indent=2`, `ensure_ascii=False`, 파일 끝 개행 1개. 저장 위치는 앱(또는 API 패키지) 루트 `openapi.json`, profile이 있으면 `openapi.<profile>.json` | geo·map `--check` + workflow, weather export + `git diff`(`oa` §2.11) | `export --check` 결정적 산출물·drift 검사 | 기존 표면 미준수는 YAML 예외 등록 | 도구 T-303, 워크플로 T-309, pinvi T-484·concierge T-485·ktdm T-486 파이프라인 신설 |
| M2 | 즉시 MUST | `servers`를 산출물에 넣지 않는다(`servers=[]` 또는 export 후 제거) | 7개 앱 모두 결과적으로 없음, map ADR-031 명문화(`oa` §2.1) | `servers` 부재 정적 검사 | 없음 | 없음 |
| M3 | 신규 MUST·기존 SHOULD+예외 | 에러 본문은 RFC 7807 `application/problem+json`이며 확장 멤버 `code`(UPPER_SNAKE), `request_id`, `errors[]{field,message}`를 필수로 둔다. 모든 4xx/5xx와 `default`를 `ProblemDetail`로 선언하고 자동 `HTTPValidationError`는 제거한다 | map·weather 일치, airport는 `code`/`request_id` 없음(`oa` §2.5) | problem+json 스키마·응답 계약 검사 | 기존 표면은 YAML 예외 등록 | airport T-482(additive), geo v2/admin T-483(opt-in), pinvi·concierge·ktdm은 breaking 묶음(§6 예외) |
| M3.1 | 신규 MUST·기존 SHOULD+예외 | 검증 오류 상태 코드는 **422** 기본이다. geo의 400(ADR-061)은 등록된 예외다 | 6개 앱 422 vs geo 400(`oa` Q2) | 검증 오류 상태 코드 계약 검사 | geo 400은 YAML 예외 등록 | geo 예외 등록(무기한) |
| M3.2 | 신규 MUST·기존 SHOULD+예외 | `type`은 `about:blank`(기본) 또는 앱이 소유하는 안정 URI다. URI를 쓰면 코드별로 값이 변하지 않아야 하고 앱 문서에서 해석 가능해야 한다(후보: 형식은 T-480에서 map `https://kor-travel-map/errors/<code-kebab>`와 정렬하며 확정) | map URI·weather `about:blank`(`oa` §2.5) | `type` URI 안정성 계약 검사 | 앱 소유 URI는 YAML 예외 등록 | T-480 |
| M3.3 | 신규 MUST·기존 SHOULD+예외 | `errors[]` 항목은 `field`(경로 문자열, 예 `body.lat`)와 `message`만 필수이며 pydantic `loc`/`msg`/`type`은 그 둘로 정규화한다. `input`/`ctx`/`url`은 싣지 않는다(N4) | weather `_safe_errors`, geo ADR-061(`oa` N4) | `errors[]` 정규화·민감 입력 회귀 검사 | 기존 원문 노출은 YAML 예외 등록 | T-303(C5 핸들러 기본값) |
| M4 | 즉시 MUST | 모든 응답에 `X-Request-ID` 헤더를 싣는다. 수신 값은 M4.1 형식 검증을 통과했을 때만 재사용하고 아니면 서버가 발급한다. 에러 본문 `request_id`와 같은 값이며 로그에 바인딩한다 | map·weather·pinvi echo-or-generate, ktdm 서버 발급(`oa` §2.5) | `X-Request-ID` 미들웨어·응답 헤더 검사 | 기존 미구현은 기한부 YAML 예외 등록 | airport T-482·concierge T-485·geo T-483 신규, ktdm T-486(`trust_incoming=False`) |
| M4.1 | 신규 MUST·기존 SHOULD+예외 | 형식: UUID v4/v7(하이픈 포함 36자) 또는 ULID(Crockford base32 26자). 128자 이하의 인쇄 가능 ASCII만 허용하고 공백·제어 문자가 있으면 무효로 본다. 서버 발급 기본은 UUID v4(v7 허용). 수신 값을 무조건 버리는 `trust_incoming=False`는 앱 옵션이다(ktdm 스푸핑 방지 근거). 응답 헤더 표기는 `X-Request-ID`이고 수신은 대소문자를 구분하지 않는다. CORS는 이 헤더를 expose한다 | D-14; `oa` Q9 | 요청 ID validator 단위·헤더 노출 검사 | 형식 예외 불가; `trust_incoming`만 앱 옵션 | T-307(C2) |
| M5 | 신규 MUST·기존 SHOULD+예외 | 비버저닝 운영 경로는 `/health`(외부 의존 없는 liveness), `/readyz`(의존성 점검, 저하 시 503), `/version`으로 고정한다. `/metrics`는 `include_in_schema=False` + production 토큰 필수. 나머지 업무 경로는 `/v1/...` 아래 둔다. `/health` 응답은 최소 `{status, service}`, `/version`은 `{service, version, commit}`, `/readyz`는 `{status, ready, components[]}`(geo `ReadinessResponse` 형태)를 SHOULD로 둔다. geo `/v1/healthz`·`/v1/readyz`는 별칭으로 병행하며 소비자 probe·Prometheus 갱신 확인 전까지 무기한 예외다 | map·weather `/health`·`/version`, geo `/v1/healthz`·`/v1/readyz`(`oa` §2.10; `be` §2.5) | health·readyz·version export 계약 검사 | 기존 health alias는 YAML 예외 등록 | T-304(C4, alias 옵션), airport `/health` DB 질의는 `/readyz`로 T-482 |
| M5.1 | 신규 MUST·기존 SHOULD+예외 | 버전 prefix는 신규 앱·신규 표면에서 `/v1`이다. 기존 `/api/v1`(concierge·ktdm)과 pinvi 비버저닝 경로는 등록된 예외이며, BFF 뒤에 있는 앱은 외부 경로가 프론트 route handler에서 정해지므로 `sunset: null`을 허용한다 | `oa` §2.2·Q6 | prefix·alias 경로 계약 검사 | 기존 prefix·비버저닝은 YAML 예외 등록 | 없음(예외 유지) |
| M6 | 신규 MUST·기존 SHOULD+예외 | 좌표 필드명은 `lon`/`lat`, 배열·GeoJSON은 lon-first, CRS는 EPSG:4326, bbox는 `min_lon,min_lat,max_lon,max_lat` 4개 float 파라미터 | map ADR-048, pinvi 문서, geo v2 목표(`oa` §2.7) | 좌표·bbox 스키마 정적 검사 | legacy 좌표명은 YAML 예외 등록 | geo v1 `x/y` 예외, weather·concierge body 이름 예외 |
| M7 | 신규 MUST·기존 SHOULD+예외 | 시각은 ISO 8601 offset 포함(tz-aware). 입력은 pydantic `AwareDatetime`으로 받고 offset 없는 값은 거부한다. 앱이 문서로 "offset 없으면 KST 해석"을 택할 수 있으나(pinvi) 기본은 거부다. 저장 tz는 앱 소유 | weather validator, map §1.8, pinvi §4.1(`oa` §2.7) | AwareDatetime·offset 회귀 검사 | 앱 저장·해석 차이는 YAML 예외 등록 | T-304(C13), ktdm naive UTC 예외 |
| M8 | 신규 MUST·기존 SHOULD+예외 | 인증은 `components.securitySchemes`에 선언하고 operation별 `security`를 채운다(`APIKeyHeader(scheme_name=...)` + `Security`). 쿠키 세션도 `apiKey in=cookie`로 선언한다 | map 6종·weather 1종(`oa` §2.4) | securitySchemes·operation security export 검사 | 기존 security 선언 누락은 YAML 예외 등록 | geo T-483(typegen 재생성 동반), pinvi T-484, concierge T-485, ktdm T-486 |
| M8.1 | 신규 MUST·기존 SHOULD+예외 | 앱 고유 헤더 이름은 `X-<AppId>-<Purpose>` 형식이다. `<Purpose>` 어휘는 `Api-Key`, `Service-Token`, `Actor`, `Admin-Proxy-Secret`, `Ops-Token`, `Ops-Scope` 여섯 가지다. `<AppId>`는 풀네임(`Kor-Travel-Map`)이든 약어(`KTG`·`KTC`)든 앱이 소유하되 앱당 하나만 쓴다(D-22). 공통 헤더 `X-Request-ID`·`Idempotency-Key`·`If-Match`·`Retry-After`·`ETag`는 접두를 붙이지 않는다. 어휘 밖 Purpose는 예외 등록 | geo `X-KTG-*`, map `X-Kor-Travel-Map-*`, concierge `X-KTC-*`, weather 소문자 `x-admin-token`(`oa` §2.4) | 헤더 이름 정적·OpenAPI 검사 | Purpose 위반은 YAML 예외 등록 | weather `x-admin-token` 예외 |
| M9 | 즉시 MUST | export 산출물은 운영이 실제로 제공하는 표면이다. 환경 플래그에 따라 등장하는 route는 export 시 production 자세로 계산하거나 테스트로 차단한다 | map `test_openapi_contract_is_the_production_surface.py`(`oa` §3.1 M9) | production 표면 export 회귀 검사 | weather export 환경 고정은 YAML 예외 등록 | weather export `development` 강제 → T-481 재검증 |
| M10 | 교차 저장소 MUST | map OpenAPI 산출물(`openapi.json`·`openapi.user.json`·`openapi.service.json`) 변경은 pinvi·ktdm의 sha256 pin 갱신 PR을 동반하지 않으면 머지하지 않는다. common은 이 pin 계약을 흡수하지 않는다(매트릭스 B10) | pinvi `test_kor_travel_map_contract.py`, ktdm runtime pin(`oa` §2.11; [매트릭스](../survey/commonality-matrix.md) §4.1 B10) | map 산출물 pin 일치 PR review | pin 갱신 evidence가 동반돼야 함 | T-480 |

### 4.2 SHOULD

| ID | 계층 | 규칙 | 현행 근거 | 검사 수단 | 예외 여부 | 비고 |
|---|---|---|---|---|---|---|
| S1 | SHOULD | 성공 응답은 `{data, meta}` envelope. `meta = {request_id, duration_ms, page?}`, `data`는 payload만(목록은 `{items:[...]}`) | map·weather `Meta`, pinvi `EnvelopeWithMeta`(`oa` §3.2) | envelope 계약 테스트 | 미채택은 예외가 아니라 매니페스트에 기록 | geo v2 `{status, query_id, ...}`는 예외(`query_id`↔`request_id` 대응만 문서화). airport는 ADR-005로 유보 |
| S2 | SHOULD | 목록은 cursor 페이지네이션: 요청 `page_size`+opaque `cursor`, 응답 `meta.page{page_size, next_cursor(null=끝), total?}`, `total`은 `include_total=true` opt-in. 관리자 표의 페이지 점프에는 `limit`+`offset` 변형(`meta.page{limit,offset,returned,total}`)을 허용한다. `has_more`는 additive 옵션으로만 | map 표준, weather offset, pinvi·concierge cursor(`oa` §2.6) | 페이지네이션 계약 테스트 | 형식 차이는 비고·매니페스트에 기록 | 이름 충돌은 소비자 매니페스트에 기록하며, concierge features export만 외부 계약 예외 |
| S3 | SHOULD | cursor는 opaque + 버전 + query fingerprint + HMAC 서명. 위조·재사용은 요청 처리 전 4xx이며 common 기본은 422(`CURSOR_TAMPERED`) | map §1.6.1, concierge fingerprint(`oa` §2.6) | cursor 위조·재사용 회귀 테스트 | 앱별 미채택은 비고에 기록 | concierge 400 `invalid_cursor`는 매니페스트 미채택 |
| S4 | SHOULD | 정렬은 `sort`(enum) + `order`(`asc\|desc`), 다중값은 단수 반복 파라미터, 자유 검색 `q`, lifecycle `status`, 범위 `min_*/max_*`, 시각 `*_from/*_to` | map §1.9 | query parameter 계약 검사 | 앱별 미채택은 비고에 기록 | geo `order_by`, concierge `sort` 값 체계 상이 |
| S5 | SHOULD | 낙관적 동시성은 strong ETag `"<revision>"` + `If-Match`(누락 428, 불일치 412, 형식 오류 422). 조건부 GET은 `If-None-Match`/304. CORS는 `ETag`, `Retry-After`, `X-Request-ID`를 expose | map(`oa` §2.8) | ETag·If-Match 계약 테스트 | pinvi legacy는 소비자 매니페스트 미채택 | pinvi 정수 `If-Match`+409는 모바일 배포 주기와 함께 재평가 |
| S6 | SHOULD | 재시도 가능한 비멱등 POST는 UUID `Idempotency-Key`, 재생 시 `Idempotency-Replayed: true`, 본문 불일치 409 | map | idempotency replay 계약 테스트 | 미채택은 비고에 기록 | 다른 앱은 공통 모듈 제공 후 opt-in |
| S7 | SHOULD | 429는 `Retry-After` 필수 | geo·map·pinvi·ktdm(`oa` §2.9) | 429 `Retry-After` 응답 테스트 | 미채택은 비고에 기록 | — |
| S7.1 | SHOULD | 상태→코드 사전은 common이 기본값을 소유하고 앱이 덮어쓴다. 429 기본 코드는 `TOO_MANY_REQUESTS`(O-14 기본값). 사전 항목: 400 `BAD_REQUEST`, 401 `UNAUTHORIZED`, 403 `FORBIDDEN`, 404 `NOT_FOUND`, 409 `CONFLICT`, 412 `PRECONDITION_FAILED`, 422 `VALIDATION_ERROR`, 428 `PRECONDITION_REQUIRED`, 429 `TOO_MANY_REQUESTS`, 500 `INTERNAL_ERROR`, 503 `SERVICE_UNAVAILABLE` | map `_ERROR_CODE_BY_STATUS`, pinvi 사전(`oa` §2.5·Q3) | 상태→코드 사전 계약 테스트 | 앱 코드 사전 덮어쓰기는 소비자 매니페스트 미채택 | pinvi `RATE_LIMITED`·geo `E0200`은 매니페스트에 기록 |
| S8 | SHOULD | operationId는 `generate_unique_id_function`으로 `{tag}_{함수명}`(태그 없으면 함수명)으로 안정화한다 | 7개 앱 FastAPI 기본, 외부 소비처 없음(`oa` §2.3) | operationId export 검사 | 미채택은 비고에 기록 | weather 내부 `split("_")[0]` 판별은 함수명 접두 유지 시 무영향 |
| S9 | SHOULD | 태그는 kebab-case 라우터 단위, 최상위 `openapi_tags`로 설명 제공 | map 32종 | tag·openapi_tags 검사 | 태그 누락은 소비자 매니페스트 미채택 | airport 태그 없음 |
| S10 | SHOULD | 프론트 타입은 `openapi-typescript` 7.x 단일 버전(값은 `versions.json`)으로 생성한다. 스크립트 이름 `gen:types`/`gen:types:check`, 출력 경로는 `src/api/types.ts` 또는 `types/api.gen.ts` 하나, CI에서 `gen:types:check`(생성 후 `git diff --exit-code`와 동치) | map 두 패키지, geo(`oa` §2.11) | `gen:types:check` drift 검사 | 수기 타입은 이관 task에 기록 | weather·airport·concierge·ktdm 수기 타입은 생성본과의 호환 assert부터 점진 전환 |
| S10.1 | SHOULD | pinvi의 Pydantic↔Zod 이중 유지는 "OpenAPI 산출물↔Zod 스키마 일치 테스트"로 검증한다(O-14 기본값). `openapi-typescript` 도입은 강제하지 않는다 | pinvi `packages/schemas`(`oa` Q5) | OpenAPI↔Zod 일치 테스트 | pinvi는 일치 테스트로 대체 | T-484 |
| S11 | SHOULD | CORS는 브라우저 노출 표면에만 적용하고 service/operator/metrics 표면은 CORS를 광고하지 않는다 | map `SurfaceScopedCORSMiddleware` | 표면별 CORS 회귀 테스트 | 전역 CORS는 비고에 기록 | pinvi·ktdm·concierge 전역 `*` |
| S12 | SHOULD | production에서 `docs_url`/`redoc_url`을 끄고 `/openapi.json`은 유지한다 | map ADR-066 | production docs/redoc export 검사 | 앱별 production 설정은 비고에 기록 | airport는 설정 하나로 3개를 함께 끔 |
| S13 | SHOULD | 여러 principal이 있으면 profile별 export(admin/user/service)와 미참조 schema 가지치기, user profile의 raw 필드 금지 목록을 둔다 | map `export_openapi.py --profile` | profile export·schema 가지치기 검사 | principal 없는 앱은 적용 제외 | 단일 principal 앱은 불필요 |

### 4.3 MUST NOT

| ID | 계층 | 규칙 | 근거 | 검사 수단 | 예외 여부 | 정합 task |
|---|---|---|---|---|---|---|
| N1 | 신규 MUST NOT·기존 SHOULD+예외 | 와이어와 다른 에러 스키마를 스펙에 남기지 않는다(자동 422 `HTTPValidationError`가 스펙에 있는데 실제는 problem+json인 상태) | airport 스펙-와이어 불일치(`oa` §2.5; [airport 인벤토리](../survey/inventory/kor-travel-airport.md) §4.1) | wire·OpenAPI 오류 스키마 비교 | 기존 wire drift는 YAML 예외 등록 | 해당 앱 이관 task |
| N2 | 신규 MUST NOT·기존 SHOULD+예외 | 신규 표면에서 API 키를 query string으로 받지 않는다. VWorld 호환 `?key=`는 문서화된 legacy 예외로만 | map T-VN-H01(접근 로그·Referer 유출) | query key 정적·로그 노출 검사 | VWorld legacy query key만 YAML 예외 등록 | 해당 앱 이관 task |
| N3 | 신규 MUST NOT·기존 SHOULD+예외 | 신규 표면에서 FastAPI 기본 `{detail}` 에러 본문을 쓰지 않는다 | concierge·ktdm 현행 | `detail` 오류 본문 계약 검사 | 기존 detail은 YAML 예외 등록 | 해당 앱 이관 task |
| N4 | 신규 MUST NOT·기존 SHOULD+예외 | pydantic 검증 오류의 `input`/`ctx`/`url`을 응답에 그대로 싣지 않는다 | geo ADR-061, weather `_safe_errors`; map은 원본을 실으므로 T-480에서 검토 | validation 민감 필드 제거 회귀 검사 | 기존 원문 노출은 YAML 예외 등록 | 해당 앱 이관 task |
| N5 | 신규 MUST NOT·기존 SHOULD+예외 | 신규 표면에서 `x`/`y`, `lng`, `latitude`/`longitude` 혼용을 만들지 않는다 | geo v1·pinvi bbox 문서·weather/concierge body | 좌표 필드명 lint·스키마 검사 | 기존 명칭은 YAML 예외 등록 | 해당 앱 이관 task |
| N6 | 즉시 MUST NOT | 환경 플래그에 따라 있다 없다 하는 route를 커밋 산출물에 넣지 않는다 | map M05 사례 | production export route 안정성 검사 | 없음 | 해당 앱 이관 task |
| N7 | 즉시 MUST NOT | 커밋 산출물에 호스트별 `servers`를 넣지 않는다 | map ADR-031 | `servers` 부재 export 검사 | 없음 | 해당 앱 이관 task |
| N8 | 신규 MUST NOT·기존 SHOULD+예외 | liveness `/health`에서 DB 등 외부 의존성을 호출하지 않는다(readiness로 분리) | airport `/health` DB count 질의 | health 외부 의존성 격리 테스트 | 기존 liveness DB 호출은 YAML 예외 등록 | 해당 앱 이관 task |

### 4.4 본문·헤더 예시

규칙의 형태를 고정하기 위한 예시다(값은 임의). 예시에 필드를 더하는 것은 additive이고, 예시에 있는 필드를 빼는 것은 계약 변경이다.

에러(M3·M3.1·M3.3·M4·S7.1):

```json
{
  "type": "about:blank",
  "title": "Unprocessable Entity",
  "status": 422,
  "detail": "요청 본문 검증에 실패했습니다.",
  "code": "VALIDATION_ERROR",
  "request_id": "018f6b2e-7c1a-7d3e-9a4b-2f1c0e5d8a77",
  "errors": [
    { "field": "body.lat", "message": "위도는 -90과 90 사이여야 합니다." }
  ]
}
```

성공 envelope(S1·S2):

```json
{
  "data": { "items": [ { "id": "f_01", "lon": 126.978, "lat": 37.566 } ] },
  "meta": {
    "request_id": "018f6b2e-7c1a-7d3e-9a4b-2f1c0e5d8a77",
    "duration_ms": 12,
    "page": { "page_size": 50, "next_cursor": null }
  }
}
```

운영 경로(M5; 위에서부터 `/health`·`/readyz`(503)·`/version`):

```json
{ "status": "ok", "service": "kor-travel-map-api" }
{ "status": "degraded", "ready": false, "components": [ { "name": "db", "status": "timeout", "latency_ms": 1500 } ] }
{ "service": "kor-travel-map-api", "version": "0.2.0", "commit": "c494e227" }
```

`X-Request-ID` 흐름(M4·M4.1; BFF 체인의 발급자 결정, `oa` Q9):

| 위치 | 동작 |
|---|---|
| 브라우저 → Next BFF | 브라우저가 보낸 값은 M4.1 검증을 통과할 때만 전달하고, 아니면 BFF가 발급한다 |
| BFF → 백엔드 | `X-Request-ID`를 전달한다. 백엔드는 다시 검증한 뒤 echo한다(`trust_incoming=True`) |
| `trust_incoming=False` 앱(ktdm) | 수신 값을 버리고 서버가 발급한다. 응답 헤더로 새 값을 돌려주므로 BFF 로그는 두 값을 함께 남긴다 |
| 백엔드 ↔ 타 서비스(pinvi → map) | 호출 측이 자기 요청 ID를 전달하고 응답의 `X-Request-ID`를 로그에 바인딩한다 |
| 응답 | `X-Request-ID` 헤더, 에러 본문 `request_id`, `meta.request_id`(S1)가 모두 같은 값이다 |

## 5. 앱별 적용 상태

기준 커밋은 [survey README](../survey/README.md) §2.1. 판정은 `oa` §4를 규칙 ID로 접은 것이며 실행 검증은 하지 않았다(사실은 파일 기준, 난이도는 추정).

| 앱 | 준수(변경 없음) | 예외 등록(§6) | 정합 task | 난이도 |
|---|---|---|---|---|
| map | M1·M2·M3·M4·M5·M6·M7·M8·M9·S1~S6·S8~S13 | M3.2 `type` URI, BE-3 `starlette<1.0` | T-480(`type`·429 정렬, N4 검토, pin 갱신 동반) | 낮음 |
| weather | M1(export)·M2·M3·M4·M5·S1·S2(offset 변형) | M6 body 이름, M8.1 소문자 헤더, M9 development 강제 | T-481(`--check` 전환, `HTTP_ERROR` 1종 → S7.1 사전) | 낮음~중간 |
| airport | M2·M6(좌표 없음)·M7 | M1·M3·M4·N1·N8 | T-482(`code`/`request_id` additive, 스펙 422 정합, `--check` CI, `/readyz` 분리) | 중간 |
| geo | M1·M2·M9·S8 무영향 | v1: M3·M6·N2·N5 / v2: M3·S1 / M3.1·M5·M8 | T-483(health alias 병행, securitySchemes+typegen, admin problem+json opt-in, request-id) | 높음(v1 외부 계약) / 중간(v2·admin) |
| pinvi | M2·M4·M7(문서상 KST 해석 완화) | M1·M3·M5.1·M8·N5 | T-484(export·drift 신설, request-id additive, Zod 일치 테스트) | 높음(모바일까지 고정) |
| concierge | M2 | M1·M3·M4·M5.1·M8·N2·N5·S1·S2(features export) | T-451(CI 신설)·T-485(export·request-id, features export 계약 문서화) | 중간~높음(map provider 외부 계약) |
| ktdm | M2·M4(서버 발급 = `trust_incoming=False`) | M1·M3·M5.1·M7·M8·N2 | T-486(request-id 옵션, quality) | 중간 |

### 5.1 신규 표면 체크리스트

새 앱·새 prefix·새 라우터를 만들 때 설계 단계에서 확인한다. 항목마다 규칙 ID를 적어 리뷰 evidence로 남긴다.

1. 경로는 `/v1/...` 아래이고 `/health`·`/readyz`·`/version`·`/metrics`만 비버저닝인가(M5·M5.1).
2. 에러 핸들러가 problem+json + `code`/`request_id`/`errors[]`를 내고 스펙에서 `HTTPValidationError`가 제거됐는가(M3·N1).
3. `X-Request-ID` 미들웨어가 등록됐고 로그 필터에 바인딩되는가(M4).
4. 인증 헤더 이름이 `X-<AppId>-<Purpose>`이고 `securitySchemes`에 선언됐는가(M8·M8.1). query string 키는 없는가(N2).
5. 좌표는 `lon`/`lat`·bbox 4 float·EPSG:4326, 시각은 `AwareDatetime`인가(M6·M7·N5).
6. export 스크립트가 common CLI를 쓰고 CI에 `--check`가 있는가(M1). 환경 플래그 route는 production 자세로 계산되는가(M9·N6).
7. 목록은 `page_size`+`cursor`(또는 offset 변형)이고 `meta.page` 형식인가(S2). 정렬·필터 파라미터 이름이 S4인가.
8. 프론트가 `gen:types:check`를 CI에 두는가(S10).
9. 타 저장소가 이 표면을 sha256 pin으로 소비하는가 — 그렇다면 M10 동반 PR 규칙을 PR 본문에 적는다.

## 6. 예외 레지스트리

정본은 [openapi-exceptions.yaml](openapi-exceptions.yaml) 하나다. 사람이 읽는 표 [openapi-exceptions.md](openapi-exceptions.md)는 `tools/openapi_exceptions.py`가 YAML로부터 생성하며 수기 편집하지 않는다. `--check`는 YAML 스키마·규칙 ID·날짜·생성물 drift를 함께 검사한다.

### 6.1 항목 형식

```yaml
- app: geo                       # airport | concierge | ktdm | geo | map | weather | pinvi
  rule: M3                       # 이 문서의 ID(M/S/N, 점 번호 포함) 또는 backend-stack.md의 BE-n
  surface: "/v1/*"               # 경로 접두, profile 이름, 또는 "*"(앱 전체)
  reason: "…"                    # 사실 근거와 실제 원장에 정의된 정합 task ID(T-NNN)를 반드시 포함
  sunset: null                   # ISO 날짜 또는 null(무기한). 계층 1 규칙은 null 금지
  review: 2026-12-31             # ISO 날짜. 등록일 + 6개월 이내, 분기 감사(T-506) 주기에 맞춤
  owner: kor-travel-geo          # 예외를 닫을 저장소
```

### 6.2 등록·검토 규칙

1. 예외 한 항목은 앱 하나·규칙 하나·표면 하나다. 같은 앱의 여러 규칙은 항목을 나눈다.
2. `sunset`이 지난 항목은 `check-versions`의 `EXEMPT_EXPIRED`와 같은 취급으로 CI가 `::error::`를 낸다(report 모드에서도). 연장은 새 `review`와 사유를 적은 common PR로만 한다.
3. `review`가 지난 항목은 분기 감사(T-506)에서 재판정한다. 재판정 결과는 유지(새 `review`)·축소(`surface` 좁힘)·삭제 중 하나다.
4. 소비 저장소 매니페스트 `kor-travel-common.lock.json`의 `openapi.exceptions`는 이 레지스트리에서 자기 앱 항목의 `rule`·`surface` 목록을 그대로 복사한다(D-19). 매니페스트에만 있고 레지스트리에 없는 예외는 무효다.
5. 계층 3(S1~S13) 미채택은 예외가 아니라 "미채택"이며 소비자 매니페스트에만 기록한다. 단 geo v2처럼 타 저장소가 직접 소비하거나 concierge features export처럼 변경이 타 저장소를 깨뜨리는 **외부 계약**은 구체적인 `surface`로 등록할 수 있다. 이때 `reason`에는 문장 중간 substring이 아닌 정확한 긍정 assertion `소비하는 외부 계약` 또는 `소비되는 외부 계약`을 `이다`·`임` 또는 여는 괄호로 닫고, 정합 task ID와 독립된 `M10` 또는 `동반 PR` token을 적는다. task ID는 파일명에 있는 `T-NNN[a-z]?`의 standalone token이어야 하며 `_`·한국어 문자·`.1`·`-suffix`를 붙이지 않는다. `M10`과 `동반 PR`도 identifier·점·underscore 접미사를 허용하지 않는다. 부정·불확정 근거와 예약 YAML indicator는 허용하지 않는다. `surface`는 `*`·`/*`·`/**` 같은 전역 wildcard가 아닌 구체 표면이어야 하며 validator가 이를 강제한다.
6. 초기 등록(D-14)은 geo v1·geo v2 envelope·pinvi `{error:{}}`·정수 `If-Match`+409·비버저닝 경로·concierge `/api/v1`·`{detail}`·features export·ktdm `/api/v1`·`{detail}`·airport 스펙 422 불일치·map `starlette<1.0`이며, 조사에서 확인된 나머지 미준수 항목도 같은 형식으로 함께 등록했다.

### 6.3 소비자 매니페스트 발췌

소비 저장소 `kor-travel-common.lock.json`(D-19)의 `openapi` 항목은 레지스트리의 자기 앱 항목을 `rule`·`surface`로만 복사한다(사유·기한은 레지스트리가 정본).

```json
{
  "openapi": {
    "exceptions": [
      { "rule": "M3", "surface": "/v1/*" },
      { "rule": "M5", "surface": "/v1/healthz, /v1/readyz" }
    ]
  }
}
```

`tools/collect_manifests.py`(T-012)가 레지스트리와 매니페스트를 대조해 [integration map](../integration-map.md)에 앱별 예외 수를 적는다.

## 7. 검증 gate

| gate | 명령·도구 | 실행 위치 | 실패 조건 |
|---|---|---|---|
| export drift | `python3 -m kortravelcommon.openapi export --app <module:app> --output openapi.json --check`(T-303; 현재 앱 스크립트 `scripts/export_openapi.py --check` 대체) | 앱 CI(`openapi-drift.yml`, T-309) | 산출물이 커밋본과 다름, `servers` 존재, 미참조 `HTTPValidationError` 잔존 |
| production 표면 | 환경 플래그 route 테스트(map `test_openapi_contract_is_the_production_surface.py` 형태) | 앱 테스트 | export 산출물에 플래그 route 포함 |
| typegen drift | `npm run gen:types:check` | 앱 CI(`typegen-drift.yml`, T-309) | 생성 타입이 커밋본과 다름 |
| Zod 일치 | pinvi OpenAPI↔Zod 일치 테스트 | pinvi CI | 스키마 필드·타입 불일치 |
| 예외 레지스트리 | `python -B -X utf8 tools/openapi_exceptions.py --check` | common `docs` job | 형식 오류, `sunset` 경과, 계층 1 규칙에 `sunset: null`, 생성물 drift |
| 교차 pin | pinvi `contract-pin-consistency`, ktdm runtime pin | map PR 리뷰 | M10 위반(pin 갱신 PR 미동반) |
| 규약 리뷰 | 2인 독립 리뷰([agent workflow](../runbooks/agent-workflow.md)) | common PR | 이 문서·yaml은 D-04 비면제 대상 |

도구가 통과했다는 사실은 계약 호환을 증명하지 않는다. 계약 변경은 소비자 빌드·e2e evidence를 요구한다(D-25 NOT_RUN 규칙).

## 8. 열린 결정

| # | 항목 | 기본값(이 문서가 채택) | 사용자 확인 |
|---|---|---|---|
| O-14 | 429 코드명·geo v2 problem+json 시점·pinvi Zod | `TOO_MANY_REQUESTS`; geo v2는 ADR-060 breaking 묶음에서 판정; pinvi는 일치 테스트 | 열림(사용자 확인 필요) |
| — | M3.2 `type` URI 형식 | `about:blank` 기본, 앱 URI 허용 | 후보(T-480에서 map과 정렬하며 확정) |
| — | metrics 인증 방식(Bearer/`X-API-Key`/`?key=`) | Bearer 권장, 앱 예외 등록(`oa` Q11) | 후보([backend-stack](backend-stack.md) BE-12) |
| — | map `x-required-service-scope` 확장의 공통 어휘(`x-kor-travel-*`) 승격 | 승격하지 않음(map 소유) | 후보(`oa` Q10) |

## 9. 근거

- [브리프](../plan/design-brief.md) D-14·D-15·D-19·D-22·D-25·O-14.
- [openapi 횡단 비교](../survey/cross/openapi.md) §2.1~§2.12(현행 사실), §3(규약 초안 M/S/N), §4(마이그레이션 난이도), §5(코드 후보 C1~C11), §6(열린 질문 Q1~Q12).
- [backend 횡단 비교](../survey/cross/backend.md) §2.5(health)·§2.10(에러 계층)·§2.18(export).
- [ci-deploy 횡단 비교](../survey/cross/ci-deploy.md) §1.2(OpenAPI drift 게이트)·§2.1(`openapi-drift.yml`).
- [공통화 매트릭스](../survey/commonality-matrix.md) §1.4·§2.5·§4.1 B10·§4.2 D16~D22.
- [airport 인벤토리](../survey/inventory/kor-travel-airport.md) §4.1(스펙 21 paths·422 불일치; 수치는 [survey README](../survey/README.md) §6.2 항목 4 정정값).
