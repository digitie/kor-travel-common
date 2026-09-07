# 디자인 토큰 계약(`--kt-*`) — 색상 톤·형태·모션 규칙

- 정본 지위: 이 문서는 `@kor-travel/tokens`가 배포하는 토큰의 **이름·의미·계층·검사 규칙**의 정본이다. 토큰 **값**의 정본은 `packages/tokens/tokens.css`이며(TK-1), 이 문서의 값 표는 요약이다. 색 값 자체(브랜드 hue·paper hue)는 앱이 소유한다(TK-8).
- 확정 task: **T-104**(실물 `packages/tokens`, T-101과 대조해 확정). 이 판은 브리프 D-10·D-12·D-13·D-26을 규칙 ID로 옮긴 초안이다. 마지막 갱신: 2026-09-06.
- 근거 약칭: `dt` = [design-tokens 조사](../survey/cross/design-tokens.md), `ux` = [ux-patterns 조사](../survey/cross/ux-patterns.md), `ui` = [ui-components 조사](../survey/cross/ui-components.md), `inv/<app>` = [인벤토리](../survey/README.md) §3.1. 결정 ID(D-nn·O-nn)는 [설계 브리프](../plan/design-brief.md).

## 1. 목표와 기준

| 항목 | 내용 | 근거 |
|---|---|---|
| common이 소유하는 것 | 토큰 **이름·의미·계층·밀도 프로필·대비 규칙·alpha 정책·shadcn alias 의미·정본 파일 형식** | `dt` §3.3(5개 앱 문서가 "구조는 map, 색상 톤은 유지" 선언), D-12 |
| 앱이 소유하는 것 | 브랜드 4종·focus·paper·ink·status 값(오버라이드 허용 목록 안에서), 다크 값 여부, 폰트 로딩, 도메인 팔레트(마커·차트·기상 상태) | `dt` §3.3·§3.5, D-12·D-26 |
| 기본값 원형 | kor-travel-map admin `globals.css`(`c494e227`) 값. 5개 앱이 이미 형태(6/8px·36/30px)와 역할 이름을 이식했다 | `dt` §0·§3.1.2 |
| 사실 표기 | 별도 표기 없는 값·수치는 `dt` §3.1~§3.4에서 확인한 사실. "후보"는 T-101 실물에서 확정 | — |

## 2. 정본 파일과 생성물

**TK-1 (MUST)** 토큰 값의 정본은 `packages/tokens/tokens.css` 하나다. `tokens.json`(DTCG)·`tokens.ts`·`tailwind-preset.cjs`는 빌드 생성물이며, CI가 생성물을 재생성해 diff 0을 검사한다. 정본과 생성물을 수동으로 어긋나게 두지 않는다(canview A6.1 대응, [canview 체크리스트](../survey/cross/canview-structure-checklist.md) §2.6).

| 파일 | 내용 | 소비자 | Tailwind 의존 |
|---|---|---|---|
| `tokens.css` | `:root { --kt-*: <map 기본값>; color-scheme: light }` + `.dark { --kt-*: <map dark 값> }` 순수 CSS | 전 앱(Tailwind 없는 앱 포함) | 없음 |
| `theme.css` | `@theme`/`@theme inline`으로 `--kt-*`를 Tailwind v4 네임스페이스(`--color-kt-*`·`--spacing-kt-*`·`--radius-kt-*`·`--text-kt-*`·`--font-kt-*`·`--ease-kt-*`·`--shadow-kt-*`)에 연결 + `@utility duration-kt-*`·`z-kt-*` | Tailwind v4 앱 | v4 |
| `shadcn.css` | `:root/.dark { --background: var(--kt-surface-page); … }` alias(TK-6) | shadcn 사용 앱 | 없음 |
| `base.css` | `:focus-visible` 단일 레시피, hairline 2종 유틸, reduced-motion 전역(+스피너 예외), `button:not(:disabled){cursor:pointer}` | 원하는 앱 | 없음 |
| `base.scoped.css` | `base.css`와 같은 규칙을 `[data-kt-surface]` 하위에만 적용 | 사용자 표면과 admin이 한 앱에 공존하는 앱(pinvi) | 없음 |
| `dark-class.css` / `dark-media.css` | 다크 활성화 파일(TK-9). 앱이 하나만 import | 다크 활성 앱 | v4 class variant / 기본 media variant |
| `aliases/map-vocabulary.css` | 레거시 어휘 별칭 shim(TK-16) | map·weather·geo 이관 기간 | 없음 |
| `tokens.json` / `tokens.ts` / `tailwind-preset.cjs` | 생성물. DTCG JSON, TS 상수, Tailwind v3 preset(NativeWind) | pinvi mobile·`@pinvi/design-tokens` 재수출, 도구 | — |

