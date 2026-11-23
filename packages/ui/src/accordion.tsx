// SPDX-License-Identifier: GPL-3.0-or-later AND MIT
// SPDX-FileCopyrightText: 2023 shadcn; 2026 Youn-sok Choi (digitie)
// Origin: shadcn-ui/ui@dd41d19e2f80ff6891951f7ced74c2c9a650b065 apps/v4/registry/bases/radix/ui/accordion.tsx (MIT)
// Derived-From: shadcn/ui Radix Nova
// Modified: 2026-11-11 — 공통 패키지 경로·아이콘·표현 계약 연결; 2026-11-23 — focus를 UX-G9.1 outline 2px·offset 2px 하나로(ring·border 변화·outline-none 제거); 2026-11-23 — 내용 영역을 overflow:clip + clip-margin 4px로 잘라 안쪽 컨트롤 포커스 outline이 보이게
"use client";

import { ChevronDownIcon, ChevronUpIcon } from "lucide-react";
import {  } from "lucide-react";
// SPDX-License-Identifier: MIT
// Origin: https://ui.shadcn.com/r/styles/radix-nova/accordion.json
// Modified: 2026-11-11 — 패키지 내부 import 경로로 변경

import * as React from "react"
import { cn } from "./utils.js"
import { Accordion as AccordionPrimitive } from "radix-ui"


function Accordion({
  className,
  ...props
}: React.ComponentProps<typeof AccordionPrimitive.Root>) {
  return (
    <AccordionPrimitive.Root
      data-slot="accordion"
      className={cn("flex w-full flex-col", className)}
      {...props}
    />
  )
}

function AccordionItem({
  className,
  ...props
}: React.ComponentProps<typeof AccordionPrimitive.Item>) {
  return (
    <AccordionPrimitive.Item
      data-slot="accordion-item"
      className={cn("not-last:border-b", className)}
      {...props}
    />
  )
}

function AccordionTrigger({
  className,
  children,
  ...props
}: React.ComponentProps<typeof AccordionPrimitive.Trigger>) {
  return (
    <AccordionPrimitive.Header className="flex">
      <AccordionPrimitive.Trigger
        data-slot="accordion-trigger"
        className={cn(
          "group/accordion-trigger relative flex flex-1 items-start justify-between rounded-lg border border-transparent py-2.5 text-left text-sm font-medium transition-[color,background-color,border-color] hover:underline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-kt-focus disabled:pointer-events-none disabled:opacity-50 **:data-[slot=accordion-trigger-icon]:ml-auto **:data-[slot=accordion-trigger-icon]:size-4 **:data-[slot=accordion-trigger-icon]:text-muted-foreground",
          className
        )}
        {...props}
      >
        {children}
        <ChevronDownIcon


          data-slot="accordion-trigger-icon"



          className="pointer-events-none shrink-0 group-aria-expanded/accordion-trigger:hidden"
        />
        <ChevronUpIcon


          data-slot="accordion-trigger-icon"



          className="pointer-events-none hidden shrink-0 group-aria-expanded/accordion-trigger:inline"
        />
      </AccordionPrimitive.Trigger>
    </AccordionPrimitive.Header>
  )
}

// overflow:hidden은 열린 뒤에도 안쪽 컨트롤의 포커스 outline(2px+offset 2px)을 위·양옆에서 잘랐다.
// overflow:clip + overflow-clip-margin 4px은 그 outline 폭만큼만 잘림 경계를 넓힌다. 넓은 자식이나
// 높이 애니메이션 중의 안쪽 높이는 여전히 잘려 바깥 스크롤 폭·높이에 더해지지 않는다(clip-path와 다름).
// overflow-clip-margin이 없는 엔진(WebKit)에서는 이전 overflow:hidden과 같게 잘린다.
function AccordionContent({
  className,
  children,
  ...props
}: React.ComponentProps<typeof AccordionPrimitive.Content>) {
  return (
    <AccordionPrimitive.Content
      data-slot="accordion-content"
      className="overflow-clip text-sm [overflow-clip-margin:4px] data-open:animate-accordion-down data-closed:animate-accordion-up"
      {...props}
    >
      <div
        className={cn(
          "h-(--radix-accordion-content-height) pt-0 pb-2.5 [&_a]:underline [&_a]:underline-offset-3 [&_a]:hover:text-foreground [&_p:not(:last-child)]:mb-4",
          className
        )}
      >
        {children}
      </div>
    </AccordionPrimitive.Content>
  )
}

export { Accordion, AccordionItem, AccordionTrigger, AccordionContent }
