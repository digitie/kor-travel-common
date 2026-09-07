# 횡단 비교 — CI·배포·운영 규약

kor-travel 계열 7개 저장소의 GitHub Actions, pre-commit, npm 검증 스크립트, Dockerfile, docker compose 체계, 포트 대역, prod(n150) 런북 관례, 시크릿·env 처리, 백업/복원, 관측, docker-manager 레지스트리를 저장소에서 직접 읽어 비교하고, `kor-travel-common`이 배포할 공통 CI 템플릿·명명 표준·자체 CI 구성을 후보로 제시한다.

표기: **사실** = 기준 커밋의 파일에서 직접 확인. **후보** = 설계 제안(결정 아님). **추정** = 파일 근거가 간접적. **미확인** = 이번 조사에서 확인하지 못함.

## 0. 기준 (조사 커밋)

| 저장소 | 체크아웃 경로 | 커밋 | 약칭 |
|---|---|---|---|
| kor-travel-airport | `F:/dev/kor-travel-common-survey/kta-main` | `2bb1111` | kta |
| kor-travel-concierge | `F:/dev/kor-travel-concierge` | `7945305` | ktc |
| kor-travel-docker-manager | `F:/dev/kor-travel-common-survey/ktdm-main` | `862562d` | ktdm |
| kor-travel-geo | `F:/dev/kor-travel-geo-fixes` | `1d9d74d` | geo |
| kor-travel-map | `F:/dev/kor-travel-common-survey/ktm-main` | `c494e227` | map |
| kor-travel-weather | `F:/dev/kor-travel-weather` | `6003da9` | wx |
| pinvi | `F:/dev/kor-travel-common-survey/pinvi` | `9af25e5` | pinvi |
| kor-travel-common (새 저장소) | `F:/dev/kor-travel-common` | `b92fabe` (브랜치 `feat/bootstrap-survey-and-integration-plan`, 미추적 파일 포함) | common |
| canview (구조 참조) | `F:/dev/canview` | — (`.github` 없음, 사실) | — |

조사일 2026-09-06. 모든 명령은 읽기 전용(`git ls-files`, `git grep`, `cat/sed/grep`)이며 조사 대상 저장소에는 아무것도 쓰지 않았다.

## 방법

- 기존 조사 문서 재사용: `inventory/*.md` §6(CI·배포·운영), `cross/version-matrix.md` §3(도구·CI·컨테이너 매트릭스)·§5.1, `cross/backend.md` §2.5·§2.13·§2.17, `cross/docs-conventions.md` §1.15~§1.17·§1.19, `cross/openapi.md` §2.11. 이 문서들의 사실은 아래에서 "(재확인)" 표시가 있으면 저장소에서 다시 읽었고, 없으면 해당 문서 절 번호를 인용했다.
- 워크플로: 7개 저장소의 `.github/workflows/*.yml` 전부(총 18개, 2,078줄)를 읽었다(pinvi `api.yml` 473줄은 job/step 구조와 트리거만).
- Dockerfile 18개 전부에서 `FROM/USER/HEALTHCHECK/EXPOSE/LABEL/ARG/--mount` 행을 추출했다.
- compose 파일 15개에서 `name/services/networks/volumes/secrets/x-anchor/container_name/network_mode/profiles/ports/healthcheck` 행을 추출했다(ktdm 1,522줄, map 773줄 포함).
- `.env.example` 17개에서 키 접두사를 집계했다(`grep -oE "^#? ?[A-Z][A-Z0-9_]+="`).
- 포트 정본: ktdm `docs/ports.md`·`config/docker-targets.yml`, geo `docs/ports.md`, map `docs/deploy.md`·`docs/integration-map.md` §1, wx `deploy/README.md`·`deploy/n150.md`, ktc `docs/decisions.md` ADR-27/28, pinvi `docs/decisions.md` ADR-047, kta `README.md`·`docs/runbooks/deployment.md`·`scripts/deploy-server14.sh`.
- 운영: 각 `AGENTS.md`의 배포·보안 감사 절, `.gitignore`, `.gitattributes`, 배포 스크립트 머리 부분, 백업 스크립트 머리 부분, Prometheus/Grafana 설정, ktdm `config/runtime-pins.seed.json`·`docs/runtime-pin-registry.md`·`docs/bindings.md`·`docs/prod-deployment.md`.
- prod 도메인/IP 노출 집계: `git grep -l "digitie\.mywire\.org"`, `git grep -lE "\b192\.168\.[0-9]+\.[0-9]+\b"` (추적 파일, `*.local.md` 제외).
- 선행 보고서 `F:/dev/kor-travel-geo-fixes/docs/kor-travel-common-library-review.md` §7.2·§8을 읽고 §1.15에서 대조했다.

## 1. 비교표

### 1.1 GitHub Actions 워크플로 구성 (사실, 재확인)

| 항목 | kta | ktc | ktdm | geo | map | wx | pinvi |
|---|---|---|---|---|---|---|---|
| 파일 수 | 1 (`ci.yml`) | **0** (`.github` 미추적) | 1 (`ci.yml`) | 2 (`ci.yml`, `openapi.yml`) | 6 (`ci`, `lint`, `openapi`, `frontend`, `docker-images`, `postgis-only`) | 1 (`ci.yml`) | 7 (`api`, `web`, `etl`, `mobile`, `aggregate-ci`, `codex-pr-review`, `codex-pr-monitor`) + `README.md` |
| 트리거 | push `main`, `codex/**`; PR | — | PR; push `main`; `workflow_dispatch` | PR; push `main` | push/PR `main`, `integration/t-vn`; `postgis-only`는 manual | push `main`, `feat/**`; PR | PR/push `main` **path 필터**; `aggregate-ci`는 모든 PR(opened/synchronize/reopened/ready_for_review); monitor는 5분 cron |
| job 이름 | `backend`, `frontend`, `live-e2e` | — | `backend`(백엔드 검사), `frontend`(프론트엔드 검사) | `backend`, `frontend`, `openapi` | `unit`(3.11/3.12/3.13 matrix), `integration`, `fixture-replay`, `lint`, `openapi-drift`, `build`(이름 `type-check + next build (Node 20)`), `build`(docker), `integration`(manual) | `python`, `frontend` | `lint-typecheck-test`, `integration-test`(4-shard), `docker-provenance-image`, `contract-pin-consistency`, `contract-staleness`(schedule); `lint-typecheck-build`, `docker-image`, `e2e`; `docker-image`, `sanity`; `mobile-typecheck/lint/doctor`; `aggregate`; `reminder`; `remind` |
| Python / 설치 | 3.12 / `uv sync --extra dev --locked` | — | 3.11 / `pip install -e ./backend httpx==0.28.1 pytest==9.1.1 ruff==0.16.4` | 3.12 / apt GDAL + `pip install -e ".[api,loaders,dev]"` | 3.11·3.12·3.13 / `pip install -e ".[dev]"` ×3 패키지 (`setup-uv@v6`는 설치만 하고 미사용) | 3.12 / `uv sync --locked --extra dev --extra dagster` | 3.12 / `pip install -e ".[dev]"` |
| Node / npm | 22 / 동봉 | — | 20 / 동봉 | 20 / 동봉 | 22.23.1 / `npx --yes npm@12.0.1` | 20 / `npm ci --ignore-scripts --no-audit --no-fund` | 22 / `npm install -g npm@11.19.1` |
| CI DB | `services.postgres: postgres:16` | — | 없음 | 없음(`services` 블록 없음) | testcontainers PostGIS(digest) | `services.postgres: postgres:16` | `postgis/postgis:16-3.5-alpine` service (`version-matrix.md` §3.2) |
| 실제 운영 호출 | `live-e2e`가 `https://<prod-host>` 호출(`ci.yml:64`) | — | 없음 | 없음 | 없음(Playwright는 n150에서 수동) | 없음 | `e2e`는 mock(`page.route`); live-mutating은 `--list`만 |
| branch protection | 문서만(`docs/runbooks/branch-protection.md`: 2026-08-23 `404 Branch not protected`) | — | 미확인 | `docs/agent-guide.md` §7.5.6(운영자 수동 설정 지시) | `docs/runbooks/branch-protection.md` §4 required check 8개 | 미확인(문서 없음) | ruleset `main-pr-only`(id `17146781`) 적용, required는 `Aggregate CI gate` 하나(`.github/workflows/README.md:30-56`) |

### 1.2 게이트 매트릭스 (사실, 재확인)

| 게이트 | kta | ktc | ktdm | geo | map | wx | pinvi |
|---|---|---|---|---|---|---|---|
| Python lint (`ruff check`) | ✗ | — | ✓ (`--ignore EXE001`) | ✓ | ✓ (`lint.yml`) | ✓ | ✓ |
| `ruff format --check` | ✗ | — | ✗ | ✗ | 정의만(`if: false`, `lint.yml:63`) | ✗ | ✓ |
| mypy | ✗ | — | ✗ | ✓ | ✓ `--strict` ×4 (D2 lane 스크립트 포함) | ✗ | ✓ `--strict` |
| import-linter | ✗ | — | ✗ | ✓ | ✓ | ✗ | ✗ |
| pytest | ✓ | — | ✓ | ✓ | ✓ unit matrix + integration(PostGIS) + fixture replay; coverage api 70 / dagster 80 | ✓ | ✓ unit + integration 4-shard |
| alembic | `upgrade head` + **`check`** | — | ✗ | ✗ | integration 테스트 내부(`test_alembic_metadata_consistency.py`) | `upgrade head` | `upgrade head`(PostGIS service) |
| TS type-check | `tsc -p tsconfig.test.json` | — | ✓ | ✓ | ✓ (admin + user-client) | ✓ | ✓ (workspaces) + mobile |
| ESLint | ✗ | — | ✓ `--max-warnings=0` | ✓ | ✓ + `verify:frontend-eslint` + React Doctor | ✓ | ✓ (workspaces) + mobile |
| FE 단위 테스트 | vitest `--run` | — | ✓ | ✓ | ✓ vitest(36파일 286케이스, 2026-09 이전엔 미실행이었음을 주석이 기록) | ✗ | ✓ (workspaces; `packages/*` 104테스트 T-321) |
| FE 빌드 | ✓ | — | ✓ | ✓ | ✓ (`NEXT_PUBLIC_*` 더미) | ✓ | ✓ (`NEXT_PUBLIC_PINVI_API_URL=http://localhost:12801`) |
| E2E | live(prod) | — | ✗ | ✗ | ✗ | ✗ | Playwright mock + trace 업로드(실패 시) |
| OpenAPI drift | ✗ | — | ✗ | ✓ `export_openapi.py --check` | ✓ `--profile all --check` 3 spec | ✓ export 후 `git diff --exit-code` | 소비자 측: vendored map spec sha256 pin 일치·byte equality |
| 프론트 typegen drift | ✗ | — | ✗ | `gen:types` + `git diff --exit-code` | `gen:types:check` ×2 | ✗ | ✗ |
| Docker build | ✗ | — | ✗ | ✗ | ✓ 전 production 이미지(`scripts/docker-buildx.sh`, OCI 출력, 산출물 수 대조) | ✗ | ✓ web/etl/api 이미지 빌드 + **기동 확인**(HTTP 응답, Dagster definitions import) |
| 보안·공급망 | ✗ | — | ✗ | ✗ | `audit:high`(차단), `audit:dev`(비차단), `verify:npm-tree`, `verify:next-sharp` | ✗ | `check-lockfile-integrity.mjs`, wheel provenance, image provenance |
| 문서 게이트 | ✗ | — | ✗ | ✗ | `check_task_ledger_deletions.py`, `check_prod_redaction.py` | ✗ | ✗ |
| 인프라 설정 검증 | ✗ | — | ✗ | ✗ | ✗ | `promtool check config/rules`(docker `prom/prometheus:v3.5.0`) | ✗ |
| cross-repo 계약 | ✗ | — | ✗ | ✗ | ✗ | ✗ | `contract-pin-consistency`(map 4개 pin checkout·byte 비교), `contract-staleness`(일일) |

