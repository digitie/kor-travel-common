# T-103 수정 후 독립 적대적 리뷰 28 — Reviewer A

- 실행 ID: T103-POST28-A-20260908-161121-KST
- 판정: **NO-GO**. 신규 finding A-P2-24(P2) 1건, P0/P1/P3 0건.
- 제품 candidate: 71a6f99de297e809c165f005d4d6b1753468d157
- 제품 tree: b0ba565c1fe6d6002c7a983307853f2bb1999c39
- delta base: 009ec5dcf70e55b6c736ccaeabbfeb71a08836f6
- 공통 manifest: commit f661de2의 docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-28-manifest.md를 git show로 읽었다. 제품 candidate에는 아직 없는 별도 commit 문서다.
- 격리: F:/dev/kor-travel-common-wt/review-t103-post28-a, detached.
- 시작: 2026-09-08 16:11:21.720 KST. 제품 검증 종료: 2026-09-08 16:18:52.198 KST.
- 시작/종료 HEAD·tree는 위 candidate와 일치하며 git status --porcelain=v1 출력 없음.
- 상대 reviewer 원본·결과는 읽거나 요청하지 않았다. 제품·manifest·공유 branch·소비자·기존 evidence·git config는 수정하지 않았다. 검증 종료 후 이 원본 한 파일만 report-only commit한다.

## 전달 요청 원문

> post-fix-28 독립 적대적 리뷰를 시작해 주세요. 코드 후보 71a6f99de297e809c165f005d4d6b1753468d157, tree b0ba565c1fe6d6002c7a983307853f2bb1999c39, manifest f661de2의 docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-28-manifest.md입니다. 전문 범위는 CommonMark blockquote/fence와 invalid backtick info fallback, inline span 경계·P6/P8, nested·CR/LF/CRLF입니다. 이전 post-28 B 결과/raw를 읽지 말고 독립 검증하세요. 후보/manifest/공유 branch/소비자/기존 evidence는 수정하지 말고 자신의 worktree에 docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-28-reviewer-a.md만 작성해 report-only commit을 만드세요. PASS/NO-GO와 commit SHA/SHA-256을 회신하세요.

> post-fix-28 리뷰를 지금 실행하고 원본 report-only commit까지 완료해 주세요.

원문의 코드 표시용 backtick만 일반 텍스트로 옮겼다.

## 범위와 독립 판단

전체 delta 5파일 중 제품인 tools/ux_lint.py와 tests/test_ux_lint.py 전체 diff를 읽었다. 나머지 3파일은 직전 manifest 및 A/B 원본 보존이다. 상대 원본 본문은 읽지 않았다. AGENTS·문서 라우터·resume·T-103의 수용 기준을 재확인하고, 변경 없는 정본/코드의 이전 읽기는 동일성 대조로 재사용했다. 실제 full/focused/static 및 직접 corpus는 이번 candidate에서 다시 실행했다.

무효 fence 뒤 별도 block opener를 inline 닫힘으로 연결하지 않는 수정 방향은 유효하다. 그러나 이번 구현은 같은 줄의 backtick을 전부 공백으로 바꾸면서 정상 inline code까지 노출한다. T-103의 백틱 인용 제외 계약과 충돌한다.

## A-P2-24 — 무효 fence 처리로 정상 closed inline code가 위반으로 보고됨

