# UX 가이드 — admin·사용자 표면 공통 규칙(UX-G0~G9)

- 정본 지위: 이 문서는 kor-travel 제품군 웹 표면의 **구조·밀도·상태·접근성·문구 규칙**의 정본이다. 색 값·nav 항목·권한·라우트는 앱이 소유한다(UX-G0.1). PC/Mobile 수치는 [responsive-web](responsive-web.md), 토큰은 [design-tokens](design-tokens.md), 컴포넌트 마크업은 [ui-contract](ui-contract.md)가 정본이며 여기서는 링크만 한다.
- 확정 task: **T-105**. 이 판은 [ux-patterns 조사](../survey/cross/ux-patterns.md) §2 G0~G9와 §4 C1~C22를 브리프 D-13 결정으로 옮긴 초안이다. 마지막 갱신: 2026-09-06.
- 근거 약칭: `ux` = ux-patterns 조사, `dt` = [design-tokens 조사](../survey/cross/design-tokens.md), `ui` = [ui-components 조사](../survey/cross/ui-components.md), `inv/<app>` = [인벤토리](../survey/README.md) §3.1.

## 0. 적용 범위와 수준

| 항목 | 규칙 |
|---|---|
| 규칙 ID | `UX-Gn.m`(장 n, 규칙 m). 조사 §2의 번호를 그대로 승계했으므로 조사 문서와 1:1 대조할 수 있다 |
| 수준 | **MUST** = 브리프 D-13이 결정한 항목(§3 C1~C22 판정 포함) 또는 4앱 이상에서 사실로 확인된 규칙. 나머지는 **SHOULD**. 보안 경계에 닿는 규칙(UX-G6.6·G7.3)은 근거 앱 수와 무관하게 MUST |
| 신규 vs 기존 | 신규 코드는 MUST를 예외 없이 따른다. 기존 잔존 위반은 앱별 baseline(§5)에 등록하고 **신규 위반만** fail |
| 장 분리 | §1 admin 표면(map·ktc·geo·ktdm·weather·pinvi admin·airport 백업 패널), §2 사용자 표면(pinvi 사용자 웹·모바일 앱·kta 대시보드). 밀도 규칙이 다르므로 한 규칙을 두 표면에 그대로 적용하지 않는다(`ux` G0.2) |
| 검사 | grep 가능한 금지 패턴(§4)은 `tools/ux_lint.py`(T-103)가 전체 report + `--base <sha>` diff-based fail. 나머지 규칙은 2인 리뷰와 e2e |
| 도구·엔진 | 토스트·모달 엔진은 앱 소유(D-09). 이 문서는 행동 계약만 정한다 |
| 인용 금지 | Hallmark SKILL 본문·map `design.md` 원문을 인용하지 않는다(라이선스 B3). 규칙 근거는 조사 문서 절로만 가리킨다 |

## 1. admin 표면

### UX-G0. 범위와 소유

| ID | 규칙 | 수준 | 근거 |
|---|---|---|---|
| UX-G0.1 | common은 구조·밀도·상태·접근성·문구 규칙을 소유하고, 브랜드 색·nav 항목·권한·라우트는 앱이 소유한다 | MUST | `ux` G0.1(5앱 동일 선언) |
| UX-G0.2 | admin 표면과 사용자 표면은 장을 분리하고, 한 앱에 공존할 때는 스코프 셀렉터(`[data-kt-surface]`)로 밀도를 나눈다 | MUST | `ux` G0.2, `dt` §3.6.5 |
| UX-G0.3 | 규칙 문서는 grep 가능한 금지 패턴 목록(§4)을 포함하고, 도구가 그 목록만 검사한다 | MUST | `ux` G0.3, D-13 |

### UX-G1. 셸(Rail-Workbench)

