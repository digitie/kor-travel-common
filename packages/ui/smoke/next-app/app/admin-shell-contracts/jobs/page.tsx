// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"use client";
import { AdminPageTitle } from "@kor-travel/ui";

export default function AdminShellJobs() {
  return <>
    <AdminPageTitle description="실행 중 3건" actions={<button type="button">새로고침</button>} />
    <p>작업 본문</p>
  </>;
}
