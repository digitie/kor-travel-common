// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)

/** 리다이렉트는 루트 기준 로컬 경로만 허용한다. 인코딩된 경계 문자도 거부한다. */
export function sanitizeLocalPath(value: string | null | undefined): string {
  if (!value || !value.startsWith("/") || value.startsWith("//")) return "/";
  // 중첩 인코딩은 소비자 라우터의 추가 디코딩 여부와 무관하게 차단한다.
  if (/[\\\u0000-\u0020\u007f]|%(?:2f|5c|0[0-9a-f]|1[0-9a-f]|20|7f|25)/i.test(value)) return "/";
  try {
    const parsed = new URL(value, "https://local.invalid");
    if (parsed.origin !== "https://local.invalid" || parsed.pathname.startsWith("//")) return "/";
    return parsed.pathname + parsed.search + parsed.hash;
  } catch {
    return "/";
  }
}

export interface MenuRoute {
  id: string;
  href: string;
  exact?: boolean;
}

/** 라우트 경계가 일치하는 최장 경로를 선택한다. 같은 경로는 첫 항목을 쓴다. */
export function getActiveMenuItemId(items: readonly MenuRoute[], pathname: string): string | undefined {
  const current = sanitizeLocalPath(pathname).split(/[?#]/, 1)[0]!.replace(/\/+$/, "") || "/";
  let active: MenuRoute | undefined;
  let longest = -1;
  for (const item of items) {
    // query/hash 메뉴는 activeItemId를 통해 앱에서 판정한다.
    if (!item.href.startsWith("/") || /[?#]/.test(item.href) || sanitizeLocalPath(item.href) !== item.href) continue;
    const path = item.href.replace(/\/+$/, "") || "/";
    const matches = current === path || (!item.exact && path !== "/" && current.startsWith(path + "/"));
    if (matches && path.length > longest) {
      active = item;
      longest = path.length;
    }
  }
  return active?.id;
}
