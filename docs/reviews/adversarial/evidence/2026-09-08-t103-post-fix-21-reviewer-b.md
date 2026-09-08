<!-- SPDX-License-Identifier: GPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie) -->

# T-103 post-fix-21 독립 적대적 리뷰 B 원본

- 실행 ID: T103-POST21-B-20260908-141026
- 판정: **NO-GO**. 신규 B-P2-18 1건, 신규 P0/P1/P3 0건. 기존 B finding 17개는 이번 누적 반례에서 FIXED.
- 시작 KST: 2026-09-08T14:10:26.2435441+09:00
- 제품 검토 종료 KST: 2026-09-08T14:13:19.5534378+09:00
- 시작/종료 제품 HEAD: 7e31b54e92c52e3b859b80c520d7ae88c2522159
- 시작/종료 제품 tree: 2cd07cf45d1428d1027b6dd647c48353c3bdde59
- 시작/종료 제품 상태: detached, git status --porcelain=v1 --untracked-files=all 출력 없음.
- 격리: F:/dev/kor-travel-common-wt/review-t103-post21-b. 전체 시험·정적 gate는 이 후보의 임시 독립 사본에서 실행했고, focused 시험은 후보에서 직접 실행했다. Git 반례는 GIT_* 환경을 제거한 임시 저장소에만 썼다.
- manifest commit: 6bd3e445acc3e97851e1caa0254ba0b02af604cc. [공통 manifest](2026-09-08-t103-post-fix-21-manifest.md)를 git show로 읽었다.
- manifest Git blob SHA256: 5d3b88bb472acd98b1a7cd5fcaec196e01a75ac3d807189d023ee2669c962564
- delta 기준: dd06f22150d9ac9bed25ee7abc0b65265cdaa651.
- 소스 .git/config 시작/종료 SHA256: 0A0F849E7874CF0A25926856F9D2E381CCBF4C2DCB5999869C57B86E0F5BEB5B. 설정 변경 없음.
- 상대 reviewer 결과와 과거 raw 본문을 읽지 않았다. 후보·manifest·소비자를 수정하거나 commit/push하지 않았다. 제품 검토 종료 후 이 원본 한 파일만 별도 commit한다.

## 요청과 검토 범위

요청: “post-fix-21 독립 리뷰를 시작해 주세요. immutable 코드 후보 7e31b54e92c52e3b859b80c520d7ae88c2522159 (tree 2cd07cf45d1428d1027b6dd647c48353c3bdde59), manifest 6bd3e44/docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-21-manifest.md를 기준으로 사용하세요. Git diff/added-line·입력/검증·소비자 이관 경계가 전문 영역입니다. review-t103-post21-b 격리 worktree에서 Windows Python 3.14·WSL Python 3.11 full/focused와 CR/LF/CRLF/LS/PS, --base, fence/paragraph/closed span 반례를 재현하세요. 상대 결과를 보지 말고 원본 report만 docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-21-reviewer-b.md에 작성한 뒤 report-only raw commit hash·SHA256·clean tree·verdict를 보내 주세요. 후보는 수정하지 마세요.”

tools/ux_lint.py·tests/test_ux_lint.py의 전체 delta를 읽고 Markdown/ECMAScript 경계 분리, raw 개행 보존과 Git LF 행 좌표, 입력 오류·redaction·baseline, 누적 CSS/MDX corpus, task·evidence·소비자 경계를 확인했다. delta의 과거 manifest/raw 경로는 목록만 확인했으며 원본 본문은 읽지 않았다.

## 실제 실행

Windows Python 3.14.3·Node v25.9.0, WSL Python 3.11.15·Node v22.22.2다. WSL Python 경로는 /home/digitie/.local/share/uv/python/cpython-3.11-linux-x86_64-gnu/bin/python3.11이다. 다음은 작성자의 manifest 결과가 아니라 이번 독립 실행 결과다.

