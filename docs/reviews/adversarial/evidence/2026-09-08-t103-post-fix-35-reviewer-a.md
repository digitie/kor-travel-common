# T-103 수정 후 35 A 독립 리뷰 원본

- 실행 ID: `T103-POST35-A-20260908-182055-KST`
- 최종 판정: **NO-GO**. 신규 P1 1건과 기존 P2 2건의 잔여 경계가 미해결이다. 신규 P0/P2/P3는 0건.
- 후보 commit: `aedfdd659255c27bcc4377bd15b39452c004417d`
- 후보 tree: `4bb189dddeab51d3cd0222d0ab50bef17a84ad99`
- 수정 비교 기준: `888fbbc2e943eab4198cf19a4dda6d88ce24b933`
- manifest: commit `ea60635`의 `2026-09-08-t103-post-fix-35-manifest.md`를 `git show`로 확인했다.
- 격리: `review-t103-post35-a` detached worktree. 시작과 제품 검토 종료의 HEAD/tree는 위 후보와 동일하며 `git status --short`는 모두 빈 출력이었다.
- 시작: 2026-09-08 18:20:55.740 KST. 제품 검토 종료: 2026-09-08 18:28:24.601 KST.
- post-34 원본과 상대 reviewer 결과는 열람하지 않았다. 후보·manifest·소비자·기존 evidence·Git 설정을 수정하지 않았다. 이 원본 한 파일만 별도 커밋한다.

## A-P1-31 — Markdown URL을 JavaScript 주석으로 오인하여 실행식을 누락한다

- 심각도 **P1**, disposition **OPEN · FIX_REQUIRED**.
- 위치: `tools/ux_lint.py` 516~520행의 delimiter 재개, 860~884행의 호출자, 901~906행의 줄 주석 전이.
- 최소 재현: 첫 행에 일반 prose, inline opener, 일반 HTTPS URL, P6/P8 대상 마크업·표현식을 순서대로 둔다. 다음 행에서 tilde fence를 열고 그 안에 동일 길이의 inline delimiter를 둔다. URL은 Markdown 일반 텍스트이며 JavaScript 주석이 아니다.
- 기대: 같은 행의 P6/P8을 보고하고 fail 모드 exit 1. 실제: URL의 두 slash에서 줄 주석 상태가 되어 뒤의 실행식을 가린다. 일반 CLI와 LF/CRLF/CR의 `--base` 모두 exit 0·finding 0이며 traceback은 없다.
- base 대조: 같은 최소 입력이 base에서는 P6/P8·exit 1, 후보에서는 exit 0이다. 이번 즉시 lexer 재개가 도입한 회귀다.
- 영향·권고: 신규 위반 gate가 실제 검사 대상을 누락한다. delimiter 뒤의 Markdown prose를 곧바로 JavaScript 문맥으로 해석하지 말고 prose·JSX·표현식의 경계를 구분해야 한다. URL을 금지하거나 주석 검사를 끄는 방식은 수용 기준을 만족하지 않는다.

## 기존 A-P2-29 — 아포스트로피 prose 뒤의 주석 오탐이 남는다

- 원 심각도 **P2**, disposition **PARTIAL · FIX_REQUIRED**.
- 위치: `tools/ux_lint.py` 802~839행, 특히 prose를 문자열로 취급하는 837~839행.
- 기본 주석 원 반례는 수정됐지만 opener 뒤의 일반 단어에 ASCII 아포스트로피가 있으면 이를 JavaScript 문자열 시작으로 처리한다. 이후 같은 행의 MDX block comment는 주석으로 가려지지 않는다.
- 최소 재현: 첫 행의 opener 뒤에 `don't` 같은 일반 단어, P6/P8 문자열이 들어 있는 MDX block comment를 두고 뒤 fence 안에 matching delimiter를 둔다. 기대는 exit 0·finding 0이나 실제는 P6/P8·exit 1이다. 일반 단어 대조와 정상 닫힌 span은 통과한다.
- base와 후보 모두 확장 입력에서 오탐했다. 기존 finding의 prose 경계가 남은 것으로 기록하며 원 ID·심각도를 유지한다. 실제 JavaScript 문자열과 Markdown 문장부호를 구분해야 한다.

## 기존 A-P2-30 — 닫힘 없는 span도 아포스트로피 뒤 주석 내부에서 재개한다

