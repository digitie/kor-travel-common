# T-308 C5 errors/problem(`exclude_paths`)·C16 security_headers·C17 cors·C8 trusted_proxy·C11 testing·C10 alembic 템플릿·C15 http·C18 dagster

- 상태: BLOCKED
- 우선순위: P2
- Gate: 단위 테스트
- 선행: T-306, T-307

## 목표

D-15의 3차 모듈 8종을 넣는다. 모두 "계약 일부 변경 또는 정책 결정 동반"이라 opt-in이며 기본값은 기존 앱 동작을 바꾸지 않는다. 핵심은 C5 problem+json 핸들러(map·weather 형식, `exclude_paths`로 geo v1 등 예외 경로 제외, 자동 `HTTPValidationError` 제거 + `ProblemDetail` 주입)이고, 나머지는 얇은 원시 함수·미들웨어·템플릿이다. 범위가 넓으므로 [tasks-rule §2](../tasks-rule.md)의 하위 ID(`T-308a`~)로 분할해 진행할 수 있다(분할은 coordinator가 원장에 추가).

## 고정 결정

- [design-brief](../plan/design-brief.md) D-15(3차 C5·C16·C17·C8·C11·C10·C15·C18; C5 opt-in `exclude_paths`; C16 HSTS 전달 헤더 불신 기본; 보류 C6·C14·C19·C21은 제외), D-14(M3 RFC7807 `code`·`request_id`·`errors[]`, N1·N4 검증 오류 `input/ctx/url` 미노출, 422 기본·geo 400 예외, 429 `TOO_MANY_REQUESTS` 기본 O-14), D-06(httpx 0.27·tenacity 9·testcontainers 4.8·alembic 1.13·dagster 1.9 floor). ADR-009·ADR-011 — [ADR 색인](../adr/README.md). 규칙 정본: [openapi](../standards/openapi.md), [backend-stack](../standards/backend-stack.md), 예외 목록 [openapi-exceptions.yaml](../standards/openapi-exceptions.yaml).
- C5 원형: map `_error_response`/`_augment_problem_responses`, weather `Problem`·`_safe_errors`([oa §2.5·§5 C1](../survey/cross/openapi.md)). `type` 접두는 인자(map `https://kor-travel-map/errors/`, 기본 `about:blank`), 상태→코드 사전은 common 기본 + 앱 덮어쓰기.
- C16: nosniff/DENY/Referrer/Permissions/CSP/HSTS, HSTS는 실제 scheme https 또는 production일 때만이 기본(pinvi #344), `trust_forwarded_proto=True`는 kta용 옵션([be §2.9](../survey/cross/backend.md)). C17: `parse_origins_csv`(`*`와 credentials 동시 사용 제거). C8: peer CIDR + 비밀 상수시간 비교 + actor/roles 파싱, 헤더 이름 인자([be C8](../survey/cross/backend.md)).
- C11: testcontainers(map·pinvi) + 외부 DSN 가드(geo `_pg_guard`) 두 계열 모두 지원, 이미지 digest 핀 옵션, loop-scope 가이드([be §2.16](../survey/cross/backend.md)). C10: async `env.py` 골격(kta≈ktc≈pinvi)·NullPool·`%` 이스케이프·선택적 advisory lock — import 의존 없는 템플릿. C15: `AsyncClient` 팩토리 + tenacity 정책(geo 파라미터 3회·0.2→2.0s). C18: 3단 리소스 폴백(geo=map)·`run_failure_sensor` 통지 어댑터·`dagster.yaml` 템플릿.
- 도메인 결합 부분과 인증 서버·사용자 저장소는 넣지 않는다. 공용 인증 프리미티브는 T-312에서 별도로 다룬다([ADR-015](../adr/015-common-shared-systems-scope.md), [be §4](../survey/cross/backend.md)).

## 구현 범위

1. `kortravelcommon/api/problem.py`(`[api]`): `ProblemDetail`, `ProblemError(code, status, detail, hint=None)`, `register_problem_handlers(app, *, type_base="about:blank", code_by_status=None, exclude_paths=(), validation_status=422, include_validation_input=False)`, `augment_openapi_problem_responses(schema, *, drop_auto_422=True)`. `request_id`는 T-307 `current_request_id()`.
2. `kortravelcommon/api/security_headers.py`, `cors.py`, `trusted_proxy.py`(`[api]`).
3. `kortravelcommon/testing/`(`[testing]`): `postgres_container(image, digest=None)`, `external_dsn_guard(protected_names)`, `truncate_all(session, exclude)`, loop-scope 문서.
4. `templates/alembic/{env.py.tmpl,alembic.ini.tmpl,README.md}` + `alembic check` CI step 조각(T-305 ci-steps와 링크).
5. `kortravelcommon/http.py`(`[http]`): `make_async_client(timeouts: TimeoutProfile, event_hooks=None)`, `retry_policy(attempts=3, base=0.2, cap=2.0, retry_on=(...))`.
6. `kortravelcommon/dagster.py`(`[dagster]`): `build_definitions(required_keys, defaults, real_resources)`, `failure_notifier_sensor(notify)`, `templates/dagster/dagster.yaml.tmpl`.
7. 모듈별 테스트(각 ≥ 4). C5는 `exclude_paths` 아래 경로가 앱 핸들러로 떨어짐, 검증 오류 본문에 `input`·`ctx`·`url` 없음, OpenAPI에서 `HTTPValidationError` 제거·`ProblemDetail` 4xx/5xx/`default` 주입을 단언.

## 범위 밖

pagination 코덱·envelope `Meta/PageMeta`(C6 보류, T-508), geo_primitives·좌표 경계(C14 금지), cli.mutex(C19 보류), 백업 규약 문서(C21, `backend-stack.md` 절로만), structlog 로깅 설정 본체, 앱별 채택 PR(T-483 geo admin opt-in, T-482 airport additive, T-484~T-486), 헤더 AppId 통일.

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다.

```text
packages/py/kor-travel-common/src/kortravelcommon/api/{problem.py,security_headers.py,cors.py,trusted_proxy.py}
packages/py/kor-travel-common/src/kortravelcommon/testing/{__init__.py,postgres.py,guard.py}
packages/py/kor-travel-common/src/kortravelcommon/{http.py,dagster.py}
packages/py/kor-travel-common/tests/api/{test_problem.py,test_security_headers.py,test_cors.py,test_trusted_proxy.py}
packages/py/kor-travel-common/tests/{test_testing_fixtures.py,test_http.py,test_dagster.py}
templates/alembic/{env.py.tmpl,alembic.ini.tmpl,README.md}
templates/dagster/{dagster.yaml.tmpl,README.md}
packages/py/kor-travel-common/pyproject.toml          # [testing]·[http]·[dagster] 의존 확정
docs/standards/backend-stack.md                        # 모듈 표·백업 규약 절(standards-be 합의)
```

## 수용 기준

- [ ] `register_problem_handlers` 등록 후 `HTTPException(404)`·도메인 `ProblemError`·`RequestValidationError`·미처리 `Exception`이 모두 `application/problem+json`이며 본문에 `type,title,status,detail,code,request_id`가 있고 검증 오류 `errors[]`에 `input`·`ctx`·`url`이 없다.
- [ ] `exclude_paths=("/v1",)`일 때 `/v1/x` 오류는 앱 핸들러 응답(예: VWorld 형식)이 그대로 나온다.
- [ ] `augment_openapi_problem_responses` 적용 스키마에 `HTTPValidationError`가 없고 모든 operation의 4xx/5xx·`default`가 `ProblemDetail`을 참조한다; `validation_status=400` 옵션이 geo 예외를 재현한다.
- [ ] HSTS는 기본값에서 `X-Forwarded-Proto: https`만으로는 발급되지 않고 `trust_forwarded_proto=True`일 때만 발급된다; CSP 기본 `default-src 'none'`.
- [ ] `parse_origins_csv("a, *, b", credentials=True) == ["a","b"]`; `trusted_proxy` 비밀 비교가 `hmac.compare_digest`를 사용하고 CIDR 밖 peer는 거부.
- [ ] `[testing]` 픽스처가 testcontainers 모드와 외부 DSN 모드 양쪽에서 같은 테스트를 통과시킨다(Docker 없으면 컨테이너 모드 `NOT_RUN`).
- [ ] alembic 템플릿으로 생성한 최소 프로젝트에서 `alembic upgrade head && alembic check`가 통과한다(CI PostgreSQL).
- [ ] 각 모듈 테스트 ≥ 4, 전체 skip 0, `mypy --strict`·`ruff`·`lint-imports`(core가 `[api]`·`[db]`·`[http]`·`[dagster]`를 import하지 않음) 통과.

## 검증 명령

```bash
cd packages/py/kor-travel-common
uv sync --locked --all-extras && uv run pytest tests -q
uv run pytest tests/api/test_problem.py -q -k "exclude_paths or validation"
uv run mypy --strict src && uv run ruff check src tests && uv run lint-imports
python3 -B -X utf8 ../../../tools/validate_document_links.py
```

## evidence

이 파일 하단 "실행 기록"에 모듈별 테스트 수·컨테이너/DSN 모드 결과·alembic 템플릿 검증 결과·`python-package` run URL을 남긴다. 하위 ID로 분할했으면 각 하위 파일에 기록하고 여기에는 링크만 둔다.

## rollback·release 차단 조건

- 패키지 내부 모듈·템플릿이라 `git revert` 1회로 원복된다. 하위 분할 시 모듈 단위로 개별 revert 가능해야 한다(한 PR = 한 모듈군).
- C5가 기본값(opt-in 미호출)에서 앱 응답 형식을 바꾸거나, HSTS 기본이 전달 헤더를 신뢰하면 `py-v0.2.x`에 포함하지 않는다. pinvi `{error:{}}`·concierge/ktdm `{detail}`·geo v1을 바꾸는 코드는 이 task 범위가 아니며 발견 시 예외 레지스트리로 되돌린다.
