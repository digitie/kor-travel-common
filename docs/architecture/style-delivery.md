# 스타일 배포 계약(Tailwind v4 CSS-first)

- 정본 지위: `@kor-travel/tokens`·`@kor-travel/ui`의 CSS 파일 구성과 소비자 연결 방식의 정본(초안). 값 정본은 `packages/tokens/tokens.css`. 확정 task: T-008(설계 초기판) → T-101·T-102·T-103·T-104. 마지막 갱신: 2026-09-06.
- 근거: [브리프](../plan/design-brief.md) D-10·D-12·D-13, `docs/survey/cross/design-tokens.md` §3.2.3·§3.4.1·§3.4.2·§3.6.1~§3.6.6, `docs/survey/cross/ui-components.md` §6.3, `docs/survey/inventory/pinvi.md` §3.1(`[data-pv-surface]`), `docs/survey/inventory/kor-travel-weather.md` §3.1·§9.1.

이 문서는 [아키텍처 개요](README.md) §3의 tokens·ui 책임 중 "CSS가 소비자에게 어떻게 도달하는가"만 다룬다. 토큰 이름·역할·오버라이드 규칙의 정본은 [design-tokens](../standards/design-tokens.md), UX 금지 패턴은 [ux-guide](../standards/ux-guide.md), 이관 절차는 [consumer adoption runbook](../runbooks/consumer-adoption.md)이다.

## 1. 파일 구성

| 파일 | 내용 | Tailwind | 소비자 | 근거 |
|---|---|---|---|---|
| `tokens.css` | `:root { --kt-*: <map 기본값> }` + `.dark { --kt-* }`. 순수 CSS, 값 정본 | 무관 | 전 앱(Tailwind 없는 weather·airport main 포함) | `dt` §3.6.3 |
| `theme.css` | `@import "./tokens.css"`; `@theme inline { --color-kt-*, --spacing-kt-*, --radius-kt-*, --font-kt-*, --shadow-kt-*, --ease-kt-* }`; `@theme { --text-kt-* }`; `@utility duration-kt-fast/base` | v4 필수 | Tailwind v4 앱 + ui 소비 앱(필수) | `dt` §3.6.3·§3.6.5, D-10 |
| `shadcn.css` | `:root/.dark { --background: var(--kt-surface-page); … --input: var(--kt-control-line); --accent: var(--kt-brand-tint); --radius: var(--kt-radius-control); --border: var(--kt-border) }` | 무관 | shadcn 사용 앱(map·geo·concierge·pinvi admin·airport WIP) | `dt` §3.2.3 |
| `base.css` | `@layer base :focus-visible { outline: 2px solid var(--kt-focus); outline-offset: 2px }` 단일 발행, hairline 2종(장식 `--kt-border`·3:1 `--kt-control-line`), reduced-motion 전역(스피너 예외), `button:not(:disabled){cursor:pointer}`, `color-scheme: light` 기본 | 무관 | 선택(전 admin 권장) | `dt` §3.4.1, `ux` G9 |
| `base.scoped.css` | `base.css`를 `[data-kt-surface]` 하위로 한정. 사용자 표면과 admin이 한 앱에 공존하는 pinvi용 | 무관 | 선택(pinvi admin) | D-10, `inv/pinvi` §3.1 |
| `dark-class.css` | `@custom-variant dark (&:is(.dark *))` | v4 | 다크 class 활성 앱(map·geo·concierge 계열) | `dt` §3.6.6 |
| `dark-media.css` | `@media (prefers-color-scheme: dark)` 래퍼로 `.dark` 값 적용 | v4 | 다크 media 활성 앱(airport) | `dt` §3.6.6 |
| `aliases/map-vocabulary.css` | map·weather·geo 공통 레거시 이름(`--surface-page`·`--brand`·`--rail`…) → `var(--kt-*)` shim. 앱 고유 접두(`--ktc-*`·`--color-admin-*`·`--ui-*`)는 앱 파일 | 무관 | 선택(weather 1차, map·geo 이행기) | D-12, `inv/kor-travel-weather` §3.1(map 어휘 294회) |
| `tokens.json`·`tokens.ts`·`tailwind-preset.cjs` | 정본 CSS에서 생성. DTCG·TS 상수·v3/NativeWind preset | v3(preset) | pinvi mobile(O-8 승인 후)·`@pinvi/design-tokens` 재수출·문서 | `dt` §3.6.3 |

