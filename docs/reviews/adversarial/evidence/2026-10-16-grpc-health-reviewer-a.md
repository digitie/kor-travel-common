# Common33 gRPC health 격리 독립 FULL 리뷰 A

- 실행 ID: COMMON33-GRPC-HEALTH-A-20261016.
- 전문 영역: 네트워크 경로/실제 RPC/파서/공유 deadline/실패 격리.
- 격리 checkout 생성 시각: 2026-10-15T20:44:01.069151+00:00. 완료: 2026-10-15T20:50:30.485064+00:00.
- review HEAD: `3ed16d1050bb55b87cc5005c11df3490d88205b6`.
- 제품: `6ffc243cd590fa0bd09a819269dc18edecda4264`.
- 기준선: `b76623266446a3c1e5729e5bc6876a2638af9a27`.
- manifest: `docs/reviews/adversarial/evidence/2026-10-16-grpc-health-isolation-manifest.md`, SHA256 `fb4e92bed8633ebf1430cf9820217e2018704a5b51b5093410d5883dd4430ed4`.
- 범위: manifest 포함 14개 전체 delta, 기존 parser와 public health/CLI 계약 및 관련 호출 경계.
- 격리 방식: 별도 detached worktree `/home/digitie/dev/common33-grpc-review-a-20261016`. 시작·종료 tracked 상태 clean, 도구 종료 후 worktree 제거 완료. 원 작성자 checkout 수정 없음.
- 다른 리뷰어 원문/결과 NOT_READ. 작성자 모형을 독립 결과에 합산하지 않았다.
- 판정: **CONDITIONAL / CHANGES_REQUESTED — P0 0, P1 0, P2 1 OPEN**.

## 전달 요청과 정본

요청은 Common33 고정 reviewHEAD의 FULL 독립 제품 리뷰이며 네트워크/파서/시간 예산/실패 격리를 소유한다. 기존 light dagster_health·legacy API 보존, 선택 grpc_health의 live HealthCheck 단일 조회와 ready ListRepositories, 공유 논리4초, 명시 wire profile1.13.24/.25, 자동 channel retry 차단, quiet CLI, core lazy dependency를 검토한다. health에 DB/Dagster import/kill/reaper를 넣지 않고 복구와 분리하는 가이드, 동등 ready의 CPU 절감 미입증 및 Python 시작을 포함하지 않는 논리 budget을 구분한다. 운영/SSH/실제 소비자 호출·수정은 금지이고, immutable 격리와 독립 부정 모형을 사용한다.

AGENTS → docs/README → resume → T-319 → agent-workflow와 manifest의 상세 범위를 읽었다. CodeGraph index는 생성하지 않았으며 rg·직접 parser/RPC/호출 경계·회귀로 대체했다.

## A-P2-01 — loopback 채널이 환경 proxy로 우회되어 다른 서버를 정상으로 판정할 수 있다

위치: `packages/py/kor-travel-common/src/kortravelcommon/grpc_health.py:52–57`.

새 채널은 loopback 주소를 구성하지만 C-core HTTP proxy 사용을 차단하지 않는다. 실제 gRPC는 `grpc_proxy` 환경을 사용해 proxy로 CONNECT한다. 이는 기대한 같은 호스트의 port를 직접 조회한다는 live/ready 계약과 맞지 않는다.

독립 실제 loopback 재현:

1. 합성 표준 DagsterApi SERVING 서버를 직접 조회하면 EXIT0이다. 별도 합성 HTTP proxy를 `grpc_proxy`로 설정하자 해당 proxy가 CONNECT를 받았고, 403을 반환하면 동일 정상 target이 EXIT1이 됐다. gRPC native stderr171B도 발생하여 quiet CLI가 깨진다. 비밀/원문 stderr는 보고서에 싣지 않는다.
2. 더 강한 반례로 **닫힌 target port**는 direct EXIT1이지만, proxy가 전혀 다른 합성 건강 서버로 터널하면 **EXIT0**을 반환했다. 대상 code-server가 살아 있다는 증거가 없는데 건강하다고 오인한다.
3. 제품 소스를 바꾸지 않고 subprocess에서 실제 channel factory에 `('grpc.enable_http_proxy', 0)` 옵션만 추가하는 모형은 닫힌 target EXIT1 / 실제 건강 target EXIT0, stdout/stderr0을 반환했다. 두 모형 모두 외부 접속 0이며 자기 loopback 서버만 사용했다.

영향: proxy가 설정된 소비자 환경에서 무관한 서버 응답을 해당 loopback code-server 상태로 오인하거나 정상 서버를 실패로 판정할 수 있다. proxy가 외부를 가리키면 의도하지 않은 외부 네트워크 경로도 생길 수 있다. 실제 소비자에 이 환경이 설정됐다고 주장하지 않는다.

권고: **새 모듈의 채널**에 HTTP proxy 비활성 옵션을 명시하고 grpc_proxy/https_proxy/http_proxy/no_proxy 경계의 실제 loopback 회귀를 추가한다. 기존 legacy API를 이 변경에 섞어 의미 변경하지 않는다. proxy 거절 및 잘못된 다른 서버 터널 모두에서 올바른 target 판정과 quiet 출력이 유지돼야 한다. root에게 즉시 보고했고 최소 수정이 수용됐으나 이 고정 HEAD에는 아직 반영되지 않았다.

재현 소스/결과:

