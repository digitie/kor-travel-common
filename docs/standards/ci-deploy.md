# kor-travel-common CI·배포·운영 규약

이 문서는 [규칙 문서 색인](README.md)에 속한 재사용 워크플로 계약·CI 하드닝·포트·명명·컨테이너 최소 규약·redaction·common 자체 CI의 정본이다. 정본 지위: **확정 초안** — [브리프](../plan/design-brief.md) D-18·D-03·D-06·D-07을 규칙 ID `CI-n`으로 옮긴 것이며, 워크플로 실물(T-009 하드닝·T-010 1단계·T-309 2단계·T-401 3단계)과 포트 확정(T-014)에서 대조해 확정하는 task가 남아 있다. 마지막 갱신: 2026-09-07, T-009 구현 대조 중.

릴리스 절차(태그·rc·CHANGELOG)는 [release](../runbooks/release.md), 소비자 도입 절차는 [consumer adoption](../runbooks/consumer-adoption.md), 버전 값은 [versions](versions.md)·`versions.json`이 정본이다. 이 문서는 계약과 기본값만 정한다.

## 1. 목표와 기준

- CI가 있는 6개 저장소는 "Python 검사 + Node 검사" 2-job 골격이 같지만 게이트 폭(map·pinvi 10종 이상 ↔ airport·ktdm·weather 3~5종)·도구 버전·npm 핀이 달라 워크플로 파일 복사는 성립하지 않는다(사실: [ci-deploy 횡단 비교](../survey/cross/ci-deploy.md) §1.1·§1.2·§1.15). 따라서 common은 inputs로 폭을 조절하는 `workflow_call` 재사용 워크플로를 배포하고, 앱 기존 워크플로에 job을 **추가**하는 방식으로 도입한다(전면 대체 금지).
- 하드닝 관행은 저장소마다 한 조각씩만 있다(`permissions` ktdm·weather, `concurrency` map·pinvi, `timeout` pinvi, SHA 핀 ktdm, `ubuntu-24.04` ktdm, head SHA checkout pinvi; `ci` §1.3). common 재사용 워크플로는 이 조각을 모두 기본값으로 합성한다.
- 포트·서비스명·env 접두는 정본 이원화를 금지한다. 포트 정본은 ktdm `docs/ports.md` 하나이고 common은 인용만 한다(ktdm `docs/bindings.md` DO NOT 15 원칙).
- 운영 호스트·자격증명은 문서에 넣지 않는다. common 전체 트리는 prod 도메인/IP redaction 대상이다(O-23 기본값).

## 2. 문서 사용법

| 변경 대상 | 상세 정본 |
|---|---|
| 재사용 워크플로 이름·inputs·단계 배포 | 이 문서 §3 |
| 워크플로 하드닝 기본값·액션 버전 | 이 문서 §4, 값은 `versions.json` `actions` 절 |
| 포트 대역·슬롯·sibling 등록 | ktdm `docs/ports.md`(정본), 이 문서 §5(인용·슬롯 명문화) |
| 서비스/컨테이너/이미지/볼륨/네트워크/env 접두 | 이 문서 §6 |
| Dockerfile·compose 최소 규약 | 이 문서 §7 |
| prod redaction·secret scan | 이 문서 §8, 절차는 [agent workflow](../runbooks/agent-workflow.md) §7 |
| common 자체 CI job·branch protection | 이 문서 §9, 현행 파일 [docs.yml](../../.github/workflows/docs.yml) |
| 패키지 릴리스·태그·rc | [release](../runbooks/release.md), D-11·D-31 |
| Python 품질 게이트 내용 | [backend-stack](backend-stack.md) §4 |
| 프론트 품질 게이트 내용 | [frontend-stack](frontend-stack.md) |
| 개발 환경(Windows Tier 2·WSL) | [dev-environment](../dev-environment.md) |
| 결정 이유 | [ADR-003](../adr/003-linux-wsl-canonical-env-windows-tier2-worktree.md)·[ADR-005](../adr/005-release-channel-immutable-tags-semver-0x.md)·[ADR-008](../adr/008-version-alignment-policy.md)([ADR 색인](../adr/README.md)) |

## 3. 재사용 워크플로 계약

### 3.1 호출 규칙

