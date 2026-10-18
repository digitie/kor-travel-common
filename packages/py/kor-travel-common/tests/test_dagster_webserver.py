# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"""실제 native schema/SQLite를 사용하며 provider·daemon·job은 실행하지 않는다."""

import asyncio
import copy
import importlib
import json
import subprocess
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from types import SimpleNamespace
from uuid import uuid4

import pytest

pytest.importorskip("dagster_graphql")
pytest.importorskip("dagster_webserver")

from dagster import DagsterInstance, job, op
from dagster._core.execution.api import create_execution_plan
from dagster._core.remote_representation.external import RemoteExecutionPlan, RemoteJob
from dagster._core.remote_representation.external_data import JobDataSnap
from dagster._core.remote_representation.handle import RepositoryHandle
from dagster._core.snap.execution_plan_snapshot import snapshot_from_execution_plan
from dagster._core.storage.dagster_run import DagsterRunStatus
from dagster_graphql.implementation.utils import UserFacingGraphQLError
from dagster_graphql.schema import create_schema as native_schema

from kortravelcommon import dagster_webserver as adapter


@op(config_schema={"value": str})
def item():
    raise AssertionError("fixture job을 실행하면 안 됩니다")


@job
def refresh():
    item()


class Context:
    def __init__(self, instance, allowed=True):
        self.instance = instance
        self.asset_graph = None
        self.allowed = allowed
        self.checked = []

    def has_permission_for_selector(self, permission, selector):
        self.checked.append((permission, selector))
        return self.allowed

    def was_permission_checked(self, permission):
        return any(p == permission for p, _ in self.checked)


@pytest.fixture
def native_storage_config():
    return {}


@pytest.fixture
def native(tmp_path, monkeypatch, native_storage_config):
    overrides = {
        "run_coordinator": {
            "module": "dagster._core.run_coordinator",
            "class": "QueuedRunCoordinator",
        },
        "telemetry": {"enabled": False},
    }
    overrides.update(native_storage_config)
    with DagsterInstance.local_temp(str(tmp_path), overrides=overrides) as instance:
        remote = RemoteJob(
            JobDataSnap.from_job_def(refresh, include_parent_snapshot=True),
            RepositoryHandle.for_test(location_name="owned", repository_name="repo"),
        )
        external = importlib.import_module("dagster_graphql.implementation.external")
        lifecycle = importlib.import_module(
            "dagster_graphql.implementation.execution.run_lifecycle"
        )

        async def get_remote(info, selector):
            assert selector.location_name == "owned"
            return remote

        def plan(graphql_context, remote_job, run_config, step_keys_to_execute, known_state):
            # RPC만 소유 in-memory 정의로 대체하고 native config/create/submit은 실행한다.
            assert known_state is None
            value = create_execution_plan(refresh, run_config=run_config)
            snapshot = snapshot_from_execution_plan(value, refresh.get_job_snapshot_id())
            return RemoteExecutionPlan(snapshot)

        monkeypatch.setattr(external, "get_remote_job_or_raise", get_remote)
        monkeypatch.setattr(lifecycle, "get_remote_execution_plan_or_raise", plan)
        yield SimpleNamespace(instance=instance, context=Context(instance), remote=remote)


def values(value="a"):
    return {
        "selector": {
            "repositoryLocationName": "owned",
            "repositoryName": "repo",
            "jobName": "refresh",
        },
        "runConfigData": {"ops": {"item": {"config": {"value": value}}}},
        "executionMetadata": {
            "tags": [
                {"key": "consumer/request", "value": "safe"},
                {"key": "dagster/code_location", "value": "owned"},
            ]
        },
    }


def launch(native, request_id=None, data=None, context=None):
    return asyncio.run(
        adapter._launch(
            SimpleNamespace(context=context or native.context),
            request_id or str(uuid4()),
            data or values(),
        )
    )


def run_id(result):
    return result[0].runId


def test_schema_preserves_native_fields():
    old, new = native_schema().graphql_schema, adapter.create_schema().graphql_schema
    assert set(new.mutation_type.fields) == set(old.mutation_type.fields) | {"launchIdempotentRun"}
    for key in old.mutation_type.fields:
        assert str(new.mutation_type.fields[key].type) == str(old.mutation_type.fields[key].type)
    field = new.mutation_type.fields["launchIdempotentRun"]
    assert {key: str(arg.type) for key, arg in field.args.items()} == {
        "executionParams": "ExecutionParams!",
        "requestId": "String!",
    }
    assert set(new.get_type("IdempotentLaunchRunSuccess").fields) == {"run", "replayed"}
    assert set(new.query_type.fields) == set(old.query_type.fields)


