# Common36 격리 복구 시나리오 부분 증거 종결

- 실행 식별자: common36-historical-partial-closure-d-20261016.
- 제품/검토 pin: 5d2ad2bb45e64197ea359e0e5136b84780dab97a. 문서 출발 HEAD: 872072f3c9847d69aac7905f2ff60a397987ba9a.
- 판정: **역사 증거의 부분 검증 PASS / 원 전체 LIVE gate HOLD**. 제품 SOURCE_PASS 두 명과 실제 전체 시나리오 PASS는 다른 gate다.
- 환경: WSL의 ARM64/QEMU 격리 lab, Dagster1.13.24·Weather99 f1d59·Common36 5d2. 운영 Odroid native ARM 및 소비자 수집 성능 증명이 아니다.
- 원본 소스 리뷰는 [A/C 최종 소스 판정](2026-10-16-pid1-leader-clock-closure.md)에 그대로 보존한다. 제품·테스트·의존성·clock/cursor/활성화 규범 변경은 없다.

## 실제 r2 시간순서와 확인 범위

lab 식별자 0a0443e6-ea68-4e7e-8059-d626e89f58ff의 보존 SQLite와 원 영수증을 검증했다.
원 controller 영수증 SHA87c01138c077da6bb9cb55bebb4f9aab57c159b9dbf2a463a5dba2b6e25e7620의 실패는 그대로다. 별도 continuation/정상 정리와 사후 읽기 검증을 합친 **composite 부분 증거**다.

1. 소유 main에 fault 신호1회, 새 init의 실제 clock 첫 anchor tick19는 SKIPPED였다. 당시 부모는 STARTED, 실패 event0, RunRequest0이었다. 기존 cursor 초기화로 얻은 결과가 아니다.
2. 부모 bf3b027e-feaa-4a2e-8f1f-046c0d08d1d2는 공식 RUN_WORKER_RESTART FAILURE event1개로 정산됐다.
3. Common 인프라 재시도 자식 62d0c2c6-46f3-4b2a-8172-3b451059461b만 발급되어 SUCCESS(1792131587.019034)였다. exact origin/project/config와 infra parent 태그·결정적 run key·attempt1로 결박된다. Dagster parent_run_id는 null이므로 native reexecution 계보라고 부르지 않는다. 총 run4, 전 run native retry budget0이다.
4. foreign와 동일 location의 control 두 개도 SUCCESS였고 소유 세 컨테이너는 별도 정상 종료했다.
5. 자식 성공 뒤 owned_infra tick24/26, owned_incarnation tick25/27이 각각 완료 SKIPPED/run_ids=[]였다. 추가 자식0이다. 단 이 tick들은 **control 두 개가 이미 SUCCESS한 뒤** 완료됐다.

| 실제 사건 | epoch 초 |
|---|---|
| child SUCCESS | 1792131587.019034 |
| control 두 개 SUCCESS | 1792132324.493112 / 1792132324.542734 |
| infra tick24 / 26 시작 | 1792132353.424815 / 1792132414.634313 |
| incarnation tick25 / 27 시작 | 1792132355.012016 / 1792132417.608452 |

따라서 “정상 control들을 STARTED로 유지한 상태에서 child 성공 뒤 두 센서의 두 tick 동안 오판/중복이 없음”이라는 원 run()의 동시 보호 gate는 아직 통과하지 않았다. 사후 tick 양성만으로 이 시간순서 조건을 대체하지 않는다. 전체 LIVE·merge 최종 gate를 닫지 않는다. Weather 실제 live UI34도 이 기록에서 합격으로 처리하지 않는다.

## 독립 확인과 안전 증거

D는 정확 보존 DB를 mode=ro/query_only로 읽었고 root와 C가 별도로 실제 DB를 읽어 확인했다. C는 소유 세 컨테이너가 현재 stopped/PID0/Exit0/OOMfalse/RestartCount0이며 대상 DB/WAL 읽기 전후 SHA가 같은 것도 확인했다. 여러 DB 파일 전체의 원자 snapshot은 아니며, 컨테이너들이 정지한 상태였다. 정확 시작/종료 시각이 없는 기록에 임의 시각을 보충하지 않는다.

