# T-218 Radix 공통 UI와 소비 앱 의존성 일치

- 상태: IN_PROGRESS
- 우선순위: P1
- Gate: 공통·소비자 계약 시험·브라우저·독립2리뷰·PR CI·배포 검증
- 선행: 없음

## 목표와 고정 결정

2026-11-11 사용자 지시로 [ADR-017](../adr/017-shadcn-radix-shared-components.md)에 따라 shadcn/ui Radix 공통 컴포넌트와 공통 VirtualTable, 입력·상태·글꼴을 실제 적용한다. [라이브러리 규약](../standards/frontend-libraries.md)을 따르며 기존 Base UI 채택 계획의 해당 부분을 대체한다.

## 구현 범위와 예상 변경 파일

packages/ui의 프리미티브·VirtualTable·LoginForm·DagsterOperations, packages/tokens의 Pretendard·Radix bridge, versions.json과 생성 정책·검사기·CI·관련 문서다. 앱 이관은 각 저장소의 개별 커밋·PR로 관리한다.

Geo·Map·Weather·Concierge·Docker Manager·Pinvi 웹/모바일·Transport를 병렬 처리한다. 작업 브랜치는 agent/codex-common-unification-20261111이며 각 PR 번호는 통합 evidence에 기록한다. 지도 라이브러리 결함은 maplibre-vworld-react 원본 저장소에서 수정한다.

## 범위 밖

앱 권한 정책·운영 비밀·DB 생명주기·도메인 전용 로직의 common 승격은 이 작업에서 하지 않는다. 과거의 모든 백엔드·설계 backlog 완료를 뜻하지 않는다.

## 수용 기준

- common의 lint·타입·빌드·UI/토큰·정책 검사가 통과한다.
- React Doctor 전체 검사에서 실제 진단을 조치하고 국소 예외는 근거를 남긴다.
- 모든 소비자는 동일한 단일 pack bytes·정확 버전·workspace lock을 사용한다.
- Pinvi NativeWind5 RC·Tailwind4와 native 글꼴을 검증한다.
- 전문영역이 다른 2인의 독립 리뷰와 finding 재검토를 완료한다.
- 각 PR CI·머지 후 새 이미지를 배포하고 실제 UI·API를 확인한다.

## 빌드·테스트 도구 후속 수용 기준

[ADR-018](../adr/018-exact-node-npm-build-toolchain.md)과 [버전 규약](../standards/versions.md)에
따라 private anchor·selector·engine-strict·실제 Node/npm·Node Dockerfile 경로를 검사한다.

- Common private root 도구에는 공식 ini·shell-quote 두 도구 dependency만 승인한다. 기존 lock entry는 모두 deep-equal이며 두 parser node의 정확 버전/SRI를 검증한다. 소비자 graph/version/SRI와 `packages/**`·7개 C11 pack·65개 프론트 버전/정책은 불변이다.
- Common npm ci로 잠긴 공식 INI·shell parser를 준비한 뒤 `npm run test:toolchain`은 인용 key/section·shell 제어문자·physical registry alias 및 경로 이탈/외부 symlink·잘못된 목록·workspace 상속·비정상 이미지·runtime 불일치를 실제 거부한다.
- `npm run check:toolchain`은 정본 runtime에서 실행하고 reusable guard는 기존 `frontends`와 선택 추가 manifest/Dockerfile을 live 축으로 대조한다.
- 소비자 실제 설치·build·원2리뷰·CI는 앱별 증거로 수용한다. 미실행은 NOT_RUN이며 이 후보만으로 native 실기기/EAS/스토어·T-218을 완료하지 않는다.
- CI 순서/needs/fail-fast 감사·최적화는 마지막 별도 단계이며 이 후속은 기존 step 상대 순서를 유지한다.

## 검증 명령

npm run lint, npm run build, npm run check, npm test, npm run doctor, npm run check:examples --workspace packages/ui, npm run check:policy, tools/check_spdx.py, tools/validate_plan.py 및 소비자별 빌드·브라우저 검증을 실행한다.

## Evidence

