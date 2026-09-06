# T-461 weather: `app/tokens.css` → `@kor-travel/tokens/tokens.css` + `aliases/map-vocabulary.css` + navy·`--rail`·font 오버라이드 + 매니페스트(6폭 diff 0 evidence)

- 상태: BLOCKED
- 우선순위: P0
- Gate: 시각 diff(수동)
- 선행: T-109

## 목표

weather admin의 `app/tokens.css`(161행, "kor-travel-map admin design system" 사본)를 `@kor-travel/tokens/tokens.css` + 레거시 어휘 별칭 shim `aliases/map-vocabulary.css`로 교체한다. weather 고유 값(navy brand, `--rail: 17rem`, Geist 1순위 font 스택)은 `--kt-*` 오버라이드로 얹어 2,334행 `globals.css`가 쓰는 map 어휘 294회를 무변경으로 유지한다. Tailwind는 아직 없으므로 순수 CSS 교체이며 Next 버전과 독립이다. Playwright가 없어 6폭 diff는 common 템플릿으로 수동 실행한다.

## 고정 결정

- [design-brief](../plan/design-brief.md) D-08 ⑥(weather 1단 = `tokens.css` 교체, 별칭 shim + font·`--rail` 오버라이드 동반)·D-12(별칭 shim `aliases/map-vocabulary.css`, font 스택은 앱이 현재 스택으로 오버라이드, Pretendard MUST는 로드 앱만; `--rail` 22rem 기본)·D-16(tokens 1차 = map + weather)·D-21(wx는 `templates/playwright.baseline.ts`)·D-24(≤10 파일).
- ADR-006·ADR-010 — [ADR 색인](../adr/README.md). 정본: [design-tokens](../standards/design-tokens.md), [consumer-adoption runbook](../runbooks/consumer-adoption.md).
- 사실: `tokens.css` `:root`/`.dark`, shadcn 이름(`--background`…) 포함, `--space-3xs…2xl`, `--radius-control/panel`, `--control-h/-sm`, `--rail 17rem`(design.md는 16rem, 접힘 미구현), map 어휘 294회, 폰트 미로딩·`--font-geist`/`--font-pretendard` 미정의, 다크 토글 없음, vitest 4개·Playwright 없음 — [inv/weather §3.1·§8-1·§9](../survey/inventory/kor-travel-weather.md), [dt §3.1·§3.6.4·§5-8](../survey/cross/design-tokens.md), [ux §4 C2·C12](../survey/cross/ux-patterns.md).
- PR 순서: [judge-migration-feasibility §3.1 weather #1](../plan/design-panel/judge-migration-feasibility.md), §4.2(T-460 선행 아님).

## 구현 범위

- `app/globals.css` 10행 `@import "./tokens.css"` → `@import "@kor-travel/tokens/tokens.css"; @import "@kor-travel/tokens/aliases/map-vocabulary.css"; @import "./tokens.override.css";`. Tailwind 없이 CSS `@import`가 `node_modules`를 해석하려면 Next CSS 로더 경로(`~@kor-travel/...` 또는 상대 경로) 중 빌드로 확인된 형식을 쓴다.
- `app/tokens.override.css`(신규): `--kt-brand*` navy 4종, `--kt-rail: 17rem`, `--kt-font-sans`(현재 Geist 1순위 스택 그대로), 그 외 weather가 map 값과 다른 변수 전수(착수 시 `tokens.css` vs 패키지 `tokens.css` diff로 목록화). `.dark` 값은 선택(토글 없음).
- 기존 `app/tokens.css` 삭제. `package.json`에 `@kor-travel/tokens`(tarball + integrity), lock 동반.
- `packages/kor-travel-weather-admin/frontend/kor-travel-common.lock.json` `tokens{version, override: "app/tokens.override.css"}`·`contrast{baseline, dark:false}`; `kt_contrast` light report → 미달 쌍 baseline.

## 범위 밖

Tailwind 도입(T-462), 컴포넌트 교체(T-463), preflight·도메인 CSS(T-464), 셸 17rem/16rem 불일치 해소(T-464), 폰트 로딩, Next/Vitest/Node(T-460).

## 대상 저장소·브랜치·PR·되돌리기

- `digitie/kor-travel-weather`, 브랜치 `feat/T-461-tokens`, `origin/main`에서 분기, Draft PR. PR 1개(≤10 파일).
- 되돌리기 = `git revert <merge-sha>` + `npm ci`(`app/tokens.css` 복원 포함).

## 예상 변경 파일

아래는 이 task가 만들거나 고칠 예정 경로다. 예정 경로는 존재·실행 증거가 아니다.

```text
packages/kor-travel-weather-admin/frontend/app/globals.css        # import 3줄
packages/kor-travel-weather-admin/frontend/app/tokens.css         # 삭제
packages/kor-travel-weather-admin/frontend/app/tokens.override.css
packages/kor-travel-weather-admin/frontend/package.json, package-lock.json
packages/kor-travel-weather-admin/frontend/kor-travel-common.lock.json
packages/kor-travel-weather-admin/frontend/contrast-baseline.json
.github/workflows/ci.yml                                          # contrast-check job(report)
```

## 수용 기준

- [ ] 착수 전/후 6폭 스크린샷(대시보드·datasets·sync-runs·weather 지도·admin/dagster·로그인) 픽셀 diff 0 — common `templates/playwright.baseline.ts`를 weather 서버(`npm run dev` 또는 `start -p 14105`)에 외부 실행. 실행 못 하면 `NOT_RUN`이며 DONE 불가.
- [ ] `globals.css` 2,334행 diff가 import 3줄뿐이고 map 어휘 294회 소비처 무변경(`git diff --stat`).
- [ ] 빌드 CSS에서 `--rail`이 17rem, brand가 navy, `--font-sans` 첫 항목이 현재 스택과 동일(grep 대조표).
- [ ] CI frontend job(`lint`·`type-check`·`build`) green; vitest 4개는 CI 미실행 상태면 로컬 실행 기록.
- [ ] `kt_contrast` light 신규 미달 0; `check_versions` weather 행 tokens `OK`.

## 검증 명령

```bash
# kor-travel-weather/packages/kor-travel-weather-admin/frontend
npm ci --ignore-scripts && npm run lint && npm run type-check && npm test && npm run build
npm run start -- --port 14105 &   # 별도 터미널
BASELINE_APP=weather BASELINE_URL=http://127.0.0.1:14105 npx playwright test -c ../../../../kor-travel-common/templates/playwright.baseline.ts
# kor-travel-common
python3 -B -X utf8 tools/kt_contrast.py --app weather --baseline ../kor-travel-weather/packages/kor-travel-weather-admin/frontend/contrast-baseline.json
python3 -B -X utf8 tools/check_versions.py --manifest ../kor-travel-weather/packages/kor-travel-weather-admin/frontend/kor-travel-common.lock.json
```

## evidence

PR 본문(6폭 전후 캡처와 diff 결과, 변수 대조표, 명령 출력), `consumers.pins.json`·`docs/integration-map.md`·`docs/journal.md`, 이 파일 "실행 기록"(캡처 digest·브라우저 버전).

## rollback·release 차단 조건

- 원인 불명 diff → revert 후 확대 중단(D-08 중단 조건, Phase 1 "원인 불명 diff → patch 후 확대 중단").
- 이 PR 머지 전 `tokens-v0.1.0` 정식 태그를 "weather 검증 완료"로 표기하지 않는다(T-109).
