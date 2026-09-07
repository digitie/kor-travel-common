# T-005b 네 번째 수정 후 독립 full 적대적 리뷰 A 원본

- 실행 ID: `T005B-A-PF4-20260907-144350-5b68758`.
- 최종 판정: **PASS**. 누적 A finding 9개 모두 FIXED이며 새 finding은 없다. 아래 범위의 독립 검토 결과이고 실제 소비자 설치·배포 성공을 뜻하지 않는다.
- 시작: `2026-09-07T14:43:50.8654708+09:00`; 검증 종료: `2026-09-07T14:46:05.6488523+09:00`.
- 실제 immutable candidate: **`5b687585cddf6e7a5145911e75647a0e814d9078`**.
- PR base: `796445fadb9b4fa6de2f392d6169f31abdccc0fa`; 수정 delta base: `18637212e50bf061b75d4f2749fdb6d62399ff99`.
- 격리 detached worktree: `F:/dev/kor-travel-common-wt/review-t005b-a-post4`. `git worktree add --detach <worktree> <candidate>`로 새로 생성했다. 시작·종료 `git rev-parse HEAD`가 candidate와 일치하고 `git status --porcelain=v1 --untracked-files=all`은 빈 출력이었다. WSL Git에서도 동일 SHA·clean을 확인하고 종료 시 clean을 재확인했다.
- 전체 수정 delta 2파일·12행 추가·5행 삭제를 직접 읽었다. 코드의 marker 처리 4곳과 시험에 추가한 반례를 확인하고 기존 모든 A finding 및 URL·Poetry·requirements 경계를 재현했다. 상대 reviewer 결과는 읽거나 요청하지 않았다.
- candidate·소비자·다른 작업자의 파일은 수정하지 않았다. 임시 입력은 자동 정리되는 별도 디렉터리에 생성했으며 이 원본만 지정된 candidate 밖 경로에 보존한다.

## 전달 요청 원문

> post3의 A-P2-05/A-P2-09를 수정한 새 후보를 독립적으로 post4 적대적 리뷰하세요. 정확한 immutable SHA는 `5b687585cddf6e7a5145911e75647a0e814d9078`입니다. marker 인용 문자열 대괄호, 소문자 and/or/in/not in, 값/값·변수/변수 비교, 기존 모든 finding과 URL/Poetry/requirements 경계를 다시 공격하세요. reviewer B 결과는 공유하지 않습니다. Windows·WSL 전체/focused 시험, 관련 validators, exact CI/clean SHA/NOT_RUN을 기록하고 원본을 `.git/codex-audit/2026-09-07-t005b-post4-reviewer-a.md`에 저장해 PASS/BLOCK을 보내세요. 코드 수정은 하지 마세요.

## 새 검증

Windows Python 3.14.3과 WSL Ubuntu-26.04의 uv managed Python 3.11.15에서 실행했다. WSL 명령 접두사는 `/home/digitie/.local/bin/uv run --no-project --python 3.11 python -B -X utf8`다. Git 기반 WSL validator 프로세스에만 `GIT_DIR=/mnt/f/dev/kor-travel-common/.git/worktrees/review-t005b-a-post4`, `GIT_WORK_TREE=/mnt/f/dev/kor-travel-common-wt/review-t005b-a-post4`를 설정했다. 저장소 설정은 수정하지 않았다.

| 실제 명령·검사 | Windows | WSL |
|---|---|---|
| `python -B -X utf8 -m unittest discover -s tests -p 'test_*.py'` | 162 tests·skip 0, 43.857초, exit 0 | 162 tests·skip 0, 23.741초, exit 0 |
| `python -B -X utf8 -m unittest discover -s tests -p 'test_check_versions.py'` | 67 tests·skip 0, 17.364초, exit 0 | 67 tests·skip 0, 16.050초, exit 0 |
| `python -B -X utf8 tools/validate_document_links.py` | 283문서·2166대상, 오류 0 | 동일 |
| `python -B -X utf8 tools/validate_plan.py` | task 102개, 오류 0 | 동일 |
| `python -B -X utf8 tools/check_spdx.py` | 22파일, 오류 0 | 동일 |
| `python -B -X utf8 tools/scan_secrets.py --all` | 351파일, 발견 0·예외 0 | 동일 |
| `python -B -X utf8 tools/check_prod_redaction.py --all` | 351파일, 발견 0·예외 0 | 동일 |
| `python -B -X utf8 tools/check_versions.py --self-check` | exit 0 | exit 0 |
| 직접 CLI | **126회**, 기존 수정 유지·새 반례 실패 없음 | 같은 126회·같은 결과 |
| `git diff --check <PR base> HEAD`, `git diff --check <delta base> HEAD` | 각각 exit 0 | Windows 결과 사용 |

