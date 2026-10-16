# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"""여러 job이 한 scan·cursor·예산을 공유해도 엄격한 재시도 판정을 보존한다."""

from types import SimpleNamespace

import pytest
from dagster import (
    DagsterEvent,
    DagsterEventType,
    DagsterInstance,
    DagsterRunStatus,
    build_sensor_context,
    job,
    op,
)
from dagster._core.events import JobFailureData, RunFailureReason

import kortravelcommon.dagster as recovery
from kortravelcommon.dagster import (
    INFRA_RETRY_PARENT_TAG,
    INFRA_RETRY_PENDING_TAG,
    PROJECT_TAG,
    RecoveryPolicy,
)


@op
def noop():
    pass


def jobs(count=2):
    result = {}
    for index in range(count):
        name = f"sample_{index}"
        policy = RecoveryPolicy(300 + index, idempotent=True, infrastructure_retries=1)

        @job(name=name, tags=policy.tags(project="test", job_name=name))
        def definition():
            noop()

        result[name] = (definition, policy)
    return result


def definition(mapping):
    return recovery.infrastructure_retry_sensor_for_jobs(
        name="shared_infra",
        project="test",
        location_name="test",
        jobs=mapping,
    )


def failure(instance, target, reason=RunFailureReason.RUN_WORKER_RESTART, **kwargs):
    run = instance.create_run_for_job(
        target,
        status=DagsterRunStatus.FAILURE,
        run_config={"ops": {"noop": {}}},
        tags={**target.tags, "dagster/code_location": "test", **kwargs.pop("tags", {})},
        **kwargs,
    )
    instance.report_dagster_event(
        DagsterEvent(
            event_type_value=DagsterEventType.RUN_FAILURE.value,
            job_name=target.name,
            event_specific_data=JobFailureData(None, failure_reason=reason),
        ),
        run.run_id,
    )
    return run


def test_seventeen_jobs_share_one_failure_page(monkeypatch):
    mapping = jobs(17)
    shared = definition(mapping)
    with DagsterInstance.local_temp() as instance:
        for target, _ in mapping.values():
            failure(instance, target, RunFailureReason.UNKNOWN)
        original = instance.get_runs
        pages = []

        def observed(**kwargs):
            if kwargs["filters"].statuses == [DagsterRunStatus.FAILURE]:
                pages.append(kwargs)
            return original(**kwargs)

        monkeypatch.setattr(instance, "get_runs", observed)
        result = shared.evaluate_tick(build_sensor_context(instance=instance))
        assert not result.run_requests
        assert len(pages) == 1
        assert pages[0]["limit"] == 100
        assert pages[0]["filters"].job_name is None
        assert pages[0]["filters"].tags == {PROJECT_TAG: "test"}


def test_selected_job_config_policy_and_single_handoff_are_preserved():
    mapping = jobs()
    shared = definition(mapping)
    with DagsterInstance.local_temp() as instance:
        earlier = failure(instance, mapping["sample_0"][0])
        later = failure(instance, mapping["sample_1"][0])
        result = shared.evaluate_tick(build_sensor_context(instance=instance))
        assert len(result.run_requests) == 1
        request = result.run_requests[0]
        assert request.job_name == "sample_1"
        assert request.run_config == later.run_config
        assert request.tags["dagster/max_runtime"] == "301"
        assert request.tags["dagster/max_retries"] == "0"
        assert request.tags[INFRA_RETRY_PARENT_TAG] == later.run_id
        assert request.run_key == f"test/infra/{later.run_id}/1"
        assert instance.get_run_by_id(later.run_id).tags[INFRA_RETRY_PENDING_TAG] == "true"
        assert INFRA_RETRY_PENDING_TAG not in instance.get_run_by_id(earlier.run_id).tags


@pytest.mark.parametrize(
    "reason",
    [
        RunFailureReason.STEP_FAILURE,
        RunFailureReason.RUN_EXCEPTION,
        RunFailureReason.UNKNOWN,
        RunFailureReason.JOB_INITIALIZATION_FAILURE,
    ],
)
def test_disallowed_final_reason_is_not_broadened(reason):
    mapping = jobs()
    with DagsterInstance.local_temp() as instance:
        failure(instance, mapping["sample_1"][0], reason)
        assert not definition(mapping).evaluate_tick(
            build_sensor_context(instance=instance)
        ).run_requests


