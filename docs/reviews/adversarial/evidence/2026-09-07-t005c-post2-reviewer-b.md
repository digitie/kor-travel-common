# T005c post-fix 02 독립 적대적 리뷰 B 원본

- 실행 ID: T005C-B-POST2-20260907-161727-AE6D257
- 검사 시작: 2026-09-07T16:17:27.9091769+09:00
- 검사 종료: 2026-09-07T16:24:11.0657400+09:00
- Candidate: ae6d25711ac04a03db7b8182bd7ffae4a1b2d852
- Parent: 8a662a4a981f20d62c8ab98d9311a610bdb30b5c
- 시작·종료 tree: 800afe7b02fbd179c21c85c3b1037a4b37d53e48
- 격리 경로: F:/dev/kor-travel-common-wt/review-t005c-post2-b
- 시작·종료 HEAD 모두 candidate 일치, git status --porcelain=v1 출력 없음.
- Manifest: F:/dev/kor-travel-common/.git/codex-audit/2026-09-07-t005c-post2-manifest.md
- Manifest SHA256: 45ABD6DEC358012B353F1A7AD71D81C1904A5A5BDF2E7982BAA2E4A83576E101. 전체를 읽었고 시작·종료 해시 일치.
- 최종 verdict: **BLOCK**. OPEN P1 2건, P2 2건. P0/P3 발견 없음.
- 상대 reviewer 결과와 이전 post-fix raw를 열지 않았다. 이전 B 반례는 전달 컨텍스트와 자체 재현 스크립트에서 다시 실행했다. 후보·소비자·다른 원본 변경 및 commit/push/게시는 하지 않았다.

## 전달 요청 원문

> T005c post-fix 02 독립 재검토를 시작해 주세요. 정확한 candidate SHA ae6d25711ac04a03db7b8182bd7ffae4a1b2d852, parent 8a662a4a981f20d62c8ab98d9311a610bdb30b5c, 공통 manifest F:\dev\kor-travel-common\.git\codex-audit\2026-09-07-t005c-post2-manifest.md, SHA256 45ABD6DEC358012B353F1A7AD71D81C1904A5A5BDF2E7982BAA2E4A83576E101입니다. 새 detached clean worktree F:\dev\kor-travel-common-wt\review-t005c-post2-b에서 exact SHA만 검토하세요. 상대 reviewer 결과와 이전 post-fix 원본을 읽지 말고 후보를 수정하지 마세요. redaction policy parity·repo derivation, local/workflow symlink modes·manifest, Docker reference grammar, docs/registry/CI consistency와 이전 B finding을 독립 재현하고 Windows/WSL 전체·focused tests 및 validators를 실행하세요. raw를 .git/codex-audit/2026-09-07-t005c-post2-reviewer-b.md에 기록하고 시작·종료 SHA/tree/clean·NOT_RUN·verdict·hash를 알려 주세요.

코드 표기를 위한 backtick 외 요청 문구·범위는 그대로 기록했다.

## 범위와 실제 검증

parent 대비 전체 5파일 delta(155 추가/23 삭제)를 직접 확인했다. 코드·시험·versions 규약·T-005c task 및 이전 공통 manifest의 보관 추가다. 역사 manifest는 요청 문서이며 상대 reviewer 결과가 아니다. 코드 전체 변경부와 호출 경로, registry exception 적용, Markdown/JSON/annotation/summary 출력, 원래 workflow 탐색·manifest 통합을 읽었다. 기존 README/resume·versions.json·workflow는 직전 후보 대비 diff가 없음을 확인하여 앞선 정본 확인을 재사용했다. 현재 task의 제한 YAML 범위 정정도 읽었다.

