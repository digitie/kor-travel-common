// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
import { test, expect } from "@playwright/test";
test("Radix 세로탭·상태 CSS·포커스가 격리 설치본에서 동작한다", async ({page})=>{
  const errors:string[]=[];
  page.on("pageerror",error=>errors.push(error.message));
  await page.goto("/radix-contracts");
  await expect(page.getByRole("tabpanel")).toHaveCount(1);
  await expect(page.getByRole("tablist")).toHaveAttribute("aria-orientation","vertical");
  await page.getByRole("tab",{name:"첫 탭"}).focus();
  await page.keyboard.press("ArrowDown");
  await expect(page.getByRole("tab",{name:"둘째 탭"})).toHaveAttribute("aria-selected","true");
  await page.keyboard.press("Tab");
  const panel=page.getByRole("tabpanel",{name:"둘째 탭"});
  await expect(panel).toBeFocused();
  await expect(panel).toHaveCSS("outline-style","solid");
  await expect(panel).toHaveCSS("outline-width","2px");
  const toggle=page.getByRole("switch",{name:"사용 상태"});
  const colors=await toggle.evaluate(el=>{
    const probe=document.createElement("i"); probe.style.backgroundColor="var(--kt-brand)";
    document.body.append(probe);
    const result={actual:getComputedStyle(el).backgroundColor,expected:getComputedStyle(probe).backgroundColor};
    probe.remove();return result;
  });
  expect(colors.actual).toBe(colors.expected);
  await toggle.click();
  await expect(toggle).toHaveAttribute("aria-checked","false");
  await expect(toggle).not.toHaveCSS("background-color",colors.actual);
  await expect(page.getByRole("checkbox",{name:"작업 선택"})).toBeChecked();
  const trigger=page.getByRole("button",{name:"상세 열기"});
  await trigger.click();
  await expect(page.getByRole("dialog",{name:"작업 상세"})).toBeVisible();
  await page.keyboard.press("Escape");
  await expect(page.getByRole("dialog")).toBeHidden();
  await expect(trigger).toBeFocused();
  expect(errors).toEqual([]);
});
