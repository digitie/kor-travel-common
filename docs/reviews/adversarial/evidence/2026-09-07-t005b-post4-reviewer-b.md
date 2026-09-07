# T-005b post4 독립 적대적 리뷰 B 원본

- 실행 ID: `B-T005B-POST4-20260907-144350-5b68758`.
- 최종 판정: **PASS**. 기존 B finding 8건 모두 FIXED. 이번 검토 범위에서 새 finding 없음.
- 시작: 2026-09-07T14:43:50.1399637+09:00. 종료 SHA·clean 확인: 2026-09-07T14:48:30.7230836+09:00.
- immutable candidate: `5b687585cddf6e7a5145911e75647a0e814d9078`.
- 이전 B candidate / delta base: `18637212e50bf061b75d4f2749fdb6d62399ff99`.
- T-005b 누적 base: `796445fadb9b4fa6de2f392d6169f31abdccc0fa`.
- tree: `182e772dff7262b72afb3d810bfd1156e92ae8ba`.
- 격리: `F:/dev/kor-travel-common-wt/review-t005b-b-post4`에 candidate로 새 detached worktree를 생성했다. 직접 확인한 시작·종료 HEAD가 candidate와 같고 `git status --porcelain=v1`은 모두 빈 출력이었다.
- 후보·소비자·다른 작업자의 파일·과거 원본은 수정하거나 commit하지 않았다. 임시 시험 입력·산출물은 임시 디렉터리에서 생성·정리했다. 이 원본만 지정 `.git/codex-audit` 경로에 저장한다.
- 이전 B 원본을 기준으로 삼았고 A 및 다른 reviewer 결과는 읽거나 요청하지 않은 상태로 확정했다.

## 전달 요청 원문

> post3의 B-P2-08을 수정한 새 후보를 독립적으로 post4 적대적 리뷰하세요. 정확한 immutable SHA는 `5b687585cddf6e7a5145911e75647a0e814d9078`입니다. marker 인용 문자열 대괄호, 소문자 and/or/in/not in, 값/값·변수/변수 비교, 기존 모든 finding과 URL/Poetry/requirements 경계를 다시 공격하세요. reviewer A 결과는 공유하지 않습니다. Windows·WSL 전체/focused 시험, 관련 validators, exact CI/clean SHA/NOT_RUN을 기록하고 원본을 `.git/codex-audit/2026-09-07-t005b-post4-reviewer-b.md`에 저장해 PASS/BLOCK을 보내세요. 코드 수정은 하지 마세요.

## 범위와 재사용

이번 delta는 `tools/check_versions.py`와 `tests/test_check_versions.py`의 2파일·12행 추가·5행 삭제다. 전체 diff를 읽고 네 코드 변경의 문맥을 확인했다. 인용 문자열 안의 대괄호를 구조 오류로 보던 전역 검사를 제거하고, 논리·비교 keyword를 정확한 소문자로 비교하며, 값/값·변수/변수 비교를 구문상 수용한다.

누적 base부터는 13파일·1218행 추가·72행 삭제다. 변경 없는 코드·문서·Poetry upstream 대조는 앞선 B 원본의 검토를 재사용했다. 이번 delta에는 정본·resume·task 변경이 없다. 새 구현은 현재 버전 정본의 인용 문자열·비교·and/or 계약과 검사한 범위에서 일치한다. marker는 구문을 확인한 뒤 선언을 검사하며 환경에 따라 의존성을 선택하거나 실제 설치 가능성을 확정하는 resolver가 아니다.

## 직접 실행한 검증

