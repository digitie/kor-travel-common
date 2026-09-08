# T-103 post-fix-35 독립 적대적 리뷰 B 원본

- 실행 ID: `T103-PF35-B-20260908-182124`; reviewer: `/root/reviewer_b`.
- 시작 KST: `2026-09-08T18:21:24.4886001+09:00`; 검증 종료 KST: `2026-09-08T18:27:27.6705432+09:00`.
- 후보 commit: `aedfdd659255c27bcc4377bd15b39452c004417d`; tree: `4bb189dddeab51d3cd0222d0ab50bef17a84ad99`.
- delta base: `888fbbc2e943eab4198cf19a4dda6d88ce24b933`.
- manifest: `ea60635fa9472afb5a5ac10eb24b4c33a1660ab4`의 `docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-35-manifest.md`; Git blob SHA-256: `8d8d8f1ae1dffe8dd955fd4e556ba2f3d5e9c94e88d6b82d848aeddf9df8e5b1`.
- 격리: `F:/dev/kor-travel-common-wt/review-t103-post35-b` detached worktree. 시작·종료 `git rev-parse HEAD 'HEAD^{tree}'`는 위 후보·tree와 같고, 두 `git status --porcelain`은 빈 출력이었다. 이 원본만 이후 별도 커밋한다.
- source `.git/config` 시작·종료 SHA-256: `0a0f849e7874cf0a25926856f9d2e381ccbf4c2dcb5999869c57b86e0f5beb5b`. 후보·manifest·소비자·기존 evidence·Git 설정은 수정하지 않았다. post-34 원본과 상대 reviewer 결과/raw 본문을 읽지 않았다.

## 요청과 판정

> T-103 post-fix-35 독립 리뷰를 시작해 주세요. immutable 후보 commit aedfdd659255c27bcc4377bd15b39452c004417d, tree 4bb189dddeab51d3cd0222d0ab50bef17a84ad99, manifest ea60635(docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-35-manifest.md)입니다. post-34 원본/상대 결과는 읽지 말고 detached clean worktree에서 독립 Markdown parser, --base 추가행, 짧은 run, 같은 줄 주석/실행식, 닫힘 없는 span·tilde/backtick, plain/blockquote/nested·indent/tab-stop·오류/redaction를 검증하세요. 제품/manifest/소비자/evidence는 수정하지 말고 report 파일 하나만 작성해 report-only 커밋하세요. verdict, finding/disposition, SHA/SHA256, 시작·종료 HEAD/tree/clean, 테스트 결과만 보내 주세요.

**NO-GO.** 기존 B-P2-26은 FIXED지만 신규 **B-P1-28 OPEN 1건**, **B-P2-27 OPEN 1건**이 있다. 신규 P0/P3는 0건이다. 재현 이후 후보 수정 없이 이 원본을 확정한다.

## B-P1-28 — 일반 문장의 URL을 JS 주석으로 해석해 실행식을 누락

- 위치: `tools/ux_lint.py:531`, `_mask_unclosed_inline_span`의 새 remainder 전처리와 `tools/ux_lint.py:903`의 line-comment 전이.
- 최소 `Page.mdx` 입력(LF와 마지막 LF 포함)의 SHA-256은 `6eb2bbbc1aadcb5a349210d78a665ad6331d9d88bd4605e110201969465c4e11`이다.

