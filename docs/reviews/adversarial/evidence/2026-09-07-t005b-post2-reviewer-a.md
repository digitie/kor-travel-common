# T-005b 두 번째 수정 후 독립 full 적대적 리뷰 A 원본

- 실행 ID: `T005B-A-PF2-20260907-141506-ca461c4`.
- 최종 판정: **BLOCK**. 이전 A finding 8개 중 7개 FIXED·1개 OPEN, 새 P2 finding 1개다. 누적 9개 중 열린 finding은 P2 2개다.
- 시작: `2026-09-07T14:15:06.1592998+09:00`; 종료: `2026-09-07T14:19:25.8929887+09:00`.
- 실제 candidate: **`ca461c45e000ff24feb5a4bdf4478fefa333db8a`**. 새로 실행한 `git rev-parse ca461c4` 결과와 coordinator의 정정이 일치한다.
- PR base: `796445fadb9b4fa6de2f392d6169f31abdccc0fa`; 수정 delta base: `cdf7ba01ccb585b3c00aec69a734266e33ceb510`.
- 새 detached worktree: `F:/dev/kor-travel-common-wt/review-t005b-a-post2`. `git worktree add --detach <worktree> ca461c4`로 생성했다. 시작·종료 `git rev-parse HEAD`가 candidate와 같고 `git status --porcelain=v1 --untracked-files=all`은 빈 출력이다. WSL Git에서도 SHA·clean을 확인했다.
- 전체 수정 delta 3파일·190행 추가·21행 삭제를 읽었다. 코드·시험·버전 정본의 모든 변경과 누적 A 반례를 검토했다. 상대 원본·finding·판정은 읽거나 요청하지 않았다.
- candidate·소비자·다른 작업자의 파일을 수정하지 않았다. 임시 재현 디렉터리는 자동 정리했고 이 원본만 candidate 밖에 저장한다.

## 전달 요청과 확정 기준

요청 범위는 이전 A-P2-04/A-P2-05/A-P2-07/A-P2-08, requirements marker·괄호·옵션 값·quoted include·wildcard/equality 교집합, malformed URL 출력 비공개, 전체 delta 회귀였다. Windows/WSL 전체·focused tests와 validator·직접 CLI/출력 경로 검증을 수행하고 수정·commit하지 않는 독립 리뷰로 진행했다.

최종 SHA 정정 원문:

> 정정: 위 메시지의 가짜 full SHA는 무시하세요. 실제 candidate는 `ca461c45e000ff24feb5a4bdf4478fefa333db8a`입니다. 새 worktree·모든 검증·원본 보고서에 이 정확 SHA만 사용해 주세요.

## 새 검증 결과

Windows Python 3.14.3과 WSL Ubuntu-26.04의 uv managed Python 3.11.15에서 실행했다. WSL은 `/home/digitie/.local/bin/uv run --no-project --python 3.11 python -B -X utf8`로 실행했다. Git 기반 WSL validator 프로세스에만 `GIT_DIR=/mnt/f/dev/kor-travel-common/.git/worktrees/review-t005b-a-post2`, `GIT_WORK_TREE=/mnt/f/dev/kor-travel-common-wt/review-t005b-a-post2`를 설정했다. 저장소 설정 파일은 바꾸지 않았다.

| 실제 명령·검사 | Windows | WSL |
|---|---|---|
| `python -B -X utf8 -m unittest discover -s tests -p 'test_*.py'` | 160 tests·skip 0, 40.418초, exit 0 | 160 tests·skip 0, 22.740초, exit 0 |
| `python -B -X utf8 -m unittest discover -s tests -p 'test_check_versions.py'` | 65 tests·skip 0, 13.806초, exit 0 | 65 tests·skip 0, 12.492초, exit 0 |
| `python -B -X utf8 tools/validate_document_links.py` | 283문서·2166대상, 오류 0 | 동일 |
| `python -B -X utf8 tools/validate_plan.py` | task 102개, 오류 0 | 동일 |
| `python -B -X utf8 tools/check_spdx.py` | 22파일, 오류 0 | 동일 |
| `python -B -X utf8 tools/scan_secrets.py --all` | 351파일, 발견 0·예외 0 | 동일 |
| `python -B -X utf8 tools/check_prod_redaction.py --all` | 351파일, 발견 0·예외 0 | 동일 |
| `python -B -X utf8 tools/check_versions.py --self-check` | exit 0 | exit 0 |
| 직접 CLI | 이전 58회·새 marker 14회, 합계 **72회** | 같은 72회, 같은 결과 |
| `git diff --check <PR base> HEAD` 및 `git diff --check <delta base> HEAD` | 각각 exit 0 | Windows 결과 사용 |

