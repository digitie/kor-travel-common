# kor-travel-common 조사 문서 안내 (docs/survey)

- 조사일: 2026-09-06
- 성격: `kor-travel-common` 설계를 위한 **읽기 전용 조사** 결과 모음. 결정문이 아니며, 설계 단계에서 결정할 항목은 `commonality-matrix.md` §4에 모아 두었다.
- 구성: 인벤토리 7편(`inventory/`) + 횡단 비교 10편(`cross/`) + 종합 2편(이 문서, `commonality-matrix.md`).
- 표기 규약(전 문서 공통): **사실** = 기준 커밋의 파일에서 직접 확인 / **후보** = 설계 제안 / **추정** = 정황 근거 / **미확인** = 조사 범위에서 확인하지 못함. 별도 표기가 없는 서술은 사실이다.

## 1. 목적

`kor-travel-common`(GPL-3.0, Tailwind v4 + shadcn/ui + React + Next.js, FastAPI)은 kor-travel 제품군의 UI·백엔드 공통 코드와 공통 규칙(색상 톤·UX 가이드·OpenAPI·PC/Mobile Web·라이브러리/플랫폼 버전 일치)을 정의한다. 이 조사는 그 설계에 앞서 7개 소비 저장소의 현행 코드·문서를 **기준 커밋 단위로 고정**해 읽고, (1) 무엇이 이미 수렴했는지, (2) 무엇이 갈라져 있는지, (3) 공통화 시 어떤 계약 변경·라이선스·버전 격차가 생기는지를 근거 경로와 함께 남긴다.

설계 전제(사용자 지시)는 네 가지다: (1) Tailwind v4가 아닌 앱은 v4로 전환, (2) common 정책에 개별 시스템의 라이브러리/플랫폼 버전 일치화 포함, (3) kor-travel-airport Admin과 PinVi Admin 포함, (4) 코드뿐 아니라 규칙도 common의 산출물. 각 횡단 문서는 이 전제를 사실로 검증하거나 조건을 붙였다(예: 전제 (1)의 실제 대상은 "v3→v4"가 아니라 대부분 "미도입→도입"이다 — `cross/version-matrix.md` §1.2; 전제 (3)의 "airport Admin"은 별도 앱이 아니라 무인증 백업 패널이다 — `inventory/kor-travel-airport.md` §1·§9).

## 2. 조사 기준

### 2.1 조사 대상 저장소·커밋·경로

| 약칭 | 저장소 | 정본 체크아웃 | 기준 커밋 | 커밋 일자 | 비고 |
|---|---|---|---|---|---|
| airport / kta | kor-travel-airport(구 parking-radar) | `F:/dev/kor-travel-common-survey/kta-main` | `2bb1111` | 2026-09-06 | 작업 트리 clean. **WIP 브랜치** `codex/shadcn-ui-foundation` = `99b3f98`(`F:/dev/kor-travel-airport`, clean, main 위 단일 커밋)은 별도 열로 표기 — `inventory/kor-travel-airport.md` §3.2 |
| concierge / ktc | kor-travel-concierge(TripMate) | `F:/dev/kor-travel-concierge` | `7945305` | 2026-09-04 | CI 없음, Python lockfile 없음 |
| docker-manager / ktdm / dm | kor-travel-docker-manager(ktdctl) | `F:/dev/kor-travel-common-survey/ktdm-main` | `862562d` | 2026-09-05 | Poetry 매니페스트, lock 미커밋 |
| geo | kor-travel-geo(+kor-travel-geo-ui) | `F:/dev/kor-travel-geo-fixes` | `1d9d74d` | 2026-09-05 | 선행 보고서 기준 `daf079b`의 직후(문서 3개만 변경) |
| map / ktm | kor-travel-map(npm workspaces) | `F:/dev/kor-travel-common-survey/ktm-main` | `c494e227` | 2026-09-06 | admin UI·API·Dagster 3패키지 |
| weather / wx / ktw | kor-travel-weather(uv) | `F:/dev/kor-travel-weather` | `6003da9` | 2026-09-05 | admin은 Tailwind 없음 |
| pinvi | PinVi(apps/web admin+user, apps/mobile, apps/api, apps/etl) | `F:/dev/kor-travel-common-survey/pinvi` | `9af25e5` | 2026-09-06 | **shallow clone**(git log 1건) — 이력·저작자 조사 불가 |

