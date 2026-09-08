# T-103 수정 후 14 — Reviewer A 독립 원본

- 실행 ID: `reviewer_a-t103-post14-20260908T122745+0900`.
- 판정: **NO-GO**. 누적 15개 ID 중 14개 FIXED, `A-P2-06`(P2) OPEN. 신규 ID 0개, 잔여 P0/P1/P3 0개.
- 제품 후보 commit: `0b2330e93d2b05a954593c82ef0ea230821adf28`; tree: `688332816480e217b3615dd6426e063c223e365a`.
- 직전 제품 후보: `e8137efd8f4b53465b8cf9a1d333127e4186b73c`. 이번 도구·시험 delta는 `tools/ux_lint.py`와 `tests/test_ux_lint.py`이며 전체를 읽었다. task·standards·runbook·AGENTS·문서 라우터의 delta는 없다.
- 공통 manifest: commit `507328aa615f68b7828e9da543f80a6c805c4d3a`의 `docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-14-manifest.md`를 `git show`로 읽었다. manifest에 포함된 원본 메타데이터 외에 상대 원본·이번 결과·미확정 원본을 읽지 않았다.
- 격리: `F:/dev/kor-travel-common-wt/review-t103-post14-a`, 새 detached checkout. 제품·manifest·소비자·Git 설정을 수정하지 않았다. 새 원본 한 파일만 별도 커밋한다.
- 시작: 2026-09-08 12:27:45.949 KST, 위 SHA/tree, `git status --porcelain=v1` 빈 출력.
- 제품 검토 종료: 2026-09-08 12:31:11.233 KST, 동일 SHA/tree, `git status --porcelain=v1` 빈 출력. 이후 evidence commit/tree는 제품 후보와 구분한다.

## 요청과 검토 범위

조정자의 요청에 따라 Windows Python 3.14와 WSL Python 3.11에서 full/focused/static gate 및 누적 CSS/JSON/redaction/diff/symlink/airport corpus를 재현했다. 특히 미종결 1/2자 Markdown span 뒤 직접·단항·키워드·논리·숫자·정규식·소수·나눗셈·xor·일반 Unicode·결합 문자·ZWNJ/ZWJ·두 Unicode escape·주석 선행 expression, 여러 줄 JSX expression과 정상 닫힌 span 대조를 확인했다. 작성자 시험 주장과 상대 결과를 판단 근거로 사용하지 않았다.

## A-P2-06 — P2 / OPEN: 일부 유효 식별자와 async arrow 실행식을 문서로 가림

- 위치: `tools/ux_lint.py:172`, `tools/ux_lint.py:178`, `tools/ux_lint.py:217`, `tools/ux_lint.py:267`.
- 원인 1: `_looks_like_mdx_expression_start`의 `char.isalpha()` 진입 조건은 `_is_mdx_identifier_start`가 받을 수 있는 비알파벳 식별자 시작 문자까지 차단한다. `℘`(U+2118)가 그 반례다.
- 원인 2: `_is_mdx_identifier_continue`의 범주 목록은 JavaScript에서 식별자 계속 문자로 허용하는 `·`(U+00B7)를 누락한다. `a·`가 잘려 이후 실행식이 가려진다.
- 원인 3: `async x => window.confirm('x')`에서 첫 식별자 다음 `x`는 허용된 기호/이항 단어 목록에 없다. 유효한 비동기 arrow 함수 표현식을 문서로 오판한다.
- 세 경우 모두 `_mask_unclosed_inline_span`이 실행식 전체를 문서 인용 영역으로 가리는 동일한 `A-P2-06`의 잔여이며 새 ID로 중복 집계하지 않는다.

각 expression을 미종결 backtick 1개/2개 뒤에 놓아 총 6개 실패 경로를 양 OS에서 확인했다.

```python
expressions = [
    "\u2118 && window.confirm('x')",
    "a\u00b7 && window.confirm('x')",
    "async x => window.confirm('x')",
]
```

- 명령: 후보 도구 절대 경로를 사용해 임시 root에서 `python -B -X utf8 <후보>/tools/ux_lint.py <임시>/case.mdx --fail-new --json` 실행.
- 실제: Windows 3.14.3와 WSL 3.11.15에서 6개 경로 각각 exit **0**, `status: PASS`, findings **0**, fail_count **0**.
- 기대: 실행식 안 `window.confirm`을 P8 1개로 탐지하여 exit **1**. 지원하지 않는 문법은 거짓 PASS 대신 명시적 입력 오류로 실패시켜야 한다.
- 양성 대조: 미종결 backtick 앞부분을 제거하면 세 expression 모두 양 OS P8 1개 / exit 1. 음성 대조: 정상 닫힌 Markdown span 안에서는 모두 finding 0개 / exit 0.
- 문법 검증: Windows Node `v25.9.0`의 `new Function`으로 두 식별자를 선언해 expression을 평가했고, async arrow는 반환된 함수를 호출해 확인했다. 세 경우 모두 문법 승인, 로컬 `confirm` stub 호출 1회, 결과 true였다. 브라우저 대화상자나 소비자 코드를 실행하지 않았다.
- 영향: MDX 문서와 실행 코드의 구분에서 금지 패턴 gate가 거짓 PASS를 반환한다. 운영 사고나 실제 소비자 취약점으로 과장하지 않는다.
- 수정 수용 기준: 위 6개 경로와 양성·음성 대조를 회귀 시험에 추가한다. 일부 첫 문자·단어로 실행식 전체의 문서 면제를 결정하는 방법을 중단하고, 미종결 span 뒤 불확실한 중괄호 expression은 검사 대상으로 보존하거나 명시적 오류로 실패시킨다. 정상 닫힌 코드 인용을 면제하는 계약은 유지한다.

