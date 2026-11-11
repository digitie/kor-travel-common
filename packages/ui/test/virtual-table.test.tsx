// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
import * as React from "react";
import { act, fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { VirtualTable, type ColumnDef, type SortingState } from "../src/virtual-table.js";

type Item = { id: string; name: string; score: number };
const data: Item[] = [
  { id: "a", name: "가", score: 2 }, { id: "b", name: "나", score: 5 },
];
const columns: ColumnDef<Item, unknown>[] = [
  { accessorKey: "name", header: "이름", meta: { headerStyle: { width: 180 }, wrap: true } },
  { accessorKey: "score", header: "점수", sortDescFirst: false },
  { id: "action", header: "작업", enableSorting: false, cell: () => <button>행 작업</button> },
];
const getRowId = (item: Item) => item.id;
const rowNames = () => screen.getAllByRole("row").slice(1).map(row => within(row).getAllByRole("cell")[0]?.textContent);
afterEach(() => { vi.restoreAllMocks(); vi.unstubAllGlobals(); });

describe("VirtualTable 소비자 계약", () => {
  it("기본 서버 정렬은 입력 순서를 보존하며 정렬 상태만 갱신한다", () => {
    render(<VirtualTable data={data} columns={columns} getRowId={getRowId} />);
    fireEvent.click(screen.getByRole("button", { name: "점수" }));
    expect(screen.getByRole("columnheader", { name: "점수" })).toHaveAttribute("aria-sort", "ascending");
    fireEvent.click(screen.getByRole("button", { name: "점수" }));
    expect(rowNames()).toEqual(["가", "나"]);
  });
  it("클라이언트 정렬은 실제 데이터를 정렬하며 초기 정렬과 제거 금지를 지킨다", () => {
    render(<VirtualTable data={data} columns={columns} manualSorting={false}
      initialSorting={[{ id: "score", desc: true }]} enableSortingRemoval={false}
      sortButtonTestIdPrefix="admin-table-sort-" />);
    expect(rowNames()).toEqual(["나", "가"]);
    fireEvent.click(screen.getByTestId("admin-table-sort-score"));
    expect(rowNames()).toEqual(["가", "나"]);
    fireEvent.click(screen.getByTestId("admin-table-sort-score"));
    expect(rowNames()).toEqual(["나", "가"]);
  });
  it("제어 정렬의 함수형 updater와 외부 상태 변경이 반영된다", () => {
    function Controlled() {
      const [sorting, setSorting] = React.useState<SortingState>([]);
      return <><button onClick={() => setSorting([{ id: "score", desc: true }])}>외부 정렬</button>
        <VirtualTable data={data} columns={columns} manualSorting={false} sorting={sorting} onSortingChange={setSorting} /></>;
    }
    render(<Controlled />);
    fireEvent.click(screen.getByRole("button", { name: "외부 정렬" }));
    expect(rowNames()).toEqual(["나", "가"]);
    fireEvent.click(screen.getByRole("button", { name: "점수" }));
    expect(rowNames()).toEqual(["가", "나"]);
  });
  it("선택 predicate·중간 상태·bulk action과 데이터 교체를 일관되게 처리한다", () => {
    const { rerender } = render(<VirtualTable data={data} columns={columns} getRowId={getRowId}
      enableRowSelection rowSelectionLabel={item => item.name}
      renderBulkActions={rows => <span>{rows.map(row => row.original.name).join(",")}</span>} />);
    fireEvent.click(screen.getByRole("checkbox", { name: "가 선택" }));
    expect(screen.getByRole("checkbox", { name: "전체 선택" })).toHaveAttribute("data-state", "indeterminate");
    expect(screen.getByRole("region", { name: "선택 항목 작업" })).toHaveTextContent("1개 선택됨");
    fireEvent.click(screen.getByRole("checkbox", { name: "전체 선택" }));
    expect(screen.getByRole("checkbox", { name: "전체 선택" })).toHaveAttribute("data-state", "checked");
    rerender(<VirtualTable data={data} columns={columns} getRowId={getRowId}
      enableRowSelection={row => row.original.score > 3} rowSelectionLabel={item => item.name} />);
    expect(screen.getByRole("checkbox", { name: "가 선택" })).toBeDisabled();
  });
  it("실제 스크롤 요소의 속성·고정 헤더·표/행 identity를 보존한다", () => {
    render(<VirtualTable data={data} columns={columns} getRowId={getRowId}
      containerTestId="scroll" containerClassName="max-h-80" containerStyle={{ maxHeight: 320 }}
      tableTestId="table" stickyHeader rowIdentity={item => item.id} rowTestId={item => "row-" + item.id} />);
    const scroll = screen.getByTestId("scroll");
    expect(scroll).toHaveAttribute("data-slot", "table-container");
    expect(scroll).toHaveClass("max-h-80");
    expect(scroll).toHaveStyle({ maxHeight: "320px" });
    expect(scroll).toContainElement(screen.getByTestId("table"));
    expect(screen.getByTestId("row-a")).toHaveAttribute("data-row-identity", "a");
    expect(screen.getByRole("columnheader", { name: "이름" })).toHaveStyle({ width: "180px" });
    expect(screen.getByTestId("table").querySelector("thead")).toHaveClass("sticky");
  });
  it("rowProps와 확장행을 보존하며 셀 안 작업을 행 선택으로 중복 처리하지 않는다", () => {
    const onRowClick = vi.fn();
    render(<VirtualTable data={data} columns={columns} getRowId={getRowId}
      onRowClick={onRowClick} rowTestId={item => "row-" + item.id}
      rowProps={item => ({ className: "custom-row", "aria-expanded": item.id === "a" })}
      renderRowDetails={item => item.id === "a" ? <div>가의 자막</div> : null} />);
    const row = screen.getByTestId("row-a");
    expect(row).toHaveClass("custom-row");
    expect(row).toHaveAttribute("aria-expanded", "true");
    expect(screen.getByText("가의 자막").closest("td")).toHaveAttribute("colspan", "3");
    fireEvent.click(within(row).getByRole("button"));
    fireEvent.keyDown(within(row).getByRole("button"), { key: "Enter" });
    expect(onRowClick).not.toHaveBeenCalled();
    fireEvent.click(row);
    fireEvent.keyDown(row, { key: "Enter" });
    fireEvent.keyDown(row, { key: " " });
    expect(onRowClick).toHaveBeenCalledTimes(3);
  });
  it("로딩은 stale 데이터를 숨기고 빈 상태와 오류 슬롯을 구분한다", () => {
    const { rerender } = render(<VirtualTable columns={columns} data={data} isLoading skeletonRowCount={2} />);
    expect(screen.getByRole("table")).toHaveAttribute("aria-busy", "true");
    expect(screen.queryByText("가")).not.toBeInTheDocument();
    rerender(<VirtualTable columns={columns} data={[]} emptyState={{ title: "비어 있음", description: "검색을 변경하세요", action: <button>초기화</button> }} />);
    expect(screen.getByRole("button", { name: "초기화" })).toBeInTheDocument();
    rerender(<VirtualTable columns={columns} data={[]} isError errorState={<p role="alert">앱 오류</p>} />);
    expect(screen.getByRole("alert")).toHaveTextContent("앱 오류");
  });
  it("비동기 재시도는 중복 실행을 막고 완료 후 다시 활성화된다", async () => {
    let finish!: () => void;
    const retry = vi.fn(() => new Promise<void>(resolve => { finish = resolve; }));
    render(<VirtualTable columns={columns} data={[]} isError onRetry={retry} />);
    const button = screen.getByRole("button", { name: "다시 시도" });
    fireEvent.click(button);
    fireEvent.click(button);
    expect(retry).toHaveBeenCalledTimes(1);
    await act(async () => finish());
    expect(button).not.toHaveAttribute("aria-busy");
  });
  it("그룹 헤더의 colSpan과 표 이름을 유지한다", () => {
    const grouped: ColumnDef<Item, unknown>[] = [{ header: "묶음", columns: columns.slice(0, 2) }];
    render(<VirtualTable data={data} columns={grouped} ariaLabel="표 이름" />);
    expect(screen.getByRole("table", { name: "표 이름" })).toBeInTheDocument();
    expect(screen.getByRole("columnheader", { name: "묶음" })).toHaveAttribute("colspan", "2");
  });
  it("Geo 캡션·행 제목·헤더 숨김·줄바꿈·높이를 보존한다", () => {
    const geoColumns: ColumnDef<Item, unknown>[] = [
      { accessorKey: "name", header: "이름", meta: { rowHeader: true } },
      { accessorKey: "score", header: "점수" },
    ];
    render(<VirtualTable data={data} columns={geoColumns} caption="Geo 결과" hideHeader
      height={320} wrapCells containerTestId="geo-scroll" />);
    expect(screen.getByRole("table", { name: "Geo 결과" })).toBeInTheDocument();
    expect(screen.getAllByRole("rowheader")).toHaveLength(2);
    expect(screen.getAllByRole("rowheader")[0]).toHaveAttribute("scope", "row");
    expect(screen.getAllByRole("cell")[0]).toHaveClass("whitespace-normal");
    expect(screen.getByTestId("geo-scroll")).toHaveStyle({ height: "320px" });
    expect(screen.queryByRole("columnheader")).not.toBeInTheDocument();
    expect(screen.getByRole("table").querySelector("thead")).toBeNull();
  });
  it("직접 셀 renderer는 무관한 열 배열 교체 뒤에도 스트림 소유 셀을 재마운트하지 않는다", () => {
    const opens = vi.fn();
    const closes = vi.fn();
    function StreamCell({ id }: { id: string }) {
      React.useEffect(() => { opens(id); return () => { closes(id); }; }, [id]);
      return <span>{id} 스트림</span>;
    }
    const freshColumns = (): ColumnDef<Item, unknown>[] => [
      { id: "stream", cell: ({ row }) => <StreamCell id={row.original.id} /> },
    ];
    const direct = (item: Item) => <StreamCell id={item.id} />;
    const { rerender } = render(<VirtualTable data={data} columns={freshColumns()} getRowId={getRowId} renderCell={direct} />);
    expect(opens).toHaveBeenCalledTimes(2);
    rerender(<VirtualTable data={[...data]} columns={freshColumns()} getRowId={getRowId} renderCell={direct} />);
    expect(opens).toHaveBeenCalledTimes(2);
    expect(closes).not.toHaveBeenCalled();
  });
  it("실제 virtualizer가 행 수를 제한하고 스크롤 뒤 identity·상세행을 유지한다", async () => {
    vi.spyOn(HTMLElement.prototype, "clientHeight", "get").mockReturnValue(160);
    vi.spyOn(HTMLElement.prototype, "clientWidth", "get").mockReturnValue(800);
    vi.spyOn(HTMLElement.prototype, "getBoundingClientRect").mockImplementation(function(this: HTMLElement) {
      return { x: 0, y: 0, top: 0, left: 0, right: 800, bottom: 40, width: 800,
        height: this.tagName === "THEAD" ? 40 : 40, toJSON() {} } as DOMRect;
    });
    class Observer {
      constructor(_callback: ResizeObserverCallback) {}
      observe() {} unobserve() {} disconnect() {}
    }
    vi.stubGlobal("ResizeObserver", Observer);
    const many = Array.from({ length: 100 }, (_, index) => ({ id: String(index), name: "이름" + index, score: index }));
    render(<VirtualTable data={many} columns={columns} getRowId={getRowId} virtualized overscan={2}
      containerTestId="scroll" rowTestId={item => "row-" + item.id} rowIdentity={item => item.id}
      renderRowDetails={item => item.id === "50" ? <p>50 상세</p> : null} />);
    await waitFor(() => expect(screen.getByTestId("row-0")).toBeInTheDocument());
    expect(screen.getAllByRole("row").length).toBeLessThan(20);
    expect(screen.getByRole("table")).toHaveAttribute("aria-rowcount", "102");
    const scroll = screen.getByTestId("scroll");
    scroll.scrollTop = 2000;
    fireEvent.scroll(scroll);
    await waitFor(() => expect(screen.getByTestId("row-50")).toHaveAttribute("data-row-identity", "50"));
    expect(screen.getByText("50 상세")).toBeInTheDocument();
    expect(screen.getByTestId("row-50")).toHaveAttribute("aria-rowindex", "52");
  });
});
