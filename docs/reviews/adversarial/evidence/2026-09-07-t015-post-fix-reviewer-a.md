# T-015 수정 후 독립 full 리뷰 A 원본

- 실행 ID: `T015-A-POSTFIX-20260907-075244`.
- 전문 영역: 현재 정본·에이전트 실행 가능성·task DAG·source 명시·release 예외·0.2 보존·현재 main 원장과 과거 source 경계.
- 시작: `2026-09-07T07:52:44.8246010+09:00`.
- 종료 격리 확인: `2026-09-07T07:54:43.0604957+09:00`.
- Base: `a28c2a726f6940bf9f287188b87b1d5c12a8cd55`.
- Candidate 및 실제 시작/종료 HEAD: `ae86185ff103156ffd516b572cf97d401f4a3d31`.
- 격리: 전용 `review-t015-a` detached worktree. 시작/종료 `git status --porcelain=v1 --untracked-files=all` 출력 0줄. 기준선·제품·소비자·다른 원본을 수정하지 않았다.
- 입력: [동일 post-fix manifest](2026-09-07-t015-post-fix-manifest.md), [자신의 최초 원본](2026-09-07-t015-reviewer-a.md).
- 독립성: 최초 확정 A/B 원본과 통합 report만 교차 대조했다. 상대 reviewer의 이번 post-fix 원본이나 finding은 읽거나 요청하지 않았다.
- 최종 verdict: **PASS**. `A-P1-01`·`A-P2-02`는 원 심각도를 유지한 채 **FIXED**로 재확인했다. 새 finding 0건.
- 원본 상태: 독립 확정. 문서 계획 변경의 판정이며 실제 패키지·소비자·릴리스 성공 판정은 아니다.

## 전달 요청 원문

> T-015 수정 후 독립 full 재검토를 요청합니다. 공통 manifest: F:/dev/kor-travel-common/docs/reviews/adversarial/evidence/2026-09-07-t015-post-fix-manifest.md. Candidate ae86185ff103156ffd516b572cf97d401f4a3d31, base a28c2a726f6940bf9f287188b87b1d5c12a8cd55. 전용 worktree F:/dev/kor-travel-common-wt/review-t015-a를 candidate로 전환했습니다. 시작/종료 SHA·clean 직접 확인 후 최초 자기 finding의 원 ID/심각도를 재판정하고 전체 16개 delta 회귀를 검토하세요. A는 정본·agent 실행 가능성·DAG, source 명시·release 예외·0.2 보존·현재 main 원장과 과거 source 경계도 확인하세요. 최초 원본 2개는 이미 각각 확정되어 열람 가능하나 새 post-fix 상대 결과는 둘 다 확정 전 읽지 마세요. 원본 소유 파일은 기본 checkout의 docs/reviews/adversarial/evidence/2026-09-07-t015-post-fix-reviewer-a.md 하나입니다. 실행 ID·시각·요청·명령/결과·미검토·verdict와 원 finding disposition을 기록하고 제품/소비자/다른 파일을 수정하지 마세요. 다른 작업자의 변경을 되돌리지 마세요. 실제 배포/태그 생성은 수행하지 않습니다.

공통 요청 원문:

> 위 candidate/base에서 독립 full post-fix 적대적 리뷰를 수행한다. 자신의 최초 finding을 원 ID·심각도로 재판정하고 전체 수정의 누락·숨은 선행·source/원장 혼동·실행 불가·미실행 성공 처리를 공격한다. 코드나 다른 작업자의 변경을 고치지 말고 지정한 새 reviewer 원본 파일만 작성한다. 실행 ID·시각·전달 입력·실제 SHA·clean·실행 명령과 결과·미검토·finding disposition·BLOCK/CONDITIONAL/PASS를 남긴다. 상대 reviewer의 이번 새 결과는 읽지 않는다. 원본 마지막에는 개행 하나만 둔다.

## 검토 범위

16개 파일 전체 delta를 검토했다. ADR-014, release와 agent-workflow, T-010a·T-015·T-213·T-311, task 원장·통합 계획·resume의 규범/실행 연결과 journal·리뷰 색인·최초 manifest·독립 원본·통합 report를 대조했다. 큰 출력에서 잘린 통합 report 앞부분은 별도로 다시 읽었다. AGENTS와 문서 라우터의 정본 우선순위, 최초 리뷰에서 확인한 유지 조항을 적용했다.

0.1 후보→main의 0.2 구현→늦은 0.1 rc/정식→현재 원장 완료→0.2 후보 보존·릴리스의 순서를 상세 task와 연결했다. 내부 선행과 실제 소비자/권리 조건은 따로 확인했으며 모델의 임의 완료 상태를 현재 task에 반영하지 않았다.

## 직접 실행한 검증

