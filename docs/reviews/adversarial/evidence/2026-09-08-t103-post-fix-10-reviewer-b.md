# T-103 수정 후 10차 독립 적대적 리뷰 B 원본

## 기준선과 격리

- 실행 ID: `T103-POST10-B-20260908-113332-KST`.
- 시작: `2026-09-08T11:33:32.5535032+09:00`; 제품 검토 종료: `2026-09-08T11:36:39.2949799+09:00`.
- 시작/종료 제품 HEAD: `f6ea446547c4e71ffb272b9623729396d6ef7185`.
- 시작/종료 제품 tree: `f3b3b90d87d758d22917c7e729ec3e25c2fe06c3`.
- 시작/종료 `git status --porcelain=v1`: 빈 출력, clean. 종료 확인 뒤 본 원본 파일만 추가한다.
- 최신 manifest: `bd73856ac1d3327b1fe46acc352163eee23ad504`의 `docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-10-manifest.md`; `git show`로 전체를 읽었다. Git blob SHA256: `10cf1119900a0259bb5b3a7fb818c30a8309a6d70d1fe41b9b7bdd5b9085c5ad`.
- delta base: `e4b8fe3ff62c404660363f6751eda52428cf554c`. 변경 3개 파일은 이전 manifest와 `tools/ux_lint.py`, `tests/test_ux_lint.py`다. 두 제품 파일의 전체 diff와 현재 관련 문서·도구를 직접 확인했다.
- 격리: `F:/dev/kor-travel-common-wt/review-t103-post10-b` detached worktree. 전체 unittest/정적 gate는 이 후보의 독립 임시 사본에 Git 저장소를 초기화하고 `GIT_*` 환경을 제거해 실행했다. 직접 probe 입력은 후보 밖 임시 디렉터리에만 썼다.
- 기본 checkout `.git/config` 검토 전/후 SHA256: `0A0F849E7874CF0A25926856F9D2E381CCBF4C2DCB5999869C57B86E0F5BEB5B`, 불변. 제품·manifest·소비자·Git 설정을 수정하거나 push하지 않았다.
- 상대 결과와 과거 raw 본문은 읽지 않았다. manifest에 적힌 raw 식별 메타데이터는 본문 열람과 구분한다. B의 post-fix-09는 raw 생성/커밋 전에 중단되어 완료 evidence로 채택하지 않는다. 이번 결과는 최신 manifest를 읽은 뒤 새로 실행한 검증에 근거한다.

## 요청 원문

> 이제 post-fix-10을 최신 manifest에서 다시 시작해 주세요. 후보는 commit `f6ea446547c4e71ffb272b9623729396d6ef7185`, tree `f3b3b90d87d758d22917c7e729ec3e25c2fe06c3`, 최신 manifest commit `bd73856ac1d3327b1fe46acc352163eee23ad504`입니다. 상대 결과·과거 raw 본문은 읽지 말고 독립 full/focused/static 검증을 Windows 3.14·WSL 3.11에서 수행하세요. Windows 3.11은 NOT_RUN. 새 raw `docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-10-reviewer-b.md`만 추가해 immutable commit/SHA256/verdict를 보고하고 후보/manifest는 수정하지 마세요. 누적 CSS comment-gap와 MDX 모든 반례(같은 문단 미종결 span 뒤 HTML/JSX, blockquote 빈 문단, 파일 첫/3자 span, backslash delimiter)를 확인하세요.

## 판정

**NO-GO.** 기존 **B-P1-03 OPEN**: 미종결 span 뒤 실행 영역 누락의 두 하위 반례가 남는다. P0 0건, P1 1건, P2 0건, P3 0건이다. B-P2-13과 다른 누적 ID 11개는 이번 재현 범위에서 FIXED다. 아래 하위 반례는 동일한 기존 MDX 문맥/마스킹 finding에 귀속하며 별도 신규 ID로 중복 집계하지 않는다.

## B-P1-03 잔여 A — MDX 표현식 시작점을 누락

