# Common34 native incarnation 복구 독립 FULL 리뷰 C

판정: **SOURCE PASS / OPEN P1 0 / OPEN P2 0**. 운영·소비자 승인과 분리한다.

- 실행 ID: /root/geo_timeout_analysis / common34-native-recovery-c-20261016.
- 요청: d1aa4bb의 독립 두 번째 specialist FULL 리뷰. D는 작성자이며 C는 Common35 후속 factory 작성자지만 이3파일의 작성에는 참여하지 않았다.
- immutable HEAD: d1aa4bbacab87af9ebae08757bd3fcb80f748fe9; base: ad988a5dac252d710d41f9937b6d567c5d3398ae.
- 대상3파일 SHA와 전체 diff SHA를 Git object에서 checkpoint와 대조했다. diff SHA c455163bf8d860efcc6f1081abfde02638a2a6e302e9c34a71e4a16eb111c383.
- checkpoint: common34-native-incarnation-postfix-checkpoint-d-20261016.json, SHA 92eaf7d42dc4e68aec2b684a2e892ce91b473e47870401bbf9fa39850e083e5f.
- 다른 reviewer 원문·결론은 읽지 않았다. author evidence를 독립 실행 결과로 합산하지 않았다.
- 제품/원본 WT/source/PG/운영 변경0. repo AGENTS·docs README/router·resume·T-319·agent workflow 문맥 및 private immutable manifest를 확인했다. 테스트는 별도 Git archive에서 실행했다. checkout/branch 이동0이며 검토 WT clean이다.

## 전체 범위와 주요 판단

packages/py/kor-travel-common/src/kortravelcommon/dagster_recovery.py 전체410줄, test_native_incarnation.py 전체686줄/83case, 가이드§15 전체를 읽었다. 다른 기존 runtime/scheduling/strict HTTP/gRPC health 모듈이나 의존성은 diff에 없다.

1. launcher와 worker 귀속: native_incarnation_recovery_sensor는 instance launcher의 정확한 type이 DefaultRunLauncher일 때만 진행한다. external/custom subclass/조회 불능은 anchor나 run 조회 전 보류한다. 과거 run도 exact repository origin ID/location/repository/job과 .dagster/grpc_info host·port/socket·SSL 형식을 검사한다. 중복/미상필드·잘못된 타입·증거 부재는 대상이 아니다. 일부 project tag 없는 과거 run 허용도 exact origin과 실제 launcher tag가 전제다.
2. init과 clock: 컨테이너 표식/private PID namespace/same cgroup/boot ID/PID1 ticks를 조회한다. user-code reload child의 시작을 anchor로 쓰지 않는다. Linux64 timex208-byte ABI/modes0·정상 NTP·오차1초와 realtime/boottime 짧은 표본·btime 교차확인을 거쳐 불명확하면 None이다. 같은 boot cursor의 epoch를 고정해 slew 누적으로 하한을 이동시키지 않는다.
3. 대상과 메모리: 오직 STARTED이며 start_time이 보수적인 init하한보다 최소60초 이전인 정확한 소유 run만 대상이다. 현재 incarnation/STARTING/QUEUED/CANCELING/terminal/시간 미상은 보존한다. 첫 tick은 cursor만 기록한다. page100×최대5page/협력적5초는 조회량·상주 row 수 한도이며 DB hard deadline이 아니다. 문서도 이를 구분한다.
4. 쓰기 경계: 직전 incarnation/clock과 run status/start_time/origin을 재조회한다. 공식 report_run_failed와 구조화 RUN_WORKER_RESTART 이벤트만 사용한다. 직접SQL/RunRequest/kill/reaper가 없다. 부분 성공 뒤 오류는 cursor 성공을 반환하지 않으며 다음 tick이 terminal을 재조회한다.
5. 원자성 한계: 최종 read→report 사이 외부 수동 terminal 전환은 원자 CAS가 아니다. 실제 SDK event_methods.report_run_failed도 condition 없이 공식 실패 이벤트를 쓰므로 문서의 잔여 경쟁 설명이 정확하다. 이 리뷰가 exactly-once DB 쓰기나 모든 수동 경쟁 해결을 승인하지 않는다.
6. 복구 정책: 기본 STOPPED, 활성화는 소비자 검증 후다. 실패 정산은 실제 retry/서버 재시작과 분리된다. 기존 infrastructure retry의 멱등/partial·provider 실패 이력·상한·child 검사가 후속 책임이며 native retry 위임 계약을 그대로 둔다. Common34만으로 영구 hung server가 회복되거나 queue가 해소된다고 주장하지 않는다.

