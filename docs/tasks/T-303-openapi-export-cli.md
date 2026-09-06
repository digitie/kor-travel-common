# T-303 C12 openapi export CLI(`--check`·profile 콜백·결정적 직렬화) + typegen 규약 템플릿

- 상태: BLOCKED
- 우선순위: P0
- Gate: 단위 테스트
- 선행: T-302

## 목표

kta·geo·map·ktw 네 저장소가 각각 갖고 있는 `export_openapi.py`(핵심은 모두 `app.openapi()` → `json.dumps(ensure_ascii=False, indent=2)`, [be §2.18](../survey/cross/backend.md))를 하나의 CLI `python -m kortravelcommon.openapi export`로 대체한다. `--check`(drift 시 exit 1 + diff), profile 콜백(map의 admin/user/service 가지치기를 앱 콜백으로 주입), 결정적 직렬화(`sort_keys`·`indent=2`·`ensure_ascii=False`·후행 개행·`servers` 제거)를 제공해 M1·M2·M9·N6·N7을 코드로 뒷받침한다. 함께 프론트 typegen 규약 템플릿(`openapi-typescript` 7.x, `gen:types`/`gen:types:check`)을 둔다.

## 고정 결정

- [design-brief](../plan/design-brief.md) D-14(M1 export+`--check`는 신규 MUST/기존 SHOULD, M2·M9·N6·N7 즉시 MUST, typegen 7.x 단일 버전, map 산출물 변경 시 pin 갱신 동반), D-15(C12 1차 우선순위, `[api]` extra). ADR-009·ADR-011 — [ADR 색인](../adr/README.md). 규칙 정본: [openapi](../standards/openapi.md)(T-301).
- 원형: geo `scripts/export_openapi.py`(`--check`, `sort_keys`), map `packages/kor-travel-map-api/scripts/export_openapi.py`(`--profile`, 미참조 schema 가지치기, user profile raw 필드 금지), weather·airport 단순 export([oa §2.11·§5 C7](../survey/cross/openapi.md)). map의 route policy 기반 profile 계산은 map 소유이며 콜백으로만 연결한다.
- 산출물 경로·파일명은 앱 소유(geo 루트 `openapi.json`, map 3종, weather `packages/.../openapi.json`, airport `docs/openapi.json`). CLI는 경로를 바꾸지 않는다.
- 근거: [oa §2.1](../survey/cross/openapi.md)(`servers` 7앱 모두 없음, map만 명문화), [oa §3.1 M9](../survey/cross/openapi.md)(production 표면; weather export는 `development` 프로필 강제 — 미확인 항목).

## 구현 범위

1. `kortravelcommon/openapi/export.py`: `render_spec(app, *, profile=None, transforms=()) -> str`(결정적 직렬화), `write_or_check(text, path, check: bool) -> int`(unified diff를 stderr에, exit 0/1), `load_app(target: str)`(`module:attr` 또는 `module:factory` 호출), `strip_servers(spec)` 기본 transform.
2. `kortravelcommon/openapi/__main__.py`: `export --app <module:attr> --output <path> [--check] [--profile <name>] [--transform <module:callable> ...] [--env KEY=VALUE ...]`. `--profile`은 등록된 콜백 `Callable[[dict, str], dict]`에 이름을 전달할 뿐 profile 의미는 앱이 정의한다. `--env`는 M9(production 자세) 계산용으로 앱 factory에 넘긴다.
3. 단위 테스트: 최소 FastAPI 앱 fixture로 (a) 두 번 실행 결과가 바이트 동일, (b) `servers` 제거, (c) `--check`가 변경 시 exit 1·무변경 시 0, (d) 키 순서·비ASCII 보존, (e) transform 순서 적용, (f) Windows 경로·`\n` 개행 고정(`.gitattributes` LF).
4. 기존 산출물 대조(가능한 범위): 조사 기준 커밋의 geo·weather·airport 커밋본을 fixture로 복사하지 않고, T-310에서 pinned checkout으로 대조한다. 이 task에서는 "동일 직렬화 규칙"을 코드 주석과 테스트에 명시한다.
5. `templates/typegen/README.md` + `package.json` 조각(`openapi-typescript` 7.x devDependency, `gen:types` → `src/api/types.ts`, `gen:types:check` = 임시 생성 후 `git diff --exit-code`), geo식 schema 이름 목록 export 옵션은 선택 절로만.
6. `docs/standards/openapi.md`의 M1·M9·typegen 절에 CLI 명령과 템플릿 링크를 추가(standards-be 소유자와 합의).

