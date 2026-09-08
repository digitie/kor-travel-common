# T-103 수정 후 21 — Reviewer A 독립 원본

- 실행 ID: `reviewer_a-t103-post21-20260908T141028+0900`.
- 판정: **PASS**. 누적 A finding 16개 모두 FIXED. 이번 독립 검토에서 신규·잔여 P0/P1/P2/P3 finding 0개.
- 제품 candidate commit: `7e31b54e92c52e3b859b80c520d7ae88c2522159`; tree: `2cd07cf45d1428d1027b6dd647c48353c3bdde59`.
- 직전 제품: `dd06f22150d9ac9bed25ee7abc0b65265cdaa651`. `tools/ux_lint.py`, `tests/test_ux_lint.py` 전체 delta를 읽었다. AGENTS·문서 라우터·resume·T-103·standards·runbooks의 동일성을 확인해 이미 읽은 계약을 재사용했다.
- 공통 manifest: commit `6bd3e445acc3e97851e1caa0254ba0b02af604cc`의 `docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-21-manifest.md`를 `git show`로 읽었다.
- 격리: 새 detached checkout `F:/dev/kor-travel-common-wt/review-t103-post21-a`. 시작 2026-09-08 14:10:28.735 KST와 제품 검토 종료 14:13:48.131 KST에 위 HEAD/tree 및 `git status --porcelain=v1` 빈 출력을 직접 확인했다.
- 상대 reviewer의 이번 결과·미확정 raw·과거 상대 raw는 읽지 않았다. 후보·manifest·소비자·Git config를 변경하지 않았다. 새 원본 한 파일만 별도 commit하며 제품 후보와 raw commit을 구분한다.

## 요청과 검토 범위

Windows Python 3.14 / WSL Python 3.11에서 manifest의 full/focused/static gate 및 누적 CSS·MDX·Unicode·개행·JSON·redaction·diff·symlink·airport corpus를 독립 실행했다. 특히 CommonMark 문단/인용과 ECMAScript 주석/식의 줄 경계, CR/LF/CRLF/LS/PS의 1·2·3자 span·fence·ESM·가짜 hunk를 대조했다.

## A-P2-06 수정 확인

