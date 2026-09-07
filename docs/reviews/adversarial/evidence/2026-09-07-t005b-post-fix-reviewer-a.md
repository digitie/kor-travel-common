# T-005b 수정 후 독립 full 적대적 리뷰 A 원본

- 실행 ID: `T005B-A-PF-20260907-135802-cdf7ba0`.
- 최종 판정: **BLOCK**. 이전 A 6개 중 4개 FIXED·2개 OPEN, 새 P2 finding 2개다. 누적 8개 중 열린 finding은 P2 4개다.
- 시작: `2026-09-07T13:58:02.5238168+09:00`; 종료: `2026-09-07T14:02:42.8574071+09:00`.
- 실제 candidate: **`cdf7ba01ccb585b3c00aec69a734266e33ceb510`**. `git rev-parse cdf7ba0`로 확인했다. 최초 요청의 예시 full SHA는 기준으로 사용하지 않았다.
- PR base: `796445fadb9b4fa6de2f392d6169f31abdccc0fa`; 수정 delta base: `12570ccebc58c81510bab7de0735eb4720c494c4`.
- `git worktree add --detach F:/dev/kor-travel-common-wt/review-t005b-a-post cdf7ba01ccb585b3c00aec69a734266e33ceb510`로 새 격리 worktree를 생성했다. 시작·종료 HEAD가 candidate와 같고 `git status --porcelain=v1 --untracked-files=all`은 빈 출력이다. WSL Git에서도 SHA·clean을 확인했다.
- 전체 수정 delta 4파일·488행 추가·98행 삭제를 읽었다. 코드·새 시험·버전 규약·tools README의 변경을 검토하고 이전 A 원본은 반례 기준으로만 사용했다. 상대 원본·finding·판정은 읽거나 요청하지 않았다.
- candidate·소비자·타인 파일은 수정하지 않았다. 임시 입력은 자동 정리되는 디렉터리에만 생성하고 이 원본만 candidate 밖에 저장했다.

## 전달 요청과 확정 기준

> T-005b post-fix 재검토를 시작해 주세요. immutable candidate `cdf7ba0c3e3e6b3f0c2f6e6a6f4c5b3c8d0e0c9f`가 아니라 먼저 `git rev-parse cdf7ba0`로 실제 SHA를 확인해 사용하세요(정확 SHA는 `git rev-parse cdf7ba0` 결과). base `796445fadb9b4fa6de2f392d6169f31abdccc0fa`. 새 detached worktree `F:/dev/kor-travel-common-wt/review-t005b-a-post`를 candidate에서 만들고, old A 결과는 기준으로만 삼되 B 결과는 읽거나 요청하지 마세요. A 전문 영역: requirements `--requirement` 3형식·주석/hash/options/editable·PEP 440 wildcard/compatible/공백/교집합/경계/중복/순환·누락·오류 출력 비공개와 npm/uv 회귀. 전체 delta를 공격적으로 보고, old A-P1-01/P1-02/P2-04/P2-05/P2-06의 수정 여부와 새 finding을 재현하세요. Windows·WSL 전체/focused tests 및 relevant validators, direct negative cases를 실행하세요. 결과 원본을 `.git/codex-audit/2026-09-07-t005b-post-fix-reviewer-a.md`에 저장하고 PASS/BLOCK, 각 finding disposition, 시작/종료 SHA·clean·NOT_RUN을 메시지로 보고하세요. 수정/commit하지 마세요.

후속 정정 원문:

> 정정: 위 메시지의 예시 full SHA는 무시하세요. 실제 candidate SHA는 `cdf7ba01ccb585b3c00aec69a734266e33ceb510`입니다. 이 정확 SHA만 사용해 주세요.

## 실제 검증

Windows Python 3.14.3과 WSL Ubuntu-26.04의 uv managed Python 3.11.15에서 실행했다. WSL 실행기는 `/home/digitie/.local/bin/uv run --no-project --python 3.11 python -B -X utf8`이다. WSL validator 프로세스에만 `GIT_DIR=/mnt/f/dev/kor-travel-common/.git/worktrees/review-t005b-a-post`, `GIT_WORK_TREE=/mnt/f/dev/kor-travel-common-wt/review-t005b-a-post`를 설정했다. 저장소 설정은 바꾸지 않았다.

| 실제 명령·검사 | Windows | WSL |
|---|---|---|
| `python -B -X utf8 -m unittest discover -s tests -p 'test_*.py'` | 155 tests·skip 0, 41.225초, exit 0 | 155 tests·skip 0, 22.065초, exit 0 |
| `python -B -X utf8 -m unittest discover -s tests -p 'test_check_versions.py'` | 60 tests·skip 0, 13.301초, exit 0 | 60 tests·skip 0, 11.963초, exit 0 |
| `python -B -X utf8 tools/validate_document_links.py` | 283문서·2166대상, 오류 0 | 동일 |
| `python -B -X utf8 tools/validate_plan.py` | task 102개, 오류 0 | 동일 |
| `python -B -X utf8 tools/check_spdx.py` | 22파일, 오류 0 | 동일 |
| `python -B -X utf8 tools/scan_secrets.py --all` | 351파일, 발견 0·예외 0 | 동일 |
| `python -B -X utf8 tools/check_prod_redaction.py --all` | 351파일, 발견 0·예외 0 | 동일 |
| `python -B -X utf8 tools/check_versions.py --self-check` | exit 0 | exit 0 |
| 직접 CLI 반례 | 이전 33개·추가 23개·출력 경로 2개, 합계 **58회** | 같은 58회, 같은 결과 |
| `git diff --check <PR base> HEAD` 및 `git diff --check <delta base> HEAD` | 각각 exit 0 | Windows 결과 사용 |