사실 요약: 7개 중 CI가 있는 6개 모두 "Python 검사 + Node 검사" 2-job 골격은 같지만, 게이트 폭은 map·pinvi(10종 이상) ↔ kta·ktdm·wx(3~5종)로 갈린다. `ruff` 설정 자체가 없는 kta·ktc는 `backend.md` §2.17에서 확인된다.

### 1.3 워크플로 하드닝 관행 (사실, 재확인)

| 관행 | kta | ktdm | geo | map | wx | pinvi |
|---|---|---|---|---|---|---|
| `permissions:` 최소화 | ✗ | `contents: read`(top) | ✗ | `docker-images`·`postgis-only`만 `contents: read` | `contents: read`(top) | `aggregate-ci`(checks/contents/pull-requests read), codex 2종 `permissions: {}` + job 단위 write |
| `concurrency` cancel-in-progress | ✗ | ✗ | ✗ | 5개 워크플로 전부(`<name>-${{ github.workflow }}-${{ github.ref }}`) | ✗ | 전부(`<name>-${{ github.ref }}`; aggregate는 PR 번호) |
| `timeout-minutes` | ✗ | ✗ | backend 35, apt 12 | docker 60, postgis 30 | ✗ | 모든 job(10~45) |
| 액션 SHA 핀 | ✗ (v4/v5/v6) | ✓ (`checkout@11bd7190…# v4.2.2`, `setup-python@a26af69b…# v5.6.0`, `setup-node@49933ea5…# v4.4.0`) | ✗ | ✗ | ✗ | ✗ |
| 러너 | ubuntu-latest | **ubuntu-24.04** | ubuntu-latest | ubuntu-latest | ubuntu-latest | ubuntu-latest |
| checkout ref | 기본(merge ref) | 기본 | 기본 | 기본; `lint`는 `fetch-depth: 0` | 기본 | `ref: ${{ github.event.pull_request.head.sha \|\| github.sha }}`(web/etl/api 전 job) |
| `secrets.*` 참조 | 없음 | 없음 | 없음 | `GITHUB_TOKEN`(buildx secret, 선택) | 없음 | `github.token`만; repository secret 0개(`docs/runbooks/secrets.md`) |
| 캐시 | npm | npm | npm | npm + pip | uv(`enable-cache`) + npm | npm + pip |
| CI 더미 값 | DB 접속 문자열 평문 | — | — | `NEXT_PUBLIC_*` 더미 URL | DB 접속 문자열 평문 | YAML 평문(`secrets.md` §4) |

### 1.4 pre-commit (사실, 재확인)

| 저장소 | 파일 | 훅 | 비고 |
|---|---|---|---|
| geo | `.pre-commit-config.yaml` | `astral-sh/ruff-pre-commit@v0.7.4` `ruff --fix`; `mirrors-mypy@v1.13.0` (`additional_dependencies` 11종, 대상 `src/kortravelgeo scripts/export_openapi.py`); local `import-linter`(`language: system`) | hook 버전이 lock의 ruff 0.16.x / mypy 2.3.x와 다르다(`backend.md` §2.17 추정과 일치) |
| map | `.pre-commit-config.yaml` (`minimum_pre_commit_version: "3.7.0"`) | 전부 `repo: local`: journal 필수(`check_journal_update.py`), prod redaction(`check_prod_redaction.py`, `files: ^docs/.*\.(md\|mdx\|txt\|rst)$`), `ruff format --check`, `mypy --strict`, `lint-imports`(`scripts/run-precommit-check.sh` 경유, `language: system`) | 도구 버전은 환경(venv)에 위임 |
| kta, ktc, ktdm, wx, pinvi | 없음 | — | pinvi는 husky 등도 없음(`inventory/pinvi.md` §6) |

### 1.5 npm audit·verify·lockfile 검증 (사실, 재확인)

| 장치 | 저장소 | 내용 | CI 연결 |
|---|---|---|---|
| `audit:high` | map | `npm@12.0.1 audit --audit-level=high --omit=dev` — 배포 의존성만 차단 | `frontend.yml:44` |
| `audit:dev` | map | 동일 + dev 포함, `\|\| true`(비차단, 가시화) | `frontend.yml:47` |
| `verify:npm-tree` | map | `scripts/verify-npm-tree.mjs`: npm 실행기 == 12.0.1, `npm ls --all --json` problems 0 | `frontend.yml:50` |
| `verify:frontend-eslint` | map | `scripts/verify-frontend-eslint-config.mjs` effective config 검증 | `frontend.yml:53` |
| `verify:react-doctor-config` | map | React Doctor 예외 전체 범위 검증 | `frontend.yml:59` |
| `verify:next-sharp` | map | `scripts/verify-next-sharp.mjs`: next/sharp ABI 상수 대조 + 실제 최적화 | `frontend.yml:65` |
| `postinstall` | map | `scripts/patch-redocly-openapi-core.mjs`(vendor patch, 버전 불일치 시 실패) | 설치 시 |
| `engines`/`packageManager` | map | `node ^22.22.2 \|\| ^24.15.0 \|\| >=26.0.0`, `npm 12.0.1`, `packageManager npm@12.0.1` | — |
| `check:lockfile` | pinvi | `scripts/check-lockfile-integrity.mjs`: lock `integrity` 보유율 ≥99%(T-352/T-358 재발 방지) | `web.yml:79`(설치 전) |
| `engines` | pinvi | `node >=20`, `npm >=11`; `packageManager` 없음 | — |
| `verify-frontend-toolchain.sh` | ktdm | 배포 preflight: `node_modules/.bin` 손상 검사(`--fix`는 `npm ci`로 파괴적 복구) | CI 아님(운영 호스트) |
| `npm ci --ignore-scripts` | wx | 설치 스크립트 실행 차단 | `ci.yml:80` |
| 없음 | kta, ktc, geo | `npm ci`만 | — |

### 1.6 Dockerfile 패턴 (사실, 재확인 — 18개 파일)

| 파일 | 베이스 | 스테이지 | non-root `USER` | `HEALTHCHECK` | `EXPOSE` | 핀 방식 | 기타 |
|---|---|---|---|---|---|---|---|
| kta `backend/Dockerfile` | `python:3.12-slim` | 1 | ✗ | ✗ | 8000 | 태그 | `ENTRYPOINT /entrypoint.sh` |
| kta `frontend/Dockerfile` | `node:22-alpine` | 1 | ✗ | ✗ | 3000 | 태그 | `ARG NEXT_PUBLIC_*` |
| ktc `Dockerfile.python` | `python:3.11-slim` | 1 | ✗ | ✗ | — | 태그 | api/mcp/scheduler 공용, apt ffmpeg |
| ktc `frontend/Dockerfile` | `node:22-slim` | 1 | ✗ | ✗ | 3000 | 태그 | **`CMD npm run dev`**(dev 서버 이미지; prod는 ktdm이 production 빌드로 구동, `ktdm docs/prod-deployment.md` §7) |
| geo `docker/api.Dockerfile` | `python:3.12-trixie` | 1 | ✗ | ✗ | 12501 | 태그 | GDAL 버전 일치 검사 |
| geo `kor-travel-geo-ui/Dockerfile` | `node:22-alpine` | 3 (deps/builder/runner) | ✗ | ✗ | 12505 | 태그 | |
| geo `…/dagster.Dockerfile` | `python:3.12-slim` | 2 (builder/runtime) | ✓ `appuser`(system) | ✗ | 12502 | 태그 | |
| map `docker/api.Dockerfile` | `python@sha256:57cd7c3a…` | 2 | ✓ `appuser` | ✗ | 12701 | **digest** | OCI `LABEL`(revision·tree·Dockerfile sha256·base image id), `COPY --chown=root:root` |
| map `docker/frontend.Dockerfile` | `node:22.23.1-bookworm-slim@sha256:…` | 3 | ✓ `nextjs:nodejs` | ✗ | 12705 | digest | Next standalone 출력 |
| map `docker/dagster.Dockerfile` | `python@sha256:…` | 2 | ✓ `appuser` | ✗ | 12702 | digest | `--mount=type=secret,id=github_token` |
| map `docker/c7-playwright.Dockerfile` | `mcr.microsoft.com/playwright:v1.60.0-noble@sha256:…` | 1 | ✗ | ✗ | — | digest | e2e 러너 |
| wx `deploy/Dockerfile.python` | `ghcr.io/astral-sh/uv:0.11.21` + `python:3.13-slim` | 2(uv 바이너리 복사) | ✗ | ✗ | 14101 14102 14103 | 태그 | `ARG INSTALL_DAGSTER`로 API/Dagster 분기 |
| wx `deploy/Dockerfile.web` | `node:22-alpine` | 3 | ✗ | ✗ | 14105 | 태그 | |
| wx `deploy/Dockerfile.dagster-gateway` | `nginx:1.27-alpine` | 1 | ✗ | ✗ | — | 태그 | 기동 시 `openssl passwd -apr1`로 htpasswd 생성 |
| pinvi `apps/api/Dockerfile` | `python:3.12-slim@sha256:7a8b4750…` | 1(`AS base`) | ✗ | ✓ (`/health`, `/health/db`, `/health/feature-reference-reconciliation`) | 8000 | digest + `# syntax=docker/dockerfile:1.7-labs` | OCI `LABEL` revision·build env |
| pinvi `apps/etl/Dockerfile` | 동일 | 1 | ✗ | ✓ (Dagster `repositoriesOrError`) | 12802 | digest | |
| pinvi `apps/web/Dockerfile` | `node:22-bookworm-slim@sha256:83f487e0…` | 3 | ✗ | ✓ | 3000 | digest + syntax digest | |
| pinvi `infra/nginx/Dockerfile` | `nginx:1.27-bookworm@sha256:…` | 1 | ✗ | ✗ | — | digest | GeoIP2 선택 |

