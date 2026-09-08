# T-103 수정 후 독립 적대적 리뷰 A 원본 03

- 실행 ID: `A-T103-POST3-20260908-095330`.
- 시작: 2026-09-08 09:53:30.230 KST. 코드 검증 종료: 2026-09-08 09:57:20.107 KST.
- manifest: `826f6107fbb3d6a45fce348ad19dc1b25c7cfde7`의 `docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-03-manifest.md`를 `git show`로 직접 읽었다.
- 실제 불변 코드 후보: `790bc3ec136b480c9cb95d796990ac1cbb07c596`; tree `496e44bd27124255437ef265d29e29d680f29e94`.
- 격리: `F:/dev/kor-travel-common-wt/review-t103-post3-a` detached. 시작·코드 검증 종료 `git rev-parse HEAD HEAD^{tree}`가 위 값과 같고 `git status --porcelain=v1`은 모두 빈 출력이다. 검증 종료 후 이 원본 한 파일만 별도 commit한다.
- 요청: CSS specificity/source order·media·중첩/문자열/주석, MDX 인용·실행 template·보간 주석, diff `+++`, huge JSON/symlink/redaction, airport task/evidence를 Windows/WSL에서 독립 공격하고 원본 commit·SHA256·verdict를 반환한다.
- post-fix-02는 중단됐고 최종 원본이 없다. 그 실행을 이 후보의 검증으로 집계하지 않았다. 이전 post-fix raw와 상대 원본·결과는 읽거나 요청하지 않았다. 원 ID는 전달 이력으로 유지하며 자신의 외부 합성 probe corpus를 새 SHA에서 재실행했다.
- 제품·소비자 파일과 source `.git/config`를 수정하지 않았고 registry·workflow dispatch·배포를 호출하지 않았다.

## 판정

**NO-GO**. 기존 A ID 14건 중 **FIXED 12건 / OPEN 2건**, 신규 **OPEN 1건**이다. 미해결 심각도는 **P0 0 / P1 1 / P2 2 / P3 0**이다.

## 기존 finding별 disposition

| 원 ID·심각도 | disposition | 새 후보에서 관찰한 결과 |
|---|---|---|
| A-P1-01 / P1 | OPEN, 일부 수정 | 이전 specificity 반례는 미달을 탐지한다. 하위 selector 전역 오염·중첩·문자열 comment delimiter·단순 not/compound media도 수정됐다. 그러나 media와 selector 조건의 교집합 누락 및 `:root.dark` 선언 누락이 false PASS를 만든다. |
| A-P1-02 / P1 | FIXED | OKLCH chroma `25%`와 `0.1`의 세 채널 값이 양 OS에서 같다. 집중 수학 시험 통과. |
| A-P1-03 / P1 | FIXED | white 20%/black 비율 `1.6620953314177012`가 `#333`/black과 같다. airport 현재 수용 기준은 task/evidence에서 1.32로 동기화됐고 역사 1.15와 구분된다. |
| A-P1-04 / P1 | FIXED | baseline 1건 앞에 새 위반 삽입: 신규 행 `exempt=false, added=true, fail=true`; 기존 행만 면제. 양 OS exit 1. |
| A-P1-05 / P1 | FIXED | 외부 root의 서로 다른 하위 디렉터리 동명 파일이 충돌하지 않고 위반 1건·exit 1. 외부 Git root 회귀 통과. |
| A-P2-06 / P2 | OPEN, 일부 수정 | 일반 MDX template의 P6/P8 2건과 실제 보간 주석 음성은 맞는다. tagged template·escaped interpolation 누락과 inline/fenced code 오탐이 남는다. |
| A-P2-07 / P2 | FIXED | `--base=--name-only` 양 OS exit 2·traceback 없음. |
| A-P2-08 / P2 | FIXED | WSL tab 포함 tracked 파일의 신규 P6 1건 탐지·exit 1. Windows 금지 tab 파일명은 NOT_RUN. |
| A-P2-09 / P2 | FIXED | 기존 Infinity/NaN/음수/bool/중복 쌍·400자리 CSS 수치와 400/5000자리 대비 JSON 숫자 반례 모두 exit 2·traceback 없음. 깊은 JSON 구조의 별도 원인은 신규 A-P2-15로 구분했다. |
| A-P2-10 / P2 | FIXED | 원 잘못된 색·만료 baseline·missing CSS 파일명·var 참조·사설 주소 모양 경로·invalid read-surface marker가 해당 stderr/JSON/summary에 노출되지 않는다. |
| A-P2-11 / P2 | FIXED | `--read-surface muted`에서 31쌍을 검사하고 tertiary/muted 미달 1건·exit 1. |
| A-P3-12 / P3 | FIXED | geo 미달 8건과 evidence 8건이 일치하고 baseline 적용 시 exit 0. |
| A-P1-13 / P1 | FIXED | `++counter;` 다음 신규 P6은 이제 line 3·added=true·fail=true·exit 1. 양 OS 동일. |
| A-P2-14 / P2 | FIXED | self-symlink `--root`를 Windows와 WSL 모두 직접 생성·실행해 exit 2·traceback 없음으로 확인했다. WSL 합성 marker도 stderr에 없다. |

