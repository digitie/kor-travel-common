# Phase 0 종료 선행 정정 Reviewer A 독립 재검토 원본

- Review ID: `2026-09-06-phase0-closure-postfix`
- 실행 ID: `/root/reviewer_a` / `phase0-closure-postfix-a-20260906T190512+0900`
- 전문 영역: 도구·CI 실패 gate·task 선행·완료 원장 정합
- 시작: `2026-09-06T19:05:12.1427381+09:00`
- 검토 종료: `2026-09-06T19:05:57.5020183+09:00`
- 요청: [공통 manifest](2026-09-06-phase0-closure-postfix-manifest.md). A-P1-06의 T-009 선행/상태 수정과 전체 작은 종료 delta를 재검토한다. 코드·시험·CI는 불변이며 앞선 전체 시험은 재사용한다.
- Candidate: `fafb3f676e8dd09a5ac384b6f25ffc180e5ba64d`
- Base: `8fb1334381f8fd8d6a3da217244ef2ad136bf020`
- 격리: `F:/dev/kor-travel-common-wt/review-phase0-a` detached worktree. 시작·종료 실제 `git rev-parse HEAD`는 candidate와 같고 `git status --porcelain=v1` 출력은 모두 비었다.
- 독립성: 상대의 이번 원본·finding을 읽거나 요청하지 않았다. 과거 확정 보고서와 이번 공통 manifest만 참조했다. 이 evidence 하나만 작성하고 코드·task·정책·기존 원본·다른 에이전트 변경을 보존했다. 추가 subagent 없음.
- 최종 verdict: **PASS — A-P1-06 FIXED, 신규 finding 없음**.

## A-P1-06 원 reviewer 재확인

[이전 A 원본](2026-09-06-phase0-closure-reviewer-a.md)의 필수 SPDX 도구 선행 누락을 다음과 같이 확인했다.

1. `docs/tasks/T-009-ci-hardening.md` 상단은 `상태: BLOCKED`, `선행: T-002, T-003`이다. 열린 원장의 같은 행도 일치한다.
2. T-003은 READY·선행 없음이고 T-002는 DONE이다. 따라서 T-003의 미완료 SPDX 도구가 T-009의 실제 필수 CI를 막는 관계가 기계 검사 가능한 metadata에 반영됐다.
3. 상세 T-009 evidence는 T-003 DONE 전에 직접 지정받아도 착수하지 않는다고 명시한다. backlog를 생략하는 진입 경로나 차단된 작업을 건너뛰는 선택에서도 이전 READY 오안내가 사라졌다.
4. T-005 전체 완료는 checker 자체 검사의 기술적 선행과 구분하며 기본 실행 대기열 T-003→T-005→T-009는 유지한다. T-005의 CI 연결을 역으로 의존시키는 새 edge가 없어 순환을 만들지 않았다.
5. SPDX 도구를 이미 구현·검증했다고 바꾸거나 필수 Windows CI 수용 기준을 제거하지 않았다. 미완료 도구는 T-003에 남겨 실제 구현을 먼저 요구한다.

따라서 **A-P1-06 FIXED**다. 같은 원인의 B-P2-10 최종 disposition은 해당 원 reviewer가 독립 판정한다.

## 전체 delta와 기존 finding 회귀

이번 delta는 문서 9개, 203 insertions/4 deletions다. T-009의 metadata/해설과 원장, resume, journal, 이전 종료 리뷰 기록만 변경됐다. tools·tests·CI·versions.json은 불변이다.

- 상세 task의 상태 집계는 DONE 6·READY 5·BLOCKED 85이며 합계 96이다. 열린 원장 90행·완료 원장 6행과 일치한다.
- 완료 6개 상세 task와 완료 원장에는 base 대비 diff가 없다. 직전 종료 검토에서 확인한 H1·날짜/PR·evidence 연결이 유지된다.
- resume H2 5개·다음 한 작업 3불릿이 유지되고 다음 작업은 T-003이다. 이번 T-009 정정과 실물/소비자 NOT_RUN을 구분한다.
- journal의 이전 첫 H2부터 끝까지는 base와 정확히 같다. review 변경은 과거 종료 원본/manifest/통합 판정 추가와 색인 행 추가이며 기존 원본을 수정하지 않는다. 통합 판정은 A/B의 다른 심각도를 보존하고 높은 P1에 따른 차단을 기록한다.
- 원 A-P1-01~05와 A-P2-01은 FIXED 유지다. 코드·회귀시험 불변이며 완료 원장 형식도 불변이다. 기존 B finding의 공개 계약·외부 승인·릴리스 순서를 뒤집는 변경은 없다.

