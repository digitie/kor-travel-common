# T-103 수정 후 12 — Reviewer A 독립 원본

- 실행 ID: `reviewer_a-t103-post12-20260908T115909+0900`
- 판정: **NO-GO**. 누적 15개 ID 중 14개 FIXED, `A-P2-06`(P2) OPEN. 신규 ID 0개, 잔여 P0/P1/P3 0개.
- 제품 후보: `386d815f54b79102954a695b0d65dda093bdfbec`; tree `1236efa499a5a8fd75198745e4e3161f39cfcf33`.
- 직전 제품 후보: `c0c93c47e5f25aa0879fd0fb4e56261f6f624138`. 이번 실제 도구·시험 delta는 `tools/ux_lint.py`, `tests/test_ux_lint.py` 2개 파일이다.
- 공통 manifest: commit `3afc47080c752490b8163d69938f0e28a049540f`의 `docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-12-manifest.md`를 `git show`로 읽었다. manifest의 과거 원본 메타데이터만 확인했으며 상대 원본 본문·이번 결과는 읽지 않았다.
- 격리: `F:/dev/kor-travel-common-wt/review-t103-post12-a`, detached checkout. 후보·manifest·소비자 파일·Git 설정을 수정하지 않았다. 이번 원본 한 파일만 별도 커밋한다.
- 시작: 2026-09-08 11:59:09.227 KST, 위 후보 SHA/tree, `git status --porcelain=v1` 빈 출력.
- 제품 검토 종료: 2026-09-08 12:05:19.440 KST, 동일 SHA/tree, `git status --porcelain=v1` 빈 출력. 이후 보고서 추가로 생기는 commit/tree는 제품 후보와 구분한다.

## 요청과 독립 검토 범위

조정자는 같은 immutable 후보에서 Windows Python 3.14와 WSL Python 3.11로 full/focused/static gate와 누적 CSS/JSON/redaction/diff/symlink/airport 반례를 재현하고, 특히 미종결 1/2자 Markdown span 뒤 직접·단항·키워드·논리·숫자·주석 선행 MDX expression, 여러 줄 JSX expression과 정상 닫힌 span 대조를 확인하도록 요청했다. Windows Python 3.11은 NOT_RUN으로 기록하며 제품 후보가 아닌 원본 evidence만 커밋한다는 조건을 지켰다.

수정 구현과 시험 delta를 직접 읽고 현재 코드에 누적 A 반례를 다시 실행했다. 작성자의 성공 주장이나 상대 reviewer의 결과를 판단 근거로 사용하지 않았다. 일반 회귀 시험 성공과 직접 반례의 실패를 별도로 집계한다.

## 잔여 finding

### A-P2-06 — P2 / OPEN: 정규식·선행 소수점 표현식을 문서로 가려 P8을 누락

- 위치: `tools/ux_lint.py:38`, `tools/ux_lint.py:152`, `tools/ux_lint.py:159`, `tools/ux_lint.py:206`.
- 원인: `_looks_like_mdx_expression_start`는 첫 문자가 숫자, 명시한 기호, ASCII 식별자 또는 키워드일 때만 실행식으로 보존한다. JavaScript 정규식 리터럴의 `/`와 유효한 선행 소수점 숫자의 `.`는 이 목록에 없다. `_mask_unclosed_inline_span`은 이 표현식 전체를 문서 인용으로 가려 버린다. `/*`·`//` 주석 건너뛰기만으로 `/x/` 리터럴은 처리되지 않는다.
- 재현 입력은 다음 두 형태다. 각각 선행 backtick을 1개와 2개로 실행해 총 4개의 실패 경로를 확인했다.

````text
Example ` unmatched {/x/.test(window.confirm('x'))}
Example `` unmatched {.5 && window.confirm('x')}
````

- 명령: `python -B -X utf8 tools/ux_lint.py <임시 fixture.mdx> --fail-new --json`.
- 실제: Windows 3.14.3와 WSL 3.11.15 모두 4개 경로 각각 exit **0**, `status: PASS`, findings **0**, fail_count **0**.
- 기대: 두 표현식 모두 `window.confirm` 호출을 포함하므로 P8 1개, `--fail-new` exit **1**이어야 한다.
- 양성 대조: 같은 두 표현식에서 미종결 backtick 앞부분만 제거하면 양 OS 모두 P8 1개 / exit 1이다. 음성 대조: 표현식을 정상 닫힌 Markdown 코드 span 안에 넣으면 양 OS 모두 finding 0개 / exit 0이다.
- 영향: 문서와 실행 코드를 함께 다루는 MDX에서 유효한 실행 표현식을 정상 문서로 오판하여 금지 패턴 gate가 거짓 PASS를 반환한다. 범위는 MDX 어휘 전처리이며 실행·배포 취약점으로 과장하지 않는다.
- 수정 수용 기준: 위 4개 경로와 대조를 회귀 시험에 추가하고, 미종결 Markdown delimiter가 미인식 중괄호 실행식을 가리는 근거가 되지 않게 처리한다. 첫 문자 목록을 계속 늘리는 방식 대신 지원 여부가 불확실한 실행식은 보존하거나 명시적 입력 오류로 실패시키는 경계를 정한다. 정상 닫힌 span·일반 문서 음성 대조를 유지한다.

외부 의존성 없이 동일 반례를 재현하는 명령 본문은 다음과 같다. 후보 checkout에서 이 Python 본문을 실행하면 임시 파일만 생성한다.

```python
from pathlib import Path
import json
import subprocess
import sys
import tempfile

