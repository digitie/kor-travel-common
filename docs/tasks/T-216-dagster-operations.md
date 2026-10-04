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

## Geo 시각 구성 반영 — 2026-10-05

사용자가 geo 채택과 common 대시보드의 시각 개선을 요청했다. 비교 기준은 geo main
`3f4ddc2dac3f31634a23ef0e9592f419e29e7d14`의 `kor-travel-geo-ui/components/admin/DagsterPanel.tsx`이다.
상태 카드·목록과 상세의 나란한 배치·선택 강조·검색·코드 위치·schedule/sensor tick을
weather 유래 공용 UI에 새로 구현했다. geo의 소스 코드와 CSS를 복사하지 않았으며
geo 전용 실패 확인·백업 다운로드·step 이벤트는 소비자 상세 콜백에 남긴다.

후보 `0.1.0-dev.3`은 페이지당 50행으로 DOM 크기를 제한한다. 서버 snapshot 전체의
집계·검색은 유지하므로 서버 응답 크기와 React 메모리 전체를 50건으로 제한한다는 뜻은 아니다.
실측 RSS 개선율은 측정하지 않았다. 기존 props 기본값·표 `data-slot`·주기 표시를 보존한다.
새 수용 기준: 120건 페이지 이동/필터, 선택 상세, 실패 원문 text escaping, stale 경고,
센서/스케줄 실패 tick·시간대 표시. 단위 45건·타입·빌드·예제 타입 검사 PASS.
tarball 소비자·live UI·2인 최종 리뷰는 이 절 작성 시 IN_PROGRESS이다.

## 2026-10-05 Geo 채택·최종 코드 검증

[최종 판정](../reviews/adversarial/2026-10-05-geo-common.md)에 fixed73e3ff8/Geo4c59efe, 두 독립 최종 PASS, 최초 BLOCK와 전체 수정 원문·SHA256, Python69/UI48·Geo UI231·실제 PostgreSQL17·Linux Chromium/Firefox13항목씩의 증거를 보존했다. 메모리는 유한 page·응답·동시성 구조를 적용했고 운영 RSS 실측은 NOT_RUN이다. 운영 설정/다른 앱 채택은 완료로 세지 않는다. 가이드를 포함한 common PR26·Geo PR570의 최종 checks PASS 후 merge한다.
