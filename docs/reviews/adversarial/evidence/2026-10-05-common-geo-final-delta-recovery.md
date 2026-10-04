<!-- SPDX-License-Identifier: GPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie) -->

# common geo 마지막 표시 delta 독립 적대 리뷰 원본

실행 ID: `review-recovery-common-geo-27b4e31e-20261005T060151-KST`

시각: 2026-10-05 06:01:51–06:05:17 +09:00.

저장소: `F:\dev\kor-travel-common-geo-dashboard`.

실제 base: `589a01ef63ff1ce81960e3d531874b5e4c892995`.

실제 이전 후보: `b2e346e05e3b0bc065105414a66a858bbd905428`.

실제 candidate: `27b4e31e149ddb4f98ce0bd43429c553a09adc00`.

판정: **FAIL — 신규 P2 두 건 OPEN.** nullable 작업명을 정확히 표현하려는 변경은 타당하지만 접힌 행의 오정보와 공개 타입 이관 안내가 남아 있다. P0/P1/P3 신규 발견은 없다. 이전 B-GEO-P2-01의 CLOSED 판정은 유지한다.

## 격리·방법

고정 Git 객체로 실제 hash를 확인하고 이전 후보→candidate 3파일 delta와 필요한 전체 공개 계약 맥락을 검토했다. 동일 base의 변경 없는 객체는 앞선 독립 리뷰에서 확인한 내용을 재사용했다. 상대 리뷰 결과·원문은 읽지 않았다. 저장소 checkout/commit/source 수정이나 의존성 설치는 하지 않았다.

별도 `/tmp/popper-common-geo-27b4e31e-20261005`에 고정 source를 추출하여 기존 node_modules만 참조했다. mirror는 변경하지 않았다. 실행 환경은 Node `v22.22.2`, npm `11.19.1`이다. 앞선 두 원문 보고서를 변경하지 않았다.

## EXECUTED

- root build/check 및 UI examples 타입 검사: **PASS**.
- UI 기존 **48 PASS**, 별도 null-job 공격 회귀 **1 FAIL**.
- 동일 legacy scheduleUrl 콜백의 strict TypeScript 비교: base **PASS**, candidate **TS2322 FAIL**.
- candidate의 실제 생성된 공개 `.d.ts`에서도 동일 legacy 콜백을 컴파일하여 **TS2322 FAIL**을 확인했다.

## B-GEO-P2-02 — 접힌 행은 여전히 스케줄 이름을 실제 작업처럼 표시한다

심각도: **P2**, 신규, **OPEN**.

위치: `packages/ui/src/dagster-operations.tsx:79`, `:193`.

`jobName:null`인 경우 상세의 ‘실행되는 작업’은 미확인으로 바뀌었다. 그러나 접힌 표의 컬럼은 여전히 ‘작업’이고, 행은 `jobLabel(schedule.jobName ?? schedule.name)`를 호출한다. 실제 작업을 모르는 상태에서 스케줄 식별자를 작업 label callback에 넘기는 계약 혼동과 오정보가 남는다.

직접 재현: run이 없고 `{name:"hourly", jobName:null}` 스케줄만 있는 snapshot을 전달했다. jobLabel을 `job => "실제 작업: " + job`인 spy로 주입한 뒤, 스케줄 이름이 jobLabel에 전달되지 않을 것을 검증했다. 공격 회귀는 실제 호출 한 건 때문에 실패했다.

```json
{"calls":[["hourly"]],"table":"작업주기상태▸실제 작업: hourly매시 정각사용"}
```

영향: 일반적인 접힌 화면에서는 실제 job을 확인한 것처럼 표시되며, 상세를 펼친 뒤에만 미확인임을 알 수 있다. consumer의 job 전용 label 매핑에 schedule ID가 전달된다. 후보의 신규 테스트는 펼친 상세만 검사하여 이 경계를 잡지 못한다.

