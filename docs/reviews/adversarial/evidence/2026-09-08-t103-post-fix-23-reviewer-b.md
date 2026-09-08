<!-- SPDX-License-Identifier: GPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie) -->

# T-103 post-fix-23 독립 적대적 리뷰 B 원본

- 실행 ID: T103-POST23-B-20260908-143918
- 판정: **PASS**. 신규 P0/P1/P2/P3 0건. 기존 B finding 19개는 이번 재현 범위에서 FIXED.
- 시작 KST: 2026-09-08T14:39:18.7255717+09:00
- 제품 검토 종료 KST: 2026-09-08T14:42:51.5951566+09:00
- 시작/종료 제품 HEAD: 3a8b569889fcaf4429cc70a7bafec779181aac6f
- 시작/종료 제품 tree: f72134340a7da31e3ad756bcbde215342fef80fc
- 시작/종료 제품 상태: detached, git status --porcelain=v1 --untracked-files=all 출력 없음.
- 격리: F:/dev/kor-travel-common-wt/review-t103-post23-b. 전체 시험·정적 gate는 후보의 임시 사본, focused는 후보 worktree, Git 반례는 GIT_* 환경을 제거한 별도 임시 Git 저장소에서 실행했다.
- manifest commit: b68c07be7e1fec924ee85e5a1f7c155cb276c17b. [공통 manifest](2026-09-08-t103-post-fix-23-manifest.md)를 git show로 읽었다.
- manifest Git blob SHA256: 25ebd5a8beb1bcb911f116d328c920cae2ad73cda5f00c81d3f826af951a2b4e
- delta 기준: 61f1cc6a900e25268e0c5eadc32ce1c5ccc9d3f3.
- 소스 .git/config 시작/종료 SHA256: 0A0F849E7874CF0A25926856F9D2E381CCBF4C2DCB5999869C57B86E0F5BEB5B. 설정 변경 없음.
- 상대 reviewer 결과·raw 및 기존 raw 본문을 읽거나 요청하지 않았다. 후보·manifest·소비자·기존 evidence를 변경하지 않았다. 제품 검토 종료 뒤 이 원본 한 파일만 별도 commit한다.

## 요청 원문과 범위

“T-103 post-fix-23 독립 적대적 리뷰를 시작해 주세요. immutable 제품 후보는 commit 3a8b569889fcaf4429cc70a7bafec779181aac6f, tree f72134340a7da31e3ad756bcbde215342fef80fc; 공통 manifest는 commit b68c07be7e1fec924ee85e5a1f7c155cb276c17b의 docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-23-manifest.md입니다. 별도 detached worktree F:/dev/kor-travel-common-wt/review-t103-post23-b에서 candidate와 clean을 확인하세요. 전문 범위는 Git added-line/base·입력 오류·redaction·JSON/오류 채널·문서/task/scope 정합과 fence indentation/tab-stop·suffix·CR/CRLF 경계입니다. 최소 반례와 전체 변경을 코드/문서로 다시 확인하고 작성자 evidence를 맹신하지 마세요. 상대 reviewer 결과·raw는 읽거나 요청하지 말고, 제품·manifest·소비자·기존 evidence를 수정하지 마세요. 본인 원본 docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-23-reviewer-b.md 한 파일만 작성해 report-only commit으로 확정하세요. 실행 ID/시각/요청 원문/실제 SHA·tree·clean/명령/검증/NOT_RUN/각 finding disposition/verdict(PASS 또는 NO-GO)를 포함하고 commit hash와 SHA256을 부모에게 보내 주세요. 후보에 수정이 필요하면 먼저 NO-GO로 원본을 확정하고 작업을 멈추세요.”

tools/ux_lint.py·tests/test_ux_lint.py의 전체 제품 delta를 읽었다. _markdown_indent_columns의 탭 정렬 계산과 3열 상한, 열기·닫기 적용 위치를 확인했다. Git raw 출력·UTF-8 오류·added_lines·미추적 파일 LF 행 집계·root containment 코드를 다시 읽고 실제 CLI 반례와 대조했다. delta의 과거 raw 경로는 파일 목록만 확인하고 본문은 읽지 않았다.

## 실제 명령과 검증 결과

Windows Python 3.14.3·Node v25.9.0, WSL Python 3.11.15·Node v22.22.2다. WSL은 /home/digitie/.local/share/uv/python/cpython-3.11-linux-x86_64-gnu/bin/python3.11을 사용했다. 작성자의 manifest 성공 횟수는 아래 실행 횟수에 합산하지 않았다.

