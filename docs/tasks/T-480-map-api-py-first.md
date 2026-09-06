# T-480 map-api: py 1차 채택(export CLI·health·time·quality) + `type` URI·429 코드 정렬 + pinvi/ktdm pin 갱신 PR 동반

- 상태: BLOCKED
- 우선순위: P1
- Gate: openapi.yml·pin 대조
- 선행: T-310

## 목표

`packages/kor-travel-map-api`가 `kor-travel-common` py v0.1.0(`kortravelcommon`)의 1차 모듈(C12 openapi export CLI·C4 health·C13 time·C20 quality)을 채택한다. map의 OpenAPI 산출물(`openapi.json` 3 profile, 161 paths, 1.45MB)은 pinvi·ktdm이 sha256으로 핀하므로 "산출물 무변경"이 기본 조건이며, `type` URI·429 코드(`TOO_MANY_REQUESTS`) 정렬로 산출물이 바뀌면 같은 PR에 pinvi·ktdm pin 갱신 요청 링크를 동반한다.

## 고정 결정

- [design-brief](../plan/design-brief.md) D-14(즉시 MUST M2·M4·M9·N6·N7; 429 코드 사전 common 기본 + 앱 덮어쓰기; map 산출물 변경은 pinvi·ktdm pin 갱신 PR 동반 없이 머지 금지; map `starlette<1.0` 예외는 이 task 재검증 전까지)·D-15(C12 `--check`·profile 콜백·결정적 직렬화, C4 기존 경로 alias 옵션, C20 ruff `extend`; 메트릭 접두 `kor_travel_map_` 기한부 예외)·D-16(Python 1차 = map-api·weather-api·airport)·D-24(py PR ≤10 파일).
- ADR-009·ADR-011 — [ADR 색인](../adr/README.md). 정본: [openapi](../standards/openapi.md), [backend-stack](../standards/backend-stack.md), `docs/standards/openapi-exceptions.yaml`.
- 사실: `scripts/export_openapi.py`(`--profile`·`--check`·working tree 비교·user 프로파일 필드 제거), `ProblemDetail{type,title,status,detail,code,request_id,errors[]}` + `{data, meta}` envelope, RoutePolicy, `_ERROR_CODE_BY_STATUS`, ruff select 11종(common 베이스 상위집합), mypy strict, import-linter 4 contracts(no fastapi/starlette in core), `starlette<1.0`·`alembic<1.20` 상한, Python lock 없음 — [inv/map §3.1·§4.2·§8-16~22·§9](../survey/inventory/kor-travel-map.md), [oa §2.11·§4](../survey/cross/openapi.md), [be §2.18·§3](../survey/cross/backend.md); pin 결박 — [cm §4.1 B10](../survey/commonality-matrix.md).
- PR 순서: [judge-migration-feasibility §3.1 map #4](../plan/design-panel/judge-migration-feasibility.md).

## 구현 범위

- `packages/kor-travel-map-api/pyproject.toml`: `kor-travel-common[api] @ git+https://github.com/digitie/kor-travel-common.git@py-v0.1.0#subdirectory=packages/py/kor-travel-common`(D-11), `[tool.ruff]` → common 베이스 `extend` + map 추가 규칙 유지, mypy 베이스 상속. Python lockfile 도입(`uv.lock`)은 이 PR에 동반(lock 의무)하되 범위 초과 시 선행 PR로 분리.
- `scripts/export_openapi.py` → `kortravelcommon.openapi.export` CLI 래퍼(3 profile 콜백 등록, 결정적 직렬화). 산출물 byte 동일 확인이 1차 목표.
- health: `/health`·`/readyz`·`/version` 팩토리로 교체(기존 경로가 다르면 alias 옵션으로 병행). time: `kortravelcommon.time` KST/UTC 헬퍼로 로컬 유틸 대체(의미 일치하는 것만).
- `type` URI·429 코드 정렬: `ProblemDetail.type`을 common 규칙 URI 형식으로, 429 `code`를 `TOO_MANY_REQUESTS`로 — 산출물이 바뀌면 (a) `openapi.json` 갱신, (b) pinvi `contract-pin`·ktdm `runtime-pins` 갱신 요청 이슈/PR 링크를 본문에 첨부, (c) 머지 순서 = map → pinvi/ktdm pin 갱신 같은 날.
- `import-linter` 계약 "core는 fastapi/starlette 미의존"이 `kortravelcommon` core(stdlib+pydantic만)와 정합함을 계약 실행으로 확인.
- `starlette<1.0` 상한: common `[api]`가 starlette 0.4x/1.6 매트릭스를 통과하므로 상한 제거 가능 여부를 이 PR에서 재검증(제거는 별도 커밋, 실패 시 예외 유지).

## 범위 밖

metrics 접두 변경(예외 유지, review 2026-12), envelope 형태 변경, RoutePolicy 흡수(앱 유지), Dagster 패키지, 프론트 typegen(산출물 무변경이면 불필요).

## 대상 저장소·브랜치·PR·되돌리기

- `digitie/kor-travel-map`, WSL, 브랜치 `agent/<agent>-T-480-py-v01`, `origin/main`에서 분기. PR 1개(≤10 파일 + lock); 산출물 변경 시 pinvi·ktdm 각 1 PR 동반(T-484·T-486 범위와 별개, pin 값만).
- 되돌리기 = `git revert <merge-sha>`; 산출물이 바뀐 경우 pinvi·ktdm pin도 함께 revert(순서 역순, 같은 날).

## 예상 변경 파일

아래는 이 task가 만들거나 고칠 예정 경로다. 예정 경로는 존재·실행 증거가 아니다.

```text
packages/kor-travel-map-api/pyproject.toml, uv.lock
packages/kor-travel-map-api/scripts/export_openapi.py
packages/kor-travel-map-api/src/kortravelmap/api/{app,response,health}.py
packages/kor-travel-map-api/openapi*.json                 # 변경 시에만
.github/workflows/openapi.yml, lint.yml
kor-travel-common.lock.json                               # python.version
pinvi: contracts/*.json·contract-pin / ktdm: config/runtime-pins.seed.json   # 산출물 변경 시 동반 PR
```

## 수용 기준

- [ ] `openapi.yml`(3 profile `--check`) green; 산출물 byte 동일이면 pin 대조 불필요, 변경이면 pinvi `contract-pin-consistency`·ktdm `pin verify`가 새 sha256으로 green인 동반 PR 링크가 있다.
- [ ] map `ci.yml`·`lint.yml` green(pytest 수 기록, coverage `fail_under` 80 유지, import-linter 4 contracts 통과).
- [ ] `/health`·`/readyz`·`/version` 응답이 openapi.md 계약과 일치(스냅샷 테스트), 기존 경로가 있으면 alias로 200.
- [ ] `check_versions` map-api 행 `NO_LOCK` → `OK`; `starlette` 상한 재검증 결과(제거/유지)가 `openapi-exceptions.yaml` 또는 `versions.json` 예외에 반영.
- [ ] `openapi-exceptions.yaml`에 map 관련 항목(`starlette<1.0`)이 갱신됐다.

## 검증 명령

```bash
# kor-travel-map (WSL)
uv sync --locked --extra dev && uv run python packages/kor-travel-map-api/scripts/export_openapi.py --profile admin --check
uv run pytest packages/kor-travel-map-api -q && uv run lint-imports && uv run ruff check . && uv run mypy
sha256sum packages/kor-travel-map-api/openapi*.json     # pin 대조용
# kor-travel-common
python3 -B -X utf8 tools/check_versions.py --manifest ../kor-travel-map/kor-travel-common.lock.json
```

## evidence

PR 본문(export `--check` 출력·산출물 sha256 전후·pytest 수·동반 PR 링크), `consumers.pins.json`·`docs/journal.md`, 이 파일 "실행 기록". T-310 정식 태그의 "map 검증" evidence로 링크.

## rollback·release 차단 조건

- 산출물 변경 + pin 갱신 PR 미동반 = 머지 금지(D-14). 머지 후 pinvi/ktdm CI red 발생 시 map PR revert.
- import-linter 계약 위반(core에 fastapi 유입)이면 `kortravelcommon` extra 구성을 고치는 common patch 없이 머지 금지.
