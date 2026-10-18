# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"""주소 갱신 sensor는 due일 때 자기 location의 제한된 job만 예약한다."""

from dagster import DagsterInstance, build_sensor_context

from kortravelcommon.address_dagster import address_refresh_definitions


def test_job_force_and_automatic_request_are_distinct():
    calls = []
    job, sensor = address_refresh_definitions(
        project="fixture",
        location_name="fixture-location",
        run=lambda force: calls.append(force) or {"status": "success"},
        pending=lambda: True,
    )
    result = job.execute_in_process(
        run_config={"ops": {"refresh_addresses": {"config": {"force": True}}}}
    )
    assert result.success and calls == [True]
    with DagsterInstance.ephemeral() as instance:
        tick = sensor.evaluate_tick(build_sensor_context(instance=instance))
        assert len(tick.run_requests) == 1
        request = tick.run_requests[0]
        assert request.run_config["ops"]["refresh_addresses"]["config"]["force"] is False
        assert request.tags["dagster/code_location"] == "fixture-location"
        instance.create_run_for_job(job, tags={"dagster/code_location": "fixture-location"})
        assert not sensor.evaluate_tick(build_sensor_context(instance=instance)).run_requests


def test_no_due_target_has_no_run_or_provider_call():
    job, sensor = address_refresh_definitions(
        project="fixture",
        location_name="fixture-location",
        run=lambda force: (_ for _ in ()).throw(AssertionError("provider call")),
        pending=lambda: False,
    )
    with DagsterInstance.ephemeral() as instance:
        tick = sensor.evaluate_tick(build_sensor_context(instance=instance))
        assert not tick.run_requests
        assert tick.skip_message
