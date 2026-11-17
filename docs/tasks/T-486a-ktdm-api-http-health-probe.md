# T-486a ktdm: map-api·pinvi-api healthcheck를 공통 HTTP probe로 교체

- 상태: READY
- 우선순위: P1
- Gate: 소비자 CI(backend)·고정 이미지 확인·재구축 수용
- 선행: 없음
- 소유 저장소: kor-travel-docker-manager
- 병렬: 묶음 A(T-480a와 독립)

출처는 [공통화 재조사·계획(2026-11-17)](../plan/commonization-plan-2026-11-17.md)의 §3.3·§4.4(K-10)이다. 근거 위치(file:line)와 차이 분석은 그 문서가 정본이며 여기서 반복하지 않는다.

## 목표

Manager compose에서 weather-api는 이미 exec 형식 공통 probe를 쓴다. map-api(`docker-compose.yml:1738-1741`)와 pinvi-api(`:2204-2207`)는 `CMD-SHELL`이다. 둘을 같은 형식으로 바꾼다.

## 고정 결정

- probe 계약은 [http-health-probe](../runbooks/http-health-probe.md)가 정본이다.
- Manager는 범용으로 유지한다. 서비스 이름을 코드에 넣지 않는다. 이 변경은 compose 데이터와 그 시험뿐이다.
- compose가 요구하는 모듈이 고정 이미지에 없으면 재구축이 `compose up`에서만 죽는다. 그래서 이미지 확인이 수용 기준이다.
- PinVi Dockerfile의 세 엔드포인트 probe는 바꾸지 않는다(pinvi 소유, 한 경로 probe와 뜻이 다르다).

## 구현 범위

1. 두 서비스의 `healthcheck.test`를 `CMD`·`python`·`-I`·`-m`·`kortravelcommon.http_health`·`--port`·(기존 포트 식)·`--path`·`/health`·`--timeout-seconds`·`3`으로 바꾼다.
2. Docker `timeout`·`interval`은 weather-api 블록의 방식(Python 시작 비용을 timeout이 감싼다)을 따른다.
3. compose 구조를 고정하는 backend 시험을 갱신한다.
4. `docs/docker-management.md`의 healthcheck 절을 고친다.

## 범위 밖

geo-api(범위 밖 저장소의 이미지), Dagster webserver·code-server probe, pinvi Dockerfile.

## 대상 저장소·브랜치·PR·되돌리기

- 저장소 `digitie/kor-travel-docker-manager`. 이 저장소(common)의 작업이 아니다. 그 저장소의 규칙·리뷰·CI를 따른다.
- 브랜치: `docs/…` 또는 `agent/<agent>-<task>` 형식의 작업 브랜치, `origin/main`에서 분기. PR 1개.
- 되돌리기: `git revert <merge-sha>` 1회 뒤 trusted release 재설치.
- 그 저장소의 backlog에는 이 task를 가리키는 포인터 한 줄만 두고 수용 기준을 복제하지 않는다.

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다.

```text
docker-compose.yml
backend/tests/**                      # compose 고정 시험
docs/docker-management.md, docs/journal.md, docs/tasks.md
```

## 수용 기준

- [ ] 현재 pin된 map-api 이미지와 pinvi-api 이미지 각각에서 `python -I -c "import kortravelcommon.http_health"`가 0으로 끝난다(모듈 존재 확인. `-m` 실행은 모듈이 없어도 1로 끝나므로 존재 확인에 쓰지 않는다). 결과를 PR에 붙인다.
- [ ] backend 시험 전체와 ruff가 통과한다.
- [ ] compose에서 두 서비스의 `CMD-SHELL` healthcheck가 사라졌다.
- [ ] 설치·재구축 뒤 두 컨테이너가 `healthy`다. 실행하지 못하면 `NOT_RUN(운영 호스트)`로 남기고 병합 전 담당이 확인한다.

## 검증 명령

```bash
# kor-travel-docker-manager
python -m pytest backend -q && ruff check backend
docker run --rm --entrypoint python <map-api 이미지> -I -c 'import kortravelcommon.http_health'; echo $?
docker run --rm --entrypoint python <pinvi-api 이미지> -I -c 'import kortravelcommon.http_health'; echo $?
```

## evidence

이미지별 모듈 확인 출력, CI 결과, 재구축 뒤 health 상태.

## rollback·release 차단 조건

- `git revert` 1회 뒤 신뢰 릴리스를 다시 설치한다.
- 두 이미지 중 하나라도 모듈이 없으면 병합하지 않는다.
