// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"use client";

export interface LoginErrorProps {
  error?: string | null;
  id?: string;
}

export function LoginError({ error, id }: LoginErrorProps) {
  return <p id={id} data-slot="login-error" role="alert" aria-atomic="true"
    className="min-h-6 break-words text-kt-sm text-kt-destructive">{error || ""}</p>;
}
