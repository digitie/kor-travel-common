# T-102 초기 독립 적대적 리뷰 A 원본

- 실행 ID: A-T102-INITIAL-20260907-231212
- 최종 verdict: BLOCK.
- findings: A-T102-P1-01(OPEN), A-T102-P2-02~05(OPEN). P0 0건·P1 1건·P2 4건·P3 0건.
- candidate: 8bc8179f728de88fd9327f9d4e8159188a95f9c3
- tree: 8e7a66aeb2875b74cec2a98afc4b7fdeb1edcf97
- base: 843c404d79fd748cf6f8e40ce3e385fcabb0179f
- branch의 검토 식별자: codex/t102-aliases. 실제 검토는 F:/dev/kor-travel-common-wt/review-t102-a detached worktree.
- 시작: 2026-09-07 23:12:12.046 KST. 종료: 2026-09-07 23:18:04.166 KST.
- 시작·종료 SHA/tree는 위 값과 일치, git status --porcelain=v1은 모두 빈 출력이었다.
- 후보 파일·source .git/config·소비자 저장소를 수정하지 않았으며 commit/push/publish하지 않았다. 시험 변조는 후보 밖의 임시 사본에만 했다.
- reviewer B의 이번 결과를 열람하거나 요청하지 않고 원본을 독립 확정했다.

## 요청과 검토 범위

전달 요청: immutable 후보의 소비자 계약·CSS/토큰 계층·Tailwind exact namespace·shadcn import/중복·dark 상속·weather 어휘 재현·패키지 export를 공격한다. shadcn.css import가 제공하는 실제 CSS 이름, shadow-card/font aliases/navy·17rem·dark 값, .dark drift, package import resolution, examples 미포장을 확인한다. T-102·TK-16·package contract를 기준으로 P0–P3 finding과 verdict를 원본에 남긴다.

전체 8파일 delta(+505줄)를 읽고 T-102 상세 task, TK-3/TK-6/TK-16, architecture packages/style-delivery와 대조했다. 고정 weather 원천은 소비자 저장소의 실제 Git object 6003da995fa4b35799f9dadc406c6ba2878bfbae에서 app/tokens.css를 읽었다. 위치는 packages/kor-travel-weather-admin/frontend/app/tokens.css이며 현재 checkout 값이나 작성자 설명을 대체 근거로 삼지 않았다.

## Findings

### A-T102-P1-01 — 고정 weather 어휘 8개가 빠져 기존 spacing 호출이 무효화된다

- 심각도: P1. Disposition: OPEN / 수정 필요.
- 후보 위치: packages/tokens/aliases/map-vocabulary.css:43, tests/test_check_aliases.py:49.
- 근거: T-102 수용 기준은 고정 weather tokens.css의 변수 이름 집합을 포함하고 누락 0을 요구한다. 실제 CSS import를 모두 적용해도 --space-3xs, --space-2xs, --space-xs, --space-sm, --space-md, --space-lg, --space-xl, --space-2xl이 없다. shadcn.css에도 이 이름은 없다.
- 재현: 보존 browser probe에서 원천 weather.css와 설치된 tokens.css + aliases/map-vocabulary.css + 예제를 각각 link로 읽고 root custom property를 비교한다. light/dark 모두 missing 8개. padding:var(--space-md) 표본의 계산값은 원천 16px → 후보 0px이다.
- 영향: 호출부를 유지한 교체에서 여백·gap 계열 선언이 무효화된다. 테스트의 수기 부분 목록에는 이 이름이 없어 9개 시험과 checker가 통과한다.
- 권고: 고정 원천에서 이름 전체를 추출한 회귀를 추가하고 누락을 닫아야 한다. common 승격 근거 없이 weather 단독 값을 토큰 정본에 추가하지 말고, 공유 어휘/앱 소유 호환 값의 전달 위치를 확정해 수용 기준과 함께 정합화한다. 현 상태를 누락 0 또는 값 무변경 교체 가능으로 기록하면 안 된다.

