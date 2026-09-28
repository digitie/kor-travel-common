// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
import { act, fireEvent, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";
import axe from "axe-core";
import { LoginForm, LoginStatus, AppMenu } from "../src/index.js";

describe("로그인", () => {
  it("라벨·자동완성·오류 슬롯을 유지하고 비밀번호를 그대로 제출한다", async () => {
    const submit = vi.fn();
    const { container } = render(<LoginForm onSubmit={submit} nextPath="//outside.invalid" />);
    expect(screen.getByRole("alert")).toBeEmptyDOMElement();
    expect(screen.getByLabelText("아이디")).toHaveAttribute("autocomplete", "username");
    const field = screen.getByLabelText("비밀번호");
    const sample = " example ";
    expect(field).toHaveAttribute("autocomplete", "current-password");
    await userEvent.type(screen.getByLabelText("아이디"), "  demo  ");
    await userEvent.type(field, sample);
    await userEvent.click(screen.getByRole("button", { name: "로그인" }));
    expect(submit).toHaveBeenCalledWith({ credentials: { username: "demo", password: sample }, nextPath: "/" });
    expect(field).toHaveValue("");
    const results = await axe.run(container, { rules: { "color-contrast": { enabled: false } } });
    expect(results.violations).toEqual([]);
  });
  it("같은 틱의 제출과 pending 재제출을 막으며 포커스를 유지한다", async () => {
    let finish!: () => void;
    const submit = vi.fn(() => new Promise<void>(resolve => { finish = resolve; }));
    const { container } = render(<LoginForm onSubmit={submit} />);
    await userEvent.type(screen.getByLabelText("아이디"), "demo");
    await userEvent.type(screen.getByLabelText("비밀번호"), "example");
    const button = screen.getByRole("button", { name: "로그인" });
    button.focus();
    fireEvent.submit(container.querySelector("form")!);
    fireEvent.submit(container.querySelector("form")!);
    expect(submit).toHaveBeenCalledTimes(1);
    expect(button).toHaveFocus();
    expect(button).not.toBeDisabled();
    expect(button).toHaveAttribute("aria-disabled", "true");
    await act(async () => finish());
    expect(button).toHaveAttribute("aria-disabled", "false");
  });
  it("외부 pending도 제출을 막는다", () => {
    const submit = vi.fn();
    const { container } = render(<LoginForm onSubmit={submit} pending />);
    fireEvent.submit(container.querySelector("form")!);
    expect(submit).not.toHaveBeenCalled();
  });
  it("동기·비동기 오류를 안전한 문구로 표시하고 재시도한다", async () => {
    const submit = vi.fn().mockRejectedValueOnce(new Error("내부 응답 원문")).mockResolvedValueOnce(undefined);
    render(<LoginForm onSubmit={submit} />);
    await userEvent.type(screen.getByLabelText("아이디"), "demo");
    await userEvent.type(screen.getByLabelText("비밀번호"), "example");
    await userEvent.click(screen.getByRole("button", { name: "로그인" }));
    expect(screen.getByRole("alert")).toHaveTextContent("로그인하지 못했습니다.");
    expect(screen.queryByText("내부 응답 원문")).not.toBeInTheDocument();
    await userEvent.type(screen.getByLabelText("비밀번호"), "retry");
    expect(screen.getByRole("alert")).toBeEmptyDOMElement();
    await userEvent.click(screen.getByRole("button", { name: "로그인" }));
    expect(submit).toHaveBeenCalledTimes(2);
  });
  it("오류 연결과 입력 시 오류 초기화 콜백을 제공한다", async () => {
    const clear = vi.fn();
    render(<LoginForm onSubmit={vi.fn()} error="접속을 확인해 주세요." onClearError={clear} />);
    expect(screen.getByLabelText("아이디")).toHaveAccessibleDescription("접속을 확인해 주세요.");
    await userEvent.type(screen.getByLabelText("아이디"), "d");
    expect(clear).toHaveBeenCalled();
  });
  it("공백 아이디에 포커스를 이동한다", () => {
    const submit = vi.fn();
    const { container } = render(<LoginForm onSubmit={submit} defaultUsername="   " />);
    fireEvent.submit(container.querySelector("form")!);
    expect(submit).not.toHaveBeenCalled();
    expect(screen.getByLabelText("아이디")).toHaveFocus();
  });
  it("복수 폼의 id가 충돌하지 않는다", () => {
    render(<><LoginForm onSubmit={vi.fn()} /><LoginForm onSubmit={vi.fn()} /></>);
    const fields = screen.getAllByLabelText("아이디");
    expect(fields[0]!.id).not.toBe(fields[1]!.id);
  });
  it("확인 중 상태를 로그인 성공으로 표시하지 않는다", () => {
    const { rerender } = render(<LoginStatus status="checking" userLabel="예시" />);
    expect(screen.getByRole("status")).toHaveTextContent("로그인 상태 확인 중…");
    rerender(<LoginStatus status="unauthenticated" />);
    expect(screen.getByRole("status")).toHaveTextContent("로그인이 필요합니다.");
    rerender(<LoginStatus status="authenticated" userLabel="예시" />);
    expect(screen.getByRole("status")).toHaveTextContent("예시님, 로그인됨");
  });
});

describe("탐색 메뉴", () => {
  it("최장 경로 하나를 활성화하고 native 링크·버튼을 제공한다", async () => {
    const action = vi.fn();
    const { container } = render(<AppMenu pathname="/jobs/history/1" groups={[{ id: "ops", label: "운영", items: [
      { id: "home", label: "홈", href: "/" }, { id: "jobs", label: "작업", href: "/jobs" },
      { id: "history", label: "이력", href: "/jobs/history" }, { id: "action", label: "빠른 명령", onSelect: action },
      { id: "disabled", label: "준비 중", href: "/disabled", disabled: true },
    ] }]} />);
    expect(container.querySelectorAll('[aria-current="page"]')).toHaveLength(1);
    expect(screen.getByRole("link", { name: "이력" })).toHaveAttribute("aria-current", "page");
    expect(screen.getByRole("link", { name: "준비 중" })).not.toHaveAttribute("href");
    screen.getByRole("button", { name: "빠른 명령" }).focus();
    await userEvent.keyboard("{Enter}");
    expect(action).toHaveBeenCalledOnce();
    expect(screen.queryByRole("menu")).not.toBeInTheDocument();
    expect((await axe.run(container, { rules: { "color-contrast": { enabled: false } } })).violations).toEqual([]);
  });
  it("hash 활성 상태·명시적 비활성·라우터 링크를 주입한다", () => {
    const groups = [{ id: "g", items: [{ id: "hash", label: "서비스 원장", href: "#ledger" }] }];
    const { rerender } = render(<AppMenu groups={groups} activeItemId="hash" linkComponent={props => <a {...props} data-router="injected" />} />);
    expect(screen.getByRole("link")).toHaveAttribute("aria-current", "page");
    expect(screen.getByRole("link")).toHaveAttribute("data-router", "injected");
    rerender(<AppMenu groups={groups} activeItemId={null} />);
    expect(screen.getByRole("link")).not.toHaveAttribute("aria-current");
  });
});