tool = Path.cwd() / "tools" / "ux_lint.py"
with tempfile.TemporaryDirectory() as temporary:
    fixture = Path(temporary) / "case.mdx"
    expressions = ["/x/.test(window.confirm('x'))", ".5 && window.confirm('x')"]
    for expression in expressions:
        for length in (1, 2):
            fixture.write_text("Example " + chr(96) * length + " unmatched {" + expression + "}\n", encoding="utf-8")
            result = subprocess.run([sys.executable, "-B", "-X", "utf8", str(tool), str(fixture), "--fail-new", "--json"], capture_output=True, text=True)
            report = json.loads(result.stdout)
            print(length, result.returncode, report)
```

## 누적 finding disposition

| 원 ID | 원 심각도 | 판정 | 이번 후보에서 직접 확인한 근거 |
|---|---|---|---|
| A-P1-01 | P1 | FIXED | root/dark specificity·조건 교집합·unsupported selector·빈 목록·descendant·comment-gap 경계 재현. `.dark/**/.dark`, `.dark/**/:not(.light)` 등 미지원 형태는 일반 입력 오류 2이며, 유효 cascade의 미달은 1이다. |
| A-P1-02 | P1 | FIXED | OKLCH chroma `25%`와 대응하는 `0.1`의 RGB 결과 일치. |
| A-P1-03 | P1 | FIXED | 흰색 20%를 검정에 sRGB source-over 합성한 결과와 `#333` 비교, 비율 1.6620953314177012 일치. |
| A-P1-04 | P1 | FIXED | baseline 앞에 신규 위반 행을 삽입하면 신규 행만 실패하고 기존 등록 건은 면제됨. |
| A-P1-05 | P1 | FIXED | 같은 basename의 외부 임시 Git root가 후보 저장소와 혼동되지 않음. |
| A-P2-06 | P2 | OPEN | 요청한 14개 prefix/길이 조합은 FIXED이나 정규식·선행 소수점 4개 경로에서 거짓 PASS 재현. |
| A-P2-07 | P2 | FIXED | `--base=--name-only`가 일반 입력 오류 2로 종료. |
| A-P2-08 | P2 | FIXED | WSL의 Git quoting/tab 파일명에서도 변경 행 P6 탐지. Windows 해당 파일명은 플랫폼 제한으로 NOT_RUN. |
| A-P2-09 | P2 | FIXED | NaN/Infinity/음수/bool/중복과 400·5000자리 JSON 입력은 일반 오류 2. |
| A-P2-10 | P2 | FIXED | 합성 민감 형태의 marker를 stderr/JSON/summary 및 argparse 오류에 평문 출력하지 않음. |
| A-P2-11 | P2 | FIXED | `--read-surface-muted`의 31개 쌍, 추가 4개 및 tertiary/muted 미달을 확인. |
| A-P3-12 | P3 | FIXED | geo 예제 8개 미달과 airport의 현재 수용 비율 1.32(실측 1.320934), 과거 조사 1.15 구분 유지. |
| A-P1-13 | P1 | FIXED | 실제 `++counter;` 추가 행에서 생기는 diff `+++`를 헤더로 버리지 않으며 후속 P6 추가 행을 탐지. |
| A-P2-14 | P2 | FIXED | 양 OS의 self-symlink root가 traceback 없이 일반 오류 2. 누적 helper의 초기 Windows 미지원 표기와 별개로 후속 Windows 직접 링크 probe를 실행함. |
| A-P2-15 | P2 | FIXED | 깊이 2000 JSON을 양 OS의 두 도구에 입력해 traceback 없이 일반 오류 2. |

이번 manifest가 요청한 직접 호출, `!`, `void`, `true &&`, `1 &&`, block comment, line comment 선행은 각각 미종결 1자/2자 span에서 양 OS 모두 P8 1개 / exit 1이었다. 여러 줄 JSX expression의 `outline-none`은 P6 1개 / exit 1, `safe` 대조는 0이었다. 파일 첫 span·3자 inline·4자/tilde/suffix fence·blockquote 빈 문단·backslash delimiter·tagged/computed template·배열/삼항·중첩 object·ESM·보간 주석 누적 대조도 실행했다.

## 실행 명령과 결과

