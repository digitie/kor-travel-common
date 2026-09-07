# 디자인 토큰 계약(--kt-*) — 색상 톤·형태·모션 규칙

- 정본 지위: 이 문서는 @kor-travel/tokens의 토큰 **이름·의미·계층·프로필·오버라이드·검사 규칙**의 정본이다. 값의 정본은 [packages/tokens/tokens.css](../../packages/tokens/tokens.css)이고, dist/의 JSON·TypeScript·Tailwind preset은 이 CSS에서 생성한다.
- 확정 task: **T-104**. T-101·T-102의 실제 파일과 대조해 TK-1~TK-13을 정리했으며, 두 적대적 리뷰 통과 후 확정한다. 마지막 갱신: 2026-09-08.
- 조사 기준선: [디자인 토큰 조사](../survey/cross/design-tokens.md) §1의 앱별 기준 commit(c494e227, 9af25e5, 6003da9, 2bb1111/99b3f98, 1d9d74d, 7945305, 862562d, d078437)을 사용했다. common 실물 대조 기준은 T-102 병합 후 4cde7e8이다.
- 규칙 어휘: **MUST**는 신규 채택에서 반드시 지키고, **SHOULD**는 벗어날 때 PR 또는 예외 매니페스트에 근거와 until을 남긴다. 열림(O-n)은 기본값으로 진행하되 사용자 확인이 필요한 결정이다. UX·반응형·파일 import 절차는 [ux-guide](ux-guide.md), [responsive-web](responsive-web.md), [style-delivery](../architecture/style-delivery.md), [consumer adoption runbook](../runbooks/consumer-adoption.md)의 정본을 따른다.

## 1. 소유 범위와 계층

common은 의미 이름, 기본값, 프로필 모양, alias 의미, 대비 쌍, 값 형식과 생성물 정합성을 제공한다. 브랜드 hue·paper/ink 값의 제품별 선택, 도메인 팔레트, 폰트 파일·로딩, dark 토글, 사용자 프로필 값과 앱 정책은 소비자가 소유한다. common은 인증 서버·사용자 저장소·운영 비밀을 포함하지 않는다.

**TK-1 (MUST) — 접두와 네임스페이스.** semantic CSS 변수는 --kt-*, Tailwind 유틸리티는 kt-를 사용한다(bg-kt-surface-page, h-kt-control, text-kt-2xs). 앱은 같은 --kt-* 이름을 재선언해 오버라이드하고, 앱 고유 확장은 --ktc-*, --pv-*, --color-admin-*, --ui-*처럼 앱 파일에 둔다. common이 --ktc-*나 무접두 --color-*를 새 계약으로 배포하지 않는다. 이 조사 기준 전 저장소에서 --kt-* 충돌은 0회였다(dt §3.6.1).

**TK-2 (MUST) — 두 단계 계층.** 기본 계층은 semantic(--kt-*) ← app override 두 단계다. 공통 primitive ramp(50~900)나 컴포넌트별 세 번째 토큰 층을 강제하지 않는다. shadcn alias와 theme.css 유틸리티는 semantic을 참조하는 파생 층이며, 앱은 semantic을 건너뛰고 alias에만 값을 넣지 않는다(dt §3.6.2).

## 2. 역할 목록과 실제 대조

**TK-3 (MUST) — 역할 집합.** 아래 표는 T-101 실물 tokens.css에서 추출한 44개 변수와 1:1이다. light와 dark는 각각 :root와 .dark의 실제 값이며, 필수는 common 기본 파일에 두 모드 모두 정의해야 한다는 뜻이다. 오버라이드는 앱이 재선언할 수 있는 범위이고, 값 허용 조건은 TK-6에 있다. 표의 값은 의미를 설명하기 위한 대조값이며 값 변경은 CSS와 생성물 diff를 함께 거쳐야 한다.

### 2.1 색상·상태

