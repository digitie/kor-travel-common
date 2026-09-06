# Phase 0 문서 task 종료 Reviewer A 독립 재검토 원본

- Review ID: `2026-09-06-phase0-closure`
- 실행 ID: `/root/reviewer_a` / `phase0-closure-a-20260906T185656+0900`
- 전문 영역: validator·CI·실패 gate·완료 원장 및 evidence 정합
- 시작: `2026-09-06T18:56:56.1959598+09:00`
- 검토 종료: `2026-09-06T19:01:06.0121137+09:00`
- 요청: [공통 closure manifest](2026-09-06-phase0-closure-manifest.md). 6개 DONE/H1/archive/evidence, T-003·T-009 READY, resume 다음 작업, 정본 서두의 상태 동기화와 전체 종료 delta 회귀를 검토한다. 새 구현·설계는 범위 밖이며 기존 67 tests를 재사용할 수 있다.
- Candidate: `8fb1334381f8fd8d6a3da217244ef2ad136bf020`
- Base: `56706423bf9948909e872aa9a76229666984d289`
- 격리: `F:/dev/kor-travel-common-wt/review-phase0-a` detached worktree. 시작·종료의 실제 `git rev-parse HEAD`는 위 candidate와 같고 `git status --porcelain=v1` 출력은 모두 비었다.
- 독립성: 상대의 이번 closure 원본·finding은 읽거나 요청하지 않았다. 이전에 이미 확정한 postfix-03의 두 원본과 통합 판정은 이번에 추가된 이력의 대조에 사용했다. 이 원본 파일만 main evidence에 작성하고 코드·기존 원본·다른 에이전트 변경을 보존했다. 추가 subagent를 생성하지 않았다.
- 최종 verdict: **BLOCK — A-P1-06 OPEN**. 기존 A finding 6건은 FIXED 유지다. 최초 원본 초안 작성 뒤 제출 전에 coordinator가 T-009의 도구 선행을 확인해 달라는 질문을 보냈다. 상대 reviewer 결과를 전달받지 않았으며 아래 문서·실제 명령을 다시 확인해 독립 판정했다.

## 범위와 내용 판정

base→candidate는 문서 31개, 242 insertions/54 deletions다. 완료 요약·상세 task·정본 머리말·resume·journal과 직전 확정 리뷰의 추가 기록을 검토했다. 완료 수용 기준 자체의 내용 검토는 [직전 A 원본](2026-09-06-phase0-postfix-03-reviewer-a.md)을 재사용하며, 이번에는 그 판정과 실제 종료 기록이 연결됐는지를 확인했다.

| 대상 | 이번 종료 delta 판정 |
|---|---|
| T-001 | 상세 DONE·H1 날짜/PR과 완료 원장 제목 일치. 진입 문서의 리뷰 전 표기가 문서 확정으로 바뀌었고 실제 통합 리뷰 링크가 연결됨 |
| T-002 | 상세 DONE·H1/원장 일치. Windows/WSL 67 tests의 기준선과 새 CI를 구분할 수 있는 실제 report 연결. 코드·시험·CI 불변 확인. CI 매트릭스·SHA 핀은 T-009 잔여로 유지 |
| T-004 | 상세 DONE·H1/원장 일치. ADR 13편·색인 14파일·다음 014의 기존 검증과 실제 리뷰 연결. ADR-012 사용자 승인 대기는 그대로 유지 |
| T-007 | 상세 DONE·H1/원장 일치. runbook 서두는 문서 초기판/확정 범위로 정리되고 실물 명령 대조·최초 릴리스·소비자 적용 후속 gate는 남음 |
| T-008 | 상세 DONE·H1/원장 일치. architecture·채택 지도는 설계 초기판이며 실물 대조·생성기 전환·소비자 gate를 완료로 확대하지 않음 |
| T-013 | 상세 DONE·H1/원장 일치. 다음 T-003, 후속 T-005→T-009가 resume·원장·PR 본문에서 같음. 검토 candidate와 실제 PR head·remote branch·성공 CI가 일치 |
| T-003 | 선행 없음으로 READY가 metadata/DAG와 일치. LICENSES 원문·SPDX 도구·음성 fixture는 NOT_RUN(잔여)로 명시 |
| T-009 | metadata 검사에서는 READY가 허용되지만 필수 CI가 T-003의 미구현 도구를 실행해야 한다. 숨은 선행 A-P1-06이 남으므로 실행 가능한 순차 인계의 종료 gate는 닫히지 않음 |

