// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { expect, test, vi } from "vitest";
import { DagsterOperations } from "../src/dagster-operations.js";
import type { DagsterSnapshot } from "../src/dagster-model.js";
import { isStalledRun } from "../src/dagster-model.js";

const snapshot: DagsterSnapshot = {
  checkedAt: "2026-10-04T00:00:00Z",
  repositories: [{ name: "repo", locationName: "transport", jobs: [], assets: [], schedules: [
    { name: "hourly", status: "RUNNING", cron: "0 * * * *", jobName: "collect" },
  ] }],
  runs: [{ runId: "test-run", status: "FAILURE", jobName: "collect", startTime: 1,
    endTime: 2, errorMessage: "<script>failure</script>" }],
};

test("주입된 앱 label·URL로 실패와 스케줄을 표시한다", async () => {
  render(<DagsterOperations snapshot={snapshot} onRefresh={vi.fn()} jobLabel={() => "교통 수집"}
    runUrl={id => `/dagster/runs/${id}`} scheduleUrl={name => `/dagster/schedules/${name}`} />);
  expect(screen.getByText("<script>failure</script>")).toBeVisible();
  expect(screen.getByRole("link", { name: /Dagster에서 열기/ })).toHaveAttribute("href", "/dagster/runs/test-run");
  await userEvent.click(screen.getByRole("button", { name: "교통 수집" }));
  expect(screen.getByRole("button", { name: "교통 수집" })).toHaveAttribute("aria-expanded", "true");
  expect(screen.getByRole("link", { name: /스케줄 열기/ })).toHaveAttribute("href", "/dagster/schedules/hourly");
});

test("장시간 batch는 자체 상한을 넘기 전까지 정체로 표시하지 않는다", () => {
  const run = { ...snapshot.runs[0]!, status: "STARTED", startTime: 0, maxRuntimeSeconds: 57600 };
  expect(isStalledRun(run, 3600)).toBe(false);
  expect(isStalledRun(run, 57600)).toBe(true);
});

test("조회 오류 재시도는 소비자 콜백이며 pending 중 중복 요청을 막는다", async () => {
  const refresh = vi.fn();
  const { rerender } = render(<DagsterOperations snapshot={null} error="연결 실패"
    onRefresh={refresh} runUrl={() => "#"} scheduleUrl={() => "#"} />);
  await userEvent.click(screen.getByRole("button", { name: "다시 시도" }));
  expect(refresh).toHaveBeenCalledOnce();
  rerender(<DagsterOperations snapshot={null} error="연결 실패" loading
    onRefresh={refresh} runUrl={() => "#"} scheduleUrl={() => "#"} />);
  expect(screen.getByRole("button", { name: "다시 시도" })).toBeDisabled();
});
