# T-005b check_versions: `poetry.lock`·`requirements.txt` 파서 + `NO_LOCK` 보고

- 상태: DONE
- 우선순위: P2
- Gate: 도구 테스트
- 선행: T-005

## 목표

`uv.lock`이 없는 소비자(docker-manager Poetry, concierge `requirements*.txt`, geo·map lock 없음)도 report 단계에 올릴 수 있도록 `poetry.lock` 파서와 `requirements.txt` 선언 파서를 추가하고, lock이 없는 경우를 `NO_LOCK`으로 명시 보고한다. Poetry·requirements는 uv 전환 전까지의 과도기 입력이다.

## 고정 결정

- [설계 브리프](../plan/design-brief.md) D-06(uv lockfile 의무; Poetry·requirements.txt는 uv 전환 task), D-07(`NO_LOCK`·`BLOCKED`·`FLOATING_REF`; `blocked[]` `mcp>=2`).
- [백엔드 조사](../survey/cross/backend.md) §2.1(ktdm Poetry, ktc requirements 4종, geo·map·ktc lock 없음).
- [concierge 인벤토리](../survey/inventory/kor-travel-concierge.md) §4.1(`requirements.txt`의 `mcp<2` 주석·2026-09-04 사고), [docker-manager 인벤토리](../survey/inventory/kor-travel-docker-manager.md) §8(공통화 후보 18·19: 핀 레지스트리·strict 파서).
- stdlib만 사용(`tomllib`로 `poetry.lock`, 정규식으로 PEP 508 행). 정확 핀(`==`)만 설치본 후보로 보고 범위 선언(`>=`, `~=`)은 `NO_LOCK` 보조 정보로만 표기.

## 구현 범위

1. `poetry.lock`: `[[package]]` `name`·`version`·`source`(git이면 `reference`/`resolved_reference`) 추출. `resolved_reference` 40자 SHA면 보고, 브랜치만 있으면 `FLOATING_REF`.
2. `requirements.txt`(`-r` 재귀 포함): `pkg==x.y`는 설치본 후보, git URL `@main`은 `FLOATING_REF`, `mcp>=2` 범위가 `blocked[]`와 겹치면 `BLOCKED`; 파일이 lock이 아니므로 결과 표 머리에 `NO_LOCK` 배지를 남긴다.
3. 유효한 소비자 경로/manifest와 선언 파일은 있으나 대응 lock이 없는 경우 `NO_LOCK`과 안내(“`uv.lock` 도입 task”)를 출력한다. 검사 대상 경로/manifest 자체가 없는 호출은 입력 오류(exit 2)이며 별도 음성 fixture로 보존한다.
4. fixture: `tests/fixtures/versions/ktdm/{pyproject.toml,poetry.lock}`(축약), `tests/fixtures/versions/ktc/requirements.txt`와 재귀 `requirements/base.txt`(`mcp<2` 포함), `geo-no-lock/pyproject.toml`, 테스트 추가.

## 범위 밖

- Poetry→uv·requirements→uv 전환 자체(T-471·T-450), `blocked[]` 항목 추가 정책(T-005 소유), `pip freeze` 출력 파싱.

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다. `tools/check_versions.py`, `tests/test_check_versions.py`, `tests/fixtures/versions/ktdm/`, `tests/fixtures/versions/ktc/`, `tests/fixtures/versions/geo-no-lock/`, `docs/standards/versions.md`(지원 lockfile 표).

## 수용 기준

- `poetry.lock` fixture에서 Python 축 판정과 git 참조 판정이 나온다.
- `requirements.txt` fixture는 결과 표에 `NO_LOCK` 배지가 있고 `mcp` 범위가 `BLOCKED`로 표시된다(`::error::`).
- 다른 입력·정책 오류가 없는 선언 파일과 소비자 경로/manifest를 가진 lock 부재 fixture에서 `NO_LOCK`을 보고하고 exit code는 모드 규칙(report 0)을 따른다. 경로/manifest가 없는 호출은 exit 2이며 이 성공 사례에 포함하지 않는다.
- npm·uv 테스트 회귀 없음, Linux·Windows 결과 동일.

