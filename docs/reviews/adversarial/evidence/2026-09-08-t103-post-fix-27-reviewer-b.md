<!-- SPDX-License-Identifier: GPL-3.0-or-later -->
# T-103 post-fix-27 독립 적대적 리뷰 B 원본

## 실행 기준선과 독립성

- 실행 ID: `T103-PF27-B-20260908-155210`.
- 시작 KST `2026-09-08T15:52:10.8880932+09:00`; 검증 종료 SHA/clean 관찰 KST `2026-09-08T16:00:04.2582762+09:00`.
- 시작·종료 제품 HEAD: `009ec5dcf70e55b6c736ccaeabbfeb71a08836f6`; tree: `f521d07dd7566744659522186a4add8f01d7150b`.
- 격리 worktree: `F:/dev/kor-travel-common-wt/review-t103-post27-b`, detached. 시작·검증 종료 `git status --porcelain` 출력 없음. 이후 이 원본 한 파일만 별도 branch에 커밋한다.
- delta base: `2a32dc7e07a4c36e2b0e92402f05019b31f6c3cb`.
- manifest: `64505d7`의 [post-fix-27 manifest](2026-09-08-t103-post-fix-27-manifest.md)를 `git show`로 읽었다. Git blob SHA256: `16f253aff42a13a6b162d072b09704b16ab248efd6104fd4ac55b424b42cbbc8`.
- source `.git/config` 시작·종료 SHA256: `0a0f849e7874cf0a25926856f9d2e381ccbf4c2dcb5999869c57b86e0f5beb5b`. 후보·manifest·공유 branch·소비자·기존 evidence·Git 설정을 수정하지 않았다. 상대 reviewer의 post27 결과/raw 및 과거 상대 raw 본문을 읽거나 요청하지 않았다.

## 전달받은 요청 원문

> post-fix-27 독립 적대적 리뷰를 시작해 주세요. 코드 후보 `009ec5dcf70e55b6c736ccaeabbfeb71a08836f6`, tree `f521d07dd7566744659522186a4add8f01d7150b`, manifest `64505d7`의 `docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-27-manifest.md`입니다. 전문 범위는 위 경계의 독립 CommonMark 대조와 Git added-line/base, 오류/redaction, plain/blockquote·nested·`--base` 교차입니다. 이전 post-27 A 결과/raw를 읽지 말고 독립 검증하세요. 후보/manifest/공유 branch/소비자/기존 evidence는 수정하지 말고, 자신의 worktree에 `docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-27-reviewer-b.md`만 작성해 report-only commit을 만드세요. PASS/NO-GO와 commit SHA/SHA-256을 회신하세요.

> post-fix-27 리뷰를 지금 실행하고 원본 report-only commit까지 완료해 주세요. 동일 immutable code candidate에서 독립적으로 검증하세요.

## 검토 범위와 실행 결과

`git diff 2a32dc7 009ec5d -- tools/ux_lint.py tests/test_ux_lint.py` 전체를 읽었다. 제품 delta는 marker 선택 공백·절대 tab-stop 계산과 새 시험 2개/기존 시험 기대 수정이다. 나머지 3개 파일은 직전 manifest·A/B 원본이며 상대 원본은 경로만 확인했다. [T-103](../../../tasks/T-103-kt-contrast-ux-lint.md)의 인용 제외·추가 행 fail·P6/P8 계약과 [resume](../../../resume.md)의 IN_PROGRESS, airport 1.320934·geo 8건 예제, T-010 후행을 대조했다. CI·versions·패키지 공개 파일은 delta에서 불변이며 GPL-3.0-or-later·common 전용 도구·외부 의존 0·소비자 무수정·npm/PyPI 미게시 경계가 유지된다.

