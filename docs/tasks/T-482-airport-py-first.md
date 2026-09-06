# T-482 airport: py 1차 채택 + `code`/`request_id` additive + 스펙 422 정합 + `--check` CI + Docker `uv sync --locked` 정리

- 상태: BLOCKED
- 우선순위: P1
- Gate: backend CI
- 선행: T-310

## 목표

airport 백엔드(`backend/`, `main.py` 단일 파일 1,150행)가 py v0.1.0 1차 모듈(export CLI·health·time·quality)을 채택한다. RFC7807 problem 응답에 `code`·`request_id`를 additive로 추가(응답 본문 기존 필드 불변), 커밋된 `docs/openapi.json`(21 paths)과 코드의 422 불일치를 정합시키고, `scripts/export_openapi.py`에 `--check`를 부여해 CI drift gate를 만든다. Docker는 pip `-e`에서 `uv sync --locked`로 바꿔 CI와 같은 lock을 소비한다.

## 고정 결정

- [design-brief](../plan/design-brief.md) D-14(M3 `code`·`request_id`·`errors[]` 신규 MUST/기존 SHOULD + additive; M1 `--check`; M5 health 3경로; 422 기본; airport 스펙 422 불일치는 예외 레지스트리 초기 등록)·D-15(1차 모듈, C20 ruff 신규 도입)·D-16(Python 1차 3곳)·D-06(uv lockfile 의무, Docker `--locked`)·D-24.
- ADR-009·ADR-011 — [ADR 색인](../adr/README.md). 정본: [openapi](../standards/openapi.md), `docs/standards/openapi-exceptions.yaml`, [backend-stack](../standards/backend-stack.md).
- 사실: RFC7807 핸들러 2종(HTTPException + RequestValidationError, ADR-005), `/v1` prefix + `/health` 비버저닝, `docs/openapi.json` 21 paths·37 schemas(README §6.2-4 정정), tags 없음·operationId 자동, drift 검사 부재, CI `uv sync --extra dev --locked` vs Docker `pip install -e`, ruff/mypy 전무, alembic head 상수 검증 + `alembic check`, `/health.release_sha` 배포 대조 — [inv/kta §4.1·§8-10~16·§9](../survey/inventory/kor-travel-airport.md), [oa §2.5·§2.11·§4](../survey/cross/openapi.md), [be §2.1·§2.17·§2.18](../survey/cross/backend.md), [ci §2.2 kta](../survey/cross/ci-deploy.md).
- PR 순서: [judge-migration-feasibility §3.1 airport #4](../plan/design-panel/judge-migration-feasibility.md).

## 구현 범위

- `backend/pyproject.toml`: `kor-travel-common[api] @ git+…@py-v0.1.0#subdirectory=…`, `[tool.ruff]` common 베이스 `extend` + baseline(0에서 도입이므로 per-file-ignores 넓게), mypy는 `mypy-targets` 최소 모듈; `uv.lock` 갱신.
- problem 핸들러: `kortravelcommon.errors`(C5는 3차이므로 이 단계에서는 규칙만) 대신 기존 핸들러에 `code`(상태 매핑 사전)·`request_id`(C2는 2차 → 임시로 서버 발급 UUID v4, 형식 규칙 준수) 필드 추가. 기존 `type/title/status/detail` 불변.
- 스펙 422 정합: 코드가 422를 내는 경로에 스펙 응답을 추가(또는 반대), `docs/openapi.json` 재생성; 남는 불일치는 `openapi-exceptions.yaml` airport 항목 갱신.
- `scripts/export_openapi.py` → common CLI 래퍼(`--check`), CI backend job에 drift step; health 3경로 팩토리(`/health`는 기존 `release_sha` 필드 유지 — 확장 필드 허용 확인); time 헬퍼 대체.
- `backend/Dockerfile`(또는 `docker/`) `uv sync --locked --no-dev`로 전환.

## 범위 밖

`main.py` 라우터 분리 리팩터링(앱 소유 선행), 성공 envelope 도입(ADR-005 보류 유지), 인증(무인증 의도), metrics(미도입), 프론트.

## 대상 저장소·브랜치·PR·되돌리기

- `digitie/kor-travel-airport`, WSL2, 브랜치 `codex/T-482-py-v01`(Draft PR), `main`에서 분기. PR 1개(≤10 파일 + lock); 422 정합으로 스펙 diff가 크면 "스펙 정합" 선행 PR 분리.
- 되돌리기 = `git revert <merge-sha>` + `uv sync --locked`; Docker 이미지 재빌드. `deploy-server14.sh` 정확값 가드가 있으므로 배포 SHA 갱신 절차 동반.

## 예상 변경 파일

아래는 이 task가 만들거나 고칠 예정 경로다. 예정 경로는 존재·실행 증거가 아니다.

```text
backend/pyproject.toml, backend/uv.lock (또는 루트 uv.lock)
backend/app/main.py                      # 핸들러 additive, health 팩토리 배선
backend/app/core/time_utils.py           # common time 위임
scripts/export_openapi.py, docs/openapi.json
backend/Dockerfile 또는 docker/backend.Dockerfile
.github/workflows/ci.yml                 # drift step, ruff step
kor-travel-common.lock.json, docs/standards/openapi-exceptions.yaml(common)
```

## 수용 기준

- [ ] backend CI green: pytest(수 기록)·`alembic upgrade head && alembic check`·`export_openapi --check`·ruff(baseline) 통과.
- [ ] problem 응답 스냅샷 테스트: 기존 필드 값 불변 + `code`·`request_id` 존재, `request_id`가 UUID v4/v7 또는 ULID(≤128자 ASCII).
- [ ] `docs/openapi.json` paths 수(21 또는 정합 후 수치)와 422 응답 정의가 코드와 일치; 잔여 불일치는 `openapi-exceptions.yaml`에 `sunset|null`·`review` 포함 등록.
- [ ] `docker build`가 `uv sync --locked`로 성공하고 컨테이너 `/health`가 200 + `release_sha`를 반환.
- [ ] `check_versions` airport-backend 행 `kor-travel-common`·Python `OK`; live-e2e는 `NOT_RUN(운영 호출 job)`.

## 검증 명령

```bash
# kor-travel-airport (WSL2)
uv sync --extra dev --locked && uv run pytest -q && uv run ruff check backend
uv run alembic upgrade head && uv run alembic check
uv run python scripts/export_openapi.py --check
docker build -f backend/Dockerfile -t kta-backend . && docker run --rm -d -p 14002:8000 --name kta kta-backend && sleep 3 && curl -sSf http://127.0.0.1:14002/health ; docker stop kta
# kor-travel-common
python3 -B -X utf8 tools/check_versions.py --manifest ../kor-travel-airport/backend/kor-travel-common.lock.json
```

## evidence

PR 본문(CI run·스냅샷 테스트·`--check` 출력·Docker 기동 출력), `consumers.pins.json`·`docs/journal.md`, 이 파일 "실행 기록". T-310 정식 태그 "airport 검증" evidence로 링크.

## rollback·release 차단 조건

- problem 응답 기존 필드가 바뀌거나 `--check` red면 머지 금지; 머지 후 프론트 `ApiError` 파싱 회귀 시 revert.
- 포트 14002는 예외 등록(O-24) 상태를 전제로 하며, 포트 변경은 이 task 범위 밖.
