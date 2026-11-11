// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { expect, it } from "vitest";
import { Progress } from "../src/progress.js";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "../src/tabs.js";
import { MapTabs, MapTabPanel, MapViewTabs } from "../src/map-controls.js";

it("세로 탭은 실제 Radix 방향과 ArrowDown 탐색을 유지한다", async () => {
  render(<Tabs orientation="vertical" defaultValue="one"><TabsList><TabsTrigger value="one">첫 탭</TabsTrigger><TabsTrigger value="two">둘째 탭</TabsTrigger></TabsList><TabsContent value="one">첫 내용</TabsContent><TabsContent value="two">둘째 내용</TabsContent></Tabs>);
  expect(screen.getByRole("tablist")).toHaveAttribute("aria-orientation", "vertical");
  const user = userEvent.setup();
  screen.getByRole("tab", { name: "첫 탭" }).focus();
  await user.keyboard("{ArrowDown}");
  expect(screen.getByRole("tab", { name: "둘째 탭" })).toHaveFocus();
  expect(screen.getByRole("tab", { name: "둘째 탭" })).toHaveAttribute("aria-selected", "true");
});

it("지도 패널 forceMount는 상태를 보존하면서 비활성 영역을 숨긴다", async () => {
  const { container } = render(<MapTabs defaultValue="map"><MapViewTabs viewport={null} /><MapTabPanel value="map" forceMount><input aria-label="지도 조건" defaultValue="서울" /></MapTabPanel><MapTabPanel value="list" forceMount>목록 내용</MapTabPanel></MapTabs>);
  const field = screen.getByRole("textbox", { name: "지도 조건" });
  const mapPanel = field.closest('[data-slot="tabs-content"]')!;
  const user = userEvent.setup();
  await user.type(field, "역");
  await user.click(screen.getByRole("tab", { name: "목록" }));
  expect(mapPanel).toHaveAttribute("hidden");
  expect(screen.queryByRole("textbox", { name: "지도 조건" })).toBeNull();
  await user.click(screen.getByRole("tab", { name: "지도" }));
  expect(mapPanel).not.toHaveAttribute("hidden");
  expect(screen.getByRole("textbox", { name: "지도 조건" })).toBe(field);
  expect(field).toHaveValue("서울역");
  expect(container.querySelectorAll('[data-slot="tabs-content"]')).toHaveLength(2);
});

it("진행 값·최댓값·미확정 상태를 시각 표현과 ARIA에 같이 전달한다",()=>{
  const {container,rerender}=render(<Progress aria-label="진행" value={60} max={200}/>);
  const bar=screen.getByRole("progressbar",{name:"진행"});
  expect(bar).toHaveAttribute("aria-valuenow","60");
  expect(bar).toHaveAttribute("aria-valuemax","200");
  expect(container.querySelector('[data-slot="progress-indicator"]')).toHaveStyle({transform:"translateX(-70%)"});
  rerender(<Progress aria-label="진행" value={0}/>);
  expect(bar).toHaveAttribute("aria-valuenow","0");
  rerender(<Progress aria-label="진행" value={100}/>);
  expect(bar).toHaveAttribute("data-state","complete");
  rerender(<Progress aria-label="진행" value={null}/>);
  expect(bar).toHaveAttribute("data-state","indeterminate");
  expect(bar).not.toHaveAttribute("aria-valuenow");
});
