# T-201 packages/ui 골격(ESM·d.ts·subpath exports·`'use client'`/`'use no memo'` 보존·peer react ^19·인라인 아이콘·`cn` extendTailwindMerge·noUncheckedIndexedAccess) + base-ui 사실 확인 3건 기록 + pack 스모크(webpack/Turbopack)

- 상태: BLOCKED
- 우선순위: P0
- Gate: 패키지 빌드·tarball
- 선행: T-109
- 외부 선행: npm scope `@kor-travel` 확인(T-006, O-5)은 비차단 — 실패하면 이름만 `@digitie/kor-travel-ui`로 바꾼다(첫 소비자 PR 전이면 비용 0)

## 목표

`@kor-travel/ui`(잠정 이름)가 컴포넌트 0개 상태에서도 빌드 → `npm pack` → tarball 설치 → Next 16 `next build`(Turbopack·webpack 양쪽)까지 통과하는 배포 골격을 만든다. T-203~T-210은 이 골격 위에 컴포넌트만 추가한다. [브리프](../plan/design-brief.md) D-09가 "소스 확인 전 릴리스 금지"로 지정한 base-ui 미확인 3건(Button `type` 기본, Checkbox hidden input, Toast API)을 이 task에서 확인해 기록한다.

## 고정 결정

- ADR-005(배포 채널·SemVer 0.x)·ADR-007(React UI 배포 방식) — [ADR 색인](../adr/README.md). 결정 원문은 브리프 D-01·D-09·D-10·D-11·D-17·D-31·D-33.
- 규칙 정본: [frontend-stack](../standards/frontend-stack.md)(툴체인·tsconfig 조각), [ui-contract](../standards/ui-contract.md)(마크업 계약; T-204에서 확정), [design-tokens](../standards/design-tokens.md)(`kt-` 유틸리티·`--kt-*`), [licensing](../standards/licensing.md)(SPDX 헤더·tarball 동봉 파일). 현재 구조는 [packages](../architecture/packages.md)·[style-delivery](../architecture/style-delivery.md).
- 사실 근거: 4앱의 cva/clsx/tailwind-merge 설치 버전이 동일(0.7.1/2.1.1/3.6.0)하고 lucide-react는 0.363~1.41로 major가 갈리며 `noUncheckedIndexedAccess`는 pinvi만 true — [ui-components](../survey/cross/ui-components.md) §2.3, [version-matrix](../survey/cross/version-matrix.md) §1.3. pinvi는 Turbopack 대신 webpack을 강제(ADR-066) — [pinvi 인벤토리](../survey/inventory/pinvi.md) §9. pinvi `cn`이 등록형 `extendTailwindMerge`인 이유 — 같은 문서 §8-5. 배포 계약(peer React, `'use client'` 보존, ESM+d.ts, deep import 미지원, `npm pack` 설치 검증)은 선행 보고서 §7.3(요약: [survey README](../survey/README.md) §5).
- 이 task에서 확정하는 선택: 빌드는 번들 없는 `tsc` 파일 단위 ESM emit + `declaration`. tsc는 파일 선두 지시문(`'use client'`·`'use no memo'`)을 그대로 보존하므로 플러그인이 필요 없다. 번들러 전환은 아래 지시문 보존 검사가 통과할 때만 허용한다.

## 구현 범위

- `packages/ui/package.json`: `name`(잠정 `@kor-travel/ui`), `type: module`, `license: "GPL-3.0-or-later"`, `files`(`dist`, `LICENSE`, `NOTICE`, `THIRD_PARTY_NOTICES.md`), `sideEffects: false`, `exports`: `.`, `./cn`, `./icons`, `./package.json`(컴포넌트 subpath는 T-203부터 추가). peer: `react ^19.0.0`, `react-dom ^19.0.0`, `@kor-travel/tokens ~0.1.0`(같은 minor, D-31). dependencies: `clsx`, `tailwind-merge`, `class-variance-authority`(Apache-2.0, NOTICE 유지). `lucide-react`는 넣지 않는다. `@base-ui/react ^1.6.0`은 useRender helper 때문에 지금 peer로 선언하고 개발용으로도 설치한다. 1.6·1.8 실제 helper 호환성은 깨끗한 tarball fixture로 검증하며 실패하면 T-005 정책 변경 전 릴리스를 막는다.
- `packages/ui/tsconfig.json`: `strict`, `noUncheckedIndexedAccess: true`, `verbatimModuleSyntax`, `moduleResolution: bundler`, `jsx: react-jsx`, `declaration`, `outDir: dist`.
- `packages/ui/src/cn.ts`: `clsx` + `extendTailwindMerge`에 `kt-` 그룹 등록(`text-kt-*` 폰트 크기, `rounded-kt-*`, `h-kt-*`/`w-kt-*` spacing, `bg-kt-*`/`text-kt-*` 색). D-10 "`@kor-travel/ui/cn` = clsx + extendTailwindMerge(kt 그룹 등록)".
- `packages/ui/src/icons/`: 1차 컴포넌트가 쓰는 인라인 SVG 최소 집합(예: `TriangleAlertIcon`·`InfoIcon`·`CheckIcon`·`XIcon`·`CopyIcon`·`LoaderIcon`·`ChevronDownIcon`). 파일 헤더 `Derived-From: lucide (ISC)` + `THIRD_PARTY_NOTICES.md` 항목.
- 테스트 하네스: `vitest` + `@testing-library/react` + `jsdom` + `@testing-library/jest-dom`, axe는 opt-in(D-33; showcase 없음).
- 스모크 앱 `packages/ui/smoke/next-app/`(`private: true`, 게시 안 함): tarball 설치 후 `@import "@kor-travel/tokens/theme.css"` + `@source "../node_modules/@kor-travel/ui"` 2줄로 `next build --webpack`과 `next build`(Next 16 기본 Turbopack)를 실행. CI `packages` job(T-101이 만든 job)에 ui 단계를 추가.
- 게이트 스크립트 `packages/ui/scripts/check-directives.mjs`(dist 첫 줄 지시문을 소스와 대조)·`check-kt-classes.mjs`(패키지 클래스가 `kt-` 접두 유틸리티와 레이아웃 유틸만 쓰는지 grep; T-103 `ux_lint` 금지 7종도 적용).
- base-ui 사실 확인 3건: `@base-ui/react` 1.8.0 소스에서 (1) `Button`이 `type="button"`을 기본 부여하는지 (2) `Checkbox`가 폼 제출용 hidden `<input>`을 두는지 (3) Toast API 유무·형태를 확인하고 버전·파일·행을 evidence에 기록한다. 결과는 T-204·T-205·T-206의 입력이다.

