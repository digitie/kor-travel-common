# T-005c 두 번째 수정 후 독립 full 적대적 리뷰 A 원본

- 실행 ID: `T005C-A-PF2-20260907-161732-AE6D257`.
- 최종 판정: **BLOCK**. 누적 A finding 8개 중 **4개 FIXED·4개 OPEN**이다. 열린 finding은 **P1 2개·P2 2개**이며 이번에 새 ID는 만들지 않았다. P0·P3 finding은 없다.
- 시작: `2026-09-07T16:17:32.1725504+09:00`; 검증 종료: `2026-09-07T16:21:23.1178161+09:00`.
- Candidate: **`ae6d25711ac04a03db7b8182bd7ffae4a1b2d852`**.
- Tree: **`800afe7b02fbd179c21c85c3b1037a4b37d53e48`**.
- Parent: `8a662a4a981f20d62c8ab98d9311a610bdb30b5c`; 이전 검토 candidate: `03f2cae9a817da96a0eb28ae6487c721464d202f`.
- 공통 manifest: `.git/codex-audit/2026-09-07-t005c-post2-manifest.md`; 실제 SHA256 **`45abd6dec358012b353f1a7ad71d81c1904a5a5bdf2e7982baa2e4a83576e101`**가 전달값과 일치했다.
- 새 detached worktree: `F:/dev/kor-travel-common-wt/review-t005c-post2-a`. `git worktree add --detach <worktree> <candidate>`로 생성했다. 시작·종료 `git rev-parse HEAD`와 `git rev-parse HEAD^{tree}`가 위 값과 일치하고 `git status --porcelain=v1 --untracked-files=all`은 빈 출력이었다. WSL Git에서도 HEAD·clean을 확인하고 종료 시 clean을 재확인했다.
- Parent 대비 전체 delta는 5파일·155행 추가·23행 삭제다. 코드·시험·versions·상세 task의 모든 변경을 읽었다. 나머지 파일은 과거 공통 manifest의 기록 사본이다. 다른 reviewer 결과와 이전 post-fix 원본 파일은 읽지 않았으며 이미 확보한 자기 A 반례와 새 manifest로 독립 검토했다.
- 후보·소비자·다른 작업자의 파일은 수정하지 않았다. 재현은 candidate 밖의 자동 정리되는 임시 입력에서 실행했고 이 원본만 지정 audit 경로에 저장한다.

## 전달 요청과 검토 범위

정확한 candidate에서 parser quote-start/plain indicator/Unicode, per-job·per-step·with 구조, 유효한 2칸 subset/source lines, 모든 redaction 채널과 이전 A finding을 재현하고 Windows·WSL 전체·focused 시험·validator를 실행하도록 요청받았다.

> 상대 reviewer 결과와 이전 post-fix 원본을 읽지 말고 후보를 수정하지 마세요.

변경 없는 AGENTS·문서 라우터·resume·registry·workflow의 이전 대조를 재사용했다. `git diff --quiet <이전 후보> HEAD -- AGENTS.md docs/README.md docs/resume.md versions.json .github/workflows/docs.yml`은 exit 0이다. 변경된 task·정본과 전체 구현 delta·누적 반례는 이번에 새로 검토했다.

## 새 실행 결과

Windows Python 3.14.3과 WSL Ubuntu-26.04의 uv managed Python 3.11.15에서 실행했다. WSL 명령 접두사는 `/home/digitie/.local/bin/uv run --no-project --python 3.11 python -B -X utf8`다. Git 기반 WSL validator 프로세스에만 `GIT_DIR=/mnt/f/dev/kor-travel-common/.git/worktrees/review-t005c-post2-a`, `GIT_WORK_TREE=/mnt/f/dev/kor-travel-common-wt/review-t005c-post2-a`를 설정했다. 저장소 설정은 바꾸지 않았다.

