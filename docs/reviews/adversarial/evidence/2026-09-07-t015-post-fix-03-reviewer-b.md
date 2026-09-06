# T-015 세 번째 수정 후 독립 적대적 리뷰 B 원본

- 실행 ID: `B-T015-PF03-20260907-081116-95c139f`.
- 시작: `2026-09-07T08:11:16.2422221+09:00`. 종료 기준선 확인: `2026-09-07T08:11:59.2551573+09:00`.
- Candidate 및 실제 시작·종료 SHA: `95c139fdea523910fb5f1bdd32f5bae728df2915`. Base: `d1c7263de5c3ce930fbcdc234052bc7e98c1d2f1`.
- 격리: `review-t015-b` detached worktree, 시작·종료 porcelain 출력 0줄. 자기 새 원본만 작성하며 제품·소비자·기존 원본·다른 작업자 파일을 수정하지 않았다.
- 입력: [동일 manifest](2026-09-07-t015-post-fix-03-manifest.md), 확정된 [직전 B 원본](2026-09-07-t015-post-fix-02-reviewer-b.md)·[직전 통합](../2026-09-07-t015-post-fix-02.md). 상대의 이번 원본·결과는 읽지 않았다.
- 범위: 10파일 전체 delta(252줄 추가·15줄 삭제), 두 task의 규범 변경, 누적 9개 finding 회귀. 최종 verdict: **PASS**. 새 finding 없음.

## 전달 요청 원문

> T-015 post-fix-03 독립 full 재확인 요청. 동일 manifest F:/dev/kor-travel-common/docs/reviews/adversarial/evidence/2026-09-07-t015-post-fix-03-manifest.md를 따르세요. Candidate 95c139fdea523910fb5f1bdd32f5bae728df2915, base d1c7263de5c3ce930fbcdc234052bc7e98c1d2f1. 기존 review-t015-b worktree를 clean 확인 후 전환했습니다. 규범 delta는 T-109/T-212 두 검증 절뿐이며 다른 파일은 기록입니다. B-P1-06을 원 ID·심각도로 재확인하고 전체 delta 및 누적 finding 회귀를 확인하세요. 출력 소유는 main checkout docs/reviews/adversarial/evidence/2026-09-07-t015-post-fix-03-reviewer-b.md 한 파일입니다. 다른 작업자와 함께 있으니 다른 파일 수정/되돌리기 금지. 이번 상대 결과는 확정 전 읽지 마세요. 변경 없는 정본·코드의 이전 검증은 동일성 확인과 범위 표기로 재사용하고 원본은 새 검증·결론 중심으로 간결히 작성해 주세요. 현재 PR 머지 후 대기, 다음 task 시작 금지입니다.

## 원 finding별 재판정

| 원 ID·심각도 | 이번 확인 | Disposition |
|---|---|---|
| B-P1-01 · P1 | release의 source guard·명시 SHA·workflow 예외 불변. 직전 source 선택 검증 재사용 | **FIXED 유지** |
| B-P2-02 · P2 | ADR-014·T-213/T-311의 minor별 보존 책임 불변 | **FIXED 유지** |
| B-P2-03 · P2 | 과거 branch 원장 보존·현재 main 선행 확인·문서 PR 왕복 계약 불변 | **FIXED 유지** |
| B-P1-04 · P1 | T-213 정본 연결과 release의 실패 중단·원격 peeled SHA 대조 불변. 직전 18개 발행 모의 검증 재사용 | **FIXED 유지** |
| B-P2-05 · P2 | ci-deploy 및 CI 소유 task·후보 선행 불변. 실제 구현은 NOT_RUN이라는 경계 유지 | **FIXED 유지** |
| B-P1-06 · P1 | T-109/T-212의 별도 tag/create/dispatch 경로 삭제. 검증한 준비 PR merge commit·패키지/버전을 정본에 전달하도록 명시. 현행 규범의 발행 명령 전수 검색에서 task 우회 경로 0건 | **FIXED** |

