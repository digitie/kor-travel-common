// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
// Derived-From: digitie/kor-travel-map@32668d003ea6a259468e03970bd167359c19ecdb packages/kor-travel-map-admin/frontend/src/components/ui/data-table.tsx
// Modified: 2026-11-11 TanStack 9 API와 공통 소비자 계약
"use client";

// 공용 headless VirtualTable — @tanstack/react-table v9 기능 등록 기반. admin/ops UI의 모든
// 테이블이 본 컴포넌트로 통일된다(ADR/마이그레이션 2026-06-17). 기본은 semantic
// shadcn Table primitive로 렌더해 접근성(role=table/columnheader/row/cell)과 기존
// Playwright 셀렉터를 보존하고, 대용량/무한 목록만 `virtualized`로 @tanstack/react-virtual
// 윈도잉을 켠다(이때는 display:grid라 native table role이 죽으므로 role=table/rowgroup/row/
// columnheader/cell을 명시하고 aria-rowcount/aria-rowindex를 얹는다).
//
// 데이터 연산은 기본 server-side(manualSorting 기본 true): 페이지의 react-query가 이미
// cursor 페이징/필터/정렬을 수행하므로 DataTable은 data만 받아 렌더한다(서버 정렬이
// 일반적 케이스라 #502에서 기본을 manual로 뒤집었다). 전체 데이터셋을 한 번에 보유하는
// 완전 client 목록만 manualSorting={false}로 getSortedRowModel을 켠다.
//
// 상태 표면(design.md): loading = 형태가 맞는 skeleton 행(`aria-busy`), empty = 좌측 정렬
// EmptyState(제목 + 이유 + 행동 1개, `emptyState`), error = what/why/what-to-do Alert +
// `다시 시도`(`onRetry`). 숫자 column은 `meta.align: "right"`(tabular-nums는 Table 기본),
// 긴 본문 column은 `meta.wrap: true`로 clamp/wrap을 허용한다.

import * as React from "react";
import {
  type CellContext as CoreCellContext,
  type HeaderContext as CoreHeaderContext,
  type Cell as CoreCell,
  type Column as CoreColumn,
  type ColumnDef as CoreColumnDef,
  type Header as CoreHeader,
  type Table as CoreTable,
  type Row as CoreRow,
  type RowData,
  type OnChangeFn,
  type RowSelectionState,
  type SortingState,
  flexRender,
  useTable,
  tableFeatures,
  createSortedRowModel,
  sortFns,
  rowSortingFeature,
  rowSelectionFeature,
  columnSizingFeature,
  columnVisibilityFeature,
} from "@tanstack/react-table";
export type {
  RowData,
  OnChangeFn,
  RowSelectionState,
  SortingState,
  Updater,
  ColumnSort,
} from "@tanstack/react-table";
const features = tableFeatures({
  rowSortingFeature,
  rowSelectionFeature,
  columnSizingFeature,
  columnVisibilityFeature,
  sortedRowModel: createSortedRowModel(),
  sortFns,
  columnMeta: {} as DataTableColumnMeta,
});
export type ColumnDef<T extends RowData, V = unknown> = CoreColumnDef<
  typeof features,
  T,
  V
>;
export type Column<T extends RowData, V = unknown> = CoreColumn<
  typeof features,
  T,
  V
>;
export type Header<T extends RowData, V = unknown> = CoreHeader<
  typeof features,
  T,
  V
>;
export type Cell<T extends RowData, V = unknown> = CoreCell<
  typeof features,
  T,
  V
>;
export type CellContext<T extends RowData, V = unknown> = CoreCellContext<
  typeof features,
  T,
  V
>;
export type HeaderContext<T extends RowData, V = unknown> = CoreHeaderContext<
  typeof features,
  T,
  V
>;
export type Row<T extends RowData> = CoreRow<typeof features, T>;
export type Table<T extends RowData> = CoreTable<typeof features, T>;
type TanstackTable<T extends RowData> = Table<T>;
import { useVirtualizer } from "@tanstack/react-virtual";
import { ArrowDown, ArrowUp, ChevronsUpDown } from "lucide-react";

import {
  Empty,
  EmptyHeader,
  EmptyTitle,
  EmptyDescription,
  EmptyContent,
  EmptyMedia,
} from "./empty.js";
import { Alert, AlertDescription, AlertTitle } from "./alert.js";
import { Button } from "./button.js";
import { Checkbox } from "./checkbox.js";
import { Skeleton } from "./skeleton.js";
import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "./table.js";
import { cn } from "./utils.js";

/**
 * ColumnDef.meta에 넣는 표시 힌트. 예:
 *   { accessorKey: "duration_ms", header: "소요", meta: { align: "right" } satisfies DataTableColumnMeta }
 */
export interface DataTableColumnMeta {
  /** 정렬 — 숫자/시각/크기 column은 "right"(우측 정렬, M24). */
  rowHeader?: boolean;
  align?: "left" | "center" | "right";
  /** 긴 본문(message 등) — whitespace-normal로 wrap/line-clamp 허용(M38). */
  wrap?: boolean;
  /** th·td 공통 className. */
  className?: string;
  /** th 전용 className. */
  headerStyle?: React.CSSProperties;
  headerClassName?: string;
  /** td 전용 className. */
  cellClassName?: string;
}

