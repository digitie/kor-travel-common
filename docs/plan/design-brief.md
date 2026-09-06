# kor-travel-common 최종 브리프 (확정 결정 레지스터 · 파일 지도 · ADR 목록 · task 목록)

- 확정일: 2026-09-06. 작성: coordinator(Claude). 근거: `docs/survey/*`(인벤토리 7·횡단 10·README·매트릭스), 설계안 2(risk-first·velocity-first), 판정 3(fact-consistency·migration-feasibility·directive-fidelity). 판정이 합의한 병합 문안을 채택했고, 판정이 갈린 곳은 아래 "채택 사유"에 적었다.
- 표기: **결정** = 확정. **열림(O-n)** = 사용자 확인 필요, 기본값으로 진행. 근거 약칭은 `docs/survey/commonality-matrix.md` 머리 규약(`vm`·`dt`·`ui`·`ux`·`be`·`oa`·`ci`·`dc`·`cv`·`lic`·`cm`·`inv/<app>`·`prior`).
- 사용자 지시: (1) Tailwind v4 미도입 앱은 v4 전환 (2) 라이브러리/플랫폼 버전 일치 정책 (3) airport Admin·PinVi Admin 포함 (4) 코드 + 규칙(색상 톤·UX·OpenAPI·PC/Mobile Web) (5) canview 구조·AGENTS.md 채택 (6) GPL-3 (7) 에이전트가 바로 이어갈 구체 계획.

2026-09-07 변경: [ADR-014](../adr/014-common-implementation-without-registry-publishing.md)와 T-015가 사용자 지시의 npm/PyPI 미게시·common 단독 구현 순서를 반영했다. 아래 D-01·D-11·D-18·O-5는 이 결정을 연결한다. §3 이후 파일·ADR·Phase·task 표는 최초 설계 스냅샷이며 현재 상태/선행은 [task 원장](../tasks.md)과 [통합 계획](integration-plan.md), ADR 상태는 [단일 색인](../adr/README.md)을 따른다.

## 0. 용어

| 용어 | 뜻 |
|---|---|
| common | 이 저장소 `kor-travel-common` |
| 소비자 | kor-travel-airport(kta)·kor-travel-concierge(ktc)·kor-travel-docker-manager(ktdm)·kor-travel-geo(geo)·kor-travel-map(map)·kor-travel-weather(wx)·pinvi 7개 저장소. pinvi는 admin/사용자 웹/모바일 세 표면 |
| 배포 단위 | `packages/tokens`(npm `@kor-travel/tokens`) · `packages/ui`(npm `@kor-travel/ui`) · `packages/py/kor-travel-common`(Python 배포 이름 `kor-travel-common`, import `kortravelcommon`) · `docs/standards/*` 규칙 문서 · `templates/*` · `versions.json` + `tools/*.py` |
| 프로필 | 토큰 밀도 프로필 `admin`(6/8px radius·36/30px control·15px 본문·7단 스케일) / `consumer`(8/14/20/32·44px·16px; 값은 pinvi 소유, common은 규칙·의미 이름만) |
| 매니페스트 | 소비 저장소의 `kor-travel-common.lock.json`(schema `kor-travel-common.consumer-manifest.v1`) |
| 레지스트리 | common 루트 `versions.json`(schema `kor-travel-common.version-registry.v1`) |
| 외부 선행 | common이 대체할 수 없는 사용자·타 저장소 결정: L6(pinvi 라이선스), L8(ktc·ktdm GPL 정렬), airport WIP 병합, geo React 19 ADR |

## 1. 확정 결정 레지스터

### A. 저장소 범위·구조

