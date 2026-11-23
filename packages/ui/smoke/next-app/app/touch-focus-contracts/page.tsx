// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"use client";
import { VirtualTable, type ColumnDef } from "@kor-travel/ui/virtual-table";
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@kor-travel/ui/accordion";
import { Button } from "@kor-travel/ui/button";
import { Input } from "@kor-travel/ui/input";
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from "@kor-travel/ui/dialog";

// ui 0.2.6 회귀 표면: 선택 열 터치 영역·아코디언 안쪽 포커스 outline·Dialog 긴 제목.
type Entry = { id: string; name: string };
const entries: Entry[] = Array.from({ length: 5 }, (_, index) => ({ id: String(index), name: "행 " + (index + 1) }));
const columns: ColumnDef<Entry, unknown>[] = [
  { accessorKey: "name", header: "이름", size: 300 },
  {
    id: "action", header: "작업", size: 120,
    cell: ({ row }) => <Button size="xs" variant="outline" data-row-action
      data-testid={"row-action-" + row.original.id}>작업 {row.original.name}</Button>,
  },
];

const LONG_TITLE = "아주 긴 다이얼로그 제목이 좁은 화면에서 줄바꿈되어도 닫기 버튼과 겹치지 않아야 합니다 "
  + "kor-travel-map-admin-feature-load-schedule-identifier-without-spaces";

function SelectionTable({ testId, virtualized, selectable, clickable = false }: { testId: string; virtualized: boolean; selectable: boolean; clickable?: boolean }) {
  return <section data-testid={testId} style={{ display: "grid", minWidth: 0 }}>
    <VirtualTable columns={columns} data={entries} getRowId={(row) => row.id}
      ariaLabel={testId} caption={testId} virtualized={virtualized} height={virtualized ? 320 : undefined}
      enableRowSelection={selectable} rowSelectionLabel={(row) => testId + " " + row.name}
      onRowClick={clickable ? () => undefined : undefined} estimateRowSize={40} />
  </section>;
}

export default function TouchFocusContracts() {
  return (
    <main style={{ display: "grid", gridTemplateColumns: "minmax(0, 1fr)", gap: 24, padding: 16, boxSizing: "border-box", width: "100%" }}>
      <style>{"html,body{margin:0;overflow-x:clip}"}</style>
      <h1>터치 영역·포커스·다이얼로그 제목 검증</h1>
      <SelectionTable testId="select-table" virtualized={false} selectable clickable />
      <SelectionTable testId="select-table-virtual" virtualized selectable />
      <SelectionTable testId="plain-table" virtualized={false} selectable={false} />

      <Accordion type="multiple" defaultValue={["open"]} data-testid="accordion">
        <AccordionItem value="open">
          <AccordionTrigger>처음부터 열린 항목</AccordionTrigger>
          <AccordionContent>
            <Button data-testid="accordion-open-button">가장자리 버튼</Button>
            <Input aria-label="열린 항목 입력" data-testid="accordion-open-input" />
          </AccordionContent>
        </AccordionItem>
        <AccordionItem value="toggle">
          <AccordionTrigger>눌러서 여는 항목</AccordionTrigger>
          <AccordionContent>
            <Input aria-label="연 항목 입력" data-testid="accordion-toggle-input" />
          </AccordionContent>
        </AccordionItem>
      </Accordion>

      {/* 검출기 대조군: 일부러 overflow:hidden으로 자른 같은 버튼. 검사가 잘림을 실제로 보는지 확인한다. */}
      <div data-testid="clip-control" style={{ overflow: "hidden" }}>
        <Button data-testid="clip-control-button">잘린 대조 버튼</Button>
      </div>

      <Dialog>
        <DialogTrigger asChild><Button variant="outline">긴 제목 다이얼로그 열기</Button></DialogTrigger>
        <DialogContent data-testid="long-title-dialog">
          <DialogHeader>
            <DialogTitle data-testid="long-title">{LONG_TITLE}</DialogTitle>
            <DialogDescription>제목 오른쪽은 닫기 버튼 자리로 비워 둡니다.</DialogDescription>
          </DialogHeader>
        </DialogContent>
      </Dialog>
    </main>
  );
}