집계(사실): 멀티스테이지 9/18, non-root 4/18(map 3 + geo dagster), Dockerfile `HEALTHCHECK` 3/18(pinvi만; 나머지는 compose `healthcheck`), digest 핀 map·pinvi만, OCI 라벨 map·pinvi만. **컨테이너 내부 포트 = 호스트 포트**(geo/map/wx: 12501·12705·14101) ↔ **내부 8000/3000 + 매핑**(kta·ktc·pinvi api/web)이 갈린다.

### 1.7 docker compose 파일 체계 (사실, 재확인)

| 저장소 | 파일 | 역할 | `name:` | 네트워크 | 특징 |
|---|---|---|---|---|---|
| kta | `docker-compose.yml` | 앱(backend/frontend) | `kor-travel-airport` | external `kor-travel-airport-net` | healthcheck 2종(python urllib / node fetch), `depends_on` healthy, 포트 `${PUBLIC_API_PORT:-14001}:8000` |
| kta | `docker-compose.db.yml` | DB 스택(별도 lifecycle) | `kor-travel-airport-db` | 네트워크 생성 측(`name: kor-travel-airport-net`) | 볼륨 이름 고정 `parking-radar_parking_radar_postgres_data`(개명 후 유지) |
| kta | `docker-compose.live.yml` | 단기 검증(55432/8010) | `kor-travel-airport-live` | — | |
| kta | `docker-compose.odroid.yml` | fail-closed 마커 | `parking-radar-odroid-disabled` | — | `services: {}` |
| ktc | `docker-compose.yml` | dev 단일 파일 | 없음 | 기본 bridge + `extra_hosts host.docker.internal` | `x-app-env-file`·`x-python-env` anchor, `env_file: ${APP_ENV_FILE:-.env}`, profile `embedded-rustfs`, healthcheck api만 |
| ktdm | `docker-compose.yml` (1,522줄) | prod 통합(4 PostGIS + RustFS + 관측 + geo/conc/map/pinvi 앱) | `kor-travel-docker-manager` | `network_mode: ${KTDM_DOCKER_NETWORK_MODE:-host}` 전 서비스 | **단일 canonical 파일**(include/extends/override 거부, `docs/architecture.md:277-278`), Docker secret 4종(postgres password), healthcheck 12종 |
| geo | (저장소 내 compose 없음) `docs/deploy/docker-compose.geo-source-vol.yml` | ktdm에 넣는 override 정본 | — | — | dev는 `scripts/docker_app.sh`(`docker run`, host 네트워크 기본) |
| map | `docker-compose.yml` (773줄) + `host.yml`, `local-dev.yml`, `external-db.yml`, `external-infra.yml`, `external-object-store.yml` | base + 5 overlay | 없음 | base: bridge + `admin-control` 네트워크; `host.yml`: 전 서비스 `network_mode: host` | profile `fresh-init`·`local-infra`, 볼륨명 env override, secret `github_token`, bind host `${KOR_TRAVEL_MAP_DOCKER_BIND_HOST:-127.0.0.1}` |
| wx | `compose.yaml` + `deploy/compose.n150.yaml` | base + LAN override(`!override` ports) | 없음 | 기본 bridge | 서비스명이 일반명(`db/api/dagster/dagster-gateway/migrate/prometheus/web`), 포트 리터럴 `127.0.0.1:141xx`, native secret `metrics_token` |
| pinvi | `infra/docker-compose.yml` | dev(인프라 + profile `etl`·`observability`) | 없음 | `network_mode: host` | 볼륨 `pinvi-*` |
| pinvi | `infra/docker-compose.app.yml` (478줄) | smoke/prod 앱 스택 | 없음(`PINVI_DOCKER_PROJECT` `-p`로 지정: `pinvi-app` / `pinvi-app-smoke`) | 기본 bridge, `127.0.0.1:${PINVI_API_PORT:-12801}:8000` | 서비스 `app-*` 접두, 이미지 digest 핀, profile `maintenance`·`legacy-rebaseline`·`etl`·`observability`, healthcheck는 postgres·rustfs만(앱은 Dockerfile `HEALTHCHECK`) |

Compose 프로젝트명 부여 방식(사실): kta·ktdm은 파일 `name:`; pinvi·ktc(verify)는 `-p`/`PROJECT_NAME` env(`kor-travel-concierge-verify`); map·wx는 디렉터리명 의존.

### 1.8 서비스명·컨테이너명·이미지명·볼륨 규약 (사실, 재확인)

| 규약 축 | 관측된 형태 | 저장소 |
|---|---|---|
| compose 서비스명 — 짧은 역할명 | `backend/frontend/postgres`, `api/mcp/scheduler/frontend/rustfs`, `postgres/api/frontend/dagster/dagster-daemon/rustfs`, `db/api/dagster/dagster-gateway/migrate/prometheus/web` | kta, ktc, map, wx |
| compose 서비스명 — 프로젝트 접두 | `kor-travel-geo-api`, `kor-travel-map-dagster-daemon`, `pinvi-api` … | ktdm(통합 파일이라 충돌 회피), geo override |
| compose 서비스명 — 스택 접두 | `app-postgres`, `app-api`, `app-web`, `app-dagster`, `app-backup`, `app-migrator` | pinvi app |
| `container_name` | `${KOR_TRAVEL_GEO_API_CONTAINER:-kor-travel-geo-api-latest}`(env override, `-latest` 접미), `${PINVI_DOCKER_PROJECT:-pinvi-app}-dagster` | ktdm 전 장기 서비스; geo `docker_app.sh`(`kor-travel-geo-api-latest`); pinvi app 일부(dagster·관측). kta·ktc·map·wx는 미사용 |
| 이미지명 | `<project>-<role>:latest-main`(`kor-travel-geo-api:latest-main-gdal`, `pinvi-api:latest-main`), pinvi 로컬 `pinvi-api:local`, CI `pinvi-web-ci:${GITHUB_SHA}` | ktdm, geo, pinvi |
| 볼륨명 | `kor-travel-map-postgres`, `kor-travel-map-rustfs`(env override), `pinvi-pgdata`, `app-postgres`, `weather-postgres`, `parking-radar_parking_radar_postgres_data`(고정) | map, pinvi, wx, kta |
| 네트워크명 | `kor-travel-airport-net`, `kor-travel-geo-net`(bridge 모드), `admin-control` | kta, geo, map |
| DB 이름 | `kor_travel_geo`(+`_dagster`), `kor_travel_concierge`, `kor_travel_map`(+`_dagster`), `pinvi`, `parking_radar`, `weather`/`weather_test` | ktdm `docs/ports.md` §"PostgreSQL instance 경계", kta/wx CI |
| CLI 이름 | `ktdctl`, `ktcctl`(`scripts/ktcctl` → 루트 `ktcctl`) | ktdm, ktc |
| 약칭 | `KTG_`, `KTC_`, `KTDM_`, `kta`(브랜드 `parking-radar`), ktdm target id `geo/conc/map/pinvi` | env 접두·target |

### 1.9 포트 대역 할당표 (사실, 재확인)

정본: ktdm `docs/ports.md`("12000부터 target마다 100 단위, `+0` DB(ADR-37), `+1` API, `+2`부터 추가, `+5` Web UI, Manager `12900-12999`"). `config/docker-targets.yml`은 GM-19에서 `port_policy/port_band` 소비 코드가 없어 제거했고 정책 정본은 `docs/ports.md`뿐이라고 주석에 적었다(`docker-targets.yml:3-4`; 단 `targets.*.port_band`는 남아 있다).

| 대역 | target/소유 | `+0` DB | `+1` API | `+2` 보조 | `+3` | `+4` | `+5` Web | 근거 |
|---|---|---|---|---|---|---|---|---|
| `120xx` | `db`(호환 이름, 실사용 없음) | — | | | | | | ktdm `docs/ports.md:22` |
| `121xx` | RustFS(`storage`) | | 12101 S3 | | | | 12105 console | ktdm, geo, map, ktc, pinvi 전부 동일 |
| `122xx` | Grafana(`gra`) | | | | | | 12205 | ktdm, pinvi(`NEXT_PUBLIC_GRAFANA_URL`) |
| `123xx` | cAdvisor(`cadv`) | | 12301 | | | | | ktdm, pinvi |
| `124xx` | Prometheus(`prom`) | | 12401 | | | | | ktdm, pinvi; ktc MCP **컨테이너 내부** 12402는 ADR-27 이전 잔재 |
| `125xx` | kor-travel-geo | 12500 | 12501 | 12502 Dagster | | | 12505 | geo `docs/ports.md`, ktdm |
| `126xx` | kor-travel-concierge | 12600 | 12601 | 12602 MCP | | | 12605 | ktc ADR-27, ktdm |
| `127xx` | kor-travel-map | 12700(standalone dev는 5432) | 12701(+`/metrics` 동일 포트) | 12702 Dagster | | | 12705 | map `docs/deploy.md`, ADR-047 |
| `128xx` | PinVi | 12800 | 12801 | 12802 Dagster | | | 12805 | pinvi ADR-047, ktdm |
| `129xx` | docker-manager | | 12901 backend | | | | 12905 dashboard | ktdm |
| `140xx` | kor-travel-airport(**ktdm 미등록**) | 14000(loopback) | 14001 | **14002 web**(`+5` 규칙과 다름) | | | | kta `README.md:89-90`, `deploy-server14.sh:86-88` |
| `141xx` | kor-travel-weather(ktdm 미등록, `docs/ports.md:33`에 "sibling 점유"로 명시) | 14100 | 14101 | 14102 Dagster gateway | 14103 Dagster worker metrics(`expose`만) | 14104 Prometheus(loopback) | 14105 | wx `deploy/README.md`, `compose.yaml` |

