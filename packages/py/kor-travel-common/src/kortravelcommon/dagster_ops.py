# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)

"""Dagster 운영 UI의 상태 조회 및 실행 단위 제어 계약."""

from __future__ import annotations

from collections.abc import Awaitable, Callable, Iterable
from enum import StrEnum
from typing import Any, TypedDict
from uuid import NAMESPACE_URL, UUID, uuid5

GraphQL = Callable[[str, dict[str, object]], Awaitable[dict[str, Any]]]

DAEMON_HEALTH_FIELDS = """
  instance {
    daemonHealth {
      allDaemonStatuses {
        daemonType required healthy lastHeartbeatTime
        lastHeartbeatErrors { className }
      }
    }
  }
"""

_RUN = """
query DagsterOperatorRun($runId: ID!) {
  runOrError(runId: $runId) {
    __typename
    ... on Run {
      runId status canTerminate jobName
      mode solidSelection stepKeysToExecute assetSelectionCount assetCheckSelectionCount
      repositoryOrigin { repositoryLocationName repositoryName }
      tags { key }
    }
  }
}
"""

_ACTIVE_CHILDREN = """
query DagsterOperatorActiveRetry($parentId: String!) {
  runsOrError(filter: {
    tags: [{key: "dagster/parent_run_id", value: $parentId}],
    statuses: [NOT_STARTED, QUEUED, STARTING, STARTED, CANCELING]
  }, limit: 1) {
    __typename
    ... on Runs { results { runId } }
  }
}
"""

_FORCE_CANCEL = """
mutation DagsterOperatorForceCancel($runId: String!) {
  terminateRun(runId: $runId, terminatePolicy: MARK_AS_CANCELED_IMMEDIATELY) {
    __typename
    ... on TerminateRunSuccess { run { runId } }
  }
}
"""

_REEXECUTE_INPUT = """
query DagsterOperatorReplayConfig($runId: ID!) {
  runOrError(runId: $runId) {
    __typename
    ... on Run {
      runId status runConfig
      repositoryOrigin { repositoryLocationName repositoryName }
    }
  }
}
"""

_FULL_PLAN = """
query DagsterOperatorFullPlan($pipeline: PipelineSelector!, $config: RunConfigData) {
  executionPlanOrError(pipeline: $pipeline, mode: "default", runConfigData: $config) {
    __typename
    ... on ExecutionPlan { steps { key } }
  }
}
"""

_REEXECUTE = """
mutation DagsterOperatorReexecute($requestId: String!, $params: ExecutionParams!) {
  launchIdempotentRun(requestId: $requestId, executionParams: $params) {
    __typename
    ... on IdempotentLaunchRunSuccess { run { runId } }
  }
}
"""

_LINEAGE_TAGS = frozenset(
    {
        "dagster/partition",
        "dagster/partition_set",
        "dagster/backfill",
        "dagster/root_run_id",
        "dagster/parent_run_id",
    }
)


class RunAction(StrEnum):
    FORCE_CANCEL = "force-cancel"
    REEXECUTE = "reexecute"


class RunControlError(RuntimeError):
    """실제 GraphQL 오류 본문 없이 운영 API가 반환할 오류 분류."""

    def __init__(self, code: str):
        super().__init__(code)
        self.code = code


def _record(value: object) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


class DaemonStatus(TypedDict):
    daemon_type: str
    required: bool
    healthy: bool | None
    last_heartbeat_time: float | None
    error_classes: list[str]


