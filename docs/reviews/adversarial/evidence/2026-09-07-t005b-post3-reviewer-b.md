# T-005b post3 독립 적대적 리뷰 B 원본

- 실행 ID: `B-T005B-POST3-20260907-143239-1863721`.
- 최종 판정: **BLOCK**. 이전 B finding 7건은 FIXED. 새 B-P2-08은 OPEN.
- 시작: 2026-09-07T14:32:39.5368249+09:00. 종료 SHA·clean 확인: 2026-09-07T14:39:27.3857500+09:00.
- immutable candidate: `18637212e50bf061b75d4f2749fdb6d62399ff99`.
- 이전 B candidate / delta base: `ca461c45e000ff24feb5a4bdf4478fefa333db8a`.
- T-005b 누적 base: `796445fadb9b4fa6de2f392d6169f31abdccc0fa`.
- tree: `37bc02db57deeb17dc34d77a0c2aa95bca8f52ac`.
- 격리: `F:/dev/kor-travel-common-wt/review-t005b-b-post3`에 새 detached worktree를 생성했다. 시작·종료 HEAD가 candidate와 같고 `git status --porcelain=v1`은 모두 빈 출력이었다.
- 후보·소비자·다른 작업자의 파일·과거 원본을 수정하거나 commit하지 않았다. 임시 시험 입력·산출물은 임시 디렉터리에서 생성·정리했다. 이 원본만 지정 `.git/codex-audit` 경로에 저장한다.
- 이전 B 원본만 기준으로 삼았고 A 및 다른 reviewer 결과는 읽거나 요청하지 않은 상태로 확정했다.

## 전달 요청 원문

> 새 후보를 독립적으로 post3 적대적 리뷰하세요. 검토 대상 정확한 immutable SHA는 `18637212e50bf061b75d4f2749fdb6d62399ff99` (현재 branch HEAD)입니다. 이전 finding의 수정 여부뿐 아니라 marker 파서·URL bracket 검증의 새 경계/회귀를 코드와 문서에서 직접 확인하세요. reviewer A의 결과는 공유하지 않습니다. 시작/종료 SHA, clean 여부, Windows·WSL 시험/validator/CI 및 NOT_RUN을 기록하고 원본을 `.git/codex-audit/2026-09-07-t005b-post3-reviewer-b.md`에 저장한 뒤 최종 PASS/BLOCK과 finding IDs를 보내세요. 코드 수정은 하지 마세요.

## 검토 범위와 재사용

이번 delta는 3파일·236행 추가·37행 삭제다. `tools/check_versions.py`, `tests/test_check_versions.py`, `docs/standards/versions.md`의 전체 변경을 읽었다. 누적 base부터는 13파일·1211행 추가·72행 삭제이며 변경 없는 범위는 이전 B 원본의 코드·정본·고정 Poetry upstream 대조를 재사용했다.

AGENTS·docs/README·resume·versions.json·T-005b 상세 task가 이번 delta에 없음을 직접 확인했다. task는 IN_PROGRESS이며 소비자·게시 완료를 주장하지 않는다. bracket URL 검사는 Poetry와 uv/ref 경로에 같이 들어갔으므로 정상 IPv6·Git 판정 회귀도 새로 실행했다. marker의 인용부호 보존·논리식 분할·비교 검사를 읽고 이전 반례 및 추가 유효·무효 문법을 대조했다.

## 직접 실행한 검증

| 명령·검사 | 실제 결과 |
|---|---|
| Windows `py -3.14 -B -X utf8 -m unittest discover -s tests -p 'test_*.py'` | Python 3.14.3, 162 tests, 37.223초, OK, skip 0 |
| WSL Python 3.11.15, 같은 전체 시험 | 162 tests, 20.633초, OK, skip 0 |
| Windows 같은 명령의 `-p 'test_check_versions.py'` | 67 tests, 14.386초, OK, skip 0 |
| WSL 같은 집중 시험 | 67 tests, 13.586초, OK, skip 0 |
| 양 OS 각각 `tools/validate_document_links.py` | 283문서·2166대상·오류 0 |
| 양 OS 각각 `tools/validate_plan.py` | 102 task·오류 0 |
| 양 OS 각각 `tools/check_spdx.py` | 22파일·오류 0 |
| 양 OS 각각 `tools/check_versions.py --self-check` | exit 0, 레지스트리 자체 검사 통과 |
| `git diff --check 796445fadb9b4fa6de2f392d6169f31abdccc0fa HEAD` | exit 0, 출력 없음 |
| 이전 B 핵심 반례·정상 대조·저장소 fixture 8개, 양 OS | 기존 수정·fixture 판정 유지 |
| Poetry source·metadata·Git 경계 41개, 양 OS | 41/41 기대 일치, 합성 marker 비노출 |
| 기존 uv/Python/ref CLI 32개, 양 OS | 32/32 기대 일치 |
| 이전 port·IPv6 각각 report/fail 출력 경로 4개, 양 OS | 모두 일반 오류 2, stdout·stderr 비노출, JSON·Markdown·summary 미생성 |
| 이전 marker CLI 9개와 packaging parser 대조, 양 OS | 9/9 기대 일치 |
| 추가 bracket URL CLI 10개, 양 OS | 10/10 기대 일치, 합성 marker 비노출 |
| 추가 marker 문법 CLI 18개와 packaging parser 대조, 양 OS | 14개 일치, 4개 B-P2-08 재현 |

