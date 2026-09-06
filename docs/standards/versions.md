# 라이브러리·플랫폼 버전 일치 정책 (versions)

- 정본 지위: 이 문서는 버전 정렬 **정책**의 정본이고, 기준선 **값**의 정본은 루트 [`versions.json`](../../versions.json)(schema `kor-travel-common.version-registry.v1`)이다. 두 문서가 어긋나면 `versions.json`이 값을, 이 문서가 규칙을 이긴다. 검사기는 [`tools/check_versions.py`](../../tools/check_versions.py).
- 확정 task: T-005(★이번 PR; 7 소비자 현재값·예외의 최종 등록은 잔여), T-005a(`uv.lock` 확장), T-005b(`poetry.lock`·`requirements.txt`), T-403(소비자 CI 삽입), T-502(gate 승격), T-507(재평가). 이 문서는 정본 초안이며 실물 소비자 매니페스트(T-011)와 대조해 확정하는 task가 남아 있다.
- 마지막 갱신: 2026-09-06. 결정 근거: [설계 브리프](../plan/design-brief.md) D-06·D-07·D-30·D-31, ADR-008([ADR 색인](../adr/README.md)).
- 상위 문서: [standards 색인](README.md). 관련: [frontend-stack](frontend-stack.md), [backend-stack](backend-stack.md), [ci-deploy](ci-deploy.md), [consumer adoption runbook](../runbooks/consumer-adoption.md), [release runbook](../runbooks/release.md).

## 1. 목적과 범위

사용자 지시 (2) "라이브러리/플랫폼 버전 일치"를 **레지스트리 + 대조 도구 + 단계적 강제**로 구현한다. 7개 소비 저장소(airport·concierge·docker-manager·geo·map·weather·pinvi)의 프론트엔드·백엔드·런타임 축을 하나의 기준선(2026-09)에 맞추되, 정렬은 "선언"이 아니라 **lockfile에 기록된 설치본**으로 판정한다. 조사에서 선언 하한과 설치본이 크게 어긋난 사례(dm react-query `^5.28` ↔ 설치 5.101, concierge rhf `^7.51.5` ↔ 7.77 — [version-matrix](../survey/cross/version-matrix.md) §7.1)가 다수였기 때문이다.

범위 밖: PostgreSQL/PostGIS major(별도 트랙, `vm` §5.1), 공유 라이브러리(`maplibre-vworld-*`, `python-*-api`)의 배포·정렬 주체(보고만, O-16), Docker 이미지 digest 값 자체(형식 규칙만 [ci-deploy](ci-deploy.md)).

## 2. 용어

| 용어 | 뜻 |
|---|---|
| 축(axis) | `versions.json` `axes.<key>` 한 항목. 패키지 하나 또는 묶음(`react`+`react-dom`)에 대응 |
| floor | 하한. 설치본(또는 선언 하한)이 이보다 낮으면 `BELOW_FLOOR`. 접두 비교(`22.12`는 `22.12.x` 전체) |
| recommended | 권장 접두. 설치본이 이 접두와 일치하면 `OK`, 아니면 `NOT_RECOMMENDED`(정보용, 어느 모드에서도 실패 아님). 범위 선언(`>=22`)의 하한에는 적용하지 않는다 |
| max | 배타 상한. 근거가 있는 축에만(`typescript` 6.1 · `maplibre-gl` 6 · `@tanstack/react-table` 9). 설치본이 이 값 이상이면 `ABOVE_MAX` |
| 선언 | `package.json` `dependencies`/`devDependencies`/`engines`/`packageManager`, `pyproject.toml` `[project]`/`[tool.poetry]`, `requirements.txt`의 범위 문자열 |
| 설치본 | `package-lock.json`(lockfileVersion 3) `packages[…].version`, `uv.lock` `[[package]].version`. lockfile이 없으면 설치본은 **미확인**이다 |
| 예외(exception) | `exceptions[]{repo,key,installed,reason,until,review}`. 해당 저장소·축·설치본 접두에 한해 원 판정을 `EXEMPT`로 덮는다. `until` 경과 시 `EXEMPT_EXPIRED` |
| 차단(blocked) | `blocked[]{ecosystem,name,range,reason,since}`. 설치본이 범위에 들면 `BLOCKED` |
| enforce | `consumers.<repo>.enforce` ∈ `report`/`warn`/`fail`. 소비자별 강제 수준(D-30) |
| 매니페스트 | 소비 저장소의 `kor-travel-common.lock.json`(`consumer-manifest.v1`, T-011). 도구는 `lockfiles[]`·`repo`만 읽는다 |

