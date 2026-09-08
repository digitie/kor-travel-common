# T-103 post-fix-08 독립 적대적 리뷰 A 원본

- 실행 ID: `reviewer-a-t103-post-fix-08-20260908-110727`.
- 시작: 2026-09-08 11:07:27.799 KST. 제품 검토 종료: 2026-09-08 11:10:40.444 KST.
- 시작·종료 HEAD: `559a9e8a0e49feca2dab9d59df29039bbb0acfd3`; tree: `322fb840ac458c8fc7a0c69f90b0d1bdb77495d6`.
- 시작·종료 `git status --porcelain=v1`: 빈 출력. 별도 detached worktree `review-t103-post8-a`에서 후보를 읽고 시험했다. 보고서 한 파일만 추가해 별도 immutable commit한다.
- manifest: `5c91168b9a594039bbfcd0dfae0cdf89519ae434`의 `docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-08-manifest.md`를 `git show`로 읽었다. 직전 코드 기준선은 `63fe3d5c969b28bab4d528d3e24a054e3a8e30e6`이다.
- 요청 범위: selector/cascade/media, MDX 실행 문맥·주석·인용·fence, baseline/JSON/argparse/redaction/diff/symlink/airport의 누적 반례와 full/focused/static gates를 Windows Python 3.14·WSL Python 3.11에서 독립 검증한다. Windows 3.11은 NOT_RUN이다.
- 상대 결과·과거 보고서를 열지 않았다. 자신의 누적 실행 helper만 재사용하여 실제 CLI를 다시 실행했다. 후보 코드·manifest·소비자 파일·소스 `.git/config`를 수정하지 않았으며 registry·workflow dispatch도 호출하지 않았다.

## 판정

**NO-GO.** 누적 15개 ID 중 13개 FIXED, `A-P1-01`(P1)과 `A-P2-06`(P2)은 동일 원인의 잔여 반례로 OPEN이다. 새 ID는 없다. 현재 열린 P0 0건/P1 1건/P2 1건/P3 0건이다. 직전 정확한 반례는 수정됐지만 아래 경계가 false PASS와 false positive를 만든다.

## A-P1-01 / P1 / OPEN — 주석으로 분리한 compound selector의 미달이 계속 누락된다

- 위치: `tools/kt_contrast.py:96` `_strip_css_comments`, 166행 `_selector_has_compound_space`, 329행 이후 `global_scopes` 조건.
- 임시 `override.css`: `.dark/**/:not(.light){--kt-brand:#fff;--kt-brand-foreground:#fff}`.
- 실행: `python -B -X utf8 tools/kt_contrast.py packages/tokens/tokens.css <임시경로>/override.css --dark --fail-new --json`.
- 실제: 양 OS exit 0, `status=PASS`, 27쌍 중 미달 0건. 주석을 뺀 `.dark:not(.light)`는 같은 명령에서 일반 exit 2이다.
- 브라우저 대조: Windows Playwright Chromium에서 `<!doctype html><html class="dark">`와 위 선언을 적용하고 body의 전경/배경을 두 변수에 연결했다. computed color/background 모두 `rgb(255, 255, 255)`, 실제 대비 1:1이다.
- 원인·영향: 주석을 공백으로 바꿔 같은 요소의 compound selector를 descendant로 오인한다. 이번 수정은 root 존재 또는 알려진 scope가 2개 이상인 경우만 닫으므로, `.dark` 하나와 다른 유효한 조건 조합에서는 동일 누락이 남는다. 실제 대비 미달을 신규 gate가 정상으로 통과시킨다.
- 수정·수용: 주석과 실제 문법 공백을 구분해 selector 의미를 보존하고 지원 밖 문법은 일관되게 닫는다. 위 사례는 미달 exit 1 또는 일반 입력 오류 exit 2여야 한다. 특정 selector 문자열·개수의 특례 추가로 같은 원인을 덮지 않는다.
- 정상 결과: 직전 `.dark/**/.dark`와 그 무주석형은 둘 다 exit 2이다. `:root/**/.dark`, root descendant, 빈 목록, 지원 밖 목록 및 대소문자·인용값 경계도 이전 정상 결과를 유지했다.

## A-P2-06 / P2 / OPEN — Markdown 블록 경계와 파일 첫 span의 실행 문맥 판정이 다르다

- 위치: `tools/ux_lint.py:73` `_find_backtick_run_end`, 196행 `_has_open_inline_span`, 378행 이후 template/span 분기.
- 각 사례를 별도 임시 `.mdx`로 저장하고 `python -B -X utf8 tools/ux_lint.py <임시경로>/fixture.mdx --fail-new --json`을 실행했다.
- 사례 A: 서로 다른 Markdown 문단의 미종결 backtick이 하나의 span으로 연결되어 사이의 JSX까지 가린다.

