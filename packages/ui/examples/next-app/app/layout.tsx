// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
import type { ReactNode } from "react";
import type { Metadata } from "next";
export const metadata: Metadata = { title: "kor-travel 공통 UI 예시" };
export default function Layout({ children }: { children: ReactNode }) {
  return <html lang="ko"><body>{children}</body></html>;
}