부수 포트(사실): kta live 스택 55432/8010; ktc E2E 18080/13100, 단독 dev 3000; map CI 더미 `8087/12302/12201`, 잔여 DB `ktm-tvn36-db:18736`·`ktm-tvn38-db:18732`(`integration-map.md`); pinvi 임시 Next `12855`(`docs/resume.md:2405`); ktdm 과거 통합 DB `5432`(폐지, ADR-37).

충돌·불일치(사실): (a) 등록 대역 간 충돌 없음. (b) kta는 ktdm `docs/ports.md`에 없고 `parking-radar와 같은 취급`이라는 문장으로만 암시된다. (c) map `docs/integration-map.md` §1은 "PinVi 저장소 자체 기본값은 api 9021 · web 9022"라고 적었으나 pinvi compose 기본값은 12801/12805다(문서 drift, 추정: 구 기본값). (d) kta의 web `+2`는 유일한 규칙 이탈이다.

### 1.10 prod(n150) 배포·런북 관례 (사실, 재확인)

| 항목 | kta | ktc | ktdm | geo | map | wx | pinvi |
|---|---|---|---|---|---|---|---|
| prod 오케스트레이터 | 자체 `scripts/deploy-server14.sh`(git archive → scp → ssh → `docker compose up -d --build`) | **ktdm**(ADR-28) | 자체: trusted installer `scripts/install-ktdm-trusted-release` + systemd(`ktdm-backend.service` root, `ktdm-frontend.service`) | **ktdm**; 이미지 빌드/전송은 `scripts/deploy_app.py`(buildx amd64+arm64, 노드 `n150=deploy@<internal-host>`, `odroid=deploy@<internal-host>`) | **ktdm** pinned runtime(generation manifest v6 / rebuild journal v8) | 자체: 호스트에서 `git pull --ff-only` + `docker compose --env-file .env -f compose.yaml -f deploy/compose.n150.yaml up -d --build` | **ktdm** `ktdctl pinvi-pair rebuild-pinned --confirm`; fallback `scripts/deploy-node.sh`(2,592줄, `PINVI_DOCKER_MANAGER_UNAVAILABLE=1`) |
| 호스트 표기 | `<prod-address>`(README·AGENTS.md), `<prod-host>` | `<domain>` placeholder(ADR-28) | `manager.<domain>` placeholder | `deploy@<internal-host>`, `<prod-host>`(`docs/ports.md:34`) | `<prod-host-alias>`/`<prod-host-ip>` placeholder(redaction guard) | `digitie@<prod-address>`, `<prod-host>`(`deploy/n150.md`) | placeholder(ADR-047, 공개 repo) |
| 로컬 런북 | 없음(`*.local.md` gitignore도 없음) | `docs/deploy-runbook.local.md`(정본, DO NOT 10) | `docs/deploy-runbook.local.md`(DO NOT 14) | `docs/deploy-runbook.local.md` + `docs/prod-access.local.md` | 동일 2개 | gitignore만 복사(`docs/deploy-runbook.local.md`·`prod-access.local.md` 항목 존재, 파일 미확인) | `docs/deploy-runbook.local.md` + 커밋된 `docs/runbooks/deploy.md` |
| 배포 후 검증 의무 | `/health`의 `release_sha` == 후보 SHA(`deploy-server14.sh:120-132`) | 로그인 POST 200 + Set-Cookie, UI 컨테이너 `${#KTC_ADMIN_PASSWORD_HASH} != 0` | `/health`·`:12905` 200 + 브라우저 로그인→대시보드→로그아웃 전환 + WS 재연결 루프 없음 | 런북(로컬)에 위임; `AGENTS.md:112-113` "#399 이후 로그인 깨짐" | 로그인 POST + `${#KOR_TRAVEL_MAP_UI_ADMIN_PASSWORD_HASH} != 0` | `curl /health`, `/server_info`(Basic Auth), `open /login`(권고, 의무 문구 없음) | `docs/runbooks/deploy.md` §4 운영 체크 |
| 리버스 프록시 | 없음(LAN 포트 직접 + 외부 도메인 1개) | Caddy(`deploy/Caddyfile`, 도메인 env 주입, MCP `basic_auth` fail-safe 기본 해시) | 저장소 밖(§5) + 신뢰 프록시 IP exact `/32` | 라우터 TLS 종단(`docs/ports.md:34`) | 저장소 밖(`*.local.md`) | HAProxy(저장소 밖) + nginx Dagster gateway(Basic Auth) | Cloudflare Tunnel + WAF 한국 전용(`infra/cloudflare/waf-korea-only.md`), 선택 nginx GeoIP2 |
| 실행 비트·EOL | `.gitattributes` `*.sh text eol=lf`만 | `* text=auto eol=lf` + `*.sh` | 동일 | 확장자 8종 LF 열거 | `* text=auto eol=lf` + binary 11종 | map과 동일 | map과 동일 |
| 대상 플랫폼 | amd64(odroid 배포 `throw`로 차단) | amd64 | amd64 | amd64 + arm64 기본(`DEFAULT_PLATFORMS`) | amd64만(`docker-images.yml` 주석 "배포 대상은 amd64뿐") | amd64 | amd64(N150), `docs/runbooks/odroid-docker.md` 존재 |

prod 도메인/IP 문자열 노출 집계(사실; 추적 파일, `*.local.md` 제외):

| 저장소 | `<prod-host>` 파일 수(그중 `docs/`) | `192.168.x.x` 파일 수(그중 `docs/`) | 대표 비-docs 위치 |
|---|---|---|---|
| kta | 17 (12) | 26 (13) | `.github/workflows/ci.yml`, `README.md`, `AGENTS.md`, `CLAUDE.md`, `.env.server14.example` |
| ktc | 1 (1) | 4 (2) | `.env.example`, `backend/ktc/core/config.py` |
| ktdm | 1 (0) | 1 (0) | `backend/tests/test_api.py`, `docker-compose.yml` |
| geo | 7 (5) | 3 (3) | `.env.prod.example`, `tests/unit/test_dagster_router.py` |
| map | 3 (0) | 0 | guard 자신·`lint.yml`·`auth.ts`(패턴 문자열) |
| wx | 13 (2) | 3 (0) | `README.md`, `compose.yaml`, `deploy/compose.n150.yaml`, `deploy/README.md` |
| pinvi | 0 | 0 | — (ADR-047) |

map의 `scripts/check_prod_redaction.py`(패턴 2종: `digitie\.mywire\.org`, `\b192\.168\.\d{1,3}\.\d{1,3}\b`; 범위 `docs/` 하위 `.md/.mdx/.txt/.rst`)는 map에만 있고, 다른 저장소에는 동종 스크립트가 없다(`git ls-files scripts | grep -iE "redact|secret|audit|scan|leak"` 0건).

### 1.11 시크릿·env 처리 (사실, 재확인)

| 항목 | kta | ktc | ktdm | geo | map | wx | pinvi |
|---|---|---|---|---|---|---|---|
| `.env.example` 파일 | `.env.example`(44행), `.env.server14.example`(42행) | `.env.example`(308행) | `.env.example`(398행), `frontend/.env.example` | `.env.example`(118), `.env.dev.example`, `.env.prod.example`, `kor-travel-geo-ui/.env.local.example` | `.env.example`(283), `packages/kor-travel-map-api/.env.example`, `…admin/frontend/.env.example` | `.env.example`(66), `…admin/frontend/.env.example` | `.env.example`(348), `apps/api/.env.example`(132), `infra/.env.prod.example`(175), `.env.mcp-telegram.example` |
| 키 접두 집계 | **접두 없음**(`DATABASE_URL`, `PUBLIC_API_PORT`, `ENABLE_SCHEDULER`…), `NEXT_PUBLIC_*` 1, `POSTGRES_*` 5 | 혼합: `RUSTFS_*` 18, `KTC_*` 8, `API_*` 8, `PROMETHEUS_*` 3, `APP_*`, `CORS_*`, `DATABASE_*`, `BACKEND_*`, `KOR_TRAVEL_GEO_*` 2 | `KOR_TRAVEL_MAP_*` 52, `KOR_TRAVEL_GEO_*` 39, `PINVI_*` 31, **`KTDM_*` 19**, `RUSTFS_*` 7, `GRAFANA_*` 7, `PROMETHEUS_*` 5, `CADVISOR_*` 3, `KRTOUR_MAP_*` 2(구명) | **`KTG_*` 74(100%)**; dev/prod 예시 각 `KTG_*` 17/19 + `NEXT_PUBLIC_*` 1 | **`KOR_TRAVEL_MAP_*` 91**, `NEXT_PUBLIC_*` 5, 공공 API 키 9종은 접두 없음(`KMA_API_KEY`, `NAVER_SEARCH_*`…) | `KOR_TRAVEL_WEATHER_*` 32, `WEATHER_*` 5(compose/UI 전용), `POSTGRES_*` 3, `NEXT_PUBLIC_*` 1 | **`PINVI_*` 190**, `NEXT_PUBLIC_*` 7, `EXPO_PUBLIC_PINVI_API_URL`, `KOR_TRAVEL_MAP_*` 1, `DATA_GO_KR_SERVICE_KEY` |
| 브라우저 공개 키 | `NEXT_PUBLIC_*` | `NEXT_PUBLIC_*`(BFF라 비움 권장, ADR-28) | `NEXT_PUBLIC_*` | `NEXT_PUBLIC_*` | `NEXT_PUBLIC_KOR_TRAVEL_MAP_*` | `NEXT_PUBLIC_VWORLD_API_KEY` | `NEXT_PUBLIC_PINVI_*`, `EXPO_PUBLIC_*` |
| compose 필수 보간 `:?` | ✗ | ✗ | `KOR_TRAVEL_MAP_POSTGRES_IMAGE_ID:?` | — | ✗(스크립트가 검증) | admin token·metrics token·Fernet key·session secret | `PROMETHEUS_MULTIPROC_DIR:?`(Dockerfile CMD) |
| Docker secret | ✗ | ✗ | 파일 secret 4종(postgres password) | — | build secret `github_token`, 네트워크 `admin-control` | native `metrics_token` → `/run/secrets/metrics.token` | 미확인 |
| `.env` 권한 | 미확인 | 미확인 | installer가 0600 검증(`scripts/check-env-permissions.sh`) | `.env.prod` 또는 노드 `/etc/kor-travel-geo/app.env` | 600 또는 vault(SKILL §4) | 600(`deploy/n150.md:32`) | `infra/.env.prod` gitignore |
| `.gitignore` | `.env`, `.env.*`, `!.env.example`, `!.env.server14.example`; `*.local.md` **없음** | `.env*` 계열, `*.local.md` | `.env*`, `*.local.md`, `*.local.sh` | `.env`, `.env.*`, `!.env.*.example`, `*.local.md` | `.env`, `.env.*`, `!.env.example`, `*.local.md` + 2개 명시 | wx는 map과 동일 + `deploy/*.env` | `.env`, `.env*.local`, `.env.prod`, `.env.production`, `.env.mcp-telegram`, `*.local.md`(2회) |
| GitHub Actions secret | 없음 | — | 없음 | 없음 | `GITHUB_TOKEN`만 | 없음 | 0개(문서화) |
| 배포 env 강제값 | `require_exact` 12종(포트·스케줄러·마이그레이션 플래그) | `APP_ENV=production`, `API_KEYS`, `BACKEND_API_KEY`, `FORWARDED_ALLOW_IPS=*` | `.env` 스냅샷 해시(installer) | `KTG_ADMIN_PROXY_SECRET` 양쪽 | production profile fail-closed(ops token 3종·cursor secret·metrics token) | `KOR_TRAVEL_WEATHER_ENV=production` compose 고정 | `PINVI_ENVIRONMENT`, 이미지 provenance |

