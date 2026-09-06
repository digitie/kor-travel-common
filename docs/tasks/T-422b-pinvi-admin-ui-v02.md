# T-422b pinvi admin UI 0.2 부품 채택

- 상태: BLOCKED
- 우선순위: P1
- Gate: pinvi 빌드·단위·e2e·시각 검증·2인 리뷰
- 선행: T-213, T-422a
- 외부 선행: pinvi 저장소 담당 PR. 새 44px 예외가 필요하면 O-21의 명시 결정과 적용 범위를 먼저 기록한다.

## 목표·고정 결정

검증된 UI 0.1 기준선 위에서 UI 0.2의 Button·overlay·Table·DataTable·Pager·Form 등을 채택한다. [ADR-013](../adr/013-package-release-execution-contract.md)과 [부모 T-422](T-422-pinvi-admin-ui.md)의 공통 계약을 따른다.

## 구현 범위

부모의 PR B만 적용하고 `AdminTable`의 `manualSorting=false`·사용자 표면을 보존한다. 정식 `ui-v0.2.0`과 tokens `~0.1.0`을 설치해 lock·매니페스트를 갱신한다. T-213 rc 단계에서는 별도 외부 검증 PR으로 이 범위를 시험하고, 정식 발행 후 이 task에서 URL·lock 재검증과 merge를 완료한다.

## 범위 밖

0.1 소형 shim 재작업, 사용자 UI·모바일·앱 도메인, 미승인 예외.

## 대상 저장소·브랜치·예상 변경 파일

pinvi `codex/T-422b-ui-v02` draft PR 하나(≤30 파일). 부모의 PR B 파일·package·lock·매니페스트만 변경한다. 초과하면 파일/계약 기준으로 하위 task를 먼저 분리한다.

## 수용 기준

- 부모의 공통 gate와 정렬 모드·overlay·testid·44px·webpack 검사를 실제 실행한다.
- 예외는 승인 evidence와 범위가 일치하고 신규 예외가 없으면 기존 동작을 보존한다.
- 정식 tarball URL·digest·lock·매니페스트, 6폭 diff, 실제 시험 수와 두 reviewer 결과가 있다.

## 검증 명령

부모 T-422의 빌드·단위·e2e·시각·경계 lint를 실행한다. T-211 도구가 없으면 T-422a와 같은 수동 shim/패치 대조로 기록한다. Git Bash에서 동일.

## evidence·rollback 또는 release 차단 조건

현재 NOT_RUN(선행 미완). 소비자 rc/정식 PR·merge SHA·시험 결과를 기록한다. 실패 시 이 PR 한 건을 revert하고 0.1 lock으로 복구한다. P0/P1·계약 파손·필수 검증 미실행이면 merge하지 않는다.
