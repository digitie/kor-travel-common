# ADR-007: React UI 패키지 배포 방식(npm 1차·React 19 전용·overlay base-ui/비-overlay native·마크업 계약·레지스트리 2차)

- 상태: accepted — O-3(배포 방식) 기본값으로 진행; base-ui 미확인 3건은 T-201 확인 전 릴리스 금지
- 날짜: 2026-09-06
- 근거 문서: `docs/plan/design-brief.md` D-09·D-10·O-3·O-22, `docs/survey/cross/ui-components.md` §3.1~§3.4·§4·§5·§6·§7, `docs/survey/cross/ux-patterns.md` §4 C7~C10·C18, `docs/survey/commonality-matrix.md` §2.2, 선행 보고서 §3.2·§7.3

## 컨텍스트

프리미티브 엔진은 base-ui 29파일(map·concierge·pinvi admin·airport WIP) 대 radix 12파일(geo)이며, pinvi admin은 overlay 4종만 base-ui이고 나머지는 native로 재작성했다(`ui` §5.1). Button은 세 계열(map `render`+`loading` / pinvi native `forwardRef` / airport shadcn 기본 레시피)로 갈렸고 pinvi 사용자 Button은 `loading` 포커스 처리가 반대다(`ui` §3.1). DataTable은 두 `data-table.tsx`가 `manualSorting=true`이지만 pinvi 35~36쪽이 쓰는 `AdminTable` 어댑터는 `false` 고정이다(`ui` §3.3). 등록 방식은 현재 소스 복사이고 27/27 쌍이 드리프트했다(`ui` §6.1). 선행 보고서 §3.2는 geo의 반복 동기화 비용을 기록했다. React 18 앱(geo·ktdm)이 둘 있다.

## 결정

1. 1차 배포는 npm 패키지(ESM + d.ts + Tailwind 소스 클래스 + `'use client'`·`'use no memo'` 지시문 보존)다. 패키지 내부 클래스는 `kt-` 접두 유틸리티만 쓴다(ADR-006). `@kor-travel/ui/cn` = clsx + `extendTailwindMerge`(kt 그룹). `noUncheckedIndexedAccess: true`.
2. `@kor-travel/ui`는 React 19 전용(peer `^19.0.0`, ref prop, forwardRef 없음). React 18 앱은 tokens부터 채택한다.
3. overlay(Dialog·AlertDialog·Popover·Tooltip·Tabs·Breadcrumb·HelpTip)만 `@base-ui/react`(floor 1.6, 권장 1.8); 비-overlay(Button·Checkbox·Input·Textarea·NativeSelect·Separator·Badge)는 native 요소 + `useRender`로 `render` 합성 선택 지원. Checkbox는 native `<input>` + `data-slot="checkbox"`.
4. Button 계약: `type="button"` 명시 기본, `loading`=`aria-disabled`+`aria-busy`+spinner+포커스 유지+`onClick` 차단(native disabled 안 걺), `disabled`=native + `disabledReason`→`title`, root opacity 금지(라벨 자식 래퍼 흐림), variant 7종, size 8종(xs·lg·icon-xs·icon-lg는 deprecated alias).
5. DataTable: TanStack v8, `manualSorting` 기본 `true` 유지(map 호출부 무변경; pinvi `AdminTable` 어댑터가 `false` 명시) + `enableSortingRemoval`·`initialSorting`·`rowTestId`·`containerTestId`·`stickyHeader`·sr-only 로딩 문구·`rowSelectionLabel`·4상태 계약. 검색 툴바·`rowHeader`는 미포함(geo `VirtualTable` 잔류). Dialog는 `hasUnsavedInput`·`viewportProps` 흡수. dirty 이탈 경고는 미포함(O-22).
6. 마크업 계약(data-slot·testid·heading 구조·sr-only 문구·geo e2e 셀렉터 대응)은 `docs/standards/ui-contract.md`가 정본이며 변경은 0.x minor(이관 절 필수)/1.x major다.
7. 토스트 엔진과 모달 엔진은 앱 소유(정책 UX-G4.1·행동 계약만). 셸 nav·로그아웃·접힘·RBAC는 앱 소유이고 AdminPageHeader/SkipLink/RailGrid 골격만 공통.
8. shadcn 레지스트리 채널은 앱이 소유해야 하는 템플릿(셸 골격·로그인 페이지·playwright 기준선)에만 쓴다(T-211). 전면 레지스트리는 Phase 5에서 "npm 소비자 우회 패치 2회 이상"일 때만 재검토한다.
9. common CI `consumer-smoke`는 webpack·Turbopack 양쪽 `next build`를 검증한다. 테스트 하네스는 vitest + RTL + jsdom, axe opt-in, showcase 없음.
10. base-ui 미확인 3건(Button `type` 기본, Checkbox hidden input, Toast API)은 T-201에서 소스 확인 전 릴리스 금지.

## 대안 검토

- **A. 자체 shadcn 레지스트리 1차**: 3앱이 `base-nova` components.json을 갖고 있어 CLI 흐름과 맞지만 복사 후 드리프트가 그대로 남고(현재 27/27 상이가 증거), 토큰명이 달라 pinvi·airport에서 깨진다. 템플릿 채널로만 축소했다.
- **C. 소스 복사 유지 + 정본 지정(현행)**: 즉시 가능하지만 검증 자동화가 없고 드리프트가 상시다.
- **React 18/19 동시 peer**: forwardRef 이중 구현·검증 매트릭스 비용이 크고 React 18 앱은 둘뿐이며 각각 업그레이드 task(T-443·T-470)가 있다.
- **전 프리미티브 base-ui**: pinvi admin이 이미 native로 재작성했고 native는 엔진 무관·번들 작음. overlay만 엔진이 필요하다.
- **DataTable `manualSorting` 기본 `false`**: pinvi 어댑터와 맞지만 map 호출부 전수 수정이 필요하다(migration 판정).

## 결과

- 버전 갱신으로 전파되어 반복 동기화 비용이 줄고, `ui_drift.py`가 우회 패치를 탐지한다.
- geo는 radix→base-ui 이관(12파일·`asChild` 17곳)과 React 19가 선행이라 ui 채택이 가장 늦다.
- 앱별 확장(pinvi testid·sticky·`hasUnsavedInput`)을 prop으로 흡수해야 하므로 계약 합의 비용이 2차(v0.2.0)에 몰린다.
- 셀렉터 계약 변경은 소비자 e2e를 깨므로 minor마다 이관 절과 소비자 PR 검증이 필수다.

## 후속·적용 위치

- 현재 설계: `docs/architecture/packages.md` §3, `docs/architecture/style-delivery.md` §5
- 규칙: `docs/standards/ui-contract.md`(T-204 확정), `docs/standards/ux-guide.md`
- 실물: T-201(골격·base-ui 확인), T-203(소형 13종), T-205~T-210(v0.2), T-211(레지스트리 채널·`ui_drift`), T-212·T-213(릴리스)
- 재평가: T-508(전면 레지스트리·ConfirmDialog·토스트·VirtualTable)
