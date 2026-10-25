// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
// 실제 재현 문구의 clip ancestor를 검사하고 물리적 부족은 통과로 집계하지 않는다.
import assert from "node:assert/strict";
import { pathToFileURL } from "node:url";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULE ? pathToFileURL(process.env.PLAYWRIGHT_MODULE).href : "playwright");
const origin = process.argv[2];
assert.ok(origin, "설치 smoke 서버 URL이 필요합니다");
const browser = await chromium.launch({ headless: true });
try {
  for (const [width, height, target, font] of [[320, 568, 339, 100], [812, 375, 203, 100], [320, 568, 175, 200]]) {
    const page = await browser.newPage({ viewport: { width, height }, hasTouch: true });
    await page.goto(`${origin}/map-workspace/content`);
    await page.evaluate(({ height, target, font }) => {
      document.documentElement.style.fontSize = `${font}%`;
      document.getElementById("content-shell-header").style.flexBasis = `${height - 16 - target}px`;
    }, { height, target, font });
    for (const selected of [false, true]) {
      if (selected) await page.getByRole("button", { name: "선택 상세 전환" }).click();
      const result = await page.evaluate(() => {
        function visible(element) {
          if (!element) return false;
          const rect = element.getBoundingClientRect();
          if (!rect.width || !rect.height) return false;
          let top = 0, bottom = innerHeight, left = 0, right = innerWidth;
          for (let parent = element.parentElement; parent; parent = parent.parentElement) {
            const style = getComputedStyle(parent);
            const bounds = parent.getBoundingClientRect();
            if (/auto|hidden|scroll|clip/.test(style.overflowY)) {
              top = Math.max(top, bounds.top + parent.clientTop);
              bottom = Math.min(bottom, bounds.top + parent.clientTop + parent.clientHeight);
            }
            if (/auto|hidden|scroll|clip/.test(style.overflowX)) {
              left = Math.max(left, bounds.left + parent.clientLeft);
              right = Math.min(right, bounds.left + parent.clientLeft + parent.clientWidth);
            }
          }
          return rect.top >= top - 1 && rect.bottom <= bottom + 1 && rect.left >= left - 1 && rect.right <= right + 1;
        }
        const stage = document.querySelector('[data-slot="map-stage"]').getBoundingClientRect();
        const summary = document.querySelector('[data-slot="map-stage-summary"]').getBoundingClientRect();
        const essential = Object.fromEntries([...document.querySelectorAll("[data-essential]")].map((element) => [element.dataset.essential, visible(element)]));
        const close = document.querySelector('[aria-label="상세 닫기"]');
        const collapse = document.querySelector('[aria-label="상세 접기"]');
        return {
          stage: { y: stage.y, height: stage.height }, summary: { y: summary.y, height: summary.height }, essential,
          closeVisible: close ? visible(close) : null, collapseVisible: collapse ? visible(collapse) : null,
          closeRect: close ? { y: close.getBoundingClientRect().y, height: close.getBoundingClientRect().height } : null,
          overflow: document.documentElement.scrollWidth > innerWidth,
        };
      });
      console.log(JSON.stringify({ width, height, font, selected, essentialStatus: Object.values(result.essential).every(Boolean) ? "FULL" : "LIMITED_NOT_PASS", ...result }));
      if (font === 100 && target === 339) assert.ok(Object.values(result.essential).every(Boolean), "320px 기본 작업면 필수 정보 가림");
      if (selected) assert.ok(result.closeVisible && result.collapseVisible, "상세 닫기·접기 가림");
    }
    await page.close();
  }
} finally {
  await browser.close();
}
