// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
// 엔진 없는 설치 fixture에서 확장·초점·200% 조작기 계약을 검증한다.
import assert from "node:assert/strict";
import { pathToFileURL } from "node:url";
const runtime = await import(process.env.PLAYWRIGHT_MODULE ? pathToFileURL(process.env.PLAYWRIGHT_MODULE).href : "playwright");
const origin = process.argv[2];
assert.ok(origin, "설치 smoke 서버 URL이 필요합니다");

for (const name of ["chromium", "firefox"]) {
  const browser = await runtime[name].launch({ headless: true });
  try {
    for (const [width, height, font] of [[375, 812, 100], [320, 568, 200], [812, 375, 100]]) {
      const page = await browser.newPage({ viewport: { width, height }, hasTouch: true });
      await page.goto(`${origin}/map-workspace`);
      await page.getByRole("combobox", { name: "데이터 출처" }).selectOption("키 없음");
      await page.waitForFunction(() => document.querySelector('[data-slot="map-stage-canvas"]')?.textContent?.includes("키 없음"));
      await page.evaluate((font) => { document.documentElement.style.fontSize = `${font}%`; }, font);
      await page.addStyleTag({ content: "button { height:2.25rem; min-height:2.25rem; }" });
      const workspace = page.locator('[data-slot="map-workspace"]');
      const expand = page.getByRole("button", { name: "지도 크게 보기", exact: true });
      const filter = page.locator('[data-slot="map-filter-trigger"]');
      const initial = await page.locator('[data-slot="map-stage"]:visible').boundingBox();
      await page.locator('[data-slot="map-stage"]:visible').evaluate((element) => { window.initialStage = element; });
      await expand.click();
      await workspace.getAttribute("data-expanded").then((value) => assert.equal(value, "true"));
      assert.equal(await page.evaluate(() => window.initialStage === document.querySelector('[data-slot="map-stage"]')), true, "확장 때 canvas DOM 보존");
      const expanded = await page.locator('[data-slot="map-stage"]:visible').boundingBox();
      assert.ok(expanded.height > initial.height, "route CSS로 같은 작업면에 남은 높이 전달");
      const back = page.getByRole("button", { name: "원래 화면으로", exact: true });
      const backBox = await back.boundingBox();
      const closeBox = await page.getByRole("button", { name: "상세 닫기" }).boundingBox();
      assert.equal(backBox.height, 44);
      assert.equal(closeBox.height, 44);
      assert.equal(backBox.width, 44);
      assert.ok(closeBox.y >= expanded.y && closeBox.y + closeBox.height <= expanded.y + expanded.height, "확장 후 닫기 viewport 접근");
      const tabsFit = await page.locator('[data-slot="tabs-list"]').evaluate((element) => {
        const bounds = element.getBoundingClientRect();
        return bounds.left >= 0 && bounds.right <= innerWidth && [...element.children].every((child) => child.getBoundingClientRect().right <= bounds.right + 1);
      });
      assert.ok(tabsFit, "글자200% 탭 가로 가림 없음");
      await page.locator('[data-slot="map-detail-overlay"]').evaluate((element) => element.focus());
      await page.keyboard.press("Escape");
      assert.equal(await workspace.getAttribute("data-expanded"), "true", "첫 Escape는 상세만 닫음");
      await filter.focus();
      await page.keyboard.press("Escape");
      assert.equal(await workspace.getAttribute("data-expanded"), "false");
      assert.equal(await expand.evaluate((element) => element === document.activeElement), true);
      await expand.click();
      await page.setViewportSize({ width: 1440, height: 900 });
      assert.equal(await back.isVisible(), true, "넓은 화면에서도 복귀 버튼 표시");
      await back.click();
      assert.equal(await page.evaluate(() => document.activeElement !== document.body && document.activeElement.getClientRects().length > 0), true, "숨은 복귀 버튼 대신 보이는 탭으로 초점 이동");
      console.log(JSON.stringify({ browser: name, width, height, font, initial, expanded, tabsFit, iconHeight: closeBox.height, passed: true }));
      await page.close();
    }
    const page = await browser.newPage({ viewport: { width: 1440, height: 900 }, hasTouch: true });
    await page.goto(`${origin}/map-workspace`);
    await page.getByRole("combobox", { name: "데이터 출처" }).selectOption("키 없음");
    await page.waitForFunction(() => document.querySelector('[data-slot="map-stage-canvas"]')?.textContent?.includes("키 없음"));
    await page.locator('[data-slot="map-filter-panel-body"]').evaluate((element) => {
      const input = document.createElement("input"); input.type = "search"; input.setAttribute("aria-label", "반응형 검사"); element.append(input); input.focus();
    });
    await page.setViewportSize({ width: 375, height: 812 });
    await page.waitForFunction(() => document.activeElement?.getAttribute("data-slot") === "map-filter-trigger");
    await page.setViewportSize({ width: 1440, height: 900 });
    await page.getByRole("searchbox", { name: "반응형 검사" }).focus();
    await page.locator("h1").click();
    await page.setViewportSize({ width: 375, height: 812 });
    assert.equal(await page.locator('[data-slot="map-filter-trigger"]').evaluate((element) => element === document.activeElement), false, "외부 pointer 뒤 초점 복원 금지");
    console.log(JSON.stringify({ browser: name, responsiveFocus: true, outsidePointerPreserved: true }));
    await page.close();
  } finally {
    await browser.close();
  }
}
