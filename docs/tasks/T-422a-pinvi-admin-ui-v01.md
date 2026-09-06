# T-422a pinvi admin UI 0.1 소형 부품 채택

- 상태: BLOCKED
- 우선순위: P1
- Gate: pinvi 빌드·단위·e2e·시각 검증·2인 리뷰
- 선행: T-212, T-421
- 외부 선행: T-420의 L6 실제 반영 evidence와 pinvi 저장소 담당 PR.

## 목표·고정 결정

pinvi admin에 UI 0.1 소형 부품만 채택해 다음 minor 검증의 기준선을 만든다. [ADR-013](../adr/013-package-release-execution-contract.md), [ui-contract](../standards/ui-contract.md), [소비자 절차](../runbooks/consumer-adoption.md)를 따른다.

## 구현 범위

[부모 T-422](T-422-pinvi-admin-ui.md)의 PR A 소형 shim·`cn` 재수출·`@source`만 적용한다. 설치는 정식 `ui-v0.1.0`과 tokens `~0.1.0`, lock·매니페스트를 동반한다. `AdminTable`·Button·overlay와 사용자 표면은 유지한다.

## 범위 밖

UI 0.2 부품(T-422b), 신규 44px 예외 승인·등록, 사용자 UI·모바일·인증 변경.

## 대상 저장소·브랜치·예상 변경 파일

pinvi `codex/T-422a-ui-v01` draft PR 하나(≤30 파일). `apps/web/components/admin/ui` 소형 shim, `apps/web/lib/admin/cn.ts`, `globals.css`, manifest·package·lock. 소비자 원본은 common에 복사하지 않는다.

## 수용 기준

- 부모의 공통 빌드·e2e·시각·페이지/어댑터 무변경·경계 lint gate를 0.1 범위에서 통과한다. 현재 소형 export 목록은 T-203 실물로 대조한다.
- 설치본·lock digest·매니페스트·6폭 evidence와 원 reviewer 재확인이 있고, 현재 e2e/단위 수를 기록한다.
- merge SHA가 기록된 뒤에만 T-213의 pinvi 이전 minor 기준선으로 사용한다. T-213 완료를 선행으로 요구하지 않는다.

## 검증 명령

부모 T-422의 소비자 명령 중 해당 빌드·단위·e2e·시각·경계 lint를 실행한다. `ui_drift.py`가 아직 없으면 후속 T-211을 기다리는 대신 shim diff와 로컬 패치 유무를 수동 대조하고 evidence를 남긴다. 미구현 도구 실행을 성공으로 적지 않는다. Git Bash에서 동일.

## evidence·rollback 또는 release 차단 조건

현재 NOT_RUN(선행 미완). 소비자 PR·merge SHA·설치 버전·시험·시각 결과를 남긴다. 실패 시 소비자 PR을 revert하고 이전 lock으로 `npm ci`한다. L6 미해제·공개 계약 불일치·사용자 표면 변경이면 merge를 차단한다.
