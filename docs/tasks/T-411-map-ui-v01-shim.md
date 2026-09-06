# T-411 map: ui v0.1 소형 shim 채택 + `@source` + `verify:frontend-eslint` 집합 갱신

- 상태: BLOCKED
- 우선순위: P1
- Gate: e2e 30
- 선행: T-212, T-410

## 목표

map admin의 `components/ui/{badge,skeleton,separator,card,alert,input,textarea,native-select,field}`(+`badge-variants`·`field-variants`)를 `@kor-travel/ui` v0.1.0 재수출 shim으로 바꾼다. 호출부는 무변경이며, `@source` 1줄로 패키지 클래스가 빌드에 포함됨을 증명한다. map은 이 소형 세트의 원천이므로 마크업 계약 차이는 0이어야 한다.

## 고정 결정

- [design-brief](../plan/design-brief.md) D-09(비-overlay = native + `useRender`)·D-10(`@source "../node_modules/@kor-travel/ui"`, `kt-` 접두 유틸리티, ESM + `'use client'` 보존, webpack·Turbopack 양쪽)·D-24(ui PR 파일 상한 30)·D-31(0.x SemVer).
- ADR-007·ADR-010 — [ADR 색인](../adr/README.md). 정본: [ui-contract](../standards/ui-contract.md), [frontend-stack](../standards/frontend-stack.md), [consumer-adoption runbook](../runbooks/consumer-adoption.md).
- PR 순서: [judge-migration-feasibility §3.1 map #2](../plan/design-panel/judge-migration-feasibility.md). 앱 사실: `components/ui/` 30개 파일 목록·`verify-frontend-eslint-config.mjs`가 lint 대상 집합 = `src/**`+`e2e/**` 전수를 단언 — [inv/map §3.1·§8-24](../survey/inventory/kor-travel-map.md); 1차 후보 분류 — [ui §4.1](../survey/cross/ui-components.md).

## 구현 범위

- shim 파일 9~11개: 각 파일 본문을 `export * from "@kor-travel/ui/<name>"`(+ 필요한 `export { default }`)로 교체. 파일 경로·export 이름은 유지해 호출부 import를 바꾸지 않는다.
- `globals.css`에 `@source "../../../node_modules/@kor-travel/ui";`(모노레포 상대 경로는 consumer-adoption 표 기준) 추가.
- `package.json`에 `@kor-travel/ui` 0.1.0(tarball URL + integrity), peer `@kor-travel/tokens` 같은 minor 확인.
- `scripts/verify-frontend-eslint-config.mjs`의 lint 대상 집합 단언에 shim 파일이 포함됨을 확인(집합 규칙이 glob이면 무변경, 명시 목록이면 갱신).
- 매니페스트 `ui{version:"0.1.0"}` 갱신.

## 범위 밖

Button·overlay·Table·DataTable·Checkbox(T-412), `data-slot`/testid 계약 변경(ui-contract 소유), 앱 로컬 패치(우회 패치는 `ui_drift.py`가 탐지, T-211).

## 대상 저장소·브랜치·PR·되돌리기

- `digitie/kor-travel-map`, WSL 체크아웃, 브랜치 `agent/<agent>-T-411-ui-v01`, `origin/main`에서 분기. PR 1개(≤30 파일).
- 되돌리기 = `git revert <merge-sha>` 1회(shim → 원본 파일 복원은 revert에 포함) + `npm ci`.

## 예상 변경 파일

아래는 이 task가 만들거나 고칠 예정 경로다. 예정 경로는 존재·실행 증거가 아니다.

```text
packages/kor-travel-map-admin/frontend/src/components/ui/{badge,badge-variants,skeleton,separator,card,alert,input,textarea,native-select,native-select-option,field,field-variants}.{tsx,ts}
packages/kor-travel-map-admin/frontend/src/app/globals.css        # @source 1줄
packages/kor-travel-map-admin/frontend/package.json
package-lock.json
packages/kor-travel-map-admin/frontend/scripts/verify-frontend-eslint-config.mjs   # 필요 시
packages/kor-travel-map-admin/frontend/kor-travel-common.lock.json
```

## 수용 기준

- [ ] 호출부(`src/app/**`, `src/components/*.tsx`) diff가 0줄이다.
- [ ] Playwright mocked 30 spec green, vitest 42 파일 green, `verify:frontend-eslint` green(lint 대상 집합 단언 통과).
- [ ] `next build`(webpack)·`next build --turbopack` 산출물에 `data-slot="badge"` 등 소형 부품의 클래스가 포함돼 있고, 6폭 스크린샷 diff 0.
- [ ] shim 파일마다 SPDX 헤더와 `Origin:` 행이 있어 map 원본 → common → map shim 경로가 추적된다(D-17).
- [ ] `tools/ui_drift.py`(있으면) report에 map 로컬 패치 0건.

## 검증 명령

```bash
npx --yes npm@12.0.1 ci --workspaces --include=optional --no-audit --no-fund
npm run verify:frontend-eslint && npm run lint -w packages/kor-travel-map-admin/frontend
npm test -w packages/kor-travel-map-admin/frontend
npx playwright test -c packages/kor-travel-map-admin/frontend/playwright.config.ts
npm run build -w packages/kor-travel-map-admin/frontend
git diff --stat origin/main -- packages/kor-travel-map-admin/frontend/src/app   # 0 예상
```

## evidence

PR 본문(테스트 수·빌드 로그·6폭 diff), `consumers.pins.json`·`docs/integration-map.md` 갱신, `docs/journal.md`, 이 파일 "실행 기록".

## rollback·release 차단 조건

- e2e red 또는 시각 diff 원인 불명 → 머지 금지/revert. shim에 로컬 수정이 필요해지면 ui 패키지 patch 릴리스(`ui-v0.1.x`)로 해결하고 앱 패치는 두지 않는다(2회 이상이면 D-28 배포 방식 재검토 트리거).
- 이 PR 머지 전 `ui-v0.1.0` 정식 태그를 "map 검증 완료"로 표기하지 않는다(T-212).
