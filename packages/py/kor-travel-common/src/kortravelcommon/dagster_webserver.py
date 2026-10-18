# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"""native webserver에 영속 요청 식별자 mutation을 선택적으로 추가한다."""

from __future__ import annotations

import hashlib
import json
import os
import stat
import sys
from contextlib import contextmanager
from importlib.metadata import version
from pathlib import Path
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


class SubmissionBusyError(RuntimeError):
    """동일 run의 제출 중에는 같은 요청 식별자로 재시도해야 한다."""


@contextmanager
def _submission_lock(instance, run_id: str):
    """native 저장소와 run별로 재조회→제출을 직렬화하고 crash 때 자동 해제한다."""
    from dagster._core.storage.runs.sqlite.sqlite_run_storage import SqliteRunStorage
    from sqlalchemy import create_engine, text
    from sqlalchemy.engine import make_url
    from sqlalchemy.pool import NullPool

    if str(UUID(run_id)) != run_id:
        raise RuntimeError("정규 native run UUID가 필요합니다")
    storage = instance.run_storage
    if type(storage) is SqliteRunStorage:
        import fcntl

        database = make_url(storage._conn_string).database
        if not database or not os.path.isabs(database):
            raise RuntimeError("파일 기반 native SQLite 저장소가 필요합니다")
        directory = Path(database).resolve(strict=True).parent / ".kortravel-native-submit-locks"
        directory.mkdir(mode=0o700, exist_ok=True)
        parent_fd = os.open(directory, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        try:
            parent_stat = os.fstat(parent_fd)
            if parent_stat.st_uid != os.geteuid() or stat.S_IMODE(parent_stat.st_mode) != 0o700:
                raise RuntimeError(
                    "native SQLite 제출 잠금 디렉터리는 현재 사용자 0700이어야 합니다"
                )
            fd = os.open(
                run_id + ".lock",
                os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW,
                0o600,
                dir_fd=parent_fd,
            )
        finally:
            os.close(parent_fd)
        try:
            info = os.fstat(fd)
            if (
                not stat.S_ISREG(info.st_mode)
                or info.st_nlink != 1
                or info.st_uid != os.geteuid()
                or stat.S_IMODE(info.st_mode) != 0o600
            ):
                raise RuntimeError("native SQLite 제출 잠금은 단일 일반 파일이어야 합니다")
            try:
                fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError as error:
                raise SubmissionBusyError(
                    "native 제출 중입니다. 같은 requestId로 재시도하세요"
                ) from error
            yield
        finally:
            # unlink하면 병렬 호출이 다른 inode를 잠글 수 있어 파일은 유지한다.
            os.close(fd)
        return

    from dagster_postgres.run_storage import PostgresRunStorage

    if type(storage) is not PostgresRunStorage:
        raise RuntimeError("지원하는 native run 저장소가 아닙니다")
    expected = {"1.13.24": "0.29.24", "1.13.25": "0.29.25"}[version("dagster")]
    if version("dagster-postgres") != expected or storage._token_provider is not None:
        raise RuntimeError("검증한 버전의 URL 기반 native PostgreSQL 저장소가 필요합니다")
    key = int.from_bytes(
        hashlib.sha256(("kortravel/native-submit/" + run_id).encode()).digest()[:8],
        "big",
        signed=True,
    )
    # native engine pool을 잡은 채 submit의 추가 checkout을 기다리지 않는다.
    engine = create_engine(
        storage.postgres_url,
        poolclass=NullPool,
        connect_args={"connect_timeout": 5},
        isolation_level="AUTOCOMMIT",
    )
    try:
        with engine.connect() as connection:
            locked = connection.execute(
                text("SELECT pg_try_advisory_lock(:key)"), {"key": key}
            ).scalar_one()
            if not locked:
                raise SubmissionBusyError("native 제출 중입니다. 같은 requestId로 재시도하세요")
            try:
                yield
            finally:
                pending_error = sys.exc_info()[0] is not None
                try:
                    if not connection.execute(
                        text("SELECT pg_advisory_unlock(:key)"), {"key": key}
                    ).scalar_one():
                        raise RuntimeError("native 제출 잠금 해제를 확인하지 못했습니다")
                except Exception:
                    if not pending_error:
                        raise
    finally:
        # NullPool 실제 connection close는 unlock 예외/프로세스 종료 때도 session lock을 푼다.
        engine.dispose()


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
    with _submission_lock(instance, run_id):
        run = instance.get_run_by_id(run_id)
        if run is None:
            raise RuntimeError("native run이 제출 전에 사라졌습니다")
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