Python 메모리 내 대조에서 상세 96개의 상태는 DONE 6·READY 6·BLOCKED 84이며 IN_PROGRESS는 없다. 열린 원장 90행, 완료 원장 6행이다. DONE ID는 T-001·T-002·T-004·T-007·T-008·T-013뿐이며, 각 상세 H1의 `(2026-09-06, PR #1)`과 완료 요약 제목, 실제 통합 report 링크를 직접 확인했다. resume는 H2 5개, 다음 한 작업 3불릿이다.

이전 가상 보고서 경로는 실제 [postfix-03 통합 판정](../2026-09-06-phase0-post-fix-03.md)과 리뷰 색인으로 바뀌었다. 그 통합 판정은 검토 SHA·두 원본·명령·CI·NOT_RUN을 연결하며 이번 종료 delta를 별도로 확인한다고 명시한다. 과거 원본의 덮어쓰기는 없고, review diff는 직전 원본/manifest/통합 report 추가와 색인 행 추가뿐이다. journal의 이전 첫 H2부터 끝까지가 base와 정확히 같음을 확인했다. survey diff도 없다.

## 실제 검증 명령과 결과

Windows 실행기는 `python --version` 결과 Python 3.14.3이다. 모든 로컬 검증은 위 detached checkout에서 수행했다.

| 명령·검사 | 결과 |
|---|---|
| `python -B -X utf8 tools/validate_document_links.py` | exit 0, 문서 205개·local target 1757개·오류 0 |
| `python -B -X utf8 tools/validate_plan.py` | exit 0, 상세 task 96개·오류 0; 제품 gate 아님 |
| `git diff --check 56706423bf9948909e872aa9a76229666984d289 HEAD` | exit 0, 출력 없음 |
| `git diff --quiet 56706423bf9948909e872aa9a76229666984d289 HEAD -- tools tests .github` | exit 0, 코드·시험·CI 변경 없음 |
| `git diff --quiet 56706423bf9948909e872aa9a76229666984d289 HEAD -- docs/survey` | exit 0, 조사 스냅샷 변경 없음 |
| Python `pathlib`·`re`·`collections.Counter`로 metadata/H1/원장/evidence/resume 대조 | 위 96개 상태·90/6행·DONE 제목·실제 report 링크·5절/3불릿 확인, assertion 실패 없음 |
| `git show <base>:docs/journal.md`와 candidate의 과거 본문 비교 | 이전 기록 보존, assertion 성공 |
| 완료 task의 `IN_PROGRESS`·`2인 리뷰 전` 잔존 표기 `rg` 검사 | 대상 정본·resume·열린 원장에서 일치 없음; rg exit 1은 검색 결과 없음 |
| `python -B -X utf8 tools/check_spdx.py` | exit 2, 파일 없음. T-009 필수 도구가 아직 실행 불가능함을 재현 |
| `python -B -X utf8 tools/check_versions.py --self-check` | exit 0, 레지스트리 자체 검사 성공; 소비자 버전 검사는 실행하지 않음 |

로컬 전체 unittest와 WSL 반복 검사는 **NOT_RUN(이번 문서 종료 delta에서 코드·시험·CI가 같고 재사용 허용)**이다. [postfix-02 A 원본](2026-09-06-phase0-postfix-02-reviewer-a.md)의 Windows Python 3.14.3·WSL Python 3.14.4 각각 67 tests/skip 0 결과를 재사용했다. 이번 로컬에서 67개를 새로 실행했다고 세지 않는다.

## PR·리모트·CI 직접 확인

`gh pr view 1 --json number,url,isDraft,state,headRefName,headRefOid,baseRefName,body,statusCheckRollup`, `gh run view 34025999506 --json databaseId,headSha,status,conclusion,event,url,name,jobs`, `gh run view 34025999506 --log`, `git ls-remote origin refs/heads/feat/bootstrap-survey-and-integration-plan`을 읽기 전용으로 실행했다.

