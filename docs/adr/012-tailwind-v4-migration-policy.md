# ADR-012: Tailwind v4 전환 정책(대상·순서·4단 PR·pinvi mobile 예외 보류)

- 상태: proposed — O-8(pinvi mobile Tailwind 3 예외) 사용자 승인 대기; 나머지 항목은 기본값으로 진행
- 날짜: 2026-09-06
- 근거 문서: `docs/plan/design-brief.md` D-08·D-29·O-8·O-9, `docs/survey/cross/version-matrix.md` §1.2·§5.2·§5.3, `docs/survey/cross/design-tokens.md` §3.6.3·§3.6.7(`@config`·`@theme` 우선순위 미확인), `docs/survey/inventory/kor-travel-weather.md` §9.1, `docs/survey/inventory/kor-travel-airport.md` §3.2, `docs/survey/inventory/pinvi.md` §3.2, `docs/survey/commonality-matrix.md` §3.3

## 컨텍스트

사용자 지시 (1)은 "Tailwind v4 미도입 앱은 v4 전환"이다. 조사 결과 실제 대상은 "v3→v4"가 아니라 대부분 "미도입→도입"이다(`vm` §1.2): weather admin(2,495행 순수 CSS, 170 클래스)과 airport main(순수 CSS; WIP `99b3f98`이 4.3.3 + shadcn 전환 중). v4를 쓰는 앱 중 geo·concierge·pinvi web은 `@config` v3 JS config를 병행해 이중 정본이며, `@config`와 `@theme`의 병합 우선순위는 미확인이다(`dt` §3.6.3). pinvi mobile은 NativeWind 4 + Tailwind 3.4.19이고 NativeWind 5는 preview라 v4 전환이 외부 의존이며, RN 정확 핀(react 19.2.6·RN 0.86.3)이 web React까지 묶는다(`inv/pinvi` §3.2). ktdm은 Next 14·React 18 위에 Tailwind 4.3.1 `@theme`을 쓴다.

## 결정

1. 대상 = 미도입→도입 2(airport WIP·weather) + `@config` v3 잔존 정리 3(geo·concierge·pinvi web) + 외부 대기 1(pinvi mobile).
2. 모든 대상은 "6폭 시각 기준선 캡처 → 설정만 → 토큰만 → 컴포넌트" 4단 별도 PR로 진행한다. 중단 조건: 시각 diff가 원인 불명으로 남으면 해당 단계 revert.
3. 순서·조건: ① airport WIP `codex/shadcn-ui-foundation` 병합(값 16/10·alpha line 유지, `cn`→clsx+tailwind-merge, shadcn/postcss devDependencies; O-9) ② ktdm은 Next 16·React 19·ESLint 9·Node 22 업그레이드 PR을 먼저 별도로, 그 후 `@theme`→`--kt-*` 매핑(`ops-*` CSS 잔존 허용) ③ geo는 `@config` 실효값을 빌드 산출 CSS로 검증한 뒤 `@theme` 단일화·`tailwind.config.ts` 삭제(React 19와 독립) ④ concierge는 CI 신설 후 hex fallback 블록·`@config` 제거·`--ktc-*`를 `--kt-*` 오버라이드로 재해석 ⑤ pinvi admin은 `[data-pv-surface='admin']` 스코프만 `--kt-*` 매핑, 사용자 preset 유지 ⑥ weather는 `tokens.css` 교체(Phase 1, Next 버전과 독립; 별칭 shim + font·`--rail` 오버라이드 동반) → Next 16·Vitest 4·Node 22 → `@import "tailwindcss/theme" layer(theme)` + `utilities`만(preflight 제외) → ui v0.2 후 셸·패널·폼·로그인 3분할 PR → preflight 활성화 + 잔존 도메인 CSS `@layer components`.
4. common 토큰을 도입한 앱은 `@config` 없이 CSS-first만 쓴다(ADR-006, `style-delivery.md` §4).
5. **pinvi mobile Tailwind 3 예외 등록은 지시 (1)의 축소이므로 O-8 사용자 승인 전에는 `versions.json` `exceptions`에 넣지 않고 열림으로 둔다.** 기본값은 "예외 등록 + NativeWind 5 GA 재평가"이며, 승인 전 문서에는 "사용자 승인 대기"로만 적는다. 승인 시 `tailwind-preset.cjs` 생성물이 mobile의 소비 경로다.

## 대안 검토

- **weather를 한 PR로 v4 전환**: 2,495행 CSS·bare element 23종의 전환 정량(`inv/kor-travel-weather` §9.1)이 커서 원인 불명 diff의 revert 단위가 너무 크다. `tokens.css` 교체를 먼저 분리하면 Phase 1에서 값 무변경 채택이 가능하다.
- **preflight를 처음부터 활성화**: bare element 스타일이 preflight와 충돌해 diff 원인을 분리할 수 없다. utilities만 먼저 도입한다.
- **geo `@config`를 검증 없이 삭제**: config의 `--ui-*` 매핑이 실효 CSS에 남아 있는지 미확인이라 삭제 시 회귀를 설명할 수 없다. 빌드 산출 CSS 대조를 선행한다.
- **pinvi mobile을 정렬 정책 범위에서 제외**: 지시 (1)과 (2)를 모두 축소한다. 예외 등록(기한부·재평가)이 지시에 더 가깝지만 그 자체도 축소이므로 사용자 승인을 요구한다.
- **airport WIP를 버리고 main에서 새로 전환**: WIP는 clean·CI 확인 대상이며 값 유지 병합이 가장 짧다(O-9).

## 결과

- weather·map은 Phase 1에서 값 무변경 토큰 채택으로 첫 시각 diff 0 evidence를 만들고, v4 도입 자체는 Next 16 업그레이드와 분리된다.
- `@config` 잔존 앱은 검증 단계가 하나 더 있어 채택이 늦지만 이중 정본이 해소된다.
- pinvi mobile은 O-8 승인 전까지 `check_versions`에서 `BELOW_FLOOR`로 보고되며(report 모드이므로 fail 아님) 문서에는 "사용자 승인 대기"로만 남는다.
- 이 ADR은 O-8 결정 시 `accepted`(예외 등록) 또는 새 ADR(범위 재정의)로 갱신한다.

## 후속·적용 위치

- 현재 설계: `docs/architecture/style-delivery.md` §4, `docs/architecture/adoption-readiness.md` G-TW4
- 규칙: `docs/standards/design-tokens.md`, `docs/standards/frontend-stack.md`
- 소비자 task: T-430·T-431(airport), T-470·T-472(ktdm), T-440·T-441(geo), T-451·T-453(concierge), T-421(pinvi admin), T-460~T-464(weather)
- 외부 확인: O-8(pinvi mobile), O-9(airport WIP)
