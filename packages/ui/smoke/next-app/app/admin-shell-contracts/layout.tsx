// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"use client";
import type { ReactNode } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { AdminShell, AppMenu } from "@kor-travel/ui";

const groups = [{ id: "ops", label: "운영", items: [
  { id: "home", label: "개요", href: "/admin-shell-contracts", exact: true },
  { id: "jobs", label: "작업", href: "/admin-shell-contracts/jobs" },
] }];

export default function AdminShellContractsLayout({ children }: { children: ReactNode }) {
  const pathname = usePathname();
  const page = pathname.endsWith("/jobs") ? "작업" : "개요";
  return <AdminShell area="검증" title={page} brand="검증 관리자" navigationKey={pathname}
    collapsedStorageKey="kor-travel-ui-smoke:sidebar-collapsed" mainClassName="p-4"
    railFooter={({ collapsed }) => <button type="button" className="min-h-11 w-full">{collapsed ? "↩" : "로그아웃"}</button>}
    menu={<AppMenu groups={groups} pathname={pathname} linkComponent={Link} />}>
    {children}
  </AdminShell>;
}
