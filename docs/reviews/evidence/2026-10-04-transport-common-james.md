# James — Transport 채택용 common 후보 원본 적대 리뷰

- 실행 ID: `J-COMMON-20261004-f3e5681f`
- 시작 기록 시각: `2026-10-04 05:34:16 UTC`
- 종료 기록 시각: `2026-10-04 05:36:30 UTC`
- 전문 영역: UI·공개 API·CSS·접근성·소비자 tarball·cron/시간 경계·loading/error.
- 저장소: `F:/dev/kor-travel-common-recovery`
- immutable base: `090f98429453d8882150eb9e56ccae98e0e353a2`
- immutable candidate: `f3e5681fcc751cc2951d74f72f9c90be1f29d670`
- 요청: common Draft PR #25의 위 고정 후보를 독립 검토한다. transport PR #67의 후보는 이 리뷰 범위가 아니다.
- 격리: Windows Git show/diff/rev-parse로 고정 commit 객체의 전체 14파일 delta를 읽었다. worktree source를 검토 대상으로 사용하지 않았다. 고정 Git model 객체를 stdin으로 전달하고 설치된 TypeScript compiler로 메모리에서 변환한 뒤 WSL Node에서 경계 assertion만 실행했다. 소스·빌드 산출물·lock을 수정하지 않았다. 이 원본 report 파일만 생성했다. 다른 reviewer 원본을 읽거나 공유받지 않았다.
- 판정: **PASS — 검토 범위에서 P0/P1/P2 finding 없음. transport 소비자의 scoping/auth/active 목록 및 live UI 승인을 대신하지 않는다.**

## 확인한 변경과 공격 시나리오

1. **cron 경계** — describeCron의 새로운 minute/hour step 경로는 양수이며 60/24의 약수인 경우에만 일정한 주기로 설명한다. */7 minute 또는 */7 hour처럼 경계를 넘을 때 간격이 달라지는 값은 원문으로 남는다. 0 step, minute75, hour25, 음수/복잡한 calendar는 원문으로 유지한다. */24 hour의 하루 한 번 실행도 24시간 설명과 일치한다. whitespace 분리·hour 목록의 정상 0~23 범위를 유지한다. transport 고유 상수를 common에 넣지 않았다.
2. **terminal duration** — startTime과 계산에 사용할 end가 유한할 때만 duration을 반환한다. 종료 run은 snapshot 확인 시각 대신 endTime을 사용하므로 잘못된 now/새로고침에도 종료 duration이 변하지 않는다. endTime이 없는 종료 run이나 잘못된 startTime은 null이며 음수 차이는 0으로 제한한다. isStalledRun의 명시 STARTED 조건 때문에 오래 걸린 SUCCESS/FAILURE/CANCELED를 정체로 오표시하지 않는다. STARTED와 잘못된 now는 경과 값을 만들지 않는다.
3. **loading/error** — 이번 delta는 소비자 콜백·snapshot ownership을 변경하지 않는다. pending refresh disabled, aria-busy, 오류 React text, 조회 실패 중 마지막 snapshot/checkedAt 보존 가능한 계약을 유지한다. common이 새로운 HTTP/auth/취소·실행 권한을 소유하는 경로를 찾지 못했다.
4. **키보드 표 진입** — 두 table-wrap에 각각 한국어 이름의 role=region 및 tabIndex=0을 추가했다. 기존 table column scope·상세 header·schedule aria-expanded·링크 의미를 유지한다. 새 focus-visible rule은 kt-dagster-operations 안으로 제한되며 존재하는 kt-focus를 사용한다. 기존 tokens나 다른 앱 전역 selector를 바꾸지 않는다. 실제 keyboard scroll/outline clipping은 소비자 viewport에서 확인해야 한다.
5. **기존 API·보안** — 필수/선택 prop, slots/testId, repository 복합 schedule identity와 URL callback 문맥은 변경되지 않았다. 순수 dagster-model import에 React/auth/HTTP 의존성을 추가하지 않았다. URL 안전성과 scope는 문서대로 소비자 책임이다. 오류 문자열은 HTML로 해석하지 않는다. 날짜 표시는 기존 KST 계약을 유지한다.
6. **tarball/버전** — ui 버전을 dev.1에서 dev.2로 올리고 root workspace lock, smoke package/lock 및 prepare-lock 파일명을 함께 갱신했다. 같은 dev.1 archive를 덮어 재배포하는 방식이 아니다. exports/files/sideEffects/React19/tokens peer/license 고지는 보존된다. smoke lock의 resolved filename/version/integrity가 새 패키지명과 일치한다. 실제 archive digest와 consumer 설치는 transport 고정 후보의 provenance/lock을 대상으로 별도 확인해야 한다.
7. **문서·gate** — 변경 기록은 42 tests/build/pack을 작성자 실행 결과로 구분하고 소비자 CI·적대 리뷰·n150 live UI를 진행 중으로 남긴다. 실제 shared daemon 설정을 소비자 YAML 수정과 동일시하지 않는 안내를 유지한다. 새 transport 사례의 도메인 SQL/48·72시간 보호 구현은 transport 후속 리뷰에서 확인할 사항이며 common UI 변경 자체의 승인 범위를 넓히지 않는다.

## 독립 재현과 읽은 검증

독립 실행한 것은 고정 candidate의 dagster-model.ts 객체를 메모리에서 transpile한 순수 함수 경계 시험이다. cron 9개와 duration/stalled 6개 assertion이 PASS했다. 입력은 */15, 30 */6, */59, hour */7, */60, hour */0, hour */24, 23:59, 음수 minute 및 FAILURE/CANCELED·NaN 조회 시각·null end·Infinity start를 포함한다. 출력: `고정 Git model 객체 cron9/duration6 경계 assertion PASS`.

후보의 신규 unit tests는 transport 5분/4시간/8시간 주기, 잘못된 cron fallback, terminal/invalid now, 두 region의 tabIndex를 검증하며 기존 injection/error/stalled/repository/token 시험을 유지한다. 이 tests와 작성자의 UI42 통과 기록을 읽었으며 전체 suite를 본 reviewer가 재실행한 것으로 주장하지 않는다. 요청자가 common CI 전부 green을 확인했다고 전달했다. 본 reviewer가 GitHub 실행 상태를 독립 조회한 것은 아니다.

## findings와 미검증

P0/P1/P2 신규 finding 없음. runElapsedSeconds의 기존 STARTED 전용 설명 주석은 확장된 terminal 동작보다 좁지만 CHANGELOG/test가 새 동작을 명시하고 있어 merge 안전성 결함으로 분류하지 않았다. 이후 문서 정리 시 실제 동작에 맞출 수 있다.

NOT_RUN: 본 reviewer의 전체 UI suite/clean npm 설치/production build/tarball 재생성·digest 계산, 실제 브라우저 keyboard/mobile/focus/색상, transport auth/GraphQL/active pagination, 운영 shared instance/worker 장애·배포. transport 후보 리뷰와 n150 live UI evidence가 공용 UI의 실제 소비 계약을 확인해야 한다. 현재 PASS는 위 immutable common delta의 코드·계약 검토 판정이다.