정본은 `tokens.css` 하나이며 나머지 생성물은 빌드 diff 검사로 동기화를 강제한다(A6.1 대응). 폰트 파일은 배포하지 않는다(스택 문자열만; 로딩은 앱 책임).

## 2. 소비자 연결(필수 2줄)

Tailwind v4 앱의 `globals.css` 최소 형태(경로는 CSS 파일 기준 상대 경로; 모노레포 상대 경로 표는 [consumer adoption runbook](../runbooks/consumer-adoption.md)):

```css
@import "tailwindcss";
@import "@kor-travel/tokens/theme.css";        /* 필수 1: tokens.css 포함, kt- 유틸리티 정의 */
@import "@kor-travel/tokens/shadcn.css";       /* 선택: shadcn alias */
@import "@kor-travel/tokens/base.css";         /* 선택: focus·hairline·reduced-motion */
@import "@kor-travel/tokens/dark-class.css";   /* 선택: 다크 활성화(class 또는 media 중 하나) */
@import "./brand.css";                          /* 앱 오버라이드: 허용 목록만, tokens 뒤 */
@source "../node_modules/@kor-travel/ui";       /* 필수 2: ui 클래스 탐지 */
```

- `@import "tailwindcss"` 뒤에 `theme.css`를 둔다. 순서가 바뀌면 `@theme` 등록이 무시된다.
- `@source`는 `@kor-travel/ui`를 채택한 앱에만 필수다. `source(none)`을 쓰는 앱(geo)은 명시 `@source`가 없으면 아무 클래스도 탐지되지 않는다(`docs/runbooks/agent-failure-patterns.md`).
- Tailwind 없는 앱(weather Phase 1·airport main)은 `tokens.css`(+ `aliases/map-vocabulary.css`)만 import한다. 유틸리티는 생기지 않고 변수만 교체된다.
- 공통 CI `consumer-smoke`는 webpack·Turbopack 양쪽 `next build`로 이 연결을 검증한다(D-10).

## 3. `@theme inline`과 `@theme`의 구분

| 대상 | 정의 방식 | 이유 |
|---|---|---|
| 색·간격·radius·폰트·그림자·ease(`--color-kt-*`·`--spacing-kt-*`·`--radius-kt-*`·`--font-kt-*`·`--shadow-kt-*`·`--ease-kt-*`) | `@theme inline { --color-kt-brand: var(--kt-brand); … }` | 유틸리티가 `var(--kt-*)`를 그대로 내보내므로 `.dark`·`[data-kt-surface]`·앱 오버라이드가 런타임에 적용된다. 변수를 참조하는 토큰에 Tailwind 문서가 권장하는 방식(`dt` §3.6.3) |
| 타입 스케일(`--text-kt-2xs`…`--text-kt-2xl`) | `@theme { --text-kt-sm: 0.9375rem; … }`(비inline) | 유틸리티가 `var(--text-kt-sm)`을 참조해야 `[data-kt-surface='consumer'] { --text-kt-sm: 1rem }` 같은 변수 가리기(pinvi `[data-pv-surface='admin']` 선례)가 동작한다(`dt` §3.6.5, D-12) |
| duration | `@utility duration-kt-fast { transition-duration: var(--kt-duration-fast) }` | Tailwind v4에 duration 네임스페이스가 없어 map처럼 `@utility`로 정의 |

`@theme inline` 값이 리터럴이면 오버라이드가 먹지 않으므로(map의 리터럴 값은 영향 없음), common `theme.css`는 리터럴을 두지 않고 항상 `--kt-*` 참조만 둔다.

## 4. `@config` 금지

common 토큰을 도입한 앱은 `@config tailwind.config.ts`를 두지 않고 CSS-first만 쓴다.

