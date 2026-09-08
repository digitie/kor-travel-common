# T-103 수정 후 13 — Reviewer A 독립 원본

- 실행 ID: `reviewer_a-t103-post13-20260908T121337+0900`.
- 판정: **NO-GO**. 누적 15개 ID 중 14개 FIXED, `A-P2-06`(P2) OPEN. 신규 ID 0개. 잔여 P0/P1/P3 0개.
- 제품 후보 commit: `e8137efd8f4b53465b8cf9a1d333127e4186b73c`; tree: `091274064a82897f6f00ec8f3db2a8776379e13d`.
- 직전 제품 후보: `386d815f54b79102954a695b0d65dda093bdfbec`. 이번 도구·시험 delta는 `tools/ux_lint.py`와 `tests/test_ux_lint.py`이며 전체를 직접 읽었다.
- 공통 manifest: commit `6cb95d01de6cd4d7f8274c38854e119f1e5395e7`의 `docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-13-manifest.md`를 `git show`로 읽었다. manifest에 있는 과거 원본 메타데이터 외에 상대 원본·이번 결과·미확정 원본을 읽지 않았다.
- 격리: `F:/dev/kor-travel-common-wt/review-t103-post13-a`, 새 detached checkout. 제품·manifest·소비자·Git 설정을 수정하지 않았다. 새 원본 한 파일만 커밋한다.
- 시작: 2026-09-08 12:13:37.588 KST, 위 제품 SHA/tree, `git status --porcelain=v1` 빈 출력.
- 제품 검토 종료: 2026-09-08 12:15:44.708 KST, 동일 SHA/tree, `git status --porcelain=v1` 빈 출력. 이후 evidence commit/tree는 제품 후보와 구분한다.

## 요청과 검토 방법

동일 immutable 후보를 Windows Python 3.14와 WSL Python 3.11에서 독립 검토하고 full/focused/static gate 및 누적 CSS/JSON/redaction/diff/symlink/airport 반례를 재현했다. 특히 미종결 1/2자 Markdown span 뒤 직접·단항·키워드·논리·숫자·정규식·소수·나눗셈·xor·유니코드·주석 선행 MDX expression과 여러 줄 JSX expression, 정상 닫힌 span 음성 대조를 실행했다. 작성자의 시험 결과나 상대 reviewer 결과에 의존하지 않고 현재 코드와 실행 결과로 판정했다.

## A-P2-06 — P2 / OPEN: JavaScript 식별자와 Python 정규식의 차이로 실행식을 가림

- 위치: `tools/ux_lint.py:41`, `tools/ux_lint.py:154`, `tools/ux_lint.py:163`, `tools/ux_lint.py:213`.
- 원인: `_MDX_IDENTIFIER`의 Python `\w`가 JavaScript 식별자의 결합 문자와 ZWNJ를 포함하지 않는다. `char.isalpha()` 및 시작 문자 목록은 JavaScript 식별자의 Unicode escape 시작인 역슬래시도 허용하지 않는다. 이 결과 유효한 중괄호 실행식이 미종결 Markdown span의 문서 영역으로 가려진다.
- 최소 입력은 아래 Python의 `expression` 값으로 정확하게 생성한다. `e\u0301`과 `x\u200c`는 실제 문자를 생성하며, `\\u0078`은 JavaScript escape를 그대로 파일에 쓴다. 각 값을 미종결 backtick 1개/2개 뒤에 놓아 총 6개 실패 경로를 확인했다.

```python
expressions = [
    "e\u0301 && window.confirm('x')",
    "\\u0078 && window.confirm('x')",
    "x\u200c && window.confirm('x')",
]
```

- 실제 명령: `python -B -X utf8 tools/ux_lint.py <임시 case.mdx> --fail-new --json`.
- 실제 출력: Windows 3.14.3와 WSL 3.11.15 모두 6개 경로 각각 exit **0**, `status: PASS`, findings **0**, fail_count **0**.
- 기대: 해당 실행식의 `window.confirm`을 P8 1개로 탐지하여 exit **1**. 지원하지 않는 문법이면 거짓 PASS 대신 명시적 입력 오류로 실패해야 한다.
- 양성 대조: 동일 식에서 미종결 backtick 앞부분을 제거하면 양 OS 모두 P8 1개 / exit 1. 음성 대조: 정상 닫힌 코드 span 안에 놓으면 모두 finding 0개 / exit 0.
- JavaScript 문법 확인: Windows Node `v25.9.0`의 `new Function`에서 세 식별자를 각각 선언한 뒤 동일 expression을 평가했다. 모두 문법 승인, `window.confirm`을 대신한 로컬 stub 호출 1회, 결과 true였다. 브라우저 대화상자나 소비자 코드를 실행한 것이 아니다.
- 영향: MDX 문서 안의 유효한 실행 코드를 정상 문서로 오인해 금지 패턴 gate가 거짓 PASS를 반환한다. 도구의 탐지 정확성 결함이며 별도의 운영 보안 사고로 주장하지 않는다.
- 수정 방향·수용 기준: JavaScript 식별자 문법 일부를 Python 정규식으로 추정하여 문서 면제 여부를 결정하지 않는다. 미종결 Markdown span 뒤 미인식 중괄호 expression을 보존하거나 명시적 오류로 실패시키고, 위 6개 경로와 정상 닫힌 span 대조를 회귀 시험에 고정한다. 유효한 닫힌 인용만 면제한다는 경계를 먼저 정한다.

