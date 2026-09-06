# 횡단 비교 — 디자인 토큰·색상 톤

`kor-travel-common` 설계를 위한 읽기 전용 조사. 7개 kor-travel 앱과 참조 저장소(canview)의 **실제 토큰 정의**(CSS 변수, `@theme`, Tailwind preset, TS 상수)와 디자인 문서를 수집·비교하고, 공통 semantic 계약으로 분리할 수 있는 부분과 앱 고유로 남길 부분을 판정한 뒤, common 토큰 패키지 초안을 제안한다.

표기 규칙: **[사실]** 파일에서 직접 확인 · **[후보]** 근거는 있으나 결정이 필요 · **[추정]** 정황으로 추론 · **[미확인]** 조사 범위에서 확인하지 못함. 별도 표기가 없는 문장은 [사실]이다.

## 0. 요약

- 토큰 **어휘**는 이미 kor-travel-map admin(`globals.css` `@theme inline` + `:root`/`.dark`, OKLCH)을 원형으로 weather·geo·concierge·pinvi admin·docker-manager가 각자 이식해 두었다. 형태(6/8px radius, 36/30px control)와 역할 이름(surface-page/subtle/muted, text-primary/secondary/tertiary, brand/tint, 4종 status+tint, focus, control-line)은 사실상 수렴했다. 값(브랜드 hue, paper hue)은 앱마다 다르며 문서가 그 차이를 의도한 것으로 명시한다.
- 값 형식은 OKLCH(map·weather·airport·geo·docker-manager·canview)와 hex(pinvi·concierge)로 갈린다. pinvi는 v3 preset(hex)을 `@config`로 v4에 태우고 admin 전용 `@theme`만 추가했다.
- 대비 규칙을 **수치로 문서화하고 검증한 앱은 map과 pinvi admin 둘뿐**이다. 이번 조사에서 같은 계산으로 재검증한 결과 map의 수치는 전부 일치했고, pinvi의 hairline 두 수치(#dddddd 1.6:1, #c1c1c1 2.7:1)는 실측(1.36 / 1.80)과 달랐다(결론은 동일하게 3:1 미달). 수치가 없는 concierge·geo·docker-manager·airport의 컨트롤 경계는 계산상 WCAG 1.4.11(3:1) 미달이다.
- 마커 팔레트 `P-01`~`P-16`은 **같은 코드 공간에 서로 다른 hex 두 벌**이 존재한다(map `map-marker-react` PALETTE = Tableau 계열, P-01 파랑 `#1f77b4` / pinvi `@pinvi/design-tokens` MARKER_PALETTE = Material 계열, P-01 빨강 `#E53935`). 이는 UI 토큰이 아니라 데이터 도메인 팔레트이므로 common 토큰 패키지의 소유가 아니라 `marker_color` 데이터 소유자(kor-travel-map) 쪽 정본 확정이 필요하다.
- 접두 `--ktc-*`는 concierge가 이미 앱 전용 토큰 이름으로 125회 쓰고 있다. common 접두로 `--ktc-`를 고르면 concierge의 기존 이름과 의미가 겹치므로, `--kt-`(전 저장소 0회) 또는 concierge 토큰을 common 오버라이드로 재해석하는 두 안 중 하나를 결정해야 한다.

## 1. 기준

| 저장소 | 체크아웃 경로 | 기준 커밋 | 토큰 정본(파일) | Tailwind(설치, lockfile) | Next / React(설치) |
|---|---|---|---|---|---|
| kor-travel-map | `F:/dev/kor-travel-common-survey/ktm-main` | `c494e227` | `packages/kor-travel-map-admin/frontend/src/app/globals.css` | 4.3.3 | 16.2.12 / 19.2.8 |
| pinvi | `F:/dev/kor-travel-common-survey/pinvi` | `9af25e5` | `packages/design-tokens/src/*.ts`, `packages/design-tokens/tailwind-preset.cjs`, `apps/web/app/globals.css`(admin `@theme`) | web 4.3.3 · mobile 3.4.19(NativeWind 4) | 16.3.3 / 19.2.6 |
| kor-travel-weather | `F:/dev/kor-travel-weather` | `6003da9` | `packages/kor-travel-weather-admin/frontend/app/tokens.css` | 없음(순수 CSS) | 15.5.24 / 19.2.8 |
| kor-travel-airport | `F:/dev/kor-travel-common-survey/kta-main` | `2bb1111`(detached) · WIP `codex/shadcn-ui-foundation` = `99b3f98` | `frontend/src/app/tokens.css` | main 없음 · WIP `^4.3.3` 요구 | 16.3.2 / 19.2.8 |
| kor-travel-geo | `F:/dev/kor-travel-geo-fixes` | `1d9d74d` | `kor-travel-geo-ui/app/globals.css` (+ `tailwind.config.ts`) | 4.3.1 | 16.2.12 / 18.3.1 |
| kor-travel-concierge | `F:/dev/kor-travel-concierge` | `7945305` | `frontend/tokens.css` (+ `frontend/src/app/globals.css`, `frontend/tailwind.config.ts`) | 4.3.1 | 16.2.7 / 19.2.8 |
| kor-travel-docker-manager | `F:/dev/kor-travel-common-survey/ktdm-main` | `862562d` | `frontend/tokens.css` | 4.3.1 | 14.2.35 / 18.3.1 |
| canview(참조) | `F:/dev/canview` | `d078437`(branch `agent/codex-doc-information-architecture`) | `tokens.css` | 해당 없음 | 해당 없음 |

설치 버전은 각 저장소 `package-lock.json`의 `node_modules/<pkg>.version`에서 읽었다(pinvi web은 `apps/web/node_modules/tailwindcss` 항목 4.3.3, 루트 `node_modules/tailwindcss`는 mobile용 3.4.19). 선행 보고서(`F:/dev/kor-travel-geo-fixes/docs/kor-travel-common-library-review.md`)는 `package.json` 요구 범위만 적었고 lockfile 설치 버전은 이번에 추가로 확인한 것이다.

## 2. 방법

읽기 전용으로만 진행했다(`git rev-parse`, `git ls-files`, `git show`, `git diff --stat`, `git grep`, `grep`, `sed`, `cat`). 조사 대상 저장소에 파일을 만들거나 바꾸지 않았고, 산출물은 이 문서 하나다. 대비 계산은 스크래치 디렉터리의 Python 스크립트(OKLCH→OKLab→linear sRGB→클램프→WCAG 상대 휘도)로 수행했으며 저장소에는 남기지 않았다.

주요 명령:

```bash
git ls-files | grep -iE '(globals\.css|tokens\.css|design\.md|DESIGN|design-system|design-rules|tailwind\.config|components\.json)'
git show codex/shadcn-ui-foundation:frontend/src/app/globals.css        # airport WIP
git diff --stat 2bb1111 codex/shadcn-ui-foundation
grep -nE '"node_modules/(tailwindcss|next|react)"' -A1 package-lock.json  # 설치 버전
git grep -c -- '--ktc-' -- '*.css' '*.ts' '*.tsx'                        # 접두 충돌 확인
```

읽은 파일은 §6 근거 파일 목록에 정리했다. 큰 파일(weather `globals.css` 2334줄, airport 1844줄, geo 3750줄, docker-manager 1383줄)은 구조 grep 후 토큰 블록·focus·reduced-motion·마커 색 구간만 읽었다.

## 3. 본문

### 3.1 앱별 토큰 체계 비교

#### 3.1.1 정본 파일 · 정의 방식 · 값 형식 · 모드

| 앱 | 정본 위치 | 정의 방식 | 변수 접두/명명 | 값 형식 | 다크 모드 | 근거 |
|---|---|---|---|---|---|---|
| map admin | `globals.css` 한 파일(별도 tokens.css 없음) | `:root`/`.dark`에 값, `@theme inline`이 utility 이름으로 연결 | 접두 없음. 프로젝트 어휘(`--surface-page`, `--text-primary`, `--brand`, `--control-line`) + shadcn alias(`--background`, `--primary`, `--input`…) | OKLCH(`oklch(97.8% 0.003 128)`) | `.dark` 블록 완비, `@custom-variant dark (&:is(.dark *))`. **토글 미장착**(design.md L78, `ui/sonner.tsx` L53 "no ThemeProvider is mounted") | `globals.css` L1-29, L69-197, L211-306, L356-426; `design.md` L300-302 |
| pinvi web(사용자) | `packages/design-tokens/tailwind-preset.cjs`(v3 preset) ← `apps/web/tailwind.config.ts` `presets` ← `globals.css` `@config` | preset의 `theme.extend`(색·폰트·radius·shadow·zIndex·duration) | 접두 없음. Airbnb 어휘(`canvas`, `ink`, `hairline`, `primary`, `cta`, `scrim`) | hex(`#ff385c`) | **없음**(DESIGN.md L41 "Airbnb does not have a dark mode"; globals/preset에 `.dark`·`prefers-color-scheme` 0건) | `tailwind-preset.cjs` L7-120; `globals.css` L12-15 |
| pinvi web(admin) | `apps/web/app/globals.css` `@theme { --color-admin-* }` + `[data-pv-surface='admin']` 스코프 | v4 `@theme`(값 직접) — preset과 병합 | `--color-admin-line/control-line/page/subtle/muted/success(-tint)/danger(-tint)/warning(-tint)/info(-tint)/brand-tint/brand-ink` | hex | 없음 | `globals.css` L27-88, L114-127; `app/(admin)/layout.tsx` L20 |
| pinvi mobile | 동일 preset + `nativewind/preset`; `components/ui.tsx`가 `colors` TS 상수 직접 import | Tailwind v3 preset | 위와 동일 | hex | 없음 | `apps/mobile/tailwind.config.js`; `apps/mobile/components/ui.tsx` L12 |
| weather admin | `app/tokens.css` | `:root`/`.dark` 순수 CSS 변수. Tailwind 미사용 | map 어휘 그대로(`--surface-page`…) + legacy alias `--color-ink/paper/panel/rule/accent/danger/warning/info(-soft)` | OKLCH | `.dark` 완비, **토글 미장착**(components에 dark 클래스 조작 없음) | `tokens.css` L1-105, L107-161; `package.json`(tailwind 의존성 없음) |
| airport(main) | `frontend/src/app/tokens.css` + `globals.css` `:root` alias | 순수 CSS. primitive는 `--color-*`/`--radius-*`/`--space-*`, globals가 짧은 alias(`--bg`, `--surface`, `--ink`, `--line`, `--accent`)로 재매핑 | `--color-canvas/surface/surface-raised/ink/muted/line/accent(-strong/-soft)/button-bg/button-ink/teal/red/yellow/input/grid/sticky` | OKLCH, **alpha 다수**(`--color-line` ink/14%, `--color-accent-soft` 13%, `--color-input` white/88%) | `@media (prefers-color-scheme: dark)`만(클래스 없음), `color-scheme` 선언 | `tokens.css` L3-55; `globals.css` L4-27, L49-70 |
| airport(WIP `99b3f98`) | 위 tokens.css 유지 + `globals.css`에 `@import "tailwindcss"`, `@import "shadcn/tailwind.css"`, shadcn 변수(`--background`…)를 `var(--color-*)`로 배선, `@theme inline`(L1876) 추가 | Tailwind v4 + shadcn `base-nova` | 동일 | 동일 | media query 유지(주석 L7-9 "클래스 토글 없음… next-themes 미도입") | `git show codex/shadcn-ui-foundation:frontend/src/app/globals.css` L2-9, L35-59, L1876; `frontend/package.json` diff; `frontend/components.json` |
| geo admin | `kor-travel-geo-ui/app/globals.css` | `:root` primitive(`--color-paper/ink/rule/accent…`) → semantic(`--surface-*`, `--text-*`, `--line`, `--brand`) → `@theme inline`(map 어휘) + `@config tailwind.config.ts`(v3식 colors) + 두 번째 `@layer base :root`의 `--ui-*` shadcn alias 층 | 3중: `--color-*`(primitive), 접두 없음(semantic), `--ui-*`(shadcn) | OKLCH **소수 L 표기**(`oklch(0.975 0.008 262.9)`) | **없음**(`.dark` 0건) | `globals.css` L7-10, L14-77, L79, L91-176, L2418-2480; `tailwind.config.ts` |
| concierge admin | `frontend/tokens.css` | `:root`/`.dark`의 **`--ktc-*`** 정본 → `globals.css` `@layer base :root`가 접두 없는 semantic으로 매핑(+ 앞쪽에 hex fallback 블록 중복) → `@config tailwind.config.ts`가 utility 생성 | `--ktc-surface-page/card/subtle/muted/row`, `--ktc-brand(-tint/-ink/-hover/-foreground)`, `--ktc-shell-rail*`, `--ktc-text-*`, `--ktc-line`, `--ktc-control-line`, `--ktc-focus`, `--ktc-overlay`, 4 status+tint, radius/height/shadow/duration | hex(+ `rgb(… / a)` overlay) | `.dark` 완비, 토글 미장착. globals L7-8 주석은 "geo UI는 light 전용"이라 적혀 있어 geo에서 복사된 흔적 | `tokens.css` L1-87; `globals.css` L1-5, L20-104, L234-312; `tailwind.config.ts` |
| docker-manager | `frontend/tokens.css` | v4 `@theme`(값 직접, inline 아님) + `:root`(space/duration/z) | `--color-page/card/subtle/elevated/row/line/strong/ink/secondary/tertiary/disabled/brand(-ink/-tint)/info/warn/danger/ok/graphite(-2/-ink)`, `--shadow-*`, `--radius-card/panel/pill`, `--ease-*`, `--font-*` | OKLCH | **없음** | `tokens.css` L5-48, L50-72 |
| canview(참조) | `tokens.css` | `:root` 순수 CSS 변수 | `--color-paper(-2..4)/ink(-2)/muted/rule(-2)/accent(-ink/-wash/-line)/focus/warning(-ink/-wash)/error(-ink/-wash)/overlay/mode-sport(-wash)/mode-eco(-wash)`, `--space-*`, `--text-*`, `--radius-*`, `--rule-*`, `--touch-*`, `--ease-*`, `--dur-*`, `--z-*` | OKLCH | **다크 전용**(주행 화면) | `tokens.css` L1-67 |

관찰:

- map·weather·geo·concierge는 "shadcn 이름은 유지하되 값은 프로젝트 어휘 alias"라는 같은 패턴이다(map `globals.css` L276-305, weather `tokens.css` L63-77, geo `globals.css` L2418-2463, concierge `globals.css` L286-311). docker-manager는 shadcn 미도입이지만 DESIGN.md L130-132가 도입 시 매핑 규칙을 미리 적었다.
- geo는 alias 층이 셋(`--color-*` → semantic → `--ui-*` → `--background` 등)이고, `tailwind.config.ts` L48-60에 v3 시절 raw hex(`ink: "#172033"`, `line: "#d8dee8"`, `brand: "#2563eb"`, `info/warn/danger`)가 남아 `@theme inline`의 `--color-brand: var(--brand)`와 **같은 utility 이름을 두 곳에서 정의**한다. 어느 쪽이 이기는지는 [미확인](Tailwind 문서에서 `@config`와 `@theme` 병합 우선순위를 찾지 못했다). `text-brand` 6회·`border-brand` 4회·`bg-brand` 3회가 이 이름을 쓴다.
- concierge `globals.css` L20-104는 tokens.css와 값이 다른 hex fallback 블록을 같은 layer 앞쪽에 두고(L21-24 주석: "매핑이 제거될 경우의 fallback"), L234-312가 `--ktc-*`로 덮는다. 정본이 둘로 보이는 구조다.
- pinvi admin은 `--color-admin-*`를 **신규 이름으로만** 추가해 사용자 표면 utility와 충돌을 피했고(`globals.css` L24-25), 타입 스케일은 `[data-pv-surface='admin']`에서 변수만 가려 같은 클래스 이름이 admin에서 다른 크기로 렌더되게 했다(L99-127). admin 컴포넌트에서 `border-admin-line` 41회, `bg-admin-subtle` 30회 등 실제로 쓰인다.

#### 3.1.2 형태 · 크기

| 앱 | radius | control 높이 | rail/셸 폭 | 근거 |
|---|---|---|---|---|
| map | **2종** `--radius-control` 6px · `--radius-panel` 8px; `--radius-xs..md`→control, `lg..4xl`→panel로 강제 수렴 | `--control-h` 36px · `--control-h-sm` 30px (`h-control`/`h-control-sm`); micro 예외 4개(h-7, h-6, size-5, size-4) | `--rail` 22rem(우측 inspector), sidebar 16rem | `globals.css` L143-153, L211-218; `design.md` L94-108 |
| pinvi 사용자 | sm 8 · md 14 · lg 20 · xl 32 · full | 터치 44px(`min-h-11`, `minHeight.touch`) | — | preset L81-86, L103-108; DESIGN.md L284-289 |
| pinvi admin | + `--radius-control` 6 · `--radius-panel` 8 (utility `rounded-control/panel`) | `--spacing-control` 36 · `--spacing-control-sm` 30 (44px 예외 2쪽 명시) | `--spacing-rail`/`--container-rail` 22rem | `globals.css` L28-38 |
| weather | control 6 · panel 8; **`--radius-md`→panel**(map은 control) | 36 / 30 | `--rail` 17rem(주석은 "map's canonical" — map 값 22rem과 다름) | `tokens.css` L15-26 |
| airport | `--radius-card` 16px · `--radius-control` 10px (WIP: `--radius: var(--radius-control)`) | `.input`/`.button` min-height 46px(토큰 아님) | — | `tokens.css` L23-24; WIP globals L28, L186-200 |
| geo | control 6 · panel 8; xs..md→control, lg..2xl→panel | 36 / 30 (+ `.nav-link` min-height 2.75rem) | sidebar 16rem | `globals.css` L54-61, L144-147, L2470-2475 |
| concierge | control 6 · panel 8; `--ktc-radius` 8, `--ktc-radius-sm` 6; tailwind `md=calc(radius-2px)`, `sm=calc(radius-4px)` | 36 / 30 (`--ktc-control-height(-sm)`) | 16rem/4rem(design.md L11) | `tokens.css` L41-46; `tailwind.config.ts` L10-22 |
| docker-manager | **`--radius-card` 6px**(이름은 card지만 control 역할) · `--radius-panel` 8 · `--radius-pill` 999 | 토큰 없음 [미확인: 컴포넌트 클래스 값] | 16rem/4rem | `tokens.css` L34-37; DESIGN.md L59 |
| canview | xs 4 · sm 8 · md 12 · lg 18 | `--touch-primary` 76 · `--touch-secondary` 48 | — | `tokens.css` L46-54 |

6/8px · 36/30px는 map 원형을 weather·geo·concierge·pinvi admin·docker-manager가 그대로 받았다(각 파일 주석이 "map 값 그대로"라고 명시). airport(16/10, 46px)와 pinvi 사용자 표면(8/14/20/32, 44px)은 별도 밀도다.

#### 3.1.3 간격

| 앱 | 간격 토큰 | 값(px) | 근거 |
|---|---|---|---|
| map | Tailwind 기본 4pt만(전용 토큰 없음) | `gap-2`=8, `p-4`=16, `py-6`=24 | `design.md` L95 |
| pinvi | `spacing.ts` 0..16 + preset `spacing.section` | 0/4/8/12/16/20/24/32/40/48/64 · section 64 | `spacing.ts` L1-14; preset L100-102 |
| weather | `--space-3xs..2xl` | 2/4/8/12/16/24/40/64 | `tokens.css` L28-36 |
| airport | `--space-1..10` | 4/8/12/16/20/24/32/40 | `tokens.css` L27-34 |
| geo | `--space-3xs..2xl` | 4/8/12/16/24/32/48/72 | `globals.css` L108-115 |
| concierge | 없음(Tailwind 기본) | — | `tailwind.config.ts` |
| docker-manager | `--space-3xs..2xl` | 4/8/12/16/24/32/48/72(geo와 동일) | `tokens.css` L51-58 |
| canview | `--space-3xs..xl` | 2/4/8/12/16/24/40 | `tokens.css` L32-38 |
| pinvi DESIGN.md Exports(이식용) | `--space-3xs..3xl` | 4/8/12/16/24/32/48/64/96 | DESIGN.md L382-390 |

같은 이름 `--space-3xs`가 weather 2px, geo/ktdm 4px로 다르다. Tailwind v4 앱은 `--spacing` 기본 4pt를 쓰므로 별도 간격 토큰은 순수 CSS 앱(weather·airport)과 geo·ktdm의 legacy CSS에서만 의미가 있다.

#### 3.1.4 타입 스케일 · 폰트

| 앱 | 스케일 | 본문 | 폰트 스택(sans / mono) | 실제 로딩 | 근거 |
|---|---|---|---|---|---|
| map | 7단 `--text-2xs..2xl` = 12 / 13.5 / 15 / 17 / 20 / 24 / 30 (`text-[Npx]` 금지) | 15px | Pretendard Variable → Pretendard → Noto Sans KR… / Geist Mono | `pretendard` npm 1.3.9 dynamic subset(`layout.tsx` L22) + `next/font/google` Geist_Mono(L14) | `globals.css` L155-186; `design.md` L82-92 |
| pinvi 사용자 | 12/14/16/18/20/24/28/32/40 (`fontSize`) | 16px(입력 포함, iOS 확대 방지) | Pretendard Variable → … Roboto / 시스템 mono(`ui-monospace, "SF Mono"…`) | `pretendard` npm 1.3.9(`globals.css` L8) | `typography.ts`; DESIGN.md L276-282 |
| pinvi admin | 스코프 재정의 xs 13.5 / sm·base 15 / lg 20 / xl 24 / 2xl 30 + 전역 `--text-2xs` 12, `--text-md` 17 | 15px | 동일 | 동일 | `globals.css` L40-46, L114-127 |
| weather | 스케일 토큰 없음(`body` 0.9375rem 하드코딩) | 15px | **Geist** → Pretendard Variable → Pretendard → Noto Sans KR… / Geist Mono | **로딩 없음**(`next/font`·`pretendard`·`geist` 의존성 없음) → OS 설치 폰트 의존 | `tokens.css` L8-12; `globals.css` L28-36; `package.json` |
| airport | 없음(rem/clamp 인라인) | — | Pretendard Variable → Apple SD Gothic Neo → Noto Sans KR / JetBrains Mono | 로딩 없음 | `tokens.css` L25-26; `layout.tsx` |
| geo | map과 동일 7단(`@theme inline`) | 15px | display Pretendard Variable → Noto Sans KR · body **Noto Sans KR** → Pretendard / IBM Plex Mono | 로딩 없음(app·components·next.config에 `next/font`·`@font-face`·googleapis 0건) | `globals.css` L36-63, L105-107 |
| concierge | 2xs 12 / **xs 13** / sm 15 / md 17 / lg 20 / xl 24 / 2xl 30(행간도 map과 다름) | 15px | `--ktc-font-sans` Pretendard Variable → … / "Geist Mono" | Pretendard npm 로딩(`layout.tsx` L4); Geist Mono 미로딩 | `tailwind.config.ts` L23-35; `tokens.css` L3-4 |
| docker-manager | 없음(Tailwind 기본) | 14px 이상(DESIGN.md) | **Noto Sans KR** → Pretendard Variable(display·sans 동일 순서) / IBM Plex Mono | 로딩 없음(주석이 "실제로 로드되는 웹폰트가 없어"라고 명시) | `tokens.css` L42-48; `layout.tsx` |
| canview | micro 10 / label 12 / body 14 / title 20 / metric 64 | 14px | Segoe UI·Malgun Gothic / — | 임베디드 | `tokens.css` L29-30, L40-44 |

문서 드리프트: docker-manager `docs/DESIGN-RULES.md` L22-23은 "표시 제목 Space Grotesk, 본문 IBM Plex Sans"라고 적었으나 `tokens.css`·`DESIGN.md` L48-52는 Noto Sans KR/Pretendard다. map `docs/architecture/admin-frontend-design-rules.md` L75-84는 `text-[24px]` 등 px 임의값을 권장하지만 이후 `design.md`(2026-08-18) L88·L270은 `text-[Npx]`를 금지 패턴으로 잠갔다 — 옛 규칙 문서가 갱신되지 않은 상태다.

#### 3.1.5 모션

| 앱 | easing | duration | 정책 | 근거 |
|---|---|---|---|---|
| map | `--ease-out` (0.16,1,0.3,1) · `--ease-in` (0.7,0,0.84,0) | `--duration-fast` 100 · `--duration-base` 150(`@utility duration-fast/base`) | `transition-all`·`transition-colors`·맨 `transition` 금지(전환 목록에 `outline-color` 포함 → 링 페이드) · reduced-motion 전역 + 스피너 예외 | `globals.css` L199-209, L221-226, L430-457; `design.md` L115-135 |
| pinvi | `ease-pinvi` (0.2,0,0,1) 단일(admin `--ease-admin-out/in` 추가) | fast 100 · normal 200 · moderate 300 | overshoot·scale·layout 애니메이션 금지, reduced-motion 전역(스피너 예외 없음) | preset L109-117; `globals.css` L48-50, L227-236 |
| weather | out 동일 · **in (0.7,0,0.84,1)**(map과 마지막 계수 다름) | fast 100 · base 150 | reduced-motion 전역 | `tokens.css` L83-88; `globals.css` L1899-1907 |
| airport | 토큰 없음(design.md "160ms opacity/transform") | 토큰 없음 | reduced-motion(L1836) | `design.md` L16; `globals.css` L1836 |
| geo | `--ease-default` (0.16,1,0.3,1) · in · in-out | fast 100 · normal 150 · long 420; `@utility duration-base`가 **정의되지 않은 `--duration-base`** 참조(현재 소비처 없음 — 컴포넌트는 `duration-fast/normal`만 사용) | reduced-motion에서 `transition-duration: 0s`(0.01ms가 아닌 이유를 주석으로 설명) | `globals.css` L81-89, L152-157, L2398-2416 |
| concierge | `--ktc-ease` (0.2,0,0,1); globals fallback `--ease-in` (0.4,0,1,1) | `--ktc-duration-fast` 120 · normal 180(fallback 블록은 200) | reduced-motion 전역 + `.animate-spin` 예외 | `tokens.css` L52-54; `globals.css` L61-65, L216-230 |
| docker-manager | default (0.16,1,0.3,1) · in · in-out | fast 120 · normal 220 · long 420(DESIGN.md L61 "120ms", L132 "150ms" 불일치) | `transition-all` 금지, reduced-motion 0.001ms | `tokens.css` L38-40, L60-62; `globals.css` L51-80 |
| canview | out·in·in-out | micro 100 · short 180 · long 300 | 160ms fade, 보간 연속성 | `tokens.css` L56-61; `docs/ui/design.md` L126 |

#### 3.1.6 z-index

| 앱 | 이름 있는 단계 | 실제 사용 | 근거 |
|---|---|---|---|
| map | 없음 | utility `z-50` 7회, `z-10` 4회, `z-30`/`z-20` 1회 | `src/**` grep |
| pinvi | nav 30 · panel 40 · overlay 50 · modal 60 · toast 70 (preset `zIndex`) | 임의 `z-[` 0건(T-316) | preset L92-99; DESIGN.md L289, L326-327 |
| weather | 없음 | raw 2(3회), 100 | `globals.css` grep |
| airport | 없음 | raw 1·2·4·5 | `globals.css` L422, L536, L554, L1523 |
| geo | base 1 · raised 10 · dropdown 100 · sticky 200 · modal 400 · toast 500 | `var(--z-*)` + shadcn primitive `z-50`, toaster `z-[100]` | `globals.css` L158-163; `components/ui/*` |
| concierge | 없음 | `z-50`(dialog·popover·select), `z-10` | `components/ui/*` |
| docker-manager | base 1 · raised 10 · dropdown 100 · sticky 200 · **drawer 300** · modal 400 · toast 500 | `var(--z-*)` + `z-10` 9회, `z-50` 1회 | `tokens.css` L64-71 |
| canview | base 1 · raised 10 · sticky 200 · modal 400 | — | `tokens.css` L63-66 |

#### 3.1.7 그림자

| 앱 | 정의 | 원칙 | 근거 |
|---|---|---|---|
| map | card/card-hover(정의만, 미사용) · elevated 4/12 α.10 · modal 8/24 α.14 (oklch alpha) | rest=hairline만, 그림자는 오버레이 전용 | `globals.css` L270-274; `design.md` L110-113 |
| pinvi | card 3겹(≤8%) · overlay(≤8%) | 2티어, `shadow-sm..2xl` ESLint 금지 | preset L87-91; `eslint.config.mjs` L18 |
| weather | card/card-hover **none** · elevated · modal | map 규칙 | `tokens.css` L79-82 |
| airport | card 0 18px 42px α.09 · focus 0 0 0 3px α.30 | 카드 상시 그림자 | `tokens.css` L21-22 |
| geo | card α.04 · hover α.08 · button α.12 · modal α.18 | DESIGN-RULES 4(4%/12% 상한) — modal 18%는 자체 규칙 초과 [사실] | `globals.css` L139-142; `DESIGN-RULES.md` L29-31 |
| concierge | card α.04 · hover α.08 · button α.06 · modal α.12 · elevated α.10 (rgb 15 23 42 = slate) | 기본 카드 무그림자, popup만 modal | `tokens.css` L47-51 |
| docker-manager | card 2겹 α.05/.035 · hover α.08/.06 · modal α.22 | 모달·인증 카드만 | `tokens.css` L30-32 |
| canview | 없음(`--rule-thin/strong` 선 두께로 대체) | — | `tokens.css` L51-52 |

### 3.2 의미(semantic) 역할 매핑표

#### 3.2.1 라이트 값

열의 값은 각 앱의 **정본 파일에 적힌 그대로**다(alias 체인은 최종 값으로 풀었다). "—"는 해당 역할의 토큰이 없음.

| 역할 | map | pinvi 사용자 / admin | weather | airport | geo | concierge(`--ktc-*`) | docker-manager(`--color-*`) | canview(`--color-*`) |
|---|---|---|---|---|---|---|---|---|
| surface/canvas | `--surface-page` oklch(97.8% .003 128) | `canvas` #ffffff / `admin-page` #ffffff | `--surface-page` oklch(97.8% .003 250) | `--color-canvas` oklch(97.5% .012 86) | `--surface-page`=`--color-paper` oklch(.975 .008 262.9) | `surface-page` #f4f5f0 | `page` oklch(98.2% .006 41) | `paper` oklch(10% .02 248) |
| card/panel | `--card` oklch(99.2% .002 140) | (canvas 재사용) | `--card` oklch(99.2% .002 250) | `--color-surface` oklch(99.2% .008 86) · `surface-raised` #fff | `--surface-card`=`paper-raised` oklch(.992 .004 262.9) | `surface-card` #fcfcf9 | `card` oklch(100% 0 0) | `paper-2` oklch(14% .026 246) |
| surface-subtle | `--surface-subtle` oklch(96.7% .006 138) | `surface-soft` #f7f7f7 / `admin-subtle` | `--surface-subtle` oklch(96.7% .006 250) | (`--color-sticky` oklch(95% .022 86)) | `paper-muted` oklch(.95 .014 262.9) | `surface-subtle` #edf0e9 | `subtle` oklch(95.9% .012 41) | `paper-3` oklch(19% .03 242) |
| surface-muted | `--surface-muted` oklch(92.5% .01 141) | `surface-strong` #f2f2f2 / `admin-muted` | oklch(92.5% .01 250) | — | `paper-strong` oklch(.916 .021 262.9) | `surface-muted` #dce3d9 | `elevated` oklch(92.8% .018 41) | `paper-4` oklch(24% .032 240) |
| text/ink | `--text-primary` oklch(30% .006 157) | `ink` #222222 | oklch(30% .025 255) | `--color-ink` oklch(24% .026 258) | `--text-strong`=`ink` oklch(.235 .023 244) · `--text-primary`=`ink-soft` oklch(.35 .025 244) | `text-strong` #1d2823 · `text-primary` #29342e | `strong` oklch(24.5% .021 41) · `ink` oklch(35% .025 41) | `ink` oklch(96% .008 230) |
| text-secondary | `--text-secondary` oklch(48% .012 159) | `body` #3f3f3f · `muted` #6a6a6a | oklch(48% .04 255) | `--color-muted` oklch(52% .025 258) | `muted` oklch(.51 .018 244) | `text-secondary` #5f6b63 | `secondary` oklch(49% .023 41) | `ink-2` oklch(82% .012 235) |
| text-tertiary | `--text-tertiary` oklch(54% .012 154) | `muted-soft` #929292(disabled 전용) | oklch(54% .04 255) | — | `muted-soft` oklch(.6 .014 244) | `text-tertiary` #7e8982 | `tertiary` oklch(61% .019 41) | `muted` oklch(63% .016 240) |
| text-disabled | `--text-disabled` oklch(79% .012 154) | `primary-disabled` #ffd1da(CTA) | oklch(79% .025 255) | — | `disabled` oklch(.67 .012 244) | `text-disabled` #a8b0aa | `disabled` oklch(70% .015 41) | — |
| icon-default | `--icon-default` = text-tertiary 값 | — | oklch(54% .04 255) | — | `--color-icon-default: var(--text-secondary)`(map과 다른 단계) | `icon-default` #69776e | — | — |
| border/hairline(장식) | `--border`=`--surface-muted` | `hairline` #dddddd · `hairline-soft` #ebebeb / `admin-line` #dddddd | `--border`=`--surface-muted` | `--color-line` ink **/14%** | `--line`=`rule` oklch(.84 .014 210) | `line` #d5ddd3 | `line` oklch(87.4% .018 41) | `rule` oklch(29% .028 242) · `rule-2` |
| control line(입력 경계) | `--control-line` oklch(61% .012 145) (=`--input`) | `border-strong` #c1c1c1 / `admin-control-line` #767676 | `--control-line` oklch(61% .035 255) | `--input-border`=`--color-line`(alpha) | `--control-line`=`rule-strong` oklch(.72 .02 210) (=`--input`, `--ui-input`) | `control-line` #aab5ad | —(line 겸용) | `--rule-strong` 2px(두께) |
| primary/brand | `--brand` oklch(51.4% .081 169) 녹 | `primary` #ff385c Rausch | `--brand` oklch(47% .14 255) 남 | `--color-accent` oklch(61% .16 43) 주황 · `button-bg` oklch(48% .15 38) | `--brand`=`accent` oklch(.546 .215 262.9) 청 | `brand` #7c3aed 보라 | `brand` oklch(64.6% .222 41.1) 주황 | `accent` oklch(72% .155 230) 시안 |
| brand-hover/ink | `--brand-hover` oklch(46% .085 169) | `primary-active` #e00b41 / `admin-brand-ink` #c8093a | oklch(41% .15 255) | `accent-strong` oklch(50% .15 38) | `--brand-ink` oklch(.488 .217 264.4) | `brand-ink`=`brand-hover` #6d28d9 | `brand-ink` oklch(55.3% .195 38.4) | `accent-line` oklch(47% .105 232) |
| brand-tint | `--brand-tint` oklch(95.2% .013 172) | — / `admin-brand-tint` #ffeef1 | oklch(95% .025 250) | `accent-soft` accent **/13%** | `--brand-tint` oklch(.932 .032 255.6) | `brand-tint` #ede9fe | `brand-tint` oklch(95.4% .038 75.2) | `accent-wash` oklch(19% .06 236) |
| brand-foreground | oklch(99% .002 140) | `on-primary` #ffffff | oklch(99% .002 250) | `button-ink` white | `paper-raised` | `brand-foreground` #ffffff | — [미확인] | `accent-ink` oklch(12% .026 246) |
| cta(채운 CTA) | = brand | **`cta` #e00b41 · `cta-hover` #c8093a**(primary와 분리) | = brand | = button-bg | = brand | = brand | = brand | = accent |
| focus | `--focus` oklch(45% .09 169) 불투명 | `focus` #ff385c(=Rausch) | `--focus` oklch(43% .13 255) | outline `--accent` + `--shadow-focus` α.30 | `--focus`=`--brand` | `focus` #6d28d9 | (= `--color-brand`) | `focus` oklch(82% .145 226) |
| danger/error | `--destructive` oklch(51.4% .167 27) · tint oklch(96% .03 25) | `error-text` #c13515 · `error-bg` #fdecea / `admin-danger` 동일 | map과 동일 | `--color-red` oklch(52% .16 28) | `--danger`=`danger` oklch(.51 .175 28) · `danger-surface` oklch(.95 .042 28) | `destructive` #b23c36 · tint #fde9e7 | `danger` oklch(53% .2 28)(tint 없음) | `error` oklch(70% .18 25) · `error-wash` |
| warning | oklch(50.9% .103 71) · tint oklch(96% .035 80) | — / `admin-warning` #8a5300 · tint #fdf3e3 | 동일 | `--color-yellow` oklch(68% .14 83) | oklch(.55 .135 68) · `warning-surface` | `warning` #95631a · tint #fbf0d9 | `warn` oklch(64% .16 72) | `warning` oklch(80% .15 82) · wash |
| success | oklch(46.9% .087 149) · tint oklch(95% .03 150) | `success-text` #1b873f · `success-bg` #e6f4ea / `admin-success` #177536 | 동일 | `--color-teal` oklch(55% .12 174)(비공식) | `--ok`=`success` oklch(.48 .13 151) · `success-surface` | `success` #27714e · tint #e7f3ec | `ok` oklch(54% .14 150) | (`mode-eco`, 모드 전용) |
| info | oklch(50% .16 258) · tint oklch(95.5% .025 255) | `legal-link` #428bff / `admin-info` #1c5fbd · tint #e8f0fc | 동일 | — | `--info` oklch(.5 .14 255)(tint 없음) | `info` #276ec5 · tint #e7f0fc | `info` oklch(56% .205 260) | — |
| overlay/scrim | `--overlay` oklch(30% .006 157 **/ .45**) — 유일한 alpha | `scrim` #000000, 렌더 시 `bg-scrim/50` | —(정의 없음) | — | `--color-overlay` oklch(.22 .024 244 / .42) | `overlay` rgb(29 40 35 / .5) | — | `overlay` oklch(7% .018 248) 불투명 |
| tint 계열 방식 | 불투명 `*-tint` 5종 | 사용자: `error-bg`/`success-bg`만 · admin: 불투명 tint 5종 | map 동일 | alpha soft | `*-surface` 3종 + brand-tint | 불투명 5종 | brand-tint만 | `*-wash` |

#### 3.2.2 다크 값(정의된 앱만)

| 역할 | map `.dark` | weather `.dark` | concierge `.dark` | airport `@media dark` | canview(항상) |
|---|---|---|---|---|---|
| surface-page | oklch(19% .006 150) | oklch(19% .025 255) | #151b17 | canvas oklch(18% .022 258) | oklch(10% .02 248) |
| card | oklch(23% .007 145) | oklch(23% .028 255) | #1d2721 | surface oklch(23% .026 258) · raised oklch(27% .03 258) | oklch(14% .026 246) |
| surface-subtle / muted | oklch(24% .008 145) / oklch(31% .012 145) | oklch(24% .03 255) / oklch(31% .04 255) | #243027 / #344238 | — | paper-3/4 |
| text-primary / secondary / tertiary | 93% / 78% / 68% (.006–.012, hue 155) | 93% / 78% / 68% (hue 255) | #e1e9e3 / #b1beb5 / #8f9d94 | ink oklch(96% .012 86) / muted oklch(76% .025 258) | ink 96% / ink-2 82% / muted 63% |
| control-line | oklch(58% .012 145) | oklch(58% .035 255) | #66756a | line ink/16% | — |
| brand / hover / tint / fg | oklch(76% .085 169) / 81% / oklch(31% .035 169) / oklch(20% .02 165) | oklch(76% .13 250) / 81% / oklch(31% .06 250) / oklch(20% .04 250) | #a78bfa / #ddd6fe / #3b1670 / #1e1b4b | accent oklch(72% .14 58) / strong oklch(78% .12 65) / soft 20% | accent oklch(72% .155 230) |
| status(success/warning/info/destructive) | 75%/77%/75%/72% · tint 28–30% | map과 동일 값 | #83c7a2 / #e0b15c / #84b8ff / #ec8881 · tint #1d3b2b/#47351a/#1d3048/#482321 | teal/red/yellow 76–82% | — |
| focus | oklch(80% .09 169) | oklch(80% .12 250) | #c4b5fd | (accent) | oklch(82% .145 226) |
| overlay | oklch(10% .006 157 / .6) | — | rgb(5 8 6 / .68) | — | — |

geo·pinvi·docker-manager는 다크 값이 없다. map·weather·concierge는 다크 값이 완비돼 있으나 셋 다 토글이 없어 실행 시 라이트만 렌더된다[사실]. airport는 OS 설정을 따르는 유일한 앱이다.

#### 3.2.3 shadcn alias 매핑 비교

| shadcn 변수 | map | weather | geo(`--ui-*`→) | concierge | airport WIP | pinvi DESIGN.md Exports(이식용) |
|---|---|---|---|---|---|---|
| `--background` | surface-page | surface-page | surface-page | surface-page | `--color-canvas` | paper |
| `--foreground` | text-primary | text-primary | **text-strong** | **text-strong** | ink | ink |
| `--card` | card | card | surface-card | surface-card | **surface-raised** | — |
| `--primary` | brand | brand | accent | brand | **button-bg** | cta |
| `--secondary` | surface-subtle | surface-subtle | surface-subtle | surface-subtle | **ink**(fg=canvas) | — |
| `--muted` / `-foreground` | surface-subtle / text-secondary | 동일 | surface-subtle / text-secondary | 동일 | (미정의) / muted | paper-2 / ink-2 |
| `--accent` / `-foreground` | brand-tint / brand | 동일 | **surface-muted / text-strong** | brand-tint / brand-ink | (미정의) / ink | — |
| `--border` | surface-muted(장식) | surface-muted | rule | line | line(alpha) | rule |
| `--input` | **control-line**(3:1 대상) | control-line | rule-strong | control-line | `--color-input`(**배경색** white/88%) | rule(=border) |
| `--ring` | focus | focus | accent | focus | accent | accent |
| `--destructive` | destructive | (미정의) | danger | destructive | red | — |
| `--radius` | radius-control 6px | radius-control | radius-control | **`--ktc-radius` 8px** | radius-control | 8px |

`--input`의 의미가 갈린다: map·weather·geo·concierge는 "컨트롤 경계선 색", airport WIP는 "입력 배경색"이다. `--accent`도 map 계열은 brand tint, geo는 surface-muted다. common이 shadcn alias까지 표준화하려면 이 두 항목의 의미를 먼저 고정해야 한다.

### 3.3 브랜드 톤 차이와 분리 가능 영역

| 앱 | 장르(문서) | 브랜드 hue(OKLCH) | paper 기조 | 출처 문서 |
|---|---|---|---|---|
| map | editorial-utilitarian, Rail-Workbench | 녹 h169 C.081 | 녹회색 tinted paper h128–157, 순백 금지 | `design.md` L9-14, L31-52 |
| pinvi 사용자 | modern-minimal | Rausch h17 C.231(CTA는 h18.5) | 순백 + 무채 회색(C 0), 순검정 금지 | DESIGN.md L250-274 |
| pinvi admin | map 구조 규약 + pinvi 색 | Rausch 계열(ink #c8093a, tint #ffeef1) | 순백/#f7f7f7/#f2f2f2 | `globals.css` L17-26 |
| weather | map Rail-Workbench 그대로 | 남 h255 C.14 | h250 청회색 paper | `design.md` L1-6, L19-25 |
| airport | modern-minimal workbench | 주황 h43 C.16(버튼 h38) | 웜 뉴트럴 h86 / 다크는 h258 블루차콜 | `design.md` L9-16 |
| geo | `design.md` "editorial-utilitarian" vs `globals.css` L2 스탬프 "modern-minimal"(**문서 불일치**) | 청 h262.9 C.215 | h262.9 냉색 paper | `design.md` L6-26 |
| concierge | editorial-utilitarian, map 구조 | 보라 #7c3aed(Tailwind violet-600), rail #2e1065 | 웜그레이/크림(#f4f5f0/#fcfcf9) | `design.md` L9-24 |
| docker-manager | editorial-utilitarian, Ember | 주황 h41 C.222(Tailwind orange-600 변환) | 웜 paper h41 | DESIGN.md L11-18; `tokens.css` L1-3 |
| canview | 현대 5W 내비 계열 | 시안 h230 C.155 | 남청 다크 전용 | `docs/ui/design.md` L112-126 |

각 앱 문서는 "구조·밀도·컴포넌트 언어는 map을 따르되 **색상톤은 유지**"를 명시한다(weather `design.md` L4-6, geo `design.md` L20-21, concierge `design.md` L16-17, docker-manager `docs/design-system.md` L16-17, pinvi `globals.css` L20-22 "사용자 요구가 색상톤 제외"). 따라서 사용자 전제 (4) "규칙도 common 산출물"은 색 **값**이 아니라 **역할·대비·형태 규칙**에 대해 성립한다.

공통 semantic 계약으로 분리 가능한 것(모든 admin 앱에서 이름 또는 값이 이미 일치):

| 항목 | 근거(수렴 상태) | 판정 |
|---|---|---|
| 표면 4단(page/subtle/muted/card) | map·weather·geo·concierge·pinvi admin·ktdm 전부 동일 역할명(이름 차이만: ktdm `elevated`, pinvi `soft/strong`) | 공통 계약 [후보] |
| 잉크 4단 + icon | 동일(geo·concierge는 `text-strong` 1단 추가; icon-default 매핑 단계는 map=tertiary, geo=secondary로 상이) | 공통 계약, `text-strong` 선택적 [후보] |
| hairline 2종(장식 `border` / 컨트롤 `control-line`) | map 규칙을 pinvi admin이 명시적으로 수입(`globals.css` L52-63), weather·geo·concierge도 `--control-line` 보유 | 공통 계약 + 3:1 규칙 [후보] |
| brand 4종(brand/hover/tint/foreground) + focus | 전 앱 보유(값은 앱별) | 이름은 공통, 값은 앱 오버라이드 |
| status 4종 + 불투명 tint | map·weather 값 동일; concierge·pinvi admin은 hex 대응값; geo `*-surface`, ktdm tint 없음, airport 색 이름(teal/red/yellow) | 이름·tint 규율 공통, 기본값은 map 제공 [후보] |
| radius 6/8, control 36/30, rail 22rem | 5개 앱 동일 | 공통 계약(admin 프로필) |
| 타입 7단(12/13.5/15/17/20/24/30) | map·geo·pinvi admin 동일, concierge xs만 13 | 공통 계약(admin 프로필) [후보] |
| 모션 2단 100/150 + ease 2종 | map·weather 동일, geo 100/150, concierge 120/180, ktdm 120/220 | 이름 공통, 값은 map 기본 [후보] |
| overlay 단일 alpha 규칙 | map·geo·concierge 보유, pinvi `bg-scrim/50` | 공통 계약 [후보] |

앱 고유로 남길 것: 브랜드 hue·채도·paper hue, pinvi 사용자 표면의 밀도(44px/16px/8·14px radius)와 어휘(canvas/ink/hairline/cta), airport의 16/10px·alpha 팔레트(WIP가 어디까지 map 규약을 받을지 [미확인]), docker-manager `graphite` 관찰 표면, concierge `shell-rail*`, canview 전부(제품군 밖).

### 3.4 토큰 운용 규칙 비교

#### 3.4.1 규칙 비교표

| 규칙 | map | pinvi | weather | airport | geo | concierge | docker-manager |
|---|---|---|---|---|---|---|---|
| WCAG 수치 문서화 | AA 4.5 텍스트 + 1.4.11 3:1(컨트롤 경계·focus), design.md에 24곳, globals 6곳; 네 표면 전부 재계산 요구 | C5 결정(Rausch 3.5 → cta 4.9), admin 토큰 실측 주석 | 없음 | 없음 | 없음 | 없음 | 없음 |
| focus 레시피 | `@layer base :focus-visible { outline: 2px solid var(--focus); offset 2px }` **단일 발행**, 컴포넌트 재선언 금지, 끄는 자리 닫힌 목록 4개, `outline-none` 전면 금지 | 사용자 `.focus-ring` utility(outline) · admin 컴포넌트별 `outline-focus`; base 규칙 없음 | 요소 선택자(`input,select,textarea,button,a`) outline 2px + `border-color` | `:where(button,input,select,summary,a)` outline 2px + `box-shadow` 3px α.30 | 컴포넌트별 `focus-visible:outline-2 outline-focus` + base `* { outline-color: color-mix(ring 50%) }`(반투명 기본) | base `:focus-visible` outline 2px **와** 컴포넌트 재선언 병존(`button.tsx` L9) | 요소 선택자 outline 2px brand |
| 링 전환 금지 | `transition-all/colors/transition` 금지(v4 전환 목록에 `outline-color`) | `.focus-ring` 주석 "outline은 transition에 안 묶여" | `transition:` 열거형 | — | — | 열거형 `transition-[color,…]` | `transition-all` 금지 문서화 |
| alpha 정책 | `--overlay`·shadow만 허용, 팔레트 `/NN` 금지(게이트 5) | 사용자 `bg-scrim/50` 허용, `bg-black/NN` ESLint 금지; admin은 불투명 tint | shadow만 | line/accent-soft/input/grid **모두 alpha** | overlay·shadow·color-mix(ring, sidebar) | overlay·shadow·color-mix(sidebar-border, scrollbar) | shadow만 |
| raw 색 금지 | `globals.css` 밖 `#hex/oklch(/rgb(` 금지(게이트 4) | 컴포넌트 hex 금지(styleseed L19) | 문서 없음; globals L2170-2283에 raw hex 17건(마커) | 문서 "not scattered hex"; globals 내 `white` 등 | DESIGN-RULES 10; `tailwind.config.ts`에 raw hex 잔존 | 문서 금지; globals fallback 블록에 hex 중복 | 문서 금지 |
| 흐림(disabled) | root opacity 금지, 자식 래퍼 `opacity-55`(게이트 7) | admin `button-variants.ts` L31-34 동일 규율 수입 | — | — | — | DESIGN-RULES "opacity 하나로만 숨기지 않는다" | — |
| reduced-motion | 전역 0.01ms + 스피너 예외(1.6s) + Skeleton 끔 | 전역 0.01ms | 전역 | 전역(L1836) | 전역 **0s**(visibility 버그 회피 주석) | 전역 + `.animate-spin` 1s 예외 | 전역 0.001ms |
| 집행 수단 | design.md §금지 패턴 7종 grep 게이트(**스크립트 위치 [미확인]** — scripts/CI/eslint에서 패턴 검색 0건) + `tests/unit/test_frontend_dependency_security.py::test_frontend_owns_every_named_shadcn_css_token_it_uses`(`@custom-variant` 소유 검증) + `eslint --max-warnings 0` | `apps/web/eslint.config.mjs` `no-restricted-syntax`(`bg-white|text-white|bg-black/`, `shadow-(sm..2xl)`) — 사용자 표면 한정 | 없음 | 없음(design.md Hallmark gate는 서술) | 없음 | 없음 | 없음 |

#### 3.4.2 대비 재검증

동일 계산기로 문서 수치를 재검증하고, 수치가 없는 앱의 핵심 쌍을 추가 계산했다. 허용 오차 ±0.03(8-bit 양자화·감마 차이). WCAG 기준: 본문 텍스트 4.5:1, 대형 텍스트·UI 컴포넌트 경계·focus 3:1.

| 앱 | 쌍 | 문서 | 계산 | 판정 |
|---|---|---|---|---|
| map | text-tertiary / page · text-secondary / page | 4.73 · 6.10 | 4.73 · 6.10 | 일치, AA 통과 |
| map | control-line / page · card · muted | 3.54 · 3.69 · 3.03 | 3.54 · 3.69 · 3.03 | 일치, 1.4.11 통과 |
| map | 장식 border / card | 1.22 | 1.22 | 일치(컨트롤 경계로 쓰면 미달 — 문서와 같은 결론) |
| map | focus / page(light · dark) | 6.66 · 10.26 | 6.66 · 10.26 | 일치 |
| map | brand fill / page · dark control-line / page | 5.08 · 4.33 | 5.08 · 4.33 | 일치 |
| pinvi | Rausch/white · cta/white · cta-hover/white | 3.5 · 4.9 · 5.9 | 3.52 · 4.89 · 5.91 | 일치 |
| pinvi | **hairline #dddddd / white** | **1.6** | **1.36** | 수치 불일치(결론 동일: 3:1 미달) |
| pinvi | **border-strong #c1c1c1 / white** | **2.7** | **1.80** | 수치 불일치(결론 동일: 3:1 미달) |
| pinvi admin | control-line #767676 / white · #f7f7f7 · #f2f2f2 | 4.54 · 4.24 · 4.06 | 4.54 · 4.24 · 4.06 | 일치 |
| pinvi admin | success #177536 / tint · 구 #1b873f / tint | 5.09 · 4.03 | 5.09 · 4.03 | 일치 |
| pinvi admin | Rausch / brand-tint #ffeef1 | 3.07 | 3.14 | 근사 일치 |
| weather | control-line / page · text-tertiary / page · focus / page · dark control-line / page | — | 3.55 · 4.74 · 7.69 · 4.32 | map과 같은 L값이라 통과 |
| concierge | **control-line #aab5ad / card #fcfcf9 · / page #f4f5f0** | — | **2.06 · 1.93** | 1.4.11 미달 |
| concierge | text-tertiary #7e8982 / card · text-secondary / page · focus / page · brand fill+white | — | **3.53** · 5.08 · 6.48 · 5.70 | tertiary 본문 AA 미달(대형 텍스트만 가능) |
| concierge dark | control-line #66756a / card | — | 3.16 | 통과 |
| geo | **control-line(rule-strong) / paper · paper-raised** | — | **2.29 · 2.41** | 1.4.11 미달 |
| geo | text-tertiary(muted-soft) / paper · text-secondary / paper · focus(=accent) / paper · accent fill+paper-raised | — | **3.66** · 5.33 · 4.81 · 5.05 | tertiary 본문 AA 미달 |
| docker-manager | line / card · **tertiary / card** · secondary / page · **brand fill+white** · warn / card | — | 1.47 · **3.82** · 5.99 · **3.59** · **3.45** | line은 장식이면 무관; tertiary·warn 본문 AA 미달; brand 채움 위 흰 라벨은 14px 600 기준 미달(18px+ bold 또는 24px+만 가능) |
| airport | **line(ink/14%) / canvas · / surface** · muted / canvas · accent / canvas · button-bg+white | — | **1.15 · 1.15** · 5.12 · 3.76 · 7.01 | `--input-border: var(--color-line)`이므로 입력 경계 1.4.11 미달 |
| airport dark | muted / canvas · line(ink/16%) / canvas | — | 8.77 · 3.52 | 통과 |
| canview | accent / paper · muted / paper · focus / paper · rule / paper | — | 8.67 · 5.90 · 12.02 · 1.46 | 참조용 |

정리: "컨트롤 경계 3:1" 규칙은 map이 세우고 weather(값 복사)·pinvi admin(재측정)이 지켰다. geo·concierge·docker-manager·airport는 `--control-line`/`--line`을 두었지만 값이 규칙을 만족하지 않는다. common이 규칙을 문서화만 하면 재발하므로, 계산기를 패키지에 포함해 CI에서 앱 오버라이드 값을 검사하는 방식이 필요하다[후보].

### 3.5 도메인 팔레트 소유권

| 팔레트 | 정의 위치 | 소비처 | 성격 | 판정 |
|---|---|---|---|---|
| pinvi `MARKER_PALETTE` P-01..P-16(Material 계열, P-01 `#E53935` 빨강 … P-13 `#757575` 회색=fallback) | `packages/design-tokens/src/colors.ts` L60-77; preset `marker.p-01..16`; 운영 규칙 `docs/design/marker-palette.md` | `packages/domain/src/marker.ts`(fallback resolver, "팔레트 데이터는 `@pinvi/design-tokens`가 단일 진실"), `PoiEditor.tsx`, `TripDayControls.tsx`; DB `app.trip_days.marker_color`, `custom_marker_color`(P-xx 문자열) | 데이터 카테고리 표현. 문서가 "CTA·nav·상태에 재사용 금지", "브랜드 확정 시 별도 ADR로 교체" 명시 | 도메인 팔레트. UI 토큰 패키지가 아니라 마커 데이터 계약의 일부 |
| map `PALETTE` P-01..P-16(Tableau 10 + 보강, P-01 `#1f77b4` 파랑 … P-13 `#6366f1` 남색; `DEFAULT_MARKER_COLOR` `#3b82f6`) | `packages/map-marker-react/src/palette.ts` L31-54(ADR-029/043, "PinVi user UI와 동일 매핑 공유" 의도, npm 게시 보류) | map admin `src/lib/feature-form-options.ts` L47-75(한글 이름 P-01 파랑 … P-13 남색), `map-marker-react` `createMarkerElement`; API `admin_features.py`·`curations.py`가 `^P-(0[1-9]\|1[0-6])$` 검증 | 코드 공간은 map API가 소유·검증 | 코드 공간 정본 = kor-travel-map |
| **충돌** | 같은 `P-xx` 코드에 hex·한글 이름이 전부 다르다. 예: P-01 map 파랑 `#1f77b4` / pinvi 빨강 `#E53935`; P-13 map 남색 `#6366f1` / pinvi 회색 `#757575`(pinvi fallback). pinvi는 `map-marker-react`를 import하지 않고(저장소 grep 0건, 문서 언급만), 요구사항 문서 §2.7이 "마커 매핑이 `@kor_travel_map/map-marker-react`와 같은 소스인지 보장(drift gate)"을 요청 상태로 남겨 두었다 | — | 같은 feature의 `marker_color`가 map admin과 pinvi에서 다른 색으로 렌더된다[사실, 코드 기준] | common 토큰 패키지가 해결할 문제가 아님. `marker_color` 데이터 소유자(map)가 hex 정본을 확정하고 pinvi가 소비하도록 정리해야 한다[후보] |
| map `--compare-a/--compare-b`(dedup·enrichment 비교 마커 쌍 = brand/info) | `globals.css` L125-126, L267-268; 소비 `dedup-review-client.tsx` L166-167 `resolveCssColorHex("--compare-a")` | map admin만 | UI semantic(비교 강조) | map admin 전용 UI 토큰. common의 "강조 쌍" 슬롯 후보로만 검토 |
| weather 마커 색(`.weather-marker-clear #d98b20` 등 + `.vworld-weather-marker … #ffa500` 등 **두 벌**) | `globals.css` L2170-2175, L2239-2244 | weather 지도 | 기상 상태 도메인 팔레트, 토큰화 안 됨 | weather 소유. weather 내부에서 토큰화 필요 |
| airport `--color-teal/red/yellow` | `tokens.css` L15-17 | 차트·상태 | 준-semantic(chart/status) | airport 소유; common status 이름으로 매핑 가능 |
| shadcn `--chart-1..5` | map(brand + 회녹 4단), concierge(brand + 회녹), airport WIP(teal/accent/yellow/red/muted) | 차트 | UI semantic 슬롯 | 슬롯 이름만 common, 값은 앱 |
| canview `--color-mode-sport/eco` | `tokens.css` L24-27 | 주행 모드 | 도메인 | 제품군 밖 |

판정: 마커 16색은 **소유권이 아니라 정본이 없는 상태**다. common은 (a) "카테고리 팔레트 계약"(16슬롯, `label_color` 규칙, 마커 위 라벨 AA)만 규칙 문서로 가지되, (b) hex 값은 kor-travel-map이 `marker_color` 스키마와 함께 배포(예: `map-marker-react` npm 게시 또는 `/v1/categories` 응답에 hex 포함)하고 pinvi `@pinvi/design-tokens`는 그것을 재수출하는 구조가 문서(pinvi `marker-palette.md` §4 "정본은 kor-travel-map /v1/categories")와 부합한다[후보]. 어느 hex 집합을 정본으로 할지는 [미확인].

### 3.6 common 토큰 패키지 초안

아래는 위 사실에서 도출한 제안이며 전부 [후보]다.

#### 3.6.1 변수 접두

| 후보 | 현황(전 저장소 `*.css/*.ts/*.tsx` grep) | 판단 |
|---|---|---|
| `--ktc-*` | concierge가 앱 전용 토큰으로 **125회** 사용(`--ktc-surface-page`, `--ktc-brand` 등, 값은 보라 팔레트) + `.ktc-workspace/.ktc-eyebrow` 클래스 | common이 같은 접두를 쓰면 concierge에서 "앱 전용"과 "common 계약"이 이름으로 구분되지 않는다. 다만 concierge의 `--ktc-*` 어휘는 제안 계약과 거의 같아, "concierge 값을 common 이름의 앱 오버라이드로 재해석"하면 마이그레이션 비용이 가장 낮다 |
| `--kt-*` | 0회 | 충돌 없음. `kor-travel` 약어로 자연스럽다 |
| `--ui-*` | geo 54회(shadcn alias 층) | 사용 불가 |
| `--pv-*` | 0회(pinvi는 `data-pv-surface` 속성만) | pinvi 전용 예약이 자연스러움 |

권고: 공통 semantic은 `--kt-*`, 앱 오버라이드 파일은 같은 이름을 재선언(접두 추가 없음), 앱 고유 확장은 앱 접두(`--ktc-shell-rail`, `--pv-*`)로 남긴다. 단, 사용자가 `--ktc-`를 지정했다면 concierge의 기존 이름을 common 계약으로 승격하는 경로(concierge `tokens.css`가 사실상 초안이 됨)도 성립하므로 결정을 요청한다(§5 Q1).

#### 3.6.2 계층

```
primitive   (선택) --kt-palette-*   앱이 자기 hue/ramp를 둘 자리. common은 기본값(map 값)만 제공
semantic    --kt-surface-page/subtle/muted/card · --kt-text-primary/secondary/tertiary/disabled · --kt-icon
            --kt-border(장식) · --kt-control-line(3:1) · --kt-brand/-hover/-tint/-foreground · --kt-focus
            --kt-success/-tint · --kt-warning/-tint · --kt-info/-tint · --kt-destructive/-tint · --kt-overlay
            --kt-radius-control/panel · --kt-control-h/-sm · --kt-rail · --kt-duration-fast/base · --kt-ease-out/in
            --kt-shadow-elevated/modal · --kt-z-nav/panel/overlay/modal/toast
component   shadcn alias(--background … --ring, --radius) = semantic 참조. 이름·의미 고정(§3.2.3의 `--input`=control-line, `--accent`=brand-tint)
```

primitive 계층을 공통이 강제하지 않는 이유: 어느 앱도 ramp(50~900) 기반이 아니고, 전부 "역할당 값 1개(+dark 1개)" 방식이다(§3.1.1). 계층은 "semantic ← app override" 두 단이 실제 사용 패턴이다.

#### 3.6.3 배포 형태와 Tailwind v4 연결

| 산출물 | 내용 | 소비자 | 근거 |
|---|---|---|---|
| `tokens.css` | `:root { --kt-*: <map 기본값> }` + `.dark { … }` 순수 CSS. Tailwind 의존 없음 | 전 앱(weather·airport main처럼 Tailwind 없는 앱 포함) | 선행 보고서 §7.3 "사전 빌드 CSS + CSS 변수 우선"과 일치 |
| `theme.css` | `@theme inline { --color-surface-page: var(--kt-surface-page); … --radius-control: var(--kt-radius-control); --spacing-control: var(--kt-control-h); --text-2xs…2xl }` + `@utility duration-fast/base` | Tailwind v4 앱이 `@import "tailwindcss"` 뒤에 import | map `globals.css` L71-209, geo L14-89, pinvi admin L27-88이 이미 이 형태. `@theme inline`은 변수 참조 시 Tailwind 문서가 권장하는 방식 |
| `shadcn.css` | `:root/.dark { --background: var(--kt-surface-page); … }` | shadcn 사용 앱(map·geo·concierge·pinvi admin·airport WIP) | §3.2.3 |
| `base.css`(선택) | `:focus-visible` 단일 레시피, hairline 2종, reduced-motion 전역(+스피너 예외), `button:not(:disabled){cursor:pointer}` | 원하는 앱만 | map L308-354, L430-457; pinvi L153-161 |
| `dark-class.css` / `dark-media.css` | `@custom-variant dark (&:is(.dark *))` 또는 `@media (prefers-color-scheme: dark)` 래퍼 | 앱이 하나 선택 | map·geo·concierge = class, airport = media |
| `tokens.json`(DTCG) + `tokens.ts` + `tailwind-preset.cjs` | 같은 값을 JSON/TS/v3 preset으로 내보내기 | pinvi mobile(NativeWind 4 + Tailwind 3.4.19, CSS `@theme` 불가), pinvi `design-tokens` 대체/재수출 | pinvi DESIGN.md L364-451, ktdm DESIGN.md L113-128이 DTCG·`@theme` 병기 형식을 이미 사용 |
| `kt-contrast`(스크립트) | 앱 오버라이드 파일을 읽어 §3.4.2 쌍을 계산, 3:1/4.5:1 미달이면 실패 | CI | map만 수동 검증 중; 다른 앱은 미달 상태(§3.4.2) |

`@config`(v3 JS config)와 `@theme`의 병합 우선순위는 [미확인]이므로, common `theme.css`는 `@config` 없이도 동작하는 `@theme inline`만 쓰고, geo·concierge·pinvi처럼 `@config`를 함께 쓰는 앱은 같은 utility 이름을 config에서 제거하는 마이그레이션 항목을 둔다.

#### 3.6.4 앱 브랜드 오버라이드

```css
/* apps/<app>/brand.css — common tokens.css 뒤에 import */
:root {
  --kt-brand: oklch(47% 0.14 255);            /* weather 예 */
  --kt-brand-hover: …; --kt-brand-tint: …; --kt-brand-foreground: …;
  --kt-focus: …;
  --kt-surface-page: …; /* paper hue를 바꾸는 앱만 (map h128–157, weather h250, geo h262.9, ktdm h41) */
}
.dark { … 같은 이름 … }
```

- 오버라이드 허용 목록을 계약으로 고정한다: brand 4종, focus, paper 4종, 잉크 4종(hue만 바꾸는 경우), status는 기본값 유지 권장(map·weather가 이미 같은 값). 형태·높이·타입·모션은 프로필(§3.6.5)로만 바꾼다.
- 오버라이드 후 `kt-contrast`를 통과해야 한다(map 규칙: 네 표면 전부에서 3:1·4.5:1 재계산).
- 값 형식은 OKLCH로 통일하되(6개 저장소가 이미 OKLCH), hex 앱(pinvi·concierge)은 변환값을 병기한다(pinvi DESIGN.md L263-272가 이미 hex/OKLCH 병기).

#### 3.6.5 프로필(밀도)

| 프로필 | radius | control | body | 스케일 | 적용 |
|---|---|---|---|---|---|
| `admin` | 6/8 | 36/30 | 15px | 12/13.5/15/17/20/24/30 | map·weather·geo·concierge·ktdm·pinvi admin·airport WIP(전환 시) |
| `consumer` | 8/14/20/32 | 44 터치 | 16px | 12/14/16/18/20/24/28/32/40 | pinvi 사용자 웹·모바일 |

두 프로필을 한 앱에서 섞을 때는 pinvi의 `[data-pv-surface='admin']` 변수 가리기 기법(`globals.css` L99-127)을 표준 예로 삼는다. 이 기법은 utility가 `var(--text-sm)`을 참조한다는 v4 동작에 의존하므로 `@theme inline`이 아닌 `@theme`(비inline)로 타입 스케일을 정의해야 한다[사실: pinvi 주석 L107-112; map은 `@theme inline`이지만 값이 리터럴이라 영향 없음].

#### 3.6.6 다크 모드 전략

- 사실: 다크 값을 가진 앱(map·weather·concierge)도 토글이 없고, airport만 OS 설정을 따른다. geo·pinvi·ktdm은 다크 값이 없다.
- 제안: 계약상 모든 semantic 토큰은 `.dark` 값을 **가져야** 하되(map 값을 기본 제공), 활성화는 앱 선택(`dark-class.css` vs `dark-media.css`). 토글이 없는 앱은 `color-scheme: light`를 선언해 media 변형이 우연히 켜지지 않게 한다(airport `globals.css` L5가 `color-scheme` 선언의 예). 다크 대비 검증은 `kt-contrast`가 light와 같은 쌍으로 수행한다(map design.md L65-66, L72가 이미 dark 수치를 병기).

#### 3.6.7 버전 일치 전제와의 관계

- Tailwind: v4 앱 5개는 4.3.1~4.3.3(설치)로 근접하다. weather·airport main은 Tailwind가 없고, airport WIP는 4.3.3을 요구한다. pinvi mobile은 NativeWind 4 + Tailwind 3.4.19라 v4 전환 대상이 아니며(RN), TS/JSON 토큰 출력이 필요하다.
- React: geo·ktdm 18.3.1, 나머지 19.x. 토큰 패키지는 React 무관이라 이 격차의 영향을 받지 않는다(UI 패키지와 분리해야 하는 이유).
- shadcn: map·geo·concierge·airport WIP는 `style: base-nova`(components.json), pinvi admin은 base-ui 기반 자체 포팅. `shadcn.css` alias는 이 스타일이 참조하는 변수 이름 집합에 맞춘다.

## 4. 선행 검토 보고서와의 차이

선행 보고서(`docs/kor-travel-common-library-review.md`, 2026-09-05)의 관련 주장을 재검증했다.

| 선행 보고서 주장 | 이번 조사 결과 |
|---|---|
| §2 표: weather는 "Tailwind 직접 의존성 없음" | 일치(`package.json`에 tailwind 없음, `globals.css`는 순수 CSS) |
| §2 표: 버전은 `package.json` 요구 범위만 | lockfile 설치 버전을 추가 확인(§1 표). pinvi 루트 lock의 `tailwindcss` 3.4.19는 mobile용이고 web은 `apps/web/node_modules/tailwindcss` 4.3.3 |
| §3.5 "공유할 것은 surface/text/border/danger/focus 같은 의미와 크기 규약, 브랜드 값은 앱" | 일치. 추가로 hairline 2종 분리, 불투명 tint, focus 단일 레시피, 대비 수치 검증이 공유 대상임을 확인(§3.3, §3.4) |
| §7.1 "토큰 패키지에 폰트 강제 로딩 포함하지 않음" | 지지. 현재 weather·airport·geo·ktdm은 문서상 폰트를 지정만 하고 로딩 코드가 없다(§3.1.4) — 로딩은 앱 책임으로 두되, 스택 문자열은 common이 제공할 수 있다 |
| §7.3 "CSS 변수와 클래스에 공통 접두사" | 지지하되, 접두 `--ktc-`는 concierge와 충돌한다는 사실을 추가(§3.6.1) |
| 언급 없음 | 마커 팔레트 P-xx의 map/pinvi 이중 정의(§3.5), geo·concierge·ktdm·airport 컨트롤 경계 3:1 미달(§3.4.2), pinvi hairline 수치 오기(§3.4.2), geo `@config` raw hex 잔존(§3.1.1) — 선행 보고서 범위 밖 |

결론이 달라진 항목은 없다. 선행 보고서는 "브랜드 값은 앱 소유"를 원칙으로 적었고, 이번 조사는 그 원칙을 파일 단위 값과 대비 수치로 뒷받침했다.

## 5. 열린 질문

1. **접두 결정**: `--ktc-`(concierge 기존 이름을 common 계약으로 승격) vs `--kt-`(신규, 충돌 0). 사용자 지시에 예시로 `--ktc-*`가 있으나 concierge 충돌을 알고 지정한 것인지 [미확인].
2. **마커 팔레트 정본**: P-01..P-16의 hex를 map(Tableau) / pinvi(Material) 중 어느 쪽으로 확정할지, 그리고 `map-marker-react` npm 게시 보류(ADR-043)를 해제할지. 이 결정 없이는 common이 "카테고리 팔레트 규칙"만 가질 수 있다.
3. **`@config`와 `@theme` 병합 우선순위**: geo(`brand: "#2563eb"` vs `--color-brand: var(--brand)`)에서 어느 값이 utility에 들어가는지 빌드 산출물로 확인 필요([미확인], `.next`는 조사 범위 밖).
4. **map 금지 패턴 게이트 스크립트**: design.md가 "스크립트는 이 목록을 따른다"고 하나 저장소에서 위치를 찾지 못했다. 로컬 훅인지, 삭제됐는지 [미확인].
5. **airport WIP의 방향**: `codex/shadcn-ui-foundation`은 shadcn 변수를 자체 `--color-*`에 배선했고 `tokens.css`는 그대로다(16/10px radius, alpha line 유지). map 규약(6/8, 3:1 control-line)으로 수렴할지 airport 고유로 둘지.
6. **다크 모드 활성화 여부**: 값을 유지하는 세 앱이 토글을 도입할 계획이 있는지. 없다면 계약에서 dark를 "정의 필수, 검증 선택"으로 낮출지.
7. **pinvi 사용자 표면 포함 범위**: 사용자 지시 (3)은 PinVi Admin을 포함한다. 사용자 웹·모바일(consumer 프로필)까지 common 토큰을 적용할지는 선행 보고서(§1 "첫 이관 대상에서 제외")와 이번 조사 모두 결정하지 않았다.
8. **폰트 로딩 책임**: Pretendard npm 로딩(map·pinvi·concierge)과 미로딩(weather·airport·geo·ktdm)이 갈린다. common이 `--kt-font-sans` 스택 문자열과 함께 "로딩은 앱이, 스택은 common이" 규칙을 둘지.
9. **docker-manager의 Next 14 / React 18**: 토큰 CSS는 무관하지만 `theme.css`가 v4 전용이므로, ktdm이 Tailwind 4.3.1을 이미 쓰는 점을 감안하면 토큰 도입은 가능하다. 문서 드리프트(Space Grotesk 등)는 ktdm 쪽 정리 항목.

## 6. 근거 파일 목록

kor-travel-map (`c494e227`)
- `packages/kor-travel-map-admin/frontend/src/app/globals.css`
- `packages/kor-travel-map-admin/frontend/design.md`
- `docs/architecture/admin-frontend-design-rules.md`
- `packages/kor-travel-map-admin/frontend/components.json`
- `packages/kor-travel-map-admin/frontend/package.json`, `package-lock.json`(루트)
- `packages/kor-travel-map-admin/frontend/src/app/layout.tsx`
- `packages/kor-travel-map-admin/frontend/src/lib/status-label.ts`
- `packages/kor-travel-map-admin/frontend/src/lib/feature-form-options.ts`
- `packages/kor-travel-map-admin/frontend/src/app/admin/dedup-reviews/dedup-review-client.tsx`
- `packages/kor-travel-map-admin/frontend/src/components/ui/sonner.tsx`
- `packages/map-marker-react/src/palette.ts`, `packages/map-marker-react/src/index.ts`, `packages/map-marker-react/package.json`
- `packages/kor-travel-map-api/src/kortravelmap/api/routers/admin_features.py`, `curations.py`, `categories.py`
- `tests/unit/test_frontend_dependency_security.py`
- `docs/reports/hallmark-audit-admin-frontend-2026-08-18.md`(존재 확인만)

pinvi (`9af25e5`)
- `packages/design-tokens/src/colors.ts`, `spacing.ts`, `typography.ts`, `motion.ts`, `index.ts`
- `packages/design-tokens/tailwind-preset.cjs`, `packages/design-tokens/package.json`
- `apps/web/app/globals.css`, `apps/web/tailwind.config.ts`, `apps/web/postcss.config.mjs`
- `apps/web/app/(admin)/layout.tsx`
- `apps/web/eslint.config.mjs`
- `apps/web/components/ui/Button.tsx`, `apps/web/components/admin/ui/button-variants.ts`
- `apps/mobile/tailwind.config.js`, `apps/mobile/components/ui.tsx`
- `packages/domain/src/marker.ts`, `packages/domain/src/marker.test.ts`
- `DESIGN.md`
- `docs/design/marker-palette.md`, `docs/design/styleseed-rules.md`
- `docs/architecture/map-marker-design.md`, `docs/kor-travel-map-requirements.md`
- `package-lock.json`

kor-travel-weather (`6003da9`)
- `packages/kor-travel-weather-admin/frontend/app/tokens.css`
- `packages/kor-travel-weather-admin/frontend/app/globals.css`
- `packages/kor-travel-weather-admin/frontend/design.md`
- `packages/kor-travel-weather-admin/frontend/app/layout.tsx`
- `packages/kor-travel-weather-admin/frontend/package.json`, `package-lock.json`

kor-travel-airport (`2bb1111`, WIP `99b3f98`)
- `frontend/src/app/tokens.css`
- `frontend/src/app/globals.css`(main 및 `codex/shadcn-ui-foundation`)
- `design.md`
- `frontend/src/app/layout.tsx`
- `frontend/package.json`(main 및 WIP diff), `frontend/package-lock.json`
- `frontend/components.json`(WIP)

kor-travel-geo (`1d9d74d`)
- `kor-travel-geo-ui/app/globals.css`
- `kor-travel-geo-ui/tailwind.config.ts`, `kor-travel-geo-ui/components.json`, `kor-travel-geo-ui/postcss.config.mjs`
- `design.md`
- `kor-travel-geo-ui/docs/DESIGN-RULES.md`
- `kor-travel-geo-ui/app/layout.tsx`
- `kor-travel-geo-ui/components/ui/button.tsx`
- `kor-travel-geo-ui/package.json`, `kor-travel-geo-ui/package-lock.json`
- `docs/kor-travel-common-library-review.md`(선행 보고서)

kor-travel-concierge (`7945305`)
- `frontend/tokens.css`
- `frontend/src/app/globals.css`
- `frontend/tailwind.config.ts`, `frontend/components.json`, `frontend/postcss.config.mjs`
- `design.md`
- `frontend/docs/DESIGN-RULES.md`
- `frontend/src/app/layout.tsx`
- `frontend/src/components/ui/button.tsx`
- `frontend/package.json`, `frontend/package-lock.json`

kor-travel-docker-manager (`862562d`)
- `frontend/tokens.css`
- `frontend/src/app/globals.css`
- `DESIGN.md`
- `docs/design-system.md`
- `docs/DESIGN-RULES.md`
- `frontend/src/app/layout.tsx`
- `frontend/package.json`, `frontend/package-lock.json`

canview (`d078437`, 참조)
- `tokens.css`
- `docs/ui/design.md`
