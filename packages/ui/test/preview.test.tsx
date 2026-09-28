// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { expect, it } from "vitest";
import { Preview } from "../examples/Preview.js";

it("메뉴 선택 뒤에도 링크 DOM과 키보드 포커스를 유지한다", async () => {
  render(<Preview projectId="map" />);
  const link = screen.getByRole("link", { name: "Feature 지도" });
  link.focus();
  await userEvent.keyboard("{Enter}");
  expect(screen.getByRole("link", { name: "Feature 지도" })).toBe(link);
  expect(link).toHaveFocus();
  expect(link).toHaveAttribute("aria-current", "page");
});

it("프로젝트 변경 시 이전 메뉴 선택을 초기화한다", async () => {
  const { rerender } = render(<Preview projectId="map" />);
  await userEvent.click(screen.getByRole("link", { name: "설정" }));
  rerender(<Preview projectId="weather" />);
  expect(screen.getByRole("navigation").querySelectorAll('[aria-current="page"]')).toHaveLength(1);
  expect(screen.getByRole("heading", { level: 1 })).toHaveTextContent("로그인");
});
