# ADR-011: Python 공통 패키지 구조(extras·3.11 호환·모듈 우선순위·인증 범위 밖·메트릭 접두)

- 상태: partially superseded by ADR-015 — O-7(앱 floor 3.12 시점)·O-12(메트릭 접두 map·pinvi)는 기본값으로 진행
- 날짜: 2026-09-06
- 인증 프리미티브 제외 결정은 [ADR-015](015-common-shared-systems-scope.md)로 대체하며 Python 버전·extras·모듈 순서는 유지한다.
- 근거 문서: `docs/plan/design-brief.md` D-15·D-22·O-7·O-12, `docs/survey/cross/backend.md` §2.1~§2.19·§3·§4·§5.3·§7, `docs/survey/cross/openapi.md` §5, `docs/survey/commonality-matrix.md` §1.4·§2.4, `docs/survey/README.md` §6.2(common Python floor 3.11)

## 컨텍스트

7개 백엔드는 settings·logging·metrics·health·DB·alembic·에러·시간·테스트·품질·export 19개 항목에서 같은 골격을 각자 유지한다(`be` §2.19). 공개 API 키 함수는 4곳 동일, health 4형·에러 7종·요청 ID 4형이 갈렸고, OpenAPI export는 geo·map만 `--check`가 있다. Python 하한은 3.11(map·weather·ktdm)과 3.12(airport·geo·pinvi)로 갈리고 geo·map은 import-linter로 계층 계약을 강제한다. 메트릭 접두는 `ktc_`·`ktdm_`·`ktg_`·`ktw_` 대 map `kor_travel_map_`·pinvi `pinvi_api_`다. 선행 보고서 §3.6은 인증 경계를 첫 범위에서 제외했고 조사도 동의했다(`be` §6).

## 결정

1. 배포 이름 `kor-travel-common`, import `kortravelcommon`(일반 패키지, namespace magic 없음), hatchling, `requires-python >=3.11`(3.11 문법). core는 stdlib + pydantic만 의존해 geo·map import-linter 계약과 정합. FastAPI 의존은 `[api]` extra, 그 외 `[db]`·`[dagster]`·`[testing]`·`[http]`.
2. 모듈 우선순위: 1차 C12 openapi export CLI(`--check`·profile 콜백·결정적 직렬화)·C4 health(`/health`·`/readyz`·`/version`, 기존 경로 alias 옵션)·C13 time(KST/UTC·aware 검증)·C20 quality(ruff `extend` 베이스 `line-length=100`·`E,F,I,UP,B,ASYNC`, mypy strict 베이스, import-linter 계약 템플릿, pre-commit 템플릿; **format 규칙 미포함**, per-file-ignores baseline) → 2차 C1 settings 베이스·C9 db 엔진 팩토리·C7 public_api_key·C2 request_id(`trust_incoming`)·C3 metrics(표준 HTTP 3지표·라벨·센티널·multiproc; 접두는 인자) → 3차 C5 errors/problem(opt-in, `exclude_paths`)·C16 security_headers(HSTS 전달 헤더 불신 기본)·C17 cors·C8 trusted_proxy·C11 testing 픽스처·C10 alembic 템플릿·C15 http·C18 dagster → 보류 C6 pagination·C14 geo_primitives(좌표 경계 상수 공통화 금지)·C19 cli.mutex·C21 백업 규약(문서).
3. `[api]` starlette 범위 미선언 + CI 0.4x/1.6 매트릭스(map `starlette<1.0` 재검증 전까지).
4. 메트릭 접두: 신규 서비스 `kt<x>_` MUST, map `kor_travel_map_`·pinvi `pinvi_api_`는 기한부 예외(review 2026-12, 대시보드 영향 평가 후 재판정). 접두는 인자로 받는다.
5. 인증(비밀번호·세션·CSRF·JWT·RBAC)은 범위 밖을 유지한다. 도메인 결합 부분(geo loaders·GeoIP·VWorld 형식, map RoutePolicy·ServiceToken·300 baseline, pinvi JWT/RBAC/M05, ktdm compose/pin registry, ktc LLM/APScheduler/MCP, ktw provider, kta 스케줄러), 서비스 간 클라이언트, provider 재래핑은 제외한다.
6. 1차 소비자 map-api·weather-api·airport(T-480~T-482), 2차 geo(T-483), 3차 pinvi·concierge·ktdm(L8 후). 릴리스 `py-v0.1.0`은 1차 3모듈 + quality가 검증된 뒤 wheel 자산으로(T-310).

## 대안 검토

- **인증 순수 함수(PBKDF2·HMAC 세션·rate-limit) 포함**: 상수가 4곳 일치하지만 revocation 저장소·신원 전달이 앱마다 달라 파라미터화 후에도 신뢰 경계가 남는다(geo 2026-09-04 취소 사례). 규칙 문서로만 둔다.
- **floor 3.12**: geo의 PEP 695는 geo 내부에 국한되고 map·weather·ktdm이 3.11이다. common 3.11 호환이 소비자 범위를 넓히며 앱 상향은 Phase 4 앱 결정이다.
- **메트릭 접두 즉시 통일**: map·pinvi 이름 변경은 대시보드 회귀 범위가 미확인이다. 기한부 예외로 둔다.
- **pagination 코덱 1차 포함**: `limit`/`page_size`·`has_more`/`next_cursor` 이름 충돌 합의가 선행이라 보류한다.
- **format 규칙(`ruff format`) 포함**: ktdm은 재포맷 금지, map만 format 검사를 정의(비활성)한다. 포함하면 도입 앱마다 대량 diff가 난다.

## 결과

- 1차 모듈은 계약 무변경(export 산출물 동일·health 경로 동일)이므로 map·weather·airport에서 교체만으로 채택된다.
- extras 분리로 core는 FastAPI 없이 dagster·CLI 컨텍스트에서도 import된다.
- starlette 매트릭스 유지 비용이 있으며 map 상한 재검증(T-480) 뒤 축소한다.
- 3차 소비자(pinvi·ktc·ktdm)는 에러 envelope 변경이 breaking이라 L8 이후 묶음 PR로만 진행한다.

## 후속·적용 위치

- 현재 설계: `docs/architecture/packages.md` §4
- 규칙: `docs/standards/backend-stack.md`(T-302 확정), `docs/standards/openapi.md`
- 실물: T-302(골격), T-303(C12), T-304(C4·C13), T-305(C20), T-306·T-307(2차), T-308(3차), T-310(`py-v0.1.0`)
- 소비자: T-480~T-486; 재평가 T-508(pagination 코덱)
