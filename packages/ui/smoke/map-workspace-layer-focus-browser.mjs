// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
// 공개 마크업의 레이어 hit-test와 양방향 반응형 초점을 검증한다. SDK 검증은 별도다.
import assert from "node:assert/strict";
import { pathToFileURL } from "node:url";
const runtime = await import(process.env.PLAYWRIGHT_MODULE ? pathToFileURL(process.env.PLAYWRIGHT_MODULE).href : "playwright");
const origin = process.argv[2];
assert.ok(origin, "설치 smoke 서버 URL이 필요합니다");
for (const name of ["chromium", "firefox"]) {
  const browser = await runtime[name].launch({ headless: true });
  try {
    const page = await browser.newPage({ viewport: { width: 375, height: 812 }, hasTouch: true });
    await page.goto(`${origin}/map-workspace`);
    await page.waitForLoadState("networkidle");
    await page.getByRole("button", { name: "지도 크게 보기", exact: true }).click();
    await page.getByRole("button", { name: "원래 화면으로", exact: true }).click();
    const hit = await page.evaluate(() => {
      const canvas = document.querySelector('[data-slot="map-stage-canvas"]');
      const marker = document.createElement("button"); marker.textContent = "겹친 마커"; marker.dataset.qaMarker = "true";
      Object.assign(marker.style, { position: "absolute", zIndex: "3", top: "8px", left: "8px", width: "250px", height: "44px" });
      canvas.firstElementChild.append(marker);
      const bounds = document.querySelector('[data-slot="map-stage-summary"]').getBoundingClientRect();
      const target = document.elementFromPoint(bounds.left + 10, bounds.top + 10);
      return { summaryWins: !!target?.closest('[data-slot="map-stage-summary"]'), markerWins: !!target?.closest("[data-qa-marker]") };
    });
    assert.equal(hit.summaryWins, true, "마커 z-index가 요약 위로 탈출하지 않음");
    assert.equal(hit.markerWins, false);
    const attributionHit = await page.getByText("지도 출처", { exact: true }).evaluate((element) => {
      const bounds = element.getBoundingClientRect();
      const target = document.elementFromPoint(bounds.left + bounds.width / 2, bounds.top + bounds.height / 2);
      return target === element || element.contains(target);
    });
    assert.ok(attributionHit, "출처 표시를 overlay가 덮지 않음");
    await page.getByRole("button", { name: "확대", exact: true }).click();
    await page.waitForFunction(() => document.activeElement?.getAttribute("data-slot") === "map-detail-overlay");
    await page.keyboard.press("Escape");
    assert.equal(await page.locator('[data-slot="map-detail-overlay"]').count(), 0, "키보드 상세 닫기 보존");
    const trigger = page.locator('[data-slot="map-filter-trigger"]');
    await trigger.focus();
    await page.setViewportSize({ width: 1440, height: 900 });
    await page.waitForFunction(() => !!document.activeElement?.closest('[data-slot="map-filter-panel-body"]'));
    assert.equal(await page.evaluate(() => document.activeElement.getClientRects().length > 0), true);
    await page.locator('[data-slot="map-filter-panel-body"]').evaluate((element) => {
      const input = document.createElement("input"); input.type = "search"; element.append(input); input.focus();
    });
    await page.setViewportSize({ width: 375, height: 812 });
    await page.waitForFunction(() => document.activeElement?.getAttribute("data-slot") === "map-filter-trigger");
    await page.locator("h1").click();
    await page.setViewportSize({ width: 1440, height: 900 });
    assert.equal(await page.evaluate(() => !!document.activeElement?.closest('[data-slot="map-filter-panel-body"]')), false, "외부 pointer 뒤 초점을 훔치지 않음");
    console.log(JSON.stringify({ browser: name, ...hit, attributionHit, zoomAndKeyboard: true, responsiveBothWays: true, outsidePointerPreserved: true, passed: true }));
    await page.close();
  } finally {
    await browser.close();
  }
}