아래 Windows 명령은 detached 후보에서 Python 3.14.3으로 실행했다. WSL은 같은 명령 앞에 `uv run --no-project --python 3.11`을 붙여 Python 3.11.15로 실행했으며 전체 시험에는 `--with jsonschema`도 사용했다. WSL의 Git 기반 정적 gate에만 해당 detached checkout의 `GIT_DIR`/`GIT_WORK_TREE`를 프로세스 환경으로 지정했다. 시험과 probe에는 Git 환경을 주입하지 않았다.

| 명령 | Windows 결과 | WSL 결과 |
|---|---|---|
| `python -B -X utf8 -m unittest discover -s tests -p 'test_*.py'` | 287 실행 / 287 통과 / skip 0, 87.528초 | 287 실행 / 286 통과 / skip 1, 58.598초. skip은 Windows 8.3 전용 시험 |
| `python -B -X utf8 -m unittest tests.test_kt_contrast tests.test_ux_lint` | 49 통과 / skip 0, 12.276초 | 49 통과 / skip 0, 9.300초 |
| `python -B -X utf8 tools/validate_document_links.py` | 427개 문서 / 2412개 대상 / 오류 0 | 동일 |
| `python -B -X utf8 tools/validate_plan.py` | task 106개 / 오류 0 | 동일 |
| `python -B -X utf8 tools/check_spdx.py` | 56개 / 오류 0 | 동일 |
| `python -B -X utf8 tools/scan_secrets.py --all` | 559개 / 발견 0 | 동일 |
| `python -B -X utf8 tools/check_prod_redaction.py --all` | 559개 / 발견 0 | 동일 |
| `python -B -X utf8 tools/check_versions.py --self-check` | exit 0; 소비자 검사 아님 | 동일 |
| `python -B -X utf8 tools/check_aliases.py packages/tokens/aliases` | CSS 1개 / 오류 0 | 동일 |
| `git diff --check e47f48e 386d815f54b79102954a695b0d65dda093bdfbec` | exit 0 | exit 0 |

직접 CLI 검증은 후보 소스 경로를 인자로 받는 외부 helper로 실행했다. Windows 명령은 `python -B -X utf8 F:/dev/kor-travel-common/.git/codex-audit/t103-post12-reviewer-a-probe.py F:/dev/kor-travel-common-wt/review-t103-post12-a`이며 WSL은 두 경로를 `/mnt/f/...`로 변환하고 위 uv 런타임을 사용했다. helper는 자신의 누적 A probe 코드를 재사용하지만 과거 raw 본문이나 상대 결과를 읽지 않는다. 현재 helper SHA256은 `8F3E09019ED3549B387F322F4D24D8CC8E2115D47A935FFE2D5B0615E12C2603`이다. helper는 저장소 바깥에 있으며 원본 commit에 포함하지 않는다. 위 최소 재현은 helper 없이 실행할 수 있다.

CLI 결과에서 토큰 정본 light/dark 각각 27쌍은 미달 0이었다. 4앱 예제 light 미달은 docker-manager/concierge/geo/airport 순서로 4/8/8/4이며 등록 baseline의 `--fail-new` exit 0은 미달 자체가 없다는 뜻이 아니다. UX fixture의 report 모드는 12개를 보고하고 exit 0이었다. JSON·argparse·symlink 오류의 generic 메시지와 traceback/marker 부재도 별도 확인했다.

정확한 제품 후보에 대한 원격 읽기 명령은 `gh run list --commit 386d815f54b79102954a695b0d65dda093bdfbec --json databaseId,headSha,status,conclusion,url --limit 5`였다. [CI run 34181831448](https://github.com/digitie/kor-travel-common/actions/runs/34181831448)의 headSha는 후보와 같지만 conclusion은 **cancelled**다. 이를 성공으로 집계하지 않았고 다른 manifest commit의 CI와 혼동하지 않았다.

## 미실행과 한계

- `NOT_RUN`: Windows Python 3.11. 실행 파일이 없어 조정자 지시에 따라 Windows 3.14와 WSL 3.11을 사용했다.
- `NOT_RUN`: 실제 소비자 build/e2e, consumer adoption gate, registry 조회·게시, workflow dispatch. common 리뷰 범위 밖이며 실행하지 않았다.
- `NOT_RUN`: 이번 후보에 대한 별도 브라우저/MDX compiler 렌더링. 소스 검토와 현재 CLI 양성·음성 대조에 근거한 finding이며 실제 소비자 실행 성공으로 주장하지 않는다.
- 정확한 후보 CI는 취소 상태다. 로컬 회귀 및 정적 gate 성공을 원격 CI 성공으로 바꾸지 않는다.
- 제품 검토 종료 후 원본만 명시 경로로 stage하고 staged diff/공백·링크·비공개 검사를 수행하여 보고서-only commit을 만든다. 제품 소스와 manifest는 변경하지 않는다.
