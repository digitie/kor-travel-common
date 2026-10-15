# Common33 gRPC health 격리 독립 FULL 제품 리뷰 B

판정: **PASS**. 열린 P0/P1/P2/P3 finding은 각각 0/0/0/0이다. 고정 Common 제품·패키징·문서 범위의 판정이며 소비자 이미지 채택이나 운영 건강/CPU 개선 승인이 아니다.

- 실행 ID: COMMON33-FULL-MANAGER-B-20261016.
- 관점: core/선택 의존성 패키징, 기존 public API·CLI 호환, 자원·부작용 경계, consumer guide.
- 격리: 자체 detached ext4 worktree /home/digitie/dev/kor-travel-common-review-manager-b-33-20261016. 생성 reflog 2026-10-16T05:44:35+09:00, 검증 증거 시작 2026-10-15T20:46:16.613131+00:00, 종료 2026-10-15T20:53:28.641346+00:00. 모든 명령은 WSL Ubuntu-26.04 Linux에서 실행했다.
- HEAD: 3ed16d1050bb55b87cc5005c11df3490d88205b6.
- 제품 commit: 6ffc243cd590fa0bd09a819269dc18edecda4264.
- baseline: b76623266446a3c1e5729e5bc6876a2638af9a27.
- manifest: docs/reviews/adversarial/evidence/2026-10-16-grpc-health-isolation-manifest.md, SHA256 fb4e92bed8633ebf1430cf9820217e2018704a5b51b5093410d5883dd4430ed4.
- 작성자 handoff: common33-health-isolation-handoff-c-20261016.md, SHA256 52fc8dbefe7c15747ff1a5b51bdbcd20bdf39fa454c943a116af6450fc8c7bf7. 작성자 근거를 독립 실행 결과로 합산하지 않았다.
- Common AGENTS/CLAUDE 포인터/SKILL 라우터, docs/README·resume·T-319·agent-workflow·dev-environment, dagster-adoption §10/13/14를 적용했다. CodeGraph 대신 수동 import/call/dependency 추적을 사용했다.
- peer raw: **NOT_READ**. 소비자·SSH·운영 HTTP·DB·SDK·Docker·서비스·운영 intent/freeze/attempt: **NOT_RUN/0**. RPC는 본인 ephemeral IPv4 loopback fixture만 사용했다.
- 제품 수정/다른 작업자 편집 변경 0. 설치/빌드/테스트 산출물은 자체 evidence/venv에 한정했다. 자체 worktree 진입/종료 status clean이다.

**FULL 범위**

baseline→HEAD 변경14파일 전체를 읽었다. manifest 자신과 아래13개 SHA 표를 직접 검증했다.

1. CHANGELOG.md
2. docs/journal.md
3. docs/resume.md
4. docs/reviews/adversarial/evidence/2026-10-16-grpc-health-isolation-manifest.md
5. docs/reviews/adversarial/evidence/2026-10-16-grpc-health-local-measurements-final.json
6. docs/reviews/adversarial/evidence/2026-10-16-grpc-health-local-measurements.json
7. docs/runbooks/dagster-adoption.md
8. docs/tasks/T-319-dagster-recovery.md
9. packages/py/kor-travel-common/README.md
10. packages/py/kor-travel-common/pyproject.toml
11. packages/py/kor-travel-common/src/kortravelcommon/dagster_health.py
12. packages/py/kor-travel-common/src/kortravelcommon/grpc_health.py
13. packages/py/kor-travel-common/tests/test_grpc_health.py
14. packages/py/kor-travel-common/uv.lock

기존 dagster_health.py의 파서와 호출/CLI 문맥, package __init__, legacy tests도 읽었다. Common31 1bb5f6e와 Common32 2587915는 모두 HEAD의 조상이며 scheduling.py와 http_health.py bytes는 baseline과 같다. main merge나 소비자 적용 확인은 아니다.

**패키징·호환·부작용 판단**

core METADATA에 무조건 설치되는 의존성은 없다. grpcio/health/protobuf는 grpc-health extra에만 추가됐고 기존 dagster/http/dev 계약은 보존됐다. wheel에 두 health 모듈과 LICENSE/NOTICE가 들어 있다. 선택 모듈 import는 grpc/Dagster/SQLAlchemy를 eager import하지 않는다. grpc-only 환경에서 live는 동작하고 ready는 Dagster distribution 부재를 성공으로 오인하지 않는다.

live는 표준 DagsterApi SERVING만 검사한다. ready는 같은 health 뒤 ListRepositories와 기대 repository/symbol/pointer 일치를 검사한다. live 성공은 정의/worker/DB 준비 성공이 아니다. 설치되지 않은 앱 module 이름이 담긴 정상 wire를 처리해도 앱을 import하지 않았다. 설치된 Dagster 생성 wire 파일을 직접 읽고 Dagster 본체/SQLAlchemy를 import하지 않았다.

기존 _is_loaded_reply의 public 효과를 유지하면서 공통 파서가 payload를 반환하도록 나눴다. legacy의 RPC별4초/기존 빈 symbol 허용/기존 CLI 인자·종료 계약과 새 API의 공유 논리 예산·기대 저장소 계약을 구분했다. legacy 회귀를 포함한113개가 지원 profile에서 통과했다. 새 모듈에는 DB, subprocess/reaper, os.kill, run writer, worker /proc 관측, supervisor가 없다. False 자체가 worker 사망이나 재시작 권한을 만들지 않는다.

새 budget 기본4초/범위(0,4], 각 RPC의 남은 예산 적용, 수신4MiB, retries0, decode/close 뒤 초과 성공 거절을 소스와 테스트로 확인했다. import/decode/close를 강제 선점하는 hard wall이 아님이 guide에 명시돼 있다. 실제 bootstrap/RSS/운영 Docker timeout 측정 없이4초 프로세스 보장으로 표현하지 않는다.