| 변수 | 의미 | light(:root) | dark(.dark) | dark | 오버라이드 |
|---|---|---|---|---|---|
| --kt-surface-page | 문서·페이지 배경 | oklch(97.8% 0.003 128) | oklch(19% 0.006 150) | 필수 | 허용(paper) |
| --kt-surface-subtle | 행 hover·툴바·secondary 배경 | oklch(96.7% 0.006 138) | oklch(24% 0.008 145) | 필수 | 허용(paper) |
| --kt-surface-muted | 선택 행·장식 border 원천 | oklch(92.5% 0.01 141) | oklch(31% 0.012 145) | 필수 | 허용(paper) |
| --kt-surface-card | 카드·패널·팝업 배경 | oklch(99.2% 0.002 140) | oklch(23% 0.007 145) | 필수 | 허용(paper) |
| --kt-text-primary | 본문 텍스트 | oklch(30% 0.006 157) | oklch(93% 0.006 155) | 필수 | 허용(ink) |
| --kt-text-secondary | 보조 본문·라벨 | oklch(48% 0.012 159) | oklch(78% 0.01 155) | 필수 | 허용(ink) |
| --kt-text-tertiary | 메타·캡션 | oklch(54% 0.012 154) | oklch(68% 0.012 155) | 필수 | 허용(ink) |
| --kt-text-disabled | 비활성 라벨(대비 제외) | oklch(79% 0.012 154) | oklch(52% 0.012 155) | 필수 | 허용(ink) |
| --kt-text-strong | 제목 강조, 미정의 시 primary 파생 | var(--kt-text-primary) | var(--kt-text-primary) | 필수 | 조건부(ink) |
| --kt-icon | 기본 아이콘, tertiary 파생 | var(--kt-text-tertiary) | oklch(70% 0.01 155) | 필수 | 금지(파생) |
| --kt-border | 장식 hairline·구분선, 컨트롤 경계 금지 | var(--kt-surface-muted) | var(--kt-surface-muted) | 필수 | 금지(파생) |
| --kt-control-line | 입력·버튼 컨트롤 경계 | oklch(61% 0.012 145) | oklch(58% 0.012 145) | 필수 | 허용(대비) |
| --kt-brand | CTA 채움·활성 mark·링크 | oklch(51.4% 0.081 169) | oklch(76% 0.085 169) | 필수 | 허용(brand) |
| --kt-brand-hover | brand hover·active | oklch(46% 0.085 169) | oklch(81% 0.085 169) | 필수 | 허용(brand) |
| --kt-brand-tint | 활성 nav·선택 행의 불투명 tint | oklch(95.2% 0.013 172) | oklch(31% 0.035 169) | 필수 | 허용(brand) |
| --kt-brand-foreground | brand 채움 위 텍스트 | oklch(99% 0.002 140) | oklch(20% 0.02 165) | 필수 | 허용(brand) |
| --kt-focus | 불투명 포커스 링 | oklch(45% 0.09 169) | oklch(80% 0.09 169) | 필수 | 허용(대비) |
| --kt-success | 성공·완료 상태 텍스트/mark | oklch(46.9% 0.087 149) | oklch(75% 0.09 149) | 필수 | 허용(status) |
| --kt-success-tint | 성공 상태의 불투명 배경 | oklch(95% 0.03 150) | oklch(28% 0.04 150) | 필수 | 허용(status) |
| --kt-warning | 결정 대기·저하 상태 | oklch(50.9% 0.103 71) | oklch(77% 0.12 75) | 필수 | 허용(status) |
| --kt-warning-tint | warning의 불투명 배경 | oklch(96% 0.035 80) | oklch(30% 0.045 80) | 필수 | 허용(status) |
| --kt-info | 정보·기계 진행 상태 | oklch(50% 0.16 258) | oklch(75% 0.11 258) | 필수 | 허용(status) |
| --kt-info-tint | info의 불투명 배경 | oklch(95.5% 0.025 255) | oklch(30% 0.05 258) | 필수 | 허용(status) |
| --kt-destructive | 오류·파괴 행동 | oklch(51.4% 0.167 27) | oklch(72% 0.14 27) | 필수 | 허용(status) |
| --kt-destructive-tint | destructive의 불투명 배경 | oklch(96% 0.03 25) | oklch(30% 0.06 27) | 필수 | 허용(status) |
| --kt-overlay | 모달 backdrop, 공통 alpha 색 | oklch(30% 0.006 157 / 0.45) | oklch(10% 0.006 157 / 0.6) | 필수 | 금지(파생) |

