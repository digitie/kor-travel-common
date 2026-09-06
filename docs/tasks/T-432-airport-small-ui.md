# T-432 airport: 소형 ui 채택(백업·collector 패널: Alert·StatStrip·SectionCard·EmptyState)

- 상태: BLOCKED
- 우선순위: P2
- Gate: build·vitest
- 선행: T-431, T-212

## 목표

airport "Admin"의 실체인 무인증 백업 패널과 collector-status 패널에서 자체 마크업을 `@kor-travel/ui` v0.1 소형 부품(Alert·StatStrip·SectionCard·EmptyState)으로 교체한다. Button은 0.2까지 로컬 구현을 유지한다. 셸·로그인·`AdminPageHeader`는 이 task 범위 밖이다. T-035 병합 사실과 현재 경로는 [인계 재확인](../plan/handoff-verification.md)을 출발점으로 착수 시 갱신한다. L6가 T-2xx 착수까지 미결이면 이 task가 ui 1차 검증의 pinvi 대체 경로가 된다(D-16).

## 고정 결정

- [design-brief](../plan/design-brief.md) D-16(ui 1차 대체 경로 = airport 소형 부품)·D-20(1차 = tokens + 소형 부품; 셸·로그인은 T-035 후)·D-09(Button 계약)·D-10(`@source`, webpack·Turbopack)·D-24(≤30 파일).
- ADR-007·ADR-010 — [ADR 색인](../adr/README.md). 정본: [ui-contract](../standards/ui-contract.md), [ux-guide](../standards/ux-guide.md)(빈 상태 좌정렬, 확인 다이얼로그 동사 라벨), [consumer-adoption runbook](../runbooks/consumer-adoption.md).
- 사실: 별도 admin 앱·라우트·로그인 없음, 운영 UI = 대시보드 안의 백업 패널 + `/v1/admin/*`, `window.confirm` 1건, Button은 WIP에서 JSX 미사용 — [inv/kta §9](../survey/inventory/kor-travel-airport.md), [ux §4 C7·C19](../survey/cross/ux-patterns.md).
- PR 순서: [judge-migration-feasibility §3.1 airport #3](../plan/design-panel/judge-migration-feasibility.md).

## 구현 범위

- `@kor-travel/ui` 0.1.0 의존 추가 + `@source` 1줄; 0.1에 실제 공개된 소형 부품만 shim으로 연결한다. `@kor-travel/ui/button`은 0.1에 없으므로 import하지 않는다.
- 백업 패널·collector-status 패널의 섹션 컨테이너·통계 띠·빈 상태·경고 문구를 SectionCard·StatStrip·EmptyState·Alert로 치환(≤30 파일, 페이지 로직 무변경).
- `window.confirm` 1건은 이 task에서 건드리지 않고 `ux_gate.baseline`에 등록(AlertDialog는 v0.2 범위, 후속).
- 매니페스트 `ui{version:"0.1.0"}` 갱신, `ux_lint --base` report 첨부.

## 범위 밖

AppShell·로그인·AdminPageHeader·skip-link(T-035 후 별도 task), DataTable·overlay(v0.2; airport는 표 화면이 없어 채택 계획 없음), 백엔드, 사용자 표면 대시보드 재디자인.

## 대상 저장소·브랜치·PR·되돌리기

- `digitie/kor-travel-airport`, 브랜치 `codex/T-432-ui-small`(Draft PR), `main`에서 분기. PR 1개.
- 되돌리기 = `git revert <merge-sha>` + `npm ci`.

## 예상 변경 파일

아래는 이 task가 만들거나 고칠 예정 경로다. 예정 경로는 존재·실행 증거가 아니다.

```text
frontend/src/components/ui/<small-component>.tsx       # 0.1 공개 부품 shim
frontend/src/components/<backup-panel>.tsx, <collector-status>.tsx   # 실제 파일명은 착수 시 대조
frontend/src/app/globals.css                           # @source
frontend/package.json, frontend/package-lock.json
frontend/kor-travel-common.lock.json                   # ui.version, ux_gate.baseline
```

## 수용 기준

- [ ] frontend CI(vitest·tsc·build) green; 패널 관련 vitest가 `data-slot`·testid 계약으로 갱신되어 0 test가 아니다.
- [ ] 6폭 스크린샷: 패널 영역 diff는 허용(부품 교체)하되 페이지 나머지 diff 0, 320px 가로 스크롤 0. 변경 전후 캡처를 PR에 나란히 첨부.
- [ ] `ux_lint --base` 신규 위반 0; `window.confirm` 1건은 baseline 표시.
- [ ] `next build`(webpack)·`--turbopack` 양쪽 green.
- [ ] 공개 부품의 로컬 패치 0건. T-211 도구가 아직 없으면 shim/patch 수동 대조의 파일 목록·diff·담당자를 기록한다. T-211 완료 후 도구로 재확인하며 아직 없는 후행 도구를 이 task 완료 선행으로 삼지 않는다.

## 검증 명령

```bash
# kor-travel-airport/frontend
npm ci && npx tsc --noEmit && npm test && npm run build && npx next build --turbopack
# kor-travel-common
python3 -B -X utf8 tools/ux_lint.py --root ../kor-travel-airport/frontend --base origin/main
# T-211 완료 후 실행; 그 전에는 위 수동 대조 evidence
python3 -B -X utf8 tools/ui_drift.py --root ../kor-travel-airport/frontend
```

## evidence

PR 본문(전후 캡처·테스트 수·빌드 로그), `consumers.pins.json`·`docs/integration-map.md`·`docs/journal.md`, 이 파일 "실행 기록". T-212가 이 PR을 검증 경로로 썼으면 T-212 evidence에 링크.

## rollback·release 차단 조건

- 빌드 실패·계약 불일치·페이지 외 영역 diff면 머지 금지, 머지 후 발견 시 revert.
- T-431 미머지면 이 PR을 열지 않는다(토큰 없이 `kt-` 유틸리티가 비어 렌더 깨짐).