파일 경로는 공개 계약이다. 경로 변경은 SemVer 0.x 파괴 항목이다([ui-contract](ui-contract.md) §9).

## 3. 네임스페이스

**TK-2 (MUST)** 공통 semantic 변수 접두는 `--kt-*`, Tailwind 유틸리티 접두는 `kt-`(`bg-kt-surface-page`, `h-kt-control`, `rounded-kt-control`, `text-kt-2xs`)다. 전 저장소 `*.css/*.ts/*.tsx`에서 0회 사용이라 충돌이 없다(`dt` §3.6.1). 앱 오버라이드는 **같은 이름을 재선언**하며 접두를 덧붙이지 않는다. 앱 고유 확장은 앱 접두(`--ktc-*`·`--pv-*`·`--color-admin-*`·`--ui-*`)로 앱 파일에 둔다.

- 열림 O-4(사용자 확인 필요): 네임스페이스는 기본값 `kt-`/`--kt-*`로 진행한다. `--ktc-*`는 concierge가 앱 전용 이름으로 125회 쓰고 있어 채택하지 않는다(`dt` §3.6.1).
- 금지: `--ui-*`(geo shadcn alias 층 54회), `--color-<역할>` 무접두(shadcn `base-nova` 기본명·pinvi 사용자 preset과 충돌).

## 4. 계층

**TK-3 (MUST)** 계층은 **semantic ← app override** 2단이다. primitive ramp(50~900)는 강제하지 않는다(어느 앱도 ramp 기반이 아니고 "역할당 값 1개 + dark 1개" 방식, `dt` §3.6.2). component 계층은 shadcn alias(TK-6)이며 semantic을 참조만 한다.

```text
semantic    --kt-*                          common tokens.css(기본값) ← 앱 brand.css(같은 이름 재선언)
component   --background … --ring, --radius  shadcn.css = semantic 참조(이름·의미 고정)
utility     kt-*                             theme.css @theme = semantic 참조
```

앱 CSS에서 semantic 토큰을 건너뛰고 component alias만 재선언하는 것은 금지한다(alias는 파생값이어야 `kt_contrast`가 검사할 수 있다).

## 5. 역할 목록

**TK-4 (MUST)** 아래 역할·이름을 전부 정의한다. 값은 `tokens.css`가 정본이고 "기본값(light)" 열은 map 원형의 요약이다(`dt` §3.2.1). "대비" 열은 §9 검사 대상 여부, "오버라이드" 열은 §7 허용 여부다.

### 5.1 색

