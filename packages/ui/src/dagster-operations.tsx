// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
// Origin: kor-travel-weather@5da6e15 packages/kor-travel-weather-admin/frontend/app/admin/dagster/page.tsx (GPL-3.0-or-later)
// Modified: 2026-10-05 — 조회·label·URL을 소비자 콜백으로 분리
"use client";

import { useState, type ReactNode } from "react";
import type { DagsterRun, DagsterSchedule, DagsterSnapshot, DagsterRepository } from "./dagster-model.js";
import { STALLED_RUN_THRESHOLD_SECONDS, describeCron, formatElapsed, isStalledRun, runElapsedSeconds, runStatusLabel } from "./dagster-model.js";

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

/** DOM에 올리는 실행 행 수. 전체 결과의 집계와 검색에는 제한을 적용하지 않는다. */
export const DAGSTER_RUN_PAGE_SIZE = 50;

function statusClass(status: string | null | undefined) {
  if (status === "RUNNING" || status === "SUCCESS" || status === "STARTED") return "on";
  if (status === "FAILURE" || status === "CANCELED" || status === "STOPPED") return "off";
  return "warn";
}

// A STARTED run reads identically to a healthy one until an operator does the
// arithmetic on its start time themselves -- which is exactly the state that
// held ingestion down for hours before anyone noticed. Once it crosses
// isStalledRun's threshold this overrides the badge to "warn" instead.
function runStatusClass(run: DagsterRun, nowSeconds: number) {
  if (isStalledRun(run, nowSeconds)) return "warn";
  return statusClass(run.status);
}

function dateTime(epoch: number | null) {
  return epoch !== null ? new Date(epoch * 1000).toLocaleString("ko-KR", { dateStyle: "short", timeStyle: "short", timeZone: "Asia/Seoul" }) : "—";
}

function RunRow({ run, nowSeconds, jobLabel, dagsterRunUrl, selected, onSelect }: { run: DagsterRun; nowSeconds: number; jobLabel: (name: string) => string; dagsterRunUrl: (id: string) => string; selected?: boolean; onSelect?: () => void }) {
  const elapsed = runElapsedSeconds(run, nowSeconds);
  const stalled = isStalledRun(run, nowSeconds);
  return (
    <tr data-selected={selected || undefined}>
      <td>
        <span className={`status ${runStatusClass(run, nowSeconds)}`}>{runStatusLabel(run.status)}</span>
        {elapsed !== null ? <small className="dagster-run-elapsed">{formatElapsed(elapsed)} 경과{stalled ? " · 정체 의심" : ""}</small> : null}
      </td>
      <td>
        {onSelect ? <button type="button" className="dagster-run-select" onClick={onSelect} aria-pressed={selected} aria-label={`실행 상세: ${jobLabel(run.jobName)}, ${run.runId}`} title={run.jobName}>{jobLabel(run.jobName)}</button> : <strong title={run.jobName}>{jobLabel(run.jobName)}</strong>}
        <code>{run.runId.slice(0, 14)}…</code>
        {run.status === "FAILURE" ? <small className="dagster-run-error">{run.errorMessage ?? "실패 원인을 불러오지 못했습니다."}</small> : null}
      </td>
      <td>{dateTime(run.startTime)}</td>
      <td>{dateTime(run.endTime)}</td>
      <td><a className="inline-link" href={dagsterRunUrl(run.runId)} target="_blank" rel="noreferrer">Dagster에서 열기 <span aria-hidden="true">↗</span></a></td>
    </tr>
  );
}

