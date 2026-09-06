# T-422 pinvi: ui v0.1/v0.2 채택(`AdminTable` 어댑터 유지·`cn` 재수출·44px 예외 등록·webpack 빌드)

- 상태: BLOCKED
- 우선순위: P1
- Gate: e2e 56·vitest 27
- 선행: T-421, T-213

## 목표

pinvi `apps/web/components/admin/ui/*` 28파일(KTM 이식본)을 `@kor-travel/ui` v0.1(소형)·v0.2(Button·overlay·Table·DataTable 등) shim으로 바꾸고 `lib/admin/cn.ts`를 `@kor-travel/ui/cn` 재수출로 돌린다. `AdminTable` 어댑터(`manualSorting=false`, `mobileCard`, 소비 페이지 36곳)는 유지해 페이지 무변경을 지킨다. 44px 컨트롤 예외 2쪽을 `ux-guide` 예외로 등록한다.

## 고정 결정

- [design-brief](../plan/design-brief.md) D-09(DataTable `manualSorting` 기본 true 유지, pinvi는 `AdminTable`이 `false` 명시; Dialog `hasUnsavedInput`·`viewportProps` 흡수; Checkbox native)·D-10(`@kor-travel/ui/cn` = clsx + `extendTailwindMerge`, webpack·Turbopack 양쪽)·D-13(pinvi admin 44px 2쪽 예외 O-21 = 영구 예외)·D-24(ui PR 상한 30, 2 PR 분할).
- ADR-007·ADR-010 — [ADR 색인](../adr/README.md). 정본: [ui-contract](../standards/ui-contract.md), [ux-guide](../standards/ux-guide.md), [consumer-adoption runbook](../runbooks/consumer-adoption.md).
- 앱 사실: admin ui 28파일(README §6.2 정정), `AdminTable` 어댑터(35~36 페이지), `lib/admin/cn.ts` `extendTailwindMerge` 등록 그룹(`rounded-control/panel`, `h-control/control-sm`, `w-rail`, `text-2xs/md`), e2e 56 mock + 44px 단언, vitest 27, webpack 강제 — [inv/pinvi §3.1·§8-1~5·§9](../survey/inventory/pinvi.md), [ui §2.1·§3.3](../survey/cross/ui-components.md), [ux §4 C6·C10](../survey/cross/ux-patterns.md).
- PR 순서: [judge-migration-feasibility §3.1 pinvi #2·#3](../plan/design-panel/judge-migration-feasibility.md).

## 구현 범위

- PR A(ui v0.1): 소형 15파일(badge·skeleton·separator·card·alert·input·textarea·native-select·field·variants)을 `export * from "@kor-travel/ui/<x>"` shim으로; `lib/admin/cn.ts` → `export { cn } from "@kor-travel/ui/cn"`(pinvi 커스텀 그룹이 common `kt-` 그룹과 다른 이름이면 `extendTailwindMerge` 추가 등록 유지); `@source` 1줄.
- PR B(ui v0.2): Button·overlay 4종·Table·DataTable·Pager·Form 3종·HelpTip·CopyButton(인라인 aria-live 계약 유지 확인)·StatusBadge shim; `AdminTable` 어댑터 무변경; e2e 5파일 testid 계약 대조.
- 44px 예외 2쪽: `apps/web/kor-travel-common.lock.json` `exceptions[]`에 `{rule: UX-G…, surface, reason, until: null, review}` 등록(영구 예외, O-21).
- 각 shim 파일 헤더에 SPDX + `Origin: kor-travel-map …(T-356 이식) → kor-travel-common` 계보 기록(D-17).

## 범위 밖

사용자 표면 `components/ui/*`(Button·Dialog·ConfirmDialog·`useModalDialog`; D-29), `AdminPage` → `AdminPageHeader` 수렴(C16, pinvi 별도 판단), `@config` preset 제거, sonner 도입.

## 대상 저장소·브랜치·PR·되돌리기

- pinvi 정본 체크아웃(Linux), 브랜치 `agent/<agent>-T-422-ui-v01` / `agent/<agent>-T-422-ui-v02`, `origin/main`에서 분기. PR 2개(각 ≤30 파일, 파일 겹침 0).
- 되돌리기 = 각 PR `git revert <merge-sha>` 1회(B → A 역순 가능) + `npm ci`.

## 예상 변경 파일

아래는 이 task가 만들거나 고칠 예정 경로다. 예정 경로는 존재·실행 증거가 아니다.

```text
apps/web/components/admin/ui/*.tsx|ts            # 28파일 → shim
apps/web/lib/admin/cn.ts
apps/web/components/admin/{help-tip,copy-button,pagination-bar,status-badge,status-badge-variants,stat-strip,section-card,empty-state,detail-list,json-viewer,filter-bar}.tsx   # v0.2 범위 내
apps/web/app/globals.css                          # @source
apps/web/package.json, package-lock.json
apps/web/kor-travel-common.lock.json              # ui.version, exceptions[]
```

## 수용 기준

- [ ] e2e 56 mock 전부 green(44px 단언 2쪽 포함), vitest 27 green, `next build --webpack` green.
- [ ] `apps/web/app/(admin)/**` 페이지 소스 diff 0, `AdminTable.tsx` diff 0.
- [ ] 정렬 동작: `AdminTable` 경유 페이지는 클라이언트 정렬 유지, 직접 `DataTable` 사용처(있다면)는 서버 정렬 유지 — e2e 또는 수동 기록.
- [ ] ESLint 경계 규칙(`no-restricted-imports`)이 admin shim → `@kor-travel/ui`를 허용하고 사용자 표면에서는 여전히 차단한다(테스트 import 1건으로 lint 실패 확인 후 제거).
- [ ] `tools/ui_drift.py` report에 pinvi 로컬 패치 0건; 44px 예외가 매니페스트에 등록돼 `ux_lint`가 예외로 인식.
- [ ] 6폭 admin 스크린샷 diff 0(대화상자 열림 상태 포함).

## 검증 명령

```bash
npm ci --no-audit --no-fund && npm run lint --workspaces && npm run typecheck --workspaces
npm run test -w apps/web && npm run build -w apps/web
npx playwright test -c apps/web/playwright.config.ts
# kor-travel-common
python3 -B -X utf8 tools/ux_lint.py --root ../pinvi/apps/web --base origin/main --manifest ../pinvi/apps/web/kor-travel-common.lock.json
python3 -B -X utf8 tools/ui_drift.py --root ../pinvi/apps/web
```

## evidence

PR 본문 2개(e2e·vitest 수, 빌드 로그, 6폭 diff, 경계 lint 확인), `consumers.pins.json`·`docs/integration-map.md`·`docs/journal.md`, 이 파일 "실행 기록".

## rollback·release 차단 조건

- e2e red·testid 계약 불일치·webpack 빌드 실패 중 하나면 머지 금지, 머지 후 발견 시 해당 PR revert.
- 우회 패치가 필요하면 `ui-v0.x.y` patch로; 2회 이상이면 D-28 배포 방식 재검토.
