// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"use client";
import * as React from "react";
import { VirtualTable, type ColumnDef } from "@kor-travel/ui/virtual-table";
import { Input } from "@kor-travel/ui/input";

type Entry = { id: string; name: string; description: string };
const entries: Entry[] = Array.from({ length: 80 }, (_, index) => ({
  id: String(index),
  name: "원천_도로명주소_전자지도_긴_테이블_이름_" + index,
  description: "모바일에서도 가로 스크롤로 끝까지 접근하는 설명 " + index,
}));
const columns: ColumnDef<Entry, unknown>[] = [
  { accessorKey: "name", header: "테이블 이름", size: 400 },
  { accessorKey: "description", header: "설명", size: 500 },
];

export default function VirtualTableContracts() {
  const [query, setQuery] = React.useState("");
  const [virtualized, setVirtualized] = React.useState(false);
  const rows = entries.filter((row) => row.name.includes(query));
  return (
    <main data-testid="table-contract-main" style={{
      display: "grid", gridTemplateColumns: "minmax(0, 1fr)",
      padding: 24, boxSizing: "border-box", width: "100%",
    }}>
      <style>{"html,body{margin:0;overflow-x:clip}"}</style>
      <h1>공통 표 좁은 grid 검증</h1>
      <label>표 검색<Input aria-label="표 검색" value={query}
        onChange={(event) => setQuery(event.target.value)} /></label>
      <button type="button" onClick={() => setVirtualized((value) => !value)}>
        {virtualized ? "일반 표로 전환" : "가상 표로 전환"}
      </button>
      <section data-testid="table-contract-grid" style={{ display: "grid", minWidth: 0, gap: 8 }}>
        <VirtualTable columns={columns} data={rows} getRowId={(row) => row.id}
          caption="공통 표 크기 계약" ariaLabel="공통 표 크기 계약"
          virtualized={virtualized} stickyHeader height={180}
          containerTestId="table-contract-scroller" estimateRowSize={40} />
      </section>
    </main>
  );
}
