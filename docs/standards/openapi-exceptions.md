<!-- SPDX-License-Identifier: GPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie) -->
# OpenAPI·REST 예외 레지스트리

> 이 문서는 [정본 YAML](openapi-exceptions.yaml)에서 생성한 읽기 전용 표다. 수기 편집하지 않는다.

- schema: `kor-travel-common.openapi-exceptions.v1`
- updated: `2026-09-06`
- apps: `airport`, `concierge`, `ktdm`, `geo`, `map`, `weather`, `pinvi`
- exceptions: **39건**

| 앱 | 규칙 | 표면 | 사유 | sunset | review | owner |
|---|---|---|---|---|---|---|
| geo | M3 | /v1/&#42; | VWorld 호환 오류 객체&#40;VWorldErrorEnvelope&#41;·legacy &#96;{response:{status,errorCode}}&#96;는 외부 계약&#40;oa §2.5&#41;. problem+json 적용 불가. geo 이관은 T-483. | null | 2026-12-31 | kor-travel-geo |
| geo | M6 | /v1/&#42; | v1 &#96;Point{x=lon,y=lat}&#96;는 VWorld 호환 계약&#40;oa §2.7, geo ADR-060 §7&#41;. v2는 lon/lat 준수. geo 이관은 T-483. | null | 2026-12-31 | kor-travel-geo |
| geo | N5 | /v1/&#42; | M6 예외와 동일 사유&#40;x/y 혼용은 VWorld 호환 legacy&#41;. geo 이관은 T-483. | null | 2026-12-31 | kor-travel-geo |
| geo | N2 | /v1/&#42; | VWorld 호환 &#96;?key=&#96; 공개 키 수신&#40;oa §2.4&#41;. 문서화된 legacy 예외. 신규 표면에는 헤더 &#96;X-KTG-API-Key&#96;만. geo 이관은 T-483. | null | 2026-12-31 | kor-travel-geo |
| geo | M3 | /v2/&#42; | v2 envelope &#96;{status:'ERROR', query&#95;id, error:{code,message,hint,field}}&#96;&#40;oa §2.5&#41;. &#96;query&#95;id&#96;↔&#96;request&#95;id&#96; 대응을 문서화하고 problem+json 채택 여부는 ADR-060 배포 전 breaking 묶음에서 판정&#40;O-14&#41;. T-483. | null | 2026-12-31 | kor-travel-geo |
| geo | S1 | /v2/&#42; | v2 성공 envelope &#96;{status, query&#95;id, input, ...}&#96;&#40;oa §3.2 S1 비고&#41;는 Pinvi가 직접 소비하는 외부 계약이다. &#96;{data, meta}&#96; 전환 시 M3 v2와 함께 재판정하며 map M10 기준 동반 PR 규칙을 적용한다. T-483. | null | 2026-12-31 | kor-travel-geo |
| geo | M3.1 | &#42; | 검증 오류 400&#40;geo ADR-061 사용자 결정, FastAPI 422 억제; oa §2.5·Q2&#41;. common 기본 422과 다름. T-483. | null | 2026-12-31 | kor-travel-geo |
| geo | M5 | /v1/healthz, /v1/readyz | health 경로가 &#96;/v1&#96; 아래 &#96;healthz&#96;&#40;oa §2.10&#41;. &#96;/health&#96;·&#96;/readyz&#96; 도입 후에도 별칭 병행. 소비자 probe&#40;pinvi admin/system.py, ktdm healthcheck, Prometheus scrape&#41; 갱신 확인 전까지 무기한&#40;D-14&#41;. T-483. | null | 2026-12-31 | kor-travel-geo |
| geo | M8 | &#42; | export본 &#96;securitySchemes: None&#96;; 키는 Header&#40;&#41;/Query&#40;&#41; 파라미터로만 노출&#40;oa §2.4&#41;. 선언은 스펙 변경이므로 typegen 재생성과 함께 T-483. | null | 2026-12-31 | kor-travel-geo |
| pinvi | M3 | &#42; | &#96;{error:{code,message,details}}&#96; envelope가 &#96;packages/schemas&#96; Zod ErrorEnvelopeSchema·&#96;packages/api-client&#96;·모바일 &#96;apps/mobile/lib/api.ts&#96;까지 고정&#40;oa §2.5·§4&#41;. 전환은 v2 prefix 도입 시점에 묶음. 선행 순서: export·drift&#40;T-484&#41; → securitySchemes → request-id additive → envelope. | null | 2026-12-31 | pinvi |
| pinvi | M5.1 | &#42; | 전 경로 비버저닝&#40;&#96;api&#95;router = APIRouter&#40;&#41;&#96;, docs/api/common.md §13 'v1.0 단계 prefix /'; oa §2.2&#41;. BFF 뒤 표면이라 sunset null 허용. T-484. | null | 2026-12-31 | pinvi |
| pinvi | M1 | &#42; | 자체 export 산출물·drift CI 없음&#40;map 스펙 3종 소비자 검증만; oa §2.11&#41;. T-484. export 파이프라인·drift CI 신설. | null | 2026-12-31 | pinvi |
| pinvi | M8 | &#42; | export 없음으로 securitySchemes 선언 미확인&#40;Cookie&#40;&#41;/Header&#40;&#41; 파라미터 방식, oa §2.4·Q12&#41;. T-484. &#96;apiKey in=cookie&#96; 선언. | null | 2026-12-31 | pinvi |
| pinvi | N5 | docs/api/common.md §4.2 bbox | bbox 문서 예시 &#96;sw&#95;lng,sw&#95;lat,ne&#95;lng,ne&#95;lat&#96;&#40;oa §2.7&#41;. 코드 표면은 &#40;lon, lat&#41; 준수. 문서 정정은 pinvi 소유. T-484. | null | 2026-12-31 | pinvi |
| concierge | M5.1 | &#42; | 버전 prefix &#96;/api/v1&#96;&#40;routes.py:82-84; oa §2.2&#41;. Next BFF 뒤 표면이라 sunset null 허용. T-485. | null | 2026-12-31 | kor-travel-concierge |
| concierge | M3 | &#42; | FastAPI 기본 &#96;{detail}&#96;, 일부 409/400은 &#96;detail={code,message}&#96; dict&#40;oa §2.5&#41;. Next BFF 단일 소비자 + features export 외부 소비자. T-485 후 재판정. | null | 2026-12-31 | kor-travel-concierge |
| concierge | S1 | GET /api/v1/features/snapshot, GET /api/v1/features/changes | map &#96;kor-travel-concierge-youtube&#96; provider가 소비하는 외부 계약&#40;docs/feature-export-api.md; oa §4&#41;. 변경 시 map provider 동시 수정 PR 동반&#40;M10 기준 취급&#41;. T-485. | null | 2026-12-31 | kor-travel-concierge |
| concierge | S2 | GET /api/v1/features/snapshot, GET /api/v1/features/changes | list envelope &#96;{items, next&#95;cursor, has&#95;more, total, newest&#95;id, newer&#95;than}&#96;&#40;oa §2.6&#41;. features export는 &#96;{items,next&#95;cursor,has&#95;more}&#96;로 map provider가 소비하는 외부 계약이다. 변경 시 M10 기준 동반 PR 근거를 적용한다. T-485. | null | 2026-12-31 | kor-travel-concierge |
| concierge | M1 | &#42; | export 스크립트·산출물·&#96;.github&#96; 없음&#40;oa §2.11&#41;. T-451 CI 신설 후 T-485. export·drift. | null | 2026-12-31 | kor-travel-concierge |
| concierge | M4 | &#42; | 요청 ID 미구현&#40;oa §2.5&#41;. 계층 1 규칙이므로 기한부. T-485. additive 추가. | 2026-12-31 | 2026-12-31 | kor-travel-concierge |
| concierge | M8 | &#42; | &#96;APIKeyHeader&#96;+&#96;Security&#96; 자동 선언이나 scheme 이름은 기본값&#40;미확인; oa §2.4&#41;. T-485. 확인·정정. | null | 2026-12-31 | kor-travel-concierge |
| concierge | N2 | &#42; | DB 발급 read 키 &#96;?key=&#96; 허용&#40;oa §2.4&#41;. 신규 표면에는 &#96;X-API-Key&#96;만. T-485. | null | 2026-12-31 | kor-travel-concierge |
| concierge | N5 | &#42; | &#96;latitude&#96;/&#96;longitude&#96; 필드&#40;routes.py:176-197; oa §2.7&#41;. Next BFF 동시 수정 필요. T-485. | null | 2026-12-31 | kor-travel-concierge |
| ktdm | M5.1 | &#42; | 버전 prefix &#96;/api/v1&#96;&#40;main.py:264-267; oa §2.2&#41;. 자체 Next 프론트 단일 소비자. T-486. | null | 2026-12-31 | kor-travel-docker-manager |
| ktdm | M3 | &#42; | FastAPI 기본 &#96;{detail}&#96;; 배포 계약 오류 3종만 &#96;{detail, request&#95;id}&#96;&#40;oa §2.5&#41;. &#96;request&#95;context.py&#96; docstring이 후속 항목으로 기록. T-486. | null | 2026-12-31 | kor-travel-docker-manager |
| ktdm | M1 | &#42; | export 스크립트·산출물·typegen 없음&#40;&#96;ci.yml&#96;은 type-check만; oa §2.11&#41;. T-486. | null | 2026-12-31 | kor-travel-docker-manager |
| ktdm | M8 | &#42; | 서명 쿠키 &#96;ktdm&#95;admin&#95;session&#96;을 &#96;request.cookies&#96;로 직접 읽어 securitySchemes 미선언&#40;추정; oa §2.4&#41;. &#96;apiKey in=cookie&#96; 선언은 T-486. | null | 2026-12-31 | kor-travel-docker-manager |
| ktdm | N2 | /metrics | &#96;KTDM&#95;METRICS&#95;REQUIRE&#95;KEY=1&#96;일 때 &#96;?key=&#96; 게이트&#40;oa §2.4·Q11&#41;. Prometheus scrape 설정 종속. T-486. | null | 2026-12-31 | kor-travel-docker-manager |
| ktdm | M7 | &#42; | DB naive UTC&#40;&#96;&#95;time.py&#96;, SQLite DateTime 호환 목적; be §2.12&#41;. 응답 직렬화 시 offset 부여 필요, 전환은 명시 결정. T-486. | null | 2026-12-31 | kor-travel-docker-manager |
| airport | N1 | &#42; | 와이어는 problem+json, 스펙은 FastAPI 기본 &#96;HTTPValidationError&#96; 422&#40;oa §2.5; inventory/kor-travel-airport.md §4.1&#41;. T-482 스펙 422 정합. | null | 2026-12-31 | kor-travel-airport |
| airport | M3 | &#42; | &#96;{type:'about:blank', title, status, detail, instance}&#96;에 &#96;code&#96;·&#96;request&#95;id&#96; 없음&#40;oa §2.5&#41;. additive라 프론트 &#96;readErrorMessage&#96; 무영향. T-482. | null | 2026-12-31 | kor-travel-airport |
| airport | M4 | &#42; | 요청 ID 미구현&#40;oa §2.5&#41;. 계층 1 규칙이므로 기한부. T-482. additive 추가. | 2026-12-31 | 2026-12-31 | kor-travel-airport |
| airport | M1 | &#42; | export만 있고 &#96;--check&#96;·CI drift 없음&#40;ADR-005 후속 과제; oa §2.11&#41;. T-482. &#96;--check&#96; CI. | null | 2026-12-31 | kor-travel-airport |
| airport | N8 | /health | &#96;/health&#96;가 DB &#96;count&#40;&#42;&#41;&#96; 질의 + &#96;release&#95;sha&#96;&#40;be §2.5&#41;. T-482. &#96;/readyz&#96;로 분리하고 &#96;/health&#96;는 무의존 liveness로. | null | 2026-12-31 | kor-travel-airport |
| weather | M9 | &#42; | export 스크립트가 &#96;KOR&#95;TRAVEL&#95;WEATHER&#95;ENV=development&#96;를 강제&#40;oa §2.11·M9 비고&#41;. production 표면과의 동일성 미확인. 계층 1 규칙이므로 기한부. T-481 재검증. | 2026-12-31 | 2026-12-31 | kor-travel-weather |
| weather | M8.1 | /v1/admin/&#42; | admin 토큰 헤더가 소문자 &#96;x-admin-token&#96;으로 &#96;X-&lt;AppId&gt;-&lt;Purpose&gt;&#96; 형식 밖&#40;oa §2.4&#41;. BFF &#96;route.ts&#96;가 주입하므로 이름 변경은 프론트 동반. T-481. | null | 2026-12-31 | kor-travel-weather |
| weather | M6 | POST body &#40;routers/weather.py:493-494&#41; | query는 &#96;lat&#96;/&#96;lon&#96; 준수, body는 &#96;latitude&#96;/&#96;longitude&#96;&#40;oa §2.7&#41;. admin UI 수기 타입 동반 수정. T-481. | null | 2026-12-31 | kor-travel-weather |
| map | M3.2 | &#42; | &#96;type&#96; = &#96;https://kor-travel-map/errors/&lt;code-kebab&gt;&#96; URI&#40;oa §2.5&#41;. common 기본 &#96;about:blank&#96;와 형식 정렬은 T-480. | null | 2026-12-31 | kor-travel-map |
| map | BE-3 | packages/kor-travel-map-api | &#96;starlette&gt;=0.40,&lt;1.0&#96; 상한&#40;TestClient/httpx 2.x 사유 주석; oa §2.12·Q7, be §2.1&#41;. airport·weather·pinvi는 starlette 1.6.0 설치. T-480 재검증 전까지 예외. versions.json exceptions&#91;&#93;에도 같은 항목. | null | 2026-12-31 | kor-travel-map |

검사: `python -B -X utf8 tools/openapi_exceptions.py --check`.
