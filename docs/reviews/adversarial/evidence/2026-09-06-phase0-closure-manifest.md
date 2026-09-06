# Phase 0 문서 task 종료 공통 manifest

- Review ID: 2026-09-06-phase0-closure
- Candidate: `8fb1334381f8fd8d6a3da217244ef2ad136bf020`
- Base: `56706423bf9948909e872aa9a76229666984d289`.
- 두 reviewer는 [최초 manifest](2026-09-06-phase0-manifest.md)의 역할·독립성을 유지한다. 각자 원본 확정 전 상대의 이번 결과를 읽지 않는다.
- 범위: 6개 문서 task DONE과 H1/완료 원장/evidence, T-003·T-009 READY, 다음 T-003 인계, 문서 서두 상태·실물 후속 gate, review/journal 보존. 코드·시험·CI는 불변이며 이미 확인한 67 tests를 재사용한다. 전체 내용 재설계가 아닌 base→candidate 종료 delta의 회귀를 확인한다.
- 필수: 같은 detached checkout의 시작/종료 SHA·clean, 새 문서/plan/diff 검사. 가능한 경우 PR #1 draft·head SHA와 해당 CI를 읽기 전용 확인한다. 이미 완료한 내용 리뷰와 이번 종료 기록 검증을 구분한다.
- 원본 파일: main evidence의 `2026-09-06-phase0-closure-reviewer-a.md` 또는 `-b.md` 하나만 작성. 과거 원본·코드·다른 에이전트 변경을 보존한다.
- 출력: 시각·실행 ID·관찰 SHA/clean·명령/결과·새 finding/기존 disposition·verdict·NOT_RUN. 패키지·소비자·외부 승인·릴리스의 미완료는 유지한다.
- 두 PASS 이후 coordinator는 이번 원본·통합 종료 판정·리뷰 색인만 기록하는 closure artifact commit을 추가하고 그 commit의 CI·PR/리모트 정합을 확인한다. 해당 기록은 agent workflow의 closure 예외이며 규범 변경을 포함하면 새 리뷰가 필요하다.
