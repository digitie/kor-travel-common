# T-103 수정 후 20 — Reviewer A 독립 원본

- 실행 ID: `reviewer_a-t103-post20-20260908T135211+0900`.
- 판정: **NO-GO**. 누적 16개 중 15개 FIXED / `A-P2-06`(P2) OPEN. 직전 CR fence·ESM 반례는 해결됐으나 LS/PS를 Markdown 문단으로 확장하면서 정상 인용 오탐 회귀가 생겼다. 신규 ID 및 신규 P0/P1/P3는 없다.
- 제품 candidate: commit `dd06f22150d9ac9bed25ee7abc0b65265cdaa651`, tree `184a1755640d78fd52ce1dbeb30897a557a01ece`.
- 직전 제품: `415984bf7cb450d44d7661424884d6641fef8309`. `tools/ux_lint.py`·`tests/test_ux_lint.py` 전체 delta를 읽었다. AGENTS·문서 라우터·resume·T-103·standards·runbooks의 동일성을 확인해 이미 읽은 계약을 재사용했다.
- 공통 manifest: commit `358f67177eff969750e3bc8a40b2cea8b512c234`의 `docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-20-manifest.md`를 `git show`로 읽었다.
- 격리: 새 detached checkout `F:/dev/kor-travel-common-wt/review-t103-post20-a`. 시작 2026-09-08 13:52:11.655 KST, 제품 검토 종료 13:59:19.964 KST에 위 HEAD/tree와 `git status --porcelain=v1` 빈 출력을 직접 확인했다.
- 상대의 이번 결과·미확정 raw·과거 상대 raw는 읽지 않았다. 후보·manifest·소비자·Git config는 수정하지 않았다. 이 원본만 별도 commit하며 제품 후보와 raw commit을 구분한다.

## 요청과 범위

Windows Python 3.14 / WSL Python 3.11에서 full/focused/static gate와 누적 CSS·MDX·Unicode·개행·JSON·redaction·diff·symlink·airport corpus를 실행했다. CR/LF/CRLF/LS/PS를 source/report 좌표, JavaScript 주석/식, Markdown 인용/문단으로 나누어 대조했다. manifest의 작성자 성공 주장만으로 수용하지 않고 외부 문법 계약도 직접 확인했다.

## A-P2-06 — P2 / OPEN: LS/PS를 Markdown 빈 문단으로 오인

- 위치: `tools/ux_lint.py:21` `_MDX_LINE_BREAK_PATTERN` 및 22~25행 문단 정규식; `tools/ux_lint.py:143` `_paragraph_end`, 312행 `_find_inline_span_end`. `tests/test_ux_lint.py:340`의 새 시험도 모든 종결자를 Markdown에서 동일하게 처리한다는 가정을 고정한다.
- 이번 CR 수정의 효과: 직전 단독 CR backtick/tilde fence 밖 실행식은 P8 1개/exit 1이며 ESM 뒤 정상 인용은 0개/exit 0이다. LF·CRLF 대조 및 Git CR/LS/PS mapping도 유지됐다.
- 새 회귀: ECMAScript의 LS/PS 줄 종결자를 Markdown의 문단 경계에도 사용한다. 정상 닫힌 code span을 중간에서 미종결 span으로 나누어, 그 안에 있는 인용을 실행식으로 탐지한다.

