# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"""native webserver에 영속 요청 식별자 mutation을 선택적으로 추가한다."""

from __future__ import annotations

import hashlib
import json
from importlib.metadata import version
from uuid import UUID, uuid5

_NAMESPACE = UUID("ae499c92-88dd-5c9d-9629-8187b5d94b98")
_REQUEST_TAG = "kortravel/idempotent-request-sha256"


def _check_versions() -> None:
    """검증한 SDK 조합만 선택 진입점에서 허용한다."""
    versions = [version(name) for name in ("dagster", "dagster-graphql", "dagster-webserver")]
    if len(set(versions)) != 1 or versions[0] not in {"1.13.24", "1.13.25"}:
        raise RuntimeError("같은 버전의 Dagster 1.13.24 또는 1.13.25가 필요합니다")


def _conflict(field: str):
    from dagster_graphql.implementation.utils import UserFacingGraphQLError
    from dagster_graphql.schema.errors import GrapheneConflictingExecutionParamsError

    error = GrapheneConflictingExecutionParamsError(field)
    error.message = f"멱등 제출 요청이 지원 범위 또는 기존 요청과 다릅니다: {field}"
    raise UserFacingGraphQLError(error)


def _canonical(value) -> str:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False
    )


def _validate_shape(request_id: str, values) -> str:
    """지원하지 않는 선택/재실행과 중복 태그를 조용히 무시하지 않는다."""
    try:
        normalized = str(UUID(request_id))
    except (ValueError, TypeError, AttributeError):
        _conflict("requestId")
    if request_id.lower() != normalized:
        _conflict("requestId")
    if any(values.get(key) is not None for key in ("preset", "stepKeys")):
        _conflict("preset/stepKeys")
    selector = values["selector"]
    if any(
        selector.get(key) is not None
        for key in ("solidSelection", "assetSelection", "assetCheckSelection")
    ):
        _conflict("selector selection")
    if values.get("mode") not in (None, "default"):
        _conflict("mode")
    metadata = values.get("executionMetadata") or {}
    if any(metadata.get(key) is not None for key in ("rootRunId", "parentRunId")):
        _conflict("executionMetadata lineage")
    tags = metadata.get("tags") or []
    keys = [tag["key"] for tag in tags]
    if len(keys) != len(set(keys)) or any(
        key == _REQUEST_TAG or (key.startswith("dagster/") and key != "dagster/code_location")
        for key in keys
    ):
        _conflict("executionMetadata tags")
    if any(
        tag["key"] == "dagster/code_location"
        and tag["value"] != selector.get("repositoryLocationName")
        for tag in tags
    ):
        _conflict("dagster/code_location")
    return normalized


def _identity(request_id: str, params) -> tuple[str, str]:
    selector = params.selector
    scope = [selector.location_name, selector.repository_name, selector.job_name]
    run_id = str(uuid5(_NAMESPACE, _canonical([scope, request_id])))
    try:
        body = _canonical([scope, params.run_config, dict(params.execution_metadata.tags)])
    except (ValueError, TypeError):
        _conflict("runConfigData")
    return run_id, hashlib.sha256(body.encode()).hexdigest()


def _same_request(run, params, digest: str) -> None:
    """기존 native 행의 요청·원천이 다르면 replay로 공개하지 않는다."""
    origin = run.remote_job_origin
    selector = params.selector
    if (
        origin is None
        or origin.repository_origin.code_location_origin.location_name != selector.location_name
        or origin.repository_origin.repository_name != selector.repository_name
        or run.job_name != selector.job_name
        or run.run_config != params.run_config
        or run.tags.get(_REQUEST_TAG) != digest
        or any(run.tags.get(key) != value for key, value in params.execution_metadata.tags.items())
        or run.root_run_id is not None
        or run.parent_run_id is not None
        or run.op_selection is not None
        or run.asset_selection is not None
        or run.asset_check_selection is not None
    ):
        _conflict("requestId")