다음 Python 본문은 helper 없이 같은 반례를 생성한다. **임시 파일 root를 subprocess의 cwd로 지정하는 것이 필요하다.** 후보 checkout에서 실행하면 임시 파일만 만든다.

```python
from pathlib import Path
import json
import subprocess
import sys
import tempfile

tool = Path.cwd() / "tools" / "ux_lint.py"
expressions = ["\u2118 && window.confirm('x')", "a\u00b7 && window.confirm('x')", "async x => window.confirm('x')"]
with tempfile.TemporaryDirectory() as temporary:
    fixture = Path(temporary) / "case.mdx"
    for expression in expressions:
        for length in (1, 2):
            fixture.write_text("Example " + chr(96) * length + " unmatched {" + expression + "}\n", encoding="utf-8")
            result = subprocess.run([sys.executable, "-B", "-X", "utf8", str(tool), str(fixture), "--fail-new", "--json"], cwd=temporary, capture_output=True, text=True)
            print(ascii(expression), length, result.returncode, json.loads(result.stdout))
```

## 누적 disposition

| 원 ID | 원 심각도 | 판정 | 이번 후보 직접 검증 |
|---|---|---|---|
| A-P1-01 | P1 | FIXED | root/dark·specificity·media 교집합·unsupported selector·빈 목록·descendant·comment-gap. `.dark/**/.dark`, `.dark/**/:not(.light)` 일반 오류 2, 유효 cascade 미달 1. |
| A-P1-02 | P1 | FIXED | OKLCH chroma `25%`와 `0.1` RGB 일치. |
| A-P1-03 | P1 | FIXED | 흰색 20% / 검정 sRGB source-over와 `#333` 대비 1.6620953314177012 일치. |
| A-P1-04 | P1 | FIXED | baseline 앞 신규 행은 fail, 기존 등록 행은 면제. |
| A-P1-05 | P1 | FIXED | 같은 basename의 외부 임시 Git root 구분. |
| A-P2-06 | P2 | OPEN | 결합 문자/ZWNJ/ZWJ/escape 수정은 FIXED이나 두 식별자와 async arrow 6개 경로 거짓 PASS. |
| A-P2-07 | P2 | FIXED | `--base=--name-only` 일반 오류 2. |
| A-P2-08 | P2 | FIXED | WSL Git quoting/tab 파일명 추가 행 P6 탐지. Windows 해당 파일명은 NOT_RUN. |
| A-P2-09 | P2 | FIXED | NaN/Infinity/음수/bool/중복 및 400·5000자리 JSON 일반 오류 2. |
| A-P2-10 | P2 | FIXED | 합성 marker가 stderr/JSON/summary/argparse 오류에 평문 노출되지 않음. |
| A-P2-11 | P2 | FIXED | muted 읽기 표면 총 31쌍, 추가 4쌍 및 tertiary/muted 미달 확인. |
| A-P3-12 | P3 | FIXED | geo 미달 8개, airport 현재 1.32(실측 1.320934)와 과거 1.15 구분 유지. |
| A-P1-13 | P1 | FIXED | 실제 `++counter;` 추가 행에서 생기는 diff `+++`와 후속 P6 추가 행을 구분. |
| A-P2-14 | P2 | FIXED | 양 OS self-symlink root 일반 오류 2 / traceback 없음. 초기 helper의 Windows 미지원 표기와 별개로 Windows 직접 링크 probe도 실행. |
| A-P2-15 | P2 | FIXED | 깊이 2000 JSON을 두 도구에 입력해 양 OS 일반 오류 2 / traceback 없음. |

요청된 직접 호출·`!`·`void`·`true &&`·`1 &&`·block/line comment·`/x/`·`.5`·나눗셈·xor·한글·결합 문자·ZWNJ·ZWJ·`\uXXXX`·`\u{...}` 및 식별자 계속 위치 escape는 양 OS에서 모두 탐지됐다. 여러 줄 JSX expression의 `outline-none`은 P6 1개 / exit 1, `safe` 대조는 0. 파일 첫 span·3자 inline·4자/tilde/suffix fence·blockquote 빈 문단·backslash delimiter·tagged/computed template·배열/삼항·중첩 object·ESM·보간 주석도 누적 probe로 재실행했다.

