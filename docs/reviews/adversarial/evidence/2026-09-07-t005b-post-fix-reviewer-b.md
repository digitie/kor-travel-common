# T-005b post-fix 독립 full 적대적 리뷰 B 원본

- 실행 ID: `B-T005B-POST-20260907-135800-cdf7ba0`
- 최종 판정: **BLOCK**. 최초 B finding 4건은 FIXED. 새 finding P1 1건·P2 1건은 OPEN.
- 시작: 2026-09-07T13:58:00.9709976+09:00. 종료 SHA·clean 확인: 2026-09-07T14:07:25.3601058+09:00.
- immutable candidate: `cdf7ba01ccb585b3c00aec69a734266e33ceb510`
- 요청 base: `796445fadb9b4fa6de2f392d6169f31abdccc0fa`
- 최초 B 검토 candidate: `12570ccebc58c81510bab7de0735eb4720c494c4`
- 실제 시작·종료 HEAD는 candidate와 일치. tree: `16361fd4103e4714cd98d82ff4657f48339189df`.
- 새 격리 worktree: `F:/dev/kor-travel-common-wt/review-t005b-b-post`. candidate에서 detached로 생성했으며 시작·종료 `git status --porcelain=v1` 출력은 비어 있었다.
- 후보·소비자·다른 작업자의 파일·과거 evidence를 수정하거나 commit하지 않았다. 시험 입력과 CLI 산출물은 임시 디렉터리에서 생성·정리했다. 지정된 이 원본만 기본 checkout의 `.git/codex-audit`에 저장한다.
- 최초 B 원본만 읽었다. A 및 다른 reviewer 결과를 읽거나 요청하지 않은 상태로 확정한다.

## 전달 요청 원문

> T-005b post-fix 재검토를 시작해 주세요. immutable candidate `cdf7ba01ccb585b3c00aec69a734266e33ceb510`, base `796445fadb9b4fa6de2f392d6169f31abdccc0fa`. 새 detached worktree `F:/dev/kor-travel-common-wt/review-t005b-b-post`를 candidate에서 만들고, old B 결과는 기준으로만 삼되 A 결과는 읽거나 요청하지 마세요. B 전문 영역: Poetry lock package/source 모든 타입·metadata python-versions 누락/빈/숫자/범위·URL hostname/port·오류 원문 비공개, 조건별 dependency list의 branch/tag/rev 보존, GitHub 외 HTTPS Git의 SHA/tag/branch와 uv/npm 회귀. 전체 delta를 공격적으로 보고 old B-P1-01/P1-02/P1-03/P2-04의 수정 여부와 새 finding을 재현하세요. Windows·WSL 전체/focused tests 및 validators, direct CLI cases를 실행하세요. 결과 원본을 `.git/codex-audit/2026-09-07-t005b-post-fix-reviewer-b.md`에 저장하고 PASS/BLOCK, 각 finding disposition, 시작/종료 SHA·clean·NOT_RUN을 메시지로 보고하세요. 수정/commit하지 마세요.

## 검토 범위와 재사용

base부터 13파일·840행 추가·69행 삭제다. 최초 B 검토 이후에는 4파일·488행 추가·98행 삭제다. 해당 4파일(`tools/check_versions.py`, 시험, 버전 정본, 도구 README)의 전체 delta를 읽고, source·범위·manifest 발견·출력의 기존 문맥과 대조했다. 변경 없는 최초 delta는 최초 B 원본의 검토 범위를 재사용했다. `AGENTS.md`·`docs/README.md`·`versions.json`은 요청 base와 diff가 없음을 직접 확인했다.

T-005b 상세 수용 기준·resume·버전 정본을 대조했다. task는 IN_PROGRESS이며 소비자 설치·이관 완료로 표시하지 않는다. 범위·metadata 검사를 강화하고 requirements 패턴·hash/editable 처리를 추가한 문서와 코드는 검토한 경로에서 일치한다. 다만 새 형식 whitelist의 upstream 호환성과 오류 출력 경계에 아래 결함이 있다.

2026-09-07에 공식 upstream의 **Poetry 2.2.1 고정 tag**를 다시 읽었다. `locker.py`는 root extras와 source subdirectory를 기록하며 source reference를 Git에만 제한하지 않는다. `legacy_repository.py`는 index 이름을 legacy source reference로 설정한다. 이것은 조사 추정이나 작성자의 evidence가 아니라 정상 lock 생성 코드와의 직접 대조다.

## 직접 실행한 검증

