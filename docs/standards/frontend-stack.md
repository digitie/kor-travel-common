# 프론트엔드 스택 규약 — 표준 구성 파일·품질 게이트·`kt-`·`cn`·금지 사항

- 정본 지위: 이 문서는 프론트엔드 앱의 **구성 파일 형태·게이트·네임스페이스·금지 사항**의 정본이다. 버전 **값**(floor/recommended/exceptions)은 [versions.md](versions.md)와 `versions.json`이 정본이며 여기서는 인용만 한다. 토큰은 [design-tokens](design-tokens.md), UI 계약은 [ui-contract](ui-contract.md).
- 확정 task: **T-107**(구성 조각 `templates/eslint/*.mjs`·tsconfig base·postcss·`components.json` 산출과 함께 확정). 마지막 갱신: 2026-09-06.
- 근거 약칭: `vm` = [version-matrix 조사](../survey/cross/version-matrix.md), `ui` = [ui-components 조사](../survey/cross/ui-components.md), `dt` = [design-tokens 조사](../survey/cross/design-tokens.md), `inv/<app>` = [인벤토리](../survey/README.md) §3.1.

## 1. 표준 스택

**FS-1 (MUST)** 프론트엔드 앱은 아래 축을 쓴다. "권장" 열은 2026-09 기준선(브리프 D-06)의 요약이며 정확한 floor/recommended/예외는 [versions.md](versions.md)가 정본이다.

| 축 | 표준 | 권장(2026-09) | 비고 |
|---|---|---|---|
| Node / npm | Node 22 LTS, npm 11 + `package-lock.json` v3 | 22.23.x / 11.19.x | `engines.node ^22.12.0`, `.nvmrc`; Node 20 CI는 22로(T-403). map npm 12.0.1 exact는 예외 |
| 프레임워크 | Next.js 16 App Router + React 19 | 16.3.4 / 19.2.8 | React 18(geo·ktdm)은 tokens만 채택, ui는 React 19 승격 후(O-25, T-443·T-470) |
| 언어 | TypeScript 5.9 | 5.9.3 | TS 7은 typescript-eslint peer(`<6.1.0`) 밖 → airport 예외(O-6, T-433) |
| 스타일 | Tailwind CSS v4 + `@tailwindcss/postcss` | 4.3.3 | CSS-first(§4). pinvi mobile Tailwind 3은 열림 O-8 |
| 컴포넌트 | shadcn `base-nova` + `@base-ui/react`(overlay만) + native 요소 | shadcn CLI 4.21.x(devDependencies), base-ui 1.8.0 | D-09. geo radix → base-ui 이관은 T-444 |
| 클래스 유틸 | `class-variance-authority` + `clsx` + `tailwind-merge`(`extendTailwindMerge`) | 0.7.1 / 2.1.1 / 3.6.0 | npm `cn` 패키지 금지(§5) |
| 아이콘 | `lucide-react`(앱) | 1.x | `@kor-travel/ui`는 인라인 SVG로 lucide peer를 두지 않는다(D-01) |
| 표·가상화 | `@tanstack/react-table` 8.21 + `react-virtual` 3.14 | 8.21.x / 3.14.x | react-table 9는 미조사(T-507) |
| 데이터·폼·상태 | `@tanstack/react-query` 5, `react-hook-form` 7 + `@hookform/resolvers` 5 + `zod` 4, `zustand` 5 | 최신 5.x / 7.8x / 5.x / 4.5.x / 5.0.x | resolvers 3(ktc·pinvi)은 채택 PR에서 상향 |
| 지도 | `maplibre-gl` 5.24, `maplibre-vworld-*`(외부 공유 라이브러리) | 5.24.x | ktc 6.0 예외. common 범위 밖(D-23) |
| 린트 | ESLint 9+ flat config, typescript-eslint 8 | 10.x / 8.x | ESLint 8(ktdm)은 Next 16 업그레이드와 함께(T-470) |
| 테스트 | Vitest 4.1 + `@testing-library/react` 16 + jsdom, `@playwright/test` 1.63 | 4.1.x / 1.63.x | Vitest 5는 T-507 재평가 |
| 타입 생성 | `openapi-typescript` 7 | 7.13.x | `gen:types` / `gen:types:check`([openapi](openapi.md)) |
| 이미지 처리 | `sharp`(next optional) | next 동봉 | map은 `verify-next-sharp.mjs` 동반 갱신 |

