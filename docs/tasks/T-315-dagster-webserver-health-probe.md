# T-315 Dagster webserver 정의 로드 probe CLI

- 상태: READY
- 우선순위: P2
- Gate: Python 단위·wheel 설치·2인 리뷰
- 선행: 없음
- 소유 저장소: kor-travel-common
- 병렬: 묶음 D(언제든)

출처는 [공통화 재조사·계획(2026-11-17)](../plan/commonization-plan-2026-11-17.md)의 §3.4·§4.9(K-43)이다. 근거 위치(file:line)와 차이 분석은 그 문서가 정본이며 여기서 반복하지 않는다.

## 목표

GraphQL `{repositoriesOrError{__typename}}`의 `RepositoryConnection`을 보는 한 줄 probe가 compose·Dockerfile 7곳에 따로 있다. 공통 CLI 하나를 만든다.

## 고정 결정

- stdlib만 쓴다. core-only 설치에서 동작하고 Dagster를 import하지 않는다(`http_health`와 같은 방침, [http-health-probe](../runbooks/http-health-probe.md)).
- probe는 조회만 한다. 프로세스를 죽이거나 run을 거두지 않는다.
- Manager의 공용 webserver probe(rendered workspace를 읽음)는 대상이 아니다.

## 구현 범위

1. `python -I -m kortravelcommon.dagster_webserver_health --port <포트> [--timeout-seconds 4]`.
2. loopback POST `/graphql`, redirect·재시도 없음, 응답 크기 상한, `__typename == "RepositoryConnection"`이면 0, 그 밖은 1.
3. 단위 시험(로컬 HTTP 서버): 정상, 다른 typename, 잘린 JSON, 상한 초과, timeout, redirect.
4. 가이드에 compose 예시 한 줄.

## 범위 밖

소비자 compose 교체(각 저장소가 이 CLI가 나온 뒤 task를 만든다), code-server probe 통합(K-44).

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다.

```text
packages/py/kor-travel-common/src/kortravelcommon/dagster_webserver_health.py
packages/py/kor-travel-common/tests/test_dagster_webserver_health.py
docs/runbooks/dagster-adoption.md, packages/py/kor-travel-common/README.md, CHANGELOG.md
```

## 수용 기준

- [ ] 시험 6개 이상 통과, skip 0.
- [ ] `python -I -c "import kortravelcommon.dagster_webserver_health"`가 core-only 설치에서 성공하고 `sys.modules`에 `dagster`가 없다.
- [ ] 전체 대기가 인자로 준 timeout을 넘지 않는다(시험으로 단언).

## 검증 명령

```bash
cd packages/py/kor-travel-common
uv sync --locked --extra dev && uv run pytest -q tests/test_dagster_webserver_health.py
uv build
```

## evidence

시험 출력과 wheel 설치 스모크.

## rollback·release 차단 조건

- 새 모듈 추가. `git revert` 1회.
