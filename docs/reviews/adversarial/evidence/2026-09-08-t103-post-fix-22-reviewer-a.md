# T-103 수정 후 독립 적대적 리뷰 22 — Reviewer A

## 판정과 기준선

- 실행 ID: `T103-POST22-A-20260908-142017-KST` (`reviewer_a`).
- 최종 verdict: **NO-GO**. 신규 P0 0개, P1 0개, P2 1개(`A-P2-19`), P3 0개. 기존 A 16개 반례는 아래 범위에서 FIXED이며, Markdown fence 들여쓰기의 새 경계는 수정이 필요하다.
- 제품 후보 commit: `61f1cc6a900e25268e0c5eadc32ce1c5ccc9d3f3`.
- 제품 후보 tree: `bab9313184719713bc96fcb455b38b121f8db0f5`.
- delta 기준: `7e31b54e92c52e3b859b80c520d7ae88c2522159`.
- 공통 manifest: commit `43d7f530cbe987c89e99ad2f5a6665d65724a78d`의 `docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-22-manifest.md`. `git show`로 읽었다.
- 격리: `F:/dev/kor-travel-common-wt/review-t103-post22-a`의 detached checkout. 시작 2026-09-08 14:20:17.511 KST, 제품 검토 종료 14:27:47.153 KST. 시작·종료 HEAD/tree는 위 제품 후보와 같고 `git status --porcelain=v1` 출력은 비어 있었다.
- 상대 reviewer 원문·결과는 읽지 않았다. 공통 manifest에 있는 이전 원본 식별 정보만 보았다. 자신의 기존 재현 도구와 실행 로그를 재사용했으며, 후보 제품·manifest·소비자·git config를 수정하지 않았다. 이 보고서 한 파일만 별도 커밋한다.

## 요청과 범위

조정자 요청: 동일 immutable 후보에서 MDX lexer/CommonMark·Unicode 경계, Windows Python 3.14·WSL Python 3.11 full/focused, fence marker 뒤 ASCII space/tab와 LS/PS, 1·2·3자 span, CR/CRLF/LS/PS 문단/ESM 반례를 독립 재현하고 원본만 작성하여 report-only commit/hash/verdict를 제출한다.

`7e31b54..61f1cc6` 전체 변경 3파일을 대조했다. 제품 변경은 `tools/ux_lint.py`의 ASCII space/tab 정규화와 `tests/test_ux_lint.py`의 접미사 시험이며 나머지는 공통 manifest 기록이다. T-103 수용 기준, 기존 토큰·UX 계약과 airport 기준을 확인했다. 누적 CSS cascade/media/selector/comment, 색상 수학, MDX 실행식·인용·주석, JSON·오류 비공개, Git diff/source 행 매핑·symlink를 실제 후보에 다시 실행했다.

## 신규 finding

### A-P2-19 — 4칸 이상 들여쓴 닫힘 후보가 코드 fence를 조기에 끝내어 예제를 실패시킨다

- 심각도: **P2**, disposition: **OPEN / 수정 필요**.
- 위치: `tools/ux_lint.py:520`의 `lstrip(" \t")`, 같은 함수 524행의 닫힘 판정. 열린 fence 안에서 선행 들여쓰기 폭을 검사하지 않고 전부 제거한다.
- 최소 입력은 다음 Python 문자열이다. 세 번째 줄은 ASCII space 정확히 4개로 시작한다.

```python
body = '~~~tsx\nquoted\n    ~~~\n<div className="outline-none"/>\n~~~\n'
```

- 재현 명령: 아래 스크립트를 후보 worktree에서 `python -B -X utf8 -`의 stdin으로 실행한다. WSL은 같은 내용을 `uv run --no-project --python 3.11 python -B -X utf8 -`로 실행한다. 임시 파일만 생성한다.

