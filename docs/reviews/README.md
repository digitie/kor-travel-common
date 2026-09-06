# kor-travel-common 리뷰 아카이브

이 디렉터리는 특정 commit 또는 diff를 대상으로 수행한 리뷰를 누적 보존한다. review report는 역사적 evidence이며 현재 설계의 정본은 아니다. finding을 반영한 결과는 architecture, standards, ADR, task와 코드에 남긴다.

## 기록 규칙

1. 적대적 리뷰 요청마다 `adversarial/YYYY-MM-DD-<scope>.md` 파일을 새로 만든다. 같은 날 같은 범위가 반복되면 `-02`, `-03` suffix를 붙인다.
2. 과거 report에 새 review 결과를 덧붙이지 않는다. 오탈자나 깨진 링크를 고친 경우에만 correction note를 남긴다.
3. report는 review ID, 종류, 기준 commit과 base, 범위 밖, reviewer 전문 영역, 검증 방법, 시작·종료 시각을 기록한다.
4. 전문 리뷰어 서브에이전트 2명은 같은 manifest와 immutable 기준선을 서로 독립적으로 검토한다. 두 원본 결과가 확정되기 전에는 어느 reviewer에게도 상대 결과를 보여 주지 않는다.
5. reviewer별 실행 ID, 전달 입력, 실제 관찰 hash, 격리·clean 검증, 원본 결과는 `adversarial/evidence/YYYY-MM-DD-<scope>-reviewer-{a,b}.md`에 따로 보존하고 통합 report에서 연결한다.
6. finding ID는 report 안에서 고유하게 유지하고 심각도 `P0`~`P3`, 근거·위치, 재현 또는 실패 형태, 영향, 권고와 disposition을 포함한다.
7. 심각도와 disposition 상태의 정본은 [agent workflow §5](../runbooks/agent-workflow.md#5-전문-리뷰어-서브에이전트-2인-적대적-리뷰)다. `P0`/`P1`은 단순 risk acceptance나 release 차단으로 닫지 않는다.
8. review 반영 뒤 관련 검증을 다시 실행하고 post-fix commit을 두 reviewer가 재검토한다. report와 PR에 두 verdict를 기록한다.
9. review 원본·통합 disposition·재검증 결과와 archive index만 기록하는 closure commit은 같은 review를 재귀적으로 시작하지 않는다. 규범 문구를 함께 바꾸면 새 기준선 리뷰가 필요하다.

## 리뷰 목록

최신 항목을 위에 추가한다.

| 날짜 | 종류 | 기준선·범위 | 리뷰어 | 결과 |
|---|---|---|---|---|
| 2026-09-07 | full | [T-015 미게시·구현 선행](adversarial/2026-09-07-t015.md), a28c2a7 | A 정본·DAG / B 소스·릴리스 | A BLOCK / B BLOCK, 5 finding 수정 후 재검토 |
| 2026-09-07 | full post-fix | [T-005 최종 판정](adversarial/2026-09-07-t005-post-fix.md), f050997 | A npm·수치 / B 정책·evidence | **A PASS / B PASS, 9 finding FIXED** |
| 2026-09-07 | full | [T-005 버전 판정](adversarial/2026-09-07-t005.md), 409b95c | A npm·수치 / B 정책·evidence | A BLOCK / B BLOCK, 9 finding 수정 후 재검토 |
| 2026-09-07 | full post-fix 02 | [T-003 최종 판정](adversarial/2026-09-07-t003-post-fix-02.md), a2c1891 | A 검사기 / B 출처·전달 | **A PASS / B PASS, 6 finding FIXED** |
| 2026-09-07 | full post-fix | [T-003 재검토](adversarial/2026-09-07-t003-post-fix.md), 951b443 | A 검사기 / B 출처·전달 | A BLOCK / B PASS, 확장자 별칭 P1 잔여 |
| 2026-09-07 | full | [T-003 고지·SPDX](adversarial/2026-09-07-t003.md), 017fef1 | A 검사기 / B 출처·전달 | A BLOCK / B BLOCK, 6 finding 수정 후 재검토 대기 |
| 2026-09-06 | full 종료 post-fix | [Phase 0 최종 판정](adversarial/2026-09-06-phase0-closure-post-fix.md), fafb3f6 | A 도구·CI / B 계획·계약 | **A PASS / B PASS, 모든 finding FIXED** |
| 2026-09-06 | full 종료 delta | [Phase 0 종료 대조](adversarial/2026-09-06-phase0-closure.md), 8fb1334 | A 도구·CI / B 계획·계약 | A BLOCK / B CONDITIONAL, T-009 숨은 선행 |
| 2026-09-06 | full post-fix 03 | [Phase 0 세 번째 재검토](adversarial/2026-09-06-phase0-post-fix-03.md), 5670642 | A 도구·CI / B 계획·계약 | A PASS / B PASS, 15 finding FIXED |
| 2026-09-06 | full post-fix 02 | [Phase 0 두 번째 재검토](adversarial/2026-09-06-phase0-post-fix-02.md), 84759b6 | A 도구·CI / B 계획·계약 | A PASS / B CONDITIONAL(B-P2-09) |
| 2026-09-06 | full post-fix | [Phase 0 재검토](adversarial/2026-09-06-phase0-post-fix.md), 12fb3a8 | A 도구·CI / B 계획·계약 | A BLOCK(A-P1-05) / B PASS |
| 2026-09-06 | full | [Phase 0](adversarial/2026-09-06-phase0.md), d3712a8 → post-fix 대기 | A 도구·CI / B 계획·계약 | 최초 BLOCK·수정 재확인 대기 |

## 새 리뷰 시작

[적대적 리뷰 템플릿](adversarial/TEMPLATE.md)을 복사해 새 파일을 만들고, [agent workflow](../runbooks/agent-workflow.md)의 2인 리뷰 gate를 따른다. 일반 작업 시작 시 이 아카이브 전체를 읽지 않는다.
