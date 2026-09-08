# T-103 수정 후 독립 적대적 리뷰 A 원본 01

- 실행 ID: `A-T103-POST1-20260908-092427`.
- 시작: 2026-09-08 09:24:27.177 KST. 코드 검증 종료: 2026-09-08 09:33:48.190 KST.
- manifest: commit `f5d523fed7f3e49a25664b0d5508b8546354912b`의 `docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-01-manifest.md`를 `git show`로 읽었다. manifest commit 자체를 코드 후보로 바꾸지 않았다.
- 실제 후보: `f9666078f49ea0745f485d6d0c88206048675aae`; tree `6bcda765a470f0aed8a314512edefa7fae2fb0e9`.
- 수정 대조 기준: 최초 후보 `d12ccba48f67ad8ac863dbc97d85dda289c1e09c`; 최초 manifest `94ca2f1730b270721eb6242bfcdd9362b51d45e5`.
- 격리: `F:/dev/kor-travel-common-wt/review-t103-post1-a` detached. 시작·코드 검증 종료의 `git rev-parse HEAD HEAD^{tree}`가 위 값과 같고 `git status --porcelain=v1`은 모두 빈 출력이었다. 검증 후 이 원본 한 파일만 추가해 별도 commit한다. 제품·소비자 파일, source checkout 설정은 변경하지 않았다.
- 전달 요청: 최초 A의 `A-P1-01`부터 `A-P3-12`까지 수정 여부와 신규 P0–P3를 Windows/WSL에서 독립 공격하고, 원본을 작성·commit하여 SHA256·verdict를 보고한다. 소비자·registry·workflow dispatch는 호출하지 않는다.
- [자신의 최초 원본](2026-09-08-t103-reviewer-a.md)과 수정 delta를 검토했다. 상대 reviewer 원본·결과는 읽거나 요청하지 않았다. 상대 원본 파일 내용은 delta 통독에서도 제외했다.

## 최종 판정

**NO-GO**. 기존 12건 중 **FIXED 9건 / OPEN 3건**, 신규 **OPEN 2건**이다. 미해결 집계는 **P0 0 / P1 2 / P2 3 / P3 0**이다. 정상 회귀 성공이 아래 false PASS와 출력 노출을 해소하지 않는다.

## 최초 finding disposition

| 원 ID·심각도 | disposition | 직접 검증 결과 |
|---|---|---|
| A-P1-01 / P1 | OPEN, 일부 수정 | 원 `:root:not(.dark)`·content 위조 선언은 미달을 탐지하고 단순 미지원 조건은 exit 2. 그러나 specificity·하위/중첩 selector·문자열 속 comment delimiter 반례가 양 OS에서 false PASS다. 아래 상세 참조. |
| A-P1-02 / P1 | FIXED | `oklch(60% 25% 30)`과 `oklch(60% 0.1 30)`의 Color 세 채널이 양 OS에서 완전히 같다. 경계 수치 회귀도 통과했다. |
| A-P1-03 / P1 | FIXED | white 20%/black의 비율이 양 OS에서 `1.6620953314177012`, 실제 표시색 `#333`/black 계산과 같다. 4앱 baseline을 다시 실행했고 alpha 변경이 airport baseline/evidence에 반영됐다. |
| A-P1-04 / P1 | FIXED | 기존 P6 1건 앞에 신규 P6을 삽입하고 count 1 baseline 사용: 신규 행 `exempt=false, added=true, fail=true`; 기존 행 `exempt=true, added=false`. exit 1, 실패 1건. |
| A-P1-05 / P1 | FIXED | 외부 root의 `one/page.tsx` 위반·`two/page.tsx` 정상 조합에서 두 경로가 충돌하지 않고 위반 1건·exit 1. 외부 root Git 회귀도 통과했다. |
| A-P2-06 / P2 | OPEN, 일부 수정 | 같은 실행 template의 TSX는 P6/P8 2건·exit 1. MDX로 옮기면 0건·exit 0으로 여전히 누락된다. |
| A-P2-07 / P2 | FIXED | 실제 Git repo에서 `--base=--name-only`는 양 OS exit 2·traceback 없음. |
| A-P2-08 / P2 | FIXED | WSL의 tab 포함 tracked 파일 추가 행을 이제 P6 1건·exit 1로 탐지한다. Windows tab 파일 생성은 파일명 제약으로 NOT_RUN이다. |
| A-P2-09 / P2 | FIXED | UX Infinity count, 400자리 CSS 수치, 잘못된 대비 version, 개별 NaN/음수 measured·Infinity/음수/bool required·중복 대비 쌍 모두 양 OS exit 2·traceback 없음. |
| A-P2-10 / P2 | OPEN, 일부 수정 | 원 잘못된 색 값·만료 baseline marker는 출력되지 않는다. CSS 읽기 오류·var 오류에는 자격증명 모양 입력이, UX 경로에는 사설 주소 모양 입력이 여전히 나온다. |
| A-P2-11 / P2 | FIXED | `--read-surface muted --fail-new --json`이 31쌍을 검사하고 실제 `text-tertiary/surface-muted` 미달을 exit 1로 탐지한다. task/README에도 추가 표면 옵션이 있다. |
| A-P3-12 / P3 | FIXED | geo light 미달 8건을 양 OS에서 재현했고 수정 evidence의 8건과 일치한다. baseline 적용 시 exit 0. |

