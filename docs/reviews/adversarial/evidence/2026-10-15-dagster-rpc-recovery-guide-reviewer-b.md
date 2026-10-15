# Common PR #30 RPC·복구 가이드 독립 FULL 리뷰 B

- execution_id: `common-guide-rpc-review-b-20261015`
- 전문 영역: backend·운영 정합·문서 정본·검증 과장·비밀 노출.
- 검증 실행 시작: `2026-10-15T05:50:36.727127+00:00`; 종료·immutable 연결 확인: `2026-10-15T05:51:49.892128+00:00`. 이 시각은 로컬 검증 실행 기준이며 정적 독해는 그보다 먼저 시작했다.
- 최종 verdict: **PASS / OPEN 0**.
- 최종 immutable commit: `61f93d98d5d7df9b3e597eefd9d7d04e7bbf098b`; parent `ae5ca6c5bfaf6e514cc2d5b41855c14af67d3de7`; 전체 델타 base `091d4fe1dda8eacf43b453ad39b4f2e42e9e80fc`.
- 범위: `docs/runbooks/dagster-adoption.md`와 `docs/journal.md` 전체 델타 및 가이드 전체 맥락. 최초 ae5는 2파일 53행 추가, 최종까지는 2파일 54행 추가다. 최종 parent delta는 heartbeat 문단 한 곳뿐이다.
- 격리: WSL Ubuntu-26.04, `/bin/bash --noprofile --norc`. Git object-only 독해와 자기 임시 snapshot 검사, 로컬 설치 SDK의 순수 함수·합성 heartbeat, 기존 저장 증거의 선택 필드만 사용했다. 작성자가 요청한 중간 working guide를 읽었고 최종 Git object가 그 검증 바이트와 동일함을 다시 확인했다. 최종 worktree clean.
- 운영·네트워크·SSH·Docker·API·DB·브라우저 호출 0, 제품·문서 수정 0, 타인 리뷰 원문 **NOT_READ**. 이전 B 원문을 덮지 않았다.

## Finding disposition

**B-P3-01 / P3 / FIXED — heartbeat tolerance와 실제 cutoff 구분**

초기 ae5 가이드 **441~445행**의 “허용 지연 300초 / 기본 판정 1800초”를 실제 heartbeat age cutoff로 복제하면 기존 SDK 계약과 달라진다. Dagster 1.13.24 `get_daemon_statuses`는 `heartbeat_timestamp + heartbeat_interval_seconds + heartbeat_tolerance_seconds`를 사용한다. 기본 interval은 30초다. 최종 문서는 300/1800을 tolerance 설정값으로 명시하고 interval 합산과 같은 instance·required daemon 집합·heartbeat·interval·tolerance·오류 처리 계약 보존을 요구한다. 로컬 SDK에서 330초까지 허용/331초 거절, 기본 tolerance의 1830초까지 허용/1831초 거절을 확인했다.

검토 중 B가 덧붙였던 “GraphQL은 오류를 별도로 평가하므로 CLI와 다르다”는 설명은 **철회**한다. 하위 helper 기본 인자만 보고 instance wrapper의 `ignore_errors=True` 전달을 놓쳤다. 실제 `dagster_graphql/schema/instance.py` → `DagsterInstance.get_daemon_statuses` → `instance/methods/daemon_methods.py` 경로와 CLI `all_daemons_live`를 직접 확인하면 둘 다 이 경로에서 errors를 무시한다. 작성자는 그 중간 문구를 제거했으며 최종 immutable 문서에는 잘못된 차이 주장이 없다. 이를 확정된 제품 finding으로 집계하지 않는다.

새 OPEN P0/P1/P2/P3는 없다.

## 전체 판단과 공격한 경계

