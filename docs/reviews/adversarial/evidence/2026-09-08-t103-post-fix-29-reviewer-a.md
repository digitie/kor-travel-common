# T-103 수정 후 독립 적대적 리뷰 29 — Reviewer A

- 실행 ID: T103-POST29-A-20260908-162853-KST
- 판정: **NO-GO**. 신규 A-P1-25(P1), 잔여 A-P2-24(P2, PARTIAL/OPEN). P0/P3 0건.
- 제품 candidate: 9afea549dd81cb23d3297f83d89df4b519734382
- 제품 tree: 03cb65ba437848f279f542452705c235f19daaa8
- delta base: 71a6f99de297e809c165f005d4d6b1753468d157
- 공통 manifest: commit a100194의 docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-29-manifest.md, git show로 읽음. 제품과 별도 commit이다.
- 격리: F:/dev/kor-travel-common-wt/review-t103-post29-a detached worktree.
- 시작: 2026-09-08 16:28:53.630 KST. 제품 검증 종료: 2026-09-08 16:36:27.626 KST.
- 시작/종료 HEAD·tree는 위 candidate와 일치, git status --porcelain=v1 출력 없음.
- 다른 reviewer 원본·결과를 읽거나 요청하지 않았다. 제품·manifest·소비자·공유 branch·기존 evidence·git config를 수정하지 않았다. 이 원본 한 파일만 별도 commit한다.

## 전달 요청 원문

> post-29 독립 적대 리뷰를 시작해 주세요. immutable code candidate는 commit 9afea549dd81cb23d3297f83d89df4b519734382, tree 03cb65ba437848f279f542452705c235f19daaa8 입니다. manifest는 docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-29-manifest.md (manifest commit a100194)입니다. 별도 detached clean worktree에서 candidate SHA/tree를 checkout하고, 다른 reviewer 결과·raw를 열람하지 마세요. A 범위는 invalid backtick info의 CommonMark inline fallback, 정상 closed 3/4자 inline, line-start block fence, plain/blockquote/nested·P6/P8·LF/CRLF/CR와 양 OS입니다. 코드·manifest·소비자·기존 evidence는 수정하지 말고 자신의 단일 raw report만 커밋하세요. PASS/NO-GO와 finding ID/심각도/재현/영향/최소 수정/disposition, 시작·종료 SHA/tree·clean·명령/결과·SHA-256을 남겨 주세요. raw commit과 SHA-256을 회신하세요.

## 범위와 근거

전체 delta 5파일 중 tools/ux_lint.py·tests/test_ux_lint.py의 제품 diff를 전부 읽었다. 나머지는 직전 manifest와 두 reviewer 원본 보존이며 상대 원본 본문은 읽지 않았다. T-103의 인용 제외/실행식 검출/추가 행 gate 수용 기준을 재확인했다. 변경 없는 AGENTS·문서 라우터·resume·규칙/코드의 이전 읽기는 diff 동일성으로 재사용하고, full/focused/static·누적 직접 corpus는 이번 candidate에서 다시 실행했다.

