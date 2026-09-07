# T-005b post-fix 2 독립 full 적대적 리뷰 B 원본

- 실행 ID: `B-T005B-POST2-20260907-141508-ca461c4`
- 최종 판정: **BLOCK**. 기존 B-P1-06은 OPEN, 새 B-P2-07은 OPEN. 기존 다른 B finding 5건은 FIXED.
- 시작: 2026-09-07T14:15:08.3812387+09:00. 종료 SHA·clean 확인: 2026-09-07T14:21:47.4348178+09:00.
- immutable candidate: `ca461c45e000ff24feb5a4bdf4478fefa333db8a`.
- 요청 base: `796445fadb9b4fa6de2f392d6169f31abdccc0fa`.
- delta base: `cdf7ba01ccb585b3c00aec69a734266e33ceb510`.
- tree: `154412711572ab7c5b91c2f9b8576c123a647d23`.
- 격리: `F:/dev/kor-travel-common-wt/review-t005b-b-post2`에 candidate로 새 detached worktree를 생성했다. 직접 확인한 시작·종료 HEAD가 candidate와 같고, 양 시점 `git status --porcelain=v1`은 빈 출력이었다.
- 후보·소비자·다른 작업자의 파일·기존 원본은 수정하거나 commit하지 않았다. 임시 시험 입력·CLI 산출물은 임시 디렉터리에서 생성·정리했고, 이 원본만 지정된 기본 checkout의 `.git/codex-audit`에 저장한다.
- 이전 B 원본을 기준으로 삼았으며 A 및 다른 reviewer 결과는 읽거나 요청하지 않은 상태로 확정했다.

## 전달 요청 원문

> T-005b post-fix 2 재검토를 진행해 주세요. immutable candidate `ca461c45e000ff24feb5a4bdf4478fefa333db8a`, base `796445fadb9b4fa6de2f392d6169f31abdccc0fa`, delta base `cdf7ba01ccb585b3c00aec69a734266e33ceb510`. 새 detached worktree `F:/dev/kor-travel-common-wt/review-t005b-b-post2`. B 영역: 이전 B-P2-05/B-P1-06의 Poetry extras·legacy reference·git subdirectory upstream 호환성과 malformed manifest URL의 모든 출력 경로 비공개·exit2, Poetry source/metadata/Git·uv/npm 회귀, 전체 delta. A 결과는 읽거나 요청하지 마세요. Windows/WSL 전체·focused tests, validators, direct CLI/output paths를 실행하세요. 원본을 `.git/codex-audit/2026-09-07-t005b-post2-reviewer-b.md`에 저장하고 PASS/BLOCK, finding disposition, SHA/clean/NOT_RUN을 보고하세요. 수정/commit하지 마세요.

## 범위와 재사용

요청 base부터 13파일·1009행 추가·69행 삭제다. 이번 delta는 3파일·190행 추가·21행 삭제이며 `tools/check_versions.py`, `tests/test_check_versions.py`, `docs/standards/versions.md`의 전체 변경을 읽었다. Poetry whitelist·URL 처리 외에 requirements include 경로·옵션·범위 교집합·새 marker 검사도 검토했다.

변경 없는 최초·직전 범위는 이전 B 원본의 코드·정본·고정 Poetry upstream 대조를 재사용했다. AGENTS·docs/README·resume·versions.json·T-005b 상세 task가 이번 delta에 없음을 직접 확인했다. task IN_PROGRESS와 현재 소비자·게시 경계는 유지된다. 새 수정에 대해 로컬 검증과 직접 반례를 다시 실행했다.

## 직접 실행한 검증

| 명령·검사 | 실제 결과 |
|---|---|
| Windows `py -3.14 -B -X utf8 -m unittest discover -s tests -p 'test_*.py'` | Python 3.14.3, 160 tests, 41.825초, OK, skip 0 |
| WSL Python 3.11.15, 같은 전체 시험 | 160 tests, 23.061초, OK, skip 0 |
| Windows 같은 명령의 `-p 'test_check_versions.py'` | 65 tests, 13.650초, OK, skip 0 |
| WSL 같은 집중 시험 | 65 tests, 12.937초, OK, skip 0 |
| 양 OS 각각 `tools/validate_document_links.py` | 283문서·2166대상·오류 0 |
| 양 OS 각각 `tools/validate_plan.py` | 102 task·오류 0 |
| 양 OS 각각 `tools/check_spdx.py` | 22파일·오류 0 |
| 양 OS 각각 `tools/check_versions.py --self-check` | exit 0, 레지스트리 자체 검사 통과 |
| `git diff --check 796445fadb9b4fa6de2f392d6169f31abdccc0fa HEAD` | exit 0, 출력 없음 |
| 이전 B 핵심 반례·정상 대조·저장소 fixture 8개, 양 OS | 최초 네 finding 수정 유지, fixture 판정 동일 |
| Poetry source·metadata·Git 경계 41개, 양 OS | 40개 기대 일치, 이전 잘못된 IPv6 manifest URL 1개 미해결 |
| 기존 uv/Python/ref 독립 CLI 32개, 양 OS | 32/32 기대 일치 |
| port·IPv6 각각 report/fail 출력 경로 총 4개, 양 OS | port 2개는 값 비노출·exit 2. IPv6 2개는 B-P1-06 재현 |
| 새 marker 직접 CLI 9개와 packaging parser 대조, 양 OS | 5개 기대 일치, 유효한 입력 4개가 exit 2로 거부됨 |

