# T-005b check_versions: `poetry.lock`·`requirements.txt` 파서 + `NO_LOCK` 보고

- 상태: BLOCKED
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
3. `--lock` 미지정·부재 시 `NO_LOCK` 행 1개와 안내(“`uv.lock` 도입 task”) 출력.
4. fixture: `ktdm.poetry.lock`(축약), `ktc.requirements.txt`(`mcp<2` 포함), 테스트 추가.

## 범위 밖

- Poetry→uv·requirements→uv 전환 자체(T-471·T-450), `blocked[]` 항목 추가 정책(T-005 소유), `pip freeze` 출력 파싱.

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다. `tools/check_versions.py`, `tests/test_check_versions.py`, `tests/fixtures/versions/ktdm.poetry.lock`, `tests/fixtures/versions/ktc.requirements.txt`, `docs/standards/versions.md`(지원 lockfile 표).

## 수용 기준

- `poetry.lock` fixture에서 Python 축 판정과 git 참조 판정이 나온다.
- `requirements.txt` fixture는 결과 표에 `NO_LOCK` 배지가 있고 `mcp` 범위가 `BLOCKED`로 표시된다(`::error::`).
- `--lock` 부재 시 `NO_LOCK` 1행 + exit code는 모드 규칙(report 0).
- npm·uv 테스트 회귀 없음, Linux·Windows 결과 동일.

## 검증 명령

fixture 디렉터리에는 선언 manifest와 해당 lock/requirements를 함께 만든다. 기존 positional 경로·`--manifest` CLI를 유지한다.

```bash
python3 -B -X utf8 -m unittest discover -s tests -p "test_check_versions.py" -v
python3 -B -X utf8 tools/check_versions.py tests/fixtures/versions/ktdm --repo docker-manager
python3 -B -X utf8 tools/check_versions.py tests/fixtures/versions/ktc --repo concierge; echo "exit=$?"
python3 -B -X utf8 tools/check_versions.py --repo geo; echo "exit=$?"
```

Git Bash에서 동일.

## evidence

- 테스트 수·exit code·판정 표를 이 절과 `docs/journal.md`에 남긴다. 실제 ktdm·ktc 파일(조사 기준 커밋) 대조 결과를 첨부하고 미실행이면 `NOT_RUN`.

## rollback 또는 release 차단 조건

- 도구·테스트만 바뀌므로 `git revert` 1회로 원복한다.
- `requirements.txt` 결과를 lock과 동급으로 표시하는 변경은 D-07 위반이므로 merge하지 않는다.
