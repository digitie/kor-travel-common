# Dagster health 조회·복구 격리 FULL 리뷰 manifest

- 실행 식별자: COMMON-GRPC-HEALTH-ISOLATION-20261016.
- 사용자 요청: 여러 소비자의 CPU·반복 실패 분석에 따른 무부작용 health 분리.
- 제품 고정 commit: 6ffc243cd590fa0bd09a819269dc18edecda4264.
- 통합 기준선: b76623266446a3c1e5729e5bc6876a2638af9a27 (Common32 2587915 + Common31 1bb5f6e).
  두 원 PR main merge는 하지 않았다. scheduling/http_health 원본 bytes와 ancestry를 검증했다.
- 이 manifest와 기록을 포함한 review HEAD는 reviewer에게 전체 SHA로 별도 전달한다.
- 범위: 아래 모든 delta와 이 manifest. 기존 public API/CLI·recovery 정책은 보존한다.
- 범위 밖: 소비자 코드/운영/Manager HC override 제거/새 supervisor/실제 job 장애 주입.
- 정본: AGENTS, docs/README, resume, T-319, agent-workflow, dagster-adoption §10/13/14,
  packages Python pyproject. 사전 private 설계 ccc55dab와 HC 분석64b49는 root 보관 근거다.
- reviewer A: deadline/실제 RPC/parser/response·memory/side-effect 공격.
- reviewer B: core-only·선택 dependency·CLI/legacy 호환/소비자 상태·운영 효과 주장 공격.
  같은 immutable HEAD에서 독립 FULL로 수행하고 상대 원문을 읽지 않는다.

| 파일 | SHA256 |
|---|---|
| CHANGELOG.md | f76b88d16431eb7defe3fdebb1b81a47915d545d2f310e7d8c8ee5d3d5dc6c22 |
| docs/journal.md | 3857cb2fe0462035b9df308c6bdeaab979f0ce7d2f165d099de834da9032e32f |
| docs/resume.md | 404f9d2b59d13fe4b20464d1aa571b866d5b7c77c51c7472a26b56b608b39ae7 |
| docs/reviews/adversarial/evidence/2026-10-16-grpc-health-local-measurements-final.json | 8158d51b9f2f4031418839e4d418601e9729b0a85083541db30c4cae05969c51 |
| docs/reviews/adversarial/evidence/2026-10-16-grpc-health-local-measurements.json | c9fc7d1962ac9f31f918ff851f49383e7df9fd43b323b9c5fef7327972498cd7 |
| docs/runbooks/dagster-adoption.md | 6208ff4d6979c596c54972f6e0f9c549b34de28d641e4dd995060e6b6f5a1909 |
| docs/tasks/T-319-dagster-recovery.md | fe4ab65e81f2a4870275fe9356ace0c268a3b62ec0b3d28196b9d051b283b3eb |
| packages/py/kor-travel-common/README.md | d9d23eb48abcaff4e512a1b441ec6d3e300dd61ac4f96fcaa5714a94ed61b782 |
| packages/py/kor-travel-common/pyproject.toml | 2ebed56822731b61af7756a58965668c6b90a2f60f7c62598edf95c12ed6e108 |
| packages/py/kor-travel-common/src/kortravelcommon/dagster_health.py | a0edc3dca6c78d2dce8a4bb22094aab6e9d5234384631b72b2902d574b253f1e |
| packages/py/kor-travel-common/src/kortravelcommon/grpc_health.py | 8ed9cf1f6d132b893b7c6c80ea69d2b3cd9ac130076ac1e011a25d7334a625df |
| packages/py/kor-travel-common/tests/test_grpc_health.py | a936f69c9b7e8130e1f7519ab6ed61d94a38e815f5eece8d9fe78f3fe889099d |
| packages/py/kor-travel-common/uv.lock | e405487f1f40f177a8ac88f87a7ceb102f4e23b355fb954bb7ec1cd109c97354 |

## 작성자 검증과 한계

- Python3.11/Dagster1.13.25 전체326PASS/102.90초, 신규48 포함. 별도1.13.24 신규48PASS.
- ruff PASS, wheel build/core-only·grpc-only 빈 venv 정상 설치/pipcheck/설치 source SHA 동일.
- 실제 loopback quiet CLI success/failure/timeout, missing dependency/distribution, unsupported
  version/metadata 및 malformed response·repository/pointer·shared budget 회귀를 수행했다.
- core extra 설치는 Dagster를 요구하지 않는다. 새 readiness만 지원 Dagster distribution의
  generated wire 파일을 사용한다. source module은 Dagster/SQLAlchemy/앱을 import하지 않는다.
- 최종 cold CLI 측정은 같은 디렉터리의 local-measurements-final.json을 따른다.
  이전측정 원문은 local-measurements.json으로 보존한다. 새 ready의 CPU/RSS 절감은 입증하지
  않았다. live는 더 약한 계약이며 차이를 동등 기능 절감률로 표현하지 않는다.
- 논리 budget 초과는 성공을 거절하지만 import/decode/close를 hard preempt하지 않는다.
  프로세스 timeout/주기/startup 여유는 소비자 동일 workload 실측 gate다.
- 문서 link707/2838 targets·plan109·unittest337(336PASS/1SKIP)·diff check PASS.
  첫 잘못된 discovery 경로와 jsonschema 미설치의3SKIP 결과는 최종 성공으로 덮지 않았다.
- 독립 두 제품 리뷰·CI·소비자 exact pin/이미지/HC 효과·운영 ARM64 CPU/RSS/DB/복구·live는
  NOT_RUN이다. 작성자 확인은 독립 review가 아니다.
- 최초 module 부재 RED, mock legacy 옵션 expectation 오류·measurement argv 오류를 수정한
  원문/후속 결과는 root private evidence에 보존했다. 실제 서비스 장애가 아니다.

## 재현

패키지에서 uv sync --locked --extra dev --extra dagster --extra grpc-health --python 3.11,
uv run --no-sync ruff check ., uv run --no-sync pytest -q, uv build를 실행한다.
원형 legacy 계약은 tests/test_dagster_health.py, 신규 실제 RPC/clock/CLI는
tests/test_grpc_health.py다. 문서 명령은 dev-environment §6을 따른다.
소비자/외부 HTTP/SSH/DB/Docker 호출은 하지 않는다.
