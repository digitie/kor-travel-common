# T-103 수정 후 34 A 독립 리뷰 원본

- 실행 ID: `T103-POST34-A-20260908-180116-KST`
- 최종 판정: **NO-GO**. 이번 새 보고 finding P0 0건, P1 0건, P2 2건, P3 0건.
- 후보 commit: `888fbbc2e943eab4198cf19a4dda6d88ce24b933`
- 후보 tree: `3c25a2e5495ca6c2a91a8fc1815fee2b784bcf9f`
- 수정 비교 기준: `9ae2b6de962bf42baea23e481e57e60be9c7bf47`
- manifest: commit `de0c3ef`의 `2026-09-08-t103-post-fix-34-manifest.md`를 `git show`로 확인했다.
- 격리: `review-t103-post34-a` detached worktree. 시작과 제품 검토 종료의 HEAD/tree는 위 후보와 동일하며 `git status --short`는 모두 빈 출력이었다.
- 시작: 2026-09-08 18:01:16.602 KST. 제품 검토 종료: 2026-09-08 18:06:49.334 KST.
- post-33 원본과 상대 reviewer 결과를 열람하지 않았다. 후보·manifest·소비자·기존 evidence·Git 설정은 수정하지 않았다. 이 원본 한 파일만 별도 커밋한다.

## A-P2-29 — inline opener 행을 보존한 뒤 주석 분석을 건너뛴다

- 심각도 **P2**, disposition **OPEN · FIX_REQUIRED**.
- 위치: `tools/ux_lint.py` 516~524행과 869~872행, 887~890행. 3·4자 run의 유사 경로는 687~725행과 859~862행이다.
- 최소 재현: 첫 행에 일반 prose, 1자 inline opener, P8 문자열만 들어 있는 MDX block comment를 둔다. 다음 행에서 tilde fence를 열고 그 안에 길이가 같은 inline delimiter를 둔다. 주석 안에는 실제 실행식이 없다.
- 기대: 주석을 제외하여 exit 0·finding 0. 실제: 같은 행 주석의 P8을 보고하며 exit 1이다. 주석을 다음 행으로 옮기거나 inline span을 정상 닫으면 exit 0이다.
- 원인: delimiter만 가린 segment를 반환한 뒤 호출자가 `index = stop`으로 행 끝까지 건너뛴다. 보존된 행의 주석은 lexer를 통과하지 않는다. 3·4자 경로도 같은 형태로 주석을 남긴다.
- base 대조: 1자 최소 입력은 base에서 exit 0, 후보에서 P8·exit 1이다. 이 경로는 이번 수정의 회귀다. 3·4자 경로의 같은 문제도 이번 독립 대조에서 확인했으며 동일 주석 분석 계약으로 묶었다.
- 영향·권고: 문서 주석이 신규 위반으로 오탐되어 gate를 막는다. delimiter 이후 같은 행의 실행식은 보존하면서 주석은 정상 lexer를 거쳐 제외해야 한다. 1·2·3·4자 run, container와 개행 대조를 함께 고정해야 한다.

## A-P2-30 — 닫힘 없는 span이 주석 내부에서 실행 검사를 재개한다

- 심각도 **P2**, disposition **OPEN · FIX_REQUIRED**.
- 위치: `tools/ux_lint.py` 527~547행, 특히 535~546행의 재개 후보 탐색.
- 최소 재현: 같은 opener 행의 MDX block comment 안에 P6 대상 태그 또는 중괄호로 감싼 P8 문자열을 둔다. 뒤에는 정상 fence와 일반 텍스트만 두며 inline delimiter는 닫지 않는다.
- 기대: 주석 및 fence 내용을 제외하여 exit 0·finding 0. 실제: 주석 내부 태그를 P6, 중괄호 내부 문자열을 P8로 보고하여 exit 1이다.
- 원인: 재개 후보를 찾는 정규식과 중괄호 탐색이 주석 내부의 위치도 선택한다. 선택한 위치 앞의 주석 opener를 가린 뒤 내부에서 lexer를 재개하므로 주석 문맥이 사라진다.
- base 대조: 위 두 최소 입력은 base와 후보에서 모두 오탐된다. 새로 도입된 회귀가 아니라 이번 닫힘 없는 span 수정이 남긴 기존 경계다.
- 영향·권고: 실행되지 않는 주석이 gate 위반으로 집계된다. fence로 탐색 범위를 제한하는 것과 함께 주석·문자열 문맥을 고려해 실제 실행 위치에서만 재개해야 한다. 주석 내부 태그·중첩 중괄호 음성 대조와 주석 밖 실행식 양성 대조를 분리해야 한다.

