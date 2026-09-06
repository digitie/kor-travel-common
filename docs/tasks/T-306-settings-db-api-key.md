# T-306 C1 settings 베이스 + C9 db 엔진 팩토리 + C7 public_api_key

- 상태: BLOCKED
- 우선순위: P1
- Gate: 단위 테스트(testcontainers)
- 선행: T-304

## 목표

2차 모듈 세 개를 넣는다. (1) `BaseSettings` + `.env` + `extra="ignore"` 골격이 7개 중 6개에서 같다([be §2.2](../survey/cross/backend.md)) → settings 베이스 클래스. (2) "DSN 정규화 → `create_async_engine(pool, pre_ping, server_settings/options)` → `async_sessionmaker(expire_on_commit=False)`" 골격이 asyncpg 4곳에서 동일하고 psycopg는 `options` 인자만 다르다([be §2.6](../survey/cross/backend.md)) → db 엔진 팩토리. (3) `generate_public_api_key`/`hash_public_api_key`가 ktc·ktdm·geo·map 네 곳에서 본문까지 같다([be §2.8](../survey/cross/backend.md)) → public_api_key 함수군. env 이름·접두·저장 스키마는 앱 소유이며 절대 바꾸지 않는다.

## 고정 결정

- [design-brief](../plan/design-brief.md) D-15(2차 C1·C9·C7; core=stdlib+pydantic, db는 `[db]` extra, 인증 서비스는 범위 밖), D-06(pydantic 2.9·pydantic-settings 2.5·SQLAlchemy 2.0.35·asyncpg 0.29·psycopg 3.2 floor), D-14(N2 신규 표면 `?key=` 금지·legacy 예외), D-01(인증 서비스 비보유). ADR-011·ADR-001 — [ADR 색인](../adr/README.md). 규칙 정본: [backend-stack](../standards/backend-stack.md).
- settings: env 접두는 서브클래스가 지정(common은 접두를 정하지 않음), `SecretStr` 마스킹 + `hide_input_in_errors` + ValidationError input 재작성(pinvi), `get_settings/set_settings` 싱글턴은 geo 방식([be C1](../survey/cross/backend.md)). fail-closed 프로파일 검증은 훅만 제공.
- db: asyncpg `server_settings`와 psycopg `options`를 한 인자 집합으로 흡수, 세션 GUC 기본값(pinvi lock/idle/statement, geo statement/search_path)은 앱 인자; weather sync 엔진은 별도 함수 후보([be C9](../survey/cross/backend.md)). 엔진 메트릭 훅 지점만 두고 지표 정의는 T-307.
- public_api_key: 32자 `ascii_letters+digits` `secrets.choice`, `strip()` 후 무염 SHA-256, `key_hint = key[-6:]`, 상태 `active/revoked`; 저장소는 Protocol(ORM/raw SQL/SQLite는 앱 구현); 헤더 이름은 인자, query 파라미터 추출은 `allow_query_param=True`일 때만(N2).
- Gate가 testcontainers인 이유: map·pinvi 계열 픽스처로 실 PostgreSQL에서 팩토리를 검증한다([be §2.16](../survey/cross/backend.md)); Docker 없는 환경은 `NOT_RUN`.

## 구현 범위

1. `kortravelcommon/settings.py`(core): `BaseAppSettings(BaseSettings)` — `model_config = SettingsConfigDict(env_file=(".env",), extra="ignore", hide_input_in_errors=True)`, `redacted_validation_error` 헬퍼, `make_settings_accessor(cls) -> (get_settings, set_settings)`, `require_production_value(name)` 훅.
2. `kortravelcommon/db.py`(`[db]`): `normalize_dsn(dsn, *, driver="asyncpg"|"psycopg")`, `make_async_engine(dsn, *, pool_size, max_overflow, pool_timeout, pool_recycle, pool_pre_ping=True, statement_timeout_ms=None, search_path=None, extra_server_settings=None, json_serializer=None)`, `make_async_session_factory(engine)`, `make_get_db(session_factory)`, `on_engine_created` 훅(T-307 메트릭 연결점). `make_sync_engine`은 후보.
3. `kortravelcommon/auth/public_api_key.py`(core): `generate_public_api_key()`, `hash_public_api_key(key)`, `key_hint(key)`, `is_well_formed(key)`, `PublicApiKeyRecord`(dataclass), `PublicApiKeyStore` Protocol, `TtlCache`. `[api]`에 `extract_api_key(request, *, header_name, allow_query_param=False)` 의존성 팩토리.
4. 테스트: settings(접두 미지정·redaction·싱글턴), db(asyncpg·psycopg 양쪽에서 DSN 정규화·`SET`된 GUC 확인 — testcontainers `postgis/postgis:16-3.5` digest 핀), api_key(해시 벡터가 네 앱 구현과 동일 — 조사 문서의 알고리즘 기술로 고정, 실제 앱 코드 복사 없음).

