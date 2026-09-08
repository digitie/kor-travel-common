# T-103 수정 후 12차 독립 적대적 리뷰 B 원본

## 실행 식별·기준선·격리

- 실행 ID: `T103-POST12-B-20260908-115857-KST`.
- 시작: `2026-09-08T11:58:57.9193955+09:00`; 제품 검토 종료: `2026-09-08T12:02:15.0114608+09:00`.
- 시작/종료 제품 HEAD: `386d815f54b79102954a695b0d65dda093bdfbec`.
- 시작/종료 제품 tree: `1236efa499a5a8fd75198745e4e3161f39cfcf33`.
- 시작/종료 `git status --porcelain=v1`: 모두 빈 출력, clean. 종료 확인 뒤 본 원본 파일만 추가한다.
- manifest commit: `3afc47080c752490b8163d69938f0e28a049540f`; 경로 `docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-12-manifest.md`. `git show`로 전체를 읽었다. Git blob SHA256: `26a049c142c8d08b9fc25dd932c822c65e1c64275862512ca1be97af45597614`.
- 이전 제품 `c0c93c47e5f25aa0879fd0fb4e56261f6f624138` 대비 5개 경로 변경 중 이전 manifest와 A/B raw는 경로·통계를 확인했다. 상대 raw 본문은 읽지 않았다. `tools/ux_lint.py`, `tests/test_ux_lint.py` 전체 diff와 현재 관련 코드·문서를 직접 검토했다.
- manifest의 diff check base `e47f48e`는 `e47f48e6a61c8c3275d5392418a65035e6957daf`로 해석해 사용했다.
- 격리: `F:/dev/kor-travel-common-wt/review-t103-post12-b` detached worktree. 전체 unittest·정적 gate는 후보의 독립 임시 Git 사본에서 `GIT_*` 상속을 제거해 실행했다. 직접 입력은 후보 밖 임시 디렉터리에 생성했다.
- source `.git/config` 시작/종료 SHA256: `0A0F849E7874CF0A25926856F9D2E381CCBF4C2DCB5999869C57B86E0F5BEB5B`, 불변. 후보·manifest·소비자·Git 설정을 수정하지 않았고 push하지 않았다.
- 이번 상대 결과와 과거 raw 본문을 읽지 않았다. manifest의 식별 메타데이터는 raw 본문 열람과 구분한다. 검증 결과는 모두 이번 후보에서 새로 실행했다.

## 요청 원문