| 명령·검사 | 실제 결과 |
|---|---|
| Windows `py -3.14 -B -X utf8 -m unittest discover -s tests -p 'test_*.py'` | Python 3.14.3, 162 tests, 41.847초, OK, skip 0 |
| WSL Python 3.11.15, 같은 전체 시험 | 162 tests, 21.860초, OK, skip 0 |
| Windows 같은 명령의 `-p 'test_check_versions.py'` | 67 tests, 16.743초, OK, skip 0 |
| WSL 같은 집중 시험 | 67 tests, 16.066초, OK, skip 0 |
| 양 OS 각각 `tools/validate_document_links.py` | 283문서·2166대상·오류 0 |
| 양 OS 각각 `tools/validate_plan.py` | 102 task·오류 0 |
| 양 OS 각각 `tools/check_spdx.py` | 22파일·오류 0 |
| 양 OS 각각 `tools/check_versions.py --self-check` | exit 0, 레지스트리 자체 검사 통과 |
| `git diff --check 796445fadb9b4fa6de2f392d6169f31abdccc0fa HEAD` | exit 0, 출력 없음 |
| 이전 B 핵심 반례·정상 대조·저장소 fixture 8개, 양 OS | 기존 수정·fixture 판정 유지 |
| Poetry source·metadata·Git 경계 41개, 양 OS | 41/41 기대 일치, 합성 marker 비노출 |
| 기존 uv/Python/ref CLI 32개, 양 OS | 32/32 기대 일치 |
| 이전 port·IPv6 각각 report/fail 출력 경로 4개, 양 OS | 모두 일반 오류 2, stdout·stderr 비노출, JSON·Markdown·summary 미생성 |
| 이전 괄호·역순 marker CLI 9개, 양 OS | 9/9 기대 일치 |
| post3 marker 문법 경계 CLI 18개, 양 OS | 18/18 기대 일치. B-P2-08 네 반례 수정 |
| bracket URL CLI 10개, 양 OS | 10/10 기대 일치, 합성 marker 비노출 |
| 이번 비교 피연산자·keyword·리터럴 추가 CLI 17개, 양 OS | 17/17 기대 일치, packaging parser와 일치 |

집중 67개는 전체 162개에 포함되며 두 OS는 같은 시험을 각각 실행한다. 직접 CLI 집합도 일부 중첩되므로 고유 사례 총수로 합산하지 않는다.

WSL 명령은 다음 형태다.

```text
wsl.exe --exec bash -lc 'cd /mnt/f/dev/kor-travel-common-wt/review-t005b-b-post4 && /home/digitie/.local/share/uv/python/cpython-3.11-linux-x86_64-gnu/bin/python3.11 -B -X utf8 -m unittest discover -s tests -p "test_*.py"'
```

독립 CLI는 Python stdin 스크립트에서 `TemporaryDirectory`에 선언·lock을 만들고 실제 subprocess로 다음 명령을 실행했다. fixture는 후보 파일 바이트를 임시 입력에 복사했다. 출력 경로 비공개 시험에서는 `--no-step-summary`를 제외하고 임시 `GITHUB_STEP_SUMMARY`와 `--markdown`도 실제 설정했다.

```text
<python> -B -X utf8 tools/check_versions.py <임시 입력 경로> --repo docker-manager --mode <report|fail> --no-step-summary --json <임시 report.json>
```

합성 marker는 문자열을 나눠 생성하고 포함 여부만 출력했다. 실제 비밀·운영 주소·소비자 원문은 사용하지 않았다.

## 실제 CI 확인

`gh run list --repo digitie/kor-travel-common --commit 5b687585cddf6e7a5145911e75647a0e814d9078` 및 `gh run view 34087885355 --json headSha,status,conclusion,jobs`를 직접 실행했다.

