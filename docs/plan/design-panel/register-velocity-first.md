# kor-travel-common 결정 레지스터 — 소비자 이관 속도·단순성 우선(velocity-first) 관점

- 작성일: 2026-09-06
- 관점: 7개 소비 저장소가 **가장 적은 PR·가장 적은 breaking**으로 common을 채택하도록 설계한다. "복사 소유(shadcn 레지스트리) + 얇은 규칙 + 점진 채택"을 기본으로 하되, 드리프트 재발을 막는 자동 검사(버전 대조·대비 검사·OpenAPI drift·레지스트리 drift)를 첫 릴리스에 포함한다.
- 입력: `docs/survey/README.md`, `commonality-matrix.md`, `cross/*.md` 10편, `inventory/*.md` 7편(§1·§8·§9·§11), coordinator 초안(D-01~D-18, F절), `docs/tasks-rule.md`, `docs/runbooks/documentation-maintenance.md`, `docs/reviews/README.md`, `tools/validate_plan.py`, 선행 보고서(geo `docs/kor-travel-common-library-review.md`).
- 표기: **사실** = 조사 문서가 기준 커밋에서 확인한 것. **후보** = 이 레지스터의 제안. **추정** = 정황·경험칙(특히 PR 수·파일 수 추정은 전부 추정이며 실측이 아니다). **열림** = 사용자 확인 필요. 조사 문서 절 번호는 `dt`(design-tokens), `ui`(ui-components), `ux`(ux-patterns), `oa`(openapi), `be`(backend), `vm`(version-matrix), `ci`(ci-deploy), `dc`(docs-conventions), `cv`(canview-structure-checklist), `lic`(licensing), `cm`(commonality-matrix), `inv/<app>`로 줄인다.
- 각 결정 항목의 필드: 결정 / 대안(기각 이유) / 근거 / 실패 시나리오 / 소비자 영향(앱별 한 줄) / **첫 릴리스 소비 추정**(map admin·pinvi admin이 첫 릴리스를 소비하기까지 PR 수와 변경 파일 규모, 추정) / 열림.

## 0. 이 관점의 원칙과 coordinator 초안과의 차이 요약

### 0.1 설계 원칙(velocity-first)

| # | 원칙 | 근거 |
|---|---|---|
| V1 | **첫 릴리스는 3개 산출물**(tokens npm tarball, shadcn 레지스트리, 규칙 문서+검사 도구)로 제한한다. 패키지가 늘수록 소비자 PR·peer 충돌·릴리스 결합이 늘어난다 | 선행 §1·§7.1 "실제로 필요한 두 패키지만", `ui` §6.1(현행 등록 방식은 소스 복사) |
| V2 | **복사 소유를 기본, 드리프트 검사로 보완**한다. 소비자는 registry에서 파일을 받아 자기 저장소에서 소유하고, `kor-travel-common.lock.json`의 sha256 대조로 drift를 CI가 보고한다 | `ui` §2.1(27쌍 전부 상이 = 검사 없는 복사의 결과), §6.2 A안 |
| V3 | **클래스·변수 이름은 충돌 0인 네임스페이스**(`--kt-*`, 유틸리티 `kt-` 접두)만 쓴다. 앱이 기존 이름을 유지하도록 별칭은 앱이 소유한다 | `dt` §3.6.1(`--kt-` 0회), `dt` §3.1.1 관찰(pinvi가 `--color-admin-*` 신규 이름으로만 충돌 회피), `ui` §6.3 |
| V4 | **규칙은 강제 수준 3단(report → warn → fail)**으로 배포하고, 기본은 report다. fail 전환은 앱이 매니페스트에서 선언한다 | `vm` §7.4("격차를 실패가 아닌 보고로 내는 단계가 먼저"), `ci` §2.2(게이트 폭이 앱마다 다름) |
| V5 | **정렬 기준선은 floor/target 두 값**으로 둔다. floor 위반만 fail 대상이며 target은 권고다 | `vm` §5.1(후보 A "최소 이동"), §5.2 앱별 격차 |
| V6 | **기존 계약·이름을 바꾸는 이관은 강제하지 않는다**(메트릭 접두, 헤더 접두, 429 코드명, health 경로). 신규 표면에만 MUST | `be` §7-4(대시보드 회귀 미확인), `oa` §4(pinvi 모바일까지 결합) |
| V7 | **소비 저장소의 프로세스(리뷰 gate·원장 형식)는 규정하지 않는다.** AGENTS 공통 절 A~I만 배포하고 나머지는 로컬 | `dc` §3.5(로컬 유지 항목), `cv` §5 Q3 |

### 0.2 coordinator 초안 대비 변경점(요약)

| ID | coordinator 초안 | 이 레지스터 | 왜 |
|---|---|---|---|
| D-01 | 5개 npm/py 패키지 + 문서 + 템플릿 | **tokens 1패키지 + shadcn 레지스트리 + 문서/도구**; `@kor-travel/ui` npm·`config`·`api-client-core`는 보류/측정 후 | 패키지 수 = 소비자 PR 수·릴리스 결합 수 |
| D-05 | 소비자 원장 표준(체크박스+대응표) | 소비자 원장 형식 **미규정** | 원장 형식 변경은 0 가치·N PR |
| D-06 | 단일 기준선(정확 버전) | **floor/target 2열**; TS 7·npm 12·Python 3.11은 예외 등록 | 하향 PR(airport TS 7→5.9, map npm 12→11) 회피 |
| D-07 | P3 계층별 정확 핀 + 대조 | **P2+ (lockfile 필수 + 설치본 대조)**; 선언 형식은 앱 자유 | `package.json` 범위 재작성 PR 회피 |
| D-08 | weather를 v4+tokens+Next16 동시 전환 | weather는 registry 셸 아이템이 안정된 뒤(Phase 4 후반) 전환 | 2,495행 CSS 교체를 registry 없이 하면 두 번 작업 |
| D-09 | `@kor-travel/ui` React 19 전용 npm | registry 아이템은 React 19 소스(복사 소유); React 18 앱은 tokens부터 | 동일 결론, 배포 형태만 다름 |
| D-10 | npm 패키지 1차, 레지스트리 2차; 클래스에 공통 이름 | **레지스트리 1차**; 클래스는 `kt-` 접두 네임스페이스 | pinvi 사용자 표면 `primary`류 이름과 충돌 위험(`dt` §3.1.1 pinvi 관찰) |
| D-11 | GitHub Release tarball(npm) + git+https(py) | 동일 + 레지스트리는 `raw.githubusercontent.com/<tag>` 호스팅 → **npm org 없이 첫 릴리스 가능** | 외부 계정 작업을 critical path에서 제거 |
| D-12 | 모든 semantic에 `.dark` 값 필수 | `.dark`는 common 기본값만 제공, 앱 오버라이드의 dark 값은 **선택**; 대비 검사는 report 기본 | dark 미사용 앱 6/7(`dt` §3.2.2) |
| D-13 | G0~G9 전부 규약, C1~C22 제안대로 | **MUST 소집합(8개)** + 나머지 SHOULD; 게이트는 diff-based(신규·변경 파일만) | 기존 위반(`window.confirm` 8건 등)을 이관 조건에서 분리 |
| D-14 | MUST/SHOULD/MUST NOT 채택 + 예외 | 동일하되 **강제 수준을 "신규 표면 MUST / 기존 표면 SHOULD+예외 레지스트리"**로 분리; 429 코드명·헤더 접두는 앱 소유 | breaking 묶음을 앱 일정에 위임 |
| D-15 | 메트릭 접두 map·pinvi 이관(P2) | map·pinvi 접두 **영구 예외** | 대시보드 회귀 비용 > 통일 이득 |
| D-17 | 동일 | + registry 아이템의 SPDX/`Origin` 헤더는 drift 비교에서 헤더 블록 정규화 | Hallmark 스탬프(첫 줄 규칙)와 공존 |
| D-18 | 재사용 워크플로 5종 | `versions-check.yml`·`registry-drift.yml`·`openapi-drift.yml` 3종을 먼저, `node-quality`/`python-quality`는 Phase 5 | 앱 CI 재구성 PR 회피 |
| 신규 | — | D-19 소비자 매니페스트, D-20 강제 수준 3단, D-21 airport Admin 정의, D-22 범위 밖 정리(마커·지도 라이브러리), D-23 이관 PR 규격, D-24 회수 측정 | — |

## A. 저장소 범위·구조

### D-01 배포 단위(패키지 경계·이름·exports·peer·채널)

- 결정(후보): 첫 릴리스(`v0.1`)의 배포 단위는 다음 3종 + 문서. 그 외는 측정 후 추가한다.

| 단위 | 이름·위치 | 내용 | peer/의존 | 채널 |
|---|---|---|---|---|
| 1. tokens | npm `@kor-travel/tokens`(`packages/tokens`) | `tokens.css`(`:root/.dark` `--kt-*`, map 기본값), `theme.css`(v4 `@theme inline` `kt-` 네임스페이스 + `@utility kt-duration-*`), `shadcn.css`(shadcn alias → `--kt-*`), `base.css`(focus·hairline·reduced-motion·cursor), `dark-class.css`/`dark-media.css`, `tokens.json`(DTCG)·`tokens.ts`·`tailwind-preset.cjs`(생성물) | peer 없음(순수 CSS; `theme.css`만 Tailwind ≥4.3 전제) | GitHub Release tarball(D-11) |
| 2. registry | shadcn 레지스트리 `registry/registry.json` + `registry/<item>.json`(소스 `packages/ui-src/`) | 1차 소형 12종 → 2차 Button/overlay/Table/DataTable/Pager 등(D-09·D-10) | 아이템별 `dependencies`(`@base-ui/react`, `class-variance-authority`, `clsx`, `tailwind-merge`, `lucide-react`)와 `registryDependencies`를 항목에 선언; React 19 소스 | `https://raw.githubusercontent.com/digitie/kor-travel-common/registry-vX.Y.Z/registry/...` |
| 3. rules+tools | `docs/standards/*`, `versions.json`, `tools/*.py`, `.github/workflows/*.yml`(재사용) | 색상 톤·UX·PC/Mobile·OpenAPI·버전·에이전트 규약 + 검사 스크립트 + 재사용 워크플로 | Python 3.11+ stdlib(검사 도구) | git 태그 참조 |
| (Phase 3) py | Python dist `kor-travel-common`, import `kortravelcommon`, extras `api`/`db`/`testing`(`packages/py/kor-travel-common`) | 1차 `quality`(ruff/mypy 베이스 파일)·`openapi`(export CLI)·`time`·`fastapi.health` | 3.11 호환 문법, `[api]`에만 fastapi | `git+https://…@py-vX.Y.Z#subdirectory=packages/py/kor-travel-common` |
| 보류 | `@kor-travel/ui` npm, `@kor-travel/config`(eslint/tsconfig), `@kor-travel/api-client-core`, `templates/agent-config` | `ui` npm은 registry 복사가 실패(패치 누적)로 측정될 때만; config는 선행 §7.2 "프레임워크를 숨기는 공통 설정 금지"와 충돌; api-client-core는 앱별 `ApiError` 형태 4종이라 어댑터 비용이 이득보다 큼(`cm` §2.3) | — | — |

- 의존 방향: 앱 → registry 아이템(앱 소유 사본) → `@kor-travel/tokens`; 앱 → `kortravelcommon`. common은 앱 도메인·지도 엔진·인증 서비스를 import하지 않는다(선행 §7.1).
- 대안(기각): (a) 5패키지 동시 출범(coordinator D-01) — 소비자가 첫 릴리스에 만져야 할 `package.json` 의존이 3~4개로 늘고, `@kor-travel/config`는 map의 ESLint 10/`eslint-config-next` 미사용·airport TS 7·ktdm ESLint 8 사이에서 즉시 예외가 5개 생긴다(`vm` §1.6). (b) 단일 거대 패키지 — 선행 §6 비권고. (c) 규칙만·코드 없음 — 사용자 전제 (4) 위반.
- 근거: `ui` §6.1(등록 방식 현황 = 소스 복사), §6.2(A/B/C 비교), `cm` §2.1~2.3, `be` §3(1차 C4·C12·C13·C20), 선행 §7.1·§7.3.
- 실패 시나리오: registry 복사본에 앱별 패치가 누적돼 drift 검사가 항상 빨간 상태로 방치된다 → D-19의 `patched` 허용 목록과 D-24 측정으로 "패치 3개 이상 = npm 패키지화 검토" 트리거를 둔다.
- 소비자 영향: map — 원본 제공자이므로 아이템 재수입은 헤더·클래스 접두 변경만 / pinvi admin — 이식본 28파일을 registry 사본으로 교체 / concierge — 18종 프리미티브 교체(라이선스 정렬 선행) / airport — WIP 병합 후 소형 아이템 / geo·ktdm — tokens만(React 18) / weather — tokens 후 셸 아이템.
- 첫 릴리스 소비 추정: map **2 PR, 약 45파일**(tokens 6 + registry 재수입 ~40, 대부분 기계적 접두 치환) / pinvi admin **2 PR, 약 26파일**(tokens 6 + 1차 아이템 15 + `components.json`·매니페스트·cn 별칭). 근거는 D-10·D-12의 분해.
- 열림: npm org(`@kor-travel`) 존재 여부(403 미확인) — 첫 릴리스에는 불필요(D-11). Python dist 이름 `kor-travel-common`은 PyPI 404(가용) — 발행은 Phase 5 이후 결정.

