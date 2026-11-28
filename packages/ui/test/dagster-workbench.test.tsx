// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)

import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { DagsterLogControls, DagsterRunControls, DagsterServiceControls, DagsterServiceStatus } from "../src/dagster-workbench";

describe("Dagster 공용 조작", () => {
  it("사용자가 확인해야 강제 종료를 요청한다", () => {
    const action = vi.fn();
    render(<DagsterRunControls runId="run-one" label="수집 작업" actions={["force-cancel"]} onAction={action} />);
    fireEvent.click(screen.getByRole("button", { name: "실행 강제 종료" }));
    expect(action).not.toHaveBeenCalled();
    fireEvent.click(screen.getByRole("alertdialog").querySelector('button[data-slot="alert-dialog-action"]')!);
    expect(action).toHaveBeenCalledWith("force-cancel");
  });

  it("대상이 바뀌면 확인창을 닫고 알 수 없는 작업은 표시하지 않는다", () => {
    const action = vi.fn();
    const { rerender } = render(<DagsterRunControls runId="run-one" label="수집 작업"
      actions={["reexecute", "unknown" as "reexecute"]} onAction={action} />);
    expect(screen.getAllByRole("button")).toHaveLength(1);
    fireEvent.click(screen.getByRole("button", { name: "처음부터 재실행" }));
    expect(screen.getByRole("alertdialog").textContent).toContain("run-one");
    rerender(<DagsterRunControls runId="run-two" label="다른 작업" actions={["reexecute"]} onAction={action} />);
    expect(screen.queryByRole("alertdialog")).toBeNull();
    expect(action).not.toHaveBeenCalled();
  });

  it("서비스 제어는 설정된 작업만 표시하고 영향 범위를 알린다", () => {
    const action = vi.fn();
    render(<DagsterServiceControls serviceId="shared-daemon" label="공유 데몬" actions={["dagster-restart"]}
      affectedServices={["Geo", "Map"]} onAction={action} />);
    expect(screen.queryByRole("button", { name: "서비스 강제 종료" })).toBeNull();
    fireEvent.click(screen.getByRole("button", { name: "서비스 재시작" }));
    const dialog = screen.getByRole("alertdialog");
    expect(dialog.textContent).toContain("Geo, Map");
    expect(action).not.toHaveBeenCalled();
    fireEvent.click(dialog.querySelector('button[data-slot="alert-dialog-action"]')!);
    expect(action).toHaveBeenCalledWith("dagster-restart");
  });

  it("관리 UI 링크와 로그 이벤트 콜백을 앱에서 받는다", () => {
    const filter = vi.fn();
    const next = vi.fn();
    render(<>
      <DagsterServiceStatus daemons={[]} links={[{ href: "/services/worker", label: "서비스 상세" }]} />
      <DagsterLogControls errorsOnly={false} onFilter={filter} onNextPage={next} />
    </>);
    expect(screen.getByRole("link", { name: "서비스 상세" }).getAttribute("href")).toBe("/services/worker");
    fireEvent.click(screen.getByRole("button", { name: "오류 로그만 보기" }));
    expect(filter).toHaveBeenCalledWith(true);
    fireEvent.click(screen.getByRole("button", { name: "다음 로그 페이지" }));
    expect(next).toHaveBeenCalledOnce();
    expect(screen.queryByRole("button", { name: "첫 로그 페이지" })).toBeNull();
  });
});
