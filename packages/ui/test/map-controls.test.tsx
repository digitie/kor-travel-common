// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
import { useState } from "react";
import { fireEvent, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";
import { MapDetailOverlay, MapKindFilter, MapReadout, MapTabPanel, MapTabs, MapViewTabs } from "../src/map-controls.js";

describe("공용 지도 컨트롤", () => {
  it("아이콘과 종류 이름을 함께 표시하고 다중 선택·초기화를 전달한다", async () => {
    const toggle = vi.fn();
    const reset = vi.fn();
    render(<MapKindFilter options={[{ value: "rail", label: "철도역", icon: <svg data-testid="rail-icon" aria-hidden="true" /> }, { value: "port", label: "항구" }]} value={["rail"]} onToggle={toggle} onReset={reset} />);
    expect(screen.getByTestId("rail-icon")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "철도역" })).toHaveAttribute("aria-pressed", "true");
    expect(screen.getByRole("button", { name: "항구" })).toHaveAttribute("aria-pressed", "false");
    await userEvent.click(screen.getByRole("button", { name: "항구" }));
    expect(toggle).toHaveBeenCalledWith("port");
    await userEvent.click(screen.getByRole("button", { name: "초기화" }));
    expect(reset).toHaveBeenCalledOnce();
  });

  it("탭을 키보드로 전환하며 연결된 패널과 좌표를 유지한다", async () => {
    function Example() {
      const [view, setView] = useState<"map" | "list">("map");
      return <MapTabs value={view} onValueChange={(value) => { if (value === "map" || value === "list") setView(value); }}>
        <MapViewTabs count={12} viewport={{ longitude: 128.5316, latitude: 37.6031, zoom: 16.1 }} />
        <MapTabPanel value="map">지도 내용</MapTabPanel><MapTabPanel value="list">목록 내용</MapTabPanel>
      </MapTabs>;
    }
    render(<Example />);
    const map = screen.getByRole("tab", { name: "지도" });
    map.focus();
    await userEvent.keyboard("{ArrowRight}");
    expect(screen.getByRole("tab", { name: "목록" })).toHaveFocus();
    await userEvent.keyboard("{Enter}");
    expect(screen.getByRole("tab", { name: "목록" })).toHaveAttribute("aria-selected", "true");
    expect(screen.getByRole("tabpanel")).toHaveTextContent("목록 내용");
    expect(screen.getByRole("status")).toHaveTextContent("12건 표시");
    expect(screen.getByRole("status")).toHaveTextContent("center 128.5316, 37.6031 · z 16.1");
  });

  it("아직 읽지 않은 지도 좌표를 확정값으로 표시하지 않는다", () => {
    render(<MapReadout viewport={null} status="조회 중…" />);
    expect(screen.getByRole("status")).toHaveTextContent("조회 중…지도 로딩 중");
    expect(screen.getByRole("status")).not.toHaveTextContent("center");
  });

  it("상세 안의 Escape만 닫기로 전달한다", () => {
    const dismiss = vi.fn();
    render(<MapDetailOverlay aria-label="선택 장소 상세" onDismiss={dismiss}><button>상세 작업</button></MapDetailOverlay>);
    fireEvent.keyDown(screen.getByRole("button"), { key: "Escape" });
    expect(dismiss).toHaveBeenCalledOnce();
    fireEvent.keyDown(document.body, { key: "Escape" });
    expect(dismiss).toHaveBeenCalledOnce();
  });
});
