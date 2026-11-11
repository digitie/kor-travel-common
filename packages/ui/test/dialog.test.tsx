// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
import { createRef } from "react";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { expect, it, vi } from "vitest";
import { Dialog, DialogContent, DialogTitle, DialogDescription } from "../src/dialog.js";
import { AlertDialog, AlertDialogContent, AlertDialogTitle, AlertDialogDescription, AlertDialogCancel } from "../src/alert-dialog.js";

it("Dialog 단일 overlay의 ref·이벤트·소비자 속성을 전달하고 표현 옵션은 DOM에 흘리지 않는다", async () => {
  const click = vi.fn();
  const ref = createRef<HTMLDivElement>();
  render(<Dialog open><DialogContent unstyled data-testid="content"
    overlayProps={{ "data-testid": "scrim", ref, onClick: click }}>
    <DialogTitle>제목</DialogTitle><DialogDescription>설명</DialogDescription>
  </DialogContent></Dialog>);
  const overlay = screen.getByTestId("scrim");
  expect(ref.current).toBe(overlay);
  expect(document.querySelectorAll('[data-slot="dialog-overlay"]')).toHaveLength(1);
  await userEvent.click(overlay);
  expect(click).toHaveBeenCalledOnce();
  expect(screen.getByTestId("content")).not.toHaveAttribute("unstyled");
  expect(screen.getByTestId("content")).not.toHaveAttribute("overlayProps");
});

it("AlertDialog 바깥 클릭은 기본 닫힘 없이 소비자의 overlay 이벤트로 전달한다", async () => {
  const click = vi.fn();
  const change = vi.fn();
  render(<AlertDialog open onOpenChange={change}><AlertDialogContent unstyled data-testid="content"
    overlayProps={{ "data-testid": "scrim", onClick: click }}>
    <AlertDialogTitle>확인</AlertDialogTitle><AlertDialogDescription>설명</AlertDialogDescription>
    <AlertDialogCancel>취소</AlertDialogCancel>
  </AlertDialogContent></AlertDialog>);
  expect(document.querySelectorAll('[data-slot="alert-dialog-overlay"]')).toHaveLength(1);
  await userEvent.click(screen.getByTestId("scrim"));
  expect(click).toHaveBeenCalledOnce();
  expect(change).not.toHaveBeenCalled();
  expect(screen.getByRole("alertdialog")).toBeInTheDocument();
  expect(screen.getByTestId("content")).not.toHaveAttribute("unstyled");
});