def test_real_create_submit_replay_and_restart(native):
    request_id = str(uuid4())
    data = values()
    original = copy.deepcopy(data)
    first = launch(native, request_id, data)
    second = launch(native, request_id, data, Context(native.instance))
    assert first[1] is False and second[1] is True
    assert run_id(first) == run_id(second)
    assert native.instance.get_runs_count() == 1
    assert native.instance.get_run_by_id(run_id(first)).status == DagsterRunStatus.QUEUED
    assert data == original
    assert len(native.context.checked) == 1


@pytest.mark.parametrize("change", ["config", "tags"])
def test_same_request_conflict(native, change):
    request_id = str(uuid4())
    launch(native, request_id)
    changed = values("different" if change == "config" else "a")
    if change == "tags":
        changed["executionMetadata"]["tags"][0]["value"] = "changed"
    with pytest.raises(UserFacingGraphQLError) as error:
        launch(native, request_id, changed)
    assert type(error.value.error).__name__ == "GrapheneConflictingExecutionParamsError"
    assert native.instance.get_runs_count() == 1


def test_permission_on_new_and_replay(native):
    request_id = str(uuid4())
    denied = Context(native.instance, allowed=False)
    with pytest.raises(UserFacingGraphQLError) as error:
        launch(native, request_id, context=denied)
    assert type(error.value.error).__name__ == "GrapheneUnauthorizedError"
    assert native.instance.get_runs_count() == 0
    launch(native, request_id)
    with pytest.raises(UserFacingGraphQLError):
        launch(native, request_id, context=denied)
    assert native.instance.get_runs_count() == 1


@pytest.mark.parametrize(
    "status",
    [
        DagsterRunStatus.STARTING,
        DagsterRunStatus.STARTED,
        DagsterRunStatus.SUCCESS,
        DagsterRunStatus.FAILURE,
        DagsterRunStatus.CANCELED,
        DagsterRunStatus.CANCELING,
    ],
)
def test_non_not_started_does_not_resubmit(native, monkeypatch, status):
    request_id = str(uuid4())
    result = launch(native, request_id)
    from dagster._core.events import DagsterEvent, DagsterEventType

    # 상태 이벤트는 실제 native 저장소로 기록한다.
    native.instance.report_dagster_event(
        DagsterEvent(DagsterEventType.PIPELINE_START.value, "refresh"),
        run_id(result),
    )
    storage = native.instance.run_storage
    # 모든 상태별 replay 분기를 저장소 조회 경계에서 주입한다(실행은 하지 않음).
    original = native.instance.get_run_by_id
    monkeypatch.setattr(
        native.instance, "get_run_by_id", lambda key: original(key)._replace(status=status)
    )
    monkeypatch.setattr(native.instance, "submit_run", lambda *a, **k: pytest.fail("재제출 금지"))
    assert launch(native, request_id)[1] is True
    assert storage.get_runs_count() == 1


def test_create_submit_interruption_recovers_same_id(native, monkeypatch):
    request_id = str(uuid4())
    original = native.instance.submit_run

    def interrupted(*args, **kwargs):
        raise RuntimeError("owned interruption")

    monkeypatch.setattr(native.instance, "submit_run", interrupted)
    with pytest.raises(RuntimeError, match="owned interruption"):
        launch(native, request_id)
    pending = native.instance.get_runs()[0]
    assert pending.status == DagsterRunStatus.NOT_STARTED
    monkeypatch.setattr(native.instance, "submit_run", original)
    result = launch(native, request_id, context=Context(native.instance))
    assert result[1] is True and run_id(result) == pending.run_id
    assert native.instance.get_runs_count() == 1
    assert native.instance.get_run_by_id(pending.run_id).status == DagsterRunStatus.QUEUED


