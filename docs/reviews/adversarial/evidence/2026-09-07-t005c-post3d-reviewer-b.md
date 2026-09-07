# T005c POST3D 독립 적대적 리뷰 B 원본

- 실행 ID: T005C-B-POST3D-20260907-165523
- 시작: 2026-09-07T16:55:23.2286801+09:00
- 검증 종료: 2026-09-07T16:58:50.9989464+09:00
- Candidate: 5807e535c16310c41c21f9efce87b2113aa17ee5
- Tree: 5f5ce75f627c3b786a96c81532044ce100b30a0c
- Parent: 0f55acc2211718d91ce056b096046054b037d7e4
- 누적 코드 대조 기준: b574f74f41272eae61dc1a5965e43974cf76e196
- 격리 worktree: F:/dev/kor-travel-common-wt/review-t005c-post3d-b
- 시작·종료 HEAD/tree가 모두 위 값과 일치하고 git status --porcelain=v1은 두 시점 모두 빈 출력이다.
- 공통 manifest: F:/dev/kor-travel-common/.git/codex-audit/2026-09-07-t005c-post3d-manifest.md
- Manifest SHA256: D1AB00A0F4462AEEB1F99E14C6E3FA2C36A5BDD7FA28AE23C6B60278F3C8C451. 전체를 읽었고 시작·종료 해시 일치를 확인했다.
- **최종 verdict: PASS**. 이번 범위의 신규 P0/P1/P2/P3 finding 없음. 누적 B 반례 9건은 아래 직접 재현 범위에서 FIXED다.
- 상대 reviewer 결과와 이전 post-fix raw/report를 읽지 않았다. 후보·소비자·기존 원본 수정, commit/push/게시는 하지 않았다. 이 raw만 지정 경로에 작성한다.

## 전달 요청 원문

> POST3D exact final review를 시작하세요. candidate 5807e535c16310c41c21f9efce87b2113aa17ee5, tree 5f5ce75f627c3b786a96c81532044ce100b30a0c, parent 0f55acc2211718d91ce056b096046054b037d7e4, manifest .git/codex-audit/2026-09-07-t005c-post3d-manifest.md, SHA256 D1AB00A0F4462AEEB1F99E14C6E3FA2C36A5BDD7FA28AE23C6B60278F3C8C451. 새 detached clean worktree에서 exact SHA만 검토하고 상대 결과·이전 raw/report를 읽지 마세요. 후보 수정/commit/push 금지. redaction policy parity·registry exception/enforce·Docker Distribution grammar·plain/flow delimiter quote·모든 출력 채널·docs/CI 정합성을 재현하고 전체·focused tests/validators를 Windows/WSL에서 실행하세요. raw .git/codex-audit/2026-09-07-t005c-post3d-reviewer-b.md에 시작/종료 SHA/tree/clean·NOT_RUN·verdict·hash를 기록하세요.

코드 표기용 backtick을 생략하고 요청 내용·범위를 보존했다. 앞서 중단된 후보의 미완료 시험/판정을 이 후보의 성공 건수로 이월하지 않았다.

## 읽은 범위와 검증 명령

누적 변경은 tools/check_versions.py·tests/test_check_versions.py 두 파일, 164 추가/18 삭제다. post-fix 02 이후의 redaction·정책 식별자·run/with 구조·Docker·plain/flow quote 변경과 호출 경로를 직접 읽었고, 이번 parent delta는 mapping colon 선택의 break와 flow 인용 회귀 두 행이다. 이전 raw를 다시 열지 않고 전달 컨텍스트의 B 반례를 새 후보에 재실행했다.

versions.json, .github/workflows, docs/standards/versions.md, T-005c task, docs/README.md, docs/resume.md는 누적 기준 이후 diff가 없음을 확인했다. 이들의 정본 관계·IN_PROGRESS 상태·수용 기준·actions.checked 미활성화에 대한 기존 확인을 재사용했다. 실제 검증은 이번 SHA에서 새로 실행했다.