lockfile은 의무(`package-lock.json` v3, D-07)이며 `check_versions.py`가 설치본을 `versions.json`과 대조한다.

## 2. 저장소 배치

**FS-2 (SHOULD)** 프론트엔드 루트(`frontend/`, `apps/web/`, `packages/<app>-admin/frontend/` 등)에 다음 파일을 둔다. common은 조각을 `templates/`로 배포하고([templates README](../../templates/README.md)) 앱은 복사 후 경로만 바꾼다.

| 파일 | 역할 | 조각 위치(T-107) |
|---|---|---|
| `package.json` | scripts 표준 이름(§6), `engines`, `packageManager` | — |
| `components.json` | shadcn 기준값(§3.1) | `templates/frontend/components.json` |
| `postcss.config.mjs` | `@tailwindcss/postcss` 단일 플러그인(§3.2) | `templates/frontend/postcss.config.mjs` |
| `tsconfig.json` (+ `tsconfig.tooling.json`) | base 확장(§3.3) | `templates/frontend/tsconfig.base.json` |
| `eslint.config.mjs` | flat config, 프로필 2종(§3.4) | `templates/eslint/*.mjs`([templates/eslint README](../../templates/eslint/README.md)) |
| `vitest.config.ts`, `playwright.config.ts` | §8 | `templates/playwright.baseline.ts`(T-108) |
| `src/app/globals.css`(또는 `app/globals.css`) | Tailwind 진입점(§4) | [design-tokens](design-tokens.md) §13 |
| `src/lib/utils.ts` | `cn` 재수출(§5) | — |
| `design.md` | 표면 분류·knob·앱 고유 결정. 한국어 본문(D-32) | — |

## 3. 구성 파일 기준값

### 3.1 `components.json`

**FS-3 (MUST)** shadcn 설정은 map·concierge·airport WIP가 이미 공유하는 값을 기준으로 한다(`ui` §6.1, `inv/map` §3).

```json
{
  "$schema": "https://ui.shadcn.com/schema.json",
  "style": "base-nova",
  "rsc": true,
  "tsx": true,
  "tailwind": { "config": "", "css": "src/app/globals.css", "baseColor": "neutral", "cssVariables": true, "prefix": "" },
  "iconLibrary": "lucide",
  "rtl": false,
  "aliases": { "components": "@/components", "utils": "@/lib/utils", "ui": "@/components/ui", "lib": "@/lib", "hooks": "@/hooks" },
  "registries": {}
}
```

- `tailwind.config`는 빈 문자열이다(v3 config 없음). `@config`를 쓰는 앱은 전환 완료 전까지만 경로를 둔다(§4).
- `style`은 `base-nova`. geo `radix-nova`는 T-444에서 교체, pinvi는 `components.json` 신설(T-422; `ui: @/components/admin/ui`, `utils: @/lib/admin/cn` 경로 허용).
- `registries`는 셸·로그인·기준선 템플릿 채널(T-211)이 생기면 `@kor-travel` 항목을 추가한다. 전면 레지스트리는 Phase 5 재검토(D-10).
- `hooks` alias 디렉터리는 없어도 된다(사실: 4앱 중 3앱 부재).

### 3.2 `postcss.config.mjs`

**FS-4 (MUST)** 플러그인은 `@tailwindcss/postcss` 하나다. `autoprefixer`·`postcss` 직접 의존은 두지 않는다(v4가 처리; concierge 잔존 의존성은 제거 대상). next 중첩 `postcss 8.4.31`은 `overrides`로 8.5.x에 맞춘다(세 방식이 공존하므로 `overrides.postcss`를 표준으로, `vm` §1.2).

### 3.3 `tsconfig`

**FS-5 (MUST)** `tsconfig.base.json`(pinvi 선례, `inv/pinvi` §8-16)을 확장한다.

| 옵션 | 값 | 이유 |
|---|---|---|
| `strict` | `true` | |
| `noUncheckedIndexedAccess` | `true` | `@kor-travel/ui`가 이 옵션으로 타입 검사되므로 소비자도 같은 조건에서 검사(D-10) |
| `noImplicitOverride`, `noFallthroughCasesInSwitch` | `true` | |
| `verbatimModuleSyntax`, `isolatedModules` | `true` | ESM + 번들러 전제 |
| `moduleResolution` | `"bundler"` | common 패키지 `exports` 해석. weather `node`는 T-460에서 전환 |
| `module` / `target` | `"esnext"` / `"es2022"` | ktdm `target es5`는 T-470 실검증 |
| `jsx` | `"preserve"` | Next |
| `paths` | `{ "@/*": ["./src/*"] }` | alias 하나 |
| `tsconfig.tooling.json` | vitest/playwright config 자체 검사 | map 2026-08-12 `parsedBaseURL` 사고 재발 방지(`inv/map` §3) |