기준은 CommonMark 0.31.2(2024-01-28)의 [block 우선순위](https://spec.commonmark.org/0.31.2/#precedence), [fence](https://spec.commonmark.org/0.31.2/#fenced-code-blocks), [blockquote](https://spec.commonmark.org/0.31.2/#block-quotes), [code span](https://spec.commonmark.org/0.31.2/#code-spans)이다. 2026-09-08 직접 확인한 공식 규범을 재사용했다. Windows에 이미 설치된 markdown-it-py 4.2.0 기본 CommonMark로 신규 60개 입력의 block/inline 구분도 대조했다.

## A-P1-25 — 다른 인용 깊이의 block fence를 inline 닫힘으로 오인해 실행식을 누락

- 심각도: P1. disposition: **OPEN / FIX_REQUIRED**. 이번 candidate가 도입한 false PASS.
- 위치: tools/ux_lint.py:463, 657. _markdown_is_fence_start가 원래 opener의 container로만 닫힘 후보를 해석한다.
- 최소 재현:

~~~python
body = '> ```bad`info\n{window.confirm("outside")}\n```'
~~~

임시 root의 case.mdx에 UTF-8 bytes로 저장하고 python -B -X utf8 tools/ux_lint.py --root <임시-root> --fail-new --json을 실행한다. WSL은 uv run --no-project --python 3.11을 앞에 쓴다.

양 OS 실제: exit 0, status PASS, findings [], fail_count 0. 기대: P8 line 2(LF), exit 1. 닫힘처럼 보이는 마지막 줄은 다른 container의 새 block fence이며 인용 안 code span으로 연결해서는 안 된다. 독립 CommonMark parser에 code_inline은 없었다.

quote→plain, nested→quote, plain→quote, quote→nested의 네 전환 × 3/4자 delimiter × LF/CRLF/CR = 24개에서 모두 동일한 누락을 재현했다. 이는 단순히 같은 container의 정상 span 수정이 아니라 block 경계를 넘어 실행식을 가리는 회귀다.

추가 --base 대조는 다음 입력으로 실행했다.

~~~python
body = '> ```bad`info\n<div className="outline-none"/>\n{window.confirm("outside")}\n```'
~~~

별도 임시 Git repo의 일반 문서를 commit한 뒤 위 내용으로 바꾸고 --base <fixture-sha> --json을 실행했다. base 71a6f99 Windows는 exit 1, P6 line 2/P8 line 3, fail_count 2였다. candidate는 양 OS 모두 exit 0, findings [], fail_count 0으로 실제 추가 위반을 놓쳤다.

영향: 새 실행 코드가 UX diff gate를 통과한다. 최소 수정은 닫힘 위치의 실제 block/container를 독립적으로 판정하는 것이다. 원 opener의 깊이가 달라도 새 plain/blockquote/nested block fence와 그 전에 끝나는 문단을 구분해야 한다. 네 전환 및 P6/P8, 3/4자·세 개행·--base를 고정한다.

## A-P2-24 — 정상 inline 오탐은 일부 수정됐지만 content4 닫힘은 잔여

- 원 심각도: P2 유지. disposition: **PARTIAL / OPEN / FIX_REQUIRED**.
- 직전 원 반례 36개와 63개 양성/음성 대조는 이번에 수정됐다. 기존 정상 same-line 및 same-paragraph 99개는 기대 일치다.
- 잔여 위치: tools/ux_lint.py:466. candidate_info의 콘텐츠 들여쓰기 값을 버려 4열 이상의 위치를 block fence로 분류한다.
- 확장 최소 재현:

~~~python
body = '> ```bad`info\n> {window.confirm("quoted")}\n>     ```'
~~~

마지막 > 뒤 raw 5 spaces는 선택 공백 1열을 제외한 콘텐츠 4열이므로 fence opener가 아니다. 앞 문단의 정상 inline span 닫힘으로 해석된다. 독립 CommonMark parser도 code_inline을 반환했다. 기대 exit 0/findings [], candidate 양 OS 실제 exit 1/P8 line 2(LF). base 71a6f99도 같은 오탐이 있었으므로 이 부분은 새 P1 회귀와 구별되는 잔여다.

raw 5 spaces·두 tab·space+두 tab, quote/nested, 3/4자 delimiter, LF/CRLF/CR = 36개가 모두 오탐했다. --base 대조도 candidate 양 OS exit 1, fail_count 1, P8 added=true/fail=true였다. 정상 same-line 수정 대조는 양 OS exit 0이었다.

영향: 정상 인용 예제를 추가하는 변경이 gate에서 차단된다. 최소 수정은 _markdown_is_fence_start가 마지막 marker 뒤 콘텐츠 들여쓰기 0~3열을 확인하도록 하는 것이다. 정상 span 유지와 실제 block 경계 구분을 함께 검증하고 A-P1-25 수정 과정에서도 content4를 block으로 승격하지 않아야 한다.

## 명령과 실제 검증

모든 제품 검증은 detached candidate에서 수행했다. 본인 helper/log는 기본 checkout .git/codex-audit, fixture는 임시 디렉터리만 사용했다. Windows 전체 시험은 독립 TEMP/TMP, WSL 전체는 독립 TMPDIR을 사용했다. WSL 정적 Git gate만 프로세스 GIT_DIR/GIT_WORK_TREE로 이 worktree를 지정했다. source config를 바꾸거나 fixture에 해당 환경을 주입하지 않았다.

| 명령 | Windows Python 3.14.3 | WSL Python 3.11.15 |
|---|---|---|
| python -B -X utf8 -m unittest discover -s tests -p 'test_*.py' -v | 302 통과, skip 0, 206.593초 | 아래 명령: 302 수집, 301 통과, skip 1, 63.635초 |
| python -B -X utf8 -m unittest tests.test_kt_contrast tests.test_ux_lint | 64 통과, 69.646초 | 64 통과, 24.932초 |
| tools/validate_document_links.py | 478문서·2471대상, 오류 0 | 동일 |
| tools/validate_plan.py | 106 task, 오류 0 | 동일 |
| tools/check_spdx.py | 56파일, 오류 0 | 동일 |
| tools/scan_secrets.py --all | 610파일, 발견 0 | 동일 |
| tools/check_prod_redaction.py --all | 610파일, 발견 0 | 동일 |
| tools/check_versions.py --self-check | 자체 검사 통과, 소비자 NOT_RUN | 동일 |
| tools/check_aliases.py packages/tokens/aliases | CSS 1개, 오류 0 | 동일 |
| tools/kt_contrast.py packages/tokens/tokens.css --json | light 27쌍 PASS | 동일 |
| tools/ux_lint.py --root tests/fixtures/ux --json | 의도된 finding 12개, report fail_count 0 | 동일 |
| git diff --check 71a6f99 9afea54 | 출력 없음 | 출력 없음 |

표의 tools 명령에는 python -B -X utf8을 사용했다. WSL 전체 명령은 uv run --no-project --python 3.11 --with jsonschema python -B -X utf8 -m unittest discover -s tests다. 다른 Python 명령은 uv run --no-project --python 3.11로 실행했다. manifest의 focused 63개를 재사용하지 않고 직접 실행한 실제 64개를 기록한다. WSL skip 1은 Windows 8.3 API 전용이며 통과로 세지 않았다.

## 직접 corpus와 원 finding별 disposition

각 helper는 python -B -X utf8 <.git/codex-audit/helper.py> <detached-root>로 실행했으며 WSL은 같은 스크립트를 uv Python 3.11로 실행했다.

| helper | 양 OS 결과 |
|---|---|
| t103-post17-reviewer-a-probe.py | Windows 264행·WSL 263행. CSS cascade/media/수학, JSON·baseline·redaction·symlink·airport, MDX/Unicode/FEFF/async/주석 누적 원 출력이 직전과 동일 |
| t103-post19-margins-a.py | 21개 Markdown/ESM 줄 경계 결과 동일 |
| t103-post18-diff-a.py | 10개 가짜 hunk·Unicode/CR 추가 행 결과 동일 |
| t103-post19-mapping-a.py | 15개 plain/tracked/untracked source mapping 동일 |
| t103-post21-boundary-a.py | 44개, failures 0 |
| t103-post22-fence-a.py | 102개, failures 0 |
| t103-post23-opener-a.py | 120개, failures 0 |
| t103-post24-info-a.py | 84개, failures 0 |
| t103-post25-container-a.py | 42개, failures 0 |
| t103-post26-padding-a.py | 72개 실행, 유효 69개 일치·기존 oracle 한계 3개는 아래 분리 |
| t103-post26-literal-a.py | 6개, 외부 P8만 검출 |
| t103-post27-cli-a.py | 120개 marker/tab/nested, failures 0 |
| t103-post28-inline-a.py | 99개, failures 0. 직전 36개 정상 span 오탐 수정 |
| t103-post28-base-a.py | 직전 정상 same-line --base 반례 exit 0, findings 0으로 수정 |
| t103-post29-boundary-a.py | 60개 중 A-P1-25 누락 24개·A-P2-24 잔여 오탐 36개 |
| t103-post29-base-a.py | 새 container 누락/잔여 content4 오탐/수정된 same-line의 --base 구분 재현 |

새 helper SHA256은 t103-post29-boundary-a.py = E1CBFE536BC0D33232189BFAD0385DCAC9C6EF9A154DF0F3815ED438E13980C6, t103-post29-base-a.py = CB7948F14556B122C2FF88DD7FA568997444012C621AEE841271F1159A270614다. Windows 기존 base worktree를 읽어 원인 전후를 비교했으며 제품 파일을 수정하지 않았다.

| 원 ID | 원 심각도 | disposition |
|---|---|---|
| A-P1-01·02·03·04·05 | 각 P1 | FIXED — CSS scope/cascade, OKLCH percent, alpha, baseline 앞 추가, 외부 root |
| A-P2-06·07·08·09·10·11 | 각 P2 | FIXED — 기존 MDX 원 corpus, 옵션 base, 파일명, JSON, 비공개 출력, 읽기 표면 |
| A-P3-12 | P3 | FIXED — geo·airport 현재/역사 수치 구분 |
| A-P1-13 | P1 | FIXED — diff +++ source |
| A-P2-14·15 | 각 P2 | FIXED — self-symlink root·깊은 JSON |
| A-P1-16 | P1 | FIXED — Unicode/CR·가짜 hunk의 추가 행 |
| A-P2-19 | P2 | FIXED — plain fence indentation |
| A-P1-20·21 | 각 P1 | FIXED — invalid info 원 반례·blockquote 종료 |
| A-P2-22 | P2 | FIXED — content4 closing 원 반례 |
| A-P1-23 | P1 | FIXED — 선택 공백/tab-stop 원 반례 |
| A-P2-24 | P2 | PARTIAL/OPEN — 원 36개 수정, content4 정상 span 36개 확장 경계 잔여 |
| A-P1-25 | P1 | OPEN — 다른 container block 경계를 넘는 신규 누락 |

FIXED는 해당 원 반례의 이번 실행 결과이며 새 fallback의 결함을 덮거나 문법 전체를 보증하지 않는다.

## CI·재사용·NOT_RUN

- gh run list --commit 9afea549dd81cb23d3297f83d89df4b519734382 --json databaseId,headSha,status,conclusion,url --limit 5로 [CI 34199104378](https://github.com/digitie/kor-travel-common/actions/runs/34199104378)의 exact head/completed/success를 확인했다. 개별 job 원문 로그 감사·dispatch는 NOT_RUN.
- Windows Python 3.11: NOT_RUN(실행 파일 부재). Windows 3.14를 대신 통과로 표시하지 않는다.
- Windows에서 허용되지 않는 탭 파일명은 NOT_RUN이며 해당 corpus는 WSL에서 실행했다. WSL Windows 8.3 시험 skip은 별도 보존한다.
- padding의 content4 backtick opening 3개는 일반 CommonMark와 MDX indented-code 미지원에 따른 기존 oracle 한계로 분리했다. 실제 MDX compiler/browser는 NOT_RUN. 이번 두 finding은 공식 block/inline 규칙 및 기본 CommonMark parser 대조로 확인했다.
- 변경 없는 정본·코드의 읽기는 이전 검토 및 이번 diff 동일성으로 재사용했다. 이전 3,372개 참조 조합 전체는 재실행하지 않았고, 변경된 fallback에 신규 60개·수정 대조 99개·--base 입력을 실행했다.
- 소비자 build/type/e2e·소비자 manifest 검증, npm/PyPI registry 설치/게시: NOT_RUN(허용 범위 밖).

## 최종 판정

**NO-GO. A-P1-25와 A-P2-24를 수정 후 새 불변 후보에서 두 독립 재검토가 필요하다.** 전체 시험/CI 성공은 직접 재현한 누락과 오탐을 해결하지 않는다. 제품을 고치지 않고 이 원본 한 파일만 immutable report-only commit으로 확정하며 commit SHA와 원본 blob SHA256을 완료 메시지로 전달한다.