- **RPC 범위:** daemon→proxy→API child의 두 구간과 외부 STARTING monitor를 구분한다. proxy StartRun의 하위 `_get_response`와 daemon client `_query`가 일반 RPC 기본값을 사용함을 읽었다. 일반 `DAGSTER_GRPC_TIMEOUT_SECONDS`가 StartRun 전용이라는 잘못된 안내가 없다. 실제 utils 함수로 기본 60, general 변경이 sensor/schedule/repository/shutdown에 전파되는 경우, specialized env를 명시해 기존 값을 보존하는 경우를 검증했다. 300<360<600은 검증한 ARM64 소비자 예시이며 공통 기본값·일반 성능 보장이 아니다. 실행 중 프로세스에 env 파일 편집만으로 반영됐다고 간주하지 않는다.
- **실행 증거:** timeout을 미실행으로 바꾸거나 기존 FAILURE를 덮는 안내가 없다. 새 검증 run의 queue event·origin/worker·terminal·업무 출력·백업 불변을 연결하고 과거 실패를 별도 보존한다. 저장된 canonical NOOP의 같은 run SUCCESS·큐 이벤트·기대 endpoint·backup disabled/no-enqueue·inventory 불변과 실패 이력 보존을 대조했다. 이 리뷰에서 실제 run을 새로 실행한 것은 아니다.
- **정본 origin:** 실제 workspace/저장 상태의 origin ID·selector·정의 metadata를 함께 비교한다. 설치 1.13.24의 실제 `GrpcServerCodeLocationOrigin` 생성자로 생략된 None과 명시 False가 모두 비TLS이면서 ID는 다른 것을 확인했다. selector만으로 동일성을 인정하거나 다른 버전에 생략 규칙을 일반화하지 않는다.
- **checkpoint/CAS:** 원본·관측 snapshot을 남기고 특정 승인 상태의 전체 SHA를 fresh CAPTURE와 strict 비교하며 ACTIVATE 전체 CAS를 유지한다. 중지 schedule의 유한·단조·시간 범위 내 checkpoint만 구분하고, 런타임 임의 정상화·자동 승인·sensor cursor/origin/status 차이 무시로 넓히지 않는다.
- **CPU·health:** memory/load 단일 지표나 모든 CS probe의 전체 Dagster import 비용만으로 원인을 단정하지 않는다. 실제 PID/CID 귀속, CPU 경쟁, 열에 따른 클럭 제한을 분리 관측한다. common 경량 probe의 생성 protobuf 직접 로딩 구현과 맞는다. 경량화가 daemon thread heartbeat·CS child 복구·active run 보호·orphan reaper를 대체한다고 주장하지 않는다.
- **sensor·Janitor:** 실제 public start와 최초 tick, cron 계산과 실제 cron을 구분한다. 저장된 두 sensor 최초 tick은 각각 SKIPPED/0run이고 다른 세 schedule은 STOPPED였다. Janitor canonical ACK는 fresh start와 backup/drill STOPPED, `first_cron_observation=NOT_RUN`을 별도로 남긴다. journal의 새 NOOP·두 sensor·Janitor 관측 주장은 이 범위와 맞는다. 최초 Janitor 실제 cron·전체 batch·모든 소비자 이전 완주를 PASS라고 과장하지 않는다.
- **소유권·정본·보안:** Common에 새로운 앱 도메인 SQL·provider·독립 제어 서비스를 넣지 않으며 Python 공개 API·기본 튜닝·채택 완료 상태를 바꾸지 않는다. 운영 lifecycle은 Manager, 데이터·백업·인증은 소비자 소유라는 기존 경계를 유지한다. 가이드는 실행 절차의 정본이고 journal은 변경 기록이다. 운영 주소·자격 증명·DSN·쿠키·원본 로그가 두 파일 델타에 없다. 공식 참고 원문은 버전 1.13.24로 고정되어 있다.

## 검증 및 evidence

- 최종 guide SHA256: `3819e84cf3864457e419989d06cd9ce0dceef7d8a08f50eb011d1f3036d89454`.
- journal SHA256: `d6658a7c51751f4e08d9b10796ca799ba37e3b611e8a1a0b11110292f0681469`.
- `common-guide-rpc-review-b-check-final-20261015.json`: **40 조건 PASS**, SHA `8945ad9db2be1a4ce4206cc3dde5f79ea1bdb96e69140bccbe1a922880c8e7e3`. 실제 로컬 SDK 1.13.24의 deterministic 함수, 저장 증거와 문서 snapshot 검증이다. 최초 B 검증 스크립트의 import 경로 및 fixture timestamp 타입 오류는 자기 스크립트에서 고친 뒤 재실행했다. 중간 문구의 31조건 결과는 최종 결과와 합산하지 않는다.
- 같은 최종 바이트의 자기 임시 snapshot에서 문서 링크 **688 docs / 2797 targets / errors 0**, 계획 **109 / errors 0**. base→최종 `git diff --check` PASS.
- `common-guide-rpc-review-b-immutable-20261015.json`: SHA `c74bc40880ce8b4ba16971250a97b8fcbd248130157287c2b4e3424c2bd25061`. 최종 parent ancestry·2파일 전체 범위·clean status·최종 object와 검증한 두 blob의 SHA 및 delta 동일성을 확인했다. 검증 snapshot은 최종 commit과 내용상 동일하다.
- 저장 증거의 안전한 projection `common-guide-rpc-review-b-safe-proof-final-20261015.json`: SHA `31df336ce98ea429bf30ffad4507a912994ede0d1f5d17993806ab0897270350`. 원본 credential/address/run identity 값은 공개 원문에 옮기지 않았다.
- 작성자가 전달한 unittest **337 실행 / 336 PASS / 1 SKIP**은 B가 재실행하지 않았고 skip을 PASS로 합산하지 않는다. 새 운영 재배포·live E2E·최초 cron·전체 batch·모든 소비자 완주는 이 문서 리뷰에서 **NOT_RUN**이며 문서 승인으로 대체하지 않는다.
