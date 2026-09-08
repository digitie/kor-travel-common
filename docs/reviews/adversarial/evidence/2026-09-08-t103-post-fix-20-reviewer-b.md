<!-- SPDX-License-Identifier: GPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie) -->

# T-103 post-fix-20 독립 적대적 리뷰 B 원본

- 실행 ID: T103-POST20-B-20260908-135227
- 판정: **NO-GO**. 신규 P2 1건(B-P2-17), 신규 P0/P1/P3 0건. 기존 16개 ID는 이번 실행한 누적 반례에서 FIXED.
- 시작 KST: 2026-09-08T13:52:27.6309261+09:00
- 제품 검토 종료 KST: 2026-09-08T13:58:52.7195902+09:00
- 시작/종료 제품 HEAD: dd06f22150d9ac9bed25ee7abc0b65265cdaa651
- 시작/종료 제품 tree: 184a1755640d78fd52ce1dbeb30897a557a01ece
- 시작/종료 제품 상태: detached, git status --porcelain=v1 --untracked-files=all 출력 없음.
- 격리 경로: F:/dev/kor-travel-common-wt/review-t103-post20-b. 전체 시험과 정적 gate는 이 후보의 임시 독립 사본에서도 실행했다. Git fixture는 GIT_* 환경을 제거한 별도 임시 저장소다.
- manifest commit: 358f67177eff969750e3bc8a40b2cea8b512c234. [공통 manifest](2026-09-08-t103-post-fix-20-manifest.md)를 git show로 읽었다.
- manifest Git blob SHA256: e3ea6eacb9ea52c5b8afb1ef4dc773846e99882969104211f3f6ed49f1877644
- 수정 대조 기준: 415984bf7cb450d44d7661424884d6641fef8309.
- 소스 .git/config 시작/종료 SHA256: 0A0F849E7874CF0A25926856F9D2E381CCBF4C2DCB5999869C57B86E0F5BEB5B. Git 설정을 변경하지 않았다.
- 상대 reviewer 결과 및 과거 raw 본문을 읽지 않았다. 제품·manifest·소비자 파일을 변경하지 않았고, 이 보고서만 별도 commit한다.

## 요청과 검토 범위

요청 원문: “post-fix-20 독립 리뷰를 시작해 주세요. 동일 immutable 코드 후보 dd06f22150d9ac9bed25ee7abc0b65265cdaa651 (tree 184a1755640d78fd52ce1dbeb30897a557a01ece), manifest 358f671/docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-20-manifest.md를 기준으로 사용하세요. 전문 영역은 Git diff/added-line 판정·소비자 이관 경계·입력/검증 회귀입니다. review-t103-post20-b 격리 worktree를 만들고 Windows Python 3.14·WSL Python 3.11 full/focused 및 manifest 범위의 bare CR/CRLF/Unicode line terminator·fence/paragraph/--base를 재현하세요. 상대 reviewer 결과는 보지 마세요. 원본 report만 docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-20-reviewer-b.md에 작성하고, report 파일만 포함한 raw-only commit hash·SHA256·clean tree·verdict를 보내 주세요. 후보 코드와 테스트는 수정하지 마세요.”

제품 변경인 tools/ux_lint.py와 tests/test_ux_lint.py의 전체 delta를 읽었다. 그 외 delta의 과거 manifest/raw 경로는 파일 목록만 확인하고 raw 본문은 읽지 않았다. CR/CRLF/LS/PS의 문법별 역할, Git LF 행 좌표, 백틱 인용, fence, 문단, JSX/ESM 표현식, 입력 오류·redaction·baseline, CSS와 4앱 조사 예제를 재검증했다.

## 실제 실행과 결과

Windows는 Python 3.14.3, WSL은 /home/digitie/.local/share/uv/python/cpython-3.11-linux-x86_64-gnu/bin/python3.11의 Python 3.11.15다. Node 대조는 Windows v25.9.0·WSL v22.22.2다.

