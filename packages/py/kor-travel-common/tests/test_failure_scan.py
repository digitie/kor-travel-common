# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"""재시도 sensor의 실패 event high-water 순회와 사유 없는 실패 분류."""

from dagster import (
    DagsterEvent,
    DagsterEventType,
    DagsterInstance,
    DagsterRunStatus,
    RunsFilter,
    build_sensor_context,
)
from dagster._core.events import JobFailureData, RunFailureReason, StepFailureData
from test_recovery import failure_context, retry_definition, sample

import kortravelcommon.dagster as recovery
from kortravelcommon.dagster import (
    FAILURE_CLASS_CANCELED,
    FAILURE_CLASS_LAUNCH,
    FAILURE_CLASS_STEP_FAILURE,
    FAILURE_CLASS_TAG,
    FAILURE_CLASS_WORKER_ALIVE,
    FAILURE_CLASS_WORKER_LOST,
    INFRA_RETRY_PARENT_TAG,
    PROJECT_TAG,
)


def unreported_failure(instance, *, started=False, canceling=False, step_failure=False):
    """Dagster가 `report_run_failed(run)`로 남기는 사유 없는 실패를 만든다."""
    run = instance.create_run_for_job(
        sample,
        status=DagsterRunStatus.STARTING,
        run_config={"ops": {"noop": {}}},
        tags={**sample.tags, "dagster/code_location": "test"},
    )
    if started:
        instance.report_dagster_event(
            DagsterEvent(event_type_value=DagsterEventType.RUN_START.value, job_name=sample.name),
            run.run_id,
        )
    if canceling:
        instance.report_run_canceling(run, message="최대 실행시간 초과")
    if step_failure:
        instance.report_dagster_event(
            DagsterEvent(
                event_type_value=DagsterEventType.STEP_FAILURE.value,
                job_name=sample.name,
                step_key="noop",
                event_specific_data=StepFailureData(error=None, user_failure_data=None),
            ),
            run.run_id,
        )
    instance.report_run_failed(instance.get_run_by_id(run.run_id))
    return run


def tick(instance, cursor=None):
    return retry_definition().evaluate_tick(build_sensor_context(instance=instance, cursor=cursor))


def test_cursor_moves_past_judged_failures_and_never_rescans_them(monkeypatch):
    with DagsterInstance.local_temp() as instance:
        for _ in range(3):
            failure_context(instance, RunFailureReason.STEP_FAILURE)
        first = tick(instance)
        assert not first.run_requests
        assert first.cursor.startswith("failures:")
        reads = []
        original = instance.get_runs

        def observed(**kwargs):
            if kwargs["filters"].run_ids:
                reads.append(kwargs["filters"].run_ids)
            return original(**kwargs)

        monkeypatch.setattr(instance, "get_runs", observed)
        idle = tick(instance, first.cursor)
        assert idle.cursor == first.cursor
        assert reads == []
        newer = failure_context(instance)
        resumed = tick(instance, idle.cursor)
        assert resumed.run_requests[0].tags[INFRA_RETRY_PARENT_TAG] == newer.dagster_run.run_id
        assert reads == [[newer.dagster_run.run_id]]
        assert int(resumed.cursor.split(":")[1]) > int(first.cursor.split(":")[1])


def test_budget_stops_at_the_last_judged_event_and_resumes_later(monkeypatch):
    with DagsterInstance.local_temp() as instance:
        failures = [failure_context(instance, RunFailureReason.STEP_FAILURE) for _ in range(3)]
        target = failure_context(instance)
        clock = [0.0]
        monkeypatch.setattr(recovery, "monotonic", lambda: clock[0])
        original_runs = instance.get_runs

        def slow_scan(**kwargs):
            # 실패 event의 run 일괄 조회만 느리게 만든다(5초 협력 예산을 넘긴다).
            result = original_runs(**kwargs)
            if kwargs["filters"].run_ids:
                clock[0] += 6.0
            return result

        monkeypatch.setattr(instance, "get_runs", slow_scan)
        first = tick(instance)
        assert not first.run_requests
        storage_ids = [
            record.storage_id
            for record in instance.fetch_run_status_changes(
                DagsterEventType.RUN_FAILURE, limit=10, ascending=True
            ).records
        ]
        # 첫 event만 판정하고 멈춘다. 같은 event부터 다시 읽지 않는다.
        assert first.cursor == f"failures:{storage_ids[0]}"
        cursor = first.cursor
        for _ in range(len(failures)):
            clock[0] = 0.0
            outcome = tick(instance, cursor)
            cursor = outcome.cursor
            if outcome.run_requests:
                break
        assert outcome.run_requests[0].tags[INFRA_RETRY_PARENT_TAG] == target.dagster_run.run_id
        assert cursor == f"failures:{storage_ids[-1]}"


