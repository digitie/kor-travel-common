<!-- SPDX-License-Identifier: GPL-3.0-or-later -->
# T-103 post-fix-29 독립 적대적 리뷰 B 원본

## 실행 기준선과 요청

- 실행 ID: `T103-PF29-B-20260908-162847`.
- 시작 KST: `2026-09-08T16:28:47.6010354+09:00`; 모든 실행 결과 수집 완료 KST: `2026-09-08T16:34:15.1559318+09:00`.
- 시작·종료 제품 HEAD: `9afea549dd81cb23d3297f83d89df4b519734382`; tree: `03cb65ba437848f279f542452705c235f19daaa8`.
- 격리 worktree: `F:/dev/kor-travel-common-wt/review-t103-post29-b`, detached. 시작·검증 종료 재확인한 `git status --porcelain` 출력 없음. 이후 이 원본 한 파일만 별도 branch에 커밋한다.
- delta base: `71a6f99de297e809c165f005d4d6b1753468d157`.
- manifest: `a100194`의 [post-fix-29 manifest](2026-09-08-t103-post-fix-29-manifest.md)를 `git show`로 읽었다. Git blob SHA256: `59661643a1f00c70ac7e2cf5b1032be62e44230be5c090a6accea8d52f7dba79`.
- source `.git/config` 시작·종료 SHA256: `0a0f849e7874cf0a25926856f9d2e381ccbf4c2dcb5999869c57b86e0f5beb5b`. 후보·manifest·공유 branch·소비자·기존 evidence·Git 설정을 변경하지 않았다. 상대 reviewer 결과/raw 및 과거 상대 raw 본문을 읽거나 요청하지 않았다.

전달받은 요청 원문:

> post-29 독립 적대 리뷰를 시작해 주세요. immutable code candidate는 commit 9afea549dd81cb23d3297f83d89df4b519734382, tree 03cb65ba437848f279f542452705c235f19daaa8 입니다. manifest는 docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-29-manifest.md (manifest commit a100194)입니다. 별도 detached clean worktree에서 candidate SHA/tree를 checkout하고, 다른 reviewer 결과·raw를 열람하지 마세요. B 범위는 독립 Markdown/CommonMark parser 대조와 Git added-line/base, 정상 inline false positive·block fence false negative, plain/blockquote/nested·입력 오류/redaction·양 OS입니다. 코드·manifest·소비자·기존 evidence는 수정하지 말고 자신의 단일 raw report만 커밋하세요. PASS/NO-GO와 finding ID/심각도/재현/영향/최소 수정/disposition, 시작·종료 SHA/tree·clean·명령/결과·SHA-256을 남겨 주세요. raw commit과 SHA-256을 회신하세요.

## 검토·실행 범위

`git diff 71a6f99 9afea54 -- tools/ux_lint.py tests/test_ux_lint.py` 전체를 읽었다. 제품 delta는 fence 시작 판별 helper, 무효 info의 정상 inline 복원, 시험 1개 추가다. 나머지 3개 파일은 직전 manifest·A/B raw이며 상대 원본은 경로만 확인했다. [문서 지도](../../../README.md)·[resume](../../../resume.md)·[T-103](../../../tasks/T-103-kt-contrast-ux-lint.md)의 IN_PROGRESS, 인용 제외·P6/P8·추가 행 fail·T-010 후행과 airport 1.320934·geo 8건 예제를 대조했다. GPL-3.0-or-later·common 도구·stdlib·소비자 무수정·npm/PyPI 미게시 경계는 유지된다. CI·versions·공개 패키지 파일은 delta에서 불변이다.

아래 `ROOT`는 위 worktree, `AUDIT`는 source `.git/codex-audit`다. Windows는 `py -3.14 -B -X utf8`, WSL은 `/home/digitie/.local/share/uv/python/cpython-3.11-linux-x86_64-gnu/bin/python3.11 -B -X utf8`을 사용했다. WSL 경로는 `/mnt/f/`로 변환했다. helper·로그·fixture는 후보 밖에 두고 fixture의 `GIT_*` 환경을 제거했다.

