// SPDX-License-Identifier: GPL-3.0-or-later AND MIT
// SPDX-FileCopyrightText: 2023 shadcn; 2026 Youn-sok Choi (digitie)
// Origin: shadcn-ui/ui@dd41d19e2f80ff6891951f7ced74c2c9a650b065 apps/v4/registry/bases/radix/ui/badge.tsx (MIT)
// Derived-From: shadcn/ui Radix Nova
// Modified: 2026-11-11 — 공통 패키지 경로·아이콘·표현 계약 연결
"use client";

import * as React from "react"
import type { VariantProps } from "class-variance-authority"
import { badgeVariants } from "./badge-variants.js"
import { cn } from "./utils.js"
import { Slot } from "radix-ui"


function Badge({
  className,
  variant = "default",
  asChild = false,
  tone,
  ...props
}: React.ComponentProps<"span"> &
  VariantProps<typeof badgeVariants> & { asChild?: boolean; tone?: string }) {
  const Comp = asChild ? Slot.Root : "span"

  return (
    <Comp
      data-slot="badge"
      data-variant={variant}
      className={cn(badgeVariants({ variant }), tone === "ok" || tone === "success" ? "bg-kt-success-tint text-kt-success" : tone === "warn" || tone === "warning" ? "bg-kt-warning-tint text-kt-warning" : tone === "error" ? "bg-destructive/10 text-destructive" : tone === "neutral" ? "bg-muted text-muted-foreground" : undefined, className)}
      {...props}
    />
  )
}

export { Badge, badgeVariants }
