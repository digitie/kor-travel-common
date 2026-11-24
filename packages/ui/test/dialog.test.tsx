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

// ui 0.2.7: 모달 grid 칸은 minmax(0,1fr) 하나다. 암시적 auto 칸은 넓은 자식(표 등)의 min-content만큼
// 커져 좁은 화면에서 모달을 넘친다. 실제 기하는 smoke/dialog-overflow-browser.spec.ts가 320/390/1440에서 잰다.
const GRID_TRACK = "grid-cols-[minmax(0,1fr)]";
function gridColumnClasses(element: HTMLElement): string[] {
  // variant 접두(대괄호·슬래시 포함)와 !important 표기까지 센다.
  return (element.getAttribute("class") ?? "").split(/\s+/).filter((c) => /^(?:[^\s:]+:)*!?grid-cols-/.test(c));
}

it("DialogContent·AlertDialogContent의 grid 칸은 minmax(0,1fr) 하나이고 unstyled에는 붙지 않는다", () => {
  const { unmount } = render(<Dialog open><DialogContent data-testid="content">
    <DialogTitle>제목</DialogTitle><DialogDescription>설명</DialogDescription>
  </DialogContent></Dialog>);
  expect(gridColumnClasses(screen.getByTestId("content"))).toEqual([GRID_TRACK]);
  unmount();
  const alert = render(<AlertDialog open><AlertDialogContent data-testid="alert-content">
    <AlertDialogTitle>확인</AlertDialogTitle><AlertDialogDescription>설명</AlertDialogDescription>
    <AlertDialogCancel>취소</AlertDialogCancel>
  </AlertDialogContent></AlertDialog>);
  expect(gridColumnClasses(screen.getByTestId("alert-content"))).toEqual([GRID_TRACK]);
  alert.unmount();
  const bare = render(<Dialog open><DialogContent unstyled data-testid="bare">
    <DialogTitle>제목</DialogTitle><DialogDescription>설명</DialogDescription>
  </DialogContent></Dialog>);
  expect(gridColumnClasses(screen.getByTestId("bare"))).toEqual([]);
  bare.unmount();
  render(<AlertDialog open><AlertDialogContent unstyled data-testid="alert-bare">
    <AlertDialogTitle>확인</AlertDialogTitle><AlertDialogDescription>설명</AlertDialogDescription>
    <AlertDialogCancel>취소</AlertDialogCancel>
  </AlertDialogContent></AlertDialog>);
  expect(gridColumnClasses(screen.getByTestId("alert-bare"))).toEqual([]);
});

it("소비자 className의 grid-cols-*가 기본 칸을 대신한다", () => {
  const { unmount } = render(<Dialog open><DialogContent data-testid="content" className="grid-cols-2 md:grid-cols-3">
    <DialogTitle>제목</DialogTitle><DialogDescription>설명</DialogDescription>
  </DialogContent></Dialog>);
  expect(gridColumnClasses(screen.getByTestId("content"))).toEqual(["grid-cols-2", "md:grid-cols-3"]);
  unmount();
  render(<AlertDialog open><AlertDialogContent data-testid="alert-content" className="grid-cols-[1fr_auto]">
    <AlertDialogTitle>확인</AlertDialogTitle><AlertDialogDescription>설명</AlertDialogDescription>
    <AlertDialogCancel>취소</AlertDialogCancel>
  </AlertDialogContent></AlertDialog>);
  expect(gridColumnClasses(screen.getByTestId("alert-content"))).toEqual(["grid-cols-[1fr_auto]"]);
});