@pytest.mark.parametrize("kind", ["partial", "prior_step", "child", "active", "foreign_location"])
def test_existing_strict_gates_are_applied_to_each_target(monkeypatch, kind):
    mapping = jobs()
    target = mapping["sample_1"][0]
    with DagsterInstance.local_temp() as instance:
        kwargs = {"op_selection": ["noop"]} if kind == "partial" else {}
        if kind == "foreign_location":
            kwargs["tags"] = {"dagster/code_location": "other"}
        parent = failure(instance, target, **kwargs)
        if kind == "child":
            instance.create_run_for_job(
                target,
                tags={**target.tags, INFRA_RETRY_PARENT_TAG: parent.run_id},
                status=DagsterRunStatus.SUCCESS,
            )
        if kind == "active":
            instance.create_run_for_job(
                target,
                tags={**target.tags, "dagster/code_location": "test"},
                status=DagsterRunStatus.STARTED,
            )
        if kind == "prior_step":
            original = instance.get_records_for_run

            def records(**kwargs):
                if kwargs["of_type"] == DagsterEventType.STEP_FAILURE:
                    return SimpleNamespace(records=[object()], has_more=False)
                return original(**kwargs)

            monkeypatch.setattr(instance, "get_records_for_run", records)
        result = definition(mapping).evaluate_tick(build_sensor_context(instance=instance))
        assert not result.run_requests
        assert INFRA_RETRY_PENDING_TAG not in instance.get_run_by_id(parent.run_id).tags


def test_unknown_job_is_not_read_or_retried(monkeypatch):
    allowed, other = jobs(1), jobs(3)["sample_2"][0]
    with DagsterInstance.local_temp() as instance:
        parent = failure(instance, other)
        monkeypatch.setattr(
            instance, "get_records_for_run",
            lambda **kwargs: pytest.fail("허용 목록 밖의 event 이력을 읽지 않는다"),
        )
        assert not definition(allowed).evaluate_tick(
            build_sensor_context(instance=instance)
        ).run_requests
        assert INFRA_RETRY_PENDING_TAG not in instance.get_run_by_id(parent.run_id).tags


def test_shared_budget_preserves_progress_without_scanning_each_job(monkeypatch):
    mapping = jobs()
    shared = definition(mapping)
    with DagsterInstance.local_temp() as instance:
        failure(instance, mapping["sample_0"][0], RunFailureReason.UNKNOWN)
        latest = failure(instance, mapping["sample_1"][0], RunFailureReason.UNKNOWN)
        clock = [0.0]
        monkeypatch.setattr(recovery, "monotonic", lambda: clock[0])
        original = instance.get_records_for_run
        reads = []

        def slow(**kwargs):
            reads.append(kwargs["run_id"])
            result = original(**kwargs)
            clock[0] = 6.0
            return result

        monkeypatch.setattr(instance, "get_records_for_run", slow)
        result = shared.evaluate_tick(build_sensor_context(instance=instance))
        assert not result.run_requests
        assert reads == [latest.run_id]
        assert result.cursor == latest.run_id


def test_mapping_is_copied_and_invalid_entries_are_rejected():
    mapping = jobs()
    shared = definition(mapping)
    mapping.clear()
    assert len(shared.targets) == 2
    for invalid in [{}, {"wrong": jobs(1)["sample_0"]}]:
        with pytest.raises(ValueError):
            definition(invalid)
    with pytest.raises(ValueError, match="멱등"):
        definition({"sample_0": (jobs(1)["sample_0"][0], RecoveryPolicy(300))})


def test_native_enabled_delegates_except_durable_pending():
    mapping = jobs()
    shared = definition(mapping)
    with DagsterInstance.local_temp(overrides={"run_retries": {"enabled": True}}) as instance:
        target = mapping["sample_1"][0]
        parent = failure(instance, target)
        assert not shared.evaluate_tick(build_sensor_context(instance=instance)).run_requests
        instance.add_run_tags(
            parent.run_id,
            {INFRA_RETRY_PENDING_TAG: "true", "dagster/max_retries": "0",
             "dagster/will_retry": "false"},
        )
        result = shared.evaluate_tick(build_sensor_context(instance=instance))
        assert len(result.run_requests) == 1
        assert result.run_requests[0].job_name == target.name


