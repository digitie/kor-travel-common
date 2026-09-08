<!-- SPDX-License-Identifier: GPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie) -->

# T-103 post-fix-22 독립 적대적 리뷰 B 원본

- 실행 ID: T103-POST22-B-20260908-142006
- 판정: **NO-GO**. 신규 B-P2-19 1건, 신규 P0/P1/P3 0건. 기존 B finding 18개는 이번 누적 반례에서 FIXED.
- 시작 KST: 2026-09-08T14:20:06.8362684+09:00
- 제품 검토 종료 KST: 2026-09-08T14:22:43.8552794+09:00
- 시작/종료 제품 HEAD: 61f1cc6a900e25268e0c5eadc32ce1c5ccc9d3f3
- 시작/종료 제품 tree: bab9313184719713bc96fcb455b38b121f8db0f5
- 시작/종료 제품 상태: detached, git status --porcelain=v1 --untracked-files=all 출력 없음.
- 격리: F:/dev/kor-travel-common-wt/review-t103-post22-b. 전체 시험·정적 gate는 후보의 임시 사본, focused는 후보 worktree, 직접 반례는 GIT_* 환경을 제거한 별도 임시 Git 저장소에서 실행했다.
- manifest commit: 43d7f530cbe987c89e99ad2f5a6665d65724a78d. [공통 manifest](2026-09-08-t103-post-fix-22-manifest.md)를 git show로 읽었다.
- manifest Git blob SHA256: e31992b21a026bd895d3fb02832ef7c736517b557ba1a7a273983bdc37c1e005
- delta 기준: 7e31b54e92c52e3b859b80c520d7ae88c2522159.
- 소스 .git/config 시작/종료 SHA256: 0A0F849E7874CF0A25926856F9D2E381CCBF4C2DCB5999869C57B86E0F5BEB5B. 설정 변경 없음.
- 상대 reviewer 결과 및 과거 raw 본문을 읽지 않았다. 제품·manifest·소비자를 수정하거나 commit/push하지 않았다. 제품 검토 종료 후 이 보고서 한 파일만 별도 commit한다.

## 요청과 범위

요청: “post-fix-22 독립 리뷰를 시작해 주세요. immutable 코드 후보 61f1cc6a900e25268e0c5eadc32ce1c5ccc9d3f3 (tree bab9313184719713bc96fcb455b38b121f8db0f5), manifest 43d7f53/docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-22-manifest.md를 기준으로 사용하세요. Git diff/added-line·입력/검증·fence suffix 경계가 전문 영역입니다. review-t103-post22-b 격리 worktree에서 Windows Python 3.14·WSL Python 3.11 full/focused, --base와 fence marker ASCII space/tab/LS/PS, CR/CRLF/LS/PS 반례를 재현하세요. 상대 결과를 보지 말고 원본 report만 docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-22-reviewer-b.md에 작성한 뒤 report-only raw commit hash·SHA256·clean tree·verdict를 보내 주세요. 후보는 수정하지 마세요.”

제품 delta인 tools/ux_lint.py·tests/test_ux_lint.py 전체를 읽고 인자 없는 Unicode strip 대신 ASCII space/tab을 사용하는 수정과 선언/문서 인용 판정 회귀를 확인했다. 나머지 delta는 이전 manifest 한 경로이며 상대 raw는 포함되지 않았다. 누적 CSS·JSON·redaction·Git diff·MDX·symlink·airport corpus와 task/소비자 경계를 재검증했다.

## 실제 검증

Windows Python 3.14.3·Node v25.9.0, WSL Python 3.11.15·Node v22.22.2다. WSL Python은 /home/digitie/.local/share/uv/python/cpython-3.11-linux-x86_64-gnu/bin/python3.11이다. 아래 결과는 이번 후보에서 독립 실행했으며 작성자 evidence를 성공으로 재사용하지 않았다.