### 2.2 형태·밀도·모션·층

| 변수 | 의미 | light(:root) | dark(.dark) | dark | 오버라이드 |
|---|---|---|---|---|---|
| --kt-radius-control | 버튼·입력·배지 radius | 0.375rem(6px) | 0.375rem(6px) | 필수 | 프로필만 |
| --kt-radius-panel | 카드·패널·다이얼로그 radius | 0.5rem(8px) | 0.5rem(8px) | 필수 | 프로필만 |
| --kt-control-h | admin 기본 컨트롤 높이 | 2.25rem(36px) | 2.25rem(36px) | 필수 | 프로필만 |
| --kt-control-h-sm | admin 소형 컨트롤 높이 | 1.875rem(30px) | 1.875rem(30px) | 필수 | 프로필만 |
| --kt-rail | inspector rail 기본 폭 | 22rem | 22rem | 필수 | 프로필·등록 예외만 |
| --kt-duration-fast | 짧은 전환 시간 | 100ms | 100ms | 필수 | 프로필만 |
| --kt-duration-base | 기본 전환 시간 | 150ms | 150ms | 필수 | 프로필만 |
| --kt-ease-out | 진입·확장 easing | cubic-bezier(0.16, 1, 0.3, 1) | cubic-bezier(0.16, 1, 0.3, 1) | 필수 | 프로필만 |
| --kt-ease-in | 종료·축소 easing | cubic-bezier(0.7, 0, 0.84, 0) | cubic-bezier(0.7, 0, 0.84, 0) | 필수 | 프로필만 |
| --kt-shadow-elevated | 제한적인 elevated 그림자 | 0 4px 12px oklch(30% 0.006 157 / 0.1) | 0 4px 12px oklch(10% 0.006 157 / 0.32) | 필수 | 프로필·등록 예외만 |
| --kt-shadow-modal | 모달 전용 그림자 | 0 8px 24px oklch(30% 0.006 157 / 0.14) | 0 8px 24px oklch(10% 0.006 157 / 0.4) | 필수 | 프로필·등록 예외만 |
| --kt-z-nav | nav stacking 층 | 30 | 30 | 필수 | 프로필·등록 예외만 |
| --kt-z-panel | panel stacking 층 | 40 | 40 | 필수 | 프로필·등록 예외만 |
| --kt-z-overlay | overlay stacking 층 | 50 | 50 | 필수 | 프로필·등록 예외만 |
| --kt-z-modal | modal stacking 층 | 60 | 60 | 필수 | 프로필·등록 예외만 |
| --kt-z-toast | toast stacking 층 | 70 | 70 | 필수 | 프로필·등록 예외만 |
| --kt-font-sans | 공통 sans 스택 문자열 | "Pretendard Variable", Pretendard, "Noto Sans KR", "Apple SD Gothic Neo", system-ui, sans-serif | "Pretendard Variable", Pretendard, "Noto Sans KR", "Apple SD Gothic Neo", system-ui, sans-serif | 필수 | 허용(스택) |
| --kt-font-mono | 공통 mono 스택 문자열 | ui-monospace, "SF Mono", Menlo, Consolas, monospace | ui-monospace, "SF Mono", Menlo, Consolas, monospace | 필수 | 허용(스택) |

## 3. shadcn alias

**TK-4 (MUST) — 네 가지 의미.** packages/tokens/shadcn.css의 alias는 semantic을 참조하며 다음 네 의미를 변경하지 않는다.

| shadcn alias | 반드시 참조하는 semantic | 의미 | 금지되는 재해석 |
|---|---|---|---|
| --input | var(--kt-control-line) | 입력·버튼의 경계선(3:1 검사) | 입력 배경색 |
| --accent | var(--kt-brand-tint) | 활성·hover tint | surface-muted 또는 임의 brand 값 |
| --radius | var(--kt-radius-control) | 컨트롤 radius 6px | panel radius 8px |
| --border | var(--kt-border) | 장식 hairline | 컨트롤 경계선 |

