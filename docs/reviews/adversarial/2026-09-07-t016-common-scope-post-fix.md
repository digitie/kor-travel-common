# 2026-09-07 T-016 공용 시스템 범위 재점검 최종 적대적 리뷰

- Review ID: `T016-SCOPE-POST-FIX-20260907`
- 종류: 전문 리뷰어 2인 독립 full post-fix
- Candidate/post-fix: `a9fc2f5187bcf2517cb1da54ece9b12ab04b82ff`
- Base: `c8f81be7e70abbce892417eb0247a5d2337f31`
- 직전 candidate: `7504d0d47f0c4da31ed2683b79332ef63bcca5de`
- 범위: 공용 위젯·토큰·코어·로그인 범위, ADR/architecture/standards/task/plan 정합성, T-011 root 계약, T-213a·T-214 선행 전이, GPL·미게시·소비자 경계
- 범위 밖: 패키지 실물 구현·실제 소비자 저장소·릴리스 tag/asset·npm/PyPI 게시
- 관련 task: [T-016](../../tasks/T-016-common-shared-systems-scope.md), [PR #9](https://github.com/digitie/kor-travel-common/pull/9)
- Coordinator: Codex
- 상태: `COMPLETE`
- 최종 verdict: **PASS / PASS**

## 1. 동일 기준선과 독립 원본

동일 manifest는 [review manifest](evidence/2026-09-07-t016-common-scope-post-fix-manifest.md)다. 각 원본은 상대 결과가 확정되기 전 독립적으로 작성됐고 candidate 파일을 수정하지 않았다.

| 항목 | Reviewer A | Reviewer B |
|---|---|---|
| 전문 영역 | 정본·task DAG·문서 계약 | 외부 gate·tag/source·검증 경계 |
| 실행 ID | `/root/reviewer_a` follow-up | `/root/reviewer_b` follow-up |
| 시작·종료 | 18:45:42~18:46:09 KST | 도구 응답에 시각 미노출 |
| 격리·무결성 | detached clean, SHA/tree 동일 | detached clean, SHA/tree 동일 |
| candidate/tree | `a9fc2f5` / `4b9acba` | `a9fc2f5` / `4b9acba` |
| 원본 | [A evidence](evidence/2026-09-07-t016-common-scope-post-fix-reviewer-a.md) | [B evidence](evidence/2026-09-07-t016-common-scope-post-fix-reviewer-b.md) |
| verdict | PASS | PASS |

## 2. 전체 finding disposition

| ID | 심각도 | 최종 상태 | disposition |
|---|---|---|---|
| A-T016-P1-01 | P1 | FIXED | T-214가 공용 로그인 위젯 구현·exports·접근성·pack을 소유한다. |
| A-T016-P2-02 | P2 | FIXED | T-011·T-403·ADR-010에 manifest와 소비자 root/workflow 전달을 명시했다. |
| A-T016-P2-03 | P2 | FIXED | common fixture 임시 포트와 ktdm 운영 포트를 분리했다. |
| A-T016-P3-04 | P3 | FIXED | T-011 10개 앱 표면과 evidence count를 맞췄다. |
| A-T016-P3-05 | P3 | FIXED | T-016 예상 파일을 실제 경로로 동기화했다. |
| A-T016-P3-06 | P3 | FIXED | ADR-001·011의 부분 대체 상태를 본문에 기록했다. |
| A-T016-P3-07 | P3 | FIXED | PR 본문의 실제 개행을 확인했다. |
| A-T016-P1-08 | P1 | FIXED | T-213a 내부 common 후보를 분리해 T-214의 외부 release 의존을 제거했다. |
| A-T016-P3-09 | P3 | FIXED | 로그인 구현 소유를 T-214로 통일했다. |
| A-T016-P2-10 / B-T016-P2-07 | P2 | FIXED | annotated tag object의 로컬/원격 일치와 peeled commit/source SHA 일치를 분리했다. |
| B-T016-P2-02 | P2 | FIXED | T-312 package test 경로와 0 test/skip 실패 조건을 명시했다. |
| B-T016-P2-03 | P2 | FIXED | backend 공용 primitive와 앱 소유 저장소·비밀·정책을 구분했다. |
| B-T016-P3-04 | P3 | FIXED | ADR index와 ADR 본문 상태를 맞췄다. |

새 P0/P1/P2/P3 finding은 없다. 열린 finding 0, deferred 0, rejected 0이다.

## 3. 재검증

- coordinator: Windows Python 3.14.3에서 전체 `179 tests`, skip 0, exit 0.
- plan: `validate_plan.py`가 106 task, 오류 0.
- links: `validate_document_links.py`가 324문서·2,261대상, 오류 0.
- redaction: `check_prod_redaction.py`가 399파일·발견 0.
- diff: candidate delta와 각 fix commit `git diff --check` 성공.
- CI: [34107732188](https://github.com/digitie/kor-travel-common/actions/runs/34107732188)의 exact candidate 5개 job 성공.
- reviewer A/B는 Windows·WSL validator와 immutable SHA/tree를 확인했고, B는 annotated tag 임시 fixture를 재현했다.

## 4. 최종 판정과 미실행

**PASS / PASS.** 모든 P0/P1 finding은 수정 후 원 reviewer가 재확인했다. T-016은 이 report와 함께 DONE으로 기록하고 T-011을 READY로 전환한다.

`NOT_RUN(후속 task/외부 범위)`: packages/tokens·packages/ui·Python 실물 구현, 실제 pack/wheel 설치, 후보 tag/Release 발행, 소비자 저장소 변경·build/e2e·권리 gate, npm/PyPI 게시. 임시 fixture는 제품 또는 외부 릴리스 성공으로 집계하지 않았다.
