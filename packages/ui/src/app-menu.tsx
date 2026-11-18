// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"use client";

import { createContext, useContext, useId } from "react";
import type { ComponentType, ComponentPropsWithRef, ReactNode } from "react";
import { getActiveMenuItemId } from "./navigation.js";

interface MenuItemBase { id: string; label: string; icon?: ReactNode; hint?: string; disabled?: boolean }
export interface AppMenuLinkItem extends MenuItemBase { href: string; exact?: boolean; onSelect?: never }
export interface AppMenuActionItem extends MenuItemBase { href?: never; onSelect: () => void }
export type AppMenuItem = AppMenuLinkItem | AppMenuActionItem;
export interface AppMenuGroup { id: string; label?: string; items: readonly AppMenuItem[] }
export type AppMenuLinkProps = ComponentPropsWithRef<"a"> & { href: string };
/**
 * `responsive`(기본): lg 미만 가로 strip, lg 이상 세로 목록 — 0.2.2까지의 동작 그대로.
 * `vertical`: 모든 폭에서 세로 목록(AdminShell의 rail·drawer). `horizontal`: 모든 폭에서 가로 strip.
 */
export type AppMenuOrientation = "responsive" | "vertical" | "horizontal";
export interface AppMenuLayout { orientation?: AppMenuOrientation; compact?: boolean }
export interface AppMenuProps extends AppMenuLayout {
  groups: readonly AppMenuGroup[];
  pathname?: string;
  activeItemId?: string | null;
  label?: string;
  /** Next Link 등은 전달받은 anchor 속성과 children을 보존해야 한다. */
  linkComponent?: ComponentType<AppMenuLinkProps>;
  testId?: string;
}

/** AdminShell이 rail·drawer 안의 AppMenu에 배치를 알린다. AppMenu의 명시 prop이 우선한다. */
export const AppMenuLayoutContext = createContext<AppMenuLayout>({});

// Tailwind가 소비자 빌드에서 찾을 수 있도록 클래스는 완전한 문자열 리터럴로 둔다.
const layoutClasses = {
  responsive: {
    nav: "flex min-w-0 max-w-full gap-4 overflow-x-auto p-1 font-kt-sans lg:flex-col lg:overflow-x-visible",
    group: "shrink-0 lg:shrink lg:min-w-0",
    list: "m-0 flex list-none gap-1 p-0 lg:flex-col",
    item: "lg:w-full",
    label: "whitespace-nowrap lg:whitespace-normal lg:break-words",
  },
  vertical: {
    nav: "flex min-w-0 max-w-full flex-col gap-4 p-1 font-kt-sans",
    group: "min-w-0",
    list: "m-0 flex list-none flex-col gap-1 p-0",
    item: "w-full",
    label: "min-w-0 whitespace-normal break-words",
  },
  horizontal: {
    nav: "flex min-w-0 max-w-full gap-4 overflow-x-auto p-1 font-kt-sans",
    group: "shrink-0",
    list: "m-0 flex list-none gap-1 p-0",
    item: "",
    label: "whitespace-nowrap",
  },
} as const;

function DisabledMenuLink({ label, title, className, children }: { label: string; title?: string; className: string; children: ReactNode }) {
  return (
    // react-doctor-disable-next-line react-doctor/prefer-tag-over-role -- 비활성 링크는 href·탭 정지 없이 링크의 비활성 의미만 보존한다.
    <span data-slot="app-menu-link" role="link" aria-disabled="true" aria-label={label} title={title} className={className}>{children}</span>
  );
}

export function AppMenu({ groups, pathname = "/", activeItemId, label = "주 메뉴", linkComponent, testId, orientation, compact }: AppMenuProps) {
  const id = useId();
  const layout = useContext(AppMenuLayoutContext);
  const resolvedOrientation = orientation ?? layout.orientation ?? "responsive";
  // 아이콘만 남기는 접힘은 세로 목록에서만 의미가 있다.
  const isCompact = (compact ?? layout.compact ?? false) && resolvedOrientation === "vertical";
  const classes = layoutClasses[resolvedOrientation];
  const Link = linkComponent ?? "a";
  const links = groups.flatMap(group => group.items).filter((item): item is AppMenuLinkItem => item.href !== undefined && !item.disabled);
  const active = activeItemId === undefined ? getActiveMenuItemId(links, pathname) : activeItemId;
  return <nav data-slot="app-menu" data-testid={testId} aria-label={label}
    data-orientation={orientation || layout.orientation ? resolvedOrientation : undefined} data-compact={isCompact ? "true" : undefined}
    className={classes.nav}>
    {groups.map((group, index) => <div key={group.id} data-slot="app-menu-group"
      className={classes.group}>
      {group.label ? <p id={`${id}-${index}`} data-slot="app-menu-group-label"
        className={isCompact ? "sr-only" : "mb-2 px-3 text-kt-xs font-semibold text-kt-text-secondary"}>{group.label}</p> : null}
      <ul aria-labelledby={group.label ? `${id}-${index}` : undefined}
        className={classes.list}>
        {group.items.map(item => {
          const selected = !item.disabled && item.href !== undefined && item.id === active;
          const className = `relative flex min-h-11 items-center gap-2 rounded-kt-control ${isCompact ? "justify-center px-0" : "px-3"} py-2 text-kt-sm no-underline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-kt-focus ${classes.item} ${selected
            ? "bg-kt-brand-tint font-semibold text-kt-text-primary before:absolute before:inset-y-2 before:left-0 before:w-0.5 before:bg-kt-brand"
            : "text-kt-text-secondary hover:bg-kt-surface-subtle"} ${item.disabled ? "cursor-not-allowed text-kt-text-disabled" : ""}`;
          // 접힘 상태에서도 접근성 이름은 라벨이며, 시각 사용자는 title로 라벨을 본다.
          const title = isCompact ? item.label : undefined;
          const children = isCompact
            ? <>{item.icon
              ? <span aria-hidden="true" className="shrink-0">{item.icon}</span>
              : <span aria-hidden="true" data-slot="app-menu-initial" className="shrink-0 font-semibold">{Array.from(item.label.trim())[0] ?? ""}</span>}
              <span className="sr-only">{item.label}</span></>
            : <>{item.icon ? <span aria-hidden="true" className="shrink-0">{item.icon}</span> : null}<span className={classes.label}>{item.label}</span>{item.hint ? <kbd aria-hidden="true" className="ml-auto text-kt-2xs">{item.hint}</kbd> : null}</>;
          return <li key={item.id} data-slot="app-menu-item">
            {item.href !== undefined ? item.disabled
              ? <DisabledMenuLink label={item.label} title={title} className={className}>{children}</DisabledMenuLink>
              : <Link data-slot="app-menu-link" href={item.href} aria-label={item.label} title={title} aria-current={selected ? "page" : undefined} className={className}>{children}</Link>
              : <button data-slot="app-menu-action" type="button" disabled={item.disabled} aria-label={item.label} title={title}
                onClick={item.onSelect} className={`${className} border-0 bg-transparent text-left`}>{children}</button>}
          </li>;
        })}
      </ul>
    </div>)}
  </nav>;
}