## A-P1-01 잔여 — CSS cascade와 문자열 경계에서 실제 1:1을 PASS

- 위치: `tools/kt_contrast.py:89`, `:125`, `:158`, `:238`.
- 공통 명령: 아래 각 문자열을 임시 `override.css`에 쓰고 `python -B -X utf8 tools/kt_contrast.py packages/tokens/tokens.css <override.css> --fail-new --json`을 실행한다.

```css
/* 서로 독립된 반례 4개: 각각 별도 파일로 실행 */
:root:not(.dark){--kt-brand:#fff;--kt-brand-foreground:#fff} :root{--kt-brand:#000}
:root{--kt-brand:#fff;--kt-brand-foreground:#fff} :root .child{--kt-brand:#000}
:root{--kt-brand:#fff;--kt-brand-foreground:#fff; .child{--kt-brand:#000}}
:root{content:"/*";--kt-brand:#fff;--kt-brand-foreground:#fff;content:"*/";}
```

- 실제: 네 반례 모두 Windows/WSL **exit 0 / PASS / 27쌍 미달 0**. Windows headless Chromium의 light, 800×600, child class 없는 body에 `color:var(--kt-brand-foreground);background:var(--kt-brand)`를 적용해 네 경우 모두 foreground/background `rgb(255, 255, 255)`를 직접 관찰했다. 실제 대비는 1:1이다.
- 원인: specificity 없이 마지막 선언만 덮고, `:root` 부분 문자열로 하위 selector를 root로 승격하며, 부모 body에서 중첩 자식 선언을 추출한다. 주석 제거 regex는 CSS 문자열 안의 `/*`·`*/`까지 주석으로 처리한다.
- 반대 오탐도 남는다: light 검사에 `:root.dark{--kt-brand:#fff;--kt-brand-foreground:#fff}` 또는 `@media(prefers-color-scheme:dark){:root{...}}`를 넣으면 두 미달을 보고한다. dark 검사에서 `@media (prefers-color-scheme: dark) and (max-width:1px){:root{...}}`를 조건 확인 없이 적용한다.
- 영향: 적법한 CSS가 실제와 다른 토큰 값으로 계산돼 미달 gate를 우회하거나 정상 입력을 차단한다.
- 수정 수용: 지원 문법을 한정하더라도 selector·scope·cascade를 정확하게 처리하고, 그 밖의 조건·중첩은 명시적 exit 2로 닫아야 한다. 문자열/주석/직접 선언 경계를 분리하고 위 양방향 CLI·브라우저 반례를 회귀로 고정한다. 현 상태로 FIXED 처리할 수 없다.

## A-P2-06 잔여 — MDX의 실행 template를 인용으로 삭제

- 위치: `tools/ux_lint.py:64`, `:171`.
- 임시 `runtime.mdx` 내용: ``export const X = () => <div className={`outline-none ${window.confirm("x")}`} />;``.
- 명령: `python -B -X utf8 tools/ux_lint.py <runtime.mdx> --fail-new --json`.
- 실제: 양 OS **exit 0 / PASS / findings 0**. 동일 내용을 `.tsx`로 저장하면 **exit 1 / P6·P8 2건**이다. `.mdx` 확장자 전체에 `ignore_backticks=True`를 적용한다.
- 영향: 지원 대상 MDX의 실행 JSX/ESM 문자열과 interpolation이 금지 규칙을 우회한다.
- 수정 수용: MDX 문서의 inline/fenced 인용과 실행 ESM/JSX 표현식을 구별한다. 문서 인용 음성 시험을 유지하면서 이 실행 양성 사례도 탐지해야 한다.

## A-P2-10 잔여 — 오류/경로 출력 채널의 비식별화 누락

