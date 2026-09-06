# Phase 0 post-fix 공통 manifest

- Review ID: 2026-09-06-phase0-postfix
- Candidate: `12fb3a816e5ebbdf9822a2c17ea7ad5534195fb9`
- Base: `d3712a8c965c3193a5af13cacd6d22c603e0cfe4`; PR base `b92fabeb1c96a11c1fc9507d93271c1ebeee09b0`.
- 요청·역할·범위·독립성: [최초 manifest](2026-09-06-phase0-manifest.md)를 그대로 따른다. 각자 원 finding 전부와 base→candidate 전체 변경의 회귀를 공격한다. 상대의 post-fix 결과는 자기 원본 확정 전 읽지 않는다.
- 수정 안내: e9a3a0f inline code/Linux CI, 905779f 버전 입력/범위/ref·완료 원장, 12fb3a8 ADR-013·선행 DAG·L6·minor별 task·공개 facade·승인 smoke.
- A: 원 음성 사례 재실행, parser/registry/ref 경계와 Linux 회귀, 미실행 성공 처리 검사.
- B: 실제 순차 선택 시뮬레이션과 본문 선행, pinvi/airport 두 경로·릴리스별 내용물·공개 계약 검사.
- 격리: 기존 detached reviewer worktree의 HEAD를 candidate로 바꿨으며 clean을 먼저 확인했다. 각 reviewer도 시작·종료 hash/clean을 독립 확인한다.
- 원본 파일: `2026-09-06-phase0-postfix-reviewer-a.md` 또는 `-b.md` 하나만 main checkout evidence 디렉터리에 작성한다. 기존 원본·코드·문서는 수정하지 않는다.
- 결과: 원 finding별 FIXED/OPEN/REJECTED 근거·새 finding·명령/시험 수/NOT_RUN·실행 ID/시각·verdict. 태그 발행·소비자 수정·승인은 범위 밖이다.