## 실제 검증

Windows Python 3.14.3, WSL은 `uv run --no-project --python 3.11`의 Python 3.11.15다. WSL 전체 시험에는 `--with jsonschema`를 추가했다. WSL Git 정적 gate에만 detached checkout의 `GIT_DIR`/`GIT_WORK_TREE`를 프로세스 환경으로 지정했고 시험/probe에 주입하지 않았다. Git config를 변경하지 않았다.

| Windows 명령(WSL은 위 uv 접두 사용) | Windows | WSL |
|---|---|---|
| `python -B -X utf8 -m unittest discover -s tests -p 'test_*.py'` | 287 실행 / 287 통과 / skip 0, 100.049초 | 287 실행 / 286 통과 / skip 1, 56.164초. skip은 Windows 8.3 전용 |
| `python -B -X utf8 -m unittest tests.test_kt_contrast tests.test_ux_lint` | 49 통과 / skip 0, 13.884초 | 49 통과 / skip 0, 11.635초 |
| `python -B -X utf8 tools/validate_document_links.py` | 문서 433개 / 대상 2414개 / 오류 0 | 동일 |
| `python -B -X utf8 tools/validate_plan.py` | task 106개 / 오류 0 | 동일 |
| `python -B -X utf8 tools/check_spdx.py` | 56개 / 오류 0 | 동일 |
| `python -B -X utf8 tools/scan_secrets.py --all` | 565개 / 발견 0 | 동일 |
| `python -B -X utf8 tools/check_prod_redaction.py --all` | 565개 / 발견 0 | 동일 |
| `python -B -X utf8 tools/check_versions.py --self-check` | exit 0; 소비자 검사 아님 | 동일 |
| `python -B -X utf8 tools/check_aliases.py packages/tokens/aliases` | CSS 1개 / 오류 0 | 동일 |
| `git diff --check 6da46d4 0b2330e93d2b05a954593c82ef0ea230821adf28` | exit 0 | exit 0 |

직접 probe 명령은 `python -B -X utf8 F:/dev/kor-travel-common/.git/codex-audit/t103-post14-reviewer-a-probe.py F:/dev/kor-travel-common-wt/review-t103-post14-a`다. 추가 경계는 같은 위치의 `t103-post14-boundary-a.py`를 동일 인자로 실행했다. WSL은 두 경로를 `/mnt/f/...`로 바꿔 uv 접두로 실행했다. 누적 helper는 자신의 A probe만 재사용하고 상대 결과·과거 raw 본문을 읽지 않는다. helper는 후보 밖에 있고 commit에 포함하지 않는다.

- 누적 helper SHA256: `26520BD1DD5495711B7F75D3AA29966C12E3FF30DD93BA23006B0FF3FA84B70F`.
- 경계 helper SHA256: `1CE0E6A2DEB8FEDF50E016E1E4095CEE91729E52BB75C983835890C385741B25`.
- 경계 helper 초회는 임시 cwd를 지정하지 않아 입력 root 경계를 넘겼고, helper가 빈 stdout을 JSON으로 읽다 실패했다. 이는 제품 traceback finding으로 집계하지 않았다. 후보를 수정하지 않고 helper의 cwd만 임시 root로 정정한 뒤 양 OS 12개 결과(6개 반례와 양성/음성 대조)를 모두 확인했다.

정본 light/dark 각각 27쌍 미달 0. 4앱 예제 light 미달은 docker-manager/concierge/geo/airport 순서로 4/8/8/4이며 baseline의 `--fail-new` exit 0을 미달 없음으로 해석하지 않는다. UX fixture report는 finding 12개 / exit 0이다. 오류 채널의 traceback/합성 marker 부재도 별도 검증했다.

`gh run list --commit 0b2330e93d2b05a954593c82ef0ea230821adf28 --json databaseId,headSha,status,conclusion,url --limit 5`로 [CI run 34183504801](https://github.com/digitie/kor-travel-common/actions/runs/34183504801)의 exact headSha와 conclusion **cancelled**를 확인했다. 다른 manifest commit CI 또는 로컬 검증을 이 후보의 CI 성공으로 집계하지 않는다.

## 미실행과 한계

- `NOT_RUN`: Windows Python 3.11. 런타임 부재로 조정자가 지정한 Windows 3.14 / WSL 3.11을 사용했다.
- `NOT_RUN`: 실제 소비자 build/e2e·adoption gate, registry 조회·게시, workflow dispatch. common 독립 리뷰 범위 밖이다.
- `NOT_RUN`: 이번 후보의 브라우저/MDX compiler 렌더링. CLI 대조와 Node 문법 검증은 실제 소비자 빌드 성공을 뜻하지 않는다.
- 원본 추가 후 전체 staged diff와 공백·문서 링크·staged 비공개 검사를 확인해 원본만 커밋한다. 제품·manifest·기존 원본은 변경하지 않는다.
