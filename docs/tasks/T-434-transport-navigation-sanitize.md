# T-434 transport-admin: 로컬 경로 정규화 사본을 공통 export로 교체

- 상태: READY
- 우선순위: P2
- Gate: 소비자 단위·빌드·e2e
- 선행: 없음
- 소유 저장소: kor-travel-transport
- 병렬: 묶음 A

출처는 [공통화 재조사·계획(2026-11-17)](../plan/commonization-plan-2026-11-17.md)의 §3.5·§4.7(K-51)이다. 근거 위치(file:line)와 차이 분석은 그 문서가 정본이며 여기서 반복하지 않는다.

## 목표

transport 관리자 프론트의 `lib/navigation.ts`는 공통 `sanitizeLocalPath`와 같은 규칙의 사본이다. 사본이 세 벌이면 다시 갈라진다. 공통 export 하나만 쓴다.

## 고정 결정

- T-465와 같다.
- 이 저장소는 다른 팀이 유지한다.

## 구현 범위

1. `lib/navigation.ts`를 지우고 서버 쪽 호출부가 `@kor-travel/ui/navigation`을 import한다.
2. `fallback` 인자를 쓰는 호출부만 얇게 감싼다.
3. 기존 단위 시험을 공통 함수 기준으로 옮긴다.

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
packages/kor-travel-transport-admin/frontend/lib/navigation.ts          # 삭제
packages/kor-travel-transport-admin/frontend/**                        # 서버 쪽 호출부 import
```

## 수용 기준

- [ ] 저장소에 `sanitizeLocalPath`의 로컬 정의가 0개다.
- [ ] transport-admin job(lint·type-check·test·build)이 통과한다.

## 검증 명령

```bash
npm run lint && npm run type-check && npm test && npm run build
```

## evidence

PR의 CI 결과.

## rollback·release 차단 조건

- `git revert` 1회.
