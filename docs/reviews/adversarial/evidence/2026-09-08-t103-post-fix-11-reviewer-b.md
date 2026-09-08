# T-103 수정 후 11차 독립 적대적 리뷰 B 원본

## 실행 식별·기준선·격리

- 실행 ID: `T103-POST11-B-20260908-114726-KST`.
- 시작: `2026-09-08T11:47:26.1668995+09:00`; 제품 검토 종료: `2026-09-08T11:50:23.6311946+09:00`.
- 시작/종료 제품 HEAD: `c0c93c47e5f25aa0879fd0fb4e56261f6f624138`.
- 시작/종료 제품 tree: `f9b16a3d03f3fca49ba8048cc9d0328e78aadda4`.
- 시작/종료 `git status --porcelain=v1`: 모두 빈 출력, clean. 종료 확인 뒤 이 원본 파일만 추가한다.
- manifest commit: `f21b2007de2613fb507f8df843ad50125a38b4c3`; 경로 `docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-11-manifest.md`. `git show`로 전체를 읽었다. Git blob SHA256: `d8ceb2c722406267ab3e7ce0e3e03de3f70a7b293f81fcbefc303e066ed553a4`.
- manifest의 delta base `bd73856ac1d3327b1fe46acc352163eee23ad504`와 비교했다. 변경 4개 경로 중 과거 A/B raw 2개는 경로·통계만 확인하고 본문을 읽지 않았다. 제품 변경 `tools/ux_lint.py`, `tests/test_ux_lint.py`의 전체 diff와 필요한 현재 코드·문서를 직접 검토했다.
- 격리: `F:/dev/kor-travel-common-wt/review-t103-post11-b` detached worktree. 전체 unittest와 정적 gate는 후보를 임시 사본에 복사한 독립 Git 저장소에서 `GIT_*` 상속을 제거해 실행했다. 직접 반례는 후보 밖 임시 디렉터리에 생성했다.
- source `.git/config` 시작/종료 SHA256: `0A0F849E7874CF0A25926856F9D2E381CCBF4C2DCB5999869C57B86E0F5BEB5B`, 불변. 후보·manifest·소비자·Git 설정을 수정하지 않았고 push하지 않았다.
- 상대 reviewer의 이번 결과나 과거 raw 본문을 읽지 않았다. manifest의 raw 식별 메타데이터 열람과 raw 본문 열람은 구분한다. 아래 검증은 모두 이번 제품 후보에서 새로 실행했다.

## 요청 원문

> T-103 post-fix-11 독립 적대적 리뷰를 시작해 주세요. 반드시 동일한 immutable candidate commit c0c93c47e5f25aa0879fd0fb4e56261f6f624138, tree f9b16a3d03f3fca49ba8048cc9d0328e78aadda4, manifest docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-11-manifest.md (commit f21b200)만 기준으로 사용하세요. 상대 reviewer의 이번 raw/결과나 미확정 raw를 읽지 말고, 후보·manifest·소비자 저장소·git config를 수정하지 마세요. Windows Python 3.14와 WSL Python 3.11에서 full/focused/static gate와 누적 CSS/JSON/redaction/diff/symlink/airport corpus, 특히 미종결 1/2자 Markdown span 뒤 {window.confirm(...)}와 여러 줄 JSX expression 최소 반례 및 양성/음성 대조를 독립 재현하세요. Windows Python 3.11은 NOT_RUN으로 명시하세요. 새 원본만 docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-11-reviewer-b.md에 기록하고 immutable commit/SHA256/HEAD·tree·clean·명령·verdict를 남겨 주세요. 제품 후보가 아닌 raw evidence commit만 생성하세요. PASS/NO-GO와 모든 finding ID/disposition을 명확히 보고하고 완료 후 메시지를 주세요.

## 최종 판정

**NO-GO. B-P1-03 OPEN.** 이전 직접 호출·여러 줄 JSX 최소 반례는 FIXED지만, 같은 미종결 span 뒤 단항/논리 표현식의 금지 호출은 여전히 누락된다. P0 0건, P1 1건, P2 0건, P3 0건이다. 다른 누적 ID 12개는 이번 재현 범위에서 FIXED다. 같은 원인·계약을 공격한 표현식 변형은 B-P1-03의 잔여로 유지하고 신규 ID로 중복 집계하지 않는다.

## B-P1-03 — 표현식의 첫 연산자에 따라 미종결 span 뒤 코드를 숨김

- 심각도/상태: **P1 / OPEN**.
- 위치: `tools/ux_lint.py:128` `_mask_unclosed_inline_span`, 특히 `:137`의 표현식 시작 정규식과 `:142`의 문단 끝 fallback.
- 원인: `{` 뒤 식별자+일부 구두점 또는 `[`, `(`, `<`만 표현식 시작으로 인정한다. `!`, `void`, `true &&`, `1 &&`로 시작하는 정상 표현식은 재개 대상으로 인식하지 못해 남은 문단 전체를 가린다. JS 표현식 문법의 일부분만 나열한 휴리스틱이 문서 제외 여부를 결정한다.
- 최소 입력 `Page.mdx`:

