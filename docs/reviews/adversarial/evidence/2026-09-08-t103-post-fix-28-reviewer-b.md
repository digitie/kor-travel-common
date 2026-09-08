<!-- SPDX-License-Identifier: GPL-3.0-or-later -->
# T-103 post-fix-28 독립 적대적 리뷰 B 원본

## 실행 기준선

- 실행 ID: `T103-PF28-B-20260908-161100`.
- 시작 KST: `2026-09-08T16:11:00.5787489+09:00`; 검증 종료 KST: `2026-09-08T16:16:38.8685162+09:00`.
- 시작·종료 제품 HEAD: `71a6f99de297e809c165f005d4d6b1753468d157`; tree: `b0ba565c1fe6d6002c7a983307853f2bb1999c39`.
- 격리: `F:/dev/kor-travel-common-wt/review-t103-post28-b`, detached checkout. 시작·검증 종료 `git status --porcelain` 출력 없음. 이후 이 원본 한 파일만 별도 branch에 커밋한다.
- delta base: `009ec5dcf70e55b6c736ccaeabbfeb71a08836f6`.
- manifest: `f661de2`의 [post-fix-28 manifest](2026-09-08-t103-post-fix-28-manifest.md)를 `git show`로 읽었다. Git blob SHA256: `4a6bf9cbe607d6f9afa0cdeb25cc9deddd506142d9d0680cbcf5c8f4b65ae153`.
- source `.git/config` 시작·종료 SHA256: `0a0f849e7874cf0a25926856f9d2e381ccbf4c2dcb5999869c57b86e0f5beb5b`. source 설정·후보·manifest·공유 branch·소비자·기존 evidence를 변경하지 않았다. 상대 reviewer의 post28 결과/raw 및 과거 상대 raw 본문을 읽거나 요청하지 않았다.

## 전달받은 요청 원문

> post-fix-28 독립 적대적 리뷰를 시작해 주세요. 코드 후보 `71a6f99de297e809c165f005d4d6b1753468d157`, tree `b0ba565c1fe6d6002c7a983307853f2bb1999c39`, manifest `f661de2`의 `docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-28-manifest.md`입니다. 전문 범위는 위 경계의 독립 parser 대조와 Git added-line/base, plain/blockquote/nested·오류/redaction·누락 방지입니다. 이전 post-28 A 결과/raw를 읽지 말고 독립 검증하세요. 후보/manifest/공유 branch/소비자/기존 evidence는 수정하지 말고 자신의 worktree에 `docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-28-reviewer-b.md`만 작성해 report-only commit을 만드세요. PASS/NO-GO와 commit SHA/SHA-256을 회신하세요.

> post-fix-28 리뷰를 지금 실행하고 원본 report-only commit까지 완료해 주세요.

## 범위·코드·정본 대조

`git diff 009ec5d 71a6f99 -- tools/ux_lint.py tests/test_ux_lint.py` 전체를 읽었다. 제품 delta는 무효 backtick info 줄의 backtick만 가린 뒤 줄 끝에서 재개하는 처리 10행과 시험 1개다. 나머지 3개 파일은 직전 manifest·A/B raw 추가이며 상대 원본은 경로만 확인했다. [문서 지도](../../../README.md), [resume](../../../resume.md), [T-103](../../../tasks/T-103-kt-contrast-ux-lint.md)의 IN_PROGRESS·인용 제외·P6/P8·추가 행 fail·T-010 후행을 대조했다. airport 1.320934·geo 8건 예제 계약, GPL-3.0-or-later·common 도구·외부 의존 0·소비자 무수정·npm/PyPI 미게시 경계가 유지된다. CI·versions·공개 패키지 파일은 delta에서 불변이다.

## 실제 실행과 한계

`ROOT`는 위 worktree, `AUDIT`는 source checkout `.git/codex-audit`다. Windows 명령 앞부분은 `py -3.14 -B -X utf8`, WSL은 `/home/digitie/.local/share/uv/python/cpython-3.11-linux-x86_64-gnu/bin/python3.11 -B -X utf8`이다. WSL 경로는 `/mnt/f/`로 바꿨다. helper·fixture·로그는 후보 밖에 두고 임시 fixture의 `GIT_*` 환경을 제거했다.