## 3. 정책

### 3.1 계층별 하이브리드(D-07)

| 계층 | 선언 방식 | lockfile | 대조 |
|---|---|---|---|
| common 자체 패키지(`packages/*`, `packages/py/*`) | **정확 핀** | 루트 `package-lock.json` 커밋, `packages/py/.../uv.lock` 커밋(D-33) | common CI `check-versions(report)` job이 자기 자신을 대조 |
| 소비자 플랫폼·프레임워크·툴체인 축(node·npm·python·next·react·typescript·tailwindcss·eslint·vitest·playwright·fastapi·sqlalchemy·alembic·pytest·ruff·mypy·dagster) | 선언 형식 자유(caret·범위·exact) | **의무** | 설치본을 floor/recommended/max와 대조 |
| 그 밖의 라이브러리 축(react-query·zod·zustand·rhf·httpx·structlog 등) | 자유 | 의무 | 동일(대개 `NOT_RECOMMENDED`까지만) |
| 앱 도메인 의존성(provider 라이브러리·LLM SDK 등) | 자유 | 의무 | 축 없음. git 참조 고정 여부와 `blocked`만 검사 |

근거: map의 exact 핀 + 상수 검증(`verify-*.mjs`), pinvi lock 무결성 검사, weather `--locked`, dm SHA 핀이 각각 다른 계층을 이미 강제하고 있어(`vm` §3.6·§7.2 P3) 하나로 통일하면 어느 쪽이든 큰 이동이 필요하다. 전면 정확 핀(P1)은 봇 없이 유지 불가, caret+lock(P2)만으로는 매니페스트만 봐서 판정 불가라 기각했다.

### 3.2 lockfile 의무

- npm: `package-lock.json` **lockfileVersion 3** 커밋. CI·Docker는 `npm ci`. lockfileVersion 1·2는 `NO_LOCK`으로 본다(npm 7+에서 `npm install`로 재생성).
- Python: `uv.lock` 커밋 + CI·Docker 모두 `uv sync --locked`(weather 선례, `vm` §2.1). airport(CI만)·pinvi(미소비)는 T-482·T-484에서 소비 일관화. Poetry(ktdm)·`requirements.txt`(concierge)는 uv 전환 task(T-471·T-450)가 선행이며 그때까지 `NO_LOCK`으로 보고된다.
- 워크스페이스: npm 워크스페이스는 루트 lock 하나가 전 멤버를 해석한다(map·pinvi). 도구는 멤버 `package.json`을 별도 범위로 보고하되 설치본은 `<멤버>/node_modules/<pkg>` → 루트 `node_modules/<pkg>` 순으로 찾는다. uv 워크스페이스도 같은 방식.
- lock 재생성 사고 방지: `--package-lock-only`로 만든 lock은 `integrity`가 빠질 수 있다(pinvi T-352, `vm` §3.6). 채택 PR은 lock 동반 커밋이 필수다(D-24).

### 3.3 판정 어휘(D-07)

