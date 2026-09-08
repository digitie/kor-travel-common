# T-103 수정 후 15 — Reviewer A 독립 원본

- 실행 ID: `reviewer_a-t103-post15-20260908T124159+0900`.
- 판정: **NO-GO**. 누적 15개 ID 중 14개 FIXED, `A-P2-06`(P2) OPEN. 신규 ID 0개, 잔여 P0/P1/P3 0개.
- 제품 후보 commit: `210c2de324b18fcaa4e3f8b18fe5965226cb79d7`; tree: `58418960efa7e486d60fa95d9a3e7f335e0ad74b`.
- 직전 제품 후보: `0b2330e93d2b05a954593c82ef0ea230821adf28`. 도구·시험 delta는 `tools/ux_lint.py`, `tests/test_ux_lint.py`이며 전체를 읽었다. AGENTS·문서 라우터·task·standards·runbook의 delta는 없다.
- 공통 manifest: commit `e72b7466d02e2fcfe6f9811fd3ca4cfa4478fd60`의 `docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-15-manifest.md`를 `git show`로 읽었다. manifest의 과거 원본 메타데이터 외에 상대 원본·이번 결과·미확정 원본을 읽지 않았다.
- 격리: `F:/dev/kor-travel-common-wt/review-t103-post15-a`, 새 detached checkout. 제품·manifest·소비자·Git config를 수정하지 않았다. 새 원본 한 파일만 별도 커밋한다.
- 시작: 2026-09-08 12:41:59.974 KST, 위 SHA/tree, `git status --porcelain=v1` 빈 출력.
- 제품 검토 종료: 2026-09-08 12:44:57.036 KST, 동일 SHA/tree, `git status --porcelain=v1` 빈 출력. 이후 원본 commit/tree는 제품 후보와 구분한다.

## 요청과 검토 범위

동일 immutable 후보에서 manifest의 full/focused/static gate와 누적 CSS/JSON/redaction/diff/symlink/airport corpus를 독립 실행했다. 특히 `℘`/`Ⅳ`/U+037A/`a·`/`a·`/`async x =>`와 미종결 1/2자 span, 정상 닫힌/개방 대조를 재현했다. 작성자의 성공 주장이나 상대 결과에 의존하지 않았다. 기존 실패 형태가 닫힌 사실과 새 런타임 경계에서 같은 누락이 남은 사실을 구분한다.

## A-P2-06 — P2 / OPEN: Python Unicode DB 버전에 따라 같은 MDX를 다르게 면제

- 위치: `tools/ux_lint.py:180`, `tools/ux_lint.py:183`, `tools/ux_lint.py:232`, `tools/ux_lint.py:289`.
- 원인: 실행식 시작 판정이 실행 중인 Python의 `unicodedata.category`/`isidentifier`에 의존한다. Python 3.11의 DB에 미등록인 유효 JavaScript 식별자가 시작하면 false를 반환하고, `_mask_unclosed_inline_span`이 뒤 실행식 전체를 문서로 가린다. 불확실한 식별자를 정상 인용으로 면제하는 `A-P2-06`의 잔여이며 새 ID로 중복 집계하지 않는다.
- 최소 expression: Python의 `chr(0x11F02) + " && window.confirm('x')"`로 실제 U+11F02 문자를 생성한다. 앞에 미종결 backtick을 1개/2개 놓은 두 경로에서 실패한다.
- 실제 명령: 후보 `tools/ux_lint.py`의 절대 경로를 사용하여 임시 root에서 `python -B -X utf8 <후보>/tools/ux_lint.py <임시>/case.mdx --fail-new --json`.

| 입력 형태 | Windows Python 3.14.3 | WSL Python 3.11.15 | 기대 |
|---|---|---|---|
| 미종결 1자 span 뒤 expression | P8 1개 / exit 1 | **PASS / 0개 / fail_count 0 / exit 0** | P8 1개 / exit 1 |
| 미종결 2자 span 뒤 expression | P8 1개 / exit 1 | **PASS / 0개 / fail_count 0 / exit 0** | P8 1개 / exit 1 |
| span 없는 같은 expression | P8 1개 / exit 1 | P8 1개 / exit 1 | 양성 대조 |
| 정상 닫힌 코드 span | 0개 / exit 0 | 0개 / exit 0 | 음성 대조 |