--background·--card·--popover·--primary·--secondary·--muted·--ring·--destructive와 foreground 짝은 같은 파일의 semantic 파생 alias다. --chart-1..5는 슬롯 이름만 common이 제공하고 실제 색은 앱이 소유한다(dt §3.2.3).

## 4. 프로필

**TK-5 (MUST) — admin/consumer 분리.** common은 admin 프로필의 실물 값을 제공하고 consumer 프로필은 의미 이름만 제공한다. 한 앱에서 섞을 때는 `[data-kt-surface="admin"]` 같은 스코프에서 프로필 변수만 재선언한다. shadcn alias를 사용하는 컴포넌트는 `shadcn.css`의 `[data-kt-surface]` 파생 블록을 함께 로드해 semantic 오버라이드가 alias에도 반영되게 한다.

| 프로필 | common이 확정하는 내용 | 값의 소유권·대조 |
|---|---|---|
| admin | radius 6/8px, control 36/30px, 본문 15px, 7단 2xs/xs/sm/md/lg/xl/2xl = 12/13.5/15/17/20/24/30px, rail 22rem | tokens.css와 theme.css의 실제 값과 일치. 타입 스케일은 비inline @theme에 정의 |
| consumer | semantic 이름, 터치 컨트롤 의미와 문서 | 관찰값 8/14/20/32px radius, 44px 터치, 16px 본문은 **pinvi 소유**다. common 값으로 정본화하거나 admin에 섞지 않는다 |

**TK-6 (MUST) — 허용·금지 오버라이드.** 앱 brand.css는 tokens.css 뒤에서 아래 허용 목록만 재선언한다.

- 허용: --kt-brand, --kt-brand-hover, --kt-brand-tint, --kt-brand-foreground, --kt-focus, 네 surface, --kt-text-primary/secondary/tertiary/disabled와 선택적 --kt-text-strong, --kt-control-line, 네 status와 tint, --kt-font-sans, --kt-font-mono.
- 프로필 전용: radius·control 높이·타입 스케일·duration/ease·rail·z/shadow는 프로필 파일이나 등록된 예외에서만 바꾼다. 표의 `프로필·등록 예외만`은 brand.css에서 임의로 바꿀 수 없다는 뜻이다. weather rail=17rem처럼 이관 중인 값은 소비자 task와 예외 매니페스트에 until을 함께 적기 전까지 common 기본값을 대체하지 않는다.
- 금지: --kt-border, --kt-icon, --kt-overlay의 직접 값 변경, alias만의 값 변경, 컴포넌트 안 raw 색·팔레트 alpha, 공통 토큰에 앱 접두 값을 추가하는 행위. 형태·높이·모션을 개별 컴포넌트에서 덮어쓰지 않는다.

## 5. 다크 모드

**TK-7 (MUST) — 정의는 완비하고 활성화는 선택한다.** tokens.css의 :root는 color-scheme: light를 선언하고, .dark는 위 44개 변수의 값을 모두 명시한다. 앱은 dark-class.css 또는 dark-media.css 중 하나를 명시적으로 import해 활성화하며 둘을 동시에 import하지 않는다. 앱이 브랜드 값을 오버라이드할 때 dark 재선언은 선택이지만, common dark fallback을 사용하려면 class 경로는 light 값을 `:root:not(.dark)`에, media 경로는 `@media (prefers-color-scheme: light)` 안의 `:root`에 둔다. 일반 `:root` 오버라이드는 활성 dark 선언보다 뒤에서 이겨 common dark를 덮을 수 있으므로 fallback을 보장하지 않는다. dark 대비 검사는 dark를 실제 활성화하는 앱만 대상으로 한다(dt §3.6.6).

## 6. 대비와 값 형식

**TK-8 (MUST) — 대비 쌍과 신규 미달 정책.** T-103의 tools/kt_contrast.py는 다음 쌍을 light에서 계산하고, dark는 활성 앱에서만 계산한다.