| ID | 규칙 | 수준 | 근거 |
|---|---|---|---|
| UX-G1.1 | 데스크톱(≥1024px): 좌측 rail 16rem, 접힘 4rem. 접힘 상태는 `localStorage "<app>:sidebar-collapsed"`에 저장 | MUST | `ux` G1.1(4앱), C1·C2 |
| UX-G1.2 | <1024px: rail은 상단 가로 strip으로 전환하고 활성 항목을 `scrollIntoView`(reduced-motion 시 `behavior: "auto"`)한다. off-canvas drawer는 허용 옵션이며 UX-G4.8의 모달 접근성 계약을 동일하게 만족해야 한다 | MUST(계약) / strip 기본 SHOULD | `ux` G1.2, C4 |
| UX-G1.3 | skip link → `<main id="main-content" tabIndex={-1}>`(링 끔은 이 컨테이너만). 대상 id는 앱이 바꿀 수 있으나 한 앱에 하나 | MUST | `ux` G1.3(5앱) |
| UX-G1.4 | 활성 nav = `aria-current="page"` + 색 이외의 형태(좌측 2px brand mark) + `bg-kt-brand-tint` | MUST | `ux` G1.4(4앱), C5 |
| UX-G1.5 | 헤더 밴드 순서: breadcrumb 또는 section → h1(+HelpTip) + actions(primary ≤1, secondary ≤2) → meta → description, 아래 hairline. 현재 pathname 문자열을 헤더에 노출하지 않는다 | MUST | `ux` G1.5(4앱), C16 |
| UX-G1.6 | 로그아웃은 rail footer(데스크톱)/상단 아이콘(모바일). 별도 사이트 footer 없음 | MUST | `ux` G1.6(4앱) |
| UX-G1.7 | nav 정본은 셸 밖 모듈(`admin-pages.ts` 형태)에 두어 h1·nav 라벨·e2e가 같은 문자열을 소비한다. 활성 판정(longest-prefix)은 단위 테스트로 고정 | SHOULD | `ux` G1.7 |
| UX-G1.8 | 우측 inspector rail(`--kt-rail` 22rem)은 `xl`(1280px) 이상에서만 2열 | SHOULD | `ux` G1.8(2앱) |
| UX-G1.9 | nav 항목의 접근성 이름은 라벨만이다. 스프린트·상태 같은 운영 정보는 `data-*` 또는 시각 보조 텍스트로 둔다 | MUST | `ux` C20, D-13 |

### UX-G2. 목록 화면

| ID | 규칙 | 수준 | 근거 |
|---|---|---|---|
| UX-G2.1 | 툴바는 `FilterBar/FilterField/FilterActions`: 가시 라벨 위·hint 아래·wrap, 가로 스크롤 금지. 정렬은 컬럼 헤더, page-size는 pager | SHOULD | `ux` G2.1(2앱) |
| UX-G2.2 | 표는 4상태(loading skeleton + `aria-busy` / empty / error + `다시 시도` / data)를 표 내부에서 렌더한다 | MUST(공통 DataTable 사용 시) / SHOULD | `ux` G2.2, D-09 |
| UX-G2.3 | 서버 페이징 목록은 서버 정렬(`manualSorting: true`). 클라이언트 정렬은 전체 데이터를 보유한 목록에만. "현재 페이지 안에서만 정렬"을 사용자에게 숨기지 않는다 | MUST | `ux` G2.3, C10, D-09 |
| UX-G2.4 | pager 라벨 `첫 페이지/이전/다음/마지막 페이지`, 요약 `페이지 n / m · 총 N건`, 경계는 native disabled, 전환 중 `loading`(포커스 유지) | SHOULD | `ux` G2.4(2앱) |
| UX-G2.5 | 행 선택 목록은 `role="listbox"/"option"` + roving tabindex(↑↓/Home/End). 선택 = tint + 2px mark. disabled 사유는 흐리지 않고 `title`로 | SHOULD | `ux` G2.5 |
| UX-G2.6 | 행 체크박스 접근성 이름 `"{행 라벨} 선택"`, bulk 액션은 선택 시 표 위 `role="region"` 바 | SHOULD | `ux` G2.6 |
| UX-G2.7 | 모바일 표 대체(카드)는 표와 같은 데이터·testid 계약을 유지한다 | SHOULD | `ux` G2.7(2앱), [responsive-web](responsive-web.md) §10 |

### UX-G3. 상세·편집

| ID | 규칙 | 수준 | 근거 |
|---|---|---|---|
| UX-G3.1 | 섹션 컨테이너는 1층(카드 안 카드 금지). `SectionCard`(헤더 hairline + flat body, `headingLevel`) | MUST | `ux` G3.1(6앱) |
| UX-G3.2 | 상세 dl은 `DetailList`: `—` null glyph, 식별자 mono, `tabular-nums`, copyable·help 슬롯 | SHOULD | `ux` G3.2(3앱) |
| UX-G3.3 | 폼 필드 = 라벨 위 · 컨트롤 · 메시지 슬롯 1개 예약(error가 hint를 대체). `aria-describedby`는 표시 중인 메시지만. required `*`는 `aria-hidden`이고 접근성 이름에서 제외 | SHOULD | `ux` G3.3(admin·user 동일) |
| UX-G3.4 | 제출 실패 시 첫 오류 필드로 포커스(규칙 순서 = 포커스 순서) | SHOULD | `ux` G3.4(2앱) |
| UX-G3.5 | 파괴적 설정 변경은 저장 전 변경 전/후 diff 미리보기 | SHOULD | `ux` G3.5(ktdm) |
| UX-G3.6 | dirty 이탈 경고(`beforeunload`) | **규칙 없음**(열림 O-22: 8표면 모두 미구현, 기본값 "미포함") | `ux` G3.6·§5-2 |

### UX-G4. 피드백

