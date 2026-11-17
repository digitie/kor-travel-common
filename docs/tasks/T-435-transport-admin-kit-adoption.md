# T-435 transport: ui 0.3.0 재vendor·guard 호출 SHA 갱신과 관리자 부품 채택

- 상태: BLOCKED
- 우선순위: P2
- Gate: 소비자 빌드·단위·e2e·시각 비교
- 선행: T-221
- 소유 저장소: kor-travel-transport
- 병렬: 채택 묶음(T-424·T-466·T-474와 동시 가능, T-415 뒤 권장)

출처는 [공통화 재조사·계획(2026-11-17)](../plan/commonization-plan-2026-11-17.md)의 §3.5·§4.8(K-50)이다. 근거 위치(file:line)와 차이 분석은 그 문서가 정본이며 여기서 반복하지 않는다.

## 목표

transport의 두 프론트를 `@kor-travel/ui` 0.3.0으로 재vendor하고 guard 호출 SHA를 올린다. 관리자 프론트의 map과 같은 로컬 부품은 공통 부품으로 바꾸고 지운다.

## 고정 결정

- T-415와 같다.
- 예고 창 동안 0.3.0 소비자는 새 검사기에서만 통과한다. 호출 SHA 갱신(`ci.yml`과 독립 workflow 두 곳)과 두 프론트의 재vendor를 한 PR에 둔다. 부품 교체는 같은 PR이거나 뒤따르는 PR이다.
- transport 사본이 map과 다른 다섯 파일(`app-error-panel`·`filter-bar`·`section-card`·`status-label`·`error-recovery`)은 T-219·T-220이 고른 쪽을 따른다. `status-label`은 앱에 남는다.
- 이 저장소는 다른 팀이 유지한다.

## 구현 범위

1. 두 프론트의 ui tarball(과 T-221이 함께 올린 패키지)·원장·lock을 0.3.0으로. guard 호출 SHA 두 곳을 T-024 이후 커밋으로.
2. 관리자 프론트의 로컬 부품과 `lib/{format,error-recovery}.ts`를 공통 import로 바꾸고 지운다. `confirm-dialog`는 남긴다.
3. `components/ui/empty.tsx`와 로컬 `empty-state.tsx`의 이중 구현을 하나로 한다.

## 범위 밖

`lib/vendor/map-marker-react`(지금의 복사 방식 유지), evilcharts 사본, Dagster 콘솔.

## 대상 저장소·브랜치·PR·되돌리기

- 저장소 `digitie/kor-travel-transport`. 이 저장소(common)의 작업이 아니다. 그 저장소의 규칙·리뷰·CI를 따른다.
- 브랜치: `docs/…` 또는 `agent/<agent>-<task>` 형식의 작업 브랜치, `origin/main`에서 분기. PR 1개.
- 되돌리기: `git revert <merge-sha>` 1회.
- 그 저장소의 backlog에는 이 task를 가리키는 포인터 한 줄만 두고 수용 기준을 복제하지 않는다.

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다.

```text
packages/kor-travel-transport-admin/frontend/{package.json,package-lock.json,common-artifacts.json,vendor/*}
packages/kor-travel-transport-admin/frontend/{components,lib}/**
frontend/{package.json,package-lock.json,common-artifacts.json,vendor/*}
```

## 수용 기준

- [ ] guard job이 새 호출 SHA로 세 프론트 항목 모두 통과한다.
- [ ] 두 프론트의 의존성 검사·lint·type-check·단위·build가 통과한다.
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