CLI 공통 명령은 `tools/check_versions.py <임시 루트> --registry <임시 registry.json> --repo app-a --mode report --json <임시 report.json> --no-step-summary`다. registry는 candidate 시험의 `REGISTRY`를 사용했다. Poetry fail 반례 3개는 `--mode fail`, 출력 비공개 2개는 `--markdown <임시 out.md>`와 임시 `GITHUB_STEP_SUMMARY`까지 설정했다. stdout/stderr와 파일을 캡처하여 결과·표식 포함 여부만 출력했다.

추가 14개 marker는 양 OS에서 실제 CLI로 대조하고 Windows pip 26.0.1의 vendored `packaging.requirements.Requirement`로 원문 전체의 문법을 독립 확인했다. 설치·네트워크는 사용하지 않았다.

## 누적 finding disposition

| 원 ID | 원 심각도 | disposition | 새 검증 근거 |
|---|---|---|---|
| A-P1-01 | P1 | **FIXED** | short·long 공백·long equals·compact include 모두 하위 차단 행 유지. missing·cycle·blank는 exit 2 |
| A-P1-02 | P1 | **FIXED** | wildcard 차단 범위 누락, compatible·공백·상한 순서의 원 오탐 모두 재발하지 않음. strict lower·세 부분 compatible 대조 유지 |
| A-P1-03 | P1 | **FIXED** | Poetry 잘못된 port·legacy URL 정수·metadata runtime 정수는 양 OS fail 모드에서도 각각 exit 2 |
| A-P2-04 | P2 | **FIXED** | requirements와 Poetry manifest의 malformed bracket URL은 exit 2. stdout/stderr 표식 없음, JSON·Markdown·step summary는 생성되지 않음. 원 Poetry lock 반례도 일반 입력 오류 |
| A-P2-05 | P2 | **OPEN** | 직전 문구·중첩 괄호·옵션 값 누락은 수정. 그러나 새 marker 검사에서 피연산자 누락·잘못된 RHS가 여전히 fastapi OK로 통과 |
| A-P2-06 | P2 | **FIXED** | 탭 주석·equals/공백 hash·continuation이 정확 핀 OK와 파일 NO_LOCK을 유지. dangling continuation은 exit 2 |
| A-P2-07 | P2 | **FIXED** | 따옴표로 감싼 공백 파일 경로의 short·equals include가 하위 mcp BLOCKED를 정상 보고 |
| A-P2-08 | P2 | **FIXED** | `==2.*,==2.1`·역순·wildcard 중복 모두 유효하게 처리되고 BLOCKED를 보고. 모순되는 정확 핀은 추가 회귀 시험에서 exit 2 |

Poetry 최상위 extras·legacy reference·git subdirectory의 새 허용 범위를 코드와 새 시험에서 확인했다. 기존 잘못된 source/type 검사와 전체 npm·uv 회귀는 유지됐다. 추가 입력 검사를 성공으로 오인하지 않도록 아래 두 문제를 분리한다.

## A-P2-05 잔여 — marker 피연산자 문법을 검증하지 않는다

- 원 심각도 **P2**, disposition **OPEN**.
- 위치: `tools/check_versions.py:579`의 `_strip_requirement_hashes`, 1021행의 clause 정규식, 1056행의 `_valid_requirement_marker`.
- 최소 재현은 `requirements.txt` 한 줄 `fastapi==0.141.1; python_version >=`이다. **양 OS report exit 0·fastapi OK**다. pip Requirement parser는 피연산자 부재로 거부한다.
- 다른 잘못된 marker `python_version >= 3.11`, `python_version >= nonsense`, `python_version >= "3.11" garbage`, `python_version >= >= "3.11"`도 양 OS 모두 exit 0·fastapi OK다. 독립 parser는 모두 거부했다.
- 원인: RHS를 거의 모든 문자열로 인정한다. 특히 RHS가 없는 `>=`는 정규식이 `>` 연산자와 `=` RHS로 재해석한다. 앞 단계의 shlex 분할·재결합이 marker 문자열의 따옴표도 제거하므로 올바른 문자열과 원래 따옴표가 없던 잘못된 피연산자를 구분할 수 없다.
- 영향: 형식 오류를 입력 오류 2로 닫겠다는 계약이 여전히 성립하지 않는다. 설치할 수 없는 요구사항에서 설치본 후보를 OK로 표시한다.
- 권고: hash 옵션을 분리할 때 marker 원문의 따옴표를 보존한다. 연산자와 양 피연산자를 토큰으로 구분해 전체 입력을 소비하고, 알려진 환경 변수 또는 인용 문자열만 피연산자로 허용한다. marker의 참·거짓 평가를 요구하는 finding은 아니다.

