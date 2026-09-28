// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
import type { ReactNode } from "react";
import type { Metadata } from "next";
export const metadata: Metadata = { title: "공통 UI 설치 검증" };
import "./globals.css";
export default function Layout({ children }: { children: ReactNode }) {
  return <html lang="ko"><body>{children}</body></html>;
}