| 판정 | 조건 | report | warn | fail |
|---|---|---|---|---|
| `OK` | floor 이상, max 미만, recommended 접두 일치(범위 선언은 floor·max만) | — | — | — |
| `NOT_RECOMMENDED` | floor 이상이지만 recommended 접두와 다름 | — | `::warning::` | `::warning::`(실패 아님) |
| `BELOW_FLOOR` | 설치본 또는 선언 하한이 floor 미만 | — | `::warning::` | `::error::` + exit 1 |
| `ABOVE_MAX` | 설치본이 max 이상 | — | `::warning::` | `::error::` + exit 1 |
| `NO_LOCK` | lockfile 없음·버전 불일치·lock에 항목 없음·파서 미지원(Poetry·requirements) | — | `::warning::` | `::error::` + exit 1 |
| `NO_ENGINES` | `engines.node`(또는 `requires-python`) 미선언, 하한 없는 범위(`*`) | — | `::warning::` | `::error::` + exit 1 |
| `FLOATING_REF` | git/URL 의존성이 SHA·버전 태그·릴리스 자산으로 고정되지 않음(`@main`, 참조 없음, `semver:` 범위), npm 선언 `*`/`latest`(워크스페이스 링크 제외) | **`::error::`** | `::error::` | `::error::` + exit 1 |
| `BLOCKED` | 설치본이 `blocked[]` 범위에 포함 | **`::error::`** | `::error::` | `::error::` + exit 1 |
| `EXEMPT` | 예외 등록·`until` 이내(비고에 원 판정 표기) | — | — | — |
| `EXEMPT_EXPIRED` | 예외 `until` 경과 | **`::error::`** | `::error::` | `::error::` + exit 1 |

우선순위: `BLOCKED` > 예외(`EXEMPT`/`EXEMPT_EXPIRED`) > `ABOVE_MAX` > `BELOW_FLOOR` > `NOT_RECOMMENDED` > `OK`. `NO_LOCK`·`NO_ENGINES`·`FLOATING_REF`는 대조 자체가 불가능한 상태이므로 축 판정과 별개 행으로 나온다.

### 3.4 강제 수준 3단(D-30)

| 모드 | exit | 용도 |
|---|---|---|
| `report`(기본) | 항상 0. 단 `FLOATING_REF`·`BLOCKED`·`EXEMPT_EXPIRED`는 `::error::` 주석 | Phase 0~1 전 소비자. 격차를 실패가 아닌 보고로 낸다(`vm` §7.4) |
| `warn` | 0. 실패 후보 전부 `::warning::` | 승격 직전 관찰 기간 |
| `fail` | `BELOW_FLOOR`·`ABOVE_MAX`·`NO_LOCK`·`NO_ENGINES`·`FLOATING_REF`·`BLOCKED`·`EXEMPT_EXPIRED`가 하나라도 있으면 1 | 승격 후 |

`NOT_RECOMMENDED`는 어느 모드에서도 실패가 아니다. 권장값은 분기 감사에서 상향되며 강제는 floor/max로만 한다.

### 3.5 승격 권한과 절차(D-07·D-30)

- **모드는 common `versions.json` `consumers.<repo>.enforce`가 소유한다.** 소비 저장소의 매니페스트·워크플로에는 `enforce`를 두지 않으며(D-19), 재사용 워크플로(`versions-check.yml`, T-010)는 `--mode`를 넘기지 않는다. `--mode`는 로컬 실행용 override이고 CI에서 쓰면 규약 위반이다.
- 승격 조건: 해당 소비자의 report 실행에서 **실패 후보(§3.4 fail 기준) 0인 실행이 2회 연속**. `consumers.<repo>.clean_runs`를 common PR로 갱신하고 2에 도달하면 같은 PR 또는 다음 PR에서 `enforce`를 올린다(T-502). `report → warn → fail` 순으로만 올리며 단계를 건너뛰지 않는다.
- 강등 조건: 소비자가 우회 패치(검사 비활성·lock 제거)로 green을 만든 흔적이 발견되면 `report`로 내리고 journal에 기록한다. 강등도 common PR.
- 소비자 자율 선언(각 앱이 자기 강제 수준을 정하는 방식)은 지시 (2)의 완화이므로 기각했다.

### 3.6 예외 등록과 만료

