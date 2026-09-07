# PC/Mobile Web 규약 — 표면 분류·breakpoint·검사 폭·터치·안전영역·overflow

- 정본 지위: 이 문서는 웹 표면의 **반응형 수치와 검사 절차**의 정본이다. 셸·목록·피드백 같은 행동 규칙은 [ux-guide](ux-guide.md), 밀도 토큰 값은 [design-tokens](design-tokens.md) §5.2·§7이 정본이며 여기서는 수치와 검사만 정한다.
- 확정 task: **T-106**(시각 기준선 템플릿은 T-108). 이 판은 [ux-patterns 조사](../survey/cross/ux-patterns.md) §3과 브리프 D-13·D-21을 규칙 ID `RW-n`으로 옮긴 초안이다. 마지막 갱신: 2026-09-06.
- 근거 약칭: `ux` = ux-patterns 조사, `dt` = [design-tokens 조사](../survey/cross/design-tokens.md), `inv/<app>` = [인벤토리](../survey/README.md) §3.1.

## 1. 표면 분류와 기본 자세

**RW-1 (MUST)** 모든 화면은 아래 네 표면 중 하나로 분류하고, 표면의 기본 자세를 따른다. 표면 분류는 앱 `design.md`에 명시한다.

| 표면 | 기본 자세 | 셸 | 적용 앱 | 근거 |
|---|---|---|---|---|
| Admin | **PC-first + 최소 모바일 보장**: 1024px 이상 rail-workbench, 그 아래 strip(또는 drawer). 320px부터 문서 전체 가로 스크롤을 만들지 않는다(컨테인). 표·지도·작업면만 자체 overflow | [ux-guide](ux-guide.md) UX-G1 | map·ktc·geo·ktdm·weather·pinvi admin·airport 백업 패널 | `ux` §3.1(5앱 문서 일치) |
| 사용자 웹 | **mobile-first**: 하단 탭바 셸, 44px 타깃, 16px 입력, 안전영역 패딩, `lg` 이상 상단 탭. 판정은 뷰포트 + 포인터 능력(UA 스니핑 금지) | 하단 탭바 4 + 더보기 | pinvi 사용자 웹 | `ux` §3.1 |
| 사용자 대시보드 | 반응형 단일 페이지: 860px 이하 카드·`<details>` 접기, 320px 가독성 게이트 | 없음 | kta 대시보드 | `ux` §3.1, `inv/airport` §3 |
| 모바일 앱 | 네이티브 Stack 헤더 + SafeArea, 48px 버튼·입력, NativeWind(Tailwind 3) + `tailwind-preset.cjs` 생성물 | 네이티브 | pinvi mobile | `ux` §3.1; Tailwind 3 예외는 열림 O-8 |

사용자 웹·모바일 앱은 코드 소비 대상이 아니며(D-29) 이 문서는 수치 규칙만 공유한다.

## 2. breakpoint

**RW-2 (MUST)** breakpoint는 Tailwind v4 기본값 4개를 그대로 쓰고 재정의하지 않는다(`--breakpoint-*` 커스텀 금지). 셸 전환은 `lg` 하나뿐이다.

| 이름 | 값 | 용도 | 근거 |
|---|---|---|---|
| `sm` | 640px | 헤더 actions/summary 한 줄 배치(`sm:flex-row`), 본문 패딩 확대 | map `pagination-bar.tsx`, pinvi admin main |
| `md` | 768px | 헤더 h1/actions 행 분리, 2열 dl, 표의 block 전환, 모바일 상세 = 페이지 / PC = 모달 분기 | map 셸 헤더, `detail-list.tsx`, ktdm 48rem, ktc `use-is-mobile.ts` |
| `lg` | 1024px | **셸 전환**(rail ↔ strip/drawer), 사용자 웹 탭바 ↔ 상단 탭 | map·ktc·geo·ktdm·pinvi 전부 |
| `xl` | 1280px | 우측 inspector rail(`--kt-rail` 22rem) 2열 | map, pinvi `AdminRailGrid` |

- RW-2.1 JS/CSS 미디어 매치는 `(max-width: 1023px)`(또는 `(width < 64rem)`)로 쓴다. 992px(62rem)·860px 같은 별도 셸 전환값은 금지(§12 재조정).
- RW-2.2 터치 승격은 `(pointer: coarse) and (hover: none)`으로 판정한다(pinvi `useMobileWebLayout` 선례). User-Agent 문자열로 모바일을 판정하지 않는다.
- RW-2.3 콘텐츠 breakpoint(표 → 카드 전환 등)는 위 4개 중에서 고른다. 앱 고유 값(kta 860/980/560/380)은 §12의 재조정 대상이며 신규 코드에서 추가하지 않는다.
- RW-2.4 pinvi 사용자 웹 문서의 참조값 744/1128/1440은 코드에 반영되지 않았으므로(`ux` §5-8 사실) Tailwind 기본으로 확정한다.

