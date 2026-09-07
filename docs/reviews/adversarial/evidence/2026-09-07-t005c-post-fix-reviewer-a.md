# T-005c 수정 후 독립 full 적대적 리뷰 A 원본

- 실행 ID: `T005C-A-PF1-20260907-155259-03f2cae`.
- 최종 판정: **BLOCK**. 초기 A finding 6개 중 2개 FIXED·4개 OPEN이며 새 P2 finding 2개다. 누적 8개 중 열린 finding은 **P1 1개·P2 5개**다. P0·P3 finding은 없다.
- 시작: `2026-09-07T15:52:59.6583337+09:00`; 검증 종료: `2026-09-07T15:57:31.2819568+09:00`.
- Candidate: **`03f2cae9a817da96a0eb28ae6487c721464d202f`**.
- Parent: `3ef3fc4f91ba2b6320ba6197176f54917227c31e`; 최초 A review candidate: `5526c018380023afd362bd3993d110ee81c3b10a`.
- 공통 manifest: `.git/codex-audit/2026-09-07-t005c-post-fix-manifest.md`; 실제 SHA256 **`cd1fb434401e1b24dcb2e9d1193719d17f9a757e2ba1f6d3a23774cdc6943920`**가 전달값과 일치했다.
- 새 detached worktree: `F:/dev/kor-travel-common-wt/review-t005c-post-a`. `git worktree add --detach <worktree> <candidate>`로 생성했다. 시작·종료 `git rev-parse HEAD`가 candidate와 일치했고 `git status --porcelain=v1 --untracked-files=all`은 빈 출력이었다. WSL Git에서도 SHA·clean을 확인하고 종료 시 clean을 재확인했다.
- Parent 대비 코드·시험·정본 전체 delta **3파일·258행 추가·36행 삭제**를 읽었다. 최초 후보 대비 추가된 review 기록의 파일 목록만 확인했고 상대 reviewer 원본·통합 판정·기존 post-fix 원본 내용은 읽지 않았다. 이전 자기 A 원본과 새 manifest에 따라 결과를 독립 확정했다.
- 후보·소비자·다른 작업자 파일을 수정하지 않았다. 재현은 candidate 밖의 자동 정리되는 임시 입력에서 실행했고 이 원본만 지정 audit 경로에 저장한다.

## 요청과 범위

정확한 candidate에서 parser/YAML quote·escape·flow/list indentation, 빈 구조, setup-node canonical, 모든 출력 redaction, line/source 계약과 초기 A finding을 재현하고 Windows·WSL 전체·focused tests·validator·CI를 확인하도록 요청받았다. 수정·commit 없이 독립 원본을 제출한다.

> 상대 reviewer 결과나 기존 post-fix 원본은 읽지 말고 후보를 수정하지 마세요.

변경 없는 AGENTS·라우터·resume·상세 T-005c task·registry·workflow의 이전 정본 검토를 재사용했다. `git diff --quiet <최초 후보> HEAD -- AGENTS.md docs/README.md docs/resume.md docs/tasks/T-005c-workflow-static-report.md versions.json .github/workflows/docs.yml`은 exit 0이다. 코드·시험·versions 정본 delta와 직접 반례는 이번에 새로 검증했다.

## 실제 검증

Windows Python 3.14.3과 WSL Ubuntu-26.04의 uv managed Python 3.11.15에서 실행했다. WSL 명령 접두사는 `/home/digitie/.local/bin/uv run --no-project --python 3.11 python -B -X utf8`다. Git 기반 WSL validator 프로세스에만 `GIT_DIR=/mnt/f/dev/kor-travel-common/.git/worktrees/review-t005c-post-a`, `GIT_WORK_TREE=/mnt/f/dev/kor-travel-common-wt/review-t005c-post-a`를 설정했다. 저장소 설정은 바꾸지 않았다.

| 실제 명령·검사 | Windows | WSL |
|---|---|---|
| `python -B -X utf8 -m unittest discover -s tests -p 'test_*.py'` | 173 tests·skip 0, 41.634초, exit 0 | 173 tests·skip 0, 25.931초, exit 0 |
| `python -B -X utf8 -m unittest discover -s tests -p 'test_check_versions.py'` | 78 tests·skip 0, 18.204초, exit 0 | 78 tests·skip 0, 17.822초, exit 0 |
| `python -B -X utf8 tools/validate_document_links.py` | 303문서·2194대상, 오류 0 | 동일 |
| `python -B -X utf8 tools/validate_plan.py` | task 102개, 오류 0 | 동일 |
| `python -B -X utf8 tools/check_spdx.py` | 29파일, 오류 0 | 동일 |
| `python -B -X utf8 tools/scan_secrets.py --all` | 378파일, 발견 0·예외 0 | 동일 |
| `python -B -X utf8 tools/check_prod_redaction.py --all` | 378파일, 발견 0·예외 0 | 동일 |
| `python -B -X utf8 tools/check_versions.py --self-check` | exit 0 | exit 0 |
| 직접 CLI | **66회**, 아래 finding 재현 | 같은 66회·동일 결과 |
| `git diff --check <parent> HEAD`, `git diff --check <최초 후보> HEAD` | 각각 exit 0 | Windows 결과 사용 |

