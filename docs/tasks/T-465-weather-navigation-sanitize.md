# T-465 weather-admin: 로컬 경로 정규화 사본을 공통 export로 교체

- 상태: READY
- 우선순위: P2
- Gate: 소비자 단위·빌드·e2e
- 선행: 없음
- 소유 저장소: kor-travel-weather
- 병렬: 묶음 A

출처는 [공통화 재조사·계획(2026-11-17)](../plan/commonization-plan-2026-11-17.md)의 §3.5·§4.7(K-51)이다. 근거 위치(file:line)와 차이 분석은 그 문서가 정본이며 여기서 반복하지 않는다.

## 목표

weather 관리자 프론트의 `lib/navigation.ts`는 공통 `sanitizeLocalPath`와 같은 목적의 로컬 구현이다. 기준 커밋에서 이 사본에 빠져 있던 검증 하나는 kor-travel-weather #244(`8c3b4744`)가 더해 세 사본의 판정이 같아졌다. 남은 일은 중복 제거다. 로컬 구현의 판정 본체를 공통 호출로 바꿔 다시 갈라지지 않게 한다.

## 고정 결정

- 공통 함수의 계약은 `packages/ui/src/navigation.ts`와 그 단위 시험이 정본이다.
- 패키지 버전을 올리지 않는다. 이미 벤더한 `@kor-travel/ui`에 export가 있다.
- 두 구현은 모양이 다르다. 공통은 `string | null | undefined`를 받고 인코딩된 경계 문자·제어 문자를 거절한다. 로컬은 `unknown`을 받고 앞뒤 공백을 지우고 500자를 넘으면 거절한다. 호출부는 `unknown`을 넘긴다(로그인 route의 요청 본문). 그래서 사본을 통째로 지우지 않고, 타입 좁히기·trim·길이 상한만 가진 얇은 로컬 함수가 공통 함수를 부르게 한다.
- 이 저장소는 다른 팀이 유지한다. 시점과 방식은 그 팀이 정한다.

## 구현 범위

1. `lib/navigation.ts`를 얇은 함수로 줄인다: 문자열이 아니면 기본 경로, trim, 500자 초과면 기본 경로, 그다음 `@kor-travel/ui/navigation`의 `sanitizeLocalPath` 호출. URL 파싱과 경계 검사를 로컬에 두지 않는다.
2. 호출부 import는 그대로 `@/lib/navigation`이다. client(`components/login-form.tsx`)는 지금처럼 공통 export를 직접 쓴다.
3. `fallback` 인자는 어느 호출부도 넘기지 않는다. 인자를 없앤다.
4. 단위 시험: 기존 시험과 #244의 시험이 그대로 통과한다. 공통 구현이 더 거절하는 입력(인코딩된 경계 문자)이 이제 기본 경로가 된다는 시험을 더한다.
5. 서버 번들에 하위 경로가 실리는지 `next build`로 확인한다.

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
packages/kor-travel-weather-admin/frontend/lib/navigation.ts            # 얇은 함수로
packages/kor-travel-weather-admin/frontend/lib/navigation.test.ts
```

## 수용 기준

- [ ] `lib/navigation.ts`에 `new URL(`이 없다(판정 본체는 공통 함수).
- [ ] 기존 단위 시험 4건이 수정 없이 통과한다.
- [ ] 공백이 붙은 정상 경로, 500자 초과 경로, 문자열이 아닌 값의 결과가 바꾸기 전과 같다.
- [ ] lint·type-check·단위·`next build`·기존 e2e가 통과한다.

## 검증 명령

```bash
# kor-travel-weather/packages/kor-travel-weather-admin/frontend
rg -n "new URL\(" lib/navigation.ts && exit 1 || true
npm run lint && npm run type-check && npm test && npm run build
```

## evidence

PR의 시험 출력.

## rollback·release 차단 조건

- `git revert` 1회로 로컬 구현이 돌아온다(#244의 검증은 그 구현에 들어 있다).