def parse_daemon_statuses(instance: object) -> list[DaemonStatus]:
    """앱의 공용 운영 화면에 데몬 상태와 오류 유형만 전달한다."""
    statuses = _record(_record(instance).get("daemonHealth")).get("allDaemonStatuses")
    if not isinstance(statuses, list):
        return []
    result: list[DaemonStatus] = []
    for status in statuses:
        daemon = _record(status)
        name = daemon.get("daemonType")
        if not isinstance(name, str) or not name:
            continue
        healthy = daemon.get("healthy")
        heartbeat = daemon.get("lastHeartbeatTime")
        errors = daemon.get("lastHeartbeatErrors")
        error_classes = []
        if isinstance(errors, list):
            for error in errors:
                error_class = _record(error).get("className")
                if isinstance(error_class, str) and error_class:
                    error_classes.append(error_class)
        result.append(
            DaemonStatus(
                daemon_type=name,
                required=daemon.get("required") is True,
                healthy=healthy if isinstance(healthy, bool) else None,
                last_heartbeat_time=(
                    float(heartbeat)
                    if isinstance(heartbeat, int | float)
                    and not isinstance(heartbeat, bool)
                    and abs(heartbeat) <= 8.64e12
                    else None
                ),
                error_classes=error_classes,
            )
        )
    return result


def _result(payload: dict[str, Any], field: str) -> dict[str, Any]:
    value = _record(_record(payload.get("data")).get(field))
    if payload.get("errors") or not value:
        raise RunControlError("dagster_error")
    return value


def supports_full_reexecution(run: dict[str, Any], tag_keys: Iterable[str]) -> bool:
    """선택 범위와 파티션을 잃을 수 있는 실행은 전체 재실행 대상에서 뺀다."""
    return (
        run.get("mode") == "default"
        and "solidSelection" in run
        and run["solidSelection"] is None
        and "stepKeysToExecute" in run
        and (
            run["stepKeysToExecute"] is None
            or (
                isinstance(run["stepKeysToExecute"], list)
                and all(isinstance(step, str) for step in run["stepKeysToExecute"])
            )
        )
        and type(run.get("assetSelectionCount")) is int
        and run["assetSelectionCount"] == 0
        and type(run.get("assetCheckSelectionCount")) is int
        and run["assetCheckSelectionCount"] == 0
        and _LINEAGE_TAGS.isdisjoint(tag_keys)
    )


def run_actions(status: str, *, can_terminate: bool, has_app_state: bool) -> tuple[RunAction, ...]:
    """현재 확인한 상태에서 가능한 작업을 돌려준다."""
    if can_terminate and status in {"QUEUED", "STARTED"}:
        return (RunAction.FORCE_CANCEL,)
    if status == "FAILURE" and not has_app_state:
        return (RunAction.REEXECUTE,)
    return ()