### 1.12 백업·복원 (사실, 재확인; `backend.md` §2.13과 정합)

| 저장소 | 트리거 | 실행 주체 | 포맷·보존 | 복원 | UI/문서 |
|---|---|---|---|---|---|
| kta | cron 3일(`scripts/n150-backup-cron.sh` → `POST /v1/admin/backups`) | API(`backend/app/services/backup_restore.py`) | `pg_dump --format=custom`, `BACKUP_RETENTION_COUNT` | API | `frontend/src/components/backup-panel.tsx`, `docs/architecture/backup-restore.md` |
| ktc | 없음 | — | — | — | — |
| ktdm | cron(`scripts/run-standalone-backup.sh <role> <keep>`; role `geo_dagster/concierge/pinvi`만 허용, `CRON_TZ=UTC`) | `ktdctl` standalone backup, `offbox_backup_sync.py` | keep 개수 인자, logrotate는 installer가 `KTDM_BACKUP_ROOT`로 렌더 | — | `BackupHistoryPanel.tsx`, `docs/prod-deployment.md` §3.x |
| geo | Dagster schedule → `POST /v1/admin/backups/scheduled/run-due`(T-290f) | API 소유(advisory lock·audit) | 미확인(모듈 `backup_execute.py`) | `db_restore_execute.py`, UI RestoreWizard·HotSwapTab | `kor-travel-geo-ui/app/admin/backups/`, `scripts/benchmark_backup_restore.py` |
| map | `npm run docker:backup`(`scripts/docker-backup.sh`) | 스크립트(`KOR_TRAVEL_MAP_BACKUP_ROOT`, command fence 토큰) | `KOR_TRAVEL_MAP_BACKUP_ID=UTC 타임스탬프` | `docker-restore.sh`, `docker-restore-swap.sh`, `docker-restore-verify.sh`, `live-e2e-backup-runner/{backup,restore,swap}.sh` | `admin_backups.py`, `admin/backups/page.tsx` |
| wx | 없음 | — | — | — | — |
| pinvi | `scripts/backup-db.sh`(app-schema custom-format, 최소 여유공간, Docker fallback `postgis/postgis:16-3.5`, trusted 모드) | 스크립트 + `app-backup` compose profile `maintenance` | `PINVI_BACKUP_DIR`, catalog | `restore-db.sh`, `restore-hotswap.sh`, `restore-staging-drill.sh`, `m05_restore_drill.py` | `admin/backup/page.tsx`, `RestoreHotswapDialog.tsx`, `docs/runbooks/backup-restore.md`, Grafana `etl-backup.json` |

공통 골격(사실): `pg_dump` custom 포맷 + 보존 개수 + admin API/UI + 핫스왑 복원(geo·map·pinvi)이며, 스케줄 주체가 cron(kta·ktdm) / Dagster(geo) / 수동·UI(map·pinvi)로 갈린다. ktdm은 geo 앱 DB와 map DB를 자기 주기 대상에서 제외한다(중복 방지, `run-standalone-backup.sh:2-6`).

### 1.13 관측(Prometheus/Grafana/cAdvisor) (사실, 재확인)

| 저장소 | Prometheus | Grafana | 기타 | scrape 대상(설정 파일 기준) |
|---|---|---|---|---|
| ktdm | `prom/prometheus:v2.53.1` @12401, `config/prometheus/prometheus.yml`(`scrape_interval: 15s`) | `grafana/grafana:11.1.4` @12205, datasource provisioning → `http://127.0.0.1:12401` | cAdvisor `v0.52.1` @12301 | `prometheus`, `cadvisor`, `kor-travel-docker-manager` `:12901/metrics`, `kor-travel-geo-api` `:12501/metrics`, `kor-travel-geo-ui` `:12505/api/metrics` — **map·concierge·pinvi job 없음**(map `docs/deploy.md:75-76`도 동일 지적) |
| wx | 자체 `prom/prometheus:v3.5.0` @14104(loopback), `deploy/prometheus/prometheus.yml`(30s) + `alerts.yml`, CI `promtool check` | 없음 | nginx Dagster gateway | `kor-travel-weather-api` `api:14101/metrics`(`bearer_token_file: /run/secrets/metrics.token`), `kor-travel-weather-dagster` `dagster:14103/metrics` |
| pinvi | 자체 profile `observability`: `v2.53.1`(dev `prometheus.yml` / prod `prometheus.app.yml`) | `11.1.4` + dashboards 5종(`api-http`, `api-performance`, `db-pool`, `etl-backup`, `websocket`) + provisioning; admin UI에 iframe(`NEXT_PUBLIC_GRAFANA_URL`) | cAdvisor, `prom/blackbox-exporter:v0.25.0`(`infra/blackbox/blackbox.yml`) | `pinvi-api` `/metrics`, `pinvi-web-health`·`pinvi-dagster-health` `/probe`(blackbox) |
| map | 앱 측 `kortravelmap/api/prometheus.py`; `/metrics`는 API 포트 12701 동일; production은 metrics token 필수 | — | — | ktdm에 job 미등록 |
| geo | 앱 측 `/metrics`, UI `/api/metrics` | — | — | ktdm이 scrape |
| ktc | `.env.example`에 `PROMETHEUS_*` 3키 | — | — | 사용처 미확인 |
| kta | 없음 | — | — | — |

Prometheus major가 ktdm·pinvi(v2.53.1) ↔ wx(v3.5.0)로 다르다(`version-matrix.md` §3.4와 일치).

### 1.14 docker-manager가 관리하는 레지스트리 (사실, 재확인)

| 레지스트리 | 파일 | 스키마/내용 | 소비자 |
|---|---|---|---|
| 대상(target) 레지스트리 | `config/docker-targets.yml`(490줄, `version: 1`) | `dependency_order`(db→storage→gra→cadv→prom→geo→conc→map→pinvi); `containers.<id>`: `name`, `compose_service`, `role`, `display_name`, `connection`, `prod_url_env`(`KTDM_PROD_URL_*`), `expected_ports`; `targets.<id>`: `port_band`, `depends_on`, `aliases`, `services`, `runtime_services`, `containers`, `init_steps`(compose `exec/run` 커맨드); `all` | `ktdctl`, API/CLI registry 테스트, `docs/ports.md`(변경 절차 §"변경 절차") |
| 포트 정책 | `docs/ports.md` | §1.9 표 | 모든 형제 저장소가 source of truth로 인용(geo `docs/ports.md:23`, ktc ADR-27, map ADR-047) |
| runtime pin 레지스트리 | `config/runtime-pins.seed.json`(`schema: kor-travel-docker-manager.runtime-pin-registry.v1`, `release_version: 5`) | `sources[]{role: map\|pinvi, url, revision}`, `pinset_sha256`, `rotated_at/by`, `reason`, `history[]`, `blocked_pinsets[]{pinset_sha256, map_revision, pinvi_revision, phase?, reason, blocked_at}` | `docs/runtime-pin-registry.md`(불변식 7종, `GET /api/v1/runtime-pins`, 2-step 회전 → `ktdctl pin apply-pending --confirm`); 운영 호스트는 `KTDM_RUNTIME_PINS_FILE`로 배포 트리 밖(`/var/lib/kor-travel-docker-manager`) |
| 결박(bindings) 등록부 | `docs/bindings.md` | DO NOT 15: 같은 사실이 두 곳에 적힐 때 정본/사본/이유/결박 테스트를 등록(B-1 launcher 집합, B-2 진단 어휘, B-3 M05 2-role, B-4 규범 문서→테스트; U-1 핀된 Map revision은 cross-repo라 미결박) | 리뷰·grep |
| 앱 env 사본 | `.env.example`(398줄) | `KOR_TRAVEL_MAP_*` 52, `KOR_TRAVEL_GEO_*` 39, `PINVI_*` 31 키를 다시 나열 | compose 보간 — 각 앱 `.env.example`과 **이중 선언**(bindings U-1과 같은 종류의 미결박 중복, 추정) |
| 관측 설정 | `config/prometheus/prometheus.yml`, `config/grafana/provisioning/datasources/prometheus.yml` | §1.13 | Prometheus/Grafana 컨테이너 |
| 설치·운영 | `scripts/install-ktdm-trusted-release`(`/opt/kor-travel-docker-manager` staging→commit, wheelhouse, `.env` 0600, systemd, tmpfiles lease `/run/lock/kor-travel-docker-manager`), `scripts/run-pinned-rebuild-once`, `scripts/rotate-pinned-pair`, `scripts/run-m05-isolated-e2e-once` | `docs/prod-deployment.md` §2~§8 | 운영자(root) |