/** 비었을 때 표시할 내용 — 무엇이 비었나 · 왜/다음 행동 · 행동 1개. */
export interface DataTableEmptyState {
  title: string;
  description?: React.ReactNode;
  action?: React.ReactNode;
  icon?: React.ReactNode;
}

export interface DataTableProps<TData extends RowData> {
  columns: ColumnDef<TData, unknown>[];
  data: TData[];
  /** row.id를 도메인 안정 id로 고정(권장) — 정렬/선택/가상화 키 안정성. */
  getRowId?: (row: TData, index: number) => string;
  /** react-query 상태를 그대로 넘기면 skeleton/alert/empty를 내부에서 렌더. */
  isLoading?: boolean;
  isError?: boolean;
  error?: { message?: string } | null;
  /** 오류 제목(what). 기본 `목록을 불러오지 못했습니다`. */
  errorTitle?: string;
  /** 오류 슬롯 전체를 대체(페이지가 AppErrorPanel 등을 직접 렌더할 때). */
  errorState?: React.ReactNode;
  /** 오류 시 `다시 시도` 버튼에 연결할 refetch. Promise를 돌려주면(예: `() => query.refetch()`)
   *  resolve될 때까지 버튼을 loading 상태로 잠근다 — 페이지가 진행 상태를 따로 넘기지 않는다. */
  onRetry?: () => void | Promise<unknown>;
  /** 비었을 때 colSpan 행에 표시할 문구(제목만). `emptyState`가 있으면 그것이 우선. */
  emptyMessage?: string;
  /** 비었을 때 표시할 EmptyState(제목 + 이유 + 행동 1개). */
  emptyState?: DataTableEmptyState;
  /** skeleton 행 수(기본 6). 예상 페이지 크기에 맞추면 layout shift가 줄어든다. */
  skeletonRowCount?: number;
  /** 정렬: 제어(서버) 모드면 sorting+onSortingChange 전달 + manualSorting. */
  initialSorting?: SortingState;
  enableSortingRemoval?: boolean;
  sorting?: SortingState;
  onSortingChange?: OnChangeFn<SortingState>;
  /** true면 getSortedRowModel을 켜지 않음(서버 정렬). 기본 true(서버 정렬).
   *  완전 client 목록(전체 데이터셋을 한 번에 보유)만 manualSorting={false}로
   *  getSortedRowModel을 켠다. cursor/page_size 목록은 서버가 정렬을 소유하므로
   *  기본값(true)을 그대로 두고, 서버가 정렬하지 않는 accessor는 enableSorting:false로. */
  manualSorting?: boolean;
  /** 행 선택(opt-in) — 체크박스 컬럼 + 선택 상태. 함수를 주면 행별 선택 가능 여부
   *  (react-table getCanSelect) — 선택 불가 행은 체크박스 disabled + select-all/bulk 대상 제외.
   *  predicate 변경은 제어 상태를 자동 수정하지 않는다. 소비자가 raw rowSelection을
   *  별도 작업에 쓸 때도 권한/predicate를 검증해야 한다. 현재 페이지 밖 id는 보존한다.
   *  헤더 선택은 현재 페이지의 선택 가능 행에 적용하고, 헤더 전체 해제는 stale/페이지 밖
   *  id까지 포함해 빈 상태를 onRowSelectionChange로 전달한다. */
  enableRowSelection?: boolean | ((row: Row<TData>) => boolean);
  rowSelection?: RowSelectionState;
  onRowSelectionChange?: OnChangeFn<RowSelectionState>;
  /** 행 체크박스의 이름 조각 — `${rowSelectionLabel(row)} 선택`으로 접근성 이름을 만든다.
   *  주지 않으면 모든 행이 같은 이름(`행 선택`)이라 스크린리더/셀렉터가 행을 구분하지 못한다.
   *  행을 식별하는 짧은 값(이름·id)을 주고, column 재생성을 막기 위해 module-level 함수나
   *  useCallback으로 안정화한다. */
  rowSelectionLabel?: (row: TData) => string;
  /** 선택된 행이 있을 때 테이블 위에 표시할 bulk action 바. */
  renderBulkActions?: (rows: Row<TData>[]) => React.ReactNode;
  /** 행 클릭(detail pane 선택 등). 내부 link/button은 stopPropagation 해야 함. */
  onRowClick?: (row: TData) => void;
  /** 행 active(detail pane 강조) — data-state="selected". */
  isRowActive?: (row: TData) => boolean;
  /** 행별 data-testid(e2e 셀렉터 등). 값을 주면 비가상 경로의 <tr data-testid>로 렌더. */
  rowTestId?: (row: TData) => string | undefined;
  /** cursor 순서 검증용 불투명 행 identity. 비가상 경로의 <tr data-row-identity>로 렌더. */
  rowIdentity?: (row: TData) => string | undefined;
  /** 가상화(대용량/무한 목록만). 켜면 display:grid 레이아웃 + 명시 role=table 계열 ARIA. */
  virtualized?: boolean;
  estimateRowSize?: number;
  overscan?: number;
  /** 스크롤 컨테이너 className — Table 자신의 컨테이너(hairline 1층)에 합쳐진다: 높이 제한
   *  (`max-h-80`)·스크롤 축만 준다(테두리/배경/모서리를 다시 주지 않는다). 가상화 시 고정 높이 필수
   *  (예: h-[calc(100vh-16rem)]). */
  containerClassName?: string;
  /** 테이블 caption(스크린리더용). */
  ariaLabel?: string;
  caption?: React.ReactNode;
  hideHeader?: boolean;
  wrapCells?: boolean;
  height?: React.CSSProperties["height"];
  stickyHeader?: boolean;
  containerStyle?: React.CSSProperties;
  containerTestId?: string;
  containerRole?: React.AriaRole;
  containerAriaLabel?: string;
  containerTabIndex?: number;
  tableTestId?: string;
  tableSlot?: string;
  sortButtonTestIdPrefix?: string;
  rowProps?: (row: TData) => React.ComponentProps<"tr">;
  renderCell?: (row: TData, columnId: string) => React.ReactNode;
  renderRowDetails?: (row: TData) => React.ReactNode;
}