| ID | 규칙 | 근거 |
|---|---|---|
| CI-1 | 호출 형식은 `uses: digitie/kor-travel-common/.github/workflows/<name>.yml@<tag \| sha>`이다. `@main` 등 이동 참조는 금지한다(선행 보고서 §8, D-07 `FLOATING_REF`). 태그 이름은 [release](../runbooks/release.md)가 정한다(후보 `ci-vX.Y.Z`) | `ci` §2.3; D-11 |
| CI-2 | 모든 재사용 워크플로는 `job-name` input을 열어 둔다. 앱은 branch protection·ruleset의 required check 문자열(map 8개·pinvi 5개)과 같은 이름을 넘겨 보전한다 | `ci` §1.1·§2.3; D-18 |
| CI-3 | 도입은 앱 기존 워크플로에 job 추가 방식이다. 앱 고유 job(map `ci.yml` matrix·integration·fixture, pinvi provenance·contract-pin·staleness·e2e·mobile·codex, weather `promtool`, airport `live-e2e`)은 유지한다 | `ci` §2.2 |
| CI-4 | 운영 시스템을 호출하는 job(airport `live-e2e`가 prod 도메인 호출)은 required check로 두지 않기를 권고하고, `workflow_dispatch` 또는 스케줄로 분리한다 | `ci` §1.1·§2.2·열린 질문 10 |
| CI-5 | cross-repo 호출은 common 저장소가 공개(O-15 기본값)라는 전제다. 비공개일 때의 fallback은 `actions/checkout`으로 `repository: digitie/kor-travel-common`, `ref: <tag>`, `path: .kor-travel-common`을 체크아웃하고 `tools/*.py`를 직접 실행하는 방식이며 [consumer adoption](../runbooks/consumer-adoption.md)에 절차를 둔다 | `ci` §2.3 미확인 항목 |
| CI-6 | 재사용 워크플로 변경은 common `workflows-selftest` job(fixture `tests/fixtures/python-app`·`node-app`)을 통과해야 하며 D-04 비면제 대상이다 | `ci` §4 |

### 3.2 단계 배포와 inputs

| 단계 | 워크플로 | 주요 inputs(기본값) | steps | task |
|---|---|---|---|---|
| Phase 1 | `versions-check.yml` | `manifest-path`(`kor-travel-common.lock.json`), `working-directory`, `common-ref`, `job-name` | checkout(head SHA) → common 도구 체크아웃 → `tools/check_versions.py` → Markdown 표 + JSON + `$GITHUB_STEP_SUMMARY`. 모드(report/warn/fail)는 input이 아니라 common `versions.json` `consumers.<repo>.enforce`가 소유(D-07·D-30) | T-010 |
| Phase 1 | `contrast-check.yml` | `tokens-css`, `override-css`, `baseline`(`contrast-baseline.json`), `dark`(bool, 기본 false), `job-name` | `tools/kt_contrast.py` report; 신규 미달만 fail(D-12). `ux_lint`(`tools/ux_lint.py --base <sha>`) 옵션 step은 T-103에서 확정(후보) | T-010 |
| Phase 1 | `docs-check.yml` | `link-check`(true), `redaction-scope`(`docs/`), `redaction-patterns-file`(`.prod-redaction-patterns`), `task-ledger`(false), `job-name` | `tools/validate_document_links.py` → redaction guard(패턴 파일 입력) → `tools/validate_plan.py`(조건) | T-010 |
| Phase 3 | `openapi-drift.yml` | `python-version`, `installer`(`uv`), `install-args`, `export-command`, `spec-paths`(list), `mode`(`check` \| `git-diff`), `job-name` | install → export → `--check` 또는 `git diff --exit-code -- <spec-paths>` | T-309 |
| Phase 3 | `typegen-drift.yml` | `node-version`(22), `npm-version`(빈값=동봉), `working-directory`, `check-command`(`npm run gen:types:check`), `job-name` | setup-node → `npm ci --no-audit --no-fund` → check-command | T-309 |
| Phase 4 | `node-quality.yml` | `node-version`(22), `npm-version`, `working-directory`, `workspaces`(bool), `lockfile-integrity`(bool), `audit-level`(`high`), `ignore-scripts`(bool), `lint-max-warnings`(0), `typegen-check-command`, `test`(bool), `build-env`(JSON), `pre-lint-command`, `job-name` | checkout → setup-node(cache) → npm 핀(조건) → lockfile integrity(설치 전) → `npm ci` → `npm audit --audit-level=high --omit=dev`(차단) + dev 포함(비차단) → typegen(조건) → pre-lint 훅 → lint → type-check → test → build | T-401 |
| Phase 4 | `python-quality.yml` | `python-version`(3.12), `working-directory`, `installer`(`uv`), `install-args`, `pre-install`, `ruff-format`(bool), `mypy-targets`, `import-linter`(bool), `alembic`(bool), `pytest-args`, `coverage-fail-under`, `db-image`, `db-env`, `post-test-command`, `job-name` | checkout → setup-python → setup-uv(조건) → pre-install → install(`--locked`) → `ruff check` → `ruff format --check`(조건) → mypy(조건) → lint-imports(조건) → alembic `upgrade head` + `check`(조건) → pytest → post-test | T-401(concierge CI 신설 T-451 선행) |

`docker-build.yml`·`aggregate-gate.yml`·`secret-scan.yml`은 `ci` §2.1 후보이며 Phase 4 이후 수요가 확인될 때 추가한다(T-508 재평가 대상 아님, T-401 범위 판단).

### 3.3 호출 예시

앱 워크플로에 job을 추가하는 형태다. `uses:`는 태그(또는 SHA)로 고정하고 `job-name`으로 required check 이름을 보전한다.

