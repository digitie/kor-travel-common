# T-003 post-fix 공통 manifest

- Candidate: `951b4432bc8eb4391caf15ad0eb2e8f8f58eb02a`
- Base: `017fef1ca0aa8ca28d0ccf8cfc35fffa71149e64`
- 범위: [최초 통합 리뷰](../2026-09-07-t003.md)의 6 finding 수정과 전체 delta 15파일. [T-003](../../../tasks/T-003-notices-provenance-spdx.md)은 IN_PROGRESS이며 제품·소비자·CI 확장은 후속 task다.
- A는 경로·SPDX·회귀, B는 출처·고지 전달·정본·evidence를 우선하되 전체 delta도 확인한다. 최초 두 원본은 확정됐으므로 교차 대조 가능하다. 이번 post-fix 결과는 서로 공유하지 않고 먼저 독립 확정한다.
- 격리: 기존 reviewer별 detached worktree를 candidate로 전환했다. 시작·종료 HEAD·porcelain clean을 확인한다.
- 실행: `python -B -X utf8 tools/check_spdx.py`, 문서/plan validator, `python -B -X utf8 -m unittest discover -s tests -p 'test_*.py'`, `git diff --check <base> HEAD`. WSL은 python3. 원문 사본 자체는 변경되지 않았으므로 지난 고정 원문 대조를 재사용할 수 있다.
- 산출물: 이 디렉터리의 `2026-09-07-t003-post-fix-reviewer-a.md`, `2026-09-07-t003-post-fix-reviewer-b.md` 각자 한 파일. 실행 ID·시각·요청 원문·immutable SHA·clean·원 finding별 disposition·전체 delta·새 finding·검증·NOT_RUN·verdict 포함.
- 소비자 checkout 변경, 제품·문서 수정, 상대 보고서 변경은 금지한다. 작성자의 98 tests 통과 주장은 reviewer의 독립 재현을 대신하지 않는다.