- 원인 확인 명령: `python -B -X utf8 -c 'import unicodedata; c=chr(0x11f02); print(unicodedata.unidata_version, unicodedata.category(c), c.isidentifier())'`. Windows 출력은 `16.0.0 Lo True`, WSL uv Python 3.11 출력은 `14.0.0 Cn False`다.
- JavaScript 문법 대조: Windows Node `v25.9.0`에서 U+11F02를 변수로 선언하고 동일 expression을 `new Function`으로 평가했다. 문법 승인, 로컬 `confirm` stub 호출 1회, 결과 true. Node의 `process.versions.unicode`는 `17.0`이었다. 실제 소비자나 브라우저 대화상자를 실행하지 않았다.
- 영향: 같은 소스를 검사해도 지원 런타임에 따라 결과가 달라지고, Python 3.11 경로에서 금지 호출을 거짓 PASS로 반환한다. 드문 식별자에 한정된 도구 탐지 결함이며 운영 사고로 주장하지 않는다.
- 수정 수용 기준: 위 두 경로와 개방/닫힌 대조를 양 런타임 시험에 추가한다. 미등록/불확실한 중괄호 expression을 문서 면제 근거로 쓰지 않고 보존하거나 명시적 입력 오류로 실패시킨다. 식별자 규칙을 계속 유지한다면 지원 Unicode 기준을 고정하고 런타임 DB 차이에도 동일한 판정을 보장한다. U+11F02 한 코드포인트만 추가하여 다음 DB 차이를 숨기는 방식은 피한다.

helper 없이 재현하는 Python 본문이다. 후보 checkout에서 실행하며 임시 파일만 생성한다. subprocess의 cwd는 임시 root로 지정한다.

```python
from pathlib import Path
import json
import subprocess
import sys
import tempfile

tool = Path.cwd() / "tools" / "ux_lint.py"
expression = chr(0x11F02) + " && window.confirm('x')"
with tempfile.TemporaryDirectory() as temporary:
    fixture = Path(temporary) / "case.mdx"
    for length in (1, 2):
        fixture.write_text("Example " + chr(96) * length + " unmatched {" + expression + "}\n", encoding="utf-8")
        result = subprocess.run([sys.executable, "-B", "-X", "utf8", str(tool), str(fixture), "--fail-new", "--json"], cwd=temporary, capture_output=True, text=True)
        print(length, result.returncode, json.loads(result.stdout))
```

## 누적 disposition

| 원 ID | 원 심각도 | 판정 | 이번 후보 직접 검증 |
|---|---|---|---|
| A-P1-01 | P1 | FIXED | CSS root/dark·specificity·media 교집합·unsupported selector·빈 목록·descendant·comment-gap. `.dark/**/.dark`, `.dark/**/:not(.light)` 일반 오류 2, 유효 cascade 미달 1. |
| A-P1-02 | P1 | FIXED | OKLCH chroma `25%`와 `0.1` RGB 일치. |
| A-P1-03 | P1 | FIXED | 흰색 20% / 검정 sRGB source-over와 `#333` 대비 1.6620953314177012 일치. |
| A-P1-04 | P1 | FIXED | baseline 앞 신규 행만 fail, 기존 등록 행은 면제. |
| A-P1-05 | P1 | FIXED | 같은 basename의 외부 임시 Git root 구분. |
| A-P2-06 | P2 | OPEN | 지정된 기존 형태는 FIXED이나 U+11F02에서 WSL Python 3.11만 미종결 span 뒤 호출을 누락. |
| A-P2-07 | P2 | FIXED | `--base=--name-only` 일반 오류 2. |
| A-P2-08 | P2 | FIXED | WSL Git quoting/tab 파일명 추가 행 P6 탐지. Windows 해당 파일명은 NOT_RUN. |
| A-P2-09 | P2 | FIXED | NaN/Infinity/음수/bool/중복 및 400·5000자리 JSON 일반 오류 2. |
| A-P2-10 | P2 | FIXED | 합성 marker가 stderr/JSON/summary/argparse 오류에 평문 노출되지 않음. |
| A-P2-11 | P2 | FIXED | muted 읽기 표면 총 31쌍, 추가 4쌍 및 tertiary/muted 미달 확인. |
| A-P3-12 | P3 | FIXED | geo 미달 8개, airport 현재 1.32(실측 1.320934)와 과거 1.15 구분 유지. |
| A-P1-13 | P1 | FIXED | `++counter;` 추가 행의 diff `+++`를 헤더로 버리지 않고 후속 추가 행 P6 탐지. |
| A-P2-14 | P2 | FIXED | 양 OS self-symlink root 일반 오류 2 / traceback 없음. 초기 helper의 Windows 미지원 표기와 별개로 후속 Windows 직접 링크 probe 실행. |
| A-P2-15 | P2 | FIXED | 깊이 2000 JSON을 두 도구에 입력해 양 OS 일반 오류 2 / traceback 없음. |