function columnMeta<TData extends RowData>(
  column: Column<TData, unknown>,
): DataTableColumnMeta {
  return (column.columnDef.meta ?? {}) as DataTableColumnMeta;
}

/**
 * 긴 본문 셀(로그 message·이벤트 payload 요약)의 표준 — column에 `meta: { wrap: true }`를 주고
 * cell을 이 컴포넌트로 감싸면 N줄로 clamp되고 말줄임이 보인다(M38). 잘린 전문은 hover title이
 * 아니라 행 상세(onRowClick → inspector rail)로 도달하게 한다 — title은 보조 신호일 뿐이다.
 */
export function VirtualTableClampCell({
  lines = 2,
  className,
  title,
  children,
}: {
  /** clamp 줄 수(1–3). */
  lines?: 1 | 2 | 3;
  className?: string;
  /** 전문(문자열이면 title로도 노출). */
  title?: string;
  children: React.ReactNode;
}) {
  return (
    <div
      className={cn(
        "max-w-96 whitespace-normal break-words",
        lines === 1 && "line-clamp-1",
        lines === 2 && "line-clamp-2",
        lines === 3 && "line-clamp-3",
        className,
      )}
      title={title ?? (typeof children === "string" ? children : undefined)}
    >
      {children}
    </div>
  );
}

function alignClass(align: DataTableColumnMeta["align"]): string | undefined {
  if (align === "right") return "text-right";
  if (align === "center") return "text-center";
  return undefined;
}

function flexAlignClass(
  align: DataTableColumnMeta["align"],
): string | undefined {
  if (align === "right") return "justify-end text-right";
  if (align === "center") return "justify-center text-center";
  return undefined;
}

/** 정렬 가능한 헤더 버튼 — 접근성 이름은 title 그대로 보존(글리프 aria-hidden), th에 aria-sort.
 *  th와 같은 12px/600 활자(정렬 버튼이 헤더 텍스트보다 커 보이지 않게, M3). */
function DataTableColumnHeader({
  title,
  sorted,
  canSort,
  align,
  onToggle,
  testId,
}: {
  title: string;
  testId?: string;
  sorted: false | "asc" | "desc";
  canSort: boolean;
  align?: DataTableColumnMeta["align"];
  onToggle?: (event: React.MouseEvent) => void;
}) {
  if (!canSort) return <>{title}</>;
  const Glyph =
    sorted === "asc" ? ArrowUp : sorted === "desc" ? ArrowDown : ChevronsUpDown;
  return (
    <button
      type="button"
      data-sorted={sorted || undefined}
      data-testid={testId}
      className={cn(
        "inline-flex h-7 items-center gap-1 rounded-kt-control px-2 text-kt-2xs leading-none font-semibold whitespace-nowrap text-kt-text-secondary transition-[color,background-color,border-color] select-none hover:bg-kt-surface-muted hover:text-kt-text-primary focus-visible:outline-2 focus-visible:-outline-offset-2 focus-visible:outline-kt-focus active:translate-y-px data-[sorted]:text-kt-text-primary",
        align === "right" ? "-mr-2 flex-row-reverse" : "-ml-2",
      )}
      onClick={onToggle}
    >
      {title}
      <Glyph
        className={cn(
          "size-3.5 shrink-0",
          sorted ? "text-kt-brand" : "text-kt-text-tertiary",
        )}
        aria-hidden="true"
      />
    </button>
  );
}

function ariaSort(
  sorted: false | "asc" | "desc",
): "ascending" | "descending" | "none" {
  if (sorted === "asc") return "ascending";
  if (sorted === "desc") return "descending";
  return "none";
}

function renderHeadCellContent<TData extends RowData>(
  header: Header<TData, unknown>,
  sorted: false | "asc" | "desc",
  canSort: boolean,
  sortButtonTestIdPrefix?: string,
) {
  if (header.isPlaceholder) return null;
  if (typeof header.column.columnDef.header === "string") {
    return (
      <DataTableColumnHeader
        title={header.column.columnDef.header}
        testId={
          sortButtonTestIdPrefix
            ? sortButtonTestIdPrefix + header.column.id
            : undefined
        }
        sorted={sorted}
        canSort={canSort}
        align={columnMeta(header.column).align}
        onToggle={header.column.getToggleSortingHandler()}
      />
    );
  }
  return flexRender(header.column.columnDef.header, header.getContext());
}

