# T-103 post-fix-36 독립 적대적 리뷰 B 원본

- 실행 ID: `T103-PF36-B-20260908-184724`; reviewer: `/root/reviewer_b`.
- 시작 KST: `2026-09-08T18:47:24.0266995+09:00`; 검증 종료 KST: `2026-09-08T18:54:49.1985528+09:00`.
- 불변 후보 commit: `d8027917e4cb88b72d5d5c98d571ef3522e808c8`; tree: `3e9d2614629eafddd8b2cf126d9e8234d1ab48c8`.
- delta base: `aedfdd659255c27bcc4377bd15b39452c004417d`.
- manifest: `36f08f26208899dc75df3d53de7444970d695810`의 `docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-36-manifest.md`; Git blob SHA-256: `6983aef44bdb8f052423278e5bd44f302d11aa22309bcde6973423aae5fdfc60`.
- 격리: `F:/dev/kor-travel-common-wt/review-t103-post36-b` detached worktree. 시작 SHA/tree는 위 값과 같고 `git status --porcelain`은 빈 출력이었다. 제품 delta는 `tools/ux_lint.py`·`tests/test_ux_lint.py` 전체를 읽었다. 나머지 이전 manifest/raw 변경은 경로만 확인했고 post-35 raw와 상대 reviewer 결과는 읽지 않았다.
- 종료 HEAD/tree도 위 후보와 같고, status에는 작성 중인 이 원본 하나만 untracked로 존재했다. source `.git/config` 시작·종료 SHA-256은 `0a0f849e7874cf0a25926856f9d2e381ccbf4c2dcb5999869c57b86e0f5beb5b`로 일치한다. 후보·manifest·소비자·기존 evidence·Git 설정을 수정하지 않았으며 이 원본만 별도 커밋한다.

## 요청과 판정

> T-103 post-fix-36 독립 적대 리뷰를 진행해 주세요. immutable 후보 commit d8027917e4cb88b72d5d5c98d571ef3522e808c8, tree 3e9d2614629eafddd8b2cf126d9e8234d1ab48c8, manifest commit 36f08f2( docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-36-manifest.md )입니다. post-35 raw와 reviewer A 결과는 읽지 말고, 별도 detached clean worktree에서 제품 코드·manifest·소비자·기존 evidence는 수정하지 마세요. 독립 Markdown/CommonMark parser 대조와 --base 추가행을 포함해 URL/prose // 누락, apostrophe/따옴표 fence 오탐, 실제 JS 주석·표현식 보존, short run·tilde/backtick·plain/blockquote/nested·indent/tab-stop·오류/redaction을 양 OS에서 검증하세요. 원본 report 파일 하나만 작성해 report-only 커밋하고 verdict, finding/disposition, SHA/SHA256, 시작/종료 HEAD/tree/clean, Windows/WSL 결과를 알려 주세요. 상대 reviewer 결과를 보지 마세요.

**NO-GO.** 기존 **B-P1-28·B-P2-27은 부분 수정 OPEN**, 신규 **B-P2-29 OPEN**이다. 기존 B-P2-26의 최소 반례는 FIXED다. 총 OPEN은 P1 1건·P2 2건이며 신규 P0/P1/P3는 0건이다. 후보 수정 없이 원본을 확정한다.

## B-P1-28 — 문장 첫 단어 때문에 URL 뒤 실행식을 다시 누락

- 위치: `tools/ux_lint.py:728`의 `_is_mdx_lexical_code`, 특히 `:737`의 키워드 정규식과 `:589`의 재개 후보 전처리.
- 최소 입력은 아래 한 줄과 마지막 LF다. UTF-8 SHA-256: `ca29b4a58f267b96e1099d760cf1c8eb71def7718230fec57be831fdb7b83a06`.

````mdx
for example, `literal https://example.invalid {window.confirm("x")}
````

- 기대: 일반 문장 안 실제 MDX 실행식이므로 P8 1건·exit 1. 실제: 전체/`--base`에서 findings 0·exit 0, traceback 없음. `// prose`도 같은 결과다.
- 기존 `Example` 문장에서는 수정됐지만 첫 단어가 `for`이면 새 정규식이 JavaScript 문맥으로 단정한다. `for example,`는 JavaScript for 구문이 아닌 정상 문장이다. 그 URL의 `//`가 line comment로 처리되어 실제 실행식이 재개 후보에서 지워진다.
- Windows/WSL의 plain/`> `/`>> ` × LF/CR/CRLF × 1·2자 run × 전체/`--base`에서 URL/prose slash 72건/OS가 누락되고 실제 JS 주석·URL 없는 호출 대조 72건/OS는 기대 일치했다.
- 영향: 신규 P8 위반이 diff gate를 통과한다. 최소 수정은 첫 단어 목록이 아닌 실제 MDX 표현식·JSX·ESM 경계를 사용해 JavaScript 문맥을 확정하는 것이다. 일반 `for example,`·`if needed,` 문장은 코드로 승격하지 않아야 한다. disposition: **부분 수정 OPEN, 원 P1 유지**.

## B-P2-27 — 같은 첫 단어 판정으로 apostrophe가 fence를 다시 숨김

