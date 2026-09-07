# T-005a 수정 후 독립 full 리뷰 A 원본

- 실행 ID: `T005A-A-PF-20260907-122149-9027500`.
- 판정: **BLOCK**. 원 A-P1-01·A-P2-04는 FIXED, 원 A-P1-02·A-P2-03은 잔여 반례로 OPEN. 신규 **A-P2-05** OPEN 1개다.
- 시작: `2026-09-07T12:21:49.5622270+09:00`; 종료: `2026-09-07T12:28:01.3301469+09:00`.
- candidate: `902750016d157bb195fb05c01358c4b8a6ffe812`; PR base: `6e1881b86f017d604ccfa416bd368e5aba24c669`; 수정 대조 기준: `3bc0f473833aa51a8656b045b705891debf8cf13`.
- 새 detached worktree: `F:/dev/kor-travel-common-wt/review-t005a-post-a`. 시작·종료 실제 `git rev-parse HEAD`는 candidate와 일치했고 `git status --porcelain=v1 --untracked-files=all`은 모두 빈 출력이다.
- 검토 범위: 수정 delta 전체 3파일·171행 추가·39행 삭제, 원 finding과 shared lock·PEP 735·virtual source·기존 npm 회귀. 이번과 과거의 다른 reviewer 결과를 읽거나 공유하지 않았다.
- candidate·소비자·다른 파일은 수정하지 않았다. 이 원본만 candidate 밖의 기본 checkout `.git/codex-audit`에 작성했다. 재현 입력은 자동 정리되는 임시 디렉터리에서만 만들었다.

## 전달 요청

> T-005a post-fix 독립 리뷰를 시작해 주세요. immutable candidate는 `9027500` (`9027500b?` 정확한 SHA는 작업 트리에서 `git rev-parse 9027500`로 확인)이며 base는 `6e1881b86f017d604ccfa416bd368e5aba24c669`입니다. 새 detached worktree `F:/dev/kor-travel-common-wt/review-t005a-post-a`를 candidate에서 만들고 clean 시작/종료 SHA를 기록하세요. 초기 A finding(A-P1-01/02, A-P2-03/04)을 읽되 B 결과나 다른 리뷰 결과는 읽거나 공유하지 말고, 입력 구조 fail-close·고정 선언과 모든 lock git source 대조·오류 출력 비공개·shared lock/PEP 735/virtual source를 중심으로 공격적으로 재현하세요. Windows와 WSL의 전체 테스트 및 관련 validator를 실행하고 실제 소비자 쓰기는 하지 마세요. 결과는 `.git/codex-audit/2026-09-07-t005a-post-fix-reviewer-a.md`에 원본 보고서로 남기고, PASS/BLOCK과 finding ID·재현·NOT_RUN을 메시지로 보고하세요. 수정은 하지 마세요.

후속으로 전달받은 full SHA `902750016d157bb195fb05c01358c4b8a6ffe812`는 실제 해석 결과와 같았다. 잔여와 새 finding·최소 재현·영향·권고·미실행을 원본에 보존하라는 요청도 적용했다.

## 실제 검증

| 명령·검사 | 결과 |
|---|---|
| Windows `python -B -X utf8 -m unittest discover -s tests -p 'test_*.py'` | Python 3.14.3, **140 tests·skip 0**, 33.977초, exit 0 |
| WSL `uv run --no-project --python 3.11 python -B -X utf8 -m unittest discover -s tests -p 'test_*.py'` | Python 3.11.15, **140 tests·skip 0**, 15.529초, exit 0 |
| `python -B -X utf8 tools/validate_document_links.py` | 269문서·2150대상, 오류 0 |
| `python -B -X utf8 tools/validate_plan.py` | task 102개, 오류 0 |
| `python -B -X utf8 tools/check_spdx.py` | 20파일, 오류 0 |
| `python -B -X utf8 tools/scan_secrets.py --all` | 332파일, 발견 0·예외 0 |
| `python -B -X utf8 tools/check_prod_redaction.py --all` | 332파일, 발견 0·예외 0 |
| `python -B -X utf8 tools/check_versions.py --self-check` | exit 0. 레지스트리 자체 검사 |
| `git diff --check <PR base> HEAD` 및 `<수정 대조 기준> HEAD` | 각각 exit 0, 빈 출력 |
| 최초 실제 CLI 14사례 재실행 | Windows/WSL 모두 원 구체 반례 수정 확인. exit·판정·원문 비공개 일치 |
| 최초 Windows 보충 5사례 재실행 | 저장소 없는 git source·잘못된 source 거부, 복수 버전 BELOW_FLOOR·유효 include의 FLOATING_REF 유지 |
| 새 경계 CLI 8사례 | 양 OS에서 결과 일치. 아래 잔여·신규 반례와 virtual 정상 대조 |
| group 원 표기 include 대조 1사례 | Windows에서 `Test_Group` 원 표기를 쓰면 OK 2개·exit 0 |
| virtual root를 포함한 공유 lock 3사례 | 양 OS의 멤버 1개·두 멤버·역순 모두 차단 mcp 1행·전이 git FLOATING_REF 1행 유지 |