### 3.4 `eslint.config.mjs`

**FS-6 (MUST)** flat config만 쓰고 `.eslintrc*`는 두지 않는다. 프로필은 2종이며 앱이 하나를 고른다(조각 이름은 후보, [templates/eslint README](../../templates/eslint/README.md)가 확정).

| 프로필 | 구성 | 채택 앱 | 근거 |
|---|---|---|---|
| `next-minimal` | `eslint-config-next/core-web-vitals` + `eslint-config-next/typescript` + `kt-guards` | ktc·geo·pinvi·weather(현재 구성과 동일) | `inv/concierge` §3, `inv/geo` §3 |
| `next-strict` | `typescript-eslint` recommended + `eslint-plugin-import-x` + `eslint-plugin-react-x`/`react-dom` + `eslint-plugin-jsx-a11y-x` + `eslint-plugin-react-hooks` `recommended-latest`(React Compiler 규칙) + `@next/eslint-plugin-next`; `eslint-config-next` 미사용 + `kt-guards` | map(현행) | `inv/map` §3, §8-24 |
| `kt-guards` | `no-restricted-syntax`로 [ux-guide](ux-guide.md) §4 P2·P3·P5·P6·P7의 클래스 리터럴 판정(Literal·TemplateElement) + `no-restricted-imports` 경계 예시(사용자 표면에서 `@base-ui/react` 금지, admin↔사용자 모달 스택 양방향 금지) | 전 앱(선택) | pinvi `eslint.config.mjs` 선례(`inv/pinvi` §8-7) |

- `lint` 스크립트는 `eslint . --max-warnings 0`. 인라인 suppression은 0건이 기본이고(map `verify-frontend-eslint-config.mjs` 선례) 예외는 파일 상단 주석에 사유를 적는다.
- `ignores`: `.next`, `node_modules`, 생성물(`types/api.gen.ts`, `lib/schemas.gen.ts`).
- `react-hooks/incompatible-library` off는 TanStack 훅 파일(`data-table.tsx` 계열)에만.
- `kt-guards`는 `ux_lint.py`(정본 게이트)의 보조다. 두 도구 결과가 어긋나면 `ux_lint.py`가 우선한다.

## 4. Tailwind v4 CSS-first 규약

**FS-7 (MUST)** Tailwind v4 앱의 진입 CSS는 다음 순서·형식을 따른다.

```css
@import "tailwindcss" source(none);          /* 자동 소스 탐지 끔 */
@source "../app"; @source "../components"; @source "../lib";
@source "../node_modules/@kor-travel/ui";    /* ui 채택 앱 필수 */
@import "@kor-travel/tokens/tokens.css";
@import "@kor-travel/tokens/theme.css";
@import "@kor-travel/tokens/shadcn.css";     /* shadcn 사용 앱 */
@import "@kor-travel/tokens/base.css";       /* 또는 base.scoped.css */
@import "@kor-travel/tokens/dark-class.css"; /* 다크 활성 앱만 */
@import "./brand.css";                       /* 앱 오버라이드 */
@layer components { /* 잔존 도메인 CSS */ }
```

