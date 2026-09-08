# T-103 수정 후 독립 적대적 리뷰 30 — Reviewer A

- 실행 ID: T103-POST30-A-20260908-164640-KST
- 판정: **NO-GO**. 새로 발견한 A-P1-26(P1) 1건. 신규 P0/P2/P3 0건.
- 제품 candidate: 620e477bf841f881e6090cccefcbad81cfffe6e7
- 제품 tree: ee2964452454b255a47a27aea1edb1a0c5ede2db
- delta base: 9afea549dd81cb23d3297f83d89df4b519734382
- 공통 manifest: commit 43d5c3d의 docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-30-manifest.md를 git show로 읽었다. 제품과 별도 commit 문서다.
- 격리: F:/dev/kor-travel-common-wt/review-t103-post30-a detached worktree.
- 시작: 2026-09-08 16:46:40.371 KST. 제품 검증 종료: 2026-09-08 16:53:22.465 KST.
- 시작/종료 HEAD·tree는 위 candidate와 일치. 양 시점 git status --porcelain=v1 출력 없음.
- 다른 reviewer의 결과/raw는 읽거나 요청하지 않았다. 제품·manifest·소비자·공유 branch·기존 evidence·git config를 수정하지 않았다. 종료 후 이 보고서 한 파일만 report-only commit한다.

## 전달 요청 원문

> post-30 독립 적대 리뷰를 시작해 주세요. immutable candidate commit 620e477bf841f881e6090cccefcbad81cfffe6e7, tree ee2964452454b255a47a27aea1edb1a0c5ede2db. manifest 2026-09-08-t103-post-fix-30-manifest.md (commit 43d5c3d). 상대 reviewer raw를 읽지 말고 detached clean worktree에서 시작/종료 SHA/tree·clean을 기록하세요. A 범위: CommonMark container 전환(plain/blockquote/nested), marker 뒤 0~3열/4열 및 tabs, 3·4자 inline span, P6/P8, LF/CRLF/CR, --base 양 OS. 후보/manifest/소비자/evidence는 수정하지 말고 단일 report-only raw commit을 만들어 verdict·findings·SHA256을 회신하세요.

## 검토 범위와 근거

전체 delta 5파일 중 tools/ux_lint.py·tests/test_ux_lint.py 제품 diff를 전부 읽었다. 나머지 파일은 직전 manifest와 A/B 원본 보존이다. 상대 원본 본문은 읽지 않았다. T-103의 인용 제외·실행식 검출·추가 행 gate 계약을 직접 재확인했다. 변경 없는 AGENTS/문서 라우터/resume/정본·코드 읽기는 이전 검토와 이번 동일성 대조를 재사용했다. 실제 full/focused/static·직접 반례는 candidate에서 다시 실행했다.