모든 CLI 재현은 기존 시험의 `REGISTRY`·`python_fixture`로 임시 입력을 만든 뒤 실제 `tools/check_versions.py <임시 루트> --registry <임시 registry.json> --repo app-a --mode fail --json <임시 report.json> --no-step-summary`를 호출했다. stdout/stderr를 캡처하고 exit·판정 건수·합성 표식 포함 여부만 출력했다. 합성 비밀은 조각을 합쳐 생성했으며 원문을 출력하지 않았다. shared lock은 `discover()`가 반환한 scope 중 멤버만 선택하거나 입력 순서를 바꾸어 실제 `Checker.run()`으로 확인했다.

## 원 finding disposition

| ID | 원 심각도 | 판정 | 확인 |
|---|---|---|---|
| A-P1-01 | P1 | **FIXED** | 고정 선언에 미고정 lock source가 있으면 FLOATING_REF·exit 1. 같은 이름의 정상/비정상 복수 source도 모두 순회해 실패를 보존한다. 원 branch 선언 대조군도 계속 실패 |
| A-P1-02 | P1 | **OPEN** | 원 URL·marker·dependency 자료형과 저장소 없는 fragment 반례는 수정됐다. 하지만 host 없는 URL·잘못된 port·group 내부 항목은 아래처럼 여전히 false OK |
| A-P2-03 | P2 | **OPEN** | 원 문자열/정수 group·없는 include·잘못된 git·충돌 ref는 exit 2로 수정됐다. 순환 include와 추가 필드의 잘못된 group 항목은 아직 무시됨 |
| A-P2-04 | P2 | **FIXED** | 미지 필드명·package 이름에 합성 탐지 표식을 넣은 두 원 반례 모두 exit 2, stdout/stderr 표식 없음·traceback 없음. 새 일반 진단이 원문을 재출력하지 않음 |

## A-P1-02 잔여 — URL과 group 내부 구조를 끝까지 확인하지 않음

- 심각도 **P1**, **OPEN**, 위치 `tools/check_versions.py:478` 및 `tools/check_versions.py:540`.
- 최소 재현 1: 정상 fixture의 registry source를 `https://@`로 바꾼다. `urlsplit`의 netloc은 존재하지만 hostname이 없는 주소다. 실제 CLI는 **OK 2개·exit 0**이다.
- 최소 재현 2: source를 `https://example.invalid:bad/simple`로 바꾸면 잘못된 port를 확인하지 않아 역시 **OK 2개·exit 0**이다.
- 최소 재현 3: 정상 fastapi package에 `optional-dependencies = {test = [42]}`를 넣어도 **OK 2개·exit 0**이다. group 값이 list인지만 확인하고 실제 dependency 항목의 구조를 확인하지 않는다.
- 세 사례 모두 Windows/WSL에서 독립 CLI로 재현했다. 기존 marker와 dependency mapping 반례의 수정 자체는 확인했으나, 지원 source/자료형이 잘못됐을 때 exit 2라는 동일 계약의 잔여이므로 원 ID·심각도를 유지한다.
- 영향: 입력 형식이 유효하지 않은 lock이 fail 모드의 정상 보고로 남는다. 실제 uv 설치나 전체 metadata 해석을 요구하는 문제가 아니다.
- 권고: source URL의 hostname·port 등 선택한 문법을 검증하고, 허용된 group 내부 항목도 지원 dependency 자료형으로 검증한다. 실패 진단은 현재 원문 비공개 방식을 유지한다.

