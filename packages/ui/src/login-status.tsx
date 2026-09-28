// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"use client";

export interface LoginStatusProps {
  status: "checking" | "authenticated" | "unauthenticated";
  userLabel?: string;
}

export function LoginStatus({ status, userLabel }: LoginStatusProps) {
  const message = status === "checking" ? "로그인 상태 확인 중…"
    : status === "authenticated" ? (userLabel ? `${userLabel}님, 로그인됨` : "로그인됨")
      : "로그인이 필요합니다.";
  return <p data-slot="login-status" data-state={status} role="status" aria-atomic="true"
    className="break-words text-kt-sm text-kt-text-secondary">{message}</p>;
}
