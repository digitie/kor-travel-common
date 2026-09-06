# T-473 ktdm: ui 부분 채택(StatStrip·AppErrorPanel·SectionCard; `ops-*` 잔존 허용)

- 상태: BLOCKED
- 우선순위: P3
- Gate: vitest
- 선행: T-021, T-472, T-213
- 외부 선행: 사용자 O-2(ktdm 루트 GPL 정렬 결정, L8)

## 목표

docker-manager는 프리미티브 미도입(ADR-17)이므로 전면 채택 대신 이미 세 저장소에 복제된 부품 3종만 `@kor-travel/ui`로 바꾼다: `StatStrip`(map 형태 기준, `title` prop 흡수), `AppErrorPanel` + `error-recovery`(geo PR #391 계보), `SectionCard`(`ops-group-*`/`ops-section-title` 대체). 나머지 `ops-*` CSS·`DashboardClient.tsx` 1,970줄은 잔존한다.

## 고정 결정

- [design-brief](../plan/design-brief.md) D-08 ②(`ops-*` 잔존 허용)·D-09(AppErrorPanel·error-recovery는 T-205; 토스트 엔진 앱 소유)·D-13(C19 AppErrorPanel 계보 공통, C8 토스트 정책 통일·엔진 앱)·D-16(ktdm 3차, L8 후)·D-24.
- ADR-007·ADR-004 — [ADR 색인](../adr/README.md). 정본: [ui-contract](../standards/ui-contract.md), [licensing](../standards/licensing.md)(MIT 원천 고지 보존), [consumer-adoption runbook](../runbooks/consumer-adoption.md).
- 사실: `StatStrip.tsx` 95행(props `key/label/value/unit/caption/tone/title/href/loading/testId`, `isLoading/size/framed/ariaLabel`; `help` 없음·`title` 있음·CSS 클래스 기반), `AppErrorPanel.tsx` 103행 + `lib/error-recovery.ts`(chunk/RSC 오류 1회 hard reload), `ops-*` 약 70개 클래스, 토스트 자체(성공 6초), vitest 8 파일 — [inv/ktdm §3.1·§8-2·§8-4·§8-6·§9](../survey/inventory/kor-travel-docker-manager.md), [ui §2.2](../survey/cross/ui-components.md), [ux §4 C8·C19](../survey/cross/ux-patterns.md).
- PR 순서: [judge-migration-feasibility §3.1 ktdm #5](../plan/design-panel/judge-migration-feasibility.md).

## 구현 범위

- `@kor-travel/ui` 0.2.x 의존 + `@source` 1줄(`ops-*`와 `kt-` 접두는 충돌 없음).
- `components/StatStrip.tsx` → common `StatStrip` 어댑터(props 이름 차이가 있으면 어댑터에서 매핑, 호출부 `DashboardClient.tsx` 무변경 목표), `ops-stat*` CSS 절 삭제.
- `components/layout/AppErrorPanel.tsx`·`lib/error-recovery.ts` → `@kor-travel/ui` 재수출 shim; `app/error.tsx`·`global-error.tsx` 호출 유지. 한국어 복구 문구 계약이 common 판과 다르면 `ui-contract` 이관 절 요청 후 진행.
- `ops-group-*`·`ops-section-title/copy` 사용처를 `SectionCard`로(사용처 수는 착수 시 grep; ≤30 파일 초과 시 분할).
- 토스트(`Toast.tsx`)는 유지하되 성공 토스트 정책(UX-G4.1 "성공은 조용히")은 이 task 범위 밖 기록만.
- 매니페스트 `ui{version:"0.2.x"}`, `ux_lint --base` report.

## 범위 밖

Button·overlay·DataTable 등 프리미티브 도입(ADR-17 유지), `ops-modal` 교체, `window.confirm` 3건 제거(baseline 등록만), 로그인 화면, 사용자 표면 없음.

## 대상 저장소·브랜치·PR·되돌리기

- `digitie/kor-travel-docker-manager`, Linux/WSL, 브랜치 `agent/T-473-ui-partial`, `main`에서 분기. PR 1개(≤30 파일).
- 되돌리기 = `git revert <merge-sha>` + `npm ci` + 재배포.

## 예상 변경 파일

아래는 이 task가 만들거나 고칠 예정 경로다. 예정 경로는 존재·실행 증거가 아니다.

```text
frontend/src/components/StatStrip.tsx
frontend/src/components/layout/AppErrorPanel.tsx, frontend/src/lib/error-recovery.ts
frontend/src/components/<SectionCard 대체 사용처>
frontend/src/app/globals.css                         # @source, ops-stat*·ops-group-* 절 삭제
frontend/package.json, frontend/package-lock.json
frontend/kor-travel-common.lock.json
```

## 수용 기준

- [ ] vitest 8 파일 green(StatStrip·AppErrorPanel 관련 테스트가 common 계약으로 갱신되어 실행됨, 0 test 금지), `next build`·lint green.
- [ ] `DashboardClient.tsx` diff 0(어댑터로 흡수), `error.tsx`/`global-error.tsx` diff 0.
- [ ] 6폭 스크린샷: StatStrip·섹션 헤더 영역 diff는 부품 교체로 허용(전후 나란히 첨부), 나머지 diff 0.
- [ ] shim 헤더 SPDX + `Origin:`(ktdm MIT 원천 → common GPL 고지 보존; geo 계보는 `-only` 병기 여부 확인, O-20).
- [ ] `tools/ui_drift.py` 로컬 패치 0건; L8 evidence PR 본문 기재.

## 검증 명령

```bash
# kor-travel-docker-manager/frontend (Linux/WSL)
npm ci && npm run lint && npm run type-check && npm test && npm run build
grep -rn 'ops-stat\|ops-group' src app | wc -l    # 0 예상
BASELINE_APP=ktdm BASELINE_URL=http://127.0.0.1:12905 npx playwright test -c ../../kor-travel-common/templates/playwright.baseline.ts
# kor-travel-common
python3 -B -X utf8 tools/ui_drift.py --root ../kor-travel-docker-manager/frontend
python3 -B -X utf8 tools/ux_lint.py --root ../kor-travel-docker-manager/frontend --base origin/main
```

## evidence

PR 본문(전후 캡처·테스트 수·L8 링크), `consumers.pins.json`·`docs/integration-map.md`·`docs/journal.md`, 이 파일 "실행 기록".

## rollback·release 차단 조건

- O-2 미결/T-021 미완이면 PR을 열지 않는다(B9). vitest red·호출부 변경 필요(어댑터로 흡수 불가)면 머지 금지, 머지 후 회귀 시 revert + 재배포.
