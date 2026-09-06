# kor-travel-common 결정 레지스터 — 위험·정확성 우선(risk-first) 독립안

- 작성일: 2026-09-06 · 관점: 회귀·보안·계약 파손·라이선스·검증 불가 gate를 최소화하는 순서로 사용자 지시 (1)~(7)을 **후퇴 없이** 달성한다.
- 입력: `docs/survey/README.md`, `commonality-matrix.md`, `cross/*.md` 10편, `inventory/*.md` 7편(§1·§8·§9·§11), coordinator 초안(D-01~D-18, F절), `docs/tasks-rule.md`, `docs/runbooks/documentation-maintenance.md`, `docs/reviews/README.md`, `tools/validate_plan.py`, 선행 보고서(geo `docs/kor-travel-common-library-review.md`). common 작업 트리 상태는 `git status`로 재확인(HEAD `b92fabe`, 추적 파일 `LICENSE` 1개, scaffold 미추적, `AGENTS.md`·`docs/tasks.md`·ADR 없음 — 사실).
- 표기: **사실** = 조사 문서가 파일에서 확인 / **후보** = 이 레지스터의 설계 선택 / **추정** = 정황 / **열림** = 사용자 확인 필요(§F에 기본값과 함께 모음). 근거 약칭은 `commonality-matrix.md` 머리 규약(`vm`=version-matrix, `dt`=design-tokens, `ui`=ui-components, `ux`=ux-patterns, `be`=backend, `oa`=openapi, `ci`=ci-deploy, `dc`=docs-conventions, `cv`=canview-structure-checklist, `lic`=licensing, `inv/<app>`=인벤토리, `cm`=commonality-matrix, `prior`=선행 보고서)을 따른다.
- 각 결정의 필드 순서: **실패 시나리오 → 결정 → 대안(기각 이유) → 근거 → 소비자 영향(앱별) → 열림**. 실패 시나리오를 먼저 적는 이유는 "무엇이 깨지는가"가 정해져야 결정의 순서·조건이 정해지기 때문이다.
- coordinator 초안과의 차이는 §G 표에 모았다. 초안 문장은 복사하지 않았다.

## 0. 이 관점의 다섯 가지 원칙(모든 결정에 공통 적용)

| # | 원칙 | 적용 |
|---|---|---|
| R1 | **근거가 확실한 것만 코드로, 합의 안 된 것은 규칙 문서로** | 두 앱 이상에서 계약이 이미 같거나(사실) 이식 관계가 소스에 명시된 것만 패키지에 넣는다. 계약이 갈리는 것(토스트·ConfirmDialog·DataTable 정렬 기본값·에러 envelope 전환)은 `docs/standards/*`에 규칙과 예외 레지스트리로만 둔다 |
| R2 | **소비자 PR 하나는 revert 하나로 되돌릴 수 있어야 한다** | 프레임워크 업그레이드(Next/React/ESLint/Node)와 common 채택은 항상 별도 PR·별도 task. 같은 버전 덮어쓰기 금지(`prior` §8) |
| R3 | **gate는 "보고" 단계를 거친 뒤에만 "실패"로 승격** | `check_versions`·`kt-contrast`·ruff 프리셋·openapi drift는 소비자별 baseline 허용 목록을 두고, 2회 연속 green 이후 fail 승격 |
| R4 | **권리·계약이 확인되지 않은 파일은 옮기지 않는다** | `lic` §4 B1~B10을 task 선행 조건으로 박는다. pinvi 파일 추출, ktc/ktdm의 common **코드** 링크는 라이선스 결정(L6·L8) 전까지 BLOCKED |
| R5 | **검증 불가능한 것을 통과로 표시하지 않는다** | 브라우저 렌더·소비자 e2e·registry 권한처럼 이 저장소에서 실행 못 하는 검증은 task의 `외부 선행`·`evidence`에 NOT_RUN으로 남긴다(canview A2.5·`cv` R1.13) |

---

## A. 저장소 범위·구조

### D-01 배포 단위와 패키지 경계(이름·exports·peer·채널)

- 실패 시나리오: (a) `@kor-travel` npm org를 제3자가 소유하고 있으면 소비자 3곳이 채택한 뒤 import 경로 전면 개명 → 회귀 3배. (b) 하나의 패키지에 Python·React·설정을 섞으면 React 18 앱(geo·ktdm)이 토큰만 원해도 설치가 막힌다(`ui` §2.3 peer 사실). (c) ESLint 프리셋을 강제 배포하면 map의 `verify-frontend-eslint-config.mjs`(effective config 바이트 잠금, `inv/map` §3.1)와 pinvi의 Hallmark `no-restricted-syntax`(`inv/pinvi` §3.1)가 깨진다. (d) `api-client-core`를 먼저 만들면 4개 앱의 `ApiError` 형태가 달라(`cm` §2.3) 어댑터만 늘고 계약은 안 모인다.
- 결정(후보):
  1. **배포 단위 3 + 규칙 문서 + 레지스트리**로 시작한다. `packages/tokens`(npm, React 무관), `packages/ui`(npm, React 19 전용), `packages/py/kor-travel-common`(Python dist `kor-travel-common`, import `kortravelcommon`, extras `api`/`db`/`dagster`/`testing`/`http`). `config`·`api-client-core` 패키지는 **만들지 않는다**(아래 대안).
  2. exports: tokens = `./tokens.css`, `./theme.css`, `./shadcn.css`, `./base.css`, `./base.scoped.css`, `./dark-class.css`, `./dark-media.css`, `./tokens.json`, `./tokens.js`(TS 상수), `./tailwind-preset.cjs`(v3/NativeWind 소비용). ui = `.`(barrel 금지, 컴포넌트별 subpath `./button`, `./badge` …)와 `./styles.css`(선택). deep import는 `exports`로 차단(`prior` §7.3 [E4]).
  3. peer: ui → `react ^19.0.0`, `react-dom ^19.0.0`, `@base-ui/react ^1.8.0`, `tailwindcss ^4.3.0`(소비자가 `@source` 등록), `@kor-travel/tokens`(같은 minor). **lucide-react는 peer로 두지 않는다** — 스피너·체크·셰브론 등 내부 아이콘은 인라인 SVG로 동봉(0.363~1.41 major 혼재, breaking 미조사 — `vm` §1.3·열린 질문 13).
  4. 이름: `package.json`의 `name`은 `@kor-travel/<pkg>`를 **잠정**으로 두되, 첫 소비자 PR 전에 T-006(scope 확보 확인) gate를 통과해야 한다. 실패 시 개명 비용은 이 시점이 0에 가깝다. Python dist는 `kor-travel-common`(PyPI 404 = 미점유 사실)이며 게시하지 않는다.
  5. 의존 방향: 앱 → ui → tokens, 앱 → py 단방향. common은 앱 도메인·지도 엔진(`maplibre-vworld-*`)·인증 서비스·`python-*-api`를 import·재래핑하지 않는다(`prior` §7.2, `be` §4).
- 대안(기각): 단일 거대 패키지(React 18 앱 토큰 소비 차단, `prior` §6 비권고). `config` npm 패키지(실패 (c); 대신 `docs/standards/frontend-stack.md`에 규칙 카탈로그 + `templates/eslint/*.mjs` **조각**만 제공, 소비자가 opt-in). `api-client-core`(실패 (d); 백엔드 problem+json 통일이 두 앱에서 wire로 확인된 뒤 재평가 — Phase 5). shadcn 자체 레지스트리(A안)를 1차로 두는 것(복사 후 drift가 27/27 상이의 원인 — `ui` §2.1·§6.2).
- 근거: `prior` §7.1(두 패키지에서 시작), `ui` §4.1~4.3·§6.2, `be` §3·§5.3, `dt` §3.6.3, `cm` §2.2·§2.3, `vm` §1.3.
- 소비자 영향: map: tokens·ui 1차 소비, config 없음이라 자체 verify 스크립트 무변경 · pinvi: admin 표면만 ui 소비(사용자 표면 금지, ESLint 경계 유지) · geo·ktdm: React 19 전까지 tokens만 · weather: `tokens.css`(순수 CSS)는 Tailwind 없이도 즉시 소비 가능 · airport: WIP 병합 후 tokens→ui · concierge: L8 결정 전 코드 링크 불가(규칙 문서만).
- 열림: 스코프 이름(`@kor-travel` vs `@digitie/kor-travel-*`) — §F-1.

### D-02 저장소 구조(canview 대응)

- 실패 시나리오: canview 구조를 "파일 목록"으로만 복사하면 `docs/decisions.md`·`adr/README.md` 이중 색인(`cv` F19·Q1), 절대 링크 접두 허용(`cv` Q2)처럼 canview가 스스로 정본화하지 못한 부분까지 따라와 drift가 생긴다. 현재 `docs.yml`은 링크 오류 17건으로 push 즉시 red(`cv` §1.3 사실).
- 결정(후보): canview 계층(AGENTS 정본 → `docs/README.md` 라우터 → resume → 지정 task 1파일)과 `docs/{adr,architecture,runbooks,reviews,tasks}` + validator 2종을 채택하고, 하드웨어·차량·firmware 항목은 제외(`cv` §1.1 불필요 판정 그대로). 추가: `CLAUDE.md`(40줄 이하 포인터, `dc` C3), `docs/standards/`, `docs/survey/`(조사 스냅샷, 규범 아님), `docs/plan/`, `docs/dev-environment.md`, `docs/integration-map.md`(소비자별 채택 버전표), `docs/architecture/adoption-readiness.md`(`cv` F22·F23 변형), `packages/`, `templates/`, `versions.json`. **`docs/decisions.md`는 두지 않고 `docs/adr/README.md` 단일 색인**(다음 번호 명시)으로 고정하며, `documentation-maintenance.md` §2·§3의 `decisions.md` 문구를 T-002에서 정정한다(한 사실 두 곳 선언 금지 — ktdm DO NOT 15 계열). `validate_document_links.py`의 절대 접두 허용은 제거(절대 링크 = 오류, `dc` C11).
- 대안(기각): canview처럼 이중 색인 유지(drift), 절대 접두 유지(다른 체크아웃에서 깨짐 — kta 17개 md 사례 `dc` §1.8).
- 근거: `dc` §2 C3·C8·C11·C16, §4 대응표; `cv` §1.1~§1.3, §5 Q1·Q2·Q7.
- 소비자 영향: 소비자 저장소 구조는 강제하지 않는다(로컬 절 유지). 배포 대상은 AGENTS 공통 절 A~I와 `docs/` 트리 표준(`dc` §3.2)뿐.
- 열림: 없음(구조 결정은 common 내부).

### D-03 개발 환경 정본(common 자체·공통 절)

- 실패 시나리오: canview(Windows PowerShell 정본)를 그대로 옮기면 소비자 6/7(Linux/WSL 정본, `dc` §1.11 사실)과 runbook 명령 표기가 어긋나고, common `.py` 사본의 CRLF(`cv` §1.2)처럼 개행 사고가 재발한다.
- 결정(후보): common 자체 정본 = Linux/WSL bash, CI = `ubuntu-24.04` 고정. 공통 절은 OS를 규정하지 않고 `docs/dev-environment.md`가 프로필(고정/임시 worktree)을 선언하도록 위임(`dc` C1·C2). worktree 불변 조건 5개만 공통. `.gitattributes` `* text=auto eol=lf`, 첫 커밋에서 `.py` CRLF 정규화 확인(`cv` Q6).
- 대안(기각): Windows 정본(소비자 다수와 불일치), 두 벌 명령 블록(drift).
- 근거: `dc` §1.11·§1.12·§2 C1·C2·C15; `cv` A5.1·A5.2·Q4·Q6.
- 소비자 영향: 없음(기존 ADR 존중). pinvi·map의 MCP 설정 Windows 경로는 로컬 override로 남긴다(`dc` C13).
- 열림: 경로 표기(`F:/dev/…` vs `/mnt/f/dev/…`) — §F-14(기본: 문서는 저장소 상대 경로만, 절대 경로는 dev-environment.md에만).

### D-04 리뷰 gate

- 실패 시나리오: full/light 판정을 PR 작성자에게 맡기면 정책·계약 변경이 light로 우회된다(`dc` Q4). 반대로 전부 full이면 문서 오탈자까지 evidence 파일이 요구돼 gate가 형식화된다.
- 결정(후보): common 자체는 canview full gate(2인 독립·immutable 기준선·evidence·P0~P3·disposition 4종·post-fix 재검토)를 **비면제 목록**에 적용 — `docs/standards/*`, `versions.json`, `packages/*` 공개 API·CSS 산출물, `.github/workflows/*`(재사용 워크플로), AGENTS/SKILL/ADR/runbook/task·review 규칙. 면제는 오탈자·동의된 링크 수정뿐. 소비자 표준은 full/light 2단계로 배포하되 **판정 주체는 merge 담당(작성자 ≠ 판정자)**, 근거를 PR 본문에 남긴다. 상태 어휘 집합을 TEMPLATE·README에 명시(`IN_REVIEW`/`COMPLETE`/`POST_FIX_REVIEW`, verdict `BLOCK`/`CONDITIONAL`/`PASS`; post-fix는 `-post-fix` 별도 report — `cv` Q5).
- 대안(기각): 작성자 자율 판정(우회), 전부 full(형식화).
- 근거: `dc` §1.5·§2 C7·§3.4; `cv` §3.3 R3.1~R3.18; `docs/reviews/README.md` 규칙 4·7·9.
- 소비자 영향: kta는 James/Popper 관행 유지 가능(페르소나명 로컬) · map: 1 review approval 규칙 위에 light 요약 추가 · 나머지는 관행을 규칙으로 승격.
- 열림: 없음.