| 역할 | 변수 | 의미 | 기본값(light, map) | 대비 | 오버라이드 |
|---|---|---|---|---|---|
| surface page | `--kt-surface-page` | 문서 배경 | `oklch(97.8% 0.003 128)` | 배경 | 허용(paper) |
| surface subtle | `--kt-surface-subtle` | 행 hover·툴바·secondary 버튼 배경 | `oklch(96.7% 0.006 138)` | 배경 | 허용(paper) |
| surface muted | `--kt-surface-muted` | 선택 행·장식 border 값의 원천 | `oklch(92.5% 0.01 141)` | 배경 | 허용(paper) |
| surface card | `--kt-surface-card` | 카드·패널·팝업 배경 | `oklch(99.2% 0.002 140)` | 배경 | 허용(paper) |
| text primary | `--kt-text-primary` | 본문 | `oklch(30% 0.006 157)` | 4.5:1 | 허용(ink) |
| text secondary | `--kt-text-secondary` | 보조 본문·라벨 | `oklch(48% 0.012 159)` | 4.5:1 | 허용(ink) |
| text tertiary | `--kt-text-tertiary` | 메타·캡션 | `oklch(54% 0.012 154)` | 4.5:1 | 허용(ink) |
| text disabled | `--kt-text-disabled` | 비활성 라벨(대비 검사 제외) | `oklch(79% 0.012 154)` | 제외 | 허용(ink) |
| text strong(선택) | `--kt-text-strong` | 제목 강조. 미정의 시 `--kt-text-primary` | (= primary) | 4.5:1 | 허용(ink) |
| icon | `--kt-icon` | 기본 아이콘 색(map: tertiary 값) | `var(--kt-text-tertiary)` | 3:1 | 파생 |
| border(장식) | `--kt-border` | hairline·구분선. **컨트롤 경계에 쓰지 않는다** | `var(--kt-surface-muted)` | 제외 | 파생 |
| control line | `--kt-control-line` | 입력·버튼 경계(WCAG 1.4.11) | `oklch(61% 0.012 145)` | 3:1 | 허용(ink 계열) |
| brand | `--kt-brand` | 채움 CTA·활성 mark·링크 | `oklch(51.4% 0.081 169)` | 채움+foreground 4.5:1 | 허용(brand) |
| brand hover | `--kt-brand-hover` | brand hover/active | `oklch(46% 0.085 169)` | 4.5:1 | 허용(brand) |
| brand tint | `--kt-brand-tint` | 활성 nav·선택 행 배경(불투명) | `oklch(95.2% 0.013 172)` | brand/tint 3:1 | 허용(brand) |
| brand foreground | `--kt-brand-foreground` | brand 채움 위 글자 | `oklch(99% 0.002 140)` | 4.5:1 | 허용(brand) |
| focus | `--kt-focus` | 포커스 링(불투명) | `oklch(45% 0.09 169)` | page 대비 3:1 | 허용 |
| success / tint | `--kt-success`, `--kt-success-tint` | 활성·완료 | `oklch(46.9% 0.087 149)` / `oklch(95% 0.03 150)` | 텍스트 4.5:1(tint 위·page 위) | 허용(status) |
| warning / tint | `--kt-warning`, `--kt-warning-tint` | 사람 결정 대기·저하 | `oklch(50.9% 0.103 71)` / `oklch(96% 0.035 80)` | 4.5:1 | 허용(status) |
| info / tint | `--kt-info`, `--kt-info-tint` | 정보·기계 진행 중 | `oklch(50% 0.16 258)` / `oklch(95.5% 0.025 255)` | 4.5:1 | 허용(status) |
| destructive / tint | `--kt-destructive`, `--kt-destructive-tint` | 실제 오류·파괴 행동 | `oklch(51.4% 0.167 27)` / `oklch(96% 0.03 25)` | 4.5:1 | 허용(status) |
| overlay | `--kt-overlay` | 모달 backdrop. **유일한 alpha 색** | `oklch(30% 0.006 157 / 0.45)` | 제외 | 파생 |

상태 tone 5종(success/warning/destructive/info/neutral)의 의미는 [ux-guide](ux-guide.md) UX-G5.1이 정본이다. `neutral`은 별도 토큰 없이 `--kt-text-secondary`/`--kt-surface-subtle`로 렌더한다.

### 5.2 형태·밀도·모션·층