| 규칙 | 내용 | 근거 |
|---|---|---|
| FS-7.1 `source(none)` + 명시 `@source` | 문서·테스트 산출물의 `shadow-[var(--…)]` 같은 프로즈가 스캔되어 파서가 죽는 문제 회피. `@source` 누락은 클래스 미생성으로 나타나므로 consumer-smoke가 `kt-` 유틸리티 존재를 단언 | `inv/geo` §3·§9 |
| FS-7.2 `@config` 금지 | v3 JS config 브리지(`@config "../tailwind.config.ts"`)는 전환 완료 후 제거한다. `@config`와 `@theme`의 병합 우선순위가 미확인이므로 같은 유틸리티 이름을 두 곳에 두지 않는다 | `dt` §3.6.3, T-441·T-453·T-421 |
| FS-7.3 `@theme inline` vs `@theme` | 색·radius·spacing처럼 `var()`를 참조하는 항목은 `@theme inline`, 타입 스케일은 비inline `@theme`(TK-5). 앱이 `theme.css` 밖에서 같은 네임스페이스 이름을 재정의하지 않는다 | `dt` §3.6.5 |
| FS-7.4 `dark` variant | `dark-class.css`는 `.dark` 선택자 variant를 선언하고 `dark-media.css`는 Tailwind v4 기본 `prefers-color-scheme` variant를 유지한다. 앱이 선택한 방식과 다른 variant를 중복 선언하면 소유 검증 테스트(map `test_frontend_owns_every_named_shadcn_css_token_it_uses` 선례)가 실패해야 한다 | `dt` §3.4.1 |
| FS-7.5 `@utility` | `duration-kt-*`·`z-kt-*`는 `theme.css`가 정의. 앱 `@utility`는 앱 접두 | |
| FS-7.6 preflight | v4 preflight를 켠다. weather처럼 전역 요소 규칙에 의존하는 앱은 `@import "tailwindcss/theme" layer(theme); @import "tailwindcss/utilities" layer(utilities);`로 preflight 없이 시작해 마지막 단계에서 켠다(D-08 ⑥) | `inv/weather` §9.1 |
| FS-7.7 도메인 CSS | 공통 컴포넌트로 대체되지 않는 앱 CSS(workbench·Dagster·마커)는 `@layer components` 또는 CSS module에 두고 토큰만 참조한다 | `inv/weather` §9.1 |

## 5. `kt-` 유틸리티 네임스페이스·`cn`

**FS-8 (MUST)** `@kor-travel/ui` 패키지 내부 클래스는 `kt-` 접두 유틸리티(`bg-kt-surface-page`, `h-kt-control`, `rounded-kt-control`, `text-kt-2xs`, `border-kt-control-line`, `outline-kt-focus`)와 Tailwind 기본 레이아웃 유틸리티(`flex`, `gap-2`, `min-w-0` 등)만 쓴다. shadcn 기본 색 이름(`bg-primary`, `text-muted-foreground`)과 앱 어휘(`bg-admin-subtle`, `text-brand`)는 패키지 안에서 금지한다. 앱 코드는 `kt-` 유틸리티를 권장하되 앱 별칭(`theme.css` 밖 앱 `@theme`)을 허용한다(D-10, `ui` §6.3).

**FS-9 (MUST)** `cn`은 `@kor-travel/ui/cn`이 정본이다: `clsx` + `extendTailwindMerge`로 `kt-` 그룹(`rounded-kt-control/panel`, `h-kt-control/-sm`, `w-kt-rail`, `text-kt-2xs..2xl`)을 등록해 병합 충돌을 막는다(pinvi `lib/admin/cn.ts` 선례 — 등록형이어야 하는 이유는 `inv/pinvi` §8-5). 앱 `@/lib/utils`는 이를 재수출한다(`export { cn } from "@kor-travel/ui/cn"`). npm `cn@0.2.5` 패키지 재수출(airport WIP)은 금지하며 T-430에서 clsx + tailwind-merge로 바꾼다.

## 6. 품질 게이트

**FS-10 (MUST)** 앱 `package.json` scripts는 아래 표준 이름을 가지며 CI가 같은 이름을 호출한다. 재사용 워크플로 `node-quality.yml`(T-401)이 이 표를 구현한다([ci-deploy](ci-deploy.md)).

| script | 명령(표준) | 수준 | 비고 |
|---|---|---|---|
| `lint` | `eslint . --max-warnings 0` | MUST | §3.4 |
| `type-check` | `tsc --noEmit && tsc -p tsconfig.tooling.json --noEmit` | MUST | e2e tsconfig가 있으면 포함 |
| `test` | `vitest run` | MUST | 0 test·skip을 pass로 집계하지 않는다(D-25) |
| `test:e2e` | `playwright test` | SHOULD | 서버 외부 기동 전제는 앱별 |
| `build` | `next build` | MUST | consumer-smoke는 webpack·Turbopack 양쪽(D-10) |
| `gen:types` / `gen:types:check` | `openapi-typescript` 생성 / `git diff --exit-code` | MUST(typegen 앱) | [openapi](openapi.md) |
| `doctor` | `react-doctor --offline …` | MAY | map 선례(`doctor.config.json` 잠금). 채택 시 설정 파일을 검증 스크립트로 잠근다 |
| `verify:npm-tree` / `audit:high` | 설치 트리·감사 | SHOULD | map 보안 게이트 모델(`inv/map` §8-23) |
| `ux:lint` | `python3 -B -X utf8 tools/ux_lint.py …`(common 도구 호출) | MUST(report) → fail 승격 | [ux-guide](ux-guide.md) §4 |
| `contrast` | `tools/kt_contrast.py` | MUST(report) → fail 승격 | [design-tokens](design-tokens.md) TK-13 |
| — | `tools/check_versions.py`(CI job) | MUST(report) | [versions.md](versions.md) |

