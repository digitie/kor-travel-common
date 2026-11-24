// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
import { expect, test, type Locator, type Page } from "@playwright/test";

// ui 0.2.7: Dialog·AlertDialog 본문의 넓은 표(가상 표 600px·일반 표 약 1000px)가 좁은 화면에서 모달 grid 칸을 넓혀
// 머리글·본문이 가로로 넘치지 않고, 표 컨테이너가 자체 가로 스크롤을 맡는지 실제 기하로 잰다.
// 옛 암시적 auto 칸에서는 세 폭 모두에서 칸이 표 min-content만큼 넓어져 실패한다(1440 안쪽 736px < 일반 표).

const MOBILE_MAX = 767;

async function settle(page: Page) {
  await page.evaluate(() => new Promise<void>((resolve) => {
    // 열림 애니메이션이 끝나기를 기다리되, 무한 애니메이션이 있어도 2초 뒤에는 잰다.
    const deadline = performance.now() + 2000;
    const wait = () => document.getAnimations().every((animation) => animation.playState !== "running")
      || performance.now() > deadline
      ? requestAnimationFrame(() => requestAnimationFrame(() => resolve()))
      : setTimeout(wait, 20);
    wait();
  }));
}

type Edge = { left: number; right: number };
type Scroller = Edge & { label: string | null; clientWidth: number; scrollWidth: number; scrolledTo: number };
type Geometry = {
  box: Edge; inner: Edge; clientWidth: number; scrollWidth: number; gridTemplateColumns: string;
  children: (Edge & { slot: string | null; position: string })[]; title: Edge; scrollers: Scroller[];
};

async function measure(content: Locator): Promise<Geometry> {
  return content.evaluate((element) => {
    const edge = (rect: DOMRect) => ({ left: rect.left, right: rect.right });
    const style = getComputedStyle(element);
    const box = element.getBoundingClientRect();
    const inner = {
      left: box.left + parseFloat(style.borderLeftWidth) + parseFloat(style.paddingLeft),
      right: box.right - parseFloat(style.borderRightWidth) - parseFloat(style.paddingRight),
    };
    const children = Array.from(element.children).map((child) => ({
      ...edge(child.getBoundingClientRect()),
      slot: child.getAttribute("data-slot"),
      position: getComputedStyle(child).position,
    }));
    const title = element.querySelector('[data-slot="dialog-title"],[data-slot="alert-dialog-title"]')!;
    const scrollers = Array.from(element.querySelectorAll<HTMLElement>('[data-slot="table-container"]')).map((container) => {
      // 실제로 가로 스크롤되는지: 끝까지 밀어 본 위치를 기록하고 되돌린다.
      container.scrollLeft = 1e6;
      const scrolledTo = container.scrollLeft;
      container.scrollLeft = 0;
      return {
        ...edge(container.getBoundingClientRect()), label: container.getAttribute("aria-label"),
        clientWidth: container.clientWidth, scrollWidth: container.scrollWidth, scrolledTo,
      };
    });
    return {
      box: edge(box), inner, clientWidth: element.clientWidth, scrollWidth: element.scrollWidth,
      gridTemplateColumns: style.gridTemplateColumns, children, title: edge(title.getBoundingClientRect()), scrollers,
    };
  });
}