def test_concurrent_create_native_unique(native, monkeypatch):
    request_id = str(uuid4())
    barrier = threading.Barrier(2)
    lifecycle = importlib.import_module("dagster_graphql.implementation.execution.run_lifecycle")
    original = lifecycle.create_valid_pipeline_run

    def create(*args, **kwargs):
        barrier.wait(timeout=10)
        return original(*args, **kwargs)

    monkeypatch.setattr(lifecycle, "create_valid_pipeline_run", create)
    with ThreadPoolExecutor(2) as pool:
        futures = [
            pool.submit(launch, native, request_id, None, Context(native.instance))
            for _ in range(2)
        ]
        results = []
        for future in futures:
            try:
                results.append(future.result(timeout=20))
            except adapter.SubmissionBusyError:
                results.append(None)
    results = [
        item or launch(native, request_id, context=Context(native.instance)) for item in results
    ]
    assert len({run_id(item) for item in results}) == 1
    assert sorted(item[1] for item in results) == [False, True]
    assert native.instance.get_runs_count() == 1


def test_late_first_create_after_second_response(native, monkeypatch):
    external = importlib.import_module("dagster_graphql.implementation.external")
    original = external.get_remote_job_or_raise

    async def scenario():
        entered, release = asyncio.Event(), asyncio.Event()
        calls = 0

        async def delayed(*args):
            nonlocal calls
            calls += 1
            if calls == 1:
                entered.set()
                await release.wait()
            return await original(*args)

        monkeypatch.setattr(external, "get_remote_job_or_raise", delayed)
        request_id = str(uuid4())
        info = SimpleNamespace(context=native.context)
        first = asyncio.create_task(adapter._launch(info, request_id, values()))
        await entered.wait()
        second = await adapter._launch(info, request_id, values())
        release.set()
        late = await first
        assert run_id(second) == run_id(late)
        assert second[1] is False and late[1] is True

    asyncio.run(scenario())
    assert native.instance.get_runs_count() == 1


@pytest.mark.parametrize(
    "field,setting",
    [
        ("preset", "named"),
        ("stepKeys", []),
        ("mode", "unknown"),
        ("rootRunId", "parent"),
        ("parentRunId", "parent"),
        ("solidSelection", []),
        ("assetSelection", []),
        ("assetCheckSelection", []),
        ("tags", [{"key": "same", "value": "1"}, {"key": "same", "value": "2"}]),
        ("tags", [{"key": "dagster/is_resume_retry", "value": "true"}]),
        ("tags", [{"key": adapter._REQUEST_TAG, "value": "forged"}]),
    ],
)
def test_unsupported_shape_is_explicitly_rejected(native, field, setting):
    data = values()
    if field in {"rootRunId", "parentRunId", "tags"}:
        data["executionMetadata"][field] = setting
    elif field.endswith("Selection"):
        data["selector"][field] = setting
    else:
        data[field] = setting
    with pytest.raises(UserFacingGraphQLError):
        launch(native, data=data)
    assert native.instance.get_runs_count() == 0


@pytest.mark.parametrize("value", ["", "invalid", "{" + str(uuid4()) + "}", uuid4().hex])
def test_invalid_uuid(native, value):
    with pytest.raises(UserFacingGraphQLError):
        launch(native, request_id=value or "invalid")


def test_native_config_validation_is_kept(native):
    data = values()
    data["runConfigData"] = {"ops": {"item": {"config": {"value": 123}}}}
    with pytest.raises(UserFacingGraphQLError) as error:
        launch(native, data=data)
    assert type(error.value.error).__name__ == "GrapheneRunConfigValidationInvalid"
    assert native.instance.get_runs_count() == 0


def test_native_graphql_errors_and_success(native):
    query = """mutation($id:String!,$params:ExecutionParams!){
      launchIdempotentRun(requestId:$id,executionParams:$params){
        __typename ... on IdempotentLaunchRunSuccess{replayed run{runId status}}
        ... on UnauthorizedError{message} ... on ConflictingExecutionParamsError{message}
      }}"""
    schema = adapter.create_schema()
    request_id = str(uuid4())

    def execute(context, data):
        return asyncio.run(
            schema.execute_async(
                query,
                variable_values={
                    "id": request_id,
                    "params": data,
                },
                context_value=context,
            )
        )

    result = execute(native.context, values())
    assert result.errors is None
    assert result.data["launchIdempotentRun"]["__typename"] == "IdempotentLaunchRunSuccess"
    assert result.data["launchIdempotentRun"]["run"]["status"] == "QUEUED"
    denied = execute(Context(native.instance, allowed=False), values())
    assert denied.errors is None
    assert denied.data["launchIdempotentRun"]["__typename"] == "UnauthorizedError"
    conflict = execute(native.context, values("changed"))
    assert conflict.errors is None
    assert conflict.data["launchIdempotentRun"]["__typename"] == "ConflictingExecutionParamsError"


