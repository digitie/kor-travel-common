// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
import { expect, test, type Locator, type Page } from "@playwright/test";

// ui 0.2.6: 선택 열 터치 영역이 이웃 행·칸과 겹치지 않고 md 미만에서 44px 이상인지, 아코디언 안쪽
// 포커스 outline이 잘리지 않는지, Dialog 긴 제목이 닫기 버튼과 겹치지 않는지를 실제 기하·픽셀로 잰다.

const MOBILE_MAX = 767;

async function settle(page: Page) {
  await page.evaluate(() => new Promise<void>((resolve) => {
    const wait = () => document.getAnimations().every((animation) => animation.playState !== "running")
      ? requestAnimationFrame(() => requestAnimationFrame(() => resolve()))
      : setTimeout(wait, 20);
    wait();
  }));
}

type HitArea = {
  minX: number; maxX: number; minY: number; maxY: number;
  cell: { left: number; right: number; top: number; bottom: number };
  row: { top: number; bottom: number };
  leftOfCentre21: boolean;
  /** 위 행·아래 행·왼쪽·오른쪽 칸 안쪽 1px 지점에서 이 체크박스가 맞는가(맞으면 겹침). */
  intrudes: { above: boolean; below: boolean; left: boolean; right: boolean };
  actionHitsAction: boolean | null;
};

async function hitArea(box: Locator): Promise<HitArea> {
  // 위·아래 40px 탐침이 화면 밖으로 나가지 않게 가운데로 스크롤한다(화면 밖 좌표는 맞지 않는다).
  // 앞 행의 작업 버튼 검사가 가로로 옮긴 표 스크롤도 처음으로 되돌린다.
  await box.evaluate((element) => {
    const container = element.closest<HTMLElement>('[data-slot="table-container"]');
    if (container) container.scrollLeft = 0;
    element.scrollIntoView({ block: "center", inline: "nearest" });
  });
  return box.evaluate((element) => {
    // 정수 좌표만 찍는다 — Chromium은 hit-test 좌표를 반올림하므로 소수 좌표는 경계에서 1px 착시를
    // 만든다(n + 0.5가 n + 1로 맞는다). 정수 n은 [n, n + 1) 픽셀이고 맞은 수 = 터치 영역 폭/높이(px).
    const step = 1;
    const own = (x: number, y: number) => {
      const hit = document.elementFromPoint(x, y);
      return !!hit && (hit === element || element.contains(hit));
    };
    const cell = element.closest('[data-slot="table-cell"],[data-slot="table-head"]')!.getBoundingClientRect();
    const row = element.closest('[data-slot="table-row"]')!;
    const rowRect = row.getBoundingClientRect();
    const rect = element.getBoundingClientRect();
    const cx = rect.left + rect.width / 2;
    const cy = rect.top + rect.height / 2;
    const xs: number[] = [];
    for (let x = Math.floor(cell.left) - 40; x <= cell.right + 40; x += step) if (own(x, cy)) xs.push(x);
    const ys: number[] = [];
    for (let y = Math.floor(rowRect.top) - 40; y <= rowRect.bottom + 40; y += step) if (own(cx, y)) ys.push(y);
    // 겹침은 1px 안쪽으로 찍어 본다. 뒤에 그려지는 이웃(아래 행·오른쪽 칸)은 겹친 영역을 덮어
    // 가리므로, 행마다 위쪽 탐침이 앞 행으로 샌 것을 잡고 마지막 행은 아래 탐침이 잡는다.
    const intrudes = {
      above: own(cx, rowRect.top - 1), below: own(cx, rowRect.bottom + 1),
      left: own(cell.left - 1, cy), right: own(cell.right + 1, cy),
    };
    const leftOfCentre21 = own(cx - 21, cy);
    const action = row.querySelector<HTMLElement>("[data-row-action]");
    let actionHitsAction: boolean | null = null;
    if (action) {
      action.scrollIntoView({ block: "nearest", inline: "nearest" });
      const a = action.getBoundingClientRect();
      const hit = document.elementFromPoint(a.left + 1, a.top + a.height / 2);
      actionHitsAction = !!hit && (hit === action || action.contains(hit));
    }
    return {
      minX: Math.min(...xs), maxX: Math.max(...xs) + 1,
      minY: Math.min(...ys), maxY: Math.max(...ys) + 1,
      cell: { left: cell.left, right: cell.right, top: cell.top, bottom: cell.bottom },
      row: { top: rowRect.top, bottom: rowRect.bottom },
      leftOfCentre21, intrudes,
      actionHitsAction,
    };
  });
}

