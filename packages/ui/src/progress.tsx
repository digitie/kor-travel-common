// SPDX-License-Identifier: GPL-3.0-or-later AND MIT
// SPDX-FileCopyrightText: 2023 shadcn; 2026 Youn-sok Choi (digitie)
// Origin: shadcn-ui/ui@dd41d19e2f80ff6891951f7ced74c2c9a650b065 apps/v4/registry/bases/radix/ui/progress.tsx (MIT)
// Derived-From: shadcn/ui Radix Nova
// Modified: 2026-11-11 — 공통 패키지 경로·아이콘·표현 계약 연결
"use client";

import * as React from "react"
import { cn } from "./utils.js"
import { Progress as ProgressPrimitive } from "radix-ui"

function Progress({
  className,
  value,
  max = 100,
  ...props
}: React.ComponentProps<typeof ProgressPrimitive.Root>) {
  const maximum = Number.isFinite(max) && max > 0 ? max : 100
  const current = typeof value === "number" && Number.isFinite(value) && value >= 0 && value <= maximum ? value : null
  const percentage = current === null ? 0 : (current / maximum) * 100
  return (
    <ProgressPrimitive.Root
      data-slot="progress"
      value={current}
      max={maximum}
      className={cn(
        "relative flex h-1 w-full items-center overflow-x-hidden rounded-full bg-muted",
        className
      )}
      {...props}
    >
      <ProgressPrimitive.Indicator
        data-slot="progress-indicator"
        className="size-full flex-1 bg-primary transition-transform"
        style={{ transform: "translateX(-" + (100 - percentage) + "%)" }}
      />
    </ProgressPrimitive.Root>
  )
}

export { Progress }
