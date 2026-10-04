<!-- SPDX-FileCopyrightText: 2026 digitie -->
<!-- SPDX-License-Identifier: GPL-3.0-or-later -->

# Common geo 대시보드 — UI 독립 적대 리뷰 원본

- 실행 ID: `A-COMMON-GEO-UI-20261005-56935a7e`.
- 관찰: `2026-10-04 20:46:24~20:53:21 UTC` / `2026-10-05 05:46:24~05:53:21 KST`.
- 요청 저장소: `F:/dev/kor-travel-common-geo-dashboard`.
- 실제 base: `589a01ef63ff1ce81960e3d531874b5e4c892995`.
- 실제 candidate: `56935a7e955f2a2ea7794754e60b600efac7de3f`.
- Windows Git에서 WSL 형식 worktree 포인터를 열지 못해 공유 object 저장소 `F:/dev/kor-travel-common`의 같은 고정 commit을 show/diff했다. checkout·포인터·소스·mirror·설치를 변경하지 않았다. 검증 mirror의 Node 의존성만 읽고, 고정 source를 메모리에서 transpile했다.
- 전체 11파일 manifest와 제품 source/tests/CSS/API·채택 가이드·task·CHANGELOG를 검토했다. geo 비교는 `3f4ddc2dac3f31634a23ef0e9592f419e29e7d14`의 DagsterPanel.tsx 고정 원본을 읽었다. 상대 리뷰 결과는 참조하지 않았다.

## 판정

**FAIL(BLOCK). A-P1-01을 수정하거나 증거로 기각하고 독립 재확인해야 한다. A-P2-01도 수정하거나 owner/task/gate/시점을 명시해 disposition해야 한다.**

실제 geo 소비자·live UI 검증은 진행 중으로 전달됐으며 본 리뷰에서 PASS로 집계하지 않았다.

## Findings

### A-P1-01 — snapshot 갱신 뒤 화면의 전체 상태 필터와 실제 적용 조건이 달라진다

- 위치: `packages/ui/src/dagster-operations.tsx:117-122`, `:162`.
- 실패 조건: FAILURE/SUCCESS가 함께 있는 snapshot에서 FAILURE 필터를 선택한다. 새 snapshot이 SUCCESS 실행만 포함하면 상태 option 목록에서 FAILURE가 사라지지만 내부 필터 state는 FAILURE를 유지한다.
- 독립 재현: 고정 component/model을 React/jsdom에 렌더링하고 user-event로 FAILURE를 선택했다. SUCCESS 1건으로 rerender한 결과 select DOM value는 빈 문자열, 선택 option은 `전체 상태`인데 실제 행은 0개이고 `검색 조건에 맞는 실행이 없습니다.`가 표시됐다. 외부 API나 비정상 DTO가 필요 없는 정상적인 갱신 조건이다.
- 영향: 사용자는 전체 상태를 보고 있다고 판단하지만 전달된 정상 실행이 모두 숨겨진다. 데이터 조회 결과와 적용 조건의 표시 계약을 깨뜨린다.
- 최소 수정: 현재 선택 상태를 option에 보존해 실제 조건을 표시하거나, 새 snapshot에서 사라진 상태를 명시적으로 전체 상태로 재설정해 표시와 필터를 일치시킨다. 필터 선택→해당 상태 없는 snapshot 갱신 회귀를 추가한다.
- disposition 필요조건: 두 상태가 일치하고 SUCCESS 행 또는 명시적인 FAILURE 필터가 보이는 고정 후보 재현·회귀 결과.

### A-P2-01 — 미제공 센서 목록을 확인된 0건으로 표시한다

- 위치: `packages/ui/src/dagster-operations.tsx:185`.
- 실패 조건: 공개 타입에서 선택 필드인 `repository.sensors`를 제공하지 않고 `showRepositories`를 켠다.
- 독립 재현: 정규 snapshot의 repository에 sensors 속성 없이 렌더링하면 `코드 위치 ... 작업 0 · 자산 0 · 스케줄 0 · 센서 0`이 출력됐다.
- 영향: 센서를 조회하지 않은 소비자에서도 확인된 센서 0건처럼 보인다. 선택 metadata는 API가 확인한 값만 넘기라는 가이드와 미확인 값의 표시 원칙에 맞지 않는다. 실제 geo에 센서가 누락됐다고 주장하는 것은 아니다.
- 최소 수정: sensors 미제공이면 `센서 미확인` 또는 `—`, 명시적 빈 배열이면 0건을 구분한다. 두 경우를 회귀로 검증한다.
- disposition 필요조건: 수정 재검증 또는 P2 연기에 필요한 owner·상세 task·적용 gate·목표 시점.

## 실행한 검증

고정 Git source를 기존 mirror의 TypeScript/React/jsdom 의존성으로 메모리에서 실행했다. mirror의 source/dist를 빌드하거나 변경하지 않았다.

- 두 finding 재현: exit 0, 앞서 기재한 모순을 assertion으로 확인했다.
- 120건의 50/50/20 페이지 탐색, 상태 필터 1건, 실행 선택 콜백·상세, 검색 빈 결과: PASS.
- 실패 원문 `<script>failure</script>`가 text로 표시되고 script DOM이 생성되지 않음: PASS.
- 마지막 snapshot 오류 경고, 스케줄·센서 실패 tick, 시간대, 센서 null 상태의 확인 불가 표시: PASS.
- axe-core DOM 검사: 위반 0개. color contrast 검사는 비활성화했으며 통과로 세지 않았다.
- CSS scope와 640/1100px 전환 규칙, 표 region/tabIndex, 새 공개 타입의 선택 필드·기존 props 기본값과 data-slot 보존, dev.3 버전/lock 및 50행 변경의 Breaking/Migration 기록을 읽었다.

## NOT_RUN·남은 범위

- 실제 geo tarball 채택·build·live UI·브라우저 keyboard/viewport 실측·색 대비: NOT_RUN. root 진행 중 gate를 common DOM 검사로 대신하지 않는다.
- 실제 CSS 레이아웃·focus outline clipping·좁은 화면에서 50행 뒤의 선택 상세 탐색성은 jsdom geometry로 판정하지 못했다. 소비자 live에서 확인해야 한다.
- snapshot 전체는 검색·집계에 보유하고 DOM만 50행으로 제한한다는 설명은 코드와 일치한다. RSS 개선율·서버 응답 상한의 실측을 주장하지 않는다.
- 이 보고서는 초기 불변 후보의 원본이며 후속 수정 결과로 고치지 않는다. SHA256은 별도 전달한다.
