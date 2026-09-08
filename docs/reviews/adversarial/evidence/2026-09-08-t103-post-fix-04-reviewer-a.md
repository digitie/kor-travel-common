# T-103 수정 후 독립 적대적 리뷰 A 원본 04

- 실행 ID: `A-T103-POST4-20260908-100730`.
- 시작: 2026-09-08 10:07:30.270 KST. 코드 검증 종료: 2026-09-08 10:11:42.814 KST.
- manifest: commit `8152395679290359c8ca6af2c3bb47903f07b4db`의 `docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-04-manifest.md`를 `git show`로 읽었다.
- 불변 코드 후보: `1625bf197486448f7dc6b7780a6c4f4c13b01368`; tree `ee0626eb05e3e8dff3238f0de9ca71c3c2840563`. 대조 기준: `790bc3ec136b480c9cb95d796990ac1cbb07c596`.
- 격리: `F:/dev/kor-travel-common-wt/review-t103-post4-a` detached. 시작·코드 검증 종료의 `git rev-parse HEAD HEAD^{tree}`가 위 값과 같고 `git status --porcelain=v1`은 모두 빈 출력이다. 검증 후 이 원본 한 파일만 별도 commit한다.
- 전달 요청: CSS 조건 교집합·root.dark·specificity, 깊은 JSON/argparse redaction, MDX tagged/colon/backtick·tilde fence·escaped interpolation, diff·symlink·airport 기준을 양 OS에서 독립 공격하고 원본 commit/SHA256/verdict를 반환한다.
- 이전 post-fix raw와 상대 reviewer 결과는 읽거나 요청하지 않았다. 원 ID는 전달 이력에서 유지하고 자신의 후보 밖 합성 corpus를 새 SHA에서 실행했다. 제품·소비자 파일 및 source `.git/config`는 수정하지 않았다. 소비자·registry·workflow dispatch·배포는 호출하지 않았다.
- Windows `py -0p`에는 3.14/3.10만 있고 bundled Python은 3.12다. coordinator가 Windows 3.14/WSL 3.11 사용과 Windows 3.11 NOT_RUN 기록을 지시했다. 아래 실제 런타임을 구분했다.

## 판정과 disposition

**NO-GO**. 기존 15 ID 중 **FIXED 13 / OPEN 2**, 신규 ID는 없다. 미해결 심각도는 **P0 0 / P1 1 / P2 1 / P3 0**이다. 직전 최소 반례 자체는 수정됐지만 같은 파서 계약의 다른 표기가 여전히 누락·오탐을 만든다.

| ID·원 심각도 | disposition | 직접 확인 |
|---|---|---|
| A-P1-01 / P1 | OPEN, 일부 수정 | 기존 specificity·media 교집합·모순 중첩·`:root.dark`·문자열/주석 반례는 수정. 동치 selector 표기를 조용히 누락하는 잔여가 있다. |
| A-P1-02 / P1 | FIXED | OKLCH chroma 25%와 0.1의 세 채널이 양 OS에서 동일. 수학 회귀 통과. |
| A-P1-03 / P1 | FIXED | white 20%/black이 1.6620953314177012로 `#333` 대조와 동일. airport 1.32 현재 계약·1.15 역사 값 구분 보존. |
| A-P1-04 / P1 | FIXED | 앞 삽입한 신규 P6만 added=true·exempt=false·fail=true, 기존 행만 면제. 양 OS exit 1. |
| A-P1-05 / P1 | FIXED | 외부 root 동명 파일이 충돌하지 않고 실제 위반 1건·exit 1. 외부 Git root 회귀 통과. |
| A-P2-06 / P2 | OPEN, 일부 수정 | String.raw·colon·3자 backtick/tilde fence·escaped interpolation 반례는 수정. 일반 tag·computed tag·4자 fence·blockquote 인용 경계가 남는다. |
| A-P2-07 / P2 | FIXED | `--base=--name-only` 양 OS generic exit 2. |
| A-P2-08 / P2 | FIXED | WSL tab 파일의 신규 P6은 exit 1. Windows 금지 tab 파일명은 NOT_RUN. |
| A-P2-09 / P2 | FIXED | Infinity/NaN/음수/bool/중복 및 400/5000자리 JSON 숫자 경계는 exit 2·traceback 없음. |
| A-P2-10 / P2 | FIXED | 기존 색/var/파일명/주소/만료 baseline marker 비공개 유지. 두 CLI `--json=<marker>`도 generic exit 2·marker 없음. |
| A-P2-11 / P2 | FIXED | 추가 muted 읽기 31쌍에서 tertiary/muted 미달 1건·exit 1. |
| A-P3-12 / P3 | FIXED | geo light 미달 8건·baseline 적용 exit 0과 evidence 일치. |
| A-P1-13 / P1 | FIXED | `++counter;` 뒤 신규 P6은 line 3·added=true·fail=true·exit 1. |
| A-P2-14 / P2 | FIXED | Windows/WSL self-symlink root를 직접 생성해 generic exit 2·traceback 없음. |
| A-P2-15 / P2 | FIXED | 2000중첩 JSON 배열을 두 CLI에 전달해 Windows 3.14/WSL 3.11 모두 generic exit 2·traceback 없음. |