**D-01 배포 단위** — 결정: 3 코드 패키지(tokens·ui·py) + 규칙 문서 + 템플릿 + 레지스트리/도구. `config` npm 패키지와 `api-client-core`는 만들지 않는다(`templates/eslint/*.mjs` 조각과 `frontend-stack.md`로 대체; api-client-core는 Phase 5 재평가). ui는 아이콘을 인라인 SVG로 가져 `lucide-react`를 peer로 두지 않는다. 패키지 식별자는 ADR-014와 [packages](../architecture/packages.md#1-요약표)에서 확정했다. 공개 registry 이름 확보·실패 시 개명 조건은 철회했다. 의존 방향 앱 → ui → tokens, 앱 → py 단방향. common은 앱 도메인 모듈·지도 엔진(`maplibre-vworld-*`)·provider 라이브러리(`python-*-api`)·인증 서비스(비밀번호·세션·CSRF·JWT)를 갖지 않는다. 채택 사유: `ui` §4.1~4.3·§6.2, `be` §3·§4, `vm` §1.3(lucide 0.363~1.41 혼재), `inv/map` §3.1(ESLint 검증 스크립트 충돌), `cm` §2.3(ApiError 4형).

**D-02 저장소 구조(canview 대응)** — 결정: canview 계층(`AGENTS.md` → `docs/README.md` → `docs/resume.md` → 지정 task 1파일)과 `docs/{adr,architecture,runbooks,reviews,tasks}` + validator 2종을 채택하고 하드웨어·차량·firmware 항목은 제외. 추가: `CLAUDE.md`(40줄 이하 포인터), `docs/standards/`, `docs/survey/`(조사; 규범 아님), `docs/plan/`, `docs/dev-environment.md`, `docs/integration-map.md`(생성물), `docs/architecture/adoption-readiness.md`, `docs/architecture/canview-checklist.md`(cv §2·§3 항목별 채택/변형/제외 대조표), `packages/`, `templates/`, `versions.json`, `NOTICE`·`THIRD_PARTY_NOTICES.md`·`PROVENANCE.md`·`CONTRIBUTING.md`·`LICENSES/`. **`docs/decisions.md`는 두지 않고** `docs/adr/README.md`가 단일 색인이며 상단에 "다음 후보 번호는 ADR-NNN"을 명시(cv R2.7 보존). 링크는 저장소 상대 경로만(절대 경로는 validator 오류). 검증 도구는 Python 유지. 채택 사유: `dc` §4, `cv` Q1·Q2·Q3, ktdm DO NOT 15 계열(이중 선언 금지).

**D-03 개발 환경** — 결정: common 정본 = Linux/WSL bash, CI `ubuntu-24.04`. Windows는 Tier 2: `tools/*.py`(validator·check_versions·kt_contrast·ux_lint)는 Windows Python 3.11+ stdlib에서 동작해야 하며 CI `tools` job이 ubuntu+windows 매트릭스로 보증; 패키지 빌드·consumer-smoke는 ubuntu만. runbook 명령은 bash 표기 1벌(`python3 -B -X utf8 …`, `uv run …`, `npm …`) + "Git Bash에서 동일" 1줄; Windows 절(`py -3 -B -X utf8`, nvm-windows, `.gitattributes` LF, `core.autocrlf=false`)은 `docs/dev-environment.md`에만. 임시 worktree 프로필(canview ADR-003): 기본 `F:/dev/kor-travel-common`(WSL `/mnt/f/dev/kor-travel-common`) 작업 브랜치, 병렬·격리·독립 리뷰 때만 `<repo>-wt/<agent>-<task>`, 종료 후 제거·prune. 소비자 공통 절은 OS를 규정하지 않는다(프로필은 각 저장소 `dev-environment.md`). 채택 사유: `dc` C1·C2·C12, `cv` Q4·Q6, 현재 사용자 환경이 Windows.

**D-04 리뷰 gate** — 결정: common 자체는 canview full gate(전문 영역이 다른 리뷰어 2인 독립·상대 결과 비공개·동일 manifest·immutable 기준선(object-only 명령 4개 또는 detached worktree)·P0~P3·disposition `OPEN/FIXED/REJECTED_WITH_EVIDENCE/DEFERRED`(DEFERRED는 P2/P3만)·post-fix 재검토·evidence 파일·archive index). 비면제 목록: `docs/standards/*`, `versions.json`, `packages/*` 공개 API·CSS, `.github/workflows/*`, `AGENTS.md`·`SKILL.md`·`docs/README.md`·ADR·runbook·task/review 규칙. 면제는 오탈자·동의 링크 수정뿐이고 작성자가 아닌 merge 담당이 승인. light/full 판정 주체 = merge 담당(작성자 ≠ 판정자). 상태 어휘 `IN_REVIEW/COMPLETE/POST_FIX_REVIEW`, verdict `BLOCK/CONDITIONAL/PASS`, post-fix는 별도 `-post-fix.md` report(같은 날 같은 범위 반복은 `-02`). 소비자에게는 공통 절 B(Ruthless Review) + TEMPLATE + full/light 표준을 배포하되 채택은 SHOULD. 채택 사유: `dc` C7·Q4, `cv` R3.1~R3.18·Q5.

**D-05 task 원장** — 결정: common은 5열 표 + `READY/BLOCKED/IN_PROGRESS/DONE` + P0~P3 + `validate_plan.py` 무변경. `docs/tasks-done.md`는 5열 고정이므로 완료 날짜는 제목 열 괄호로. `docs/tasks-rule.md` §2.1 보정: 앱 대역(T-410~479)에는 버전 정렬·lock·CI·토큰·UI 채택만, Python 모듈 채택은 T-480~T-489 + `a~z` 접미. 소비자 원장 형식은 규정하지 않고 "ID 재번호 금지·완료 시 evidence 보존·요약에 acceptance 복제 금지·비단순 task는 상세 파일" SHOULD만 배포(체크박스 원장 상태 대응표 제공). 채택 사유: `cv` Q3·§4.1, `dc` §1.7.

### B. 프론트엔드·버전

**D-06 정렬 기준선(2026-09)** — 결정: `versions.json` 각 축은 `floor`(위반 시 fail 후보) / `recommended` / 소비자 `exceptions[]{repo,key,installed,reason,until,review}`. 값:

| 축 | floor | recommended | 예외·비고 |
|---|---|---|---|
| Node | 22.12 | 22.23.x(이미지 `node:22-bookworm-slim` digest) | 24/26 승격은 Phase 5(T-507); Node 20 CI(ktdm·geo·wx)는 T-403 |
| npm | 10.9(Node 22 동봉 10.9.8) | 11.19.x(CI `npm install -g npm@11.19.x` 명시 설치) | map 12.0.1 exact 예외 |
| Next.js | 16.2 | 16.3.4 | map `16.2.12` exact 허용(pin), wx 15·ktdm 14는 Phase 4 |
| React | 19.0 | 19.2.8 | geo·ktdm 18.3.1은 Phase 4 전 예외(tokens만 채택) |
| TypeScript | 5.9 | 5.9.3 | airport 7.0.2 예외(`until`: typescript-eslint peer 확장 또는 2026-12 재판정) |
| Tailwind / @tailwindcss/postcss | 4.3.0 | 4.3.3 | pinvi mobile Tailwind 3(NativeWind 4) 예외 — **O-8 사용자 승인 필요** |
| @base-ui/react | 1.6 | 1.8.0 | ktc 1.5는 채택 PR에서 상향 |
| shadcn CLI | — | 4.21.x, devDependencies | map은 CLI 미설치 유지(테스트가 부재 단언) |
| ESLint / typescript-eslint | 9.0 | 10.x / 8.x | ktdm 8은 Phase 4 |
| Vitest / @playwright/test | 4.1 / 1.60 | 4.1.x / 1.63.x | map Playwright 1.60 exact 예외; wx Vitest 3은 Phase 4 |
| react-query / react-table / react-virtual / zod / zustand / RHF / resolvers | 5 / 8.21 / 3.14 / 4 / 5 / 7.55 / 5 | 최신 5.x / 8.21.x(9는 breaking 미조사) / 3.14.x / 4.5.x / 5.0.x / 7.8x / 5.x | ktc·pinvi resolvers 3은 채택 PR에서 상향 |
| maplibre-gl | 5.24 | 5.24.x | ktc 6.0 예외(공유 라이브러리 peer 정합까지) |
| Python(common 패키지) | 3.11 호환 | — | 앱 `requires-python` 3.12 상향은 Phase 4 앱 결정(O-7) |
| Python 이미지 | 3.11-slim | 3.12-slim(3.13 허용) | |
| uv | 0.11 | 0.12.x | lockfile 의무: `uv.lock` + CI·Docker `--locked`; Poetry(ktdm)·requirements.txt(ktc)는 uv 전환 task |
| FastAPI / Starlette / uvicorn | 0.115 / 미핀 / 0.30 | 0.141.x / 1.6.x / 0.52.x | map `starlette<1.0` 상한은 T-480 재검증 전까지 예외 |
| pydantic / pydantic-settings | 2.9 / 2.5 | 2.13.x / 2.15.x | |
| SQLAlchemy / alembic | 2.0.35 / 1.13 | 2.0.52 / 1.19.x | map `alembic<1.20` 존중 |
| asyncpg / psycopg | 0.29 / 3.2 | 0.31 / 3.3 | 앱 선택 |
| httpx / tenacity / structlog / prometheus-client / typer / dagster | 0.27 / 9 / 24 / 0.20 / 0.12 / 1.9 | 0.28 / 9.1 / 26 / 0.26 / 0.27 / 1.13 | |
| pytest / pytest-asyncio / ruff / mypy / import-linter / testcontainers | 8 / 0.23 / 0.9 / 1.13 / 2.0 / 4.8 | 9.1 / 1.4 / 0.16.x / 2.3.x / 2.15 / 4.15 | |
| PostgreSQL / PostGIS | 별도 트랙(현 16 + 3.5 digest 핀) | — | 라이브러리 정렬 범위 밖 |
| GitHub Actions | 소비자: 현행 major 유지 + SHA 핀 권고 | common 내부: checkout v7·setup-node v7·setup-python v7·setup-uv v10, SHA 핀 | |
| provider `python-*-api` SHA | `providers` 절에 보고만 | — | 정렬 주체는 각 저장소(O-16) |

채택 사유: `vm` §3.2·§4.4(Node 22 동봉 npm 10.9.8)·§5.1·§6·§7.4, `be` §2.1·§5.3(3.11 floor 3곳), `inv/map` §9(exact 핀·pytest 잠금). 판정 3인 모두 coordinator 단일 정확값 표를 기각.

**D-07 핀 정책·검증** — 결정: 계층별 하이브리드 — common 자체 패키지는 정확 핀 + 루트 lockfile; 소비자는 선언 형식 자유이되 **lockfile 의무**(`package-lock.json` v3, `uv.lock`)와 설치본 대조. `tools/check_versions.py`는 매니페스트의 `lockfiles[]`를 읽고 npm lock v3·`uv.lock`·`poetry.lock` 파서로 설치본을 `versions.json`과 대조, 판정 `OK/BELOW_FLOOR/ABOVE_MAX/NOT_RECOMMENDED/NO_LOCK/NO_ENGINES/FLOATING_REF/BLOCKED/EXEMPT/EXEMPT_EXPIRED`, 출력 Markdown 표 + JSON + `$GITHUB_STEP_SUMMARY`. 모드 `report`(기본, exit 0; `FLOATING_REF`·`BLOCKED`·`EXEMPT_EXPIRED`는 `::error::` 주석) → `warn` → `fail`(exit 1). **모드는 `versions.json` `consumers.<repo>.enforce`가 소유**하며 승격 조건(해당 소비자 report 2회 연속 위반 0)을 충족하면 common PR로 전환 — 앱 자율 선언은 기각(지시 (2) 완화). `blocked[]`(예: `mcp>=2`, concierge 2026-09-04 사고)와 `exceptions[].until` 필수. Renovate 설치 미확인 → `templates/dependabot.yml`. 채택 사유: `vm` §7.2~7.4, `be` §5.1(`@main`), `inv/ktc` §4.1, `inv/ktdm` §8-18·19.

**D-08 Tailwind v4 전환** — 결정: 대상 = 미도입→도입 2(airport WIP, weather) + `@config` v3 잔존 정리 3(geo·concierge·pinvi web) + 외부 대기 1(pinvi mobile). 모든 대상은 "6폭 시각 기준선 캡처 → 설정만 → 토큰만 → 컴포넌트" 4단 별도 PR. 순서·조건: ① airport WIP `codex/shadcn-ui-foundation` 병합(값 16/10·alpha line **유지**, `cn`→clsx+tailwind-merge, shadcn/postcss devDependencies) ② ktdm은 Next 16·React 19·ESLint 9·Node 22 업그레이드 PR을 먼저 별도로, 그 후 `@theme`→`--kt-*` 매핑(`ops-*` CSS 잔존 허용) ③ geo는 `@config` 실효값을 빌드 산출 CSS로 검증한 뒤 `@theme` 단일화·`tailwind.config.ts` 삭제(React 19와 독립) ④ concierge는 CI 신설 후 hex fallback 블록·`@config` 제거·`--ktc-*`를 `--kt-*` 오버라이드로 재해석 ⑤ pinvi admin은 `[data-pv-surface='admin']` 스코프만 `--kt-*` 매핑, 사용자 preset 유지 ⑥ weather는 `tokens.css` 교체(Phase 1, Next 버전과 독립; 별칭 shim + font·`--rail` 오버라이드 동반) → Next 16·Vitest 4·Node 22 → `@import "tailwindcss/theme" layer(theme)` + `utilities`만(preflight 제외) → ui v0.2 후 셸·패널·폼·로그인 3분할 PR → preflight 활성화 + 잔존 도메인 CSS `@layer components`. 중단 조건: 시각 diff가 원인 불명으로 남으면 해당 단계 revert. **pinvi mobile Tailwind 3 예외 등록은 지시 (1)의 축소이므로 O-8 사용자 승인 전에는 `exceptions`에 넣지 않고 열림으로 둔다.** 채택 사유: `vm` §1.2·§5.2·§5.3, `inv/weather` §9.1, `inv/airport` §3.2, `dt` §5-3, `inv/pinvi` §3.2.

**D-09 프리미티브·React·Button·DataTable** — 결정: overlay(Dialog·AlertDialog·Popover·Tooltip·Tabs·Breadcrumb·HelpTip)만 `@base-ui/react` 1.8; 비-overlay(Button·Checkbox·Input·Textarea·NativeSelect·Separator·Badge)는 native 요소 + `useRender`로 `render` 합성 선택 지원. `@kor-travel/ui`는 React 19 전용(peer `^19.0.0`, ref prop, forwardRef 없음); React 18 앱(geo·ktdm)은 tokens부터. Button: `type="button"` 엔진 무관 명시 기본, `loading`=`aria-disabled`+`aria-busy`+spinner+포커스 유지+`onClick` 차단(native disabled 안 걺), `disabled`=native + `disabledReason`→`title`, root opacity 금지(라벨 자식 래퍼 흐림), variant 7종(default/outline/secondary/ghost/destructive/destructive-solid/link), size 8종(default/sm/xs/lg/icon/icon-sm/icon-xs/icon-lg; xs·lg·icon-xs·icon-lg는 deprecated alias). Checkbox native `<input>` + `data-slot="checkbox"`. DataTable: TanStack v8, **`manualSorting` 기본 `true` 유지**(map 호출부 무변경; pinvi는 `AdminTable` 어댑터가 `false` 명시) + `enableSortingRemoval`·`initialSorting`·`rowTestId`·`containerTestId`·`stickyHeader`·sr-only 로딩 문구·`rowSelectionLabel`·4상태(loading/empty/error/data) 계약 포함; 검색 툴바·`rowHeader`는 미포함(geo `VirtualTable` 잔류). Dialog는 `hasUnsavedInput`·`viewportProps` 흡수. base-ui 미확인 3건(Button `type` 기본, Checkbox hidden input, Toast API)은 T-201에서 소스 확인 전 릴리스 금지. 토스트 엔진은 앱 소유(정책 UX-G4.1만). 채택 사유: `ui` §3.1~3.4·§5.4·§7, `ux` C10; migration 판정(호출부 전수 수정 회피).

**D-10 UI 배포 방식** — 결정(O-3/O-4 기본값): 1차 배포는 npm 패키지(ESM + d.ts + Tailwind 소스 클래스 + `'use client'`·`'use no memo'` 지시문 보존). **패키지 내부 클래스는 `kt-` 접두 유틸리티만 사용**(`bg-kt-surface-page`, `h-kt-control`, `rounded-kt-control`, `text-kt-2xs`); `theme.css`가 `--color-kt-*`·`--spacing-kt-*`·`--radius-kt-*`·`--text-kt-*`·`--font-kt-*`를 정의(전 저장소 0회 → pinvi 사용자 preset·airport shadcn 기본명과 무충돌, 앱 별칭 계층 불필요). 소비자 필수 2줄: `@import "@kor-travel/tokens/theme.css"` + `@source "../node_modules/@kor-travel/ui"`(모노레포 상대 경로 표는 consumer-adoption.md). `base.css`/`base.scoped.css`(`[data-kt-surface]` 스코프) 2변형. `@kor-travel/ui/cn` = clsx + `extendTailwindMerge`(kt 그룹 등록). 마크업 계약(data-slot·testid·heading 구조·sr-only 문구·geo e2e 셀렉터 대응)은 `docs/standards/ui-contract.md`, 변경은 0.x minor(이관 절 필수)/1.x major. common CI `consumer-smoke`는 webpack·Turbopack 양쪽 `next build`. `noUncheckedIndexedAccess: true` 타입 검사. shadcn 레지스트리 채널은 앱이 소유해야 하는 템플릿(셸 골격·로그인 페이지·playwright 기준선)에만(T-211); 전면 레지스트리는 Phase 5에서 "npm 소비자 우회 패치 2회 이상"일 때만 재검토. 채택 사유: `ui` §6.2·§6.3, `prior` §3.2(반복 동기화 비용)·§7.3, `dt` §3.6.1, migration·directive 판정 2인 `kt-` 채택.

**D-11 배포 채널** — 결정: npm = GitHub Release 자산 tarball(태그 `tokens-vX.Y.Z`·`ui-vX.Y.Z`, 자산 `kor-travel-<pkg>-X.Y.Z.tgz` + `SHA256SUMS`) URL 설치 + lock `integrity`. Python = `git+https://github.com/digitie/kor-travel-common.git@py-vX.Y.Z#subdirectory=packages/py/kor-travel-common`(lock sha) + wheel 자산 병행. 태그 불변, 같은 버전 재발행 금지, `@main` 참조 금지. npm/PyPI 미게시·후보 보존 후 common 구현 순서는 ADR-014를 따른다. Renovate 재평가만 T-507에 남기며 common 공개 범위(O-15)를 승인한 것으로 보지 않는다. 각 tarball·wheel에 `LICENSE`·`NOTICE`·`THIRD_PARTY_NOTICES.md` 동봉 + `license: "GPL-3.0-or-later"` 필드(PEP 639 `license-files`). 채택 사유: `be` §5.2, `prior` §8, `lic` §3.3·§3.5.

**D-12 토큰** — 결정: 변수 접두 `--kt-*`(전 저장소 0회). 계층 2단(semantic ← app override). 역할: surface 4(page/subtle/muted/card)·text 4(primary/secondary/tertiary/disabled)+strong(선택)·icon·border(장식)·control-line(3:1)·brand 4(brand/hover/tint/foreground)·focus·status 4(success/warning/info/destructive)+tint·overlay·radius 2(control 6/panel 8)·control 높이 2(36/30)·rail 22rem·duration 2(fast 100/base 150)·ease 2·shadow 2(elevated/modal)·z 5(nav/panel/overlay/modal/toast)·font 스택(sans/mono). shadcn alias 의미 고정: `--input`=control-line, `--accent`=brand-tint, `--radius`=radius-control, `--border`=장식 border. 프로필 admin/consumer(consumer 값은 문서·`tokens.json` 의미 이름만, pinvi 소유). 타입 스케일은 `@theme`(비inline)로 정의(변수 가리기 기법 지원). 오버라이드 허용 목록 = brand 4·focus·paper(surface) 4·ink(text) 4·status 4+tint(대비 검사 대상)·font 스택; 형태·높이·모션은 프로필로만. 다크: `tokens.css`는 `.dark` 값 완비(map 기본), 앱 오버라이드의 dark 값은 선택, 활성화 파일(`dark-class.css`/`dark-media.css`)은 앱 명시 import, 기본 `color-scheme: light`. 대비: `tools/kt_contrast.py` light 쌍 필수·dark 쌍은 dark 활성 앱만, report 기본 + 앱 `contrast-baseline.json`(미달 쌍 + `until`), 신규 미달만 fail. 값 형식 OKLCH 권고·hex 허용. **정본 = `tokens.css`**, `tokens.json`(DTCG)·`tokens.ts`·`tailwind-preset.cjs`(v3/NativeWind)는 생성물(빌드 diff 검사). 레거시 어휘 별칭 shim `aliases/map-vocabulary.css`(map·weather·geo 공통 이름 → `--kt-*`)를 선택 파일로 제공; 앱 고유 접두(`--ktc-*`·`--color-admin-*`·`--ui-*`)는 앱 파일. 채택 시 font 스택은 앱이 현재 스택으로 오버라이드(Pretendard 1순위 MUST는 Pretendard를 로드하는 앱만; 로딩은 앱 책임, 폰트 파일 미배포). 마커 팔레트 P-01~16은 common 소유 아님(규칙만; hex 정본은 map). 채택 사유: `dt` §3.2~§3.6·§5, `inv/weather` §3.1(map 어휘 294회·`--rail` 17rem), fact 판정 M-1·M-3·M-11.

**D-13 UX·PC/Mobile** — 결정: `docs/standards/ux-guide.md`는 `ux` §2 G0~G9 전부를 규칙 ID `UX-Gn.m`으로 수록하고 규칙마다 MUST/SHOULD 표기(velocity U1~U8 + 4앱 이상 사실 근거 규칙 = MUST, 나머지 SHOULD). 신규 코드 MUST, 기존 잔존은 앱별 baseline(`window.confirm` map 2·ktdm 3·kta 1·wx 1 = 7). admin 장 / 사용자 표면 장 분리. 금지 패턴 grep 7종(raw hex/oklch, `text-[Npx]`, `rounded-2xl+`, 팔레트 alpha, `outline-none`, `transition-all/colors`, `aria-disabled:opacity-`) + `window.confirm`을 `tools/ux_lint.py`가 전체 report + `--base <sha>` diff-based fail. `responsive-web.md`: admin PC-first + ≥320px 컨테인(문서 가로 스크롤 금지), 사용자 웹 mobile-first(하단 탭바·44px·16px 입력·안전영역), 모바일 앱 48px; breakpoint sm 640/md 768/lg 1024(셸 전환)/xl 1280(inspector rail); 검사 폭 320/375/414/768/1024/1440; 터치 admin 36/30(히트 ≥24, micro는 의사요소 확장)/사용자 44/모바일 48; `overflow-x: clip`; light 기본. 충돌 C1~C22는 risk-first 판정 채택: 접힌 rail 4rem(pinvi 5rem 예외), 셸 전환 1024, strip 기본 + drawer 옵션(a11y 계약 동일), 활성 nav tint+mark, 컨트롤 36/30(pinvi admin 44px 2쪽 예외 O-21), 확인 다이얼로그 동사 라벨 필수·`window.confirm` 금지, 토스트 정책(성공은 조용히) 통일·엔진 앱 소유, 상태 5-tone 이름 채택(geo CANCELLED 매핑은 보류), 빈 상태 좌정렬(모바일 앱 가운데 허용), Pretendard 1순위 스택(로딩 앱 책임), 본문 15/12 하한, light 기본, 로그인 타이포 워드마크(아이콘 타일 후속), pathname 노출 대신 breadcrumb, HelpTip popover-only 허용 하위집합, 모달 엔진 앱 소유 + 행동 계약, AppErrorPanel 계보 공통, nav 접근성 이름 라벨만, Hallmark 스탬프는 common 파일에 없음(SPDX만)·SKILL 본문 인용 금지, 지도 스타일 빌더는 범위 밖. dirty 이탈 경고 미포함(O-22). 규칙 4축의 정본·검사·예외: 색상 톤(`design-tokens.md`·`kt_contrast`·`contrast-baseline.json`), UX(`ux-guide.md`·`ux_lint`·baseline), OpenAPI(`openapi.md`·drift 워크플로·`openapi-exceptions.yaml`), PC/Mobile(`responsive-web.md`·playwright 기준선 템플릿·예외). 채택 사유: `ux` §2~§5, `dt` §3.4.1, `lic` B3.

### C. 백엔드·API

**D-14 OpenAPI/REST** — 결정: `oa` §3 M1~M9 / S1~S13 / N1~N8을 3계층으로 채택. 즉시 MUST(additive, 응답 본문 불변): M2(servers 미포함)·M4(X-Request-ID)·M9(production 표면 export)·N6·N7. 신규 표면 MUST / 기존 표면 SHOULD + 예외 등록: M1(export+`--check` — pinvi·ktc·ktdm은 Phase 3 파이프라인 신설 task)·M3(RFC7807 `code`·`request_id`·`errors[]`)·M5(`/health` liveness·`/readyz`·`/version`; geo `/v1/healthz` 별칭은 소비자 probe·Prometheus 갱신 확인 전까지 무기한)·M6(lon/lat)·M7(tz-aware)·M8(securitySchemes)·N1~N5·N8. SHOULD: S1~S13. 예외 레지스트리 `docs/standards/openapi-exceptions.yaml` `{app, rule, surface, reason, sunset|null, review, owner}` + 생성 md; 초기 등록: geo v1(VWorld 호환)·geo v2 envelope(`query_id`↔`request_id`)·pinvi `{error:{}}`·정수 If-Match+409·비버저닝 경로·concierge `/api/v1`·`{detail}`·features export(map provider 외부 계약)·ktdm `/api/v1`·`{detail}`·airport 스펙 422 불일치·map `starlette<1.0`. 검증 오류 422 기본·geo 400 예외. 429 코드 사전은 common 기본(`TOO_MANY_REQUESTS`) + 앱 덮어쓰기. `X-Request-ID` 형식: UUID v4/v7 또는 ULID, ≤128자 ASCII, 검증 실패 시 서버 발급, `trust_incoming=False`는 앱 옵션(ktdm). 헤더 이름은 형식 규칙만(`X-<AppId>-Api-Key|Service-Token|Actor|Admin-Proxy-Secret|Ops-Token|Ops-Scope`), AppId(풀네임/약어)는 앱 소유. map OpenAPI 산출물 변경은 pinvi·ktdm sha256 pin 갱신 PR 동반 없이 머지 금지. 프론트 typegen: `openapi-typescript` 7.x 단일 버전, `gen:types`/`gen:types:check`, pinvi Zod 이중 유지는 "OpenAPI↔Zod 일치 테스트"로(O-14). 채택 사유: `oa` §3~§6, `be` §2.5, `ci` §1.13(S1 `/readyz` 통일).

**D-15 Python 공통 모듈** — 결정: 배포 `kor-travel-common`, import `kortravelcommon`, hatchling, `requires-python >=3.11`(3.11 문법), core는 stdlib+pydantic만(geo·map import-linter 계약), FastAPI 의존은 `[api]` extra, 그 외 `[db]`·`[dagster]`·`[testing]`·`[http]`. 우선순위 1차 C12 openapi export CLI(`--check`·profile 콜백·결정적 직렬화)·C4 health(`/health`·`/readyz`·`/version`, 기존 경로 alias 옵션)·C13 time(KST/UTC·aware 검증)·C20 quality(ruff `extend` 베이스 `line-length=100`·`E,F,I,UP,B,ASYNC`, mypy strict 베이스, import-linter 계약 템플릿, pre-commit 템플릿; **format 규칙 미포함**, per-file-ignores baseline) → 2차 C1 settings 베이스·C9 db 엔진 팩토리·C7 public_api_key·C2 request_id(`trust_incoming`)·C3 metrics(표준 HTTP 3지표·라벨·센티널·multiproc; 접두는 인자) → 3차 C5 errors/problem(opt-in, `exclude_paths`)·C16 security_headers(HSTS 전달 헤더 불신 기본)·C17 cors·C8 trusted_proxy·C11 testing 픽스처·C10 alembic 템플릿·C15 http·C18 dagster → 보류 C6 pagination·C14 geo_primitives(좌표 경계 상수 공통화 금지)·C19 cli.mutex·C21 백업 규약(문서). `[api]` starlette 범위 미선언 + CI 0.4x/1.6 매트릭스. 메트릭 접두: 신규 서비스 `kt<x>_` MUST, map `kor_travel_map_`·pinvi `pinvi_api_`는 기한부 예외(review 2026-12, 대시보드 영향 평가 후 재판정). 인증(비밀번호·세션·CSRF·JWT·RBAC)은 범위 밖 유지. 채택 사유: `be` §3·§4·§5.3·§7, `oa` §5.

**D-16 첫 소비자·순서** — 결정: L6(pinvi 라이선스 선언)을 Phase 0 외부 확인(T-020)으로 승격. tokens 1차 = **map + weather**(즉시; weather는 `tokens.css` 교체+shim) + **pinvi admin(L6 완료 조건)** + airport(WIP 병합 후). ui 1차 = **map + pinvi admin(L6)**, L6가 T-2xx 착수까지 미결이면 airport 소형 부품(Alert·StatStrip·SectionCard·EmptyState·Button)으로 대체. Python 1차 = map-api·weather-api·airport; 2차 geo; 3차 pinvi·concierge·ktdm(L8 후, breaking 묶음). concierge·ktdm은 L8 전에는 규칙 문서·`tokens.json` 참조까지만. 채택 사유: `lic` §3.6·§4 B1·L6·L8, `prior` §1(map↔pinvi 이식 관계), `inv/weather` §8-1, directive 판정(지시 (3) 충족).

### D. 라이선스·운영

**D-17 라이선스·출처** — 결정: common = `GPL-3.0-or-later`. `NOTICE`(저작권자 `Youn-sok Choi (digitie)`·버전·연락처), `THIRD_PARTY_NOTICES.md`(shadcn/ui MIT·@base-ui/react MIT·radix MIT·class-variance-authority **Apache-2.0**(NOTICE 유지)·lucide ISC·tailwind-merge/clsx/tw-animate-css MIT·maplibre-gl BSD-3·pretendard OFL-1.1·TanStack MIT·zod MIT — 버전·URL), `LICENSES/`(MIT·Apache-2.0·ISC·BSD-3-Clause·OFL-1.1·GPL-3.0-or-later 원문), `PROVENANCE.md`(`lic` §2.3 형식: 파일군·원천 저장소·커밋·경로·라이선스·수정), `CONTRIBUTING.md`(AI 보조 생성물은 권리자가 GPL로 배포). 파일 헤더 SPDX(`SPDX-License-Identifier: GPL-3.0-or-later` + `SPDX-FileCopyrightText`) + `Origin:`/`Derived-From:`/`Modified:` 행, `tools/check_spdx.py`(common 파일은 즉시 fail; Hallmark 스탬프는 common 파일에 없음). 추출 규칙: GPL 원천(map·weather·airport) 그대로, geo `-only` 유래는 `-only` 병기(재선언 시 or-later, O-20), MIT 원천(ktc·ktdm) 고지 보존, pinvi는 L6 전 추출 금지(B1), 벤더 tgz·`maplibre-vworld-*`·`python-*-api` 영구 금지(B2, 의존만), Hallmark SKILL 본문 인용 금지(B3), ktc AppShell 복사 여부 diff 후(B4), shadcn 생성물은 MIT 고지(B6), 봇 커밋분은 CONTRIBUTING 문구(B8). 소비 앱: ktc·ktdm 루트 GPL-3.0-or-later 정렬 권고(§7 추가 허가 기각, O-2), map LICENSE 전문 복원(L9), 전 앱 `license` 필드(L11), pg-aiguide 스킬은 common 미배포(각 앱 L12). 앱 사본 drift 비교는 선두 주석 블록 정규화. 채택 사유: `lic` §2~§4·§6, `cm` §4.1.

**D-18 CI·릴리스·포트** — 결정: common CI job = `docs`(link·plan·unittest·`git diff --check`·redaction 전체 트리)·`tools`(도구 자기 테스트, ubuntu+windows)·`packages`(build·`npm pack`·tarball 설치·webpack/Turbopack 스모크)·`python-package`(`uv build`·wheel 설치·starlette 매트릭스)·`consumer-smoke`(실행기 T-010·외부 dispatch T-010a, 주간 활성화는 실제 검증 뒤; 승인 소비자 선택은 ADR-013/014와 consumers.pins.json)·`secret-scan`·`check-versions(report)`. 하드닝: `permissions: contents: read`, `concurrency` cancel-in-progress, `timeout-minutes`, `runs-on: ubuntu-24.04`, PR head SHA checkout, 액션 SHA 핀(+주석 버전). 재사용 워크플로 단계 배포: Phase 1 `versions-check.yml`·`contrast-check.yml`·`docs-check.yml` → Phase 3 `openapi-drift.yml`·`typegen-drift.yml` → Phase 4 `node-quality.yml`·`python-quality.yml`(concierge CI 신설용 T-401 선행). 소비자는 태그/SHA 참조만, job `name:` 입력 개방(map 8·pinvi 5 required check 보전), 앱 기존 워크플로에 job 추가 방식(전면 대체 금지), 운영 호출 job(kta `live-e2e`) required 금지 권고. 릴리스: 패키지별 태그, `-rc.N` → 소비자 PR 검증 → 정식, CHANGELOG 단일 파일에 패키지별 H3. 포트 정본은 ktdm `docs/ports.md`(슬롯 규칙 인용), sibling 140xx/141xx 등록 요청, common `130xx`는 로컬 점유 확인 후(T-014), airport 14002 예외 등록, `-latest` 접미는 ktdm 결정. 서비스/컨테이너/이미지/볼륨/네트워크/env 접두 표준은 `ci` §3.2 채택(이름 변경은 앱 스크립트 동반). Dockerfile·compose 최소 규약은 `ci` §3.3. prod 도메인/IP redaction: common 전체 트리, 소비자 opt-in(O-23). 채택 사유: `ci` §1~§4, `cv` §1.3.

### E. 추가 결정(D-19~D-33)

| ID | 결정 |
|---|---|
| D-19 소비자 매니페스트 | 각 소비 저장소(모노레포는 앱 디렉터리)에 `kor-travel-common.lock.json`(`consumer-manifest.v1`): `repo`·`app`·`tokens{version,override}`·`ui{version}`·`python{version}`·`lockfiles[]{kind,path,scope}`·`contrast{baseline,dark}`·`ux_gate{baseline}`·`openapi{exceptions}`·`exceptions[]`. `enforce`는 두지 않음(common `versions.json` 소유). `docs/integration-map.md`는 `tools/collect_manifests.py`가 `consumers.pins.json`에서 생성(수기 편집 금지). |
| D-20 airport Admin 정의 | 현 실체 = 무인증 백업 패널 + collector-status 패널 + `/v1/admin/*`(ADR-003 무인증 의도). 1차 = tokens + 소형 부품. AdminPageHeader/skip-link/셸·로그인 소비는 airport T-035 라우트 분리 후(O-9). |
| D-21 시각 회귀 기준선 | 토큰·스타일·셸을 바꾸는 소비자 PR은 착수 전 6폭(320/375/414/768/1024/1440) 스크린샷 기준선 + 완료 diff를 **PR evidence**로(저장소 파일 아님). Playwright 없는 앱(wx·ktdm)은 `templates/playwright.baseline.ts`. |
| D-22 헤더·메트릭 접두 | 형식 규칙만 공통, AppId·메트릭 접두는 앱 소유; 신규 `kt<x>_`; 기존 기한부 예외. |
| D-23 공유 라이브러리 정책 | common 범위 밖. `versions.json` `providers` 절은 보고만. `maplibre-vworld-react` npm 게시·`license` 필드, `vworld-style.ts` 중복(map·wx), `python-airkorea-api` 이중 경로, `python-kma-api`·`python-kasi-api` SHA 정렬, 마커 팔레트 hex 정본(map) 확정 요청은 T-505 문서로. |
| D-24 이관 PR 규격 | 한 PR = 한 산출물, 프레임워크 업그레이드 PR과 분리, `git revert` 1회로 원복, lock 동반 커밋, 본문에 검사 결과·스크린샷·되돌리기 명령, 파일 상한(tokens 10·ui 30·py 10, 초과 시 분할). `templates/consumer-pr.md`. |
| D-25 NOT_RUN 표기 | common에서 실행 못 한 검증은 evidence에 `NOT_RUN(사유)`로 남기고 DONE 전 `외부 선행`으로 승격; 0 test/skip을 pass로 집계 금지; 명령을 적은 것은 실행 증거가 아님(cv R1.12·R1.13). |
| D-26 마커 팔레트 | common 소유 아님. 16슬롯·라벨 대비 규칙만 `ux-guide.md`. hex 정본은 map 확정 요청(O-13). |
| D-27 decisions.md·도구 언어·링크 | 미보유 / Python / 저장소 상대 링크만. |
| D-28 회수 측정 | `prior` §11 지표(원본 수정 시간·타 앱 반영 시간·검증 시간·회귀 수·로컬 복사본 수) + drift·EXEMPT·enforce 전환 수를 분기 `docs/reports/adoption-YYYY-QN.md`. 순절감 ≤0 2분기 → 범위 축소; npm 소비자 우회 패치 ≥2 → 배포 방식 재검토. |
| D-29 pinvi 사용자 표면·모바일 | 코드 소비 대상 아님. consumer 프로필 규칙 + `tokens.json` 의미 이름만; 값·밀도는 pinvi 소유. 모바일 Tailwind 3·RN 정확 핀 예외는 O-8 승인 후 등록. |
| D-30 강제 수준 3단 | report → warn → fail; 승격은 common `versions.json`이 소유(D-07). 코드 규칙 게이트(ux_lint)는 diff-based fail + 전체 report. |
| D-31 SemVer 0.x | 0.x 동안 minor = 파괴 허용(`-rc` + 소비자 PR 검증 + CHANGELOG `### Breaking` + 이관 절 필수), patch = 비파괴(additive). 파괴 항목 = 토큰 이름/의미·data-slot/testid·prop 기본값·정렬 모드·CSS 파일 경로. 토큰 이름 폐기는 1 minor 동안 alias 유지. tokens·ui·py 독립 버전, ui는 `@kor-travel/tokens` 같은 minor를 peer. 1.0은 GPL 소비자 3곳 채택 후. 소비자 범위 `~0.N`. |
| D-32 언어·주석 | Markdown·코드 주석·docstring·사용자 문자열 한국어 기본; 식별자·SPDX/Origin 헤더 키·CHANGELOG 절 제목·공식 필드명·명령·URL·패키지명·벤더링 원문·원칙 소제목(Think Before Coding 등) 영어 유지; 커밋 제목은 Conventional Commits 영어 type + 한국어 문장. `design.md` 본문은 한국어(kta·pinvi·wx 이행 대상). |
| D-33 common 자체 툴체인·역할 | 루트 `package.json` `workspaces: ["packages/*"]`, `packageManager: "npm@11.19.1"`, `engines.node ^22.12.0`, `.nvmrc 22.23.1`, 루트 `package-lock.json` 커밋, CI `npm install -g npm@11.19.1` 후 `npm ci`; Python은 `uv` + `packages/py/.../uv.lock`. ui 테스트 하네스 vitest + RTL + jsdom, axe opt-in, showcase 없음(consumer-smoke 대체). 단독 유지자 전제로 공통 API·릴리스 담당과 소비자 통합 담당을 겸임함을 AGENTS 로컬 절에 명시, 긴급 패치 경로(앱 임시 복사 + 종료 조건 기록). 조사 문서는 분기 감사(T-506) 때 기준 커밋을 갱신한 새 절로만 확장. |

## 2. 사용자 확인이 필요한 열린 결정(기본값으로 진행)

| # | 결정 | 기본값 | 막히는 것 |
|---|---|---|---|
| O-1 | pinvi 라이선스·공개 여부(L6) | 공개 + GPL-3.0-or-later, 1 PR(루트 LICENSE·README/AGENTS 정합·`apps/api` pyproject·maplibre 문서 정정) | T-020/T-420 → pinvi 전 트랙 |
| O-2 | ktc·ktdm 루트 GPL 정렬 vs common §7 추가 허가(L8) | GPL 정렬(각 1 PR) | T-021 → T-45x·T-47x 코드 채택 |
| O-3 | UI 배포 방식 | npm 1차 + 레지스트리는 셸·템플릿 채널만 | T-201 |
| O-4 | 유틸리티/변수 네임스페이스 | `kt-` / `--kt-*` | T-101 |
| O-5 | 패키지 식별자 | 닫힘: ADR-014로 확정, 사용자 지시로 공개 registry 이름 확보 제외 | T-015·T-006 |
| O-6 | TS 기준선·airport 7.0.2 | 5.9.3 + airport 예외(typescript-eslint peer 확장 또는 2026-12) | T-433 |
| O-7 | Python 앱 floor 3.12 시점 | Phase 4 앱별; common 3.11 호환 | T-302 |
| O-8 | **pinvi mobile Tailwind 3 예외(지시 (1) 축소)** | 예외 등록 + NativeWind 5 GA 재평가 — 명시 승인 전 미등록 | T-005 exceptions |
| O-9 | airport Admin 정의·WIP 병합 | 현 백업 패널 범위; WIP 값 유지 병합 | T-430~432 |
| O-10 | Node/npm | Node 22 + npm floor 10.9·권장 11.19; map 12.0.1 예외 | T-005 |
| O-11 | 다크 모드 | 정의 필수(map 기본)·활성 opt-in·앱 오버라이드 dark 선택 | T-104 |
| O-12 | 메트릭 접두 map·pinvi | 기한부 예외(review 2026-12) | T-307 |
| O-13 | 마커 팔레트 정본 | map(Tableau) 확정 요청 | T-505 |
| O-14 | 429 코드명·geo v2 problem+json 시점·pinvi Zod | `TOO_MANY_REQUESTS`; ADR-060 묶음; Zod 일치 테스트 | T-301 |
| O-15 | common 저장소 공개 여부·재사용 워크플로 cross-repo 호출 | 공개(GPL) 전제 + 체크아웃 fallback 문서 | T-010 |
| O-16 | 공유 라이브러리 배포 정책·provider SHA | 보고만; 정리 요청 T-505 | 없음 |
| O-17 | Windows 지원 tier | Tier 2(도구·validator Windows 동작 + CI windows job) | T-009 |
| O-18 | Renovate | 미설치, dependabot 템플릿 | T-507 |
| O-19 | 코드 주석·커밋 언어 | 한국어 기본 | T-001 |
| O-20 | geo `GPL-3.0-only` 재선언 | `-or-later` 권고, 전까지 `-only` 병기 | 없음 |
| O-21 | pinvi admin 44px 예외 2쪽 | 영구 예외 | T-422 |
| O-22 | dirty 이탈 경고 | 미포함 | T-105 |
| O-23 | prod redaction 범위 | common 전체 트리, 소비자 opt-in | T-009 |
| O-24 | 포트 `130xx`·airport 14002·`-latest` | 130xx 점유 확인 후; 14002 예외; `-latest`는 ktdm | T-014 |
| O-25 | geo React 19 승인 | 승인(ADR-019 갱신, 별도 PR, 실검증) | T-443 |

## 3. 파일 지도(소유자별)

| 경로 | 소유 작성자 | 비고 |
|---|---|---|
| `AGENTS.md`, `CLAUDE.md`, `SKILL.md`, `README.md`, `docs/README.md`, `docs/dev-environment.md` | entry | |
| `docs/runbooks/agent-workflow.md`, `docs/runbooks/consumer-adoption.md`, `docs/runbooks/release.md`, `docs/resume.md`, `docs/journal.md`, `CHANGELOG.md`, `NOTICE`, `THIRD_PARTY_NOTICES.md`, `PROVENANCE.md`, `CONTRIBUTING.md`, `.github/pull_request_template.md` | runbooks | |
| `docs/architecture/README.md`, `packages.md`, `style-delivery.md`, `consumers.md`, `adoption-readiness.md`, `canview-checklist.md`, `docs/integration-map.md`, `docs/adr/README.md`, `docs/adr/001~012-*.md` | architecture | |
| `docs/standards/README.md`, `design-tokens.md`, `ux-guide.md`, `responsive-web.md`, `frontend-stack.md`, `ui-contract.md` | standards-fe | |
| `docs/standards/openapi.md`, `openapi-exceptions.yaml`, `backend-stack.md`, `ci-deploy.md`, `licensing.md` | standards-be | |
| `docs/standards/versions.md`, `versions.json`, `tools/check_versions.py`, `tests/test_check_versions.py`, `docs/standards/agent-conventions.md`, `templates/README.md`, `templates/AGENTS.common.md`, `templates/CLAUDE.pointer.md`, `templates/agent-config/*`, `templates/consumer-pr.md`, `templates/consumer-adoption-checklist.md`, `templates/dependabot.yml`, `templates/eslint/README.md`, `tools/README.md`(행 추가) | versions-conventions | |
| `docs/tasks/T-*.md` | task 작성자 5(대역별) | |
| `docs/tasks.md`, `docs/plan/integration-plan.md` | ledger | |
| 이미 존재(coordinator 소유, 수정 금지): `docs/tasks-rule.md`, `docs/tasks-done.md`, `docs/tasks/README.md`, `docs/runbooks/README.md`, `docs/runbooks/documentation-maintenance.md`, `docs/runbooks/agent-failure-patterns.md`, `docs/reviews/README.md`, `docs/reviews/adversarial/TEMPLATE.md`, `tools/validate_document_links.py`, `tools/validate_plan.py`, `tests/test_plan_validation.py`, `tests/test_document_links.py`, `.github/workflows/docs.yml`, `.gitignore`, `.gitattributes`, `.editorconfig`, `docs/survey/**`, `LICENSE` | coordinator | 필요한 수정은 open_items로 보고 |

## 4. ADR 목록(architecture 작성자; 파일명 `NNN-<slug>.md`, H1 `# ADR-NNN: 제목`)

| ADR | 제목 | 상태 | 핵심 결정 |
|---|---|---|---|
| 001 | kor-travel-common의 목적·경계·배포 단위 | accepted | D-01, 금지 경계, 소비자 7 |
| 002 | canview 계층형 문서 정보구조와 누적 독립 리뷰 아카이브 채택(차이: decisions.md 미보유·5열 원장·상대 링크·Python 도구) | accepted | D-02·D-04·D-05·D-27 |
| 003 | 개발 환경 정본(Linux/WSL)·Windows Tier 2·임시 worktree | accepted | D-03 |
| 004 | 라이선스 GPL-3.0-or-later와 출처 고지·추출 gate | accepted | D-17 |
| 005 | 배포 채널(GitHub Release tarball·git 태그·wheel)·태그 불변·SemVer 0.x | accepted(패키지명은 잠정, O-5) | D-11·D-31 |
| 006 | 디자인 토큰 계약(`--kt-*`·`kt-` 네임스페이스·계층·프로필·다크·대비·정본 CSS) | accepted(O-4 기본값) | D-12 |
| 007 | React UI 패키지 배포 방식(npm 1차·React 19 전용·overlay base-ui/비-overlay native·마크업 계약·레지스트리 2차) | accepted(O-3 기본값) | D-09·D-10 |
| 008 | 라이브러리·플랫폼 버전 일치 정책(floor/recommended/exceptions 레지스트리·lockfile 의무·판정 어휘·승격 권한) | accepted | D-06·D-07·D-30 |
| 009 | OpenAPI/REST 규약 3계층과 예외 레지스트리·health 경로 | accepted | D-14 |
| 010 | 소비자 채택 모델(매니페스트·첫 소비자 순서·라이선스 gate·채택 PR 규격·시각 기준선·NOT_RUN) | accepted | D-16·D-19·D-21·D-24·D-25 |
| 011 | Python 공통 패키지 구조(extras·3.11 호환·모듈 우선순위·인증 범위 밖·메트릭 접두) | accepted | D-15·D-22 |
| 012 | Tailwind v4 전환 정책(대상·순서·4단 PR·pinvi mobile 예외 보류) | proposed(O-8 대기) | D-08·D-29 |

## 5. 통합 계획 Phase(ledger 작성자용 요약; 상세는 integration-plan.md)

| Phase | 목표 | 산출물 | 완료 기준 | 중단·축소 조건 |
|---|---|---|---|---|
| 0 골격·규칙·gate(이번 PR~) | canview 계층으로 자기 검증 통과, 권리·버전·규칙 정본 존재 | 진입 문서·ADR 12·규칙 문서 9·runbook·NOTICE류·`versions.json`+`check_versions`(report)·task 원장·CI 하드닝 | validator·unittest·docs.yml green; 7 소비자 현재값 등록·report; 2인 리뷰 통과 | npm scope 실패 → 개명(비용 0) |
| 1 tokens + 첫 소비자 | 값 무변경 토큰 패키지가 map·weather(+pinvi admin/airport)에서 시각 diff 0 | `packages/tokens` v0.1.0·shim·kt_contrast·ux_lint·playwright 기준선 템플릿·재사용 워크플로 3종 | 채택 PR 머지 + 6폭 diff 0 + CI green | 원인 불명 diff → patch 후 확대 중단 |
| 2 ui 1차·2차 | 소형 → Button/overlay/Table/DataTable 순 map·pinvi admin(또는 airport) 채택 | `packages/ui` v0.1.0·v0.2.0·ui-contract 확정·base-ui 사실 확인 | e2e green, testid 계약 반영 | 우회 패치 ≥2 → 앱 잔류 |
| 3 py 1차 + OpenAPI 규약 | 계약 무변경 모듈이 map-api·weather-api·airport에서 교체 | py-v0.1.0·openapi 예외 레지스트리 확정·drift 워크플로 | 3곳 drift CI green; map 산출물 무변경 또는 pin 갱신 동반 | pin 갱신 없는 산출물 변경 → rollback |
| 4 앱별 정렬·전환·채택 | 라이선스·React·lock gate가 풀린 앱부터 v4 정리·업그레이드·채택 | geo·concierge·pinvi·weather·ktdm·airport task | `check_versions` 위반 0(예외 제외), 시각 diff 0, e2e green | L6/L8 미결 앱은 규칙 참조까지만 |
| 5 운영·승격·회수 | gate 승격, 릴리스 정착, 보류 재평가 | fail 승격 PR·dependabot·분기 감사·회수 보고·공유 lib 정리 제안·공개 게시 재평가 | 2회 green 후 승격; 분기 보고 | 순절감 ≤0 2분기 → 범위 축소 |

## 6. task 목록(92개; ID·제목·선행·우선순위·Gate·대상·그룹). 상태 규칙: 선행 없음 = READY, 그 외 = BLOCKED. 이번 PR에서 산출되는 항목은 IN_PROGRESS로 두고 리뷰 통과 후 coordinator가 DONE 처리한다(표시 "★이번 PR").

### Phase 0 — T-0xx 저장소 기반·규칙·도구·CI (그룹: 기반)

| ID | 제목 | 선행 | 우선순위 | Gate | 대상 | 비고 |
|---|---|---|---|---|---|---|
| T-001 | 진입 문서·문서 지도·canview 대조표(AGENTS·CLAUDE·SKILL·README·docs/README·dev-environment·canview-checklist·PR 템플릿) | 없음 | P0 | 문서 검증·2인 리뷰 | common | ★이번 PR |
| T-002 | 문서 검증 도구 정정(절대 링크 금지·산문 오탐·Windows 동작·LF)·validator 회귀 테스트·docs.yml 정비 | 없음 | P0 | 도구 테스트·CI | common | ★이번 PR |
| T-003 | 고지·출처 파일(NOTICE·THIRD_PARTY_NOTICES·LICENSES/·PROVENANCE·CONTRIBUTING)·SPDX 헤더 규약·`tools/check_spdx.py` | 없음 | P0 | 문서 검증·도구 테스트 | common | ★이번 PR(check_spdx·LICENSES/ 원문은 잔여) |
| T-004 | ADR-001~012 + `docs/adr/README.md` 단일 색인 | 없음 | P0 | 2인 리뷰 | common | ★이번 PR |
| T-005 | `versions.json` v1 + `tools/check_versions.py`(npm lock v3·report·판정 어휘) + `docs/standards/versions.md` + 7 소비자 현재값·예외 등록 | 없음 | P0 | 도구 테스트·문서 검증 | common | ★이번 PR(현재값 등록은 잔여) |
| T-005a | `check_versions`: `uv.lock` 파서 | T-005 | P1 | 도구 테스트 | common | |
| T-005b | `check_versions`: `poetry.lock`·`requirements.txt` 파서 + `NO_LOCK` 보고 | T-005 | P2 | 도구 테스트 | common | |
| T-006 | npm scope `@kor-travel`·PyPI 이름 가용성 확인·확보(사용자 계정 작업; 실패 시 개명) | 없음 | P1 | 외부 확인 | 외부 | 외부 선행: 사용자 |
| T-007 | runbook 본문(agent-workflow·consumer-adoption·release)·`docs/standards/agent-conventions.md`·`templates/` | 없음 | P0 | 문서 검증·2인 리뷰 | common | ★이번 PR |
| T-008 | `docs/architecture/*`(README·packages·style-delivery·consumers·adoption-readiness)·`docs/integration-map.md` 초기판 | 없음 | P0 | 문서 검증·2인 리뷰 | common | ★이번 PR |
| T-009 | common CI 하드닝(permissions·concurrency·timeout·ubuntu-24.04·액션 SHA 핀)·`tools` windows 매트릭스·`secret-scan`·`check-versions(report)` job·branch protection 문서·redaction guard | T-002 | P1 | CI | common | |
| T-010 | 재사용 워크플로 1단계(`versions-check`·`contrast-check`·`docs-check`) + `workflows-selftest` fixture + `consumers.pins.json` + `consumer-smoke` | T-005, T-009 | P1 | selftest | common | |
| T-011 | 소비자 매니페스트 스키마 `consumer-manifest.v1` + `tools/validate_manifest.py` + 7 소비자 초기 매니페스트 초안 | T-005 | P1 | 도구 테스트 | common | |
| T-012 | `tools/collect_manifests.py` → `docs/integration-map.md` 생성 + `docs/architecture/adoption-readiness.md` gate 표 갱신 | T-011 | P2 | 도구 테스트 | common | |
| T-014 | common 포트 `130xx` 로컬 점유 확인·확정 + ktdm `docs/ports.md` sibling(airport 140xx·weather 141xx·common 130xx) 등록 요청 + `-latest` 접미 질의 | 없음 | P3 | 외부 확인 | common/ktdm | |
| T-020 | pinvi 라이선스 결정(L6) 반영: 결정 기록·pinvi PR 요청 문서·common 소비 gate 해제 조건 | 없음 | P0 | 문서 | common/pinvi | 외부 선행: 사용자 O-1 |
| T-021 | ktc·ktdm 라이선스 정렬(L8) 결정 반영: 결정 기록·각 저장소 PR 요청 문서 | 없음 | P1 | 문서 | common/ktc/ktdm | 외부 선행: 사용자 O-2 |

### Phase 1 — T-1xx 토큰·스타일·UX 규약 (그룹: 토큰)

| ID | 제목 | 선행 | 우선순위 | Gate | 대상 | 비고 |
|---|---|---|---|---|---|---|
| T-101 | `packages/tokens`(tokens.css map 값+.dark·theme.css `kt-`·shadcn.css·base.css·base.scoped.css·dark-class/media.css) + 생성물(tokens.json·tokens.ts·tailwind-preset.cjs; 정본 CSS) + 루트 npm workspace·lock + `npm pack` 설치 스모크 | T-003, T-004 | P0 | 패키지 빌드·tarball 설치 | common | |
| T-102 | 레거시 어휘 별칭 shim `aliases/map-vocabulary.css`(map·weather·geo 공통 이름 → `--kt-*`) + weather `--rail`·font 오버라이드 예제 + 별칭 충돌 검사 스크립트 | T-101 | P0 | 도구 테스트 | common | |
| T-103 | `tools/kt_contrast.py`(report·`contrast-baseline.json`) + `tools/ux_lint.py`(금지 7종+window.confirm, 전체 report·diff fail) + 4앱 오버라이드 예제 보고 | T-101 | P1 | 도구 테스트 | common | |
| T-104 | `docs/standards/design-tokens.md` 확정(패키지 실물과 대조·규칙 ID TK-n) | T-101 | P0 | 2인 리뷰 | common | ★이번 PR 초안 |
| T-105 | `docs/standards/ux-guide.md` 확정(UX-Gn.m·MUST/SHOULD·C1~C22·baseline·예외) | 없음 | P1 | 2인 리뷰 | common | ★이번 PR 초안 |
| T-106 | `docs/standards/responsive-web.md` 확정 | 없음 | P1 | 2인 리뷰 | common | ★이번 PR 초안 |
| T-107 | `docs/standards/frontend-stack.md` 확정 + `templates/eslint/*.mjs`·tsconfig base·postcss·components.json 조각 | 없음 | P1 | 2인 리뷰 | common | ★이번 PR 초안 |
| T-108 | `templates/playwright.baseline.ts`(6폭 스크린샷) + 기준선 캡처 절차(consumer-adoption 절) | 없음 | P1 | 도구 테스트 | common | |
| T-109 | tokens `v0.1.0-rc.1` → map·weather 검증 → `tokens-v0.1.0` 정식 + SHA256SUMS | T-101, T-102, T-103, T-104 | P1 | consumer-smoke | common | |

### Phase 2 — T-2xx React UI 패키지 (그룹: UI)

| ID | 제목 | 선행 | 우선순위 | Gate | 대상 | 비고 |
|---|---|---|---|---|---|---|
| T-201 | `packages/ui` 골격(ESM·d.ts·subpath exports·`'use client'`/`'use no memo'` 보존·peer react ^19·인라인 아이콘·`cn` extendTailwindMerge·noUncheckedIndexedAccess) + base-ui 사실 확인 3건 기록 + pack 스모크(webpack/Turbopack) | T-101 | P0 | 패키지 빌드·tarball | common | |
| T-203 | ui 1차 소형 13종(Badge·Skeleton·Separator·Card·Alert·Input·Textarea·NativeSelect·Field·EmptyState·SectionCard·FilterBar·StatStrip) + 단위 테스트(vitest+RTL+jsdom) | T-201 | P0 | 단위 테스트·tarball | common | |
| T-204 | `docs/standards/ui-contract.md` 확정(data-slot·testid·heading·sr-only·geo 셀렉터 대응·SemVer 0.x) | T-203 | P0 | 2인 리뷰 | common | ★이번 PR 초안 |
| T-205 | Button(D-09 계약)·AppErrorPanel·error-recovery | T-203 | P1 | 단위 테스트 | common | |
| T-206 | overlay 세트(Dialog(hasUnsavedInput·viewportProps)·AlertDialog·Popover·Tooltip·Tabs·Breadcrumb·HelpTip) + Table primitive + native Checkbox | T-205 | P1 | 단위 테스트 | common | |
| T-208 | DataTable(manualSorting 기본 true·removal·testid·sr-only·4상태) + OffsetPager/CursorPager | T-206 | P1 | 단위 테스트·2인 리뷰 | common | |
| T-209 | CopyButton·JsonViewer·DetailList(`onNotify` 주입)·StatusBadge(사전 주입형) | T-206 | P2 | 단위 테스트 | common | |
| T-210 | AdminPageHeader·AdminSkipLink·AdminRailGrid + FormFieldInput/FormSelect/FormTextArea + form-validation(헤드리스) | T-206 | P2 | 단위 테스트 | common | |
| T-211 | 레지스트리 채널(셸 골격·로그인 페이지·playwright 기준선 템플릿) + `tools/ui_drift.py`(npm 소비자 로컬 패치 탐지) | T-210 | P3 | selftest | common | |
| T-212 | ui `v0.1.0` rc → map + pinvi admin(L6) 또는 airport 검증 → 정식 | T-203, T-204 | P1 | consumer-smoke | common | 외부 선행: T-020 또는 T-430 |
| T-213 | ui `v0.2.0`(Button·overlay·Table·DataTable·Pager·Copy/Json/Detail·Header/Form) rc → 정식 | T-208, T-209, T-210 | P1 | consumer-smoke·2인 리뷰 | common | |

### Phase 3 — T-3xx Python 공통 패키지·OpenAPI (그룹: 백엔드)

| ID | 제목 | 선행 | 우선순위 | Gate | 대상 | 비고 |
|---|---|---|---|---|---|---|
| T-301 | `docs/standards/openapi.md` 확정 + `openapi-exceptions.yaml` 초기 등록 + 헤더·X-Request-ID 형식 규칙 | 없음 | P0 | 2인 리뷰 | common | ★이번 PR 초안 |
| T-302 | `packages/py/kor-travel-common` 골격(hatchling·extras·3.11 문법 검사·uv.lock·starlette 0.4x/1.6 CI 매트릭스) + `docs/standards/backend-stack.md` 확정 | T-003 | P0 | python-package | common | ★이번 PR 초안(문서) |
| T-303 | C12 openapi export CLI(`--check`·profile 콜백·결정적 직렬화) + typegen 규약 템플릿 | T-302 | P0 | 단위 테스트 | common | |
| T-304 | C4 health(`/health`·`/readyz`·`/version`·alias 옵션) + C13 time | T-302 | P1 | 단위 테스트 | common | |
| T-305 | C20 quality 산출물(ruff extend·mypy·import-linter·pre-commit·CI 템플릿; format 미포함) + common 자기 적용 | T-302 | P1 | 자기 적용 | common | |
| T-306 | C1 settings 베이스 + C9 db 엔진 팩토리 + C7 public_api_key | T-304 | P1 | 단위 테스트(testcontainers) | common | |
| T-307 | C2 request_id(`trust_incoming`·형식 검증) + C3 metrics(표준 라벨·센티널·multiproc; 접두 인자) | T-304 | P1 | 단위 테스트 | common | |
| T-308 | C5 errors/problem(`exclude_paths`)·C16 security_headers·C17 cors·C8 trusted_proxy·C11 testing·C10 alembic 템플릿·C15 http·C18 dagster | T-306, T-307 | P2 | 단위 테스트 | common | |
| T-309 | 재사용 워크플로 2단계(`openapi-drift.yml`·`typegen-drift.yml`) + selftest | T-303, T-010 | P1 | selftest | common | |
| T-310 | `py-v0.1.0`(1차) → weather-api·map-api·airport 검증 → 정식(wheel 자산) | T-303, T-304, T-305 | P1 | 소비자 스모크 | common | |

### Phase 4 — T-4xx 소비 앱 이관 (그룹: 소비자 — 앱별)

| ID | 제목 | 선행 | 우선순위 | Gate | 대상 | 비고 |
|---|---|---|---|---|---|---|
| T-401 | 재사용 워크플로 3단계(`node-quality.yml`·`python-quality.yml`) + selftest(concierge CI 신설용) | T-010 | P1 | selftest | common | |
| T-402 | 7앱 시각 회귀 기준선 초기 캡처(앱별 evidence; 미실행 NOT_RUN) | T-108 | P2 | NOT_RUN 허용 | 전 앱 | |
| T-403 | 공통 CI 정렬: Node 20→22(ktdm·geo·wx)·액션 SHA 핀·`check_versions` report job 삽입·매니페스트 커밋(7 저장소) | T-010, T-011 | P1 | 각 저장소 CI | 전 앱 | |
| T-410 | map: `globals.css` → `@import "@kor-travel/tokens"` + 빈 brand 오버라이드 + 매니페스트(값 diff 0) + LICENSE 전문 복원(L9)·`license` 필드 | T-109 | P0 | e2e 30·vitest 42·시각 diff | map | |
| T-411 | map: ui v0.1 소형 shim 채택 + `@source` + `verify:frontend-eslint` 집합 갱신 | T-212, T-410 | P1 | e2e 30 | map | |
| T-412 | map: ui v0.2 채택(Checkbox 호출부 3파일) + `data-table.test.tsx` 이관 + `ux_lint` report | T-213, T-411 | P1 | e2e 30·vitest 42 | map | |
| T-413 | map: Next 16.3·base-ui 1.8·Playwright 1.63 상향(`verify-next-sharp.mjs`·`test_frontend_dependency_security.py`·이미지 동반, 별도 PR) | T-005 | P2 | 전 CI | map | |
| T-420 | pinvi: L6 결정 반영 PR(루트 LICENSE·README/AGENTS 정합·`apps/api` pyproject·maplibre 문서 정정) | T-020 | P0 | docs | pinvi | 외부 선행: 사용자 O-1 |
| T-421 | pinvi: admin `--color-admin-*`→`--kt-*` 오버라이드 + `base.scoped.css` + 매니페스트(사용자 표면 무변경 e2e) | T-420, T-109 | P1 | admin e2e·app-shell-mobile e2e | pinvi | |
| T-422 | pinvi: ui v0.1/v0.2 채택(`AdminTable` 어댑터 유지·`cn` 재수출·44px 예외 등록·webpack 빌드) | T-421, T-213 | P1 | e2e 56·vitest 27 | pinvi | |
| T-430 | airport: WIP `codex/shadcn-ui-foundation` 병합(값 유지·`cn`→clsx+twMerge·devDeps 이동·Button D-09 레시피) | 없음 | P0 | frontend CI | airport | 외부 선행: WIP PR·CI 확인(O-9) |
| T-431 | airport: tokens 채택(alias 재매핑 유지·`dark-media.css`·contrast baseline) + 매니페스트 | T-430, T-109 | P1 | build·320px 게이트 | airport | |
| T-432 | airport: 소형 ui 채택(백업·collector 패널: Alert·StatStrip·SectionCard·EmptyState·Button) | T-431, T-212 | P2 | build·vitest | airport | |
| T-433 | airport: TS 7 예외 등록·ESLint 도입 판정·절대 링크 상대화·prod placeholder 치환·`engines` 선언 | T-005 | P2 | CI | airport | |
| T-440 | geo: Node 22 CI + `uv.lock` 도입 + pre-commit rev 정렬 | T-005 | P1 | ci.yml | geo | |
| T-441 | geo: `@config` 실효값 빌드 검증 → `@theme` 단일화·`tailwind.config.ts` 삭제 → tokens 채택(`--ui-*` 별칭 유지) + contrast baseline + 매니페스트 | T-109 | P1 | 시각 diff·e2e 23 | geo | |
| T-443 | geo: React 19 업그레이드(ADR-019 갱신, 별도 PR, 실검증) | T-440 | P2 | unit 43·e2e 23 | geo | 외부 선행: O-25 |
| T-444 | geo: radix→base-ui 이관(12파일·`asChild` 17곳) + ui v0.2 채택(셀렉터 diff evidence; VirtualTable 잔류) | T-443, T-441, T-213 | P2 | e2e·a11y 4 spec | geo | |
| T-450 | concierge: `pyproject.toml`·`uv.lock`(`mcp<2` blocked)·ruff/mypy baseline 도입 | T-305 | P0 | 로컬 4 gate | concierge | |
| T-451 | concierge: CI 신설(재사용 워크플로 호출·versions-check) + production `frontend/Dockerfile` | T-401, T-450 | P0 | CI | concierge | |
| T-453 | concierge: hex fallback 블록 제거 → `@config`→`@theme inline` → `--ktc-*`를 `--kt-*` 오버라이드로 + contrast baseline + 매니페스트 | T-451, T-109 | P1 | e2e 45·시각 diff | concierge | |
| T-454 | concierge: ui v0.2 채택(18종 shim·base-ui 1.8·`render` 9줄) | T-021, T-453, T-213 | P2 | e2e 45 | concierge | 외부 선행: O-2 |
| T-460 | weather: Next 16·Vitest 4·Node 22 CI·eslint-config-next 16·`moduleResolution: bundler`·react-query 미사용 정리·CI vitest/mypy 추가(별도 PR) | T-005 | P1 | ci.yml | weather | |
| T-461 | weather: `app/tokens.css` → `@kor-travel/tokens/tokens.css` + `aliases/map-vocabulary.css` + navy·`--rail`·font 오버라이드 + 매니페스트(6폭 diff 0 evidence) | T-109 | P0 | 시각 diff(수동) | weather | |
| T-462 | weather: Tailwind v4 도입(theme+utilities, preflight 제외) + `@theme inline` 1:1 매핑 | T-460, T-461 | P1 | 시각 diff | weather | |
| T-463 | weather: 셸/패널·표/폼·로그인 → common 컴포넌트 3분할 PR, 해당 CSS 절 삭제 | T-462, T-213 | P1 | 시각 diff·vitest | weather | |
| T-464 | weather: preflight 활성화 + 잔존 도메인 CSS `@layer components` + 마커 색 토큰화 + 셸 문서-코드 불일치 해소 | T-463 | P2 | 시각 diff | weather | |
| T-470 | ktdm: Next 16·React 19·ESLint 9·Node 22 CI 업그레이드(재포맷 금지, recharts 3·`target es5` 실검증, 별도 PR) | T-005 | P1 | vitest 8·build | ktdm | |
| T-471 | ktdm: Poetry→`uv.lock`·하한 상향·CI 핀 정리 + quality baseline | T-305 | P1 | ci.yml | ktdm | |
| T-472 | ktdm: tokens 채택(`@theme`→`--kt-*`·Ember 값 유지·tint 4종) + contrast baseline + 매니페스트 | T-470, T-109 | P2 | 시각 diff(수동) | ktdm | |
| T-473 | ktdm: ui 부분 채택(StatStrip·AppErrorPanel·SectionCard; `ops-*` 잔존 허용) | T-021, T-472, T-213 | P3 | vitest | ktdm | 외부 선행: O-2 |
| T-480 | map-api: py 1차 채택(export CLI·health·time·quality) + `type` URI·429 코드 정렬 + pinvi/ktdm pin 갱신 PR 동반 | T-310 | P1 | openapi.yml·pin 대조 | map(+pinvi/ktdm) | |
| T-481 | weather-api: py 1차 채택 + `--check` 전환 + airkorea 스냅샷 정본 결정(L15) + Python 3.11/3.12/3.13 정합 | T-310 | P1 | ci.yml | weather | |
| T-482 | airport: py 1차 채택 + `code`/`request_id` additive + 스펙 422 정합 + `--check` CI + Docker `uv sync --locked` | T-310 | P1 | backend CI | airport | |
| T-483 | geo: py 2차(health alias 병행·securitySchemes+typegen 재생성·admin problem+json opt-in·request-id) | T-308, T-440 | P2 | openapi drift·gen:types | geo | |
| T-484 | pinvi: `uv.lock` CI·Docker 소비 + etl `@main` 제거 + export 파이프라인·drift CI + request-id(additive) | T-310, T-420 | P2 | api.yml·etl.yml | pinvi | |
| T-485 | concierge: py 1차(export·request-id·quality) + features export 계약 문서화(map provider 동시 수정 계획) | T-451, T-310 | P2 | CI | concierge/map | |
| T-486 | ktdm: py 2차(request-id `trust_incoming=False`·quality baseline) | T-471, T-307 | P3 | ci.yml | ktdm | |

### Phase 5 — T-5xx 릴리스·승격·회수 (그룹: 운영)

| ID | 제목 | 선행 | 우선순위 | Gate | 대상 | 비고 |
|---|---|---|---|---|---|---|
| T-501 | 릴리스 runbook 1회 완주 검증(rc→소비자 PR→정식→되돌리기 리허설) | T-109, T-212 | P1 | consumer-smoke | common | |
| T-502 | gate 승격: `check_versions`·`kt_contrast`·`ux_lint`를 소비자별 2회 green 후 `enforce: fail`(common PR) + 승격 절차 runbook | T-403, T-103 | P2 | CI | common+전 앱 | |
| T-503 | 회수 지표 1회차 보고 `docs/reports/adoption-2026-Q4.md` | T-411, T-461 | P2 | 문서 검증 | common | |
| T-505 | 공유 라이브러리·마커 팔레트 정본 결정 요청 문서(`maplibre-vworld-react` npm·`license`·`vworld-style.ts` 중복·airkorea 이중 경로·kma/kasi SHA·P-01~16 hex) | T-008 | P3 | 문서 | 외부 저장소 | |
| T-506 | 분기별 cross-repo drift 감사 runbook + 첫 실행 + 조사 기준 커밋 갱신 절 | T-012 | P2 | 문서 검증 | common | |
| T-507 | 재평가: 공개 npm/PyPI 게시·Renovate·Vitest 5·Node 24/26·react-table 9·lucide 1.x·mypy 2·TS 7 → `versions.json` 갱신 | T-006, T-005 | P3 | 문서·도구 테스트 | common | |
| T-508 | 보류 항목 재평가(api-client-core·pagination 코덱·VirtualTable 흡수·ConfirmDialog API·토스트·전면 레지스트리) | T-213, T-310 | P3 | 2인 리뷰 | common | |

## 7. 작성자 공통 유의사항

- 이번 PR에서 만드는 규칙 문서는 "정본 초안"이며 실물 패키지(T-101·T-201·T-302)와 대조해 확정하는 task가 남아 있음을 각 문서 머리에 1문장으로 밝힌다.
- 조사 문서(`docs/survey/*`)의 오기 정정 값은 `docs/survey/README.md` §6.2를 따른다(pinvi admin ui 28파일, airport openapi 21 paths, pinvi JWT 10분, pinvi AdminTable 35~36, `window.confirm` 7건, readiness 경로 `/readyz`, Node 22 동봉 npm 10.9.8, common Python floor 3.11).
- 사용자 지시 완화로 보일 수 있는 유일한 항목은 pinvi mobile Tailwind 3 예외(O-8)이며, 문서에는 "사용자 승인 대기"로만 적는다.
