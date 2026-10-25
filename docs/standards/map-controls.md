# 공용 지도 작업면 계약 — 개발 후보 0.1.0-dev.8

## 이관 근거

사용자는 Map Feature 지도와 Transport 교통·유가 지도, Weather 날씨 지도의 폰트·컨트롤·
종류 아이콘·좌표/줌·상세 배치를 동일하게 요청했다. Map `974e2d025`의 Feature 작업면을
정본으로 추출하며 지도 엔진과 각 앱의 조회·선택·인증·저장 동작은 소비자가 소유한다.
세 소비자의 실제 채택 변경은 각각 `codex/shared-map-admin-ui` 브랜치에 둔다.

## 사용과 치수

React 19와 Base UI 1.8을 사용한다. `@kor-travel/ui/map-controls`에서 컴포넌트·타입을,
`@kor-travel/ui/map-controls.css`에서 범위가 한정된 스타일을 가져온다.
tokens의 `theme.css`와 기존 토큰 테마를 함께 불러온다.

- `MapFilterBar` 안에 아이콘 슬롯을 가진 `MapKindFilter`와 라벨이 연결된 `MapFilterField`를 둔다.
  종류는 문자열 배열을 받으며 toggle 콜백만 전달한다. 의미·조회 기준·기본값은 소비자 책임이다.
- 필터는 30px, 입력·출처 선택 기본 폭은 176px다. 라벨 12px, 필터 본문 13.5px를 사용한다.
  PC는 공간이 있으면 한 줄, 모바일은 종류를 한 줄 전체에 두고 나머지 필드를 나눈다.
- 다중 선택 칩은 높이 30px를 유지하며 선택 영역을 가로 스크롤한다. 팝업 항목의 기존 선택·해제는 유지한다.
- `MapTabs`·`MapViewTabs`·`MapTabPanel`은 Base UI의 키보드·ARIA 연결을 유지한다.
  Map의 목록 값 `table`도 지원한다. 방향키 포커스 뒤 Enter/Space로 선택한다.
- `MapReadout`은 건수와 `center 128.5316, 37.6031 · z 16.1` 형식의 실제 카메라 값을 함께 표시한다.
  카메라를 읽기 전에는 `null`로 지도 로딩 중을 표시하며 임의 좌표를 확정값으로 만들지 않는다.
- `kt-map-stage` 안의 `MapDetailOverlay`는 지도 위 오른쪽 패널이다. 내부 스크롤을 제공하며
  Escape는 패널 안에서만 dismiss한다. 닫기 버튼과 포커스 반환은 소비자가 연결한다.

## 검증과 배포 경계

WSL 내부 디스크에 동일 소스를 복사하여 `npm ci` 후 UI 전체54 테스트와 타입·패키지 고지 검사를
통과했다. NTFS 경로의 worker 시작 timeout은 성공으로 계산하지 않았다.
Weather 소비자375/1440px 브라우저에서 필터 높이/폭·PC 한 줄·종류 요청·실제 카메라·
상세 위치·Escape/포커스 반환·가로 overflow 검증2개를 통과했다.
각 소비자의 추가 검증·정확 커밋·tarball 해시는 채택 PR과 해당 저장소 vendor 문서에 남긴다.
운영 빌드·배포는 사용자 지시로 다른 에이전트가 통합하며 이 후보에서 재개하지 않는다.


## 남은 높이 작업면 — dev.8 선택 적용

기존 dev.7 컴포넌트의 props·기본값·CSS 경로·치수는 그대로다. 다음 컴포넌트를 새로
사용하는 작업면에서만 남은 높이 전달과 coarse 포인터의 44px 컨트롤을 적용한다.
공통 UI는 지도 엔진·키·조회·선택·저장·SDK resize를 소유하지 않는다.

| API | 선택 props | 계약 |
|---|---|---|
| `MapWorkspace` | 일반 `div` props·`style`·`ref` | 제한된 부모 높이를 자식 탭과 stage로 전달 |
| `MapFilterPanel` | `label="지도 필터"`, `expanded`, `onExpandedChange`, `triggerRef` | 폭640px 또는 높이480px 이하에서 기본 접힘, 그 밖에서는 본문 표시 |
| `MapStage` | `view="map"` 또는 `"list"`, `summary`, `detail`, 일반 `div` props | children은 canvas/목록, summary/detail은 분리된 상부 요약·상세 슬롯 |
| `MapDetailOverlay` 확장 | `header`, `collapsible=false`, `collapsed`, `onCollapsedChange` | header를 제공한 경우만 고정 header와 본문 스크롤을 사용 |

`MapFilterPanel.label`에는 현재 선택 조건 요약을 넣을 수 있다. 접기 때 본문 DOM과
입력값은 보존하며 CSS로만 숨긴다. 모바일로 전환하거나 외부에서 접을 때 본문 안의
초점은 보이는 trigger로 돌린다. `triggerRef`는 React 버튼 ref다. 넓고 높은 화면에서는 trigger가
숨겨지므로 소비자는 `getClientRects().length` 등으로 가시성을 확인한 뒤 지도 또는
원래 열기 버튼으로 복원한다. 상세 진입 초점·닫은 뒤 복원은 기존과 같이 소비자 소유다.