| 검증 | Windows | WSL |
|---|---|---|
| 전체 unittest discover -s tests -p test_*.py | 291개 실행 성공, 158.327초, skip 0 | 291개 수집, 288개 실행 성공, skip 3, 48.368초 |
| tests.test_kt_contrast + tests.test_ux_lint | 53개 성공, 28.604초, skip 0 | 53개 성공, 15.364초, skip 0 |
| uv run --offline --no-project --python 3.11의 tests.test_ux_lint | 해당 없음 | 30개 성공, 7.363초, skip 0 |
| 별칭 focused unittest | 35개 성공, skip 0 | 35개 수집, 34개 성공, skip 1 |
| validate_plan.py | task 106개, 오류 0 | 동일 |
| validate_document_links.py | 문서 451개, 대상 2420개, 오류 0 | 동일 |
| check_spdx.py | 파일 56개, 오류 0 | 동일 |
| scan_secrets.py --all | 파일 583개, 발견 0, 명시적 예외 0 | 동일 |
| check_prod_redaction.py --all | 파일 583개, 발견 0, 명시적 예외 0 | 동일 |
| check_versions.py --self-check | exit 0, 레지스트리 자체 검사만 | 동일 |
| check_aliases.py packages/tokens/aliases | CSS 1개, 오류 0 | 동일 |
| kt_contrast.py packages/tokens/tokens.css --json | exit 0, 27쌍 | 동일 |
| ux_lint.py --root tests/fixtures/ux --json | report exit 0, 12개 발견 | 동일 |
| git diff --check 기준..후보 | exit 0 | exit 0 |

실제 명령은 Python에 -B -X utf8을 붙였다. 전체 시험과 정적 gate는 .git/codex-audit/review-t102-b-wsl-unittest.py 및 review-t102-post-b-gates.py에 후보 경로를 전달해 실행했다. 두 helper는 후보의 임시 사본에서 실행하며 원본 Git 설정을 변경하지 않는다. focused 명령은 후보 worktree에서 -m unittest tests.test_kt_contrast tests.test_ux_lint로 직접 실행했다. manifest의 -v는 출력 상세 옵션이며 위 실행은 -v 없이 같은 시험을 수집했다.

WSL diff 명령은 Windows 형식 worktree 포인터를 해석하지 않도록 git --git-dir=/mnt/f/dev/kor-travel-common/.git --work-tree=/mnt/f/dev/kor-travel-common-wt/review-t103-post20-b diff --check 415984bf7cb450d44d7661424884d6641fef8309 dd06f22150d9ac9bed25ee7abc0b65265cdaa651로 실행했다. 이는 명령별 경로 지정이며 core.worktree 변경이 아니다.

독립 직접 반례는 양 OS에서 아래 외부 probe 스크립트에 후보 경로를 전달했다. 모든 출력은 현재 회차에서 새로 얻었으며 과거 raw에서 복사하지 않았다.

| 스크립트(.git/codex-audit 아래) | OS별 관찰 수 | 결과 |
|---|---:|---|
| t103-post9-b-corpus.py | 105 | 기존 입력·diff·CSS·인용·redaction 반례 기대 일치 |
| t103-post15-b-late-corpus.py | 140 | 미종결 span·표현식·Unicode·CSS comment-gap·4앱 대조 일치 |
| t103-post17-b-latest-corpus.py | 104 | 최신 식별자·FEFF·async·JS 주석·Git Unicode 행 회귀 일치 |
| t103-post18-b-new.py | 37 | CR/LS/PS/FF/NEL 가짜 hunk·문자열·untracked·ESM 회귀 일치 |
| t103-post19-b-new.py | 34 | 정확한 CR/CRLF bytes·paragraph/fence·--base 회귀 일치 |
| t103-post20-b-new.py | 18 | 12건 기대 일치, LS/PS 닫힌 span 6건 오차단 |

합계 438개 관찰/OS다. unittest 개수와 합산하지 않는다. 438개 JSON 행을 대조했으며 Unicode 데이터베이스 메타데이터(Windows 16.0.0, WSL 14.0.0) 한 행만 다르고 판정은 동일했다. 이전 probe의 write_text CRLF 변환 가능성은 새 write_bytes 입력의 SHA256 일치로 별도 검증했다. 새 6건도 입력 SHA256과 결과가 두 OS에서 동일하다.