### 1.15 선행 보고서(2026-09-05)와의 대조

- 선행 보고서 §7.2는 "CI·lint·TypeScript 설정: 별도 필요 검토 — 프레임워크 버전을 숨기거나 모든 앱 빌드를 묶는 공통 설정 금지"라고 했다. 이번 조사도 같은 결론이다: 6개 CI의 job 골격은 같지만 게이트 폭·도구 버전·npm 핀(12.0.1 vs 11.19.1)이 달라 **하나의 워크플로 파일을 복사해 쓰는 방식은 성립하지 않고**, 입력(inputs)으로 폭을 조절하는 재사용 워크플로가 적합하다(§2).
- 선행 보고서 §8은 "운영에서 `latest`나 이동하는 Git branch를 직접 참조하지 않는다"고 권고했다. 사실 대조: ktdm·geo·pinvi 이미지 태그는 `latest-main`이지만 그것은 **로컬 빌드 태그**이고, 실제 배포 단위는 runtime pin 레지스트리의 소스 revision + 이미지 digest(pinvi app compose)다. 즉 "태그 이름"과 "핀 단위"를 구분하면 권고와 모순되지 않는다. 다만 RustFS/mc `latest`(ktdm·map·ktc·pinvi dev)는 권고 위반 상태로 남아 있다(`version-matrix.md` §3.4).
- 선행 보고서는 포트·compose·런북 관례를 다루지 않았다(§12 조사 범위에 없음). 이 문서가 처음 정리한다.

## 2. 공통 CI 템플릿 후보와 각 앱 도입 변경점

### 2.1 재사용 워크플로 후보 (후보)

common 저장소 `.github/workflows/`에 `workflow_call` 워크플로를 두고, 각 앱은 `uses: digitie/kor-travel-common/.github/workflows/<name>.yml@<sha|tag>`로 호출한다. 이름·입력은 다음과 같이 잡는다(입력 기본값은 §1.2에서 다수인 값).

| 워크플로 | 주요 inputs | steps(순서) | 근거 관행 |
|---|---|---|---|
| `python-quality.yml` | `python-version`(기본 3.12), `working-directory`, `installer`(`uv`\|`pip`, 기본 `uv`), `install-args`(예 `--extra dev --locked` / `.[api,loaders,dev]`), `pre-install`(apt 등 자유 스크립트), `ruff-format`(bool), `mypy-targets`(문자열, 빈값이면 생략), `import-linter`(bool), `alembic`(bool: `upgrade head` + `check`), `pytest-args`, `coverage-fail-under`, `db-image`(빈값\|`postgres:16`\|`postgis/postgis:16-3.5-alpine`), `db-env`(DATABASE_URL 등) | checkout(exact head SHA) → setup-python → setup-uv(조건) → pre-install → install → `ruff check` → `ruff format --check`(조건) → mypy(조건) → lint-imports(조건) → alembic(조건) → pytest | kta(`alembic check`), geo(GDAL pre-install, import-linter), map(mypy strict), wx(uv locked), pinvi(ruff format) |
| `node-quality.yml` | `node-version`(기본 22), `npm-version`(빈값이면 동봉), `working-directory`, `workspaces`(bool), `lockfile-integrity`(bool: pinvi 스크립트), `audit-level`(`high`\|`none`), `ignore-scripts`(bool), `lint-max-warnings`(기본 0), `typegen-check-command`(빈값이면 생략), `test`(bool), `build-env`(더미 `NEXT_PUBLIC_*` JSON) | checkout → setup-node(cache npm) → npm 핀(조건) → lockfile integrity(조건, 설치 전) → `npm ci --no-audit --no-fund [--ignore-scripts]` → `npm audit --audit-level=high --omit=dev`(차단) + dev 포함(비차단) → typegen drift(조건) → lint → type-check → test(조건) → build | map(`audit:high`/`audit:dev`, `gen:types:check`), pinvi(lockfile, npm 핀, workspaces), ktdm(`--max-warnings=0`), wx(`--ignore-scripts`) |
| `openapi-drift.yml` | `python-version`, `install-args`, `export-command`, `spec-paths`(list), `mode`(`check`\|`git-diff`) | install → export → `--check` 또는 `git diff --exit-code -- <spec-paths>` | geo(`--check`), map(3 profile), wx(`git diff`) |
| `docs-check.yml` | `link-check`(bool), `redaction-patterns-file`(기본 `.prod-redaction-patterns`), `redaction-scope`(기본 `docs/`), `task-ledger`(bool) | `tools/validate_document_links.py`(common 도구를 `uses` 저장소에서 체크아웃) → 일반화한 `check_prod_redaction.py`(패턴 파일 입력) → `validate_plan.py`(조건) | common `docs.yml`, map `lint.yml:43-47`, map pre-commit |
| `secret-scan.yml` | `patterns-file`, `paths` | staged/diff grep(ktc·ktdm·pinvi AGENTS.md 4~5단계 절차의 grep 패턴을 스크립트화: `api[_-]?key\|secret\|password\|passwd\|token\|pbkdf2_sha256\|AKIA…\|BEGIN … PRIVATE KEY`, `docs-conventions.md` §1.16) + 프로젝트별 패턴 파일 | 어느 저장소도 CI에 넣지 않았음(수동 절차만). 외부 스캐너(gitleaks 등) 채택 여부는 열린 질문 |
| `docker-build.yml` | `dockerfiles`(list of `{file, context, build-args}`) 또는 `build-script`, `platforms`(기본 `linux/amd64`), `boot-check`(`{port, path}` 선택) | setup-buildx → 빌드(OCI 출력, `--load` 없음) → 산출물 수 대조 → 기동 확인(조건: HTTP 응답 또는 `--entrypoint python -c import …`) | map `docker-images.yml`, pinvi `web.yml:100-141`·`etl.yml:25-54` |
| `aggregate-gate.yml` | `rules`(경로 prefix → check 이름 매핑 JSON), `deadline-minutes`(기본 40), `timeout`(기본 45) | pinvi `aggregate-ci.yml`의 `github-script`를 규칙 입력형으로 일반화 | pinvi(`README.md` §branch protection: path-filtered 워크플로를 required로 묶으면 `Expected` 상태에 갇힘) |

공통 하드닝 기본값(후보): 모든 재사용 워크플로에 `permissions: contents: read`(dm·wx 선례), `concurrency: <name>-${{ github.ref }}` cancel-in-progress(map·pinvi 선례), `timeout-minutes` 기본 30(pinvi 선례), `runs-on: ubuntu-24.04` 고정(dm 선례; `ubuntu-latest` 6곳은 러너 이미지 갱신에 무방비), checkout `ref: ${{ github.event.pull_request.head.sha || github.sha }}`(pinvi 선례), 액션 참조는 SHA + 주석 버전(dm 선례) — 액션 major는 `version-matrix.md` §4.4(checkout v7 / setup-node v7 / setup-python v7)와 §5.1(현행 v4/v5 유지 + SHA 핀) 중 결정 필요.

### 2.2 각 앱 도입 변경점 (후보)

| 앱 | 유지할 앱 고유 job | 재사용 워크플로로 대체 | 도입 시 바꿔야 하는 것 | 난이도(추정) |
|---|---|---|---|---|
| kta | `live-e2e`(prod 호출) — required에서 제외하거나 `workflow_dispatch`/스케줄로 분리 검토(`branch-protection.md:46-49`가 이미 재검토 대상으로 적음) | `python-quality`(uv, alembic check ON, `postgres:16`), `node-quality`(Node 22), `openapi-drift`(`git-diff` 모드; `scripts/export_openapi.py`에 `--check` 없음), `docs-check`, `secret-scan` | `pyproject.toml`에 ruff 설정 신설(현재 없음, `backend.md` §2.17); prod 도메인/IP가 `README.md`·`AGENTS.md`·`ci.yml`에 17/26 파일 노출 → redaction 도입 전 placeholder 치환 필요; `*.local.md` gitignore 추가; 테스트 tsconfig(`tsconfig.test.json`)를 `type-check` 스크립트로 흡수 | 중 |
| ktc | (없음 — CI 신설) | `python-quality`(pip, 3.11 → 기준선 3.12 이상 검토), `node-quality`, `docs-check`, `secret-scan`, `docker-build`(`Dockerfile.python`, `frontend/Dockerfile`) | `.github` 신설; ruff 설정 신설; `frontend/Dockerfile`이 `npm run dev`라 `docker-build` 기동 확인은 production 빌드 Dockerfile 추가 후; 4개 `requirements*.txt` → lock 정책은 `version-matrix.md` §7.2 결정에 종속 | 상(제로 베이스) |
| ktdm | 없음 | `python-quality`(pip + 3종 정확 핀 → `install-args`), `node-quality`(Node 20 → 22) | SHA 핀 관행 유지: 재사용 워크플로 참조도 SHA로; `--ignore EXE001` 유지 입력; mypy 미도입 상태 유지 가능(`mypy-targets` 빈값) | 하 |
| geo | 없음 | `python-quality`(`pre-install`에 GDAL apt + `pip install "gdal==$(gdal-config --version)"`, import-linter ON, mypy ON), `node-quality`(Node 20 → 22, `typegen-check-command: npm run gen:types && git diff --exit-code -- types/api.gen.ts lib/schemas.gen.ts`), `openapi-drift`(`check` 모드) | `openapi.yml` 폐지(통합); pre-commit ruff/mypy rev를 lock과 맞추거나 map식 `language: system`으로 전환; `docs/ports.md:34`의 실제 도메인 → placeholder | 중 |
| map | `ci.yml`(matrix·integration·fixture), `lint.yml`의 task ledger·D2 lane mypy, `docker-images.yml`, `postgis-only.yml` — 그대로 유지 | `openapi-drift`, `docs-check`(redaction 스크립트를 common으로 이관하고 map은 소비), `node-quality`(npm 12.0.1 핀 입력, `verify:*`는 `pre-lint-command` 같은 훅 입력으로 유지) | required check 이름 8개(`branch-protection.md` §4)가 바뀌면 ruleset 갱신 필요; `type-check + next build (Node 20)` legacy 이름 정리 기회 | 중(보수적으로는 openapi/docs만) |
| wx | `promtool` 검사(앱 고유 → `python-quality`의 `post-test-command` 입력 또는 별도 step) | `python-quality`(uv, alembic ON, `postgres:16`), `node-quality`(Node 20 → 22, test ON — vitest 3.2.7 존재), `openapi-drift`(`git-diff`) | `README.md`·`compose.yaml`·`deploy/*`의 도메인/IP 13/3 파일 → redaction 정책 결정(운영 기록 문서를 `*.local.md`로 옮길지); `*.local.md` gitignore는 이미 있음 | 중 |
| pinvi | `api.yml`의 provenance·contract-pin·staleness, `web.yml` e2e, `mobile.yml`, codex 2종 — 유지 | `node-quality`(npm 11.19.1 핀, lockfile ON, workspaces), `python-quality`(ruff format ON, mypy strict, PostGIS service), `docker-build`(boot-check), `aggregate-gate`(규칙 입력형) | required check 이름(`lint-typecheck-test`, `lint-typecheck-build`, `e2e`, `sanity`, `mobile-typecheck`)을 재사용 job 이름과 일치시켜야 aggregate 규칙이 유지됨; path 필터 목록(트리거와 aggregate에 **이중 선언**, `web.yml:19-25` 주석이 인정)을 `rules` 입력 하나로 합칠 기회 | 중 |

