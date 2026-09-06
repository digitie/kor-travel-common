# T-015 두 번째 수정 후 독립 full 리뷰 A 원본

- 실행 ID: `T015-A-POSTFIX02-20260907-080359`.
- 시작: `2026-09-07T08:03:59.9530469+09:00`.
- 종료 격리 확인: `2026-09-07T08:06:05.0504985+09:00`.
- Candidate 및 실제 시작/종료 HEAD: `d1c7263de5c3ce930fbcdc234052bc7e98c1d2f1`.
- Base: `ae86185ff103156ffd516b572cf97d401f4a3d31`.
- 격리: `review-t015-a` detached worktree, 시작/종료 porcelain 출력 0줄. 제품·소비자·다른 파일을 수정하지 않았다.
- 입력: [동일 manifest](2026-09-07-t015-post-fix-02-manifest.md), 확정된 이전 A/B 원본·통합 report.
- 전문 영역: 정보 정본·에이전트 실행 가능성·DAG·CI 선행. 14개 전체 delta와 누적 finding의 회귀를 검토했다.
- 독립성: 이번 상대 reviewer의 새 원본·finding은 읽거나 요청하지 않았다. 새 원본 한 파일만 작성한다.
- 최종 verdict: **BLOCK**. 자신의 기존 `A-P1-01`/P1·`A-P2-02`/P2는 **FIXED 유지**. 새 `A-P1-03`/P1 **OPEN**.
- 사용자 범위: PR #4 검증·병합 후 대기. 이 리뷰에서 다음 task 구현은 시작하지 않았다.

## 전달 요청 원문

> T-015 두 번째 post-fix 독립 full 리뷰를 수행해 주세요. 공통 manifest F:/dev/kor-travel-common/docs/reviews/adversarial/evidence/2026-09-07-t015-post-fix-02-manifest.md를 읽고 따르세요. Candidate d1c7263de5c3ce930fbcdc234052bc7e98c1d2f1, base ae86185ff103156ffd516b572cf97d401f4a3d31. 기존 worktree F:/dev/kor-travel-common-wt/review-t015-a는 clean 확인 후 candidate detached로 전환했습니다. 시작·종료 SHA/clean을 직접 확인하세요. A 영역은 정보 정본·agent 실행 가능성·DAG·CI 선행이며 전체 14파일 delta와 누적 finding 회귀도 검토합니다. 이전 두 원본은 확정되어 열람 가능합니다. 이번 상대 새 결과는 읽지 마세요. 출력 소유 파일은 main checkout docs/reviews/adversarial/evidence/2026-09-07-t015-post-fix-02-reviewer-a.md 한 개입니다. 다른 작업자가 함께 있으니 다른 파일 변경/되돌리기 금지. 실제 검증과 미실행을 분리하고 원 ID/심각도를 보존해 최종 판정하세요. 현재 사용자 요청은 PR #4 머지 후 대기이며 다음 task 구현은 범위 밖입니다.

공통 요청:

> 위 candidate/base에서 독립 full post-fix 적대적 리뷰를 수행한다. 기존 finding은 원 ID·심각도로 재판정하고 전체 수정에서 새 회귀를 찾는다. 다른 작업자의 변경을 고치지 말고 지정한 새 reviewer 원본 파일만 작성한다. 실행 ID·시각·전달 입력·실제 SHA·clean·검증 명령과 결과·미검토·finding disposition·BLOCK/CONDITIONAL/PASS를 남긴다. 상대 reviewer의 이번 새 결과는 읽지 않는다. 원본 마지막에는 개행 하나만 둔다.

## 직접 검증과 범위

release·ci-deploy·T-009/015/101/213/302의 변경, journal·resume·리뷰 색인·직전 manifest/두 원본/통합 report를 모두 대조했다. 최초 정본·후보/source·원장 분리 검토는 [직전 A 원본](2026-09-07-t015-post-fix-reviewer-a.md)에 보존돼 있으며, 이번 변경과 연결되는 실제 발행 명령과 CI 선행을 추가로 공격했다.

