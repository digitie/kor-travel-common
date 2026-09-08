# T-103 post-fix-06 독립 적대적 리뷰 A 원본

- 실행 ID: `reviewer-a-t103-post-fix-06-20260908-104148`
- 검토 시작: 2026-09-08 10:41:48.057 KST. 제품 검토 종료: 2026-09-08 10:47:57.131 KST.
- 불변 코드 후보, 시작·종료 HEAD: `a40668bfb4ecac66d141da2ff791947d77208bd7`.
- 시작·종료 tree: `9c5cbf93bc6b34c4895c98745404375becbc0b32`.
- 시작·종료 `git status --porcelain=v1`: 빈 출력. 격리 방식: 별도 detached worktree `review-t103-post6-a`. 이 원본을 추가하기 전까지 후보 코드·문서·시험을 변경하지 않았다.
- manifest: `6372b29f40abaf2168594fdf792eb44009264a54`의 `docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-06-manifest.md`를 `git show`로 읽었다. 직전 코드 기준선은 `ecad460db93a9369d96435a28b6cb48dd7516ace`이다.
- 요청: selector 내부 공백·문자열 대소문자·지원 밖 목록, 다중행 JSX·ESM·blockquote·2자 inline span 및 누적 CSS cascade/media·JSON/argparse/redaction/diff/symlink/airport 반례를 Windows 3.14·WSL 3.11에서 독립 검증하고, 원본 한 파일만 별도 commit한다. Windows 3.11은 NOT_RUN으로 기록한다.
- 독립성: 상대 raw와 이전 상대 raw를 열지 않았다. 검증 완료 뒤 coordinator가 상대 finding 요약을 메시지로 보내 독립 원본 확정 전 수신하게 되었다. 아래 두 finding과 재현 출력은 그 수신 전에 실행 완료한 자신의 probe 결과이며, 수신 내용을 추가 검증·판정 근거로 사용하지 않았다.

## 판정

**NO-GO.** 누적 15개 ID 중 13개 FIXED, `A-P1-01`과 `A-P2-06`은 부분 수정 후 잔여 반례가 있어 OPEN이다. 열린 심각도는 P1 1건·P2 1건이며 새 ID는 없다. 양 OS 회귀 성공은 아래 CLI의 잘못된 PASS를 해소하지 않는다.

## 남은 finding과 최소 재현

### A-P1-01 / P1 / OPEN — selector 주석이 실제 cascade를 바꾸어 해석된다

- 위치: `tools/kt_contrast.py:96`의 `_strip_css_comments`, `tools/kt_contrast.py:166`의 `_selector_has_compound_space`, `tools/kt_contrast.py:205`의 `_selector_rules`.
- 임시 `override.css` 내용: `:root/**/.dark{--kt-brand:#fff;--kt-brand-foreground:#fff}`.
- 명령: `python -B -X utf8 tools/kt_contrast.py packages/tokens/tokens.css <임시경로>/override.css --dark --fail-new --json`.
- Windows 3.14.3와 WSL 3.11에서 동일하게 exit 0, `status=PASS`, 27쌍 중 미달 0건이다. 주석을 공백으로 바꾼 결과 같은 요소의 `:root.dark` compound selector가 descendant처럼 판정되어 오버라이드가 누락된다.
- 실제 렌더링 대조: Windows Node·Playwright Chromium에서 `<!doctype html><html class="dark">`와 위 CSS를 사용하고 body의 전경/배경을 해당 변수에 연결했다. `getComputedStyle(document.body)`는 전경·배경 모두 `rgb(255, 255, 255)`였다. 따라서 `brand-foreground/brand` 실제 대비는 1:1이며 4.5:1에 미달한다.
- 영향: 유효한 CSS의 대비 미달이 `--fail-new` gate를 통과한다. 단순 주석 추가로 token override를 검사에서 빠뜨릴 수 있다.
- 수정 권고와 수용 조건: 주석과 문법 공백을 구분해 selector 의미를 보존한다. 위 사례는 미달 exit 1이어야 하며, 지원하지 않는다고 결정한다면 일반 입력 오류 exit 2로 닫아야 한다. 실제 descendant selector, 선언·인용 문자열의 주석 경계 및 light/dark 회귀는 유지해야 한다.
- 이번 수정의 정상 결과: `:root:where( .dark )`, `.DARK`, `[data-theme='d ark']`, 지원·비지원 selector 혼합 목록은 일반 exit 2로 닫힌다. `.dark:root`와 인용 방식이 다른 지원 attribute selector는 실제 미달 exit 1로 검사한다.

### A-P2-06 / P2 / OPEN — 다중행 실행 template과 미종결 inline delimiter가 뒤의 실행 코드를 숨긴다