문서마다 열 이름 약칭이 다르다(예: `ktdm`/`dm`, `weather`/`wx`/`ktw`, `concierge`/`ktc`/`conc`). 위 표의 약칭을 대응표로 쓴다.

### 2.2 참조·대조 대상

| 대상 | 경로 | 커밋 | 용도 |
|---|---|---|---|
| canview(구조 참조, 제품군 밖) | `F:/dev/canview` | `d078437`(`cross/docs-conventions.md`·`cross/design-tokens.md`) / `1f93b8a`(`cross/canview-structure-checklist.md`·`cross/licensing.md`; 직후 1커밋, 문서 규약 파일 차이 없음 — checklist 기준 표) | AGENTS/SKILL/docs 구조 모델 |
| 기존 공유 라이브러리(중복 금지) | `F:/dev/maplibre-vworld-react`(`95b49d3`), `F:/dev/maplibre-vworld-js`(`2a13ce0`), GitHub `digitie/python-*-api` 13종, `digitie/python-kraddr-base` | — | peer 범위·라이선스·핀 대조만 |
| 선행 검토 보고서 | `F:/dev/kor-travel-geo-fixes/docs/kor-travel-common-library-review.md` | 2026-09-05, geo PR #546 | §5에서 계승·보완·반박 정리 |
| 새 저장소 | `F:/dev/kor-travel-common` | `b92fabe`(브랜치 `feat/bootstrap-survey-and-integration-plan`, 추적 파일 `LICENSE` 1개, 나머지는 미추적 scaffold) | `cross/canview-structure-checklist.md` §1이 scaffold 내용 대조 |

### 2.3 방법과 한계

- 모든 명령은 읽기 전용(`git rev-parse/ls-files/show/diff/grep`, `cat/sed/grep/rg`, lockfile 파싱 스크립트)이며 조사 대상 저장소에는 어떤 파일도 만들지 않았다. 예외적으로 `cross/canview-structure-checklist.md`는 canview·common의 문서 검증 도구(`validate_plan.py`, `validate_document_links.py`)를 실행했고 부산물이 없음을 확인했다.
- 버전은 "선언 범위"(`package.json`/`pyproject.toml`/`requirements.txt`)와 "lockfile 설치 버전"(`package-lock.json`/`uv.lock`)을 분리해 읽었다. Python lockfile이 없는 geo·map·docker-manager·concierge의 설치 버전은 **미확인**이다(`cross/version-matrix.md` §2.1). 최신 안정 버전은 2026-09-06 npm/PyPI/endoflife.date/GitHub API 조회값이다(§4.1).
- **제외 범위**: 로컬 미커밋 코드, 운영(n150) 실제 배포 버전과 컨테이너 내부 상태, `node_modules`/`.venv`/`.next`/빌드 산출물, gitignore된 `*.local.md`. 빌드·테스트·브라우저 렌더 검증은 하지 않았다(airport CI 결과만 `gh run view`로 조회 — `cross/version-matrix.md` §6).
- pinvi는 shallow clone이라 `git log`·`git shortlog`가 1건뿐이다. 이력 기반 판단(변경 시점, 저작자 분포)은 pinvi에 대해 성립하지 않는다(`cross/licensing.md` §2.6).
- airport WIP 브랜치는 지시문의 "dirty"와 달리 clean이며, 인벤토리·횡단 문서는 main(`2bb1111`)과 WIP(`99b3f98`)를 항상 구분해 적었다. 단 `cross/licensing.md` §5는 WIP 체크아웃을 열지 않았다(§6.2 항목 13).
- 파일 수·줄 수 같은 집계는 문서마다 grep 범위(테스트 포함 여부, 확장자, 주석 언급 포함)가 달라 수치가 어긋날 수 있다. §6.2에 재확인 결과를 적었다.

## 3. 문서 목록

### 3.1 인벤토리(저장소별, 각 §1 개요 → §8 공통화 후보 → §9 고유 차이 → §10 버전 표 → §11 미확인 → §12 근거)

