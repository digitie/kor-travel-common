// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"use client";

import { createContext, useContext, useEffect, useLayoutEffect, useRef, useState, useSyncExternalStore } from "react";
import type { MouseEvent, ReactNode } from "react";
import { Dialog as DialogPrimitive } from "radix-ui";
import { MenuIcon, PanelLeftCloseIcon, PanelLeftOpenIcon, XIcon } from "lucide-react";
import { AppMenuLayoutContext } from "./app-menu.js";
import { cn } from "./utils.js";

/** "영역 - 페이지" 형식의 제목 문자열. document.title도 같은 함수로 맞출 수 있다. */
export function formatAdminTitle(area: string | null | undefined, page: string | null | undefined): string {
  const left = area?.trim() ?? "";
  const right = page?.trim() ?? "";
  if (!left) return right;
  if (!right || left === right) return left;
  return `${left} - ${right}`;
}

export interface AdminTitleContent {
  /** 영역(서비스) 이름. 예: "날씨". `title`과 함께 "날씨 - 날씨지도"로 표시한다. */
  area?: string;
  /** 페이지 이름 또는 이미 합친 제목. 예: "날씨지도" 또는 "날씨 - 날씨지도". */
  title?: string;
  /** 제목 옆의 작은 설명. 좁은 폭에서는 말줄임하고 전체 문자열은 title 속성으로 제공한다. */
  description?: ReactNode;
  /** description이 문자열이 아닐 때 title 속성에 쓸 전체 문자열. */
  descriptionTitle?: string;
  /** 상단 바 오른쪽 동작 영역. */
  actions?: ReactNode;
}

export interface AdminTopBarProps extends AdminTitleContent {
  /** 제목 앞에 둘 요소. AdminShell은 모바일 메뉴 버튼을 넣는다. */
  leading?: ReactNode;
  className?: string;
  testId?: string;
}

/** 페이지 제목·설명·동작을 한 줄(약 48px)에 담는 상단 바. 페이지 h1은 여기서만 만든다. */
export function AdminTopBar({ area, title, description, descriptionTitle, actions, leading, className, testId }: AdminTopBarProps) {
  const page = title?.trim() ?? "";
  const zone = area?.trim() ?? "";
  const fullTitle = formatAdminTitle(zone, page);
  const showArea = zone !== "" && page !== "" && zone !== page;
  const descriptionText = descriptionTitle ?? (typeof description === "string" || typeof description === "number" ? String(description) : undefined);
  const hasDescription = description !== undefined && description !== null && description !== false && description !== "";
  return <header data-slot="admin-shell-header" data-testid={testId}
    className={cn("sticky top-0 z-kt-nav flex min-h-12 shrink-0 items-center gap-2 border-b border-kt-border bg-kt-surface-card px-2 pt-[env(safe-area-inset-top)] font-kt-sans text-kt-text-primary lg:px-4", className)}>
    {leading}
    <div data-slot="admin-shell-heading" className="flex min-w-0 flex-1 items-baseline gap-2">
      {fullTitle ? <h1 data-slot="admin-shell-title" title={fullTitle}
        className="m-0 min-w-0 shrink truncate text-kt-md font-semibold">
        {showArea ? <><span data-slot="admin-shell-area" className="font-medium text-kt-text-secondary">{zone}</span> - {page}</> : fullTitle}
      </h1> : null}
      {hasDescription ? <p data-slot="admin-shell-description" title={descriptionText}
        className="m-0 min-w-0 flex-1 basis-0 truncate text-kt-2xs text-kt-text-secondary">{description}</p> : null}
    </div>
    {actions ? <div data-slot="admin-shell-actions" className="ml-auto flex shrink-0 items-center gap-1">{actions}</div> : null}
  </header>;
}

type TitleRegistrar = (token: object, content: AdminTitleContent | null) => void;
const AdminShellTitleContext = createContext<TitleRegistrar | null>(null);
const useIsomorphicLayoutEffect = typeof window === "undefined" ? useEffect : useLayoutEffect;

export type AdminPageTitleProps = AdminTitleContent;

/**
 * 레이아웃에 둔 AdminShell의 상단 바 제목을 페이지에서 바꾼다. 지정한 필드만 덮어쓰고,
 * 페이지를 벗어나면 셸의 기본값으로 돌아간다. AdminShell 밖에서는 AdminTopBar를 직접 그린다.
 * 서버 렌더 첫 화면에도 제목이 필요하면 셸 prop(`area`·`title`)에 nav 정본의 라벨을 함께 준다.
 */