- 예외는 `exceptions[]` 한 항목 = 저장소 1 × 축 1 × 설치본 접두 1. 여섯 필드(`repo`·`key`·`installed`·`reason`·`until`·`review`) 모두 필수이며 `until`은 ISO 날짜, `review`는 재판정 task ID(또는 열린 결정 O-n)와 조사 근거다.
- `until`이 없는 예외는 등록할 수 없다(레지스트리 로더가 거부). 기본 만료는 다음 분기 감사(`next_review` 2026-12, T-506). 만료되면 `EXEMPT_EXPIRED`로 `::error::`가 뜨며, 연장은 새 `until`과 갱신된 `reason`으로 common PR을 낸다.
- 예외는 **위반을 없애지 않는다**. 원 판정이 비고에 남고 [adoption-readiness](../architecture/adoption-readiness.md)의 gate 표에 집계된다.
- 사용자 승인 대기 항목은 예외로 등록하지 않는다: pinvi mobile Tailwind 3(NativeWind 4)은 **O-8 사용자 승인 전까지 미등록**이며 report에 `BELOW_FLOOR`로 그대로 보인다(브리프 §7). 승인 시 `installed: "3.4"`, `until`: NativeWind 5 GA 재평가 시점으로 등록한다.

### 3.7 차단 목록

`blocked[]`는 회귀가 확인된 버전 범위다. 초기 등록: `mcp >=2`(PyPI) — FastMCP→MCPServer API 변경으로 concierge `ktc/mcp_server/server.py` v1 API와 비호환, 2026-09-04 배포에서 전이 의존성으로 2.1.1이 설치되며 깨졌다([inv/ktc](../survey/inventory/kor-travel-concierge.md) §4.1, `vm` §7.3). 차단은 report 모드에서도 `::error::`이며 해제는 근거(호환 PR 머지)와 함께 common PR로만 한다. dm 런타임 핀 레지스트리의 `blocked_pinsets`(삭제 API 없음, fail-close) 원칙을 따른다(`vm` §7.3).

### 3.8 floating 참조 금지(D-11)

`@main`·branch·참조 없는 git URL, `latest` 태그, npm `*`/`latest` 선언은 `FLOATING_REF`다. 허용되는 고정 형식: 40자리 SHA, GitHub `/tarball|/archive|/commit/<sha>`, GitHub Release 자산 URL(`/releases/download/<tag>/…` — common npm 배포 형식), 버전형 태그(`v1.2.3`, `py-v0.1.0`; `uv.lock`이 SHA를 기록). 관찰된 위반: pinvi `apps/etl` `python-kasi-api@main`(`vm` §2.7), RustFS/mc `latest` 이미지(도구 범위 밖, [ci-deploy](ci-deploy.md)). 재사용 워크플로 참조(`uses: digitie/kor-travel-common/.github/workflows/x.yml@<tag|sha>`)도 같은 규칙이며 T-009에서 검사 대상에 넣는다.

### 3.9 기준선 갱신

- 값 변경(`axes`·`blocked`·`exceptions`·`consumers.enforce`)은 common PR + 2인 리뷰 비면제(D-04) + `CHANGELOG.md` 기록.
- 분기마다(T-506) 최신 안정 버전을 재조회해 `recommended`를 올리고 `floor`는 EOL·보안 floor·peer 제약이 있을 때만 올린다. Node 24/26·Vitest 5·react-table 9·lucide 1.x·mypy 2·TS 7 재평가는 T-507.
- 기준선을 올리면 `baseline`을 `YYYY-MM`으로 바꾸고 이 문서 §4 표를 함께 갱신한다. 과거 기준선은 CHANGELOG에 남기고 레지스트리에 이력을 쌓지 않는다.

## 4. 2026-09 기준선 매트릭스(D-06 표)

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

값의 출처: `vm` §4(2026-09-06 registry 조회), §5.1 후보 A(현재 다수와 최소 이동) 채택. 최신(후보 B: Node 24·Python 3.12 floor·TS 7)은 채택하지 않았다 — Node 20 CI 3곳·Python 3.11 하한 3곳·typescript-eslint peer 때문(`vm` §5.1, [backend](../survey/cross/backend.md) §2.1·§5.3). 판정 3인 모두 "단일 정확값 표"를 기각했으므로 floor/recommended 두 값으로 둔다(브리프 D-06 채택 사유).

