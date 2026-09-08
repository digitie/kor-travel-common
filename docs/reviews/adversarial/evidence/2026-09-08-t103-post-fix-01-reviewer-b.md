# T-103 수정 후 독립 적대적 리뷰 B 원본 01

## 기준선·실행

- 실행 ID: `T103-POST1-B-20260908-092426-KST`; reviewer `/root/reviewer_b`; 최초 B 원본의 동일 ID·심각도를 유지한 full 재검토.
- 시작 KST: `2026-09-08T09:24:26.4695137+09:00`; 코드 검토 종료 KST: `2026-09-08T09:30:50.9029132+09:00`.
- manifest commit: `f5d523fed7f3e49a25664b0d5508b8546354912b`.
- manifest: `docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-01-manifest.md`; Git blob SHA256 `4147ccc726025f945ee11aaa2f56741e4ec550cccc1003fe59aeb7f7df85f5c8`.
- 실제 시작·종료 code SHA: `f9666078f49ea0745f485d6d0c88206048675aae`.
- 실제 시작·종료 tree: `6bcda765a470f0aed8a314512edefa7fae2fb0e9`.
- 비교한 최초 후보: `d12ccba48f67ad8ac863dbc97d85dda289c1e09c`; 전체 delta 11파일·869행 추가·116행 삭제. 독립성 지시에 따라 reviewer A 원본 내용은 제외했다. manifest·자기 원본·나머지 제품/시험/문서 delta를 확인했다.
- 격리: `F:/dev/kor-travel-common-wt/review-t103-post1-b`의 새 detached worktree. 시작·종료 `git status --short` 출력 없음. 이 시점까지 후보 제품 파일을 수정하지 않았다. 원본 기록만 `codex/review-t103-post1-b` branch에서 수행한다.
- source `.git/config` 시작·종료 SHA256 `0A0F849E7874CF0A25926856F9D2E381CCBF4C2DCB5999869C57B86E0F5BEB5B` 동일. `core.worktree` 또는 source 파일을 수정하지 않았다.
- 전체 시험·정적 gate는 후보를 복사한 별도 임시 Git 저장소에서 수행하고 자식 프로세스의 `GIT_*` 환경을 제거했다. 직접 반례는 임시 파일·Git 저장소만 만들었다. reviewer A의 원본·결과를 열람하거나 요청하지 않았다.

## 전달 요청 원문

> T-103 최초 B NO-GO finding을 수정했습니다. post-fix-01을 독립적으로 수행해 주세요. immutable code candidate는 `f9666078f49ea0745f485d6d0c88206048675aae` / tree `6bcda765a470f0aed8a314512edefa7fae2fb0e9`, manifest는 branch의 `docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-01-manifest.md`(manifest commit f5d523f)입니다. B 원본의 각 ID(B-P1-01..B-P3-07)가 실제로 FIXED인지와 신규 P0-P3를 Windows/WSL 경계에서 다시 공격하세요. reviewer A 결과를 읽지 말고, 제품 코드/소비자/registry/workflow dispatch를 수정·호출하지 마세요. raw report를 별도 `docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-01-reviewer-b.md`로 작성·commit하고 commit SHA·파일 SHA256·verdict를 알려 주세요.

manifest를 해당 commit의 Git object로 읽고 위 code 후보에만 판정을 귀속했다. 최초 B 원본의 SHA256은 `f9eeff355a684f7861043e5252195c52973c54567799a8df355a9f236322a053`이다.

## 판정·최초 finding disposition

**NO-GO**. 기존 7건 중 4건 FIXED, 3건 OPEN. 신규 발견 3건을 포함한 현재 OPEN은 P0 0건·P1 4건·P2 2건·P3 0건이다. 원 반례의 일부가 수정됐더라도 같은 계약의 잔여 재현이 있으면 finding 전체를 FIXED로 올리지 않았다.

