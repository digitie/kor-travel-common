# ADR-021: 관리자 셸의 모바일 좌측 drawer와 한 줄 상단 제목 바

- 상태: accepted
- 날짜: 2026-11-19
- 근거 문서: 소유자 요청(2026-11-19), [ux-guide](../standards/ux-guide.md) UX-G1, [responsive-web](../standards/responsive-web.md) RW-9, [ui-contract](../standards/ui-contract.md) §4.6·§4.7, [T-222](../tasks/T-222-admin-shell.md)
- Supersedes: UX-G1.2·UX-G1.5·RW-9의 "상단 strip 기본"과 헤더 밴드 순서, RW-9 끝의 "셸 골격 코드는 레지스트리 템플릿(T-211)으로 배포"(D-10의 셸 부분)

## 컨텍스트

일곱 관리자 화면 가운데 geo만 좁은 화면에서 drawer를 쓰고, 나머지는 lg(1024px) 미만에서 rail을 본문 위 가로 strip으로 쌓는다. 그 위에 앱 설명(예: "Weather Scraper / admin"), section 줄, `h1`, meta, description이 여러 줄로 쌓여 모바일에서 첫 화면의 상당 부분을 메뉴와 제목이 차지한다. 소유자는 2026-11-19에 두 가지를 요청했다.

1. 모든 관리자 화면의 모바일 메뉴는 위가 아니라 왼쪽으로 접힌다(햄버거로 여는 off-canvas drawer).
2. 페이지 제목은 맨 위에 둔다. 앱 설명은 쓰지 않고 "영역 - 페이지"(예: "날씨 - 날씨지도")만 보인다. 제목 아래 설명(예: "활성 위치 카탈로그 n곳")도 같은 맨 위 줄에 작은 글씨로 둔다. PC와 모바일 모두 적용한다.

목적은 쓸 수 있는 화면 넓이를 최대로 하는 것이다. 메뉴와 제목이 세로 공간을 차지하지 않아야 한다.

## 결정

1. **모바일(<1024px) 관리자 셸은 좌측 drawer다.** 상단 바 왼쪽의 메뉴 버튼(`aria-expanded`·`aria-controls`)으로 열고, 모달 접근성 계약(포커스 가둠, Esc 닫기, 배경 비활성·스크롤 잠금, 닫힌 뒤 포커스 복원)을 지킨다. 메뉴 항목으로 이동하면 닫고 본문으로 포커스를 옮긴다. `prefers-reduced-motion`에서는 움직임을 끈다. 가로 strip은 관리자 셸의 기본에서 뺀다.
2. **페이지 제목은 한 줄 상단 바(약 48px)다.** 순서는 [메뉴 버튼(모바일)] → `h1` "영역 - 페이지" → 작은 설명(말줄임, 전체는 `title` 속성) → 오른쪽 동작이다. 앱 설명 문구와 별도 section 줄은 두지 않는다. PC도 같은 바를 쓰고, 데스크톱 rail(16rem, 아이콘 4rem 접힘)은 유지한다.
3. **공통 구현은 `@kor-travel/ui`의 `AdminShell`·`AdminTopBar`·`AdminPageTitle`이다.** 일곱 앱이 같은 동작을 각자 다시 구현하지 않도록 셸 골격을 패키지에 둔다. nav 항목·권한·로그아웃·브랜드 색은 계속 앱이 주입한다(UX-G0.1). `AppMenu`는 셸 안에서 세로 목록으로 그려지도록 `orientation`·`compact`를 더하고, 기본값(`responsive`)의 마크업은 바꾸지 않는다.
4. **버전은 patch다.** 공개 API를 더하기만 하고 기존 export·prop 기본값·`data-slot`을 바꾸지 않으므로 [release](../runbooks/release.md) §1에 따라 ui 0.2.3이다. 내장 정책 bytes가 바뀌는 tokens·toast도 patch를 올린다(0.1.4·0.1.3).

## 대안 검토

- **strip 유지 + 높이만 줄이기**: 항목이 10개를 넘는 앱(map·pinvi)에서 strip 자체가 한 줄을 차지하고 가로 스크롤로 항목을 찾아야 한다. 요청의 "메뉴가 세로 공간을 차지하지 않아야 한다"를 만족하지 못한다.
- **레지스트리 템플릿(T-211)으로 셸 배포**: 앱마다 복사본이 생겨 포커스·이동 닫힘 같은 접근성 결함을 일곱 번 고쳐야 한다. T-211은 아직 BLOCKED이고 소유자가 즉시 적용을 요청했다.
- **선택형 `@kor-travel/admin-kit`(T-219)에 넣기**: admin-kit은 T-022·T-025 뒤로 막혀 있다. 셸은 이미 ui에 있는 `AppMenu`·Radix Dialog와 맞물리므로 ui에 둔다. admin-kit의 peer 범위(`>=0.2.1 <0.3.0`)와도 충돌하지 않는다.
- **0.3.0 minor**: 파괴 변경이 없어 SemVer 0.x 규칙상 patch가 맞다. minor는 rc·소비자 검증 절차를 요구해 적용을 늦춘다.

## 결과

- 소비자는 각 저장소의 이관 PR에서 자체 셸을 `AdminShell`로 바꾸고, 페이지 헤더의 section·meta·description을 상단 바의 `area`·`title`·`description`으로 옮긴다. 기존 `AppMenu`만 쓰는 화면은 0.2.3으로 올려도 그대로 동작한다.
- 상단 바가 페이지 `h1`을 만든다. `AdminPageHeader`(T-210 계획)의 여러 줄 헤더 밴드 대신 이 바를 쓴다.
- 레이아웃에 둔 셸은 서버 렌더 첫 화면의 제목을 셸 prop(nav 정본의 라벨)으로 받고, 페이지별 설명·동작은 `AdminPageTitle`이 hydration 직후 채운다.
- 소비자 build·e2e·시각 기준선 갱신은 각 저장소의 몫이며 common에서는 실행하지 않는다.

## 후속·적용 위치

- 구현: `packages/ui/src/admin-shell.tsx`, `packages/ui/src/app-menu.tsx`, 시험 `packages/ui/test/admin-shell.test.tsx`, 브라우저 smoke `packages/ui/smoke/admin-shell-browser.spec.ts`.
- 규칙: [ux-guide](../standards/ux-guide.md) UX-G1.2·G1.5·G1.6, [responsive-web](../standards/responsive-web.md) RW-9·§7, [ui-contract](../standards/ui-contract.md) §4.6·§4.7·UC-5.
- 소비자 이관: map·weather·transport·geo·concierge·docker-manager·pinvi admin의 셸 교체 task(각 저장소 소유).
