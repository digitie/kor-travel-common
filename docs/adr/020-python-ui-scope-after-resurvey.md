# ADR-020: 2026-11 재조사로 Python·UI 공통 범위를 다시 정한다

- 상태: accepted
- 날짜: 2026-11-17
- 결정자: 소유자(2026-11-17, "ADR-020 (기존 표준과 어긋나는 판정): T-022가 초안을 만들고, 항목별로 수락·거부·보류를 정합니다 … 이것들은 추천안 대로")
- 근거 문서: [공통화 재조사·계획](../plan/commonization-plan-2026-11-17.md) §1.5·§3·§5, [T-022](../tasks/T-022-ledger-reality-reconcile.md)
- Supersedes: [ADR-011](011-python-common-package.md)의 모듈 우선순위(1차 C12·C4·C13·C20, 2차 C1·C9·C2·C3, 3차 C5·C10·C15·C16·C17·C18) 가운데 아래 표에서 '수락'·'보류'한 항목. Python 버전·extras·메트릭 접두와 C6·C7·C8·C11·C14 결정은 그대로 둔다

## 컨텍스트

ADR-011과 [backend-stack](../standards/backend-stack.md)·[openapi](../standards/openapi.md)·[ci-deploy](../standards/ci-deploy.md)·[ui-contract](../standards/ui-contract.md)는 2026-09 조사를 근거로 Python 모듈 19개와 UI 부품의 공통 순서를 정했다. 2026-11-17 재조사는 다섯 저장소의 고정 커밋에서 같은 항목을 다시 읽었다. 계획한 1차·2차 Python 모듈은 구현되지 않았고, 실물 `kortravelcommon`은 운영 장애가 요구한 묶음(Dagster 복구·probe·응답 상한 HTTP 등)이 됐다. 재조사의 판정 가운데 기존 결정과 어긋나는 것은 계획 §1.5 표의 15행이다. 이 ADR은 그 15행을 하나씩 결정한다.

판정 어휘:

- **수락**: 재조사의 판정을 채택한다. 기존 ADR-011·standards의 해당 결정을 대체하고 연결된 task를 철회하거나 범위를 줄인다.
- **보류**: 재조사가 '나중에 공유'로 둔 항목이다. 기존 결정의 시행 순위(1차·2차)를 내리고, 적힌 조건이 생길 때 다시 결정한다. 그 전에는 구현 task를 열지 않는다.
- **거부**: 기존 결정을 유지한다.

## 결정

소유자는 계획의 권고대로 결정했다. 15행 가운데 수락 12, 보류 2, 수락과 보류로 나눈 것 1, 거부 0이다.