| 쌍 | 기준 | 표면·용도 |
|---|---:|---|
| text primary/secondary/strong ↔ surface 4종 | 4.5:1 | 본문·강조 라벨 |
| text tertiary ↔ surface 4종 | 3:1 | 메타·캡션 |
| text disabled ↔ surface 4종 | 검사 제외 | 비활성 상태는 대비 합격 쌍에서 제외 |
| icon ↔ surface 4종 | 3:1 | 아이콘 |
| control-line ↔ surface 4종 | 3:1 | WCAG 1.4.11 컨트롤 경계 |
| focus ↔ surface-page | 3:1 | 포커스 링 |
| brand-foreground ↔ brand | 4.5:1 | CTA 채움 위 텍스트 |
| brand ↔ brand-tint | 3:1 | tint 위 mark·아이콘 |
| status 4종 ↔ status-tint | 3:1 | tint 위 상태 텍스트 |

--kt-border는 장식 전용이므로 대비 쌍에서 제외하고 컨트롤 경계로 사용하면 TK-3·TK-4 위반이다. report는 전체 결과와 JSON을 남기며, 기존 미달은 앱의 contrast-baseline.json에 {pair, surface, measured, required, until}로 등록한다. **새 미달만 fail**하고 until 만료는 EXEMPT_EXPIRED 오류로 승격한다. 허용 오차는 조사 기준 ±0.03이다(dt §3.4.2).

**TK-9 (SHOULD) — 값 형식과 alpha.** 기본값은 OKLCH(oklch(L% C H))를 권고하고 hex를 허용한다. hex를 쓰는 앱은 오버라이드 주석에 대응 OKLCH를 남긴다. alpha는 overlay와 shadow에만 허용하며 status·brand tint와 컴포넌트 팔레트에는 쓰지 않는다. 컴포넌트·페이지의 raw #hex·oklch()·rgb()·hsl()와 팔레트 alpha 유틸리티는 금지한다. 이 문서는 UX 금지 패턴을 복제하지 않고 [ux-guide §4](ux-guide.md)의 정본을 가리킨다.

## 7. 정본·생성물·별칭·폰트

**TK-10 (MUST) — 정본과 생성물.** 값은 packages/tokens/tokens.css에서만 편집한다. packages/tokens/dist/tokens.json(DTCG), dist/tokens.ts, dist/tailwind-preset.cjs, dist/index.js, dist/index.d.ts는 build가 생성한다. theme.css는 @theme inline에서 semantic을 Tailwind v4 네임스페이스(--color-kt-*, --spacing-kt-*, --radius-kt-*, --font-kt-*, --ease-kt-*, --shadow-kt-*)로 연결하고, 타입 7단은 비inline @theme에 둔다. npm run build --workspace packages/tokens 뒤 npm run check --workspace packages/tokens가 생성물 diff 0을 확인한다. 정본과 생성물을 수동으로 따로 바꾸지 않는다(dt §3.6.3).

대조 결과는 다음과 같다.

| 대상 | 실제 파일에서 확인한 계약 | 판정 |
|---|---|---|
| 변수 집합 | tokens.css regex 고유값 44개, 표 TK-3 44개 | 일치 |
| light/dark | :root 44개와 .dark 44개, .dark에 color-scheme: dark | 일치 |
| alias | shadcn.css의 --input, --accent, --radius, --border가 각각 TK-4 의미를 참조 | 일치 |
| admin 값 | tokens.css의 0.375/0.5rem, 2.25/1.875rem과 theme.css의 7단·@theme | 일치 |
| 생성물 경로 | package root CSS → dist/ JSON·TS·preset | 일치 |

**TK-11 (SHOULD) — 선택 shim과 앱 어휘.** packages/tokens/aliases/map-vocabulary.css는 map·weather·geo의 이관 기간에만 공통 레거시 이름을 var(--kt-*)로 연결하는 선택 파일이다. T-102에서 map의 control radius 의미와 weather의 panel·rail·font 앱 소유 값을 분리했다. 앱이 kt- 유틸리티와 semantic 이름으로 이관하면 shim import를 제거한다. concierge의 --ktc-*, geo의 --ui-*, pinvi의 --pv-*·--color-admin-*는 common shim이 재정의하지 않는다.

