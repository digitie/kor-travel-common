# 프론트엔드 공통 라이브러리와 산출물 일치

2026-11-11 사용자 지시를 반영한다. 정확 버전과 프로필의 유일한 정본은 [versions.json](../../versions.json)의 axes·frontendPolicy다. [frontend-dependencies.json](../../frontend-dependencies.json)은 빌드 시 생성하고 CI에서 동일성을 검사한다. UI와 tokens에 담는 dependency-policy.json도 같은 생성물이다.

## 필수 사용과 범위

Geo·Map·Weather·Concierge·Docker Manager·Pinvi 웹/관리자·Transport 웹/관리 UI가 대상이다. Pinvi 모바일은 NativeWind5 RC와 대응 스타일 엔진을 통해 Tailwind4를 적용하며 DOM용 UI는 설치하지 않는다. 앱의 도메인 의존성 목록을 강제로 같게 만들지는 않지만, 공통 사용 가능한 기능은 같은 구현과 버전으로 채택한다.

공통 컴포넌트는 shadcn/ui Radix, 표는 TanStack Table9·Virtual3의 VirtualTable이다. React Hook Form·Zod는 입력 등록과 검증에, Zustand는 실제 화면 상태에 적용한다. 기본 로그인은 인스턴스별 저장소를 사용하고 비밀번호를 전역 상태에 넣지 않는다. 권한·API·인증 저장소는 앱 소유다. Radix가 내부적으로 사용하는 Floating UI는 전이 의존성이며 앱에서 별도 overlay 엔진을 직접 구현하지 않는다.

지도는 maplibre-vworld-react GitHub의 정확 커밋에서 core/web/RN을 빌드한다. 이동하는 main 참조와 개발자별 재포장은 배포 참조로 사용하지 않는다. 라이브러리의 재현된 결함은 원 저장소에서 수정·검증한 후 같은 산출물을 소비한다.

## 버전 표

다음 표는 생성 정책의 검토용 표현이다.

| 라이브러리 | 정확 버전 |
|---|---|
| @axe-core/playwright | 4.14.0 |
| @hookform/resolvers | 7.0.5 |
| @kor-travel/tokens | 0.1.1 |
| @kor-travel/ui | 0.2.0 |
| @next/eslint-plugin-next | 16.4.6 |
| @playwright/test | 1.65.0 |
| @tailwindcss/postcss | 4.3.5 |
| @tanstack/react-query | 5.107.1 |
| @tanstack/react-table | 9.3.1 |
| @tanstack/react-virtual | 3.14.26 |
| @testing-library/dom | 10.4.2 |
| @testing-library/jest-dom | 7.0.1 |
| @testing-library/react | 16.3.3 |
| @testing-library/user-event | 14.6.9 |
| @types/node | 22.20.5 |
| @types/react | 19.3.0 |
| @types/react-dom | 19.3.0 |
| @vitejs/plugin-react | 6.3.0 |
| autoprefixer | 10.6.2 |
| class-variance-authority | 0.7.1 |
| clsx | 2.1.1 |
| eslint | 10.14.0 |
| eslint-config-next | 16.4.6 |
| eslint-import-resolver-typescript | 4.4.5 |
| eslint-plugin-import-x | 4.18.1 |
| eslint-plugin-jsx-a11y-x | 0.2.0 |
| eslint-plugin-react-dom | 5.30.1 |
| eslint-plugin-react-hooks | 7.1.1 |
| eslint-plugin-react-x | 5.30.1 |
| jsdom | 31.0.0 |
| lucide-react | 1.72.0 |
| maplibre-gl | 6.17.0 |
| nativewind | 5.0.0-rc.1 |
| next | 16.4.6 |
| next-intl | 4.15.0 |
| openapi-typescript | 7.13.0 |
| postcss | 8.5.32 |
| pretendard | 1.3.9 |
| radix-ui | 1.8.1 |
| react | 19.3.1 |
| react-doctor | 0.9.22 |
| react-dom | 19.3.1 |
| react-hook-form | 7.92.0 |
| react-native | 0.88.1 |
| react-native-css | 3.1.0-rc.1 |
| recharts | 3.10.1 |
| shadcn | 4.23.0 |
| sharp | 0.35.5 |
| sonner | 2.0.8 |
| tailwind-merge | 3.7.0 |
| tailwindcss | 4.3.5 |
| tw-animate-css | 1.4.0 |
| typescript | 5.9.3 |
| typescript-eslint | 8.72.2 |
| undici | 8.12.4 |
| vite | 8.3.8 |
| vite-tsconfig-paths | 6.1.1 |
| vitest | 5.1.0 |
| vworld-map-core | 1.0.1 |
| vworld-map-rn | 1.0.1 |
| vworld-map-web | 1.0.3 |
| zod | 4.6.7 |
| zustand | 5.1.0 |