문법 근거를 2026-09-08에 직접 열어 확인했다. [CommonMark 0.31.2 §2.1](https://spec.commonmark.org/0.31.2/#line-ending)은 Markdown 줄 끝을 LF·단독 CR·CRLF로 정의하며 LS/PS는 포함하지 않는다. [§6.1](https://spec.commonmark.org/0.31.2/#code-spans)의 같은 길이 backtick delimiter는 code span을 닫는다. [MDX 공식 설명](https://mdxjs.com/docs/what-is-mdx/#markdown)은 기본 Markdown 문법으로 CommonMark를 사용한다고 명시한다. 따라서 manifest의 모든 종결자 동일 취급 주장보다 T-103의 실제 MDX 인용 제외 계약을 우선해 판정했다. JavaScript 주석/식에서 LS/PS를 줄 끝으로 인식해야 한다는 기존 수정은 유지해야 한다.

임시 root의 `case.mdx`에 다음 Python 문자열을 UTF-8 bytes로 쓴다. `separator`는 실제 U+2028 또는 U+2029 문자다.

```python
separator = "\u2028"  # U+2029도 같은 결과
body = 'Example `` quoted' + separator + separator
body += '{window.confirm("quoted")}' + separator + 'closing ``'
fixture.write_bytes(body.encode('utf-8'))
```

명령: 임시 root에서 `python -B -X utf8 <후보>/tools/ux_lint.py --root <임시-root> --fail-new --json`.

| 입력 | 후보 Windows 3.14 / WSL 3.11 | 직전 제품 양 OS | 기대 |
|---|---|---|---|
| LS가 든 정상 2자 span | **P8 1개, line 1, exit 1** | finding 0, exit 0 | 인용이므로 finding 0, exit 0 |
| PS가 든 정상 2자 span | **P8 1개, line 1, exit 1** | finding 0, exit 0 | 인용이므로 finding 0, exit 0 |
| 같은 문자열의 LF·CRLF·CR 빈 문단 대조 | P8 1개, exit 1 | CR은 직전 미해결 경계 | 실제 빈 문단이 span을 나누므로 정상 탐지 |

설치되어 있던 Windows `markdown-it-py 4.2.0`의 `MarkdownIt('commonmark').parse(body)`로도 LS/PS 두 입력이 `text` + **단일 `code_inline`**임을 확인했다. 렌더 결과에서 `{window.confirm(...)}`는 `<code>` 안에 있다. LF 대조는 두 문단과 일반 text로 나뉜다. 추가 Windows 대조에서는 delimiter를 1자로 바꾼 LS/PS 입력도 같은 code_inline/후보 P8 오탐이다. 이 로컬 parser는 리뷰용 독립 대조이며 제품 의존성으로 추가하거나 registry에서 설치하지 않았다.

- 영향: 유효한 MDX의 정상 인용이 실패 gate에 걸린다. 원 MDX finding의 P2를 유지한다.
- 수정 방향: Markdown(CR/LF/CRLF), ECMAScript(CR/LF/LS/PS), Git/report(LF 물리 행)의 경계를 분리한다. Markdown의 paragraph/fence/span에 LS/PS를 일괄 도입하지 않는다. 기존 JS 주석 종료와 Git newline preservation은 유지한다.
- 수용 기준: 정상 1·2자 span의 LS/PS는 finding 0/exit 0이고, CR/LF/CRLF의 실제 빈 문단 뒤 실행식은 finding 1/exit 1이다. CR fence·ESM 오탐, JSX 중첩 주석, 미종결 span, Git 가짜 hunk·baseline 대조를 함께 유지한다. 이번 시험의 LS/PS 기대값도 실제 Markdown 의미에 맞춰 수정한다.

후보 밖 helper `F:/dev/kor-travel-common/.git/codex-audit/t103-post20-boundary-a.py`의 SHA256은 `8F2725CB830A6C9B12432C199F837468A60EFEC8CE8C4B91AB12CAB7872D70F6`이다. `python -B -X utf8 <helper> <후보-worktree>`로 양 OS 실행했고, WSL은 `/mnt/f/...` 경로와 uv Python 3.11을 사용했다. 같은 helper를 직전 `review-t103-post19-a` 제품에도 양 OS 실행해 새 회귀임을 대조했다. 후보 제품은 변경하지 않았다.

## 누적 finding disposition

| 원 ID | 원 심각도 | 판정과 실제 대조 |
|---|---|---|
| A-P1-01 | P1 | FIXED — CSS scope/specificity/media 교집합·unsupported·comment-gap·빈 목록·descendant. |
| A-P1-02 | P1 | FIXED — OKLCH chroma 25%와 0.1 일치. |
| A-P1-03 | P1 | FIXED — sRGB source-over 및 대비 1.6620953314177012 대조. |
| A-P1-04 | P1 | FIXED — baseline 앞 신규 행만 fail. |
| A-P1-05 | P1 | FIXED — 외부 Git root의 동일 basename 구분. |
| A-P2-06 | P2 | OPEN — CR 원 반례 해결, LS/PS 정상 code span 오탐 새 회귀. |
| A-P2-07 | P2 | FIXED — 옵션 형태 base 일반 오류 2. |
| A-P2-08 | P2 | FIXED — WSL quoted/tab 파일명 diff. Windows tab 파일명은 NOT_RUN. |
| A-P2-09 | P2 | FIXED — 비유한/음수/bool/중복/400·5000자리 JSON 오류 2. |
| A-P2-10 | P2 | FIXED — 오류·JSON·summary·argparse 합성 marker 비공개. |
| A-P2-11 | P2 | FIXED — muted 읽기 표면 추가 31쌍 및 미달 판정. |
| A-P3-12 | P3 | FIXED — geo 미달 8개, airport 현재 1.32와 과거 조사 1.15 구분. |
| A-P1-13 | P1 | FIXED — 실제 `++counter;` 추가 행 diff `+++` 후속 P6 탐지. |
| A-P2-14 | P2 | FIXED — 양 OS self-symlink root 오류 2, traceback 없음. Windows 직접 링크 확인 포함. |
| A-P2-15 | P2 | FIXED — 깊이 2000 JSON 양 도구 오류 2, traceback 없음. |
| A-P1-16 | P1 | FIXED — CR/CRLF/LF/LS/PS 가짜 hunk 유무 10개 및 plain/tracked/untracked 15개 대조에서 P8 added/fail true, exit 1. |

## 실행 검증

Windows Python 3.14.3와 WSL uv Python 3.11.15를 사용했다. WSL 명령에는 `uv run --no-project --python 3.11`을 붙였고 전체 unittest에만 `--with jsonschema`를 추가했다.

| 명령 | Windows | WSL |
|---|---|---|
| `python -B -X utf8 -m unittest discover -s tests -p 'test_*.py'` | 최초 291개 실행 중 오류 1; 전용 TEMP 재실행 **291 통과/skip 0**, 100.860초 | 291 실행/290 통과/skip 1, 113.261초; Windows 8.3 전용 skip |
| `python -B -X utf8 -m unittest tests.test_kt_contrast tests.test_ux_lint` | 53 통과, 24.155초 | 53 통과, 17.408초 |
| `python -B -X utf8 -m unittest tests.test_ux_lint` | 위 focused/full에 포함 | 별도 30 통과, 7.855초 |
| `python -B -X utf8 tools/validate_document_links.py` | 문서 451/대상 2420/오류 0 | 동일 |
| `python -B -X utf8 tools/validate_plan.py` | task 106/오류 0 | 동일 |
| `python -B -X utf8 tools/check_spdx.py` | 파일 56/오류 0 | 동일 |
| `python -B -X utf8 tools/scan_secrets.py --all` | 파일 583/발견 0 | 동일 |
| `python -B -X utf8 tools/check_prod_redaction.py --all` | 파일 583/발견 0 | 동일 |
| `python -B -X utf8 tools/check_versions.py --self-check` | exit 0, 소비자 검사 아님 | 동일 |
| `python -B -X utf8 tools/check_aliases.py packages/tokens/aliases` | CSS 1/오류 0 | 동일 |
| `git diff --check 415984bf7cb450d44d7661424884d6641fef8309 dd06f22150d9ac9bed25ee7abc0b65265cdaa651` | exit 0 | exit 0 |

Windows 최초 full은 160.408초, `test_requirements_include_cannot_escape_consumer_root`의 임시 `outside-requirements.txt` 삭제에서 `PermissionError: WinError 5`가 발생했다. 해당 시험은 `root.parent` 아래 고정 이름을 사용하며 이번 delta에는 없다. 다른 프로세스와의 충돌 가능성은 추정으로 남기고, 확정된 사실은 삭제 접근 오류다. 별도 UUID 임시 디렉터리에 프로세스 `TEMP`/`TMP`를 설정해 전체를 다시 실행했고 291개가 모두 통과했다. 최초 실행을 성공으로 덮어쓰지 않으며 제품 파일·Git config는 변경하지 않았다.

자신의 후보 밖 `t103-post17-reviewer-a-probe.py`, `t103-post18-diff-a.py`, `t103-post19-margins-a.py`, `t103-post19-mapping-a.py`에 이번 후보 경로를 전달해 누적 corpus를 양 OS 실행했다. 누적 helper의 직전/이번 Windows 출력 차이는 없고, 양 OS 차이는 runtime·tab 파일명·플랫폼별 symlink probe뿐이었다. 상대 raw/결과는 사용하지 않았다. 정본 light/dark 27쌍 미달 0, 4앱 light 예제 미달 4/8/8/4 및 등록 baseline의 exit 0, UX fixture report 12개/exit 0을 확인했다. 기본 report의 exit 0을 위반 없음으로 집계하지 않는다.

WSL 정적 gate에만 `GIT_DIR=/mnt/f/dev/kor-travel-common/.git/worktrees/review-t103-post20-a`, `GIT_WORK_TREE=/mnt/f/dev/kor-travel-common-wt/review-t103-post20-a`를 프로세스 환경으로 설정했고 시험/probe에는 주입하지 않았다. 임시 Git fixture의 commit은 개별 경로 stage와 `git -c user.name=Review fixture -c user.email=fixture@example.invalid commit`으로 만들었다.

`gh run list --commit dd06f22150d9ac9bed25ee7abc0b65265cdaa651 --json databaseId,headSha,status,conclusion,url --limit 5`로 [CI 34188310748](https://github.com/digitie/kor-travel-common/actions/runs/34188310748)의 exact head 및 **success**를 직접 확인했다. CI 성공과 미해결 P2는 별개로 기록한다.

## 미실행과 원본 보존

- NOT_RUN: Windows Python 3.11(런타임 부재), 소비자 build/e2e·adoption, npm/PyPI registry·게시, workflow dispatch, 실제 브라우저/MDX compiler 렌더링. 로컬 CommonMark parse는 실제 소비자 빌드 성공이 아니다.
- 원본만 경로를 명시해 stage하고 전체 staged diff·diff check·문서 링크·staged secret/redaction을 검증한 후 raw-only commit한다. 제품 후보·manifest·기존 원본은 변경하지 않는다.