### A-T102-P2-02 — weather 예제가 실제 font·radius·light/dark 값을 보존하지 않는다

- 심각도: P2. Disposition: OPEN / 수정 또는 명시적 계약 disposition 필요.
- 후보 위치: packages/tokens/examples/weather-overrides.css:7, :16; aliases/map-vocabulary.css:48, :80, :131, :161.
- 근거: T-102 목표는 기존 호출을 유지한 값 무변경 교체이고, 예제 설명은 weather의 현재 폰트와 navy 값을 재현한다고 한다. brand 4종·17rem·sans 스택은 일치하지만 mono 스택을 덮어쓰지 않으며 radius-md를 weather의 panel(0.5rem) 대신 control(0.375rem)에 연결한다. surface/ink/focus 등도 고정 weather 값과 다르다.
- 재현: 같은 browser probe의 link 3개 조합에서 font-mono는 기존 Geist Mono/ui-monospace/SFMono-Regular/.../Liberation Mono → common ui-monospace/SF Mono/...로 달라지고, radius-md는 8px → 6px이다. card light는 oklch(0.992 0.002 250) → oklch(0.992 0.002 140), dark는 oklch(0.23 0.028 255) → oklch(0.23 0.007 145)다. ease-in도 마지막 제어점 1 → 0, dark shadow 색/alpha도 바뀐다.
- 영향: spacing을 복구해도 예제 3파일만으로 기존 weather 시각/모션 계약이 재현되지 않는다. 실제 소비자 전체 e2e를 실행한 주장은 아니며, 후보가 제공하는 CSS 값의 직접적인 불일치다.
- 권고: 고정 원천과 light/dark 변수별 대조표를 전수 생성하고, weather 소유 차이(특히 mono 스택·radius-md·paper/ink/focus)를 합법적인 앱 오버라이드/호환 계층으로 보존한다. 공통 의미로 의도적으로 변경하는 항목은 값 무변경 목표의 예외·이관 계약으로 명시하고 승인된 task disposition을 남겨야 한다. 일부 brand 문자열 존재 검사를 전체 재현 증거로 사용하지 않는다.

### A-T102-P2-03 — .dark 선언을 전부 지워도 checker가 통과한다

- 심각도: P2. Disposition: OPEN / 수정 필요.
- 후보 위치: tools/check_aliases.py:156.
- 재현: 후보 패키지 임시 사본의 aliases/map-vocabulary.css를 .dark 블록 직전까지 자른 뒤 checker CLI 실행. Windows/WSL 모두 exit 0, CSS 1개·오류 0개. 반대로 .dark brand만 var(--kt-info)로 바꾸면 exit 1이므로 값 집합 비교는 작동하나 모드의 이름 집합은 검사하지 않는다.
- 실제 영향 재현: root 아래 .dark 요소의 --kt-brand는 oklch(76% 0.085 169)인데 누락 alias의 --brand는 root light의 oklch(51.4% 0.081 169)를 상속한다. 온전한 후보에서는 둘 다 dark 76%다.
- 권고: :root와 .dark를 구분해 각 블록의 별칭 이름 집합과 대응 값을 확인한다. 누락·추가·상이한 mode 선언을 각각 실패 fixture로 고정한다. selector를 구분하지 않는 전역 by_name 집합만으로 dark 계약을 보증하지 않는다.

### A-T102-P2-04 — 유효한 url() import 형식이 조용히 검사 범위에서 빠진다

