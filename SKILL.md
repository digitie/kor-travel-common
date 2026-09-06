# SKILL — kor-travel-common 작업 라우터

이 파일은 kor-travel-common 작업에 필요한 상세 문서를 빠르게 고르는 라우터다. 저장소 정책과 금지선의 정본은 [AGENTS.md](AGENTS.md)이며, 이 파일에 같은 규칙을 복제하지 않는다. 확정 task: T-001 · 마지막 갱신: 2026-09-06.

## 1. 최소 컨텍스트

모든 저장소 작업은 다음 순서로 시작한다.

1. [AGENTS.md](AGENTS.md)
2. [docs 문서 지도](docs/README.md)
3. [현재 상태](docs/resume.md)
4. 해당 상세 task가 있는 경우 그 파일 한 개

전체 `docs/`, 모든 ADR, 모든 task, `docs/survey/` 전체, 과거 review와 journal을 한꺼번에 읽지 않는다. 작업 대상이 정해지지 않았을 때만 [task 요약](docs/tasks.md)을 연다. task가 없는 문서·review 요청은 해당 runbook 또는 review template을 기준으로 삼는다.

## 2. 작업별 시작점

| 작업 | 첫 문서 | 이어서 볼 대상 |
|---|---|---|
| 배포 단위·의존 방향·경계 | [architecture](docs/architecture/README.md) | [packages](docs/architecture/packages.md), ADR-001 |
| 디자인 토큰(`--kt-*`·프로필·다크·대비) | [design tokens 규약](docs/standards/design-tokens.md) | [style delivery](docs/architecture/style-delivery.md), T-101~T-104 |
| React UI 컴포넌트·마크업 계약 | [ui contract](docs/standards/ui-contract.md) | [frontend stack](docs/standards/frontend-stack.md), T-201~T-213 |
| UX 규칙(셸·확인 다이얼로그·토스트·상태) | [ux guide](docs/standards/ux-guide.md) | `tools/ux_lint.py`(T-103), T-105 |
| PC/Mobile Web·breakpoint·터치 타깃 | [responsive web](docs/standards/responsive-web.md) | T-106, playwright 기준선 템플릿(T-108) |
| OpenAPI·REST·health·request-id | [openapi 규약](docs/standards/openapi.md) | `docs/standards/openapi-exceptions.yaml`, T-301 |
| Python 공통 모듈·extras·품질 도구 | [backend stack](docs/standards/backend-stack.md) | T-302~T-310 |
| 라이브러리/플랫폼 버전 정렬·예외 | [versions 규약](docs/standards/versions.md) | `versions.json`, `tools/check_versions.py`, T-005 |
| CI·재사용 워크플로·포트·컨테이너 명명 | [ci-deploy 규약](docs/standards/ci-deploy.md) | `.github/workflows/`, T-009·T-010 |
| 라이선스·출처·SPDX 헤더 | [licensing 규약](docs/standards/licensing.md) | `NOTICE`, `THIRD_PARTY_NOTICES.md`, `PROVENANCE.md`, T-003 |
| 소비자 채택·이관 PR | [consumer adoption](docs/runbooks/consumer-adoption.md) | [adoption readiness](docs/architecture/adoption-readiness.md), [integration map](docs/integration-map.md), T-4xx |
| 릴리스(rc·태그·tarball·wheel) | [release](docs/runbooks/release.md) | `CHANGELOG.md`, T-109·T-212·T-310 |
| 소비자용 AGENTS/CLAUDE 템플릿·설정 조각 | [agent conventions](docs/standards/agent-conventions.md) | [templates](templates/README.md) |
| 개발 환경·Windows·검증 명령 | [dev environment](docs/dev-environment.md) | [tools](tools/README.md) |
| 통합 순서·Phase·중단 조건 | [integration plan](docs/plan/integration-plan.md) | [설계 브리프](docs/plan/design-brief.md) |
| 규칙의 사실 근거 확인 | [조사 안내](docs/survey/README.md) | [commonality matrix](docs/survey/commonality-matrix.md), 해당 `cross/`·`inventory/` 절 |
| 기존 결정 변경 | [ADR 색인](docs/adr/README.md) | 관련 ADR 하나, [documentation maintenance](docs/runbooks/documentation-maintenance.md) |
| 적대적 리뷰 | [review archive](docs/reviews/README.md) | [template](docs/reviews/adversarial/TEMPLATE.md)과 관련 diff |
| branch·PR·merge | [agent workflow](docs/runbooks/agent-workflow.md) | 실패했을 때만 [failure patterns](docs/runbooks/agent-failure-patterns.md) |
| task 작성·완료 | [tasks rule](docs/tasks-rule.md) | [tasks](docs/tasks.md), `python3 -B -X utf8 tools/validate_plan.py` |