helper 없이 같은 CLI 실패를 재현하는 전체 Python 본문이다. 후보 checkout에서 실행하며 임시 파일만 생성한다.

```python
from pathlib import Path
import json
import subprocess
import sys
import tempfile

tool = Path.cwd() / "tools" / "ux_lint.py"
expressions = ["e\u0301 && window.confirm('x')", "\\u0078 && window.confirm('x')", "x\u200c && window.confirm('x')"]
with tempfile.TemporaryDirectory() as temporary:
    fixture = Path(temporary) / "case.mdx"
    for expression in expressions:
        for length in (1, 2):
            fixture.write_text("Example " + chr(96) * length + " unmatched {" + expression + "}\n", encoding="utf-8")
            result = subprocess.run([sys.executable, "-B", "-X", "utf8", str(tool), str(fixture), "--fail-new", "--json"], capture_output=True, text=True)
            print(ascii(expression), length, result.returncode, json.loads(result.stdout))
```

## 누적 finding disposition

| 원 ID | 원 심각도 | 판정 | 이번 후보에서 직접 재현한 근거 |
|---|---|---|---|
| A-P1-01 | P1 | FIXED | CSS root/dark·specificity·media 교집합·unsupported selector·빈 목록·descendant·comment-gap. `.dark/**/.dark`, `.dark/**/:not(.light)` 등은 일반 오류 2이며 유효 cascade의 미달은 1. |
| A-P1-02 | P1 | FIXED | OKLCH chroma `25%`와 `0.1` 변환 RGB 일치. |
| A-P1-03 | P1 | FIXED | 흰색 20% / 검정 sRGB source-over 결과와 `#333`의 대비 1.6620953314177012 일치. |
| A-P1-04 | P1 | FIXED | baseline 앞 신규 행 삽입 시 신규 행만 fail, 기존 등록 행만 면제. |
| A-P1-05 | P1 | FIXED | 같은 basename의 외부 임시 Git root를 후보 저장소와 구분. |
| A-P2-06 | P2 | OPEN | regexp/decimal 및 요청된 연산자·한글 식별자는 FIXED이나 결합 문자·ZWNJ·Unicode escape 6개 경로에서 거짓 PASS. |
| A-P2-07 | P2 | FIXED | `--base=--name-only` 일반 오류 2. |
| A-P2-08 | P2 | FIXED | WSL Git quoting/tab 파일명 변경 행의 P6 탐지. Windows 해당 파일명은 플랫폼 제한으로 NOT_RUN. |
| A-P2-09 | P2 | FIXED | NaN/Infinity/음수/bool/중복 및 400·5000자리 JSON 일반 오류 2. |
| A-P2-10 | P2 | FIXED | 합성 민감 형태 marker가 stderr/JSON/summary/argparse 오류에 평문 노출되지 않음. |
| A-P2-11 | P2 | FIXED | 추가 muted 읽기 표면의 총 31개 쌍, 추가 4개 및 tertiary/muted 미달 확인. |
| A-P3-12 | P3 | FIXED | geo 8개 미달, airport 현재 1.32(실측 1.320934)와 과거 조사 1.15 구분 유지. |
| A-P1-13 | P1 | FIXED | `++counter;` 추가 행의 diff `+++`를 파일 헤더로 버리지 않고 후속 추가 행 P6 탐지. |
| A-P2-14 | P2 | FIXED | 양 OS self-symlink root 일반 오류 2 / traceback 없음. 초기 helper의 Windows 미지원 표기와 별개로 후속 Windows 직접 링크 probe를 실행함. |
| A-P2-15 | P2 | FIXED | 깊이 2000 JSON을 두 도구에 입력해 양 OS에서 일반 오류 2 / traceback 없음. |

