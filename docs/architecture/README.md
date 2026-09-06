# kor-travel-common 아키텍처

- 정본 지위: 현재 설계의 상위 정본(초안). 확정 task: T-008(초기판, ★이번 PR) → T-101·T-201·T-302(실물 패키지와 대조해 확정). 마지막 갱신: 2026-09-06.
- 근거: [브리프](../plan/design-brief.md) D-01·D-02·D-09~D-12·D-15·D-31, `docs/survey/commonality-matrix.md` §1·§2, `docs/survey/cross/ui-components.md` §4·§6.2, `docs/survey/cross/backend.md` §3~§5, `docs/survey/cross/design-tokens.md` §3.6.

이 문서는 kor-travel-common의 배포 단위, 의존 방향과 책임 경계를 설명하는 상위 아키텍처 정본이다. 여기서 전체 형태를 확인한 뒤 변경 대상에 해당하는 상세 문서만 읽는다. 소비자별 채택 gate는 [채택 준비 기준](adoption-readiness.md), 결정의 역사는 [ADR 색인](../adr/README.md), 현재 작업은 [tasks](../tasks.md)를 따른다. 이 문서와 하위 architecture 문서는 정본 초안이며, 실물 패키지(T-101 tokens·T-201 ui·T-302 py)와 대조해 확정하는 task가 남아 있다.

## 문서 사용법

| 변경 대상 | 상세 정본 |
|---|---|
| 패키지 이름·경로·exports·peer·배포 채널·공개 계약 | [패키지](packages.md) |
| CSS 파일 구성·Tailwind v4 연결·`kt-` 네임스페이스·프로필 스코프·대비 검사 | [스타일 배포](style-delivery.md) |
| 소비자별 현재 상태·채택 순서·선행 조건 | [소비자](consumers.md) |
| 소비자별 채택 gate와 현재 판정 | [채택 준비 기준](adoption-readiness.md) |
| 소비자별 채택 버전(생성물) | [통합 지도](../integration-map.md) |
| canview 구조·AGENTS 절·규약 대비 채택/변형/제외 | [canview 대조표](canview-checklist.md) |
| 토큰 이름·역할·오버라이드 허용 목록·대비 규칙 | [design-tokens](../standards/design-tokens.md) |
| 컴포넌트 마크업 계약(data-slot·testid·sr-only) | [ui-contract](../standards/ui-contract.md) |
| UX 규칙·PC/Mobile 규약 | [ux-guide](../standards/ux-guide.md), [responsive-web](../standards/responsive-web.md) |
| OpenAPI/REST 규약·예외 레지스트리·health 경로 | [openapi](../standards/openapi.md) |
| 버전 기준선·판정 어휘·강제 수준 | [versions](../standards/versions.md), `versions.json` |
| Python 패키지 구조·extras·모듈 우선순위 | [backend-stack](../standards/backend-stack.md) |
| 프론트 스택·ESLint/tsconfig 조각 | [frontend-stack](../standards/frontend-stack.md) |
| CI 하드닝·재사용 워크플로·포트·명명 | [ci-deploy](../standards/ci-deploy.md) |
| 라이선스·고지·SPDX 헤더·추출 gate | [licensing](../standards/licensing.md) |
| 릴리스 절차(rc → 소비자 PR → 정식) | [release runbook](../runbooks/release.md) |
| 소비자 이관 절차·되돌리기·PR 본문 | [consumer adoption runbook](../runbooks/consumer-adoption.md) |

규칙 문서(`docs/standards/`)와 조사 문서(`docs/survey/`)는 architecture의 입력이지만 각각 규칙과 관찰의 정본이다. 일반 작업에서 위 문서를 모두 선제적으로 읽지 않는다.

## 1. 범위

kor-travel-common은 kor-travel 제품군의 UI·백엔드 공통 코드와 공통 규칙(색상 톤·UX·OpenAPI·PC/Mobile Web·라이브러리/플랫폼 버전 일치)을 정의하는 GPL-3.0-or-later 라이브러리다. 소비자는 7개 저장소(kor-travel-airport·kor-travel-concierge·kor-travel-docker-manager·kor-travel-geo·kor-travel-map·kor-travel-weather·pinvi)이며 pinvi는 admin·사용자 웹·모바일 세 표면으로 나뉜다. kor-travel-airport Admin(현 실체는 무인증 백업·collector-status 패널, D-20)과 PinVi Admin은 소비자에 포함한다.

배포 단위는 다음 여섯 가지다(D-01).

