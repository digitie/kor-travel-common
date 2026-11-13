// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
import test from "node:test";
import assert from "node:assert/strict";
import { Toast } from "../index.js";
import { Toast as RadixToast } from "radix-ui";

test("공개 Toast namespace와 모든 primitive는 Radix 원본과 동일하다", () => {
  assert.strictEqual(Toast, RadixToast);
  for (const name of ["Provider", "Root", "Title", "Description", "Close", "Viewport", "Action"])
    assert.strictEqual(Toast[name], RadixToast[name]);
});