function ScheduleRow({ schedule, expanded, onToggle, jobLabel, dagsterScheduleUrl }: { schedule: DagsterSchedule; expanded: boolean; onToggle: () => void; jobLabel: (name: string) => string; dagsterScheduleUrl: (name: string) => string }) {
  return (
    <>
      <tr>
        <td>
          <button className="ghost row-expand-toggle" type="button" onClick={onToggle} aria-expanded={expanded}>
            {expanded ? <span aria-hidden="true">▾</span> : <span aria-hidden="true">▸</span>}
            {jobLabel(schedule.jobName)}
          </button>
        </td>
        <td>{schedule.cron ? describeCron(schedule.cron) : "수동 실행"}</td>
        <td><span className={`status ${statusClass(schedule.status)}`}>{schedule.status === "RUNNING" ? "사용" : schedule.status === "STOPPED" ? "중지" : schedule.status ?? "확인 불가"}</span></td>
      </tr>
      {expanded ? (
        <tr className="sync-run-detail-row" data-slot="dagster-operations-schedule-detail">
          <td colSpan={3}>
            <div className="sync-run-detail-grid">
              <div><span>실행되는 작업</span><code>{schedule.jobName}</code></div>
              <div><span>스케줄 이름</span><code>{schedule.name}</code></div>
              {schedule.timezone ? <div><span>시간대</span><code>{schedule.timezone}</code></div> : null}
              {schedule.lastTick ? <div><span>최근 tick</span><span className={`status ${statusClass(schedule.lastTick.status)}`}>{runStatusLabel(schedule.lastTick.status)}</span><small>{dateTime(schedule.lastTick.timestamp)}</small>{schedule.lastTick.errorMessage ? <small className="dagster-run-error">{schedule.lastTick.errorMessage}</small> : null}</div> : null}
              {schedule.overdue ? <div className="warn-text">조회 시점에 예정된 tick이 지연되었습니다.</div> : null}
              <div><span>실행 주기(원본)</span><code>{schedule.cron ?? "—"}</code></div>
              <div><span>Dagster</span><a className="inline-link" href={dagsterScheduleUrl(schedule.name)} target="_blank" rel="noreferrer">스케줄 열기 <span aria-hidden="true">↗</span></a></div>
            </div>
          </td>
        </tr>
      ) : null}
    </>
  );
}