```yaml
jobs:
  backend:            # 앱 고유 job은 그대로 둔다
    # ...
  versions-check:
    uses: digitie/kor-travel-common/.github/workflows/versions-check.yml@ci-v0.1.0
    with:
      manifest-path: kor-travel-common.lock.json
      job-name: versions-check
  openapi-drift:
    uses: digitie/kor-travel-common/.github/workflows/openapi-drift.yml@ci-v0.1.0
    with:
      installer: uv
      install-args: --locked --extra dev
      export-command: python -m kortravelcommon.openapi export --app kortravelweather_api.app:app --output packages/kor-travel-weather-api/openapi.json --check
      spec-paths: packages/kor-travel-weather-api/openapi.json
      mode: check
      job-name: openapi-drift
```

### 3.4 앱별 도입 변경점(`ci` §2.2 요약)

| 앱 | 유지할 앱 고유 job | 재사용 워크플로 | 선행 변경 | task |
|---|---|---|---|---|
| airport | `live-e2e`(required 제외 권고) | python-quality(uv, alembic ON)·node-quality(22)·openapi-drift·docs-check | ruff 설정 신설, prod 도메인 placeholder 치환, `*.local.md` gitignore | T-433·T-482 |
| concierge | 없음(CI 신설) | python-quality·node-quality·docs-check·secret-scan | `.github` 신설, ruff 신설, production `frontend/Dockerfile`, uv lock | T-450·T-451 |
| ktdm | 없음 | python-quality(uv 전환 후)·node-quality(20→22) | SHA 핀 관행 유지 | T-470·T-471 |
| geo | 없음 | python-quality(GDAL `pre-install`, import-linter·mypy ON)·node-quality(20→22, typegen)·openapi-drift(check) | `openapi.yml` 통합, pre-commit `language: system` 전환 | T-440·T-483 |
| map | `ci.yml` matrix·integration·fixture, `lint.yml` ledger·D2 lane, `docker-images.yml`, `postgis-only.yml` | openapi-drift·docs-check(redaction 이관)·node-quality(npm 12.0.1 입력, `pre-lint-command`로 `verify:*`) | required check 8개 이름 보전 | T-410·T-413 |
| weather | `promtool`(`post-test-command`) | python-quality(uv, alembic ON)·node-quality(20→22, test ON)·openapi-drift(git-diff → check) | README·compose 도메인 redaction 결정 | T-460·T-481 |
| pinvi | provenance·contract-pin·staleness·e2e·mobile·codex | node-quality(npm 11.19.1, lockfile, workspaces)·python-quality(ruff format ON, PostGIS) | required check 5개 이름 보전, path 필터 이중 선언 정리 | T-484 |

## 4. 하드닝 기본값

| ID | 기본값 | 선례 |
|---|---|---|
| CI-7 | `permissions: contents: read`를 워크플로 최상위에 두고 쓰기 권한은 job 단위로만 연다 | ktdm·weather top-level, pinvi `permissions: {}` + job write(`ci` §1.3) |
| CI-8 | `concurrency: { group: <name>-${{ github.workflow }}-${{ github.ref }}, cancel-in-progress: true }` | map 5개·pinvi 전부 |
| CI-9 | 모든 job에 `timeout-minutes`(기본 30; docker 60·postgis 30 허용) | pinvi 전 job 10~45 |
| CI-10 | `runs-on: ubuntu-24.04` 고정(`ubuntu-latest` 금지 — 러너 이미지 갱신에 무방비). common `tools` job은 `windows-2025` 매트릭스 추가(D-03 Tier 2) | ktdm; 6곳 `ubuntu-latest` |
| CI-11 | PR에서는 `ref: ${{ github.event.pull_request.head.sha \|\| github.sha }}`로 head SHA를 체크아웃한다(merge ref 아님) | pinvi web/etl/api |
| CI-12 | 액션 참조는 `owner/repo@<40자 SHA> # vX.Y.Z` 형식으로 SHA 핀 + 주석 버전. common 내부 기준은 `actions/checkout` v7·`actions/setup-node` v7·`actions/setup-python` v7·`astral-sh/setup-uv` v10(값은 `versions.json` `actions` 절). 소비자는 현행 major 유지 + SHA 핀 권고(D-06) | ktdm SHA 핀; 최신값 `vm` §4.4 |
| CI-13 | `secrets.*`는 원칙적으로 0개다. CI 더미값(DB 접속 문자열·`NEXT_PUBLIC_*`)은 평문 허용하되 실제 운영값과 달라야 하고 redaction guard 대상이다 | pinvi repository secret 0개 문서화(`ci` §1.3·§1.11) |
| CI-14 | 캐시는 `setup-node` npm cache·`setup-uv` `enable-cache`만 쓰고 `node_modules`·`.venv` 자체를 캐시하지 않는다 | `ci` §1.3 |
| CI-15 | 설치 명령은 lock을 소비한다: `npm ci --no-audit --no-fund`(선택 `--ignore-scripts`), `uv sync --locked`. `npm install`·`pip install -e`는 CI에서 금지 | weather `--ignore-scripts`·`--locked`(`ci` §1.1·§1.5); [backend-stack](backend-stack.md) BE-2 |

### 4.1 골격 예시

재사용 워크플로와 common 자체 워크플로가 공유하는 머리 부분이다(`<sha>`는 자리이며 실제 값은 `versions.json` `actions` 절에서 가져온다).

