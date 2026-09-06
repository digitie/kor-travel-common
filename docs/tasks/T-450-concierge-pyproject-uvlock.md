# T-450 concierge: `pyproject.toml`·`uv.lock`(`mcp<2` blocked)·ruff/mypy baseline 도입

- 상태: BLOCKED
- 우선순위: P0
- Gate: 로컬 4 gate
- 선행: T-305

## 목표

concierge 백엔드(`backend/ktc` + `etl/`·`mcp/`·`scheduler/` 래퍼)의 하한 전용 `requirements.txt` 4벌을 `pyproject.toml` + `uv.lock`으로 바꾸고, common C20 quality 산출물(ruff `extend` 베이스·mypy strict 베이스·pre-commit 템플릿)을 per-file-ignores baseline과 함께 도입한다. `mcp<2`는 `versions.json` `blocked[]`와 pyproject 상한 양쪽에 남긴다(2026-09-04 crash-loop 사고). CI가 없으므로 로컬 4 gate(ruff·mypy·pytest·`uv sync --locked`)가 판정 기준이다.

## 고정 결정

- [design-brief](../plan/design-brief.md) D-06(uv 0.11 floor·`uv.lock` 의무·requirements.txt는 uv 전환 task; Python 이미지 3.12-slim 권장, 3.11-slim floor)·D-07(`blocked[]` 예: `mcp>=2`)·D-15(C20 quality: `line-length=100`·`E,F,I,UP,B,ASYNC`, format 규칙 미포함, per-file-ignores baseline)·D-16(ktc는 L8 전 규칙 문서 참조까지 — 이 task는 규칙 산출물 적용이며 common 코드 링크 없음).
- ADR-008·ADR-011 — [ADR 색인](../adr/README.md). 정본: [backend-stack](../standards/backend-stack.md), [versions](../standards/versions.md).
- 사실: `pyproject.toml`/lockfile 없음, `backend/requirements.txt` 하한 핀 + `mcp<2` + `python-vworld-api` 커밋 아카이브 URL 핀, 래퍼 3개가 `-r ../backend/requirements.txt`, 테스트 의존이 런타임 requirements에 포함, ruff/mypy 설정 없음(미사용 import 12건 기록), `Dockerfile.python` `python:3.11-slim` — [inv/ktc §4.1·§9](../survey/inventory/kor-travel-concierge.md), [vm §2.1](../survey/cross/version-matrix.md), [be §2.1·§2.17](../survey/cross/backend.md).
- PR 순서: [judge-migration-feasibility §3.1 concierge #1](../plan/design-panel/judge-migration-feasibility.md).

## 구현 범위

- 루트(또는 `backend/`) `pyproject.toml`: 패키지 `ktc`, `requires-python >=3.11`(이미지 3.11 유지, 3.12 상향은 O-7 앱 결정), 의존은 requirements 하한을 옮기되 `mcp>=1.2,<2` 상한 유지, `python-vworld-api @ git+https://github.com/digitie/python-vworld-api@<sha>`(아카이브 URL → git sha 핀), extras `[etl]`·`[mcp]`·`[scheduler]`·`[dev]`(pytest·pytest-asyncio를 dev로 이동).
- `uv lock` → `uv.lock` 커밋; `Dockerfile.python`을 `uv sync --locked --extra etl --extra mcp --extra scheduler`로; `requirements*.txt`는 삭제하거나 `uv export`로 생성물임을 헤더에 명시.
- `[tool.ruff]` = common 베이스 `extend` + `[tool.ruff.lint.per-file-ignores]` baseline(현재 위반을 파일 단위로 등록, 신규 코드 MUST), `[tool.mypy]` strict 베이스 + `ignore_errors` 모듈 baseline, `.pre-commit-config.yaml` 템플릿.
- 매니페스트 `lockfiles[]` `{kind: uv, path: uv.lock, scope: python}`; `versions.json` `blocked[]`에 `mcp>=2` 등록(common PR, T-005 범위에 이미 있으면 확인).

## 범위 밖

CI 신설(T-451), common Python 모듈 import(T-485, L8 후), ruff `format` 전면 적용(D-15 format 미포함), 프론트, `python-vworld-api` 버전 상향.

## 대상 저장소·브랜치·PR·되돌리기

- `digitie/kor-travel-concierge`, 작업은 Linux/WSL2 bash(ADR-23/33), 브랜치 `agent/<agent>-T-450-uv-lock`, `origin/main`에서 분기. PR 1개(≤10 파일 + `uv.lock`).
- 되돌리기 = `git revert <merge-sha>`(requirements 복원 포함). Docker 이미지는 revert 후 재빌드.

## 예상 변경 파일

아래는 이 task가 만들거나 고칠 예정 경로다. 예정 경로는 존재·실행 증거가 아니다.

```text
pyproject.toml, uv.lock
backend/requirements.txt, etl/requirements.txt, mcp/requirements.txt, scheduler/requirements.txt   # 삭제 또는 생성물 표기
Dockerfile.python
.pre-commit-config.yaml
kor-travel-common.lock.json
kor-travel-common: versions.json   # blocked[] mcp>=2
```

## 수용 기준

- [ ] `uv sync --locked`가 clean 환경에서 성공하고 `uv.lock`의 `mcp` 버전이 1.x다(`uv pip list | grep mcp`).
- [ ] `uv run ruff check .`·`uv run mypy <targets>`·`uv run pytest -q`가 통과(pytest 수 기록, 0 test 금지); baseline에 등록된 위반 수를 PR 본문에 표로.
- [ ] `docker build -f Dockerfile.python .`이 성공하고 컨테이너에서 `python -c "import ktc, mcp"` 가 실행된다.
- [ ] `check_versions` report concierge 행이 `NO_LOCK`에서 `OK`/`NOT_RECOMMENDED`/`BLOCKED`(mcp 상한 준수 시 BLOCKED 아님)로 바뀐다.
- [ ] `python-vworld-api` 참조가 git sha 핀이다(`FLOATING_REF` 0).

## 검증 명령

```bash
# kor-travel-concierge (Linux/WSL2)
uv lock && uv sync --locked --all-extras
uv run ruff check . && uv run mypy backend/ktc && uv run pytest -q
docker build -f Dockerfile.python -t ktc-local . && docker run --rm ktc-local python -c "import ktc, mcp; print(mcp.__version__)"
# kor-travel-common
python3 -B -X utf8 tools/check_versions.py --manifest ../kor-travel-concierge/kor-travel-common.lock.json
```

## evidence

PR 본문(4 gate 출력·baseline 위반 표·`uv.lock` digest), `docs/journal.md`, 이 파일 "실행 기록". CI가 없으므로 로컬 실행의 도구 버전·exit code를 반드시 적는다.

## rollback·release 차단 조건

- `mcp` 2.x가 lock에 들어오면 머지 금지(사고 재발). 로컬 gate 중 하나라도 red면 baseline 확장이 아니라 원인 기록 후 재시도.
- 이 PR 없이 T-451 CI를 열지 않는다(설치 재현 불가).