| 역할 | 변수 | admin 기본값 | 비고 |
|---|---|---|---|
| radius control | `--kt-radius-control` | 6px | 버튼·입력·배지. shadcn `--radius`의 원천 |
| radius panel | `--kt-radius-panel` | 8px | 카드·팝업·다이얼로그 |
| control 높이 | `--kt-control-h`, `--kt-control-h-sm` | 36px / 30px | `h-kt-control`, `h-kt-control-sm`. micro-control 예외는 [ux-guide](ux-guide.md) UX-G9.7 |
| rail | `--kt-rail` | 22rem | 우측 inspector rail 폭(`xl` 이상). weather 17rem은 앱 오버라이드(§7 예외) |
| duration | `--kt-duration-fast`, `--kt-duration-base` | 100ms / 150ms | `@utility duration-kt-fast/base` |
| ease | `--kt-ease-out`, `--kt-ease-in` | `cubic-bezier(0.16,1,0.3,1)` / `cubic-bezier(0.7,0,0.84,0)` | |
| shadow | `--kt-shadow-elevated`, `--kt-shadow-modal` | `0 4px 12px oklch(… / 0.10)` / `0 8px 24px oklch(… / 0.14)` | rest 상태는 hairline만, 그림자는 오버레이 전용(`dt` §3.1.7) |
| z-index | `--kt-z-nav`, `--kt-z-panel`, `--kt-z-overlay`, `--kt-z-modal`, `--kt-z-toast` | 30 / 40 / 50 / 60 / 70(후보, pinvi 값) | 임의 `z-[N]` 금지. 값은 T-101 확정 |
| font | `--kt-font-sans`, `--kt-font-mono` | §10 | 스택 문자열만. 로딩은 앱 |

### 5.3 타입 스케일

**TK-5 (MUST)** admin 프로필 스케일은 7단 `2xs/xs/sm/md/lg/xl/2xl` = 12 / 13.5 / 15 / 17 / 20 / 24 / 30px, 본문 `sm`(15px)이다(`dt` §3.1.4: map·geo·pinvi admin 동일, concierge xs 13은 이관 시 정렬). `theme.css`는 스케일을 **비inline `@theme`**(`--text-kt-<step>`, `--text-kt-<step>--line-height`)로 정의해 유틸리티가 `var()`를 참조하게 한다. 그래야 pinvi처럼 한 앱에서 스코프별로 변수만 가려 다른 밀도를 렌더할 수 있다(`dt` §3.6.5 사실). 임의값 `text-[Npx]`는 금지 패턴이다([ux-guide](ux-guide.md) §4).

## 6. shadcn alias 의미 고정

**TK-6 (MUST)** `shadcn.css`가 배포하는 alias의 의미를 아래로 고정한다. 앱은 alias를 직접 값으로 재선언하지 않는다(TK-3). 조사에서 갈렸던 두 항목(`--input`, `--accent`)은 map 계열 의미를 채택한다(`dt` §3.2.3, D-12).

| shadcn 변수 | = semantic | 의미 | 조사에서의 편차(이관 시 정정) |
|---|---|---|---|
| `--background` / `--foreground` | surface-page / text-primary | 문서 배경·본문 | geo·concierge는 foreground=text-strong → strong을 선택 정의하면 동일 |
| `--card` / `--card-foreground` | surface-card / text-primary | | airport WIP `surface-raised` → card로 재매핑(T-431) |
| `--popover` / `--popover-foreground` | surface-card / text-primary | | |
| `--primary` / `--primary-foreground` | brand / brand-foreground | 채움 CTA | airport WIP `button-bg` → brand |
| `--secondary` / `--secondary-foreground` | surface-subtle / text-primary | | airport WIP `ink` 채움 → 정정 |
| `--muted` / `--muted-foreground` | surface-subtle / text-secondary | | |
| `--accent` / `--accent-foreground` | **brand-tint** / brand | 활성·hover tint | geo `surface-muted / text-strong` → 정정(T-441) |
| `--border` | **border(장식)** | hairline | airport `line`(alpha) → 장식 전용으로 격하, 컨트롤 경계는 `--input` |
| `--input` | **control-line** | 컨트롤 경계선 색(3:1 대상) | airport WIP는 입력 **배경색**으로 씀 → 재매핑 필수(T-431) |
| `--ring` | focus | | |
| `--destructive` | destructive | | weather 미정의 → shim 제공 |
| `--radius` | radius-control(6px) | | concierge 8px → 이관 시 6px(T-453) |
| `--chart-1..5` | 앱 소유 | 슬롯 이름만 공통 | `dt` §3.5 |

