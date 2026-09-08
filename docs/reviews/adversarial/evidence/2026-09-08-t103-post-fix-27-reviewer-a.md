# T-103 수정 후 독립 적대적 리뷰 27 — Reviewer A

- 실행 ID: T103-POST27-A-20260908-155221-KST
- 판정: **PASS**. 신규 P0/P1/P2/P3 각 0건. 누적 A 원 finding 21건의 원 반례는 FIXED.
- 제품 candidate: 009ec5dcf70e55b6c736ccaeabbfeb71a08836f6
- 제품 tree: f521d07dd7566744659522186a4add8f01d7150b
- delta base: 2a32dc7e07a4c36e2b0e92402f05019b31f6c3cb
- 공통 manifest: commit 64505d7의 docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-27-manifest.md, git show로 읽음. 제품 candidate에는 아직 없는 별도 manifest commit이므로 로컬 링크를 만들지 않았다.
- 격리: F:/dev/kor-travel-common-wt/review-t103-post27-a detached worktree.
- 시작: 2026-09-08 15:52:21.072 KST. 종료: 2026-09-08 15:59:46.211 KST.
- 시작/제품 검증 종료 HEAD와 tree는 위 candidate와 일치. 양 시점 git status --porcelain=v1 출력 없음.
- 상대 reviewer 원본·결과는 읽거나 요청하지 않았다. 제품·manifest·소비자·기존 evidence·git config는 수정하지 않았다. 제품 검토 종료 후 이 원본 파일 하나만 별도 commit한다.

## 전달 요청 원문

> post-fix-27 독립 적대적 리뷰를 시작해 주세요. 코드 후보 009ec5dcf70e55b6c736ccaeabbfeb71a08836f6, tree f521d07dd7566744659522186a4add8f01d7150b, manifest 64505d7의 docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-27-manifest.md입니다. 전문 범위는 CommonMark blockquote marker 선택 공백·tab-stop, fence opener/closer 콘텐츠 0~3열·4열, nested/depth 감소·빈 줄·CR/LF/CRLF와 P6/P8 회귀입니다. 이전 post-27 B 결과/raw를 읽지 말고 독립 검증하세요. 후보/manifest/공유 branch/소비자/기존 evidence는 수정하지 말고, 자신의 worktree에 docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-27-reviewer-a.md만 작성해 report-only commit을 만드세요. PASS/NO-GO와 commit SHA/SHA-256을 회신하세요.

> post-fix-27 리뷰를 지금 실행하고 원본 report-only commit까지 완료해 주세요. 동일 immutable code candidate에서 독립적으로 검증하세요.

원문의 코드 표시용 backtick만 일반 텍스트로 옮겼다.

## 직접 검토한 범위와 결정 근거

전체 delta는 5파일이다. 제품 변경 tools/ux_lint.py와 tests/test_ux_lint.py의 전체 diff를 읽었다. 나머지 3파일은 직전 manifest 및 A/B 원본 보존이며 상대 원본 본문은 독립성 때문에 제외했다. AGENTS, 문서 라우터, resume, T-103 상세 task를 다시 확인했다. 변경 없는 CSS·대비·JSON·오류 처리 코드/규칙은 이전 읽기와 이번 동일성 대조를 재사용하고, 실제 회귀 명령은 이번 candidate에서 다시 실행했다.

tools/ux_lint.py의 _markdown_consume_marker_padding은 marker 뒤 선택 공백 한 열을 콘텐츠에서 제외하며 tab을 실제 열의 다음 4열 경계로 전개한다. _markdown_fence_container와 _markdown_fence_candidate가 동일한 계산을 사용한다. 마지막 marker 뒤 콘텐츠 4열은 fence body로 남기고, 중간 marker 앞 4열은 해당 인용 깊이의 종료로 처리한다.