```python
from pathlib import Path
import subprocess
import sys
import tempfile

tool = Path.cwd() / 'tools/ux_lint.py'
body = '~~~tsx\nquoted\n    ~~~\n<div className="outline-none"/>\n~~~\n'
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

- 실제: 양 OS 모두 exit 1, `status=FAIL`, `fail_count=1`, `case.mdx` line 4 column 17에 `P6`, `added=true`, `fail=true`.
- 기대: 마지막 줄의 정상 fence까지 JSX는 예제 텍스트이므로 findings 0, fail_count 0, exit 0. [CommonMark 0.31.2 §4.5](https://spec.commonmark.org/0.31.2/#fenced-code-blocks)는 닫힘의 선행 들여쓰기를 최대 3칸으로 제한한다. §2.2의 tab stop 4 기준도 적용해야 한다. 2026-09-08 공식 원문을 조회했다.
- 독립 대조: Windows의 기존 `markdown-it-py 4.2.0`, `MarkdownIt('commonmark').parse(body)`는 `fence` 토큰 하나를 만들며 그 내용에 `outline-none` JSX가 포함된다. 이 라이브러리는 리뷰 대조용이며 제품 의존성에 추가하지 않았다.
- 확장 재현: LF/CRLF/CR × backtick/tilde × 선행 4 space/tab/space+tab의 18개 모두 같은 오탐. 선행 1·2·3 space는 정상 닫힘으로 판단되고, 선행 LS/PS는 닫힘이 되지 않았다. 접미사의 space/tab/혼합은 닫힘, LS/PS/NBSP/VT/FF는 비닫힘으로 기대와 일치했다. 전체 102개 중 84개 기대 일치, 18개 불일치가 양 OS에서 동일했다.
- 원인과 도입 경계: post21 제품의 같은 최소 입력도 exit 1/P6이므로 이번 ASCII 제한 변경이 도입한 회귀로 분류하지 않는다. 기존의 무제한 `lstrip`에서 남은 경계를 이번 후보에서 확인했다.
- 영향: 정상 MDX 문서의 코드 예제가 실제 앱 코드처럼 report되고 `--fail-new`를 차단한다. 현재 추가된 접미사 시험만으로는 검출할 수 없다.
- 수정 수용 기준: 닫힘 후보의 시각적 선행 들여쓰기 폭을 보존하여 0~3칸만 허용하고 tab 확장을 고려한다. 양 OS에서 위 18개는 exit 0/발견 0, 0~3칸 정상 닫힘 뒤 실제 JSX는 P6, space/tab 접미사와 LS/PS 비닫힘 대조를 모두 유지한다. 후보에는 수정하지 않았다.

## 누적 A finding disposition

아래 FIXED는 해당 ID의 실행한 반례가 기대대로 동작한다는 뜻이며 전체 Markdown 문법의 완전성을 뜻하지 않는다. 새 들여쓰기 반례는 `A-P2-19`로 분리한다.

| ID | 원 심각도 | 이번 disposition·재현 근거 |
|---|---|---|
| A-P1-01 | P1 | FIXED. root/dark 순서·specificity·조건 교집합·지원하지 않는 selector/media·주석 gap·빈 목록 경계 유지 |
| A-P1-02 | P1 | FIXED. OKLCH chroma 25%와 0.1의 변환값 일치 |
| A-P1-03 | P1 | FIXED. sRGB 흰색 20%/검정 합성 대비 1.6620953314177012 |
| A-P1-04 | P1 | FIXED. 앞에 추가한 위반은 기존 baseline 예산으로 면제되지 않음 |
| A-P1-05 | P1 | FIXED. 이름이 같은 외부 Git root의 실제 추가행 검출 |
| A-P2-06 | P2 | FIXED. 기존 MDX 실행식·문서 인용 corpus와 LS/PS 1·2·3자 닫힌 span 음성 대조 유지 |
| A-P2-07 | P2 | FIXED. option 모양 base는 일반 입력 오류 2 |
| A-P2-08 | P2 | FIXED(WSL). Git quoted/tab 파일명 추가행 검출. Windows tab 파일명은 지원하지 않아 NOT_RUN |
| A-P2-09 | P2 | FIXED. NaN/Infinity/음수/bool/중복·거대 숫자 JSON 입력 거부 |
| A-P2-10 | P2 | FIXED. JSON·Markdown·annotation·summary·argparse 오류의 비공개 유지 |
| A-P2-11 | P2 | FIXED. muted 읽기 표면을 선언하면 31쌍, text-tertiary 미달 검출 |
| A-P3-12 | P3 | FIXED. geo 8개 미달, airport 현재 sRGB 1.320934와 과거 조사 1.15의 문서 경계 유지 |
| A-P1-13 | P1 | FIXED. 실제 `+++` 시작 추가 소스행을 diff 파일 헤더로 버리지 않음 |
| A-P2-14 | P2 | FIXED. self-symlink root는 양 OS exit 2, traceback 없음 |
| A-P2-15 | P2 | FIXED. 깊이 2000 JSON은 두 도구 모두 일반 입력 오류 2 |
| A-P1-16 | P1 | FIXED. CR/CRLF/LF/LS/PS와 문자열 가짜 hunk의 plain/tracked/untracked 추가행 매핑 유지 |

## 실제 실행·결과

- Windows Python 3.14.3: 전용 프로세스 TEMP/TMP에서 `python -B -X utf8 -m unittest discover -s tests -p 'test_*.py' -v` — **292개 통과, skip 0**, 95.526초.
- WSL Python 3.11.15: 전용 TMPDIR에서 `uv run --no-project --python 3.11 --with jsonschema python -B -X utf8 -m unittest discover -s tests` — **292개 실행, 291개 통과, skip 1**, 53.559초. Windows 8.3 API 전용 시험의 플랫폼 skip은 통과 건수에서 제외한다.
- 양 OS `python -B -X utf8 -m unittest tests.test_kt_contrast tests.test_ux_lint -v` — 각각 **54개 통과**, Windows 19.598초, WSL 12.856초. WSL은 `uv run --no-project --python 3.11` 접두사를 사용했다.
- WSL `uv run --no-project --python 3.11 python -B -X utf8 -m unittest tests.test_ux_lint` — **31개 통과**, 5.211초.
- 누적 외부 probe `t103-post17-reviewer-a-probe.py <candidate-root>` — Windows 264개 출력 행, WSL 263개 출력 행(이는 unittest 건수가 아님). 자신의 post21 실행 로그와 label/값 전체 대조에서 변경 0, traceback true 0. Windows self-symlink의 초기 helper NOT_RUN 행은 뒤의 실제 Windows 전용 재현 exit 2로 보완된다.
- `t103-post19-margins-a.py <candidate-root>` — 21개 LF/CRLF/CR fence·문단·ESM 양성/음성 대조 일치.
- `t103-post18-diff-a.py <candidate-root>` — 10개 separator/fake-hunk 조합 모두 새 P8 added/fail true. LF/CRLF line 3, CR/LS/PS line 2.
- `t103-post19-mapping-a.py <candidate-root>` — 15개 plain/tracked/untracked 조합 같은 기대 일치.
- `t103-post21-boundary-a.py <candidate-root>` — 44개 span·문단·ESM·주석·혼합 개행 조합, 양 OS `FAILURES []`.
- 새 `t103-post22-fence-a.py <candidate-root>` — 위 102개 행렬, 양 OS 18개 실패를 보존했다. helper SHA256 `78654BB162715E9A3B52D251EB1A81CE0EE5D6E905E60CA8BB3420BAB552E7AF`.
- 외부 helper와 실행 로그는 공용 checkout의 `.git/codex-audit/`에만 있으며 제품 트리에는 추가하지 않았다. Windows는 해당 Python 명령, WSL은 `/mnt/f/` 경로와 uv Python 3.11로 동일 helper를 실행했다.

다음 정적 명령을 양 OS 후보에서 실행했다. WSL Git 기반 검사는 프로세스 환경의 `GIT_DIR`·`GIT_WORK_TREE`만 해당 detached worktree로 지정했다.

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
git diff --check 7e31b54e92c52e3b859b80c520d7ae88c2522159 61f1cc6a900e25268e0c5eadc32ce1c5ccc9d3f3
```

