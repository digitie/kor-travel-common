# T-015 세 번째 수정 후 독립 full 리뷰 A 원본

- 실행 ID: `T015-A-POSTFIX03-20260907-081115`.
- 시작/종료 격리 확인: `2026-09-07T08:11:15.4573803+09:00` / `2026-09-07T08:11:50.0343941+09:00`.
- Candidate 및 실제 시작/종료 SHA: `95c139fdea523910fb5f1bdd32f5bae728df2915`.
- Base: `d1c7263de5c3ce930fbcdc234052bc7e98c1d2f1`.
- 격리: `review-t015-a` detached, 시작/종료 `git status --porcelain=v1 --untracked-files=all` 출력 0줄. 자기 원본 외의 파일과 소비자 저장소는 변경하지 않았다.
- 입력: [동일 manifest](2026-09-07-t015-post-fix-03-manifest.md). 이전 확정 원본은 읽었으며 이번 상대 새 결과는 읽거나 요청하지 않았다.
- 범위: 10파일 전체 delta(252줄 추가·15줄 삭제), 규범 변경 두 검증 절 및 기록·누적 finding 회귀.
- 최종 verdict: **PASS**. `A-P1-03`/P1 **FIXED**, 기존 A 2건 FIXED 유지, 새 finding 0건.

## 전달 요청 원문

> T-015 post-fix-03 독립 full 재확인 요청. 동일 manifest F:/dev/kor-travel-common/docs/reviews/adversarial/evidence/2026-09-07-t015-post-fix-03-manifest.md를 따르세요. Candidate 95c139fdea523910fb5f1bdd32f5bae728df2915, base d1c7263de5c3ce930fbcdc234052bc7e98c1d2f1. 기존 review-t015-a worktree를 clean 확인 후 전환했습니다. 규범 delta는 T-109/T-212 두 검증 절뿐이며 다른 파일은 기록입니다. A-P1-03을 원 ID·심각도로 재확인하고 전체 delta 및 누적 finding 회귀를 확인하세요. 출력 소유는 main checkout docs/reviews/adversarial/evidence/2026-09-07-t015-post-fix-03-reviewer-a.md 한 파일입니다. 다른 작업자와 함께 있으니 다른 파일 수정/되돌리기 금지. 이번 상대 결과는 확정 전 읽지 마세요. 변경 없는 정본·코드의 이전 검증은 동일성 확인과 범위 표기로 재사용하고 원본은 새 검증·결론 중심으로 간결히 작성해 주세요. 현재 PR 머지 후 대기, 다음 task 시작 금지입니다.

공통 요청:

> 지정 candidate/base의 독립 full post-fix 리뷰를 수행한다. 자신의 기존 finding과 전체 delta의 회귀를 검토하고 새 원본만 작성한다. 이번 두 원본 확정 전 상대의 새 결과를 읽지 않는다. 실행 ID·시각·요청·실제 hash·clean·검증·미검토·원 ID별 disposition·verdict를 기록한다. 변경되지 않은 배경의 긴 재서술 대신 기존 확정 원본을 연결하며 새 검증과 재사용을 구분한다. 다른 작업자 파일을 고치거나 되돌리지 않는다.

## 새로 실행한 검증