| 근거 | 원문 SHA256 / 보관 방식 |
|---|---|
| D 실제 RO 관측 | 694912926240fc32894f9b6f5c9ddf0f076dc988d83d78e6b2df92a6f792e97f → [명시 allowlist 투영](evidence/2026-10-16-common36-historical-d.safe.json) |
| root 독립 실제 RO 확인 r2 | a8ba234ec36cfb1b70f91cc6e34a41209c206957cf94fc59de2c444c49d61923 → [명시 allowlist 투영](evidence/2026-10-16-common36-historical-root.safe.json) |
| C 독립 실제 RO 확인 | [원문 MD](evidence/2026-10-16-common36-historical-reviewer-c.md), SHA70693c85c8af0a5d19b8ee05e77989c35c98bf2463cac26198299d3c4d57c57b |
| C 안전 JSON | [원문 안전 투영](evidence/2026-10-16-common36-historical-c.safe.json), SHA893ed66c268d88b6b90f79c889a85ea1f7f442424b28aab3cc0af70390e5624c |

D/root 투영은 원시 private JSON 복사가 아니다. 원문 SHA를 보존하고 run 상태·센서 tick·시간·개수·범위만 선택했다. 투영본은 private 산출물에서 repo evidence로 바이트 동일 복사했다. C의 MD·안전 JSON도 byte 동일 복사했다. 원시 Env/DSN/full Config·운영 주소·cursor는 반입하지 않았다. D 실행자와 독립 root/C의 관측을 중복 시험 수로 합산하지 않는다.

root 최초 r1의 child event shard/index mirror 중복 집계 assertion 실패와 C 최초 reader의 더 강한 시간순서 assertion 실패는 private 원문 그대로다. 정확 child shard의 SUCCESS event1개만 계산하며 mirror를 추가 run/성공으로 세지 않는다. 시간순서 한계는 후속에서도 유지한다.

## 실패·정리 기록 보존

| 실행 | 관측과 판정 |
|---|---|
| r2 원 controller | FAILED 유지. daemon OOM137와 이후 C continuation의 Mounts 배열 순서 false assertion도 보존한다. C 별도 정상 정리 receipt SHA1451f0b1684dd5683f99c96a9b504a873bb5b0c873500e262fa610b49f57733b는 원 controller PASS가 아니다. |
| r3 새 lab | fault0. main SDK audit의 실제 Docker exec는 약65.003초 뒤 Exit0였지만 caller60초에서 TimeoutExpired/UNKNOWN으로 끝났다. 이 당시 결과를 소급 SUCCESS로 바꾸지 않는다. 이후 background daemon OOM137도 실제 발생했다. import/SQLite/RPC 비용별 분해나 OOM 할당 원인은 미확정이다. |
| r3 cleanup 첫 시도 | daemon이 이미 OOM 종료되어 Running 가드에서 중단; release0/stop0/fault0. |
| r3 별도 cleanup r2 | receipt SHA7d4d3c0e96e9d60a869d5ea40386541febec071b29c698dd2c78af5a8c29c0ab. 기존 두 run만 release2→자연 SUCCESS→worker 소멸→main/foreign 정상 stop Exit0. 이미 OOM137인 daemon stop0. 원 drill LIVE=false/fault0 유지. |

실패·UNKNOWN·SQLite·원 영수증/로그를 삭제하거나 양성으로 덮지 않았다. r3 cleanup은 r2 제품 복구 부분 증거와 별도이며 새 fault/retry 검증이 아니다. QEMU lab 자원 실패를 Odroid 운영 제품 메모리 원인으로 일반화하지 않는다.

## 다음 gate

남은 동시 보호 순서를 검증하려면 별도 검토된 native amd64 SDK1.13.24 격리 lab 계획을 고려한다. QEMU cold CLI를 반복하거나 제품 deadline/TTL/cap을 높여 PASS를 만들지 않는다. 현재는 cached image/host SDK 가용성만 읽었으며 새 build/pull/container/fault0이다. native 계획도 ARM 원본 증거를 대체하는 운영 성능 시험은 아니다.

소비자 exact image/등록·기본 STOPPED에서의 승인된 전이·물리 old worker 소멸·운영 live/수집 신선도·CPU/RSS 및 PR36 병합은 별도다. 전역 T-319는 IN_PROGRESS다. 이 문서 종결은 review closure artifact이며 기존 규범·제품을 바꾸지 않는다.

## 이번 문서 종결 검증

링크731문서/2902 local targets 오류0, plan109 오류0, 문서 도구 unittest337실행/336PASS/1SKIP(66.616초), 공백 검사 PASS다. 전체 트리 secret scan1138파일/발견0·예외0을 확인했다. 제품 packages·워크플로·versions는 검토5d2 대비 바이트 불변이며 제품 시험을 새로 실행한 것으로 집계하지 않는다. CodeGraph는 이번 증거/문서 전용 정산에서 실행하지 않았다. 출발872의 CI8SUCCESS는 GH에서 확인했으나 새 문서 HEAD의 CI는 별도로 추적한다.