```yaml
name: python-quality
on:
  workflow_call:
    inputs:
      job-name: { type: string, default: python-quality }
      python-version: { type: string, default: "3.12" }
permissions:
  contents: read
concurrency:
  group: python-quality-${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
jobs:
  quality:
    name: ${{ inputs.job-name }}
    runs-on: ubuntu-24.04
    timeout-minutes: 30
    steps:
      - uses: actions/checkout@<sha> # v7.0.1
        with:
          ref: ${{ github.event.pull_request.head.sha || github.sha }}
      - uses: actions/setup-python@<sha> # v7.0.0
        with:
          python-version: ${{ inputs.python-version }}
      - uses: astral-sh/setup-uv@<sha> # v10.0.1
        with:
          enable-cache: true
```

## 5. 포트 규칙

| ID | 규칙 | 근거 |
|---|---|---|
| CI-16 | **정본은 ktdm `docs/ports.md`** 하나다: `12000 + dependency index × 100 + offset`, DB `+0`, API `+1`, `+2`부터 추가, Web UI `+5`, Manager `12900~12999`. common은 이 규칙을 인용만 하고 값을 복제하지 않는다. 대역 신설·변경은 ktdm PR로만 한다 | ktdm `docs/ports.md`, `AGENTS.md` DO NOT 4·9([ktdm 인벤토리](../survey/inventory/kor-travel-docker-manager.md) §1-6); `ci` §1.9 |
| CI-17 | 슬롯을 명문화한다(정본 규칙의 보강, ktdm 등록 요청 T-014): `00` DB, `01` API(+`/metrics` 동일 포트), `02` worker/Dagster/MCP, `03` 보조 metrics/exporter(weather 14103 선례), `04` 관측 로컬 예약, `05` Web, `06~09` 추가 Web/BFF, `10~99` 임시·E2E(pinvi 12855 선례) | `ci` §3.1-2 |
| CI-18 | 컨테이너 내부 포트는 호스트 포트와 **동일**하게 listen한다(geo·map·weather 선례; host 네트워크 전제). 내부 8000/3000 + 매핑(airport·concierge·pinvi api/web)은 예외로 소비자 매니페스트 `exceptions[]`에 등록 | `ci` §1.6 집계 |
| CI-19 | sibling 대역 `140xx` kor-travel-airport·`141xx` kor-travel-weather를 `docs/ports.md` 표에 명시 행으로 등록 요청한다(현재 weather는 문장, airport는 없음). airport web `14002`(`+5` 규칙 이탈)는 예외 등록이 기본안(O-24; 14005 이전은 HAProxy·CORS·`require_exact` 변경 비용) | `ci` §1.9 충돌 (b)·(d), §3.1-3; T-014 |
| CI-20 | common 테스트가 필요하면 `13001`·`13005` 등을 실행 시 임시 주입할 수 있다. 이는 common 운영 대역·서비스 등록·포트 소유권을 뜻하지 않으며 ktdm `docs/ports.md`에는 등록하지 않는다. 소비자 운영 대역은 각 소비자와 ktdm 정본이 소유한다(T-014) | `ci` §3.1-4·T-014·ADR-015 |
| CI-21 | 컨테이너명 `-latest` 접미 제거 여부는 ktdm 결정이다(ktdm `docker-targets.yml`·registry 테스트·geo `docker_app.sh`가 참조). common은 `<project>-<role>[-<lane>]` 형식만 권고 | `ci` §3.2·열린 질문 4; O-24 |

인용용 현행 대역표(사실, `ci` §1.9; 값은 ktdm `docs/ports.md`가 정본):

| 대역 | 소유 | `+0` DB | `+1` API | `+2` | `+3` | `+5` Web |
|---|---|---|---|---|---|---|
| `121xx` | RustFS | — | 12101 S3 | — | — | 12105 console |
| `122xx`~`124xx` | Grafana 12205 · cAdvisor 12301 · Prometheus 12401 | | | | | |
| `125xx` | kor-travel-geo | 12500 | 12501 | 12502 Dagster | — | 12505 |
| `126xx` | kor-travel-concierge | 12600 | 12601 | 12602 MCP | — | 12605 |
| `127xx` | kor-travel-map | 12700 | 12701 | 12702 Dagster | — | 12705 |
| `128xx` | PinVi | 12800 | 12801 | 12802 Dagster | — | 12805 |
| `129xx` | docker-manager | — | 12901 backend | — | — | 12905 |
| `140xx` | kor-travel-airport(미등록) | 14000 | 14001 | **14002 web**(예외) | — | — |
| `141xx` | kor-travel-weather(문장만) | 14100 | 14101 | 14102 gateway | 14103 metrics | 14105 |
| `130xx` | common 테스트 fixture(운영 등록 없음) | — | 실행 시 주입 | — | — | 실행 시 주입 |

## 6. 명명 표준

`ci` §3.2를 채택한다(D-18). 이름 변경은 각 앱 스크립트(`verify-docker-compose.sh`·`deploy-server14.sh`·`docker-app.sh`)의 서비스 참조 수정을 동반해야 하며, 변경 비용이 큰 기존 이름은 매니페스트 예외로 등록한다.