function expectContained(geometry: Geometry) {
  // 모달 자체는 가로로 넘치지 않는다(머리글·본문이 함께 밀리지 않는다).
  expect(geometry.scrollWidth).toBeLessThanOrEqual(geometry.clientWidth);
  // grid 칸 하나 = 모달 안쪽 폭.
  const track = parseFloat(geometry.gridTemplateColumns);
  expect(geometry.gridTemplateColumns.trim().split(/\s+/)).toHaveLength(1);
  expect(track).toBeLessThanOrEqual(geometry.inner.right - geometry.inner.left + 0.5);
  expect(geometry.title.right).toBeLessThanOrEqual(geometry.inner.right + 0.5);
  for (const child of geometry.children) {
    if (child.position === "absolute") continue; // 닫기 버튼(우상단 고정)
    // 바닥 행은 -mx-4로 모달 테두리까지 닿는다. 나머지는 안쪽 폭 안.
    const limit = /-footer$/.test(child.slot ?? "") ? geometry.box : geometry.inner;
    expect(child.left, JSON.stringify(child)).toBeGreaterThanOrEqual(limit.left - 0.5);
    expect(child.right, JSON.stringify(child)).toBeLessThanOrEqual(limit.right + 0.5);
  }
  for (const scroller of geometry.scrollers) {
    expect(scroller.left, JSON.stringify(scroller)).toBeGreaterThanOrEqual(geometry.inner.left - 0.5);
    expect(scroller.right, JSON.stringify(scroller)).toBeLessThanOrEqual(geometry.inner.right + 0.5);
    expect(scroller.clientWidth, JSON.stringify(scroller)).toBeLessThanOrEqual(geometry.inner.right - geometry.inner.left + 0.5);
  }
}

for (const viewport of [{ width: 320, height: 640 }, { width: 390, height: 844 }, { width: 1440, height: 900 }]) {
  test.describe(`${viewport.width}px 넓은 본문`, () => {
    test.use({ viewport });

    test("Dialog 안 넓은 표는 모달을 넓히지 않고 표 안에서 가로로 스크롤된다", async ({ page }) => {
      await page.goto("/dialog-overflow-contracts");
      await page.getByRole("button", { name: "넓은 표 상세 열기", exact: true }).click();
      const content = page.getByTestId("wide-detail-dialog");
      await expect(content).toBeVisible();
      await settle(page);
      const geometry = await measure(content);
      console.log(JSON.stringify({ viewport: viewport.width, dialog: "detail", geometry }));
      expectContained(geometry);
      // 모달은 화면 안(좌우 16px 여백, lg 최대 48rem)에 있다.
      expect(geometry.box.left).toBeGreaterThanOrEqual(16 - 0.5);
      expect(geometry.box.right).toBeLessThanOrEqual(viewport.width - 16 + 0.5);
      expect(geometry.scrollers).toHaveLength(2);
      const videos = geometry.scrollers.find((scroller) => scroller.label === "누적 수집 영상 표")!;
      if (viewport.width <= MOBILE_MAX) {
        // 표는 자기 컨테이너 안에서 가로로 스크롤된다.
        for (const scroller of geometry.scrollers) {
          expect(scroller.scrollWidth, JSON.stringify(scroller)).toBeGreaterThan(scroller.clientWidth);
          expect(scroller.scrolledTo, JSON.stringify(scroller)).toBeGreaterThan(0);
        }
      } else {
        // 데스크톱(안쪽 736px)에서 600px 가상 표는 스크롤 없이 들어간다.
        expect(videos.scrollWidth, JSON.stringify(videos)).toBeLessThanOrEqual(videos.clientWidth);
      }
      await content.getByRole("button", { name: "닫기", exact: true }).last().click();
      await expect(content).toBeHidden();
    });

    test("AlertDialog 안 넓은 표도 모달을 넓히지 않는다", async ({ page }) => {
      await page.goto("/dialog-overflow-contracts");
      await page.getByRole("button", { name: "넓은 표 확인 열기", exact: true }).click();
      const content = page.getByTestId("wide-alert-dialog");
      await expect(content).toBeVisible();
      await settle(page);
      const geometry = await measure(content);
      console.log(JSON.stringify({ viewport: viewport.width, dialog: "alert", geometry }));
      expectContained(geometry);
      expect(geometry.scrollers).toHaveLength(1);
      // 640 미만 max-w-xs(20rem)·이상 max-w-sm(24rem)이라 모든 폭에서 표가 컨테이너 안에서 스크롤된다.
      expect(geometry.scrollers[0].scrollWidth).toBeGreaterThan(geometry.scrollers[0].clientWidth);
      expect(geometry.scrollers[0].scrolledTo).toBeGreaterThan(0);
      await content.getByRole("button", { name: "확인 취소", exact: true }).click();
      await expect(content).toBeHidden();
    });
  });
}
