# T-481 weather-api: py 1차 채택 + `--check` 전환 + airkorea 스냅샷 정본 결정(L15) + Python 3.11/3.12/3.13 정합

- 상태: BLOCKED
- 우선순위: P1
- Gate: ci.yml
- 선행: T-310

## 목표

`packages/kor-travel-weather-api`가 py v0.1.0 1차 모듈(export CLI·health·time·quality)을 채택하고, CI의 OpenAPI drift 검사를 `git diff` 방식에서 `--check`로 바꾼다. 부수 결정 2건: (1) `packages/python-airkorea-api` 스냅샷(50파일)과 GitHub `digitie/python-airkorea-api`의 정본 관계(L15) — common은 어느 쪽도 복제하지 않고 git sha 핀 전환을 권고, (2) Python 선언 3.11 / CI 3.12 / Docker 3.13-slim 3중 불일치를 `requires-python >=3.11` + CI 매트릭스 + 이미지 3.12-slim(3.13 허용)으로 정합.

## 고정 결정

- [design-brief](../plan/design-brief.md) D-06(Python common 3.11 호환, 앱 3.12 상향은 Phase 4 앱 결정 O-7; 이미지 3.11-slim floor·3.12-slim 권장·3.13 허용; provider SHA는 보고만 O-16)·D-14(M1 export+`--check`, M5 health, M9)·D-15(1차 모듈)·D-16(Python 1차 3곳)·D-23(`python-airkorea-api` 이중 경로는 T-505 문서)·D-24.
- ADR-009·ADR-011 — [ADR 색인](../adr/README.md). 정본: [openapi](../standards/openapi.md), [backend-stack](../standards/backend-stack.md), [licensing](../standards/licensing.md)(L15).
- 사실: `scripts/export_openapi.py` + CI "Check OpenAPI is exported"(`git diff` 모드), envelope `{data, meta{request_id, generated_at, duration_ms, page}}` + problem+json, `request_context` 미들웨어(`x-request-id`·`x-duration-ms`), metrics 614행 `ktw_`, ruff `E,F,I,UP,B,ASYNC,RET,SIM`·mypy strict(CI 미실행), `uv sync --locked`, 선언 3.11/CI 3.12/Docker 3.13, airkorea 스냅샷 자체 docs 규약 동봉 — [inv/weather §4.2·§4.4·§6·§8-11~17·§9](../survey/inventory/kor-travel-weather.md), [lic §3.7 L15](../survey/cross/licensing.md), [vm §2.7](../survey/cross/version-matrix.md).
- PR 순서: [judge-migration-feasibility §3.1 weather #8](../plan/design-panel/judge-migration-feasibility.md).

## 구현 범위

- PR 1(py 채택): `packages/kor-travel-weather-api/pyproject.toml`(또는 루트 workspace)에 `kor-travel-common[api] @ git+…@py-v0.1.0#subdirectory=…`, `uv.lock` 갱신; `scripts/export_openapi.py` → common CLI 래퍼; CI step을 `export_openapi --check`로; health 3경로 팩토리(기존 `/health` 유지); time 헬퍼 대체; ruff `extend` 베이스 + baseline; mypy step 추가(T-460에서 추가됐으면 확인).
- PR 2(정합): `requires-python >=3.11` 유지 + CI python 매트릭스 `3.11/3.12/3.13`(또는 3.12 단일 + 이미지 3.12-slim), `deploy/Dockerfile.*` 이미지 태그 정리. 3.12 floor 상향은 O-7 앱 결정으로 별도 기록.
- PR 3(L15 결정 문서 + 전환): weather `docs/decisions.md`(또는 ADR)에 "airkorea 정본 = GitHub 저장소, 스냅샷은 제거 예정" 결정; 결정이 나면 `pyproject`를 `python-airkorea-api @ git+…@<sha>`로 바꾸고 `packages/python-airkorea-api` 삭제(별도 PR, 테스트 green 조건). 결정이 반대(스냅샷 정본)면 스냅샷에 라이선스·출처 고지만 보강하고 common `versions.json` `providers` 절에 보고.

## 범위 밖

metrics 모듈 공통화(C3는 2차), envelope 변경, Dagster 패키지, 프론트(T-460~464), `python-kma-api` SHA 정렬(T-505 요청).

## 대상 저장소·브랜치·PR·되돌리기

- `digitie/kor-travel-weather`, 브랜치 `feat/T-481-py-v01` / `feat/T-481-python-versions` / `chore/T-481-airkorea-l15`, `origin/main`에서 순차 분기, Draft PR. PR 3개(각 ≤10 파일 + lock).
- 되돌리기 = 각 PR `git revert` 1회. PR 3(스냅샷 삭제)은 revert로 50파일이 복원되므로 단독 커밋으로 둔다.

## 예상 변경 파일

아래는 이 task가 만들거나 고칠 예정 경로다. 예정 경로는 존재·실행 증거가 아니다.

```text
pyproject.toml, uv.lock, packages/kor-travel-weather-api/pyproject.toml
packages/kor-travel-weather-api/scripts/export_openapi.py
packages/kor-travel-weather-api/src/kortravelweather_api/{app,response,health}.py
.github/workflows/ci.yml
deploy/Dockerfile.api (+ dagster)                      # 이미지 태그
docs/decisions.md 또는 docs/adr/*                       # L15 결정
packages/python-airkorea-api/**                        # 삭제(결정 시, 별도 PR)
kor-travel-common.lock.json
```

## 수용 기준

- [ ] `ci.yml` green: `export_openapi --check` step이 산출물 무변경(또는 갱신 커밋 동반)으로 통과, pytest(수 기록)·ruff·mypy 통과, alembic upgrade head 유지.
- [ ] `/health`·`/readyz`·`/version` 계약 스냅샷 테스트 통과; `x-request-id` 헤더 동작 무변경.
- [ ] Python 버전: `pyproject` `requires-python`, CI 매트릭스, Docker 이미지가 정합 표(PR 본문)와 일치하고 `check_versions` weather Python 행 `OK`.
- [ ] L15 결정 문서가 있고, 전환했다면 `python-airkorea-api` 참조가 git sha 핀(`FLOATING_REF` 0)이며 스냅샷 디렉터리 0파일; `versions.json` `providers` 절 보고 갱신.
- [ ] `check_versions` weather-api 행에 `kor-travel-common` `OK`.

## 검증 명령

```bash
# kor-travel-weather
uv sync --locked --extra dev --extra dagster
uv run python packages/kor-travel-weather-api/scripts/export_openapi.py --check
uv run pytest -q && uv run ruff check . && uv run mypy src packages
grep -n 'python-airkorea-api' pyproject.toml packages/*/pyproject.toml
# kor-travel-common
python3 -B -X utf8 tools/check_versions.py --manifest ../kor-travel-weather/kor-travel-common.lock.json
```

## evidence

PR 3개 본문(CI run·`--check` 출력·정합 표·L15 결정 링크), `consumers.pins.json`·`docs/journal.md`, 이 파일 "실행 기록". T-310 정식 태그 "weather 검증" evidence로 링크.

## rollback·release 차단 조건

- `--check` 실패 상태 머지 금지; health 경로 응답 형태가 바뀌면(기존 `/health` 소비자 probe) alias 없이는 머지 금지.
- 스냅샷 삭제 PR은 pytest green + 운영 이미지 빌드 성공 없이는 머지 금지.
