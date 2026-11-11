# 프론트엔드 공통 라이브러리와 산출물 일치

2026-11-11 사용자 지시를 반영한다. 정확 버전과 프로필의 유일한 정본은 [versions.json](../../versions.json)의 axes·frontendPolicy다. [frontend-dependencies.json](../../frontend-dependencies.json)은 빌드 시 생성하고 CI에서 동일성을 검사한다. UI와 tokens에 담는 dependency-policy.json도 같은 생성물이다.

## 필수 사용과 범위

Geo·Map·Weather·Concierge·Docker Manager·Pinvi 웹/관리자·Transport 웹/관리 UI가 대상이다. Pinvi 모바일은 NativeWind5 RC와 대응 스타일 엔진을 통해 Tailwind4를 적용하며 DOM용 UI는 설치하지 않는다. 앱의 도메인 의존성 목록을 강제로 같게 만들지는 않지만, 공통 사용 가능한 기능은 같은 구현과 버전으로 채택한다.

공통 컴포넌트는 shadcn/ui Radix, 표는 TanStack Table9·Virtual3의 VirtualTable이다. React Hook Form·Zod는 입력 등록과 검증에, Zustand는 실제 화면 상태에 적용한다. 기본 로그인은 인스턴스별 저장소를 사용하고 비밀번호를 전역 상태에 넣지 않는다. 권한·API·인증 저장소는 앱 소유다. Radix가 내부적으로 사용하는 Floating UI는 전이 의존성이며 앱에서 별도 overlay 엔진을 직접 구현하지 않는다.

Radix FocusScope의 재현된 초기패널 Shift+Tab 결함은 원본 수정1.3.1+kortravel.fix.1의 단일 배포물로 적용한다. 웹의 직접 file 의존성·root override는 엔진을 같은 bytes로 공급하는 예외이며 앱에서 개별 Radix를 import하는 예외가 아니다. patchedRadixPackages의 각 이름은 공식 scoped 이름·exact 축·artifact 목록과 연결되어야 하고 잘못된 설정은 생성 전에 거부한다. [고정 출처·빌드·라이선스](../../vendor/README.md)를 따른다.

지도는 maplibre-vworld-react GitHub의 정확 커밋에서 core/web/RN을 빌드한다. 이동하는 main 참조와 개발자별 재포장은 배포 참조로 사용하지 않는다. 라이브러리의 재현된 결함은 원 저장소에서 수정·검증한 후 같은 산출물을 소비한다.

## 버전 표

다음 표는 versions.json에서 자동 생성하며 JSON 정책과 함께 CI에서 동일성을 검사한다.

<!-- frontend-library-versions:start -->

| 라이브러리 | 정확 버전 |
|---|---|
| @axe-core/playwright | 4.14.0 |
| @hookform/resolvers | 7.0.5 |
| @kor-travel/tokens | 0.1.1 |
| @kor-travel/ui | 0.2.0 |
| @next/eslint-plugin-next | 16.4.6 |
| @playwright/test | 1.65.0 |
| @radix-ui/react-focus-scope | 1.3.1+kortravel.fix.1 |
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
| lightningcss | 1.33.0+nativecss.fix.4 |
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

<!-- frontend-library-versions:end -->

TypeScript는 OpenAPI 생성기와 typescript-eslint peer 범위 때문에 5.9.3, Node 타입은 Node22 실행환경에 맞춘다. NativeWind RC는 사용자 승인에 따른 것으로 대응 엔진과 함께 고정한다. stable로 표시하지 않는다.

## CSS compiler의 공통 bytes

Lightning CSS는 웹과 모바일 모두 필수인 **빌드/개발 의존성**이다. runtimeRequired에는 넣지 않는다. 승인한 stable SemVer의 build metadata를 포함한 전체 문자열과 단일 vendor SHA512를 대조하며, metadata가 다른 같은 기본 버전도 같은 후보로 취급하지 않는다. 원본 수정과 라이선스/소스 동봉은 [vendor 고지](../../vendor/README.md)를 따른다.

앱 root나 모바일 workspace가 같은 물리 파일을 공유할 수 있다. file:vendor/...뿐 아니라 file:apps/web/vendor/...와 file:../web/vendor/...도 허용한다. 대상은 lock 루트 내부의 vendor 디렉터리와 정규 산출물 파일명이어야 한다. 절대 경로·루트 밖 경로·밖으로 나가는 symlink는 거부하며, 파일·원장·lock·중앙 SHA512 검증은 유지한다. 해당 앱이 실제로 참조하는 개발 그래프의 중첩 Lightning CSS도 같은 버전/bytes여야 한다. 앱에서 도달한 linked workspace의 devDependencies도 빌드 그래프에 포함한다. registry 패키지 자체의 개발 의존성과 연결되지 않은 다른 workspace의 설치본은 현재 앱 설치 그래프에 섞지 않는다.

