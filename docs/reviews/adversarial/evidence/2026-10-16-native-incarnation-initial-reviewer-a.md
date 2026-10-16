# Common34 초기 독립 적대 리뷰 A

- 실행 ID: common34-review-a-cc954b8-20261016
- 시작: 2026-10-16 09:17 KST / 종료: 2026-10-16 09:21 KST
- 기준 HEAD: `cc954b834f0ecbbe05f921cbbd518911be150bb3`; base: `ad988a5dac252d710d41f9937b6d567c5d3398ae`
- 작성자 체크포인트: `common34-native-incarnation-source-checkpoint-d-20261016.json`, SHA `db9dfbb50ab84d38f573c4b13d83af46088137d7c984a33ad0e786c70e5d3025`
- 전체 diff SHA: `6b179d4fdac4ee1c0d702248c9281c05cf3a71bb6a5f1affd39238f411bdef09`
- 격리: `/home/digitie/dev/kor-travel-common-review-a-native34-20261016` detached HEAD, 시작·종료 추적 파일 clean. D 원본 수정 없음. 다른 reviewer 원문 미열람.
- 범위: 신규 dagster_recovery.py 349줄, 신규 test_native_incarnation.py 540줄, 가이드 §15 83줄 전체 및 기존 infrastructure retry/API·실제 SDK1.13.24 호출 문맥.
- 전문 관점: clock/anchor·실행 소유권·origin·cursor/pagination·경합·복구 요청 중복·SDK 호환성.

## 요청 원문

“현재 독립 검토 가능한 Common34(D 작성) 소스/테스트를 읽고 적대적으로 검토하세요. D에게 현재 커밋 freeze 요청 후 immutable head 기준으로 검토, 초기 결함은 D에게 직접 전달하고 root에도 보고. 별도 Common 작업 트리에서 검증하고 D 원본은 변경하지 마세요. 다른 에이전트와 같은 코드베이스에 있으므로 타인 변경을 되돌리지 마세요. 운영 호출/변경 금지. Clock/anchor/origin/cursor/pagination/race/SDK compatibility/재시도 남발 관점 중요. 현재 다른 리뷰어 C는96 작성 중이므로 두번째 검토는 추후 root가 맡거나 별도 요청합니다. 최종 검토 보고에 실제 실행한 체크와 미실행 구분.”

## A-P1-01 — 외부 launcher의 살아 있는 worker를 code-server init 시각으로 실패 처리

- 위치: `packages/py/kor-travel-common/src/kortravelcommon/dagster_recovery.py:273` 및 `:333`.
- 상태: OPEN, 작성자 수용. root가 같은 문제를 독립 제기했으므로 논리 finding 하나로 조율하며 별개 두 건으로 집계하지 않는다.
- 재현: 실제 SDK1.13.24의 격리 DagsterInstance에 별도 생존 스레드를 시작하는 외부 RunLauncher를 등록하고, 정확한 origin/STARTED/구 시작 시각을 가진 native run을 만들었다. 동일 실제 sensor.evaluate_tick이 살아 있는 외부 worker를 종료하지도 확인하지도 않은 채 native FAILURE/RUN_WORKER_RESTART로 기록했다. 이는 운영 컨테이너 재현이 아니라 실제 공용 함수·SDK 저장소와 자기 스레드를 이용한 로컬 반례다.
- 원인: PID1이 재시작되면 worker도 소멸한다는 전제는 code-server 내에서 worker를 시작하는 DefaultRunLauncher에 한정된다. 현재 factory와 recover는 launcher 종류를 검사하지 않는다. Docker/K8s/custom launcher에서는 code-server만 재시작되어도 run worker가 계속 살아 있을 수 있다. exact repository origin과 STARTED/start_time 조건은 launcher의 worker 수명을 증명하지 못한다.
- 영향: 정상 외부 실행을 실패 처리하고 기존 infrastructure_retry_sensor가 멱등 실행에 새 child를 발급할 수 있다. 실패 이벤트만 쓰는 모듈이어도 정상 실행 귀속을 손상시킨다.
- 권고: recover에서 정확한 DefaultRunLauncher만 허용하고 외부·알 수 없는 launcher 및 동작이 다른 subclass는 SKIP한다. 가이드에 지원 범위를 적고 실제 SDK 음성 회귀로 쓰기0을 검증한다.

## 실제 실행·검토

- 본인 detached 기준선의 신규 테스트 58개: PASS, 실제 SDK1.13.24, 1.44초. 로그 `common34-review-a-baseline-tests-20261016.private.log`.
- 본인 별도 모형 5개: 외부 생존 worker 오판 재현 1건, 실제 SQLite cursor에서 상태 필터 제거 후에도 2/4/6/7개 순회, 완주 후 늦게 추가된 구 run 발견, 실패 이벤트 중복0, 마지막 anchor 변경 시 STARTED 보존. 스크립트 `common34-review-a-model-20261016.py`, 결과 `common34-review-a-model-baseline-20261016.safe.json`.
- 실제 SDK source에서 get_run_records의 run-id cursor/기본 역순 및 report_run_failed의 구조화 이벤트 쓰기를 확인했다. 최종 재조회와 이벤트 기록 사이 비원자 경합은 가이드가 명시하며 이 구현에서 해결됐다고 주장하지 않는다.
- clock은 동일 boot의 최초 epoch를 동결해 누적 slew가 cursor 기준을 옮기지 않는다. 불확실한 NTP·init 표본/경계 동등/다른 origin·project·job은 보류한다. DB call 자체 hard timeout이 아닌 협력적 5초 한계와 bounded page 100×5도 가이드가 구분한다.
- `git diff --check` PASS. 새 실행 모듈은 AST/파일 읽기 범위에서 Python3.11 문법 호환을 확인했으며 실제3.11 전체 시험은 본인 미실행이다.

## 미실행·한계

운영 SSH/컨테이너/외부 HTTP/소비자 DB·SDK 호출·실제 NTP 변경·실제 Docker/K8s 재시작·소비자 E2E는 모두 NOT_RUN. 공용 패키지 전체 suite/새 wheel 빌드는 본인 미실행이며 작성자 결과를 독립 시험 수에 합산하지 않는다. 실제 Docker private PID namespace와 worker 소멸의 배포 전제는 소비자 검증이 필요하다. 제품 소스 변경0, 운영 변경0, 실행 도구 모두 terminal.

Verdict: **BLOCK** — OPEN P1 1건, P2 0건. 수정 immutable에서 closure와 전체 delta를 다시 확인해야 한다.