필요한 disposition: null 작업은 jobLabel에 전달하지 않는다. 스케줄 이름을 표시할 때는 작업명이 아님을 명시하고 작업 미확인 상태가 접힌 행에서도 드러나게 한다. 실제 string 작업명은 기존 jobLabel 동작을 유지한다. null 스케줄의 callback 호출·접힌 행과 실제 작업명이 있는 행을 함께 검증하는 회귀가 필요하다.

별도 공격 경로: `/tmp/popper-common-geo-27b4e31e-20261005/packages/ui/test/popper-null-job-probe.test.tsx`.

## B-GEO-P2-03 — nullable 공개 타입의 파괴 변경·이관 안내가 빠져 있다

심각도: **P2**, 신규, **OPEN**.

위치: `packages/ui/src/dagster-model.ts:6`, `CHANGELOG.md`의 Breaking/Migration 절, `docs/runbooks/dagster-adoption.md` 운영 UI 절.

공개 DagsterSchedule.jobName이 `string`에서 `string | null`로 바뀌면 기존 string 전제의 읽기와 repository callback 입력 타입은 호환되지 않는다. 기존 string snapshot을 새 컴포넌트에 전달하는 것 자체는 가능하지만 모든 기존 소비 코드가 호환된다는 뜻은 아니다. 현재 Breaking/Migration은 50행 pagination만 설명한다. 공개 export 타입은 UI 계약의 일부이며 파괴 변경은 이관 안내가 필요하다.

직접 재현: 이전 공개 구조와 동일하게 jobName:string을 갖는 LegacyRepository를 만들고 다음 callback을 scheduleUrl에 할당했다.

```ts
const oldScheduleUrl = (name: string, repository: LegacyRepository) =>
  `/${repository.locationName}/${name}/${repository.schedules[0]?.jobName.toLowerCase()}`;
const accepted: Pick<DagsterOperationsProps, "scheduleUrl"> = {
  scheduleUrl: oldScheduleUrl,
};
```

strict TypeScript에서 base는 exit 0이었다. candidate source 및 실제 생성된 `.d.ts`는 모두 exit 2였다. TS2322의 원인은 `DagsterRepository`의 schedules에 `jobName:string|null`이 있고 LegacyRepository는 string만 허용하는 점이다. 특정 실제 weather/transport 앱의 빌드 실패를 주장하는 것이 아니라 공개 소비 코드의 파괴 변경을 직접 증명한 것이다.

영향: 소비자는 패키지 업데이트 후 콜백 타입이나 jobName 문자열 연산에서 컴파일 오류를 받을 수 있는데 현재 가이드에는 필요한 대응이 없다.

필요한 disposition: nullable 변경은 유지하되 Breaking/Migration과 채택 가이드에 unknown job 의미, 읽기의 null guard, callback에서 새 공용 repository 타입 또는 nullable 입력을 수용하는 방법을 명시한다. 이전 string-only snapshot의 입력 호환성과 읽기/콜백의 비호환성을 구분한다. 잘못된 non-null assertion이나 schedule.name을 실제 job으로 대체하는 이관은 피한다.

재현 경로는 임시 디렉터리의 `compat-base/probe.ts`, `compat-candidate/probe.ts`, `compat-published-types/probe.ts`다.

## NOT_RUN·최종 판정

이번 delta에서 clean install, tarball pack 재실행, 실제 geo/weather/transport 소비자 빌드·배포·live UI, Dagster 장애/복구, 전체 Python 및 RSS 측정은 수행하지 않았다. 직전 후보의 pack 검증은 이번 직접 실행으로 세지 않았다. geo/live는 진행 중으로 취급한다.

최종 결과: **B-GEO-P2-01 CLOSED 유지, B-GEO-P2-02/03 OPEN, FAIL.** 두 신규 finding의 수정 또는 구체적인 disposition을 고정 후보에서 재검토해야 한다.