- 위치: `tools/ux_lint.py:128`, 특히 `:133`의 `_mask_unclosed_inline_span` 재개 정규식.
- 원인: 미종결 inline span 이후 `<태그` 또는 일부 줄 시작 선언만 실행 시작점으로 찾는다. MDX의 `{표현식}`은 재개 대상으로 찾지 않아 문단 끝까지 가린다.
- 입력 A1:

````mdx
Example ` unmatched {window.confirm("확인")}
````

- 입력 A2: A1의 여는 backtick 한 자를 두 자로 바꾼다. 닫는 backtick은 없다.
- 실행: `python -B -X utf8 <후보>/tools/ux_lint.py --root <Page.mdx만 있는 임시 디렉터리> --fail-new --json`.
- 실제: Windows/WSL 모두 A1·A2 `exit=0`, `status=PASS`, finding 0개. 기대: 실행 `window.confirm`을 P8로 검출해 `exit=1`, finding 1개.
- 대조: `Example {window.confirm("확인")}`는 양 OS에서 `exit=1`, P8 1개다. 표현식 전체를 정상적으로 닫힌 backtick으로 감싼 문서 인용은 `exit=0`, 0개다.
- 영향: 미종결 문서 기호가 실제 실행될 수 있는 UX 금지 호출을 정상 판정으로 바꾼다. T-103의 `.mdx` 검사·실행 코드 보존·`--fail-new` 계약을 충족하지 못한다.
- 권고: 유효하게 닫힌 문서 인용만 제외하고, 닫히지 않은 opener가 임의의 뒤 코드를 통째로 숨기지 않게 한다. 실행 재개 대상에 태그 형태만 추가하는 대신 MDX 표현식 문맥과 Markdown 문맥을 일관되게 판정해야 한다.

## B-P1-03 잔여 B — 재개한 여러 줄 JSX를 다시 문서 span으로 오인

- 위치: `tools/ux_lint.py:133`의 재개 처리, `:153`의 `_has_open_inline_span` 호출 및 `:244`의 원문 span 상태 탐색.
- 최소 입력:

````mdx
Example `` unmatched
<div className={
 [`outline-none`].join(" ")
}/>
````

- 명령은 잔여 A와 동일하다. 실제: 양 OS에서 `exit=0`, `status=PASS`, finding 0개. 기대: 실행 JSX template의 `outline-none`을 P6로 검출해 `exit=1`, 1개.
- 대조: 첫 줄의 두 backtick을 제거하면 `exit=1`, P6 1개다. 첫 줄을 단일 backtick으로 바꾼 대조도 P6 1개를 검출했다.
- 원인: `<div`를 찾아 검사를 재개하지만 JSX 문맥을 판단할 때 가리기 전 원문을 다시 읽는다. 앞의 미종결 두 backtick 때문에 실제 `className={`를 문서 span 안이라고 간주해 버린다. 단순 문자열 속성은 복구됐지만 여러 줄 template 경로는 닫히지 않았다.
- 영향/권고: 접근성 위반이 `--fail-new`를 우회한다. 실행 문맥과 문서 span 상태를 공유해 재개 이후의 JSX를 원래 미종결 문서 문맥으로 되돌리지 않게 해야 한다. A/B의 양성·음성 대조를 모두 회귀로 추가한 후 독립 재검토가 필요하다.

## 반례 실행 보존

실제 후보 밖 `.git/codex-audit/t103-post10-b-new.py`로 위 반례와 대조군 7개를 각각 두 런타임에서 실행했다. 실행 형식은 `python -B -X utf8 <probe.py> <이번 후보 worktree>`이며, 내부 명령은 위 `ux_lint.py --root ... --fail-new --json`이다. 파일별로 `Page.mdx` 하나만 만들어 검사했다. 재현을 위한 핵심 입력/관찰값은 다음과 같다(`\n`은 실제 개행으로 저장).

| 사례 | 입력 | exit / 규칙 건수 |
|---|---|---|
| A1 | `Example ` + backtick 1자 + ` unmatched {window.confirm("확인")}\n` | 0 / 0 |
| A2 | A1에서 backtick 2자 | 0 / 0 |
| A 정상 코드 | `Example {window.confirm("확인")}\n` | 1 / P8 1 |
| A 문서 인용 | `Example ` 뒤 표현식을 정상 backtick 한 쌍으로 감쌈 | 0 / 0 |
| B | 위 여러 줄 최소 입력 | 0 / 0 |
| B 정상 코드 | B의 첫 두 backtick 제거 | 1 / P6 1 |
| B 단일 opener | B의 첫 두 backtick을 한 자로 변경 | 1 / P6 1 |

## 누적 ID와 이번 수정 대조

| ID | disposition | 현재 후보 직접 확인 |
|---|---|---|
| B-P1-01 | FIXED | 외부 root/CWD의 diff 신규 위반 검출 |
| B-P1-02 | FIXED | prepend가 baseline 기존 건수를 소모하지 않음 |
| B-P1-03 | OPEN | 위 A/B 잔여; 나머지 MDX corpus는 아래 확인 |
| B-P1-04 | FIXED | 경로/값·argparse·JSON/Markdown/summary marker 비노출 |
| B-P2-05 | FIXED | 추가 muted 읽기 쌍의 미달 차단 |
| B-P2-06 | FIXED | baseline 숫자·schema·거대 정수·깊은 JSON 오류 2 |
| B-P3-07 | FIXED | 4앱 미달 건수 4/8/8/4와 geo 문서 8 일치 |
| B-P1-08 | FIXED | diff `+++` 실제 추가 내용 검사 |
| B-P1-09 | FIXED | media·specificity·source order·string/comment/nested corpus |
| B-P2-10 | FIXED | airport 1.320934 실측과 역사 1.15 구분 |
| B-P1-11 | FIXED | selector case/quoted-space 경계 오류 2 |
| B-P1-12 | FIXED | 빈 selector 목록 및 root descendant 오류 2 |
| B-P2-13 | FIXED | 파일 첫 span·3자 inline 문서 및 대조군 exit 0 |

- 이번 요청의 동일 문단 미종결 1/2자 뒤 단순 HTML/JSX 문자열 속성, 바로 다음 줄 JSX, blockquote 빈 문단, 공백을 포함한 빈 문단, CRLF, backslash 뒤 닫는 delimiter를 모두 재실행했다. 각 실행 코드에서 P6 1개/exit 1이며 닫힌 문서 인용은 exit 0이다.
- CSS `.dark/**/:not(.light)`, `.dark/**/.dark`, `:root/**/.dark`, root descendant와 comment-gap 목록은 일반 오류 2/traceback 없음이다. root 선택자 앞/뒤 주석의 정상 대조는 허용된다.
- 배열·삼항·임의 tag·중첩 object·다중행·blockquote JSX·ESM, JS 중괄호 주석, fenced/tilde/fence 길이·suffix, escaped interpolation 및 기존 문서 제외 corpus를 현재 후보에서 반복 실행했다. 위 잔여는 이 범위에 추가한 조합 반례다.

## 검증 명령과 실제 결과

Windows `py -3.14`는 Python `3.14.3`, WSL 실행기는 `/home/digitie/.local/share/uv/python/cpython-3.11-linux-x86_64-gnu/bin/python3.11`이며 `3.11.15`다. 표의 Python 명령은 각각 이 런타임으로 실행했다.

| 명령 | Windows | WSL |
|---|---|---|
| `python -B -X utf8 -m unittest discover -s tests -p test_*.py` | 287 실행/성공, skip 0, 92.100초 | 287 수집, 284 실행/성공, skip 3, 25.537초 |
| `python -B -X utf8 -m unittest tests.test_kt_contrast tests.test_ux_lint -v` | 49 성공, skip 0, 19.778초 | 49 성공, skip 0, 9.973초 |
| `python -B -X utf8 tools/validate_plan.py` | task 106, 오류 0 | 동일 |
| `python -B -X utf8 tools/validate_document_links.py` | 문서 420, 대상 2412, 오류 0 | 동일 |
| `python -B -X utf8 tools/check_spdx.py` | 56개, 오류 0 | 동일 |
| `python -B -X utf8 tools/scan_secrets.py --all` | 552개, 검출 0 | 동일 |
| `python -B -X utf8 tools/check_prod_redaction.py --all` | 552개, 검출 0 | 동일 |
| `python -B -X utf8 tools/check_versions.py --self-check` | exit 0, 소비자 검사 아님 | 동일 |
| `python -B -X utf8 tools/check_aliases.py packages/tokens/aliases` | CSS 1개, 오류 0 | 동일 |
| aliases 집중 unittest | 35 성공, skip 0 | 35 수집, 34 성공, skip 1 |
| `python -B -X utf8 tools/kt_contrast.py packages/tokens/tokens.css --json` | exit 0, 27쌍 | 동일 |
| `python -B -X utf8 tools/ux_lint.py --root tests/fixtures/ux --json` | 보고 모드 exit 0, 12 findings | 동일 |
| `git diff --check 94ca2f1730b270721eb6242bfcdd9362b51d45e5 f6ea446547c4e71ffb272b9623729396d6ef7185` | exit 0 | 명시적 Git 경로로 exit 0 |

전체 unittest는 출력 축약을 위해 manifest의 `-v`만 생략했다. 전체 수집 범위는 동일하다. 임시 Git 사본 실행 보조기는 후보 밖 `review-t102-b-wsl-unittest.py`, `review-t102-post-b-gates.py`이며 현재 후보 경로를 인자로 사용했다. 기본 Git 설정을 변경하지 않는다. WSL의 Windows worktree 직접 `git diff` 호출은 Windows 절대 `.git` 포인터를 해석하지 못해 실패했으며 그 실행을 성공으로 집계하지 않았다. 이후 `git --git-dir=/mnt/f/dev/kor-travel-common/.git --work-tree=/mnt/f/dev/kor-travel-common-wt/review-t103-post10-b diff --check <고정 base> <고정 candidate>`의 읽기 전용 재실행이 exit 0이었다.

기존 독립 probe 9개를 `t103-post9-b-corpus.py`로 현재 후보에 실행한 관찰값 105개가 양 OS에서 완전히 일치했다. 이는 unittest 건수가 아닌 probe 관찰값이다. 모든 `marker`·`traceback` 검출 불리언은 false다. 별도의 `t103-post9-b-new.py` 21개 관찰과 `t103-post10-b-new.py` 7개 관찰도 양 OS에서 실행했다. CSS/media smoke의 8개 조건/모드 결과도 같았고 airport는 `1.3209340364487114`, 4앱 미달 건수는 4/8/8/4였다.

문서에서는 T-103 `IN_PROGRESS`, 실제 앱 검증/T-010 `NOT_RUN`, GPL-3.0-or-later 및 common 전용 실행 경계를 확인했다. 제품 delta에는 소비자·패키지 공개 API·CI 변경이 없고 이전 검증을 새 CI 성공으로 선언한 변경도 없다. 과거 raw 원문은 검증 자료로 읽지 않았다.

## NOT_RUN과 한계

- `NOT_RUN(Windows Python 3.11 미설치)`; `py -0p`는 3.14/3.10만 반환했다.
- `NOT_RUN(WSL jsonschema 미설치)` 2개와 `NOT_RUN(WSL의 Windows 8.3 전용 시험)` 1개가 전체 unittest skip 3개다. 성공 건수에서 제외했다.
- `NOT_RUN(원격 CI 독립 조회)`; 로컬 결과는 exact 후보 CI 성공 evidence가 아니다.
- `NOT_RUN(소비자 build/e2e, npm/PyPI registry·게시, workflow dispatch는 사용자/manifest 범위 밖)`; 실제 소비자/릴리스 gate를 해제하지 않는다.
- `NOT_RUN(MDX compiler/browser 실행)`; 로컬 CLI의 문서 제외·실행 코드 보존 계약과 최소 입력/대조군에 근거한 판정이다.
- 본 원본만 별도 commit한다. 제품 종료 SHA/tree와 보고서 추가 commit은 구분하며, 보고서-only commit SHA와 파일/Git blob SHA256은 coordinator에게 별도로 전달한다.
