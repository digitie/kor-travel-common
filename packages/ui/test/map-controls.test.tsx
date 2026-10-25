// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
import { createRef, useState } from "react";
import { act, fireEvent, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { MapDetailOverlay, MapFilterPanel, MapKindFilter, MapReadout, MapStage, MapTabPanel, MapTabs, MapViewTabs, MapWorkspace } from "../src/map-controls.js";

describe("공용 지도 컨트롤", () => {
  beforeEach(() => vi.stubGlobal("matchMedia", vi.fn(() => ({ matches: true, addEventListener: vi.fn(), removeEventListener: vi.fn() }))));
  afterEach(() => vi.unstubAllGlobals());
  it("기본 작업면은 확장 UI를 추가하지 않는다", () => {
    const { container } = render(<MapWorkspace><MapFilterPanel>기존 필터</MapFilterPanel></MapWorkspace>);
    expect(screen.queryByRole("button", { name: "지도 크게 보기" })).toBeNull();
    expect(container.querySelector('[data-slot="map-workspace"]')).toHaveAttribute("data-expanded", "false");
  });

  it("명시 확장은 DOM·조건을 유지하고 Escape 뒤 확장 버튼으로 초점을 돌린다", async () => {
    const { container } = render(<MapWorkspace expandable id="map-work"><MapFilterPanel><input aria-label="조건" defaultValue="서울" /></MapFilterPanel><MapStage>지도</MapStage></MapWorkspace>);
    const field = screen.getByRole("textbox");
    const stage = container.querySelector('[data-slot="map-stage"]');
    const expand = screen.getByRole("button", { name: "지도 크게 보기" });
    vi.spyOn(expand, "getClientRects").mockReturnValue([{}] as unknown as DOMRectList);
    expect(expand).toHaveAttribute("aria-controls", "map-work");
    await userEvent.click(expand);
    expect(container.querySelector('[data-slot="map-workspace"]')).toHaveAttribute("data-expanded", "true");
    expect(screen.getByRole("button", { name: "원래 화면으로" })).toHaveAttribute("aria-expanded", "true");
    field.focus();
    await userEvent.keyboard("{Escape}");
    expect(expand).toHaveFocus();
    expect(expand).toHaveAttribute("aria-expanded", "false");
    expect(screen.getByRole("textbox")).toBe(field);
    expect(field).toHaveValue("서울");
    expect(container.querySelector('[data-slot="map-stage"]')).toBe(stage);
  });

  it("넓은 화면에서 복귀 버튼이 숨으면 초점을 작업면으로 돌린다", async () => {
    const { container } = render(<MapWorkspace expandable><MapFilterPanel /><button>지도 작업</button></MapWorkspace>);
    await userEvent.click(screen.getByRole("button", { name: "지도 크게 보기" }));
    fireEvent.keyDown(screen.getByRole("button", { name: "지도 작업" }), { key: "Escape" });
    expect(container.querySelector('[data-slot="map-workspace"]')).toHaveFocus();
  });

  it("상세와 자식 팝업이 처리한 Escape는 작업면 확장을 유지한다", async () => {
    const dismiss = vi.fn();
    const { container } = render(<MapWorkspace expandable><MapFilterPanel /><MapDetailOverlay onDismiss={dismiss}><button>상세</button></MapDetailOverlay><button onKeyDown={(event) => { if (event.key === "Escape") event.preventDefault(); }}>팝업</button></MapWorkspace>);
    await userEvent.click(screen.getByRole("button", { name: "지도 크게 보기" }));
    fireEvent.keyDown(screen.getByRole("button", { name: "상세", exact: true }), { key: "Escape" });
    expect(dismiss).toHaveBeenCalledOnce();
    expect(container.querySelector('[data-slot="map-workspace"]')).toHaveAttribute("data-expanded", "true");
    fireEvent.keyDown(screen.getByRole("button", { name: "팝업" }), { key: "Escape" });
    expect(container.querySelector('[data-slot="map-workspace"]')).toHaveAttribute("data-expanded", "true");
  });
  it("작업면은 데이터·지도 초기화에 의존하지 않고 빈 작업면과 요약·상세를 유지한다", () => {
    const { container, rerender } = render(<MapWorkspace><MapStage summary="관측 기준" detail={<MapDetailOverlay>선택 상세</MapDetailOverlay>}>키 없음</MapStage></MapWorkspace>);
    expect(container.querySelector('[data-slot="map-stage-canvas"]')).toHaveTextContent("키 없음");
    expect(container.querySelector('[data-slot="map-stage-summary"]')).toHaveTextContent("관측 기준");
    rerender(<MapWorkspace><MapStage view="list">저장 자료 없음</MapStage></MapWorkspace>);
    expect(container.querySelector('[data-slot="map-stage-list"]')).toHaveTextContent("저장 자료 없음");
  });

  it("접힌 필터는 값을 보존하고 외부에서 버튼으로 포커스를 돌릴 수 있다", async () => {
    const trigger = createRef<HTMLButtonElement>();
    const changed = vi.fn();
    const { container } = render(<MapFilterPanel triggerRef={trigger} onExpandedChange={changed}><input aria-label="검색" defaultValue="서울" /></MapFilterPanel>);
    expect(trigger.current).toHaveAttribute("aria-expanded", "false");
    await userEvent.click(trigger.current!);
    expect(changed).toHaveBeenLastCalledWith(true);
    expect(document.getElementById(trigger.current!.getAttribute("aria-controls")!)).toContainElement(screen.getByRole("textbox"));
    await userEvent.click(trigger.current!);
    expect(container.querySelector("input")).toHaveValue("서울");
    trigger.current!.focus();
    expect(trigger.current).toHaveFocus();
  });

  it("외부 필터 펼침 상태는 콜백만 전달하고 임의로 바꾸지 않는다", async () => {
    const changed = vi.fn();
    render(<MapFilterPanel expanded onExpandedChange={changed}>조건</MapFilterPanel>);
    await userEvent.click(screen.getByRole("button"));
    expect(changed).toHaveBeenCalledWith(false);
    expect(screen.getByRole("button")).toHaveAttribute("aria-expanded", "true");
  });

  it("외부에서 모바일 필터를 접으면 숨은 입력의 초점을 보이는 버튼으로 돌린다", () => {
    const { rerender } = render(<MapFilterPanel expanded><input aria-label="검색" /></MapFilterPanel>);
    screen.getByRole("textbox").focus();
    rerender(<MapFilterPanel expanded={false}><input aria-label="검색" /></MapFilterPanel>);
    expect(screen.getByRole("button")).toHaveFocus();
  });

  it("짧은 가로 화면으로 전환되어 입력이 숨으면 필터 버튼으로 초점을 돌린다", () => {
    let change = () => {};
    const media = { matches: false, addEventListener: (_: string, listener: () => void) => { change = listener; }, removeEventListener: vi.fn() };
    vi.stubGlobal("matchMedia", vi.fn(() => media));
    render(<MapFilterPanel><input aria-label="검색" /></MapFilterPanel>);
    screen.getByRole("textbox").focus();
    media.matches = true;
    act(() => change());
    expect(screen.getByRole("button")).toHaveFocus();
  });

  it("외부에서 상세를 접으면 본문의 초점을 접기 버튼으로 돌린다", () => {
    const { rerender } = render(<MapDetailOverlay header="상세" collapsible collapsed={false}><input aria-label="본문 입력" /></MapDetailOverlay>);
    screen.getByRole("textbox").focus();
    rerender(<MapDetailOverlay header="상세" collapsible collapsed><input aria-label="본문 입력" /></MapDetailOverlay>);
    expect(screen.getByRole("button", { name: "상세 펼치기" })).toHaveFocus();
  });

  it("선택적 상세 header의 접기·펼치기·닫기가 본문 값과 Escape 계약을 보존한다", async () => {
    const dismiss = vi.fn();
    render(<MapDetailOverlay header="서울역" collapsible onDismiss={dismiss}><input aria-label="상세 메모" defaultValue="보존" /></MapDetailOverlay>);
    await userEvent.click(screen.getByRole("button", { name: "상세 접기" }));
    expect(screen.getByRole("button", { name: "상세 펼치기" })).toHaveAttribute("aria-expanded", "false");
    expect(screen.queryByRole("textbox")).toBeNull();
    await userEvent.click(screen.getByRole("button", { name: "상세 펼치기" }));
    expect(screen.getByRole("textbox")).toHaveValue("보존");
    await userEvent.click(screen.getByRole("button", { name: "상세 닫기" }));
    expect(dismiss).toHaveBeenCalledOnce();
  });

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