## 범위 밖

비밀번호 해시·세션·CSRF·JWT·RBAC(D-01 범위 밖), `ops.public_api_keys` DDL·저장소 구현(앱 소유), 헤더 AppId 통일(D-22), request_id·metrics(T-307), trusted_proxy·testing 픽스처 배포(T-308), 앱 채택 PR(T-480~T-486), 좌표 경계 상수(공통화 금지).

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다.

```text
packages/py/kor-travel-common/src/kortravelcommon/settings.py
packages/py/kor-travel-common/src/kortravelcommon/db.py
packages/py/kor-travel-common/src/kortravelcommon/auth/{__init__.py,public_api_key.py}
packages/py/kor-travel-common/src/kortravelcommon/api/api_key.py
packages/py/kor-travel-common/tests/{test_settings.py,test_public_api_key.py}
packages/py/kor-travel-common/tests/db/{conftest.py,test_engine_factory.py}
packages/py/kor-travel-common/pyproject.toml            # [db] extra 의존 확정
docs/standards/backend-stack.md                          # 모듈 표 갱신(standards-be 합의)
```

## 수용 기준

- [ ] `BaseAppSettings`를 접두 없이 서브클래스하면 env 접두를 강제하지 않고, `SecretStr` 필드 검증 실패 메시지에 원문이 나타나지 않는다(정규식 단언).
- [ ] `normalize_dsn("postgres://u:p@h/db", driver="asyncpg")`가 `postgresql+asyncpg://…`, `driver="psycopg"`가 `postgresql+psycopg://…`를 만들고 이미 정규화된 DSN은 그대로 둔다.
- [ ] testcontainers PostgreSQL에서 asyncpg·psycopg 두 드라이버로 엔진을 만들어 `SHOW statement_timeout`·`SHOW search_path`가 인자값과 같다(Docker 없으면 `NOT_RUN`).
- [ ] `hash_public_api_key(" abc ") == sha256("abc")`, `generate_public_api_key()`가 32자 영숫자, `key_hint`가 마지막 6자.
- [ ] `extract_api_key`가 기본값에서 `?key=`를 무시하고 `allow_query_param=True`일 때만 읽는다.
- [ ] core 모듈(`settings`·`auth.public_api_key`)이 `[db]`·`[api]` 미설치 venv에서 import된다(`lint-imports` 계약 포함).
- [ ] pytest 테스트 수 ≥ 20, 통합 테스트는 skip이 아니라 명시적 `NOT_RUN` 마커로 집계, `mypy --strict`·`ruff` 통과.

## 검증 명령

```bash
cd packages/py/kor-travel-common
uv sync --locked --all-extras
uv run pytest tests/test_settings.py tests/test_public_api_key.py -q
uv run pytest tests/db -q -m "not requires_docker" ; docker info >/dev/null 2>&1 && uv run pytest tests/db -q
uv run mypy --strict src && uv run ruff check src tests && uv run lint-imports
```

## evidence

이 파일 하단 "실행 기록"에 테스트 수·드라이버별 결과·컨테이너 이미지 digest를 남긴다. Windows/Docker 부재 환경에서는 통합 테스트를 `NOT_RUN(Docker 없음)`으로 적고 CI(`python-package` job, Docker 사용 가능)의 run URL로 대체한다.

## rollback·release 차단 조건

- 패키지 내부 모듈이라 `git revert` 1회로 원복된다.
- 해시 벡터가 네 앱 구현과 하나라도 다르면(기존 키 무효화 위험) 릴리스 차단. settings 베이스가 env 접두를 기본값으로 넣거나 db 팩토리가 GUC 기본값을 강제하면 배포 `.env` 계약 위반이므로 `py-v0.1.x`에 포함하지 않는다.