## 실제 검증 명령과 결과

| 명령·검사 | 결과 |
|---|---|
| `python -B -X utf8 tools/validate_document_links.py` | exit 0, 문서 209개·local target 1770개·오류 0 |
| `python -B -X utf8 tools/validate_plan.py` | exit 0, 상세 task 96개·오류 0; 제품 gate 아님 |
| `git diff --check 8fb1334381f8fd8d6a3da217244ef2ad136bf020 HEAD` | exit 0, 출력 없음 |
| `git diff --quiet 8fb1334381f8fd8d6a3da217244ef2ad136bf020 HEAD -- tools tests .github versions.json` | exit 0, 구현·시험·CI·레지스트리 불변 |
| 완료 원장과 T-001·002·004·007·008·013 상세를 지정한 `git diff --quiet <base> HEAD -- <각 경로>` | exit 0, 완료 기록 불변 |
| Python `pathlib`·`re`·`Counter`로 task·원장·resume 구조 대조 | T-009 BLOCKED/T-002,T-003 선행, 상태 6/5/85, 원장 90/6행, resume 5절/3불릿; assertion 성공 |
| `git show <base>:docs/journal.md`와 candidate의 이전 본문 비교 | 이전 기록 보존; assertion 성공 |
| `git diff --name-status <base> HEAD -- docs/reviews` | 이전 종료 report·manifest·두 원본 추가와 색인 수정만 존재 |

로컬 전체 unittest와 새 WSL 검사는 **NOT_RUN(코드·시험·CI 불변과 manifest 재사용 허용)**이다. [postfix-02 A 원본](2026-09-06-phase0-postfix-02-reviewer-a.md)의 Windows Python 3.14.3·WSL Python 3.14.4 각각 67 tests/skip 0 결과를 재사용하며 이번 로컬에서 새로 실행한 수치로 세지 않는다.

## PR·리모트·CI 직접 확인

`gh pr view 1 --json number,isDraft,state,headRefOid,headRefName,baseRefName,statusCheckRollup`, `gh pr view 1 --json body`, `gh run view 34026385095 --json databaseId,headSha,status,conclusion,url`, `gh run view 34026385095 --log`, `git ls-remote origin refs/heads/feat/bootstrap-survey-and-integration-plan`을 읽기 전용 실행했다.

- [PR #1](https://github.com/digitie/kor-travel-common/pull/1): OPEN·draft, base main. head와 remote branch는 모두 candidate `fafb3f676e8dd09a5ac384b6f25ffc180e5ba64d`다.
- PR 본문은 이번 선행 수정의 재확인 중 상태, 해당 CI, 완료 6개·열린 90개·다음 T-003·후속 T-005→T-009 및 NOT_RUN을 일치하게 기록한다.
- [CI run 34026385095](https://github.com/digitie/kor-travel-common/actions/runs/34026385095): candidate head, completed/success, validate-docs 성공. 완료 시각 `2026-09-06T10:04:22Z`.
- 실제 CI 로그: 문서 209개·target 1770개·오류 0, task 96개·오류 0, `Ran 67 tests in 1.862s`, `OK`. 개별 `... ok` 67개·`... skipped` 0개를 직접 집계했다. 로컬 재사용 수치와 구분되는 해당 candidate의 원격 실행이다.

## 한계와 최종 판정

신규 finding, OPEN 또는 DEFERRED 없음. A-P1-06을 포함한 A finding 7건은 FIXED 또는 FIXED 유지다. 이번 기준선에서 종료 기록을 추가 수정할 요구는 없다.

패키지 build·pack/wheel·소비자 build/e2e/시각·권리 승인·릴리스는 **NOT_RUN(실물·소비자 실행 없음, 이번 문서 종료 범위 밖)**이다. 이 PASS는 Phase 0 전체 완료·소비자 gate 통과·릴리스 허가를 뜻하지 않는다.

두 원본·통합 판정·색인만 추가할 후속 closure artifact commit의 최종 SHA/CI/PR 동기화는 **NOT_RUN(두 reviewer 확정 후 coordinator 수행)**이다. 규범 변경이 포함되면 이번 판정을 재사용할 수 없다. **Candidate 한정 PASS**.
