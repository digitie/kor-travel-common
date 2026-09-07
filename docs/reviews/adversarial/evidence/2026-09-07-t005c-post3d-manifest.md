# T005c post-fix 03d workflow 정적 보고 독립 review manifest

- Review ID: T005C-20260907-POST3D
- Candidate: 5807e535c16310c41c21f9efce87b2113aa17ee5
- Candidate tree: 5f5ce75f627c3b786a96c81532044ce100b30a0c
- Parent: 0f55acc2211718d91ce056b096046054b037d7e4
- Branch: codex/t005c-workflow-static-report
- Task: docs/tasks/T-005c-workflow-static-report.md
- 범위: post-fix-02 이후 workflow parser·redaction·repo policy·Docker 경계 코드와 회귀 시험
- 목적: post-fix-02 P1/P2 finding과 post-fix-03C의 flow quoted item delimiter 경계를 immutable candidate에서 재현하고 닫는다.
- 수용: 민감값과 경로·repo·mode_source가 stdout/JSON/Markdown/annotation/step summary에 남지 않음; 원 repo 식별자로 exception/enforce가 유지됨; malformed input은 exit 2; 유효 constrained YAML·Docker separator/registry 및 단일 repository 규칙은 유지; plain scalar·flow quoted item의 quote/colon/comma/bracket 문맥을 보존; Windows/WSL parity; 전체 test와 validators 기록.
- 범위 밖: 전체 YAML parser, 원격 action/version 조회·실행, Docker pull/inspect, 소비자 저장소 수정, package build/install/publish, npm/PyPI 게시.
- 규칙: exact candidate에서 detached clean worktree를 만들고 시작·종료 SHA/tree/status를 기록한다. 후보와 소비자 파일을 수정·commit·push하지 않는다. 상대 reviewer raw와 이전 post-fix raw/report를 읽지 않는다. 각 reviewer는 서로 다른 전문 영역에서 독립적으로 재현하고 P0-P3 finding·NOT_RUN·verdict를 raw에 남긴다.
- Reviewer A 요청: parser/YAML quote·indicator·flow/list·run/with 구조·workflow 출력 redaction·repo identity regression·Docker single repository·plain/flow delimiter quote·회귀시험.
- Reviewer B 요청: redaction policy parity·registry exception/enforce·Docker Distribution name grammar·plain/flow delimiter quote·출력 채널·docs/CI 정합성·Windows/WSL parity.
- Raw targets: .git/codex-audit/2026-09-07-t005c-post3d-reviewer-a.md, .git/codex-audit/2026-09-07-t005c-post3d-reviewer-b.md