레지스트리 키와의 대응: 표의 "Node"→`node`, "npm"→`npm`, "Next.js"→`next`, "React"→`react`(react-dom 포함), "Tailwind / @tailwindcss/postcss"→`tailwindcss`(두 패키지), "ESLint / typescript-eslint"→`eslint`·`typescript-eslint`(후자는 floor 8.0), "react-query … resolvers"→`@tanstack/react-query`·`@tanstack/react-table`(max 9)·`@tanstack/react-virtual`·`zod`·`zustand`·`react-hook-form`(recommended `7.87`)·`@hookform/resolvers`, "Python(common 패키지)"→`python`(앱 `requires-python` 하한 대조), "Python 이미지"→`python-image`(`checked: false`), "uv"→`uv`(`checked: false`), "PostgreSQL / PostGIS"→`postgresql`(`checked: false`), "GitHub Actions"→`actions` 절(`checked: false`, T-009), "provider SHA"→`providers` 절.

## 5. 앱별 격차(2026-09-06 기준 커밋)

[commonality-matrix](../survey/commonality-matrix.md) §3.2 요약. 난이도는 조사의 추정이다. `check_versions` 열은 이 PR에서 기준 커밋 체크아웃에 report 모드로 실행한 결과 요약(도구 실행 evidence; 값은 `vm` §1~§2와 일치)이다.

| 앱 | major 격차 | 선행 작업(공통 소비 전) | `check_versions` report(실패 후보) | 난이도 |
|---|---|---|---|---|
| airport | TypeScript 7.0.2(예외 등록, O-6); Tailwind 미도입(WIP `99b3f98`) | WIP 병합(T-430), `engines` 선언·ESLint 도입 판정(T-433), Docker `uv sync --locked`(T-482) | `NO_ENGINES` 1(frontend); TS 7은 `EXEMPT` | 낮~중 |
| concierge | `@hookform/resolvers` 3, `maplibre-gl` 6.0(예외), `@base-ui/react` 1.5 | **CI 신설**(T-451), **Python lock 도입**(T-450; `mcp<2` 사고), `@config` 제거 | `NO_LOCK` 14(requirements 4벌), `NO_ENGINES` 5, `BELOW_FLOOR` 3(node `>=22`·base-ui·resolvers) | 중~높 |
| docker-manager | Next 14, React 18, ESLint 8(모두 예외, T-470), shadcn 미도입 | Poetry→uv(T-471), 하한 상향, CI Node 22 | `NO_LOCK` 9(Poetry), `NO_ENGINES` 1 | **높음** |
| geo | React 18(예외, O-25), Radix→Base UI, lucide 0.x | CI Node 22·`uv.lock`(T-440), `@config` 제거(T-441), pre-commit 정렬 | `NO_LOCK` 25(Python), `NO_ENGINES` 1 | **높음**(UI) / 중(Python) |
| map | TS 6.0.3(map-marker-react) vs 5.9.3 | **Python lock 도입**, `starlette<1.0`·`alembic<1.20` 재검토(T-480), npm 12.0.1 합의 | `NO_LOCK` 26(Python 3 패키지); exact 핀 4건은 `EXEMPT` | 낮~중 |
| weather | Tailwind 미도입, Next 15, Vitest 3(예외, T-460) | CI Node 22, `engines` 선언, 벤더링 `python-airkorea-api` `requires-python >=3.10` 정리(T-481) | `NO_ENGINES` 1, `BELOW_FLOOR` 1(벤더링 패키지 python 3.10) | 중~높 |
| pinvi web/admin | `@hookform/resolvers` 3, jsdom 25, lucide 0.x | `uv.lock` CI·Docker 소비, etl `@main` 제거(T-484), **라이선스 결정 선행**(O-1) | `BELOW_FLOOR` 3(engines `>=20`, resolvers, mobile tailwind 3), `NO_LOCK` 9(etl), `FLOATING_REF` 1(`python-kasi-api@main`) | 중 |
| pinvi mobile | Tailwind 3.4.19(NativeWind 4) — O-8 대기 | NativeWind 5 GA | `BELOW_FLOOR`(tailwindcss) — 승인 전 미등록 | **높음**(외부) |