**TK-12 (MUST) — 폰트.** common은 폰트 파일·로더가 아니라 다음 스택 문자열만 제공한다. Pretendard를 실제로 로드하는 앱만 Pretendard 1순위를 MUST로 유지하고, 로드하지 않는 앱은 현재 로드 가능한 스택으로 오버라이드한다. 로딩은 앱의 next/font 또는 패키지 책임이다.

| 변수 | common 기본 스택 |
|---|---|
| --kt-font-sans | "Pretendard Variable", Pretendard, "Noto Sans KR", "Apple SD Gothic Neo", system-ui, sans-serif |
| --kt-font-mono | ui-monospace, "SF Mono", Menlo, Consolas, monospace |

**TK-13 (MUST) — marker 팔레트 범위.** P-01~P-16 marker 색의 hex와 데이터 매핑은 common 소유가 아니다. common은 16 슬롯·라벨 대비 같은 규칙만 제공하고, hex 정본은 kor-travel-map이 확정한 뒤 소비자가 가져온다. --chart-1..5도 슬롯 이름만 common이고 값은 앱 소유다. O-13 확인 전 common이 hex를 정본화하거나 pinvi 팔레트를 복사하지 않는다(dt §3.5).

## 8. 소비와 변경

소비자는 [consumer adoption runbook](../runbooks/consumer-adoption.md)의 import 순서와 @source 경로를 따른다. 일반적인 Tailwind v4 진입은 tokens.css(값) → theme.css(유틸리티) → 필요 시 shadcn.css·base.css·선택 shim 순서다. CSS 파일 경로와 토큰 이름·의미는 공개 계약이므로 변경은 0.x minor의 breaking 절차와 alias 유지 기간을 [ui-contract §9](ui-contract.md)와 [release runbook](../runbooks/release.md)에 기록한다.

## 9. 예외와 열린 결정

| ID | 항목 | 기본값 | 상태·처리 |
|---|---|---|---|
| O-4 | 변수·유틸리티 네임스페이스 | --kt-* / kt- | **열림(사용자 확인 필요)**. 현재 기본값으로 진행 |
| O-8 | pinvi mobile Tailwind 3/NativeWind 예외 | 예외 미등록, 생성 preset은 소비 가능 | **열림(사용자 확인 필요)**. 승인 전 common 예외로 등록하지 않음 |
| O-11 | 다크 | 정의 필수·활성 opt-in·앱 dark override 선택 | **열림(사용자 확인 필요)**. TK-7 기본값으로 진행 |
| O-13 | marker hex 정본 | kor-travel-map 확정 요청 | **열림(사용자 확인 필요)**. common은 규칙만 유지 |
| — | weather rail 17rem | common 22rem | T-461 채택 task에서 예외 매니페스트와 until을 함께 확정하기 전에는 관찰값으로만 취급 |
| — | pinvi admin 터치 44px | admin 기본 36/30px | 소비자 프로필 소유. common admin 기본값을 바꾸지 않음 |

## 10. 검증·근거·미실행 gate

T-104에서 다음을 실행해 문서와 실물 대조를 재현한다.

- python -B -X utf8 tools/validate_document_links.py
- python -B -X utf8 tools/validate_plan.py
- python -B -X utf8 -m unittest discover -s tests -p "test_*.py"
- npm run check --workspace packages/tokens
- git diff --check
- rg -o -- '--kt-[a-z0-9-]+' packages/tokens/tokens.css | sort -u와 TK-3 표 집합 비교(Windows PowerShell은 `Sort-Object -Unique`)

T-103의 tools/kt_contrast.py 실행은 **NOT_RUN(T-103 대기)**이며 소비자 build/e2e·6폭 시각 비교·npm/PyPI 게시도 **NOT_RUN(후속 task 또는 사용자 범위)**이다. 실행하지 않은 gate를 통과로 표시하지 않는다.

근거는 [디자인 토큰 조사](../survey/cross/design-tokens.md) §3.1~§3.6·§5, [설계 브리프](../plan/design-brief.md) D-10·D-12·D-26·O-4·O-11·O-13, [ADR-006](../adr/006-design-token-contract.md)와 T-101·T-102 상세 task다. 조사 문서는 근거이며 현재 규칙의 정본은 이 문서와 실제 package 계약이다.