## 3. 저장소 영역

    packages/tokens/               — 디자인 토큰 패키지(정본 tokens.css·theme.css·shadcn.css·base.css·생성물)
    packages/ui/                   — React 19 UI 패키지(프리미티브·컴포넌트·cn·인라인 아이콘)
    packages/py/kor-travel-common/ — Python 공통 패키지 kortravelcommon(extras: api·db·dagster·testing·http)
    templates/                     — 소비자 설정 조각(AGENTS 공통 절·CLAUDE 포인터·eslint·dependabot·PR·체크리스트)
    versions.json                  — 버전 레지스트리(floor/recommended/exceptions/blocked/consumers.enforce)
    tools/                         — 문서·계획·버전·대비·UX·SPDX 검사 도구(Python stdlib, Windows Tier 2)
    tests/                         — 도구 회귀 시험
    .github/workflows/             — common CI와 소비자용 재사용 워크플로
    docs/standards/                — 소비 저장소 전체가 따르는 공통 규칙 정본
    docs/architecture/             — 배포 단위·의존 방향·스타일 배포·소비자·채택 준비·canview 대조표
    docs/adr/                      — 구조적 결정(단일 색인 README, 다음 후보 번호 명시)
    docs/plan/                     — 설계 브리프·통합 계획·설계 패널 기록
    docs/survey/                   — 기준 커밋 고정 조사(근거, 규범 아님)
    docs/runbooks/                 — 반복 절차(workflow·adoption·release·문서 유지·실패 패턴)
    docs/reviews/                  — 변경하지 않는 review 기록과 색인
    docs/tasks/                    — task별 실행 명세

## 4. 핵심 용어

값·규칙의 정본은 각 standards 문서와 machine-readable 파일이며, 이 표는 어휘를 빨리 맞추기 위한 안내다.