| 실행 | Windows Python 3.14.3 | WSL Python 3.11.15 |
|---|---:|---:|
| unittest 전체 | 176 tests, OK, skip 0 | 176 tests, OK, skip 0 |
| test_check_versions.py focused | 81 tests, OK, skip 0 | 81 tests, OK, skip 0 |
| validate_document_links.py | 307 문서/2198 대상, 오류 0 | 동일 |
| validate_plan.py | 102 task, 오류 0 | 동일 |
| check_spdx.py | 29 파일, 오류 0 | 동일 |
| check_versions.py --self-check | exit 0 | exit 0 |
| scan_secrets.py --all | 382 파일, 발견 0, 예외 0 | 동일 |
| check_prod_redaction.py --all | 382 파일, 발견 0, 예외 0 | 동일 |
| 직접 workflow/정책 CLI | 68개, 아래 판정 확인 | 같은 68개, 판정 동일 |
| 합성 registry 형태 검사 | 5개, 전부 exit 0 | 같은 5개, 전부 exit 0 |

직접 실행은 OS별 총 73 CLI 호출이다. 68개는 이전 55개, registry 정책 대조 4개, Docker/YAML 추가 8개, 네 출력 채널 대조 1개다. registry 자체 검사는 정책 대조 입력의 유효성을 확인하려고 --today 2026-09-01로 추가 실행한 5개다. 실제 정책 판단은 --today 2026-09-07로 고정했다.

~~~text
git worktree add --detach F:/dev/kor-travel-common-wt/review-t005c-post2-b ae6d25711ac04a03db7b8182bd7ffae4a1b2d852
git rev-parse HEAD
git rev-parse 'HEAD^{tree}'
git status --porcelain=v1
git diff --stat 8a662a4a981f20d62c8ab98d9311a610bdb30b5c HEAD
git diff 8a662a4a981f20d62c8ab98d9311a610bdb30b5c HEAD -- tools/check_versions.py tests/test_check_versions.py docs/standards/versions.md docs/tasks/T-005c-workflow-static-report.md docs/reviews/adversarial/evidence/2026-09-07-t005c-post-fix-manifest.md
git diff --check 8a662a4a981f20d62c8ab98d9311a610bdb30b5c HEAD
git diff 03f2cae9a817da96a0eb28ae6487c721464d202f HEAD -- versions.json .github/workflows docs/README.md docs/resume.md
py -3.14 -B -X utf8 -m unittest discover -s tests -p 'test_*.py'
py -3.14 -B -X utf8 -m unittest discover -s tests -p 'test_check_versions.py'
py -3.14 -B -X utf8 tools/validate_document_links.py
py -3.14 -B -X utf8 tools/validate_plan.py
py -3.14 -B -X utf8 tools/check_spdx.py
py -3.14 -B -X utf8 tools/check_versions.py --self-check
py -3.14 -B -X utf8 tools/scan_secrets.py --all
py -3.14 -B -X utf8 tools/check_prod_redaction.py --all
~~~

git diff --check exit 0이며 불변 범위 diff 출력은 없다. WSL은 wsl.exe --exec bash -lc에서 /mnt/f/dev/kor-travel-common-wt/review-t005c-post2-b로 이동하고 /home/digitie/.local/share/uv/python/cpython-3.11-linux-x86_64-gnu/bin/python3.11로 같은 인수를 실행했다. Git을 사용하는 validator에는 Windows 생성 worktree를 읽도록 프로세스 환경만 아래처럼 설정했다.

~~~text
GIT_DIR=/mnt/f/dev/kor-travel-common/.git/worktrees/review-t005c-post2-b
GIT_WORK_TREE=/mnt/f/dev/kor-travel-common-wt/review-t005c-post2-b
~~~

직접 CLI는 TemporaryDirectory 입력만 만들고 각 OS의 sys.executable로 후보 tools/check_versions.py를 호출했다. stdout/stderr를 캡처하고 JSON/Markdown/GITHUB_STEP_SUMMARY를 읽어 판정·marker 포함 여부만 출력했다. 원문 시험 비밀·사설 주소는 분할 문자열로 생성했으며 터미널이나 원본에 완성값을 적지 않았다.

## 원 finding별 disposition