| 명령·방법 | 실제 결과 |
|---|---|
| `git rev-parse HEAD`·`git status --porcelain=v1 --untracked-files=all` | 시작/종료 candidate 일치, clean |
| `git diff --stat a28c2a726f6940bf9f287188b87b1d5c12a8cd55 HEAD` 및 경로별 전체 diff | 16개 파일, 343줄 추가·30줄 삭제 |
| Windows Python 3.14.3: `python -B -X utf8 -m unittest discover -s tests -p 'test_*.py'` | **115 tests**, 14.800초, OK, skip 0, exit 0 |
| WSL Python 3.11.15: `uv run --no-project --python 3.11 python -B -X utf8 -m unittest discover -s tests -p 'test_*.py'` | **115 tests**, 10.458초, OK, skip 0, exit 0 |
| `python -B -X utf8 tools/validate_document_links.py` | **246문서·2022 로컬 대상**, 오류 0 |
| `python -B -X utf8 tools/validate_plan.py` | **101 tasks**, 오류 0 |
| `git diff --check a28c2a726f6940bf9f287188b87b1d5c12a8cd55 HEAD` | 출력 없음, exit 0 |
| `git diff --quiet a28c2a726f6940bf9f287188b87b1d5c12a8cd55 HEAD -- tools tests versions.json .github` | exit 0, 코드·시험·registry·CI 불변 |
| release의 bash 블록 추출 후 WSL `bash -n` | **8개 블록**, 구문 오류 0 |
| 새 source 확인 블록을 그대로 WSL `bash -s`에 넣고 `git`·`gh`를 메모리 mock 함수로 치환 | **9개 시나리오 모두 기대 결과**. 정상 1개 exit 0, 실패 8개 exit 1. 이 모델에서 실제 git/gh 호출 0 |
| Python stdin으로 실제 `validate_plan.details()`·`check_graph()` 실행 | 아래 DAG·원장 모델의 기대 결과 일치, task 파일 변경 0 |
| `gh pr view 4 --json number,isDraft,state,headRefOid,baseRefName,statusCheckRollup` | [PR #4](https://github.com/digitie/kor-travel-common/pull/4) OPEN·draft·base main·head candidate 일치. [CI 34065243380](https://github.com/digitie/kor-travel-common/actions/runs/34065243380) validate-docs COMPLETED·SUCCESS |

WSL unittest는 `wsl -d Ubuntu-26.04 --cd /mnt/f/dev/kor-travel-common-wt/review-t015-a -- /home/digitie/.local/bin/uv run --no-project --python 3.11 python -B -X utf8 -m unittest discover -s tests -p 'test_*.py'`로 실행했다.

처음 bash 구문 전달 시 Windows Python의 `text=True`가 LF를 CRLF로 변환해 backslash 연속행에서 구문 오류가 발생했다. fixture 전달을 UTF-8 bytes로 바꾸어 저장소 블록의 LF를 보존한 뒤 8개가 모두 통과했다. 저장소 bash 원문은 수정하지 않았으며 최초 전달 실패를 제품 결함이나 검증 성공으로 집계하지 않았다.

## 원 finding 재판정

| 원 ID·심각도 | Disposition | 직접 재확인한 수정과 회귀 |
|---|---|---|
| **A-P1-01 / P1** | **FIXED** | [release](../../../runbooks/release.md) §2.1~2.2·§3.1·§3.3·§3.5·체크리스트가 해당 minor release base/준비 PR의 merge commit을 사용한다. main 강제 전환이 제거됐고 tag 명령에 `RELEASE_SHA`를 명시한다. PR MERGED/base·후보 tag type/commit·ancestry·HEAD·metadata 확인, rc→정식의 새 PR/SHA 재확인과 artifact 대조가 연결됐다. [agent-workflow](../../../runbooks/agent-workflow.md) §7/8에도 release PR base 예외와 main 완료 기록 경계가 반영됐다. |
| **A-P2-02 / P2** | **FIXED** | [T-010a](../../../tasks/T-010a-external-consumer-smoke.md)와 현재 task 원장이 `T-010, T-109a`를 같은 선행으로 갖는다. 입력에 T-109a의 tag·commit·자산 URL·digest를 명시하고 임의 중간 pack 대체를 금지한다. T-010만 DONE인 모델은 이제 착수 선행을 충족하지 않는다. T-109를 역선행으로 추가하지 않아 순환도 없다. |

### source 확인 실패 경계

실제 release §3.1의 source 확인 블록을 수정 없이 가져와 mock `git`·`gh` 함수에 연결했다. 다른 minor의 main HEAD에서 시작하는 정상 모델은 지정된 준비 PR merge SHA로 detach하고 그 SHA를 확인했다. 다음 8개 조건은 모두 exit 1로 중단했다.

- PR 미병합.
- PR base가 main으로 잘못 지정됨.
- dirty worktree.
- 후보 ref가 annotated tag가 아닌 commit.
- 후보 tag의 peeled commit이 evidence SHA와 다름.
- 후보가 release merge commit의 조상이 아님.
- release merge commit이 지정 remote release branch의 조상이 아님.
- detach 이후 HEAD가 지정된 merge SHA와 다름.

이는 블록의 분기/실패 제어를 실제 bash에서 실행한 모델이다. GitHub API 권한·원격 fetch·실제 tag 생성·패키지 metadata/산출물 일치 검증을 실행한 것으로 확장하지 않았다.

### 과거 source와 현재 원장 모델

실제 101개 task를 읽어 메모리에 과거 후보 원장과 현재 main 원장을 만들었다. 후보 쪽은 T-109a가 IN_PROGRESS, T-010a가 BLOCKED인 시점으로 유지했다.

| 모델 | 실제 `check_graph()` 결과 |
|---|---|
| 과거 후보 원장을 그대로 유지 | 오류 0 |
| 현재 main에서 T-109a·T-010a 완료 evidence를 반영하고 T-109 IN_PROGRESS | 오류 0 |
| 음성 대조: 과거 branch의 T-109만 DONE으로 변경 | 두 선행 미완료 오류 2개 |
| 발행 후 현재 main 문서 원장에서 T-109를 DONE으로 변경 | 오류 0 |
| 외부 evidence도 충족했다는 모델 전제에서 내부 선행이 충족된 T-410·T-441·T-461을 READY로 변경 | 오류 0 |
| 과거 후보 원장 보존 여부 | 원본 메모리 사본과 동일 |

새 release §2.2는 위 정상 경로를 명시한다. 현재 main의 40자리 원장 commit으로 선행을 확인하고, 취소/실패가 새로 생겼으면 발행 전 다시 대조한다. 과거 원장의 상태를 진전시키지 않으므로 과거 source의 plan CI를 억지로 맞출 필요가 없다. main에는 문서 전용 PR로 완료 evidence와 해당 CHANGELOG 절만 반영하며 과거 package/lock 또는 branch 전체를 합치지 않는다. 기록 PR이 병합되기 전에는 현재 원장 완료로 세지 않는다.

## 전체 delta 회귀와 다른 최초 finding 관련 대조

- 0.2 보존 책임은 ADR-014·release §2.1·T-213·T-311에 연결됐다. 각각 검증한 0.2 전체 소스의 40자리 commit과 새 후보 tag, 별도 0.2 release branch를 요구한다. 0.1 branch의 버전만 올리는 경로를 금지한다. 별도 0.1 정식·소비자 조건은 유지된다.
- source commit·release merge commit·main 완료 기록 commit을 분리하고 준비 때 없는 결과를 NOT_RUN으로 둔다. 문서에 자기 commit hash를 미리 만들어 넣지 않는다.
- release 준비 PR은 해당 minor release branch를 base로 하며 일반 작업과 현재 원장 완료 PR은 main을 사용한다. 예외를 일반 workflow와 통합 계획에서도 확인했다.
- npm/PyPI 미게시·registry 이름 확보 철회·고정 파일 설치 정책을 다시 열지 않았다. 고정 source·artifact 만료/다른 바이트의 재검증·새 후보 번호와 불변 tag 조건도 유지된다.
- journal·resume·T-015·통합 report는 첫 두 BLOCK과 수정 후 재검토 대기를 드러낸다. 자체 FIXED 표시는 reviewer 재확인/merge 승인과 구분되고, T-015는 아직 IN_PROGRESS다.
- 미승인 소비자·권리 gate·실제 소비자 실행·rc 결과를 요구하는 정식 발행 조건이 common fixture 성공으로 대체되지 않았다. 원장 모델에서 외부 조건을 충족시킨 가정은 실제 외부 성공 evidence가 아니다.

이 대조는 A의 독립 회귀 판단이다. B의 이번 원 finding 재판정과 verdict를 대신하지 않는다.

## 미검증·남은 한계

- `NOT_RUN(manifest 범위 밖·패키지 실물 미구현)`: package build/install, pack/wheel의 실제 내용·reproducible digest, 시각/E2E 및 소비자 설치. 해당 구현/후보/릴리스 task의 gate로 남는다.
- `NOT_RUN(사용자 common-only 범위 및 외부 선행)`: 소비자 저장소 쓰기·실제 CI dispatch·권리 승인. common 검증으로 해제하지 않는다.
- `NOT_RUN(manifest 범위 밖)`: 실제 candidate tag 생성·release branch 준비 PR·GitHub Release 발행·자산 업로드/다운로드 대조. bash mock을 실제 발행 성공으로 기록하지 않았다.
- `NOT_RUN(사용자가 제외)`: npm/PyPI 조회·예약·게시·게시 재평가. 후속 실행을 요구하지 않는다.
- 모든 과거 조사·소비자 원천을 재조사하지 않았다. 이번 delta는 그 자료나 권리 사실을 갱신하지 않는다.

## 최종 verdict

**PASS — 원 A finding 2건 FIXED, 새 finding 0건.** 문서·계획·Windows/WSL 각 115 tests·diff·bash 구문·실패 경계 및 원장 모델이 위 범위에서 통과했다. 실제 패키지/소비자/릴리스 gate는 각 task에서 계속 검증해야 한다.
