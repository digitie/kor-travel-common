// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
import { act } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";
import { useLayoutEffect } from "react";
import { hydrateRoot, type Root } from "react-dom/client";
import { renderToString } from "react-dom/server";
import { LoginForm } from "../src/login-form.js";

const roots: Root[] = [];
const hosts: HTMLElement[] = [];
afterEach(async () => {
  await act(async () => { for (const root of roots.splice(0)) root.unmount(); });
  for (const host of hosts.splice(0)) host.remove();
});

function serverForm(onSubmit = vi.fn()) {
  const host = document.createElement("div");
  host.innerHTML = renderToString(<LoginForm onSubmit={onSubmit} defaultUsername="admin" />);
  document.body.append(host);
  hosts.push(host);
  return { host, form: host.querySelector("form")!, username: host.querySelector<HTMLInputElement>("[name=username]")!,
    field: host.querySelector<HTMLInputElement>("[name=password]")!, button: host.querySelector<HTMLButtonElement>("button[type=submit]")! };
}

describe("로그인 hydration 준비", () => {
  it("hydration commit 뒤 passive effect 전의 제출도 callback 없이 기본 동작을 취소한다", async () => {
    const submit = vi.fn();
    const intercepted: boolean[] = [];
    function Boundary() {
      useLayoutEffect(() => {
        const form = host.querySelector("form")!;
        const event = new Event("submit", { bubbles: true, cancelable: true });
        form.dispatchEvent(event);
        intercepted.push(event.defaultPrevented);
      }, []);
      return <LoginForm onSubmit={submit} defaultUsername="admin" />;
    }
    const host = document.createElement("div");
    host.innerHTML = renderToString(<Boundary />);
    document.body.append(host);
    hosts.push(host);
    await act(async () => { roots.push(hydrateRoot(host, <Boundary />)); });
    expect(intercepted).toEqual([true]);
    expect(submit).not.toHaveBeenCalled();
    expect(host.querySelector("button")).toBeEnabled();
  });

  it("SSR 입력과 버튼은 native disabled이며 hydration 없는 click·Enter가 기본 제출을 만들지 않는다", async () => {
    const submit = vi.fn();
    const { form, username, field, button } = serverForm(submit);
    let nativeSubmits = 0;
    form.addEventListener("submit", event => { nativeSubmits += 1; event.preventDefault(); });
    // 브라우저 자동완성처럼 값이 있어도 초기 HTML의 제약 자체가 제출을 닫아야 한다.
    field.value = "example";
    expect(username).toBeDisabled();
    expect(field).toBeDisabled();
    expect(button).toBeDisabled();
    expect(button).toHaveAttribute("aria-disabled", "true");
    const user = userEvent.setup();
    await user.click(button);
    field.focus();
    await user.keyboard("{Enter}");
    expect(nativeSubmits).toBe(0);
    expect(submit).not.toHaveBeenCalled();
  });

  it("지연한 hydration 직전까지 닫혀 있고 준비 후 Enter·click은 callback으로만 제출된다", async () => {
    const submit = vi.fn();
    const sample = "example";
    const { host, form, username, field, button } = serverForm(submit);
    let nativeSubmits = 0;
    const observe = (event: Event) => { if (!event.defaultPrevented) { nativeSubmits += 1; event.preventDefault(); } };
    host.addEventListener("submit", observe);
    const user = userEvent.setup();
    // 임의 대기시간 대신 client를 아직 붙이지 않은 실제 SSR DOM에서 두 번 시도한다.
    await user.click(button);
    expect(button).toBeDisabled();
    expect(nativeSubmits).toBe(0);
    host.removeEventListener("submit", observe);
    document.addEventListener("submit", observe);
    try {
      await act(async () => { roots.push(hydrateRoot(host, <LoginForm onSubmit={submit} defaultUsername="admin" />)); });
      expect(username).toBeEnabled();
      expect(field).toBeEnabled();
      expect(button).toBeEnabled();
      expect(button).toHaveAttribute("aria-disabled", "false");
      await user.type(field, sample);
      await user.keyboard("{Enter}");
      expect(submit).toHaveBeenCalledExactlyOnceWith({ credentials: { username: "admin", password: sample }, nextPath: "/" });
      expect(field).toHaveValue("");
      await user.type(field, "retry");
      await user.click(button);
      expect(submit).toHaveBeenCalledTimes(2);
      expect(nativeSubmits).toBe(0);
      expect(form).toHaveAttribute("method", "post");
    } finally { document.removeEventListener("submit", observe); }
  });
});