TypeScript는 OpenAPI 생성기와 typescript-eslint peer 범위 때문에 5.9.3, Node 타입은 Node22 실행환경에 맞춘다. NativeWind RC는 사용자 승인에 따른 것으로 대응 엔진과 함께 고정한다. stable로 표시하지 않는다.

## CSS와 글꼴

웹은 Tailwind4, tokens/theme.css, tokens/radix.css, tokens/font.css를 가져오고 UI dist를 Tailwind source에 포함한다. radix.css는 공통 부품의 Tailwind 어휘를 의미 토큰에 연결하고 공식 shadcn 상태 variant를 포함하는 선택형 bridge다. [공식 eject 절차](https://ui.shadcn.com/docs/changelog/2026-05-shadcn-eject)에 따라 CSS 원문·MIT 고지를 동봉하여 CLI 전체를 실행 의존성으로 넣지 않는다. 앱의 지역 색상은 그 뒤 같은 의미 토큰을 오버라이드한다. Pretendard는 로컬 자산을 제공하며 모바일은 네이티브 font loader로 실제 파일을 로드한다. CSS import만으로 모바일 글꼴이 적용되었다고 보지 않는다.

## 검사와 갱신

웹은 @kor-travel/ui/check-dependencies.mjs, 모바일은 @kor-travel/tokens/check-dependencies.mjs를 check:dependencies 및 CI에서 실행한다. --profile mobile, --package, --lock, --workspace로 대상 frontend를 지정하고 --artifacts common-artifacts.json을 반드시 전달한다. 필수 직접 의존성·정확 선언·workspace lock의 실제 버전·공통 파일과 원장 및 lock SHA512가 다르면 실패한다.

중앙 reusable CI의 실행 코드는 검토한 common40자리 커밋으로 고정한다. 비교할 버전·산출물 데이터는 현재 common main의 단일 정본을 읽고 실제 관찰 SHA를 기록한다. 이 main은 배포 파일 참조가 아닌 검증 정책 데이터다. 앱이 오래된 workflow/내장 정책을 유지해도 최신 정본과 다른 버전·해시는 중앙 CI에서 실패한다. 앱이 vendor 파일·원장·lock을 함께 바꿔 자체 검사만 통과하는 차이를 차단한다. 로컬 검사에서는 --canonical 경로를 추가해 같은 검증을 실행할 수 있다.

소스 경로는 --source를 반복 지정하거나 앱의 src/app/components/lib에서 자동 검색한다. 소스가 없으면 실패한다. 개별 table/Table 마크업과 Base UI/Floating UI 직접 구현의 재도입도 검사한다. 동적 마크업까지 증명하는 정적 분석기는 아니므로 공개 API 계약 시험과 코드 리뷰를 함께 유지한다.

갱신은 registry와 peer 확인 → 정본 변경 → 공통 구현·테스트 → 단일 pack·원장 생성 → 소비자 동일 bytes 적용·lock 갱신 → 앱 검증 → 같은 불변 커밋 기준의 독립 리뷰2인 → PR CI·머지 → 새 이미지 빌드·배포·동작 확인 순서다. 릴리스된 같은 버전에 다른 bytes를 덮어쓰지 않는다.

## 현재 수용 상태

이 변경은 구현 후보이며 최종 배포 수용을 뜻하지 않는다. 최종 source commit·산출물 해시·앱별 테스트·리뷰·PR·이미지 digest·배포 결과는 Geo의 단일 통합 보고서에서 기록한다.