function handleClickableRowKeyDown<TData extends RowData>(
  event: React.KeyboardEvent<HTMLTableRowElement>,
  row: TData,
  onRowClick: (row: TData) => void,
) {
  if (event.target !== event.currentTarget) return;
  if (event.key !== "Enter" && event.key !== " ") return;
  event.preventDefault();
  onRowClick(row);
}

/** 클릭 가능한 행의 focus 표면 — 표 안이라 inset outline(이웃 행/스크롤 컨테이너에 잘리지 않게)
 *  + 배경 변화(색 1채널이 아니게). 링은 즉시 나타나야 하므로(design.md §Focus) 행의 전환은
 *  `transition-colors`가 아니라 `transition-[color,background-color,border-color]`로 열거한다 —
 *  tailwind v4의 `transition-colors`는 `outline-color`를 포함해서 링 색이 100ms 페이드인 된다. */
const CLICKABLE_ROW_CLASS =
  "cursor-pointer focus-visible:bg-kt-surface-subtle focus-visible:outline-2 focus-visible:-outline-offset-2 focus-visible:outline-kt-focus active:bg-kt-surface-muted";

function pageSelectionState<T extends RowData>(
  table: TanstackTable<T>,
): boolean | "indeterminate" {
  const eligible = table.getRowModel().rows.filter((row) => row.getCanSelect());
  const selected = eligible.filter((row) => row.getIsSelected()).length;
  if (selected === 0) return false;
  return selected === eligible.length ? true : "indeterminate";
}

/** 선택 열. 행 체크박스 이름은 `rowSelectionLabel`이 있으면 행마다 다르게(`홍길동 선택`),
 *  없으면 기존 계약대로 `행 선택`으로 남는다(호출부 호환). */
function selectionColumn<TData extends RowData>(
  rowSelectionLabel?: (row: TData) => string,
): ColumnDef<TData, unknown> {
  return {
    id: "__select__",
    enableSorting: false,
    size: 36,
    header: ({ table }) => (
      <Checkbox
        aria-label="전체 선택"
        checked={pageSelectionState(table)}
        onCheckedChange={(checked) => {
          if (checked) table.toggleAllPageRowsSelected(true);
          else table.resetRowSelection(true);
        }}
      />
    ),
    cell: ({ row }) => (
      <Checkbox
        aria-label={
          rowSelectionLabel
            ? `${rowSelectionLabel(row.original)} 선택`
            : "행 선택"
        }
        checked={row.getCanSelect() && row.getIsSelected()}
        disabled={!row.getCanSelect()}
        onCheckedChange={(checked) => row.toggleSelected(!!checked)}
        onClick={(event) => event.stopPropagation()}
      />
    ),
  };
}

const DEFAULT_ERROR_TITLE = "목록을 불러오지 못했습니다";
const DEFAULT_ERROR_WHY = "서버가 응답하지 않았거나 요청이 거부되었습니다.";
const DEFAULT_ERROR_NEXT = "잠시 후 다시 시도하세요.";

function DataTableError({
  title,
  message,
  onRetry,
}: {
  title: string;
  message: string | undefined;
  onRetry?: () => void | Promise<unknown>;
}) {
  // 재시도 진행 상태는 onRetry가 돌려준 Promise로 스스로 판단한다(페이지 prop 없음).
  // React 19는 unmount 후 setState를 무시하므로 mounted guard가 필요 없다.
  const [retrying, setRetrying] = React.useState(false);
  const handleRetry = () => {
    if (!onRetry || retrying) return;
    const result: unknown = onRetry();
    if (!(result instanceof Promise)) return;
    setRetrying(true);
    void result.catch(() => undefined).finally(() => setRetrying(false));
  };
  return (
    <Alert variant="destructive">
      <AlertTitle>{title}</AlertTitle>
      <AlertDescription>
        <span>{message ?? DEFAULT_ERROR_WHY}</span>
        {onRetry ? null : <span className="ml-1">{DEFAULT_ERROR_NEXT}</span>}
      </AlertDescription>
      {onRetry ? (
        <div className="mt-3 flex justify-end">
          <Button
            aria-busy={retrying || undefined}
            aria-disabled={retrying || undefined}
            size="sm"
            type="button"
            variant="outline"
            onClick={handleRetry}
          >
            다시 시도
          </Button>
        </div>
      ) : null}
    </Alert>
  );
}

