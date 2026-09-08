# T-103 post-fix-34 독립 적대적 리뷰 B 원본

- 실행 ID: `T103-PF34-B-20260908-180118`; reviewer: `/root/reviewer_b`.
- 시작 KST: `2026-09-08T18:01:18.7982004+09:00`; 후보 clean 확인 KST: `2026-09-08T18:08:45.6477848+09:00`; 잔여 focused/CLI 결과 확정 KST: `2026-09-08T18:10:53.3901513+09:00`.
- 불변 후보: `888fbbc2e943eab4198cf19a4dda6d88ce24b933`; tree: `3c25a2e5495ca6c2a91a8fc1815fee2b784bcf9f`.
- delta base: `9ae2b6de962bf42baea23e481e57e60be9c7bf47`.
- manifest: `de0c3ef9fb21d69458a50ba2c64fc4097f978396`의 `docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-34-manifest.md`; Git blob SHA-256: `38dbc972b57832656fe82dc0bfc359800bf052959bc0a19f6dd58189b6f5857b`.
- 격리: `F:/dev/kor-travel-common-wt/review-t103-post34-b` detached worktree. 시작과 원본 작성 직전 `git rev-parse HEAD 'HEAD^{tree}'`는 위 후보·tree와 일치하고 `git status --porcelain`은 모두 빈 출력이었다. 마지막 focused/CLI 확정 시에도 HEAD/tree는 같고 status에는 이 원본 한 파일만 untracked로 존재했다. 보고서 커밋은 별도 단계다.
- 후보·manifest·소비자·기존 evidence·Git 설정을 수정하지 않았다. 시작·종료 source `.git/config` SHA-256은 `0a0f849e7874cf0a25926856f9d2e381ccbf4c2dcb5999869c57b86e0f5beb5b`로 같다. post-33 원본과 상대 reviewer 결과·raw 본문을 읽지 않았다.

## 요청 원문

> T-103 post-fix-34 독립 리뷰를 시작해 주세요. immutable 후보 commit 888fbbc2e943eab4198cf19a4dda6d88ce24b933, tree 3c25a2e5495ca6c2a91a8fc1815fee2b784bcf9f, manifest de0c3ef(docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-34-manifest.md)입니다. post-33 원본/상대 결과는 읽지 말고 detached clean worktree에서 독립 Markdown parser, --base 추가행, 1·2자 opener·같은 줄·닫힘 없는 span, tilde/backtick, plain/blockquote/nested, indent/tab-stop, 오류/redaction를 검증하세요. 제품/manifest/소비자/evidence는 수정하지 말고 report 파일 하나만 작성해 report-only 커밋하세요. verdict, finding/disposition, SHA/SHA256, 시작·종료 HEAD/tree/clean, 테스트 결과만 보내 주세요.

## 판정: NO-GO

신규 P0 0건, P1 0건, **P2 1건(B-P2-26, OPEN)**, P3 0건이다. 기존 B-P1-23의 같은 줄 실행식 누락과 닫힘 없는 span/fence 경계는 이번 재현에서 FIXED다. 다만 같은 줄의 주석까지 검사하는 새 오류 때문에 주석 제외 계약을 만족하지 않는다. 후보 수정 없이 이 원본을 확정한다.

### B-P2-26 — opener 줄의 JavaScript 주석을 실행 패턴으로 보고함

- 위치: `tools/ux_lint.py:516`의 `_mask_inline_opener_line`, 호출부 `tools/ux_lint.py:870` 및 `tools/ux_lint.py:888`. 계약: `docs/tasks/T-103-kt-contrast-ux-lint.md` 구현 범위 2의 백틱·주석 안 인용 제외.
- 최소 입력은 다음 `Page.mdx`의 UTF-8/LF 바이트다. 마지막 LF 포함 SHA-256: `011032b250018daf78d3791ef68725e83890e51c3c074ec56c4cbcb8d397b9ad`.

````mdx
Example `literal {/* window.confirm("x") */}
~~~js
close `
~~~
````

