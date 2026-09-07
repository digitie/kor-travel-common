# 소비 저장소 채택 Runbook (consumer adoption)

이 문서는 소비 저장소(kor-travel-*, pinvi)가 common의 패키지·규칙·CI 템플릿을 채택하거나 버전을 올릴 때의 표준 절차 정본이다(브리프 D-10·D-11·D-16·D-19·D-21·D-24·D-25, ADR-010). 확정 task는 T-007(문서 초기판)이며, 패키지 실물(T-101·T-201·T-302)과 매니페스트 스키마(T-011), 기준선 템플릿(T-108)이 생기면 명령·필드명을 대조해 확정한다. 마지막 갱신 2026-09-06.

앱별 특이사항은 이 문서에 쓰지 않고 §10의 링크로만 가리킨다. common 쪽 작업 절차는 [agent workflow](agent-workflow.md), 버전 발행은 [release](release.md), 계약의 정본은 [standards](../standards/README.md)다. 명령은 bash 기준이며 Git Bash에서 동일하다.

## 0. 적용 범위와 원칙

| 산출물 | 형태 | 정본 |
|---|---|---|
| tokens | npm `@kor-travel/tokens`(`tokens.css`·`theme.css`·`shadcn.css`·`base.css`·`base.scoped.css`·`dark-class.css`·`dark-media.css`·`aliases/map-vocabulary.css`, 생성물 `tokens.json`·`tokens.ts`·`tailwind-preset.cjs`) | [design tokens](../standards/design-tokens.md) |
| ui | npm `@kor-travel/ui`(ESM + d.ts + Tailwind 소스 클래스, React 19 전용) | [ui contract](../standards/ui-contract.md) |
| py | PyPI 이름 `kor-travel-common`, import `kortravelcommon`, extras `[api]`·`[db]`·`[dagster]`·`[testing]`·`[http]` | [backend stack](../standards/backend-stack.md), [openapi](../standards/openapi.md) |
| 규칙 문서 | `docs/standards/*`의 규칙 ID(`TK-n`·`UX-Gn.m` 등)와 예외 레지스트리 | [standards](../standards/README.md) |
| CI 템플릿 | 재사용 워크플로(`versions-check`·`contrast-check`·`docs-check` → `openapi-drift`·`typegen-drift` → `node-quality`·`python-quality`), `templates/*` | [ci-deploy](../standards/ci-deploy.md), [templates](../../templates/README.md) |
| 매니페스트 | `kor-travel-common.lock.json`(schema `kor-travel-common.consumer-manifest.v1`) | [versions](../standards/versions.md), §9 |