## A-P2-03 잔여 — 순환 include와 잘못된 include 항목을 정상 처리함

- 심각도 **P2**, **OPEN**, 위치 `tools/check_versions.py:952`, `tools/check_versions.py:963`.
- 최소 재현 1: 정상 프로젝트·lock에 `[dependency-groups] dev=[{include-group="dev"}]`를 넣는다. 결과는 **OK 2개·exit 0**이다. `a → b → a` 두 그룹 순환도 같은 결과다.
- 최소 재현 2: 유효한 lint 그룹을 두고 `dev=[{include-group="lint",unexpected=true}]`를 넣어도 **OK 2개·exit 0**이다.
- 원인: 확장 완료와 현재 재귀 경로를 하나의 `expanded_groups`로 처리해 순환을 단순 재방문으로 무시한다. include 항목도 정확한 key 집합을 확인하지 않는다.
- 영향: 새 PEP 735 처리에서 잘못된 group 입력을 정상으로 숨기는 원 finding이 일부 남았다. [PEP 735](https://peps.python.org/pep-0735/#dependency-group-include)의 순환 금지와 검증 계약을 이전 리뷰에서 직접 확인한 근거로 재사용했다.
- 권고: 방문 중인 그룹과 확장 완료 그룹을 구분해 순환을 거부하고, include 항목의 자료형·허용 key를 확인한다. 유효한 DAG의 중복 include는 계속 허용해야 한다.

## A-P2-05 신규 — 정상 group 이름을 정규화하지 않아 유효한 include가 실패함

- 심각도 **P2**, **OPEN**, 위치 `tools/check_versions.py:954`, `tools/check_versions.py:964`.
- 최소 재현:

```toml
[dependency-groups]
Test_Group = ["fastapi>=0.115"]
dev = [{include-group = "test-group"}]
```

- 정상 Python manifest·fastapi lock에 위 절을 넣으면 양 OS에서 **exit 2**, 보고서가 생성되지 않는다. `include-group="Test_Group"`처럼 원 표기를 그대로 쓴 일반 대조군은 성공한다.
- 근거: [PEP 735 Specification](https://peps.python.org/pep-0735/#specification)은 group 이름을 비교하기 전에 정규화하도록 규정한다. 위 두 표기는 같은 정규 이름이다. 현재 코드는 원 문자열을 dictionary key와 직접 비교해 없는 그룹으로 판단한다.
- 영향: 유효한 PEP 735 프로젝트가 새 include 검증에서 거부되는 오탐이다. 원 A-P2-03의 잘못된 입력 무시와 반대 방향의 새 회귀이므로 별도 ID를 부여했다.
- 권고: 그룹 정의와 include 참조를 같은 규칙으로 정규화해 비교한다. 정규화 충돌은 오류로 구분하고, 이 정상 입력과 missing/cycle 반례를 함께 회귀 검증한다.

## 재사용·미실행·최종 판정

- **재사용**: 최초 A 원본의 변경 없는 규범·fixture·범위 검토. `git diff --quiet <최초 candidate> HEAD -- AGENTS.md docs/README.md docs/resume.md docs/tasks.md docs/tasks/T-005a-check-versions-uv-lock.md tests/fixtures/versions versions.json`이 exit 0임을 새로 확인했다. 수정된 세 파일과 모든 시험·위 반례는 직접 다시 확인했다.
- **NOT_RUN(독립 원격 CI 미조회)**: candidate의 실제 GitHub run, main/release 경로. 양 OS 로컬 140 tests를 CI 성공으로 표시하지 않았다.
- **NOT_RUN(외부 실측 없음)**: weather/airport 고정 원천 lock 재대조, 실제 설치·빌드·`uv sync --locked`. 합성 입력은 소비자 evidence가 아니다.
- **NOT_RUN(범위 밖)**: 소비자 쓰기, registry 게시, 태그·Release 생성, merge, 전체 uv resolver 실행. 상대 리뷰를 읽거나 후속 수정 내용을 검토하지 않았다.
- 최종 **BLOCK**. 원 2개 FIXED, 원 2개 OPEN, 신규 1개 OPEN. 현재 후보의 전체 회귀 성공은 위 추가 반례를 무효화하지 않으며 후속 수정은 새 immutable 기준선에서 재확인이 필요하다.
