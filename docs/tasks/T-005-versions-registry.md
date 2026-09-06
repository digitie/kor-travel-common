# T-005 versions.json v1 + `tools/check_versions.py`(npm lock v3·report·판정 어휘) + `docs/standards/versions.md` + 7 소비자 현재값·예외 등록 (2026-09-07, PR #3)

- 상태: DONE
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

1. `versions.json`: `"schema": "kor-travel-common.version-registry.v1"`, `baseline: "2026-09"`, 축별 `{floor, recommended, max?}`(D-06 표 전 행: node·npm·next·react·typescript·tailwindcss·@tailwindcss/postcss·@base-ui/react·shadcn·eslint·typescript-eslint·vitest·@playwright/test·react-query·react-table·react-virtual·zod·zustand·react-hook-form·resolvers·maplibre-gl·python·python-image·uv·fastapi·starlette·uvicorn·pydantic·pydantic-settings·sqlalchemy·alembic·asyncpg·psycopg·httpx·tenacity·structlog·prometheus-client·typer·dagster·pytest·pytest-asyncio·ruff·mypy·import-linter·testcontainers·actions), `axes.*.image`(이미지 참조, digest 검사 범위 밖), `blocked[]`(`mcp>=2`, concierge 2026-09-04), `providers`(보고만), `consumers.<repo>{enforce: "report", clean_runs, aliases}`와 최상위 `exceptions[]{repo, key, installed, reason, until, review}`. 미지 필드 거부.
2. `tools/check_versions.py`: 입력 `<소비자-checkout> --repo <name>` 또는 `--manifest <kor-travel-common.lock.json>`(manifest와 v3 `packages` 트리에서 선언·설치본 추출); 판정 `OK/BELOW_FLOOR/ABOVE_MAX/NOT_RECOMMENDED/NO_LOCK/NO_ENGINES/FLOATING_REF/BLOCKED/EXEMPT/EXEMPT_EXPIRED`; 모드는 `consumers.<repo>.enforce`가 결정(`report` exit 0, `warn`, `fail` exit 1); `FLOATING_REF`·`BLOCKED`·`EXEMPT_EXPIRED`는 report에서도 `::error::` 주석; 출력 Markdown 표 + `--json` + `$GITHUB_STEP_SUMMARY`; `--self-check`(스키마·`until` 형식·만료 검사); stdlib만, Windows 동작. 매니페스트 입력의 정식 스키마 정합은 T-011에서 검증한다. 기존 positional 경로 입력을 유지하고 미구현 `--lock`·`--engines`를 실행 예시로 요구하지 않는다.
3. `tests/test_check_versions.py`: fixture lock v3(직접·전이·git URL·workspace)로 10 판정 전부 + 모드별 exit code + strict 스키마 거부.
4. `docs/standards/versions.md`: 정책(계층별 하이브리드·lockfile 의무·판정 어휘·모드·승격 조건 "report 2회 연속 위반 0 → common PR"·예외 형식·`blocked` 운영) + D-06 표는 `versions.json`을 정본으로 두고 의미만 서술.
5. 7개 소비자 고정 commit의 manifest/lock을 읽기 전용으로 대조하고 `docs/evidence/t005/`에 입력 digest·보고·예외 근거를 기록한다. 설치값을 registry에 복제하지 않는다. base-ui 하향과 pinvi mobile Tailwind 3은 승인 예외가 아니며, map alembic 상한은 현 floor와 충돌하지 않으므로 예외를 신설하지 않는다. 기존 map starlette 예외는 설치 lock 부재로 적용 여부 미검증임을 표시한다.

## 범위 밖

- `uv.lock`(T-005a)·`poetry.lock`/`requirements.txt`(T-005b) 파서, 매니페스트 스키마(T-011), 재사용 워크플로(T-010), `fail` 승격(T-502), 기준선 상향(T-507).
- 소비자 저장소 수정(T-403·T-413·T-433 등).

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다. `versions.json`, `tools/check_versions.py`, `tests/test_check_versions.py`, `tests/fixtures/versions/*.json`, `docs/standards/versions.md`, `tools/README.md`(행 추가).

## 수용 기준

- `versions.json`이 D-06 표의 모든 축을 갖고, 각 `exceptions[]` 항목에 `until`·`review`가 있으며, pinvi mobile Tailwind 3 예외는 없다(O-8 승인 전).
- `python3 -B -X utf8 tools/check_versions.py --self-check` exit 0; 미지 필드·잘못된 정책 값을 넣은 fixture는 입력 오류 exit 2.
- report 모드는 `BELOW_FLOOR`가 있어도 exit 0이고 `FLOATING_REF`(예: `git+…@main`)는 `::error::`를 출력한다. `fail` 모드는 exit 1.
- 테스트가 10 판정·3 모드·strict 스키마를 고정하고 Linux·Windows에서 같은 결과를 낸다(Windows 미실행이면 `NOT_RUN`).
- `versions.md`가 값을 복제하지 않고 `versions.json`을 정본으로 가리킨다. `docs.yml` 또는 T-009 `check-versions` job이 `--self-check`를 실행한다.
- 잔여 등록 완료 시: 7 소비자 report 실행 결과(위반 목록)가 evidence에 있다.

