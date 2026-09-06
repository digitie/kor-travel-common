# T-440 geo: Node 22 CI + `uv.lock` 도입 + pre-commit rev 정렬

- 상태: BLOCKED
- 우선순위: P1
- Gate: ci.yml
- 선행: T-005

## 목표

geo의 플랫폼 격차 3건을 코드 무변경 PR로 닫는다: CI Node 20 → 22, Python lockfile 부재 → `uv.lock` + CI·Docker `--locked` 소비, pre-commit ruff 0.7.4/mypy 1.13.0 rev를 lock과 같은 버전(또는 map식 `language: system`)으로. 이 PR이 geo 트랙(T-441·T-443·T-483)의 첫 revert 단위다.

## 고정 결정

- [design-brief](../plan/design-brief.md) D-06(Node 22 floor, uv 0.11 floor·`uv.lock` + `--locked` 의무, ruff 0.9/mypy 1.13 floor·recommended 0.16.x/2.3.x)·D-07(lockfile 의무, `NO_LOCK` 판정)·D-24(프레임워크 PR 분리).
- ADR-008·ADR-011 — [ADR 색인](../adr/README.md). 정본: [versions](../standards/versions.md), [backend-stack](../standards/backend-stack.md), [ci-deploy](../standards/ci-deploy.md).
- 사실: CI `node-version: "20"`, Docker `node:22-alpine`; Python `>=3.12` setuptools namespace, lockfile 없음, CI `pip install -e ".[api,loaders,dev]"` 매 실행 최신 해석, GDAL apt pre-install; pre-commit ruff v0.7.4·mypy v1.13.0·local import-linter; lock 2026-07-28 이후 미갱신 — [inv/geo §3.1·§4.1·§6·§9](../survey/inventory/kor-travel-geo.md), [vm §1.1·§2.1·§3.5](../survey/cross/version-matrix.md), [ci §2.2 geo](../survey/cross/ci-deploy.md).
- PR 순서: [judge-migration-feasibility §3.1 geo #1](../plan/design-panel/judge-migration-feasibility.md).

## 구현 범위

- `.github/workflows/ci.yml`: frontend job `node-version: 22`; python job을 `astral-sh/setup-uv` + `uv sync --locked --extra api --extra loaders --extra dev`로(GDAL pre-install 유지, `pip install "gdal==$(gdal-config --version)"`는 uv 환경에서 동일 실행).
- 루트 `uv.lock` 생성·커밋(`uv lock`), `kor-travel-geo-dagster/`는 별도 distribution이므로 자체 `uv.lock` 또는 workspace 멤버 등록 중 하나를 택해 기록.
- `docker/api.Dockerfile`: `uv sync --locked` 소비로 전환(이미지 `python:3.12-slim` 유지).
- `.pre-commit-config.yaml`: ruff/mypy rev를 `uv.lock`의 설치 버전과 일치시키거나 `repo: local` + `language: system`으로 전환(map 선례).
- 매니페스트 `lockfiles[]`에 `{kind: uv, path: uv.lock, scope: python}` 추가.

## 범위 밖

React 19(T-443), `@config` 정리·토큰(T-441), ruff/mypy 버전 상향으로 생기는 규칙 위반 수정(baseline은 T-483 quality 단계), Node 24 승격(T-507).

## 대상 저장소·브랜치·PR·되돌리기

- `digitie/kor-travel-geo`, 작업은 geo 정본 Linux/WSL(`F:/dev/kor-travel-geo-fixes`는 조사 체크아웃), 브랜치 `agent/<agent>-T-440-node22-uvlock`, `origin/main`에서 분기. PR 1개.
- 되돌리기 = `git revert <merge-sha>`(uv.lock 삭제·CI 복원 포함).

## 예상 변경 파일

아래는 이 task가 만들거나 고칠 예정 경로다. 예정 경로는 존재·실행 증거가 아니다.

```text
.github/workflows/ci.yml
uv.lock (+ kor-travel-geo-dagster/uv.lock 또는 workspace 설정)
pyproject.toml                       # [tool.uv] 최소 설정
docker/api.Dockerfile
.pre-commit-config.yaml
kor-travel-common.lock.json          # lockfiles[]
```

## 수용 기준

- [ ] `ci.yml` green(unit 1,395 passed 수준 유지 — 실제 수치를 PR에 기록, 0 test 금지), frontend job이 Node 22에서 lint·type-check·test·build 통과.
- [ ] `uv sync --locked`가 CI·Docker에서 성공하고 `uv.lock`에 ruff·mypy·pytest 버전이 기록돼 `check_versions`가 `NO_LOCK` 대신 `OK`/`NOT_RECOMMENDED`를 낸다.
- [ ] `pre-commit run --all-files`가 lock 버전과 같은 ruff/mypy로 실행됐음이 로그로 확인(버전 문자열 첨부).
- [ ] 통합 테스트(`KTG_TEST_PG_DSN` opt-in)는 실행 여부를 명시(`NOT_RUN(DSN 없음)` 허용).

## 검증 명령

```bash
# kor-travel-geo (Linux/WSL)
uv lock && uv sync --locked --extra api --extra loaders --extra dev
uv run pytest tests/unit -q
uv run pre-commit run --all-files
cd kor-travel-geo-ui && npm ci && npm run lint && npm run type-check && npm test && npm run build
# kor-travel-common
python3 -B -X utf8 tools/check_versions.py --manifest ../kor-travel-geo/kor-travel-common.lock.json
```

## evidence

PR URL·CI run·`uv.lock` digest·pytest 수를 이 파일 "실행 기록"·`docs/journal.md`에, `consumers.pins.json` 갱신.

## rollback·release 차단 조건

- Node 22에서 red가 나면 원인 기록 후 revert; `versions.json`에 geo Node 예외를 `until`과 함께 등록하고 재시도.
- `uv.lock` 없이 T-441 이후 PR을 열지 않는다(lock 의무).
