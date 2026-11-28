import asyncio
from uuid import UUID

import pytest

from kortravelcommon.dagster_ops import RunAction, RunControlError, execute_run_action, run_actions

PARENT = UUID("1d012606-4215-4f42-8a97-ef106603899f")
CHILD = UUID("2d012606-4215-4f42-8a97-ef106603899f")


def _run(**overrides):
    return {
        "data": {
            "runOrError": {
                "__typename": "Run",
                "runId": str(PARENT),
                "jobName": "test-job",
                "status": "FAILURE",
                "canTerminate": False,
                "tags": [],
                "repositoryOrigin": {"repositoryLocationName": "geo", "repositoryName": "main"},
                "mode": "default",
                "solidSelection": None,
                "stepKeysToExecute": None,
                "assetSelectionCount": 0,
                "assetCheckSelectionCount": 0,
                **overrides,
            }
        }
    }


def test_force_cancel_uses_native_policy():
    async def graphql(query, variables):
        if "OperatorRun" in query:
            return _run(status="STARTED", canTerminate=True)
        assert "MARK_AS_CANCELED_IMMEDIATELY" in query
        assert variables == {"runId": str(PARENT)}
        return {
            "data": {
                "terminateRun": {"__typename": "TerminateRunSuccess", "run": {"runId": str(PARENT)}}
            }
        }

    assert (
        asyncio.run(
            execute_run_action(
                graphql,
                run_id=PARENT,
                action=RunAction.FORCE_CANCEL,
                location_name="geo",
                repository_name="main",
            )
        )
        == PARENT
    )


def test_reexecution_replays_config_with_same_request_id():
    request_ids = []

    async def graphql(query, variables):
        if "OperatorRun" in query:
            return _run(stepKeysToExecute=["stage-a", "stage-b"])
        if "ActiveRetry" in query:
            return {"data": {"runsOrError": {"__typename": "Runs", "results": []}}}
        if "ReplayConfig" in query:
            return {
                "data": {
                    "runOrError": {
                        "__typename": "Run",
                        "runId": str(PARENT),
                        "runConfig": {"ops": {}},
                        "status": "FAILURE",
                        "repositoryOrigin": {
                            "repositoryLocationName": "geo",
                            "repositoryName": "main",
                        },
                    }
                }
            }
        if "OperatorFullPlan" in query:
            assert variables == {
                "pipeline": {
                    "repositoryLocationName": "geo",
                    "repositoryName": "main",
                    "pipelineName": "test-job",
                },
                "config": {"ops": {}},
            }
            return {
                "data": {
                    "executionPlanOrError": {
                        "__typename": "ExecutionPlan",
                        "steps": [{"key": "stage-b"}, {"key": "stage-a"}],
                    }
                }
            }
        assert "launchIdempotentRun" in query
        request_ids.append(UUID(variables["requestId"]))
        params = variables["params"]
        assert params["selector"] == {
            "repositoryLocationName": "geo",
            "repositoryName": "main",
            "jobName": "test-job",
        }
        assert params["runConfigData"] == {"ops": {}}
        assert {"key": "kortravel/operator-source-run", "value": str(PARENT)} in params[
            "executionMetadata"
        ]["tags"]
        return {
            "data": {
                "launchIdempotentRun": {
                    "__typename": "IdempotentLaunchRunSuccess",
                    "run": {"runId": str(CHILD)},
                }
            }
        }

    async def request():
        return await execute_run_action(
            graphql,
            run_id=PARENT,
            action=RunAction.REEXECUTE,
            location_name="geo",
            repository_name="main",
        )

    async def concurrent():
        return await asyncio.gather(request(), request())

    assert asyncio.run(concurrent()) == [CHILD, CHILD]
    assert len(set(request_ids)) == 1


@pytest.mark.parametrize(
    "overrides,code",
    [
        ({"repositoryOrigin": {"repositoryName": "wrong"}}, "run_not_found"),
        ({"tags": [{"key": "geo.load_job"}]}, "action_unavailable"),
        ({"tags": [{"key": "dagster/partition"}]}, "action_unavailable"),
        ({"solidSelection": ["step"]}, "action_unavailable"),
        ({"stepKeysToExecute": ["step", None]}, "action_unavailable"),
        ({"assetSelectionCount": 1}, "action_unavailable"),
        ({"status": "CANCELED"}, "action_unavailable"),
    ],
)
def test_unsupported_reexecution_never_queries_config_or_mutates(overrides, code):
    async def graphql(query, _variables):
        assert "OperatorRun" in query
        return _run(**overrides)

    with pytest.raises(RunControlError, match=code):
        asyncio.run(
            execute_run_action(
                graphql,
                run_id=PARENT,
                action=RunAction.REEXECUTE,
                location_name="geo",
                repository_name="main",
                app_state_tags="geo.load_job",
            )
        )


@pytest.mark.parametrize(
    "action,location,tags,code",
    [
        ("force-cancel", "geo", (), "action_unavailable"),
        (RunAction.REEXECUTE, "", (), "dagster_error"),
        (RunAction.REEXECUTE, "geo", {".dagster/state"}, "dagster_error"),
    ],
)
def test_invalid_control_parameters_fail_closed(action, location, tags, code):
    async def graphql(_query, _variables):
        pytest.fail("invalid action unexpectedly queried Dagster")

    with pytest.raises(RunControlError, match=code):
        asyncio.run(
            execute_run_action(
                graphql,
                run_id=PARENT,
                action=action,
                location_name=location,
                repository_name="main",
                app_state_tags=tags,
            )
        )


def test_cancelled_run_needs_worker_stop_confirmation():
    assert run_actions("CANCELED", can_terminate=False, has_app_state=False) == ()
