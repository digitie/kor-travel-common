# T-302 packages/py/kor-travel-common 골격(hatchling·extras·3.11 문법 검사·uv.lock·starlette 0.4x/1.6 CI 매트릭스) + `docs/standards/backend-stack.md` 확정

- 상태: READY
- 우선순위: P0
- Gate: python-package
- 선행: T-003

## 목표

Python 공통 패키지의 배포 골격을 만든다: 배포 이름 `kor-travel-common`, import `kortravelcommon`, hatchling 빌드, extras 5종, `requires-python >=3.11`, `uv.lock`, common CI `python-package` job(`uv build` → wheel 설치 → starlette 0.4x/1.6 매트릭스). 모듈 본문은 T-303~T-308이 채우므로 이 task의 코드는 `__init__`·버전·`py.typed`·import-linter 계약까지다. 함께 규칙 정본 `docs/standards/backend-stack.md`를 확정한다(이번 PR은 문서 초안, 실물 대조 후 확정 — 브리프 §7). T-003 선행 사유: 모든 `.py`에 SPDX 헤더와 wheel 동봉 고지 파일이 필요하다(D-17).

## 고정 결정

- [design-brief](../plan/design-brief.md) D-15(패키지 이름·extras·3.11 문법·core는 stdlib+pydantic·`[api]` starlette 미핀 + CI 매트릭스·인증 범위 밖), D-06(Python 3.11 호환, FastAPI floor 0.115·pydantic 2.9·uv 0.11), D-07(lockfile 의무), D-11(`git+https@py-vX.Y.Z#subdirectory=packages/py/kor-travel-common` + wheel 자산, `license-files`), D-17(SPDX 헤더·`check_spdx.py`), D-18(`python-package` job), D-32(docstring 한국어), D-33(`uv` + `packages/py/.../uv.lock`). ADR-011·ADR-005·ADR-004 — [ADR 색인](../adr/README.md).
- Python floor 3.12 시점은 **열림(O-7, 사용자 확인 필요)**; 기본값 = common 3.11 호환 유지(map·wx·ktdm floor 3.11, [be §2.1](../survey/cross/backend.md), [vm §2.1](../survey/cross/version-matrix.md)).
- geo·map import-linter 계약 때문에 core 모듈은 fastapi/starlette/sqlalchemy를 import하지 않는다([be §3](../survey/cross/backend.md) 전제). extras: `api`(fastapi·prometheus-client), `db`(sqlalchemy·alembic), `dagster`, `testing`(pytest·pytest-asyncio·testcontainers), `http`(httpx·tenacity) — [cm §2.4](../survey/commonality-matrix.md).
- starlette 상한 충돌(map `<1.0` vs kta·ktw·pinvi 1.6.0, [oa §2.12](../survey/cross/openapi.md))은 범위 미선언 + CI 매트릭스로 흡수하고 재검증은 T-480.
- 규칙 정본 위치: 스택·버전은 [backend-stack](../standards/backend-stack.md)(standards-be 소유), 값은 [versions.json](../../versions.json)(versions-conventions 소유). 같은 규범을 두 문서에 복제하지 않는다.

## 구현 범위

1. `packages/py/kor-travel-common/pyproject.toml`: `[build-system] hatchling`, `name = "kor-travel-common"`, `version`은 `src/kortravelcommon/_version.py` 동적, `requires-python = ">=3.11"`, `license = "GPL-3.0-or-later"`, `license-files = ["LICENSE", "NOTICE", "THIRD_PARTY_NOTICES.md"]`(PEP 639; 루트 파일을 빌드 시 복사), core 의존 `pydantic>=2.9,<3`·`pydantic-settings>=2.5,<3`, extras 5종, dev 그룹(ruff·mypy·import-linter·pytest).
2. `src/kortravelcommon/{__init__.py,_version.py,py.typed}` + 빈 서브패키지 `api/`·`openapi/`(T-303·T-304가 채움). 모든 `.py`에 SPDX 헤더.
3. `uv.lock` 생성·커밋, `uv sync --locked --all-extras` 성공.
4. 공개 facade: `kortravelcommon.health`, `kortravelcommon.request_id`, `kortravelcommon.metrics` 등 architecture에 명시된 공개 모듈은 내부 `api.*`를 재수출한다. 이 facade와 내부 api를 프레임워크 의존 허용 대상으로 명시하고, 최상위 `__init__.py`는 api를 eager import하지 않는다. core-only wheel에서 `import kortravelcommon`이 되고 `[api]` 설치 후 공개 facade import가 되는 시험을 수용 기준으로 둔다. 내부 구현 task(T-304·T-307)는 facade를 함께 완성한다.
5. import-linter 계약(`[tool.importlinter]`): core 모듈 목록을 명시해 `fastapi|starlette|sqlalchemy|prometheus_client|httpx|dagster`로의 직접·간접 의존을 금지한다. 내부 `api`·`db`·`http`·`dagster`·`testing`과 위 공개 facade는 extras 영역으로 별도 분류한다. 전체 루트 패키지를 core로 취급해 facade까지 금지하는 계약은 사용하지 않는다.
6. 3.11 문법 검사: ruff `target-version = "py311"` + CI Python 3.11·3.12·3.13 매트릭스에서 `import kortravelcommon` 및 pytest.
7. `.github/workflows/python-package.yml`: `uv build` → 임시 venv에 wheel 설치 → `python -c "import kortravelcommon"` → starlette 매트릭스(`starlette<1.0` / `starlette>=1.6`)로 `[api]` 설치·테스트 → wheel 안 `LICENSE`·`NOTICE`·`THIRD_PARTY_NOTICES.md` 존재 검사. 하드닝은 D-18(권한·concurrency·timeout·`ubuntu-24.04`·SHA 핀).
8. `docs/standards/backend-stack.md` 확정: Python floor/이미지/uv·lock 의무/extras/모듈 우선순위(1차~보류)/메트릭 접두 규칙(D-22)/인증 범위 밖/provider `python-*-api` SHA는 보고만(D-23).