async def _launch(info, request_id: str, values):
    from dagster._core.definitions.selector import JobSelector
    from dagster._core.errors import DagsterRunAlreadyExists
    from dagster._core.run_coordinator.queued_run_coordinator import QueuedRunCoordinator
    from dagster._core.storage.dagster_run import DagsterRunStatus, RunsFilter
    from dagster._core.workspace.permissions import Permissions
    from dagster_graphql.implementation.execution.run_lifecycle import create_valid_pipeline_run
    from dagster_graphql.implementation.external import get_remote_job_or_raise
    from dagster_graphql.implementation.utils import assert_permission_for_job
    from dagster_graphql.schema.pipelines.pipeline import GrapheneRun
    from dagster_graphql.schema.roots.mutation import create_execution_params

    normalized = _validate_shape(request_id, values)
    params = await create_execution_params(info, values)
    assert_permission_for_job(
        info,
        Permissions.LAUNCH_PIPELINE_EXECUTION,
        JobSelector(
            location_name=params.selector.location_name,
            repository_name=params.selector.repository_name,
            job_name=params.selector.job_name,
        ),
    )
    instance = info.context.instance
    # 즉시 launcher를 실행하는 coordinator에서는 동시 재제출 안전성을 약속하지 않는다.
    if type(instance.run_coordinator) is not QueuedRunCoordinator:
        _conflict("runCoordinator")
    run_id, digest = _identity(normalized, params)
    run = instance.get_run_by_id(run_id)
    replayed = run is not None
    if run is None:
        remote_job = await get_remote_job_or_raise(info, params.selector)
        metadata = params.execution_metadata._replace(
            run_id=run_id, tags={**params.execution_metadata.tags, _REQUEST_TAG: digest}
        )
        try:
            run = create_valid_pipeline_run(
                info.context, remote_job, params._replace(execution_metadata=metadata)
            )
        except DagsterRunAlreadyExists:
            # 유일 키 충돌만 재조회한다. RPC/설정/DB 장애를 성공으로 바꾸지 않는다.
            run = instance.get_run_by_id(run_id)
            if run is None:
                raise
            replayed = True
    _same_request(run, params, digest)
    if run.status == DagsterRunStatus.NOT_STARTED:
        instance.submit_run(run_id, workspace=info.context)
    records = instance.get_run_records(RunsFilter(run_ids=[run_id]))
    if len(records) != 1:
        raise RuntimeError("native run 조회 결과가 하나가 아닙니다")
    return GrapheneRun(records[0]), replayed


def create_schema():
    """기존 query/subscription/mutation을 보존한 opt-in schema를 만든다."""
    _check_versions()
    import graphene
    from dagster._core.workspace.permissions import Permissions
    from dagster_graphql.implementation.utils import capture_error, require_permission_check
    from dagster_graphql.schema import types
    from dagster_graphql.schema.inputs import GrapheneExecutionParams
    from dagster_graphql.schema.pipelines.pipeline import GrapheneRun
    from dagster_graphql.schema.roots.mutation import GrapheneMutation
    from dagster_graphql.schema.roots.query import GrapheneQuery
    from dagster_graphql.schema.roots.subscription import GrapheneSubscription
    from dagster_graphql.schema.runs import GrapheneLaunchRunResult, GrapheneLaunchRunSuccess

    class IdempotentLaunchRunSuccess(graphene.ObjectType):
        run = graphene.NonNull(GrapheneRun)
        replayed = graphene.NonNull(graphene.Boolean)

    class IdempotentLaunchRunResult(graphene.Union):
        class Meta:
            types = (IdempotentLaunchRunSuccess,) + tuple(
                item
                for item in GrapheneLaunchRunResult._meta.types
                if item is not GrapheneLaunchRunSuccess
            )

    class LaunchIdempotentRun(graphene.Mutation):
        class Arguments:
            requestId = graphene.String(required=True)
            executionParams = GrapheneExecutionParams(required=True)

        Output = graphene.NonNull(IdempotentLaunchRunResult)

        @capture_error
        @require_permission_check(Permissions.LAUNCH_PIPELINE_EXECUTION)
        async def mutate(self, info, requestId, executionParams):
            run, replayed = await _launch(info, requestId, executionParams)
            return IdempotentLaunchRunSuccess(run=run, replayed=replayed)

    class Mutation(GrapheneMutation):
        launchIdempotentRun = LaunchIdempotentRun.Field()

        class Meta:
            name = "Mutation"

    return graphene.Schema(
        query=GrapheneQuery, mutation=Mutation, subscription=GrapheneSubscription, types=types()
    )


def main() -> None:
    """별도 프로세스 없이 기존 native CLI 인자를 그대로 처리한다."""
    _check_versions()
    from dagster_webserver import app, cli
    from dagster_webserver.webserver import DagsterWebserver

    class IdempotentWebserver(DagsterWebserver):
        def build_graphql_schema(self):
            return create_schema()

    app.DagsterWebserver = IdempotentWebserver
    cli.main()


if __name__ == "__main__":
    main()