공통 CLI는 `tools/check_versions.py <임시 루트> --registry <임시 registry.json> --repo app-a --mode report --json <임시 report.json> --no-step-summary`다. registry는 candidate의 시험 `REGISTRY`로 만들었다. 이전 fail 모드 반례 3개는 `--mode fail`로 다시 실행했다. 출력 유출 2사례는 `--markdown <임시 out.md>`와 임시 `GITHUB_STEP_SUMMARY`도 설정했다. stdout/stderr·파일은 캡처하고 합성 표식의 포함 여부만 출력했다.

## 기존 finding disposition

| 원 ID | 원 심각도 | disposition | 새 재현 근거 |
|---|---|---|---|
| A-P1-01 | P1 | **FIXED** | short·long 공백·long equals·compact include 모두 하위 mcp BLOCKED를 보고한다. equals 형태 missing도 exit 2. 순환·누락·빈 include는 계속 exit 2 |
| A-P1-02 | P1 | **FIXED** | `==2.*`와 차단 `>=2.1` 교집합을 탐지한다. `~=1.0`·`< 2`·동일 상한의 두 순서 모두 원 오탐이 사라졌다. strict lower 양 순서·세 부분 compatible 상한도 새 대조에서 일치 |
| A-P1-03 | P1 | **FIXED** | 잘못된 Poetry port·legacy URL 정수·metadata runtime 정수를 fail 모드에서 각각 exit 2로 닫는다. source/package/group의 기존 자료형 오류와 정상 대조도 유지 |
| A-P2-04 | P2 | **OPEN** | Poetry lock URL의 원 예외 유출은 수정됐다. requirements의 원 반례는 이제 exit 0·FLOATING_REF가 되어 일반 출력 전체에 표식을 다시 싣는다. 아래 잔여 재현 참조 |
| A-P2-05 | P2 | **OPEN** | 원 unknown option·잘못된 버전 문구·빈 URL은 exit 2, editable main은 FLOATING_REF다. 다만 malformed marker·중첩 괄호·필수 옵션 값 누락은 아직 정상 입력으로 처리한다 |
| A-P2-06 | P2 | **FIXED** | 탭 주석·equals/공백 hash가 정확 fastapi 핀의 OK를 유지한다. 여러 줄 hash도 OK, 끝나지 않은 continuation은 exit 2 |

### A-P2-04 잔여 — 예외를 판정으로 바꾸면서 모든 결과 형식으로 유출된다

- 위치: `tools/check_versions.py:936`의 `ref_is_pinned`에서 URL 오류를 False로 바꾸는 경로, 991행의 strict URL 검사, `record_ref`의 원 선언 보존.
- 최소 재현은 최초와 같다. `marker = "AK" + "IA" + "A" * 16`으로 합성 표식을 만들고 `"git+https://[" + marker + "]/repo@v1.2.3"`를 requirements의 custom-lib URL로 둔다.
- 양 OS에서 이전 exit 2가 **report exit 0·FLOATING_REF**로 바뀌었지만 표식은 **stdout·JSON·Markdown·step summary 모두 true**다. stderr와 traceback은 없다. 동일 URL을 Poetry manifest git 선언으로 넣고 정상 lock을 주어도 같은 4개 출력에 유출된다.
- 영향: 원 입력의 민감 문자열이 예외 메시지 대신 정상 결과 행으로 복제된다. Poetry lock 파서만 일반 오류로 바꾸는 것으로는 닫히지 않는다.
- 권고: malformed URL을 결과 행 생성 전에 일반화한 입력 오류 2로 차단한다. URL 오류 판정이 원문 출력으로 이어지지 않도록 모든 결과 경로를 시험한다. 합성 표식 원문은 이 보고서와 도구 출력에 기록하지 않았다.

### A-P2-05 잔여 — strict 입력 검사가 문법 오류를 받아들인다

