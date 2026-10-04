# T-216 공용 Dagster 운영 화면

- 상태: IN_PROGRESS
- 우선순위: P1
- Gate: UI 빌드·단위·tarball·weather 빌드·2인 리뷰
- 선행: T-215
- 외부 선행: common·weather PR 병합 및 소비자 운영 UI 확인

사용자 요청으로 weather의 Dagster 운영 UI를 공용 `DagsterOperations`로 추출한다.
snapshot·label·scope가 적용된 URL·새로고침 콜백을 앱에서 주입한다. GraphQL 문서·인증·
프록시·실행/취소 권한은 소비자가 소유한다. 실패 원인·시작/종료 KST·실행 상한을 넘긴
run·스케줄 상세·새로고침 UI를 유지한다. 공용 CSS는 `.kt-dagster-operations`로 범위를
한정한다. UI 후보 버전은 `0.1.0-dev.1`이며 기존 `dev.0` 산출물을 덮어 배포하지 않는다.

## 수용 기준

- [x] weather의 label/URL을 상수로 common에 넣지 않는다.
- [x] 오류 원문은 React text로 렌더링하고 pending 중 중복 새로고침을 막는다.
- [x] 긴 batch는 자체 실행 상한 전에 정체로 표시하지 않는다.
- [x] 소비자는 UI·tokens tarball과 출처 SHA·digest를 고정한다.
- [x] 단위·패키지 빌드·tarball 설치·weather lint/type/test/build 및 2인 리뷰를 기록한다.

## 검증 기록

실행 결과는 journal·리뷰 기록에 남긴다. 다른 소비자의 채택은 `NOT_RUN(후속 이관)`.

코드·단위·소비자 live 검증과 2인 review는 완료했다.
[최종 리뷰](../reviews/adversarial/2026-10-04-dagster-recovery.md),
[PR #24](https://github.com/digitie/kor-travel-common/pull/24),
[weather PR #72](https://github.com/digitie/kor-travel-weather/pull/72)에 증거를 보존한다.
IN_PROGRESS는 외부 운영 배포/채택까지 완료로 세지 않기 위해 유지한다.


## Transport 후속 채택 후보 — 2026-10-04

사용자가 transport 확산과 필요시 common 수정을 요청했다. UI `0.1.0-dev.2`의 주기 표시,
키보드 표 진입, terminal 경과 시간·잘못된 확인 시각 방어를 추가했다. Python 도메인 SQL은
소비자가 소유하고 기존 `090f984` 공용 복구 코어를 사용한다. 기존 T-301 checkout은 보존한다.
UI 42건·build·pack 및 tarball lock 생성 PASS. 소비자 CI·2인 최종 적대 리뷰·n150 live UI는
현재 IN_PROGRESS이며 후속 evidence에서 정확한 candidate SHA와 결과를 기록한다.