````mdx
Example ` unmatched {!window.confirm("확인")}
````

- 명령: `python -B -X utf8 <후보>/tools/ux_lint.py --root <Page.mdx만 있는 임시 디렉터리> --fail-new --json`.
- 실제: Windows 3.14.3와 WSL 3.11.15 모두 `exit=0`, `status=PASS`, finding 0개.
- 기대: 실행 `window.confirm`을 P8로 검출해 `exit=1`, finding 1개. 여는 backtick을 제거한 같은 표현식은 두 OS에서 실제 P8 1개/exit 1이다.
- 추가 직접 재현: 여는 backtick 1자·2자 각각에 대해 아래 네 표현식 모두 같은 누락이다. 닫는 backtick은 없다.

| 중괄호 안 표현식 | opener 없음 대조 | 미종결 1자 | 미종결 2자 |
|---|---|---|---|
| `!window.confirm("확인")` | exit 1 / P8 1 | exit 0 / 0건 | exit 0 / 0건 |
| `void window.confirm("확인")` | exit 1 / P8 1 | exit 0 / 0건 | exit 0 / 0건 |
| `true && window.confirm("확인")` | exit 1 / P8 1 | exit 0 / 0건 | exit 0 / 0건 |
| `1 && window.confirm("확인")` | exit 1 / P8 1 | exit 0 / 0건 | exit 0 / 0건 |
| `window.confirm("확인")` | exit 1 / P8 1 | exit 1 / P8 1 | exit 1 / P8 1 |

- 영향: 같은 금지 호출 앞에 단항/논리 연산자를 놓으면 `--fail-new`가 정상 판정으로 바뀐다. T-103의 `.mdx` 대상·실행 코드 보존·P8 금지 호출 판정 계약을 충족하지 못한다.
- 권고/disposition: 유효하게 닫힌 Markdown 인용만 제외하고 미종결 opener 뒤 내용은 정상 스캐너에 남기는 방식을 우선 검토한다. 실행 시작 문법을 한 연산자씩 열거해 보완하는 방식은 같은 누락을 반복한다. 여는 delimiter를 무효한 일반 텍스트로 처리하는 상태와 정상 인용·fence·JSX 상태를 일관되게 관리하고, 위 양성/음성 대조를 회귀에 추가해 재검토해야 한다.
- 재현 보조기: 후보 밖 `.git/codex-audit/t103-post11-b-new.py`. `python -B -X utf8 <보조기> <이번 후보 worktree>`로 각 OS에서 실행했다. 5개 표현식 × opener 0/1/2자의 15개 관찰을 위 표에 전부 기록했다. 도구 입력 이외의 외부 호출은 하지 않았다.

## 누적 finding disposition

| ID | 판정 | 이번 후보에서 확인한 근거 |
|---|---|---|
| B-P1-01 | FIXED | 외부 root/CWD diff 신규 위반을 exit 1로 검출 |
| B-P1-02 | FIXED | prepend가 baseline의 기존 건수를 소비하지 않음 |
| B-P1-03 | OPEN | 직접 호출·여러 줄 JSX 이전 반례 수정; 위 연산자 변형 잔여 |
| B-P1-04 | FIXED | 경로/값·argparse·JSON/Markdown/summary 합성 marker 비노출 |
| B-P2-05 | FIXED | 명시한 muted 읽기 표면의 추가 쌍 검사·미달 차단 |
| B-P2-06 | FIXED | baseline 숫자·schema·거대 정수·깊은 JSON 오류 2 |
| B-P3-07 | FIXED | 예제 미달 건수 4/8/8/4, geo 문서 8과 일치 |
| B-P1-08 | FIXED | diff `+++` 실제 추가 내용 검출 |
| B-P1-09 | FIXED | CSS media/specificity/source order·string/comment/nested corpus |
| B-P2-10 | FIXED | airport 1.320934 실측과 역사 1.15 구분 |
| B-P1-11 | FIXED | selector case/quoted-space 경계 입력 오류 2 |
| B-P1-12 | FIXED | 빈 selector 목록·root descendant 입력 오류 2 |
| B-P2-13 | FIXED | 파일 첫 span·3자 inline 문서 인용 및 정상 대조군 exit 0 |

현재 후보에서 이전 직접 `window.confirm` 앞 미종결 1/2자 span은 P8 1개/exit 1이고, 정상 닫힌 인용은 0개/exit 0이다. 미종결 두 backtick 뒤 여러 줄 JSX template도 P6 1개/exit 1이며 opener 제거·단일 opener 대조도 같다. 같은 문단·다음 줄 HTML/JSX, blockquote 빈 문단, CRLF·공백 빈 줄, backslash delimiter와 문단 밖 닫는 기호도 기대대로 분리된다.

CSS comment-gap의 `.dark/**/:not(.light)`, `.dark/**/.dark`, `:root/**/.dark`, root descendant/빈 목록은 오류 2·traceback 없음이다. root 선택자 앞/뒤 주석의 정상 대조는 허용된다. 배열·삼항·임의 tag·중첩 object·다중행·blockquote JSX·ESM, JS 주석, inline/fenced/tilde 및 fence 길이/suffix·escaped interpolation corpus를 재실행했다.

## 실행 명령과 결과

Windows 실행기 `py -3.14`: Python `3.14.3`. WSL 실행기 `/home/digitie/.local/share/uv/python/cpython-3.11-linux-x86_64-gnu/bin/python3.11`: Python `3.11.15`. 아래 Python 명령은 각각 이 런타임으로 실제 실행했다.

| 명령 | Windows | WSL |
|---|---|---|
| `python -B -X utf8 -m unittest discover -s tests -p test_*.py` | 287 실행/성공, skip 0, 82.544초 | 287 수집, 284 실행/성공, skip 3, 22.908초 |
| `python -B -X utf8 -m unittest tests.test_kt_contrast tests.test_ux_lint -v` | 49 성공, skip 0, 15.764초 | 49 성공, skip 0, 8.155초 |
| `python -B -X utf8 tools/validate_plan.py` | task 106, 오류 0 | 동일 |
| `python -B -X utf8 tools/validate_document_links.py` | 문서 424, 대상 2412, 오류 0 | 동일 |
| `python -B -X utf8 tools/check_spdx.py` | 56개, 오류 0 | 동일 |
| `python -B -X utf8 tools/scan_secrets.py --all` | 556개, 검출 0 | 동일 |
| `python -B -X utf8 tools/check_prod_redaction.py --all` | 556개, 검출 0 | 동일 |
| `python -B -X utf8 tools/check_versions.py --self-check` | exit 0, registry 자체 검사 | 동일 |
| `python -B -X utf8 tools/check_aliases.py packages/tokens/aliases` | CSS 1개, 오류 0 | 동일 |
| aliases 집중 unittest | 35 성공, skip 0 | 35 수집, 34 성공, skip 1 |
| `python -B -X utf8 tools/kt_contrast.py packages/tokens/tokens.css --json` | exit 0, 27쌍 | 동일 |
| `python -B -X utf8 tools/ux_lint.py --root tests/fixtures/ux --json` | 보고 모드 exit 0, 12 findings | 동일 |
| `git diff --check bd73856ac1d3327b1fe46acc352163eee23ad504 c0c93c47e5f25aa0879fd0fb4e56261f6f624138` | exit 0 | 명시적 Git 경로로 exit 0 |

전체 unittest는 출력 축약을 위해 manifest의 `-v`만 생략했으며 동일하게 전체를 수집했다. 후보 밖 `review-t102-b-wsl-unittest.py`, `review-t102-post-b-gates.py`는 이번 후보 경로를 인자로 받아 임시 독립 사본에서 위 명령을 실행했다. WSL diff는 Windows worktree의 `.git` 포인터 해석을 피하기 위해 `git --git-dir=/mnt/f/dev/kor-travel-common/.git --work-tree=/mnt/f/dev/kor-travel-common-wt/review-t103-post11-b diff --check <고정 base> <고정 candidate>`를 사용했다. Git 설정을 쓰지 않는 읽기 전용 명령이다.

기존 probe 9개를 `t103-post9-b-corpus.py`로 실행한 관찰값 105개가 두 OS에서 완전히 일치했다. 모든 marker·traceback 검출 불리언은 false다. `t103-post9-b-new.py` 21개, `t103-post10-b-new.py` 7개, 이번 `t103-post11-b-new.py` 15개 관찰도 각각 두 OS에서 실행했다. 이 건수는 unittest 성공 건수와 합산하지 않는다. CSS/media 8개 조건/모드 대조와 smoke도 동일했고, airport line/page는 `1.3209340364487114`였다.

현재 문서에서 T-103 `IN_PROGRESS`, 소비자 build/e2e·T-010 selftest `NOT_RUN`, airport 역사/현행 값, GPL-3.0-or-later와 common 전용 경계를 확인했다. 제품 delta에는 소비자 파일·패키지 계약·CI 변경이 없다. source drift나 상태 오승인의 추가 finding은 발견하지 않았다.

## NOT_RUN과 한계

- `NOT_RUN(Windows Python 3.11 미설치)`; `py -0p`는 3.14/3.10을 반환했다.
- `NOT_RUN(WSL jsonschema 미설치)` 2개와 `NOT_RUN(WSL의 Windows 8.3 전용 시험)` 1개가 전체 unittest의 skip 3개다. 성공 건수에서 제외했다.
- `NOT_RUN(원격 CI 독립 조회)`; 로컬 성공을 exact 후보 CI 성공으로 집계하지 않았다.
- `NOT_RUN(소비자 build/e2e·npm/PyPI registry/게시·workflow dispatch는 manifest와 사용자 범위 밖)`; 후속 소비자/릴리스 gate는 해제하지 않는다.
- `NOT_RUN(MDX compiler/browser 실행)`; CLI의 문서 제외·실행 코드 보존 계약 및 최소 입력과 대조군에 근거한 판정이다.
- 제품 종료 SHA/tree/clean 확인 뒤 본 원본 한 파일만 별도 commit한다. 보고서 commit SHA와 파일/Git blob SHA256은 제품 후보와 구분해 coordinator에게 전달한다.
