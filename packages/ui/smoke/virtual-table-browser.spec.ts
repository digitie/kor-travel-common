// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
import { test, expect } from "@playwright/test";

for (const width of [375, 1280]) {
  for (const virtualized of [false, true]) {
    test(`공통 표 ${width}px ${virtualized ? "가상" : "일반"}: grid 내부 가로 접근·폼·sticky header`, async ({ page }) => {
      const errors: string[] = [];
      page.on("pageerror", (error) => errors.push(error.message));
      await page.setViewportSize({ width, height: 900 });
      await page.goto("/virtual-table-contracts");
      if (virtualized) await page.getByRole("button", { name: "가상 표로 전환" }).click();
      const table = page.getByRole("table", { name: "공통 표 크기 계약" });
      const scroller = page.getByTestId("table-contract-scroller");
      await expect(table).toBeVisible();
      await page.evaluate(() => new Promise<void>((resolve) =>
        requestAnimationFrame(() => requestAnimationFrame(() => resolve()))));
      const bounds = await scroller.evaluate((element) => ({
        body: document.body.scrollWidth,
        main: document.querySelector("main")!.scrollWidth,
        viewport: innerWidth,
        client: element.clientWidth,
        scroll: element.scrollWidth,
        right: element.getBoundingClientRect().right,
      }));
      // 루트 overflow:clip이 숨기는 body/main의 실제 폭과 스크롤 범위를 검사한다.
      expect(bounds.body).toBeLessThanOrEqual(width);
      expect(bounds.main).toBeLessThanOrEqual(width);
      expect(bounds.right).toBeLessThanOrEqual(width);
      if (width === 375) {
        expect(bounds.scroll).toBeGreaterThan(bounds.client);
        const moved = await scroller.evaluate((element) => {
          const table = element.querySelector("table")!;
          const before = table.getBoundingClientRect().x;
          element.scrollLeft = 160;
          return { left: element.scrollLeft, delta: before - table.getBoundingClientRect().x };
        });
        expect(moved.left).toBeGreaterThan(0);
        expect(moved.delta).toBeGreaterThan(0);
      } else {
        expect(await table.evaluate((element) => element.getBoundingClientRect().width))
          .toBeGreaterThanOrEqual(bounds.client - 1);
      }
      await scroller.evaluate((element) => { element.scrollLeft = 0; element.scrollTop = 80; });
      await expect.poll(async () => table.locator("thead").evaluate((head) => {
        const scroller = head.closest('[data-slot="table-container"]')!;
        return Math.abs(head.getBoundingClientRect().top - scroller.getBoundingClientRect().top);
      })).toBeLessThanOrEqual(2);
      if (virtualized) expect(await table.getByRole("row").count()).toBeLessThan(81);
      await page.getByRole("textbox", { name: "표 검색" }).fill("_79");
      await expect(table.getByRole("row").filter({ hasText: "긴_테이블_이름_79" })).toHaveCount(1);
      await expect(page.getByRole("textbox", { name: "표 검색" })).toHaveValue("_79");
      expect(errors).toEqual([]);
    });
  }
}
