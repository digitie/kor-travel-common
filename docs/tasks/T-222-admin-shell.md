# T-222 관리자 셸(모바일 좌측 drawer·한 줄 상단 제목 바)과 ui 0.2.3 (2026-11-19, PR #70)

- 상태: DONE
- 우선순위: P1
- Gate: UI 단위·타입·lint·doctor, 정규 pack·Next webpack/Turbopack smoke·브라우저 smoke, 독립 2인 리뷰·CI
- 선행: 없음
- 외부 선행: 일곱 관리자 화면의 셸 교체·build·e2e는 각 소비자 저장소의 이관 PR이 소유한다.

## 목표

소유자 요청(2026-11-19)에 따라 모든 관리자 화면의 모바일 메뉴를 좌측 drawer로 접고, 페이지 제목과 설명을 한 줄 상단 바에 둔다. 앱 설명 없이 "영역 - 페이지"만 보인다. 결정과 대안은 [ADR-021](../adr/021-admin-shell-left-drawer-and-single-top-bar.md)이 정본이다.

## 고정 결정

- 공통 구현은 `@kor-travel/ui`의 `AdminShell`·`AdminTopBar`·`AdminPageTitle`·`formatAdminTitle`이며 `AppMenu`에 `orientation`·`compact`를 더한다([ui-contract](../standards/ui-contract.md) §4.7).
- 기존 `AppMenu` 기본(`responsive`) 마크업·클래스·prop 기본값은 그대로다. 공개 API 추가만 있으므로 ui 0.2.3 patch이고 내장 정책 bytes가 바뀌는 tokens 0.1.4·toast 0.1.3도 patch를 올린다([release](../runbooks/release.md) §1).
- 규칙은 [ux-guide](../standards/ux-guide.md) UX-G1.2·G1.5·G1.6과 [responsive-web](../standards/responsive-web.md) RW-9를 갱신한다.

## 구현 범위

1. `AdminShell`: 데스크톱 좌측 rail(16rem, 4rem 아이콘 접힘·localStorage 저장), lg 미만 메뉴 버튼과 Radix Dialog 기반 좌측 drawer(포커스 가둠·Esc·배경 비활성·이동 시 닫힘·lg 전환 시 닫힘·reduced-motion), skip link, `fillViewport`.
2. `AdminTopBar`: 한 줄(약 48px) 상단 바. `h1` "영역 - 페이지", 작은 설명 말줄임과 `title` 속성, 오른쪽 동작.
3. `AdminPageTitle`: 레이아웃의 셸 상단 바를 페이지에서 덮어쓰고 셸 밖에서는 상단 바를 직접 그린다.
4. 단위 시험, 예시(Preview)와 설치 smoke route·브라우저 spec, 문서·CHANGELOG·버전 축.

## 범위 밖

소비자 저장소 수정·배포, `AdminPageHeader`(T-210)의 다른 부품, admin-kit(T-219~T-221), 시각 기준선 등록.

## 예상 변경 파일

```text
packages/ui/src/{admin-shell.tsx,app-menu.tsx,index.ts}, packages/ui/package.json
packages/ui/test/admin-shell.test.tsx, packages/ui/examples/{Preview.tsx,preview.css}
packages/ui/smoke/{admin-shell-browser.spec.ts,playwright.radix.config.ts,next-app/**}
versions.json, frontend-dependencies.json, packages/*/dependency-policy.json, packages/{tokens,toast}/package.json, package-lock.json
docs/adr/021-*, docs/standards/{ux-guide,responsive-web,ui-contract,frontend-libraries}.md, CHANGELOG.md
```

## 수용 기준

- [x] `AppMenu` 기본 렌더의 클래스·DOM이 0.2.2와 같다(시험 고정).
- [x] drawer: 메뉴 버튼 `aria-expanded`·`aria-controls`, dialog 이름, Esc 닫힘과 포커스 복원, 링크 이동·`navigationKey` 변경 시 닫힘과 본문 포커스, 이전 경로로 돌아와도 다시 열리지 않음, lg 전환 시 닫힘, axe 위반 0.
- [x] 상단 바: "영역 - 페이지" `h1`, 설명 말줄임·`title`, 동작 슬롯. `AdminPageTitle`의 덮어쓰기와 복원.
- [x] Button 포커스가 UX-G9.1 outline 하나다(반투명 ring·outline-none·transition-all 없음, 시험·브라우저 smoke 단언). 소비자 전역 규칙 정리는 FS-7.8.
- [x] rail 접힘·저장·복원, compact 메뉴의 접근성 이름은 라벨.
- [x] 정규 pack을 설치한 Next webpack·Turbopack build와 320·390·1280px 브라우저 smoke가 CI에서 통과한다.
- [x] 독립 2인 리뷰 finding이 닫힌다(아래 Evidence).

## 검증 명령

```bash
npm run check:policy && npm run lint && npm run check && npm run doctor && npm run build
npm run check:examples --workspace packages/ui
npm test
```

## Evidence

- 로컬(WSL, Node 26.13.1/npm 12.0.1): `npm test` 전체 PASS(UI vitest 121·node 시험 235·tokens 90·toast 9·toolchain 3), lint·check·doctor(0 issue)·check:policy PASS.
- 브라우저 smoke·Next build: 로컬 디스크 여유 부족으로 NOT_RUN(로컬), CI `packages` job이 실행한다.
- 첫 CI(b04333c)에서 320·390px drawer smoke 2건이 `getByRole("button", { name: "메뉴 열기" })` not found로 실패했다. 모달 drawer가 열리면 Radix가 바깥 형제에 `aria-hidden`을 거는 정상 동작이라 트리거가 역할 트리에서 빠진 것이며 drawer 결함이 아니다. 225ddcd에서 닫힌 상태의 접근 가능한 이름은 역할 셀렉터로, 열린 뒤 `aria-expanded`·Escape 포커스 복귀는 `data-slot` 핸들로 확인하고, 열린 동안 바깥 버튼이 역할 트리에서 빠지는 것을 새로 단언했다. PR CI 9 job SUCCESS(Playwright 72 PASS)로 병합, merge R=0e2a3f5aa16323df0d009360802661c9bc496dc6, main push CI 3종 SUCCESS.
- main pack catalog: [admin-shell-ui-0.2.3-catalog](../evidence/releases/admin-shell-ui-0.2.3-catalog.md).

- 독립 2인 리뷰(34bd8f3 기준, React·접근성 / CSS·릴리스·문서): 둘 다 P0·P1 0, PASS. 반영: drawer 링크 닫힘 애니메이션 중 경로가 바뀌면 본문 포커스를 잃던 P2와 저장소 차단 시 접힘 버튼 무반응 P2를 고치고 회귀 시험 2개·smoke 본문 포커스 단언을 더했다. 소비자 이관 안내에 입력 요소 전역 규칙을 더하고, 셸 컨테이너의 `outline-none`을 `focus-visible:outline-0`으로 바꾸고, README에 모바일 actions·testId 중복·animation 전제를 적었다. 다른 공통 컴포넌트(Input·Select·Checkbox·Switch 등)의 UX-G9.1 정렬은 후속으로 남긴다(리뷰 P2, 범위 밖).

## Rollback

common은 이 task의 PR revert와 다음 patch로 되돌린다. 같은 버전 bytes를 재발행하지 않는다. 소비자는 채택 PR revert로 원복한다.
