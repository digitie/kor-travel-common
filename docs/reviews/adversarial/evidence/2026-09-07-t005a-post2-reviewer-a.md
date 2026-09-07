# T-005a 두 번째 수정 후 독립 full 리뷰 A 원본

- 실행 ID: `T005A-A-PF2-20260907-123400-735efed`.
- 판정: **PASS**. 누적 A finding 5개 모두 FIXED, 새 finding 0개다.
- 시작: `2026-09-07T12:34:00.2181327+09:00`; 종료: `2026-09-07T12:37:57.5157746+09:00`.
- candidate: `735efed760d2703b3f5769e58270954352566f39`; PR base: `6e1881b86f017d604ccfa416bd368e5aba24c669`; 수정 대조 기준: `902750016d157bb195fb05c01358c4b8a6ffe812`.
- 새 detached worktree: `F:/dev/kor-travel-common-wt/review-t005a-post2-a`. 시작·종료 실제 HEAD가 candidate와 일치하고 `git status --porcelain=v1 --untracked-files=all`은 모두 빈 출력이다.
- 변경은 5파일·241행 추가·19행 삭제다. 실행 코드·시험 2파일 전체 delta, 공통 manifest와 A의 기존 기록을 대조했다. 추가된 상대 reviewer 기록의 내용은 지시대로 읽지 않았다. 최신 요청의 candidate를 검토 기준으로 삼았으며 역사 manifest의 최초 SHA로 바꾸지 않았다.
- candidate·소비자·다른 작업자의 파일은 수정하지 않았다. 이 원본만 candidate 밖 `.git/codex-audit`에 저장한다. 재현 입력은 자동 정리되는 임시 디렉터리에만 작성했다.

## 전달 요청 원문

> 새 수정 후보 `735efed760d2703b3f5769e58270954352566f39`에 대해 T-005a 사후 독립 full 리뷰를 다시 실행해 주세요. base는 `6e1881b86f017d604ccfa416bd368e5aba24c669`, 새 detached worktree는 `F:/dev/kor-travel-common-wt/review-t005a-post2-a`로 고정하세요. 이전 A 원본의 A-P1-02/A-P2-03/A-P2-05 반례와 이번 수정 delta를 읽고, B 결과는 읽거나 공유하지 마세요. hostname 없는/잘못된 port URL, lock group 내부 자료형, PEP 735 이름 정규화·중복·순환·include 정확한 key, branch 이름에 @가 있는 고정 우회, 최초 모든 반례를 Windows/WSL에서 다시 공격하세요. 전체 140+ 회귀와 validators를 실행하고 consumer write는 하지 마세요. 결과를 `.git/codex-audit/2026-09-07-t005a-post2-reviewer-a.md`에 원본으로 저장해 주세요. 수정은 하지 말고 정확한 SHA/clean 상태·PASS/BLOCK·finding disposition·NOT_RUN을 보고하세요.

## 새 실행 결과

| 실제 명령·검사 | 결과 |
|---|---|
| Windows `python -B -X utf8 -m unittest discover -s tests -p 'test_*.py'` | Python 3.14.3, **140 tests·skip 0**, 33.045초, exit 0 |
| WSL `uv run --no-project --python 3.11 python -B -X utf8 -m unittest discover -s tests -p 'test_*.py'` | Python 3.11.15, **140 tests·skip 0**, 15.780초, exit 0 |
| `python -B -X utf8 tools/validate_document_links.py` | 272문서·2151대상, 오류 0 |
| `python -B -X utf8 tools/validate_plan.py` | task 102개, 오류 0 |
| `python -B -X utf8 tools/check_spdx.py` | 20파일, 오류 0 |
| `python -B -X utf8 tools/scan_secrets.py --all` | 335파일, 발견 0·예외 0 |
| `python -B -X utf8 tools/check_prod_redaction.py --all` | 335파일, 발견 0·예외 0 |
| `python -B -X utf8 tools/check_versions.py --self-check` | exit 0. 레지스트리 자체 검사 |
| `git diff --check <PR base> HEAD` 및 `<수정 대조 기준> HEAD` | 각각 exit 0, 빈 출력 |
| 원 반례·추가 경계의 실제 CLI | **Windows 38사례, WSL 38사례**, 기대 exit 전부 일치·traceback 0·합성 표식 유출 0 |
| virtual root 공유 lock scope 재현 | 양 OS 각각 3사례, 멤버 하나·둘·역순 모두 차단 mcp 1행과 전이 git FLOATING_REF 1행 유지 |

