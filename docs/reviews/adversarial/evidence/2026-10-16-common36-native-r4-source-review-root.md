# Common36 native r4 root 독립 리뷰

SOURCE_PASS, 열린 P0/P1/P2 없음. CP9ae12437/once8cc68661 및 delta3f89bed2 전체를 읽었다. 원 r1 전체 source5/artifact와 r2 시간경계·r3 검토를 상속한다. 원 r2/r3 초기화 실패·DB·정리 원문을 유지한다.

실제 SDK를 모두 시작하기 전 순서가 핵심이다. 새 one-shot bootstrap만 새 소유 /drill에서 DagsterInstance.get을 실행하고 run/event/schedule 세 storage revision=head, runs0·instigators0·정책을 확인한 뒤 dispose한다. 자연Exit0와 정확 init PID/ticks·cgroup 소멸 및 Config/HostConfig/Mount 보존이 확인된 다음에만 main/foreign/daemon3을 시작한다. host /drill·원 tainted DB·수동DDL/stamp/합성시계는 사용하지 않는다.

bootstrap은 별도512MiB/swap512MiB/.5CPU/PIDs64/readOnly/privatePID/netnone/capdropALL/no-new-privileges/포트0이며 먼저 끝나므로 세 lab의 동시3.5GiB/CPU2 예산을 늘리지 않는다. 정확16 stopped와 종료 bootstrap fingerprint를 후속 foreign_fence에서 확인한다. 실패/UNKNOWN에는 자동 retry/fault를 추가하지 않는다. 빠른 자연 종료를 live inspect보다 먼저 관찰하면 여전히 failclosed이며 성공으로 추정하지 않는다.

추가 SDK 소스 읽기로 세 storage의 alembic_version() 계약·event index shard 생성 및 SDK startup도 instance를 여는 경계를 확인했다. 실제 BOOTSTRAP_PROGRAM AST를 import 없이 대역 실행하여 dispose 후 JSON 양성과 runs/states/retry/버전/세 schema mismatch 거절을 확인했다. 상속 메서드 및 bootstrap이 모든 server create 이전이라는 호출 순서도 확인했다. 새로운 실제 SDK/DB/Docker/실험0이다.

원 공식 RUN_WORKER_RESTART·child1 SUCCESS·native budget0·실제 child 성공 전 양 control 시작/STARTED·동일 물리 worker/RPC·센서별 완료2tick 이후 release·75grace/1500TTL는 변경하지 않았다. A 독립 리뷰와 실제 새 UUID 1회 결과가 추가로 필요하며 이번 source 리뷰를 full LIVE나 Odroid 성능 PASS로 쓰지 않는다.

모델 SHA256 98e172a57710b5dc4d59da154cb994f9c83714c0b510a77c497e3bc5ab7777e5
