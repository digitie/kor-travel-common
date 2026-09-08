# T-103 수정 후 독립 적대적 리뷰 25 — Reviewer A

## 판정·기준선·격리

- 실행 ID: `T103-POST25-A-20260908-150730-KST` (`reviewer_a`).
- 최종 verdict: **NO-GO**. 신규 P0 0개, P1 1개(`A-P1-21`), P2 1개(`A-P2-22`), P3 0개. 기존 A 18개 반례는 해당 범위에서 FIXED를 유지한다.
- immutable 제품 candidate: `155941045a077529cb12f875cad5ab2b2f7639da`, tree `4fb87fcc870402df48ac3f336f5f9c2a6ede7767`.
- delta base: `535beecaeaf06296df3c8c1e108c1b86564e48d7`.
- manifest: commit `0e3238ce37e496ec5e88773ffc5e4add90b6dab0`의 `docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-25-manifest.md`를 `git show`로 읽었다.
- 별도 detached worktree: `F:/dev/kor-travel-common-wt/review-t103-post25-a`.
- 시작 2026-09-08 15:07:30.337 KST, 제품 검토 종료 15:11:57.404 KST. 시작·종료 HEAD/tree가 위 후보와 같고 `git status --porcelain=v1` 출력은 비어 있었다.
- 상대 post25 결과·raw나 이전 상대 원문을 읽거나 요청하지 않았다. 변경 파일 목록의 상대 원본 이름만 보았다. 후보·manifest·소비자·기존 evidence·Git config를 수정하지 않았다. 이 원본 한 파일만 report-only commit으로 추가한다.

## 요청 원문

> T-103 post-fix-25 독립 적대적 리뷰를 시작해 주세요. immutable 제품 후보는 commit `155941045a077529cb12f875cad5ab2b2f7639da`, tree `4fb87fcc870402df48ac3f336f5f9c2a6ede7767`; 공통 manifest는 commit `0e3238ce37e496ec5e88773ffc5e4add90b6dab0`의 `docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-25-manifest.md`입니다. 별도 detached worktree `F:/dev/kor-travel-common-wt/review-t103-post25-a`에서 candidate와 clean을 확인하세요. 전문 범위는 CommonMark blockquote/fence 컨테이너와 nested `>` 깊이, 빈 quoted 행, plain/CR/LF/CRLF, 0~3열·4열/tab, suffix, 인용 블록 밖 P6/P8, 누적 T-103 finding 회귀입니다. 코드와 문서를 직접 확인하고 작성자 evidence를 맹신하지 마세요. 상대 reviewer의 post25 결과/raw를 읽거나 요청하지 말고, 제품·manifest·소비자·기존 evidence를 수정하지 마세요. 본인 원본 `docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-25-reviewer-a.md` 한 파일만 작성해 report-only commit으로 확정하세요. 실행 ID/시각/요청 원문/실제 SHA·tree·clean/명령/검증/NOT_RUN/각 finding disposition/verdict(PASS 또는 NO-GO)를 포함하고 commit hash와 SHA256을 부모에게 보내 주세요. 후보에 수정이 필요하면 먼저 NO-GO raw를 확정하고 작업을 멈추세요.

## 전체 delta와 검토 범위

전체 5파일 중 제품 변경은 `tools/ux_lint.py`와 `tests/test_ux_lint.py` 2파일이다. 두 제품 파일의 전체 diff, `_markdown_fence_container`·`_markdown_fence_candidate`와 호출자의 container 종료 분기를 직접 읽었다. 나머지 3파일은 직전 manifest·A/B 원본 보존이며 상대 본문은 열지 않았다. AGENTS·문서 라우터·resume·T-103 task·standards·runbooks·versions·CI에 delta가 없음을 확인하여 동일 정본의 직전 검토를 재사용했다. 누적 반례와 정적 gate는 새 후보에 실제로 다시 실행했다.

## 신규 finding과 공통 재현

다음 스크립트를 후보 worktree에서 `python -B -X utf8 -`로 실행하면 세 최소 입력을 각각 독립 임시 파일에 넣는다. WSL은 `uv run --no-project --python 3.11 python -B -X utf8 -`로 동일 내용을 실행한다.

