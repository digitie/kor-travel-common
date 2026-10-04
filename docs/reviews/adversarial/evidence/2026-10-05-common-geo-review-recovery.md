<!-- SPDX-License-Identifier: GPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie) -->

# common geo 대시보드 독립 적대 리뷰 원본

실행 ID: `review-recovery-common-geo-56935a7e-20261005T054609-KST`

시작: 2026-10-05 05:46:09 +09:00. 검토 종료: 2026-10-05 05:53:11 +09:00.

대상 저장소: `F:\dev\kor-travel-common-geo-dashboard`.

실제 확인한 base: `589a01ef63ff1ce81960e3d531874b5e4c892995`.

실제 확인한 candidate: `56935a7e955f2a2ea7794754e60b600efac7de3f`.

판정: **FAIL — B-GEO-P2-01 수정 후 재검토 필요.** P0/P1/P3 발견은 없고 P2 한 건을 직접 재현했다. 기존 테스트의 통과만으로 이 후보를 승인하지 않는다.

## 격리와 검토 범위

두 commit을 WSL Git의 `rev-parse ...^{commit}`으로 확인하고 고정 객체의 `show`/`diff`로 전체 11파일 변경을 읽었다. AGENTS, 관련 작업·채택 가이드와 공개 계약도 확인했다. Windows Git은 WSL worktree의 Linux gitdir 경로 때문에 첫 조회가 실패하여 WSL Git으로 전환했다. checkout, commit, 저장소 소스 수정, 의존성 설치를 수행하지 않았다. 상대 리뷰 원본·판정은 읽지 않았다.

시각 비교는 geo `3f4ddc2dac3f31634a23ef0e9592f419e29e7d14`의 `kor-travel-geo-ui/components/admin/DagsterPanel.tsx`만 읽었다. 실행 복구, 인증, GraphQL, 실패 확인, 백업 다운로드는 common에 옮기지 않고 소비자에 남기는 경계를 확인했다.

고정 Git 객체에서 packages/scripts/패키지 메타데이터만 별도 `/tmp/popper-common-geo-56935a7e-20261005`로 추출했다. 제공된 `/tmp/common-geo-dashboard-source/node_modules`는 임시 디렉터리에서 참조했고 제공 mirror의 소스·생성물은 수정하지 않았다. 빌드 생성물, tarball, 추가 공격 테스트는 모두 별도 임시 디렉터리에만 작성했다. Node `v22.22.2`, npm `11.19.1`을 사용했다.

## EXECUTED

- 별도 고정 스냅샷의 root `npm run build`: PASS. tokens 생성과 UI TypeScript 컴파일, client 지시문·고지 검사가 통과했다.
- root `npm run check` 및 UI `npm run check:examples`: PASS.
- UI `vitest run`: 후보의 기존 테스트 **45 PASS**, 독립 추가 공격 회귀 **1 FAIL**. 실패는 아래 B-GEO-P2-01의 실제 화면 상태 불일치다.
- tokens의 공식 `npm test --workspace packages/tokens`: **7 PASS**. 앞서 tokens에 Vitest를 잘못 적용한 실행은 `No test suite found`로 실패했으며 제품 결함이나 검증 PASS로 세지 않았다.
- UI `npm pack`: PASS. `@kor-travel/ui@0.1.0-dev.3` tarball 24파일에서 공개 subpath의 JS/d.ts, `dagster.css`, LICENSE/NOTICE/THIRD_PARTY_NOTICES 존재를 확인했다. `dagster-operations.js`의 `"use client"`는 유지되고 순수 `dagster-model.js`에는 없다.

## B-GEO-P2-01 — 갱신 뒤 상태 필터가 ‘전체 상태’로 보이면서 사라진 상태를 계속 적용한다

심각도: **P2**, 신규 발견, **OPEN**.

위치: `packages/ui/src/dagster-operations.tsx:111`, `:117`–`:122`, `:162`.

실패 시나리오: 정상 polling/새로고침으로 최근 실행의 상태 구성은 바뀐다. 최초 snapshot에 FAILURE가 있어 사용자가 FAILURE를 선택한 뒤, 다음 snapshot에 SUCCESS만 있으면 `statuses`에서 FAILURE option이 제거된다. React state `status`는 FAILURE를 유지한다. 브라우저 select는 존재하는 첫 option인 ‘전체 상태’를 표시하지만 실제 `filteredRuns`는 여전히 FAILURE만 검색한다. 빈 결과를 보여 주며 새 실행을 숨긴다. 이 동작은 `showRunDetails`의 기본값에서도 발생하므로 weather/transport가 기존 props로 채택하는 경우에도 영향을 받는다.

직접 재현:

1. FAILURE run 한 건의 snapshot으로 렌더링한다.
2. `userEvent.selectOptions(screen.getByLabelText("상태 필터"), "FAILURE")`를 실행한다.
3. 동일 컴포넌트를 SUCCESS run 한 건만 포함하는 새 snapshot으로 rerender한다.
4. ‘전체 상태’ 선택과 표 1행의 일치를 검증한다.

실제 관측값:

```json
{"value":"","shown":"전체 상태","summary":"조회 1건 · 검색 0건 · 1/1 페이지","tableRows":0,"empty":"검색 조건에 맞는 실행이 없습니다."}
```

별도 공격 테스트의 표 1행 기대는 실제 0행으로 실패했다. 같은 실행에서 후보 기존 UI 45개 테스트는 통과했다. 재현 테스트 경로는 `/tmp/popper-common-geo-56935a7e-20261005/packages/ui/test/popper-probe.test.tsx`이며 원 저장소에는 추가하지 않았다.

영향: 조회 자체는 성공하고 요약에는 최근 성공이 있지만 목록은 빈 검색 결과가 된다. 필터가 화면상 이미 ‘전체 상태’여서 사용자가 현재 적용 중인 숨은 FAILURE 조건을 알 수 없고, 일반 새로고침으로도 state가 해제되지 않는다. 실행과 복구 결과 확인을 방해하는 공개 UI 계약 결함이다.

필요한 disposition: 선택 중인 상태가 현재 목록에 없어도 해당 option을 명시적으로 유지하여 ‘실패, 결과 0건’으로 보여 주거나, 옵션 유효성과 필터 조건을 함께 전체 상태로 정규화한다. 표시만 변경해서는 안 된다. polling 중 상태가 사라졌다 다시 나타나는 경우, 빈 snapshot을 거치는 경우까지 선택 표시와 실제 조건이 일치하는 회귀 검증이 필요하다. 수정 candidate에서 독립 공격 회귀가 통과해야 CLOSED로 변경할 수 있다.

## 다른 공격 관점의 결과

- 공개 계약: 기존 props 기본값, table `data-slot`, callback으로 주입하는 URL/label/refresh, repository별 schedule identity를 보존한다. 50행 pagination은 기존 전행 DOM 계약을 바꾸므로 CHANGELOG의 Breaking/Migration 및 채택 가이드에 명시한 것이 적절하다.
- 실패 상태: 실패 원문은 React text로 렌더링하고 HTML로 실행하지 않는다. 조회 실패와 마지막 snapshot이 함께 있으면 이전 결과임을 경고한다. schedule/sensor의 중지와 확인 불가를 구분하며 실패 tick을 표시한다. tick 정보의 조회·정확성·인증 실패 처리는 소비자 API 책임이라는 가이드와 일치한다.
- 메모리: 실행 행의 DOM은 페이지당 50개지만 검색·집계는 전체 배열을 계속 사용한다. 응답 상한과 polling 취소를 서버/소비자가 적용해야 한다는 문서가 이 한계를 명시한다. 이 후보만으로 전체 snapshot 메모리 또는 RSS 상한이 보장된다고 판정하지 않는다.
- 서버/클라이언트: 선택·검색 state는 client 컴포넌트 안에 있고 모델 subpath에는 React/인증/provider 의존성이 추가되지 않았다. 상세 callback의 앱 전용 작업·권한과 데이터 조회는 소비자에 남는다.
- 라이선스·패키징: 기존 weather Origin, GPL/SPDX, 저작권과 수정일을 보존했다. geo UI의 구체적 API·실패 확인·백업 로직을 복사한 변경은 관측하지 않았다. package.json/lock의 dev.3 버전은 일치하고 패키지 자산 및 지시문 검사도 직접 통과했다.
- 기존 소비자: 기본 props/주기 표시/장시간 실행 상한/조회 오류 재시도/동명 스케줄 분리의 기존 테스트가 통과했다. 상태 필터의 갱신 문제는 그 테스트가 다루지 못한 신규 회귀다. Python/Dagster runtime 변경은 이번 11파일 delta에 없다.

## NOT_RUN 및 판정 한계

실제 geo/weather/transport 소비자 빌드·배포·live 브라우저 E2E, 실제 Dagster 장애·취소·복구, 전체 Python 회귀, clean dependency install, 실측 브라우저/RSS 메모리 측정은 이 독립 리뷰에서 실행하지 않았다. 부모가 진행 중인 소비자/live 검증이나 CI 결과를 나의 직접 실행 PASS로 세지 않았다. jsdom 재현은 실제 브라우저 live 검증을 대신하지 않는다.

최종 disposition은 **P2 한 건 OPEN, FAIL**이다. 필터 표시/조건 불일치를 수정한 고정 후보의 재검토와 별도의 소비자/live gate 완료가 필요하다.