## A-P1-01 잔여 — media 조건 교집합과 전역 selector 누락

- 위치: `tools/kt_contrast.py:159`, `:254`, `:294`.
- 최소 재현 1: 다음 임시 override를 canonical 뒤에 주고 light 기본 모드로 실행한다.

```css
:root{--kt-brand:#fff;--kt-brand-foreground:#fff}
@media(prefers-color-scheme:dark){:root:not(.dark){--kt-brand:#000}}
```

- 명령: `python -B -X utf8 tools/kt_contrast.py packages/tokens/tokens.css <override.css> --fail-new --json`.
- 실제 Windows/WSL: **exit 0 / PASS / 27쌍 미달 0**. dark media는 light OS에서 비활성이므로 실제 root는 white/white, 1:1이다. Windows headless Chromium light에서 foreground/background가 모두 `rgb(255, 255, 255)`임을 직접 확인했다.
- 원인: `_selector_rules()`의 명시적 light/dark selector 분기가 `parent_mode`와 교집합을 취하지 않는다. 중첩 media 역시 이전 부모 조건을 새 media 값으로 덮는다. 반대로 dark media 안의 light selector·light media 안의 `.dark`·dark/light 모순 중첩 media는 비활성 white/white를 적용해 양 OS false FAIL도 만든다.
- 최소 재현 2: `:root.dark{--kt-brand:#fff;--kt-brand-foreground:#fff}`를 override로 주고 `--dark --fail-new --json`을 실행하면 양 OS **exit 0 / PASS**다. Chromium의 dark OS·`html.dark`에서 white/white를 관찰했다. 지원 목록에 없는 selector를 오류 없이 버리기 때문이다.
- 영향: 실제 대비 미달을 통과시키거나 비활성 규칙 때문에 정상 값을 차단한다. specificity 수정만으로 CSS 적용 범위 계약을 충족하지 못한다.
- 수정 수용: 부모 media와 selector 조건을 교집합으로 적용하고 모순 중첩은 적용하지 않거나 명시적 입력 오류로 닫는다. 전역 토큰을 가진 미지원 selector를 조용히 누락하지 않는다. 두 false PASS와 반대 false FAIL을 모두 회귀로 고정한다.

## A-P2-06 잔여 — MDX/JavaScript 인용 구분의 양방향 오류

- 위치: `tools/ux_lint.py:66`, `:80`, `:91`, `:183`.
- 공통 명령: 각 입력을 별도 임시 파일에 쓰고 `python -B -X utf8 tools/ux_lint.py <file> --fail-new --json`으로 실행한다.

