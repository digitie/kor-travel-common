# `@kor-travel/tokens`

`kor-travel-common`의 공용 디자인 토큰 패키지다. 토큰 값의 정본은 `tokens.css`이며, `dist/`의 JSON·TypeScript·Tailwind preset은 `npm run build`로 생성한다.

Tailwind v4 앱은 다음 순서로 CSS를 가져온다.

```css
@import "tailwindcss";
@import "@kor-travel/tokens/theme.css";
@import "@kor-travel/tokens/shadcn.css";
@import "@kor-travel/tokens/base.css";
```

다크 모드는 앱이 `dark-class.css` 또는 `dark-media.css` 중 하나를 선택한다. 여러 표면을 한 앱에서 섞을 때는 `data-kt-surface`를 같은 요소에 두고 `shadcn.css`의 스코프 파생 alias가 프로필 semantic 값을 다시 참조하게 한다. 레거시 map·weather·geo 어휘가 필요한 이관 앱은 선택적으로 `@kor-travel/tokens/aliases/map-vocabulary.css`를 import한다. 이 파일은 shadcn 이름을 중복 선언하지 않고 패키지의 `shadcn.css`를 내부 import한다. weather 값 재현 예제와 앱 전용 `--space-*` 간격은 `examples/`에 있으며 npm 배포 대상이 아니다.

이 패키지는 GPL-3.0-or-later로 배포되며 폰트 파일이나 폰트 로더를 포함하지 않는다. 저작권·서드파티 고지는 동봉 문서를 따른다.