export function AdminPageTitle({ area, title, description, descriptionTitle, actions }: AdminPageTitleProps) {
  const register = useContext(AdminShellTitleContext);
  const token = useRef<object>({});
  useIsomorphicLayoutEffect(() => {
    if (!register) return undefined;
    register(token.current, { area, title, description, descriptionTitle, actions });
    return undefined;
  }, [register, area, title, description, descriptionTitle, actions]);
  useIsomorphicLayoutEffect(() => {
    const current = token.current;
    return () => register?.(current, null);
  }, [register]);
  if (register) return null;
  return <AdminTopBar area={area} title={title} description={description} descriptionTitle={descriptionTitle} actions={actions} />;
}

export interface AdminShellLabels {
  openMenu: string;
  closeMenu: string;
  menu: string;
  skipToContent: string;
  collapseRail: string;
  expandRail: string;
}

const defaultLabels: AdminShellLabels = {
  openMenu: "메뉴 열기",
  closeMenu: "메뉴 닫기",
  menu: "메뉴",
  skipToContent: "본문으로 건너뛰기",
  collapseRail: "메뉴 접기",
  expandRail: "메뉴 펼치기",
};

function resolveLabels(overrides: Partial<AdminShellLabels> | undefined): AdminShellLabels {
  return {
    openMenu: overrides?.openMenu ?? defaultLabels.openMenu,
    closeMenu: overrides?.closeMenu ?? defaultLabels.closeMenu,
    menu: overrides?.menu ?? defaultLabels.menu,
    skipToContent: overrides?.skipToContent ?? defaultLabels.skipToContent,
    collapseRail: overrides?.collapseRail ?? defaultLabels.collapseRail,
    expandRail: overrides?.expandRail ?? defaultLabels.expandRail,
  };
}

export interface AdminShellSlotState {
  /** 데스크톱 rail이 아이콘만 남긴 상태인지. drawer 안에서는 항상 false. */
  collapsed: boolean;
  /** 모바일 drawer 안에서 그리는지. */
  inDrawer: boolean;
}
type ShellSlot = ReactNode | ((state: AdminShellSlotState) => ReactNode);

export interface AdminShellProps extends AdminTitleContent {
  /** 주 메뉴. 보통 `<AppMenu …/>`이며 rail과 drawer에서 세로 목록으로 그려진다. */
  menu: ReactNode;
  /** rail·drawer 맨 위의 서비스 표시(워드마크). 앱 설명 문구는 넣지 않는다. */
  brand?: ShellSlot;
  /** rail·drawer 맨 아래(로그아웃 등). */
  railFooter?: ShellSlot;
  /** 현재 경로 등 이동을 나타내는 값. 바뀌면 열린 drawer를 닫는다. */
  navigationKey?: string;
  /** 데스크톱 rail 접힘 버튼을 둔다(기본 true). */
  collapsible?: boolean;
  /** 접힘 상태를 저장할 localStorage 키. 예: "kor-travel-weather:sidebar-collapsed". */
  collapsedStorageKey?: string;
  defaultCollapsed?: boolean;
  /** 셸을 화면 높이에 고정하고 본문이 남은 높이를 채운다(지도 화면 등). */
  fillViewport?: boolean;
  mainId?: string;
  labels?: Partial<AdminShellLabels>;
  className?: string;
  railClassName?: string;
  drawerClassName?: string;
  mainClassName?: string;
  testId?: string;
  children?: ReactNode;
}

const LG_QUERY = "(min-width: 64rem)";
const ICON_BUTTON = "inline-flex size-11 shrink-0 items-center justify-center rounded-kt-control border-0 bg-transparent text-kt-icon hover:bg-kt-surface-subtle focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-kt-focus";

function renderSlot(slot: ShellSlot | undefined, state: AdminShellSlotState) {
  return typeof slot === "function" ? slot(state) : slot;
}

function definedFields(content: AdminTitleContent | null | undefined): AdminTitleContent {
  if (!content) return {};
  return Object.fromEntries(Object.entries(content).filter(([, value]) => value !== undefined)) as AdminTitleContent;
}