| 문서 | 한 줄 설명 |
|---|---|
| [inventory/kor-travel-airport.md](inventory/kor-travel-airport.md) | 순수 CSS·무인증 대시보드(main)와 Tailwind v4+shadcn `base-nova` 도입 WIP(`99b3f98`)를 함께 기록. 선행 보고서에 없던 최초 인벤토리. RFC7807·`/v1`·OpenAPI export를 map에서 이식했으나 CI drift·lint·lock 소비가 빠져 있음 |
| [inventory/kor-travel-concierge.md](inventory/kor-travel-concierge.md) | Base UI `base-nova` 18종 프리미티브(map 계보 부분집합), `--ktc-*` 3단 토큰, Next `proxy.ts` 세션+BFF, keyset cursor 목록 계약. MIT, CI·lockfile 없음, 라우터 단일 파일 3,759줄 |
| [inventory/kor-travel-docker-manager.md](inventory/kor-travel-docker-manager.md) | Next 14/React 18, shadcn 미도입(`ops-*` CSS), `@theme` OKLCH 토큰, 포트 정본 `docs/ports.md`, runtime pin registry, `bindings.md`(중복 선언 결박) — 버전 일치 정책의 선행 사례 |
| [inventory/kor-travel-geo.md](inventory/kor-travel-geo.md) | React 18 + Radix `radix-nova`, `@config` 잔존 혼합 Tailwind v4, VirtualTable(클라이언트 정렬), openapi-typescript 파이프라인, `KTG_` settings·`ktg_` 메트릭·`/v1/healthz`·`/v1/readyz`, GPL-3.0-only |
| [inventory/kor-travel-map.md](inventory/kor-travel-map.md) | admin UI 정본(Hallmark 잠금 `design.md`, 30 primitive + 26 앱 부품, DataTable), RFC7807+`{data,meta}`, RoutePolicy, OpenAPI 3 profile export, npm 12.0.1 exact 핀·검증 스크립트·pytest 잠금 |
| [inventory/kor-travel-weather.md](inventory/kor-travel-weather.md) | Tailwind 없는 2,495행 CSS admin(map 토큰 값 복사), geo 세션 상수 일치, uv.lock을 CI·Docker 모두 `--locked` 소비, `python-airkorea-api` 저장소 내 벤더링. §9.1에 v4 전환 정량 추정 |
| [inventory/pinvi.md](inventory/pinvi.md) | admin(KTM 이식 28 primitive + 22 부품, base-ui는 overlay만)·사용자 웹(Airbnb 톤 44px)·모바일(NativeWind 4/Tailwind 3) 세 표면, `{error:{}}` envelope, 루트 LICENSE 없음·README "비공개" vs AGENTS "공개" 상충 |

### 3.2 횡단 비교(주제별)

| 문서 | 한 줄 설명 | 핵심 절 |
|---|---|---|
| [cross/version-matrix.md](cross/version-matrix.md) | 7개 저장소 프론트·백엔드·CI·컨테이너 버전을 선언/설치로 대조하고 2026-09-06 최신과 비교. airport TS 7.0.2 실검증 | §1.8 요약, §5.1 기준선 후보, §5.2 앱별 격차, §6 TS7, §7 핀 정책 |
| [cross/design-tokens.md](cross/design-tokens.md) | 토큰 정본·값 형식·역할 매핑·shadcn alias·대비 재검증·마커 팔레트 소유권, common 토큰 패키지 초안(`--kt-*`) | §3.2 역할표, §3.4.2 대비, §3.5 마커, §3.6 패키지 초안, §5 |
| [cross/ui-components.md](cross/ui-components.md) | map↔pinvi 27쌍 정규화 diff, Button/Table/DataTable 계약 차이, 1차/2차/보류 후보, 프리미티브 엔진(base-ui vs radix), 등록 방식 A/B/C | §2.1~2.3, §3.1~3.3, §4, §5.4, §6.2 |
| [cross/ux-patterns.md](cross/ux-patterns.md) | 셸·목록·상세·피드백·상태·위험 작업·로그인·PC/Mobile 대응 비교, UX 가이드 초안 G0~G9, PC/Mobile 규약 초안, 충돌 C1~C22 | §1.1~1.13, §2, §3, §4 |
| [cross/backend.md](cross/backend.md) | Python 백엔드 19개 항목 비교(설정·로깅·메트릭·health·DB·alembic·인증·에러·retry·시간·백업·Dagster·CLI·테스트·품질·export), 공통 모듈 C1~C21, 배포 방식 | §2.19 요약, §3, §4 제외 목록, §5, §7 |
| [cross/openapi.md](cross/openapi.md) | 7개 FastAPI의 팩토리·prefix·태그·operationId·securitySchemes·에러 envelope·페이지네이션·ETag·health·export 비교, 규약 초안 MUST/SHOULD/MUST NOT, 코드 후보 C1~C11 | §2.5, §2.6, §2.11, §3, §4, §5, §6 |
| [cross/ci-deploy.md](cross/ci-deploy.md) | 워크플로·게이트·하드닝·Dockerfile·compose·포트 대역·prod 런북·시크릿·백업·관측·ktdm 레지스트리, 재사용 워크플로 후보, 명명 표준, common 자체 CI | §1.2, §1.9, §1.10, §2.1, §3, §4 |
| [cross/docs-conventions.md](cross/docs-conventions.md) | AGENTS/CLAUDE/SKILL·우선순위·언어·원칙·리뷰·docs 트리·task ID·ADR·journal·환경·worktree·codegraph·PR·보안 감사 비교, canview 채택 충돌 C1~C16, AGENTS 공통 절 A~I | §1.1~1.20, §2, §3, §4 |
| [cross/canview-structure-checklist.md](cross/canview-structure-checklist.md) | canview 파일·AGENTS 절·규약을 항목 단위 체크리스트로 추출하고 common 미추적 scaffold와 diff 대조, validator 문법 명세 | §1.1~1.3, §2, §3, §4 |
| [cross/licensing.md](cross/licensing.md) | 저장소·패키지·벤더 tgz·스킬·의존성 라이선스와 출처, GNU FAQ 근거, 재라이선스 판정, 고지 파일·헤더·메타데이터 규약, 조치 L1~L16, 차단 B1~B8 | §2.1~2.5, §3.2~3.7, §4, §6 |