| ID | 규칙 | 수준 | 근거 |
|---|---|---|---|
| UX-G4.1 | 성공은 조용히: 자기 영역이 다시 그려지는 mutation은 토스트를 띄우지 않고, 교차 페이지 효과만 토스트. 성공 Alert 없음. 토스트 **엔진**은 앱 소유이며 common은 이 정책만 배포 | MUST | `ux` G4.1, C8, D-09 |
| UX-G4.2 | 오류는 what / why / what-to-do 3부 + 회복 행동 1~2개. stack trace만 남는 dead-end 금지. 요청 ID가 있으면 항상 노출 | MUST | `ux` G4.2, C19 |
| UX-G4.3 | 런타임 오류는 chunk/RSC/network 계열에 한해 같은 pathname 1회 hard reload(`sessionStorage` 플래그), 반복 시 오류 패널. `AppErrorPanel` 계보(geo 원천, 5앱 동일)가 공통 | MUST | `ux` G4.3(5앱), C19 |
| UX-G4.4 | 빈 상태 = 좌측 정렬, 무엇이 비었나 1문장 + 다음 행동 1개. dashed 테두리·가운데 정렬·아이콘 타일 금지 | MUST | `ux` G4.4, C11 |
| UX-G4.5 | 로딩: 형태가 정해진 목록/카드는 Skeleton(`aria-hidden`, 감싸는 영역 `aria-busy`), 인라인 액션은 버튼 스피너(라벨 유지), 페이지 스피너는 목적지 불명확한 대기만 | SHOULD | `ux` G4.5 |
| UX-G4.6 | 파괴적·비가역 행동은 공용 확인 다이얼로그: 질문형 제목 + 결과 1줄, **동사 라벨 필수**(`확인`/`OK`/`예` 금지, 기본값 없음), 취소 초기 포커스, destructive 채움은 다이얼로그 안에서만. `window.confirm` 금지(§4 P8) | MUST | `ux` G4.6, C7 |
| UX-G4.7 | 가역 행동은 즉시 실행 + Undo 스낵바(`role="status"`), 마지막 1건 | SHOULD | `ux` G4.7 |
| UX-G4.8 | 모달 접근성 계약: 열릴 때 포커스 이동, Tab trap, Escape 닫기, 닫힐 때 트리거로 복원(분리된 트리거면 생략), body scroll lock, 배경 `inert`. 한 화면에 두 모달 스택을 섞지 않는다. 엔진(base-ui·radix·자체 훅)은 앱 소유 | MUST | `ux` G4.8(3앱), C18 |

### UX-G5. 상태 표현

| ID | 규칙 | 수준 | 근거 |
|---|---|---|---|
| UX-G5.1 | 5-tone: `success`(활성·완료) · `warning`(사람 결정 대기·저하) · `destructive`(실제 잘못된 것만) · `info`(정보·기계 진행 중) · `neutral`(보관·비활성·정상 취소) | MUST | `ux` G5.1, C9 |
| UX-G5.2 | enum raw 렌더 금지. 라벨은 `statusLabel()` 단일 정본, 같은 한글 라벨은 같은 tone(테스트로 잠금) | SHOULD | `ux` G5.2 |
| UX-G5.3 | 배지는 dot + 텍스트(색 단독 의미 전달 금지) | MUST | `ux` G5.3(4앱) |
| UX-G5.4 | HTTP 코드 tone: 2xx neutral · 3xx info · 4xx warning · 5xx destructive | SHOULD | `ux` G5.4 |
| UX-G5.5 | 상태색은 dot·배지·소수치 강조에만. 큰 표면 채움 금지 | SHOULD | `ux` G5.5(2앱) |
| UX-G5.6 | 값 없음은 `—`, 단위는 값이 있을 때만, 로딩 중 가짜 0 금지. stale·추정 값을 확정값처럼 렌더하지 않는다 | SHOULD | `ux` G5.6, [canview 체크리스트](../survey/cross/canview-structure-checklist.md) A6.13 |

C9 부속 결정: ktdm `ok/warn/danger`는 이름 alias(ok=success, warn=warning, danger=destructive), kta 도메인 5단계(`full/critical/warning/busy/stable`)는 앱이 tone 매핑표를 둔다, weather는 `statusLabel` 도입(T-463), geo `CANCELLED → warn`은 도메인 의미 확인 전까지 **보류**(neutral로 바꾸지 않는다).

### UX-G6. 위험 작업