// 같은 탭의 다른 셸과 다른 탭(storage 이벤트)의 접힘 상태 변경을 함께 구독한다.
const collapseListeners = new Set<() => void>();
function subscribeCollapse(listener: () => void) {
  collapseListeners.add(listener);
  window.addEventListener("storage", listener);
  return () => {
    collapseListeners.delete(listener);
    window.removeEventListener("storage", listener);
  };
}
function readCollapsed(key: string | undefined): boolean | null {
  if (!key) return null;
  try {
    const stored = window.localStorage.getItem(key);
    if (stored === "true" || stored === "1") return true;
    if (stored === "false" || stored === "0") return false;
  } catch {
    // 저장소를 쓸 수 없으면 기본값을 쓴다.
  }
  return null;
}

/** 접힘 상태. 저장 키가 있으면 localStorage가 정본이고 서버 렌더·hydration은 기본값으로 시작한다. */
function useRailCollapse(storageKey: string | undefined, defaultCollapsed: boolean) {
  const [local, setLocal] = useState(defaultCollapsed);
  const stored = useSyncExternalStore(subscribeCollapse, () => readCollapsed(storageKey), () => null);
  const collapsed = storageKey ? stored ?? defaultCollapsed : local;
  const toggle = () => {
    const next = !collapsed;
    if (!storageKey) {
      setLocal(next);
      return;
    }
    try {
      // 기존 앱이 "1"/"0"으로 저장해 왔다면 같은 형식을 유지한다(PinVi 등).
      const numeric = /^[01]$/.test(window.localStorage.getItem(storageKey) ?? "");
      window.localStorage.setItem(storageKey, numeric ? (next ? "1" : "0") : (next ? "true" : "false"));
    } catch {
      setLocal(next);
    }
    collapseListeners.forEach(listener => listener());
  };
  return [collapsed, toggle] as const;
}

interface RailProps {
  brand?: ShellSlot;
  railFooter?: ShellSlot;
  menu: ReactNode;
  collapsible: boolean;
  collapsedStorageKey?: string;
  defaultCollapsed: boolean;
  labels: AdminShellLabels;
  className?: string;
}

function AdminShellRail({ brand, railFooter, menu, collapsible, collapsedStorageKey, defaultCollapsed, labels, className }: RailProps) {
  const [storedCollapsed, toggle] = useRailCollapse(collapsedStorageKey, defaultCollapsed);
  const collapsed = collapsible && storedCollapsed;
  const state: AdminShellSlotState = { collapsed, inDrawer: false };
  const toggleLabel = collapsed ? labels.expandRail : labels.collapseRail;
  return <aside data-slot="admin-shell-rail" data-collapsed={collapsed ? "true" : undefined}
    className={cn("sticky top-0 hidden h-dvh shrink-0 flex-col border-r border-kt-border bg-kt-surface-card lg:flex", collapsed ? "w-16" : "w-64", className)}>
    <div data-slot="admin-shell-brand" className={cn("flex min-h-12 shrink-0 items-center gap-1 border-b border-kt-border", collapsed ? "flex-col justify-center px-1 py-1" : "pr-1 pl-3")}>
      {/* 접힘 상태에서는 함수형 brand만 그린다(예: 아이콘 로고). 문자열·노드 brand는 숨긴다. */}
      {collapsed
        ? typeof brand === "function" ? <div className="flex min-w-0 justify-center">{brand(state)}</div> : null
        : <div className="min-w-0 flex-1 truncate text-kt-sm font-semibold">{renderSlot(brand, state)}</div>}
      {collapsible ? <button type="button" data-slot="admin-shell-collapse" onClick={toggle}
        aria-label={toggleLabel} aria-expanded={!collapsed} title={toggleLabel} className={ICON_BUTTON}>
        {collapsed ? <PanelLeftOpenIcon aria-hidden="true" className="size-4" /> : <PanelLeftCloseIcon aria-hidden="true" className="size-4" />}
      </button> : null}
    </div>
    <div data-slot="admin-shell-nav" className="min-h-0 flex-1 overflow-y-auto overscroll-contain px-2 py-3">
      <AppMenuLayoutContext value={collapsed ? COMPACT_VERTICAL : VERTICAL}>{menu}</AppMenuLayoutContext>
    </div>
    {railFooter ? <div data-slot="admin-shell-rail-footer" className="shrink-0 border-t border-kt-border p-2">{renderSlot(railFooter, state)}</div> : null}
  </aside>;
}