export function VirtualTable<TData extends RowData>({
  columns,
  data,
  getRowId,
  isLoading,
  isError,
  error,
  errorTitle = DEFAULT_ERROR_TITLE,
  errorState,
  onRetry,
  emptyMessage = "데이터가 없습니다.",
  emptyState,
  skeletonRowCount = 6,
  sorting,
  onSortingChange,
  initialSorting = [],
  enableSortingRemoval = true,
  manualSorting = true,
  enableRowSelection = false,
  rowSelection,
  onRowSelectionChange,
  rowSelectionLabel,
  renderBulkActions,
  onRowClick,
  isRowActive,
  rowTestId,
  rowIdentity,
  virtualized = false,
  estimateRowSize = 40,
  overscan = 12,
  containerClassName,
  ariaLabel,
  caption,
  hideHeader,
  wrapCells,
  height,
  stickyHeader = false,
  containerStyle,
  containerTestId,
  containerRole,
  containerAriaLabel,
  containerTabIndex,
  tableTestId,
  tableSlot = "table",
  sortButtonTestIdPrefix,
  rowProps,
  renderRowDetails,
  renderCell,
}: DataTableProps<TData>) {
  "use no memo";

  const [internalSorting, setInternalSorting] =
    React.useState<SortingState>(initialSorting);
  const [internalSelection, setInternalSelection] =
    React.useState<RowSelectionState>({});

  const resolvedColumns = React.useMemo(
    () =>
      enableRowSelection
        ? [selectionColumn<TData>(rowSelectionLabel), ...columns]
        : columns,
    [columns, enableRowSelection, rowSelectionLabel],
  );

  // 기능 집합은 모듈 단위로 고정하고 제어 상태의 갱신 경로를 함께 넘긴다.
  const table = useTable({
    features,
    data,
    columns: resolvedColumns,
    getRowId,
    enableSortingRemoval,
    manualSorting,
    enableRowSelection,
    state: {
      sorting: sorting ?? internalSorting,
      ...(enableRowSelection
        ? { rowSelection: rowSelection ?? internalSelection }
        : {}),
    },
    onSortingChange: onSortingChange ?? setInternalSorting,
    onRowSelectionChange: onRowSelectionChange ?? setInternalSelection,
  });

  if (isError) {
    if (errorState !== undefined) return <>{errorState}</>;
    return (
      <DataTableError
        title={errorTitle}
        message={error?.message}
        onRetry={onRetry}
      />
    );
  }

  const rows = table.getRowModel().rows;
  const colCount = table.getAllLeafColumns().length;
  const selectedRows = enableRowSelection
    ? table.getSelectedRowModel().rows.filter((row) => row.getCanSelect())
    : [];
  const resolvedEmpty: DataTableEmptyState = emptyState ?? {
    title: emptyMessage,
  };

  const bulkBar =
    enableRowSelection && renderBulkActions && selectedRows.length > 0 ? (
      <div
        className="flex flex-wrap items-center gap-2 rounded-kt-control bg-kt-brand-tint px-3 py-2 text-xs text-kt-text-primary"
        data-slot="bulk-actions"
        role="region"
        aria-label="선택 항목 작업"
      >
        <span className="font-medium tabular-nums">
          {selectedRows.length}개 선택됨
        </span>
        {renderBulkActions(selectedRows)}
      </div>
    ) : null;

  return (
    <div className="space-y-2">
      {bulkBar}
      <TableSurface
        table={table}
        rows={rows}
        colCount={colCount}
        isLoading={isLoading}
        emptyState={resolvedEmpty}
        skeletonRowCount={skeletonRowCount}
        virtualized={virtualized}
        estimateRowSize={estimateRowSize}
        overscan={overscan}
        onRowClick={onRowClick}
        isRowActive={isRowActive}
        rowTestId={rowTestId}
        rowIdentity={rowIdentity}
        containerClassName={containerClassName}
        containerStyle={containerStyle}
        containerTestId={containerTestId}
        containerRole={containerRole}
        containerAriaLabel={containerAriaLabel}
        containerTabIndex={containerTabIndex}
        tableTestId={tableTestId}
        tableSlot={tableSlot}
        ariaLabel={ariaLabel}
        caption={caption}
        hideHeader={hideHeader}
        wrapCells={wrapCells}
        height={height}
        stickyHeader={stickyHeader}
        sortButtonTestIdPrefix={sortButtonTestIdPrefix}
        rowProps={rowProps}
        renderRowDetails={renderRowDetails}
        renderCell={renderCell}
      />
    </div>
  );
}

// skeleton 행 — 실제 행과 같은 셀 구조, 폭은 column마다 조금씩 다르게(형태가 맞는 skeleton).
const SKELETON_WIDTHS = [
  "w-3/4",
  "w-1/2",
  "w-2/3",
  "w-2/5",
  "w-3/5",
  "w-1/3",
] as const;

function skeletonWidth(rowIndex: number, columnIndex: number): string {
  return (
    SKELETON_WIDTHS[(rowIndex + columnIndex) % SKELETON_WIDTHS.length] ??
    "w-1/2"
  );
}

function SkeletonRows<TData extends RowData>({
  columns,
  rowCount,
  virtualized = false,
}: {
  columns: Column<TData, unknown>[];
  rowCount: number;
  virtualized?: boolean;
}) {
  const rowKeys = Array.from(
    { length: Math.max(1, rowCount) },
    (_, index) => `skeleton-row-${index + 1}`,
  );
  return (
    <>
      {rowKeys.map((rowKey, rowIndex) => (
        <TableRow
          className={cn("hover:bg-transparent", virtualized && "flex")}
          key={rowKey}
          role={virtualized ? "row" : undefined}
        >
          {columns.map((column, columnIndex) => {
            const meta = columnMeta(column);
            return (
              <TableCell
                className={cn(
                  alignClass(meta.align),
                  meta.className,
                  meta.cellClassName,
                )}
                key={`${rowKey}-${column.id}`}
                role={virtualized ? "cell" : undefined}
                style={
                  virtualized
                    ? { width: column.getSize(), flexShrink: 0 }
                    : undefined
                }
              >
                <Skeleton
                  className={cn(
                    "h-4",
                    skeletonWidth(rowIndex, columnIndex),
                    meta.align === "right" && "ml-auto",
                  )}
                />
              </TableCell>
            );
          })}
        </TableRow>
      ))}
    </>
  );
}

