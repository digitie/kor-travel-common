# `@kor-travel/tokens` 서드파티 고지

마지막 확인: 2026-09-07 (T-101). 이 패키지는 외부 실행 코드나 폰트 파일을
번들하지 않으며, npm·PyPI에 게시하지 않는다.

## 원천 토큰

`tokens.css`의 semantic 값은 GPL-3.0-or-later인
[kor-travel-map](https://github.com/digitie/kor-travel-map)의
커밋 `c494e227e010565be295de3f9670b2f7c8c20944`에서 추출했다. 원천 경로는
`packages/kor-travel-map-admin/frontend/src/app/globals.css`와
`packages/kor-travel-map-admin/frontend/design.md`이고, common에서의 수정
범위는 저장소 `PROVENANCE.md`의 PV-013에 기록되어 있다. 원천 라이선스
전문은 이 패키지의 `LICENSE`와 저장소의 `LICENSES/` 기록을 따른다.

## 이름만 참조하는 구성요소

`tokens.css`의 폰트 스택에는 Pretendard, Noto Sans KR, Apple SD Gothic Neo,
SF Mono, Menlo, Consolas, 시스템 글꼴 이름만 들어 있다. 글꼴 파일이나 해당
프로젝트의 코드·고지는 이 패키지에 포함하지 않는다. Tailwind·shadcn·React
런타임도 의존성이나 번들 코드로 포함하지 않는다.

현재 패키지에는 별도 서드파티 소스 사본이 없으므로 추가 MIT·ISC·OFL 고지
항목은 없다. 향후 외부 코드를 포함할 때는 해당 버전·커밋·라이선스 전문과
출처를 이 파일과 `PROVENANCE.md`에 함께 추가한다.

shadcn-tailwind.css는 shadcn/ui MIT 원문에서 가져온 상태 variant·유틸리티다. 공식 eject 방식과 같이 common에 동봉하며 MIT 전문은 SHADCN_LICENSE에 있다. 출처·수정 표기는 파일 헤더와 PROVENANCE를 따른다.

Radix bridge의 애니메이션 유틸리티는 tw-animate-css1.4.0의 공개 CSS를 의존성으로 가져온다. 해당 MIT 고지는 배포 의존성 패키지에 포함된다.