직접 CLI 공통 명령은 `python -B -X utf8 tools/check_versions.py <임시 루트> --registry <임시 registry.json> --repo app-a --mode report --json <임시 report.json> --no-step-summary`다. registry는 candidate의 시험 `REGISTRY`를 사용했다. Poetry 입력 오류 3회는 `--mode fail`로 실행했고, 출력 비공개 2회는 `--markdown <임시 out.md>`와 임시 `GITHUB_STEP_SUMMARY`를 함께 설정했다. stdout/stderr·JSON·Markdown·summary를 캡처하고 실제 시험 비밀·사설 IP를 출력하지 않았다. 합성 표식과 주소는 문자열을 분할 생성했다.

126회 구성은 누적 일반 반례 53회·기존 marker 24회·추가 marker 8회·URL 36회·출력 비공개 2회·Poetry fail 모드 3회다. 범위 검사의 보수적인 기존 보고 규칙까지 포함해 누적 결과와 대조했으며, 모든 결과를 정밀 resolver 결과와 동일하다고 주장하지 않는다.

## 원 finding별 disposition

| 원 ID | 원 심각도 | disposition | 이번 재현 근거 |
|---|---|---|---|
| A-P1-01 | P1 | **FIXED** | short·long 공백·long equals·compact include에서 하위 mcp BLOCKED 유지. missing·cycle·blank는 exit 2 |
| A-P1-02 | P1 | **FIXED** | wildcard overlap을 놓치지 않음. compatible·공백·상한 순서·strict lower의 원 오탐 재발 없음 |
| A-P1-03 | P1 | **FIXED** | Poetry 잘못된 port·legacy URL 정수·metadata runtime 정수는 양 OS fail 모드에서도 각각 exit 2 |
| A-P2-04 | P2 | **FIXED** | requirements·Poetry malformed bracket URL은 exit 2. stdout/stderr 표식 없음, JSON·Markdown·step summary 미생성. URL 행렬 36회 전부 기대 결과 |
| A-P2-05 | P2 | **FIXED** | 미지원 옵션·누락된 옵션 값·잘못된 requirement/marker는 exit 2. 직전 대문자 AND/OR/IN/NOT IN 및 이번 혼합 대문자도 exit 2 |
| A-P2-06 | P2 | **FIXED** | 탭 주석·equals/공백 hash·continuation의 정확 핀 OK와 파일 NO_LOCK 유지. dangling continuation exit 2 |
| A-P2-07 | P2 | **FIXED** | 공백 파일 경로를 인용한 short·equals include에서 하위 mcp BLOCKED 유지 |
| A-P2-08 | P2 | **FIXED** | wildcard/exact 교집합·역순·중복을 정상 처리. 전체 회귀에서 모순 exact 핀 거부 유지 |
| A-P2-09 | P2 | **FIXED** | 괄호 그룹·역순 비교·인용 문자열의 and/괄호/대괄호를 정상 처리. 값/값·변수/변수 비교도 양 OS exit 0·fastapi OK |

### 두 잔여 finding의 직접 대조