| 원 ID·심각도 | 재판정 | 실제 결과 |
|---|---|---|
| B-P1-01 | 부분 수정, OPEN | 원 URL/Node/사설 IPv4·미등록 root→repo 반례는 비공개. 등록된 repo의 mode_source는 비공개를 우회 |
| B-P1-02 | FIXED 유지 | 외부 workflow 파일/디렉터리 symlink 모두 exit 2, 외부 root를 검사 기준으로 채택하지 않음 |
| B-P1-03 | FIXED 유지 | job-only·run-only·name-only·manifest 빈 범위 모두 exit 2 |
| B-P2-04 | 부분 수정, OPEN | 원 dotdot/빈 image/중복 @/대문자/중간 port/끝 점은 거부. 잘못된 separator·hostname 구조가 여전히 OK |
| B-P2-05 | 부분 수정, OPEN | 원 @/backtick은 exit 2. 다른 금지 첫 indicator 뒤 일반 문자가 붙으면 여전히 정상 승인 |
| B-P2-06 | FIXED | lone surrogate를 uses에 넣은 report/fail·quiet/일반 모두 exit 2, traceback 없음, 출력 artifact 없음 |
| B-P2-07 | FIXED | local symlink 탈출: positional/manifest × report/warn/fail 6가지 모두 exit 2 |

초기 22개 스크립트는 local-escape의 이전 기대값 1과 새 실제값 2를 mismatch로 출력한다. 이는 이번 정본의 명시적 변경에 맞는 수정이며 시험 실패/회귀로 집계하지 않았다. static fixture 행 10/12/14/15/17, dynamic fixture 행 15/17/18/20도 유지된다. 파일명 비밀형 marker와 최초 55개 반례의 비공개 결과는 양 OS에서 일치한다.

## B-P1-01 — 등록 repo의 mode_source가 표시값 정제를 우회

- 원 ID·원 심각도 P1 유지, OPEN.
- 위치: tools/check_versions.py:2725, :2600, :2643.
- 최소 재현: name = 'SYNTH' + 'TOKEN' + 'Z' * 12로 합성 식별자를 만든다. 임시 versions.json은 후보 registry 복사에 consumers[name] = {'enforce': 'fail'}을 추가한다. 정상 setup-node workflow를 임시 root에 둔다. --registry <임시 registry> --repo <name>으로 실행하고 **--mode는 생략**한다.
- 실제: report의 repo와 findings.repo는 비공개지만 mode_source = 'versions.json consumers.' + name + '.enforce'가 원문을 보존한다. stdout, JSON, Markdown, GITHUB_STEP_SUMMARY 네 채널에서 marker 포함을 양 OS에서 확인했다. stderr에는 없다.
- 영향: 레지스트리에서 정책을 선택하는 정상 CLI 경로에서 같은 비밀형 입력을 다시 출력한다. 이전 미등록 root 반례만 고쳐 전체 출력 비공개 계약을 닫을 수 없다.
- 권고: 정책 선택 이유의 표시 문자열도 출력 경계에서 비공개 처리한다. 아래 B-P1-08처럼 정책 매칭 식별자 자체를 바꾸면 안 된다.
- 증거 범위: 기본 registry의 현재 7개 repo가 실제 비밀이라는 주장이 아니다. CLI가 허용하는 유효한 합성 registry와 같은 비밀형 marker로 우회 경로를 재현했다.

## B-P1-08 — 표시용 repo 정제가 만료 예외를 누락해 fail을 OK로 변경

- 신규 P1, OPEN.
- 위치: tools/check_versions.py:1782 및 :1816.
- 원인: Checker.self.repo를 _workflow_display_value 결과로 바꾼 뒤 apply_exception에서 이를 registry.exception의 정책 식별자로 다시 사용한다.
- 최소 재현: 후보 versions.json 복사에 아래 consumer와 exception을 추가한다. 모든 값은 임시 디렉터리에만 쓴다.

~~~python
name = 'SYNTH' + 'TOKEN' + 'Z' * 12
registry['consumers'][name] = {'enforce': 'fail'}
registry['exceptions'] = [{
    'repo': name, 'key': 'node', 'installed': '22.23',
    'reason': '합성 예외 대조', 'until': '2026-09-06',
    'review': 'T-005c 합성 시험',
}]
~~~

workflow는 actions/setup-node@v4와 문자열 node-version: "22.23"이다. 먼저 --registry <임시 registry> --self-check --today 2026-09-01로 형태가 유효함(exit 0)을 확인했다. 실제 검사는 다음과 같다.

