# T-005 수정 후 독립 적대적 리뷰 B 원본

- 실행 ID: `B-T005-PF-20260907-072202-f050997`
- 시작: `2026-09-07T07:22:02.7821437+09:00`
- 종료 검증: `2026-09-07T07:25:42.3002186+09:00`
- Candidate 및 실제 시작·종료 SHA: `f0509970b291a4e1f30ac5499150953ca80ab447`
- Base: `3bec3eb0d17b986a9140c4f8ba876beb596d560a`. 최초 candidate `409b95c692c073807906e2c1546f022c59a7499c`와 `git diff --quiet` 결과 exit 0으로 트리 동일성을 직접 확인했다.
- 격리: `review-t005-b` detached worktree. 시작·종료 `git status --porcelain=v1` 출력 0줄. 기준선·snapshot·소비자·제품·다른 원본을 수정하지 않았다. 고장 주입은 메모리에서 수행했다.
- 입력: [공통 manifest](2026-09-07-t005-post-fix-manifest.md), [최초 B 원본](2026-09-07-t005-reviewer-b.md), 원본이 확정된 최초 통합 finding. 상대의 이번 수정 후 원본·결과는 읽지 않았다.
- 범위: 13파일 전체 delta(578줄 추가·47줄 삭제), 기존 B finding 세 건과 정책·차단·예외·CLI·evidence 중심 회귀. 코드·시험·정책 수정과 기록·인계 상태를 함께 대조했다.
- 최종 verdict: **PASS**. 기존 `B-P1-01`·`B-P1-02`·`B-P2-03`은 원 심각도를 유지하여 모두 **FIXED**로 확인했다. 새로운 finding은 없다. 이 판정은 해당 candidate의 T-005 수정 검토이며 소비자 정책 준수·제품 빌드·배포 성공을 뜻하지 않는다.

## 전달 요청 원문

> T-005 full post-fix 리뷰 B를 진행하세요. 동일 manifest F:/dev/kor-travel-common/docs/reviews/adversarial/evidence/2026-09-07-t005-post-fix-manifest.md. candidate f0509970b291a4e1f30ac5499150953ca80ab447, base 3bec3eb0d17b986a9140c4f8ba876beb596d560a(최초409와 동일 트리). 기존 detached F:/dev/kor-travel-common-wt/review-t005-b를 candidate로 옮겼습니다. 자신의 3개 최초 ID 원 심각도로 재확인하고 전체 delta 회귀도 검토. 우선 정책/차단/예외/CLI/evidence. 다른 reviewer 새 결과는 읽지 마세요. 코드 수정 금지, 자신의 새 원본 F:/dev/kor-travel-common/docs/reviews/adversarial/evidence/2026-09-07-t005-post-fix-reviewer-b.md만 작성. ID/시각/전달원문/SHA/clean/명령/검증/한계/기존disposition/새finding/verdict 포함. 실제 입력과 원천 목록은 기존 .git/codex-audit/t005-snapshots 및 t005-inputs.json 읽기 전용. 다른 작업자가 있으므로 타인 편집을 되돌리지 마세요. 소비자 저장소 쓰기 금지. 115 tests 성공을 믿고 공격을 생략하지 마세요.

## 기존 finding disposition과 재현

| 원 ID·심각도 | 수정 위치 | 직접 재확인 | Disposition |
|---|---|---|---|
| B-P1-01 · P1 | [check_versions.py](../../../../tools/check_versions.py) `installed_version` 78행, `blocked_name` 422행, `record_blocked` 634행 | 축에 없는 차단 전용 패키지도 해석 실패 시 NO_LOCK을 만든다. 지원 npm 실제 main 호출과 현재 PyPI 공통 차단 경로에서 정상·비차단·미지원·깨진 값·빈 값을 대조했다. 아래 10개 경계 모두 기대와 일치 | **FIXED** |
| B-P1-02 · P1 | 같은 파일 `Registry.load` 373~376행 | `>=2.1.1.0.0` 자체 검사 main 반환 2. `>=2.1.1.0`·`>=2.1.1`·`>=2`·`>=3`은 반환 0이며 실제 2.1.1 차단 비교가 각각 True·True·True·False. 자체 검사와 실행 숫자 파서의 불일치 해소 | **FIXED** |
| B-P2-03 · P2 | 같은 파일 `Registry.load` 349~352행 | 예외 reason/review 각각 `"   "`와 `" \t "`를 넣은 네 경우 main 반환 2. 두 필드 각각 정상 한국어 사유·task 문자열을 넣은 대조군은 반환 0. 공백만 있는 필수 근거로 EXEMPT를 승인할 수 없음 | **FIXED** |