2026-11-12 최신: 주 이관 PR과 원본 라이브러리 머지는 완료했다. 현재 운영 수용6개와 Transport의 최신 PR184·185·186, 실제 mergef30/image0ac의 정상9개 수용·Geo형 PC 세로 메뉴·실제 PNG decode2+2·zoom7→8은 [원문 정산](../reviews/adversarial/2026-11-12-consumer-sdk-final.md#최종-운영-수용-6개-정산) 및 [배포 정산](../reviews/adversarial/evidence/2026-11-12-frontend-deployment-receipt.json)을 따른다. 과거184/185 실패와 새5초 피드백/60초 bootstrap 계약을 구분한다. 현재 사실 출판의 원2검토·정확 CI·Common50·Geo 단일 MD 출판을 마감한 뒤 Transport 남은 PR/빌드 체계, 전체 프로젝트 규칙 일관화, 마지막 CI 순서 최적화를 진행한다. T-218은 IN_PROGRESS이며 Map 추가 소스·빌드·이미지·배포는 사용자/Claude 범위, native 실기기/EAS/스토어는 NOT_RUN이다.

이전47a 시점 스냅샷:

2026-11-12 후속: common49와 원본4개, Geo631·Map1496·Weather226·Concierge265·Manager588·Pinvi732·Transport181의 주 이관 PR이 모두 머지됐고 최종 전체 tree를 대조했다. 원 A/B 판정과 input2 SDK BLOCK→input3 FIXED, 실제 Mounts 순서 오탐 수정590의 별도 독립 검토·CI를 [원문 정산](../reviews/adversarial/2026-11-12-consumer-sdk-final.md)에 기록한다. 실제 완료 앱은 Manager·Concierge·Pinvi·Weather·Geo·Transport 6개다. Transport는 공개936/image3262의 단계별13개 수용과 관리자47a/image3f207의 공식 SDK508 단독 교체·단일 정상 세션9개 수용을 완료했다. 실제 PNG36·decode2+2·zoom7→8·7폭/9행·폰트·로그아웃303→보호401과 비선택54 불변을 확인했다. 이전6b75 첫76건 미분류·후속36건 XML 및 모든 source/CI/review snapshot은 [배포 정산](../reviews/adversarial/evidence/2026-11-12-frontend-deployment-receipt.json)의 priorHistory에 보존한다. Map의 추가 빌드·배포는 최신 사용자 지시로 Claude의 별도 작업에 맡긴다. 이미 머지한 Map1496은 되돌리지 않는다. toolchain·build ecosystem·CI_LAST 후속과 이 facts3의 원2검토·정확 CI·출판은 별도이며 T-218을 완료로 변경하지 않는다. 모바일 최종 Expo Doctor20/20·React Doctor0, web531·browser209 PASS/4기존 SKIP·API2259 PASS/9 SKIP와 Android/iOS/WebSSR·강제WASM export를 구분하고 실기기/EAS/스토어 출시는 NOT_RUN이다.

이하 이전 checkpoint:

현재 C11은 원본 Scope2 preferred1752a53·고유1.3.1+kortravel.fix.2·고정1ca0487을 공통 정본/세 lock에 연결했다. source38와 Node22 실제 version/SRI/ESM·CJS, 정책175·빌드·Doctor80파일0을 확인했다. 새 packed/browser·두 리뷰·정확 CI/소비자·merge/배포를 진행한다. C10의 Doctor A-P2-11/B-P1-11은5715e94에서 실제3경고→0으로 수정했고 원 재확인을 받는다. 소비자 A/B 원문과 당시 BLOCK은 보존하며 Geo Button43·Concierge checkbox50·Map CI/variant b102/f55·Manager UI 후보 경로b86을 별도 최종 입력에서 수용한다. 후보10과 Scope1/f97을 최종 성공으로 바꾸지 않는다.

이하 이전 checkpoint:

2026-11-12 후보8 UI101·tokens9·타입·예시·두 production builder·lint·Doctor0·실제 packed browser65를 확인했다. 후보9 source2c1182e는 checker 두 파일만 바꾸며 실행 코드/CSS/metadata117개가 같다. 정책68 및 source97ccc97의 도구379실행(378 PASS/1 SKIP)·정보 유출 발견0을 확인했다. integration-9-review의 단일 bytes는 frontend-artifacts.json에 기록하며 이전 후보와 원 BLOCK·수정 후 판정을 보존한다. 소비자 검증·리뷰·PR·이미지 배포는 진행 중이다. 최종 근거는 Geo 저장소 docs/kor-travel-common-library-review.md에 하나로 기록한다. 미실행 gate는 통과로 간주하지 않는다.

## Rollback과 release 차단

미해결 P0/P1, 공통 산출물 해시 차이, SSR/인증·표 회귀 또는 앱 검증 실패가 있으면 release·배포를 차단한다. 롤백은 각 앱의 이전 vendor·manifest·lock 커밋과 이전 이미지 digest로 복구한다. DB와 운영 비밀은 변경하지 않는다.