def test_other_project_failures_are_filtered_in_one_query(monkeypatch):
    with DagsterInstance.local_temp() as instance:
        foreign = failure_context(instance, **{PROJECT_TAG: "foreign"})
        owned = failure_context(instance)
        result = tick(instance)
        assert result.run_requests[0].tags[INFRA_RETRY_PARENT_TAG] == owned.dagster_run.run_id
        assert FAILURE_CLASS_TAG not in instance.get_run_by_id(foreign.dagster_run.run_id).tags


def test_failures_older_than_the_window_are_not_retried(monkeypatch):
    with DagsterInstance.local_temp() as instance:
        failure_context(instance)
        monkeypatch.setattr(recovery, "FAILURE_LOOKBACK_SECONDS", 0.0)
        result = tick(instance)
        assert not result.run_requests
        # 창 안에 실패가 없으면 그때의 최신 event를 기준으로 삼아 다음부터 읽는다.
        latest = instance.fetch_run_status_changes(
            DagsterEventType.RUN_FAILURE, limit=1, ascending=False
        ).records[0]
        assert result.cursor == f"failures:{latest.storage_id}"


def test_empty_instance_starts_from_zero():
    with DagsterInstance.local_temp() as instance:
        assert tick(instance).cursor == "failures:0"


def test_legacy_head_and_run_id_cursors_start_from_the_recent_window():
    with DagsterInstance.local_temp() as instance:
        context = failure_context(instance)
        for legacy in ("head", context.dagster_run.run_id, "failures:not-a-number"):
            result = tick(instance, legacy)
            assert result.run_requests[0].tags[INFRA_RETRY_PARENT_TAG] == (
                context.dagster_run.run_id
            )


def classify(instance, run):
    return recovery.classify_unreported_failure(instance, run.run_id)


def test_unreported_failures_are_classified_by_event_structure():
    with DagsterInstance.local_temp() as instance:
        assert classify(instance, unreported_failure(instance)) == FAILURE_CLASS_LAUNCH
        assert (
            classify(instance, unreported_failure(instance, started=True))
            == FAILURE_CLASS_WORKER_LOST
        )
        assert (
            classify(instance, unreported_failure(instance, started=True, canceling=True))
            == FAILURE_CLASS_CANCELED
        )
        assert (
            classify(instance, unreported_failure(instance, started=True, step_failure=True))
            == FAILURE_CLASS_STEP_FAILURE
        )


def test_unreported_launch_failure_is_retried_and_tagged():
    with DagsterInstance.local_temp() as instance:
        run = unreported_failure(instance)
        result = tick(instance)
        assert result.run_requests[0].tags[INFRA_RETRY_PARENT_TAG] == run.run_id
        stored = instance.get_run_by_id(run.run_id)
        assert stored.tags[FAILURE_CLASS_TAG] == FAILURE_CLASS_LAUNCH
        assert FAILURE_CLASS_TAG not in result.run_requests[0].tags


def test_unreported_worker_loss_is_retried():
    with DagsterInstance.local_temp() as instance:
        run = unreported_failure(instance, started=True)
        result = tick(instance)
        assert result.run_requests[0].tags[INFRA_RETRY_PARENT_TAG] == run.run_id


