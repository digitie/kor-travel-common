// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
// Origin: kor-travel-weather@5da6e15 packages/kor-travel-weather-admin/frontend/lib/dagster.ts (GPL-3.0-or-later)
// Modified: 2026-10-04 — 공용 표시 계약과 선택 실행 상한 추출
export type DagsterSchedule = { name: string; status: string | null; cron: string | null; jobName: string };
export type DagsterRepository = { name: string; locationName: string; schedules: DagsterSchedule[]; jobs: string[]; assets: string[] };
export type DagsterRun = { runId: string; status: string; jobName: string; startTime: number | null; endTime: number | null; errorMessage: string | null; maxRuntimeSeconds?: number };
export type DagsterSnapshot = { repositories: DagsterRepository[]; runs: DagsterRun[]; checkedAt: string };

const RUN_STATUS_LABELS: Record<string, string> = {
  SUCCESS: "성공",
  FAILURE: "실패",
  STARTED: "진행 중",
  STARTING: "시작 중",
  QUEUED: "대기 중",
  CANCELING: "취소 중",
  CANCELED: "취소됨",
  NOT_STARTED: "대기",
};

/** A Dagster run status a person can read, falling back to the raw enum for any status this project doesn't expect. */
export function runStatusLabel(status: string): string {
  return RUN_STATUS_LABELS[status] ?? status;
}

/** Seconds a run now shown as STARTED has been running, or null if it isn't. */
export function runElapsedSeconds(run: DagsterRun, nowSeconds: number): number | null {
  if (run.status !== "STARTED" || run.startTime == null) return null;
  return Math.max(0, nowSeconds - run.startTime);
}

/**
 * A STARTED run past this age is worth an operator's attention: either it is
 * a genuinely long batch, or it is the exact zombie-run failure mode
 * documented in deploy/dagster.yaml -- a run whose process died holding its
 * concurrency slot for ever. Either way "still STARTED" alone does not say
 * which, so the page needs to call out the age instead of a bare badge.
 */
export const STALLED_RUN_THRESHOLD_SECONDS = 600;

export function isStalledRun(run: DagsterRun, nowSeconds: number): boolean {
  const elapsed = runElapsedSeconds(run, nowSeconds);
  const configured = run.maxRuntimeSeconds;
  const threshold = configured !== undefined && Number.isFinite(configured) && configured > 0
    ? configured : STALLED_RUN_THRESHOLD_SECONDS;
  return elapsed !== null && elapsed >= threshold;
}

/** "1시간 12분" style duration, for a person -- not "4320s" or a raw epoch delta. */
export function formatElapsed(seconds: number): string {
  const totalMinutes = Math.floor(seconds / 60);
  const hours = Math.floor(totalMinutes / 60);
  const minutes = totalMinutes % 60;
  if (hours > 0) return `${hours}시간 ${minutes}분`;
  if (minutes > 0) return `${minutes}분`;
  return "1분 미만";
}

/**
 * A cron string is precise but not something a person reads at a glance.
 * Covers this project's own schedules (every hour, a couple of fixed times a
 * day) in plain Korean; anything shaped differently falls back to the raw
 * expression rather than guessing wrong.
 */
export function describeCron(cron: string): string {
  const parts = cron.trim().split(/\s+/);
  if (parts.length !== 5) return cron;
  const [minute = "", hour = "", day, month, weekday] = parts;
  if (day !== "*" || month !== "*" || weekday !== "*") return cron;
  if (hour === "*") {
    if (/^\d+$/.test(minute)) {
      return minute === "0" ? "매시 정각" : `매시 ${minute}분`;
    }
    return cron;
  }
  const minuteNum = Number(minute);
  if (!/^\d+$/.test(minute) || Number.isNaN(minuteNum)) return cron;
  const hours = hour.split(",");
  if (!hours.every((value) => /^\d+$/.test(value))) return cron;
  const times = hours.map((value) => `${value.padStart(2, "0")}:${minute.padStart(2, "0")}`);
  return `매일 ${times.join(", ")}`;
}
