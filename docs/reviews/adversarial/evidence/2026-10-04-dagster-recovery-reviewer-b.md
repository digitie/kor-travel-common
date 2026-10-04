# Reviewer B 원본 적대 리뷰

실행 ID: `B-20261004-DAGSTER-RECOVERY-01`

- 기록된 검토 시각: `2026-10-04T09:59:25+09:00`~`10:02+09:00`. 최초 시작 시각은 기록하지 않았다.
- common: base `be7f21f2a645f4ce882b3d841487e1b40ad23425`, candidate `270619bd98c21ead62d077bf46f09c92dd946a59`.
- weather: base `5da6e158dccc8ea98e8301078ce9610525da0ebf`, candidate `709dc44cf2661ab546a6b126ce06fcea00d666c0`.
- 격리: Windows Git의 고정 commit `show`·`diff`·`rev-parse`와 commit 내 tarball 바이트만 읽었다. source 수정·checkout·빌드·운영 서비스 조작을 하지 않았다.
- 다른 reviewer 결과를 전달받거나 열람하지 않았다.
- manifest는 제공된 동일 파일을 읽었다.

**Verdict: CONDITIONAL**

P0/P1은 발견하지 않았다. 아래 P2 네 건의 수정 또는 규정에 맞는 명시적 disposition이 필요하다. 사용자 필수 조건인 live UI e2e 및 CI는 이 리뷰에서 실행하지 않았으므로, 이 verdict 자체는 merge 승인이 아니다.

## B-P2-01 — 특보 fan-out은 여전히 전체 실행의 fact를 메모리에 누적한다

**위치**

weather `packages/kor-travel-weather-dagster/src/kortravelweather_dagster/kma_weather.py:1170`~`:1217`, `_publish_alerts`.

**근거와 실패 시나리오**

격자 수집은 `KMA_STAGE_VALUES=5000`에서 게시·해제하지만 특보는 모든 station/notice/location에 대해 `alert_values.append(...)`한 뒤에야 `_publish_alerts`를 호출한다. `_publish_alerts`도 원본 `alert_values`를 보유한 채 재시도 subset을 추가로 만든다.

정상적으로 허용되는 10,000 target에 여러 공통 특보가 매칭되면 fact 수는 target × notice 수로 증가한다. `max_values_per_run` 기본값은 8,000,000이며 이 경로에는 5,000개 staging 한도가 적용되지 않는다. 따라서 격자 합성 실측의 97% 감소를 특보에도 적용할 수 없다. 현재 runbook의 “KMA peak는 batch + 한 location의 response” 설명도 특보에서는 성립하지 않는다.

**영향**

전국 fan-out 특보 job은 큰 Python 객체 집합을 계속 보유한다. shared host의 메모리 압박·swap 및 다른 job의 지연이라는 원래 문제의 경로가 남는다. 새로운 회귀는 아니지만 이번 사용자의 구조적 메모리 개선 범위에서 중요한 미완성 부분이다.

**권고**

특보도 bounded staging으로 게시하고 해제하되 다음 기존 계약을 보존한다.

- 전체 normalized 예산은 누적 생성량으로 계산한다.
- raw/source lineage는 각 게시 batch에 포함한다.
- skip 대상은 bounded batch 내에서 제한된 재시도를 수행하고, run 전체 skipped/starved 판정에 필요한 것은 location ID 집합 등 작은 상태만 보관한다.
- 같은 location의 일부 batch는 성공하고 다른 batch는 skip되는 경우의 최종 skip 판정을 명확히 한다.
- 전국 target × 복수 notice 테스트로 게시 전에 전체 fan-out을 누적하지 않는 것을 확인한다.

## B-P2-02 — 회수 후보의 고정 첫 페이지 때문에 뒷부분의 terminal 실행이 계속 누락될 수 있다

**위치**

weather `src/kortravelweather/repository.py:2718`~`:2730`, `reconcile_interrupted_sync_runs`.

**근거와 재현**

쿼리는 매번 `ORDER BY started_at LIMIT limit`으로 같은 첫 페이지를 읽으며 cursor나 다음 페이지 처리가 없다.

