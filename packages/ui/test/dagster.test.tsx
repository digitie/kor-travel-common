// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { expect, test, vi } from "vitest";
import { DagsterOperations } from "../src/dagster-operations.js";
import type { DagsterSnapshot } from "../src/dagster-model.js";
import { describeCron, isStalledRun, runElapsedSeconds } from "../src/dagster-model.js";
import { readFileSync } from "node:fs";

const snapshot: DagsterSnapshot = {
  checkedAt: "2026-10-04T00:00:00Z",
  repositories: [{ name: "repo", locationName: "transport", jobs: [], assets: [], schedules: [
    { name: "hourly", status: "RUNNING", cron: "0 * * * *", jobName: "collect" },
  ] }],
  runs: [{ runId: "test-run", status: "FAILURE", jobName: "collect", startTime: 1,
    endTime: 2, errorMessage: "<script>failure</script>" }],
};

test("종료된 실행의 경과 시간과 유효하지 않은 조회 시각을 구분한다", () => {
  expect(runElapsedSeconds(snapshot.runs[0]!, NaN)).toBe(1);
  expect(isStalledRun({ ...snapshot.runs[0]!, endTime: 10000 }, 20000)).toBe(false);
  expect(runElapsedSeconds({ ...snapshot.runs[0]!, status: "STARTED", endTime: null }, NaN)).toBeNull();
});

test.each([
  ["*/5 * * * *", "5분마다"], ["45 */4 * * *", "4시간마다 45분"],
  ["0 */8 * * *", "8시간마다 0분"], ["*/0 * * * *", "*/0 * * * *"],
  ["75 */4 * * *", "75 */4 * * *"], ["0 25 * * *", "0 25 * * *"],
  ["*/7 * * * *", "*/7 * * * *"],
])("소비자 주기 %s를 정확한 한국어 또는 원본으로 표시한다", (cron, label) => {
  expect(describeCron(cron)).toBe(label);
});

test("주입된 앱 label·URL로 실패와 스케줄을 표시한다", async () => {
  render(<DagsterOperations snapshot={snapshot} onRefresh={vi.fn()} jobLabel={() => "교통 수집"}
    runUrl={id => `/dagster/runs/${id}`} scheduleUrl={name => `/dagster/schedules/${name}`} />);
  expect(screen.getByText("<script>failure</script>")).toBeVisible();
  expect(screen.getByRole("region", { name: "최근 Dagster 실행 표" })).toHaveAttribute("tabindex", "0");
  expect(screen.getByRole("region", { name: "Dagster 스케줄 표" })).toHaveAttribute("tabindex", "0");
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

test("동명 스케줄도 repository별로 확장과 링크를 구별한다", async () => {
  const first = snapshot.repositories[0]!;
  const second = { ...first, name: "other", locationName: "geo",
    schedules: [{ ...first.schedules[0]!, jobName: "collect_geo" }] };
  render(<DagsterOperations snapshot={{ ...snapshot, repositories: [first, second] }}
    onRefresh={vi.fn()} runUrl={() => "#"} testId="dagster"
    scheduleUrl={(name, repository) => `/${repository.locationName}/${name}`} />);
  expect(screen.getByTestId("dagster")).toHaveAttribute("data-slot", "dagster-operations");
  expect(screen.getByRole("columnheader", { name: "상세" })).toBeVisible();
  await userEvent.click(screen.getByRole("button", { name: "collect" }));
  expect(screen.getByRole("button", { name: "collect_geo" })).toHaveAttribute("aria-expanded", "false");
  expect(screen.getByRole("link", { name: /스케줄 열기/ })).toHaveAttribute("href", "/transport/hourly");
});

test("운영 CSS의 모든 공용 토큰이 배포 토큰에 존재한다", () => {
  const css = readFileSync("dagster.css", "utf8");
  const tokens = readFileSync("../tokens/tokens.css", "utf8");
  for (const [, name] of css.matchAll(/var\((--kt-[\w-]+)\)/g)) {
    expect(tokens).toContain(`${name}:`);
  }
});