66회는 최초 반례·대조 33회, 새 경계 20회, fixture/manifest 9회, symlink 3회, Unicode 오류 종류 재확인 1회다. 기본 CLI는 `python -B -X utf8 tools/check_versions.py <임시 루트> --registry <임시 registry.json> --repo app-a --mode fail --json <임시 out.json> --markdown <임시 out.md>`이며 임시 `GITHUB_STEP_SUMMARY`도 설정했다. registry는 candidate 시험의 `REGISTRY`다. fixture는 report 모드, manifest는 report/warn/fail 세 모드로 실행했다. 실제 표식·사설 주소를 출력하지 않고 문자열을 분할 생성한 뒤 stdout/stderr·JSON·Markdown·summary 포함 여부만 출력했다.

static fixture의 5 findings와 dynamic의 4 findings, 각각 uses·Node의 원본 행 번호가 유지됐다. with-first 수정은 node 행 8·uses 행 9로 정확히 보고했다. malformed fixture 4개는 파일별 격리 입력에서 각각 exit 2, manifest의 루트 이동 참조는 report/warn exit 0·fail exit 1과 같은 FLOATING_REF 행을 유지했다.

## 초기 finding disposition

| 원 ID | 원 심각도 | disposition | 직접 재현 결과 |
|---|---|---|---|
| A-P1-01 | P1 | **OPEN** | 최초 AWS 형태의 ref·Node·파일명은 네 출력 채널에서 가려졌다. 비밀번호 할당문·사설 주소/파일명은 여전히 네 채널로 노출 |
| A-P1-02 | P1 | **FIXED** | colon-space plain scalar·잉여 flow bracket·bare alias·잘못된 single quote 원 반례 모두 exit 2. 새 잘못된 hex·범위 밖 Unicode escape도 exit 2 |
| A-P2-03 | P2 | **OPEN** | 단독 missing/empty/operation 없는 구조와 setup-node의 잘못된 with는 exit 2로 수정. 정상 uses와 섞으면 빈 step·job이 정상 성공 |
| A-P2-04 | P2 | **OPEN** | with-first key 순서 수정과 행 보존 확인. 원 4칸 block 들여쓰기·indentless sequence 반례는 그대로 exit 2 |
| A-P2-05 | P2 | **OPEN** | 원 balanced shell quote와 YAML escape는 수정. plain scalar 내부의 짝 없는 apostrophe/double quote는 여전히 잘못 거부 |
| A-P2-06 | P2 | **FIXED** | 공백 있는 setup-node가 node BELOW_FLOOR·fail exit 1을 정확히 보고 |

## A-P1-01 잔여 — 기존 비공개 정책과 다른 regex로 비밀번호·운영 주소가 노출된다

- 원 심각도 **P1**, disposition **OPEN**.
- 위치: `tools/check_versions.py:1307`의 새 sensitive regex와 1320행 `_workflow_display_value`.
- 최소 재현: `marker = "fixture" + "pw" + "Z" * 12`로 값을 만들고 setup-node의 인용 node-version에 `"password=" + marker`를 넣는다. **양 OS NO_ENGINES·exit 1이지만 stdout·JSON·Markdown·step summary에 marker가 그대로 포함**된다.
- 사설 주소도 `".".join(["10", "29", "41", "53"])`로 생성해 Docker registry host 또는 workflow 파일명에 넣었다. 두 경우 모두 **양 OS exit 0·uses OK**, 네 출력 채널에 주소가 남았다. 실제 주소 원문을 도구 출력이나 이 보고서에 적지 않았다.
- 원인: 새 정규식은 비밀 키워드 뒤의 colon/equals 구문과 운영 주소 정책을 포함하지 않는다. 이미 candidate의 `.secret-scan-patterns`에는 SECRET-ASSIGNMENT가, `.prod-redaction-patterns`에는 PRIVATE-IPV4 등이 정의돼 있다.
- 영향: 최초 예시만 가려지고 CI 로그·artifact 비공개 계약은 성립하지 않는다.
- 권고: 기존 정책과 workflow 출력 비공개 처리의 탐지 집합을 일치시키고, declared·installed·scope·roots 및 모든 채널에서 정책에 걸린 원문이 남지 않는지 검사한다.

