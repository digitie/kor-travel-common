# T-103 수정 후 33 A 독립 리뷰 원본

- 실행 ID: `T103-POST33-A-20260908-174304-KST`
- 최종 판정: **NO-GO**. 이번 새 보고 finding P0 0건, P1 1건, P2 0건, P3 0건.
- 후보 commit: `9ae2b6de962bf42baea23e481e57e60be9c7bf47`
- 후보 tree: `125095a9ad9af4979cec6e784bd2e781c69de662`
- 수정 비교 기준: `2375c8b052c94ec8982e0a4be294a747e75835b1`
- manifest: commit `77a94e4`의 `2026-09-08-t103-post-fix-33-manifest.md`를 `git show`로 확인했다.
- 격리: `review-t103-post33-a` detached worktree. 시작과 제품 검토 종료의 HEAD/tree는 위 후보와 동일하며 `git status --short`는 모두 빈 출력이었다.
- 시작: 2026-09-08 17:43:04.848 KST. 제품 검토 종료: 2026-09-08 17:49:19.746 KST.
- post-32 원본과 상대 reviewer 결과를 열람하지 않았다. 후보·manifest·소비자·기존 evidence·Git 설정은 수정하지 않았다. 이 원본 한 파일만 별도 커밋한다.

## A-P1-28 — 중간 fence 앞 inline opener와 같은 행의 검사 대상이 누락된다

- 심각도: **P1**. disposition: **OPEN · FIX_REQUIRED**.
- 위치: `tools/ux_lint.py` 510~519행, 862~866행, 880~884행.
- 최소 재현: 첫 행에 일반 prose와 1자 또는 2자 inline opener, 이어서 P6/P8 대상 마크업·표현식을 둔다. 다음 행에서 tilde 또는 더 긴 backtick block fence를 열고, 그 fence 안에 앞 inline opener와 길이가 같은 delimiter를 둔다. 해당 Markdown의 inline span은 block fence를 넘어 닫히지 않는다.
- 기대: opener와 같은 행의 P6/P8을 각각 보고하고 fail 모드에서 exit 1을 반환해야 한다.
- 실제: 새 `_mask_inline_opener_line`이 opener 이후 첫 행의 문자 전체를 공백으로 바꾼다. 일반 CLI는 exit 0·빈 finding JSON이며 traceback은 없다. LF/CRLF/CR의 `--base` 추가 행 검사도 각각 exit 0·finding 0·fail_count 0이다.
- 영향: 실제 검사 대상이 있어도 신규 위반 gate가 성공한다. 정상 인용 제외 계약과 실행 코드 검사 계약을 함께 충족하지 못한다.
- 원인 경계: base `2375c8b`에서도 동일한 첫 행 입력이 누락됐다. 이번 후보가 새로 도입한 회귀로 분류하지 않는다. post-33이 다음 행 검사는 복구했지만 같은 행을 닫지 못한 잔여 경계다.
- 최소 수정·수용 기준: block fence 때문에 유효 inline span이 아닌 경우 opener delimiter만 처리하고 같은 행의 실행 가능한 마크업·표현식은 계속 검사해야 한다. 1·2자 run과 plain/blockquote/nested, LF/CRLF/CR, 중간 tilde/더 긴 backtick, 일반 및 `--base` 모드에서 P6/P8을 보고해야 한다. 정상 닫힌 span과 4열/tab 대조는 계속 제외해야 한다.

## 독립 대조와 disposition

후보 parser와 새 시험의 전체 diff를 읽고 T-103의 백틱 인용 제외·실행 코드 검사·양 OS CLI 계약을 적용했다. AGENTS·문서 라우터·resume·T-103 task·UX 정본은 직전 후보와 동일함을 확인해 이전 정본 확인 범위를 재사용했다. 과거 raw를 요구사항으로 사용하지 않았다.

- 양 OS 각각 360개 직접 parser 대조: 1·2·3·4자 run × 3 container × 3 개행 × 2 fence × 같은 행/다음 행/정상 닫힘/4열/tab의 5개 문맥. 36개 실패, 324개 기대 결과 일치. 실패는 1자와 2자의 같은 행 문맥 각 18개뿐이다.
- CLI 양성·음성 대조 각 OS 3개: 같은 행은 잘못된 exit 0·finding 없음, 다음 행은 기대한 exit 1·P6/P8, 정상 닫힘은 기대한 exit 0·finding 없음이다.
- `--base` 각 OS 3개: LF/CRLF/CR 모두 같은 행의 신규 P6/P8이 누락됐다. Windows에서 base 후보도 같은 결과임을 직접 대조했다.
- Windows에 설치된 markdown-it-py 4.2.0의 CommonMark 모드로 최소 입력을 대조했다. inline 토큰은 일반 텍스트·HTML이며 `code_inline`은 0개다. 실제 MDX compiler의 실행 증거로 세지는 않는다.
- A-P2-27의 짧은 marker 반환 계약은 코드에서 `None` 경계를 유지하며 해당 checked-in 회귀가 통과했다. 기존 3·4자 중간 fence, 정상 닫힘·들여쓰기 경계도 이번 대조에서 유지됐다. 1·2자 중간 fence 수정의 disposition은 **PARTIAL**이며 잔여 위치와 영향은 A-P1-28에 모았다.
- 독립 재현은 후보 밖의 `t103-post33-opener-line-a.py`, `t103-post33-base-a.py`로 수행했다. 제품 코드나 소비자 파일을 수정하지 않았다.

## 실제 검증과 NOT_RUN

- Windows Python 3.14.3: 전체 unittest 307개 통과, skip 0, 295.695초. focused 69개 통과, 115.847초.
- WSL Python 3.11.15: 전체 307개 중 306개 통과, Windows 전용 8.3 API 시험 1개 skip, 105.400초. focused 69개 통과, 45.101초. skip은 통과로 집계하지 않았다.
- Windows 전체 명령: `python -B -X utf8 -m unittest discover -s tests -p "test_*.py" -v`. WSL 전체 명령: `uv run --no-project --python 3.11 --with jsonschema python -B -X utf8 -m unittest discover -s tests`. focused: 각 런타임의 `-m unittest tests.test_kt_contrast tests.test_ux_lint`.
- 양 OS의 정적 검사 통과: 링크 490문서/2487대상, plan 106 task, SPDX 56파일, 비밀·redaction 각 622파일, registry 자체 검사, alias CSS 1개, 대비 27쌍, UX 예시 12 finding/report 모드 fail 0, 후보 delta의 `git diff --check`.
- 정확한 후보 CI run `34205492927`의 head SHA와 completed/success를 `gh run list --commit`으로 읽기 전용 확인했다. 이 성공 상태는 새 finding의 해결 근거가 아니다.
- Windows Python 3.11, CI 개별 job 로그 감사, 실제 소비자 빌드·e2e·manifest 검증, 실제 MDX compiler/browser 실행, npm/PyPI 설치·게시, workflow dispatch는 NOT_RUN이다. 변경 없는 독립 역사 corpus 전체를 추가로 재실행하지 않았으며, 이번 full/focused 시험과 위 명시한 직접 대조를 이번 결과로 기록했다.
- 원본 SHA-256과 보고서 전용 commit은 저장 후 계산하여 완료 메시지에 기록한다.