| ID | 대상 | 표준 | 기존과의 관계 |
|---|---|---|---|
| CI-22 | 앱 자체 compose 서비스명 | 짧은 역할명 고정 어휘: `postgres`, `api`, `web`, `dagster`, `dagster-daemon`, `mcp`, `scheduler`, `migrate`, `rustfs`, `rustfs-init`, `prometheus`, `grafana`, `cadvisor`, `backup` | airport `backend/frontend` → `api/web`, weather `db` → `postgres`, concierge `frontend` → `web`, pinvi `app-*` 접두는 `-p`로 구분 |
| CI-23 | ktdm 통합 compose 서비스명 | `<project>-<role>`(`kor-travel-geo-api`, `pinvi-web`) 현행 유지 | 이미 일관 |
| CI-24 | `container_name` | `<project>-<role>[-<lane>]`, 항상 `${<PREFIX>_<ROLE>_CONTAINER:-…}` env override 가능(ktdm 선례). `-latest` 접미는 CI-21 | ktdm·geo·pinvi 일부 |
| CI-25 | 이미지명 | `<project>-<role>:<tag>`; tag 어휘 `latest-main`(로컬 최신 main 빌드), `local`(작업 트리), `ci-<sha>`(CI 검증). 배포 단위는 digest 또는 ktdm runtime pin revision이지 tag가 아니다. 변형 접미(`-gdal`)는 `<role>` 뒤 | ktdm·geo·pinvi 현행 일치 |
| CI-26 | 볼륨 | `<project>-<purpose>`(`kor-travel-map-postgres`); 유산 볼륨은 `name:`으로 고정(airport 선례) | `pinvi-pgdata` → `pinvi-postgres`, `weather-postgres` → `kor-travel-weather-postgres` 후보 |
| CI-27 | 네트워크 | bridge는 `<project>-net`(airport·geo 선례); host 모드는 `network_mode: ${<PREFIX>_DOCKER_NETWORK_MODE:-host}` env 스위치 | map `admin-control`은 목적 네트워크 예외 |
| CI-28 | compose 프로젝트명 | 파일 `name: <project>[-<stack>]`(airport 선례). 디렉터리명 의존 금지 | map·weather·pinvi·concierge 추가 대상 |
| CI-29 | health 경로 | `/health`(liveness) + `/readyz`(readiness) + `/version` — [openapi](openapi.md) M5 | geo `/v1/healthz` 별칭 병행 |
| CI-30 | env 접두 | 앱당 단일 접두 필수. 신규 `KOR_TRAVEL_<APP>_`, 기존 `KTG_`·`KTC_`·`KTDM_`·`PINVI_` 유지. 브라우저 노출은 `NEXT_PUBLIC_<접두>`·`EXPO_PUBLIC_<접두>`. compose 인프라 키(`POSTGRES_*`·`RUSTFS_*`)와 외부 API 키(`KMA_API_KEY` 등)는 예외 목록 | airport 접두 없음 44키·concierge 혼합 정리 대상(`ci` §1.11); [backend-stack](backend-stack.md) BE-12 |
| CI-31 | 약칭 | `kta`, `ktc`, `ktdm`, `geo`(env `KTG`), `map`(env `KOR_TRAVEL_MAP`), `wx`(env `KOR_TRAVEL_WEATHER`), `pinvi`; ktdm target id(`geo/conc/map/pinvi`)는 별칭 테이블 | ktdm `aliases` 필드 |
| CI-32 | ktdm `.env.example`의 앱 키 사본(`KOR_TRAVEL_MAP_*` 52 등)은 각 앱 `.env.example`에서 생성·검증하는 결박이 필요하다(cross-repo, ktdm `bindings.md` U-1 계열). common은 요청만(T-505 계열 문서) | `ci` §1.14·열린 질문 8 |

## 7. Dockerfile·compose 최소 규약

`ci` §3.3을 채택한다. 현재 충족률은 멀티스테이지 9/18, non-root 4/18, `HEALTHCHECK` 3/18, digest 핀·OCI 라벨은 map·pinvi만이다(사실, `ci` §1.6). ktdm은 컨테이너가 아니라 systemd+venv 실행이므로 예외다.

