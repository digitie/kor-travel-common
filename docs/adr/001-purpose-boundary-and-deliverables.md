# ADR-001: kor-travel-common의 목적·경계·배포 단위

- 상태: accepted
- 날짜: 2026-09-06
- 근거 문서: `docs/plan/design-brief.md` D-01·§0, `docs/survey/commonality-matrix.md` §1·§2·§4.1, `docs/survey/cross/ui-components.md` §4.1~§4.3·§6.2, `docs/survey/cross/backend.md` §3·§4, `docs/survey/cross/version-matrix.md` §1.3, `docs/survey/inventory/kor-travel-map.md` §3.1

## 컨텍스트

kor-travel 제품군 7개 저장소(kor-travel-airport·concierge·docker-manager·geo·map·weather·pinvi)는 map admin을 원형으로 하는 UI 계보, 같은 FastAPI 골격, 같은 에이전트 규약을 각자 복사해 유지한다. pinvi admin 28 primitive는 map 소스 복사본이지만 정규화 후에도 27쌍 전부가 갈라졌고(`ui` §2.1), 에러 본문 7종·페이지네이션 4형·health 4형·요청 ID 4형이 저장소 간 sha256 pin 비용으로 이미 나타났다(`be` §6, `oa` §3.5). 사용자는 코드뿐 아니라 규칙(색상 톤·UX·OpenAPI·PC/Mobile Web·버전 일치)도 common 산출물로 요구했고(지시 (4)), kor-travel-airport Admin·PinVi Admin을 소비자에 포함하도록 지시했다(지시 (3)).

반면 인증·도메인·지도 엔진은 화면이 비슷해도 신뢰 경계가 다르며(선행 보고서 §3.6, geo 2026-09-04 취소 사례), 이미 분리된 공유 라이브러리(`maplibre-vworld-*`·`python-*-api`·`python-kraddr-base`)가 있다.

## 결정

1. 배포 단위는 여섯 가지로 고정한다: `packages/tokens`(npm `@kor-travel/tokens`), `packages/ui`(npm `@kor-travel/ui`), `packages/py/kor-travel-common`(PyPI 이름 `kor-travel-common`, import `kortravelcommon`), `docs/standards/*` 규칙 문서, `templates/*`, `versions.json` + `tools/*.py`(+ 재사용 워크플로).
2. `config` npm 패키지와 `api-client-core`는 만들지 않는다. 전자는 `templates/eslint/*.mjs` 조각과 `docs/standards/frontend-stack.md`로, 후자는 Phase 5(T-508)에서 재평가한다. ui는 아이콘을 인라인 SVG로 가져 `lucide-react`를 peer로 두지 않는다(0.363~1.41 혼재).
3. 의존 방향은 앱 → ui → tokens, 앱 → py의 단방향이다. common은 소비자 코드를 import하지 않는다.
4. common은 앱 도메인 모듈, 지도 엔진(`maplibre-vworld-*`), provider 라이브러리(`python-*-api`), 인증 서비스(비밀번호·세션·CSRF·JWT·RBAC)를 갖지 않는다. 공유 라이브러리는 의존만 하고 복제·재래핑하지 않는다.
5. 소비자는 7개 저장소이며 pinvi는 admin·사용자 웹·모바일 세 표면으로 나눈다. 사용자 웹·모바일은 코드 소비 대상이 아니고 consumer 프로필 규칙과 `tokens.json` 의미 이름만 공유한다.
6. 공통화 승격은 소비자 2곳 이상의 사실 근거·권리 gate·계약 시험·SemVer 판정 네 요소가 동시에 있어야 한다. 소비자 1곳 관찰만으로 승격하지 않는다.
7. 패키지명 `@kor-travel/<pkg>`는 잠정이며 npm scope 확보(T-006) 실패 시 `@digitie/kor-travel-<pkg>`로 개명한다.

## 대안 검토

- **단일 모노 패키지(UI+토큰+설정)**: 설치는 단순하지만 React 18 앱(geo·ktdm)과 Tailwind 없는 앱(weather·airport main)이 토큰만 채택할 길이 막힌다. tokens은 React 무관이어야 한다(`dt` §3.6.7).
- **`api-client-core` 1차 포함**: 앱별 `ApiError` 4형이 달라 어댑터 단계가 필요하고(`cm` §2.3), 1차 가치가 낮다. Phase 5 재평가로 미뤘다.
- **인증·세션 순수 함수 공통화**: 세션 상수가 4곳 일치하지만 revocation 저장소·신원 전달이 앱마다 달라 파라미터화 후에도 신뢰 경계가 남는다. 공개 API 키·trusted proxy·request-id 같은 비인증 인프라만 py 모듈로 둔다(ADR-011).

## 결과

- tokens·ui·py를 독립 버전으로 릴리스할 수 있고 소비자는 필요한 단위만 채택한다.
- 규칙 문서는 코드 링크가 아니므로 라이선스 정렬(L8) 전인 MIT 앱도 참조할 수 있다.
- 경계 밖 요청(지도 스타일 빌더·마커 팔레트 hex·provider SHA 정렬)은 각 저장소에 결정 요청 문서(T-505)로 넘긴다.
- 배포 단위가 여섯이므로 릴리스·CI·문서가 단위별로 분리되어 초기 골격 비용이 든다.

## 후속·적용 위치

- 현재 설계: `docs/architecture/README.md` §1~§3, `docs/architecture/packages.md`
- 정책: `AGENTS.md` §1(경계)·§6(금지)
- task: T-006(scope 확인), T-101·T-201·T-302(실물), T-505(공유 라이브러리 정리 요청), T-508(보류 재평가)
