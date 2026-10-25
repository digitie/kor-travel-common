// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
// Origin: kor-travel-map@974e2d025 packages/kor-travel-map-admin/frontend/src/app/features/features-client.tsx (GPL-3.0-or-later)
// Derived-From: FeatureMapToolbar·FeatureMapWorkspace 및 Map의 Base UI 탭 구성
// Modified: 2026-10-25 — 기존 계약을 보존하고 남은 높이 작업면·접기·상세 슬롯 추가
"use client";

import { Tabs } from "@base-ui/react/tabs";
import { ChevronDownIcon, ChevronUpIcon, ListIcon, MapIcon, Maximize2Icon, Minimize2Icon, XIcon } from "lucide-react";
import { createContext, useContext, useEffect, useId, useImperativeHandle, useRef, useState, type ComponentProps, type ReactNode, type Ref, type RefObject } from "react";

const WorkspaceExpansion = createContext<{
  enabled: boolean; expanded: boolean; toggle: () => void; id: string; trigger: RefObject<HTMLButtonElement | null>;
} | null>(null);

/** 부모 route shell이 제공한 남은 높이를 탭과 작업면으로 전달한다. */
export function MapWorkspace({ className = "", expandable = false, id, onKeyDown, ref, tabIndex, ...props }: ComponentProps<"div"> & { expandable?: boolean }) {
  const generatedId = useId();
  const workspaceId = id ?? generatedId;
  const [localExpanded, setLocalExpanded] = useState(false);
  const expanded = expandable && localExpanded;
  const trigger = useRef<HTMLButtonElement>(null);
  const workspace = useRef<HTMLDivElement>(null);
  useImperativeHandle(ref, () => workspace.current!, []);
  const restoreFocus = useRef(false);
  const close = () => { restoreFocus.current = true; setLocalExpanded(false); };
  useEffect(() => {
    if (!expanded && restoreFocus.current) {
      restoreFocus.current = false;
      const candidates = [trigger.current, workspace.current?.querySelector<HTMLElement>('[role="tab"][aria-selected="true"]')];
      const target = candidates.find((element) => element?.getClientRects().length && getComputedStyle(element).visibility !== "hidden");
      (target ?? workspace.current)?.focus({ preventScroll: true });
    }
  }, [expanded]);
  return <WorkspaceExpansion.Provider value={{ enabled: expandable, expanded, id: workspaceId, trigger, toggle: () => {
    if (expanded) close(); else setLocalExpanded(true);
  } }}>
    <div {...props} ref={workspace} tabIndex={tabIndex ?? (expandable ? -1 : undefined)} id={workspaceId} className={`kt-map-workspace ${className}`} data-slot="map-workspace" data-expanded={expanded} onKeyDown={(event) => {
      onKeyDown?.(event);
      if (!event.defaultPrevented && event.key === "Escape" && expanded) {
        event.preventDefault(); event.stopPropagation(); close();
      }
    }} />
  </WorkspaceExpansion.Provider>;
}