### D-02 저장소 구조(canview 대응)

- 결정(후보): canview의 계층형 문서 구조를 채택하고 하드웨어·차량·firmware 항목을 제외한다(`cv` §1.1 F21·F25·F27·F41~F44 불필요). 추가·변형: 루트 `CLAUDE.md`(40줄 이하 포인터, `dc` C3), `docs/standards/`, `docs/survey/`, `docs/plan/`, `docs/dev-environment.md`, `docs/integration-map.md`(소비자별 채택 버전표), `packages/{tokens,ui-src,py}`, `registry/`, `versions.json`, `tools/{check_versions,registry_drift,kt_contrast,validate_manifest,ux_grep_gate}.py`. `docs/decisions.md`는 **두지 않는다**(색인은 `docs/adr/README.md` 하나) — `documentation-maintenance.md` §2·§3의 `decisions.md` 문구를 함께 수정해 `cv` Q1 충돌을 닫는다.
- 대안(기각): canview처럼 `decisions.md` 이중 색인 유지 — 갱신 누락 지점만 늘린다(`dc` §4 "불필요").
- 근거: `cv` §1.1·§1.2·§4, `dc` §4 대응표.
- 실패 시나리오: `docs/runbooks/README.md`가 가리키는 `agent-workflow.md`·`consumer-adoption.md`·`release.md` 부재로 링크 검사 17건 실패가 지속(`cv` §1.3) → T-001·T-009에서 파일을 만들기 전까지 `docs.yml`을 필수 체크로 두지 않는다.
- 소비자 영향: 없음(common 내부).
- 첫 릴리스 소비 추정: 해당 없음.
- 열림: 없음.

### D-03 개발 환경 정본(common 자체)

- 결정(후보): common 자체는 Linux/WSL bash 정본, CI ubuntu-24.04. 검사 도구는 Python 3.11+ stdlib로만 작성해 Windows에서도 동작하게 한다(도구 이식성이 곧 소비자 이식성). worktree는 임시 프로필(canview ADR-003 방식). 공통 절(D-09 문서 규약)은 OS를 규정하지 않는다.
- 대안(기각): Windows PowerShell 정본(canview) — 소비자 6/7이 Linux/WSL(`dc` §1.11).
- 근거: `dc` §2 C1·C2·C12, `cv` §5 Q4·Q5.
- 실패 시나리오: `.py` 사본의 CRLF가 커밋에 섞인다(`cv` §1.2) → T-003에서 `.gitattributes` 정규화 확인.
- 소비자 영향: 없음.
- 열림: 없음.

### D-04 리뷰 gate

- 결정(후보): common 자체는 canview full gate(2인 독립·immutable 기준선·P0~P3·disposition 4종)를 **규칙 문서·토큰·레지스트리 아이템·py 공개 API·OpenAPI 규약** 변경에 적용하고, 그 외(조사 문서 정정·CHANGELOG·매니페스트 스키마 patch)는 light. **소비자에게는 리뷰 절차를 부과하지 않는다** — 공통 절 B(Ruthless Review 4불릿)와 TEMPLATE만 배포하고 채택은 로컬.
- 대안(기각): 소비자 full/light 2단계 표준(coordinator D-04) — kta만 성문 규칙(`dc` §1.5)이라 6개 저장소에 신설 PR이 필요하고, 이관 PR 자체의 통과를 늦춘다.
- 근거: `dc` §1.5·§3.4, `cv` §3.3.
- 실패 시나리오: 소비 앱이 registry 아이템 사본을 리뷰 없이 수정해 drift가 누적 → D-19 drift 검사가 report로 드러낸다(리뷰가 아니라 검사로 막는다).
- 소비자 영향: 없음(선택 채택).
- 열림: light 판정 주체(`dc` Q4) — common 안에서는 "PR 작성자가 아닌 merge 담당"으로 고정(기본값).

### D-05 task 원장 형식

- 결정(후보): common 자체는 `docs/tasks-rule.md`의 5열 표 + `validate_plan.py`(무변경). **소비자 원장 형식은 규정하지 않는다.** `docs/standards/agent-conventions.md`는 "ID `T-NNN` 재번호 금지·완료 시 evidence 보존"만 SHOULD로 적는다.
- 대안(기각): 체크박스 원장 표준 + `validate_task_ledger.py`(`dc` §3.3-7) — 도구 하나를 더 만들고 7개 저장소 원장을 바꾸는 비용 대비 이득이 없다.
- 근거: `cv` §1.2(common `tasks-rule.md`는 이미 5열 표), §5 Q3, `dc` §1.7.
- 실패 시나리오: 없음(소비자 무영향).
- 소비자 영향: 없음.
- 열림: 없음.

## B. 프론트엔드 스택·버전 정렬

### D-06 정렬 기준선 표(floor/target)와 예외

- 결정(후보): `versions.json`은 축마다 **floor**(이보다 낮으면 fail 후보)와 **target**(권고)을 둔다. 첫 릴리스의 floor는 "현재 설치본 중 최저 안전선", target은 2026-09 최신 안정이다(`vm` §4). 예외는 `exceptions[]`에 저장소·키·사유·재검토 시점을 등록한다.

| 축 | floor | target | 예외(등록) | 근거 |
|---|---|---|---|---|
| Node 런타임 | 22.12(Vitest 5 최소) | 22.23.x(2026-10 이후 24 재검토) | 없음(CI Node 20인 ktdm·geo·weather는 floor 위반 → Phase 4 정렬) | `vm` §1.1·§4.4·§5.1 |
| npm | 11.19 | 11.19.x(동봉) | map `12.0.1` 정확 핀 허용(`verify-npm-tree` 결박) | `vm` §3.2·Q3 |
| Next.js | 16.2.7 | 16.3.4 | weather 15.5(Phase 4 상향), ktdm 14.2(Phase 4 상향) | `vm` §1.2 |
| React | 19.0 | 19.2.8 | geo·ktdm 18.3.1(tokens만 소비; React 19 후 registry) | `vm` §1.8·§5.3 |
| TypeScript | 5.9 | 5.9.3 | airport 7.0.2 **추적 예외**(ESLint 도입 시점에 재판단; 하향 강제 없음) | `vm` §6 |
| Tailwind / `@tailwindcss/postcss` | 4.3.1 | 4.3.3 | pinvi mobile 3.4.19(NativeWind 4) 예외 | `vm` §1.2·§1.7 |
| `@base-ui/react` | 1.6 | 1.8.0 | concierge 1.5(1차 아이템 소비 전 1.6+로) | `ui` §5.1, `vm` §1.3 |
| shadcn CLI | (제한 없음) | 4.21 | devDependencies 권고(SHOULD); concierge dependencies 위치는 정정 대상이나 fail 아님 | `vm` §7.1, `lic` D9 |
| cva / clsx / tailwind-merge | 0.7.1 / 2.1.1 / 3.6.0 | 동일 | airport WIP `cn@0.2.5` → clsx+tailwind-merge(T-430) | `vm` §1.3, `ui` §7-7 |
| lucide-react | 0.460 | 1.41 | registry 아이템은 아이콘 이름만 사용(0.x/1.x 공통 이름 확인 필요 — 미확인) | `vm` §1.3·Q13 |
| ESLint | (Phase 1 미규정) | 10.x | Phase 4부터 floor 9 | `vm` §1.6 |
| Vitest / Playwright | 4.1 / 1.60 | 4.1.x / 1.63 | weather 3.2.7(Phase 4) | `vm` §1.6 |
| react-query / react-table / react-virtual | 5.90 / 8.21 / 3.14 | 5.102 / **8.21**(9.x 미조사) / 3.14.10 | — | `vm` §1.4 |
| Python | `>=3.11`(common 코드 호환) | 앱 `>=3.12`, 이미지 3.12-slim | weather 이미지 3.13 허용 | `be` §2.1·§7-1, `vm` Q4 |
| 잠금 도구 | **lockfile 존재**(uv.lock 또는 poetry.lock) | uv + CI/Docker `--locked` | ktdm poetry.lock 허용(Phase 4 uv 전환) | `vm` §2.1·Q10 |
| fastapi / starlette / uvicorn / pydantic / pydantic-settings | 0.141 / 1.6 / 0.52 / 2.13 / 2.15 | 동일 | map `starlette<1.0` 상한 **재검증 전까지 예외** | `vm` §2.2, `oa` Q7 |
| SQLAlchemy / alembic | 2.0.52 / 1.19 | 동일 / 1.19.2 | map `alembic<1.20` 예외 | `vm` §2.3 |
| pytest / pytest-asyncio / ruff / mypy | 9.1 / 1.4 / 0.16 / 2.3 | 동일 | geo pre-commit(0.7.4/1.13.0)은 `language: system` 전환 권고 | `vm` §2.6·§3.5 |
| dagster | 1.13 | 1.13.21 | — | `vm` §2.5 |
| PostgreSQL/PostGIS | 별도 트랙(정렬 범위 밖, 현 16+3.5 digest 유지) | — | — | `vm` Q9 |
| GitHub Actions | v4/v5(현행) + SHA 핀 권고 | v7 | 재사용 워크플로 안에서만 common이 SHA 핀 | `ci` §2.3 |
| provider `python-*-api` SHA | 등록만(대조 대상 아님) | — | `python-kasi-api@main`(pinvi etl)은 report에 "floating" 표시 | `vm` §2.7·Q7 |

- 대안(기각): (a) 단일 정확 기준선(coordinator D-06) — TS·npm·Next에서 하향/상향 PR을 첫 릴리스 조건으로 만든다. (b) 후보 B 최신(Node 24·npm 12·TS 7) — typescript-eslint peer `<6.1`(`vm` §1.6)과 Vitest·Next 이미지 전면 교체.
- 근거: `vm` §5.1 후보 A·§5.2·§6·§7.4, `cm` §3.2·§3.3.
- 실패 시나리오: floor를 너무 낮게 잡아 "전부 통과"로 정렬이 진행되지 않는다 → 분기별 floor 상향을 `versions.json` `baseline` 갱신 task(T-502)로 고정.
- 소비자 영향: airport — TS 7 예외 등록, `engines` 선언 추가 / concierge — base-ui 1.5→1.6+, Python lock 도입 / ktdm — Node 20 CI·Next 14·React 18·ESLint 8 모두 floor 위반(Phase 4) / geo — Node 20 CI·React 18·lock 없음 / map — 위반 없음(starlette 예외) / weather — Node 20 CI·Next 15·Vitest 3 / pinvi — uv.lock 미소비(report).
- 첫 릴리스 소비 추정: map·pinvi 모두 **0 PR**(report 모드에서는 격차만 보고). fail 전환은 Phase 4.
- 열림: Node 22 vs 24(기본 22), npm 11.19 vs 12(기본 11.19 + map 예외), TS 7 예외 기간(기본 "typescript-eslint가 TS 7 peer를 허용할 때까지"), Python 앱 floor 3.12 시점(기본 Phase 4).

### D-07 핀 정책·`versions.json` 스키마·검증 스크립트

- 결정(후보): **P2+** — 선언 형식(caret/exact)은 앱 자유, **lockfile 존재와 설치본 대조가 규칙**이다. `tools/check_versions.py`가 앱의 `package-lock.json`(v3)·`uv.lock`·`poetry.lock`을 파싱해 `versions.json`과 대조한다. 정확 핀 강제 목록은 두지 않는다(map은 이미 정확 핀 + 스크립트 결박, pinvi는 lock 무결성 검사 — 각자 방식 유지).
- 스키마 초안(`versions.json`, `schema: kor-travel-common.version-registry.v1`):

