// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
// 설치된 smoke 서버와 별도로 제공한 Playwright 런타임에서만 실행한다.
import assert from "node:assert/strict";
import { mkdir } from "node:fs/promises";
import { pathToFileURL } from "node:url";

const { chromium } = await import(process.env.PLAYWRIGHT_MODULE ? pathToFileURL(process.env.PLAYWRIGHT_MODULE).href : "playwright");
const origin = process.argv[2];
assert.ok(origin, "검증할 smoke 서버 URL이 필요합니다");
const browser = await chromium.launch({ headless: true });
try {
  for (const [width, height, hasTouch] of [[1440, 900, false], [375, 812, true], [320, 568, true], [812, 375, true]]) {
    const context = await browser.newContext({ viewport: { width, height }, hasTouch });
    const page = await context.newPage();
    const errors = [];
    page.on("pageerror", (error) => errors.push(error.message));
    await page.goto(`${origin}/map-workspace`);
    const stage = page.locator('[data-slot="map-stage"]:visible');
    await stage.waitFor();
    const initial = await stage.boundingBox();
    if (process.env.EVIDENCE_DIR) {
      await mkdir(process.env.EVIDENCE_DIR, { recursive: true });
      await page.screenshot({ path: `${process.env.EVIDENCE_DIR}/workspace-initial-${width}-${height}.png` });
    }
    assert.ok(initial.height > 150 && initial.y + initial.height <= height + 1, "남은 높이 작업면 경계");
    assert.equal(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth || document.documentElement.scrollHeight > innerHeight + 1), false, "문서 이중 스크롤/넘침");
    const summary = page.locator('[data-slot="map-stage-summary"]:visible');
    const detail = page.locator('[data-slot="map-detail-overlay"]:visible');
    const summaryBox = await summary.boundingBox();
    assert.equal(await summary.evaluate((element) => element.scrollHeight <= element.clientHeight + 1), true, "짧은 필수 안내는 상세 때문에 축소되지 않음");
    const detailBox = await detail.boundingBox();
    assert.ok(summaryBox.y + summaryBox.height <= detailBox.y, "요약과 상세 겹침");
    const close = page.getByRole("button", { name: "상세 닫기" });
    const closeBox = await close.boundingBox();
    assert.ok(closeBox.y >= initial.y && closeBox.y + closeBox.height <= initial.y + initial.height, "짧은 화면 닫기 접근");
    if (hasTouch) assert.ok(closeBox.width >= 44 && closeBox.height >= 44, "상세 coarse 44px");
    assert.equal(await page.locator('[data-slot="map-detail-body"]:visible').evaluate((element) => element.scrollHeight > element.clientHeight), true, "상세 본문만 스크롤");
    const filter = page.getByRole("button", { name: "지도 필터" });
    if (width <= 640) {
      assert.equal(await filter.getAttribute("aria-expanded"), "false");
      await filter.click();
    }
    const select = page.getByRole("combobox", { name: "데이터 출처" });
    const selectBox = await select.boundingBox();
    assert.equal(Math.round(selectBox.height), hasTouch ? 44 : 30);
    if (!hasTouch) assert.equal(Math.round(selectBox.width), 176);
    const expandedStage = await stage.boundingBox();
    for (const value of ["키 없음", "WebGL 불가", "조회 중", "자료 없음"]) {
      await select.selectOption(value);
      assert.equal(Math.round((await stage.boundingBox()).height), Math.round(expandedStage.height), "상태별 작업면 높이 보존");
    }
    if (width <= 640) await filter.click();
    await page.getByRole("button", { name: "상세 접기" }).click();
    assert.equal(await page.locator('[data-slot="map-detail-body"]:visible').count(), 0);
    await page.getByRole("button", { name: "상세 펼치기" }).click();
    await page.getByRole("button", { name: "확대", exact: true }).click();
    await detail.evaluate((element) => element.focus());
    await page.keyboard.press("Escape");
    assert.equal(await detail.count(), 0);
    if (width <= 640) assert.equal(await filter.evaluate((element) => element === document.activeElement), true);
    await page.getByRole("tab", { name: "목록", exact: true }).click();
    const list = page.locator('[data-slot="map-stage-list"]');
    assert.equal(await list.evaluate((element) => element.scrollHeight > element.clientHeight && getComputedStyle(element).overflowY === "auto"), true);
    const legacy = await page.evaluate(() => {
      const wrapper = document.createElement("div");
      wrapper.innerHTML = '<div class="kt-map-detail"></div><div class="kt-map-filter-field"><select><option>기존 선택</option></select></div>';
      document.body.append(wrapper);
      const detail = getComputedStyle(wrapper.firstElementChild);
      const select = wrapper.querySelector("select").getBoundingClientRect();
      const result = { position: detail.position, top: detail.top, bottom: detail.bottom, controlHeight: select.height };
      wrapper.remove();
      return result;
    });
    assert.deepEqual(legacy, { position: "absolute", top: "80px", bottom: "96px", controlHeight: 30 }, "dev.7 기본 스타일 보존");
    assert.deepEqual(errors, []);
    if (process.env.EVIDENCE_DIR) {
      await mkdir(process.env.EVIDENCE_DIR, { recursive: true });
      await page.screenshot({ path: `${process.env.EVIDENCE_DIR}/workspace-${width}-${height}.png` });
    }
    console.log(JSON.stringify({ width, height, hasTouch, stage: initial, select: selectBox, legacy, errors: errors.length, passed: true }));
    await context.close();
  }
} finally {
  await browser.close();
}
