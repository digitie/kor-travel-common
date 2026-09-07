# T-005a 세 번째 수정 후 독립 full 리뷰 A 원본

- 실행 ID: `T005A-A-PF3-20260907-124501-3c5801f`.
- 최종 판정: **PASS**. 누적 A finding 5개 모두 FIXED, 새 finding 0개다.
- 시작: `2026-09-07T12:45:01.8878317+09:00`; 종료: `2026-09-07T12:47:45.6951878+09:00`.
- candidate: `3c5801f14855a067080f257ec83d2279de32c74a`; PR base: `6e1881b86f017d604ccfa416bd368e5aba24c669`; 수정 대조 기준: `735efed760d2703b3f5769e58270954352566f39`.
- 새 detached worktree: `F:/dev/kor-travel-common-wt/review-t005a-post3-a`. `git worktree add --detach <worktree> <candidate>`로 생성했다. 시작·종료 `git rev-parse HEAD`가 candidate와 일치하고 `git status --porcelain=v1 --untracked-files=all`은 빈 출력이다. WSL Git에서도 실제 HEAD와 clean을 확인했다.
- 전체 수정 delta는 코드 3행·회귀 시험 6행 추가, 2파일이다. 전체 diff와 호출 문맥, 이전 A 원본 및 post2 판정을 대조했다. candidate·소비자·다른 작업자의 파일을 수정하지 않았으며 이 원본만 candidate 밖에 저장했다.

## 전달 요청 원문

> post3 독립 리뷰를 새 후보에서 진행해 주세요. immutable candidate `3c5801f14855a067080f257ec83d2279de32c74a`, base `6e1881b86f017d604ccfa416bd368e5aba24c669`, detached worktree `F:/dev/kor-travel-common-wt/review-t005a-post3-a`. 이전 A 원본·post2 PASS 및 이번 3줄 수정만 읽고 B 결과는 읽거나 공유하지 마세요. 모든 누적 A 반례와 특히 branch/tag/rev 값에 @가 있는 경우, URL/group/PEP735·공유 lock·오류 비공개를 Windows/WSL에서 재현하고 전체 140 테스트/validators를 실행하세요. 결과는 `.git/codex-audit/2026-09-07-t005a-post3-reviewer-a.md`에 원본으로 보존하고 정확한 SHA/clean·finding disposition·PASS/BLOCK·NOT_RUN을 보고하세요. 수정은 하지 마세요.

## 실제 검증

모든 명령은 candidate worktree에서 실행했다. WSL의 실행기는 `/home/digitie/.local/bin/uv run --no-project --python 3.11 python -B -X utf8`다. Windows에서 생성한 worktree의 Git 메타데이터 경로를 WSL에서 명시하기 위해 validator 프로세스에만 `GIT_DIR=/mnt/f/dev/kor-travel-common/.git/worktrees/review-t005a-post3-a`, `GIT_WORK_TREE=/mnt/f/dev/kor-travel-common-wt/review-t005a-post3-a`를 설정했다. 저장소 설정 파일은 바꾸지 않았다.

| 명령·검사 | Windows 결과 | WSL 결과 |
|---|---|---|
| `python -B -X utf8 -m unittest discover -s tests -p 'test_*.py'` | Python 3.14.3, 140 tests·skip 0, 30.572초, exit 0 | Python 3.11.15, 140 tests·skip 0, 14.635초, exit 0 |
| `python -B -X utf8 tools/validate_document_links.py` | 272문서·2151대상, 오류 0 | 동일 |
| `python -B -X utf8 tools/validate_plan.py` | task 102개, 오류 0 | 동일 |
| `python -B -X utf8 tools/check_spdx.py` | 20파일, 오류 0 | 동일 |
| `python -B -X utf8 tools/scan_secrets.py --all` | 335파일, 발견 0·예외 0 | 동일 |
| `python -B -X utf8 tools/check_prod_redaction.py --all` | 335파일, 발견 0·예외 0 | 동일 |
| `python -B -X utf8 tools/check_versions.py --self-check` | exit 0 | exit 0 |
| 누적 반례와 추가 경계의 실제 CLI | 55사례, 기대 exit 55개 일치 | 동일 |
| virtual root 공유 lock 검사 | 3사례, 누락·중복 없음 | 동일 |

`git diff --check <PR base> HEAD`와 `git diff --check <수정 대조 기준> HEAD`는 각각 exit 0이다. 변경 없는 AGENTS·라우터·resume·task·버전 규약·registry·fixture·workflow는 `git diff --quiet <수정 대조 기준> HEAD -- AGENTS.md docs/README.md docs/resume.md docs/tasks.md docs/tasks/T-005a-check-versions-uv-lock.md docs/standards/versions.md versions.json tests/fixtures/versions .github/workflows/docs.yml`의 exit 0으로 동일성을 확인하고 이전 정본 대조를 재사용했다.

