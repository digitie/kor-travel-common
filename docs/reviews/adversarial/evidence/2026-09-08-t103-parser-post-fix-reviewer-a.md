# T-103 MDX BOM 보정 독립 재검토 A 원본

- 실행 ID: `T103-PARSER-POST-A-20260908-200104-KST`; 최종 verdict: **PASS**.
- 시작: 2026-09-08 20:01:04.019 KST; 검증 완료 관찰: 2026-09-08 20:04:13.107 KST.
- 불변 제품 HEAD: `49d3867fd8fb941fde260966d2b4b3296c0f3d77`; tree: `e2bfb5702ad976bfda5d47ddc6e52f2f735e440b`.
- 제품 delta 기준: `31e3f0affd2ce1c32ac912bedf687d82c12ee876`. 공통 manifest는 `ef91306f3c29ec0bd753df4229428b6eb90965c4`의 `docs/reviews/adversarial/evidence/2026-09-08-t103-parser-post-fix-manifest.md`를 `git show`로 읽었다.
- 격리: `F:/dev/kor-travel-common-wt/review-t103-parser-post-a`의 detached worktree. 시작·종료 HEAD/tree는 위 값과 같고 `git status --short`는 모두 비어 있었다. 이후 이 원본 한 파일만 추가한다.
- 동일 요청: “검토 대상은 전체 제품 delta 4파일과 기존 finding 회귀다.” A 역할은 A-P1-38의 원문/AST/CLI 및 Unicode·문법 마스킹 경계 재검증이다. 이번 상대 결과·raw를 읽거나 요청하지 않았다.
- 후보·시험·manifest·소비자·기존 evidence·git config는 수정하지 않았다. 설치한 잠긴 의존과 자기 임시 fixture 외에 보고서 한 파일만 추가한다. 후속 구현 task는 시작하지 않는다.

## 변경과 disposition

제품 delta는 `tools/mdx_mask.mjs`, 개발 대조 스크립트, 누적 JSON 자료와 집중 시험의 4파일이다. Git diff에는 이전 parser manifest 한 파일도 포함되며 제품 변경과 구분했다. 전체 4파일 diff를 읽었다.

첫 U+FEFF를 파서가 소비한 경우에만 모든 code·inlineCode·JavaScript comment 범위에 1을 더하고, 기존 UTF-16/Unicode 마스킹 로직에 전달한다. 원문을 삭제하거나 BOM 문서를 검사 제외하지 않는다. offset 변환이 범위 병합 전에 한 번 적용되고 BOM 없는 입력에는 적용되지 않음을 확인했다. 이중 FEFF는 첫 문자만 파서가 소비하므로 1만 보정한다. 두 번째 FEFF의 Markdown 의미를 무시하지 않도록 fence 시험의 실제 줄 구분을 명시한 것도 타당하다.

- **A-P1-38 / P1: FIXED.** 원래 누락됐던 BOM1/2·LF/CRLF/CR·block/line 주석의 12입력과 BOM0의 6대조가 모두 정확한 원문 마스킹을 얻었다. 양 OS에서 각 18파일의 plain/base 두 CLI 실행 모두 P8 18건·fail_count18·exit1이며 누락이 없다. 이전 잘못된 `window.confir` 결과가 `window.confirm` 보존으로 바뀌었다.
- **A-P1-35/A-P2-36/A-P1-37: FIXED 유지.** ESM·비교식은 누적 66입력·498변형과 집중 시험에서 회귀가 없었다. Airport evidence·CSS·baseline·대비 도구는 이번 delta에서 불변이므로 직전 직접 검증의 10미달·예외4·신규6·exit1 및 정확한 정정 기록을 재사용한다.
- 이전 URL·wildcard·주석·인용 원 반례의 FIXED 판정은 현재 누적 시험으로 유지한다. 과거의 비표준 MDX 가정을 되살리거나 새 문법 요구를 추가하지 않았다. 새 P0/P1/P2/P3 finding은 없다.

## 직접 검증