`MapDetailOverlay.header`를 제공하고 `onDismiss`를 연결하면 닫기 버튼이 생긴다.
기존 children 안에 닫기를 넣은 소비자는 header 방식으로 전환할 때 중복 버튼을 제거한다.
`collapsible`이 true면 접기 버튼이 생기며 본문 DOM/입력값을 유지한다. 외부에서 본문을
접었는데 내부에 초점이 있으면 접기 버튼으로 돌린다. Escape의 기존 소비자 콜백은 유지한다.

### 부모 높이 전달

```tsx
<div style={{ height: "100dvh", display: "flex", flexDirection: "column", minHeight: 0 }}>
  <header>운영 메뉴와 페이지 제목</header>
  <MapWorkspace>
    <MapFilterPanel label="필터 · 선택 조건">필터 내용</MapFilterPanel>
    <MapTabs defaultValue="map">
      <MapViewTabs viewport={viewport} count={count} />
      <MapTabPanel value="map">
        <MapStage summary={summary} detail={detail}>{canvasOrFallback}</MapStage>
      </MapTabPanel>
      <MapTabPanel value="list"><MapStage view="list">목록 내용</MapStage></MapTabPanel>
    </MapTabs>
  </MapWorkspace>
</div>
```

route shell→workspace→tabs→panel→stage의 flex/grid 경로에 `min-height:0`을 전달한다.
중간 소비자 wrapper가 있으면 그 wrapper도 flex:1/min-height:0을 제공한다.
자식 지도·fallback은 `height:100%`를 쓰고 앱의 64/70dvh·min28rem 중복은 제거한다.
Workspace 자체는 viewport 높이를 추측하지 않으며 임의 문서 흐름에서 자동 측정하지 않는다.
지도 뒤 시간표/비교는 route의 별도 영역 또는 접기 영역으로 나누고 높이 경계를 제공한다.
SDK의 기존 ResizeObserver가 실제 canvas 변경에 대응하며 공용 측정 hook을 추가하지 않는다.

Stage는 빈 자료·키 없음·WebGL 불가·로딩에도 같은 높이를 유지한다. map content는
스크롤하지 않고, list content만 단일 주 스크롤을 소유한다. 목록 자식에 별도 고정 높이와
중복 overflow:auto를 두지 않는다. 상세 본문은 별도의 문맥 스크롤이다.

요약은 고정 비율 제한 없이 자연 높이를 우선 사용한다. 상세가 없으면 안전 영역 전체를
사용할 수 있고, 상세가 있으면44px 동작과 header 여백을 먼저 보장한 뒤 요약과 본문을 배분한다.
전체 내용이 맞지 않는 경우에만 요약 자체를 스크롤한다. 긴 상세 header는 별도의 줄 수 제한 없이
사용 가능한 높이에서 스크롤하며 닫기·접기 버튼은 상단에 고정한다.
중요 오류/갱신 지연은 summary의 첫 항목에 둔다. overlay는 오른쪽44px+.75rem·아래24px+1.5rem을
비워 우측 지도 컨트롤과 하단 출처를 피한다. 소비자가 추가 컨트롤을 다른 위치에 둔다면
슬롯 바깥의 해당 앱 배치를 점검해야 한다. 요약/상세 자체의 과도한 고정 높이는 넣지 않는다.

### 공개 마크업

기존 data-slot은 보존한다. 새 슬롯은 `map-workspace`, `map-filter-panel`,
`map-filter-trigger`, `map-filter-panel-body`, `map-stage`, `map-stage-canvas`,
`map-stage-list`, `map-stage-summary`, `map-stage-detail`, `map-detail-header`,
`map-detail-body`다. stage의 `data-view`는 map/list, 필터의 `data-expanded`는 true/false다.
새 testid는 강제하지 않으며 일반 DOM props로 소비자가 추가할 수 있다.
긴 필터 label은 접힌 상태에서 한 줄로 줄이며 title과 접근 가능한 이름에 원문을 유지하고,
펼친 상태에서는 전체 label을 줄바꿈한다. 짧은 높이 조건과 focus 복원의 matchMedia 조건은 같다.

### 후보 검증

[설치 smoke 화면](../../packages/ui/smoke/next-app/app/map-workspace/page.tsx)과
[실브라우저 검사](../../packages/ui/smoke/map-workspace-browser.mjs)는 실제 API를 호출하지
않고 높이·접기·단일 스크롤·초점·기존 기본 스타일을 검사한다. 정확 산출물과 수치는
[검증 기록](../reports/2026-10-25-map-workspace.md)에 둔다. 소비자 실제 데이터/지도 SDK·
소비자 build/E2E·최종 두 독립 리뷰/CI는 별도 게이트다. registry/Release/운영 변경은 하지 않는다.
