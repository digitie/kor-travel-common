# T-441 geo: `@config` 실효값 빌드 검증 → `@theme` 단일화·`tailwind.config.ts` 삭제 → tokens 채택(`--ui-*` 별칭 유지) + contrast baseline + 매니페스트

- 상태: BLOCKED
- 우선순위: P1
- Gate: 시각 diff·e2e 23
- 선행: T-109

## 목표

geo-ui의 Tailwind v4 혼합 모드(`@theme inline` + `@config "../tailwind.config.ts"`)를 CSS-first 단일 정본으로 정리한 뒤 `@kor-travel/tokens`를 채택한다. 3단 별도 PR: (1) `@config` 실효값 evidence만, (2) `@theme` 단일화 + `tailwind.config.ts` 삭제(시각 diff 0), (3) tokens 채택 + `--ui-*`/shadcn 별칭 유지 + contrast baseline + 매니페스트. React 18 상태에서 진행한다(토큰은 React 무관).

## 고정 결정

- [design-brief](../plan/design-brief.md) D-08 ③(geo는 `@config` 실효값을 빌드 산출 CSS로 검증한 뒤 `@theme` 단일화, React 19와 독립; 4단 별도 PR, 원인 불명 diff는 revert)·D-12(`--kt-*`, 앱 고유 접두 `--ui-*`는 앱 파일, 별칭 shim `aliases/map-vocabulary.css` 선택)·D-16(React 18 앱은 tokens부터)·D-21·D-24.
- ADR-006·ADR-012 — [ADR 색인](../adr/README.md). 정본: [design-tokens](../standards/design-tokens.md), [consumer-adoption runbook](../runbooks/consumer-adoption.md).
- 사실: `globals.css` 3,750행, `source(none)` + 명시 `@source`(프로즈 스캔 파서 오류 회피), `@theme inline` 33개 `--color-*` vs `tailwind.config.ts` `theme.extend.colors` 43개가 겹침(어느 쪽이 실효하는지 미확인), 3중 별칭(OKLCH 원색 → 의미 토큰 → `--ui-*`/shadcn), 라이트 전용, e2e 셀렉터 계약 — [inv/geo §3.1·§8-1·§8-16·§9·§11-2](../survey/inventory/kor-travel-geo.md), [dt §3.1.1·§5-3](../survey/cross/design-tokens.md)(geo `@config` raw hex 잔존, 대비 2.29/2.41 미달).
- PR 순서: [judge-migration-feasibility §3.1 geo #2](../plan/design-panel/judge-migration-feasibility.md).

## 구현 범위

- PR 1(evidence): `next build` 산출 CSS에서 겹치는 유틸리티(`bg-brand`, `text-primary` 등 43개)의 실효 값을 추출해 표로 기록. 코드 변경 0. 표는 PR 본문 + 이 파일 "실행 기록".
- PR 2(단일화): 표에서 `@config` 쪽이 실효였던 값을 `@theme inline`에 옮기고 `@config` 줄·`tailwind.config.ts`·`components.json` `tailwind.config` 참조 삭제. 6폭 diff 0.
- PR 3(tokens): `@import "@kor-travel/tokens/tokens.css"`·`theme.css`·`shadcn.css`·`aliases/map-vocabulary.css`(geo 공통 이름용) 추가, geo brand(blue) 오버라이드 블록, `--ui-*` 별칭은 `--kt-*` 참조로 유지, `@source`에 `../node_modules/@kor-travel/tokens` 불필요(CSS만)·`ui`는 T-444에서. `contrast-baseline.json`에 2.29/2.41 쌍 등록. 매니페스트 `tokens{version, override}`·`contrast{baseline, dark:false}`.

## 범위 밖

React 19(T-443), radix → base-ui·ui 패키지(T-444), 다크 값 정의(라이트 전용 유지), e2e 셀렉터 변경, `VirtualTable`.

## 대상 저장소·브랜치·PR·되돌리기

- `digitie/kor-travel-geo`(`kor-travel-geo-ui/` 하위), 브랜치 `agent/<agent>-T-441-config-evidence` / `-theme-unify` / `-tokens`, `origin/main`에서 순차 분기. PR 3개(각 ≤10 파일).
- 되돌리기 = 각 PR `git revert` 1회, 역순(3 → 2). PR 2 revert 시 `tailwind.config.ts`가 복원된다.

## 예상 변경 파일

아래는 이 task가 만들거나 고칠 예정 경로다. 예정 경로는 존재·실행 증거가 아니다.

```text
kor-travel-geo-ui/app/globals.css
kor-travel-geo-ui/tailwind.config.ts          # 삭제(PR 2)
kor-travel-geo-ui/components.json             # tailwind.config: ""
kor-travel-geo-ui/app/brand.css               # geo blue 오버라이드(PR 3)
kor-travel-geo-ui/package.json, package-lock.json
kor-travel-geo-ui/kor-travel-common.lock.json
kor-travel-geo-ui/contrast-baseline.json
.github/workflows/ci.yml                      # contrast-check job(report)
```

## 수용 기준

- [ ] PR 1: 43개 겹침 이름의 실효 값 표(빌드 CSS 인용 줄 번호 포함)가 있고, `.next` 산출물이 아닌 `next build` 출력 CSS 파일 digest를 적었다.
- [ ] PR 2·3 각각 6폭 스크린샷 diff 0(로그인·목록·상세·모달 열림), e2e 23 spec + a11y 4 spec green, unit 43 파일 green.
- [ ] PR 2 후 저장소에 `tailwind.config.ts`·`@config` 0건, `source(none)` + `@source` 명시 규약 유지.
- [ ] PR 3 후 빌드 CSS에 `--kt-*` 정의 존재, `--ui-*` 별칭이 `var(--kt-…)`를 가리킴(grep 첨부); `kt_contrast` 신규 미달 0(2.29/2.41은 baseline).
- [ ] `check_versions` report geo 행 `OK`/등록된 예외만.

## 검증 명령

```bash
# kor-travel-geo/kor-travel-geo-ui (Linux)
npm ci && npm run lint && npm run type-check && npm test && npm run build
grep -o '\-\-kt-[a-z0-9-]*: *[^;]*' .next/static/css/*.css | sort -u > /tmp/kt-vars.txt   # 산출 CSS 대조(PR 3)
PLAYWRIGHT_MOCK_LOGIN=1 npm run test:e2e
# kor-travel-common
python3 -B -X utf8 tools/kt_contrast.py --app geo --baseline ../kor-travel-geo/kor-travel-geo-ui/contrast-baseline.json
python3 -B -X utf8 tools/check_versions.py --manifest ../kor-travel-geo/kor-travel-geo-ui/kor-travel-common.lock.json
```

## evidence

PR 3개 본문(실효값 표·6폭 diff·e2e 수), `consumers.pins.json`·`docs/integration-map.md`·`docs/journal.md`, 이 파일 "실행 기록".

## rollback·release 차단 조건

- 어느 단계든 원인 불명 diff → 그 PR revert 후 확대 중단(D-08). PR 1 표 없이 PR 2를 열지 않는다.
- `uv.lock`(T-440)은 이 task의 선행이 아니지만, `check_versions`가 `NO_LOCK`을 내는 동안에는 T-502 승격 후보에서 제외된다.