## 누적 finding disposition

| 원 ID·심각도 | 이번 판정 | 직접 확인한 경계 |
|---|---|---|
| B-P1-01 | FIXED | 외부 root/CWD에 따른 diff 대상 선택 |
| B-P1-02 | FIXED | 앞쪽 추가로 기존 baseline 허용 건수를 넘기는 경우 |
| B-P1-03 | FIXED | 배열·삼항·임의 tag·nested object·ESM·JSX·미종결 1/2자 span의 실행식, bare CR/CRLF 문단·fence |
| B-P1-04 | FIXED | 경로·값·argparse·JSON·Markdown·step summary 오류 redaction |
| B-P2-05 | FIXED | muted 읽기 표면 선언 시 추가 text 4쌍 |
| B-P2-06 | FIXED | baseline bool/소수/비유한/큰 정수/깊은 JSON 입력 오류 |
| B-P3-07 | FIXED | geo 미달 8건 근거와 예제 |
| B-P1-08 | FIXED | 추가 내용의 +++가 diff 파일 헤더로 오인되지 않음 |
| B-P1-09 | FIXED | CSS 조건·교집합·specificity·source order·문자열·주석 |
| B-P2-10 | FIXED | airport 현행 1.320934와 역사 1.15 구분 |
| B-P1-11 | FIXED | selector 인용 공백·대소문자 경계 |
| B-P1-12 | FIXED | 빈 selector list·root descendant 거부 |
| B-P2-13 | FIXED | 파일 첫 span·3자 inline 인용 음성 대조 |
| B-P1-14 | FIXED | LS/PS JS 줄 주석 종료, template 보간·중첩 JSX |
| B-P1-15 | FIXED | Git diff LF 분리, Unicode 가짜 hunk/context |
| B-P1-16 | FIXED | raw CR 읽기·Git 출력 개행 보존, plain 및 --base의 line/added 일치 |

FIXED는 위 실행한 반례 범위의 판정이며 모든 JavaScript/Markdown 문법을 완전 검증했다는 뜻이 아니다. 신규 B-P2-17은 별도 오차단이며 원 P1의 심각도를 낮춘 것이 아니다.

## 신규 B-P2-17 — JavaScript LS/PS를 Markdown 문단 종료로 적용해 닫힌 인용을 오차단

