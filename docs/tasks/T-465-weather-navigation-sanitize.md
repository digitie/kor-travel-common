# T-465 weather-admin: 로컬 경로 정규화 사본을 공통 export로 교체

- 상태: READY
- 우선순위: P1
- Gate: 소비자 단위·빌드·e2e
- 선행: 없음
- 소유 저장소: kor-travel-weather
- 병렬: 묶음 A

출처는 [공통화 재조사·계획(2026-11-17)](../plan/commonization-plan-2026-11-17.md)의 §3.5·§4.7(K-51)이다. 근거 위치(file:line)와 차이 분석은 그 문서가 정본이며 여기서 반복하지 않는다.

## 목표

weather 관리자 프론트는 client에서는 `@kor-travel/ui/navigation`의 `sanitizeLocalPath`를 쓰고 서버 쪽에는 로컬 사본을 쓴다. 서버 쪽 사본에는 다른 두 사본(공통, transport)에 있는 검증 하나가 빠져 있다. 사본을 지우고 공통 export 하나만 쓴다.

## 고정 결정

- 공통 함수의 계약은 `packages/ui/src/navigation.ts`와 그 단위 시험이 정본이다.
- 패키지 버전을 올리지 않는다. 이미 벤더한 `@kor-travel/ui`에 export가 있다.
- 이 저장소는 다른 팀이 유지한다. 시점과 방식은 그 팀이 정한다.

## 구현 범위

1. `lib/navigation.ts`를 지우고 서버 쪽 호출부가 `@kor-travel/ui/navigation`을 import한다.
2. 공통 함수에는 `fallback` 인자가 없다. 기본 경로가 `/`가 아닌 호출부만 얇게 감싼다.
3. 단위 시험: 공통 구현의 시험 입력 표(`packages/ui/test/navigation.test.ts`)와 같은 입력에 같은 결과를 낸다. 정상 경로의 query·hash는 보존한다.
4. 서버 번들에 하위 경로가 실리는지 `next build`로 확인한다.

## 범위 밖

세션·로그인 로직, 다른 화면, 패키지 변경.

## 대상 저장소·브랜치·PR·되돌리기

- 저장소 `digitie/kor-travel-weather`. 이 저장소(common)의 작업이 아니다. 그 저장소의 규칙·리뷰·CI를 따른다.
- 브랜치: `docs/…` 또는 `agent/<agent>-<task>` 형식의 작업 브랜치, `origin/main`에서 분기. PR 1개.
- 되돌리기: `git revert <merge-sha>` 1회.
- 그 저장소의 backlog에는 이 task를 가리키는 포인터 한 줄만 두고 수용 기준을 복제하지 않는다.

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다.

```text
packages/kor-travel-weather-admin/frontend/lib/navigation.ts            # 삭제
packages/kor-travel-weather-admin/frontend/**                          # 서버 쪽 호출부 import
packages/kor-travel-weather-admin/frontend/**/*.test.ts
```

## 수용 기준

- [ ] 저장소에 `sanitizeLocalPath`의 로컬 정의가 0개다(grep).
- [ ] 공통 구현의 시험 입력 표를 weather 호출부 기준으로 옮긴 시험이 통과한다.
- [ ] 정상 경로(예: `/locations?tab=a#b`)는 그대로 보존된다.
- [ ] lint·type-check·단위·`next build`·기존 e2e가 통과한다.

## 검증 명령

```bash
# kor-travel-weather/packages/kor-travel-weather-admin/frontend
rg -n "function sanitizeLocalPath" . --glob '!node_modules' && exit 1 || true
npm run lint && npm run type-check && npm test && npm run build
```

## evidence

PR의 시험 출력.

## rollback·release 차단 조건

- `git revert` 1회로 로컬 사본이 돌아온다.