## 7. 프로필과 오버라이드

### 7.1 프로필

**TK-7 (MUST)** 밀도 프로필은 2종이다. common은 `admin` 값을 배포하고 `consumer`는 **의미 이름과 문서만** 제공한다(값·밀도는 pinvi 소유, D-29).

| 프로필 | radius | control 높이 | 본문 | 스케일 | 적용 | 근거 |
|---|---|---|---|---|---|---|
| `admin` | 6 / 8px | 36 / 30px | 15px | 7단(§5.3) | map·weather·geo·concierge·ktdm·pinvi admin·airport(WIP 병합 후 전환 시) | `dt` §3.6.5 |
| `consumer` | 8 / 14 / 20 / 32px | 44px 터치 | 16px(입력 포함) | 9단 12~40(pinvi 현재값, 참고) | pinvi 사용자 웹·모바일 | `dt` §3.6.5, pinvi `DESIGN.md` |

한 앱에서 두 프로필을 섞을 때는 스코프 셀렉터(pinvi `[data-pv-surface='admin']`, common 권장 `[data-kt-surface="admin"]`) 안에서 형태·스케일 변수만 재선언한다. `base.scoped.css`가 같은 셀렉터를 쓴다.

### 7.2 오버라이드 허용 목록

**TK-8 (MUST)** 앱 오버라이드 파일(권장 이름 `brand.css`, `tokens.css` 뒤에 import)이 재선언할 수 있는 토큰은 아래뿐이다. 형태·높이·타입·모션·z·shadow는 프로필로만 바뀐다(개별 오버라이드 금지).

| 그룹 | 토큰 | 조건 |
|---|---|---|
| brand 4 | `--kt-brand`, `-hover`, `-tint`, `-foreground` | 대비 검사 통과(§9) |
| focus | `--kt-focus` | page 대비 3:1 |
| paper 4 | `--kt-surface-page/subtle/muted/card` | hue만 바꾸는 용도(map h128~157, weather h250, geo h262.9, ktdm h41) |
| ink 4 | `--kt-text-primary/secondary/tertiary/disabled`(+`-strong`) | paper hue에 맞춘 hue 조정 |
| status 4 + tint | `--kt-success/warning/info/destructive`(+`-tint`) | 기본값 유지 권장(map·weather 동일 값); 바꾸면 검사 대상 |
| control line | `--kt-control-line` | 3:1 검사 |
| font 스택 | `--kt-font-sans`, `--kt-font-mono` | §10 |
| 앱 확장 | 앱 접두(`--ktc-shell-rail*`, `--pv-*` 등) | 앱 파일에만 |

등록된 예외: weather `--kt-rail: 17rem`(`inv/weather` §3.1, 이관 T-461 동반), pinvi admin 44px 2쪽(O-21, [responsive-web](responsive-web.md) §4). 그 외 형태 값 오버라이드는 매니페스트 `exceptions[]`에 `until`과 함께 등록해야 한다.

```css
/* apps/<app>/brand.css — @import "@kor-travel/tokens/tokens.css" 뒤 */
:root {
  --kt-brand: oklch(47% 0.14 255);            /* weather 예: 남색 */
  --kt-brand-hover: oklch(41% 0.15 255);
  --kt-brand-tint: oklch(95% 0.025 250);
  --kt-brand-foreground: oklch(99% 0.002 250);
  --kt-focus: oklch(43% 0.13 255);
}
.dark { /* 선택: 같은 이름만 */ }
```

