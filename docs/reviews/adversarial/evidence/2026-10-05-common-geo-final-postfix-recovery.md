<!-- SPDX-License-Identifier: GPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie) -->

# common geo 마지막 표시 post-fix 독립 적대 리뷰 원본

실행 ID: `review-recovery-common-geo-426de4fb-20261005T060755-KST`

시각: 2026-10-05 06:07:55–06:10:15 +09:00.

저장소: `F:\dev\kor-travel-common-geo-dashboard`.

실제 base: `589a01ef63ff1ce81960e3d531874b5e4c892995`.

실제 이전 후보: `27b4e31e149ddb4f98ce0bd43429c553a09adc00`.

실제 candidate: `426de4fbad35282bb558712d922c06268e9aba62`.

판정: **PASS — 독립 소스·공개 타입·패키지 재검토 범위.** B-GEO-P2-02/03은 **CLOSED**, B-GEO-P2-01의 CLOSED도 유지하며 새 P0/P1/P2/P3 finding은 없다. 실제 geo/live gate 완료를 뜻하지 않는다.

## 격리·방법

WSL Git의 고정 객체로 실제 hash와 이전 후보→candidate 4파일 delta를 확인했다. 동일 base의 전체 manifest 맥락과 변경 없는 객체는 앞선 독립 리뷰에서 확인한 내용을 재사용했다. 상대 리뷰 원본·결과를 읽지 않았다. 저장소 checkout/commit/source 수정 및 의존성 설치를 수행하지 않았다.

별도 `/tmp/popper-common-geo-426de4fb-20261005`에 고정 source를 추출하고 기존 node_modules만 참조했다. 제공 mirror는 변경하지 않았다. Node `v22.22.2`, npm `11.19.1`을 사용했다. 임시 공격 테스트·빌드·tarball·소비 타입 검증물만 작성했고 앞선 원본 보고서는 수정하지 않았다.

## EXECUTED

- root build/check, UI examples 타입 검사: **PASS**.
- UI 후보 기존 **48 PASS**, 독립 null-job 공격 **1 PASS**, 합계 **49 PASS**.
- 생성된 공개 `.d.ts`에서 문서대로 공용 DagsterRepository와 null guard를 적용한 scheduleUrl callback: strict TypeScript **PASS**. 기존 string-only snapshot을 새 DagsterSnapshot에 전달하는 입력 호환성도 같은 검증에서 **PASS**.
- 수정 후보 UI `npm pack`: **PASS**, 배포 24파일. tarball을 별도 소비 경로에 풀고 실제 operations/model 공개 subpath 타입 import로 이관된 callback을 다시 컴파일했다. **PASS**.

## B-GEO-P2-02 disposition — CLOSED

수정 위치: `packages/ui/src/dagster-operations.tsx:79`.

null 작업의 접힌 버튼은 ‘스케줄 · hourly (작업 미확인)’을 표시하고 jobLabel에 schedule ID를 전달하지 않는다. 독립 spy 공격에서 접힌 상태와 상세를 펼친 상태 모두 jobLabel 호출이 없었다. 상세의 실행되는 작업은 미확인이다.

같은 컴포넌트를 실제 jobName `collect`가 있는 snapshot으로 갱신하면 jobLabel을 `collect`로 호출하고 기존 작업 label을 표시한다. 다시 null snapshot으로 갱신하면 스케줄명과 작업 미확인 표시로 복귀하며 `hourly`를 jobLabel에 전달하지 않는다. 이전 후보에서 실패한 경계를 직접 통과했다.

공격 경로: `/tmp/popper-common-geo-426de4fb-20261005/packages/ui/test/popper-final-job-probe.test.tsx`.

## B-GEO-P2-03 disposition — CLOSED

CHANGELOG Breaking에 공개 jobName의 `string | null` 변경을 기록하고 Migration에 문자열 연산의 null guard, 미확인 작업의 의미와 스케줄명을 job으로 추측하지 않는 원칙을 추가했다. 채택 가이드는 자체 string-only repository로 callback 입력을 축소하지 않고 공용 DagsterRepository를 사용하도록 명시한다.

해당 이관 방식으로 작성한 callback이 후보의 생성 공개 타입과 실제 packed subpath 모두에서 strict TypeScript로 통과했다. 기존 string-only snapshot 입력은 계속 호환된다. 기존 string-only callback의 비호환성을 없앤 변경으로 주장하지 않고, 필요한 파괴 변경과 안전한 이관을 문서화한 disposition으로 CLOSED 처리한다.

소비 검증 경로: 임시 디렉터리의 `compat-published-types/migrated-probe.ts`, `packed-types-consumer/migrated-probe.ts`.

## NOT_RUN·최종 판정

clean install, 실제 geo/weather/transport 소비자 빌드·배포·live 브라우저 E2E, Dagster 장애/복구, 전체 Python 및 RSS 측정은 이번 리뷰에서 수행하지 않았다. 이전 단계의 실행과 부모의 진행 중 검증을 이번 직접 PASS에 합산하지 않았다. 서버 응답 상한·polling/취소 및 소비자 권한 경계에 대한 앞선 판정은 유지한다.

최종 결과: **B-GEO-P2-01/02/03 CLOSED, 새 finding 없음, 독립 재검토 PASS.** geo 소비자와 live gate는 별도로 완료해야 한다.
