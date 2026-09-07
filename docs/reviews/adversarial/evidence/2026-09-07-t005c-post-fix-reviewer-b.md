# T005c post-fix 독립 적대적 리뷰 B 원본

- 실행 ID: T005C-B-POST-20260907-155255-03f2cae
- 검사 시작: 2026-09-07T15:52:55.7969075+09:00
- 검사 종료: 2026-09-07T16:01:12.6357354+09:00
- Candidate: 03f2cae9a817da96a0eb28ae6487c721464d202f
- Parent: 3ef3fc4f91ba2b6320ba6197176f54917227c31e
- 누적 대조 기준: 5526c018380023afd362bd3993d110ee81c3b10a
- Candidate tree: e5259142a8244d9e755c836ed22f25c87ac5927a
- 격리 경로: F:/dev/kor-travel-common-wt/review-t005c-post-b
- 시작·종료 HEAD 모두 candidate와 일치. 두 시점 모두 git status --porcelain=v1 출력 없음.
- 공통 manifest: F:/dev/kor-travel-common/.git/codex-audit/2026-09-07-t005c-post-fix-manifest.md
- Manifest SHA256: CD1FB434401E1B24DCB2E9D1193719D17F9A757E2BA1F6D3A23774CDC6943920, 시작·종료 재확인 일치.
- 최종 판정: **BLOCK**. 미해결 P1 1건, P2 4건. P0/P3 발견 없음.
- 상대 reviewer 결과와 기존 post-fix 원본은 읽지 않았다. 후보 파일·소비자 저장소를 수정하지 않았고 commit/push/게시하지 않았다. 이 원본만 기본 checkout의 .git/codex-audit에 기록한다.

## 전달 요청 원문

> T005c post-fix 독립 재검토를 시작해 주세요. 정확한 candidate SHA는 03f2cae9a817da96a0eb28ae6487c721464d202f, parent 3ef3fc4f91ba2b6320ba6197176f54917227c31e, 공통 manifest는 F:\dev\kor-travel-common\.git\codex-audit\2026-09-07-t005c-post-fix-manifest.md, SHA256 CD1FB434401E1B24DCB2E9D1193719D17F9A757E2BA1F6D3A23774CDC6943920 입니다. 새 detached clean worktree F:\dev\kor-travel-common-wt\review-t005c-post-b 를 만들고 exact SHA만 검토하세요. 상대 reviewer 결과나 기존 post-fix 원본은 읽지 말고 후보를 수정하지 마세요. symlink/root containment, Docker/remote target validation, stdout/JSON/Markdown/GITHUB_STEP_SUMMARY redaction, manifest integration, docs/registry consistency, CI evidence, Windows/Linux parity를 초기 B findings와 독립적으로 재현하고 전체·focused tests 및 validators를 실행하세요. 원본 결과를 .git/codex-audit/2026-09-07-t005c-post-fix-reviewer-b.md에 기록하고 시작/종료 SHA·clean·NOT_RUN·P0-P3·verdict·hash를 알려 주세요.

## 범위와 실행 증거

parent 대비 3개 파일의 전체 delta(258 추가, 36 삭제)를 직접 읽었다: tools/check_versions.py, tests/test_check_versions.py, docs/standards/versions.md. 최초 candidate 대비 규범·코드 delta도 같은 세 파일이다. 누적 변경 목록에 나온 별도 reviewer 원본·통합 결과는 열지 않았다. 이전 B의 최초 반례를 다시 실행했고 변경 없는 npm/uv/Poetry/requirements 범위는 전체 회귀로 검증했다. docs/README.md·resume·T-005c task와 관련 versions/ci-deploy 절을 대조했다.

Windows Python 3.14.3, WSL Python 3.11.15를 사용했다. 모든 시험에서 skip 0이다.

