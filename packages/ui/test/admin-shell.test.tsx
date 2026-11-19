// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
import { useState } from "react";
import { act, render, screen, waitFor, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";
import axe from "axe-core";
import { AdminPageTitle, AdminShell, AdminTopBar, AppMenu, formatAdminTitle } from "../src/index.js";
import type { AppMenuGroup } from "../src/index.js";

const groups: AppMenuGroup[] = [{ id: "ops", label: "운영", items: [
  { id: "home", label: "홈", href: "/" },
  { id: "map", label: "날씨지도", href: "/weather" },
  { id: "jobs", label: "작업", href: "/jobs", icon: <svg data-testid="jobs-icon" /> },
] }];
const menu = (pathname = "/weather") => <AppMenu groups={groups} pathname={pathname} />;
const axeRun = (node: Element) => axe.run(node, { rules: { "color-contrast": { enabled: false } } });

afterEach(() => { window.localStorage.clear(); });

describe("formatAdminTitle", () => {
  it("영역 - 페이지 형식으로 합치고 빈 값·중복을 정리한다", () => {
    expect(formatAdminTitle("날씨", "날씨지도")).toBe("날씨 - 날씨지도");
    expect(formatAdminTitle(" 날씨 ", "")).toBe("날씨");
    expect(formatAdminTitle(undefined, "날씨 - 날씨지도")).toBe("날씨 - 날씨지도");
    expect(formatAdminTitle("날씨", "날씨")).toBe("날씨");
    expect(formatAdminTitle(null, null)).toBe("");
  });
});

describe("AppMenu 배치", () => {
  it("기본 반응형 클래스와 DOM은 0.2.2와 같다", () => {
    render(menu());
    const nav = screen.getByRole("navigation");
    expect(nav).toHaveClass("overflow-x-auto", "lg:flex-col", "lg:overflow-x-visible");
    expect(nav).not.toHaveAttribute("data-orientation");
    expect(nav.querySelector("ul")).toHaveClass("lg:flex-col");
    expect(screen.getByRole("link", { name: "날씨지도" })).not.toHaveAttribute("title");
  });

  it("vertical은 모든 폭에서 세로 목록이고 compact는 라벨을 접근성 이름·title로만 남긴다", async () => {
    const { rerender, container } = render(<AppMenu groups={groups} pathname="/jobs" orientation="vertical" />);
    const nav = screen.getByRole("navigation");
    expect(nav).toHaveAttribute("data-orientation", "vertical");
    expect(nav).toHaveClass("flex-col");
    expect(nav).not.toHaveClass("overflow-x-auto");
    rerender(<AppMenu groups={groups} pathname="/jobs" orientation="vertical" compact />);
    const jobs = screen.getByRole("link", { name: "작업" });
    expect(jobs).toHaveAttribute("title", "작업");
    expect(jobs).toHaveAttribute("aria-current", "page");
    expect(within(jobs).getByText("작업")).toHaveClass("sr-only");
    expect(screen.getByText("운영")).toHaveClass("sr-only");
    // 아이콘이 없는 항목은 첫 글자를 시각 표지로 쓴다.
    expect(container.querySelector('[data-slot="app-menu-initial"]')).toHaveTextContent("홈");
    expect((await axeRun(container)).violations).toEqual([]);
  });

  it("compact는 vertical에서만 적용되고 명시 prop이 셸 배치보다 우선한다", () => {
    render(<AppMenu groups={groups} orientation="horizontal" compact />);
    expect(screen.getByRole("navigation")).not.toHaveAttribute("data-compact");
    expect(screen.getByRole("link", { name: "홈" })).not.toHaveAttribute("title");
  });
});

describe("AdminTopBar", () => {
  it("영역 - 페이지 h1과 작은 설명을 한 줄에 두고 전체 문자열을 title로 제공한다", () => {
    render(<AdminTopBar area="날씨" title="날씨지도" description="활성 위치 카탈로그 12곳" actions={<button type="button">새로고침</button>} />);
    const heading = screen.getByRole("heading", { level: 1 });
    expect(heading).toHaveTextContent("날씨 - 날씨지도");
    expect(heading).toHaveAttribute("title", "날씨 - 날씨지도");
    expect(heading).toHaveClass("truncate");
    const description = screen.getByText("활성 위치 카탈로그 12곳");
    expect(description).toHaveAttribute("title", "활성 위치 카탈로그 12곳");
    expect(description).toHaveClass("truncate", "text-kt-2xs");
    expect(screen.getByRole("button", { name: "새로고침" }).closest('[data-slot="admin-shell-actions"]')).not.toBeNull();
  });

  it("문자열이 아닌 설명은 descriptionTitle을 title로 쓴다", () => {
    render(<AdminTopBar title="날씨 - 날씨지도" description={<strong>12곳</strong>} descriptionTitle="활성 위치 12곳" />);
    expect(screen.getByRole("heading", { level: 1 })).toHaveTextContent("날씨 - 날씨지도");
    expect(document.querySelector('[data-slot="admin-shell-description"]')).toHaveAttribute("title", "활성 위치 12곳");
  });
});

describe("AdminShell", () => {
  it("상단 바 제목·rail·메뉴 버튼과 접근성 위반 없음", async () => {
    const { container } = render(<AdminShell area="날씨" title="날씨지도" description="활성 위치 카탈로그 12곳" brand="날씨" menu={menu()}>
      <p>본문</p>
    </AdminShell>);
    expect(screen.getByRole("heading", { level: 1 })).toHaveTextContent("날씨 - 날씨지도");
    const trigger = screen.getByRole("button", { name: "메뉴 열기" });
    expect(trigger).toHaveAttribute("aria-expanded", "false");
    expect(trigger).toHaveAttribute("aria-haspopup", "dialog");
    expect(trigger).toHaveClass("lg:hidden");
    const rail = container.querySelector('[data-slot="admin-shell-rail"]')!;
    expect(rail).toHaveClass("hidden", "lg:flex", "w-64");
    expect(within(rail as HTMLElement).getByRole("navigation")).toHaveAttribute("data-orientation", "vertical");
    expect(screen.getByRole("link", { name: "본문으로 건너뛰기" })).toHaveAttribute("href", "#main-content");
    expect(screen.getByRole("main")).toHaveAttribute("id", "main-content");
    expect((await axeRun(container)).violations).toEqual([]);
  });

  it("모바일 drawer는 좌측 dialog로 열리고 Esc로 닫히며 포커스를 메뉴 버튼으로 돌려준다", async () => {
    const user = userEvent.setup();
    render(<AdminShell title="날씨 - 날씨지도" brand="날씨" menu={menu()}><p>본문</p></AdminShell>);
    const trigger = screen.getByRole("button", { name: "메뉴 열기" });
    await user.click(trigger);
    const drawer = screen.getByRole("dialog", { name: "메뉴" });
    expect(trigger).toHaveAttribute("aria-expanded", "true");
    expect(trigger).toHaveAttribute("aria-controls", drawer.id);
    expect(drawer).toHaveAttribute("data-slot", "admin-shell-drawer");
    expect(drawer).toHaveClass("left-0", "motion-safe:data-open:slide-in-from-left");
    const nav = within(drawer).getByRole("navigation");
    expect(nav).toHaveAttribute("data-orientation", "vertical");
    expect(nav).not.toHaveAttribute("data-compact");
    expect(drawer.contains(document.activeElement)).toBe(true);
    expect((await axeRun(drawer)).violations).toEqual([]);
    await user.keyboard("{Escape}");
    await waitFor(() => expect(screen.queryByRole("dialog")).not.toBeInTheDocument());
    expect(trigger).toHaveFocus();
    expect(trigger).toHaveAttribute("aria-expanded", "false");
  });

  it("drawer의 링크를 누르면 닫고 본문으로 포커스를 옮기며 수정 키 클릭은 유지한다", async () => {
    const user = userEvent.setup();
    render(<AdminShell title="홈" menu={menu("/")}><p>본문</p></AdminShell>);
    const link = () => within(screen.getByRole("dialog")).getByRole("link", { name: "작업" });
    await user.click(screen.getByRole("button", { name: "메뉴 열기" }));
    link().addEventListener("click", event => event.preventDefault());
    await user.keyboard("{Control>}");
    await user.click(link());
    await user.keyboard("{/Control}");
    expect(screen.getByRole("dialog")).toBeInTheDocument();
    await user.click(link());
    await waitFor(() => expect(screen.queryByRole("dialog")).not.toBeInTheDocument());
    expect(screen.getByRole("main")).toHaveFocus();
  });

  it("navigationKey가 바뀌면 열린 drawer를 닫는다", async () => {
    const user = userEvent.setup();
    let navigate: (path: string) => void = () => {};
    function Harness() {
      const [path, setPath] = useState("/");
      navigate = setPath;
      return <AdminShell title="홈" navigationKey={path} menu={menu(path)}><p>{path}</p></AdminShell>;
    }
    render(<Harness />);
    await user.click(screen.getByRole("button", { name: "메뉴 열기" }));
    expect(screen.getByRole("dialog")).toBeInTheDocument();
    act(() => navigate("/jobs"));
    await waitFor(() => expect(screen.queryByRole("dialog")).not.toBeInTheDocument());
    expect(screen.getByRole("main")).toHaveFocus();
    // 이전 경로로 돌아와도 다시 열리지 않는다.
    act(() => navigate("/"));
    expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
    expect(screen.getByRole("button", { name: "메뉴 열기" })).toHaveAttribute("aria-expanded", "false");
    // 이동 뒤 직접 다시 열고 Esc로 닫으면 포커스는 메뉴 버튼으로 돌아간다.
    await user.click(screen.getByRole("button", { name: "메뉴 열기" }));
    await user.keyboard("{Escape}");
    await waitFor(() => expect(screen.queryByRole("dialog")).not.toBeInTheDocument());
    expect(screen.getByRole("button", { name: "메뉴 열기" })).toHaveFocus();
  });

  it("lg 이상이 되면 열린 drawer를 닫는다", async () => {
    const listeners = new Set<() => void>();
    const query = { matches: false, addEventListener: (_: string, fn: () => void) => listeners.add(fn), removeEventListener: (_: string, fn: () => void) => listeners.delete(fn) };
    const original = window.matchMedia;
    window.matchMedia = vi.fn().mockReturnValue(query) as unknown as typeof window.matchMedia;
    try {
      const user = userEvent.setup();
      render(<AdminShell title="홈" menu={menu("/")}><p>본문</p></AdminShell>);
      await user.click(screen.getByRole("button", { name: "메뉴 열기" }));
      expect(window.matchMedia).toHaveBeenCalledWith("(min-width: 64rem)");
      query.matches = true;
      act(() => listeners.forEach(fn => fn()));
      await waitFor(() => expect(screen.queryByRole("dialog")).not.toBeInTheDocument());
    } finally {
      window.matchMedia = original;
    }
  });

  it("데스크톱 rail을 아이콘으로 접고 상태를 저장·복원한다", async () => {
    const user = userEvent.setup();
    const key = "kor-travel-test:sidebar-collapsed";
    const { container, unmount } = render(<AdminShell title="홈" brand="날씨" collapsedStorageKey={key} menu={menu("/jobs")}
      railFooter={({ collapsed }) => <span>{collapsed ? "접힘" : "펼침"}</span>}><p>본문</p></AdminShell>);
    const rail = () => container.querySelector('[data-slot="admin-shell-rail"]') as HTMLElement;
    expect(within(rail()).getByText("펼침")).toBeInTheDocument();
    await user.click(screen.getByRole("button", { name: "메뉴 접기" }));
    expect(rail()).toHaveAttribute("data-collapsed", "true");
    expect(rail()).toHaveClass("w-16");
    expect(within(rail()).getByRole("navigation")).toHaveAttribute("data-compact", "true");
    expect(within(rail()).getByRole("link", { name: "작업" })).toHaveAttribute("title", "작업");
    expect(within(rail()).getByText("접힘")).toBeInTheDocument();
    expect(window.localStorage.getItem(key)).toBe("true");
    unmount();
    const second = render(<AdminShell title="홈" collapsedStorageKey={key} menu={menu()}><p>본문</p></AdminShell>);
    await waitFor(() => expect(second.container.querySelector('[data-slot="admin-shell-rail"]')).toHaveAttribute("data-collapsed", "true"));
    expect(screen.getByRole("button", { name: "메뉴 펼치기" })).toHaveAttribute("aria-expanded", "false");
  });

  it("기존 1/0 저장 형식을 유지하고 접힘에서는 함수형 brand만 그린다", async () => {
    const user = userEvent.setup();
    const key = "pinvi.admin.sidebar.collapsed";
    window.localStorage.setItem(key, "0");
    const { container } = render(<AdminShell title="대시보드" collapsedStorageKey={key} menu={menu()}
      brand={({ collapsed }) => <span>{collapsed ? "PA" : "Pinvi Admin"}</span>}><p>본문</p></AdminShell>);
    const rail = container.querySelector('[data-slot="admin-shell-rail"]') as HTMLElement;
    expect(within(rail).getByText("Pinvi Admin")).toBeInTheDocument();
    await user.click(within(rail).getByRole("button", { name: "메뉴 접기" }));
    expect(window.localStorage.getItem(key)).toBe("1");
    expect(within(rail).getByText("PA")).toBeInTheDocument();
  });

  it("localStorage가 막혀도 접힘 버튼이 동작한다", async () => {
    const user = userEvent.setup();
    const get = vi.spyOn(Storage.prototype, "getItem").mockImplementation(() => { throw new Error("blocked"); });
    const set = vi.spyOn(Storage.prototype, "setItem").mockImplementation(() => { throw new Error("blocked"); });
    try {
      const { container } = render(<AdminShell title="홈" collapsedStorageKey="blocked:sidebar" menu={menu()}><p>본문</p></AdminShell>);
      await user.click(screen.getByRole("button", { name: "메뉴 접기" }));
      expect(container.querySelector('[data-slot="admin-shell-rail"]')).toHaveAttribute("data-collapsed", "true");
    } finally {
      get.mockRestore();
      set.mockRestore();
    }
  });

  it("링크로 닫는 도중 경로가 바뀌어도 포커스는 본문으로 간다", async () => {
    const user = userEvent.setup();
    let navigate: (path: string) => void = () => {};
    function Harness() {
      const [path, setPath] = useState("/");
      navigate = setPath;
      return <AdminShell title="홈" navigationKey={path} menu={<AppMenu groups={groups} pathname={path}
        linkComponent={props => <a {...props} onClick={event => { event.preventDefault(); navigate(props.href); }} />} />}><p>{path}</p></AdminShell>;
    }
    render(<Harness />);
    await user.click(screen.getByRole("button", { name: "메뉴 열기" }));
    await user.click(within(screen.getByRole("dialog")).getByRole("link", { name: "작업" }));
    await waitFor(() => expect(screen.queryByRole("dialog")).not.toBeInTheDocument());
    expect(screen.getByText("/jobs")).toBeInTheDocument();
    expect(screen.getByRole("main")).toHaveFocus();
  });

  it("collapsible=false면 접힘 버튼이 없다", () => {
    render(<AdminShell title="홈" collapsible={false} menu={menu()} />);
    expect(screen.queryByRole("button", { name: "메뉴 접기" })).not.toBeInTheDocument();
  });

  it("AdminPageTitle은 셸 상단 바의 지정 필드만 바꾸고 떠나면 기본값으로 돌아간다", () => {
    function Page({ count }: { count: number }) {
      return <AdminPageTitle title="날씨지도" description={`활성 위치 카탈로그 ${count}곳`} actions={<button type="button">새로고침</button>} />;
    }
    const { rerender } = render(<AdminShell area="날씨" title="홈" menu={menu()}><Page count={3} /></AdminShell>);
    expect(screen.getAllByRole("heading", { level: 1 })).toHaveLength(1);
    expect(screen.getByRole("heading", { level: 1 })).toHaveTextContent("날씨 - 날씨지도");
    expect(screen.getByText("활성 위치 카탈로그 3곳")).toBeInTheDocument();
    rerender(<AdminShell area="날씨" title="홈" menu={menu()}><Page count={4} /></AdminShell>);
    expect(screen.getByText("활성 위치 카탈로그 4곳")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "새로고침" })).toBeInTheDocument();
    rerender(<AdminShell area="날씨" title="홈" menu={menu()}><p>다른 페이지</p></AdminShell>);
    expect(screen.getByRole("heading", { level: 1 })).toHaveTextContent("날씨 - 홈");
    expect(screen.queryByText(/활성 위치/)).not.toBeInTheDocument();
    expect(screen.queryByRole("button", { name: "새로고침" })).not.toBeInTheDocument();
  });

  it("AdminPageTitle은 셸 밖에서 상단 바를 직접 그린다", () => {
    render(<AdminPageTitle area="교통" title="노선" description="노선 120개" />);
    expect(screen.getByRole("heading", { level: 1 })).toHaveTextContent("교통 - 노선");
    expect(document.querySelector('[data-slot="admin-shell-header"]')).not.toBeNull();
  });

  it("fillViewport는 셸을 화면 높이에 고정하고 본문이 남은 높이를 채운다", () => {
    const { container } = render(<AdminShell title="지도" fillViewport mainClassName="p-0" menu={menu()}><p>지도</p></AdminShell>);
    expect(container.querySelector('[data-slot="admin-shell"]')).toHaveClass("h-dvh", "overflow-hidden");
    expect(screen.getByRole("main")).toHaveClass("min-h-0", "overflow-hidden", "p-0");
  });
});
