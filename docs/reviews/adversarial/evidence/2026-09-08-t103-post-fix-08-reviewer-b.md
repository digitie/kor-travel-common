# T-103 수정 후 8차 독립 적대적 리뷰 B 원본

## 실행 식별과 불변 기준선

- 실행 ID: `T103-POST8-B-20260908-110716-KST`
- 리뷰어: `reviewer_b`; 상대 reviewer 결과와 과거 raw report 본문은 열람하지 않았다. manifest의 기준선 메타데이터만 읽었다.
- 시작: `2026-09-08T11:07:16.3513601+09:00`; 제품 검토 종료: `2026-09-08T11:13:46.4659827+09:00`.
- 관찰 시작/종료 HEAD: `559a9e8a0e49feca2dab9d59df29039bbb0acfd3`.
- 관찰 시작/종료 tree: `322fb840ac458c8fc7a0c69f90b0d1bdb77495d6`.
- 시작/종료 `git status --porcelain=v1`: 모두 빈 출력, clean. 이 확인 뒤 본 원본 파일만 추가한다.
- manifest: commit `5c91168b9a594039bbfcd0dfae0cdf89519ae434`의 `2026-09-08-t103-post-fix-08-manifest.md`; `git show`로 읽었다. Git blob SHA256: `f7843254c68d24bfeeae2780773908bd4fdb7019e1aa730987ced6be5d309afc`.
- delta 기준: `63fe3d5c969b28bab4d528d3e24a054e3a8e30e6`; 변경 7개 경로 중 과거 raw 2개는 경로/통계만 대조하고 본문은 제외했다. 제품 변경 4개 파일과 manifest를 검토했다.
- 격리: `F:/dev/kor-travel-common-wt/review-t103-post8-b` detached worktree. 전체 시험/정적 gate는 이를 임시 디렉터리로 복사한 독립 Git 저장소에서 실행하고 `GIT_*` 상속을 제거했다. 직접 반례 입력은 별도 임시 디렉터리에만 생성했다.
- 기본 checkout `.git/config` 시작/종료 SHA256: `0A0F849E7874CF0A25926856F9D2E381CCBF4C2DCB5999869C57B86E0F5BEB5B`, 불변. 후보 제품/manifest/소비자 파일과 Git 설정은 수정하지 않았다.

## 전달받은 요청 원문

> post-fix-08 독립 적대적 리뷰를 실행해 주세요. 기준선은 불변 코드 후보 commit `559a9e8a0e49feca2dab9d59df29039bbb0acfd3`, tree `322fb840ac458c8fc7a0c69f90b0d1bdb77495d6`, manifest commit `5c91168b9a594039bbfcd0dfae0cdf89519ae434`입니다. 상대 reviewer의 결과나 과거 보고서를 읽지 말고, 같은 범위의 full/focused/static gates를 Windows Python 3.14와 WSL Python 3.11에서 가능한 만큼 재현하세요. Windows 3.11은 NOT_RUN으로 기록하세요. 결과는 새 raw 파일 `docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-08-reviewer-b.md`에 기록하고, 보고서 파일만 포함하는 immutable commit을 만들고 SHA256·verdict를 알려 주세요. 후보 코드/manifest를 수정하지 마세요. P0/P1/P2/P3를 엄격히 분류하고 PASS가 아니면 정확한 재현을 남겨 주세요.

## 최종 판정

**NO-GO.** 잔여 P1 1건과 신규 P2 1건이 Windows/WSL에서 동일하게 재현된다. P0 0건, P1 1건, P2 1건, P3 0건이다. 회귀 시험 성공은 이 직접 반례의 해소를 의미하지 않는다.

## B-P1-03 — 문단 경계를 넘은 닫는 delimiter가 실행 JSX를 가림

- 심각도/상태: **P1 / OPEN**, 기존 MDX 실행 영역 누락 finding의 잔여 반례.
- 위치: `tools/ux_lint.py:73`의 `_find_backtick_run_end`, `tools/ux_lint.py:368`의 다중 backtick span 처리.
- 원인: 같은 길이 delimiter를 파일 끝까지 탐색한다. Markdown 문단을 나누는 빈 줄 뒤의 별도 delimiter를 닫는 기호로 취급해 그 사이 ESM/JSX까지 문서 인용으로 가린다.
- 최소 입력 `Page.mdx`:

````mdx
Example `` unmatched

export const X=()=> <div className="outline-none"/>;

Later `` delimiter
````

