# T-451 concierge: CI 신설(재사용 워크플로 호출·versions-check) + production `frontend/Dockerfile` 정리

- 상태: BLOCKED
- 우선순위: P0
- Gate: CI
- 선행: T-401, T-450

## 목표

`.github/`가 없는 concierge에 CI를 처음 만든다. common 재사용 워크플로 `python-quality.yml`·`node-quality.yml`·`versions-check.yml`을 태그/SHA로 호출하고, 개발 서버(`npm run dev`)를 실행하는 `frontend/Dockerfile`을 production 빌드(standalone) 이미지로 바꿔 `docker-build` 기동 확인이 가능하게 한다. 이후 concierge 트랙(T-453·T-454·T-485)은 이 CI를 gate로 쓴다.

## 고정 결정

- [design-brief](../plan/design-brief.md) D-18(소비자는 태그/SHA 참조만, 하드닝, Phase 4 재사용 워크플로는 concierge CI 신설용)·D-06(GitHub Actions SHA 핀)·D-07(report 모드)·D-03(CI `ubuntu-24.04`).
- ADR-008 — [ADR 색인](../adr/README.md). 정본: [ci-deploy](../standards/ci-deploy.md)(Dockerfile·compose 최소 규약 `ci` §3.3 채택), [versions](../standards/versions.md).
- 사실: `.github/` 없음, pre-commit 없음, `frontend/Dockerfile` `node:22-slim` + `CMD ["npm","run","dev"]`(prod 동일 이미지 여부 미확인, docker-manager 소관), Playwright 별도 `tests/` 패키지(webServer 자동 기동, 45 test), `next.config.mjs`에 `output` 설정 없음 — [inv/ktc §3.1·§6·§9·§11-2](../survey/inventory/kor-travel-concierge.md), [ci §1.6·§2.2 ktc](../survey/cross/ci-deploy.md).
- PR 순서: [judge-migration-feasibility §3.1 concierge #2](../plan/design-panel/judge-migration-feasibility.md).

## 구현 범위

- `.github/workflows/ci.yml`: `python-quality`(installer `uv`, `install-args "--locked --all-extras"`, `mypy-targets backend/ktc`, `pytest-args -q`, `db-image` = 테스트가 PostGIS를 요구하면 `postgis/postgis:16-3.5-alpine`), `node-quality`(`working-directory frontend`, `lint-max-warnings 0`, `test false`(vitest 없음), `build-env` 더미 `NEXT_PUBLIC_*`), `versions-check`(report). 모두 `uses: digitie/kor-travel-common/.github/workflows/<name>.yml@<sha>`.
- e2e(Playwright 45 test)는 PostgreSQL·seed가 필요하므로 1차는 `workflow_dispatch` job으로 두고 required에 넣지 않는다(운영 결합 회피).
- `frontend/Dockerfile`: multi-stage(deps → builder `next build` → runner standalone), `next.config.mjs` `output: "standalone"`, non-root, `EXPOSE 3000`, `HEALTHCHECK`; dev 이미지는 `Dockerfile.dev`로 분리. `docker-compose.yml` frontend 서비스는 prod 이미지를 가리키되 dev override로 기존 동작 유지.
- 하드닝: `permissions: contents: read`, `concurrency`, `timeout-minutes`, `ubuntu-24.04`, head SHA checkout.
- 매니페스트 갱신(T-403의 concierge 행 "매니페스트만"을 이 PR이 CI로 승격).

## 범위 밖

토큰·UI(T-453·T-454), Python 모듈 채택(T-485), branch protection 설정(저장소 소유자), docker-manager 배포 스크립트 변경(별도 요청).

## 대상 저장소·브랜치·PR·되돌리기

- `digitie/kor-travel-concierge`, Linux/WSL2, 브랜치 `agent/<agent>-T-451-ci`, `origin/main`에서 분기. PR 2개 가능(CI / Dockerfile)이나 Dockerfile 기동 확인이 CI에 있으므로 1 PR 허용(≤10 파일).
- 되돌리기 = `git revert <merge-sha>`(워크플로 삭제·Dockerfile 복원). 운영 이미지가 새 Dockerfile로 이미 배포됐으면 docker-manager 측 롤백 절차 동반.

## 예상 변경 파일

아래는 이 task가 만들거나 고칠 예정 경로다. 예정 경로는 존재·실행 증거가 아니다.

```text
.github/workflows/ci.yml
.github/workflows/e2e.yml              # workflow_dispatch
frontend/Dockerfile, frontend/Dockerfile.dev, frontend/.dockerignore
frontend/next.config.mjs               # output: standalone
docker-compose.yml (+ compose.dev.override)
kor-travel-common.lock.json
```

## 수용 기준

- [ ] PR CI가 `python-quality`·`node-quality`·`versions-check` 3 job green이고 required check 후보 이름이 PR 본문에 명시돼 있다.
- [ ] `docker build frontend/`가 성공하고 `docker run` 후 `curl -f http://127.0.0.1:3000/`이 200(또는 로그인 리다이렉트)을 반환한다(CI step 또는 로컬 기록).
- [ ] 워크플로의 모든 `uses:`가 SHA 핀(common 참조 포함, `@main` 0건).
- [ ] `versions-check` step summary에 concierge 행이 나타나고 `NO_LOCK` 0(T-450 반영).
- [ ] e2e dispatch job이 1회 수동 실행돼 45 test 결과가 기록됐다(실행 못 하면 `NOT_RUN(DB seed 필요)`).

## 검증 명령

```bash
# kor-travel-concierge (Linux/WSL2)
docker build -t ktc-frontend frontend && docker run -d --rm -p 3000:3000 --name ktc-fe ktc-frontend && sleep 5 && curl -sSf -o /dev/null -w '%{http_code}\n' http://127.0.0.1:3000/ ; docker stop ktc-fe
grep -nE 'uses: .*@(main|v[0-9]+)$' .github/workflows/*.yml   # 0건
gh pr checks <pr-number>
gh workflow run e2e.yml && gh run watch
```

## evidence

PR URL·CI run URL·기동 확인 출력·e2e 결과를 이 파일 "실행 기록"·`docs/journal.md`에, `consumers.pins.json` 갱신.

## rollback·release 차단 조건

- CI red 상태로 머지 금지(제로 베이스라 첫 green이 기준선). Dockerfile 기동 실패면 Dockerfile 부분만 분리 revert.
- T-450 미머지면 `python-quality`의 `uv sync --locked`가 실패하므로 이 PR을 열지 않는다.