| 검증 | Windows | WSL |
|---|---|---|
| 전체 unittest discover -s tests -p test_*.py | 292개 성공, skip 0, 107.807초 | 292개 수집, 289개 성공, skip 3, 34.270초 |
| tests.test_kt_contrast + tests.test_ux_lint | 54개 성공, skip 0, 22.373초 | 54개 성공, skip 0, 11.686초 |
| uv run --offline --no-project --python 3.11의 tests.test_ux_lint | 해당 없음 | 31개 성공, skip 0, 5.383초 |
| 별칭 focused unittest | 35개 성공, skip 0 | 35개 수집, 34개 성공, skip 1 |
| validate_plan.py | task 106개, 오류 0 | 동일 |
| validate_document_links.py | 문서 455개, 대상 2425개, 오류 0 | 동일 |
| check_spdx.py | 파일 56개, 오류 0 | 동일 |
| scan_secrets.py --all | 파일 587개, 발견 0, 명시적 예외 0 | 동일 |
| check_prod_redaction.py --all | 파일 587개, 발견 0, 명시적 예외 0 | 동일 |
| check_versions.py --self-check | 레지스트리 자체 검사 exit 0 | 동일 |
| check_aliases.py packages/tokens/aliases | CSS 1개, 오류 0 | 동일 |
| kt_contrast.py packages/tokens/tokens.css --json | exit 0, 27쌍 | 동일 |
| ux_lint.py --root tests/fixtures/ux --json | report exit 0, 12개 발견 | 동일 |
| git diff --check 기준..후보 | exit 0 | exit 0 |

Python에는 -B -X utf8을 사용했다. 전체/정적 gate는 .git/codex-audit/review-t102-b-wsl-unittest.py 및 review-t102-post-b-gates.py에 후보 경로를 전달해 임시 사본에서 실행했다. focused는 -m unittest tests.test_kt_contrast tests.test_ux_lint로 직접 실행했다. 출력 -v 없이 같은 테스트 집합을 수집했다. WSL 전체는 uv가 설치한 Python 실행 파일로 직접 실행했고, uv 전면 명령으로 전체를 중복 실행하지 않았다.

WSL diff는 git --git-dir=/mnt/f/dev/kor-travel-common/.git --work-tree=/mnt/f/dev/kor-travel-common-wt/review-t103-post22-b diff --check 7e31b54e92c52e3b859b80c520d7ae88c2522159 61f1cc6a900e25268e0c5eadc32ce1c5ccc9d3f3로 실행했다. 명령별 경로 지정이며 core.worktree 설정 변경이 아니다.

다음은 양 OS에서 .git/codex-audit 아래 독립 probe 스크립트에 후보 경로를 전달한 결과다. 과거 raw 본문을 읽지 않고 새 출력만 대조했다.

| 스크립트 | OS별 관찰 수 | 결과 |
|---|---:|---|
| t103-post9-b-corpus.py | 105 | 기존 입력·baseline·CSS·diff·redaction·MDX 기대 일치 |
| t103-post15-b-late-corpus.py | 140 | 표현식·문단·인용·CSS comment-gap·4앱 기대 일치 |
| t103-post17-b-latest-corpus.py | 104 | Unicode·FEFF·async·JS 주석·Git 행 기대 일치 |
| t103-post18-b-new.py | 37 | CR/LS/PS/FF/NEL 가짜 hunk·context·untracked 기대 일치 |
| t103-post19-b-new.py | 34 | 정확한 CR/CRLF bytes·문단·fence·plain/--base 기대 일치 |
| t103-post20-b-new.py | 18 | 닫힌 LS/PS 1/2/3자 span 포함 기대 일치 |
| t103-post21-b-new.py | 29 | fence LS/PS suffix·ASCII 공백/탭 대조 포함 기대 일치 |
| t103-post22-b-new.py | 28 | 20건 기대 일치, 종료 fence 4열 들여쓰기 8건 오차단 |

합계 495개 관찰/OS이며 unittest 개수와 합산하지 않는다. 저장한 Windows/WSL JSON 전체 행은 Unicode 데이터베이스 메타데이터 1행(16.0.0/14.0.0)만 다르고 판정·입력 SHA256·발견 행은 동일했다. 새 입력은 write_bytes로 기록해 자동 개행 변환을 피했다.