| 검증 | Windows | WSL |
|---|---|---|
| 전체 unittest discover -s tests -p test_*.py | 291개 성공, skip 0, 112.758초 | 291개 수집, 288개 성공, skip 3, 26.756초 |
| tests.test_kt_contrast + tests.test_ux_lint | 53개 성공, skip 0, 28.417초 | 53개 성공, skip 0, 14.753초 |
| uv run --offline --no-project --python 3.11의 tests.test_ux_lint | 해당 없음 | 30개 성공, skip 0, 7.074초 |
| 별칭 focused unittest | 35개 성공, skip 0 | 35개 수집, 34개 성공, skip 1 |
| validate_plan.py | task 106개, 오류 0 | 동일 |
| validate_document_links.py | 문서 454개, 대상 2425개, 오류 0 | 동일 |
| check_spdx.py | 파일 56개, 오류 0 | 동일 |
| scan_secrets.py --all | 파일 586개, 발견 0, 명시적 예외 0 | 동일 |
| check_prod_redaction.py --all | 파일 586개, 발견 0, 명시적 예외 0 | 동일 |
| check_versions.py --self-check | 레지스트리 자체 검사 exit 0 | 동일 |
| check_aliases.py packages/tokens/aliases | CSS 1개, 오류 0 | 동일 |
| kt_contrast.py packages/tokens/tokens.css --json | exit 0, 27쌍 | 동일 |
| ux_lint.py --root tests/fixtures/ux --json | report exit 0, 12개 발견 | 동일 |
| git diff --check 기준..후보 | exit 0 | exit 0 |

Python 명령은 -B -X utf8을 사용했다. 전체/정적 gate는 후보 경로를 .git/codex-audit/review-t102-b-wsl-unittest.py와 review-t102-post-b-gates.py에 전달했다. 두 helper는 임시 사본과 별도 Git 저장소를 사용해 소스 Git 설정을 변경하지 않는다. focused는 -m unittest tests.test_kt_contrast tests.test_ux_lint로 후보에서 직접 실행했다. -v 없이 같은 테스트 집합을 수집했고, WSL 전체는 uv가 설치한 Python 3.11 실행 파일로 직접 실행했다. 전체 시험을 uv 전면 명령으로 중복 실행하지 않았다.

WSL diff는 git --git-dir=/mnt/f/dev/kor-travel-common/.git --work-tree=/mnt/f/dev/kor-travel-common-wt/review-t103-post21-b diff --check dd06f22150d9ac9bed25ee7abc0b65265cdaa651 7e31b54e92c52e3b859b80c520d7ae88c2522159로 실행했다. 명령별 경로 지정이며 core.worktree 설정 변경이 아니다.

아래 독립 probe를 양 OS에서 후보 경로 인자로 실행했다. .git/codex-audit 아래 스크립트이며 raw 보고서 본문을 입력으로 사용하지 않는다.

| 스크립트 | OS별 관찰 수 | 결과 |
|---|---:|---|
| t103-post9-b-corpus.py | 105 | 입력·diff·baseline·CSS·redaction·MDX 기존 반례 기대 일치 |
| t103-post15-b-late-corpus.py | 140 | 표현식·selector/comment-gap·문단·인용·4앱 대조 기대 일치 |
| t103-post17-b-latest-corpus.py | 104 | 최신 Unicode·FEFF·async·JS 주석·Git 행 회귀 기대 일치 |
| t103-post18-b-new.py | 37 | CR/LS/PS/FF/NEL 가짜 hunk·context·untracked·ESM 기대 일치 |
| t103-post19-b-new.py | 34 | CR/CRLF bytes·문단·fence·plain/--base 기대 일치 |
| t103-post20-b-new.py | 18 | 닫힌 LS/PS span 6건 포함 전부 기대 일치 |
| t103-post21-b-new.py | 29 | 25건 기대 일치, fence suffix LS/PS의 plain/--base 4건 오차단 |

합계 467개 관찰/OS다. unittest와 중복 합산하지 않는다. 저장된 Windows/WSL JSON 전체 행을 대조했으며 Unicode 데이터베이스 메타데이터 1행(16.0.0/14.0.0)만 다르고 판정·발견 행·입력 SHA256은 일치했다. CR/CRLF와 신규 사례는 write_bytes를 사용해 Windows 자동 개행 변환을 피했다.