def test_next_tick_routes_the_other_job_with_shared_cursor():
    mapping = jobs()
    shared = definition(mapping)
    with DagsterInstance.local_temp() as instance:
        earlier = failure(instance, mapping["sample_0"][0])
        failure(instance, mapping["sample_1"][0])
        first = shared.evaluate_tick(build_sensor_context(instance=instance))
        second = shared.evaluate_tick(
            build_sensor_context(instance=instance, cursor=first.cursor)
        )
        assert len(first.run_requests) == len(second.run_requests) == 1
        assert first.run_requests[0].job_name == "sample_1"
        assert second.run_requests[0].job_name == "sample_0"
        assert second.run_requests[0].tags[INFRA_RETRY_PARENT_TAG] == earlier.run_id


def test_other_job_active_does_not_block_selected_job():
    mapping = jobs()
    with DagsterInstance.local_temp() as instance:
        failure(instance, mapping["sample_1"][0])
        instance.create_run_for_job(
            mapping["sample_0"][0], status=DagsterRunStatus.STARTED,
            tags={**mapping["sample_0"][0].tags, "dagster/code_location": "test"},
        )
        result = definition(mapping).evaluate_tick(build_sensor_context(instance=instance))
        assert len(result.run_requests) == 1
        assert result.run_requests[0].job_name == "sample_1"


@pytest.mark.parametrize("child_tag", ["dagster/parent_run_id", INFRA_RETRY_PARENT_TAG])
def test_existing_child_of_selected_job_prevents_new_handoff(child_tag):
    mapping = jobs()
    with DagsterInstance.local_temp() as instance:
        target = mapping["sample_1"][0]
        parent = failure(instance, target)
        instance.create_run_for_job(
            target,
            tags={**target.tags, child_tag: parent.run_id},
            status=DagsterRunStatus.SUCCESS,
        )
        assert not definition(mapping).evaluate_tick(
            build_sensor_context(instance=instance)
        ).run_requests


def test_pending_handoff_reuses_deterministic_key_after_sensor_recreation():
    mapping = jobs()
    with DagsterInstance.local_temp() as instance:
        failure(instance, mapping["sample_1"][0])
        first = definition(mapping).evaluate_tick(build_sensor_context(instance=instance))
        # 요청 제출 전에 daemon이 재시작해도 별도 횟수/UUID를 만들지 않는다.
        repeated = definition(mapping).evaluate_tick(build_sensor_context(instance=instance))
        assert first.run_requests[0].job_name == repeated.run_requests[0].job_name
        assert first.run_requests[0].run_key == repeated.run_requests[0].run_key
        assert first.run_requests[0].tags == repeated.run_requests[0].tags


def test_mutable_input_pair_cannot_change_registered_policy():
    mapping = jobs(1)
    target, policy = mapping["sample_0"]
    pair = [target, policy]
    shared = definition({"sample_0": pair})
    pair[1] = RecoveryPolicy(300)
    with DagsterInstance.local_temp() as instance:
        failure(instance, target)
        request = shared.evaluate_tick(
            build_sensor_context(instance=instance)
        ).run_requests[0]
        assert request.tags["dagster/max_retries"] == "0"


def test_selected_job_storage_error_preserves_cursor_for_later_retry(monkeypatch):
    mapping = jobs()
    with DagsterInstance.local_temp() as instance:
        failure(instance, mapping["sample_1"][0])
        context = build_sensor_context(instance=instance)
        original = instance.get_records_for_run
        monkeypatch.setattr(
            instance, "get_records_for_run",
            lambda **kwargs: (_ for _ in ()).throw(ConnectionError("로컬 합성 오류")),
        )
        with pytest.raises(Exception) as caught:
            definition(mapping).evaluate_tick(context)
        assert isinstance(caught.value, ConnectionError)
        assert context.cursor is None
        monkeypatch.setattr(instance, "get_records_for_run", original)
        assert len(definition(mapping).evaluate_tick(context).run_requests) == 1