```json
{
  "schema": "kor-travel-common.version-registry.v1",
  "baseline": "2026-09",
  "updated": "2026-09-06",
  "toolchain": {
    "node":   { "floor": "22.12.0", "target": "22.23.1", "image": "node:22-bookworm-slim" },
    "npm":    { "floor": "11.19.0", "target": "11.19.1" },
    "python": { "floor": "3.11",    "target": "3.12",    "image": "python:3.12-slim" },
    "uv":     { "floor": "0.11",    "target": "0.12.10" }
  },
  "npm":  { "next": { "floor": "16.2.7", "target": "16.3.4" }, "react": { "floor": "19.0.0", "target": "19.2.8" },
            "typescript": { "floor": "5.9.0", "target": "5.9.3" }, "tailwindcss": { "floor": "4.3.1", "target": "4.3.3" },
            "@base-ui/react": { "floor": "1.6.0", "target": "1.8.0" }, "vitest": { "floor": "4.1.0", "target": "4.1.11" } },
  "pypi": { "fastapi": { "floor": "0.141", "target": "0.141.1" }, "starlette": { "floor": "1.6", "target": "1.6.0" },
            "sqlalchemy": { "floor": "2.0.52", "target": "2.0.52" }, "ruff": { "floor": "0.16", "target": "0.16.6" } },
  "images":  { "postgis": { "note": "별도 트랙", "current": "postgis/postgis:16-3.5" } },
  "actions": { "actions/checkout": { "floor": "v4", "target": "v7" } },
  "providers": { "python-kma-api": { "note": "SHA 등록만" } },
  "exceptions": [
    { "repo": "kor-travel-airport", "key": "npm.typescript", "installed": "7.0.2", "reason": "typescript-eslint peer <6.1", "review": "2026-12" },
    { "repo": "kor-travel-map", "key": "pypi.starlette", "installed": "<1.0", "reason": "TestClient/httpx2 재검증 전", "review": "T-414" }
  ],
  "blocked": [ { "pypi": "mcp", "range": ">=2", "reason": "concierge 2026-09-04 crash-loop", "since": "2026-09-04" } ]
}
```

- 검증 스크립트 동작(`tools/check_versions.py --repo <path> --manifest kor-travel-common.lock.json [--mode report|warn|fail]`):
  1. 매니페스트(D-19)의 `lockfiles[]`를 읽어 각 lock을 파싱(npm lock v3 `packages["node_modules/<pkg>"].version`, `uv.lock` `[[package]]`, `poetry.lock` `[[package]]`). lock이 없으면 항목 `LOCK_MISSING`.
  2. `versions.json`의 각 키에 대해 installed < floor → `FLOOR`, floor ≤ installed < target → `BEHIND`, ≥ target → `OK`, `exceptions[]`에 있으면 `EXEMPT`, `blocked[]` 범위에 걸리면 `BLOCKED`.
  3. 출력: Markdown 표(stdout + `$GITHUB_STEP_SUMMARY`) + JSON(`--json`).
  4. 종료 코드: `report`(기본) 항상 0 / `warn` 0 + `::warning::` 주석 / `fail` `FLOOR`·`LOCK_MISSING`·`BLOCKED`가 1개 이상이면 1. 모드는 CLI 인자 < 매니페스트 `versions.enforce` < 워크플로 input 순으로 결정.
  5. 읽기 전용, 네트워크 없음(레지스트리 조회는 별도 `--refresh-latest` 옵션, CI에서는 비활성).
- 대안(기각): P3 계층별 정확 핀(coordinator D-07) — 6개 저장소의 `package.json`·`pyproject.toml` 범위를 다시 쓰는 PR이 선행된다. P4 renovate preset — 설치 가능 여부 미확인(`vm` Q12), 7곳 모두 미사용.
- 근거: `vm` §7.1~§7.4, ktdm 레지스트리 형식(`vm` §7.3), pinvi lock 무결성(`ci` §1.5).
- 실패 시나리오: lock 파서가 workspace 중첩(pinvi `apps/web/node_modules/tailwindcss`)을 놓쳐 오탐 → 매니페스트 `lockfiles[].scope`로 workspace 경로를 지정하고 중첩 항목 우선.
- 소비자 영향: 전 앱 — 워크플로 1개(`versions-check.yml` 호출) + 매니페스트 1파일. lock 없는 geo·map·ktdm·concierge는 `LOCK_MISSING` 보고(fail 아님).
- 첫 릴리스 소비 추정: map·pinvi 각 **매니페스트+워크플로 2파일**(D-19 PR에 합산).
- 열림: Renovate/dependabot 채택 여부(기본: Phase 5에 `templates/dependabot.yml`만 제공).

### D-08 Tailwind v4 전환 대상별 방식과 순서

- 결정(후보): 전환 순서는 "이미 v4인 앱의 `@config` 정리 → 진행 중 앱(airport) → 미도입 앱(weather) → ktdm 정리"이며, 모두 **tokens 채택과 분리된 별도 PR**로 한다.

| 순서 | 대상 | 현황(사실) | 방식 | 규모(추정) | 근거 |
|---|---|---|---|---|---|
| 1 | airport | main Tailwind 없음(순수 CSS 1,844행), WIP `99b3f98`이 v4.3.3+shadcn `base-nova`(61파일, JSX 미변경) | WIP 병합 전 정렬(T-430): `cn@0.2.5`→clsx+twMerge, shadcn/postcss devDeps, Button을 D-09 레시피로 교체, `tokens.css`의 alpha line·16/10 radius는 **airport 고유 유지**(오버라이드 허용 목록 밖은 `dt` §3.6.4 대로 admin 프로필 값으로 전환 권고, 강제 없음) | WIP diff 위에 ~8파일 | `inv/kor-travel-airport` §3.2·§9, `dt` Q5 |
| 2 | geo | v4.3.1 + `@config tailwind.config.ts`(raw hex 43색 이중 정의, 우선순위 미확인) | `@config` 제거 + `tailwind.config.ts` 삭제; `--ui-*` 3층은 앱 별칭으로 유지(tokens 뒤에 둠) | 3~5파일 + `text-brand` 13곳 시각 검증 | `dt` §3.1.1·Q3, `inv/kor-travel-geo` §9 |
| 3 | concierge | v4.3.1 + `@config` + globals hex fallback 블록 중복 | `@config`·fallback 블록 제거, `--ktc-*` 정본을 `--kt-*` 오버라이드 파일로 재해석(값 이동 없음, 이름만) | `tokens.css`·`globals.css`·`tailwind.config.ts` 3파일 + `--ktc-` 125회 sed | `dt` §3.1.1·§3.6.1 |
| 4 | pinvi web | admin `@theme` + 사용자 v3 preset `@config`; mobile v3 | admin 표면만 tokens; **사용자 preset `@config`는 유지**(consumer 프로필은 pinvi 소유). mobile은 NativeWind 5 GA까지 **예외 등록** | admin `globals.css` 1파일 | `dt` §3.6.7, `inv/pinvi` §3.2·§9 |
| 5 | weather | Tailwind 없음, CSS 2,495행·170 클래스·13 TSX·220 `className`·동적 19곳 | (a) Next 16·Node 22·Vitest 4 선행(T-460) → (b) tokens.css만 먼저(shadcn 변수명 이미 사용, 1:1 매핑 `inv/kor-travel-weather` §9.1) → (c) registry 셸/패널/폼 아이템으로 CSS 40~48% 교체, preflight 대체 10%, 반응형 9% 유틸 흡수, 도메인 CSS 32~35% 잔존 | (b) 3파일 / (c) 약 18파일·CSS 1,000~1,190행 | `inv/kor-travel-weather` §9.1 |
| 6 | ktdm | v4.3.1 설치 + `ops-*` CSS 146줄·유틸 179줄 혼용, Next 14/React 18 | Next 16·React 19·ESLint 9 선행(T-470) → tokens(`@theme` 20색 → `--kt-*` 별칭) → registry는 StatStrip·AppErrorPanel부터 | 선행 업그레이드 별도, tokens 2파일 | `inv/kor-travel-docker-manager` §9, `vm` §5.2 |

- 대안(기각): weather를 tokens·Next16·셸 교체와 한 PR로(coordinator D-08) — 2,495행 CSS를 registry 없이 손으로 옮기면 registry 안정화 후 두 번째 교체가 생긴다.
- 근거: `vm` §1.2(전제 (1)의 실제 대상은 "미도입→도입"), `cm` §3.3 전환 트랙.
- 실패 시나리오: geo `@config` 제거 후 `text-brand`류가 raw hex에서 토큰으로 바뀌며 시각 회귀 → 제거 PR에 스크린샷 비교(320/1024/1440) evidence 요구.
- 소비자 영향: 위 표.
- 첫 릴리스 소비 추정: map·pinvi admin은 **v4 전환 작업 0**(이미 v4).
- 열림: airport `tokens.css` 16/10 radius·alpha line을 admin 프로필로 수렴할지(기본: 유지, 오버라이드 밖 항목으로 문서화), pinvi mobile 예외 재검토 시점(기본: NativeWind 5 GA).

### D-09 UI 프리미티브 엔진·React 범위·Button/DataTable 계약

- 결정(후보):
  - 엔진: overlay(Dialog·AlertDialog·Popover·Tooltip·Tabs·Breadcrumb Link)는 `@base-ui/react`; 비-overlay(Button·Checkbox·Input·Textarea·NativeSelect·Separator·Badge)는 **native 요소 우선**, Button·Badge는 `useRender`로 `render` prop을 선택 지원(map·concierge 호출부 12줄 보존).
  - React: registry 아이템은 **React 19 소스**(ref prop, `forwardRef` 없음). React 18 앱(geo·ktdm)은 tokens부터 채택하고 React 19 후 registry.
  - Button 계약: `type="button"` 명시 기본 / `loading` = `aria-disabled`+`aria-busy`+spinner+**포커스 유지**(native `disabled` 안 걺, `blockBusyActivation`) / `disabled`는 native + `disabledReason`→`title` / root opacity 금지(라벨 래퍼 `opacity-55`) / variant 7종(`default·outline·secondary·ghost·destructive·destructive-solid·link`), size 8종(deprecated alias 유지).
  - Checkbox: native `<input type=checkbox>` + `onCheckedChange(boolean)` + `data-slot="checkbox"`(pinvi식) — Table 선택 열 셀렉터는 `[data-slot=checkbox]`로 엔진 무관.
  - DataTable: TanStack v8 `ColumnDef` + `meta{align,wrap,className,headerClassName,cellClassName,headerStyle}`, `manualSorting` 기본 **true**, `initialSorting`·`enableSortingRemoval`·`enableMultiSort:false`, 선택(`enableRowSelection`·`rowSelectionLabel`·`renderBulkActions`), 가상화 opt-in + `stickyHeader`·`containerStyle`·`containerTestId`·`rowTestId`(pinvi 확장 흡수), 4상태(skeleton/empty/error/data), `aria-selected` 미부착(pinvi 판단). pinvi `AdminTable` 어댑터·`mobileCard`는 pinvi 소유로 잔류. geo `VirtualTable` 검색 툴바·`rowHeader`는 흡수하지 않는다(T-442a 별도 판정).
- 대안(기각): (a) radix 채택 — base-ui 소비 파일 29 vs radix 12(`ui` §5.3). (b) React 18 동시 지원(`forwardRef` 유지) — 두 벌 소스 유지 비용; 소비 시점을 React 19 이후로 미루는 편이 싸다(geo ADR-019는 18 유지 사유 없음, `inv/kor-travel-geo` §11-1). (c) `manualSorting` 기본 false(pinvi 어댑터) — G2.3 "페이징 목록 = 서버 정렬" 위반.
- 근거: `ui` §3.1(회귀 위험 표), §3.2, §3.3, §5.4, `ux` §4 C10.
- 실패 시나리오: base-ui Button의 `type` 기본값이 pinvi 주석과 달라 폼 안 보조 버튼이 submit → 아이템이 엔진과 무관하게 `type="button"`을 명시하므로 무영향; base-ui Checkbox hidden input 여부는 native 채택으로 무관(`ui` §7-1·§5.4 미확인 항목 회피).
- 소비자 영향: map — Button은 이미 동일 계약(재수입 시 접두 치환만); Checkbox base-ui→native는 `checkbox.tsx` 1파일 + 호출부 시그니처 `(checked, details)`→`(checked)` 확인 / pinvi admin — Button·Checkbox·Input·Separator는 pinvi 판이 곧 규약(변경 최소); overlay `hasUnsavedInput`·`viewportProps`·`data-pv-surface`는 흡수 / concierge — Button 동일, `destructive` `aria-expanded:` 누락만 / geo — React 19·base-ui 전환 후(`asChild` 17곳→`render`) / airport WIP — Button 레시피 교체(`disabled:opacity-50` 제거).
- 첫 릴리스 소비 추정: 1차 아이템(소형 12종)에는 Button·DataTable이 없으므로 map·pinvi **0 추가 PR**; 2차(registry-v0.2) 소비는 map ~15파일·pinvi ~12파일 1 PR씩(추정).
- 열림: base-ui Toast API(미확인) — 토스트는 아이템으로 제공하지 않음(C8).

### D-10 UI 배포 방식(레지스트리 1차 + `kt-` 네임스페이스)