/** 필터 값과 DOM은 보존하고 모바일에서만 기본 접힘을 적용한다. */
export function MapFilterPanel({ children, label = "지도 필터", expanded, onExpandedChange, triggerRef, className = "", ...props }: ComponentProps<"div"> & {
  label?: string; expanded?: boolean; onExpandedChange?: (expanded: boolean) => void; triggerRef?: Ref<HTMLButtonElement>;
}) {
  const [localExpanded, setLocalExpanded] = useState(false);
  const workspace = useContext(WorkspaceExpansion);
  const open = expanded ?? localExpanded;
  const id = useId();
  const trigger = useRef<HTMLButtonElement>(null);
  const body = useRef<HTMLDivElement>(null);
  const lastFilterFocus = useRef<Element | null>(null);
  useImperativeHandle(triggerRef, () => trigger.current!, []);
  useEffect(() => {
    const mobile = window.matchMedia("(max-width: 40rem), (max-height: 30rem)");
    const rememberFocus = (event: FocusEvent) => {
      if (event.target instanceof Element && (body.current?.contains(event.target) || trigger.current === event.target)) lastFilterFocus.current = event.target;
      else if (event.target !== document.body) lastFilterFocus.current = null;
    };
    const clearOutsidePointer = (event: PointerEvent) => {
      if (!(event.target instanceof Node) || (!body.current?.contains(event.target) && !trigger.current?.contains(event.target))) lastFilterFocus.current = null;
    };
    const restore = () => {
      const inside = body.current?.contains(document.activeElement);
      const lostOnHide = document.activeElement === document.body && lastFilterFocus.current?.isConnected;
      if (!open && mobile.matches && (inside || (lostOnHide && body.current?.contains(lastFilterFocus.current)))) {
        lastFilterFocus.current = null;
        trigger.current?.focus();
      } else if (!mobile.matches && (document.activeElement === trigger.current || (lostOnHide && lastFilterFocus.current === trigger.current))) {
        lastFilterFocus.current = null;
        const fields = body.current?.querySelectorAll<HTMLElement>('input:not([type="hidden"]), select, textarea, button, a[href], [tabindex]:not([tabindex="-1"])');
        const target = Array.from(fields ?? []).find((element) => !element.matches(":disabled") && element.getClientRects().length && getComputedStyle(element).visibility !== "hidden");
        (target ?? body.current)?.focus({ preventScroll: true });
      }
    };
    restore();
    document.addEventListener("focusin", rememberFocus);
    document.addEventListener("pointerdown", clearOutsidePointer, true);
    mobile.addEventListener("change", restore);
    return () => {
      document.removeEventListener("focusin", rememberFocus);
      document.removeEventListener("pointerdown", clearOutsidePointer, true);
      mobile.removeEventListener("change", restore);
    };
  }, [open]);
  return <div {...props} className={`kt-map-filter-panel ${className}`} data-slot="map-filter-panel" data-expanded={open}>
    <div className="kt-map-filter-header" data-slot="map-filter-header">
    <button ref={trigger} type="button" className="kt-map-filter-toggle" data-slot="map-filter-trigger" title={label} aria-expanded={open} aria-controls={id} onClick={() => {
      setLocalExpanded(!open); onExpandedChange?.(!open);
    }}><span className="kt-map-filter-toggle-label">{label}</span>{open ? <ChevronUpIcon aria-hidden="true" /> : <ChevronDownIcon aria-hidden="true" />}</button>
    {workspace?.enabled ? <button ref={workspace.trigger} type="button" className="kt-map-workspace-expand" data-slot="map-workspace-expand"
      aria-label={workspace.expanded ? "원래 화면으로" : "지도 크게 보기"} title={workspace.expanded ? "원래 화면으로" : "지도 크게 보기"}
      aria-expanded={workspace.expanded} aria-controls={workspace.id} onClick={workspace.toggle}>
      {workspace.expanded ? <Minimize2Icon aria-hidden="true" /> : <Maximize2Icon aria-hidden="true" />}
    </button> : null}
    </div>
    <div ref={body} id={id} tabIndex={-1} className="kt-map-filter-panel-body" data-slot="map-filter-panel-body">{children}</div>
  </div>;
}

/** 엔진·데이터 상태와 관계없이 높이를 소유하며 목록 스크롤은 한 곳에 둔다. */
export function MapStage({ children, view = "map", summary, detail, className = "", ...props }: ComponentProps<"div"> & {
  view?: "map" | "list"; summary?: ReactNode; detail?: ReactNode;
}) {
  const hasSummary = summary != null && typeof summary !== "boolean";
  const hasDetail = detail != null && typeof detail !== "boolean";
  return <div {...props} className={`kt-map-stage kt-map-workspace-stage ${className}`} data-slot="map-stage" data-view={view}>
    <div className="kt-map-stage-content" data-slot={view === "map" ? "map-stage-canvas" : "map-stage-list"}>{children}</div>
    {hasSummary || hasDetail ? <div className="kt-map-stage-overlays">
      {hasSummary ? <div className="kt-map-stage-summary" data-slot="map-stage-summary">{summary}</div> : null}
      {hasDetail ? <div className="kt-map-stage-detail" data-slot="map-stage-detail">{detail}</div> : null}
    </div> : null}
  </div>;
}

export function MapFilterBar({ className = "", ...props }: ComponentProps<"div">) {
  return <div {...props} className={`kt-map-filter-bar ${className}`} data-slot="map-filter-bar" />;
}

export function MapFilterField({ label, htmlFor, children, className = "" }: {
  label: string; htmlFor?: string; children: ReactNode; className?: string;
}) {
  return <div className={`kt-map-filter-field ${className}`} data-slot="map-filter-field">
    {htmlFor ? <label htmlFor={htmlFor}>{label}</label> : <span className="kt-map-filter-label">{label}</span>}
    {children}
  </div>;
}

export type MapKindOption = { value: string; label: string; icon?: ReactNode };

