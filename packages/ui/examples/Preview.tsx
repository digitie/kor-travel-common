// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"use client";

import { createContext, useContext, useState } from "react";
import type { CSSProperties } from "react";
import * as icons from "lucide-react";
import { AppMenu, LoginForm, LoginStatus } from "@kor-travel/ui";
import type { AppMenuGroup, AppMenuLinkProps } from "@kor-travel/ui/app-menu";
import projectData from "./projects.json";
import "./preview.css";

interface ExampleItem { id: string; label: string; icon: string; href?: string; action?: string; hint?: string }
interface ExampleProject {
  id: string; name: string; sha: string; menu: string; theme: Record<string, string | undefined>;
  rail?: { background: string; foreground: string; muted: string };
  groups: { id: string; label?: string; items: ExampleItem[] }[];
}
const projects: readonly ExampleProject[] = projectData;

const NavigationContext = createContext<(href: string) => void>(() => {});

function PreviewLink({ href, onClick, ...props }: AppMenuLinkProps) {
  const navigate = useContext(NavigationContext);
  return <a {...props} href={href} onClick={event => {
    onClick?.(event);
    if (event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    event.preventDefault();
    navigate(href);
  }} />;
}

export function Preview({ projectId = "map" }: { projectId?: string }) {
  const project = projects.find(item => item.id === projectId) ?? projects[0]!;
  return <ProjectPreview key={project.id} project={project} />;
}

function ProjectPreview({ project }: { project: (typeof projects)[number] }) {
  const [activeId, setActiveId] = useState(project.groups[0]!.items[0]!.id);
  const [view, setView] = useState<"login" | "menu">("login");
  const [notice, setNotice] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<"success" | "error">("error");
  const allItems = project.groups.flatMap(group => group.items);
  const selected = allItems.find(item => item.id === activeId)!;
  const groups: AppMenuGroup[] = project.groups.map(group => ({
    id: group.id, label: group.label ?? undefined,
    items: group.items.map(item => {
      const Icon = icons[item.icon as keyof typeof icons] as typeof icons.Home;
      const base = { id: item.id, label: item.label, hint: "hint" in item ? item.hint : undefined, icon: Icon ? <Icon size={16} strokeWidth={1.8} /> : undefined };
      return "href" in item && item.href ? { ...base, href: item.href } : {
        ...base, onSelect: () => setNotice(`${item.label}: 실제 동작을 연결할 자리입니다.`),
      };
    }),
  }));
  function navigate(href: string) {
    const item = allItems.find(candidate => "href" in candidate && candidate.href === href);
    if (item) { setActiveId(item.id); setView("menu"); }
  }
  const railStyle = project.rail ? {
    background: project.rail.background, color: project.rail.foreground,
    "--kt-text-secondary": project.rail.muted, "--kt-text-primary": project.rail.foreground,
    "--kt-brand-tint": "#4c1d95", "--kt-brand": "#c4b5fd", "--kt-surface-subtle": "#4c1d95", "--kt-focus": project.rail.muted,
  } as CSSProperties : undefined;

  return <div className="preview-root" style={project.theme as CSSProperties} data-project={project.id}>
    <a className="preview-skip" href="#preview-main">본문으로 건너뛰기</a>
    <div className="preview-banner"><a href="/">공통 UI 예시</a><span>리모트 메뉴 기준 · 인증 연동 없음</span></div>
    <div className="preview-layout">
      <aside className="preview-rail" style={railStyle}>
        <div className="preview-wordmark"><strong>{project.name}</strong><span>admin</span></div>
        <div className="preview-navigation"><NavigationContext value={navigate}><AppMenu groups={groups} activeItemId={activeId} linkComponent={PreviewLink} /></NavigationContext></div>
        {project.id !== "docker-manager" ? <button className="preview-logout" onClick={() => setNotice("로그아웃: 실제 인증 연동은 소비자가 제공합니다.")} type="button"><icons.LogOut size={16} />로그아웃</button> : null}
      </aside>
      <main id="preview-main" tabIndex={-1} className="preview-main">
        <header className="preview-header">
          <p>공통 컴포넌트 / {project.id}</p>
          <div><h1>{view === "login" ? "로그인" : selected.label}</h1><span className="preview-version">예시 화면</span></div>
          <p>{view === "login" ? "프로젝트의 색상으로 적용한 공용 로그인 폼입니다." : "실제 프로젝트의 메뉴 구성과 경로를 사용합니다."}</p>
        </header>
        <div className="preview-switcher" role="group" aria-label="예시 화면 선택">
          <button type="button" aria-pressed={view === "login"} onClick={() => setView("login")}>로그인 예시</button>
          <button type="button" aria-pressed={view === "menu"} onClick={() => setView("menu")}>메뉴 예시</button>
        </div>
        {view === "login" ? <section className="preview-login" aria-label="로그인 컴포넌트 예시">
          <LoginForm brand={project.name} description="관리자 계정으로 로그인해 주세요."
            error={error} onClearError={() => setError(null)} onSubmit={async () => {
              await new Promise(resolve => setTimeout(resolve, 800));
              if (result === "error") setError("아이디 또는 비밀번호를 확인해 주세요.");
              else setNotice("예시 로그인 성공 — 실제 세션은 생성하지 않았습니다.");
            }} footer="이 화면은 공통 UI 예시입니다. 실제 계정 정보를 입력하지 마세요." />
          <div className="preview-scenario"><label htmlFor="result">제출 결과 예시</label><select id="result" value={result} onChange={event => setResult(event.target.value as "success" | "error")}><option value="error">인증 오류</option><option value="success">성공 안내</option></select></div>
        </section> : <section className="preview-content">
          <p className="preview-kicker">선택한 메뉴</p><h2>{selected.label}</h2>
          <dl><dt>프로젝트</dt><dd>{project.name}</dd><dt>연결 경로</dt><dd>{"href" in selected ? selected.href : "소비자 콜백"}</dd><dt>상태</dt><dd>메뉴 표시 예시 · 서비스 데이터 미연결</dd></dl>
          <LoginStatus status="unauthenticated" />
        </section>}
        <p className="preview-notice" role="status">{notice}</p>
        <footer className="preview-footer"><span>메뉴·컬러 출처</span><a href={project.menu}>main · {project.sha.slice(0, 8)}</a><span>2026.09.29 확인</span></footer>
      </main>
    </div>
  </div>;
}