- 심각도: P2. disposition: **OPEN / FIX_REQUIRED**. 이번 candidate에서 새로 도입된 오탐 회귀.
- 위치: tools/ux_lint.py:626–634의 _mask_mdx_fence. 직접 관련 시험은 tests/test_ux_lint.py:452의 신규 양성만 검사하며 정상 inline 음성 대조가 없다.
- 계약: docs/tasks/T-103-kt-contrast-ux-lint.md:22·39의 백틱 인용 제외와 양성/음성 fixture 수용 기준.
- 근거: [CommonMark 0.31.2 §4.5 Example 145](https://spec.commonmark.org/0.31.2/#example-145)는 backtick을 포함한 info-string이 inline code로 해석되는 예를 명시한다. [§6.1 code spans](https://spec.commonmark.org/0.31.2/#code-spans)는 같은 길이 delimiter와 줄 연결을 정의하며 [block 우선순위](https://spec.commonmark.org/0.31.2/#precedence)는 별도 fence block을 구분한다. revision 2024-01-28, 조회 2026-09-08. Windows의 기존 markdown-it-py 4.2.0 기본 CommonMark도 아래 두 음성 사례를 code_inline으로 해석했다.

### 최소 재현과 실제 출력

임시 root의 case.mdx 내용을 다음 Python 문자열로 만들고 CLI를 실행한다. 후보 파일은 수정하지 않는다.

~~~python
body = '```<div className="outline-none"/> {window.confirm("quoted")}```'
body_multiline = '```bad`info\n{window.confirm("quoted")} ```'
~~~

명령: python -B -X utf8 tools/ux_lint.py --root <임시-root> --fail-new --json. WSL은 uv run --no-project --python 3.11을 앞에 사용했다.

| 입력 | 기대 | base 009ec5d Windows | candidate 양 OS |
|---|---|---|---|
| body | exit 0, findings 0 | exit 0, findings 0 | exit 1, P6 line 1·P8 line 1 |
| body_multiline | exit 0, findings 0 | exit 0, findings 0 | exit 1, P8 line 2(LF) |
| 무효 info 줄 → P8 줄 → 단독 3자 delimiter 줄 | exit 1, P8 line 2 | exit 0으로 누락 | exit 1, P8 line 2로 수정 |

세 번째 입력은 별도 fence block이 앞 문단을 종료하므로 실제 P8을 검출해야 한다. 첫 두 입력은 정상 닫힌 inline code이므로 인용 안 내용을 검출하면 안 된다. 단순히 새 수정을 되돌리면 세 번째 원인도 다시 발생한다.

본인 t103-post28-inline-a.py에서 delimiter 1/2/3/4자, same-line/same-paragraph/outside-positive, plain/blockquote/nested, LF/CRLF/CR 총 99개를 양 OS에 실행했다. 63개 대조는 기대 일치, 3·4자 정상 span 36개는 모두 오탐이다. 같은 줄은 P6/P8 모두, 같은 문단 다중행은 P8을 잘못 보고한다.

추가로 t103-post28-base-a.py가 별도 임시 Git repo에 일반 문서를 commit한 뒤 정상 인용 예제를 새 행으로 추가하고 --base <fixture-sha> --json을 실행했다. 양 OS 실제 exit 1, fail_count 2, P6/P8 added=true·fail=true·line=1이다. 기대는 exit 0, finding 0이다. 문서 예제를 추가하는 실제 diff gate가 잘못 차단된다.

### 영향과 최소 수정 수용 기준

정상 MDX 예제의 3자 이상 backtick 인용을 사용하는 문서 변경이 --fail-new 및 --base에서 차단된다. quoted 예제에 나타난 모든 금지 패턴에 영향을 줄 수 있다.

무효 fence 판정 후에도 inline 구문을 정상 처리해야 한다. 같은 줄/문단의 유효한 동일 길이 span은 유지하고, 다음 줄의 실제 block fence처럼 문단을 끝내는 경계만 inline 닫힘 후보에서 제외한다. delimiter 일괄 삭제는 제거한다. 위 36개 음성, 63개 대조, 별도 fence block 앞 실제 P8 양성을 함께 고정한다. plain·quote·nested, CR/LF/CRLF, --base를 포함해 양 OS에서 재검토해야 한다.

## 실제 검증 명령과 결과

모든 제품 검증은 위 detached candidate에서 수행했다. helper/log는 기본 checkout .git/codex-audit의 본인 파일, 입력 fixture는 별도 임시 디렉터리를 사용했다. Windows 전체 시험 TEMP/TMP와 WSL TMPDIR은 각각 독립 경로다. WSL 정적 Git gate에만 프로세스 GIT_DIR/GIT_WORK_TREE를 지정했고 config를 바꾸지 않았다.

| 명령/검증 | Windows Python 3.14.3 | WSL Python 3.11.15 |
|---|---|---|
| python -B -X utf8 -m unittest discover -s tests -p 'test_*.py' -v | 301 통과, skip 0, 203.072초 | 아래 명령: 301 수집, 300 통과, skip 1, 68.989초 |
| python -B -X utf8 -m unittest tests.test_kt_contrast tests.test_ux_lint | 63 통과, 59.797초 | 63 통과, 21.896초 |
| tools/validate_document_links.py | 475문서·2464대상, 오류 0 | 동일 |
| tools/validate_plan.py | 106 task, 오류 0 | 동일 |
| tools/check_spdx.py | 56파일, 오류 0 | 동일 |
| tools/scan_secrets.py --all | 607파일, 발견 0 | 동일 |
| tools/check_prod_redaction.py --all | 607파일, 발견 0 | 동일 |
| tools/check_versions.py --self-check | 자체 검사 통과, 소비자 NOT_RUN | 동일 |
| tools/check_aliases.py packages/tokens/aliases | CSS 1개, 오류 0 | 동일 |
| tools/kt_contrast.py packages/tokens/tokens.css --json | light 27쌍 PASS | 동일 |
| tools/ux_lint.py --root tests/fixtures/ux --json | 의도된 report finding 12개, fail_count 0 | 동일 |
| git diff --check 009ec5d 71a6f99 | 출력 없음 | 출력 없음 |

표의 tools 명령에는 python -B -X utf8을 사용했다. WSL 전체 명령은 uv run --no-project --python 3.11 --with jsonschema python -B -X utf8 -m unittest discover -s tests이며 그 외 Python 명령은 uv run --no-project --python 3.11을 사용했다. WSL skip 1은 Windows 8.3 경로 API 전용 시험이며 통과로 세지 않았다.

전체/focused 시험은 통과하지만 위 A-P2-24 반례를 포함하지 않으므로 승인 근거로 삼지 않았다.

## 누적 직접 corpus와 기존 disposition

각 helper는 python -B -X utf8 <.git/codex-audit/helper.py> <detached-root>로 실행했다. WSL은 같은 helper를 uv Python 3.11에서 실행했다.

| helper | 양 OS 관찰 |
|---|---|
| t103-post17-reviewer-a-probe.py | Windows 264행·WSL 263행, CSS/JSON/오류/redaction/symlink/airport 및 MDX Unicode·FEFF·async·주석 누적 원 반례 출력이 직전 후보와 동일 |
| t103-post19-margins-a.py | 21개 Markdown 줄 경계·ESM 출력 동일 |
| t103-post18-diff-a.py | 10개 Unicode/CR/가짜 hunk의 실제 추가 P8 mapping 동일 |
| t103-post19-mapping-a.py | 15개 plain/tracked/untracked source mapping 동일 |
| t103-post21-boundary-a.py | 44개, failures 0 |
| t103-post22-fence-a.py | 102개, failures 0 |
| t103-post23-opener-a.py | 120개, failures 0 |
| t103-post24-info-a.py | 84개, failures 0 |
| t103-post25-container-a.py | 42개, failures 0 |
| t103-post26-padding-a.py | 72개 실행, 기존 유효 69개 일치. content4 backtick opening 3개는 아래 제한 |
| t103-post26-literal-a.py | 6개, 외부 P8만 검출 |
| t103-post27-cli-a.py | 120개 marker/tab/nested 조합, failures 0 |
| t103-post28-inline-a.py | 99개 중 정상 span 36개 오탐, 나머지 63개 일치 |
| t103-post28-base-a.py | 양 OS 정상 인용 신규 행을 fail_count 2로 오탐 |

새 helper SHA256: t103-post28-inline-a.py = 065886C0886C640E118AAEBDFB9FBC1DBE1D841F020C09824275E9950698DC96, t103-post28-base-a.py = DFAE49DA52164ECD3ADD7CDE9474D998EBC9B67405D98421E1C99E0FD712DEE3.

기존 원 finding 21건의 원 반례는 다음과 같다. FIXED는 해당 원 반례에 한정하며 새 정상 span 회귀 A-P2-24를 덮지 않는다.

| 원 ID | 원 심각도 | disposition |
|---|---|---|
| A-P1-01·02·03·04·05 | 각 P1 | FIXED — CSS scope/cascade, OKLCH percent, alpha, baseline 추가, 외부 root |
| A-P2-06·07·08·09·10·11 | 각 P2 | FIXED — 기존 MDX 원 corpus, 옵션 base, 파일명, JSON, 출력 비공개, 읽기 표면 |
| A-P3-12 | P3 | FIXED — geo/airport 수치와 역사 구분 |
| A-P1-13 | P1 | FIXED — diff +++ source |
| A-P2-14·15 | 각 P2 | FIXED — self-symlink root·깊은 JSON |
| A-P1-16 | P1 | FIXED — Unicode/CR·가짜 hunk 추가 행 |
| A-P2-19 | P2 | FIXED — plain fence 들여쓰기 |
| A-P1-20·21 | 각 P1 | FIXED — backtick info 금지 원 반례·container 종료 |
| A-P2-22 | P2 | FIXED — content4 closing |
| A-P1-23 | P1 | FIXED — marker 선택 공백/tab-stop |

## 원격 확인·재사용·NOT_RUN

- gh run list --commit 71a6f99de297e809c165f005d4d6b1753468d157 --json databaseId,headSha,status,conclusion,url --limit 5: [CI 34197631092](https://github.com/digitie/kor-travel-common/actions/runs/34197631092)의 exact head·completed/success를 직접 확인했다. 개별 job 원문 로그 감사와 workflow dispatch는 NOT_RUN.
- Windows Python 3.11: NOT_RUN(실행 파일 부재). Windows 3.14 결과를 대신 통과로 표시하지 않는다.
- Windows에서 허용되지 않는 탭 파일명은 NOT_RUN, 해당 corpus는 WSL에서 실행했다. WSL Windows 8.3 API 시험은 skip으로 보존했다.
- padding helper의 3개 content4 backtick opening은 일반 CommonMark와 MDX indented-code 미지원의 차이가 있어 직전과 동일하게 판정에서 분리했다. 이 미해결 oracle 범위를 새 성공으로 집계하지 않는다. 실제 MDX compiler/browser는 NOT_RUN. 이번 finding의 정상 code span은 공식 CommonMark의 명시적 규칙과 독립 parser 양쪽으로 확인했다.
- 변경 없는 규칙과 코드의 읽기는 이전 검토와 diff 동일성으로 재사용했다. 별도 3,372개 참조 조합 전체를 이번에는 다시 실행하지 않았다. 변경된 fallback 경계에는 99개 직접 반례 및 --base 대조를 새로 실행했다.
- 소비자 build·type/e2e·소비자 manifest 검사, npm/PyPI registry 설치/게시: NOT_RUN(허용 범위 밖). 소비자 저장소를 수정하지 않았다.

## 최종 판정

**NO-GO — A-P2-24 FIX_REQUIRED.** 정상 closed inline code의 인용 제외 계약이 회귀했다. 후보는 고치지 않았으며 원본 한 파일을 immutable report-only commit으로 확정하고 commit SHA·원본 blob SHA256을 완료 메시지로 전달한다.
