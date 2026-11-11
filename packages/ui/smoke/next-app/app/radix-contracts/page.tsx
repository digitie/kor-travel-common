// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"use client";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@kor-travel/ui/tabs";
import { Switch } from "@kor-travel/ui/switch";
import { Checkbox } from "@kor-travel/ui/checkbox";
import { Dialog, DialogTrigger, DialogContent, DialogTitle, DialogDescription } from "@kor-travel/ui/dialog";
import { Button } from "@kor-travel/ui/button";

export default function RadixContracts() {
  return <main className="space-y-6 p-6"><h1>Radix 상태·접근성 검증</h1>
    <Tabs orientation="vertical" defaultValue="one"><TabsList><TabsTrigger value="one">첫 탭</TabsTrigger><TabsTrigger value="two">둘째 탭</TabsTrigger></TabsList><TabsContent value="one" forceMount>첫 내용</TabsContent><TabsContent value="two" forceMount>둘째 내용</TabsContent></Tabs>
    <label className="flex items-center gap-2"><Switch aria-label="사용 상태" defaultChecked />사용 상태</label>
    <label className="flex items-center gap-2"><Checkbox aria-label="작업 선택" defaultChecked />작업 선택</label>
    <Dialog><DialogTrigger asChild><Button>상세 열기</Button></DialogTrigger><DialogContent><DialogTitle>작업 상세</DialogTitle><DialogDescription>포커스 복원과 대화상자 상태를 확인합니다.</DialogDescription></DialogContent></Dialog>
  </main>;
}
