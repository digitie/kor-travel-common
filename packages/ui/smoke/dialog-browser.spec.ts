// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
import { expect, test, type Locator, type Page } from "@playwright/test";

async function expectContainedScroll(page: Page, content: Locator) {
  await expect(content).toHaveCSS("position", "fixed");
  const bounds = await content.boundingBox();
  const viewport = page.viewportSize()!;
  console.log(JSON.stringify({ viewport, bounds, metrics: await content.evaluate(element => ({
    scrollHeight: element.scrollHeight, clientHeight: element.clientHeight,
    overflowY: getComputedStyle(element).overflowY,
  })) }));
  expect(bounds!.y).toBeGreaterThanOrEqual(8);
  expect(bounds!.y + bounds!.height).toBeLessThanOrEqual(viewport.height - 8);
  expect(bounds!.x).toBeGreaterThanOrEqual(8);
  expect(bounds!.x + bounds!.width).toBeLessThanOrEqual(viewport.width - 8);
  await expect(content).toHaveCSS("overflow-y", "auto");
  expect(await content.evaluate(element => element.scrollHeight > element.clientHeight)).toBe(true);
}

for (const viewport of [{ width: 320, height: 568 }, { width: 375, height: 667 }, { width: 667, height: 375 }, { width: 1280, height: 720 }]) {
  test.describe(`${viewport.width}px 긴 폼`, () => {
    test.use({ viewport });
    test("Dialog의 내부 스크롤·저장·상단 닫기·포커스 복원", async ({ page }) => {
      const errors: string[] = [];
      page.on("pageerror", error => errors.push(error.message));
      await page.goto("/dialog-contracts");
      const trigger = page.getByRole("button", { name: "긴 양식 열기", exact: true });
      await trigger.click();
      const content = page.getByRole("dialog", { name: "긴 양식", exact: true });
      await expectContainedScroll(page, content);
      await expect(page.locator('[data-slot="dialog-overlay"]')).toHaveCount(1);
      await content.getByRole("textbox", { name: "항목 24", exact: true }).fill("마지막 값");
      await content.getByRole("button", { name: "양식 저장" }).click();
      await expect(page.getByTestId("saved")).toHaveText("1");
      expect(await content.evaluate(element => element.scrollTop)).toBeGreaterThan(0);
      expect(await page.evaluate(() => window.scrollY)).toBe(0);
      await content.getByRole("button", { name: "닫기", exact: true }).click();
      await expect(content).toBeHidden();
      await expect(trigger).toBeFocused();
      await trigger.click();
      await page.keyboard.press("Escape");
      await expect(trigger).toBeFocused();
      expect(errors).toEqual([]);
    });
    test("AlertDialog의 긴 내용·승인·취소·포커스 복원", async ({ page }) => {
      await page.goto("/dialog-contracts");
      const trigger = page.getByRole("button", { name: "긴 확인 열기", exact: true });
      await trigger.click();
      const content = page.getByRole("alertdialog", { name: "긴 확인", exact: true });
      await expectContainedScroll(page, content);
      await content.getByRole("button", { name: "작업 승인", exact: true }).click();
      await expect(page.getByTestId("confirmed")).toHaveText("1");
      await expect(trigger).toBeFocused();
      await trigger.click();
      await content.getByRole("button", { name: "확인 취소", exact: true }).click();
      await expect(content).toBeHidden();
      await expect(trigger).toBeFocused();
    });
    test("중첩 포털의 스크롤·초점 trap·부모 입력 복원", async ({ page }) => {
      await page.goto("/dialog-contracts");
      const trigger = page.getByRole("button", { name: "긴 양식 열기", exact: true });
      await trigger.click();
      const parent = page.getByTestId("long-dialog");
      await parent.getByRole("textbox", { name: "항목 1", exact: true }).fill("보존값");
      const nestedTrigger = parent.getByRole("button", { name: "중첩 확인 열기", exact: true });
      await nestedTrigger.click();
      const nested = page.getByRole("alertdialog", { name: "중첩 확인", exact: true });
      await expectContainedScroll(page, nested);
      expect(await nested.evaluate(element => element.parentElement === document.body)).toBe(true);
      await expect(page.locator('[data-slot="dialog-overlay"]')).toHaveCount(1);
      await expect(page.locator('[data-slot="alert-dialog-overlay"]')).toHaveCount(1);
      await page.keyboard.press("Tab");
      expect(await nested.evaluate(element => element.contains(document.activeElement))).toBe(true);
      await nested.getByRole("button", { name: "중첩 확인 취소", exact: true }).click();
      await expect(nested).toBeHidden();
      await expect(nestedTrigger).toBeFocused();
      await expect(parent.getByRole("textbox", { name: "항목 1", exact: true })).toHaveValue("보존값");
      await page.keyboard.press("Escape");
      await expect(trigger).toBeFocused();
    });
    test("unstyled sheet·중앙 확인 폭과 overlay 취소 정책을 보존한다", async ({ page }) => {
      await page.goto("/dialog-contracts");
      const sheetTrigger = page.getByRole("button", { name: "표현 전용 양식 열기", exact: true });
      await sheetTrigger.click();
      const sheet = page.getByRole("dialog", { name: "표현 전용 양식", exact: true });
      await expect(page.getByTestId("custom-sheet-overlay")).toHaveCount(1);
      await expect(page.getByTestId("custom-sheet-overlay")).toHaveCSS("backdrop-filter", "none");
      await expect.poll(async () => (await sheet.boundingBox())!.height).toBeLessThanOrEqual(viewport.height * 0.88 + 1);
      const box = (await sheet.boundingBox())!;
      if (viewport.width >= 640) expect(box.width).toBe(512);
      else {
        expect(box.x).toBe(0);
        expect(box.width).toBe(viewport.width);
        expect(box.y + box.height).toBe(viewport.height);
      }
      const footer = sheet.getByRole("button", { name: "표현 전용 닫기", exact: true });
      const footerBefore = (await footer.boundingBox())!.y;
      await sheet.getByRole("textbox", { name: "항목 24", exact: true }).fill("끝");
      expect(await page.getByTestId("custom-sheet-body").evaluate(element => element.scrollTop)).toBeGreaterThan(0);
      expect((await footer.boundingBox())!.y).toBe(footerBefore);
      await footer.click();
      await expect(sheetTrigger).toBeFocused();

      const confirmTrigger = page.getByRole("button", { name: "표현 전용 확인 열기", exact: true });
      await confirmTrigger.click();
      const confirm = page.getByRole("alertdialog", { name: "표현 전용 확인", exact: true });
      await expect.poll(async () => (await confirm.boundingBox())!.width).toBe(Math.min(448, viewport.width - 32));
      await confirm.getByRole("checkbox", { name: "작업 진행 중" }).check();
      const overlay = page.getByTestId("custom-confirm-overlay");
      await overlay.click({ position: { x: 2, y: 2 } });
      await expect(confirm).toBeVisible();
      await page.keyboard.press("Escape");
      await expect(confirm).toBeVisible();
      await confirm.getByRole("checkbox", { name: "작업 진행 중" }).uncheck();
      await overlay.click({ position: { x: 2, y: 2 } });
      await expect(confirm).toBeHidden();
      await expect(confirmTrigger).toBeFocused();
    });
  });
}