export function DagsterOperations({ snapshot, error = "", loading = false, onRefresh: load,
  jobLabel = (name) => name, runUrl, scheduleUrl, locationUrl, testId,
  showRunDetails = false, showRepositories = false, selectedRunId, onSelectRun,
  renderRunDetail }: DagsterOperationsProps) {
  const [expandedSchedule, setExpandedSchedule] = useState<string | null>(null);
  const [localSelectedRunId, setLocalSelectedRunId] = useState<string | null>(null);
  const [search, setSearch] = useState("");
  const [status, setStatus] = useState("");
  const [page, setPage] = useState(0);
  const runs = snapshot?.runs ?? [];
  const selectedId = selectedRunId === undefined ? localSelectedRunId : selectedRunId;
  const selectedRun = runs.find(run => run.runId === selectedId) ?? null;
  const query = search.trim().toLocaleLowerCase("ko-KR");
  const filteredRuns = runs.filter(run => (!status || run.status === status)
    && `${run.runId} ${run.jobName} ${jobLabel(run.jobName)}`.toLocaleLowerCase("ko-KR").includes(query));
  const lastPage = Math.max(0, Math.ceil(filteredRuns.length / DAGSTER_RUN_PAGE_SIZE) - 1);
  const visiblePage = Math.min(page, lastPage);
  const visibleRuns = filteredRuns.slice(visiblePage * DAGSTER_RUN_PAGE_SIZE, (visiblePage + 1) * DAGSTER_RUN_PAGE_SIZE);
  const statuses = [...new Set(runs.map(run => run.status))].sort();
  function selectRun(runId: string) {
    setLocalSelectedRunId(runId);
    onSelectRun?.(runId);
  }
  const schedules = snapshot?.repositories.flatMap((repository: DagsterRepository) =>
    repository.schedules.map(schedule => ({ schedule, repository,
      identity: JSON.stringify([repository.locationName, repository.name, schedule.name]) }))) ?? [];
  const healthy = schedules.filter(({ schedule }) => schedule.status === "RUNNING").length;
  const successes = snapshot?.runs.filter((run) => run.status === "SUCCESS").length ?? 0;
  const failures = snapshot?.runs.filter((run) => run.status === "FAILURE").length ?? 0;
  // The snapshot's own fetch time, not the render clock: elapsed durations
  // then describe exactly what the data on screen showed, and remain correct
  // even if this tab sits open a while before the next refresh.
  const nowSeconds = snapshot ? new Date(snapshot.checkedAt).getTime() / 1000 : Date.now() / 1000;
  const stalled = snapshot?.runs.filter((run) => isStalledRun(run, nowSeconds)).length ?? 0;

  return (
    <div className="kt-dagster-operations" data-slot="dagster-operations" data-testid={testId} aria-busy={loading}>
      <div className="panel-head">
        <button data-slot="dagster-operations-refresh" type="button" onClick={load} disabled={loading}>새로고침</button>
        {locationUrl ? <a className="inline-link" href={locationUrl} target="_blank" rel="noreferrer">Dagster UI ↗</a> : null}
      </div>
      {error ? <div className="error" data-slot="dagster-operations-error" role="alert">{error}{snapshot ? <small>아래는 마지막 조회 결과입니다. 현재 상태는 확인하지 못했습니다.</small> : null} <button type="button" className="ghost" onClick={load} disabled={loading}>다시 시도</button></div> : null}
      {stalled > 0 ? (
        <div className="error" role="alert">
          {stalled}개 실행이 실행 상한을 넘었습니다. 아래 목록에서 &quot;정체 의심&quot; 표시를 확인하세요.
        </div>
      ) : null}
      <section className="ops-grid" data-slot="dagster-operations-summary" aria-label="Dagster 요약">
        <div className="panel ops-card"><span>사용 중인 스케줄</span><strong>{snapshot ? `${healthy}/${schedules.length}` : "—"}</strong><small>전체 스케줄 대비</small></div>
        <div className="panel ops-card"><span>최근 성공</span><strong>{snapshot ? successes : "—"}</strong><small>최근 {snapshot?.runs.length ?? 0}건 중</small></div>
        <div className="panel ops-card" data-tone={failures > 0 ? "error" : undefined}><span>최근 실패</span><strong>{snapshot ? failures : "—"}</strong><small>재시도·원인 확인 대상</small></div>
        <div className="panel ops-card" data-tone={stalled > 0 ? "warning" : undefined}><span>정체된 실행</span><strong className={stalled > 0 ? "warn-text" : undefined}>{snapshot ? stalled : "—"}</strong><small>job별 실행 상한 · 미설정 시 {Math.floor(STALLED_RUN_THRESHOLD_SECONDS / 60)}분</small></div>
      </section>
      <div className={showRunDetails ? "dagster-run-layout" : undefined}>
      <section className="panel dagster-runs">
        <div className="panel-head"><div><h2>최근 실행 · 마지막 확인 {snapshot ? new Date(snapshot.checkedAt).toLocaleTimeString("ko-KR", { timeZone: "Asia/Seoul" }) : "불러오는 중…"}</h2></div></div>
        {runs.length ? <div className="dagster-run-toolbar">
          <label>실행 검색<input aria-label="실행 검색" placeholder="작업 이름 또는 run ID" value={search} onChange={event => { setSearch(event.target.value); setPage(0); }} /></label>
          <label>상태<select aria-label="상태 필터" value={status} onChange={event => { setStatus(event.target.value); setPage(0); }}><option value="">전체 상태</option>{statuses.map(value => <option key={value} value={value}>{runStatusLabel(value)}</option>)}</select></label>
        </div> : null}
        {visibleRuns.length ? <div className="table-wrap" role="region" aria-label="최근 Dagster 실행 표" tabIndex={0}><table data-slot="dagster-operations-run-table"><thead><tr><th scope="col">상태</th><th scope="col">작업</th><th scope="col">시작</th><th scope="col">종료</th><th scope="col">상세</th></tr></thead><tbody>{visibleRuns.map((run) => <RunRow key={run.runId} run={run} nowSeconds={nowSeconds} jobLabel={jobLabel} dagsterRunUrl={runUrl} selected={run.runId === selectedId} onSelect={showRunDetails ? () => selectRun(run.runId) : undefined} />)}</tbody></table></div> : <div className="empty">{runs.length ? "검색 조건에 맞는 실행이 없습니다." : snapshot ? "최근 Dagster 실행이 없습니다." : "실행 기록을 불러오는 중…"}</div>}
        {runs.length ? <div className="dagster-run-pagination" aria-label="실행 페이지">
          <span role="status">조회 {runs.length}건 · 검색 {filteredRuns.length}건 · {visiblePage + 1}/{lastPage + 1} 페이지</span>
          <button type="button" disabled={visiblePage === 0} onClick={() => setPage(visiblePage - 1)}>이전 실행 페이지</button>
          <button type="button" disabled={visiblePage === lastPage} onClick={() => setPage(visiblePage + 1)}>다음 실행 페이지</button>
        </div> : null}
      </section>
      {showRunDetails ? <section className="panel dagster-run-detail" data-slot="dagster-operations-run-detail" aria-label="선택한 실행 상세">
        {renderRunDetail ? renderRunDetail(selectedRun) : <>
          <div className="panel-head"><h2>실행 상세</h2></div>
          {selectedRun ? <div className="dagster-detail-body"><strong>{jobLabel(selectedRun.jobName)}</strong><code>{selectedRun.runId}</code>
            <span className={`status ${runStatusClass(selectedRun, nowSeconds)}`}>{runStatusLabel(selectedRun.status)}</span>
            <dl><dt>시작</dt><dd>{dateTime(selectedRun.startTime)}</dd><dt>종료</dt><dd>{dateTime(selectedRun.endTime)}</dd>
              <dt>실행 상한</dt><dd>{formatElapsed(selectedRun.maxRuntimeSeconds !== undefined && Number.isFinite(selectedRun.maxRuntimeSeconds) && selectedRun.maxRuntimeSeconds > 0 ? selectedRun.maxRuntimeSeconds : STALLED_RUN_THRESHOLD_SECONDS)}</dd></dl>
            {selectedRun.errorMessage ? <p className="dagster-run-error">{selectedRun.errorMessage}</p> : null}
            <a className="inline-link" href={runUrl(selectedRun.runId)} target="_blank" rel="noreferrer">선택한 실행을 Dagster에서 열기 ↗</a>
          </div> : <p className="empty">목록에서 실행을 선택하면 상세를 확인할 수 있습니다.</p>}
        </>}
      </section> : null}
      </div>
      {showRepositories && snapshot ? <section className="panel" data-slot="dagster-operations-repositories">
        <div className="panel-head"><h2>코드 위치</h2></div><div className="dagster-repositories">{snapshot.repositories.map(repository => <div key={JSON.stringify([repository.locationName, repository.name])}><strong>{repository.locationName}</strong><code>{repository.name}</code><small>작업 {repository.jobs.length} · 자산 {repository.assetCount ?? repository.assets.length} · 스케줄 {repository.schedules.length} · 센서 {repository.sensors?.length ?? 0}</small></div>)}</div>
      </section> : null}
      <section className="panel">
        <div className="panel-head"><div><h2>스케줄</h2></div></div>
        {schedules.length ? (
          <div className="table-wrap" role="region" aria-label="Dagster 스케줄 표" tabIndex={0}>
            <table data-slot="dagster-operations-schedule-table">
              <thead><tr><th scope="col">작업</th><th scope="col">주기</th><th scope="col">상태</th></tr></thead>
              <tbody>
                {schedules.map(({ schedule, repository, identity }) => (
                  <ScheduleRow
                    key={identity}
                    schedule={schedule}
                    jobLabel={jobLabel}
                    dagsterScheduleUrl={(name) => scheduleUrl(name, repository)}
                    expanded={expandedSchedule === identity}
                    onToggle={() => setExpandedSchedule((current) => (current === identity ? null : identity))}
                  />
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="empty">{snapshot ? "등록된 스케줄이 없습니다." : "스케줄을 불러오는 중…"}</div>
        )}
      </section>
      {snapshot?.repositories.some(repository => repository.sensors?.length) ? <section className="panel" data-slot="dagster-operations-sensors">
        <div className="panel-head"><h2>센서</h2></div>
        <div className="table-wrap" role="region" aria-label="Dagster 센서 표" tabIndex={0}><table>
          <thead><tr><th scope="col">센서</th><th scope="col">상태</th><th scope="col">최근 tick</th></tr></thead>
          <tbody>{snapshot.repositories.flatMap(repository => (repository.sensors ?? []).map(sensor => <tr key={JSON.stringify([repository.locationName, repository.name, sensor.name])}>
            <td><strong>{sensor.name}</strong><small>{repository.locationName}</small></td>
            <td><span className={`status ${statusClass(sensor.status)}`}>{sensor.status === "RUNNING" ? "사용" : sensor.status === "STOPPED" ? "중지" : sensor.status ?? "확인 불가"}</span></td>
            <td>{sensor.lastTick ? <><span className={`status ${statusClass(sensor.lastTick.status)}`}>{runStatusLabel(sensor.lastTick.status)}</span><small>{dateTime(sensor.lastTick.timestamp)}</small>{sensor.lastTick.errorMessage ? <small className="dagster-run-error">{sensor.lastTick.errorMessage}</small> : null}</> : "—"}</td>
          </tr>))}</tbody>
        </table></div>
      </section> : null}
    </div>
  );
}