## A-P1-01 잔여 — 동치 selector를 조용히 버려 실제 1:1을 PASS

- 위치: `tools/kt_contrast.py:166`의 `_selector_rules()` whitelist와 미지원 selector 반환 경계.
- 최소 재현: 다음 두 줄은 서로 독립된 임시 override다. 첫째는 `--dark`, 둘째는 기본 light로 검사한다.

```css
.dark:root{--kt-brand:#fff;--kt-brand-foreground:#fff}
[data-theme='light']{--kt-brand:#fff;--kt-brand-foreground:#fff}
```

- 명령: `python -B -X utf8 tools/kt_contrast.py packages/tokens/tokens.css <override.css> --fail-new --json [--dark]`.
- 실제: 둘 다 Windows/WSL **exit 0 / PASS / 27쌍 미달 0**. Windows Chromium에서 첫째는 `html.dark`, 둘째는 `html[data-theme="light"]`를 주고 body에 두 var를 적용해 foreground/background 모두 `rgb(255, 255, 255)`임을 관찰했다. 실제 대비는 1:1이다.
- 원인: 지원하는 `:root.dark`와 `.dark:root`의 순서 차이, 지원하는 double-quoted light attribute와 single-quoted 표기를 다른 계약으로 취급한다. 미지원 selector가 선언을 포함해도 오류 없이 버려 canonical 값만 계산한다.
- 영향: 지원 기능과 의미가 같은 앱 CSS를 정상으로 잘못 승인한다. root.dark 문자열 하나를 추가하는 방식으로는 기존 scope finding의 수정 수용 조건을 충족하지 못한다.
- 수정 수용: 지원 subset의 selector를 구성요소 단위로 정규화하거나, 전역 토큰을 정의할 수 있는 미지원 표기를 명시적 exit 2로 닫는다. 미지원 입력을 자동 PASS로 만들지 않는다. 두 동치 표기는 실제 미달·exit 1 또는 명시적 입력 오류가 돼야 한다.

## A-P2-06 잔여 — 일반 tagged template 누락과 fence/blockquote 오탐

- 위치: `tools/ux_lint.py:87`의 실행 template 판정과 `:109`의 fence 종료 판정.
- 최소 양성 반례: 별도 `.mdx` 파일에 다음 코드를 저장한다.

```tsx
export const classes = parts => parts[0];
export const X = () => <div className={classes`outline-none`} />;
```

- 두 번째 양성은 `export const X = () => <div className={String['raw']` + backtick + `outline-none` + backtick + `} />;`이다. helper가 실제 backtick 문자열을 작성한다.
- 명령: `python -B -X utf8 tools/ux_lint.py <fixture.mdx> --fail-new --json`.
- 실제: 두 파일 모두 Windows/WSL **exit 0 / PASS / findings 0**. 브라우저 JavaScript에서 두 tag의 반환값이 `outline-none`임을 직접 관찰했다. whitelist가 `String.raw`라는 한 표기만 실행으로 인식하고 같은 computed 접근이나 사용자 정의 tag를 문서 인용으로 지운다.
- 음성 반례 1: `chr(96)*4 + 'tsx\n' + chr(96)*3 + '\nwindow.confirm("x");\n' + chr(96)*4 + '\n'`로 4자 fence 문서를 생성한다. 내부의 3자 backtick 행은 4자 fence를 닫지 못하므로 전체는 인용이다. 도구는 양 OS **exit 1 / P8 1건**으로 오탐한다. opener 길이를 보존하지 않고 어떤 3자 marker도 닫힘으로 처리한다.
- 음성 반례 2: `'> ' + chr(96) + 'outline-none window.confirm()' + chr(96)`로 blockquote 속 inline code를 생성하면 양 OS **exit 1 / P6·P8 2건**이다. `>` 접두 문장을 실행으로 인식한다.
- 정상 대조: colon 뒤 inline code, 3자 backtick·tilde fence는 0건; `String.raw` tag 및 escaped interpolation의 실제 outline-none은 1건을 탐지한다. 실제 보간 주석은 0건이다.
- 영향: 실행되는 금지 클래스가 gate를 우회하고 정상 MDX 문서가 gate에서 차단된다.
- 수정 수용: MDX의 인용/ESM/JSX 문맥과 fence marker 종류·길이를 구분한다. 실행 문맥의 tag 식을 특정 함수 이름에 한정하지 않는다. 지원하지 않는 문법을 확정 정상으로 처리하지 않고 제한을 문서화하거나 입력 오류로 닫는다. 위 양성 2종·음성 2종을 각각 회귀로 고정한다.

