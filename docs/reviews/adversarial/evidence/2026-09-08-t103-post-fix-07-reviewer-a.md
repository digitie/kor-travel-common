# T-103 post-fix-07 독립 적대적 리뷰 A 원본

- 실행 ID: `reviewer-a-t103-post-fix-07-20260908-105515`.
- 시작: 2026-09-08 10:55:15.370 KST. 제품 검토 종료: 2026-09-08 10:58:08.274 KST.
- 시작·종료 HEAD: `63fe3d5c969b28bab4d528d3e24a054e3a8e30e6`; tree: `c9fb07160de150d7a4cfbbb31fc226cb6a9fb3af`.
- 시작·종료 `git status --porcelain=v1`: 빈 출력. 새 detached worktree `review-t103-post7-a`에서 읽기·시험만 수행하고, 원본 보고서 한 파일만 추가하여 별도 commit한다.
- manifest: `dbfb036`의 `docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-07-manifest.md`를 `git show`로 읽었다. 수정 delta 기준선: `a40668bfb4ecac66d141da2ff791947d77208bd7`.
- 요청 범위: `:root` descendant·빈 selector 목록·중첩 JSX object·무들여쓰기 ESM·미종결 inline span 이후 JSX와 누적 CSS/media/JSON/argparse/redaction/diff/symlink/airport 반례를 Windows 3.14·WSL 3.11에서 독립 재현한다.
- 상대 post-fix-07 raw와 이전 상대 raw를 열지 않았으며 이번 상대 결과를 수신하지 않았다. 제품·소비자 파일, 소스 `.git/config`, registry 및 workflow dispatch는 변경하거나 호출하지 않았다.

## 최종 판정

**NO-GO.** 누적 15개 finding 중 13개 FIXED, `A-P1-01`(P1)과 `A-P2-06`(P2)은 잔여 반례로 OPEN이다. 새 ID는 없다. 이전에 제시한 정확한 반례는 이번 수정으로 닫혔지만 동일 원인의 인접 경계가 아래처럼 false PASS를 만든다.

## A-P1-01 / P1 / OPEN — root를 쓰지 않은 compound selector의 주석 우회가 남는다

- 위치: `tools/kt_contrast.py:96` `_strip_css_comments`, 166행 `_selector_has_compound_space`, 325행 이후 `_parse_blocks`의 지원 밖 selector 검사.
- 임시 `override.css` 내용: `.dark/**/.dark{--kt-brand:#fff;--kt-brand-foreground:#fff}`.
- 명령: `python -B -X utf8 tools/kt_contrast.py packages/tokens/tokens.css <임시경로>/override.css --dark --fail-new --json`.
- 실제: Windows 3.14.3·WSL 3.11.15 모두 exit 0, `status=PASS`, 27쌍 중 미달 0. 주석을 뺀 `.dark.dark`는 같은 명령에서 일반 입력 오류 exit 2이다.
- 렌더링 근거: Windows Playwright Chromium에 `<!doctype html><html class="dark">`와 위 선언을 적용했다. body의 color/background를 해당 변수에 연결한 `getComputedStyle` 결과는 둘 다 `rgb(255, 255, 255)`이다. 같은 요소를 선택하는 유효한 selector이며 실제 대비는 1:1이다.
- 원인·영향: 주석을 공백으로 바꿔 compound를 descendant로 오인한다. 이번 수정은 공백과 `:root`가 함께 있을 때만 오류를 내므로 `:root`가 없는 경우는 여전히 검사에서 누락된다. 지원 밖 문법에 주석을 넣으면 대비 미달을 정상값으로 통과시킨다.
- 수정·수용 조건: selector를 판정하기 전에 주석과 실제 공백의 의미를 구분한다. 위 사례는 실제 미달 exit 1 또는 지원 밖 문법의 일반 exit 2여야 한다. 주석 없는 동등 문법과 판정을 일치시키고 실제 하위 요소 선택자는 전역 값으로 승격하지 않는다.
- 정상 회귀: 이전 `:root/**/.dark`, `:root .dark`, `:root,`, 지원 밖 목록은 일반 exit 2로 닫혔다. selector 내부 문법 공백·인용값·대소문자·`.dark:root`·light/dark media 교집합의 기존 결과도 유지됐다.

## A-P2-06 / P2 / OPEN — JSX 주석의 중괄호와 1자 미종결 span이 실행 문맥을 가린다