### D-05 task 원장 형식

- 실패 시나리오: `dc` §3.3(체크박스 원장)을 채택하면 현재 `validate_plan.py`(5열 표 파서, `cv` §4.1 사실)를 바꿔야 하고 35개 회귀 테스트 계약이 깨진다. map의 평면화 사고(acceptance 삭제 후 무조건 완료, `dc` §1.7)는 "요약과 상세의 기계 대조"가 없어서 생겼다.
- 결정(후보): common 자체는 5열 표 + `READY/BLOCKED/IN_PROGRESS/DONE` + `validate_plan.py` **무변경**(현재 `docs/tasks-rule.md` 그대로). 소비자 표준은 체크박스 원장을 허용하되 상태 대응표와 "요약에 acceptance 복제 금지·상세 파일 필수(비단순)"만 공통 규약으로 배포. `validate_task_ledger.py`(체크박스용)는 소비자 opt-in 도구로 Phase 5.
- 대안(기각): validator 교체(회귀), 소비자에 5열 표 강제(7개 저장소 원장 재작성 비용).
- 근거: `cv` §4.1·§4.2·Q3; `dc` §1.7·§3.3; `docs/tasks-rule.md` §2~§6.
- 소비자 영향: 없음(선택). ID 대역은 common 내부 규칙.
- 열림: 없음.

---

## B. 프론트엔드 스택·버전 정렬

### D-06 정렬 기준선 표(프론트·백엔드·도구·CI·이미지)

- 실패 시나리오: (a) 최신값(TS 7, Vitest 5, react-table 9, lucide 1.x)을 기준선으로 박으면 typescript-eslint peer(`<6.1.0`, `vm` §1.6 사실)·Node 20 CI(`vm` §5.3)·breaking 미조사 항목(`vm` 열린 질문 13)이 한꺼번에 터진다. (b) 정확 핀 하나를 7개 저장소에 강제하면 map의 `next 16.2.12` exact + `verify-next-sharp.mjs` + pytest 잠금(`inv/map` §9)과 즉시 충돌해 map CI가 red가 된다. (c) Python `>=3.12`를 common 자체 floor로 두면 map·weather·ktdm(3.11 floor, `be` §2.1)이 설치조차 못 한다.
- 결정(후보): 기준선은 **"floor(허용 하한) / recommended(권장 정확값) / consumer pin(저장소별 실제값)" 3열**로 `versions.json`에 두고, 강제 대상은 floor 위반·blocked 범위·floating 참조뿐이다(D-07). 2026-09 기준선:

| 축 | floor | recommended | 근거·주의 |
|---|---|---|---|
| Node 런타임 | 22.12(Vitest 4/5 engines) | 22.23.x LTS, 이미지 `node:22-bookworm-slim@sha256` digest | 이미지 7곳 모두 22(`vm` §3.3). Node 20 CI 3곳(dm·geo·weather)은 EOL → T-4xx 선행. 24/26 승격은 Phase 5 재평가 |
| npm | 11.19 | 저장소별 exact 유지(map 12.0.1, pinvi 11.19.1) | 동봉 npm 10.9(`vm` §3.2). 단일값 강제하지 않음(map verify 스크립트 회귀 방지) |
| Next.js | 16.2 | 16.3.x | dm 14, weather 15는 별도 업그레이드 PR(R2) |
| React | 19.0 | 19.2.x | geo·dm 18.3.1은 tokens만 소비(D-09) |
| TypeScript | 5.9 | 5.9.3 | airport 7.0.2는 **등록 예외**(ESLint 도입 시 재판정, `vm` §6) |
| Tailwind / @tailwindcss/postcss | 4.3.0 | 4.3.3 | `@config` 잔존 3곳은 D-08 |
| @base-ui/react | 1.8.0 | 1.8.0 | concierge 1.5, map 1.6 상향은 ui 채택 PR에 포함 |
| shadcn CLI | — | devDependencies에만, 소스 소유(CLI 재생성 금지) | map 테스트가 devDeps 부재를 단언(`lic` D9) → map은 CLI 미설치 예외 |
| cva / clsx / tailwind-merge | 0.7.1 / 2.1.1 / 3.6.0 | 동일 | 4개 앱 동일 설치(`vm` §1.3). airport WIP `cn@0.2.5`는 정렬 대상 |
| lucide-react | 0.460 | 앱 선택 | common은 의존하지 않음(D-01) |
| ESLint | 9.39 | 10.x(신규) | flat config 전제. dm 8은 Next 16 전환과 함께(`vm` §5.3) |
| Vitest / Playwright | 4.1 / 1.60 | 4.1.x / 1.63.x | Vitest 5는 출시 3일(`vm` §4.2) — Phase 5 재평가. map Playwright 1.60 exact+이미지는 예외 등록 |
| react-query / react-table / react-virtual | 5.90 / 8.21 / 3.14 | 5.10x / 8.21.x / 3.14.x | react-table 9 미조사 → blocked가 아니라 "미평가" |
| zod / RHF / resolvers / zustand | 4.4 / 7.77 / 5.4(신규) / 5.0 | — | resolvers 3.x(concierge·pinvi)는 예외 등록, 강제 안 함 |
| maplibre-gl | 5.24 | 5.24.x | concierge 6.0은 예외 등록(공유 lib peer `^5.24`, `vm` §1.5) |
| Python(common 자체) | **3.11** | 3.12-slim 이미지, 3.13 허용 | common 코드는 3.11 문법(PEP 695 금지). 앱 floor 3.12 상향은 앱 결정 |
| uv | 0.11 | 0.12.x | 잠금 도구 통일(D-07) |
| fastapi / starlette / uvicorn / pydantic / pydantic-settings | 0.115 / (미핀) / 0.30 / 2.9 / 2.4 | 0.141.x / 1.6.x / 0.52.x / 2.13.x / 2.15.x | common `[api]`는 **starlette를 핀하지 않는다**(map `<1.0` 상한, `vm` §2.2); CI 매트릭스에 starlette 0.4x·1.6 양쪽 |
| SQLAlchemy / alembic | 2.0.35 / 1.19 | 2.0.52 / 1.19.x | map `alembic<1.20` 상한 존중(named CHECK 사유) |
| asyncpg / psycopg | 0.30 / 3.2 | 0.31 / 3.3 | 앱 선택(C9가 둘 다 흡수) |
| structlog / prometheus-client / httpx / tenacity | 24.4 / 0.20 / 0.27 / 9.0 | 26.x / 0.26 / 0.28 / 9.1 | httpx `<1.0` 상한 유지 |
| dagster | 1.9 | 1.13.x | `[dagster]` extra만 |
| pytest / pytest-asyncio / ruff / mypy / import-linter / testcontainers | 8.3 / 0.24 / 0.9 / 1.13 / 2.0 / 4.8 | 9.1 / 1.4 / 0.16 / 2.3 / 2.15 / 4.15 | mypy 2.x breaking 미조사(`vm` 열린 질문 13) — "권장"까지만 |
| PostgreSQL / PostGIS | 16 / 3.5 | digest 핀 유지 | 라이브러리 정렬 범위 **밖**(별도 트랙, `vm` Q9) |
| GitHub Actions | v4/v5 + SHA 핀 | v7 계열 + SHA 핀(common 재사용 워크플로 내부) | 소비자 액션 major 상향은 강제하지 않음 |
| Prometheus | — | 앱 소유 | v2.53 vs v3.5(`ci` §1.13) — 규칙 범위 밖 |

- 대안(기각): 후보 B "2026-09 최신"(실패 (a)), 단일 exact 기준선(실패 (b)), Python 3.12 floor(실패 (c)).
- 근거: `vm` §1.8·§2.1·§4·§5.1·§5.3·§6·§7; `be` §2.1·§5.3·§7-1·2; `inv/map` §9; `inv/airport` §9.
- 소비자 영향: map: floor 위반 0, exact 핀 유지 · pinvi: floor 위반 0(resolvers 3 예외) · geo: React·Node CI·lock 3건 격차 · dm: Next·React·ESLint·Node CI·lock 5건 · weather: Next·Vitest·Node CI·Tailwind 4건 · concierge: lock·CI·maplibre 예외 · airport: TS 예외·lint 부재.
- 열림: TS 기준선(§F-3), Node 24 승격 시점(§F-4).

### D-07 핀 정책·`versions.json` 스키마·검증 스크립트 동작

- 실패 시나리오: (a) lockfile 없는 4곳(geo·map·dm·concierge, `vm` §2.1)에서는 "일치"를 검증할 대상 자체가 없다 — 정책이 문서로만 남는다. (b) 검증 스크립트가 도입 즉시 실패로 동작하면 7개 저장소 CI가 동시에 red가 되어 아무도 켜지 않는다. (c) 이동 참조(pinvi etl `python-kasi-api@main`, `be` §5.1)와 `mcp` 2.x 유입 사고(`inv/ktc` §4.1)는 핀 정책이 아니라 상한·blocked 부재가 원인이다.
- 결정(후보):
  1. **P3 계층별 하이브리드**: 플랫폼·프레임워크·툴체인(D-06 표의 floor/recommended 행)은 registry 대조 대상, 나머지는 caret + lockfile.
  2. **lockfile 의무**: npm `package-lock.json`(lockfileVersion 3) + Python `uv.lock`을 CI·Docker 모두 `--locked`/`npm ci`로 소비(weather 모델, `vm` §2.1). Poetry(dm)·requirements.txt(concierge)는 uv 전환 task. 상한 없는 `>=` 전용 선언은 `blocked`와 함께 관리.
  3. **금지 3종은 Phase 2부터 즉시 실패**: floating git ref(`@main`, `@master`), `latest` 이미지 태그(운영 compose), `blocked` 범위 매치. 그 외는 report → fail 승격(R3).
  4. `versions.json` 스키마(`kor-travel-common.version-registry.v1`, 미지 키 거부, 순서 고정 — dm registry 관행 차용 `vm` §7.3):

```json
{
  "schema": "kor-travel-common.version-registry.v1",
  "baseline": "2026-09",
  "updated_at": "2026-09-06",
  "toolchain": {
    "node":   { "floor": "22.12.0", "recommended": "22.23.1", "image": "node:22.23.1-bookworm-slim@sha256:<digest>" },
    "npm":    { "floor": "11.19.0", "recommended": null, "note": "저장소 exact 유지 허용" },
    "python": { "floor": "3.11", "recommended": "3.12", "image": "python:3.12-slim@sha256:<digest>", "uv": "0.12.10" }
  },
  "npm":  { "next": { "floor": "16.2.0", "recommended": "16.3.4" }, "react": { "floor": "19.0.0", "recommended": "19.2.8" },
            "typescript": { "floor": "5.9.0", "recommended": "5.9.3", "max": "5.9.x" }, "tailwindcss": { "floor": "4.3.0", "recommended": "4.3.3" } },
  "pypi": { "fastapi": { "floor": "0.115", "recommended": "0.141.1" }, "alembic": { "floor": "1.19", "recommended": "1.19.2" } },
  "images":  { "postgis": { "recommended": "postgis/postgis@sha256:<digest>", "track": "db-major-separate" } },
  "actions": { "actions/checkout": { "recommended": "v7.0.1", "sha": "<40hex>" } },
  "blocked": [ { "ecosystem": "pypi", "name": "mcp", "range": ">=2", "reason": "FastMCP API 변경, concierge 2026-09-04 crash-loop", "since": "2026-09-04" } ],
  "consumers": {
    "kor-travel-map": { "manifests": ["package.json", "packages/kor-travel-map-admin/frontend/package.json", "pyproject.toml"],
                        "locks": ["package-lock.json"], "require_lock": { "npm": true, "pypi": false },
                        "enforce": "report",
                        "exceptions": [ { "name": "npm", "pin": "12.0.1", "reason": "verify-npm-tree.mjs", "until": "2026-12-31" },
                                        { "name": "starlette", "range": "<1.0", "reason": "TestClient/httpx2 미검증", "until": "2026-12-31" } ] }
  }
}
```

  5. `tools/check_versions.py` 동작: 입력 = registry + 소비자 체크아웃 경로(로컬) 또는 CI 내 자기 저장소. 읽는 것 = `package.json`(engines·deps·overrides), `package-lock.json`(설치본), `pyproject.toml`/`requirements*.txt`(선언), `uv.lock`(설치본), `Dockerfile*` FROM, `.github/workflows/*.yml` `uses:`·`node-version`·`python-version`. 판정 = `OK`/`BELOW_FLOOR`/`ABOVE_MAX`/`NOT_RECOMMENDED`/`NO_LOCK`/`FLOATING_REF`/`BLOCKED`/`EXCEPTION(만료일)`. 출력 = Markdown 표 + JSON. 종료 코드: `enforce: report`면 항상 0(단 `BLOCKED`·`FLOATING_REF`·만료 예외는 report 모드에서도 1), `enforce: fail`이면 `BELOW_FLOOR`·`NO_LOCK`도 1. 승격 조건: 소비자 CI에서 report 2회 연속 위반 0 → registry `enforce`를 `fail`로 바꾸는 common PR이 곧 승격 기록.
  6. 자동 갱신: Renovate 설치 가능 여부 미확인(`vm` 열린 질문 12) → Phase 5 전까지 `templates/dependabot.yml` + 분기별 `check_versions` 보고서로 대체.