| ID | 규칙 | 수준 | 근거 |
|---|---|---|---|
| UX-G6.1 | 복원·교체류는 단계형(선택 → 미리보기 → dry-run → 확인·실행) + typed confirmation(정확 문구 입력, 복사 버튼 없음, 일치 여부 `aria-live`) | SHOULD | `ux` G6.1(geo) |
| UX-G6.2 | 확인 문구에 영향 범위(대상 수·이름·DB 포함 경고)를 명시 | SHOULD | `ux` G6.2(ktdm) |
| UX-G6.3 | 장기 작업은 phase 목록 + 상태 아이콘으로 진행 표시 | SHOULD | `ux` G6.3 |
| UX-G6.4 | 필요 역할을 다이얼로그 안에 안내 | SHOULD | `ux` G6.4 |
| UX-G6.5 | UI에서 막은 작업은 CLI 명령 원형을 제시(`CopyableCommand`) | SHOULD | `ux` G6.5 |
| UX-G6.6 | 개발 전용·위험 버튼은 클라이언트 게이트만으로 부족하다. 서버가 차단해야 하며 UI 숨김을 "유일한 방어선"으로 두지 않는다 | MUST(보안) | `ux` G6.6(ktdm T-044 교훈), [openapi](openapi.md) |

### UX-G7. 로그인

| ID | 규칙 | 수준 | 근거 |
|---|---|---|---|
| UX-G7.1 | 단일 가운데 열, 타이포 워드마크, 카드 프레임·아이콘 타일 없음, 항상 렌더되는 오류 live region, 제출 중 CTA는 `loading`(탭 순서 유지) | MUST | `ux` G7.1, C15 |
| UX-G7.2 | 오류 문구는 상태 코드/오류 코드 → 한국어 맵(503 설정 누락 / 429 시도 제한 / 403 출처 / 기타 자격 증명) | MUST | `ux` G7.2(5앱) |
| UX-G7.3 | `next` 리다이렉트 경로는 로컬 경로만 허용(`sanitizeLocalPath`) | MUST(보안) | `ux` G7.3(weather) |

공용 `LoginForm`은 T-214에서 접근성·오류·상태 슬롯과 입력 계약을 제공한다. endpoint·IdP·redirect·세션 왕복·운영 rate limit은 앱이 주입하고 소유한다. 앱별 셸 골격과 로그인 페이지 조립은 레지스트리 채널 템플릿(T-211) 또는 소비자 코드가 담당한다([ADR-015](../adr/015-common-shared-systems-scope.md)).

### UX-G8. 도움말·복사·JSON·지도

| ID | 규칙 | 수준 | 근거 |
|---|---|---|---|
| UX-G8.1 | HelpTip: 24px 박스 + 의사요소로 40px 히트(히트 ≥24px는 MUST). hover 800ms/focus 0ms tooltip + click popover가 기본이고 popover-only는 허용 하위집합. 접근성 이름 `도움말: {label}` | 히트 MUST / 나머지 SHOULD | `ux` G8.1, C17 |
| UX-G8.2 | CopyButton: 아이콘 스왑 + sr-only live `복사됨`, 비보안 컨텍스트·실패는 인라인 상태(토스트는 앱 주입) | SHOULD | `ux` G8.2(3앱) |
| UX-G8.3 | JSON은 `JsonViewer`(mono 12px, `—`, copyable, destructive tone) 또는 접이식 | SHOULD | `ux` G8.3 |
| UX-G8.4 | 지도 엔진·VWorld 스타일 빌더는 common 범위 밖(`maplibre-vworld-*` 유지). 배포 경로 4종 정리는 T-505 | MUST(범위) | `ux` G8.4, C22 |

### UX-G9. 접근성·모션·타이포(횡단)

| ID | 규칙 | 수준 | 근거 |
|---|---|---|---|
| UX-G9.1 | focus 링 = `outline 2px` 불투명 토큰 + offset 2px, 즉시 표시(transition 밖). `outline-none` 금지. 끄는 자리는 프로그램 포커스 컨테이너 닫힌 목록뿐 | MUST | `ux` G9.1, [design-tokens](design-tokens.md) TK-8 |
| UX-G9.2 | `disabled`와 `aria-disabled` 두 벌. 진행 중은 `aria-busy` + `aria-disabled`(native disabled 안 걺, 포커스 유지). 흐림은 root가 아니라 라벨 자식 래퍼에만 | MUST | `ux` G9.2, D-09 Button |
| UX-G9.3 | reduced-motion 전역 규칙 + "사라지면 상태를 알 수 없는 애니메이션(스피너)은 유지, 자리표시(skeleton)는 끈다" | MUST | `ux` G9.3, §1.12(7앱 전역 규칙 보유) |
| UX-G9.4 | 전환 유틸은 열거형만. `transition-all`·`transition-colors`·맨 `transition` 금지(v4 전환 목록에 `outline-color`가 포함돼 링이 페이드된다) | MUST | `ux` G9.4, §4 P1 |
| UX-G9.5 | 한글 라벨에 `uppercase`·`tracking-*` 금지 | MUST | `ux` G9.5(4앱) |
| UX-G9.6 | admin 타입 스케일 7단(12/13.5/15/17/20/24/30), 본문 15px, 최소 12px, `text-[Npx]` 금지 | MUST | `ux` G9.6, C13, [design-tokens](design-tokens.md) TK-3 |
| UX-G9.7 | radius 2종(6px 컨트롤/8px 패널), 컨트롤 높이 2종(36/30px). micro-control(≥24px)은 정렬 버튼·닫기·HelpTip·Copy 등 닫힌 목록만 | MUST | `ux` G9.7(6앱), `dt` §3.1.2 |
| UX-G9.8 | hairline 2종: 장식 `border-kt-border` vs 컨트롤 경계 `border-kt-control-line`(3:1). 장식선을 입력 경계에 쓰지 않는다 | MUST | `ux` G9.8, TK-4·TK-8 |
| UX-G9.9 | `html, body { overflow-x: clip }`(`hidden` 금지). 표·지도·작업면만 자체 overflow | MUST | `ux` G9.9(4앱), [responsive-web](responsive-web.md) §7 |
| UX-G9.10 | 다크 모드는 light 기본. 다크 값은 토큰이 준비하고 활성화는 앱 opt-in | MUST | `ux` C14, TK-7 |

