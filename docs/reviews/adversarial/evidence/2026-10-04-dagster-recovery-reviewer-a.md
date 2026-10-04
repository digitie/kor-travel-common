# Reviewer A 원본 적대 리뷰

- 실행 ID: `A-20261004-DAGSTER-270619bd-709dc44c`
- 최초 기록 시각: `2026-10-04 00:56:49 UTC`
- 종료 기록 시각: `2026-10-04 00:58:50 UTC`
- common base: `be7f21f2a645f4ce882b3d841487e1b40ad23425`
- common candidate: `270619bd98c21ead62d077bf46f09c92dd946a59`
- weather base: `5da6e158dccc8ea98e8301078ce9610525da0ebf`
- weather candidate: `709dc44cf2661ab546a6b126ce06fcea00d666c0`
- 격리: 지정 저장소의 Windows Git `show`, `diff`, `rev-parse`로 고정 commit 객체만 읽었다. 소스 수정·빌드·테스트 실행 없이 검토했다. 다른 reviewer의 결과를 받거나 참조하지 않았다.
- 판정: **BLOCK — 아래 P2 두 건과 공개 마크업 계약 누락을 수정하고, 변경된 후보 및 실제 브라우저 결과를 재검토해야 한다.**

## 발견 사항

### A-P2-01 — 존재하지 않는 상태 토큰 때문에 실패 색상과 오류 테두리가 사라진다

**위치:** common `packages/ui/dagster.css:19`, `:21`

```css
.off, .dagster-run-error { color: var(--kt-error); }
.error { border: 1px solid var(--kt-error); }
```

배포 tokens의 상태 토큰은 `--kt-destructive`이며 `--kt-error`는 정의되지 않았다. tokens/theme.css에도 해당 별칭이 없다. weather globals에도 이를 보완하는 `--kt-error` 정의가 없다.

**재현:** README대로 tokens와 dagster.css만 가져온 소비자에서 FAILURE/CANCELED run 또는 조회 오류를 렌더링한다. 해당 `color`와 `border` 선언이 computed-value 단계에서 무효가 되어 실패 강조와 오류 테두리가 적용되지 않는다. weather에서는 높은 specificity를 가진 무효 선언이 기존 오류 색상도 덮을 수 있다.

**영향:** 이번 공용 UI의 핵심인 실패·연결 장애 표시가 공통 토큰 계약을 따르지 못한다. 일반 소스 문자열 테스트나 Next 빌드는 이 오류를 검출하지 못한다.

**권고:** 두 곳 모두 `var(--kt-destructive)`로 교체한다. 실제 브라우저에서 error 영역의 border-width/color 및 실패 상태의 computed color를 확인한다. 선언에 사용하는 모든 `--kt-*`가 배포 tokens에 존재하는지도 점검한다.

### A-P2-02 — 복수 repository에서 동일한 schedule 이름을 구별할 수 없다

**위치:** common `packages/ui/src/dagster-operations.tsx:94`, `:133–140`; `DagsterOperationsProps.scheduleUrl`

`DagsterSnapshot.repositories`는 배열인데 schedules를 repository 정보 없이 펼친다. React key와 확장 상태는 `schedule.name`만 사용하며 URL callback에도 이름만 전달한다.

**재현:** 다음 두 repository를 하나의 scoped snapshot에 제공한다.

- `repo_a@location_a`: schedule `hourly`, job `collect_a`
- `repo_b@location_b`: schedule `hourly`, job `collect_b`

첫 행을 클릭하면 두 행 모두 확장된다. React key도 중복된다. 두 링크 모두 `scheduleUrl("hourly")`를 호출하므로 소비자는 어느 repository/location의 스케줄인지 판단할 수 없다.

**영향:** 현재 weather의 단일 repository에서는 드러나지 않지만, 공개 DTO가 허용하는 복수 repository에서는 잘못된 운영 링크·확장 상태가 발생한다. 다른 앱에 확산할 공용 컴포넌트의 계약상 결함이다.

**권고:** repository/location을 보존한 schedule 항목을 사용하고 composite identity로 key와 확장 상태를 관리한다. `scheduleUrl`에 schedule과 repository 문맥을 전달하는 호환 가능한 계약을 제공한다. 대안으로 단일 repository만 받는 계약을 명시하고 타입/검증으로 강제해야 한다. 동일 schedule 이름의 두 repository를 사용하는 회귀 시나리오가 필요하다.

### A-P3-01 — 신규 컴포넌트가 기존 공개 마크업 계약을 준수하지 않는다

**위치:** common `packages/ui/src/dagster-operations.tsx:105–150`; `docs/standards/ui-contract.md` UC-3.1

UC-3.1은 모든 컴포넌트 루트와 이름 있는 부분에 `data-slot`을 요구한다. 새 DagsterOperations에는 어떤 `data-slot`도 없다. `testId` prop도 제공되지 않는다. 소비자는 `.kt-dagster-operations`, `.ops-card` 등 계약에서 내부 구현으로 분류한 클래스에 의존해야 한다.