| 직접 실행 | Windows | WSL |
|---|---:|---:|
| unittest 전체 | 173 tests, 41.074초, OK | 173 tests, 26.324초, OK |
| test_check_versions.py focused | 78 tests, 18.492초, OK | 78 tests, 19.137초, OK |
| validate_document_links.py | 303 문서·2194 대상·오류 0 | 동일 |
| validate_plan.py | 102 task·오류 0 | 동일 |
| check_spdx.py | 29 파일·오류 0 | 동일 |
| check_versions.py --self-check | exit 0 | exit 0 |
| scan_secrets.py --all | 378 파일·발견 0·예외 0 | 동일 |
| check_prod_redaction.py --all | 378 파일·발견 0·예외 0 | 동일 |
| 직접 CLI 반례·대조군 | 55개 호출 | 55개 호출, 판정 동일 |

실행 명령:

~~~text
git worktree add --detach F:/dev/kor-travel-common-wt/review-t005c-post-b 03f2cae9a817da96a0eb28ae6487c721464d202f
git rev-parse HEAD
git rev-parse 'HEAD^{tree}'
git status --porcelain=v1
git diff --stat 3ef3fc4f91ba2b6320ba6197176f54917227c31e HEAD
git diff 3ef3fc4f91ba2b6320ba6197176f54917227c31e HEAD -- tools/check_versions.py tests/test_check_versions.py docs/standards/versions.md
git diff --check 3ef3fc4f91ba2b6320ba6197176f54917227c31e HEAD
git diff --check 5526c018380023afd362bd3993d110ee81c3b10a HEAD
py -3.14 -B -X utf8 -m unittest discover -s tests -p 'test_*.py'
py -3.14 -B -X utf8 -m unittest discover -s tests -p 'test_check_versions.py'
py -3.14 -B -X utf8 tools/validate_document_links.py
py -3.14 -B -X utf8 tools/validate_plan.py
py -3.14 -B -X utf8 tools/check_spdx.py
py -3.14 -B -X utf8 tools/check_versions.py --self-check
py -3.14 -B -X utf8 tools/scan_secrets.py --all
py -3.14 -B -X utf8 tools/check_prod_redaction.py --all
~~~

두 git diff --check 모두 exit 0. WSL은 wsl.exe --exec bash -lc에서 /mnt/f/dev/kor-travel-common-wt/review-t005c-post-b로 이동하고 /home/digitie/.local/share/uv/python/cpython-3.11-linux-x86_64-gnu/bin/python3.11로 같은 Python 인수를 실행했다. Windows가 만든 worktree의 Git 경로를 Linux에서 읽도록 validator 프로세스에만 다음 환경을 명시했다. 후보를 편집하지 않았다.

~~~text
GIT_DIR=/mnt/f/dev/kor-travel-common/.git/worktrees/review-t005c-post-b
GIT_WORK_TREE=/mnt/f/dev/kor-travel-common-wt/review-t005c-post-b
~~~

직접 CLI는 TemporaryDirectory 안의 합성 입력을 사용했다. 기본 호출은 아래와 같다. 각 OS의 sys.executable로 실행하고 stdout/stderr는 capture_output=True, text=True, encoding='utf-8'로 수집했다. 비밀형/사설 주소형 시험값은 분할 문자열로만 생성했고, 콘솔에는 case ID·exit·판정·포함 여부만 출력했다. 실제 운영값·자격증명은 사용하지 않았다.

~~~text
python -B -X utf8 tools/check_versions.py <temporary-root> --repo docker-manager --mode fail --json <temporary-report.json> --markdown <temporary-report.md>
GITHUB_STEP_SUMMARY=<temporary-summary.md>
~~~

55개/OS 구성: 최초 CLI 반례·대조군 22개, symlink 3개, 저장소 fixture/manifest 8개, 추가 경계 13개, local symlink 모드/입력 경로·파일명/Unicode 출력 경계 9개. 최초 22개는 기대 exit와 전부 일치하고 합성 비밀 marker 노출 0이다. static fixture는 원본 행 10/12/14/15/17, dynamic은 15/17/18/20을 유지한다. malformed fixture 4개는 모두 exit 2. manifest-floating은 report 모드에서 FLOATING_REF 행이 생기며 manifest-empty는 exit 2다.

