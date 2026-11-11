// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
// Origin: kor-travel-weather@5da6e15 packages/kor-travel-weather-admin/frontend/app/admin/dagster/page.tsx (GPL-3.0-or-later)
// Modified: 2026-10-05 — 조회·label·URL을 소비자 콜백으로 분리
"use client";


import { useState, type ComponentProps, type ReactNode } from "react";
import type { DagsterRun, DagsterSchedule, DagsterSnapshot, DagsterRepository, DagsterTick, DagsterSensor } from "./dagster-model.js";
import { STALLED_RUN_THRESHOLD_SECONDS, describeCron, formatElapsed, isStalledRun, runElapsedSeconds, runStatusLabel } from "./dagster-model.js";
import { VirtualTable, type ColumnDef } from "./virtual-table.js";
export interface DagsterOperationsProps {
  snapshot: DagsterSnapshot | null;
  error?: string;
  loading?: boolean;
  onRefresh: () => void;
  jobLabel?: (name: string) => string;
  runUrl: (id: string) => string;
  scheduleUrl: (name: string, repository: DagsterRepository) => string;
  locationUrl?: string;
  testId?: string;
  /** 기본 표 계약은 유지하고 소비자가 목록·상세 구성을 선택한다. */
  showRunDetails?: boolean;
  showRepositories?: boolean;
  selectedRunId?: string | null;
  onSelectRun?: (runId: string) => void;
  renderRunDetail?: (run: DagsterRun | null) => ReactNode;
}