- 게이트 명령을 PR 본문에 적는 것은 실행 증거가 아니다. 실제 결과(test 수·exit code)를 적는다(D-25).
- 시각 기준선(6폭)은 [responsive-web](responsive-web.md) §3.

## 7. 폰트

**FS-11 (SHOULD)** 폰트 로딩은 앱 책임이며 스택 문자열만 토큰이다(TK-15). 권장 방식은 두 가지다.

| 방식 | 예 | 채택 앱 |
|---|---|---|
| `pretendard` npm dynamic subset CSS import | `import "pretendard/dist/web/variable/pretendardvariable-dynamic-subset.css"` in `layout.tsx` | map·pinvi·concierge(1.3.9 exact) |
| `next/font/google` mono | `Geist_Mono({ variable: "--font-geist-mono" })` → `--kt-font-mono` 오버라이드 | map |

로드하지 않는 폰트를 스택 1순위에 두지 않는다. 미로드 앱(weather·airport·geo·ktdm)은 채택 시 현재 스택으로 오버라이드하고 로딩 도입은 별도 task로 둔다. `@kor-travel/ui`·`tokens`는 폰트 파일을 배포하지 않는다.

## 8. 테스트 하네스

**FS-12 (MUST)** 단위 테스트는 Vitest + `@testing-library/react` + jsdom이다. `@kor-travel/ui`의 계약 테스트([ui-contract](ui-contract.md) §11)는 같은 하네스로 작성돼 소비자가 이관할 수 있다. axe(`vitest-axe`)는 opt-in이다(D-33).

| 항목 | 규칙 |
|---|---|
| 셋업 | `tests/setup.ts`에서 `@testing-library/jest-dom/vitest` 등록, `cleanup` 자동 |
| 네이티브 select | `fireEvent.change`로 구동 가능한 `NativeSelect`를 우선한다(geo 주석 근거) |
| e2e | Playwright mocked suite(`page.route`·storageState auth setup·`timezoneId: "UTC"`)와 live suite를 config 파일로 분리(map 선례). live suite는 required check로 두지 않는다(D-18) |
| 기준선 | `templates/playwright.baseline.ts` 6폭 스크린샷 |
| 하네스 타입 검사 | `tsconfig.tooling.json`(§3.3) |
| 계약 e2e | testid·sr-only 문구 변경은 [ui-contract](ui-contract.md) §9 파괴 항목이므로 e2e가 먼저 깨져야 한다 |

## 9. 지시문·React Compiler

**FS-13 (MUST)** 클라이언트 컴포넌트는 파일 첫 줄 `'use client'`, React Compiler를 끄는 파일은 `'use no memo'`를 두며 패키지 빌드가 두 지시문을 보존한다(D-10). `'use no memo'`는 TanStack 훅 파일(DataTable·VirtualizedTable)처럼 사유가 문서화된 곳에만 두고, map처럼 개수를 검증 스크립트로 잠그는 것을 권장한다(`inv/map` §3). `eslint-plugin-react-hooks` `recommended-latest`의 Compiler 규칙을 끄지 않는다.

## 10. 금지 사항

**FS-14 (MUST)** 다음은 하지 않는다.

