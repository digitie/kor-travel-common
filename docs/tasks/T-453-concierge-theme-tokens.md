# T-453 concierge: hex fallback 블록 제거 → `@config`→`@theme inline` → `--ktc-*`를 `--kt-*` 오버라이드로 + contrast baseline + 매니페스트

- 상태: BLOCKED
- 우선순위: P1
- Gate: e2e 45·시각 diff
- 선행: T-451, T-109
- 외부 선행: ktc 루트 GPL-3.0-or-later 정렬(L8, O-2; T-021 결과) — 브리프 선행 열에는 없으나 D-16이 L8 전 코드 소비를 금지하므로 tokens 패키지 설치 단계(PR 3)는 L8 후에만

## 목표

concierge 프론트의 스타일 정본을 3단 별도 PR로 정리하고 `@kor-travel/tokens`를 채택한다: (1) `globals.css` 앞쪽의 구 geo 계열 hex fallback 블록 제거(뒤 블록이 이미 덮어씀), (2) `@config "../../tailwind.config.ts"` → `@theme inline` 1:1 매핑 + `tailwind.config.ts` 삭제, (3) `--ktc-*` 값을 `--kt-*` 오버라이드로 재해석(보라 브랜드·짙은 보라 rail은 앱 값 유지) + contrast baseline + 매니페스트. 각 단계 6폭 diff 0.

## 고정 결정

- [design-brief](../plan/design-brief.md) D-08 ④(concierge는 CI 신설 후 hex fallback 블록·`@config` 제거·`--ktc-*`를 `--kt-*` 오버라이드로 재해석; 4단 별도 PR)·D-12(접두 `--kt-*`는 전 저장소 0회, `--ktc-*`는 앱 파일; 오버라이드 허용 목록 brand 4·focus·paper·ink·status)·D-16(ktc는 L8 전 규칙·`tokens.json` 참조까지)·D-21·D-24.
- ADR-006·ADR-012 — [ADR 색인](../adr/README.md). 정본: [design-tokens](../standards/design-tokens.md), [consumer-adoption runbook](../runbooks/consumer-adoption.md).
- 사실: `globals.css` 5줄 헤더 `@config "../../tailwind.config.ts"`, `tailwind.config.ts` 148줄(colors → `var(--…)`, fontSize 7단계 xs=13px), `tokens.css` 87줄 `--ktc-*`(surface 5·brand 5·rail 4·text 5·status 4×2·radius 4·control 2·shadow 5·duration 2, z-index 없음), 3단 매핑, 앞 `@layer base :root` fallback 블록, `.dark` 정의만, 컨트롤 경계 2.06/1.93 대비 미달 — [inv/ktc §3.1·§8-1·§9](../survey/inventory/kor-travel-concierge.md), [dt §3.1.1·§3.4.2·§3.6.1](../survey/cross/design-tokens.md), [README §6.2-12](../survey/README.md)(13px 정본).
- PR 순서: [judge-migration-feasibility §3.1 concierge #4](../plan/design-panel/judge-migration-feasibility.md).

## 구현 범위

- PR 1: fallback 블록 삭제만. 빌드 CSS diff로 실효 값 무변경 증명.
- PR 2: `tailwind.config.ts`의 `theme.extend`를 `@theme inline`으로 옮기고(`--color-*: var(--ktc-…)`, `--radius-control/panel`, `--spacing-control/-sm`, `--text-xs: 0.8125rem` 등 7단계), `@config` 줄·파일 삭제, `components.json` 갱신. `autoprefixer` 잔존 여부 확인(v4 불필요).
- PR 3(L8 후): `@import "@kor-travel/tokens/tokens.css"`·`theme.css`·`shadcn.css` 추가, `tokens.css`는 `--kt-*` 오버라이드 파일로 재작성(`--kt-brand: #7c3aed` 계열, `--kt-surface-*` 웜그레이/크림, `--kt-text-*`, `--kt-status-*`; rail 4종·shadow 5종처럼 common에 없는 이름은 `--ktc-*`로 잔류), `--ktc-*` 소비처는 별칭으로 유지. `contrast-baseline.json`에 2.06/1.93 등록. 매니페스트 `tokens{version, override: "frontend/tokens.css"}`.

## 범위 밖

UI 18종 shim(T-454), base-ui 1.5 → 1.8(T-454), 다크 토글, `ReviewWorkspace.tsx` 4,386줄 접촉, maplibre-gl 6 → 5(예외 유지).

## 대상 저장소·브랜치·PR·되돌리기

- `digitie/kor-travel-concierge`, Linux/WSL2, 브랜치 `agent/<agent>-T-453-fallback` / `-theme` / `-tokens`, `origin/main`에서 순차 분기. PR 3개(각 ≤10 파일).
- 되돌리기 = 각 PR `git revert` 1회, 역순. PR 2 revert 시 `tailwind.config.ts` 복원.

## 예상 변경 파일

아래는 이 task가 만들거나 고칠 예정 경로다. 예정 경로는 존재·실행 증거가 아니다.

```text
frontend/src/app/globals.css
frontend/tailwind.config.ts             # 삭제(PR 2)
frontend/components.json
frontend/tokens.css                     # --kt-* 오버라이드로 재작성(PR 3)
frontend/package.json, frontend/package-lock.json
frontend/kor-travel-common.lock.json
frontend/contrast-baseline.json
.github/workflows/ci.yml                # contrast-check job(report)
```

## 수용 기준

- [ ] PR마다 6폭 스크린샷 diff 0(대시보드·목록·`ReviewWorkspace`·로그인·모달), Playwright 45 test green(로컬 또는 dispatch job), `node-quality` green.
- [ ] PR 2 후 `@config`·`tailwind.config.ts` 0건, `text-xs`가 13px로 유지됨을 빌드 CSS로 확인(design.md 13.5px가 아닌 코드 정본).
- [ ] PR 3 후 빌드 CSS에 `--kt-*` 정의 존재, `--ktc-*` 별칭이 `var(--kt-…)` 참조(grep 첨부); `kt_contrast` 신규 미달 0.
- [ ] `check_versions` report ktc 행에 `@kor-travel/tokens` `OK`; L8 완료 evidence(T-021 PR 링크)가 PR 3 본문에 있다.

## 검증 명령

```bash
# kor-travel-concierge/frontend (Linux/WSL2)
npm ci && npm run lint && npx tsc --noEmit && npm run build
grep -c '@config\|tailwind.config' src/app/globals.css   # 0 (PR 2 후)
cd ../tests && npm ci && npx playwright test                  # 45 test(webServer 자동 기동)
# kor-travel-common
python3 -B -X utf8 tools/kt_contrast.py --app concierge --baseline ../kor-travel-concierge/frontend/contrast-baseline.json
python3 -B -X utf8 tools/check_versions.py --manifest ../kor-travel-concierge/frontend/kor-travel-common.lock.json
```

## evidence

PR 3개 본문(빌드 CSS diff·6폭 diff·e2e 수), `consumers.pins.json`·`docs/integration-map.md`·`docs/journal.md`, 이 파일 "실행 기록".

## rollback·release 차단 조건

- 원인 불명 diff → 해당 PR revert(D-08). PR 1·2는 L8과 무관하게 진행 가능하지만 PR 3은 L8(T-021 결과) 전 머지 금지.
- T-451 CI가 없는 상태에서는 e2e evidence를 로컬 실행으로 대체하되 `NOT_RUN`이 아닌 실제 실행 기록만 인정.
