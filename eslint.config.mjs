// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
import js from "@eslint/js";
import tseslint from "typescript-eslint";

export default tseslint.config(
  { ignores: ["**/dist/**", "**/node_modules/**", "**/.next/**", "**/next-env.d.ts", "**/test-results/**", "**/playwright-report/**"] },
  js.configs.recommended,
  ...tseslint.configs.recommended,
  { files: ["**/*.ts", "**/*.tsx"], rules: {
    "@typescript-eslint/no-unused-vars": ["error", { argsIgnorePattern: "^_", varsIgnorePattern: "^_" }],
  } },
);
