# T-421 pinvi: admin `--color-admin-*`→`--kt-*` 오버라이드 + `base.scoped.css` + 매니페스트(사용자 표면 무변경 e2e)

- 상태: BLOCKED
- 우선순위: P1
- Gate: admin e2e·app-shell-mobile e2e
- 선행: T-420, T-109

## 목표

pinvi `apps/web` admin 표면(`[data-pv-surface='admin']` subtree)만 `@kor-travel/tokens`를 소비한다. 기존 `--color-admin-*`·`--radius-control`·`--spacing-control` 등 admin `@theme` 변수는 `--kt-*`를 참조하는 별칭으로 남겨 admin 페이지 무변경, 사용자 표면(Airbnb 톤 preset)은 바이트 무변경을 e2e로 증명한다.

## 고정 결정

- [design-brief](../plan/design-brief.md) D-08 ⑤(pinvi admin은 `[data-pv-surface='admin']` 스코프만 `--kt-*` 매핑, 사용자 preset 유지)·D-10(`base.scoped.css` = `[data-kt-surface]` 스코프 변형)·D-12(오버라이드 허용 목록: brand 4·focus·paper 4·ink 4·status 4+tint·font)·D-29(사용자 표면·모바일은 코드 소비 대상 아님)·D-16(L6 완료 조건).
- ADR-006·ADR-010·ADR-012 — [ADR 색인](../adr/README.md). 정본: [design-tokens](../standards/design-tokens.md), [consumer-adoption runbook](../runbooks/consumer-adoption.md).
- 앱 사실: admin `@theme`(`--color-admin-line` #dddddd, `--color-admin-control-line` #767676 4.24:1, `--spacing-rail` 22rem, `--text-2xs` 12px), `[data-pv-surface='admin']`에서 `--text-*` 가리기, `@config` v3 preset ↔ `@theme` 이중 정본, webpack 강제(ADR-066), 두 UI 스택 공존을 ESLint가 강제 — [inv/pinvi §3.1·§8-4·§9](../survey/inventory/pinvi.md), [dt §3.1.1·§3.6.5](../survey/cross/design-tokens.md).
- PR 순서: [judge-migration-feasibility §3.1 pinvi #1](../plan/design-panel/judge-migration-feasibility.md)(페이지 무변경, `app-shell-mobile` e2e = 사용자 표면 무변경 조건).

## 구현 범위

- `apps/web/app/globals.css`: admin 블록 앞에 `@import "@kor-travel/tokens/tokens.css"`·`theme.css`·`base.scoped.css`(`[data-kt-surface]` 스코프)를 추가하고, `apps/web/app/(admin)/layout.tsx`가 `data-pv-surface='admin'`과 함께 `data-kt-surface`를 건다. 전역 `base.css`는 쓰지 않는다.
- admin `@theme` 변수를 `--kt-*` 참조로 바꾸는 별칭 블록(`--color-admin-line: var(--kt-border)` 등) + pinvi brand 오버라이드(`--kt-brand: #e00b41` 계열, admin 스코프 안에서만).
- `@config` preset은 사용자 표면용으로 그대로 두고 admin `@theme` 이중 정의는 별칭으로만 축소한다(preset 제거는 pinvi 측 별도 판단).
- `apps/web/kor-travel-common.lock.json` `tokens{version, override}`·`contrast{baseline}` 기록; `kt_contrast` report의 미달 쌍은 `contrast-baseline.json`에 `until` 포함 등록.
- 44px 컨트롤 예외 2쪽은 T-422에서 등록(이 task는 토큰만).

## 범위 밖

사용자 표면·모바일 토큰(`packages/design-tokens`는 pinvi 소유), UI 컴포넌트(T-422), `@config` preset 제거, 다크 모드, 마커 팔레트 16색(D-26).

## 대상 저장소·브랜치·PR·되돌리기

- pinvi 정본 체크아웃(Linux-only 정책), 브랜치 `agent/<agent>-T-421-admin-tokens`, `origin/main`에서 분기. PR 1개(≤10 파일).
- 되돌리기 = `git revert <merge-sha>` + `npm ci`(lock 동반). `data-kt-surface` 속성 제거도 revert에 포함.

## 예상 변경 파일

아래는 이 task가 만들거나 고칠 예정 경로다. 예정 경로는 존재·실행 증거가 아니다.

```text
apps/web/app/globals.css
apps/web/app/(admin)/layout.tsx
apps/web/package.json, package-lock.json
apps/web/kor-travel-common.lock.json
apps/web/contrast-baseline.json
.github/workflows/web.yml            # contrast-check job(report)
```

## 수용 기준

- [ ] `app-shell-mobile` e2e를 포함한 사용자 표면 e2e 전부 green이고, 사용자 표면 6폭 스크린샷 diff 0(마케팅 `/`·앱 셸·콘텐츠 페이지 각 1).
- [ ] admin e2e(56 mock 중 admin 스펙) green, admin 6폭 diff 0(44px 단언 2쪽 포함).
- [ ] 빌드 산출 CSS에서 `--kt-*` 정의가 `[data-kt-surface]` 스코프 밖으로 새지 않는다(`:root` 레벨 `--kt-` 0건, 사용자 표면 DOM에서 `getComputedStyle` `--kt-brand` 빈값).
- [ ] `next build --webpack` green(ADR-066), Turbopack은 common 측 consumer-smoke에서만 검증.
- [ ] `kt_contrast` report에 신규 미달 0(기존 미달은 baseline에 `until`과 함께).
- [ ] admin 페이지 소스(`apps/web/app/(admin)/**`) diff 0(layout.tsx 속성 1줄 제외).

## 검증 명령

```bash
# pinvi(Linux)
npm ci --no-audit --no-fund && npm run lint --workspaces && npm run typecheck --workspaces
npm run build -w apps/web            # next build --webpack
npm run test -w apps/web             # vitest 27
npx playwright test -c apps/web/playwright.config.ts   # mock e2e 56
# kor-travel-common
python3 -B -X utf8 tools/kt_contrast.py --app pinvi-admin --baseline ../pinvi/apps/web/contrast-baseline.json
python3 -B -X utf8 tools/check_versions.py --manifest ../pinvi/apps/web/kor-travel-common.lock.json
```

## evidence

PR 본문(사용자 표면·admin 6폭 diff 캡처, e2e 수, 스코프 누출 검사 결과), `consumers.pins.json`·`docs/integration-map.md`·`docs/journal.md`, 이 파일 "실행 기록".

## rollback·release 차단 조건

- 사용자 표면 diff ≠ 0 또는 `--kt-*` 스코프 누출이 있으면 머지 금지(D-29 위반). 머지 후 발견 시 revert.
- T-420 미머지 상태에서는 이 PR을 열지 않는다(B1).
