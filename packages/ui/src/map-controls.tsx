// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
// Origin: kor-travel-map@974e2d025 packages/kor-travel-map-admin/frontend/src/app/features/features-client.tsx (GPL-3.0-or-later)
// Derived-From: FeatureMapToolbar·FeatureMapWorkspace 및 Map의 Base UI 탭 구성
// Modified: 2026-10-24 — 지도 엔진·도메인과 분리한 공용 필터·탭·상세 오버레이
"use client";

import { Tabs } from "@base-ui/react/tabs";
import { ListIcon, MapIcon, XIcon } from "lucide-react";
import type { ComponentProps, ReactNode } from "react";

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

export function MapDetailOverlay({ className = "", onDismiss, onKeyDown, ...props }: ComponentProps<"aside"> & { onDismiss?: () => void }) {
  return <aside {...props} className={`kt-map-detail ${className}`} tabIndex={-1} data-slot="map-detail-overlay" onKeyDown={(event) => {
    onKeyDown?.(event);
    if (!event.defaultPrevented && event.key === "Escape" && onDismiss) { event.preventDefault(); event.stopPropagation(); onDismiss(); }
  }} />;
}