## 3. 검사 폭과 시각 기준선

**RW-3 (MUST)** 검사 폭은 **320 / 375 / 414 / 768 / 1024 / 1440**px 6폭이다(`ux` §3.2, 설계 문서 합집합).

| 항목 | 규칙 | 근거 |
|---|---|---|
| 기준선 시점 | 토큰·스타일·셸을 바꾸는 소비자 PR은 **착수 전** 6폭 스크린샷 기준선을 캡처하고 **완료 후** diff를 PR evidence로 첨부한다(저장소 파일 아님) | D-21 |
| 템플릿 | `templates/playwright.baseline.ts`(T-108): 6폭 × 대표 라우트(목록·상세·폼·로그인·대시보드 knob별 1개) 스크린샷 + `scrollWidth` 단언. Playwright가 없는 앱(weather·ktdm)도 이 템플릿을 일시 설치해 캡처한다 | D-21 |
| 4단 PR | Tailwind v4 전환은 "기준선 캡처 → 설정만 → 토큰만 → 컴포넌트" 4단 별도 PR이며 각 단계가 diff 0(또는 원인이 설명된 diff)을 evidence로 남긴다 | D-08 |
| 중단 조건 | 원인 불명 시각 diff가 남으면 해당 단계를 revert한다 | D-08 |
| 320px 게이트 | admin은 320px에서 본문·표 컨테이너·헤더가 클리핑 없이 읽혀야 한다(kta 감사 게이트 승계) | `inv/airport` §9 |

각 폭에서 확인하는 항목(체크리스트, 기준선 스펙이 단언 가능한 것은 단언):

| 항목 | 단언 |
|---|---|
| 문서 가로 스크롤 없음 | `document.documentElement.scrollWidth <= window.innerWidth` |
| 셸 상태 | <1024: strip/drawer 렌더, rail 숨김; ≥1024: rail 렌더 |
| 헤더 밴드 | actions가 wrap되고 h1이 잘리지 않음 |
| 표 | `[data-slot="table-container"]`만 `overflow-x: auto` |
| 터치 타깃 | §4 수치(`getBoundingClientRect`) |
| 텍스트 | `text-kt-2xs`(12px) 미만 렌더 없음 |

## 4. 터치·히트 영역

**RW-4 (MUST)** 독립 컨트롤 높이와 최소 히트 영역은 표면별로 다르며 섞지 않는다(`ux` §3.3, C6).

| 표면 | 독립 컨트롤 | 최소 히트 영역 | micro-control 처리 | 근거 |
|---|---|---|---|---|
| Admin | 36px(`h-kt-control`) / 30px(`h-kt-control-sm`) | 24px(WCAG 2.5.8) | 24px 아이콘 버튼은 의사요소(`before:-inset-2`)로 40px 히트 확장, 체크박스 16px + 8px 패딩 = 32px. 허용 목록은 [ux-guide](ux-guide.md) UX-G9.7 | map·ktc·geo·weather·ktdm·pinvi admin 토큰 |
| 사용자 웹 | 44px(`min-h-11`) | 44px | `sm` 버튼은 coarse pointer에서 44px로 승격 | pinvi `Button.tsx`, `DESIGN.md` |
| 모바일 앱 | 48px(`min-h-12`) 버튼·입력 | 44px(체크박스·칩) | — | pinvi mobile `ui.tsx` |
| kta 대시보드 | 46px 버튼·입력(토큰 아님) | 44px | 이관 시 admin 프로필로 정렬(T-430·T-431) | `dt` §3.1.2 |

- 등록된 예외: pinvi admin `feature-requests`·`feature-reference-reconciliations` 2쪽은 e2e가 44px를 단언하므로 **영구 예외**(열림 O-21, 매니페스트 `exceptions[]`에 `until: null` + `review`).
- geo `.field select/textarea`·`.checkbox-row`·`.filter-bar` 44px 규칙은 admin 프로필 이관(T-441·T-444) 시 36/30으로 정렬한다.

## 5. 타이포 하한

**RW-5 (MUST)** 폰트 하한은 표면별로 다음과 같다. 스케일 이름·값은 [design-tokens](design-tokens.md) TK-5, 금지 패턴은 [ux-guide](ux-guide.md) §4 P2.

| 표면 | 본문 | 최소 | 비고 |
|---|---|---|---|
| Admin | 15px(`text-kt-sm`) | 12px(`text-kt-2xs`) | ktdm 14px 본문·11px, kta 11px는 정렬 대상(C13) |
| 사용자 웹 | 16px(입력 포함 — iOS 자동 확대 방지) | 12px(배지 예외) | pinvi `DESIGN.md` |
| 모바일 앱 | 16px | 12px | `text-base/sm/xs` |