- 위치: `tools/ux_lint.py:737`의 문맥 판정과 `:978`의 quote 진입. 최소 입력 UTF-8/LF·마지막 LF 포함 SHA-256: `cfd954f642409f078cda76b9a3ff679c671142216902b6e2e25f9a73933356c1`.

````mdx
for example, `don't
~~~js
{window.confirm("x")}
close `
~~~
````

- 기대: P8은 fence 내부 문서 코드이므로 findings 0·exit 0. 실제: `P8`, `line: 3`, `added: true`, exit 1. `don't` 대신 일반 문장의 닫히지 않은 큰따옴표도 같다.
- 동일한 plain/인용 깊이·LF/CR/CRLF·1/2 run·전체/`--base` 교차에서 apostrophe/큰따옴표 72건/OS가 오검출되고, 같은 줄의 닫힌 따옴표·보통 문장·실제 호출 전후 144건/OS는 기대 일치했다.
- 기존 `Example` 최소 반례는 수정됐지만 일반 문장의 첫 단어만 바꿔 동일한 quote 상태 문제가 남는다. 정상 문서가 CI를 차단한다. 위 B-P1-28과 함께 실제 코드 영역을 확정하고 문장 quote가 다음 Markdown 블록의 마스킹을 막지 않도록 수정해야 한다. disposition: **부분 수정 OPEN, 원 P2 유지**.

## B-P2-29 — 중괄호 뒤 공백이 있는 주석 내부로 재개

- 위치: `tools/ux_lint.py:681`의 정확한 `text.startswith("{/*", index)` 조건, `:523`의 `_mask_mdx_resume_comments`, `:589` 이후 재개 후보 탐색.
- 최소 입력 UTF-8/LF·마지막 LF 포함 SHA-256: `278f4ae3df2dc9906eb93b785a40f65f8c163610164ad884118c527fae05dc10`.

