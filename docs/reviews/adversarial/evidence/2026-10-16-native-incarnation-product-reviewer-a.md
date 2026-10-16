# Common34 후속 독립 적대 리뷰 A

- 실행 ID: common34-review-a-d1aa4bb-20261016
- 시작/종료: 2026-10-16 09:23 / 09:26 KST
- 고정 HEAD: `d1aa4bbacab87af9ebae08757bd3fcb80f748fe9`
- 최초 base: `ad988a5dac252d710d41f9937b6d567c5d3398ae`; 수정 전: `cc954b834f0ecbbe05f921cbbd518911be150bb3`
- 체크포인트: `common34-native-incarnation-postfix-checkpoint-d-20261016.json` SHA `92eaf7d42dc4e68aec2b684a2e892ce91b473e47870401bbf9fa39850e083e5f`
- 전체 base diff SHA: `c455163bf8d860efcc6f1081abfde02638a2a6e302e9c34a71e4a16eb111c383`
- 격리: `/home/digitie/dev/kor-travel-common-review-a-native34-postfix-20261016` detached, 시작·종료 clean. 작성자 WT/제품 변경0, peer 원문 미열람.
- 범위: 초기 전체3파일 검토를 계승하고 수정3파일 223추가/7삭제 전체를 직접 읽었다. Clock/anchor/origin/cursor/pagination·SDK·재시도 부작용을 다시 확인했다.
- 요청: 초기 원문에 보존한 FULL 리뷰 요청 및 root의 “Common34 postfix독립closure우선 진행”을 따른다.

## A-P1-01 FIXED

recover 진입에서 실제 `type(instance.run_launcher) is DefaultRunLauncher`만 진행한다. 외부 launcher/custom subclass/조회 불능은 anchor·run 조회·상태 쓰기 전에 SKIP한다. 따라서 외부 worker가 살아 있는데 code-server init으로 사망을 추정하는 초기 반례를 차단한다.

현재 launcher만 바뀐 과거 실행도 보호하려고 run별 `.dagster/grpc_info`를 엄격 확인한다. 실제 SDK의 DefaultRunLauncher가 생성하는 host+port 또는 host+socket 형식에 한정하고, true SSL만 명시 태그를 허용하며 origin의 None/False와 태그 부재를 대응시킨다. 중복 JSON/추가 키/누락/문자열 port/bool port/다른 endpoint·SSL은 보류한다. 원래 exact persisted repository origin·job·선택 project/location 조건을 유지한다. 임의 태그를 보정하거나 증거 없는 실행을 자동 승인하지 않는다.

본인 초기 반례를 같은 실제 SDK1.13.24·생존 외부 스레드로 다시 실행했다. 수정 후 native STARTED/worker alive/SkipReason을 유지했다. 정상 Default launcher 페이지·늦은 실행·중복 이벤트·anchor 경합 양성 모형에는 SDK가 실제 생성하는 연결 태그를 명시했으며, 이 fixture 변경을 숨기지 않는다. 초기 반례 스크립트/결과는 그대로 보존했다.

## 직접 실행한 검증

| 검증 | 결과 |
|---|---|
| 수정 기준선 신규 시험, 실제 Dagster1.13.24 | 83 PASS / 2.39초 |
| 수정 기준선 신규 시험, 실제 Dagster1.13.25 | 83 PASS / 2.54초 |
| 별도 실제 SDK1.13.24 모형 | 5조건 PASS |
| 체크포인트3파일 SHA | 전체 exact |
| Python3.11 AST 문법 검사 | PASS |
| 전체 base diff whitespace / 종료 clean | PASS |

83개 시험에는 실제 SDK Default launcher의 태그 생산을 fake RPC 하나로 확인한 TCP/socket×SSL None/False/True 6개, 외부/custom/unknown guard, malformed/history 타입·추가 키·중복 키 검증이 있다. 실제 worker 시작이나 외부 gRPC 성공으로 집계하지 않는다.

본인 별도5조건은 외부 worker 오판 closure, 실제 SQLite status 변경 이후 cursor 순회(2→4→6→7), 한 바퀴 완료 뒤 새 구 실행 탐지, 실패 이벤트 각1개, 마지막 anchor drift에서 STARTED 보존이다. `common34-review-a-model-postfix-20261016.py` 및 같은 postfix safe JSON에 원문을 남겼다. 초기58와 현재83은 서로 다른 기준선의 실행이며 더해 전체141로 표시하지 않는다.

## 다른 경계와 잔여 한계

동일 boot의 최초 epoch 동결, 누적 slew 보류, private PID1 anchor, grace 최소60초·엄격한 이전 시작 시간, 정확 origin/launcher/run 연결, STARTED 전용과 마지막 실행 재조회가 유지된다. 한 tick 최대100×5 page와 협력적5초는 DB hard timeout이 아니며, 이 한계와 최종 read→event write의 비원자 경합을 가이드가 명시한다. pagination cursor는 실패 처리로 STARTED 필터에서 빠진 run ID에도 실제 SDK 저장소가 다음 페이지를 찾을 수 있음을 확인했다.

새 센서는 RunRequest·kill·relaunch·직접 SQL을 만들지 않는다. RUN_WORKER_RESTART는 기존 멱등 선언/상한/child 검사와 native retry 위임의 입력이며 별도 재시도 경로를 추가하지 않았다. 증거 없는 legacy run이 보류되는 것은 안전을 위한 의도된 제한으로 가이드에 수동 확인 필요가 적혀 있다.

운영 SSH/컨테이너/실제 NTP 변경·소비자 adoption·외부 HTTP·실제 Docker/K8s worker 재시작·운영 DB·live E2E는 NOT_RUN이다. 본인 전체 Python suite/새 wheel 빌드/실제 Python3.11 runtime은 NOT_RUN이며 작성자 결과와 독립 시험 수를 합치지 않는다. 실제 배포의 private PID namespace 및 code-server worker lifetime 전제는 소비자 단계에서 확인해야 한다. 소스 리뷰로 운영 CPU/RSS·복구 효과를 주장하지 않는다.

초기 BLOCK 원문 `common34-native-incarnation-review-a-initial-20261016.md` SHA `3b54abdf7a2f8c70ae745dfb6b2caa206bf4b9c74084ab7be0fdcd61f5bb441a`는 수정하지 않았다. 실행 도구/자기 스레드 모두 terminal이며 타인의 파일을 되돌리지 않았다.

Verdict: **PASS** — A-P1-01 FIXED, OPEN P0/P1/P2 0. 이는 현재 immutable 소스 판정이며 두번째 독립 심사·CI·소비자 검증을 대체하지 않는다.
