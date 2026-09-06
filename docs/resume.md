# 현재 상태와 다음 한 작업

현재 상태의 정본이다. 정책은 [AGENTS](../AGENTS.md), 상세 문서 선택은 [문서 지도](README.md), 선행과 상태는 [task 원장](tasks.md), 실행 순서·출구는 [통합 계획](plan/integration-plan.md)을 따른다. 마지막 갱신: 2026-09-06, Codex.

## 현재 상태

[Draft PR #1](https://github.com/digitie/kor-travel-common/pull/1)의 `09104ed`와 로컬 Claude 초안을 인수했다. 누락된 원장·통합 계획을 추가했고 상세 task 96개를 연결했다. 외부 선행과 실물 패키지를 기다리는 task는 BLOCKED로 정정했다. 기존 소비자 조사 기준은 갱신하지 않았다.

Windows Python 3.14.3에서 unittest 65개 성공·skip 0. 앞선 커밋 e9a3a0f는 Linux CI green이며 새 리뷰 정정 커밋의 검증은 진행 중이다. 두 원본 리뷰는 BLOCK이었고 버전 판정·릴리스 선행·승인 gate finding을 수정해 재검토할 예정이다. 최신 결과는 [리뷰 색인](reviews/README.md)에서 확인한다. 이 수치는 문서·도구 검증이며 패키지 또는 소비자 gate 통과가 아니다.

실물 `packages/tokens`·`packages/ui`·Python 패키지가 없다. 패키지 빌드·tarball/wheel 설치·소비자 빌드·e2e·시각 검증은 NOT_RUN(실물·소비자 변경 없음). T-003 SPDX 검사·라이선스 사본과 T-005 실제 소비자 현재값 등록도 남아 있다. 따라서 Phase 0 전체 완료·릴리스 가능 상태가 아니다.

## 다음 한 작업

[T-013 계획·인계 마무리](tasks/T-013-plan-handoff-closure.md): immutable candidate를 두 전문 리뷰어가 독립 적대적 검토 → 원본 evidence 보존 → finding 수정·후속 task 지정 → post-fix commit 재검토 → 실제 gate가 닫힌 task만 DONE → draft PR 본문·인계 갱신. PR merge는 이번 요청 범위 밖이다.

시작 파일: 위 T-013과 [agent workflow §5](runbooks/agent-workflow.md#5-전문-리뷰어-서브에이전트-2인-적대적-리뷰). 검증 명령은 [개발 환경 §6](dev-environment.md#6-검증-명령-사다리). 리뷰 결과는 [리뷰 색인](reviews/README.md)에 기록한다.

T-013 이후에는 [T-003](tasks/T-003-notices-provenance-spdx.md)의 미완료 수용 기준부터 한 작업씩 진행한다. 그 뒤 T-005 잔여 → T-009 순서이며, 상세 선행·외부 선행이 우선한다.

## 차단 조건

- 외부 결정: npm/PyPI 계정(T-006), pinvi 권리(T-020), concierge·docker-manager 권리(T-021), airport 병합 후 현재 기준선·미해결 CI 재확인(T-430), geo React 승인(T-443), pinvi mobile 명시 예외(O-8). 기본값은 승인 evidence가 아니다.
- 아직 배포하지 않은 규칙·계약 초안은 T-104·T-204·T-302에서 실물과 대조한다. 소비자 테스트 개수·버전은 고정 조사 관찰이며 최신 실행값으로 재사용하지 않는다.
- `check_versions.py`는 초기 구현이다. 미확인·파싱 실패를 정상으로 표시하는 경계와 강제 수준을 회귀 시험으로 정정했으며 T-005 전체 완료 전 CI 강제 승격을 하지 않는다.
- CodeGraph는 이 checkout에 초기화되지 않아 실패했다. 코드 직접 읽기·`rg`·회귀 테스트로 확인했다.

## 인계 자료

[전체 작업](tasks.md) · [완료 원장](tasks-done.md) · [통합 계획](plan/integration-plan.md) · [architecture](architecture/README.md) · [standards](standards/README.md) · [ADR](adr/README.md) · [journal](journal.md). 이력·survey 전체를 작업 시작 때 통독하지 않는다.
