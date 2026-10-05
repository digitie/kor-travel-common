## 2026-10-06 — Map·PinVi 공통 Dagster 실제 재구축·live 수용 완료

Common a960bdb, Map 1a3c467, PinVi 0058369의 제품113파일 두 독립 FULL 리뷰와 가이드 리뷰를 통과했다. 공용 Python은 bounded HTTP·경량 child health·실행 복구 정책을 제공하며 앱의 operation/lease/claim·비멱등 쓰기 계약을 유지한다. 요청별 응답4MiB/10초와 정리50ms, DB pool/step 제한·100개 batch를 적용했다. Map tick 조회의 오래된 batch history 정렬 지연은 상태 조건을 명시하여 native indexed LIMIT 경로로 줄였고 실제 summary/UI 복구를 확인했다.

운영 paired 재구축과 설치 source·관련 Common bytes·실제 이미지 identity·여섯 서비스 healthy를 검증했다. Chromium/Firefox×Map/PinVi 실제 UI4건과 캡처8개를 직접 확인했다. ACL40·D1 11건·D2 정상 수용/validator·소유 fixture purge1/7·잔존0/ACTIVE없음/BLOCKED없음까지 통과했다. Common의 ESM export를 읽기 위한 type=module은 별도 테스트 이미지 package.json에만 추가하고 실제 마지막 layer/semantic delta를 증명했다. 앞선 모든 실패·초기 BLOCK와 수정 후 PASS 원문은 보존한다.

격리 native Dagster에서 실제 raise·worker crash·stall/timeout 뒤 수동 재시도와 동시 정상 job을 확인했다. 최종 Map 운영 Dagster 이미지의 관련 설치 코드와 버전이 이전 격리 이미지와 같은지, 실제 최종 이미지 ID가 배포 기록과 맞는지 독립 검증했다. 이 결과는 해당 불변 코드 범위에 한정해 이어받는다. 공유 운영 DB의 worker 장애 주입이나 운영 RSS 감소율 실측으로 설명하지 않는다. 유한 응답·batch·동시성 구조와 합성 메모리 측정은 운영 RSS와 구분한다. 기존 인간 dirty checkout·외부 transport/HAProxy 후속은 보존한다.

다음 한 작업은 문서 포함 exact HEAD CI 통과 후 Common #28 → Map #1303 → PinVi #576 순서로 merge commit 병합하는 것이다. 제품 Git pin의 ancestry를 보존한다. 이 절이 현재 상태이며 아래의 진행 중/NOT_RUN 문단은 이전 시점의 이력이다.

[실제 검증·리뷰 원문과 실패 이력](reviews/adversarial/2026-10-05-map-health-closure.md), [공통 적용 가이드](runbooks/dagster-adoption.md).

## 2026-10-05 — metadata map의 serdes marker 차단 (진행 중)

99d8 고정 후보 재리뷰에서 library versions와 pointer dictionary의 typed marker가 경량 검증을 우회하는 P2를 확인했다. 다섯 reserved serdes marker를 거부하되 정상 Map default 이름 __repository__는 허용한다. 실제 isolated CLI 정상 default repository와 두 공격 응답, 모든 marker 회귀를 포함한 health65 PASS를 확인했다. 이전99 전체146 PASS는 이전 소스 증거이며 새 후보의 두 독립 FULL 리뷰·CI·운영 재구축/live가 남았다. [가이드 §10](runbooks/dagster-adoption.md#10-code-server-자식-로딩을-확인하는-경량-건강-점검)에 지원 경계를 보완했다.

## 2026-10-05 — 경량 health의 표준 metadata profile 보강 (진행 중)

독립 리뷰에서 e0b5e31 후보의 null/미등록 code pointer와 executable/entry point 잘못된 타입이 실제 Dagster 역직렬화에서는 거부되지만 경량 CLI에서는 정상 처리되는 P2를 확인했다. 기존 PASS/BLOCK 판정은 그대로 보존한다. module/file/package pointer와 nullable metadata 타입을 검증하고, stateful/custom typed metadata·알려지지 않은 필드는 실패로 판정한다. 지원 profile과 확장 방법은 [가이드 §10](runbooks/dagster-adoption.md#10-code-server-자식-로딩을-확인하는-경량-건강-점검)에 명시했다. schema 변경 후 전체 Python139 PASS, 실제 isolated CLI 7건을 포함한 health51 PASS를 각각 확인했으며 합산하지 않는다. 새 고정 후보의 두 독립 리뷰·CI·운영 재구축/live가 남았다.

## 2026-10-05 — Map code-server의 빈 reply 오인 방지 (진행 중)

T-319의 공용 `dagster_health`는 proxy SERVING 뒤 실제 `ListRepositoriesResponse` protobuf/JSON을 검증한다. Map 최신 main의 substring 점검이 빈/잘못된 reply를 정상으로 판정한 독립 적대 리뷰 반례를 반영했다. 전체 Dagster import 없이 설치된 생성 protobuf를 사용하며 각 RPC 4초·수신 4MiB·channel 정리와 fail-closed를 적용한다. [가이드 §10](runbooks/dagster-adoption.md#10-code-server-자식-로딩을-확인하는-경량-건강-점검)에 소비자 채택·재시작 정책 경계를 기록했다. 새 고정 후보 2인 리뷰·CI·실제 paired 재구축/live는 진행 중이다.

# 현재 상태와 다음 한 작업

## 2026-10-05 — Map·PinVi HTTP 최종 독립 리뷰

고정1f8e339의 두 독립 FULL 리뷰 PASS와 모든 finding FIXED, Python95/HTTP26·strict 타입·wheel·문서 도구 검증을 [최종 판정](reviews/adversarial/2026-10-05-map-http-closure.md)에 보존했다. 소비자 실제 재구축/live 및 공통 PR28 exact CI gate는 후속이다.

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
