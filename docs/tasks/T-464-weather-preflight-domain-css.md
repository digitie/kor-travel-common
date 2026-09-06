# T-464 weather: preflight 활성화 + 잔존 도메인 CSS `@layer components` + 마커 색 토큰화 + 셸 문서-코드 불일치 해소

- 상태: BLOCKED
- 우선순위: P2
- Gate: 시각 diff
- 선행: T-463

## 목표

weather Tailwind v4 전환의 마지막 단계다. `@import "tailwindcss/preflight"`(또는 `tailwindcss` 전체)를 활성화해 base reset 243행을 삭제하고, 잔존 도메인 CSS(workbench 915–1376, Dagster 1649–1788, markers/clusters 2143–2335, 약 800행)를 `@layer components`로 옮기며, 하드코딩 마커 색 23곳을 `--weather-marker-*` 도메인 토큰으로 승격한다. `design.md`(16rem·접힘)와 코드(17rem·접힘 없음)의 셸 불일치는 T-463 PR A에서 규약(4rem 접힘·16rem 또는 22rem `--kt-rail`)으로 코드가 바뀌었으므로 문서를 코드에 맞춘다.

## 고정 결정

- [design-brief](../plan/design-brief.md) D-08 ⑥(마지막 = preflight 활성화 + 잔존 도메인 CSS `@layer components`)·D-12(마커 팔레트는 common 소유 아님, 규칙만; 앱 도메인 토큰은 앱 파일)·D-26·D-13(rail 접힘 4rem, `--rail` 22rem 기본)·D-32(`design.md` 본문 한국어 — wx 이행 대상).
- ADR-012 — [ADR 색인](../adr/README.md). 정본: [design-tokens](../standards/design-tokens.md), [ux-guide](../standards/ux-guide.md)(마커 16슬롯·라벨 대비 규칙), [responsive-web](../standards/responsive-web.md).
- 사실: base reset 1–243행, bare element 23종(전역 `button`/`table`/`a` 의존 → preflight 후 무스타일 위험, 13 TSX 전수 확인 필요), 마커 색 하드코딩 23곳, `design.md`(영어, 16rem·접힘·localStorage) vs `tokens.css` 17rem vs 코드 접힘 없음 — [inv/weather §3.1·§9·§9.1](../survey/inventory/kor-travel-weather.md), [ux §4 C2](../survey/cross/ux-patterns.md).
- PR 순서: [judge-migration-feasibility §3.1 weather #7](../plan/design-panel/judge-migration-feasibility.md).

## 구현 범위

- PR 1(preflight): `globals.css` 헤더를 `@import "tailwindcss" source(none);` + 명시 `@source`로 바꾸고 base reset 절 삭제. 13 TSX 전수에서 bare element 의존(`button`·`table`·`a`·`h1~h6`·`ul`)을 확인해 필요한 곳만 `kt-` 유틸리티 또는 `@layer base` 최소 규칙으로 보전. 6폭 diff 0 목표(불가피한 preflight 차이는 항목별 근거).
- PR 2(도메인 CSS): workbench·Dagster·markers/clusters 절을 `@layer components { … }`로 감싸고 클래스명은 유지; 마커 색 23곳을 `app/markers.css`의 `--weather-marker-<name>` 토큰으로 승격(값 무변경, 라벨 대비 규칙은 ux-guide 검사 대상).
- PR 3(문서): `design.md`를 한국어로 이행하고 셸 서술(rail 폭·접힘·breakpoint 1024)을 코드와 일치시킴; `docs/architecture/admin-ui.md`의 62rem 서술 갱신.

## 범위 밖

지도 스타일 빌더(`vworld-style.ts` 중복은 T-505), 마커 hex 정본 확정(O-13), 사용자 표면, Python.

## 대상 저장소·브랜치·PR·되돌리기

- `digitie/kor-travel-weather`, 브랜치 `feat/T-464-preflight` / `-domain-css` / `docs/T-464-design-md`, `origin/main`에서 순차 분기, Draft PR. PR 3개.
- 되돌리기 = 각 PR `git revert` 1회, 역순. PR 1 revert 시 base reset 243행이 복원된다.

## 예상 변경 파일

아래는 이 task가 만들거나 고칠 예정 경로다. 예정 경로는 존재·실행 증거가 아니다.

```text
packages/kor-travel-weather-admin/frontend/app/globals.css
packages/kor-travel-weather-admin/frontend/app/markers.css            # 신규 도메인 토큰
packages/kor-travel-weather-admin/frontend/components/{weather-map,vworld-map-view}.tsx, lib/weather-clusters.ts   # 마커 색 참조
packages/kor-travel-weather-admin/frontend/<bare element 의존 TSX 일부>
packages/kor-travel-weather-admin/frontend/design.md
docs/architecture/admin-ui.md
```

## 수용 기준

- [ ] PR 1: 빌드 CSS에 preflight 시그니처 존재, base reset 절 0행, 6폭 diff 0(예외 항목은 PR 본문 표: 요소·차이·근거).
- [ ] PR 2: `globals.css`에 unlayered 도메인 규칙 0(전부 `@layer components` 또는 삭제), 마커 하드코딩 색 0건(`grep -nE '#[0-9a-f]{3,8}|rgba?\(' components lib app --include=*.tsx --include=*.ts` 결과가 토큰 파일 밖에서 0), 마커 렌더 diff 0.
- [ ] PR 3: `design.md` 한국어, rail·breakpoint 서술이 코드와 같고 `validate_document_links.py` 임시 실행 0 오류.
- [ ] `ux_lint` 전체 report에서 raw hex/oklch 위반이 baseline 대비 감소(수치 기록), 신규 위반 0.
- [ ] CI frontend job green, vitest green.

## 검증 명령

```bash
# kor-travel-weather/packages/kor-travel-weather-admin/frontend
npm ci --ignore-scripts && npm run lint && npm run type-check && npm test && npm run build
grep -nE '#[0-9a-fA-F]{3,8}\b|rgba?\(' components lib app --include=*.tsx --include=*.ts | grep -v markers.css | wc -l
BASELINE_APP=weather BASELINE_URL=http://127.0.0.1:14105 npx playwright test -c ../../../../kor-travel-common/templates/playwright.baseline.ts
# kor-travel-common
python3 -B -X utf8 tools/ux_lint.py --root ../kor-travel-weather/packages/kor-travel-weather-admin/frontend
```

## evidence

PR 3개 본문(preflight 예외 표·grep 결과·6폭 diff·문서 diff), `consumers.pins.json`·`docs/integration-map.md`·`docs/journal.md`, 이 파일 "실행 기록". T-503 회수 보고에 "weather CSS 행 수 2,495 → N" 지표 제공.

## rollback·release 차단 조건

- preflight 활성화로 설명 불가 diff가 남으면 PR 1 revert(D-08 중단 조건).
- 마커 색 값이 바뀌면(토큰화는 이름만) PR 2 머지 금지.
