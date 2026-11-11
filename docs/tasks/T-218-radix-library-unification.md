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

## 검증 명령

npm run lint, npm run build, npm run check, npm test, npm run doctor, npm run check:examples --workspace packages/ui, npm run check:policy, tools/check_spdx.py, tools/validate_plan.py 및 소비자별 빌드·브라우저 검증을 실행한다.

## Evidence

현재 C11은 원본 Scope2 preferred1752a53·고유1.3.1+kortravel.fix.2·고정1ca0487을 공통 정본/세 lock에 연결했다. source38와 Node22 실제 version/SRI/ESM·CJS, 정책175·빌드·Doctor80파일0을 확인했다. 새 packed/browser·두 리뷰·정확 CI/소비자·merge/배포를 진행한다. C10의 Doctor A-P2-11/B-P1-11은5715e94에서 실제3경고→0으로 수정했고 원 재확인을 받는다. 소비자 A/B 원문과 당시 BLOCK은 보존하며 Geo Button43·Concierge checkbox50·Map CI/variant b102/f55·Manager UI 후보 경로b86을 별도 최종 입력에서 수용한다. 후보10과 Scope1/f97을 최종 성공으로 바꾸지 않는다.

이하 이전 checkpoint:

2026-11-12 후보8 UI101·tokens9·타입·예시·두 production builder·lint·Doctor0·실제 packed browser65를 확인했다. 후보9 source2c1182e는 checker 두 파일만 바꾸며 실행 코드/CSS/metadata117개가 같다. 정책68 및 source97ccc97의 도구379실행(378 PASS/1 SKIP)·정보 유출 발견0을 확인했다. integration-9-review의 단일 bytes는 frontend-artifacts.json에 기록하며 이전 후보와 원 BLOCK·수정 후 판정을 보존한다. 소비자 검증·리뷰·PR·이미지 배포는 진행 중이다. 최종 근거는 Geo 저장소 docs/kor-travel-common-library-review.md에 하나로 기록한다. 미실행 gate는 통과로 간주하지 않는다.

## Rollback과 release 차단

미해결 P0/P1, 공통 산출물 해시 차이, SSR/인증·표 회귀 또는 앱 검증 실패가 있으면 release·배포를 차단한다. 롤백은 각 앱의 이전 vendor·manifest·lock 커밋과 이전 이미지 digest로 복구한다. DB와 운영 비밀은 변경하지 않는다.