## 2. 사용자 표면(pinvi 사용자 웹·모바일 앱·kta 대시보드)

사용자 표면은 **코드 소비 대상이 아니다**(D-29). consumer 프로필의 값·밀도·어휘(`canvas/ink/hairline/cta`)와 Hallmark 잠금 시스템은 pinvi `DESIGN.md`가 소유하며 common은 인용하지 않는다. 아래는 admin 규칙 중 사용자 표면에 그대로 적용되는 것과 대체되는 것의 대응표다(근거: `ux` §1.11·§1.14·§3.1·§3.3).

| admin 규칙 | 사용자 웹(pinvi) | 모바일 앱(pinvi mobile) | kta 대시보드 | 수준 |
|---|---|---|---|---|
| UX-G1.1~1.2 셸 | 하단 탭바 4 + 더보기(`--app-tabbar-h` 56px), `lg` 이상 상단 탭. 판정은 뷰포트 + 포인터 능력(UA 스니핑 금지) | 네이티브 Stack 헤더 | 셸 없음(단일 페이지, 860px 이하 카드·`<details>`) | MUST(각 표면 사실) |
| UX-G1.3 skip link | 유지 | 해당 없음 | 도입 권고 | SHOULD |
| UX-G1.4 활성 nav | 색 이외 형태 유지(ink 2px 밑줄 / 탭바 바) | 탭 아이콘 + 라벨 | — | MUST(형태 원칙) |
| UX-G2.x 목록 | 표 대신 row divider 리스트·카드. 4상태 원칙 동일 | 동일 | 표 ↔ 카드 전환은 같은 testid 계약(UX-G2.7) | SHOULD |
| UX-G3.3 폼 슬롯 | 동일(메시지 슬롯 1개 예약, `role="alert"`), 컨트롤 44px·16px 입력 | 48px | 기본 `<label><input>` | SHOULD |
| UX-G4.1 성공 조용히 | 동일(`role="status"`, 축하 토스트 금지) | 동일 | — | MUST |
| UX-G4.4 빈 상태 | 좌정렬(`FullPageMessage`) | **가운데 허용**(플랫폼 관용, C11) | `notice` 좌정렬 | MUST / 모바일 앱 예외 |
| UX-G4.6 확인 | 동사 라벨 필수. `ConfirmDialog` 기본 라벨 `'확인'`은 제거 대상(C7) | `lib/confirm.ts` 동일 원칙 | `window.confirm` 1건 baseline | MUST |
| UX-G4.8 모달 계약 | `useModalDialog`(inert·trap·복원) — 계약 동일, admin base-ui와 스택 혼용 금지 | — | — | MUST |
| UX-G5 상태 | 상태 UI 4종(empty/loading/error/success)·색 단독 금지 동일 | 중립 배지 1종(색 의미 없음) | 도메인 5단계 → tone 매핑표 | SHOULD |
| UX-G6 위험 작업 | 해당 없음(사용자 표면에 파괴 작업 없음) | — | 복원은 admin 규칙(UX-G6.2) 적용 | — |
| UX-G7 로그인 | `(auth)/login` 세부 미확인 — 규칙 적용 보류 | — | 무인증 | 미확인 |
| UX-G8.1 툴팁 | hover 800ms/focus 0ms 동일, 히트 44px | — | — | SHOULD |
| UX-G9.1·9.3 focus·모션 | `.focus-ring` 동일 레시피, reduced-motion 전역 | reduced-motion 전역 | 동일 | MUST |
| UX-G9.6 타이포 | 본문 16px(입력 포함, iOS 확대 방지), 12px 이하 금지(배지 예외) | 16 / 14 / 12 | 12.8px~, 11px 1건은 정렬 대상 | MUST(하한) |
| UX-G9.7 밀도 | 44px 터치, `sm`은 coarse pointer에서 44px 승격, radius 8/14/20/32 | 48px 버튼·입력, 44px 체크박스·칩 | — | MUST(표면별) |
| UX-G9.9 overflow | `overflow-x: clip` 동일 | — | 동일 | MUST |