| 명령·검토 | 결과 |
|---|---|
| `git diff --stat <base> HEAD` 및 10개 파일 delta·직전 원본/통합 읽기 | T-109/T-212의 발행 복제 제거와 정본 연결 확인. 나머지는 기록이며 T-015 IN_PROGRESS·병합 후 대기 상태 유지 |
| `python -B -X utf8 tools/validate_document_links.py` | **254문서·2077 로컬 대상**, 오류 0 |
| `python -B -X utf8 tools/validate_plan.py` | **101 tasks**, 오류 0 |
| `git diff --check d1c7263de5c3ce930fbcdc234052bc7e98c1d2f1 HEAD` | exit 0, 출력 없음 |
| `rg`로 AGENTS·README·task·runbook·standards·architecture의 `git tag -a`, `gh release create`, 버전 태그 push 명령 전수 검색 | 실행 명령은 **release runbook에만** 남음. T-109/T-212/T-213에 발행 복제 없음 |
| 두 task의 실제 자산 검사 블록을 UTF-8 bytes로 WSL `bash -n` 전달 | **2블록 구문 통과** |
| 같은 블록을 WSL `bash -s`에서 cd·sha256sum·tar mock 함수로 실행, 뒤에 완료 도달 감시 추가 | **2 task × 4조건 = 8개** 기대 결과. 정상 exit 0; cd 실패·checksum 실패·tar 실패는 exit 1과 완료 도달 없음. cd/checksum 실패에서 tar도 호출되지 않음. 실제 git/gh/파일 mutation 0 |
| `gh pr view 4 --json number,isDraft,state,headRefOid,baseRefName,statusCheckRollup` | [PR #4](https://github.com/digitie/kor-travel-common/pull/4) OPEN·draft·base main·candidate head 일치. [CI 34066138272](https://github.com/digitie/kor-travel-common/actions/runs/34066138272) validate-docs COMPLETED·SUCCESS |

자산 검사는 출력 목록을 상세 tarball 수용 기준과 대조하도록 명시한다. 체크섬/목록 명령 성공만으로 고지·export·설치 시험 전부가 통과했다고 해석하지 않았다.

## 동일성 확인 후 재사용

`git diff --quiet d1c7263de5c3ce930fbcdc234052bc7e98c1d2f1 HEAD -- AGENTS.md docs/adr docs/architecture docs/standards docs/runbooks tools tests versions.json .github`는 exit 0이다.

따라서 [직전 A 원본](2026-09-07-t015-post-fix-02-reviewer-a.md)의 Windows Python 3.14.3 **115 tests/67.390초/skip 0**, WSL Python 3.11.15 **115 tests/29.849초/skip 0**, release의 **8개 bash 구문·14개 발행 mock**, CI 선행 DAG 대조를 재사용했다. 이번 candidate에서 전체 unittest와 변경 없는 runbook mock을 새로 실행한 것으로 집계하지 않았다. source 확인과 과거/현재 원장 전이의 이전 검증은 [앞선 A 원본](2026-09-07-t015-post-fix-reviewer-a.md)에 있으며 관련 정본 변경이 없다.

## 원 finding 재판정과 누적 회귀

| 원 ID·심각도 | Disposition·근거 |
|---|---|
| **A-P1-03 / P1** | **FIXED**. [T-109](../../../tasks/T-109-tokens-v0-1-0-release.md)·[T-212](../../../tasks/T-212-ui-v0-1-0-release.md)의 tag/create/dispatch 복제를 제거했다. release §3.1~3.5의 source 확인·준비 PR merge commit·버전/자산 선택·tag/push/원격 peeled SHA/발행 실패 중단을 명시적으로 연결한다. 두 task에는 실패 즉시 종료하는 자산 확인만 남아 이전 실패 후 발행 경로가 제거됐다. |
| **A-P1-01 / P1** | **FIXED 유지**. 명시 release source·main 전환 제거·PR base 예외 정본 불변. |
| **A-P2-02 / P2** | **FIXED 유지**. T-010a의 T-109a 선행·후보 입력 연결 불변, 새 plan 오류 없음. |

B-P1-01/P1·B-P2-02/P2·B-P2-03/P2·B-P1-04/P1·B-P2-05/P2의 source·0.2 보존·main 원장·발행 중단·CI 선행 계약은 이번 delta로 바뀌지 않았다. B-P1-06/P1과 같은 잔여 경로도 위 두 task에서 제거됐다. 이는 A의 전체 회귀 확인이며 B의 독립 재판정을 대신하지 않는다. 누적 9개 ID를 병합하거나 심각도를 낮추지 않았다.

## 한계와 최종 판정

`NOT_RUN(이번에는 동일성 확인 후 재사용)`: 전체 unittest 재실행·불변 source/발행 mock 재실행. 위 원본의 직접 실행만 증거로 삼았다.

`NOT_RUN(후속 구현/외부 task 범위)`: 실제 package build/install·CI 구현/임시 release branch 실행·후보 tag·Release·소비자 실행. mock은 제품/발행 성공이 아니다. npm/PyPI 조회·예약·게시·재평가는 사용자 제외다. 다음 task 구현은 시작하지 않았다.

**PASS — A의 3개 finding 모두 FIXED, 새 finding 0건.** 현재 PR의 최종 기록·병합은 coordinator 범위이며, 사용자 지시대로 병합 후 대기한다.