| 명령·검증 | Windows Python 3.14.3 | WSL Python 3.11.15 |
|---|---|---|
| `-m unittest discover -s tests` | 301 성공, skip 0, 163.888초 | `AUDIT/review-t102-b-wsl-unittest.py ROOT` 임시 독립 Git 사본: 301 수집·298 실행 성공·3 skip, 29.532초 |
| `-m unittest tests.test_kt_contrast tests.test_ux_lint` | 63 성공, skip 0, 45.877초 | 63 성공, skip 0, 19.441초 |
| `AUDIT/review-t102-post-b-gates.py ROOT` | plan 106/오류 0, links 475문서·2464대상/오류 0, SPDX 56/오류 0 | 동일 |
| 위 helper의 secrets·redaction | 각각 607파일·발견 0·예외 0 | 동일 |
| 위 helper의 registry·aliases | registry 자체 검사 exit 0, aliases CSS 1/오류 0 | 동일; 소비자 버전 검사는 미실행 |
| 위 helper의 aliases focused | 35 성공, skip 0 | 35 수집·34 성공·1 skip |
| `AUDIT/t103-post28-b-run-corpus.py ROOT win` 또는 `ROOT wsl` | 누적 1263개 관찰, 기대 지정 exit 불일치 0 | 동일 |
| `AUDIT/t103-post26-b-new.py ROOT OUTPUT_JSON` | B-P1-22 지정 원 반례·대조 72개 일치 | 동일 |
| `AUDIT/t103-post27-b-new.py ROOT OUTPUT_JSON` | 144개 중 원 누락 36개 FIXED, 정상 inline 대조 36개 회귀, 나머지 72개 일치 | 동일 |
| `AUDIT/t103-post28-b-new.py ROOT OUTPUT_JSON` | 216개: P1 누락 72개·P2 오검출 36개·대조 일치 108개 | 동일 |
| `AUDIT/t103-post28-b-base.py BASE_ROOT ROOT OUTPUT_JSON` | 2입력 × base/candidate = 4개 관찰; 아래 원인 경계 확인 | 동일 |
| `git diff --check 009ec5d 71a6f99` | 출력 없음, exit 0 | 별도 WSL Git 실행 미실행 |

WSL skip 3개는 Windows 8.3 전용 1개·선택적 jsonschema 미설치 2개다. manifest의 coordinator 환경과 달라 그 실행 수를 재사용하지 않았다. WSL full/static helper는 `.git`·`__pycache__`·`node_modules`를 제외해 임시 사본을 만들고 독립 Git을 초기화한다. source `core.worktree`는 변경하지 않았다. 최초 WSL corpus 호출에서 OS 라벨 대신 경로를 전달해 helper 로그 저장이 실패한 실행은 폐기했다. 올바른 `wsl` 인자로 다시 실행한 결과만 집계했으며 이 helper 오류를 제품 traceback으로 세지 않는다.

누적 1263개는 543개 기존 관찰(105·140·104·37·34·18·29·28·48), opener 함수/CLI 564개, quoted 12개, 깊이/들여쓰기 144개다. 564개 중 `expected_exit=null`인 탐색 12개는 PASS/FAIL로 세지 않았다. exit 기대 필드가 없는 관찰도 자동 합격 건수로 더하지 않았다. 원 반례 72개·144개, 새 216개, base 대조 4개까지 총 1699개 관찰/OS이며 unittest 수가 아니다. Win/WSL JSON은 Unicode DB 메타데이터(16.0.0/14.0.0)만 다르고 실제 판정은 같다.

canonical 27쌍 exit 0, UX fixture 의도된 finding 12개/fail_count 0, 4앱 baseline exit 0·airport 1.320934를 재현했다. CSS selector/media/specificity/comment·JSON 숫자/huge/deep·argparse·Git `+++`/가짜 hunk/added 행·CR/CRLF/LS/PS·self-symlink·오류/redaction corpus를 다시 실행했다. 합성 경로 marker 노출·제품 traceback 없음과 일반 입력 오류 exit 2가 유지됐다. 실제 CR/CRLF fixture는 bytes로 보존했고 Windows 임시 Git LF→CRLF 경고는 별도로 구분했다.