| 실제 명령·검사 | Windows | WSL |
|---|---|---|
| `python -B -X utf8 -m unittest discover -s tests -p 'test_*.py'` | 176 tests·skip 0, 53.336초, exit 0 | 176 tests·skip 0, 34.498초, exit 0 |
| `python -B -X utf8 -m unittest discover -s tests -p 'test_check_versions.py'` | 81 tests·skip 0, 26.604초, exit 0 | 81 tests·skip 0, 20.775초, exit 0 |
| `python -B -X utf8 tools/validate_document_links.py` | 307문서·2198대상, 오류 0 | 동일 |
| `python -B -X utf8 tools/validate_plan.py` | task 102개, 오류 0 | 동일 |
| `python -B -X utf8 tools/check_spdx.py` | 29파일, 오류 0 | 동일 |
| `python -B -X utf8 tools/scan_secrets.py --all` | 382파일, 발견 0·예외 0 | 동일 |
| `python -B -X utf8 tools/check_prod_redaction.py --all` | 382파일, 발견 0·예외 0 | 동일 |
| `python -B -X utf8 tools/check_versions.py --self-check` | exit 0 | exit 0 |
| 직접 CLI | **90회**, 아래 잔여 finding 재현 | 같은 90회·동일 결과 |
| `git diff --check <parent> HEAD`, `git diff --check <이전 후보> HEAD` | 각각 exit 0 | Windows 결과 사용 |

90회는 최초 A 반례·대조 33회, 첫 post-fix 경계 20회, 이번 경계 24회, fixture/manifest 9회, symlink 3회, root 이름에서 유도한 repo의 비공개 대조 1회다. 공통 CLI는 `python -B -X utf8 tools/check_versions.py <임시 루트> --registry <임시 registry.json> --repo app-a --mode fail --json <임시 out.json> --markdown <임시 out.md>`이고 임시 `GITHUB_STEP_SUMMARY`도 설정했다. registry는 candidate 시험의 `REGISTRY`다. fixture는 report 모드, manifest는 report/warn/fail로 실행했다. repo 유도 대조만 `--repo`를 생략했다.

stdout/stderr·JSON·Markdown·summary를 캡처하고 합성값 포함 여부만 출력했다. 비밀·사설 주소 원문은 문자열을 분할 생성했으며 출력하거나 원본에 적지 않았다.

## 누적 finding disposition

| 원 ID | 원 심각도 | disposition | 이번 근거 |
|---|---|---|---|
| A-P1-01 | P1 | **OPEN** | 기존 AWS·단순 password 할당·사설 IPv4·파일명·유도 repo는 비공개 처리. 접두/인용 할당·사설 IPv6·password hash는 네 채널에 노출 |
| A-P1-02 | P1 | **OPEN (재개)** | 원 malformed 4개와 @/backtick은 exit 2. 그러나 새 plain indicator 검사에서 ]bad·}bad·,bad를 fail exit 0·uses OK로 허용 |
| A-P2-03 | P2 | **OPEN** | 원 빈 형제 step/job·step with list는 exit 2. run list/null과 reusable job with list는 여전히 성공 |
| A-P2-04 | P2 | **FIXED (계약 명시)** | task·versions에 2칸 block·trailing separator 없는 flow만 허용한다고 명시. 원 subset 밖 표기는 exit 2, 허용 with-first·flow·행 대조는 정상 |
| A-P2-05 | P2 | **OPEN** | 원 plain 내부 apostrophe·double quote는 수정. 공백 뒤의 quote는 여전히 인용 시작으로 오인해 정상 plain scalar 거부 |
| A-P2-06 | P2 | **FIXED** | 공백 있는 setup-node에서 Node BELOW_FLOOR·fail exit 1 유지 |
| A-P2-07 | P2 | **FIXED** | 원 surrogate와 낮은 surrogate 경계는 양 OS exit 2·traceback 없음·파일 미생성. 허용 인접 Unicode 경계는 정상 |
| A-P2-08 | P2 | **FIXED** | root 밖 local·workflow file·workflow directory symlink가 각각 양 OS exit 2·traceback 없음 |

## A-P1-01 잔여 — 기존 비공개 정책의 일부가 출력 처리에서 누락된다

