// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
import { expect, test } from "@playwright/test";

for (const viewport of [{ width: 320, height: 568 }, { width: 390, height: 844 }]) {
  test.describe(`${viewport.width}px 모바일 셸`, () => {
    test.use({ viewport });
    test("한 줄 상단 바와 좌측 drawer·이동 시 닫힘", async ({ page }) => {
      const errors: string[] = [];
      page.on("pageerror", error => errors.push(error.message));
      await page.goto("/admin-shell-contracts");
      const header = page.locator('[data-slot="admin-shell-header"]');
      const heading = page.getByRole("heading", { level: 1 });
      await expect(heading).toHaveText("검증 - 개요");
      // 메뉴·제목이 세로 공간을 차지하지 않는다: 상단 바 한 줄, rail 숨김, 본문은 바로 아래.
      const headerBox = (await header.boundingBox())!;
      expect(headerBox.height).toBeLessThanOrEqual(56);
      await expect(page.locator('[data-slot="admin-shell-rail"]')).toBeHidden();
      const mainBox = (await page.getByRole("main").boundingBox())!;
      expect(mainBox.y).toBeLessThanOrEqual(headerBox.y + headerBox.height + 1);
      const description = page.locator('[data-slot="admin-shell-description"]');
      await expect(description).toHaveAttribute("title", /활성 위치 카탈로그 12곳/);
      await expect(description).toHaveCSS("text-overflow", "ellipsis");
      expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth)).toBe(true);

      const trigger = page.getByRole("button", { name: "메뉴 열기" });
      await expect(trigger).toBeVisible();
      await expect(trigger).toHaveAttribute("aria-expanded", "false");
      await trigger.click();
      const drawer = page.getByRole("dialog", { name: "메뉴" });
      await expect(drawer).toBeVisible();
      await expect(trigger).toHaveAttribute("aria-expanded", "true");
      await expect.poll(async () => (await drawer.boundingBox())?.x).toBe(0);
      const drawerBox = (await drawer.boundingBox())!;
      expect(drawerBox.width).toBeLessThanOrEqual(Math.min(280, viewport.width * 0.84) + 1);
      // focus trap: Tab을 반복해도 drawer 밖으로 나가지 않는다.
      for (let index = 0; index < 6; index += 1) {
        await page.keyboard.press("Tab");
        expect(await drawer.evaluate(element => element.contains(document.activeElement))).toBe(true);
      }
      await page.keyboard.press("Escape");
      await expect(drawer).toBeHidden();
      await expect(trigger).toBeFocused();

      await trigger.click();
      await page.getByRole("dialog", { name: "메뉴" }).getByRole("link", { name: "작업" }).click();
      await expect(page).toHaveURL(/\/admin-shell-contracts\/jobs$/);
      await expect(page.getByRole("dialog")).toBeHidden();
      await expect(page.getByRole("main")).toBeFocused();
      await expect(heading).toHaveText("검증 - 작업");
      await expect(description).toHaveText("실행 중 3건");
      await expect(page.getByRole("button", { name: "새로고침" })).toBeVisible();
      expect(errors).toEqual([]);
    });
  });
}

test.describe("1280px 데스크톱 셸", () => {
  test.use({ viewport: { width: 1280, height: 720 } });
  test("좌측 rail을 아이콘으로 접고 새로고침 후에도 유지한다", async ({ page }) => {
    const errors: string[] = [];
    page.on("pageerror", error => errors.push(error.message));
    await page.goto("/admin-shell-contracts");
    await expect(page.getByRole("button", { name: "메뉴 열기" })).toBeHidden();
    const rail = page.locator('[data-slot="admin-shell-rail"]');
    await expect(rail).toBeVisible();
    expect((await rail.boundingBox())!.width).toBe(256);
    const header = page.locator('[data-slot="admin-shell-header"]');
    expect((await header.boundingBox())!.height).toBeLessThanOrEqual(56);
    await page.getByRole("button", { name: "메뉴 접기" }).click();
    await expect(rail).toHaveAttribute("data-collapsed", "true");
    expect((await rail.boundingBox())!.width).toBe(64);
    await expect(rail.getByRole("link", { name: "작업" })).toHaveAttribute("title", "작업");
    await page.reload();
    await expect(rail).toHaveAttribute("data-collapsed", "true");
    await rail.getByRole("link", { name: "작업" }).click();
    await expect(page.getByRole("heading", { level: 1 })).toHaveText("검증 - 작업");
    await expect(rail.getByRole("link", { name: "작업" })).toHaveAttribute("aria-current", "page");
    expect(errors).toEqual([]);
  });
});