- `common33-proxy-probe-a-20261016.py` / `.json`, 결과 SHA256 `94626c419d987e47b47c4a0a9a77341fe09bda3fbc8e7e13e4004e4f2a0a722e`.
- `common33-proxy-tunnel-a-20261016.py` / `.json`, 결과 SHA256 `e9e0e13847e46b029f483dec0fcb3795dd820bf51520f7bc6794b32a8861609f`.

## 나머지 공격 결과

추가 확정 P1/P2는 없다. 다음은 제한된 소스/로컬 결과이며 운영 승인이 아니다.

- lazy grpc/health import, optional readiness의 설치 distribution version gate, generated reply 로딩, unsupported 버전 fail-closed를 확인했다. 실제 로컬 Dagster1.13.25 server.py의 DagsterApi SERVING 등록과 generated ListRepositories 경로를 직접 읽었다. 본체 Dagster/SQLAlchemy/앱 import 없이 ready도 동작하는 것을 독립 확인했다.
- 기존 parser의 반환을 payload로 재사용하는 리팩터는 legacy `_is_loaded_reply`의 bool 의미를 보존한다. expected repository/symbol/pointer 및 전체 이름 집합, 중복/누락·추가 metadata·typed marker·손상 wire/JSON 등을 거절했다. 오류명 substring이 정상 이미지 문자열에 존재하는 경우와 structured error를 구분한다.
- 두 RPC는 남은 monotonic 예산을 각각 전달하고 optional import/decode/channel close 뒤 초과 성공을 거절한다. 이 구조는 hard process wall이나 interpreter 시작 시간 상한이 아니다. 문서가 그 한계를 명시하므로 4초보다 큰 측정 wall을 곧바로 계약 위반으로 보지 않았다.
- 4MiB 수신/입력 cap은 논리 응답 바이트 상한이며 Python 객체/RSS 상한을 의미하지 않는다. 같은 raw를 중복 JSON 파싱하지 않고 cap 초과와 손상 응답을 실패로 돌려준다. 운영 메모리 절감은 독립 측정하지 않았다.
- live는 HealthCheck 한 번만 수행하여 정의/worker/DB 준비를 보장하지 않는다. ready 역시 run 성공/worker 사망을 증명하지 않는다. API에는 run 변경/kill/reaper/앱 DB 동작이 없고 복구 정책은 소비자 경계에 남는다.
- CLI0/1/2와 core/optional 경계, 기존 API별4초와 새 공유4초의 차이, Python3.11 타입·정수/NaN/무한대 예산 거절을 확인했다. retry 비활성 옵션은 있으나 proxy 차단을 대신하지 않는다.
- pyproject/lock의 추가 extra 및 기존 scheduling/http_health 보존, README/task/resume/changelog/journal의 미실행 구분을 확인했다. 합성 cold 측정 두 파일 전체를 읽고 최종 source SHA와 표본·단위를 대조했다. ready CPU/RSS 절감은 입증하지 않았고 live는 다른 계약이라는 문구가 타당하다. 초기 다른 source의 측정은 원문 이력으로 분리돼 있다.

## 직접 실행한 검증

- 고정 manifest의 13개 제품/문서/측정 파일 SHA 및 manifest 자체 SHA, 실제 14파일 delta 범위 확인.
- 새 모듈/기존 parser의 저장소 테스트 **113 PASS / 2.98초**. 작성자326 결과와 합산하지 않는다.
- 자기 별도 부정 suite **33 PASS / 13.49초**, 실제 합성 loopback RPC. repo/pointer/metadata 변형, invalid/oversized wire, non-SERVING, 중복 JSON, File/Package pointer, decode 예산초과, ready import 격리를 포함한다. 113개와 중복되는 계약이 있으므로 합계 unique test 수를 주장하지 않는다.
- 자기 suite 초기 실행은 weather cwd의 autouse DB fixture에 잘못 연결돼 33 setup ERROR였다. psycopg import 부재에서 중단됐고 DB 연결/시험 본문 실행은 없었다. 이를 Common 결함이나 제품 통과로 집계하지 않았다. 이후 `--noconftest`로 격리하여 통과했다. 남은 asyncio_mode 미지원 warning1은 바깥 pytest config의 설정이며 제품 경고가 아니다. 초기 로그 및 수정 실행 로그 모두 보존했다.
- Python3.11.15, grpcio1.84.0, protobuf6.33.6, Dagster distribution1.13.25. 1.13.24 독립 재실행은 NOT_RUN이며 작성자 증거만 읽은 것으로 구분한다.

검증 연결 원문: `common33-review-verification-a-20261016.json`, SHA256 `cba493e4da253ea3484383926511687cb2c849b9514277b6ffd18ed282e8ed82`.

## 범위와 종료

실제 소비자/외부 HTTP/SSH/DB/Docker/운영 호출·변경 0, 제품 소스 수정 0. 테스트는 로컬 ephemeral loopback 서버와 자기 subprocess만 사용했고 모든 서버·스레드·실행 세션은 종료했다. 이 리뷰는 설치 wheel의 전체 재빌드나 운영 ARM64 CPU/RSS/DB/실패복구/live 검증을 대체하지 않는다. Common31/32 baseline은 feature 통합이며 main merge나 소비자 pin 완료라고 표시하지 않는다.

P2가 수정된 새 immutable 소스에 대한 독립 postfix 검토가 필요하다. 이 3ed16d1 원문을 새 소스의 승인으로 재사용하면 안 된다.