- 위치: `tools/ux_lint.py:100`의 `_is_executable_mdx_template`, 특히 123–128행의 정규식·들여쓰기 조건; 73행의 `_find_backtick_run_end`와 299–306행의 inline span 마스킹.
- 아래 각각을 별도 임시 `.mdx`에 저장한 뒤 `python -B -X utf8 tools/ux_lint.py <임시경로>/fixture.mdx --fail-new --json`을 실행했다. 세 사례 모두 양 OS에서 exit 0, `status=PASS`, `fail_count=0`, findings 0건이다.

```mdx
export const classes =
`outline-none`;
```

```mdx
export function classes(a,b){return b;}

export function X() {
  return <div className={classes(
    {},
    `outline-none`
  )} />;
}
```

```mdx
Example `` unmatched

export const X = () => <div className="outline-none" />;
```

- 첫 사례는 들여쓰기 없는 유효한 ESM 선언이므로 template 문자열이 검사되어야 한다. 둘째 사례는 JSX 속성의 중간 object literal 때문에 `[^{}]*` 기반 열린 문맥 추적이 끊긴다. 셋째 사례는 닫히지 않은 Markdown inline delimiter를 EOF까지 코드로 취급하여 별도 문단의 JSX까지 마스킹한다.
- 영향: 같은 실행 값을 줄 나눔·중간 object·앞쪽 Markdown 문구만 바꾸어 금지 `outline-none`(P6)의 신규 검사를 우회한다.
- 수정 권고와 수용 조건: 실행 영역의 괄호·중괄호·문자열 상태를 추적하고 들여쓰기로 실행 여부를 결정하지 않는다. 닫힌 Markdown code span만 제외한다. 세 사례는 실제 P6를 보고해 exit 1이어야 한다. 해당 문법을 해석할 수 없다면 false PASS 대신 입력 오류로 닫는다.
- 이번 수정의 정상 결과: 기존 들여쓴 다중행 JSX·ESM과 blockquote JSX는 exit 1; 정상 2자 inline span은 findings 0; 배열·삼항·일반/computed tag template은 검출; 4자 backtick·tilde fence와 blockquote 인용 예제는 제외된다.

## 누적 ID별 disposition

| 원 ID | 원 심각도 | 판정 | 이번 직접 확인 |
|---|---|---|---|
| A-P1-01 | P1 | OPEN | 위 CSS 주석 compound false PASS; 기존 공백·대소문자·조건 교집합 반례는 수정됨 |
| A-P1-02 | P1 | FIXED | OKLCH chroma `25%`와 `0.1`의 RGB 결과 동일 |
| A-P1-03 | P1 | FIXED | 흰색 20%/검정 source-over와 `#333` 대비 모두 1.6620953314177012 |
| A-P1-04 | P1 | FIXED | baseline 앞 삽입 신규 행은 fail, 기존 행만 exempt |
| A-P1-05 | P1 | FIXED | 외부 root의 같은 basename 충돌에서도 신규 P6 exit 1 |
| A-P2-06 | P2 | OPEN | 위 MDX 세 반례; 기존 template·fence·보간 주석 반례는 수정됨 |
| A-P2-07 | P2 | FIXED | option 모양 `--base=--name-only` 일반 입력 오류 exit 2 |
| A-P2-08 | P2 | FIXED | WSL의 Git quoted/tab 파일명 추가 행 검출; Windows 파일명은 NOT_RUN |
| A-P2-09 | P2 | FIXED | NaN/Infinity/음수/bool/중복 baseline·400/5000자리 수 일반 exit 2 |
| A-P2-10 | P2 | FIXED | 입력값·누락 경로·var·baseline·비공개 형태 경로의 marker가 JSON/stderr/summary에 노출되지 않음; argparse 일반 exit 2 |
| A-P2-11 | P2 | FIXED | `--read-surface muted` 31쌍 검사, `text-tertiary/surface-muted` 미달 검출 |
| A-P3-12 | P3 | FIXED | geo 예제 미달 8쌍; task/evidence의 현재 airport 1.320934와 역사 1.15 분리 확인 |
| A-P1-13 | P1 | FIXED | `++counter;` 때문에 hunk를 잃지 않고 다음 3행 P6가 added/fail |
| A-P2-14 | P2 | FIXED | self-symlink root 양 OS 일반 exit 2, traceback 없음 |
| A-P2-15 | P2 | FIXED | 깊이 2000 JSON 양 도구·양 OS 일반 exit 2, traceback 없음 |

## 실행 명령과 결과

작업 디렉터리는 불변 detached 후보이다. Windows는 Python 3.14.3, WSL은 `uv run --no-project --python 3.11`의 Python 3.11이며 전체 시험에는 `--with jsonschema`를 추가했다. WSL 정적 Git gate에만 process `GIT_DIR`/`GIT_WORK_TREE`로 해당 detached 경로를 지정했다. 소스 `.git/config`는 수정하지 않았고 합성 Git 반례에서는 이 환경변수를 제거했다.