| 명령·검증 | Windows Python 3.14.3 | WSL Python 3.11.15 |
|---|---|---|
| `-m unittest discover -s tests` | 302 실행 성공·skip 0, 181.459초 | `AUDIT/review-t102-b-wsl-unittest.py ROOT` 임시 독립 Git 사본에서 302 수집·299 실행 성공·3 skip, 31.564초 |
| `-m unittest tests.test_kt_contrast tests.test_ux_lint` | **64** 성공·skip 0, 65.516초 | **64** 성공·skip 0, 25.565초 |
| `AUDIT/review-t102-post-b-gates.py ROOT` | plan 106/오류 0, links 478문서·2471대상/오류 0, SPDX 56/오류 0 | 동일 |
| 위 helper의 secrets·redaction | 각각 610파일·발견 0·예외 0 | 동일 |
| 위 helper의 registry·aliases | 자체 검사 exit 0, aliases CSS 1/오류 0 | 동일; 소비자 버전 검사 미실행 |
| 위 helper의 aliases focused | 35 성공·skip 0 | 35 수집·34 성공·1 skip |
| `AUDIT/t103-post29-b-run-corpus.py ROOT win` 또는 `ROOT wsl` | 기존 1263개 관찰, 기대 지정 exit 불일치 0 | 동일 |
| `AUDIT/t103-post26-b-new.py ROOT OUTPUT_JSON` | B-P1-22 원 반례·대조 72개 일치 | 동일 |
| `AUDIT/t103-post27-b-new.py ROOT OUTPUT_JSON` | 원 반례·same-line 대조 144개 일치 | 동일 |
| `AUDIT/t103-post28-b-new.py ROOT OUTPUT_JSON` | 216개 중 설명 문구 뒤 누락 72개, 나머지 144개 일치 | 동일 |
| `AUDIT/t103-post29-b-new.py ROOT OUTPUT_JSON` | 새 48개 중 경계 누락 24개·인용 오검출 12개·대조 일치 12개 | 동일 |
| `AUDIT/t103-post29-b-base.py BASE_ROOT ROOT OUTPUT_JSON` | 4입력 × base/current = 8개, 아래 원인 경계 확인 | 동일 |
| `git diff --check 71a6f99 9afea54` | 출력 없음, exit 0 | 별도 WSL Git 실행 미실행 |

WSL skip 3개는 Windows 8.3 전용 1개·선택적 jsonschema 미설치 2개다. manifest coordinator 결과의 skip 수를 재사용하지 않았다. WSL full/static helper는 `.git`·`__pycache__`·`node_modules`를 제외한 임시 사본을 만들고 독립 Git을 초기화한다. source `core.worktree`는 변경하지 않았다.

기존 1263개는 543개 관찰(105·140·104·37·34·18·29·28·48), opener 함수/CLI 564개, quoted 12개, 깊이/들여쓰기 144개다. `expected_exit=null` 탐색 12개와 기대 필드 없는 관찰을 자동 성공 건수로 세지 않는다. 전체 결과는 1751개 관찰/OS이며 unittest 수가 아니다. 두 OS JSON은 Unicode DB 메타데이터(16.0.0/14.0.0)만 다르고 실제 판정은 동일하다. Windows 마지막 결과 파일 생성 전에 읽은 일시적 집계 오류는 폐기하고 완료 후 다시 집계했다.

canonical 27쌍 exit 0, UX fixture 의도된 finding 12개/fail_count 0, 4앱 baseline exit 0·airport 1.320934를 다시 확인했다. 누적 CSS selector/media/specificity/comment, JSON 숫자/huge/deep, argparse, Git `+++`·가짜 hunk·added 행·CR/CRLF/LS/PS, self-symlink, JSON/Markdown/step summary redaction을 재실행했다. 합성 경로 marker·제품 traceback 없음과 일반 입력 오류 exit 2가 유지됐다. fixture bytes의 CR/CRLF를 보존했고 Windows 임시 Git LF→CRLF 경고를 제품 오류로 세지 않았다.