규범 대조는 CommonMark 0.31.2(2024-01-28)의 [block quote marker](https://spec.commonmark.org/0.31.2/#block-quotes), [tab](https://spec.commonmark.org/0.31.2/#tabs), [fence](https://spec.commonmark.org/0.31.2/#fenced-code-blocks) 정의를 조회일 2026-09-08에 직접 확인했다. 선택 공백과 최대 3열 들여쓰기를 구분하는 후보 계산과 일치한다. [MDX 공식 Markdown 차이](https://mdxjs.com/docs/what-is-mdx/#markdown)(문서 갱신 2025-01-27, 조회 2026-09-08)의 indented code 미지원은 일반 CommonMark와 분리했다.

## 명령과 실제 결과

명령은 이 detached worktree에서 실행했다. 임시 입력은 별도 임시 디렉터리, 본인 helper/log는 기본 checkout의 .git/codex-audit에만 작성했다. Windows 전체 시험은 독립 TEMP/TMP, WSL 전체 시험은 독립 TMPDIR로 실행해 병렬 reviewer fixture 충돌을 피했다.

| 명령/검증 | Windows Python 3.14.3 | WSL Python 3.11.15 |
|---|---|---|
| python -B -X utf8 -m unittest discover -s tests -p 'test_*.py' -v | 300 통과, skip 0, 194.832초 | 아래 WSL 명령으로 300 수집, 299 통과, skip 1, 62.935초 |
| python -B -X utf8 -m unittest tests.test_kt_contrast tests.test_ux_lint | 62 통과, 60.772초 | 62 통과, 19.807초 |
| tools/validate_document_links.py | 472문서·2458대상, 오류 0 | 동일 |
| tools/validate_plan.py | 106 task, 오류 0 | 동일 |
| tools/check_spdx.py | 56파일, 오류 0 | 동일 |
| tools/scan_secrets.py --all | 604파일, 발견 0 | 동일 |
| tools/check_prod_redaction.py --all | 604파일, 발견 0 | 동일 |
| tools/check_versions.py --self-check | 자체 검사 통과, 소비자 NOT_RUN | 동일 |
| tools/check_aliases.py packages/tokens/aliases | CSS 1개, 오류 0 | 동일 |
| tools/kt_contrast.py packages/tokens/tokens.css --json | light 27쌍 PASS | 동일 |
| tools/ux_lint.py --root tests/fixtures/ux --json | report의 의도된 finding 12개, fail_count 0 | 동일 |
| git diff --check 2a32dc7 009ec5d | 출력 없음 | 출력 없음 |

표의 tools 명령에는 python -B -X utf8을 사용했다. WSL 전체 명령은 uv run --no-project --python 3.11 --with jsonschema python -B -X utf8 -m unittest discover -s tests이며, 그 외 Python 명령은 uv run --no-project --python 3.11 뒤에 실행했다. WSL의 Git 기반 정적 gate만 프로세스 환경 GIT_DIR/GIT_WORK_TREE로 이 worktree를 지정했다. config를 바꾸지 않았으며 시험·임시 Git fixture에는 해당 환경을 주입하지 않았다.

WSL skip 1은 tests/test_check_aliases.py:228의 Windows 8.3 API 전용 시험이다. 이를 WSL 통과 건수로 세지 않았다. 최초 상세 task 경로 입력을 T-103-contrast-ux-lint.md로 잘못 적어 읽기 실패했으며, 실제 T-103-kt-contrast-ux-lint.md를 찾아 읽었다. 제품 오류가 아니다.

## 독립 직접 반례와 누적 corpus

각 helper는 python -B -X utf8 <helper>.py <detached-root>로 Windows에서 실행하고, WSL에서는 같은 스크립트에 uv Python 3.11을 사용했다. helper 경로는 .git/codex-audit 아래이며 아래 명칭은 모두 reviewer A 소유다.

| helper/범위 | 실제 결과 |
|---|---|
| t103-post17-reviewer-a-probe.py | Windows 264행·WSL 263행. CSS specificity/media/string/comment, alpha·baseline·오류/redaction·symlink·airport, MDX/Unicode/FEFF/async/LS/PS 주석 회귀 출력이 직전 candidate와 모두 동일 |
| t103-post19-margins-a.py | 21개 LF/CRLF/CR fence·문단·ESM 회귀 출력 동일 |
| t103-post18-diff-a.py | 10개 LS/PS/LF/CRLF/CR 및 문자열 가짜 @@ hunk, 실제 추가 P8 mapping 동일 |
| t103-post19-mapping-a.py | 15개 plain/tracked/untracked mapping 동일 |
| t103-post21-boundary-a.py | 44개, failures 0 |
| t103-post22-fence-a.py | 102개 suffix·선행 공백, failures 0 |
| t103-post23-opener-a.py | 120개 opener/closer·indent, failures 0 |
| t103-post24-info-a.py | 84개 backtick info 금지·tilde 허용·3/4자 delimiter·ASCII/LS/PS, failures 0 |
| t103-post25-container-a.py | 42개 depth 감소·빈 행·새 quote·content3/4, failures 0 |
| t103-post26-padding-a.py | 72개 실행. 판정 유효 69개 일치, 일반 CommonMark와 MDX의 indented-code 차이 3개는 아래 제한으로 분리 |
| t103-post26-literal-a.py | 6개 outer fence 안의 추가 > literal 유지, 외부 P8만 검출 |
| t103-post27-cli-a.py | 120개 모두 exit·pattern·source line 기대 일치. 양 OS failures 0 |

새 CLI helper는 20개 padding/nested 조합 × backtick/tilde × LF/CRLF/CR을 실행했다. marker 선택 공백, 한 tab·space+tab, marker 앞 0~3열, 두 tab·콘텐츠 4열, 깊이 2/3, 중간 marker 앞 과도한 들여쓰기를 포함한다. LF/CRLF의 외부 P6/P8은 line 4/5, CR 단독 source는 Git LF 행 계약에 따라 line 1에 보고된다.

A-P1-23 최소 반례를 다시 실행했다.

~~~python
body = '> ~~~tsx\n> quoted\n>    ~~~\n> <div className="outline-none"/>\n> {window.confirm("x")}'
~~~

양 OS 실제 결과는 exit 1, P6 line 4 및 P8 line 5다. 마지막 marker 뒤 공백을 tab 또는 space+tab으로 바꾼 대조도 동일하다. 콘텐츠 4열인 raw 5 spaces 및 두 tab은 내부 P6/P8을 올바르게 가린다. 이전 18개 closing 누락과 9개 tilde opener 오탐은 모두 수정됐다.

### 독립 참조 파서의 차이와 채택하지 않은 finding

Windows의 기존 markdown-it-py 4.2.0과 3,372개 조합을 추가 대조했다(t103-post27-reference-a.py). 기본 CommonMark 설정은 3,220개 일치, 152개 차이였다. 차이는 모두 중첩 인용의 중간 marker 앞 4열 이상을 기존 container의 연속으로 처리하는 참조 파서 동작이다. 공식 marker 정의의 최대 3열 및 fenced body에서 lazy paragraph continuation을 허용하지 않는 규칙과 대조해, 해당 경계를 종료시키는 후보를 결함으로 분류하지 않았다. 같은 경계를 포함한 위 CLI 120개는 규범 기대와 일치한다.

사전 탐색에서 참조 파서의 code 규칙을 껐을 때는 660개 차이가 나왔다. 이 설정은 indented code뿐 아니라 fence의 4열 검사도 바꾸므로 MDX 전체의 신뢰할 만한 oracle로 사용하지 않았다. 차이 수를 제품 실패 수로 집계하지 않는다. 실제 MDX compiler는 실행하지 않았다.

기존 72개 padding helper의 backtick/content4/opening 3개(LF/CRLF/CR)는 일반 CommonMark 기대와 MDX indented-code 미지원 차이에 걸린다. 이는 직전 리뷰에서도 분리한 제한이며 이번 수정 회귀로 세지 않았다. 그 외 69개, 신규 CLI 120개, 기존 실패 원 반례의 결과를 명시적으로 구분한다.

## 누적 A finding disposition

각 ID의 원 심각도를 보존했다. FIXED는 원 반례를 이번 candidate에서 재현한 판정이며 언어 전체의 완전한 파싱 보증이 아니다.

| 원 ID | 심각도 | disposition / 재현 범위 |
|---|---|---|
| A-P1-01 | P1 | FIXED — CSS scope·cascade·specificity·media·comment-gap |
| A-P1-02 | P1 | FIXED — OKLCH percent |
| A-P1-03 | P1 | FIXED — sRGB alpha 합성 |
| A-P1-04 | P1 | FIXED — baseline 앞 추가된 신규 위반 |
| A-P1-05 | P1 | FIXED — 외부 Git root |
| A-P2-06 | P2 | FIXED — MDX 인용/실행 문맥·Unicode·개행 누적 원 반례 |
| A-P2-07 | P2 | FIXED — 옵션 모양 base |
| A-P2-08 | P2 | FIXED — 인용/탭 파일명 WSL. Windows 금지 파일명은 NOT_RUN |
| A-P2-09 | P2 | FIXED — JSON 수치·중복·비정상 값 |
| A-P2-10 | P2 | FIXED — JSON/Markdown/annotation/summary·argparse 오류 비공개 |
| A-P2-11 | P2 | FIXED — 읽기 surface-muted 추가 쌍 |
| A-P3-12 | P3 | FIXED — geo 8쌍·airport 현재 1.320934와 과거 1.15 구분 |
| A-P1-13 | P1 | FIXED — diff +++ 실제 source |
| A-P2-14 | P2 | FIXED — self-symlink root 입력 오류 |
| A-P2-15 | P2 | FIXED — 깊은 JSON 오류 |
| A-P1-16 | P1 | FIXED — CR/LS/PS·가짜 hunk의 Git 추가 행 보존 |
| A-P2-19 | P2 | FIXED — plain fence 과도한 들여쓰기 |
| A-P1-20 | P1 | FIXED — backtick info-string의 backtick 금지 |
| A-P1-21 | P1 | FIXED — blockquote 깊이 감소·빈 행·컨테이너 종료 |
| A-P2-22 | P2 | FIXED — marker 뒤 콘텐츠 4열 closing |
| A-P1-23 | P1 | FIXED — optional padding·tab-stop과 콘텐츠 0~3열 분리 |

## 원격 관찰과 NOT_RUN

- gh run list --commit 009ec5dcf70e55b6c736ccaeabbfeb71a08836f6 --json databaseId,headSha,status,conclusion,url --limit 5: [CI 34196371150](https://github.com/digitie/kor-travel-common/actions/runs/34196371150)의 exact head, completed/success를 직접 확인했다. 개별 job 원문 로그 감사는 NOT_RUN. CI dispatch는 하지 않았다.
- Windows Python 3.11: NOT_RUN(실행 파일 부재). Windows 3.14 성공을 3.11 성공으로 바꾸어 표시하지 않는다.
- 실제 MDX compiler/browser, 소비자 build·type/e2e·소비자 manifest 검사, npm/PyPI registry 설치/게시: NOT_RUN(허용 범위 밖 또는 런타임 부재).
- 외부 consumer의 gate·릴리스 가능 판정은 하지 않았다. CommonMark/MDX 전체 문법 지원을 보증하는 결과가 아니다.

## 최종 판정

PASS. 이번 immutable 제품 후보에서 수정이 필요한 신규 P0/P1/P2/P3 finding을 확인하지 못했다. 제품 종료 SHA/tree/clean을 먼저 고정한 뒤 이 원본 하나만 report-only commit하고, commit SHA와 원본 blob SHA256은 완료 메시지로 전달한다.