- [PR #1](https://github.com/digitie/kor-travel-common/pull/1): OPEN, `isDraft=true`, base `main`, head branch `feat/bootstrap-survey-and-integration-plan`, head SHA는 candidate와 일치한다. `ls-remote`의 같은 branch SHA도 candidate다.
- PR 본문은 완료 6개·열린 90개·다음 T-003·후속 T-005→T-009와 package/consumer NOT_RUN을 명시한다. 이번 종료 candidate의 두 reviewer 검토는 진행 중으로 구분하며 이미 PASS라고 쓰지 않는다.
- [CI run 34025999506](https://github.com/digitie/kor-travel-common/actions/runs/34025999506): event `pull_request`, head SHA candidate, `completed/success`, validate-docs와 각 실제 검사 step 성공. 완료 시각은 `2026-09-06T09:55:52Z`다.
- CI 로그는 문서 205개·target 1757개·오류 0, task 96개·오류 0, `Ran 67 tests in 1.780s`, `OK`를 출력했다. 로그의 개별 `... ok` 67개·`... skipped` 0개도 직접 집계했다. 이는 candidate의 원격 실행 결과이며 로컬 재사용 결과와 구분한다.

## 새 finding: A-P1-06 — T-009 READY에 필수 SPDX 도구 선행 누락

- 위치: `docs/tasks/T-009-ci-hardening.md` 3·6행(READY, 선행 T-002), 21행(구현 범위), 39행(Windows CI 수용 기준); `docs/tasks.md`의 T-009 READY 행.
- 근거: T-009는 Windows `tools` job에서 `check_spdx` 성공을 필수로 요구한다. 그 도구와 음성 fixture의 소유는 T-003이고, T-003 67행은 미완료라고 기록한다. candidate의 `tools/check_spdx.py`는 실제로 없다. 해당 명령은 exit 2지만 `validate_plan.py`는 현재 metadata만 보고 오류 0을 반환한다.
- 실패 시나리오: T-003이 원문 조회 등으로 막혔을 때 통합 계획 §2.4와 실행 대기열은 독립적인 다음 READY 항목으로 넘어가도록 한다. T-009가 READY이므로 이를 선택할 수 있지만, 완료하려면 다른 task 소유 도구를 대신 구현하거나 필수 CI를 빼거나 다시 중단해야 한다. 순서 문장만으로 실제 선행 관계가 보존되지 않는다.
- 영향: 원장의 실행 가능 상태와 실제 필수 CI gate가 불일치한다. T-013의 실행 가능한 순차 인계 완료 주장을 유지할 수 없다.
- 최소 수정: T-009 상세와 원장에 T-003을 선행으로 명시하고 현재 상태를 BLOCKED로 되돌린다. 수정 후 원장/DAG/관련 인계 표현을 확인하고 새 immutable candidate에서 두 reviewer가 재확인한다.
- T-005 경계: `check_versions.py --self-check`는 지금도 실제 exit 0이다. T-009가 현재 부분 구현으로 report/자체 검사 CI를 붙이는 데 T-005의 소비자 7곳 보고 전체 완료가 기술적으로 필수라고 단정할 근거는 부족하다. 최소 수정에 T-005를 무조건 더하지 않는다. T-005 DONE을 CI task 선행으로 강제하려면 T-005 수용 기준의 `docs.yml 또는 T-009` 자체 검사 연결을 T-005가 먼저 제공하는 경로로 명확히 해 순환을 피해야 한다. 현재 확실한 결함은 T-003 누락이다.
- Disposition: **OPEN**. 검토자는 코드·task·정책을 수정하지 않았다.

## 기존 finding과 한계

| 원 A finding | 이번 disposition |
|---|---|
| A-P1-01 설치 버전 파싱 실패 | FIXED 유지 — 소스·음성 fixture 불변, candidate CI의 회귀시험 성공 |
| A-P1-02 빈 scope 성공 | FIXED 유지 — 소스·fixture 불변, 입력 오류를 성공으로 바꾸는 문서 delta 없음 |
| A-P1-03 하한 없는 OR | FIXED 유지 — 코드·회귀시험 불변 |
| A-P1-04 registry 정책 오타 | FIXED 유지 — 코드·회귀시험 불변 |
| A-P1-05 npm/Python/uv ref 문맥 | FIXED 유지 — 코드·회귀시험 불변 |
| A-P2-01 완료 원장 제목 | FIXED 유지 — 이번 실제 6개 DONE 이동에서 상세 H1·완료 제목·날짜/PR과 plan 검사 모두 일치 |

기존 B finding과 B-P2-09를 뒤집는 계약·선행·문서 입력 지침 변경은 없다. 별도의 A-P1-06이 OPEN이며 DEFERRED는 없다. 패키지 build·tarball/wheel 설치·소비자 build/e2e/시각·외부 승인·릴리스는 **NOT_RUN(이번 종료 기록의 범위 밖이며 실물·소비자 실행 없음)**이다. 성공한 문서 검사·CI는 새 계획 finding을 해소하지 않는다.

후속 종료 기록 commit은 아직 존재하지 않아 그 SHA/CI/PR 동기화는 **NOT_RUN(후속 수정·재검토 뒤 coordinator 수행)**이다. A-P1-06은 task 선행·상태 수정이 필요하므로 review 원본/통합/index만 추가하는 closure artifact 예외로 닫을 수 없다. **현재 candidate는 BLOCK**이다.