| 원 ID | 원 심각도 | disposition | 직접 재현 결과 |
|---|---|---|---|
| B-P1-01 | P1 | FIXED | common CWD와 임시 앱 CWD에서 동일 `--root <app> --base HEAD`: 모두 finding 1·fail 1·exit 1. Git top-level이 대상 기준으로 일치 |
| B-P1-02 | P1 | FIXED | count 1의 기존 P6 앞에 새 P6 삽입: 새 행 `exempt=false, added=true, fail=true`, 기존 행 exempt, exit 1 |
| B-P1-03 | P1 | OPEN | 최초 TSX template·interpolation은 탐지됨. MDX 실행 template 누락과 interpolation 안 주석 오탐은 남음 |
| B-P1-04 | P1 | OPEN | 최초 잘못된 색 값/JSON basename 및 UX 파일명 출력은 비식별화됨. CSS 읽기 경로·미정의 var·argparse choice stderr는 노출 |
| B-P2-05 | P2 | FIXED | `--read-surface muted`로 31쌍 생성. 기존 1:1 반례가 text/muted FAIL·exit 1. 같은 표면 중복 인자도 31쌍 유지 |
| B-P2-06 | P2 | OPEN | count `1e309`·1.9·true와 version 999/NaN 조합은 exit 2. 5,000자리 JSON 정수는 두 도구 모두 traceback·exit 1 |
| B-P3-07 | P3 | FIXED | geo 미달 8건이 두 OS 실행·후보 evidence와 일치 |

기존 FIXED 4건은 Windows·WSL에서 각각 재현했다. 아래 신규 ID는 이번 리뷰에서 새로 발견한 문제를 뜻하며, 모두 이번 수정 commit에서 처음 도입됐다는 뜻은 아니다.

## 실제 실행과 결과

Windows Python `3.14.3`, WSL Python `3.14.4`. 이전 결과를 통과 근거로 재사용하지 않고 이번 후보에서 다시 실행했다.

```text
python -B -X utf8 -m unittest discover -s tests -p test_*.py
python -B -X utf8 -m unittest tests.test_kt_contrast tests.test_ux_lint -v
python -B -X utf8 tools/validate_document_links.py
python -B -X utf8 tools/validate_plan.py
python -B -X utf8 tools/check_spdx.py
python -B -X utf8 tools/scan_secrets.py --all
python -B -X utf8 tools/check_prod_redaction.py --all
python -B -X utf8 tools/check_versions.py --self-check
python -B -X utf8 tools/check_aliases.py packages/tokens/aliases
python -B -X utf8 -m unittest discover -s tests -p test_check_aliases.py
python -B -X utf8 tools/kt_contrast.py packages/tokens/tokens.css --json
python -B -X utf8 tools/ux_lint.py --root tests/fixtures/ux --json
git diff --check 94ca2f1730b270721eb6242bfcdd9362b51d45e5 f9666078f49ea0745f485d6d0c88206048675aae
```

| 검사 | Windows | WSL |
|---|---|---|
| 전체 unittest | 260개 통과·skip 0, 67.593초 | 259개 통과·skip 1, 총 260개, 22.959초 |
| T-103 focused | 22개 통과·skip 0, 4.376초 | 22개 통과·skip 0, 2.685초 |
| 문서 링크 | 397문서·2,411대상·오류 0 | 동일 |
| plan | 106 task·오류 0 | 동일 |
| SPDX | 56파일·오류 0 | 동일 |
| secret·운영값 각각 | 529파일·발견 0·예외 0 | 동일 |
| versions self-check | exit 0, 소비자 버전 검사는 아님 | 동일 |
| aliases | CSS 1개·오류 0 | 동일 |
| aliases focused | 35개 통과 | 34개 통과·Windows 전용 1개 skip |
| canonical light/dark 직접 CLI | 각 27/27·exit 0 | 동일 |
| UX manifest fixture report 직접 CLI | finding 12·exit 0 | 이 fixture CLI 명령은 NOT_RUN; focused 시험은 위 별도 결과 |
| diff check | exit 0 | 별도 명령 NOT_RUN; 동일 object diff에 Windows 실행 |

