// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
import { render, screen } from "@testing-library/react";
import { expect, it } from "vitest";
import { Button } from "../src/button.js";
import { buttonVariants } from "../src/button-variants.js";

it("Button 포커스는 UX-G9.1 outline 하나이며 반투명 ring·outline-none·transition-all을 쓰지 않는다", () => {
  for (const variant of ["default", "outline", "secondary", "ghost", "destructive", "destructive-solid", "link"] as const) {
    const classes = buttonVariants({ variant }).split(/\s+/);
    expect(classes).toEqual(expect.arrayContaining(["focus-visible:outline-2", "focus-visible:outline-offset-2", "focus-visible:outline-kt-focus"]));
    expect(classes.filter(name => /^(?:outline-none|outline-solid|transition-all)$|focus-visible:(?:ring|border)/.test(name))).toEqual([]);
  }
  render(<Button variant="outline">저장</Button>);
  expect(screen.getByRole("button", { name: "저장" })).toHaveClass("border", "border-border", "focus-visible:outline-2");
});
