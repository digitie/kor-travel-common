// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
import { render, screen } from "@testing-library/react";
import { expect, it } from "vitest";
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "../src/accordion.js";
import { Dialog, DialogContent, DialogTitle } from "../src/dialog.js";
import { VirtualTable, type ColumnDef } from "../src/virtual-table.js";

// ui 0.2.6 회귀 고정. 실제 기하(겹침·잘림·줄바꿈)는 smoke/touch-focus-browser.spec.ts가
// 320/390/1440에서 브라우저로 잰다. 여기서는 그 기하를 만드는 클래스 계약을 고정한다.

function classesOf(element: Element | null): string[] {
  expect(element).not.toBeNull();
  return (element!.getAttribute("class") ?? "").split(/\s+/).filter(Boolean);
}

type Item = { id: string; name: string };
const rows: Item[] = [{ id: "a", name: "가" }, { id: "b", name: "나" }];
const columns: ColumnDef<Item, unknown>[] = [{ accessorKey: "name", header: "이름" }];

for (const virtualized of [false, true]) {
  it(`VirtualTable 선택 칸(${virtualized ? "가상" : "일반"})은 md 미만에서 체크박스 터치 영역과 같은 44px이다`, () => {
    render(<VirtualTable columns={columns} data={rows} getRowId={(row) => row.id}
      ariaLabel="선택 표" enableRowSelection virtualized={virtualized} height={200} />);
    const boxes = screen.getAllByRole("checkbox");
    // jsdom에는 레이아웃이 없어 가상 표는 머리 행만 그린다(행 기하는 브라우저 smoke가 잰다).
    expect(boxes).toHaveLength(virtualized ? 1 : 3);
    for (const box of boxes) {
      const cls = classesOf(box);
      // 체크박스의 md 미만 터치 영역(padding box 14px + 2×15px = 44px)은 그대로 두고 칸 가운데에 놓는다.
      expect(cls).toEqual(expect.arrayContaining(["relative", "size-4", "max-md:after:-inset-[15px]", "max-md:mx-auto"]));
      const cell = box.closest('[data-slot="table-cell"],[data-slot="table-head"]');
      const cellCls = classesOf(cell);
      // 칸 = 44×44, padding 없음 → 터치 영역이 칸 밖(이웃 행·옆 칸)으로 새지 않는다.
      expect(cellCls).toEqual(expect.arrayContaining(["max-md:h-11", "max-md:w-11", "max-md:min-w-11", "max-md:p-0"]));
      // 칸을 positioned로 만들지 않는다(클릭 가능한 행 outline·선택 배경이 첫 칸에서 끊기지 않게).
      expect(cellCls.filter((c) => /^(?:relative|absolute|sticky|fixed)$/.test(c))).toEqual([]);
      // 데스크톱 밀도: 접두 없는 높이·폭 변경을 더하지 않는다(행 높이·36px 열 그대로).
      expect(cellCls.filter((c) => /^(?:h|min-h|w|min-w)-/.test(c)).filter((c) => c !== "h-10")).toEqual([]);
    }
    // 가상 표는 md 미만 선택 칸이 넓어진 8px을 표 최소 폭에 더한다(일반 표는 auto 배치가 받는다).
    const tableEl = screen.getByRole("table");
    if (virtualized) expect(classesOf(tableEl)).toContain("max-md:[--kt-vt-select-extra:8px]");
    else expect(classesOf(tableEl)).not.toContain("max-md:[--kt-vt-select-extra:8px]");
    // 선택 열이 아닌 칸에는 번지지 않는다.
    const nameCell = screen.getByText("이름").closest('[data-slot="table-cell"],[data-slot="table-head"]');
    expect(classesOf(nameCell)).not.toContain("max-md:h-11");
  });
}

it("AccordionContent는 overflow:hidden 대신 outline 폭(4px) clip-margin을 둔 overflow:clip으로 자른다", () => {
  const { container } = render(
    <Accordion type="single" defaultValue="a" collapsible>
      <AccordionItem value="a"><AccordionTrigger>항목</AccordionTrigger>
        <AccordionContent><button type="button">안쪽 버튼</button></AccordionContent>
      </AccordionItem>
    </Accordion>,
  );
  const content = classesOf(container.querySelector('[data-slot="accordion-content"]'));
  expect(content.filter((c) => /^(?:[\w-]+:)*overflow-/.test(c))).toEqual(["overflow-clip"]);
  const margin = content.find((c) => c.startsWith("[overflow-clip-margin:"));
  // outline 2px + offset 2px = 4px 이상.
  expect(Number.parseFloat(/:(\d+(?:\.\d+)?)px\]$/.exec(margin ?? "")?.[1] ?? "0")).toBeGreaterThanOrEqual(4);
});

it("DialogTitle은 닫기 버튼이 있을 때만 오른쪽에 버튼 자리를 비우고, 소비자 padding이 이긴다", () => {
  const { unmount } = render(<Dialog open><DialogContent data-testid="content"><DialogTitle>제목</DialogTitle></DialogContent></Dialog>);
  expect(classesOf(screen.getByText("제목"))).toEqual(expect.arrayContaining(["pr-7", "wrap-anywhere"]));
  // 닫기 버튼: top-2 right-2(8px) + icon-sm(size-7 = 28px) = 오른쪽 36px. 본문 p-4(16px) 안쪽에서
  // 제목이 비워야 할 폭은 20px, pr-7(28px)은 8px 간격을 더 둔다.
  const close = screen.getByRole("button", { name: "닫기" });
  expect(classesOf(close)).toEqual(expect.arrayContaining(["absolute", "top-2", "right-2", "size-7"]));
  expect(classesOf(screen.getByTestId("content"))).toContain("p-4");
  unmount();

  const second = render(<Dialog open><DialogContent><DialogTitle className="pr-0">덮은 제목</DialogTitle></DialogContent></Dialog>);
  const overridden = classesOf(screen.getByText("덮은 제목"));
  expect(overridden).toContain("pr-0");
  expect(overridden).not.toContain("pr-7");
  second.unmount();

  for (const props of [{ showCloseButton: false }, { unstyled: true }]) {
    const view = render(<Dialog open><DialogContent {...props}><DialogTitle>빈 제목</DialogTitle></DialogContent></Dialog>);
    expect(classesOf(screen.getByText("빈 제목"))).not.toContain("pr-7");
    view.unmount();
  }
});
