# T-015 두 번째 수정 후 독립 적대적 리뷰 B 원본

- 실행 ID: `B-T015-PF02-20260907-080406-d1c7263`
- 시작: `2026-09-07T08:04:06.1894221+09:00`
- 종료 기준선 검증: `2026-09-07T08:08:04.2230624+09:00`
- Candidate 및 실제 시작·종료 SHA: `d1c7263de5c3ce930fbcdc234052bc7e98c1d2f1`
- Base: `ae86185ff103156ffd516b572cf97d401f4a3d31`
- 격리: `review-t015-b` detached worktree. 시작·종료 `git status --porcelain=v1` 출력 0줄. 발행 시험은 메모리 git/gh 응답 함수로 실행했고 실제 태그·Release·dispatch를 만들지 않았다.
- 입력: [공통 manifest](2026-09-07-t015-post-fix-02-manifest.md), 이전 확정 [B 원본](2026-09-07-t015-post-fix-reviewer-b.md)·[통합 기록](../2026-09-07-t015-post-fix.md), candidate의 정본과 task. 상대의 이번 새 원본·결과는 읽지 않았다.
- 범위: 전체 14파일 delta(299줄 추가·23줄 삭제), 누적 finding 회귀, source/tag/asset·CI 선행·후속 버전 보존·현재 main 원장과 외부 gate 정합.
- 최종 verdict: **BLOCK**. 기존 B finding 다섯 개는 원 ID·심각도대로 **FIXED**. 남은 task 발행 예시에서 새 **B-P1-06 · OPEN**을 재현했다.

## 전달 요청 원문

> T-015 두 번째 post-fix 독립 full 리뷰를 수행해 주세요. 공통 manifest F:/dev/kor-travel-common/docs/reviews/adversarial/evidence/2026-09-07-t015-post-fix-02-manifest.md를 읽고 따르세요. Candidate d1c7263de5c3ce930fbcdc234052bc7e98c1d2f1, base ae86185ff103156ffd516b572cf97d401f4a3d31. 기존 worktree F:/dev/kor-travel-common-wt/review-t015-b는 clean 확인 후 candidate detached로 전환했습니다. 시작·종료 SHA/clean을 직접 확인하세요. B 영역은 tag/push/Release 실패·source SHA·CI 검증 경로이며 전체 14파일 delta와 누적 finding 회귀도 검토합니다. 특히 B-P1-04/B-P2-05는 원 ID·심각도로 재판정하세요. 이전 두 원본은 확정되어 열람 가능합니다. 이번 상대 새 결과는 읽지 마세요. 출력 소유 파일은 main checkout docs/reviews/adversarial/evidence/2026-09-07-t015-post-fix-02-reviewer-b.md 한 개입니다. 다른 작업자가 함께 있으니 다른 파일 변경/되돌리기 금지. 실제 검증과 미실행을 분리해 최종 판정하세요. 현재 사용자 요청은 PR #4 머지 후 대기이며 다음 task 구현은 범위 밖입니다.

## 기존 finding disposition

| 원 ID·심각도 | 직접 확인 및 재사용 범위 | 판정 |
|---|---|---|
| B-P1-01 · P1 | source guard 블록은 직전 candidate와 동일하다. PR base·merge SHA·후보 ancestry를 검증한 뒤 명시 SHA를 태그에 사용한다. 직전 정상 1·실패 10개 source guard 모의 검증을 재사용하며 이번 rc·정식 절을 새로 실행했다 | **FIXED** |
| B-P2-02 · P2 | ADR-014·T-311은 직전과 불변. T-213은 0.2 보존 후보·release branch 책임을 유지하고 발행 부분만 정본으로 연결했다. minor별 소스와 자산 보존 계약 회귀 없음 | **FIXED** |
| B-P2-03 · P2 | 현재 main 원장 정본·과거 branch 상태 보존·발행 결과 문서 PR 왕복 계약을 유지한다. 해당 상태 전이 및 직전 실제 plan 함수의 세 단계 모델 검증을 재사용한다 | **FIXED** |
| B-P1-04 · P1 | T-213의 중복 태그·발행·dispatch 명령을 제거하고 release §3.1~3.5로 연결했다. 정본 rc·정식 절에서 tag/push 실패는 발행 이전에 중단하고 원격 peeled SHA도 확인한다. 이번 18개 모의 실행에서 실패 후 dispatch 0회 | **FIXED** |
| B-P2-05 · P2 | ci-deploy §9와 T-009/101/302가 `codex/release-*` push의 merge SHA checkout·필수 job·source SHA evidence를 명시한다. 후보 보존 task의 선행 graph에 CI 소유 task가 포함된다. 실제 workflow 구현 전에는 release CI를 NOT_RUN으로 차단한다 | **FIXED** |