## A-P2-03 잔여 — workflow 단위 개수만 검사해 잘못된 형제 구조를 놓친다

- 원 심각도 **P2**, disposition **OPEN**.
- 위치: `tools/check_versions.py:2126`의 checked_targets, 2149행의 uses 없는 step continue, 2158행의 workflow 전체 0건 검사.
- 최소 재현: 정상 `actions/checkout@v4` step 뒤에 `- name: useless`를 추가한다. **양 OS fail exit 0·uses OK 1행**이다. 정상 job 옆에 `steps: []`인 별도 job을 추가해도 같은 결과다.
- checkout step의 `with: [22, 24]`도 정상 uses OK·exit 0이다. setup-node의 with 자료형 검사만 추가됐고 다른 action의 동일 구조 오류는 남아 있다.
- 영향: 단독 빈 workflow를 닫아도 malformed job/step을 정상 형제 하나로 가릴 수 있다.
- 권고: 전역 대상 개수와 별개로 job별 steps·step별 run/uses·with map 구조를 검증하고 잘못된 형제 구조를 건너뛰지 않는다.

## A-P2-04 잔여 — 문서가 지원하는 block collection 범위와 구현이 다르다

- 원 심각도 **P2**, disposition **OPEN**.
- 위치: `tools/check_versions.py:1552`의 고정 parent+2 검사 및 block/list continuation 처리.
- 원 with-first 반례는 수정됐다. 그러나 정상 workflow를 단계당 4칸으로 쓰거나 steps와 sequence marker를 같은 들여쓰기에 놓은 최초 두 반례는 **양 OS exit 2**다. 최초 PyYAML 6.0.3 구문 대조를 재사용했으며 후보 CLI는 이번에 다시 실행했다.
- 새 문서도 block map/list를 지원한다고 쓰고 2칸만 허용하는 제한을 명시하지 않는다. 지원 경계의 수정 또는 명시적 근거 있는 disposition이 없다.
- 추가 collection 대조: 단순 flow sequence `on: [push,]`도 exit 2지만 PyYAML은 유효하게 읽는다. quoted flow sequence 대조는 정상이다. 이 trailing separator까지 지원하지 않을 의도라면 허용 집합을 문서에 명확히 구분해야 한다.
- 영향: 일반적인 YAML 표기 선택 때문에 소비자 입력 전체가 거부되고 실제 제한을 문서에서 알 수 없다.
- 권고: 허용 block/flow collection 문법을 task·정본과 맞추고 key 순서·들여쓰기·sequence 구분자 경계를 각각 검증한다.

## A-P2-05 잔여 — plain scalar 안의 quote를 인용 시작으로 오인한다

- 원 심각도 **P2**, disposition **OPEN**.
- 위치: `tools/check_versions.py:1345`의 `_strip_yaml_comment` 및 동일 방식의 pair 분할 quote 추적.
- 최소 재현: 정상 workflow의 첫 줄을 `name: fixture's build`로 바꾸면 **양 OS exit 2**다. `name: a"b`도 같은 결과다. 두 값은 plain scalar이며 인용 문자열을 시작한 것이 아니다.
- Windows PyYAML 6.0.3으로 두 파일을 이번에 새로 읽어 유효한 YAML임을 확인했다. 원 balanced shell quote·YAML double-quoted escape 대조는 이제 통과한다.
- 원인: scalar가 plain 형태인지와 무관하게 중간의 quote도 인용 시작으로 간주한다.
- 영향: 정상 workflow 이름·shell 명령의 apostrophe 하나로 전체 정적 보고가 중단된다.
- 권고: scalar 시작 위치와 문맥에 따라 인용 여부를 구분하고 plain 내용의 quote와 주석을 올바르게 처리한다.

## 새 A-P2-07 — Unicode escape가 출력 단계의 처리되지 않은 예외를 유발한다