A-P1-01/P1·A-P2-02/P2의 기존 source·후보 선행 수정에도 회귀가 없다. A-P1-03/P1은 B-P1-06과 같은 두 위치의 실패 전파 문제이며 이번 제거로 해당 경로가 닫혔음을 B 관점에서 확인했다. A 원 reviewer의 독립 재판정을 대신하지 않는다.

## 새 검증과 재사용

| 명령·검증 | 결과 |
|---|---|
| `git diff --stat/--numstat d1c7263de5c3ce930fbcdc234052bc7e98c1d2f1..HEAD` 및 전체 10파일 읽기 | 규범 변경 두 task와 기록의 상태 정합 확인. T-015는 재확인 전 IN_PROGRESS 유지 |
| `py -3 -B -X utf8 tools/validate_document_links.py` | **254문서·2077 local target**, 오류 0, exit 0 |
| `py -3 -B -X utf8 tools/validate_plan.py` | **101 task**, 오류 0, exit 0 |
| `git diff --check d1c7263de5c3ce930fbcdc234052bc7e98c1d2f1..HEAD` | 오류 0, exit 0 |
| `rg -n 'git tag -a\|gh release create\|git push origin.*v0'`를 architecture·standards·tasks·runbooks·AGENTS·docs/README·ADR에서 실행 | 태그 생성·push·Release 생성 명령은 release 정본의 rc/정식 두 절에만 존재. task에는 조회 명령만 남음 |
| 두 task의 bash 블록을 원문 추출하여 UTF-8 바이트로 WSL `bash -n`·`bash -s` 전달 | **구문 2개·모의 실행 8개 통과**. task마다 정상은 exit 0, cd/checksum/tar 실패는 각각 exit 1·후속 감시 호출 없음. cd 실패 뒤 checksum 0회, cd/checksum 실패 뒤 tar 0회. git/gh 호출 0회 |
| base와 `AGENTS.md docs/README.md docs/adr docs/runbooks docs/standards tools tests versions.json .github`의 `git diff --quiet`, 변경 파일 목록과 기존 관련 task 대조 | exit 0·관련 계약 불변. 직전 B가 직접 실행한 Windows Python 3.14.3 **115 tests·skip 0·72.698초** 및 source guard 11개·발행 18개·원장 모델 3단계 검증을 해당 불변 범위에서 **재사용**. 이번 실행 건수로 다시 집계하지 않음 |
| `gh pr view 4 --json isDraft,headRefOid,statusCheckRollup` | [PR #4](https://github.com/digitie/kor-travel-common/pull/4) draft·candidate 일치. [CI 34066138272](https://github.com/digitie/kor-travel-common/actions/runs/34066138272) validate-docs SUCCESS |

새 자산 확인은 `dist/release`를 정본과 일치시키고 checksum 및 tar 명령 실패를 중단한다. tar 목록을 task 수용 기준과 대조하라는 문장을 유지하므로 목록 출력만으로 고지·내용물 합격을 선언하지 않는다. 모의 실행은 메모리 cd/sha256sum/tar 함수로 실패를 주입했으며 실제 자산·원격 상태를 조작하지 않았다.

## 미실행과 판정 경계

- `NOT_RUN(동일성 확인 후 재사용)`: 이번 candidate에서 전체 unittest·불변 source guard/발행 블록 재실행. 이전 직접 결과와 재사용 범위는 위 표와 직전 원본에 명시했다.
- `NOT_RUN(후속 구현·외부 task 범위)`: 실제 package build/install·두 빌드 digest·release branch CI·후보 태그·Release·소비자 실행·권리 승인. 문서 CI와 모의 실행은 해당 gate의 성공이 아니다.
- `NOT_RUN(사용자 제외)`: npm/PyPI 조회·예약·게시·재평가 및 다음 task 착수.

**PASS — B-P1-06/P1 수정 확인, 기존 B 5건 FIXED 유지, 새 finding 0건.** 이 판정은 지정한 문서 candidate에 한정하며 실제 발행 가능 또는 외부 gate 완료 판정이 아니다. 현재 PR 병합 뒤 대기 경계를 유지한다.
