# T-103 post-fix-33 독립 적대적 리뷰 B 원본

- 실행 ID `T103-PF33-B-20260908-174317`; 시작 KST `2026-09-08T17:43:17.4077058+09:00`.
- 제품 후보 HEAD `9ae2b6de962bf42baea23e481e57e60be9c7bf47`, tree `125095a9ad9af4979cec6e784bd2e781c69de662`.
- 격리 worktree `F:/dev/kor-travel-common-wt/review-t103-post33-b`의 detached 시작 status는 clean이다. 후보·manifest·소비자·기존 evidence·Git 설정을 수정하지 않고 원본 한 파일만 별도 커밋한다.
- manifest: `77a94e4`의 `docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-33-manifest.md`를 `git show`로 읽었다. blob SHA-256 `646e9b6df57041ec5e134a8ee606fa2241cbb7668c13f22089e686f0709a70fd`.
- `2375c8b..9ae2b6d` 제품 2파일 전체 diff를 읽었다. 나머지 변경 3파일은 이전 manifest·A/B 원본의 경로만 확인했다. post32 원본과 상대 결과는 읽거나 요청하지 않았다.
- 범위: 독립 Markdown parser·Git 추가행/`--base`·1/2자 inline·중간 tilde/긴 backtick·plain/quoted/nested·indent/tab-stop·오류/redaction. source `.git/config` 시작 SHA-256 `0A0F849E7874CF0A25926856F9D2E381CCBF4C2DCB5999869C57B86E0F5BEB5B`.

## 판정과 disposition

**NO-GO — B-P1-23 부분 수정 OPEN**. 이전의 다음 줄 실행식은 수정됐지만 같은 줄 실행식이 남아 있다. 새 P0/P1/P2/P3 ID를 추가하지 않고 동일 원인의 잔여로 기록한다.

| ID·심각도 | disposition | 근거 |
|---|---|---|
| B-P1-23 | 부분 수정 OPEN | 다음 줄의 P8 및 3/4자 span은 FIXED. 1/2자 opener와 같은 줄의 P8은 전체 줄 마스킹으로 누락. |
| B-P2-25 | FIXED 유지 | 내부 짧은 marker 72교차에서 정상 출력·exit 0, TypeError 없음. |
| B-P2-13 | FIXED 유지 | 같은 문단/같은 행 닫힘과 quoted/nested 4열·tab-stop 대조. |
| B-P3-24 | FIXED 유지 | manifest focused 69 표기를 실제 실행과 대조. |
| B-P1-01/02/03/04, B-P2-05/06, B-P3-07, B-P1-08/09, B-P2-10, B-P1-11/12/14/15/16, B-P2-17/18/19/20, B-P1-21/22 | FIXED 유지(검증 범위 한정) | 변경 없는 코드의 이전 검증을 동일성으로 재사용하고 이번 full/focused 및 선택한 직접 corpus를 실행했다. 과거 모든 개별 CLI의 전수 재실행은 아니다. |

## B-P1-23 최소 재현

위치: `tools/ux_lint.py:510`~519 `_mask_inline_opener_line`, 호출 지점 `:863`, `:881`. 새 함수는 fence 경계를 발견하면 opener 이후 같은 줄의 모든 문자를 공백으로 바꾸고 다음 줄로 건너뛴다.

~~~~python
text = 'Example ' + chr(96) + 'literal {window.confirm("x")}\n~~~js\nclose ' + chr(96) + '\n~~~\n'
~~~~