- 결정(후보): **shadcn 레지스트리(A)를 1차 배포 방식**으로 한다. 아이템 소스는 `packages/ui-src/`(map 원본 이식 + SPDX/Origin 헤더)이고 빌드 스크립트가 `registry/registry.json`과 아이템 JSON을 만든다. 소비자는 `shadcn add https://raw.githubusercontent.com/digitie/kor-travel-common/registry-v0.1.0/registry/badge.json` 형태로 받는다(태그 고정 URL; `registries` alias는 `components.json`에 등록).
  - 아이템 안의 Tailwind 클래스는 **`kt-` 접두 유틸리티**만 쓴다: `bg-kt-surface-subtle`, `text-kt-ink`, `border-kt-control-line`, `h-kt-control`, `rounded-kt-control`, `text-kt-2xs`, `duration-kt-fast`, `outline-kt-focus`. `theme.css`가 `--color-kt-*`, `--spacing-kt-control`, `--radius-kt-*`, `--text-kt-*`를 정의한다. 앱의 기존 이름(`bg-surface-page`, `bg-admin-subtle`, `--ui-*`, `--ktc-*`)은 **앱이 자기 `@theme inline` 별칭으로 계속 소유**한다.
  - `cn`: 아이템은 `@/lib/utils`의 `cn`을 import한다(`components.json` `aliases.utils`). pinvi는 `aliases.utils: "@/lib/admin/cn"`(등록형 twMerge)로 맞춘다.
  - 드리프트: D-19 매니페스트 + `tools/registry_drift.py`.
- 대안(기각): (a) npm 패키지 1차(coordinator D-10) — 소비자마다 `@source` 등록·peer 정렬(base-ui 1.5/1.6/1.8, React 18)·`transpilePackages`/webpack·Turbopack 검증(pinvi ADR-066)이 첫 릴리스 조건이 된다; 앱별 확장(pinvi testid·sticky)을 prop으로 흡수하기 전엔 pinvi가 소비할 수 없다. (b) 클래스에 공통 이름(`bg-surface-page`) 사용 — pinvi 사용자 표면 preset의 `primary`·`canvas`·`ink`류와 이름 공간이 겹칠 위험이 있고, pinvi가 이미 `admin-*` 신규 이름으로만 충돌을 피했다는 사실(`dt` §3.1.1 관찰)이 위험의 증거다. `kt-` 접두는 전 저장소 0회(`dt` §3.6.1)라 어떤 앱에서도 무충돌이다. (c) 소스 복사 현행(C) — 검사 없는 복사가 27/27 상이를 만들었다.
- 근거: `ui` §6.1~§6.3, §7-8·9, `dt` §3.6.1, 선행 §6·§7.3(E1 `@source`, E6 `transpilePackages`).
- 실패 시나리오: raw.githubusercontent 태그 URL이 GitHub 가용성·rate limit에 의존 → `registry/` 디렉터리는 태그로 불변이므로 소비 앱 lock(매니페스트 sha256)이 정본이고 CI drift 검사는 common 체크아웃(`actions/checkout` with `repository:`·`ref: registry-vX`)으로 수행해 raw URL 의존을 CI에서 제거한다.
- 소비자 영향: map — ui 32파일·app 부품 ~12파일에서 클래스 접두 치환(기계적 sed; 페이지 파일은 무변경) / pinvi admin — 이식본 28파일 중 1차 15종을 registry 사본으로 교체, `admin-*` 별칭 유지로 페이지 무변경 / concierge — 18종 교체(라이선스 정렬 후) / airport WIP — button 1파일 교체 / geo·ktdm — Phase 4.
- 첫 릴리스 소비 추정: map **1 PR ~40파일**(접두 치환 + SPDX 헤더 + 매니페스트), pinvi **1 PR ~20파일**(15 아이템 + `components.json` + `cn` 별칭 + 매니페스트 + 워크플로).
- 열림: raw.githubusercontent 호스팅 허용 여부(기본: 허용, Phase 5에 GitHub Pages/npm으로 이전 검토), map 원본 클래스 접두 치환을 map이 수용하는지(기본: 수용 — 페이지 무변경이 조건).

### D-11 npm·레지스트리·Python 배포 채널

- 결정(후보):
  - tokens: GitHub Release 자산 `kor-travel-tokens-X.Y.Z.tgz`(태그 `tokens-vX.Y.Z`)를 `npm install https://github.com/digitie/kor-travel-common/releases/download/tokens-vX.Y.Z/kor-travel-tokens-X.Y.Z.tgz`로 설치, lock `integrity`로 고정. `package.json` `name`은 `@kor-travel/tokens`(org 확보 시 publish로 전환, 이름 불변).
  - registry: 태그 `registry-vX.Y.Z`의 `registry/` 트리(raw URL 또는 CI 체크아웃).
  - Python: `git+https://github.com/digitie/kor-travel-common.git@py-vX.Y.Z#subdirectory=packages/py/kor-travel-common`(lock에 sha). 릴리스 자산으로 wheel도 첨부(D안 병행; Docker에 git이 없는 map api.Dockerfile 대비).
  - common 참조는 항상 태그/SHA, `@main` 금지(선행 §8).
- 대안(기각): GitHub Packages(설치 인증 필요, 선행 §8 E5), 공개 npm(org 미확인·계정 작업이 critical path), git URL + `prepare`(모노레포 subpath 불편).
- 근거: `be` §5.1·§5.2(git+sha 관례 13종), `ci` §2.3, 선행 §8.
- 실패 시나리오: 사용자가 이미 `@kor-travel` 이름을 다른 org가 점유했음을 확인 → `name`만 `@digitie/kor-travel-tokens`로 바꾸면 되고 tarball 설치 경로는 불변(소비자 `package.json` 의존 키 1줄 변경).
- 소비자 영향: 전 앱 — `package.json` 1줄 + lock 갱신.
- 첫 릴리스 소비 추정: map·pinvi 각 **2파일**(D-12 PR에 합산).
- 열림: npm org 생성(기본: Phase 5, 비차단).

### D-12 토큰 접두·계층·프로필·다크·오버라이드·대비 검사

- 결정(후보):
  - 접두 `--kt-*`(전 저장소 0회). 계층 2단: `semantic(--kt-*) ← app override(같은 이름 재선언)`. 앱 고유 확장은 앱 접두(`--ktc-shell-*`, `--pv-*`, `--weather-marker-*`).
  - 어휘: surface 4(page/subtle/muted/card) · text 4(primary/secondary/tertiary/disabled) · icon · border(장식) · control-line(3:1) · brand 4(brand/hover/tint/foreground) · focus · status 4+tint(success/warning/info/destructive) · overlay · radius 2 · control-h 2 · rail · duration 2 · ease 2 · shadow 2 · z 5 · font-sans/mono 스택 문자열 · 타입 7단.
  - shadcn alias 의미 고정(`shadcn.css`): `--input` = control-line, `--accent` = brand-tint, `--accent-foreground` = brand, `--muted` = surface-subtle, `--card` = card, `--radius` = radius-control.
  - 프로필: `admin`(6/8, 36/30, 15px, 12/13.5/15/17/20/24/30) 기본 / `consumer`(8/14/20/32, 44px, 16px) 값은 **문서로만**(pinvi 소유). 표면 스코프 기법(`[data-*-surface]`)은 `docs/standards/design-tokens.md`에 예시로.
  - 오버라이드 허용 목록: brand 4·focus·paper 4(surface)·ink 4(text)·**status 4+tint(허용하되 대비 검사 대상)**. 형태·타입·모션은 프로필로만. 값 형식은 OKLCH 권고, hex 허용(pinvi·concierge).
  - 다크: `tokens.css`가 map 기본 `.dark` 값을 제공하지만, **앱 오버라이드의 `.dark` 값은 선택**. 토글 없는 앱은 `color-scheme: light` 선언 SHOULD. `dark-media.css`(airport식)·`dark-class.css`(map식) 중 앱이 선택.
  - 대비 검사 `tools/kt_contrast.py`: 앱의 `brand.css`(오버라이드)를 읽어 light 쌍(text-primary/secondary/tertiary vs page/card/subtle/muted, control-line vs page/card/muted, focus vs page, brand-foreground vs brand, status-ink vs status-tint)을 계산. 기본 report; 매니페스트 `contrast.enforce: true`면 3:1(컨트롤·focus)/4.5:1(본문) 미달 시 fail. dark 쌍은 `contrast.dark: true`일 때만.
- 대안(기각): (a) `--ktc-` 승격 — concierge 125회 사용과 의미 충돌(`dt` §3.6.1). (b) 모든 semantic `.dark` 필수(coordinator D-12) — dark 값 없는 geo·pinvi·ktdm에 값 발명 부담, 토글 없는 앱에서 검증 불가(`dt` §3.6.6). (c) status 오버라이드 금지 — pinvi admin·concierge가 이미 자기 값을 쓰므로 금지는 즉시 위반.
- 근거: `dt` §3.2.3, §3.3, §3.4.2(geo 2.29/2.41·concierge 2.06/1.93·ktdm brand 3.59·airport 1.15 미달), §3.6.1~3.6.6, `cm` §2.1.
- 실패 시나리오: 미달 앱(geo·concierge·ktdm·airport)이 enforce를 켜지 않고 방치 → Phase 4 이관 task에 "control-line 값 1개 조정 + enforce 전환"을 수용 기준으로 넣는다(값 1개 변경이라 비용은 낮고 시각 변화는 hairline 진하기뿐).
- 소비자 영향: map — 오버라이드 파일이 거의 비어 있음(기본값 = map) / pinvi admin — `--color-admin-*` 19종을 `--kt-*` 오버라이드로 재선언 + 기존 이름을 별칭으로 유지 / weather — hue만(navy) / geo — hue + control-line 조정 / concierge — `--ktc-*` 이름 이동 + control-line 조정 / ktdm — hue(Ember) + tint 4종 신규 / airport — hue + alpha line 대체(선택).
- 첫 릴리스 소비 추정: map **1 PR ~6파일**(`package.json`·lock·`globals.css` 분리·`brand.css` 신설·매니페스트·워크플로), pinvi admin **1 PR ~6파일**(동일 구성; `globals.css` admin 블록 치환).
- 열림: 접두 `--kt-` 확정(기본 `--kt-`), 마커 팔레트 P-01~16은 범위 밖(D-22).

### D-13 UX 가이드·PC/Mobile 규약과 충돌 C1~C22

- 결정(후보): `ux` §2 G0~G9를 `docs/standards/ux-guide.md`(admin 장 + 사용자 표면 장 분리)로, §3을 `docs/standards/responsive-web.md`로 채택하되, **MUST는 8개**로 제한하고 나머지는 SHOULD다. 게이트(`tools/ux_grep_gate.py`)는 **변경 파일(diff)만** 검사하고 기본 report다.

| MUST | 규칙 | 근거 |
|---|---|---|
| U1 | focus 링 = `outline 2px` 불투명 토큰 + offset 2px, `outline-none` 금지(신규 코드) | G9.1, `ux` §1.12 |
| U2 | 신규 코드 `window.confirm` 금지; 파괴적 행동은 확인 다이얼로그 | G4.6, C7 |
| U3 | 상태 5-tone 이름(success/warning/destructive/info/neutral) 또는 등록된 alias | G5.1, C9 |
| U4 | 표는 4상태(loading/empty/error/data)를 컴포넌트 안에서 렌더 | G2.2 |
| U5 | skip link + `<main id tabIndex=-1>` | G1.3 |
| U6 | `html/body overflow-x: clip`(hidden 금지), 표·지도만 자체 overflow | G9.9, §3.3 |
| U7 | 셸 전환 breakpoint = 1024(lg), 검사 폭 320/375/414/768/1024/1440 | §3.2, C3 |
| U8 | 접근성 이름에 운영 정보 금지(`(Sprint N)`류) | C20 |

- 충돌 C1~C22 결정(한 줄씩):