## 누적 finding disposition

| 원 ID·심각도 | 판정 | 이번 재현 범위 |
|---|---|---|
| B-P1-01 | FIXED | root/CWD에 따른 Git diff 대상 |
| B-P1-02 | FIXED | 앞쪽 추가의 baseline 초과 |
| B-P1-03 | FIXED | 배열·삼항·tag·nested object·ESM·JSX·미종결 span 표현식, CR/CRLF 문단/fence |
| B-P1-04 | FIXED | 경로·값·argparse·JSON·Markdown·step summary redaction |
| B-P2-05 | FIXED | muted 추가 읽기 text 쌍 |
| B-P2-06 | FIXED | bool/소수/비유한/거대 정수/깊은 JSON |
| B-P3-07 | FIXED | geo 예제 미달 8건 |
| B-P1-08 | FIXED | +++ 추가 내용과 Git 헤더 구분 |
| B-P1-09 | FIXED | CSS 조건·specificity·순서·중첩·문자열·주석 |
| B-P2-10 | FIXED | airport 현재 1.320934와 역사 1.15 |
| B-P1-11 | FIXED | selector 인용 공백·대소문자 |
| B-P1-12 | FIXED | 빈 selector list·root descendant 입력 오류 |
| B-P2-13 | FIXED | 파일 첫 span·3자 inline 인용 |
| B-P1-14 | FIXED | LS/PS JS 줄 주석·template 보간·중첩 JSX |
| B-P1-15 | FIXED | Git diff LF 분리·Unicode 가짜 hunk |
| B-P1-16 | FIXED | bare CR raw 읽기와 added-line 판정 |
| B-P2-17 | FIXED | 닫힌 LS/PS 1/2/3자 span plain·--base |
| B-P2-18 | FIXED | 종료 fence suffix LS/PS plain·--base, ASCII space/tab 대조 |

B-P2-18 원 LS 입력 SHA256 900cbc34efebac74b997fe110055bb4c82e6ee3148b699aea0fb3c342ea1a825 및 PS 입력 7d560181383149c5722b159a4076a44523b3f55b997fb5868dc224a27a087382는 plain·--base 모두 exit 0·발견 0이다. ASCII space/tab suffix는 실제 종료 fence로 인정해 후속 JSX를 P6/exit 1로 보고한다. FIXED는 실행한 반례 범위이며 모든 Markdown 문법을 완전 검증했다는 뜻이 아니다.

## 신규 B-P2-19 — 종료 fence 앞의 4열 들여쓰기를 제한 없이 제거