- 심각도 **P2**, disposition **OPEN**.
- 위치: `tools/check_versions.py:1515`의 `chr(int(digits, 16))`, 1320행 display 검사와 main의 출력 경로.
- 최소 재현: setup-node의 node-version에 YAML 텍스트 `"\uD800"`을 둔다. backslash+u escape를 파일에 쓰는 재현이며 실제 surrogate 문자를 파일에 직접 기록한 것이 아니다.
- **Windows·WSL 모두 exit 1·UnicodeEncodeError traceback·JSON 미생성**이다. 별도 CLI로 exception 종류까지 확인했다. 문법 오류나 지원 밖 값에 대한 일반 입력 오류 2가 아니다.
- 원인: Unicode surrogate 코드 포인트를 문자열로 만들고 UTF-8 출력 가능성을 검사하지 않은 채 보고서에 넣는다.
- 영향: 비정상 입력 하나가 판정·보고 출력을 중단시키고 내부 stack/path를 출력한다.
- 권고: Unicode scalar가 아닌 escape를 파싱 경계에서 일반 오류로 닫고, 인용 문자열의 모든 허용 코드 포인트가 모든 출력 인코딩에서 안전한지 검증한다.

## 새 A-P2-08 — local action symlink의 exit 계약이 새 정본과 다르다

- 심각도 **P2**, disposition **OPEN**.
- 위치: `tools/check_versions.py:2015` 부근 local action 경로 분류, `docs/standards/versions.md:103`.
- 최소 재현: 임시 입력 root 안의 `local`을 root 밖의 다른 임시 디렉터리로 symlink하고 `uses: ./local`로 검사한다. 두 임시 경로는 리뷰어가 소유한 fixture이며 실제 소비자 경로가 아니다.
- **Windows·WSL 모두 NO_LOCK·fail exit 1**이다. 새 정본과 manifest는 workflow/local 경로의 root 밖 symlink를 입력 오류 2로 닫는다고 명시한다.
- workflow 파일 자체 및 workflows 디렉터리를 root 밖으로 symlink한 두 대조는 각각 양 OS exit 2로 수정됐다.
- 영향: local symlink escape만 다른 진단·모드 규칙을 적용해 report 모드에서는 입력이 성공 상태로 남을 수 있다. 이번 fail 실행에서 외부 action 본문을 읽었다는 증거는 없으며 그 주장은 하지 않는다.
- 권고: local symlink에도 명시된 입력 오류 2를 적용하거나, 기술적 근거가 있다면 task·정본의 계약을 정확히 수정하고 모든 모드 대조를 남긴다.

## 정상 회귀·근거·CI

기존 Node 하한·동적/list/숫자/file 입력, 원본 행 위치, canonical setup-node, malformed scalar·quote·flow 실패, 단독 빈 대상 오류, 정상/비정상 remote·Docker 참조 대조가 양 OS에서 일치했다. 새 Docker empty name·다중 @·remote parent segment는 FLOATING_REF이며 정상 Node image tag·digest는 OK다. 전체 npm/Python 회귀 시험도 통과했다.

[YAML 1.2.2 공식 규격](https://yaml.org/spec/1.2.2/)과 [GitHub workflow 문법](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax)을 2026-09-07에 확인한 근거를 재사용했다. 새 plain scalar·flow/escape 6개를 PyYAML로 별도 대조했고, 그 구문 결과를 workflow 실행 성공으로 세지 않았다.

`gh run list --commit <candidate> --json databaseId,headSha,event,status,conclusion,url`와 `gh run view 34092707302 --json headSha,event,status,conclusion,url,jobs`로 [PR CI 34092707302](https://github.com/digitie/kor-travel-common/actions/runs/34092707302)를 직접 확인했다. HEAD는 정확한 candidate, event는 pull_request, run 결론은 success다. docs(101649415903)·Windows tools(101649415956)·check-versions(101649416007)·secret-scan(101649416020)·Ubuntu tools(101649416030) 5개 job 모두 success였다.

- **NOT_RUN(원격 범위 제한)**: main/release CI, CI job 내부 로그·시험 건수. 로컬 시험 건수·시간과 CI 결론은 분리했다.
- **NOT_RUN(범위 밖)**: 실제 소비자 원천·설치·workflow 실행, remote action major·Docker 내용 조회, 전체 YAML/Actions parser 동등성, 패키지 build/install/publish.
- **NOT_RUN(권한 범위 밖)**: consumer write, 후보 수정, commit·merge·태그·Release 생성.
- **독립성 때문에 미열람**: 다른 reviewer 원본·통합 판정·기존 post-fix 원본 내용. manifest에 나열된 다른 reviewer ID의 disposition을 그들의 결과를 읽고 대신 확정하지 않았다.
- 최종 **BLOCK**: A-P1-01·A-P2-03·A-P2-04·A-P2-05 OPEN, 새 A-P2-07·A-P2-08 OPEN. A-P1-02·A-P2-06은 FIXED다.