| # | 결정 |
|---|---|
| C1 | 접힌 rail 4rem SHOULD; pinvi 5rem은 "터치 admin 변형"으로 예외 등록(변경 강제 없음) |
| C2 | weather 17rem·접힘 없음은 registry 셸 채택(T-462) 시 자연 해소; 그 전엔 문서만 정정 |
| C3 | 1024(lg)로 통일(MUST U7); airport 860은 콘텐츠 breakpoint 예외 |
| C4 | strip 기본·drawer 허용; a11y 계약(G4.8)만 SHOULD |
| C5 | tint+2px mark SHOULD; pinvi ink 채움 허용 |
| C6 | 표면별 분리(admin 36/30·사용자 44·모바일 48); pinvi admin 44px 2쪽은 예외 등록 |
| C7 | 신규 `window.confirm` 금지(MUST U2, diff-based); 기존 잔존(map 2·ktdm 3·kta 1·weather 1)은 목록화만, 기한 없음; 동사 라벨 SHOULD |
| C8 | 토스트 정책 G4.1(silent success)만 SHOULD; 엔진은 앱 선택, common은 토스트 아이템을 만들지 않음 |
| C9 | 5-tone 이름 MUST(U3) + alias 표(ktdm `ok/warn/danger`); geo CANCELLED→warn은 geo 도메인 판단(강제 없음) |
| C10 | DataTable `manualSorting=true`; pinvi `AdminTable` 어댑터는 pinvi 소유 |
| C11 | admin·사용자 웹 좌측 정렬 SHOULD; 모바일 앱 가운데 허용 |
| C12 | 스택 문자열은 tokens(`--kt-font-sans` Pretendard 1순위); 로딩은 앱 책임, 방식 미규정 |
| C13 | admin 15/12px SHOULD; ktdm 14px·11px, kta 11px은 이관 시 |
| C14 | light 기본 명시; `.dark` 슬롯은 유지(airport 자동 dark 허용) |
| C15 | 로그인 G7.1 SHOULD; geo·weather 아이콘 타일은 후속(강제 없음) |
| C16 | pinvi 헤더 2종·weather pathname 노출은 각 앱 소유(권고만) |
| C17 | HelpTip popover-only 허용 하위 집합; 히트 ≥24px만 SHOULD |
| C18 | 모달 엔진 앱 소유; 행동 계약(G4.8)과 "두 스택 금지"만 SHOULD |
| C19 | `app-error-panel` registry 아이템 제공; weather·kta 도입 SHOULD |
| C20 | MUST U8 |
| C21 | Hallmark 스탬프는 앱 소유·registry 아이템에 미포함(B3 라이선스 미확인); drift 비교는 선두 주석 블록 정규화(D-17) |
| C22 | 지도 스타일 빌더 배포 경로는 범위 밖(D-22, T-506) |

- 대안(기각): G0~G9 전부 규약·게이트 전체 파일 검사(coordinator D-13) — 기존 위반이 이관 PR의 차단 조건이 되어 첫 소비가 늦어진다.
- 근거: `ux` §2, §3, §4, §5, `cm` §2.5.
- 실패 시나리오: diff-based 게이트가 "줄 이동"을 신규로 오인 → `--base <sha>` 대비 추가된 줄만 검사(`git diff -U0`).
- 소비자 영향: 전 앱 — 워크플로 input 1줄로 게이트 on/off(기본 report).
- 첫 릴리스 소비 추정: map·pinvi **0 추가 PR**(D-19 워크플로에 포함).
- 열림: dirty 이탈 경고(Q2, 기본: 규약 미포함), 규칙 ID 체계(Q9, 기본: common `UX-Gn.m` 신규, 앱 M/C 번호는 출처 인용), pinvi 44px 예외(Q3, 기본: 예외 등록).

## C. 백엔드·API

### D-14 OpenAPI/REST 규약 채택(강제 수준 분리)과 예외 레지스트리

- 결정(후보): `oa` §3의 M1~M9/S1~S13/N1~N8을 `docs/standards/openapi.md`로 채택하되, **적용 대상을 "신규 표면"과 "기존 표면"으로 나눈다.** 기존 표면의 위반은 `docs/standards/openapi-exceptions.md`에 앱·항목·사유·해제 조건으로 등록하고 CI는 report한다.

| 항목 | 신규 표면 | 기존 표면 | 비고 |
|---|---|---|---|
| M1 export 커밋 + `--check` CI | MUST | MUST(Phase 3 앱별 task) | additive; pinvi·concierge·ktdm 신설 |
| M2 `servers` 제거 | MUST | MUST | 전 앱 이미 충족 |
| M3 problem+json + `code`/`request_id` | MUST | SHOULD + 예외(pinvi `{error}`, concierge/ktdm `{detail}`, geo v1/v2) | airport는 additive(`code`·`request_id` 추가) |
| M4 `X-Request-ID` echo(형식 검증 통과 시)/발급, `trust_incoming=False` 옵션 | MUST | SHOULD | ktdm 정책 옵션으로 수용 |
| M5 `/health`·`/readyz`·`/version` + `/metrics` schema 제외 | MUST | SHOULD + 별칭 병행(geo `/v1/healthz` 무기한) | probe 변경은 ktdm compose·Prometheus 동반 |
| M6 좌표 `lon/lat` | MUST | 예외(geo v1 `x/y`, weather body, concierge body, pinvi bbox 문서) | |
| M7 tz-aware | MUST | SHOULD | pinvi KST 해석 완화 허용 |
| M8 `securitySchemes` 선언 | MUST | SHOULD(Phase 4 MUST) | geo typegen 재생성 동반 |
| M9 production 표면만 export | MUST | MUST | weather `development` 강제 확인 |
| S1~S13 | SHOULD | SHOULD | S10 typegen: pinvi Zod 이중 유지 예외(Q5) |
| N1~N8 | MUST NOT | 예외 등록(N2 `?key=` legacy) | |

- 세부: 검증 오류 422 기본, geo 400 예외. 429 코드명·상태→코드 사전은 **common 기본 사전(map 값) + 앱 덮어쓰기 허용, 이름 변경 강제 없음**. 헤더 접두는 형식 규칙(`X-<AppId>-Api-Key|Service-Token|Actor|Admin-Proxy-Secret|Ops-Token`)만, AppId 표는 앱 소유(풀네임·약어 병존 허용). 버전 prefix는 `/v1` SHOULD(concierge·ktdm `/api/v1`, pinvi `/` 예외).
- 대안(기각): 기존 표면까지 MUST(coordinator D-14) — pinvi는 모바일 배포 주기까지 결합(`oa` §4 "높음"), concierge features export는 map provider와 동시 수정.
- 근거: `oa` §3.1~3.3, §4, §5 C11, §6 Q1~Q4·Q6·Q9, `inv/kor-travel-map` §8-18.
- 실패 시나리오: 예외 레지스트리가 영구화 → 예외마다 `review` 날짜 필수, 분기 감사(T-502)에서 재확인.
- 소비자 영향: map — 규약 원형, `type` URI 접두만 문서화 / weather — `--check` 모드 전환·`code` 사전 / airport — additive 2필드 + 스펙 422 정합 / geo — v1 예외, v2/admin은 ADR-060 breaking 묶음에 위임 / pinvi — export+drift(신규)·securitySchemes / concierge·ktdm — export 신설, 나머지 예외.
- 첫 릴리스 소비 추정: 프론트 첫 릴리스와 무관(Phase 3). map-api **1 PR ~4파일**(export 스크립트 교체 + 워크플로), pinvi-api **1 PR ~5파일**(export 신설 + 워크플로 + 스펙 커밋).
- 열림: 429 코드명 통일 여부(기본: 미통일), `/health` vs geo `/healthz` 별칭 기간(기본: 무기한).

### D-15 Python 공통 모듈 우선순위와 배포

- 결정(후보): 1차(py-v0.1) = `quality`(`ruff-base.toml`·`mypy-base.ini` 파일 + `[tool.ruff] extend` 사용법), `openapi`(export CLI `--check`·profile 콜백), `time`(`KST`·`kst_now/utc_now`·`check_aware_datetime`), `fastapi.health`(`/health`·`/readyz`·`/version` 라우터 팩토리, 별칭 인자). 2차(py-v0.2, T-308~T-310 후 T-311 절차 반복) = `settings` 베이스, `db`(asyncpg/psycopg 흡수), `fastapi.request_id`, `fastapi.problem`(opt-in 핸들러). 3차 = `auth.public_api_key`·`auth.trusted_proxy`·`testing`·`http`·`cors`·`security_headers`. 보류 = `logging`(structlog 실구현 pinvi 1곳), `pagination`, `dagster`, `geo_primitives`, `cli.mutex`, alembic 템플릿(cookiecutter 대신 `templates/alembic-env.py` 파일만).
  - 메트릭 접두: 신규 서비스 `kt<x>_` SHOULD; **map `kor_travel_map_`·pinvi `pinvi_api_`는 영구 예외**(대시보드 5종·alert 회귀).
  - Python floor: common 코드는 3.11 문법(PEP 695 미사용).
- 대안(기각): 3차까지 한 릴리스(coordinator D-15 범위) — `problem`·`request_id`는 앱 계약 변경을 동반해 1차 소비자(map·weather·airport)에서도 프론트 동시 수정이 필요(`oa` §4 weather 행).
- 근거: `be` §3(C4·C12·C13·C20 "계약 변경 없음, 근거 강함"), §4 제외 목록, §5.3, §7-4.
- 실패 시나리오: map `starlette<1.0` 상한 때문에 `[api]` extra 범위가 충돌 → `[api]` extra는 `fastapi>=0.115`만 선언하고 starlette 범위를 두지 않는다(T-414 재검증 전까지).
- 소비자 영향: map-api — export 스크립트 교체·ruff extend / weather-api — 동일 + `--check` / airport — export 교체·ruff 신설(baseline 허용 목록) / geo — health 별칭·export 교체·lock 도입 / pinvi — export 신설 / concierge — pyproject·uv 도입 후 / ktdm — Poetry lock 후.
- 첫 릴리스 소비 추정: Phase 3 이후. map-api·pinvi-api 각 1 PR(D-14 추정에 포함).
- 열림: 메트릭 접두 예외 영구화(기본: 영구), Python 앱 floor 3.12 시점.

### D-16 소비자 첫 대상과 순서

- 결정(후보): 1차 공동 소비자 = **map admin + pinvi admin**(tokens-v0.1 + registry-v0.1). 2차 = concierge(라이선스 정렬 후), airport(WIP 병합 후 tokens + 소형 아이템). 3차 = weather(Next16 선행 후), geo·ktdm(React 19 후). Python 1차 = map-api·weather-api·airport, 2차 geo, 3차 pinvi·concierge·ktdm. 각 앱은 **tokens PR → registry PR → py PR**을 분리하고 한 PR당 "빌드·e2e 통과 + 되돌리기 명령"을 evidence로 남긴다(D-23).
- 대안(기각): 7앱 동시 — 선행 §8 "모든 앱 동시 배포 요구 금지".
- 근거: `ui` §4, 선행 §1·§10, `cm` §3.2.
- 실패 시나리오: pinvi 라이선스 결정(L6)이 지연되면 1차 소비자가 map 하나 → 그 경우 concierge를 앞당기되 라이선스 정렬(L8)이 필요하므로 **airport(GPL, WIP)를 2번째 소비자로 승격**한다.
- 소비자 영향: 위 순서.
- 첫 릴리스 소비 추정: map 2 PR ~45파일, pinvi admin 2 PR ~26파일(D-01 합산).
- 열림: pinvi 라이선스(L6) — critical path.

## D. 라이선스·운영

### D-17 라이선스·출처 조치

- 결정(후보): common = GPL-3.0-or-later(`NOTICE`에 저작권자·버전·연락처, L1). 파일 규약: registry 아이템·tokens·py 모듈 전부 SPDX 헤더 + `Origin:`(원천 저장소@커밋 경로) + `Derived-From:`(shadcn MIT 등) + `Modified:`(L4 린트). `THIRD_PARTY_NOTICES.md` + `LICENSES/`(MIT·Apache-2.0(cva)·ISC·BSD-3·OFL-1.1)(L3). `PROVENANCE.md` = `lic` §2.3 표 형식(L2). 이동 규칙: 원천 GPL(map·weather·airport) 그대로, geo(only)는 파일에 `GPL-3.0-only` 병기 또는 권리자 재선언(L10), MIT(concierge·ktdm) 코드는 고지 보존, **pinvi 파일은 L6 전까지 이동 금지(B1)**, 벤더 tgz·`maplibre-vworld-react`·Hallmark 본문은 영구/조건부 금지(B2·B3).
  - 소비 방향: GPL 코드(registry 아이템·tokens.css)를 MIT 저장소(concierge·ktdm)에 복사하면 결합물이 GPL(`lic` §3.1 `#IfLibraryIsGPL`) → concierge·ktdm은 **루트 GPL-3.0-or-later 정렬(L8, 1 PR)** 후 코드 채택. 정렬 전에는 규칙 문서만 참조.
  - drift 검사와의 관계: 앱 사본의 선두 주석 블록(SPDX·Origin·Hallmark 스탬프)은 정규화 후 비교(사본이 스탬프를 첫 줄에 두어도 drift 아님).
- 대안(기각): common §7 추가 허가(MIT 앱 링크 허용) — 모든 파일에 예외 문구 유지·검증 비용, `lic` §3.6 권고와 반대.
- 근거: `lic` §2.3, §3.2~3.7, §4 B1~B10, §6.
- 실패 시나리오: shadcn 생성 시점 버전 미기록(B6)으로 `Derived-From` 정확도 부족 → 저장소 URL + 연도만 기재(MIT 고지 요건 충족).
- 소비자 영향: pinvi — LICENSE 추가·pyproject·`maplibre-vworld.md` 정정 1 PR(L6) / concierge·ktdm — LICENSE 교체 1 PR(L8) / map — LICENSE 전문 복원(L9, 비차단) / geo — only/or-later 결정(L10) / airport·weather — `license` 필드 추가(L11, 비차단).
- 첫 릴리스 소비 추정: pinvi **+1 PR 3파일**(L6, 선행), map **0**(L9는 비차단).
- 열림: pinvi 공개/GPL 여부(기본: 공개 + GPL-3.0-or-later), concierge·ktdm GPL 정렬 vs §7 예외(기본: 정렬), geo only 유지(기본: or-later 재선언).

