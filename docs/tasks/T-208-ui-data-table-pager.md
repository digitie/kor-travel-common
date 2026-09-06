# T-208 DataTable(manualSorting 기본 true·removal·testid·sr-only·4상태) + OffsetPager/CursorPager

- 상태: BLOCKED
- 우선순위: P1
- Gate: 단위 테스트·2인 리뷰
- 선행: T-206

## 목표

map `data-table.tsx`(799행 + 테스트 175행)와 pinvi 이식본(853행)의 계약을 하나로 합쳐 헤드리스 `DataTable`을 만들고, map/pinvi에만 있는 `OffsetPager`/`CursorPager`를 함께 옮긴다. map 호출부는 무변경, pinvi는 `AdminTable` 어댑터(pinvi 소유)가 `manualSorting={false}`를 명시하는 것으로 두 정렬 모드를 수용한다.

## 고정 결정

- ADR-007 — [ADR 색인](../adr/README.md). [브리프](../plan/design-brief.md) D-09 DataTable: TanStack v8, **`manualSorting` 기본 `true` 유지**, `enableSortingRemoval`·`initialSorting`·`rowTestId`·`containerTestId`·`stickyHeader`·sr-only 로딩 문구·`rowSelectionLabel`·4상태(loading/empty/error/data) 계약 포함; 검색 툴바·`rowHeader`는 미포함(geo `VirtualTable` 잔류). D-31: 정렬 모드·prop 기본값은 파괴 항목.
- 규칙 정본: [ui-contract](../standards/ui-contract.md), [ux-guide](../standards/ux-guide.md) UX-G2.2(표 4상태 내부 렌더)·G2.3(서버 페이징 목록 = 서버 정렬)·G2.4(pager 라벨 `첫 페이지/이전/다음/마지막 페이지`, `페이지 n / m · 총 N건`, 경계 native disabled, 전환 중 `loading`)·G2.6(행 체크박스 이름 `"{row label} 선택"`, bulk 바)·G5.6(`—`, 가짜 0 금지), [versions](../standards/versions.md)(react-table floor 8.21, react-virtual 3.14; 9.x breaking 미조사).
- 사실 근거: [ui-components](../survey/cross/ui-components.md) §3.3(절 단위 비교표·회귀 위험 표: pinvi testid 계약, `aria-selected` on `role=table` 무효, `enableSortingRemoval` 없으면 desc에 갇힘, `noUncheckedIndexedAccess` 타입 오류), §2.2(pagination-bar 290/298행 유사); [ux-patterns](../survey/cross/ux-patterns.md) C10; [map 인벤토리](../survey/inventory/kor-travel-map.md) §8-8, §3.1(`"use no memo"` 정확히 2곳을 ESLint 검증 스크립트가 단언).
- 이 task에서 확정하는 선택: `@tanstack/react-table ^8.21.0`·`@tanstack/react-virtual ^3.14.0`은 optional peerDependency(subpath `./data-table`를 쓰는 앱만 설치). 행 선택 상태는 `data-state="selected"`(pinvi 발견대로 `aria-selected` 미부착). pinvi e2e가 잠근 `admin-table-*` testid는 공통 기본값이 아니라 `AdminTable` 어댑터가 `containerTestId`·`rowTestId`·`sortTestId`(후보 prop)로 공급한다.

## 구현 범위