## 실행한 검증

- Windows Python 3.14.3 전체: `python -B -X utf8 -m unittest discover -s tests -p 'test_*.py'` → **275 PASS, skip 0, 71.029초**.
- WSL Python 3.11.15 전체: `uv run --no-project --with jsonschema --python 3.11 python -B -X utf8 -m unittest discover -s tests -p 'test_*.py'` → **275개 발견, 274 PASS, Windows 전용 1 skip, 42.259초**. skip을 성공으로 세지 않았다.
- 집중: `python -B -X utf8 -m unittest tests.test_kt_contrast tests.test_ux_lint -v` → Windows **37 PASS / 10.197초**; WSL uv Python 3.11 동일 모듈 시험 **37 PASS / 6.054초**, skip 0.
- 양 OS 정적 gate: `tools/validate_document_links.py` 문서 404·target 2412·오류 0; `tools/validate_plan.py` task 106·오류 0; `tools/check_spdx.py` 소스 56·오류 0; `tools/scan_secrets.py --all`·`tools/check_prod_redaction.py --all` 각각 536개·발견 0; `tools/check_versions.py --self-check` exit 0; `tools/check_aliases.py packages/tokens/aliases` CSS 1개·오류 0; `git diff --check 94ca2f1730b270721eb6242bfcdd9362b51d45e5 HEAD` exit 0.
- WSL 정적 gate는 process `GIT_DIR=/mnt/f/dev/kor-travel-common/.git/worktrees/review-t103-post4-a`, `GIT_WORK_TREE=/mnt/f/dev/kor-travel-common-wt/review-t103-post4-a`를 사용했다. source 설정 파일은 변경하지 않았고 합성 Git probe·unittest에 이 환경을 넘기지 않았다.
- 직접 CLI: canonical light/dark 각 27쌍 PASS; 추가 muted 31쌍 중 1건 미달·exit 1; 4앱 light 미달 4/8/8/4건·각 baseline `--fail-new` exit 0. UX checked-in fixture 기본 report는 12건·fail 0·exit 0이며 위반 0으로 세지 않았다. airport task/evidence는 직전 후보와 동일하고 1.32 현재 기준/1.15 역사 구분을 유지한다.
- 합성 probe: Windows `python -B -X utf8 F:/dev/kor-travel-common/.git/codex-audit/t103-post4-reviewer-a-probe.py F:/dev/kor-travel-common-wt/review-t103-post4-a`; WSL은 `/mnt/f/...`와 uv Python 3.11로 실행했다. SHA256 `9CE3E1E70CD39DA205E745FFA357AF4DEDE839D64EBEADE3667DCDE6D2933DA6`. 자신의 초기/post1/post3 helper를 이어 재생하되 raw 보고서는 읽지 않는다. 합성 marker는 원문 대신 포함 여부 boolean만 출력했다.
- 브라우저: `node F:/dev/kor-travel-common/.git/codex-audit/t103-post4-reviewer-a-browser.cjs`, SHA256 `562C8C788B70B4C1BC3D35D62BFC277A9642E2E5719AF2C92AED90C9E7BC787E`. Windows bundled Playwright headless Chromium에서 CSS 1:1 두 사례와 tag 반환값을 직접 확인했다. 제품 의존성은 변경하지 않았다.
- 원격 읽기: `gh run list --commit 1625bf197486448f7dc6b7780a6c4f4c13b01368 --json databaseId,headSha,status,conclusion,url --limit 5` → exact SHA [run 34175519082](https://github.com/digitie/kor-travel-common/actions/runs/34175519082)는 completed/cancelled였다. 다른 SHA의 CI 성공을 가져오지 않았다.

## 범위와 한계

- 직전 코드 후보와 현재의 두 도구·두 시험 전체 delta를 읽었다. 기존 task/evidence의 동일성과 현재 수용 기준도 대조했다. 역사 raw 및 상대 report는 내용 미열람이다.
- NOT_RUN: Windows Python 3.11 직접 실행(미설치, coordinator 확인), Windows tab 파일명, WSL 브라우저, exact code SHA의 성공 CI, 소비자 build/e2e·registry·배포·workflow dispatch·후행 T-010 workflow selftest.
- 보고서 한 파일만 commit한다. 미해결 두 finding의 수정과 새 불변 후보 재검토 전에는 완료를 승인할 수 없다.