| 검증 | Windows | WSL |
|---|---|---|
| 전체 unittest discover -s tests -p test_*.py | 293개 성공, skip 0, 159.643초 | 293개 수집, 290개 성공, skip 3, 43.573초 |
| tests.test_kt_contrast + tests.test_ux_lint | 55개 성공, skip 0, 39.280초 | 55개 성공, skip 0, 23.916초 |
| 별칭 focused unittest | 35개 성공, skip 0 | 35개 수집, 34개 성공, skip 1 |
| validate_plan.py | task 106개, 오류 0 | 동일 |
| validate_document_links.py | 문서 460개, 대상 2435개, 오류 0 | 동일 |
| check_spdx.py | 파일 56개, 오류 0 | 동일 |
| scan_secrets.py --all | 파일 592개, 발견 0, 명시적 예외 0 | 동일 |
| check_prod_redaction.py --all | 파일 592개, 발견 0, 명시적 예외 0 | 동일 |
| check_versions.py --self-check | 레지스트리 자체 검사 exit 0 | 동일 |
| check_aliases.py packages/tokens/aliases | CSS 1개, 오류 0 | 동일 |
| kt_contrast.py packages/tokens/tokens.css --json | exit 0, 27쌍 | 동일 |
| ux_lint.py --root tests/fixtures/ux --json | report exit 0, 의도된 발견 12개, fail_count 0 | 동일 |
| git diff --check 기준..후보 | exit 0 | exit 0 |

모든 Python 실행에 -B -X utf8을 사용했다. 전체/정적 gate는 .git/codex-audit/review-t102-b-wsl-unittest.py 및 review-t102-post-b-gates.py에 정확한 후보 경로를 전달해 임시 사본에서 실행했다. focused는 -m unittest tests.test_kt_contrast tests.test_ux_lint로 후보에서 직접 실행했다. -v 없이 같은 시험 집합을 실행했으며 0 test·skip을 성공으로 계산하지 않았다.

WSL diff 명령은 git --git-dir=/mnt/f/dev/kor-travel-common/.git --work-tree=/mnt/f/dev/kor-travel-common-wt/review-t103-post23-b diff --check 61f1cc6a900e25268e0c5eadc32ce1c5ccc9d3f3 3a8b569889fcaf4429cc70a7bafec779181aac6f였다. 명령별 경로 지정이며 core.worktree 설정 변경이 아니다.

아래 .git/codex-audit의 독립 probe를 양 OS에서 후보 경로 인자로 실행했다. 재사용한 것은 스크립트이며 결과는 현재 후보에서 새로 얻었다. 과거 raw 본문은 사용하지 않았다.

| 스크립트 | OS별 관찰 수 | 결과 |
|---|---:|---|
| t103-post9-b-corpus.py | 105 | 입력·baseline·CSS·diff·redaction·MDX 기대 일치 |
| t103-post15-b-late-corpus.py | 140 | 표현식·인용·문단·CSS comment-gap·4앱 기대 일치 |
| t103-post17-b-latest-corpus.py | 104 | Unicode·FEFF·async·JS 주석·Git 행 기대 일치 |
| t103-post18-b-new.py | 37 | CR/LS/PS/FF/NEL 가짜 hunk·context·untracked 기대 일치 |
| t103-post19-b-new.py | 34 | CR/CRLF bytes·문단·fence·plain/--base 기대 일치 |
| t103-post20-b-new.py | 18 | 닫힌 LS/PS 1/2/3자 span 대조 기대 일치 |
| t103-post21-b-new.py | 29 | fence suffix ASCII space/tab/LS/PS 기대 일치 |
| t103-post22-b-new.py | 28 | 0/1/3열 양성, 4칸/tab·LS/PS prefix 음성 기대 일치 |
| t103-post23-b-new.py | 48 | 2칸/공백+tab/3칸+tab/tab+공백 × LF/CR/CRLF × tilde/backtick × plain/--base 기대 일치 |

합계 543개 관찰/OS다. unittest 개수와 합산하지 않는다. Windows/WSL JSON 전체 행을 대조했으며 Unicode 데이터베이스 메타데이터 1행(16.0.0/14.0.0)만 다르고 판정·입력 SHA256·발견 위치는 같았다. 새 직접 반례는 write_bytes로 기록해 CR/CRLF의 실제 bytes를 보존했다.

## 각 finding disposition