export function MapKindFilter({ options, value, onToggle, onReset, resetDisabled = false, resetTitle, label = "종류", ariaLabel = "종류 필터", testId }: {
  options: readonly MapKindOption[]; value: readonly string[];
  onToggle: (value: string) => void; onReset?: () => void;
  resetDisabled?: boolean; resetTitle?: string; label?: string; ariaLabel?: string; testId?: string;
}) {
  return <MapFilterField label={label} className="kt-map-kind-field">
    <div className="kt-map-kinds" role="group" aria-label={ariaLabel} data-testid={testId}>
      {options.map((option) => <button key={option.value} type="button" aria-pressed={value.includes(option.value)} onClick={() => onToggle(option.value)}>
        {option.icon}<span>{option.label}</span>
      </button>)}
      {onReset ? <button type="button" className="kt-map-kind-reset" disabled={resetDisabled} title={resetTitle} onClick={onReset}><XIcon aria-hidden="true" />초기화</button> : null}
    </div>
  </MapFilterField>;
}

export function MapTabs({ className = "", ...props }: Tabs.Root.Props) {
  return <Tabs.Root {...props} className={(state) => `kt-map-tabs ${typeof className === "function" ? className(state) ?? "" : className}`} data-slot="tabs" />;
}

export function MapTabPanel({ className = "", ...props }: Tabs.Panel.Props) {
  return <Tabs.Panel {...props} className={(state) => `kt-map-tab-panel ${typeof className === "function" ? className(state) ?? "" : className}`} data-slot="tabs-content" />;
}

export type MapViewportReadout = { longitude: number; latitude: number; zoom: number };

export function MapReadout({ viewport, count, status }: { viewport: MapViewportReadout | null; count?: number; status?: ReactNode }) {
  return <div className="kt-map-readout" role="status">
    {status ?? (count !== undefined ? <span className="kt-map-count">{count.toLocaleString("ko-KR")}건 표시</span> : null)}
    <span className="kt-map-coordinates">{viewport ? `center ${viewport.longitude.toFixed(4)}, ${viewport.latitude.toFixed(4)} · z ${viewport.zoom.toFixed(1)}` : "지도 로딩 중"}</span>
  </div>;
}

export function MapViewTabs({ viewport, count, status, listValue = "list", listLabel = "목록", ariaLabel = "보기 전환" }: {
  viewport: MapViewportReadout | null; count?: number; status?: ReactNode;
  listValue?: "list" | "table"; listLabel?: string; ariaLabel?: string;
}) {
  return <div className="kt-map-view-header">
    <Tabs.List className="kt-map-view-tabs" aria-label={ariaLabel} data-slot="tabs-list">
      <Tabs.Tab value="map" data-slot="tabs-trigger"><MapIcon aria-hidden="true" />지도</Tabs.Tab>
      <Tabs.Tab value={listValue} data-slot="tabs-trigger"><ListIcon aria-hidden="true" />{listLabel}</Tabs.Tab>
    </Tabs.List>
    <MapReadout viewport={viewport} count={count} status={status} />
  </div>;
}

export function MapDetailOverlay({ className = "", onDismiss, onKeyDown, header, children, collapsible = false, collapsed, onCollapsedChange, ...props }: ComponentProps<"aside"> & {
  onDismiss?: () => void; header?: ReactNode; collapsible?: boolean; collapsed?: boolean; onCollapsedChange?: (collapsed: boolean) => void;
}) {
  const [localCollapsed, setLocalCollapsed] = useState(false);
  const compact = collapsed ?? localCollapsed;
  const bodyId = useId();
  const body = useRef<HTMLDivElement>(null);
  const toggle = useRef<HTMLButtonElement>(null);
  useEffect(() => {
    if (collapsible && compact && body.current?.contains(document.activeElement)) toggle.current?.focus();
  }, [collapsible, compact]);
  return <aside {...props} className={`kt-map-detail ${header !== undefined ? "kt-map-detail-slotted" : ""} ${className}`} tabIndex={-1} data-slot="map-detail-overlay" onKeyDown={(event) => {
    onKeyDown?.(event);
    if (!event.defaultPrevented && event.key === "Escape" && onDismiss) { event.preventDefault(); event.stopPropagation(); onDismiss(); }
  }}>{header !== undefined ? <>
    <div className="kt-map-detail-header" data-slot="map-detail-header">
      <div className="kt-map-detail-heading">{header}</div>
      {collapsible ? <button ref={toggle} type="button" aria-label={compact ? "상세 펼치기" : "상세 접기"} aria-expanded={!compact} aria-controls={bodyId} onClick={() => {
        setLocalCollapsed(!compact); onCollapsedChange?.(!compact);
      }}>{compact ? <ChevronDownIcon aria-hidden="true" /> : <ChevronUpIcon aria-hidden="true" />}</button> : null}
      {onDismiss ? <button type="button" aria-label="상세 닫기" onClick={onDismiss}><XIcon aria-hidden="true" /></button> : null}
    </div>
    <div ref={body} id={bodyId} className="kt-map-detail-body" data-slot="map-detail-body" hidden={collapsible && compact}>{children}</div>
  </> : children}</aside>;
}