```mdx
Example ` unmatched

export const X = () => <div className="outline-none" />;

Another ` unmatched
```

- A 실제: 양 OS exit 0, `status=PASS`, `fail_count=0`, findings 0. 기대: 가운데 실행 JSX의 P6 1건·exit 1. 뒤 문단에 backtick이 없으면 직전 수정대로 검출되지만, 다른 문단의 backtick을 추가하면 다시 누락된다.
- 사례 B: 파일 첫 문자부터 시작하는 정상 code span이다.

```mdx
`<div className={`

Another `outline-none`
```

- B 실제: 양 OS exit 1, `status=FAIL`, P6 1건. 기대: 두 내용 모두 Markdown code span이므로 findings 0·exit 0.
- B 원인: `_has_open_inline_span`의 `text.rfind("\n\n", 0, index) + 2`는 앞 빈 줄이 없을 때 1이 되어 첫 문자 backtick을 건너뛴다. 첫 인용 안의 JSX 속성이 열린 실행 문맥으로 남아 다음 정상 인용을 실행 코드로 오인한다.
- 보조 대조: 설치된 `marked` lexer를 Windows Node로 실행했다. A는 3개 paragraph이며 앞·뒤 backtick은 일반 text, 중간 JSX는 HTML token이었다. B는 2개 paragraph이며 각 내용이 codespan으로 분류됐다. 이는 Markdown 블록/인용 대조이며 MDX compiler 실행을 대신하지 않는다.
- 영향·수용: 앞뒤 문서 문구로 실행 금지 패턴을 숨기거나 정상 문서가 gate를 실패시킨다. block 단위 inline 영역을 구분하고 파일 첫 위치를 포함해 열린 span을 추적한다. A는 P6 exit 1, B는 findings 0이어야 하며 JSX/ESM·주석·fence의 정상 결과도 유지해야 한다.
- 정상 결과: 직전 JSX line/block 주석 `}`와 미종결 1자 span 이후 JSX는 모두 P6 1건·exit 1이다. 중첩 object·무들여쓰기 ESM·2자 span·blockquote·일반/computed tag·배열/삼항·escaped interpolation·보간 주석·4자/tilde/suffix fence corpus도 정상 결과를 유지했다.

## 누적 disposition

| 원 ID | 원 심각도 | 판정 | 직접 확인 |
|---|---|---|---|
| A-P1-01 | P1 | OPEN | 위 comment compound false PASS |
| A-P1-02 | P1 | FIXED | OKLCH chroma `25%`와 `0.1` RGB 동일 |
| A-P1-03 | P1 | FIXED | 흰색 20%/검정 source-over와 `#333` 대비 모두 1.6620953314177012 |
| A-P1-04 | P1 | FIXED | 앞 삽입 신규 행은 fail, 기존 행만 baseline exempt |
| A-P1-05 | P1 | FIXED | 외부 root basename 충돌에서도 신규 P6 검출 |
| A-P2-06 | P2 | OPEN | 위 Markdown block/첫 span의 누락·오탐 |
| A-P2-07 | P2 | FIXED | option 모양 `--base=--name-only` 일반 exit 2 |
| A-P2-08 | P2 | FIXED | WSL Git quoted/tab 파일명 추가 행 검출; Windows는 OS 제한 |
| A-P2-09 | P2 | FIXED | NaN/Infinity/음수/bool/중복 baseline·거대 수 일반 exit 2 |
| A-P2-10 | P2 | FIXED | 입력값·경로·baseline·argparse 합성 marker가 JSON/stderr/summary에 노출되지 않음 |
| A-P2-11 | P2 | FIXED | `--read-surface muted` 31쌍, tertiary/muted 미달 검출 |
| A-P3-12 | P3 | FIXED | geo 8쌍; airport task/evidence의 현재 1.320934와 역사 1.15 분리 |
| A-P1-13 | P1 | FIXED | `++counter;` 뒤 3행 P6가 Git diff added/fail |
| A-P2-14 | P2 | FIXED | 양 OS self-symlink root 일반 exit 2·traceback 없음 |
| A-P2-15 | P2 | FIXED | 양 도구 깊이 2000 JSON 일반 exit 2·traceback 없음 |

## 실제 실행

WSL은 `uv run --no-project --python 3.11`을 붙였고 전체 시험에는 `--with jsonschema`를 추가했다. WSL 정적 Git gate만 process `GIT_DIR`/`GIT_WORK_TREE`를 detached 경로로 지정했다. 합성 Git 반례에서는 해당 환경변수를 제거했고 저장소 config는 수정하지 않았다.

| 명령·대상 | Windows Python 3.14.3 | WSL Python 3.11.15 |
|---|---|---|
| `python -B -X utf8 -m unittest discover -s tests -p 'test_*.py'` | 286 통과·skip 0, 83.950초 | 286 실행·285 통과·skip 1, 52.127초; Windows 8.3 API 제외 |
| `python -B -X utf8 -m unittest tests.test_kt_contrast tests.test_ux_lint` | 48 통과, 11.883초 | 48 통과, 7.158초 |
| `python -B -X utf8 tools/validate_document_links.py` | 416 문서·2412 대상·오류 0 | 동일 |
| `python -B -X utf8 tools/validate_plan.py` | 106 task·오류 0 | 동일 |
| `python -B -X utf8 tools/check_spdx.py` | 56 파일·오류 0 | 동일 |
| `python -B -X utf8 tools/scan_secrets.py --all` | 548 파일·발견 0 | 동일 |
| `python -B -X utf8 tools/check_prod_redaction.py --all` | 548 파일·발견 0 | 동일 |
| `python -B -X utf8 tools/check_versions.py --self-check` | exit 0 | exit 0 |
| `python -B -X utf8 tools/check_aliases.py packages/tokens/aliases` | CSS 1개·오류 0 | 동일 |
| `git diff --check 94ca2f1730b270721eb6242bfcdd9362b51d45e5 559a9e8a0e49feca2dab9d59df29039bbb0acfd3` | exit 0 | exit 0 |
| canonical tokens CLI light/dark | 각각 27쌍 미달 0·exit 0 | 동일 |
| 4앱 예제·baseline CLI | 미달 4/8/8/4건, 등록 baseline exit 0 | 동일 |
| `ux_lint.py --root tests/fixtures/ux --json` | 보고 12건·기본 report 모드 exit 0 | 동일; 위반 0건을 뜻하지 않음 |
| 누적 독립 CLI corpus | 위 정상·잔여 반례 재현 | 동일; tab 파일명도 실행 |

- 제품 delta는 두 도구·두 시험 파일 62행 추가/2행 삭제로 전체 읽었다. task/evidence는 직전 코드 대비 동일하며 airport 현재 수용 기준과 역사 값 분리를 직접 확인했다.
- probe 명령: `python -B -X utf8 F:/dev/kor-travel-common/.git/codex-audit/t103-post8-reviewer-a-probe.py F:/dev/kor-travel-common-wt/review-t103-post8-a`; WSL은 `/mnt/f/...` 경로와 uv Python. 자신의 이전 실행 helper를 순차 실행하며 임시 fixture만 쓴다. SHA256: `6184624F4E993EE77D78F98276EF2890BCD20F5BC18E22D143900A9635FDD5D3`.
- CSS 대조: `node F:/dev/kor-travel-common/.git/codex-audit/t103-post8-reviewer-a-browser.cjs`; SHA256: `939D8C05ACF9CFFC0BD85882914327A2919E542B99798F325D4EE86A822EB2DB`.
- Markdown 대조: `node F:/dev/kor-travel-common/.git/codex-audit/t103-post8-reviewer-a-markdown.cjs`; SHA256: `DD5E214AEEF92DE0CD01B206CC37AAC368F38F70D4C700613D35FB45D9F3EE3B`. 설치된 `marked`를 사용했으며 registry 접근·설치는 하지 않았다.
- exact CI: `gh run list --commit 559a9e8a0e49feca2dab9d59df29039bbb0acfd3 --json databaseId,headSha,status,conclusion,url --limit 5`에서 [run 34178760599](https://github.com/digitie/kor-travel-common/actions/runs/34178760599)의 head SHA 일치 및 `completed/success`를 확인했다. 개별 job 로그를 이번 리뷰에서 재독하지 않았다.

## NOT_RUN 및 제한

- Windows Python 3.11: 실행 파일 부재. Windows tab 파일명은 OS 제한이며 WSL에서 실행했다. Windows self-symlink는 helper의 초기 플랫폼 안내와 별개로 후속 실제 생성·CLI 실행을 수행해 일반 exit 2를 확인했다.
- WSL 브라우저·Markdown 대조, 별도 MDX compiler: NOT_RUN. CSS 렌더링과 Markdown lexer 대조는 Windows이며 이를 소비자 실행 결과로 부르지 않는다.
- 소비자 build/e2e, npm/PyPI registry·게시, workflow dispatch, T-010 플랫폼 검사: NOT_RUN(검토 범위 밖). 후보와 manifest는 변경하지 않았으며 raw-only commit은 제품 수정 또는 이후 후보 검증이 아니다.
