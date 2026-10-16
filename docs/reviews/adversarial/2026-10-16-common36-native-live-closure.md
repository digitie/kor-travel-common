# Common36 native SDK 격리 복구 실제 종결

- 실행 ID: common36-native-r4-d-20261016 / UUID 659b40ec-091e-4674-a2da-65e26b94860f.
- 판정: **WSL native amd64·실제 SDK 격리 복구 시나리오 15 gate PASS**. 운영 Odroid ARM 배포·CPU/RSS 효과·Weather live UI·전역 T-319 DONE 판정은 아니다.
- 제품 Common36 5d2ad2bb45e64197ea359e0e5136b84780dab97a, Weather fixture f1d59f79, Dagster1.13.24.
- 실행 원문 once SHA256 8cc6866154d2c803585e044c83e249c28111b966e3753497b07983bc2b2e122c.
- checkpoint 9ae1243792516831eba6dfd0c324404023bb53825f0afcd7d4312cd787e302ba / 실행 freeze 02842b7bf72d762cebd371f52198ca213d528f8ff340dbea75f816e2fbde618e.
- 실행 CLI PID4143238·종료0 / 기록된 153 CLI 모두 terminal0 / fault 정확1. 새 lab 재시도는 없다.
- 원본 private receipt SHA256 6fe820585cef66c027bc44967eca1f3eb89df9cabfbbb94ff8fdc04d6d98d729 및 원 DB/컨테이너는 별도 보존한다. Env·Config·DSN 원문은 저장소에 반입하지 않았다.

## 독립 소스 검토와 실제 근거

동일 source5에 대해 [root 원문](evidence/2026-10-16-common36-native-r4-source-review-root.md)과
[A 원문](evidence/2026-10-16-common36-native-r4-source-review-a.md)은 SOURCE_PASS·열린 P0/P1/P2=0이다.
이는 아래 실제 실행 증거와 다른 gate다. [안전 투영 JSON](evidence/2026-10-16-common36-native-r4-safe.json)
SHA256 0721e542c2c48b2d5c6dc2334472a74c86f1c10ae7d773199a1cea7ff9806cab에 15 gate·실제 시간순서·종료 상태를 담았다.
실행자 D가 원 SQLite를 mode=ro/query_only로 다시 읽고 DB/WAL 해시 전후 동일을 확인했다.
그 재검증은 추가 SDK·run·sensor·서비스 mutation 0이다.

## 실제 순서

1. 모든 main/foreign/daemon보다 먼저 one-shot bootstrap에서 원 SDK가 빈 instance를 초기화·dispose했다. run/event/schedule revision=head, runs0/instigators0, 자연Exit0와 PID/cgroup 소멸 이후에만 lab3을 시작했다. 수동 DDL/stamp/기존 실패 DB 수리는 없다.
2. 실제 main·두 thread의 canonical PID1 clock이 host PID1 leader ticks와 일치했다. source57·Common9·실제 SDK를 확인하고 parent·foreign control STARTED와 물리 worker가 75초 grace 동안 유지됐다.
3. exact main 장애 주입1회 뒤 이전 init/worker/cgroup이 사라졌다. 동일 source 재시작의 새 incarnation 첫 tick은 SKIPPED·run0였고, 그 뒤 parent에 공식 RUN_WORKER_RESTART FAILURE1이 기록됐다.
4. native retry budget0을 유지하며 Common infra retry child1이 큐→STARTING→STARTED→SUCCESS로 완료됐다. 부모 귀속·attempt1을 확인했고 child shard SUCCESS1만 집계했다(index mirror는 중복 집계하지 않았다).
5. main/foreign control2의 실제 record start와 PIPELINE_START는 child PIPELINE_SUCCESS보다 앞선다. child 성공 후 각 sensor의 완료 tick2회 동안 실제 audit 모두 두 control STARTED/end=None·RPC/물리 identity 불변이었다. 그 뒤 release2→controls SUCCESS2로 끝났다.
6. 총 run4(parent FAILURE1·child SUCCESS1·controls SUCCESS2)이고 추가 child0이다. lab3 정상 stop3 후 Exit0/PID0/noOOM/restart0·물리 process/cgroup 소멸을 확인했다. 먼저 끝난 bootstrap까지 own4 stopped이며 기존15 lab+reader1=16과 기존 외부 컨테이너 fingerprint를 보존했다.

| 사건 | 실제 UTC |
|---|---|
| foreign control PIPELINE_START | 2026-10-16T08:51:56.302549+00:00 |
| main control PIPELINE_START | 2026-10-16T08:55:02.953825+00:00 |
| child PIPELINE_SUCCESS | 2026-10-16T08:56:45.707482+00:00 |
| owned_incarnation postchild tick1 완료 | 2026-10-16T08:57:40.837645+00:00 |
| owned_incarnation postchild tick2 완료 | 2026-10-16T08:58:40.873727+00:00 |
| owned_infra postchild tick1 완료 | 2026-10-16T08:57:35.920316+00:00 |
| owned_infra postchild tick2 완료 | 2026-10-16T08:58:36.006626+00:00 |
| control release | 2026-10-16T08:58:51.598422+00:00 |
| foreign release | 2026-10-16T08:58:51.603073+00:00 |
| control SUCCESS | 2026-10-16T08:58:51.803620+00:00 |
| foreign SUCCESS | 2026-10-16T08:58:51.869463+00:00 |

## 한계와 원 실패 보존

- 원 ARM/QEMU의 [역사 부분 증거](2026-10-16-common36-historical-partial-closure.md)는 그대로다. 그 r2의 postchild tick은 controls SUCCESS 뒤여서 원 동시 보호 gate HOLD였다. 이번 native 실행이 별도로 그 시간순서 빈틈을 검증했으며 과거 controller를 성공으로 바꾸지 않았다.
- ARM r3 audit timeout·배경 OOM137·별도 cleanup, native r2/r3의 SQLite 초기화 race·fault0·정상 정리도 모두 보존했다. r4는 모든 CS보다 앞선 원 SDK bootstrap으로 초기화 순서만 고쳤다.
- 최종 정산의 첫 스크립트는 snapshot canonicalJSON hash를 파일 pretty-bytes hash로 오인해 실패했다. 실제 audit() 계약에 맞춘 canonical 비교로 정산을 완료했으며 드릴/SDK/서비스 재실행은 없다.
- caps는 lab main1536MiB/foreign1024MiB/daemon1024MiB·합CPU2·각PIDs256, TTL1500/75초 grace 그대로다. bootstrap은 먼저 끝나는512MiB/.5CPU/PIDs64여서 lab3 동시 상한을 올리지 않는다.
- 기록한 cgroup memory.peak는 역할별 최대값이며 동시에 합산한 host peak/PSS가 아니다. 이 native 환경을 Odroid 메모리/CPU 개선 증거로 쓰지 않는다.
- singleton/exclusive origin·serial 교체·이전 worker 실제 소멸·clock 전제와 외부 수동 terminal race/원자CAS 아님·unreachable code-location 복구 불가 한계는 가이드 그대로다.
- 소비자 실제 활성화·신선도/live API/UI·운영 성능·병합은 별도 gate다. 제품/테스트/의존성/규범은 이 closure에서 변경하지 않는다.
