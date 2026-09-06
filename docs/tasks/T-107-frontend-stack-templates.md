# T-107 docs/standards/frontend-stack.md 확정 + `templates/eslint/*.mjs`·tsconfig base·postcss·components.json 조각

- 상태: IN_PROGRESS
- 우선순위: P1
- Gate: 2인 리뷰
- 선행: 없음

## 목표

프론트엔드 스택 규칙의 정본 `docs/standards/frontend-stack.md`(규칙 ID `FS-n`)와, `config` npm 패키지를 만들지 않는 대신 배포하는 설정 조각(ESLint flat config `.mjs`·tsconfig base·postcss·`components.json`)을 만든다. 이번 PR에서는 문서를 초안으로 산출하고(브리프 §7) 조각과 함께 2인 리뷰로 확정한다.

## 고정 결정

- [설계 브리프](../plan/design-brief.md) D-01(`config` 패키지 없음 → `templates/eslint/*.mjs` + `frontend-stack.md`), D-06(Next 16.2/16.3.4·React 19·TS 5.9.3·Tailwind 4.3·base-ui 1.8·shadcn 4.21 devDependencies·ESLint 9/10·typescript-eslint 8·Vitest 4.1·Playwright 1.63·openapi-typescript 7.x), D-08(Tailwind v4 CSS-first, `@config` 잔존 정리), D-09(overlay만 base-ui·비-overlay native·React 19 전용), D-10(`@source`·`noUncheckedIndexedAccess`·webpack/Turbopack 양쪽), D-33(vitest + RTL + jsdom), O-6.
- ADR-007·ADR-008 — [docs/adr/README.md](../adr/README.md). 버전 값은 [versions.md](../standards/versions.md)·`versions.json`이 정본이며 이 문서는 값을 복제하지 않는다.
- 근거: [버전 매트릭스](../survey/cross/version-matrix.md) §1.2~§1.6(스택·린트·테스트 현황)·§5.3(breaking 근거)·§6(airport TS 7), [UI 컴포넌트 조사](../survey/cross/ui-components.md) §2.3(스택 매트릭스)·§6.1(`components.json` 현황: `base-nova`·base-ui), [map 인벤토리](../survey/inventory/kor-travel-map.md) §3.1(`verify:frontend-eslint` 집합·react-doctor·exact 핀)·§9, [airport 인벤토리](../survey/inventory/kor-travel-airport.md) §3.2(`cn` 패키지·devDeps 위치·autoprefixer 없음), [weather 인벤토리](../survey/inventory/kor-travel-weather.md) §9(`moduleResolution: node`), [실패 패턴](../runbooks/agent-failure-patterns.md) `@source`·`@config` 행.
- 헤더는 T-003 SPDX 규약(조각 파일에도 적용).

## 구현 범위

1. `docs/standards/frontend-stack.md`: FS-1 런타임·패키지 매니저(Node 22·npm; lockfile v3 의무) / FS-2 Next·React 19(React 18 앱은 tokens부터) / FS-3 TypeScript(`strict`·`noUncheckedIndexedAccess`·`moduleResolution: bundler`; TS 7 예외 O-6) / FS-4 Tailwind v4 CSS-first(`@import "tailwindcss"` → `@kor-travel/tokens/theme.css` → `@source`; `@config` 금지(common 도입 앱); `tw-animate-css` 선택) / FS-5 shadcn(CLI devDependencies, `style: base-nova`, 소스 소유·레지스트리 채널 범위) / FS-6 프리미티브 엔진(overlay base-ui 1.8·비-overlay native + `useRender`) / FS-7 `cn` = clsx + tailwind-merge(`@kor-travel/ui/cn`, `cn` 패키지 금지) / FS-8 ESLint flat config(조각 사용·`--max-warnings=0`) / FS-9 테스트(vitest 4·RTL·jsdom·axe opt-in; Playwright 1.63) / FS-10 typegen(`openapi-typescript` 7.x, `gen:types`/`gen:types:check`) / FS-11 빌드 검증(webpack·Turbopack 양쪽 `next build`) / 예외·열림 표.
2. `templates/eslint/base.mjs`(typescript-eslint 8 recommended-type-checked 부분집합 + import 정렬), `templates/eslint/next.mjs`(`eslint-config-next` 16 결합·`react-hooks`), 각 파일 머리에 사용법 주석; `templates/eslint/README.md`는 versions-conventions 작성자 소유(행 추가만 요청).
3. `templates/tsconfig.base.json`(`strict`, `noUncheckedIndexedAccess`, `moduleResolution: bundler`, `verbatimModuleSyntax`), `templates/postcss.config.mjs`(`@tailwindcss/postcss` 단일), `templates/components.json`(`style: base-nova`, `cssVariables: true`, `iconLibrary` 미사용 표기, aliases `@/components`·`@/lib/utils`, `registries: {}`).
4. `tests/test_templates_syntax.py`: `node --check` 각 `.mjs`, `json.load` 각 `.json`(stdlib + Node 22).

## 범위 밖

- `ui-contract.md`(T-204), 실제 ESLint 실행 fixture(T-010 `tests/fixtures/node-app`에서 조각을 소비하도록 후속), 소비자 적용(T-403·T-433·T-460·T-470), 버전 값 갱신(T-507).

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다. `docs/standards/frontend-stack.md`, `templates/eslint/base.mjs`, `templates/eslint/next.mjs`, `templates/tsconfig.base.json`, `templates/postcss.config.mjs`, `templates/components.json`, `tests/test_templates_syntax.py`, `docs/standards/README.md`(행 추가·standards-fe 소유), `templates/README.md`(행 추가·versions-conventions 소유).

## 수용 기준

- FS 규칙마다 MUST/SHOULD·근거 절이 있고 버전 숫자는 `versions.md` 링크로만 나온다(`rg "16\.3\.4|19\.2\.8"` 0건).
- FS-7이 `cn` npm 패키지 사용을 금지하고 airport WIP 정렬(T-430)과 연결된다.
- 조각 5개가 `node --check`·`json.load`를 통과하고 SPDX 헤더를 갖는다(`check_spdx.py` exit 0).
- `templates/components.json`이 map·geo·concierge·airport WIP의 `base-nova` 스타일과 base-ui 엔진에 정합한다(`ui` §6.1 표 대조).
- validator 오류 0, 리뷰어 2인(프론트 툴체인 · 소비자 이관) verdict `PASS`, 초안 문장 제거.

## 검증 명령

```bash
python3 -B -X utf8 tools/validate_document_links.py
python3 -B -X utf8 -m unittest discover -s tests -p "test_templates_syntax.py" -v
for f in templates/eslint/*.mjs templates/postcss.config.mjs; do node --check "$f" && echo "ok $f"; done
python3 -c "import json;[json.load(open(p)) for p in ['templates/tsconfig.base.json','templates/components.json']];print('json ok')"
python3 -B -X utf8 tools/check_spdx.py
rg -n "16\.3\.4|19\.2\.8|5\.9\.3" docs/standards/frontend-stack.md || echo "no version literals"
```

Git Bash에서 동일.

## evidence

- 검증 출력·리뷰 report(`docs/reviews/adversarial/YYYY-MM-DD-frontend-stack.md`)를 이 절과 `docs/journal.md`에 남긴다.

## rollback 또는 release 차단 조건

- 문서·템플릿만 바뀌므로 `git revert` 1회로 원복한다.
- 조각이 문법 검사에 실패하거나 `@config` 허용 문구가 들어가면 merge하지 않는다(D-08·실패 패턴 "같은 utility 이름 두 값" 재발 방지).
