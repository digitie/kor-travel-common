# VirtualTable의 좁은 grid 가로 스크롤 회귀

- 기준선: Common main `55e3e95c9362b64bbeaddf8abaac0247f0a0df6f`.
- 변경: 공통 VirtualTable 루트에 `min-w-0`만 추가한다. 공개 props·슬롯·정렬·가상화 기본값은 유지한다.
- 현재 준비 버전: UI `0.2.2`, tokens `0.1.3`, toast `0.1.2`. 소비자 수정·이미지 빌드·배포는 포함하지 않는다.

## 실제 재현과 가설 검증

375px에서 documentElement.scrollWidth는 375였지만 body/main은 861이었다. 327px 패널 안의 293px grid에서 공통 루트가 820px로 확장되고 내부 overflow:auto 컨테이너도 clientWidth/scrollWidth 820/820이라 scrollLeft가 0에 머물렀다. 처음부터 375px로 연 경우와 desktop에서 바꾼 경우 모두 두 animation frame 후 재현했다. viewport PNG는 375px, full-page PNG는 861px였다.

QA에서 공통 루트의 minWidth만 일시적으로 0으로 설정하면 body/main 375, 컨테이너 293/820, scrollLeft 240과 실제 표 이동이 확인됐다. 스타일 원복 후 body 861로 돌아왔고 로그아웃 200·browser close를 확인했다. 이 DOM 실험을 제품 수정·배포 성공으로 집계하지 않는다.

## 제품 회귀 시험

`packages/ui/smoke/virtual-table-browser.spec.ts`는 실제 공통 표를 375/1280px, semantic/virtualized 네 조합으로 검사한다. 바깥 minmax(0,1fr) grid와 내부 grid에서 body/main 폭, 실제 수평 이동, desktop 표 채움, 폼 검색, sticky header, 가상 행 수와 pageerror를 검사한다.

- 수정 전: 모바일 두 경우가 body 폭 689/924로 같은 단언에서 실패하고 desktop 두 경우는 통과했다.
- 수정 후: 네 경우 모두 통과했다. min-width:0만으로 충분하여 width:100%는 추가하지 않았다.
- 캐시된 Node 26.13.1/npm 12.0.1·기존 의존성을 재사용했다. Vite Linux binding 누락에 따른 첫 서버 시작 실패는 RED로 세지 않았다. 실제 RED/GREEN은 기존 webpack·Playwright로 같은 fixture를 묶어 Chromium에서 실행했다.
- canonical Next 설치 스모크의 Playwright 목록에 같은 시험을 연결했다. CI 설치본 webpack/Turbopack·전체 단위 검증과 독립 리뷰는 PR에서 별도 확인한다.

## pack과 후속 채택

첫 head 05eba117의 정규 UI build/pack과 타입 선언·고지를 검사했다. 당시 로컬 UI 0.2.2 SHA256은 `81362f9e71e231a4b89af25fcb819fc2327235c86b7445cab5fbf8b2739756a9`다. 당시 정규 tokens 0.1.2 pack의 SHA256은 `c6e2e27d716d5db7c9157f412cfd28d941536c032ce702a8cceb32f2a0c16253`이며 기존 수용 tarball과 전체 bytes가 동일했다.

로컬 pack은 canonical release artifact가 아니다. 병합 후 부모가 `common-release-packs-<merge-sha>`의 SOURCE_SHA·SHA256SUMS·SRI를 대조하고 Geo·Weather·Transport 공개/관리 네 표면에 같은 UI tarball/version/dist를 공급한다. 기존 공개 tarball bytes와 artifact catalog는 보존하고 새 버전의 배포물을 생성한다. 카탈로그 동결과 소비자 채택은 부모가 소유한다. T-025 정책 분리·Map·N150·SDK 변경은 범위 밖이다.

## PR 직전 로컬 gate 한계

- policy 생성물 대조·UI 타입 검사·문서 링크·diff 공백 검사는 통과했다.
- lint는 재사용 의존성에 @eslint/js가 없어 실행 환경 오류로 실패했다. 통과로 집계하지 않으며 PR CI가 정본이다.
- plan 검사는 기준선부터 T-416/T-419 요약 제목과 T-419의 T-025 선행 상태 오류 3건이 있다. 해당 task·원장·검사기는 이 PR에서 변경하지 않았다.
- tools unittest 실행은 405건 중 failures 38/errors 3/skipped 1이었다. 재사용 환경의 MDX parser 등 누락 오류를 포함한다. 제품 회귀 4건의 성공과 합산하지 않는다. 별도 정책·Python 작업으로 확장하거나 이 결과를 전체 green으로 표시하지 않는다.
- 독립 리뷰 두 건과 canonical CI/merge artifact는 부모 통합에서 확인한다.

## 정확 CI 실패에 따른 최소 릴리스 동기화

head 05eba117의 common frontend 44301094514에서 기존 toast.test.mjs의 정확 축 단언이 UI metadata 0.2.2와 versions.json의 0.2.1 차이로 실패했다. 같은 기존 시험으로 로컬 1 FAIL/2 PASS를 재현했다. 단언과 guard는 수정하지 않았다.

versions.json의 UI 0.2.2·tokens 0.1.3·toast 0.1.2와 package metadata·UI tokens peer·lock을 맞췄다. sync_frontend_policy.mjs가 정본과 규약 표를 생성하고 각 sync-policy.mjs가 UI/tokens 내장 사본을 갱신하며 Toast 사본도 같은 정본 bytes로 동기화한다. 이 결합으로 tokens/toast의 policy bytes까지 바뀌므로 기존 버전 재포장 대신 patch를 올린다. T-025 정책 분리 설계나 검사 조건은 변경하지 않는다.

기존 metadata·dependency-policy·native CSS guard 238건은 모두 PASS/skip 0이다. tokens 0.1.3과 toast 0.1.2의 tar 엔트리를 이전 공개 버전과 대조하면 package.json과 dependency-policy.json만 다르고 runtime/CSS·파일 집합은 동일하다. 이전 자산은 교체하지 않으며 신규 canonical artifact와 catalog 동결은 부모 통합에서 대조한다.