````mdx
Example `literal https://example.invalid {window.confirm("x")}
````

- 기대: 닫히지 않은 backtick은 일반 문자의 일부이며 URL 뒤 `{window.confirm("x")}`는 MDX 실행식이다. P8 1건, exit 1이어야 한다. 실제: 전체/`--base` 모두 `findings: []`, exit 0, traceback 없음.
- URL 대신 일반 문장 `// prose`를 넣어도 같다. plain/`> `/`>> ` × LF/CR/CRLF × 1·2자 run × 전체/`--base`에서 URL과 prose slash **72건/OS 모두 누락**했다. 실제 JS 주석 `{/* window.confirm("x") */}`과 URL 없는 실제 실행식 대조 **72건/OS는 기대와 일치**했다.
- 독립 근거: `markdown-it-py 4.2.0`의 `MarkdownIt('commonmark')`는 이 내용을 하나의 일반 문단으로 해석하고 inline code를 만들지 않는다. [MDX 공식 Expressions 설명](https://mdxjs.com/docs/what-is-mdx/#expressions)은 문장 안 중괄호를 JavaScript 표현식으로 정의하고 JS 주석을 중괄호 안에서 작성하도록 설명한다(페이지 수정일 2025-01-27, 조회 2026-09-08). 실제 compiler/browser 실행은 NOT_RUN이며 문법·계약과 검사기 결과의 대조다.
- 원인: Markdown 문장 조각 전체에 `ignore_backticks=False`의 JS lexer를 적용하여 URL의 `//`부터 줄 끝까지 가린다. 실행식 재개 후보를 찾기 전에 실제 `{...}`도 지워지고, 원본 문단 전체가 마스킹된다.
- base 원인 대조: 두 버전의 `_mask_comments_and_backticks`를 각 Git object 코드로 로드한 동일 입력 시험에서 base는 호출을 보존(`True`), 후보는 제거(`False`)했다. 전체 base CLI 회귀를 실행했다고 주장하지 않는다.
- 영향: 실제 P8 위반을 `--fail-new`와 `--base` gate가 정상으로 통과시킨다. 최소 수정은 Markdown 문장과 실행식 경계를 먼저 구분하고 확인된 JS 표현식 내부에만 주석 규칙을 적용하는 것이다. URL·일반 slash 문장·진짜 JS 주석·실행식을 함께 회귀시험에 넣어야 한다. disposition: **OPEN, 수정 필요**.

## B-P2-27 — 문장 속 apostrophe가 다음 fence의 마스킹을 막음

- 위치: `tools/ux_lint.py:516`, delimiter 뒤 재개; `tools/ux_lint.py:829`와 `tools/ux_lint.py:837`, 문장과 JS 문자열을 구분하지 않는 quote 상태.
- 최소 입력의 UTF-8/LF·마지막 LF 포함 SHA-256은 `5b18d6859963b2c6b89e50bf06e8f89277c3fc8467efdd2c8b15635b6341f857`이다.

````mdx
Example `don't
~~~js
{window.confirm("x")}
close `
~~~
````

- 기대: P8은 fenced 문서 코드 안에만 있으므로 findings 0, exit 0. 실제: `P8`, `line: 3`, `added: true`, exit 1, traceback 없음. `don't` 대신 닫히지 않은 일반 큰따옴표 문장도 같은 결과다.
- plain/`> `/`>> ` × LF/CR/CRLF × 1·2자 run × 전체/`--base`의 apostrophe/큰따옴표 **72건/OS 모두 오검출**했다. 같은 줄에서 닫힌 따옴표·일반 문장·fence 앞뒤 실제 호출 대조 **144건/OS는 기대 일치**했다.
- 독립 parser는 첫 문단 `[0,1]`과 fence `[1,5]`를 구분한다. [CommonMark 0.31.2 §3.1](https://spec.commonmark.org/0.31.2/#precedence)의 블록 우선 해석과 일치한다. JS 문자열 상태가 Markdown 블록 경계를 덮어서는 안 된다.
- 원인: delimiter 뒤 재개 후 일반 문장의 apostrophe가 JS quote를 열고, 다음 줄의 `~~~`를 fence로 처리하지 않는다. base 함수에서는 호출 제거(`False`), 후보에서는 호출 보존(`True`)으로 이번 delta의 회귀를 확인했다.
- 영향: 정상 문서 코드가 신규 위반으로 집계되어 CI를 차단한다. 최소 수정은 Markdown 블록 경계를 먼저 확정하고 JS quote 상태를 실제 JS 영역으로 한정하는 것이다. 기존 같은 줄 실제 호출 검출과 B-P2-26 주석 제외도 함께 보존해야 한다. disposition: **OPEN, 수정 필요**.

## 재현 명령과 회귀 disposition

각 반례는 임시 Git 저장소에 `Page.mdx`의 `safe\n`을 명시적으로 add·commit하여 `BASE`를 만들고, 해당 파일만 반례 바이트로 바꾼 후 실행했다. `ROOT`는 임시 fixture이며 도구는 불변 후보의 절대 경로다.

```text
python -B -X utf8 CANDIDATE/tools/ux_lint.py --root ROOT --fail-new --json
python -B -X utf8 CANDIDATE/tools/ux_lint.py --root ROOT --fail-new --json --base BASE
```

Windows prefix는 `py -3.14 -B -X utf8`, WSL은 `/home/digitie/.local/share/uv/python/cpython-3.11.15-linux-x86_64-gnu/bin/python3.11 -B -X utf8`이다. 후보 밖 `.git/codex-audit/t103-post35-b-new.py ROOT OUTPUT`가 B-P2-27의 216행, `t103-post35-b-url.py ROOT OUTPUT`가 B-P1-28의 144행을 생성한다. 같은 명령 뒤 `oracle` 인자로 독립 parser의 10개 양성/음성 구조를 관찰했다. 두 matrix는 exit뿐 아니라 findings 건수도 대조했다.

- **B-P2-26 FIXED**: 주석·실행식·미종결 span/fence 전후 216건/OS 모두 기대 일치.
- **B-P1-23 FIXED 유지**: 짧은 run/cross-fence 216건과 같은 줄 실행식 216건/OS 모두 기대 일치. 새 문장 문맥 회귀는 위 두 ID로 별도 기록했다.
- **B-P2-13/B-P2-25 FIXED 유지**: 정상 inline·들여쓰기/tab-stop 48건과 `False`/문장 경계 72건/OS 기대 일치. **B-P3-24 FIXED 유지**: manifest focused 72건과 실제 실행 건수가 일치한다.
- B-P1-01~04, B-P2-05~06, B-P3-07, B-P1-08~09, B-P2-10, B-P1-11~12의 기존 105개 관찰 행을 재실행해 root/CWD, baseline 증가, CSS, JSON/argparse/redaction, symlink, MDX, airport 결과를 대조했다. 해당 기존 최소 반례는 FIXED 유지이며 105행을 unittest 105개로 집계하지 않는다.
- B-P1-14~16/B-P2-17~22는 현재 전체/focused 회귀에 포함된 범위에서 재발이 없었다. 과거 별도 matrix 모두를 다시 실행했다고 주장하지 않는다. 제품 delta 2파일(`tools/ux_lint.py`, `tests/test_ux_lint.py`)은 전부 읽었고, 나머지 변경은 이전 manifest/raw 경로만 확인했다. 현재 task의 IN_PROGRESS·소비자 미실행·미게시 경계에는 새 문서 충돌을 발견하지 않았다.

## 실제 검증 결과

전체/static/focused는 exact candidate의 `git archive --format=zip`을 임시 사본에 풀어 실행했고 상속 `GIT_*`를 제거했다. Windows 3.14.3 및 WSL 3.11.15를 사용했다. Windows 첫 full/static 보조 스크립트는 임시 사본의 명시적 `git add` 인자 길이가 한계를 넘어 `WinError 206`으로 제품 시험 실행 전에 실패했다. 그 실행은 폐기하고 **보조 스크립트만** 파일 40개씩 명시적으로 stage하도록 바꿔 재실행했다. 후보/Git 설정 변경은 없었다.

| 검증 | Windows | WSL |
|---|---|---|
| `-m unittest discover -s tests -p test_*.py` | 310 실행, skip 0, exit 0, 248.398초 | 310개 중 307 실행, skip 3, exit 0, 36.278초 |
| `-m unittest tests.test_kt_contrast tests.test_ux_lint` | 72 실행, skip 0, exit 0, 137.961초 | 72 실행, skip 0, exit 0, 26.349초 |
| `validate_plan.py` / `validate_document_links.py` | 106 task·496문서/2493 target, 오류 0 | 동일 |
| `check_spdx.py` | 56파일, 오류 0 | 동일 |
| `scan_secrets.py --all` / `check_prod_redaction.py --all` | 각각 628파일, 발견 0 | 동일 |
| `check_versions.py --self-check` | exit 0, 소비자 검사는 아님 | 동일 |
| `check_aliases.py packages/tokens/aliases` / aliases focused | CSS 1·오류 0 / 35 실행·skip 0 | CSS 1·오류 0 / 34 실행·skip 1 |
| `kt_contrast.py packages/tokens/tokens.css --json` | 27쌍 PASS, exit 0 | 동일 |
| `ux_lint.py --root tests/fixtures/ux --json` | 12 findings, fail_count 0, exit 0 | 동일 |
| 신규 두 matrix | 360행 중 144행 오류, 216행 기대 일치 | 동일 |

후보 밖 `t103-post35-b-run.py ROOT win|wsl tests|corpus`, Windows 재실행의 `t103-post35-b-run-win.py`, `t103-post35-b-final.py win|wsl`로 위 결과를 수집했다. 48/72/216/216/216건 기존 matrix와 신규 216/144행은 Windows/WSL JSON이 완전히 같았다. `git diff --check 888fbbc aedfdd6`은 exit 0/빈 출력이었다.

`gh run view 34208926971 --json headSha,status,conclusion,jobs`로 [exact 후보 CI](https://github.com/digitie/kor-travel-common/actions/runs/34208926971)의 head SHA 일치, completed/success, 6개 job과 각 source SHA 확인 step의 success를 읽기 전용으로 확인했다. 기존 회귀/CI 성공은 신규 반례의 NO-GO를 바꾸지 않는다.

## NOT_RUN와 원본 보존

- Windows Python 3.11: NOT_RUN(실행 파일 부재). WSL skip 3건은 Windows 8.3 전용 1건과 선택 `jsonschema` 미설치 2건이다. skip을 실행 성공 건수에 더하지 않았다.
- 실제 MDX compiler/browser, npm/PyPI registry 설치·게시, 소비자 저장소 build/type/e2e/manifest, workflow dispatch: NOT_RUN(범위 밖). 독립 CommonMark parser 결과를 MDX compiler 실행으로 표현하지 않는다.
- 원격 job 전체 로그·산출물 다운로드, 로컬 package pack/install, 과거 별도 전체 matrix 전부: NOT_RUN(이번 제품 delta와 명시한 재현 범위로 한정). 실제 소비자 영향은 재현하지 않았다.
- 이 원본 파일 하나만 report-only commit으로 보존하고 commit SHA·파일/Git blob SHA-256·최종 clean 상태는 완료 메시지로 확정한다. 후보 수정·commit·push는 수행하지 않았다.
