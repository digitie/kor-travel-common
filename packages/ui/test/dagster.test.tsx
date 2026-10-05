// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
import { render, screen, within } from "@testing-library/react";
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

test("120개 실행의 집계를 유지하며 행은 50개씩 검색·탐색한다", async () => {
  const runs = Array.from({ length: 120 }, (_, index) => ({ ...snapshot.runs[0]!,
    runId: `run-${index}`, jobName: `collect-${index}`, status: index === 119 ? "FAILURE" : "SUCCESS" }));
  const { container } = render(<DagsterOperations snapshot={{ ...snapshot, runs }}
    onRefresh={vi.fn()} runUrl={() => "#"} scheduleUrl={() => "#"} />);
  const table = container.querySelector('[data-slot="dagster-operations-run-table"]')!;
  expect(table.querySelectorAll("tbody tr")).toHaveLength(50);
  expect(screen.getByRole("status")).toHaveTextContent("조회 120건 · 검색 120건 · 1/3 페이지");
  await userEvent.click(screen.getByRole("button", { name: "다음 실행 페이지" }));
  await userEvent.click(screen.getByRole("button", { name: "다음 실행 페이지" }));
  expect(table.querySelectorAll("tbody tr")).toHaveLength(20);
  expect(screen.getByRole("button", { name: "다음 실행 페이지" })).toBeDisabled();
  await userEvent.selectOptions(screen.getByLabelText("상태 필터"), "FAILURE");
  expect(table.querySelectorAll("tbody tr")).toHaveLength(1);
  expect(within(table as HTMLElement).getByText("collect-119")).toBeVisible();
  expect(screen.getByRole("status")).toHaveTextContent("1/1 페이지");
  await userEvent.type(screen.getByLabelText("실행 검색"), "missing");
  expect(screen.getByText("검색 조건에 맞는 실행이 없습니다.")).toBeVisible();
});

test("선택한 실행 상세와 마지막 조회 오류를 숨기지 않는다", async () => {
  const selected = vi.fn();
  const { container } = render(<DagsterOperations snapshot={snapshot} showRunDetails showRepositories
    error="metadata 연결 실패" onSelectRun={selected} onRefresh={vi.fn()} runUrl={() => "#"} scheduleUrl={() => "#"} />);
  await userEvent.click(screen.getByRole("button", { name: "실행 상세: collect, test-run" }));
  expect(selected).toHaveBeenCalledWith("test-run");
  const detail = screen.getByRole("region", { name: "선택한 실행 상세" });
  expect(within(detail).getByText("test-run")).toBeVisible();
  expect(within(detail).getByText("<script>failure</script>")).toBeVisible();
  expect(container.querySelector("script")).toBeNull();
  expect(screen.getByRole("alert")).toHaveTextContent("마지막 조회 결과");
  expect(screen.getByText("코드 위치")).toBeVisible();
});

test("센서와 스케줄의 실패 tick 및 시간대를 표시한다", async () => {
  const repository = snapshot.repositories[0]!;
  render(<DagsterOperations snapshot={{ ...snapshot, repositories: [{ ...repository,
    schedules: [{ ...repository.schedules[0]!, timezone: "Asia/Seoul", overdue: true,
      lastTick: { status: "FAILURE", timestamp: 1, errorMessage: "schedule tick 실패" } }],
    sensors: [{ name: "recovery", status: "RUNNING", lastTick: { status: "FAILURE", timestamp: 2, errorMessage: "sensor tick 실패" } }]
  }] }} onRefresh={vi.fn()} runUrl={() => "#"} scheduleUrl={() => "#"} />);
  expect(screen.getByRole("region", { name: "Dagster 센서 표" })).toHaveTextContent("sensor tick 실패");
  await userEvent.click(screen.getByRole("button", { name: "collect" }));
  expect(screen.getByText("Asia/Seoul")).toBeVisible();
  expect(screen.getByText("schedule tick 실패")).toBeVisible();
  expect(screen.getByText("조회 시점에 예정된 tick이 지연되었습니다.")).toBeVisible();
});

test("refresh 후 0건이 된 상태 필터도 화면과 내부 조건을 일치시킨다", async () => {
  const props = { onRefresh: vi.fn(), runUrl: () => "#", scheduleUrl: () => "#" };
  const { rerender } = render(<DagsterOperations {...props} snapshot={snapshot} />);
  await userEvent.selectOptions(screen.getByLabelText("상태 필터"), "FAILURE");
  rerender(<DagsterOperations {...props} snapshot={{ ...snapshot,
    runs: [{ ...snapshot.runs[0]!, status: "SUCCESS" }] }} />);
  expect(screen.getByLabelText("상태 필터")).toHaveValue("FAILURE");
  expect(screen.getByRole("option", { name: "실패 · 현재 0건" })).toBeInTheDocument();
  await userEvent.selectOptions(screen.getByLabelText("상태 필터"), "");
  expect(screen.getByRole("status")).toHaveTextContent("검색 1건");
  expect(screen.getByRole("link", { name: /Dagster에서 열기/ })).toBeVisible();
});

test("미제공 센서 목록을 확인된 0개로 표시하지 않는다", () => {
  render(<DagsterOperations snapshot={snapshot} showRepositories onRefresh={vi.fn()}
    runUrl={() => "#"} scheduleUrl={() => "#"} />);
  expect(screen.getByText(/센서 미확인/)).toBeVisible();
});

test("job 정보가 없는 스케줄은 이름을 작업으로 단정하지 않는다", async () => {
  const repository = snapshot.repositories[0]!;
  render(<DagsterOperations snapshot={{ ...snapshot, repositories: [{ ...repository,
    schedules: [{ ...repository.schedules[0]!, jobName: null }] }] }}
    onRefresh={vi.fn()} runUrl={() => "#"} scheduleUrl={() => "#"} />);
  await userEvent.click(screen.getByRole("button", { name: "스케줄 · hourly (작업 미확인)" }));
  const detail = screen.getByText("실행되는 작업").parentElement!;
  expect(detail).toHaveTextContent("미확인");
});


test("explicit unknown runtime does not invent a cap or mark an active run stalled", () => {
  const run = { runId: "unknown-cap", jobName: "__ASSET_JOB", status: "STARTED",
    startTime: 1, endTime: null, errorMessage: null, maxRuntimeSeconds: null };
  expect(isStalledRun(run, 100000)).toBe(false);
});

test("unknown cap detail is explicit, while omitted cap is labeled only as a delay heuristic", async () => {
  const run = { runId: "unknown-cap", jobName: "__ASSET_JOB", status: "STARTED",
    startTime: 1, endTime: null, errorMessage: null, maxRuntimeSeconds: null };
  const props = {onRefresh:vi.fn(), runUrl:()=>"#", scheduleUrl:()=>"#", showRunDetails:true};
  const {rerender} = render(<DagsterOperations {...props} snapshot={{...snapshot,runs:[run]}} />);
  await userEvent.click(screen.getByRole("button",{name:/실행 상세:/}));
  expect(screen.getByText("미확인")).toBeVisible();
  expect(screen.queryByText("정체 의심")).toBeNull();
  rerender(<DagsterOperations {...props} snapshot={{...snapshot,runs:[{...run,maxRuntimeSeconds:undefined}]}} />);
  expect(screen.getByText("지연 판단 기준")).toBeVisible();
});
