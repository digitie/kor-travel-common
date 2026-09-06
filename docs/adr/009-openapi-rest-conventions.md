# ADR-009: OpenAPI/REST 규약 3계층과 예외 레지스트리·health 경로

- 상태: accepted — O-14(429 코드명·geo v2 시점·pinvi Zod)는 기본값으로 진행
- 날짜: 2026-09-06
- 근거 문서: `docs/plan/design-brief.md` D-14·D-22·O-14, `docs/survey/cross/openapi.md` §2.1~§2.12·§3.1~§3.3·§4·§5·§6, `docs/survey/cross/backend.md` §2.5·§2.10, `docs/survey/cross/ci-deploy.md` §1.13, `docs/survey/README.md` §6.2 항목 4(airport 21 paths)

## 컨텍스트

7개 FastAPI 백엔드는 팩토리·prefix(`/v1`·`/api/v1`·`/`)·에러 envelope(RFC7807 2·`{detail}` 2·`{error:{}}` 1·경로별 3종 1·`code` 없는 problem 1)·페이지네이션 4형·health 경로(`/health` 6 vs geo `/v1/healthz`)·export/drift 유무(geo·map `--check`, weather `git diff`, airport export만, 나머지 없음)가 갈린다(`oa` §2·§3.5). map OpenAPI 산출물은 pinvi·ktdm이 sha256으로 핀하므로 산출물 변경이 곧 cross-repo 계약 변경이다. 프론트 typegen은 geo·map만 `openapi-typescript`이고 나머지는 수기 타입, pinvi는 Zod 이중 유지다.

## 결정

1. `oa` §3의 M1~M9 / S1~S13 / N1~N8을 3계층으로 채택한다. 즉시 MUST(additive, 응답 본문 불변): M2(servers 미포함)·M4(`X-Request-ID`)·M9(production 표면 export)·N6·N7. 신규 표면 MUST / 기존 표면 SHOULD + 예외 등록: M1(export + `--check`)·M3(RFC7807 `code`·`request_id`·`errors[]`)·M5(`/health` liveness·`/readyz`·`/version`)·M6(lon/lat)·M7(tz-aware)·M8(securitySchemes)·N1~N5·N8. SHOULD: S1~S13.
2. 예외 레지스트리 `docs/standards/openapi-exceptions.yaml` `{app, rule, surface, reason, sunset|null, review, owner}` + 생성 md. 초기 등록: geo v1(VWorld 호환)·geo v2 envelope(`query_id`↔`request_id`)·pinvi `{error:{}}`·정수 `If-Match`+409·비버저닝 경로·concierge `/api/v1`·`{detail}`·features export(map provider 외부 계약)·ktdm `/api/v1`·`{detail}`·airport 스펙 422 불일치·map `starlette<1.0`.
3. health: `/health`는 무의존 liveness, `/readyz`는 의존성 점검(저하 시 503), `/version`. geo `/v1/healthz` 별칭은 소비자 probe·Prometheus 갱신 확인 전까지 무기한 예외. `/metrics`는 스키마 제외 + production 토큰.
4. 검증 오류 422 기본·geo 400 예외. 429 코드 사전은 common 기본 `TOO_MANY_REQUESTS` + 앱 덮어쓰기.
5. `X-Request-ID` 형식: UUID v4/v7 또는 ULID, ≤128자 ASCII, 검증 실패 시 서버 발급, `trust_incoming=False`는 앱 옵션(ktdm).
6. 헤더 이름은 형식 규칙만(`X-<AppId>-Api-Key|Service-Token|Actor|Admin-Proxy-Secret|Ops-Token|Ops-Scope`), AppId(풀네임/약어)는 앱 소유. 메트릭 접두도 형식만 공통(신규 `kt<x>_`, map·pinvi 기한부 예외).
7. map OpenAPI 산출물 변경은 pinvi·ktdm sha256 pin 갱신 PR 동반 없이 머지 금지.
8. 프론트 typegen: `openapi-typescript` 7.x 단일 버전, `gen:types`/`gen:types:check`. pinvi Zod 이중 유지는 "OpenAPI↔Zod 일치 테스트"로 대체한다.
9. 재사용 워크플로 `openapi-drift.yml`·`typegen-drift.yml`은 Phase 3(T-309); pinvi·ktc·ktdm은 export 파이프라인 신설 task가 선행이다.

## 대안 검토

- **전 규약 즉시 MUST**: pinvi `{error:{}}`·concierge/ktdm `{detail}`·geo v1은 breaking이라 클라이언트·모바일까지 깨진다. 응답 본문 불변인 additive 항목만 즉시 MUST로 두고 나머지는 예외 등록으로 흡수했다.
- **health 경로를 geo `healthz`로 통일**: 6곳이 `/health`이고 geo만 다르며, geo 경로 이동은 probe·Prometheus 설정 동반이 필요하다. 별칭 병행이 비용이 낮다.
- **헤더 AppId 통일(풀네임 또는 약어)**: BFF·proxy·프론트 상수까지 결합된 배포 계약이라 이름 변경 비용이 크고 이득이 작다. 형식 규칙만 둔다.
- **pinvi를 `openapi-typescript`로 전환**: Pydantic↔Zod 이중 유지 정책과 충돌한다. 일치 테스트가 더 맞다(`oa` Q5).

## 결과

- 신규 표면은 처음부터 통일된 계약을 갖고, 기존 표면은 예외 레지스트리로 현재 상태를 명시한 채 점진 정렬한다.
- 예외에는 `review`가 필수라 분기 감사(T-506)에서 재판정된다.
- map 산출물 변경 절차가 무거워지지만 pinvi·ktdm의 pin 사고를 막는다.
- py 패키지의 C12 export CLI·C4 health·C5 problem(opt-in)·C2 request_id가 이 규약의 구현체다(ADR-011).

## 후속·적용 위치

- 규칙: `docs/standards/openapi.md`, `docs/standards/openapi-exceptions.yaml`(T-301)
- 구현: T-303(export CLI), T-304(health), T-307(request_id·metrics), T-308(problem 등)
- 워크플로: T-309(`openapi-drift`·`typegen-drift`)
- 소비자: T-480~T-486(app별 정렬; map pin 갱신 동반), T-484(pinvi export 파이프라인)
