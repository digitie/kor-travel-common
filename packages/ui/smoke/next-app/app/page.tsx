// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState } from "react";
import { AppMenu, LoginForm } from "@kor-travel/ui";
import { sanitizeLocalPath } from "@kor-travel/ui/navigation";

export default function Page() {
  const pathname = usePathname();
  const [error, setError] = useState<string | null>(null);
  return <main><h1>설치 산출물 검증</h1>
    <AppMenu pathname={pathname} linkComponent={Link} groups={[{ id: "main", items: [
      { id: "home", label: "홈", href: "/" }, { id: "query", label: "쿼리 이동", href: "/?menu=1" },
    ] }]} />
    <LoginForm error={error} onClearError={() => setError(null)} nextPath={sanitizeLocalPath("//outside.invalid")}
      onSubmit={async () => setError("인증 서버를 연결하지 않은 검증 화면입니다.")} />
  </main>;
}
