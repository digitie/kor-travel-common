# T-435 transport-admin: admin-kit 채택

- 상태: BLOCKED
- 우선순위: P2
- Gate: 소비자 빌드·단위·e2e·시각 비교
- 선행: T-221
- 소유 저장소: kor-travel-transport
- 병렬: 채택 묶음 C(T-466과 동시 가능, T-415 뒤 권장)

출처는 [공통화 재조사·계획(2026-11-17)](../plan/commonization-plan-2026-11-17.md)의 §3.5·§4.8(K-50)이다. 근거 위치(file:line)와 차이 분석은 그 문서가 정본이며 여기서 반복하지 않는다.

## 목표

transport 관리자 프론트의 map과 같은 로컬 부품을 `@kor-travel/admin-kit`의 것으로 바꾸고 로컬 파일을 지운다.

## 고정 결정

- T-415와 같다.
- admin-kit은 벤더한 날부터 중앙 정본과 대조돼야 한다. 옛 guard(main 정책을 읽음)는 그대로 대조한다. 새 guard(T-024)는 고정한 커밋의 정책에 admin-kit이 없으면 건너뛰므로, 호출 SHA를 T-221이 지정한 admin-kit 채택 커밋으로 올리는 것이 채택의 일부다. 그 커밋의 정책은 `ui`·`tokens`가 T-025 판이므로 함께 재vendor한다. transport는 workflow 하나가 두 프론트를 검사하므로 호출 SHA를 올리면 공개 프론트(`frontend/`)의 `ui`·`tokens`도 같은 PR에서 재vendor한다. 공개 프론트는 admin-kit을 쓰지 않는다.
- transport 사본이 map과 다른 다섯 파일(`app-error-panel`·`filter-bar`·`section-card`·`status-label`·`error-recovery`)은 T-219·T-220이 고른 쪽을 따른다. `status-label`은 앱에 남는다.
- 이 저장소는 다른 팀이 유지한다.

## 구현 범위

1. 첫 단계(앞선 PR 권장, [ADR-010](../adr/010-consumer-adoption-model.md) 결정 5): 호출하는 guard가 새 판(T-024)이면 호출 SHA와 `common-ref`를 T-221이 지정한 admin-kit 채택 커밋으로 올리고 `ui`·`tokens`를 그 커밋의 값(T-025 판)으로 재vendor한다. 옛 판(main 정책을 읽음)이면 `ui`·`tokens`는 T-025 릴리스 날 이미 올라와 있어 이 단계가 없다.
2. 관리자 프론트의 `vendor/`에 admin-kit tarball을 더하고 `package.json`·lock·`common-artifacts.json`에 등록한다.
3. 로컬 부품과 `lib/{format,error-recovery}.ts`를 공통 import로 바꾸고 지운다. `confirm-dialog`·`sonner.tsx`·로컬 `button.tsx`는 남긴다.
4. `components/ui/empty.tsx`와 로컬 `empty-state.tsx`의 이중 구현을 T-219의 결정대로 하나로 한다.

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
frontend/{package.json,package-lock.json,common-artifacts.json,vendor/*}          # 새 guard일 때 ui·tokens 재vendor
.github/workflows/ci.yml, .github/workflows/common-frontend-policy.yml          # 새 guard일 때
```

## 수용 기준

- [ ] guard job(두 프론트 항목): guard 실행이 admin-kit을 중앙 정본과 대조했고 통과한다(옛 guard면 호출 SHA 그대로, 새 guard면 admin-kit 채택 커밋). admin-kit이 없는 정책으로 건너뛴 통과는 인정하지 않는다.
- [ ] 관리자 프론트의 의존성 검사·lint·type-check·단위·build가 통과한다.
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