Windows의 설치된 `markdown-it-py 4.2.0`으로 `AUDIT/t103-post29-b-new.py ROOT OUTPUT_JSON oracle`을 실행해 새 최소 입력 8개의 `MarkdownIt("commonmark")` AST를 대조했다. container 전환 4개는 문단과 뒤의 fence가 별개이며, 들여쓴 inline 3개·같은 문단 inline 1개는 `code_inline`이다. [CommonMark 0.31.2 §3.1](https://spec.commonmark.org/0.31.2/#precedence)·[§4.5](https://spec.commonmark.org/0.31.2/#fenced-code-blocks)·[§6.1](https://spec.commonmark.org/0.31.2/#code-spans)의 block 우선순위·0~3열 fence·inline 정의와 함께 판정했다. parser 설치·registry 호출·제품 의존성 추가는 하지 않았다. 실제 MDX compiler/browser 검증으로 확대하지 않는다.

`gh run list --commit 9afea549dd81cb23d3297f83d89df4b519734382 --json databaseId,event,status,conclusion,headSha,url`와 `gh run view 34199104378 --json headSha,status,conclusion,jobs`로 [정확한 후보 PR CI](https://github.com/digitie/kor-travel-common/actions/runs/34199104378)의 해당 SHA·completed/success·6개 job 및 각 source SHA 비교 step 성공을 독립 확인했다. job 로그 전체·소비자 실행을 확인한 것으로 표시하지 않는다.

## B-P1-23 — 일반 inline 경로와 container 전환에서 block 경계를 계속 넘어감

- 원 심각도 **P1**, **OPEN(부분 수정) / FIX_REQUIRED**.
- 위치: `tools/ux_lint.py:433-450`의 닫힘 검색, `:452-476`의 fence 시작 판별, `:653-675`의 무효 info 분기 및 그 밖의 일반 inline fallback.
- post28 최소 입력 `"Example " + "`"*3 + "literal\n{window.confirm(\"x\")}\n" + "`"*3 + "\n"`는 여전히 P8을 누락한다. SHA256 `cf380531ead499a71602bc32fff9b0ec5d0343ccf864217a0ead35c9c831c6e7`. plain/quoted/nested·LF/CR/CRLF·P6/P8·전체/`--base`·설명 변형 2개 총 72개/OS가 기대 exit 1 대신 exit 0이다.
- 새 최소 입력은 `"`"*3 + "bad`info\n{window.confirm(\"x\")}\n> " + "`"*3 + "\n"`. SHA256 `422c0301746996c2856105345dc37edbc69bd0cb1a685e17328ee0f87d661146`. 마지막 줄은 새 blockquote의 fence이며 앞 문단 inline의 닫힘이 아니다.
- 재현 명령: 임시 Git root의 `Page.mdx`에 `safe\n`을 커밋해 `BASE`를 기록하고 위 bytes로 바꾼다. `PYTHON ROOT/tools/ux_lint.py --root TEMP --fail-new --json` 및 `--base BASE` 추가 명령을 실행한다. **기대 P8/exit 1, 실제 exit 0/findings=[]**. plain→quote, quote→plain, quote→nested, nested→quote × LF/CR/CRLF × 두 모드 = 24개/OS 누락이다.
- 원인: 일반 inline 경로에는 새 helper가 적용되지 않는다. 무효 info 경로에서도 helper가 닫힘 후보를 이전 container에 맞춰 검사하여 깊이가 달라지는 새 block을 inline 닫힘으로 허용한다.
- base/current 직접 대조: 설명 문구 반례는 0→0(미해결), plain→quote 반례는 1→0(이번 회귀). base는 `71a6f99`와 raw-only commit 사이 도구 diff가 없는 post28 worktree의 코드만 사용했다.
- 영향: 신규 실행 패턴이 필수 UX gate를 잘못 통과한다.
- 최소 권고: 모든 inline 닫힘 경로를 실제 Markdown block 경계 안으로 제한한다. 다음 줄의 독립 container를 판별하여 깊이 변화·block 종료를 기존 container 불일치와 혼동하지 않아야 한다. 정상 인용은 유지하고 미종결 span 뒤 실행식/JSX를 계속 검사한다.

## B-P2-13 — quoted 4열 닫힘은 정상 inline인데 fence로 오인됨

- 원 심각도 **P2**, **OPEN(부분 수정) / FIX_REQUIRED**. 이전 같은 행 triple 인용은 FIXED지만 정상 다중 행 인용 계약에 잔여 결함이 있다. 새 ID로 중복 집계하지 않는다.
- 위치: `tools/ux_lint.py:466`의 `candidate, _ = candidate_info`에서 콘텐츠 들여쓰기 값을 버린다. `:653-664`가 잘못된 fence 판정을 받아 정상 인용을 노출한다.
- 최소 입력은 `"> " + "`"*3 + "bad`info\n> {window.confirm(\"x\")}\n>     " + "`"*3 + "\n"`. 마지막 `>` 뒤 space는 5개, marker 선택 공백을 제외한 콘텐츠 들여쓰기는 4열이다. SHA256 `31f7bd33e12744d306d968de20e4f2aa466296453137d7fb85ab8eb903272004`.
- 위 임시 Git fixture와 두 CLI 모드로 재현한다. 기대는 같은 문단에서 닫힌 `code_inline` 제외·exit 0. **실제 P8/line 2/added true/exit 1**(bare CR의 report 좌표는 LF 기준 line 1). quoted/nested × LF/CR/CRLF × 두 모드 = 12개/OS 오검출이다.
- plain 4열 inline, quoted 같은 문단의 비-fence 닫힘 대조 12개/OS는 exit 0이다. 같은 행 triple 인용의 이전 36개/OS도 이제 제외된다. base/current 대조에서 같은 행 인용은 1→0으로 수정됐지만 quoted 4열 인용은 1→1로 남았다.
- 영향: 정상 문서 코드 예제를 신규 위반으로 차단한다. 실행 누락과 구분하여 P2를 유지한다.
- 최소 권고: helper가 콘텐츠 들여쓰기 0~3열만 fence로 인정하도록 값을 보존·검사하고, plain/quoted/nested가 동일한 block 기준을 사용하도록 대조한다. 정상 다중 행 인용과 실제 fence 종료의 양성/음성을 함께 고정한다.

## B-P3-24 — manifest의 focused 시험 수가 현재 후보와 다름

- 신규 **P3**, **OPEN / FIX_REQUIRED**. 위치: manifest `a100194`의 고정 검증 표에서 Windows·WSL focused 두 행.
- 재현: 같은 후보의 `-m unittest tests.test_kt_contrast tests.test_ux_lint`는 두 OS 모두 64개/skip 0인데 manifest는 63개로 기록한다. 이번 delta에 시험 1개가 추가됐으며 전체 302개와 focused의 관계를 원본 로그로 대조할 수 있다.
- 영향: 감사 기록의 실행 수가 부정확하다. 제품 검사 실패나 0-test false pass는 아니므로 P3다.
- 최소 권고: 후속 evidence에서 원 실행 로그와 환경에 따라 64개로 정정하고 이 manifest의 63개를 실제 실행 수로 재사용하지 않는다. 기존 immutable 원본은 보존한다.

## 누적 disposition·NOT_RUN·verdict

| 원 ID | 현재 판정 |
|---|---|
| B-P1-01, B-P1-02, B-P1-03, B-P1-04 | root/Git·baseline 증가·기존 MDX 표현식·오류/redaction 지정 반례 FIXED |
| B-P2-05, B-P2-06, B-P3-07 | 읽기 쌍·baseline JSON·geo 문서 FIXED |
| B-P1-08, B-P1-09, B-P2-10, B-P1-11, B-P1-12 | diff·CSS·airport·selector 지정 반례 FIXED |
| **B-P2-13** | 같은 행 원 반례 FIXED, 다중 행 잔여로 **OPEN(부분 수정)** |
| B-P1-14, B-P1-15, B-P1-16, B-P2-17, B-P2-18, B-P2-19 | 줄 종결자·Git mapping·suffix/열 지정 반례 FIXED |
| B-P2-20, B-P1-21, B-P1-22 | quoted fence·depth·marker 선택 공백 지정 반례 FIXED |
| **B-P1-23** | **OPEN(부분 수정)** |
| **B-P3-24** | 신규 **OPEN** |

- `NOT_RUN(Windows Python 3.11)`: 실행 파일 부재. Windows 3.14/WSL 3.11을 대체 실행으로 표시하지 않는다.
- `NOT_RUN(WSL Git diff --check 별도 실행, WSL 비교 parser, 이전 parser 탐색 미확정 차이 전체 재판정, 실제 MDX compiler/browser, CI 로그 전체, 비 UTF-8 Git 출력 직접 주입)`.
- `NOT_RUN(소비자 build/type/e2e·manifest 검사, npm/PyPI 설치·게시, workflow dispatch)`: 요청 범위 밖이며 호출하지 않았다.
- 기존 23개 중 21개 지정 반례 FIXED, P1/P2 각 1개 잔여와 신규 P3 1개다. P0 발견 0개이며 반복 교차 입력을 finding 수로 세지 않는다.
- **verdict: NO-GO.** 후보·manifest를 수정하지 않고 이 원본 한 파일만 report-only commit으로 확정한다.