def test_unreported_timeout_and_step_failure_are_reported_not_retried():
    with DagsterInstance.local_temp() as instance:
        canceled = unreported_failure(instance, started=True, canceling=True)
        stepped = unreported_failure(instance, started=True, step_failure=True)
        cursor = None
        for _ in range(2):
            result = tick(instance, cursor)
            assert not result.run_requests
            cursor = result.cursor
        assert instance.get_run_by_id(canceled.run_id).tags[FAILURE_CLASS_TAG] == (
            FAILURE_CLASS_CANCELED
        )
        assert instance.get_run_by_id(stepped.run_id).tags[FAILURE_CLASS_TAG] == (
            FAILURE_CLASS_STEP_FAILURE
        )


def test_reported_reasons_are_not_reclassified():
    with DagsterInstance.local_temp() as instance:
        context = failure_context(instance, RunFailureReason.STEP_FAILURE)
        assert not tick(instance).run_requests
        assert FAILURE_CLASS_TAG not in instance.get_run_by_id(context.dagster_run.run_id).tags
        # JobFailureData가 있으나 사유가 비어 있는 실패도 기존처럼 거부한다.
        other = instance.create_run_for_job(
            sample,
            status=DagsterRunStatus.FAILURE,
            tags={**sample.tags, "dagster/code_location": "test"},
        )
        instance.report_dagster_event(
            DagsterEvent(
                event_type_value=DagsterEventType.RUN_FAILURE.value,
                job_name=sample.name,
                event_specific_data=JobFailureData(None, failure_reason=None),
            ),
            other.run_id,
        )
        assert not tick(instance).run_requests
        assert not instance.get_runs(filters=RunsFilter(tags={FAILURE_CLASS_TAG: "launch_failure"}))


def test_parent_failure_judgement_tags_are_not_inherited_by_the_child():
    with DagsterInstance.local_temp() as instance:
        failure_context(
            instance,
            **{
                FAILURE_CLASS_TAG: FAILURE_CLASS_LAUNCH,
                recovery.BREAKER_TAG: "open",
                recovery.BREAKER_FINGERPRINT_TAG: "x",
                recovery.BREAKER_STREAK_TAG: "3",
            },
        )
        request = tick(instance).run_requests[0]
        assert not {
            FAILURE_CLASS_TAG,
            recovery.BREAKER_TAG,
            recovery.BREAKER_FINGERPRINT_TAG,
            recovery.BREAKER_STREAK_TAG,
        } & request.tags.keys()


def test_young_failures_wait_for_the_settle_window(monkeypatch):
    with DagsterInstance.local_temp() as instance:
        context = failure_context(instance)
        monkeypatch.setattr(recovery, "FAILURE_SETTLE_SECONDS", 3600)
        waiting = tick(instance)
        # 자리 잡지 않은 event는 읽지도 건너뛰지도 않는다.
        assert not waiting.run_requests and waiting.cursor == "failures:0"
        monkeypatch.setattr(recovery, "FAILURE_SETTLE_SECONDS", 0)
        settled = tick(instance, waiting.cursor)
        assert settled.run_requests[0].tags[INFRA_RETRY_PARENT_TAG] == context.dagster_run.run_id


def test_legacy_three_field_checkpoint_does_not_freeze_the_sensor():
    with DagsterInstance.local_temp() as instance:
        old = failure_context(instance, RunFailureReason.STEP_FAILURE)
        legacy = 'steps:["' + old.dagster_run.run_id + '","x",1]'
        moved = tick(instance, legacy)
        assert moved.cursor == "failures:0"
        newer = failure_context(instance)
        resumed = tick(instance, moved.cursor)
        assert resumed.run_requests[0].tags[INFRA_RETRY_PARENT_TAG] == newer.dagster_run.run_id


def test_worker_activity_after_the_failure_is_reported_not_retried():
    with DagsterInstance.local_temp() as instance:
        run = unreported_failure(instance, started=True)
        instance.report_dagster_event(
            DagsterEvent(
                event_type_value=DagsterEventType.STEP_START.value,
                job_name=sample.name,
                step_key="noop",
            ),
            run.run_id,
        )
        assert not tick(instance).run_requests
        assert instance.get_run_by_id(run.run_id).tags[FAILURE_CLASS_TAG] == (
            FAILURE_CLASS_WORKER_ALIVE
        )


