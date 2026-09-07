# 횡단 비교 — 라이브러리·플랫폼 버전 매트릭스

- 작성일: 2026-09-06
- 상태: 읽기 전용 조사 결과. 버전 일치 정책(공통 라이브러리 `kor-travel-common`이 개별 시스템의 라이브러리/플랫폼 버전을 정렬한다는 전제)의 **근거 자료**이며, 결정문이 아니다.
- 범위: 7개 저장소의 프론트엔드·백엔드·도구/CI/컨테이너 버전을 **선언 범위**(package.json / pyproject.toml / requirements.txt)와 **lockfile 설치 버전**(package-lock.json / uv.lock)으로 나눠 읽고, 2026-09-06 registry 기준 최신 안정 버전과 대조했다.
- 표기 규칙: 각 셀은 `선언 / 설치`다. lockfile이 없는 곳은 `미확인(lock 없음)`, 의존성이 없는 곳은 `—`, 전이 의존성으로만 존재하는 것은 `(전이)`로 적는다. 주장에는 사실 / 후보 / 추정 / 미확인을 구분해 표기한다.
- 선행 검토 보고서 `kor-travel-geo` `docs/kor-travel-common-library-review.md`(2026-09-05) §2의 요구 범위 표는 본 조사에서 재검증했으며 불일치는 없었다. 본 문서는 그 표에 없던 airport, lockfile 설치 버전, Python 백엔드, 도구/CI/컨테이너, 최신 버전 대조를 추가한다.

## 0. 기준 — 조사 커밋

| 약칭 | 저장소 | 체크아웃 경로 | 기준 커밋 | 커밋 일자 |
|---|---|---|---|---|
| airport | kor-travel-airport | `F:/dev/kor-travel-common-survey/kta-main` | `2bb1111` | 2026-09-06 |
| concierge | kor-travel-concierge | `F:/dev/kor-travel-concierge` | `7945305` | 2026-09-04 |
| dm | kor-travel-docker-manager | `F:/dev/kor-travel-common-survey/ktdm-main` | `862562d` | 2026-09-05 |
| geo | kor-travel-geo | `F:/dev/kor-travel-geo-fixes` | `1d9d74d` | 2026-09-05 |
| map | kor-travel-map | `F:/dev/kor-travel-common-survey/ktm-main` | `c494e227` | 2026-09-06 |
| weather | kor-travel-weather | `F:/dev/kor-travel-weather` | `6003da9` | 2026-09-05 |
| pinvi | pinvi | `F:/dev/kor-travel-common-survey/pinvi` | `9af25e5` | 2026-09-06 |

lockfile의 마지막 갱신 커밋(사실, `git log -1 -- <lockfile>`):

| 앱 | lockfile | 마지막 갱신 |
|---|---|---|
| airport | `frontend/package-lock.json`, `backend/uv.lock` | `395717b` 2026-09-06 |
| concierge | `frontend/package-lock.json` | `e7ee99e` 2026-08-31 |
| dm | `frontend/package-lock.json` | `38e268b` 2026-09-02 |
| geo | `kor-travel-geo-ui/package-lock.json` | `18ad3b0` 2026-07-28 |
| map | `package-lock.json`(workspace 루트) | `14792385` 2026-08-20 |
| weather | `packages/kor-travel-weather-admin/frontend/package-lock.json`, `uv.lock` | `03e5cd9` 2026-09-01 |
| pinvi | `package-lock.json`(workspace 루트), `apps/api/uv.lock` | `9af25e5` 2026-09-06 |

## 방법

읽은 파일(모두 `git ls-files`로 추적 여부를 확인한 뒤 열람; node_modules·.venv·빌드 산출물은 읽지 않음):

- 프론트엔드 매니페스트: airport `frontend/package.json`; concierge `frontend/package.json`, `tests/package.json`; dm `frontend/package.json`; geo `kor-travel-geo-ui/package.json`; map `package.json`, `packages/kor-travel-map-admin/frontend/package.json`, `packages/map-marker-react/package.json`, `packages/kor-travel-map-user-client/package.json`; weather `packages/kor-travel-weather-admin/frontend/package.json`; pinvi `package.json`, `apps/web/package.json`, `apps/mobile/package.json`, `packages/{api-client,design-tokens,domain,hooks,i18n,schemas,state}/package.json`.
- 프론트엔드 lockfile: 위 8개 `package-lock.json`(전부 `lockfileVersion: 3`)을 Node 스크립트로 파싱해 `packages["node_modules/<pkg>"].version`과 중첩 설치(`*/node_modules/<pkg>`)를 함께 읽었다.
- 백엔드 매니페스트: airport `backend/pyproject.toml`; dm `backend/pyproject.toml`(Poetry); geo `pyproject.toml`, `kor-travel-geo-dagster/pyproject.toml`; map `pyproject.toml`, `packages/kor-travel-map-api/pyproject.toml`, `packages/kor-travel-map-dagster/pyproject.toml`; weather `pyproject.toml`, `packages/kor-travel-weather-{api,dagster}/pyproject.toml`, `packages/python-airkorea-api/pyproject.toml`; pinvi `apps/api/pyproject.toml`, `apps/etl/pyproject.toml`; concierge `backend|etl|mcp|scheduler/requirements.txt`.
- 백엔드 lockfile: airport `backend/uv.lock`, weather `uv.lock`, pinvi `apps/api/uv.lock`을 Python `tomllib`으로 파싱. geo·map·dm·concierge에는 추적된 Python lockfile이 없다(`git ls-files`에서 `uv.lock|poetry.lock|*.lock|requirements*.txt` 검색, `.gitignore`에도 lock 언급 없음).
- CI: 각 저장소 `.github/workflows/*.yml`(concierge는 워크플로 없음). `uses:`·`runs-on`·`node-version`·`python-version`·설치 명령을 추출했다.
- 컨테이너: 모든 `Dockerfile*`·`docker-compose*.yml`·`compose*.yaml`의 `FROM`·`image:` 행, map `docker/*.Dockerfile`, geo `docker/api.Dockerfile`·`kor-travel-geo-dagster/docker/dagster.Dockerfile`.
- 훅·검증 스크립트: geo·map `.pre-commit-config.yaml`; map `scripts/verify-npm-tree.mjs`, `scripts/verify-next-sharp.mjs`, `scripts/patch-redocly-openapi-core.mjs`; pinvi `scripts/check-lockfile-integrity.mjs`; dm `docs/runtime-pin-registry.md`, `config/runtime-pins.seed.json`.
- 문서: airport `docs/architecture/dependencies.md`; geo `docs/adr/019-nextjs-16-security-floor.md`, `docs/journal.md`; dm `docs/decisions.md`(ADR-17/36), `docs/dev-environment.md`; pinvi `docs/decisions.md`(ADR-011), `docs/dev-environment.md`, `apps/mobile/README.md`; map `README.md`, `docs/dev-environment.md`, `docs/archive/journal-2026-08a.md`; concierge `AGENTS.md`, `docs/dev-environment.md`; weather `packages/kor-travel-weather-admin/frontend/design.md`.
- 기존 공유 라이브러리: `F:/dev/maplibre-vworld-react/package.json`, `F:/dev/maplibre-vworld-js/package.json`(peer 범위 확인용).

실행한 외부 조회(§4에 결과 기록): `npm view <pkg> version|time|peerDependencies|engines|dist-tags`(로컬 node v25.9.0 / npm 11.12.1), `curl https://pypi.org/pypi/<pkg>/json`, `curl https://endoflife.date/api/{nodejs,python,postgresql}.json`, `curl https://api.github.com/repos/<action>/releases/latest`, `curl https://hub.docker.com/v2/repositories/postgis/postgis/tags`, `curl https://nodejs.org/dist/index.json`, `git ls-remote --tags`(액션 SHA→태그 해석), `gh run list/view --repo digitie/kor-travel-airport`(airport CI 결과, §6), Context7 문서 조회(Next.js·TypeScript-Go·React·NativeWind v5).

## 1. 프론트엔드 매트릭스