## 범위 밖

모듈 본문(T-303~T-308), `py-v0.1.0` 릴리스와 wheel 자산 발행(T-310), 소비 앱 `uv.lock` 도입(T-440·T-450·T-471), `python-quality.yml` 재사용 워크플로(T-401), PyPI 공개 게시(T-507), Python 앱 floor 3.12 상향(O-7, Phase 4 앱 결정).

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다.

```text
packages/py/kor-travel-common/pyproject.toml
packages/py/kor-travel-common/uv.lock
packages/py/kor-travel-common/README.md
packages/py/kor-travel-common/src/kortravelcommon/{__init__.py,_version.py,py.typed}
packages/py/kor-travel-common/src/kortravelcommon/{api,openapi}/__init__.py
packages/py/kor-travel-common/tests/test_import_surface.py
.github/workflows/python-package.yml
docs/standards/backend-stack.md
docs/architecture/packages.md                # py 절 정합(architecture 소유자와 합의)
```

## 수용 기준

- [ ] `uv build`가 sdist·wheel을 만들고, 깨끗한 venv에 wheel만 설치해 `python -c "import kortravelcommon; print(kortravelcommon.__version__)"`이 3.11·3.12·3.13에서 성공한다.
- [ ] wheel `unzip -l` 출력에 `LICENSE`·`NOTICE`·`THIRD_PARTY_NOTICES.md`가 있고 `METADATA`의 `License-Expression`이 `GPL-3.0-or-later`다.
- [ ] `lint-imports`가 통과하며, core 모듈에서 fastapi를 import하는 테스트용 위반 파일을 두면 실패한다(부정 시험 1회 기록).
- [ ] `uv sync --locked --all-extras`가 lock 변경 없이 성공하고, `[api]` extra가 `starlette<1.0`·`starlette>=1.6` 양쪽에서 설치·import된다.
- [ ] `python3 -B -X utf8 tools/check_spdx.py packages/py`가 0 오류(T-003 도구).
- [ ] `backend-stack.md`에 floor/recommended 값이 `versions.json`과 글자 단위로 일치하고(값은 링크로 인용), O-7이 "열림·기본값 3.11"로 표기돼 있다.
- [ ] `docs.yml`·`python-package` job green.

## 검증 명령

```bash
cd packages/py/kor-travel-common
uv sync --locked --all-extras && uv run pytest -q
uv run lint-imports
uv build && python3 -m venv /tmp/ktc-wheel && /tmp/ktc-wheel/bin/pip install dist/*.whl \
  && /tmp/ktc-wheel/bin/python -c "import kortravelcommon; print(kortravelcommon.__version__)"
unzip -l dist/*.whl | grep -E 'LICENSE|NOTICE|THIRD_PARTY_NOTICES'
uv pip install --python /tmp/ktc-wheel/bin/python "starlette<1.0" ".[api]" && /tmp/ktc-wheel/bin/python -c "import kortravelcommon.api"
cd ../../.. && python3 -B -X utf8 tools/check_spdx.py packages/py && python3 -B -X utf8 tools/validate_document_links.py
```

Git Bash에서 동일하게 실행한다(Windows 절은 [dev-environment](../dev-environment.md)).

## evidence

이 파일 하단 "실행 기록"에 Python 3종·starlette 2종 매트릭스 결과(exit code, 설치된 starlette 버전), wheel 파일명·sha256, `check_spdx` 결과를 남기고 `python-package` run URL을 링크한다. Windows에서 `uv build`만 확인하고 매트릭스를 못 돌리면 `NOT_RUN(CI 필요)`로 적고 CI green 전 DONE 금지(D-25).

## rollback·release 차단 조건

- 패키지 디렉터리·워크플로 신설이므로 `git revert` 1회로 원복된다. 소비자는 아직 없다.
- 다음 중 하나면 T-303~T-305를 시작하지 않는다: wheel에 고지 파일 누락, import-linter 계약 부재, starlette 매트릭스 한쪽 red, `requires-python`이 3.11 미만 앱을 배제.
- 패키지 이름이 PyPI에서 불가하면(T-006) `pyproject` `name`만 바꾸고 import 이름 `kortravelcommon`은 유지한다.