def test_cli_preserves_arguments_and_same_process(monkeypatch):
    from dagster_webserver import app, cli

    original = app.DagsterWebserver
    argv = [
        "kortravelcommon.dagster_webserver",
        "-h",
        "127.0.0.1",
        "-p",
        "12345",
        "-w",
        "owned.yaml",
    ]
    monkeypatch.setattr(sys, "argv", argv)
    calls = []

    def native_main():
        calls.append(sys.argv[:])
        schema = app.DagsterWebserver.__new__(app.DagsterWebserver).build_graphql_schema()
        assert "launchIdempotentRun" in schema.graphql_schema.mutation_type.fields

    monkeypatch.setattr(cli, "main", native_main)
    try:
        adapter.main()
    finally:
        app.DagsterWebserver = original
    assert calls == [argv]


def test_cli_help_subprocess():
    # 소유 process는 --help만 처리하며 서버·socket·DB를 열지 않는다.
    source = str(importlib.import_module("kortravelcommon").__path__[0])
    code = (
        "import sys;sys.path.insert(0,"
        + repr(str(__import__("pathlib").Path(source).parent))
        + ");"
        "from kortravelcommon.dagster_webserver import main;sys.argv=['owned','--help'];main()"
    )
    result = subprocess.run(
        [sys.executable, "-I", "-B", "-c", code], capture_output=True, text=True, timeout=30
    )
    assert result.returncode == 0
    assert "--workspace" in result.stdout


def test_default_import_is_lazy():
    source = str(__import__("pathlib").Path(adapter.__file__).parents[1])
    code = (
        "import sys;sys.path.insert(0," + repr(source) + ");"
        "import kortravelcommon.dagster_webserver;"
        "assert not any(k.startswith('dagster') for k in sys.modules)"
    )
    subprocess.run([sys.executable, "-I", "-B", "-c", code], check=True, timeout=15)


def test_consumer_code_location_tag_must_match_selector(native):
    request_id = str(uuid4())
    result = launch(native, request_id)
    assert native.instance.get_run_by_id(run_id(result)).tags["dagster/code_location"] == "owned"
    bad = values()
    bad["executionMetadata"]["tags"][-1]["value"] = "another-consumer"
    with pytest.raises(UserFacingGraphQLError):
        launch(native, str(uuid4()), bad)
    assert native.instance.get_runs_count() == 1


def test_reopen_native_instance_replays_without_submit(native, monkeypatch):
    from dagster import DagsterInstance

    request_id = str(uuid4())
    first = launch(native, request_id)
    with DagsterInstance.from_ref(native.instance.get_ref()) as reopened:
        monkeypatch.setattr(
            reopened, "submit_run", lambda *a, **k: pytest.fail("queued 재제출 금지")
        )
        result = launch(native, request_id, context=Context(reopened))
        assert result[1] is True and run_id(first) == run_id(result)
        assert reopened.get_runs_count() == 1


def test_native_unique_conflict_with_unrelated_run_is_not_replay(native):
    from dagster_graphql.schema.roots.mutation import create_execution_params

    params = asyncio.run(create_execution_params(SimpleNamespace(context=native.context), values()))
    request_id = str(uuid4())
    key, _ = adapter._identity(request_id, params)
    native.instance.create_run_for_job(refresh, run_id=key, run_config=values()["runConfigData"])
    with pytest.raises(UserFacingGraphQLError):
        launch(native, request_id)
    assert native.instance.get_runs_count() == 1


def test_other_create_failure_does_not_become_success(native, monkeypatch):
    lifecycle = importlib.import_module("dagster_graphql.implementation.execution.run_lifecycle")

    def fail(*args, **kwargs):
        raise OSError("owned DB failure")

    monkeypatch.setattr(lifecycle, "create_valid_pipeline_run", fail)
    with pytest.raises(OSError, match="owned DB failure"):
        launch(native)
    assert native.instance.get_runs_count() == 0


def test_nonqueued_coordinator_is_rejected(native, monkeypatch):
    from dagster._core.run_coordinator.sync_in_memory_run_coordinator import (
        SyncInMemoryRunCoordinator,
    )

    monkeypatch.setattr(native.instance, "_run_coordinator", SyncInMemoryRunCoordinator())
    with pytest.raises(UserFacingGraphQLError):
        launch(native)
    assert native.instance.get_runs_count() == 0


