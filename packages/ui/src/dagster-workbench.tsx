// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"use client";

import {
  AlertDialog, AlertDialogAction, AlertDialogCancel, AlertDialogContent, AlertDialogDescription,
  AlertDialogFooter, AlertDialogHeader, AlertDialogTitle, AlertDialogTrigger
} from "./alert-dialog.js";
import { Button } from "./button.js";

export type DagsterControlAction = "force-cancel" | "reexecute";

function DagsterConfirmation({ label, description, dangerous, disabled, onConfirm }: {
  label: string;
  description: string;
  dangerous?: boolean;
  disabled?: boolean;
  onConfirm: () => void;
}) {
  return (
    <AlertDialog>
      <AlertDialogTrigger asChild>
        <Button size="sm" variant={dangerous ? "destructive" : "outline"} disabled={disabled}>{label}</Button>
      </AlertDialogTrigger>
      <AlertDialogContent>
        <AlertDialogHeader>
          <AlertDialogTitle>{label}</AlertDialogTitle>
          <AlertDialogDescription>{description}</AlertDialogDescription>
        </AlertDialogHeader>
        <AlertDialogFooter>
          <AlertDialogCancel>닫기</AlertDialogCancel>
          <AlertDialogAction variant={dangerous ? "destructive" : "default"} disabled={disabled}
            onClick={onConfirm}>{label}</AlertDialogAction>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>
  );
}

export function DagsterRunControls({ actions, pending, onAction }: {
  actions: readonly DagsterControlAction[];
  pending?: boolean;
  onAction: (action: DagsterControlAction) => void;
}) {
  if (!actions.length) return null;
  return (
    <div className="flex flex-wrap gap-2" aria-label="Dagster 실행 제어">
      {actions.map(action => {
        const force = action === "force-cancel";
        return (
          <DagsterConfirmation key={action}
            label={force ? "실행 강제 종료" : "처음부터 재실행"}
            description={force
              ? "Dagster에 즉시 취소를 요청합니다. 실행 상태가 먼저 바뀔 수 있으므로 작업 프로세스 상태를 확인하세요."
              : "이 실행의 설정으로 새로운 전체 실행을 시작합니다. 원본마다 한 번만 접수합니다."}
            dangerous={force}
            disabled={pending}
            onConfirm={() => onAction(action)}
          />
        );
      })}
    </div>
  );
}

export type DagsterServiceAction = "force-stop" | "dagster-restart";

const serviceActions = [
  { key: "dagster-restart", label: "서비스 재시작" },
  { key: "force-stop", label: "서비스 강제 종료" }
] as const satisfies ReadonlyArray<{ key: DagsterServiceAction; label: string }>;

export function DagsterServiceControls({ actions, label, affectedServices = [], pending, onAction, onLogs }: {
  actions: readonly DagsterServiceAction[];
  label: string;
  affectedServices?: readonly string[];
  pending?: boolean;
  onAction: (action: DagsterServiceAction) => void;
  onLogs?: () => void;
}) {
  if (!actions.length && !onLogs) return null;
  const scope = affectedServices.length ? ` 영향받는 대상은 ${affectedServices.join(", ")}입니다.` : "";
  return (
    <div className="flex flex-wrap gap-2" aria-label="Dagster 서비스 제어">
      {onLogs ? <Button size="sm" variant="outline" onClick={onLogs}>서비스 로그</Button> : null}
      {serviceActions.filter(({ key }) => actions.includes(key)).map(({ key, label: actionLabel }) => (
        <DagsterConfirmation key={key}
          label={actionLabel}
          description={`${label}의 ${actionLabel}를 요청합니다. 실행 중인 작업이 중단될 수 있습니다.${scope}`}
          dangerous={key === "force-stop"}
          disabled={pending}
          onConfirm={() => onAction(key)}
        />
      ))}
    </div>
  );
}

export interface DagsterDaemonState {
  id: string;
  healthy: boolean | null;
  heartbeatAt: number | null;
  errors?: readonly string[];
}

type ServiceLink = { href: string; label: string };

const clock = new Intl.DateTimeFormat("ko-KR", {
  dateStyle: "short", timeStyle: "medium", timeZone: "Asia/Seoul"
});

export function DagsterServiceStatus({ daemons, links = [] }: {
  daemons: readonly DagsterDaemonState[];
  links?: readonly ServiceLink[];
}) {
  if (!daemons.length && !links.length) return null;
  return (
    <section className="grid min-w-0 gap-3 rounded-md border p-4" aria-label="Dagster 서비스">
      <h3 className="text-sm font-semibold">Dagster 서비스</h3>
      {daemons.length ? (
        <ul className="grid gap-2 text-sm">
          {daemons.map(daemon => (
            <li key={daemon.id} className="flex flex-wrap items-center gap-2">
              <strong>{daemon.id}</strong>
              <span>{daemon.healthy == null ? "미확인" : daemon.healthy ? "정상" : "비정상"}</span>
              {daemon.heartbeatAt != null && Math.abs(daemon.heartbeatAt) <= 8.64e12
                ? <span>최근 확인 {clock.format(daemon.heartbeatAt * 1000)}</span>
                : null}
              {daemon.errors?.join(", ")}
            </li>
          ))}
        </ul>
      ) : null}
      {links.length ? <div className="flex flex-wrap gap-2">
        {links.map(link => (
          <Button key={link.href} asChild size="sm" variant="outline">
            <a href={link.href}>{link.label}</a>
          </Button>
        ))}
      </div> : null}
    </section>
  );
}

export function DagsterLogControls({ errorsOnly, onFilter, onFirstPage, onNextPage }: {
  errorsOnly: boolean;
  onFilter: (errorsOnly: boolean) => void;
  onFirstPage?: () => void;
  onNextPage?: () => void;
}) {
  return (
    <div className="flex flex-wrap gap-2" aria-label="Dagster 로그 보기">
      <Button size="sm" variant="outline" aria-pressed={errorsOnly} onClick={() => onFilter(!errorsOnly)}>
        오류 로그만 보기
      </Button>
      {onFirstPage ? <Button size="sm" variant="outline" onClick={onFirstPage}>첫 로그 페이지</Button> : null}
      {onNextPage ? <Button size="sm" variant="outline" onClick={onNextPage}>다음 로그 페이지</Button> : null}
    </div>
  );
}
