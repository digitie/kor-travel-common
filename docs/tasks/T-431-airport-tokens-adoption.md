# T-431 airport: tokens 채택(alias 재매핑 유지·`dark-media.css`·contrast baseline) + 매니페스트

- 상태: BLOCKED
- 우선순위: P1
- Gate: build·320px 게이트
- 선행: T-430, T-109

## 목표

병합된 airport 프론트가 `@kor-travel/tokens`를 소비하되 airport 고유 값(airport-orange, radius 16/10, alpha line)을 `--kt-*` 오버라이드로 얹어 렌더 무변경을 유지한다. WIP가 재명명한 `--muted`/`--accent`/`--radius` 별칭 약 30곳은 그대로 두고, 다크는 `prefers-color-scheme` 전용이므로 `dark-media.css`를 import한다. 대비 미달 쌍은 `contrast-baseline.json`에 등록한다.

## 고정 결정

- [design-brief](../plan/design-brief.md) D-12(오버라이드 허용 목록·형태는 프로필로만·다크 활성화 파일은 앱 명시 import·`kt_contrast` light 필수/dark는 dark 활성 앱·baseline 신규 미달만 fail)·D-16(airport tokens 1차는 WIP 병합 후)·D-20·D-21·D-24(≤10 파일).
- ADR-006·ADR-010 — [ADR 색인](../adr/README.md). 정본: [design-tokens](../standards/design-tokens.md), [responsive-web](../standards/responsive-web.md)(320px 컨테인·가로 스크롤 금지), [consumer-adoption runbook](../runbooks/consumer-adoption.md).
- 사실: `tokens.css` OKLCH 계층 + `prefers-color-scheme` 다크, 루트 `overflow-x: clip`, 검증 폭 320/375/414/768/1440, raw `rgba`/hex 22건 잔존, 폰트 Pretendard 선언만·로딩 없음 — [inv/kta §3.1·§8-1~6·§9](../survey/inventory/kor-travel-airport.md), [dt §3.4.2](../survey/cross/design-tokens.md)(line 1.15 등 대비 미달).
- PR 순서: [judge-migration-feasibility §3.1 airport #2](../plan/design-panel/judge-migration-feasibility.md).

## 구현 범위

- `frontend/src/app/globals.css` 헤더에 `@import "@kor-travel/tokens/tokens.css"`·`theme.css`·`shadcn.css`·`dark-media.css` 추가; `tokens.css`(앱)는 유지하되 common과 의미가 같은 변수는 `--kt-*` 오버라이드 블록(`--kt-brand`·`--kt-radius-control: 10px`·`--kt-radius-panel: 16px`·`--kt-border`(alpha) 등)으로 재선언하고, 앱 전용 이름은 그대로 둔다. 형태 값(radius)은 프로필 규칙상 오버라이드 금지이므로 `exceptions[]`에 `{key: radius, reason: "WIP 값 유지(O-9)", until, review}`로 등록한다.
- WIP의 `:root` shadcn 배선 블록은 `shadcn.css`가 대체 가능한 부분만 제거(diff 0 확인 후), 나머지 30곳 별칭 재매핑은 유지.
- font 스택은 현재 스택으로 오버라이드(Pretendard 로딩 없음 → 1순위 MUST 비적용, D-12).
- `frontend/kor-travel-common.lock.json` `tokens{version, override}`·`contrast{baseline: "frontend/contrast-baseline.json", dark: true}` 기록; `kt_contrast` light+dark 쌍 report → 미달 쌍 baseline 등록.

## 범위 밖

raw hex 22건 정리(`ux_lint` baseline으로 등록만), 폰트 로딩 도입, `.dark` 클래스 토글, 컴포넌트 교체(T-432), 백엔드.

## 대상 저장소·브랜치·PR·되돌리기

- `digitie/kor-travel-airport`, 브랜치 `codex/T-431-tokens`(Draft PR), `main`에서 분기. PR 1개(≤10 파일).
- 되돌리기 = `git revert <merge-sha>` + `npm ci`.

## 예상 변경 파일

아래는 이 task가 만들거나 고칠 예정 경로다. 예정 경로는 존재·실행 증거가 아니다.

```text
frontend/src/app/globals.css
frontend/src/app/tokens.css                  # --kt-* 오버라이드 블록 추가
frontend/package.json, frontend/package-lock.json
frontend/kor-travel-common.lock.json
frontend/contrast-baseline.json
.github/workflows/ci.yml                     # contrast-check job(report)
```

## 수용 기준

- [ ] 착수 전 6폭 기준선 대비 완료 diff 0(대시보드·백업 패널·collector 패널, light + `prefers-color-scheme: dark` 에뮬레이션).
- [ ] 320px에서 문서 가로 스크롤 0(`document.documentElement.scrollWidth <= 320` 단언, Playwright 또는 수동 기록).
- [ ] frontend CI(vitest·tsc·build) green; `next build` 산출 CSS에 `--kt-*` 존재.
- [ ] `kt_contrast` light·dark 쌍 report에 신규 미달 0, 기존 미달은 baseline에 `until`과 함께.
- [ ] radius 예외가 `versions.json` 또는 매니페스트 `exceptions[]`에 `until`·`review` 포함으로 등록.

## 검증 명령

```bash
# kor-travel-airport/frontend
npm ci && npx tsc --noEmit && npm test && npm run build
npx playwright test -c ../../kor-travel-common/templates/playwright.baseline.ts   # 6폭 캡처(BASELINE_URL 지정)
# kor-travel-common
python3 -B -X utf8 tools/kt_contrast.py --app airport --dark --baseline ../kor-travel-airport/frontend/contrast-baseline.json
python3 -B -X utf8 tools/check_versions.py --manifest ../kor-travel-airport/frontend/kor-travel-common.lock.json
```

## evidence

PR 본문(6폭 light/dark diff, 320px scrollWidth 결과, contrast report), `consumers.pins.json`·`docs/integration-map.md`·`docs/journal.md`, 이 파일 "실행 기록". live-e2e는 실행 대상이 아니므로 `NOT_RUN(운영 호출 job)`로 표기.

## rollback·release 차단 조건

- 시각 diff 원인 불명·320px 가로 스크롤 발생·contrast 신규 미달 중 하나면 머지 금지, 머지 후 발견 시 revert.
- T-430 PR 0가 main에 없으면 이 PR을 열지 않는다.