~~~text
git worktree add --detach F:/dev/kor-travel-common-wt/review-t005c-post3d-b 5807e535c16310c41c21f9efce87b2113aa17ee5
git rev-parse HEAD
git rev-parse 'HEAD^{tree}'
git status --porcelain=v1
git diff --stat b574f74f41272eae61dc1a5965e43974cf76e196 HEAD
git diff 0f55acc2211718d91ce056b096046054b037d7e4 HEAD -- tools/check_versions.py tests/test_check_versions.py
git diff --check b574f74f41272eae61dc1a5965e43974cf76e196 HEAD
git diff b574f74f41272eae61dc1a5965e43974cf76e196 HEAD -- versions.json .github/workflows docs/README.md docs/resume.md docs/standards/versions.md docs/tasks/T-005c-workflow-static-report.md
py -3.14 -B -X utf8 -m unittest discover -s tests -p 'test_*.py'
py -3.14 -B -X utf8 -m unittest discover -s tests -p 'test_check_versions.py'
py -3.14 -B -X utf8 tools/validate_document_links.py
py -3.14 -B -X utf8 tools/validate_plan.py
py -3.14 -B -X utf8 tools/check_spdx.py
py -3.14 -B -X utf8 tools/check_versions.py --self-check
py -3.14 -B -X utf8 tools/scan_secrets.py --all
py -3.14 -B -X utf8 tools/check_prod_redaction.py --all
~~~

WSL은 wsl.exe --exec bash -lc에서 /mnt/f/dev/kor-travel-common-wt/review-t005c-post3d-b로 이동하고 /home/digitie/.local/share/uv/python/cpython-3.11-linux-x86_64-gnu/bin/python3.11로 같은 Python 인수를 실행했다. Git을 사용하는 validator에는 Windows 생성 worktree를 읽도록 프로세스 환경만 설정했다.

~~~text
GIT_DIR=/mnt/f/dev/kor-travel-common/.git/worktrees/review-t005c-post3d-b
GIT_WORK_TREE=/mnt/f/dev/kor-travel-common-wt/review-t005c-post3d-b
~~~

| 검증 | Windows Python 3.14.3 | WSL Python 3.11.15 |
|---|---:|---:|
| 전체 unittest | 179 tests, 60.161초, OK | 179 tests, 37.741초, OK |
| focused unittest | 84 tests, 25.198초, OK | 84 tests, 25.991초, OK |
| 문서 링크 | 311 문서/2202 대상, 오류 0 | 동일 |
| plan | 102 task, 오류 0 | 동일 |
| SPDX | 29 파일, 오류 0 | 동일 |
| registry 자체 검사 | exit 0 | exit 0 |
| secret 전체 검사 | 386 파일, 발견 0, 예외 0 | 동일 |
| prod redaction 전체 검사 | 386 파일, 발견 0, 예외 0 | 동일 |
| 직접 입력 CLI | 95회 | 같은 95회, 결과 일치 |
| 합성 registry 형태 검사 | 5회, exit 0 | 같은 5회, exit 0 |

모든 unittest skip 0. git diff --check exit 0. 두 수정 파일의 GPL-3.0-or-later 및 저작권 헤더도 직접 확인했다.

직접 CLI는 OS별 100회, 합계 200회다. 누적 반례와 중복 회귀 호출을 포함한 실행 횟수이며 고유 fixture 개수나 제품 시험 개수로 표시하지 않는다. 콘솔 결과 행에는 별도 네 채널 검증 요약 1행이 추가돼 OS별 case 행은 96개다. 이를 추가 실행으로 세지 않았다. Python 버전 요약을 제외한 모든 case 결과 객체가 두 OS에서 동일한지도 비교했다.

## 직접 재현과 disposition

기본 CLI는 임시 root와 출력 디렉터리를 사용했다.

~~~text
python -B -X utf8 tools/check_versions.py <temporary-root> --repo docker-manager --mode fail --json <report.json> --markdown <report.md>
GITHUB_STEP_SUMMARY=<temporary-summary.md>
~~~