## 8. 다크 모드

**TK-9 (MUST)** `tokens.css`는 모든 semantic 색 토큰의 `.dark` 값을 **완비**한다(map 기본, `dt` §3.2.2). 활성화는 앱 선택이다.

| 항목 | 규칙 |
|---|---|
| 기본 | `tokens.css`가 `:root { color-scheme: light }`를 선언한다. 토글 없는 앱에서 media 변형이 우연히 켜지지 않는다(airport `globals.css` 선례) |
| 활성화 | `dark-class.css`(`.dark { color-scheme: dark }` + `@custom-variant dark (&:is(.dark *))`) 또는 `dark-media.css`(`@media (prefers-color-scheme: dark)` 아래 같은 dark 값 재선언 + Tailwind v4 기본 media `dark` variant 유지) 중 **하나만** 명시 import. 둘 다 import 금지 |
| 앱 오버라이드의 dark 값 | 선택. 미정의 시 map dark 값이 그 역할에 적용되므로 브랜드 오버라이드 앱은 dark 활성 전에 4종 이상을 정의해야 한다 |
| 검사 | dark 쌍 대비 검사는 dark 활성 앱(매니페스트 `contrast.dark: true`)만(§9) |
| 열림 O-11 | "정의 필수(map 기본)·활성화 opt-in·앱 오버라이드 dark 선택"이 기본값. 사용자 확인 필요 |

## 9. 값 형식·alpha·raw 색·대비

**TK-10 (SHOULD)** 값 형식은 OKLCH(`oklch(L% C H)`)를 권고하고 hex를 허용한다. hex 앱(pinvi·concierge)은 오버라이드 파일 주석에 OKLCH 변환값을 병기한다(`dt` §3.6.4). `tokens.css` 기본값은 OKLCH다.

**TK-11 (MUST)** alpha는 `--kt-overlay`와 shadow 토큰에만 허용한다. status·brand tint는 **불투명**이다. 컴포넌트 클래스에서 팔레트 alpha(`bg-kt-brand/40`, `bg-black/50`)를 쓰지 않는다. `color-mix()`는 앱 토큰 파일에서 파생 토큰을 만들 때만(컴포넌트 금지).

**TK-12 (MUST)** raw 색(`#hex`, `oklch(`, `rgb(`, `hsl(`)은 토큰 파일(`tokens.css`, 앱 `brand.css`/오버라이드, 도메인 팔레트 파일)에만 둔다. 컴포넌트·페이지·유틸리티 클래스(`bg-[#…]`, `text-[oklch(…)]`)에서 금지한다. 검사는 [ux-guide](ux-guide.md) §4 금지 패턴 P4.

**TK-13 (MUST)** 대비 규칙과 검사 쌍은 아래와 같다. 검사 도구는 `tools/kt_contrast.py`(T-103)이며 앱 오버라이드 파일을 읽어 light 쌍 전부를 계산한다.

| 쌍 | 기준 | 표면 | 비고 |
|---|---|---|---|
| text-primary / secondary / tertiary ↔ surface | ≥ 4.5:1 | page·subtle·muted·card 4곳 | map 4.73(tertiary/page)·6.10 통과 |
| text-strong(정의 시) ↔ surface | ≥ 4.5:1 | 4곳 | |
| icon ↔ surface | ≥ 3:1 | 4곳 | |
| control-line ↔ surface | ≥ 3:1 | 4곳 | map 3.54 / 3.69 / 3.03 통과. geo 2.29·concierge 2.06·airport 1.15는 현재 미달(`dt` §3.4.2) |
| focus ↔ page | ≥ 3:1 | page | map 6.66 |
| brand-foreground ↔ brand | ≥ 4.5:1 | brand 채움 | 본문 크기 CTA 기준. ktdm 3.59 미달 |
| brand ↔ brand-tint | ≥ 3:1 | tint 배경 위 mark·아이콘 | pinvi admin 3.14 |
| status(4) ↔ status-tint | ≥ 4.5:1 | tint 배경 위 텍스트 | pinvi admin success 5.09 |
| status(4) ↔ surface-page | ≥ 4.5:1 | 배지·인라인 텍스트 | ktdm warn 3.45 미달 |
| border(장식) ↔ surface | 검사 제외 | — | 장식은 대비 요구 없음. 컨트롤 경계로 쓰면 TK-4 위반 |
| dark 쌍 | 위와 동일 | dark 활성 앱만 | map dark control-line/page 4.33 |