## 6. 전환 트랙(매트릭스 §3.3)

| 트랙 | 대상 | 근거 | task |
|---|---|---|---|
| Tailwind v4 도입(미도입→도입) | weather admin, airport main(WIP), pinvi mobile(v3→v4, NativeWind 5 대기) | `vm` §1.2·§1.7; [inv/weather](../survey/inventory/kor-travel-weather.md) §9.1; [inv/airport](../survey/inventory/kor-travel-airport.md) §3.2 | T-462, T-430, O-8 |
| `@config` v3 config 잔존 제거 | geo, concierge, pinvi web | [design-tokens](../survey/cross/design-tokens.md) §3.1.1·§3.6.3 | T-441, T-453, T-421 |
| React 18→19 | geo, docker-manager | `vm` §5.3 | T-443(O-25), T-470 |
| Next 14/15→16 | docker-manager(14.2.35), weather(15.5.24) | `vm` §5.3(Async Request API·`proxy`·`next lint` 제거) | T-470, T-460 |
| Radix→Base UI | geo | [ui-components](../survey/cross/ui-components.md) §5.2 | T-444 |
| TypeScript 기준선 | airport 7.0.2 → 5.9(또는 6.x 경유) | `vm` §6 | T-433(O-6) |
| ESLint 8→9/10 | docker-manager; airport는 0에서 도입 | `vm` §1.6 | T-470, T-433 |
| Vitest 3→4 | weather | `vm` §1.6 | T-460 |
| Node 20 CI→22 | docker-manager, geo, weather(Node 20 EOL 2026-04-30) | `vm` §1.1·§4.4 | T-403 |
| npm 실행기 정책 | map 12.0.1 vs pinvi 11.19.1 vs 동봉 10.9 | `vm` §3.2 | T-005(O-10) |
| Python lockfile 도입 | geo, map, docker-manager, concierge | `vm` §2.1·§7; `be` §5.3 | T-440, T-480, T-471, T-450 |
| Python floor 3.11 vs 3.12 | map·weather·docker-manager(3.11) vs airport·geo·pinvi(3.12) | `be` §2.1·§7-1 | O-7 |
| lockfile 소비 일관화 | airport Docker pip, pinvi CI·Docker pip | `vm` §2.1 | T-482, T-484 |
| lucide-react 0.x→1.x | docker-manager, geo, weather, pinvi | `vm` §1.3(breaking 미조회) | T-507 |
| starlette/alembic 상한 | map `starlette<1.0`, `alembic<1.20` | `vm` §2.2·§2.3 | T-480 |
| provider git SHA 정렬 | `python-kma-api`(map ≠ weather), `python-kasi-api`(airport SHA vs pinvi etl `@main`), `python-airkorea-api`(weather path vs map SHA) | `vm` §2.7 | T-505(O-16) |
| PostgreSQL/PostGIS major | 전 앱 16+3.5(최신 18+3.6) — 분리 | `vm` §3.4·§5.1 | 범위 밖 |
| Prometheus major | ktdm·pinvi v2.53.1 vs weather v3.5.0 | `vm` §3.4 | [ci-deploy](ci-deploy.md) |

## 7. 레지스트리 스키마(`kor-travel-common.version-registry.v1`)

