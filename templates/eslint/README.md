# templates/eslint — ESLint 설정 조각(T-107)

이 디렉터리는 소비 저장소가 `eslint.config.mjs`에서 import하거나 복사해 쓰는 **설정 조각**을 담는다. `config` npm 패키지는 만들지 않는다(브리프 D-01: `templates/eslint/*.mjs` 조각 + `docs/standards/frontend-stack.md`로 대체). 조각 실물(`*.mjs`)은 T-107(`frontend-stack.md` 확정)에서 작성하며, 이 README는 그 조각의 목록·역할·버전 전제만 정한다. 실물이 없는 동안 이 문서는 "후보"이며 소비 저장소는 자기 `eslint.config.mjs`를 유지한다.

- 정본 지위: 조각 파일 목록·구성 순서의 정본(후보). 규칙 내용의 정본은 [frontend-stack](../../docs/standards/frontend-stack.md).
- 확정 task: T-107(조각 실물), T-005(버전 축 `eslint`·`typescript-eslint`).
- 마지막 갱신: 2026-09-06.

## 1. 조각 목록(후보)

| 파일 | 역할 | 적용 대상 | 근거 |
|---|---|---|---|
| `base.mjs` | flat config 공통 베이스: `@eslint/js` recommended, `typescript-eslint` recommended(type-aware는 앱 opt-in), `import-x` 순서·중복 금지, 보고 형식 | 전 프론트엔드 | map admin 설정(`@next/eslint-plugin-next` + `typescript-eslint ^8.65` + `eslint-plugin-{react-x,react-dom}` + `import-x` + `jsx-a11y-x` + `react-hooks ^7`)이 원형 — `docs/survey/cross/version-matrix.md` §1.6 |
| `next.mjs` | `@next/eslint-plugin-next` core-web-vitals + `react-hooks` 7 | Next 16 앱 | `eslint-config-next 16` peer `eslint >=9` — vm §1.6 |
| `react.mjs` | `eslint-plugin-react-x`·`react-dom`·`jsx-a11y-x` | React 19 앱 | map 설정 |
| `kt-style-guard.mjs` | 금지 패턴 7종의 ESLint 대응 규칙(raw hex/oklch 클래스, `text-[Npx]`, `rounded-2xl+`, 팔레트 alpha, `outline-none`, `transition-all/colors`, `aria-disabled:opacity-`) + `window.confirm` 금지 | tokens·ui 채택 앱 | `docs/standards/ux-guide.md` 금지 패턴(D-13); pinvi Hallmark 클래스 가드 선례 — `docs/survey/inventory/pinvi.md` §8-7 |
| `test.mjs` | vitest·testing-library 파일 오버라이드 | 테스트 파일 | — |

`tools/ux_lint.py`(T-103)가 전체 report·diff-based fail의 정본 게이트이며, `kt-style-guard.mjs`는 편집기 즉시 피드백용 보조다. 두 규칙 집합이 어긋나면 `ux_lint.py`가 정본이다.

## 2. 구성 순서(후보)

```js
// eslint.config.mjs (소비 저장소)
import base from "./eslint/base.mjs";          // 복사본 또는 common tarball의 templates/eslint 경로
import next from "./eslint/next.mjs";
import react from "./eslint/react.mjs";
import ktStyleGuard from "./eslint/kt-style-guard.mjs";
import test from "./eslint/test.mjs";

export default [
  { ignores: [".next/**", "node_modules/**", "dist/**", "coverage/**", "playwright-report/**"] },
  ...base,
  ...next,
  ...react,
  ...ktStyleGuard,
  ...test,
  // 앱 로컬 규칙은 항상 마지막에 둔다. 조각 파일은 수정하지 않는다.
];
```

- 조각은 **복사**해 쓰고 수정하지 않는다(drift 비교는 선두 주석 블록을 정규화한 뒤 수행 — D-17). 변경이 필요하면 common PR.
- `next lint`는 Next 16에서 제거됐으므로 스크립트는 `eslint .`로 둔다(vm §5.3).
- 경고 0을 요구하는 앱(map `verify:frontend-eslint`)은 `--max-warnings 0`을 자기 스크립트에 둔다. 조각은 severity를 `error`/`warn`으로만 정하고 CI 실패 여부는 앱이 정한다.

## 3. 버전 전제

| 축 | floor | recommended | 근거 |
|---|---|---|---|
| eslint | 9.0 | 10.x | `versions.json` axes.eslint; ktdm 8은 T-470 |
| typescript-eslint | 8.0 | 8.x | peer `typescript <6.1.0` — vm §1.6 |
| eslint-plugin-react-hooks | — | 7.x | Next 16·React 19 동반 |
| @next/eslint-plugin-next | — | 16.3.x | Next 축과 동일 minor |

TypeScript 7(airport)은 typescript-eslint 지원 범위 밖이므로 airport는 ESLint 도입 판정(T-433)과 함께 결정한다.

## 4. 범위 밖

- Prettier·`ruff format` 같은 포맷 규칙(D-15 C20: format 규칙 미포함; 재포맷 금지 — T-470).
- 앱 도메인 규칙(import 경계·금지 모듈)은 앱 `eslint.config.mjs`.
- Python 품질 베이스(ruff `extend`·mypy strict·import-linter)는 `packages/py/kor-travel-common` C20 산출물(T-305)이며 이 디렉터리와 무관하다.