추가로 최근 실행 표의 마지막 column header가 빈 `<th scope="col" />`이다(`:124`). 링크 열에 의미 있는 header가 없어 보조 기술 사용자가 열 문맥을 확인하기 어렵다.

**영향:** 후속 소비자 e2e와 공용 UI 계약 검증이 안정된 selector를 사용할 수 없다. 새 표시 컴포넌트의 접근성 검사도 현재 신규 테스트에 포함되어 있지 않다.

**권고:** root 및 refresh/error/summary/run-table/schedule-table/detail에 문서화한 `data-slot`을 제공하고 선택 `testId`를 지원한다. 링크 열에 시각적으로 숨긴 “상세” 또는 “Dagster” header를 제공한다. 공개 계약과 tests를 함께 갱신한다.

### A-P3-02 — 공용 wrapper 도입 후 weather Dagster 페이지의 콘텐츠 여백이 제거된다

**위치:** weather `app/admin/dagster/page.tsx:38`; `app/globals.css`의 `.main > .panel`, `.main > .ops-grid` 등 direct-child margin 규칙

기존 페이지의 cards·panels는 `.main` 직계 자식이라 좌우 1.5rem 및 상단 여백을 받았다. 이제 실제 직계 자식은 `.kt-dagster-operations` wrapper인데 해당 selector가 weather gutter 규칙에 없다. `.main` 자체는 padding 0이며 공용 wrapper도 외부 margin이 없다.

**재현:** desktop/mobile에서 `/admin/dagster`를 연다. PageHeader는 기존 좌우 여백을 유지하지만 운영 UI wrapper의 panel/card는 content 경계까지 붙는다.

**영향:** 추출 과정에서 페이지 정렬과 반응형 외부 여백이 달라졌다. common 내부 간격과 소비자 페이지 여백의 책임이 연결되지 않았다.

**권고:** weather adapter에 app 소유 wrapper를 두거나 기존 gutter selector에 새 공용 root를 포함하고 desktop/mobile 규칙을 맞춘다. live e2e screenshot에서 header와 cards의 좌우 정렬을 확인한다.

## 검토한 공격 시나리오와 결과

- **공유 Dagster tenant 유출:** overview/failure 쿼리가 server 소유 selector/tag filter를 유지한다. 추가한 run tags 조회가 filter를 넓히지 않는다. raw GraphQL·scope override·mutation을 허용하는 새 경로를 찾지 못했다.
- **오래된 비동기 결과의 최신 화면 덮어쓰기:** weather requestVersion guard가 이전 응답 및 unmount 후 상태 변경을 차단한다.
- **조회 실패의 정상 빈 목록 오표시:** 기존 GraphQL union 검사를 유지한다. snapshot을 보존한 상태에서 error alert가 표시된다.
- **긴 batch의 정체 오탐:** 유한한 양수의 job별 maxRuntimeSeconds를 사용한다. 누락·0·음수·비유한 값에는 600초 fallback이 유지된다.
- **XSS:** 실패 문자열은 React text로 렌더링한다. `dangerouslySetInnerHTML`을 도입하지 않았다.
- **로그인·redirect:** shared form의 local-path sanitize 및 weather 성공 응답의 sanitize가 유지된다. consumer가 원격 서버 detail을 그대로 렌더링하지 않고 password를 finally에서 비운다. common inFlight guard는 중복 제출을 차단한다.
- **메뉴 상태와 auth ownership:** pathname/Next Link/weather 항목을 주입하고 logout API는 앱에 남겼다. 공용 메뉴가 자격 증명이나 권한 검증을 소유하는 새 결합을 찾지 못했다.
- **Python·DB 변경 전체 검토:** 정책 태그·schedule coalescing·주입 sensor·deadline·run owner migration·terminal/lease CAS·부분 publish와 예산 유지·native executor/instance 설정 및 새 tests를 읽었다. 본 reviewer 관점에서 추가 P0/P1은 찾지 못했다. 실제 process termination·daemon native retry·DB race의 런타임 검증은 수행하지 않았다.
- **배포 소비 계약:** Docker dependency stage의 vendor 복사, SHA로 고정된 Python Git 의존성, UI archive 출처/digest 문서를 확인했다.

## 증거와 미검증 경계

Manifest의 Python/UI/build/smoke 및 메모리 측정 결과는 **작성자가 제공한 기록**으로 읽었으며 독립 재실행 결과로 주장하지 않는다. 신규 공용 UI 테스트는 문자열·URL·확장·pending·긴 batch를 확인하지만 computed CSS, 동일 schedule 이름의 복수 repository, 신규 root의 공개 slots, table header 접근성은 검증하지 않는다.

다음은 **NOT_RUN**이다: live browser UI, axe 검사, desktop/mobile screenshot, 실제 auth cookie/login/logout 왕복, Docker clean build, 운영 Dagster 장애 주입, 공유 daemon 설정 반영, 다른 소비자 적용. 필수 live e2e 및 두 reviewer의 post-fix 재검토 후 merge 판단이 필요하다.