B-P1-01의 npm 재현은 최초와 같은 방법이다. 현재 registry를 메모리 복제하여 기존 mcp 차단 항목만 npm 생태계로 옮기고 airport enforce를 fail로 바꿨다. 정상 node/npm engines와 `mcp >=1` 선언, lockfileVersion 3의 `node_modules/mcp`가 있는 manifest/lock의 읽기만 메모리로 대체했다. 실제 `main()`을 호출했으며 snapshot 파일은 바꾸지 않았다. 비차단 대조군도 만들기 위해 선언 범위의 하한만 최초 재현보다 낮췄다.

| 입력 경로 | 설치 문자열 | 관찰된 mcp 판정 | fail 반환 |
|---|---|---|---:|
| npm CLI | `2.1.1` | BLOCKED | 1 |
| npm CLI | `1.9.0` | 차단 행 없음 | 0 |
| npm CLI | `2.1.1-rc.1` | NO_LOCK | 1 |
| npm CLI | `broken` | NO_LOCK | 1 |
| npm CLI | 빈 문자열 | NO_LOCK | 1 |
| 현재 registry의 PyPI 공통 차단 함수 | `2.1.1` | BLOCKED | 1 |
| 현재 registry의 PyPI 공통 차단 함수 | `1.9.0` | 차단 행 없음 | 0 |
| 현재 registry의 PyPI 공통 차단 함수 | `2.1.1rc1` | NO_LOCK | 1 |
| 현재 registry의 PyPI 공통 차단 함수 | `broken` | NO_LOCK | 1 |
| 현재 registry의 PyPI 공통 차단 함수 | 빈 문자열 | NO_LOCK | 1 |

PyPI 행은 `Checker.record_blocked()`와 `exit_code()`를 직접 호출한 공통 로직 검사다. 이를 uv 파서 전체 재검증으로 표시하지 않는다. 기존 결함의 영향과 권고는 [최초 원본](2026-09-07-t005-reviewer-b.md)에 보존했다. 이번 후보에서는 세 원인이 해소되어 추가 수정 권고가 없다.

## 실행 명령과 전체 회귀