### 3.3 종합

| 문서 | 한 줄 설명 |
|---|---|
| [commonality-matrix.md](commonality-matrix.md) | (a) 영역×앱 매트릭스(●◐○×), (b) 후보별 판정표(배포 단위·1차 소비자·신뢰도·난이도), (c) 버전 정렬 격차 요약, (d) 차단 항목·열린 결정 목록 |
| `README.md`(이 문서) | 기준·문서 목록·읽는 순서·선행 보고서 관계·문서 간 불일치 |

## 4. 읽는 순서

### 4.1 설계자(common 패키지·규칙을 정하는 사람)

1. 이 문서 §5·§6 → `commonality-matrix.md` §1(매트릭스)·§4(열린 결정)로 결정 목록을 먼저 확보한다.
2. UI: `cross/design-tokens.md` §3.6 → `cross/ui-components.md` §4·§5.4·§6 → `cross/ux-patterns.md` §2·§3·§4.
3. 백엔드·계약: `cross/openapi.md` §3·§5 → `cross/backend.md` §3·§4·§5.
4. 플랫폼: `cross/version-matrix.md` §5·§7 → `cross/ci-deploy.md` §2·§3·§4.
5. 규약·저장소 골격: `cross/docs-conventions.md` §2·§3·§4 → `cross/canview-structure-checklist.md` §2·§3·§4.
6. 권리: `cross/licensing.md` §3·§4 — 코드 이동 전 차단 항목(B1~B8) 확인.

### 4.2 이관 담당(특정 앱을 common에 맞추는 사람)

1. 해당 앱 인벤토리 §8(공통화 후보)·§9(고유 차이)·§10(버전 표)·§11(미확인).
2. `commonality-matrix.md` §1에서 해당 앱 열, §3에서 버전 격차 행.
3. 앱별 도입 변경점: `cross/openapi.md` §4·§5, `cross/ci-deploy.md` §2.2, `cross/ui-components.md` §5.2(geo)·§3.1(Button 회귀 위험)·§3.3(DataTable), `cross/design-tokens.md` §3.6.4(브랜드 오버라이드).
4. airport는 `inventory/kor-travel-airport.md` §3.2(WIP)·§9, weather는 `inventory/kor-travel-weather.md` §9.1(v4 전환 정량), pinvi는 `inventory/pinvi.md` §3.2(모바일 v3 유지 사유)·`cross/licensing.md` §3.6을 추가로 읽는다.

### 4.3 리뷰어(조사 자체를 검증하는 사람)