집중 67개는 전체 162개에 포함되며 두 OS는 같은 시험을 각각 실행한다. 고유 시험 수를 합산하거나 두 배로 세지 않는다. 직접 CLI 집합도 서로 중첩되는 회귀 사례가 있으므로 고유 사례 총수로 합산하지 않았다.

WSL 명령은 다음 형태다.

```text
wsl.exe --exec bash -lc 'cd /mnt/f/dev/kor-travel-common-wt/review-t005b-b-post3 && /home/digitie/.local/share/uv/python/cpython-3.11-linux-x86_64-gnu/bin/python3.11 -B -X utf8 -m unittest discover -s tests -p "test_*.py"'
```

독립 CLI는 Python stdin 스크립트의 `TemporaryDirectory`에 선언·lock을 만들고 실제 subprocess로 아래 명령을 실행했다. fixture는 후보 파일 바이트를 임시 입력으로 복사했다. 출력 비공개 시험에서는 `--no-step-summary`를 제외하고 임시 `GITHUB_STEP_SUMMARY`와 `--markdown`도 실제 설정했다.

```text
<python> -B -X utf8 tools/check_versions.py <임시 입력 경로> --repo docker-manager --mode <report|fail> --no-step-summary --json <임시 report.json>
```

합성 marker는 문자열을 나눠 생성하고 포함 여부만 출력했다. 실제 비밀·운영 주소·소비자 원문은 시험이나 보고서에 사용하지 않았다.

## 실제 CI 확인

`gh run list --repo digitie/kor-travel-common --commit 18637212e50bf061b75d4f2749fdb6d62399ff99`와 `gh run view 34087168804 --json headSha,conclusion,jobs`를 직접 실행했다.