### D-18 CI·릴리스·포트/서비스명 규약

- 결정(후보):
  - common 자체 CI(`ci.yml`): `docs`(link·plan·unittest·redaction) → `tools`(check_versions·registry_drift·kt_contrast 자기 테스트) → `tokens`(build·`npm pack`·tarball 설치 스모크) → `registry`(빌드·`registry.json` 스키마 검증·fixture Next 16 앱에 `shadcn add` 후 `next build` webpack+Turbopack) → `python`(uv build·wheel 설치·pytest). 하드닝: `permissions: contents: read`, concurrency, timeout, `ubuntu-24.04`, 액션 SHA 핀.
  - 재사용 워크플로(소비자 호출, 태그 참조): **Phase 1** `versions-check.yml`(inputs: `manifest`, `mode`), `registry-drift.yml`(inputs: `manifest`, `mode`), `contrast-check.yml`; **Phase 3** `openapi-drift.yml`, `typegen-drift.yml`; **Phase 5** `node-quality.yml`·`python-quality.yml`(선택). 앱 기존 워크플로는 유지하고 job 1개만 추가한다.
  - 릴리스: 태그 `tokens-vX.Y.Z`·`registry-vX.Y.Z`·`py-vX.Y.Z` 독립, CHANGELOG `[Unreleased]`→절, 정식 태그 전 map·pinvi PR 스모크(선행 §8-3). 같은 버전 덮어쓰기 금지.
  - 포트/서비스명: 정본은 ktdm `docs/ports.md`(인용만), sibling `140xx`(airport)·`141xx`(weather) 등록 요청, common 자체 `130xx`(13001 fixture API, 13005 registry 프리뷰). 서비스명 고정 어휘·`container_name`·볼륨·env 접두 규약은 `docs/standards/ci-deploy.md`에 SHOULD로만(이름 변경 강제 없음, airport 14002는 예외 등록).
  - Dockerfile 최소 규약(멀티스테이지·non-root·HEALTHCHECK 1곳·digest 병기·OCI revision)은 SHOULD.
- 대안(기각): 5종 재사용 워크플로 동시 제공 + 앱 CI 대체(coordinator D-18) — map 8개·pinvi 5개 required check 이름이 ruleset에 결박(`ci` §2.3)돼 재구성 PR이 크다.
- 근거: `ci` §1.2·§1.9·§2.1~§2.3·§3·§4, `cv` §1.3.
- 실패 시나리오: 재사용 워크플로 cross-repo 호출 조건(공개 여부) 미확인(`ci` Q1) → common은 공개 GPL이므로 성립 추정; 미성립 시 각 앱이 common을 `actions/checkout`으로 받아 스크립트를 직접 실행하는 fallback을 워크플로 문서에 둔다.
- 소비자 영향: 전 앱 — `.github/workflows/kor-travel-common.yml` 1파일 추가(concierge는 `.github` 신설).
- 첫 릴리스 소비 추정: map·pinvi 각 **1파일**(D-19 PR에 합산).
- 열림: `live-e2e`(kta) 같은 운영 호출 job 금지 여부(기본: 규약에서 다루지 않음), 컨테이너명 `-latest` 접미(기본: 유지).

## E. 신규 결정(D-19~D-24)

### D-19 소비자 채택 매니페스트 `kor-travel-common.lock.json`

- 결정(후보): 각 소비 저장소 루트(모노레포는 앱 디렉터리)에 매니페스트 1파일을 둔다. 버전 대조·registry drift·대비 검사·UX 게이트가 모두 이 파일을 읽는다.

```json
{
  "schema": "kor-travel-common.consumer-manifest.v1",
  "repo": "pinvi", "app": "apps/web/admin",
  "tokens": { "version": "0.1.0", "override": "apps/web/app/kt-brand.css" },
  "registry": { "tag": "registry-v0.1.0", "target": "apps/web/components/admin/ui",
    "items": { "badge": { "sha256": "…", "patched": false },
               "dialog": { "sha256": "…", "patched": true, "reason": "hasUnsavedInput 유지", "since": "2026-09" } } },
  "python": { "version": null },
  "lockfiles": [ { "kind": "npm", "path": "package-lock.json", "scope": "apps/web" }, { "kind": "uv", "path": "apps/api/uv.lock" } ],
  "versions": { "enforce": false }, "contrast": { "enforce": false, "dark": false }, "ux_gate": { "mode": "report" },
  "exceptions": [ { "key": "tokens.profile", "value": "admin-touch-44px", "paths": ["apps/web/app/(admin)/admin/feature-requests"] } ]
}
```

- `tools/registry_drift.py`: 매니페스트의 각 아이템에 대해 앱 사본(선두 주석 블록·행끝 공백 정규화)과 registry 태그 사본의 sha256을 비교. 결과 `IDENTICAL`/`PATCHED(허용)`/`DRIFT`/`MISSING`/`OUTDATED(태그 뒤짐)`. `patched: true`인데 `reason` 없음은 오류. 모드 report/warn/fail.
- 대안(기각): 앱 `package.json`의 `kor-travel-common` 필드 — 모노레포·Python 앱에서 위치가 불명확.
- 근거: ktdm runtime pin registry 원칙("값은 파일, 계약은 코드", `vm` §7.3), pinvi 이식 주석 관행(`ui` §2.1).
- 실패 시나리오: `patched` 남발 → D-24 측정에서 앱당 patched ≥3이면 npm 패키지화(prop 흡수) 검토 트리거.
- 소비자 영향: 전 앱 — 1파일.
- 첫 릴리스 소비 추정: map·pinvi 각 1파일(tokens PR에 포함).
- 열림: 없음.

### D-20 규칙 강제 수준 3단과 "신규·변경 파일만" 정책

- 결정(후보): 모든 검사(버전·drift·대비·UX·OpenAPI drift)는 `report`(기본) → `warn` → `fail` 3단이며, 전환은 매니페스트에서 앱이 선언한다. 코드 규칙 게이트는 diff-based. common은 Phase 5 분기 감사에서 "report 상태로 2분기 이상 방치된 앱"을 목록화해 사용자에게 보고한다(강제 전환은 사용자 결정).
- 대안(기각): 도입 즉시 fail — 6개 CI 게이트 폭이 3~10종으로 다르고(`ci` §1.2) 기존 위반이 많다.
- 근거: `vm` §7.4, `ux` §1.12(기존 위반 수), `dt` §3.4.2.
- 실패 시나리오: 영구 report → D-24 지표에 "enforce 전환 앱 수"를 포함.
- 소비자 영향: 없음(선택).
- 첫 릴리스 소비 추정: 0.
- 열림: 없음.

### D-21 "kor-travel-airport Admin"의 정의

- 결정(후보): 현재 실체(무인증 백업 패널 + collector-status + `/v1/admin/*`)를 대상으로 하되, 첫 채택 범위는 **tokens + 소형 아이템(StatStrip·SectionCard·EmptyState·Alert·Badge)**이며 AdminPageHeader/skip-link는 airport T-035 라우트 분리 이후(T-431a). 로그인·AdminShell은 대상 아님(ADR-003 무인증 의도).
- 대안(기각): airport에 admin 앱 신설을 common 계획에 포함 — 제품 결정이며 범위 밖.
- 근거: `inv/kor-travel-airport` §1-4, §9, §11-9, `ux` §5-5.
- 실패 시나리오: 사용자가 "Admin"을 신설 앱으로 의도 → T-431a를 확장하고 AppShell 아이템 소비를 추가(계획 변경만).
- 소비자 영향: airport — 위.
- 첫 릴리스 소비 추정: 해당 없음(2차).
- 열림: 사용자 확인(기본: 현재 실체).

### D-22 범위 밖 정리(마커 팔레트·지도 라이브러리·provider SHA)

- 결정(후보): 마커 팔레트 P-01~16 hex 정본은 map 소유로 확정 요청(T-507), `maplibre-vworld-react` npm 배포·`vworld-style.ts` 중복·`python-airkorea-api` 이중 경로·provider SHA 불일치는 common 범위 밖의 "공유 라이브러리 배포 정책" 결정 요청(T-506)으로만 다룬다. `versions.json` `providers`는 등록만.
- 대안(기각): common이 마커 팔레트 규칙을 소유 — 데이터 도메인(`dt` §3.5).
- 근거: `dt` §3.5·Q2, `ux` C22, `be` §5.1, `vm` §2.7.
- 실패 시나리오: 없음(결정 요청만).
- 소비자 영향: 없음.
- 열림: 두 결정 모두 사용자.

### D-23 소비자 이관 PR 규격

- 결정(후보): 이관 PR은 (1) 한 PR = 한 산출물(tokens / registry / py), (2) 본문에 매니페스트 diff·`check_versions`/`registry_drift` 결과·빌드·e2e·스크린샷(320/1024/1440) evidence·되돌리기 명령(`git revert` + lock 복원), (3) 페이지 파일 무변경이 원칙(별칭 계층으로 흡수), (4) 앱별 최대 변경 파일 상한(초과 시 분할) — tokens 10, registry 1차 30, registry 2차 30, py 10. `docs/runbooks/consumer-adoption.md`·`templates/consumer-pr.md`가 정본.
- 대안(기각): 앱당 단일 대형 이관 PR — 회귀 원인 구분 불가(선행 §2 "업그레이드와 공통화는 독립 작업").
- 근거: 선행 §8·§10, `dc` §1.14 PR 본문 관례.
- 실패 시나리오: 상한 초과(weather 셸 교체) → 셸/패널/폼으로 3분할.
- 소비자 영향: 전 앱.
- 첫 릴리스 소비 추정: map·pinvi 2 PR씩(D-01).
- 열림: 없음.

### D-24 회수 측정 지표

- 결정(후보): 선행 §11 지표(원본 수정 시간·타 앱 반영 시간·검증 시간·회귀 수·로컬 복사본 수)에 **drift 지표**(앱당 `DRIFT`·`PATCHED` 수, enforce 전환 앱 수, `EXEMPT` 수)를 더해 분기별 `docs/reports/adoption-YYYY-QN.md`로 기록. "패치 ≥3 아이템은 npm 패키지화 검토", "2분기 연속 순절감 ≤0이면 공유 범위 축소"를 중단 조건으로 둔다.
- 대안(기각): 측정 없음 — 선행 §11 "측정 결과 없이 예측으로 쓰면 안 됨".
- 근거: 선행 §11, `ui` §6.2 A안 비용.
- 실패 시나리오: 측정 부담으로 미기록 → 지표를 CI 산출물(JSON)에서 자동 집계.
- 소비자 영향: 없음.
- 열림: 없음.

## F. 통합 계획 초안(Phase 0~5)

### F.1 단계 표

| Phase | 목표 | 산출물 | 완료 기준 | 중단 조건 |
|---|---|---|---|---|
| 0 골격 | common 저장소가 자기 규칙으로 검증 통과 | AGENTS/CLAUDE/SKILL/README/docs 지도, ADR-001~006, 계획, task 원장, 고지 파일, `versions.json`+`check_versions`(report), 매니페스트 스키마, 재사용 워크플로 골격 | `docs.yml`·`ci.yml` green, `validate_plan` 오류 0, 링크 오류 0 | 없음(내부) |
| 1 tokens | `tokens-v0.1.0` 릴리스 + 규칙 문서 3종 | `packages/tokens`, `kt_contrast`, `design-tokens.md`·`ux-guide.md`·`responsive-web.md`, `ux_grep_gate` | tarball 설치 스모크 통과, 대비 검사 map 기본값 전부 통과, map·pinvi tokens PR 병합 | pinvi L6 미결 시 pinvi 대신 airport WIP로 스모크 |
| 2 registry | `registry-v0.1.0`(1차 12종+4) → `v0.2.0`(2차) | `packages/ui-src`, 빌드, `registry_drift`, fixture 앱 webpack/Turbopack 스모크 | map 재수입 drift 0, pinvi 1차 교체 e2e 통과 | map 페이지 파일 변경이 필요해지면 접두 전략 재검토 |
| 3 py+OpenAPI | `py-v0.1.0` + `openapi.md`·예외 레지스트리 + drift 워크플로 | `kortravelcommon` 1차 4모듈, `openapi-drift.yml`·`typegen-drift.yml` | map-api·weather-api·airport export 교체 + CI 통과 | map starlette 상한 미해결 시 `[api]` 범위 미선언 유지 |
| 4 소비 확대 | 7앱 정렬·전환·채택 | 앱별 T-4xx | 각 앱 매니페스트 존재 + report 0 `FLOOR`(fail 전환은 앱 선언) | React/Next 업그레이드가 범위를 압도하는 앱(ktdm·geo)은 tokens에서 멈춤 |
| 5 운영 | 릴리스·감사·측정 | consumer-smoke, 분기 감사, 회수 보고, dependabot 템플릿 | 1회차 회수 보고 제출 | 순절감 ≤0 2분기 → 범위 축소 |