````mdx
Example `literal
{ /* <div className="outline-none"/> {window.confirm("x")} */}
~~~js
code
~~~
````

- 기대: P6/P8 문자열은 모두 JS block comment 안이므로 findings 0·exit 0. 실제: `P6`·`P8`, 각각 `line: 2`, `added: true`, exit 1, traceback 없음. 중괄호 뒤 tab·줄바꿈도 재현된다.
- `{/*`는 통과하지만 `{ /*`는 특수 분기에서 빠진다. 나머지 표현식 판별도 주석 뒤 닫는 중괄호를 실행식 시작으로 보지 않아 주석을 가리지 못한다. 이후 주석 내부 `<div`/`{window.confirm...}`를 재개 위치로 선택한다.
- 공백/tab/줄바꿈 × 인용 깊이·run·LF/CR/CRLF·전체/`--base`에서 108건/OS가 오검출된다. 공백 없는 주석 및 주석 뒤 실제 호출 양성 대조 72건/OS는 기대 일치했다. base와 후보의 함수를 동일 입력으로 직접 대조하면 base는 호출 문자열을 제거하고 후보는 보존한다. 이번 delta의 신규 회귀다.
- 영향: 유효한 주석이 신규 금지 패턴으로 집계되어 gate를 차단한다. 최소 수정은 실제 MDX 표현식 시작과 주석-only 표현식을 공백·줄바꿈에 관계없이 인식하고, 주석 내부를 재개 후보로 선택하지 않게 하는 것이다. disposition: **신규 P2 OPEN**.

## 독립 해석과 재현 방법

Windows의 `markdown-it-py 4.2.0`, `MarkdownIt('commonmark')`로 새 15개 양성/음성 입력의 블록을 대조했다. `for example,` 입력은 일반 문단이며 apostrophe 예제는 첫 문단 `[0,1]`·fence `[1,5]`다. 주석 예제는 문단 `[0,2]`·fence `[2,5]`로 구분된다. [CommonMark 0.31.2 블록 우선 규칙](https://spec.commonmark.org/0.31.2/#precedence) 및 [MDX 공식 문법](https://mdxjs.com/docs/what-is-mdx/#expressions)(페이지 수정 2025-01-27, 조회 2026-09-08)의 문장/중괄호 표현식/주석 경계를 근거로 기대를 정했다. 실제 MDX compiler/browser는 NOT_RUN이며 parser 대조를 실행 증거로 대체하지 않는다.

각 CLI 반례는 임시 Git 저장소에 `Page.mdx` 내용 `safe\n`을 명시적으로 add·commit하여 `BASE`를 만든 다음 그 파일만 입력 바이트로 바꿔 재현했다. 후보의 절대 도구 경로에 `--root ROOT --fail-new --json`과 `--root ROOT --fail-new --json --base BASE`를 각각 실행했다. `ROOT`만 fixture 쓰기 대상이다. 각 matrix는 exit와 findings 건수를 모두 대조했다.

후보 밖 `.git/codex-audit/t103-post36-b-new.py ROOT OUTPUT`는 B-P2-27 216행, `t103-post36-b-url.py ROOT OUTPUT`는 B-P1-28 144행, `t103-post36-b-comments.py ROOT OUTPUT`는 B-P2-29 180행이다. 각 스크립트 뒤 `oracle` 인자로 독립 parser를 호출했다. Windows prefix는 `py -3.14 -B -X utf8`; WSL은 `/home/digitie/.local/share/uv/python/cpython-3.11.15-linux-x86_64-gnu/bin/python3.11 -B -X utf8`이다.

## 검증과 기존 disposition

- B-P2-26 최소 반례와 주석/실행식/fence 전후 216행, B-P2-27의 `Example` 대조 216행, B-P1-28의 `Example` 대조 144행을 재실행했다. 원래 입력의 수정과 위 일반 문장·공백 변형의 실패를 분리했다.
- B-P1-23의 짧은 run/cross-fence 216행과 같은 줄 실행식 216행, B-P2-13/B-P2-25의 inline·indent/tab-stop·`False` 대조 48/72행을 실행했다. 해당 최소 반례에는 회귀가 없다. B-P3-24는 focused 수 76으로 현재 manifest와 일치한다.
- 기존 root/CWD, baseline 증가, CSS cascade/selector, JSON 깊이·숫자, argparse/path/redaction·symlink, MDX, airport 105개 관찰 행도 재실행했다. 관찰 행을 unittest 개수로 집계하지 않는다. 과거 별도 matrix 전부를 실행했다고 주장하지 않는다. 현재 task IN_PROGRESS·소비자 미실행·npm/PyPI 미게시 경계에서 새 문서 충돌은 발견하지 않았다.
- 전체/static/focused는 exact candidate `git archive --format=zip`을 임시 사본으로 풀어 실행했고 `GIT_*` 상속을 제거했다. 임시 사본 안에서만 Git fixture를 만들고 파일을 40개씩 명시적으로 stage했다. 보조 스크립트는 `t103-post36-b-run.py ROOT win|wsl tests|corpus`, `t103-post36-b-fixes.py ROOT win|wsl corpus`, `t103-post36-b-final.py win|wsl`이다.

| 검증 | Windows Python 3.14.3 | WSL Python 3.11.15 |
|---|---|---|
| `-m unittest discover -s tests -p test_*.py` | 314 실행, skip 0, exit 0, 316.945초 | 314개 중 311 실행, skip 3, exit 0, 62.653초 |
| contrast/UX focused | 76 실행, skip 0, exit 0, 165.122초 | 76 실행, skip 0, exit 0, 30.237초 |
| plan·문서 링크 | 106 task·499문서/2496 target, 오류 0 | 동일 |
| SPDX | 56파일, 오류 0 | 동일 |
| secrets/redaction `--all` | 각각 631파일, 발견 0 | 동일 |
| versions self-check / aliases | exit 0 / CSS 1·오류 0, aliases 35 실행·skip 0 | exit 0 / CSS 1·오류 0, aliases 34 실행·skip 1 |
| tokens 대비 CLI / UX fixture CLI | 27쌍 PASS / 12 findings·fail_count 0, exit 0 | 동일 |
| 신규 교차 재현 540행 | 252행 오류·288행 기대 일치 | 동일 |

기존 matrix 48/72/216/216/216/216/144행과 신규 216/144/180행의 Windows/WSL JSON은 각각 완전히 일치했다. focused 명령은 `-m unittest tests.test_kt_contrast tests.test_ux_lint`다. 정적 명령은 `tools/validate_plan.py`, `tools/validate_document_links.py`, `tools/check_spdx.py`, `tools/scan_secrets.py --all`, `tools/check_prod_redaction.py --all`, `tools/check_versions.py --self-check`, `tools/check_aliases.py packages/tokens/aliases`이며 모두 exit 0이다. 레지스트리 자기 검사를 소비자 검사 성공으로 세지 않는다.

`git diff --check aedfdd6 d8027917`은 exit 0·빈 출력이었다. `gh run view 34211197016 --json headSha,status,conclusion,jobs`로 [exact 후보 CI](https://github.com/digitie/kor-travel-common/actions/runs/34211197016)의 head SHA·completed/success, 6개 job과 source SHA 확인 step의 success를 읽기 전용으로 확인했다. 이 성공은 새 반례를 닫지 않는다.

## NOT_RUN와 보존

- Windows Python 3.11: NOT_RUN(실행 파일 부재). WSL skip은 Windows 8.3 전용 1건과 선택 `jsonschema` 미설치 2건이며 실행 성공 건수에 더하지 않았다.
- 실제 MDX compiler/browser, npm/PyPI registry 설치·게시, 소비자 저장소 build/type/e2e/manifest, workflow dispatch: NOT_RUN(범위 밖).
- 원격 job 전체 로그·산출물 다운로드, 로컬 package pack/install, 과거 별도 matrix 전부: NOT_RUN(이번 제품 delta와 명시한 재현 범위로 한정). 실제 소비자 영향으로 과장하지 않는다.
- 이 원본 파일만 추가한 report-only commit을 만들고 commit SHA·파일/Git blob SHA-256·종료 clean 상태를 완료 메시지로 확정한다. 후보 제품 코드의 수정·commit·push는 수행하지 않았다.