| 명령·검증 | 실제 결과 |
|---|---|
| 시작/종료 `git rev-parse HEAD`·`git status --porcelain=v1 --untracked-files=all` | candidate 일치, clean |
| `git diff --stat ae86185ff103156ffd516b572cf97d401f4a3d31 HEAD` 및 전체 경로별 diff | 14파일, 299줄 추가·23줄 삭제 |
| Windows Python 3.14.3: `python -B -X utf8 -m unittest discover -s tests -p 'test_*.py'` | **115 tests**, 67.390초, OK, skip 0, exit 0 |
| WSL Python 3.11.15: `uv run --no-project --python 3.11 python -B -X utf8 -m unittest discover -s tests -p 'test_*.py'` | **115 tests**, 29.849초, OK, skip 0, exit 0 |
| `python -B -X utf8 tools/validate_document_links.py` | **250문서·2052 로컬 대상**, 오류 0 |
| `python -B -X utf8 tools/validate_plan.py` | **101 tasks**, 오류 0 |
| `git diff --check ae86185ff103156ffd516b572cf97d401f4a3d31 HEAD` | 출력 없음, exit 0 |
| `git diff --quiet ae86185ff103156ffd516b572cf97d401f4a3d31 HEAD -- tools tests versions.json .github` | exit 0, 코드·시험·registry·실제 workflow 불변 |
| release bash 8개 블록을 추출해 UTF-8 bytes로 WSL `bash -n`에 전달 | **8개 모두 구문 통과** |
| release §3.3/3.5 원문을 WSL `bash -s`로 실행하고 git·gh·node를 mock 함수로 대체 | **14개 시나리오**, 정상/실패 기대 결과 모두 일치. 실제 발행 없음 |
| `rg -n -C 2 'git tag -a\|gh release create\|git push.*v[0-9]' docs/tasks docs/runbooks`에 해당하는 발행 명령 전수 검색과 원문 대조 | T-213 복제는 제거됐지만 T-109·T-212의 위험한 복제 명령 잔류 |
| T-109·T-212의 정확한 해당 행을 추출해 WSL bash mock 실행 | 실패 3건 모두 `gh release create` 도달·최종 exit 0. T-212 두 경우는 dispatch도 도달 |
| Python stdin에서 `validate_plan.details()`의 실제 선행을 재귀 추적 | 세 0.1 후보 모두 T-009 후행. 아래 CI 선행 대조 참조 |
| `gh pr view 4 --json number,isDraft,state,headRefOid,baseRefName,statusCheckRollup` | [PR #4](https://github.com/digitie/kor-travel-common/pull/4) OPEN·draft·base main·head candidate 일치. [CI 34065770960](https://github.com/digitie/kor-travel-common/actions/runs/34065770960) validate-docs COMPLETED·SUCCESS |

WSL unittest는 `wsl -d Ubuntu-26.04 --cd /mnt/f/dev/kor-travel-common-wt/review-t015-a -- /home/digitie/.local/bin/uv run --no-project --python 3.11 python -B -X utf8 -m unittest discover -s tests -p 'test_*.py'`로 실행했다. Python task 파일명 하나를 잘못 추정해 읽기 검색이 실패한 뒤 `rg --files`와 실제 metadata 파서로 경로를 확인했다. 해당 읽기 실패는 검증 성공 건수에 포함하지 않았다.

## 기존 finding과 회귀 대조

| 원 ID·심각도 | 이번 A 확인 |
|---|---|
| **A-P1-01 / P1** | **FIXED 유지**. runbook의 main 강제 전환 제거, 준비 PR base/merge SHA·후보 ancestry·명시 source tag와 workflow 예외가 유지된다. 새 finding은 이 수정의 번복이 아니라 남은 별도 task 발행 경로다. |
| **A-P2-02 / P2** | **FIXED 유지**. T-010a의 T-109a 선행과 후보 tag/commit/digest 입력 연결이 유지되고 plan은 순환 없이 통과한다. |
| B-P1-01 / P1 | 동일 source 수정과 workflow 예외의 회귀 없음. B의 원 disposition을 변경하지 않는다. |
| B-P2-02 / P2 | T-213/T-311의 0.2 전체 소스 후보 보존·별도 minor branch 책임 유지. |
| B-P2-03 / P2 | 과거 source 원장 보존·현재 main commit 선행 확인·발행 후 main 문서 전용 PR 완료/후속 READY 경계 유지. 이번에 해당 절을 바꾸지 않았다. |
| B-P1-04 / P1 | 지적된 T-213의 중복 발행 블록은 제거됐고 단일 runbook 연결 및 build 실패 전파가 추가됐다. 다만 같은 유형의 다른 복제 경로가 남아 `A-P1-03`으로 별도 기록한다. |
| B-P2-05 / P2 | CI trigger·checkout SHA·artifact source·임시 release branch 실제 run acceptance와 담당 task가 연결됐다. 아래 선행 검토 범위에서 계획 누락 수정 확인. 실제 workflow 구현은 NOT_RUN이다. |

### CI 선행과 실행 가능성

[ci-deploy §9](../../../standards/ci-deploy.md#9-common-자체-ci)는 PR과 main/release push를 구분하고 release push의 `github.sha`를 checkout하도록 요구한다. 필수 job의 path/PR 조건 생략을 금지하며 run/artifact SHA를 RELEASE_SHA와 대조한다. T-009·T-101·T-302의 실제 임시 release 검증 branch CI와 source 일치가 수용 기준으로 들어갔다. PR head H를 merge R의 성공으로 세지 않으며 미구현은 발행 차단이다.

실제 task DAG에서 T-109a는 T-010을 통해 T-009를 선행으로 갖고, T-212a는 T-109a/T-201을 통해 T-009·T-101을 선행으로 갖는다. T-310a도 T-309→T-010을 통해 T-009를 선행으로 갖고 T-302의 Python CI를 포함한다. T-101/T-302 자체가 독립 착수 가능한 점을 후보 보존의 선행 누락으로 오인하지 않았다. 후보를 보존하기 전 필요한 CI 경로가 각각 연결되고, UI 추가도 ci-deploy의 T-201 책임에 명시돼 있다.

현재 docs.yml은 여전히 PR/main만 실행한다. 이번 범위가 계획과 수용 기준 보완임을 manifest와 상세 task가 명시하므로 이를 미래 release CI가 이미 구현됐다는 성공으로 세지 않았다.

### 수정 runbook의 발행 mock

rc와 정식 각각 다음 7개 시나리오를 실행했다. 정상은 exit 0과 create/view 도달, 나머지는 exit 1이었다.

| 주입 조건 | rc·정식 공통 결과 |
|---|---|
| 정상 HEAD·metadata·원격 SHA | create 1회, view 1회 |
| tag 실패 | create/view 0회 |
| push 실패 | create/view 0회 |
| ls-remote 실패·빈 출력 | create/view 0회 |
| 원격 peeled SHA 불일치 | create/view 0회 |
| release create 실패 | create 1회, view 0회 |
| release view 실패 | create 1회, view 1회, 실패 종료 |

실제 원문 블록을 실행하고 외부 도구의 응답만 함수로 바꿨다. 이 결과는 bash 실패 전파 확인이며 실제 GitHub/태그/자산 발행의 성공 증거가 아니다.

## A-P1-03 — T-109·T-212에 발행 단일화에서 빠진 위험한 명령이 남았다

- 심각도: **P1**.
- Disposition: **OPEN**.
- 위치: [T-109](../../../tasks/T-109-tokens-v0-1-0-release.md) **54~55행**, [T-212](../../../tasks/T-212-ui-v0-1-0-release.md) **59~61행**. 수정 정책: [release](../../../runbooks/release.md) §3.3의 142행과 T-213의 단일 절차 연결.
- 근거: 이번 수정은 tag/push/source 확인/발행을 runbook 한 곳에서 유지하고 실패 뒤 후속 실행을 금지한다. T-213에서는 복제 명령을 제거했지만 두 0.1 상세 task에는 같은 발행 명령이 남았다. 이 명령 자체는 이번 delta에서 수정되지 않은 잔여이며, 이번 발행 정본 단일화 및 누적 실패 경계 검토와 직접 연결된다.
- T-109 원문은 `git tag -a ... && git tag -v ... || git show ...` 뒤 독립 `gh release create ...`를 실행한다. tag 생성 실패를 show 성공으로 덮고 발행을 계속할 수 있다. 이 블록에는 명시 RELEASE_SHA·원격 peeled SHA 대조·실패 중단·verify-tag도 없다.
- T-212 원문은 `git tag -a ... && git push ...` 뒤 독립 `gh release create ...`와 `gh workflow run ...`을 실행한다. tag 또는 push 실패는 뒤 줄의 발행을 중단하지 않는다.
- 직접 재현: T-109 54~55행을 그대로 추출하고 git tag만 exit 128로 대체했다. `gh release create`가 1회 호출되고 최종 exit 0이었다. T-212 59~61행은 tag 실패와 push 실패를 각각 주입했으며 두 경우 모두 create와 workflow run이 각 1회 호출되고 최종 exit 0이었다. 모든 git/gh는 메모리 함수이고 실제 원격 행동은 없다.
- 실패 시나리오: 이전 commit을 가리키는 같은 rc tag가 남아 있는 상태에서 새 자산으로 재시도한다. tag 충돌 또는 push 거절을 무시한 task 명령이 이전 source tag에 새 artifact를 연결하는 발행을 계속할 수 있다. 새 runbook의 안전한 명령만 읽으면 차단되지만 상세 task가 별도 실행 경로를 여전히 제공한다.
- 영향: 정상적인 Git 실패에서 source/tag/asset 정합성과 필수 발행 중단 gate가 깨진다. 가장 먼저 실행될 0.1 릴리스 두 곳에 남은 경로이므로 T-213 한 곳의 수정만으로 전역 실패 경계가 닫히지 않는다.
- 권고: T-109·T-212에서도 실제 tag/push/create/dispatch 복제를 제거하고 T-213처럼 release 단일 절차를 연결한다. task에는 해당 패키지의 build·계약 검증만 유지한다. 현재 규범 task의 발행 명령을 전수 검색해 예외가 없는지 확인하고, 같은 실패 시나리오에서 발행 도달 0회를 재검증한다. 과거 리뷰·조사 원문은 수정 대상이 아니다.
- 기존 ID와 관계: B-P1-04가 지적한 T-213 위치는 수정됐다. 이 finding은 다른 두 task의 잔여 위치와 재현을 추가한 A의 독립 결과이며 기존 ID·심각도를 덮어쓰지 않는다.

## 미실행·한계와 최종 판정

- `NOT_RUN(구현 task 범위)`: 실제 release push workflow 구현·임시 검증 branch 실행·package build/install·artifact 재현. T-009/101/201/302 및 각 후보 task에서 검증해야 한다.
- `NOT_RUN(manifest 범위 밖)`: 실제 후보 tag·Release 생성, 소비자 설치·빌드·dispatch·권리 승인. mock을 실제 발행 성공으로 세지 않았다.
- `NOT_RUN(사용자 제외)`: npm/PyPI 조회·예약·게시·게시 재평가. 후속 실행을 요구하지 않는다.
- 변경되지 않은 과거 조사 전체를 재조사하지 않았다. 이번 원본 외의 파일은 쓰지 않았으며 다음 task 구현도 시작하지 않았다.

**BLOCK — 기존 A 2건 FIXED 유지, 새 A-P1-03/P1 OPEN.** 필수 검사와 수정된 runbook 자체의 14개 mock은 통과했지만 실제 상세 task에 남은 발행 경로가 실패를 무시한다. 해당 경로의 수정 또는 근거 있는 기각과 원 reviewer 재확인 전 merge gate는 닫히지 않는다.
