# T-412 map: ui v0.2 채택(Checkbox 호출부 3파일) + `data-table.test.tsx` 이관 + `ux_lint` report

- 상태: BLOCKED
- 우선순위: P1
- Gate: e2e 30·vitest 42
- 선행: T-213, T-411

## 목표

map admin의 Button·overlay(Dialog·AlertDialog·Popover·Tooltip·Tabs·Breadcrumb·HelpTip)·Table·DataTable·Pager·CopyButton·JsonViewer·DetailList·AdminPageHeader·Form 3종을 `@kor-travel/ui` v0.2.0 shim으로 바꾼다. DataTable은 `manualSorting` 기본 `true` 유지로 호출부 무변경이며, 유일한 시그니처 변경은 native `Checkbox` 호출부 3파일이다. `data-table.test.tsx`(175줄)는 common 패키지 테스트로 옮기고 map에는 통합 스모크만 남긴다.

## 고정 결정

- [design-brief](../plan/design-brief.md) D-09(overlay만 base-ui 1.8, Button 계약, DataTable `manualSorting` 기본 true·`enableSortingRemoval`·`rowTestId`·4상태, Checkbox native `<input>` + `data-slot="checkbox"`)·D-10·D-13(`ux_lint` 금지 7종 + `window.confirm`, map baseline 2건)·D-24(ui PR 상한 30, 초과 시 분할).
- ADR-007·ADR-010 — [ADR 색인](../adr/README.md). 정본: [ui-contract](../standards/ui-contract.md), [ux-guide](../standards/ux-guide.md), [consumer-adoption runbook](../runbooks/consumer-adoption.md).
- PR 순서: [judge-migration-feasibility §3.1 map #3](../plan/design-panel/judge-migration-feasibility.md). 앱 사실: `data-table.tsx` 799행·`"use no memo"` 2곳을 ESLint 검증 스크립트가 단언, `window.confirm` 잔존 2건 — [inv/map §3.1·§8-8](../survey/inventory/kor-travel-map.md), [ui §3.1~3.3](../survey/cross/ui-components.md), [ux §4 C7·C10](../survey/cross/ux-patterns.md).

## 구현 범위

- shim 교체(≤30 파일, 초과 시 "Button·overlay" / "Table·DataTable·Pager" / "Copy·Json·Detail·Header·Form" 3 PR로 분할).
- Checkbox 호출부 3파일: base-ui `Checkbox.Root` props → native `<input type="checkbox">` 계약(`checked`/`onChange`)로 수정.
- `verify-frontend-eslint-config.mjs`의 `"use no memo"` 정확히 2곳 단언을 패키지 이동 후 값(map 로컬 0곳 + VirtualizedTable 1곳 등 실측)으로 갱신.
- `data-table.test.tsx`를 `packages/ui/src/data-table.test.tsx`로 이관(common PR, T-208과 동일 계약), map에는 렌더 스모크 1개 유지.
- `tools/ux_lint.py --base <merge-base>` report를 PR에 첨부. `window.confirm` 2건은 baseline 등록(`ux_gate.baseline`)만 하고 이 PR에서 고치지 않는다.

## 범위 밖

토스트 엔진(sonner, 앱 소유), 인증·프록시, `window.confirm` 2건 제거(별도 앱 task), Next/base-ui 상향(T-413; base-ui 1.6 → 1.8은 ui v0.2 peer가 요구하면 T-413 선행 머지 필요 — 그 경우 이 task는 T-413 뒤로 미룸).

## 대상 저장소·브랜치·PR·되돌리기

- `digitie/kor-travel-map`, WSL 체크아웃, 브랜치 `agent/<agent>-T-412-ui-v02(-part-N)`, `origin/main`에서 분기.
- PR별 `git revert <merge-sha>` 1회로 원복. 분할 PR은 역순으로 revert 가능해야 하므로 PR 간 파일 겹침 0.

## 예상 변경 파일

아래는 이 task가 만들거나 고칠 예정 경로다. 예정 경로는 존재·실행 증거가 아니다.

```text
packages/kor-travel-map-admin/frontend/src/components/ui/{button,button-variants,dialog,alert-dialog,popover,tooltip,tabs,tabs-variants,breadcrumb,checkbox,table,data-table,form-field-input,form-select,form-textarea,form-field,form-field-shared}.{tsx,ts}
packages/kor-travel-map-admin/frontend/src/components/{help-tip,copy-button,json-viewer,detail-list,pagination-bar,admin-shell-parts}.tsx   # 실제 파일명은 착수 시 대조
packages/kor-travel-map-admin/frontend/src/components/ui/data-table.test.tsx      # 삭제 또는 축소
packages/kor-travel-map-admin/frontend/src/**/<Checkbox 호출부 3파일>
packages/kor-travel-map-admin/frontend/scripts/verify-frontend-eslint-config.mjs
packages/kor-travel-map-admin/frontend/kor-travel-common.lock.json                 # ui 0.2.0, ux_gate.baseline
kor-travel-common: packages/ui/src/data-table.test.tsx
```

## 수용 기준

- [ ] Playwright mocked 30 spec·vitest 42 파일(이관분 제외 시 수치 갱신·명시) green; `data-table` 테스트 175줄분이 common 패키지 테스트에서 통과.
- [ ] Checkbox 3파일 외 호출부 diff 0; DataTable 호출부는 `manualSorting` 명시 없이 기존 동작(서버 정렬) 유지가 e2e로 확인된다.
- [ ] `verify:frontend-eslint` 단언(`"use no memo"` 수·inline suppression 0)이 갱신값으로 통과.
- [ ] `ux_lint --base` diff 판정에서 신규 위반 0, 전체 report에 `window.confirm` 2건이 baseline으로 표시.
- [ ] 6폭 스크린샷 diff 0(대화상자 열림 상태 포함 6페이지 이상).

## 검증 명령

```bash
npx --yes npm@12.0.1 ci --workspaces --include=optional --no-audit --no-fund
npm run verify:frontend-eslint && npm test -w packages/kor-travel-map-admin/frontend
npx playwright test -c packages/kor-travel-map-admin/frontend/playwright.config.ts
npm run build -w packages/kor-travel-map-admin/frontend
# kor-travel-common
python3 -B -X utf8 tools/ux_lint.py --root ../kor-travel-map/packages/kor-travel-map-admin/frontend --base origin/main
npm test -w packages/ui    # 이관된 data-table 테스트
```

## evidence

PR 본문(테스트 수 전후 대조표·ux_lint report·6폭 diff), `consumers.pins.json`·`docs/integration-map.md`·`docs/journal.md`, 이 파일 "실행 기록".

## rollback·release 차단 조건

- e2e red·정렬 동작 변화·testid 계약 불일치 중 하나면 머지 금지. 머지 후 발견 시 해당 PR revert.
- 앱 로컬 우회 패치가 필요해지면 `ui-v0.2.x` patch로 해결; 우회 패치 2회 이상은 D-28 재검토 트리거.