- 대안(기각): P1 전면 exact(봇 없이 유지 불가), P2 caret+lock만(정렬 목표 표현 불가), 이미지 라벨로 검증(`oa` Q8 — lock보다 늦고 드물다).
- 근거: `vm` §3.6·§7.1~7.4·열린 질문 7·10·11·12; `be` §5.1·§7-9; `inv/ktdm` §8-18·19(유도→결박→탐지, pin registry 형식).
- 소비자 영향: geo·map·dm·concierge: `uv.lock` 도입 PR(T-48x) 선행 · pinvi: `uv.lock`을 CI·Docker에서 실제 소비 · airport: Docker pip → `uv sync --locked` · weather: 변경 최소(모델).
- 열림: provider `python-*-api` SHA를 registry에 넣을지(§F-5, 기본: `providers` 절에 **보고만**).

### D-08 Tailwind v4 전환 — 대상별 방식과 순서

- 실패 시나리오: (a) weather에 `@import "tailwindcss"`를 넣는 순간 preflight가 `button`/`table`/`a` 전역 규칙 23종을 리셋해 13개 TSX·220개 className이 무스타일이 된다(`inv/weather` §9.1 사실). Playwright가 없어 320~768px 컨테인 검증을 수동으로만 할 수 있다. (b) geo·concierge에서 `@config`를 지우면 `theme.extend.colors` 43개와 `@theme inline`의 동명 utility 중 어느 쪽이 실효했는지 미확인(`dt` §5-3)이라 색이 조용히 바뀐다. (c) pinvi web에서 `@config`를 지우면 모바일(NativeWind 4, Tailwind 3.4.19)과 preset 이중 정본이 갈라지고 Dockerfile 런타임 복사 전략(중첩 `node_modules` 의존)이 깨진다(`inv/pinvi` §3.2). (d) dm에서 v4 정리와 Next 14→16·React 18→19를 한 PR에 묶으면 실패 원인을 분리할 수 없다(`prior` §2).
- 결정(후보) — 전제 (1)의 실제 대상은 "미도입→도입" 2곳 + "혼합 정리" 3곳 + "외부 대기" 1곳(`vm` §1.2 사실)이며, 각 대상은 **"시각 회귀 기준선 캡처 → 설정만 → 토큰만 → 컴포넌트"** 4단을 반드시 별도 PR로 밟는다:

| 순서 | 대상 | 방식 | 선행·중단 조건 |
|---|---|---|---|
| 1 | airport WIP(`99b3f98`, 이미 v4.3.3 + shadcn `base-nova`) | WIP를 main에 병합하되 `tokens.css` 16/10px·alpha line은 **유지**(값 변경은 D-12 프로필 정렬 task로 분리), `cn@0.2.5`→clsx+tailwind-merge, `shadcn`·`postcss`·`@tailwindcss/postcss`를 devDependencies로 이동 | 선행: WIP PR·CI 확인(`inv/airport` §11-1 미확인). 중단: `live-e2e` 외 frontend job red |
| 2 | docker-manager(v4 설치 있음, `ops-*` 146줄+유틸 혼용) | ① Next 16·React 19·ESLint 9·Node 22 CI 업그레이드 PR(대규모 재포맷 금지, `inv/ktdm` §9) → ② `tokens.css` `@theme`을 `--kt-*` 매핑으로 교체(값 Ember 유지) → ③ `ops-*` 클래스는 **잔존 허용**, common UI 채택 시 컴포넌트 단위로만 교체 | 중단: ①에서 recharts 3·`target es5` 문제 발생 시 v4 정리를 ①과 분리 유지 |
| 3 | geo(`@config` 잔존, source(none)+@source) | ① 빌드 산출 CSS로 `brand` 등 동명 utility의 실효값 확인(T-441) → ② 확인된 값으로 `@theme` 단일화, `tailwind.config.ts` 삭제 → ③ `--ui-*` 3층 별칭을 `shadcn.css` 매핑으로 축약 | 선행: React 19 업그레이드와 **독립**. 중단: ①에서 두 값이 다르면 시각 회귀 기준선 재캡처 후 진행 |
| 4 | concierge(`@config` + hex fallback 블록) | ① `globals.css` 앞쪽 fallback 블록 제거(정본 이중화 해소, `dt` §3.1.1) → ② `tailwind.config.ts` colors/radius/spacing을 `@theme inline`으로 이전 → ③ `--ktc-*`를 `--kt-*` 오버라이드로 재해석(D-12) | 선행: CI 신설(T-451) 없이는 회귀 검증 불가 → BLOCKED |
| 5 | pinvi web | admin만 `[data-pv-surface='admin']` 스코프 안에서 `--kt-*` 매핑. **사용자 표면 `@config` v3 preset은 유지**(모바일 결합). 웹 전용 `@theme` 이전은 NativeWind 5 GA 이후 | 선행: 라이선스 L6(D-17). 중단: webpack 강제(ADR-066) 하 common CSS 미탐지 |
| 6 | weather(Tailwind 없음, 2,495행 CSS) | ① Next 16·Vitest 4·Node 22 CI(별도 PR) → ② `@import "tailwindcss/theme" layer(theme)` + `utilities`만 도입(**preflight 제외**), `tokens.css`는 `@theme inline` 매핑으로 1:1 이전(shadcn 이름 이미 보유, `inv/weather` §3.1) → ③ 페이지 단위로 셸·패널·폼을 common 컴포넌트로 교체하며 해당 CSS 절 삭제 → ④ 마지막에 preflight 활성화 + 잔존 도메인 CSS(약 800행)는 `@layer components`로 유지 | 선행: 320/375/414/768/1024/1440 스크린샷 기준선(T-460). 중단: 기준선 대비 diff 발생 시 해당 절 롤백 |
| — | pinvi mobile | **문서화된 예외**(NativeWind 4 = Tailwind 3). `tokens.json`/`tailwind-preset.cjs`로 의미 토큰만 공급. NativeWind 5 GA 시 재평가 | 정렬 정책의 `exceptions`에 등록 |

- 대안(기각): weather를 "사전 빌드 CSS + CSS 변수"로 남기기(`prior` §7.3 — 전제 (1) 위반; 단 ②단계까지는 그 접근이 안전하므로 순서로 흡수). dm v4 정리를 프레임워크 업그레이드와 동시 진행(실패 (d)). geo `@config` 즉시 삭제(실패 (b)).
- 근거: `vm` §1.2·§1.7·§5.2·§5.3; `inv/weather` §3.1·§9·§9.1; `inv/airport` §3.2·§9; `inv/geo` §3.1·§9; `inv/ktc` §3.1·§9; `inv/pinvi` §3.1·§3.2·§9; `inv/ktdm` §3.1·§9; `dt` §3.1.1·§3.6.3·§5-3.
- 소비자 영향: airport: 1주 내 병합 가능 · dm: 업그레이드 PR 2개 선행 · geo: 빌드 검증 1 task 선행 · concierge: CI 신설 선행 · pinvi: L6 선행 · weather: 4 PR, 가장 긴 트랙 · mobile: 없음.
- 열림: airport WIP 방향(값 수렴 여부, §F-9), weather 셸 교체 vs 문서 수정(§F-10).

### D-09 프리미티브 엔진·React 범위·Button/DataTable 계약

- 실패 시나리오: (a) React 18 지원을 선언하면 `forwardRef` 없는 컴포넌트가 geo·dm에서 ref를 조용히 잃는다(`ui` §2.3 추정). (b) base-ui Button의 `type="button"` 기본은 pinvi 주석 근거뿐(`ui` §5.4 미확인) → 엔진 교체 시 폼 안 보조 버튼이 submit을 일으킬 수 있다. (c) base-ui Checkbox의 hidden input 여부 미확인 → `FormData` 직렬화 누락. (d) DataTable을 `manualSorting=true` 단일 기본으로 배포하면 pinvi 36페이지(`AdminTable`, `manualSorting=false` 고정)와 e2e testid 계약(`admin-table-scroll` 등)이 깨진다(`ui` §3.3 사실). (e) geo `VirtualTable`(13 소비 파일, `as="table"` 26회)을 DataTable로 바꾸면 검색 툴바·`rowHeader`가 사라진다.
- 결정(후보):
  1. 엔진: overlay(Dialog/AlertDialog/Popover/Tooltip/Tabs)만 `@base-ui/react`; Button/Checkbox/Input/Textarea/NativeSelect/Separator/Badge는 **native 요소**(pinvi 절충, `ui` §5.4). `render` 합성은 Badge/Breadcrumb에 `useRender`로 제공하되 Button은 `render` 대신 `<a className={buttonVariants()}>` 관용구를 문서화(geo `asChild` 17곳 이관 지침).
  2. React: **19 전용**, peer `react ^19.0.0`으로 설치 단계에서 fail-fast. 18 앱은 tokens만.
  3. Button 계약(고정): `type="button"`을 **엔진과 무관하게 명시** 기본; `loading` = `aria-disabled`+`aria-busy`+spinner+포커스 유지+`onClick` 차단(map·concierge·pinvi admin 동일 계약 사실); `disabled`는 native + `disabledReason`→`title`; root opacity 금지(라벨 래퍼 `opacity-55`); variant 7종·size 4+icon(`xs`/`lg`는 deprecated alias). pinvi 사용자 `Button`(native disabled)은 **범위 밖**.
  4. Checkbox: native `<input type=checkbox>` + `onCheckedChange(boolean)` + `data-slot="checkbox"`; Table 선택 열 셀렉터는 `[data-slot=checkbox]`(엔진 무관).
  5. DataTable: `sortMode: "server" | "client"` **필수 prop**(기본값 없음 → 컴파일 오류로 강제), `enableSortingRemoval` 지원, `rowTestId`/`containerTestId`/`stickyHeader`/sr-only 로딩 문구를 계약에 포함(pinvi e2e 보전). 검색 툴바·`rowHeader`는 **포함하지 않고** geo `VirtualTable`은 geo 잔류(Phase 5 재평가).
- 대안(기각): radix 채택(변경 파일 12 vs 29, style 정합 1:3 — `ui` §5.3), React 18/19 동시 지원(실패 (a)), DataTable 기본값 하나(실패 (d)).
- 근거: `ui` §3.1~§3.4·§4.1·§4.2·§5.1~§5.4·§7-1·2·4·6; `prior` §3.3·§3.4.
- 소비자 영향: map: Button 무변경, Checkbox 엔진 교체(3파일) · pinvi admin: `AdminTable` 어댑터 유지, `sortMode` 매핑 1줄 · concierge: `render` 9줄 → 관용구 · geo: React 19 후 `asChild` 17곳 · airport WIP: `loading`·`destructive-solid` 신규.
- 열림: base-ui `type`·hidden input·Toast API 확인(구현 task에서 소스 확인 — 열림 아님, `외부 선행`).

### D-10 UI 배포 방식(Tailwind 소스 + `@source`)

- 실패 시나리오: (a) Tailwind 소스 클래스를 배포했는데 소비자가 `@source`를 등록하지 않으면 무스타일(`prior` §7.3 [E1]); geo는 `source(none)`이라 더 확실히 빠진다(`inv/geo` §9). (b) `base.css`의 전역 `:focus-visible`·`button{cursor}`가 pinvi 사용자 표면에 누출된다(`prior` §5). (c) pinvi webpack 강제·Turbopack 청크 파손(ADR-066) 환경에서 패키지 CSS/ESM 해석이 다르다. (d) 소비자 e2e 셀렉터(geo `section.panel .panel-header h2`, `pre.json-box`; pinvi testid)가 마크업 변경으로 깨진다.
- 결정(후보): npm 패키지 = ESM + `.d.ts` + Tailwind 소스 클래스(공통 토큰 utility 이름 `bg-surface-page`, `h-control`) + 컴포넌트별 `'use client'` 보존. 소비자 필수 2줄: `@import "@kor-travel/tokens/theme.css"` + `@source "../node_modules/@kor-travel/ui"`. `base.css`는 두 변형 — `base.css`(전역, 단일 표면 앱) / `base.scoped.css`(`[data-kt-surface]` 하위만; pinvi·airport처럼 표면이 섞이는 앱). common CI의 `consumer-smoke`는 webpack·Turbopack 양쪽에서 `next build`를 돈다. 마크업 계약(data-slot·testid·heading 구조)은 `docs/standards/ui-contract.md`에 명시하고 변경 시 major.
- 대안(기각): 사전 빌드 CSS 단독(`prior` §7.3 — Tailwind 없는 앱은 D-08 ②단계까지만 그 형태; 두 방식 동시 지원은 시작 시 금지), shadcn 레지스트리 1차(drift).
- 근거: `ui` §6.2·§6.3·§7-8·9; `dt` §3.6.3; `inv/pinvi` §3.1·§9; `inv/geo` §9.
- 소비자 영향: 전 앱 `@source` 1줄 · pinvi: `base.scoped.css` · geo: `@source` 목록에 패키지 추가.
- 열림: 없음.