- 위치: `tools/kt_contrast.py:246`, `:347`, `:360`; `tools/ux_lint.py:58`, `:454`.
- 합성값은 원문을 보고서·로그에 적지 않았다. 자격증명 모양 marker는 Python `marker = 'gh' + 'p_' + 'Z' * 24`, 주소 모양 marker는 `'.'.join(map(str, [10, 23, 45, 67]))`로 생성했다. 실제 자격증명·운영 주소는 사용하지 않았다.
- 반례 1: 존재하지 않는 `<marker>.css`를 `kt_contrast.py --json`에 전달하면 양 OS exit 2지만 `marker in stderr`가 true다.
- 반례 2: `:root{--kt-brand:var(--kt-<marker>)}` 임시 override를 canonical 뒤에 전달해도 exit 2이고 stderr에 marker가 남는다.
- 반례 3: 주소 모양 파일명에 `.tsx`를 붙여 `const x="outline-none";`을 저장한다. `ux_lint.py <file> --json --step-summary <summary.md>` 실행 시 양 OS에서 JSON과 summary 모두 `marker in output`이 true다. UX credential regex는 주소 계열을 처리하지 않는다.
- 영향: 입력 값이 stderr/JSON/CI summary에 복제된다. 원 색 값·baseline 값 수정만으로 전체 출력 비공개 계약을 충족하지 못한다.
- 수정 수용: generic 입력 오류와 검증된 식별자 또는 공유 redactor를 사용한다. 파일명·참조명·만료 baseline 경로까지 stdout/stderr/Markdown/summary를 실제 검사하며 marker가 전부 없어야 한다.

## A-P1-13 신규 — diff hunk 안의 `+++`를 파일 header로 오인

- 위치: `tools/ux_lint.py:255`–`:265`, 특히 `:261`.
- 최소 재현: 임시 Git repo에서 `a.tsx`에 `let counter=0;` 한 줄을 commit하고, 다음처럼 수정한다.

```tsx
let counter=0;
++counter;
const x="outline-none";
```

- 명령: `python -B -X utf8 tools/ux_lint.py --root <repo> --base HEAD --json`.
- 실제: Windows/WSL **exit 0 / PASS**, P6 finding은 `line=3, added=false, fail=false`다. baseline은 없다. 실제 Git diff의 추가 `++counter;` 행은 앞에 `+`가 붙어 `+++counter;`가 되므로 header 제외 조건에 걸려 새 행 번호도 증가하지 않는다.
- 영향: 일반적인 전위 증가문 다음에 추가한 UX 위반이 `--base` 신규 실패 gate를 우회한다. 전체 regex가 위반을 발견해도 diff 분류에서 숨긴다.
- 수정 수용: hunk 진입 상태와 파일 header를 분리하고 hunk 내부의 모든 `+` 행을 추가 행으로 처리한다. `++counter;` 뒤 P6과 실제 source가 `+++`로 시작하는 경우, 여러 hunk·삭제/추가 혼합을 회귀로 검증한다. 이 반례는 반드시 exit 1·line 3 added=true가 돼야 한다.

## A-P2-14 신규 — WSL self-symlink root에서 traceback과 경로 노출

- 위치: `tools/ux_lint.py:405`, `:472`.
- 최소 재현: 임시 디렉터리에서 `loop = root / ('loop-' + marker); loop.symlink_to(loop.name)`으로 self-symlink를 만들고 `ux_lint.py --root <loop> --json`을 호출한다. marker 생성은 A-P2-10과 같다.
- 실제 WSL Python 3.11.15: **exit 1**, `Traceback in stderr=true`, `marker in stderr=true`. `Path.resolve()`의 RuntimeError가 `UxLintError` 처리 범위를 벗어난다. Windows 직접 symlink는 권한 의존으로 NOT_RUN이며 양 OS 성공으로 집계하지 않았다.
- 영향: 잘못된 경로가 약속된 입력 오류 형태로 닫히지 않고 실행 내부와 입력 경로를 노출한다.
- 수정 수용: root/입력 경로 해석의 symlink loop·I/O 예외를 generic exit 2로 변환한다. 직접·중간 self-symlink를 양 OS에서 확인하고 traceback/marker가 없어야 한다.

## 실행 명령과 결과

