# T-444 geo: radix→base-ui 이관(12파일·`asChild` 17곳) + ui v0.2 채택(셀렉터 diff evidence; VirtualTable 잔류)

- 상태: BLOCKED
- 우선순위: P2
- Gate: e2e·a11y 4 spec
- 선행: T-443, T-441, T-213

## 목표

geo-ui의 radix 기반 프리미티브 12파일(`asChild` 17곳)을 `@kor-travel/ui` v0.2(overlay = base-ui 1.8 `render`, 비-overlay = native + `useRender`)로 바꾸고 소형 세트도 shim으로 채택한다. `Panel`(`section.panel .panel-header h2`)·`JsonBlock`(`pre.json-box`)·`StatusBadge`(`span.status`) 같은 e2e DOM 계약은 셀렉터 diff evidence로 무변경을 증명한 뒤에만 common 부품으로 바꾼다. `VirtualTable`은 잔류.

## 고정 결정

- [design-brief](../plan/design-brief.md) D-09(overlay만 base-ui, 비-overlay native + `useRender`, DataTable에 `rowHeader`·검색 툴바 미포함 → geo VirtualTable 잔류)·D-10(마크업 계약 = `ui-contract.md`, geo e2e 셀렉터 대응)·D-24(≤30 파일, 분할).
- ADR-007 — [ADR 색인](../adr/README.md). 정본: [ui-contract](../standards/ui-contract.md)(geo 셀렉터 대응 절), [consumer-adoption runbook](../runbooks/consumer-adoption.md).
- 사실: radix-ui 1.6.0(121 하위), 12파일 재작성·`asChild` 17곳, `Button` forwardRef+Slot, `useModalA11y`, Toast(radix+zustand), e2e 셀렉터 계약, a11y spec 4개 — [inv/geo §3.1·§8-3~13·§9](../survey/inventory/kor-travel-geo.md), [ui §5.2·§5.4](../survey/cross/ui-components.md).
- PR 순서: [judge-migration-feasibility §3.1 geo #4](../plan/design-panel/judge-migration-feasibility.md)(`Panel`→`SectionCard`는 셀렉터 diff evidence 후에만).

## 구현 범위

- PR A(소형 shim + Button): badge·input·native-select·field·label·checkbox·card → `@kor-travel/ui` shim(파일 경로 유지), `Button`은 `asChild` 호출부 17곳을 `render` prop으로 치환; `@source` 1줄; radix `Slot` 의존 제거.
- PR B(overlay): Dialog·AlertDialog·Popover·Tooltip·Tabs → base-ui 1.8 기반 common overlay shim; `useModalA11y`는 common Dialog가 포커스 트랩·복귀·Escape를 제공하므로 호출부에서 제거하되 drawer(`AppShell`)용은 잔류; `ConfirmActionDialog`·`TypedConfirmField`는 앱 유지.
- PR C(계약 부품, 조건부): `Panel`·`JsonBlock`·`StatusBadge`·`EmptyState`·`HelpTip`을 common 부품으로 바꾸기 전 렌더 DOM 셀렉터 diff(`section.panel .panel-header h2`, `pre.json-box`, `span.status`)를 evidence로 남기고, diff 0인 부품만 교체. diff가 있으면 앱 잔류 + `ui-contract` 이관 절 요청.
- radix-ui 패키지 제거는 사용처 0 확인 후 PR B 또는 별도 커밋. Toast는 앱 소유 유지(D-09).

## 범위 밖

`VirtualTable`(잔류, T-508 재평가), 토스트 엔진 교체, AppShell 셸 자체 교체, 세션·프록시, 다크.

## 대상 저장소·브랜치·PR·되돌리기

- `digitie/kor-travel-geo`, 브랜치 `agent/<agent>-T-444-ui-a|b|c`, `origin/main`에서 순차 분기. PR 3개(각 ≤30 파일, 겹침 0).
- 되돌리기 = 각 PR `git revert` 1회, 역순. PR B revert 시 radix 의존이 복원돼야 하므로 radix 제거 커밋은 PR B 안에 둔다.

## 예상 변경 파일

아래는 이 task가 만들거나 고칠 예정 경로다. 예정 경로는 존재·실행 증거가 아니다.

```text
kor-travel-geo-ui/components/ui/{button,button-variants,badge,badge-variants,input,native-select,field,label,checkbox,card,dialog,alert-dialog,popover,tooltip,tabs}.tsx|ts
kor-travel-geo-ui/components/ui/{Panel,JsonBlock}.tsx, components/admin/shared/{EmptyState,HelpTip,StatusBadge,...}.tsx   # PR C 조건부
kor-travel-geo-ui/<asChild 호출부 17곳>
kor-travel-geo-ui/lib/use-modal-a11y.ts                # drawer 전용으로 축소
kor-travel-geo-ui/app/globals.css                      # @source
kor-travel-geo-ui/package.json, package-lock.json      # radix-ui 제거, @kor-travel/ui
kor-travel-geo-ui/kor-travel-common.lock.json
```

## 수용 기준

- [ ] PR마다 e2e 23 spec + a11y 4 spec green, unit 43 파일 green(이관·삭제된 테스트 수 명시), `next build` green.
- [ ] `grep -rn 'asChild\|@radix-ui\|radix-ui' kor-travel-geo-ui/{app,components,lib}` 0건(PR B 후).
- [ ] PR C: 교체한 부품마다 전후 DOM 셀렉터 diff 표(`section.panel .panel-header h2` 등 3계약 + 해당 e2e spec 이름)가 있고 diff 0; 교체하지 않은 부품은 사유 기록.
- [ ] 포커스 트랩·복귀·Escape 동작이 a11y spec 또는 `app-shell-drawer.test.tsx`로 유지 확인.
- [ ] 6폭 스크린샷 diff 0(모달·팝오버 열림 상태 포함), `tools/ui_drift.py` 로컬 패치 0건.

## 검증 명령

```bash
# kor-travel-geo/kor-travel-geo-ui (Linux)
npm ci && npm run lint && npm run type-check && npm test && npm run build
PLAYWRIGHT_MOCK_LOGIN=1 npm run test:e2e -- tests/e2e/*-a11y.spec.ts && PLAYWRIGHT_MOCK_LOGIN=1 npm run test:e2e
grep -rn 'asChild\|radix-ui' app components lib | wc -l
# kor-travel-common
python3 -B -X utf8 tools/ui_drift.py --root ../kor-travel-geo/kor-travel-geo-ui
python3 -B -X utf8 tools/ux_lint.py --root ../kor-travel-geo/kor-travel-geo-ui --base origin/main
```

## evidence

PR 3개 본문(셀렉터 diff 표·테스트 수·6폭 diff), `consumers.pins.json`·`docs/integration-map.md`·`docs/journal.md`, 이 파일 "실행 기록".

## rollback·release 차단 조건

- 셀렉터 diff evidence 없이 PR C 부품을 교체하면 머지 금지. e2e red면 해당 PR revert.
- T-443(React 19) 미머지 상태에서는 `@kor-travel/ui` peer가 맞지 않아 PR A를 열지 않는다.