- 원 심각도 **P1**, disposition **OPEN**.
- 위치: `tools/check_versions.py:1307`의 `_WORKFLOW_SENSITIVE_VALUE_RE`와 1326행 부근 display 처리.
- 최소 재현: `marker = "fixture" + "pw" + "Z" * 12`로 값을 만들고 setup-node의 인용 node-version을 `"DB_PASSWORD=" + marker`로 둔다. **양 OS NO_ENGINES·exit 1이지만 stdout·JSON·Markdown·step summary에 marker가 포함**된다.
- JSON 모양의 인용 key/value 할당문, 분할 생성한 사설 IPv6, 분할 생성한 PBKDF2 형태 문자열도 같은 네 채널로 노출됐다. 실제 payload를 출력하지 않고 bool만 확인했다.
- candidate의 `.secret-scan-patterns`·`.prod-redaction-patterns`를 `tomllib`로 읽어 새 합성값에 `re.search`로 적용했다. 각각 **SECRET-ASSIGNMENT**, **SECRET-ASSIGNMENT/SECRET-QUOTED**, **PRIVATE-IPV6**, **PASSWORD-HASH**가 실제로 일치했다.
- 원인: 새 출력용 regex는 기존 정책의 접두 key·인용 key·IPv6·password hash 범위를 반영하지 않는다.
- 영향: 일부 예시가 가려져도 현재 비공개 정책상 민감한 값이 CI 로그와 artifact에 게시된다.
- 권고: 기존 비공개 정책을 공통 판정 원천으로 사용하거나 적어도 해당 정책 전체에 대한 출력 대조를 추가한다. 개별 발견값만 새 regex에 덧붙이는 방식으로 정책 집합을 따로 유지하지 않는다.

## A-P1-02 잔여 — 예약 indicator 뒤에 문자가 붙으면 malformed YAML을 허용한다

- 원 심각도 **P1**, disposition **OPEN (재개)**.
- 위치: `tools/check_versions.py:1544`.
- 최소 재현: 정상 checkout workflow의 첫 줄을 `name: ]bad`로 바꾼다. **양 OS fail exit 0·uses OK·보고서 생성**이다. `name: }bad`·`name: ,bad`도 같다.
- Windows에 설치된 PyYAML 6.0.3의 `yaml.safe_load`는 세 파일 모두 구문 오류로 거부했다. @/backtick 대조는 candidate도 정상 거부했고, 유효한 `?valid`·`:valid` 대조는 양쪽 모두 허용했다.
- 원인: 무조건 금지해야 하는 첫 문자와 뒤 공백 여부에 따라 허용되는 첫 문자를 한 조건으로 묶었다.
- 영향: manifest가 요구하는 plain indicator 실패 경계가 성립하지 않고 실행할 수 없는 workflow를 정상으로 보고한다.
- 권고: plain scalar의 첫 문자 규칙을 문자별 문법에 맞게 구분하고, 각 indicator의 단독·공백 후속·문자 후속 입력을 대조한다.

## A-P2-03 잔여 — run 값과 reusable job의 with 자료형 검사가 빠졌다

- 원 심각도 **P2**, disposition **OPEN**.
- 위치: `tools/check_versions.py:2165`의 job uses 분기, 2184행의 run key 존재 여부만 검사하는 분기.
- 최소 재현: 정상 checkout step 뒤에 `- run: []`를 추가한다. **양 OS fail exit 0·uses OK 1행**이다. `run: null`도 같은 결과다.
- reusable job에 `uses: owner/repo/.github/workflows/ci.yml@v4`와 `with: []`를 두면 **양 OS fail exit 0·uses OK**다. step with의 map 검사를 reusable job에는 적용하지 않는다.
- 영향: malformed 형제 구조를 key 존재나 정상 uses 하나로 가릴 수 있어 per-job/per-step/with 수용 기준이 닫히지 않는다.
- 권고: run의 지원 scalar/빈 값 계약과 reusable with map을 검증하고, job/step 양쪽에서 동일한 입력 구조 원칙을 적용한다.