- Windows Python 3.14.3: `python -B -X utf8 -m unittest discover -s tests -p 'test_*.py'` → **260개 PASS, skip 0, 68.090초**.
- WSL Python 3.11.15: `uv run --no-project --with jsonschema --python 3.11 python -B -X utf8 -m unittest discover -s tests -p 'test_*.py'` → **260개 발견, 259개 PASS, Windows 전용 1개 skip, 44.999초**. skip은 PASS로 세지 않았다.
- 집중 시험: `python -B -X utf8 -m unittest tests.test_kt_contrast tests.test_ux_lint -v` → Windows **22개 PASS / 6.065초**. WSL은 같은 모듈 명령을 uv Python 3.11로 실행해 **22개 PASS / 2.626초**, 모두 skip 0.
- 양 OS 정적 gate: `tools/validate_document_links.py` → 문서 397·target 2411·오류 0; `tools/validate_plan.py` → task 106·오류 0; `tools/check_spdx.py` → 소스 56·오류 0; `tools/scan_secrets.py --all`, `tools/check_prod_redaction.py --all` → 각각 529개·발견 0; `git diff --check 94ca2f1730b270721eb6242bfcdd9362b51d45e5 HEAD` → exit 0.
- WSL 정적 gate만 process 환경의 `GIT_DIR=/mnt/f/dev/kor-travel-common/.git/worktrees/review-t103-post1-a`, `GIT_WORK_TREE=/mnt/f/dev/kor-travel-common-wt/review-t103-post1-a`로 detached 메타데이터를 지정했다. source `.git/config`는 수정하지 않았다. synthetic Git probe는 이 환경과 summary 환경을 제거했다. 최초 반복 shell 명령 2회는 변수 전달이 소실되어 실행 오류였고, 명시적 개별 명령으로 다시 실행해 위 성공을 확인했다.
- 직접 CLI: canonical light/dark 각 27쌍 PASS; docker-manager/concierge/geo/airport light 미달 4/8/8/4건이며 각각 baseline `--fail-new` exit 0. `ux_lint.py --root tests/fixtures/ux --json`은 전체 report 12건·fail 0·exit 0. report 기본 모드의 PASS는 위반 0이라는 뜻으로 세지 않았다.
- 반례 명령: Windows `python -B -X utf8 F:/dev/kor-travel-common/.git/codex-audit/t103-post1-reviewer-a-probe.py F:/dev/kor-travel-common-wt/review-t103-post1-a`; WSL은 두 경로를 `/mnt/f/...`로 바꾸고 `uv run --no-project --python 3.11 python -B -X utf8`로 실행했다. helper SHA256 `BB5C5E12E6E0007F376F54C61BA6933CC34A1B0B109563291019DAE3B26CAA49`이며 최초 A helper를 읽어 이전 반례도 함께 재생한다. helper는 후보 트리 밖 임시 파일만 작성하고 합성값 대신 exit·boolean·건수만 출력한다.
- Windows 브라우저: `node F:/dev/kor-travel-common/.git/codex-audit/t103-post1-reviewer-a-browser.cjs`; helper SHA256 `08CB78352AA768DC742F55488A3BEF16F0631C6078D77EB34053717D83FB84C1`. bundled Playwright의 headless Chromium에서 위 CSS 반례 4종을 직접 확인했다. 이 브라우저 의존성은 검증용이며 제품의 stdlib 계약을 변경하지 않았다.
- 원격 읽기: `gh run list --commit f9666078f49ea0745f485d6d0c88206048675aae --json databaseId,headSha,status,conclusion,url --limit 5` → exact SHA의 run `34173131041`은 completed/cancelled였다. [해당 run](https://github.com/digitie/kor-travel-common/actions/runs/34173131041). 다른 commit의 CI 성공을 이 코드 SHA의 직접 성공으로 옮겨 적지 않았다.

## 검토 범위와 NOT_RUN

- 최초 후보→수정 후보의 제품 두 도구·두 시험·task·도구 README·4앱 evidence·airport baseline과 자신의 원본/manifest를 대조했다. 상대 원본은 독립성 규칙에 따라 내용 미열람이다. 변경 없는 초기 정본의 전체 재통독은 최초 리뷰에 의존하되 이번 task·관련 계약과 수정 delta는 직접 확인했다.
- NOT_RUN: Windows 금지 tab 파일명; Windows 직접 symlink 권한 검사; WSL 브라우저; exact code SHA의 성공 CI(관찰 run은 cancelled); 소비자 build/e2e·registry·배포·workflow dispatch·T-010 selftest. 소비자 gate는 해당 이관 task와 후행 T-010이 소유한다.
- 발견된 미해결 P1/P2를 수정한 새 immutable 후보와 두 독립 재검토가 필요하다. 이 원본은 성공 CI나 작성자 수정 의도만으로 closure를 승인하지 않는다.