## 범위 밖

- 컴포넌트 구현(T-203 이후), overlay 구현(T-206), DataTable peer(T-208), 레지스트리 채널(T-211).
- React 18 지원(`forwardRef`)·CommonJS 출력·소스 TS 배포(`transpilePackages`) — D-09와 선행 보고서 E4·E6에 따라 미지원.
- npm 공개 게시·Renovate(T-507), 아이콘 전체 세트(필요한 컴포넌트 task에서 추가).

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다.

```text
packages/ui/package.json
packages/ui/tsconfig.json
packages/ui/vitest.config.ts
packages/ui/README.md
packages/ui/LICENSE  packages/ui/NOTICE  packages/ui/THIRD_PARTY_NOTICES.md  (루트 사본)
packages/ui/src/index.ts  packages/ui/src/cn.ts  packages/ui/src/cn.test.ts
packages/ui/src/icons/*.tsx
packages/ui/scripts/check-directives.mjs  packages/ui/scripts/check-kt-classes.mjs
packages/ui/smoke/next-app/{package.json,next.config.ts,app/globals.css,app/page.tsx}
package.json  package-lock.json  (루트 workspace lock 갱신)
.github/workflows/packages.yml  (ui 단계)
THIRD_PARTY_NOTICES.md  PROVENANCE.md  (lucide·cva 항목)
```

## 수용 기준

- `npm run build -w packages/ui`가 `dist/**/*.js` + `*.d.ts`를 생성하고 `check-directives.mjs`가 지시문 불일치 0을 보고한다.
- `npx tsc --noEmit -p packages/ui`가 `noUncheckedIndexedAccess: true`에서 오류 0.
- `cn` 단위 테스트: `cn("p-2", "p-4") === "p-4"`, `cn("text-kt-2xs", "text-kt-sm") === "text-kt-sm"`, `cn("bg-kt-surface-page", "text-kt-primary")`는 두 클래스를 모두 유지.
- `npm pack` tarball 목록에 `LICENSE`·`NOTICE`·`THIRD_PARTY_NOTICES.md`·`dist/`가 있고 `src/`·`smoke/`가 없으며, `react`·`lucide-react`가 dependencies와 번들 어디에도 없다. `license` 필드가 `GPL-3.0-or-later`.
- 스모크 앱이 tarball 설치본으로 `next build --webpack`·`next build` 모두 exit 0이며 산출 CSS에 `kt-` 유틸리티(예: `.bg-kt-surface-page`)가 실제로 포함된다.
- base-ui 3건의 확인 결과가 버전·파일·행과 함께 기록된다. 미확인이 남으면 이 task는 DONE이 될 수 없고 T-212 릴리스가 차단된다.
- `packages/ui` 모든 소스 파일에 SPDX 헤더가 있다(`tools/check_spdx.py`; T-003 잔여로 도구가 없으면 `NOT_RUN(check_spdx 미구현)` + 수동 grep 결과).

## 검증 명령

```bash
npm ci
npm run build -w packages/ui
node packages/ui/scripts/check-directives.mjs
node packages/ui/scripts/check-kt-classes.mjs
npx tsc --noEmit -p packages/ui
npm run test -w packages/ui
npm pack -w packages/ui --pack-destination /tmp/kt-ui && tar tzf /tmp/kt-ui/kor-travel-ui-*.tgz
cd packages/ui/smoke/next-app && npm install /tmp/kt-ui/kor-travel-ui-*.tgz && npx next build --webpack && npx next build
python3 -B -X utf8 tools/check_spdx.py packages/ui
```

## evidence

PR 본문과 `docs/journal.md`에 Node·npm·TypeScript·Next 버전, 각 명령의 exit code, tarball 파일 목록과 sha256, 스모크 빌드 로그 요약, base-ui 3건 확인표(`@base-ui/react@<ver>`, 파일, 행, 결론)를 남긴다. 실행하지 못한 검증은 `NOT_RUN(사유)`로 적는다(D-25; 명령을 적은 것은 실행 증거가 아니다).

## rollback 또는 release 차단 조건

- 골격 PR은 단일 revert로 되돌린다(게시 전이므로 소비자 영향 없음).
- 차단: Turbopack·webpack 중 하나라도 실패, 지시문 유실, base-ui 3건 중 미확인 존재, `react`가 dependencies나 번들에 포함, tarball 라이선스 파일 누락. 하나라도 남으면 T-212 rc 태그를 만들지 않는다.