- 재현: 임시 Git 저장소에 `Page.mdx` 내용 `safe\n`을 명시적으로 add·commit하고 그 SHA를 `BASE`로 저장한다. 그 파일을 위 바이트로 바꾼 뒤 후보의 절대 경로를 사용해 `python -B -X utf8 tools/ux_lint.py --root TEMP --fail-new --json` 및 같은 명령에 `--base BASE`를 더해 실행한다. `tools/ux_lint.py`는 후보 파일이며 `TEMP`만 쓰기 대상이다.
- 기대: 주석 안에만 P8 문자열이 있으므로 findings 0, exit 0. 실제: 두 명령 모두 `P8`, `line: 1`, `added: true`, exit 1. traceback은 없다.
- 독립 parser: Windows `markdown-it-py 4.2.0`, `MarkdownIt('commonmark')`는 첫 문단 `[0,1]`과 fence `[1,4]`로 분리한다. 첫 줄 backtick은 fence 내부의 backtick과 inline span을 만들지 않는다. 블록 구조를 먼저 구분하는 근거는 [CommonMark 0.31.2 §3.1](https://spec.commonmark.org/0.31.2/#precedence)·[§6.1](https://spec.commonmark.org/0.31.2/#code-spans)이며 2026-09-08 조회했다. JS 주석 제외 판정은 위 task 계약과 코드의 주석 마스킹 책임을 직접 대조했다. 실제 MDX compiler는 실행하지 않았다.
- 범위: plain/`> `/`>> ` × LF/CR/CRLF × 1·2자 opener × 전체/`--base` = **36건/OS 모두 동일 오류**. 같은 구조의 실제 호출은 정상 검출하고, matching backtick이 fence 안에 없는 주석·fence 내부 전용 호출·fence 전후 실제 호출 대조는 **180건/OS 모두 기대 일치**했다.
- 원인: helper는 delimiter만 공백으로 바꾸지만 반환 stop은 줄 끝이다. 호출부가 `index = stop`으로 이동하여 같은 줄의 `/* ... */`를 lexical scanner가 처리하지 못하고, 원문 주석이 후단 패턴 검사에 남는다. 직전 base에서 줄 전체를 가렸던 누락을 고치는 과정에서 생긴 새 false positive다.
- 영향: 정상 MDX 주석이 신규 금지 패턴으로 집계되어 `--fail-new`와 `--base` CI를 차단한다. 실제 소비자 적용 결과로 과장하지 않는다.
- 최소 수정: opener delimiter만 가린 뒤 바로 다음 문자부터 같은 줄의 기존 주석/표현식 처리를 재개한다. 1·2자 delimiter, 양 줄바꿈, 인용 깊이와 실제 호출 음성/양성 대조를 함께 회귀시험에 추가한다. disposition: **OPEN, 수정 필요**.

## 기존 finding 및 전체 delta 대조

- 제품 delta는 `tools/ux_lint.py`와 `tests/test_ux_lint.py`를 전부 읽었다. 나머지 변경은 이전 manifest/raw 경로임을 목록으로만 확인했고 raw 본문은 열지 않았다.
- **B-P1-23: FIXED.** 이전 짧은 1·2자 opener/cross-fence 216건과 같은 줄 P6/P8 216건이 각각 양 OS에서 기대 일치했다. 닫힘 없는 span/fence 앞·뒤 대조도 이번 216건 matrix에 포함했다. 새로운 주석 오류는 심각도·증상이 달라 B-P2-26으로 분리했다.
- **B-P2-13·B-P2-25: FIXED 유지.** 정상 inline/들여쓰기·tab-stop 및 `False` tuple 경계 48건과 72건의 exit/결과가 양 OS에서 기대 일치했다.
- **B-P3-24: FIXED 유지.** 현재 manifest의 focused 71건은 실제 focused 실행 건수와 일치한다.
- B-P1-01~04, B-P2-05~06, B-P3-07, B-P1-08~09, B-P2-10, B-P1-11~12의 기존 재현 105행을 재실행했다. root/CWD, baseline 증가, CSS cascade/selector, MDX runtime/문서, JSON 숫자/깊이, argparse/path redaction, symlink, airport를 결과별로 대조했으며 해당 반례는 FIXED 유지다. 105행은 보조 관찰 행을 포함하며 unittest 105개로 집계하지 않는다.
- B-P1-14~16, B-P2-17~22의 줄바꿈·diff·fence/container 경계는 현재 전체/focused 회귀에 포함된 범위에서 회귀가 없었다. 과거 별도 전체 matrix를 이번에 모두 재실행했다고 주장하지 않는다. 문서/task/소비자 경계와 GPL·미게시 계약에 이번 delta로 생긴 추가 문제는 발견하지 않았다.

## 실제 명령과 결과

환경은 Windows Python **3.14.3**, WSL uv Python **3.11.15**다. 모든 subprocess에서 상속 `GIT_*`를 제거했다. 전체·static 검사는 source object repo의 `git archive --format=zip 888fbbc2e943eab4198cf19a4dda6d88ce24b933`를 임시 사본에 풀어 실행했다. 사본 내부 Git fixture만 생성했고 source Git 설정은 건드리지 않았다.

| 검사 | Windows | WSL |
|---|---|---|
| `python -B -X utf8 -m unittest discover -s tests -p test_*.py` | 309개, skip 0, exit 0, 232.086초 | 309개 중 306개 실행, skip 3, exit 0, 53.275초 |
| `python -B -X utf8 -m unittest tests.test_kt_contrast tests.test_ux_lint` | 71개, skip 0, exit 0, 76.742초 | 71개, skip 0, exit 0, 20.116초 |
| `validate_plan.py` / `validate_document_links.py` | 106 task·493문서/2490 target, 오류 0 | 동일 |
| `check_spdx.py` | 56파일, 오류 0 | 동일 |
| `scan_secrets.py --all` / `check_prod_redaction.py --all` | 각각 625파일, 발견 0 | 동일 |
| `check_versions.py --self-check` | exit 0, 소비자 검사 아님 | 동일 |
| `check_aliases.py packages/tokens/aliases` 및 aliases focused | CSS 1·오류 0; 35개 skip 0 | CSS 1·오류 0; 35개 중 34개 실행, skip 1 |
| tokens 대비 CLI / UX fixture CLI | 27쌍 PASS·exit 0 / 12 findings·fail_count 0·exit 0 | 동일 |
| 기존 별도 corpus | 48+72+216+216건 기대 일치, 105개 관찰 대조 | 동일 |
| 새 comment/call/unclosed matrix | 216건 중 36건 오류, 180건 기대 일치 | 동일; 216행 JSON 완전 일치 |

실행 wrapper는 후보 밖 `.git/codex-audit/t103-post34-b-run.py`의 `win|wsl tests|corpus`, 새 matrix는 `t103-post34-b-new.py ROOT OUTPUT`, parser 대조는 같은 명령의 마지막 `oracle` 인자, focused/CLI는 `t103-post34-b-final.py win|wsl`이다. Windows prefix는 `py -3.14 -B -X utf8`, WSL은 `/home/digitie/.local/share/uv/python/cpython-3.11.15-linux-x86_64-gnu/bin/python3.11 -B -X utf8`다. 새 matrix의 기대 exit는 call/unclosed-after/unclosed-before만 1, 나머지는 0이며 prefix·newline·run·mode 전 조합을 실행했다. 기존 48/72/216/216행과 새 216행은 Windows/WSL JSON이 완전히 같다.

`git diff --check 9ae2b6de962bf42baea23e481e57e60be9c7bf47 888fbbc2e943eab4198cf19a4dda6d88ce24b933`은 exit 0/빈 출력이다. PowerShell glob을 rg 인자로 준 파일 탐색은 경로 오류를 내어 `rg -g test_*py tests` 방식으로 정정했다. 검증 실패나 제품 finding으로 집계하지 않았다.

원격은 `gh run view 34207168929 --json headSha,status,conclusion,jobs`로 읽기만 수행했다. exact 후보 head SHA, completed/success, 6개 job과 각 source SHA 확인 step의 success를 확인했다. [실제 CI](https://github.com/digitie/kor-travel-common/actions/runs/34207168929)는 성공했지만 신규 반례 36건이 없으므로 NO-GO를 바꾸지 않는다.

## NOT_RUN와 한계

- Windows Python 3.11: NOT_RUN(실행 파일 부재). WSL skip 3건은 Windows 8.3 전용 1건과 선택 `jsonschema` 모듈 미설치 2건이며 PASS 실행 건수에 포함하지 않았다.
- 실제 MDX compiler/browser, npm/PyPI registry 설치·게시, 소비자 저장소 빌드·타입·e2e·manifest 검증, workflow dispatch: NOT_RUN(허용된 common 독립 리뷰 범위 밖). Windows의 독립 CommonMark parser는 Markdown 블록 대조이며 MDX 런타임 증거를 대신하지 않는다.
- 원격 job 전체 로그·산출물 다운로드와 로컬 package pack/install: NOT_RUN(제품 delta가 두 Python 파일이고 원격 job 상태만 읽음). ECMAScript 전체 규격 페이지 조회는 크기 제한으로 실패했으며 이를 검증 성공으로 세지 않았다.
- 수정은 수행하지 않았고 기존 원본을 덮어쓰지 않았다. 이 파일만 추가한 raw-only commit을 별도로 생성하며 commit SHA·파일/Git blob SHA-256·최종 clean 상태는 완료 메시지에서 확정한다.