WSL 제외 시험은 `tests/test_check_aliases.py:228`의 Windows 8.3 API 전용 검사이며 통과 수에 포함하지 않았다. full suite는 별도 사본의 `review-t102-b-wsl-unittest.py`, gate는 `review-t102-post-b-gates.py` helper로 수행했다. helper 이름과 무관하게 인자는 이번 후보의 위 worktree였다.

직접 반례는 `.git/codex-audit/t103-post1-b-originals.py`, `t103-b-edge.py`, `t103-post1-b-new.py`, `t103-post1-b-media.py`를 이번 후보 경로로 양 OS에서 실행했다. 이 helper는 후보 제품/보고서 commit에 포함하지 않는다. 합성 marker는 `'gh' + 'p_' + 'Z' * 36`으로 만들고 캡처 출력의 포함 여부만 boolean으로 보고했다. 원문 값은 출력하지 않았다.

4앱 예제와 각 baseline의 `--fail-new --json`은 두 OS에서 모두 exit 0, light 미달은 docker-manager 4·concierge 8·geo 8·airport 4였다. 실제 소비자 저장소 실행의 증거가 아니다.

## OPEN B-P1-03 — MDX 실행 template와 interpolation 주석 경계

- 위치: `tools/ux_lint.py:64-130`, `:171`.
- 최초 TSX `className` template는 P2/P6로 exit 1, `${window.confirm(...)}`은 P8로 exit 1이 되어 수정됐다.
- 잔여 최소 반례: `Page.mdx`에 다음 한 줄을 쓰고 `ux_lint.py Page.mdx --fail-new --json`을 실행한다.

```tsx
export const Widget = () => <div className={`outline-none text-[13px]`}/>;
```

- 양 OS 결과: finding 0·`status=PASS`·exit 0. `.mdx` 확장자 전체에서 backtick을 인용으로 마스킹해 실제 JSX class 표현식까지 제외한다.
- 반대 방향 반례: TSX의 ``const text=`${1 /* window.confirm("not-executed") */}`;``는 실제 호출 없는 주석인데 P8 finding 1·exit 1이다. 일반 template를 quote 상태로 넘기는 동안 interpolation 코드의 주석을 구분하지 못한다.
- 영향: T-103 대상 확장자 MDX에서 실행되는 금지 패턴을 누락하고, TSX의 허용 주석은 실패시킨다. 정본의 문서 인용·주석 제외와 실행 패턴 탐지를 동시에 만족하지 못한다.
- 권고: MDX 문서 인용과 JSX/ESM 표현식, template text와 `${...}` 내부 코드의 상태를 분리한다. 무조건 확장자별 backtick 제외로 해결하지 않는다. 위 양성·음성을 모두 회귀에 추가한다.

## OPEN B-P1-04 — 잔여 stderr 비식별화

- 위치: `tools/kt_contrast.py:243-246`, `:360`, `:555-576`; 정상 argparse 오류 경로도 원문을 재출력한다.
- 원 반례 중 raw 색 값·JSON basename과 UX의 파일명 JSON/Markdown/step summary는 더 이상 marker를 노출하지 않는다.
- 잔여 최소 반례: (1) 존재하지 않는 `<marker>.css`를 입력, (2) override의 `--kt-brand: var(--kt-<marker>);`, (3) `--read-surface <marker>`를 각각 실행한다. `<marker>`는 위 분할식으로만 만든다.
- 양 OS 결과: 세 경우 모두 exit 2·traceback 없음이지만 `marker in stderr`가 `true`다. (1)은 `path.name`, (2)는 `reference`, (3)은 argparse invalid choice 진단이 원문을 복제한다.
- 영향: 입력 오류가 CI 로그로 재노출되는 기존 finding이 닫히지 않았다.
- 권고: CSS 읽기 오류·변수 식별자·인자 검증을 포함한 전체 오류 경로를 원문 없는 진단으로 수렴한다. argparse의 입력 문자열 echo도 포함하고 각 출력 채널 캡처 assertion을 유지한다.