## 누적 finding disposition

| 원 ID·심각도 | 판정 | 이번 재현 범위 |
|---|---|---|
| B-P1-01 | FIXED | root/CWD별 Git diff 대상 |
| B-P1-02 | FIXED | 앞쪽 추가에 의한 baseline 초과 |
| B-P1-03 | FIXED | 배열·삼항·tag·중첩 object·ESM·JSX·미종결 span 실행식, CR/CRLF 문단/fence |
| B-P1-04 | FIXED | 경로·값·argparse·JSON·Markdown·step summary redaction |
| B-P2-05 | FIXED | muted 추가 읽기 text 쌍 |
| B-P2-06 | FIXED | bool/소수/비유한/거대 정수/깊은 JSON |
| B-P3-07 | FIXED | geo 미달 8건 |
| B-P1-08 | FIXED | 추가 내용의 +++와 Git 헤더 구분 |
| B-P1-09 | FIXED | CSS 조건·specificity·순서·중첩·문자열·주석 |
| B-P2-10 | FIXED | airport 1.320934와 역사 1.15 구분 |
| B-P1-11 | FIXED | selector 인용 공백·대소문자 |
| B-P1-12 | FIXED | 빈 selector list·root descendant 오류 |
| B-P2-13 | FIXED | 파일 첫 span·3자 inline 인용 |
| B-P1-14 | FIXED | LS/PS JS 줄 주석·template 보간·중첩 JSX |
| B-P1-15 | FIXED | Git diff LF 분리·Unicode 가짜 hunk |
| B-P1-16 | FIXED | bare CR raw 읽기와 Git added-line 보존 |
| B-P2-17 | FIXED | LS/PS 포함 닫힌 1/2/3자 span, plain와 --base 모두 exit 0 |

B-P2-17은 원 LS/2자 입력 SHA256 9e647c68fa2ea96698bead7a80fae12cdb0b1ea2bd4e60d36ac4613fa6924b2e 및 PS/2자 b4383025c114ccc8b67ecb75c2e881bc67bf57efd7037b46047daa14271e1bfe를 다시 실행해 exit 0·발견 0으로 확인했다. LF/CR/CRLF 실제 빈 문단 뒤 JSX는 exit 1을 유지한다. bare CR 문단 뒤 ESM도 1/2자 미종결 span에서 P6/exit 1이다. FIXED는 실행한 반례 범위의 판정이며 모든 문법의 완전 검증을 뜻하지 않는다.

## 신규 B-P2-18 — fence 종료 suffix의 LS/PS를 공백처럼 지워 인용을 조기 종료

