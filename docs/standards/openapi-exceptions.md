<!-- SPDX-License-Identifier: GPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie) -->
# OpenAPI·REST 예외 레지스트리

> 이 문서는 [정본 YAML](openapi-exceptions.yaml)에서 생성한 읽기 전용 표다. 수기 편집하지 않는다.

- schema: `kor-travel-common.openapi-exceptions.v1`
- updated: `2026-09-06`
- apps: `airport`, `concierge`, `ktdm`, `geo`, `map`, `weather`, `pinvi`
- exceptions: **46건**

| 앱 | 규칙 | 표면 | 사유 | sunset | review | owner |
|---|---|---|---|---|---|---|
| geo | M3 | /v1/* | VWorld 호환 오류 객체(VWorldErrorEnvelope)·legacy `{response:{status,errorCode}}`는 외부 계약(oa §2.5). problem+json 적용 불가. | null | 2026-12-31 | kor-travel-geo |
| geo | M6 | /v1/* | v1 `Point{x=lon,y=lat}`는 VWorld 호환 계약(oa §2.7, geo ADR-060 §7). v2는 lon/lat 준수. | null | 2026-12-31 | kor-travel-geo |
| geo | N5 | /v1/* | M6 예외와 동일 사유(x/y 혼용은 VWorld 호환 legacy). | null | 2026-12-31 | kor-travel-geo |
| geo | N2 | /v1/* | VWorld 호환 `?key=` 공개 키 수신(oa §2.4). 문서화된 legacy 예외. 신규 표면에는 헤더 `X-KTG-API-Key`만. | null | 2026-12-31 | kor-travel-geo |
| geo | M3 | /v2/* | v2 envelope `{status:'ERROR', query_id, error:{code,message,hint,field}}`(oa §2.5). `query_id`↔`request_id` 대응을 문서화하고 problem+json 채택 여부는 ADR-060 배포 전 breaking 묶음에서 판정(O-14). | null | 2026-12-31 | kor-travel-geo |
| geo | S1 | /v2/* | v2 성공 envelope `{status, query_id, input, ...}`(oa §3.2 S1 비고). `{data, meta}` 미채택. M3 v2 항목과 같은 시점에 재판정. | null | 2026-12-31 | kor-travel-geo |
| geo | M3.1 | * | 검증 오류 400(geo ADR-061 사용자 결정, FastAPI 422 억제; oa §2.5·Q2). common 기본 422과 다름. | null | 2026-12-31 | kor-travel-geo |
| geo | M5 | /v1/healthz, /v1/readyz | health 경로가 `/v1` 아래 `healthz`(oa §2.10). `/health`·`/readyz` 도입 후에도 별칭 병행. 소비자 probe(pinvi admin/system.py, ktdm healthcheck, Prometheus scrape) 갱신 확인 전까지 무기한(D-14). T-483. | null | 2026-12-31 | kor-travel-geo |
| geo | M8 | * | export본 `securitySchemes: None`; 키는 Header()/Query() 파라미터로만 노출(oa §2.4). 선언은 스펙 변경이므로 typegen 재생성과 함께 T-483. | null | 2026-12-31 | kor-travel-geo |
| geo | S7.1 | * | 429 코드 `E0200`(admission control, oa §2.9). 앱 사전 덮어쓰기 유지. | null | 2026-12-31 | kor-travel-geo |
| pinvi | M3 | * | `{error:{code,message,details}}` envelope가 `packages/schemas` Zod ErrorEnvelopeSchema·`packages/api-client`·모바일 `apps/mobile/lib/api.ts`까지 고정(oa §2.5·§4). 전환은 v2 prefix 도입 시점에 묶음. 선행 순서: export·drift(T-484) → securitySchemes → request-id additive → envelope. | null | 2026-12-31 | pinvi |
| pinvi | S5 | /trips/*, /trips/{trip_id}/pois/* | 정수 `If-Match`(따옴표 없음) 불일치 시 409 `VERSION_CONFLICT`(oa §2.8). 문서·클라이언트·모바일까지 고정, 모바일 배포 주기 종속(oa Q4). | null | 2026-12-31 | pinvi |
| pinvi | M5.1 | * | 전 경로 비버저닝(`api_router = APIRouter()`, docs/api/common.md §13 'v1.0 단계 prefix /'; oa §2.2). BFF 뒤 표면이라 sunset null 허용. | null | 2026-12-31 | pinvi |
| pinvi | M1 | * | 자체 export 산출물·drift CI 없음(map 스펙 3종 소비자 검증만; oa §2.11). T-484에서 export 파이프라인·drift CI 신설. | null | 2026-12-31 | pinvi |
| pinvi | M8 | * | export 없음으로 securitySchemes 선언 미확인(Cookie()/Header() 파라미터 방식, oa §2.4·Q12). T-484에서 `apiKey in=cookie` 선언. | null | 2026-12-31 | pinvi |
| pinvi | S2 | * | `meta{cursor, has_more, total?, page?, limit?}`와 admin `page`+`limit`(oa §2.6); admin 일부 스키마 `next_cursor` 필드로 문서와 이름 불일치. 이름 전환은 M3 v2 시점에 묶음. | null | 2026-12-31 | pinvi |
| pinvi | N5 | docs/api/common.md §4.2 bbox | bbox 문서 예시 `sw_lng,sw_lat,ne_lng,ne_lat`(oa §2.7). 코드 표면은 (lon, lat) 준수. 문서 정정은 pinvi 소유. | null | 2026-12-31 | pinvi |
| pinvi | S7.1 | * | 429 코드 `RATE_LIMITED`·`RATE_LIMIT_BLOCKED`(RateLimitMiddleware, oa §2.9). 앱 사전 덮어쓰기 유지. | null | 2026-12-31 | pinvi |
| pinvi | S10.1 | apps/web, apps/mobile | Pydantic↔Zod 이중 유지 정책(oa Q5). `openapi-typescript` 대신 OpenAPI 산출물↔Zod 일치 테스트로 검증(O-14 기본값). T-484. | null | 2026-12-31 | pinvi |
| concierge | M5.1 | * | 버전 prefix `/api/v1`(routes.py:82-84; oa §2.2). Next BFF 뒤 표면이라 sunset null 허용. | null | 2026-12-31 | kor-travel-concierge |
| concierge | M3 | * | FastAPI 기본 `{detail}`, 일부 409/400은 `detail={code,message}` dict(oa §2.5). Next BFF 단일 소비자 + features export 외부 소비자. T-485 후 재판정. | null | 2026-12-31 | kor-travel-concierge |
| concierge | S1 | GET /api/v1/features/snapshot, GET /api/v1/features/changes | map `kor-travel-concierge-youtube` provider가 소비하는 외부 계약(docs/feature-export-api.md; oa §4). 변경 시 map provider 동시 수정 PR 동반(M10과 같은 취급). T-485. | null | 2026-12-31 | kor-travel-concierge |
| concierge | S2 | * | list envelope `{items, next_cursor, has_more, total, newest_id, newer_than}`(oa §2.6). features export는 `{items,next_cursor,has_more}`로 외부 계약. | null | 2026-12-31 | kor-travel-concierge |
| concierge | M1 | * | export 스크립트·산출물·`.github` 없음(oa §2.11). T-451 CI 신설 후 T-485에서 export·drift. | null | 2026-12-31 | kor-travel-concierge |
| concierge | M4 | * | 요청 ID 미구현(oa §2.5). 계층 1 규칙이므로 기한부. T-485에서 additive 추가. | 2026-12-31 | 2026-12-31 | kor-travel-concierge |
| concierge | M8 | * | `APIKeyHeader`+`Security` 자동 선언이나 scheme 이름은 기본값(미확인; oa §2.4). T-485에서 확인·정정. | null | 2026-12-31 | kor-travel-concierge |
| concierge | N2 | * | DB 발급 read 키 `?key=` 허용(oa §2.4). 신규 표면에는 `X-API-Key`만. | null | 2026-12-31 | kor-travel-concierge |
| concierge | N5 | * | `latitude`/`longitude` 필드(routes.py:176-197; oa §2.7). Next BFF 동시 수정 필요. | null | 2026-12-31 | kor-travel-concierge |
| concierge | S3 | * | cursor 훼손 시 400 `invalid_cursor`(docs/list-api-contract.md; oa §2.6). common 기본 422과 다름. | null | 2026-12-31 | kor-travel-concierge |
| ktdm | M5.1 | * | 버전 prefix `/api/v1`(main.py:264-267; oa §2.2). 자체 Next 프론트 단일 소비자. | null | 2026-12-31 | kor-travel-docker-manager |
| ktdm | M3 | * | FastAPI 기본 `{detail}`; 배포 계약 오류 3종만 `{detail, request_id}`(oa §2.5). `request_context.py` docstring이 후속 항목으로 기록. T-486. | null | 2026-12-31 | kor-travel-docker-manager |
| ktdm | M1 | * | export 스크립트·산출물·typegen 없음(`ci.yml`은 type-check만; oa §2.11). T-486. | null | 2026-12-31 | kor-travel-docker-manager |
| ktdm | M8 | * | 서명 쿠키 `ktdm_admin_session`을 `request.cookies`로 직접 읽어 securitySchemes 미선언(추정; oa §2.4). `apiKey in=cookie` 선언은 T-486. | null | 2026-12-31 | kor-travel-docker-manager |
| ktdm | N2 | /metrics | `KTDM_METRICS_REQUIRE_KEY=1`일 때 `?key=` 게이트(oa §2.4·Q11). Prometheus scrape 설정 종속. | null | 2026-12-31 | kor-travel-docker-manager |
| ktdm | M7 | * | DB naive UTC(`_time.py`, SQLite DateTime 호환 목적; be §2.12). 응답 직렬화 시 offset 부여 필요, 전환은 명시 결정. | null | 2026-12-31 | kor-travel-docker-manager |
| airport | N1 | * | 와이어는 problem+json, 스펙은 FastAPI 기본 `HTTPValidationError` 422(oa §2.5; inventory/kor-travel-airport.md §4.1). T-482 스펙 422 정합. | null | 2026-12-31 | kor-travel-airport |
| airport | M3 | * | `{type:'about:blank', title, status, detail, instance}`에 `code`·`request_id` 없음(oa §2.5). additive라 프론트 `readErrorMessage` 무영향. T-482. | null | 2026-12-31 | kor-travel-airport |
| airport | M4 | * | 요청 ID 미구현(oa §2.5). 계층 1 규칙이므로 기한부. T-482에서 additive 추가. | 2026-12-31 | 2026-12-31 | kor-travel-airport |
| airport | M1 | * | export만 있고 `--check`·CI drift 없음(ADR-005 후속 과제; oa §2.11). T-482에서 `--check` CI. | null | 2026-12-31 | kor-travel-airport |
| airport | N8 | /health | `/health`가 DB `count(*)` 질의 + `release_sha`(be §2.5). T-482에서 `/readyz`로 분리하고 `/health`는 무의존 liveness로. | null | 2026-12-31 | kor-travel-airport |
| airport | S9 | * | 태그 없음(export본 `tags` 전부 null), `info.version` 미지정(oa §2.1·§2.2). T-482에서 정합. | null | 2026-12-31 | kor-travel-airport |
| weather | M9 | * | export 스크립트가 `KOR_TRAVEL_WEATHER_ENV=development`를 강제(oa §2.11·M9 비고). production 표면과의 동일성 미확인. 계층 1 규칙이므로 기한부. T-481 재검증. | 2026-12-31 | 2026-12-31 | kor-travel-weather |
| weather | M8.1 | /v1/admin/* | admin 토큰 헤더가 소문자 `x-admin-token`으로 `X-<AppId>-<Purpose>` 형식 밖(oa §2.4). BFF `route.ts`가 주입하므로 이름 변경은 프론트 동반. | null | 2026-12-31 | kor-travel-weather |
| weather | M6 | POST body (routers/weather.py:493-494) | query는 `lat`/`lon` 준수, body는 `latitude`/`longitude`(oa §2.7). admin UI 수기 타입 동반 수정. | null | 2026-12-31 | kor-travel-weather |
| map | M3.2 | * | `type` = `https://kor-travel-map/errors/<code-kebab>` URI(oa §2.5). common 기본 `about:blank`와 형식 정렬은 T-480. | null | 2026-12-31 | kor-travel-map |
| map | BE-3 | packages/kor-travel-map-api | `starlette>=0.40,<1.0` 상한(TestClient/httpx 2.x 사유 주석; oa §2.12·Q7, be §2.1). airport·weather·pinvi는 starlette 1.6.0 설치. T-480 재검증 전까지 예외. versions.json exceptions[]에도 같은 항목. | null | 2026-12-31 | kor-travel-map |

검사: `python -B -X utf8 tools/openapi_exceptions.py --check`.