[PR CI run 34087168804](https://github.com/digitie/kor-travel-common/actions/runs/34087168804)는 head SHA가 candidate와 정확히 같고 success다. secret-scan·docs·tools (windows-2025)·tools (ubuntu-24.04)·check-versions의 5 job이 모두 success이며 각 job의 source SHA 확인 step도 success였다. Windows tools job의 실제 로그에서 162 tests, 21.809초를 추가 확인했다.

처음 전체 jobs JSON 출력은 도구 예산으로 일부 잘려서, jq로 각 job 이름·conclusion·source SHA 확인 step만 재조회해 다섯 job을 확인했다. 잘린 출력을 전체 검토했다고 세지 않았다. CI를 새로 trigger하거나 다른 SHA의 CI를 이 후보의 결과로 세지 않았다.

## 이전 finding disposition

| 원 ID·심각도 | 판정 | 이번 직접 결과 |
|---|---|---|
| B-P1-01 / P1 | FIXED | Poetry 조건별 branch/tag 배열·group·lock 순서 반전에서도 branch FLOATING_REF 유지 |
| B-P1-02 / P1 | FIXED | include 등호·공백형 모두 mcp>=2 BLOCKED·error annotation 유지 |
| B-P1-03 / P1 | FIXED | Python metadata 오류는 2, 낮은 하한은 BELOW_FLOOR, 정상 하한은 OK |
| B-P2-04 / P2 | FIXED | GitHub 외 HTTPS Git의 정상 SHA/tag 수용, branch 차단 유지 |
| B-P2-05 / P2 | FIXED | top extras·legacy reference·git subdirectory 정상 입력 수용 유지 |
| B-P1-06 / P1 | FIXED | 이전 비숫자 port·경로 없는 잘못된 bracket URL 모두 report/fail에서 2, 모든 출력 경로 비노출 |
| B-P2-07 / P2 | FIXED | 괄호 복합식·역순 비교·mcp 조건부 범위의 이전 네 반례가 정상 report·BLOCKED 행으로 복구 |

B-P1-06의 추가 대조는 정상 IPv6 경로·port·userinfo, 잘못된 bracket 값·userinfo·suffix·port·닫는 괄호 누락·중복의 10사례다. 유효한 source는 기존 tag/SHA 규칙대로 통과하고 잘못된 값은 일반 입력 오류로 닫혔다. 문서의 IPv6 허용 범위 밖인 모든 URL 문법을 검증했다고 주장하지 않는다.

기존 npm·uv 회귀는 전체 시험과 uv의 @·%40 branch/tag/rev·복수 SHA·marker 순서·source/group 경계 32개 CLI로 확인했다. 저장소 fixture 판정도 유지됐다.

## B-P2-08 — marker의 인용 문자열·연산자 문법이 PEP 508과 불일치한다

- 심각도: **P2**. Disposition: **OPEN**.
- 위치: `tools/check_versions.py:1222`의 전체 문자열 대괄호 거부, `:1128`·`:1203`의 논리·비교 keyword 대소문자 변환.
- 재현: 다음 각 행을 독립 requirements.txt로 만들고 `--mode report`로 실행한다.

```text
fastapi==0.141.1; platform_release == "6.8 [custom]"
fastapi==0.141.1; platform_release == "["
fastapi==0.141.1; python_version >= "3.11" AND os_name == "posix"
fastapi==0.141.1; os_name IN "posix"
```

- 실제 결과: 첫 두 행은 양 OS의 packaging parser가 수용하는 정상 인용 문자열인데 도구는 exit 2로 전체 report를 중단한다. 뒤 두 행은 양 OS의 packaging parser가 거부하는 잘못된 대문자 keyword인데 도구는 fastapi OK·NO_LOCK 등의 행을 만들고 report exit 0으로 종료한다.
- 유효성 대조: Windows pip 26.0.1의 packaging 26.0, WSL pip 26.1.2의 packaging 26.2에서 같은 원문을 `pip._vendor.packaging.requirements.Requirement`에 전달했다. 파서만 실행했으며 설치·네트워크는 없다. [PyPA marker 문법](https://packaging.python.org/en/latest/specifications/dependency-specifiers/#grammar)의 인용 문자열 문자 집합에는 대괄호가 포함되며 keyword는 소문자다. 이 공식 문법은 직전 B 검토에서 2026-09-07에 직접 조회한 근거를 재사용했다.
- 원인: `_valid_marker_expression`이 인용부호 여부를 확인하기 전에 문자열 전체에서 대괄호를 금지한다. 반대로 keyword를 `lower()`로 비교하므로 문법상 다른 token인 대문자를 수용한다.
- 영향: 문서가 약속하는 인용 문자열 조합의 정상 requirements를 report할 수 없고, 일부 잘못된 marker는 명시한 입력 오류 2를 회피한다. 이 report exit 0은 모드 계약상 결과이며 실제 설치 가능성을 뜻하지 않지만, 잘못된 입력을 오류로 닫는 새 계약과 충돌한다.
- 정상 음성 대조: 문자열 안의 괄호·and, 역순 비교, 중첩식, 빈 문자열은 검사한 사례에서 정상 처리됐다. RHS 누락·bare RHS·중복 operator·중복/미완료 논리식·미지 변수는 올바르게 오류 2였다. 기존 B-P2-07의 수정도 유지된다.
- 권고: 인용 문자열 내부의 문자는 그대로 검증하고 구조 token과 구별한다. 논리·비교 keyword는 문법에 맞춰 정확하게 비교한다. 위 네 경계와 기존 괄호·역순·잘못된 RHS 시험을 함께 보존한다. 새 resolver나 marker의 환경별 평가를 도입할 필요는 없다.

## 미실행과 최종 판정

NOT_RUN: 이 검토에서 CI 새 실행·release push CI·main merge 후 CI, 실제 Poetry lock 생성/설치, pip install·uv sync, 소비자 원천의 새 전체 대조·수정·빌드·e2e, 태그·Release·registry 게시. 이미 존재하는 candidate PR CI는 위와 같이 직접 확인했으므로 미실행 CI 전체와 혼동하지 않는다.

기존 B finding 7건은 수정됐고 로컬 전체·집중 시험, validators, 실제 PR CI는 통과했다. 추가 marker 경계에서 새 P2 한 건을 직접 재현했다. **BLOCK**: B-P2-08의 disposition과 수정 후보 재검토가 필요하다.
