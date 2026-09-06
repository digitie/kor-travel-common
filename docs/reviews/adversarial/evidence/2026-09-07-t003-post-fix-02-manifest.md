# T-003 두 번째 post-fix 공통 manifest

- Candidate: `a2c189185870b3b1ea124531feb36b59b5533f65`
- Base: `951b4432bc8eb4391caf15ad0eb2e8f8f58eb02a`
- 범위: 전체 10파일 delta, A-T003-P1-01의 확장자 별칭 잔여·정상 대문자 소스 검사·Windows 끝 점/공백·editorconfig 대소문자, 이전 판정 보존. [이전 통합](../2026-09-07-t003-post-fix.md).
- 정본: [licensing §5.2](../../../standards/licensing.md#52-검사-범위와-출처-대조), [T-003](../../../tasks/T-003-notices-provenance-spdx.md), [agent workflow](../../../runbooks/agent-workflow.md). A는 경로·실패 경계, B는 고지 계약·기존 수정 회귀를 우선하며 전체 delta도 검토한다.
- 원문 사본·고지 전달·geo 식별 로직은 불변이며 지난 검증을 재사용한다. 사용자의 GPLv3 통일 예정은 journal의 미래 방향 기록일 뿐 현재 원천 식별자·권리 gate 변경이 아니다.
- 동일 reviewer별 detached worktree를 candidate로 전환했다. 시작·종료 SHA와 clean 확인. 이번 결과는 상대에게 공유하기 전에 독립 확정한다.
- 검사: 전체 unittest(작성자 Windows/WSL 100개 성공·skip 0), SPDX, 문서·plan, diff check와 기존 A의 재현 경계. 원문 재다운로드·소비자 수정·제품 구현은 범위 밖.
- 각자 `2026-09-07-t003-post-fix-02-reviewer-a.md` 또는 `2026-09-07-t003-post-fix-02-reviewer-b.md` 한 파일을 이 디렉터리에 작성한다. 실행 ID·시각·요청 원문·실제 SHA/clean·disposition·새 finding·검증/NOT_RUN·verdict를 포함하고 기존 원본·다른 파일은 수정하지 않는다.
