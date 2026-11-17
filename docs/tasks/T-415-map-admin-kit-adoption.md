# T-415 map: 관리자 공통 부품 묶음 채택

- 상태: BLOCKED
- 우선순위: P1
- Gate: 소비자 빌드·단위·e2e·시각 비교
- 선행: T-221, T-416
- 소유 저장소: kor-travel-map
- 병렬: 채택 묶음의 첫 번째(원천 저장소). T-424·T-435·T-466·T-474보다 먼저 권장

출처는 [공통화 재조사·계획(2026-11-17)](../plan/commonization-plan-2026-11-17.md)의 §3.5·§4.8(K-50)이다. 근거 위치(file:line)와 차이 분석은 그 문서가 정본이며 여기서 반복하지 않는다.

## 목표

map 관리자 프론트의 로컬 부품을 `@kor-travel/ui` 0.3.0의 것으로 바꾸고 로컬 파일을 지운다. map이 원천이므로 먼저 채택해 시각 차이를 잡는다.

## 고정 결정

- 한 PR은 한 산출물이다. 프레임워크 업그레이드와 섞지 않는다([ADR-010](../adr/010-consumer-adoption-model.md) 결정 5).
- `status-label.ts`는 도메인 사전이라 map에 남고 공통 부품에 주입한다.
- 화면 값(색·간격)이 바뀌면 안 된다. 바뀌는 곳은 PR에 전후 화면을 붙인다.
- 예고 창 동안 0.3.0을 받으려면 guard 호출 SHA가 T-024 이후여야 한다(옛 검사기는 현재 값 0.2.1만 통과시킨다). 그래서 T-416의 결정이 선행이다. '채택'이면 T-417 뒤에 병합한다. '미채택'이면 이 PR은 검증까지 마치고 대기하다가 T-222의 전환 PR 직후 병합한다.

## 구현 범위

1. `vendor/`의 ui tarball(과 T-221이 함께 올린 패키지)·`common-artifacts.json`·lock을 0.3.0으로.
2. 로컬 `components/{empty-state,stat-strip,status-badge*,detail-list,json-viewer,copy-button,pagination-bar,help-tip,app-error-panel,section-card,filter-bar}`, `components/ui/form-*`, `lib/{format,error-recovery}.ts`를 공통 import로 바꾸고 파일을 지운다. `confirm-dialog`는 남긴다.
3. `components/ui/*`의 얇은 재수출 중 공통과 같은 것은 지운다. `button.tsx` 로컬 wrapper는 공통 `Button`이 같은 동작을 주는 범위에서만 지운다.
4. `StatusBadge`·`StatStrip`에 map의 `status-label` 사전을, `StatStrip`·`DetailList`에 `next/link`를 주입한다.
5. 단위 시험·e2e 선택자 갱신.

## 범위 밖

지도 작업면 채택(`T-UI-MAPWORKSPACE`, map이 보류 중), guard 호출 SHA(T-417).

## 대상 저장소·브랜치·PR·되돌리기

- 저장소 `digitie/kor-travel-map`. 이 저장소(common)의 작업이 아니다. 그 저장소의 규칙·리뷰·CI를 따른다.
- 브랜치: `docs/…` 또는 `agent/<agent>-<task>` 형식의 작업 브랜치, `origin/main`에서 분기. PR 1개.
- 되돌리기: `git revert <merge-sha>` 1회.
- 그 저장소의 backlog에는 이 task를 가리키는 포인터 한 줄만 두고 수용 기준을 복제하지 않는다.

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다.

```text
packages/kor-travel-map-admin/frontend/{package.json,package-lock.json,common-artifacts.json,vendor/*}
packages/kor-travel-map-admin/frontend/src/components/**, src/lib/**
packages/kor-travel-map-admin/frontend/{tests,e2e}/**
docs/journal.md, docs/resume.md, docs/tasks.md
```

## 수용 기준

- [ ] `npm run check:dependencies`·lint·type-check·단위 시험·`next build`가 통과한다.
- [ ] 지운 로컬 파일 수와 줄 수를 PR에 적는다(목표: 표시·폼 부품 파일 0개 잔존).
- [ ] mocked e2e가 통과하고 6폭(320/375/414/768/1024/1440) 화면 비교에서 의도하지 않은 차이가 0이다.
- [ ] '공통 프론트엔드 정책' check가 통과한다.

## 검증 명령

```bash
# kor-travel-map/packages/kor-travel-map-admin/frontend
npm run check:dependencies && npm run lint && npm run type-check && npm test && npm run build
npx playwright test   # 저장소의 e2e 진입점
```

## evidence

PR 본문(지운 파일·줄 수, 6폭 전후 화면, check 결과).

## rollback·release 차단 조건

- `git revert` 1회(lock·vendor 포함).
- 의도하지 않은 시각 차이가 남으면 병합하지 않는다.
