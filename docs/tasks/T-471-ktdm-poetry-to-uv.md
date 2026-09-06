# T-471 ktdm: Poetry→`uv.lock`·하한 상향·CI 핀 정리 + quality baseline

- 상태: BLOCKED
- 우선순위: P1
- Gate: ci.yml
- 선행: T-305

## 목표

docker-manager 백엔드의 "선언(poetry pyproject) / CI pip 정확 핀 3종 / 운영 offline wheelhouse" 3중 버전 결정을 `uv.lock` 단일 정본으로 바꾼다. `[build-system]`을 poetry-core에서 hatchling(또는 uv 호환 유지)으로, 하한(`fastapi ^0.110`·`uvicorn ^0.28`·`ruff ^0.3`·`mypy ^1.9`·`pytest ^8`)을 common floor로 올리고, CI는 `uv sync --locked`, wheelhouse 프로비저닝은 `uv export`로 생성한다. C20 quality 산출물은 per-file-ignores baseline과 함께 도입(`ruff format` 전체 실행 금지 유지).

## 고정 결정

- [design-brief](../plan/design-brief.md) D-06(uv 0.11 floor, `uv.lock` 의무, Poetry는 uv 전환 task; FastAPI 0.115/uvicorn 0.30/ruff 0.9/mypy 1.13/pytest 8 floor)·D-07(`poetry.lock` 파서는 T-005b이나 전환이 정본)·D-15(C20: format 미포함, per-file-ignores baseline)·D-16(ktdm은 L8 전 규칙 참조까지 — common 코드 무관).
- ADR-008·ADR-011 — [ADR 색인](../adr/README.md). 정본: [backend-stack](../standards/backend-stack.md), [versions](../standards/versions.md).
- 사실: `poetry-core` 빌드, `poetry.lock` 미추적, CI `pip install -e ./backend httpx==0.28.1 pytest==9.1.1 ruff==0.16.4`, 운영 root-owned wheelhouse(`scripts/provision-ktdm-offline-wheelhouse.py`), `pytest ^8` vs CI 9.1.1·`ruff ^0.3` vs 0.16.4 drift, `ruff format` 미적용본, DO NOT 15 "lockfile 없으면 하드 실패" 문구와 현 상태 모순 — [inv/ktdm §4.1·§9](../survey/inventory/kor-travel-docker-manager.md), [vm §2.1·§3.2](../survey/cross/version-matrix.md), [be §2.1·§2.17](../survey/cross/backend.md).
- PR 순서: [judge-migration-feasibility §3.1 ktdm #2](../plan/design-panel/judge-migration-feasibility.md).

## 구현 범위

- `backend/pyproject.toml`: `[build-system]` hatchling, `[project]` 의존 하한 상향(fastapi ≥0.115, uvicorn ≥0.30, httpx ≥0.27), `[project.optional-dependencies] dev`(pytest ≥8, ruff ≥0.9, mypy ≥1.13), console script `ktdctl` 유지; `[tool.ruff]` common 베이스 `extend` + per-file-ignores baseline + `--ignore EXE001` 유지; `[tool.mypy]` strict 베이스 + `ignore_errors` baseline(현재 mypy 미도입 → `mypy-targets` 최소 모듈부터).
- `uv lock` → `backend/uv.lock`; `.github/workflows/ci.yml` python job `setup-uv` + `uv sync --locked --extra dev` + `ruff check --ignore EXE001` + `pytest`(정확 핀 3종 삭제).
- `scripts/provision-ktdm-offline-wheelhouse.py`가 `uv export --frozen --format requirements-txt`를 입력으로 쓰도록 수정(운영 배포 절차 문서 갱신).
- ktdm `AGENTS.md` DO NOT 15 문구와 `docs/bindings.md` 등록(lockfile = `backend/uv.lock`)을 코드 사실과 일치시킴(`test_normative_docs_cite_real_symbols` 통과).
- 매니페스트 `lockfiles[]` `{kind: uv, path: backend/uv.lock, scope: python}`.

## 범위 밖

프론트 업그레이드(T-470), common Python 모듈 import(T-486, L8 후), `ruff format` 전면 적용, 운영 서버 wheelhouse 실제 재프로비저닝(ktdm 배포 runbook 소유; 이 task는 스크립트·문서까지).

## 대상 저장소·브랜치·PR·되돌리기

- `digitie/kor-travel-docker-manager`, Linux/WSL, 브랜치 `agent/T-471-uv-lock`, `main`에서 분기. PR 1개(≤10 파일 + `uv.lock`).
- 되돌리기 = `git revert <merge-sha>`(poetry 선언·CI 핀 복원). wheelhouse는 revert 후 다음 프로비저닝에서 이전 방식으로 생성.

## 예상 변경 파일

아래는 이 task가 만들거나 고칠 예정 경로다. 예정 경로는 존재·실행 증거가 아니다.

```text
backend/pyproject.toml, backend/uv.lock
.github/workflows/ci.yml
scripts/provision-ktdm-offline-wheelhouse.py
docs/prod-deployment.md, docs/bindings.md, AGENTS.md   # lockfile 결박 문구
kor-travel-common.lock.json
```

## 수용 기준

- [ ] `ci.yml` green: `uv sync --locked` 성공, `ruff check`(baseline 적용) 통과, pytest 통과(수 기록), mypy step 존재·통과(대상 모듈 명시).
- [ ] `uv.lock`의 fastapi·uvicorn·httpx·pytest·ruff·mypy 버전이 `versions.json` floor 이상(`check_versions` ktdm 행 `NO_LOCK` → `OK`/`NOT_RECOMMENDED`).
- [ ] `test_normative_docs_cite_real_symbols` 등 ktdm 규범 문서 테스트 통과(DO NOT 15 문구 정합).
- [ ] `git diff --stat backend/src`가 0(코드 재포맷 없음; baseline만).
- [ ] wheelhouse 스크립트가 `uv export` 출력으로 dry-run 성공(로컬 기록).

## 검증 명령

```bash
# kor-travel-docker-manager (Linux/WSL)
cd backend && uv lock && uv sync --locked --extra dev
uv run ruff check --ignore EXE001 . && uv run mypy <targets> && uv run pytest -q
uv export --frozen --format requirements-txt > /tmp/ktdm-req.txt && python3 ../scripts/provision-ktdm-offline-wheelhouse.py --dry-run --requirements /tmp/ktdm-req.txt
# kor-travel-common
python3 -B -X utf8 tools/check_versions.py --manifest ../kor-travel-docker-manager/kor-travel-common.lock.json
```

## evidence

PR URL·CI run·`uv.lock` digest·baseline 위반 표·dry-run 출력을 이 파일 "실행 기록"·`docs/journal.md`에, `consumers.pins.json` 갱신.

## rollback·release 차단 조건

- `uv sync --locked` 실패·규범 문서 테스트 실패면 머지 금지; 머지 후 운영 프로비저닝 실패 시 revert + 이전 wheelhouse 유지.
- `uv.lock` 없이 T-486을 열지 않는다.
