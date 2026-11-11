// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
import { defineConfig } from "@playwright/test";
const app = process.env.SMOKE_APP;
if (!app) throw new Error("SMOKE_APP 격리 설치 경로 필요");
export default defineConfig({
  testDir: ".",
  testMatch: ["radix-browser.spec.ts", "dialog-browser.spec.ts"],
  workers: 1,
  use: { baseURL: "http://127.0.0.1:13010" },
  webServer: {
    command: "npm exec -- next start --hostname 127.0.0.1 --port 13010",
    cwd: app,
    url: "http://127.0.0.1:13010/radix-contracts",
    reuseExistingServer: false,
  },
});