- 심각도: P2. Disposition: OPEN / 수정 필요.
- 후보 위치: tools/check_aliases.py:16, :44.
- 재현: 정상 @import "../shadcn.css"를 @import url("../absent.css");로 치환한다. CSS의 합법적인 import 문법이지만 IMPORT 정규식은 이 행을 인식하지 않으며 Windows/WSL CLI가 모두 exit 0이다.
- 영향: 빠진 import의 shadcn 이름 제공이 없어지고, 파일 누락·package 밖 경로·순환·전이 정의 검사가 모두 우회된다. 실제 checked-in import는 정상이며 이 finding은 지원 경계의 실패 시나리오다.
- 권고: 지원하는 CSS import 문법을 파싱하고 인식하지 못한 @import가 있으면 오류로 중단한다. url()·인용 문자열·주석/공백·허용하지 않는 modifier의 경계를 시험한다. 미해석 import를 성공으로 건너뛰지 않는다.

### A-T102-P2-05 — 전이 import의 금지 정의가 검사를 우회한다

- 심각도: P2. Disposition: OPEN / 수정 필요.
- 후보 위치: tools/check_aliases.py:105, :119, :131, :165.
- 재현: 임시 패키지 루트 extra.css에 :root { --kt-brand: red; }를 쓰고 alias 선두에 @import "../extra.css";를 추가한다. Windows/WSL checker는 모두 exit 0이다.
- 원인: imported_defs를 모으지만 금지 --kt-* 정의·theme/shadcn 충돌 검사는 alias_defs에만 적용하며 all_defs는 마지막에 사용하지 않는다. import 예외가 공인 shadcn 파일에만 한정되지 않는다.
- 영향: 선택 shim을 읽는 것만으로 정본 semantic을 덮어쓰는 CSS가 전달돼도 checker의 merge/rc gate는 정상으로 표시된다.
- 권고: 허용된 정본 shadcn import와 기타 import를 명시적으로 구분하거나 전이 closure 전체에 alias 계약을 적용한다. 임의 helper CSS를 통해 --kt-* 재정의·충돌을 우회하는 negative fixture를 추가한다.

## 직접 통과를 확인한 부분

- shadcn import는 실제 설치 CSS에서 정상 작동한다. CSS 파일을 문자열로 합쳐 이름을 세는 대신 browser link와 상대 @import를 사용해 --card/--border/--destructive/--input/--primary의 계산값을 확인했다. 직접 중복 정의 없이 shadcn 소유 이름이 제공된다.
- navy brand 4종 light/dark·17rem rail·sans/display/body/heading 스택·shadow-card/shadow-card-hover none은 weather 기준과 일치한다. 실제 로딩한 폰트 파일까지 검증한 것은 아니다.
- 원본 .dark 블록은 같은 별칭을 재선언해 nested dark 상속을 정상 전달한다. 위 A-P2-03은 그 블록이 삭제돼도 gate가 실패하지 않는 회귀 취약점이다.
- common theme.css가 실제 선언한 --color-kt-brand를 alias에 추가하면 두 OS에서 exit 1이다. 미정의 참조·직접 --kt-* 정의·직접 shadcn 중복·패키지 밖 인용 import의 기존 9개 시험도 통과했다.
- Tailwind 4.3.3에서 설치 패키지의 @import "@kor-travel/tokens/aliases/map-vocabulary.css"가 해결되고 bg-kt-brand가 생성된다.
- Tailwind 기본 rounded-sm은 shim 없이 4px, shim과 함께 6px인 것도 관찰했다. T-102의 명시적 namespace 수용 기준은 common theme.css의 exact 이름이고 기존 weather도 radius-sm=6px를 소유하므로, 이 opt-in legacy 의미의 영향 자체를 별도 신규 finding으로 집계하지 않았다. 이를 모든 Tailwind 기본 utility가 불변이라는 증거로 해석하면 안 된다.
- npm tarball 19파일에 aliases/map-vocabulary.css가 있고 examples/는 없다. 두 OS 설치 후 공개 alias export require.resolve가 성공했다.

## 실행 명령·결과