열은 앱, 행은 패키지다. map은 workspace 루트 lock 하나가 admin·map-marker-react·user-client를 모두 해석하고, pinvi도 루트 lock 하나가 web·mobile·packages/*를 해석한다.

### 1.1 플랫폼 선언 — Node / npm

| 항목 | airport | concierge | dm | geo | map | weather | pinvi |
|---|---|---|---|---|---|---|---|
| `engines.node` | 없음 | `>=22` | 없음 | 없음 | `^22.22.2 \|\| ^24.15.0 \|\| >=26.0.0` | 없음 | `>=20` |
| `engines.npm` | 없음 | 없음 | 없음 | 없음 | `12.0.1` | 없음 | `>=11` |
| `packageManager` | 없음 | 없음 | 없음 | 없음 | `npm@12.0.1` | 없음 | 없음 |
| CI Node | 22 | (CI 없음) | 20 | 20 | 22.23.1 + `npx npm@12.0.1` | 20 | 22 + `npm install -g npm@11.19.1` |
| Docker Node | `node:22-alpine` | `node:22-slim` | (이미지 없음, 호스트 실행) | `node:22-alpine` | `node:22.23.1-bookworm-slim@sha256:6c74…` | `node:22-alpine` | `node:22-bookworm-slim@sha256:83f4…` |
| 문서상 요구 | "Node 22"(`docs/architecture/dependencies.md`) | "Node.js v20.9 이상"(`docs/dev-environment.md`), "Node.js 20+"(`AGENTS.md`) | "Node.js 20 LTS"(`docs/dev-environment.md`) | ADR-019: Node 20.9 이상, CI Node 20 | `nvm use 22.23.1`(`README.md`), "Node 20 결과는 CI와 다를 수 있다"(`docs/dev-environment.md:630`) | 없음 | npm 11 필수(`docs/dev-environment.md:162-176`) |
| `.nvmrc`/`.node-version` | 없음 | 없음 | 없음 | 없음 | 없음 | 없음 | 없음 |

사실: 7개 저장소 중 Node 버전을 `engines`로 선언한 곳은 3개(concierge, map, pinvi)이고 정확 버전을 강제하는 곳은 map뿐이다(`verify-npm-tree.mjs`가 npm 12.0.1이 아니면 실패). CI가 Node 20을 쓰는 곳이 3개(dm, geo, weather)인데 Node 20은 2026-04-30에 EOL이 됐다(§4.4). concierge는 `engines.node >=22`이면서 문서는 20.9+를 요구해 자체 불일치가 있다.

### 1.2 프레임워크·스타일 코어

| 패키지 | airport | concierge | dm | geo | map(admin) | weather | pinvi(web) | 최신(§4) |
|---|---|---|---|---|---|---|---|---|
| next | `^16.3.2` / 16.3.2 | `^16.2.7` / 16.2.7 | `^14.1.4` / 14.2.35 | `^16.2.12` / 16.2.12 | `16.2.12`(정확) / 16.2.12 | `^15.2.0` / 15.5.24 | `16.3.3`(정확) / 16.3.3 | 16.3.4 |
| react / react-dom | `^19.2.8` / 19.2.8 | `^19.2.8` / 19.2.8 | `^18.2.0` / 18.3.1 | `^18.3.1` / 18.3.1 | `^19.2.6` / 19.2.8 | `^19.0.0` / 19.2.8 | `^19.0.0`, 루트 `overrides` `19.2.6` / 19.2.6 | 19.2.8 |
| typescript | `^7.0.2` / **7.0.2** | `^5.4.5` / 5.9.3 | `^5.4.3` / 5.9.3 | `^5.9.3` / 5.9.3 | `^5.9.3` / 5.9.3 (map-marker-react `^6.0.3` / 6.0.3 중첩) | `^5.7.3` / 5.9.3 | `^5.6.0` / 5.9.3 | 7.0.2 (`latest`), 6.0.3, 5.9.3 |
| tailwindcss | — | `^4.3.1` / 4.3.1 | `^4.0.0` / 4.3.1 | `^4.0.0` / 4.3.1 | `^4.3.0` / 4.3.3 | — (자체 `app/tokens.css`+`globals.css`) | `^4.3.3` / 4.3.3(`apps/web/node_modules`에 중첩; 루트에는 mobile용 3.4.19) | 4.3.3 |
| @tailwindcss/postcss | — | `^4.3.1` / 4.3.1 | `^4.0.0` / 4.3.1 | `^4.0.0` / 4.3.1 | `^4.3.0` / 4.3.3 | — | `^4.3.3` / 4.3.3 | 4.3.3 |
| postcss | (전이) 8.5.23 | `^8.4.38` / 8.5.15, `overrides.postcss: "$postcss"` | `^8.4.38` / 8.5.15(next 중첩 8.4.31) | `^8.5.15` / 8.5.15(next 중첩 8.4.31) | `overrides.next.postcss 8.5.23` / 8.5.23 | (전이) 8.4.31 | `^8.4.49` / 8.5.28, `overrides "postcss@8.4.31": "^8.5.23"` | 8.5.28 |
| autoprefixer | — | `^10.4.19` / 10.5.0 | — | — | — | — | — | — |
| tw-animate-css | — | `^1.4.0` / 1.4.0 | — | — | `^1.4.0` / 1.4.0 | — | — | 1.4.0 |
| pretendard | — | `1.3.9`(정확) | — | — | `1.3.9`(정확) | — | `^1.3.9` / 1.3.9 | — |
| sharp(next optional) | 0.35.3 | 0.34.5 | — | 0.34.5 | `overrides.next.sharp 0.35.3` / 0.35.3 | 0.35.4 | `overrides "sharp@^0.34.3": "^0.35.0"` / 0.35.4 | next 16.3.4 optional `^0.35.4` |

사실:
- Tailwind v4를 쓰는 앱은 5개(concierge, dm, geo, map, pinvi web). **airport와 weather admin은 Tailwind 자체가 없고**, pinvi mobile은 NativeWind 4 때문에 Tailwind 3.4.19다(§1.7). 설계 전제 (1) "Tailwind v4가 아닌 앱은 v4로 전환"의 실제 대상은 "v3 → v4 전환"이 아니라 대부분 "미도입 → 도입"이다. dm은 ADR-17(2026-06)에서 이미 v3 → v4로 전환했다(`docs/decisions.md:517-546`).
- next 중첩 `postcss 8.4.31`이 dm·geo·weather에 남아 있다. map(`overrides.next.postcss`)과 pinvi(`overrides "postcss@8.4.31"`)는 override로 8.5.23으로 올렸고, concierge는 `$postcss` 참조 override를 쓴다. 같은 문제를 세 가지 방식으로 푼 셈이다.
- Next 정확 핀은 map·pinvi 두 곳이다. map은 `scripts/verify-next-sharp.mjs`가 `next 16.2.12`·`sharp 0.35.3`을 상수로 검증하므로 Next를 올리면 스크립트도 함께 고쳐야 한다.

### 1.3 UI primitive·클래스 유틸

| 패키지 | airport | concierge | dm | geo | map(admin) | weather | pinvi(web) | 최신 |
|---|---|---|---|---|---|---|---|---|
| @base-ui/react | — | `^1.5.0` / 1.5.0 | — | — | `^1.5.0` / 1.6.0 | — | `^1.7.0` / 1.8.0 | 1.8.0 (peer react `^17 \|\| ^18 \|\| ^19`) |
| radix-ui | — | — | — | `^1.4.3` / 1.6.0 (`@radix-ui/react-slot` 1.3.0) | — | — | (전이) `@radix-ui/react-slot` 1.3.3 | 1.6.7 (peer react `^16.8 … ^19`) |
| shadcn(CLI) | — | `^4.10.0` / 4.10.0 — `dependencies`에 위치, 중첩 zod 3.25.76 동반 | — | — | — | — | — | 4.21.0 |
| class-variance-authority | — | `^0.7.1` / 0.7.1 | — | `^0.7.1` / 0.7.1 | `^0.7.1` / 0.7.1 | — | `^0.7.1` / 0.7.1 | 0.7.1 |
| clsx | — | `^2.1.1` / 2.1.1 | (전이) 2.1.1 | `^2.1.1` / 2.1.1 | `^2.1.1` / 2.1.1 | — | `^2.1.1` / 2.1.1 | 2.1.1 |
| tailwind-merge | — | `^3.6.0` / 3.6.0 | — | `^3.6.0` / 3.6.0 | `^3.6.0` / 3.6.0 | — | `^3.6.0` / 3.6.0 | 3.6.0 |
| lucide-react | — | `^1.17.0` / 1.17.0 | `^0.363.0` / 0.363.0 | `^0.468.0` / 0.468.0 | `^1.17.0` / 1.27.0 | `^0.468.0` / 0.468.0 | `^0.460.0` / 0.460.0 | 1.41.0 (1.0.0은 2026-03-23) |
| sonner | — | — | — | — | `^2.0.7` / 2.0.7 | — | — | 2.0.8 |
| recharts | — | — | `^3.8.1` / 3.8.1 | — | — | — | — | — |

사실: cva·clsx·tailwind-merge는 4개 앱 모두 동일 설치 버전(0.7.1 / 2.1.1 / 3.6.0)이며 최신과 같다. primitive 엔진은 Base UI(concierge, map, pinvi) 대 Radix(geo)로 갈리고, Base UI도 1.5.0 / 1.6.0 / 1.8.0 세 버전이 공존한다. lucide-react는 0.363 → 1.41 사이에 5개 버전이 흩어져 있고 0.x와 1.x 사이에는 major 경계가 있다.

### 1.4 데이터·상태·폼·검증

| 패키지 | concierge | dm | geo | map(admin) | weather | pinvi(web) | 최신 |
|---|---|---|---|---|---|---|---|
| @tanstack/react-query | `^5.40.0` / 5.101.0 | `^5.28.0` / 5.101.0 | `^5.90.10` / 5.101.0 | `^5.100.14` / 5.101.4 | `^5.66.8` / 5.102.8 | `^5.59.0` / 5.102.8 (mobile 동일) | 5.102.8 |
| @tanstack/react-table | — | — | `^8.21.3` / 8.21.3 | `^8.21.3` / 8.21.3 | — | `^8.20.5` / 8.21.3 | **9.2.4** (9.0.0은 2026-08-04) |
| @tanstack/react-virtual | — | — | `^3.14.3` / 3.14.3 | `^3.14.3` / 3.14.8 | — | `^3.10.8` / 3.14.10 | 3.14.10 |
| zustand | — | — | `^5.0.14` / 5.0.14 | `^5.0.14` / 5.0.14 | — | `^5.0.0` / 5.0.15 (`@pinvi/state` 동일) | 5.0.15 |
| react-hook-form | `^7.51.5` / 7.77.0 | — | `^7.77.0` / 7.79.0 | — | — | `^7.54.0` / 7.87.0 | 7.87.0 |
| @hookform/resolvers | `^3.4.2` / 3.10.0 | — | `^5.4.0` / 5.4.0 | — | — | `^3.9.0` / 3.10.0 | 5.9.1 (peer zod `^3.25 \|\| ^4`) |
| zod | `^4.4.3` / 4.4.3 (shadcn 중첩 3.25.76) | — | `^4.4.3` / 4.4.3 | map-marker-react peer `^4.4.3` / 4.4.3 | — | `^4.4.3` / 4.5.4(workspace별 중첩; 루트 3.25.76은 `@expo/cli` 요구) | 4.5.4 |

사실: react-query는 선언 하한이 5.28 ~ 5.100으로 넓지만 설치는 5.101 ~ 5.102로 사실상 모여 있다. `@hookform/resolvers`는 geo만 5.x이고 concierge·pinvi는 3.x다(major 격차). react-table 9.x가 2026-08-04에 나왔으나 세 앱 모두 8.21.3이다.

### 1.5 지도·i18n

| 패키지 | concierge | geo | map | weather | pinvi(web) | pinvi(mobile) | 최신 |
|---|---|---|---|---|---|---|---|
| maplibre-gl | `^6.0.0` / **6.0.0** | `^5.24.0` / 5.24.0 | `^5.24.0` / 5.24.0 (map-marker-react peer `^5.24.0`) | `^5.24.0` / 5.24.0 | `^5.24.0` / 5.24.0 | (`@maplibre/maplibre-react-native` `^11.3.4` / 11.3.8) | 6.7.0 (6.0.0은 2026-07-22) |
| maplibre-vworld-react | — | GitHub tarball `95b49d3` / 0.0.0 | — | — | — | — | (peer 미확인, §1.8) |
| vworld-map-web / -core / -rn | — | — | — | — | `file:vendor/*.tgz` 1.0.0 | `file:vendor/*.tgz` 1.0.0 | — |
| next-intl | — | — | — | — | `^4.13.7` / 4.14.2 | — | 4.14.2 |

사실: 기존 공유 라이브러리 `maplibre-vworld-js`(`F:/dev/maplibre-vworld-js/package.json`)의 peer는 `maplibre-gl ^5.24.0`, `react >=18 <20`, `zod ^4.4.3`이다. concierge만 maplibre-gl 6.0.0이라 이 peer 범위를 벗어난다(concierge가 해당 라이브러리를 소비하는지는 본 조사 범위 밖 — 미확인).

### 1.6 린트·테스트·타입·툴체인

| 패키지 | airport | concierge | dm | geo | map(admin) | weather | pinvi(web) | 최신 |
|---|---|---|---|---|---|---|---|---|
| eslint | — (lint 스크립트 없음) | `^9.39.4` / 9.39.4 | `^8.57.1` / 8.57.1 | `^9.39.4` / 9.39.4 | `^10.8.0` / 10.8.0 | `^9.0.0` / 9.39.5 | `^9.16.0` / 9.39.5 | 10.10.0 (10.0.0은 2026-02-06) |
| eslint-config-next | — | `^16.2.7` / 16.2.7 | `^14.2.35` / 14.2.35 | `^16.2.12` / 16.2.12 | — (`@next/eslint-plugin-next ^16.2.12` + `typescript-eslint ^8.65.0` + `eslint-plugin-{react-x,react-dom} ^5.18.0`, `import-x ^4.17.1`, `jsx-a11y-x ^0.2.0`, `react-hooks ^7.1.1`) | `^15.5.24` / 15.5.24 | `16.3.3`(정확) / 16.3.3 | 16.3.4 (peer eslint `>=9`) |
| typescript-eslint | — | (전이) 8.60.1 | — | (전이) 8.61.1 | 8.65.0 | (전이) 미확인 | (전이) 8.69.0 | 8.69.0 (peer typescript `>=4.8.4 <6.1.0`) |
| eslint-plugin-react-hooks | — | 7.1.1 | 5.0.0-canary(next 14 동반) | 7.1.1 | 7.1.1 | 5.2.0 | 7.1.1 | 7.1.1 |
| vitest | `^4.1.11` / 4.1.11 | `^4.1.9` / 4.1.9 | `^4.1.11` / 4.1.11 | `^4.1.8` / 4.1.9 | `^4.1.7` / 4.1.10 | `^3.0.5` / **3.2.7** | `^4.1.10` / 4.1.11 | **5.0.0** (2026-09-03; engines node `^22.12 \|\| ^24 \|\| >=26`) |
| @vitejs/plugin-react | — | — | `^6.1.1` / 6.1.1 | `^4.7.0` / 4.7.0 | `^4.7.0` / 4.7.0 | — | — | 6.1.1 |
| vite(전이) | 8.2.2 | 8.1.0 | 8.2.2 | 7.3.5 | 7.3.6 (marker 8.1.5) | 7.3.6 | 8.2.2 | — |
| @testing-library/react | `^16.3.2` / 16.3.2 | — | `^16.3.3` / 16.3.3 | `^16.3.0` / 16.3.2 | `^16.3.2` / 16.3.2 | — | `^16.1.0` / 16.3.3 | 16.3.3 |
| @testing-library/jest-dom | `^7.0.1` / 7.0.1 | — | `^6.9.1` / 6.9.1 | `^6.9.1` / 6.9.1 | — | — | `^6.6.3` / 6.9.1 | 7.0.1 |
| @testing-library/user-event | `^14.6.5` / 14.6.5 | — | `^14.6.7` / 14.6.7 | — | — | — | `^14.6.6` / 14.6.7 | 14.6.7 |
| @playwright/test | `^1.62.1` / 1.62.1 | tests/ `^1.44.0` / 1.60.0 | — | `^1.57.0` / 1.61.0 | `1.60.0`(정확) / 1.60.0 (+ `mcr.microsoft.com/playwright:v1.60.0-noble` 이미지) | — | `^1.56.0` / 1.63.0 | 1.63.0 |
| jsdom | `^30.0.1` / 30.0.1 | — | `^27.4.0` / 27.4.0 | `^25.0.1` / 25.0.1 | `^25.0.1` / 25.0.1 | — | `^25.0.0` / 25.0.1 | 30.0.1 |
| react-doctor | — | — | — | — | `^0.9.1` / 0.9.1 | — | — | 0.9.13 |
| openapi-typescript | — | — | — | `^7.10.1` / 7.13.0 | `^7.13.0` / 7.13.0 (admin·user-client) | — | — | 7.13.0 |
| @types/node | `^26.2.0` / 26.2.0 | `^20` / 20.19.42 | `^20.11.30` / 20.19.42 | `^20.19.25` / 20.19.43 | `^25.9.1` / 25.9.5 | `^22.13.0` / 22.20.1 | `^22.0.0` / 22.20.1 | 26.4.1 |
| @types/react | 19.2.18 | 19.2.17 | 18.3.31 | 18.3.31 | 19.2.17 | 19.2.18 | 19.2.18 | 19.2.18 |
| prettier | — | — | — | — | — | — | 루트 `^3.3.3` / 3.9.6 | — |

사실:
- ESLint는 8(dm) / 9(concierge, geo, weather, pinvi) / 10(map) 세 major가 공존하고 airport는 lint 자체가 없다. `eslint-config-next 16.3.4`의 peer가 `eslint >=9`이므로 dm이 Next 16으로 가려면 ESLint 8 → 9+ 전환이 동반된다.
- **`typescript-eslint 8.69.0`(최신)의 peer는 `typescript >=4.8.4 <6.1.0`이다.** TypeScript 7을 쓰는 airport는 ESLint가 없어서 문제가 드러나지 않지만, typescript-eslint를 쓰는 concierge·geo·map·pinvi에서는 TS 7이 지원 범위 밖이다(§5.3, §6).
- `@types/node`가 20 / 22 / 25 / 26으로 흩어져 있다. 런타임 Node는 전부 22 계열 이미지인데 타입은 그보다 높은 곳(airport 26, map 25)과 낮은 곳(concierge·dm·geo 20)이 섞여 있다.
- Vitest 5.0.0은 조사 3일 전(2026-09-03) 출시됐고 Node `^22.12 || ^24 || >=26`을 요구한다. weather만 3.x다.

### 1.7 pinvi mobile (Expo)

| 패키지 | 선언 | 설치 | 최신 | 비고 |
|---|---|---|---|---|
| expo | `~57.0.16`(루트·mobile) | 57.0.20 | 57.0.20 | `apps/mobile/package.json` description·`README.md:14-18`은 "Expo SDK 56"이라고 적혀 있어 매니페스트(57)와 문서가 불일치 |
| react-native | `0.86.3`(정확, 루트 override) | 0.86.3 | 0.87.1 | |
| react / react-dom | `^19.2.3`, 루트 override `19.2.6` | 19.2.6 | 19.2.8 | |
| react-native-reanimated / worklets | `4.6.0` / `0.12.1`(정확, override) | 4.6.0 / 0.12.1 | — | |
| expo-router | `~57.0.16` | 57.0.19 | — | |
| nativewind | `^4.1.23` | 4.2.6 | 4.2.6 (`preview` 5.0.0-preview.4) | peer `tailwindcss >3.3.0`; v5는 Tailwind 4.1+ 필수(Context7 `nativewind.dev/v5/guides/migrate-from-v4`) |
| tailwindcss | `^3.4.15` | 3.4.19(루트 hoist) | 4.3.3 | web 4.3.3과 같은 모노레포에 두 major 공존 |
| eslint-config-expo | `~57.0.2` | 57.0.2 | — | |
| @maplibre/maplibre-react-native | `^11.3.4` | 11.3.8 | — | |
| typescript | `^5.6.0` | 5.9.3 | — | `expo.install.exclude`로 react/react-dom/reanimated/worklets/typescript는 `expo install --check` 정렬에서 제외 |

사실: pinvi 루트 `overrides`가 `react 19.2.6`·`react-dom 19.2.6`·`react-native 0.86.3`·`react-native-reanimated 4.6.0`·`react-native-worklets 0.12.1`을 정확 고정한다(`package.json`). 이는 Expo SDK 정합을 위한 것으로 web까지 React 19.2.6에 묶인다. 후보: mobile을 Tailwind v4로 옮기려면 NativeWind 5 GA가 선행 조건이며, 현재는 preview다.

### 1.8 매트릭스에서 읽히는 사실 요약

1. Next.js: 16.3(airport, pinvi) / 16.2(concierge, geo, map) / 15.5(weather) / 14.2(dm). 최신 16.3.4.
2. React: 19.2.8(airport, concierge, map, weather) / 19.2.6(pinvi, override) / 18.3.1(dm, geo).
3. TypeScript: 5.9.3이 6개 앱, 7.0.2가 airport, 6.0.3이 map-marker-react. 기존 공유 라이브러리도 `maplibre-vworld-js` devDeps `^6.0.3`, `maplibre-vworld-react` 루트 `^5.0.0`으로 갈린다.
4. Tailwind: v4 설치본은 4.3.1(concierge, dm, geo)과 4.3.3(map, pinvi web)으로 좁게 모여 있다. 미도입 2곳(airport, weather), v3 1곳(pinvi mobile).
5. 테스트 스택은 Vitest 4.1.x + Testing Library 16.3.x + Playwright 1.60~1.63으로 사실상 모여 있고 weather(Vitest 3.2.7)만 예외다.
6. 선언 범위가 넓어도(`^5.28.0` 등) lockfile 설치본이 최신 부근으로 모여 있는 패키지(react-query, zustand, react-hook-form)가 있는 반면, lockfile이 오래된 geo(2026-07-28)는 하한도 설치본도 낮은 편이다.

## 2. 백엔드 매트릭스

### 2.1 Python 플랫폼·패키징 방식

| 항목 | airport | concierge | dm | geo | map | weather | pinvi |
|---|---|---|---|---|---|---|---|
| 패키징 | setuptools + `uv.lock` | `requirements.txt` 4개(하한만) | Poetry(`[tool.poetry]`), lock 없음 | setuptools, lock 없음 | setuptools ×3, lock 없음 | setuptools + `uv.lock`(workspace path source) | hatchling ×2 + `apps/api/uv.lock` |
| `requires-python` | `>=3.12` | (없음; `AGENTS.md` "Python 3.10+") | `^3.11` | `>=3.12` (dagster도 `>=3.12`) | `>=3.11` (api·dagster 동일) | `>=3.11` (airkorea `>=3.10`) | `>=3.12` (api·etl) |
| uv.lock `requires-python` | `>=3.12` | — | — | — | — | `>=3.11` | `>=3.12` |
| CI Python | 3.12 (`uv sync --extra dev --locked`) | (CI 없음) | 3.11 (`pip install -e ./backend httpx==0.28.1 pytest==9.1.1 ruff==0.16.4`) | 3.12 (`pip install -e ".[api,loaders,dev]"` + `gdal==$(gdal-config --version)`) | 3.11/3.12/3.13 매트릭스, lint·openapi·postgis job 3.13 (`pip install -e`) | 3.12 (`uv sync --locked --extra dev --extra dagster`) | 3.12 (`pip install -e ".[dev]"`, **uv.lock 미사용**) |
| Docker Python | `python:3.12-slim`, `pip install -e ".[dev]"`(**uv.lock 미사용**) | `python:3.11-slim`, `pip install -r` ×4 | (이미지 없음) | api `python:3.12-trixie`, dagster `python:3.12-slim`, pip | `python@sha256:57cd7c3a…`(builder/runtime 동일; `scripts/create-application-0236-source-oracle.sh:173-178` 주석상 과거 `python:3.12-slim` 태그 — 3.12-slim 계열로 **추정**), pip `--prefix=/install` | `python:3.13-slim` + `ghcr.io/astral-sh/uv:0.11.21`, `uv sync --locked --no-dev` | api·etl `python:3.12-slim@sha256:7a8b4750…`, `pip install -e .`(**uv.lock 미사용**) |
| `[tool.ruff] target-version` | (없음) | (없음) | py311 | py312 | py311 | py311 | py312 |
| `[tool.mypy] python_version` | (없음) | (없음) | (없음) | 3.12 strict | 3.11 strict | 3.11 strict | 3.12 strict |

사실:
- Python lockfile은 3곳에만 있고, 그중 CI와 Docker 양쪽에서 `--locked`로 소비하는 곳은 weather뿐이다. airport는 CI만, pinvi는 어느 쪽도 lock을 쓰지 않는다. 즉 pinvi `apps/api/uv.lock`은 재현성 보장에 기여하지 않는 상태다.
- dm은 Poetry 매니페스트지만 CI는 `pip install -e ./backend`에 도구 3종을 정확 핀으로 덧붙인다. `pytest==9.1.1`은 `[tool.poetry.group.dev.dependencies] pytest = "^8.0.0"` 범위 밖이다(dev 그룹이 CI에서 설치되지 않으므로 충돌은 발생하지 않는다).
- Python 하한은 3.11(dm, map, weather)과 3.12(airport, geo, pinvi)로 갈리고, 실행 이미지는 3.11(concierge) / 3.12(airport, geo, map, pinvi) / 3.13(weather)이다. map CI만 3.13을 검증한다.

### 2.2 웹 프레임워크·검증 라이브러리

| 패키지 | airport | concierge | dm | geo | map(api) | weather | pinvi(api) | 최신 |
|---|---|---|---|---|---|---|---|---|
| fastapi | `>=0.141,<1.0` / 0.141.1 | `>=0.110.0` / 미확인 | `^0.110.0` / 미확인 | `>=0.115`(api extra) / 미확인 | `>=0.115` / 미확인 | `>=0.115` / 0.141.1 | `>=0.115` / 0.141.1 | 0.141.1 (requires `starlette>=0.46.0`, python `>=3.10`) |
| starlette | (전이) 1.6.0 | 미확인 | 미확인 | 미확인 | **`>=0.40,<1.0`**(명시 상한; 주석: starlette 1.0+ TestClient가 httpx2를 요구) / 미확인 | (전이) 1.6.0 | (전이) 1.6.0 | 1.6.0 (`full` extra가 `httpx2>=2.0.0`과 `httpx<0.29`를 병기) |
| uvicorn | `[standard]>=0.52,<1` / 0.52.4 | `>=0.28.0` / 미확인 | `^0.28.0` / 미확인 | `[standard]>=0.32` / 미확인 | `[standard]>=0.30` / 미확인 | `[standard]>=0.30` / 0.52.4 | `[standard]>=0.32` / 0.52.3 | 0.52.4 |
| pydantic | (전이) 2.13.4 | `>=2.6.4` / 미확인 | `^2.6.0` / 미확인 | `>=2.9,<3` / 미확인 | `>=2.7` / 미확인 | `>=2.7` / 2.13.5 | `>=2.9` / 2.13.4 | 2.13.5 |
| pydantic-settings | `>=2.15,<3` / 2.15.0 | `>=2.2.1` / 미확인 | `^2.2.0` / 미확인 | `>=2.5` / 미확인 | `>=2.4` / 미확인 | `>=2.4` / 2.15.0 | `>=2.6` / 2.15.0 | 2.15.0 |
| python-multipart | `>=0.0.32,<1` / 0.0.32 | — | — | — | `>=0.0.20` / 미확인 | — | `>=0.0.12` / 0.0.32 | — |

사실: lock이 있는 세 앱의 설치본은 FastAPI 0.141.1 / Starlette 1.6.0 / uvicorn 0.52.x / pydantic 2.13.x로 동일하다. map api의 `starlette<1.0` 상한은 FastAPI 0.141.1(`starlette>=0.46.0`, 상한 없음)과 충돌하지는 않지만, 다른 세 앱의 Starlette 1.6.0과 major가 다른 해석을 강제한다.

### 2.3 DB·ORM·마이그레이션

| 패키지 | airport | concierge | dm | geo | map | weather | pinvi | 최신 |
|---|---|---|---|---|---|---|---|---|
| sqlalchemy | `>=2.0.52,<3` / 2.0.52 | `>=2.0.28` / 미확인 | `^2.0.0` / 미확인 | `[asyncio]>=2.0.35` / 미확인 | `>=2.0` / 미확인 | `>=2.0` / 2.0.52 | `[asyncio]>=2.0.36` / 2.0.52 | 2.0.52 |
| alembic | `>=1.19,<2` / 1.19.1 | `>=1.13.1` / 미확인 | — | `>=1.13` / 미확인 | **`>=1.19.1,<1.20`** / 미확인 | `>=1.13,<2` / 1.19.1 | `>=1.14` / 1.19.1 | 1.19.2 |
| asyncpg | `>=0.31,<1` / 0.31.0 | `>=0.29.0` / 미확인 | — | — | `>=0.29` / 미확인 | — | `>=0.30` / 0.31.0 (etl `>=0.30`) | 0.31.0 |
| psycopg | — | scheduler `[binary]>=3.1.18` / 미확인 | — | `[binary,pool]>=3.2` / 미확인 | `[binary,pool]>=3.2` / 미확인 | `[binary]>=3.2,<4` / 3.3.4 | — | 3.3.5 |
| geoalchemy2 | — | `>=0.14.7` / 미확인 | — | `>=0.15` / 미확인 | `>=0.15` / 미확인 | — | — | 0.20.0 |
| aiosqlite | `>=0.22,<1` / 0.22.1 | — | — | — | — | — | — | — |

사실: DB 드라이버는 asyncpg(airport, concierge, map, pinvi)와 psycopg 3(geo, map, weather, concierge scheduler)이 혼재하고 map은 둘 다 선언한다. alembic 1.19.x는 lock 3곳에서 동일하나 map만 `<1.20` 상한을 둔다(`pyproject.toml` 주석: named CHECK 비교·drift gate 때문).

### 2.4 HTTP·유틸·관측

| 패키지 | airport | concierge | dm | geo | map | weather | pinvi | 최신 |
|---|---|---|---|---|---|---|---|---|
| httpx | `>=0.28,<1` / 0.28.1 | `>=0.27.0` / 미확인 | dev `^0.27.0`(CI `0.28.1`) | `>=0.27` / 미확인 | `>=0.27,<1.0`(api·dagster·dev) / 미확인 | `>=0.27,<1` / 0.28.1 | `>=0.27` / 0.28.1 | 0.28.1 |
| tenacity | — | — | — | `>=9.0` / 미확인 | — | — | `>=9.0` / 9.1.4 | 9.1.4 |
| structlog | — | — | — | `>=24.4` / 미확인 | — | (전이, dagster) 26.1.0 | `>=24.4` / 26.1.0 (etl `>=24.4`) | 26.1.0 |
| prometheus-client | — | `>=0.20.0` / 미확인 | — | `>=0.21`(api) / 미확인 | `>=0.20`(api) / 미확인 | `>=0.20,<1` / 0.26.0 | `>=0.22` / 0.26.0 | 0.26.0 |
| typer | — | — | — | `>=0.12` / 미확인 | — | — | — | 0.27.2 |
| cryptography | — | — | — | — | — | `>=42` / 50.0.1 | `>=43.0` / 50.0.0 | — |
| boto3 | — | `>=1.34.0` | — | dagster `>=1.34,<2` | `>=1.34` (dagster 동일) | — | `>=1.35` / 1.43.74 | — |
| pyproj | — | `>=3.6.0` | — | — | `>=3.6` | `>=3.5` / 3.7.2 | — | — |

### 2.5 오케스트레이션

| 패키지 | geo(dagster) | map(dagster) | weather | pinvi(etl) | 최신 |
|---|---|---|---|---|---|
| dagster | `>=1.9,<2` / 미확인 | `>=1.9,<2` / 미확인 | `>=1.9,<2` / 1.13.20 | `>=1.9` / (etl에는 lock 없음) | 1.13.21 |
| dagster-webserver | `>=1.9,<2` | `>=1.9,<2` | `>=1.9,<2` / 1.13.20 | `>=1.9` | 1.13.21 |
| dagster-postgres | `>=0.25,<1` | `>=0.25,<1` | — | — | — |
| 본체 라이브러리 핀 | `kor-travel-geo==0.1.0` | `kor-travel-map==0.2.0-dev` | path editable | — | — |

### 2.6 테스트·품질 도구

| 패키지 | airport | concierge | dm | geo | map | weather | pinvi | 최신 |
|---|---|---|---|---|---|---|---|---|
| pytest | `>=9.1,<10` / 9.1.1 | `>=8.1.1` | `^8.0.0`(CI `9.1.1`) | `>=8.3` | `>=8` | `>=8` / 9.1.1 | `>=8.3` / 9.1.1 | 9.1.1 |
| pytest-asyncio | `>=1.4,<2` / 1.4.0 | `>=0.23.5` | — | `>=0.24` | `>=0.23` | `>=0.23` / 1.4.0 | `>=0.24` / 1.4.0 | 1.4.0 |
| pytest-cov | `>=7.1,<8` / 7.1.0 | — | — | — | `>=5` | — | — | — |
| ruff | — | — | `^0.3.0`(CI `0.16.4`) | `>=0.7`(pre-commit `v0.7.4`) | `>=0.5` | `>=0.9` / 0.16.5 | `>=0.7` / 0.16.3 | 0.16.6 |
| mypy | — | — | `^1.9.0` | `>=1.13`(pre-commit `v1.13.0`) | `>=1.10` | `>=1.13` / **2.3.1** | `>=1.13` / **2.3.1** | 2.3.1 |
| import-linter | — | — | — | `>=2.0` | `>=2.0` | — | — | 2.15 |
| testcontainers | — | — | — | `[postgres]>=4.8` | `[postgres]>=4` | — | `[postgres]>=4.8` / 4.15.0 | 4.15.0 |
| hypothesis | — | — | — | `>=6.115` | `>=6.100` | — | — | — |
| pre-commit | — | — | — | `>=4.0` | `>=3.7`(`minimum_pre_commit_version 3.7.0`) | — | — | 4.6.2 |

사실: mypy는 2026년에 2.x major가 나왔고 lock이 있는 weather·pinvi는 2.3.1을 설치한다. 하한이 `>=1.13`·`^1.9.0`인 앱은 lock이 없으면 설치 시점에 따라 1.x 또는 2.x가 잡힌다. geo의 pre-commit은 ruff `v0.7.4`·mypy `v1.13.0`으로 고정돼 CI(하한만)와 다른 버전이 로컬에서 돈다.

### 2.7 자체 provider 라이브러리 git 핀 (중복 금지 대상 `digitie/python-*-api`)

| 라이브러리 | airport | map | weather | pinvi(etl) | concierge |
|---|---|---|---|---|---|
| python-kasi-api | `@51c39c1b…` (lock 0.1.0) | (주석 처리) | — | **`@main`**(floating) | — |
| python-krairport-api | `@cbe4d138…` (lock 0.1.0) | `@cbe4d138…`(동일) | — | — | — |
| python-kma-api | — | `@a75d1e15…` | **`@0868b76b…`**(lock 0.1.0) — map과 다른 SHA | — | — |
| python-airkorea-api | — | `@c4c8d122…` | 저장소 내 `packages/python-airkorea-api` path source 0.4.0 | — | — |
| python-vworld-api | — | — | — | — | GitHub zip `@a1fea840…` |
| 기타 | — | datagokr·khoa·opinet·krex·visitkorea·knps·krforest·krheritage·mois·mcst 각 SHA 핀(`providers` extra) | — | — | — |

사실: 같은 provider가 저장소마다 다른 SHA(kma: map ≠ weather)이거나 floating(`@main`, pinvi etl)이다. weather는 airkorea를 저장소 안에 vendoring한다. 공통 정책이 "provider SHA 레지스트리"를 다뤄야 하는지는 열린 질문이다(§열린 질문).

## 3. 도구·CI·컨테이너 매트릭스

### 3.1 GitHub Actions

| 액션 | airport | dm | geo | map | weather | pinvi | 최신 릴리스(§4.4) |
|---|---|---|---|---|---|---|---|
| actions/checkout | v4 | `@11bd7190…`(= v4.2.2) | v4 | v4 | v4 | v4 | v7.0.1 |
| actions/setup-node | v4 | `@49933ea5…`(= v4.4.0) | v4 | v4 | v4 | v4 | v7.0.0 |
| actions/setup-python | v5 | `@a26af69b…`(= v5.6.0) | v5 | v5 | v5 | v5 | v7.0.0 |
| astral-sh/setup-uv | v6 | — | — | v6(설치 후 실제로는 pip 사용) | v5 | — | v10.0.1 |
| actions/upload-artifact / download-artifact | — | — | — | v4 / v4 | — | v4 / — | v7.0.1 / v8.0.1 |
| docker/setup-buildx-action | — | — | — | v3 | — | — | v4.3.0 |
| actions/github-script | — | — | — | — | — | v7 | v9.0.0 |
| runner | ubuntu-latest | **ubuntu-24.04**(고정) | ubuntu-latest | ubuntu-latest | ubuntu-latest | ubuntu-latest | — |
| concierge | (워크플로 없음) | | | | | | |

사실: 액션 major는 저장소 간 동일(v4/v5)하나 최신 major보다 2~4단계 낮다. SHA 핀은 dm만 쓴다. concierge는 CI가 없다.

### 3.2 CI 런타임 버전과 설치 방식

| 항목 | airport | dm | geo | map | weather | pinvi |
|---|---|---|---|---|---|---|
| Node | 22 | 20 | 20 | 22.23.1 | 20 | 22 |
| npm | 기본(Node 22 동봉 10.9.x) | 기본 | 기본 | `npx --yes npm@12.0.1` 강제 | 기본 | `npm install -g npm@11.19.1` |
| npm 설치 명령 | `npm ci` | `npm ci` | `npm ci` | `npm ci --workspaces --include=optional --no-audit --no-fund` + `audit:high`·`verify:npm-tree`·`verify:next-sharp`·`verify:frontend-eslint`·`verify:react-doctor-config` | `npm ci --ignore-scripts --no-audit --no-fund` | `check:lockfile` → `npm ci --no-audit --no-fund` → lint/typecheck/test/build(workspaces) |
| Python | 3.12 | 3.11 | 3.12 | 3.11/3.12/3.13 | 3.12 | 3.12 |
| Python 설치 | `uv sync --extra dev --locked` | `pip install -e ./backend` + 3종 정확 핀 | `pip install -e ".[api,loaders,dev]"` | `pip install -e ".[dev]"` ×3 패키지 | `uv sync --locked --extra dev --extra dagster` | `pip install -e ".[dev]"` |
| DB 서비스 | `postgres:16` | (없음) | (없음) | (testcontainers, `postgis@sha256:dc17b064…`) | `postgres:16` | `postgis/postgis:16-3.5-alpine` |

Node 22 동봉 npm이 10.9.x이므로(`nodejs.org/dist/index.json`: v22.23.2 → npm 10.9.8, v24.20.0 → npm 11.19.0, v26.8.1 → npm 11.19.0) pinvi(`>=11`)와 map(`12.0.1`)은 별도로 npm을 올려야 한다는 것이 두 CI의 명시 이유다(`.github/workflows/web.yml:71-73`, `verify-npm-tree.mjs:4`).

### 3.3 Docker 베이스 이미지

| 앱 | 프론트엔드 | 백엔드 | 기타 |
|---|---|---|---|
| airport | `node:22-alpine` | `python:3.12-slim` | — |
| concierge | `node:22-slim` | `python:3.11-slim`(api/mcp/scheduler/etl 공용) | — |
| dm | (없음) | (없음) | — |
| geo | `node:22-alpine`(deps/builder/runner) | api `python:3.12-trixie`, dagster `python:3.12-slim` | — |
| map | `node:22.23.1-bookworm-slim@sha256:6c74791e…` | `python@sha256:57cd7c3a…`(api·dagster) | `mcr.microsoft.com/playwright:v1.60.0-noble@sha256:9bd26ad9…` |
| weather | `node:22-alpine` | `python:3.13-slim` + `ghcr.io/astral-sh/uv:0.11.21` | `nginx:1.27-alpine`(dagster gateway) |
| pinvi | `node:22-bookworm-slim@sha256:83f487e0…` | `python:3.12-slim@sha256:7a8b4750…`(api·etl) | `nginx:1.27-bookworm@sha256:6784fb08…`; `# syntax=docker/dockerfile:1.7.1-labs@sha256:…` |

사실: Node 이미지는 전부 22 계열이지만 변형(alpine / slim / bookworm-slim)과 핀 방식(태그 / digest)이 다르다. digest 핀은 map·pinvi만 쓴다.

### 3.4 DB·인프라 이미지

| 이미지 | airport | dm(`docker-compose.yml`) | map | weather | pinvi | concierge |
|---|---|---|---|---|---|---|
| PostgreSQL/PostGIS | `postgres:16-alpine`(compose db/live) | geo·concierge용 `postgis/postgis:16-3.5`; pinvi용 `postgis/postgis@sha256:8b33190b…`; map용 `${KOR_TRAVEL_MAP_POSTGRES_IMAGE_ID:?…}` 필수 지정; 보조 `postgres:16-alpine` | `postgis/postgis@sha256:dc17b064…`(과거 `postgis/postgis:16-3.5-alpine` 태그를 digest로 고정 — `docs/archive/journal-2026-08a.md:314-318`); 보조 `postgres:16-alpine` | `postgres:16-alpine` | dev `postgis/postgis:16-3.5-alpine`; app `postgis/postgis@sha256:8b33190b…`(dm과 동일 digest, `docs/architecture.md:147`) | 외부 DB(`host.docker.internal:5432`; dm이 관리) |
| RustFS / mc | — | `rustfs/rustfs:latest`, `minio/mc:latest` | `rustfs/rustfs:latest`, `minio/mc:latest`, `alpine:3.20` | — | dev `latest`; app digest `rustfs@sha256:41fe8938…`, `mc@sha256:a7fe349e…` | `rustfs/rustfs:latest` |
| 관측 | — | `prom/prometheus:v2.53.1`, `grafana/grafana:11.1.4`, `gcr.io/cadvisor/cadvisor:v0.52.1` | — | `prom/prometheus:v3.5.0` | prometheus v2.53.1, grafana 11.1.4, cadvisor v0.52.1, `prom/blackbox-exporter:v0.25.0` | — |

사실: DB는 전 저장소가 PostgreSQL 16 + PostGIS 3.5 계열이다(최신 PostgreSQL 18.6 / PostGIS 이미지 `18-3.6`, §4.4). Prometheus는 dm·pinvi(v2.53.1)와 weather(v3.5.0)가 major가 다르다. `latest` 태그 사용은 RustFS/mc(dm, map, concierge, pinvi dev)에 남아 있다.

### 3.5 pre-commit

| 저장소 | 파일 | 훅 | 버전 |
|---|---|---|---|
| geo | `.pre-commit-config.yaml` | `astral-sh/ruff-pre-commit` ruff(--fix), `pre-commit/mirrors-mypy` mypy(+ additional_dependencies 11종), local `import-linter` | ruff `v0.7.4`, mypy `v1.13.0` |
| map | `.pre-commit-config.yaml` | local: journal 필수 검사, prod redaction, `ruff format --check`, `mypy --strict`, `lint-imports`(모두 시스템 설치본 사용) | `minimum_pre_commit_version: "3.7.0"`; 도구 버전은 환경에 위임 |
| airport, concierge, dm, weather, pinvi | 없음 | — | — |

### 3.6 lockfile·트리 검증 관행(선행 사례)

| 저장소 | 장치 | 내용 |
|---|---|---|
| map | `scripts/verify-npm-tree.mjs` | npm 실행기가 정확히 `12.0.1`인지, `npm ls --all --json`의 `problems`가 0개인지 검사 |
| map | `scripts/verify-next-sharp.mjs` | 설치된 `next`가 `16.2.12`, `sharp` ABI가 `0.35.3`인지 상수 대조 후 이미지 최적화 실제 실행 |
| map | `scripts/patch-redocly-openapi-core.mjs`(postinstall) | `@redocly/openapi-core`가 검증된 `1.34.17`이 아니면 실패, vendor patch 적용 |
| map | `package.json` `overrides`·`allowScripts` | `next.postcss 8.5.23`, `next.sharp 0.35.3`, `@redocly/openapi-core.{js-yaml 4.3.0, minimatch 10.2.5}`; 설치 스크립트 허용 목록 `esbuild@0.28.1`, `unrs-resolver@1.12.2` |
| pinvi | `scripts/check-lockfile-integrity.mjs` | lock 항목의 `integrity` 보유율이 99% 미만이면 실패(`--package-lock-only` 재생성 사고 T-352/T-358 재발 방지) |
| pinvi | `package.json` `overrides` | react/react-dom/react-native/reanimated/worklets 정확 고정, postcss·sharp 상향 |
| airport | `docs/architecture/dependencies.md` | 사람이 읽는 버전 기준선(2026-08-22 갱신, "Major 업데이트는 lock 갱신 후 WSL·Docker·live E2E 통과 필요") |
| dm | `.github/workflows/ci.yml` | 액션 SHA 핀 + 도구 3종 정확 핀 |
| dm | `docs/runtime-pin-registry.md`, `config/runtime-pins.seed.json` | Map·PinVi **소스 revision** 레지스트리(§7.3) |
| 전체 | renovate / dependabot 설정 | **없음**(7개 저장소 모두 `git ls-files`에 `renovate*`·`dependabot*` 없음) |

## 4. 최신 안정 버전 조사 (2026-09-06)

### 4.1 실행 명령

```
npm view <pkg> version            # 로컬 node v25.9.0 / npm 11.12.1, registry.npmjs.org
npm view <pkg> time --json        # 릴리스 일자
npm view <pkg> peerDependencies|engines|dist-tags --json
curl -s https://pypi.org/pypi/<pkg>/json | jq .info.version   # (python -c 로 동일 처리)
curl -s https://pypi.org/pypi/fastapi/<ver>/json               # requires_dist 확인
curl -s https://endoflife.date/api/{nodejs,python,postgresql}.json
curl -s https://api.github.com/repos/<owner>/<action>/releases/latest
curl -s "https://hub.docker.com/v2/repositories/postgis/postgis/tags?page_size=100&name=18"
curl -s https://nodejs.org/dist/index.json                      # Node 동봉 npm
git ls-remote --tags https://github.com/actions/<action>       # SHA→태그
```

모든 조회는 성공했다(네트워크 불가 항목 없음). 값은 조회 시점(2026-09-06) 기준이며 하루 뒤에도 달라질 수 있다.

### 4.2 npm (사실)

| 패키지 | latest | 비고(릴리스 일자·peer) |
|---|---|---|
| next | 16.3.4 | 16.3.0 2026-08-03, 16.3.4 2026-08-31; 16.2.0 2026-03-18; 15.5.24 2026-08-25(backport); 14.2.35 2025-12-11; engines `node >=20.9.0`; peer react `^18.2.0 \|\| ^19.0.0` |
| react / react-dom | 19.2.8 | 19.0.0 2024-12-05, 19.2.0 2025-10-01; 18.3.1 2024-04-26 |
| typescript | 7.0.2 | 7.0.2 2026-07-08(`latest`); 6.0.2 2026-03-23, 6.0.3 2026-04-16; 5.9.3 2025-09-30; dist-tags `rc 7.0.1-rc`, `next 7.1.0-dev.20260905.1`; 7.0.2는 플랫폼별 `@typescript/typescript-<os>-<arch>` optional 바이너리로 구성 |
| tailwindcss / @tailwindcss/postcss | 4.3.3 | 4.0.0 2025-01-21, 4.3.0 2026-05-08, 4.3.3 2026-07-16 |
| postcss | 8.5.28 | |
| @base-ui/react | 1.8.0 | peer react `^17 \|\| ^18 \|\| ^19` |
| radix-ui | 1.6.7 | peer react `^16.8 \|\| … \|\| ^19.0` |
| shadcn | 4.21.0 | deps `zod ^3.24.1` |
| class-variance-authority / clsx / tailwind-merge / tw-animate-css | 0.7.1 / 2.1.1 / 3.6.0 / 1.4.0 | |
| lucide-react | 1.41.0 | 1.0.0 2026-03-23, 1.41.0 2026-09-04 |
| @tanstack/react-query | 5.102.8 | |
| @tanstack/react-table | 9.2.4 | 9.0.0 2026-08-04; peer react `>=18` |
| @tanstack/react-virtual | 3.14.10 | |
| zustand | 5.0.15 | |
| react-hook-form / @hookform/resolvers | 7.87.0 / 5.9.1 | resolvers peer `zod ^3.25 \|\| ^4`, `react-hook-form ^7.55.0` |
| zod | 4.5.4 | 4.0.0 2025-07-09, 4.5.4 2026-08-29 |
| sonner | 2.0.8 | 2026-08-09 |
| maplibre-gl | 6.7.0 | 5.24.0 2026-04-23, 6.0.0 2026-07-22, 6.7.0 2026-09-02 |
| next-intl | 4.14.2 | |
| eslint / eslint-config-next / typescript-eslint | 10.10.0 / 16.3.4 / 8.69.0 | eslint 10.0.0 2026-02-06, engines `^20.19 \|\| ^22.13 \|\| >=24`; eslint-config-next peer `eslint >=9`; **typescript-eslint peer `typescript >=4.8.4 <6.1.0`** |
| eslint-plugin-react-hooks | 7.1.1 | |
| vitest / @vitejs/plugin-react | 5.0.0 / 6.1.1 | vitest 5.0.0 2026-09-03, engines `^22.12 \|\| ^24 \|\| >=26`, peer vite `^6.4 \|\| ^7 \|\| ^8` |
| @testing-library/react / jest-dom / user-event | 16.3.3 / 7.0.1 / 14.6.7 | |
| @playwright/test | 1.63.0 | |
| jsdom | 30.0.1 | |
| react-doctor | 0.9.13 | dev 태그가 하루 단위로 갱신 중 |
| openapi-typescript | 7.13.0 | |
| expo / react-native / nativewind | 57.0.20 / 0.87.1 / 4.2.6 | nativewind `preview` 5.0.0-preview.4 |
| @types/node / @types/react / @types/react-dom | 26.4.1 / 19.2.18 / 19.2.7 | |
| npm | 12.0.2 | 12.0.0 2026-07-08, 12.0.1 2026-07-10, 12.0.2 2026-07-29; 11.19.1 2026-08-26 |

### 4.3 PyPI (사실)

| 패키지 | latest | 비고 |
|---|---|---|
| fastapi | 0.141.1 | requires `starlette>=0.46.0`, `pydantic>=2.9.0`, python `>=3.10`. 0.130.0에서 `starlette<1.0.0` 상한, 0.135.0부터 상한 제거 |
| starlette | 1.6.0 | `full` extra: `httpx2>=2.0.0`, `httpx<0.29,>=0.27` 병기; python `>=3.10` |
| uvicorn | 0.52.4 | |
| pydantic / pydantic-settings | 2.13.5 / 2.15.0 | |
| sqlalchemy / alembic | 2.0.52 / 1.19.2 | |
| asyncpg / psycopg / geoalchemy2 | 0.31.0 / 3.3.5 / 0.20.0 | |
| httpx / tenacity / structlog / prometheus-client / typer | 0.28.1 / 9.1.4 / 26.1.0 / 0.26.0 / 0.27.2 | |
| dagster / dagster-webserver | 1.13.21 / 1.13.21 | |
| pytest / pytest-asyncio | 9.1.1 / 1.4.0 | |
| ruff / mypy / import-linter / testcontainers | 0.16.6 / 2.3.1 / 2.15 / 4.15.0 | mypy는 2.x major |
| uv / poetry / pre-commit | 0.12.10 / 2.4.3 / 4.6.2 | |

### 4.4 런타임·플랫폼·액션·이미지 (사실)

| 항목 | 값 | 출처 |
|---|---|---|
| Node.js | 26.8.1 최신(LTS 전환 2026-10-28, EOL 2029-04-30); 24.20.0 Active LTS(Active 종료 2026-10-20, EOL 2028-04-30); 22.23.2 Maintenance(Active 종료 2025-10-21, EOL 2027-04-30); **20.20.2 EOL 2026-04-30**; 25는 Current(EOL 2026-06-01) | endoflife.date |
| Node 동봉 npm | v22.23.2 → 10.9.8, v24.20.0 → 11.19.0, v26.8.1 → 11.19.0 | nodejs.org/dist/index.json |
| Python | 3.14.7(EOL 2030-10-31); 3.13.15(bugfix 2026-10-01까지, EOL 2029-10-31); 3.12.14(security-only, EOL 2028-10-31); 3.11.16(EOL 2027-10-31); 3.10.21(EOL 2026-10-31) | endoflife.date |
| PostgreSQL | 18.6 / 17.11 / 16.15(EOL 2028-11-09) / 15.19 / 14.24(EOL 2026-11-12) | endoflife.date |
| postgis/postgis 이미지 태그 | `18-3.6`, `18-3.6-alpine`, `17-3.6-alpine`, `17-3.5`, `17-3.4` | Docker Hub API |
| GitHub Actions | checkout v7.0.1, setup-node v7.0.0, setup-python v7.0.0, astral-sh/setup-uv v10.0.1, upload-artifact v7.0.1, download-artifact v8.0.1, docker/setup-buildx-action v4.3.0, github-script v9.0.0 | GitHub releases API |
| TypeScript 7 특성 | Go 네이티브 포트. 컴파일러 API(`lib/typescript.js`) 미제공(README "API: not ready"); `baseUrl`·`outFile`·`target ES5`·`module AMD/System/UMD`·`moduleResolution classic/node10`·`alwaysStrict:false`·`esModuleInterop:false` 등 제거(`internal/compiler/program.go`); JSDoc/expando/CommonJS 일부 패턴 제거(`CHANGES.md`) | Context7 `/microsoft/typescript-go` |
| Next.js × TS 7 | TS 7에는 컴파일러 API가 없어 Next가 프로젝트 로컬 `tsc` CLI로 타입 검사(`experimental.useTypeScriptCli`); API 부재 시 "TS 6를 설치하거나 CLI 모드"를 안내(`packages/next/src/lib/typescript/runTypeScriptCli.ts`) | Context7 `/vercel/next.js` |

## 5. 정렬 목표 후보와 격차·난이도

### 5.1 후보 기준선 (후보 — 결정 아님)

| 축 | 후보 A: 현재 다수와 최소 이동 | 후보 B: 2026-09 최신 안정 | 판단 근거(사실) |
|---|---|---|---|
| Node 런타임 | 22.x(모든 Docker 이미지가 이미 22; CI 20 사용처 3곳만 22로) | 24.x Active LTS(2026-10-20까지 Active) 또는 26.x(2026-10-28 LTS) | map `engines`는 `^22.22.2 \|\| ^24.15.0 \|\| >=26`으로 둘 다 허용. Vitest 5 최소 22.12. Node 20은 EOL |
| npm | 11.19.x(Node 24/26 동봉 11.19.0과 일치) | 12.0.2 | map 12.0.1 강제 vs pinvi 11.19.1 강제. Node 동봉 npm이 11.19.0이므로 12는 별도 설치 필요 |
| Next.js | 16.3.x | 16.3.4 | airport·pinvi 이미 16.3; 16.2 → 16.3 minor 3곳; weather major 1, dm major 2 |
| React | 19.2.x | 19.2.8 | dm·geo 18.3.1이 유일한 major 격차 |
| TypeScript | **5.9.3**(6개 앱) | 7.0.2 | typescript-eslint 8.69.0 peer `<6.1.0`: TS 7은 lint 스택과 정합하지 않음. 6.0.3은 "bridge"(deprecation) 릴리스 — 미확인(공식 릴리스 노트 미조회) |
| Tailwind | 4.3.3 | 4.3.3 | 5개 앱 4.3.1~4.3.3; airport·weather 신규 도입; mobile은 NativeWind 5 GA 대기 |
| primitive | Base UI 1.8.0 | 1.8.0 | concierge 1.5 / map 1.6 / pinvi 1.8; geo Radix 1.6.0 |
| ESLint | 9.39.x 또는 10.x | 10.10.0 | map만 10; dm 8은 EOL(9.0 이후) — 추정 |
| Vitest | 4.1.x | 5.0.0(3일 경과) | weather 3.2.7만 격차 |
| Playwright | 1.63.0 | 1.63.0 | map은 1.60.0 정확 핀 + Docker 이미지 동시 갱신 필요 |
| Python | `requires-python >=3.12`, 이미지 3.12-slim | 이미지 3.13-slim(weather 선례), 3.14 미검증 | 3.12는 security-only; map CI만 3.13 검증; geo GDAL 바인딩은 시스템 libgdal 버전 핀 |
| FastAPI 계열 | 0.141.x / Starlette 1.6 / uvicorn 0.52 / pydantic 2.13 | 동일 | lock 3곳 설치본 일치; map api `starlette<1.0` 상한이 예외 |
| SQLAlchemy / alembic | 2.0.52 / 1.19.x | 동일 | map `alembic<1.20` 상한 |
| dagster | 1.13.x | 1.13.21 | |
| pytest / pytest-asyncio | 9.1.x / 1.4.x | 동일 | dm poetry `^8` 하한만 불일치 |
| ruff / mypy | 0.16.x / 2.3.x | 0.16.6 / 2.3.1 | geo pre-commit(0.7.4 / 1.13.0)이 가장 멀다 |
| PostgreSQL/PostGIS | 16 + 3.5(digest 핀, dm·map·pinvi 선례) | 17/18 + 3.6 | DB major는 데이터 마이그레이션 문제 — 라이브러리 정렬과 분리 필요(후보) |
| GitHub Actions | checkout v4/setup-node v4/setup-python v5 유지 + SHA 핀(dm 선례) | v7/v7/v7 | — |

### 5.2 앱별 격차와 업그레이드 난이도 (후보 기준선 A=Next 16.3 / React 19.2 / TS 5.9 / Tailwind 4.3 / Base UI 1.8 / ESLint 9+ / Vitest 4.1 / Node 22 / Python ≥3.12 / uv.lock 기준)

| 앱 | major 격차 | minor·patch 격차 | 추가 작업 | 난이도(추정) |
|---|---|---|---|---|
| airport | TypeScript 7 → 5.9 **하향**이 필요한지(§6) | next 16.3.2 → 16.3.4 | Tailwind·ESLint 신규 도입; Docker에서 uv.lock 사용; `engines` 선언 | 낮음~중간 |
| concierge | maplibre-gl 6 → 5(공유 라이브러리 peer) 또는 공유 라이브러리를 6으로; @hookform/resolvers 3 → 5 | next 16.2.7 → 16.3; base-ui 1.5 → 1.8; lucide 1.17 → 1.41 | CI 부재; Python lock 부재(`requirements.txt` 하한만, `mcp<2` 사고 이력 주석); `shadcn` CLI를 `dependencies`에서 제거 여부; `autoprefixer` 불필요 여부(v4) — 후보; Node 문서(20.9+)와 `engines`(>=22) 정합 | 중간 |
| dm | **Next 14 → 16**(2 major), **React 18 → 19**, ESLint 8 → 9+/eslint-config-next 14 → 16, lucide 0.363 → 1.x, `@vitejs/plugin-react` 6(이미 최신) | tailwind 4.3.1 → 4.3.3 | Poetry → lock 도입(또는 uv), fastapi `^0.110`·uvicorn `^0.28`·ruff `^0.3`·mypy `^1.9` 하한 상향, CI Node 20 → 22, `pytest ^8` vs CI 9.1.1 정리 | **높음** |
| geo | **React 18 → 19**(ADR-019가 18 유지를 명시 결정), Radix → Base UI(정책 채택 시), lucide 0.468 → 1.x, jsdom 25 → 30 | next 16.2.12 → 16.3; tailwind 4.3.1 → 4.3.3 | CI Node 20 → 22; Python lock 도입; pre-commit ruff 0.7.4 → 0.16 / mypy 1.13 → 2.3(strict 규칙 변화 검토); lock 2026-07-28 이후 미갱신 | **높음**(UI) / 중간(Python) |
| map | TS 6.0.3(marker) vs 5.9.3(admin) 통일 | next 16.2.12 → 16.3(`verify-next-sharp.mjs` 상수 동반 수정); base-ui 1.6 → 1.8; Playwright 1.60 → 1.63(+이미지) | Python lock 도입; `starlette<1.0`·`alembic<1.20` 상한 재검토; npm 12.0.1 강제와 pinvi 11.19.1 강제의 합의 | 낮음~중간 |
| weather | **Next 15 → 16**, Vitest 3 → 4/5, eslint-config-next 15 → 16, react-hooks plugin 5.2 → 7 | — | Tailwind 신규 도입(현재 `tokens.css` 기반); CI Node 20 → 22; Python 이미지 3.13-slim은 이미 최신 편 | 중간~높음 |
| pinvi web | @hookform/resolvers 3 → 5, jsdom 25 → 30, lucide 0.460 → 1.x | react 19.2.6(override) → 19.2.8 | uv.lock을 CI·Docker에서 실제 사용; TS `^5.6.0` 하한 상향 | 중간 |
| pinvi mobile | **Tailwind 3 → 4는 NativeWind 5 GA 필요**(현재 preview) | expo 57 문서/매니페스트 정합 | react-native 0.86.3 정확 핀은 Expo SDK 정합용 — common이 건드릴 영역인지 열린 질문 | **높음**(외부 의존) |

### 5.3 breaking change 근거

| 전환 | 근거(사실) | 조사 대상에서의 영향 |
|---|---|---|
| React 18 → 19 | `ref`가 일반 prop이 되어 `forwardRef` 불필요; `propTypes`·함수 컴포넌트 `defaultProps`·string ref·`createFactory`·legacy context 제거; `react-test-renderer` deprecated(Context7 `/react/react` CHANGELOG) | geo `Button`은 Radix `Slot`+`forwardRef` 기반(선행 보고서 §3.3); dm 프론트엔드도 React 18 |
| Next 14 → 16 | Next 16에서 `cookies()`·`headers()`·`draftMode()`·`params`·`searchParams` 동기 접근 완전 제거(15에서 도입된 Async Request API의 호환 계층 삭제); `middleware` → `proxy` 파일 규약; `next lint` 제거 → ESLint CLI; codemod `npx @next/codemod@canary upgrade latest` 제공; engines `node >=20.9.0`(Context7 `/vercel/next.js` version-16.mdx) | dm(14.2.35), weather(15.5.24). geo는 이미 `proxy.ts`로 전환(`docs/journal.md:872`) |
| Radix → Base UI | Base UI 1.8.0 peer는 React 17/18/19 모두 허용 → React 19 업그레이드와 독립적으로 진행 가능(npm peer) | geo만 Radix. 컴포넌트 계약(`asChild` vs `render`) 차이는 선행 보고서 §3.3이 다룸 |
| TypeScript 5.9 → 7 | 컴파일러 API 부재(도구 생태계 영향), `baseUrl`·`node10`·`ES5` 등 제거; typescript-eslint 8.69.0 peer `<6.1.0`; Next는 CLI 모드로 우회 | airport만 7. tsconfig는 `moduleResolution: bundler`·`target ES2022`라 제거 옵션에 걸리지 않음(§6). map-marker-react·maplibre-vworld-js는 6.0.3 |
| Tailwind 3 → 4 | CSS-first `@theme`, `@tailwindcss/postcss`, `tailwind.config.js` 선택화(dm ADR-17 `docs/decisions.md:527`, NativeWind v5 migrate 문서) | pinvi mobile은 NativeWind 4 → 5 전환이 전제 |
| ESLint 8 → 9/10 | eslint-config-next 16 peer `eslint >=9`; eslint 10 engines `^20.19 \|\| ^22.13 \|\| >=24` | dm |
| Vitest 4 → 5 | engines Node `^22.12 \|\| ^24 \|\| >=26` | Node 20 CI(dm, geo, weather)에서는 설치 불가 |
| @tanstack/react-table 8 → 9 | 9.0.0 2026-08-04 출시(변경 내용은 미조회 — 미확인) | geo·map·pinvi DataTable |
| lucide-react 0.x → 1.x | 1.0.0 2026-03-23(변경 내용 미조회 — 미확인) | dm·geo·weather·pinvi |
| mypy 1 → 2 | 2.3.1 latest(변경 내용 미조회 — 미확인) | lock 있는 weather·pinvi는 이미 2.3.1; geo pre-commit 1.13.0 |

## 6. airport의 `typescript ^7.0.2` 검증

사실(파일·lock·CI 로그 근거):

| 항목 | 근거 | 값 |
|---|---|---|
| 선언 | `frontend/package.json` devDependencies | `"typescript": "^7.0.2"` — `481cb78`(2026-08-22)에서 `^5.8.3` → `^7.0.2`로 변경 |
| 설치 | `frontend/package-lock.json` `packages["node_modules/typescript"]` | `version 7.0.2`, `resolved https://registry.npmjs.org/typescript/-/typescript-7.0.2.tgz`, `license Apache-2.0`, `bin.tsc bin/tsc`, `engines.node >=16.20.0`, `optionalDependencies`로 `@typescript/typescript-{darwin,linux,win32,…}-{x64,arm64,…}@7.0.2` 20종 |
| 문서 | `docs/architecture/dependencies.md` | "Frontend: Next.js 16.3.2, React/React DOM 19.2.8, TypeScript 7.0.2, Vitest 4.1.11, Playwright 1.62.1"(2026-08-22) |
| tsconfig | `frontend/tsconfig.json` | `target ES2022`, `module esnext`, `moduleResolution bundler`, `strict`, `noEmit`, `plugins: [{name: "next"}]` — TS 7에서 제거된 `baseUrl`·`node10`·`ES5`·`outFile` 미사용 |
| CI 단계 | `.github/workflows/ci.yml` frontend job | `npm ci` → `npm run test -- --run`(vitest) → `npx tsc -p tsconfig.test.json --noEmit` → `npm run build`(`next build`) |
| CI 결과 | `gh run list/view --repo digitie/kor-travel-airport --branch main` | run 32668739519(`8cafd8f`, 2026-08-23): backend·frontend·live-e2e 모두 success. run 33992484153(`395717b`)·33997589658(`b893d0b`)·33997890538(**`2bb1111`**, 2026-09-05): **frontend success, backend success, live-e2e failure** |
| next.config | `frontend/next.config.ts` | `experimental.useTypeScriptCli`·`typescript.ignoreBuildErrors` 미설정 → Next 기본 동작(TS 7 감지 시 로컬 `tsc` CLI 타입 검사; Context7 Next 문서) |

결론:
- TypeScript 7.0.2는 lockfile에 실제로 해석·고정돼 있고, 기준 커밋 `2bb1111`의 GitHub Actions에서 `tsc --noEmit`과 `next build`가 통과했다(사실). 따라서 "선언만 7이고 실제로는 5가 설치된다"는 가설은 기각된다.
- `live-e2e` 실패는 외부 URL(`E2E_BASE_URL=https://<prod-host>`)에 대한 E2E job이며 TypeScript와 무관하다는 것은 job 이름·env로부터의 **추정**이다(로그 미열람).
- airport에는 ESLint·typescript-eslint가 없어 TS 7의 생태계 제약이 드러나지 않는다. 다른 앱이 따라가면 typescript-eslint(peer `<6.1.0`) 문제가 발생한다(사실). 즉 "airport가 7에서 동작한다"는 것이 "전 앱 7 정렬이 가능하다"를 뜻하지 않는다.
- 후보: 정책상 TS 기준선을 5.9.x로 두고 airport를 하향하거나, 6.x를 중간 단계로 두고 typescript-eslint 지원 범위 확장을 기다린다. 어느 쪽이든 결정은 TS 7이 필요한 이유(빌드 속도 등)가 airport 문서에 기록돼 있지 않으므로(미확인) 확인 후에 한다.

## 7. 버전 핀 정책 후보

### 7.1 현재 관행 요약

| 관행 | 사용처 | 비고 |
|---|---|---|
| caret 선언 + lockfile | 다수(airport, concierge, dm, geo, weather, pinvi 대부분) | 하한이 설치본보다 크게 낮은 곳 다수(dm react-query `^5.28`, concierge rhf `^7.51.5`) |
| 정확 핀 | map `next 16.2.12`, `@playwright/test 1.60.0`, `pretendard 1.3.9`, `engines.npm 12.0.1`; pinvi `next 16.3.3`, `eslint-config-next 16.3.3`, 루트 override react/RN; concierge `pretendard 1.3.9`; dm CI 도구 3종·액션 SHA | 정확 핀 + 상수 검증 스크립트(map)가 가장 강한 형태 |
| overrides | map, pinvi, concierge | 전이 의존성 보안 상향(postcss, sharp, js-yaml, minimatch) |
| Python 상한 명시 | airport(`<1.0`, `<2.0` 등 전부), map(`starlette<1.0`, `alembic<1.20`), geo(`pydantic<3`), weather(`<1`, `<2`, `<4`) | dm(Poetry caret), pinvi·concierge는 하한만 |
| Python lock 소비 | weather(CI+Docker `--locked`), airport(CI만), pinvi(미소비) | geo·map·dm·concierge lock 없음 |
| 자동 갱신 봇 | 없음 | — |
| 버전 기준 문서 | airport `docs/architecture/dependencies.md` | 다른 저장소는 ADR·journal에 분산 |

### 7.2 정책 후보

| 후보 | 내용 | 장점 | 비용·위험 |
|---|---|---|---|
| P1. 전면 정확 핀 | 모든 직접 의존성을 정확 버전으로 선언, lockfile 필수 | 선언과 설치가 일치, 레지스트리 파일과 1:1 대조 가능 | 갱신 PR 수 증가; 봇 없이는 유지 어려움(현재 봇 없음) |
| P2. caret + lockfile(현행 다수) | 선언은 범위, lockfile이 진실 | 변경 최소 | "일치"의 정의가 lockfile 비교가 되어 매니페스트만 봐서는 판단 불가(§1 표의 선언/설치 괴리) |
| P3. 계층별 하이브리드 | 플랫폼·프레임워크·툴체인(node, npm, python, next, react, typescript, tailwindcss, @tailwindcss/postcss, eslint+config, vitest, @playwright/test, ruff, mypy, pytest, fastapi, sqlalchemy, alembic, dagster)은 **정확 핀 + 레지스트리 대조**; 나머지 라이브러리는 caret + lockfile; Python은 uv.lock을 CI·Docker 모두 `--locked`로 | map·pinvi·weather 선례와 정합; 봇 없이도 대조 가능한 범위가 작음 | 각 저장소에 검증 스크립트(map `verify-*.mjs`류) 이식 필요 |
| P4. 공유 renovate preset | common 저장소에 `renovate/*.json` preset을 두고 각 저장소 `renovate.json`이 `extends: ["github>digitie/kor-travel-common//renovate/default"]` | 그룹·일정·자동 머지 규칙 중앙화 | Renovate 앱 설치·권한 필요(미확인); 7개 저장소 모두 현재 미사용 |
| P5. dependabot per-repo | 각 저장소 `.github/dependabot.yml` | 설정 단순 | 저장소 간 프리셋 공유 불가(추정); 정렬 목표를 표현할 수단이 없음 |

P3와 P4의 조합이 선행 사례(map의 상수 검증, pinvi의 lock 무결성 검사, dm의 SHA 핀·정확 핀, weather의 `--locked`)를 모두 흡수한다는 점에서 유력 후보다(후보, 결정 아님).

### 7.3 버전 레지스트리 파일 형식 후보 — docker-manager 선행 사례 검토

dm `docs/runtime-pin-registry.md`와 `config/runtime-pins.seed.json`은 **라이브러리 버전이 아니라 Map·PinVi 소스 revision**을 고정하는 레지스트리다(사실). 그럼에도 형식과 운영 원칙은 직접 참고할 만하다:

| dm 레지스트리 특성(사실) | 라이브러리 버전 레지스트리에의 적용 후보 |
|---|---|
| 스키마 식별자 `"schema": "kor-travel-docker-manager.runtime-pin-registry.v1"`, `release_version: 5`, 미지 필드 거부, 항목 순서 고정 | `"schema": "kor-travel-common.version-registry.v1"` + strict 파서 |
| `sources[] {role, url, revision}` + `pinset_sha256`(로드마다 재계산 대조) | `toolchain {node, npm, python}`, `packages {npm: {...}, pypi: {...}}`, `images {...}`, `actions {...}` + 정본 digest |
| `history[]`(500건 상한, `supersedes` 기록), `blocked_pinsets[]`(삭제 API 없음, fail-close) | 갱신 이력과 "회귀가 확인된 버전 차단 목록"(예: `mcp 2.x`가 concierge를 깨뜨린 2026-09-04 사고 — `backend/requirements.txt` 주석) |
| "값은 파일이 소유, 계약(canonical URL·하한선)은 코드가 소유" | 값은 registry JSON, 검증 규칙(허용 range·필수 lock 사용)은 common의 검증 스크립트 |
| CLI `ktdctl pin init/show/verify/rotate/rollback/block/apply-pending`, mutation은 `--confirm` 필수, root `0600`·공개 사본 `0644` 분리 | 라이브러리 버전은 비밀·권한 문제가 없으므로 권한 계층은 불필요(추정); `verify`(각 저장소 lock 대조)·`rotate`(기준선 상향 PR 생성)만 있으면 됨 |
| 교차 저장소 바이트 계약(map `scripts/lib/c7_prod_attestation.py`와 digest 규칙 공유) | 각 저장소 검증 스크립트가 같은 registry 파일을 읽고 같은 비교 규칙을 쓰도록 스크립트 자체를 common이 배포 |

형식 후보(예시, 결정 아님):

```json
{
  "schema": "kor-travel-common.version-registry.v1",
  "baseline": "2026-09",
  "toolchain": {
    "node": { "engines": "^22.22.2 || ^24.15.0", "image": "node:22.23.1-bookworm-slim@sha256:…" },
    "npm": "11.19.1",
    "python": { "requires": ">=3.12", "image": "python:3.12-slim@sha256:…", "uv": "0.12.10" }
  },
  "npm": { "next": "16.3.4", "react": "19.2.8", "typescript": "5.9.3", "tailwindcss": "4.3.3", "eslint": "10.10.0", "vitest": "4.1.11", "@playwright/test": "1.63.0" },
  "pypi": { "fastapi": "0.141.1", "sqlalchemy": "2.0.52", "alembic": "1.19.2", "pytest": "9.1.1", "ruff": "0.16.6", "mypy": "2.3.1" },
  "images": { "postgis": "postgis/postgis@sha256:8b33190b…" },
  "actions": { "actions/checkout": "v4.2.2@11bd7190…" },
  "blocked": [ { "pypi": "mcp", "range": ">=2", "reason": "FastMCP→MCPServer API 변경, concierge 2026-09-04", "since": "2026-09-04" } ]
}
```

이 예시는 dm의 `sources/history/blocked_pinsets` 구조를 라이브러리 축으로 옮긴 것이며, 실제 키·값은 정책 결정 후 확정해야 한다.

### 7.4 자동 갱신(renovate/dependabot) 현황

사실: 7개 저장소 어디에도 `renovate.json`·`.renovaterc*`·`.github/dependabot.yml`이 없다. 갱신은 사람이 lock을 재생성하고 문서를 갱신하는 방식이다(airport `docs/architecture/dependencies.md`: "2026-08-22 레지스트리와 공식 릴리스 페이지를 확인한 뒤 lock을 갱신했다"). pinvi는 lock 재생성 사고(T-352)를 겪은 뒤 무결성 검사를 추가했고, map은 npm 실행기 버전까지 고정한다. 봇 없이 정렬 정책을 유지하려면 검증 스크립트가 CI에서 registry와 lock을 대조해 **격차를 실패가 아닌 보고로** 내는 단계가 먼저 필요하다(후보).

## 열린 질문

1. TypeScript 기준선: airport의 7.0.2를 유지할 이유(빌드 속도·정책)가 문서화돼 있지 않다. typescript-eslint의 TS 7 지원 시점을 확인하기 전까지 5.9.x로 통일할지, 6.0.x를 거칠지 결정이 필요하다.
2. Node 기준선: 22.x(모든 이미지 일치)로 우선 통일한 뒤 24/26으로 갈지, 지금 24 Active LTS로 갈지. map `engines`는 이미 둘 다 허용한다. Node 20 CI(dm, geo, weather)는 EOL이므로 어느 쪽이든 선행 정리 대상이다.
3. npm 기준선: map 12.0.1 vs pinvi 11.19.1. Node 24/26 동봉 npm이 11.19.0이므로 12를 기준으로 삼으면 모든 CI·Docker에서 별도 설치가 필요하다.
4. Python 이미지: 3.12(다수) vs 3.13(weather). geo의 GDAL 시스템 라이브러리 핀과 dagster의 3.13 지원 여부(map CI 매트릭스는 3.13을 통과 — 사실)를 근거로 3.13 이미지 전환 가능성을 검토할지.
5. maplibre-gl 6.x: concierge만 6.0.0이고 기존 공유 라이브러리 peer는 `^5.24.0`이다. 공유 라이브러리를 6으로 올릴지, concierge를 5.24로 되돌릴지.
6. map api의 `starlette<1.0`·`alembic<1.20` 상한: 다른 앱의 Starlette 1.6.0과의 정렬을 위해 상한을 풀 수 있는지(TestClient·httpx2 문제 재검증 필요).
7. provider 라이브러리 SHA(python-kma-api가 map·weather에서 다름, pinvi etl `@main`)를 버전 레지스트리 범위에 넣을지.
8. pinvi mobile: NativeWind 5 GA 전까지 Tailwind 3을 예외로 둘지, mobile을 정렬 정책 범위에서 제외할지. Expo SDK 정합용 정확 핀(react 19.2.6, RN 0.86.3)이 web의 React 버전까지 묶는 구조를 common이 존중해야 하는지.
9. DB major(PostgreSQL 16 → 17/18, PostGIS 3.5 → 3.6)를 라이브러리 정렬 정책과 분리해 별도 트랙으로 둘지.
10. geo·map·dm·concierge에 Python lockfile을 도입할 때 도구(uv)를 통일할지(dm은 Poetry 매니페스트).
11. 선언 하한만 있는 Python 의존성(concierge `requirements.txt`, pinvi `>=` only)에 상한을 둘지 — concierge의 `mcp<2` 사고는 상한 부재가 원인이었다(`backend/requirements.txt` 주석).
12. Renovate 앱 설치 가능 여부와 권한(조직/개인 계정) — 미확인.
13. lucide-react 1.x·@tanstack/react-table 9.x·mypy 2.x의 실제 breaking 내용 — 본 조사에서 미조회.

## 근거 파일 목록

저장소 상대 경로. 라인은 인용한 곳만 표기.

airport (`2bb1111`):
1. `frontend/package.json`
2. `frontend/package-lock.json` (`packages["node_modules/typescript"]`, `["node_modules/next"]`)
3. `frontend/tsconfig.json`
4. `frontend/next.config.ts`
5. `frontend/Dockerfile`
6. `backend/pyproject.toml`
7. `backend/uv.lock`
8. `backend/Dockerfile`
9. `.github/workflows/ci.yml`
10. `docker-compose.db.yml`, `docker-compose.live.yml`
11. `docs/architecture/dependencies.md`
12. `docs/dev-environment.md:36-37`

concierge (`7945305`):
13. `frontend/package.json`
14. `frontend/package-lock.json`
15. `tests/package.json`, `tests/package-lock.json`
16. `backend/requirements.txt`, `etl/requirements.txt`, `mcp/requirements.txt`, `scheduler/requirements.txt`
17. `Dockerfile.python`, `frontend/Dockerfile`, `docker-compose.yml:14,55`
18. `AGENTS.md:96-97`, `docs/dev-environment.md:16,22`

docker-manager (`862562d`):
19. `frontend/package.json`, `frontend/package-lock.json`
20. `backend/pyproject.toml`
21. `.github/workflows/ci.yml:18-47`
22. `docker-compose.yml` (image 행 9, 93, 158, 228, 262, 300, 334, 363, 739, 790, 1314-1348, 1377)
23. `docs/runtime-pin-registry.md` (§0~§7)
24. `config/runtime-pins.seed.json`
25. `docs/decisions.md:517-546` (ADR-17), `:1879-1900` (ADR-36)
26. `docs/architecture.md:143-150`, `docs/dev-environment.md:11-12`

geo (`1d9d74d`):
27. `kor-travel-geo-ui/package.json`, `kor-travel-geo-ui/package-lock.json`
28. `kor-travel-geo-ui/Dockerfile`
29. `pyproject.toml`, `kor-travel-geo-dagster/pyproject.toml`
30. `docker/api.Dockerfile:29-37`, `kor-travel-geo-dagster/docker/dagster.Dockerfile:18,47-49,66`
31. `.pre-commit-config.yaml`
32. `.github/workflows/ci.yml:10-54`, `.github/workflows/openapi.yml:10-19`
33. `docs/adr/019-nextjs-16-security-floor.md`
34. `docs/journal.md:872,997,1725`, `docs/postmerge-review-fixups-pr384-pr392.md:12`
35. `docs/kor-travel-common-library-review.md` (선행 보고서, §2·§3.3·§12)

map (`c494e227`):
36. `package.json` (engines, packageManager, overrides, allowScripts, scripts)
37. `package-lock.json`
38. `packages/kor-travel-map-admin/frontend/package.json`
39. `packages/map-marker-react/package.json`
40. `packages/kor-travel-map-user-client/package.json`
41. `pyproject.toml`, `packages/kor-travel-map-api/pyproject.toml`, `packages/kor-travel-map-dagster/pyproject.toml`
42. `scripts/verify-npm-tree.mjs`, `scripts/verify-next-sharp.mjs`, `scripts/patch-redocly-openapi-core.mjs`
43. `.pre-commit-config.yaml`
44. `.github/workflows/ci.yml:24-75,114-194`, `frontend.yml:25-98`, `lint.yml`, `openapi.yml`, `postgis-only.yml`, `docker-images.yml:37-43`
45. `docker/api.Dockerfile:1-34`, `docker/dagster.Dockerfile:1-44`, `docker/frontend.Dockerfile:1,26,70`, `docker/c7-playwright.Dockerfile:1`
46. `docker-compose.yml:1-12,37,239,287,344-369`
47. `docs/archive/journal-2026-08a.md:312-322`, `scripts/create-application-0236-source-oracle.sh:173-210`
48. `README.md:105-106`, `docs/dev-environment.md:355-358,630-631`

weather (`6003da9`):
49. `packages/kor-travel-weather-admin/frontend/package.json`, `package-lock.json`
50. `packages/kor-travel-weather-admin/frontend/design.md:1-25`, `app/tokens.css`, `app/globals.css` (존재 확인)
51. `pyproject.toml`, `packages/kor-travel-weather-api/pyproject.toml`, `packages/kor-travel-weather-dagster/pyproject.toml`, `packages/python-airkorea-api/pyproject.toml`
52. `uv.lock`
53. `deploy/Dockerfile.python:1-36`, `deploy/Dockerfile.web:1,16`, `deploy/Dockerfile.dagster-gateway:1`
54. `compose.yaml:3,163`
55. `.github/workflows/ci.yml:13-80`

pinvi (`9af25e5`):
56. `package.json` (workspaces, overrides, engines)
57. `package-lock.json`
58. `apps/web/package.json`, `apps/mobile/package.json`
59. `packages/{api-client,design-tokens,domain,hooks,i18n,schemas,state}/package.json`
60. `apps/api/pyproject.toml`, `apps/api/uv.lock`, `apps/etl/pyproject.toml`
61. `apps/api/Dockerfile:1-6,42,62`, `apps/etl/Dockerfile:3`, `apps/web/Dockerfile:1-10,29,55`, `infra/nginx/Dockerfile:6`
62. `infra/docker-compose.yml:11-135`, `infra/docker-compose.app.yml:6-450`
63. `.github/workflows/api.yml:76-114`, `web.yml:56-100`, `mobile.yml:29-100`, `etl.yml:57-74`, `aggregate-ci.yml:32`
64. `scripts/check-lockfile-integrity.mjs`
65. `docs/decisions.md:273-300` (ADR-011), `docs/dev-environment.md:162-176`, `apps/mobile/README.md:14-18,52-55`

기존 공유 라이브러리:
66. `F:/dev/maplibre-vworld-js/package.json` (peerDependencies)
67. `F:/dev/maplibre-vworld-react/package.json` (devDependencies, overrides, packageManager)

외부 조회(§4.1 명령으로 재현 가능): npm registry, PyPI JSON, endoflife.date API, GitHub releases API, Docker Hub tags API, nodejs.org dist index, GitHub Actions run 로그(`gh run view 33997890538 --repo digitie/kor-travel-airport`), Context7 문서(`/vercel/next.js` typescript.mdx·version-16.mdx, `/microsoft/typescript-go` README·CHANGES.md·program.go, `/react/react` CHANGELOG, `/websites/nativewind_dev_v5` migrate-from-v4).