### D-11 배포 채널

- 실패 시나리오: 공개 npm 게시는 scope 미확보(403)·라이선스 미정 상태에서 되돌릴 수 없고(unpublish 제한), GitHub Packages는 소비자 CI마다 토큰이 필요하다(`prior` §8 [E5]). `@main` 참조는 재현 불가(`be` §5.1 위반 사례).
- 결정(후보): npm = **GitHub Release tarball**(태그 `tokens-vX.Y.Z`/`ui-vX.Y.Z`, 자산 `kor-travel-<pkg>-X.Y.Z.tgz`, 소비자 `package.json`은 URL + lockfile `integrity`). Python = `git+https://github.com/digitie/kor-travel-common.git@py-vX.Y.Z#subdirectory=packages/py/kor-travel-common` + `uv.lock` sha. 규칙: 같은 태그 재발행 금지, 태그는 immutable, 소비자는 sha/integrity를 lock에 기록. 공개 npm/PyPI 게시는 Phase 5 재평가(D-01 gate 통과 후).
- 대안(기각): 공개 npm 즉시(불가역), GitHub Packages(인증), git URL + prepare(모노레포 subpath 빌드 불편).
- 근거: `be` §5.2 A안; `prior` §8; `ci` §2.3.
- 소비자 영향: 모든 소비자 동일(URL 의존 1줄 + lock).
- 열림: 공개 게시 시점(§F-2).

### D-12 토큰 접두·계층·프로필·다크 모드·오버라이드·대비 검사

- 실패 시나리오: (a) `--ktc-*`를 common 접두로 쓰면 concierge 125회 사용과 의미가 겹친다(`dt` §3.6.1 사실). (b) `--muted`/`--accent`/`--radius`를 shadcn 의미로 예약하면 airport main 별칭과 충돌(WIP가 이미 겪음, `inv/airport` §3.2). (c) `kt-contrast`를 즉시 실패로 켜면 geo·concierge·ktdm·airport의 control-line이 3:1 미달(`dt` §3.4.2 사실)이라 채택 첫날 CI red. (d) `@custom-variant dark`를 패키지가 기본 발행하면 다크 값을 검증한 적 없는 앱(weather·concierge·map 모두 토글 없음, `dt` §3.2.2)에서 OS 다크 설정 사용자에게 미검증 팔레트가 노출된다.
- 결정(후보):
  1. 접두 `--kt-*`(전 저장소 0회). 계층 = semantic ← app override 2단(primitive ramp 강제 없음 — 어느 앱도 ramp 기반이 아님, `dt` §3.6.2). shadcn alias(`shadcn.css`)는 이름·의미 고정: `--input`=control-line(3:1 대상), `--accent`=brand-tint, `--radius`=radius-control. airport는 alias 재매핑 30곳을 WIP 그대로 유지(D-08 ①).
  2. 프로필: `admin`(6/8px, 36/30px, 15px, 7단 12/13.5/15/17/20/24/30) · `consumer`(8/14/20/32, 44px, 16px). 타입 스케일은 `@theme`(비inline)로 정의해 `[data-kt-surface]` 변수 가리기가 동작하게 한다(`dt` §3.6.5 사실).
  3. 오버라이드 허용 목록(계약): brand 4 + focus + paper 4 + ink 4(hue만). status 4+tint는 기본값 유지 권장(map·weather 동일값). 형태·높이·타입·모션은 프로필로만.
  4. 다크: `tokens.css`는 `.dark` 값을 **반드시** 포함(map 기본값). 활성화 파일(`dark-class.css`/`dark-media.css`)은 **앱이 명시적으로 import**할 때만 적용; 기본 `color-scheme: light`. airport(media 전용)는 `dark-media.css`.
  5. `kt-contrast`: 검사 쌍은 `dt` §3.4.2 표(control-line/page·card·muted 3:1, text-secondary·tertiary/page 4.5:1, focus/page 3:1, brand fill+foreground 4.5:1, light·dark 동일 쌍). **모드 = report 기본**, 앱별 `contrast-baseline.json`(현재 미달 쌍 목록 + `until`)을 두고, 미달 쌍이 새로 늘어날 때만 fail. 값 재조정(T-14x)은 별도 task.
  6. 마커 팔레트 P-01~16: common 소유 아님(D-26).
- 대안(기각): `--ktc-` 승격(실패 (a)), 다크 기본 활성(실패 (d)), contrast 즉시 fail(실패 (c)).
- 근거: `dt` §3.1~§3.6·§5-1·5·6; `inv/airport` §3.2·§8-2; `inv/pinvi` §3.1·§8-4; `ux` C14.
- 소비자 영향: map: 값 무변경(원형) · weather: `tokens.css` 교체만 · geo·concierge·ktdm·airport: contrast 미달 baseline 등록 후 값 재조정 task · pinvi admin: `--color-admin-*` → `--kt-*` 매핑표 · pinvi user/mobile: `tokens.json`만.
- 열림: 접두 최종 확정(§F-6, 기본 `--kt-`), 다크 토글 도입 계획(§F-7).

### D-13 UX 가이드·PC/Mobile 규약 — 채택 범위와 충돌 해결(C1~C22)

- 실패 시나리오: 규칙을 "코드 게이트"로 즉시 바꾸면 `window.confirm` 잔존(map 2·ktdm 3·kta·weather), 44px 예외 페이지(pinvi 2), drawer(geo)가 첫 채택 PR에서 전부 위반이 된다. 반대로 문서만 두면 map 금지 패턴 7종처럼 스크립트가 없어 지켜지지 않는다(`dt` §3.4.1 미확인).
- 결정(후보): `ux` §2 G0~G9를 `docs/standards/ux-guide.md`(admin 장 / 사용자 표면 장 분리), §3을 `docs/standards/responsive-web.md`로 채택. 규칙 ID는 common이 `UX-Gn.m`로 새로 발급하고 앱 M/C 번호는 출처로만 인용(`ux` Q9). 게이트화는 **grep 스크립트 `tools/ux_lint.py` report 모드**부터(금지 패턴 7종 + `window.confirm`), 앱별 baseline 허용 목록 → fail 승격(R3). 표면 분류: admin = PC-first + ≥320px 컨테인, 사용자 웹 = mobile-first, breakpoint sm640/md768/lg1024/xl1280, 검사 폭 320/375/414/768/1024/1440, 터치 admin 36/30(히트 ≥24) · 사용자 44 · 모바일 48. 충돌 해결:

| # | 결정 한 줄 |
|---|---|
| C1 | 접힌 rail 4rem이 admin 규약. pinvi 5rem은 "터치 admin 변형"으로 **예외 등록**(36px 행으로 낮추는 변경은 pinvi 결정) |
| C2 | weather 17rem·접힘 없음은 common 셸 채택 시 자연 해소; 그 전까지 weather 문서를 코드에 맞춰 정정(코드 변경 없음) |
| C3 | 셸 전환 1024(lg) 통일. weather 62rem은 셸 교체 시, kta 860은 콘텐츠 breakpoint로 잔존 허용 |
| C4 | strip 기본 + drawer 허용(둘 다 G4.8 a11y 요구 충족 시). common 셸 골격은 strip만 1차, drawer는 geo 참조 구현으로 문서 |
| C5 | admin 활성 nav = tint + 2px mark + `aria-current`. pinvi ink 채움은 예외 등록(색 외 형태 mark 추가 권고) |
| C6 | 표면별 분리(36/30 · 44 · 48). pinvi admin 44px 2페이지는 "터치 검토 화면" 예외로 등록, e2e 유지 |
| C7 | 동사 라벨 필수·기본 라벨 없음·`window.confirm` 금지 — **신규 코드 MUST, 기존 잔존은 baseline 목록**(map 2·ktdm 3·kta 1·weather 1) |
| C8 | 성공은 조용히(G4.1) 정책만 통일, 토스트 엔진은 앱 선택. common 컴포넌트(CopyButton 등)는 inline 피드백 기본 + `onNotify` 주입 |
| C9 | 5-tone 이름·의미 채택. geo CANCELLED→neutral 매핑은 도메인 확인 전 **변경하지 않음**(`ux` Q1). ktdm은 alias 표, kta는 도메인 레벨→tone 매핑표 |
| C10 | "페이징 목록 = 서버 정렬"은 규칙; 코드는 `sortMode` 필수 prop(D-09)로 강제. pinvi 페이지별 전환 목록은 pinvi task |
| C11 | admin·사용자 웹 좌정렬. 모바일 앱 가운데 허용 |
| C12 | 한글 본문 1순위 Pretendard Variable 스택은 common 제공, **로딩은 앱 책임**(weather Geist 1순위는 정정 권고) |
| C13 | admin 15px/12px 하한. ktdm 14px·11px, kta 11px은 baseline 등록 후 정렬 |
| C14 | admin 기본 light. `.dark` 슬롯 필수, 활성화 opt-in(D-12) |
| C15 | 로그인 = 타이포 워드마크(G7.1). geo·weather 아이콘 타일은 후속 정렬(LoginForm은 common 범위 밖이므로 문서 권고만) |
| C16 | pinvi `AdminPage`→`AdminPageHeader` 수렴, weather pathname 표시→breadcrumb: 앱 task |
| C17 | HelpTip popover-only 허용 하위집합, 히트 ≥24px만 필수 |
| C18 | 모달 엔진 앱 소유; G4.8 행동 계약 + "두 모달 스택 금지"만 규약 |
| C19 | `AppErrorPanel` 계보(5앱 동일)를 ui 1차 후보에 포함(Alert/Button 이후), weather·kta 도입 |
| C20 | 접근성 이름 = 라벨만, 운영 정보는 `data-*`(pinvi `(Sprint N)` 정정) |
| C21 | Hallmark 스탬프: **인용 금지**(B3), 형식·위치(SPDX 헤더 다음 줄)만 규약. 이식 파일은 출처 앱 스탬프 제거 후 common 스탬프 |
| C22 | 지도 스타일 빌더 배포 경로는 common 범위 밖(D-23) |

- 대안(기각): 규칙 즉시 게이트화(첫날 red), 문서만(미준수).
- 근거: `ux` §1.1~§1.13·§2·§3·§4·§5; `dt` §3.4.1; `inv/pinvi` §8-6·23; `inv/ktdm` §8-21.
- 소비자 영향: 신규 코드 MUST만 즉시, 기존은 baseline. pinvi 예외 3건(C1·C5·C6) 등록.
- 열림: dirty 이탈 경고(§F-11), pinvi 44px 예외 영구화 여부(§F-12).

---

## C. 백엔드·API

### D-14 OpenAPI/REST 규약 채택(MUST/SHOULD/MUST NOT)과 예외 레지스트리

- 실패 시나리오: (a) M3(problem+json)를 기존 표면에 MUST로 걸면 pinvi `{error:{}}`(Zod·모바일까지 고정), concierge `{detail}`(map provider가 소비하는 외부 계약 `/api/v1/features/*`), geo v1(VWorld 호환)이 동시에 breaking(`oa` §4 사실). (b) M5 health 경로를 바꾸면 geo `/v1/healthz`를 ktdm healthcheck·Prometheus가 참조(`be` §2.5, `ci` §1.13)해 probe가 unhealthy. (c) M8 securitySchemes 선언은 geo typegen 산출물을 바꿔 CI drift가 난다(`oa` C5). (d) map 산출물이 바뀌면 pinvi·ktdm의 sha256 pin이 깨진다(`oa` §4 map 행, B10).
- 결정(후보): `oa` §3의 M1~M9/S1~S13/N1~N8을 `docs/standards/openapi.md`로 채택하되 **적용 범위를 3계층**으로 나눈다:
  - **즉시 MUST(additive, 기존 표면 포함)**: M1(산출물 커밋 + `--check`), M2(`servers` 없음), M4(`X-Request-ID`; 형식 검증 후 echo, `trust_incoming=False` 옵션), M9(운영 표면만 export), N6·N7. — 응답 본문을 바꾸지 않는다.
  - **신규 표면 MUST / 기존 표면 SHOULD + 예외 등록**: M3(problem+json+`code`+`request_id`), M5(`/health`·`/readyz`·`/version`; 기존 경로는 **별칭 병행 2 릴리스**), M6(lon/lat), M7(aware datetime), M8(securitySchemes — geo는 typegen 재생성 task와 묶음), N1~N5·N8.
  - **SHOULD 전체**(S1~S13): 규칙 문서 + 코드 후보. S2 이름은 `page_size`+`next_cursor`(null=끝), `has_more`는 additive 옵션. S7 429 코드는 `TOO_MANY_REQUESTS`(map) 채택, 상태→코드 사전은 common 소유·앱 덮어쓰기 허용. 검증 오류 422 기본, geo 400 예외.
  - 예외 레지스트리 `docs/standards/openapi-exceptions.yaml`: `{app, rule, surface, reason, sunset|null, owner}`. 초기 등록: geo v1(M3·M6·N2·N5, sunset 없음/VWorld 호환), geo v2(M3 — ADR-060 breaking 묶음 시점), geo 400(Q2), pinvi(M3·M5 prefix·S5 정수 If-Match/409 — v2 prefix 시점), concierge(`/api/v1`·`{detail}`·features export envelope — map provider 동시 수정 전), ktdm(`/api/v1`·`{detail}`), airport(envelope 없음 ADR-005), map(`type` URI 접두·starlette 상한).
  - 헤더 이름: **형식 규칙만** 공통(`X-<AppId>-Api-Key|Service-Token|Actor|Admin-Proxy-Secret|Ops-Token|Ops-Scope`), AppId(풀네임 vs 약어)는 저장소 identity 표 소유. 메트릭 접두는 D-22.