## OPEN B-P2-06 — JSON 정수 길이 제한 예외 미처리

- 위치: `tools/ux_lint.py:269-273`, `tools/kt_contrast.py:431-435`.
- 기존 숫자 변환 반례는 수정됐지만 `json.loads` 단계의 일반 `ValueError`는 두 도구의 예외 목록에 없다.
- 최소 재현: 유효한 UX baseline의 `count` 또는 contrast baseline의 `measured`를 따옴표 없는 `'9' * 5000`자리 JSON 숫자로 만든다. 각 도구에 `--baseline <json> --json`으로 전달한다. Python 정수 문자열 제한 설정은 변경하지 않는다.
- 양 OS 결과: exit 1, stderr `Traceback` 및 정수 변환 길이 제한 `ValueError`. 정책 미달 exit 1과 입력 오류 exit 2 계약이 뒤섞인다.
- 영향: 비정상 숫자를 일반 입력 오류로 보고하지 못하며 traceback을 공개한다.
- 권고: JSON 파싱이 발생시키는 입력 예외도 한곳에서 처리하거나 제한된 숫자 hook으로 검증해 exit 2·generic·traceback 없음으로 처리한다. 정상 유한 숫자 입력을 보존한다.

## 신규 B-P1-08 — `+++`로 시작하는 추가 코드 행을 헤더로 오인

- 위치: `tools/ux_lint.py:253-265`, 특히 `:261`.
- 최소 재현: 새 임시 Git 저장소에 `App.tsx` 한 줄 `let counter=0;`을 commit한다. 다음 행을 추가한다.

```tsx
++counter; window.confirm("x");
```

```text
python <candidate>/tools/ux_lint.py --root <temporary-repo> --base HEAD --json
```

- 양 OS 결과: P8 finding 1, line 2, `added=false, exempt=false, fail=false`, `status=PASS`, exit 0. 동일 파일을 `--base` 대신 `--fail-new`로 검사하면 exit 1이다.
- 원인: Git patch에서 이 코드 행은 추가 표시 `+`와 코드의 `++`가 합쳐져 `+++counter...`가 된다. hunk 안에서도 `startswith("+++")`인 행을 파일 헤더로 제외하고 행 번호 증가도 누락한다.
- 영향: 유효한 JavaScript prefix increment로 시작하는 추가 행에서 UX gate를 우회하며 다음 추가 행의 번호까지 어긋날 수 있다.
- 권고: 파일 헤더를 hunk 진입 전에만 구분하고 hunk 내부의 추가 행은 첫 `+`만 제거한다. prefix increment·연속 추가 행·삭제/추가 혼합·EOF 반례를 넣는다.

## 신규 B-P1-09 — media 조건의 공백·부정·추가 조건을 잘못 판정

- 위치: `tools/kt_contrast.py:128-157`, `:193-205`.
- 최소 재현: canonical 뒤에 아래 override를 두고 각각 light 및 `--dark`의 `--fail-new --json`을 실행한다.

```css
@media not all and (prefers-color-scheme: dark) {
  :root { --kt-brand:#fff; --kt-brand-foreground:#fff; }
}
```