## 검증 명령

fixture 디렉터리에는 선언 manifest와 해당 lock/requirements를 함께 만든다. `geo-no-lock`은 유효한 선언 파일만 가진 fixture다. 기존 positional 경로·`--manifest` CLI를 유지한다.

```bash
python3 -B -X utf8 -m unittest discover -s tests -p "test_check_versions.py" -v
python3 -B -X utf8 tools/check_versions.py tests/fixtures/versions/ktdm --repo docker-manager
python3 -B -X utf8 tools/check_versions.py tests/fixtures/versions/ktc --repo concierge; echo "exit=$?"
python3 -B -X utf8 tools/check_versions.py tests/fixtures/versions/geo-no-lock --repo geo; echo "exit=$?"
# 음성 사례: 입력 경로/manifest가 없으므로 exit 2여야 한다.
python3 -B -X utf8 tools/check_versions.py --repo geo; echo "exit=$?"
```

Git Bash에서 동일.

## evidence

- PR #7의 최종 candidate `5b687585cddf6e7a5145911e75647a0e814d9078`를 `codex/t005b-poetry-requirements`에 push했다. PR CI run [34087885355](https://github.com/digitie/kor-travel-common/actions/runs/34087885355)의 docs·check-versions·secret-scan·tools Windows·tools Ubuntu 5개 job이 candidate HEAD와 일치해 모두 성공했다.
- Windows Python 3.14.3과 WSL Python 3.11.15에서 전체 162 tests·skip 0, `test_check_versions.py` focused 67 tests·skip 0이 각각 성공했다. 문서 링크 283/2166, plan 102, SPDX 22, secrets/redaction 351, `check_versions.py --self-check`, `git diff --check`도 오류 0이다.
- fixture `ktdm`은 Poetry Python·fastapi·custom-lib 판정을 보고하고, `ktc`는 requirements `NO_LOCK`·정확 핀·Git `FLOATING_REF`를 보고한다. 조사 원문에 있는 `mcp<2`는 차단되지 않는 정상 음성 사례이며, 합성 `mcp>=2`에서는 `BLOCKED`와 error annotation을 확인했다. `geo-no-lock`은 report 0과 `NO_LOCK`, 경로/manifest 부재 호출은 exit 2다.
- requirements `-r`·`--requirement` 공백/등호/축약형·순환·누락·quoted path·주석/hash·editable, PEP 440 wildcard/compatible/교집합, Poetry source/metadata/조건별 Git, malformed URL 출력 비공개, PEP 508 marker 괄호·인용 문자열·소문자 keyword·역순·값/값·변수/변수 비교를 Windows·WSL 직접 CLI로 확인했다.
- 최초부터 네 차례의 독립 리뷰 원본과 disposition은 [T-005b review archive](../reviews/adversarial/2026-09-07-t005b-post4.md), [manifest](../reviews/adversarial/evidence/2026-09-07-t005b-manifest.md), [A/B post4 원본](../reviews/adversarial/evidence/2026-09-07-t005b-post4-reviewer-a.md), [B 원본](../reviews/adversarial/evidence/2026-09-07-t005b-post4-reviewer-b.md)에 보존했다. 최종은 A PASS / B PASS, 누적 finding 모두 FIXED다.
- `NOT_RUN`: 실제 소비자 저장소 설치·빌드·e2e·Poetry/pip/uv 설치·전환, 전체 resolver 동등성, 소비자 변경·CI, npm/PyPI 게시·Release·태그, merge 후 main CI. common fixture·임시 입력·정적 parser/validator와 PR CI만 실행했다.

## rollback 또는 release 차단 조건

- 도구·테스트만 바뀌므로 `git revert` 1회로 원복한다.
- `requirements.txt` 결과를 lock과 동급으로 표시하는 변경은 D-07 위반이므로 merge하지 않는다.
