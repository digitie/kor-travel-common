# T-103 수정 후 독립 적대적 리뷰 23 — Reviewer A

## 기준선과 판정

- 실행 ID: `T103-POST23-A-20260908-143913-KST` (`reviewer_a`).
- 최종 verdict: **NO-GO**. 신규 P0 0개, P1 1개(`A-P1-20`), P2 0개, P3 0개. 직전 `A-P2-19`는 FIXED다.
- 제품 candidate: `3a8b569889fcaf4429cc70a7bafec779181aac6f`, tree `f72134340a7da31e3ad756bcbde215342fef80fc`.
- delta base: `61f1cc6a900e25268e0c5eadc32ce1c5ccc9d3f3`.
- 공통 manifest: commit `b68c07be7e1fec924ee85e5a1f7c155cb276c17b`의 `docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-23-manifest.md`를 `git show`로 읽었다.
- 격리: `F:/dev/kor-travel-common-wt/review-t103-post23-a` detached worktree. 시작 2026-09-08 14:39:13.523 KST, 제품 검토 종료 14:43:31.384 KST. 시작·종료 HEAD/tree가 위 후보와 일치하고 `git status --porcelain=v1` 출력이 비어 있었다.
- 상대 reviewer의 결과·raw를 읽거나 요청하지 않았다. 변경 파일 목록에 있는 상대 원본의 이름만 확인했고 본문은 열지 않았다. 제품·manifest·소비자·기존 evidence·source git config는 수정하지 않았다. 이 원본 한 파일만 report-only commit으로 확정한다.

## 요청 원문

> T-103 post-fix-23 독립 적대적 리뷰를 시작해 주세요. immutable 제품 후보는 commit `3a8b569889fcaf4429cc70a7bafec779181aac6f`, tree `f72134340a7da31e3ad756bcbde215342fef80fc`; 공통 manifest는 commit `b68c07be7e1fec924ee85e5a1f7c155cb276c17b`의 `docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-23-manifest.md`입니다. 별도 detached worktree `F:/dev/kor-travel-common-wt/review-t103-post23-a`에서 candidate와 clean을 확인하세요. 전문 범위는 CommonMark fenced block 선행 indentation 0/1/2/3/4 spaces, tab/space+tab 열 확장, backtick/tilde, suffix ASCII/LS/PS, CR/LF/CRLF와 MDX inline·JSX·ESM·Unicode 경계 및 기존 T-103 finding 회귀입니다. 최소 반례와 전체 변경을 코드/문서로 다시 확인하고 작성자 evidence를 맹신하지 마세요. 상대 reviewer 결과·raw는 읽거나 요청하지 말고, 제품·manifest·소비자·기존 evidence를 수정하지 마세요. 본인 원본 `docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-23-reviewer-a.md` 한 파일만 작성해 report-only commit으로 확정하세요. 실행 ID/시각/요청 원문/실제 SHA·tree·clean/명령/검증/NOT_RUN/각 finding disposition/verdict(PASS 또는 NO-GO)를 포함하고 commit hash와 SHA256을 부모에게 보내 주세요. 후보에 수정이 필요하면 먼저 NO-GO로 원본을 확정하고 작업을 멈추세요.

## 검토 범위

전체 delta는 7파일이며 제품 수정은 `tools/ux_lint.py`와 `tests/test_ux_lint.py` 2파일이다. 나머지 5개는 이전 manifest와 A/B 원본 보존이다. 상대 본문 미열람 원칙에 따라 기록 파일은 목록·차이 범위만 확인했다. 새 `_markdown_indent_columns`와 열기·닫기 분기, 새 회귀 시험의 전체 diff를 읽었다. AGENTS·문서 라우터·resume을 확인했고, T-103 task·standards·runbook·versions·CI의 delta가 없음을 확인하여 직전 정본 검토를 재사용했다. 누적 직접 반례는 모두 새 후보에서 다시 실행했다.

## 신규 finding

### A-P1-20 — backtick이 있는 info 문자열을 검증하지 않아 정상 inline span 뒤 실행식을 전부 누락한다

- 심각도: **P1**, disposition: **OPEN / 수정 필요**.
- 위치: `tools/ux_lint.py`의 `_mask_mdx_fence`, 523~531행의 opener 판정. marker 길이·선행 들여쓰기만 확인하고 backtick fence의 info 문자열에 backtick이 포함되는지 검사하지 않는다.
- 최소 입력: 첫 줄은 3자 backtick으로 닫힌 정상 code span이고, 빈 줄 뒤 MDX 표현식은 실행 대상이다.

```python
body = '```a`b```\n\n{window.confirm("x")}\n'
```

- 재현: 아래 내용을 후보 worktree에서 `python -B -X utf8 -`로 실행한다. WSL은 `uv run --no-project --python 3.11 python -B -X utf8 -`로 동일 입력을 실행한다. 임시 디렉터리만 쓴다.

```python
from pathlib import Path
import subprocess
import sys
import tempfile

