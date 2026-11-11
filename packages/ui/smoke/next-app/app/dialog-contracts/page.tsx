// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"use client";

import { useState, type ComponentProps } from "react";
import {
  Dialog, DialogTrigger, DialogContent, DialogTitle, DialogDescription,
  DialogFooter, DialogClose,
} from "@kor-travel/ui/dialog";
import {
  AlertDialog, AlertDialogTrigger, AlertDialogContent, AlertDialogTitle,
  AlertDialogDescription, AlertDialogFooter, AlertDialogAction, AlertDialogCancel,
} from "@kor-travel/ui/alert-dialog";

function LongFields() {
  return <div className="grid gap-4">
    {Array.from({ length: 24 }, (_, index) => <label key={index} className="grid gap-2">
      항목 {index + 1}
      <input className="min-h-11 border p-2" aria-label={`항목 ${index + 1}`} />
    </label>)}
  </div>;
}

function NestedConfirmation() {
  return <AlertDialog>
    <AlertDialogTrigger asChild><button type="button">중첩 확인 열기</button></AlertDialogTrigger>
    <AlertDialogContent data-testid="nested-alert">
      <AlertDialogTitle>중첩 확인</AlertDialogTitle>
      <AlertDialogDescription>부모 입력과 포커스는 닫을 때까지 유지됩니다.</AlertDialogDescription>
      <LongFields />
      <AlertDialogFooter><AlertDialogCancel>중첩 확인 취소</AlertDialogCancel></AlertDialogFooter>
    </AlertDialogContent>
  </AlertDialog>;
}

function CustomPresentation() {
  const [open, setOpen] = useState(false);
  const [busy, setBusy] = useState(false);
  return <>
    <Dialog>
      <DialogTrigger asChild><button type="button">표현 전용 양식 열기</button></DialogTrigger>
      <DialogContent unstyled showCloseButton={false} data-testid="custom-sheet"
        className="fixed inset-x-0 bottom-0 z-50 flex max-h-[88dvh] flex-col rounded-t-xl bg-white p-5 sm:inset-x-auto sm:bottom-auto sm:top-1/2 sm:left-1/2 sm:w-full sm:max-w-lg sm:-translate-x-1/2 sm:-translate-y-1/2"
        overlayProps={{ "data-testid": "custom-sheet-overlay", className: "fixed inset-0 z-50 bg-black/50" }}>
        <DialogTitle className="shrink-0">표현 전용 양식</DialogTitle>
        <DialogDescription className="shrink-0">모바일 sheet와 데스크톱 중앙 창 표현을 소비자가 정합니다.</DialogDescription>
        <div data-testid="custom-sheet-body" className="min-h-0 overflow-y-auto"><LongFields /></div>
        <DialogClose asChild><button type="button" className="shrink-0">표현 전용 닫기</button></DialogClose>
      </DialogContent>
    </Dialog>
    <AlertDialog open={open} onOpenChange={setOpen}>
      <AlertDialogTrigger asChild><button type="button">표현 전용 확인 열기</button></AlertDialogTrigger>
      <AlertDialogContent unstyled data-testid="custom-confirm"
        className="fixed top-1/2 left-1/2 z-50 w-[calc(100%-2rem)] max-w-md -translate-x-1/2 -translate-y-1/2 rounded-xl bg-white p-5"
        onEscapeKeyDown={event => { if (busy) event.preventDefault(); }}
        overlayProps={{ "data-testid": "custom-confirm-overlay", className: "fixed inset-0 z-50 bg-black/50", onClick: () => { if (!busy) setOpen(false); } }}>
        <AlertDialogTitle>표현 전용 확인</AlertDialogTitle>
        <AlertDialogDescription>진행 중일 때는 소비자의 취소 정책을 유지합니다.</AlertDialogDescription>
        <label><input type="checkbox" checked={busy} onChange={event => setBusy(event.target.checked)} />작업 진행 중</label>
        <AlertDialogCancel disabled={busy}>표현 전용 취소</AlertDialogCancel>
      </AlertDialogContent>
    </AlertDialog>
  </>;
}

function SizedDialog() {
  const [size, setSize] = useState<NonNullable<ComponentProps<typeof DialogContent>["size"]>>("md");
  const [override, setOverride] = useState(false);
  const [baseOverride, setBaseOverride] = useState(false);
  return <section>
    <label>대화상자 크기<select aria-label="대화상자 크기" value={size} onChange={event => setSize(event.target.value as typeof size)}>
      {(["sm", "md", "lg", "xl", "2xl", "full"] as const).map(value => <option key={value}>{value}</option>)}
    </select></label>
    <label><input type="checkbox" checked={override} onChange={event => setOverride(event.target.checked)} />폭 재정의</label>
    <label><input type="checkbox" checked={baseOverride} onChange={event => setBaseOverride(event.target.checked)} />기본 폭 재정의</label>
    <Dialog>
      <DialogTrigger asChild><button type="button">크기 창 열기</button></DialogTrigger>
      <DialogContent size={size} className={baseOverride ? "max-w-3xl" : override ? "sm:max-w-md" : undefined} data-testid="sized-dialog">
        <DialogTitle>크기 계약</DialogTitle>
        <DialogDescription>크기와 관계없이 viewport 여백과 긴 내용 접근을 유지합니다.</DialogDescription>
        <LongFields />
        <DialogFooter><DialogClose asChild><button type="button">크기 창 닫기</button></DialogClose></DialogFooter>
      </DialogContent>
    </Dialog>
  </section>;
}

export default function DialogContracts() {
  const [saved, setSaved] = useState(0);
  const [confirmed, setConfirmed] = useState(0);
  return <main className="min-h-screen space-y-6 p-8">
    <h1>긴 대화상자 접근성 검증</h1>
    <output data-testid="saved">{saved}</output>
    <output data-testid="confirmed">{confirmed}</output>
    <Dialog>
      <DialogTrigger asChild><button type="button">긴 양식 열기</button></DialogTrigger>
      <DialogContent data-testid="long-dialog">
        <DialogTitle>긴 양식</DialogTitle>
        <DialogDescription>모바일과 데스크톱에서 모든 항목과 동작에 접근합니다.</DialogDescription>
        <form className="grid gap-4" onSubmit={event => { event.preventDefault(); setSaved(value => value + 1); }}>
          <LongFields />
          <NestedConfirmation />
          <DialogFooter>
            <DialogClose asChild><button type="button">양식 닫기</button></DialogClose>
            <button type="submit">양식 저장</button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
    <CustomPresentation />
    <SizedDialog />
    <AlertDialog>
      <AlertDialogTrigger asChild><button type="button">긴 확인 열기</button></AlertDialogTrigger>
      <AlertDialogContent data-testid="long-alert">
        <AlertDialogTitle>긴 확인</AlertDialogTitle>
        <AlertDialogDescription>작업 전체 내용을 읽고 취소하거나 승인합니다.</AlertDialogDescription>
        <LongFields />
        <AlertDialogFooter>
          <AlertDialogCancel>확인 취소</AlertDialogCancel>
          <AlertDialogAction onClick={() => setConfirmed(value => value + 1)}>작업 승인</AlertDialogAction>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>
  </main>;
}
