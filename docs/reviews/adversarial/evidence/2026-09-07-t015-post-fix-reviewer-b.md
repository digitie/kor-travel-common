# T-015 수정 후 독립 적대적 리뷰 B 원본

- 실행 ID: `B-T015-PF-20260907-075300-ae86185`
- 시작: `2026-09-07T07:53:00.8356566+09:00`
- 종료 검증: `2026-09-07T07:55:43.4026234+09:00`
- Candidate 및 실제 시작·종료 SHA: `ae86185ff103156ffd516b572cf97d401f4a3d31`
- Base: `a28c2a726f6940bf9f287188b87b1d5c12a8cd55`
- 격리: `review-t015-b` detached worktree. 시작·종료 porcelain 출력 0줄. 문서 명령 실행 시험의 git/gh는 메모리 응답 함수로 대체했고 실제 태그·발행·소비자 실행은 하지 않았다. 제품·다른 파일·이전 원본을 수정하지 않았다.
- 입력: [공통 manifest](2026-09-07-t015-post-fix-manifest.md), [최초 B 원본](2026-09-07-t015-reviewer-b.md), 독립 원본이 모두 확정된 [최초 통합](../2026-09-07-t015.md). 상대의 이번 새 원본·결과는 읽지 않았다.
- 범위: 16개 전체 delta(343줄 추가·30줄 삭제), 기존 세 finding, source/tag/asset·0.2 보존·main 원장 왕복·외부 gate·CI 회귀.
- 최종 verdict: **BLOCK**. 기존 `B-P1-01`·`B-P2-02`·`B-P2-03`은 원 심각도대로 모두 **FIXED**다. 새 `B-P1-04`와 `B-P2-05`는 **OPEN**이다.

## 전달 요청 원문

> T-015 수정 후 독립 full 재검토를 요청합니다. 공통 manifest: F:/dev/kor-travel-common/docs/reviews/adversarial/evidence/2026-09-07-t015-post-fix-manifest.md. Candidate ae86185ff103156ffd516b572cf97d401f4a3d31, base a28c2a726f6940bf9f287188b87b1d5c12a8cd55. 전용 worktree F:/dev/kor-travel-common-wt/review-t015-b를 candidate로 전환했습니다. 시작/종료 SHA·clean 직접 확인 후 최초 자기 finding의 원 ID/심각도를 재판정하고 전체 16개 delta 회귀를 검토하세요. B는 source/tag/asset·0.2 보존·과거 원장 유지와 현재 main 문서 PR 왕복·외부 gate를 확인하세요. 최초 원본 2개는 이미 각각 확정되어 열람 가능하나 새 post-fix 상대 결과는 둘 다 확정 전 읽지 마세요. 원본 소유 파일은 기본 checkout의 docs/reviews/adversarial/evidence/2026-09-07-t015-post-fix-reviewer-b.md 하나입니다. 실행 ID·시각·요청·명령/결과·미검토·verdict와 원 finding disposition을 기록하고 제품/소비자/다른 파일을 수정하지 마세요. 다른 작업자의 변경을 되돌리지 마세요. 실제 배포/태그 생성은 수행하지 않습니다.

## 기존 finding 재판정

| 원 ID·심각도 | 수정·독립 재확인 | Disposition |
|---|---|---|
| B-P1-01 · P1 | release §3.1의 PR base·merge SHA·후보 ancestry 검증, §3.3/3.5의 명시 `RELEASE_SHA` 태그와 main 전환 제거, workflow의 release base 예외가 정렬됨. 문서에서 source guard를 그대로 추출해 WSL bash에서 git/gh 응답을 대체한 11개 경우를 실행: 정상은 main과 다른 release SHA를 선택, 실패 10개는 exit 1 | **FIXED** |
| B-P2-02 · P2 | ADR-014·release의 후보 형식이 minor별로 일반화되고 T-213·T-311이 각 0.2 전체 소스 검증·후보 tag·별도 0.2 branch 준비를 명시적으로 소유. 두 task의 acceptance에 source/release/main 기록 commit 구분과 두 branch plan 검증이 추가됨. 0.1 후보/branch의 버전만 올리는 경로를 금지 | **FIXED** |
| B-P2-03 · P2 | release §2.2가 현재 main 상태 정본과 과거 branch 스냅샷을 구분하고, main 선행 evidence를 commit으로 고정한 뒤 발행 결과만 문서 전용 PR으로 돌려보냄. 실제 `validate_plan.check_graph`를 사용한 branch 상태 모델에서 역사 원장 미변경, 현재 main의 발행 전 상태, 문서 PR 완료 후 T-109 DONE·T-212 READY 모두 오류 0 | **FIXED** |