## 기존 finding과 직접 검증

- **A-P1-28 FIXED**: 원 반례와 대조 360개가 양 OS에서 모두 기대 결과와 일치했다. 같은 행·다음 행 P6/P8, 정상 닫힘, 4열/tab, plain/blockquote/nested, 1·2·3·4자 run, tilde/더 긴 backtick, LF/CRLF/CR를 포함한다. 기존 `--base` 3개도 양 OS에서 수정된 판정을 확인했다.
- 새 경계 대조는 각 OS 504개였다. fence 앞·안·뒤 실행식, 같은 행·다음 행 주석, 닫힘 없는 주석, 정상 닫힘을 비교했다. 같은 행 주석 72개와 닫힘 없는 같은 행 주석 72개가 오탐했고 나머지 360개는 기대 결과와 일치했다. 두 finding은 원인에 따라 구분했으며 이 144개를 중복 집계하지 않았다.
- 최소 `--base` 입력은 각 OS 9개였다. A-P2-29의 주석 문자열, A-P2-30의 주석 내부 태그·중첩 식 각각 LF/CRLF/CR에서 exit 1로 오탐했고 traceback은 없었다. Windows에서 base 후보와도 직접 비교했다.
- 독립 fixture는 후보 밖의 `t103-post33-opener-line-a.py`, `t103-post33-base-a.py`, `t103-post34-unclosed-a.py`, `t103-post34-comment-min-a.py`로 실행했다. 제품 parser와 새 시험의 전체 diff를 직접 읽었다. 정본 문서들은 직전 후보와 동일함을 확인해 이전 확인 범위를 재사용했다.

## 실행 결과와 NOT_RUN

- Windows Python 3.14.3: 전체 unittest 309개 통과, skip 0, 262.048초. focused 71개 통과, 115.645초.
- WSL Python 3.11.15: 전체 309개 중 308개 통과, Windows 전용 8.3 API 시험 1개 skip, 111.000초. focused 71개 통과, 50.482초. skip은 통과로 집계하지 않았다.
- Windows 전체 명령: `python -B -X utf8 -m unittest discover -s tests -p "test_*.py" -v`. WSL 전체 명령: `uv run --no-project --python 3.11 --with jsonschema python -B -X utf8 -m unittest discover -s tests`. focused: 각 런타임의 `-m unittest tests.test_kt_contrast tests.test_ux_lint`.
- 양 OS의 정적 검사 통과: 링크 493문서/2490대상, plan 106 task, SPDX 56파일, 비밀·redaction 각 625파일, registry 자체 검사, alias CSS 1개, 대비 27쌍, UX 예시 12 finding/report 모드 fail 0, 후보 delta의 `git diff --check`.
- 정확한 후보 CI run `34207168929`의 head SHA와 completed/success를 `gh run list --commit`으로 읽기 전용 확인했다. 새 finding의 해결 근거로 사용하지 않는다.
- Windows Python 3.11, CI 개별 job 로그 감사, 실제 소비자 빌드·e2e·manifest 검증, 실제 MDX compiler/browser 실행, npm/PyPI 설치·게시, workflow dispatch는 NOT_RUN이다. 변경 없는 독립 역사 corpus 전체는 추가 재실행하지 않았으며 이번 full/focused 시험과 명시한 직접 대조만 이번 실행으로 집계했다.
- 원본 SHA-256과 보고서 전용 commit은 저장 후 계산하여 완료 메시지에 기록한다.