## 최초 finding disposition

| 원 ID·심각도 | 판정 | 직접 확인 |
|---|---|---|
| B-P1-01 | 부분 수정, OPEN | 최초 URL userinfo·Node marker는 모든 출력에서 제거됨. 새 root→repo 경로와 운영 주소형 값이 같은 출력 보호를 우회함 |
| B-P1-02 | FIXED | workflow 파일 symlink와 workflows 디렉터리 symlink의 외부 탈출 모두 양 OS에서 읽기 전 exit 2. 외부 root를 local 기준으로 삼지 않음 |
| B-P1-03 | FIXED | job-only·run-only·name-only step·manifest 빈 대조 범위 모두 exit 2, findings 없음 |
| B-P2-04 | 부분 수정, OPEN | 최초 ../repo@v4·빈 Docker 이름·중복 @는 FLOATING_REF/exit 1. 새 기본 Docker 이름 경계는 여전히 OK |

## B-P1-01 — repo로 전파된 입력 경로 및 운영 주소형 값의 출력 노출

- 위치: tools/check_versions.py:1307, :1320, :2557, :2598, :2680.
- 심각도: P1(원 ID·원 심각도 유지), OPEN.
- 최소 재현 A: marker = 'SYNTH' + 'TOKEN' + 'Z' * 12로 이름을 만든 임시 root 아래 .github/workflows/ci.yml에 정상 actions/checkout@v4만 둔다. 기본 호출에서 --repo를 **생략**한다.
- 실제: exit 0, uses OK. root 자체는 비공개로 바뀌지만 root.name이 repo로 채택되어 stdout 표제, JSON repo/findings.repo, Markdown, GITHUB_STEP_SUMMARY에 marker가 그대로 들어간다. stderr에는 없다.
- 최소 재현 B: private = '10' + '.' + '71' + '.' + '82' + '.' + '93'으로 합성 사설 주소를 만든다. uses를 'docker://' + private + '/app:1.2'로 두면 exit 0/OK이며 네 출력에 주소가 남는다. setup-node의 문자열 node-version으로 두면 BELOW_FLOOR/exit 1이며 역시 네 출력에 남는다.
- 영향: T-005c 수용 기준의 비밀·운영값 비공개와 manifest의 모든 출력 경로 비공개를 충족하지 못한다. 동일 marker가 workflow 파일명일 때는 정상 차단되므로, 현재 개별 필드 정제만으로는 출력 그래프 전체를 보호하지 못하는 구체적 우회다.
- 권고: 정책용 repo 식별자와 표시값을 분리하고, 경로에서 파생된 repo를 포함한 모든 출력 필드에 일관된 정제를 적용한다. 운영 주소형 값도 현재 비공개 요구에 맞게 처리하고 Node 미지원 값은 정상 버전으로 해석하지 않는다. 소비자 예외/정책 매칭 자체를 표시값 정제로 바꾸지 않는다.
- Windows/WSL 동일 재현. 원문 비밀을 출력하지 않고 포함 여부만 판정했다.

## B-P2-04 — 기본 Docker 이름의 잘못된 구조가 계속 OK

