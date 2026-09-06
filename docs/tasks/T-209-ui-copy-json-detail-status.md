# T-209 CopyButton·JsonViewer·DetailList(`onNotify` 주입)·StatusBadge(사전 주입형)

- 상태: BLOCKED
- 우선순위: P2
- Gate: 단위 테스트
- 선행: T-206

## 목표

피드백 채널(sonner vs inline)과 도메인 사전(`lib/status-label`)이 앱마다 달라 2차로 미뤄진 네 부품을, 토스트·사전을 prop으로 주입받는 형태로 공통화한다. 성공은 조용히(UX-G4.1) 원칙에 따라 CopyButton의 기본 피드백은 인라인이며 토스트 엔진은 앱이 소유한다.

## 고정 결정

- ADR-007 — [ADR 색인](../adr/README.md). [브리프](../plan/design-brief.md) D-09·D-13: 토스트 엔진은 앱 소유(정책 UX-G4.1만 공통), 상태 5-tone 이름 채택(geo CANCELLED 매핑은 보류), 마커 팔레트는 common 소유 아님(D-26).
- 규칙 정본: [ui-contract](../standards/ui-contract.md), [ux-guide](../standards/ux-guide.md) UX-G8.2(CopyButton 아이콘 스왑 + sr-only live "복사됨", 비보안 컨텍스트 폴백)·G8.3(JsonViewer mono 12px·`—`·copyable·destructive tone)·G3.2(DetailList `—` null glyph·mono 식별자·tabular-nums·copyable·help)·G5.1~G5.4(5-tone 의미, enum raw 렌더 금지, dot + 텍스트, HTTP 코드 tone)·G4.1(성공 조용히).
- 사실 근거: [ui-components](../survey/cross/ui-components.md) §2.2(copy-button 피드백 채널 상이 map 87/pinvi 131행, json-viewer·detail-list 유사, status-badge 5종 + tone 5종 ← `lib/status-label`), §3.4 Toast 행, §4.2, §7-5; [ux-patterns](../survey/cross/ux-patterns.md) C8(토스트 엔진 4종·없음 2앱)·C9(tone 이름 충돌).
- 이 task에서 확정하는 선택: `CopyButton`은 인라인 상태(copied/error/unsupported)를 기본으로 하고 `onNotify?(event)`가 있으면 앱이 토스트로 연결한다(pinvi 방식은 코드 복사 없이 재구현, B1). `StatusBadge`는 헤드리스 `{tone, label, dot}` + `defineStatusDictionary()`로 앱 사전을 주입하며 `HttpStatusBadge`(G5.4 규칙 내장)·`LiveBadge`만 공통이 값을 정한다. `LevelBadge`·`SeverityBadge`는 앱 사전 인스턴스.

## 구현 범위

- `src/copy-button.tsx`: `value`/`label`, `navigator.clipboard` + 비보안 컨텍스트 폴백(선택 안내), 아이콘 스왑 + `role="status"` sr-only, `onNotify`.
- `src/json-viewer.tsx`: `value`/`maxHeight`/`tone`/`copyable`(CopyButton 사용), `null`/`undefined` → `—`.
- `src/detail-list.tsx`: `items[]{label,value,mono,copyable,href,help,numeric}`, `columns`/`layout`, HelpTip(T-206)·CopyButton 의존, `onNotify` 전달.
- `src/status-badge.tsx` + `status-badge-variants.ts`: `StatusBadge`(tone ← `StatusTone`, T-203), `defineStatusDictionary`, `HttpStatusBadge`(2xx neutral·3xx info·4xx warning·5xx destructive), `LiveBadge`.
- 테스트: 클립보드 mock으로 copied/error/unsupported 3경로 + `onNotify` 호출; JsonViewer `—`·copyable; DetailList 각 item 옵션; StatusBadge dot 존재·raw enum 미노출·HTTP tone 매핑.
- `exports` 4 subpath.

## 범위 밖

- 토스트 컴포넌트·Toaster 마운트(앱), `statusLabel` 사전 값(앱), geo `JsonBlock`/`KeyValueGrid`·ktdm `CopyableCommand` 대체(앱 이관 task), geo CANCELLED 의미 확인(D-13 보류).

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다.

```text
packages/ui/src/{copy-button,json-viewer,detail-list,status-badge}.tsx
packages/ui/src/status-badge-variants.ts
packages/ui/src/*.test.tsx  (4 파일)
packages/ui/package.json  (exports 4)
packages/ui/smoke/next-app/app/detail/page.tsx
PROVENANCE.md
```

## 수용 기준

- CopyButton: 복사 성공 시 토스트 없이 아이콘이 바뀌고 `role="status"` 영역에 "복사됨"이 나타나며, `onNotify`를 주면 `{kind: "copied"}`가 1회 호출된다; `navigator.clipboard` 부재 시 `unsupported` 경로가 렌더된다.
- JsonViewer: `value`가 `null`이면 `—`, `copyable`이면 CopyButton이 있고 `tone="destructive"` 클래스가 적용된다.
- DetailList: `copyable` item에만 CopyButton, `help`가 있으면 HelpTip 접근성 이름 `도움말: {label}`, `numeric`이면 tabular-nums 클래스.
- StatusBadge: dot 요소가 있고 텍스트가 사전의 라벨이며 raw enum 문자열이 DOM에 없다; `HttpStatusBadge(404)` tone `warning`, `(503)` `destructive`.
- vitest 실패 0·skip 0, axe 위반 0, `check-kt-classes.mjs` 위반 0, `check-directives.mjs` 불일치 0.

## 검증 명령

```bash
npm run test -w packages/ui -- copy-button json-viewer detail-list status-badge
npm run build -w packages/ui && node packages/ui/scripts/check-kt-classes.mjs && node packages/ui/scripts/check-directives.mjs
npx tsc --noEmit -p packages/ui
```

## evidence

PR 본문·`docs/journal.md`에 테스트 수·exit code, axe 결과, map 원본 대비 API 변경(sonner 제거·`onNotify`·사전 주입)을 표로 남긴다.

## rollback 또는 release 차단 조건

- 컴포넌트 단위 revert.
- 차단: 공통 코드가 `sonner` 등 특정 토스트 엔진을 import, 사전 값이 공통에 하드코딩, pinvi 코드 복사 흔적. 하나라도 있으면 T-213 rc를 만들지 않는다.
