# T-454 concierge: ui v0.2 채택(18종 shim·base-ui 1.8·`render` 9줄)

- 상태: BLOCKED
- 우선순위: P2
- Gate: e2e 45
- 선행: T-021, T-453, T-213
- 외부 선행: T-021 common 결정 완료(2026-09-08); concierge 루트 LICENSE·metadata·고지의 외부 PR evidence

## 목표

concierge의 shadcn `base-nova` 프리미티브 18종(`frontend/src/components/ui/*`)을 `@kor-travel/ui` v0.2 shim으로 바꾸고 `@base-ui/react`를 1.5 → 1.8로, `@hookform/resolvers` 3 → 5로 올린다. base-ui `render` prop 관용구 차이 9줄만 호출부에서 수정한다. `AppShell`·`panels.tsx`·`ConfirmActionButton`은 이번 범위 밖(앱 잔류, B4 diff 결과에 따라 후속).

## 고정 결정

- [design-brief](../plan/design-brief.md) D-09(overlay base-ui 1.8, Button 계약 = concierge 계약과 동일 계보, `render` 합성)·D-06(base-ui floor 1.6·ktc 1.5는 채택 PR에서 상향; resolvers 5)·D-16(ktc 3차, L8 후)·D-17(B4: ktc `AppShell`·`globals.css` 복사 여부 diff 후, MIT 원천 고지 보존)·D-24(≤30 파일).
- ADR-007·ADR-004 — [ADR 색인](../adr/README.md). 정본: [ui-contract](../standards/ui-contract.md), [licensing](../standards/licensing.md), [consumer-adoption runbook](../runbooks/consumer-adoption.md).
- 사실: 18종 `base-nova`(map과 동일 계보, "최신 기준 레포" 주석), Button `loading`·`disabledReason`·`blockBusyActivation` 계약이 map과 동일, `shadcn` CLI가 dependencies, E2E 셀렉터가 base-ui DOM 계약에 결합(ADR-34), RHF·zod 사용, `data-table`/`tooltip`/`skeleton` 없음 — [inv/ktc §3.1·§8-2·§8-3·§9](../survey/inventory/kor-travel-concierge.md), [ui §2.1·§3.1](../survey/cross/ui-components.md), [lic §4 B4](../survey/cross/licensing.md).
- PR 순서: [judge-migration-feasibility §3.1 concierge #5](../plan/design-panel/judge-migration-feasibility.md).

## 구현 범위

- `components/ui/*` 18파일 → `export * from "@kor-travel/ui/<x>"` shim(경로 유지), `@source` 1줄, `@base-ui/react` 1.8.0·`@hookform/resolvers` 5.x·`shadcn` CLI devDependencies 이동, lock 동반.
- `render` 관용구 9줄 수정(파일·줄은 착수 시 `grep -n 'render=' src` 로 확정해 PR에 표기).
- Form: common `Field`·`FormFieldInput`은 헤드리스 검증과 RHF 양쪽을 수용해야 하므로(D-09 form-validation 헤드리스), RHF 사용처는 `Field` 래퍼만 교체하고 `register`/`Controller` 흐름은 유지.
- shim 헤더 SPDX + `Origin:`(shadcn MIT 고지 보존, B6).
- 매니페스트 `ui{version:"0.2.0"}`, `ux_lint --base` report 첨부.

## 범위 밖

`AppShell`(B4 diff 판정 후 별도), `panels.tsx`·`StatStrip`·`SectionCard`·`HelpTip`·`CopyButton` 교체(2차, T-508 재평가 항목 아님 — 후속 ktc task), `ReviewWorkspace.tsx`, maplibre-gl 6 → 5, `useIsMobile` 767px 조정(C3 후속).

## 대상 저장소·브랜치·PR·되돌리기

- `digitie/kor-travel-concierge`, Linux/WSL2, 브랜치 `agent/<agent>-T-454-ui-v02`, `origin/main`에서 분기. PR 1개(≤30 파일; 초과 시 "shim" / "base-ui 1.8 + render 9줄" 2 PR).
- 되돌리기 = `git revert <merge-sha>` + `npm ci`(base-ui 1.5 복원 포함).

## 예상 변경 파일

아래는 이 task가 만들거나 고칠 예정 경로다. 예정 경로는 존재·실행 증거가 아니다.

```text
frontend/src/components/ui/*.tsx            # 18종 shim
frontend/src/**/<render 관용구 9줄 파일>
frontend/src/app/globals.css                # @source
frontend/package.json, frontend/package-lock.json
frontend/kor-travel-common.lock.json
```

## 수용 기준

- [ ] Playwright 45 test green(base-ui DOM 계약 결합 스펙 포함; 실패 스펙은 ui-contract 이관 절로 해결하고 앱 로컬 패치 금지), `node-quality` green.
- [ ] `npm ls @base-ui/react @hookform/resolvers`가 1.8.x / 5.x 단일이고 peer 경고 0.
- [ ] 6폭 스크린샷 diff 0(대시보드·목록·모달·폼 오류 상태).
- [ ] `grep -rn 'render=' src | wc -l` 변경분이 9줄 이내로 PR 본문 표와 일치.
- [ ] L8 외부 LICENSE evidence(T-454 PR 링크·루트 LICENSE) 확인, `tools/ui_drift.py` 로컬 패치 0건, `ux_lint --base` 신규 위반 0.

## 검증 명령

```bash
# kor-travel-concierge (Linux/WSL2)
cd frontend && npm ci && npm ls @base-ui/react @hookform/resolvers --depth=0 && npm run lint && npx tsc --noEmit && npm run build
cd ../tests && npx playwright test
# kor-travel-common
python3 -B -X utf8 tools/ui_drift.py --root ../kor-travel-concierge/frontend
python3 -B -X utf8 tools/ux_lint.py --root ../kor-travel-concierge/frontend --base origin/main
python3 -B -X utf8 tools/check_versions.py --manifest ../kor-travel-concierge/frontend/kor-travel-common.lock.json
```

## evidence

PR 본문(e2e 수·peer 검사·render 9줄 표·6폭 diff·L8 링크), `consumers.pins.json`·`docs/integration-map.md`·`docs/journal.md`, 이 파일 "실행 기록".

## rollback·release 차단 조건

- T-021 결정 또는 L8 외부 LICENSE evidence가 없으면 PR을 열지 않는다(B9). e2e red·peer 경고면 머지 금지, 머지 후 회귀 시 revert 1회.
- 우회 패치 필요 시 `ui-v0.2.x` patch; 2회 이상은 D-28 재검토.