입력 요소의 `font-size`는 사용자 웹에서 16px 미만으로 두지 않는다. admin은 PC-first라 15px 입력을 허용한다.

## 6. 안전영역

**RW-6 (MUST)** 하단·상단 고정 요소가 있을 때만 `env(safe-area-inset-*)`를 더한다.

| 표면 | 규칙 | 근거 |
|---|---|---|
| Admin | 하단 고정 바(bulk 액션 바 등)가 있을 때만 `pb-[calc(0.5rem+env(safe-area-inset-bottom))]`. 셸 자체에는 불필요 | ktc `ReviewBulkPanel` |
| 사용자 웹 | 탭바 `pb-[env(safe-area-inset-bottom)]` + `main` 하단 패딩 `--app-tabbar-h` + 안전영역; sticky 상단 헤더는 `env(safe-area-inset-top)`; `viewport-fit=cover` 메타 | pinvi `AppShell.tsx`·`globals.css` |
| 모바일 앱 | `SafeAreaView edges={['top','bottom']}` | pinvi mobile |

## 7. overflow

**RW-7 (MUST)** 문서 루트는 `html, body { overflow-x: clip }`이다. `overflow-x: hidden`은 sticky·anchor positioning을 깨므로 금지한다(kta 감사가 hidden → clip으로 결정, `ux` G9.9 4앱).

| 대상 | 규칙 |
|---|---|
| 표 | `[data-slot="table-container"]`가 `overflow-x: auto`. 스크롤 가능하면 `tabIndex={0}` + 접근 가능한 이름(`aria-label` 또는 `aria-labelledby`)으로 키보드 스크롤을 보장 |
| 지도·작업면 | 컴포넌트 루트가 자체 overflow. full-bleed 지도는 셸 본문 패딩을 제거하되 문서 폭을 넘지 않는다 |
| nav strip | `<nav>` 안에서만 `overflow-x-auto`, 스크롤바 숨김 없이 |
| 긴 문자열 | 컨테이너 `min-w-0` + 식별자는 `truncate`/`break-all`, 한글 본문은 `word-break: keep-all` |
| 검사 | §3 6폭 `scrollWidth` 단언 |

## 8. 다크 기본

**RW-8 (MUST)** 웹 표면은 light 기본이다(`ux` C14, 4앱 사실). 토큰은 `.dark` 값을 준비하고(TK-7) 활성화는 앱이 `dark-class.css`/`dark-media.css` 중 하나를 import해 opt-in한다. kta처럼 OS 설정을 따르는 자동 dark는 `dark-media.css` 경로로 허용한다. e2e·시각 기준선은 light에서 캡처하고, dark 활성 앱만 dark 기준선을 추가한다. 열림 O-11.

## 9. 모바일 셸 전략

**RW-9 (MUST 계약 / SHOULD 선택)** admin의 좁은 화면 셸은 **상단 가로 strip이 기본**, off-canvas drawer는 옵션이며 둘 다 [ux-guide](ux-guide.md) UX-G4.8의 접근성 계약을 만족해야 한다(C4). 하단 탭바는 사용자 웹 전용이다.

| 전략 | 규칙 | 참조 구현 | 근거 |
|---|---|---|---|
| 상단 strip(기본) | `<nav>` 안 `overflow-x-auto`, 활성 항목 `scrollIntoView({ inline: "center", behavior })`(reduced-motion 시 `auto`), 라벨 표시. 아이콘 전용 항목은 sr-only 라벨 + `title`. 항목 ≤10이면 라벨 표시, 그 이상은 drawer 검토(후보) | map·ktc `AppShell` | `ux` §3.4 |
| off-canvas drawer(옵션) | 폭 `min(280px, 84vw)`, 상단 56px topbar, backdrop, 닫힘 시 `inert`, focus trap, body scroll lock, hydration 전 `visibility` 처리. 단위 테스트로 포커스 순서 고정 | geo `AppShell.tsx` + `tests/unit/app-shell-drawer.test.tsx` | `ux` §1.1 |
| 하단 탭바(사용자 웹) | 4 + 더보기 시트, 앱 밖 목적지는 시트로, 셸 밖 페이지(여행 상세 등)는 chrome 제거 허용, `--app-tabbar-h` 56px | pinvi `AppShell.tsx` | `ux` §3.4 |

셸 골격 코드는 `@kor-travel/ui`가 아니라 레지스트리 채널 템플릿(T-211)으로 배포한다(D-10). nav 정본·접힘·RBAC는 앱 소유([ui-components 조사](../survey/cross/ui-components.md) §4.3).

