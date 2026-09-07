# 라이브러리·플랫폼 버전 일치 정책 (versions)

- 정본 지위: 이 문서는 버전 정렬 **정책**의 정본이고, 기준선 **값**의 정본은 루트 [`versions.json`](../../versions.json)(schema `kor-travel-common.version-registry.v1`)이다. 두 문서가 어긋나면 `versions.json`이 값을, 이 문서가 규칙을 이긴다. 검사기는 [`tools/check_versions.py`](../../tools/check_versions.py).
- 확정 task: T-005(정책·npm v3 구현, 독립 리뷰 진행), T-005a(`uv.lock` 확장), T-005b(`poetry.lock`·`requirements.txt`), T-011(consumer-manifest.v1 strict validator), T-403(소비자 CI 삽입), T-502(gate 승격), T-507(재평가). 이 문서는 버전 정책 정본이고 매니페스트 필드·초안은 [T-011](../tasks/T-011-consumer-manifest-schema.md)과 `templates/`가 소유한다.
- 마지막 갱신: 2026-09-07. 결정 근거: [설계 브리프](../plan/design-brief.md) D-06·D-07·D-30·D-31, ADR-008([ADR 색인](../adr/README.md)).
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
| 선언 | `package.json` `dependencies`/`devDependencies`/`optionalDependencies`/`engines`/`packageManager`, `pyproject.toml` `[project]`/`[tool.poetry]`, `requirements.txt`의 범위 문자열 |
| 설치본 | `package-lock.json`(lockfileVersion 3) `packages[…].version`, `uv.lock` `[[package]].version`. lockfile이 없으면 설치본은 **미확인**이다 |
| 예외(exception) | `exceptions[]{repo,key,installed,reason,until,review}`. 해당 저장소·축·설치본 접두에 한해 원 판정을 `EXEMPT`로 덮는다. `until` 경과 시 `EXEMPT_EXPIRED` |
| 차단(blocked) | `blocked[]{ecosystem,name,range,reason,since}`. 설치본이 범위에 들면 `BLOCKED` |
| enforce | `consumers.<repo>.enforce` ∈ `report`/`warn`/`fail`. 소비자별 강제 수준(D-30) |
| 매니페스트 | 소비 저장소의 `kor-travel-common.lock.json`(`consumer-manifest.v1`, T-011). `validate_manifest.py`가 전체 v1 계약을 strict 검사한 뒤 `check_versions.py`가 `lockfiles[]`·`repo`와 저장소 루트 workflow를 읽는다 |

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