| 원 ID·심각도 | 판정 | 이번 재현 범위 |
|---|---|---|
| B-P1-01 | FIXED | root/CWD와 Git diff 대상 선택 |
| B-P1-02 | FIXED | 앞쪽 추가로 baseline 건수를 넘기는 경우 |
| B-P1-03 | FIXED | 배열·삼항·tag·중첩 object·ESM·JSX·미종결 span 실행식, CR/CRLF 문단/fence |
| B-P1-04 | FIXED | 경로·값·argparse·JSON·Markdown·step summary redaction |
| B-P2-05 | FIXED | muted 추가 읽기 text 4쌍 |
| B-P2-06 | FIXED | baseline bool/소수/비유한/거대 정수/깊은 JSON 오류 |
| B-P3-07 | FIXED | geo 예제 미달 8건 |
| B-P1-08 | FIXED | +++ 추가 내용과 Git 헤더 구분 |
| B-P1-09 | FIXED | CSS 조건·specificity·순서·중첩·문자열·주석 |
| B-P2-10 | FIXED | airport 현재 1.320934와 역사 1.15 분리 |
| B-P1-11 | FIXED | selector 인용 공백·대소문자 |
| B-P1-12 | FIXED | 빈 selector list·root descendant 입력 오류 |
| B-P2-13 | FIXED | 파일 첫 span·3자 inline 인용 |
| B-P1-14 | FIXED | LS/PS JS 줄 주석·template 보간·중첩 JSX |
| B-P1-15 | FIXED | Git diff LF 분리·Unicode 가짜 hunk |
| B-P1-16 | FIXED | bare CR raw 읽기와 added-line 좌표 보존 |
| B-P2-17 | FIXED | 닫힌 LS/PS 1/2/3자 span plain·--base |
| B-P2-18 | FIXED | fence suffix LS/PS 거부, ASCII space/tab 허용 |
| B-P2-19 | FIXED | 4열 이상 종료 fence 거부, 0~3열 허용, tab-stop·CR/CRLF |

B-P2-19의 원 tilde/4칸 입력 SHA256 895daec1a47f84813e4459494f7f96a6b54b3dd400d1098455adca2024ce8679와 tilde/tab a452f7feb209889fd89bc16113fcf5641ac99be7acb73812654050a04b8f5705는 plain·--base 모두 exit 0·발견 0이다. backtick/4칸 b2c4d7b3dcdfbc775856aab9689c79d00022e05fbe81a249d9334e0a1da811bf 및 backtick/tab 273ea08253a7234633fcb57e1e8264d772baf27d57de9dc1b28da2c4fda48930도 동일하다.

최소 입력은 marker×3 + tsx + LF + quoted + LF + 4칸 또는 tab + marker×3 + LF + outline-none JSX + LF + marker×3 + LF다. 이전에는 내부 JSX를 P6로 오차단했지만 현재는 실제 마지막 fence까지 인용을 유지한다. 새 LF/CR/CRLF 교차 대조에서 2칸은 P6/exit 1, 공백+tab·3칸+tab·tab+공백은 exit 0이다. 추가 행 판정은 LF 기반이므로 bare CR 입력의 실제 발견 위치 line 1도 plain/--base에서 일치한다.

신규 finding은 없다. FIXED와 PASS는 위 독립 코드 검토·실행 범위에 대한 판정이며 모든 Markdown/JavaScript 문법 또는 소비자 제품의 완전 검증을 뜻하지 않는다.

## 문서·범위 및 미실행

[T-103](../../../tasks/T-103-kt-contrast-ux-lint.md)·[resume](../../../resume.md)은 IN_PROGRESS다. [evidence](../../../evidence/t103-kt-contrast-ux-lint.md)는 airport 현재 1.320934와 조사 당시 1.15를 구분하며, 실제 소비자 build/e2e·후행 T-010 재사용 workflow 자체 시험을 NOT_RUN으로 둔다. 4앱 조사 예제와 baseline·geo 8건을 실행했고 이 결과를 실제 소비자 채택 증거로 보지 않았다. GPL-3.0-or-later와 common 공용 도구 범위를 유지한다.

- NOT_RUN(Windows Python 3.11): 설치되지 않았다. Windows 3.14 결과와 구분한다.
- NOT_RUN(WSL skip 3): Windows 8.3 경로 1개 및 선택한 Python 환경의 jsonschema 대조 2개. manifest의 coordinator WSL skip 1과 이번 독립 환경의 skip 3을 혼동하지 않는다.
- NOT_RUN(exact candidate 원격 CI 독립 조회): 로컬 gate 성공을 CI 성공으로 집계하지 않았다.
- NOT_RUN(실제 MDX compiler/browser·CommonMark parser 의존성 실행): 새 의존성을 추가하지 않았다. 공식 규격과 코드·CLI 양성/음성 대조를 사용했다.
- NOT_RUN(소비자 build/e2e·실제 앱 baseline·소비자 manifest 검증·npm/PyPI registry 설치/게시·workflow dispatch·T-010 selftest): 요청 범위 밖이며 호출하지 않았다.
- NOT_RUN(non-UTF8 Git 출력 주입): 해당 오류 처리 코드는 읽었지만 이번 직접 입력은 UTF-8 bytes다.

검토 범위의 누적 finding이 모두 닫혔고 새로운 P0~P3가 없어 PASS로 확정한다. 제품 검토 종료 이후 이 원본 한 파일만 추가한 commit을 부모에게 전달하며 제품 후보와 Git 설정을 보존한다.