| 명령·대상 | Windows | WSL |
|---|---|---|
| `python -B -X utf8 -m unittest discover -s tests -p 'test_*.py'` | 282 실행·282 통과·skip 0, 86.528초 | 282 실행·281 통과·skip 1, 54.105초; Windows 8.3 API 시험 제외 |
| `python -B -X utf8 -m unittest tests.test_kt_contrast tests.test_ux_lint -v` | 44 통과, 11.652초 | 44 통과, 6.739초 |
| `python -B -X utf8 tools/validate_document_links.py` | 410 문서·2412 대상·오류 0 | 동일 |
| `python -B -X utf8 tools/validate_plan.py` | 106 task·오류 0 | 동일 |
| `python -B -X utf8 tools/check_spdx.py` | 56 파일·오류 0 | 동일 |
| `python -B -X utf8 tools/scan_secrets.py --all` | 542 파일·발견 0 | 동일 |
| `python -B -X utf8 tools/check_prod_redaction.py --all` | 542 파일·발견 0 | 동일 |
| `python -B -X utf8 tools/check_versions.py --self-check` | exit 0 | exit 0 |
| `python -B -X utf8 tools/check_aliases.py packages/tokens/aliases` | CSS 1개·오류 0 | 동일 |
| `git diff --check 94ca2f1730b270721eb6242bfcdd9362b51d45e5 a40668bfb4ecac66d141da2ff791947d77208bd7` | exit 0 | exit 0 |
| `kt_contrast.py packages/tokens/tokens.css --json` 및 `--dark` | 각각 27쌍 미달 0 | 동일 |
| 4앱 예제·baseline corpus | 미달 4/8/8/4건 확인; 등록 baseline exit 0 | 동일 |
| `ux_lint.py --root tests/fixtures/ux --json` | 보고 12건, 기본 report 모드 exit 0 | 동일; 위반 0건을 뜻하지 않음 |
| 독립 누적 CLI probe | 기존 반례 및 위 잔여 반례 재현 | 동일; tab 파일명도 실행 |

- 제품 delta는 두 도구·두 시험 파일의 142행 추가/38행 삭제이며 전체를 읽었다. task/evidence는 직전 코드 대비 불변이고 airport의 현재 계산값과 과거 조사값 구분도 직접 검색했다. 불필요한 이전 raw 재독은 하지 않았다.
- 독립 probe 명령: `python -B -X utf8 F:/dev/kor-travel-common/.git/codex-audit/t103-post6-reviewer-a-probe.py F:/dev/kor-travel-common-wt/review-t103-post6-a`; WSL은 `/mnt/f/...` 경로와 위 uv Python을 사용했다. 임시 디렉터리에서 fixture·Git 저장소를 생성하고 후보는 읽기만 했다.
- probe SHA256: `5B27435B03327D5D9478AAC276C99F98E504FA70A7E079339F63A67861D0C759`. 자신의 초기·post1·post3·post4·post5 helper를 순차 실행하는 누적 corpus이다.
- 브라우저 대조 명령: `node F:/dev/kor-travel-common/.git/codex-audit/t103-post6-reviewer-a-browser.cjs`. helper SHA256: `DA4E24D959328D984EF136CF569A2D017227D18303C0F22A4FB1A8D46ECF854C`.
- exact 후보 CI를 `gh run list --commit a40668bfb4ecac66d141da2ff791947d77208bd7 --json databaseId,headSha,status,conclusion,url --limit 5`로 읽었다. [run 34177437033](https://github.com/digitie/kor-travel-common/actions/runs/34177437033)은 해당 SHA에서 `completed/cancelled`였다. 다른 SHA의 CI 성공을 이 코드 후보의 성공으로 집계하지 않았다.

## 미실행과 한계

- `NOT_RUN`: Windows Python 3.11 실행 파일 부재. Windows 3.14 결과를 3.11 결과로 대체 표기하지 않았다.
- `NOT_RUN`: Windows의 tab 포함 파일명은 OS 제한. 해당 반례는 WSL에서 실행했다. self-symlink는 helper의 초기 플랫폼 안내와 별개로 후속 실제 생성·CLI 실행을 Windows에서도 성공했으며 그 결과를 위에 기록했다.
- `NOT_RUN`: WSL 브라우저 렌더링·별도 MDX compiler 실행. CSS 렌더링 대조는 Windows Chromium이며 MDX는 후보 CLI와 코드의 실행 문맥 판정으로 확인했다.
- `NOT_RUN`: 소비자 저장소 build/e2e, npm/PyPI registry·게시, workflow dispatch, T-010 플랫폼 검사. 이번 읽기·합성 fixture 리뷰 범위 밖이며 common의 로컬 성공으로 외부 gate를 닫지 않는다.
- exact 후보 CI는 취소 상태여서 성공 검증은 미완료이다. 원본은 위 불변 제품 tree에 귀속되며, 이후 report-only commit은 제품 수정 또는 수정 후 재검토를 뜻하지 않는다.