| 배포 단위 | 경로 | 형태 | 소비 방식 | 1차 소비자(D-16) |
|---|---|---|---|---|
| `@kor-travel/tokens` | `packages/tokens` | npm(CSS 정본 + 생성물 JSON/TS/v3 preset) | tarball URL 설치 + `@import` | map·weather → pinvi admin(L6 완료 조건)·airport(WIP 병합 후) |
| `@kor-travel/ui` | `packages/ui` | npm(ESM + d.ts + Tailwind 소스 클래스) | tarball URL 설치 + `@source` | map·pinvi admin(L6) 또는 airport 소형 부품 |
| `kor-travel-common`(import `kortravelcommon`) | `packages/py/kor-travel-common` | Python(hatchling, extras) | git 태그 + wheel 자산, `uv.lock` | map-api·weather-api·airport |
| 규칙 문서 | `docs/standards/*` | Markdown + `openapi-exceptions.yaml` | 참조(코드 링크 없음) | 전 소비자(ktc·ktdm은 L8 전 규칙 참조까지만) |
| 템플릿 | `templates/*` | 복사형 파일(AGENTS 공통 절·에이전트 설정·PR 본문·ESLint 조각·dependabot·playwright 기준선) | 복사 후 앱 소유 | 전 소비자 |
| 레지스트리·도구 | `versions.json` + `tools/*.py` + `.github/workflows/*`(재사용 워크플로) | JSON + Python stdlib 스크립트 + `workflow_call` | 소비자 CI가 태그/SHA로 호출 | 전 소비자 |

패키지명 `@kor-travel/<pkg>`는 잠정이며 T-006에서 npm scope 확보에 실패하면 `@digitie/kor-travel-<pkg>`로 개명한다(O-5, 첫 소비자 PR 전이면 비용 0).

만들지 않는 것: `config` npm 패키지(`templates/eslint/*.mjs` 조각과 [frontend-stack](../standards/frontend-stack.md)으로 대체), `api-client-core`(Phase 5 T-508 재평가), 아이콘 패키지(ui는 인라인 SVG, `lucide-react` peer 없음 — `vm` §1.3의 0.363~1.41 혼재), shadcn 전면 레지스트리(셸·로그인·playwright 기준선 템플릿 채널만, T-211).

소비자 한 곳에 있다는 이유만으로 공통화하지 않는다. common은 앱 도메인 모듈, 지도 엔진(`maplibre-vworld-react`·`maplibre-vworld-js`), provider 라이브러리(`python-*-api`·`python-kraddr-base`), 인증 서비스(비밀번호·세션·CSRF·JWT·RBAC)를 갖지 않으며 이들과 중복되는 코드를 만들지 않는다(`be` §4, `ui` §4.3, `lic` §4 B2).

