// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
import { describe, expect, it } from "vitest";
import { sanitizeLocalPath, getActiveMenuItemId } from "../src/navigation.js";
import { getLoginErrorMessage } from "../src/login-messages.js";

describe("안전한 경로", () => {
  it.each([undefined, null, "", "https://outside.invalid", "//outside.invalid", "/\\outside.invalid", "/%2foutside.invalid", "/%5coutside.invalid", "/%252foutside.invalid", "/\n/outside.invalid", "/%00bad", "/a/..//outside.invalid"])("위험한 경로 %s", value => {
    expect(sanitizeLocalPath(value)).toBe("/");
  });
  it.each(["/admin", "/jobs?page=2#recent", "/search?q=%EA%B8%B0%EC%B0%A8"])("로컬 경로 %s", value => {
    expect(sanitizeLocalPath(value)).toBe(value);
  });
  it("경로 경계·루트·exact·동률·query를 구분한다", () => {
    const items = [{ id: "home", href: "/" }, { id: "jobs", href: "/jobs" }, { id: "deep", href: "/jobs/1", exact: true }];
    expect(getActiveMenuItemId(items, "/jobs/12")).toBe("jobs");
    expect(getActiveMenuItemId(items, "/jobs/1")).toBe("deep");
    expect(getActiveMenuItemId(items, "/jobs/1/sub")).toBe("jobs");
    expect(getActiveMenuItemId(items, "/jobsite")).toBeUndefined();
    expect(getActiveMenuItemId(items, "/?a=b")).toBe("home");
    expect(getActiveMenuItemId([...items, { id: "last", href: "/jobs" }], "/jobs/")).toBe("jobs");
  });
});

it("로그인 상태 코드를 한국어 문구로 매핑한다", () => {
  expect(getLoginErrorMessage(503)).toContain("설정");
  expect(getLoginErrorMessage(429)).toContain("시도가 너무 많습니다");
  expect(getLoginErrorMessage(403)).toContain("허용되지 않은 요청");
  expect(getLoginErrorMessage(401)).toContain("비밀번호");
});