- `@config`(v3 JS config)와 `@theme`의 병합 우선순위가 미확인이라 같은 utility 이름이 두 값으로 해석될 수 있다(`dt` §3.6.3; 실패 패턴 "같은 utility 이름이 두 값으로 해석됨").
- 대상 앱: geo(`--ui-*` 매핑 config), concierge(색·radius extend), pinvi web(`@pinvi/design-tokens/tailwind-preset`). 각각 T-441·T-453·T-421에서 `@config` 실효값을 빌드 산출 CSS로 검증한 뒤 `@theme` 단일화·config 삭제(D-08 ③④⑤).
- 예외: pinvi mobile(NativeWind 4·Tailwind 3.4.19)은 `tailwind-preset.cjs` 생성물을 소비한다. Tailwind 3 예외 등록은 O-8 사용자 승인 전까지 열림이며 기본값은 "예외 등록 + NativeWind 5 GA 재평가"다(D-29).

## 5. `kt-` 유틸리티 네임스페이스

패키지 내부 클래스는 `kt-` 접두 유틸리티만 쓴다(D-10). 예: `bg-kt-surface-page`, `text-kt-text-primary`, `border-kt-control-line`, `h-kt-control`, `h-kt-control-sm`, `rounded-kt-control`, `rounded-kt-panel`, `text-kt-2xs`, `font-kt-sans`, `shadow-kt-elevated`, `duration-kt-fast`, `outline-kt-focus`.

| 근거 | 내용 |
|---|---|
| 충돌 0 | `kt-` 접두는 전 저장소 0회. pinvi 사용자 preset(`cta`·`canvas`…)·airport shadcn 기본명(`primary`·`background`)·geo `--ui-*`·concierge `--ktc-*`와 겹치지 않는다(`dt` §3.6.1, `ui` §6.3) |
| 별칭 계층 불필요 | pinvi 치환표·concierge config 매핑 같은 앱 별칭 계층 없이 ui 클래스가 어느 앱에서나 동작한다(`ui` §6.3의 두 길 중 (i)를 접두로 해결) |
| tailwind-merge | `@kor-travel/ui/cn`이 `extendTailwindMerge`로 `kt-` 그룹(색·간격·radius·텍스트)을 등록해 `cn("bg-kt-surface-page", "bg-kt-surface-card")`가 뒤 값을 이기게 한다 |

앱 자체 코드는 `kt-` 유틸리티를 써도 되고 기존 이름(`bg-surface-page` 등)을 유지해도 된다. 앱 이름을 유지하려면 앱 `@theme inline`에서 `--color-surface-page: var(--kt-surface-page)`처럼 자기 이름을 `--kt-*`에 연결한다(`aliases/map-vocabulary.css`가 변수 계층에서 같은 일을 한다).

## 6. 프로필과 스코프 기법

| 프로필 | radius(control/panel) | control 높이 | 본문 | 스케일 | 값 소유 |
|---|---|---|---|---|---|
| `admin` | 6/8px | 36/30px | 15px | 7단(12/13.5/15/17/20/24/30) | common(`tokens.css` 기본값) |
| `consumer` | 8/14/20/32 | 44px 터치 | 16px | 9단(12~40) | pinvi(common은 `tokens.json` 의미 이름만) |

한 앱에서 두 프로필을 섞을 때(pinvi web)는 `[data-kt-surface='admin']`(또는 앱 속성 `[data-pv-surface='admin']`) 하위에서 형태·높이·타입 스케일 변수를 재선언하는 변수 가리기 기법을 쓴다. 형태·높이·모션은 이 프로필로만 바꾸고 브랜드 오버라이드 허용 목록(§7)에는 넣지 않는다. `base.scoped.css`는 이 스코프 안에서만 base 레시피를 발행한다.

## 7. 앱 오버라이드 허용 목록

앱 `brand.css`는 `tokens.css` 뒤에 import하며 다음 이름만 재선언한다(D-12, `dt` §3.6.4): brand 4(`--kt-brand`·`-hover`·`-tint`·`-foreground`), `--kt-focus`, paper(surface) 4, ink(text) 4, status 4 + tint(대비 검사 대상), font 스택(`--kt-font-sans`·`--kt-font-mono`; Pretendard 1순위는 Pretendard를 로드하는 앱만). `.dark` 값은 선택이다. 값 형식은 OKLCH 권고·hex 허용.