const VERTICAL = { orientation: "vertical", compact: false } as const;
const COMPACT_VERTICAL = { orientation: "vertical", compact: true } as const;
const DRAWER_STATE: AdminShellSlotState = { collapsed: false, inDrawer: true };

interface DrawerProps {
  brand?: ShellSlot;
  railFooter?: ShellSlot;
  menu: ReactNode;
  labels: AdminShellLabels;
  className?: string;
  onNavigate: () => void;
  onCloseAutoFocus: (event: Event) => void;
}

function AdminShellDrawer({ brand, railFooter, menu, labels, className, onNavigate, onCloseAutoFocus }: DrawerProps) {
  const closeOnNavigate = (event: MouseEvent<HTMLElement>) => {
    // next/link 등 클라이언트 라우터는 기본 동작을 막고 이동하므로 defaultPrevented로 거르지 않는다.
    if (event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    const target = event.target instanceof Element ? event.target.closest("a[href], [data-slot='app-menu-action']") : null;
    if (!target || (target instanceof HTMLAnchorElement && target.target && target.target !== "_self")) return;
    onNavigate();
  };
  return <DialogPrimitive.Portal>
    <DialogPrimitive.Overlay data-slot="admin-shell-drawer-overlay"
      className="fixed inset-0 z-kt-overlay bg-kt-overlay motion-safe:data-open:animate-in motion-safe:data-open:fade-in-0 motion-safe:data-closed:animate-out motion-safe:data-closed:fade-out-0 lg:hidden" />
    <DialogPrimitive.Content data-slot="admin-shell-drawer" aria-describedby={undefined} onClick={closeOnNavigate}
      onCloseAutoFocus={onCloseAutoFocus}
      className={cn("fixed inset-y-0 left-0 z-kt-modal flex w-[min(280px,84vw)] flex-col border-r border-kt-border bg-kt-surface-card pt-[env(safe-area-inset-top)] pb-[env(safe-area-inset-bottom)] font-kt-sans text-kt-text-primary shadow-[var(--kt-shadow-modal)] outline-none motion-safe:data-open:animate-in motion-safe:data-open:slide-in-from-left motion-safe:data-closed:animate-out motion-safe:data-closed:slide-out-to-left lg:hidden", className)}>
      <div data-slot="admin-shell-drawer-header" className="flex min-h-12 shrink-0 items-center gap-1 border-b border-kt-border pr-1 pl-3">
        <DialogPrimitive.Title className="sr-only">{labels.menu}</DialogPrimitive.Title>
        <div className="min-w-0 flex-1 truncate text-kt-sm font-semibold">{renderSlot(brand, DRAWER_STATE)}</div>
        <DialogPrimitive.Close asChild>
          <button type="button" data-slot="admin-shell-drawer-close" aria-label={labels.closeMenu} className={ICON_BUTTON}>
            <XIcon aria-hidden="true" className="size-5" />
          </button>
        </DialogPrimitive.Close>
      </div>
      <div data-slot="admin-shell-drawer-nav" className="min-h-0 flex-1 overflow-y-auto overscroll-contain px-2 py-3">
        <AppMenuLayoutContext value={VERTICAL}>{menu}</AppMenuLayoutContext>
      </div>
      {railFooter ? <div data-slot="admin-shell-drawer-footer" className="shrink-0 border-t border-kt-border p-2">{renderSlot(railFooter, DRAWER_STATE)}</div> : null}
    </DialogPrimitive.Content>
  </DialogPrimitive.Portal>;
}

/**
 * drawer 열림 상태. navigationKey가 바뀌면(이동하면) 렌더 중에 닫고, 닫힌 뒤 포커스를 본문으로 보낸다.
 * lg 이상으로 넓어지면 닫는다.
 */
function useDrawer(navigationKey: string | undefined) {
  const [drawer, setDrawer] = useState({ open: false, key: navigationKey, returnToMain: false });
  if (drawer.key !== navigationKey) {
    // 이동 직후 같은 렌더에서 닫는다(이전 경로로 돌아와도 다시 열리지 않는다).
    setDrawer({ open: false, key: navigationKey, returnToMain: drawer.open });
  }
  const open = drawer.open && drawer.key === navigationKey;
  const setOpen = (next: boolean) => setDrawer({ open: next, key: navigationKey, returnToMain: false });
  const closeForNavigation = () => setDrawer({ open: false, key: navigationKey, returnToMain: true });
  useEffect(() => {
    if (!open || typeof window.matchMedia !== "function") return undefined;
    const query = window.matchMedia(LG_QUERY);
    const close = () => {
      if (query.matches) setDrawer(current => ({ ...current, open: false, returnToMain: false }));
    };
    query.addEventListener("change", close);
    return () => query.removeEventListener("change", close);
  }, [open]);
  return { open, setOpen, closeForNavigation, returnToMain: drawer.returnToMain };
}

/**
 * 관리자 화면 공통 셸. 데스크톱(lg 이상)은 좌측 rail(16rem, 접힘 4rem), 그 아래는 상단 바의
 * 메뉴 버튼으로 여는 좌측 drawer다. 페이지 제목·설명·동작은 한 줄 상단 바에 둔다.
 */
export function AdminShell({
  menu, brand, railFooter, navigationKey, collapsible = true, collapsedStorageKey, defaultCollapsed = false,
  fillViewport = false, mainId = "main-content", labels: labelOverrides, className, railClassName, drawerClassName,
  mainClassName, testId, children, area, title, description, descriptionTitle, actions,
}: AdminShellProps) {
  const labels = resolveLabels(labelOverrides);
  const { open, setOpen, closeForNavigation, returnToMain } = useDrawer(navigationKey);
  const [pageTitle, setPageTitle] = useState<{ token: object; content: AdminTitleContent } | null>(null);
  const [register] = useState<TitleRegistrar>(() => (token: object, content: AdminTitleContent | null) => setPageTitle(previous => {
    if (content) return { token, content };
    return previous?.token === token ? null : previous;
  }));
  const mainRef = useRef<HTMLElement>(null);

  const handleCloseAutoFocus = (event: Event) => {
    if (!returnToMain) return;
    event.preventDefault();
    mainRef.current?.focus({ preventScroll: true });
  };

  const content = { area, title, description, descriptionTitle, actions, ...definedFields(pageTitle?.content) };

  return <AdminShellTitleContext value={register}>
    <DialogPrimitive.Root open={open} onOpenChange={setOpen}>
      <div data-slot="admin-shell" data-testid={testId}
        className={cn("flex min-h-dvh bg-kt-surface-page font-kt-sans text-kt-text-primary", fillViewport && "h-dvh overflow-hidden", className)}>
        <a data-slot="admin-shell-skip-link" href={`#${mainId}`}
          className="sr-only focus:not-sr-only focus:fixed focus:top-2 focus:left-2 focus:z-kt-toast focus:rounded-kt-control focus:bg-kt-surface-card focus:p-3 focus:text-kt-sm focus:text-kt-text-primary focus:shadow-[var(--kt-shadow-elevated)]">
          {labels.skipToContent}
        </a>
        <AdminShellRail brand={brand} railFooter={railFooter} menu={menu} collapsible={collapsible}
          collapsedStorageKey={collapsedStorageKey} defaultCollapsed={defaultCollapsed} labels={labels} className={railClassName} />
        <div data-slot="admin-shell-body" className={cn("flex min-w-0 flex-1 flex-col", fillViewport && "min-h-0")}>
          <AdminTopBar {...content} leading={<DialogPrimitive.Trigger asChild>
            <button type="button" data-slot="admin-shell-menu-button" aria-label={labels.openMenu} className={cn(ICON_BUTTON, "-ml-1 lg:hidden")}>
              <MenuIcon aria-hidden="true" className="size-5" />
            </button>
          </DialogPrimitive.Trigger>} />
          <main id={mainId} ref={mainRef} tabIndex={-1} data-slot="admin-shell-main"
            className={cn("min-w-0 flex-1 outline-none", fillViewport && "min-h-0 overflow-hidden", mainClassName)}>
            {children}
          </main>
        </div>
      </div>
      <AdminShellDrawer brand={brand} railFooter={railFooter} menu={menu} labels={labels} className={drawerClassName}
        onNavigate={closeForNavigation} onCloseAutoFocus={handleCloseAutoFocus} />
    </DialogPrimitive.Root>
  </AdminShellTitleContext>;
}