### F.2 상세 task 목록(ID 대역은 `docs/tasks-rule.md` §2·§2.1)

형식: ID | 제목 | 선행 | 우선순위 | gate | 대상 저장소. 상태는 상세 파일 작성 시 `validate_plan.py` 규칙(READY는 선행 DONE)에 맞춰 READY/BLOCKED로 둔다. 외부 조건(L6·L8·WIP 병합 등)은 `외부 선행` 줄에 적는다. 첫 5개(T-001~T-005)는 선행 `없음`으로 즉시 병렬 시작 가능하다.

Phase 0(T-001~T-099)

| ID | 제목 | 선행 | 우선순위 | gate | 대상 |
|---|---|---|---|---|---|
| T-001 | 문서 골격: `README.md`·`AGENTS.md`(공통 절 A~I + 로컬 절)·`CLAUDE.md`(≤40줄)·`SKILL.md`(라우터)·`docs/README.md`·`resume.md`·`journal.md`·`tasks.md` | 없음 | P0 | 문서 검증 | common |
| T-002 | ADR-001~006 작성(배포 단위·레지스트리 1차·`kt-` 네임스페이스·floor/target·강제 3단·라이선스) + `docs/adr/README.md` | 없음 | P0 | 문서 검증·2인 리뷰 | common |
| T-003 | 검증 도구 정비: `validate_document_links.py` 절대 접두 제거·`.py` LF 정규화·`docs.yml` 필수화 시점 정의 | 없음 | P0 | 도구 단위 테스트 | common |
| T-004 | `versions.json` v1 + `tools/check_versions.py`(npm lock v3·uv.lock·poetry.lock 파서, report/warn/fail, 예외·blocked) + 테스트 | 없음 | P0 | 도구 단위 테스트 | common |
| T-005 | 고지 파일: `NOTICE`·`THIRD_PARTY_NOTICES.md`·`PROVENANCE.md`·`LICENSES/` + SPDX 헤더 린트 `tools/check_spdx.py` | 없음 | P0 | 문서 검증·도구 단위 테스트 | common |
| T-006 | `docs/plan/integration-plan.md`(Phase 0~5) + `docs/architecture/{README,packages,consumers}.md` + `docs/integration-map.md` | T-002 | P1 | 문서 검증 | common |
| T-007 | 소비자 매니페스트 스키마 `kor-travel-common.consumer-manifest.v1` + `tools/validate_manifest.py` | T-004 | P1 | 도구 단위 테스트 | common |
| T-008 | 재사용 워크플로 골격 `versions-check.yml`·`registry-drift.yml`·`contrast-check.yml` + selftest fixture(`tests/fixtures/consumer-app`) | T-004, T-007 | P1 | 워크플로 selftest | common |
| T-009 | runbooks: `agent-workflow.md`·`consumer-adoption.md`·`release.md`·`agent-failure-patterns.md` + `templates/consumer-pr.md` | T-001 | P1 | 문서 검증 | common |
| T-010 | `docs/standards/README.md` + `agent-conventions.md`(공통 절 A~I 원문, docs 트리 SHOULD) + `templates/AGENTS-common-section.md` | T-001 | P1 | 문서 검증·2인 리뷰 | common |
| T-011 | common `ci.yml`(docs·tools·tokens·registry·python job, 하드닝, 액션 SHA 핀) | T-003 | P1 | CI green | common |
| T-012 | `docs/dev-environment.md`(Linux/WSL 정본, 임시 worktree, 도구 이식성) + `docs/standards/ci-deploy.md`(포트 인용·명명 SHOULD·Dockerfile 최소 규약) + `docs/standards/versions.md`(floor/target 정책·예외 절차) + `templates/dependabot.yml` | T-001, T-004 | P2 | 문서 검증 | common |

Phase 1(T-100~T-199)

| ID | 제목 | 선행 | 우선순위 | gate | 대상 |
|---|---|---|---|---|---|
| T-100 | `packages/tokens/tokens.css`(`--kt-*` 어휘·map 기본값·`.dark`) + `package.json`(`@kor-travel/tokens`, `exports`, `license`) + 생성물 스크립트(`tokens.json` DTCG·`tokens.ts`·`tailwind-preset.cjs`, 정본 = CSS) | T-005 | P0 | 패키지 빌드·tarball 설치 | common |
| T-101 | `theme.css`(`@theme inline` `kt-` 네임스페이스, `@utility duration-kt-*`)·`shadcn.css`·`base.css`·`dark-class.css`/`dark-media.css` | T-100 | P0 | 패키지 빌드·tarball 설치 | common |
| T-102 | `tools/kt_contrast.py`(OKLCH/hex→WCAG, light/dark 쌍, report/fail) + map 기본값 전 쌍 통과 테스트 | T-100 | P0 | 도구 단위 테스트 | common |
| T-104 | `docs/standards/design-tokens.md`(접두·계층·프로필·shadcn alias 의미·오버라이드 허용 목록·다크·대비 규칙·표면 스코프 예시) | T-100 | P0 | 문서 검증·2인 리뷰 | common |
| T-105 | `docs/standards/ux-guide.md`(G0~G9, MUST U1~U8, C1~C22 결정, 규칙 ID `UX-Gn.m`) + `docs/standards/responsive-web.md`(표면 분류·breakpoint·검사 폭·터치·안전영역) | T-001 | P1 | 문서 검증·2인 리뷰 | common |
| T-107 | `tools/ux_grep_gate.py`(금지 패턴 7종 + `window.confirm` + `outline-none`, diff-based, report/fail) | T-105 | P1 | 도구 단위 테스트 | common |
| T-108 | `tokens-v0.1.0` 릴리스(GitHub Release tarball, CHANGELOG, `npm pack` 설치 스모크 evidence) | T-101, T-102, T-104 | P0 | 릴리스 | common |

Phase 2(T-200~T-299)

| ID | 제목 | 선행 | 우선순위 | gate | 대상 |
|---|---|---|---|---|---|
| T-200 | registry 빌드 파이프라인(`packages/ui-src` → `registry/registry.json`·아이템 JSON, 스키마 검증, 태그 URL 규약) | T-101 | P0 | 패키지 빌드 | common |
| T-201 | 1차 아이템 12종(badge+variants·skeleton·separator·card·alert·input·textarea·native-select(+option)·field(+variants)·empty-state·section-card·stat-strip) map 원본 이식 + `kt-` 클래스 + SPDX/Origin | T-200, T-005 | P0 | 아이템 테스트·fixture 빌드 | common |
| T-202 | 1차 후반 4종(filter-bar·help-tip·app-error-panel+error-recovery·button-variants) | T-201 | P1 | 아이템 테스트 | common |
| T-203 | Button 아이템(계약 D-09, `render` 선택, 테스트: type 기본·loading 포커스 유지·disabledReason) | T-201 | P1 | 아이템 테스트·2인 리뷰 | common |
| T-204 | overlay 세트(dialog·alert-dialog·popover·tooltip·tabs·breadcrumb, base-ui, pinvi 확장 흡수) + admin-page-header·admin-skip-link·admin-rail-grid(셸 골격만) | T-203 | P1 | 아이템 테스트·2인 리뷰 | common |
| T-205 | table + data-table(pinvi 확장 흡수, `manualSorting` 기본 true) + pagination-bar + checkbox(native) | T-204 | P1 | 아이템 테스트·2인 리뷰 | common |
| T-206 | copy-button·json-viewer·detail-list(피드백 채널 prop) + status-badge(tone 사전 주입) + form-field-input/select/textarea + form-validation(헤드리스) | T-203 | P2 | 아이템 테스트 | common |
| T-209 | `tools/registry_drift.py`(선두 주석 정규화·sha256·patched 허용·OUTDATED) + `registry-drift.yml` 완성 | T-200, T-007 | P0 | 도구 단위 테스트·워크플로 selftest | common |
| T-210 | fixture Next 16 앱 스모크(`shadcn add` 1차 전부 → `next build` webpack/Turbopack, tokens tarball 설치) | T-201 | P0 | 소비자 빌드 | common |
| T-211 | `registry-v0.1.0` 릴리스(1차 16종) | T-202, T-209, T-210 | P0 | 릴리스 | common |
| T-212 | `registry-v0.2.0` 릴리스(2차: Button·overlay·table·data-table·pager·copy/json/detail·status-badge·헤더·form) | T-205, T-206 | P1 | 릴리스 | common |

Phase 3(T-300~T-399)

| ID | 제목 | 선행 | 우선순위 | gate | 대상 |
|---|---|---|---|---|---|
| T-300 | `docs/standards/openapi.md`(M/S/N + 신규/기존 강제 수준 + 헤더 형식 규칙 + 코드 사전 기본값) | T-001 | P0 | 문서 검증·2인 리뷰 | common |
| T-301 | `docs/standards/openapi-exceptions.md`(앱·항목·사유·review 날짜) 초기 등록(geo v1/v2·pinvi·concierge·ktdm·weather) | T-300 | P1 | 문서 검증 | common |
| T-302 | `packages/py/kor-travel-common` 골격(hatchling, extras `api/db/testing`, 3.11 문법, PEP 639 license, pytest) | T-005 | P0 | 패키지 빌드·wheel 설치 | common |
| T-303 | `kortravelcommon.quality`(`ruff-base.toml`·`mypy-base.ini`·pre-commit 템플릿·`[tool.ruff] extend` 문서) | T-302 | P0 | 패키지 테스트 | common |
| T-304 | `kortravelcommon.openapi` export CLI(`--app`·`--output`·`--check`·profile 콜백·결정적 직렬화) | T-302 | P0 | 패키지 테스트 | common |
| T-305 | `kortravelcommon.time`(`KST`·`kst_now/utc_now`·`check_aware_datetime`) | T-302 | P1 | 패키지 테스트 | common |
| T-306 | `kortravelcommon.fastapi.health`(`/health`·`/readyz`·`/version` 팩토리, 별칭 인자, envelope 옵션) | T-302 | P1 | 패키지 테스트 | common |
| T-307 | `openapi-drift.yml`·`typegen-drift.yml` 재사용 워크플로 + selftest | T-304 | P1 | 워크플로 selftest | common |
| T-308 | `kortravelcommon.settings`(BaseSettings 믹스인) + `db`(`normalize_dsn`·`make_async_engine` asyncpg/psycopg) | T-302 | P2 | 패키지 테스트 | common |
| T-309 | `kortravelcommon.fastapi.request_id` + `problem`(opt-in 핸들러·OpenAPI 주입·검증 sanitizer) | T-306 | P2 | 패키지 테스트·2인 리뷰 | common |
| T-310 | `kortravelcommon.auth.public_api_key` + `trusted_proxy`(헤더 이름 인자) | T-308 | P2 | 패키지 테스트·2인 리뷰 | common |
| T-311 | `py-v0.1.0` 릴리스(git 태그 + wheel 자산); 2차 모듈(T-308~T-310)은 `py-v0.2.0`으로 같은 절차 반복 | T-303, T-304, T-305, T-306 | P0 | 릴리스 | common |

Phase 4(T-400~T-489)