1. `@main`·branch 참조·`latest` 태그로 패키지를 설치하지 않는다(`git+https://…@main`, D-11).
2. `shadcn`·`postcss`·`@tailwindcss/postcss`를 `dependencies`에 두지 않는다(devDependencies).
3. npm `cn` 패키지, `autoprefixer`, `.eslintrc*`, `tailwind.config.*`(전환 완료 후), `eslint-config-next`와 `next-strict` 플러그인 집합의 혼합을 쓰지 않는다.
4. `@kor-travel/ui` 안에서 `forwardRef`·`lucide-react` import·shadcn 기본 색 이름·앱 어휘를 쓰지 않는다.
5. TypeScript 7·Node 20·ESLint 8을 신규 앱에 도입하지 않는다(기존 앱은 `versions.json` 예외로만).
6. `overflow-x: hidden`, 커스텀 `--breakpoint-*`, `text-[Npx]`, `z-[N]`([ux-guide](ux-guide.md) §4 · [responsive-web](responsive-web.md) §2·§7).
7. 생성물(`*.gen.ts`, `tokens.json`)을 손으로 고치지 않는다.
8. Hallmark 스탬프·SKILL 본문을 common 배포 파일에 넣지 않는다(SPDX 헤더만, [licensing](licensing.md)).
9. 실행하지 않은 게이트를 통과로 적지 않는다(`NOT_RUN(사유)`, D-25).

## 11. 앱별 현재 격차(요약)

수치 정본은 [versions.md](versions.md)·[통합 계획](../plan/integration-plan.md). 아래는 이 문서 규칙 관점의 요약이다(`ui` §2.3, `vm` §1.2~§1.6).

| 앱 | 규약과의 차이(사실) | 조치 task |
|---|---|---|
| map | ESLint 10 `next-strict`, Next 16.2.12 exact + `verify-next-sharp`, Playwright 1.60 exact, npm 12.0.1 | 예외 등록, 상향은 T-413 별도 PR |
| pinvi web | `components.json` 없음, `@config` v3 preset, `tsconfig.base` 규약과 일치 | T-421·T-422 |
| geo | React 18, radix `radix-nova`, `@config` + raw hex config, `asChild` 17곳 | T-440·T-441·T-443·T-444 |
| concierge | base-ui 1.5, `@config`, hex fallback 블록, autoprefixer 잔존, CI 없음 | T-450·T-451·T-453·T-454 |
| weather | Tailwind 없음(순수 CSS 2,495행), Next 15, Vitest 3, `moduleResolution: node`, react-query 미사용 선언 | T-460~T-464 |
| ktdm | Next 14 / React 18 / ESLint 8, `ops-*` CSS 혼용 | T-470~T-473 |
| airport | main Tailwind 없음, WIP는 shadcn 4.21 `base-nova` + npm `cn` + deps 위치, TS 7.0.2, ESLint 없음 | T-430~T-433 |

## 12. 열린 결정

| # | 항목 | 기본값(이 문서) |
|---|---|---|
| O-3 | UI 배포 방식 | npm 1차, 레지스트리는 셸·템플릿 채널만 |
| O-5 | 패키지 식별자 | [ADR-014](../adr/014-common-implementation-without-registry-publishing.md)로 확정. 공개 registry 이름 확보 제외 |
| O-6 | TS 기준선·airport 7.0.2 | 5.9.3 + airport 예외 |
| O-8 | pinvi mobile Tailwind 3 | 미등록(사용자 승인 대기) |
| O-10 | Node/npm | Node 22 + npm 11.19 권장 |
| O-25 | geo React 19 | 승인 기본값, 별도 PR 실검증 |
| — | ESLint 프로필 조각 이름(`next-minimal`/`next-strict`/`kt-guards`) | 후보, T-107 확정 |

## 13. 근거

- 버전 매트릭스·최신 대조·핀 정책: [version-matrix 조사](../survey/cross/version-matrix.md) §1·§5·§7.
- 스택·`components.json`·`cn`·엔진: [ui-components 조사](../survey/cross/ui-components.md) §2.3·§5·§6.
- Tailwind v4 구성 함정(`source(none)`, `@config`): [geo 인벤토리](../survey/inventory/kor-travel-geo.md) §3·§9, [design-tokens 조사](../survey/cross/design-tokens.md) §3.6.3.
- ESLint·react-doctor·보안 게이트 모델: [map 인벤토리](../survey/inventory/kor-travel-map.md) §3·§8.
- `tsconfig.base`·Hallmark ESLint 가드·등록형 `cn`: [pinvi 인벤토리](../survey/inventory/pinvi.md) §3·§8.
- weather v4 전환 정량: [weather 인벤토리](../survey/inventory/kor-travel-weather.md) §9.1.
- 결정: [설계 브리프](../plan/design-brief.md) D-01·D-06~D-11·D-25·D-33, O-3·O-5·O-6·O-8·O-10·O-25.