## 범위 밖

problem+json 응답 스키마 주입·자동 422 제거(T-308 C5), `openapi-drift.yml`·`typegen-drift.yml`(T-309), 각 앱의 스크립트 교체 PR(T-480~T-485), map profile 가지치기 로직 이전(map 소유 유지), `@kor-travel/openapi-typegen` npm 래퍼(D-01: 만들지 않음, 템플릿 조각으로 대체), pinvi Zod 일치 테스트 구현(O-14, T-484).

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다.

```text
packages/py/kor-travel-common/src/kortravelcommon/openapi/{__init__.py,__main__.py,export.py}
packages/py/kor-travel-common/tests/openapi/{conftest.py,test_export.py,test_check_mode.py}
templates/typegen/README.md
templates/typegen/package.scripts.json
docs/standards/openapi.md                     # M1·M9·typegen 절 링크(standards-be 합의)
```

## 수용 기준

- [ ] `uv run python -m kortravelcommon.openapi export --app tests.openapi.fixture_app:app --output /tmp/x.json`을 두 번 실행한 파일의 sha256이 같다.
- [ ] 출력 JSON에 `servers` 키가 없고, 키가 정렬돼 있으며, 한글 description이 `\u` 이스케이프 없이 보존되고, 파일이 `\n` 하나로 끝난다.
- [ ] `--check`는 산출물이 같으면 exit 0·다르면 exit 1과 unified diff를 출력하고 파일을 쓰지 않는다(파일 해시 불변 단언).
- [ ] `--profile user --transform tests.openapi.fixture_app:prune_user`로 콜백이 호출되고 결과에 반영된다(콜백 미등록 이름은 exit 2).
- [ ] pytest 테스트 수 ≥ 8, skip 0, 3.11·3.12·3.13 매트릭스 green(0 test를 pass로 집계 금지).
- [ ] `templates/typegen/README.md`가 `openapi-typescript` 7.x 정확 minor를 명시하고 `gen:types:check` 명령이 `git diff --exit-code`로 끝난다.
- [ ] `mypy --strict`·`ruff check`·`lint-imports`(`openapi` 서브패키지가 `[api]` 밖에서 fastapi를 import하지 않음 — `load_app`은 앱 모듈만 import) 통과.

## 검증 명령

```bash
cd packages/py/kor-travel-common
uv sync --locked --all-extras
uv run pytest tests/openapi -q
uv run python -m kortravelcommon.openapi export --app tests.openapi.fixture_app:app --output /tmp/a.json
uv run python -m kortravelcommon.openapi export --app tests.openapi.fixture_app:app --output /tmp/a.json --check; echo "exit=$?"
uv run mypy --strict src && uv run ruff check src tests && uv run lint-imports
```

## evidence

이 파일 하단 "실행 기록"에 pytest 수·exit code·두 번 실행 sha256·매트릭스 run URL을 남긴다. 실제 앱(geo·map·weather·airport) 대조는 T-310 evidence로 넘기며 여기서는 `NOT_RUN(소비자 체크아웃은 T-310)`으로 표기한다.

## rollback·release 차단 조건

- 패키지 내부 모듈이므로 `git revert` 1회로 원복된다. 소비자 스크립트 교체는 T-48x에서 각 앱 PR 단위로 되돌린다.
- 다음이면 `py-v0.1.0-rc`(T-310)에 포함하지 않는다: `--check`가 파일을 수정하는 경우, 직렬화가 플랫폼(Windows/Linux)에 따라 달라지는 경우, map 3 profile 콜백 경로가 검증되지 않은 경우.
