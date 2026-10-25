# C-MAP-01 남은 높이 작업면 후보 검증

## 범위

UI `0.1.0-dev.8` 개발 후보이며 정식 registry/Release 발행이나 운영 배포는 하지 않는다.
공개 계약은 [지도 작업면](../standards/map-controls.md), 구현은
[map-controls](../../packages/ui/src/map-controls.tsx)와
[CSS](../../packages/ui/map-controls.css)다. 소비자 저장소는 수정하지 않았다.

## 작성자 검증

WSL Ubuntu의 본인 전용 `/var/tmp/codex-common-map-workspace-20261025`에서 잠긴 의존성을
설치했다. Node22/npm11.19.1 환경이며, 소스 정본은 격리 feature worktree다.

| 검증 | 결과 |
|---|---|
| UI 타입·빌드·지시문·고지 | PASS |
| UI 단위 | 60 PASS |
| tokens 타입·빌드·단위 | 7 PASS |
| npm pack·실제 tarball 설치 | PASS, 저장소 밖 별도 경로에서 설치 |
| 설치 smoke Next webpack/Turbopack | PASS |
| 문서 링크·plan·SPDX | PASS |
| 값 비공개 전체 secret scan | 1,230개 파일·발견0·오류0(Windows Git 작업면 보조 도구) |
| 문서 도구 unittest | 336 PASS·1 SKIP, skip을 성공에 합산하지 않음 |

위 수치는 작성자 실행 결과이며 두 독립 리뷰나 CI를 대체하지 않는다.
최종 source·산출물 pin과 재실행 결과는 같은 문서의 후속 기록에 추가한다.

## 실제 브라우저

n150 Linux native Chromium과 설치 smoke로 다음 네 조건을 검증했다. WSL 브라우저를
사용하지 않았다. 새 작업면의 route shell은 100dvh 안에서 제목을 제외한 남은 높이를 전달했다.

| viewport | 터치 | stage 시작 y | stage 높이 |
|---|---|---|---|
| 1440×900 | false | 138 | 754 |
| 375×812 | true | 148 | 656 |
| 320×568 | true | 148 | 412 |
| 812×375 | true | 164 | 203 |

네 조건 모두 문서의 이중 스크롤·가로 넘침·페이지 오류0이다. 요약과 상세 비겹침,
짧은 화면의 닫기 접근, coarse44px, 목록 단일 주 스크롤, 상세 본문 스크롤,
키 없음/WebGL 불가/빈 자료/로딩의 높이 불변, 접기·입력값 보존·Escape/보이는 trigger 복귀를
확인했다. PC 입력 폭176px/높이30px이며 coarse에서는 높이44px다.
Workspace 밖 기존 dev.7 상세의 absolute/top80px/bottom96px와 필터 높이30px도 유지됐다.

원시 로그·스크린샷은 본인 QA 디렉터리에 보존한다. 실행 가능한
[브라우저 검사](../../packages/ui/smoke/map-workspace-browser.mjs)와
[설치 fixture](../../packages/ui/smoke/next-app/app/map-workspace/page.tsx)를 함께 제공한다.

## 한계와 다음 게이트

- smoke는 대체 데이터이며 실제 지도 엔진·운영 API를 연결하지 않았다.
- 실제 FuelSummary·오류·갱신 지연 시각이 함께 있는320px 화면에서 모든 필수 내용이
  clip ancestor 안에 보이는지는 Transport 소비자 검증이다. summary 최대35%와 스크롤이
  데이터 의미의 가시성을 보장했다고 주장하지 않는다.
- Firefox/실제 지도 SDK·소비자 앱 build/E2E·CI·두 독립 리뷰는 NOT_RUN(각 소유자가 후속 수행).
- 부모가 높이를 제한하지 않는 임의 문서 흐름은 자동 지원하지 않는다. 공용 측정 hook은 없다.
- 본인 로컬 QA 프로세스 정리는 최종 결과 인계 때 별도로 정산한다.