type Sides = { top: number; right: number; bottom: number; left: number };

/** 네 변 중앙에서 요소 바깥 `distances`(기본 2~4px, outline 2px·offset 2px 띠) 픽셀을 읽는다. */
async function ringPixels(page: Page, target: Locator, distances = [2, 3, 4]): Promise<Record<keyof Sides, number[][]>> {
  const r = (await target.boundingBox())!;
  const pad = 8;
  const clip = { x: Math.floor(r.x - pad), y: Math.floor(r.y - pad), width: Math.ceil(r.width + 2 * pad), height: Math.ceil(r.height + 2 * pad) };
  const png = (await page.screenshot({ clip, scale: "css", animations: "disabled", caret: "hide" })).toString("base64");
  const points = {
    top: distances.map((d) => [r.x + r.width / 2 - clip.x, r.y - d - clip.y]),
    bottom: distances.map((d) => [r.x + r.width / 2 - clip.x, r.y + r.height + d - 1 - clip.y]),
    left: distances.map((d) => [r.x - d - clip.x, r.y + r.height / 2 - clip.y]),
    right: distances.map((d) => [r.x + r.width + d - 1 - clip.x, r.y + r.height / 2 - clip.y]),
  };
  return page.evaluate(async ({ png, points }) => {
    const image = new Image();
    image.src = "data:image/png;base64," + png;
    await image.decode();
    const canvas = document.createElement("canvas");
    canvas.width = image.width;
    canvas.height = image.height;
    const context = canvas.getContext("2d")!;
    context.drawImage(image, 0, 0);
    const read = (list: number[][]) => list.map(([x, y]) => Array.from(context.getImageData(Math.floor(x!), Math.floor(y!), 1, 1).data));
    return { top: read(points.top), right: read(points.right), bottom: read(points.bottom), left: read(points.left) };
  }, { png, points });
}

/** 키보드로 포커스해 :focus-visible을 만든 뒤, 포커스 전과 비교해 네 변에 outline이 보이는지 잰다
 *  (각 변은 띠 안 샘플 중 가장 크게 바뀐 값). `distances`가 음수면 요소 안쪽(inset outline)이다. */
async function outlineVisibility(page: Page, target: Locator, distances?: number[]): Promise<Sides> {
  await target.scrollIntoViewIfNeeded();
  await page.evaluate(() => (document.activeElement as HTMLElement | null)?.blur());
  await settle(page);
  const before = await ringPixels(page, target, distances);
  await target.focus();
  await page.keyboard.press("Shift+Tab");
  await page.keyboard.press("Tab");
  await expect(target).toBeFocused();
  expect(await target.evaluate((element) => element.matches(":focus-visible"))).toBe(true);
  await settle(page);
  const after = await ringPixels(page, target, distances);
  const one = (a: number[], b: number[]) => a.slice(0, 3).reduce((sum, value, index) => sum + Math.abs(value - b[index]!), 0);
  const diff = (a: number[][], b: number[][]) => Math.max(...a.map((pixel, index) => one(pixel, b[index]!)));
  return {
    top: diff(before.top, after.top), right: diff(before.right, after.right),
    bottom: diff(before.bottom, after.bottom), left: diff(before.left, after.left),
  };
}

const VISIBLE = 60;