- 출력: 기본 `report`(Markdown 표 + JSON), fail은 **신규 미달만**. 기존 미달은 앱 `contrast-baseline.json`(매니페스트 `contrast.baseline` 경로)에 `{pair, surface, measured, required, until}`로 등록한다. `until` 경과 시 `EXEMPT_EXPIRED`로 `::error::` 주석.
- 채택 순서: report → 소비자 2회 연속 신규 미달 0 → common `versions.json` `enforce`로 fail 승격(D-30).
- 허용 오차 ±0.03(8-bit 양자화·감마, `dt` §3.4.2).

**TK-14 (MUST)** focus 링 레시피는 `base.css`가 `@layer base :focus-visible { outline: 2px solid var(--kt-focus); outline-offset: 2px }`로 **단일 발행**한다. 컴포넌트는 재선언하지 않고, 끄는 자리(`focus-visible:outline-0`)는 프로그램 포커스 컨테이너(`<main tabIndex={-1}>`, 다이얼로그 패널, listbox 컨테이너, 표 스크롤 영역)의 닫힌 목록뿐이다. 링은 transition 목록 밖에 둔다. 행동 규칙은 [ux-guide](ux-guide.md) UX-G9.1.

## 10. 폰트

**TK-15 (MUST)** common은 스택 **문자열**만 제공하고 폰트 파일을 배포하지 않으며 로딩은 앱 책임이다(`dt` §4 선행 보고서 §7.1 지지, D-12).

| 토큰 | 기본값 | 규칙 |
|---|---|---|
| `--kt-font-sans` | `"Pretendard Variable", Pretendard, "Noto Sans KR", "Apple SD Gothic Neo", system-ui, sans-serif` | Pretendard 1순위는 **Pretendard를 실제로 로드하는 앱**(map·pinvi·concierge: `pretendard` npm 1.3.9)에만 MUST. 미로드 앱(weather·airport·geo·ktdm)은 채택 시 현재 스택으로 오버라이드하고, 로딩 도입은 별도 task |
| `--kt-font-mono` | `ui-monospace, "SF Mono", Menlo, Consolas, monospace` | mono 계열(Geist Mono·IBM Plex Mono·JetBrains Mono)은 앱 선택. 로드하지 않는 폰트를 1순위에 두지 않는다 |

로딩 방식(`pretendard` npm dynamic subset, `next/font`)의 권고는 [frontend-stack](frontend-stack.md) §7.

## 11. 별칭 shim과 앱 고유 어휘

**TK-16 (SHOULD)** `aliases/map-vocabulary.css`는 map·weather·geo가 공유하는 무접두 어휘(`--surface-page`, `--text-primary`, `--brand`, `--control-line`, `--focus`, `--radius-control`, `--control-h`, `--rail`, `--duration-fast` 등)를 `var(--kt-*)`로 재선언하는 **선택 파일**이다(weather에서 map 어휘 294회, `inv/weather` §3.1). 이관 기간에만 import하고, 앱이 `kt-` 유틸리티로 옮기면 제거한다. 앱 고유 접두 별칭(`--ktc-*`, `--color-admin-*`, `--ui-*`)은 common이 배포하지 않으며 앱 파일에서 `var(--kt-*)`로 재해석한다(T-421·T-441·T-453).