아래 `ROOT`는 위 worktree, `AUDIT`는 source checkout `.git/codex-audit`다. 모든 helper·fixture·로그는 후보 밖에 두었다. `WIN`은 `py -3.14 -B -X utf8`, `WSL`은 `/home/digitie/.local/share/uv/python/cpython-3.11-linux-x86_64-gnu/bin/python3.11 -B -X utf8`이며 WSL 경로는 `/mnt/f/`로 변환했다. 임시 fixture의 Git 환경변수는 제거했다.

| 명령·검사 | Windows Python 3.14.3 | WSL Python 3.11.15 |
|---|---|---|
| `-m unittest discover -s tests` | 300 실행 성공, skip 0, 159.663초 | `AUDIT/review-t102-b-wsl-unittest.py ROOT` 임시 독립 Git 사본에서 300 수집·297 실행 성공·3 skip, 33.005초 |
| `-m unittest tests.test_kt_contrast tests.test_ux_lint` | 62 성공, skip 0, 56.760초 | 62 성공, skip 0, 21.057초 |
| `AUDIT/review-t102-post-b-gates.py ROOT` | plan 106/오류 0, links 472문서·2458대상/오류 0, SPDX 56/오류 0 | 동일 |
| 위 helper의 secrets·redaction | 각각 604파일·발견 0·예외 0 | 동일 |
| 위 helper의 registry·aliases | `check_versions.py --self-check` exit 0; aliases CSS 1/오류 0 | 동일; 소비자 버전 검사는 미실행 |
| 위 helper의 aliases focused | 35 성공, skip 0 | 35 수집·34 성공·1 skip |
| `AUDIT/t103-post27-b-run-corpus.py ROOT win` 또는 `ROOT wsl` | 누적 1263개 관찰, 기대 지정 불일치 0 | 동일 |
| `AUDIT/t103-post26-b-new.py ROOT OUTPUT_JSON` | B-P1-22 원 반례 72개, 기대 불일치 0 | 동일 |
| `AUDIT/t103-post27-b-new.py ROOT OUTPUT_JSON` | 새 CLI 144개: 36개 누락, 108개 대조 일치 | 동일 |
| `git diff --check 2a32dc7 009ec5d` | 출력 없음, exit 0 | 별도 WSL Git 검사는 미실행 |

WSL skip 3개는 Windows 8.3 전용 1개와 선택적 jsonschema 미설치 2개다. manifest의 coordinator 환경과 다르므로 skip을 성공 실행으로 세지 않았다. WSL full/static helper는 `.git`·`__pycache__`·`node_modules`를 제외한 임시 사본에 독립 Git을 만들었으며 source `core.worktree`를 변경하지 않았다.

누적 1263개는 기존 543개(105·140·104·37·34·18·29·28·48), opener 함수/CLI 564개, quoted fence 12개, 깊이/들여쓰기 144개다. 564개 안의 기대 미지정 탐색 CLI 12개는 합격으로 세지 않았다. wrapper는 `expected_exit=null`을 불일치로 출력하므로 이를 제외한 기대 지정 사례를 별도로 대조했다. B-P1-22 원 반례까지 합쳐 1335개 관찰이며 unittest 수가 아니다. 두 OS 결과는 Unicode DB 메타데이터(16.0.0/14.0.0)만 다르고 모든 실제 판정은 같다. 새 CLI 144개 JSON은 전체 동일하다.

canonical 27쌍 exit 0, UX fixture 의도된 finding 12개/fail_count 0, 4앱 baseline exit 0·airport 1.320934를 corpus에서 재현했다. CSS comment/selector/media/specificity·deep/huge JSON·argparse·diff `+++`/가짜 hunk·CR/CRLF/LS/PS·self-symlink·JSON/Markdown/step summary redaction도 재실행했다. 합성 경로 marker 노출·traceback은 없었고 입력 오류 exit 2가 유지됐다. Windows 임시 Git의 LF→CRLF 경고는 제품 실패로 세지 않았으며 fixture bytes는 직접 보존했다.