### 2.3 도입 제약과 미확인 사항

- 재사용 워크플로를 다른 저장소에서 호출하려면 common이 public이거나 private/internal 저장소의 Actions 접근 설정이 필요하다(GitHub 일반 기능; 이번 세션에서 공식 문서 미조회 → **미확인**). common은 GPL-3.0 공개 전제이므로 성립할 것으로 추정.
- 재사용 워크플로 안의 `uses:` 액션 SHA는 common이 한 곳에서 관리하므로 dm의 SHA-핀 관행이 7개 저장소로 확산되는 효과가 있다. 반대로 common 참조 자체를 `@main`으로 두면 선행 보고서 §8 권고("이동하는 branch 참조 금지")와 충돌하므로 태그/SHA 참조를 규칙으로 둔다(후보).
- npm 버전 정책(map 12.0.1 vs pinvi 11.19.1 vs 나머지 동봉 10.9.x)은 `version-matrix.md` §5.1 후보 A(11.19.x)/B(12.0.2)에 종속된다. `node-quality`의 `npm-version` 입력은 정책 결정 전까지 앱별 값을 그대로 받는다.
- 게이트 이름은 branch protection/ruleset의 required check 문자열과 결합돼 있다(map 8개, pinvi 5개). job `name:`을 입력으로 열어 두어야 한다.

## 3. 포트/서비스명/컨테이너 명명 표준 초안 (후보)

### 3.1 포트

1. **정본은 계속 ktdm `docs/ports.md`** 하나로 두고, common은 그 규칙을 문서 규약으로 인용만 한다(정본 이원화 금지 — ktdm `docs/bindings.md` 원칙과 동일).
2. 대역 규칙을 슬롯까지 명문화: `12{n}00` DB, `01` API, `02` worker/Dagster/MCP, `03` 보조 metrics/exporter(wx 14103 선례), `04` 예약(관측 로컬), `05` Web, `06~09` 추가 Web/BFF, `10~99` 임시·E2E(pinvi 12855 선례). 컨테이너 내부 포트는 **호스트 포트와 동일**하게 listen(geo/map/wx 선례; ktdm `docs/ports.md:14-16` host 네트워크 전제)을 권장하고, 8000/3000 내부 포트(kta·ktc·pinvi)는 예외로 등록한다.
3. sibling 대역 등록: `140xx` kor-travel-airport, `141xx` kor-travel-weather를 `docs/ports.md` 표에 **명시 행**으로 추가(현재 weather만 문장으로, airport는 없음). airport web 14002는 (a) 예외 등록 또는 (b) 14005 이전(`deploy-server14.sh` `require_exact PUBLIC_WEB_PORT 14002`, `README.md`, CORS 원본 `<prod-address>:14002`, HAProxy 매핑 변경 필요) 중 결정 — 이 문서는 (a)를 기본안으로 둔다(운영 변경 비용).
4. common 자체 대역 후보: `130xx`(예: 13001 smoke API, 13005 showcase/문서 사이트). 근거: 12xxx는 ktdm 예약, 14xxx는 sibling, 13100은 ktc E2E가 사용하므로 `130xx`만 비어 있음(사실: 조사 파일 내 `130[0-9]{2}` 사용 없음 — 단 grep 범위는 §방법의 문서·compose·스크립트로 한정, **미확인** 영역 있음).

### 3.2 서비스명·컨테이너명·이미지·볼륨·네트워크

| 대상 | 표준 초안 | 기존과의 관계 |
|---|---|---|
| 앱 자체 compose 서비스명 | 짧은 역할명 고정 어휘: `postgres`, `api`, `web`, `dagster`, `dagster-daemon`, `mcp`, `scheduler`, `migrate`, `rustfs`, `rustfs-init`, `prometheus`, `grafana`, `cadvisor`, `backup` | kta `backend/frontend` → `api/web`, wx `db` → `postgres`, ktc `frontend` → `web`, pinvi `app-*` 접두 제거(또는 `-p`로 구분) — 이름 변경은 각 앱 스크립트(`verify-docker-compose.sh`, `deploy-server14.sh`, `docker-app.sh`)의 서비스 참조를 함께 바꿔야 함 |
| ktdm 통합 compose 서비스명 | `<project>-<role>` (`kor-travel-geo-api`, `pinvi-web`) — 현행 유지 | 이미 일관됨 |
| `container_name` | `<project>-<role>[-<lane>]`; `-latest` 접미는 lane이 아니므로 제거 후보(`kor-travel-geo-api-latest` → `kor-travel-geo-api`); 항상 env override 가능(`${X_CONTAINER:-…}`, ktdm 선례) | ktdm `docker-targets.yml` `containers.*.name`·geo `docker_app.sh`·ktdm registry 테스트가 `-latest`를 참조하므로 변경 비용 있음 — 열린 질문 |
| 이미지명 | `<project>-<role>:<tag>`; tag 어휘 `latest-main`(로컬 최신 main 빌드), `local`(작업 트리), `ci-<sha>`(CI 검증), 배포 단위는 digest 또는 pin registry revision | ktdm·geo·pinvi 현행과 일치; `latest-main-gdal`처럼 변형 접미는 `<role>` 뒤에 둔다 |
| 볼륨 | `<project>-<purpose>`(`kor-travel-map-postgres`, `pinvi-pgdata` → `pinvi-postgres`); 이름 고정이 필요한 유산 볼륨은 `name:`으로 명시(kta 선례) | wx `weather-postgres` → `kor-travel-weather-postgres` 후보 |
| 네트워크 | bridge일 때 `<project>-net`(kta·geo 선례); host 모드는 `network_mode: ${<PREFIX>_DOCKER_NETWORK_MODE:-host}` env 스위치(ktdm·geo 선례) | map `admin-control`은 목적 네트워크라 예외 |
| compose 프로젝트명 | 파일 `name: <project>[-<stack>]`(kta 선례) — 디렉터리명 의존 금지 | map·wx·pinvi·ktc 추가 |
| health 경로 | `/health`(liveness) + `/ready`(readiness) — `backend.md` §2.5(6/7이 `/health`) | geo `/healthz`·`/readyz`는 ktdm healthcheck(`/v1/healthz`)·Prometheus 설정과 결합 → 별칭 병행 기간 필요 |
| env 접두 | 앱당 **단일 접두** 필수. 신규는 `KOR_TRAVEL_<APP>_`(map·wx 선례), 기존 단축형 `KTG_`/`KTC_`/`KTDM_`/`PINVI_`는 유지. 브라우저 노출은 `NEXT_PUBLIC_<접두>` / `EXPO_PUBLIC_<접두>`. compose 인프라 키(`POSTGRES_*`, `RUSTFS_*`)와 외부 API 키(`KMA_API_KEY` 등)는 예외 목록으로 등록 | kta(접두 없음 44키), ktc(혼합) 정리 대상; ktdm `.env.example`의 앱 키 사본은 각 앱 `.env.example`에서 **생성**하는 방식 검토(bindings 원칙) |
| 약칭 | `kta`, `ktc`, `ktdm`, `geo`(env `KTG`), `map`(env 없음, `KOR_TRAVEL_MAP`), `wx`(env `KOR_TRAVEL_WEATHER`), `pinvi`; ktdm target id(`geo/conc/map/pinvi`)는 별칭 테이블로 유지 | ktdm `aliases` 필드가 이미 다중 별칭을 지원 |

### 3.3 Dockerfile·compose 최소 규약 (후보)

- 멀티스테이지 + 최종 스테이지 non-root(`groupadd --system`/`useradd --system … --shell /usr/sbin/nologin`, map·geo dagster 선례). 현재 4/18만 충족.
- `HEALTHCHECK`는 Dockerfile(pinvi 선례) 또는 compose 중 **한 곳**에 두되, 명령은 이미지에 이미 있는 런타임으로(`python -c urllib`, `node -e fetch`, `pg_isready -p <port>`; ktdm `docker-compose.yml:84`가 `-p` 누락 시 영원히 unhealthy가 됨을 기록).
- 베이스 이미지는 `<image>:<tag>@sha256:<digest>` 병기(map·pinvi 선례), OCI `org.opencontainers.image.revision` 라벨 필수(map·pinvi 선례).
- `.gitattributes`는 `* text=auto eol=lf` + 바이너리 목록(map·wx·pinvi·common 동일) — kta(`*.sh`만)·geo(확장자 열거) 정렬.

## 4. common 저장소 자체 CI 구성 제안 (후보)

현 상태(사실): `.github/workflows/docs.yml` 하나 — `actions/checkout@v6`, `actions/setup-python@v6`, `tools/validate_document_links.py`, `tools/validate_plan.py`, `unittest`(`tests/test_plan_validation.py`), `git diff --check`. `permissions`·`concurrency`·`timeout` 없음. 액션 major(v6)가 앱들(v4/v5)보다 높다.