원칙(D-24): 한 PR = 한 산출물, 프레임워크 업그레이드 PR과 분리, `git revert` 1회로 원복, lock 동반 커밋, 파일 상한(tokens 10·ui 30·py 10; 초과 시 분할). 토큰·스타일·셸을 바꾸는 PR은 시각 기준선(§5)을 PR evidence로 남긴다(D-21). 확정 패키지 식별자와 파일 배포 채널은 [packages](../architecture/packages.md#1-요약표)를 따른다. 공개 npm/PyPI 계정·이름 확보는 채택 gate가 아니다(ADR-014).

## 1. 사전 조건 확인

| 항목 | 확인 방법 | 통과 조건 | 근거 |
|---|---|---|---|
| 라이선스 gate | 저장소 루트 `LICENSE`·`package.json`/`pyproject.toml` `license` 필드 | GPL-3.0-or-later 정렬. pinvi는 T-020(O-1), concierge·docker-manager는 T-021(O-2) 전에는 규칙 문서·`tokens.json` 의미 이름 참조까지만 허용하고 코드 채택 금지 | D-16·D-17, [licensing](../standards/licensing.md), `docs/survey/cross/licensing.md` §3.6·§4 B1 |
| 버전 기준선 | `python3 -B -X utf8 tools/check_versions.py <소비자 저장소 루트> --manifest <소비자 저장소 루트>/<앱 경로>/kor-travel-common.lock.json`(report 모드) | `BELOW_FLOOR`·`BLOCKED`·`FLOATING_REF` 0(등록된 `exceptions[]` 제외). ui는 React `^19.0.0` 필수(React 18 앱은 tokens부터), `theme.css`는 Tailwind 4.3+ 필수 | D-06·D-07·D-09·T-011, [versions](../standards/versions.md) |
| lockfile | `package-lock.json`(`lockfileVersion: 3`)·`uv.lock` 존재, lock 항목 `integrity` 보유 | 존재 + `npm ci`/`uv sync --locked` 재현 | D-07, `docs/survey/cross/version-matrix.md` §3.6(pinvi `check-lockfile-integrity.mjs` 선례) |
| 릴리스 자산 | `gh release view <tag> --repo digitie/kor-travel-common` | 태그가 존재하고 tarball/wheel + `SHA256SUMS`가 첨부됨. `-rc.N`은 검증 PR에만, 정식 태그만 merge | D-11, [release](release.md) §2 |
| Tailwind 상태 | `@import "tailwindcss"` 유무, `@config` 잔존, `source(none)` | v4 미도입 앱(weather, airport main)은 `tokens.css`만 채택(Phase 1), `@config` 잔존 앱(geo·concierge·pinvi web)은 §4.3 정리 항목 포함 | D-08, `docs/survey/cross/version-matrix.md` §1.2 |
| 기준선 상태 | 대상 브랜치 최신, 소비자 CI green, 작업 트리 clean | 사용자 변경과 채택 diff를 섞지 않음 | [agent workflow §1](agent-workflow.md#1-범위와-기준선-확정) |

사전 조건 중 하나라도 실패하면 채택 PR을 열지 않는다. 예외가 필요하면 먼저 common PR로 `versions.json` `exceptions[]`(`repo`·`key`·`installed`·`reason`·`until`·`review` 필수)를 등록한다.

## 2. 브랜치

소비 저장소 자체의 브랜치 명명을 따른다(common은 소비자 원장·브랜치 형식을 규정하지 않는다, D-05). 권장은 `agent/<agent>-T-4NN-<산출물>`처럼 common task ID를 포함하는 이름이다. 채택 브랜치에는 그 산출물 외의 변경(포맷 일괄 수정, 무관한 의존성 상향)을 섞지 않는다.

## 3. 설치

### 3.1 npm(tokens·ui)

GitHub Release 자산 tarball URL로 설치하고 lock의 `resolved`·`integrity`를 커밋한다. `@main`·branch·`latest` 참조는 금지다.

```bash
TAG=tokens-v0.1.0
ASSET=kor-travel-tokens-0.1.0.tgz
BASE=https://github.com/digitie/kor-travel-common/releases/download/$TAG
curl -fsSLO "$BASE/SHA256SUMS" && curl -fsSLO "$BASE/$ASSET"
sha256sum -c SHA256SUMS --ignore-missing
npm install "$BASE/$ASSET"
git diff --stat package.json package-lock.json
```

- 모노레포(map·pinvi)는 workspace 디렉터리에서 `npm install --workspace <경로> <URL>`로 설치하거나 루트에서 workspace를 지정한다. lock은 루트 `package-lock.json` 하나다.
- ui는 `@kor-travel/tokens`를 호환 minor 하나로 peer 요구한다(D-31). tokens를 먼저 채택하고 같은 PR에서 상향하지 않는다.
- 설치 후 `npm ls @kor-travel/tokens @kor-travel/ui`로 단일 버전인지 확인한다. 중복 설치는 CSS 변수 이중 정의의 원인이 된다.
- `.npmrc`나 registry 설정 변경은 필요 없다(tarball URL 설치).

### 3.2 Python(py)

```bash
uv add "kor-travel-common @ git+https://github.com/digitie/kor-travel-common.git@py-v0.1.0#subdirectory=packages/py/kor-travel-common"
# extras가 필요하면
uv add "kor-travel-common[api] @ git+https://github.com/digitie/kor-travel-common.git@py-v0.1.0#subdirectory=packages/py/kor-travel-common"
uv lock && uv sync --locked
uv run python -c "import kortravelcommon; print(kortravelcommon.__version__)"
```

- `uv.lock`에 커밋 sha가 고정된다. Docker 빌드 스테이지에는 `git`이 있어야 하며, 없으면 Release의 wheel 자산 URL(`.../py-v0.1.0/kor_travel_common-0.1.0-py3-none-any.whl`)로 바꾼다([failure patterns](agent-failure-patterns.md)).
- Poetry(docker-manager)·`requirements.txt`(concierge)는 uv 전환 task(T-471·T-450)가 선행이다. 전환 전에는 py를 채택하지 않는다.
- CI와 Docker 모두 `uv sync --locked`로 설치한다(D-06 lockfile 의무).

### 3.3 규칙 문서·CI 템플릿

- `AGENTS.md` 공통 절, PR 템플릿, dependabot, ESLint 조각 등은 `templates/`에서 복사하고 원본 경로·common 커밋을 파일 머리 주석에 남긴다. 목록과 복사 규칙은 [templates](../../templates/README.md)가 정본이다.
- 재사용 워크플로는 태그 또는 SHA로만 참조하고(`uses: digitie/kor-travel-common/.github/workflows/versions-check.yml@<tag|sha>`), 기존 워크플로에 job을 추가하는 방식으로 넣는다(전면 대체 금지). required check 이름은 `name:` 입력으로 기존 이름을 보전한다(D-18). 참조 태그 형식은 T-010에서 확정하며 그 전에는 SHA를 쓴다.
- 규칙 문서 채택은 코드 채택과 독립이다. 라이선스 gate가 닫힌 앱(concierge·docker-manager·pinvi)도 규칙 ID 참조와 예외 등록은 가능하다.

## 4. 등록(CSS·Tailwind·Python)

### 4.1 필수 2줄(Tailwind v4 앱)

```css
@import "tailwindcss";
@import "@kor-travel/tokens/theme.css";
@source "../node_modules/@kor-travel/ui";
```

`theme.css`는 `@import "tailwindcss"` 뒤에 둔다. `@source`는 ui를 채택한 앱만 필요하며 경로는 **CSS 파일 기준 상대 경로**다. 파일 구성(`tokens.css`·`shadcn.css`·`base.css`/`base.scoped.css`·`dark-*.css`·앱 오버라이드·`aliases/map-vocabulary.css`)과 import 순서는 [design tokens](../standards/design-tokens.md)가 정본이고, 이 문서는 "어디에 적는가"만 다룬다.

| 앱 | CSS 진입 파일(조사 기준) | `node_modules` 위치(추정) | `@source` 경로 후보 |
|---|---|---|---|
| map admin | `packages/kor-travel-map-admin/frontend/src/app/globals.css` | 저장소 루트(npm workspaces hoist) | `../../../../../node_modules/@kor-travel/ui` |
| pinvi web | `apps/web/app/globals.css` | 저장소 루트(npm workspaces) | `../../../node_modules/@kor-travel/ui` |
| weather admin | `packages/kor-travel-weather-admin/frontend/app/globals.css` | `frontend/` | `../../node_modules/@kor-travel/ui` |
| geo ui | `kor-travel-geo-ui/app/globals.css` | `kor-travel-geo-ui/` | `../../node_modules/@kor-travel/ui`(`source(none)` 앱이므로 명시 `@source` 필수) |
| concierge | `frontend/src/app/globals.css` | `frontend/` | `../../../node_modules/@kor-travel/ui` |
| docker-manager | `frontend/src/app/globals.css` | `frontend/` | `../../../node_modules/@kor-travel/ui` |
| airport | `frontend/src/app/globals.css` | `frontend/` | `../../../node_modules/@kor-travel/ui` |

진입 파일 경로의 근거는 `docs/survey/cross/licensing.md` §2.3(M6·P4·W1·G1·C1·T1·K1)이며, hoist 위치는 추정이므로 채택 PR에서 `ls <상대 경로>/package.json`으로 실제 경로를 확인하고 PR 본문에 적는다.

### 4.2 Tailwind 미도입 앱(weather Phase 1, airport main)

```css
@import "@kor-travel/tokens/tokens.css";
@import "@kor-travel/tokens/aliases/map-vocabulary.css"; /* map 어휘를 쓰는 앱만 */
@import "./brand.css"; /* 앱 오버라이드: brand 4·focus·paper 4·ink 4·status·font 스택만 */
```

값 무변경이 목표이므로 앱의 `tokens.css`를 삭제하고 shim + 오버라이드로 같은 실효값이 나오는지 §4.4로 검증한다.

### 4.3 제거·정리 항목

| 항목 | 이유 | 대상 앱 |
|---|---|---|
| `@config "tailwind.config.ts"`와 `theme.extend`의 같은 utility 이름 | `@theme`과 config가 같은 이름을 두 값으로 해석함([failure patterns](agent-failure-patterns.md)) | geo·concierge·pinvi web |
| `tailwind.config.ts` 자체 | `@theme` 단일화 후 삭제(geo는 실효값 검증 후, D-08 ③) | geo |
| hex fallback 블록 | `--ktc-*`를 `--kt-*` 오버라이드로 재해석한 뒤 불필요(D-08 ④) | concierge |
| 앱 `tokens.css`의 map 값 복사본 | common `tokens.css`가 정본; 앱에는 오버라이드만 남김 | weather·pinvi admin(`--color-admin-*`)·docker-manager(`@theme`) |
| 앱 `cn` 구현(`cn` 패키지 등) | `@kor-travel/ui/cn`(clsx + `extendTailwindMerge`) 재수출로 교체; pinvi는 `cn` 재수출 유지 | airport WIP·pinvi |
| `lucide-react` peer 기대 | ui는 인라인 SVG를 가져 peer가 없다(D-01). 앱이 직접 쓰는 lucide는 그대로 둔다 | 전 앱 |

### 4.4 실효값 확인

토큰 채택 PR은 "값 무변경"이 acceptance이므로 빌드 산출 CSS에서 `--kt-*`와 앱 별칭의 실효값을 채택 전후로 비교한다.

```bash
# 채택 전(기준선 commit)과 후에 각각 실행해 두 파일을 diff한다. 출력 위치는 gitignore된 디렉터리를 쓴다.
npx @tailwindcss/cli@4 -i <CSS 진입 파일> -o /tmp/kt-effective-after.css
grep -oE -- '--(kt|color|radius|spacing|text)-[a-z0-9-]+: *[^;]+' /tmp/kt-effective-after.css | sort -u > /tmp/kt-after.txt
diff /tmp/kt-before.txt /tmp/kt-after.txt
```

Tailwind가 없는 앱은 `next build` 후 `.next/static/css/*.css`를 같은 방식으로 비교한다. diff가 0이 아니면 각 줄을 "의도한 오버라이드"로 설명할 수 있어야 하고, 설명할 수 없는 diff는 해당 단계를 revert한다(D-08 중단 조건).

### 4.5 Python 등록

모듈별 등록 지점(FastAPI 팩토리, health 라우터 alias, `X-Request-ID` 미들웨어 `trust_incoming`, ruff `extend`, import-linter 계약)은 [backend stack](../standards/backend-stack.md)이 정본이다. 채택 PR은 계약 무변경(응답 본문·경로 불변, additive만)을 확인하고 OpenAPI export를 `--check`로 대조한다(D-14 M1). map OpenAPI 산출물이 바뀌면 pinvi·docker-manager의 sha256 pin 갱신 PR을 동반하지 않는 한 merge하지 않는다.

## 5. 시각 기준선(D-21)

토큰·스타일·셸을 바꾸는 소비자 PR은 착수 전 기준선 스크린샷과 완료 후 diff를 **PR evidence**로 남긴다(저장소 파일로 커밋하지 않는다).

| 항목 | 값 |
|---|---|
| 검사 폭 | 320 / 375 / 414 / 768 / 1024 / 1440 px([responsive web](../standards/responsive-web.md)) |
| 대상 화면 | 셸(rail 펼침·접힘), 목록(표), 상세, 폼, 로그인, 빈 상태·오류 상태 — 앱의 e2e가 이미 여는 화면을 우선 |
| 도구 | 앱의 Playwright; 없는 앱(weather·docker-manager)은 `templates/playwright.baseline.ts`(T-108)를 앱 e2e 디렉터리에 복사해 실행 |
| 기준선 시점 | 채택 브랜치 분기 commit(사용자 변경 제외)에서 캡처하고 commit hash를 evidence에 기록 |
| 완료 조건 | 값 무변경 단계는 픽셀 diff 0. 컴포넌트 교체 단계는 의도한 차이 목록과 스크린샷 쌍 |
| 실행 불가 | 브라우저를 띄울 수 없으면 `NOT_RUN(사유)`로 적고 task를 `DONE`으로 바꾸지 않는다(D-25) |

캡처·비교 명령의 인자는 템플릿 파일 머리 주석이 정본이다(T-108 산출). 실행 결과 요약(폭별 diff 픽셀 수·스크린샷 저장 위치·commit)을 PR 본문 §5 evidence에 적는다.

## 6. 검증 사다리(소비자 측)

변경 범위에 맞는 계층만 실행하고, 실행하지 않은 계층은 `NOT_RUN(사유)`로 PR에 남긴다.

| 순서 | 계층 | 명령(앱 스크립트 이름은 앱 정본) | 통과 조건 |
|---|---|---|---|
| 1 | 설치 무결성 | `sha256sum -c SHA256SUMS --ignore-missing`, `npm ci`, `uv sync --locked` | 오류 0, lock diff가 채택 항목뿐 |
| 2 | 타입 | `npx tsc --noEmit`, `npm run gen:types:check`(typegen 앱), `uv run mypy` | 오류 0 |
| 3 | 단위 | `npm test`(vitest), `uv run pytest` | 실패 0, 테스트 수가 채택 전과 같거나 증가 |
| 4 | 빌드 | `npm run build`(앱이 쓰는 번들러 그대로: webpack 또는 Turbopack) | 성공, CSS 산출물에 `--kt-*` 존재 |
| 5 | e2e | `npx playwright test` | green; `data-testid`·heading·sr-only 셀렉터 계약 유지([ui contract](../standards/ui-contract.md)) |
| 6 | 시각 diff | §5 | diff 0 또는 의도 목록 |
| 7 | 버전 report | `python3 -B -X utf8 tools/check_versions.py --manifest kor-travel-common.lock.json` | `BELOW_FLOOR`·`BLOCKED`·`FLOATING_REF` 0(예외 제외) |
| 8 | 대비 | `python3 -B -X utf8 tools/kt_contrast.py --override <brand.css> --baseline contrast-baseline.json`(T-103) | 신규 미달 0(기존 미달은 `until` 있는 baseline) |
| 9 | UX lint | `python3 -B -X utf8 tools/ux_lint.py --base <분기 commit>`(T-103) | diff 기준 신규 위반 0 |
| 10 | OpenAPI | export `--check`, drift 워크플로(T-309) | 산출물 무변경 또는 pin 갱신 PR 동반 |
| 11 | 배포 스모크 | 소비자 저장소 배포 runbook(n150 등) | 앱 정본 기준. common task에는 `NOT_RUN(소비자 배포)`로 기록 |

`tools/*.py`는 common 체크아웃에서 실행한다(`python3 -B -X utf8 /path/to/kor-travel-common/tools/check_versions.py …`). 재사용 워크플로를 붙인 앱은 7·8·9를 CI job으로 대체할 수 있고, 로컬 실행 결과와 CI 결과가 다르면 CI가 정본이다.

## 7. PR 본문(소비자)

소비자 PR 본문은 `templates/consumer-pr.md`가 정본이다([templates](../../templates/README.md)). 최소 항목은 다음과 같다.

- 산출물·버전·태그·자산 digest(`SHA256SUMS`의 해당 행)
- common task ID(T-4xx)와 이 PR이 닫는 gate
- 변경 파일 목록(파일 상한 이내), 제거한 항목(§4.3)
- 검증 사다리 결과 표(명령·수치·exit code; `NOT_RUN(사유)` 포함)
- 시각 기준선 commit·폭별 diff·스크린샷 위치
- 매니페스트·예외 등록 diff(§9)
- 되돌리기 명령(§8)

기존 소비자 PR 템플릿(동기/변경/영향/검증/문서/관련)을 쓰는 앱은 위 항목을 해당 절에 끼워 넣는다.

## 8. 되돌리기

- merge 전: 채택 브랜치를 닫는다. 기준선 스크린샷과 실패 원인은 common task의 evidence에 남긴다.
- merge 후: `git revert -m 1 <merge commit>`(squash merge면 `git revert <commit>`) 1회로 원복되어야 한다(D-24). revert 커밋에 lock 변화가 포함되는지 `git show --stat`으로 확인한다.
- Python은 revert 뒤 `uv sync --locked`가 통과해야 한다. lock이 손으로 수정됐다면 `uv lock`을 다시 실행해 revert 커밋에 포함한다.
- 되돌리기 뒤 매니페스트(§9)의 버전 필드도 함께 원복하고, common `consumers.pins.json`을 갱신했다면 common PR로 되돌린다.
- 되돌리기 판단 기준: 원인 불명 시각 diff, e2e red, `check_versions` `BLOCKED`, 소비자 배포 스모크 실패, common 릴리스 회수([release §4](release.md#4-회귀-시-되돌리기)).

## 9. 매니페스트·integration-map 갱신

각 소비 저장소(모노레포는 앱 디렉터리)에 `kor-travel-common.lock.json`을 두고 채택·상향 PR마다 갱신한다(D-19). `lockfiles.path`는 저장소 루트 기준이며 검사 호출에는 저장소 루트와 manifest 경로를 함께 전달해 shared lock과 루트 workflow를 읽는다. npm `scope`가 `root`이면 해당 lockfile의 루트 package, 그 밖이면 lockfile 기준 workspace 멤버 package를 선택한다. lock이 없는 선언 전용 앱은 빈 `lockfiles`와 `app` 경로로 선언을 남기고 report에서 `NO_LOCK`을 확인한다. `enforce`는 매니페스트에 두지 않으며 common `versions.json`의 `consumers.<repo>.enforce`가 소유한다(D-07).

```json
{
  "schema": "kor-travel-common.consumer-manifest.v1",
  "repo": "kor-travel-map",
  "app": "admin",
  "tokens": { "version": "0.1.0", "override": "packages/kor-travel-map-admin/frontend/src/app/brand.css" },
  "ui": { "version": null },
  "python": { "version": null },
  "lockfiles": [
    { "kind": "npm", "path": "package-lock.json", "scope": "root" }
  ],
  "contrast": { "baseline": "contrast-baseline.json", "dark": true },
  "ux_gate": { "baseline": "ux-baseline.json" },
  "openapi": { "exceptions": ["docs/standards/openapi-exceptions.yaml#map"] },
  "exceptions": []
}
```

위 예시는 필드 이름만 보여 주며 스키마 정본과 검증 명령(`python3 -B -X utf8 tools/validate_manifest.py <path>`)은 T-011 산출물이다. 절차는 다음과 같다.

1. 채택 PR에서 매니페스트를 갱신하고 `validate_manifest.py`와 소비자 저장소 루트를 함께 준 `check_versions.py` report를 통과시킨다.
2. 소비자 PR merge 뒤 common PR로 `consumers.pins.json`의 해당 저장소 SHA를 갱신한다(`consumer-smoke` 대상이면 필수).
3. `docs/integration-map.md`는 `python3 -B -X utf8 tools/collect_manifests.py`(T-012)가 생성한다. 수기 편집은 금지이며 생성 결과를 common PR에 포함한다.
4. 새 예외(`exceptions[]`)는 `until`과 `review`가 필수이고, 만료되면 `EXEMPT_EXPIRED`로 report에 표시된다(D-07).
5. 채택 준비 상태 표는 [adoption readiness](../architecture/adoption-readiness.md)가, 현재 채택 현황은 [integration map](../integration-map.md)이 정본이다.

## 10. 앱별 특이사항(링크만)

| 앱 | 1차 산출물(D-16) | 선행 gate | 특이사항 근거 | task 대역 |
|---|---|---|---|---|
| map admin | tokens → ui → py | 없음(첫 소비자) | `docs/survey/inventory/kor-travel-map.md` §8·§9, `docs/survey/cross/ui-components.md` §3.3(`manualSorting`) | T-410~T-413, T-480 |
| weather admin | tokens(`tokens.css` 교체 + shim) → Tailwind v4 → ui | Next 16·Vitest 4·Node 22(T-460) | `docs/survey/inventory/kor-travel-weather.md` §8·§9.1 | T-460~T-464, T-481 |
| pinvi admin | tokens(`[data-pv-surface='admin']` 스코프) → ui | L6(T-020) | `docs/survey/inventory/pinvi.md` §3.2·§8, `docs/survey/cross/licensing.md` §3.6 | T-420~T-422, T-484 |
| airport | tokens → 소형 ui | WIP 병합(T-430, O-9) | `docs/survey/inventory/kor-travel-airport.md` §3.2·§9 | T-430~T-433, T-482 |
| geo | tokens(`--ui-*` 별칭 유지) → React 19(O-25) → ui | `@config` 실효값 검증(T-441) | `docs/survey/inventory/kor-travel-geo.md` §8·§9, `docs/survey/cross/ui-components.md` §5.2 | T-440~T-444, T-483 |
| concierge | 규칙 참조 → CI 신설 → tokens → ui | L8(T-021), CI(T-451) | `docs/survey/inventory/kor-travel-concierge.md` §8·§11.12 | T-450~T-454, T-485 |
| docker-manager | 규칙 참조 → 업그레이드 PR → tokens → 부분 ui | L8(T-021), Next 16·React 19(T-470) | `docs/survey/inventory/kor-travel-docker-manager.md` §8·§9 | T-470~T-473, T-486 |

task 상세는 [tasks](../tasks.md)와 `docs/tasks/T-4xx-*.md`, 순서·Phase는 [integration plan](../plan/integration-plan.md), 앱별 이관 PR 수·규모 판정 근거는 [migration-feasibility 판정](../plan/design-panel/judge-migration-feasibility.md) §3.1, 소비자별 계약 요약은 [consumers](../architecture/consumers.md)를 본다. pinvi 사용자 표면·모바일은 코드 소비 대상이 아니며 consumer 프로필 규칙과 `tokens.json` 의미 이름만 참조한다(D-29; 모바일 Tailwind 3 예외는 O-8 사용자 승인 대기).