def test_separate_process_resumes_not_started_native_run(native, monkeypatch, tmp_path):
    from dagster._serdes import serialize_value

    request_id = str(uuid4())
    original = native.instance.submit_run

    def stop_before_submit(*args, **kwargs):
        raise RuntimeError("owned process interruption")

    monkeypatch.setattr(native.instance, "submit_run", stop_before_submit)
    with pytest.raises(RuntimeError):
        launch(native, request_id)
    pending = native.instance.get_runs()[0]
    assert pending.status == DagsterRunStatus.NOT_STARTED
    monkeypatch.setattr(native.instance, "submit_run", original)
    source = str(__import__("pathlib").Path(adapter.__file__).parents[1])
    code = """
import sys,json,asyncio
from types import SimpleNamespace
sys.path.insert(0,sys.argv[1])
from dagster import DagsterInstance
from dagster._serdes import deserialize_value
from dagster._core.instance.ref import InstanceRef
from kortravelcommon.dagster_webserver import _launch
value=json.loads(sys.stdin.readline())
with DagsterInstance.from_ref(deserialize_value(value['ref'],InstanceRef)) as instance:
    context=SimpleNamespace(instance=instance,has_permission_for_selector=lambda *args:True)
    result=asyncio.run(_launch(SimpleNamespace(context=context),value['id'],value['params']))
    print(json.dumps({'run_id':result[0].runId,'replayed':result[1],
                      'count':instance.get_runs_count()}))
"""
    import os

    env = {
        "PATH": os.defpath,
        "HOME": str(tmp_path),
        "TMPDIR": str(tmp_path),
        "PYTHONDONTWRITEBYTECODE": "1",
    }
    result = subprocess.run(
        [sys.executable, "-I", "-B", "-c", code, source],
        input=json.dumps(
            {
                "ref": serialize_value(native.instance.get_ref()),
                "id": request_id,
                "params": values(),
            }
        ),
        text=True,
        capture_output=True,
        timeout=30,
        env=env,
    )
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout) == {"run_id": pending.run_id, "replayed": True, "count": 1}
    assert native.instance.get_run_by_id(pending.run_id).status == DagsterRunStatus.QUEUED


def test_lost_response_after_native_submit_replays_without_resubmit(native, monkeypatch):
    request_id = str(uuid4())
    original = native.instance.submit_run
    calls = []

    def submit_then_lost(*args, **kwargs):
        calls.append(args[0])
        original(*args, **kwargs)
        raise TimeoutError("owned response lost")

    monkeypatch.setattr(native.instance, "submit_run", submit_then_lost)
    with pytest.raises(TimeoutError):
        launch(native, request_id)
    pending = native.instance.get_runs()[0]
    assert pending.status == DagsterRunStatus.QUEUED
    result = launch(native, request_id)
    assert result[1] is True and run_id(result) == pending.run_id
    assert len(calls) == 1 and native.instance.get_runs_count() == 1


def test_stale_submit_cannot_regress_started_run(native, monkeypatch):
    from dagster._core.events import DagsterEvent, DagsterEventType

    request_id = str(uuid4())
    original_submit = native.instance.submit_run

    def interrupted(*args, **kwargs):
        raise RuntimeError("owned before submit")

    monkeypatch.setattr(native.instance, "submit_run", interrupted)
    with pytest.raises(RuntimeError):
        launch(native, request_id)
    row = native.instance.get_runs()[0]
    monkeypatch.setattr(native.instance, "submit_run", original_submit)
    coordinator = native.instance.run_coordinator
    original = coordinator.submit_run
    entered, release = threading.Event(), threading.Event()
    entries = []

    def delayed(context):
        entries.append(context.dagster_run.status)
        entered.set()
        assert release.wait(10)
        return original(context)

    monkeypatch.setattr(coordinator, "submit_run", delayed)
    with ThreadPoolExecutor(1) as pool:
        first = pool.submit(launch, native, request_id, None, Context(native.instance))
        try:
            assert entered.wait(10)
            with pytest.raises(adapter.SubmissionBusyError):
                launch(native, request_id, context=Context(native.instance))
        finally:
            release.set()
        result = first.result(timeout=15)
    native.instance.report_dagster_event(
        DagsterEvent(DagsterEventType.PIPELINE_START.value, "refresh"), row.run_id
    )
    assert native.instance.get_run_by_id(row.run_id).status == DagsterRunStatus.STARTED
    replay = launch(native, request_id)
    assert run_id(result) == run_id(replay) == row.run_id
    assert entries == [DagsterRunStatus.NOT_STARTED]
    records = native.instance.get_records_for_run(row.run_id).records
    events = [
        r.event_log_entry.dagster_event.event_type_value
        for r in records
        if r.event_log_entry.dagster_event
    ]
    assert events == ["PIPELINE_ENQUEUED", "PIPELINE_START"]
    assert native.instance.get_runs_count() == 1