export {
  VirtualTable as DataTable,
  VirtualTableClampCell as DataTableClampCell,
};
export type VirtualTableProps<T extends RowData> = DataTableProps<T>;
export type VirtualTableColumnMeta = DataTableColumnMeta;
export type VirtualTableEmptyState = DataTableEmptyState;
function EmptyState({
  title,
  description,
  action,
  icon,
}: DataTableEmptyState & { size?: "sm" }) {
  return (
    <Empty className="items-start text-left">
      <EmptyHeader className="items-start">
        {icon ? <EmptyMedia>{icon}</EmptyMedia> : null}
        <EmptyTitle>{title}</EmptyTitle>
        {description ? (
          <EmptyDescription>{description}</EmptyDescription>
        ) : null}
      </EmptyHeader>
      {action ? (
        <EmptyContent className="items-start">{action}</EmptyContent>
      ) : null}
    </Empty>
  );
}

/** 확장행도 독립 가상 항목으로 측정하여 자막·상세 높이가 뒤 행의 위치에 반영된다. */
type SurfaceEntry<T extends RowData> =
  | { key: string; row: Row<T>; detail?: undefined }
  | { key: string; row: Row<T>; detail: React.ReactNode };

function TableSurface<T extends RowData>({
  table,
  rows,
  colCount,
  isLoading,
  emptyState,
  skeletonRowCount,
  virtualized,
  estimateRowSize,
  overscan,
  onRowClick,
  isRowActive,
  rowTestId,
  rowIdentity,
  containerClassName,
  containerStyle,
  containerTestId,
  containerRole,
  containerAriaLabel,
  containerTabIndex,
  tableTestId,
  tableSlot,
  ariaLabel,
  stickyHeader,
  sortButtonTestIdPrefix,
  rowProps,
  renderRowDetails,
  renderCell,
  caption,
  hideHeader,
  wrapCells,
  height,
}: {
  table: TanstackTable<T>;
  rows: Row<T>[];
  colCount: number;
  isLoading?: boolean;
  emptyState: DataTableEmptyState;
  skeletonRowCount: number;
  virtualized: boolean;
  estimateRowSize: number;
  overscan: number;
} & Pick<
  DataTableProps<T>,
  | "onRowClick"
  | "isRowActive"
  | "rowTestId"
  | "rowIdentity"
  | "containerClassName"
  | "containerStyle"
  | "containerTestId"
  | "containerRole"
  | "containerAriaLabel"
  | "containerTabIndex"
  | "tableTestId"
  | "caption"
  | "hideHeader"
  | "wrapCells"
  | "height"
  | "tableSlot"
  | "ariaLabel"
  | "stickyHeader"
  | "sortButtonTestIdPrefix"
  | "rowProps"
  | "renderRowDetails"
  | "renderCell"
>) {
  "use no memo";
  const { scrollRef, headRef, entries, items, totalSize, measure } =
    useSurfaceWindow({
      rows,
      isLoading,
      renderRowDetails,
      virtualized,
      estimateRowSize,
      overscan,
    });
  const groups = hideHeader ? [] : table.getHeaderGroups();
  const role = structuralRole(virtualized);
  const totalWidth = table.getTotalSize();
  return (
    <Table
      containerRef={scrollRef}
      containerClassName={cn("relative overflow-auto", containerClassName)}
      containerStyle={{ height, ...containerStyle }}
      containerTestId={containerTestId}
      containerRole={containerRole}
      containerAriaLabel={containerAriaLabel}
      containerTabIndex={containerTabIndex}
      data-slot={tableSlot}
      data-testid={tableTestId}
      aria-label={ariaLabel}
      aria-busy={isLoading || undefined}
      role={role("table")}
      aria-rowcount={virtualized ? entries.length + groups.length : undefined}
      aria-colcount={virtualized ? colCount : undefined}
      className={cn("tabular-nums", virtualized && "grid")}
      style={virtualized ? { minWidth: totalWidth } : undefined}
    >
      {caption ? <TableCaption>{caption}</TableCaption> : null}
      {!hideHeader ? (
        <TableHeaders
          table={table}
          headRef={headRef}
          virtualized={virtualized}
          stickyHeader={stickyHeader}
          sortButtonTestIdPrefix={sortButtonTestIdPrefix}
        />
      ) : null}
      <TableBody
        role={role("rowgroup")}
        className={virtualized ? "relative grid" : undefined}
        style={surfaceBodyStyle(
          virtualized,
          isLoading,
          entries.length,
          totalSize,
        )}
      >
        {isLoading ? (
          <SkeletonRows
            columns={table.getAllLeafColumns()}
            rowCount={skeletonRowCount}
            virtualized={virtualized}
          />
        ) : rows.length === 0 ? (
          <TableRow
            role={role("row")}
            className={virtualized ? "flex" : undefined}
          >
            <TableCell
              role={role("cell")}
              colSpan={colCount}
              className="w-full whitespace-normal"
            >
              <EmptyState {...emptyState} />
            </TableCell>
          </TableRow>
        ) : (
          items.map((item) => (
            <SurfaceEntryRow
              key={item.entry.key}
              {...item}
              virtualized={virtualized}
              headerRowCount={groups.length}
              colCount={colCount}
              measure={measure}
              onRowClick={onRowClick}
              isRowActive={isRowActive}
              rowTestId={rowTestId}
              rowIdentity={rowIdentity}
              rowProps={rowProps}
              wrapCells={wrapCells}
              renderCell={renderCell}
            />
          ))
        )}
      </TableBody>
    </Table>
  );
}

