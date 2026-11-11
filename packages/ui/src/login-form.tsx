// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"use client";

import { useId, useRef, useState, useSyncExternalStore } from "react";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { createStore } from "zustand/vanilla";
import { useStore } from "zustand";
import type { ReactNode } from "react";
import { LoginError } from "./login-error.js";
import { sanitizeLocalPath } from "./navigation.js";

export interface LoginCredentials { username: string; password: string }
export interface LoginSubmission { credentials: LoginCredentials; nextPath: string }
export interface LoginFormProps {
  onSubmit: (submission: LoginSubmission) => void | Promise<void>;
  nextPath?: string;
  pending?: boolean;
  error?: string | null;
  onClearError?: () => void;
  defaultUsername?: string;
  usernameLabel?: string;
  brand?: string;
  description?: string;
  footer?: ReactNode;
  testId?: string;
}

const subscribeReady = () => () => {};
const clientReady = () => true;
const serverReady = () => false;

const inputClass = "min-h-11 w-full rounded-kt-control border border-kt-control-line bg-kt-surface-page px-3 py-2 text-kt-sm text-kt-text-primary focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-kt-focus read-only:bg-kt-surface-subtle";

export function LoginForm({
  onSubmit, nextPath = "/", pending = false, error, onClearError,
  defaultUsername = "", usernameLabel = "아이디", brand = "kor travel",
  description = "계정으로 로그인해 주세요.", footer, testId,
}: LoginFormProps) {
  const id = useId();
  const passwordRef = useRef<HTMLInputElement>(null);
  const inFlight = useRef(false);
  const ready = useSyncExternalStore(subscribeReady, clientReady, serverReady);
  const [store] = useState(() => createStore<{ submitting: boolean; localError: string | null }>(() => ({ submitting: false, localError: null })));
  const { submitting, localError } = useStore(store);
  const setSubmitting = (submitting: boolean) => store.setState({ submitting });
  const setLocalError = (localError: string | null) => store.setState({ localError });
  const { register, handleSubmit, resetField, setFocus } = useForm<LoginCredentials>({ defaultValues: { username: defaultUsername, password: "" } });
  const schema = z.object({ username: z.string().trim().min(1), password: z.string().min(1) });
  const usernameField = register("username", { onChange: clearError });
  const passwordField = register("password", { onChange: clearError });
  const busy = pending || submitting;
  const message = localError || error;

  // SSR와 최초 client 렌더를 같은 disabled HTML로 유지하고 handler 준비 뒤 연다.

  function clearError() {
    setLocalError(null);
    if (error) onClearError?.();
  }

  async function submit(credentials: LoginCredentials) {
    if (!ready || pending || inFlight.current) return;
    const parsed = schema.safeParse(credentials);
    const username = credentials.username.trim();
    if (!parsed.success) {
      setLocalError(`${usernameLabel}를 입력해 주세요.`);
      setFocus(username ? "password" : "username");
      return;
    }
    inFlight.current = true;
    setSubmitting(true);
    setLocalError(null);
    try {
      onClearError?.();
      await onSubmit({ credentials: parsed.data, nextPath: sanitizeLocalPath(nextPath) });
    } catch {
      // 콜백의 오류 원문(비밀·서버 상세 포함 가능)을 렌더링하거나 로그에 남기지 않는다.
      setLocalError("로그인하지 못했습니다. 잠시 후 다시 시도해 주세요.");
    } finally {
      resetField("password");
      if (passwordRef.current) passwordRef.current.value = "";
      inFlight.current = false;
      setSubmitting(false);
    }
  }

  return <form data-slot="login-form" data-testid={testId} aria-labelledby={`${id}-title`}
    aria-busy={busy} onSubmit={(event) => { event.preventDefault(); if (!ready || pending || inFlight.current) return; void handleSubmit(submit)(event); }} method="post"
    className="mx-auto flex w-full max-w-sm flex-col gap-4 px-4 py-8 font-kt-sans text-kt-text-primary">
    <div className="space-y-2">
      <p data-slot="login-brand" className="break-words text-kt-xl font-semibold">{brand}</p>
      <h2 id={`${id}-title`} className="text-kt-lg font-semibold">로그인</h2>
      <p className="text-kt-sm text-kt-text-secondary">{description}</p>
    </div>
    <div className="space-y-2">
      <label htmlFor={`${id}-username`} className="text-kt-sm">{usernameLabel}</label>
      <input id={`${id}-username`} data-slot="login-username" defaultValue={defaultUsername} {...usernameField} type="text"
        autoComplete="username" autoCapitalize="none" spellCheck={false} required
        disabled={!ready} readOnly={busy}
        aria-describedby={message ? `${id}-error` : undefined} className={inputClass} />
    </div>
    <div className="space-y-2">
      <label htmlFor={`${id}-password`} className="text-kt-sm">비밀번호</label>
      <input {...passwordField} ref={(element) => { passwordField.ref(element); passwordRef.current = element; }} id={`${id}-password`} data-slot="login-password" type="password"
        autoComplete="current-password" required disabled={!ready} readOnly={busy}
        aria-describedby={message ? `${id}-error` : undefined} className={inputClass} />
    </div>
    <LoginError id={`${id}-error`} error={message} />
    <button data-slot="login-submit" type="submit" disabled={!ready} aria-disabled={!ready || busy} aria-busy={busy}
      className="min-h-11 w-full rounded-kt-control bg-kt-brand px-4 py-2 text-kt-sm font-semibold text-kt-brand-foreground hover:bg-kt-brand-hover focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-kt-focus">
      {busy ? "로그인 중…" : "로그인"}
    </button>
    <p className="sr-only" role="status">{busy ? "로그인 중…" : ""}</p>
    {footer ? <div data-slot="login-footer" className="border-t border-kt-border pt-4 text-kt-sm text-kt-text-secondary">{footer}</div> : null}
  </form>;
}
