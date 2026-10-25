// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"use client";
import { useRef, useState } from "react";
import { MapDetailOverlay, MapFilterBar, MapFilterField, MapFilterPanel, MapKindFilter, MapStage, MapTabPanel, MapTabs, MapViewTabs, MapWorkspace } from "@kor-travel/ui/map-controls";

/** 설치 산출물의 높이·키보드·스크롤 계약만 검증하며 실제 조회는 하지 않는다. */
export default function WorkspaceSmoke() {
  const [view, setView] = useState("map");
  const [selected, setSelected] = useState(true);
  const [state, setState] = useState("자료 없음");
  const trigger = useRef<HTMLButtonElement>(null);
  const detail = useRef<HTMLElement>(null);
  const stage = useRef<HTMLDivElement>(null);
  return <main className="workspace-smoke-route" style={{ height: "100dvh", display: "flex", flexDirection: "column", minHeight: 0, padding: 8, boxSizing: "border-box" }}>
    <h1 style={{ fontSize: 16, margin: "0 0 8px" }}>공용 지도 작업면</h1>
    <MapWorkspace expandable>
      <MapFilterPanel triggerRef={trigger} label="지도 필터 · 모든 종류 · 전체 데이터 출처 · 선택 조건 요약">
        <MapFilterBar>
          <MapKindFilter value={["station"]} options={[{ value: "station", label: "역", icon: <span aria-hidden="true">●</span> }, { value: "fuel", label: "주유소" }]} onToggle={() => undefined} />
          <MapFilterField label="데이터 출처" htmlFor="source"><select id="source" value={state} onChange={(event) => setState(event.target.value)}>{["자료 없음", "키 없음", "WebGL 불가", "조회 중"].map((value) => <option key={value}>{value}</option>)}</select></MapFilterField>
        </MapFilterBar>
      </MapFilterPanel>
      <MapTabs value={view} onValueChange={(value) => { if (typeof value === "string") setView(value); }}>
        <MapViewTabs count={0} viewport={null} />
        {["map", "list"].map((value) => <MapTabPanel key={value} value={value}>
          <MapStage ref={stage} tabIndex={-1} view={value === "map" ? "map" : "list"} summary={<div style={{ background: "var(--kt-surface-card)", padding: 4 }}>저장 관측 · 갱신 지연</div>}
            detail={selected ? <MapDetailOverlay ref={detail} header="선택 장소" collapsible onDismiss={() => { setSelected(false); (trigger.current?.getClientRects().length ? trigger.current : stage.current)?.focus(); }}>
              {Array.from({ length: 30 }, (_, index) => <p key={index}>상세 정보 {index + 1}</p>)}
            </MapDetailOverlay> : null}>
            {value === "map" ? <div style={{ background: "var(--kt-surface-subtle)", position: "relative" }}>
              <button style={{ position: "absolute", right: 4, top: 4 }} onClick={() => { setSelected(true); requestAnimationFrame(() => detail.current?.focus()); }}>확대</button>
              <span style={{ position: "absolute", left: 4, bottom: 4 }}>지도 출처</span><span>{state}</span>
            </div> : <div>{Array.from({ length: 100 }, (_, index) => <p key={index}>목록 {index + 1}</p>)}</div>}
          </MapStage>
        </MapTabPanel>)}
      </MapTabs>
    </MapWorkspace>
  </main>;
}
