<!-- SPDX-License-Identifier: GPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie) -->

# common geo 대시보드 독립 post-fix 적대 리뷰 원본

실행 ID: `review-recovery-common-geo-b2e346e0-20261005T055500-KST`

시작: 2026-10-05 05:55:00 +09:00. 종료: 2026-10-05 05:57:41 +09:00.

저장소: `F:\dev\kor-travel-common-geo-dashboard`.

실제 확인한 base: `589a01ef63ff1ce81960e3d531874b5e4c892995`.

실제 확인한 candidate: `b2e346e05e3b0bc065105414a66a858bbd905428`.

이전 독립 검토 후보: `56935a7e955f2a2ea7794754e60b600efac7de3f`.

판정: **PASS — 독립 소스·패키지 재검토 범위.** B-GEO-P2-01은 직접 공격 회귀로 **CLOSED**이며 새 P0/P1/P2/P3 finding은 없다. 실제 소비자/live gate의 PASS나 전체 merge 완료를 의미하지 않는다.

## 격리·검토 방법

WSL Git으로 base/candidate의 실제 commit을 확인했다. 전체 base→candidate 11파일 변경과 이전 후보→수정 후보의 고정 Git 객체를 검토했다. 이전 후보에서 이미 읽은 동일 객체는 재사용하고 새 두 파일의 delta를 집중 공격했다. 상대 리뷰 원본·결과는 읽지 않았으며 부모의 CI/live 결과를 직접 실행 검증으로 세지 않았다.

source checkout/commit/수정 및 의존성 설치는 수행하지 않았다. 별도 `/tmp/popper-common-geo-b2e346e0-20261005`에 고정 source를 추출하고 기존 mirror의 node_modules만 참조했다. mirror는 변경하지 않았고 임시 테스트·빌드·tarball·packed 소비자 검증물은 모두 별도 디렉터리에 작성했다. Node `v22.22.2`, npm `11.19.1`을 사용했다. 초기 원본 `common-geo-review-recovery.md`는 변경하지 않았다.

## EXECUTED

- root `npm run build`, `npm run check`, UI `npm run check:examples`: **PASS**.
- UI Vitest: 후보 기존 **47 PASS**와 별도 독립 공격 **3 PASS**, 합계 **50 PASS**.
- tokens 공식 `npm test --workspace packages/tokens`: **7 PASS**.
- 수정 후보 UI `npm pack`: **PASS**. 버전 `0.1.0-dev.3`, 배포 24파일, JS/d.ts/CSS 및 GPL 고지가 존재하며 모든 공개 export의 대상 파일을 확인했다. client 지시문은 operations에 유지되고 순수 model에는 없다.
- tarball을 별도 packed 소비자 경로에 풀어 공개 operations/model subpath를 실제 import했다. React 서버 렌더링에서 선택 상세와 실패 원문 escaping을 확인했다. **PASS**. 실제 Next/geo 소비자 빌드를 대신하는 검증은 아니다.

직접 생성한 tarball SHA256: `fea44242327ece7507ace64b227e06ea658782a39f1286d29b1bd8b14915b932`.

## B-GEO-P2-01 disposition — CLOSED

원래 P2는 FAILURE 필터를 선택한 뒤 FAILURE가 사라지는 snapshot으로 갱신하면 select는 ‘전체 상태’로 보이지만 실제 조건은 FAILURE에 남아 실행 목록을 숨기는 결함이었다.

수정 위치: `packages/ui/src/dagster-operations.tsx:122`–`:123`, `:163`. 선택 상태를 option 집합에 함께 유지하고 현재 결과에 없으면 ‘실패 · 현재 0건’으로 표시한다. 내부 필터와 표시의 조건이 일치한다.

독립 공격은 다음 연속 상태를 직접 통과했다.

1. FAILURE snapshot에서 FAILURE를 선택한다.
2. SUCCESS만 있는 snapshot으로 갱신한다. 선택값은 FAILURE, 표시에는 ‘현재 0건’, 검색은 0건이다.
3. 빈 snapshot을 거친 뒤 SUCCESS snapshot으로 복귀한다. 선택 상태와 0건 표시가 일치한다.
4. FAILURE가 다시 나타난 snapshot으로 갱신한다. 0건 표시는 사라지고 FAILURE 한 행만 보인다.
5. 전체 상태를 선택한다. 실제 두 행과 검색 2건을 표시한다.

선택 상태를 조용히 해제하지 않고 명시적으로 보존하는 계약은 타당하며 원래 결함이 재현되지 않았다. 공격 테스트는 `/tmp/popper-common-geo-b2e346e0-20261005/packages/ui/test/popper-postfix-probe.test.tsx`에만 작성했다.

## 추가 공격 결과

- `dagster-operations.tsx:186`의 센서 미제공 상태가 ‘미확인’이고 확인된 빈 배열은 0개로 구별되는지 undefined→[]→undefined 갱신으로 직접 확인했다.
- 제어 중인 selectedRunId가 최근 목록 밖이면 상세 callback에 null을 전달하고, 클릭은 onSelectRun에 요청만 전달하며 제어 ID가 갱신되기 전까지 부모 선택을 따르는지 직접 확인했다. 선택 실행이 이후 snapshot에서 사라져도 callback은 null이다.
- 기본 props·기존 data-slot·주기·장시간 실행 상한·재시도 callback·repository별 동명 스케줄 분리의 기존 회귀가 유지된다. 상태 필터 수정은 기본 구성에도 적용된다.
- 50행 DOM 제한과 전체 snapshot 검색·집계의 구분, 서버 응답 상한·polling 취소의 소비자 책임이 문서와 일치한다. RSS 또는 snapshot 메모리 자체의 50건 상한을 주장하지 않는다.
- React text escaping, 마지막 snapshot의 조회 실패 경고, schedule/sensor tick 표시 및 소비자 권한·상세 조회의 경계에 새 회귀를 발견하지 않았다.
- GPL/SPDX/Origin, 공개 subpath와 패키지/lock 버전이 유지된다. Python/Dagster runtime 변경은 이 delta에 없다.

## NOT_RUN 및 판정 한계

실제 geo/weather/transport 소비자 빌드·배포·live 브라우저 E2E, 실제 Dagster 장애/취소/복구, 전체 Python 회귀, clean install, 브라우저/RSS 측정은 이 리뷰에서 수행하지 않았다. 부모의 소비자/live 검증은 진행 중으로 취급하며 이 보고서의 PASS에 합산하지 않는다.

최종 결과: **B-GEO-P2-01 CLOSED, 새 finding 없음, 독립 재검토 PASS.** 소비자 및 live gate는 별도로 완료해야 한다.
