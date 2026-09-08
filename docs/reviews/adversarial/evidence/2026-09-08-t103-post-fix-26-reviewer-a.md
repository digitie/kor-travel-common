# T-103 수정 후 독립 적대적 리뷰 26 — Reviewer A

## 판정·기준선·격리

- 실행 ID: `T103-POST26-A-20260908-152237-KST` (`reviewer_a`).
- 최종 verdict: **NO-GO**. 신규 P0 0개, P1 1개(`A-P1-23`), P2 0개, P3 0개. 직전 A-P1-21/A-P2-22 원 반례는 해결됐지만 유효한 closing을 거부하는 새 회귀가 있다.
- immutable 제품 candidate: `2a32dc7e07a4c36e2b0e92402f05019b31f6c3cb`, tree `a08e12fc66c67dfe65015f714a69c5fc0740a3f0`.
- delta base: `155941045a077529cb12f875cad5ab2b2f7639da`.
- manifest: commit `af9ffdce3e9edc107572b050576a6735f0c3bdb8`의 `docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-26-manifest.md`를 `git show`로 읽었다.
- detached worktree: `F:/dev/kor-travel-common-wt/review-t103-post26-a`.
- 시작 2026-09-08 15:22:37.008 KST, 제품 검토 종료 15:28:10.871 KST. 시작·종료 HEAD/tree가 위 candidate와 같고 `git status --porcelain=v1` 출력은 비어 있었다.
- 상대 post26 결과·raw와 이전 상대 원문을 읽거나 요청하지 않았다. 변경 목록의 상대 원본 이름만 확인했다. 후보·manifest·소비자·기존 evidence·Git config를 수정하지 않았다. 이 원본 한 파일만 report-only commit으로 추가한다.

## 요청 원문

> T-103 post-fix-26 독립 적대적 리뷰를 시작해 주세요. immutable 제품 후보는 commit `2a32dc7e07a4c36e2b0e92402f05019b31f6c3cb`, tree `a08e12fc66c67dfe65015f714a69c5fc0740a3f0`; 공통 manifest는 commit `af9ffdce3e9edc107572b050576a6735f0c3bdb8`의 `docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-26-manifest.md`입니다. 별도 detached worktree `F:/dev/kor-travel-common-wt/review-t103-post26-a`에서 candidate와 clean을 확인하세요. 전문 범위는 CommonMark blockquote/fence container 깊이·종료·nested literal, opener/closer post-marker 0~3열·4열/tab/space+tab, 빈 줄·새 quote block, CR/LF/CRLF, P6/P8와 누적 T-103 회귀입니다. 코드와 문서를 직접 확인하고 작성자 evidence를 맹신하지 마세요. 상대 reviewer의 post26 결과/raw를 읽거나 요청하지 말고, 제품·manifest·소비자·기존 evidence를 수정하지 마세요. 본인 원본 `docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-26-reviewer-a.md` 한 파일만 작성해 report-only commit으로 확정하세요. 실행 ID/시각/요청 원문/실제 SHA·tree·clean/명령/검증/NOT_RUN/각 finding disposition/verdict(PASS 또는 NO-GO)를 포함하고 commit hash와 SHA256을 부모에게 보내 주세요. 후보에 수정이 필요하면 먼저 NO-GO raw를 확정하고 작업을 멈추세요.

## 전체 delta와 정본 확인

전체 5파일 중 제품 변경은 `tools/ux_lint.py`·`tests/test_ux_lint.py` 2파일이다. 제품 전체 diff와 container 반환값·호출자의 masking 종료 경로를 읽었다. 나머지 3파일은 직전 manifest·A/B 원본 보존이며 상대 본문은 열지 않았다. AGENTS·문서 라우터·resume·T-103 task·standards·runbooks·versions·CI에 delta가 없음을 확인하여 동일 정본의 직전 검토를 재사용했다. 기존 반례와 정적 gate는 후보에서 새로 실행했다.

## A-P1-23 — 인용 padding을 콘텐츠 들여쓰기로 세어 유효한 fence를 거부한다

