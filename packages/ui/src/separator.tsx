// SPDX-License-Identifier: GPL-3.0-or-later AND MIT
// SPDX-FileCopyrightText: 2023 shadcn; 2026 Youn-sok Choi (digitie)
// Origin: shadcn-ui/ui@dd41d19e2f80ff6891951f7ced74c2c9a650b065 apps/v4/registry/bases/radix/ui/separator.tsx (MIT)
// Derived-From: shadcn/ui Radix Nova
// Modified: 2026-11-11 — 공통 패키지 경로·아이콘·표현 계약 연결
"use client";

import * as React from "react"
import { cn } from "./utils.js"
import { Separator as SeparatorPrimitive } from "radix-ui"

function Separator({
  className,
  orientation = "horizontal",
  decorative = true,
  ...props
}: React.ComponentProps<typeof SeparatorPrimitive.Root>) {
  return (
    <SeparatorPrimitive.Root
      data-slot="separator"
      decorative={decorative}
      orientation={orientation}
      className={cn(
        "shrink-0 bg-border data-horizontal:h-px data-horizontal:w-full data-vertical:w-px data-vertical:self-stretch",
        className
      )}
      {...props}
    />
  )
}

export { Separator }