for (const viewport of [{ width: 320, height: 640 }, { width: 390, height: 844 }, { width: 1440, height: 900 }]) {
  const mobile = viewport.width <= MOBILE_MAX;
  test.describe(`${viewport.width}px 터치·포커스·제목`, () => {
    test.use({ viewport });

    for (const table of ["select-table", "select-table-virtual"]) {
      test(`${table} 선택 칸 터치 영역은 이웃 행·칸과 겹치지 않는다`, async ({ page }) => {
        const errors: string[] = [];
        page.on("pageerror", (error) => errors.push(error.message));
        await page.goto("/touch-focus-contracts");
        await settle(page);
        const boxes = page.getByTestId(table).getByRole("checkbox");
        await expect(boxes).toHaveCount(6);
        for (let index = 0; index < 6; index += 1) {
          const area = await hitArea(boxes.nth(index));
          console.log(JSON.stringify({ viewport: viewport.width, table, index, area }));
          // 터치 영역은 자기 칸(=자기 행) 안에만 있다: 위·아래 행, 옆 칸의 작업 버튼과 겹치지 않는다.
          expect(area.intrudes).toEqual({ above: false, below: false, left: false, right: false });
          if (area.actionHitsAction !== null) expect(area.actionHitsAction).toBe(true);
          if (mobile) {
            expect(area.maxX - area.minX).toBeGreaterThanOrEqual(44);
            expect(area.maxY - area.minY).toBeGreaterThanOrEqual(44);
            // Map admin 390px 재현점: 중심에서 왼쪽 21px도 같은 체크박스다.
            expect(area.leftOfCentre21).toBe(true);
          }
        }
        // 넓어진 선택 칸 때문에 마지막 칸이 행(·머리 행) 밖으로 밀려나지 않는다.
        const overflow = await page.getByTestId(table).locator('[data-slot="table-row"]').evaluateAll((list) =>
          list.map((row) => (row.lastElementChild as HTMLElement).getBoundingClientRect().right - row.getBoundingClientRect().right));
        expect(Math.max(...overflow)).toBeLessThanOrEqual(0.5);
        expect(errors).toEqual([]);
      });
    }

    test("클릭 가능한 행의 inset 포커스 outline은 선택 칸 쪽(왼쪽)도 끊기지 않는다", async ({ page }) => {
      await page.goto("/touch-focus-contracts");
      await settle(page);
      const row = page.getByTestId("select-table").locator('tbody [data-slot="table-row"]').first();
      const selectCell = row.locator('[data-slot="table-cell"]').first();
      await selectCell.scrollIntoViewIfNeeded();
      await page.evaluate(() => (document.activeElement as HTMLElement | null)?.blur());
      await settle(page);
      // -outline-offset-2·outline 2px → 행 테두리 안쪽 0~2px 띠. 선택 칸의 왼쪽·위 안쪽 1·2px이 그 띠다.
      const before = await ringPixels(page, selectCell, [-1, -2]);
      await row.focus();
      await page.keyboard.press("Shift+Tab");
      await page.keyboard.press("Tab");
      await expect(row).toBeFocused();
      await settle(page);
      const after = await ringPixels(page, selectCell, [-1, -2]);
      const one = (a: number[], b: number[]) => a.slice(0, 3).reduce((sum, value, index) => sum + Math.abs(value - b[index]!), 0);
      const changed = (side: "left" | "top") => Math.max(...before[side].map((pixel, index) => one(pixel, after[side][index]!)));
      console.log(JSON.stringify({ viewport: viewport.width, id: "clickable-row", left: changed("left"), top: changed("top") }));
      expect(changed("left")).toBeGreaterThanOrEqual(VISIBLE);
      expect(changed("top")).toBeGreaterThanOrEqual(VISIBLE);
    });

    test("데스크톱 밀도는 그대로다(선택 열이 행 높이를 키우지 않는다)", async ({ page }) => {
      test.skip(mobile, "md 이상 전용");
      await page.goto("/touch-focus-contracts");
      await settle(page);
      const heightOf = (testId: string) => page.getByTestId(testId).locator('tbody [data-slot="table-row"]').first()
        .evaluate((row) => row.getBoundingClientRect().height);
      const plain = await heightOf("plain-table");
      expect(await heightOf("select-table")).toBe(plain);
      expect(plain).toBeLessThan(44);
      // 가상 표 선택 칸은 열 크기(size 36) 그대로다(일반 표 폭은 auto 배치가 나눈다).
      const cellWidth = await page.getByTestId("select-table-virtual").getByRole("checkbox").nth(1)
        .evaluate((box) => box.closest('[data-slot="table-cell"]')!.getBoundingClientRect().width);
      expect(cellWidth).toBe(36);
    });

    test("아코디언 안쪽 컨트롤의 포커스 outline은 네 변 모두 보인다", async ({ page }) => {
      await page.goto("/touch-focus-contracts");
      await settle(page);
      // 대조군: 일부러 잘린 버튼은 이 검사가 잘림으로 본다(검사가 항진명제가 아님).
      const control = await outlineVisibility(page, page.getByTestId("clip-control-button"));
      console.log(JSON.stringify({ viewport: viewport.width, control }));
      expect(Math.min(control.top, control.left, control.bottom)).toBeLessThan(VISIBLE);

      for (const id of ["accordion-open-button", "accordion-open-input"]) {
        const sides = await outlineVisibility(page, page.getByTestId(id));
        console.log(JSON.stringify({ viewport: viewport.width, id, sides }));
        for (const side of ["top", "right", "bottom", "left"] as const) expect(sides[side], `${id} ${side}`).toBeGreaterThanOrEqual(VISIBLE);
      }

      // 닫힌 항목을 연 뒤(애니메이션 종료 후)에도 같다.
      await page.getByRole("button", { name: "눌러서 여는 항목" }).click();
      const input = page.getByTestId("accordion-toggle-input");
      await expect(input).toBeVisible();
      await settle(page);
      const sides = await outlineVisibility(page, input);
      console.log(JSON.stringify({ viewport: viewport.width, id: "accordion-toggle-input", sides }));
      for (const side of ["top", "right", "bottom", "left"] as const) expect(sides[side], `toggle ${side}`).toBeGreaterThanOrEqual(VISIBLE);
    });

    test("Dialog 긴 제목은 줄바꿈되고 닫기 버튼과 겹치지 않는다", async ({ page }) => {
      await page.goto("/touch-focus-contracts");
      await page.getByRole("button", { name: "긴 제목 다이얼로그 열기" }).click();
      const dialog = page.getByTestId("long-title-dialog");
      await expect(dialog).toBeVisible();
      await settle(page);
      const geometry = await dialog.evaluate((content) => {
        const title = content.querySelector('[data-slot="dialog-title"]')!;
        const close = Array.from(content.querySelectorAll("button"))
          .find((button) => button.textContent?.trim() === "닫기")!.getBoundingClientRect();
        const range = document.createRange();
        range.selectNodeContents(title);
        const lines = Array.from(range.getClientRects()).filter((rect) => rect.width > 0)
          .map((rect) => ({ left: rect.left, right: rect.right, top: rect.top, bottom: rect.bottom }));
        const box = content.getBoundingClientRect();
        return {
          lines, close: { left: close.left, right: close.right, top: close.top, bottom: close.bottom },
          contentRight: box.right, scrollWidth: content.scrollWidth, clientWidth: content.clientWidth,
        };
      });
      console.log(JSON.stringify({ viewport: viewport.width, geometry }));
      const tops = new Set(geometry.lines.map((line) => Math.round(line.top)));
      expect(tops.size).toBeGreaterThanOrEqual(2);
      // 닫기 버튼과 그 포커스 outline(4px)을 둘러싼 영역에 제목 글자가 들어가지 않는다.
      const guard = { left: geometry.close.left - 4, right: geometry.close.right + 4, top: geometry.close.top - 4, bottom: geometry.close.bottom + 4 };
      for (const line of geometry.lines) {
        const overlaps = line.left < guard.right && line.right > guard.left && line.top < guard.bottom && line.bottom > guard.top;
        expect(overlaps, JSON.stringify(line)).toBe(false);
        expect(line.right).toBeLessThanOrEqual(geometry.contentRight - 16 + 0.5);
      }
      // 공백 없는 긴 토큰도 가로 넘침 없이 줄바꿈된다.
      expect(geometry.scrollWidth).toBeLessThanOrEqual(geometry.clientWidth);
    });
  });
}