/** 검색·집계는 전체 결과, DOM 행은 페이지 단위로 제한한다. */
export const DAGSTER_RUN_PAGE_SIZE = 50;
function statusClass(status: string | null | undefined) {
  if (status === "RUNNING" || status === "SUCCESS" || status === "STARTED") return "on";
  if (status === "FAILURE" || status === "CANCELED" || status === "STOPPED") return "off";
  return "warn";
}
function runStatusClass(run: DagsterRun, now: number) {
  return isStalledRun(run, now) ? "warn" : statusClass(run.status);
}
function dateTime(epoch: number | null) {
  return epoch !== null ? new Date(epoch * 1000).toLocaleString("ko-KR", { dateStyle: "short", timeStyle: "short", timeZone: "Asia/Seoul" }) : "—";
}
function ScheduleStatus({ status }: { status: string | null }) {
  const label = status === "RUNNING" ? "사용" : status === "STOPPED" ? "중지" : status ?? "확인 불가";
  return <span className={'status ' + statusClass(status)}>{label}</span>;
}
function TickDetail({ tick }: { tick: DagsterTick | null | undefined }) {
  if (!tick) return <>—</>;
  return <><span className={'status ' + statusClass(tick.status)}>{runStatusLabel(tick.status)}</span><small>{dateTime(tick.timestamp)}</small>{tick.errorMessage ? <small className="dagster-run-error">{tick.errorMessage}</small> : null}</>;
}
function RunStatus({ run, now }: { run: DagsterRun; now: number }) {
  const elapsed = runElapsedSeconds(run, now);
  return <><span className={'status ' + runStatusClass(run, now)}>{runStatusLabel(run.status)}</span>
    {elapsed !== null ? <small className="dagster-run-elapsed">{formatElapsed(elapsed)} 경과{isStalledRun(run, now) ? " · 정체 의심" : ""}</small> : null}</>;
}
function RunName({ run, label, selected, onSelect }: { run: DagsterRun; label: string; selected: boolean; onSelect?: () => void }) {
  return <>{onSelect ? <button type="button" className="dagster-run-select" onClick={onSelect} aria-pressed={selected} aria-label={'실행 상세: ' + label + ', ' + run.runId} title={run.jobName}>{label}</button> : <strong title={run.jobName}>{label}</strong>}
    <code>{run.runId.slice(0, 14)}…</code>
    {run.status === "FAILURE" ? <small className="dagster-run-error">{run.errorMessage ?? "실패 원인을 불러오지 못했습니다."}</small> : null}</>;
}
type RunListProps = {
  snapshot: DagsterSnapshot | null; jobLabel: (name: string) => string; runUrl: (id: string) => string;
  selectedId: string | null; onSelect?: (id: string) => void; now: number;
};
function RunList({ snapshot, jobLabel, runUrl, selectedId, onSelect, now }: RunListProps) {
  const [search, setSearch] = useState("");
  const [status, setStatus] = useState("");
  const [page, setPage] = useState(0);
  const runs = snapshot?.runs ?? [];
  const query = search.trim().toLocaleLowerCase("ko-KR");
  const filtered = runs.filter(run => (!status || run.status === status)
    && (run.runId + ' ' + run.jobName + ' ' + jobLabel(run.jobName)).toLocaleLowerCase("ko-KR").includes(query));
  const lastPage = Math.max(0, Math.ceil(filtered.length / DAGSTER_RUN_PAGE_SIZE) - 1);
  const visiblePage = Math.min(page, lastPage);
  const visibleRuns = filtered.slice(visiblePage * DAGSTER_RUN_PAGE_SIZE, (visiblePage + 1) * DAGSTER_RUN_PAGE_SIZE);
  const statuses = [...new Set([...runs.map(run => run.status), ...(status ? [status] : [])])].sort();
  const currentStatuses = new Set(runs.map(run => run.status));
  const columns: ColumnDef<DagsterRun>[] = [
    { id: "status", header: "상태" }, { id: "job", header: "작업" },
    { id: "start", header: "시작" }, { id: "end", header: "종료" }, { id: "detail", header: "상세" },
  ];
  function renderCell(run: DagsterRun, id: string) {
    if (id === "status") return <RunStatus run={run} now={now} />;
    if (id === "job") return <RunName run={run} label={jobLabel(run.jobName)} selected={run.runId === selectedId} onSelect={onSelect ? () => onSelect(run.runId) : undefined} />;
    if (id === "start") return dateTime(run.startTime);
    if (id === "end") return dateTime(run.endTime);
    return <a className="inline-link" href={runUrl(run.runId)} target="_blank" rel="noreferrer">Dagster에서 열기 <span aria-hidden="true">↗</span></a>;
  }
  const empty = snapshot ? "최근 Dagster 실행이 없습니다." : "실행 기록을 불러오는 중…";
  return <section className="panel dagster-runs">
    <div className="panel-head"><div><h2>최근 실행 · 마지막 확인 {snapshot ? new Date(snapshot.checkedAt).toLocaleTimeString("ko-KR", { timeZone: "Asia/Seoul" }) : "불러오는 중…"}</h2></div></div>
    {runs.length > 0 ? <div className="dagster-run-toolbar">
      <label>실행 검색<input aria-label="실행 검색" placeholder="작업 이름 또는 run ID" value={search} onChange={event => { setSearch(event.target.value); setPage(0); }} /></label>
      <label>상태<select aria-label="상태 필터" value={status} onChange={event => { setStatus(event.target.value); setPage(0); }}><option value="">전체 상태</option>{statuses.map(value => <option key={value} value={value}>{runStatusLabel(value)}{currentStatuses.has(value) ? "" : " · 현재 0건"}</option>)}</select></label>
    </div> : null}
    <VirtualTable columns={columns} renderCell={renderCell} data={visibleRuns} getRowId={run => run.runId} ariaLabel="최근 Dagster 실행 표" containerRole="region" containerAriaLabel="최근 Dagster 실행 표" tableSlot="dagster-operations-run-table" containerClassName="table-wrap" rowProps={run => ({ "data-selected": run.runId === selectedId || undefined } as ComponentProps<"tr">)} emptyMessage={runs.length ? "검색 조건에 맞는 실행이 없습니다." : empty} />
    {runs.length > 0 ? <div className="dagster-run-pagination" aria-label="실행 페이지">
      <span role="status">조회 {runs.length}건 · 검색 {filtered.length}건 · {visiblePage + 1}/{lastPage + 1} 페이지</span>
      <button type="button" disabled={visiblePage === 0} onClick={() => setPage(visiblePage - 1)}>이전 실행 페이지</button>
      <button type="button" disabled={visiblePage === lastPage} onClick={() => setPage(visiblePage + 1)}>다음 실행 페이지</button>
    </div> : null}
  </section>;
}
function runtimeLabel(run: DagsterRun) {
  if (run.maxRuntimeSeconds === undefined) return formatElapsed(STALLED_RUN_THRESHOLD_SECONDS);
  return run.maxRuntimeSeconds != null && Number.isFinite(run.maxRuntimeSeconds) && run.maxRuntimeSeconds > 0 ? formatElapsed(run.maxRuntimeSeconds) : "미확인";
}
function RunDetail({ run, jobLabel, now, runUrl, render }: { run: DagsterRun | null; jobLabel: (name: string) => string; now: number; runUrl: (id: string) => string; render?: (run: DagsterRun | null) => ReactNode }) {
  if (render) return <>{render(run)}</>;
  return <><div className="panel-head"><h2>실행 상세</h2></div>{run ? <div className="dagster-detail-body"><strong>{jobLabel(run.jobName)}</strong><code>{run.runId}</code>
    <span className={'status ' + runStatusClass(run, now)}>{runStatusLabel(run.status)}</span>
    <dl><dt>시작</dt><dd>{dateTime(run.startTime)}</dd><dt>종료</dt><dd>{dateTime(run.endTime)}</dd>
      <dt>{run.maxRuntimeSeconds === undefined ? "지연 판단 기준" : "실행 상한"}</dt><dd>{runtimeLabel(run)}</dd></dl>
    {run.errorMessage ? <p className="dagster-run-error">{run.errorMessage}</p> : null}
    <a className="inline-link" href={runUrl(run.runId)} target="_blank" rel="noreferrer">선택한 실행을 Dagster에서 열기 ↗</a>
  </div> : <p className="empty">목록에서 실행을 선택하면 상세를 확인할 수 있습니다.</p>}</>;
}
type ScheduleEntry = { schedule: DagsterSchedule; repository: DagsterRepository; identity: string };
function scheduleEntries(snapshot: DagsterSnapshot | null): ScheduleEntry[] {
  return snapshot?.repositories.flatMap(repository => repository.schedules.map(schedule => ({
    schedule, repository, identity: JSON.stringify([repository.locationName, repository.name, schedule.name]),
  }))) ?? [];
}
function ScheduleDetail({ schedule, url }: { schedule: DagsterSchedule; url: string }) {
  return <div className="sync-run-detail-grid" data-slot="dagster-operations-schedule-detail">
    <div><span>실행되는 작업</span><code>{schedule.jobName ?? "미확인"}</code></div>
    <div><span>스케줄 이름</span><code>{schedule.name}</code></div>
    {schedule.timezone ? <div><span>시간대</span><code>{schedule.timezone}</code></div> : null}
    {schedule.lastTick ? <div><span>최근 tick</span><TickDetail tick={schedule.lastTick} /></div> : null}
    {schedule.overdue ? <div className="warn-text">조회 시점에 예정된 tick이 지연되었습니다.</div> : null}
    <div><span>실행 주기(원본)</span><code>{schedule.cron ?? "—"}</code></div>
    <div><span>Dagster</span><a className="inline-link" href={url} target="_blank" rel="noreferrer">스케줄 열기 <span aria-hidden="true">↗</span></a></div>
  </div>;
}
function ScheduleList({ entries, snapshot, jobLabel, scheduleUrl }: { entries: ScheduleEntry[]; snapshot: DagsterSnapshot | null; jobLabel: (name: string) => string; scheduleUrl: DagsterOperationsProps["scheduleUrl"] }) {
  const [expanded, setExpanded] = useState<string | null>(null);
  const columns: ColumnDef<ScheduleEntry>[] = [
    { id: "job", header: "작업" }, { id: "cron", header: "주기" }, { id: "status", header: "상태" },
  ];
  function renderCell(entry: ScheduleEntry, id: string) {
    if (id === "cron") return entry.schedule.cron ? describeCron(entry.schedule.cron) : "수동 실행";
    if (id === "status") return <ScheduleStatus status={entry.schedule.status} />;
    return <button className="ghost row-expand-toggle" type="button" onClick={() => setExpanded(current => current === entry.identity ? null : entry.identity)} aria-expanded={expanded === entry.identity}>
      <span aria-hidden="true">{expanded === entry.identity ? "▾" : "▸"}</span>
      {entry.schedule.jobName === null ? '스케줄 · ' + entry.schedule.name + ' (작업 미확인)' : jobLabel(entry.schedule.jobName)}
    </button>;
  }
  return <section className="panel"><div className="panel-head"><div><h2>스케줄</h2></div></div>
    <VirtualTable columns={columns} renderCell={renderCell} data={entries} getRowId={entry => entry.identity} ariaLabel="Dagster 스케줄 표" containerRole="region" containerAriaLabel="Dagster 스케줄 표" tableSlot="dagster-operations-schedule-table" containerClassName="table-wrap"
      emptyMessage={snapshot ? "등록된 스케줄이 없습니다." : "스케줄을 불러오는 중…"}
      renderRowDetails={entry => expanded === entry.identity ? <ScheduleDetail schedule={entry.schedule} url={scheduleUrl(entry.schedule.name, entry.repository)} /> : null} />
  </section>;
}
type SensorEntry = { sensor: DagsterSensor; location: string; identity: string };
function Sensors({ snapshot }: { snapshot: DagsterSnapshot | null }) {
  const entries: SensorEntry[] = snapshot?.repositories.flatMap(repository => (repository.sensors ?? []).map(sensor => ({ sensor, location: repository.locationName, identity: JSON.stringify([repository.locationName, repository.name, sensor.name]) }))) ?? [];
  const columns: ColumnDef<SensorEntry>[] = [
    { id: "sensor", header: "센서", cell: ({ row }) => <><strong>{row.original.sensor.name}</strong><small>{row.original.location}</small></> },
    { id: "status", header: "상태", cell: ({ row }) => <ScheduleStatus status={row.original.sensor.status} /> },
    { id: "tick", header: "최근 tick", cell: ({ row }) => <TickDetail tick={row.original.sensor.lastTick} /> },
  ];
  if (!entries.length) return null;
  return <section className="panel" data-slot="dagster-operations-sensors"><div className="panel-head"><h2>센서</h2></div><VirtualTable columns={columns} data={entries} getRowId={entry => entry.identity} ariaLabel="Dagster 센서 표" containerRole="region" containerAriaLabel="Dagster 센서 표" containerClassName="table-wrap" /></section>;
}
function Repositories({ snapshot }: { snapshot: DagsterSnapshot | null }) {
  if (!snapshot) return null;
  return <section className="panel" data-slot="dagster-operations-repositories">
    <div className="panel-head"><h2>코드 위치</h2></div><div className="dagster-repositories">{snapshot.repositories.map(repository => <div key={JSON.stringify([repository.locationName, repository.name])}><strong>{repository.locationName}</strong><code>{repository.name}</code><small>작업 {repository.jobs.length} · 자산 {repository.assetCount ?? repository.assets.length} · 스케줄 {repository.schedules.length} · 센서 {repository.sensors === undefined ? "미확인" : repository.sensors.length}</small></div>)}</div>
  </section>;
}
function Summary({ snapshot, entries, stalled }: { snapshot: DagsterSnapshot | null; entries: ScheduleEntry[]; stalled: number }) {
  const healthy = entries.filter(({ schedule }) => schedule.status === "RUNNING").length;
  const successes = snapshot?.runs.filter(run => run.status === "SUCCESS").length ?? 0;
  const failures = snapshot?.runs.filter(run => run.status === "FAILURE").length ?? 0;
  return <section className="ops-grid" data-slot="dagster-operations-summary" aria-label="Dagster 요약">
    <div className="panel ops-card"><span>사용 중인 스케줄</span><strong>{snapshot ? healthy + '/' + entries.length : "—"}</strong><small>전체 스케줄 대비</small></div>
    <div className="panel ops-card"><span>최근 성공</span><strong>{snapshot ? successes : "—"}</strong><small>최근 {snapshot?.runs.length ?? 0}건 중</small></div>
    <div className="panel ops-card" data-tone={failures > 0 ? "error" : undefined}><span>최근 실패</span><strong>{snapshot ? failures : "—"}</strong><small>재시도·원인 확인 대상</small></div>
    <div className="panel ops-card" data-tone={stalled > 0 ? "warning" : undefined}><span>정체된 실행</span><strong className={stalled > 0 ? "warn-text" : undefined}>{snapshot ? stalled : "—"}</strong><small>job별 실행 상한 · 생략 시 지연 기준 {Math.floor(STALLED_RUN_THRESHOLD_SECONDS / 60)}분</small></div>
  </section>;
}
function SnapshotError({ error, snapshot, loading, onRefresh }: Pick<DagsterOperationsProps, "error" | "snapshot" | "loading" | "onRefresh">) {
  if (!error) return null;
  return <div className="error" data-slot="dagster-operations-error" role="alert">{error}{snapshot ? <small>아래는 마지막 조회 결과입니다. 현재 상태는 확인하지 못했습니다.</small> : null} <button type="button" className="ghost" onClick={onRefresh} disabled={loading}>다시 시도</button></div>;
}
const identityLabel = (name: string) => name;
export function DagsterOperations({ snapshot, error = "", loading = false, onRefresh, jobLabel = identityLabel, runUrl, scheduleUrl, locationUrl, testId,
  showRunDetails = false, showRepositories = false, selectedRunId, onSelectRun, renderRunDetail }: DagsterOperationsProps) {
  const [localSelectedRunId, setLocalSelectedRunId] = useState<string | null>(null);
  const selectedId = selectedRunId === undefined ? localSelectedRunId : selectedRunId;
  const selectedRun = snapshot?.runs.find(run => run.runId === selectedId) ?? null;
  // 경과 시간은 화면을 다시 그리는 시각이 아니라 스냅샷의 확인 시각을 기준으로 한다.
  const now = snapshot ? new Date(snapshot.checkedAt).getTime() / 1000 : 0;
  const stalled = snapshot?.runs.filter(run => isStalledRun(run, now)).length ?? 0;
  const entries = scheduleEntries(snapshot);
  function selectRun(id: string) { setLocalSelectedRunId(id); onSelectRun?.(id); }
  return <div className="kt-dagster-operations" data-slot="dagster-operations" data-testid={testId} aria-busy={loading}>
    <div className="panel-head"><button data-slot="dagster-operations-refresh" type="button" onClick={onRefresh} disabled={loading}>새로고침</button>
      {locationUrl ? <a className="inline-link" href={locationUrl} target="_blank" rel="noreferrer">Dagster UI ↗</a> : null}</div>
    <SnapshotError error={error} snapshot={snapshot} loading={loading} onRefresh={onRefresh} />
    {stalled > 0 ? <div className="error" role="alert">{stalled}개 실행의 경과 시간이 확인 기준을 넘었습니다. 아래 목록에서 &quot;정체 의심&quot; 표시를 확인하세요.</div> : null}
    <Summary snapshot={snapshot} entries={entries} stalled={stalled} />
    <div className={showRunDetails ? "dagster-run-layout" : undefined}>
      <RunList snapshot={snapshot} jobLabel={jobLabel} runUrl={runUrl} selectedId={selectedId} onSelect={showRunDetails ? selectRun : undefined} now={now} />
      {showRunDetails ? <section className="panel dagster-run-detail" data-slot="dagster-operations-run-detail" aria-label="선택한 실행 상세">
        <RunDetail run={selectedRun} jobLabel={jobLabel} now={now} runUrl={runUrl} render={renderRunDetail} />
      </section> : null}
    </div>
    {showRepositories ? <Repositories snapshot={snapshot} /> : null}
    <ScheduleList entries={entries} snapshot={snapshot} jobLabel={jobLabel} scheduleUrl={scheduleUrl} />
    <Sensors snapshot={snapshot} />
  </div>;
}