def test_run_locks_are_distinct_and_exception_releases(native):
    first, second = str(uuid4()), str(uuid4())
    with pytest.raises(ValueError, match="owned"):
        with adapter._submission_lock(native.instance, first):
            with adapter._submission_lock(native.instance, second):
                with pytest.raises(adapter.SubmissionBusyError):
                    with adapter._submission_lock(native.instance, first):
                        pytest.fail("같은 run의 중첩 잠금 금지")
                raise ValueError("owned")
    with adapter._submission_lock(native.instance, first):
        pass


def test_process_crash_releases_lock(native, tmp_path):
    from dagster._serdes import serialize_value

    source = str(__import__("pathlib").Path(adapter.__file__).parents[1])
    key = str(uuid4())
    code = """
import sys,os,json
sys.path.insert(0,sys.argv[1])
from dagster import DagsterInstance
from dagster._serdes import deserialize_value
from dagster._core.instance.ref import InstanceRef
from kortravelcommon.dagster_webserver import _submission_lock
value=json.loads(sys.stdin.readline())
with DagsterInstance.from_ref(deserialize_value(value['ref'],InstanceRef)) as instance:
    with _submission_lock(instance,value['key']):
        print('locked',flush=True)
        sys.stdin.readline()
        os._exit(7)
"""
    child = subprocess.Popen(
        [sys.executable, "-I", "-B", "-c", code, source],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    try:
        child.stdin.write(
            json.dumps({"ref": serialize_value(native.instance.get_ref()), "key": key}) + "\n"
        )
        child.stdin.flush()
        assert child.stdout.readline().strip() == "locked"
        with pytest.raises(adapter.SubmissionBusyError):
            with adapter._submission_lock(native.instance, key):
                pytest.fail("살아 있는 프로세스의 잠금 금지")
        child.stdin.write("exit\n")
        child.stdin.flush()
        assert child.wait(timeout=15) == 7
        with adapter._submission_lock(native.instance, key):
            pass
    finally:
        if child.poll() is None:
            # 소유 fixture만 정상 EOF로 종료하며 다른 프로세스를 조작하지 않는다.
            child.stdin.close()
            child.wait(timeout=15)


def test_bound_connection_is_context_local_and_restores_original(native):
    storage = native.instance.run_storage
    with storage.connect() as original:
        with adapter._bound_run_connection(storage, original):
            with storage.connect() as bound:
                assert bound is original

            def another_thread():
                with storage.connect() as other:
                    assert other is not original
                    return native.instance.get_runs_count()

            with ThreadPoolExecutor(1) as pool:
                assert pool.submit(another_thread).result(timeout=10) == 0
        with storage.connect() as later:
            assert later is not original


@pytest.mark.parametrize("attribute", ["closed", "invalidated"])
def test_bound_connection_refuses_reconnect(native, attribute):
    storage = native.instance.run_storage
    connection = SimpleNamespace(closed=False, invalidated=False)
    setattr(connection, attribute, True)
    with adapter._bound_run_connection(storage, connection):
        with pytest.raises(RuntimeError, match="재연결"):
            with storage.connect():
                pytest.fail("끊긴 제출 session의 재연결 금지")
    with storage.connect() as normal:
        assert normal is not connection


def test_console_entrypoint_matches_same_process_main():
    from importlib.metadata import distribution

    entries = {entry.name: entry.value for entry in distribution("kor-travel-common").entry_points}
    assert entries["kor-travel-dagster-webserver"] == "kortravelcommon.dagster_webserver:main"
    executable = __import__("pathlib").Path(sys.executable).parent / "kor-travel-dagster-webserver"
    result = subprocess.run([str(executable), "--help"], capture_output=True, text=True, timeout=30)
    assert result.returncode == 0
    assert "--workspace" in result.stdout