독립 비교로 설치되어 있던 `markdown-it-py 4.2.0`의 `MarkdownIt("commonmark")`를 사용해 `AUDIT/t103-post27-b-oracle.py ROOT OUTPUT_JSON`을 Windows에서 실행했다. prefix/탭/깊이/marker 1024개 탐색 중 220개가 검사기의 masking과 달랐다. 이를 220개 제품 결함으로 세지 않았다. 그중 84개는 과도한 들여쓰기의 backtick이 inline fallback으로 연결되는 종류이고, 나머지 136개는 중간 marker/세 겹 탭 해석에서 구현 간 차이가 있어 공식 문법으로 최종 판정을 내리지 않았다. 탐색 일치도도 PASS gate로 세지 않는다. 아래 finding은 별도 최소 입력·공식 block 우선순위·양 OS CLI로 확정했다. WSL 비교 parser·실제 MDX compiler는 실행하지 않았다.

`gh run list --commit 009ec5dcf70e55b6c736ccaeabbfeb71a08836f6 --json databaseId,event,status,conclusion,headSha,url`와 `gh run view 34196371150 --json headSha,status,conclusion,jobs`로 [정확한 후보의 PR CI](https://github.com/digitie/kor-travel-common/actions/runs/34196371150)를 독립 조회했다. 해당 SHA·completed/success와 6개 job 성공을 확인했다. job 원문 로그 전체·실제 소비자 실행을 확인한 것으로 확대하지 않는다.

## 누적 disposition과 새 finding

원 ID의 아래 반례를 현재 후보에서 다시 실행했다. 원 심각도는 ID 그대로 유지한다.

| 원 ID | 현재 disposition |
|---|---|
| B-P1-01, B-P1-02 | root/CWD Git·prepend baseline 증가: FIXED |
| B-P1-03, B-P1-04 | 기존 MDX 표현식·Unicode·주석 corpus 및 오류/redaction: FIXED |
| B-P2-05, B-P2-06, B-P3-07 | 읽기 쌍·baseline JSON·geo 문서: FIXED |
| B-P1-08, B-P1-09, B-P2-10 | `+++`·CSS cascade/media·airport 수치: FIXED |
| B-P1-11, B-P1-12, B-P2-13 | selector 대소문자/공백·빈 목록/root descendant·inline span 원 반례: FIXED |
| B-P1-14, B-P1-15, B-P1-16 | JS LS/PS·Git 가짜 hunk·bare CR 읽기/좌표: FIXED |
| B-P2-17, B-P2-18, B-P2-19 | LS/PS 문단·closing suffix·plain 4열/tab-stop: FIXED |
| B-P2-20, B-P1-21 | quoted fence·직접 depth 감소/빈 행: FIXED |
| B-P1-22 | marker 선택 공백·정상 3열·중간 prefix의 지정된 원 반례 72개: FIXED |
| **B-P1-23** | **새 발견, OPEN / FIX_REQUIRED**: inline span이 뒤의 독립 fence block을 넘어 연결됨 |

### B-P1-23 — 새 fence opener를 inline span의 닫힘으로 소비해 실행 P6/P8을 누락

- 심각도: **P1**. 신규 변경의 필수 실패 gate가 실제 실행 패턴을 숨기므로 NO-GO다.
- 위치: `tools/ux_lint.py:144-148`의 문단 끝 계산, `:433-450`의 inline 닫힘 검색, `:759-774`의 무효 fence 이후 inline fallback.
- LF 최소 입력의 Python 문자열: `'```bad`info\n{window.confirm("x")}\n```\n'`. UTF-8 SHA256: `1ed1313533c0c620dea8bc9d521b41492fb3735ac157d13eed794103e6549eb3`.
- 첫째 행은 info string에 backtick이 있어 fence opener가 아니다. 셋째 행은 유효한 새 fence opener이며 앞 문단을 종료한다. 둘째 행은 그 fence의 내용이나 유효한 inline code가 아니므로 P8을 report하고 `--fail-new`에서 exit 1이어야 한다.
- 재현: 임시 Git root의 `Page.mdx`에 `safe\n`을 커밋하고 `BASE`를 기록한 다음 위 입력 bytes로 바꾼다. `PYTHON ROOT/tools/ux_lint.py --root TEMP --fail-new --json` 및 같은 명령에 `--base BASE`를 더해 실행한다. **실제: exit 0, findings=[]**, stderr traceback 없음. 두 OS 동일하다.
- P6 변형은 둘째 행을 `<div className="outline-none"/>`로 바꾼다. SHA256: `2e736f451e100159cda67f3c387c35fd3703a4409a47b254d1e2c363077ef941`. 동일한 누락이다.
- plain/`> `/`>> ` × LF/CR/CRLF × P6/P8 × 전체/`--base` = **36개/OS**가 기대 exit 1 대신 exit 0이다. 동일 행의 정상 닫힌 triple span, 정상 fence info, 마지막 fence 없는 입력의 **108개/OS** 대조는 기대와 일치했다.
- 독립 AST 관찰: 위 LF 입력의 `MarkdownIt("commonmark").parse(text)`는 `[0,2]` 문단과 `[2,3]` 별도 fence를 생성한다. 문단 inline의 내용에 둘째 행 표현식이 남는다. 이는 [CommonMark 0.31.2 §3.1](https://spec.commonmark.org/0.31.2/#precedence)의 block 우선순위와 [§4.5](https://spec.commonmark.org/0.31.2/#fenced-code-blocks)의 backtick info 금지·문단을 끊는 fence 규칙과 일치한다(revision 2024-01-28, 조회 2026-09-08).
- 원인: `_mask_mdx_fence`는 첫 fence를 올바르게 거절하지만 이어지는 `_find_inline_span_end`는 빈 문단 경계까지만 검색한다. 새 block 시작인지 확인하지 않고 다음 triple run을 닫힘으로 인정하여 중간 실행 코드를 모두 가린다. 이번 marker 공백 계산 변경 자체가 새로 만든 회귀라고 단정하지 않는다. 이 fallback 경로는 이전 base에도 존재하며 이번 full 검토에서 추가로 확정된 결함이다.
- 최소 권고: inline 닫힘 후보를 같은 실제 Markdown block 안으로 제한하고, 새 유효 fence/blockquote 경계를 만나면 그것을 inline 닫힘으로 소비하지 않는다. 그때 미종결 span 뒤 실행 식/JSX 검사를 계속해야 한다. 정상 동일 행·동일 문단 code span 대조와 plain/quoted/nested·CR/LF·`--base` 반례를 함께 고정한다. stdlib 제약을 유지하며 제3자 parser를 제품 의존성으로 추가하라는 권고가 아니다.

## NOT_RUN과 최종 verdict

- `NOT_RUN(Windows Python 3.11)`: 실행 파일 부재. Windows 3.14와 WSL 3.11 성공을 대체 실행으로 표시하지 않는다.
- `NOT_RUN(WSL Git diff --check 별도 실행, WSL 비교 parser, 실제 MDX compiler/browser, CI job 로그 전체, 비 UTF-8 Git 출력 직접 주입)`.
- `NOT_RUN(실제 소비자 build/type/e2e·manifest 검사, npm/PyPI 설치·게시, workflow dispatch)`: 요청된 common 독립 리뷰 범위 밖.
- 탐색 parser 간 미확정 차이는 위에 별도로 기록했고 기존 finding closure·신규 finding 수에 합치지 않았다.
- 기존 22개 ID의 지정된 원 반례 FIXED. 새 확정 finding **B-P1-23 1개 OPEN**, P0/P2/P3 확정 신규 0개.
- **verdict: NO-GO.** 후보·manifest를 수정하지 않고 이 원본 한 파일만 report-only commit으로 확정한다. 수정 후보의 두 독립 reviewer 재검토가 필요하다.