1. 각 문서 말미의 근거 파일 목록(§12 또는 "근거 파일 목록")과 기준 커밋을 대조한다.
2. 이 문서 §6.2의 재확인 결과(직접 확인 명령 포함)를 먼저 보고, 남은 "미확인" 항목은 각 문서의 열린 질문 절(`인벤토리 §11`, 횡단 문서 말미 "열린 질문")에서 찾는다.
3. 선행 보고서와 결론이 다른 곳은 §5 표와 각 문서의 "선행 보고서" 절(`cross/design-tokens.md` §4, `cross/ui-components.md` §3.1·§3.3, `cross/ux-patterns.md` §1.14, `cross/backend.md` §6, `cross/openapi.md` §3.5, `cross/ci-deploy.md` §1.15, `cross/licensing.md` §5)에서 확인한다.

## 5. 선행 보고서(2026-09-05, geo `docs/kor-travel-common-library-review.md`)와의 관계

선행 보고서는 geo `daf079b`·pinvi `2396d65`·map `c72456f` 기준이며 UI 라이브러리 도입 검토가 주제였다. 이번 조사는 기준 커밋을 갱신하고(geo `1d9d74d`는 `daf079b` 직후, 코드 무변경 — `inventory/kor-travel-geo.md` 머리), airport·docker-manager·weather 백엔드·PinVi admin을 추가했다.

| 주제 | 선행 보고서 주장 | 이번 조사 결과 | 판정 | 근거 절 |
|---|---|---|---|---|
| 요구 범위 버전 표(§2) | `package.json` 요구 범위만 | 불일치 없음. lockfile 설치 버전·Python·CI·컨테이너·최신 대조를 추가 | 계승·보완 | `cross/version-matrix.md` 머리·§1~§4 |
| React 18/19 세대 차이(§2) | geo·docker-manager React 18 | 사실 재확인. dm은 업그레이드 계획 문서 없음(미확인), geo는 ADR-019 "peer 허용 범위 유지"만 | 계승 | `inventory/kor-travel-docker-manager.md` §3.1, `inventory/kor-travel-geo.md` §3.1 |
| pinvi admin `data-table.tsx`는 map 이식본(§3.1) | 30/28/27/0 수치 | 수치 일치. 정규화 후에도 27쌍 전부 차이, 그중 8쌍은 계약 차이. 이식 범위는 table뿐 아니라 filter-bar·pager·status-label 등 | 계승·보완 | `cross/ui-components.md` §2.1, `cross/ux-patterns.md` §1.14 |
| Button 계약 차이(§3.3) | geo Radix Slot / map base-ui / pinvi native | geo Slot은 통합 패키지 `radix-ui`; pinvi에는 Button이 **두 벌**(admin·user)이며 `loading` 포커스 처리가 반대; concierge는 map 계열; airport WIP는 shadcn 기본 레시피(세 번째 계열) | 보완 | `cross/ui-components.md` §3.1 |
| DataTable `manualSorting=true`(§3.4) | map·pinvi 기본 서버 정렬 | 두 `data-table.tsx`는 맞지만 pinvi 36페이지가 쓰는 `AdminTable` 어댑터는 `manualSorting=false` 고정 + `serverSort` opt-in | **보정** | `cross/ui-components.md` §3.3, `cross/ux-patterns.md` §1.14 |
| 토큰은 의미·크기 규약만 공유, 브랜드 값은 앱(§3.5) | 원칙 | 파일 단위 값·대비 수치로 뒷받침. 추가: hairline 2종, 불투명 tint, focus 단일 레시피, 대비 계산기 필요, `--ktc-` 접두는 concierge와 충돌, 마커 팔레트 P-xx가 map/pinvi에서 다른 hex | 계승·보완 | `cross/design-tokens.md` §3.3·§3.4·§3.5·§4 |
| 인증 경계는 화면이 비슷해도 다르다(§3.6) | 로그인·세션·CSRF 첫 범위 제외 | 동의. 단 공개 API 키 함수(4곳 동일)·trusted proxy 원시 함수·request-id 등 비인증 인프라는 근거 있음. weather 세션 상수는 geo와 일치 | 계승·보완 | `cross/backend.md` §2.8·§6, `inventory/kor-travel-weather.md` §3.1 |
| concierge는 작은 UI 부품 후보(§2) | map과 동일하다 볼 근거 없음 | button/card/input/tabs/field/AppShell이 map recipe를 명시적으로 이식 — "같은 계보의 부분집합" | 보정 | `inventory/kor-travel-concierge.md` §11.12 |
| 백엔드·인증 통합 근거 부족(§1) | 백엔드 전반 | 런타임 공유·SSO에는 동의. 계약 규칙과 얇은 코드(problem+json, request-id, export/drift, typegen)는 근거 있음(에러 본문 7종·페이지네이션 4형·health 4형·요청 ID 4형이 저장소 간 sha256 pin 비용으로 이미 나타남) | **부분 상이** | `cross/backend.md` §6, `cross/openapi.md` §3.5 |
| CI·lint·TS 설정 공통화 금지(§7.2) | 프레임워크를 숨기는 공통 설정 금지 | 동의. 대신 inputs로 폭을 조절하는 재사용 워크플로가 적합. 사용자 전제 (2)(도구 일치)와의 충돌은 결정 필요 | 계승·조건 | `cross/ci-deploy.md` §1.15·§2.1, `inventory/kor-travel-airport.md` §9 |
| 사전 빌드 CSS + CSS 변수 우선(§7.3) | 배포 방식 | weather·airport main처럼 Tailwind 없는 앱에는 유효하나 전제 (1)(v4 전환)과 방향이 다름 → 양자택일 | 조건 | `inventory/kor-travel-weather.md` §11.10, `cross/design-tokens.md` §3.6.3 |
| 이동 branch 직접 참조 금지(§8) | 운영 `latest`·branch 금지 | pinvi `apps/etl` `python-kasi-api@main`이 위반 사례; `latest-main` 태그는 로컬 빌드 태그라 핀 단위와 구분하면 무모순; RustFS/mc `latest`는 위반 | 계승·사례 | `cross/backend.md` §6, `cross/ci-deploy.md` §1.15 |
| 라이선스(§9) | geo·map·weather GPL, ktc·ktdm MIT, pinvi LICENSE 없음 | 일치. 추가: kta GPL 원문, map 25행 요약본, geo `-only`, 벤더 tgz 라이선스 부재, cva·pg-aiguide Apache-2.0 | 계승·보완 | `cross/licensing.md` §2.2·§5 |
| airport·ktdm UX·문서 규약·CI·포트 | 범위 밖 | 최초 정리 | 신규 | `inventory/kor-travel-airport.md`, `cross/docs-conventions.md`, `cross/ci-deploy.md` |

