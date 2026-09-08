# T-103 반복 리뷰 근본 수정 기준선

- 단계: post-36 이후 상태 스택 교체의 독립 post-fix 검토
- 코드 후보: `b013ab0d2e95e3d892f6dbfa42042389582ea8a9`
- 후보 tree: `de5b30f25840bd9da19f073f62ae6bc9607fa7ef`
- parent·수정 delta 기준: `841ee985db564deb0d571edb6f0f9330311a35d6`
- 수용 기준: [T-103](../../../tasks/T-103-kt-contrast-ux-lint.md), [근본 원인 분석](../2026-09-08-t103-root-cause.md)
- 이전 원본: [post-36 A](2026-09-08-t103-post-fix-36-reviewer-a.md), [post-36 B](2026-09-08-t103-post-fix-36-reviewer-b.md)

## 동일 전달 요청

상태 추정 helper를 상태 스택으로 교체한 전체 delta와 자신의 누적 finding closure를 독립적으로 검사한다. 상대 reviewer의 이번 결과는 두 원본 확정 전 읽거나 전달받지 않는다. 별도 detached worktree에서 시작·종료 HEAD/tree와 clean을 확인한다. 제품 코드는 수정하지 않고 한국어 raw report 한 파일만 별도 commit한다. 기준선 관찰·실행 ID·시각·실제 명령·미검증 범위·finding의 위치/재현/영향과 최종 verdict를 기록한다.

- A: MDX/JavaScript 문맥 전환, 원본 P1 누락과 P2 오탐, 본문·표현식·ESM·JSX·template의 수명과 좌표 보존.
- B: 참조 파서와 기대값의 독립성, `--base` 추가행, 컨테이너·줄 종결자 변형, 기존 TS/TSX/CSS·CLI 계약·의존성과 evidence 정합성.
- 산출물: `2026-09-08-t103-root-fix-reviewer-a.md`, `2026-09-08-t103-root-fix-reviewer-b.md`(이 디렉터리).
- 심각도·판정은 [workflow](../../../runbooks/agent-workflow.md)의 `P0`~`P3`, `BLOCK/CONDITIONAL/PASS`를 사용한다. P0/P1은 재현·수정 확인 없이는 닫지 않는다. 코드가 바뀌지 않은 전체 시험은 정확한 후보 evidence/CI 확인으로 재사용할 수 있지만 자신의 실행으로 세지 않는다.

## 수정 범위

`tools/ux_lint.py`의 MDX 마스킹, `tests/test_ux_mdx_context.py`, `tests/fixtures/ux/mdx-contexts.json`, 개발 대조 전용 `tests/verify_mdx_reference.mjs`, T-103의 MDX 수용 기준, 원인 분석과 resume 포인터다. 제품 런타임은 stdlib만 유지한다. 근거 없이 JS 문맥을 여는 본문 prefix·식별자 추정을 없애고 실제 표현식·태그·ESM 진입과 닫힘을 스택 한 곳에서 소비한다. 기존 fence 계산·패턴·baseline·Git diff·출력 계약은 보존한다.

## 작성자 실행 evidence

아래 결과는 코드 후보와 동일한 파일 내용에서 실행했다. 그 뒤 변경은 이 manifest 기록뿐이다.

| 검증 | 명령·결과 |
|---|---|
| Windows 전체 | `python -B -X utf8 -m unittest discover -s tests -p 'test_*.py'`: 317 실행·성공, skip 0, 162.699초, exit 0 |
| WSL 전체 | `wsl.exe --cd /mnt/f/dev/kor-travel-common -- python3 -B -X utf8 -m unittest discover -s tests -p 'test_*.py'`: 317 수집, 316 실행·성공, Windows 전용 1 skip, 111.642초, exit 0 |
| 누적 문맥 시험 | 위 전체 시험에 50개 자료의 문맥·줄바꿈 변형 408건과 delimiter 변형 120건, 50개 파일의 기존행/추가행 CLI 비교를 포함 |
| 실제 MDX 대조 | `node tests/verify_mdx_reference.mjs .git/codex-audit/mdx-oracle/node_modules/@mdx-js/mdx/index.js`: 고정 3.1.1, 396 PASS, 호환 문법 2건 NOT_RUN, exit 0 |
| 문서·계획 | `validate_document_links.py`: 503문서·2506대상 오류 0; `validate_plan.py`: 106 task 오류 0 |
| 코드 고지·정보 검사 | `check_spdx.py`: 58파일 오류 0; `scan_secrets.py --all`·`check_prod_redaction.py --all`: 각 638파일 finding 0 |
| 기존 도구 | canonical 대비 27쌍 PASS; UX fixture report finding 12·fail_count 0; aliases CSS 1 오류 0; versions self-check PASS |
| diff | `git diff --staged --check` 오류 0, stage 전체 직접 감사 완료 |

## 미실행과 범위 밖

- 정확한 후보 CI `34214642467`: manifest 작성 시 실행 대기, merge 전 6개 job을 별도 확인한다.
- 소비자 저장소 build/e2e·버전 검사: `NOT_RUN(다른 저장소 수정·실행 없이 common만 작업)`; 상세 task의 외부 이관 task 소유.
- 실제 MDX compile/render/browser: `NOT_RUN(이 검증은 구문 트리와 기대값의 대조)`.
- Windows Python 3.11: `NOT_RUN(실행 파일 부재)`; WSL 3.11과 Windows 3.14 실행을 이 결과로 대체 표기하지 않는다.
- npm/PyPI 게시: 사용자 지시에 따라 수행하지 않는다. 참조 파서는 개발 임시 경로에만 설치하며 제품 의존·배포 자산에 넣지 않는다.
