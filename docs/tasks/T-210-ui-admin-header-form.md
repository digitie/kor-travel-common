# T-210 AdminPageHeader·AdminSkipLink·AdminRailGrid + FormFieldInput/FormSelect/FormTextArea + form-validation(헤드리스)

- 상태: BLOCKED
- 우선순위: P2
- Gate: 단위 테스트
- 선행: T-206

## 목표

셸에서 앱 소유 부분(nav·로그아웃·접힘·RBAC)을 뺀 골격 3종과, react-hook-form/zod 앱과 공존 가능한 헤드리스 폼 부품 3종 + 검증 유틸을 공통화한다. pinvi가 map `AdminShell`(510행)에서 이식 가능한 부분만 분리한 `admin-shell-parts.tsx`(224행)가 범위의 기준이다.

## 고정 결정

- ADR-007·[ADR-015](../adr/015-common-shared-systems-scope.md) — [ADR 색인](../adr/README.md). [브리프](../plan/design-brief.md) D-13: 접힌 rail 4rem(pinvi 5rem 예외), 셸 전환 1024, inspector rail 22rem은 `xl` 이상 2열, pathname 노출 대신 breadcrumb, nav 접근성 이름은 라벨만, pinvi `AdminPage` → `AdminPageHeader` 수렴(C16). D-20: airport 셸·로그인 소비는 T-035 라우트 분리 후(O-9). 로그인 위젯은 common 계약을 사용하고 endpoint·IdP·RBAC 구성은 앱이 소유한다.
- 규칙 정본: [ui-contract](../standards/ui-contract.md)(heading 구조), [ux-guide](../standards/ux-guide.md) UX-G1.3(skip link → `<main id tabIndex={-1} focus-visible:outline-0>`)·G1.5(헤더 밴드 순서: breadcrumb/section → h1(+help) + actions(primary ≤1·secondary ≤2) → meta → description, hairline)·G1.8(우측 rail 22rem)·G3.3(라벨 위·컨트롤·메시지 슬롯 1개, `aria-describedby`는 표시 중 메시지만, required 별표는 접근성 이름 제외)·G3.4(제출 실패 시 첫 오류 필드 포커스)·G9.5, [responsive-web](../standards/responsive-web.md)(breakpoint xl 1280·검사 폭 6종).
- 사실 근거: [ui-components](../survey/cross/ui-components.md) §2.2(admin-shell 행: pinvi 부분 이식, geo `PageHeader`·weather `PageHeader`·ktdm `AppShell` props 동형; form-field-* map/pinvi 유사; `form-validation.ts`), §4.2, §4.3(nav·로그아웃·RBAC 보류), §7-12(`Section` vs `SectionCard` 이름 충돌); [map 인벤토리](../survey/inventory/kor-travel-map.md) §8-9·§8-11(rhf/zod 부재 → 헤드리스 요구); [pinvi 인벤토리](../survey/inventory/pinvi.md) §8-2.
- 이 task에서 확정하는 선택: `AdminPageHeader` props = `title`/`description`/`section`/`breadcrumbs`/`help`/`meta`/`actions`(map 계약), actions 개수 제한은 타입으로(`primary?: ReactNode; secondary?: [ReactNode?, ReactNode?]`, 후보). `AdminRailGrid`는 `--kt-rail`(22rem)만 참조하고 접힌 rail 폭은 다루지 않는다(셸 nav는 앱).

## 구현 범위

- `src/admin-page-header.tsx`(Breadcrumb·HelpTip 의존, h1 유일), `src/admin-skip-link.tsx`(대상 `#main` 계약 문서화), `src/admin-rail-grid.tsx`(`xl:` 2열, `--kt-rail`).
- `src/form-field-input.tsx`·`form-select.tsx`·`form-textarea.tsx`(Field + Input/NativeSelect/Textarea + HelpTip 조합, 메시지 슬롯 1개, `aria-describedby` 동적), `src/form-field-shared.ts`.
- `src/form-validation.ts`: `validateForm(values, rules)`, `firstErrorField(errors)`, `focusFirstError(form, errors)` — 프레임워크 의존 0(RHF/zod 앱은 결과만 넘겨 포커스 유틸만 사용 가능).
- 테스트: 헤더 밴드 DOM 순서·h1 1개·breadcrumb `aria-current`; skip link 포커스 이동; rail grid 클래스; 폼 3종의 라벨·hint/error 슬롯 교체·`aria-describedby` 값·required 별표 `aria-hidden`; `firstErrorField` 순서·`focusFirstError` 호출.
- `exports` 7 subpath.

## 범위 밖

- `AdminShell` nav·로그아웃·접힘·RBAC·`NAV_GROUPS`(앱), 로그인 위젯 계약·앱 endpoint/IdP 어댑터(T-214·T-312), pinvi `AdminPage` 어댑터 교체(T-422), weather 셸 교체(T-463), RHF/zod 어댑터, dirty 이탈 경고(O-22 미포함).

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다.

```text
packages/ui/src/{admin-page-header,admin-skip-link,admin-rail-grid}.tsx
packages/ui/src/{form-field-input,form-select,form-textarea}.tsx  packages/ui/src/form-field-shared.ts
packages/ui/src/form-validation.ts
packages/ui/src/*.test.ts(x)  (7 파일)
packages/ui/package.json  (exports 7)
packages/ui/smoke/next-app/app/header/page.tsx
PROVENANCE.md
```

## 수용 기준

- AdminPageHeader가 G1.5 순서대로 DOM을 만들고 페이지에 h1이 정확히 1개이며 `secondary` actions 3개는 타입 오류다.
- AdminSkipLink 활성화 시 `#main`이 포커스를 받고(`tabIndex={-1}` 계약) 화면에 outline이 없다.
- AdminRailGrid가 `xl` 미만에서 1열, 이상에서 `--kt-rail` 폭의 2열 클래스를 갖는다(폭 6종 검사는 소비자 PR evidence, D-21).
- 폼 3종: error가 있으면 hint 대신 error가 같은 슬롯에 렌더되고 `aria-describedby`가 그 메시지 id만 가리킨다; required 별표가 접근성 이름에 들어가지 않는다.
- `focusFirstError`가 DOM 순서상 첫 오류 필드에 포커스를 준다.
- vitest 실패 0·skip 0, axe 위반 0, `check-kt-classes.mjs` 위반 0, `check-directives.mjs` 불일치 0.

## 검증 명령

```bash
npm run test -w packages/ui -- admin-page-header admin-skip-link admin-rail-grid form-field-input form-select form-textarea form-validation
npm run build -w packages/ui && node packages/ui/scripts/check-kt-classes.mjs && node packages/ui/scripts/check-directives.mjs
npx tsc --noEmit -p packages/ui
```

## evidence

PR 본문·`docs/journal.md`에 테스트 수·exit code, axe 결과, map `admin-shell.tsx`·pinvi `admin-shell-parts.tsx`(재구현) 대비 props diff를 남긴다.

## rollback 또는 release 차단 조건

- 컴포넌트 단위 revert.
- 차단: 헤더에 nav·앱별 인증 정책이 유입되거나, 공용 위젯이 운영 비밀·저장소를 직접 읽거나, 폼 부품이 RHF/zod를 import하거나 h1 중복을 허용하면 T-213 rc를 만들지 않는다.
