# T-005a check_versions: `uv.lock` 파서

- 상태: READY
- 우선순위: P1
- Gate: 도구 테스트
- 선행: T-005

## 목표

`tools/check_versions.py`가 `uv.lock`을 읽어 Python 축(fastapi·starlette·pydantic·sqlalchemy·alembic·ruff·mypy·pytest·dagster 등)과 `requires-python`, git 소스 핀을 `versions.json`과 대조하게 한다. lockfile 의무(`uv.lock` + CI·Docker `--locked`)를 보고 단계에서 검증할 수 있게 된다.

## 고정 결정

- [설계 브리프](../plan/design-brief.md) D-06(Python 축·uv floor 0.11·lockfile 의무), D-07(`lockfiles[]` 대조, `FLOATING_REF`·`NO_LOCK` 판정), D-15(`requires-python >=3.11`).
- [백엔드 조사](../survey/cross/backend.md) §2.1(빌드·lock 현황: weather·airport만 `uv.lock`), §5.1(`git+https@<sha>` 관례, pinvi etl `@main`).
- [버전 매트릭스](../survey/cross/version-matrix.md) §2.1·§2.7(provider git 핀), §7.1(Python lock 소비 현황).
- 파서는 Python 3.11 stdlib `tomllib`만 사용한다(D-03 Windows Tier 2).

## 구현 범위

1. `tools/check_versions.py`에 기존 소비자 디렉터리/manifest 입력으로 `uv.lock` 자동 탐색·판별(파일명·`version = 1` 헤더)을 검증. `[[package]]`의 `name`·`version`·`source`(`registry`/`git`/`editable`/`directory`)를 읽고 프로젝트 자신(`source.editable`/`virtual`)의 `requires-python`을 대조한다.
2. git 소스: `source.git` URL의 rev가 40자 SHA면 `providers` 절에 보고, 브랜치·태그 참조면 `FLOATING_REF`.
3. `tests/fixtures/versions/weather.uv.lock`(축약 fixture)·`git-main.uv.lock`으로 `OK/BELOW_FLOOR/NOT_RECOMMENDED/FLOATING_REF/NO_LOCK` 검증.
4. `docs/standards/versions.md`의 "지원 lockfile" 표에 `uv.lock` 행과 `--locked` 요구를 반영(값 복제 없이).

## 범위 밖

- `poetry.lock`·`requirements.txt`(T-005b), 소비자 저장소에 `uv.lock`을 도입하는 작업(T-440·T-450·T-471·T-484), `[api]` starlette 범위 결정(T-302).

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다. `tools/check_versions.py`, `tests/test_check_versions.py`, `tests/fixtures/versions/*.uv.lock`, `docs/standards/versions.md`.

## 수용 기준

- `uv.lock` fixture로 실행 시 Python 축 판정이 표에 나오고 `requires-python` 하한이 3.11 미만이면 `BELOW_FLOOR`.
- `@main` git 소스는 `FLOATING_REF` + `::error::`, 40자 SHA는 `providers` 보고 행으로만 나온다.
- `uv.lock`이 없는 저장소(`--lock` 미지정·파일 부재)는 `NO_LOCK`으로 보고하고 exit code는 모드 규칙을 따른다.
- 외부 의존 0(`import tomllib`만), Linux·Windows 결과 동일.
- 기존 npm 테스트가 그대로 통과한다.

## 검증 명령

fixture 디렉터리에는 선언 manifest와 해당 lock/requirements를 함께 만든다. 기존 positional 경로·`--manifest` CLI를 유지한다.

```bash
python3 -B -X utf8 -m unittest discover -s tests -p "test_check_versions.py" -v
python3 -B -X utf8 tools/check_versions.py tests/fixtures/versions/weather --repo weather
python3 -B -X utf8 tools/check_versions.py tests/fixtures/versions/git-main --repo pinvi; echo "exit=$?"
```

Git Bash에서 동일.

## evidence

- 테스트 수·exit code·판정 표를 이 절과 `docs/journal.md`에 남긴다. 실제 소비자 `uv.lock`(weather·airport, 조사 기준 커밋) 대조 결과를 첨부하고 미실행이면 `NOT_RUN`.

## rollback 또는 release 차단 조건

- 도구·테스트만 바뀌므로 `git revert` 1회로 원복한다.
- npm 판정 회귀가 생기면 merge하지 않는다.