## 6. 문서 간 불일치 목록

### 6.1 대조 방법

- 인벤토리 7편의 §10 버전 표 각 셀 ↔ `cross/version-matrix.md` §1.1~§1.7, §2.1~§2.7, §3.1~§3.4.
- 인벤토리 §3 컴포넌트 인벤토리(파일명·줄 수·엔진) ↔ `cross/ui-components.md` §2.1~§2.3, `cross/ux-patterns.md` §1.1~§1.13.
- 인벤토리 §3 토큰 목록(radius·control·spacing·motion·z·brand) ↔ `cross/design-tokens.md` §3.1.1~§3.1.7, §3.2.
- 인벤토리 §6 포트 ↔ `cross/ci-deploy.md` §1.9.
- 인벤토리 머리 라이선스 행·`cross/backend.md` §2.1 ↔ `cross/licensing.md` §2.1·§5.
- 그 외 줄 수·개수·경로 수·TTL 같은 수치 주장을 문서 간 교차 grep했고, 어긋난 항목은 저장소에서 직접 재확인했다(재확인 명령은 `ls | wc -l`, `wc -l`, `git grep -l`, `python -c "json.load"`, `grep -n`; 읽기 전용).

### 6.2 발견한 불일치와 재확인 결과

| # | 축 | 문서 A | 문서 B | 재확인(2026-09-06, 기준 커밋) | 정본 판단 |
|---|---|---|---|---|---|
| 1 | 컴포넌트 | `inventory/pinvi.md` §3.1 "`components/admin/ui/*` 26개"(같은 문서 §1은 "프리미티브 28종") | `cross/ui-components.md` §2.1·§2.3, `cross/licensing.md` §2.3 P1 "28파일" | `ls apps/web/components/admin/ui \| wc -l` = **28** | 28. 인벤토리 §3.1 오기 |
| 2 | 컴포넌트 | `inventory/kor-travel-weather.md` §3.1 `admin-shell.tsx` "158(추정, 5,463B)" | `cross/ui-components.md` §2.2, `cross/ux-patterns.md` §1.1 "152" | `wc -l` = **152** | 152 |
| 3 | 컴포넌트 | `cross/ux-patterns.md` §1.13 pinvi Hallmark 스탬프 "38" | `cross/ui-components.md` §2.3 "39" | `git grep -l "Hallmark ·"` = **39**(map은 양쪽 88로 일치) | 39 |
| 4 | OpenAPI | `inventory/kor-travel-airport.md` §4.1 "`docs/openapi.json` 22 paths … 코드 라우트 22개와 일치" | `cross/openapi.md` §2.1 "경로 수 21" | `docs/openapi.json` paths=**21**, schemas=37; `main.py` 라우트 데코레이터는 22(동일 경로 다중 메서드 포함) | 21 paths. 인벤토리의 "22 paths" 오기, 스키마 37은 일치 |
| 5 | 인증 | `inventory/pinvi.md` §3.1 "`pinvi_access`(HS256 JWT **15분**)" | `cross/backend.md` §2.8 "JWT HS256 access(**10분**, `token_version`)" | `apps/api/app/core/config.py:656` `pinvi_access_token_minutes: int = 10` | 10분 |
| 6 | 문서 | `inventory/kor-travel-concierge.md` §5 README "약 130줄" | `cross/docs-conventions.md` §1.1 "205" | `wc -l README.md` = **205** | 205 |
| 7 | 문서 | `inventory/kor-travel-docker-manager.md` §5 `CLAUDE.md` "135" | `cross/docs-conventions.md` §1.1 "134" | `wc -l` = **134** | 134 |
| 8 | 라이선스 | `cross/backend.md` §2.1 "kta 라이선스 선언 없음(미확인)", §5.3·§7-8 "kta `LICENSE` 존재 여부 미확인" | `inventory/kor-travel-airport.md` 머리, `cross/licensing.md` §2.1 "GPL-3.0 원문" | `wc -l LICENSE` = **674**(geo와 동일 원문) | GPL-3.0. backend.md의 "선언 없음"은 `pyproject.toml` 메타데이터 부재로만 읽어야 함(licensing §5가 정정) |
| 9 | 라이선스 | `cross/backend.md` §2.1 "pinvi MIT" | `cross/licensing.md` §2.1 "루트 `LICENSE` 없음, `apps/api/pyproject.toml`만 MIT" | 인벤토리·licensing 일치 | licensing. backend.md 셀은 pyproject 값 |
| 10 | 라이선스 | `inventory/pinvi.md` §7 벤더 tgz "라이선스 MIT(문서)" | `cross/licensing.md` §2.2 D5·§2.5 "원천 GPL-3.0, tgz 내 표기 없음" | 인벤토리는 pinvi 문서를 옮겨 적은 것(문서 기재 자체는 사실) | 실제 권리는 GPL-3.0(licensing) |
| 11 | 라이선스 | `inventory/kor-travel-map.md` 머리 "`LICENSE` 첫 줄 `GNU GENERAL PUBLIC LICENSE / Version 3`"(전문 여부 미언급) | `cross/licensing.md` §2.2 D1 "25행 요약본" | `wc -l LICENSE` = **25** | 요약본. 인벤토리 서술은 참이지만 불완전 |
| 12 | 토큰 | `inventory/kor-travel-concierge.md` §3.1(`design.md` 인용) "보조 13.5px" | `cross/design-tokens.md` §3.1.4 "concierge xs **13**" | `frontend/tailwind.config.ts:29` `xs: 0.8125rem`(13px); `design.md:31`은 13.5px | 코드 13px. concierge 내부 문서-코드 drift; 인벤토리는 문서를, 횡단은 코드를 인용 |
| 13 | 기준 | `cross/licensing.md` §5 "kta `2bb1111`에 `components.json`·`shadcn` 없음, WIP는 다른 사본으로 보이며 미확인" | `inventory/kor-travel-airport.md` §3.2, `cross/ui-components.md` §0 "WIP `F:/dev/kor-travel-airport` @`99b3f98`" | 인벤토리가 `git show --stat`으로 확인 | WIP는 실재. licensing은 WIP 체크아웃을 열지 않았고, 추가 파일은 shadcn CLI 생성물이라 라이선스 판단(M1·C1 계열)에 영향 없음 |
| 14 | 기준 | `cross/design-tokens.md` §1, `cross/docs-conventions.md` 기준 canview `d078437` | `cross/licensing.md` §0, `cross/canview-structure-checklist.md` 기준 `1f93b8a` | checklist 기준 표: 직후 1커밋, 문서 규약 파일 차이 없음 | 둘 다 유효. 이 README §2.2에 병기 |
| 15 | 규약 | `cross/docs-conventions.md` §3.3-3·4·7 "체크박스 원장 + `validate_task_ledger.py`(후보)" | `cross/canview-structure-checklist.md` §1.2·§4.1·Q3 "common `tasks-rule.md` §4와 무변경 `validate_plan.py`는 5열 표를 요구" | common 작업 트리 `tools/validate_plan.py`는 5열 표 파서 | **미결**(설계 결정) — `commonality-matrix.md` §4.2 |
| 16 | 규약 | `cross/docs-conventions.md` §4 "`docs/decisions.md` 불필요" | common `docs/runbooks/documentation-maintenance.md`(`cross/canview-structure-checklist.md` §1.2·Q1) "갱신 필수" | 두 문서 모두 사실을 적음 | 미결 |
| 17 | 규약 | `cross/docs-conventions.md` §2 C11 "절대 링크 접두 허용 제거" | common `tools/validate_document_links.py` 사본(`cross/canview-structure-checklist.md` §1.2·Q2) "접두 유지·치환" | 사본 diff로 확인 | 미결 |
| 18 | 빌드 | `inventory/pinvi.md` §4.1 "`Dockerfile`·CI는 `pip install -e ".[dev]"`" | `cross/version-matrix.md` §2.1, `cross/backend.md` §2.1 "Docker `pip install -e .`" | `apps/api/Dockerfile:42` `pip install -e .`, `api.yml:114` `pip install -e ".[dev]"` | Docker는 `-e .`, CI는 `.[dev]`. 인벤토리 축약 오기(uv.lock 미소비라는 결론은 동일) |
| 19 | 빌드 | `cross/backend.md` §2.1 "ktdm Docker Python 미확인(호스트 실행 **추정**)" | `inventory/kor-travel-docker-manager.md` §2·§6 "Dockerfile 없음, systemd+venv 실행(**사실**)" | 인벤토리가 `git ls-files`로 확인 | 사실로 확정 |