## 3. 충돌 결정(C1~C22)

브리프 D-13이 risk-first 판정을 채택했다. "반영" 열의 규칙 ID가 정본이고, 앱별 후속 작업은 [통합 계획](../plan/integration-plan.md)의 task ID다.

| # | 충돌 | 결정 | 반영 | 후속·예외 |
|---|---|---|---|---|
| C1 | 접힌 rail 4rem vs 5rem | 4rem | UX-G1.1 | pinvi admin 5rem은 "터치 admin 변형"으로 매니페스트 예외 등록(T-422) |
| C2 | weather rail 17rem·접힘 없음·문서 불일치 | 16rem + 접힘 규약 | UX-G1.1 | weather는 shim에서 `--rail` 17rem 오버라이드 유지 후 셸 교체(T-461·T-463)로 닫음 |
| C3 | 셸 전환 1024 vs 992 vs 860 | 1024(`lg`) | [responsive-web](responsive-web.md) §2 | weather 62rem 재조정(T-463); kta 860은 콘텐츠 breakpoint로 잔존 검토 |
| C4 | strip vs drawer | strip 기본 + drawer 옵션, a11y 계약 동일 | UX-G1.2·G4.8 | geo drawer 유지 |
| C5 | 활성 nav tint+mark vs ink 채움 vs 밑줄 | admin은 tint + mark | UX-G1.4 | pinvi admin은 mark 추가 권고(T-422); 사용자 웹은 §2 |
| C6 | 컨트롤 36/30 vs 44 vs 48 | 표면별 분리 | UX-G9.7, §2 | pinvi admin 44px 2쪽(`feature-requests`·`feature-reference-reconciliations`) **영구 예외**(열림 O-21) |
| C7 | 확인 다이얼로그 라벨·`window.confirm` | 동사 라벨 필수·기본값 없음·`window.confirm` 금지 | UX-G4.6, §4 P8 | baseline 7건(§5); pinvi `ConfirmDialog` 기본 `'확인'`, geo `"실행"`, ktc `"삭제"` 기본값은 제거 대상 |
| C8 | 토스트 엔진·성공 토스트 | 정책 통일, 엔진 앱 소유 | UX-G4.1 | ktdm 성공 토스트 6초는 이관 시 정리(T-473) |
| C9 | 상태 tone 이름 | 5-tone 채택 | UX-G5.1 | geo CANCELLED 매핑 보류 |
| C10 | 정렬 기본값 | 페이징 목록 = 서버 정렬, DataTable `manualSorting` 기본 `true` | UX-G2.3, [ui-contract](ui-contract.md) DataTable | pinvi `AdminTable`은 `false` 명시 유지 |
| C11 | 빈 상태 정렬 | 좌정렬, 모바일 앱만 가운데 허용 | UX-G4.4, §2 | ktdm 모달 EmptyState 가운데 → 정렬(T-473) |
| C12 | 폰트 스택 | Pretendard 1순위(로드하는 앱), 로딩은 앱 | [design-tokens](design-tokens.md) TK-12 | weather Geist 1순위·ktdm Noto 1순위는 채택 시 오버라이드 |
| C13 | 본문 14px·11px | 15/12 하한 | UX-G9.6 | ktdm·kta 스케일 정렬 |
| C14 | 다크 자동 vs 준비 vs 없음 | light 기본, `.dark` 슬롯 준비, kta media dark 허용 | UX-G9.10, TK-7 | 열림 O-11 |
| C15 | 로그인 아이콘 타일 vs 워드마크 vs graphite 분할 | 타이포 워드마크 | UX-G7.1 | geo·weather 아이콘 타일 후속 정렬 |
| C16 | 헤더 2종 공존·pathname 노출 | breadcrumb/section만 | UX-G1.5 | pinvi `AdminPage` → `AdminPageHeader` 수렴; weather `page-path` 제거 |
| C17 | HelpTip tooltip+popover vs popover-only | popover-only 허용 하위집합, 히트 ≥24px 필수 | UX-G8.1 | — |
| C18 | 모달 엔진 3종 | 엔진 앱 소유 + 행동 계약 + 두 스택 혼용 금지 | UX-G4.8 | — |
| C19 | 오류 페이지 부재 | `AppErrorPanel` 계보 공통(T-205) | UX-G4.3 | weather·kta `error.tsx` 도입(T-463·T-432) |
| C20 | nav 접근성 이름에 운영 정보 | 라벨만 | UX-G1.9 | pinvi `(Sprint N)` 분리 |
| C21 | Hallmark 스탬프 형식 | common 배포 파일에는 Hallmark 스탬프 없음(SPDX 헤더 + `Origin:`만). SKILL 본문 인용 금지. 이식 파일의 출처 앱 스탬프는 `PROVENANCE.md` 기록으로 대체 | §0 | [licensing](licensing.md) |
| C22 | 지도 스타일 빌더 배포 경로 4종 | 범위 밖 | UX-G8.4 | T-505 |

