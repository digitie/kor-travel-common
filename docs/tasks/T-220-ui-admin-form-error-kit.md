# T-220 관리자 폼·도움말·오류 부품 묶음을 공통 UI로 이관

- 상태: BLOCKED
- 우선순위: P1
- Gate: UI 단위·타입·pack 설치·2인 리뷰
- 선행: T-219
- 소유 저장소: kor-travel-common
- 병렬: 병렬 없음

출처는 [공통화 재조사·계획(2026-11-17)](../plan/commonization-plan-2026-11-17.md)의 §3.5·§4.8(K-50·K-52)이다. 근거 위치(file:line)와 차이 분석은 그 문서가 정본이며 여기서 반복하지 않는다.

## 목표

T-219에 이어 폼 필드·도움말·오류 패널·구획 카드·필터 띠와 셸의 작은 조각을 옮긴다. 버전은 올리지 않는다.

## 고정 결정

- T-219와 같다.
- `help-tip`은 weather·transport 판(툴팁 억제 수정 포함)을 원천으로 한다. map 판보다 새 것이다.
- 셸 조각은 skip link와 header 띠, 접힘 선호 hook까지다. nav 내용·권한·로그아웃은 앱 소유다([ui-contract](../standards/ui-contract.md) §4.6).

## 구현 범위

1. 원천: `form-field-input`·`form-select`·`form-textarea`·`form-field-shared`, `help-tip`, `app-error-panel`과 `lib/error-recovery.ts`, `section-card`, `filter-bar`.
2. transport 사본과 다른 네 파일(`app-error-panel`·`filter-bar`·`section-card`·`status-label`)은 차이를 읽고 어느 쪽을 택했는지 PR에 적는다.
3. `AdminSkipLink`, `AdminPageHeader`, 접힘 선호 hook(저장 키는 인자).
4. 단위 시험과 exports 추가. `version`은 그대로.

## 범위 밖

버전 올림과 동결(T-221), 소비자 채택, 앱별 nav·로그아웃.

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다.

```text
packages/ui/src/{form-field-*,form-select,form-textarea,help-tip,app-error-panel,error-recovery,section-card,filter-bar,admin-skip-link,admin-page-header}.ts(x)
packages/ui/test/*.test.tsx, packages/ui/package.json  # exports만
PROVENANCE.md, docs/standards/ui-contract.md
```

## 수용 기준

- [ ] 부품이 하위 경로로 import되고 빌드·타입 검사가 통과한다.
- [ ] `AppErrorPanel`이 `role="alert"`와 재시도·이전 화면 동작을 갖는다는 시험이 있다.
- [ ] `HelpTip`의 접근성 이름(`도움말: {label}`)과 키보드 동작 시험이 있다.
- [ ] `version`과 `dependency-policy.json`이 바뀌지 않았다.

## 검증 명령

```bash
npm run build --workspace packages/ui && npm test --workspace packages/ui
python3 -B -X utf8 tools/check_spdx.py
```

## evidence

T-219와 같은 형식.

## rollback·release 차단 조건

- `git revert` 1회. 버전이 오르지 않았으므로 소비자 영향이 없다.