- 양 OS 링크 455문서/2425대상, plan 106 task, SPDX 56파일, secret/redaction 각각 587파일에 오류·발견 0. registry 자체 검사와 별칭 CSS 1개 통과, diff-check 출력 없음.
- canonical light 대비 27쌍 통과, full/focused 및 누적 probe의 dark 전수 대조도 통과. UX checked-in fixture는 report 기본 모드로 예상 12건을 보고하고 fail_count 0/exit 0. 이를 위반 0건으로 집계하지 않았다.
- 정확한 후보 CI를 `gh run list --commit 61f1cc6a900e25268e0c5eadc32ce1c5ccc9d3f3 --json databaseId,headSha,status,conclusion,url --limit 5`로 읽기 전용 확인: [run 34189947563](https://github.com/digitie/kor-travel-common/actions/runs/34189947563), headSha 일치, completed/success. 개별 job 로그의 별도 재감사는 하지 않았다.

## 미실행과 한계

- `NOT_RUN`: Windows Python 3.11(실행 파일 없음). Windows 3.14와 WSL 3.11 결과를 대신 그 환경의 성공으로 표기하지 않았다.
- `NOT_RUN`: 실제 MDX compiler·브라우저 실행. CommonMark 공식 규격과 Windows의 기존 Markdown 파서로 이번 Markdown 코드 블록 경계를 대조했다. WSL에서는 제품 CLI를 동일 바이트 입력으로 실행했으며 외부 Markdown 파서를 설치하지 않았다.
- `NOT_RUN`: 소비자 저장소 build/e2e·채택 gate, npm/PyPI registry/게시, workflow dispatch. 이 요청 범위 밖이며 각각 후속 소비자 task와 T-010/T-502의 책임을 유지한다.
- 이번 원본은 독립 리뷰 결과이며 제품 수정이나 완료 승인, 소비자 gate 실행 증거가 아니다. A-P2-19를 수정한 새 불변 후보에서 두 reviewer의 재확인이 필요하다.
