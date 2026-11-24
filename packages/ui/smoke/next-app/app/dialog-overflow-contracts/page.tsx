// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"use client";
import { VirtualTable, type ColumnDef } from "@kor-travel/ui/virtual-table";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@kor-travel/ui/table";
import { Button } from "@kor-travel/ui/button";
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from "@kor-travel/ui/dialog";
import {
  AlertDialog, AlertDialogCancel, AlertDialogContent, AlertDialogDescription, AlertDialogFooter, AlertDialogHeader,
  AlertDialogTitle, AlertDialogTrigger,
} from "@kor-travel/ui/alert-dialog";

// ui 0.2.7 회귀 표면: 모달 안 넓은 표가 좁은 화면에서 모달 grid 칸을 넓히지 않고 표 컨테이너 안에서
// 가로로 스크롤되는지. 가상 표는 열 폭 합(600px)을 최소 폭으로, 일반 표는 줄바꿈 없는 칸 내용으로 넓다.
// 본문 래퍼는 min-width:0이 없는 세로 flex(소비자 상세 화면 구성).
type Video = { id: string; title: string; channel: string; length: string };
const videos: Video[] = Array.from({ length: 6 }, (_, index) => ({
  id: String(index), title: "수집 영상 " + (index + 1), channel: "채널 " + (index + 1), length: "12:3" + index,
}));
const videoColumns: ColumnDef<Video, unknown>[] = [
  { accessorKey: "title", header: "영상", size: 240 },
  { accessorKey: "channel", header: "채널", size: 200 },
  { accessorKey: "length", header: "길이", size: 160 },
];
const WIDE_HEADERS = ["대상", "실행 횟수", "마지막 수집", "다음 실행", "기본 카테고리"];

function WideTable({ label }: { label: string }) {
  return <Table aria-label={label} containerAriaLabel={label}>
    <TableHeader><TableRow>{WIDE_HEADERS.map((header) => <TableHead key={header}>{header}</TableHead>)}</TableRow></TableHeader>
    <TableBody>
      {[1, 2, 3].map((row) => <TableRow key={row}>
        {WIDE_HEADERS.map((header) => <TableCell key={header}>{header} 값 2026-11-24 09:3{row}</TableCell>)}
      </TableRow>)}
    </TableBody>
  </Table>;
}

export default function DialogOverflowContracts() {
  return (
    <main style={{ display: "flex", flexDirection: "column", alignItems: "flex-start", gap: 12, padding: 16 }}>
      <h1>다이얼로그 넓은 본문 검증</h1>

      <Dialog>
        <DialogTrigger asChild><Button variant="outline">넓은 표 상세 열기</Button></DialogTrigger>
        <DialogContent size="lg" data-testid="wide-detail-dialog">
          <DialogHeader>
            <DialogTitle>반복 작업 상세</DialogTitle>
            <DialogDescription>반복 작업의 설정과 그동안 수집한 영상</DialogDescription>
          </DialogHeader>
          <div data-testid="wide-detail-body" style={{ display: "flex", flexDirection: "column", gap: 20 }}>
            <section style={{ display: "flex", flexDirection: "column", gap: 8 }}>
              <h2>누적 수집 영상</h2>
              <div style={{ maxHeight: 320, overflow: "auto" }}>
                <VirtualTable columns={videoColumns} data={videos} getRowId={(row) => row.id}
                  ariaLabel="누적 수집 영상" containerAriaLabel="누적 수집 영상 표" virtualized height={240}
                  estimateRowSize={40} />
              </div>
            </section>
            <WideTable label="반복 대상 요약" />
          </div>
          <DialogFooter showCloseButton />
        </DialogContent>
      </Dialog>

      <AlertDialog>
        <AlertDialogTrigger asChild><Button variant="outline">넓은 표 확인 열기</Button></AlertDialogTrigger>
        <AlertDialogContent data-testid="wide-alert-dialog">
          <AlertDialogHeader>
            <AlertDialogTitle>대상 일괄 중지</AlertDialogTitle>
            <AlertDialogDescription>아래 대상을 중지합니다.</AlertDialogDescription>
          </AlertDialogHeader>
          {/* 표를 일반 블록으로 감싼다: 스크롤 컨테이너가 grid 항목이면 auto 칸도 넘치지 않아 회귀를 못 본다. */}
          <div data-testid="wide-alert-body"><WideTable label="중지 대상" /></div>
          <AlertDialogFooter><AlertDialogCancel>확인 취소</AlertDialogCancel></AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </main>
  );
}
