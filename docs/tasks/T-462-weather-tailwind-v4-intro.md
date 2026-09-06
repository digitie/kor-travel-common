# T-462 weather: Tailwind v4 도입(theme+utilities, preflight 제외) + `@theme inline` 1:1 매핑

- 상태: BLOCKED
- 우선순위: P1
- Gate: 시각 diff
- 선행: T-460, T-461

## 목표

Tailwind가 전혀 없는 weather admin에 Tailwind v4.3.x를 "설정만" 단계로 도입한다. `@import "tailwindcss/theme" layer(theme)`과 `utilities`만 넣고 preflight는 제외해 2,334행 손수 CSS와 bare element 규칙 23종이 그대로 살아 있게 한다. `@theme inline`으로 `--kt-*`(T-461) → `--color-*`/`--spacing-*`/`--radius-*` 유틸리티 이름을 1:1 매핑해 이후 컴포넌트 단계(T-463)에서 `kt-` 유틸리티가 즉시 쓰이도록 준비한다. 렌더 diff 0.

## 고정 결정

- [design-brief](../plan/design-brief.md) D-08(4단 별도 PR: 기준선 → 설정만 → 토큰만 → 컴포넌트; weather ⑥ = `@import "tailwindcss/theme" layer(theme)` + `utilities`만, preflight 제외)·D-10(`theme.css`가 `--color-kt-*` 등 정의 → 소비자 2줄)·D-06(Tailwind 4.3.0 floor·4.3.3 recommended, `@tailwindcss/postcss`)·D-24.
- ADR-012·ADR-006 — [ADR 색인](../adr/README.md). 정본: [frontend-stack](../standards/frontend-stack.md)(postcss·components.json 조각), [design-tokens](../standards/design-tokens.md).
- 사실: Tailwind 부재, `postcss.config.mjs`·`components.json` 없음, 최상위 규칙 약 277개·bare element 23종·className 220개/13 TSX·동적 className 19곳, 전환 정량 표(preflight 대체 243행 10%, 공유 컴포넌트 대체 40~48%, responsive 233행, 도메인 잔존 32~35%) — [inv/weather §9.1](../survey/inventory/kor-travel-weather.md); geo의 `source(none)` + 명시 `@source` 함정 — [inv/geo §8-16](../survey/inventory/kor-travel-geo.md).
- PR 순서: [judge-migration-feasibility §3.1 weather #3](../plan/design-panel/judge-migration-feasibility.md).

## 구현 범위

- `package.json` devDependencies: `tailwindcss` 4.3.x, `@tailwindcss/postcss` 4.3.x, `postcss`; `postcss.config.mjs` 신설(`@tailwindcss/postcss` 단일 플러그인, autoprefixer 없음).
- `app/globals.css` 헤더: `@import "tailwindcss/theme" layer(theme); @import "tailwindcss/utilities" layer(utilities) source(none); @source "../app"; @source "../components"; @source "../lib";` + `@import "@kor-travel/tokens/theme.css";`(`kt-` 유틸리티 등록). `preflight` import 없음.
- `@theme inline { --color-background: var(--background); … }`로 shadcn 이름·`--space-*`·`--control-h`·`--rail` 을 유틸리티 네임스페이스에 매핑(inv/weather §9.1 추정대로 거의 1:1). 기존 CSS는 cascade 순서상 `@layer` 밖(unlayered)이라 utilities보다 우선하므로 diff 0이어야 한다.
- 빌드 CSS 크기·규칙 수 전후 비교표(utilities 사용 0이므로 추가분은 theme 변수뿐).

## 범위 밖

className 교체·컴포넌트 도입(T-463), preflight(T-464), `components.json`·shadcn CLI(T-463에서 필요 시), 마커 색 토큰화(T-464).

## 대상 저장소·브랜치·PR·되돌리기

- `digitie/kor-travel-weather`, 브랜치 `feat/T-462-tailwind-config`, `origin/main`에서 분기, Draft PR. PR 1개(≤10 파일).
- 되돌리기 = `git revert <merge-sha>` + `npm ci`.

## 예상 변경 파일

아래는 이 task가 만들거나 고칠 예정 경로다. 예정 경로는 존재·실행 증거가 아니다.

```text
packages/kor-travel-weather-admin/frontend/package.json, package-lock.json
packages/kor-travel-weather-admin/frontend/postcss.config.mjs
packages/kor-travel-weather-admin/frontend/app/globals.css        # 헤더 + @theme inline 블록
packages/kor-travel-weather-admin/frontend/kor-travel-common.lock.json
```

## 수용 기준

- [ ] 6폭 스크린샷 diff 0(T-461과 같은 페이지 세트, 수동 템플릿 실행).
- [ ] 빌드 CSS에 `preflight` 규칙(`*, ::before, ::after { box-sizing … }` 등 Tailwind preflight 시그니처) 0건, `--color-kt-*` 정의 존재.
- [ ] `grep -c 'className="[^"]*\bkt-' app components` 0(이 단계에서 유틸리티 사용 없음).
- [ ] CI frontend job green(lint·type-check·test·build; T-460 후 vitest 포함).
- [ ] `check_versions` weather 행 Tailwind `OK`.

## 검증 명령

```bash
# kor-travel-weather/packages/kor-travel-weather-admin/frontend
npm ci --ignore-scripts && npm run lint && npm run type-check && npm test && npm run build
grep -rl 'box-sizing' .next/static/css/ | head   # preflight 시그니처 확인용(0 예상)
BASELINE_APP=weather BASELINE_URL=http://127.0.0.1:14105 npx playwright test -c ../../../../kor-travel-common/templates/playwright.baseline.ts
# kor-travel-common
python3 -B -X utf8 tools/check_versions.py --manifest ../kor-travel-weather/packages/kor-travel-weather-admin/frontend/kor-travel-common.lock.json
```

## evidence

PR 본문(6폭 diff·빌드 CSS 크기/규칙 수 전후·preflight 부재 grep), `consumers.pins.json`·`docs/integration-map.md`·`docs/journal.md`, 이 파일 "실행 기록".

## rollback·release 차단 조건

- 원인 불명 diff(특히 `@layer` 순서로 utilities가 기존 규칙을 덮는 경우) → revert, `@source` 범위·layer 선언을 재검토한 뒤 재시도(D-08).
- T-460(Next 16) 미머지 상태에서는 이 PR을 열지 않는다(PostCSS 파이프라인 검증 대상이 달라짐).
