# T-463 weather: 셸/패널·표/폼·로그인 → common 컴포넌트 3분할 PR, 해당 CSS 절 삭제

- 상태: BLOCKED
- 우선순위: P1
- Gate: 시각 diff·vitest
- 선행: T-462, T-213

## 목표

weather admin의 손수 CSS 중 common 부품으로 대체 가능한 40~48%(약 1,000~1,190행)를 3개 PR로 교체한다: (A) 셸(`admin-shell.tsx` rail·PageHeader·skip-link → `AdminRailGrid`·`AdminPageHeader`·`AdminSkipLink`), (B) 패널·표(`.panel`·`.table-wrap`·`.status`·`.toolbar`·`.pagination` → `SectionCard`·`Table`·`DataTable`·`StatusBadge`·`FilterBar`·`OffsetPager`), (C) 폼·로그인(`.field`·`.button.*`·로그인 카드 → `Field`·`FormFieldInput`·`Button`·로그인 템플릿). 각 PR은 교체한 CSS 절을 삭제하고 그 화면의 6폭 diff를 "의도된 변경 0"으로 증명한다.

## 고정 결정

- [design-brief](../plan/design-brief.md) D-08 ⑥(ui v0.2 후 셸·패널·폼·로그인 3분할 PR)·D-09(Button·DataTable 계약)·D-10(`@source`, `kt-` 유틸리티)·D-13(C2 rail 접힘 4rem·셸 전환 1024, C15 로그인 타이포 워드마크, C16 pathname 대신 breadcrumb — 이 단계에서 셸 규약이 적용되므로 "diff 0"이 아니라 "규약 적용 diff만")·D-24(각 ≤30 파일).
- ADR-007·ADR-012 — [ADR 색인](../adr/README.md). 정본: [ui-contract](../standards/ui-contract.md), [ux-guide](../standards/ux-guide.md), [responsive-web](../standards/responsive-web.md).
- 사실: `globals.css` 절 표(shell 244–536, data surfaces 537–744, cards 745–914, forms 1377–1648, login 1789–1889, 모션 1890–1909, responsive 1910–2142), `admin-shell.tsx` 152행(README §6.2 정정), `PageHeader` 슬롯 section/path/title/actions/description, 로그인 "same as kor-travel-geo", `.status.on/off/warn` raw, `window.confirm` 1건, vitest 4개(순수 함수) — [inv/weather §3.1·§8-5~8·§9.1](../survey/inventory/kor-travel-weather.md), [ux §1.1·§1.8·§4 C2·C9·C15·C16](../survey/cross/ux-patterns.md).
- PR 순서: [judge-migration-feasibility §3.1 weather #4~6](../plan/design-panel/judge-migration-feasibility.md).

## 구현 범위

- 공통: `@kor-travel/ui` 0.2.x 의존 + `@source "../node_modules/@kor-travel/ui"`; 각 PR에서 교체 대상 TSX의 className을 common 부품/`kt-` 유틸리티로 바꾸고 대응 CSS 절 삭제; `statusLabel()` 사전(5-tone) 도입으로 `.status.on/off/warn` 대체(C9).
- PR A 셸: rail 접힘(4rem, localStorage)·1024 전환·breadcrumb 도입은 규약 적용 diff로 허용하되 목록·상세 콘텐츠 영역 diff 0. `design.md`의 16rem/접힘 서술과 코드를 일치시키는 것은 T-464.
- PR B 패널·표: 목록 4화면(datasets·sync-runs·weather·admin/dagster)의 표를 `DataTable`(서버 정렬 여부는 API 계약 확인 후 `manualSorting` 명시) 또는 `Table`로; 페이지네이션 `OffsetPager`.
- PR C 폼·로그인: `settings/providers`·`location-admin` 폼과 `LoginForm.tsx`; 로그인은 타이포 워드마크(C15) 적용, `window.confirm` 1건은 `AlertDialog` + 동사 라벨로 교체(C7).
- 각 PR에 컴포넌트 렌더 vitest 최소 1개씩 추가(현재 컴포넌트 테스트 0).

## 범위 밖

preflight·도메인 CSS(workbench·Dagster·마커, T-464), 지도 뷰(`vworld-map-view`, 공유 라이브러리 소관), 앱별 인증 로직·사용자 저장소·IdP 왕복, API 타입 생성기 도입. 로그인 UI는 common 위젯 계약과 앱 어댑터를 사용한다.

## 대상 저장소·브랜치·PR·되돌리기

- `digitie/kor-travel-weather`, 브랜치 `feat/T-463-shell` / `-panels-tables` / `-forms-login`, `origin/main`에서 순차 분기, Draft PR. PR 3개(각 ≤30 파일, 겹침 0).
- 되돌리기 = 각 PR `git revert` 1회, 역순(C → B → A). CSS 절 삭제가 revert로 복원된다.

## 예상 변경 파일

아래는 이 task가 만들거나 고칠 예정 경로다. 예정 경로는 존재·실행 증거가 아니다.

```text
packages/kor-travel-weather-admin/frontend/components/admin-shell.tsx, components/auth/LoginForm.tsx
packages/kor-travel-weather-admin/frontend/app/{page,datasets,sync-runs,weather,admin/dagster,settings/providers}/*.tsx
packages/kor-travel-weather-admin/frontend/components/{location-admin,weather-map}.tsx   # 클래스 교체 범위 내
packages/kor-travel-weather-admin/frontend/lib/status-label.ts                            # 신규
packages/kor-travel-weather-admin/frontend/app/globals.css                                # 절 삭제
packages/kor-travel-weather-admin/frontend/tests/*.test.tsx                               # 신규 렌더 테스트
packages/kor-travel-weather-admin/frontend/package.json, package-lock.json, kor-travel-common.lock.json
```

## 수용 기준

- [ ] PR마다 6폭 전후 캡처가 있고, 교체 화면 외 영역 diff 0; 교체 화면의 diff는 PR 본문에서 규약 항목(UX-Gn.m)별로 설명된다. 320~768px 컨테인·가로 스크롤 0.
- [ ] 삭제한 CSS 절의 행 범위와 삭제 후 `globals.css` 행 수를 PR 본문에 기록(누적 목표: shell·data surfaces·cards·forms 공통·login·모션 ≈ 1,000행 이상 삭제).
- [ ] vitest: 기존 4 + 신규 렌더 테스트 ≥3 green; `ux_lint --base` 신규 위반 0, `window.confirm` 0건(PR C 후).
- [ ] CI frontend job green, `next build` webpack·Turbopack 양쪽.
- [ ] `tools/ui_drift.py` 로컬 패치 0건.

## 검증 명령

```bash
# kor-travel-weather/packages/kor-travel-weather-admin/frontend
npm ci --ignore-scripts && npm run lint && npm run type-check && npm test && npm run build
wc -l app/globals.css && grep -c 'window.confirm' -r app components lib
BASELINE_APP=weather BASELINE_URL=http://127.0.0.1:14105 npx playwright test -c ../../../../kor-travel-common/templates/playwright.baseline.ts
# kor-travel-common
python3 -B -X utf8 tools/ux_lint.py --root ../kor-travel-weather/packages/kor-travel-weather-admin/frontend --base origin/main
python3 -B -X utf8 tools/ui_drift.py --root ../kor-travel-weather/packages/kor-travel-weather-admin/frontend
```

## evidence

PR 3개 본문(전후 캡처·삭제 행 범위·테스트 수), `consumers.pins.json`·`docs/integration-map.md`·`docs/journal.md`, 이 파일 "실행 기록".

## rollback·release 차단 조건

- 교체 화면 외 diff·가로 스크롤 발생·규약 외 diff 설명 불가 → 해당 PR revert(D-08).
- ui v0.2 부품 계약이 weather 요구(예: `PageHeader` description 슬롯)를 못 채우면 앱 패치 대신 `ui-contract` 이관 절 + `ui-v0.2.x` patch로 해결.