- `src/data-table.tsx`(`'use client'` + `'use no memo'` 선두): 컬럼 `ColumnDef` + `meta{align,wrap,className,headerClassName,cellClassName,headerStyle}`; 정렬(`manualSorting` 기본 true, `sorting`/`onSortingChange` 제어형 또는 내부 상태, `initialSorting`, `enableSortingRemoval`, `enableMultiSort: false`); 선택(`enableRowSelection`, `rowSelection`/`onRowSelectionChange`, `rowSelectionLabel`, `renderBulkActions` `role=region`); 가상화 opt-in(`virtualized`, `estimateRowSize` 40, `overscan` 12, ARIA role 명시, `aria-rowcount`); 4상태(`isLoading` → Skeleton 행 + `aria-busy` + sr-only "불러오는 중…", `emptyState`/`emptyMessage` → EmptyState, `isError`/`error`/`onRetry` → Alert + 재시도 Button(Promise면 loading), data); 행 상호작용(`onRowClick` Enter/Space, `isRowActive`, `rowIdentity`); testid(`containerTestId`, `rowTestId(row)`, `sortTestId(columnId)`); `stickyHeader`; `ariaLabel`(caption) + 정렬 헤더 버튼 `aria-sort`.
- `src/pagination-bar.tsx`: `OffsetPager`·`CursorPager`, `formatCount`, `NULL_GLYPH`(`—`), 라벨·aria 규약 G2.4.
- 테스트: map `data-table.test.tsx` 175행 이관(Origin 헤더) + 추가 케이스(`manualSorting` 기본값 true·false 양쪽, `enableSortingRemoval` 3상태, testid 3종, sr-only 문구, 4상태 전환, 가상화 role, `noUncheckedIndexedAccess` 하 타입 통과) + Pager 라벨·경계 disabled·loading 포커스 유지.
- `package.json`: optional peer 2종, `exports` `./data-table`·`./pagination-bar`.

## 범위 밖

- 검색 툴바·`getSearchText`·`rowHeader`·기본 가상화 `as="grid"`(geo `VirtualTable` 잔류; 흡수 재평가는 T-508), pinvi `mobileCard`·`virtualizeThreshold`·`maxHeight`(pinvi `AdminTable` 어댑터 소유), 페이지별 `serverSort` 전환 목록(pinvi T-422), react-table 9 검토(T-507).

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다.

```text
packages/ui/src/data-table.tsx  packages/ui/src/data-table.test.tsx
packages/ui/src/pagination-bar.tsx  packages/ui/src/pagination-bar.test.tsx
packages/ui/package.json  (optional peer 2종, exports 2)
packages/ui/smoke/next-app/app/table/page.tsx
docs/reviews/adversarial/YYYY-MM-DD-ui-data-table.md  + evidence/…-reviewer-{a,b}.md
PROVENANCE.md
```

## 수용 기준

- props를 주지 않은 `DataTable`은 `manualSorting === true`로 동작하고(정렬 클릭 시 `onSortingChange`만 호출, 행 순서 불변), `manualSorting={false}`이면 클라이언트 정렬된다.
- `enableSortingRemoval={false}`에서 헤더 클릭이 asc↔desc만 순환하고, 기본값에서는 세 번째 클릭에 정렬이 해제된다.
- `containerTestId`·`rowTestId`·`sortTestId`가 DOM에 반영되고, 로딩 상태에 sr-only "불러오는 중…"과 `aria-busy="true"`가 있다.
- 4상태가 상호 배타적으로 렌더되며 error 상태의 재시도 버튼은 `onRetry`가 Promise면 `loading`을 건다.
- 가상화 경로에서 `role=table/rowgroup/row/columnheader/cell`과 `aria-rowcount`가 명시된다.
- 행에 `aria-selected`가 없고 `data-state="selected"`가 있다.
- Pager: 라벨 4종과 요약 문구가 규약 문자열과 일치, 경계 버튼은 native `disabled`, 전환 중 버튼은 포커스를 유지한다.
- `noUncheckedIndexedAccess: true`에서 타입 오류 0, vitest 실패 0·skip 0, axe 위반 0, 2인 리뷰 verdict `PASS`(P0/P1 0).

## 검증 명령

```bash
npm run test -w packages/ui -- data-table pagination-bar
npx tsc --noEmit -p packages/ui
npm run build -w packages/ui && node packages/ui/scripts/check-directives.mjs && node packages/ui/scripts/check-kt-classes.mjs
rg -n "use no memo" packages/ui/dist | sort
```

## evidence

PR 본문·`docs/journal.md`에 테스트 수·exit code, 리뷰 report 경로, map 원본 대비 계약 diff 표(prop 추가/변경/제거), TanStack 설치 버전을 남긴다.

## rollback 또는 release 차단 조건

- DataTable·Pager 단위 revert. 소비자 영향은 T-213 이후.
- 차단: `manualSorting` 기본값 변경, testid·sr-only 문구가 ui-contract와 불일치, 리뷰 P0/P1 미해결, map 이관 테스트 175행 중 실패. 하나라도 있으면 T-213 rc를 만들지 않는다.