```json
{
  "schema": "kor-travel-common.version-registry.v1",
  "baseline": "2026-09",
  "updated": "2026-09-06",
  "next_review": "2026-12",
  "axes": {
    "node": {"ecosystem": "runtime", "floor": "22.12", "recommended": "22.23", "image": "node:22-bookworm-slim", "check": "engines.node"},
    "react": {"ecosystem": "npm", "packages": ["react", "react-dom"], "floor": "19.0", "recommended": "19.2.8"},
    "typescript": {"ecosystem": "npm", "floor": "5.9", "recommended": "5.9.3", "max": "6.1"},
    "python-image": {"ecosystem": "image", "floor": "3.11-slim", "recommended": "3.12-slim", "checked": false}
  },
  "actions": {"consumer_policy": "현행 major 유지 + SHA 핀", "common": {"actions/checkout": "v7"}, "checked": false},
  "exceptions": [{"repo": "kor-travel-airport", "key": "typescript", "installed": "7.0", "reason": "…", "until": "2026-12-31", "review": "T-433; vm §6"}],
  "blocked": [{"ecosystem": "pypi", "name": "mcp", "range": ">=2", "reason": "…", "since": "2026-09-04"}],
  "consumers": {"kor-travel-map": {"enforce": "report", "clean_runs": 0, "aliases": ["ktm", "map"]}},
  "providers": {"policy": "report", "packages": {"python-kasi-api": {"repo": "https://github.com/digitie/python-kasi-api"}}}
}
```

| 절 | 필드 | 규칙 |
|---|---|---|
| 머리 | `schema`(고정 문자열)·`baseline`(`YYYY-MM`)·`updated`·`next_review`·`policy`·`source` | 로더는 `schema` 불일치 시 exit 2 |
| `axes.<key>` | `ecosystem` ∈ `runtime`/`npm`/`pypi`/`image`/`tool`/`db`(필수), `packages[]`(생략 시 key), `floor`/`recommended`/`max`(문자열 또는 null), `image`, `check`, `checked`(기본 true), `note`, `source` | `runtime` 축은 `engines.node`·`engines.npm`(또는 `packageManager`)·`requires-python`의 **하한**을 대조하고, exact 값이면 recommended까지 대조 |
| `actions` | `consumer_policy`·`common{}`·`checked: false` | 도구 미검사(T-009에서 워크플로 파서 추가 후보) |
| `exceptions[]` | `repo`(consumers 키)·`key`(axes 키)·`installed`(접두)·`reason`·`until`(ISO)·`review` — 6개 모두 필수 | 접두 일치 시에만 적용; 다른 설치본이 되면 자동 무효 |
| `blocked[]` | `ecosystem`·`name`·`range`·`reason`(필수)·`since`·`source` | `range`는 `>=`·`<`·`==`·`,` 조합 |
| `consumers.<repo>` | `enforce`(`report`/`warn`/`fail`)·`clean_runs`·`aliases[]`·`note` | 7개 고정. 신규 소비자는 common PR |
| `providers` | `policy: "report"`·`packages{name:{repo}}`·`note` | 보고 전용. `python-*-api` 패턴은 목록에 없어도 보고 |

형식은 dm 런타임 핀 레지스트리(`schema`·`blocked_pinsets`·"값은 파일이, 계약은 코드가 소유")를 라이브러리 축으로 옮긴 것이다(`vm` §7.3). 소비자 매니페스트(`consumer-manifest.v1`, T-011)는 별도 파일이며 이 레지스트리에 소비자 값을 복제하지 않는다.

## 8. 도구 사용법(`tools/check_versions.py`)

```bash
# 소비 저장소 체크아웃을 자동 탐색(package.json·pyproject.toml·requirements.txt, 깊이 4, node_modules 제외)
python3 -B -X utf8 tools/check_versions.py /path/to/kor-travel-map --repo kor-travel-map

# 매니페스트의 lockfiles[]만 대조(T-011 이후 CI 표준 호출; --mode 없음 = versions.json enforce)
python3 -B -X utf8 tools/check_versions.py --manifest /path/to/app/kor-travel-common.lock.json \
  --json report.json --markdown report.md

# 예외 만료를 미리 보기
python3 -B -X utf8 tools/check_versions.py /path/to/app --repo wx --today 2027-01-15
```

