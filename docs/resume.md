# 현재 상태와 다음 한 작업

현재 상태의 정본이다. 정책은 [AGENTS](../AGENTS.md), 상세 문서 선택은 [문서 지도](README.md), 선행과 상태는 [task 원장](tasks.md), 실행 순서·출구는 [통합 계획](plan/integration-plan.md)을 따른다. 마지막 갱신: 2026-09-07, Codex.

## 현재 상태

[PR #1](https://github.com/digitie/kor-travel-common/pull/1)의 계획·문서와 [PR #2](https://github.com/digitie/kor-travel-common/pull/2)의 T-003 고지·출처·SPDX 구현을 main에 squash merge했다. [PR #3](https://github.com/digitie/kor-travel-common/pull/3)의 T-005는 f050997에서 두 독립 reviewer PASS, 최초 9개 finding 모두 FIXED다. 완료 기록 CI 34064140128 성공 후 PR #3을 659aa6d로 병합했다. T-015의 npm/PyPI 미게시·common 구현 선행 정리와 T-006의 범위 변경 기록을 [PR #4](https://github.com/digitie/kor-travel-common/pull/4)에 반영했다. 최종 candidate 95c139f는 두 reviewer PASS·누적 9개 finding FIXED이며 CI 34066138272가 성공했다. 현재 완료 10개·열린 91개다.

T-005는 Windows Python 3.14.3·WSL Python 3.11.15에서 각각 전체 115 tests 성공·skip 0, SPDX 13개 오류 0, CI 성공이다. 7개 소비자의 고정 입력 48파일·306개 판정을 재현했다. report에 fail 기준 위반 102행이 있어 소비자 정책 준수·제품 검증 완료로 세지 않는다. [최종 리뷰](reviews/adversarial/2026-09-07-t005-post-fix.md)에 원본·경계 재현·한계를 연결했다.

`packages/tokens`·`packages/ui`·Python 패키지 실물은 아직 없다. 패키지 build·pack/wheel 설치·소비자 빌드·e2e·시각 검증은 NOT_RUN(실물 없음). SPDX 필수 CI 단계·Windows matrix는 T-009가 맡는다. 소비자 저장소는 수정하지 않았다.

## 다음 한 작업

- 현재 다음 구현 task는 선택하지 않았다. [T-015](tasks/T-015-common-delivery-plan.md)·[T-006](tasks/T-006-npm-scope-pypi-name.md)의 문서·검증·독립 리뷰를 마쳤다([최종 리뷰](reviews/adversarial/2026-09-07-t015-post-fix-03.md)).
- 사용자 최신 지시: 현재 PR #4의 완료 기록과 최종 CI를 확인해 병합한 뒤 대기한다. T-009 및 다른 다음 task는 재개 요청 전 착수하지 않는다.
- 완료 범위는 계획·규범·기록이다. 실제 패키지·후보 보존·외부 릴리스·채택 gate는 미완료 상태를 유지한다.

## 시작 파일과 검증

재개 요청이 오면 [T-009](tasks/T-009-ci-hardening.md)의 선행과 현재 원격 상태부터 확인한다. 현재는 착수하지 않는다. 명령 사다리는 [개발 환경](dev-environment.md#6-검증-명령-사다리), 리뷰는 [agent workflow](runbooks/agent-workflow.md)를 따른다.

## 차단 조건

- 다른 저장소에 쓰지 않는다. 소비자 채택·CI·배포는 해당 저장소의 task와 PR에서 실행한다.
- 사용자 지시: npm·PyPI에 게시하지 않는다. GitHub Release 자산·고정 Git 태그 채널을 유지하며 T-015에서 계정 확보·공개 registry 재평가와 불필요한 선행을 제거했다. 현재 작업 병합 후에는 대기한다.
- 사용자는 모든 라이브러리를 GPLv3로 통일할 예정이라고 밝혔다. 현재 common의 GPL-3.0-or-later와 고정 원천 고지를 유지하며 실제 재선언 이전에 과거 원문·권리 gate를 바꾸지 않는다.
- 외부 결정: pinvi 권리(T-020), concierge·docker-manager 권리(T-021), airport 병합 후 현재 기준선·미해결 CI 재확인(T-430), geo React 승인(T-443), pinvi mobile 명시 예외(O-8). 기본값은 승인 evidence가 아니다.
- 아직 배포하지 않은 규칙·계약 초안은 T-104·T-204·T-302에서 실물과 대조한다. 소비자 테스트 개수·버전은 고정 조사 관찰이며 최신 실행값으로 재사용하지 않는다.
- CodeGraph는 이 checkout에 초기화되지 않아 실패했다. 코드 직접 읽기·rg·회귀 테스트로 확인했다.

## 인계 자료

[전체 작업](tasks.md) · [완료 원장](tasks-done.md) · [통합 계획](plan/integration-plan.md) · [architecture](architecture/README.md) · [standards](standards/README.md) · [ADR](adr/README.md) · [journal](journal.md). 이력·survey 전체를 작업 시작 때 통독하지 않는다.