## 10. 표의 모바일 대체

**RW-10 (SHOULD)** `md` 미만에서 표를 카드로 대체할 때는 같은 데이터·같은 testid 계약을 유지한다([ux-guide](ux-guide.md) UX-G2.7). pinvi `AdminTable mobileCard`(`data-testid="admin-mobile-cards"`)와 kta `desktop-lot-table`/`mobile-lot-grid`가 선례다. 카드 전환은 앱 어댑터 책임이며 공통 `DataTable`은 카드를 렌더하지 않는다([ui-contract](ui-contract.md) DataTable). 대안으로 표 컨테이너만 가로 스크롤(ktdm)과 `<details>` 접기(kta)를 허용한다.

## 11. e2e 뷰포트

**RW-11 (SHOULD)** e2e 기본 프로젝트는 `Desktop Chrome`(1280×720)이고, 6폭 기준선 스펙(§3)을 별도 프로젝트로 둔다. 사용자 웹은 모바일 셸 회귀 스펙(pinvi `app-shell-mobile.e2e.ts`)을 유지하고, 터치 타깃 단언은 `getBoundingClientRect().height >= 44`(사용자)·`>= 36`(admin) 패턴으로 쓴다(pinvi `admin-feature-requests.e2e.ts` 선례). Playwright mocked/live 이중 suite 규약은 [frontend-stack](frontend-stack.md) §8.

## 12. 앱별 현재 격차와 재조정

| 앱 | 현재(사실) | 규약 | 조치 |
|---|---|---|---|
| weather | 셸 전환 62rem(992px), 42rem(672px); rail 17rem·접힘 없음 | `lg`/`md`; 16rem + 접힘 | 셸 교체 PR(T-463)에서 정렬. 그 전에는 매니페스트 예외 |
| kta | 860/980/560/380, JS `innerWidth < 860` | 콘텐츠 breakpoint는 `md`/`lg` | admin 셸이 없으므로 860은 콘텐츠 값으로 잔존 허용, T-432에서 768/1024 재조정 검토 |
| ktdm | 64rem/48rem | = `lg`/`md` | 일치. 표 영역만 가로 스크롤 유지 |
| ktc | `useIsMobile` `(max-width: 767px)` | = `md` 미만 | 일치 |
| geo | `(max-width: 1023px)` drawer | = `lg` 미만 | 일치(drawer 옵션) |
| pinvi admin | strip 항목 44px 아이콘 전용, 접힘 5rem | 36px 행, 4rem | C1·C6 예외 등록(T-422) |
| pinvi 사용자 웹 | 문서 744/1128/1440, 코드 Tailwind 기본 | Tailwind 기본 | 문서 정정은 pinvi 소유 |
| 안전영역 | ktc bulk 바·pinvi 탭바만 | §6 | 신규 하단 고정 바에 적용 |

## 13. 검증 요약

| 검사 | 도구 | 시점 |
|---|---|---|
| 6폭 시각 기준선·`scrollWidth` | `templates/playwright.baseline.ts` | 토큰·스타일·셸 변경 PR(착수 전·완료 후) |
| 터치 타깃·44px 예외 | 앱 e2e | 채택 PR |
| breakpoint·overflow 위반 | 2인 리뷰(grep: `max-width: 62rem`, `overflow-x: hidden`, 커스텀 `--breakpoint-`) | 채택 PR |
| 다크 기준선 | dark 활성 앱만 | 활성화 PR |

## 14. 열린 결정

| # | 항목 | 기본값(이 문서) |
|---|---|---|
| O-8 | pinvi mobile Tailwind 3 예외 | 미등록(사용자 승인 대기), 규칙은 수치만 공유 |
| O-11 | 다크 모드 | light 기본, opt-in |
| O-21 | pinvi admin 44px 2쪽 | 영구 예외 |
| — | strip 항목 수 상한(≤10) | 후보, T-211에서 확정 |
| — | kta 860 콘텐츠 breakpoint | 잔존 허용, T-432 재검토 |

## 15. 근거

- 표면 분류·breakpoint·터치·안전영역·셸 전략: [ux-patterns 조사](../survey/cross/ux-patterns.md) §1.1·§1.11·§3·§4 C1~C6·C11·C13·C14.
- 밀도 토큰·프로필: [design-tokens 조사](../survey/cross/design-tokens.md) §3.1.2·§3.6.5.
- kta 320px 게이트·overflow clip 결정: [airport 인벤토리](../survey/inventory/kor-travel-airport.md) §3·§9.
- pinvi 모바일 판정·모달 계약: [pinvi 인벤토리](../survey/inventory/pinvi.md) §3.
- 결정: [설계 브리프](../plan/design-brief.md) D-08·D-13·D-21·D-29, O-8·O-11·O-21.
