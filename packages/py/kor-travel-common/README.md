# 실행 복구 프리미티브

`kor-travel-common`의 최소 Python 개발 후보다. 공개 import는 `kortravelcommon`이며
Dagster가 필요할 때만 `[dagster]` extra를 설치한다. 인증·DB·provider client를 소유하지 않는다.
이번 후보는 [T-319](../../../docs/tasks/T-319-dagster-recovery.md) 범위이며 다른 Python task의
구현·릴리스 완료를 뜻하지 않는다.
소비자 적용 순서는 [Dagster 적용 가이드](../../../docs/runbooks/dagster-adoption.md)를 따른다.

```python
from kortravelcommon.dagster import RecoveryPolicy, coalescing_schedule

tags = RecoveryPolicy(7200, idempotent=True, infrastructure_retries=1).tags(
    project="weather", job_name="collect"
)
# job(tags=tags) 또는 define_asset_job(..., tags=tags)
# coalescing_schedule(project="weather", location_name="앱의 실제 location", job=job, ...)
```

`coalescing_schedule`은 동일 location/job에 QUEUED·STARTING·STARTED·CANCELING 실행이 남아
있으면 새 tick을 합친다. 이전 배포의 무태그 run도 origin으로 판정한다. 다른 location의 동명
job은 영향을 받지 않는다. metadata 조회 실패는 tick 실패로 전달한다.

멱등성 기본값은 false, 재시도 기본값은 0이다. Pinvi email/Telegram 전송·geo restore처럼
전체 재실행이 안전하지 않은 작업에 자동 재시도를 켜지 않는다. op/provider 오류는 provider
자체 재시도와 다음 schedule이 처리하며, worker/launcher 장애만 Dagster native run retry에
맡긴다. 수동 취소는 자동 재시도하지 않는다.

`reconciliation_sensor`에는 앱의 CAS/lease 회수 함수를 주입한다. 원천 소유권·orchestrator
run ID·회수 SQL·부분 게시된 데이터의 멱등성은 앱이 유지한다. 오래된 heartbeat만으로 생존이
확인된 worker를 죽이지 않는다. 조회 장애와 없는 run ID를 terminal로 간주하지 않는다.

`call_with_deadline`은 동기 호출의 **대기만** 제한한다. `DeadlineExceeded` 후 같은 client를
재사용하거나 close하지 않고 해당 step을 끝낸다. daemon thread를 강제 종료하거나
transaction을 취소하는 기능은 없다. OS process 회수는 launcher·run monitoring의 책임이다.

## instance 설정

태그만으로 native run monitoring/retry가 켜지지 않는다. 실제 daemon의 `dagster.yaml`에
다음 설정을 병합하고 재시작한다. `run_coordinator`와 `concurrency.runs`를 동시에 선언하지
않으며, 이미 pools를 쓰는 instance는 `concurrency.runs`에 limits를 넣는다.

```yaml
run_monitoring:
  enabled: true
  start_timeout_seconds: 300
  cancel_timeout_seconds: 300
  max_resume_run_attempts: 0
  poll_interval_seconds: 60
run_retries:
  enabled: true
  max_retries: 0
  retry_on_asset_or_op_failure: false
# 기존 queued coordinator의 config.tag_concurrency_limits에 병합:
# - key: kortravelcommon/job
#   value: {applyLimitPerUniqueValue: true}
#   limit: 1
# - key: kortravelcommon/project
#   value: weather
#   limit: 6
```

프로젝트별 상한은 호스트 메모리 실측으로 정한다. weather의 6은 동시 실행 기본 10개 중
다른 앱에 슬롯을 남기는 상한이며, external provider 그룹은 기존 3개 상한을 함께 유지한다.
다른 앱에 6을 일괄 복사하지 않는다. 장애를 반복하는 실행은 재시도 상한에서 멈추고 이후
정상 tick이 새 실행을 만든다. code server/daemon 자체가 내려간 상태는 서비스 관리자가
복구해야 한다. shared plane에 설정을 반영하지 않은 상태는 운영 검증 완료가 아니다.

## 검증

```bash
uv sync --extra dev --extra dagster
uv run pytest -q
uv run ruff check .
uv build
```
