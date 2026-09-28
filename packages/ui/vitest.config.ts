// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
import { defineConfig } from "vitest/config";

export default defineConfig({
  test: { environment: "jsdom", include: ["test/**/*.test.ts", "test/**/*.test.tsx"], setupFiles: ["./test/setup.ts"] },
});
