# T-206 overlay 세트(Dialog(hasUnsavedInput·viewportProps)·AlertDialog·Popover·Tooltip·Tabs·Breadcrumb·HelpTip) + Table primitive + native Checkbox

- 상태: BLOCKED
- 우선순위: P1
- Gate: 단위 테스트
- 선행: T-205

## 목표

프리미티브 엔진에 종속된 2차 후보 가운데 overlay 7종을 `@base-ui/react`로 통일하고, Table primitive와 Checkbox는 엔진 무관(native)으로 만든다. pinvi가 map 이식 과정에서 추가한 확장(`hasUnsavedInput`·`viewportProps`·`containerTestId`·`stickyHeader`·`scope="col"`·`data-clickable`·`[data-slot=checkbox]` 셀렉터)을 공통 계약으로 흡수한다.

## 고정 결정

- ADR-007 — [ADR 색인](../adr/README.md). [브리프](../plan/design-brief.md) D-09: overlay(Dialog·AlertDialog·Popover·Tooltip·Tabs·Breadcrumb·HelpTip)만 `@base-ui/react`, Checkbox는 native `<input>` + `data-slot="checkbox"`, Dialog는 `hasUnsavedInput`·`viewportProps` 흡수, 토스트 엔진은 앱 소유. D-13: HelpTip은 popover-only 허용 하위집합(C17), 모달은 행동 계약(C18)·한 화면 두 모달 스택 금지.
- 규칙 정본: [ui-contract](../standards/ui-contract.md), [ux-guide](../standards/ux-guide.md) UX-G4.8(모달 a11y: 포커스 이동·trap·Escape·트리거 복원·scroll lock)·G4.6(확인 다이얼로그 동사 라벨·취소 초기 포커스)·G8.1(HelpTip hover 800ms/focus 0ms + click popover, 히트 ≥24px→40px 확장, 이름 `도움말: {label}`)·G2.6(행 체크박스 접근성 이름), [versions](../standards/versions.md)(`@base-ui/react` floor 1.6·recommended 1.8.0).
- 사실 근거: [ui-components](../survey/cross/ui-components.md) §3.2(Table 확장 4종 표), §3.4(Checkbox 세 구현·폼 직렬화 위험, Dialog pinvi 확장, AlertDialog `Close`+`Button` 조합, Tabs `Tab/Panel`, HelpTip 4앱 Popover 트리거 일치), §5.1·§5.4(base-ui 소비 29파일 vs radix 12; 비-overlay native 절충), §2.1(Breadcrumb map `useRender`); T-201 evidence의 base-ui Checkbox hidden input 확인 결과(native 선택의 근거).
- 이 task에서 확정하는 선택: `@base-ui/react`는 peerDependency `^1.6.0`(versions.json floor; map 1.6.0이 T-413 전에도 설치 가능) + CI 매트릭스 1.6.0·1.8.0. 1.6에서 API 차이가 드러나면 floor 상향을 T-005 `versions.json` 갱신으로 요청한다. 선택 열 셀렉터는 `[data-slot=checkbox]`(map의 `[role=checkbox]` 대신, pinvi 방식).

## 구현 범위

- `src/dialog.tsx`(Root/Trigger/Close/Popup/Backdrop/Viewport 재수출 + `hasUnsavedInput`이면 Escape·바깥 클릭 차단, `viewportProps`로 testid 전달), `src/alert-dialog.tsx`(`Close` + `Button`; 취소 초기 포커스), `src/popover.tsx`, `src/tooltip.tsx`, `src/tabs.tsx` + `tabs-variants.ts`(`Tab/Panel`), `src/breadcrumb.tsx`(`useRender`로 `Link` 합성, `aria-current="page"`), `src/help-tip.tsx`(Tooltip + Popover 조합, 40px 히트 확장, `label` 필수).
- `src/table.tsx`: `Table`(컨테이너 `data-slot="table-container"` + `containerClassName`/`containerStyle`/`containerTestId`), `TableHeader`(`sticky` prop), `TableBody`, `TableRow`(`data-clickable`에만 hover), `TableHead`(`scope="col"` 기본), `TableCell`, `TableCaption`; Card 내부 flush 규칙(`group-data-[slot=card]/card`)과 선택 열 패딩 셀렉터 `[data-slot=checkbox]`.
- `src/checkbox.tsx`: native `<input type="checkbox">` + `data-slot="checkbox"`, `onCheckedChange(checked: boolean)`, `indeterminate`(ref로 설정 + `data-indeterminate`), 20px 히트.
- `package.json`: peer `@base-ui/react ^1.6.0` 추가, `exports` 9 subpath.
- 테스트: Dialog 포커스 trap·복원·Escape·`hasUnsavedInput` 차단·`viewportProps` testid; AlertDialog 취소 초기 포커스; Tooltip 지연; Tabs 키보드(←→); Breadcrumb `aria-current`; HelpTip 접근성 이름·popover 열림; Checkbox `FormData` 포함·`indeterminate`·콜백 시그니처; Table `scope`·`containerTestId`·sticky 클래스; CI 매트릭스 두 버전 모두 통과.