- 심각도: P2. disposition: OPEN, 수정 필요.
- 위치: tools/ux_lint.py:520의 candidate = text[cursor:next_end].lstrip(" \t"), :524의 종료 판정.
- 계약: [T-103](../../../tasks/T-103-kt-contrast-ux-lint.md)의 인용 제외 계약. [CommonMark 0.31.2 §4.5](https://spec.commonmark.org/0.31.2/#fenced-code-blocks)(2024-01-28, 조회 2026-09-08)는 종료 fence 들여쓰기를 최대 3칸으로 제한하며, Example 137은 4칸이면 종료가 아님을 명시한다.
- 최소 재현: 임시 root의 Page.mdx에 아래 bytes를 쓴다.

~~~python
from pathlib import Path
source = (
    "~~~tsx\nquoted\n    ~~~\n"
    + '<div className="outline-none"/>\n~~~\n'
)
Path("TEMP_ROOT/Page.mdx").write_bytes(source.encode("utf8"))
~~~

- 명령: python -B -X utf8 CANDIDATE/tools/ux_lint.py --root TEMP_ROOT --fail-new --json. --base 대조는 별도 Git fixture에서 safe+LF 내용의 Page.mdx를 commit한 SHA를 --base로 추가한다.
- tilde/4칸 입력 SHA256: 895daec1a47f84813e4459494f7f96a6b54b3dd400d1098455adca2024ce8679.
- tilde/tab 입력 SHA256: a452f7feb209889fd89bc16113fcf5641ac99be7acb73812654050a04b8f5705.
- backtick/4칸 입력 SHA256: b2c4d7b3dcdfbc775856aab9689c79d00022e05fbe81a249d9334e0a1da811bf.
- backtick/tab 입력 SHA256: 273ea08253a7234633fcb57e1e8264d772baf27d57de9dc1b28da2c4fda48930.
- 실제: 양 OS, tilde/backtick, 4칸/tab, plain/--base 총 8건/OS에서 exit 1·status FAIL·P6 line 4·added true·traceback 없음.
- 기대: 3행의 marker는 들여쓰기가 4열이므로 종료가 아니며 4행은 5행의 실제 종료까지 코드 인용이다. exit 0·발견 0이어야 한다.
- 대조: 0/1/3칸 들여쓴 종료 marker는 후속 JSX를 P6/exit 1로 올바르게 판정한다. LS/PS prefix가 붙은 marker는 종료로 인정하지 않아 exit 0이다. 두 marker 종류와 두 CLI 모드 모두 기대 일치했다.
- 원인·영향: ASCII 문자 집합 제한은 적용됐으나 lstrip이 개수·열을 보존하지 않아 4열 이상을 유효한 종료 위치로 만든다. 문서 예제에 불필요한 UX 위반을 생성해 --fail-new·이관 gate를 부당하게 차단한다. 재현된 false failure 범위에 맞춰 P2로 분류했다.
- 수정 권고: 종료 fence의 선행 들여쓰기를 원문 열 기준으로 검사해 3열 이하에서만 marker를 인정한다. 선행 탭은 다음 4열 정렬 지점까지 계산하고, suffix의 ASCII space/tab 규칙과 별도로 다룬다. 기존 LS/PS suffix·prefix와 CR/CRLF 문단·Git LF 행 좌표를 유지한다.
- 원인 경계: base의 인자 없는 lstrip도 들여쓰기 양을 제한하지 않았다. 이번 변경 줄에서 재확인한 잔여 결함이며 새로 도입된 동작이라고 주장하지 않는다. base CLI의 동일 입력 재실행은 NOT_RUN이다.

## 문서·범위 및 NOT_RUN

[T-103](../../../tasks/T-103-kt-contrast-ux-lint.md)·[resume](../../../resume.md)은 IN_PROGRESS다. [evidence](../../../evidence/t103-kt-contrast-ux-lint.md)는 airport 현재 1.320934·역사 1.15 및 소비자 build/e2e·후행 T-010 workflow selftest의 NOT_RUN을 구분한다. 4앱 조사 예제·baseline과 geo 8건을 재현했다. GPL-3.0-or-later와 common 공용 도구 경계를 유지한다.

- NOT_RUN(Windows Python 3.11): 설치되지 않았다. Windows 3.14 결과와 구분한다.
- NOT_RUN(WSL skip 3): Windows 8.3 경로 1개, jsonschema 미설치로 schema 대조 2개. 289개 실행 성공과 구분했다.
- NOT_RUN(exact candidate 원격 CI 독립 조회): 로컬 실행을 CI 성공으로 집계하지 않는다.
- NOT_RUN(MDX compiler/browser): Node의 표현식 대조는 실행했으나 실제 MDX 컴파일/렌더는 실행하지 않았다. 신규 P2는 공식 문법·코드·CLI 재현에 근거한다.
- NOT_RUN(소비자 build/e2e·실제 앱 baseline·registry·npm/PyPI 게시·workflow dispatch·T-010 selftest): 범위 밖이며 호출하지 않았다.
- NOT_RUN(uv 전면 명령으로 전체 재실행): 동일 uv Python 3.11로 전체를 직접 실행했고 focused만 uv run으로 확인했다.
- NOT_RUN(non-UTF8 Git 출력 주입): 이번 입력은 UTF-8 bytes다.

신규 P2가 열려 있어 PASS로 확정하지 않는다. 제품 검토 종료 뒤 보고서 한 파일만 commit하며 후보와 Git 설정을 보존한다.
