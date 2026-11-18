# T-222 관리자 셸(모바일 좌측 drawer·한 줄 상단 제목 바)과 ui 0.2.3

- 상태: IN_PROGRESS
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
- [ ] 정규 pack을 설치한 Next webpack·Turbopack build와 320·390·1280px 브라우저 smoke가 CI에서 통과한다.
- [ ] 독립 2인 리뷰 finding이 닫힌다.

## 검증 명령

```bash
npm run check:policy && npm run lint && npm run check && npm run doctor && npm run build
npm run check:examples --workspace packages/ui
npm test
```

## Evidence

- 로컬(WSL, Node 26.13.1/npm 12.0.1): `npm test` 전체 PASS(UI vitest 119·node 시험 235·tokens 90·toast 9·toolchain 3), lint·check·doctor(0 issue)·check:policy PASS.
- 브라우저 smoke·Next build: 로컬 디스크 여유 부족으로 NOT_RUN(로컬), CI `packages` job이 실행한다.

## Rollback

common은 이 task의 PR revert와 다음 patch로 되돌린다. 같은 버전 bytes를 재발행하지 않는다. 소비자는 채택 PR revert로 원복한다.