function structuralRole(virtualized: boolean) {
  return (
    value: "table" | "rowgroup" | "row" | "columnheader" | "rowheader" | "cell",
  ) => (virtualized ? value : undefined);
}

function TableHeaders<T extends RowData>({
  table,
  headRef,
  virtualized,
  stickyHeader,
  sortButtonTestIdPrefix,
}: {
  table: TanstackTable<T>;
  headRef: React.Ref<HTMLTableSectionElement>;
  virtualized: boolean;
} & Pick<DataTableProps<T>, "stickyHeader" | "sortButtonTestIdPrefix">) {
  const role = structuralRole(virtualized);
  const groups = table.getHeaderGroups();
  return (
    <TableHeader
      ref={headRef}
      role={role("rowgroup")}
      className={cn(
        (virtualized || stickyHeader) &&
          "sticky top-0 z-10 bg-kt-surface-subtle",
        virtualized && "grid",
      )}
    >
      {groups.map((group, groupIndex) => (
        <TableRow
          key={group.id}
          role={role("row")}
          aria-rowindex={virtualized ? groupIndex + 1 : undefined}
          className={virtualized ? "flex" : undefined}
        >
          {group.headers.map((header) => {
            const meta = columnMeta(header.column);
            const canSort = header.column.getCanSort();
            const sorted = header.column.getIsSorted();
            return (
              <TableHead
                key={header.id}
                colSpan={header.colSpan}
                role={role("columnheader")}
                aria-sort={canSort ? ariaSort(sorted) : undefined}
                style={{
                  ...(virtualized
                    ? { width: header.getSize(), flexShrink: 0 }
                    : {}),
                  textAlign: meta.align,
                  ...meta.headerStyle,
                }}
                className={cn(
                  alignClass(meta.align),
                  virtualized && "flex items-center",
                  virtualized && flexAlignClass(meta.align),
                  meta.className,
                  meta.headerClassName,
                )}
              >
                {renderHeadCellContent(
                  header,
                  sorted,
                  canSort,
                  sortButtonTestIdPrefix,
                )}
              </TableHead>
            );
          })}
        </TableRow>
      ))}
    </TableHeader>
  );
}

type RowDisplayProps<T extends RowData> = Pick<
  DataTableProps<T>,
  | "onRowClick"
  | "isRowActive"
  | "rowTestId"
  | "rowIdentity"
  | "rowProps"
  | "wrapCells"
  | "renderCell"
>;

function SurfaceEntryRow<T extends RowData>({
  entry,
  index,
  start,
  virtualized,
  headerRowCount,
  colCount,
  measure,
  onRowClick,
  isRowActive,
  rowTestId,
  rowIdentity,
  rowProps,
  wrapCells,
  renderCell,
}: {
  entry: SurfaceEntry<T>;
  index: number;
  start: number;
  virtualized: boolean;
  headerRowCount: number;
  colCount: number;
  measure: (node: HTMLTableRowElement | null) => void;
} & RowDisplayProps<T>) {
  const role = structuralRole(virtualized);
  const { row } = entry;
  const positioning: React.CSSProperties | undefined = virtualized
    ? {
        position: "absolute",
        display: "flex",
        width: "100%",
        transform: `translateY(${start}px)`,
      }
    : undefined;
  const measureRef = virtualized ? measure : undefined;
  if (entry.detail !== undefined)
    return (
      <TableRow
        key={entry.key}
        role={role("row")}
        data-index={index}
        ref={measureRef}
        style={positioning}
        aria-rowindex={virtualized ? index + headerRowCount + 1 : undefined}
      >
        <TableCell
          role={role("cell")}
          colSpan={colCount}
          className="w-full whitespace-normal"
        >
          {entry.detail}
        </TableCell>
      </TableRow>
    );
  return (
    <TableRow
      {...dataRowProps(
        row,
        virtualized,
        index + headerRowCount + 1,
        positioning,
        {
          onRowClick,
          isRowActive,
          rowTestId,
          rowIdentity,
          rowProps,
        },
      )}
      key={entry.key}
      data-index={index}
      ref={measureRef}
    >
      <DataCells
        row={row}
        virtualized={virtualized}
        wrapCells={wrapCells}
        renderCell={renderCell}
      />
    </TableRow>
  );
}

