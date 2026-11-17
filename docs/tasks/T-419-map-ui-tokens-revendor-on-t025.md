# T-419 map: T-025 릴리스 당일 ui·tokens 재vendor(T-417 미완일 때)

- 상태: BLOCKED
- 우선순위: P2
- Gate: 소비자 CI(공통 프론트엔드 정책·frontend)
- 선행: T-025
- 외부 선행: T-025 동결 PR 병합 당일에 실행한다. 그 전에 T-417이 병합됐으면 실행하지 않고 닫는다
- 소유 저장소: kor-travel-map
- 병렬: T-025 동결과 같은 날. T-415의 외부 선행(map이 옛 guard에 남아 있을 때)

출처는 [공통화 재조사·계획(2026-11-17)](../plan/commonization-plan-2026-11-17.md)의 §4.1(K-01·K-02)이다. 근거 위치(file:line)와 차이 분석은 그 문서가 정본이며 여기서 반복하지 않는다.

## 목표

map은 정확 Node/npm 핀 결정(T-416)을 기다리는 동안 옛 guard(`55a921b`)를 호출하고, 그 판은 common `main`의 정책을 읽는다. T-025가 `ui`·`tokens`의 현재 값을 올리는 날 map의 guard가 실패한다. 그날 두 tarball을 재vendor한다. T-417이 먼저 끝나 map이 새 guard에 있으면 이 task는 필요 없다.

## 고정 결정

- 한 PR은 한 산출물 묶음(`ui`·`tokens`)이다. 프레임워크 업그레이드나 부품 채택(T-415)과 섞지 않는다([ADR-010](../adr/010-consumer-adoption-model.md) 결정 5).
- T-025 판은 patch 올림이고 공개 API·CSS 변경이 없다(`ui` 0.2.2·`tokens` 0.1.3). 화면이 바뀌면 안 된다.
- guard 호출 SHA는 바꾸지 않는다. 그것은 T-416의 결정과 T-417의 몫이다.
- T-025의 source PR이 병합되면 main push artifact에 tarball이 있다. 이 PR은 그때 미리 만들어 두고 동결 PR이 병합된 날 병합한다.

## 구현 범위

1. `vendor/`의 `kor-travel-ui`·`kor-travel-tokens` tarball을 T-025 판으로 바꾸고 `package.json`·루트 `package-lock.json`·`common-artifacts.json`을 갱신한다(#1504와 같은 파일 묶음).
2. T-025의 이관 절이 `check:dependencies` 명령 줄 교체를 요구하면 그 줄로 바꾼다(요구하지 않는 것이 T-025의 수용 기준이다).
3. T-417이 이미 병합됐는지 먼저 확인한다. 병합됐으면 이 task를 '대상 없음'으로 닫고 근거를 적는다.

## 범위 밖

guard 호출 SHA·도구 규칙(T-417), admin-kit 채택(T-415), 재수출 shim(T-418), `vworld-*` 등 다른 산출물.

## 대상 저장소·브랜치·PR·되돌리기

- 저장소 `digitie/kor-travel-map`. 이 저장소(common)의 작업이 아니다. 그 저장소의 규칙·리뷰·CI를 따른다.
- 브랜치: `docs/…` 또는 `agent/<agent>-<task>` 형식의 작업 브랜치, `origin/main`에서 분기. PR 1개.
- 되돌리기: `git revert <merge-sha>` 1회.
- 그 저장소의 backlog에는 이 task를 가리키는 포인터 한 줄만 두고 수용 기준을 복제하지 않는다.

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다.

```text
packages/kor-travel-map-admin/frontend/{package.json,common-artifacts.json}
packages/kor-travel-map-admin/frontend/vendor/kor-travel-{ui,tokens}-*.tgz
package-lock.json(루트)
docs/journal.md, docs/resume.md, docs/tasks.md
```

## 수용 기준

- [ ] '공통 프론트엔드 정책' check가 호출 SHA(`55a921b`) 그대로 통과한다.
- [ ] `npm run check:dependencies`·lint·type-check·단위 시험·`next build`가 통과한다.
- [ ] 벤더한 두 tarball의 SHA-256이 common 원장(`frontend-artifacts.json`)의 T-025 판 값과 같다.
- [ ] T-025 동결 PR 병합 시각과 이 PR 병합 시각을 PR에 적는다(map main의 guard가 빨간 구간).

## 검증 명령

```bash
# kor-travel-map
npm ci --ignore-scripts
(cd packages/kor-travel-map-admin/frontend && npm run check:dependencies && npm run lint && npm run type-check && npm test && npm run build)
sha256sum packages/kor-travel-map-admin/frontend/vendor/kor-travel-{ui,tokens}-*.tgz
gh pr checks <PR>
```

## evidence

PR의 check 결과, 두 tarball의 SHA-256, 빨간 구간의 두 시각.

## rollback·release 차단 조건

- 되돌리지 않는다. 되돌리면 map의 guard가 다시 실패한다. 문제가 있으면 common의 다음 patch를 받아 앞으로 고친다.