원 finding의 영향·재현·권고는 최초 원본에 유지했다. 새 결함을 기존 ID의 미수정으로 섞지 않았다. T-010a의 T-109a 선행·후보 tag/digest 연결도 원장과 상세 task에 함께 반영됐으며 새 DAG 순환은 없다. 외부 승인·실행 evidence 없이는 READY/DONE을 정당화하지 않는 조건을 유지한다.

## 실행 검증

| 명령·검증 | 실제 결과 |
|---|---|
| 시작·종료 `git rev-parse HEAD`, `git status --porcelain=v1` | candidate 유지·clean |
| `git diff --stat a28c2a726f6940bf9f287188b87b1d5c12a8cd55..HEAD` 및 경로별 전체 diff/필요 정본 읽기 | 16파일. 새 규범과 원본/통합 기록·상태 갱신 대조 |
| `py -3 -B -X utf8 tools/validate_document_links.py` | 246개 문서·2022개 local target, 오류 0, exit 0 |
| `py -3 -B -X utf8 tools/validate_plan.py` | 101개 상세 task, 오류 0, exit 0 |
| `py -3 -B -X utf8 -m unittest discover -s tests -p 'test_*.py'` | Windows Python 3.14.3, **115 tests 성공·skip 0**, 12.890초, exit 0 |
| `git diff --check a28c2a726f6940bf9f287188b87b1d5c12a8cd55..HEAD` | 출력 없음, exit 0 |
| `git diff --quiet a28c2a726f6940bf9f287188b87b1d5c12a8cd55..HEAD -- tools tests versions.json .github` | exit 0. 코드·시험·registry·CI 불변 |
| 표준 입력 Python에서 release의 bash 블록을 추출하여 `wsl.exe --exec bash --noprofile --norc -n` 실행 | **8개 블록 구문 통과**. 실제 발행·빌드 실행이 아님 |
| 같은 방식으로 source guard를 `bash -s` 실행, git/gh는 메모리 응답 함수 | 정상 1개 exit 0, 실패 10개 exit 1. 아래 경계 참조. 저장소/원격 mutation 없음 |
| `validate_plan.details()`·`check_graph()`를 호출한 메모리 branch 모델 | 과거 release 원장 미변경 상태, 현재 main의 선행 완료·T-109 IN_PROGRESS, 발행 뒤 문서 PR 반영·T-212 READY의 3단계에서 오류 0. 외부 승인 충족은 모델의 명시적 가정이며 실제 승인 아님 |
| T-213의 태그/발행 부분을 그대로 추출하여 mock tag 실패·push 실패 주입 | **두 경우 모두 release create·workflow run까지 진행하고 최종 exit 0**. B-P1-04 |
| docs.yml·ci-deploy §9·T-009/101/302와 새 release §3.1 대조 | PR/main 전용 trigger와 release merge SHA 필수 CI 사이 실행 경로 누락. B-P2-05 |
| `gh release create --help` | `--verify-tag`가 원격 태그 존재 여부를 확인함을 로컬 CLI 도움말로 확인. 임의의 `RELEASE_SHA`와의 동일성 검사가 아님 |
| `gh pr view 4 --json isDraft,headRefOid,statusCheckRollup` | [PR #4](https://github.com/digitie/kor-travel-common/pull/4) draft·candidate head 일치. [CI 34065243380](https://github.com/digitie/kor-travel-common/actions/runs/34065243380) validate-docs COMPLETED·SUCCESS |

source guard의 실패 입력은 dirty checkout, main 대상 branch, 미병합 PR, 다른 PR base, 잘못된 merge SHA, fetch 실패, lightweight 후보 tag, 후보 peeled commit 불일치, 후보의 후손이 아닌 release SHA, release branch에서 도달하지 않는 SHA다. 정상 모델은 main M과 release R을 다르게 둔 상태에서 R을 선택했다. 이 결과는 명령의 분기 검증이며 실제 GitHub PR·태그·패키지 무결성 검증을 대신하지 않는다.

첫 bash 구문 확인은 Python의 Windows text stdin 전달이 줄 끝을 바꾸어 continuation이 깨졌고 exit 1이었다. 같은 문자열을 UTF-8 바이트로 전달하여 8개 블록을 다시 검사한 뒤 모두 통과했다. 이를 문서 결함으로 보고하거나 처음 실패를 성공으로 합산하지 않았다.

## B-P1-04 — UI rc의 태그/푸시 실패 뒤에도 발행·dispatch를 계속함

- 심각도: **P1**. Disposition: **OPEN**.
- 위치: [T-213](../../../tasks/T-213-ui-v0-2-0-release.md) **65~69행**, 특히 `git tag ... "$RELEASE_SHA" && git push ...` 다음의 독립 `gh release create --verify-tag`·`gh workflow run`.
- 근거: 수정된 runbook의 tokens 명령은 tag와 push 각각 `|| exit 1`로 중단하지만 T-213의 복제 예시는 같은 보호를 갖지 않는다. `&&`는 push 실행만 제어하며 다음 줄의 release create를 중단하지 않는다. 블록에 `set -e`도 없다. 새 `--verify-tag`는 원격 태그의 존재만 확인하므로 현재 빌드 source와의 동일성을 보장하지 않는다.
- 직접 재현: 현재 문서의 `test "$(git rev-parse HEAD)" ...`부터 마지막 validator까지를 추출했다. HEAD는 RELEASE_SHA와 같게 반환하고 git tag 또는 git push를 각각 exit 128로 대체했다. git/gh/python3는 모두 메모리 함수라 실제 외부 행동은 없다. 두 경우 모두 `gh release create ... --verify-tag`와 `gh workflow run ...`이 호출됐고 마지막 반환은 0이었다.
- 실패 시나리오: 원격에 같은 rc 태그가 이전 commit을 가리키지만 Release는 아직 없는 불완전한 발행 상태에서, 다른 RELEASE_SHA의 자산으로 명령을 다시 실행한다. tag 생성 또는 push 충돌이 발생해도 다음 줄은 진행한다. `--verify-tag`는 기존 원격 태그 때문에 성공할 수 있어 예전 tag source와 새 자산을 묶는 Release를 만들 수 있다. 사후 digest/source 확인만으로 이미 발행한 잘못된 버전을 없던 것으로 만들 수 없다.
- 영향: 정상적인 Git 실패가 발행 중단으로 전파되지 않아 source/tag/asset 계약과 불변 발행 경계를 깨뜨릴 수 있다. 원래 main 대상 충돌은 수정됐지만 수정된 source 지정만으로 이 실패 경로가 닫히지 않는다.
- 권고: T-213의 tag·push·발행 실패를 각각 즉시 중단하고 이후 dispatch를 호출하지 않게 한다. 가능하면 중복 태그/발행 예시를 runbook의 단일 절차로 연결한다. 발행 전 원격 태그의 peeled commit이 검증한 RELEASE_SHA와 같은지도 대조하고, 기존 다른 태그에는 새 rc 번호로 재검증한다. tag 실패·push 실패에서 발행 호출 0회를 회귀 기준으로 삼는다.

## B-P2-05 — release merge commit을 검증할 CI trigger가 계획에 없음

- 심각도: **P2**. Disposition: **OPEN**.
- 위치: [release](../../../runbooks/release.md) **66행**의 새 merge commit CI 요구와 [ci-deploy](../../../standards/ci-deploy.md) §9의 216~223행 trigger 표, [T-009](../../../tasks/T-009-ci-hardening.md)의 CI 구현/수용 기준. 실제 [docs.yml](../../../../.github/workflows/docs.yml) 6~9행도 push main·PR만 받는다.
- 근거: 새 절차는 준비 PR의 merge commit을 `RELEASE_SHA`로 고정하고 그 commit의 docs/tools/해당 패키지/secret-scan green을 요구한다. 하지만 현행 및 계획의 docs/packages/python-package는 PR·push main, tools와 secret-scan은 PR이고 release branch push·해당 SHA를 대상으로 한 dispatch가 없다. T-009는 PR head SHA checkout을 요구하므로 준비 PR의 성공을 다른 merge SHA의 실행으로 바꿔 적을 수도 없다.
- 실패 시나리오: 준비 PR head H에서 검증한 뒤 `codex/release-ui-0.1`에 squash/merge되어 새 commit R이 된다. R은 main push가 아니므로 명시된 trigger에서 필수 job을 얻지 못한다. branch/source 선택과 후보 ancestry는 맞아도 §3.1의 “그 commit CI green”을 충족할 실행 경로가 없다. PR의 H 결과를 R 결과로 적으면 미실행 성공 처리가 되고, 정확히 지키면 발행이 멈춘다.
- 검증: 현재 workflow와 정본 trigger 표·구현 task를 직접 읽고 PR head H와 release merge R을 구분한 사건 모델로 대조했다. 실제 release branch 생성이나 CI dispatch는 수행하지 않았다. 현재 PR #4의 문서 CI 성공은 미래 R의 필수 패키지 CI를 증명하지 않는다.
- 영향: 새 release branch 설계가 요구하는 필수 gate를 다음 구현자가 만들 수 있도록 연결되지 않은 계획상 공백이다. CI를 실제로 구현할 T-009/101/302에서 해소할 수 있으며 이번 문서 PR에 패키지 구현을 요구하는 finding은 아니다.
- 권고: release branch merge SHA에 필요한 job을 실행할 push trigger 또는 명시 SHA dispatch 계약을 ci-deploy·해당 구현 task에 연결한다. 필터로 tools/secret-scan이 빠지지 않게 하고 run/artifact의 source SHA 확인을 acceptance에 둔다. 늦게 분기한 보존 후보에도 그 CI 실행 경로가 존재해야 한다. 별도 후속으로 처리한다면 owner·task·발행 차단 gate·적용 시점을 명시해야 한다.

## 미검증과 최종 경계

- `NOT_RUN(범위 밖)`: 실제 package build/install, 두 빌드 digest, 원격 candidate tag·release branch/PR·GitHub Release, 소비자 설치·CI dispatch·권리 변경. 문서 모델·bash 구문/모의 응답은 실제 발행 evidence가 아니다.
- `NOT_RUN(이번 reviewer의 전체 Python 시험 환경은 Windows 3.14.3)`: WSL Python 전체 115 tests 재실행. WSL bash 구문·분기 시험은 별도 실제 실행으로 기록했다.
- `NOT_RUN(사용자 범위 제외)`: npm/PyPI 조회·예약·게시·게시 재평가. 이번 결과로 이를 재도입하지 않는다.
- 기존 세 finding은 FIXED이며 source/원장 분리와 0.2 보존 책임은 독립 확인됐다. 새 P1은 수정 또는 근거 있는 기각을 원 reviewer가 재확인해야 한다. 새 P2도 수정하거나 owner·상세 task·gate·시점이 있는 disposition이 필요하다. 상대 새 결과를 보지 않고 **BLOCK**를 확정했으며 자기 원본 한 파일만 작성했다.