작은 재현은 `limit=1`로 충분하다.

1. 먼저 생성된 `running` 행 A의 orchestrator는 생존 중이다.
2. 뒤에 생성된 행 B의 orchestrator는 terminal이다.
3. `reconcile_interrupted_sync_runs(..., limit=1)`을 반복 호출한다.
4. A가 생존하는 동안 B는 한번도 조회되지 않고 `running`을 유지한다.

기본값에서는 같은 현상이 100행 뒤에서 발생한다. 현재 job 수와 project 동시성 제한 때문에 운영 발생 가능성은 낮지만, API 호출·기존 행·확장된 provider 조합과 배포 전환을 포함한 회수 알고리즘 자체는 완료를 보장하지 않는다. `start_sync_run`의 provider/dataset unique 제약 때문에 누락된 B는 후속 실행을 계속 막는다.

**영향**

회수 sensor가 매분 성공 실행돼도 특정 수집 행은 회수되지 않을 수 있다. 사용자가 요구한 영구 정지 방지의 경계다.

**권고**

stable keyset cursor를 사용해 bounded batch를 순회하거나, sensor cursor로 다음 페이지를 이어서 검사한다. `started_at` 동률을 고려해 `run_id` tie-breaker를 포함한다. 최소 두 페이지와 생존 첫 페이지/terminal 다음 페이지 테스트가 필요하다.

## B-P2-03 — RecoveryPolicy의 안전 조건이 잘못된 동적 입력을 허용한다

**위치**

common `packages/py/kor-travel-common/src/kortravelcommon/dagster.py:36`~`:47`.

**실행한 재현**

고정 commit에서 `RecoveryPolicy` AST만 메모리로 추출해 실행했다. worktree source를 import하거나 변경하지 않았다.

다음 입력이 모두 허용되었다.

```python
RecoveryPolicy(float("nan"))
# dagster/max_runtime = "nan"

RecoveryPolicy(300, idempotent="false", infrastructure_retries=1)
# dagster/max_retries = "1"

RecoveryPolicy(300, idempotent=True, infrastructure_retries=1.5)
# dagster/max_retries = "1.5"
```