전체 160개에 집중 65개가 포함되므로 고유 시험 수를 합산하지 않는다. 두 OS도 동일 시험을 각각 실행한 것이다. 모든 후보 Python 실행은 `-B -X utf8`를 사용했다.

WSL 명령은 다음 형태다.

```text
wsl.exe --exec bash -lc 'cd /mnt/f/dev/kor-travel-common-wt/review-t005b-b-post2 && /home/digitie/.local/share/uv/python/cpython-3.11-linux-x86_64-gnu/bin/python3.11 -B -X utf8 -m unittest discover -s tests -p "test_*.py"'
```

독립 CLI는 Python stdin 스크립트에서 `TemporaryDirectory`에 선언·lock을 만들고 실제 subprocess로 다음 명령을 실행했다. 저장소 fixture도 후보 파일 바이트를 임시 디렉터리에 복사해 검사했다.

```text
<python> -B -X utf8 tools/check_versions.py <임시 입력 경로> --repo docker-manager --mode <report|fail> --no-step-summary --json <임시 report.json>
```

출력 비공개 시험에서는 `--no-step-summary`를 제외하고 `--markdown`과 임시 `GITHUB_STEP_SUMMARY`를 실제 설정했다. stdout·stderr·JSON·Markdown·summary의 marker 포함 여부만 출력했으며 합성 값 전체는 출력하지 않았다.

## 기존 finding disposition

| 원 ID·심각도 | 판정 | 이번 직접 결과 |
|---|---|---|
| B-P1-01 / P1 | FIXED | Poetry 조건별 branch/tag 배열과 group·lock 순서 반전에서 branch가 FLOATING_REF·exit 1 |
| B-P1-02 / P1 | FIXED | include 등호·공백형 모두 mcp>=2의 BLOCKED·error annotation 유지 |
| B-P1-03 / P1 | FIXED | Python metadata 누락·빈·숫자·잘못된 범위는 2, 낮은 하한은 BELOW_FLOOR·1, 정상 하한은 0 |
| B-P2-04 / P2 | FIXED | GitHub 외 HTTPS Git의 정상 SHA/tag는 0, 명시 branch는 1 |
| B-P2-05 / P2 | FIXED | top extras·legacy reference·git subdirectory 세 독립 정상 사례 모두 0, 기존 축·Git 판정 유지 |
| B-P1-06 / P1 | **OPEN** | port는 수정됐지만 이전 IPv6 반례는 stdout·JSON·Markdown·summary 비공개 및 exit 2를 충족하지 못함 |

