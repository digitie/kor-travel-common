<!-- SPDX-FileCopyrightText: 2026 digitie -->
<!-- SPDX-License-Identifier: GPL-3.0-or-later -->

# Common geo 최종 표시 수정 — UI 독립 리뷰 원본

- 실행 ID: `A-COMMON-GEO-UI-FINAL-POSTFIX-20261005-426de4f`.
- 관찰: `2026-10-04 21:07:17~21:07:58 UTC` / `2026-10-05 06:07:17~06:07:58 KST`.
- 전체 base: `589a01ef63ff1ce81960e3d531874b5e4c892995`.
- delta base: `27b4e31e149ddb4f98ce0bd43429c553a09adc00`.
- 실제 후보: `426de4fbad35282bb558712d922c06268e9aba62`.
- 요청 저장소: `F:/dev/kor-travel-common-geo-dashboard`. Windows에서는 공유 object 저장소 `F:/dev/kor-travel-common`의 같은 고정 객체를 rev-parse/show/diff했다.
- 격리: 기존 전체 manifest 맥락에서 4파일 9줄 추가·2줄 삭제를 독립 검토했다. peer 결과는 읽지 않았다. 구현·checkout·commit·설치·mirror·DB를 변경하지 않았다. 이전 원본 보고서는 유지했다.

## 판정

**PASS — 본 독립 소스·DOM·타입 이관 리뷰 범위. A-P2-02와 A-P2-03은 CLOSED이며 새로운 finding은 없다.**

실제 geo 소비자·production build·live gate는 별도 진행 중이다. 본 판정에서 완료로 집계하지 않는다.

## Finding disposition

- **A-P2-02 / P2 — CLOSED.** `packages/ui/src/dagster-operations.tsx:79`의 null job 행이 `스케줄 · hourly-schedule (작업 미확인)`으로 표시됐다. 접힌 버튼의 접근 가능한 이름을 assertion으로 확인했다. schedule 이름을 jobLabel에 넘기지 않는 것도 확인했다. 펼친 실제 job은 미확인이고 스케줄 링크는 원래 schedule 이름과 repository를 사용한다. 실제 job이 제공되면 기존 작업 label과 상세가 유지된다.
- **A-P2-03 / P2 — CLOSED.** CHANGELOG Breaking에 `DagsterSchedule.jobName: string | null`을 기록하고 Migration에 null 확인과 API 미제공 처리, 스케줄을 jobLabel에 전달하지 않는 표시 계약을 추가했다. 가이드에도 `jobName !== null`과 공용 `DagsterRepository` 콜백 타입을 안내한다. 동일 전/후 고정 model을 메모리 TypeScript host에서 검사할 때 이 null guard를 적용한 소비자는 양쪽 모두 semantic diagnostics 0개였다. 실제 공개 타입이 nullable이라는 사실은 유지되며 이관 안내가 누락됐던 finding을 수정으로 닫는다.
- **A-P1-01 / P1 및 A-P2-01 / P2 — CLOSED 유지.** 같은 refresh 필터 공격과 미제공/명시적 빈/1개 센서 assertion을 최신 후보에서 다시 통과했다. 초기 severity는 변경하지 않는다.

## EXECUTED

고정 component/model을 기존 mirror 의존성으로 메모리 transpile했다. mirror 구현이나 dist를 빌드·수정하지 않았다. 독립 실행 4건 모두 exit 0이다.

- null job의 접힌 이름·상세·jobLabel 입력·스케줄 URL/repository scope·알려진 job 갱신: PASS.
- 초기 두 finding 수정 유지, 빈 snapshot/복원, 센서 미확인·0·1 구분: PASS.
- 120건 pagination 50/50/20, FAILURE 필터·선택·상세·검색, text escaping·마지막 snapshot 경고·tick·시간대: PASS.
- axe-core DOM 위반 0개. color contrast는 비활성화했으며 PASS로 세지 않았다.
- 문서에 제시한 null guard의 TypeScript 전/후 consumer 진단 0개: PASS.

## NOT_RUN

- 전체 UI48·build/type/examples PASS는 부모 전달 결과이며 본인이 직접 전체 suite를 실행한 결과가 아니다.
- 실제 geo tarball 채택·production build·live·브라우저 keyboard/viewport·CSS geometry·색 대비는 NOT_RUN이다.
- 이번 delta의 CSS·인증·URL 권한·Python 변경은 없다. 소비자 실제 gate를 DOM probe로 대신하지 않는다.
- 본 원본 SHA256은 파일 생성 뒤 별도로 전달한다.