- 대안(기각): 전 규칙 MUST 일괄(실패 (a)~(d)), 규칙 문서만(sha256 pin 비용이 이미 발생 — `oa` §3.5).
- 근거: `oa` §2.5·§2.6·§2.10·§2.11·§3·§4·§5·§6 Q1~Q11; `be` §2.5·§2.10; `inv/map` §8-16·18.
- 소비자 영향: map: 거의 무변경, 산출물 변경 시 pinvi/ktdm pin 갱신 동반 · weather: `code` 사전·`type`만(낮음) · airport: `code`/`request_id` additive + CI drift 신설 · geo: v2/admin opt-in, health 별칭 · pinvi: export 파이프라인 신설이 전부(본문 무변경) · concierge·ktdm: export·request-id만.
- 열림: 429 코드명(§F-13, 기본 `TOO_MANY_REQUESTS`), geo v2 envelope의 problem+json 채택 시점(§F-13).

### D-15 Python 공통 모듈 우선순위

- 실패 시나리오: (a) `[api]` extra가 fastapi/starlette를 import하는 모듈을 core에 섞으면 geo·map import-linter forbidden 계약(`be` §3 전제)에 걸린다. (b) 메트릭 이름을 바꾸면 map·pinvi 대시보드·alert가 조용히 끊긴다(`be` §7-4, 영향 범위 미확인). (c) C20 ruff 프리셋을 그대로 적용하면 airport·concierge(설정 0)에서 대량 위반, ktdm은 `ruff format` 전체 실행 금지(`inv/ktdm` §4.1). (d) C5 errors 핸들러를 opt-out 없이 넣으면 geo v1 경로가 깨진다.
- 결정(후보): 배포 이름 `kor-travel-common`, import `kortravelcommon`, **core는 stdlib+pydantic만**. 순서:
  - 1차(계약 무변경·근거 강): C12 `openapi.export`(`--check`, profile 콜백, 결정적 직렬화), C4 `health`(라우터 팩토리; 기존 경로 alias 옵션), C13 `time`(`KST=ZoneInfo`, `kst_now/utc_now`, aware 검증; ktdm naive·weather 고정 오프셋은 앱 명시 결정), C20 `quality`(ruff `extend` 베이스 `line-length=100`·`E,F,I,UP,B,ASYNC`; mypy strict 베이스; **format 규칙은 미포함**; 앱별 `per-file-ignores` baseline 허용).
  - 2차: C1 `settings` 베이스(접두는 앱 인자, env 이름 불변), C9 `db`(asyncpg/psycopg 흡수, sync는 별도 함수), C7 `auth.public_api_key`(4곳 동일 함수; 저장소 Protocol), C2 `request_id` 미들웨어(+`trust_incoming`), C3 `metrics` **표준 라벨·센티널·multiproc만** — 접두는 인자, 이름 변경 강제 없음.
  - 3차: C5 `errors`(problem+json 핸들러, `exclude_paths` 옵션으로 geo v1 제외), C16 security_headers(HSTS 기본 = 전달 헤더 **불신**, pinvi #344), C17 cors csv, C8 trusted_proxy 원시 함수, C11 testing(testcontainers·DSN 두 계열), C10 alembic 템플릿, C15 http, C18 dagster.
  - 보류: C6 pagination 코덱, C14 geo_primitives(경계 상수 공통화 **금지**), C19 cli.mutex, C21 backup spec(문서만).
  - 범위 밖 고정: 비밀번호·세션·CSRF·JWT·RBAC, 서비스 간 클라이언트, provider 재래핑(`be` §4).
- 대안(기각): C5를 1차로(실패 (d)), 접두 통일을 코드로 강제(실패 (b)).
- 근거: `be` §2.19·§3·§4·§5.3·§7; `oa` §5 C1~C7; `inv/geo` §8-23·§9.
- 소비자 영향: map-api·weather-api·airport: 1차 교체(낮음) · geo: health alias·admin opt-in · pinvi·concierge·ktdm: export·request-id·quality baseline부터 · concierge: pyproject·uv 도입 선행(T-485).
- 열림: Python floor 상향 여부(§F-8, 기본: common 3.11 호환 유지), 메트릭 접두 이관 시점(§F-13).

### D-16 소비자 첫 대상과 순서(권리·계약 gate 반영)

- 실패 시나리오: map+pinvi admin을 첫 공동 소비자로 잡으면(`prior` §1) pinvi는 B1(라이선스 미결)과 B9(GPL common 링크)에 걸려 **첫 소비자 PR을 열 수 없다**(`lic` §3.6·§4). concierge·ktdm(MIT)도 L8 결정 전 코드 링크 불가. 결과: 1차 소비자가 map 하나가 되어 "두 앱 동일 의미" 검증(`prior` 착수 조건)이 성립하지 않는다.
- 결정(후보):
  - tokens 1차 = **map + weather + airport(WIP)** — 셋 다 GPL, weather는 순수 CSS라 `tokens.css` 교체만으로 채택 가능(`inv/weather` §8-1), airport는 WIP 브릿지가 참조 구현(`inv/airport` §8-2). 2차 = geo·ktdm(React 무관), pinvi admin(L6 후), concierge(L8 후).
  - ui 1차 = **map + airport**(둘 다 GPL, React 19). airport 범위는 백업 패널·collector 패널이 쓰는 소형 부품(Alert·StatStrip·SectionCard·EmptyState·Button)이며 AdminShell/LoginForm 소비는 T-035 라우트 분리 이후(D-20). 2차 = pinvi admin(L6), concierge(L8), geo(React 19 + base-ui 이관 후). ktdm은 Next/React 업그레이드 후.
  - Python 1차 = map-api·weather-api·airport(문제+json 근접, GPL). 2차 = geo v2/admin. 3차 = pinvi·concierge·ktdm(라이선스 결정 후, breaking은 v2 prefix 묶음).
  - "두 소비자 검증" 조건은 tokens: map↔weather, ui: map↔airport로 충족한다.
- 대안(기각): map+pinvi admin 1차(실패 시나리오), 전 앱 동시(R2 위반).
- 근거: `lic` §3.6·§4 B1·B9·L6·L8; `ui` §4; `oa` §4; `inv/airport` §1·§9; `inv/weather` §8; `prior` §1·§10.
- 소비자 영향: pinvi: L6 결정이 곧 착수 조건(기본값 §F-1) · concierge·ktdm: L8 결정 전 규칙 문서·`tokens.json`(값 참조)만.
- 열림: §F-1(pinvi 공개/라이선스), §F-2(ktc·ktdm GPL 정렬 vs §7 예외).

---

## D. 라이선스·운영

### D-17 라이선스·출처 조치(licensing.md 반영)

- 실패 시나리오: (a) pinvi 파일을 옮기면 권리 유보 코드가 GPL 저장소에 섞인다(B1). (b) shadcn 생성물(MIT)·cva(Apache-2.0, MIT 아님 — `lic` §2.4 사실)·pretendard(OFL) 고지 없이 tarball을 배포하면 §4 위반. (c) geo `-only` 파일을 `-or-later`로 표기하면 권리자 재선언 없이는 오표기. (d) kta·common `LICENSE`가 버전 미고지면 수령자가 임의 버전 선택(GPLv3 §14).
- 결정(후보): common = **GPL-3.0-or-later**(`LICENSE` 유지 + `NOTICE`에 저작권자·버전·연락처). 파일별 SPDX 헤더 + `Origin/Derived-From/Modified` 3행, Hallmark 스탬프는 그 다음 줄(`lic` §3.4). `THIRD_PARTY_NOTICES.md` + `LICENSES/`(MIT·Apache-2.0·OFL-1.1·BSD-3·ISC 원문), `PROVENANCE.md`(`lic` §2.3 표 형식; 이동 파일마다 원천 커밋·경로·라이선스). 추출 규칙: GPL 원천(geo/map/weather/airport)은 그대로(geo는 재선언 전 `GPL-3.0-only` 표기), MIT 원천(ktc/ktdm)은 MIT 고지 보존, **pinvi는 L6 완료까지 추출 금지**, 벤더 tgz·maplibre-vworld-react는 영구 금지(B2), Hallmark 본문 인용 금지(B3), ktc AppShell/globals는 diff로 복사 여부 확정 후(B4). 봇 커밋분은 `CONTRIBUTING.md`에 "AI 보조 생성물은 지시자가 GPL로 배포" 명시(B8). 소비 앱 정렬 권고 = ktc·ktdm·pinvi를 `GPL-3.0-or-later`로(§7 추가 허가 방식은 파일마다 예외 문구를 유지·검증해야 해 기각). 린트: `tools/check_spdx.py`(헤더 부재 = fail, Phase 1부터 — common 자체 파일이라 baseline 불필요).
- 대안(기각): §7 추가 허가로 MIT 앱 링크 허용(유지 비용·"GPL common" 전제와 불일치), pinvi 추출 선행(B1).
- 근거: `lic` §2.2 D1~D10·§2.4·§3.1~§3.7·§4·§6; `cm` §4.1 B1~B10.
- 소비자 영향: map: `LICENSE` 전문 복원(L9) · geo: `-only`→`-or-later` 재선언 여부(L10) · ktc·ktdm: 루트 라이선스 결정(L8) · pinvi: README/AGENTS 상충 해소 + LICENSE(L6) · weather: airkorea 스냅샷 정본 결정(L15) · 전 앱: `license` 메타데이터 필드(L11).
- 열림: §F-1, §F-2, geo `-only`(§F-2).

### D-18 CI·릴리스·포트/서비스명 규약(ci-deploy.md 반영)

- 실패 시나리오: (a) 재사용 워크플로를 `@main`으로 참조하면 common 변경이 7개 CI를 동시에 깨뜨린다. (b) required check 이름이 바뀌면 map(8개)·pinvi(aggregate 5개) ruleset이 `Expected`에 갇힌다(`ci` §2.3). (c) kta `live-e2e`처럼 운영을 호출하는 job이 required면 서버 다운 시 PR이 막힌다. (d) 포트 정본을 common으로 옮기면 ktdm `docs/ports.md`와 이원화된다.
- 결정(후보):
  - common 자체 CI: `docs`(link·plan·unittest·`git diff --check`·redaction 전체 트리), `packages`(lint·type·test·build·`npm pack`→tarball 설치 스모크, webpack/Turbopack 양쪽), `python-package`(`uv build`·wheel 설치·starlette 0.4x/1.6 매트릭스), `consumer-smoke`(`workflow_dispatch`+주간; `consumers.pins.json`으로 map·weather·airport pinned SHA 체크아웃 → 설치 → `type-check`+`next build`), `secret-scan`, `check-versions`(report). 하드닝: `permissions: contents: read`, `concurrency`, `timeout-minutes`, `ubuntu-24.04`, head SHA checkout, 액션 SHA 핀. branch protection: PR 필수 + required `docs`·`packages` + linear history + force-push 차단.
  - 재사용 워크플로(`workflow_call`): `python-quality`, `node-quality`, `openapi-drift`, `docs-check`, `secret-scan`, `docker-build`, `aggregate-gate` — 소비자는 **태그/SHA로만** 참조, job `name:`은 입력으로 개방(required check 이름 보전). 운영 호출 job은 required 금지(kta는 `workflow_dispatch`/스케줄로 분리 권고).
  - 릴리스: 패키지별 태그, `CHANGELOG.md` `[Unreleased]`→버전 절, 시험 버전(`-rc.N`)을 소비자 PR에서 검증한 뒤 정식, 같은 버전 덮어쓰기 금지, 회귀 시 소비자는 직전 버전+lock으로 되돌림.
  - 포트/이름: 정본은 ktdm `docs/ports.md` 유지(인용만). common 대역 `130xx`(13001 smoke API, 13005 showcase) — 미사용 여부 미확인이라 T-0xx에서 로컬 점유 확인 후 확정. sibling 등록(`140xx` airport, `141xx` weather) 요청은 ktdm task. 서비스명 어휘(`postgres/api/web/dagster/…`), 컨테이너 `<project>-<role>`(`-latest` 제거는 ktdm registry 결박이라 열림), 이미지 tag 어휘, env 접두 단일화 규칙, Dockerfile 최소 규약(멀티스테이지·non-root·digest·OCI revision·HEALTHCHECK 1곳)은 `docs/standards/ci-deploy.md`.
- 대안(기각): 워크플로 파일 복사 배포(`prior` §7.2·`ci` §1.15 — 폭 조절 불가), 포트 정본 이관(이원화).
- 근거: `ci` §1.1~§1.3·§1.9·§2.1~§2.3·§3·§4·열린 질문 1·3·4·10; `cv` §1.3.
- 소비자 영향: concierge: CI 신설(제로 베이스) · kta: redaction 전 placeholder 치환 17/26 파일 · map·pinvi: job 이름 입력으로 ruleset 보전 · ktdm: SHA 핀 관행 유지.
- 열림: airport 14002 예외 vs 14005(§F-15), `-latest` 접미(§F-15), redaction 적용 범위(§F-16).

---

## E-0. 초안에 없던 추가 결정(D-19 이후)

### D-19 pinvi 사용자 표면·모바일의 취급
- 실패 시나리오: consumer 프로필 값(44px, Rausch)을 common이 소유하면 pinvi `@pinvi/design-tokens` 이중 정본(`prior` §3.5).
- 결정: 사용자 웹·모바일은 **코드 소비 대상 아님**. common은 `consumer` 프로필의 규칙(밀도·breakpoint·터치)과 `tokens.json`(DTCG, 의미 이름만)을 제공하고 값 정본은 pinvi가 유지. 모바일은 정렬 정책 `exceptions`(Tailwind 3, RN 정확 핀) 등록. 근거: `dt` §3.6.5·§3.6.7·§5-7; `ux` §3.1; `inv/pinvi` §3.2·§9. 열림: §F-12.

### D-20 "kor-travel-airport Admin"의 정의
- 실패 시나리오: 존재하지 않는 admin 앱을 전제로 AdminShell/LoginForm 소비 task를 만들면 착수 불가.
- 결정: 현 시점의 airport Admin = 무인증 백업 패널 + collector 상태 패널 + `/v1/admin/*`(ADR-003 의도, `inv/airport` §1-4 사실). 1차 채택 범위는 tokens + 소형 부품. 라우트 분리(T-035)·인증 도입은 airport 결정이며 common은 셸 소비 task를 그 이후 BLOCKED로 둔다. 근거: `inv/airport` §1·§9·§11-9; `ux` Q5. 열림: §F-9.

### D-21 시각 회귀 기준선 의무
- 실패 시나리오: Tailwind 전환·토큰 교체 후 "픽셀 동일" 주장이 재현 불가(airport WIP 커밋 메시지, `inv/airport` §3.2 미확인).
- 결정: 토큰·스타일·셸을 바꾸는 모든 소비자 PR은 착수 전 6폭(320/375/414/768/1024/1440) 스크린샷 기준선을 `docs/reports/`(앱) 또는 PR 자산으로 남기고, 완료 evidence에 diff 결과를 첨부. Playwright 없는 앱(weather·ktdm)은 common의 `templates/playwright.baseline.ts`를 임시 사용. 근거: `ux` §1.11 e2e 뷰포트 표; `inv/weather` §9.1; R5.

### D-22 헤더·메트릭 접두 명명
- 실패 시나리오: map `kor_travel_map_`·pinvi `pinvi_api_`를 `kt<x>_`로 바꾸면 대시보드·alert 회귀(범위 미확인, `be` §7-4).
- 결정: **신규 서비스만** `kt<x>_`(geo·ktc·ktdm·ktw 선례). 기존 접두는 예외 등록, 변경은 대시보드 영향 평가 task 후 앱 결정. 헤더 접두도 형식 규칙만(D-14). 근거: `be` §2.4·§7-4; `inv/geo` §9; `inv/map` §9.

### D-23 기존 공유 라이브러리 배포 정책(common 범위 밖, 계획에는 포함)
- 실패 시나리오: `maplibre-vworld-react`(npm 미발행) 때문에 weather 로컬 재구현·pinvi tgz·geo tarball·map 포팅 4경로가 계속 갈라진다(`ux` §1.10); `python-airkorea-api` 벤더 스냅샷(weather)과 git+sha(map) 이중 경로; kma SHA 불일치.
- 결정: common은 지도·provider 코드를 갖지 않는다. 통합 계획에 "공유 라이브러리 배포 경로 정리" task(T-5xx)를 두고 `versions.json` `providers` 절에 SHA를 **보고**한다. 근거: `be` §5.1·§7-13; `lic` L7·L15; `dt` §3.5.

### D-24 소비자 채택 PR의 되돌리기 규칙
- 결정: 채택 PR은 (1) 프레임워크 업그레이드와 분리, (2) 단일 revert로 원복 가능, (3) lockfile·버전을 함께 커밋, (4) PR 본문에 회귀 시 되돌리기 명령을 명시. `docs/runbooks/consumer-adoption.md`에 절차 고정. 근거: `prior` §5·§8; R2.

### D-25 검증 불가 gate의 표기
- 결정: 브라우저 렌더·소비자 e2e·registry 권한처럼 common에서 실행 못 하는 검증은 task `evidence`에 `NOT_RUN(사유)`로 남기고 DONE 전 `외부 선행`으로 승격. 0 test/skip을 pass로 집계 금지. 근거: `cv` R1.12·R1.13; canview A2.5.

### D-26 마커 팔레트 P-01~P-16 소유
- 결정: common 소유 아님. 16슬롯·라벨 대비 규칙만 `ux-guide`에, hex 정본은 map(`marker_color` 소유자)이 확정하고 pinvi가 재수출. 계획에는 map task로 기록(common 소속 task 아님). 근거: `dt` §3.5·§5-2.

### D-27 `docs/decisions.md`·문서 도구 언어·링크 규칙
- 결정: `decisions.md` 미보유(단일 색인 `adr/README.md`), 도구는 Python 유지(`python3`/`uv run` 표기; 소비자 7곳 전부 Python 보유), 링크는 저장소 상대만(절대 접두 = 오류). `documentation-maintenance.md`·`validate_document_links.py` 정정은 T-002. 근거: `cv` Q1·Q2·Q5; `dc` C11·C12·Q5.

---

## E. 통합 계획 초안(Phase 0~5)

원칙: 각 Phase는 **중단 조건**을 만족하면 다음 Phase의 소비자 확대를 멈추고 common 내부 task로 되돌아온다. 소비자 PR은 항상 "프레임워크 업그레이드 PR → 채택 PR" 순서이며 둘을 한 PR에 묶지 않는다(R2). 검증 못 한 것은 NOT_RUN으로 남긴다(R5).

| Phase | 목표 | 산출물 | 완료 기준 | 중단 조건 |
|---|---|---|---|---|
| 0 골격·규칙·gate (현재 PR~) | common 저장소가 canview 계층으로 자기 검증을 통과하고, 권리·버전·규칙의 정본 파일이 존재 | `AGENTS/CLAUDE/SKILL/README`, `docs/README`, ADR-001~006, `docs/tasks.md`+상세, `NOTICE`·`THIRD_PARTY_NOTICES`·`LICENSES/`·`PROVENANCE`, `versions.json`+`check_versions.py`(report), `docs/standards/{agent-conventions,versions}.md`, runbook 4종, common CI 하드닝 | `docs.yml`·`validate_plan`·`validate_document_links` green; 7 소비자 현재값이 registry에 등록되고 report 산출; ADR 6건 accepted; T-006 scope 확인 결과 기록 | npm scope 확보 실패 → 개명 후 재진행(비용 0) |
| 1 tokens + 첫 소비자 | 값 무변경 토큰 패키지가 GPL 소비자 3곳(map·weather·airport)에서 시각 diff 0으로 채택 | `packages/tokens` v0.1.0, `kt-contrast`(report)+baseline 형식, `design-tokens.md`·`ux-guide.md`·`responsive-web.md`, 시각 기준선 템플릿, 재사용 워크플로 5종, consumer-smoke | map·weather·airport 채택 PR 머지 + 6폭 스크린샷 diff 0 + 각 CI green; `check_versions` report가 3곳 CI에 삽입 | 어느 한 곳이라도 시각 diff가 원인 불명으로 남으면 tokens v0.1.x 패치로 되돌리고 확대 중단 |
| 2 ui 1차·2차 | 계약이 이미 같은 소형 부품 → Button/overlay/Table/DataTable 순으로 map·airport에서 채택 | `packages/ui` v0.1.0(소형)·v0.2.0(2차), `ui-contract.md`, base-ui 사실 확인 기록, showcase 없음(스모크는 consumer-smoke) | map e2e 30 spec·airport frontend CI green; pinvi e2e testid 계약이 DataTable 계약 문서에 반영(pinvi 채택 전) | 소비자 우회 패치가 2회 이상 반복되면 해당 컴포넌트를 앱 잔류로 되돌림(`prior` §10 1단계 중단 조건) |
| 3 Python 1차 + OpenAPI 규약 | 계약 무변경 모듈(export·health·time·quality)이 map-api·weather-api·airport에서 교체 | `kor-travel-common` py-v0.1.0, `openapi.md` + `openapi-exceptions.yaml`, `backend-stack.md`, request-id·metrics 2차 | 3곳 openapi drift CI green; map 산출물 무변경(pinvi/ktdm pin 그대로) 또는 pin 갱신 PR 동반; starlette 0.4x/1.6 매트릭스 green | map 산출물 변경이 pinvi pin 갱신 없이 머지되면 rollback |
| 4 앱별 정렬·전환 | 라이선스·React·lock 게이트가 풀린 앱부터 v4 정리·업그레이드·채택 | geo(React 19·base-ui·@config), concierge(pyproject·CI·@config·L8), pinvi(L6·admin 매핑·export), weather(v4 4단), ktdm(Next/React/uv/tokens), py 2·3차 | 각 앱 `check_versions` 위반 0(예외 등록분 제외); 시각 diff 0; e2e green | L6/L8 미결이면 pinvi·concierge·ktdm은 규칙 문서·tokens.json 참조까지만 |
| 5 운영·승격·회수 | gate 승격, 릴리스 운영 정착, 보류 항목 재평가 | fail 승격 PR, dependabot 템플릿, 분기 drift 감사, 공유 lib 정리 제안, 회수 측정, 공개 게시 재평가 | 소비자별 report 2회 연속 0 위반 후 fail 승격; 3개월 회수 지표 보고 | 순절감 ≤0이면 공유 범위 축소(`prior` §11) |

### E.1 상세 task 목록(79개; ID는 `docs/tasks-rule.md` §2 대역, 형식 `ID | 제목 | 선행 | 우선순위 | Gate | 대상`)

**Phase 0 — T-0xx (저장소 기반·규칙·도구·CI). 첫 5개(T-001~T-005)는 선행 없음, 이 저장소에서 즉시 시작.**

| ID | 제목 | 선행 | 우선순위 | Gate | 대상 |
|---|---|---|---|---|---|
| T-001 | `AGENTS.md`(공통 절 A~I + 로컬 경계 절)·`CLAUDE.md`(≤40줄 포인터)·`SKILL.md`(라우터)·`README.md`·`docs/README.md` 작성 | 없음 | P0 | 문서 검증 | common |
| T-002 | `docs/tasks.md`+상세 task 초기화, `docs.yml` 링크 17건 해소, `documentation-maintenance.md`의 `decisions.md` 문구 정정, `validate_document_links.py` 절대 접두 제거, `.py` CRLF→LF 확인 | 없음 | P0 | 문서 검증·CI | common |
| T-003 | `NOTICE`·`THIRD_PARTY_NOTICES.md`·`LICENSES/`·`PROVENANCE.md` 골격·`CONTRIBUTING.md`(B8)·`tools/check_spdx.py`·SPDX 헤더 규약 | 없음 | P0 | 문서 검증·도구 테스트 | common |
| T-004 | ADR-001~006 초안(배포 단위 D-01, 라이선스 D-17, 개발 환경 D-03, 원장 형식 D-05, 리뷰 gate D-04, 배포 채널 D-11) + `docs/adr/README.md` 단일 색인 | 없음 | P0 | 2인 리뷰 | common |
| T-005 | `versions.json` v1 스키마 + `tools/check_versions.py`(report 모드, 판정 8종) + 7 소비자 현재값·예외 등록 + `docs/standards/versions.md` | 없음 | P0 | 도구 테스트·문서 검증 | common |
| T-006 | npm scope(`@kor-travel`)·PyPI 이름 가용성 확인·확보(사용자 계정 작업; 실패 시 D-01 이름 개명) | 없음 | P1 | 외부 확인 | 외부(npm/PyPI) |
| T-007 | runbook: `agent-workflow.md`·`consumer-adoption.md`(D-24)·`release.md`·`dev-environment.md` + `docs/standards/agent-conventions.md` + `templates/agent-config/` | T-001 | P1 | 문서 검증 | common |
| T-008 | `docs/architecture/{README,packages,consumers,adoption-readiness}.md` + `docs/integration-map.md`(소비자 7 기준 커밋·채택 상태) | T-004, T-005 | P1 | 문서 검증 | common |
| T-009 | common CI 하드닝(`permissions`·`concurrency`·`timeout`·`ubuntu-24.04`·액션 SHA 핀) + `secret-scan`·`check-versions(report)` job + branch protection 문서 | T-002, T-005 | P1 | CI | common |
| T-010 | 재사용 워크플로 5종(`python-quality`·`node-quality`·`openapi-drift`·`docs-check`·`secret-scan`) + `workflows-selftest` fixture + `consumers.pins.json`·`consumer-smoke` | T-009 | P1 | workflows-selftest | common |
| T-014 | common 포트 `130xx` 로컬 점유 확인·확정 + ktdm `docs/ports.md` sibling(airport 140xx·weather 141xx·common 130xx) 등록 요청 + `-latest` 접미 질의 | 없음 | P3 | 외부 확인 | common/ktdm |

**Phase 1 — T-1xx (tokens·UX 규약) + 첫 소비자**

| ID | 제목 | 선행 | 우선순위 | Gate | 대상 |
|---|---|---|---|---|---|
| T-101 | `packages/tokens`: `tokens.css`(map 값+`.dark`)·`theme.css`·`shadcn.css`·`base.css`·`base.scoped.css`·`dark-class/media.css` + `tokens.json`/`tokens.js`/`tailwind-preset.cjs` 생성기(정본=tokens.css) + `npm pack` 설치 스모크 | T-003, T-004 | P0 | 패키지 빌드·tarball 설치 | common |
| T-103 | `tools/kt_contrast.py`(report + `contrast-baseline.json` 형식) + `tools/ux_lint.py`(금지 패턴 7종+`window.confirm`, report) + 4앱 오버라이드 예제로 보고 | T-101 | P1 | 도구 테스트 | common |
| T-104 | `docs/standards/design-tokens.md`(접두·계층·프로필·오버라이드 허용 목록·다크·대비·shadcn alias 의미) | T-101 | P0 | 2인 리뷰 | common |
| T-105 | `docs/standards/ux-guide.md`(G0~G9, `UX-Gn.m` ID, C1~C22 판정표, 예외 레지스트리, Hallmark 인용 금지) | T-007 | P1 | 2인 리뷰 | common |
| T-106 | `docs/standards/responsive-web.md`(표면 분류·breakpoint·검사 폭·터치·안전영역·overflow) | T-105 | P1 | 2인 리뷰 | common |
| T-108 | `templates/playwright.baseline.ts`(6폭 스크린샷) + 기준선 캡처 runbook(D-21) | 없음 | P1 | 도구 테스트 | common |
| T-109 | tokens `v0.1.0-rc.1` → map·weather 검증 → `tokens-v0.1.0` 정식 릴리스 | T-101, T-103, T-104 | P1 | consumer-smoke | common |
| T-402 | 7앱 시각 회귀 기준선 초기 캡처(앱별 evidence; 미실행은 NOT_RUN) | T-108 | P1 | NOT_RUN 허용 | 전 앱 |
| T-403 | 공통 CI 정렬: Node 20→22(dm·geo·weather), 액션 SHA 핀, `check_versions` report job 삽입(7 저장소) | T-010 | P1 | 각 저장소 CI | 전 앱 |
| T-410 | map: `globals.css` → `@import "@kor-travel/tokens"`(값 diff 0 단언) + `LICENSE` 전문 복원(L9)·`license` 필드 | T-109, T-402 | P0 | 소비자 빌드·e2e 30 | map |
| T-430 | airport: WIP `codex/shadcn-ui-foundation` 병합(shadcn·postcss devDeps 이동, `cn`→clsx+tailwind-merge, `tokens.css` 값 유지) | 외부 선행(WIP PR·CI 확인) | P0 | frontend CI(vitest·tsc·build) | airport |
| T-431 | airport: tokens 채택(alias 재매핑 유지, `dark-media.css`) + contrast baseline | T-430, T-109 | P1 | build·320px 게이트 | airport |
| T-460 | weather: 시각 기준선 6폭 캡처 + Next 16·Vitest 4·Node 22 CI + vitest/mypy CI 추가(별도 PR) | T-108 | P0 | ci.yml | weather |
| T-461 | weather: `app/tokens.css` → `@kor-travel/tokens/tokens.css` 교체(순수 CSS, 값 diff 0) | T-460, T-109 | P0 | 스크린샷 diff | weather |

**Phase 2 — T-2xx (React UI 패키지)**

| ID | 제목 | 선행 | 우선순위 | Gate | 대상 |
|---|---|---|---|---|---|
| T-201 | `packages/ui` 골격(ESM·d.ts·subpath exports·`'use client'`·peer react ^19·인라인 아이콘) + base-ui 사실 확인(Button `type`·Checkbox hidden input·Toast API) 기록 + pack 스모크(webpack/Turbopack) | T-101 | P0 | 패키지 빌드·tarball 설치 | common |
| T-203 | ui 1차 소형: Badge·Skeleton·Separator·Card·Alert·Input·Textarea·NativeSelect·Field·EmptyState·SectionCard·FilterBar·StatStrip + 단위 테스트 | T-201 | P0 | 단위 테스트·tarball | common |
| T-204 | `docs/standards/ui-contract.md`(data-slot·testid·heading·sr-only 문구·SemVer 범위·마크업 변경=major) | T-203 | P0 | 2인 리뷰 | common |
| T-205 | Button(D-09 계약)·AppErrorPanel·error-recovery | T-203 | P1 | 단위 테스트 | common |
| T-206 | overlay 세트(Dialog·AlertDialog·Popover·Tooltip·Tabs·Breadcrumb·HelpTip; `hasUnsavedInput`·`viewportProps` 포함) + Table primitive + native Checkbox(`data-slot=checkbox`) | T-205 | P1 | 단위 테스트 | common |
| T-208 | DataTable(`sortMode` 필수·`enableSortingRemoval`·testid·sr-only) + OffsetPager/CursorPager | T-206 | P1 | 단위 테스트·2인 리뷰 | common |
| T-209 | CopyButton·JsonViewer·DetailList(`onNotify` 주입)·StatusBadge(사전 주입형) | T-206 | P2 | 단위 테스트 | common |
| T-210 | AdminPageHeader·AdminSkipLink·AdminRailGrid + FormFieldInput/FormSelect/FormTextArea + form-validation(헤드리스) | T-206 | P2 | 단위 테스트 | common |
| T-212 | ui `v0.1.0`(1차 소형) rc → map·airport 검증 → 정식 | T-203, T-204 | P1 | consumer-smoke | common |
| T-213 | ui `v0.2.0`(Button·overlay·Table·DataTable·Pager) rc → map 검증 → 정식 | T-208, T-209, T-210 | P1 | consumer-smoke·2인 리뷰 | common |
| T-411 | map: ui v0.1 소형 채택 + `@source` 등록 | T-212, T-410 | P1 | 소비자 빌드·e2e 30 | map |
| T-412 | map: ui v0.2 채택(Checkbox 엔진 교체 3파일) + `ux_lint` report 도입 | T-213, T-411 | P1 | e2e 30·vitest 42 | map |
| T-432 | airport: 소형 ui 채택(백업 패널·collector 패널: Alert·StatStrip·SectionCard·EmptyState·Button) | T-212, T-431 | P2 | build·vitest 10 | airport |

**Phase 3 — T-3xx (Python·OpenAPI) + py 1차 소비자**

| ID | 제목 | 선행 | 우선순위 | Gate | 대상 |
|---|---|---|---|---|---|
| T-301 | `docs/standards/openapi.md`(M/S/N 3계층) + `openapi-exceptions.yaml` 초기 등록(geo v1/v2·pinvi·concierge·ktdm·airport·map) + 헤더 형식 규칙 | T-007 | P0 | 2인 리뷰 | common |
| T-302 | `packages/py/kor-travel-common` 골격(extras, 3.11 문법 검사, starlette 0.4x/1.6 CI 매트릭스) + `docs/standards/backend-stack.md` | T-003 | P0 | python-package | common |
| T-303 | C12 openapi export CLI(`--check`·profile 콜백·결정적 직렬화) + typegen 규약(openapi-typescript 7 gen/check 템플릿) | T-302 | P0 | 단위 테스트 | common |
| T-304 | C4 health 라우터(기존 경로 alias 옵션) + C13 time | T-302 | P1 | 단위 테스트 | common |
| T-305 | C20 quality 산출물(ruff `extend` 베이스·mypy 베이스·import-linter·pre-commit·CI 템플릿; format 미포함) + common 자기 적용 | T-302 | P1 | 자기 적용 | common |
| T-306 | C1 settings 베이스 + C9 db + C7 public_api_key | T-304 | P1 | 단위 테스트(testcontainers) | common |
| T-307 | C2 request_id(`trust_incoming`) + C3 metrics(표준 라벨·센티널·multiproc; 접두 인자) | T-304 | P1 | 단위 테스트 | common |
| T-308 | C5 errors(problem+json, `exclude_paths`)·C16 security_headers(HSTS 불신 기본)·C17 cors·C8 trusted_proxy·C11 testing·C10 alembic 템플릿·C15 http·C18 dagster | T-306, T-307 | P2 | 단위 테스트 | common |
| T-310 | `py-v0.1.0`(1차) → weather-api·map-api 검증 → 정식 | T-303, T-304, T-305 | P1 | wheel 설치·소비자 스모크 | common |
| T-480 | map-api: export CLI·health·time·quality 교체, `type` URI·429 코드 정렬, pinvi/ktdm pin 갱신 동반 | T-310 | P1 | openapi.yml·pin 대조 | map(+pinvi/ktdm pin) |
| T-481 | weather-api: py 1차 채택 + airkorea 스냅샷 정본 결정(L15) + Python 3.11/3.12/3.13 정합 | T-310 | P1 | ci.yml | weather |
| T-482 | airport: py 1차 채택 + `code`/`request_id` additive + openapi `--check` CI + Docker `uv sync --locked` | T-310 | P1 | backend CI | airport |

**Phase 4 — T-4xx (앱별 정렬·전환·채택)**

| ID | 제목 | 선행 | 우선순위 | Gate | 대상 |
|---|---|---|---|---|---|
| T-420 | pinvi: 라이선스 결정 반영(L6: 루트 `LICENSE`·README/AGENTS 상충 해소·`apps/api` pyproject·maplibre 문서 정정) | 외부 선행 §F-1 | P0 | BLOCKED→문서 | pinvi |
| T-421 | pinvi: admin `--color-admin-*`→`--kt-*` 매핑 + `base.scoped.css` + tokens 채택(사용자 표면 무변경 e2e) | T-420, T-109, T-402 | P1 | e2e admin·app-shell-mobile | pinvi |
| T-422 | pinvi: ui 채택(`AdminTable` 어댑터 유지, `sortMode` 매핑, 44px 예외 등록) | T-421, T-213 | P1 | e2e 56·44px 단언 | pinvi |
| T-433 | airport: TS 7 예외 등록·ESLint 도입 판정(§F-3) + 절대 링크 상대화 + prod 도메인 placeholder 치환 + `engines` 선언 | T-005 | P2 | CI | airport |
| T-440 | geo: Node 22 CI + `uv.lock` 도입(pre-commit rev 정렬) | T-005 | P1 | ci.yml | geo |
| T-441 | geo: `@config` 실효값 빌드 검증 → `@theme` 단일화·`tailwind.config.ts` 삭제 → tokens 채택 + contrast baseline | T-402, T-109 | P1 | 시각 diff·e2e 23 | geo |
| T-443 | geo: React 19 업그레이드(ADR-019 갱신, 별도 PR, 실검증) | T-440 | P2 | unit 43·e2e 23 | geo |
| T-444 | geo: radix→base-ui 이관(12파일, `asChild` 17곳) + ui 채택; VirtualTable 잔류 | T-443, T-213 | P2 | e2e·a11y 4 spec | geo |
| T-450 | concierge: `pyproject.toml`·`uv.lock`·ruff/mypy baseline(per-file-ignores) 도입 | T-305 | P0 | 로컬 4 gate | concierge |
| T-451 | concierge: CI 신설(재사용 워크플로 호출) + production Dockerfile | T-010, T-450 | P0 | CI | concierge |
| T-452 | concierge·ktdm: 라이선스 정렬(L8) 결정 반영 | 외부 선행 §F-2 | P1 | BLOCKED→문서 | concierge/ktdm |
| T-453 | concierge: fallback 블록 제거 → `@config`→`@theme inline` → `--ktc-*`를 `--kt-*` 오버라이드로 재해석 | T-451, T-402, T-109 | P1 | e2e 45·시각 diff | concierge |
| T-454 | concierge: ui 채택(`render` 9줄→관용구, base-ui 1.8) | T-452, T-453, T-213 | P2 | e2e 45 | concierge |
| T-462 | weather: Tailwind v4 도입(theme+utilities, preflight 제외) + `@theme inline` 매핑 | T-461 | P1 | 스크린샷 diff | weather |
| T-463 | weather: 페이지별 셸·패널·폼·로그인 → common 컴포넌트, 해당 CSS 절 삭제(4 PR) | T-462, T-213 | P1 | 스크린샷 diff·vitest | weather |
| T-464 | weather: preflight 활성화 + 잔존 도메인 CSS `@layer components` + 마커 색 토큰화 + 셸 문서-코드 불일치 해소 | T-463 | P2 | 스크린샷 diff | weather |
| T-470 | ktdm: Next 16·React 19·ESLint 9·Node 22 CI 업그레이드(재포맷 금지, 별도 PR) | T-005 | P1 | ci.yml·vitest 8 | ktdm |
| T-471 | ktdm: Poetry→`uv.lock`·하한 상향·CI 핀 정리 + quality baseline + request-id `trust_incoming=False` 채택 | T-310 | P1 | ci.yml | ktdm |
| T-472 | ktdm: tokens 채택(`@theme`→`--kt-*`, Ember 값 유지) + contrast baseline | T-470, T-109, T-402 | P2 | 스크린샷 diff | ktdm |
| T-473 | ktdm: ui 부분 채택(StatStrip·AppErrorPanel) | T-452, T-472, T-213 | P3 | vitest | ktdm |
| T-483 | geo: py 2차(health alias 병행·securitySchemes+typegen 재생성·admin problem+json opt-in·request-id) | T-308, T-440 | P2 | openapi drift·gen:types | geo |
| T-484 | pinvi: `uv.lock` CI·Docker 소비 + etl `@main` 제거 + export 파이프라인·drift CI + request-id(additive) | T-310 | P2 | api.yml·etl.yml | pinvi |
| T-485 | concierge: py 1차(export·request-id·quality) + features export 계약 문서화(map provider 동시 수정 계획) | T-451, T-310 | P2 | CI | concierge/map |

**Phase 5 — T-5xx (릴리스·승격·회수)**

| ID | 제목 | 선행 | 우선순위 | Gate | 대상 |
|---|---|---|---|---|---|
| T-501 | 릴리스 runbook 1회 완주 검증(rc→소비자 PR→정식→회귀 시 되돌리기 리허설) | T-109, T-212 | P1 | consumer-smoke | common |
| T-502 | gate 승격: `check_versions`·`kt-contrast`·`ux_lint`를 소비자별 2회 green 후 `enforce: fail` | T-403, T-103 | P2 | CI | common+전 앱 |
| T-504 | 분기별 cross-repo drift 감사 runbook + 첫 실행 + 회수 지표(이식 시간·회귀 수·로컬 복사본 수) 3개월 보고 | T-008 | P2 | 문서 검증 | common |
| T-505 | 공유 라이브러리 배포 경로 정리 제안(`maplibre-vworld-react` npm·`python-*-api` SHA 정렬·airkorea 이중 경로·마커 팔레트 정본 요청) | T-008 | P3 | 문서 | 외부 저장소 |
| T-507 | 공개 npm/PyPI 게시·Renovate 설치 재평가 + Vitest 5·Node 24·react-table 9·lucide 1.x·mypy 2 breaking 평가 → `versions.json` 갱신 | T-006, T-005 | P3 | 문서·도구 테스트 | common |
| T-508 | 보류 항목 재평가(api-client-core·pagination 코덱·VirtualTable 흡수·ConfirmDialog API·토스트) | T-213, T-310 | P3 | 2인 리뷰 | common |

### E.2 critical path(추정)
T-001/002/003/005 → T-101 → T-109 → T-410·T-461 → T-201 → T-203 → T-212 → T-411 → T-208 → T-213 → T-412 (ui 트랙). 병렬: T-302 → T-303 → T-310 → T-480/481/482 (py 트랙). 소비자 확대의 실제 병목은 §F-1·§F-2(라이선스)와 T-430(airport WIP)·T-443(geo React 19)이며, 이 넷은 common 쪽에서 대체 불가능한 **외부 선행**이다.

---

## F. 사용자 확인이 필요한 열린 결정(기본값 제안 포함)

| # | 결정 | 선택지 | 기본값(이 레지스터의 제안) | 막히는 task |
|---|---|---|---|---|
| F-1 | pinvi 라이선스·공개 여부 | (a) 공개 + `GPL-3.0-or-later`(루트 LICENSE·README/AGENTS 정합) / (b) 사내 비공개(GPL 이식 코드 P1~P3 제거 또는 재선언) | **(a)** — 이미 GPL 코드(map·geo 이식, tgz)가 소스에 있고 AGENTS가 "공개"라 적음(`lic` §3.6) | T-420 → T-421/422/484 |
| F-2 | ktc·ktdm 라이선스 정렬 vs common §7 추가 허가 | (a) 두 저장소를 `GPL-3.0-or-later`로 / (b) common에 §7 예외 문구 | **(a)** — ktc는 이미 GPL `python-vworld-api` 의존; (b)는 파일마다 예외 유지·검증 비용 | T-452 → T-454/473 |
| F-2′ | geo `GPL-3.0-only` 유지 여부 | (a) `-or-later` 재선언 / (b) 유지(common에서 geo 유래 파일만 `-only` 표기) | **(a)** 권고, 결정 전엔 (b)로 진행 가능 | 없음(표기만) |
| F-3 | TypeScript 기준선과 airport 7.0.2 | (a) 5.9.3 통일(airport 하향) / (b) airport 예외 유지, ESLint 도입 시 재판정 / (c) 6.x 경유 | **(b)** — 하향 사유(빌드 속도 등) 미문서, typescript-eslint peer가 유일한 제약 | T-433 |
| F-4 | Node 24 승격 시점 | 지금 / 2026-10 Active 종료 후 / Phase 5 | **Phase 5**(T-507) — 이미지 7곳 22 일치 유지 | 없음 |
| F-5 | provider `python-*-api` SHA를 registry 범위에 넣을지 | 보고만 / 강제 / 제외 | **보고만**(`providers` 절) — 정렬 주체가 각 저장소 | T-005 |
| F-6 | 토큰 접두 | `--kt-*` / `--ktc-*` 승격 | **`--kt-*`**(충돌 0) | T-101 |
| F-7 | 다크 모드 토글 도입 계획 | 없음(정의 필수·활성 opt-in) / 있음(활성 기본) | **없음**(현재 어느 admin도 토글 미장착) | T-104 |
| F-8 | Python floor | common 3.11 호환 유지 / 앱 floor 3.12 상향 동반 | **3.11 호환 유지**; 상향은 앱별 결정 | T-302 |
| F-9 | airport "Admin" 정의·WIP 방향 | 현 백업 패널 범위 / T-035 분리 라우트 이후 셸 소비 / 토큰 값 map 프로필로 수렴 여부 | **현 범위 + 값 유지**, 셸·값 수렴은 airport 결정 후 | T-430/431/432 |
| F-10 | weather 셸 불일치 처리 | 문서 정정 / common 셸 교체 | **문서 정정 먼저**, 교체는 T-463 | T-460 |
| F-11 | dirty 이탈 경고 규칙 | 규약 포함(대상 폼 목록 필요) / 미포함 | **미포함**(8표면 모두 없음) | T-105 |
| F-12 | pinvi admin 44px 예외 2페이지 | 영구 예외 / 36px 복귀 | **영구 예외 등록** | T-422 |
| F-13 | OpenAPI 세부 | 429 코드명(`TOO_MANY_REQUESTS`/`RATE_LIMITED`), geo v2 problem+json 채택 시점, 메트릭 접두 이관 시점 | `TOO_MANY_REQUESTS`; geo는 ADR-060 묶음 시점; 접두 이관은 대시보드 평가 후 | T-301 |
| F-14 | 문서 경로 표기 | 상대 경로만 / 절대 경로 허용 | **상대만**, 절대는 `dev-environment.md`에만 | T-002 |
| F-15 | 포트·이름 | airport 14002 예외 vs 14005 이전; 컨테이너 `-latest` 제거 | **예외 등록**; `-latest`는 ktdm 결정 | T-014 |
| F-16 | prod 도메인/IP redaction 범위 | `docs/`만 / 추적 파일 전체(kta·weather 운영 기록 이동) | **common은 전체 트리**, 소비자는 opt-in 입력 | T-009 |
| F-17 | 리뷰 light 판정 주체 | merge 담당 / 작성자 | **merge 담당** | T-004 |
| F-18 | 검증 도구 언어 | Python 유지 / Node | **Python** | T-002 |

## G. coordinator 초안과의 차이(비교 가능성 유지)

| ID | 초안 | 이 레지스터 | 이유 |
|---|---|---|---|
| D-01 | 5 패키지(`config`·`api-client-core` 포함), lucide peer | 3 배포 단위, `config`·`api-client-core` 미생성, lucide 비의존, scope 확보 gate | map ESLint 잠금·pinvi 가드 파손, `ApiError` 4형 어댑터 비용, lucide major 혼재 |
| D-02 | `decisions.md` 유지(canview 동일) | `adr/README.md` 단일 색인, runbook 문구 정정 | 이중 색인 drift(ktdm DO NOT 15) |
| D-06 | 단일 기준선 표(정확값 위주), Python `>=3.12`, Actions v7 | floor/recommended/consumer pin 3열, common 3.11 호환, Actions major 강제 없음 | map exact 핀 충돌·3.11 floor 3곳 설치 불가 |
| D-07 | 정확 핀 + 대조, 보고→실패 2단계 | 금지 3종은 즉시 fail, 나머지 report→2회 green→fail, 예외 레지스트리·lockfile 의무를 스키마에 내장 | 도입 첫날 7 CI red 방지, `mcp<2`·`@main` 재발 방지 |
| D-08 | 앱별 방식 서술 | 순서(airport→dm→geo→concierge→pinvi→weather) + 4단 PR + 중단 조건 + weather preflight 제외 단계 | weather 2,495행 무스타일·geo 실효값 미확인 |
| D-09 | React 19 전용, base-ui overlay | 동일 + peer fail-fast, `type` 명시, native Checkbox, DataTable `sortMode` 필수 prop, VirtualTable 잔류 | pinvi 36페이지·e2e 계약, base-ui 미확인 사실 |
| D-10 | npm + `@source`, 레지스트리 2차 | 동일 + `base.scoped.css` 변형, webpack/Turbopack 양쪽 스모크, 마크업 계약 major | pinvi 사용자 표면 누출·ADR-066 |
| D-12 | 다크 "활성화는 앱 선택" | 다크 값 필수·활성 파일 **명시 import**만, contrast report+baseline | 미검증 다크 노출·첫날 red |
| D-13 | C1~C22 제안대로 | 신규 MUST/기존 baseline 이원화, grep 게이트 report 선행, C9 geo 매핑 보류 | 잔존 `window.confirm` 7건 |
| D-14 | MUST 전면 채택 + 예외 | 즉시 MUST(additive)/신규 MUST·기존 SHOULD/SHOULD 3계층 + 예외 yaml + health 별칭 2릴리스 | pinvi·concierge 외부 계약, ktdm probe |
| D-15 | 1차 C4·C12·C13·C20 | 동일하되 C20 format 미포함·baseline, C3 접두 강제 없음, C5는 `exclude_paths` 필수 | ktdm format 금지, 대시보드 회귀, geo v1 |
| D-16 | tokens·UI 1차 = map+pinvi admin | tokens = map+weather+airport, ui = map+airport; pinvi·concierge·ktdm은 라이선스 gate 뒤 | B1·B9(`lic` §4) |
| D-17 | licensing 결론 대기 | GPL-3.0-or-later 확정, §7 예외 기각, 추출 gate B1~B10, SPDX 린트 즉시 fail | 조사 완료됨 |
| D-18 | ci-deploy 결론 대기 | 재사용 워크플로 태그 참조·job 이름 입력·운영 호출 job required 금지·포트 정본 ktdm 유지 | ruleset 잠김·이원화 |
| 신규 | — | D-19~D-27(모바일 취급·airport Admin 정의·시각 기준선 의무·접두 명명·공유 lib·되돌리기·NOT_RUN·마커·decisions.md) | 초안 F절 메모를 결정으로 승격 |

## H. 상위 위험(설계 전체)

1. **라이선스 gate가 소비자 확대의 실제 병목**(F-1·F-2): pinvi·concierge·ktdm 3곳은 결정 전까지 규칙 문서·`tokens.json`까지만 — 계획은 이를 BLOCKED로 명시했다.
2. **weather v4 전환은 검증 수단이 없다**(Playwright 부재, 2,495행): 스크린샷 기준선(T-108·T-460)이 없으면 어떤 diff도 "픽셀 동일" 주장에 그친다.
3. **버전 정렬은 lockfile 없는 4곳에서 검증 불가**: `uv.lock` 도입(T-440·T-450·T-471·T-484·T-480)이 선행돼야 `check_versions`가 의미를 가진다.
4. **map 산출물 변경 = pinvi·ktdm pin 파손**: T-480은 pin 갱신 PR을 동반하지 않으면 머지 금지.
5. **base-ui 미확인 3건**(`type` 기본·hidden input·Toast API)은 T-201에서 소스로 확정하기 전까지 Button/Checkbox 계약을 릴리스하지 않는다.
6. **geo `@config` 실효값 미확인**: T-441 ①단계 없이 `@theme` 단일화하면 색이 조용히 바뀐다.
7. **npm scope 미확보**: T-006 실패 시 개명은 첫 소비자 PR 전이어야 비용 0.