const sizeLimits = { sm: 320, md: 384, lg: 768, xl: 1024, "2xl": 1280, full: Infinity } as const;
for (const width of [375, 500, 640, 700, 1280, 1600]) {
  test.describe(`${width}px 크기 계약`, () => {
    test.use({ viewport: { width, height: 667 } });
    for (const size of ["full", "sm", "md", "lg", "xl", "2xl"] as const) {
      test(`${size}의 실제 폭·여백·긴 내용 스크롤`, async ({ page }) => {
        await page.goto("/dialog-contracts");
        await page.getByRole("combobox", { name: "대화상자 크기" }).selectOption(size);
        const trigger = page.getByRole("button", { name: "크기 창 열기", exact: true });
        await trigger.click();
        const dialog = page.getByRole("dialog", { name: "크기 계약", exact: true });
        const expectedWidth = Math.min(width - 32, sizeLimits[size]);
        await expect.poll(async () => (await dialog.boundingBox())!.width).toBe(expectedWidth);
        await expectContainedScroll(page, dialog);
        await dialog.getByRole("textbox", { name: "항목 24", exact: true }).fill(size);
        await dialog.getByRole("button", { name: "크기 창 닫기", exact: true }).click();
        await expect(trigger).toBeFocused();
      });
    }
    test("소비자 max-w-3xl가 기본 md 최대 폭을 덮어쓴다", async ({ page }) => {
      await page.goto("/dialog-contracts");
      await page.getByRole("checkbox", { name: "기본 폭 재정의", exact: true }).check();
      await page.getByRole("button", { name: "크기 창 열기", exact: true }).click();
      const dialog = page.getByRole("dialog", { name: "크기 계약", exact: true });
      await expect.poll(async () => (await dialog.boundingBox())!.width).toBe(Math.min(width - 32, 768));
      await expectContainedScroll(page, dialog);
    });
    test("소비자 sm:max-w-md가 크기 기본값을 덮어쓴다", async ({ page }) => {
      await page.goto("/dialog-contracts");
      await page.getByRole("combobox", { name: "대화상자 크기" }).selectOption("lg");
      await page.getByRole("checkbox", { name: "폭 재정의", exact: true }).check();
      await page.getByRole("button", { name: "크기 창 열기", exact: true }).click();
      const dialog = page.getByRole("dialog", { name: "크기 계약", exact: true });
      await expect.poll(async () => (await dialog.boundingBox())!.width).toBe(Math.min(width - 32, width < 640 ? 768 : 448));
      await expectContainedScroll(page, dialog);
    });
  });
}
