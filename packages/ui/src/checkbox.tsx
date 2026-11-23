// SPDX-License-Identifier: GPL-3.0-or-later AND MIT
// SPDX-FileCopyrightText: 2023 shadcn; 2026 Youn-sok Choi (digitie)
// Origin: shadcn-ui/ui@dd41d19e2f80ff6891951f7ced74c2c9a650b065 apps/v4/registry/bases/radix/ui/checkbox.tsx (MIT)
// Derived-From: shadcn/ui Radix Nova
// Modified: 2026-11-11 — 공통 패키지 경로·아이콘·표현 계약 연결; 2026-11-23 — focus를 UX-G9.1 outline 2px·offset 2px 하나로(ring·border 변화·outline-none 제거), md 미만 after 터치 영역 44px
"use client";

import { CheckIcon } from "lucide-react";
import {  } from "lucide-react";
// SPDX-License-Identifier: MIT
// Origin: https://ui.shadcn.com/r/styles/radix-nova/checkbox.json
// Modified: 2026-11-11 — 패키지 내부 import 경로로 변경

import * as React from "react"
import { cn } from "./utils.js"
import { Checkbox as CheckboxPrimitive } from "radix-ui"


function Checkbox({
  className,
  ...props
}: React.ComponentProps<typeof CheckboxPrimitive.Root>) {
  return (
    <CheckboxPrimitive.Root
      data-slot="checkbox"
      className={cn(
        "peer relative flex size-4 shrink-0 items-center justify-center rounded-[4px] border border-input transition-[color,background-color,border-color] group-has-disabled/field:opacity-50 after:absolute after:-inset-x-3 after:-inset-y-2 max-md:after:-inset-[15px] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-kt-focus disabled:cursor-not-allowed disabled:opacity-50 aria-invalid:border-destructive aria-invalid:ring-3 aria-invalid:ring-destructive/20 aria-invalid:aria-checked:border-primary dark:bg-input/30 dark:aria-invalid:border-destructive/50 dark:aria-invalid:ring-destructive/40 data-checked:border-primary data-checked:bg-primary data-checked:text-primary-foreground dark:data-checked:bg-primary",
        className
      )}
      {...props}
    >
      <CheckboxPrimitive.Indicator
        data-slot="checkbox-indicator"
        className="grid place-content-center text-current transition-none [&>svg]:size-3.5"
      >
        <CheckIcon





        />
      </CheckboxPrimitive.Indicator>
    </CheckboxPrimitive.Root>
  )
}

export { Checkbox }
