# T-466 weather-admin: admin-kit 채택

- 상태: BLOCKED
- 우선순위: P2
- Gate: 소비자 빌드·단위·e2e·시각 비교
- 선행: T-221
- 소유 저장소: kor-travel-weather
- 병렬: 채택 묶음 C(T-435와 동시 가능, T-415 뒤 권장)

출처는 [공통화 재조사·계획(2026-11-17)](../plan/commonization-plan-2026-11-17.md)의 §3.5·§4.8(K-50)이다. 근거 위치(file:line)와 차이 분석은 그 문서가 정본이며 여기서 반복하지 않는다.

## 목표

weather 관리자 프론트의 map과 같은 로컬 부품을 `@kor-travel/admin-kit`의 것으로 바꾸고 로컬 파일을 지운다.

## 고정 결정

- T-415와 같다. map의 채택 PR을 참고 구현으로 쓴다.
- guard 호출 SHA와 `@kor-travel/ui`·`tokens` 버전은 이 PR에서 바꾸지 않는다.
- `status-label.ts`는 weather의 도메인 사전으로 남긴다(지금은 map 사전을 그대로 갖고 있다. 정리는 이 task 밖).
- 이 저장소는 다른 팀이 유지한다.

## 구현 범위

1. `vendor/`에 admin-kit tarball을 더하고 `package.json`·lock·`common-artifacts.json`에 등록한다.
2. 로컬 표시·폼·도움말·오류 부품과 `lib/{format,error-recovery}.ts`를 공통 import로 바꾸고 지운다. `confirm-dialog`·`sonner.tsx`·로컬 `button.tsx`는 남긴다.
3. 단위·e2e 선택자 갱신.

## 범위 밖

evilcharts 사본, Dagster 콘솔(T-216), 팔레트.

## 대상 저장소·브랜치·PR·되돌리기

- 저장소 `digitie/kor-travel-weather`. 이 저장소(common)의 작업이 아니다. 그 저장소의 규칙·리뷰·CI를 따른다.
- 브랜치: `docs/…` 또는 `agent/<agent>-<task>` 형식의 작업 브랜치, `origin/main`에서 분기. PR 1개.
- 되돌리기: `git revert <merge-sha>` 1회.
- 그 저장소의 backlog에는 이 task를 가리키는 포인터 한 줄만 두고 수용 기준을 복제하지 않는다.

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다.

```text
packages/kor-travel-weather-admin/frontend/{package.json,package-lock.json,common-artifacts.json,vendor/*}
packages/kor-travel-weather-admin/frontend/{components,lib}/**
```

## 수용 기준

- [ ] `common-policy / guard` job이 지금 호출 SHA 그대로 통과한다.
- [ ] 의존성 검사·lint·type-check·단위·build·e2e가 통과한다.
- [ ] 지운 파일 수와 줄 수를 PR에 적는다.
- [ ] 6폭 화면 비교에서 의도하지 않은 차이가 0이다.

## 검증 명령

```bash
npm run check:dependencies && npm run lint && npm run type-check && npm test && npm run build
```

## evidence

PR 본문.

## rollback·release 차단 조건

- `git revert` 1회(lock·vendor 포함).
