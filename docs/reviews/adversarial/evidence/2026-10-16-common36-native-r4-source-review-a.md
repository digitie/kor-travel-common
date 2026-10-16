# Common36 native owned LIVE r4 독립 리뷰 A

판정: SOURCE_PASS / 열린 P0·P1·P2 = 0. 실제 LIVE 성공 판정은 아니다.

## 고정 대상

- checkpoint common36-native-live-d-r4-20261016.checkpoint.json:
  9ae1243792516831eba6dfd0c324404023bb53825f0afcd7d4312cd787e302ba
- once.py: 8cc6866154d2c803585e044c83e249c28111b966e3753497b07983bc2b2e122c
- r3→r4 delta: 3f89bed201cb10181ff225dc657d7fd211d6e5432d8a6517cf7cd97db642566e
- 정의 fixture: 5f7a465c5e1a058587bc7dae8740854117b018b90441ceea8812a3b901b8bd28
- native artifact runtime manifest e5ccda09… / config ce6e7655… / amd64.
- Common 제품5d2ad2bb45e64197ea359e0e5136b84780dab97a, Weather source f1d59f79…, SDK1.13.24.
- source5 전체(build/context/verify/definitions/once), once1050줄, r2 controls 시간/r3 직렬 위치/r4 전체 delta와 저장된 artifact를 직접 읽었다.
- 이번 root/author/다른 reviewer의 모델·판정 원문은 읽거나 합산하지 않았다. handoff는 저자 설명으로만 사용했다.

## 경계와 의미

새 bootstrap은 독립 새 UUID root에 생성한 instance 설정과 expected.json만 공유하며 모든 main/foreign/daemon 생성 전에 실행된다.
동일 immutable 이미지에서 실제 DagsterInstance.get 컨텍스트를 열고 exact DefaultRunLauncher·QueuedRunCoordinator/native retries OFF,
runs0·instigators0 및 run/event/schedule 세 storage의 revision==head를 검사한다.
컨텍스트 종료 뒤 disposed 양성을 출력한다. 직접 DDL/stamp/이전 tainted SQLite 변경은 없다.
SDK 메서드명·tuple 반환 경로는 설치된1.13.24 세 SQLite storage 소스를 읽어 확인했으며 SDK를 import/호출하지 않았다.

create 검토: pullnever·netnone·privatePID·readOnly·capdropALL·no-new-privileges·restartno,
memory=swap512MiB/.5CPU/PIDs64와 자기 /drill mount1개. 동일 조건을 inspect로 검증한다.
자연 wait0·로그의 빈 instance/3revision·동일 Config/HostConfig/Mount·restart0/noOOM/dead/restarting/exec없음,
oldPID+startticks 소멸과 cgroup 비움을 통과한 뒤만 phase STOPPED_VERIFIED_BEFORE_ALL_CS가 된다.
이 뒤의 foreign_fence는 원16 stopped 전체 fingerprint와 종료 bootstrap의 exact fingerprint도 계속 검사한다.
bootstrap이 끝난 뒤 기존 lab3만 시작하므로 동시 memory3.5GiB/CPU2를 늘리지 않는다.
OomKillDisable None/False의 기존 Docker 기본값 정규화만 있고, true나 다른 HostConfig drift는 거절한다.

기존 command/UNKNOWN 무재전송·audit/worker 매핑·run budget·control identity 보호는 AST 동일이다.
run()은 첫 bootstrap call1개 삽입 외 r3와 AST 동일임을 실제 AST로 확인했다.
75초 parent grace/실제clock·NTP/privatePID/cgroup·faultKILL1 최대·물리 oldworker 소멸·첫 anchor only 역사증거,
공식 RUN_WORKER_RESTART1·child1 SUCCESS/duplicate0·양 control의 childSUCCESS 이전 실제 시작 확인,
두 센서별 추가 completed ticks2 이후 release·controls SUCCESS·자기3개 normalstop을 유지한다.
원16은 다시 start/stop하지 않으며 archive load/다운로드/PG/provider/운영 경로도 추가하지 않았다.

## 독립 실행한 검사

- source5 exactSHA 및 compile5 + bootstrap 문자열 compile: PASS. 제품/SDK 실행 아님.
- archive127441920B fullSHA FD/path identity 전후 확인, manifest/config digest 구분,
  expectedConfig/RootFS/architecture amd64·source57/dists101 메타·context/buildreceipt 고정SHA: PASS.
- 실제 bootstrap_instance·foreign_fence·controls_started_by_child_success를 AST 추출해
  CLI/proc/cgroup/inspect만 순수 stub으로 대체한 독립51조건 PASS.
  정상 None/False, wrongimage/namespace/resources/no-new-priv/port, nonzero·unknown wait,
  SDK version/lab/common/runs/instigator/disposed·revision 누락/불일치,
  terminal Running/PID/137/OOM/dead/restarting/config/mount/restart/실제PID소멸 실패,
  기존 foreign 누락/metadata drift·bootstrap 미완료·control 늦은 시작/NaN/종료를 거절했다.
- 원 첫 reviewer 모델은 AST 본문 위치를 [7]로 잘못 단정해 실패했다.
  해당 모델 원본은 보존했고 [6] 위치의 bootstrap이 모든 create보다 선행하는 상대 순서 및
  call제거 후 전체 AST동일을 검증하도록 모델만 새 r2로 고쳤다. 제품 결함/OLD_RED로 집계하지 않는다.
- Docker/SDK/DB/clock 조회·실험·서비스·SSH·HTTP·빌더 실행0. 모든 도구 terminal 회수.

## 실행 한계

bootstrap import/초기화가 너무 빨리 끝나 livePID를 포착하지 못하면 안전하게 중단한다.
512MiB OOM·60초 UNKNOWN·revision 실패도 실제로는 새 lab이 남을 수 있으므로 읽기 정산 전 재실행/임의 cleanup 금지다.
이번 검토는 실제 SQLite 초기화 race 해소·전체 fault/controlsheld LIVE 완주·Odroid ARM 비용 개선을 입증하지 않는다.
r2/r3 이전 실제 실패·cleanup 부분 양성은 별도 보존하며 성공으로 바꾸지 않는다.

## 자체 원문
- common36-native-live-review-a-r4-r2-20261016.model.py: cee6b4301b0ea7523429a23618360407646ad57c01bbae3d2b5c1e6b5c1e07d5
- common36-native-live-review-a-r4-r2-20261016.model.json: 7084e1a4ea3cd7eef114fb3d7993f3548f3fa38de727623d23ff982591266fdc
- common36-native-live-review-a-r4-20261016.artifact.json: cbcff1e74caee7f47931a2550353ef205c8855467b5a9bc80ff3f52be22e718b
