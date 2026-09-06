# T-483 geo: py 2차(health alias 병행·securitySchemes+typegen 재생성·admin problem+json opt-in·request-id)

- 상태: BLOCKED
- 우선순위: P2
- Gate: openapi drift·gen:types
- 선행: T-308, T-440

## 목표

geo 백엔드(`kortravelgeo`)가 py 2차 모듈까지 채택한다: C4 health(`/health`·`/readyz`·`/version` + 기존 `/v1/healthz`·`/v1/readyz` alias 무기한 병행), M8 `securitySchemes` 선언(additive) + 프론트 `gen:types` 재생성, C5 problem+json을 admin 라우터에만 opt-in(`exclude_paths`로 v1 VWorld 호환·v2 envelope 제외), C2 request-id(`X-Request-ID` 발급·형식 검증; v2 `query_id`는 `request_id`와 병행). C12 export CLI·C20 quality도 이 단계에서 common 판으로 교체한다.

## 고정 결정

- [design-brief](../plan/design-brief.md) D-14(M5 geo `/v1/healthz` alias는 소비자 probe·Prometheus 갱신 확인 전까지 무기한; M8 securitySchemes; 예외 초기 등록 geo v1(VWorld 호환)·v2 envelope `query_id`↔`request_id`·400; typegen `openapi-typescript` 7.x·`gen:types:check`; O-14 geo v2 problem+json 시점 = ADR-060 묶음)·D-15(C5 opt-in `exclude_paths`, C2 `trust_incoming`, C4 alias 옵션; 메트릭 `ktg_` 신규 규칙 `kt<x>_` 정합)·D-16(Python 2차 = geo)·D-22.
- ADR-009·ADR-011 — [ADR 색인](../adr/README.md). 정본: [openapi](../standards/openapi.md), `docs/standards/openapi-exceptions.yaml`, [backend-stack](../standards/backend-stack.md).
- 사실: `/v1/healthz` `{status:"ok"}`, `/v1/readyz` `{status, ready, degraded, components}` + pool 포화 503; v2 envelope `{status, query_id, error{code,message,hint?,field?}}` 400 통일; v1 vworld 호환; `X-KTG-*` 헤더; `ktg_` 메트릭(dual-emission 없이 전환 이력); `scripts/export_openapi.py --check` + `openapi.yml`; `gen-types.mjs`/`check-sync.sh` → `types/api.gen.ts`·`lib/schemas.gen.ts`; import-linter layers `api > cli > client > loaders > infra > core > dto`; ruff `E F W I N UP B A C4 SIM TCH RUF ASYNC`·mypy strict — [inv/geo §4.1·§8-18~25·§9](../survey/inventory/kor-travel-geo.md), [oa §2.4·§2.5·§2.10·§4](../survey/cross/openapi.md), [be §2.5·§2.10](../survey/cross/backend.md).
- PR 순서: [judge-migration-feasibility §3.1 geo #5](../plan/design-panel/judge-migration-feasibility.md).

## 구현 범위

- PR 1(1차 모듈 + health): `pyproject.toml`에 `kor-travel-common[api] @ git+…@py-v0.2.x`(2차 모듈 포함 태그), `uv.lock` 갱신(T-440 전제); export CLI 래퍼; health 팩토리 + `alias=["/v1/healthz","/v1/readyz"]`; ruff `extend` + geo 추가 규칙 유지·per-file-ignores 보존; import-linter 계약에 `kortravelcommon` core 허용 확인.
- PR 2(securitySchemes + typegen): admin 라우터의 `X-KTG-Actor`·`X-KTG-Admin-Proxy-Secret`·API key를 `securitySchemes`로 선언(additive), `openapi.json` 재생성, `npm run gen:types` 재생성물 커밋, `check-sync.sh` green.
- PR 3(problem+json opt-in + request-id): `install_problem_handlers(app, exclude_paths=["/v1/…", "/v2/…"])`로 admin 경로만 RFC7807; request-id 미들웨어(`trust_incoming=True` 기본, 형식 검증 실패 시 서버 발급), v2 응답 `query_id`는 유지하고 `meta`/헤더에 `request_id` 병행; `openapi-exceptions.yaml` geo 항목(v1·v2·400) `review` 갱신.

## 범위 밖

v2 envelope → problem+json 전면 전환(ADR-060 묶음, O-14), `ktg_` 접두 변경(규칙 정합 확인만), Dagster distribution, `_pg_guard` 등 테스트 인프라(C11은 3차 후속), 프론트 UI(T-441·T-444).

## 대상 저장소·브랜치·PR·되돌리기

- `digitie/kor-travel-geo`, Linux/WSL, 브랜치 `agent/<agent>-T-483-py-a|b|c`, `origin/main`에서 순차 분기. PR 3개(각 ≤10 파일 + 생성물).
- 되돌리기 = 각 PR `git revert` 1회, 역순. PR 2 revert 시 `types/api.gen.ts`·`lib/schemas.gen.ts`도 함께 복원된다(생성물 커밋 동반 조건).

## 예상 변경 파일

아래는 이 task가 만들거나 고칠 예정 경로다. 예정 경로는 존재·실행 증거가 아니다.

```text
pyproject.toml, uv.lock
scripts/export_openapi.py, openapi.json
src/kortravelgeo/api/{app,routers/healthz,responses,security}.py
src/kortravelgeo/infra/request_id.py                 # common 위임
kor-travel-geo-ui/types/api.gen.ts, kor-travel-geo-ui/lib/schemas.gen.ts
.github/workflows/{ci,openapi}.yml
kor-travel-common.lock.json, docs/standards/openapi-exceptions.yaml(common)
```

## 수용 기준

- [ ] `openapi.yml`(`--check`) green, `kor-travel-geo-ui` `gen:types` + `check-sync.sh` green, unit 1,395 수준 통과(수 기록), import-linter 통과.
- [ ] `/v1/healthz`·`/v1/readyz` 응답이 기존 스냅샷과 byte 동일(alias), `/health`·`/readyz`·`/version`이 openapi.md 계약과 일치.
- [ ] `openapi.json` diff가 `securitySchemes`·`security` 추가와 health 3경로 추가뿐(경로·스키마 제거 0) — 스펙 diff 요약 첨부.
- [ ] admin 경로 오류가 `application/problem+json`(`code`·`request_id` 포함)이고 v1·v2 경로 오류 형식은 무변경(계약 테스트).
- [ ] `X-Request-ID` 헤더가 모든 응답에 있고 v2 `query_id`는 유지; `openapi-exceptions.yaml` geo 항목 `review` 갱신; `check_versions` geo Python 행 `OK`.

## 검증 명령

```bash
# kor-travel-geo (Linux/WSL)
uv sync --locked --extra api --extra loaders --extra dev
uv run python scripts/export_openapi.py --check && uv run pytest tests/unit -q && uv run lint-imports && uv run ruff check . && uv run mypy
cd kor-travel-geo-ui && npm run gen:types && bash scripts/check-sync.sh && git diff --exit-code -- types/api.gen.ts lib/schemas.gen.ts
# kor-travel-common
python3 -B -X utf8 tools/check_versions.py --manifest ../kor-travel-geo/kor-travel-common.lock.json
```

## evidence

PR 3개 본문(`--check`·typegen 출력·스펙 diff 요약·계약 테스트 수), `consumers.pins.json`·`docs/journal.md`, 이 파일 "실행 기록".

## rollback·release 차단 조건

- `/v1/healthz` alias 응답이 바뀌면 머지 금지(소비자 probe·Prometheus 갱신 확인 전, D-14). 생성물(`*.gen.ts`) 미동반 스펙 변경도 머지 금지.
- T-440(`uv.lock`) 미머지 상태에서는 PR 1을 열지 않는다.
