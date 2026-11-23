// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
import { render } from "@testing-library/react";
import { expect, it } from "vitest";
import { Accordion, AccordionItem, AccordionTrigger } from "../src/accordion.js";
import { Badge } from "../src/badge.js";
import { Checkbox } from "../src/checkbox.js";
import { Field, FieldLabel } from "../src/field.js";
import { Input } from "../src/input.js";
import { NativeSelect, NativeSelectOption } from "../src/native-select.js";
import { ScrollArea } from "../src/scroll-area.js";
import { Select, SelectTrigger, SelectValue } from "../src/select.js";
import { Switch } from "../src/switch.js";
import { Textarea } from "../src/textarea.js";

// FS-7.8·UX-G9.1: 포커스 가능한 공통 컨트롤은 Button과 같은 레시피 하나다 —
// 불투명 outline 2px·offset 2px(--kt-focus). 반투명 ring·테두리 색 변화·outline-none·transition-all 없음.
const RECIPE = ["focus-visible:outline-2", "focus-visible:outline-kt-focus", "focus-visible:outline-offset-2"];
const FORBIDDEN = /(?:^|:)(?:outline-none|outline-solid|transition-all)$|(?:^|:)focus(?:-visible|-within)?:(?:ring|border|shadow|outline-(?:1|ring|none|solid))|(?:^|:)focus(?:-visible)?:after:border|has-\[:focus-visible\]|group-has-\[:focus-visible\]/;

function classesOf(element: Element | null): string[] {
  expect(element).not.toBeNull();
  return (element!.getAttribute("class") ?? "").split(/\s+/).filter(Boolean);
}

function expectSingleOutline(name: string, element: Element | null) {
  const classes = classesOf(element);
  expect(classes.filter(cls => /^focus-visible:outline-/.test(cls)).sort(), name).toEqual(RECIPE);
  expect(classes.filter(cls => FORBIDDEN.test(cls)), name).toEqual([]);
  // 테두리 두께는 상태와 무관하게 하나다(상태 접두 border-width 변화 금지).
  expect(classes.filter(cls => /:border(?:-[xytrbl])?-(?:\d+|\[[^\]]+\])$/.test(cls)), name).toEqual([]);
}

it("입력·선택·체크·스위치·아코디언·스크롤 영역·배지 포커스는 Button과 같은 outline 하나다", () => {
  const { container } = render(
    <div>
      <Input aria-label="입력" />
      <Textarea aria-label="여러 줄" />
      <NativeSelect aria-label="기본 선택"><NativeSelectOption value="a">가</NativeSelectOption></NativeSelect>
      <Select><SelectTrigger aria-label="선택"><SelectValue placeholder="고르기" /></SelectTrigger></Select>
      <Checkbox aria-label="체크" />
      <Switch aria-label="스위치" />
      <Accordion type="single" collapsible><AccordionItem value="a"><AccordionTrigger>항목</AccordionTrigger></AccordionItem></Accordion>
      <ScrollArea><p>본문</p></ScrollArea>
      <Badge asChild><a href="#x">배지 링크</a></Badge>
    </div>,
  );
  for (const slot of ["input", "textarea", "native-select", "select-trigger", "checkbox", "switch", "accordion-trigger", "scroll-area-viewport", "badge"]) {
    expectSingleOutline(slot, container.querySelector(`[data-slot="${slot}"]`));
  }
});

it("선택 카드 FieldLabel은 내부 컨트롤 포커스 때 두 번째 ring·테두리를 그리지 않는다", () => {
  const { container } = render(
    <FieldLabel>
      <Field orientation="horizontal"><Checkbox aria-label="카드 선택" /></Field>
    </FieldLabel>,
  );
  const label = classesOf(container.querySelector('[data-slot="field-label"]'));
  expect(label.filter(cls => /focus-visible/.test(cls))).toEqual([]);
  expectSingleOutline("card checkbox", container.querySelector('[data-slot="checkbox"]'));
});

it("체크박스·스위치는 md 미만에서 after 터치 영역을 44px 이상으로 넓히고 데스크톱 밀도는 유지한다", () => {
  const { container } = render(<div><Checkbox aria-label="체크" /><Switch aria-label="스위치" /></div>);
  const checkbox = classesOf(container.querySelector('[data-slot="checkbox"]'));
  // 16px + 2×14px = 44px
  expect(checkbox).toEqual(expect.arrayContaining(["size-4", "after:-inset-x-3", "after:-inset-y-2", "max-md:after:-inset-x-3.5", "max-md:after:-inset-y-3.5"]));
  const toggle = classesOf(container.querySelector('[data-slot="switch"]'));
  // 기본 18.4px + 2×14px ≥ 44px, 폭은 32px + 2×12px = 56px
  expect(toggle).toEqual(expect.arrayContaining(["after:-inset-x-3", "after:-inset-y-2", "max-md:after:-inset-y-3.5"]));
});
