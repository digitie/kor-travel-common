# T-013 PR #1·로컬 초안 통합과 순차 실행 계획·인계 마무리 (2026-09-06, PR #1)

- 상태: DONE
- 우선순위: P0
- Gate: 문서 검증·도구 테스트·CI·2인 리뷰
- 선행: 없음

## 목표

2026-09-06 사용자 요청에 따라 PR #1의 커밋과 로컬 미커밋 초안을 대조하고, 다음 에이전트가 task를 하나씩 실행할 수 있는 계획과 인계를 완성한다. 기존 draft PR #1을 이어 사용한다. 이 task의 완료는 패키지 구현·소비자 이관 또는 Phase 0 전체 완료를 뜻하지 않는다.

## 고정 결정

- 정책·우선순위는 [AGENTS](../../AGENTS.md), 설계 경계는 [architecture](../architecture/README.md), 문서 역할은 [문서 유지보수](../runbooks/documentation-maintenance.md)를 따른다.
- 기존 초안의 주장보다 코드·정본 문서·실행 결과를 우선한다. 구조적 결정을 바꾸면 [ADR 색인](../adr/README.md)에 후속 ADR을 등록한다.
- 리뷰는 [agent workflow](../runbooks/agent-workflow.md)의 동일 immutable 기준선과 서로 다른 전문 영역 2인 독립 적대적 리뷰로 수행한다.

## 구현 범위

1. PR #1 기준 커밋·로컬 초안·실제 파일·검증 결과를 기록하고 누락된 task 원장과 통합 계획을 작성한다.
2. 상세 task의 선행·외부 선행·범위·수용 기준을 대조한다. 순환·숨은 선행·미구현 도구를 성공으로 취급하는 지침을 수정한다.
3. 문서 링크·CI 검사 대상·실제 구현과 문서의 불일치를 수정한다. 출처·미확인 버전·미실행 검증을 확정 사실로 표시하지 않는다.
4. 두 리뷰어 원본·manifest·통합 disposition·post-fix 재검토를 보존하고 실제 gate가 닫힌 task만 완료 원장으로 이동한다.
5. 의미 있는 변경 묶음마다 명시 경로 stage·diff 검사·커밋·push하고 draft PR #1의 목적·검증·리뷰·잔여 위험·evidence·rollback을 갱신한다.

## 범위 밖

소비자 저장소 직접 수정, 라이선스·계정 권한 승인, 패키지 구현·릴리스, PR merge. 해당 작업은 후속 task와 외부 선행으로 남긴다.

## 예상 변경 파일

`docs/tasks.md`, `docs/tasks-done.md`, 관련 `docs/tasks/T-*.md`, `docs/plan/integration-plan.md`, `docs/resume.md`, `docs/journal.md`, 불일치가 확인된 문서·도구·CI, `docs/reviews/adversarial/`와 리뷰 색인.

## 수용 기준

- 원장과 모든 상세 task의 제목·상태·우선순위·선행이 일치하며 DAG 검사 오류가 없다.
- 통합 계획에 한 작업 선택 규칙·단계별 출구·외부 대기 시 다음 선택·rc 검증과 정식 채택의 경계가 있다.
- 문서 링크·unittest·공백 검사와 PR CI가 통과한다. 수치·기준 커밋·미실행 이유를 기록한다.
- 두 리뷰어가 같은 기준선을 독립 검토하고 모든 finding에 disposition이 있다. P0/P1은 원 reviewer 재확인으로 닫힌다.
- 다음 한 작업·시작 파일·잔여 차단 조건이 resume에 있고 draft PR #1과 리모트 branch가 최종 커밋을 가리킨다.

## 검증 명령

```bash
python3 -B -X utf8 tools/validate_document_links.py
python3 -B -X utf8 tools/validate_plan.py
python3 -B -X utf8 -m unittest discover -s tests -p "test_*.py"
git diff --check
gh pr checks 1
```

Git Bash에서 동일. Windows 치환은 [개발 환경](../dev-environment.md) §5를 따른다.

## evidence

2026-09-06 완료: PR #1의 09104ed와 로컬 초안을 인수해 96개 상세 task 원장·순차 실행 계획을 완성했다. 최초 14건과 후속 1건의 finding을 수정했고 두 원 reviewer가 모두 FIXED로 재확인했다. 완료 문서 task만 archive로 이동하고 다음 한 작업은 T-003, 이후 T-005·T-009로 지정한다. 기존 draft PR #1을 갱신하며 소비자 변경·패키지 구현·릴리스·merge는 후속 범위다.

검증 기준선·CI·2인 gate·원본·실행 수치·NOT_RUN은 [통합 재검토](../reviews/adversarial/2026-09-06-phase0-post-fix-03.md)에 보존한다. 완료 원장 이동과 인계 문서의 후속 delta도 같은 두 리뷰어의 별도 immutable 기준선 검토 대상으로 삼으며 최신 판정은 [리뷰 색인](../reviews/README.md)을 따른다.

## rollback 또는 release 차단 조건

각 변경 커밋을 역순으로 revert한다. 원래 로컬 초안은 커밋 이력으로 보존한다. 리뷰·필수 검사 미완료이면 이 task를 DONE으로 바꾸지 않는다. 패키지·소비자 검증은 NOT_RUN(이번 범위에 실물 패키지·소비자 변경 없음)이며 릴리스 허가로 해석하지 않는다.
