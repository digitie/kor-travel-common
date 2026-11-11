// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
import { buttonVariants } from "@kor-travel/ui/button-variants";
import { badgeVariants } from "@kor-travel/ui/badge-variants";
import { Button } from "@kor-travel/ui/button";
export default function ServerVariants() {
  return <main><h1>서버 variant 함수 검증</h1><a href="/" className={buttonVariants({variant:"outline"})}>서버 링크</a><span className={badgeVariants({variant:"secondary"})}>서버 배지</span><Button>클라이언트 부품 대조</Button></main>;
}