[PR CI run 34087885355](https://github.com/digitie/kor-travel-common/actions/runs/34087885355)의 head SHA는 candidate와 정확히 같다. 검토 종료 전에 completed/success를 확인했다. docs·check-versions·secret-scan·tools (windows-2025)·tools (ubuntu-24.04) 다섯 job과 각 job의 source SHA 확인 step이 모두 success다. 다른 SHA의 CI를 이 후보 결과로 세거나 새 CI 실행을 요청하지 않았다. 전체 CI 로그 전수 검토가 아니라 run/job/관련 step의 상태를 확인한 결과다.

## 기존 finding disposition

| 원 ID·심각도 | 판정 | 이번 직접 결과 |
|---|---|---|
| B-P1-01 / P1 | FIXED | Poetry 조건별 branch/tag 배열·group·lock 순서 반전에서도 branch FLOATING_REF 유지 |
| B-P1-02 / P1 | FIXED | include 등호·공백형 모두 mcp>=2 BLOCKED·error annotation 유지 |
| B-P1-03 / P1 | FIXED | Python metadata 오류는 2, 낮은 하한은 BELOW_FLOOR, 정상 하한은 OK |
| B-P2-04 / P2 | FIXED | GitHub 외 HTTPS Git의 정상 SHA/tag 수용·branch 차단 유지 |
| B-P2-05 / P2 | FIXED | top extras·legacy reference·git subdirectory 정상 입력 수용 유지 |
| B-P1-06 / P1 | FIXED | 비숫자 port·잘못된 bracket URL 모두 report/fail에서 2, 모든 출력 경로 비노출 유지 |
| B-P2-07 / P2 | FIXED | 괄호 복합식·역순 비교·조건부 mcp 범위가 report 및 BLOCKED 행으로 유지 |
| B-P2-08 / P2 | FIXED | 정상 인용 문자열의 대괄호 수용, 잘못된 대문자 AND·IN은 입력 오류 2 |

## marker 및 주변 경계의 새 대조

B-P2-08 원 반례인 `platform_release == "6.8 [custom]"`와 `platform_release == "["`는 양 OS에서 정상 report 0이었다. 대문자 AND·IN은 오류 2로 바뀌었다. 소문자 and/or/in/not in과 문자열 안의 대문자 keyword·대괄호는 정상 처리됐다.

추가 17사례에는 다음 대조를 포함했다.

- 값/값: `"3.11" == "3.11"`, `"dev" in "dev,test"`는 구문상 수용.
- 변수/변수: `python_version == os_name`, `os_name not in sys_platform`는 구문상 수용.
- 대문자 OR·NOT IN 및 혼합 대소문자 `not IN`은 오류 2.
- 인용 문자열 `"[and/or]"`와 역순 비교를 연결한 식은 수용.
- 값 대신 list를 둔 `["dev"] == extra`·`extra == ["dev"]`, 비교 연산자 누락·피연산자 누락은 오류 2.

동일 원문을 양 OS의 `pip._vendor.packaging.requirements.Requirement`에 전달해 구문 수용 여부를 대조했다. Windows pip 26.0.1/packaging 26.0, WSL pip 26.1.2/packaging 26.2다. 파서만 실행했으며 설치·네트워크는 없다. [PyPA dependency specifiers의 marker 문법](https://packaging.python.org/en/latest/specifications/dependency-specifiers/#grammar)은 이전 B 검토에서 2026-09-07에 확인한 근거를 재사용했다. 비교가 구문상 유효하다는 결과를 환경별 평가·설치 성공으로 세지 않았다.

정상 IPv6 경로·port·userinfo와 잘못된 bracket 값·userinfo·suffix·port·닫는 괄호 누락·중복의 결과도 유지됐다. npm·uv는 전체 시험 및 @·%40 branch/tag/rev·복수 SHA·marker 순서·source/group 경계 32개 CLI에서 회귀가 없었다.

## 새 finding·미실행·최종 판정

새 finding 없음. 실행한 반례와 전체 delta 검토 범위에서 미해결 B finding은 없다.

NOT_RUN: CI 새 실행·release push CI·main merge 후 CI, 실제 Poetry lock 생성/설치, pip install·uv sync, 소비자 원천의 새 전체 대조·수정·빌드·e2e, 태그·Release·registry 게시. 현재 candidate PR CI는 위와 같이 직접 확인했다. 이러한 외부 gate까지 통과했다고 주장하지 않는다.

**PASS**: immutable candidate의 이번 변경과 누적 B finding 수정은 검토 범위에서 수용한다. 이 판정은 T-005b 도구 리뷰의 결과이며 소비자 이관·배포 완료 판정이 아니다.