- 심각도: **P1**, disposition: **OPEN / 수정 필요**.
- 위치: `tools/ux_lint.py:264,270,305,615`. 마지막 `>` 바로 뒤의 전체 공백을 0열부터 계산한 값에 3열 상한을 적용한다. 인용 문법용 선택 공백과 콘텐츠 들여쓰기를 분리하지 않으며 tab의 실제 열 위치도 반영하지 않는다.
- 재현 명령: 후보 worktree에서 아래 내용을 `python -B -X utf8 -`로 실행한다. WSL에서는 `uv run --no-project --python 3.11 python -B -X utf8 -`로 동일 입력을 실행한다.

```python
from pathlib import Path
import json
import subprocess
import sys
import tempfile

tool = Path.cwd() / 'tools/ux_lint.py'
body = '> ~~~tsx\n> quoted\n>    ~~~\n> <div className="outline-none"/>\n> {window.confirm("x")}'
with tempfile.TemporaryDirectory() as directory:
    root = Path(directory)
    (root / 'case.mdx').write_bytes(body.encode('utf-8'))
    result = subprocess.run(
        [sys.executable, '-B', '-X', 'utf8', str(tool),
         '--root', str(root), '--fail-new', '--json'],
        cwd=root, capture_output=True, text=True,
    )
    print(result.returncode, json.loads(result.stdout))
```