| 용어 | 의미 |
|---|---|
| common | 이 저장소 `kor-travel-common` |
| 소비자 | kor-travel-airport(kta)·kor-travel-concierge(ktc)·kor-travel-docker-manager(ktdm)·kor-travel-geo(geo)·kor-travel-map(map)·kor-travel-weather(wx)·pinvi 7개 저장소. pinvi는 admin/사용자 웹/모바일 세 표면 |
| 배포 단위 | tokens·ui·py 3 코드 패키지 + `docs/standards/*` + `templates/*` + `versions.json`·`tools/*.py` |
| `--kt-*` / `kt-` | 공통 semantic 토큰 변수 접두와 Tailwind 유틸리티 접두(`bg-kt-surface-page`, `h-kt-control`). 전 저장소 0회 사용이라 충돌 없음(열림 O-4, 기본값) |
| 토큰 정본 | `packages/tokens/tokens.css`. `tokens.json`(DTCG)·`tokens.ts`·`tailwind-preset.cjs`는 생성물(빌드 diff 검사) |
| 계층 | semantic 토큰 ← 앱 override 2단. 오버라이드 허용 목록은 brand·focus·surface·text·status·font 스택 |
| 프로필 | 토큰 밀도 프로필 `admin` / `consumer`. consumer 값은 pinvi 소유, common은 의미 이름만 |
| shadcn alias | 의미 고정: `--input`=control-line, `--accent`=brand-tint, `--radius`=radius-control, `--border`=장식 border |
| 소비자 필수 2줄 | `@import "@kor-travel/tokens/theme.css"` + `@source "../node_modules/@kor-travel/ui"` |
| 별칭 shim | `aliases/map-vocabulary.css` — map·weather·geo 공통 레거시 이름 → `--kt-*`(선택 파일) |
| `base.scoped.css` | `[data-kt-surface]` 스코프 변형. pinvi admin처럼 한 앱에 두 표면이 있을 때 사용 |
| 마크업 계약 | `data-slot`·testid·heading 구조·sr-only 문구. 변경은 0.x minor(이관 절 필수)/1.x major |
| OpenAPI 3계층 | M(MUST) / S(SHOULD) / N(MUST NOT). 즉시 MUST는 M2·M4·M9·N6·N7, 나머지는 신규 표면 MUST·기존 표면 SHOULD + 예외 등록 |
| problem+json | RFC 7807 에러 본문 + 확장 멤버 `code`(UPPER_SNAKE)·`request_id`·`errors[]` |
| `X-Request-ID` | UUID v4/v7 또는 ULID, ≤128자 ASCII. 검증 실패 시 서버 발급 |
| 운영 경로 | `/health`(liveness)·`/readyz`(의존성)·`/version`. geo `/v1/healthz` 별칭은 등록 예외 |
| 예외 레지스트리 | `docs/standards/openapi-exceptions.yaml` `{app, rule, surface, reason, sunset, review, owner}` |
| PC/Mobile | admin PC-first + ≥320px 컨테인(문서 가로 스크롤 금지) / 사용자 웹 mobile-first(44px·16px 입력) / 모바일 앱 48px |
| breakpoint | sm 640 / md 768 / lg 1024(셸 전환) / xl 1280(inspector rail). 검사 폭 320/375/414/768/1024/1440 |
| 레지스트리 | `versions.json`(schema `kor-travel-common.version-registry.v1`): 축별 `floor`/`recommended`, `exceptions[]{repo,key,installed,reason,until,review}`, `blocked[]`, `consumers.<repo>.enforce` |
| 판정 어휘 | `OK`/`BELOW_FLOOR`/`ABOVE_MAX`/`NOT_RECOMMENDED`/`NO_LOCK`/`NO_ENGINES`/`FLOATING_REF`/`BLOCKED`/`EXEMPT`/`EXEMPT_EXPIRED` |
| 강제 3단 | `report` → `warn` → `fail`. 승격은 common `versions.json`이 소유하며 소비자 report 2회 연속 위반 0이 조건 |
| 매니페스트 | 소비 저장소의 `kor-travel-common.lock.json`(schema `kor-travel-common.consumer-manifest.v1`). `enforce`는 두지 않음 |
| 이관 PR | 한 PR = 한 산출물, 프레임워크 업그레이드와 분리, `git revert` 1회 원복, lock 동반, 파일 상한(tokens 10·ui 30·py 10) |
| 시각 기준선 | 6폭 스크린샷(320/375/414/768/1024/1440)을 착수 전 캡처하고 완료 diff와 함께 PR evidence로 남김(저장소 파일 아님) |
| `NOT_RUN(사유)` | common에서 실행하지 못한 검증 표기. DONE 전 `외부 선행`으로 승격하며 0 test·skip은 pass가 아님 |
| 외부 선행 | common이 대체할 수 없는 결정: L6(pinvi 라이선스), L8(ktc·ktdm GPL 정렬), airport WIP 병합, geo React 19 |
| 열림(O-n) | 사용자 확인 대기 결정. 기본값으로 진행하며 문서에는 "열림(사용자 확인 필요)"와 기본값을 함께 적음 |
| 릴리스 태그 | `tokens-vX.Y.Z`·`ui-vX.Y.Z`·`py-vX.Y.Z`, `-rc.N` 선행. 태그 불변, 같은 버전 재발행 금지, `@main` 참조 금지 |
| SemVer 0.x | minor = 파괴 허용(rc + 소비자 PR 검증 + `### Breaking` + 이관 절), patch = additive. 1.0은 GPL 소비자 3곳 채택 후 |

## 5. 종료 경로

검증, 전문 리뷰어 2인의 독립 적대적 리뷰, 문서 갱신, 보안 점검, PR과 worktree 정리는 [agent workflow](docs/runbooks/agent-workflow.md)를 따른다. 패키지·규약 버전 발행은 [release](docs/runbooks/release.md), 소비자 PR은 [consumer adoption](docs/runbooks/consumer-adoption.md), 문서 역할과 기록 형식은 [documentation maintenance](docs/runbooks/documentation-maintenance.md)를 필요할 때만 읽는다.