- 명령: `python -B -X utf8 tools/ux_lint.py --root <이 파일만 있는 임시 디렉터리> --fail-new --json`.
- 실제: 두 OS 모두 `exit=0`, `status=PASS`, `findings=0`.
- 기대: 문단 사이 실행 JSX의 `outline-none`를 P6로 검출, `exit=1`, finding 1개. 마지막 `Later` 문단을 제거한 대조군은 실제로 `exit=1`, P6 1개였다.
- 영향: 문서 파일 앞뒤 인용 기호만으로 신규 접근성 위반이 성공 판정을 받는다. 실패를 차단해야 하는 `--fail-new` 계약을 우회한다.
- 권고/disposition: inline span 탐색을 유효한 Markdown 블록 범위로 제한하고 문단 밖 닫는 delimiter가 실행 블록을 흡수하지 못하게 한다. 단일/다중 delimiter, 빈 줄, ESM/JSX 조합을 실패·정상 대조군으로 추가한 뒤 다시 검증해야 한다.
- 이번 수정으로 닫힌 하위 반례: JS block comment의 `}`가 JSX 중괄호 깊이를 잘못 닫던 입력, 일반 접두 문장의 JSX 문법 인용, 이후 닫는 delimiter가 없는 미종결 1자/2자 span. 각각 기대한 P6 검출 또는 문서 제외를 확인했다.

## B-P2-13 — 파일 첫 문자와 3자 inline span에서 문서 인용을 실행 코드로 오인

- 심각도/상태: **P2 / NEW**. B-P1-03의 누락과 달리 문서만으로 CI가 잘못 실패하는 문제로 구분했다.
- 위치: `tools/ux_lint.py:200`의 `scope_start`, `tools/ux_lint.py:210`의 `run >= 3` 제외.
- 원인 1: 이전 빈 줄이 없으면 `rfind`가 -1인데 2를 더해 위치 1부터 탐색하므로 위치 0의 여는 backtick을 건너뛴다.
- 원인 2: 3자 이상 backtick을 항상 제외하여 줄 중간의 합법적인 inline code span도 추적하지 않는다. 뒤의 평범한 `outline-none` 인용을 앞의 가짜 JSX 문맥으로 읽는다.
- 최소 입력 A: 첫 문자가 아래 여는 backtick이다.

````mdx
`<div className={`

다른 인용: `outline-none`
````

- 최소 입력 B: fence가 아닌 문장 중간의 3자 inline span이다.

````mdx
문법 예시: ```<div className={```

다른 인용: `outline-none`
````

- 명령은 B-P1-03과 동일하다. 실제: 두 입력/두 OS 모두 `exit=1`, `status=FAIL`, P6 1개. 기대: 문서 인용뿐이므로 `exit=0`, finding 0개.
- 대조군: A 앞에 `문법 예시: `를 붙이거나 B의 delimiter를 2자로 바꾸면 두 OS 모두 `exit=0`, finding 0개다.
- 영향: 동일한 문서 예시의 파일 시작 위치나 합법적인 인용 길이에 따라 결과가 뒤집힌다. 문서 제외 계약과 `--fail-new`의 안정적인 판정을 깨뜨린다.
- 권고/disposition: 이전 문단이 없으면 시작을 0으로 정하고 fence는 줄/블록 위치와 함께 구분한다. 유효한 inline run 길이를 지원하고 원문 재탐색 대신 이미 판정한 Markdown/JSX 상태를 일관되게 사용한다. 두 최소 입력과 대조군을 회귀로 추가해야 한다.

## 최소 반례 재실행 코드

아래를 후보 밖 `probe.py`에 저장해 `python -B -X utf8 probe.py <후보 worktree>`로 실행한다. `python`은 Windows의 `py -3.14` 또는 WSL의 Python 3.11.15로 대체한다. 제품 파일을 쓰지 않는다.