common root와 실제 Next smoke/example의 설치 정의도 같은 tarball과 root override를 사용한다. 새 패키지 설치 전에 준비 스크립트가 생성 vendor를 복사하며 CI 경로에서도 이를 보존한다. 소비자별 로컬 재빌드/재포장으로 동일 버전의 다른 bytes를 만들지 않는다.

## CSS와 글꼴

웹은 Tailwind4, tokens/theme.css, tokens/radix.css, tokens/font.css를 가져오고 UI dist를 Tailwind source에 포함한다. radix.css는 공통 부품의 Tailwind 어휘를 의미 토큰에 연결하고 공식 shadcn 상태 variant를 포함하는 선택형 bridge다. [공식 eject 절차](https://ui.shadcn.com/docs/changelog/2026-05-shadcn-eject)에 따라 CSS 원문·MIT 고지를 동봉하여 CLI 전체를 실행 의존성으로 넣지 않는다. 앱의 지역 색상은 그 뒤 같은 의미 토큰을 오버라이드한다. Pretendard는 로컬 자산을 제공하며 모바일은 네이티브 font loader로 실제 파일을 로드한다. CSS import만으로 모바일 글꼴이 적용되었다고 보지 않는다.

## 검사와 갱신

웹은 @kor-travel/ui/check-dependencies.mjs, 모바일은 @kor-travel/tokens/check-dependencies.mjs를 check:dependencies 및 CI에서 실행한다. --profile mobile, --package, --lock, --workspace로 대상 frontend를 지정하고 --artifacts common-artifacts.json을 반드시 전달한다. 필수 직접 의존성·정확 선언·workspace lock의 실제 버전·공통 파일과 원장 및 lock SHA512가 다르면 실패한다.

중앙 reusable CI의 실행 코드는 검토한 common40자리 커밋으로 고정한다. 비교할 버전·산출물 데이터는 현재 common main의 단일 정본을 읽고 실제 관찰 SHA를 기록한다. 이 main은 배포 파일 참조가 아닌 검증 정책 데이터다. 앱이 오래된 workflow/내장 정책을 유지해도 최신 정본과 다른 버전·해시는 중앙 CI에서 실패한다. 앱이 vendor 파일·원장·lock을 함께 바꿔 자체 검사만 통과하는 차이를 차단한다. 루트뿐 아니라 실제 런타임·빌드와 도달한 linked workspace 개발 그래프의 모든 공통 산출물 복사본을 version/integrity로 검사한다. 무관 workspace와 설치되지 않은 registry 개발 그래프는 제외한다. 로컬 검사에서는 --canonical 경로를 추가해 같은 검증을 실행할 수 있다.

소스 경로는 --source를 반복 지정하거나 앱의 src/app/components/lib에서 자동 검색한다. 소스가 없으면 실패한다. 개별 table/Table 마크업과 Base UI/Floating UI 직접 구현의 재도입도 검사한다. 동적 마크업까지 증명하는 정적 분석기는 아니므로 공개 API 계약 시험과 코드 리뷰를 함께 유지한다.

갱신은 registry와 peer 확인 → 정본 변경 → 공통 구현·테스트 → 단일 pack·원장 생성 → 소비자 동일 bytes 적용·lock 갱신 → 앱 검증 → 같은 불변 커밋 기준의 독립 리뷰2인 → PR CI·머지 → 새 이미지 빌드·배포·동작 확인 순서다. 릴리스된 같은 버전에 다른 bytes를 덮어쓰지 않는다.

## 현재 수용 상태

이 변경은 구현 후보이며 최종 배포 수용을 뜻하지 않는다. 최종 source commit·산출물 해시·앱별 테스트·리뷰·PR·이미지 digest·배포 결과는 Geo의 단일 통합 보고서에서 기록한다.

옛 private mono-root인 maplibre-vworld-react 직접 설치를 모든 프로필에서 금지한다. 기존 source AST 검사도 정본 forbidden 목록의 정확한 package root와 / 하위 경로 import를 거부한다. 지도는 공개 core/web/RN 배포물을 사용하며 node_modules/maplibre-vworld-react/packages/* source alias로 되돌리지 않는다.

정적 모듈 경로 검사는 JS/TS·JSX/TSX·MJS/CJS·MTS/CTS에서 import, 재export, 외부 TS import, 타입 import와 리터럴 import()/require()를 동일하게 대조한다. 금지 이름의 정확 root 또는 root 뒤 / 경로를 거부하고 인접한 다른 패키지 이름은 허용한다. 설명 문자열과 주석을 모듈 로딩으로 오인하지 않는다.