- 양 OS 결과: light는 canonical brand 대비 5.263·PASS·exit 0, dark는 1:1·FAIL·exit 1. 이 조건은 전체 dark query의 부정인데 구현은 문자열 안 `dark`만 보고 dark로 분류한다. 지원하지 않을 조건을 exit 2로 거절하지도 않는다.
- 같은 의미의 dark query `(prefers-color-scheme: dark)`와 `(prefers-color-scheme:dark)`도 비교했다. 앞 입력은 light에서 override를 제외하지만 뒤 입력은 light에도 적용되어 exit 1이다. 조건 허용 검사는 가변 공백 regex, 모드 선택은 고정 공백 문자열이라 판단이 다르다.
- `(prefers-color-scheme: dark) and (max-width: 1px)` 역시 추가 width 조건을 판정하거나 거절하지 않고 모든 dark에 적용한다.
- 영향: 선택한 모드에 실제 적용되는 미달을 통과시키거나 적용되지 않는 미달로 실패시킨다. CSS 파싱의 실패 차단 계약이 조건 조합에서 열려 있다.
- 권고: 지원하는 단순 media 문법을 정확히 파싱하고 공백을 정규화한다. 부정·복합 조건은 의미를 구현하거나 일관된 입력 오류로 거절한다. 문자열 일부가 알려진 조건이라는 이유로 전체 조건을 지원한다고 간주하지 않는다.

## 신규 B-P2-10 — airport 수용 기준과 수정된 계산 evidence 충돌

- 위치: `docs/tasks/T-103-kt-contrast-ux-lint.md:38` 대 `docs/evidence/t103-kt-contrast-ux-lint.md:13`, `packages/tokens/examples/airport.contrast-baseline.example.json`.
- task는 여전히 airport line 1.15의 재현을 수용 기준으로 요구한다. 이번 수정은 alpha 계산·example baseline·현재 evidence를 1.32로 바꿨다.
- 직접 명령: `python tools/kt_contrast.py packages/tokens/tokens.css packages/tokens/examples/airport-overrides.css --json`.
- Windows 실제 `control-line/surface-page`: `measured=1.3209340364487114`, `required=3`, `pass=false`. task의 1.15와 차이는 약 0.171로 ±0.05 재현 범위에도 들어가지 않는다.
- 영향: 올바른 계산 수정과 별개로, 현재 task의 완료 수용 기준을 충족했다고 기록할 수 없다. 조사 수치는 역사적 근거인데 현재 계산의 합격 조건으로 남아 있다.
- 권고: 역사 조사 값은 보존하고, 현재 계산의 검증 근거·변경 이유와 수용 기준을 동기화한다. 1.15를 되맞추기 위해 구현을 되돌리지 말고 과거 관찰과 현재 재현값을 구분한다.

## 범위·한계

- task 표·상세·resume의 T-103은 IN_PROGRESS다. T-010 후행 workflow를 이미 실행한 gate로 표시하지 않았다. 제품 파일은 수정하지 않았다. 소비자 저장소·registry·workflow dispatch는 호출하지 않았다.
- GPL-3.0-or-later 고지와 SPDX gate, stdlib 의존 경계는 이번 후보에서도 유지된다. 로컬 secret 검사는 입력 CLI의 모든 출력 비식별화를 증명하지 않는다.
- coordinator가 exact candidate CI 6개 성공을 알려 주었으나 독립 원격 조회는 `NOT_RUN`이다. 위 로컬 시험을 CI 성공으로 집계하지 않았다.
- `NOT_RUN(소비자 build/e2e·실제 baseline 등록·npm/PyPI registry 조회/게시·workflow dispatch)`: 요청상 금지 또는 소비자/후행 task 범위.
- `NOT_RUN(브라우저 rendering·screenshot 실측·재사용 workflow selftest)`: CLI와 고정 CSS/TSX/MDX 입력을 검사했다. media finding은 입력 언어 조건과 parser 결과를 직접 대조했으며 브라우저 실행을 주장하지 않는다.
- 원본과 신규 반례는 명시한 OS·후보에만 귀속한다. A 결과와 합쳐서 내린 결론이 아니다. 모든 OPEN finding의 수정 후 새 immutable 후보에서 재검토해야 한다.