- 세 번째 줄은 `>` 뒤 ASCII space가 정확히 4개다. 인용 marker의 선택 공백 1개를 제외한 콘텐츠 들여쓰기는 3열이므로 유효한 closing이다.
- 실제: 양 OS exit0, `status=PASS`, findings0, fail_count0.
- 기대: P6 line4·P8 line5, exit1. 정상 closing 뒤 실제 JSX/MDX 표현식은 검사해야 한다.
- 추가 확인: 해당 closing을 `>\t~~~` 또는 `> \t~~~`로 바꿔도 같은 false PASS다. 3가지 padding × backtick/tilde × LF/CRLF/CR의 **18개 closing 반례**가 양 OS에서 재현됐다. tilde opener도 같은 3가지 padding을 사용하면 정상 fence를 거부하고 내부 P6/P8을 보고하는 **9개 오탐**이 재현된다. 한 원인의 opener·closer 양 방향 증상으로 묶었다.
- 도입 경계: 동일 tilde 최소 입력에서 post25 제품은 P6 line4/P8 line5를 exit1로 검출했고 post26은 exit0이다. 이번 수정이 도입한 회귀다.
- 공식/독립 대조: [CommonMark0.31.2 §5.1](https://spec.commonmark.org/0.31.2/#block-quotes)의 인용 marker와 [§4.5](https://spec.commonmark.org/0.31.2/#fenced-code-blocks)의 콘텐츠 3열 상한을 구분해야 한다. 2026-09-08 공식 규격을 확인했다. Windows의 기존 `MarkdownIt('commonmark')`(markdown-it-py4.2.0)는 위 closing 뒤 P6이 fence에 포함되지 않는 것으로, 대응하는 유효 opener의 P6은 fence 내부로 판정했다.
- 시험의 문제: `tests/test_ux_lint.py:509`는 `">" + "    "`와 tab·space+tab을 모두 비닫힘으로 기대한다. 이 값은 이전 보고서의 `">" + "     "`(선택1+콘텐츠4)과 다르다. 현재 전체 시험 통과는 이 잘못된 기대값도 통과한 결과다.
- 영향: 실제 위반을 성공으로 표시하므로 신규 UX gate를 우회하며, 반대 방향에서는 정상 코드 예제를 실패시킨다.
- 최소 수정·수용 기준: 인용 marker가 소비하는 선택 padding만 제거하고 원본 열 위치·tab-stop을 보존하여 남은 콘텐츠의 들여쓰기를 계산한다. 유효 콘텐츠0~3열 opener/closer, 콘텐츠4열 비fence, tab/space+tab을 분리한다. 위 closing18개는 P6/P8·exit1, tilde opener9개는 발견0·exit0이어야 한다. 시험의 raw4/raw5 공백 기대값도 바로잡고 depth 감소·빈 줄·nested literal 회귀를 유지한다. 후보에는 수정하지 않았다.

## 직전 finding과 누적 disposition

A-P1-21의 깊이 감소·unquoted 빈 줄 12개는 양 OS에서 이제 P6/P8을 검출한다. A-P2-22의 선택1+콘텐츠4열 closing 6개는 정상적으로 body에 남아 오탐이 없어졌다. 다만 이전 42개 container 행렬의 유효 콘텐츠3열 대조 6개가 새로 실패했으며 A-P1-23에 포함했다. FIXED는 각 원 반례의 범위에 한정한다.

| ID | 원 심각도 | 이번 disposition |
|---|---|---|
| A-P1-01 | P1 | FIXED — CSS selector/specificity/media/comment-gap/미지원 오류 |
| A-P1-02 | P1 | FIXED — OKLCH chroma percent |
| A-P1-03 | P1 | FIXED — sRGB alpha 합성 |
| A-P1-04 | P1 | FIXED — baseline 신규 앞줄 독립 |
| A-P1-05 | P1 | FIXED — 외부 Git root 이름 충돌 |
| A-P2-06 | P2 | FIXED — 기존 MDX·Unicode/FEFF/async·인용·문단 corpus |
| A-P2-07 | P2 | FIXED — option 모양 base 거부 |
| A-P2-08 | P2 | FIXED(WSL) — quoted/tab 파일명; Windows tab 파일명 NOT_RUN |
| A-P2-09 | P2 | FIXED — JSON 숫자·중복 입력 경계 |
| A-P2-10 | P2 | FIXED — 오류·보고 출력 비공개 |
| A-P2-11 | P2 | FIXED — muted 읽기31쌍 |
| A-P3-12 | P3 | FIXED — geo8개·airport 현재/과거 수치 경계 |
| A-P1-13 | P1 | FIXED — 실제 `+++` 추가 소스행 |
| A-P2-14 | P2 | FIXED — self-symlink root 일반 입력 오류 |
| A-P2-15 | P2 | FIXED — 깊이2000 JSON 일반 입력 오류 |
| A-P1-16 | P1 | FIXED — 개행·가짜 hunk·Git 추가행 매핑 |
| A-P2-19 | P2 | FIXED — plain fence 들여쓰기/tab-stop |
| A-P1-20 | P1 | FIXED — backtick info·tilde 예외 |
| A-P1-21 | P1 | FIXED — 깊이 감소·빈 줄의 원 반례 |
| A-P2-22 | P2 | FIXED — 선택1+콘텐츠4열의 원 반례 |
| A-P1-23 | P1 | OPEN — padding과 콘텐츠 열 혼합 회귀 |

## 실제 검증과 참조 가정 정정

- Windows Python3.14.3, 전용 TEMP/TMP: `python -B -X utf8 -m unittest discover -s tests -p 'test_*.py' -v` — **298개 통과,skip0**,153.346초.
- WSL Python3.11.15, 전용 TMPDIR: `uv run --no-project --python 3.11 --with jsonschema python -B -X utf8 -m unittest discover -s tests` — **298개 실행,297개 통과,skip1**,56.207초. Windows8.3 API 전용 skip은 성공으로 집계하지 않았다.
- 양 OS `python -B -X utf8 -m unittest tests.test_kt_contrast tests.test_ux_lint` — **60개 통과**,Windows28.020초·WSL17.139초. WSL은 uv Python3.11을 사용했다.
- 외부 `t103-post17-reviewer-a-probe.py <candidate-root>` — Windows264/WSL263 출력 행(시험 개수 아님). 자신의 직전 label/값 대조 변경0.
- `t103-post19-margins-a.py`21개·`t103-post18-diff-a.py`10개·`t103-post19-mapping-a.py`15개: 양 OS 직전 출력과 전체 동일. 각각 candidate root를 인수로 지정했다.
- `t103-post21-boundary-a.py`44개·`t103-post22-fence-a.py`102개·`t103-post23-opener-a.py`120개·`t103-post24-info-a.py`84개: 양 OS 실패 목록 없음.
- `t103-post25-container-a.py`42개: 양 OS36개 기대 일치, 새 유효3열 closing 대조6개 불일치. 직전 18개 원 실패는 해결됐다.
- 새 `t103-post26-literal-a.py <candidate-root>`: 양 OS6개 모두 내부의 추가 `>`를 literal body로 보존하고 외부 P8만 검출했다.
- 새 `t103-post26-padding-a.py <candidate-root>`72개: 양 OS42개 초기 기대 일치, **27개 확정 오류**, 나머지3개는 아래 참조 가정 문제로 finding에 넣지 않았다. helper SHA256 `DCA3A5B853CB0352D642276AA815B14D4A0B99B74B0C3B326BB838CDB107A2BB`.
- 위3개는 콘텐츠4열 backtick opener의 LF/CRLF/CR 대조였다. 일반 CommonMark 파서는 indented code로 처리하지만 [MDX 공식 문서](https://mdxjs.com/docs/what-is-mdx/#markdown)는 indented code를 지원하지 않는다고 명시한다(문서 수정일2025-01-27, 확인일2026-09-08). Windows MarkdownIt에서 indented-code 규칙을 끈 대조는 해당 부분을 fence로 처리했다. 따라서 일반 CommonMark의 초기 기대값을 MDX 제품 실패의 증거로 사용하지 않았다. 이3개는 실제 MDX compiler 미실행 한계이며, 별도 P0~P3를 확정하지 않는다. A-P1-23의27개는 이 차이와 독립적인 유효0~3열 경계다.
- helper·로그는 source checkout `.git/codex-audit/`에만 보존했다. Windows는 `python -B -X utf8`, WSL은 `/mnt/f/` 경로와 `uv run --no-project --python 3.11 python -B -X utf8`로 같은 helper를 실행했다.

아래 정적 gate를 양 OS 후보에서 실행했다. WSL Git 기반 검사에는 프로세스 `GIT_DIR`·`GIT_WORK_TREE`만 해당 detached worktree로 지정했다.

```text
python -B -X utf8 tools/validate_document_links.py
python -B -X utf8 tools/validate_plan.py
python -B -X utf8 tools/check_spdx.py
python -B -X utf8 tools/scan_secrets.py --all
python -B -X utf8 tools/check_prod_redaction.py --all
python -B -X utf8 tools/check_versions.py --self-check
python -B -X utf8 tools/check_aliases.py packages/tokens/aliases
python -B -X utf8 tools/kt_contrast.py packages/tokens/tokens.css --json
python -B -X utf8 tools/ux_lint.py --root tests/fixtures/ux --json
git diff --check 155941045a077529cb12f875cad5ab2b2f7639da 2a32dc7e07a4c36e2b0e92402f05019b31f6c3cb
```

양 OS 링크469문서/2452대상·plan106 task·SPDX56파일·secret/redaction 각각601파일 오류0. registry 자체 검사·별칭CSS1개 통과·diff-check 출력 없음. canonical light27쌍 PASS·full/focused dark 전수 시험 통과. UX fixture report12건·fail_count0은 의도된 결과이며 위반0으로 집계하지 않았다.

`gh run list --commit 2a32dc7e07a4c36e2b0e92402f05019b31f6c3cb --json databaseId,headSha,status,conclusion,url --limit 5`로 [exact 후보 CI34194106207](https://github.com/digitie/kor-travel-common/actions/runs/34194106207)의 headSha 일치·completed/success를 읽기 전용 확인했다. 개별 job 로그는 재감사하지 않았다.

## NOT_RUN·종료

- Windows Python3.11: 실행 환경 없음. Windows3.14·WSL3.11 성공과 구분한다.
- 실제 MDX compiler/browser: 미실행. 공식 문서·기존 Windows Markdown 파서 대조와 제품 CLI 실행을 구분했다. 외부 파서 설치·제품 의존성 추가 없음.
- 소비자 build/type/e2e·채택 gate, npm/PyPI registry 설치·게시, workflow dispatch: 요청 범위 밖. 소비자 task와 T-010/T-502의 책임을 유지한다.
- 새 P1을 재현했으므로 후보 수정 없이 NO-GO 원본을 확정하여 종료한다. 수정된 새 후보에서 두 독립 리뷰가 필요하다.