**본인 실행 — 결과를 서로 합산하지 않음**

- Python3.11.15의 offline wheel build PASS. wheel SHA256 8469a1d37c205cc64bcea46565b92bca4dff422e60457df961daec7d0556ff0a. wheel의 grpc_health/dagster_health/scheduling/http_health bytes가 HEAD와 같음을 확인했다.
- 빈 core-only, grpc-only venv에 offline wheel 설치 및 uv pip check PASS. 지원25와 별도24 테스트 환경 pip check도 PASS.
- Dagster1.13.25에서 pytest -q tests/test_dagster_health.py tests/test_grpc_health.py: **113PASS/3.10초**. grpcio1.84.0/health1.81.1/protobuf6.33.6으로 핵심 버전이 uv.lock과 같다.
- 별도 Dagster1.13.24에서 pytest -q tests/test_grpc_health.py: **48PASS/0.78초**. 25 결과에 합산하지 않는다.
- 설치 distribution24/25의 dagster/_grpc/__generated__/dagster_api_pb2.py SHA256이 모두 101c50a5a5b15fe33bd5e7a53f2843fafb5cbd774b8763e27dc18cd966b96fce로 같다.
- 설치 wheel 대상 별도 독립 fixture **35조건 PASS**: core/grpc-only dependency shape, lazy import, 잘못된 CLI 인자2·missing dependency1·성공0 모두 stdout/stderr 빈 값, live의 ListRepositories 생략, grpc-only ready 거절, expected repository 불일치, 손상 wire/NOT_SERVING/symbol 불일치/중복 repository/여분 pointer 거절, 단일 요청/no retry, Dagster·SQLAlchemy·앱 미수입. 자체 loopback 이외 endpoint를 사용하지 않았다.
- 변경 source2개와 신규 test에 ruff PASS. baseline→HEAD git diff --check PASS.
- 전체 Python326·문서 link/plan/unittest 전체 suite는 본인 NOT_RUN. 작성자 전체 결과를 본인 결과로 합산하지 않는다.

**실패 보존과 반례 disposition**

빈 venv에 broad [grpc-health,dagster,dev] extras를 lock 없이 offline 설치한 첫 시도는 Dagster1.13.26을 선택했다. 관련 suite **2FAIL/111PASS/3.35초**를 보존했다. test_real_ready_and_quiet_cli와 test_harmless_error_substring_is_not_a_structured_error가 ready False로 실패했다. 원로그 targeted-health.stdout.log SHA256 d9b095a284509ed10cc83af651387c74b3ee33c33148ce7b4302a40039d00020이다.

이 실패를 숨기거나 네트워크 문제로 재분류하지 않는다. 새 ready 지원 목록은 정확히1.13.24/25이고 guide도 미지원 버전 거절을 명시한다. 기존 dagster extra 범위를 줄이지 않고 소비자 exact pin/lock을 요구하는 설계와 정합한다. 지원25 pin 후113PASS와 별도24의48PASS로 경계를 확인했다. 현 범위의 P1/P2 finding으로 분류하지 않는다. broad extras 설치만으로 최신 Dagster readiness까지 보장하는 계약은 없으며 소비자 채택 gate에서 확인해야 한다.

**문서·운영 주장 검토**

§14는 조회 전용 선택 기능이며 Manager override 유지 중 Common 설치만으로 전환 완료로 세지 않는다. exact pin/lock→effective HC→복구 책임 분리→idle/active/지연/load error/UNKNOWN→리뷰/이미지/live 순서를 명시한다. §10 legacy proxy/child 준비 계약과 §13 예약 횟수/provider/freshness/동시성 경계도 유지됐다.

최종 measurement JSON의 source hash는 현재 소스와 같고 이전 측정 원문은 별도로 보존됐다. 문서는 x86 WSL/Python3.11 cold CLI 각3표본, interpreter/hook 포함 wall, VmHWM이지 PSS가 아님을 밝힌다. 기존 ready 대비 새 ready CPU/RSS 절감은 입증하지 않았고 약한 live와 동등 기능 절감률을 주장하지 않는다. 운영 ARM64/server CPU/DB/worker 복구/소비자 E2E는 NOT_RUN이다. 본인도 운영 효과를 추가 측정하거나 개선으로 확정하지 않았다.

**finding·한계·인계**

새 finding 없음. 열린 P1=0/P2=0, verdict **PASS**는 명시한 immutable FULL 소스와 로컬 패키징·호환 검증에 한정한다. 미지원 Dagster/다른 Python·OS/ARM64/소비자 실제 lock·image·effective HC·프로세스 timeout/active worker·DB·복구·실제 장애 주입·운영 성능은 미실행이다. 논리 deadline이 bootstrap을 hard preempt하지 않는 제한은 남는다.

증거 디렉터리 /home/digitie/dev/common33-review-manager-b-evidence-20261016, index SHA256 71aeea9541ee89dce8a1c0dd13021effee12964c47703bc4b5e3f73b77767d6d. 독립 fixture JSON SHA256 12a57622447184f38d90160881f89a790c79dde2ec5aee85f0ef2828168655b8, script SHA256 10928ee6f5a3b688374d92acd730fcce03b13dbc1d3dc1054153286912a77c42. 전부 본인 실행이다. worktree는 merge/abandon 전이므로 재검토용으로 유지한다. 모든 실행 도구/테스트 프로세스는 종료·회수했다.

별도 Transport81 ops r2 소유권 postfix 본인 검토는 아직 **NOT_RUN**이며 이 결과에 포함하지 않는다.