## A-P2-05 잔여 — 공백 뒤 quote도 plain 내용일 수 있다

- 원 심각도 **P2**, disposition **OPEN**.
- 위치: `tools/check_versions.py:1352`의 `_yaml_quote_starts`와 이를 사용하는 comment/pair 분할.
- 최소 재현: 정상 workflow 첫 줄을 `name: a 'b`로 바꾸면 **양 OS exit 2**다. `name: a "b`도 같다. PyYAML은 두 파일을 유효한 plain scalar로 읽었다.
- 원인: quote 바로 앞이 공백이면 인용 시작으로 간주한다. 이미 plain scalar가 시작됐는지 판단하지 않아서 문자 사이 quote만 수정하고 공백 뒤 내용은 놓친다.
- 영향: 허용된 2칸 YAML subset 안에서도 정상 이름·shell 문자열 때문에 전체 보고가 중단된다.
- 권고: 바로 앞 문자 대신 scalar 토큰의 시작/문맥을 추적한다. quoted scalar 시작과 plain scalar 내부 quote를 구분하고 주석을 처리한다.

## 정상 회귀·독립 대조

이번 PyYAML 대조 11개에서 malformed indicator 5개는 모두 거부됐고, question/colon prefix·plain quote·doubled single quote/flow 6개는 모두 허용됐다. candidate의 불일치는 위 A-P1-02와 A-P2-05로 기록했다. [YAML 1.2.2 규격](https://yaml.org/spec/1.2.2/)과 [GitHub workflow 문법](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax)을 2026-09-07에 확인한 근거를 재사용했고, 구문 판정을 실제 workflow 실행으로 세지 않았다.

static fixture는 5 findings·dynamic은 4 findings를 유지했으며 원본 행 번호도 같다. malformed fixture 4개는 각각 격리 실행에서 exit 2였다. manifest 루트 workflow의 이동 참조는 report/warn exit 0·fail exit 1과 동일 FLOATING_REF 행이다. 유도 repo의 민감형 root 이름은 stdout·JSON·Markdown·summary에서 사라졌고, root 밖 symlink 세 종류는 모두 입력 오류 2다.

Docker uppercase·middle port·trailing separator는 FLOATING_REF이며 유효한 registry port 대조는 OK다. Node 정적 하한·동적/list/file·canonical 식별과 Unicode 오류 회귀도 유지됐다. 176개 전체 시험에는 기존 npm/Python parser 회귀가 포함된다.

## 정확한 CI·미실행

`gh run list --commit <candidate> --json databaseId,headSha,event,status,conclusion,url`와 `gh run view 34094677429 --json headSha,event,status,conclusion,url,jobs`로 [PR CI 34094677429](https://github.com/digitie/kor-travel-common/actions/runs/34094677429)를 직접 조회했다. HEAD는 candidate, event는 pull_request, run 결론은 success다. Ubuntu tools(101655493063)·Windows tools(101655493275)·secret-scan(101655493341)·docs(101655493375)·check-versions(101655493450) 5개 job 모두 success였다.

- **NOT_RUN(원격 범위 제한)**: main/release CI와 CI job 내부 로그·시험 건수. 로컬 건수·시간을 CI 실행 증거로 대체하지 않았다.
- **NOT_RUN(범위 밖)**: 실제 소비자 원천·설치·workflow 실행, remote action major·Docker 내용 조회, 전체 YAML/Actions parser 동등성, package build/install/publish.
- **NOT_RUN(권한 범위 밖)**: consumer write, 후보 수정, commit·merge·태그·Release 생성.
- **독립성 때문에 미열람**: 상대 reviewer 결과·이전 post-fix 원본 파일. 다른 reviewer ID의 disposition을 대신 확정하지 않았다.
- 최종 **BLOCK**: A-P1-01·A-P1-02·A-P2-03·A-P2-05 OPEN. A-P2-04·A-P2-06·A-P2-07·A-P2-08은 FIXED다.