tool = Path.cwd() / 'tools/ux_lint.py'
body = '```a`b```\n\n{window.confirm("x")}\n'
with tempfile.TemporaryDirectory() as directory:
    root = Path(directory)
    (root / 'case.mdx').write_bytes(body.encode('utf-8'))
    result = subprocess.run(
        [sys.executable, '-B', '-X', 'utf8', str(tool),
         '--root', str(root), '--fail-new', '--json'],
        cwd=root, capture_output=True, text=True,
    )
    print(result.returncode, result.stdout)
```

- 실제: Windows 3.14와 WSL 3.11 모두 exit 0, `status=PASS`, `findings=[]`, `fail_count=0`.
- 기대: `P8` 1건, LF/CRLF 입력은 line 3, `--fail-new` exit 1. 첫 줄의 인용만 제외하고 다음 문단의 실행식을 계속 검사해야 한다.
- 근거: [CommonMark 0.31.2 §4.5](https://spec.commonmark.org/0.31.2/#fenced-code-blocks)는 backtick fence의 info 문자열에 backtick을 허용하지 않는다. 2026-09-08 공식 원문을 확인했다. 기존 Windows `markdown-it-py 4.2.0`의 `MarkdownIt('commonmark').parse(body)`는 첫 문단에 ``code_inline(content='a`b')``, 두 번째 문단에 `{window.confirm("x")}`를 반환한다. fence 토큰은 없다.
- 확장 재현: 3·4자 delimiter × LF/CRLF/CR의 6개 모두 동일한 false PASS. 같은 실행식을 포함한 실제 열린/닫힌 fence 대조 및 0~3열 정상 opener/closer는 기대대로 동작한다.
- 원인·도입 경계: 직전 post22 제품에 같은 최소 입력을 실행해 동일한 exit 0을 확인했다. 이번 들여쓰기 수정이 새로 도입한 회귀는 아니며, 새 후보의 opener 경계를 공격하여 발견한 잔여 누락이다.
- 영향: 문서 인용 뒤의 실제 MDX 위반을 EOF까지 가릴 수 있어 신규 위반 gate를 우회한다. 단순 report 오탐이 아니라 실패해야 할 입력을 성공으로 표시하므로 P1이다.
- 최소 수정 방향·수용 기준: backtick opener의 나머지 info 문자열에 backtick이 있으면 fence로 인정하지 않고 inline 처리로 돌린다. tilde info 문자열에는 같은 제한을 적용하지 않는다. 위 6개는 P8/exit 1, 실제 fence와 정상 닫힌 code span 음성 대조는 계속 제외되어야 한다. 제품 후보에는 수정하지 않았다.

## 기존 finding disposition

FIXED는 각 ID의 실제 재현 corpus에 대한 판정이다. 새 opener 누락은 `A-P1-20`으로 분리한다.

| ID | 원 심각도 | 이번 disposition·근거 |
|---|---|---|
| A-P1-01 | P1 | FIXED. CSS selector/specificity/조건 교집합/주석 gap/미지원·빈 목록 오류 유지 |
| A-P1-02 | P1 | FIXED. OKLCH chroma 25%와 0.1 일치 |
| A-P1-03 | P1 | FIXED. sRGB alpha 흰색20%/검정 대비 1.6620953314177012 유지 |
| A-P1-04 | P1 | FIXED. 새 앞줄 위반이 기존 baseline 예산을 소비하지 않음 |
| A-P1-05 | P1 | FIXED. 외부 Git root basename 충돌 대조 유지 |
| A-P2-06 | P2 | FIXED. 기존 MDX 실행식·Unicode·인용·주석·1/2/3자 span·문단 corpus 유지 |
| A-P2-07 | P2 | FIXED. option 모양 base 일반 입력 오류 |
| A-P2-08 | P2 | FIXED(WSL). quoted/tab 파일명 추가행 검출; Windows tab 파일명 NOT_RUN |
| A-P2-09 | P2 | FIXED. NaN/Infinity/음수/bool/중복·거대 숫자 JSON 거부 |
| A-P2-10 | P2 | FIXED. JSON/Markdown/annotation/summary/argparse 오류 비공개 |
| A-P2-11 | P2 | FIXED. muted 읽기 선언 31쌍·text-tertiary 미달 검출 |
| A-P3-12 | P3 | FIXED. geo 미달 8개·airport 현재 sRGB 1.320934와 과거 조사1.15 경계 유지 |
| A-P1-13 | P1 | FIXED. 실제 `+++` 소스 추가행 검출 |
| A-P2-14 | P2 | FIXED. 양 OS self-symlink root exit 2, traceback 없음 |
| A-P2-15 | P2 | FIXED. 깊이2000 JSON 양 도구 일반 입력 오류 |
| A-P1-16 | P1 | FIXED. CR/CRLF/LF/LS/PS 가짜 hunk·추가행 매핑 유지 |
| A-P2-19 | P2 | FIXED. 직전 102개 fence 행렬 전체 기대 일치, 4 space/tab/space+tab의 조기 닫힘 18개 해결 |