### 6.3 대조했으나 불일치를 찾지 못한 축

- **버전 표 vs version-matrix**: 인벤토리 7편 §10의 선언/설치 셀(next·react·typescript·tailwind·base-ui/radix·shadcn·lucide·eslint·vitest·playwright·react-query·zod·zustand·rhf·maplibre·python·fastapi·pydantic·sqlalchemy·alembic·asyncpg/psycopg·ruff·mypy·pytest·dagster·provider git SHA)을 `cross/version-matrix.md` §1~§2와 대조한 결과 값 차이는 없었다. 표기 차이만 있다(예: airport `postcss` "없음(next 내부) 8.5.23" ↔ "(전이) 8.5.23").
- **포트 vs ci-deploy**: 7개 인벤토리 §6의 포트가 `cross/ci-deploy.md` §1.9 대역표와 모두 일치한다. 단 한쪽에만 기록된 저장소 내부 drift 2건이 있다 — airport `docs/tasks.md`의 옛 값 `14000/14001`(`inventory/kor-travel-airport.md` §9만), map `docs/integration-map.md` §1의 PinVi 옛 기본값 `9021/9022`(`cross/ci-deploy.md` §1.9만).
- **토큰 값 vs design-tokens**: radius·control 높이·spacing 단계·motion·z-index·brand hue·shadow가 인벤토리와 일치한다(항목 12의 concierge 13/13.5만 예외).

## 7. 열린 결정·차단 항목

설계 단계에서 결정해야 할 질문과 권리 확인 전 이동 금지 항목은 `commonality-matrix.md` §4에 모아 두었다(차단 8 + 결정 약 40). 각 횡단 문서의 "열린 질문" 절이 원본이다.

## 8. 갱신 규칙

- 조사 문서는 §2.1의 기준 커밋에 고정된 스냅샷이다. 저장소가 바뀌어도 본문을 고치지 않고, 재조사 시 기준 커밋을 갱신한 새 절 또는 새 문서를 만든다(`docs/runbooks/documentation-maintenance.md` §2 "조사 기준 커밋 갱신").
- 이 README §6.2의 오기(항목 1·2·4·5·6·7·11·18)는 해당 인벤토리를 수정하지 않고 여기에 정정 기록으로만 둔다. 설계 문서는 정정된 값을 인용한다.
- 문서 링크는 저장소 상대 경로만 쓴다(`cross/docs-conventions.md` C11).
