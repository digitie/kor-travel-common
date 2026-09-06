# 현재 상태와 다음 한 작업

현재 상태의 정본이다. 정책은 [AGENTS](../AGENTS.md), 상세 문서 선택은 [문서 지도](README.md), 선행과 상태는 [task 원장](tasks.md), 실행 순서·출구는 [통합 계획](plan/integration-plan.md)을 따른다. 마지막 갱신: 2026-09-07, Codex.

## 현재 상태

[PR #1](https://github.com/digitie/kor-travel-common/pull/1)의 계획·문서와 [PR #2](https://github.com/digitie/kor-travel-common/pull/2)의 T-003 고지·출처·SPDX 구현을 main에 squash merge했다. main은 a3a8444이며 완료 7개·열린 89개다. [Draft PR #3](https://github.com/digitie/kor-travel-common/pull/3)의 T-005 구현은 최초 2인 리뷰의 9개 지적을 수정했고 재검토를 준비 중이다. 완료하지 않았다.

T-003은 a2c1891에서 두 독립 reviewer PASS, 최초 6 finding 모두 FIXED다. Windows Python 3.14.3·WSL Python 3.14.4·Python 3.11.15에서 각각 unittest 100개 성공·skip 0, SPDX 13개 오류 0, CI 성공이다. [최종 리뷰](reviews/adversarial/2026-09-07-t003-post-fix-02.md)에 원본·경계 재현·검증을 연결했다.

`packages/tokens`·`packages/ui`·Python 패키지 실물은 아직 없다. 패키지 build·pack/wheel 설치·소비자 빌드·e2e·시각 검증은 NOT_RUN(실물 없음). SPDX 필수 CI 단계·Windows matrix는 T-009가 맡는다. 소비자 저장소는 수정하지 않았으며 common 구현만 순차 진행한다.

## 다음 한 작업

- 작업: [T-005 버전 레지스트리·현재값](tasks/T-005-versions-registry.md), IN_PROGRESS. 7곳 고정 커밋의 manifest/lock 메타데이터를 읽기 전용으로 대조한다.
- 출구: strict 정책·npm lock 판정·실제 report·예외 근거·자체 검사 CI를 검증하고 2인 리뷰를 마친다. report exit 0을 정책 준수로 세지 않는다.
- 후속: npm/PyPI 게시 제외·common 구현 선행 정리 → T-009 CI 하드닝 → common 구현 순서다. 외부 소비자·권리·릴리스 gate는 담당 task에 남긴다.

## 시작 파일과 검증

T-005 상세 task와 [versions](standards/versions.md), `versions.json`, `tools/check_versions.py`, 해당 회귀 시험을 읽는다. 예비 고장 주입에서 미지 providers 필드·뒤집힌 floor/max가 자체 검사를 통과하고 npm prerelease가 OK로 표시되는 문제를 재현했다. 최초 7개와 리뷰 수정 8개 회귀 시험을 추가했다. 전체 115 tests 성공이며 같은 두 reviewer가 수정 결과를 재확인해야 한다. 명령 사다리는 [개발 환경](dev-environment.md#6-검증-명령-사다리), 리뷰는 [agent workflow](runbooks/agent-workflow.md)를 따른다.

## 차단 조건

- 다른 저장소에 쓰지 않는다. 소비자 채택·CI·배포는 해당 저장소의 task와 PR에서 실행한다.
- 사용자는 모든 라이브러리를 GPLv3로 통일할 예정이라고 밝혔다. 현재 common의 GPL-3.0-or-later와 고정 원천 고지를 유지하며 실제 재선언 이전에 과거 원문·권리 gate를 바꾸지 않는다.

- 사용자 지시: npm·PyPI에 게시하지 않는다. GitHub Release 자산·고정 Git 태그 채널을 유지하며 계정 확보·공개 registry 재평가 task와 불필요한 선행을 다음 계획 정리에서 제거한다. 검증·리뷰가 끝난 작업은 PR로 병합하며 계속 진행한다.
- 외부 결정: pinvi 권리(T-020), concierge·docker-manager 권리(T-021), airport 병합 후 현재 기준선·미해결 CI 재확인(T-430), geo React 승인(T-443), pinvi mobile 명시 예외(O-8). 기본값은 승인 evidence가 아니다.
- 아직 배포하지 않은 규칙·계약 초안은 T-104·T-204·T-302에서 실물과 대조한다. 소비자 테스트 개수·버전은 고정 조사 관찰이며 최신 실행값으로 재사용하지 않는다.
- `check_versions.py`는 초기 구현이다. 미확인·파싱 실패를 정상으로 표시하는 경계와 강제 수준을 회귀 시험으로 정정했으며 T-005 전체 완료 전 CI 강제 승격을 하지 않는다.
- CodeGraph는 이 checkout에 초기화되지 않아 실패했다. 코드 직접 읽기·`rg`·회귀 테스트로 확인했다.

## 인계 자료

[전체 작업](tasks.md) · [완료 원장](tasks-done.md) · [통합 계획](plan/integration-plan.md) · [architecture](architecture/README.md) · [standards](standards/README.md) · [ADR](adr/README.md) · [journal](journal.md). 이력·survey 전체를 작업 시작 때 통독하지 않는다.