| 명령·검증 | 실제 결과 |
|---|---|
| `git diff --quiet 409b95c692c073807906e2c1546f022c59a7499c 3bec3eb0d17b986a9140c4f8ba876beb596d560a` | exit 0, 재배치된 base가 최초 검토 트리와 동일 |
| `git diff --numstat 3bec3eb0d17b986a9140c4f8ba876beb596d560a..HEAD` 및 코드·시험·문서 delta 읽기 | 13파일. npm 이름·링크·전이 선언/resolved·build metadata·제한된 런타임 범위·strict 정책 변경을 정본과 대조 |
| `py -3 -B -X utf8 -m unittest discover -s tests -p 'test_*.py'` | Windows Python 3.14.3, **115 tests 성공·skip 0**, 14.687초, exit 0 |
| `py -3 -B -X utf8 tools/check_versions.py --self-check --today 2026-09-07` | 정상 registry exit 0 |
| 실제 main에 기준일 2026-12-31 / 2027-01-01 전달 | 마지막 유효일 반환 0·만료 annotation 0개, 다음 날 반환 1·EXEMPT_EXPIRED 12개 |
| `py -3 -B -X utf8 tools/check_spdx.py` | 13개 파일, 오류 0, exit 0 |
| `py -3 -B -X utf8 tools/validate_document_links.py` | 232개 문서, 1924개 로컬 target, 오류 0, exit 0 |
| `py -3 -B -X utf8 tools/validate_plan.py` | 상세 task 96개, 오류 0, exit 0. metadata/DAG 검사이며 제품 gate 아님 |
| `git diff --check 3bec3eb0d17b986a9140c4f8ba876beb596d560a..HEAD` | 출력 없음, exit 0 |
| base→candidate `git diff --quiet`로 versions.json·inputs.json·reports.json·docs.yml 대조 | exit 0. 정책 수치·예외·강제 수준·최초 실측 원본·자체 검사 CI 불변 |
| 표준 입력 Python으로 10판정 × 3모드 `exit_code`·`annotations` 대조 | **30조합 일치**. HARD 3종은 report에서도 error, fail 실패 후보 7종은 반환 1, NOT_RECOMMENDED는 반환 0·warn/fail warning |
| 표준 입력 Python으로 `Registry.load`·실제 `main` 메모리 고장 주입 | 기존 B 세 finding의 위 경계와 정상 대조군 확인. 파일 출력·소비자 쓰기 없음 |
| `gh pr view 3 --json number,isDraft,state,headRefOid,statusCheckRollup,url` | [PR #3](https://github.com/digitie/kor-travel-common/pull/3) OPEN·draft, head f050997 일치. [CI run 34063775506](https://github.com/digitie/kor-travel-common/actions/runs/34063775506)의 validate-docs COMPLETED·SUCCESS 직접 확인 |
| 종료 `git rev-parse HEAD`·`git status --porcelain=v1` | candidate 유지·clean |

추가된 회귀 시험과 실제 코드에서 전이 링크의 정책 축/차단 대상 NO_LOCK, 전이 branch 선언이 resolved SHA에 가려지지 않는 처리, npm 이름과 Python 이름 정규화 분리, 빈 런타임 교집합/미지원 연산자의 NO_ENGINES, 안정 npm build metadata 처리를 확인했다. 해당 문법의 한계는 versions §8 및 전이 npm 참조 절과 일치한다. 사설 registry/mirror와 전체 SemVer 지원을 성공 범위로 확대하지 않았다.

상태 문서는 T-005를 IN_PROGRESS로 유지하고 두 reviewer 재확인을 출구로 남겼다. npm/PyPI 미게시 사용자 지시는 후속 계획 정리로 기록했으며 이 후보가 후속 task 정리를 완료했다고 주장하지 않는다. 최초 리뷰 원본·통합 기록과 새 코드 digest를 분리한 인계가 실제 변경과 일치한다.

## 고정 입력과 보고서 재생성

`py -3 -B -X utf8 -` 표준 입력 스크립트로 [inputs.json](../../../evidence/t005/inputs.json)의 7개 정식 repo/commit을 비공개 입력 목록과 매핑했다. snapshot 48파일의 실제 바이트 SHA-256이 전부 일치했다. 각 snapshot에 현재 후보의 `discover` → `Checker.run` → `build_report`를 실행했고, 최초 방식과 같이 report의 `registry.path`·`roots`만 정규화하여 [reports.json](../../../evidence/t005/reports.json) 전체 객체와 비교했다. 요약만 비교한 것이 아니며 모든 findings 필드도 동일하다. 각 입력에 실제 `main([snapshot, '--registry', registry, '--repo', repo, '--today', '2026-09-07', '--quiet', '--no-step-summary'])`도 별도로 호출했다.

| 고정 입력 | 파일 | 판정 행 | fail 기준 위반 행 | 원본 전체 일치·CLI |
|---|---:|---:|---:|---|
| airport bb47f107 | 4 | 24 | 2 | 일치·0 |
| concierge 7945305d | 8 | 38 | 23 | 일치·0 |
| docker-manager 862562dc | 3 | 18 | 10 | 일치·0 |
| geo 1d9d74d3 | 4 | 44 | 25 | 일치·0 |
| map c494e227 | 8 | 67 | 26 | 일치·0 |
| weather 6003da99 | 7 | 42 | 2 | 일치·0 |
| pinvi 9af25e58 | 14 | 73 | 14 | 일치·0 |
| 합계 | **48** | **306** | **102** | **7개 일치·report 실행 7개** |

[post-fix.json](../../../evidence/t005/post-fix.json)의 네 digest를 LF·UTF-8로 독립 재계산했다. checker `aa4e1dbec1e42f5ad6bcbfa961d837ccf7bd0239156db1664b14a678e9cd7b93`, registry `dc608f881e93b93500e71e64df6ddee25e58ab0cf3f0f8f9715d2999284e361a`, inputs `481306dfb06228b8e8dd299744653bf68e0c88cd4ef5f28fdf7b0811937ae8d6`, reports `bad711219c47195744c4add91c19fe6987fb4da84c90a78fc386a527120d7fed` 모두 일치했다.

고정 Git object 48파일과 탐색 대상 누락 검사는 최초 B 원본의 실제 검증을 재사용했다. 그 입력/보고 파일이 base부터 변하지 않았고 이번 snapshot 바이트도 모두 일치함을 확인했다. airport 현재 HEAD나 dirty 파일은 사용하지 않았다. 소비자 전부 report 모드이며 반환 0을 clean run으로 계산하지 않는 evidence 설명을 유지한다.

## 미검증과 판정 경계

- `NOT_RUN(이번 reviewer는 Windows Python 3.14.3 사용)`: WSL Python 3.11.15 독립 재실행. post-fix.json의 WSL 결과는 작성자 evidence이며 이번 Windows 115 tests와 합산하지 않았다. 원격 CI 성공은 별도로 조회했다.
- `NOT_RUN(소비자 저장소 실행·범위 밖)`: npm ci·uv sync·제품 빌드·e2e·소비자 CI·배포. 고정 lock의 읽기 전용 대조는 설치나 런타임 성공의 증거가 아니다.
- `NOT_RUN(후속 task)`: T-005a uv marker/workspace 전체 해석, T-005b Poetry/requirements 잠금 파서, T-011 정식 manifest 스키마, T-009 전체 CI 하드닝. 이번 후보가 이 항목들을 완료했다고 판정하지 않았다.
- `NOT_RUN(사용자 범위 밖)`: npm·PyPI 게시. 전체 SemVer/PEP 440 해석기 및 사설 registry 지원 확대도 검토 완료 범위가 아니다.
- 새 원본 한 파일만 주 checkout에 작성했다. 상대 reviewer의 이번 결과를 보지 않고 **PASS**를 독립 확정했으며, 다른 reviewer의 finding 유무와 최종 merge 판단은 이 원본으로 대신하지 않는다.
