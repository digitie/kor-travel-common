# 현재 상태와 다음 한 작업

현재 상태의 정본이다. 정책은 [AGENTS](../AGENTS.md), 상세 문서 선택은 [문서 지도](README.md), 선행과 상태는 [task 원장](tasks.md), 실행 순서·출구는 [통합 계획](plan/integration-plan.md)을 따른다. 마지막 갱신: 2026-09-06, Codex.

## 현재 상태

[Draft PR #1](https://github.com/digitie/kor-travel-common/pull/1)의 `09104ed`와 로컬 Claude 초안을 통합했다. 상세 task 96개 중 문서·계획 6개(T-001·T-002·T-004·T-007·T-008·T-013)를 완료 원장으로 옮겼고 열린 90개는 선행·외부 대기·잔여 수용 기준을 갖는다. 기존 소비자 조사 기준은 갱신하지 않았다.

Windows Python 3.14.3·WSL Python 3.14.4에서 unittest 67개 성공·skip 0. 코드가 같은 5670642의 Linux CI도 성공했다. 원 14건과 후속 1건의 finding은 모두 FIXED이며 두 전문 reviewer가 PASS로 재확인했다. 기준선별 원본·CI와 종료 delta의 최신 판정은 [리뷰 색인](reviews/README.md)이 연결한다. 이 결과는 문서·도구 검증이며 패키지 또는 소비자 gate 통과가 아니다.

실물 `packages/tokens`·`packages/ui`·Python 패키지가 없다. 패키지 빌드·tarball/wheel 설치·소비자 빌드·e2e·시각 검증은 NOT_RUN(실물·소비자 변경 없음). T-003 SPDX 검사·라이선스 사본과 T-005 실제 소비자 현재값 등록도 남아 있다. 따라서 Phase 0 전체 완료·릴리스 가능 상태가 아니다.

## 다음 한 작업

- 작업: [T-003 고지·출처·SPDX](tasks/T-003-notices-provenance-spdx.md)의 READY 상태를 인수해 미완료 수용 기준부터 착수한다.
- 출구: 고정 upstream 원문 사본·고지 연결·SPDX 도구와 음성 fixture를 검증하고 2인 리뷰를 마친다. 실제 수행 전에는 DONE으로 옮기지 않는다.
- 후속: T-005 잔여(소비자 실제 현재값·예외·보고) → T-009(CI 하드닝) 순서로 한 작업씩 진행한다. 상세 선행·외부 선행이 우선한다.

## 시작 파일과 검증

시작 파일: 위 T-003의 범위·수용 기준과 [licensing](standards/licensing.md), [PROVENANCE](../PROVENANCE.md). 명령은 해당 task와 [개발 환경 §6](dev-environment.md#6-검증-명령-사다리), 검증·리뷰 절차는 [agent workflow](runbooks/agent-workflow.md)를 따른다. 실물 구현에 앞서 고지·출처 gate부터 닫는다.

## 차단 조건

- 외부 결정: npm/PyPI 계정(T-006), pinvi 권리(T-020), concierge·docker-manager 권리(T-021), airport 병합 후 현재 기준선·미해결 CI 재확인(T-430), geo React 승인(T-443), pinvi mobile 명시 예외(O-8). 기본값은 승인 evidence가 아니다.
- 아직 배포하지 않은 규칙·계약 초안은 T-104·T-204·T-302에서 실물과 대조한다. 소비자 테스트 개수·버전은 고정 조사 관찰이며 최신 실행값으로 재사용하지 않는다.
- `check_versions.py`는 초기 구현이다. 미확인·파싱 실패를 정상으로 표시하는 경계와 강제 수준을 회귀 시험으로 정정했으며 T-005 전체 완료 전 CI 강제 승격을 하지 않는다.
- CodeGraph는 이 checkout에 초기화되지 않아 실패했다. 코드 직접 읽기·`rg`·회귀 테스트로 확인했다.

## 인계 자료

[전체 작업](tasks.md) · [완료 원장](tasks-done.md) · [통합 계획](plan/integration-plan.md) · [architecture](architecture/README.md) · [standards](standards/README.md) · [ADR](adr/README.md) · [journal](journal.md). 이력·survey 전체를 작업 시작 때 통독하지 않는다.
