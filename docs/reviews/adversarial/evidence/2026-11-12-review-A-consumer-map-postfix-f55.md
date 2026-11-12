# 원 A-CONS-P2-02 수정 후 검토 — Map f55

- runid `Mill-A-Map-f55`, 원 reviewer A(Mill), frontend/accessibility. 구현 비참여, source read-only, 상대 raw/verdict 미열람.
- 시작 UTC 2026-11-11T18:51:57.941551+00:00; 작성 UTC 2026-11-11T18:59:55.094465+00:00.
- source **f55c4c009952d4ad59494c0778643d718a3e4d07**, parent **b102c659b48e2e3c089cb4798c87b52a3affe623**. user의 Mapf55 지정 후 정확한 전체 SHA를 Git으로 확인했다. 별도 최종 소비자 전체 manifest가 제공되었다고 주장하지 않는다.
- 이전 original input925의 button/variants/utils bytes가 b102와 같음을 직접 확인했다. e4 merge의 backend 재검토를 새로 한 것이 아니다.
- 격리 `/tmp/review-A-map-f55/{before,after}`의 Git frontend snapshot. canonical C9 UI/tokens는 본인 Geo closure의 private 추출본, 나머지 기존 Geo modules를 읽기 참조했다. Map fresh install은 하지 않았다. source/vendor/lock를 변경하지 않았다.

**Verdict: PASS(이 원 finding source/markup/DOM 범위). A-CONS-P2-02 FIXED. 신규 P0/P1/P2/P3=0.** 원7repo report와 Map925 CONDITIONAL 기록은 보존하며 최종 C11 채택·전체 build/browser/CI/배포 승인은 별도다.

## 수정과 직접 원 공격

원 finding은 local Button이 variant/size를 destructure한 뒤 common ButtonPrimitive에 전달하지 않아 ghost/link에도 default bg-primary와 default size가 남던 문제다.

`packages/kor-travel-map-admin/frontend/src/components/ui/button.tsx:73` 부근에서 **variant={variant}, size={size}를 실제 common primitive에 전달**한다. 지역 CVA 전체를 제거했다. `button-variants.ts:1`에서 공통 순수 recipe를 사용하고, 색/크기 recipe를 재정의하지 않는다. Link/a용 helper는 그 공통 recipe에 지역 focus·disabled 도달성 클래스와 caller class만 합친다. 일반 Button도 공통 색상/크기를 받은 뒤 같은 최소 상호작용 클래스를 적용한다. loading의 native disabled 해제, 기존 label/root 보존 및 activation 차단 정책은 유지한다.

신규 동일 test bytes의 8개를 before/after에 적용했다. before **6FAIL/2PASS**, after **8PASS**를 본인이 직접 실행했다. variant/size3, default fill 누출2, Link recipe size1이 실제 red였고 loading/disabled 두 기존 계약은 before도 통과했다. loading 선택에서는 same root/label/focus·접근성 이름·aria busy/disabled·click 차단과 해제 후 click 재개를 검사한다. test assertion을 수정하지 않았다. `source-matches.json`에 test와 실제 source hashes를 남겼다.

원 A `button-forwarding-probe.cjs`를 같은 C9 common으로 다시 실행했다. default/ghost/link/outline × Map/common 8개 SSR 관찰을 비교했다.

| 원 SSR 공격 | 결과 |
|---|---|
| before b102 | exit1; Map의 요청 variant/size가 default로 출력, ghost/link bg-primary=true |
| after f55 | exit0; Map data-variant=요청값, data-size=icon-xs, ghost/link bg-primary=false |

after scoped TypeScript(button/variants/utils 및 import된 공개 types)도 exit0. old full source의 새 모든 사용처 타입 검사를 실행한 것으로 확대하지 않는다. Node22.22.2, Vitest5.1.0, React19.3.1, canonical C9 UI0.2.0/tokens0.1.1 API를 사용했다.

## 실제 실행·인계 증거 구분

```text
# git archive b102/f55 packages/kor-travel-map-admin/frontend, vendor 제외
# final 동일8 test를 before에도 추가; source는 original Git blob 유지
node node_modules/vitest/vitest.mjs run --config vitest.review.config.mjs
node E/before-ssr-probe.cjs
node E/after-ssr-probe.cjs
node node_modules/typescript/bin/tsc --project tsconfig.review.json
```

E=`review-A-map-f55-evidence/`. 직접 before/after unit 및 SSR 로그, source-delta.patch, source-matches.json, inputs.json, scoped-type.log를 보존했다. codegen/cache는 자기 fixture에만 생성했다. 별도 owner `validation/map-A-button-closure-20261112`의 동일 test8, 기존21+신규8, scoped type/lint/Doctor325files0 인계는 참고했지만 본인의 새 전체29/440·Doctor·D286 성공으로 기록하지 않는다.

전체 Map suite·webpack/Turbopack build·실제 theme/viewport browser·새 Scope2/C11 설치·정확 최신 CI는 **이번 NOT_RUN**. 이번 SSR은 class/markup 계약 검증이며 실제 CSS computed color/geometry를 측정하지 않았다. 신규 backend/search/migration/DB/API/Dagster lifecycle 검토도 아니다.

**A-CONS-P2-02 FIXED.** 후속 C11/final app manifest에서 이 수정 포함 여부와 최종 runtime/lock/browser gates를 별도 확인해야 한다. 이 원문이 Map925의 역사 verdict를 수정하거나 새 전체 앱 병합/배포를 승인하지 않는다.
