# T-474 ktdm: ui 0.3.0 재vendor와 guard 호출 SHA 갱신

- 상태: BLOCKED
- 우선순위: P2
- Gate: 소비자 CI(frontend·공통 프론트엔드 정책)
- 선행: T-221
- 소유 저장소: kor-travel-docker-manager
- 병렬: 채택 묶음(T-424·T-435·T-466과 동시 가능)

출처는 [공통화 재조사·계획(2026-11-17)](../plan/commonization-plan-2026-11-17.md)의 §4.1·§4.8이다. 근거 위치(file:line)와 차이 분석은 그 문서가 정본이며 여기서 반복하지 않는다.

## 목표

Manager 프론트는 `@kor-travel/ui` 0.2.1을 벤더한다. T-222가 현재 값을 0.3.0으로 바꾸기 전에 0.3.0으로 재vendor하고 guard 호출 SHA를 T-024 이후로 올린다.

## 고정 결정

- 예고 창 동안 0.3.0 소비자는 새 검사기에서만 통과한다. 호출 SHA 갱신과 재vendor를 한 PR에 둔다.
- Manager의 로컬 `StatStrip`·`AppErrorPanel`은 map과 다른 구현이다. 공통 부품으로 바꿀지는 기존 [T-473](T-473-ktdm-ui-partial.md)이 소유한다. 이 task의 필수 범위가 아니다.

## 구현 범위

1. `frontend/vendor/`의 ui tarball(과 T-221이 함께 올린 패키지), `frontend/common-artifacts.json`, `package.json`·lock.
2. `.github/workflows/common-frontend-policy.yml`의 호출 SHA와 `common-ref`.

## 범위 밖

로컬 부품의 공통 부품 전환(T-473), 토큰 브리지(T-472).

## 대상 저장소·브랜치·PR·되돌리기

- 저장소 `digitie/kor-travel-docker-manager`. 이 저장소(common)의 작업이 아니다. 그 저장소의 규칙·리뷰·CI를 따른다.
- 브랜치: `docs/…` 또는 `agent/<agent>-<task>` 형식의 작업 브랜치, `origin/main`에서 분기. PR 1개.
- 되돌리기: `git revert <merge-sha>` 1회.
- 그 저장소의 backlog에는 이 task를 가리키는 포인터 한 줄만 두고 수용 기준을 복제하지 않는다.

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다.

```text
frontend/vendor/*, frontend/common-artifacts.json, frontend/package.json, frontend/package-lock.json
.github/workflows/common-frontend-policy.yml
docs/journal.md, docs/tasks.md
```

## 수용 기준

- [ ] '공통 프론트엔드 정책' check가 새 호출 SHA로 통과한다.
- [ ] `ci`의 frontend job(lint·type-check·test·build)이 통과한다.
- [ ] 호출 SHA와 `common-ref`가 같은 40자리 값이고 T-024 병합 커밋 이후다.

## 검증 명령

```bash
# kor-travel-docker-manager/frontend
npm ci --engine-strict && npm run check:dependencies && npm test && npm run build
```

## evidence

PR의 check 결과.

## rollback·release 차단 조건

- `git revert` 1회(lock·vendor·호출 SHA 포함).