허용 목록 밖 이름을 재선언하면 `kt_contrast`가 아니라 [design-tokens](../standards/design-tokens.md) 규칙(TK-n) 위반이며 채택 PR 리뷰에서 막는다.

## 8. 다크 모드

- `tokens.css`는 `.dark` 값을 완비한다(map 기본값). 앱 오버라이드의 dark 값은 선택이다.
- 활성화는 앱이 `dark-class.css` 또는 `dark-media.css` 중 하나를 명시 import한다. 둘 다 import하지 않으면 `color-scheme: light`(base.css)로 media 변형이 우연히 켜지지 않는다(airport `globals.css`의 `color-scheme` 선언 선례).
- 대비 검사의 dark 쌍은 dark를 활성화한 앱에서만 필수다(O-11 기본값).

## 9. 대비 검사 `tools/kt_contrast.py`

| 항목 | 규칙 |
|---|---|
| 검사 쌍 | 본문 4.5:1(`--kt-text-primary/secondary/tertiary` × surface 4, `--kt-brand-foreground`/`--kt-brand`, status 텍스트/tint), 컨트롤 경계·focus 3:1(`--kt-control-line`/surface, `--kt-focus`/surface). `dt` §3.4.2의 재검증 쌍을 그대로 쓴다 |
| 대상 | 앱 `brand.css`(오버라이드 결과값)와 `tokens.css` 기본값. light 쌍 필수, dark 쌍은 dark 활성 앱만 |
| 모드 | report 기본. 앱 `contrast-baseline.json`(미달 쌍 + `until`)에 없는 **신규 미달**만 fail. 검사를 끄지 않는다(임시 예외는 owner·기한이 있는 `DEFERRED`로만) |
| 실행 | `python3 -B -X utf8 tools/kt_contrast.py <brand.css> [--baseline contrast-baseline.json] [--dark]`(인자는 T-103 확정). 소비자 CI는 `contrast-check.yml` 재사용 워크플로로 호출 |
| 현재 상태 | map만 수치 검증됨; geo·concierge·ktdm·airport는 미달 쌍이 있어 초기 baseline 등록이 필요(`dt` §3.4.2, `docs/survey/commonality-matrix.md` §2.1) |

Windows Python 3.11+ stdlib에서 동작해야 하며(D-03) 결과는 Markdown 표 + JSON + `$GITHUB_STEP_SUMMARY`로 낸다.

## 10. 검증 계층과 실패 시 조치

| 계층 | 검증 | 실패 시 |
|---|---|---|
| 패키지 | `npm pack` → tarball 설치 → `*.css`·`dist`·d.ts 존재, 생성물 diff 0 | `files`·`exports`·`sideEffects` 정정(실패 패턴 표) |
| 스모크 | `consumer-smoke`(패키지별 승인 소비자 pinned SHA) webpack·Turbopack `next build` | 릴리스 중단 |
| 소비자 PR | 6폭(320/375/414/768/1024/1440) 스크린샷 기준선 → 설정만 → 토큰만 → 컴포넌트 4단 PR, 각 단계 diff evidence(D-08·D-21) | 원인 불명 diff는 해당 단계 revert |
| 규칙 | `ux_lint`(raw hex/oklch, `text-[Npx]`, `rounded-2xl+`, 팔레트 alpha, `outline-none`, `transition-all/colors`, `aria-disabled:opacity-`, `window.confirm`) 전체 report + `--base <sha>` diff fail | 신규 위반만 fail, 잔존은 앱 baseline |

## 11. 열림(사용자 확인 필요)

| # | 항목 | 기본값 |
|---|---|---|
| O-4 | 유틸리티/변수 네임스페이스 | `kt-` / `--kt-*`(이 문서 전제) |
| O-8 | pinvi mobile Tailwind 3 예외 | 사용자 승인 대기; 승인 전 `exceptions` 미등록 |
| O-11 | 다크 모드 | 정의 필수·활성 opt-in·앱 오버라이드 dark 선택 |
| O-13 | 마커 팔레트 정본 | map 확정 요청(T-505); common은 규칙만 |