B-P2-05는 이전에 직접 읽은 Poetry 2.2.1 고정 tag의 [locker.py](https://github.com/python-poetry/poetry/blob/2.2.1/src/poetry/packages/locker.py)와 [legacy_repository.py](https://github.com/python-poetry/poetry/blob/2.2.1/src/poetry/repositories/legacy_repository.py) 구조 대조를 재사용하고, 후보 CLI에서 세 입력을 새로 실행했다. uv의 @·%40 branch/tag/rev·복수 SHA·marker 순서와 npm 회귀는 전체 시험 및 32개 CLI에서 유지됐다.

ktdm fixture는 Python·fastapi·custom-lib OK, ktc는 NO_ENGINES·fastapi OK·NO_LOCK·custom-lib FLOATING_REF, geo-no-lock은 Python OK·fastapi NO_LOCK이었다. report exit는 모두 0이며 ktc에는 error annotation이 있다. mcp>=2 차단은 별도 include 양성 사례에서 확인했다.

## B-P1-06 — 이전 잘못된 IPv6 manifest URL 반례가 남아 있다

- 원 심각도: **P1**, 변경하지 않음. Disposition: **OPEN**.
- 위치: `tools/check_versions.py:1613`~`:1619`의 URL·ref 결합 및 `:967`~`:979`의 결합 후 URL 검사.
- 재현: 이전 원본과 같은 경로 없는 잘못된 bracket URL을 Poetry manifest Git 선언에 넣고 정상 tag·정상 lock SHA를 둔다. 합성 marker는 분할 생성한다.

```python
marker = "SYNTH" + "CHECK" + "Z" * 10
url = "https://[" + marker + "]"
# custom-lib = {git = url, tag = "v1.2.3"} 형태로 TOML 직렬화한다.
```

- 실제 결과: Windows·WSL 모두 custom-lib FLOATING_REF. report exit 0, fail exit 1. 두 모드의 stdout·JSON·Markdown·실제 GITHUB_STEP_SUMMARY에 marker 포함 여부가 모두 true였다. stderr에는 없었다. 실제 비밀은 사용하거나 노출하지 않았다.
- port 음성 대조: 같은 marker를 비숫자 port에 넣은 이전 반례는 report/fail 모두 exit 2, stdout·stderr 비노출, JSON·Markdown·summary 미생성이다. 따라서 port 수정만으로 전체 finding을 FIXED로 판단하지 않았다.
- 원인: 원래 Git URL에 `@v1.2.3`를 덧붙이고 나서 구조를 검사한다. 경로가 없는 URL에서는 덧붙인 @ 때문에 bracket 부분이 userinfo, tag 부분이 hostname으로 재해석된다. 원래 URL의 잘못된 host가 사라진 구조를 검사하므로 ValueError가 발생하지 않고 원래 선언 값이 FLOATING_REF 행으로 전달된다.
- 영향: 이전 finding의 합성 입력 원문이 여전히 CI 요약·보존 산출물로 전달된다. report 모드에서는 잘못된 입력도 exit 0이다.
- 권고: Poetry manifest의 원래 Git URL을 ref와 합치기 전에 검증한다. 잘못된 원래 URL은 값을 포함하지 않는 일반 manifest 입력 오류 2로 중단한다. 경로 없는 bracket URL·경로 있는 URL·비숫자 port를 각각 report/fail과 모든 출력 경로로 재검증한다.

## B-P2-07 — 새 marker 검사가 정상 괄호 복합식과 역순 비교를 거부한다

- 심각도: **P2**. Disposition: **OPEN**.
- 위치: `tools/check_versions.py:1056`~`:1077`, 특히 `:1063`의 and/or 분할과 이름을 왼쪽에만 허용하는 clause 정규식.
- 재현: 다음 각 행을 독립 requirements.txt로 만든 뒤 report 모드로 실행한다.

```text
fastapi==0.141.1; (python_version < "3.12" and sys_platform == "win32")
fastapi==0.141.1; python_version >= "3.11" and (sys_platform == "win32" or sys_platform == "linux")
fastapi==0.141.1; "3.12" > python_version
mcp>=2; (python_version >= "3.11" and sys_platform == "win32")
```

- 실제 결과: 네 행 모두 Windows·WSL에서 exit 2, findings JSON 미생성. 괄호 없는 같은 복합식·단일 조건을 감싼 괄호는 exit 0으로 처리한다. malformed marker와 닫히지 않은 괄호 음성 사례는 의도대로 2다.
- 유효성 대조: 같은 원문을 양 OS의 `pip._vendor.packaging.requirements.Requirement`에 전달했으며 네 행 모두 수용했다. Windows pip 26.0.1/packaging 26.0, WSL pip 26.1.2/packaging 26.2다. 파서만 실행했으며 설치·네트워크는 없다. [PyPA dependency specifiers의 marker 문법](https://packaging.python.org/en/latest/specifications/dependency-specifiers/#grammar)도 괄호 marker와 양쪽 피연산자의 문자열·환경 변수 표기를 허용한다(조회 2026-09-07).
- 원인: 전체 marker를 괄호 깊이와 무관하게 and/or로 먼저 분리하므로 각 clause에는 짝 없는 괄호가 남는다. 또 왼쪽을 환경 변수 이름으로만 제한하고 정상 문자열-변수 비교를 거부한다. hash 제거 과정의 shlex 정규화가 따옴표를 제거한다는 기존 경계도 고려해야 한다.
- 영향: 기존에 보고하던 정상 조건부 requirements가 새 형식 검사에서 전체 입력 오류로 바뀐다. 정상 mcp 범위도 BLOCKED 행을 제공하지 못한다. 조용한 성공 우회는 아니지만 report 단계의 정상 입력 호환성이 깨진다.
- 권고: marker의 괄호·따옴표·논리 연산자 구조를 보존해 검증하고, 정상 피연산자 순서를 수용한다. 이 도구에서 marker를 실제 환경에 맞춰 평가할 필요는 없으며, 유효성 검증 뒤 기존 전체 선언 검사 방침을 유지하면 된다. 단순식·복합식·역순 비교·잘못된 식을 같이 시험한다.

## 미실행·최종 판정

NOT_RUN: 이 immutable SHA의 원격 CI, 실제 Poetry lock 재생성·설치, pip install·uv sync, 소비자 원천의 새 전체 대조·변경·빌드·e2e, 태그·Release·registry 게시. 로컬 테스트와 파서 대조를 이러한 외부 gate의 성공으로 세지 않는다.

전체·집중 시험과 validators는 통과했다. B-P2-05는 수정됐으나 B-P1-06의 원 반례가 남았고 새 marker 회귀 B-P2-07을 독립 재현했다. **BLOCK**. 원 심각도와 ID를 보존하며, 두 미해결 finding의 disposition·수정 후보 재검토가 필요하다.
