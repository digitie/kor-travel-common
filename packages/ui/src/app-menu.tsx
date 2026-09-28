// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"use client";

import { useId } from "react";
import type { ComponentType, ComponentPropsWithRef, ReactNode } from "react";
import { getActiveMenuItemId } from "./navigation.js";

interface MenuItemBase { id: string; label: string; icon?: ReactNode; hint?: string; disabled?: boolean }
export interface AppMenuLinkItem extends MenuItemBase { href: string; exact?: boolean; onSelect?: never }
export interface AppMenuActionItem extends MenuItemBase { href?: never; onSelect: () => void }
export type AppMenuItem = AppMenuLinkItem | AppMenuActionItem;
export interface AppMenuGroup { id: string; label?: string; items: readonly AppMenuItem[] }
export type AppMenuLinkProps = ComponentPropsWithRef<"a"> & { href: string };
export interface AppMenuProps {
  groups: readonly AppMenuGroup[];
  pathname?: string;
  activeItemId?: string | null;
  label?: string;
  /** Next Link 등은 전달받은 anchor 속성과 children을 보존해야 한다. */
  linkComponent?: ComponentType<AppMenuLinkProps>;
  testId?: string;
}

export function AppMenu({ groups, pathname = "/", activeItemId, label = "주 메뉴", linkComponent, testId }: AppMenuProps) {
  const id = useId();
  const Link = linkComponent ?? "a";
  const links = groups.flatMap(group => group.items).filter((item): item is AppMenuLinkItem => item.href !== undefined && !item.disabled);
  const active = activeItemId === undefined ? getActiveMenuItemId(links, pathname) : activeItemId;
  return <nav data-slot="app-menu" data-testid={testId} aria-label={label}
    className="flex min-w-0 max-w-full gap-4 overflow-x-auto p-1 font-kt-sans lg:flex-col lg:overflow-x-visible">
    {groups.map((group, index) => <div key={group.id} data-slot="app-menu-group"
      className="shrink-0 lg:shrink lg:min-w-0">
      {group.label ? <p id={`${id}-${index}`} data-slot="app-menu-group-label"
        className="mb-2 px-3 text-kt-xs font-semibold text-kt-text-secondary">{group.label}</p> : null}
      <ul aria-labelledby={group.label ? `${id}-${index}` : undefined}
        className="m-0 flex list-none gap-1 p-0 lg:flex-col">
        {group.items.map(item => {
          const selected = !item.disabled && item.href !== undefined && item.id === active;
          const className = `relative flex min-h-11 items-center gap-2 rounded-kt-control px-3 py-2 text-kt-sm no-underline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-kt-focus lg:w-full ${selected
            ? "bg-kt-brand-tint font-semibold text-kt-text-primary before:absolute before:inset-y-2 before:left-0 before:w-0.5 before:bg-kt-brand"
            : "text-kt-text-secondary hover:bg-kt-surface-subtle"} ${item.disabled ? "cursor-not-allowed text-kt-text-disabled" : ""}`;
          const children = <>{item.icon ? <span aria-hidden="true" className="shrink-0">{item.icon}</span> : null}<span className="whitespace-nowrap lg:whitespace-normal lg:break-words">{item.label}</span>{item.hint ? <kbd aria-hidden="true" className="ml-auto text-kt-2xs">{item.hint}</kbd> : null}</>;
          return <li key={item.id} data-slot="app-menu-item">
            {item.href !== undefined ? item.disabled
              ? <span data-slot="app-menu-link" role="link" aria-disabled="true" aria-label={item.label} className={className}>{children}</span>
              : <Link data-slot="app-menu-link" href={item.href} aria-label={item.label} aria-current={selected ? "page" : undefined} className={className}>{children}</Link>
              : <button data-slot="app-menu-action" type="button" disabled={item.disabled} aria-label={item.label}
                onClick={item.onSelect} className={`${className} border-0 bg-transparent text-left`}>{children}</button>}
          </li>;
        })}
      </ul>
    </div>)}
  </nav>;
}