```tsx
// runtime.mdx: 실행 tagged template의 outline-none이 누락된다.
export const X = () => <div className={String.raw`outline-none`} />;
// escaped.tsx: 역슬래시 때문에 ${...}는 실제 보간이 아닌 문자열이다.
const X = () => <div className={`\${/* outline-none */}`} />;
```

- 실제: 두 입력 모두 Windows/WSL **exit 0 / PASS / findings 0**. tagged template는 접두 문장 heuristic에서 문서 인용으로 오인한다. escaped interpolation는 실제 문자열의 `/* outline-none */`를 JS 주석으로 지운다. 브라우저 JavaScript에서 두 번째 결과를 element.className에 넣어 `classList.contains('outline-none') === true`를 직접 확인했다. `String.raw`의 결과도 `outline-none`이다.
- 반대 오탐 1: MDX 문서 한 줄 ``Example: `outline-none window.confirm()` `` → 양 OS **exit 1 / P6·P8 2건**. 문서의 colon 뒤 인용을 실행 코드로 취급한다.
- 반대 오탐 2: Python 문자열 `"```tsx\nconst x = `outline-none`;\nwindow.confirm('x');\n```\n"`로 fenced MDX 문서를 생성하면 양 OS **exit 1 / P8 1건**이다. 인용 전체가 실행되지 않는데 fence 내부의 backtick을 개별 종료점으로 사용한다.
- 정상 대조: `${/* window.confirm('x') */ value}`의 실제 보간 주석은 양 OS findings 0이고, 일반 MDX JSX template의 P6/P8은 2건을 탐지한다.
- 영향: 실행되는 금지 클래스가 gate를 우회하고 정상 문서 예제가 실패한다.
- 수정 수용: MDX inline/fenced 인용 경계를 우선 인식하고 실행 ESM/JSX에서는 tagged template와 escape·중첩 template·보간 주석을 구분한다. 단순 접두 문장과 첫 backtick 탐색만으로 정상/위반을 확정하지 않는다. 위 양성·음성 4종을 각각 회귀로 검증한다.

## A-P2-15 신규 — 깊은 JSON 배열의 RecursionError가 generic 입력 오류를 벗어남

- 위치: `tools/kt_contrast.py:491`, `tools/ux_lint.py:340`.
- 최소 재현: 임시 baseline에 `'[' * 2000 + '0' + ']' * 2000`을 UTF-8로 쓴다. `kt_contrast.py packages/tokens/tokens.css --baseline <file> --json`과 정상 TSX 대상의 `ux_lint.py <fixture.tsx> --baseline <file> --json`을 각각 실행한다.
- WSL Python 3.11.15 실제: 두 CLI 모두 **exit 1 / stderr에 Traceback / JSON payload 없음**. JSON 해독 중 `RecursionError`가 발생하지만 loader는 OSError·UnicodeError·ValueError 계열만 입력 오류로 처리한다.
- Windows Python 3.14.3 실제: 같은 두 입력은 **exit 2 / traceback 없음**이다. 이 플랫폼 결과를 3.11에서도 성공한 것으로 간주하지 않았다.
- 영향: 지원 최소 Python에서 구조상 잘못된 입력이 공개 CLI 오류 계약을 깨고 traceback을 노출한다. 5000자리 숫자만 회귀로 추가해 이 구조 경계를 확인하지 못했다.
- 수정 수용: JSON 구조 깊이 또는 RecursionError를 두 도구에서 일관된 generic exit 2로 처리한다. 3.11을 포함한 양 OS에서 traceback과 입력 marker가 없어야 한다. 심각도 P2, OPEN이다.

## 검증 명령과 결과