## 실행한 검증

- Windows Python 3.14.3, 전용 프로세스 TEMP/TMP: `python -B -X utf8 -m unittest discover -s tests -p 'test_*.py' -v` — **293개 통과, skip 0**, 148.948초.
- WSL Python 3.11.15, 전용 TMPDIR: `uv run --no-project --python 3.11 --with jsonschema python -B -X utf8 -m unittest discover -s tests` — **293개 실행, 292개 통과, skip 1**, 85.562초. Windows 8.3 API 전용 skip은 성공 개수에서 제외했다.
- `python -B -X utf8 -m unittest tests.test_kt_contrast tests.test_ux_lint` — Windows **55개 통과**, 16.318초; WSL uv Python 3.11로 **55개 통과**, 13.690초.
- 양 OS에서 `.git/codex-audit/t103-post17-reviewer-a-probe.py <candidate-root>` 실행: Windows 264개·WSL 263개 출력 행(시험 건수 아님). 자신의 직전 실행 로그와 label/값 전체 대조 변경 0. CSS·수학·JSON·redaction·symlink·MDX Unicode/FEFF/async·주석 반례가 그대로 기대대로 동작한다.
- 양 OS `t103-post19-margins-a.py <candidate-root>` 21개, `t103-post18-diff-a.py <candidate-root>` 10개, `t103-post19-mapping-a.py <candidate-root>` 15개, `t103-post21-boundary-a.py <candidate-root>` 44개: 기존 기대 결과 유지, 마지막 helper `FAILURES []`.
- 양 OS `t103-post22-fence-a.py <candidate-root>`: 102개, `failures=[]`. LF/CRLF/CR × backtick/tilde와 선행·접미사의 ASCII space/tab·LS/PS를 대조했다.
- 양 OS 새 `t103-post23-opener-a.py <candidate-root>`: 120개 중 114개 기대 일치, 위 신규 6개 false PASS. 0/1/2/3열 opener × 0/1/2/3열 closer × 두 marker × 세 개행의 96개와 4 space/tab/space+tab 비opener 18개는 통과했다. helper SHA256 `65AD5E6E495E9D5D5877E36BA311FDFDE198F8A541B6D405D266C845527C33EE`.
- 재현 helper·로그는 source checkout의 `.git/codex-audit/`에만 두었다. 후보의 제품 파일에는 쓰지 않았다. WSL helper는 `/mnt/f/` 경로와 `uv run --no-project --python 3.11 python -B -X utf8`로 실행했다.

아래 정적 명령을 양 OS에서 실행했다. WSL은 uv Python 3.11을 사용하고 Git 기반 검사에 한해 프로세스 `GIT_DIR`와 `GIT_WORK_TREE`를 해당 detached worktree로 지정했다. Git config는 바꾸지 않았다.

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
git diff --check 61f1cc6a900e25268e0c5eadc32ce1c5ccc9d3f3 3a8b569889fcaf4429cc70a7bafec779181aac6f
```

양 OS 링크 460문서/2435대상·plan106 task·SPDX56파일·secret/redaction 각각592파일 오류0, registry 자체 검사·별칭CSS1개 통과, diff-check 출력 없음. canonical light 대비27쌍 PASS, full/focused의 dark 전수 시험 통과. UX fixture는 의도된 report12건과 fail_count0이며 위반0으로 세지 않았다.

읽기 전용 `gh run list --commit 3a8b569889fcaf4429cc70a7bafec779181aac6f --json databaseId,headSha,status,conclusion,url --limit 5`: [정확한 후보 CI 34191169944](https://github.com/digitie/kor-travel-common/actions/runs/34191169944), headSha 일치·completed/success. 개별 job 로그의 재감사는 실행하지 않았다.

## NOT_RUN과 종료

- Windows Python 3.11: 실행 환경 없음. Windows3.14·WSL3.11 성공과 구분한다.
- 실제 MDX compiler/browser: 미실행. 이번 Markdown 경계는 공식 CommonMark0.31.2와 기존 Windows Markdown 파서로 대조했다. 제품 의존성 추가·외부 파서 설치 없음.
- 소비자 build/type/e2e·채택 gate, npm/PyPI registry 설치·게시, workflow dispatch: 요청 범위 밖. 소비자 이관 task와 T-010/T-502의 책임을 유지한다.
- 신규 P1을 재현했으므로 제품 수정 없이 이 원본을 확정하고 검토를 종료한다. 수정한 새 immutable 후보에서 두 독립 reviewer가 다시 확인해야 한다.
