// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
import { defineConfig } from "@playwright/test";

const baseURL = process.env.SMOKE_BASE_URL;
if (!baseURL) throw new Error("SMOKE_BASE_URL에 격리 smoke 서버 주소가 필요합니다.");
export default defineConfig({
  testDir: ".",
  testMatch: "dialog-browser.spec.ts",
  workers: 1,
  use: { baseURL, trace: "retain-on-failure", screenshot: "only-on-failure" },
});
