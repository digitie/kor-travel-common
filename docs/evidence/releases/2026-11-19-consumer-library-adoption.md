# 공통 라이브러리 소비·실제 실행 현황

2026-11-19 공통 리소스 릴리스의 소비 현황이다. 각 표면에 실제로 적용한 이미지와 검증 범위를 기록한다.

## 정본과 필요한 라이브러리

공통 구현은 shadcn/ui Radix, TanStack Table·Virtual의 VirtualTable, React Hook Form·Zod, Zustand, Pretendard다. 동일 이름을 사용하는 표면은 exact 버전과 동일 pack bytes를 소비한다. 도메인 의존성·권한·API·인증 저장소는 앱이 소유한다. 모바일은 NativeWind5 RC와 Tailwind4 및 공통 tokens를 적용한다.

필수·선택 프로필과 자동 생성 전체 버전 표는 [라이브러리 규약](../../standards/frontend-libraries.md), [정본 정책](../../../versions.json), [생성 프론트엔드 정책](../../../frontend-dependencies.json)을 따른다. 정책 application149개와 build tool3개는 실제 사용하는 Python 이름에 적용한다. 상세 장단점·105개 비교·149개 정확 버전·68개 프론트엔드 축은 [Geo의 단일 보고서 PR644](https://github.com/digitie/kor-travel-geo/pull/644)에 모은다.

## 변경 방지와 산출물

불변 UI0.2.3/tokens0.1.4/선택형Toast0.1.3의 producer는 `0e2a3f5aa16323df0d009360802661c9bc496dc6`, frontend catalog는 `d644632ea9eaf2f6b6baa49305d65fae5bbc0bd4`다. application 정책 출처는 `f7017c63a332b58365ff3ce1976de9e2cc452a2e`이며 기존 pack을 재포장하지 않는다. ZIP artifact14500111373/SHA256은 `19881f2c3ed598ed7ec213c559be21ece2be77068bddee6de5bd249b6f8019e1`다.

| pack | SHA256 | 파일 |
| --- | --- | ---: |
| kor-travel-ui-0.2.3.tgz | `aa19793165ae37b2214d210692e23235545e1464c4e0059f99d943411fa753d9` | 96 |
| kor-travel-tokens-0.1.4.tgz | `33d08d7b37c60d3e319da19608ce05137f6bf587dc8d42e3ce0dfb4b597a61fc` | 25 |
| kor-travel-toast-0.1.3.tgz | `34b514b270f88fc19c6b411b975d4497f91f3581530f32a39be264874ca09b37` | 8 |

웹은 UI96+tokens25=121파일,Geo는Toast8을 더한129파일,모바일 직접 tokens는25파일이다. exact·manifest·lock SRI·canonical pack·실제 설치 파일과 실제-used Python 교집합을 기존 검사기로 대조한다. reusable guard의 uses/common-ref는 같은 불변 ref를 쓴다. source·pack producer·정책·normal 이미지·native·실제 화면을 각각 기록한다.

## 현재 소비·실행 근거

| 표면 | source 관찰 | 공통 파일 | 실제 검증과 범위 |
| --- | --- | ---: | --- |
| Geo | API·코드 서버 `8260e3577ac1`, UI `500c84797b00` | 129 | 배포 후 ARM 실행, PC 1280px·모바일 390px 제목·테이블·인증 확인. UI 환경값과 API·코드 서버·DB 실행 상태 동일. |
| weather | `2b269b03d4ac` | 121 | ARM 3개 이미지·SDK627 적용. 27개 기존 상태 복원, 모바일 390px 수용. 첫 단기예보 진단 200·5.790초·`stale` |
| transport-public | `810373320c18` | 121 | SDK627 코어 적용·기존 일정 20개 복원. 공개 주차 390px·1280px 수용. 철도 첫 진단 200·7,766ms 및 조건부 304·305ms |
| transport-admin | UI `736b731faa54`;core `810373320c18` | 121 | 실제 db139445 UI,375/1280 PC세로메뉴·모바일메뉴·일반 로그인/로그아웃401;복사8h쿠키 서버회수는 기존 미지원 |
| transport-fuel | UI `2ed65d8d8ec3`·gateway `736b731faa54`·core `810373320c18` | 121 | Fuel 웹 단독 ARM·native 교체. 고정 12308·12307 및 API 게이트웨이 유지. 공개 HTTPS 390px·1280px에서 전체 화면·44×44px 위치 아이콘·위치 권한 허용 후 조회 확인 |
| pinvi-web | `716781d04657` | 121 | 현재2e62713a/ec02765b/073cfedb 설치65/78·공통PY19파일·UI121일치;공개CURRENT정산·현재1280/4타일/인증 수용.과거5폭은 이전tuple |
| pinvi-mobile-tokens | `716781d04657` | 25 | 소스/설치 정책에서NativeWind5 RC·Tailwind4·tokens 일치.실기기/EAS/스토어 미실행 |
| concierge | API/MCP/CS `9e2668142cd3`; UI `039c445a0a36` | 121 | API/MCP·CS 정상/native·SDK626·3개sensor복원·실제 화면/타일/인증 수용;재사용UI 출처 별도 기록 |
| manager-odroid | 기록 `db78d1a869c6`;wheel `30330a2cf0e9`;UI `7f07a171e39d` | 121 | 실제627 설치77모듈·28분포/pipcheck·인증 수용.동일bytes wheel30330·UI7f07 출처 유지 |
| manager-n150 | 기록 `db78d1a869c6`;wheel `30330a2cf0e9`;UI `7f07a171e39d` | 121 | 실제627 설치77모듈·28분포/pipcheck·인증 수용.동일bytes wheel30330·UI7f07 출처 유지 |

Map은 기존 담당 분담을 유지한다. 기존5폭 수용과 새 이미지1280 smoke를 같은 범위로 합치지 않는다. Manager의 UI7f07과 동일 code bytes의30330 wheel, Transport의 backendb750와UI736도 실제 출처를 따로 보존한다.

## 미완료와 해석 범위

- Transport 운영 `b7509988`의 철도 요청 첫 200은 3,067ms였다. 304 세 건은 141·263·176ms였고 커서와 전체 1,466행 수를 검증했다.
- Weather에서 현재 승인한 1,078격자 중 349격자의 최근 6시간 갱신을 확인했다. 6시간 목표에 필요한 조건은 운영 키 승인 한도와 공유 사용량 확인이다.

- Transport는 API 기동 후 같은 워커에서 철도 입력 지문을 한 번 읽는다. 동일 1,466행의 준비된 본문을 사용하는 로컬 HTTP 200 비교에서 중앙값이 154ms에서 103ms로 줄었다. 별도 반복 비교는 196ms에서 129ms였다. 입력 리비전 변경 시 다시 계산하고 API readiness는 기다리지 않는다. 운영 `8103733`에서는 첫 200이 7,766ms, 조건부 304가 305ms였다. 입력 지문 SQL을 재실행하지 않았으며 새 응답 본문 생성이 실행됐다. 첫 응답 1초 목표는 미달했다. [Transport PR #234](https://github.com/digitie/kor-travel-transport/pull/234)
- 동일 1,466행 본문을 새 릴리스로 먼저 발행한 로컬 PostgreSQL 검증에서 첫 200은 311ms에서 42ms로 줄었다. 운영 첫 요청까지 보장하려면 이전 API와 수집 중지 뒤, 새 API 시작 전에 실행할 배포 지점이 필요하다.
- 별도 공개 HTTPS 검증에서 지도와 API 상태가 200을 반환했다. 모바일 390px에서 제목과 메뉴가 없고 줌 10에 집계 없이 주유소 300건이 표시됐다.
- **Weather** 이전 `b5039fa8`에서 정기 Map 적재 중 503이 발생한 뒤 200으로 회복했다. 별도 저장 단기예보 진단은 HTTP 200, 16.469초였다. 새 `2b269b03`의 첫 진단은 HTTP 200, 5.790초였다. 두 표본의 부하와 시각은 다르고 새 표본의 원천은 `stale`이다. 적용 후 발행 센서 실행은 대기 조회 7.4초와 7.7초에 각각 27건과 36건을 발행했다. 11월 21일 08:30 KST 정기 소비와 일치한 Weather SHORT 접근 로그 47건은 모두 200이었다. 해당 관측 구간 SHORT 503은 0건이었다. 503 재발률과 6시간 신선도는 추가 운영 확인이 필요하다. [Weather PR #279](https://github.com/digitie/kor-travel-weather/pull/279)
- **transportSession**: 일반 로그아웃 뒤 쿠키 없는 보호 경로401.기존8h서명쿠키 복사본은 만료까지 유효;추가 서버회수 기능을 요구/구현한 것으로 표시하지 않음
- **mobile**: NativeWind5.0.0-rc.1/react-native-css3.1.0-rc.1의 RC 표기 유지;실기기/EAS/스토어 수용 아님
- **nativeABI**: 실제 GDAL Geo3.10.3/Transport3.13.3.인터프리터 Pinvi3.12.14/Transport3.12.16.149 application exact는 OS/인터프리터 바이너리 전체 일치 증거가 아님
- **PinviRebuild**: 다른 작업의 같은716 새tuple에 설치bytes·현재1280·공개adopt를 새로 연결.옛5폭/전체native/producer 영수증을 새image에 전용하지 않음

## CI 검사 순서

- **Geo** Common 웹 guard와 OpenAPI는 독립 실행한다. Python 정책이 끝난 뒤 백엔드·PostGIS·Dagster를 병렬로 시작한다. PR CI에서 정책 완료 후 세 작업이 2–3초 뒤 시작했다. [PR #653](https://github.com/digitie/kor-travel-geo/pull/653) · [검증 실행](https://github.com/digitie/kor-travel-geo/actions/runs/44840179735)
- **Transport** Common 웹 guard 뒤 공개·관리 웹이 병렬 실행한다. 공개 웹 런타임 계약 19건을 npm 설치 전에 실행한다. 이전 CI에서 뒤따르는 설치·검사에 약 86초가 걸렸다. [PR #236](https://github.com/digitie/kor-travel-transport/pull/236) · [검증 실행](https://github.com/digitie/kor-travel-transport/actions/runs/44840343022)
- **Weather** Python 정책과 Python 테스트는 병렬로 실행된다. 웹은 Common guard, 정적 검사·단위 테스트·빌드, Playwright 순서다. headless shell로 fixture 34건과 타일 5건을 유지한다. [PR #280](https://github.com/digitie/kor-travel-weather/pull/280) · [검증 실행](https://github.com/digitie/kor-travel-weather/actions/runs/44840934957)
- **Concierge** 웹 정적 검사·단위 테스트·빌드 뒤 브라우저 회귀 17건을 실행한다. 기본 Chromium headless 프로젝트에 필요한 shell만 내려받는다. [PR #281](https://github.com/digitie/kor-travel-concierge/pull/281) · [검증 실행](https://github.com/digitie/kor-travel-concierge/actions/runs/44841095023)
- **Pinvi** 웹 선행 검사는 lockfile·Common·Doctor·lint·typecheck 뒤 웹 빌드·이미지·E2E에 연결된다. 모바일은 lockfile 직후 스타일 계약을 검사한다. 기존 실패 두 건에서는 앞선 npm 설치에 28–36초를 사용했다. [PR #793](https://github.com/digitie/pinvi/pull/793) · [검증 실행](https://github.com/digitie/pinvi/actions/runs/44840388515)
- **Common** 비밀 값·버전 정책이 문서·도구·패키지의 선행 조건이다. 문서 job은 소스 SHA 직후 공백을 검사하고 Python·Node 설치를 시작한다. [PR #77](https://github.com/digitie/kor-travel-common/pull/77) · [검증 실행](https://github.com/digitie/kor-travel-common/actions/runs/44840180300)
- **Manager** 별도 Common 웹·Python 정책과 제품 검사를 병렬 실행한다. 웹은 빌드 통과 후 Chromium을 설치한다. 백엔드 21분 8초 중 pytest가 20분 45초였다. 현재 순서를 유지했다. [검증 실행](https://github.com/digitie/kor-travel-docker-manager/actions/runs/44646286987)
- **Map** Claude 담당 실행을 읽기 전용으로 비교했다. PostGIS 통합은 단위 행렬 성공 뒤 시작하며 lint·이미지·프런트엔드·fixture는 독립 실행한다. [검증 실행](https://github.com/digitie/kor-travel-map/actions/runs/44833958026)

68개 프론트엔드 exact의 정본은 위 라이브러리 규약과 생성 정책에 둔다. 이 근거 문서는 별도의 버전 규범을 만들지 않는다.
