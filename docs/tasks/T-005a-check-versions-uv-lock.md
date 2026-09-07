# T-005a check_versions: `uv.lock` 파서

- 상태: DONE
- 우선순위: P1
- Gate: 도구 테스트
- 선행: T-005

## 목표

`tools/check_versions.py`가 `uv.lock`을 읽어 Python 축(fastapi·starlette·pydantic·sqlalchemy·alembic·ruff·mypy·pytest·dagster 등)과 `requires-python`, git 소스 핀을 `versions.json`과 대조하게 한다. lockfile 존재·지원 형식과 기록된 버전을 정적으로 보고한다. CI·Docker의 `--locked` 실행과 선언/lock 일치는 소비자 gate이며 이 파서의 성공 주장이 아니다.

## 고정 결정

- [설계 브리프](../plan/design-brief.md) D-06(Python 축·uv floor 0.11·lockfile 의무), D-07(`lockfiles[]` 대조, `FLOATING_REF`·`NO_LOCK` 판정), D-15(`requires-python >=3.11`).
- [백엔드 조사](../survey/cross/backend.md) §2.1(빌드·lock 현황: weather·airport만 `uv.lock`), §5.1(`git+https@<sha>` 관례, pinvi etl `@main`).
- [버전 매트릭스](../survey/cross/version-matrix.md) §2.1·§2.7(provider git 핀), §7.1(Python lock 소비 현황).
- 파서는 Python 3.11 stdlib `tomllib`만 사용한다(D-03 Windows Tier 2).

## 구현 범위

1. 기존 소비자 디렉터리/manifest 입력으로 `uv.lock` 자동 탐색·판별과 지원 schema를 검증한다. `[[package]]`의 `name`·`version`·`source`를 읽고 manifest와 lock 최상위의 `requires-python`을 각각 대조한다. 공유 lock은 명시된 멤버 범위만 있어도 전이 축·차단·git 소스를 검사한다. 알 수 없는 schema/source는 정상 설치본으로 보고하지 않는다.
2. git 소스: 선언의 branch는 lock에 SHA가 있어도 `FLOATING_REF`; 전체 SHA·버전형 태그 선언은 버전 정본 §3.8에 따라 허용한다. lock의 `source.git`은 해석된 전체 SHA fragment를 별도로 확인한다. provider는 설치 축과 구분해 보고한다. 2026-09-07 정정: 과거 task의 태그 일괄 금지 문구는 상위 버전 정본과 충돌해 제거했다.
3. `tests/fixtures/versions/weather/uv.lock`(축약 fixture)·`git-main/uv.lock`으로 `OK/BELOW_FLOOR/NOT_RECOMMENDED/FLOATING_REF/NO_LOCK` 검증.
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
- 지원하지 않는 lock version/revision, 잘못된 package/source 형태, lock Python 하한 누락·미해석, marker별 복수 버전, dependency group·복수 git source, 공유 lock 멤버 입력을 정상 값으로 숨기지 않는 회귀 시험을 둔다.

## 검증 명령

fixture 디렉터리에는 선언 manifest와 해당 lock/requirements를 함께 만든다. 기존 positional 경로·`--manifest` CLI를 유지한다.

```bash
python3 -B -X utf8 -m unittest discover -s tests -p "test_check_versions.py" -v
python3 -B -X utf8 tools/check_versions.py tests/fixtures/versions/weather --repo weather
python3 -B -X utf8 tools/check_versions.py tests/fixtures/versions/git-main --repo pinvi; echo "exit=$?"
```

Git Bash에서 동일.

## evidence

- 최종 candidate `3c5801f14855a067080f257ec83d2279de32c74a`의 PR #6 CI run `34080403871`에서 `docs`, `tools (ubuntu-24.04)`, `tools (windows-2025)`, `secret-scan`, `check-versions`가 모두 성공했다.
- Windows Python 3.14.3·WSL Python 3.11.15에서 전체 140 tests·skip 0, `test_check_versions.py` 45 tests, `check_versions.py --self-check`, SPDX·문서 링크·계획·비밀/운영정보 검사와 `git diff --check`가 성공했다.
- 두 독립 reviewer의 최종 post-fix가 A PASS/B PASS이고 누적 8개 finding이 모두 FIXED다. [통합 판정](../reviews/adversarial/2026-09-07-t005a-post3.md), [A 원본](../reviews/adversarial/evidence/2026-09-07-t005a-post3-reviewer-a.md), [B 원본](../reviews/adversarial/evidence/2026-09-07-t005a-post3-reviewer-b.md)에 실행 ID·반례·clean SHA를 보존했다.
- 실제 공항 저장소는 읽기 전용으로 양 OS에서 `findings=24 failing=2 exit=0`, weather fixture는 `findings=2 failing=0 exit=0`을 재현했다. 이는 제품 gate 성공이 아닌 정적 관찰이다.
- NOT_RUN: 실제 소비자 `uv sync --locked`·설치·빌드·e2e, 전체 upstream lock 생성 형식 동등성, npm/PyPI 게시·Release·태그, 소비자 저장소 쓰기.

## rollback 또는 release 차단 조건

- 도구·테스트만 바뀌므로 `git revert` 1회로 원복한다.
- npm 판정 회귀가 생기면 merge하지 않는다.
