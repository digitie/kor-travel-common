# T-485 concierge: py 1차(export·request-id·quality) + features export 계약 문서화(map provider 동시 수정 계획)

- 상태: BLOCKED
- 우선순위: P2
- Gate: CI
- 선행: T-451, T-311
- 외부 선행: ktc 루트 GPL-3.0-or-later 정렬(L8, O-2; T-021 결과) — 브리프 선행 열에는 없으나 D-16이 L8 전 코드 소비를 금지하므로 common 모듈 import 단계는 L8 후에만

## 목표

concierge 백엔드(`ktc`)가 py 1차 모듈 중 export CLI·request-id·quality를 채택한다(health는 `/health` healthcheck가 있으므로 `/readyz`·`/version` additive 추가). OpenAPI export/drift가 없던 저장소에 `openapi.json` 커밋 + `openapi-drift.yml` 호출을 신설하고, `/api/v1` prefix·`{detail}` 오류 형식은 예외 등록으로 유지한다. concierge의 features export는 map provider(`kor-travel-map` 측 concierge provider)가 소비하는 외부 계약이므로 이 task에서는 계약을 문서화하고 "map provider 동시 수정 계획"만 세운다(변경은 하지 않는다).

## 고정 결정

- [design-brief](../plan/design-brief.md) D-14(M1 export+`--check`는 ktc Phase 3 신설; M4 X-Request-ID 즉시 MUST; 예외 초기 등록 concierge `/api/v1`·`{detail}`·features export(map provider 외부 계약))·D-15(C12·C2·C20; 메트릭 `<app>_` 규칙 신규 `kt<x>_`는 신규 서비스만 — ktc 기존 접두는 예외 검토)·D-16(ktc Python 3차, L8 후)·D-24.
- ADR-009·ADR-011·ADR-004 — [ADR 색인](../adr/README.md). 정본: [openapi](../standards/openapi.md), `docs/standards/openapi-exceptions.yaml`, [backend-stack](../standards/backend-stack.md), [licensing](../standards/licensing.md).
- 사실: export/저장/drift 없음, tags/operationId 없음, 계약은 md 문서 4종이 정본, `routes.py` 3,759줄 단일 라우터, `X-API-Key` + `X-KTC-Actor`/`X-KTC-Admin-Proxy-Secret` + deny-by-default, `{detail}` 오류, Prometheus `<app>_` + `ProcessCollector(namespace)` + HTTP 미들웨어, `/health` healthcheck, MCP 서버(`FastMCP`), 목록 envelope + watermark cursor(ADR-37) — [inv/ktc §4.1·§8-8~11·§9](../survey/inventory/kor-travel-concierge.md), [oa §2.1·§2.5·§2.11·§4](../survey/cross/openapi.md); map provider 결합 — [inv/map §7](../survey/inventory/kor-travel-map.md).
- PR 순서: [judge-migration-feasibility §3.1 concierge #6](../plan/design-panel/judge-migration-feasibility.md).

## 구현 범위

- PR 1(export + drift, L8 후): `pyproject.toml`에 `kor-travel-common[api] @ git+…@py-v0.2.0#subdirectory=…`, `uv.lock` 갱신(T-450 전제); `scripts/export_openapi.py`(common CLI) + `backend/openapi.json` 커밋; `ci.yml`에 `openapi-drift.yml` 호출 job; tags·operationId는 부여하지 않음(S 계층, 후속) — 대신 `openapi-exceptions.yaml` concierge 항목(`/api/v1`·`{detail}`·features export) `review` 갱신.
- PR 2(request-id + health additive): `X-Request-ID` 미들웨어(`kortravelcommon.request_id`, `trust_incoming=True`) 추가 — 응답 헤더·로그 contextvar만 추가, 오류 본문 `{detail}` 불변; `/readyz`·`/version` 추가(`/health` 유지). ruff/mypy는 T-450에서 common 베이스를 이미 `extend`했으므로 baseline 축소만.
- 문서(concierge `docs/features-export-contract.md` 신규 또는 기존 계약 md 갱신): features export 응답 필드·버전·소비자(map provider 경로·핀 방식)·변경 절차("concierge PR + map provider PR 같은 날, 소비자 스냅샷 갱신 후 머지")를 적고 common `openapi-exceptions.yaml` 항목에서 링크. provider-policy.md C-6(원본 vs 파생 필드 경계) 결정과의 동기화 요구를 기록.

## 범위 밖

features export 응답 변경·map provider 수정(계획만), `{detail}` → problem+json 전환, `/api/v1` prefix 변경, MCP 서버 규약, 인증(X-API-Key·세션), 라우터 분리 리팩터링.

## 대상 저장소·브랜치·PR·되돌리기

- `digitie/kor-travel-concierge`, Linux/WSL2, 브랜치 `agent/<agent>-T-485-openapi-export` / `-request-id`, `origin/main`에서 순차 분기. PR 2개(각 ≤10 파일) + 문서 커밋(PR 1에 포함 가능).
- 되돌리기 = 각 PR `git revert` 1회. `openapi.json`·drift job 삭제도 revert에 포함.

## 예상 변경 파일

아래는 이 task가 만들거나 고칠 예정 경로다. 예정 경로는 존재·실행 증거가 아니다.

```text
pyproject.toml, uv.lock
scripts/export_openapi.py, backend/openapi.json
backend/main.py                         # request-id 미들웨어, /readyz·/version
.github/workflows/ci.yml                # openapi-drift job
docs/features-export-contract.md (또는 기존 계약 md)
kor-travel-common.lock.json, docs/standards/openapi-exceptions.yaml(common)
```

## 수용 기준

- [ ] CI(`python-quality`·`openapi-drift`) green; pytest 수 기록; `backend/openapi.json`이 커밋돼 있고 `--check`가 working tree와 일치.
- [ ] 모든 응답에 `X-Request-ID` 헤더가 있고 `{detail}` 오류 본문 byte 무변경(계약 테스트); 로그에 request_id contextvar 포함.
- [ ] `/health` 응답 무변경(healthcheck 유지), `/readyz`·`/version`이 openapi.md 계약과 일치.
- [ ] features export 계약 문서가 존재하고 map provider 파일 경로·핀 방식·동시 수정 절차가 적혀 있으며 common `openapi-exceptions.yaml` 항목이 그 문서를 가리킨다.
- [ ] L8 evidence(T-021 결과) PR 본문 기재; `check_versions` ktc Python 행 `OK`.

## 검증 명령

```bash
# kor-travel-concierge (Linux/WSL2)
uv sync --locked --all-extras && uv run python scripts/export_openapi.py --check
uv run pytest -q && uv run ruff check . && uv run mypy backend/ktc
curl -sSI http://127.0.0.1:12601/health | grep -i x-request-id     # 로컬 compose 기동 시
# kor-travel-common
python3 -B -X utf8 tools/check_versions.py --manifest ../kor-travel-concierge/kor-travel-common.lock.json
python3 -B -X utf8 tools/validate_document_links.py
```

## evidence

PR 2개 본문(CI run·`--check` 출력·계약 테스트·L8 링크), 계약 문서 링크, `consumers.pins.json`·`docs/journal.md`, 이 파일 "실행 기록".

## rollback·release 차단 조건

- L8(T-021) 미완이면 common 모듈 import PR을 열지 않는다(B9). features export 응답을 바꾸는 변경이 이 task에 섞이면 머지 금지(map provider 동시 PR 필요).
- drift job red 상태 머지 금지; 머지 후 map provider 소비 실패 보고 시 concierge PR revert.
