# 공용 지도 작업면 계약 — 개발 후보 0.1.0-dev.7

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