CLI 재현은 기존 시험의 `REGISTRY`와 `python_fixture`로 자동 정리되는 임시 디렉터리에 입력을 만들고 `tools/check_versions.py <임시 루트> --registry <임시 registry.json> --repo app-a --mode fail --json <임시 report.json> --no-step-summary`를 실행했다. stdout/stderr와 JSON을 캡처해 exit·traceback·합성 표식 유출을 검사했다. 양 OS 모두 traceback 0, 표식 유출 0이며 합성 비밀 원문은 출력하지 않았다.

## 누적 finding disposition

| 원 ID | 원 심각도 | disposition | 원 반례의 새 재현 결과 |
|---|---|---|---|
| A-P1-01 | P1 | **FIXED** | 고정 선언 아래 미고정 lock git source와 정상/비정상 복수 source 모두 exit 1. branch 선언과 고정 lock 조합도 실패하며 전체 lock source 순회 유지 |
| A-P1-02 | P1 | **FIXED** | malformed URL·hostname 없음·잘못된 port·저장소 없는 fragment·marker 정수·dependency mapping·group 내부 정수 모두 exit 2. 정상 lock 및 marker별 복수 버전 대조 유지 |
| A-P2-03 | P2 | **FIXED** | group 문자열/정수, list source의 잘못된 git 자료형·충돌 ref, 없는 include·자기/상호 순환·추가 include key 모두 exit 2 |
| A-P2-04 | P2 | **FIXED** | field/package 이름의 합성 표식 입력 오류는 exit 2. stdout/stderr에 표식과 traceback 없음 |
| A-P2-05 | P2 | **FIXED** | `Test_Group`을 `test-group`으로 include한 원 반례와 점·대소문자 정규화가 exit 0. 정규 이름 충돌 exit 2, 정상 diamond include exit 0 |

post2의 38사례를 전부 다시 실행하고 이번 경계 17사례를 추가했다. `tag`와 `rev` 각각에 `topic@v1.2.3`, `topic@<40자리 SHA>`, 인코딩한 `@`, 이중 `@`, 선두 `@`, 두 번 인코딩한 `@`, `main`을 넣은 14사례가 모두 exit 1이다. 직접 PEP 508 git URL의 중첩/인코딩 `@` 2사례도 exit 1이다. 정상 `git+ssh://git@github.com/example/custom-lib@v1.2.3` 선언은 exit 0이므로 사용자명 구분자의 `@`는 오탐하지 않았다. 기존 branch 5사례는 모두 exit 1이고 정상 tag·전체 SHA rev 대조는 exit 0이다.

최소 재현은 Python 3.12 이상 프로젝트의 `dependencies=["custom-lib"]`, `[tool.uv.sources]`의 git 저장소와 `tag` 또는 `rev` 값 `topic@v1.2.3`, 동일 패키지의 전체 SHA로 고정된 lock source다. 두 필드 모두 `FLOATING_REF`로 실패한다. `tools/check_versions.py` 598행 부근의 변경은 디코딩한 URL 경로의 `@` 개수를 정확히 하나로 제한해 마지막 조각만 고정 태그로 해석하던 경계를 닫는다. 이번 시험 6행도 두 필드의 이 반례를 명시한다.

공유 lock 재현은 virtual root와 두 member, lock 전체의 차단 대상 mcp 및 미고정 전이 git 소스로 구성했다. member 하나만 선택·둘 선택·역순 선택 각각에서 mcp BLOCKED 1행과 git FLOATING_REF 1행이 양 OS 모두 유지됐다.

## 한계와 독립성

- **재사용**: 변경 없는 정본·고정 upstream 및 PEP 735 근거의 이전 A 대조. 코드 delta·누적 반례·전체 회귀·validator는 새로 실행했다.
- **NOT_RUN(독립 원격 CI 미조회)**: 이 candidate의 GitHub PR/main/release run. 로컬 성공을 CI 성공으로 세지 않는다.
- **NOT_RUN(외부 실측 범위 밖)**: 실제 소비자 고정 원천 재대조, 소비자 설치·빌드·`uv sync --locked`, 전체 uv resolver 동등성 검사. fixture 결과를 소비자 성공으로 세지 않는다.
- **NOT_RUN(금지·범위 밖)**: consumer write, npm/PyPI 게시, merge·태그·Release 생성.
- 상대 reviewer의 원본·finding·재현 결과는 열람하거나 요청하지 않았다. 모든 검증 완료 후 원본 저장 직전 coordinator가 상대 PASS 상태를 자발적으로 통지했으나, 이 판정의 근거에는 사용하지 않았다.
- 최종 **PASS — 누적 A finding 5개 모두 FIXED, 새 finding 0개**. 이 판정은 위 명시된 검사 범위와 미실행 한계를 포함한다.