~~~text
python -B -X utf8 tools/check_versions.py <temporary-root> --registry <temporary-versions.json> --repo <name> --today 2026-09-07 --json <report.json> --no-step-summary
~~~

- 실제: 양 OS에서 uses OK·node OK, exit 0. 동일 registry/예외/입력의 repo만 fixture-app으로 바꾼 대조군은 node EXEMPT_EXPIRED, exit 1.
- 추가 대조: installed/node-version을 20, until을 2026-09-08로 바꾸면 fixture-app은 EXEMPT/exit 0, 비공개 대상 name은 BELOW_FLOOR/exit 1이다. 따라서 단순 출력 차이가 아니라 정책 적용 자체의 변경이다.
- 영향: 만료 예외의 필수 실패를 숨길 수 있고 유효 예외도 적용되지 않는다. 이 코드 경로는 workflow Node뿐 아니라 기존 npm/Python 축의 예외에도 공유된다. 실제 소비자 npm/Python에서의 발생은 별도로 실행했다고 주장하지 않는다.
- 권고: 원 정책 식별자를 별도 보존하고, Finding/보고서 렌더링용 문자열에서만 비공개 처리한다. 같은 registry의 유효/만료 예외와 표시값에 대한 회귀를 함께 둔다.

## B-P2-04 — Docker separator와 registry hostname 구조의 잔여 정상 승인