- npm: `package-lock.json` **lockfileVersion 3** 커밋. CI·Docker는 `npm ci`. lockfileVersion 1·2는 `NO_LOCK`으로 본다. `npm-shrinkwrap.json`이 함께 있으면 npm이 이를 우선하므로, 미지원 shrinkwrap 대신 package-lock을 신뢰하지 않고 `NO_LOCK`으로 보고한다.
- Python: `uv.lock` 커밋 + CI·Docker 모두 `uv sync --locked`(weather 선례, `vm` §2.1). airport(CI만)·pinvi(미소비)는 T-482·T-484에서 소비 일관화한다. 과도기 Poetry는 `poetry.lock`의 package/version·Python metadata와 git source를 제한적으로 읽고, `requirements*.txt`는 재귀 선언을 읽되 정확 `==` 핀만 설치본 후보로 삼는다. requirements 결과에는 `NO_LOCK`을 남기며 범위 선언은 설치본 대조가 아니다. Poetry parser의 결과도 uv lock 도입·소비자 gate를 대신하지 않는다(T-005b, T-471·T-450).
- `poetry.lock` 검사기는 `[[package]]`의 `name`·`version`·유효한 source 형식을 축과 대조하고 `[package.source] type = "git"`의 `reference`·`resolved_reference`를 검사한다. Poetry가 생성하는 최상위 `extras`, legacy source의 `reference`, Git source의 `subdirectory`는 타입을 확인한 뒤 보존하며 판정을 우회하지 않는다. `metadata.python-versions`가 없거나 문자열·범위가 아니면 입력 오류(exit 2)로 닫는다. 40자리 `resolved_reference`는 lock SHA로 확인하지만 선언 branch는 `FLOATING_REF`로 남긴다. `requirements*.txt`의 `-r`·`--requirement`(공백·등호·축약형)는 상대 파일을 재귀 확장하고 순환·누락·미지원 옵션·형식 오류는 exit 2로 닫는다. 인라인 주석과 per-requirement `--hash`는 선언에서 제거한 뒤 검사하며 editable Git도 같은 고정 참조 규칙을 따른다. requirements marker는 알려진 변수·인용 문자열·비교의 조합(and/or)과 역순 비교를 확인하고, 잘못된 연산자·RHS·괄호는 exit 2로 닫는다. URL 대괄호 호스트는 실제 IPv6 주소만 허용해 malformed URL이 보고서에 부동 참조로 남지 않게 한다. `==2.*`·`~=`·교집합 등 지원하는 PEP 440 범위가 `blocked[]`와 겹치면 설치본이 없어도 `BLOCKED`로 보고한다.
- `uv.lock` 검사기는 Python 3.11 표준 라이브러리 `tomllib`으로 schema `version = 1`, `revision` 0~4, 최상위 `requires-python`, `[[package]]`의 이름·버전·`source`(registry/git/editable/directory/virtual)를 제한적으로 읽는다. `resolution-markers`·workspace 관련 메타데이터는 알려진 필드만 허용하고, 미지 schema·source·형식은 exit 2로 닫힌다. uv의 lock 내부 형식은 안정적인 공개 API가 아니므로 이 경계는 [공식 lockfile versioning 문서](https://docs.astral.sh/uv/concepts/resolution/#lockfile-versioning)(2026-07-30 문서 revision)와 [upstream source 3c979abda4530fe9bf3d92e9bcf5c5575e3b3126](https://github.com/astral-sh/uv/blob/3c979abda4530fe9bf3d92e9bcf5c5575e3b3126/crates/uv-resolver/src/lock/mod.rs)에 고정한 검사 범위다. universal lock의 marker별 복수 package와 PEP 735 `dependency-groups`, `tool.uv.sources`의 복수 git 항목을 모두 보고하며, 실제 `uv sync --locked` 성공이나 metadata 해석 결과를 대신하지 않는다.
- 워크스페이스: npm 워크스페이스는 루트 lock 하나가 전 멤버를 해석한다(map·pinvi). 도구는 멤버 `package.json`을 별도 범위로 보고하되 설치본은 `<멤버>/node_modules/<pkg>`부터 각 상위 디렉터리의 `node_modules/<pkg>`를 거쳐 루트까지 찾는다. 직접 선언 대조 뒤 lock 전체의 나머지 축·차단 대상·전이 git/URL 선언과 resolved를 검사한다. 로컬 링크의 축·차단 대상은 NO_LOCK으로 남긴다. npm 이름의 점·밑줄·하이픈을 서로 합치지 않으며 Python 이름만 정규화한다. 전이 행의 scope에는 lock 내부 경로를 붙이며, 명시한 멤버 범위라도 공유 lock 전체를 검사한다. uv의 세부 워크스페이스 해석은 T-005a가 확정한다.
- lock 재생성 사고 방지: `--package-lock-only`로 만든 lock은 `integrity`가 빠질 수 있다(pinvi T-352, `vm` §3.6). 채택 PR은 lock 동반 커밋이 필수다(D-24).

### 3.3 판정 어휘(D-07)

| 판정 | 조건 | report | warn | fail |
|---|---|---|---|---|
| `OK` | floor 이상, max 미만, recommended 접두 일치(범위 선언은 floor·max만) | — | — | — |
| `NOT_RECOMMENDED` | floor 이상이지만 recommended 접두와 다름 | — | `::warning::` | `::warning::`(실패 아님) |
| `BELOW_FLOOR` | 설치본 또는 선언 하한이 floor 미만 | — | `::warning::` | `::error::` + exit 1 |
| `ABOVE_MAX` | 설치본이 max 이상 | — | `::warning::` | `::error::` + exit 1 |
| `NO_LOCK` | lockfile 없음·버전 불일치·lock에 항목 없음·requirements 선언 전용 입력 | — | `::warning::` | `::error::` + exit 1 |
| `NO_ENGINES` | `engines.node`(또는 `requires-python`) 미선언, 하한 없는 범위(`*`) | — | `::warning::` | `::error::` + exit 1 |
| `FLOATING_REF` | git/URL 의존성이 SHA·버전 태그·릴리스 자산으로 고정되지 않음(`@main`, 참조 없음, `semver:` 범위), 직접 npm 선언 `*`/`latest`(워크스페이스 링크 제외) | **`::error::`** | `::error::` | `::error::` + exit 1 |
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

`@main`·branch·참조 없는 git URL, `latest` 태그, npm `*`/`latest` 선언은 `FLOATING_REF`다. 허용되는 고정 형식: 40자리 SHA, GitHub `/tarball|/archive|/commit/<sha>`, GitHub Release 자산 URL(`/releases/download/<tag>/…` — common npm 배포 형식), 버전형 태그(`v1.2.3`, `py-v0.1.0`; `uv.lock`이 SHA를 기록). 관찰된 위반: pinvi `apps/etl` `python-kasi-api@main`(`vm` §2.7), RustFS/mc `latest` 이미지(도구 범위 밖, [ci-deploy](ci-deploy.md)). 재사용 워크플로 참조(`uses: digitie/kor-travel-common/.github/workflows/x.yml@<tag|sha>`)도 같은 규칙이다.

`tools/check_versions.py`는 저장소 루트와 manifest 기준 루트의 `.github/workflows/*.yml`·`*.yaml`에서 job/step의 `uses`를 정적으로 보고한다. `owner/repo@<40자리 SHA|버전형 태그>`는 `OK`, branch·unknown·ref 누락은 `FLOATING_REF`다. `./` local action은 저장소 안의 경로가 존재할 때만 `OK`, `docker://`는 기본 image 이름이 유효하고 버전형 tag 또는 sha256 digest일 때만 `OK`이며 원격 이미지·action의 실제 버전이나 major를 조회·추정하지 않는다. `actions/setup-node`의 정확한 step에 있는 정적 문자열 `with.node-version`만 런타임 하한과 대조하고, matrix·expression·list·비문자열·`node-version-file`은 `NO_ENGINES`다. 위치는 workflow 상대 경로와 원본 행으로 보고한다.

파서는 **2칸씩 증가하는** block map/list·인용/일반 scalar와 **trailing separator 없는** 단순 flow sequence만 지원한다. 이 subset의 plain scalar 예약 문자, single quote의 doubled escape, YAML double-quoted escape를 끝까지 소비하며 잘못된 quote·괄호·alias·colon 구조는 정상화하지 않는다. flow mapping, anchor/alias, block scalar, YAML tag/document stream, 중복 key, tab 들여쓰기와 잘못된 들여쓰기는 일반 입력 오류(exit 2)로 닫는다. job/step에 정적 `uses` 대상이 하나도 없거나 workflow·local 경로가 입력 root 밖으로 symlink된 경우도 빈 성공으로 만들지 않고 입력 오류로 닫는다. 진단·JSON·Markdown·step summary의 workflow 원문·경로는 비밀형 값과 제어 문자를 비식별화한다. 이 오류는 원문 값·경로를 재출력하지 않는다. T-009는 common 자체 workflow의 핀·실행 검증을, T-005c는 이 제한된 정적 보고를 소유한다.

### 3.9 기준선 갱신

- 값 변경(`axes`·`blocked`·`exceptions`·`consumers.enforce`)은 common PR + 2인 리뷰 비면제(D-04) + `CHANGELOG.md` 기록.
- 분기마다(T-506) 최신 안정 버전을 재조회해 `recommended`를 올리고 `floor`는 EOL·보안 floor·peer 제약이 있을 때만 올린다. Node 24/26·Vitest 5·react-table 9·lucide 1.x·mypy 2·TS 7 재평가는 T-507.
- 기준선을 올리면 `baseline`을 `YYYY-MM`으로 바꾸고 변경 이유와 영향받는 축을 CHANGELOG에 기록한다. 과거 기준선은 CHANGELOG에 남기고 레지스트리에 이력을 쌓지 않는다.

## 4. 기준선 값과 축

수치의 유일한 정본은 [`versions.json`](../../versions.json)의 `axes`·`actions`·`providers`·`exceptions`다. 표를 수동 복제하지 않는다. `packages[]`가 있는 축은 여러 npm/Python 이름을 같은 정책으로 묶는다. `checked: false`인 이미지·DB·도구 축은 실제 실행 버전 검사 결과가 아니다.

기준선 결정은 ADR-008과 브리프 D-06에 있으며, 변경 시 §3.9 절차를 따른다. `actions.common`은 사용할 major 정책이고 실제 workflow SHA 대조는 T-009다.

## 5. 소비자 실측

[T-005 고정 입력 보고](../evidence/t005/README.md)는 7개 소비자의 commit·입력 digest·실행 환경·판정 목록을 보존한다. 값은 해당 commit의 관찰이며 현재 배포 상태나 소비자 빌드 성공을 뜻하지 않는다. report exit 0은 정책 준수 증거가 아니며, 이번 위반 결과로 `clean_runs`나 `enforce`를 올리지 않는다.

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

전체 형식과 현재 값은 [`versions.json`](../../versions.json)을 참조한다. 아래는 필드 의미와 검사 계약이다.

| 절 | 필드 | 규칙 |
|---|---|---|
| 머리 | `schema`(고정 문자열)·`baseline`(`YYYY-MM`)·`updated`·`next_review`·`policy`·`source` | schema 고정·문자열·YYYY-MM·ISO 날짜 검사, 미지 필드 exit 2 |
| `axes.<key>` | `ecosystem` ∈ `runtime`/`npm`/`pypi`/`image`/`tool`/`db`(필수), `packages[]`(생략 시 key), `floor`/`recommended`/`max`(문자열 또는 null), `image`, `check`, `checked`(기본 true), `note`, `source` | `runtime` 축은 `engines.node`·`engines.npm`(또는 `packageManager`)·`requires-python`의 **하한**을 대조하고, exact 값이면 recommended까지 대조 |
| `actions` | `consumer_policy`·`common{}`·`checked: false` | 현재 미검사. 정적 참조 보고는 T-005c가 소유하며 SHA의 액션 major 실측과 구분한다 |
| `exceptions[]` | `repo`(consumers 키)·`key`(axes 키)·`installed`(접두)·`reason`·`until`(ISO)·`review` — 6개 모두 필수 | 숫자 접두 일치 시에만 적용; 같은 저장소·축의 중첩 접두는 거부; 다른 설치본이면 무효 |
| `blocked[]` | `ecosystem`·`name`·`range`·`reason`(필수)·`since`·`source` | `range`는 `>=`·`<`·`==`·`,` 조합 |
| `consumers.<repo>` | `enforce`(`report`/`warn`/`fail`)·`clean_runs`·`aliases[]`·`note` | 7개 고정. 신규 소비자는 common PR |
| `providers` | `policy: "report"`·`packages{name:{repo}}`·`note` | 보고 전용. `python-*-api` 패턴은 목록에 없어도 보고 |

형식은 dm 런타임 핀 레지스트리(`schema`·`blocked_pinsets`·"값은 파일이, 계약은 코드가 소유")를 라이브러리 축으로 옮긴 것이다(`vm` §7.3). 소비자 매니페스트(`consumer-manifest.v1`, T-011)는 별도 파일이며 이 레지스트리에 소비자 값을 복제하지 않는다.

## 8. 도구 사용법(`tools/check_versions.py`)

```bash
# 소비 저장소 체크아웃을 자동 탐색(package.json·pyproject.toml·requirements*.txt·.github/workflows/*.yml|*.yaml, 깊이 4, node_modules 제외)
python3 -B -X utf8 tools/check_versions.py /path/to/kor-travel-map --repo kor-travel-map

# 매니페스트의 lockfiles[]와 저장소 루트 workflow를 대조(T-011 이후 CI 표준 호출)
python3 -B -X utf8 tools/check_versions.py /path/to/consumer-repo \
  --manifest /path/to/consumer-repo/<app-dir>/kor-travel-common.lock.json \
  --json report.json --markdown report.md

# 예외 만료를 미리 보기
python3 -B -X utf8 tools/check_versions.py /path/to/app --repo wx --today 2027-01-15
```

- 인자: 위치 인자 = 저장소 루트(여러 개 가능), `--manifest`, `--registry`(기본 common 루트 `versions.json`), `--repo`(consumers 키 또는 별칭; 기본 매니페스트 `repo` → 디렉터리 이름), `--mode`(로컬 override), `--today`, `--json`, `--markdown`, `--no-step-summary`, `--quiet`, `--self-check`(형식·순서·예외 만료). T-011 strict 호출은 저장소 루트와 `--manifest`를 함께 준다.
- 출력: 표준 출력에 Markdown 표(범위·축·생태계·선언·설치·판정·비고) + GitHub annotation(`::error::`/`::warning::`) + 요약 1줄. `--json`은 `kor-travel-common.version-report.v1`. `GITHUB_STEP_SUMMARY`가 있으면 표를 덧붙인다.
- exit: 0(report·warn), 1(fail 모드 실패 후보 존재 또는 `--self-check` 예외 만료), 2(레지스트리·매니페스트·경로 오류). 자체 검사는 소비자 report 모드와 별개로 만료를 실패 처리한다.
- 읽는 것: `package.json`·`package-lock.json`(v3)·`pyproject.toml`(PEP 621·Poetry 선언)·`uv.lock`·`poetry.lock`·`requirements*.txt`(재귀 선언)·`.github/workflows/*.yml|*.yaml`(제한된 정적 YAML). 쓰는 것: `--json`·`--markdown` 출력 파일뿐. 네트워크 없음. Python 3.11+ 표준 라이브러리(`tomllib`)만 쓰며 Windows에서 동작한다(D-03 Tier 2; 회귀 시험 `tests/test_check_versions.py`).
- 한계(사실): Poetry lock은 제한된 package/version·metadata·git source만 읽고 requirements 설치본은 정확 핀 후보와 차단 범위만 보고하며 두 입력 모두 uv lock을 대신하지 않는다. workflow는 §3.8의 제한된 YAML과 `uses`·setup-node 정적 선언만 읽고 실제 실행 버전·액션 major·Docker digest의 이미지 내용을 확인하지 않는다. 지원 밖 YAML·빈 대조 범위·root 밖 symlink는 exit 2, 동적 Node 값은 `NO_ENGINES`, 이동 ref와 기본 구조가 잘못된 Docker/remote target은 `FLOATING_REF`이며 `actions.checked`를 활성화하지 않는다. 실제 실행 버전·Docker 파서는 범위 밖이고 git 고정 판정은 §3.8 휴리스틱이다. 지원 범위는 전체 Poetry resolver·전체 PEP 440 해석기가 아니며 lock과 선언의 만족 여부는 소비자의 `npm ci`·`uv sync --locked` gate가 검증한다. npm 사전 배포 버전·별칭·로컬 링크는 안정 원 패키지와 비교하지 않고 `NO_LOCK`으로 보고한다. npm 설치본은 `major.minor.patch`와 선택적 build metadata만 지원한다. 런타임/정책 숫자 접두와 이미지 `-slim`은 별도 허용한다. 런타임 하한은 단일 숫자와 제한된 비교·compatible·wildcard·교집합·`||` 대안을 지원하며 해석할 수 없는 범위는 안전한 정상 판정으로 축소하지 않는다.
- CI 연동: common `check-versions(report)` job(T-009)과 재사용 워크플로 `versions-check.yml`(T-010). 소비자는 기존 워크플로에 job을 추가하는 방식으로 호출하며 required check 이름은 입력으로 개방한다([ci-deploy](ci-deploy.md)).

## 9. 열린 결정(사용자 확인 필요; 기본값으로 진행)

| # | 결정 | 기본값(이 문서·레지스트리 반영) |
|---|---|---|
| O-5 | 패키지 식별자 | [ADR-014](../adr/014-common-implementation-without-registry-publishing.md)로 확정. 공개 registry 이름 확보 제외 |
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

### 입력 오류와 자체 검사

`check_versions.py --self-check`는 소비자 버전 조회 없이 레지스트리 형식·판정 정책을 검증한다. 모든 정책 객체의 미지 필드, 잘못된 enforce/버전/날짜/예외/차단 값, 뒤집힌 `floor <= recommended < max`, 겹치는 예외 접두와 빈 검사 범위는 입력 오류(exit 2)다. 현재 지원하지 않는 actions의 `checked: true`와 providers의 report 외 정책도 거부한다. 자체 검사에서 `until` 다음 날부터 `EXEMPT_EXPIRED` 주석과 exit 1을 반환한다. 설치 버전 파싱 실패는 axes 밖의 차단 전용 패키지에도 NO_LOCK, 하한 없는 OR 또는 지원하지 않는 런타임 범위는 NO_ENGINES이며 OK로 바꾸지 않는다. URL은 npm 선언의 `#ref`, Python 선언의 `@rev`, uv lock git source의 전체 SHA fragment를 구분해 실제 ref 위치를 해석하고 임의 query·자산 fragment의 SHA를 고정 근거로 삼지 않는다. 지원 파서의 확대와 실제 소비자 대조는 T-005·T-005a·T-005b에서 검증한다.


### npm 입력 형식 근거

2026-09-07 조회: [npm package-lock 문서](https://docs.npmjs.com/cli/v11/configuring-npm/package-lock-json/)(표시 버전 11.19.1)의 packages·link·shrinkwrap 우선순위와 [node-semver README](https://github.com/npm/node-semver/blob/6e05b7637396ac66522cff8731f07cfe0ef49a29/README.md)의 사전 배포 구분을 참고했다. 이 도구는 안정 버전 수치 비교만 구현하며 node-semver 전체 문법 지원을 주장하지 않는다.


### 전이 npm 참조의 범위

전이 패키지의 git/URL 선언은 resolved가 SHA여도 원 선언이 branch이면 FLOATING_REF다. 전이 numeric/wildcard 선언은 lock 설치본으로 대조하고 직접 manifest의 `*`/`latest` 금지와 구분한다. 기본 npm registry의 `/-/<이름>-<설치버전>.tgz` 경로는 registry 설치본으로 분류한다. 그 외 외부 resolved는 §3.8의 고정 참조 규칙을 적용하므로 미지원 사설 registry/mirror는 FLOATING_REF일 수 있다. 실제 파일 다운로드·integrity 검증은 이 읽기 전용 검사기의 성공 주장에 포함하지 않는다.