- 인자: 위치 인자 = 저장소 루트(여러 개 가능), `--manifest`, `--registry`(기본 common 루트 `versions.json`), `--repo`(consumers 키 또는 별칭; 기본 매니페스트 `repo` → 디렉터리 이름), `--mode`(로컬 override), `--today`, `--json`, `--markdown`, `--no-step-summary`, `--quiet`.
- 출력: 표준 출력에 Markdown 표(범위·축·생태계·선언·설치·판정·비고) + GitHub annotation(`::error::`/`::warning::`) + 요약 1줄. `--json`은 `kor-travel-common.version-report.v1`. `GITHUB_STEP_SUMMARY`가 있으면 표를 덧붙인다.
- exit: 0(report·warn), 1(fail 모드 실패 후보 존재), 2(레지스트리·매니페스트·경로 오류).
- 읽는 것: `package.json`·`package-lock.json`(v3)·`pyproject.toml`(PEP 621·Poetry 선언)·`uv.lock`·`requirements.txt`(선언만). 쓰는 것: `--json`·`--markdown` 출력 파일뿐. 네트워크 없음. Python 3.11+ 표준 라이브러리(`tomllib`)만 쓰며 Windows에서 동작한다(D-03 Tier 2; 회귀 시험 `tests/test_check_versions.py`).
- 한계(사실): `poetry.lock` 파서 없음(T-005b) → `NO_LOCK`; Docker 이미지·GitHub Actions·CI Node 버전은 읽지 않음(T-009); git 고정 판정은 §3.8 휴리스틱; 여러 lock 항목(중첩 설치)이 있으면 워크스페이스 멤버 경로를 우선한다.
- CI 연동: common `check-versions(report)` job(T-009)과 재사용 워크플로 `versions-check.yml`(T-010). 소비자는 기존 워크플로에 job을 추가하는 방식으로 호출하며 required check 이름은 입력으로 개방한다([ci-deploy](ci-deploy.md)).

## 9. 열린 결정(사용자 확인 필요; 기본값으로 진행)

| # | 결정 | 기본값(이 문서·레지스트리 반영) |
|---|---|---|
| O-5 | npm scope `@kor-travel` | 잠정; 실패 시 `@digitie/kor-travel-*`(레지스트리 값과 무관) |
| O-6 | TS 기준선·airport 7.0.2 | 5.9.3 + airport 예외(`until` 2026-12-31, T-433) |
| O-7 | Python 앱 floor 3.12 시점 | common 3.11 호환 유지; 앱 상향은 Phase 4 |
| O-8 | pinvi mobile Tailwind 3 예외 | **미등록**(사용자 승인 대기). report에 `BELOW_FLOOR`로 표시 |
| O-10 | Node/npm | Node 22 floor 22.12·recommended 22.23; npm floor 10.9·recommended 11.19; map 12.0.1 예외 |
| O-16 | 공유 라이브러리·provider SHA | `providers` 보고만; 정리 요청 T-505 |
| O-18 | Renovate | 미설치 전제, [`templates/dependabot.yml`](../../templates/dependabot.yml) |

## 10. 근거

- 결정: [design-brief](../plan/design-brief.md) D-06·D-07·D-30·D-31·D-33, §2 O-5~O-10·O-16·O-18, §7.
- 조사: [version-matrix](../survey/cross/version-matrix.md) §1~§7(선언/설치 표, 2026-09-06 최신 조회, 핀 정책 후보 P1~P5, dm 레지스트리 형식), [commonality-matrix](../survey/commonality-matrix.md) §3, [backend](../survey/cross/backend.md) §2.1·§5, [ci-deploy](../survey/cross/ci-deploy.md) §1.3, [inv/map](../survey/inventory/kor-travel-map.md) §9, [inv/ktc](../survey/inventory/kor-travel-concierge.md) §4.1, [inv/ktdm](../survey/inventory/kor-travel-docker-manager.md) §8.
- 조사 오기 정정값은 [survey README](../survey/README.md) §6.2를 따른다(Node 22 동봉 npm 10.9.8, common Python floor 3.11).