| ID | 규칙 | 선례 |
|---|---|---|
| CI-33 | 멀티스테이지 + 최종 스테이지 non-root(`groupadd --system` / `useradd --system … --shell /usr/sbin/nologin`) | map 3·geo dagster |
| CI-34 | `HEALTHCHECK`는 Dockerfile 또는 compose 중 **한 곳**. 명령은 이미지에 이미 있는 런타임으로(`python -c urllib`, `node -e fetch`, `pg_isready -p <port>` — `-p` 누락 시 영원히 unhealthy) | pinvi Dockerfile, ktdm compose 12종 |
| CI-35 | 베이스 이미지는 `<image>:<tag>@sha256:<digest>` 병기. `latest` 참조 금지(RustFS/mc `latest`는 정리 대상) | map·pinvi digest; `vm` §3.4 |
| CI-36 | OCI 라벨 `org.opencontainers.image.revision` 필수, `org.opencontainers.image.licenses=GPL-3.0-or-later`([licensing](licensing.md) §6) | map·pinvi |
| CI-37 | 빌드는 lock을 소비한다(`uv sync --locked --no-dev`, `npm ci`). dev 서버 이미지(`CMD npm run dev`)를 production으로 쓰지 않는다 | concierge `frontend/Dockerfile`은 T-451에서 production Dockerfile 추가 |
| CI-38 | `.gitattributes`는 `* text=auto eol=lf` + 바이너리 목록(map·weather·pinvi·common 동일). airport(`*.sh`만)·geo(확장자 열거) 정렬 | 현행 [.gitattributes](../../.gitattributes) |
| CI-39 | 배포 후 검증 의무(`/health` 200 + 로그인 왕복 또는 앱별 동등 검사)를 각 앱 runbook에 두기를 권고한다(weather `AGENTS.md`에 없음). common은 문구를 강제하지 않는다 | `ci` §1.10·열린 질문 12 |

## 8. redaction·secret scan

