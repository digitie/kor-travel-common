# T-484 pinvi: `uv.lock` CI·Docker 소비 + etl `@main` 제거 + export 파이프라인·drift CI + request-id(additive)

- 상태: BLOCKED
- 우선순위: P2
- Gate: api.yml·etl.yml
- 선행: T-310, T-420

## 목표

pinvi `apps/api`·`apps/etl`의 Python 축을 common 정책에 맞춘다: (1) 존재하지만 CI·Docker가 읽지 않는 `apps/api/uv.lock`을 실제 소비(`uv sync --locked`), (2) `apps/etl`의 `python-kasi-api @ git+…@main`을 sha 핀으로 + `uv.lock` 신설(`FLOATING_REF` 해소), (3) 없는 OpenAPI export 파이프라인을 common CLI로 신설하고 `openapi-drift.yml` 호출, `securitySchemes` additive, (4) 기존 RequestId 미들웨어를 common C2 형식 규칙(UUID/ULID, ≤128자, 검증 실패 시 서버 발급)에 맞춤(additive). pinvi `{error:{}}` envelope·`pinvi_api_` 접두는 예외 유지.

## 고정 결정

- [design-brief](../plan/design-brief.md) D-06(uv lockfile 의무 + CI·Docker `--locked`)·D-07(`FLOATING_REF`는 report에서도 `::error::`)·D-14(M1 export+`--check`는 pinvi Phase 3 파이프라인 신설; M4 X-Request-ID 즉시 MUST; M8; 예외 초기 등록 pinvi `{error:{}}`·정수 If-Match+409·비버저닝 경로; pinvi Zod 이중 유지는 OpenAPI↔Zod 일치 테스트 O-14)·D-15(메트릭 `pinvi_api_` 기한부 예외 review 2026-12)·D-16(pinvi Python 3차, L6 후)·D-24.
- ADR-009·ADR-011·ADR-010 — [ADR 색인](../adr/README.md). 정본: [openapi](../standards/openapi.md), `docs/standards/openapi-exceptions.yaml`, [backend-stack](../standards/backend-stack.md), [versions](../standards/versions.md).
- 사실: `apps/api/uv.lock` 384KB 존재, Docker `pip install -e .`·CI `pip install -e ".[dev]"`(README §6.2-18), hatchling, fastapi 0.141.1·pydantic 2.13.4 등 lock 값; `apps/etl` lockfile 없음 + `python-kasi-api@main`; 자체 스펙 export/drift 없음(대신 map 계약 스냅샷 byte-equality + staleness); RequestId(`X-Request-Id`)·SecurityHeaders·Prometheus·RateLimit 미들웨어; `{error:{code,message,details}}` 표준 코드 12종; `/v1` prefix 문서 불일치; api.yml(unit·integration 4-shard·provenance·contract-pin) — [inv/pinvi §4.1·§4.2·§6·§8-9~15·§9](../survey/inventory/pinvi.md), [oa §2.5·§2.11·§4](../survey/cross/openapi.md), [vm §2.1·§2.7](../survey/cross/version-matrix.md).
- PR 순서: [judge-migration-feasibility §3.1 pinvi #4](../plan/design-panel/judge-migration-feasibility.md).

## 구현 범위

- PR 1(lock 소비): `apps/api/Dockerfile` `uv sync --locked --no-dev`, `api.yml` `setup-uv` + `uv sync --locked --extra dev`(pytest-split 샤딩 유지), wheel provenance 검증 스크립트가 uv 환경을 읽도록 확인; `apps/etl/pyproject.toml` `python-kasi-api @ git+…@<sha>` + `apps/etl/uv.lock` 신설 + `etl.yml`·`Dockerfile` `--locked`.
- PR 2(export + drift): `apps/api`에 `kor-travel-common[api] @ git+…@py-v0.1.0#subdirectory=…` 추가, `scripts/export_openapi.py`(common CLI, 결정적 직렬화) + `apps/api/openapi.json` 커밋, `api.yml`에 `openapi-drift.yml`(common, `check` 모드) 호출 job 추가(required check 이름 보존), `securitySchemes`(JWT·admin 토큰) additive. OpenAPI↔Zod 일치 테스트는 `packages/schemas` vitest 1건으로 시작(O-14 기본값).
- PR 3(request-id): `app/middleware/request_id.py`를 `kortravelcommon.request_id`(`trust_incoming=True`, 형식 검증)로 교체 — 헤더 이름 `X-Request-ID` 대소문자 무관 유지, 응답 헤더·로그 contextvar 동작 계약 테스트로 무변경 확인; `openapi-exceptions.yaml` pinvi 항목 `review` 갱신.

## 범위 밖

envelope `{error:{}}` → problem+json 전환(예외 유지), 메트릭 접두 변경, map 계약 스냅샷 pin 체계(B10, 흡수 부적합), 인증(JWT·argon2·RBAC), 프론트.

## 대상 저장소·브랜치·PR·되돌리기

- pinvi 정본 체크아웃(Linux), 브랜치 `agent/<agent>-T-484-uv-locked` / `-openapi-export` / `-request-id`, `origin/main`에서 순차 분기. PR 3개(각 ≤10 파일 + lock/생성물).
- 되돌리기 = 각 PR `git revert` 1회, 역순. PR 1 revert 시 Docker가 다시 `pip -e`로 돌아가므로 이미지 재빌드 동반.

## 예상 변경 파일

아래는 이 task가 만들거나 고칠 예정 경로다. 예정 경로는 존재·실행 증거가 아니다.

```text
apps/api/Dockerfile, apps/api/pyproject.toml, apps/api/uv.lock
apps/etl/pyproject.toml, apps/etl/uv.lock, apps/etl/Dockerfile
.github/workflows/api.yml, etl.yml
apps/api/scripts/export_openapi.py, apps/api/openapi.json
apps/api/app/middleware/request_id.py, app/main.py
packages/schemas/src/*.test.ts                      # OpenAPI↔Zod 일치 1건
apps/api/kor-travel-common.lock.json, apps/etl/kor-travel-common.lock.json
```

## 수용 기준

- [ ] `api.yml`·`etl.yml`·`aggregate-ci` green(required check 이름 무변경); unit 91·integration 89 파일 수준 통과(수 기록), provenance·contract-pin·staleness job 유지.
- [ ] `docker build apps/api`·`apps/etl`이 `uv sync --locked`로 성공; `check_versions` pinvi api/etl 행에서 `FLOATING_REF` 0, `NO_LOCK` 0.
- [ ] `openapi-drift` job이 `--check` 모드로 green이고 `apps/api/openapi.json`이 커밋돼 있다; `securitySchemes` 추가 외 경로·스키마 제거 0.
- [ ] request-id 계약 테스트: 유효 수신 ID 반영, 비형식 ID는 서버 발급, 응답 헤더·로그 contextvar 존재; envelope `{error:{}}` 무변경.
- [ ] OpenAPI↔Zod 일치 테스트 1건 이상 실행(0 test 금지); `openapi-exceptions.yaml` pinvi 항목 갱신.

## 검증 명령

```bash
# pinvi (Linux)
cd apps/api && uv sync --locked --extra dev && uv run pytest tests/unit -q && uv run python scripts/export_openapi.py --check
cd ../etl && uv sync --locked && uv run python -c "import kasi"
docker build apps/api -t pinvi-api && docker build apps/etl -t pinvi-etl
npm run test -w packages/schemas
# kor-travel-common
python3 -B -X utf8 tools/check_versions.py --manifest ../pinvi/apps/api/kor-travel-common.lock.json
python3 -B -X utf8 tools/check_versions.py --manifest ../pinvi/apps/etl/kor-travel-common.lock.json
```

## evidence

PR 3개 본문(CI run·`--check` 출력·계약 테스트 수·`FLOATING_REF` 해소 report), `consumers.pins.json`·`docs/journal.md`, 이 파일 "실행 기록".

## rollback·release 차단 조건

- T-420(L6) 미머지면 PR 2·3(common 코드 소비)을 열지 않는다(B1); PR 1(lock 소비·sha 핀)은 common 코드 무관이라 L6 전에도 가능.
- required check 이름이 바뀌어 aggregate가 `Expected`에 갇히면 머지 금지; 머지 후 CI red면 해당 PR revert.