설치되어 있던 `markdown-it-py 4.2.0`의 `MarkdownIt("commonmark").parse(text)`로 아래 두 최소 입력을 Windows에서 독립 대조했다. 첫 입력은 문단 `[0,2]`와 별도 fence `[2,3]`, 둘째 입력은 하나의 `code_inline`으로 파싱됐다. 이 비교는 외부 parser를 제품에 추가하거나 registry를 호출하지 않았다. 공식 CommonMark 0.31.2의 block 우선순위·fence info 제한·code span 정의와 함께 판단했으며 실제 MDX compiler/browser 실행으로 표시하지 않는다. 이전 탐색 parser 간 미확정 차이 전체를 이번에 재판정한 것은 아니다.

`gh run list --commit 71a6f99de297e809c165f005d4d6b1753468d157 --json databaseId,event,status,conclusion,headSha,url`와 `gh run view 34197631092 --json headSha,status,conclusion,jobs`로 [정확한 후보 PR CI](https://github.com/digitie/kor-travel-common/actions/runs/34197631092)의 SHA·completed/success·6개 job 성공 및 각 source SHA 비교 step 성공을 직접 확인했다. 로그 전체와 소비자 실행은 확인하지 않았다.

## Finding 1: B-P1-23 — 설명 문구 뒤의 inline span은 여전히 다음 fence block을 넘어 연결됨

- 원 심각도 **P1** 유지. disposition **OPEN(부분 수정) / FIX_REQUIRED**.
- 위치: `tools/ux_lint.py:144-148`, `:433-450`, `:767-782`; 이번 특수 처리는 `:625-635`에서 fence prefix로 인정한 줄에만 적용된다.
- LF 최소 입력은 다음 Python 문자열이다: `"Example " + "`"*3 + "literal\n{window.confirm(\"x\")}\n" + "`"*3 + "\n"`. SHA256: `cf380531ead499a71602bc32fff9b0ec5d0343ccf864217a0ead35c9c831c6e7`.
- 임시 Git root의 `Page.mdx`에 `safe\n`을 먼저 커밋하고 `BASE`를 기록한 뒤 위 bytes로 변경한다. `PYTHON ROOT/tools/ux_lint.py --root TEMP --fail-new --json` 및 `--base BASE` 추가 명령으로 재현한다.
- 기대: 첫째 행 triple run은 문단 안의 미종결 inline delimiter이며, 셋째 행의 새 fence는 그 문단을 끝낸다. 둘째 행 P8은 인용 밖의 실행식이므로 finding·exit 1이어야 한다. **실제: exit 0, findings=[]**. 두 OS 동일하다.
- `Example ` 뒤를 `bad`와 backtick 하나가 포함된 info로 바꾼 변형도 누락된다. plain/`> `/`>> ` × LF/CR/CRLF × P6/P8 × 전체/`--base` × 설명 변형 2개 = **72개/OS** 누락이다.
- base/current CLI 직접 대조는 둘 다 exit 0이다. 즉 원인 경로가 남아 있다. 이전 최소 입력처럼 줄이 triple run으로 바로 시작하는 36개는 이제 exit 1이지만, 문단 범위를 넘어 delimiter를 연결하는 일반 원인은 수정되지 않았다.
- 영향: 정상적인 신규 소스가 필수 UX gate를 잘못 통과한다.
- 최소 권고: 특정 무효 fence 줄만 분기하지 말고, inline 닫힘을 같은 Markdown block 안으로 제한한다. 다음 유효 fence를 닫힘으로 소비하지 않고 미종결 span 뒤 실행식/JSX를 계속 검사해야 한다. [CommonMark §3.1](https://spec.commonmark.org/0.31.2/#precedence)·[§4.5](https://spec.commonmark.org/0.31.2/#fenced-code-blocks)의 block 우선순위를 plain/quoted/nested에 일관되게 적용한다.

## Finding 2: B-P2-13 — 정상 닫힌 triple inline 인용이 실행 패턴으로 다시 오검출됨

- 원 심각도 **P2** 유지. disposition **REOPENED / FIX_REQUIRED**. 파일 첫·3자 inline 인용 계약의 회귀이므로 새 ID를 만들지 않는다.
- 위치: `tools/ux_lint.py:625-635`의 무효 info 분기가 같은 행에서 정상 종료된 code span까지 backtick만 지운 뒤 본문을 노출한다.
- LF 최소 입력: `"`"*3 + "{window.confirm(\"x\")}" + "`"*3 + "\n"`. SHA256: `dba156b7f5f03e62c4244d492b33e409be429ab5b0d28f979b1bfd4a6e57004a`.
- 같은 임시 Git fixture·위 두 CLI 모드로 실행한다. 기대는 정상 `code_inline` 인용 제외·exit 0. **실제: P8, line 1, added true, exempt false, fail true, exit 1**. P6 대조도 오검출한다.
- plain/quoted/nested × LF/CR/CRLF × P6/P8 × 전체/`--base` = **36개/OS** 오검출이다. 별도의 이전 `bad`/backtick 포함 same-line 대조 36개도 같은 원인으로 실패한다. 반면 `Example ` 뒤의 정상 닫힌 triple span 36개는 계속 제외된다.
- base/current CLI 직접 대조: base exit 0/findings=[] → candidate exit 1/P8. 이전 base와 그 raw-only commit 사이 도구 diff가 없음을 확인한 post27 worktree의 코드만 사용했다.
- 영향: 정상 문서 코드 예제가 신규 UX 위반으로 차단되어 인용 제외 공개 계약을 깨뜨린다. 실행 누락이 아닌 오검출이므로 P2로 분리한다.
- 최소 권고: backtick이 info에 있다는 이유만으로 해당 줄 전체의 inline 해석을 금지하지 않는다. 같은 block에서 정상 닫힌 span은 계속 제외하면서 B-P1-23의 다음 block 연결만 차단한다. [CommonMark §6.1](https://spec.commonmark.org/0.31.2/#code-spans)의 같은 길이 delimiter 계약과 기존 양성/음성 대조를 함께 보존한다.

## 누적 disposition·NOT_RUN·최종 판정

| 원 ID | 현재 판정 |
|---|---|
| B-P1-01, B-P1-02, B-P1-03, B-P1-04 | root/Git·baseline 증가·기존 MDX 실행식·오류/redaction 지정 원 반례 FIXED |
| B-P2-05, B-P2-06, B-P3-07 | 읽기 쌍·baseline JSON·geo 문서 FIXED |
| B-P1-08, B-P1-09, B-P2-10, B-P1-11, B-P1-12 | diff·CSS·airport·selector 지정 원 반례 FIXED |
| **B-P2-13** | **REOPENED**, 위 정상 inline 회귀 |
| B-P1-14, B-P1-15, B-P1-16, B-P2-17, B-P2-18, B-P2-19 | Unicode 줄 종결자·Git mapping·fence suffix/열 지정 원 반례 FIXED |
| B-P2-20, B-P1-21, B-P1-22 | quoted fence·depth·marker 선택 공백 지정 원 반례 FIXED |
| **B-P1-23** | **OPEN(부분 수정)**, 위 설명 문구 변형 누락 |

- `NOT_RUN(Windows Python 3.11)`: 실행 파일 부재. 다른 환경을 대체 실행으로 표시하지 않는다.
- `NOT_RUN(WSL Git diff --check 별도 실행, WSL 비교 parser, 이전 parser 탐색 불일치 전체 재판정, 실제 MDX compiler/browser, CI 로그 전체, 비 UTF-8 Git 출력 직접 주입)`.
- `NOT_RUN(소비자 build/type/e2e·manifest 검사, npm/PyPI 설치·게시, workflow dispatch)`: common 독립 리뷰 밖이며 호출하지 않았다.
- 23개 누적 ID 중 21개 지정 원 반례 FIXED, P1 1개 OPEN·P2 1개 REOPENED. 새 ID·P0/P3 발견 0개다. 반복 입력 수를 독립 finding 수로 세지 않는다.
- **verdict: NO-GO.** 후보·manifest는 수정하지 않고 이 원본 한 파일만 report-only commit으로 확정한다.