```python
from pathlib import Path
import json
import os
import subprocess
import sys
import tempfile

root = Path(sys.argv[1]).resolve()
env = {k: v for k, v in os.environ.items()
       if not k.startswith("GIT_") and k != "GITHUB_STEP_SUMMARY"}
cases = {
    "B-P1-03": 'Example `` unmatched\n\nexport const X=()=> <div className="outline-none"/>;\n\nLater `` delimiter\n',
    "B-P1-03-control": 'Example `` unmatched\n\nexport const X=()=> <div className="outline-none"/>;\n',
    "B-P2-13-start": '`<div className={`\n\n다른 인용: `outline-none`\n',
    "B-P2-13-prefix-control": '문법 예시: `<div className={`\n\n다른 인용: `outline-none`\n',
    "B-P2-13-triple": '문법 예시: ```<div className={```\n\n다른 인용: `outline-none`\n',
    "B-P2-13-double-control": '문법 예시: ``<div className={``\n\n다른 인용: `outline-none`\n',
}
with tempfile.TemporaryDirectory(prefix="t103-post8-b-") as directory:
    target = Path(directory)
    for name, source in cases.items():
        (target / "Page.mdx").write_text(source, encoding="utf8")
        result = subprocess.run(
            [sys.executable, "-B", "-X", "utf8",
             str(root / "tools/ux_lint.py"), "--root", str(target),
             "--fail-new", "--json"], cwd=target, env=env,
            capture_output=True, text=True, encoding="utf8")
        output = json.loads(result.stdout)
        print(name, result.returncode, output["status"],
              len(output["findings"]))
```

양 OS 관찰값은 순서대로 `0 PASS 0`, `1 FAIL 1`, `1 FAIL 1`, `0 PASS 0`, `1 FAIL 1`, `0 PASS 0`이다. 위 코드는 실제 실행한 두 독립 probe의 여섯 사례를 한 파일로 묶은 재실행용이며, 묶음 자체는 추가 실행하지 않았다.

## 누적 finding disposition

과거 raw 본문을 읽지 않고 동일 입력 corpus를 현재 후보에서 다시 실행했다.

| ID | 판정 | 이번 확인 |
|---|---|---|
| B-P1-01 | FIXED | 외부 root/CWD에서 diff 대상 신규 위반 검출 |
| B-P1-02 | FIXED | prepend가 baseline 기존 건수를 소비하지 않음 |
| B-P1-03 | OPEN | 문단 밖 delimiter 잔여 누락; 위 최소 재현 |
| B-P1-04 | FIXED | 경로/값, argparse, JSON/Markdown/summary 합성 marker 비노출 |
| B-P2-05 | FIXED | 명시한 muted 읽기 쌍을 검사하고 임계값 미달 차단 |
| B-P2-06 | FIXED | 잘못된 숫자/schema, 거대 정수, 깊은 JSON 입력 오류 2 |
| B-P3-07 | FIXED | 앱 예시 건수 4/8/8/4, geo 8과 문서 일치 |
| B-P1-08 | FIXED | diff의 실제 추가 내용 `+++` 처리 |
| B-P1-09 | FIXED | media/specificity/source order, string/comment/nested 조건 반례 |
| B-P2-10 | FIXED | airport 현재 측정 1.32와 역사 1.15 구분 |
| B-P1-11 | FIXED | selector quoted-space/case, 지원 외 selector 오류 2 |
| B-P1-12 | FIXED | 빈 selector list 3종 오류 2, root descendant 오류 2 |
| B-P2-13 | NEW | 위치 0/3자 inline 문서 오탐; 위 최소 재현 |

## 실행 명령과 결과

Windows Python은 `3.14.3`, WSL은 `3.11.15`이다. WSL 실행기는 `/home/digitie/.local/share/uv/python/cpython-3.11-linux-x86_64-gnu/bin/python3.11`이다. 아래 Python 명령은 각각 이 런타임으로 실행했다.

| 명령/검증 | Windows | WSL |
|---|---|---|
| `python -B -X utf8 -m unittest discover -s tests -p test_*.py` | 286개 실행, 286 성공, skip 0, 83.482초 | 286개 수집, 283 실행/성공, skip 3, 23.099초 |
| `python -B -X utf8 -m unittest tests.test_kt_contrast tests.test_ux_lint -v` | 48 성공, skip 0, 11.271초 | 48 성공, skip 0, 6.861초 |
| `python -B -X utf8 tools/validate_plan.py` | task 106, 오류 0 | 동일 |
| `python -B -X utf8 tools/validate_document_links.py` | 문서 416, 대상 2412, 오류 0 | 동일 |
| `python -B -X utf8 tools/check_spdx.py` | 56개, 오류 0 | 동일 |
| `python -B -X utf8 tools/scan_secrets.py --all` | 548개, 검출 0 | 동일 |
| `python -B -X utf8 tools/check_prod_redaction.py --all` | 548개, 검출 0 | 동일 |
| `python -B -X utf8 tools/check_versions.py --self-check` | exit 0, registry 자체 검사 | 동일 |
| `python -B -X utf8 tools/check_aliases.py packages/tokens/aliases` | CSS 1개, 오류 0 | 동일 |
| aliases 집중 unittest | 35 성공, skip 0 | 35 수집, 34 성공, skip 1 |
| `python -B -X utf8 tools/kt_contrast.py packages/tokens/tokens.css --json` | exit 0, 27쌍 | 동일 |
| `python -B -X utf8 tools/ux_lint.py --root tests/fixtures/ux --json` | 보고 모드 exit 0, 12 findings | 동일 |
| `git diff --check 94ca2f1730b270721eb6242bfcdd9362b51d45e5 559a9e8a0e49feca2dab9d59df29039bbb0acfd3` | exit 0, 빈 출력 | 별도 실행하지 않음 |

전체 unittest는 출력 축약을 위해 manifest의 `-v`만 생략했으며 수집 범위는 같다. WSL skip 3개는 Windows 8.3 전용 1개와 설치되지 않은 `jsonschema` 의존 시험 2개다. skip을 성공 건수에 넣지 않았다. 격리 실행 보조기는 후보 밖 `.git/codex-audit/review-t102-b-wsl-unittest.py` 및 `review-t102-post-b-gates.py`이며 후보 경로를 인자로 넘겨 위 명령을 실행했다.

직접 실패 주입은 후보 밖의 `t103-post1-b-originals.py`, `t103-b-edge.py`, `t103-post1-b-new.py`, `t103-post3-b-new.py`, `t103-post4-b-new.py`, `t103-post5-b-new.py`, `t103-post6-b-new.py`, `t103-post7-b-new.py`, `t103-post8-b-new.py`를 각각 두 런타임의 `python -B -X utf8 <probe> <현재 후보 경로>`로 실행했다. 초기 task 이름이 남은 보조기 파일명은 검토 코드 기준선이 아니며 모든 입력 root는 이번 후보였다.

- CSS: 정상 light/dark 각각 27쌍, 현재 airport line/page 실제 비율 `1.3209340364487114`; dark media 공백/축약 두 표기는 light PASS와 dark FAIL로 동일하다. `not all`/width 복합 조건은 두 모드 모두 입력 오류 2다. 중첩 조건·root.dark·specificity/source order·문자열·주석·selector case/인용 공백·빈 목록/descendant corpus를 실행했다.
- MDX: 배열·삼항·임의 tag·중첩 object·다중행·blockquote JSX·들여쓰기 없는 ESM·보간 주석·escaped interpolation·fence run 길이/suffix·tilde fence·1/2자 span corpus를 실행했다. 잔여/신규 예외는 위 두 finding에 한정해 기록했다.
- 오류: huge integer/deep JSON, baseline 숫자형/필드 오류, argparse 값, symlink root, diff 추가 행, 경로·값 redaction을 재현했다. 합성 marker는 분할 생성하고 stdout/JSON/Markdown/`GITHUB_STEP_SUMMARY`에는 원문 비노출을 확인했다.
- 문서: task는 `IN_PROGRESS`; 실제 앱 채택/T-010·소비자 검증은 `NOT_RUN`으로 유지한다. geo 건수와 airport 재현/역사 값, GPL 및 common 전용 범위를 확인했다. 도구 성공을 소비자 e2e나 게시 성공으로 바꾼 근거는 발견하지 않았다.

## 미실행과 한계

- `NOT_RUN(Windows Python 3.11이 이 호스트에 없음)`; Windows 3.14 결과로 대체해 표기했다.
- `NOT_RUN(WSL jsonschema 미설치)` 2개, `NOT_RUN(WSL에서 Windows 8.3 전용)` 1개; WSL 전체 시험의 skip 3에 해당한다.
- `NOT_RUN(원격 CI 독립 조회)`; coordinator/로컬 성공을 exact 후보의 CI 성공으로 집계하지 않았다.
- `NOT_RUN(소비자 저장소 build/e2e, registry/npm/PyPI 게시, workflow dispatch는 요청 범위 밖)`; 관련 앱 이관/게시 gate는 이 리뷰로 해제하지 않는다.
- `NOT_RUN(실제 MDX compiler/browser 실행)`; CLI의 문서 제외/실행 영역 계약 및 최소 문자열 대조로 판정했다.
- 종료 SHA/tree/status를 확인한 뒤 이 원본 파일만 별도 커밋한다. 제품 검토 기준선과 보고서 추가 commit은 서로 다른 SHA이며, 보고서 commit SHA와 파일 SHA256은 coordinator에게 별도로 전달한다.