```python
from pathlib import Path
import json
import subprocess
import sys
import tempfile

tool = Path.cwd() / 'tools/ux_lint.py'
cases = {
    'shallower': '> > ~~~tsx\n> > quoted\n> <div className="outline-none"/>\n> {window.confirm("x")}',
    'blank': '> ~~~tsx\n> quoted\n\n> <div className="outline-none"/>\n> {window.confirm("x")}',
    'indent': '> ~~~tsx\n> quoted\n>     ~~~\n> <div className="outline-none"/>\n> ~~~',
}
for label, body in cases.items():
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        (root / 'case.mdx').write_bytes(body.encode('utf-8'))
        result = subprocess.run(
            [sys.executable, '-B', '-X', 'utf8', str(tool),
             '--root', str(root), '--fail-new', '--json'],
            cwd=root, capture_output=True, text=True,
        )
        payload = json.loads(result.stdout)
        print(label, result.returncode,
              [(item['line'], item['pattern']) for item in payload['findings']])
```

### A-P1-21 — 인용 컨테이너 종료를 놓쳐 뒤의 실제 P6/P8을 가린다

- 심각도: **P1**, disposition: **OPEN / 수정 필요**.
- 위치: `tools/ux_lint.py:594-602`. `_markdown_fence_candidate`가 None을 반환한 뒤 `non_space`가 있고 `>`로 시작하지 않을 때만 종료한다. 깊이가 줄어든 인용 줄과 인용 marker가 없는 빈 줄을 종료로 처리하지 않는다.
- `shallower` 실제: 양 OS exit 0, findings 없음. 기대: 내부 2단계 fence는 1단계 인용으로 돌아가는 줄에서 끝나고 P6 line3·P8 line4, exit1이어야 한다.
- `blank` 실제: 양 OS exit 0, findings 없음. 기대: 인용 marker가 없는 빈 줄에서 첫 인용 블록이 끝나고 다음 인용 블록의 P6 line4·P8 line5, exit1이어야 한다.
- 확장: 두 종료 유형 × tilde/backtick × LF/CRLF/CR의 12개가 동일한 false PASS였다. 같은 깊이의 정상 닫힘과 실제 인용 marker가 있는 빈 줄, 인용 접두사 없는 비공백 줄의 양성·음성 대조는 정상이다.
- 도입 경계: 직전 post24 제품에 같은 tilde 최소 입력을 실행하면 `shallower`는 P6 line3/P8 line4, `blank`는 P6 line4/P8 line5를 exit1로 검출한다. **이번 수정에서 발생한 실제 회귀**다.
- 근거: [CommonMark0.31.2 §5.1](https://spec.commonmark.org/0.31.2/#block-quotes)은 marker 없는 빈 줄로 인용 블록이 분리되는 경계를 규정하고, [§4.5](https://spec.commonmark.org/0.31.2/#fenced-code-blocks)는 포함 컨테이너가 끝나면 미종결 fence도 끝나는 규칙을 둔다. 2026-09-08 공식 원문을 조회했다. Windows의 기존 `markdown-it-py4.2.0`, `MarkdownIt('commonmark').parse(body)`에서 `shallower`의 내부 fence와 내부 인용이 P6 이전에 닫히고, `blank`는 두 독립 인용 블록으로 나뉘는 것을 확인했다.
- 영향: 실제 앱 마크업·MDX 실행식을 EOF까지 가려 신규 위반 gate가 잘못 통과한다.
- 최소 수정·수용 기준: fence가 속한 인용 깊이의 지속 여부를 별도로 판정하고, marker 없는 빈 줄과 상위 깊이로 복귀하는 줄에서 해당 fence masking을 끝낸다. 현재 줄부터 일반 lexer가 재개되어야 한다. 위 12개는 P6/P8·exit1, 정상 깊이·quoted 빈 줄·fence 내부 인용은 계속 제외해야 한다.

### A-P2-22 — 인용 marker 뒤의 실제 들여쓰기 폭을 버려 4열 닫힘을 허용한다

- 심각도: **P2**, disposition: **OPEN / 수정 필요**.
- 위치: `tools/ux_lint.py:288-294`. 각 `>` 뒤의 space/tab을 전부 소비한 뒤 나머지를 반환하므로 인용 문법의 padding과 fence의 콘텐츠 들여쓰기를 구분하지 않는다.
- `indent`의 세 번째 줄은 `>` 뒤 ASCII space 5개다. 인용 padding 한 칸을 제외해도 콘텐츠에 4칸이 남으므로 유효한 closing fence가 아니다.
- 실제: 양 OS P6 line4·exit1. 기대: 마지막 정상 closing까지 코드 예제 내부이므로 findings0·exit0.
- 확장: tilde/backtick × LF/CRLF/CR의 6개 모두 같은 오탐. 콘텐츠 3칸의 유효한 closing 대조는 P6을 정상 검출한다.
- 도입 경계: 직전 post24 제품도 같은 최소 입력에 P6을 보고한다. 기존 quoted-fence 지원 누락에서 남은 경계로 분류한다. A-P2-19의 plain fence 수정은 유지되지만 새 quoted 경로에는 동일한 열 상한이 적용되지 않아 새 ID로 분리했다.
- 독립 대조: Windows `MarkdownIt('commonmark').parse(body)`는 fence 내용에 `    ~~~`와 다음 JSX를 포함한다. CommonMark3열 상한을 quoted 콘텐츠에서도 유지해야 한다.
- 영향: 정상 코드 예제를 제품 마크업으로 보고하여 report 오탐·신규 fail 차단을 유발한다.
- 최소 수정·수용 기준: 각 인용 marker의 허용 padding만 제거하고 남은 콘텐츠의 시각적 열 수를 보존한다. 0~3열/4열과 tab-stop 규칙을 그 결과에 적용한다. 위 6개는 발견0·exit0, 유효한 closing 뒤 실제 JSX는 P6을 유지해야 한다. 후보에는 수정하지 않았다.

## 누적 finding disposition

기존 FIXED는 각 ID의 이미 실행한 반례 범위이며 신규 quoted 경계 2개를 제외한다.

| ID | 원 심각도 | 이번 disposition |
|---|---|---|
| A-P1-01 | P1 | FIXED — CSS selector/specificity/media/comment-gap/미지원 오류 |
| A-P1-02 | P1 | FIXED — OKLCH chroma percent 변환 |
| A-P1-03 | P1 | FIXED — sRGB alpha 합성 |
| A-P1-04 | P1 | FIXED — 신규 앞줄의 baseline 예산 독립 |
| A-P1-05 | P1 | FIXED — 외부 Git root 이름 충돌 |
| A-P2-06 | P2 | FIXED — 기존 MDX 실행식·인용·Unicode/FEFF/async·문단 corpus |
| A-P2-07 | P2 | FIXED — option 모양 base 거부 |
| A-P2-08 | P2 | FIXED(WSL) — quoted/tab 파일명; Windows tab 파일명 NOT_RUN |
| A-P2-09 | P2 | FIXED — NaN/Infinity/음수/bool/중복·거대 숫자 JSON |
| A-P2-10 | P2 | FIXED — 모든 오류·보고 출력 비공개 |
| A-P2-11 | P2 | FIXED — muted 읽기 선언31쌍·미달 검출 |
| A-P3-12 | P3 | FIXED — geo8개, airport 현재1.320934/과거1.15 경계 |
| A-P1-13 | P1 | FIXED — 실제 `+++` 추가 소스행 |
| A-P2-14 | P2 | FIXED — 양 OS self-symlink root 일반 입력 오류 |
| A-P2-15 | P2 | FIXED — 깊이2000 JSON 일반 입력 오류 |
| A-P1-16 | P1 | FIXED — 실제 개행·가짜 hunk·Git 추가행 매핑 |
| A-P2-19 | P2 | FIXED — plain fence 들여쓰기/tab-stop102개 |
| A-P1-20 | P1 | FIXED — backtick info·tilde 예외·후속 P8 |
| A-P1-21 | P1 | OPEN — 인용 컨테이너 종료 누락 회귀 |
| A-P2-22 | P2 | OPEN — 인용 콘텐츠의4열 closing 오탐 |

## 실행한 검증·관찰

- Windows Python3.14.3, 전용 프로세스 TEMP/TMP: `python -B -X utf8 -m unittest discover -s tests -p 'test_*.py' -v` — **297개 통과, skip0**,142.997초.
- WSL Python3.11.15, 전용 TMPDIR: `uv run --no-project --python 3.11 --with jsonschema python -B -X utf8 -m unittest discover -s tests` — **297개 실행,296개 통과,skip1**,79.517초. Windows8.3 API 전용 skip은 성공으로 집계하지 않았다.
- 양 OS `python -B -X utf8 -m unittest tests.test_kt_contrast tests.test_ux_lint` — **59개 통과**,Windows24.087초·WSL15.332초. WSL은 uv Python3.11을 사용했다.
- 양 OS 외부 helper `t103-post17-reviewer-a-probe.py <candidate-root>` — Windows264/WSL263 출력 행(시험 개수 아님), 자신의 직전 label/값 전체 대조 변경0.
- `t103-post19-margins-a.py <candidate-root>`21개, `t103-post18-diff-a.py <candidate-root>`10개, `t103-post19-mapping-a.py <candidate-root>`15개: 양 OS 직전 기대 결과와 전체 동일.
- `t103-post21-boundary-a.py <candidate-root>`44개, `t103-post22-fence-a.py <candidate-root>`102개, `t103-post23-opener-a.py <candidate-root>`120개, `t103-post24-info-a.py <candidate-root>`84개: 양 OS 실패 목록 없음.
- 새 `t103-post25-container-a.py <candidate-root>`42개: 양 OS24개 기대 일치,18개 불일치(P1 반례12개·P2 반례6개). helper SHA256 `C369089E3A2B924104E3EF300B5A235E72BDD44717773C39ED6CF15AB57C43A9`. 깊이1·2 정상 quoted fence·빈 quoted 행·인용 밖 P6/P8·컨테이너 감소/빈줄·quoted3/4열을 포함한다.
- helper·로그는 source checkout의 `.git/codex-audit/`에만 보존했다. Windows는 `python -B -X utf8`, WSL은 `/mnt/f/` 경로와 `uv run --no-project --python 3.11 python -B -X utf8`로 동일 helper를 실행했다.

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
git diff --check 535beecaeaf06296df3c8c1e108c1b86564e48d7 155941045a077529cb12f875cad5ab2b2f7639da
```

양 OS 링크466문서/2446대상·plan106 task·SPDX56파일·secret/redaction 각각598파일 오류0. registry 자체 검사·별칭CSS1개 통과·diff-check 출력 없음. canonical light27쌍 PASS·full/focused dark 전수 시험 통과. UX fixture는 의도된 report12건·fail_count0이며 위반0으로 집계하지 않았다.

`gh run list --commit 155941045a077529cb12f875cad5ab2b2f7639da --json databaseId,headSha,status,conclusion,url --limit 5`로 [exact 후보 CI34193097617](https://github.com/digitie/kor-travel-common/actions/runs/34193097617)의 headSha 일치·completed/success를 읽기 전용 확인했다. 개별 job 로그의 재감사는 하지 않았다.

## NOT_RUN·종료

- Windows Python3.11: 실행 환경 없음. Windows3.14·WSL3.11 성공과 구분한다.
- 실제 MDX compiler/browser: 미실행. 이번 Markdown 경계는 공식 CommonMark0.31.2와 Windows의 기존 Markdown 파서로 대조했다. 외부 파서를 설치하거나 제품 의존성에 추가하지 않았다.
- 소비자 build/type/e2e·채택 gate, npm/PyPI registry 설치·게시, workflow dispatch: 요청 범위 밖. 소비자 task와 T-010/T-502의 책임을 유지한다.
- 신규 P1/P2를 재현했으므로 제품을 수정하지 않고 NO-GO 원본을 확정하여 종료한다. 수정 후보의 두 독립 리뷰가 필요하다.