기본 실행 위치는 detached 후보이다. Windows Python 3.14.3 / Node v25.9.0 / npm 11.12.1, WSL uv Python 3.11.15 / Node v22.22.2 / npm 11.19.1을 사용했다. Windows npm ci의 ^22.12.0 engine 경고는 버전 일치 성공으로 세지 않았다.

    python -B -X utf8 -m unittest discover -s tests -q
    python -B -X utf8 -m unittest discover -s tests -p test_check_aliases.py -q
    python -B -X utf8 tools/check_aliases.py packages/tokens/aliases
    python -B -X utf8 F:/dev/kor-travel-common/.git/codex-audit/t102-a-package.py
    python -B -X utf8 F:/dev/kor-travel-common/.git/codex-audit/t102-a-negative.py

WSL에서는 /mnt/f/dev/kor-travel-common-wt/review-t102-a로 이동해 uv run --no-project --python 3.11 python -B -X utf8로 같은 명령/helper의 /mnt/f 경로를 실행했다. 전체 unittest에는 --with jsonschema==4.26.0을 추가했다.

| 검증 | Windows | WSL |
|---|---|---|
| 전체 Python 회귀 | 212 tests / 64.144초 / OK / skip 0 | 212 tests / 42.987초 / OK / skip 0 |
| focused aliases | 9 tests / 0.256초 / OK | 9 tests / 0.234초 / OK |
| checker 원본 | exit 0 | exit 0 |
| npm ci/check/build/check/test | 모두 0, package tests 7 / skip 0 | 동일 |
| pack / 임시 install / alias resolve | 성공 | 성공 |
| plan | 106 task / 오류 0 | 동일 |
| 문서 링크 | 366문서 / 2331대상 / 오류 0 | 동일 |
| SPDX | 45파일 / 오류 0 | 동일 |

Windows에서 scan_secrets --all / check_prod_redaction --all은 각각 481파일·발견 0·예외 0, check_versions --self-check 및 base..HEAD git diff --check는 exit 0이었다. 이 성공들은 위 CSS 의미·검사기 우회 반례를 배제하지 못한다.

브라우저 원본 fixture와 결과는 F:/dev/kor-travel-common/.git/codex-audit/t101-css-a/t102에 보존했다.

    cd F:/dev/kor-travel-common/.git/codex-audit/t101-css-a/t102
    node probe.mjs

probe.mjs, probe-output.txt, weather.css(고정 Git object 사본), npm tarball 설치본, weather-overrides.css 후보 사본, light/dark/nested HTML, compiled.css가 있다. 실제 consumer 저장소에서는 git show/read만 수행했다.

## 원격 CI와 한계

[draft PR #14](https://github.com/digitie/kor-travel-common/pull/14)의 headRefOid가 정확한 후보 SHA임을 확인했고 [CI run 34131587507](https://github.com/digitie/kor-travel-common/actions/runs/34131587507)의 docs·tools Ubuntu·tools Windows·secret-scan·check-versions·packages 6개 SUCCESS를 직접 관찰했다. green CI를 의미 계약의 성공으로 대신하지 않았다.

- NOT_RUN: 실제 weather 애플리케이션 build/e2e 및 320·375·414·768·1024·1280px 전체 화면 diff(T-461). 이번 검증은 고정 원천 CSS와 설치 패키지로 만든 작은 browser fixture이며 소비자 시각 검증 완료가 아니다.
- NOT_RUN: 폰트 파일 로딩·실제 glyph 레이아웃 비교, WSL 브라우저 실행, 로컬 exact Node 22.23.1. Windows browser와 양 OS 도구/package 실행을 구분했다.
- NOT_RUN: 공개 registry 게시·release/tag 생성·소비자 채택·소비자 파일 변경. 요청 밖이다.
- NOT_RUN: WSL secret/redaction 전체 트리 재실행 및 release/main push CI 관찰. 수행한 gate만 위 표에 집계했다.

필수 이름 포함과 값 재현 계약, 검사기의 정상 표시 우회를 해결하기 전에는 T-102 완료/rc 가능으로 표시하지 않아야 한다. 원본 판정은 BLOCK이다.

