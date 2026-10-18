# Common41 독립 적대 리뷰 C — 초기 원문

- 요청: native 영속 멱등 제출의 전체 diff를 독립 검토하고 실제 SDK 1.13.24/1.13.25의 소유 SQLite에서 반례를 확인한다. 수정 권한은 없다.
- 저장소: /home/digitie/dev/kor-travel-common-codex-native-submit-20261018
- 불변 base: 27cd146ed9e83d3ef481757d2b48e16f232dc88c
- 불변 head: 23e4775cf883b672ababad1b291bddd3441c9c63
- 제품 모듈 SHA256: 1a55cf10f06ce561bc143f2293d0e7b7d8bbaaa786ce7bc8df976b50515593bc
- 판정: **SOURCE_HOLD / 열린 P1 1건 / P0·P2·P3 0건**. 작성자가 진행 중인 후속 수정은 이 판정에 포함하지 않는다.

## C41-C-P1-01: 오래된 NOT_STARTED 제출이 STARTED를 QUEUED로 되돌린다

위치: packages/py/kor-travel-common/src/kortravelcommon/dagster_webserver.py:150–151.

run ID 유일키는 행 중복을 막지만 상태 조회와 submit_run을 직렬화하지 않는다. 실제 native instance.submit_run이 읽은 NOT_STARTED SubmitRunContext를 native QueuedRunCoordinator에 늦게 전달하면 이미 시작된 같은 run에 RUN_ENQUEUED를 다시 기록한다.

소유 fixture의 순서:

1. 첫 제출의 submit 직전 TimeoutError를 주입하여 실제 SQLite에 NOT_STARTED 행 하나를 남긴다.
2. 복구 요청 A가 instance.submit_run 내부에서 NOT_STARTED context를 얻은 뒤 coordinator 입구에서 대기한다.
3. 복구 요청 B가 같은 UUID를 제출해 실제 native coordinator가 같은 행을 QUEUED로 바꾼다.
4. worker를 실행하는 대신 소유 SQLite에 공식 RUN_START 이벤트를 기록하여 현재 상태가 STARTED임을 확인한다.
5. A를 해제하면 native coordinator가 오래된 context로 enqueue 이벤트를 기록하며 상태가 QUEUED로 회귀한다.

SDK .24와 .25 모두 before_late_submit=STARTED, after_late_submit=QUEUED, native_run_count=1을 직접 재현했다. worker/daemon/provider는 실행하지 않았다. 재dispatch 가능성을 만드는 상태 회귀이므로 현재 후보는 머지/배포 수용 전 수정이 필요하다. 단일 행 보존을 단일 실행 보장으로 확대할 수 없다. 수정 후 같은 반례와 프로세스 간 재개를 다시 검증해야 한다.

증거:
- /tmp/common41-review-c-7f11mf80/test_independent.py: test_stale_not_started_submission_must_not_regress_started
- fixture SHA256 d6f70613b70b9e8aeec96348c47684731499b15ae9c3816822df3e7706a9dc6e
- stale-1.13.24.safe.json 및 stale-1.13.25.safe.json은 모두 SHA256 85e00e5042c7bd2a59f7bf821f08e212c20d86f9e2a1153e0856dded114171b3
- stale-124.log SHA256 b8dce26cdf0d0afe4c08899f391589977f81ae7d36c35512c10066e6a7a8baee
- stale-125.log SHA256 d2059580442d86576b4b4c72d40cd357385c4cad77ee65768383e3927a6450d7

## 전체 소스 검토와 실제 실행 범위

AGENTS/CLAUDE/SKILL의 최소 정본과 문서 라우터를 읽고 6개 변경 파일 전체를 확인했다. 새 모듈 226줄과 원 집중 테스트를 모두 읽었다. 기본 Common import는 stdlib만 로드하며 SDK version 검증/서버 subclass 연결은 선택 진입점에 한정된다. native query/subscription/mutation은 상속·재사용한다. SDK 세 패키지의 동일 .24 또는 .25 조합만 허용한다.

lock 비교에서는 기존 package version/artifact 삭제·교체 없이 webserver extra 의존 18개만 추가되었다. workflow는 선택 extra를 테스트 환경에 포함한다. 소유 fixture의 RPC 경계만 in-memory RemoteJob/실행계획으로 대체했고 실제 native config 검증/create/SQLite unique/submit/이벤트 저장은 사용했다.

직접 실행한 결과는 각 버전마다 다음과 같다.

- immutable head의 기존 집중 테스트: 39 PASS.
- 본인 독립 테스트: 10 PASS.
- 본인 오래된 NOT_STARTED 상태 회귀 반례: 1 FAIL(제품 RED).

독립 통과 항목은 UUID 대소문자 정규화/비정규 UUID 거절, location/repository scope 분리, replay 권한 검사 후 저장소 접근, 변경 tags/config 충돌, 실제 instance.from_ref 재개, 동시 같은 UUID의 다른 config, 동시 NOT_STARTED의 단일 행, 늦은 첫 생성 후 동일 ID, 비유한 config 거절, 호출자가 제시한 runId로 결정적 ID를 덮어쓰지 못함, terminal replay 재제출 금지, 기존 query/mutation/subscription의 field·인자·기본값 보존이다.

원 테스트를 독립적으로 실행한 결과와 별도 작성한 반례 결과를 구분했다. 작성자 결과나 다른 리뷰어 원문/모형, root의 소비자/native 실측은 판정 근거로 합산하지 않았다.

## 재현 환경과 한계

readonly interpreter:
- /home/digitie/dev/common41-owned-sdk124-a-20261018/bin/python — SDK1.13.24/SQLAlchemy2.0.54
- /home/digitie/dev/common41-owned-sdk125-a-20261018/bin/python — SDK1.13.25/SQLAlchemy2.1.5

원 venv는 변경하지 않았고 immutable Git 모듈을 별도 scratch/src에 복사하여 로드했다. 환경은 소유 HOME/TMPDIR와 제한 PATH로 새로 구성했으며 원 저장소 conftest·환경을 사용하지 않았다. 명령은 python -I -B run_tests.py 및 pytest --noconftest -c /dev/null -p no:cacheprovider로 한정했다.

운영/SSH/컨테이너/외부 DB/provider/daemon/worker 실행, root 소유 포트 접속, 원본 source/index/branch 변경은 모두 0이다. 실제 webserver의 HTTP/auth proxy·소비자 UI·PostgreSQL 다중 호스트 수용은 이 리뷰가 검증하지 않았다. 이 제한은 본 리뷰 범위이며 root의 기존 실행 권한을 변경하지 않는다.

기계 증거: /home/digitie/dev/common41-independent-review-c-r1-20261018.safe.json
SHA256 b1161ffac33ad74f4102d218fa05e790143b23a1dccdf3e9aa9839aeab5c0bba.