## 새 A-P2-09 — 정상적인 marker 그룹·문자열을 거부하는 회귀

- 심각도 **P2**, disposition **OPEN**.
- 위치: `tools/check_versions.py:1063`의 and/or 문자열 분할과 1021행의 왼쪽 피연산자 제한.
- 최소 재현: `requirements.txt`에 `fastapi==0.141.1; (python_version >= "3.11" and python_version < "4")`를 둔다. **양 OS exit 2**다. 같은 비교에서 바깥 괄호를 제거하면 exit 0·fastapi OK다.
- 추가 정상 반례: `python_version >= "3.11" and (sys_platform == "win32" or sys_platform == "linux")`, `"3.11" <= python_version`, `platform_version == "x and y"`, `platform_version == "(value)"`도 모두 exit 2다. pip Requirement parser는 다섯 문법을 모두 허용한다.
- 원인: 괄호 깊이와 인용 문자열을 고려하지 않고 and/or를 먼저 분할하며 환경 변수만 왼쪽에 올 수 있다고 가정한다. marker 값에 있는 괄호도 구문 괄호처럼 처리한다.
- 영향: 이전에는 읽던 정상 플랫폼·Python 조건부 요구사항을 이번 수정부터 검사할 수 없다. 보편적인 괄호 그룹이나 문자열 값 때문에 전체 report가 중단된다.
- 권고: 인용 문자열·괄호 깊이를 보존하는 marker tokenizer와 구문 분석을 사용한다. 논리 연산자는 문자열 밖에서만 나누고 양쪽 피연산자에 환경 변수와 인용 문자열을 허용한다.
- 공식 [PyPA dependency specifier 문법](https://packaging.python.org/en/latest/specifications/dependency-specifiers/#grammar)을 2026-09-07에 조회했다. 문법은 인용 문자열/환경 변수인 양 피연산자, 괄호로 묶은 marker, 문자열 안의 공백·괄호 등을 허용한다. 이 근거는 구문 확인에만 사용했다.

14개 추가 marker 중 정상 입력 8개는 독립 parser가 모두 허용했지만 candidate는 5개를 거부했다. 잘못된 입력 6개는 독립 parser가 모두 거부했지만 candidate는 5개를 허용했다. 따옴표가 끝나지 않은 입력은 candidate도 exit 2로 닫았고, 단순 조건·괄호 없는 conjunction·not in의 정상 대조는 유지됐다.

## 재사용·미실행·판정 범위

- **재사용**: 변경 없는 AGENTS·라우터·resume·task·registry·workflow의 이전 정본 대조. `git diff --quiet <delta base> HEAD -- AGENTS.md docs/README.md docs/resume.md versions.json .github/workflows/docs.yml`이 exit 0이며 상세 task는 변경 목록에 없다. 코드·시험·버전 규약 delta와 누적 반례는 새로 확인했다.
- **NOT_RUN(독립 원격 CI 미조회)**: candidate PR/main/release CI. 양 OS 로컬 160 tests를 CI 성공으로 세지 않는다.
- **NOT_RUN(실제 소비자 실측 없음)**: ktdm·ktc 고정 원천 재대조, 실제 설치·빌드·Poetry/uv 전환. 공통 fixture와 임시 입력만 실행했다.
- **NOT_RUN(범위 밖)**: 전체 pip/Poetry resolver 동등성, consumer write, npm/PyPI 게시, commit·merge·태그·Release 생성.
- 최종 **BLOCK — A-P2-05 OPEN, 새 A-P2-09 OPEN**. 나머지 누적 7개 finding은 FIXED다. 새 marker 문법 변경을 수정한 immutable candidate의 독립 재검토가 필요하다.
