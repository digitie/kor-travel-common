# T-305 C20 quality 산출물(ruff extend·mypy·import-linter·pre-commit·CI 템플릿; format 미포함) + common 자기 적용

- 상태: BLOCKED
- 우선순위: P1
- Gate: 자기 적용
- 선행: T-302

## 목표

ruff를 설정한 5곳이 모두 `line-length = 100`이고 `E,F,I,UP,B,ASYNC`를 공통으로 포함하며 mypy strict가 4곳에 있다([be §2.17](../survey/cross/backend.md)). 이 task는 그 교집합을 규칙 산출물로 배포한다: ruff 베이스(`[tool.ruff] extend`로 참조), mypy strict 베이스, import-linter 계약 템플릿, pre-commit 템플릿, CI 스텝 조각. `ruff format` 규칙은 포함하지 않는다(ktdm 재포맷 금지, map만 CI에서 format check). 먼저 common 자신(`packages/py`·`tools/`·`tests/`)에 적용해 산출물이 실행 가능함을 증명한다.

## 고정 결정

- [design-brief](../plan/design-brief.md) D-15(C20 1차: ruff `extend` 베이스 `line-length=100`·`E,F,I,UP,B,ASYNC`, mypy strict 베이스, import-linter 계약 템플릿, pre-commit 템플릿, **format 규칙 미포함**, per-file-ignores baseline), D-06(ruff floor 0.9/recommended 0.16.x, mypy 1.13/2.3.x, import-linter 2.0/2.15), D-03(도구는 Windows Python stdlib에서 동작). ADR-011 — [ADR 색인](../adr/README.md). 규칙 정본: [backend-stack](../standards/backend-stack.md).
- 기존 위반은 앱별 `[tool.ruff.lint.per-file-ignores]` baseline으로 두고 신규 파일은 MUST(D-13과 같은 "신규 MUST·기존 baseline" 모델). airport·concierge는 0에서 도입이라 baseline이 클 수 있다([cm §2.4](../survey/commonality-matrix.md)).
- pre-commit은 map식 `language: system`(lock 버전과 pre-commit rev 불일치 방지, geo v0.7.4/v1.13.0 사례 [be §2.17](../survey/cross/backend.md)).
- 배포 형태: 저장소 `templates/python/*`가 정본이고 같은 내용을 wheel 패키지 데이터(`kortravelcommon/quality/`)로 동봉해 `python -m kortravelcommon.quality ruff-base --check <복사본>`으로 drift를 검사한다(후보; 리뷰에서 템플릿 단독으로 축소 가능).
- 재사용 워크플로 `python-quality.yml` 자체는 T-401 범위다. 이 task는 그 워크플로가 실행할 step 조각과 설정 파일만 만든다.

## 구현 범위

1. `templates/python/ruff.base.toml`: `line-length = 100`, `target-version = "py311"`, `[lint] select = ["E","F","I","UP","B","ASYNC"]`, `[lint.isort]` 최소 설정; `[format]` 절 없음. 소비자 `pyproject.toml`은 `[tool.ruff] extend = "ruff.base.toml"` + 앱 추가 규칙군.
2. `templates/python/mypy.base.toml`: `strict = true`, `warn_unused_ignores = true`, `plugins = ["pydantic.mypy"]`, `python_version` 주석(앱 floor). mypy는 `extend`가 없으므로 복사 조각으로 배포.
3. `templates/python/importlinter.base.toml`: layers 계약 예시(geo·map 형태)와 forbidden 계약(`fastapi|starlette|uvicorn` in core) 템플릿.
4. `templates/python/pre-commit.yaml`: ruff check·mypy·lint-imports를 `language: system` local hook으로.
5. `templates/python/ci-steps.md`: `ruff check` → `mypy` → `lint-imports` → `pytest` 순서와 per-file-ignores baseline 도입 절차(1 PR = baseline 추가만).
6. `kortravelcommon/quality/`(패키지 데이터 사본) + `python -m kortravelcommon.quality ruff-base [--check PATH | --print]`.
7. 자기 적용: `packages/py/kor-travel-common/pyproject.toml`에 `extend = "../../../templates/python/ruff.base.toml"`, 루트 `ruff.toml`이 `tools/`·`tests/`에 같은 베이스를 `extend`(기존 validator 위반은 per-file-ignores baseline). `python-package` job에 ruff·mypy·lint-imports step 추가; `tools/`·`tests/` ruff step은 T-009 `tools` job 소유자와 합의.
8. `docs/standards/backend-stack.md` 품질 절에 템플릿 링크와 baseline 규칙(standards-be 소유자와 합의).

