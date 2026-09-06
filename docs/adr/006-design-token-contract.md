# ADR-006: 디자인 토큰 계약(`--kt-*`·`kt-` 네임스페이스·계층·프로필·다크·대비·정본 CSS)

- 상태: accepted — O-4(네임스페이스)·O-11(다크)·O-13(마커 정본)은 기본값으로 진행
- 날짜: 2026-09-06
- 근거 문서: `docs/plan/design-brief.md` D-10·D-12·D-26·O-4·O-11·O-13, `docs/survey/cross/design-tokens.md` §3.1~§3.6·§5, `docs/survey/cross/ui-components.md` §6.3, `docs/survey/inventory/kor-travel-weather.md` §3.1, `docs/survey/inventory/pinvi.md` §3.1, `docs/survey/commonality-matrix.md` §2.1

## 컨텍스트

6개 admin이 map 원형의 역할명(surface·text·brand·control-line·radius 6/8·control 36/30·7단 스케일)으로 수렴했지만 접두와 값 형식이 다르다: map `--color-*`+`@theme inline`, geo 3층 `--ui-*`, concierge `--ktc-*` 125회, pinvi `--color-admin-*`, ktdm `@theme` OKLCH, weather는 map 값을 순수 CSS로 복사(map 어휘 294회, `--rail` 17rem)(`dt` §3.1·§3.2). shadcn alias의 `--input`·`--accent` 의미가 앱마다 다르고(`dt` §3.2.3), 대비 수치는 map만 검증됐다(`dt` §3.4.2). 같은 클래스 문자열이 pinvi admin·airport에서는 동작하지 않아 pinvi는 치환표, concierge는 config 매핑으로 풀었다(`ui` §6.3). `--kt-*`와 `kt-` 접두는 전 저장소 0회다. pinvi mobile은 CSS `@theme`을 쓸 수 없어 JSON/TS/v3 preset 출력이 필요하다.

## 결정

1. 변수 접두는 `--kt-*`(전 저장소 0회). 계층은 semantic ← app override 2단이며 primitive ramp를 강제하지 않는다.
2. 역할: surface 4(page/subtle/muted/card)·text 4(primary/secondary/tertiary/disabled)+strong(선택)·icon·border(장식)·control-line(3:1)·brand 4(brand/hover/tint/foreground)·focus·status 4(success/warning/info/destructive)+tint·overlay·radius 2(control 6/panel 8)·control 높이 2(36/30)·rail 22rem·duration 2(fast 100/base 150)·ease 2·shadow 2(elevated/modal)·z 5(nav/panel/overlay/modal/toast)·font 스택(sans/mono).
3. shadcn alias 의미 고정: `--input`=control-line, `--accent`=brand-tint, `--radius`=radius-control, `--border`=장식 border.
4. **정본은 `tokens.css`**이며 `tokens.json`(DTCG)·`tokens.ts`·`tailwind-preset.cjs`(v3/NativeWind)는 생성물이다(빌드 diff 검사). 기본값은 map 값, `.dark` 값 완비.
5. `theme.css`는 `--color-kt-*`·`--spacing-kt-*`·`--radius-kt-*`·`--font-kt-*`를 `@theme inline`으로, 타입 스케일 `--text-kt-*`는 `@theme`(비inline)으로 정의해 변수 가리기 기법을 지원한다. 패키지 내부 클래스는 `kt-` 접두 유틸리티만 쓴다(`bg-kt-surface-page`·`h-kt-control`·`rounded-kt-control`·`text-kt-2xs`).
6. 프로필 admin/consumer. consumer 값은 문서·`tokens.json` 의미 이름만(pinvi 소유). 한 앱에서 혼용 시 `[data-kt-surface]` 스코프 변수 가리기, `base.scoped.css` 제공.
7. 오버라이드 허용 목록 = brand 4·focus·paper 4·ink 4·status 4+tint(대비 검사 대상)·font 스택. 형태·높이·모션은 프로필로만.
8. 다크: `tokens.css` `.dark` 값 완비, 앱 오버라이드의 dark 값 선택, 활성화 파일(`dark-class.css`/`dark-media.css`) 앱 명시 import, 기본 `color-scheme: light`.
9. 대비: `tools/kt_contrast.py` light 쌍 필수·dark 쌍은 dark 활성 앱만, report 기본 + 앱 `contrast-baseline.json`(미달 쌍 + `until`), 신규 미달만 fail. 값 형식 OKLCH 권고·hex 허용.
10. 레거시 어휘 shim `aliases/map-vocabulary.css`(map·weather·geo 공통 이름 → `--kt-*`)를 선택 파일로 제공한다. 앱 고유 접두(`--ktc-*`·`--color-admin-*`·`--ui-*`)는 앱 파일이다. font 스택은 앱이 현재 스택으로 오버라이드하고(Pretendard 1순위는 로드하는 앱만), 폰트 파일은 배포하지 않는다.
11. 마커 팔레트 P-01~16은 common 소유가 아니다(규칙만; hex 정본은 map 확정 요청).

## 대안 검토

- **`--ktc-*` 승격(concierge 어휘를 계약으로)**: 마이그레이션 비용이 가장 낮지만 concierge에서 앱 전용과 common 계약이 이름으로 구분되지 않는다. 대신 concierge `--ktc-*`를 `--kt-*` 오버라이드로 재해석한다(D-08 ④).
- **접두 없는 클래스(`bg-surface-page`) + 앱 별칭 계층**: map·geo·concierge에서는 그대로 동작하지만 pinvi·airport에 별칭 계층(치환표·config)이 선행돼야 한다. `kt-` 접두는 별칭 계층 자체를 없앤다.
- **JSON(DTCG)을 정본으로 두고 CSS 생성**: 도구 의존이 늘고 Tailwind 없는 앱의 즉시 소비가 어렵다. 6개 저장소가 이미 CSS 변수를 정본으로 쓴다.
- **다크를 필수 검증**: 토글 없는 앱이 다수라 비용 대비 효과가 낮다. 정의 필수·활성 opt-in으로 둔다.

## 결과

- 소비자 필수 2줄(`@import "@kor-travel/tokens/theme.css"` + `@source`)로 ui 클래스가 어느 앱에서나 동작한다.
- 값이 map 기본값이므로 map·weather 1차 채택은 시각 diff 0을 목표로 한다.
- 오버라이드 허용 목록 밖 재선언은 규칙 위반이고, 대비 미달은 baseline 등록 없이는 새 fail이 된다.
- `@theme`(비inline) 타입 스케일 때문에 `theme.css`는 리터럴 값을 두지 않는다.

## 후속·적용 위치

- 현재 설계: `docs/architecture/style-delivery.md`, `docs/architecture/packages.md` §2
- 규칙: `docs/standards/design-tokens.md`(TK-n, T-104 확정)
- 실물: T-101(tokens), T-102(shim), T-103(`kt_contrast`·`ux_lint`), T-109(v0.1.0)
- 외부: T-505(마커 팔레트 hex 정본 요청, O-13)
