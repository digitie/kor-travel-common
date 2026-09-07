# `@kor-travel/tokens`

`kor-travel-common`의 공용 디자인 토큰 패키지다. 토큰 값의 정본은 `tokens.css`이며, `dist/`의 JSON·TypeScript·Tailwind preset은 `npm run build`로 생성한다.

Tailwind v4 앱은 다음 순서로 CSS를 가져온다.

```css
@import "tailwindcss";
@import "@kor-travel/tokens/theme.css";
@import "@kor-travel/tokens/shadcn.css";
@import "@kor-travel/tokens/base.css";
```

다크 모드는 앱이 `dark-class.css` 또는 `dark-media.css` 중 하나를 선택한다. 레거시 어휘 별칭 shim은 T-102에서 추가하며 이 패키지의 T-101 산출물에는 포함하지 않는다.

이 패키지는 GPL-3.0-or-later로 배포되며 폰트 파일이나 폰트 로더를 포함하지 않는다. 저작권·서드파티 고지는 동봉 문서를 따른다.
