# T-005b 세 번째 수정 후 독립 full 적대적 리뷰 A 원본

- 실행 ID: `T005B-A-PF3-20260907-143240-1863721`.
- 최종 판정: **BLOCK**. 누적 A finding 9개 중 7개 FIXED·2개 OPEN이다. 새 ID는 없으며 A-P2-05와 A-P2-09의 원 반례 수정과 잔여 경계를 구분한다.
- 시작: `2026-09-07T14:32:40.9299294+09:00`; 검증 종료: `2026-09-07T14:40:12.1360610+09:00`.
- 실제 immutable candidate: **`18637212e50bf061b75d4f2749fdb6d62399ff99`**.
- PR base: `796445fadb9b4fa6de2f392d6169f31abdccc0fa`; 수정 delta base: `ca461c45e000ff24feb5a4bdf4478fefa333db8a`.
- 격리 detached worktree: `F:/dev/kor-travel-common-wt/review-t005b-a-post3`. 정정된 candidate로 생성했다. 시작·종료 `git rev-parse HEAD`가 위 SHA와 일치했고 `git status --porcelain=v1 --untracked-files=all`은 빈 출력이었다. WSL Git에서도 동일 SHA·clean을 확인하고 종료 시 clean을 재확인했다.
- 전체 수정 delta는 3파일·236행 추가·37행 삭제다. 코드·시험·버전 정본의 모든 변경을 직접 읽고 누적 A 반례와 새 marker·URL 경계를 검토했다. 상대 리뷰 결과는 읽거나 요청하지 않았다.
- candidate·소비자·다른 작업자의 파일을 수정하지 않았다. 재현은 자동 정리되는 임시 입력 디렉터리에서만 실행했다. 이 원본은 candidate 밖의 지정 경로에 저장한다.

## 전달 요청과 확정 기준

요청 범위는 이전 finding의 수정 여부, marker 파서·URL bracket 검증의 새 경계와 회귀, 코드·문서 대조, Windows·WSL 시험·validator·CI 확인이다. 수정·commit 없이 독립 원본과 PASS/BLOCK을 제출하도록 요청받았다.

최종 SHA 정정 원문:

> 정정: 위 메시지의 SHA 오기는 무시하세요. 실제 `git rev-parse HEAD`는 `18637212e50bf061b75d4f2749fdb6d62399ff99`입니다. 이 정확한 SHA만 post3 기준으로 사용하세요.

## 실제 검증 결과

Windows Python 3.14.3과 WSL Ubuntu-26.04의 uv managed Python 3.11.15에서 실행했다. WSL Python 명령 접두사는 `/home/digitie/.local/bin/uv run --no-project --python 3.11 python -B -X utf8`다. Git 기반 WSL validator 프로세스에만 `GIT_DIR=/mnt/f/dev/kor-travel-common/.git/worktrees/review-t005b-a-post3`, `GIT_WORK_TREE=/mnt/f/dev/kor-travel-common-wt/review-t005b-a-post3`를 설정했다. 저장소 설정은 바꾸지 않았다.

| 실제 명령·검사 | Windows | WSL |
|---|---|---|
| `python -B -X utf8 -m unittest discover -s tests -p 'test_*.py'` | 162 tests·skip 0, 39.664초, exit 0 | 162 tests·skip 0, 23.090초, exit 0 |
| `python -B -X utf8 -m unittest discover -s tests -p 'test_check_versions.py'` | 67 tests·skip 0, 14.830초, exit 0 | 67 tests·skip 0, 12.715초, exit 0 |
| `python -B -X utf8 tools/validate_document_links.py` | 283문서·2166대상, 오류 0 | 동일 |
| `python -B -X utf8 tools/validate_plan.py` | task 102개, 오류 0 | 동일 |
| `python -B -X utf8 tools/check_spdx.py` | 22파일, 오류 0 | 동일 |
| `python -B -X utf8 tools/scan_secrets.py --all` | 351파일, 발견 0·예외 0 | 동일 |
| `python -B -X utf8 tools/check_prod_redaction.py --all` | 351파일, 발견 0·예외 0 | 동일 |
| `python -B -X utf8 tools/check_versions.py --self-check` | exit 0 | exit 0 |
| 직접 CLI 118회 | 아래 잔여 marker 7개 외 기대 결과 일치 | 같은 118회·같은 결과 |
| `git diff --check <PR base> HEAD`, `git diff --check <delta base> HEAD` | 각각 exit 0 | Windows 결과 사용 |