| ID | 규칙 | 근거 |
|---|---|---|
| CI-40 | common의 추적 파일과 ignore되지 않은 새 파일 전체를 `check_prod_redaction.py --all`로 검사한다. `.prod-redaction-patterns`에 사설 IPv4/IPv6·내부 호스트·운영 서비스/DNS의 일반 형식을 정규식으로 둔다. 실제 운영 값은 패턴에도 쓰지 않는다. 소비자는 opt-in | D-18·T-009 |
| CI-41 | `docs/survey/**`도 검사한다. 과거 조사에 남은 민감 값은 [보안 정정 기록](../survey/README.md#9-t-009-보안-정정)에 따라 placeholder로 치환하고 기준 커밋·나머지 조사 사실은 보존한다. 디렉터리 전체 제외는 허용하지 않는다 | AGENTS 비밀·운영 정보 금지, T-009 |
| CI-42 | `scan_secrets.py`는 `.secret-scan-patterns`의 값 형태·개인키·제공자 token/hash·URL 자격증명 패턴으로 차단한다. 필드명만 찾는 기존 보안 grep은 수동 감사 보조이며 자동 fail 기준과 구분한다. 원문은 출력하지 않고 파일·행·규칙 ID만 출력한다. `.env.example`에는 placeholder만 둔다 | D-18·T-009 |
| CI-43 | `git add -A`·`git add .` 금지, staged diff 직접 읽기, 경로별 명시 stage — 절차는 [agent workflow](../runbooks/agent-workflow.md) §7 | canview A8.4; geo·canview 선례 |
| CI-44 | `.gitignore`에 `.env`, `.env.*`, `!.env.example`, `*.local.md`, `*.local.sh`가 있어야 한다. airport는 `*.local.md` 항목이 없다(T-433) | `ci` §1.11; 현행 `.gitignore` |
| CI-45 | GitHub Actions secret은 0개가 원칙이며 `github.token`만 쓴다. 외부 저장소 체크아웃이 필요하면 공개 저장소 + 태그 참조로 해결한다 | pinvi `secrets.md`, map `GITHUB_TOKEN` 선택 |

### 8.1 검사 범위와 실패 처리

두 CLI는 Python 3.11 표준 라이브러리와 Git만 사용한다. 기본/`--all`은 추적 파일 및 ignore되지 않은 새 파일의 현재 내용, `--staged`는 변경 파일의 index blob, `--base <commit>`은 해당 commit과 HEAD 사이 변경 파일의 HEAD blob을 검사한다. 변경 파일 전체를 읽으며 삭제된 파일과 삭제된 행은 성공 근거로 세지 않는다. 빈 변경 범위는 exit 2·NOT_RUN이다.

정책 파일도 같은 스냅샷에서 읽는다. unstaged 수정으로 staged 비밀이나 정책을 가리는 것을 막는다. `--patterns`는 저장소 상대 경로이며 기본 파일을 바꿀 때는 정책 diff도 두 독립 리뷰 대상이다. Git 추적 밖의 무시된 로컬 파일·과거 commit 전체는 검사 범위가 아니다.

패턴 파일은 TOML `version = 1`, `[[patterns]]`의 고유 `id`·`regex`를 갖는다. 예외가 필요한 경우 `[[allowlist]]`의 정확한 `path`·`rules`·한국어 `reason`을 검토받는다. wildcard·없는 파일·없는 규칙·빈 사유는 오류다. 파일 내용 전체를 읽되 허용된 규칙의 일치 수를 별도 표시한다. 현재 예외는 없다.

exit 0은 선택 범위의 패턴 일치가 없거나 명시적 예외로 처리됐다는 뜻이다. 발견은 exit 1, Git/경로/정책/읽기/UTF-8/NUL 오류는 exit 2다. 심볼릭 링크·junction·submodule·바이너리는 조용히 건너뛰지 않고 오류로 처리한다. 예약 호스트 `host.docker.internal`·`gateway.docker.internal`, loopback·문서 예시 주소 대역은 운영 주소 패턴과 구분한다.

선택한 정책의 패턴에 파일명·부모 디렉터리를 포함한 경로가 일치하면 본문·allowlist와 무관하게 원문 없는 입력 오류(exit 2)로 중단한다. 그 실행의 발견 목록도 출력하지 않는다. 정책 정규식의 컴파일 깊이 초과는 traceback 없이 같은 입력 오류로 처리한다. 경로 검사도 선택한 패턴의 범위 안에서만 보장한다.

정규식은 모든 비밀·도메인을 식별하는 보증이 아니다. 분할·암호화된 값, 새 제공자 형식과 업무 맥락은 staged diff 수동 감사와 독립 리뷰로 보완한다. source나 패턴 파일에 실제 값을 복사해 탐지 규칙을 만들지 않는다.

## 9. common 자체 CI

현행 구현: [docs.yml](../../.github/workflows/docs.yml)의 docs·tools(두 OS)·secret-scan·check-versions. checkout/setup-python은 공식 release commit SHA로 고정하고 권한·동시 실행·timeout·명시 source 확인을 적용했다. 실제 CI gate 결과는 [T-009 evidence](../tasks/T-009-ci-hardening.md#evidence)에 기록한다.

| job | 트리거 | 내용 | 러너 | task |
|---|---|---|---|---|
| `docs` | PR, push `main`·`codex/release-*` | `validate_document_links.py` → `validate_plan.py` → `unittest discover -s tests -p "test_*.py"` → `git diff --check` → redaction 전체 트리(CI-40) | ubuntu-24.04 | T-002·T-009 |
| `tools` | PR, push `main`·`codex/release-*` | validator·unittest·check_versions 자체 검사·SPDX·secret/redaction(토큰 도구는 T-103 구현 후) | ubuntu-24.04 + windows-2025 매트릭스(D-03) | T-009 |
| `workflows-selftest` | PR(`.github/**`) | 재사용 워크플로를 fixture로 호출 | ubuntu-24.04 | T-010 |
| `packages` | PR, push `main`·`codex/release-*` | `npm install -g npm@11.19.1` → `npm ci` → **커밋 생성물 `check`** → build → `check` → 생성물 Git diff → test → `npm pack` → 임시 디렉터리 tarball 설치. UI가 추가되면 T-201 승인 범위에서 webpack·Turbopack `next build` 스모크를 덧붙인다(D-10) | ubuntu-24.04 | T-101·T-201 |
| `python-package` | PR, push `main`·`codex/release-*` | `uv build` → wheel 설치 → import 스모크 → starlette 0.4x/1.6 매트릭스 | ubuntu-24.04 | T-302 |
| `consumer-smoke` | `workflow_dispatch`; 주간은 T-010a 검증 뒤 활성화 | `consumers.pins.json`(role·url·revision, ktdm runtime pin 형식) 패키지별 승인 소비자의 pinned SHA 체크아웃 → tarball 설치 → type-check + `next build` | ubuntu-24.04 | 실행기 T-010, 외부 dispatch T-010a |
| `secret-scan` | PR, push `main`·`codex/release-*` | CI-42 패턴 | ubuntu-24.04 | T-009 |
| `check-versions` | PR, push `main`·`codex/release-*` | `tools/check_versions.py` report 모드(`FLOATING_REF`·`BLOCKED`·`EXEMPT_EXPIRED`는 `::error::`) | ubuntu-24.04 | T-005·T-009 |

**릴리스 후보에도 필요한 실행 경로(ADR-014)**: `docs`·`tools`·`secret-scan`·`check-versions` 및 존재하는 `packages`·`python-package`는 PR 외에 `main`과 `codex/release-*` push에서도 실행한다. release push에서는 path filter나 PR 전용 조건으로 필수 job을 생략하지 않고 `github.sha`의 실제 merge commit을 checkout한다. run의 head SHA와 build/artifact source SHA가 릴리스 evidence의 `RELEASE_SHA`와 같아야 한다. PR head 성공은 다른 merge SHA의 실행으로 세지 않는다. 아래 구현 task가 이를 적용하고, 후보 보존 전에 실행 경로를 확인해야 과거 후보에서 분기한 release branch에서도 사용할 수 있다. 현재 packages/python-package의 미구현은 NOT_RUN이며 해당 발행을 차단한다. T-009의 기반 job은 실제 PR·release push run으로 검증한다.

- T-009: docs·tools(두 OS)·secret-scan·check-versions의 push 실행과 SHA evidence.
- T-101: 같은 push에서 tokens/UI `packages` 검증과 artifact source 기록(T-201에서 UI 추가).
- T-302: 같은 push에서 Python 지원/extras 매트릭스·wheel 검증과 artifact source 기록.

branch protection의 실제 check 이름과 설정 절차는 [branch protection](../runbooks/branch-protection.md)에 있다. T-009는 설정 문서만 작성하며 원격 ruleset을 적용하지 않는다. check-versions의 표는 [고정 fixture](../../tests/fixtures/version-report/README.md)이며 소비자 실측으로 세지 않는다. 모든 job summary에는 실제 checkout source SHA가 기록된다.

### 9.1 `consumers.pins.json` 형식(후보, T-010)

ktdm runtime pin 레지스트리(`kor-travel-docker-manager.runtime-pin-registry.v1`)의 `sources[]{role,url,revision}` 형식을 따른다(`vm` §7.3). 갱신은 PR로만 하고 `revision`은 40자 SHA다.

```json
{
  "schema": "kor-travel-common.consumer-pins.v1",
  "updated": "2026-09-06",
  "sources": [
    { "role": "map-admin", "url": "https://github.com/digitie/kor-travel-map", "revision": "<40-hex>", "path": "packages/kor-travel-map-admin/frontend" },
    { "role": "pinvi-web", "url": "<pinvi 저장소 URL>", "revision": "<40-hex>", "path": "apps/web" }
  ]
}
```

`tools/collect_manifests.py`(T-012)가 같은 파일을 읽어 [integration map](../integration-map.md)을 생성한다(D-19).

## 10. 릴리스 참조

패키지별 태그(`tokens-vX.Y.Z`·`ui-vX.Y.Z`·`py-vX.Y.Z`), `-rc.N` → 소비자 PR 검증 → 정식, GitHub Release 자산 tarball/wheel + `SHA256SUMS`, 태그 불변·재발행 금지, CHANGELOG 단일 파일 패키지별 H3(D-11·D-18·D-31). 절차와 되돌리기 리허설(T-501)은 [release](../runbooks/release.md)가 정본이다.

## 11. 검증 gate

| gate | 검사 | 실패 조건 |
|---|---|---|
| 워크플로 하드닝 | 재사용 워크플로·common 워크플로의 §4 기본값 존재(`workflows-selftest`가 YAML 정적 검사) | `ubuntu-latest`, SHA 미핀, `permissions` 누락, `@main` 참조 |
| 포트 | 소비자 매니페스트 `exceptions[]`의 내부 포트 예외, ktdm `docs/ports.md` 등록 상태(T-014 evidence) | 미등록 대역 사용 |
| 명명 | 신규 compose 파일의 CI-22·CI-28·CI-30 준수(리뷰 체크리스트) | 접두 2개 이상, 디렉터리명 의존 프로젝트 |
| 컨테이너 | Dockerfile CI-33~CI-37(리뷰 체크리스트; `docker-build.yml` 도입 시 자동) | non-root 아님, digest 없음, `latest` |
| redaction·secret | CI-40·CI-42 | 패턴 일치 |

## 12. 열린 결정

| # | 항목 | 기본값 | 상태 |
|---|---|---|---|
| O-15 | common 공개 여부·cross-repo 호출 | 공개(GPL) 전제 + 체크아웃 fallback 문서 | 열림(사용자 확인 필요) |
| O-17 | Windows 지원 tier | Tier 2(도구·validator + CI windows job) | 열림(사용자 확인 필요) |
| O-23 | prod redaction 범위 | common 전체 트리, 소비자 opt-in | 열림(사용자 확인 필요) |
| O-24 | airport 14002·`-latest` | airport 14002 예외; `-latest`는 ktdm. common `130xx`는 운영 등록 없이 fixture 실행 시 주입 | 열림(사용자 확인 필요) |
| — | 외부 secret 스캐너 채택 | 미채택(grep 패턴) | 후보(`ci` 열린 질문 6) |
| — | arm64/odroid 대상 | common CI는 amd64만 | 후보(`ci` 열린 질문 7) |
| — | Prometheus major(v2.53 vs v3.5)·scrape 결선(ktdm에 map·concierge·pinvi job 없음) | ktdm 소유, common 규약 밖 | 후보(`ci` 열린 질문 9; 매트릭스 D39) |

## 13. 근거

- [브리프](../plan/design-brief.md) D-03·D-06·D-07·D-10·D-11·D-18·D-19·D-30·D-31·O-15·O-17·O-23·O-24.
- [ci-deploy 횡단 비교](../survey/cross/ci-deploy.md) §1.1~§1.15(현행 사실), §2.1~§2.3(재사용 워크플로 후보·도입 변경점·제약), §3.1~§3.3(포트·명명·컨테이너 초안), §4(common 자체 CI), 열린 질문 1~12.
- [version-matrix 횡단 비교](../survey/cross/version-matrix.md) §3.1~§3.6(Actions·CI 런타임·이미지·pre-commit·lock 검증), §4.4(액션 최신값), §7.2~§7.4.
- [docs-conventions 횡단 비교](../survey/cross/docs-conventions.md) §1.16(보안 감사 절차·grep 패턴), §1.17(`*.local.md`·`.env`).
- [ktdm 인벤토리](../survey/inventory/kor-travel-docker-manager.md) §1-6·§6(포트 정본·`docker-targets.yml`·runtime pin·bindings).
- [canview 구조 체크리스트](../survey/cross/canview-structure-checklist.md) §1.3(현행 docs.yml 결과), §2.8 A8.4.
- [공통화 매트릭스](../survey/commonality-matrix.md) §2.6·§4.2 D31·D32·D39.
