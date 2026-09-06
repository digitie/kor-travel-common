# T-203 ui 1차 소형 13종(Badge·Skeleton·Separator·Card·Alert·Input·Textarea·NativeSelect·Field·EmptyState·SectionCard·FilterBar·StatStrip) + 단위 테스트(vitest+RTL+jsdom)

- 상태: BLOCKED
- 우선순위: P0
- Gate: 단위 테스트·tarball
- 선행: T-201

## 목표

ui `v0.1.0`의 내용물을 만든다. 13종은 조사에서 "두 앱 이상 props 계약 일치 또는 색 토큰 치환만으로 갈라짐 · 프리미티브 엔진 비의존 · 도메인 import 없음" 기준을 통과한 1차 후보다([ui-components](../survey/cross/ui-components.md) §4.1). map 원본(GPL)을 정본으로 옮기고 pinvi 확장은 코드 복사 없이 prop 계약으로 재구현한다.

## 고정 결정

- ADR-007([ADR 색인](../adr/README.md)); [브리프](../plan/design-brief.md) D-09(비-overlay는 native 요소 + `useRender`로 `render` 합성 선택 지원)·D-10(`kt-` 접두 유틸리티만)·D-16(1차 소비자 map + pinvi admin, 대체 airport 소형 부품)·D-17(추출 규칙: map 원천 그대로, pinvi는 L6 전 추출 금지 B1, shadcn 생성물 MIT 고지 B6)·D-20(airport 1차 = 소형 부품).
- 규칙 정본: [ui-contract](../standards/ui-contract.md)(data-slot·testid; T-204 확정), [ux-guide](../standards/ux-guide.md) UX-G2.1(FilterBar 툴바)·G3.1(SectionCard 1층·`headingLevel`)·G4.4(EmptyState 좌정렬)·G4.5(Skeleton `aria-hidden` + 영역 `aria-busy`)·G5.6(값 없음 `—`, 로딩 중 가짜 0 금지)·G9.5(한글 `uppercase` 금지), [design-tokens](../standards/design-tokens.md).
- 사실 근거: [ui-components](../survey/cross/ui-components.md) §2.1(27쌍 정규화 diff; Badge `render` prop, Separator·Input native 대체, Field 11 서브컴포넌트·`FieldMessage`, Card 서브 7종 동일), §2.2(EmptyState·SectionCard·StatStrip·FilterBar props), §3.4, §4.1(소비처 계수); [commonality-matrix](../survey/commonality-matrix.md) §2.2; [map 인벤토리](../survey/inventory/kor-travel-map.md) §8-7·§8-10; [pinvi 인벤토리](../survey/inventory/pinvi.md) §8-1·§8-2.
- 이 task에서 확정하고 T-204가 문서화하는 계약: Badge·Input·Textarea·NativeSelect·Separator는 `useRender`로 `render` 합성 지원(map·concierge 호출부 유지; pinvi식 `<a className={badgeVariants()}>`도 계속 가능). Alert는 `AlertActions` 포함, Field는 `FieldMessage` 포함(map 계열). StatStrip `tone`은 `StatusTone`(success/warning/destructive/info/neutral; ktdm `ok/warn/danger`는 앱 alias). SectionCard `headingLevel` 기본 2. EmptyState `framed`/`size` 유지. Badge variant 축은 map 10종(geo `tone` 축은 geo 측 매핑).

## 구현 범위

- 13 컴포넌트 각각 `src/<name>.tsx`(+ 필요 시 `<name>-variants.ts` cva 레시피) + `src/<name>.test.tsx`, `package.json` `exports`에 `./<name>` 추가. `'use client'`는 이벤트·hook을 쓰는 파일에만 둔다.
- 공유 타입 `src/status-tone.ts`(`StatusTone`, `STATUS_TONES`) — T-208 DataTable·T-209 StatusBadge가 재사용.
- 모든 클래스는 `kt-` 접두 유틸리티(`bg-kt-surface-card`, `h-kt-control`, `rounded-kt-control`, `text-kt-2xs`)와 레이아웃 유틸만. raw 색·radius·px 값 0.
- 파일 헤더: SPDX + `Origin: kor-travel-map@c494e227 packages/kor-travel-map-admin/frontend/src/components/<path> (GPL-3.0-or-later)` + `Derived-From: shadcn/ui (MIT)`(해당 파일만) + `Modified:`. Hallmark 스탬프는 두지 않는다(D-13).
- 테스트: 렌더·`data-slot`·접근성 role·`render` 합성·kt 클래스 존재를 13종 모두, axe(opt-in) 기본 렌더 13종.
- 스모크 앱(T-201)에 13종을 각 1회 렌더하는 페이지 추가.