- 원 ID·원 심각도 P2 유지, OPEN.
- 위치: tools/check_versions.py:2085–2107.
- 최소 재현: uses를 각각 docker://a..b:1.2, docker://a___b:1.2, docker://reg.-example:5000/app:1.2로 둔다.
- 실제: 세 경우 모두 양 OS의 fail 모드에서 OK/exit 0.
- 대조군: docker://a__b:1.2와 docker://a---b:1.2는 OK/exit 0이며 이들은 허용되는 separator다. registry.example:5000/app:1.2도 기존 재현에서 OK 유지.
- 원인: 현재 [a-z0-9_.-]* 문자 집합은 separator의 길이·조합을 제한하지 않는다. host 문자 집합은 각 DNS label의 앞/뒤 하이픈을 검사하지 않는다.
- 영향: 수정 규약이 약속한 기본 image 이름 유효성과 미지원 입력의 비정상 판정이 충족되지 않는다. 원격 이미지 존재 여부나 전체 Docker 버전 해석 문제가 아니다.
- 권고: 검사 범위에 맞게 registry host/port와 repository를 분리하고 separator 생산 규칙을 검증한다. 점 1개·밑줄 1/2개·하이픈 연속의 허용 관계를 문자 클래스 하나로 합치지 않는다.
- 외부 기준: 이전 검토에서 직접 확인한 [Distribution reference regexp.go의 고정 commit](https://raw.githubusercontent.com/distribution/reference/6ccba5a0d2b78d2aac91d03c37aefa8da0e456c8/regexp.go)을 재사용한다. [Docker image tag 정본](https://docs.docker.com/reference/cli/docker/image/tag/)이 이 형식 정의를 연결한다. 조회일 2026-09-07, 코드/이미지 실행은 NOT_RUN.

## B-P2-05 — comma/닫는 괄호 첫 문자의 예외 범위를 잘못 허용

- 원 ID·원 심각도 P2 유지, OPEN.
- 위치: tools/check_versions.py:1544.
- 최소 재현: 정상 actions/checkout@v4 workflow 앞에 각각 name: ,bad / name: ]bad / name: }bad를 추가한다.
- 실제: 세 경우 모두 양 OS에서 uses OK, fail exit 0. 기대는 일반 입력 오류 exit 2다.
- 원인: ?, :와 함께 comma·닫는 대괄호·닫는 중괄호에도 두 번째 문자가 공백인 경우만 거부하는 조건을 적용한다. 뒤에 일반 문자가 붙으면 금지 indicator가 통과한다.
- 영향: 앞선 @/backtick 두 예는 고쳐졌지만 제한 YAML의 malformed fail-close 계약은 여전히 위반된다.
- 권고: 항상 금지되는 첫 indicator와 뒤의 안전 문자를 조건부 허용하는 -, ?, :를 분리한다. 정상 quote/plain 대조군을 보존한다.
- 근거: [YAML 1.2.2 §7.3.3](https://yaml.org/spec/1.2.2/#733-plain-style), revision 2021-10-01, 2026-09-07 재조회. 첫 indicator의 조건부 예외는 -, ?, :다. 전체 YAML parser 확대 요구가 아니다.

## CI·정본·게이트

~~~text
gh run list --repo digitie/kor-travel-common --commit ae6d25711ac04a03db7b8182bd7ffae4a1b2d852 --json databaseId,headSha,status,conclusion,event,url --limit 5
gh run view 34094677429 --repo digitie/kor-travel-common --json headSha,status,conclusion,jobs
gh pr list --repo digitie/kor-travel-common --head codex/t005c-workflow-static-report --json number,isDraft,headRefOid,baseRefName,state
~~~

[PR CI 34094677429](https://github.com/digitie/kor-travel-common/actions/runs/34094677429)는 exact candidate의 pull_request run, completed/success다. docs·tools(Windows)·tools(Ubuntu)·check-versions·secret-scan 5개 job과 각 source SHA 확인 step 모두 success를 독립 조회했다. 모든 로그를 통독하거나 별도 remote workflow를 실행한 것으로 확대하지 않는다.

[PR #8](https://github.com/digitie/kor-travel-common/pull/8)은 OPEN, draft, base main, head exact candidate다. versions.json·기존 CI 파일은 직전 후보 이후 불변이며 actions.checked를 활성화하지 않았다. GPL 헤더는 수정하지 않았고 SPDX 검사가 통과했다. T-005c는 IN_PROGRESS이며 범위 정정은 2칸 block/trailing separator 없는 flow subset을 명시한다. 현재 도구·CI 성공은 미해결 finding이나 실제 소비자 gate를 닫는 증거가 아니다.

## 미실행·실패한 시도와 한계

- 추가 redaction 정책 대조 묶음은 exec_command가 프로세스 생성 단계에서 Access is denied (os error 5)로 거부해 실행되지 않았다. 축소 묶음도 같은 결과라 해당 비공개 값 시험을 계속 재시도하지 않았다. 이것은 candidate CLI의 exit나 시험 성공이 아니다.
- NOT_RUN: 그 묶음에 포함된 assignment 접두/인용 key/짧은 인용 비밀값, 사설 IPv6, password hash, service endpoint의 직접 CLI 대조 6종. .secret-scan-patterns/.prod-redaction-patterns와 코드의 문자식 차이는 읽었지만 이 6종의 런타임 결과를 주장하지 않는다.
- 별도의 비민감 Docker/YAML 8종은 정상 프로세스로 실행 완료했고 위 finding으로 기록했다. repo-policy 4종과 네 채널 대조 1종도 별도로 실행 완료했다. 거부된 묶음을 실행 건수에 넣지 않았다.
- NOT_RUN: 실제 소비자 CI/workflow/수정, remote action 실행·major 조회, Docker daemon/pull/inspect, package build/install/publish, npm/PyPI 게시. common 임시 합성 입력만 사용했으며 사용자 경계를 유지한다.
- NOT_RUN: exact candidate의 별도 release-push CI. 실제 성공 근거는 위 PR CI다.
- NOT_RUN: 모든 YAML 문법, Windows junction/공유 경로/경쟁 조건, 실제 소비자의 모든 예외 정책 실측. 파일·디렉터리 symlink는 양 OS에서 실제 실행했으며 no-skip이다.
- 기존 전체/focused 시험과 validator, 명시한 직접 CLI는 실행 완료했다. 미실행 정책 대조는 후속 immutable 수정 후보의 회귀에 포함할 수 있다.

최종 판정은 BLOCK이다. B-P1-01/B-P2-04/B-P2-05는 부분 수정이며 B-P1-08은 새 정책 회귀다. B-P1-02/B-P1-03/B-P2-06/B-P2-07은 해당 직접 반례에서 FIXED다.