## 2. 데이터·의존 흐름

    소비 저장소(앱)
      │
      ├─ 프론트엔드(Next.js 16, Tailwind v4)
      │     ├──► @kor-travel/ui ──► @kor-travel/tokens      (ui는 tokens 같은 minor를 peer)
      │     └──► @kor-travel/tokens                         (tokens만 채택하는 앱: React 18·Tailwind 없는 앱)
      │
      ├─ 백엔드(FastAPI) ──► kor-travel-common[core|api|db|http|dagster|testing]
      │
      ├─ 규칙 문서 참조 ──► docs/standards/*                  (코드 링크 없음 → 라이선스 gate와 독립)
      ├─ 템플릿 복사   ──► templates/*                        (복사 후 앱 소유)
      │
      └─ kor-travel-common.lock.json(매니페스트)
                │
                ▼
          tools/check_versions.py ◄── versions.json(레지스트리, enforce 소유)
                │
                ▼
          docs/integration-map.md(생성물, T-012)

의존 규칙은 다음과 같다.

1. 방향은 앱 → ui → tokens, 앱 → py의 단방향이다. tokens은 어떤 패키지도 import하지 않는다(React·Tailwind 무관; `theme.css`만 소비자의 Tailwind v4 빌드 컨텍스트 안에서 의미를 가진다). py는 프론트와 독립이며 core는 stdlib + pydantic만 의존한다(D-15).
2. common은 소비자 코드를 import하지 않는다. 앱 도메인·지도·provider·인증은 §1의 금지 경계다. 소비자 저장소를 직접 수정하지 않고 PR 요청 문서(T-020·T-021·T-505)로 요청한다.
3. 규칙 문서는 코드 링크 없이 참조되므로 GPL 결합 판단(`lic` §3.6)과 독립이다. MIT 앱(ktc·ktdm)은 L8 결정 전까지 규칙 문서와 `tokens.json` 참조까지만 허용한다(D-16).
4. 매니페스트 → `check_versions` → `integration-map`은 보고 경로이며, 강제 수준(`enforce`)은 common `versions.json`이 소유한다(D-07·D-30).
5. 벤더링 원본(shadcn 생성물·map 유래 파일)은 `PROVENANCE.md`와 SPDX/`Origin:` 헤더로 출처를 남기며(D-17), 생성물(`tokens.json`·`tokens.ts`·`tailwind-preset.cjs`)은 정본 `tokens.css`에서만 만든다.

## 3. 책임과 경계

| 계층 | 허용 책임 | 금지 책임 |
|---|---|---|
| `@kor-travel/tokens` | `--kt-*` 의미 토큰 이름·역할·기본값(map 값)·`.dark` 값, `kt-` 유틸리티 매핑, shadcn alias 의미 고정, 프로필 admin 값, base 레시피(focus·hairline·reduced-motion), 별칭 shim, 생성물 | 앱 브랜드 값 확정, consumer 프로필 값(pinvi 소유), 마커 팔레트 hex(map 소유), 폰트 파일 배포·로딩, 다크 활성화 강제 |
| `@kor-travel/ui` | 프리미티브·부품의 마크업 계약(data-slot·testid·heading·sr-only), 키보드·포커스 동작, prop 기본값, `cn`, 인라인 아이콘, React 19 전용 구현 | 앱 도메인 부품, 지도 뷰, 셸 nav·로그아웃·RBAC, 토스트·모달 엔진 선택(정책만), 세션·인증, 앱 고유 확장의 흡수 없는 복제 |
| `kor-travel-common`(py) | openapi export CLI, health/readyz/version, time, quality 베이스, settings 베이스, db 엔진 팩토리, public_api_key, request_id, metrics, problem+json, security_headers, cors, trusted_proxy, testing 픽스처, alembic 템플릿, http, dagster 어댑터 | 비밀번호·세션·CSRF·JWT·RBAC, 도메인 결합 부분(geo loaders·map RoutePolicy·pinvi M05 등, `be` §4), 좌표 경계 상수 공통화, provider 재래핑, 서비스 간 클라이언트 |
| `docs/standards/*` | 규칙 ID(TK-n·UX-Gn.m·M/S/N·판정 어휘)·MUST/SHOULD·예외 레지스트리 형식·검사 도구 지정 | 앱별 예외 값 본문 수록(예외는 레지스트리·앱 baseline 파일로), 조사 기록, 특정 앱 절차 |
| `templates/*` | 복사 시점의 정본 사본, 형식·필수 항목 | 복사 후 앱 파일의 동기화 강제(drift는 `ui_drift`·분기 감사로 보고만) |
| `versions.json`·`tools/*.py`·재사용 워크플로 | floor/recommended/exceptions/blocked, `enforce` 모드, 판정 어휘, 매니페스트 스키마, 대조·대비·UX lint·SPDX 검사, `workflow_call` job | 앱 워크플로 전면 대체, 운영 호출 job(kta `live-e2e`) required 지정, provider SHA 정렬 주체(보고만, O-16) |
| 소비자(앱) | 브랜드 오버라이드 값(허용 목록 내), 밀도 프로필 선택, 토스트·모달 엔진, 폰트 로딩, AppId·헤더 이름, 메트릭 접두, `AdminTable` 같은 어댑터, 매니페스트·baseline 파일, 시각 기준선 evidence | common 내부 클래스·마크업 우회 패치(불가피하면 종료 조건과 함께 기록, ≥2회면 배포 방식 재검토 D-28), `@main` 참조, `enforce` 자율 선언 |
| 공유 라이브러리(`maplibre-vworld-*`·`python-*-api`) | common과 무관하게 각 저장소가 소유 | common이 복제·재래핑·재배포(영구 금지, B2); `versions.json` `providers` 절은 보고만 |

공통화 승격은 다음 네 요소가 동시에 맞아야 한다.

1. 사실 근거: 소비자 2곳 이상에서 같은 목적의 구현이 확인된다(`docs/survey/commonality-matrix.md` §1의 ●/◐). 소비자 1곳 관찰만으로 규칙·컴포넌트를 승격하지 않는다.
2. 권리: 원천 파일의 라이선스 gate(`lic` §4 B1~B8)를 통과하고 `PROVENANCE.md`에 원천 커밋·경로·라이선스를 기록했다.
3. 계약: 해당 규칙 문서(`ui-contract`·`openapi`·`design-tokens`)에 계약 항목이 있고 계약 시험(단위·drift·대비)이 있다.
4. 버전: `CHANGELOG.md` 항목과 SemVer 판정(§4)이 있다.

하나라도 빠지면 앱에 잔류시키고 이유를 task 또는 `docs/adr/`에 기록한다.

## 4. 릴리스·버전 경계

| 단계 | 허용 변경 | 검증 | 소비자 영향 |
|---|---|---|---|
| 0.x patch | 비파괴(additive)만 | 패키지 CI(`packages`·`python-package`) green | 소비자 범위 `~0.N` 안에서 채택 |
| 0.x minor | 파괴 허용 | `-rc.N` 태그 → 소비자 PR 검증 → 정식; `CHANGELOG.md` `### Breaking` + 이관 절 필수 | 소비자 PR 필요(이관 절 따라) |
| 1.0 | GPL 소비자 3곳(map·weather·airport 또는 geo) 채택 후 | 릴리스 runbook 1회 완주(T-501) | 1.x major에서만 파괴 |

파괴 항목(D-31): 토큰 이름/의미, data-slot·testid, prop 기본값(예: DataTable `manualSorting`), 정렬 모드, CSS 파일 경로. 토큰 이름 폐기는 1 minor 동안 alias를 유지한다. tokens·ui·py는 독립 버전이며 ui는 tokens 같은 minor를 peer로 요구한다.

릴리스 채널(D-11): 패키지별 태그(`tokens-vX.Y.Z`·`ui-vX.Y.Z`·`py-vX.Y.Z`), 태그 불변, 같은 버전 재발행 금지, `@main` 참조 금지. 강제 수준은 소비자별 `report → warn → fail`이며 승격은 common PR로만 한다(D-30). 릴리스 절차는 [release runbook](../runbooks/release.md), 채택 절차는 [consumer adoption runbook](../runbooks/consumer-adoption.md)이 정본이다.

## 5. 저장소 구조

    AGENTS.md · CLAUDE.md · SKILL.md · README.md   — 정책 정본·포인터·라우터·문서 지도
    CHANGELOG.md                                      — 패키지별 H3, `### Breaking`
    NOTICE · THIRD_PARTY_NOTICES.md · PROVENANCE.md · CONTRIBUTING.md · LICENSES/
    versions.json                                     — 버전 레지스트리(schema version-registry.v1)
    consumers.pins.json                               — consumer-smoke 대표 소비자 pinned SHA(T-010)
    packages/tokens/                                  — @kor-travel/tokens
    packages/ui/                                      — @kor-travel/ui
    packages/py/kor-travel-common/                    — kortravelcommon
    templates/                                        — 소비자 복사형 파일
    tools/                                            — validator·check_versions·kt_contrast·ux_lint·check_spdx 등
    tests/                                            — 도구 회귀 테스트
    .github/workflows/                                — common CI + 재사용 워크플로
    docs/README.md · docs/resume.md · docs/journal.md — 문서 지도·진척·일지
    docs/architecture/                                — 이 문서·packages·style-delivery·consumers·adoption-readiness·canview-checklist
    docs/standards/                                   — 규칙 정본
    docs/adr/                                         — 결정 기록(단일 색인)
    docs/runbooks/                                    — 반복 절차
    docs/reviews/                                     — 독립 리뷰 아카이브
    docs/tasks.md · docs/tasks/ · docs/tasks-done.md  — 작업 원장
    docs/plan/                                        — 브리프·통합 계획
    docs/survey/                                      — 조사(규범 아님)
    docs/integration-map.md                           — 채택 지도(생성물)
    docs/dev-environment.md                           — 개발 환경 프로필

## 6. 문서 정본

| 목적 | 정본 |
|---|---|
| 배포 단위·의존 방향 | 이 문서와 [패키지](packages.md) |
| 스타일 배포 계약 | [스타일 배포](style-delivery.md), 값 정본은 `packages/tokens/tokens.css` |
| 소비자 상태·gate | [소비자](consumers.md), [채택 준비 기준](adoption-readiness.md), [통합 지도](../integration-map.md) |
| 공통 규칙 | [standards 색인](../standards/README.md) |
| 결정 | [ADR 색인](../adr/README.md) |
| 진척 | [resume](../resume.md), [journal](../journal.md) |
| 작업 | [task 요약](../tasks.md)과 `docs/tasks/`, [통합 계획](../plan/integration-plan.md) |
| 조사 근거 | [survey 안내](../survey/README.md), [공통화 매트릭스](../survey/commonality-matrix.md) |