`℘`/`Ⅳ`/U+037A/`a·`/`a·`/`async x =>`의 미종결 1/2자 span은 양 OS 모두 P8 1개 / exit 1이다. 직접 호출·단항·키워드·논리·숫자·정규식·소수·나눗셈·xor·한글·결합 문자·ZWNJ/ZWJ·두 Unicode escape·주석 선행도 유지됐다. 여러 줄 JSX expression의 `outline-none`은 P6 1개 / exit 1, `safe`는 0. 파일 첫 span·3자 inline·4자/tilde/suffix fence·blockquote 빈 문단·backslash delimiter·tagged/computed template·배열/삼항·중첩 object·ESM·보간 주석도 재실행했다.

## 실제 검증

Windows Python 3.14.3, WSL은 `uv run --no-project --python 3.11`의 Python 3.11.15다. WSL 전체 시험에는 `--with jsonschema`를 추가했다. WSL Git 기반 정적 gate에만 detached checkout의 `GIT_DIR`/`GIT_WORK_TREE`를 프로세스 환경으로 지정했고 시험/probe에는 주입하지 않았다. Git config는 불변이다.

| Windows 명령(WSL은 위 uv 접두 사용) | Windows | WSL |
|---|---|---|
| `python -B -X utf8 -m unittest discover -s tests -p 'test_*.py'` | 288 실행 / 288 통과 / skip 0, 94.578초 | 288 실행 / 287 통과 / skip 1, 54.972초. skip은 Windows 8.3 전용 |
| `python -B -X utf8 -m unittest tests.test_kt_contrast tests.test_ux_lint` | 50 통과 / skip 0, 12.327초 | 50 통과 / skip 0, 9.464초 |
| `python -B -X utf8 tools/validate_document_links.py` | 문서 436개 / 대상 2416개 / 오류 0 | 동일 |
| `python -B -X utf8 tools/validate_plan.py` | task 106개 / 오류 0 | 동일 |
| `python -B -X utf8 tools/check_spdx.py` | 56개 / 오류 0 | 동일 |
| `python -B -X utf8 tools/scan_secrets.py --all` | 568개 / 발견 0 | 동일 |
| `python -B -X utf8 tools/check_prod_redaction.py --all` | 568개 / 발견 0 | 동일 |
| `python -B -X utf8 tools/check_versions.py --self-check` | exit 0; 소비자 검사 아님 | 동일 |
| `python -B -X utf8 tools/check_aliases.py packages/tokens/aliases` | CSS 1개 / 오류 0 | 동일 |
| `git diff --check 9f7dcf7 210c2de324b18fcaa4e3f8b18fe5965226cb79d7` | exit 0 | exit 0 |

직접 probe 명령은 `python -B -X utf8 F:/dev/kor-travel-common/.git/codex-audit/t103-post15-reviewer-a-probe.py F:/dev/kor-travel-common-wt/review-t103-post15-a`다. WSL은 두 경로를 `/mnt/f/...`로 바꾸고 uv 접두로 실행했다. 자신의 누적 A probe만 재사용하며 상대 결과·과거 raw 본문은 읽지 않는다. 후보 밖 helper SHA256은 `BB533BAFB4E852E55EAB939438036FC294D4AB1D316E24FE615ACCAA9698ED15`이며 commit에 포함하지 않는다.

정본 light/dark 각각 27쌍 미달 0. 4앱 예제 light 미달은 docker-manager/concierge/geo/airport 순서로 4/8/8/4이며 baseline의 `--fail-new` exit 0을 미달 없음으로 해석하지 않는다. UX fixture report는 finding 12개 / exit 0이다. 오류 채널의 traceback/합성 marker 부재도 별도 검증했다.

`gh run list --commit 210c2de324b18fcaa4e3f8b18fe5965226cb79d7 --json databaseId,headSha,status,conclusion,url --limit 5`로 [CI run 34184310063](https://github.com/digitie/kor-travel-common/actions/runs/34184310063)의 exact headSha와 conclusion **success**를 확인했다. 회귀·CI 성공과 직접 반례의 잔여 P2를 별도로 판정한다.

## 미실행과 한계

- `NOT_RUN`: Windows Python 3.11. 런타임 부재로 조정자 지정 Windows 3.14 / WSL 3.11을 사용했다.
- `NOT_RUN`: 실제 소비자 build/e2e·adoption gate, registry 조회·게시, workflow dispatch. common 리뷰 범위 밖이다.
- `NOT_RUN`: 이번 후보의 브라우저/MDX compiler 렌더링. CLI 대조와 Node 문법 검증은 실제 소비자 빌드 성공을 뜻하지 않는다.
- 원본 추가 후 전체 staged diff·공백·문서 링크·staged 비공개 검사를 확인하여 원본만 커밋한다. 제품·manifest·기존 원본은 변경하지 않는다.