| 실행 | 결과 |
|---|---|
| `npm ci --ignore-scripts` | 성공, 113개 설치. Windows Node v25.9.0/npm11.12.1에서 engine 경고가 있었으므로 지원 Node22 실행과 구분한다 |
| Windows Python3.14.3 `python -B -X utf8 -m unittest tests.test_ux_mdx_context -v` | 8개 성공·skip0·14.933초 |
| WSL Node22.22.2/Python3.11.15 `uv run --no-project --python 3.11 python -B -X utf8 -m unittest tests.test_ux_mdx_context -v` | 8개 성공·skip0·32.637초. 로그인 bash에서 실행 |
| `node tests/verify_mdx_reference.mjs node_modules/@mdx-js/mdx/index.js` | 498 PASS·실패/제외0·exit0. 제품과 같은 파서로 기대값을 대조한 결과이며 독립 파서 일치로 주장하지 않는다 |
| 기존 자기 Unicode helper, 양 OS | 각각 원문120개 정확한 마스킹120개, 불일치0. 120파일 batch CLI의135 finding은 파일·행·열·패턴이 전부 일치하고 summary 생성 |
| 자기 BOM helper, 양 OS | 각각 원 입력18개 정확한 마스킹18개, plain/base 두 CLI에서 파일별 P8 총18건·exit1. 총36개 파일 관찰, traceback 없음 |
| link / plan / SPDX | 508문서·2542대상 오류0 / 106 task 오류0 / 59파일 오류0 |
| secret / redaction / diff | 각644파일 finding0 / `git diff --check 31e3f0a 49d3867` 오류0 |

기존 독립 Unicode helper는 BMP·astral emoji·결합문자·ZWJ·FEFF, inline/fence/comment/속성/ESM/template/줄 주석과 LF/CRLF/CR를 포함한다. 직전 111/120 정확 일치·BOM 9개 불일치가 현재 120/120 일치로 바뀌었다. 집중 시험에는 새 정확한 마스킹54경우와 BOM18파일 외에 기존 delimiter120변형·누적 문맥·Git 추가행·실패 처리 대조가 포함된다.

자기 재현 자료는 주 checkout `.git/codex-audit/t103-parser-a-unicode.py`, `t103-parser-post-a-bom-batch.py`, `t103-parser-post-a-{win,wsl}-tests.log`다. Windows는 `python -B -X utf8 <helper.py> F:/dev/kor-travel-common-wt/review-t103-parser-post-a`, WSL은 로그인 bash에서 `uv run --no-project --python 3.11 python -B -X utf8 <동일 helper의 /mnt/f 경로> /mnt/f/dev/kor-travel-common-wt/review-t103-parser-post-a`로 실행했다. CLI 반복의 Node 로딩 비용을 줄이기 위해 같은 원 입력을 한 번에 전달했으며 검증 대상을 줄이지 않았다.

## 재사용·CI·미실행

- 작성자의 현재 코드 Windows 전체322개 성공·skip0·190.810초는 `.git/codex-audit/t103-bom-win-full.log`의 완료 결과와 coordinator의 후보 동일성 통보로 확인했다. 자기 전체 실행으로 세지 않는다.
- [CI 34218404453](https://github.com/digitie/kor-travel-common/actions/runs/34218404453)의 HEAD `ef91306f3c29ec0bd753df4229428b6eb90965c4`, completed/success 및 6 job success를 직접 조회했다. 제품 후보와 이 HEAD 사이의 차이는 이전 A/B raw와 이번 manifest뿐임을 파일 목록으로 확인했다. 상대 raw 본문은 읽지 않았다. 제품 SHA 자체의 별도 CI가 성공했다고 표기하지 않는다.
- `NOT_RUN`: 자기 전체322시험, 로컬 Windows Node22·Python3.11, 소비자 build/e2e·버전 검사, 실제 MDX compile/render/browser, npm/PyPI 게시, CI 개별 job 로그 전수 감사. 변경 없는 실행은 기존 evidence/CI 재사용으로 구분했다. 이번 양 OS 집중·직접 검증에는 중단이나 skip이 없다.
- 최종 **PASS**는 이 불변 후보와 명시한 검토 범위에 대한 판정이다. 사용자 요청대로 현재 PR의 통합·merge gate는 coordinator가 마무리하고 다음 task 없이 대기한다. 원본 보고서만 커밋하며 SHA256·commit SHA·커밋 후 clean 상태는 완료 메시지로 전달한다.