| ID | 제목 | 선행 | 우선순위 | gate | 대상 |
|---|---|---|---|---|---|
| T-400 | 공통 이관 절차 확정(runbook 검증·PR 템플릿·되돌리기·파일 상한) + 회수 지표 기록 양식 | T-009 | P0 | 문서 검증 | common |
| T-410 | map: tokens 채택(`globals.css` 분리·`kt-brand.css`·매니페스트·`versions-check`/`contrast-check` job); next 16.3·base-ui 1.8·Playwright 상향은 하위 `T-410a`(`verify-next-sharp` 상수·pytest 잠금 동반) | T-108, T-400 | P0 | 소비자 빌드·e2e | map |
| T-411 | map: registry 1차 재수입(`kt-` 접두 치환·SPDX·drift 0·페이지 무변경) | T-211, T-410 | P0 | 소비자 빌드·e2e | map |
| T-412 | map: registry 2차(Button·overlay·checkbox native·DataTable·pager) | T-212, T-411 | P1 | 소비자 빌드·e2e | map |
| T-413 | map-api: py 1차(ruff extend·export CLI 교체·health 팩토리) + `openapi-drift.yml` | T-311 | P1 | 소비자 CI | map |
| T-414 | map-api: `starlette<1.0`·`alembic<1.20` 상한 재검증 + `uv.lock` 도입 | T-413 | P2 | 소비자 CI | map |
| T-420 | pinvi admin: tokens 채택(admin `@theme` → `--kt-*` 오버라이드 + `admin-*` 별칭 유지·매니페스트·job) — 외부 선행 L6 | T-108, T-400 | P0 | 소비자 빌드·e2e | pinvi |
| T-421 | pinvi admin: registry 1차 교체(`components.json` 신설·`cn` 별칭·15 아이템·`AdminPage` 어댑터 무변경) | T-211, T-420 | P0 | 소비자 빌드·e2e | pinvi |
| T-422 | pinvi admin: registry 2차(overlay 확장 흡수 확인·DataTable → `AdminTable` 어댑터 유지·testid e2e 5파일) | T-212, T-421 | P1 | 소비자 빌드·e2e | pinvi |
| T-423 | pinvi api: export 신설 + `openapi-drift.yml` + securitySchemes(additive) + `uv.lock` CI·Docker 소비 + versions enforce 전환 | T-311, T-420 | P1 | 소비자 CI | pinvi |
| T-430 | airport: WIP 병합 전 정렬(`cn`→clsx+twMerge·shadcn/postcss devDeps·Button 레시피 교체·`engines`) — 외부 선행 WIP PR | T-108, T-203 | P1 | 소비자 빌드·e2e | airport |
| T-431 | airport: tokens + 소형 아이템(StatStrip·SectionCard·EmptyState·Alert·Badge) 채택 + 매니페스트; 라우트 분리(airport T-035) 이후 헤더·skip-link 채택은 하위 `T-431a` | T-430, T-211 | P1 | 소비자 빌드·e2e | airport |
| T-432 | airport: export `--check`·`openapi-drift.yml`·problem `code`/`request_id` additive·스펙 422 정합 | T-311 | P1 | 소비자 CI | airport |
| T-433 | airport: ruff 베이스 도입(baseline 허용 목록) + ESLint 도입 + TS 7 예외 재판단 | T-431 | P2 | 소비자 CI | airport |
| T-440 | geo: `@config` 제거 + tokens 채택(radix 유지, `--ui-*` 별칭 유지, control-line 대비 조정) + 매니페스트 | T-108, T-400 | P1 | 소비자 빌드·e2e | geo |
| T-441 | geo: React 19 업그레이드 ADR + 실검증(ADR-019 갱신) | T-440 | P1 | 소비자 빌드·e2e | geo |
| T-442 | geo: radix→base-ui + registry 1·2차(`asChild` 17곳→`render`, 12 ui 파일); `VirtualTable`→DataTable 판정(검색 툴바·`rowHeader`)은 하위 `T-442a` | T-441, T-212 | P2 | 소비자 빌드·e2e·2인 리뷰 | geo |
| T-443 | geo: py 1차(health 별칭 `/v1/healthz` 병행·export CLI 교체·`uv.lock` 도입·pre-commit `language: system`) | T-311 | P2 | 소비자 CI | geo |
| T-450 | concierge: CI 신설(`versions-check`·`registry-drift`·최소 node 검사) + `pyproject.toml`/uv 도입(`mcp<2` blocked 반영) | T-008 | P0 | 소비자 CI | concierge |
| T-451 | concierge: 라이선스 정렬(GPL-3.0-or-later, `THIRD_PARTY_NOTICES` 고지) — 외부 선행 L8 | T-005 | P1 | 문서 검증 | concierge |
| T-452 | concierge: `@config`·fallback 블록 제거 + `--ktc-*`→`--kt-*` 오버라이드 + tokens + 매니페스트 | T-108, T-450, T-451 | P1 | 소비자 빌드·e2e | concierge |
| T-453 | concierge: registry 1·2차(18종 교체, base-ui 1.6+ 상향, shadcn devDeps) | T-212, T-452 | P1 | 소비자 빌드·e2e | concierge |
| T-454 | concierge: ruff 베이스(baseline 허용 목록) + export 신설 + `openapi-drift.yml` | T-311, T-450 | P2 | 소비자 CI | concierge |
| T-460 | weather: Node 22 CI·Next 16·Vitest 4·`eslint-config-next` 16·`moduleResolution: bundler` 선행 정렬 + react-query 미사용 정리 | T-004 | P1 | 소비자 빌드 | weather |
| T-461 | weather: Tailwind v4 도입 + tokens(shadcn 변수명 1:1 매핑) + 매니페스트 | T-460, T-108 | P1 | 소비자 빌드·e2e | weather |
| T-462 | weather: registry 셸·패널·폼·로그인 아이템으로 CSS 40~48% 교체(3분할 PR, 320/768 수동 검증) | T-461, T-212 | P2 | 소비자 빌드·e2e | weather |
| T-463 | weather-api: py 1차 + export `--check` 모드 전환 + `code` 사전 | T-311 | P2 | 소비자 CI | weather |
| T-470 | ktdm: Next 16·React 19·ESLint 9·Node 22 CI 선행 정렬 ADR + 실검증(recharts peer 포함) + `poetry.lock`/uv 도입 + `versions-check` | T-004 | P1 | 소비자 빌드 | ktdm |
| T-471 | ktdm: 라이선스 정렬(GPL-3.0-or-later) — 외부 선행 L8 | T-005 | P2 | 문서 검증 | ktdm |
| T-472 | ktdm: tokens 채택(`@theme` 20색 → `--kt-*` 별칭, tint 4종 추가) + 매니페스트 | T-108, T-470, T-471 | P2 | 소비자 빌드 | ktdm |
| T-473 | ktdm: registry 도입(StatStrip·AppErrorPanel·SectionCard부터, `ops-*` 잔존 허용) | T-212, T-472 | P2 | 소비자 빌드 | ktdm |

Phase 5(T-500~T-599)

| ID | 제목 | 선행 | 우선순위 | gate | 대상 |
|---|---|---|---|---|---|
| T-500 | 첫 정식 릴리스 절차 실행(`release.md`): 소비자 스모크 evidence → 태그 → CHANGELOG 절 | T-410, T-420, T-411, T-421 | P0 | 릴리스 | common |
| T-501 | `consumers.pins.json` + `consumer-smoke.yml`(map·pinvi pinned SHA 주간) | T-500 | P1 | 워크플로 selftest | common |
| T-502 | 분기 cross-repo 감사 체크리스트(`FLOOR`·`DRIFT`·`EXEMPT`·report 방치 앱) + `versions.json` baseline 갱신 절차 | T-501 | P2 | 문서 검증 | common |
| T-503 | 회수 지표 1회차 보고(`docs/reports/adoption-2026-Q4.md`) | T-411, T-421 | P2 | 문서 검증 | common |
| T-504 | npm org 확보 시 publish 전환(이름 불변) + GitHub Pages registry 호스팅 검토 + `@kor-travel/ui` npm 패키지화 판정(patched ≥3 트리거) | T-108, T-503 | P3 | 릴리스 | common |
| T-506 | 공유 라이브러리 배포 정책 결정 요청(`maplibre-vworld-react` npm·`vworld-style.ts` 중복·airkorea 이중 경로·provider SHA) | 없음 | P3 | 문서 검증 | 사용자·map·geo·weather |
| T-507 | 마커 팔레트 P-01~16 hex 정본 확정 요청(map 소유, pinvi 재수출) | 없음 | P3 | 문서 검증 | 사용자·map |

task 수: Phase 0 12 + Phase 1 7 + Phase 2 11 + Phase 3 12 + Phase 4 31 + Phase 5 7 = **80**. 하위 범위(`T-410a`·`T-431a`·`T-442a`)는 상세 파일 작성 시 `a` 접미 하위 task로 분리하되 원장 수는 80을 넘기지 않는다(초과 시 Phase 5 항목부터 보류).

### F.3 critical path(추정)

T-001/T-004/T-005 → T-100 → T-101 → T-102 → T-108(tokens-v0.1) → T-410(map tokens) / T-420(pinvi tokens, **L6 대기**) → T-200 → T-201 → T-209 → T-210 → T-211(registry-v0.1) → T-411 / T-421 → T-500. Python은 T-302 → T-304 → T-311 → T-413이 병행 트랙.

## G. 사용자 확인이 필요한 열린 결정(기본값 포함)

| # | 결정 | 선택지 | 기본값(이 레지스터) | 차단 여부 |
|---|---|---|---|---|
| O1 | pinvi 라이선스·공개 여부(L6) | 공개+GPL-3.0-or-later / 사내 비공개(GPL 코드 제거) | 공개 + GPL-3.0-or-later, 1 PR | **1차 소비자 critical path** |
| O2 | concierge·ktdm 라이선스 | GPL-3.0-or-later 정렬 / common §7 추가 허가 | 정렬(1 PR씩) | 2차 소비자 차단 |
| O3 | UI 배포 방식 | 레지스트리 1차(복사 소유+drift 검사) / npm 패키지 1차 | 레지스트리 1차 | 설계 차단 |
| O4 | 유틸리티 네임스페이스 `kt-`·변수 `--kt-` | `kt-` / 공통 이름 / `--ktc-` 승격 | `kt-`, `--kt-` | 설계 차단 |
| O5 | registry 호스팅 | raw.githubusercontent 태그 URL / npm / GitHub Pages | raw 태그 URL(CI는 체크아웃) | 낮음 |
| O6 | npm org `@kor-travel` | 생성 / `@digitie/*` / 미발행 | 첫 릴리스는 tarball(미발행); org는 Phase 5 | 비차단 |
| O7 | TS 기준선·airport TS 7 | 5.9 통일(airport 하향) / 7 예외 등록 | 예외 등록 | 비차단 |
| O8 | Node·npm 기준선 | 22+11.19 / 24 / npm 12 | 22 + 11.19(map 12 예외) | 비차단 |
| O9 | Python 앱 floor 3.12 시점 | 지금 / Phase 4 / 미정렬 | Phase 4 | 비차단 |
| O10 | 다크 모드 요구 수준 | 앱 오버라이드 dark 필수 / 선택 | 선택, light 기본 | 비차단 |
| O11 | 대비 검사·UX 게이트 fail 전환 시점 | Phase 1 / 앱 선언(Phase 4) | 앱 선언 | 비차단 |
| O12 | 메트릭 접두 map·pinvi 예외 | 영구 / 기한부 이관 | 영구 | 비차단 |
| O13 | health 경로 geo `/v1/healthz` | 별칭 무기한 / 기한부 | 무기한 | 비차단 |
| O14 | 429 코드명·검증 오류 코드 | 통일 / 앱 소유 | 앱 소유(기본 사전 제공) | 비차단 |
| O15 | "kor-travel-airport Admin" 정의 | 현재 실체(백업 패널) / 신설 admin | 현재 실체 | airport 2차 범위 |
| O16 | 마커 팔레트 정본·`map-marker-react` 게시 | map Tableau / pinvi Material | map 소유 확정 요청(T-507) | 비차단 |
| O17 | 공유 라이브러리 배포 정책(`maplibre-vworld-react` npm 등) | 결정 요청(T-506) | — | 비차단 |
| O18 | Renovate 설치 | 설치 / dependabot 템플릿만 | 템플릿만 | 비차단 |
| O19 | 재사용 워크플로 cross-repo 호출 조건 | 공개 확인 / fallback(체크아웃 실행) | 공개 전제 + fallback 문서 | 낮음 |
| O20 | `window.confirm` 잔존 8건 기한 | 없음 / Phase 4 | 없음(목록화만) | 비차단 |
| O21 | pinvi mobile Tailwind 3 예외 | NativeWind 5 GA까지 / 정렬 범위 제외 | 예외 등록 | 비차단 |
| O22 | geo React 19 업그레이드 승인 | 승인(ADR-019 갱신) / 18 유지 | 승인(T-441) | geo 3차 범위 |

## H. 최상위 위험

1. **pinvi 라이선스 미결(B1/L6)이 1차 소비자 절반을 막는다** — 대체는 airport WIP 승격(D-16).
2. **map 원본의 `kt-` 접두 치환 규모(~40파일)** — 기계적이지만 map e2e 전체 통과가 조건. 페이지 파일 변경이 필요해지면 접두 전략 재검토(Phase 2 중단 조건).
3. **drift 검사 오탐(선두 주석·EOL·포맷터)** — 정규화 규칙을 도구 테스트로 잠근다(T-209).
4. **geo·ktdm React 18/Next 14가 registry 소비를 Phase 4 후반으로 미룬다** — tokens만 먼저(무손실).
5. **airport TS 7 ↔ typescript-eslint peer** — 예외 등록으로 회피하되 ESLint 도입(T-433)이 늦어진다.
6. **weather CSS 2,495행 교체**는 registry 2차 셸 아이템 품질에 종속 — 3분할 PR과 수동 검사 폭 evidence.
7. **concierge CI·lock 부재** — common 채택 전 T-450이 선행(제로 베이스).
8. **map `starlette<1.0` 상한** — `[api]` extra 범위 미선언으로 우회, T-414 재검증.
9. **raw.githubusercontent 의존** — CI는 체크아웃 방식, 소비 lock은 매니페스트 sha256.
10. **report 영구화** — D-24 지표와 분기 감사에서 사용자에게 전환 여부를 묻는다.
