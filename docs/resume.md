# 현재 상태와 다음 한 작업

## 2026-10-05 Map·PinVi HTTP 후보

[T-319](tasks/T-319-dagster-recovery.md)의 HTTP 응답 cap·deadline·별도 정리 예산과 dev 의존을 보강했다. 신규 26개 HTTP 회귀가 통과했다. 두 독립 사전 리뷰 원문은 보존하고 고정 후보 전체 post-fix 리뷰·CI는 진행 중이다. 소비자 재구축·live는 해당 저장소 검증이며 현재 완료로 표시하지 않는다.


현재 상태의 정본이다. 정책은 [AGENTS](../AGENTS.md), 문서 선택은 [문서 지도](README.md), 상세 상태·선행은 [task 원장](tasks.md)을 따른다. 마지막 갱신: 2026-10-05, Codex.

## 현재 상태

2026-10-04 사용자 요청: [T-319](tasks/T-319-dagster-recovery.md) Python 실행 복구와 [T-216](tasks/T-216-dagster-operations.md) 공용 Dagster UI 코드·2인 리뷰·live UI·회귀·코드 후보 CI가 완료되었다. [최종 리뷰](reviews/adversarial/2026-10-04-dagster-recovery.md), common PR #24와 weather PR #72에 증거를 보존했다. 다른 소비자 확산과 운영 배포는 미실행이다.

사용자 요청 T-215 공용 로그인·메뉴·6개 실제 프로젝트 테마 예시를 구현했다. 최신 React/Next의 WSL 빌드·단위·tarball 설치·브라우저 검증, 두 독립 post-fix 리뷰와 후보 CI가 통과했다. [최종 리뷰](reviews/adversarial/2026-09-29-t215-wsl-post-fix.md)와 [PR #23](https://github.com/digitie/kor-travel-common/pull/23)이 evidence다. 기존 T-301 작업 checkout과 PR #22는 보존했다.

## 다음 한 작업

common #24·weather #72는 main에 머지되었다. transport 채택을 위한 Python `430a9e9`와 UI `0.1.0-dev.2`의 두 독립 리뷰·CI·격리 소비자 live UI가 통과했다. [common PR #25](https://github.com/digitie/kor-travel-common/pull/25)와 [최종 코드 판정](reviews/adversarial/2026-10-04-transport-adoption-closure.md)에 증거를 보존했다. transport PR #67은 머지 완료했다. 운영 shared coordinator 전환·worker kill·RSS 측정은 NOT_RUN이다. T-301 원본 변경은 보존한다.

## 시작 파일과 검증

[T-215](tasks/T-215-shared-login-menu.md), [예시 실행 안내](../packages/ui/examples/README.md), [최종 리뷰](reviews/adversarial/2026-09-29-t215-wsl-post-fix.md)를 확인한다. 일반 명령은 [개발 환경](dev-environment.md#6-검증-명령-사다리), branch·리뷰·merge는 [agent workflow](runbooks/agent-workflow.md)를 따른다.

## 유지할 제한과 외부 선행

- common 저장소만 수정한다. npm/PyPI에 게시하지 않는다. 공용 라이브러리는 GPL-3.0-or-later이며 기존 외부 원문의 출처·고지는 보존한다.
- 실제 소비자 build/e2e·MDX compile/render·baseline 등록은 해당 이관 task 소유다. Airport dark 예제는 예상 FAIL이며 T-431 외부 gate를 유지한다.
- T-020·T-021은 common의 GPL 결정·요청 문서 완료다. 외부 LICENSE 반영·소비자 채택을 완료로 세지 않는다. T-420·T-430·T-443과 pinvi mobile 예외 등 외부 상태는 각 상세 task에서 확인한다.
- 소비자 저장소·registry·외부 CI를 실행하지 않은 검증은 `NOT_RUN`으로 남긴다. 과거 조사 수치와 후보 값을 현재 정상값으로 사용하지 않는다.

## 인계 자료

[통합 계획](plan/integration-plan.md) · [architecture](architecture/README.md) · [standards](standards/README.md) · [ADR](adr/README.md). 역사·survey 전체를 시작할 때 통독하지 않는다.

## 2026-10-05 geo 대시보드 후속

[T-216](tasks/T-216-dagster-operations.md)의 `dev.3` 후보: 목록/상세·tick·검색·50행 pagination. 기존 작업 branch를 보존한다. [최종 판정](reviews/adversarial/2026-10-05-geo-common.md)에 두 코드 PASS·69 Python/48 UI·소비자 live와 실패 수정 원문을 보존했다. common PR26·Geo PR570의 문서 포함 최종 checks가 통과한 뒤 순서대로 merge한다. 운영 배포·RSS 측정·다른 소비자 확산은 후속이며 완료로 세지 않는다.

## 2026-10-05 PinVi 채택 후속

Common dev.6의 두 독립 post-fix PASS, UI50·tarball smoke와 PinVi 실제 N150 live 4PASS를 [최종 판정](reviews/adversarial/2026-10-05-pinvi-common.md)에 보존했다. [Common #27](https://github.com/digitie/kor-travel-common/pull/27)과 [PinVi #575](https://github.com/digitie/pinvi/pull/575)에 최종 CI/머지 게이트를 결박했다. 이후 운영 검증은 별도 배포 요청에서 진행한다. Common #26/Geo #570은 merge 완료. 운영 shared daemon/worker kill/RSS는 NOT_RUN이다. 기존 T-301 원본 변경은 보존한다.
