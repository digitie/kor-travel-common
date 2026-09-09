# 현재 상태와 다음 한 작업

현재 상태의 정본이다. 정책은 [AGENTS](../AGENTS.md), 문서 선택은 [문서 지도](README.md), 상세 상태·선행은 [task 원장](tasks.md)을 따른다. 마지막 갱신: 2026-09-09, Codex.

## 현재 상태

T-103 대비·UX 검사기 구현과 반복 리뷰의 근본 수정을 완료했다. 수동 MDX 파서를 제거하고 [ADR-016](adr/016-mdx-parser-for-ux-lint.md)의 실제 파서로 전환했으며 원문 BOM 좌표도 보정했다. [최종 통합 리뷰](reviews/adversarial/2026-09-08-t103-parser-post-fix.md)에 후보·두 독립 PASS·CI·실패 및 미실행 기록을 보존한다. T-010 재사용 워크플로 1단계도 실제 tarball·fixture 경계와 두 독립 최종 PASS, candidate CI까지 완료했으며 [최종 통합 리뷰](reviews/adversarial/2026-09-09-t010-post-fix.md)와 [PR #21](https://github.com/digitie/kor-travel-common/pull/21)에 기록했다. 현재 T-301 OpenAPI 정본 초안·예외 레지스트리 생성 도구·회귀 시험을 진행 중이다. 앞선 완료 작업은 [완료 원장](tasks-done.md), 재현 이력은 [journal](journal.md)에 있다.

## 다음 한 작업

**T-301 구현·리뷰 준비.** `openapi.md`의 core 규칙 30개에 계층·검사 수단·예외 여부를 명시하고, M10은 ADR-009에 맞게 교차 저장소 MUST로 분리했다. `openapi-exceptions.yaml` 46건을 7키·규칙 ID·날짜·sunset으로 검증하며 `openapi-exceptions.md`를 생성하는 stdlib 도구와 8개 회귀 시험을 추가했다. 다음은 문서 gate와 두 독립 적대적 리뷰, finding 반영, candidate CI, draft PR이다. T-010a의 실제 소비자 dispatch는 외부 선행으로 계속 BLOCKED다.

## 시작 파일과 검증

현재 작업 확인은 [T-301](tasks/T-301-openapi-standard.md), [OpenAPI 표준](standards/openapi.md), [ADR-009](adr/009-openapi-rest-conventions.md)에서 시작한다. 로컬에서는 `tools/openapi_exceptions.py --check`와 focused/full unittest를 실행하고, 소비자 build/e2e는 후속 이관 task로 `NOT_RUN`을 기록한다. 설치·검증 명령은 [개발 환경](dev-environment.md#6-검증-명령-사다리), 리뷰·병합은 [agent workflow](runbooks/agent-workflow.md)가 정본이다.

## 유지할 제한과 외부 선행

- common 저장소만 수정한다. npm/PyPI에 게시하지 않는다. 공용 라이브러리는 GPL-3.0-or-later이며 기존 외부 원문의 출처·고지는 보존한다.
- 실제 소비자 build/e2e·MDX compile/render·baseline 등록은 해당 이관 task 소유다. Airport dark 예제는 예상 FAIL이며 T-431 외부 gate를 유지한다.
- T-020·T-021은 common의 GPL 결정·요청 문서 완료다. 외부 LICENSE 반영·소비자 채택을 완료로 세지 않는다. T-420·T-430·T-443과 pinvi mobile 예외 등 외부 상태는 각 상세 task에서 확인한다.
- 소비자 저장소·registry·외부 CI를 실행하지 않은 검증은 `NOT_RUN`으로 남긴다. 과거 조사 수치와 후보 값을 현재 정상값으로 사용하지 않는다.

## 인계 자료

[통합 계획](plan/integration-plan.md) · [architecture](architecture/README.md) · [standards](standards/README.md) · [ADR](adr/README.md). 역사·survey 전체를 시작할 때 통독하지 않는다.
