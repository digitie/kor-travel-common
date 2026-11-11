// SPDX-License-Identifier: GPL-3.0-or-later AND MIT
// SPDX-FileCopyrightText: 2023 shadcn; 2026 Youn-sok Choi (digitie)
// Origin: shadcn-ui/ui@dd41d19e2f80ff6891951f7ced74c2c9a650b065 apps/v4/registry/bases/radix/ui/collapsible.tsx (MIT)
// Derived-From: shadcn/ui Radix Nova
// Modified: 2026-11-11 — 공통 패키지 경로·아이콘·표현 계약 연결
"use client";

import { Collapsible as CollapsiblePrimitive } from "radix-ui"

function Collapsible({
  ...props
}: React.ComponentProps<typeof CollapsiblePrimitive.Root>) {
  return <CollapsiblePrimitive.Root data-slot="collapsible" {...props} />
}

function CollapsibleTrigger({
  ...props
}: React.ComponentProps<typeof CollapsiblePrimitive.CollapsibleTrigger>) {
  return (
    <CollapsiblePrimitive.CollapsibleTrigger
      data-slot="collapsible-trigger"
      {...props}
    />
  )
}

function CollapsibleContent({
  ...props
}: React.ComponentProps<typeof CollapsiblePrimitive.CollapsibleContent>) {
  return (
    <CollapsiblePrimitive.CollapsibleContent
      data-slot="collapsible-content"
      {...props}
    />
  )
}

export { Collapsible, CollapsibleTrigger, CollapsibleContent }