def test_started_run_failed_by_the_launch_path_is_reported_not_retried():
    from dagster._core.events import EngineEventData
    from dagster._utils.error import SerializableErrorInfo

    with DagsterInstance.local_temp() as instance:
        run = instance.create_run_for_job(
            sample,
            status=DagsterRunStatus.STARTING,
            run_config={"ops": {"noop": {}}},
            tags={**sample.tags, "dagster/code_location": "test"},
        )
        instance.report_dagster_event(
            DagsterEvent(event_type_value=DagsterEventType.RUN_START.value, job_name=sample.name),
            run.run_id,
        )
        instance.report_engine_event(
            "launch RPC timeout",
            instance.get_run_by_id(run.run_id),
            EngineEventData.engine_error(SerializableErrorInfo("deadline", [], "TimeoutError")),
        )
        instance.report_run_failed(instance.get_run_by_id(run.run_id))
        assert not tick(instance).run_requests
        assert instance.get_run_by_id(run.run_id).tags[FAILURE_CLASS_TAG] == (
            FAILURE_CLASS_WORKER_ALIVE
        )


def test_only_settled_failures_are_judged_and_the_cursor_stops_before_young_ones(monkeypatch):
    with DagsterInstance.local_temp() as instance:
        older = failure_context(instance)
        younger = failure_context(instance)
        events = instance.fetch_run_status_changes(
            DagsterEventType.RUN_FAILURE, limit=2, ascending=True
        ).records
        settle = 120
        monkeypatch.setattr(recovery, "FAILURE_SETTLE_SECONDS", settle)
        # 첫 event만 settle을 지난 시각.
        between = (events[0].timestamp + events[1].timestamp) / 2
        monkeypatch.setattr(recovery, "wall_clock", lambda: between + settle)
        first = tick(instance)
        assert first.run_requests[0].tags[INFRA_RETRY_PARENT_TAG] == older.dagster_run.run_id
        assert first.cursor == f"failures:{events[0].storage_id}"
        # 그 뒤에는 젊던 event도 판정한다.
        monkeypatch.setattr(recovery, "wall_clock", lambda: events[1].timestamp + settle + 1)
        second = tick(instance, first.cursor)
        assert second.run_requests[0].tags[INFRA_RETRY_PARENT_TAG] == younger.dagster_run.run_id


def test_id_and_timestamp_disorder_does_not_skip_the_young_event(monkeypatch):
    with DagsterInstance.local_temp() as instance:
        failure_context(instance)
        failure_context(instance)
        events = instance.fetch_run_status_changes(
            DagsterEventType.RUN_FAILURE, limit=2, ascending=True
        ).records
        settle = 120
        monkeypatch.setattr(recovery, "FAILURE_SETTLE_SECONDS", settle)
        # 낮은 id event가 젊으면(생성 뒤 늦게 insert된 높은 id가 더 오래됨) 그 앞에서 멈춘다.
        monkeypatch.setattr(recovery, "wall_clock", lambda: events[0].timestamp + settle - 1)
        waiting = tick(instance)
        assert not waiting.run_requests
        assert waiting.cursor == "failures:0"


def test_compute_log_error_before_worker_loss_is_still_retried():
    from dagster._core.events import EngineEventData
    from dagster._utils.error import SerializableErrorInfo

    with DagsterInstance.local_temp() as instance:
        run = instance.create_run_for_job(
            sample,
            status=DagsterRunStatus.STARTING,
            run_config={"ops": {"noop": {}}},
            tags={**sample.tags, "dagster/code_location": "test"},
        )
        instance.report_dagster_event(
            DagsterEvent(event_type_value=DagsterEventType.RUN_START.value, job_name=sample.name),
            run.run_id,
        )
        instance.report_engine_event(
            "compute log upload 실패",
            instance.get_run_by_id(run.run_id),
            EngineEventData.engine_error(SerializableErrorInfo("s3", [], "S3UploadError")),
            step_key="noop",
        )
        instance.report_engine_event("worker 상태 확인", instance.get_run_by_id(run.run_id))
        instance.report_run_failed(instance.get_run_by_id(run.run_id))
        assert tick(instance).run_requests
        assert instance.get_run_by_id(run.run_id).tags[FAILURE_CLASS_TAG] == (
            FAILURE_CLASS_WORKER_LOST
        )