미종결 1자/2자 span 뒤 직접 호출·`!`·`void`·`true &&`·`1 &&`·block/line comment·`/x/`·`.5`·나눗셈·xor·한글 식별자·`in`·`instanceof`는 모두 양 OS에서 탐지됐다. 여러 줄 JSX expression의 `outline-none`은 P6 1개 / exit 1, `safe` 대조는 0이었다. 파일 첫 span·3자 inline·4자/tilde/suffix fence·blockquote 빈 문단·backslash delimiter·tagged/computed template·배열/삼항·중첩 object·ESM·보간 주석 누적 대조도 재실행했다.

## 실제 명령과 결과

Windows Python은 3.14.3, WSL은 `uv run --no-project --python 3.11`로 실행한 3.11.15다. WSL 전체 시험에는 `--with jsonschema`도 사용했다. WSL Git 기반 정적 gate에만 detached checkout의 `GIT_DIR`/`GIT_WORK_TREE`를 프로세스 환경으로 지정했다. 시험/probe에는 Git 환경을 주입하지 않았으며 `.git/config`를 바꾸지 않았다.

| Windows 명령(WSL은 위 uv 접두 사용) | Windows 결과 | WSL 결과 |
|---|---|---|
| `python -B -X utf8 -m unittest discover -s tests -p 'test_*.py'` | 287 실행 / 287 통과 / skip 0, 85.874초 | 287 실행 / 286 통과 / skip 1, 51.940초. skip은 Windows 8.3 전용 시험 |
| `python -B -X utf8 -m unittest tests.test_kt_contrast tests.test_ux_lint` | 49 통과 / skip 0, 12.728초 | 49 통과 / skip 0, 7.603초 |
| `python -B -X utf8 tools/validate_document_links.py` | 430개 문서 / 2412개 대상 / 오류 0 | 동일 |
| `python -B -X utf8 tools/validate_plan.py` | task 106개 / 오류 0 | 동일 |
| `python -B -X utf8 tools/check_spdx.py` | 56개 / 오류 0 | 동일 |
| `python -B -X utf8 tools/scan_secrets.py --all` | 562개 / 발견 0 | 동일 |
| `python -B -X utf8 tools/check_prod_redaction.py --all` | 562개 / 발견 0 | 동일 |
| `python -B -X utf8 tools/check_versions.py --self-check` | exit 0; 소비자 검사 아님 | 동일 |
| `python -B -X utf8 tools/check_aliases.py packages/tokens/aliases` | CSS 1개 / 오류 0 | 동일 |
| `git diff --check 081e898 e8137efd8f4b53465b8cf9a1d333127e4186b73c` | exit 0 | exit 0 |

직접 CLI probe 명령은 `python -B -X utf8 F:/dev/kor-travel-common/.git/codex-audit/t103-post13-reviewer-a-probe.py F:/dev/kor-travel-common-wt/review-t103-post13-a`다. WSL은 두 경로를 `/mnt/f/...`로 변환하고 uv 접두를 사용했다. helper는 자신의 누적 A probe 코드를 재사용하며 과거 raw 본문이나 상대 결과를 읽지 않는다. helper SHA256: `63A96A61C909FD861F6B4D6C7F0E58D4EA69A1D7B9E28E4CF028EB00347443C8`. 후보 밖 helper는 evidence commit에 포함하지 않는다.

CLI에서 정본 light/dark 각각 27개 쌍 미달 0. 4앱 예제 light 미달은 docker-manager/concierge/geo/airport 순서로 4/8/8/4이며 등록 baseline의 `--fail-new` exit 0은 미달 자체가 없다는 뜻이 아니다. UX fixture의 report 모드는 12개를 보고하고 exit 0이었다. 일반 오류와 각 출력 채널의 traceback/marker 부재도 별도로 확인했다.

원격 읽기 명령 `gh run list --commit e8137efd8f4b53465b8cf9a1d333127e4186b73c --json databaseId,headSha,status,conclusion,url --limit 5`로 [CI run 34182659672](https://github.com/digitie/kor-travel-common/actions/runs/34182659672)의 exact headSha와 conclusion **success**를 확인했다. 이 성공과 직접 반례의 잔여 P2를 별도로 판정한다.

## 미실행과 한계

- `NOT_RUN`: Windows Python 3.11. 실행 파일이 없어 조정자 지시대로 Windows 3.14와 WSL 3.11을 사용했다.
- `NOT_RUN`: 실제 소비자 build/e2e 및 adoption gate, registry 조회·게시, workflow dispatch. 사용자 common 범위 밖이며 수행하지 않았다.
- `NOT_RUN`: 이번 후보의 별도 브라우저/MDX compiler 렌더링. 현재 CLI 대조와 Node JavaScript 문법 검증이 실제 소비자 빌드 성공을 뜻하지 않는다.
- 원본 추가 후 전체 staged diff를 읽고 공백·문서 링크·staged 비공개 검사를 수행해 원본 한 파일만 커밋한다. 후보 소스·manifest와 기존 원본은 변경하지 않는다.
