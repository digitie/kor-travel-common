# T-480b map-api: compose healthcheck를 공통 HTTP probe로 교체

- 상태: READY
- 우선순위: P1
- Gate: 소비자 CI·컨테이너 healthy 확인
- 선행: 없음
- 소유 저장소: kor-travel-map
- 병렬: 묶음 A(T-486a와 독립)

출처는 [공통화 재조사·계획(2026-11-17)](../plan/commonization-plan-2026-11-17.md)의 §3.3·§4.4(K-10)이다. 근거 위치(file:line)와 차이 분석은 그 문서가 정본이며 여기서 반복하지 않는다.

## 목표

map 자체 `docker-compose.yml`의 API healthcheck는 `CMD-SHELL`로 인라인 `python -c urllib`를 돌린다. 이미지에 이미 들어 있는 `kortravelcommon.http_health`(exec 형식, shell 없음, 전체 대기 상한)로 바꾼다.

## 고정 결정

- probe 계약은 [http-health-probe](../runbooks/http-health-probe.md)가 정본이다.
- `/health` 응답과 OpenAPI는 바꾸지 않는다. 바뀌는 것은 compose의 probe 명령뿐이다.
- 새 의존이 없다. map-api는 이미 `kor-travel-common[http]`를 설치한다(`packages/kor-travel-map-api/pyproject.toml:31`).
- map 자체 compose는 컨테이너 env와 게시 포트가 같은 변수 `KOR_TRAVEL_MAP_API_PORT`를 쓴다(`docker-compose.yml:417,508`). 그래서 compose 치환 값이 컨테이너 안 포트와 같다. Manager compose는 그렇지 않다(T-486a).

## 구현 범위

1. `docker-compose.yml:513-518`의 `test`를 `["CMD", "python", "-I", "-m", "kortravelcommon.http_health", "--port", "${KOR_TRAVEL_MAP_API_PORT:-12701}", "--path", "/health", "--timeout-seconds", "3"]`로 바꾼다.
2. Docker `timeout`이 Python 시작 비용을 감싸는지 확인하고 필요하면 값을 조정한다(현재 5s).
3. compose 내용을 고정하는 map의 시험이 있으면 함께 갱신한다.

## 범위 밖

Manager compose의 같은 probe(T-486a), Dagster webserver probe, `/health` 본문.

## 대상 저장소·브랜치·PR·되돌리기

- 저장소 `digitie/kor-travel-map`. 이 저장소(common)의 작업이 아니다. 그 저장소의 규칙·리뷰·CI를 따른다.
- 브랜치: `docs/…` 또는 `agent/<agent>-<task>` 형식의 작업 브랜치, `origin/main`에서 분기. PR 1개.
- 되돌리기: `git revert <merge-sha>` 1회.
- 그 저장소의 backlog에는 이 task를 가리키는 포인터 한 줄만 두고 수용 기준을 복제하지 않는다.

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다.

```text
docker-compose.yml
tests/**(compose 고정 시험이 있으면)
docs/journal.md, docs/resume.md
```

## 수용 기준

- [ ] 빌드한 API 이미지에서 `python -I -c "import kortravelcommon.http_health"`가 0으로 끝난다(모듈 존재 확인. `-m` 실행은 모듈이 없어도 1로 끝나므로 존재 확인에 쓰지 않는다).
- [ ] standalone 스택에서 API 컨테이너가 `healthy`가 된다.
- [ ] compose 파일에 API용 `CMD-SHELL` healthcheck가 남아 있지 않다.
- [ ] map CI(`ci`·`lint`·`docker-images`)가 통과한다.

## 검증 명령

```bash
# kor-travel-map
docker compose config >/dev/null
docker compose run --rm --no-deps --entrypoint python api -I -c 'import kortravelcommon.http_health'; echo $?
docker compose up -d api && docker inspect --format '{{.State.Health.Status}}' <api 컨테이너>
```

## evidence

PR 본문에 healthy 전환 출력과 CI 결과.

## rollback·release 차단 조건

- `git revert` 1회로 이전 probe로 돌아간다.
