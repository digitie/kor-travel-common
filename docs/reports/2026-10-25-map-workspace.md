# C-MAP-01 남은 높이 작업면 후보 검증

## 범위

UI `0.1.0-dev.8` 개발 후보이며 정식 registry/Release 발행이나 운영 배포는 하지 않는다.
공개 계약은 [지도 작업면](../standards/map-controls.md), 구현은
[map-controls](../../packages/ui/src/map-controls.tsx)와
[CSS](../../packages/ui/map-controls.css)다. 소비자 저장소는 수정하지 않았다.

## 작성자 검증

WSL Ubuntu의 본인 전용 `/var/tmp/codex-common-map-workspace-20261025`에서 잠긴 의존성을
설치했다. Node22.22.2/npm11.19.1 환경이며, 소스 정본은 격리 feature worktree다.

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


## 고정 산출물과 최종 정산

- 제품 소스: `96103d95c64f59bf35fb8979cb573137a43636cc`.
- 후보: `/var/tmp/codex-common-map-workspace-20261025/test-results/ui-pack/kor-travel-ui-0.1.0-dev.8.tgz`.
- SHA256: `e36bae790e3fc7910cd083d446d65f346744bd444974aacc5d3697c12a2e44c7`.
- 독립 설치: `/var/tmp/codex-common-map-workspace-install-20261025` 아래 설치 smoke.
- 최종 pack의 CSS·emitted JS·버전·고지가 제품 소스/빌드와 일치함을 직접 비교했다.
  source의 문서 후속 정산은 제품 트리를 바꾸지 않으며 재pack하지 않는다.
- 최종 CSS(요약 shrink0·새 stage 외곽 frame 포함)로 독립 설치·webpack/Turbopack·
  native Chromium 네 조건을 다시 통과했다. 위 표의 stage 수치는 최종 결과와 같다.
- 본인 QA preview·SSH reverse forward 종료, native runner 잔존0을 확인했다.
  다른 앱 preview·공유 브라우저·운영 프로세스는 변경하지 않았다. 로그/스크린샷은 보존했다.

초기 단위 실행은 jsdom에 `matchMedia` 모의 구현이 없어 새 필터 테스트2개가 실패했다.
테스트 모의를 보완한 뒤60개가 통과했다. QA mirror 전체 SPDX 검사는 저장소 밖 검증 helper의
헤더 누락2개를 검출했으며, 실제 소스 정본140개 파일의 SPDX 오류0으로 범위를 구분했다.
이 과정을 제품 실패나 검증 성공으로 바꾸어 집계하지 않는다.


## v2 — 실제 소비자 clipping 후속

앞선 source96103d9·문서a4d28dd·해시e36bae의 단독 짧은 안내 smoke는 통과했지만,
Transport 소비자의 실제 오류3줄+유가 통계를 넣자320×568/stage y221·h339에서
요약35%가98.34px로 제한돼 평균/최저 가격(y346–404)이 전부 가렸다. 이 후보는
소비자 수용 기준으로 superseded이며 원 tarball과 실패 이미지는 보존한다.

35% 제한을 제거하고 자연 높이 우선으로 바꿨다. 상세를 열 때는 닫기/접기 header의 최소
공간을 남기며, 긴 header 자체를 스크롤하고 동작 버튼을 상단에 고정한다. header의
필수 시각/상태가 항상 최초에 보인다고 보장하지 않으므로 소비자는 우선순위를 배치해야 한다.
새 public prop·측정 hook은 없다. 짧은 높이480px 이하도 필터를 기본 접고, 긴 조건 label은
접힌 상태에서 줄임·펼친 상태에서 전체 줄바꿈으로 처리한다.

고정 문구 재현 fixture의 clip ancestor 전체를 검사한 CSS 초안 결과:

| viewport / 글자 | stage | 상세 | 오류/가격/지연시각 전체 표시 | 닫기·접기 |
|---|---|---|---|---|
| 320×568 / 100% | y221·h339 | 없음/있음 | 모두 표시, 요약 자연 높이206px | 44px 접근 가능 |
| 812×375 / 100% | h203 | 없음 | 모두 표시 | 해당 없음 |
| 812×375 / 100% | h203 | 있음 | 가격/지연시각 가림, NOT_PASS | 44px 접근 가능 |
| 320×568 / 200% | h175 | 없음/있음 | 공간 부족, NOT_PASS | 상세가 있으면44px 접근 가능 |

첫 소비자 재현의 가림과 달리 뒤 두 조건은 전체 필수 내용+상세 동작이 물리적으로 맞지 않는
경우다. 스크롤할 수 있다는 사실만으로 최초 가시성 PASS로 세지 않는다. 소비자 compact화나
명시적 지도 확장의 판단이 필요하며, 이 미해결 한계를 두 독립 리뷰와 root에 전달한다.
[재현 fixture](../../packages/ui/smoke/next-app/app/map-workspace/content/page.tsx)와
[clip 검사](../../packages/ui/smoke/map-workspace-content-browser.mjs)를 함께 보존한다.

v2 최종 source·별도 tarball 경로/해시·정적 설치 결과는 후속 정산에서 고정한다.


### v2 정적 설치와 pin

- 후보: `/var/tmp/codex-common-map-workspace-20261025/test-results/ui-pack-v2/kor-travel-ui-0.1.0-dev.8.tgz`.
- SHA256: `143273f4d435b98f7b5355f33883332bd1873835d70cabce5fc819b45e17f710`.
- v1은 원래 `ui-pack` 경로에 e36bae 해시 그대로 보존했다. 정식 릴리스 번호는 발행하지 않았다.
- 최종 정적 설치 후 WSL 타입·UI61·tokens7·별도 설치·webpack/Turbopack PASS.
- n150 native Chromium 일반4조건과320/200% 긴 필터 label 접근을 통과했다.
  짧은 가로 화면의 stage는 y148/h219로 늘었다. 기존 dev.7 기본 스타일 검증도 유지됐다.
- 정적 재현조합6조건은 위 CSS 초안 표와 같은 FULL3/LIMITED_NOT_PASS3 결과다.
  스크립트의 exit0은 검사가 실행됐음을 뜻하며 제한3조건을 PASS로 바꾸지 않는다.
- 최종 문서 링크·SPDX142파일·전체 비밀 검사1,232파일 오류/발견0·diff check를 확인했다.
- 정확 제품 소스는 이 변경의 feature commit으로 고정하며 뒤 기록은 제품 바이트를 바꾸지 않는다.

### 깨끗한 소스에서 재현한 정본 산출물

- 제품 소스는 `ec0f88743331370026aef9c15864ad2f4ee84566`이다. 이 commit의 `git archive`에서
  잠긴 의존성을 새로 설치하고 Docker에서 타입·UI61·tokens7·고지/빌드를 통과했다.
  검증 중 외부 네트워크는 차단했고 운영 이미지 빌드나 배포는 하지 않았다.
- 정본 후보는 `/tmp/codex-map-common-qa.dM0roR/test-results/ui-pack/kor-travel-ui-0.1.0-dev.8.tgz`,
  SHA256은 `7504bd10261a4983ceb53f704b6a8a1c1a7f751d7595e5bdbfb7bff58a54c0aa`이다.
- 앞선 v2의 `143273…`과 27개 파일의 내용이 모두 같다. Windows 복제에서 생긴 원본 파일7개의
  실행 권한0755를 Git 정본0644로 보존하면서 압축 파일의 해시가 달라졌다. 이전 해시를 예상한
  첫 재pack 비교는 실패했고, 파일별 내용·권한을 대조해 그 원인을 확인했다. 제품 테스트 실패로
  합산하거나 압축 파일이 같다고 보고하지 않는다. 두 후보는 원래 경로에 각각 보존한다.
- 소비자는 정본 `7504bd…`를 vendor/lock에 고정한다. 앞선 v2의 내용 검증 증거는 위 동등성
  비교를 근거로 유지하며, 실제 앱의 최종 통합 검증과 두 독립 리뷰/CI는 별도 정산한다.