38사례는 최초 14개, 최초 보충 5개, 직전 잔여/정상 대조 8개, 이번 정규화·branch 경계 11개다. 기존 `REGISTRY`와 `python_fixture`로 임시 입력을 만들고 candidate의 실제 `tools/check_versions.py <임시 루트> --registry <임시 registry.json> --repo app-a --mode fail --json <임시 report.json> --no-step-summary`를 실행했다. 출력은 캡처하고 기대 exit·traceback·표식 유출을 단언했다. 합성 비밀은 조각을 합쳐 생성했고 원문을 출력하지 않았다.

추가 경계에는 정규 이름 충돌, diamond 형태의 정상 중복 include, 빈 include 이름, 점/밑줄/하이픈·대소문자 정규화, branch 값 `topic@v1.2.3`, `topic@<40자리 SHA>`, 인코딩된 `@`, 이중 `@`, 버전처럼 생긴 branch를 포함했다. branch 다섯 사례는 모두 fail exit 1이고 정상 tag·rev 대조는 exit 0이다. 코드의 branch 종류 표식 확인이 마지막 `@` 뒤의 태그/SHA 모양보다 먼저 적용되는 것도 직접 읽었다.

## 누적 finding disposition

| 원 ID | 원 심각도 | disposition | 새 재현 근거 |
|---|---|---|---|
| A-P1-01 | P1 | **FIXED** | 고정 선언 아래의 미고정 lock source와 정상/비정상 복수 source는 fail exit 1. branch 선언+고정 lock도 계속 실패. 모든 lock git source 순회를 유지 |
| A-P1-02 | P1 | **FIXED** | 최초 URL·marker·dependency mapping과 저장소 없는 fragment, 잔여 hostname 없는 URL·잘못된 port·group 내부 정수 항목 모두 exit 2. 정상 lock·복수 버전 대조 유지 |
| A-P2-03 | P2 | **FIXED** | 잘못된 group/source·충돌 ref·없는 include, 자기/상호 순환과 include의 추가 key 모두 exit 2. 활성 경로와 완료 집합 분리, 정확한 include key 확인이 반례와 일치 |
| A-P2-04 | P2 | **FIXED** | 필드명·package 이름의 합성 탐지 표식을 포함한 입력 오류는 exit 2이고 stdout/stderr에 표식·traceback 없음 |
| A-P2-05 | P2 | **FIXED** | `Test_Group`을 `test-group`으로 include한 원 반례가 exit 0. 점을 포함한 이름도 동일 정규화. 정규 이름 충돌은 exit 2, 정상 공유 include DAG는 exit 0 |

새 finding은 없다. virtual source와 공유 lock 전체의 차단·전이 검사도 양 OS에서 확인했다. 기존 npm 판정은 전체 회귀에 포함되며 이번 변경은 runtime 검사·오류 종료·출력의 기존 계약을 유지한다. PEP 735와 uv source의 기준은 기존 A 리뷰에서 직접 확인한 공식 문서·고정 upstream source를 재사용했다.

## 재사용·미실행·판정 범위

- **재사용**: 변경 없는 AGENTS·문서 라우터·resume·task·버전 정본·registry·fixture·workflow의 이전 대조. `git diff --quiet <직전 candidate> HEAD -- AGENTS.md docs/README.md docs/resume.md docs/tasks.md docs/tasks/T-005a-check-versions-uv-lock.md docs/standards/versions.md versions.json tests/fixtures/versions .github/workflows/docs.yml`이 exit 0임을 새로 확인했다. 코드·시험 delta와 모든 실패 반례는 재사용으로 대체하지 않았다.
- **NOT_RUN(독립 원격 CI 미조회)**: 이 candidate의 GitHub run 및 main/release 실행. 양 OS 로컬 140 tests를 CI 성공으로 세지 않는다.
- **NOT_RUN(외부 실측 없음)**: airport/weather 고정 원천의 재대조, 실제 설치·빌드·`uv sync --locked`. 공통 fixture 결과는 실제 소비자 evidence가 아니다.
- **NOT_RUN(범위 밖)**: consumer write, npm/PyPI 게시, merge·태그·Release 생성, 전체 uv resolver 동등성 검사. 다른 reviewer의 결과를 읽거나 이번 원본과 합치지 않았다.
- 최종 **PASS — 누적 A 5개 ID 모두 FIXED, 새 finding 0개**. 실제 외부 gate의 완료 여부는 위 미실행 항목과 구분한다.