> T-103 post-fix-12 독립 적대적 리뷰를 시작해 주세요. 제품 candidate는 commit 386d815f54b79102954a695b0d65dda093bdfbec, tree 1236efa499a5a8fd75198745e4e3161f39cfcf33로 detached clean checkout하고, 공통 manifest는 commit 3afc470의 docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-12-manifest.md를 git show로 읽으세요. 상대 reviewer의 이번 raw/결과나 미확정 raw를 읽지 말고 후보·manifest·소비자 저장소·git config를 수정하지 마세요. Windows Python 3.14와 WSL Python 3.11에서 full/focused/static gate와 누적 CSS/JSON/redaction/diff/symlink/airport corpus, 특히 미종결 1/2자 Markdown span 뒤 직접/단항(!)/키워드(void)/논리(true &&)/숫자(1 &&)/주석 선행({/* ... */ window.confirm}, //) MDX expression, 여러 줄 JSX expression, 정상 닫힌 span/음성 대조를 독립 재현하세요. Windows Python 3.11은 NOT_RUN으로 명시하세요. 새 원본만 docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-12-reviewer-b.md에 기록하고 immutable raw-only commit/SHA256/HEAD·tree·clean·명령·verdict를 남겨 주세요. 제품 후보는 수정/커밋/푸시하지 마세요. PASS/NO-GO와 모든 finding ID/disposition을 명확히 보고하고 완료 후 메시지를 주세요.

## 최종 판정

**NO-GO. B-P1-03 OPEN.** 직접·단항·키워드·논리·정수·주석 선행 표현식의 기존 반례는 수정됐지만, 실행 문법의 일부만 인정하는 동일한 원인으로 다른 정상 표현식이 누락된다. P0 0건, P1 1건, P2 0건, P3 0건이다. 다른 누적 ID 12개는 이번 재현 범위에서 FIXED다. 아래 변형은 기존 MDX 문맥/마스킹 finding에 귀속하며 신규 ID로 중복 집계하지 않는다.

## B-P1-03 — 재개 문자·식별자 목록 밖 표현식이 계속 가려짐

- 심각도/상태: **P1 / OPEN**.
- 위치: `tools/ux_lint.py:38`·`:39`의 시작/후속 문자 집합, `:152`의 `_looks_like_mdx_expression_start`, `:162`의 ASCII 시작 식별자 정규식.
- 원인: 정규식 리터럴의 `/`와 소수 `.5`의 `.`는 시작 문자 집합에 없고, 식별자 뒤 `/`·`^`는 후속 문자 집합에 없다. 한글 식별자는 `isalpha()`를 통과해도 `[A-Za-z_$]` 정규식에서 탈락한다. 모두 미종결 문서 span의 나머지로 가려져 실행 호출 검사가 재개되지 않는다.
- 최소 입력 `Page.mdx`:

````mdx
Example ` unmatched {/x/.test("x") && window.confirm("확인")}
````

- 명령: `python -B -X utf8 <후보>/tools/ux_lint.py --root <Page.mdx만 있는 임시 디렉터리> --fail-new --json`.
- 실제: Windows 3.14.3·WSL 3.11.15 모두 `exit=0`, `status=PASS`, finding 0개. 기대: 실행 금지 호출 P8 1개, `exit=1`.
- 여는 backtick을 제거한 대조군은 두 OS에서 `exit=1`, P8 1개다. 아래 5개 표현식은 미종결 opener 1자·2자 모두 같은 결과였다.

| 중괄호 안 표현식 | 사전 선언 | opener 없음 | 미종결 1자/2자 각각 |
|---|---|---|---|
| `/x/.test("x") && window.confirm("확인")` | 없음 | exit 1 / P8 1 | exit 0 / 0건 |
| `.5 && window.confirm("확인")` | 없음 | exit 1 / P8 1 | exit 0 / 0건 |
| `n / window.confirm("확인")` | `export const n = 1` | exit 1 / P8 1 | exit 0 / 0건 |
| `n ^ window.confirm("확인")` | `export const n = 1` | exit 1 / P8 1 | exit 0 / 0건 |
| `값 && window.confirm("확인")` | `export const 값 = 1` | exit 1 / P8 1 | exit 0 / 0건 |

사전 선언이 있는 사례는 선언과 빈 줄 뒤에 위 최소 입력 형식의 `Example ... {표현식}`을 넣었다. 미정의 변수에 기대는 반례가 아니다. 정규식·소수·한글 식별자의 조건은 참이므로 호출이 평가되는 표현식이다. 검사기는 코드를 실행하지 않고 소스 패턴을 판정한다.

- 영향: 동일한 `window.confirm` 호출의 앞부분을 바꾸는 것만으로 `--fail-new` 판정이 FAIL에서 PASS로 바뀐다. T-103의 `.mdx`·P8 검사와 실행 코드 보존 계약이 닫히지 않았다.
- 권고/disposition: JavaScript 표현식 시작을 문자/키워드 목록으로 더 열거하는 대신, 유효하게 닫힌 Markdown 인용만 제외하고 미종결 opener 뒤 나머지는 정상 스캐너에 남기는 방식을 우선 검토한다. 무효한 opener만 처리한 뒤 정상 인용·fence·JSX 상태와 일관되게 이어가야 한다. 위 양성·음성 대조를 함께 회귀로 추가해 재검토해야 한다.
- 실제 보조기: 후보 밖 `.git/codex-audit/t103-post12-b-new.py`; `python -B -X utf8 <보조기> <이번 후보 worktree>`로 양 OS에서 실행했다. 위 5개 표현식과 block/line 주석 대조 2개 × opener 0/1/2자의 21개 관찰을 실행했다.

## 누적 finding disposition과 수정 확인

| ID | 판정 | 현재 후보 직접 확인 |
|---|---|---|
| B-P1-01 | FIXED | 외부 root/CWD diff 신규 위반 검출 |
| B-P1-02 | FIXED | prepend가 기존 baseline 건수를 소비하지 않음 |
| B-P1-03 | OPEN | 이전 호출·연산자·여러 줄 JSX 수정; 위 문법 변형 잔여 |
| B-P1-04 | FIXED | 경로/값·argparse·JSON/Markdown/summary marker 비노출 |
| B-P2-05 | FIXED | 추가 muted 읽기 쌍 검사·미달 차단 |
| B-P2-06 | FIXED | baseline 숫자/schema·거대 정수·깊은 JSON 오류 2 |
| B-P3-07 | FIXED | 예제 미달 4/8/8/4와 geo 문서 8 일치 |
| B-P1-08 | FIXED | diff `+++` 실제 추가 내용 검출 |
| B-P1-09 | FIXED | CSS media/specificity/source order/string/comment/nested corpus |
| B-P2-10 | FIXED | airport 1.320934 실측과 역사 1.15 구분 |
| B-P1-11 | FIXED | selector case/quoted-space 경계 오류 2 |
| B-P1-12 | FIXED | 빈 selector 목록·root descendant 오류 2 |
| B-P2-13 | FIXED | 파일 첫 span·3자 inline 문서 및 정상 대조 exit 0 |

현재 후보에서 미종결 1/2자 span 뒤 직접 `window.confirm`, `!`, `void`, `true &&`, `1 &&`는 모두 P8 1개/exit 1이다. `{/* 설명 */ window.confirm(...)}`과 `{// 설명` 다음 줄의 호출도 각 opener 조건에서 P8 1개/exit 1이다. 이전 여러 줄 JSX template은 P6 1개/exit 1이며 정상 닫힌 문서 인용은 0개/exit 0이다.

같은 문단·다음 줄 HTML/JSX, blockquote 빈 문단, CRLF/공백 빈 줄·backslash delimiter·문단 밖 닫는 기호, 배열·삼항·임의 tag·중첩 object·다중행·ESM·JS 주석·fence 길이/suffix·tilde·escaped interpolation을 누적 corpus에서 재실행했다. CSS `.dark/**/:not(.light)`, `.dark/**/.dark`, `:root/**/.dark`, root descendant/빈 목록은 오류 2·traceback 없음이고 root 앞/뒤 주석 대조는 허용된다.

## 실행 명령과 실제 결과

Windows 실행기 `py -3.14`는 Python `3.14.3`이고, WSL `/home/digitie/.local/share/uv/python/cpython-3.11-linux-x86_64-gnu/bin/python3.11`은 `3.11.15`다. 표의 Python 명령은 각각 이 런타임으로 실행했다.

| 명령 | Windows | WSL |
|---|---|---|
| `python -B -X utf8 -m unittest discover -s tests -p test_*.py` | 287 실행/성공, skip 0, 91.530초 | 287 수집, 284 실행/성공, skip 3, 28.464초 |
| `python -B -X utf8 -m unittest tests.test_kt_contrast tests.test_ux_lint -v` | 49 성공, skip 0, 18.477초 | 49 성공, skip 0, 9.220초 |
| `python -B -X utf8 tools/validate_plan.py` | task 106, 오류 0 | 동일 |
| `python -B -X utf8 tools/validate_document_links.py` | 문서 427, 대상 2412, 오류 0 | 동일 |
| `python -B -X utf8 tools/check_spdx.py` | 56개, 오류 0 | 동일 |
| `python -B -X utf8 tools/scan_secrets.py --all` | 559개, 검출 0 | 동일 |
| `python -B -X utf8 tools/check_prod_redaction.py --all` | 559개, 검출 0 | 동일 |
| `python -B -X utf8 tools/check_versions.py --self-check` | exit 0, 소비자 검사 아님 | 동일 |
| `python -B -X utf8 tools/check_aliases.py packages/tokens/aliases` | CSS 1개, 오류 0 | 동일 |
| aliases 집중 unittest | 35 성공, skip 0 | 35 수집, 34 성공, skip 1 |
| `python -B -X utf8 tools/kt_contrast.py packages/tokens/tokens.css --json` | exit 0, 27쌍 | 동일 |
| `python -B -X utf8 tools/ux_lint.py --root tests/fixtures/ux --json` | 보고 모드 exit 0, 12 findings | 동일 |
| `git diff --check e47f48e6a61c8c3275d5392418a65035e6957daf 386d815f54b79102954a695b0d65dda093bdfbec` | exit 0 | 명시적 Git 경로로 exit 0 |

전체 unittest는 출력 축약을 위해 manifest의 `-v`만 생략했으며 수집 범위는 같다. 후보 밖 `review-t102-b-wsl-unittest.py`와 `review-t102-post-b-gates.py`에 이번 후보 경로를 주어 임시 독립 사본에서 위 명령을 실행했다. WSL diff는 `git --git-dir=/mnt/f/dev/kor-travel-common/.git --work-tree=/mnt/f/dev/kor-travel-common-wt/review-t103-post12-b diff --check <고정 base> <고정 candidate>`로 실행했으며 Git 설정을 쓰지 않았다.

기존 probe 9개를 `t103-post9-b-corpus.py`로 실행한 105개 관찰값은 양 OS에서 완전히 일치하고 모든 marker/traceback 검출 불리언은 false다. 별도의 `t103-post9-b-new.py` 21개, `t103-post10-b-new.py` 7개, `t103-post11-b-new.py` 15개, 이번 `t103-post12-b-new.py` 21개 관찰도 각 OS에서 실행했다. 이 건수는 unittest 성공 건수와 합산하지 않는다. CSS/media 8개 조건/모드 대조와 smoke도 같았으며 airport 실제 비율은 `1.3209340364487114`, 4앱 예제 미달은 4/8/8/4였다.

현재 문서의 T-103 `IN_PROGRESS`, 소비자·T-010 `NOT_RUN`, airport 역사/현행 값, GPL-3.0-or-later와 common 전용 경계를 확인했다. 제품 delta에는 소비자·공개 패키지·CI 변경이 없다. 상태/evidence 관련 추가 finding은 발견하지 않았다.

## NOT_RUN과 한계

- `NOT_RUN(Windows Python 3.11 미설치)`; `py -0p`는 3.14/3.10을 반환했다.
- `NOT_RUN(WSL jsonschema 미설치)` 2개와 `NOT_RUN(WSL의 Windows 8.3 전용 시험)` 1개가 전체 unittest skip 3개다. 성공 건수에서 제외했다.
- `NOT_RUN(원격 CI 독립 조회)`; 로컬 결과를 exact 후보 CI 성공으로 집계하지 않았다.
- `NOT_RUN(소비자 build/e2e·npm/PyPI registry/게시·workflow dispatch는 사용자/manifest 범위 밖)`; 외부 소비자·릴리스 gate를 해제하지 않는다.
- `NOT_RUN(MDX compiler/browser 실행)`; 로컬 CLI 계약·최소 입력·대조군에 근거한 판정이다.
- 제품 종료 SHA/tree/clean 확인 뒤 본 원본 한 파일만 별도 commit한다. 보고서 commit SHA와 파일/Git blob SHA256은 제품 기준선과 구분해 coordinator에게 전달한다.