function dataRowProps<T extends RowData>(
  row: Row<T>,
  virtualized: boolean,
  rowIndex: number,
  positioning: React.CSSProperties | undefined,
  {
    onRowClick,
    isRowActive,
    rowTestId,
    rowIdentity,
    rowProps,
  }: RowDisplayProps<T>,
) {
  const active =
    (row.getCanSelect() && row.getIsSelected()) ||
    isRowActive?.(row.original) === true;
  const props = rowProps?.(row.original) ?? {};
  return {
    ...props,
    role: virtualized ? "row" : undefined,
    "data-row-identity": rowIdentity?.(row.original),
    "data-testid": rowTestId?.(row.original),
    "data-state": active ? "selected" : undefined,
    "aria-rowindex": virtualized ? rowIndex : undefined,
    "aria-selected":
      props["aria-selected"] ?? (onRowClick ? active : undefined),
    className: cn(onRowClick && CLICKABLE_ROW_CLASS, props.className),
    style: { ...props.style, ...positioning },
    tabIndex: props.tabIndex ?? (onRowClick ? 0 : undefined),
    onClick:
      props.onClick ??
      (onRowClick
        ? (event: React.MouseEvent<HTMLTableRowElement>) => {
            if (
              !(event.target instanceof Element) ||
              !event.target.closest(
                "button,a,input,select,textarea,[data-row-action]",
              )
            )
              onRowClick(row.original);
          }
        : undefined),
    onKeyDown:
      props.onKeyDown ??
      (onRowClick
        ? (event: React.KeyboardEvent<HTMLTableRowElement>) =>
            handleClickableRowKeyDown(event, row.original, onRowClick)
        : undefined),
  };
}

function DataCells<T extends RowData>({
  row,
  virtualized,
  wrapCells,
  renderCell,
}: {
  row: Row<T>;
  virtualized: boolean;
} & Pick<DataTableProps<T>, "wrapCells" | "renderCell">) {
  const role = structuralRole(virtualized);
  return (
    <>
      {row.getVisibleCells().map((cell) => {
        const meta = columnMeta(cell.column);
        const BodyCell = meta.rowHeader ? TableHead : TableCell;
        return (
          <BodyCell
            key={cell.id}
            role={role(meta.rowHeader ? "rowheader" : "cell")}
            scope={meta.rowHeader ? "row" : undefined}
            style={{
              ...(virtualized
                ? { width: cell.column.getSize(), flexShrink: 0 }
                : {}),
              textAlign: meta.align,
            }}
            className={cn(
              alignClass(meta.align),
              virtualized && "flex items-center",
              virtualized && flexAlignClass(meta.align),
              (meta.wrap || wrapCells) && "whitespace-normal",
              meta.className,
              meta.cellClassName,
            )}
          >
            {renderCell && cell.column.id !== "__select__"
              ? renderCell(row.original, cell.column.id)
              : flexRender(cell.column.columnDef.cell, cell.getContext())}
          </BodyCell>
        );
      })}
    </>
  );
}

function useHeaderHeight(virtualized: boolean) {
  const headRef = React.useRef<HTMLTableSectionElement>(null);
  const [headHeight, setHeadHeight] = React.useState(0);
  React.useEffect(() => {
    const element = headRef.current;
    if (!element || !virtualized) return;
    const update = () => setHeadHeight(element.getBoundingClientRect().height);
    update();
    if (typeof ResizeObserver === "undefined") return;
    const observer = new ResizeObserver(update);
    observer.observe(element);
    return () => observer.disconnect();
  }, [virtualized]);

  return { headRef, headHeight };
}

function surfaceEntries<T extends RowData>(
  rows: Row<T>[],
  isLoading: boolean | undefined,
  renderRowDetails: DataTableProps<T>["renderRowDetails"],
) {
  const entries: SurfaceEntry<T>[] = [];
  if (!isLoading)
    for (const row of rows) {
      entries.push({ key: JSON.stringify(["row", row.id]), row });
      const detail = renderRowDetails?.(row.original);
      if (detail !== null && detail !== undefined && detail !== false)
        entries.push({ key: JSON.stringify(["detail", row.id]), row, detail });
    }

  return entries;
}

function useSurfaceWindow<T extends RowData>({
  rows,
  isLoading,
  renderRowDetails,
  virtualized,
  estimateRowSize,
  overscan,
}: {
  rows: Row<T>[];
  isLoading?: boolean;
  virtualized: boolean;
  estimateRowSize: number;
  overscan: number;
} & Pick<DataTableProps<T>, "renderRowDetails">) {
  "use no memo";
  const scrollRef = React.useRef<HTMLDivElement>(null);
  const { headRef, headHeight } = useHeaderHeight(virtualized);

  const entries = surfaceEntries(rows, isLoading, renderRowDetails);
  const virtualizer = useVirtualizer({
    enabled: virtualized && !isLoading,
    count: entries.length,
    getScrollElement: () => scrollRef.current,
    estimateSize: () => estimateRowSize,
    getItemKey: (index) => entries[index]?.key ?? index,
    overscan,
    scrollMargin: headHeight,
    measureElement: (element) => element.getBoundingClientRect().height,
  });
  const virtualItems = virtualizer.getVirtualItems();
  const items = virtualized
    ? virtualItems.flatMap((item) => {
        const entry = entries[item.index];
        return entry
          ? [{ entry, index: item.index, start: item.start - headHeight }]
          : [];
      })
    : entries.map((entry, index) => ({ entry, index, start: 0 }));

  return {
    scrollRef,
    headRef,
    entries,
    items,
    totalSize: virtualizer.getTotalSize(),
    measure: virtualizer.measureElement,
  };
}

function surfaceBodyStyle(
  virtualized: boolean,
  isLoading: boolean | undefined,
  count: number,
  totalSize: number,
) {
  return virtualized && !isLoading && count
    ? { height: totalSize, width: "100%" }
    : undefined;
}