## 4. 금지 패턴(grep 목록)

`tools/ux_lint.py`(T-103)가 검사하는 패턴이다. map `design.md` 게이트 7종의 **의미**를 승계하되 정규식은 common이 새로 정의한다(원문 인용 금지). 대상: 앱 프론트엔드 소스(`*.ts`, `*.tsx`, `*.css`, `*.mdx`), 제외: `e2e/**`, `tests/**`, `*.test.*`, `node_modules`, `.next`, `vendor/**`, 생성물(`*.gen.ts`). 토큰 파일 allowlist(P4b 제외 대상)는 `--token-files` 인자로 넘긴다.

| ID | 패턴(ripgrep) | 잡는 것 | 대체 | 관련 규칙 |
|---|---|---|---|---|
| P1 | `(^\|[\s"'`])transition(-all\|-colors)?(?=[\s"'`]\|$)` | `transition-all`, `transition-colors`, 맨 `transition` | `transition-[color,background-color,border-color]`, `transition-opacity` | UX-G9.4 |
| P2 | `text-\[\d+(\.\d+)?px\]` | px 임의 폰트 크기 | `text-kt-2xs`~`text-kt-2xl` | UX-G9.6 |
| P3 | `rounded(-[a-z]{1,2})?-(2xl\|3xl\|4xl\|\[)` | 큰 radius·임의 radius | `rounded-kt-control`, `rounded-kt-panel` | UX-G9.7 |
| P4a | `(bg\|text\|border\|outline\|ring\|fill\|stroke\|from\|to\|via)-\[(#\|oklch\(\|rgba?\(\|hsla?\()` | 클래스 안 raw 색 | `bg-kt-*` 토큰 유틸리티 | TK-9 |
| P4b | `#[0-9a-fA-F]{3,8}\b\|oklch\(\|rgba?\(\|hsla?\(` (CSS, allowlist 밖) | 토큰 파일 밖 raw 색 | 토큰 파일로 이동 | TK-9 |
| P5 | `\b(bg\|text\|border\|ring\|outline\|fill\|stroke\|from\|to\|via\|shadow)-[a-z][a-z0-9-]*/\d{1,3}\b` | 팔레트 alpha | 불투명 tint 토큰, overlay 토큰 | TK-9 |
| P6 | `\boutline-none\b` | 포커스 링 제거(모든 variant 접두 포함) | `focus-visible:outline-0`(닫힌 목록만) | UX-G9.1 |
| P7 | `aria-(disabled\|busy):opacity-` | root 흐림 | 라벨 자식 래퍼 `opacity-55` | UX-G9.2 |
| P8 | `\bwindow\.confirm\b\|(^\|[^.\w])confirm\(` | 브라우저 확인 대화상자 | 공용 확인 다이얼로그 | UX-G4.6 |

- 제외 규칙: 행에서 패턴이 백틱(`` ` ``)으로 감싸여 있으면(주석·문서 인용) 무시한다. 인라인 억제 주석은 두지 않는다 — 예외는 baseline 파일(§5)로만.
- 출력: 전체 트리 report(패턴별 건수 + 파일:행) + `--base <sha>` 지정 시 diff에 새로 추가된 행만 fail(exit 1). CI는 PR에서 `--base origin/main`, 주간 실행은 report만.
- 명령: `python3 -B -X utf8 tools/ux_lint.py --root <frontend-dir> --baseline <baseline.json> [--base <sha>] [--token-files tokens.css,brand.css]`. Windows Python에서도 동작해야 한다(D-03, `tools` CI 매트릭스).

## 5. 기존 위반 baseline

baseline은 앱 저장소 파일이며 매니페스트 `ux_gate.baseline`이 경로를 가리킨다(D-19). 형식(후보, T-103 확정):

```json
{
  "schema": "kor-travel-common.ux-baseline.v1",
  "entries": [
    { "rule": "P8", "path": "src/.../curation-collections-client.tsx", "count": 2,
      "reason": "useConfirm 이관 전", "until": "2026-12-31", "task": "T-412" }
  ]
}
```

- `count`는 상한이다. 같은 파일에서 건수가 늘면 fail, 줄면 baseline을 같은 PR에서 갱신한다.
- `until` 경과 시 `EXEMPT_EXPIRED`로 `::error::` 주석(판정 어휘는 [versions.md](versions.md)와 동일).

초기 baseline(조사 시점 사실, D-13 "`window.confirm` 7건"):

| 앱 | 규칙 | 건수 | 위치(조사 grep 범위 기준, 등록 시 재확인) | 종료 task |
|---|---|---|---|---|
| map | P8 | 2 | `packages/kor-travel-map-admin/frontend/src/app/admin/features/curated/curation-collections-client.tsx` | T-412 |
| ktdm | P8 | 3(파일 수) | `frontend/src/components/*`(`DashboardClient.tsx`·`BackupHistoryPanel.tsx` 등, `ux` §1.12) | T-473 |
| kta | P8 | 1 | `frontend/src/components/backup-panel.tsx`(복원 확인) | T-432 |
| weather | P8 | 1 | API 키 삭제 확인(`app/settings/providers/page.tsx`, 추정 위치) | T-463 |

추가 baseline 후보(채택 PR에서 report로 확정): ktc `HelpTip` `text-[12px]`(P2), ktdm `text-[11px]`(P2)·`transition-all` 잔존 여부, kta `font-size: 11px`(CSS, 규칙 밖이나 UX-G9.6 정렬 대상), geo `tailwind.config.ts` raw hex(P4b, T-441에서 삭제). ktc의 `window.confirm` 1건은 주석이라 위반이 아니다(`ux` §1.12).

## 6. 마커 팔레트 규칙(common 소유는 규칙만)

| ID | 규칙 | 수준 | 근거 |
|---|---|---|---|
| UX-G5.7 | 카테고리 팔레트는 16슬롯 코드(`P-01`~`P-16`, 정규식 `^P-(0[1-9]\|1[0-6])$`)로만 데이터에 저장하고 hex는 렌더 시 정본에서 조회한다 | MUST | `dt` §3.5(map API 검증 규칙) |
| UX-G5.8 | 마커 위 라벨(가격·번호)은 마커 채움색 대비 4.5:1(본문 크기) 또는 3:1(≥18px bold). 미달 슬롯은 라벨을 어두운/밝은 ink로 자동 선택한다 | MUST | TK-13 원칙 적용 |
| UX-G5.9 | 마커 팔레트를 CTA·nav·상태 tone에 재사용하지 않는다 | MUST | pinvi `marker-palette.md` 운영 규칙(`dt` §3.5) |
| UX-G5.10 | hex 정본은 kor-travel-map(`map-marker-react` PALETTE 또는 `/v1/categories` 응답)이며 pinvi는 재수출한다. 두 벌 hex(Tableau vs Material) 해소는 map에 요청(열림 O-13, T-505) | MUST(소유) | `dt` §3.5, D-26 |

## 7. 예외 등록 절차

1. 규칙 ID·표면·사유·`until`·종료 task를 매니페스트 `exceptions[]`(형식 규칙)나 baseline(§5, grep 패턴)에 적는다.
2. 영구 예외(O-21 같은 사용자 결정)는 `until: null` + `review` 날짜를 둔다.
3. 예외는 채택 PR 본문의 검사 결과 표에 나타나야 한다([consumer adoption runbook](../runbooks/consumer-adoption.md)).
4. 예외 수 증가는 분기 회수 보고(D-28)의 지표다.

## 8. 열린 결정

| # | 항목 | 기본값(이 문서) |
|---|---|---|
| O-21 | pinvi admin 44px 2쪽 | 영구 예외 |
| O-22 | dirty 이탈 경고 | 규칙 없음(미포함) |
| O-11 | 다크 모드 | light 기본, opt-in |
| O-13 | 마커 hex 정본 | map 확정 요청 |
| — | geo `CANCELLED → warn` | 보류(도메인 확인) |
| — | 상단 strip 항목 수 상한(≤10 라벨 표시) | 후보, T-211 셸 템플릿에서 확정 |
| — | 규칙 번호 승계(map 감사 M/C 번호) | 승계하지 않음. 이 문서의 `UX-G` ID만 사용(`ux` §5-9) |

## 9. 근거

- 앱별 비교표·규칙 초안·PC/Mobile·충돌: [ux-patterns 조사](../survey/cross/ux-patterns.md) §1~§5.
- 토큰 운용 규칙·대비: [design-tokens 조사](../survey/cross/design-tokens.md) §3.4·§3.5.
- 컴포넌트 계약·엔진: [ui-components 조사](../survey/cross/ui-components.md) §3·§5.
- 금지 패턴 원형(의미만 승계)·스크립트 부재: [map 인벤토리](../survey/inventory/kor-travel-map.md) §8-5·§11-2.
- Hallmark 클래스 ESLint 가드 선례: [pinvi 인벤토리](../survey/inventory/pinvi.md) §8-7.
- 결정: [설계 브리프](../plan/design-brief.md) D-09·D-13·D-19·D-26·D-29·D-30, O-11·O-13·O-21·O-22.
