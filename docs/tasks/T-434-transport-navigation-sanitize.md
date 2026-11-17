# T-434 transport-admin: 로컬 경로 정규화 사본을 공통 export로 교체

- 상태: READY
- 우선순위: P3
- Gate: 소비자 단위·빌드·e2e
- 선행: 없음
- 소유 저장소: kor-travel-transport
- 병렬: 묶음 A

출처는 [공통화 재조사·계획(2026-11-17)](../plan/commonization-plan-2026-11-17.md)의 §3.5·§4.7(K-51)이다. 근거 위치(file:line)와 차이 분석은 그 문서가 정본이며 여기서 반복하지 않는다.

## 목표

transport 관리자 프론트의 `lib/navigation.ts`는 공통 `sanitizeLocalPath`와 같은 목적의 로컬 구현이고 서버 쪽과 client(`components/login-form.tsx`) 모두 이 로컬 구현을 쓴다. 판정은 지금 공통과 맞지만 구현이 세 벌이면 다시 갈라진다. 로컬 구현의 판정 본체를 공통 호출로 바꾼다.

## 고정 결정

- T-465와 같다(얇은 로컬 함수가 타입 좁히기·trim·500자 상한을 갖고 공통 함수를 부른다).
- 호출부 세 곳(로그인 route, 로그인 page, client 로그인 폼)의 import는 그대로 `@/lib/navigation`이다.
- 이 저장소는 다른 팀이 유지한다.

## 구현 범위

1. `lib/navigation.ts`를 얇은 함수로 줄인다. URL 파싱과 경계 검사를 로컬에 두지 않는다.
2. `fallback` 인자는 어느 호출부도 넘기지 않는다. 인자를 없앤다.
3. 기존 단위 시험을 유지하고, 공통 구현이 더 거절하는 입력의 시험을 더한다.

## 범위 밖

세션·로그인 로직, 패키지 변경.

## 대상 저장소·브랜치·PR·되돌리기

- 저장소 `digitie/kor-travel-transport`. 이 저장소(common)의 작업이 아니다. 그 저장소의 규칙·리뷰·CI를 따른다.
- 브랜치: `docs/…` 또는 `agent/<agent>-<task>` 형식의 작업 브랜치, `origin/main`에서 분기. PR 1개.
- 되돌리기: `git revert <merge-sha>` 1회.
- 그 저장소의 backlog에는 이 task를 가리키는 포인터 한 줄만 두고 수용 기준을 복제하지 않는다.

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다.

```text
packages/kor-travel-transport-admin/frontend/lib/navigation.ts          # 얇은 함수로
packages/kor-travel-transport-admin/frontend/**/*.test.ts
```

## 수용 기준

- [ ] `lib/navigation.ts`에 `new URL(`이 없다.
- [ ] 공백이 붙은 정상 경로, 500자 초과 경로, 문자열이 아닌 값의 결과가 바꾸기 전과 같다.
- [ ] transport-admin job(lint·type-check·test·build)이 통과한다.

## 검증 명령

```bash
npm run lint && npm run type-check && npm test && npm run build
```

## evidence

PR의 CI 결과.

## rollback·release 차단 조건

- `git revert` 1회.