- 심각도: P2. disposition: OPEN, 수정 필요.
- 위치: tools/ux_lint.py:524의 not candidate[closing_run:].strip(), 함수 시작 :504.
- 계약: [T-103](../../../tasks/T-103-kt-contrast-ux-lint.md) 구현 범위 2와 수용 기준은 백틱/문서 인용을 제외한다. [CommonMark 0.31.2 §4.5](https://spec.commonmark.org/0.31.2/#fenced-code-blocks)(2024-01-28, 조회 2026-09-08)는 종료 fence 뒤에 허용하는 문자를 공백·탭으로 한정한다.
- 최소 입력: 임시 root의 Page.mdx에 다음 bytes를 쓴다. LS를 PS로 바꿔도 같다.

~~~python
from pathlib import Path
source = (
    "~~~tsx\nquoted\n~~~" + chr(0x2028)
    + '\n<div className="outline-none"/>\n~~~\n'
)
Path("TEMP_ROOT/Page.mdx").write_bytes(source.encode("utf8"))
~~~

- 명령: python -B -X utf8 CANDIDATE/tools/ux_lint.py --root TEMP_ROOT --fail-new --json. --base 대조는 별도 Git fixture의 Page.mdx 내용 safe+LF를 commit한 SHA를 --base로 추가한다.
- LS 입력 SHA256: 900cbc34efebac74b997fe110055bb4c82e6ee3148b699aea0fb3c342ea1a825.
- PS 입력 SHA256: 7d560181383149c5722b159a4076a44523b3f55b997fb5868dc224a27a087382.
- Windows 3.14·WSL 3.11 실제: plain/--base 모두 exit 1, status FAIL, P6 line 4, added true, traceback 없음.
- 기대: 3행은 suffix에 LS/PS가 있으므로 종료 fence가 아니며, 4행은 5행의 실제 종료까지 코드 인용이다. exit 0·발견 0이어야 한다.
- 대조: suffix를 ASCII 공백 또는 탭으로 바꾸면 3행이 정상 종료 fence가 되어 4행의 실제 JSX를 P6/exit 1로 판정한다. 두 대조는 양 OS에서 기대대로 동작했다.
- 원인과 영향: Markdown 줄 종료 helper는 분리됐지만 Python의 인자 없는 strip()은 LS/PS도 없앤다. 따라서 코드 예제 내부를 런타임 위반처럼 보고해 소비자 이관의 --fail-new gate를 부당하게 차단한다. 실행 위반 우회로 확대하지 않고 재현된 오차단에 맞춰 P2로 분류했다.
- 수정 권고: fence suffix를 CommonMark에서 허용한 ASCII 공백·탭만으로 검사한다. 별도로 일반 lstrip()/strip()을 사용하는 fence 시작·들여쓰기 경계도 같은 문법 기준인지 확인하되, 검증하지 않은 경계를 이번 finding에 추가하지 않는다. 기존 LF/CR/CRLF 문단·fence와 LS/PS JS 주석 처리는 유지한다.
- 원인 경계: 해당 suffix strip 조건은 base에도 존재하며 이번 delta에서 새로 추가된 줄은 아니다. 이번 CommonMark/ECMAScript 분리 검토에서 발견한 후보의 잔여 결함이다. base CLI의 같은 입력 재실행은 NOT_RUN이며 base 코드의 동일 조건만 직접 확인했다.

## 문서·범위 및 NOT_RUN

[T-103](../../../tasks/T-103-kt-contrast-ux-lint.md)·[resume](../../../resume.md)은 IN_PROGRESS다. [evidence](../../../evidence/t103-kt-contrast-ux-lint.md)는 airport 현재 1.320934와 역사 1.15를 분리하고, 소비자 실행과 후행 T-010 workflow selftest를 NOT_RUN으로 둔다. geo 예제 8건, canonical 27쌍, 4앱 예제와 baseline 대조를 실행했다. GPL-3.0-or-later 헤더와 common 도구 범위를 유지한다.

- NOT_RUN(Windows Python 3.11): 설치되지 않았다. Windows 3.14 결과와 구분한다.
- NOT_RUN(WSL skip 3): Windows 8.3 경로 1개, jsonschema 미설치로 schema 대조 2개. 나머지 288개 실행과 구분했다.
- NOT_RUN(exact candidate 원격 CI 독립 조회): 로컬 성공을 CI 성공으로 세지 않는다.
- NOT_RUN(MDX compiler/browser): JS 표현식 Node 대조는 실행했으나 전체 MDX 컴파일·렌더는 하지 않았다. 신규 P2는 공식 문법과 CLI 재현에 근거한다.
- NOT_RUN(소비자 build/e2e·실제 앱 baseline·registry·npm/PyPI 게시·workflow dispatch·T-010 selftest): common 리뷰 범위 밖이며 실행하지 않았다.
- NOT_RUN(uv 전면 명령을 통한 전체 중복 실행): 같은 uv Python 3.11로 전체 시험을 직접 실행했고 focused만 uv run으로 확인했다.
- NOT_RUN(non-UTF8 Git 출력 주입): 이번 직접 입력은 UTF-8 bytes다.

신규 P2가 열려 있으므로 PASS로 확정하지 않는다. 위 검토 종료 제품 SHA/tree는 변경하지 않았고, 이후 원본 한 파일만 추가하는 commit을 전달한다.