## 독립 실행

실제 설치 Dagster/Dagster-GraphQL1.13.24를 사용했다. 원 Weather conftest·15432/15433·운영 DB는 접근하지 않았다. isolated archive PYTHONPATH를 설정하고 --confcutdir를 archive로 고정했다.

- immutable 대상 test_native_incarnation.py: **83 PASS, 2.54초**. 자체 임시 SQLite/가짜 RPC에 한정한다.
- 별도 C 모형 **8 PASS**: 첫 tick0write, 현재 incarnation 보존, 같은 location의 다른 exact origin 보존, worker history 불명 보존, STARTING 보존, old STARTED1건 정산, RunRequest0, clock drift 시 DB query0.
- 테스트 로그: common34-native-recovery-review-c-tests-20261016.log, SHA e97ceaadff14f31ba308c4a8adabcbd1aec6c69cd82f22133d44fe5bfeeabbb5.
- 독립 모형: common34-native-recovery-independent-c-20261016.json, SHA fb22f155e60e2349d6643854c10aced266d4140f2d376e2ee1266987031eaab1.
- archive 정산: common34-review-c-archive-20261016.json, SHA 6894eba876da1e9701c6acef40098ea23b41d5b82ebcc7d816fbd9ed2eb85f5b.
- SDK primary source 확인: DefaultRunLauncher.launch_run_from_grpc_client 실제 .dagster/grpc_info 태그 생산과 false SSL 필드 생략, launcher base의 health/resume 기본 미지원, event_methods.report_run_failed의 공식 실패 이벤트 경로. 설치 source를 읽었으며 외부/운영 호출0.

## 소비자 전제·남은 한계

이 API는 private PID namespace에서 **종료된 이전 code-server init의 worker**를 정산하는 계약이다. exact origin은 endpoint 귀속이며 구 컨테이너의 물리 사망을 네트워크로 증명하는 수단이 아니다. 같은 exact origin을 공유하는 살아 있는 구 서버와 신 서버가 겹치는 rolling/blue-green/LB 배포까지 자동으로 안전하다고 확대하면 안 된다. 이번 범위의 컨테이너 재시작 계약 밖이며 소비자 gate에서 구 init/worker 소멸과 단일 endpoint 소유를 확인해야 한다. 다른 launcher/증거 없는 run은 이미 보류한다.

과거 NTP 변경 이력 전체, clock namespace/운영 권한·파일 배치, 실제 host/private PID namespace, server교체·동시 타 location·정상 장기run·큐/신선도·CPU/RSS·live E2E는 **NOT_RUN**이다. 가이드는 현재 clock 교차확인의 한계와 code-location이 로드되지 않으면 센서가 실행되지 않는 한계를 명시한다. HC reaper/PID1 종료 제거를 Common34 등록만으로 완전 동등 복구라고 주장하지 않는다.

## Disposition

신규 확인 P1/P2 없음. 전역 native retry 활성화, supervisor 서비스 추가, HC 수치·튜닝, 소비자 pin/배포/센서 활성화는 이 SOURCE PASS에 포함하지 않는다. 실제 소비자 gate·다른 독립 reviewer·CI는 root가 별도로 확인한다. r5 continuation 작성 소스는 동결 상태로 유지했다. 모든 로컬 도구는 terminal이다.