공식 기준은 CommonMark 0.31.2(2024-01-28)의 [block 우선순위](https://spec.commonmark.org/0.31.2/#precedence), [fence](https://spec.commonmark.org/0.31.2/#fenced-code-blocks), [blockquote](https://spec.commonmark.org/0.31.2/#block-quotes), [code span](https://spec.commonmark.org/0.31.2/#code-spans)이다. 2026-09-08 직접 확인한 규범을 재사용했고 Windows 기존 markdown-it-py 4.2.0 기본 CommonMark로 신규 입력의 block/inline 분리를 대조했다. 참조 파서 설치나 registry 호출은 하지 않았다.

## A-P1-26 — 중간에 시작한 유효 fence를 넘어서 inline 닫힘을 찾으며 실행식을 누락

- 심각도: P1. disposition: **OPEN / FIX_REQUIRED**.
- 위치: tools/ux_lint.py:433의 _find_inline_span_end 및 :667–668의 invalid info fallback.
- 원인: 같은 길이의 backtick 닫힘을 먼저 고르고 그 위치만 실제 block opener인지 검사한다. opener와 선택된 닫힘 사이에 다른 종류/길이의 유효 fence가 시작해도 탐색을 멈추지 않는다.
- 이번에 처음 발견했지만 base 9afea54에서도 동일하게 존재했다. 이번 delta가 도입한 회귀로 표시하지 않는다. 직전 A-P1-25의 직접 container 전환 반례는 이번에 수정됐다.

### 최소 재현

임시 root의 case.mdx에 다음 Python 문자열을 UTF-8 bytes로 저장한다.

~~~python
body = '```bad`info\n{window.confirm("outside")}\n~~~js\ntext ```\n~~~'
~~~

명령: python -B -X utf8 tools/ux_lint.py --root <임시-root> --fail-new --json. WSL은 uv run --no-project --python 3.11을 앞에 사용했다.

양 OS 실제: exit 0, status PASS, findings [], fail_count 0. 기대: P8 line 2(LF), exit 1.

독립 CommonMark parser의 결과는 앞 두 줄 inline 문단 map [0,2], 뒤 세 줄 fence map [2,5]다. fence 안의 text 뒤 backtick은 문자 그대로의 예제이며 앞 문단의 code span을 닫을 수 없다. 후보는 이 backtick까지 한 span으로 가려 앞 문단의 실행식도 삭제한다.

tilde fence를 opener보다 한 자 긴 backtick fence로 바꿔도 같은 오류다. 예를 들어 원 delimiter가 3자면 중간 fence는 4자다. 원 delimiter 3/4자 × 중간 tilde/더 긴 backtick × plain/quote/nested × LF/CRLF/CR = 36개 모두 누락됐다.

정상 같은 문단 inline span과, 선택된 matching backtick 자체가 block 경계에 있는 대조 36개는 기대와 일치했다. 본인 t103-post30-intervening-a.py 총 72개 중 누락 36개/정상 36개다. 작성자 회귀시험 결과와 별도로 이 직접 반례를 판정했다.

### --base와 영향

본인 t103-post30-base-a.py는 임시 Git repo에서 일반 문서를 commit한 뒤 아래 새 입력으로 바꾸고 --base <fixture-sha> --json을 실행했다.

~~~python
body = '```bad`info\n<div className="outline-none"/>\n{window.confirm("outside")}\n~~~js\ntext ```\n~~~'
~~~

candidate 양 OS 실제 exit 0, findings [], fail_count 0. 기대는 신규 P6 line 2/P8 line 3, exit 1이다. base 9afea54 Windows에서도 같은 누락이 재현됐다.

실행 코드에 새 금지 패턴을 추가해도 UX diff gate를 통과할 수 있다. 최소 수정은 유효 inline span의 범위를 결정할 때 **중간에 나타난 실제 block 경계**에서 탐색을 종료하는 것이다. 닫힘 후보 한 위치만 검사해서는 부족하다. 중간 tilde·더 긴 backtick, plain/quote/nested, 3/4자와 CR/LF/CRLF, P6/P8 및 --base를 함께 고정하고 정상 closed span을 보존해야 한다.

## 이전 수정 직접 재확인

| 이전 반례 | 이번 candidate 양 OS 실제 | disposition |
|---|---|---|
| 정상 same-line/same-paragraph 99개 | failures 0 | A-P2-24의 최초 36개 오탐 수정 유지 |
| 다른 container의 matching block fence 앞 P8 24개 | 기대 P8/exit 1 | A-P1-25 FIXED |
| content4 정상 inline closing 36개 | 기대 findings 0/exit 0 | A-P2-24 잔여 FIXED |
| --base 다른 container 앞 신규 P6/P8 | exit 1, fail_count 2 | 수정 확인 |
| --base content4/정상 same-line 인용 | exit 0, findings 0 | 수정 확인 |

직전 60개 경계 helper와 --base helper를 새 candidate에서 다시 실행했다. 기존 원 반례의 수정과 새 중간 block 탐색 누락은 별개로 기록한다.

## 명령과 실제 검증

모든 제품 검증은 detached candidate에서 실행했다. helper/log는 기본 checkout .git/codex-audit의 본인 파일, fixture는 별도 임시 디렉터리를 사용했다. Windows full 시험은 독립 TEMP/TMP, WSL full 시험은 독립 TMPDIR을 사용했다. WSL의 Git 정적 gate에만 프로세스 GIT_DIR/GIT_WORK_TREE를 지정했고 source config를 바꾸거나 임시 Git 시험에 주입하지 않았다.

| 명령 | Windows Python 3.14.3 | WSL Python 3.11.15 |
|---|---|---|
| python -B -X utf8 -m unittest discover -s tests -p 'test_*.py' -v | 303 통과, skip 0, 195.994초 | 아래 명령: 303 수집, 302 통과, skip 1, 63.156초 |
| python -B -X utf8 -m unittest tests.test_kt_contrast tests.test_ux_lint | 65 통과, 70.833초 | 65 통과, 27.684초 |
| tools/validate_document_links.py | 481문서·2478대상, 오류 0 | 동일 |
| tools/validate_plan.py | 106 task, 오류 0 | 동일 |
| tools/check_spdx.py | 56파일, 오류 0 | 동일 |
| tools/scan_secrets.py --all | 613파일, 발견 0 | 동일 |
| tools/check_prod_redaction.py --all | 613파일, 발견 0 | 동일 |
| tools/check_versions.py --self-check | 자체 검사 통과, 소비자 NOT_RUN | 동일 |
| tools/check_aliases.py packages/tokens/aliases | CSS 1개, 오류 0 | 동일 |
| tools/kt_contrast.py packages/tokens/tokens.css --json | light 27쌍 PASS | 동일 |
| tools/ux_lint.py --root tests/fixtures/ux --json | 의도된 report finding 12개, fail_count 0 | 동일 |
| git diff --check 9afea54 620e477 | 출력 없음 | 출력 없음 |

표의 tools 명령에는 python -B -X utf8을 사용했다. WSL 전체 명령은 uv run --no-project --python 3.11 --with jsonschema python -B -X utf8 -m unittest discover -s tests다. 다른 Python 명령도 uv Python 3.11을 사용했다. manifest의 focused 64개를 재사용하지 않고 실제 65개를 기록한다. WSL skip 1은 Windows 8.3 API 전용 시험이며 통과로 세지 않았다.

## 누적 corpus와 disposition

각 helper는 python -B -X utf8 <.git/codex-audit/helper.py> <detached-root>로 Windows에서 실행하고, WSL에서는 동일 스크립트를 uv Python 3.11로 실행했다.

| helper | 양 OS 관찰 |
|---|---|
| t103-post17-reviewer-a-probe.py | Windows 264행·WSL 263행. CSS/수학·baseline/JSON/redaction/symlink/airport 및 MDX/Unicode/FEFF/async/주석 원 corpus 출력 동일 |
| t103-post19-margins-a.py | 21개 Markdown/ESM 줄 경계 동일 |
| t103-post18-diff-a.py | 10개 Unicode/CR·가짜 hunk 추가 행 동일 |
| t103-post19-mapping-a.py | 15개 plain/tracked/untracked mapping 동일 |
| t103-post21-boundary-a.py | 44개, failures 0 |
| t103-post22-fence-a.py | 102개, failures 0 |
| t103-post23-opener-a.py | 120개, failures 0 |
| t103-post24-info-a.py | 84개, failures 0 |
| t103-post25-container-a.py | 42개, failures 0 |
| t103-post26-padding-a.py | 72개 실행, 기존 판정 유효 69개 일치·oracle 한계 3개 분리 |
| t103-post26-literal-a.py | 6개, 외부 P8만 검출 |
| t103-post27-cli-a.py | 120개, failures 0 |
| t103-post28-inline-a.py | 99개, failures 0 |
| t103-post28-base-a.py | 정상 same-line --base exit 0 |
| t103-post29-boundary-a.py | 60개, failures 0 |
| t103-post29-base-a.py | 실제 위반과 정상 인용의 --base 판정 기대 일치 |
| t103-post30-intervening-a.py | 신규 72개 중 중간 block을 건너뛴 36개 false PASS |
| t103-post30-base-a.py | 신규 누락 및 이전 두 수정의 --base 대조 |

새 helper SHA256: t103-post30-intervening-a.py = 7D7E1A53E78567EC9174D53DC5216F74A4154AEDBEA40ED52CF041235E6D40F9, t103-post30-base-a.py = E861EA2187D770B89EC1CE3567030663873FA5B0F6BC04A594160284A475E1B6.

| 원 ID | 원 심각도 | disposition |
|---|---|---|
| A-P1-01·02·03·04·05 | 각 P1 | FIXED — CSS scope/cascade, OKLCH percent, alpha, baseline 추가, 외부 root |
| A-P2-06·07·08·09·10·11 | 각 P2 | FIXED — 기존 MDX 원 corpus, 옵션 base, 파일명, JSON, 비공개 출력, 읽기 표면 |
| A-P3-12 | P3 | FIXED — geo·airport 현재/역사 수치 구분 |
| A-P1-13 | P1 | FIXED — diff +++ source |
| A-P2-14·15 | 각 P2 | FIXED — self-symlink root·깊은 JSON |
| A-P1-16 | P1 | FIXED — Unicode/CR·가짜 hunk 추가 행 |
| A-P2-19 | P2 | FIXED — plain fence 들여쓰기 |
| A-P1-20·21 | 각 P1 | FIXED — invalid info 원 반례·container 종료 |
| A-P2-22 | P2 | FIXED — content4 closing 원 반례 |
| A-P1-23 | P1 | FIXED — marker 선택 공백/tab-stop |
| A-P2-24 | P2 | FIXED — 정상 span 최초/잔여 반례 |
| A-P1-25 | P1 | FIXED — 다른 container block 전환 |
| A-P1-26 | P1 | OPEN — matching delimiter 전에 시작한 중간 fence 누락 |

FIXED는 원 반례의 실행 결과이며 언어 전체의 파싱 보증이 아니다. 원 finding 23개 수정 결과와 새 finding을 분리한다.

## CI·재사용·NOT_RUN

- gh run list --commit 620e477bf841f881e6090cccefcbad81cfffe6e7 --json databaseId,headSha,status,conclusion,url --limit 5로 [CI 34200652371](https://github.com/digitie/kor-travel-common/actions/runs/34200652371)의 exact head/completed/success를 확인했다. 개별 job 원문 로그 감사·workflow dispatch는 NOT_RUN.
- Windows Python 3.11: NOT_RUN(실행 파일 부재). Windows 3.14 성공을 대신 표시하지 않는다.
- Windows에서 금지된 탭 파일명은 NOT_RUN, 해당 corpus는 WSL에서 실행했다. WSL Windows 8.3 API 시험은 skip으로 보존했다.
- 기존 padding helper의 content4 backtick opening 3개는 일반 CommonMark와 MDX indented-code 미지원의 차이 때문에 직전과 동일한 oracle 한계로 분리했다. 실제 MDX compiler/browser는 NOT_RUN. 이번 중간 fence finding은 공식 block 우선순위와 기본 CommonMark parser로 확인했다.
- 변경 없는 정본/코드 읽기는 이전 검토와 diff 동일성으로 재사용했다. 이전 3,372개 참조 조합 전체는 재실행하지 않았다. 변경한 fallback 주변에 신규 72개·이전 99/60개·--base 반례를 직접 실행했다.
- 소비자 build/type/e2e·소비자 manifest 검사와 npm/PyPI registry 설치/게시: NOT_RUN(허용 범위 밖).

## 최종 판정

**NO-GO — A-P1-26 FIX_REQUIRED.** 전체 시험과 CI 성공만으로 중간 block 경계를 건너뛰는 실제 실행식 누락을 해결할 수 없다. 제품을 수정하지 않고 이 원본 한 파일만 immutable report-only commit으로 확정한 뒤 commit SHA와 원본 blob SHA256을 완료 메시지로 전달한다.