Markdown 문단·fence·line prefix는 CR/LF/CRLF로 제한하고, JavaScript 주석·expression의 LS/PS 의미는 유지한다. Git/report의 LF 행 좌표도 보존한다. 이 분리는 앞서 직접 확인한 [CommonMark 0.31.2의 줄 끝](https://spec.commonmark.org/0.31.2/#line-ending)·[code span](https://spec.commonmark.org/0.31.2/#code-spans) 및 [MDX의 CommonMark 기본 지원](https://mdxjs.com/docs/what-is-mdx/#markdown)과 일치한다. 이번에는 과거 원본 판정을 가져오지 않고 아래 입력을 새 후보에서 다시 실행했다.

임시 root의 `case.mdx`에 다음 구조를 `write_bytes`로 쓰고 `python -B -X utf8 <후보>/tools/ux_lint.py --root <임시-root> --fail-new --json`을 실행했다.

```python
delimiter = "`" * width  # width는 1, 2, 3
body = 'Example ' + delimiter + ' quoted' + separator + separator
body += '{window.confirm("quoted")}' + separator + 'closing ' + delimiter
```

| 직접 대조 | Windows·WSL 실제 결과 | 판정 |
|---|---|---|
| LS/PS 각각 1·2·3자 정상 span(6개) | finding 0 / exit 0 | FIXED: 정상 인용 제외 |
| LF/CRLF/CR 각각 빈 문단을 사이에 둔 1·2·3자 span(9개) | P8 1개 / exit 1 | 실제 문단 뒤 실행식 탐지 |
| 5개 구분자의 JS 줄 주석 종료·ESM template(10개) | 각각 P8/P6 1개 / exit 1 | ECMAScript 경계 유지 |
| LF/CRLF/CR 각각 닫힌 backtick·tilde fence 뒤 실행식(6개) | P8 1개 / exit 1 | fence 밖 실행식 탐지 |
| LF/CRLF/CR 각각 ESM 뒤 정상 인용(3개) | finding 0 / exit 0 | CR 오탐 회귀 없음 |
| LF/CRLF/CR 각각 미종결 1·2자 span 뒤 ESM(6개) | P6 1개 / exit 1 | 선언 문맥 복귀 유지 |
| CR-LF/LF-CR/CRLF-CR/CR-CRLF 혼합 fence(4개) | P8 1개 / exit 1 | 혼합 개행 닫힘 유지 |

총 **각 OS 44개, 기대값 불일치 0개**다. 후보 밖 helper는 `F:/dev/kor-travel-common/.git/codex-audit/t103-post21-boundary-a.py`, SHA256 `C7A0C195A402309C53DA4C24D458569D30B35A9CCC6C6B93B97C55D9E55B5684`다. 명령은 `python -B -X utf8 <helper> <후보-worktree>`이며 WSL은 `/mnt/f/...` 경로와 uv Python 3.11을 사용했다. helper는 임시 root만 쓰고 제품 파일은 변경하지 않는다.

## 누적 finding disposition

| 원 ID | 원 심각도 | 판정과 이번 재검증 |
|---|---|---|
| A-P1-01 | P1 | FIXED — CSS scope/specificity/media 교집합·unsupported selector·comment-gap·빈 목록·descendant. |
| A-P1-02 | P1 | FIXED — OKLCH chroma 25%와 0.1 RGB 일치. |
| A-P1-03 | P1 | FIXED — sRGB source-over 대비 1.6620953314177012 및 `#333` 대조. |
| A-P1-04 | P1 | FIXED — baseline 앞 신규 행만 fail, 기존 등록 행 면제. |
| A-P1-05 | P1 | FIXED — 외부 Git root의 같은 basename 구분. |
| A-P2-06 | P2 | FIXED — 누적 MDX lexer 반례와 이번 CommonMark/ECMAScript 44개 대조 통과. |
| A-P2-07 | P2 | FIXED — 옵션 형태 base 일반 오류 2. |
| A-P2-08 | P2 | FIXED — WSL quoted/tab 파일명 diff; Windows tab 파일명은 NOT_RUN. |
| A-P2-09 | P2 | FIXED — 비유한/음수/bool/중복/400·5000자리 JSON 일반 오류 2. |
| A-P2-10 | P2 | FIXED — 오류·JSON·summary·argparse의 합성 marker 비공개. |
| A-P2-11 | P2 | FIXED — muted 읽기 표면 추가 31쌍 및 미달 판정. |
| A-P3-12 | P3 | FIXED — geo 미달 8개, airport 현재 1.32와 과거 조사 1.15 구분 유지. |
| A-P1-13 | P1 | FIXED — 실제 `++counter;` 추가 행의 diff `+++` 후속 P6 탐지. |
| A-P2-14 | P2 | FIXED — 양 OS self-symlink root 일반 오류 2/traceback 없음. Windows 직접 링크 확인 포함. |
| A-P2-15 | P2 | FIXED — 깊이 2000 JSON 양 도구 일반 오류 2/traceback 없음. |
| A-P1-16 | P1 | FIXED — CR/CRLF/LF/LS/PS 가짜 hunk 유무 10개와 plain/tracked/untracked 15개에서 P8 added/fail true, exit 1. |

## 실행 명령과 결과

Windows Python 3.14.3, WSL uv Python 3.11.15. WSL 명령에는 `uv run --no-project --python 3.11`을 붙였고 전체 unittest에만 `--with jsonschema`를 추가했다. 전체 시험은 양 OS 모두 A 전용 임시 디렉터리를 사용했다. Windows의 프로세스 TEMP/TMP와 WSL의 TMPDIR만 지정했고 source Git config는 수정하지 않았다.

| 명령 | Windows | WSL |
|---|---|---|
| `python -B -X utf8 -m unittest discover -s tests -p 'test_*.py'` | 291 통과 / skip 0, 104.222초 | 291 실행 / 290 통과 / skip 1, 62.636초; Windows 8.3 전용 skip |
| `python -B -X utf8 -m unittest tests.test_kt_contrast tests.test_ux_lint` | 53 통과, 17.693초 | 53 통과, 12.662초 |
| `python -B -X utf8 -m unittest tests.test_ux_lint` | full/focused에 포함 | 별도 30 통과, 4.986초 |
| `python -B -X utf8 tools/validate_document_links.py` | 문서 454 / 대상 2425 / 오류 0 | 동일 |
| `python -B -X utf8 tools/validate_plan.py` | task 106 / 오류 0 | 동일 |
| `python -B -X utf8 tools/check_spdx.py` | 파일 56 / 오류 0 | 동일 |
| `python -B -X utf8 tools/scan_secrets.py --all` | 파일 586 / 발견 0 | 동일 |
| `python -B -X utf8 tools/check_prod_redaction.py --all` | 파일 586 / 발견 0 | 동일 |
| `python -B -X utf8 tools/check_versions.py --self-check` | exit 0, 소비자 검사 아님 | 동일 |
| `python -B -X utf8 tools/check_aliases.py packages/tokens/aliases` | CSS 1 / 오류 0 | 동일 |
| `git diff --check dd06f22150d9ac9bed25ee7abc0b65265cdaa651 7e31b54e92c52e3b859b80c520d7ae88c2522159` | exit 0 | exit 0 |

자신의 후보 밖 `t103-post17-reviewer-a-probe.py`, `t103-post18-diff-a.py`, `t103-post19-margins-a.py`, `t103-post19-mapping-a.py`에 이번 후보 경로를 전달해 누적 corpus를 양 OS 실행했다. 누적 helper의 직전/이번 Windows 출력 차이는 없고, 양 OS 차이는 runtime·tab 파일명·플랫폼별 self-symlink probe뿐이었다. 이는 상대 reviewer 결과 비교가 아니라 자신의 두 환경 출력 대조다. 이전 raw 본문은 사용하지 않았다.

정본 light/dark 각각 27쌍 미달 0, 4앱 light 예제 미달 4/8/8/4 및 등록 baseline의 exit 0, UX fixture report 12개/exit 0을 확인했다. 기본 report의 exit 0을 위반 없음으로 해석하지 않는다. 기존 Unicode 식별자·FEFF·async·LS/PS 줄 주석·JSX 보간 주석 양성 및 닫힌 인용·주석 음성도 유지됐다.

WSL 정적 gate에만 `GIT_DIR=/mnt/f/dev/kor-travel-common/.git/worktrees/review-t103-post21-a`, `GIT_WORK_TREE=/mnt/f/dev/kor-travel-common-wt/review-t103-post21-a`를 프로세스 환경으로 설정했고 시험/probe에는 주입하지 않았다. 임시 Git fixture의 baseline은 개별 경로 stage와 `git -c user.name=Review fixture -c user.email=fixture@example.invalid commit`으로 만들었다.

`gh run list --commit 7e31b54e92c52e3b859b80c520d7ae88c2522159 --json databaseId,headSha,status,conclusion,url --limit 5`로 [CI 34189368995](https://github.com/digitie/kor-travel-common/actions/runs/34189368995)의 exact head 및 **success**를 직접 확인했다.

## 미실행과 원본 보존

- NOT_RUN: Windows Python 3.11(런타임 부재), 소비자 build/e2e·adoption, npm/PyPI registry·게시, workflow dispatch, 이번 후보의 실제 브라우저/MDX compiler 렌더링. 이 PASS는 검토한 common 제품 후보에만 적용하며 후속 소비자 gate를 닫지 않는다.
- 원본 파일만 경로를 명시해 stage하고 전체 staged diff·diff check·문서 링크·staged secret/redaction을 확인한 뒤 raw-only commit한다. 제품 후보·manifest·기존 evidence는 변경하지 않는다.