별칭 충돌 검사(T-102): shim이 정의하는 이름이 앱 CSS에서 다른 값으로 재정의되면 보고한다.

## 12. 도메인 팔레트(마커·차트·기상)

**TK-17 (MUST)** 마커 팔레트 P-01~P-16은 common 소유가 아니다(D-26). map(Tableau 계열)과 pinvi(Material 계열)가 같은 코드에 다른 hex를 갖는 상태이며 hex 정본 확정은 map에 요청한다(O-13, T-505). common은 [ux-guide](ux-guide.md) §6의 16슬롯·라벨 대비 규칙만 가진다. `--chart-1..5`는 슬롯 이름만 공통이고 값은 앱, weather 기상 마커 색은 weather 소유(도메인 토큰으로 승격 권고, T-464).

## 13. 소비 방법 요약

필수 2줄(D-10)과 순서는 [consumer adoption runbook](../runbooks/consumer-adoption.md)이 정본이다.

```css
@import "tailwindcss";
@import "@kor-travel/tokens/tokens.css";      /* 값 정본 */
@import "@kor-travel/tokens/theme.css";       /* kt- 유틸리티 */
@import "@kor-travel/tokens/shadcn.css";      /* shadcn 사용 앱만 */
@import "@kor-travel/tokens/base.css";        /* 또는 base.scoped.css */
@import "./brand.css";                        /* 앱 오버라이드(TK-8) */
@source "../node_modules/@kor-travel/ui";     /* ui 채택 앱 */
```

Tailwind 없는 앱(weather 1단계)은 `tokens.css` + `aliases/map-vocabulary.css`만 import한다(T-461). 채택 PR은 6폭 시각 기준선 diff 0을 evidence로 남긴다(D-21, [responsive-web](responsive-web.md) §3).

## 14. 변경과 버전

토큰 이름·의미 변경은 0.x minor 파괴 항목이고 패치는 additive만 허용한다. 이름 폐기는 1 minor 동안 alias를 유지한다. 절차는 [ui-contract](ui-contract.md) §9(SemVer 0.x)와 [release runbook](../runbooks/release.md)이 정본이다. `@kor-travel/ui`는 `@kor-travel/tokens`의 호환 minor 하나를 peer로 요구한다.

## 15. 열린 결정

| # | 항목 | 기본값(이 문서) | 확인 필요 |
|---|---|---|---|
| O-4 | 네임스페이스 | `kt-` / `--kt-*` | 사용자 |
| O-8 | pinvi mobile Tailwind 3(NativeWind 4) 예외 | `exceptions`에 **미등록**, `tailwind-preset.cjs` 생성물로 소비 | 사용자 승인 전 등록 금지(D-08) |
| O-11 | 다크 모드 | 정의 필수·활성 opt-in·오버라이드 dark 선택 | 사용자 |
| O-13 | 마커 팔레트 hex 정본 | map(Tableau) 확정 요청 | map 저장소 |
| — | z-index 기본값·shadow 값·`--kt-text-*` line-height | pinvi/map 값 후보 | T-101 실물 |

## 16. 근거

- 토큰 비교·역할표·대비 재검증·패키지 초안: [design-tokens 조사](../survey/cross/design-tokens.md) §3.1~§3.6·§5.
- 접근성·모션·타이포 규칙: [ux-patterns 조사](../survey/cross/ux-patterns.md) §2 G9, §4 C12~C14.
- 토큰 이름 정합(모든 배포 방식의 선행 조건): [ui-components 조사](../survey/cross/ui-components.md) §6.3.
- 결정: [설계 브리프](../plan/design-brief.md) D-08·D-10·D-12·D-13·D-21·D-26·D-29·D-31, O-4·O-8·O-11·O-13·O-21.
- 배포 형태·CSS 파일 구조의 현재 설계: [style-delivery](../architecture/style-delivery.md), ADR-006(색인: [ADR README](../adr/README.md)).
