// SPDX-License-Identifier: GPL-3.0-or-later AND MIT
// SPDX-FileCopyrightText: 2023 shadcn; 2026 Youn-sok Choi (digitie)
// Origin: shadcn-ui/ui@dd41d19e2f80ff6891951f7ced74c2c9a650b065 apps/v4/registry/bases/radix/ui/button.tsx (MIT)
// Derived-From: shadcn/ui Radix Nova
// Modified: 2026-11-11 — 공통 패키지 경로·아이콘·표현 계약 연결
"use client";

import * as React from "react"
import type { VariantProps } from "class-variance-authority"
import { buttonVariants } from "./button-variants.js"
import { cn } from "./utils.js"
import { Slot } from "radix-ui"


function Button({
  className,
  variant = "default",
  size = "default",
  asChild = false,
  loading = false,
  disabledReason,
  disabled,
  onClick,
  type = "button",
  ...props
}: React.ComponentProps<"button"> &
  VariantProps<typeof buttonVariants> & {
    loading?: boolean
    disabledReason?: string
    asChild?: boolean
  }) {
  const Comp = asChild ? Slot.Root : "button"

  return (
    <Comp
      type={asChild ? undefined : type}
      disabled={disabled && !loading}
      aria-busy={loading || undefined}
      aria-disabled={loading || undefined}
      title={disabled ? disabledReason : undefined}
      onClick={loading ? (event) => { event.preventDefault(); event.stopPropagation(); } : onClick}
      data-loading={loading || undefined}
      data-slot="button"
      data-variant={variant}
      data-size={size}
      className={cn(buttonVariants({ variant, size, className }))}
      {...props}
    />
  )
}

export { Button, buttonVariants }