| job | 트리거 | 내용 | 비고 |
|---|---|---|---|
| `docs` | PR, push `main` | 현행 4 step + 일반화한 `check_prod_redaction.py`(common은 prod 값을 가질 이유가 없으므로 전체 트리 대상) + Markdown 링크 검사 범위에 `docs/survey/**` 포함 | 기존 `docs.yml` 확장 |
| `workflows-selftest` | PR(`.github/**` 변경) | 재사용 워크플로를 `workflow_call`로 호출하는 fixture(`tests/fixtures/python-app`, `tests/fixtures/node-app`)로 dry-run; `actionlint`(후보, 미채택 도구) | §2.1 워크플로가 생기면 |
| `packages` | PR, push `main` | `npm ci` → lint → type-check → test → build → `npm pack` → 임시 디렉터리에서 tarball 설치 후 import/CSS 산출물 존재 검사(선행 보고서 §7.3·§10 "배포 tarball 설치 테스트") | 패키지 디렉터리 확정 후 |
| `python-package` | PR, push `main` | 공통 Python 패키지(`backend.md` §5)가 생기면 `python-quality` 자기 호출 + `uv build` + wheel 설치 검사 | 조건부 |
| `consumer-smoke` | `workflow_dispatch` + 주간 schedule(비용) | 대표 소비자 2곳(map admin, pinvi web — 선행 보고서 §8 "두 대표 소비자")을 pinned SHA로 체크아웃 → `npm install <tarball>` → `type-check` + `next build` | ktdm `runtime-pins.seed.json`과 같은 형식의 `consumers.pins.json`(role, url, revision)을 common에 두는 방안 — `version-matrix.md` §7.3 논의와 결합 |
| `secret-scan` | PR | §2.1 `secret-scan` 자기 호출 | |
| 하드닝 | 전체 | `permissions: contents: read`, `concurrency`, `timeout-minutes`, `runs-on: ubuntu-24.04`, 액션 SHA 핀(+주석 버전) | dm·map·pinvi 선례 합성 |

branch protection: PR 필수 + required check(`docs`, `packages`) + linear history + force-push 차단(pinvi ruleset·kta·map 문서 공통분모). required check 이름은 재사용 워크플로 이름 변경과 함께 관리한다.

## 열린 질문

1. 재사용 워크플로의 cross-repo 호출 조건(common 공개 여부, private일 때 Actions 접근 설정) — 공식 문서 미조회.
2. npm 실행기 버전 정책(12.0.1 / 11.19.x / 동봉) 결정 전에는 `node-quality`가 앱별 값을 그대로 받아야 한다. 결정은 `version-matrix.md` §5.1.
3. airport web 포트 14002 예외 등록 vs 14005 이전 — 운영 변경 비용(HAProxy·CORS·`require_exact`) 대비 규칙 일관성.
4. 컨테이너명 `-latest` 접미 제거 여부 — ktdm `docker-targets.yml`·registry 테스트·geo `docker_app.sh`가 참조.
5. prod 도메인/IP redaction 정책의 적용 범위: map처럼 `docs/`만 볼지, kta(README·AGENTS.md·`ci.yml`)·wx(`compose.n150.yaml`·`deploy/n150.md`)처럼 운영 기록을 추적 파일에 두는 관행을 허용할지. 허용하면 CI guard는 저장소별 opt-in이어야 한다.
6. 외부 secret 스캐너(gitleaks 등) 채택 여부 — 현재 7개 저장소 모두 수동 grep 절차뿐.
7. arm64/odroid 대상 포함 여부 — geo는 기본 포함, map은 amd64만, kta는 fail-closed, pinvi는 runbook만 존재.
8. ktdm `.env.example`의 앱 키 사본(`KOR_TRAVEL_MAP_*` 52 등)을 앱 `.env.example`에서 생성/검증하는 결박 테스트를 어디에 둘지(ktdm `bindings.md` U-1과 같은 cross-repo 문제).
9. Prometheus major(v2.53.1 vs v3.5.0)와 scrape 결선(ktdm에 map·concierge·pinvi job 없음)을 common 규약으로 정할지, ktdm 소유로 둘지.
10. `live-e2e`(kta)처럼 운영 시스템을 호출하는 CI job을 공통 규약에서 금지할지(pinvi는 mock, map은 n150 수동으로 이미 분리).
11. common 자체 포트 대역 `130xx`의 실제 미사용 여부 — 조사 범위 밖 로컬 프로세스·다른 저장소 미확인.
12. wx `AGENTS.md`에 배포 후 검증 의무 문구가 없음(사실) — 다른 5개와 같은 로그인 검증 의무를 공통 규약으로 올릴지.

## 근거 파일 목록 (저장소 상대 경로)

kor-travel-airport @ 2bb1111
- `.github/workflows/ci.yml`
- `docker-compose.yml`, `docker-compose.db.yml`, `docker-compose.live.yml`, `docker-compose.odroid.yml`
- `backend/Dockerfile`, `frontend/Dockerfile`
- `scripts/deploy-server14.sh`, `scripts/n150-backup-cron.sh`
- `docs/runbooks/branch-protection.md`, `docs/runbooks/deployment.md`, `README.md`, `AGENTS.md`
- `.env.example`, `.env.server14.example`, `.gitignore`, `.gitattributes`

kor-travel-concierge @ 7945305
- `docker-compose.yml`, `Dockerfile.python`, `frontend/Dockerfile`
- `deploy/Caddyfile`, `scripts/verify-docker-compose.sh`, `scripts/ktcctl`
- `docs/decisions.md`(ADR-27, ADR-28), `AGENTS.md`(DO NOT 9·10, §prod 배포 & 보안 감사)
- `.env.example`, `.gitignore`, `.gitattributes`

kor-travel-docker-manager @ 862562d
- `.github/workflows/ci.yml`
- `docker-compose.yml`
- `config/docker-targets.yml`, `config/runtime-pins.seed.json`, `config/prometheus/prometheus.yml`, `config/grafana/provisioning/datasources/prometheus.yml`
- `docs/ports.md`, `docs/runtime-pin-registry.md`, `docs/bindings.md`, `docs/prod-deployment.md`, `docs/architecture.md`
- `scripts/install-ktdm-trusted-release`, `scripts/run-standalone-backup.sh`, `scripts/verify-frontend-toolchain.sh`
- `AGENTS.md`, `.env.example`, `.gitignore`, `.gitattributes`

kor-travel-geo @ 1d9d74d
- `.github/workflows/ci.yml`, `.github/workflows/openapi.yml`, `.pre-commit-config.yaml`
- `docker/api.Dockerfile`, `kor-travel-geo-ui/Dockerfile`, `kor-travel-geo-dagster/docker/dagster.Dockerfile`
- `docs/deploy/docker-compose.geo-source-vol.yml`, `docs/ports.md`, `docs/agent-guide.md`(§7.5.6)
- `scripts/docker_app.sh`, `scripts/deploy_app.py`
- `kor-travel-geo-dagster/src/kortravelgeo_dagster/backup.py`
- `AGENTS.md`, `.env.example`, `.env.dev.example`, `.env.prod.example`, `.gitignore`, `.gitattributes`
- `docs/kor-travel-common-library-review.md`(선행 보고서 §7.2, §8)

kor-travel-map @ c494e227
- `.github/workflows/ci.yml`, `lint.yml`, `openapi.yml`, `frontend.yml`, `docker-images.yml`, `postgis-only.yml`, `.pre-commit-config.yaml`
- `docker-compose.yml`, `docker-compose.host.yml`, `docker-compose.local-dev.yml`, `docker-compose.external-db.yml`, `docker-compose.external-infra.yml`, `docker-compose.external-object-store.yml`
- `docker/api.Dockerfile`, `docker/frontend.Dockerfile`, `docker/dagster.Dockerfile`, `docker/c7-playwright.Dockerfile`
- `package.json`(scripts·engines), `scripts/check_prod_redaction.py`, `scripts/docker-buildx.sh`, `scripts/docker-backup.sh`, `scripts/preflight-ports.sh`
- `docs/deploy.md`, `docs/integration-map.md`(§1), `docs/runbooks/branch-protection.md`, `AGENTS.md`(§prod 배포 & 보안 감사)
- `.env.example`, `.gitignore`, `.gitattributes`

kor-travel-weather @ 6003da9
- `.github/workflows/ci.yml`
- `compose.yaml`, `deploy/compose.n150.yaml`, `deploy/Dockerfile.python`, `deploy/Dockerfile.web`, `deploy/Dockerfile.dagster-gateway`
- `deploy/README.md`, `deploy/n150.md`, `deploy/prometheus/prometheus.yml`
- `AGENTS.md`, `.env.example`, `.gitignore`, `.gitattributes`

pinvi @ 9af25e5
- `.github/workflows/README.md`, `api.yml`, `web.yml`, `etl.yml`, `mobile.yml`, `aggregate-ci.yml`, `codex-pr-review.yml`, `codex-pr-monitor.yml`
- `infra/docker-compose.yml`, `infra/docker-compose.app.yml`, `apps/api/Dockerfile`, `apps/etl/Dockerfile`, `apps/web/Dockerfile`, `infra/nginx/Dockerfile`
- `infra/prometheus/prometheus.yml`, `infra/prometheus/prometheus.app.yml`
- `package.json`, `scripts/deploy-node.sh`, `scripts/docker-app.sh`, `scripts/backup-db.sh`
- `docs/decisions.md`(ADR-047), `docs/runbooks/deploy.md`, `docs/runbooks/secrets.md`, `AGENTS.md`
- `.env.example`, `apps/api/.env.example`, `infra/.env.prod.example`, `.gitignore`, `.gitattributes`

kor-travel-common @ b92fabe (+미추적)
- `.github/workflows/docs.yml`, `tools/README.md`, `tools/validate_document_links.py`, `.gitignore`, `.gitattributes`, `.editorconfig`
- `docs/survey/inventory/*.md` §6, `docs/survey/cross/version-matrix.md` §3·§5.1, `docs/survey/cross/backend.md` §2.5·§2.13·§2.17, `docs/survey/cross/docs-conventions.md` §1.15~§1.17·§1.19, `docs/survey/cross/openapi.md` §2.11
