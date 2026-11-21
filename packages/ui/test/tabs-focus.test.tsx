// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
import { render, screen } from "@testing-library/react";
import { expect, it } from "vitest";
import { Tabs, TabsList, TabsTrigger } from "../src/tabs.js";

// FS-7.8·UX-G9.1: Button과 같은 포커스 레시피 — 불투명 outline 2px·offset 2px 하나, ring·border·두 번째 outline 없음.
const FORBIDDEN = /(?:^|:)(?:outline-none|outline-solid|transition-all)$|(?:^|:)focus(?:-visible|-within)?:(?:ring|border|shadow|outline-(?:1|ring|none|solid))|(?:^|:)active:\S*translate/;

it("TabsTrigger 포커스는 Button과 같은 UX-G9.1 outline 하나이며 ring·border 변화·outline-1·transition-all을 쓰지 않는다", () => {
  for (const variant of ["default", "line"] as const) {
    const { unmount } = render(
      <Tabs defaultValue="one">
        <TabsList variant={variant}>
          <TabsTrigger value="one">첫 탭</TabsTrigger>
          <TabsTrigger value="two">둘째 탭</TabsTrigger>
        </TabsList>
      </Tabs>,
    );
    for (const name of ["첫 탭", "둘째 탭"]) {
      const trigger = screen.getByRole("tab", { name });
      const classes = trigger.className.split(/\s+/).filter(Boolean);
      expect(classes).toEqual(expect.arrayContaining(["focus-visible:outline-2", "focus-visible:outline-offset-2", "focus-visible:outline-kt-focus"]));
      expect(classes.filter(cls => /focus-visible:outline-/.test(cls)).sort()).toEqual(["focus-visible:outline-2", "focus-visible:outline-kt-focus", "focus-visible:outline-offset-2"]);
      expect(classes.filter(cls => FORBIDDEN.test(cls))).toEqual([]);
      // 테두리 두께는 상태와 무관하게 1px 하나(border)로 고정 — 상태 접두 border-width 변화 금지.
      expect(classes.filter(cls => /:border(?:-[xytrbl])?-(?:\d+|\[[^\]]+\])$/.test(cls))).toEqual([]);
    }
    unmount();
  }
});
