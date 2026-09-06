# T-005 versions.json v1 + `tools/check_versions.py`(npm lock v3·report·판정 어휘) + `docs/standards/versions.md` + 7 소비자 현재값·예외 등록

- 상태: IN_PROGRESS
- 우선순위: P0
- Gate: 도구 테스트·문서 검증
- 선행: 없음

## 목표

"라이브러리/플랫폼 버전 일치" 정책의 기계 판독 정본 `versions.json`과 대조 도구 `check_versions.py`(npm lock v3, report 모드)를 만들고 정책 문서 `versions.md`와 함께 배포한다. 이번 PR에서 스키마·도구·문서를 산출하며, 7 소비자 현재값·예외 등록은 잔여로 이 task 안에서 완료한다.

## 고정 결정

- [설계 브리프](../plan/design-brief.md) D-06(축별 floor/recommended/예외 표), D-07(핀 정책·판정 어휘 10종·모드 3단·`enforce`는 common 소유·`blocked[]`·`until` 필수), D-30, D-33(common 자체 툴체인 값).
- ADR-008 — [docs/adr/README.md](../adr/README.md).
- [버전 매트릭스](../survey/cross/version-matrix.md) §3.2(CI 런타임), §4.4(Node 22 동봉 npm 10.9.8), §5.1·§5.2(격차), §7.2 P3(계층별 하이브리드), §7.3(레지스트리 형식·strict 파서·`blocked`), §7.4(봇 없음 → 보고 단계 우선).
- 정정값([조사 안내](../survey/README.md) §6.2): Node 22 동봉 npm 10.9.8, common Python floor 3.11.
- 열림: O-8(pinvi mobile Tailwind 3 예외 — 승인 전 `exceptions`에 넣지 않음), O-6(airport TS 7.0.2 예외 `until`), O-10(npm 정책), O-18(Renovate 미설치 → `templates/dependabot.yml`은 T-007).

## 구현 범위

1. `versions.json`: `"schema": "kor-travel-common.version-registry.v1"`, `baseline: "2026-09"`, 축별 `{floor, recommended, max?}`(D-06 표 전 행: node·npm·next·react·typescript·tailwindcss·@tailwindcss/postcss·@base-ui/react·shadcn·eslint·typescript-eslint·vitest·@playwright/test·react-query·react-table·react-virtual·zod·zustand·react-hook-form·resolvers·maplibre-gl·python·python-image·uv·fastapi·starlette·uvicorn·pydantic·pydantic-settings·sqlalchemy·alembic·asyncpg·psycopg·httpx·tenacity·structlog·prometheus-client·typer·dagster·pytest·pytest-asyncio·ruff·mypy·import-linter·testcontainers·actions), `images`(digest), `blocked[]`(`mcp>=2`, concierge 2026-09-04), `providers`(보고만), `consumers.<repo>{enforce: "report", exceptions[]{key, installed, reason, until, review}}`. 미지 필드 거부.
2. `tools/check_versions.py`: 입력 `--repo <name> --lock <package-lock.json>`(v3 `packages` 트리에서 직접 의존성 설치본 추출) + `--engines <package.json>`; 판정 `OK/BELOW_FLOOR/ABOVE_MAX/NOT_RECOMMENDED/NO_LOCK/NO_ENGINES/FLOATING_REF/BLOCKED/EXEMPT/EXEMPT_EXPIRED`; 모드는 `consumers.<repo>.enforce`가 결정(`report` exit 0, `warn`, `fail` exit 1); `FLOATING_REF`·`BLOCKED`·`EXEMPT_EXPIRED`는 report에서도 `::error::` 주석; 출력 Markdown 표 + `--json` + `$GITHUB_STEP_SUMMARY`; `--self-check`(스키마·`until` 형식·만료 검사); stdlib만, Windows 동작. 매니페스트 `lockfiles[]` 입력은 T-011에서 연결.
3. `tests/test_check_versions.py`: fixture lock v3(직접·전이·git URL·workspace)로 10 판정 전부 + 모드별 exit code + strict 스키마 거부.
4. `docs/standards/versions.md`: 정책(계층별 하이브리드·lockfile 의무·판정 어휘·모드·승격 조건 "report 2회 연속 위반 0 → common PR"·예외 형식·`blocked` 운영) + D-06 표는 `versions.json`을 정본으로 두고 의미만 서술.
5. 잔여: 7 소비자 현재값(`vm` §1~§3, 인벤토리 §10)과 예외(map npm 12.0.1·next 16.2.12·Playwright 1.60, airport TS 7.0.2, ktc maplibre 6.0·base-ui 1.5, geo·ktdm React 18, map `starlette<1.0`·`alembic<1.20`)를 `consumers` 절에 등록하고 `check_versions --self-check`로 검증.

## 범위 밖

- `uv.lock`(T-005a)·`poetry.lock`/`requirements.txt`(T-005b) 파서, 매니페스트 스키마(T-011), 재사용 워크플로(T-010), `fail` 승격(T-502), 기준선 상향(T-507).
- 소비자 저장소 수정(T-403·T-413·T-433 등).

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다. `versions.json`, `tools/check_versions.py`, `tests/test_check_versions.py`, `tests/fixtures/versions/*.json`, `docs/standards/versions.md`, `tools/README.md`(행 추가).

## 수용 기준

- `versions.json`이 D-06 표의 모든 축을 갖고, 각 `exceptions[]` 항목에 `until`·`review`가 있으며, pinvi mobile Tailwind 3 예외는 없다(O-8 승인 전).
- `python3 -B -X utf8 tools/check_versions.py --self-check` exit 0; 미지 필드를 넣은 fixture는 exit 1.
- report 모드는 `BELOW_FLOOR`가 있어도 exit 0이고 `FLOATING_REF`(예: `git+…@main`)는 `::error::`를 출력한다. `fail` 모드는 exit 1.
- 테스트가 10 판정·3 모드·strict 스키마를 고정하고 Linux·Windows에서 같은 결과를 낸다(Windows 미실행이면 `NOT_RUN`).
- `versions.md`가 값을 복제하지 않고 `versions.json`을 정본으로 가리킨다. `docs.yml` 또는 T-009 `check-versions` job이 `--self-check`를 실행한다.
- 잔여 등록 완료 시: 7 소비자 report 실행 결과(위반 목록)가 evidence에 있다.

## 검증 명령

```bash
python3 -B -X utf8 tools/check_versions.py --self-check
python3 -B -X utf8 -m unittest discover -s tests -p "test_check_versions.py" -v
python3 -B -X utf8 tools/check_versions.py --repo map --lock tests/fixtures/versions/map.package-lock.json
python3 -B -X utf8 tools/validate_document_links.py
```

Git Bash에서 동일.

## evidence

- 명령·exit code·테스트 수·판정 표를 이 절과 `docs/journal.md`에 남긴다. 소비자 실제 lockfile 대조는 조사 기준 커밋을 명시한다.

## rollback 또는 release 차단 조건

- 도구·JSON·문서만 바뀌므로 `git revert` 1회로 원복한다.
- `--self-check` 실패, `until` 없는 예외, O-8 미승인 예외 등록은 merge 차단. `enforce`를 `fail`로 두는 변경은 T-502 절차 없이는 금지.
