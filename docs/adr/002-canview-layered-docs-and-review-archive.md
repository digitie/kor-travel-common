# ADR-002: canview 계층형 문서 정보구조와 누적 독립 리뷰 아카이브 채택

- 상태: accepted
- 날짜: 2026-09-06
- 근거 문서: `docs/plan/design-brief.md` D-02·D-04·D-05·D-27, `docs/survey/cross/canview-structure-checklist.md` §1~§4·Q1~Q5, `docs/survey/cross/docs-conventions.md` §2 C1~C16·§3·§4, canview `docs/adr/004-layered-documentation-and-review-archive.md`(`1f93b8a`)

## 컨텍스트

사용자는 canview의 프로젝트 구조와 `AGENTS.md` 내용을 채택하도록 지시했다(지시 (5)). canview는 `AGENTS.md` → `docs/README.md` → `docs/resume.md` → 지정 task 1파일의 3단계 읽기 정책, `docs/{adr,architecture,runbooks,reviews,tasks}` 분리, 5열 task 원장과 validator 2종, 실행마다 새 report를 만드는 2인 독립 적대적 리뷰 아카이브를 갖는다. 그중 하드웨어·차량·firmware 항목(F21·F25·F27·F41~F44, A6.2~A6.8 등)은 라이브러리에 불필요하다.

canview와 다른 점도 있다. canview는 `docs/decisions.md`와 `adr/README.md`를 이중 색인으로 관리하고(R2.7), validator가 절대 접두 2종을 허용하며(R6.2), 정본 환경이 Windows PowerShell이다(A5.1). 조사 문서 `docs-conventions.md`는 체크박스 원장을 제안했으나 common 작업 트리의 `validate_plan.py`는 5열 표를 요구한다(Q3). 소비자 7개 중 map·geo가 파일별 ADR, ktc·ktdm·pinvi가 단일 `decisions.md`를 쓴다(`dc` §1.8).

## 결정

1. canview 계층(`AGENTS.md` → `docs/README.md` → `docs/resume.md` → 지정 task 1파일)과 `docs/{adr,architecture,runbooks,reviews,tasks}` + validator 2종을 채택한다. 하드웨어·차량·firmware 항목은 제외한다. 항목별 판단은 `docs/architecture/canview-checklist.md`가 정본이다.
2. 추가 파일: `CLAUDE.md`(40줄 이하 포인터, 읽기 순서에 넣지 않음), `docs/standards/`, `docs/survey/`(조사; 규범 아님), `docs/plan/`, `docs/dev-environment.md`, `docs/integration-map.md`(생성물), `docs/architecture/adoption-readiness.md`·`canview-checklist.md`, `packages/`, `templates/`, `versions.json`, 고지 파일군.
3. **`docs/decisions.md`는 두지 않는다.** `docs/adr/README.md`가 단일 색인이며 상단에 "다음 후보 번호는 ADR-NNN"을 명시해 canview R2.7의 기능을 보존한다.
4. task 원장은 5열 표 + `READY/BLOCKED/IN_PROGRESS/DONE` + P0~P3, `validate_plan.py` 무변경. `docs/tasks-done.md`는 5열 고정이므로 완료 날짜는 제목 열 괄호에 적는다. ID 대역은 common 6대역 + 앱 대역(`docs/tasks-rule.md` §2.1; 앱 대역에는 버전·lock·CI·토큰·UI 채택만, Python 모듈 채택은 T-480~T-489).
5. 링크는 저장소 상대 경로만 허용하고 절대 경로는 validator 오류다. 검증 도구는 Python stdlib을 유지한다.
6. 리뷰 gate는 canview full gate를 그대로 채택한다: 전문 영역이 다른 2인 독립·상대 결과 비공개·동일 manifest·immutable 기준선(object-only 명령 4개 또는 detached worktree)·P0~P3·disposition `OPEN/FIXED/REJECTED_WITH_EVIDENCE/DEFERRED`(DEFERRED는 P2/P3만)·post-fix 재검토·evidence 파일·archive index. 상태 어휘 `IN_REVIEW/COMPLETE/POST_FIX_REVIEW`, verdict `BLOCK/CONDITIONAL/PASS`, post-fix는 별도 `-post-fix.md`, 같은 날 같은 범위 반복은 `-02`. 비면제 목록은 `docs/standards/*`·`versions.json`·`packages/*` 공개 API·CSS·`.github/workflows/*`·AGENTS/SKILL/docs README/ADR/runbook/task·review 규칙이며 면제는 오탈자·동의 링크 수정뿐이다. light/full 판정 주체는 merge 담당(작성자 ≠ 판정자)이다.
7. 소비자에게는 공통 절 B(Ruthless Review) + TEMPLATE + full/light 표준과 "ID 재번호 금지·완료 시 evidence 보존·요약에 acceptance 복제 금지·비단순 task는 상세 파일" SHOULD만 배포하고 원장 형식은 규정하지 않는다.

## 대안 검토

- **`decisions.md` 이중 색인 유지**: canview와 동일하지만 두 표의 불일치를 검사하는 도구가 없고 ktdm DO NOT 15 계열(이중 선언 금지)과 어긋난다. 단일 색인 + 상단 번호 명시로 대체했다.
- **체크박스 원장 + 새 `validate_task_ledger.py`**: 소비자 관례(map·geo)와 가깝지만 validator를 새로 써야 하고 35 tests 계약을 버린다. 5열 표는 이미 검증기가 있다.
- **절대 링크 접두 허용 유지**: 다른 체크아웃 경로에서 깨지는 링크를 허용하게 되므로 제거했다. 다른 저장소 파일은 커밋 고정 GitHub URL로 인용한다.
- **light 리뷰를 작성자가 판정**: 면제 남용을 막을 수 없어 merge 담당이 판정한다.

## 결과

- 에이전트는 중앙 인덱스에서 작업과 직접 관련된 문서만 점진적으로 읽고, 현재 설계·결정·작업·절차·역사의 정본이 분리된다.
- 리뷰 기준선·2인 관점·disposition이 실행별로 감사 가능하다.
- validator 2종이 무변경이므로 canview의 문법 계약(cv §4)이 그대로 유효하고 회귀 테스트 35건을 재사용한다.
- 문서 이동 시 incoming link·plain path·상위 인덱스를 함께 검증해야 하며, 절대 링크가 섞인 복사본은 즉시 실패한다.

## 후속·적용 위치

- 정책과 읽기 계층: `AGENTS.md`, `SKILL.md`, `CLAUDE.md`, `docs/README.md`
- 원장·리뷰 규칙: `docs/tasks-rule.md`, `docs/reviews/README.md`, `docs/runbooks/agent-workflow.md` §5, `docs/runbooks/documentation-maintenance.md`
- 대조표: `docs/architecture/canview-checklist.md`(T-001)
- 소비자 배포판: `templates/AGENTS.common.md`, `docs/standards/agent-conventions.md`(T-007)
- 도구 정비: T-002(`docs.yml` unittest 범위·Windows 동작)