## 범위 밖

`ruff format` 규칙·강제(앱 소유), `python-quality.yml` 재사용 워크플로(T-401), 각 앱 baseline 도입 PR(T-450·T-471·T-480~T-486), coverage 임계(앱 소유), pre-commit 설치 강제, TypeScript/ESLint 조각(T-107).

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다.

```text
templates/python/{ruff.base.toml,mypy.base.toml,importlinter.base.toml,pre-commit.yaml,ci-steps.md,README.md}
packages/py/kor-travel-common/src/kortravelcommon/quality/{__init__.py,__main__.py,ruff.base.toml}
packages/py/kor-travel-common/pyproject.toml          # [tool.ruff] extend·mypy·importlinter
packages/py/kor-travel-common/tests/test_quality_cli.py
ruff.toml                                             # 루트: tools/·tests/ 자기 적용
.github/workflows/python-package.yml                  # ruff·mypy·lint-imports step
docs/standards/backend-stack.md
```

## 수용 기준

- [ ] `templates/python/ruff.base.toml`에 `[format]` 절이 없고 `select`가 정확히 `E,F,I,UP,B,ASYNC`, `line-length = 100`이다.
- [ ] `packages/py`에서 `uv run ruff check src tests`·`uv run mypy --strict src`·`uv run lint-imports`가 0 오류로 통과하고, 루트 `python3 -m ruff check tools tests`(ruff 설치 venv)가 baseline 적용 후 0 오류다.
- [ ] `python -m kortravelcommon.quality ruff-base --check templates/python/ruff.base.toml`이 exit 0, 한 글자 바꾼 사본은 exit 1(부정 시험 기록).
- [ ] 템플릿 README에 소비자 도입 3단계(복사 → `extend` → baseline PR)와 "format 미포함" 문장이 있다.
- [ ] `python-package` job에 세 step이 있고 green; Windows Python에서 `ruff-base --check`가 동작한다(stdlib `tomllib`, `-X utf8`).
- [ ] `backend-stack.md`의 품질 절 값(select·line-length·도구 floor)이 `versions.json`·템플릿과 글자 단위로 일치한다.

## 검증 명령

```bash
cd packages/py/kor-travel-common
uv sync --locked --all-extras
uv run ruff check src tests && uv run mypy --strict src && uv run lint-imports
uv run python -m kortravelcommon.quality ruff-base --check ../../../templates/python/ruff.base.toml; echo "exit=$?"
cd ../../.. && uv run --project packages/py/kor-travel-common ruff check tools tests
python3 -B -X utf8 tools/validate_document_links.py
```

## evidence

이 파일 하단 "실행 기록"에 ruff/mypy/lint-imports exit code·위반 수(baseline 전/후)·`ruff-base --check` 부정 시험 결과·`python-package` run URL을 남긴다. Windows 실행 결과는 별도 줄로 남기고 못 돌린 항목은 `NOT_RUN(사유)`.

## rollback·release 차단 조건

- 템플릿·설정 추가이므로 `git revert` 1회로 원복된다. 자기 적용으로 `python-package`가 red가 되면 baseline을 넓히지 말고 위반을 고치거나 task를 되돌린다.
- 템플릿에 `[format]`이 들어가거나 select가 교집합 밖으로 확장되면 릴리스(T-310) 포함 금지 — 소비자 5곳 중 하나라도 즉시 red가 된다.
