# T-222 ui 0.3.0 전환 마감(현재 값 전환과 예고 필드 제거)

- 상태: BLOCKED
- 우선순위: P2
- Gate: 정책 검사·소비자 guard 확인·2인 리뷰
- 선행: T-221, T-416, T-424, T-435, T-466, T-474
- 외부 선행: geo·concierge(이번 조사 범위 밖)의 0.3.0 채택 PR. 두 저장소도 같은 guard의 소비자다
- 소유 저장소: kor-travel-common
- 병렬: 병렬 없음. 묶음의 마지막

출처는 [공통화 재조사·계획(2026-11-17)](../plan/commonization-plan-2026-11-17.md)의 §4.1·§4.8이다. 근거 위치(file:line)와 차이 분석은 그 문서가 정본이며 여기서 반복하지 않는다.

## 목표

소비자 채택이 끝나면 정책의 현재 값을 0.3.0으로 바꾸고 예고 필드를 지운다. 이 PR이 병합되는 순간 0.2.1에 남은 소비자는 어느 검사기로도 실패한다. 그래서 채택 확인이 선행이다.

## 고정 결정

- 창은 날짜가 아니라 이 PR이 닫는다(ADR-019). 공지한 마감 예정일 전에는 병합하지 않는다.
- 소비자 저장소를 이 task가 고치지 않는다. 채택이 안 된 저장소가 있으면 이 task는 BLOCKED로 남는다.

## 구현 범위

1. 소비자별 확인표: pinvi(T-424), map(T-415), weather(T-466), transport(T-435), docker-manager(T-474), geo·concierge. 각 저장소 main의 벤더 버전과 guard 호출 SHA를 적는다.
2. Map: T-416이 정확 Node/npm 핀을 채택했고 T-417로 호출 SHA를 올렸다면 T-415 병합을 확인한다. 채택하지 않았다면 Map은 창 동안 0.3.0을 받을 수 없다(옛 검사기는 현재 값만 읽는다). 그때는 T-415 PR이 검증을 마치고 대기 중인지 확인하고, 이 PR 병합 직후 T-415를 병합한다. 그 사이 Map의 guard는 실패한다는 것을 공지한다.
3. `versions.json`·`frontend-dependencies.json`·`frontend-artifacts.json`의 현재 값을 0.3.0으로 바꾸고 예고 값을 지운다.

## 범위 밖

소비자 저장소의 변경, 다음 버전의 예고.

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다.

```text
versions.json, frontend-dependencies.json, frontend-artifacts.json
docs/journal.md, docs/resume.md, docs/integration-map.md
```

## 수용 기준

- [ ] 확인표의 모든 소비자가 main에서 0.3.0을 벤더하고 있다(Map이 '직후 병합' 경로면 그 PR 링크와 검증 결과가 있다).
- [ ] 전환 뒤 0.3.0 소비자 fixture가 최신 검사기와 `97f8ed9` 검사기 모두에서 통과한다.
- [ ] `npm run check:policy`가 통과한다.

## 검증 명령

```bash
npm run check:policy && npm test --workspace packages/ui
```

## evidence

소비자 확인표(저장소·벤더 버전·호출 SHA·PR), 정책 검사 출력.

## rollback·release 차단 조건

- `git revert` 1회로 현재 값이 0.2.1, 예고가 0.3.0으로 돌아간다. 0.3.0 소비자는 최신 검사기에서 계속 통과한다.