- Windows Python 3.14.3: `python -B -X utf8 -m unittest discover -s tests -p 'test_*.py'` → **268개 PASS / skip 0 / 82.199초**.
- WSL Python 3.11.15: `uv run --no-project --with jsonschema --python 3.11 python -B -X utf8 -m unittest discover -s tests -p 'test_*.py'` → **268개 발견 / 267개 PASS / Windows 전용 1개 skip / 49.203초**. skip은 성공으로 세지 않았다.
- 집중 시험: `python -B -X utf8 -m unittest tests.test_kt_contrast tests.test_ux_lint -v` → Windows **30개 PASS / 7.913초**. WSL uv Python 3.11의 동일 모듈 시험은 **30개 PASS / 3.929초**. 둘 다 skip 0.
- 양 OS 정적 gate: `tools/validate_document_links.py` → 문서 401·target 2412·오류 0; `tools/validate_plan.py` → task 106·오류 0; `tools/check_spdx.py` → 소스 56·오류 0; `tools/scan_secrets.py --all`·`tools/check_prod_redaction.py --all` → 각각 533개·발견 0; `tools/check_versions.py --self-check` → exit 0; `tools/check_aliases.py packages/tokens/aliases` → CSS 1개·오류 0; `git diff --check 94ca2f1730b270721eb6242bfcdd9362b51d45e5 HEAD` → exit 0.
- WSL 정적 gate에서만 process `GIT_DIR=/mnt/f/dev/kor-travel-common/.git/worktrees/review-t103-post3-a`, `GIT_WORK_TREE=/mnt/f/dev/kor-travel-common-wt/review-t103-post3-a`를 사용했다. 파일 설정은 변경하지 않았다. 합성 Git probe와 unittest에는 이 환경을 넘기지 않았다.
- 직접 CLI: canonical light/dark 각 27쌍 PASS; 추가 muted 읽기 31쌍 중 tertiary/muted 1건 미달·exit 1; docker-manager/concierge/geo/airport light 미달 4/8/8/4건 및 각 baseline 적용 exit 0. UX checked-in fixture는 기본 report 12건·fail 0·exit 0이다. 기본 report의 PASS를 위반 0으로 세지 않았다.
- 합성 corpus: Windows `python -B -X utf8 F:/dev/kor-travel-common/.git/codex-audit/t103-post3-reviewer-a-probe.py F:/dev/kor-travel-common-wt/review-t103-post3-a`; WSL은 `/mnt/f/...` 경로와 uv Python 3.11로 실행했다. helper SHA256 `E0A1AE67CE7310335E044C52A42AA9D35353E5AA7E022E307FFA054ACA5CEBAE`. 자신의 초기·post1 helper를 재생하고 새 반례를 더하며, 이전 raw report는 읽지 않는다. 합성 marker의 원문은 출력하지 않고 exit/boolean/건수만 출력한다.
- 브라우저: `node F:/dev/kor-travel-common/.git/codex-audit/t103-post3-reviewer-a-browser.cjs` → Windows bundled Playwright headless Chromium에서 media/selector 1:1 두 반례와 JavaScript 실제 클래스 값을 확인했다. 검증용 브라우저 의존성을 제품에 추가하지 않았다.
- 원격 읽기: `gh run list --commit 790bc3ec136b480c9cb95d796990ac1cbb07c596 --json databaseId,headSha,status,conclusion,url --limit 5` → exact SHA [run 34174744665](https://github.com/digitie/kor-travel-common/actions/runs/34174744665)는 completed/cancelled다. 다른 SHA의 CI 성공을 이 후보의 직접 성공으로 기록하지 않았다.

## 범위와 NOT_RUN

- post-fix-01 코드 후보부터 현재까지 두 도구·두 시험·airport task/evidence delta를 읽고 중단된 02 이후 변경도 직접 대조했다. 역사 원본·상대 report는 내용 미열람이다. 소비자 원천을 새로 읽거나 실행하지 않았다.
- NOT_RUN: Windows tab 파일명·WSL 브라우저·Windows Python 3.11 직접 실행·exact code SHA의 성공 CI·소비자 build/e2e·registry·배포·workflow dispatch·후행 T-010 workflow selftest. Windows Python 3.14와 WSL Python 3.11의 차이는 위 finding에서 따로 기록했다.
- 이 원본만 commit하며 제품 수정은 하지 않는다. 미해결 finding을 수정한 새 불변 후보에서 두 독립 재검토가 필요하다.