## 검증 명령

```bash
python3 -B -X utf8 tools/check_versions.py --self-check
python3 -B -X utf8 -m unittest discover -s tests -p "test_check_versions.py" -v
python3 -B -X utf8 tools/check_versions.py ../kor-travel-map --repo map --mode report
python3 -B -X utf8 tools/validate_document_links.py
```

Git Bash에서 동일.

## evidence

2026-09-07 완료: f050997에서 두 독립 reviewer의 수정 후 재검토를 마쳤다. 최종 판정·원본·잔여 한계는 [post-fix 리뷰](../reviews/adversarial/2026-09-07-t005-post-fix.md)에 있다. 9개 최초 finding을 모두 FIXED로 확인했으며 Windows·WSL 전체 115 tests 성공, 고정 입력 48파일·306판정 재현, [CI](https://github.com/digitie/kor-travel-common/actions/runs/34063775506) 성공이다. 소비자 정책 준수·제품 검증·릴리스 완료를 뜻하지 않는다.

2026-09-07 독립 리뷰: [A/B 최초 판정](../reviews/adversarial/2026-09-07-t005.md)은 BLOCK, 9개 ID를 모두 수용했다. 수정 회귀 8개에서 20 실패를 먼저 재현한 뒤 Windows·WSL Python 3.11에서 전체 115 tests 성공·skip 0을 확인했다. 같은 7개 입력 48파일·306행도 재실행해 원본과 동일했다([수정 digest](../evidence/t005/post-fix.json)). 수정 commit의 두 reviewer 재확인 전 DONE/merge하지 않는다.

2026-09-07 구현 후보: 새 회귀 시험 7개를 먼저 실행해 31 tests 중 24 subtest 실패를 재현했다. 중첩 정책 오타·숫자 역전·예외 중첩/만료·prerelease·optional/hoist·전이 설치·shrinkwrap 경계를 수정했다. 전체 Windows Python 3.14.3·WSL Python 3.14.4에서 각각 107 tests 성공·skip 0, SPDX 13개 오류 0이다. 문서 228개/1893 target·task 96개 오류 0. `.github/workflows/docs.yml`에 자체 검사를 연결했으며 CI·2인 리뷰는 commit 후 실제 결과를 기록한다. 제품·소비자 build/e2e는 NOT_RUN(소비자 저장소 실행)이다.

2026-09-07 정본 대조: 초안의 중첩 exceptions·현재값 registry 복제 지시는 versions 정책 §7 및 AGENTS §4·§6과 충돌해 정정했다. 수치 floor와 기존 승인 예외는 유지한다. 자세한 고정 입력 결과는 [실측 보고](../evidence/t005/README.md)로 연결한다.

2026-09-06 T-013 인계: 부분 구현은 인수했으나 7개 소비자 실제 report·예외·자체 검사 CI 연결이 미완료다. 다음 T-003 완료 뒤 이 task 하나를 이어서 실행한다.

2026-09-06 T-013 리뷰 정정: 미해석 설치 버전은 NO_LOCK, 비어 있는 검사 범위는 입력 오류(exit 2), 하한 없는 OR 범위는 NO_ENGINES, 정책 오타·잘못된 버전/예외/차단 항목은 입력 오류, URL의 query·무관 fragment는 고정 ref 증거로 인정하지 않는다. `--self-check`는 소비자 조회 없이 레지스트리 형식을 검사한다. 7곳 현재값·예외의 실제 대조와 T-009 자체 검사 job 연결은 여전히 잔여이며 자체 검사 통과만으로 이 task를 완료하지 않는다. uv/Poetry 초안도 후속 T-005a·T-005b의 실제 fixture 대조 전 확정하지 않는다.

- 명령·exit code·테스트 수·판정 표를 이 절과 `docs/journal.md`에 남긴다. 소비자 실제 lockfile 대조는 조사 기준 커밋을 명시한다.

## rollback 또는 release 차단 조건

- 도구·JSON·문서만 바뀌므로 `git revert` 1회로 원복한다.
- `--self-check` 실패, `until` 없는 예외, O-8 미승인 예외 등록은 merge 차단. `enforce`를 `fail`로 두는 변경은 T-502 절차 없이는 금지.
