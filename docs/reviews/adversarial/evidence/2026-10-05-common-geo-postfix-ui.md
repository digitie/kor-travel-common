<!-- SPDX-FileCopyrightText: 2026 digitie -->
<!-- SPDX-License-Identifier: GPL-3.0-or-later -->

# Common geo 대시보드 — UI 독립 post-fix 리뷰 원본

- 실행 ID: `A-COMMON-GEO-UI-POSTFIX-20261005-b2e346e`.
- 관찰: `2026-10-04 20:57:31~20:59:03 UTC` / `2026-10-05 05:57:31~05:59:03 KST`.
- 요청 저장소: `F:/dev/kor-travel-common-geo-dashboard`.
- 실제 base: `589a01ef63ff1ce81960e3d531874b5e4c892995`.
- 초기 후보: `56935a7e955f2a2ea7794754e60b600efac7de3f`.
- 실제 post-fix candidate: `b2e346e05e3b0bc065105414a66a858bbd905428`.
- Windows worktree의 WSL 포인터 문제로 공유 object 저장소 `F:/dev/kor-travel-common`에서 rev-parse/show/diff했다. 고정 commit만 읽었다. checkout·제품 source·mirror·설치·DB는 변경하지 않았다. 상대 리뷰 결과는 읽지 않았다.
- 초기 전체 11파일 검토에 이어 같은 base 대비 공개 API·표시 계약·CSS·채택 가이드·버전/lock을 재확인했다. 초기→수정 delta는 component와 해당 테스트 2파일, 23줄 추가·3줄 삭제다. 초기 원본은 수정하지 않았다.

## 판정

**PASS — 본 독립 소스·DOM 리뷰 범위. A-P1-01과 A-P2-01은 수정 확인으로 CLOSED이며 새 P0/P1/P2/P3 finding은 없다.**

실제 geo tarball 소비·build·live UI 검증은 별도 진행 중으로 전달됐다. 본 판정은 그 gate 완료 또는 PR 머지 승인을 뜻하지 않으며 완료로 집계하지 않는다.

## 이전 finding disposition

### A-P1-01 / P1 — CLOSED

- 위치: `packages/ui/src/dagster-operations.tsx:122-123`, `:163`.
- 수정: 현재 선택 상태를 option 목록에 유지하고 새 snapshot에 해당 상태가 없으면 `실패 · 현재 0건`으로 표시한다.
- 독립 실행: FAILURE/SUCCESS snapshot에서 FAILURE 선택→SUCCESS 1건 snapshot으로 rerender했다. select value는 FAILURE, option 표시는 실패 · 현재 0건, 결과는 명시적인 필터에 따라 0건이었다. 전체 상태 선택 후 SUCCESS 1행이 표시됐다. 빈 snapshot→두 실행 복원에서도 전체 상태와 2행이 일치했다.
- 초기의 “전체 상태로 보이지만 실제 FAILURE 적용” 모순은 재현되지 않는다. 고정 후보의 refresh 회귀 테스트도 같은 실패 조건을 검증한다. 초기 severity P1을 유지한 채 수정으로 닫는다.

### A-P2-01 / P2 — CLOSED

- 위치: `packages/ui/src/dagster-operations.tsx:186`.
- 수정: sensors 속성 미제공은 `센서 미확인`, 명시적 배열은 실제 길이를 표시한다.
- 독립 실행: 속성 없음→센서 미확인, 빈 배열→센서 0, 1개 배열→센서 1을 assertion으로 확인했다. 미제공 경우 센서 0 문자열이 없었다.
- 고정 후보에 미제공 회귀가 추가됐다. 초기 severity P2를 유지한 채 수정으로 닫는다.

## EXECUTED

고정 Git component/model을 기존 `/tmp/common-geo-dashboard-source`의 Node 의존성으로 메모리 transpile하고 React/jsdom/user-event assertion을 실행했다. 구현과 dist는 mirror에서 읽거나 빌드하지 않았다. 독립 probe 3건 모두 exit 0이다.

- 두 finding 수정, 필터 해제·빈 snapshot·복원, 미제공/빈/1개 센서 구분: PASS.
- 120건 50/50/20 페이지 탐색, FAILURE 필터 1건, 선택 콜백·상세, 검색 빈 결과: PASS.
- 실패 문자열의 text escaping, 마지막 성공 snapshot 오류 경고, schedule/sensor 실패 tick·시간대·null 상태의 확인 불가 표시: PASS.
- 제어된 목록 밖 ID의 상세 콜백 null, 선택 콜백 후 소비자가 ID를 갱신하기 전 제어 선택 유지, 명시적 null 해제: PASS.
- 같은 이름의 스케줄이 두 location에 있을 때 펼침 identity와 URL callback의 repository scope 보존: PASS.
- snapshot null의 요약은 0이 아닌 — 표시, loading 중 refresh/retry 비활성화·aria-busy: PASS.
- axe-core DOM 검사 위반 0개. color contrast는 비활성화했으며 PASS로 세지 않았다.

## READ_ONLY·NOT_RUN·남은 검증

- CSS는 공용 root로 scope되고 640/1100px 반응형 규칙, 기존 props 기본값·data-slot·선택형 metadata, 50행 Breaking/Migration 안내와 dev.3/lock의 일치를 읽었다. app 인증·URL·외부 작업 권한은 소비자 소유라는 가이드와 구현의 콜백 경계를 확인했다.
- npm 47건·build/check/examples PASS는 부모의 전달 결과다. 직접 전체 suite나 production build를 실행했다고 주장하지 않는다.
- 실제 geo 채택·tarball build·live UI·브라우저 keyboard·viewport 실측·색 대비는 NOT_RUN. jsdom은 CSS geometry를 검증하지 않는다.
- focus outline clipping, 좁은 화면에서 목록 뒤의 선택 상세 탐색성은 소비자 live에서 확인해야 한다. 현재 증거로 구체적 새 finding을 만들지는 않았다.
- snapshot 전체 검색·집계와 50행 DOM 제한을 구분했다. RSS 개선율이나 서버 응답 상한의 실측은 NOT_RUN.
- 초기 원본 SHA256: `26B978A4F31632668FEF9BD62323D6FBFDFFEBD915FF6D7232534F3EE417647E`. 본 원본 SHA256은 파일 생성 후 별도로 전달한다.