- 위치: `tools/check_versions.py:991`~1019의 `parse_requirement`, 586행의 옵션 집합과 646행의 무조건 제외.
- `fastapi==0.141.1; this is invalid`, `fastapi(((==0.141.1)))`는 양 OS에서 **report exit 0·fastapi OK**다. marker는 비어 있는지만 확인하고, 괄호는 개수·대칭 없이 양끝에서 제거한다.
- 필수 값이 없는 `--only-binary`도 양 OS report exit 0·일반 NO_LOCK만 남는다. 값이 필요한 옵션을 무인자 옵션 집합에 넣었다.
- Windows pip 26.0.1의 Requirement parser는 앞의 두 문장을 거부했고 pip requirements parser는 `--only-binary`를 RequirementsFileParseError로 거부했다. 설치·네트워크는 사용하지 않았다.
- 권고: 지원할 PEP 508 marker·괄호 구조를 검증하거나 해당 문법을 명시적으로 거부한다. 값이 필요한 옵션과 무인자 옵션을 나누어 검사한다. 이 finding은 환경 marker를 평가해 설치 대상을 결정하라는 요구가 아니다.
- 추가 입력의 `--no-index unexpected`는 pip도 무시한다는 반대 대조를 확인했으므로 finding 근거로 사용하지 않았다.

## 새 findings

### A-P2-07 — 따옴표가 있는 정상 include 경로를 찾지 못한다

- 심각도 **P2**, disposition **OPEN**.
- 위치: `tools/check_versions.py:626`~633.
- 최소 재현: `requirements.txt`에 `-r "child name.txt"`를 쓰고 실제 `child name.txt`에는 `mcp>=2`를 둔다. 양 OS에서 exit 2다. `--requirement="child name.txt"`도 동일하다.
- 원인: include 값의 따옴표를 제거하지 않고 파일 이름의 일부로 넘긴다.
- 영향: 존재하는 상대 파일·정상 선언을 누락 파일처럼 거부하여 requirements 재귀 검사가 중단된다.
- 권고: include 옵션의 인자를 shell token 규칙에 맞게 하나의 경로로 읽고 실제 파일 경로에 따옴표를 포함하지 않는다. Windows·Linux의 공백 경로를 함께 검증한다.
- 독립 대조: Windows pip 26.0.1의 `parse_requirements`는 두 입력에서 하위 mcp 선언 1개를 읽었다. 공식 [pip requirements 형식](https://pip.pypa.io/en/stable/reference/requirements-file-format/#referring-to-other-requirements-files), 2026-09-07 조회 근거를 재사용했다.

### A-P2-08 — wildcard와 정확 핀의 유효한 교집합·중복을 거부한다

- 심각도 **P2**, disposition **OPEN**.
- 위치: `tools/check_versions.py:746`~760의 `exact_seen` 검사.
- 최소 재현: `mcp==2.*,==2.1`, 순서를 바꾼 `mcp==2.1,==2.*`, 같은 wildcard를 반복한 `mcp==2.*,==2.*`가 양 OS 모두 **exit 2**다. 같은 정확 핀 `==2.1,==2.1`은 정상 처리한다.
- 원인: 첫 equality/wildcard를 만난 사실 자체를 다음 equality/wildcard의 오류 조건으로 사용해 구간 교집합을 계산하지 않는다.
- 영향: 지원한다고 명시한 wildcard·교집합의 유효한 조합을 입력 오류로 처리한다. 중복이나 선언 순서로 결과가 달라진다.
- 권고: 각 equality/wildcard를 구간으로 바꾸어 기존 하한·상한과 교집합을 계산한다. 같은 조건의 반복은 멱등하게 유지하고 실제 빈 교집합만 정해진 오류로 닫는다.
- 독립 대조: pip 26.0.1의 `SpecifierSet`은 세 문법 모두 2.1을 허용했다. [PyPA 버전 범위의 쉼표 교집합·prefix matching](https://packaging.python.org/en/latest/specifications/version-specifiers/#version-specifiers), 2026-09-07 조회 근거를 재사용했다.

## 재사용·미실행·판정 범위

- **재사용**: 변경 없는 AGENTS·라우터·resume·task·registry·workflow의 이전 대조. `git diff --quiet <delta base> HEAD -- AGENTS.md docs/README.md docs/resume.md versions.json .github/workflows/docs.yml`이 exit 0이며 상세 task는 변경 파일 목록에 없다. 코드·시험·정본 delta와 모든 A 반례는 새로 검토했다.
- **NOT_RUN(독립 원격 CI 미조회)**: 이 candidate의 PR/main/release CI. 로컬 155 tests 성공을 CI 성공으로 세지 않는다.
- **NOT_RUN(실제 소비자 실측 없음)**: ktdm·ktc 고정 원천 재대조, Poetry/pip 설치·빌드·uv 전환. common fixture와 임시 입력만 실행했다.
- **NOT_RUN(범위 밖)**: 전체 pip/Poetry resolver·전체 PEP 440 동등성, consumer write, npm/PyPI 게시, commit·merge·태그·Release 생성.
- 정상 대조: diamond include의 공통 하위 파일 재방문은 순환으로 오인하지 않았다. 실제 순환·누락은 계속 exit 2이며 정확 핀의 파일 수준 NO_LOCK도 유지된다. 기존 npm·uv 회귀는 전체 155 tests 안에서 통과했다.
- `!=` wildcard 구간의 보수적 겹침과 미지원 짧은 index 옵션은 이번 새 finding으로 확대하지 않았다. 보고서에 기록한 수정 범위·입력 문법과 직접 재현된 잔여 오류를 기준으로 **BLOCK**을 확정한다.