| 명령·검사 | 실제 결과 |
|---|---|
| Windows `py -3.14 -B -X utf8 -m unittest discover -s tests -p 'test_*.py'` | Python 3.14.3, 155 tests, 42.246초, OK, skip 0 |
| WSL Python 3.11.15, 같은 전체 unittest 명령 | 155 tests, 22.198초, OK, skip 0 |
| Windows 같은 명령의 `-p 'test_check_versions.py'` | 60 tests, 13.720초, OK, skip 0 |
| WSL 같은 집중 시험 | 60 tests, 12.334초, OK, skip 0 |
| 양 OS 각각 `tools/validate_document_links.py` | 283문서·2166대상·오류 0 |
| 양 OS 각각 `tools/validate_plan.py` | 102 task·오류 0 |
| 양 OS 각각 `tools/check_spdx.py` | 22파일·오류 0 |
| 양 OS 각각 `tools/check_versions.py --self-check` | exit 0, 레지스트리 자체 검사 통과 |
| `git diff --check 796445fadb9b4fa6de2f392d6169f31abdccc0fa HEAD` | exit 0, 출력 없음 |
| 최초 B 핵심 반례·정상 대조·저장소 fixture 8개, 양 OS | 같은 행·exit·error annotation. 최초 네 finding 모두 수정 확인 |
| 새 Poetry 경계 CLI 41개, 양 OS | 같은 결과. 35개 초기 기대 일치, 5개 새 finding 재현, 1개 아래의 제한 범위 판정 |
| 기존 uv/Python/ref 독립 CLI 32개, 양 OS | 32/32 기대 일치 |
| 잘못된 manifest URL의 report/fail 출력 경로 2개, 양 OS | 양 모드에서 stdout·JSON·Markdown·step summary에 합성 marker 존재 |

집중 60개는 전체 155개에 포함되므로 고유 시험 수를 합산하지 않는다. 양 OS도 같은 시험을 각각 실행한 것이며 고유 시험을 두 배로 세지 않는다. 모든 Python 실행은 `-B -X utf8`를 사용했다.

WSL 실행 형태는 다음과 같다.

```text
wsl.exe --exec bash -lc 'cd /mnt/f/dev/kor-travel-common-wt/review-t005b-b-post && /home/digitie/.local/share/uv/python/cpython-3.11-linux-x86_64-gnu/bin/python3.11 -B -X utf8 -m unittest discover -s tests -p "test_*.py"'
```

합성 CLI는 PowerShell here-string을 Windows Python 또는 같은 WSL Python의 stdin으로 전달했다. Python `tempfile.TemporaryDirectory` 안에 manifest·lock을 만든 후 다음 형태의 실제 subprocess를 실행하고 JSON findings와 exit를 읽었다.

```text
<python> -B -X utf8 tools/check_versions.py <임시 입력 경로> --repo docker-manager --mode fail --no-step-summary --json <임시 report.json>
```

범위 probe의 `>=3.11,!=3.12.*`는 초기 기대 0과 달리 양 OS에서 Python NO_ENGINES·exit 1이었다. `lower_bound`가 지원하지 않는 배제 범위를 미확인으로 남기는 기존 경계이며, 정본도 전체 PEP 440 해석을 약속하지 않는다. 정상으로 축소하지 않았으므로 새 finding으로 세지 않았다. 이 차이를 시험 통과로 바꾸거나 숨기지 않았다.

## 최초 finding disposition

| 원 ID·심각도 | 판정 | 재현 결과 |
|---|---|---|
| B-P1-01 / P1 | FIXED | Python 조건별 branch/tag 배열에서 branch v1.2.3이 FLOATING_REF로 남고 fail exit 1. group 배열과 marker/lock 순서 반전도 동일하게 차단 |
| B-P1-02 / P1 | FIXED | `--requirement=child.txt`와 공백형 모두 child의 mcp>=2를 BLOCKED·error annotation으로 보고. report exit 0은 모드 계약대로 유지 |
| B-P1-03 / P1 | FIXED | lock metadata Python 누락·빈 문자열·숫자·잘못된 범위·빈 교집합은 exit 2. 정상 >=3.10 하한은 BELOW_FLOOR·1, >=3.11은 OK·0 |
| B-P2-04 / P2 | FIXED | codeberg.org HTTPS Git의 40자리 rev·버전형 tag는 OK·0. 같은 호스트의 명시 branch는 FLOATING_REF·1 |

기존 Poetry 전이 SHA·branch 판정과 uv/npm 회귀는 전체 시험 및 32개 직접 CLI에서 확인했다. uv branch의 @·%40 구분, tag/rev 우회 반례, marker 순서·복수 lock SHA, Python 축·source/group 경계의 기대 결과가 유지됐다.

저장소 fixture는 후보 파일 바이트를 임시 입력에 복사해 양 OS에서 실행했다. ktdm은 Python·fastapi·custom-lib 3행 OK; ktc는 NO_ENGINES·fastapi OK·NO_LOCK·custom-lib FLOATING_REF; geo-no-lock은 Python OK·fastapi NO_LOCK이다. report exit는 각각 0이며 ktc에는 error annotation이 있다. mcp>=2 차단은 별도 include 양성 사례에서 검증했다.

## B-P2-05 — 새 whitelist가 Poetry의 정상 lock 필드를 거부한다

- 심각도: **P2**. Disposition: **OPEN**.
- 위치: `tools/check_versions.py:450`·`:455`·`:487`·`:508`·`:525`.
- 재현: 정상 fixture의 manifest Python은 ^3.11, lock fastapi는 0.141.1, metadata Python은 >=3.11,<4로 둔다. 아래 세 요소를 각각 독립 추가한다.

