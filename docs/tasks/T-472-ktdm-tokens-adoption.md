# T-472 ktdm: tokens 채택(`@theme`→`--kt-*`·Ember 값 유지·tint 4종) + contrast baseline + 매니페스트

- 상태: BLOCKED
- 우선순위: P2
- Gate: 시각 diff(수동)
- 선행: T-470, T-109
- 외부 선행: T-021 common 결정 완료(2026-09-08); ktdm license-only 외부 PR evidence는 [T-021 external evidence](T-021-ktc-ktdm-license-l8.md#외부-evidence현재-open)의 docker-manager 행에서 확인한다. D-16에 따라 tokens 패키지 설치는 그 evidence 후에만 진행한다.

## 목표

docker-manager `frontend/tokens.css`의 `@theme` 색 20종(Ember 오렌지)·shadow·radius·easing·font와 `:root` 간격·duration·z-index를 `@kor-travel/tokens` 위에 `--kt-*` 오버라이드 + 기존 이름 별칭으로 재구성한다. 값(Ember)은 그대로, status tint 4종(`--kt-status-*-tint`)을 추가하고 brand 3.59:1 등 대비 미달 쌍을 baseline에 등록한다. `ops-*` CSS 1,300줄은 건드리지 않는다.

## 고정 결정

- [design-brief](../plan/design-brief.md) D-08 ②(ktdm은 업그레이드 PR 후 `@theme`→`--kt-*` 매핑, `ops-*` CSS 잔존 허용)·D-12(오버라이드 허용 목록, status 4+tint, z 5, radius 2 control 6/panel 8)·D-16(ktdm은 L8 전 규칙·`tokens.json` 참조까지)·D-21(ktdm은 템플릿 캡처)·D-24.
- ADR-006·ADR-012 — [ADR 색인](../adr/README.md). 정본: [design-tokens](../standards/design-tokens.md), [consumer-adoption runbook](../runbooks/consumer-adoption.md).
- 사실: `tokens.css` 72줄(`@theme` 색 20종 oklch: page/card/subtle/elevated/row/line, strong/ink/secondary/tertiary/disabled, brand/brand-ink/brand-tint, info/warn/danger/ok, graphite×3; shadow 3, radius 3(card 0.375/panel 0.5/pill), easing 3, font 3; `:root` 간격 8·duration 3·z-index 7), Tailwind 4.3.1, `@layer components` 수기 CSS, 라이트 단일, 웹폰트 미로드, `DESIGN.md` Ember 정본, `.hallmark/log.json` Cobalt stale — [inv/ktdm §3.1·§8-1·§9](../survey/inventory/kor-travel-docker-manager.md), [dt §3.2·§3.4.2](../survey/cross/design-tokens.md)(brand 3.59 미달), [ux §4 C9·C13](../survey/cross/ux-patterns.md)(ok/warn/danger 별칭, 14px 본문).
- PR 순서: [judge-migration-feasibility §3.1 ktdm #4](../plan/design-panel/judge-migration-feasibility.md).

## 구현 범위

- `frontend/src/app/globals.css` 헤더에 `@import "@kor-travel/tokens/tokens.css"`·`theme.css` 추가(`shadcn.css`는 shadcn 미사용이라 생략 가능, `base.css`는 `ops-*`와 충돌 여부 확인 후 결정).
- `frontend/tokens.css` 재작성: `--kt-brand: <Ember oklch>`·`--kt-brand-hover/tint/foreground`, `--kt-surface-*` ← page/card/subtle/elevated/row, `--kt-text-*` ← strong/ink/secondary/tertiary/disabled, `--kt-status-{success,warning,destructive,info}` ← ok/warn/danger/info + tint 4종 신설(값은 Ember 팔레트에서 파생, 대비 검사), `--kt-font-*` 현재 스택(Noto Sans KR 1순위 유지; Pretendard MUST 비적용). 기존 `@theme` 이름(`--color-page` 등)은 `var(--kt-…)` 별칭으로 남겨 `ops-*` CSS·유틸리티 무변경. graphite 3종·radius pill·z-index 7단 중 common에 없는 이름은 앱 `@theme` 잔류.
- `contrast-baseline.json`에 brand 3.59 등 미달 쌍 + `until`; 매니페스트 `tokens{version, override: "frontend/tokens.css"}`·`contrast{baseline, dark:false}`.
- `DESIGN.md` 토큰 표에 `--kt-*` 대응 열 추가(값 무변경).

## 범위 밖

`ops-*` → 유틸리티 전환, UI 부품(T-473), 프리미티브 도입, 본문 14px → 15px 스케일 정렬(C13, 후속), `.hallmark/log.json` 정정(ktdm 소유), 다크.

## 대상 저장소·브랜치·PR·되돌리기

- `digitie/kor-travel-docker-manager`, Linux/WSL, 브랜치 `agent/T-472-tokens`, `main`에서 분기. PR 1개(≤10 파일).
- 되돌리기 = `git revert <merge-sha>` + `npm ci`; 운영은 rsync 배포이므로 revert 후 재배포.

## 예상 변경 파일

아래는 이 task가 만들거나 고칠 예정 경로다. 예정 경로는 존재·실행 증거가 아니다.

```text
frontend/tokens.css
frontend/src/app/globals.css
frontend/package.json, frontend/package-lock.json
frontend/kor-travel-common.lock.json
frontend/contrast-baseline.json
DESIGN.md
.github/workflows/ci.yml                 # contrast-check job(report)
```

## 수용 기준

- [ ] 6폭 스크린샷 diff 0(대시보드·로그 모달·설정 모달·로그인; common 템플릿 외부 실행, 실행 못 하면 `NOT_RUN`·DONE 불가).
- [ ] 빌드 CSS에서 기존 `--color-page` 등 20종의 계산값이 착수 전과 동일(`getComputedStyle` 대조표 또는 CSS grep).
- [ ] `kt_contrast` light 신규 미달 0, 기존 미달은 baseline(`until` 포함); tint 4종은 라벨 대비 규칙 통과.
- [ ] vitest 8 파일·`next build`·`eslint --max-warnings=0` green; `git diff --stat frontend/src` 가 `globals.css` 헤더 외 0.
- [ ] T-021 docker-manager 행의 license-only 외부 PR URL·main merge SHA·root LICENSE 첫 줄·검사 결과를 PR 본문에 인용하고, `check_versions` ktdm tokens `OK`.

## 검증 명령

```bash
# kor-travel-docker-manager/frontend (Linux/WSL)
npm ci && npm run lint && npm run type-check && npm test && npm run build
grep -o '\-\-kt-[a-z0-9-]*: *[^;]*' .next/static/css/*.css | sort -u
BASELINE_APP=ktdm BASELINE_URL=http://127.0.0.1:12905 npx playwright test -c ../../kor-travel-common/templates/playwright.baseline.ts
# kor-travel-common
python3 -B -X utf8 tools/kt_contrast.py --app ktdm --baseline ../kor-travel-docker-manager/frontend/contrast-baseline.json
python3 -B -X utf8 tools/check_versions.py --manifest ../kor-travel-docker-manager/frontend/kor-travel-common.lock.json
```

## evidence

PR 본문(6폭 diff·계산값 대조표·contrast report·L8 링크), `consumers.pins.json`·`docs/integration-map.md`·`docs/journal.md`, 이 파일 "실행 기록".

## rollback·release 차단 조건

- 원인 불명 diff → revert(D-08). L8 외부 LICENSE evidence가 없으면 PR을 열지 않는다(B9).
- T-470 미머지 상태에서는 열지 않는다(D-08 ② 순서; Tailwind 4.3.1 자체는 토큰 소비 가능하나 순서 고정).