- A-P2-05: `python_version >= "3.11" AND python_version < "4"`, 대문자 `OR`, `sys_platform IN "win32,linux"`, `sys_platform NOT IN "win32,linux"`는 모두 양 OS exit 2다. 추가한 `And`·`Not in`도 거부한다. 소문자 `and/or/in/not in`의 정상 대조는 허용한다.
- A-P2-09: `platform_version == "[value]"`, `"linux" == "linux"`, `python_version <= python_full_version`는 모두 양 OS exit 0·fastapi OK다. 문자열 안의 단독 여는/닫는 대괄호도 허용하며, 문자열 밖의 `[python_version == "3.11"]` 및 배열 RHS는 exit 2다.
- 추가 8개 marker는 Windows pip 26.0.1의 vendored `packaging.requirements.Requirement`로 전체 원문을 새로 확인했다. 유효 4개·무효 4개에서 candidate와 독립 parser의 허용 여부가 일치했다. 여러 공백이 있는 `not   in`과 인용 문자열 안의 keyword·대괄호도 포함했다.
- 코드 검토 결과 `tools/check_versions.py:1128`·1203행은 keyword의 대소문자를 그대로 비교하고, 1213행은 두 피연산자를 각각 검증하며, 1222행은 문자열 내부의 대괄호를 일괄 금지하지 않는다. 변경은 현행 `docs/standards/versions.md:46`의 marker 계약에 맞는다.
- [PyPA dependency specifier 문법](https://packaging.python.org/en/latest/specifications/dependency-specifiers/#grammar)을 2026-09-07에 확인한 근거를 재사용했다. 이번 검토는 문법 수용 여부를 확인했고 marker의 환경별 참·거짓 평가는 요구하지 않았다.

### URL·Poetry·기존 도구 회귀

requirements·Poetry·uv 각각에 URL 12종을 넣은 36회 행렬을 두 OS에서 새로 실행했다. 정상 IPv6·port·userinfo·DNS 대조는 허용했고, 잘못된 prefix/suffix·추가 bracket·empty/nested bracket·userinfo bracket·IPv4 bracket·잘못된 port는 입력 오류 2로 닫았다. 출력 비공개 반례 2회에서는 오류 뒤 보고서 파일이 생성되지 않았다.

Poetry source/type/version/group/metadata 및 requirements 재귀·누락·순환·quoted include·hash·editable·정확 핀/범위 차단·NO_LOCK의 누적 반례에서 새 회귀를 찾지 못했다. 기존 npm·uv 시험을 포함한 162개 전체 시험도 통과했다.

## 정확한 candidate의 원격 CI

`gh run list --commit <candidate> --json databaseId,headSha,event,status,conclusion,url`와 `gh run view 34087885355 --json headSha,event,status,conclusion,url,jobs`로 [PR CI 34087885355](https://github.com/digitie/kor-travel-common/actions/runs/34087885355)를 직접 확인했다. event는 pull_request, HEAD는 **`5b687585cddf6e7a5145911e75647a0e814d9078`**, run은 completed/success였다. 아래 5개 job 모두 success다.

- docs: job 101635334878.
- check-versions: job 101635335024.
- secret-scan: job 101635335064.
- tools (windows-2025): job 101635335094.
- tools (ubuntu-24.04): job 101635335119.

CI job 내부 로그는 읽지 않았다. 로컬 시험 건수·시간을 CI 시험 결과로 대체하지 않았다.

## 재사용·NOT_RUN·판정 범위

- **재사용**: 변경 없는 AGENTS·라우터·resume·상세 task·registry·workflow의 이전 정본 대조와 누적 전체 변경 검토. `git diff --quiet <delta base> HEAD -- AGENTS.md docs/README.md docs/resume.md docs/tasks/T-005b-check-versions-poetry-requirements.md versions.json .github/workflows/docs.yml`은 exit 0이다. 이번 코드·시험 delta와 누적 A 반례는 새로 확인했다.
- **NOT_RUN(원격 범위 제한)**: candidate main/release CI와 CI job 내부 로그·시험 건수. PR run·정확한 HEAD·5개 job의 결론은 직접 확인했다.
- **NOT_RUN(실제 소비자 실측 없음)**: ktdm·ktc 고정 원천 재대조, 실제 소비자 설치·빌드·Poetry/uv 전환. common fixture와 임시 입력만 실행했다.
- **NOT_RUN(범위 밖)**: 전체 pip/Poetry resolver 동등성, consumer write, npm/PyPI 게시, commit·merge·태그·Release 생성.
- 최종 **PASS**. A-P2-05·A-P2-09를 포함한 누적 9개 finding은 FIXED이며 이번 delta와 재현 범위에서 새 finding은 없다.