- 원 심각도 **P2**, disposition **PARTIAL · FIX_REQUIRED**.
- 위치: `tools/ux_lint.py` 524~547행의 사전 마스킹과 재개 후보 탐색.
- 기본 주석 내부 태그·중첩 식 반례 9개는 양 OS에서 수정됐다. 그러나 앞에 아포스트로피가 포함된 일반 단어를 두면 사전 마스킹에 사용한 JavaScript lexer가 주석을 문자열 내용으로 취급한다. 가려지지 않은 주석 내부의 태그·중괄호가 다시 실행 재개 후보가 된다.
- 닫힘 없는 1·2자 span, plain/blockquote/nested, LF/CRLF/CR의 추가 36개 직접 대조에서 일반 단어 18개는 통과했지만 아포스트로피 18개는 주석 내부 P6/P8을 오탐했다. 양 OS 결과가 같았다.
- 권고: 재개 후보를 고르기 전에 Markdown prose와 실제 JS 표현식 문맥을 보존해야 한다. 기본 최소 입력의 수정만으로 finding 전체가 닫힌 것으로 판단하지 않는다.

## 검증 범위와 결과

- **A-P1-28 FIXED 유지**: 원 반례와 대조 360개가 양 OS에서 기대 결과와 일치했다. 기존 같은 행·다음 행 실행식, 정상 닫힘, 4열/tab, plain/blockquote/nested, 1·2·3·4자 run, tilde/더 긴 backtick, LF/CRLF/CR와 `--base` 대조를 포함한다.
- 이전 주석·닫힘 없는 span·fence 전후의 기본 대조 504개도 양 OS에서 통과했다. 이후 prose를 추가한 새 324개 대조에서는 URL 뒤 실행식 누락 36개, 아포스트로피 뒤 주석 오탐 36개가 발생했고 나머지 252개는 일치했다. 닫힘 없는 prose 추가 36개는 위 A-P2-30에 별도 집계했다.
- 새 최소 `--base` 6개는 각 OS에서 LF/CRLF/CR의 URL 누락·아포스트로피 오탐을 재현했다. Windows에서 base 후보와도 직접 비교했다. 설치된 markdown-it-py 4.2.0 CommonMark 대조는 해당 첫 행을 일반 텍스트·HTML로 처리하며 `code_inline` 0개였다. 실제 MDX compiler 결과로 세지는 않는다.
- 독립 재현은 후보 밖의 기존 자기 fixture와 `t103-post35-prose-a.py`, `t103-post35-prose-base-a.py`, `t103-post35-unclosed-prose-a.py`로 실행했다. 제품 parser·새 시험 delta를 직접 읽었고 정본 문서의 동일성을 확인해 이전 문서 확인 범위를 재사용했다.
- Windows Python 3.14.3: 전체 unittest 310개 통과, skip 0, 285.040초. focused 72개 통과, 135.985초.
- WSL Python 3.11.15: 전체 310개 중 309개 통과, Windows 전용 8.3 API 시험 1개 skip, 102.198초. focused 72개 통과, 48.275초. skip은 통과로 집계하지 않았다.
- Windows 전체 명령: `python -B -X utf8 -m unittest discover -s tests -p "test_*.py" -v`. WSL 전체 명령: `uv run --no-project --python 3.11 --with jsonschema python -B -X utf8 -m unittest discover -s tests`. focused: 각 런타임의 `-m unittest tests.test_kt_contrast tests.test_ux_lint`.
- 양 OS 정적 검사 통과: 링크 496문서/2493대상, plan 106 task, SPDX 56파일, 비밀·redaction 각 628파일, registry 자체 검사, alias CSS 1개, 대비 27쌍, UX 예시 12 finding/report 모드 fail 0, 후보 delta의 `git diff --check`.
- 정확한 후보 CI run `34208926971`의 head SHA와 completed/success를 `gh run list --commit`으로 읽기 전용 확인했다. 이 성공은 미해결 finding을 닫는 근거가 아니다.
- NOT_RUN: Windows Python 3.11, CI 개별 job 로그 감사, 실제 소비자 빌드·e2e·manifest 검증, 실제 MDX compiler/browser 실행, npm/PyPI 설치·게시, workflow dispatch. 변경 없는 독립 역사 corpus 전체는 추가 재실행하지 않았으며 이번 full/focused 시험과 명시한 직접 대조만 이번 실행으로 집계했다.
- 원본 SHA-256과 보고서 전용 commit은 저장 후 계산하여 완료 메시지에 기록한다.
