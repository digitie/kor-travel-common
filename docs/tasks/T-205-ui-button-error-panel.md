# T-205 Button(D-09 계약)·AppErrorPanel·error-recovery

- 상태: BLOCKED
- 우선순위: P1
- Gate: 단위 테스트
- 선행: T-203, T-212

## 목표

세 계열(map/concierge base-ui, pinvi native 두 벌, airport WIP shadcn 기본)로 갈라진 Button을 [브리프](../plan/design-brief.md) D-09 계약 하나로 통합하고, 5앱이 같은 계보로 갖고 있는 `AppErrorPanel` + `error-recovery`를 공통 부품으로 옮긴다. v0.2.0(T-213)의 첫 항목이며 overlay·DataTable·Pager가 이 Button에 의존한다.

## 고정 결정

- ADR-007 — [ADR 색인](../adr/README.md). D-09 Button 계약: `type="button"` 엔진 무관 명시 기본 · `loading` = `aria-disabled` + `aria-busy` + spinner + 포커스 유지 + `onClick` 차단(native `disabled`를 걸지 않음) · `disabled` = native + `disabledReason` → `title` · root opacity 금지(라벨 자식 래퍼만 흐림) · variant 7종(default/outline/secondary/ghost/destructive/destructive-solid/link) · size 8종(default/sm/xs/lg/icon/icon-sm/icon-xs/icon-lg; xs·lg·icon-xs·icon-lg는 deprecated alias). 비-overlay이므로 native `<button>` + `useRender`.
- 규칙 정본: [ui-contract](../standards/ui-contract.md), [ux-guide](../standards/ux-guide.md) UX-G4.2(오류 3부 + 회복 행동)·G4.3(chunk/RSC/network 계열만 같은 pathname 1회 hard reload, 반복 시 패널)·G9.2(`disabled`/`aria-disabled` 두 벌, 흐림은 라벨 자식)·G4.5(버튼 스피너는 라벨 유지), [licensing](../standards/licensing.md)(geo 유래 `-only` 병기).
- 사실 근거: [ui-components](../survey/cross/ui-components.md) §3.1(구현 6종 비교표·회귀 위험 표), §3.4 AppErrorPanel(map/geo/ktdm props 동일 `error`/`reset?`/`standalone?`), §4.2; [ux-patterns](../survey/cross/ux-patterns.md) G4.3(error-recovery 원천 geo `lib/error-recovery.ts`, 5앱 동일)·C19(weather·kta 오류 페이지 부재); [map 인벤토리](../survey/inventory/kor-travel-map.md) §8-6(8-state 레시피).
- 출처: Button·button-variants는 map 원천(GPL-3.0-or-later). error-recovery는 geo 원천이므로 헤더에 `Origin: kor-travel-geo@1d9d74d … (GPL-3.0-only)`를 병기(D-17, O-20 재선언 전까지).

## 구현 범위

- `src/button.tsx` + `src/button-variants.ts`(T-203의 레시피 파일을 여기서 완성): D-09 계약 전항. `loading` 중 `onClick`은 `preventDefault` 후 차단(폼 submit 방지). `render` 합성 지원(`render={<Link/>}`). deprecated size alias는 타입에 `@deprecated` JSDoc.
- `src/app-error-panel.tsx`: `Alert` + `Button` 조합, what/why/what-to-do 3부, `reset` 있으면 재시도 버튼, `standalone`이면 페이지 레이아웃.
- `src/error-recovery.ts`: `shouldHardReload(error)`(chunk/RSC/network 판별) + `sessionStorage` 키 `kt:error-recovery:<pathname>`으로 1회 reload, 두 번째는 패널.
- 테스트: `type` 기본값, `type="submit"` 명시 시 유지, `loading` 시 포커스 유지·클릭 무시·`aria-busy`·`aria-disabled`, `disabled` + `disabledReason` → `title`, root에 opacity 클래스 없음, 7 variant × 대표 size 스냅샷 없이 클래스 존재 검사, `render` 합성; AppErrorPanel 3부 렌더·`reset` 호출; error-recovery 1회 reload·2회째 패널(reload는 mock).
- `exports`: `./button`, `./app-error-panel`, `./error-recovery`.

## 범위 밖

- `ConfirmDialog`(API 4종 미합의, T-508 보류), `LoginForm`/`LoginScreen`(인증 경계), pinvi 사용자 표면 `ui/Button`(D-29), geo `asChild` 호출부 17곳 변환(T-444), airport `disabled:opacity-50` 레시피 교체(T-430 정렬 PR), 토스트.

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다.

```text
packages/ui/src/button.tsx  packages/ui/src/button-variants.ts  packages/ui/src/button.test.tsx
packages/ui/src/app-error-panel.tsx  packages/ui/src/app-error-panel.test.tsx
packages/ui/src/error-recovery.ts  packages/ui/src/error-recovery.test.ts
packages/ui/package.json  (exports 3 subpath)
packages/ui/smoke/next-app/app/error.tsx  (AppErrorPanel 사용 예)
PROVENANCE.md  (map·geo 원천 행)
```

## 수용 기준

- 렌더된 `<button>`의 `type` 기본값이 `"button"`이고 `<form>` 안에서 클릭해도 submit 이벤트가 발생하지 않는다.
- `loading` 상태에서 `document.activeElement`가 버튼에 남고 `onClick` 핸들러가 호출되지 않으며 native `disabled` 속성이 없다.
- `disabled` + `disabledReason="…"`이면 `title` 속성에 사유가 있고 native `disabled`가 있다.
- root 요소 클래스에 `opacity-` 계열이 없고 라벨 래퍼에만 흐림 클래스가 있다(T-103 `ux_lint` 금지 패턴 `aria-disabled:opacity-` 0건).
- AppErrorPanel props 타입이 map/geo/ktdm 현행(`error`, `reset?`, `standalone?`)과 호환(타입 테스트).
- error-recovery: 같은 pathname에서 첫 chunk 오류는 reload 1회, 두 번째는 패널; network가 아닌 일반 오류는 reload 없이 패널.
- vitest 실패 0·skip 0, axe 위반 0, `check-kt-classes.mjs` 위반 0.

## 검증 명령

```bash
npm run test -w packages/ui -- button app-error-panel error-recovery
npm run build -w packages/ui && node packages/ui/scripts/check-kt-classes.mjs
npx tsc --noEmit -p packages/ui
python3 -B -X utf8 tools/ux_lint.py packages/ui/src
```

## evidence

PR 본문·`docs/journal.md`에 테스트 수·exit code, `ux_lint` report, 원천 파일(map `button.tsx`·`button-variants.ts`, geo `error-recovery.ts`) 대비 변경 요약을 남긴다.

## rollback 또는 release 차단 조건

- 컴포넌트 단위 revert. 소비자 영향은 T-213 이후에만 생긴다.
- 차단: `type` 기본이 submit으로 돌아가는 회귀(pinvi 폼 보조 버튼 사고 재현), `loading`에 native disabled 사용(포커스 이탈), geo 유래 파일의 라이선스 병기 누락. 하나라도 있으면 T-213 rc를 만들지 않는다.