## 범위 밖

- DataTable(T-208), Toast(앱 소유; base-ui Toast 채택 여부는 T-508), `ConfirmDialog` API, concierge `Select`·`Switch`, geo radix→base-ui 이관(T-444)과 `asChild` 변환, pinvi 사용자 표면 `ui/Dialog`(D-29), `data-pv-surface` 스코프 속성(앱이 `base.scoped.css`로 처리).

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다.

```text
packages/ui/src/{dialog,alert-dialog,popover,tooltip,tabs,breadcrumb,help-tip,table,checkbox}.tsx
packages/ui/src/tabs-variants.ts
packages/ui/src/*.test.tsx  (9 파일)
packages/ui/package.json  (peer @base-ui/react, exports 9)
.github/workflows/packages.yml  (base-ui 1.6.0/1.8.0 매트릭스)
packages/ui/smoke/next-app/app/overlay/page.tsx
PROVENANCE.md
```

## 수용 기준

- Dialog: 열릴 때 Popup 내부로 포커스 이동, Tab이 밖으로 나가지 않음, Escape 닫힘, 닫히면 트리거로 복원; `hasUnsavedInput`이면 Escape·바깥 클릭에 닫히지 않음; `viewportProps={{ "data-testid": "x" }}`가 DOM에 반영.
- Checkbox: `<form>` 제출 시 `FormData`에 name/value 포함, `indeterminate` 시 `data-indeterminate` 존재, `onCheckedChange`가 boolean만 받음.
- Table: `TableHead` 기본 `scope="col"`, 컨테이너 `data-testid` 전달, `sticky` 시 헤더에 sticky 클래스, `TableRow`는 `data-clickable` 없으면 hover 클래스 없음.
- HelpTip: 접근성 이름이 `도움말: {label}`, 트리거 히트 영역 클래스가 40px 확장, hover 800ms/focus 0ms 지연 값이 상수로 노출.
- base-ui 1.6.0과 1.8.0 두 매트릭스에서 vitest 실패 0·skip 0, axe 위반 0, `check-directives.mjs` 불일치 0(overlay 파일 전부 `'use client'`).
- `check-kt-classes.mjs` 위반 0; 애니메이션은 base-ui `data-[starting-style]`/`data-[ending-style]`만 사용(radix `data-[state]` 0건).

## 검증 명령

```bash
npm run test -w packages/ui -- dialog alert-dialog popover tooltip tabs breadcrumb help-tip table checkbox
npm install --no-save @base-ui/react@1.6.0 -w packages/ui && npm run test -w packages/ui
npm run build -w packages/ui && node packages/ui/scripts/check-directives.mjs && node packages/ui/scripts/check-kt-classes.mjs
npx tsc --noEmit -p packages/ui
```

## evidence

PR 본문·`docs/journal.md`에 두 base-ui 버전별 테스트 수·exit code, axe 결과, 원천(map·pinvi 확장은 재구현) 대비 변경 요약을 남긴다. 1.6.0 매트릭스를 못 돌렸으면 `NOT_RUN(사유)`.

## rollback 또는 release 차단 조건

- 컴포넌트 단위 revert. peer 추가는 `package.json` 한 줄이라 함께 되돌린다.
- 차단: 두 base-ui 버전 중 하나 실패, 포커스 복원 실패, Checkbox가 `FormData`에서 빠짐, `data-[state]` 애니메이션 잔존. 하나라도 있으면 T-213 rc를 만들지 않는다.