최초 A-P1-01의 source 충돌도 위 B-P1-01과 같은 정본 수정으로 닫혀 있다. A-P2-02의 T-010a → T-109a 선행은 유지되며 상세 task도 직전과 동일하다. 신규 finding은 T-213의 수정 실패로 재분류하지 않고 별도 task에 남은 실행 예시를 대상으로 기록했다.

## 실행 검증

| 명령·검증 | 실제 결과 |
|---|---|
| `git rev-parse HEAD`, `git status --porcelain=v1` | 시작·종료 candidate 일치, clean |
| `git diff --stat ae86185ff103156ffd516b572cf97d401f4a3d31..HEAD`와 전체 경로별 diff·관련 정본/task 읽기 | 14파일 전체 검토. 이번 변경과 누적 실행 경로 대조 |
| `py -3 -B -X utf8 tools/validate_document_links.py` | 250문서·2052개 local target, 오류 0, exit 0 |
| `py -3 -B -X utf8 tools/validate_plan.py` | 101개 상세 task, 오류 0, exit 0 |
| `py -3 -B -X utf8 -m unittest discover -s tests -p 'test_*.py'` | Windows Python 3.14.3, **115 tests 성공·skip 0**, 72.698초, exit 0 |
| `git diff --check ae86185ff103156ffd516b572cf97d401f4a3d31..HEAD` | 출력 없음, exit 0 |
| `git diff --quiet ae86185ff103156ffd516b572cf97d401f4a3d31..HEAD -- tools tests versions.json .github` | exit 0. 코드·시험·registry·workflow 불변 |
| Python 표준 입력에서 release의 bash 블록을 추출하고 UTF-8 바이트로 `wsl.exe --exec bash --noprofile --norc -n` 전달 | 8개 블록 구문 통과 |
| rc·정식 발행 블록을 그대로 추출하여 `bash -s`에 전달, git/gh/node를 응답 함수로 대체하고 뒤에 dispatch 감시 호출 추가 | **2단계 × 9경우 = 18개 검증 성공**. 각 정상은 exit 0·후속 호출 도달. HEAD 불일치·메타데이터 불일치·tag 실패·push 실패·원격 조회 실패·원격 SHA 불일치·Release 생성 실패·Release 조회 실패는 모두 exit 1·후속 호출 없음 |
| `git show`와 현재 파일 내용 대조 | source guard·ADR-014·T-311·T-010a의 관련 내용 불변 확인. 이전 직접 검증 재사용 범위 한정 |
| 실제 task 선행의 전이적 조상 계산 | T-109a에 T-009/T-101, T-212a에 T-009/T-101/T-201, T-310a에 T-009/T-101/T-302 포함. release CI 소유 구현이 후보 보존 전에 위치 |
| `rg -n 'git tag -a\|gh release create\|git push origin'`에 해당하는 표현을 task·runbook에서 검색한 뒤 실제 명령 확인 | task의 중복 발행 명령이 T-109와 T-212에 남음. 아래 새 finding |
| T-109/T-212의 발행 3줄만 추출하고 git/gh 응답 함수를 주입한 4개 WSL bash 실행 | T-109 정상·tag 실패, T-212 tag 실패·push 실패에서 모두 Release 생성 및 dispatch 도달, exit 0 |
| `gh release create --help` | 원격에 태그가 없으면 기본 branch에서 자동 생성하며 `--verify-tag`로 이를 차단할 수 있음을 설치된 CLI 도움말에서 직접 확인 |
| `gh pr view 4 --json isDraft,headRefOid,statusCheckRollup` | [PR #4](https://github.com/digitie/kor-travel-common/pull/4) draft·candidate head 일치. [CI 34065770960](https://github.com/digitie/kor-travel-common/actions/runs/34065770960) validate-docs SUCCESS |

처음 T-212 모의 실행 범위를 뒤의 소비자 설치·checksum 줄까지 잡았을 때, 없는 smoke 디렉터리와 checksum 파일 때문에 해당 부분이 실패했다. 이를 성공으로 합산하지 않았으며 발행 3줄만 추출해 다시 실행했다. 실제 npm 설치·패키지 빌드는 실행되지 않았다. 마지막 위치 확인에서 PowerShell의 `rg docs/tasks/T-109*` 형태가 glob 경로 오류를 냈고 실제 두 파일명으로 다시 실행해 위치를 확인했다.

## B-P1-06 — 0.1 릴리스 task의 이전 명령이 잘못된 source 발행 경로를 유지함

- 심각도: **P1**. Disposition: **OPEN**.
- 위치: [T-109](../../../tasks/T-109-tokens-v0-1-0-release.md) **54~56행**, [T-212](../../../tasks/T-212-ui-v0-1-0-release.md) **59~61행**. 두 task는 최초 T-015 delta에서 보존 후보의 release branch를 사용하는 것으로 변경됐지만 해당 명령은 그대로다.
- 근거: T-109는 로컬 `git tag` 뒤 원격 push 없이 `gh release create`를 실행한다. `--verify-tag`·명시 source target도 없다. 설치된 CLI 도움말에 따르면 원격에 해당 태그가 없으면 기본 branch의 최신 commit에서 자동 생성한다. 따라서 검증된 release source R과 현재 main M이 다르면, 최초 정상 실행만으로도 R의 자산을 M의 원격 태그에 붙일 수 있다. T-212 역시 tag/push 실패 뒤 다음 줄의 발행을 계속하며 원격 태그 존재·peeled SHA 확인이 없다.
- 직접 재현: 두 task의 `git tag`·`gh release create`·`gh workflow run` 3줄을 추출했다. T-109의 URL placeholder만 문법상 실행 가능한 `fixture-asset-url`로 치환했고 git/gh는 메모리 함수로 대체했다. T-109 정상 실행은 push 호출 없이 release create·dispatch에 도달했다. T-109 tag 실패(128), T-212 tag 실패(128), T-212 push 실패(128)도 모두 release create·dispatch에 도달하고 exit 0이었다. 실제 원격 변경은 하지 않았다.
- 영향: 원격 태그가 없으면 main의 잘못된 commit을 가리키는 태그가 생길 수 있고, 기존 태그가 다른 commit을 가리키면 새 자산과 이전 source가 결합할 수 있다. 소비자 dispatch가 이어져 발행 실패를 성공처럼 전달할 수도 있다. 정본 runbook의 안전한 절차를 연결해 두었어도 실행 task가 별도로 제공하는 이 명령은 그 보장을 우회한다.
- 권고: T-213에 적용한 것처럼 T-109와 T-212의 태그·push·Release 발행 명령을 제거하고 release §3.1~3.5의 단일 절차로 연결한다. task에는 필요한 빌드·수용 기준만 남긴다. task 전체에서 중복 발행 명령이 남지 않았는지 검색하고, 정본의 tag/push/원격 SHA 실패 회귀를 확인한다. 제품 구현이나 실제 Release 실행은 이 수정의 조건이 아니다.

## 미검증과 종료 경계

- `NOT_RUN(구현 task 범위)`: 실제 release branch push CI·필수 package job·artifact source SHA. T-009/101/201/302가 구현하고 검증할 계획만 이번에 확인했다. 현재 문서 CI 성공을 미래 merge SHA의 필수 gate 통과로 집계하지 않았다.
- `NOT_RUN(범위 밖)`: 실제 package build/install·두 빌드 digest·candidate tag·Release·소비자 실행·권리 변경. bash 모의 실행은 실패 분기 확인이며 실제 발행 evidence가 아니다.
- `NOT_RUN(이번 전체 Python 시험은 Windows에서 실행)`: WSL Python 115 tests 재실행. WSL bash 구문·분기 검증은 실제 수행했다.
- `NOT_RUN(사용자 범위 제외)`: npm/PyPI 조회·예약·게시·게시 재평가. 다음 task 구현도 시작하지 않았다.
- 상대의 이번 결과를 읽지 않고 **BLOCK**를 확정했다. 이 원본 한 파일만 작성하며 다른 작업자 변경·기존 원본·제품·소비자 파일은 수정하지 않는다. PR #4 검증·머지 후 대기는 주 에이전트의 현재 작업 경계다.
