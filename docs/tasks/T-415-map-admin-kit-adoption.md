# T-415 map: admin-kit 채택

- 상태: BLOCKED
- 우선순위: P1
- Gate: 소비자 빌드·단위·e2e·시각 비교
- 선행: T-221
- 외부 선행: map이 옛 guard(`55a921b`)에 남아 있으면 T-419 완료
- 소유 저장소: kor-travel-map
- 병렬: 채택 묶음 C. 원천 저장소라 먼저 하기를 권한다(선행 관계는 아니다)

출처는 [공통화 재조사·계획(2026-11-17)](../plan/commonization-plan-2026-11-17.md)의 §3.5·§4.8(K-50)이다. 근거 위치(file:line)와 차이 분석은 그 문서가 정본이며 여기서 반복하지 않는다.

## 목표

map 관리자 프론트의 로컬 부품을 `@kor-travel/admin-kit`의 것으로 바꾸고 로컬 파일을 지운다. map이 원천이므로 먼저 채택해 시각 차이를 잡는다.

## 고정 결정

- 한 PR은 한 산출물이다. 프레임워크 업그레이드와 섞지 않는다([ADR-010](../adr/010-consumer-adoption-model.md) 결정 5).
- `status-label.ts`는 도메인 사전이라 map에 남고 공통 부품에 주입한다.
- 화면 값(색·간격)이 바뀌면 안 된다. 바뀌는 곳은 PR에 전후 화면을 붙인다.
- admin-kit은 벤더한 날부터 중앙 정본과 대조돼야 한다. 옛 guard(main 정책을 읽음)는 그대로 대조한다. 새 guard(T-024)는 고정한 커밋의 정책에 admin-kit이 없으면 건너뛰므로, 호출 SHA를 T-221이 지정한 admin-kit 채택 커밋으로 올리는 것이 채택의 일부다. 그 커밋의 정책은 `ui`·`tokens`가 T-025 판이므로 함께 재vendor한다. map은 T-416·T-417을 기다리지 않는다: `55a921b`에 남아 있으면 `ui`·`tokens`는 T-419로 T-025 판이고 `55a921b` 검사기가 main 정책으로 admin-kit을 대조한다.

## 구현 범위

1. 첫 단계(앞선 PR 권장, [ADR-010](../adr/010-consumer-adoption-model.md) 결정 5): 호출하는 guard가 새 판(T-024)이면 호출 SHA와 `common-ref`를 T-221이 지정한 admin-kit 채택 커밋으로 올리고 `ui`·`tokens`를 그 커밋의 값(T-025 판)으로 재vendor한다. 옛 판(main 정책을 읽음)이면 `ui`·`tokens`는 T-025 릴리스 날 이미 올라와 있어 이 단계가 없다.
2. `vendor/`에 admin-kit tarball을 더하고 `package.json`·루트 `package-lock.json`·`common-artifacts.json`에 등록한다.
3. 로컬 `components/{stat-strip,status-badge*,detail-list,json-viewer,copy-button,pagination-bar,help-tip,app-error-panel,section-card,filter-bar}`, `components/ui/form-*`, `lib/{format,error-recovery}.ts`를 공통 import로 바꾸고 파일을 지운다. `empty-state`는 T-219의 결정을 따른다. `confirm-dialog`·`sonner.tsx`·로컬 `button.tsx`는 남긴다.
4. `StatusBadge`·`StatStrip`에 map의 `status-label` 사전을, `StatStrip`·`DetailList`에 `next/link`를, `CopyButton`에 토스트 함수를 주입한다.
5. 단위 시험·e2e 선택자 갱신.

## 범위 밖

지도 작업면 채택(`T-UI-MAPWORKSPACE`, map이 보류 중), 도구 규칙 이관(T-417), 재수출 shim 제거(T-418).

## 대상 저장소·브랜치·PR·되돌리기

- 저장소 `digitie/kor-travel-map`. 이 저장소(common)의 작업이 아니다. 그 저장소의 규칙·리뷰·CI를 따른다.
- 브랜치: `docs/…` 또는 `agent/<agent>-<task>` 형식의 작업 브랜치, `origin/main`에서 분기. PR 1개.
- 되돌리기: `git revert <merge-sha>` 1회.
- 그 저장소의 backlog에는 이 task를 가리키는 포인터 한 줄만 두고 수용 기준을 복제하지 않는다.

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다.

```text
packages/kor-travel-map-admin/frontend/{package.json,common-artifacts.json,vendor/*}, package-lock.json(루트)
.github/workflows/common-frontend-policy.yml          # 새 guard일 때만
packages/kor-travel-map-admin/frontend/src/components/**, src/lib/**
packages/kor-travel-map-admin/frontend/{tests,e2e}/**
docs/journal.md, docs/resume.md, docs/tasks.md
```

## 수용 기준

- [ ] `npm run check:dependencies`·lint·type-check·단위 시험·`next build`가 통과한다.
- [ ] 지운 로컬 파일 수와 줄 수를 PR에 적는다.
- [ ] mocked e2e가 통과하고 6폭(320/375/414/768/1024/1440) 화면 비교에서 의도하지 않은 차이가 0이다.
- [ ] '공통 프론트엔드 정책' check: guard 실행이 admin-kit을 중앙 정본과 대조했고 통과한다(옛 guard면 호출 SHA 그대로, 새 guard면 admin-kit 채택 커밋). admin-kit이 없는 정책으로 건너뛴 통과는 인정하지 않는다.

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