Python annotation은 runtime 검증이 아니다. `"false"`는 truthy이므로 비멱등 선언을 잘못 읽어 자동 재시도를 허용한다. Dagster 1.13.20의 timeout 구현은 tag를 `float`로 읽고 elapsed와 비교하므로 `nan`/`inf` runtime은 상한 회수를 무력화한다. 재시도 tag는 정수 소비 계약과도 어긋난다. [Dagster 고정 버전 timeout 구현](https://raw.githubusercontent.com/dagster-io/dagster/1.13.20/python_modules/dagster/dagster/_daemon/monitoring/run_monitoring.py)

**영향**

weather의 현재 호출은 상수 정수/boolean이라 이 문제에 직접 노출되지 않는다. 그러나 다른 소비자가 환경 설정·JSON 등을 주입하는 공용 안전 프리미티브에서는 보호 장치가 조용히 해제될 수 있다.

**권고**

`max_runtime_seconds`와 `infrastructure_retries`가 boolean을 제외한 정수인지, `idempotent`가 실제 boolean인지 검증한다. runtime 양수·retry 0 이상 검사를 유지하고 nan/inf/fraction/string/bool 경계 테스트를 추가한다.

## B-P2-04 — 기존 architecture 정본의 게시 계약이 새 코드와 반대다

**위치**

weather `docs/architecture/dagster-boundary.md:46`, `:67`~`:77`.

**근거**

기존 architecture는 여전히 다음을 선언한다.

- 모든 응답이 유효해야 게시를 시작한다.
- N번째 grid의 provider/parse 오류에서는 아무 fact도 게시하지 않는다.
- publish 도중 DB/lease 오류에 대해서만 all-or-nothing을 포기한다.

이번 코드는 수집 중 5,000개 batch를 commit하므로 뒤쪽 provider/parse 오류에도 이전 fact가 남는다. 새로운 recovery runbook은 이를 올바르게 설명하지만 기존 architecture와 충돌한다.

**영향**

운영자 및 transport/map/geo 확산 작업자가 실패 run의 데이터 잔존·replay·count 계약을 잘못 이해할 수 있다. provider 실패 시 zero-publication을 전제한 후속 테스트나 운영 복구를 만들 위험이 있다.

**권고**

architecture의 게시 및 메모리 단락을 새 bounded/partial 계약으로 갱신한다. 과거 운영 실측은 당시 전체 staging 방식의 역사로 명시하고, 현행 메모리 보증과 섞지 않는다. 기존 코드의 “chunks built up front” 주석도 현재 lazy iterator 계약으로 정정한다.

## 공격한 시나리오와 확인된 좋은 경계

- terminal worker와 fresh heartbeat: terminal 판정을 권위로 사용하고, `status=running` CAS로 회수한다.
- metadata 유실과 heartbeat 갱신 경쟁: UPDATE에서 만료 조건을 다시 검사하여 갱신된 lease를 보호한다.
- metadata DB 장애: terminal로 오인하지 않고 예외를 전달한다.
- 늦은 worker의 게시: ingest가 run row를 잠그고 status를 확인하므로 회수 뒤 게시가 거절된다.
- 부분 commit 뒤 재실행: fact identity/source association과 count 갱신을 transaction 안에서 처리하며, 버퍼 flush 뒤 전체 생성 예산을 유지한다.
- deadline 이후 client 공유: `DeadlineExceeded`에서 dataset loop를 중단하고 provider.close를 생략하여 살아 있는 thread와의 경합을 피한다. thread 강제 종료를 보장하지 않는다는 문서도 정확하다.
- foreign 동명 job: origin location을 검사하고, originless 경우 project tag를 검사한다.
- shared plane: weather YAML이 실제 shared daemon 설정을 바꾸지 않는다고 문서가 명확히 밝힌다.
- 멱등 native retry: 비멱등 기본 0회, op/provider failure 재시도 금지, 수동 취소 제외 계약은 타당하다.
- multiprocess executor의 실제 job resolve에 `max_concurrent=1`을 적용한 것은 Definitions 수준 설정만 추가하는 것보다 정확하다.

## 검증과 한계

**직접 실행/확인**

- 두 base/candidate의 실제 full hash를 확인했다.
- 고정 Git object의 backend/UI/packaging/CI/provenance 변경과 관련 기존 게시·복구 계약을 읽었다.
- vendor tgz를 commit 객체에서 메모리로 열어 package metadata·배포 파일·LICENSE/NOTICE/THIRD_PARTY_NOTICES를 확인했다.
- tarball SHA-256은 고정 README와 일치했다.
  - tokens: `22b7613085e55885987ce05720a178b65ac649b097763db650b8c7b8b4acaa84`
  - ui: `ef4da827e008e086997022a00cf0f9ee19990b9437ad256502d632e401cafffc`
- immutable `RecoveryPolicy` AST의 동적 입력 경계를 실행했다.
- Dagster 공식 1.13.20 monitoring/auto-reexecution/multiprocess 구현 및 1.9.0 origin/status 계약을 대조했다.

**읽은 evidence**

manifest의 weather Python338, common Python13/UI32, frontend63/build, tools/문서 검사 및 합성 memory 실측 기록을 읽었다. 리뷰어가 해당 전체 suite를 독립 재실행한 것은 아니다.

**NOT_RUN**

- 실제 daemon에서 launcher crash·hard hang·강제 취소·native retry child launch 장애 주입.
- shared plane 설정 적용 및 host RSS/OS process 회수 확인.
- live UI e2e, 브라우저 접근성·반응형 확인.
- PR 최종 CI 및 merge gate.
- Dagster 1.9 floor 설치 실행. common lock은 1.13.25, weather lock은 1.13.20이므로 두 설치 및 CI 결과를 명시적으로 확인하는 것이 좋다.

완료 주장에서는 bounded Python staging과 운영 전체 RSS를 구분해야 하며, daemon/code server 자체 중단은 서비스 관리자 복구가 필요하다는 현재 문서의 제한을 유지해야 한다.