- 심각도: P2. disposition: OPEN, 수정 필요.
- 위치: tools/ux_lint.py:21-24의 _MDX_LINE_BREAK_PATTERN·_MDX_PARAGRAPH_BOUNDARY, :136-147의 문단 계산, :628-648의 닫힌 span 탐색/마스킹.
- 계약: [T-103](../../../tasks/T-103-kt-contrast-ux-lint.md) 구현 범위 2와 수용 기준은 백틱 안 인용을 제외한다.
- 원인: Markdown 문단 경계 정규식에 U+2028/U+2029가 들어가 정상 닫힌 span의 종료 delimiter 탐색이 중간에서 끊긴다. JS 줄 주석은 LS/PS에서 끝나지만 Markdown 문단 규칙은 다르다. [CommonMark 0.31.2 §2.1](https://spec.commonmark.org/0.31.2/#line-ending)(2024-01-28, 조회 2026-09-08)의 문서 줄 종료는 LF·bare CR·CRLF다. 따라서 아래 LS/PS 입력은 빈 문단 없이 닫힌 code span 하나다.
- 최소 입력 생성 및 CLI: 후보 경로를 CANDIDATE로 두고 별도 임시 root에 아래 bytes를 쓴 뒤 python -B -X utf8 CANDIDATE/tools/ux_lint.py --root TEMP_ROOT --fail-new --json을 실행한다.

~~~python
from pathlib import Path
tick = chr(96)
sep = chr(0x2028)
source = (
    "Example " + tick * 2 + "one" + sep * 2
    + '<div className="outline-none"/>' + sep * 2
    + "two" + tick * 2 + "\n"
)
Path("TEMP_ROOT/Page.mdx").write_bytes(source.encode("utf8"))
~~~

- 위 LS/2자 입력 SHA256: 9e647c68fa2ea96698bead7a80fae12cdb0b1ea2bd4e60d36ac4613fa6924b2e.
- PS/2자 입력 SHA256: b4383025c114ccc8b67ecb75c2e881bc67bf57efd7037b46047daa14271e1bfe.
- Windows 3.14·WSL 3.11 실제: exit 1, status FAIL, P6 1건, line 1, added true, traceback 없음.
- 기대: 인용 문서이므로 exit 0, 발견 0. 같은 입력의 delimiter 길이 1·2·3 각각, LS·PS 각각 모두 오차단한다(6건/OS).
- 양성/음성 대조: sep를 일반 공백으로 바꾸면 1·2·3자 모두 exit 0. LF·CR·CRLF로 바꾸면 실제 빈 문단 뒤 JSX이므로 모두 P6/exit 1. 이전 bare CR paragraph/fence P1도 모두 P6/exit 1로 정상 수정됐다.
- 영향: 문서 코드 예제가 신규 UX 위반으로 분류되어 --fail-new/이관 gate를 부당하게 차단한다. JS 실행 위반 우회로 확대하지 않고 재현된 false failure에 맞춰 P2로 분류했다.
- 수정 권고: Markdown 문단·fence의 LF/CR/CRLF 경계와 JS expression/comment의 LF/CR/LS/PS 경계를 분리한다. raw bytes와 Git LF 행 좌표 보존은 유지한다. 위 6개 닫힌 span 음성과 기존 CR 문단/fence·JS LS/PS 주석 양성을 함께 회귀한다.
- base의 문단 정규식은 CR?LF만 포함했고 후보 delta에서 LS/PS 문단 처리가 도입된 것을 코드 대조했다. 이 최소 입력을 base CLI에서 다시 실행하지는 않았으므로 base의 전체 CLI 결과는 NOT_RUN이다.

## 문서·소비자 경계 및 한계

[T-103](../../../tasks/T-103-kt-contrast-ux-lint.md)과 [resume](../../../resume.md)은 IN_PROGRESS를 유지한다. [evidence](../../../evidence/t103-kt-contrast-ux-lint.md)는 airport 1.320934와 역사 1.15를 구분하며 geo 8건 및 소비자 build/e2e NOT_RUN을 연결한다. 재사용 workflow 자체 검증은 후행 T-010이며 현재 CLI 구현 완료로 대신 표시하지 않았다. GPL-3.0-or-later 헤더·공용 도구 범위가 유지된다.

- NOT_RUN(Windows Python 3.11): 설치되지 않았다. Windows 3.14 결과로 대체 표기하지 않는다.
- NOT_RUN(WSL의 skip 3): Windows 8.3 경로 1개 및 jsonschema 미설치로 schema 대조 2개. 나머지 288개 실행과 구분했다.
- NOT_RUN(exact candidate 원격 CI 독립 조회): coordinator의 CI 성공 전달은 받았으나 독립 관찰 결과로 집계하지 않았다.
- NOT_RUN(MDX compiler/browser): JS 식별자·표현식 Node 대조는 실행했지만 실제 MDX 컴파일/브라우저 렌더는 하지 않았다. 신규 P2의 문서 해석은 위 공식 CommonMark 규칙과 코드/CLI 대조에 근거한다.
- NOT_RUN(소비자 build/e2e·실제 앱 baseline·npm/PyPI 게시·registry·workflow dispatch·T-010 workflow selftest): common 리뷰 범위 밖이며 실행하지 않았다.
- NOT_RUN(non-UTF8 Git 출력 주입): 이번 직접 입력은 UTF-8 bytes다.

신규 P2를 닫기 전 PASS 또는 릴리스 가능으로 표시하지 않는다. 제품 검토 종료 후 생성하는 commit에는 이 원본 한 파일만 포함한다.