async def execute_run_action(
    graphql: GraphQL,
    *,
    run_id: UUID,
    action: RunAction,
    location_name: str,
    repository_name: str,
    app_state_tags: Iterable[str] = (),
) -> UUID:
    """공용 instance에서 호출자의 저장소에 속하는 실행만 변경한다.

    실제 요청 직전 상태를 읽는다. 전체 재실행을 원본 실행으로
    식별하는 키가 고정되므로 프로세스가 여러 개여도 같은 대체 실행을 돌려준다.
    """
    if not isinstance(action, RunAction):
        raise RunControlError("action_unavailable")
    if not all(
        isinstance(value, str) and value.strip() for value in (location_name, repository_name)
    ):
        raise RunControlError("dagster_error")
    protected = (
        frozenset((app_state_tags,))
        if isinstance(app_state_tags, str)
        else frozenset(app_state_tags)
    )
    if any(not isinstance(key, str) or not key or key.startswith(".dagster/") for key in protected):
        raise RunControlError("dagster_error")
    identifier = str(run_id)
    run = _result(await graphql(_RUN, {"runId": identifier}), "runOrError")
    if run.get("__typename") == "RunNotFoundError":
        raise RunControlError("run_not_found")
    if run.get("__typename") != "Run":
        raise RunControlError("dagster_error")
    origin = _record(run.get("repositoryOrigin"))
    if (
        run.get("runId") != identifier
        or origin.get("repositoryLocationName") != location_name
        or origin.get("repositoryName") != repository_name
    ):
        raise RunControlError("run_not_found")
    status = run.get("status")
    tags = run.get("tags")
    if not isinstance(status, str) or not isinstance(tags, list):
        raise RunControlError("dagster_error")
    known_keys: set[str] = set()
    for tag in tags:
        key = _record(tag).get("key")
        if not isinstance(key, str) or key in known_keys:
            raise RunControlError("dagster_error")
        known_keys.add(key)
    if action not in run_actions(
        status,
        can_terminate=run.get("canTerminate") is True,
        has_app_state=(
            not known_keys.isdisjoint(protected) or not supports_full_reexecution(run, known_keys)
        ),
    ):
        raise RunControlError("action_unavailable")

    if action is RunAction.FORCE_CANCEL:
        response = await graphql(_FORCE_CANCEL, {"runId": identifier})
        result = _result(response, "terminateRun")
        if result.get("__typename") == "TerminateRunFailure":
            raise RunControlError("action_unavailable")
        expected = "TerminateRunSuccess"
    else:
        children = _result(await graphql(_ACTIVE_CHILDREN, {"parentId": identifier}), "runsOrError")
        if children.get("__typename") != "Runs" or not isinstance(children.get("results"), list):
            raise RunControlError("dagster_error")
        if children["results"]:
            raise RunControlError("action_unavailable")
        job_name = run.get("jobName")
        config = _result(await graphql(_REEXECUTE_INPUT, {"runId": identifier}), "runOrError")
        config_origin = _record(config.get("repositoryOrigin"))
        if (
            not isinstance(job_name, str)
            or not job_name
            or config.get("__typename") != "Run"
            or config.get("runId") != identifier
            or config.get("status") != "FAILURE"
            or config_origin.get("repositoryLocationName") != location_name
            or config_origin.get("repositoryName") != repository_name
            or not isinstance(config.get("runConfig"), dict)
        ):
            raise RunControlError("dagster_error")
        params: dict[str, object] = {
            "selector": {
                "repositoryLocationName": location_name,
                "repositoryName": repository_name,
                "jobName": job_name,
            },
            "runConfigData": config["runConfig"],
        }
        selected = run["stepKeysToExecute"]
        if isinstance(selected, list):
            plan = _result(
                await graphql(
                    _FULL_PLAN,
                    {
                        "pipeline": {
                            "repositoryLocationName": location_name,
                            "repositoryName": repository_name,
                            "pipelineName": job_name,
                        },
                        "config": config["runConfig"],
                    },
                ),
                "executionPlanOrError",
            )
            steps = plan.get("steps")
            if plan.get("__typename") != "ExecutionPlan" or not isinstance(steps, list):
                raise RunControlError("dagster_error")
            keys = [_record(step).get("key") for step in steps]
            if any(not isinstance(key, str) for key in keys):
                raise RunControlError("dagster_error")
            if set(selected) != set(keys):
                raise RunControlError("action_unavailable")
        params["executionMetadata"] = {
            "tags": [
                {"key": "dagster/code_location", "value": location_name},
                {"key": "kortravel/operator-source-run", "value": identifier},
            ],
        }
        response = await graphql(
            _REEXECUTE,
            {
                "requestId": str(uuid5(NAMESPACE_URL, "kortravel:dagster:reexecute:" + identifier)),
                "params": params,
            },
        )
        result = _result(response, "launchIdempotentRun")
        expected = "IdempotentLaunchRunSuccess"

    if result.get("__typename") != expected:
        raise RunControlError("dagster_error")
    observed = _record(result.get("run")).get("runId")
    try:
        result_id = UUID(observed)
    except (TypeError, ValueError, AttributeError) as exc:
        raise RunControlError("dagster_error") from exc
    if (action is RunAction.FORCE_CANCEL) != (result_id == run_id):
        raise RunControlError("dagster_error")
    return result_id
