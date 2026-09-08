# T-103 실제 MDX 파서 전환 독립 리뷰 기준선

- 코드 후보: `31e3f0affd2ce1c32ac912bedf687d82c12ee876`
- 후보 tree: `249c38a4fab91903f9536c6c7f6c938efeab0445`
- parent·delta 기준: `196a8a37754848bb3fabef6c5bb9e5c2dd275608`
- 수용 기준: [T-103](../../../tasks/T-103-kt-contrast-ux-lint.md), [ADR-016](../../../adr/016-mdx-parser-for-ux-lint.md)
- 이전 독립 원본: [A](2026-09-08-t103-root-fix-reviewer-a.md), [B](2026-09-08-t103-root-fix-reviewer-b.md)

## 동일 전달 요청

36회 반복 원인이던 수동 MDX 파서를 제거하고 실제 구문 분석으로 전환한 전체 delta를 검토한다. 두 reviewer 모두 이 manifest의 동일 불변 후보에서 작업한다. 별도 detached worktree의 시작·종료 HEAD/tree·clean을 확인하고, 그 worktree 루트에서 `npm ci --ignore-scripts`로 잠긴 의존을 설치한다. 제품·시험 파일을 수정하지 않고 한국어 원본 report 하나만 별도 commit한다. 상대의 이번 결과는 두 원본 확정 전 읽거나 전달받지 않는다. 실행 ID·역할·시각·전달 요청·실제 명령·관찰과 미검증을 구분한다.

- A: 실제 AST 마스킹·Unicode 좌표·MDX 문법, 변경된 기존 시험 기대값의 타당성, 자신의 누적 finding과 A-P1-35·A-P2-36·A-P1-37 해결을 재현한다.
- B: Node 의존·lock·설치·CI, 실패 시 exit 2·오류 정보 보호·사용자 소스 실행 금지, Git CLI와 자신의 누적 finding 및 B-P1-30·B-P2-31·B-P2-32 해결을 재현한다.
- 산출물: 이 디렉터리의 `2026-09-08-t103-parser-reviewer-a.md`, `2026-09-08-t103-parser-reviewer-b.md`.
- 심각도·verdict는 [workflow](../../../runbooks/agent-workflow.md)의 `P0`~`P3`와 `BLOCK/CONDITIONAL/PASS`다. 취향·범위 밖 개선을 새 필수 계약으로 추가하지 않되 재현되는 실질 결함은 남긴다. 원본 심각도를 보존하고 P0/P1은 원 reviewer 재확인 없이 닫지 않는다. full/light도 작성자 대신 reviewer가 판정한다.

## 검토 범위와 판단 근거

후보의 18개 변경 파일 전체: Python adapter·새 `tools/mdx_mask.mjs`, 64개 누적 자료와 시험·AST 기대값 대조, package와 lock, docs CI의 Node 설치, ADR-003 부분 대체·ADR-016 및 색인, 개발 환경·task·도구 문서·CHANGELOG·resume, Airport dark evidence 정정이다. T-103 전체 기존 대비·UX CLI 계약도 회귀 범위다.

상태 스택 교체만으로는 ESM 연속·정규식·비교 연산자의 정상 문법 결함이 남았으므로 lexer 자체를 제거했다. 설치 실패나 잘못된 MDX는 추정 검사로 대체하지 않는다. 사용자 코드는 parse만 하며 compile/evaluate하지 않는다. MDX가 없으면 Node 없이 동작한다. 기존 시험의 CommonMark 가정·잘못된 MDX 입력을 공식 MDX 문법에 맞췄고, 모든 변경 이유는 ADR-016에 연결한다. 제품과 대조 스크립트는 같은 MDX 파서를 쓰므로 서로 독립적인 두 파서의 일치로 주장하지 않는다.

## 작성자 실행 evidence

아래 시험은 후보와 동일한 코드·시험 내용에서 실행했다. 이후 수정은 문서 정리뿐이다.

| 검증 | 명령·결과 |
|---|---|
| Windows 전체 | `python -B -X utf8 -m unittest discover -s tests -p 'test_*.py'`: 320 실행·성공, skip 0, 210.432초, exit 0 |
| 기존 UX 시험 | `python -B -X utf8 -m unittest discover -s tests -p 'test_ux_lint.py'`: 53 실행·성공, skip 0, 98.419초, exit 0 |
| 누적 자료 | 전체 시험에 64개 입력·문맥/줄 종결자 492변형·delimiter 120변형과 64파일 Git 기존행/추가행, 문법 오류·파서 실패·좌표·실행 금지 시험 포함 |
| AST 기대값 | `node tests/verify_mdx_reference.mjs node_modules/@mdx-js/mdx/index.js`: 492 PASS, 실패·제외 0, exit 0 |
| 문서·계획 | `python -B -X utf8 tools/validate_document_links.py`: 507문서·2537대상 오류 0; `python -B -X utf8 tools/validate_plan.py`: 106 task 오류 0 |
| 고지·정보 검사 | `python -B -X utf8 tools/check_spdx.py`: 59파일 오류 0; `scan_secrets.py --all`·`check_prod_redaction.py --all`: 각 643파일 finding 0 |
| diff | `git diff --staged --check` 오류 0, 18파일 staged diff 전체 직접 감사 완료 |

## 실행 대기·실패·범위 밖

- WSL Python 3.14.4와 명시적 Python 3.11.15 전체 시험은 manifest 작성 시 실행 중이며 결과를 추정하지 않는다. 종료 결과는 새 통합 report에 기록한다.
- 이 코드 후보 CI는 push 후 대기 중이다. merge 전에 정확한 source의 6개 job을 확인한다.
- 이전 수동 파서 후보는 두 reviewer BLOCK이다. 위 finding의 새 후보 확인 전 PASS로 바꾸지 않는다.
- 최초 실제 파서 전환 시험은 기존 53개 중 8개 실패했다. 문법이 잘못된 JSX fixture와 MDX가 지원하지 않는 indented code 가정을 바로잡은 뒤 53개가 통과했다.
- Airport dark 예제는 10미달·baseline 적용 후 신규 6건, 예상 exit 1이다. 과거 성공 표기를 정정했으며 값·baseline을 조작해 통과시키지 않았다. 실제 dark 채택은 T-431 외부 gate다.
- 소비자 build/e2e·실제 MDX compile/render/browser: `NOT_RUN(다른 저장소 실행과 실제 앱 채택은 외부 이관 task)`.
- Windows Python 3.11: `NOT_RUN(로컬 실행 파일 부재)`; CI의 별도 실행을 로컬 결과로 표현하지 않는다.
- npm/PyPI 게시: 사용자 지시에 따라 수행하지 않는다. 라이브러리 소비자에게 이 도구용 Node 의존을 추가하지 않는다.