- 위치: `tools/ux_lint.py:100` `_has_open_jsx_expression`의 중괄호 상태 추적; 332행 이후 span 마스킹 및 단일 backtick 분기.
- 재현 A: 아래를 임시 `fixture.mdx`에 저장한다. `// }`를 `/* } */`로 바꾼 경우도 별도로 실행했다.

```mdx
export function X() {
 return <div className={
 // }
 `outline-none`
 } />;
}
```

- 재현 B: 아래 별도 파일은 닫히지 않은 1자 inline delimiter와 그 다음 문단의 JSX이다.

```mdx
Example ` unmatched

export const X = () => <div className="outline-none" />;
```

- 명령: `python -B -X utf8 tools/ux_lint.py <임시경로>/fixture.mdx --fail-new --json`.
- 실제: A의 line/block 주석 두 경우와 B 모두 양 OS에서 exit 0, `status=PASS`, `fail_count=0`, findings 0건이다. 기대: 실행 값 `outline-none`의 P6를 보고해 exit 1. 파서가 문법을 지원하지 않는다고 판단한다면 false PASS 대신 일반 입력 오류로 닫아야 한다.
- 원인·영향: 새 JSX 중괄호 추적은 문자열을 제외하지만 JavaScript 주석은 제외하지 않아 주석의 `}`가 열린 속성을 닫아 버린다. 단일 backtick은 여전히 닫힘 없이 EOF까지 마스킹한다. 실행 속성은 바꾸지 않고 주석이나 앞쪽 문서만 추가해 신규 금지 패턴을 숨길 수 있다.
- 수정·수용 조건: JSX 문맥 추적에 line/block 주석 상태를 포함하고 이미 마스킹한 문맥과 일관되게 판정한다. 모든 길이의 Markdown span은 닫힌 경우만 제외한다. 정상 inline/fenced 예시를 실행 코드로 오인하지 않는 회귀도 유지한다.
- 정상 회귀: 직전 중첩 object, 무들여쓰기 ESM, 2자 미종결 span 이후 JSX는 각각 P6 1건·exit 1이다. 기존 다중행·blockquote·tagged/computed/배열/삼항 template 검출, 보간 주석 제외, escaped interpolation, 2자 code span·4자/tilde fence·suffix·blockquote 예시 제외도 유지됐다.

## 누적 disposition

| 원 ID | 심각도 | 판정 | 이번 확인 |
|---|---|---|---|
| A-P1-01 | P1 | OPEN | 위 `.dark/**/.dark` false PASS |
| A-P1-02 | P1 | FIXED | OKLCH chroma `25%`와 `0.1`의 RGB 동일 |
| A-P1-03 | P1 | FIXED | 흰색 20%/검정 source-over와 `#333` 대비 모두 1.6620953314177012 |
| A-P1-04 | P1 | FIXED | 앞 삽입 신규 행은 fail, 기존 행만 baseline exempt |
| A-P1-05 | P1 | FIXED | 외부 root의 basename 충돌에서 신규 P6 검출 |
| A-P2-06 | P2 | OPEN | 위 JSX 주석·미종결 1자 span false PASS |
| A-P2-07 | P2 | FIXED | option 모양 `--base=--name-only` 일반 exit 2 |
| A-P2-08 | P2 | FIXED | WSL Git quoted/tab 파일명 추가 행 검출; Windows는 OS 제한 |
| A-P2-09 | P2 | FIXED | NaN/Infinity/음수/bool/중복 baseline·거대 수 일반 exit 2 |
| A-P2-10 | P2 | FIXED | 입력값·경로·baseline·argparse의 합성 marker가 JSON/stderr/summary에 노출되지 않음 |
| A-P2-11 | P2 | FIXED | `--read-surface muted` 31쌍, tertiary/muted 미달 검출 |
| A-P3-12 | P3 | FIXED | geo 8쌍; airport task/evidence의 현재 1.320934와 역사 1.15 분리 유지 |
| A-P1-13 | P1 | FIXED | `++counter;` 다음 3행 P6가 Git diff added/fail |
| A-P2-14 | P2 | FIXED | 양 OS self-symlink root 일반 exit 2·traceback 없음 |
| A-P2-15 | P2 | FIXED | 양 도구의 깊이 2000 JSON 일반 exit 2·traceback 없음 |

## 실행과 검증 한계

