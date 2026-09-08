# T-103 MDX 파서 원문 좌표 보정 재검토 기준선

- 코드 후보: `49d3867fd8fb941fde260966d2b4b3296c0f3d77`
- 후보 tree: `e2bfb5702ad976bfda5d47ddc6e52f2f735e440b`
- parent: `71dc7c2a806caa87738ea9b5da6ab9c896db5980`; 제품 delta 기준: `31e3f0affd2ce1c32ac912bedf687d82c12ee876`
- 앞선 동일 요청과 범위: [실제 파서 manifest](2026-09-08-t103-parser-manifest.md)
- 확정 원본: [A BLOCK](2026-09-08-t103-parser-reviewer-a.md), [B PASS](2026-09-08-t103-parser-reviewer-b.md)
- 수용 기준: [T-103](../../../tasks/T-103-kt-contrast-ux-lint.md), [ADR-016](../../../adr/016-mdx-parser-for-ux-lint.md). 새 요구나 심각도 변경은 없다.

## 동일 전달 요청

두 reviewer는 위 동일 후보의 별도 detached worktree에서 시작·종료 HEAD/tree·clean을 확인한다. `npm ci --ignore-scripts`로 해당 후보의 의존을 설치하고, 제품과 시험은 수정하지 않는다. 원본 `2026-09-08-t103-parser-post-fix-reviewer-{a,b}.md` 하나만 별도 commit한다. 실행 ID·시각·역할·입력 요청·실제 명령·미실행·verdict를 기록하고 두 원본 확정 전 상대의 이번 결과를 공유하지 않는다.

검토 대상은 전체 제품 delta 4파일과 기존 finding 회귀다. `tools/mdx_mask.mjs`의 첫 BOM 한 문자 offset을 모든 AST range에 적용하는 보정, 대조 스크립트의 같은 원문 좌표 보정, 누적 BOM 입력 2건, 원문 마스킹·Git CLI 시험 2개다. A는 A-P1-38과 Unicode/문법 마스킹 경계를, B는 같은 변경이 CLI·실패 처리·기존 누적 결과에 미치는 영향을 독립 확인한다. 심각도·verdict는 정본의 `P0`~`P3`, `BLOCK/CONDITIONAL/PASS`를 사용한다. 이전 원본의 기존 finding FIXED 판정은 보존하되 관련 회귀를 확인한다.

## 조치와 작성자 검증

고정 MDX 파서는 파일 첫 U+FEFF 한 문자를 제외한 offset을 반환한다. 원문은 그대로 두고 모든 code·inlineCode·JS comment range를 원문 기준으로 한 번 변환했다. 나머지 UTF-16/Unicode 마스킹, Node 실행, Git 판정과 출력에는 변경이 없다. BOM을 검사 제외하거나 입력 오류로 우회하지 않는다.

- `python -B -X utf8 -m unittest tests.test_ux_mdx_context -v`: 8개 실행·성공, skip 0, 12.367초, exit 0. 원문 마스킹 54경우, BOM0/1/2×줄바꿈3×주석2의 18파일과 plain/base 36관찰을 포함한다.
- `node tests/verify_mdx_reference.mjs node_modules/@mdx-js/mdx/index.js`: 누적 66입력의 498변형 PASS, 실패·제외 0. 기존 delimiter 120변형도 위 집중 시험에 포함한다.
- 링크 508문서·2542대상 오류 0, plan 106 task 오류 0, SPDX 59파일 오류 0, staged diff 4파일 전체 직접 감사·공백 오류 0.
- 작성자 Windows 전체 322 시험은 manifest 작성 시 실행 중이다. 새 후보 CI는 이 manifest와 확정 raw를 함께 push한 source에서 별도 확인한다. 이전 후보 CI `34217374527`의 6 job 성공을 새 후보 실행으로 표시하지 않는다.
- 앞선 작성자 WSL 전체 두 실행은 NTFS 의존 로딩으로 장시간 진행돼 중단했다. 성공으로 세지 않으며, 이전 후보의 독립 B WSL 317실행·3skip 및 CI와 구분한다. 새 후보 Linux 검증은 CI 및 reviewer의 실제 실행으로 확인한다.
- BOM 회귀 시험 초안은 이중 FEFF 바로 뒤 fence도 code라는 잘못된 기대 3건으로 실패했다. 파서는 첫 BOM 하나만 제거하므로 두 번째 FEFF가 본문인 입력임을 확인했고, fence 앞 줄 구분을 명시해 정상 fence로 검사한다. 직접 기대 마스킹과 실제 입력 의미를 함께 검증한다.
- 소비자 build/e2e·실제 compile/render·npm/PyPI 게시: 기존 `NOT_RUN` 범위를 유지한다. 사용자 최신 지시는 현재 PR merge 후 대기이며 다음 task를 실행하지 않는다.