```toml
# 사례 1: lock 최상위. package.extras가 아니다.
[extras]
web = ["fastapi"]

# 사례 2: fastapi package source. 정상 index 이름이다.
[package.source]
type = "legacy"
url = "https://example.com/simple"
reference = "mirror"

# 사례 3: 정상 전체 resolved SHA를 가진 git package source에 추가.
subdirectory = "python"
```

- 실제 결과: 세 사례 모두 Windows·WSL에서 exit 2, findings JSON을 생성하지 않는다. 각각의 해당 요소를 제거한 대조는 exit 0이다.
- 직접 원문 대조: [Poetry 2.2.1 locker.py](https://github.com/python-poetry/poetry/blob/2.2.1/src/poetry/packages/locker.py)의 root extras 생성(197~201), source 직렬화(540~563), source subdirectory 읽기(341); [Poetry 2.2.1 legacy_repository.py](https://github.com/python-poetry/poetry/blob/2.2.1/src/poetry/repositories/legacy_repository.py)의 legacy source reference 설정을 확인했다. 세 형태 모두 upstream에서 생성한다.
- 원인: 최상위 extras와 source subdirectory가 whitelist에 없고, non-git reference를 무조건 오류로 처리한다.
- 영향: 선택 extras·사용자 index·Git 하위 디렉터리를 사용하는 정상 과도기 Poetry 소비자는 버전 report 자체를 만들지 못한다. 알려지지 않은 임의 필드에 대한 차단과 정상 upstream 필드의 거부는 구별해야 한다.
- 권고: 고정 upstream에 맞춰 해당 필드·타입을 검증한 후 필요한 축·Git 참조를 계속 검사한다. legacy reference를 branch로 해석하지 말고, Git subdirectory가 있어도 원래 SHA/tag/branch 판정을 유지한다. 정상 출력 fixture와 잘못된 타입의 음성 fixture를 함께 보존한다.

## B-P1-06 — 잘못된 manifest Git URL 원문이 보고 출력으로 전달된다

- 심각도: **P1**. Disposition: **OPEN**.
- 위치: `tools/check_versions.py:947`~`:953`, `:1504`~`:1519`.
- 재현: lock URL과 전체 resolved SHA는 정상으로 둔다. manifest의 Git URL에 잘못된 IPv6 hostname 또는 비숫자 port를 넣는다. 원문 노출 검사용 합성 marker는 문자열을 나눠 생성했다.

```python
marker = "SYNTH" + "CHECK" + "Z" * 10
url = "https://example.com:" + marker + "/repo.git"
# custom-lib = {git = url, tag = "v1.2.3"} 형태로 TOML 직렬화한다.
```

- 실제 결과: 양 OS에서 입력 오류 2가 아니라 FLOATING_REF가 된다. fail은 exit 1, report는 exit 0이다. 양 모드 모두 stdout·`--json`·`--markdown`·`GITHUB_STEP_SUMMARY`에서 marker 포함 여부가 true였다. stderr에는 없었다. 이 보고서와 도구 출력에는 합성 값 전체나 실제 비밀을 출력하지 않았다.
- 정상 음성 대조: 같은 잘못된 URL을 lock source에 넣으면 `_validate_url`가 일반 오류로 닫고 exit 2, marker 비노출이다.
- 원인: manifest Git 선언은 URL 구조 검증 없이 `urls`에 저장된다. `ref_is_pinned`가 hostname/port의 ValueError를 False로 바꾸지만, 호출자는 원래 선언 문자열을 FLOATING_REF 행에 담아 모든 보고 경로로 보낸다. 예외 문구만 없애는 조치로 원문 비공개를 보장하지 못한다.
- 영향: 잘못된 URL 값에 포함된 불필요한 입력 원문이 CI 요약·보존 artifact로 확산된다. 실제 자격증명 유출은 수행하거나 관찰하지 않았으며, 합성 marker의 전달 경로만 입증했다. report 모드는 이러한 잘못된 manifest 입력도 정상 모드 exit 0으로 종료한다.
- 권고: Poetry manifest Git URL의 hostname·port·구조를 findings 생성 전에 검증하고, 실패는 값을 포함하지 않는 일반 manifest 입력 오류 2로 처리한다. 본문·JSON·Markdown·step summary의 비노출과 report/fail 동일 입력 오류를 함께 검증한다. lock에만 적용한 비공개 경계를 manifest에도 유지한다.

## 미실행과 최종 판정

NOT_RUN: 이 immutable SHA의 원격 CI, Poetry lock 생성/설치, pip install·uv sync, 실제 소비자 파일의 새 전체 대조·수정·빌드·e2e, 태그·Release·registry 게시. 해당 외부 gate의 성공을 이 로컬 리뷰로 주장하지 않는다. 공식 upstream source 구조는 읽었지만 Poetry resolver 전체 의미와 동등하다고 주장하지 않는다.

기존 B 네 finding은 FIXED이며 전체·집중 시험과 validator는 직접 통과했다. 새 P1·P2 두 finding은 양 OS에서 재현했고 원문·코드로 확인했다. **BLOCK**: 두 finding의 disposition과 수정 candidate에 대한 독립 재검토가 필요하다.