- UTF-8 SHA-256 `da6c3141f6d062b9358c7d5e08d51866a99bd967838e8783e77b49bf31a6a644`.
- 임시 Git 저장소의 `Page.mdx`를 `safe\n`으로 커밋해 BASE를 만든 뒤 위 입력으로 바꾼다. `python tools/ux_lint.py --root TEMP --fail-new --json` 및 `--base BASE`를 추가한 명령을 실행한다.
- 기대: line 1의 실행식은 문서 code span 밖이므로 P8·exit 1. 실제 양 OS는 exit 0, `findings=[]`, traceback 없음이다.
- 독립 `markdown-it-py 4.2.0`의 `MarkdownIt('commonmark')` AST는 paragraph `[0,1]` + fence `[1,4]`다. 실행식은 첫 paragraph의 text이며 닫힘 backtick은 별도 fenced block 내용이다. 정상 같은 행에서 닫힌 대조는 `code_inline`이다. [CommonMark 0.31.2 block 우선](https://spec.commonmark.org/0.31.2/#precedence)·[code span](https://spec.commonmark.org/0.31.2/#code-spans) 기준으로 판정했다. 실제 MDX compiler 실행으로 기록하지 않는다.
- 새216교차/OS: plain/quoted/nested × 1/2/3/4자 run × 중간 tilde/더 긴 backtick/정상 닫힘 × LF/CR/CRLF × 전체/`--base`. 1/2자와 중간 fence의 조합72개만 누락되고 나머지144개는 기대와 일치한다.
- 영향: 새 추가행에 실제 MDX 실행식이 있어도 gate가 통과한다. newline 위치에 따라 의미가 같은 실행식의 판정이 달라진다.
- 최소 수정: block fence로 인해 미종결로 판정된 span에서 줄 전체를 버리지 말고, 기존 미종결 span의 실행식/JSX 재개 판정과 일관되게 같은 줄의 실행식도 검사한다. 이미 닫힌 인용, 1/2/3/4자, 같은 줄/다음 줄, fence 전후, quoted/nested 및 4열/tab-stop 음성 대조를 함께 보존한다. 기존 B-P1-23의 마스킹 경계가 아직 닫히지 않았으므로 부분 수정 OPEN이다.

## 명령·검증 경계

Windows `py -3.14 -B -X utf8`, WSL `/home/digitie/.local/share/uv/python/cpython-3.11.15-linux-x86_64-gnu/bin/python3.11 -B -X utf8`를 사용했다. ROOT는 위 worktree, AUDIT는 source `.git/codex-audit`다. fixture·probe·로그는 후보 밖의 임시 디렉터리에만 쓰고 `GIT_*` 환경을 제거했다.

```text
python AUDIT/t103-post33-b-run.py ROOT win|wsl tests
  -> exact SHA git archive 사본의 full/focused/static/aliases focused
python AUDIT/t103-post33-b-run.py ROOT win|wsl corpus
  -> t103-post26/27/28/29/30/31/32-b-new.py 및 t103-post9-b-corpus.py
python AUDIT/t103-post33-b-new.py ROOT OUTPUT.json
python AUDIT/t103-post33-b-new.py ROOT unused oracle
git diff --check 2375c8b 9ae2b6d
```

WSL 최초 helper는 Windows worktree의 `.git` 경로 형식을 Linux Git이 해석하지 못해 archive 진입 전에 실패했다. 제품 시험 결과로 세지 않았다. source object 저장소에서 정확한 후보 SHA만 읽는 `git archive`로 재실행했으며 source Git 설정을 바꾸지 않았다. 완료된 full/focused/static 검증은 원본 작성과 무관한 archive 사본만 사용했다. OS별 미실행은 아래 표에서 구분한다.

exact 후보 CI를 `gh run list --commit 9ae2b6de962bf42baea23e481e57e60be9c7bf47`, `gh run view 34205492927 --json headSha,status,conclusion,jobs`로 직접 확인했다. [run 34205492927](https://github.com/digitie/kor-travel-common/actions/runs/34205492927)은 후보 headSHA, PR/completed/success, 6개 job 및 source SHA 확인 step 모두 success다. 전체 job 로그는 NOT_RUN이다.

NOT_RUN: Windows Python 3.11(부재), 실제 소비자 build/type/e2e·manifest, npm/PyPI 설치·게시, workflow dispatch, MDX compiler/browser, WSL 독립 Markdown parser, WSL 별도 diff check, 이전 모든 개별 probe 전수 재실행. 규범·task·패키지·버전·CI·소비자 경계는 이번 delta에서 불변이므로 이전 확인을 동일성으로 재사용했다. T-103은 IN_PROGRESS이며 소비자 gate를 완료로 대신하지 않는다.

## 실행 결과와 종료 기록

| 검증 | Windows Python 3.14.3 | WSL Python 3.11.15 |
|---|---|---|
| 전체 unittest | 307개 실행, skip 0, 248.980초, exit 0 | 307개 수집/304개 실행, skip 3, 46.770초, exit 0 |
| contrast/UX 별도 focused | 실행 미완료, 원본 즉시 확정 요청으로 중단 | 69개, skip 0, 17.599초, exit 0 |
| aliases focused | NOT_RUN(별도 static 단계 미도달) | 35개 수집/34개 실행, skip 1, 0.185초, exit 0 |
| plan / links | 로컬 별도 gate NOT_RUN | 106 task 오류 0 / 490문서·2487대상 오류 0 |
| SPDX / secrets / redaction | 로컬 별도 gate NOT_RUN | 56파일 오류 0 / 각각 622파일 발견·예외 0 |
| versions self-check / aliases | 로컬 별도 gate NOT_RUN | exit 0(consumer NOT_RUN) / CSS 1 오류 0 |

WSL skip 3은 Windows 8.3 전용 1개와 선택 jsonschema 부재 2개이며 통과한 시험으로 세지 않았다. Windows 전체 시험은 완료했지만 standalone focused·static과 남은 직접 corpus는 parent의 원본 즉시 확정 지시로 중단했다. 이를 0건/통과로 표기하지 않는다. exact CI의 6개 job success와 로컬 미실행을 구분한다.

WSL 직접 corpus는 26/27/28/29/30/31/32 그룹과 초기 경계의 72/144/216/48/120/72/216/105행(993행), 새216행으로 총1,209관찰이다. 기존993행의 명시적 기대 불일치는 없고 새216행 중72개가 같은 줄 P8 누락이다. Windows 완료 수집 범위는 26/27/28/29 그룹480행과 새216행(총696행)이며, 대응 WSL 결과와 동일하다. Windows 30/31/32/초기 경계의 완전한 별도 결과 수집은 NOT_RUN(미완료/중단)이다. 새216개 같은 줄 반례는 양 OS 모두 완료했고 1/2자72개만 누락, 3/4자·정상 닫힘144개는 일치한다. 관찰 행 수를 중복 없는 테스트 수 또는 과거 corpus의 전수 검증으로 해석하지 않는다.

종료 결과 수집 KST `2026-09-08T17:49:17.5821064+09:00`. 제품 HEAD/tree는 명시한 후보와 동일하고 status는 자신의 새 원본 한 파일만 untracked였다. 제품 변경과 Git 설정 변경은 없으며 `.git/config` 종료 해시는 시작과 같다. raw 파일만 커밋한 뒤 clean·raw tree·파일/Git blob 동일 SHA-256을 완료 메시지로 전달한다.