| # | 항목 | 기존 결정 | 판정 | 이유(한 줄) | 후속 |
|---|---|---|---|---|---|
| 1 | C12 OpenAPI export CLI | ADR-011 1차, openapi export drift 행, ci-deploy `openapi-drift.yml`, T-303·T-309 | 보류 | 직렬화·비교 규칙이 셋 다 달라 맞추는 비용이 줄 수 이득보다 크다(K-16) | T-303·T-309 범위 재정의(T-022). 조건: 네 번째 export 소비자 또는 직렬화 통일 결정 |
| 2 | C4 health 라우터 | ADR-011 1차, BE-15, T-304 | 수락 | 응답 본문이 각 서비스 OpenAPI 계약이다. 공유는 probe만(K-15, K-10) | T-304에서 health 철회(T-022). probe는 T-480b·T-486a |
| 3 | C13 time | ADR-011 1차, BE-19, T-304 | 보류 | 저장소 **안** 중복이 더 크다. 저장소 안 정리가 먼저다(K-35) | T-304의 time 부분 범위 재정의(T-022) |
| 4 | C20 quality(ruff·mypy 베이스, `python-quality.yml`) | ADR-011 1차, BE-6~BE-11, T-305, T-401의 Python 절반 | 수락 | 베이스의 공통 부분은 이미 같고 나머지는 저장소별 선택이다(K-71) | T-305 철회, T-401 Python 절반 철회(T-022), standards 반영(T-027) |
| 5 | C1 settings 베이스 | ADR-011 2차, BE-12, T-306 | 수락 | 빈 env 처리가 네 방식이고 profile 기본값이 반대라 공통 베이스가 의미를 조용히 바꾼다(K-12) | T-306에서 C1 철회(T-022) |
| 6 | C9 db 엔진 팩토리 | ADR-011 2차, BE-23, T-306 | 수락 | 드라이버가 셋이고 timeout 값이 사고별로 조정돼 있다(K-13) | T-306에서 C9 철회. C7은 독립 task로 남긴다(T-022) |
| 7 | C2 logging | ADR-011 2차, BE-13, T-307 | 수락(로깅 설정)·보류(request-id 미들웨어) | 로깅 설정은 저장소별이고, request-id는 신뢰 정책이 갈려 `trust_incoming` 옵션을 정한 뒤에 공유한다(K-23, K-24) | T-307을 request-id와 지표로 나눈다(T-022) |
| 8 | C3 metrics | ADR-011 2차, BE-14, T-307 | 수락 | 지표 이름·라벨이 대시보드 계약이다(K-24) | T-307의 지표 부분 철회(T-022) |
| 9 | C5 errors·problem | ADR-011 3차, BE-16, T-308 | 수락 | 오류 형식 다섯 가지를 프론트와 형제 client가 읽는다. 통합은 세 저장소 이상의 파괴적 변경이다(K-19) | T-308에서 C5 철회(T-022) |
| 10 | C10 alembic 템플릿 | ADR-011 3차, BE-24, T-308 | 수락 | P·M이 같은 위험을 반대 방식으로 다룬다. 규약 문장 한 줄만 남긴다(K-14) | T-308에서 C10 철회, 규약 한 줄은 T-027 |
| 11 | C15 http(재시도·circuit) | ADR-011 3차, BE-20, T-308 | 수락 | 재시도·circuit은 호출 자리의 결정이다. 응답 상한 요청(`bounded_request`)은 이미 있다(K-18) | T-308에서 C15 철회(T-022) |
| 12 | C18 dagster(Definitions 3단 폴백·`dagster.yaml` 템플릿) | ADR-011 3차, BE-21, T-308 | 수락 | Definitions 조립은 도메인 결선이다. 복구·coalescing·회수 sensor는 이미 있다(K-47, K-49) | T-308에서 C18 철회(T-022) |
| 13 | `validateForm`(헤드리스 폼 검증) | ui-contract §4.6, T-210 | 수락 | 규칙 기반 구현은 map 한 곳이고 다른 저장소는 이름만 같은 다른 모델이다(K-55) | T-210 범위 재정의(T-022), ui-contract 반영(T-027) |
| 14 | UI 엔진 표기 | ui-contract §2·§3의 `@base-ui/react` | 수락 | 실물은 `radix-ui`다([ADR-017](017-shadcn-radix-shared-components.md)). 문서를 실물에 맞춘다(K-50) | ui-contract 본문 정정(T-027) |
| 15 | C16 security headers·C17 cors | ADR-011 3차, BE-17, T-308 | 수락 | 헤더 값이 제품별이고 CORS는 이미 Starlette `CORSMiddleware`가 공통이다(K-25) | T-308에서 C16·C17 철회(T-022) |

기존 결정과 같은 방향이라 이 ADR이 결정하지 않는 것: C6 pagination(코덱만 나중, T-508), C7 `public_api_key`(유지, T-306에서 분리), C8 `trusted_proxy`(유지, T-308에서 분리), C11 testing(유지), C14 좌표 경계(금지), `ConfirmDialog`(앱 소유, T-508), 세션·로그인(ADR-015).

## 대안 검토

- **기존 결정 유지(전부 거부)**: 1차·2차 모듈을 계획대로 만든다. 다섯 저장소가 일부러 다르게 둔 계약(오류 형식·health 본문·빈 env 의미·지표 이름) 위에 결박층을 하나 더 얹는다. 단순함 우선(R2)과 계약 비결박(R1·R8)에 어긋나 기각한다.
- **'나중에 공유'도 수락으로 처리**: C12·C13·request-id를 철회하면 조건이 생겨도 다시 열 근거가 없어진다. 보류로 두고 조건을 적는다.

## 결과

- 이 표의 '수락' 항목에 대해서는 ADR-011의 모듈 순서와 standards의 해당 규칙이 더는 유효하지 않다. standards 본문은 [T-027](../tasks/T-027-standards-after-reclassification.md)이 옮긴다. T-027의 외부 선행(ADR-020 accepted)은 이 ADR로 충족됐고, 남은 선행은 T-022다.
- task 원장 재분류(T-201~T-214·T-302~T-312 대조표, T-304·T-306·T-307·T-308 분할)는 [T-022](../tasks/T-022-ledger-reality-reconcile.md)가 이 표를 입력으로 한다.
- 보류 항목은 구현 task를 열지 않는다. 조건이 생기면 새 ADR로 다시 결정한다.

## 후속·적용 위치

[T-022](../tasks/T-022-ledger-reality-reconcile.md)(원장 재분류), [T-027](../tasks/T-027-standards-after-reclassification.md)(standards 본문), [ADR-011](011-python-common-package.md) 상태 표기.