각 OS의 sys.executable로 실행하고 stdout/stderr·JSON·Markdown·summary를 직접 읽었다. 민감형 시험값은 분할 문자열로 생성했고 완성값 대신 판정·포함 여부만 출력했다. 실제 운영값·자격증명을 사용하지 않았다.

| 원 ID·원 심각도 | Disposition | 이번 후보의 직접 결과 |
|---|---|---|
| B-P1-01 | FIXED | URL userinfo·Node 민감값·사설 주소·workflow 파일명·root에서 파생된 repo·등록 repo의 mode_source에서 marker 노출 0 |
| B-P1-02 | FIXED | 외부 workflow 파일 symlink와 workflows 디렉터리 symlink 모두 읽기 전 exit 2. 외부 root를 기준으로 local action을 승인하지 않음 |
| B-P1-03 | FIXED | job-only, run-only, name-only step, manifest 빈 대조 범위 모두 exit 2 |
| B-P2-04 | FIXED | dotdot remote/빈 image/중복 @/대문자 repository/중간 port/끝 separator/반복 점/밑줄 3개/잘못된 host label은 FLOATING_REF. 유효 tag/digest·registry port·밑줄 2개·연속 하이픈은 OK |
| B-P2-05 | FIXED | @/backtick/comma/닫는 대괄호/닫는 중괄호로 시작하는 잘못된 plain scalar는 exit 2 |
| B-P2-06 | FIXED | lone surrogate의 uses 입력은 report/fail·quiet/일반 모두 exit 2, traceback/출력 artifact 없음 |
| B-P2-07 | FIXED | local symlink 탈출: positional/manifest × report/warn/fail 6경로 모두 exit 2 |
| B-P1-08 | FIXED | 민감형 repo에서도 원 식별자로 예외를 찾음. 유효 예외 EXEMPT/exit 0, 만료 예외 EXEMPT_EXPIRED/exit 1. 비공개 표시와 정책 결과가 분리됨 |
| B-P2-09 | FIXED | 검토 중 전달한 a, 'b / a:'b / a[ 'b plain 문자열 3종이 정상 보존되어 exit 0 |

초기 스크립트는 local-escape에 이전 기대 exit 1을 남겨 mismatch를 출력했지만 실제 exit 2가 현재 명시적 계약의 올바른 값이다. 이 알려진 기대값 변경 외 최초 기대 비교의 불일치는 없었다. 이를 후보 실패나 미실행으로 집계하지 않았다.

정책·redaction 추가 대조:

- prefix가 있는 password assignment, 인용 key, 짧은 인용 값, 사설 IPv6, password hash, 서비스 endpoint 형식을 Node 입력으로 생성했다. 모두 NO_ENGINES/exit 1이고 stdout·stderr·JSON·Markdown·summary에 해당 원문이 없었다. JSON escape로 단순 문자열 검색이 빗나가지 않도록 파싱한 finding 값도 대조했다.
- 이전 후보에서 프로세스 생성 거부로 미실행이었던 6종은 이번에는 독립적인 임시 입력 스크립트로 두 OS에서 모두 실행했다. 과거 NOT_RUN을 그대로 성공으로 바꾼 것이 아니라 이번 명령·결과로 검증했다.
- 원 repo = 'SYNTH' + 'TOKEN' + 'Z' * 12의 합성 registry와 fixture-app 대조군을 사용했다. installed=node 22.23, until=2026-09-06, 실제 today=2026-09-07에서 양쪽 모두 EXEMPT_EXPIRED/exit 1이다. installed=20, until=2026-09-08에서는 양쪽 모두 EXEMPT/exit 0이다.
- 위 합성 registry의 형태는 --self-check --today 2026-09-01로 각각 확인했다. 정책 검사에서 --mode를 생략해 registry enforce=fail 선택과 mode_source 비공개를 함께 검증했다. 네 출력 채널의 marker 포함 결과는 빈 목록이다.

Docker·plain/flow 경계:

- docker://a_b.c:1.2, docker://a__b.c:1.2, docker://a_b.c@sha256: 뒤에 64자리 소문자 hex를 붙인 입력, registry.example/a_b.c:1.2는 모두 OK/exit 0이다.
- Distribution의 repository component와 registry host의 차이는 [고정 regexp.go](https://raw.githubusercontent.com/distribution/reference/6ccba5a0d2b78d2aac91d03c37aefa8da0e456c8/regexp.go), 단일 repository의 처리는 [같은 commit의 normalize.go](https://raw.githubusercontent.com/distribution/reference/6ccba5a0d2b78d2aac91d03c37aefa8da0e456c8/normalize.go)로 확인한 근거를 재사용했다. 조회일 2026-09-07. 이미지를 pull하거나 코드를 벤더링하지 않았다.
- plain 문자열 5종과 flow 인용 4종을 대조했다. matrix: ['a: b', ' #tag'], 같은 double-quoted 형태, plain/quoted 혼합 flow는 exit 0이다. trailing separator가 있는 flow는 현재 제한 subset 계약대로 exit 2다.
- YAML plain/quoted/flow 문맥의 외부 기준은 [YAML 1.2.2 §7.3.3](https://yaml.org/spec/1.2.2/#733-plain-style), revision 2021-10-01, 2026-09-07 조회다. 전체 YAML 구현 적합성을 주장하지 않는다.
- static fixture 원본 행 10/12/14/15/17, dynamic fixture 행 15/17/18/20을 유지한다. malformed fixture 4종은 exit 2. manifest 이동 ref는 report 모드에서 FLOATING_REF 행을 실제 추가하며 빈 manifest workflow는 exit 2다.

## CI와 문서 상태

~~~text
gh run list --repo digitie/kor-travel-common --commit 5807e535c16310c41c21f9efce87b2113aa17ee5 --json databaseId,headSha,status,conclusion,event,url --limit 5
gh run view 34097813843 --repo digitie/kor-travel-common --json headSha,status,conclusion,jobs
gh pr list --repo digitie/kor-travel-common --head codex/t005c-workflow-static-report --json number,isDraft,headRefOid,baseRefName,state
~~~

[PR CI 34097813843](https://github.com/digitie/kor-travel-common/actions/runs/34097813843)는 exact candidate의 pull_request run으로 completed/success다. docs·tools(Windows)·tools(Ubuntu)·check-versions·secret-scan 5개 job 및 각 source SHA 확인 step의 success를 독립 조회했다. 모든 로그를 통독하거나 원격 workflow를 별도로 실행했다고 주장하지 않는다.

[PR #8](https://github.com/digitie/kor-travel-common/pull/8)은 OPEN, draft, base main, head exact candidate다. 문서·registry·CI 파일이 누적 기준 이후 불변임을 확인했고 actions.checked를 활성화하거나 실제 action major를 추정하지 않았다. 이 PASS는 immutable 코드·문법 계약·도구 검증의 결론이며 T-403 소비자 CI나 package/release gate의 완료가 아니다.

## NOT_RUN과 한계

- NOT_RUN: 실제 소비자 workflow/CI/파일 변경. common의 임시 합성 입력만 사용했다.
- NOT_RUN: 원격 action 실행·실제 major 조회, Docker daemon/pull/inspect. 정적 문법·고정 참조만 확인했다.
- NOT_RUN: package build/install/publish, npm/PyPI 게시. 사용자 경계와 task 범위 밖을 유지했다.
- NOT_RUN: exact candidate의 별도 release-push CI. 실제 성공 근거는 위 PR CI다.
- NOT_RUN: 전체 YAML 표준 적합성, 모든 Docker 형식·주소, Windows junction/네트워크 공유/경쟁 조건. 제한 subset의 명시한 정상/음성 입력과 양 OS 파일·디렉터리 symlink를 실제 검증했다.
- 이전 후보의 중단된 실행은 이번 성공 건수에서 제외했다. 이번 요청의 전체/focused tests, validator, 직접 CLI는 새 SHA에서 실행 완료했으며 skip 0이다.

신규 finding은 없으며 최종 verdict는 PASS다. 외부/제품 gate와 위 NOT_RUN 범위를 이 결론에 포함하지 않는다.

