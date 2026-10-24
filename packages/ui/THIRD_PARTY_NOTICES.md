# UI 패키지 고지

이 패키지의 컴포넌트·순수 함수는 자체 작성이며 GPL-3.0-or-later로 제공한다. 외부 컴포넌트 소스·아이콘을 배포물에 복사하거나 번들하지 않는다. GPL 전문은 [LICENSE](LICENSE), 저작권 고지는 [NOTICE](NOTICE)에 있다.

React·React DOM(MIT), tokens는 peer이며 별도로 설치한 배포물의 고지가 적용된다. 개발용 Vitest·Testing Library·TypeScript·axe-core 등은 tarball에 포함하지 않는다. 지도 컨트롤은 Base UI(MIT)와 Lucide(ISC)를 런타임 의존성으로 사용하며 각 설치 배포물의 고지가 적용된다.

지도 필터·탭·상세 배치는 `digitie/kor-travel-map@974e2d025`의 Feature 지도·필터·버튼·탭 레시피(GPL-3.0-or-later)를 공용 토큰과 API로 재구성했다. 지도 엔진·provider·도메인 코드는 포함하지 않는다.
