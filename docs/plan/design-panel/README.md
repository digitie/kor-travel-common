# 설계 판정 산출물 (2026-09-06)

이 디렉터리는 [설계 브리프](../design-brief.md)를 확정하기 위해 실행한 설계 판정의 원본 산출물이다. 규범이 아니라 **역사 기록**이며, 현재 결정의 정본은 브리프와 ADR·규칙 문서다.

| 파일 | 역할 |
|---|---|
| [register-coordinator-draft.md](register-coordinator-draft.md) | coordinator(Claude)의 초안 결정 레지스터(D-01~D-18 + F절 메모) |
| [register-risk-first.md](register-risk-first.md) | 설계자 A(위험·정확성 우선) 독립 설계안(D-01~D-27, task 79) |
| [register-velocity-first.md](register-velocity-first.md) | 설계자 B(소비자 이관 속도 우선) 독립 설계안(D-01~D-24, task 80) |
| [judge-fact-consistency.md](judge-fact-consistency.md) | 판정자 1: 조사 문서·원 저장소 사실과의 정합, 내부 모순 |
| [judge-migration-feasibility.md](judge-migration-feasibility.md) | 판정자 2: 7개 앱 이관 PR 수·규모·DAG 실현성 |
| [judge-directive-fidelity.md](judge-directive-fidelity.md) | 판정자 3: 사용자 지시 (1)~(7)·canview 충실도·GPL 조치 |

절차: 두 설계자는 서로의 산출물을 보지 않고 같은 조사 문서와 초안을 입력으로 독립 작성했다. 세 판정자는 세 레지스터를 D-ID별로 대조해 승자·병합 문안·심각도·누락 결정·사실 오류를 보고했다. coordinator가 세 판정의 합의 문안을 채택하고 갈린 항목은 브리프의 "채택 사유"에 근거를 적어 확정했다. 파일 안의 경로는 작성 당시 임시 디렉터리를 이 디렉터리로 치환한 것이다.
