<!-- SPDX-FileCopyrightText: 2026 digitie -->
<!-- SPDX-License-Identifier: GPL-3.0-or-later -->

# Common geo 최종 표시 delta — UI 독립 리뷰 원본

- 실행 ID: `A-COMMON-GEO-UI-FINAL-DELTA-20261005-27b4e31e`.
- 관찰: `2026-10-04 21:01:55~21:03:49 UTC` / `2026-10-05 06:01:55~06:03:49 KST`.
- 저장소: `F:/dev/kor-travel-common-geo-dashboard`. Windows에서는 공유 object 저장소 `F:/dev/kor-travel-common`으로 같은 고정 Git 객체를 읽었다.
- 전체 base: `589a01ef63ff1ce81960e3d531874b5e4c892995`.
- delta base: `b2e346e05e3b0bc065105414a66a858bbd905428`.
- 실제 후보: `27b4e31e149ddb4f98ce0bd43429c553a09adc00`.
- 독립 격리: source read-only/show/diff, 3파일 13줄 추가·3줄 삭제를 검토했다. 기존 전체 manifest 맥락과 공개 계약을 함께 확인했다. peer 결과는 읽지 않았다. 구현·checkout·commit·설치·mirror·DB는 변경하지 않았다. 이전 원문은 보존했다.

## 판정

**CONDITIONAL — 새 P2 두 건의 수정 또는 명시적 disposition이 필요하다. 새 P0/P1은 없다.**

null 작업 이름의 펼친 상세는 미확인으로 수정됐다. 그러나 접힌 표의 표시 의미와 공개 nullable 타입의 소비자 이관 안내는 남아 있다. 실제 geo/live gate는 진행 중이며 본 판정에서 완료로 집계하지 않는다.

## 새 findings

### A-P2-02 — 접힌 목록은 미확인 작업을 여전히 작업 이름처럼 표시한다

- 위치: `packages/ui/src/dagster-operations.tsx:79`, `:193`.
- 실패 시나리오: `{name:"hourly-schedule", jobName:null}`을 표시한다. 첫 열 header는 작업이며 그 열에 hourly-schedule이 표시된다. 펼쳐야만 실행되는 작업 미확인이 보인다.
- 독립 재현: 고정 component/model을 jsdom에 렌더링했다. header 작업과 버튼 hourly-schedule을 assertion으로 확인했다. 펼친 상세의 미확인과 실제 schedule 이름 기반 URL도 확인했다.
- 영향: 접힌 기본 목록과 스크린리더의 열 맥락은 미확인 job을 스케줄 이름으로 단정한다. 상세의 올바른 표시만으로 목록의 의미를 고치지는 못한다.
- 최소 수정: 열 이름을 작업/스케줄 등으로 구분하고 jobName null인 행은 스케줄 이름임을 화면·접근 가능한 이름에서 명시한다. 알려진 job 이름 표시는 유지한다.
- disposition 조건: 접힌 목록에서도 job과 schedule의 구별이 검증되거나 P2 연기 owner/task/gate/목표 시점을 기록한다.

### A-P2-03 — 공개 nullable 타입의 파괴 변경과 이관이 문서에서 누락됐다

- 위치: `packages/ui/src/dagster-model.ts:7`; `CHANGELOG.md:17`, `:21`.
- 실패 시나리오: 기존 소비자의 `jobLabel(schedule.jobName)` 또는 string 변수 대입은 이전 공개 타입에서 유효했으나 이제 strict TypeScript 검사에 실패한다.
- 독립 재현: 고정 전/후 model과 메모리 consumer의 semantic diagnostics를 TypeScript로 비교했다. 아래 코드는 b2e에서 진단 0개, 27b에서 TS2345(string | null을 string 매개변수에 전달할 수 없음)였다.

```ts
import type { DagsterSchedule } from "./dagster-model";
declare const schedule: DagsterSchedule;
declare function jobLabel(name: string): string;
jobLabel(schedule.jobName);
```

- 영향: 기존 string을 만드는 DTO 입력은 여전히 유효하지만 공개 타입을 읽는 소비자 코드의 build는 깨질 수 있다. 현재 Breaking/Migration은 50행 변경만 안내한다.
- 최소 수정: nullable 변경을 Breaking/Migration과 채택 가이드에 기록하고 소비자가 null을 미확인으로 처리하는 예제를 제공한다. schedule.name을 실제 job의 대체 정본으로 안내하지 않는다. 알려진 job만 필요한 코드는 null guard 뒤 사용한다.
- disposition 조건: 타입 변경의 실제 소비자 이관 안내와 검증 또는 명시적 P2 disposition. nullable 의미 자체를 잘못됐다고 주장하는 finding은 아니다.

## EXECUTED

고정 source를 mirror의 기존 의존성으로 메모리에서 실행했다.

- null job 상세 미확인, 콜백에는 string 전달, schedule URL/repository scope, 알려진 job으로 갱신 후 label·실제 job 상세 유지: PASS.
- 이전 A-P1-01 필터 갱신 불일치와 A-P2-01 센서 미제공 표시: 수정 유지 확인, CLOSED 유지. 초기 P1/P2 severity를 변경하지 않는다.
- 120건 pagination 50/50/20, 필터·선택·상세·검색, text escaping·오류 snapshot·tick·시간대: PASS.
- axe-core DOM 위반 0개. color contrast는 비활성화했고 PASS로 세지 않았다.
- 공개 타입 consumer 전/후 비교: TS2345 차이를 재현했다. 첫 가상 module harness는 resolver를 누락해 자체 assertion 실패했으며 후보 결함으로 세지 않았다. 고정 model을 명시적으로 해석하는 메모리 host로 보정한 뒤 위 진단 차이를 확인했다.

## NOT_RUN

- 직접 전체 UI48 suite·build/check/examples를 실행하지 않았다. 해당 PASS는 부모 전달 결과다.
- 실제 geo tarball 채택·production build·live·브라우저 keyboard/viewport·CSS geometry·색 대비는 NOT_RUN이다.
- 이번 delta는 CSS·인증·URL 권한·Python을 변경하지 않는다. 별도 live gate를 본 DOM 실행으로 대신하지 않는다.
- 본 원문 SHA256은 파일 생성 뒤 별도로 전달한다.