아래 명령은 고정 후보 worktree에서 실행했다. WSL은 `uv run --no-project --python 3.11`을 붙였고 전체 시험에는 `--with jsonschema`를 추가했다. WSL 정적 Git gate에서만 process `GIT_DIR`/`GIT_WORK_TREE`로 해당 detached metadata를 지정했고 합성 Git 반례에서는 이를 제거했다. 저장소 config는 수정하지 않았다.

| 명령·대상 | Windows Python 3.14.3 | WSL Python 3.11.15 |
|---|---|---|
| `python -B -X utf8 -m unittest discover -s tests -p 'test_*.py'` | 285 통과·skip 0, 79.780초 | 285 실행·284 통과·skip 1, 52.581초; Windows 8.3 API 시험 제외 |
| `python -B -X utf8 -m unittest tests.test_kt_contrast tests.test_ux_lint` | 47 통과, 11.467초 | 47 통과, 7.295초 |
| `python -B -X utf8 tools/validate_document_links.py` | 413 문서·2412 대상·오류 0 | 동일 |
| `python -B -X utf8 tools/validate_plan.py` | 106 task·오류 0 | 동일 |
| `python -B -X utf8 tools/check_spdx.py` | 56 파일·오류 0 | 동일 |
| `python -B -X utf8 tools/scan_secrets.py --all` | 545 파일·발견 0 | 동일 |
| `python -B -X utf8 tools/check_prod_redaction.py --all` | 545 파일·발견 0 | 동일 |
| `python -B -X utf8 tools/check_versions.py --self-check` | exit 0 | exit 0 |
| `python -B -X utf8 tools/check_aliases.py packages/tokens/aliases` | CSS 1개·오류 0 | 동일 |
| `git diff --check 94ca2f1730b270721eb6242bfcdd9362b51d45e5 63fe3d5c969b28bab4d528d3e24a054e3a8e30e6` | exit 0 | exit 0 |
| canonical tokens CLI light/dark | 각각 27쌍 미달 0·exit 0 | 동일 |
| 4앱 예제·baseline CLI | 미달 4/8/8/4건; 등록 baseline exit 0 | 동일 |
| `ux_lint.py --root tests/fixtures/ux --json` | 보고 12건·기본 report 모드 exit 0 | 동일; 위반 0건을 뜻하지 않음 |
| 누적 독립 CLI corpus | 위 정상·잔여 반례 재현 | 동일; tab 파일명 추가 행 포함 |

- 제품 delta 두 도구·두 시험 파일의 94행 추가/5행 삭제를 전체 읽었다. task/evidence는 직전 후보와 동일하며 airport 현재 수용 기준과 역사 값 분리를 직접 확인했다. 이전 상대 raw를 읽지 않았다.
- 독립 probe: `python -B -X utf8 F:/dev/kor-travel-common/.git/codex-audit/t103-post7-reviewer-a-probe.py F:/dev/kor-travel-common-wt/review-t103-post7-a`. WSL은 동일 명령의 `/mnt/f/...` 경로와 uv Python을 사용한다. 자기 이전 helper를 순차 실행하여 누적 반례를 재현하고 임시 디렉터리만 사용한다. SHA256: `B0F20A99F57CBEB072A1A06DA1B48E5A64C3B2FAE930C59E0C1E6A5F0747DD0F`.
- Windows 실제 CSS 대조: `node F:/dev/kor-travel-common/.git/codex-audit/t103-post7-reviewer-a-browser.cjs`; helper SHA256: `5B58C4883CCB0DC06E0DD5672C956CE432E77F291414405071DCB0710B886B9C`.
- exact 후보 CI 조회: `gh run list --commit 63fe3d5c969b28bab4d528d3e24a054e3a8e30e6 --json databaseId,headSha,status,conclusion,url --limit 5`. [run 34178188880](https://github.com/digitie/kor-travel-common/actions/runs/34178188880)은 해당 SHA에서 `completed/cancelled`; 다른 SHA의 성공으로 대체하지 않는다.
- `NOT_RUN`: Windows Python 3.11은 실행 파일 부재. Windows tab 파일명은 OS 제한이며 WSL에서 재현했다. self-symlink는 초기 helper의 플랫폼 안내와 별개로 후속 실제 Windows 실행도 수행해 exit 2를 확인했다.
- `NOT_RUN`: WSL 브라우저·별도 MDX compiler, 소비자 build/e2e, npm/PyPI registry·게시, workflow dispatch, T-010 플랫폼 검사. exact 후보 CI 성공은 취소로 미완료다. 이번 원본 commit은 제품 변경이나 후속 수정 재검토를 의미하지 않는다.