## 범위 밖

- Button·AppErrorPanel(T-205), HelpTip·overlay(T-206), DataTable(T-208), StatusBadge(T-209), Form 3종(T-210).
- pinvi `AdminPage`/`Section`/`FilterBar` 어댑터와 geo `Panel`→`SectionCard` 셀렉터 대응(앱 이관 task; geo는 셀렉터 diff evidence 후에만).
- 토스트, concierge 전용 `Select`·`Switch`·`Label`, geo 전용 `Collapsible`·`Progress`.

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다.

```text
packages/ui/src/{badge,skeleton,separator,card,alert,input,textarea,native-select,field,empty-state,section-card,filter-bar,stat-strip}.tsx
packages/ui/src/{badge,button,field}-variants.ts   (button-variants는 레시피만, Button 본체는 T-205)
packages/ui/src/status-tone.ts
packages/ui/src/*.test.tsx
packages/ui/package.json  (exports 13 subpath)
packages/ui/smoke/next-app/app/small/page.tsx
PROVENANCE.md  (map 원천 커밋·경로 13행)
```

## 수용 기준

- 13 subpath가 빌드·`npm pack`·스모크 앱 `next build --webpack`/`next build`까지 통과.
- vitest 실패 0, skip 0(skip·0 test를 pass로 집계하지 않음), 파일당 최소 3 케이스.
- axe: 13종 기본 렌더 위반 0.
- Skeleton `aria-hidden="true"`; Separator `role="separator"` + `aria-orientation`; NativeSelect는 native `<select>`이며 `FormData`에 값이 실린다; StatStrip은 `value == null`이면 `—`, `loading` 중 숫자 0을 렌더하지 않고 단위는 값이 있을 때만; EmptyState 기본 좌정렬.
- `render={<a href="…" />}` 합성 시 요소가 교체되고 className이 병합된다(Badge·Input·Separator 각 1 케이스).
- `check-kt-classes.mjs` 위반 0, `check-directives.mjs` 불일치 0.
- map 원본 대비 markup 변경(요소·속성·data-slot)이 파일별 `Modified:` 행에 요약되어 있고 `PROVENANCE.md`에 원천 커밋·경로가 있다.

## 검증 명령

```bash
npm run build -w packages/ui && npm run test -w packages/ui
node packages/ui/scripts/check-kt-classes.mjs && node packages/ui/scripts/check-directives.mjs
npx tsc --noEmit -p packages/ui
npm pack -w packages/ui --pack-destination /tmp/kt-ui
cd packages/ui/smoke/next-app && npm install /tmp/kt-ui/kor-travel-ui-*.tgz && npx next build --webpack && npx next build
python3 -B -X utf8 tools/ux_lint.py packages/ui/src
```

## evidence

PR 본문과 `docs/journal.md`에 vitest 테스트 수·exit code, axe 결과, tarball 파일 목록·sha256, 스모크 빌드 로그, `ux_lint` report를 남긴다. `ux_lint`(T-103)가 아직 없으면 `NOT_RUN(T-103 미완료)`.

## rollback 또는 release 차단 조건

- 컴포넌트 단위 revert가 가능하도록 컴포넌트당 커밋을 분리한다.
- 차단: 어느 컴포넌트든 테스트 실패·axe 위반·kt 클래스 위반, 원천 미기록 파일, pinvi 코드 복사 흔적. 하나라도 남으면 T-212 rc를 만들지 않는다.