CLI 공통 명령은 `python -B -X utf8 tools/check_versions.py <임시 루트> --registry <임시 registry.json> --repo app-a --mode report --json <임시 report.json> --no-step-summary`다. registry는 candidate 시험의 `REGISTRY`를 사용했다. Poetry 입력 오류 3개는 `--mode fail`로 실행했다. 출력 비공개 2개는 `--markdown <임시 out.md>`와 임시 `GITHUB_STEP_SUMMARY`도 설정했다. stdout/stderr와 산출물을 캡처하고 표식 포함 여부만 출력했다.

118회 구성은 이전 일반 반례 53회·직전 marker 14회·이번 marker 10회·이번 URL 행렬 36회·출력 비공개 2회·Poetry fail 모드 3회다. 원본의 평문 시험 비밀·사설 IP 출력 없이 합성 문자열을 분할 생성했다.

### CI 직접 확인

`gh run list --commit <candidate> --json databaseId,headSha,event,status,conclusion,url` 및 `gh run view 34087168804 --json headSha,event,status,conclusion,url,jobs`로 [PR CI 34087168804](https://github.com/digitie/kor-travel-common/actions/runs/34087168804)를 직접 조회했다. event는 `pull_request`, run HEAD는 정확한 candidate, status는 completed, conclusion은 success였다. 아래 5개 job이 각각 success임을 확인했다.

- secret-scan: job 101633311110.
- docs: job 101633311291.
- tools (windows-2025): job 101633311312.
- tools (ubuntu-24.04): job 101633311341.
- check-versions: job 101633311683.

CI job 로그는 읽지 않았다. 위 로컬 test 건수·시간을 CI 실행 건수·시간으로 대체하지 않았다.

## 누적 finding disposition

| 원 ID | 원 심각도 | disposition | 이번 근거 |
|---|---|---|---|
| A-P1-01 | P1 | **FIXED** | short·long 공백·long equals·compact include에서 하위 차단 행 유지. missing·cycle·blank는 exit 2 |
| A-P1-02 | P1 | **FIXED** | wildcard 차단 범위, compatible·공백·상한 순서·strict lower의 기존 반례 모두 기대 판정 유지 |
| A-P1-03 | P1 | **FIXED** | Poetry 잘못된 port·legacy URL 정수·metadata runtime 정수는 양 OS fail 모드에서도 각각 exit 2 |
| A-P2-04 | P2 | **FIXED** | requirements·Poetry malformed bracket URL은 exit 2. stdout/stderr 표식 없음, JSON·Markdown·step summary 미생성. 새 URL 36개 대조도 일치 |
| A-P2-05 | P2 | **OPEN** | 직전 RHS 누락·무인용·garbage·중복 연산자 반례는 모두 exit 2로 수정됐다. 대문자 논리·멤버십 연산자 4개는 여전히 잘못 통과 |
| A-P2-06 | P2 | **FIXED** | 탭 주석·equals/공백 hash·continuation의 정확 핀 OK와 파일 NO_LOCK 유지. dangling continuation exit 2 |
| A-P2-07 | P2 | **FIXED** | 공백 파일 경로를 따옴표로 감싼 short·equals include에서 하위 mcp BLOCKED 유지 |
| A-P2-08 | P2 | **FIXED** | wildcard/exact 교집합·역순·중복 모두 정상 처리. 모순 exact 핀 exit 2 |
| A-P2-09 | P2 | **OPEN** | 직전 괄호 그룹·역순 비교·인용 문자열의 and/괄호 반례는 모두 정상 처리됐다. 정상적인 대괄호 문자열·같은 종류 피연산자의 비교 3개는 여전히 거부 |

수정된 URL 코드는 공통 `_parse_url`에서 netloc 대괄호와 host를 확인하고 파싱 예외를 일반 오류로 바꾼다. requirements·Poetry·uv 각각에 12개 URL을 넣은 총 36회 행렬은 두 OS에서 모두 기대 결과였다. 정상 IPv6·port·userinfo·DNS 대조는 허용했고, 잘못된 prefix/suffix·추가 bracket·empty/nested bracket·userinfo bracket·IPv4 bracket·잘못된 port는 exit 2였다. 기존 npm·uv 전체 회귀 시험도 유지됐다.

## A-P2-05 잔여 — 대소문자를 구분해야 하는 marker 연산자를 잘못 허용한다

- 원 심각도 **P2**, disposition **OPEN**.
- 위치: `tools/check_versions.py:1128`의 `_split_marker_top`, `tools/check_versions.py:1203`의 `_marker_comparison`. 입력 오류 계약은 `docs/standards/versions.md:46`.
- 최소 재현은 requirements 한 줄 `fastapi==0.141.1; python_version >= "3.11" AND python_version < "4"`다. **Windows·WSL 모두 report exit 0·fastapi OK**다.
- `OR`, `sys_platform IN "win32,linux"`, `sys_platform NOT IN "win32,linux"`도 같은 잘못된 허용 결과다. Windows pip 26.0.1의 vendored `packaging.requirements.Requirement`는 네 원문을 모두 거부했다.
- 원인: 논리 keyword와 membership operator를 비교할 때 입력에 `.lower()`를 적용한다. 표준 문법은 소문자 연산자만 허용한다.
- 영향: 설치 도구가 거부하는 요구사항 파일을 이 검사기는 정상 핀 OK로 표시한다. 잘못된 연산자를 입력 오류 2로 닫겠다는 현재 계약이 성립하지 않는다.
- 권고: 문법 keyword를 대소문자 그대로 비교하고, 소문자 정상 대조와 대문자·혼합 대문자 실패 대조를 함께 보존한다. marker의 참·거짓 평가를 요구하는 finding은 아니다.

## A-P2-09 잔여 — 정상 문자열·피연산자 조합을 임의로 거부한다

- 원 심각도 **P2**, disposition **OPEN**.
- 위치: `tools/check_versions.py:1222`의 marker 전체 대괄호 금지, `tools/check_versions.py:1213`의 같은 피연산자 종류 거부.
- 최소 재현은 requirements 한 줄 `fastapi==0.141.1; platform_version == "[value]"`다. **Windows·WSL 모두 exit 2**다.
- 추가 정상 반례 `"linux" == "linux"`와 `python_version <= python_full_version`도 두 OS에서 exit 2다. pip Requirement parser는 세 원문을 모두 허용했다.
- 원인: 인용 문자열 안의 대괄호까지 구문 오류로 취급하며, 양쪽이 모두 인용 문자열이거나 모두 알려진 변수면 거부한다. 표준 marker 문법의 양 피연산자는 각각 환경 변수 또는 인용 문자열이며, 한쪽을 다른 종류로 강제하지 않는다.
- 영향: 정상 요구사항을 읽지 못해 전체 검사 report가 중단된다. 대괄호를 포함한 실제 platform 문자열이나 합법적인 비교 조합에 오탐이 발생한다.
- 권고: 인용 문자열 내부 문자를 marker 구문 문자로 검사하지 않고, 양 피연산자를 각각 검증한다. 두 종류가 달라야 한다는 추가 제약을 제거한다.

[PyPA dependency specifier 문법](https://packaging.python.org/en/latest/specifications/dependency-specifiers/#grammar)을 2026-09-07에 확인한 근거를 재사용했다. 이 문법은 소문자 논리·membership 연산자를 지정하고, 문자열 안의 대괄호와 각 피연산자의 환경 변수/문자열 선택을 허용한다. 이번에는 pip 26.0.1의 Requirement parser로 추가 marker 10개의 전체 원문을 새로 확인했다. 위 7개에서만 candidate와 표준 파서의 문법 허용 여부가 달랐다. 빈 인용 문자열·문자열 안의 대문자 keyword는 정상 허용됐고, 끝의 논리 연산자 누락 입력은 정상 거부됐다.

## 재사용·미실행·판정 범위

- **재사용**: 변경 없는 AGENTS·문서 라우터·resume·상세 task·registry·workflow의 이전 정본 검토. `git diff --quiet <delta base> HEAD -- AGENTS.md docs/README.md docs/resume.md docs/tasks/T-005b-check-versions-poetry-requirements.md versions.json .github/workflows/docs.yml`은 exit 0이다. 코드·시험·버전 규약 delta 및 누적 직접 반례는 이번에 새로 검토했다.
- **NOT_RUN(원격 범위 제한)**: candidate main/release CI 및 CI job 내부 로그·시험 건수 확인. PR run·5개 job의 HEAD/결론은 위와 같이 직접 확인했다.
- **NOT_RUN(실제 소비자 실측 없음)**: ktdm·ktc 고정 원천 재대조, 실제 소비자 설치·빌드·Poetry/uv 전환. common fixture와 임시 입력만 사용했다.
- **NOT_RUN(범위 밖)**: 전체 pip/Poetry resolver 동등성, consumer write, npm/PyPI 게시, commit·merge·태그·Release 생성.
- 최종 **BLOCK — A-P2-05 OPEN, A-P2-09 OPEN**. 직전 marker 반례의 수정은 확인했지만 새 경계에서 같은 문법 계약의 잔여 문제가 재현됐다. 나머지 누적 7개 finding은 FIXED다.
