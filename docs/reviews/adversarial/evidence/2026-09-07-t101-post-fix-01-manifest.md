# T-101 post-fix 리뷰 manifest

- 리뷰 종류: full post-fix, 두 reviewer 독립 실행
- 기준 commit: `4c33a5d951e32df0c2170b7a865f324d122dbe05`
- 기준 tree: `aa81767746cb40641e43397af19082456aaacb3b`
- 수정 delta base: `f8894e293ca9677f457011197052cd55dbdc9696`
- PR 원 base: `cf2c610cecfa7a9b8f7a035c9529d7a296e27527`
- task: [T-101](../../../tasks/T-101-tokens-package.md)
- 범위: `packages/tokens` 공개 CSS·생성기·생성물·시험·`packages` CI와 관련 architecture·standards·T-101/T-102 경로 문서
- 범위 밖: 소비자 저장소 수정·채택, npm/PyPI·GitHub Release·tag 게시, T-103 대비 도구, 소비자 build/e2e

## 리뷰 요청

초기 리뷰에서 BLOCK된 DTCG 자료형·계층, Tailwind v4 z 유틸리티와 v3 easing 키, dark-media 모드, scoped `color-scheme`, profile/media 생성물 동기화, CI drift 선행 검사, light/dark 전수 비교, 순수 CSS hairline, T-102 flat 경로를 새 immutable 기준선에서 독립 재현한다. 양 OS package/build/test/pack/install 및 정적 gate를 기준 commit에 귀속하고 P0–P3 finding과 미실행 gate를 원본 보고서에 남긴다.

## 공통 검증 기준

- Windows와 WSL에서 Python 정적 gate·npm build/check/test·pack/install을 실행한다.
- 공식 DTCG 2025.10 schema와 Tailwind v3/v4·Chromium 계산값을 가능한 범위에서 직접 확인한다.
- 수정·commit·push·publish와 상대 reviewer 결과 열람은 금지한다.
- 보고서에는 시작·종료 SHA/tree·clean 상태·실행 시각·원본 결과 hash를 기록한다.