- 위치: tools/check_versions.py:2057–2074, 호출 :2031/:2040.
- 심각도: P2(원 ID·원 심각도 유지), OPEN.
- 최소 재현: 정상 steps 아래 uses를 각각 docker://UPPER:1.2, docker://registry.example/path:123/app:1.2, docker://image.:1.2로 설정한다.
- 실제: 세 경우 모두 양 OS에서 uses OK, fail 모드 exit 0. 대조군 docker://registry.example:5000/app:1.2도 정상 OK다.
- 원인: 모든 slash segment를 같은 문자 집합으로 허용하고, 어느 segment에나 host:port 문법을 허용한다. repository 대문자, repository 내부 colon, 끝 separator도 기본 유효 이름으로 통과한다.
- 영향: 실행할 수 없는 기본 image 이름을 정본의 유효한 고정 참조로 승인한다. 전체 Docker 이미지 조회·버전 parser 요구가 아니라 이미 구현한 기본 구조 판정의 결함이다.
- 권고: 첫 registry host/port와 나머지 repository segment를 구분하고 repository의 최소 문법을 검사한다. 지원하지 않는 유효 형식은 미지원으로 보고할 수 있지만 명백히 잘못된 형식을 OK로 만들지 않는다.
- 근거: [Docker image tag 정본](https://docs.docker.com/reference/cli/docker/image/tag/)이 연결하는 [Distribution reference의 고정 regexp.go](https://raw.githubusercontent.com/distribution/reference/6ccba5a0d2b78d2aac91d03c37aefa8da0e456c8/regexp.go)에서 repository는 소문자·숫자를 separator로 잇고 port는 선택적 domain 부분에만 붙는다. 조회일 2026-09-07. Docker 실행/이미지 pull은 하지 않았다.

## B-P2-05 — plain scalar 예약문자를 정상 입력으로 승인

- 위치: tools/check_versions.py:1455–1464, :1518–1538; docs/standards/versions.md:102.
- 심각도: P2, 신규 OPEN.
- 최소 재현: 정상 actions/checkout@v4 workflow 앞에 name: @bad를 추가한다. 별도 경우는 name: 뒤 첫 문자를 chr(96)으로 만든다.
- 실제: 둘 다 uses OK, fail 모드 exit 0. 기대는 입력 오류 exit 2다.
- 영향: 수정 정본이 명시한 plain scalar 예약 문자 처리와 malformed YAML fail-close 계약에 어긋난다. 런너가 읽을 수 없는 workflow가 이 검사에서는 정상 성공한다.
- 권고: quote/flow 처리 뒤 plain scalar의 첫 indicator를 제한하고, 허용되는 plain scalar와 invalid indicator를 별도 회귀로 검증한다.
- 근거: [YAML 1.2.2 §5.3](https://yaml.org/spec/1.2.2/#53-indicator-characters), revision 2021-10-01, 조회일 2026-09-07. 해당 절의 예약 indicator 예제와 직접 대조했다. 전체 YAML 지원 확대 요청이 아니다.

## B-P2-06 — 새 Unicode escape가 보고서 생성 단계에서 traceback 발생

- 위치: tools/check_versions.py:1515, :1320, :2700–2710.
- 심각도: P2, 신규 OPEN.
- 최소 재현: YAML double-quoted uses 문자열을 'actions/checkout@v4' + chr(92) + 'ud800'으로 작성한다. JSON/Markdown/summary 출력 경로를 지정한다.
- 실제: 양 OS에서 UnicodeEncodeError traceback, exit 1. report 모드와 fail 모드, --quiet 유무를 대조해 동일한 실패를 확인했다. 새 출력 파일 세 개 모두 생성되지 않았다.
- 원인: escape 숫자를 chr로 바꾸며 lone surrogate를 내부 문자열에 보존하고, 이를 UTF-8 출력 가능한 문자열로 보장하지 않는다. 출력은 checker.run의 입력 오류 처리 영역 밖이다.
- 영향: 합성 YAML 값 하나로 정해진 일반 입력 오류 2 대신 예외 종료가 발생하고 증거 보고서가 생성되지 않는다. 실제 자격증명 노출이라고 주장하지 않는다.
- 권고: decode 후 Unicode scalar 유효성을 확인해 지원하지 않는 escape는 원문 없는 입력 오류로 닫고 출력 경로에서도 동일 오류 계약을 보장한다. 정상 Unicode escape 대조군을 유지한다.
- [YAML 1.2.2 문자·escape 규정](https://yaml.org/spec/1.2.2/#51-character-set)을 참고했으며, finding의 직접 근거는 실제 CLI의 UTF-8 출력 예외다.

## B-P2-07 — local symlink 탈출의 새 exit 계약과 구현 불일치

- 위치: tools/check_versions.py:2014–2019; docs/standards/versions.md:102, :177.
- 심각도: P2, 신규 OPEN.
- 최소 재현: 임시 root/.github/actions/local을 root의 형제 outside 디렉터리로 symlink하고, 정상 workflow의 uses를 ./.github/actions/local로 둔다.
- 실제: positional과 manifest 입력 모두 report/warn은 NO_LOCK + exit 0, fail은 NO_LOCK + exit 1. 양 OS 동일. manifest는 schema=kor-travel-common.consumer-manifest.v1, repo=docker-manager, lockfiles=[]로 실행했다.
- 기대: 새 정본은 workflow·local 경로가 root 밖으로 symlink되면 입력 오류 2라고 명시한다.
- 영향: 문서에 따라 report 모드에서도 경계 오류가 차단된다고 판단하는 호출자가 실제로는 성공 exit를 받는다. 외부 파일을 읽거나 local action을 OK로 승인한 것은 아니며, 최초 B-P1-02의 읽기 탈출과는 구별한다.
- 권고: local symlink 탈출도 일반 입력 오류로 반환하거나, 의도한 별도 NO_LOCK 정책을 task·정본·manifest에서 명시적으로 일치시킨다. 정본을 조용히 해석해서 완료로 만들지 않는다.

## CI·정본·고지 확인

~~~text
gh run list --repo digitie/kor-travel-common --commit 03f2cae9a817da96a0eb28ae6487c721464d202f --json databaseId,headSha,status,conclusion,event,url --limit 5
gh run view 34092707302 --repo digitie/kor-travel-common --json headSha,status,conclusion,jobs
~~~

[PR CI 34092707302](https://github.com/digitie/kor-travel-common/actions/runs/34092707302)는 exact candidate HEAD, pull_request, completed/success다. docs·tools(windows-2025)·tools(ubuntu-24.04)·check-versions·secret-scan 5개 job과 각 검사 source SHA 확인 step의 success를 독립 조회했다. 이 확인은 원격 job 상태/step 메타데이터 대조이며 모든 로그를 통독했다고 주장하지 않는다.

versions.json과 .github/workflows는 최초 candidate부터 내용 변화가 없다. registry node floor=22.12, actions.checked=false를 직접 읽었다. setup-node 앞뒤 공백과 with가 먼저 오는 list mapping에서도 Node 20이 BELOW_FLOOR로 보고된다. 코드·시험 GPL-3.0-or-later/저작권 헤더를 직접 확인했고 SPDX 검사가 통과했다. 정본의 actions.checked를 실제 major 검증 완료로 바꾸지 않았다. task는 IN_PROGRESS이며 소비자/배포 완료라고 쓰지 않는다. 현재 CI 성공과 미해결 finding은 별개이며 이 후보를 PASS로 전환할 근거가 아니다.

## NOT_RUN·한계

- NOT_RUN: 실제 소비자 workflow 실행·CI·수정. common 합성 fixture와 고정 후보만 검토했으며 소비자 gate/T-403을 닫지 않는다.
- NOT_RUN: Docker daemon/pull/inspect, 원격 action 실행·실제 버전/major 조회. 문법과 정적 참조 판정만 확인했다.
- NOT_RUN: package build/install/publish, npm/PyPI 게시. task 범위 밖이며 사용자 미게시 제약을 유지한다.
- NOT_RUN: exact candidate의 별도 release-push CI. 이번에는 조회한 PR run만 성공 근거다.
- NOT_RUN: 모든 YAML 문법의 완전 적합성·Windows junction/네트워크 공유·경쟁 조건. 양 OS의 파일/디렉터리 symlink는 실제 실행했으며 이를 모든 파일시스템 경계 증명으로 확대하지 않는다.
- 두 OS 전체 시험·validator·위 110회 CLI는 실행 완료했다. 위 NOT_RUN을 성공 건수에 넣지 않았다.

최종 판정은 BLOCK이다. 원 B-P1-01/B-P2-04는 부분 수정이며, B-P2-05/06/07의 새 재현도 disposition이 필요하다. 원 B-P1-02/B-P1-03은 위 범위에서 FIXED다. 수정 후보는 별도 immutable SHA로 재검토해야 한다.
